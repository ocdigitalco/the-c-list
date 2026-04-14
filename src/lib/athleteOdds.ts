/**
 * Universal athlete odds engine.
 *
 * Computes hit probabilities for any athlete in any set, for any box type.
 * Used by the Break Hit Calculator on athlete pages.
 *
 * All DB queries happen server-side; the exported functions are async and
 * intended for use in Next.js server components or API routes.
 */

import { rawQuery } from "./db";

// ─── Types ───────────────────────────────────────────────────────────────────

export interface OddsResult {
  probability: number;
  percentagePerBox: number;
  oneInXBoxes: number;
  athletePoolShare: number;
  guaranteedPerBox: number;
  cardCount: number;
  /** True when the pool has usable data */
  hasData: boolean;
  /** True when using guaranteed-slot model instead of pack-odds */
  usesGuarantee: boolean;
}

export interface AthleteOdds {
  athleteId: number;
  athleteName: string;
  anyCard: OddsResult;
  numbered: OddsResult;
  auto: OddsResult;
}

export interface BoxFormatConfig {
  label: string;
  packsPerBox: number;
  boxesPerCase: number;
  guaranteedAutos: number;
}

interface PoolEntry {
  insertSetId: number;
  insertSetName: string;
  parallelName: string | null;
  oddsKey: string;
  weight: number; // 1 / odds_denominator
  isAuto: boolean;
  isNumbered: boolean;
  totalAppsInIS: number;
}

interface AthletePoolEntry extends PoolEntry {
  playerApps: number;
}

// ─── Odds normalization ──────────────────────────────────────────────────────

import { normalizeOddsObj } from "./parseOdds";
export { normalizeOddsObj };

// ─── Insert set name → odds key prefix resolution ───────────────────────────

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

const AUTO_KEYWORDS = ["auto", "signature", "graph", "relic"];

function isAutoInsertSet(name: string): boolean {
  const lower = name.toLowerCase();
  return AUTO_KEYWORDS.some((kw) => lower.includes(kw));
}

function resolvePrefix(
  name: string,
  packOddsData: Record<string, number>
): string {
  if (name === "Base Set") return "Base";
  const overridden = ODDS_KEY_OVERRIDES[name];
  if (overridden) return overridden;
  if (name in packOddsData) return name;
  // Case-insensitive fallback
  const ciMatch = Object.keys(packOddsData).find(
    (k) => k.toLowerCase() === name.toLowerCase()
  );
  if (ciMatch) return ciMatch;
  // Base subset variants
  if (name.startsWith("Base")) {
    if ("Base Cards" in packOddsData) return "Base Cards";
    const hasBasePrefix = Object.keys(packOddsData).some((k) =>
      k.startsWith("Base ")
    );
    if (hasBasePrefix) return "Base";
  }
  return name;
}

function lookupDenom(
  packOddsData: Record<string, number>,
  prefix: string,
  parallelName?: string
): number | null {
  if (parallelName) {
    return (
      packOddsData[`${prefix} ${parallelName}`] ??
      packOddsData[`${prefix} ${parallelName} Parallel`] ??
      null
    );
  }
  return (
    packOddsData[prefix] ??
    packOddsData[`${prefix} Geometric`] ??
    packOddsData[`${prefix} Refractor`] ??
    packOddsData[`${prefix} Refractor Parallel`] ??
    null
  );
}

// ─── Pool building ───────────────────────────────────────────────────────────

interface InsertSetRow {
  id: number;
  name: string;
}

interface ParallelRow {
  insert_set_id: number;
  name: string;
  print_run: number | null;
}

interface AppCountRow {
  insert_set_id: number;
  total_apps: number;
}

interface PlayerAppRow {
  insert_set_id: number;
  player_apps: number;
}

/**
 * Build the full odds pool for a set + box type.
 * Returns one entry per (insert_set, parallel) pair that has a matching odds key.
 */
export async function buildOddsPool(
  setId: number,
  packOddsData: Record<string, number>
): Promise<PoolEntry[]> {
  // Get all insert sets for this set
  const insertSetRows = await rawQuery.all<InsertSetRow>(
    "SELECT id, name FROM insert_sets WHERE set_id = ?",
    setId
  );

  if (insertSetRows.length === 0) return [];

  const isIds = insertSetRows.map((r) => r.id);
  const placeholders = isIds.map(() => "?").join(",");

  // Get all parallels for these insert sets
  const parallelRows = await rawQuery.all<ParallelRow>(
    `SELECT insert_set_id, name, print_run FROM parallels WHERE insert_set_id IN (${placeholders})`,
    ...isIds
  );

  // Get total appearances per insert set
  const appCountRows = await rawQuery.all<AppCountRow>(
    `SELECT insert_set_id, COUNT(DISTINCT card_number) AS total_apps
     FROM player_appearances
     WHERE insert_set_id IN (${placeholders})
     GROUP BY insert_set_id`,
    ...isIds
  );
  const totalAppsMap = new Map(appCountRows.map((r) => [r.insert_set_id, r.total_apps]));

  // Group parallels by insert set
  const parallelsByIS = new Map<number, ParallelRow[]>();
  for (const p of parallelRows) {
    if (!parallelsByIS.has(p.insert_set_id)) parallelsByIS.set(p.insert_set_id, []);
    parallelsByIS.get(p.insert_set_id)!.push(p);
  }

  const pool: PoolEntry[] = [];

  for (const is of insertSetRows) {
    const prefix = resolvePrefix(is.name, packOddsData);
    const isAuto = isAutoInsertSet(is.name);
    const totalApps = totalAppsMap.get(is.id) ?? 0;
    if (totalApps === 0) continue;

    // Base entry for this insert set
    const baseDenom = lookupDenom(packOddsData, prefix);
    if (baseDenom !== null && baseDenom > 0) {
      pool.push({
        insertSetId: is.id,
        insertSetName: is.name,
        parallelName: null,
        oddsKey: prefix,
        weight: 1 / baseDenom,
        isAuto,
        isNumbered: isAuto, // auto base cards count as numbered
        totalAppsInIS: totalApps,
      });
    }

    // Parallel entries
    const pars = parallelsByIS.get(is.id) ?? [];
    for (const par of pars) {
      const denom = lookupDenom(packOddsData, prefix, par.name);
      if (denom === null || denom <= 0) continue;
      pool.push({
        insertSetId: is.id,
        insertSetName: is.name,
        parallelName: par.name,
        oddsKey: `${prefix} ${par.name}`,
        weight: 1 / denom,
        isAuto,
        isNumbered: par.print_run !== null,
        totalAppsInIS: totalApps,
      });
    }
  }

  return pool;
}

// ─── Athlete-specific pool ───────────────────────────────────────────────────

async function getAthleteApps(
  athleteId: number,
  insertSetIds: number[]
): Promise<Map<number, number>> {
  if (insertSetIds.length === 0) return new Map();
  const placeholders = insertSetIds.map(() => "?").join(",");
  const rows = await rawQuery.all<PlayerAppRow>(
    `SELECT insert_set_id, COUNT(*) AS player_apps
     FROM player_appearances
     WHERE player_id = ? AND insert_set_id IN (${placeholders})
     GROUP BY insert_set_id`,
    athleteId,
    ...insertSetIds
  );
  return new Map(rows.map((r) => [r.insert_set_id, r.player_apps]));
}

// ─── Probability math ────────────────────────────────────────────────────────

function calcPoolProbability(
  athleteWeight: number,
  totalWeight: number,
  packsPerBox: number,
  boxes: number,
  guaranteePerBox: number
): number {
  if (totalWeight <= 0 || athleteWeight <= 0) return 0;
  const athleteShare = athleteWeight / totalWeight;

  if (guaranteePerBox >= 1) {
    // Guaranteed-slot model
    const slots = guaranteePerBox * boxes;
    return 1 - Math.pow(1 - athleteShare, slots);
  }
  // Pack-odds model: compound per-pack probability across all packs
  const pPerPack = athleteWeight;
  const totalPacks = packsPerBox * boxes;
  return 1 - Math.pow(1 - Math.min(pPerPack, 1), totalPacks);
}

function buildResult(
  probability: number,
  athletePoolShare: number,
  guaranteedPerBox: number,
  cardCount: number,
  hasData: boolean,
  usesGuarantee: boolean
): OddsResult {
  return {
    probability,
    percentagePerBox: Math.round(probability * 10000) / 100,
    oneInXBoxes: probability > 0 ? Math.round(1 / probability) : 0,
    athletePoolShare,
    guaranteedPerBox,
    cardCount,
    hasData,
    usesGuarantee,
  };
}

// ─── Main exported functions ─────────────────────────────────────────────────

/**
 * Parse pack_odds JSON for a specific box type.
 * Returns null if the box type doesn't exist in the odds.
 */
export function getOddsForBoxType(
  packOddsJson: string | null,
  boxType: string
): Record<string, number> | null {
  if (!packOddsJson) return null;
  const raw = JSON.parse(packOddsJson);
  const firstVal = Object.values(raw)[0];
  const isNested = firstVal !== null && typeof firstVal === "object";

  if (isNested) {
    const data = raw[boxType];
    if (!data || typeof data !== "object") return null;
    return normalizeOddsObj(data as Record<string, unknown>);
  }
  // Flat odds — apply to all box types
  return normalizeOddsObj(raw as Record<string, unknown>);
}

/**
 * Parse box_config JSON and extract config for a specific box type.
 */
export function getBoxConfig(
  boxConfigJson: string | null,
  boxType: string
): BoxFormatConfig | null {
  if (!boxConfigJson) return null;
  const raw = JSON.parse(boxConfigJson);
  const firstVal = Object.values(raw)[0];
  const isMulti = firstVal !== null && typeof firstVal === "object";

  const fmt = isMulti ? raw[boxType] : raw;
  if (!fmt) return null;

  return {
    label: boxType,
    packsPerBox: fmt.packs_per_box ?? 1,
    boxesPerCase: fmt.boxes_per_case ?? 8,
    guaranteedAutos:
      fmt.autos_per_box ??
      fmt.autos_or_memorabilia_per_box ??
      fmt.autos_or_relics_per_box ??
      fmt.autos_or_auto_relics_per_box ??
      0,
  };
}

/**
 * Get all available box type keys from pack_odds or box_config.
 */
export function getBoxTypeKeys(
  packOddsJson: string | null,
  boxConfigJson: string | null
): string[] {
  const keys = new Set<string>();

  if (packOddsJson) {
    const raw = JSON.parse(packOddsJson);
    const firstVal = Object.values(raw)[0];
    if (firstVal !== null && typeof firstVal === "object") {
      for (const k of Object.keys(raw)) keys.add(k);
    }
  }

  if (boxConfigJson) {
    const raw = JSON.parse(boxConfigJson);
    const firstVal = Object.values(raw)[0];
    if (firstVal !== null && typeof firstVal === "object") {
      for (const k of Object.keys(raw)) keys.add(k);
    }
  }

  return Array.from(keys);
}

/**
 * Compute odds for a single athlete in a set for a given box type.
 */
export async function getAthleteOdds(
  setId: number,
  athleteId: number,
  athleteName: string,
  packOddsData: Record<string, number>,
  boxConfig: BoxFormatConfig,
  boxes: number = 1
): Promise<AthleteOdds> {
  const pool = await buildOddsPool(setId, packOddsData);

  // Get this athlete's appearances per insert set
  const uniqueISIds = [...new Set(pool.map((e) => e.insertSetId))];
  const playerAppsMap = await getAthleteApps(athleteId, uniqueISIds);

  const { packsPerBox, guaranteedAutos } = boxConfig;

  // Calculate per-pool weights
  let anyAthleteWeight = 0;
  let anyTotalWeight = 0;
  let anyCardCount = 0;
  let numberedAthleteWeight = 0;
  let numberedTotalWeight = 0;
  let numberedCardCount = 0;
  let autoAthleteWeight = 0;
  let autoTotalWeight = 0;
  let autoCardCount = 0;

  for (const entry of pool) {
    const playerApps = playerAppsMap.get(entry.insertSetId) ?? 0;
    const playerShare = playerApps / entry.totalAppsInIS;
    const athleteW = entry.weight * playerShare;

    // Any card pool
    anyTotalWeight += entry.weight;
    anyAthleteWeight += athleteW;
    if (playerApps > 0) anyCardCount++;

    // Numbered pool
    if (entry.isNumbered) {
      numberedTotalWeight += entry.weight;
      numberedAthleteWeight += athleteW;
      if (playerApps > 0) numberedCardCount++;
    }

    // Auto pool
    if (entry.isAuto) {
      autoTotalWeight += entry.weight;
      autoAthleteWeight += athleteW;
      if (playerApps > 0) autoCardCount++;
    }
  }

  // Calculate probabilities
  const usesGuaranteeAuto = guaranteedAutos >= 1;
  const autoShare = autoTotalWeight > 0 ? autoAthleteWeight / autoTotalWeight : 0;

  const pAuto = usesGuaranteeAuto
    ? calcPoolProbability(autoAthleteWeight, autoTotalWeight, packsPerBox, boxes, guaranteedAutos)
    : calcPoolProbability(autoAthleteWeight, autoTotalWeight, packsPerBox, boxes, 0);

  const pNumberedFromPacks = calcPoolProbability(
    numberedAthleteWeight, numberedTotalWeight, packsPerBox, boxes, 0
  );

  const pAnyFromPacks = calcPoolProbability(
    anyAthleteWeight, anyTotalWeight, packsPerBox, boxes, 0
  );

  // Fold guaranteed auto probability into numbered and any
  let pNumbered: number;
  let pAny: number;
  if (usesGuaranteeAuto) {
    pNumbered = 1 - (1 - pNumberedFromPacks) * (1 - pAuto);
    pAny = 1 - (1 - pAnyFromPacks) * (1 - pAuto);
  } else {
    pNumbered = pNumberedFromPacks;
    pAny = pAnyFromPacks;
  }

  return {
    athleteId,
    athleteName,
    anyCard: buildResult(
      pAny,
      anyTotalWeight > 0 ? anyAthleteWeight / anyTotalWeight : 0,
      0,
      anyCardCount,
      anyTotalWeight > 0,
      false
    ),
    numbered: buildResult(
      pNumbered,
      numberedTotalWeight > 0 ? numberedAthleteWeight / numberedTotalWeight : 0,
      0,
      numberedCardCount,
      numberedTotalWeight > 0,
      false
    ),
    auto: buildResult(
      pAuto,
      autoShare,
      guaranteedAutos,
      autoCardCount,
      autoTotalWeight > 0,
      usesGuaranteeAuto
    ),
  };
}
