import { db, rawQuery } from "@/lib/db";
import {
  sets,
  players,
  insertSets,
  parallels,
  playerAppearances,
} from "@/lib/schema";
import { eq, inArray, sql, and } from "drizzle-orm";
import { notFound } from "next/navigation";
import { SetMetadataBar } from "@/components/sets-v2/SetMetadataBar";
import { StatCards } from "@/components/sets-v2/StatCards";
import { BoxConfigTable } from "@/components/sets-v2/BoxConfigTable";
import { PackOddsInline } from "@/components/sets-v2/PackOddsInline";
import { LeaderboardSidebar } from "@/components/sets-v2/LeaderboardSidebar";
import { RightSidebar } from "@/components/sets-v2/RightSidebar";
import { MobileLeaderboardDrawer } from "@/components/sets-v2/MobileLeaderboardDrawer";
import type { LeaderboardRow } from "@/components/sets-v2/types";
import type { BreakSheetPlayer } from "@/components/BreakSheetModal";

export const dynamic = "force-dynamic";

export default async function V2SetPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const setId = parseInt(id, 10);
  if (isNaN(setId)) notFound();

  const setRow = await db.query.sets.findFirst({
    where: (t, { eq }) => eq(t.id, setId),
  });
  if (!setRow) notFound();

  // Insert set IDs
  const insertSetIdRows = await db
    .select({ id: insertSets.id })
    .from(insertSets)
    .where(eq(insertSets.setId, setId));
  const insertSetIds = insertSetIdRows.map((r) => r.id);

  // ── Stats ─────────────────────────────────────────────────────────────────
  const [athleteCountRow] = await db
    .select({ count: sql<number>`cast(count(*) as integer)` })
    .from(players)
    .where(eq(players.setId, setId));

  const [cardCountRow] = await db
    .select({ count: sql<number>`cast(count(*) as integer)` })
    .from(playerAppearances)
    .where(
      insertSetIds.length > 0
        ? inArray(playerAppearances.insertSetId, insertSetIds)
        : sql`1 = 0`
    );

  const [parallelTypesRow] = await db
    .select({ count: sql<number>`cast(count(distinct ${parallels.name}) as integer)` })
    .from(parallels)
    .where(
      insertSetIds.length > 0 ? inArray(parallels.insertSetId, insertSetIds) : sql`1 = 0`
    );

  const totalParallelsResult =
    insertSetIds.length > 0
      ? ((await rawQuery.get<{ total: number }>(
          `SELECT COALESCE(SUM(apps * pars), 0) AS total FROM (
             SELECT
               (SELECT COUNT(*) FROM player_appearances WHERE insert_set_id = i.id) AS apps,
               (SELECT COUNT(*) FROM parallels WHERE insert_set_id = i.id) AS pars
             FROM insert_sets i
             WHERE i.id IN (${insertSetIds.map(() => "?").join(",")})
           )`,
          ...insertSetIds
        )) ?? { total: 0 })
      : { total: 0 };

  const autoInsertSetIds =
    insertSetIds.length > 0
      ? (
          await db
            .select({ id: insertSets.id })
            .from(insertSets)
            .where(
              and(
                inArray(insertSets.id, insertSetIds),
                sql`(
                  lower(${insertSets.name}) like '%auto%' or
                  lower(${insertSets.name}) like '%signature%' or
                  lower(${insertSets.name}) like '%signed%' or
                  lower(${insertSets.name}) like '%autograph%'
                )`
              )
            )
        ).map((r) => r.id)
      : [];

  const [autographCountRow] = await db
    .select({ count: sql<number>`cast(count(*) as integer)` })
    .from(playerAppearances)
    .where(
      autoInsertSetIds.length > 0
        ? inArray(playerAppearances.insertSetId, autoInsertSetIds)
        : sql`1 = 0`
    );

  const autoParallelsResult =
    autoInsertSetIds.length > 0
      ? ((await rawQuery.get<{ total: number }>(
          `SELECT COALESCE(SUM(apps * pars), 0) AS total FROM (
             SELECT
               (SELECT COUNT(*) FROM player_appearances WHERE insert_set_id = i.id) AS apps,
               (SELECT COUNT(*) FROM parallels WHERE insert_set_id = i.id) AS pars
             FROM insert_sets i
             WHERE i.id IN (${autoInsertSetIds.map(() => "?").join(",")})
           )`,
          ...autoInsertSetIds
        )) ?? { total: 0 })
      : { total: 0 };

  // Numbered parallels for right sidebar
  const numberedParallelsResult =
    insertSetIds.length > 0
      ? ((await rawQuery.get<{ total: number }>(
          `SELECT COUNT(*) AS total FROM parallels WHERE insert_set_id IN (${insertSetIds.map(() => "?").join(",")}) AND print_run IS NOT NULL`,
          ...insertSetIds
        )) ?? { total: 0 })
      : { total: 0 };

  // ── Break Sheet data ───────────────────────────────────────────────────────
  const allPlayers = await db.query.players.findMany({
    where: (t, { eq: e }) => e(t.setId, setId),
    orderBy: (p, { asc: a }) => [a(p.name)],
  });

  const rookieRows =
    insertSetIds.length > 0
      ? await db
          .selectDistinct({ playerId: playerAppearances.playerId })
          .from(playerAppearances)
          .where(
            and(
              eq(playerAppearances.isRookie, true),
              inArray(playerAppearances.insertSetId, insertSetIds)
            )
          )
      : [];
  const rookiePlayerIds = new Set(rookieRows.map((r) => r.playerId));

  function classifyIS(name: string): "base" | "pure_auto" | "mem_auto" | "relic" | "insert" {
    if (name === "Base Set") return "base";
    const lower = name.toLowerCase();
    const isAuto = /auto|autograph|signature|signed/.test(lower);
    const isRelic = /relic|memorabilia/.test(lower);
    if (isAuto && isRelic) return "mem_auto";
    if (isAuto) return "pure_auto";
    if (isRelic) return "relic";
    return "insert";
  }

  const allAppearancesForSheet =
    insertSetIds.length > 0
      ? await db
          .select({ playerId: playerAppearances.playerId, insertSetName: insertSets.name })
          .from(playerAppearances)
          .innerJoin(insertSets, eq(playerAppearances.insertSetId, insertSets.id))
          .where(
            and(
              inArray(playerAppearances.insertSetId, insertSetIds),
              sql`${insertSets.name} != 'Base Set'`
            )
          )
      : [];

  type PlayerBreakAccum = {
    autoSetNames: Set<string>;
    hasMemAuto: boolean;
    hasRelic: boolean;
    insertSetNamesSet: Set<string>;
  };
  const breakMap = new Map<number, PlayerBreakAccum>();
  for (const p of allPlayers) {
    breakMap.set(p.id, { autoSetNames: new Set(), hasMemAuto: false, hasRelic: false, insertSetNamesSet: new Set() });
  }
  for (const app of allAppearancesForSheet) {
    const e = breakMap.get(app.playerId);
    if (!e) continue;
    const type = classifyIS(app.insertSetName);
    if (type === "pure_auto") e.autoSetNames.add(app.insertSetName);
    else if (type === "mem_auto") e.hasMemAuto = true;
    else if (type === "relic") e.hasRelic = true;
    else if (type === "insert") e.insertSetNamesSet.add(app.insertSetName);
  }

  const breakSheetPlayers: BreakSheetPlayer[] = allPlayers.map((p) => {
    const d = breakMap.get(p.id)!;
    return {
      id: p.id,
      name: p.name,
      autoCount: d.autoSetNames.size,
      hasMemAuto: d.hasMemAuto,
      hasRelic: d.hasRelic,
      isRookie: rookiePlayerIds.has(p.id),
      insertSetNames: Array.from(d.insertSetNamesSet),
    };
  });

  // ── Leaderboard ─────────────────────────────────────────────────────────────
  const leaderboardRaw = await rawQuery.all<{
    id: number;
    name: string;
    totalCards: number;
    isRookie: number;
    team: string | null;
    autographs: number;
    inserts: number;
    numberedParallels: number;
  }>(
    `WITH player_is AS (
       SELECT DISTINCT pa.player_id, pa.insert_set_id
       FROM player_appearances pa
       INNER JOIN players p ON p.id = pa.player_id
       WHERE p.set_id = ?
     ),
     numbered AS (
       SELECT pis.player_id, COUNT(*) AS cnt
       FROM player_is pis
       INNER JOIN parallels par ON par.insert_set_id = pis.insert_set_id
       WHERE par.print_run IS NOT NULL
       GROUP BY pis.player_id
     )
     SELECT
       p.id,
       p.name,
       p.unique_cards AS totalCards,
       CAST(MAX(CASE WHEN pa.is_rookie = 1 THEN 1 ELSE 0 END) AS INTEGER) AS isRookie,
       MAX(pa.team) AS team,
       COUNT(DISTINCT CASE
         WHEN lower(i.name) LIKE '%auto%'
           OR lower(i.name) LIKE '%signature%'
           OR lower(i.name) LIKE '%signed%'
           OR lower(i.name) LIKE '%autograph%'
         THEN pa.insert_set_id END) AS autographs,
       COUNT(DISTINCT CASE
         WHEN i.name != 'Base Set'
           AND lower(i.name) NOT LIKE '%auto%'
           AND lower(i.name) NOT LIKE '%signature%'
           AND lower(i.name) NOT LIKE '%signed%'
           AND lower(i.name) NOT LIKE '%autograph%'
         THEN pa.insert_set_id END) AS inserts,
       COALESCE(n.cnt, 0) AS numberedParallels
     FROM players p
     LEFT JOIN player_appearances pa ON pa.player_id = p.id
     LEFT JOIN insert_sets i ON i.id = pa.insert_set_id
     LEFT JOIN numbered n ON n.player_id = p.id
     WHERE p.set_id = ?
     GROUP BY p.id
     ORDER BY p.unique_cards DESC`,
    setId,
    setId
  );

  const leaderboardEntries: LeaderboardRow[] = leaderboardRaw.map((r) => ({
    id: r.id,
    name: r.name,
    team: r.team,
    isRookie: r.isRookie === 1,
    totalCards: r.totalCards,
    autographs: r.autographs,
    inserts: r.inserts,
    numberedParallels: r.numberedParallels,
  }));

  const hasTeamData = leaderboardEntries.some((e) => e.team != null && e.team !== "");

  return (
    <div className="flex min-h-screen">
      {/* Left Sidebar — Leaderboard (desktop) */}
      <aside
        className="hidden lg:flex w-[350px] shrink-0 flex-col sticky top-0 h-screen overflow-hidden"
        style={{ borderRight: "1px solid var(--v2-border)" }}
      >
        <LeaderboardSidebar entries={leaderboardEntries} hasTeamData={hasTeamData} setId={setId} />
      </aside>

      {/* Center Main */}
      <main className="flex-1 min-w-0">
        <div className="max-w-4xl mx-auto px-6 py-6 space-y-6">
          {/* Mobile leaderboard toggle */}
          <div className="lg:hidden">
            <MobileLeaderboardDrawer
              entries={leaderboardEntries}
              hasTeamData={hasTeamData}
              setId={setId}
            />
          </div>

          <SetMetadataBar
            setName={setRow.name}
            sport={setRow.sport}
            tier={setRow.tier}
            athleteCount={athleteCountRow.count}
          />

          <StatCards
            cards={cardCountRow.count}
            parallelTypes={parallelTypesRow.count}
            totalParallels={totalParallelsResult.total}
            insertSets={insertSetIds.length}
            autographs={autographCountRow.count}
            autoParallels={autoParallelsResult.total}
          />

          {/* Box Configuration */}
          <section className="space-y-3">
            <h2 className="text-base font-semibold" style={{ color: "var(--v2-text-primary)" }}>
              Box Configuration
            </h2>
            <BoxConfigTable boxConfig={setRow.boxConfig ?? null} />
          </section>

          {/* Pack Odds */}
          <section className="space-y-3">
            <h2 className="text-base font-semibold" style={{ color: "var(--v2-text-primary)" }}>
              Pack Odds
            </h2>
            <PackOddsInline boxConfig={setRow.boxConfig ?? null} packOdds={setRow.packOdds ?? null} />
          </section>

          {/* Right sidebar content — mobile only */}
          <div className="xl:hidden">
            <RightSidebar
              releaseDate={setRow.releaseDate ?? null}
              hasCards={cardCountRow.count > 0}
              hasNumberedParallels={numberedParallelsResult.total > 0}
              hasBoxConfig={!!setRow.boxConfig}
              hasPackOdds={!!setRow.packOdds}
              sampleImageUrl={setRow.sampleImageUrl ?? null}
              setName={setRow.name}
              sport={setRow.sport}
              league={setRow.league ?? null}
              breakSheetPlayers={breakSheetPlayers}
            />
          </div>
        </div>
      </main>

      {/* Right Sidebar (desktop) */}
      <aside
        className="hidden xl:block w-[300px] shrink-0 sticky top-0 h-screen overflow-y-auto"
        style={{ borderLeft: "1px solid var(--v2-border)" }}
      >
        <RightSidebar
          releaseDate={setRow.releaseDate ?? null}
          hasCards={cardCountRow.count > 0}
          hasNumberedParallels={numberedParallelsResult.total > 0}
          hasBoxConfig={!!setRow.boxConfig}
          hasPackOdds={!!setRow.packOdds}
          sampleImageUrl={setRow.sampleImageUrl ?? null}
          setName={setRow.name}
          sport={setRow.sport}
          league={setRow.league ?? null}
          breakSheetPlayers={breakSheetPlayers}
        />
      </aside>
    </div>
  );
}
