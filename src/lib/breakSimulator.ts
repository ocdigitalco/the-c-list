/**
 * Box Break Simulator engine.
 *
 * Runs Monte Carlo simulations of box breaks using the weighted card pool
 * from athleteOdds.ts. All DB queries happen server-side; the simulation
 * math runs client-side after receiving the pool data.
 */

import { buildOddsPool, getOddsForBoxType, getBoxConfig } from "./athleteOdds";
import type { BoxFormatConfig } from "./athleteOdds";
import { rawQuery } from "./db";

// ─── Types ───────────────────────────────────────────────────────────────────

export interface SimPoolCard {
  insertSetId: number;
  insertSetName: string;
  parallelName: string | null;
  oddsKey: string;
  weight: number;
  isAuto: boolean;
  isNumbered: boolean;
  totalAppsInIS: number;
  /** Athletes in this insert set with their appearance count */
  athletes: { id: number; name: string; apps: number }[];
}

export interface SimConfig {
  setId: number;
  setName: string;
  boxType: string;
  boxConfig: BoxFormatConfig;
  pool: SimPoolCard[];
  cardsPerPack: number;
}

export interface PackPull {
  packNumber: number;
  athleteName: string;
  insertSetName: string;
  parallelName: string | null;
  printRun: number | null;
  isAuto: boolean;
  isNumbered: boolean;
}

export interface BreakTrial {
  pulls: PackPull[];
  autoCount: number;
  numberedCount: number;
  totalCards: number;
}

export interface SimulationResult {
  config: { setName: string; boxType: string; boxCount: number; trials: number };
  medianTrial: BreakTrial;
  bestTrial: BreakTrial;
  worstTrial: BreakTrial;
  singleRandomTrial: BreakTrial;
  distributions: {
    autos: Record<number, number>;
    numbered: Record<number, number>;
  };
  topAutoAthletes: {
    athleteName: string;
    autoAppearances: number;
    autoPercentage: number;
  }[];
}

// ─── Server-side: build the simulation pool ──────────────────────────────────

interface AthleteRow {
  insert_set_id: number;
  player_id: number;
  player_name: string;
  apps: number;
}

/**
 * Build the full simulation pool for a set + box type.
 * Returns pool cards with athlete breakdowns — ready to serialize to client.
 */
export async function buildSimPool(
  setId: number,
  packOddsJson: string | null,
  boxConfigJson: string | null,
  boxType: string
): Promise<SimConfig | null> {
  const oddsData = getOddsForBoxType(packOddsJson, boxType);
  const boxConfig = getBoxConfig(boxConfigJson, boxType);
  if (!oddsData || !boxConfig) return null;

  const pool = await buildOddsPool(setId, oddsData);
  if (pool.length === 0) return null;

  // Get set name
  const setRow = await rawQuery.get<{ name: string; box_config: string }>(
    "SELECT name, box_config FROM sets WHERE id = ?",
    setId
  );
  if (!setRow) return null;

  // Get cards_per_pack from box_config
  const bcRaw = JSON.parse(boxConfigJson!);
  const firstVal = Object.values(bcRaw)[0];
  const isMulti = firstVal !== null && typeof firstVal === "object";
  const fmt = isMulti ? bcRaw[boxType] : bcRaw;
  const cardsPerPack = fmt?.cards_per_pack ?? 4;

  // Get athletes per insert set
  const isIds = [...new Set(pool.map((p) => p.insertSetId))];
  const placeholders = isIds.map(() => "?").join(",");
  const athleteRows = await rawQuery.all<AthleteRow>(
    `SELECT pa.insert_set_id, pa.player_id, p.name AS player_name, COUNT(*) AS apps
     FROM player_appearances pa
     JOIN players p ON p.id = pa.player_id
     WHERE pa.insert_set_id IN (${placeholders})
     GROUP BY pa.insert_set_id, pa.player_id`,
    ...isIds
  );

  // Group athletes by insert set
  const athletesByIS = new Map<number, { id: number; name: string; apps: number }[]>();
  for (const r of athleteRows) {
    if (!athletesByIS.has(r.insert_set_id)) athletesByIS.set(r.insert_set_id, []);
    athletesByIS.get(r.insert_set_id)!.push({
      id: r.player_id,
      name: r.player_name,
      apps: r.apps,
    });
  }

  const simPool: SimPoolCard[] = pool.map((entry) => ({
    ...entry,
    athletes: athletesByIS.get(entry.insertSetId) ?? [],
  }));

  return {
    setId,
    setName: setRow.name,
    boxType,
    boxConfig,
    pool: simPool,
    cardsPerPack,
  };
}

// ─── Client-side: run the simulation ─────────────────────────────────────────
// These functions are pure math — no DB access. They run in the browser.

function weightedSampleAthlete(
  card: SimPoolCard
): { name: string; id: number } {
  const athletes = card.athletes;
  if (athletes.length === 0) return { name: "Unknown", id: 0 };
  const totalApps = athletes.reduce((s, a) => s + a.apps, 0);
  let r = Math.random() * totalApps;
  for (const a of athletes) {
    r -= a.apps;
    if (r <= 0) return { name: a.name, id: a.id };
  }
  return { name: athletes[athletes.length - 1].name, id: athletes[athletes.length - 1].id };
}

function weightedSampleCard(pool: SimPoolCard[]): SimPoolCard {
  const totalWeight = pool.reduce((s, c) => s + c.weight, 0);
  let r = Math.random() * totalWeight;
  for (const c of pool) {
    r -= c.weight;
    if (r <= 0) return c;
  }
  return pool[pool.length - 1];
}

function simulateOneTrial(
  config: SimConfig,
  boxCount: number
): BreakTrial {
  const { pool, boxConfig, cardsPerPack } = config;
  const { packsPerBox, guaranteedAutos } = boxConfig;

  const autoPool = pool.filter((c) => c.isAuto);
  const fullPool = pool;

  const pulls: PackPull[] = [];
  let autoCount = 0;
  let numberedCount = 0;

  for (let box = 0; box < boxCount; box++) {
    // Guaranteed auto slots distributed across packs
    let autosRemaining = guaranteedAutos;

    for (let pack = 0; pack < packsPerBox; pack++) {
      const packNum = box * packsPerBox + pack + 1;

      for (let card = 0; card < cardsPerPack; card++) {
        let sampled: SimPoolCard;

        // Use auto pool for guaranteed slots
        if (autosRemaining > 0 && autoPool.length > 0 && card === 0) {
          sampled = weightedSampleCard(autoPool);
          autosRemaining--;
        } else {
          // Regular card from full pool — weighted random
          // Each pack slot has a chance of being any card type based on odds
          sampled = weightedSampleCard(fullPool);
        }

        const athlete = weightedSampleAthlete(sampled);

        const pull: PackPull = {
          packNumber: packNum,
          athleteName: athlete.name,
          insertSetName: sampled.insertSetName,
          parallelName: sampled.parallelName,
          printRun: sampled.isNumbered && sampled.parallelName ? null : null,
          isAuto: sampled.isAuto,
          isNumbered: sampled.isNumbered,
        };

        pulls.push(pull);
        if (sampled.isAuto) autoCount++;
        if (sampled.isNumbered) numberedCount++;
      }
    }
  }

  return { pulls, autoCount, numberedCount, totalCards: pulls.length };
}

/**
 * Run the full Monte Carlo simulation. Pure function — no DB access.
 * Call from client-side with the SimConfig obtained from the API.
 */
export function runSimulation(
  config: SimConfig,
  boxCount: number = 1,
  trialCount: number = 10000
): SimulationResult {
  const trials: BreakTrial[] = [];

  for (let i = 0; i < trialCount; i++) {
    trials.push(simulateOneTrial(config, boxCount));
  }

  // Sort by autoCount for percentile selection
  const sorted = [...trials].sort((a, b) => a.autoCount - b.autoCount);
  const p10 = sorted[Math.floor(trialCount * 0.1)];
  const p50 = sorted[Math.floor(trialCount * 0.5)];
  const p90 = sorted[Math.floor(trialCount * 0.9)];
  const randomIdx = Math.floor(Math.random() * trialCount);

  // Distribution histograms
  const autoDist: Record<number, number> = {};
  const numberedDist: Record<number, number> = {};
  const autoAthleteCount = new Map<string, number>();
  const anyAthleteCount = new Map<string, number>();

  for (const trial of trials) {
    autoDist[trial.autoCount] = (autoDist[trial.autoCount] ?? 0) + 1;
    numberedDist[trial.numberedCount] = (numberedDist[trial.numberedCount] ?? 0) + 1;

    const seenAuto = new Set<string>();
    const seenAny = new Set<string>();
    for (const pull of trial.pulls) {
      if (pull.isAuto && !seenAuto.has(pull.athleteName)) {
        seenAuto.add(pull.athleteName);
        autoAthleteCount.set(pull.athleteName, (autoAthleteCount.get(pull.athleteName) ?? 0) + 1);
      }
      if (!seenAny.has(pull.athleteName)) {
        seenAny.add(pull.athleteName);
        anyAthleteCount.set(pull.athleteName, (anyAthleteCount.get(pull.athleteName) ?? 0) + 1);
      }
    }
  }

  // Normalize distributions
  for (const k in autoDist) autoDist[k] = autoDist[k] / trialCount;
  for (const k in numberedDist) numberedDist[k] = numberedDist[k] / trialCount;

  // Top auto athletes
  const topAutoAthletes = Array.from(autoAthleteCount.entries())
    .map(([name, count]) => ({
      athleteName: name,
      autoAppearances: count,
      autoPercentage: Math.round((count / trialCount) * 1000) / 10,
    }))
    .sort((a, b) => b.autoAppearances - a.autoAppearances)
    .slice(0, 10);

  return {
    config: {
      setName: config.setName,
      boxType: config.boxType,
      boxCount,
      trials: trialCount,
    },
    medianTrial: p50,
    bestTrial: p90,
    worstTrial: p10,
    singleRandomTrial: trials[randomIdx],
    distributions: { autos: autoDist, numbered: numberedDist },
    topAutoAthletes,
  };
}
