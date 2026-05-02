import { db, rawQuery } from "@/lib/db";
import {
  sets,
  players,
  insertSets,
  parallels,
  playerAppearances,
  appearanceCoPlayers,
} from "@/lib/schema";
import { eq, inArray, asc, sql, and } from "drizzle-orm";
import { notFound, redirect } from "next/navigation";
import type { LeaderboardRow, InsertSetDetail, BoxConfigSingle, BoxConfigMulti, BoxFormatSummary } from "@/components/sets/types";
import type { PackOddsSlot, BoxFormat } from "@/components/PackOddsCalculator";
import { AthleteDetailClient } from "@/components/sets/AthleteDetailClient";


export const revalidate = 3600;

const ODDS_KEY_OVERRIDES: Record<string, string> = {
  "Base Chrome": "Base Chrome Variations",
  "Base Chrome Autographs": "Base Chrome Autograph Variations",
  "Clubhouse Collection Autographed Relics": "Clubhouse Collection Autograph Relics",
  "Clubhouse Collection Dual Autographed Relics": "Clubhouse Collection Dual Autograph Relics",
  "Flashbacks Autographed Relics": "Flashback Autographed Relics",
  "Best Of 2025 Autographs": "Best of 2025 Autographs",
  "Best Tek": "Best-Tek",
  "Best Tek Autographs": "Best-Tek Autographs",
  "Best Mix Autographs": "Best Mix Autograph Diecuts",
  "Prospect Patch Autographs": "Prospect Patch Autograph",
  "Strokes Of Gold": "Strokes of Gold",
  "8-Bit Ballers": "8 Bit Ballers",
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
  "Finest Partnerships": "Finest Partnerships Dual Autographs",
  "Finest Autographs": "Autographs",
  "Finest Rookie Autographs": "Rookie Autographs",
  "Cosmic Chrome Autographs": "Cosmic Chrome Autograph Variation",
  "Cosmic Chrome Autographs II": "Cosmic Chrome Autograph Variation II",
  "Electro Static Signatures": "Electro-Static Signatures",
  "Starfractor": "StarFractor",
  "Re Entry": "Re-Entry",
};

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
  fdi: "First Day Issue",
  // Retail exclusive variants (SE/EA/CEE) map to their base box type
  value_se: "Value",
  value_ea: "Value",
  value_cee: "Value",
  mega_se: "Mega",
  mega_ea: "Mega",
  mega_cee: "Mega",
  hanger_se: "Hanger",
  hanger_ea: "Hanger",
  hanger_cee: "Hanger",
};

function formatBoxLabel(key: string): string {
  return BOX_LABEL_MAP[key] ?? key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function isMultiConfig(cfg: BoxConfigSingle | BoxConfigMulti): cfg is BoxConfigMulti {
  const first = Object.values(cfg)[0];
  return first !== null && typeof first === "object";
}

export default async function V2AthletePage({
  params,
}: {
  params: Promise<{ id: string; athleteId: string }>;
}) {
  const { id: rawSetParam, athleteId: rawAthleteParam } = await params;
  const setIsNumeric = /^\d+$/.test(rawSetParam);
  const athleteIsNumeric = /^\d+$/.test(rawAthleteParam);

  // Resolve set
  let setRow;
  if (setIsNumeric) {
    setRow = await db.query.sets.findFirst({
      where: (t, { eq }) => eq(t.id, parseInt(rawSetParam, 10)),
    });
  } else {
    try {
      const slugRow = await rawQuery.get<{ id: number }>(
        "SELECT id FROM sets WHERE slug = ?", rawSetParam
      );
      if (slugRow) {
        setRow = await db.query.sets.findFirst({
          where: (t, { eq }) => eq(t.id, slugRow.id),
        });
      }
    } catch { /* slug column may not exist yet */ }
  }
  if (!setRow) notFound();
  const setId = setRow.id;

  // Resolve athlete
  let playerData;
  if (athleteIsNumeric) {
    playerData = await db.query.players.findFirst({
      where: (t, { eq }) => eq(t.id, parseInt(rawAthleteParam, 10)),
    });
  } else {
    try {
      const slugRow = await rawQuery.get<{ id: number }>(
        "SELECT id FROM players WHERE slug = ? AND set_id = ?", rawAthleteParam, setId
      );
      if (slugRow) {
        playerData = await db.query.players.findFirst({
          where: (t, { eq }) => eq(t.id, slugRow.id),
        });
      }
    } catch { /* slug column may not exist yet */ }
  }
  if (!playerData || playerData.setId !== setId) notFound();

  // Redirect numeric URLs to slug URLs
  if (setIsNumeric || athleteIsNumeric) {
    let setSlug: string | null = null;
    let athleteSlug: string | null = null;
    try {
      const setSlugRow = await rawQuery.get<{ slug: string | null }>(
        "SELECT slug FROM sets WHERE id = ?", setId
      );
      const athleteSlugRow = await rawQuery.get<{ slug: string | null }>(
        "SELECT slug FROM players WHERE id = ?", playerData.id
      );
      setSlug = setSlugRow?.slug ?? null;
      athleteSlug = athleteSlugRow?.slug ?? null;
    } catch { /* slug column may not exist yet */ }
    if (setSlug && athleteSlug) {
      redirect(`/sets/${setSlug}/athlete/${athleteSlug}`);
    }
  }

  const athleteId = playerData.id;

  // Fetch image_url (not in Drizzle schema)
  let playerImageUrl: string | null = null;
  try {
    const imgRow = await rawQuery.get<{ image_url: string | null }>(
      "SELECT image_url FROM players WHERE id = ?", athleteId
    );
    playerImageUrl = imgRow?.image_url ?? null;
  } catch { /* column may not exist */ }

  // Insert set IDs for this set
  const insertSetIdRows = await db
    .select({ id: insertSets.id })
    .from(insertSets)
    .where(eq(insertSets.setId, setId));
  const insertSetIds = insertSetIdRows.map((r) => r.id);

  // Player appearances
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
    .where(eq(playerAppearances.playerId, athleteId))
    .orderBy(asc(playerAppearances.cardNumber));

  // Co-players
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

  // Look up slugs for co-players
  const coPlayerIds = [...new Set(coPlayerRows.map((r) => r.coPlayerId))];
  const coPlayerSlugMap = new Map<number, string>();
  if (coPlayerIds.length > 0) {
    try {
      const placeholders = coPlayerIds.map(() => "?").join(",");
      const slugRows = await rawQuery.all<{ id: number; slug: string | null }>(
        `SELECT id, slug FROM players WHERE id IN (${placeholders})`,
        ...coPlayerIds
      );
      for (const row of slugRows) {
        if (row.slug) coPlayerSlugMap.set(row.id, row.slug);
      }
    } catch { /* slug column may not exist yet */ }
  }

  const coPlayersByAppearance = new Map<number, { id: number; name: string; slug: string | null }[]>();
  for (const row of coPlayerRows) {
    if (!coPlayersByAppearance.has(row.appearanceId)) {
      coPlayersByAppearance.set(row.appearanceId, []);
    }
    coPlayersByAppearance.get(row.appearanceId)!.push({ id: row.coPlayerId, name: row.coPlayerName, slug: coPlayerSlugMap.get(row.coPlayerId) ?? null });
  }

  // Parallels per insert set
  const playerInsertSetIds = [...new Set(appearanceRows.map((a) => a.insertSetId))];
  const parallelsByIS = new Map<number, { id: number; name: string; printRun: number | null }[]>();
  if (playerInsertSetIds.length > 0) {
    const parallelRows = await db
      .select()
      .from(parallels)
      .where(inArray(parallels.insertSetId, playerInsertSetIds));
    for (const row of parallelRows) {
      if (!parallelsByIS.has(row.insertSetId)) {
        parallelsByIS.set(row.insertSetId, []);
      }
      parallelsByIS.get(row.insertSetId)!.push(row);
    }
  }

  const teams = [...new Set(appearanceRows.map((a) => a.team).filter(Boolean))] as string[];
  const hasRookie = appearanceRows.some((a) => a.isRookie);

  // Build insert set detail
  const insertSetMap = new Map<number, InsertSetDetail>();
  for (const appearance of appearanceRows) {
    const key = appearance.insertSetId;
    if (!insertSetMap.has(key)) {
      insertSetMap.set(key, {
        insertSetId: key,
        insertSetName: appearance.insertSetName,
        appearances: [],
        parallels: parallelsByIS.get(key) ?? [],
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
  const playerInsertSets = Array.from(insertSetMap.values());

  // ── Pack Odds ───────────────────────────────────────────────────────────────
  const hasBoxConfig = !!setRow.boxConfig;
  const hasPackOdds = !!setRow.packOdds;
  const autoKeywords = ["auto", "signature", "graph", "relic"];

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

  const packOddsSlotsByFormat: Record<string, PackOddsSlot[]> = {};
  if (hasPackOdds) {
    const rawOdds = JSON.parse(setRow.packOdds!);
    const firstVal = Object.values(rawOdds)[0];
    const isNestedOdds = firstVal !== null && typeof firstVal === "object";

    // Normalize odds values using shared parser
    const { normalizeOddsObj } = await import("@/lib/parseOdds");

    const totalAppsByIS = new Map<number, number>();
    if (playerInsertSetIds.length > 0) {
      const rows = await rawQuery.all<{ insert_set_id: number; total_apps: number }>(
        `SELECT insert_set_id, COUNT(DISTINCT card_number) AS total_apps
         FROM player_appearances
         WHERE insert_set_id IN (${playerInsertSetIds.map(() => "?").join(",")})
         GROUP BY insert_set_id`,
        ...playerInsertSetIds
      );
      for (const row of rows) totalAppsByIS.set(row.insert_set_id, row.total_apps);
    }

    const ODDS_TO_FORMAT_LABEL: Record<string, string> = {
      breaker: "Breaker's Delight",
    };

    function resolvePrefix(name: string, packOddsData: Record<string, number>): string {
      if (name === "Base Set") return "Base";
      const overridden = ODDS_KEY_OVERRIDES[name];
      if (overridden) return overridden;
      // Direct match — use as-is
      if (name in packOddsData) return name;
      // Case-insensitive fallback (e.g. "Ace Of Trades" vs "Ace of Trades")
      const ciMatch = Object.keys(packOddsData).find(
        (k) => k.toLowerCase() === name.toLowerCase()
      );
      if (ciMatch) return ciMatch;
      // Base subset variants (e.g. "Base - Comic Accurate", "Base Cards I",
      // "Base Tier III") should map to the common base odds prefix.
      // Try "Base Cards" first (Deadpool style), then "Base" (WWE Chrome style / F1 style).
      if (name.startsWith("Base")) {
        if ("Base Cards" in packOddsData) return "Base Cards";
        const hasBasePrefix = Object.keys(packOddsData).some((k) => k.startsWith("Base "));
        if (hasBasePrefix) return "Base";
      }
      return name;
    }

    function buildSlots(packOddsData: Record<string, number>): PackOddsSlot[] {
      return playerInsertSets.map((is) => {
        const isAuto = autoKeywords.some((kw) => is.insertSetName.toLowerCase().includes(kw));
        const prefix = resolvePrefix(is.insertSetName, packOddsData);
        const baseDenom =
          packOddsData[prefix] ??
          packOddsData[`${prefix} Geometric`] ??
          packOddsData[`${prefix} Refractor`] ??
          packOddsData[`${prefix} Refractor Parallel`] ??
          null;
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
              denom:
                packOddsData[`${prefix} ${p.name}`] ??
                packOddsData[`${prefix} ${p.name} Parallel`] ??
                null,
            })),
        };
      });
    }

    if (isNestedOdds) {
      for (const [key, data] of Object.entries(rawOdds as Record<string, Record<string, unknown>>)) {
        const label = ODDS_TO_FORMAT_LABEL[key] ?? formatBoxLabel(key);
        // First pack_odds key for a given label wins (e.g. value_se before value_ea)
        if (!(label in packOddsSlotsByFormat)) {
          packOddsSlotsByFormat[label] = buildSlots(normalizeOddsObj(data));
        }
      }
    } else {
      const slots = buildSlots(normalizeOddsObj(rawOdds as Record<string, unknown>));
      for (const fmt of boxFormats) {
        packOddsSlotsByFormat[fmt.label] = slots;
      }
      if (boxFormats.length === 0) packOddsSlotsByFormat["default"] = slots;
    }
  }

  // Total auto cards for guaranteed-slot model
  const autoFilter = `(LOWER(i.name) LIKE '%auto%' OR LOWER(i.name) LIKE '%signature%' OR LOWER(i.name) LIKE '%graph%' OR LOWER(i.name) LIKE '%relic%')`;
  const totalAutoCards =
    (await rawQuery.get<{ n: number }>(
      `SELECT COUNT(*) AS n
       FROM player_appearances pa
       JOIN insert_sets i ON pa.insert_set_id = i.id
       WHERE i.set_id = ? AND ${autoFilter}`,
      setRow.id
    ))?.n ?? 0;

  const playerAutoCards = playerInsertSets
    .filter((is) => autoKeywords.some((kw) => is.insertSetName.toLowerCase().includes(kw)))
    .reduce((sum, is) => sum + is.appearances.length, 0);

  // ── Other sets this player appears in ───────────────────────────────────────
  const otherSetRows = await rawQuery.all<{
    setId: number;
    setName: string;
    season: string;
    tier: string;
    uniqueCards: number;
    setSlug: string | null;
  }>(
    `SELECT s.id AS setId, s.name AS setName, s.season, s.tier, s.slug AS setSlug, p.unique_cards AS uniqueCards
     FROM players p
     JOIN sets s ON s.id = p.set_id
     WHERE p.name = ? AND p.set_id != ?
     ORDER BY s.season DESC, s.name`,
    playerData.name,
    setId
  );

  // ── Leaderboard ─────────────────────────────────────────────────────────────
  const leaderboardRaw = await rawQuery.all<{
    id: number;
    name: string;
    slug: string | null;
    totalCards: number;
    isRookie: number;
    team: string | null;
    autographs: number;
    inserts: number;
    numberedParallels: number;
    nbaPlayerId: number | null;
    ufcImageUrl: string | null;
    mlbPlayerId: number | null;
    imageUrl: string | null;
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
       p.slug,
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
       COALESCE(n.cnt, 0) AS numberedParallels,
       p.nba_player_id AS nbaPlayerId,
       p.ufc_image_url AS ufcImageUrl,
       p.mlb_player_id AS mlbPlayerId,
       p.image_url AS imageUrl
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
    slug: r.slug,
    team: r.team,
    isRookie: r.isRookie === 1,
    totalCards: r.totalCards,
    autographs: r.autographs,
    inserts: r.inserts,
    numberedParallels: r.numberedParallels,
    nbaPlayerId: r.nbaPlayerId,
    ufcImageUrl: r.ufcImageUrl,
    mlbPlayerId: r.mlbPlayerId,
    imageUrl: r.imageUrl,
  }));

  const hasTeamData = leaderboardEntries.some((e) => e.team != null && e.team !== "");

  // ── Right sidebar stats ───────────────────────────────────────────────────
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

  const statItems = [
    { label: "Card Types", value: playerData.insertSetCount ?? 0 },
    { label: "Total Cards", value: playerData.uniqueCards ?? 0 },
    { label: "Numbered", value: playerData.totalPrintRun ?? 0 },
    { label: "1/1s", value: playerData.oneOfOnes ?? 0 },
  ];

  // Build other sets data for the client
  const otherSetsForClient = otherSetRows.map((s) => ({
    id: s.setId,
    name: s.setName,
    slug: s.setSlug,
    sport: setRow.sport,
    totalCards: s.uniqueCards,
    autographs: 0,
    parallels: 0,
  }));

  // Serialize insert sets to plain objects for client
  const plainInsertSets = playerInsertSets.map((is) => ({
    insertSetId: is.insertSetId,
    insertSetName: is.insertSetName,
    appearances: is.appearances.map((a) => ({
      cardNumber: a.cardNumber,
      team: a.team,
      isRookie: a.isRookie,
      subsetTag: a.subsetTag,
      coPlayers: a.coPlayers.map((c) => ({ id: c.id, name: c.name, slug: c.slug })),
    })),
    parallels: is.parallels.map((p) => ({ id: p.id, name: p.name, printRun: p.printRun })),
  }));

  return (
    <AthleteDetailClient
      athleteName={playerData.name}
      athleteId={athleteId}
      athleteSlug={rawAthleteParam}
      teams={teams}
      hasRookie={hasRookie}
      nbaPlayerId={playerData.nbaPlayerId}
      ufcImageUrl={playerData.ufcImageUrl}
      mlbPlayerId={playerData.mlbPlayerId}
      imageUrl={playerImageUrl}
      setName={setRow.name}
      setSlug={rawSetParam}
      setId={setId}
      sport={setRow.sport}
      league={setRow.league ?? null}
      cardTypes={playerData.insertSetCount ?? 0}
      totalCards={playerData.uniqueCards ?? 0}
      numberedParallels={playerData.totalPrintRun ?? 0}
      oneOfOnes={playerData.oneOfOnes ?? 0}
      insertSets={plainInsertSets}
      otherSets={otherSetsForClient}
      packOddsJson={setRow.packOdds ?? null}
      boxConfigJson={setRow.boxConfig ?? null}
      packOddsSlotsByFormat={packOddsSlotsByFormat}
      boxFormats={boxFormats}
      totalAutoCards={totalAutoCards}
      playerAutoCards={playerAutoCards}
      hasBreakCalc={hasBoxConfig && hasPackOdds && Object.keys(packOddsSlotsByFormat).length > 0}
      entries={leaderboardEntries}
      hasTeamData={hasTeamData}
    />
  );
}
