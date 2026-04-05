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
import { notFound } from "next/navigation";
import Link from "next/link";
import { V2StatCard } from "@/components/sets-v2/V2StatCard";
import { V2Tabs } from "@/components/sets-v2/V2Tabs";
import { V2Checklist } from "@/components/sets-v2/V2Checklist";
import { PackOddsCalculator, type PackOddsSlot, type BoxFormat } from "@/components/PackOddsCalculator";
import { BreakCalcWarning } from "@/components/BreakCalcWarning";
import type { InsertSetDetail, BoxConfigSingle, BoxConfigMulti } from "@/components/sets-v2/types";

export const dynamic = "force-dynamic";

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
  const { id, athleteId: athleteIdStr } = await params;
  const setId = parseInt(id, 10);
  const athleteId = parseInt(athleteIdStr, 10);
  if (isNaN(setId) || isNaN(athleteId)) notFound();

  const setRow = await db.query.sets.findFirst({
    where: (t, { eq }) => eq(t.id, setId),
  });
  if (!setRow) notFound();

  const playerData = await db.query.players.findFirst({
    where: (t, { eq }) => eq(t.id, athleteId),
  });
  if (!playerData || playerData.setId !== setId) notFound();

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

  const coPlayersByAppearance = new Map<number, { id: number; name: string }[]>();
  for (const row of coPlayerRows) {
    if (!coPlayersByAppearance.has(row.appearanceId)) {
      coPlayersByAppearance.set(row.appearanceId, []);
    }
    coPlayersByAppearance.get(row.appearanceId)!.push({ id: row.coPlayerId, name: row.coPlayerName });
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

    // Total distinct players per insert set
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

    function buildSlots(packOddsData: Record<string, number>): PackOddsSlot[] {
      return playerInsertSets.map((is) => {
        const isAuto = autoKeywords.some((kw) => is.insertSetName.toLowerCase().includes(kw));
        const prefix =
          is.insertSetName === "Base Set"
            ? "Base"
            : (ODDS_KEY_OVERRIDES[is.insertSetName] ?? is.insertSetName);
        const baseDenom =
          packOddsData[prefix] ??
          packOddsData[`${prefix} Geometric`] ??
          packOddsData[`${prefix} Refractor`] ??
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
              denom: packOddsData[`${prefix} ${p.name}`] ?? null,
            })),
        };
      });
    }

    if (isNestedOdds) {
      for (const [key, data] of Object.entries(rawOdds as Record<string, Record<string, number>>)) {
        const label = ODDS_TO_FORMAT_LABEL[key] ?? formatBoxLabel(key);
        packOddsSlotsByFormat[label] = buildSlots(data);
      }
    } else {
      const slots = buildSlots(rawOdds as Record<string, number>);
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
  }>(
    `SELECT s.id AS setId, s.name AS setName, s.season, s.tier, p.unique_cards AS uniqueCards
     FROM players p
     JOIN sets s ON s.id = p.set_id
     WHERE p.name = ? AND p.set_id != ?
     ORDER BY s.season DESC, s.name`,
    playerData.name,
    setId
  );

  return (
    <div className="max-w-4xl mx-auto px-6 py-8 space-y-8">
      {/* Breadcrumb */}
      <div className="flex items-center gap-1.5">
        <Link
          href={`/sets-v2/${setId}`}
          className="flex items-center gap-1 text-xs text-zinc-500 hover:text-zinc-300 transition-colors"
        >
          <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
          </svg>
          Set Overview
        </Link>
      </div>

      {/* Player header */}
      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight">{playerData.name}</h1>
          {teams.length > 0 && (
            <p className="text-zinc-400 mt-1.5 text-sm">{teams.join(" · ")}</p>
          )}
        </div>
        {hasRookie && (
          <span className="text-xs font-semibold text-amber-400 bg-amber-400/10 px-2 py-1 rounded mt-1 shrink-0">
            Rookie
          </span>
        )}
      </div>

      {/* Stat cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <V2StatCard label="Insert Sets" value={playerData.insertSetCount ?? 0} />
        <V2StatCard label="Unique Cards" value={playerData.uniqueCards ?? 0} />
        <V2StatCard label="Numbered Parallels" value={playerData.totalPrintRun ?? 0} />
        <V2StatCard
          label="1/1s"
          value={playerData.oneOfOnes ?? 0}
          subtext={(playerData.oneOfOnes ?? 0) > 0 ? "One-of-ones" : undefined}
        />
      </div>

      {/* Tabs */}
      <V2Tabs
        tabs={[
          {
            key: "cards",
            label: "Cards",
            content: (
              <V2Checklist setId={setId} insertSets={playerInsertSets} />
            ),
          },
          {
            key: "pack-odds",
            label: "Break Hit Calculator",
            content: (
              <div className="pt-2">
                {!hasBoxConfig || !hasPackOdds ? (
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
                ) : (
                  <p className="text-sm text-zinc-500 text-center py-8">
                    No pack odds data available for this player.
                  </p>
                )}
              </div>
            ),
          },
        ]}
        defaultTab="cards"
      />

      {/* Other sets */}
      {otherSetRows.length > 0 && (
        <div>
          <h2 className="text-xs font-semibold text-zinc-500 uppercase tracking-widest mb-3">
            Also appears in
          </h2>
          <div className="space-y-2">
            {otherSetRows.map((s) => (
              <Link
                key={s.setId}
                href={`/sets-v2/${s.setId}`}
                className="flex items-center justify-between px-4 py-3 rounded-xl border border-zinc-800 bg-zinc-900 hover:bg-zinc-800/50 transition-colors"
              >
                <div className="flex items-center gap-2.5 min-w-0">
                  <span className="text-sm font-medium text-zinc-300 truncate">{s.setName}</span>
                  <span className="text-xs text-zinc-600">{s.season}</span>
                  {s.tier !== "Standard" && (
                    <span className="text-[10px] font-medium text-slate-300 bg-slate-800 border border-slate-600/50 px-1.5 py-0.5 rounded">
                      {s.tier}
                    </span>
                  )}
                </div>
                <span className="text-xs text-zinc-500 tabular-nums shrink-0 ml-2">
                  {s.uniqueCards} card{s.uniqueCards !== 1 ? "s" : ""}
                </span>
              </Link>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
