/**
 * Client-side Monte Carlo simulation engine.
 * NO database imports — runs entirely in the browser.
 * Receives pre-fetched pool data from the API.
 *
 * Structurally accurate: respects box guarantees, fixed card counts,
 * and pack-level slot distribution.
 */

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
  numberedPerBox?: number;
  insertsPerBox?: number;
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
  config: {
    setName: string;
    boxType: string;
    boxCount: number;
    trials: number;
    totalCards: number;
    guaranteedAutos: number;
  };
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

function weightedSampleAthlete(card: SimPoolCard): string {
  const athletes = card.athletes;
  if (athletes.length === 0) return "Unknown";
  const totalApps = athletes.reduce((s, a) => s + a.apps, 0);
  let r = Math.random() * totalApps;
  for (const a of athletes) {
    r -= a.apps;
    if (r <= 0) return a.name;
  }
  return athletes[athletes.length - 1].name;
}

// Pre-compute cumulative weights for faster sampling
interface WeightedPool {
  cards: SimPoolCard[];
  cumWeights: number[];
  totalWeight: number;
}

function buildWeightedPool(cards: SimPoolCard[]): WeightedPool {
  const cumWeights: number[] = [];
  let total = 0;
  for (const c of cards) {
    total += c.weight;
    cumWeights.push(total);
  }
  return { cards, cumWeights, totalWeight: total };
}

function sampleFrom(wp: WeightedPool): SimPoolCard {
  const r = Math.random() * wp.totalWeight;
  // Binary search for the right card
  let lo = 0;
  let hi = wp.cumWeights.length - 1;
  while (lo < hi) {
    const mid = (lo + hi) >>> 1;
    if (wp.cumWeights[mid] <= r) lo = mid + 1;
    else hi = mid;
  }
  return wp.cards[lo];
}

function makePull(card: SimPoolCard, packNum: number): PackPull {
  return {
    packNumber: packNum,
    athleteName: weightedSampleAthlete(card),
    insertSetName: card.insertSetName,
    parallelName: card.parallelName,
    printRun: null,
    isAuto: card.isAuto,
    isNumbered: card.isNumbered,
  };
}

// ─── Guarantee distribution ──────────────────────────────────────────────────

interface PackSlots {
  autos: number;
  numbered: number;
  inserts: number;
}

function distributeGuarantees(
  totalPacks: number,
  autos: number,
  numbered: number,
  inserts: number,
  cardsPerPack: number
): PackSlots[] {
  const slots: PackSlots[] = Array.from({ length: totalPacks }, () => ({
    autos: 0,
    numbered: 0,
    inserts: 0,
  }));

  // Spread each guarantee type evenly across packs
  function spread(count: number, field: keyof PackSlots) {
    if (count <= 0 || totalPacks === 0) return;
    const interval = totalPacks / count;
    for (let i = 0; i < count; i++) {
      let packIdx = Math.min(Math.floor(i * interval), totalPacks - 1);
      // If this pack is already full, find the next available
      while (
        packIdx < totalPacks &&
        slots[packIdx].autos + slots[packIdx].numbered + slots[packIdx].inserts >= cardsPerPack
      ) {
        packIdx++;
      }
      if (packIdx < totalPacks) {
        slots[packIdx][field]++;
      }
    }
  }

  spread(autos, "autos");
  spread(numbered, "numbered");
  spread(inserts, "inserts");

  return slots;
}

// ─── Single trial ────────────────────────────────────────────────────────────

function simulateOneTrial(
  fullWP: WeightedPool,
  autoWP: WeightedPool | null,
  numberedWP: WeightedPool | null,
  insertWP: WeightedPool | null,
  packSlots: PackSlots[],
  cardsPerPack: number,
  totalPacks: number
): BreakTrial {
  const pulls: PackPull[] = [];
  let autoCount = 0;
  let numberedCount = 0;

  for (let pack = 0; pack < totalPacks; pack++) {
    const packNum = pack + 1;
    const gs = packSlots[pack];

    // Guaranteed auto slots
    for (let i = 0; i < gs.autos; i++) {
      if (autoWP && autoWP.cards.length > 0) {
        const pull = makePull(sampleFrom(autoWP), packNum);
        pulls.push(pull);
        if (pull.isAuto) autoCount++;
        if (pull.isNumbered) numberedCount++;
      }
    }

    // Guaranteed numbered slots
    for (let i = 0; i < gs.numbered; i++) {
      if (numberedWP && numberedWP.cards.length > 0) {
        const pull = makePull(sampleFrom(numberedWP), packNum);
        pulls.push(pull);
        if (pull.isAuto) autoCount++;
        if (pull.isNumbered) numberedCount++;
      }
    }

    // Guaranteed insert slots
    for (let i = 0; i < gs.inserts; i++) {
      if (insertWP && insertWP.cards.length > 0) {
        const pull = makePull(sampleFrom(insertWP), packNum);
        pulls.push(pull);
        if (pull.isAuto) autoCount++;
        if (pull.isNumbered) numberedCount++;
      }
    }

    // Remaining slots from full weighted pool
    const guaranteed = gs.autos + gs.numbered + gs.inserts;
    const remaining = cardsPerPack - guaranteed;
    for (let i = 0; i < remaining; i++) {
      const pull = makePull(sampleFrom(fullWP), packNum);
      pulls.push(pull);
      if (pull.isAuto) autoCount++;
      if (pull.isNumbered) numberedCount++;
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
  const { pool, boxConfig, cardsPerPack } = config;
  const { packsPerBox, guaranteedAutos } = boxConfig;
  const numberedPerBox = config.numberedPerBox ?? 0;
  const insertsPerBox = config.insertsPerBox ?? 0;

  const totalPacks = packsPerBox * boxCount;
  const totalCards = cardsPerPack * totalPacks;
  const totalGuaranteedAutos = guaranteedAutos * boxCount;
  const totalGuaranteedNumbered = numberedPerBox * boxCount;
  const totalGuaranteedInserts = insertsPerBox * boxCount;

  // Build sub-pools
  const autoCards = pool.filter((c) => c.isAuto);
  const numberedCards = pool.filter((c) => c.isNumbered && !c.isAuto);
  // Insert pool: non-base, non-auto, non-numbered cards
  const insertCards = pool.filter(
    (c) =>
      !c.isAuto &&
      !c.isNumbered &&
      !c.insertSetName.startsWith("Base")
  );

  const fullWP = buildWeightedPool(pool);
  const autoWP = autoCards.length > 0 ? buildWeightedPool(autoCards) : null;
  const numberedWP = numberedCards.length > 0 ? buildWeightedPool(numberedCards) : null;
  const insertWP = insertCards.length > 0 ? buildWeightedPool(insertCards) : null;

  // Distribute guarantees across packs
  const packSlots = distributeGuarantees(
    totalPacks,
    totalGuaranteedAutos,
    totalGuaranteedNumbered,
    totalGuaranteedInserts,
    cardsPerPack
  );

  // Run trials
  const trials: BreakTrial[] = [];
  for (let i = 0; i < trialCount; i++) {
    trials.push(
      simulateOneTrial(fullWP, autoWP, numberedWP, insertWP, packSlots, cardsPerPack, totalPacks)
    );
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

  for (const trial of trials) {
    autoDist[trial.autoCount] = (autoDist[trial.autoCount] ?? 0) + 1;
    numberedDist[trial.numberedCount] = (numberedDist[trial.numberedCount] ?? 0) + 1;

    const seenAuto = new Set<string>();
    for (const pull of trial.pulls) {
      if (pull.isAuto && !seenAuto.has(pull.athleteName)) {
        seenAuto.add(pull.athleteName);
        autoAthleteCount.set(
          pull.athleteName,
          (autoAthleteCount.get(pull.athleteName) ?? 0) + 1
        );
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
      totalCards,
      guaranteedAutos: totalGuaranteedAutos,
    },
    medianTrial: p50,
    bestTrial: p90,
    worstTrial: p10,
    singleRandomTrial: trials[randomIdx],
    distributions: { autos: autoDist, numbered: numberedDist },
    topAutoAthletes,
  };
}
