/**
 * Client-side Monte Carlo simulation engine.
 * NO database imports — runs entirely in the browser.
 * Receives pre-fetched pool data from the API.
 */

// ─── Types (shared with server) ──────────────────────────────────────────────

export interface SimPoolCard {
  insertSetId: number;
  insertSetName: string;
  parallelName: string | null;
  oddsKey: string;
  weight: number;
  isAuto: boolean;
  isNumbered: boolean;
  totalAppsInIS: number;
  athletes: { id: number; name: string; apps: number }[];
}

export interface BoxFormatConfig {
  label: string;
  packsPerBox: number;
  boxesPerCase: number;
  guaranteedAutos: number;
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

// ─── Sampling ────────────────────────────────────────────────────────────────

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
    let autosRemaining = guaranteedAutos;

    for (let pack = 0; pack < packsPerBox; pack++) {
      const packNum = box * packsPerBox + pack + 1;

      for (let card = 0; card < cardsPerPack; card++) {
        let sampled: SimPoolCard;

        if (autosRemaining > 0 && autoPool.length > 0 && card === 0) {
          sampled = weightedSampleCard(autoPool);
          autosRemaining--;
        } else {
          sampled = weightedSampleCard(fullPool);
        }

        const athlete = weightedSampleAthlete(sampled);

        pulls.push({
          packNumber: packNum,
          athleteName: athlete.name,
          insertSetName: sampled.insertSetName,
          parallelName: sampled.parallelName,
          printRun: null,
          isAuto: sampled.isAuto,
          isNumbered: sampled.isNumbered,
        });

        if (sampled.isAuto) autoCount++;
        if (sampled.isNumbered) numberedCount++;
      }
    }
  }

  return { pulls, autoCount, numberedCount, totalCards: pulls.length };
}

// ─── Main simulation function ────────────────────────────────────────────────

export function runSimulation(
  config: SimConfig,
  boxCount: number = 1,
  trialCount: number = 10000
): SimulationResult {
  const trials: BreakTrial[] = [];

  for (let i = 0; i < trialCount; i++) {
    trials.push(simulateOneTrial(config, boxCount));
  }

  const sorted = [...trials].sort((a, b) => a.autoCount - b.autoCount);
  const p10 = sorted[Math.floor(trialCount * 0.1)];
  const p50 = sorted[Math.floor(trialCount * 0.5)];
  const p90 = sorted[Math.floor(trialCount * 0.9)];
  const randomIdx = Math.floor(Math.random() * trialCount);

  const autoDist: Record<number, number> = {};
  const numberedDist: Record<number, number> = {};
  const autoAthleteCount = new Map<string, number>();

  for (const trial of trials) {
    autoDist[trial.autoCount] = (autoDist[trial.autoCount] ?? 0) + 1;
    numberedDist[trial.numberedCount] = (numberedDist[trial.numberedCount] ?? 0) + 1;

    const seenAuto = new Set<string>();
    for (const pull of trial.pulls) {
      if (pull.isAuto && !seenAuto.has(pull.athleteName)) {
        seenAuto.add(pull.athleteName);
        autoAthleteCount.set(pull.athleteName, (autoAthleteCount.get(pull.athleteName) ?? 0) + 1);
      }
    }
  }

  for (const k in autoDist) autoDist[k] = autoDist[k] / trialCount;
  for (const k in numberedDist) numberedDist[k] = numberedDist[k] / trialCount;

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
