import { db, rawQuery } from "@/lib/db";
import { sets, players, insertSets, parallels, playerAppearances, appearanceCoPlayers } from "@/lib/schema";
import { eq, inArray, asc, sql, and } from "drizzle-orm";
import { notFound } from "next/navigation";
import Link from "next/link";
import { PlayerSidebar } from "@/components/PlayerSidebar";
import { InsertSetRow } from "@/components/InsertSetRow";
import { PlayerViewTracker } from "@/components/PlayerViewTracker";
import { PackOddsCalculator, type PackOddsSlot, type BoxFormat } from "@/components/PackOddsCalculator";
import { BreakCalcWarning } from "@/components/BreakCalcWarning";
import { BreakSheetModal, type BreakSheetPlayer } from "@/components/BreakSheetModal";
import { LeaderboardPanel, type LeaderboardEntry } from "@/components/LeaderboardPanel";

export const dynamic = "force-dynamic";

interface SearchParams {
  player?: string;
}

export default async function SetPage({
  params,
  searchParams,
}: {
  params: Promise<{ id: string }>;
  searchParams: Promise<SearchParams>;
}) {
  const { id } = await params;
  const setId = parseInt(id, 10);
  if (isNaN(setId)) notFound();

  const { player: playerIdStr } = await searchParams;
  const selectedPlayerId = playerIdStr ? parseInt(playerIdStr, 10) : null;

  // Fetch the parent set
  const setRow = await db.query.sets.findFirst({
    where: (t, { eq }) => eq(t.id, setId),
  });
  if (!setRow) notFound();

  // Collect all insert set IDs for this set (used across multiple queries)
  const insertSetIdRows = await db
    .select({ id: insertSets.id })
    .from(insertSets)
    .where(eq(insertSets.setId, setId));
  const insertSetIds = insertSetIdRows.map((r) => r.id);

  // Header strip stats
  const [insertSetCountRow] = await db
    .select({ count: sql<number>`cast(count(*) as integer)` })
    .from(insertSets)
    .where(eq(insertSets.setId, setId));

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

  // Total parallel cards = Σ(appearances × parallel_count) per insert set
  const totalParallelsResult =
    insertSetIds.length > 0
      ? ((await rawQuery.get<{ total: number }>(
            `SELECT COALESCE(SUM(apps * pars), 0) AS total FROM (
               SELECT
                 (SELECT COUNT(*) FROM player_appearances WHERE insert_set_id = i.id) AS apps,
                 (SELECT COUNT(*) FROM parallels           WHERE insert_set_id = i.id) AS pars
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

  // Auto parallels = Σ(appearances × parallel_count) scoped to auto insert sets
  const autoParallelsResult =
    autoInsertSetIds.length > 0
      ? ((await rawQuery.get<{ total: number }>(
            `SELECT COALESCE(SUM(apps * pars), 0) AS total FROM (
               SELECT
                 (SELECT COUNT(*) FROM player_appearances WHERE insert_set_id = i.id) AS apps,
                 (SELECT COUNT(*) FROM parallels           WHERE insert_set_id = i.id) AS pars
               FROM insert_sets i
               WHERE i.id IN (${autoInsertSetIds.map(() => "?").join(",")})
             )`,
            ...autoInsertSetIds
          )) ?? { total: 0 })
      : { total: 0 };

  const setStats = {
    insertSets: insertSetCountRow.count,
    athletes: athleteCountRow.count,
    cards: cardCountRow.count,
    parallelTypes: parallelTypesRow.count,
    totalParallels: totalParallelsResult.total,
    autographs: autographCountRow.count,
    autoParallels: autoParallelsResult.total,
  };

  // Players for the sidebar, scoped to this set
  const allPlayers = await db.query.players.findMany({
    where: (t, { eq }) => eq(t.setId, setId),
    orderBy: (p, { asc }) => [asc(p.name)],
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

  // ── Break Sheet data ────────────────────────────────────────────────────────
  // Classify each insert set name into one of: base | pure_auto | mem_auto | relic | insert
  function classifyIS(name: string): "base" | "pure_auto" | "mem_auto" | "relic" | "insert" {
    if (name === "Base Set") return "base";
    const lower = name.toLowerCase();
    const isAuto  = /auto|autograph|signature|signed/.test(lower);
    const isRelic = /relic|memorabilia/.test(lower);
    if (isAuto && isRelic) return "mem_auto";
    if (isAuto)  return "pure_auto";
    if (isRelic) return "relic";
    return "insert";
  }

  // One row per player-appearance (excluding Base Set to reduce rows fetched)
  const allAppearancesForSheet = insertSetIds.length > 0
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

  // Aggregate per-player: distinct pure-auto set count, mem-auto flag, relic flag, insert names
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
    else if (type === "relic")    e.hasRelic = true;
    else if (type === "insert")   e.insertSetNamesSet.add(app.insertSetName);
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

  const sidebarPlayers = allPlayers.map((p) => ({
    id: p.id,
    name: p.name,
    totalCards: p.uniqueCards,
    hasRookie: rookiePlayerIds.has(p.id),
  }));

  // Selected player detail
  let playerView: {
    id: number;
    name: string;
    uniqueCards: number | null;
    totalPrintRun: number | null;
    oneOfOnes: number | null;
    insertSetCount: number | null;
    hasRookie: boolean;
    teams: (string | null)[];
    insertSets: {
      insertSetId: number;
      insertSetName: string;
      appearances: {
        cardNumber: string;
        team: string | null;
        isRookie: boolean;
        subsetTag: string | null;
        coPlayers: { id: number; name: string }[];
      }[];
      parallels: { id: number; name: string; printRun: number | null }[];
    }[];
  } | null = null;
  if (selectedPlayerId) {
    const playerData = await db.query.players.findFirst({
      where: (t, { eq }) => eq(t.id, selectedPlayerId),
    });

    if (playerData && playerData.setId === setId) {
      const appearanceRows = await db
        .select({
          id: playerAppearances.id,
          cardNumber: playerAppearances.cardNumber,
          team: playerAppearances.team,
          isRookie: playerAppearances.isRookie,
          subsetTag: playerAppearances.subsetTag,
          insertSetId: playerAppearances.insertSetId,
          insertSetName: insertSets.name,
        })
        .from(playerAppearances)
        .innerJoin(insertSets, eq(playerAppearances.insertSetId, insertSets.id))
        .where(eq(playerAppearances.playerId, selectedPlayerId))
        .orderBy(asc(playerAppearances.cardNumber));

      const appearanceIds = appearanceRows.map((a) => a.id);
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

      const playerInsertSetIds = [
        ...new Set(appearanceRows.map((a) => a.insertSetId)),
      ];

      const parallelsByInsertSet = new Map<
        number,
        { id: number; name: string; printRun: number | null }[]
      >();
      if (playerInsertSetIds.length > 0) {
        const parallelRows = await db
          .select()
          .from(parallels)
          .where(inArray(parallels.insertSetId, playerInsertSetIds));
        for (const row of parallelRows) {
          if (!parallelsByInsertSet.has(row.insertSetId)) {
            parallelsByInsertSet.set(row.insertSetId, []);
          }
          parallelsByInsertSet.get(row.insertSetId)!.push(row);
        }
      }

      const teams = [...new Set(appearanceRows.map((a) => a.team).filter(Boolean))];

      const insertSetMap = new Map<
        number,
        {
          insertSetId: number;
          insertSetName: string;
          appearances: {
            cardNumber: string;
            team: string | null;
            isRookie: boolean;
            subsetTag: string | null;
            coPlayers: { id: number; name: string }[];
          }[];
          parallels: { id: number; name: string; printRun: number | null }[];
        }
      >();

      for (const appearance of appearanceRows) {
        const key = appearance.insertSetId;
        if (!insertSetMap.has(key)) {
          insertSetMap.set(key, {
            insertSetId: key,
            insertSetName: appearance.insertSetName,
            appearances: [],
            parallels: parallelsByInsertSet.get(key) ?? [],
          });
        }
        insertSetMap.get(key)!.appearances.push({
          cardNumber: appearance.cardNumber,
          team: appearance.team,
          isRookie: appearance.isRookie,
          subsetTag: appearance.subsetTag,
          coPlayers: coPlayersByAppearance.get(appearance.id) ?? [],
        });
      }

      playerView = {
        id: playerData.id,
        name: playerData.name,
        uniqueCards: playerData.uniqueCards,
        totalPrintRun: playerData.totalPrintRun,
        oneOfOnes: playerData.oneOfOnes,
        insertSetCount: playerData.insertSetCount,
        hasRookie: appearanceRows.some((a) => a.isRookie),
        teams,
        insertSets: Array.from(insertSetMap.values()),
      };
    }
  }

  // Break Hit Calculator — detect available data
  const hasBoxConfig = !!setRow.boxConfig;
  const hasPackOdds = !!setRow.packOdds;

  // box_config supports two shapes:
  //   flat:        { cards_per_pack, packs_per_box, boxes_per_case, ... }
  //   multi-format: { hobby?: {...}, jumbo?: {...}, mega?: {...}, blaster?: {...} }
  //
  // When a set has both hobby and jumbo keys, the calculator shows a toggle.
  // Otherwise the calculator uses hobby (if present) or the flat config.
  type BoxConfigSingle = {
    cards_per_pack?: number;
    packs_per_box?: number;
    boxes_per_case: number;
    autos_or_memorabilia_per_box?: number;
    autos_or_relics_per_box?: number;
    autos_per_box?: number;
    memorabilia_per_box?: number;
    relics_per_box?: number;
    [key: string]: number | undefined;
  };
  type BoxConfigMulti = Record<string, BoxConfigSingle>;

  const rawBoxConfig = hasBoxConfig
    ? (JSON.parse(setRow.boxConfig!) as BoxConfigSingle | BoxConfigMulti)
    : null;

  // Build a shared note from all relevant formats (hobby + jumbo guarantees)
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

  function singleToBoxFormat(label: string, fmt: BoxConfigSingle, note: string | undefined): BoxFormat {
    const packsPerBox = fmt.packs_per_box ?? 1;
    // Extract guaranteed auto (or auto-or-relic) hits per box
    const guaranteedAutos =
      fmt.autos_per_box ??
      fmt.autos_or_memorabilia_per_box ??
      fmt.autos_or_relics_per_box ??
      0;
    return {
      label,
      boxesPerCase: fmt.boxes_per_case,
      packsPerCase: fmt.boxes_per_case * packsPerBox,
      packsPerBox,
      guaranteedAutos,
      autoRowLabel: fmt.autos_or_memorabilia_per_box != null
        ? "Autograph or Memorabilia"
        : fmt.autos_or_relics_per_box != null
        ? "Autograph or Relic"
        : undefined,
      note,
    };
  }

  // Map box config keys to display labels.
  // Snake_case keys get special-cased; everything else is title-cased.
  const BOX_LABEL_MAP: Record<string, string> = {
    hobby: "Hobby",
    jumbo: "Jumbo",
    mega: "Mega",
    blaster: "Blaster",
    breakers_delight: "Breaker's Delight",
    first_day_issue: "First Day Issue",
    breaker: "Breaker",
    hobby_hybrid: "Hobby Hybrid",
  };
  function formatBoxLabel(key: string): string {
    return BOX_LABEL_MAP[key] ?? key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
  }

  // Detect multi-format: any value that is an object with box config fields
  function isMultiConfig(cfg: BoxConfigSingle | BoxConfigMulti): cfg is BoxConfigMulti {
    const first = Object.values(cfg)[0];
    return first !== null && typeof first === "object";
  }

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
    // Flat config
    const flat = rawBoxConfig as BoxConfigSingle;
    const note = buildNote([{ label: "Hobby", fmt: flat }]);
    return [singleToBoxFormat("Hobby", flat, note)];
  })();

  // Some sets use different naming in pack_odds than the insert set name.
  // These overrides map insert set names → the key prefix used in the pack_odds JSON.
  const ODDS_KEY_OVERRIDES: Record<string, string> = {
    // 2025 Topps Chrome Baseball / Heritage overrides
    "Base Chrome": "Base Chrome Variations",
    "Base Chrome Autographs": "Base Chrome Autograph Variations",
    "Clubhouse Collection Autographed Relics": "Clubhouse Collection Autograph Relics",
    "Clubhouse Collection Dual Autographed Relics": "Clubhouse Collection Dual Autograph Relics",
    "Flashbacks Autographed Relics": "Flashback Autographed Relics",
    // 2025 Bowman's Best Baseball overrides
    "Best Of 2025 Autographs": "Best of 2025 Autographs",
    "Best Tek": "Best-Tek",
    "Best Tek Autographs": "Best-Tek Autographs",
    "Best Mix Autographs": "Best Mix Autograph Diecuts",
    "Prospect Patch Autographs": "Prospect Patch Autograph",
    "Strokes Of Gold": "Strokes of Gold",
    // 2025-26 Topps Basketball overrides
    "1980-81 Topps Basketball": "1980-81 Topps Basketball Insert",
    "1980-81 Topps Basketball Autographs": "1980-81 Topps Basketball Autograph",
    "1980-81 Topps Basketball Triple Autographs": "1980-81 Topps Basketball Triple Autograph",
    "1980-81 Topps Rookie Autographs": "1980-81 Topps Basketball Rookie Autograph",
    "Flagship Real One Autographs – Spike Lee": "Flagship Real One Spike Lee Autograph",
    "Flagship Real One Relics": "Flagship Real One Relic",
    "Flagship Real Ones Autographs": "Flagship Real One Autograph",
    "Flagship Real Ones Rookie Autographs": "Flagship Real One Rookie Autograph",
    "Own The Game": "Own the Game",
    "Rookie Photo Shoot Autographs": "Rookie Photo Shoot Autograph",
    "Rookie Photo Shoot Dual Autographs": "Rookie Photo Shoot Dual Autograph",
    "Social Media Follow Back Redemptions": "Social Follow Back Redemption",
    "Stars of the NBA": "Stars of NBA",
    "Team Color Border Variation": "Base Team Color Border Variation",
    "Golden Mirror Image Variations": "Base Golden Mirror Image Variations",
    "Clear Variation": "Base Clear Variation",
    "Player Number Variation": "Base Player Number Variation",
    // 2026 Topps Finest Premier League overrides
    "Finest Partnerships": "Finest Partnerships Dual Autographs",
    // 2025-26 Topps Finest Basketball overrides
    "Finest Autographs": "Autographs",
    "Finest Rookie Autographs": "Rookie Autographs",
  };

  // Build PackOddsCalculator slot data for the selected player (all sets)
  const autoKeywords = ["auto", "signature", "graph", "relic"];
  const packOddsSlotsByFormat: Record<string, PackOddsSlot[]> = {};
  if (playerView && hasPackOdds) {
    const rawOdds = JSON.parse(setRow.packOdds!);

    // Detect nested format: { hobby: { key: number }, jumbo: { key: number } }
    const firstVal = Object.values(rawOdds)[0];
    const isNestedOdds = firstVal !== null && typeof firstVal === "object";

    // Total distinct players per insert set (for player_share = 1/totalApps)
    const playerISIds = playerView.insertSets.map((is) => is.insertSetId);
    const totalAppsByIS = new Map<number, number>();
    if (playerISIds.length > 0) {
      const rows = await rawQuery.all<{ insert_set_id: number; total_apps: number }>(
        `SELECT insert_set_id, COUNT(DISTINCT card_number) AS total_apps
         FROM player_appearances
         WHERE insert_set_id IN (${playerISIds.map(() => "?").join(",")})
         GROUP BY insert_set_id`,
        ...playerISIds
      );
      for (const row of rows) totalAppsByIS.set(row.insert_set_id, row.total_apps);
    }

    function buildSlots(packOddsData: Record<string, number>): PackOddsSlot[] {
      return playerView!.insertSets.map((is) => {
        const isAuto = autoKeywords.some((kw) => is.insertSetName.toLowerCase().includes(kw));
        const prefix = is.insertSetName === "Base Set"
          ? "Base"
          : (ODDS_KEY_OVERRIDES[is.insertSetName] ?? is.insertSetName);
        const baseKey = is.insertSetName === "Base Set" ? null : prefix;
        // Some sets (e.g. Electrifying Signatures) have no plain base key in pack odds;
        // their base entry uses a suffix like " Geometric". Try fallback.
        const baseDenom = baseKey
          ? (packOddsData[baseKey] ?? packOddsData[`${baseKey} Geometric`] ?? null)
          : null;
        return {
          insertSetName: is.insertSetName,
          playerApps: is.appearances.length,
          totalApps: totalAppsByIS.get(is.insertSetId) ?? 0,
          baseOddsDenom: baseDenom,
          isAuto,
          serializedParallels: is.parallels
            .filter((p) => p.printRun !== null)
            .map((p) => ({
              name: p.name,
              printRun: p.printRun!,
              denom: packOddsData[`${prefix} ${p.name}`] ?? null,
            })),
        };
      });
    }

    // Map pack-odds JSON keys to the box-format labels used by the calculator.
    // Needed when the odds key differs from the box-config key (e.g. "breaker"
    // odds correspond to the "breakers_delight" box config → "Breaker's Delight").
    const ODDS_TO_FORMAT_LABEL: Record<string, string> = {
      breaker: "Breaker's Delight",
    };

    if (isNestedOdds) {
      // Nested odds: { hobby: {...}, jumbo: {...} }
      for (const [key, data] of Object.entries(rawOdds as Record<string, Record<string, number>>)) {
        const label = ODDS_TO_FORMAT_LABEL[key] ?? formatBoxLabel(key);
        packOddsSlotsByFormat[label] = buildSlots(data);
      }
    } else {
      // Flat odds: shared across all box formats
      const slots = buildSlots(rawOdds as Record<string, number>);
      for (const fmt of boxFormats) {
        packOddsSlotsByFormat[fmt.label] = slots;
      }
      // Fallback if no boxFormats defined
      if (boxFormats.length === 0) packOddsSlotsByFormat["default"] = slots;
    }
  }

  // ── Auto guaranteed-slot data ───────────────────────────────────────────────
  // Total auto cards across the entire set (for the guaranteed-slot auto model).
  const autoFilter = `(LOWER(i.name) LIKE '%auto%' OR LOWER(i.name) LIKE '%signature%' OR LOWER(i.name) LIKE '%graph%' OR LOWER(i.name) LIKE '%relic%')`;
  const totalAutoCards = (
    await rawQuery.get<{ n: number }>(
      `SELECT COUNT(*) AS n
       FROM player_appearances pa
       JOIN insert_sets i ON pa.insert_set_id = i.id
       WHERE i.set_id = ? AND ${autoFilter}`,
      setRow.id
    )
  )?.n ?? 0;

  // This player's auto card count
  const playerAutoCards = playerView
    ? playerView.insertSets
        .filter((is) => autoKeywords.some((kw) => is.insertSetName.toLowerCase().includes(kw)))
        .reduce((sum, is) => sum + is.appearances.length, 0)
    : 0;

  // ── Leaderboard data ────────────────────────────────────────────────────────
  // Use a CTE to pre-compute numbered parallel counts per player so we avoid
  // a correlated subquery that would run once per join-row and lock SQLite.
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
       p.unique_cards                                                        AS totalCards,
       CAST(MAX(CASE WHEN pa.is_rookie = 1 THEN 1 ELSE 0 END) AS INTEGER)   AS isRookie,
       MAX(pa.team)                                                          AS team,
       COUNT(DISTINCT CASE
         WHEN lower(i.name) LIKE '%auto%'
           OR lower(i.name) LIKE '%signature%'
           OR lower(i.name) LIKE '%signed%'
           OR lower(i.name) LIKE '%autograph%'
         THEN pa.insert_set_id END)                                         AS autographs,
       COUNT(DISTINCT CASE
         WHEN i.name != 'Base Set'
           AND lower(i.name) NOT LIKE '%auto%'
           AND lower(i.name) NOT LIKE '%signature%'
           AND lower(i.name) NOT LIKE '%signed%'
           AND lower(i.name) NOT LIKE '%autograph%'
         THEN pa.insert_set_id END)                                         AS inserts,
       COALESCE(n.cnt, 0)                                                   AS numberedParallels
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
  const leaderboardEntries: LeaderboardEntry[] = leaderboardRaw.map((r) => ({
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
    <div className="flex flex-col h-full">
      {/* Set info header strip */}
      <div className="shrink-0 border-b border-zinc-800 bg-zinc-900/50 px-5 py-3">
        {/* Breadcrumb */}
        <div className="flex items-center gap-1.5 mb-2">
          <Link
            href="/checklists"
            className="flex items-center gap-1 text-xs text-zinc-500 hover:text-zinc-300 transition-colors"
          >
            <svg
              className="w-3 h-3"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2.5}
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
            </svg>
            Checklists
          </Link>
        </div>

        {/* Set name + stats + break sheet button */}
        <div className="flex items-center justify-between gap-4">
          <div className="flex flex-wrap items-center gap-x-5 gap-y-1.5 min-w-0">
            <div className="flex items-center gap-2">
              <span className="text-sm font-semibold text-white">{setRow.name}</span>
              <span className="text-xs text-zinc-500">{setRow.season}</span>
              {setRow.league && (
                <span className="text-xs font-medium text-zinc-500 bg-zinc-800 border border-zinc-700 px-1.5 py-0.5 rounded">
                  {setRow.league}
                </span>
              )}
              {setRow.tier && setRow.tier !== "Standard" && (
                <span className="text-xs font-medium text-slate-300 bg-slate-800 border border-slate-600/50 px-1.5 py-0.5 rounded">
                  {setRow.tier}
                </span>
              )}
            </div>
            <div className="flex items-center gap-4 text-xs text-zinc-500">
              <StatChip value={setStats.athletes} label="athletes" />
              <StatChip value={setStats.cards} label="cards" />
              <StatChip value={setStats.insertSets} label="insert sets" />
              <StatChip value={setStats.parallelTypes} label="parallel types" />
              <StatChip value={setStats.totalParallels} label="total parallels" />
              <StatChip value={setStats.autographs} label="autographs" />
              <StatChip value={setStats.autoParallels} label="autograph parallels" />
            </div>
          </div>
          <div className="flex items-center gap-2 shrink-0">
            <LeaderboardPanel
              entries={leaderboardEntries}
              hasTeamData={hasTeamData}
              setId={setId}
            />
            <Link
              href={`/sets/${setId}/odds`}
              className="flex items-center gap-1.5 text-xs font-medium text-zinc-400 hover:text-white border border-zinc-700 hover:border-zinc-500 bg-zinc-900 hover:bg-zinc-800 px-3 py-1.5 rounded-md transition-colors"
            >
              <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 18 9 11.25l4.306 4.306a11.95 11.95 0 0 1 5.814-5.518l2.74-1.22m0 0-5.94-2.281m5.94 2.28-2.28 5.941" />
              </svg>
              Pack Odds
            </Link>
            <BreakSheetModal
              setName={setRow.name}
              sport={setRow.sport}
              league={setRow.league ?? null}
              players={breakSheetPlayers}
            />
          </div>
        </div>
      </div>

      {/* Split pane */}
      <div className="flex flex-1 overflow-hidden">
        <PlayerSidebar
          players={sidebarPlayers}
          selectedPlayerId={selectedPlayerId}
          setId={setId}
        />

        {/* Main panel */}
        <div className="flex-1 overflow-y-auto">
          {playerView ? (
            <div className="max-w-3xl mx-auto px-6 py-8 space-y-7">
              <PlayerViewTracker playerId={playerView.id} />
              <div className="flex items-start justify-between gap-4">
                <div>
                  <h1 className="text-3xl font-bold text-white tracking-tight">
                    {playerView.name}
                  </h1>
                  {playerView.teams.length > 0 && (
                    <p className="text-zinc-400 mt-1.5 text-sm">
                      {playerView.teams.join(" · ")}
                    </p>
                  )}
                </div>
                {playerView.hasRookie && (
                  <span className="text-xs font-semibold text-amber-400 bg-amber-400/10 px-2 py-1 rounded mt-1 shrink-0">
                    Rookie
                  </span>
                )}
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                <StatCard label="Insert Sets" value={playerView.insertSetCount ?? 0} />
                <StatCard label="Unique Cards" value={playerView.uniqueCards ?? 0} />
                <StatCard label="Numbered Parallels" value={playerView.totalPrintRun ?? 0} />
                <StatCard
                  label="1/1s"
                  value={playerView.oneOfOnes ?? 0}
                  highlight={(playerView.oneOfOnes ?? 0) > 0}
                />
              </div>

              {/* Break Hit Calculator */}
              {(!hasBoxConfig || !hasPackOdds) ? (
                <BreakCalcWarning
                  missingBoxConfig={!hasBoxConfig}
                  missingPackOdds={!hasPackOdds}
                />
              ) : Object.keys(packOddsSlotsByFormat).length > 0 ? (
                <PackOddsCalculator
                  slotsByFormat={packOddsSlotsByFormat}
                  boxFormats={boxFormats}
                  totalAutoCards={totalAutoCards}
                  playerAutoCards={playerAutoCards}
                />
              ) : null}

              <div>
                <h2 className="text-xs font-semibold text-zinc-500 uppercase tracking-widest mb-3">
                  Insert Sets
                </h2>
                <div className="space-y-2">
                  {playerView.insertSets.map((insertSet) => (
                    <InsertSetRow
                      key={insertSet.insertSetId}
                      insertSetName={insertSet.insertSetName}
                      isTeamCard={playerView.name === "Team Card"}
                      appearances={insertSet.appearances.map((a) => ({
                        cardNumber: a.cardNumber,
                        team: a.team,
                        isRookie: a.isRookie,
                        subsetTag: a.subsetTag,
                        coPlayers: a.coPlayers,
                      }))}
                      parallels={insertSet.parallels}
                    />
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <EmptyState playerCount={allPlayers.length} />
          )}
        </div>
      </div>
    </div>
  );
}

function StatChip({ value, label }: { value: number; label: string }) {
  return (
    <span>
      <span className="font-semibold text-zinc-300">{value.toLocaleString()}</span>{" "}
      {label}
    </span>
  );
}

function StatCard({
  label,
  value,
  highlight,
}: {
  label: string;
  value: number;
  highlight?: boolean;
}) {
  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900 px-4 py-4">
      <div
        className={`text-2xl font-bold tabular-nums ${
          highlight ? "text-amber-400" : "text-white"
        }`}
      >
        {value}
      </div>
      <div className="text-xs text-zinc-500 mt-0.5 font-medium">{label}</div>
    </div>
  );
}

function EmptyState({ playerCount }: { playerCount: number }) {
  return (
    <div className="flex flex-col items-center justify-center h-full text-center px-8">
      <div className="w-12 h-12 rounded-2xl border-2 border-zinc-700 bg-zinc-900 flex items-center justify-center mb-5">
        <svg
          className="w-5 h-5 text-zinc-500"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth={1.5}
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0zM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632z"
          />
        </svg>
      </div>
      <h2 className="text-lg font-semibold text-white mb-2">Select a Player</h2>
      <p className="text-sm text-zinc-500 max-w-xs leading-relaxed">
        Choose a player from the sidebar to see their full card breakdown across{" "}
        {playerCount} athletes in this set.
      </p>
    </div>
  );
}
