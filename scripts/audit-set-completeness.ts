/**
 * Audit set completeness — READ-ONLY diagnostic.
 *
 * Surfaces incomplete sets across the local database so we can scope the
 * empty-subset problem first seen in 2025-26 Topps Chrome Cactus Jack
 * Basketball (7 of 10 subsets were empty placeholders).
 *
 * Runs against the LOCAL SQLite file (the-c-list.db) and performs NO writes.
 *
 * Usage: npx tsx scripts/audit-set-completeness.ts
 *
 * Checks:
 *   1. Empty subsets        — insert_sets rows with zero player_appearances.
 *   2. Worst-affected sets  — per-set roll-up of empty vs total subsets.
 *   3. Base sequence gaps   — missing integers in a base-tier subset's
 *                             numeric card-number sequence.
 *   4. Smallest sets        — bottom 20 by total card count.
 */

import { createClient } from "@libsql/client";

const db = createClient({ url: "file:the-c-list.db" });

// Base-tier detector, mirrored from src/lib/setSeo.ts: a subset whose name
// contains "base" as a discrete token and is NOT an autograph subset.
const BASE_TOKEN_RE = /(^|\W)base(\W|$)/i;
const AUTO_KEYWORD_RE = /auto|autograph|signature|signed|ink|script/i;

// Variation/parallel markers. Subsets matching these are intentionally sparse
// (only select base cards get an image/photo/team variation, a Funko crossover,
// a vintage-reprint variation, etc.), so their numeric "gaps" are expected and
// must be excluded from Check 3's genuine-drop detection.
const VARIATION_RE =
  /variation|image|photo|funko|parallel|sketch|short print|^sp\b|ssp/i;

// A main-base subset must be densely populated relative to its number range.
// Genuinely partitioned tiers (e.g. "Future Stars", "Short Prints") cover only
// a slice of the range and self-exclude below this threshold.
const MAIN_BASE_DENSITY = 0.7;

const rule = "=".repeat(72);
const thin = "-".repeat(72);

async function all<T = Record<string, unknown>>(sql: string): Promise<T[]> {
  const r = await db.execute(sql);
  return r.rows as unknown as T[];
}

// ── Check 1 — Empty subsets ─────────────────────────────────────────────────
async function emptySubsets() {
  const rows = await all<{
    slug: string | null;
    set_name: string;
    subset_id: number;
    subset_name: string;
  }>(`
    SELECT s.slug, s.name AS set_name, ins.id AS subset_id, ins.name AS subset_name
    FROM insert_sets ins
    JOIN sets s ON ins.set_id = s.id
    LEFT JOIN player_appearances pa ON pa.insert_set_id = ins.id
    GROUP BY ins.id
    HAVING COUNT(pa.id) = 0
    ORDER BY s.name, ins.name
  `);

  console.log(rule);
  console.log("1. EMPTY SUBSETS  (subset shells with zero cards)");
  console.log(rule);

  if (rows.length === 0) {
    console.log("None. Every subset has at least one card.\n");
    return;
  }

  // Group by set.
  const bySet = new Map<string, { setName: string; subsets: string[] }>();
  for (const r of rows) {
    const key = r.slug ?? `(no-slug) ${r.set_name}`;
    if (!bySet.has(key)) bySet.set(key, { setName: r.set_name, subsets: [] });
    bySet.get(key)!.subsets.push(r.subset_name);
  }

  for (const [slug, { setName, subsets }] of bySet) {
    console.log(`\n${setName}`);
    console.log(`  slug: ${slug}`);
    for (const sub of subsets) console.log(`    - ${sub}`);
  }

  console.log(`\n${thin}`);
  console.log(`TOTAL: ${rows.length} empty subsets across ${bySet.size} sets.\n`);
}

// ── Check 2 — Worst-affected sets ───────────────────────────────────────────
async function worstAffected() {
  const rows = await all<{
    slug: string | null;
    name: string;
    total_subsets: number;
    empty_subsets: number;
  }>(`
    SELECT s.slug, s.name,
      COUNT(DISTINCT ins.id) AS total_subsets,
      COUNT(DISTINCT CASE WHEN pa_count.cards IS NULL OR pa_count.cards = 0
                          THEN ins.id END) AS empty_subsets
    FROM sets s
    JOIN insert_sets ins ON ins.set_id = s.id
    LEFT JOIN (
      SELECT insert_set_id, COUNT(*) AS cards
      FROM player_appearances GROUP BY insert_set_id
    ) pa_count ON pa_count.insert_set_id = ins.id
    GROUP BY s.id
    HAVING empty_subsets > 0
    ORDER BY empty_subsets DESC, s.name
  `);

  console.log(rule);
  console.log("2. WORST-AFFECTED SETS  (most empty subsets first)");
  console.log(rule);

  if (rows.length === 0) {
    console.log("None.\n");
    return;
  }

  console.log(
    `\n${"empty/total".padEnd(12)}${"set".padEnd(52)}slug`
  );
  console.log(thin);
  for (const r of rows) {
    const ratio = `${r.empty_subsets}/${r.total_subsets}`.padEnd(12);
    const name = r.name.length > 50 ? r.name.slice(0, 49) + "…" : r.name;
    console.log(`${ratio}${name.padEnd(52)}${r.slug ?? "(no slug)"}`);
  }
  console.log("");
}

// ── Check 3 — Base sequence gaps ────────────────────────────────────────────
async function baseSequenceGaps() {
  // Pull every base-tier subset (token "base", not autograph) with its cards.
  const subsets = await all<{
    set_id: number;
    set_name: string;
    slug: string | null;
    subset_id: number;
    subset_name: string;
    is_autograph: number;
  }>(`
    SELECT s.id AS set_id, s.name AS set_name, s.slug, ins.id AS subset_id,
           ins.name AS subset_name, ins.is_autograph
    FROM insert_sets ins
    JOIN sets s ON ins.set_id = s.id
    ORDER BY s.name, ins.name
  `);

  console.log(rule);
  console.log("3. BASE SEQUENCE GAPS  (genuine drops in true main-base subsets)");
  console.log(rule);

  // Cleanly-numeric card numbers for a subset, or null if any are non-numeric.
  async function numericCards(subsetId: number): Promise<number[] | null> {
    const cards = await all<{ card_number: string }>(`
      SELECT card_number FROM player_appearances WHERE insert_set_id = ${subsetId}
    `);
    if (cards.length === 0) return null;
    const nums: number[] = [];
    for (const c of cards) {
      const t = (c.card_number ?? "").trim();
      if (!/^\d+$/.test(t)) return null; // skip mixed/non-numeric subsets
      nums.push(parseInt(t, 10));
    }
    return nums;
  }

  // Build, per set, the union of ALL numeric card numbers across every
  // base-tier subset (including variations / Future Stars / Short Prints).
  // A number housed in any sibling base-tier subset is "partitioned", not
  // dropped — so it must not be flagged as missing.
  const baseTierBySet = new Map<number, { sub: typeof subsets[number]; nums: number[] }[]>();
  for (const sub of subsets) {
    if (sub.is_autograph === 1) continue;
    if (!BASE_TOKEN_RE.test(sub.subset_name)) continue;
    if (AUTO_KEYWORD_RE.test(sub.subset_name)) continue;
    const nums = await numericCards(sub.subset_id);
    if (!nums) continue;
    if (!baseTierBySet.has(sub.set_id)) baseTierBySet.set(sub.set_id, []);
    baseTierBySet.get(sub.set_id)!.push({ sub, nums });
  }

  type Gap = {
    setName: string;
    slug: string | null;
    subsetName: string;
    missing: number[];
    min: number;
    max: number;
  };
  const gaps: Gap[] = [];

  for (const [, entries] of baseTierBySet) {
    // Pre-compute each sibling's range so we can tell true partitions
    // (complementary slices, e.g. "Future Stars") apart from same-range twins
    // (e.g. "Veteran Class Chrome Base", the chrome finish of the same 1–100
    // checklist). Only true partitions suppress a "missing" number — a twin
    // holding the number actually CONFIRMS the subject genuinely dropped it.
    const withRange = entries.map((e) => ({
      ...e,
      min: Math.min(...e.nums),
      max: Math.max(...e.nums),
    }));

    for (const subject of withRange) {
      const { sub, nums, min, max } = subject;

      // Exclude intentionally-sparse variation/parallel subsets by name.
      if (VARIATION_RE.test(sub.subset_name)) continue;

      const present = new Set(nums);
      const range = max - min + 1;

      // Density gate: genuine main-base subsets are densely populated. Sparse
      // partition tiers (Future Stars, etc.) fall below threshold and exclude
      // themselves even if the name didn't flag them.
      if (present.size / range < MAIN_BASE_DENSITY) continue;

      // Partition set: numbers held by sibling base-tier subsets that are NOT
      // same-range twins of the subject. A twin shares the subject's exact
      // [min,max]; excluding it keeps genuine drops visible.
      const partitionNumbers = new Set<number>();
      for (const sib of withRange) {
        if (sib === subject) continue;
        if (sib.min === min && sib.max === max) continue; // same-range twin
        for (const n of sib.nums) partitionNumbers.add(n);
      }

      // Report numbers absent from this subset AND from every true partition.
      const missing: number[] = [];
      for (let i = min; i <= max; i++) {
        if (!present.has(i) && !partitionNumbers.has(i)) missing.push(i);
      }
      if (missing.length > 0) {
        gaps.push({
          setName: sub.set_name,
          slug: sub.slug,
          subsetName: sub.subset_name,
          missing,
          min,
          max,
        });
      }
    }
  }

  gaps.sort((a, b) => a.setName.localeCompare(b.setName) || a.subsetName.localeCompare(b.subsetName));

  if (gaps.length === 0) {
    console.log("None. All true main-base sequences are contiguous.\n");
    return;
  }

  for (const g of gaps) {
    console.log(`\n${g.setName}  [${g.slug ?? "no slug"}]`);
    console.log(`  subset: ${g.subsetName}  (range ${g.min}–${g.max})`);
    const shown = g.missing.slice(0, 40).join(", ");
    const more = g.missing.length > 40 ? ` … (+${g.missing.length - 40} more)` : "";
    console.log(`  missing ${g.missing.length}: ${shown}${more}`);
  }
  console.log(`\n${thin}`);
  console.log(`TOTAL: ${gaps.length} true main-base subsets with genuine gaps.\n`);
}

// ── Check 4 — Smallest sets ─────────────────────────────────────────────────
async function smallestSets() {
  // player_appearances has no set_id; join through insert_sets.
  const rows = await all<{
    slug: string | null;
    name: string;
    total_cards: number;
    subsets: number;
  }>(`
    SELECT s.slug, s.name,
      COUNT(pa.id) AS total_cards,
      COUNT(DISTINCT ins.id) AS subsets
    FROM sets s
    LEFT JOIN insert_sets ins ON ins.set_id = s.id
    LEFT JOIN player_appearances pa ON pa.insert_set_id = ins.id
    GROUP BY s.id
    ORDER BY total_cards ASC, s.name
    LIMIT 20
  `);

  console.log(rule);
  console.log("4. SMALLEST SETS  (bottom 20 by card count — may be incomplete)");
  console.log(rule);
  console.log(
    `\n${"cards".padEnd(8)}${"subsets".padEnd(9)}${"set".padEnd(48)}slug`
  );
  console.log(thin);
  for (const r of rows) {
    const name = r.name.length > 46 ? r.name.slice(0, 45) + "…" : r.name;
    console.log(
      `${String(r.total_cards).padEnd(8)}${String(r.subsets).padEnd(9)}${name.padEnd(48)}${r.slug ?? "(no slug)"}`
    );
  }
  console.log("");
}

// ── Check 5 — Orphaned zero-card players ────────────────────────────────────
// A set must never list a player with zero cards. Clearing/rebuilding a set's
// appearances (e.g. a base rebuild) can leave the set-scoped player rows behind
// with no remaining player_appearances — these surface in the athlete list with
// zero cards. Players are set-scoped (players.set_id), so each orphan belongs to
// exactly one set and is safe to inspect per-set.
async function orphanedPlayers() {
  const rows = await all<{
    slug: string | null;
    name: string;
    orphan_players: number;
  }>(`
    SELECT s.slug, s.name, COUNT(*) AS orphan_players
    FROM players p
    JOIN sets s ON p.set_id = s.id
    WHERE NOT EXISTS (
      SELECT 1 FROM player_appearances pa WHERE pa.player_id = p.id
    )
    GROUP BY s.id
    HAVING orphan_players > 0
    ORDER BY orphan_players DESC, s.name
  `);

  console.log(rule);
  console.log("5. ORPHANED ZERO-CARD PLAYERS  (player rows with no appearances)");
  console.log(rule);

  if (rows.length === 0) {
    console.log("None. Every player row has at least one card.\n");
    return;
  }

  let total = 0;
  console.log(`\n${"orphans".padEnd(10)}${"set".padEnd(50)}slug`);
  console.log(thin);
  for (const r of rows) {
    total += r.orphan_players;
    const name = r.name.length > 48 ? r.name.slice(0, 47) + "…" : r.name;
    console.log(`${String(r.orphan_players).padEnd(10)}${name.padEnd(50)}${r.slug ?? "(no slug)"}`);
  }
  console.log(`\n${thin}`);
  console.log(`TOTAL: ${total} orphaned zero-card players across ${rows.length} sets.\n`);
}

async function main() {
  console.log("\nSET COMPLETENESS AUDIT  (read-only · local the-c-list.db)\n");
  await emptySubsets();
  await worstAffected();
  await baseSequenceGaps();
  await smallestSets();
  await orphanedPlayers();
  console.log(rule);
  console.log("End of report. No data was modified.");
  console.log(rule);
}

main()
  .then(() => process.exit(0))
  .catch((e) => {
    console.error(e);
    process.exit(1);
  });
