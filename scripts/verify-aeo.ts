/** Temp verification for SEO/AEO overhaul. Run: npx tsx scripts/verify-aeo.ts */
import { rawQuery } from "../src/lib/db";
import { buildSetMeta, computeSetAeo } from "../src/lib/setSeo";

const SLUGS = [
  "2025-26-topps-signature-class-basketball",
  "2026-topps-cosmic-chrome-wwe",
  "2026-topps-disney-neon",
  "2025-26-topps-motif-basketball",
  "2026-topps-chrome-disney",
  "2025-topps-signature-class-football",
  "2026-topps-finest-baseball",
  "2025-topps-disneyland-70th-anniversary",
  "2025-topps-30-years-of-toy-story",
  "2026-topps-chrome-ufc",
];

async function main() {
  for (const slug of SLUGS) {
    const set = await rawQuery.get<{
      id: number; name: string; sport: string; release_date: string | null;
      pack_odds: string | null; box_config: string | null;
    }>(
      "SELECT id, name, sport, release_date, pack_odds, box_config FROM sets WHERE slug = ?",
      slug
    );
    if (!set) { console.log(`!! ${slug} not found`); continue; }

    const setId = set.id;
    const totalCards = (await rawQuery.get<{ c: number }>(
      `SELECT COUNT(*) AS c FROM player_appearances pa JOIN insert_sets i ON i.id = pa.insert_set_id WHERE i.set_id = ?`, setId
    ))!.c;
    const autographCount = (await rawQuery.get<{ c: number }>(
      `SELECT COUNT(*) AS c FROM player_appearances pa JOIN insert_sets i ON i.id = pa.insert_set_id WHERE i.set_id = ? AND i.is_autograph = 1`, setId
    ))!.c;
    const parallelTypes = (await rawQuery.get<{ c: number }>(
      `SELECT COUNT(DISTINCT p.name) AS c FROM parallels p JOIN insert_sets i ON i.id = p.insert_set_id WHERE i.set_id = ?`, setId
    ))!.c;
    const numberedParallels = (await rawQuery.get<{ c: number }>(
      `SELECT COUNT(*) AS c FROM parallels p JOIN insert_sets i ON i.id = p.insert_set_id WHERE i.set_id = ? AND p.print_run IS NOT NULL`, setId
    ))!.c;
    const allParallels = await rawQuery.all<{ name: string; printRun: number | null }>(
      `SELECT DISTINCT p.name, p.print_run AS printRun FROM parallels p JOIN insert_sets i ON i.id = p.insert_set_id WHERE i.set_id = ?`, setId
    );
    const role = await rawQuery.get<{ role: string }>(
      `SELECT subject_role AS role FROM players WHERE set_id = ? GROUP BY subject_role ORDER BY COUNT(*) DESC LIMIT 1`, setId
    );
    const leaderboard = await rawQuery.all<{
      id: number; name: string; totalCards: number; isRookie: number; team: string | null;
    }>(
      `SELECT p.id, p.name, p.unique_cards AS totalCards,
              CAST(MAX(CASE WHEN pa.is_rookie = 1 THEN 1 ELSE 0 END) AS INTEGER) AS isRookie,
              MAX(pa.team) AS team
       FROM players p LEFT JOIN player_appearances pa ON pa.player_id = p.id
       WHERE p.set_id = ? GROUP BY p.id ORDER BY p.unique_cards DESC`, setId
    );

    const meta = buildSetMeta(set.name, totalCards, !!set.pack_odds);
    const t0 = Date.now();
    const aeo = await computeSetAeo({
      setId, setName: set.name, sport: set.sport, releaseDate: set.release_date,
      packOdds: set.pack_odds, boxConfig: set.box_config,
      totalCards, autographCount, parallelTypes, numberedParallels, allParallels,
      subjectRole: role?.role ?? null,
      leaderboard: leaderboard.map((e) => ({ ...e, isRookie: e.isRookie === 1 })),
    });
    const ms = Date.now() - t0;

    console.log("=".repeat(100));
    console.log(`${set.name}  [${slug}]  (computed in ${ms}ms)`);
    console.log(`TITLE (${meta.title.length}): ${meta.title}`);
    console.log(`DESC (${meta.description.length}): ${meta.description}`);
    console.log(`\nSUMMARY: ${aeo.summary}\n`);
    for (const f of aeo.faqs) {
      console.log(`Q: ${f.q}`);
      console.log(`A: ${f.a}\n`);
    }
  }
  process.exit(0);
}

main().catch((e) => { console.error(e); process.exit(1); });
