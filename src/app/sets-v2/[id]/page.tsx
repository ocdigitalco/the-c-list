import { db, rawQuery } from "@/lib/db";
import {
  sets,
  players,
  insertSets,
  parallels,
  playerAppearances,
  appearanceCoPlayers,
} from "@/lib/schema";
import { eq, inArray, sql, and, asc } from "drizzle-orm";
import { notFound } from "next/navigation";
import Link from "next/link";
import { V2StatCard } from "@/components/sets-v2/V2StatCard";
import { V2Tabs } from "@/components/sets-v2/V2Tabs";
import { V2Checklist } from "@/components/sets-v2/V2Checklist";
import { V2Leaderboard } from "@/components/sets-v2/V2Leaderboard";
import { PackOddsCalculator, type PackOddsSlot, type BoxFormat } from "@/components/PackOddsCalculator";
import { BreakSheetModal, type BreakSheetPlayer } from "@/components/BreakSheetModal";
import type {
  InsertSetDetail,
  LeaderboardRow,
  BoxConfigSingle,
  BoxConfigMulti,
} from "@/components/sets-v2/types";

export const dynamic = "force-dynamic";

const BOX_LABEL_MAP: Record<string, string> = {
  hobby: "Hobby",
  jumbo: "Jumbo",
  mega: "Mega",
  blaster: "Blaster",
  value: "Value",
  fat_pack: "Fat Pack",
  hanger: "Hanger",
  breakers_delight: "Breaker's Delight",
  first_day_issue: "First Day Issue",
  breaker: "Breaker",
  hobby_hybrid: "Hobby Hybrid",
  sapphire: "Sapphire",
  hongbao: "Hongbao",
  logofractor: "Logofractor",
  ffnyc: "FFNYC",
};

function formatBoxLabel(key: string): string {
  return BOX_LABEL_MAP[key] ?? key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function isMultiConfig(cfg: BoxConfigSingle | BoxConfigMulti): cfg is BoxConfigMulti {
  const first = Object.values(cfg)[0];
  return first !== null && typeof first === "object";
}

// Classify insert set name for break sheet
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

  // Stats
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

  const numberedParallelsResult =
    insertSetIds.length > 0
      ? ((await rawQuery.get<{ total: number }>(
          `SELECT COUNT(*) AS total FROM parallels WHERE insert_set_id IN (${insertSetIds.map(() => "?").join(",")}) AND print_run IS NOT NULL`,
          ...insertSetIds
        )) ?? { total: 0 })
      : { total: 0 };

  const oneOfOnesResult =
    insertSetIds.length > 0
      ? ((await rawQuery.get<{ total: number }>(
          `SELECT COUNT(*) AS total FROM parallels WHERE insert_set_id IN (${insertSetIds.map(() => "?").join(",")}) AND print_run = 1`,
          ...insertSetIds
        )) ?? { total: 0 })
      : { total: 0 };

  // Rookies
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

  // All players
  const allPlayers = await db.query.players.findMany({
    where: (t, { eq }) => eq(t.setId, setId),
    orderBy: (p, { asc }) => [asc(p.name)],
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

  // ── Checklist data ──────────────────────────────────────────────────────────
  const insertSetRows =
    insertSetIds.length > 0
      ? await db
          .select({ id: insertSets.id, name: insertSets.name })
          .from(insertSets)
          .where(inArray(insertSets.id, insertSetIds))
          .orderBy(asc(insertSets.id))
      : [];

  const allAppearances =
    insertSetIds.length > 0
      ? await db
          .select({
            id: playerAppearances.id,
            insertSetId: playerAppearances.insertSetId,
            cardNumber: playerAppearances.cardNumber,
            team: playerAppearances.team,
            isRookie: playerAppearances.isRookie,
            subsetTag: playerAppearances.subsetTag,
            playerId: playerAppearances.playerId,
          })
          .from(playerAppearances)
          .where(inArray(playerAppearances.insertSetId, insertSetIds))
          .orderBy(asc(playerAppearances.cardNumber))
      : [];

  const appearanceIds = allAppearances.map((a) => a.id);
  const coPlayerRows =
    appearanceIds.length > 0
      ? await db
          .select({
            appearanceId: appearanceCoPlayers.appearanceId,
            coPlayerId: players.id,
            coPlayerName: players.name,
          })
          .from(appearanceCoPlayers)
          .innerJoin(players, eq(appearanceCoPlayers.coPlayerId, players.id))
          .where(inArray(appearanceCoPlayers.appearanceId, appearanceIds))
      : [];

  const coPlayersByAppearance = new Map<number, { id: number; name: string }[]>();
  for (const row of coPlayerRows) {
    if (!coPlayersByAppearance.has(row.appearanceId)) {
      coPlayersByAppearance.set(row.appearanceId, []);
    }
    coPlayersByAppearance.get(row.appearanceId)!.push({ id: row.coPlayerId, name: row.coPlayerName });
  }

  const allParallels =
    insertSetIds.length > 0
      ? await db
          .select()
          .from(parallels)
          .where(inArray(parallels.insertSetId, insertSetIds))
      : [];

  const parallelsByIS = new Map<number, { id: number; name: string; printRun: number | null }[]>();
  for (const p of allParallels) {
    if (!parallelsByIS.has(p.insertSetId)) {
      parallelsByIS.set(p.insertSetId, []);
    }
    parallelsByIS.get(p.insertSetId)!.push({ id: p.id, name: p.name, printRun: p.printRun });
  }

  // Build player name lookup
  const playerNameMap = new Map<number, string>();
  for (const p of allPlayers) {
    playerNameMap.set(p.id, p.name);
  }

  const checklistData: InsertSetDetail[] = insertSetRows.map((is) => {
    const apps = allAppearances.filter((a) => a.insertSetId === is.id);
    return {
      insertSetId: is.id,
      insertSetName: is.name,
      appearances: apps.map((a) => ({
        cardNumber: a.cardNumber,
        team: a.team,
        isRookie: a.isRookie,
        subsetTag: a.subsetTag,
        coPlayers: (coPlayersByAppearance.get(a.id) ?? []),
      })),
      parallels: parallelsByIS.get(is.id) ?? [],
    };
  });

  // ── Break Sheet data ────────────────────────────────────────────────────────
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
    breakMap.set(p.id, {
      autoSetNames: new Set(),
      hasMemAuto: false,
      hasRelic: false,
      insertSetNamesSet: new Set(),
    });
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

  // ── Box formats for pack odds ───────────────────────────────────────────────
  const hasBoxConfig = !!setRow.boxConfig;
  const hasPackOdds = !!setRow.packOdds;

  function singleToBoxFormat(
    label: string,
    fmt: BoxConfigSingle,
    note: string | undefined
  ): BoxFormat {
    const packsPerBox = fmt.packs_per_box ?? 1;
    const boxesPerCase = fmt.boxes_per_case ?? 8;
    const guaranteedAutos =
      fmt.autos_per_box ??
      fmt.autos_or_memorabilia_per_box ??
      fmt.autos_or_relics_per_box ??
      fmt.autos_or_auto_relics_per_box ??
      0;
    return {
      label,
      boxesPerCase,
      packsPerCase: boxesPerCase * packsPerBox,
      packsPerBox,
      guaranteedAutos,
      autoRowLabel:
        fmt.autos_or_memorabilia_per_box != null
          ? "Autograph or Memorabilia"
          : fmt.autos_or_relics_per_box != null
          ? "Autograph or Relic"
          : fmt.autos_or_auto_relics_per_box != null
          ? "Autograph or Relic"
          : undefined,
      note,
      totalPacksProduced: fmt.total_packs_produced ?? undefined,
    };
  }

  function buildNote(fmtPairs: { label: string; fmt: BoxConfigSingle }[]): string | undefined {
    const parts: string[] = [];
    for (const { label, fmt } of fmtPairs) {
      const guarantees: string[] = [];
      if (fmt.autos_or_memorabilia_per_box != null) {
        guarantees.push(`${fmt.autos_or_memorabilia_per_box} auto or memorabilia`);
      } else if (fmt.autos_or_relics_per_box != null) {
        guarantees.push(`${fmt.autos_or_relics_per_box} auto or relic`);
      } else {
        if (fmt.autos_per_box != null) guarantees.push(`${fmt.autos_per_box} auto`);
        if (fmt.nba_autos_per_box != null) guarantees.push(`${fmt.nba_autos_per_box} NBA auto`);
        if (fmt.ncaa_autos_per_box != null) guarantees.push(`${fmt.ncaa_autos_per_box} NCAA auto`);
        if (fmt.memorabilia_per_box != null) guarantees.push(`${fmt.memorabilia_per_box} memorabilia`);
        if (fmt.relics_per_box != null) guarantees.push(`${fmt.relics_per_box} relic`);
      }
      if (guarantees.length > 0)
        parts.push(`${label} boxes guarantee ${guarantees.join(" + ")} per box`);
    }
    if (parts.length === 0) return undefined;
    return parts.join(". ") + ". Odds shown are based on pack ratios.";
  }

  const rawBoxConfig = hasBoxConfig
    ? (JSON.parse(setRow.boxConfig!) as BoxConfigSingle | BoxConfigMulti)
    : null;

  const boxFormats: BoxFormat[] = (() => {
    if (!rawBoxConfig) return [];
    if (isMultiConfig(rawBoxConfig)) {
      const pairs = Object.entries(rawBoxConfig).map(([key, fmt]) => ({
        label: formatBoxLabel(key),
        fmt,
      }));
      const note = buildNote(pairs);
      return pairs.map(({ label, fmt }) => singleToBoxFormat(label, fmt, note));
    }
    const flat = rawBoxConfig as BoxConfigSingle;
    const note = buildNote([{ label: "Hobby", fmt: flat }]);
    return [singleToBoxFormat("Hobby", flat, note)];
  })();

  return (
    <div className="max-w-5xl mx-auto px-6 py-8 space-y-8">
      {/* Breadcrumb */}
      <div className="flex items-center gap-1.5">
        <Link
          href="/checklists"
          className="flex items-center gap-1 text-xs text-zinc-500 hover:text-zinc-300 transition-colors"
        >
          <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
          </svg>
          Checklists
        </Link>
      </div>

      {/* Stat cards */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
        <V2StatCard label="Insert Sets" value={insertSetIds.length} />
        <V2StatCard label="Athletes" value={athleteCountRow.count} />
        <V2StatCard label="Cards" value={cardCountRow.count} />
        <V2StatCard label="Numbered Parallels" value={numberedParallelsResult.total} />
        <V2StatCard label="1/1s" value={oneOfOnesResult.total} />
      </div>

      {/* Tabs */}
      <V2Tabs
        tabs={[
          {
            key: "overview",
            label: "Overview",
            content: (
              <div className="space-y-10">
                <V2Leaderboard entries={leaderboardEntries} hasTeamData={hasTeamData} setId={setId} />
                <V2Checklist setId={setId} insertSets={checklistData} />
              </div>
            ),
          },
          {
            key: "break-sheet",
            label: "Break Sheet",
            content: (
              <div className="flex justify-center pt-4">
                <BreakSheetModal
                  setName={setRow.name}
                  sport={setRow.sport}
                  league={setRow.league ?? null}
                  players={breakSheetPlayers}
                />
              </div>
            ),
          },
        ]}
        defaultTab="overview"
      />
    </div>
  );
}
