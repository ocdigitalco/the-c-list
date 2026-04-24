/**
 * SP/SSP Auto-Detection Script
 *
 * Analyzes pack odds ratios for all sets in the DB and suggests
 * SP/SSP classifications for insert sets.
 *
 * Uses dynamic per-set percentile thresholds based on each set's own
 * base insert odds distribution. Focuses on base insert pull rates only,
 * excluding parallels, SuperFractors, and autograph sets.
 *
 * Usage: npx tsx scripts/detect-sp-ssp.ts
 * Optional: npx tsx scripts/detect-sp-ssp.ts --set "2025 Topps Chrome Football"
 *
 * Output: Suggested entries for src/lib/spSspConfig.ts
 * Review all suggestions before adding to the config file.
 *
 * READ-ONLY — does not write to the database.
 */

import Database from "better-sqlite3";

const db = new Database("the-c-list.db");

// ─── Fixed fallback thresholds (used when < MIN_SAMPLE_SIZE inserts) ──
const FALLBACK_SP_RATIO = 50;
const FALLBACK_SSP_RATIO = 400;
const MAX_SP_CHECKLIST = 75;
const MIN_SAMPLE_SIZE = 8;

// ─── Anchor key patterns (ordered fallback per set name fragment) ──
const ANCHOR_KEY_PATTERNS: Record<string, string[]> = {
  "Bowman": [
    "Chrome Prospects Refractor",
    "Chrome Prospect Refractor",
    "Base Chrome Refractor",
    "Chrome Refractor",
  ],
  "Midnight": ["Base Zodiac", "Base"],
  "Hoops": ["Base"],
  "Pristine": ["Base Refractor"],
};

// ─── Global anchor fallback hierarchy ─────────────────────────
const ANCHOR_KEYS = [
  "Base Refractor",
  "Refractor",
  "Chrome Refractor",
  "Base Chrome Refractor",
  "Base Prizm",
  "Prizm",
  "Base",
];

// ─── Dynamic anchor detection constants ───────────────────────
const MIN_ANCHOR_ODDS = 10;
const MAX_ANCHOR_ODDS = 300;

const DYNAMIC_CHROME_KEYWORDS = [
  "refractor", "x-fractor", "shimmer", "logofractor", "prizm",
  "lava", "wave", "speckle", "mojo", "raywave", "fractor",
];

const DYNAMIC_EXCLUDE_KEYWORDS = [
  "gold", "silver", "red", "blue", "green", "orange", "black",
  "purple", "pink", "aqua", "teal", "yellow", "fuchsia", "rose",
  "reptilian", "superfractor", "firefractor", "printing plates",
  "autograph", "auto", "geometric", "mini", "league",
  "bowman logo", "lazer", "gum ball", "sunflower", "peanuts", "pop corn",
  "steel", "grass", "packfractor", "image variation", "etched",
];

// ─── Exclusion keywords ────────────────────────────────────────
const EXCLUDED_KEYWORDS = [
  "disney", "disneyland", "muppets", "phineas",
  "goofy movie", "wwe", "deadpool", "marvel", "neon",
];

// ─── Auto keywords (to skip autograph insert sets) ─────────────
const AUTO_KEYWORDS = ["auto", "signature", "graph", "relic", "redemption"];

// ─── Parallel qualifier words ──────────────────────────────────
const PARALLEL_QUALIFIERS = [
  "gold", "silver", "red", "blue", "green", "orange", "black", "white",
  "purple", "pink", "aqua", "teal", "yellow", "fuchsia", "rose",
  "superfractor", "firefractor", "lava", "wave", "shimmer", "speckle",
  "x-fractor", "xfractor", "geometric", "mojo", "crystal", "mini-diamond",
  "reptilian", "padparadscha", "sapphire", "prizm", "daybreak", "midnight",
  "moonrise", "moon beam", "dusk", "black light", "twilight parallel",
  "retrofractor", "etched", "floorboard", "steel", "burgundy", "navy",
  "pattern", "border",
];

// ─── Types ────────────────────────────────────────────────────
interface InsertSetResult {
  name: string;
  ratio: number;
  checklistSize: number;
  odds: string;
  anchorOdds: string;
  classification: "sp" | "ssp";
  confidence: "high" | "medium" | "low";
  boxTypeUsed: string;
}

interface SetResult {
  setId: number;
  setName: string;
  anchorKey: string;
  anchorOdds: string;
  anchorSource: "override" | "global" | "dynamic";
  spThreshold: number;
  sspThreshold: number;
  sampleSize: number;
  usedFallback: boolean;
  sp: InsertSetResult[];
  ssp: InsertSetResult[];
  skipped: { name: string; reason: string }[];
}

interface DynamicThresholds {
  spThreshold: number;
  sspThreshold: number;
  sampleSize: number;
  usedFallback: boolean;
}

// ─── Utilities ────────────────────────────────────────────────

function parseOdds(oddsStr: unknown): number | null {
  if (typeof oddsStr === "number") return oddsStr > 0 ? oddsStr : null;
  if (typeof oddsStr !== "string") return null;
  const cleaned = oddsStr.replace(/\s/g, "").replace(/,/g, "");
  if (cleaned.includes(":")) {
    const parts = cleaned.split(":");
    if (parts.length !== 2) return null;
    const num = parseFloat(parts[0]);
    const den = parseFloat(parts[1]);
    if (isNaN(num) || isNaN(den) || num === 0) return null;
    return den / num;
  }
  const n = parseFloat(cleaned);
  return !isNaN(n) && n > 0 ? n : null;
}

function isAutoInsert(name: string): boolean {
  const lower = name.toLowerCase();
  return AUTO_KEYWORDS.some((kw) => lower.includes(kw));
}

function normalizeForMatch(s: string): string {
  return s
    .toLowerCase()
    .replace(/\s*-\s*/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function findOddsKey(
  boxOdds: Record<string, unknown>,
  insertName: string
): { key: string; raw: unknown } | null {
  if (boxOdds[insertName] !== undefined)
    return { key: insertName, raw: boxOdds[insertName] };

  const normName = normalizeForMatch(insertName);
  for (const [k, v] of Object.entries(boxOdds)) {
    if (normalizeForMatch(k) === normName) return { key: k, raw: v };
  }

  const collapsed = normName.replace(/\s/g, "");
  for (const [k, v] of Object.entries(boxOdds)) {
    if (normalizeForMatch(k).replace(/\s/g, "") === collapsed) return { key: k, raw: v };
  }

  return null;
}

/**
 * Returns true if the odds key represents the BASE insert odds
 * (not a parallel variant).
 */
function isBaseInsertKey(oddsKey: string, insertName: string): boolean {
  const key = normalizeForMatch(oddsKey);
  const name = normalizeForMatch(insertName);

  if (key === name) return true;
  if (key === name + " refractor") return true;

  if (key.startsWith(name)) {
    const suffix = key.slice(name.length).trim();
    if (suffix === "" || suffix === "refractor") return true;
    const hasParallelQualifier = PARALLEL_QUALIFIERS.some((q) => suffix.includes(q));
    if (hasParallelQualifier) return false;
  }

  // Collapsed match
  const keyCollapsed = key.replace(/\s/g, "");
  const nameCollapsed = name.replace(/\s/g, "");
  if (keyCollapsed === nameCollapsed) return true;
  if (keyCollapsed === nameCollapsed + "refractor") return true;

  return false;
}

/**
 * Find the base insert odds for a given insert set name from pack_odds.
 */
function getBaseInsertOdds(
  packOdds: Record<string, Record<string, unknown>>,
  insertName: string,
  boxTypes: string[] = [
    "hobby", "jumbo", "fdi", "breakers_delight", "sapphire",
    "value_se", "mega_se", "hanger_se", "fanatics",
  ]
): { odds: string; value: number; boxType: string } | null {
  for (const bt of boxTypes) {
    const box = packOdds[bt];
    if (!box) continue;
    for (const [key, raw] of Object.entries(box)) {
      if (isBaseInsertKey(key, insertName)) {
        const value = parseOdds(raw);
        if (value && value > 0) return { odds: String(raw), value, boxType: bt };
      }
    }
  }
  return null;
}

function findAnchorOdds(
  packOdds: Record<string, Record<string, unknown>>,
  setName: string = "",
): { key: string; odds: string; value: number; source: "override" | "global" | "dynamic" } | null {
  const hobbyOdds = packOdds["hobby"] ?? {};

  // 1. Pattern overrides — try each pattern in order for matching set name
  for (const [fragment, patterns] of Object.entries(ANCHOR_KEY_PATTERNS)) {
    if (!setName.toLowerCase().includes(fragment.toLowerCase())) continue;
    for (const pattern of patterns) {
      const match = findOddsKey(hobbyOdds, pattern);
      if (match) {
        const value = parseOdds(match.raw);
        if (value && value > 0) return { key: match.key, odds: String(match.raw), value, source: "override" };
      }
    }
  }

  // 2. Global fallback hierarchy
  for (const anchorKey of ANCHOR_KEYS) {
    const match = findOddsKey(hobbyOdds, anchorKey);
    if (match) {
      const value = parseOdds(match.raw);
      if (value && value > 0) return { key: match.key, odds: String(match.raw), value, source: "global" };
    }
  }

  // 3. Dynamic auto-detection — find median chrome-type refractor in valid range
  const candidates: { key: string; odds: string; value: number }[] = [];
  for (const [key, raw] of Object.entries(hobbyOdds)) {
    const kl = key.toLowerCase();
    const isChrome = DYNAMIC_CHROME_KEYWORDS.some((kw) => kl.includes(kw));
    if (!isChrome) continue;
    const isExcluded = DYNAMIC_EXCLUDE_KEYWORDS.some((q) => kl.includes(q));
    if (isExcluded) continue;
    const value = parseOdds(raw);
    if (value === null || value < MIN_ANCHOR_ODDS || value > MAX_ANCHOR_ODDS) continue;
    candidates.push({ key, odds: String(raw), value });
  }

  if (candidates.length > 0) {
    candidates.sort((a, b) => a.value - b.value);
    const chosen = candidates[Math.floor(candidates.length / 2)];
    return { key: chosen.key, odds: chosen.odds, value: chosen.value, source: "dynamic" };
  }

  return null;
}

/**
 * Compute dynamic SP/SSP thresholds based on the set's own
 * base insert odds distribution.
 */
function computeDynamicThresholds(
  baseInsertOddsValues: number[],
  anchorOddsValue: number,
): DynamicThresholds {
  const sorted = [...baseInsertOddsValues].sort((a, b) => a - b);
  const n = sorted.length;

  if (n < MIN_SAMPLE_SIZE) {
    return {
      spThreshold: anchorOddsValue * FALLBACK_SP_RATIO,
      sspThreshold: anchorOddsValue * FALLBACK_SSP_RATIO,
      sampleSize: n,
      usedFallback: true,
    };
  }

  const p85index = Math.floor(n * 0.85);
  const p95index = Math.floor(n * 0.95);

  return {
    spThreshold: sorted[Math.min(p85index, n - 1)],
    sspThreshold: sorted[Math.min(p95index, n - 1)],
    sampleSize: n,
    usedFallback: false,
  };
}

// ─── Main ─────────────────────────────────────────────────────

const setFilter = process.argv.includes("--set")
  ? process.argv[process.argv.indexOf("--set") + 1]
  : null;

const sets = db
  .prepare(
    `SELECT id, name, pack_odds FROM sets
     WHERE pack_odds IS NOT NULL AND pack_odds != '{}' AND pack_odds != ''
     ${setFilter ? "AND name LIKE ?" : ""}
     ORDER BY name`
  )
  .all(...(setFilter ? [`%${setFilter}%`] : [])) as {
  id: number;
  name: string;
  pack_odds: string;
}[];

console.log(`\nAnalyzing ${sets.length} sets with pack odds...\n`);

const results: SetResult[] = [];
const noOddsLog: string[] = [];
const excludedLog: string[] = [];

for (const set of sets) {
  const isExcluded = EXCLUDED_KEYWORDS.some((kw) =>
    set.name.toLowerCase().includes(kw)
  );
  if (isExcluded) {
    excludedLog.push(set.name);
    continue;
  }

  let packOdds: Record<string, Record<string, unknown>>;
  try {
    packOdds = JSON.parse(set.pack_odds);
  } catch {
    noOddsLog.push(`${set.name} — invalid JSON`);
    continue;
  }

  const firstVal = Object.values(packOdds)[0];
  const isNested = firstVal !== null && typeof firstVal === "object" && !Array.isArray(firstVal);
  if (!isNested) {
    packOdds = { hobby: packOdds as unknown as Record<string, unknown> };
  }

  const anchor = findAnchorOdds(packOdds, set.name);
  if (!anchor) {
    noOddsLog.push(`${set.name} — no anchor odds found`);
    continue;
  }

  // Get all non-auto insert sets with checklist sizes
  const insertSets = db
    .prepare(
      `SELECT ins.id, ins.name,
        COUNT(DISTINCT pa.player_id) as checklist_size
       FROM insert_sets ins
       LEFT JOIN player_appearances pa ON pa.insert_set_id = ins.id
       WHERE ins.set_id = ?
       GROUP BY ins.id, ins.name
       HAVING checklist_size > 0
       ORDER BY checklist_size ASC`
    )
    .all(set.id) as { id: number; name: string; checklist_size: number }[];

  const skipped: { name: string; reason: string }[] = [];

  // ── Pass 1: collect base insert odds for all non-auto inserts ──
  const MAX_SSP_CHECKLIST = 75;

  interface InsertBaseOdds {
    id: number;
    name: string;
    checklistSize: number;
    baseOdds: string;
    baseOddsValue: number;
    boxTypeUsed: string;
  }

  const insertsWithBaseOdds: InsertBaseOdds[] = [];

  for (const insertSet of insertSets) {
    const lower = insertSet.name.toLowerCase();
    if (
      lower === "base set" ||
      lower === "base cards" ||
      (lower.startsWith("base") &&
        !lower.includes("variation") &&
        !lower.includes("etch") &&
        !lower.includes("chrome") &&
        !lower.includes("prospect") &&
        !lower.includes("paper"))
    ) {
      continue;
    }

    if (isAutoInsert(insertSet.name)) continue;

    const baseOdds = getBaseInsertOdds(packOdds, insertSet.name);
    if (!baseOdds) {
      skipped.push({ name: insertSet.name, reason: "no base insert odds found" });
      continue;
    }

    insertsWithBaseOdds.push({
      id: insertSet.id,
      name: insertSet.name,
      checklistSize: insertSet.checklist_size,
      baseOdds: baseOdds.odds,
      baseOddsValue: baseOdds.value,
      boxTypeUsed: baseOdds.boxType,
    });
  }

  // ── Pass 2: compute dynamic thresholds (only from ratio-eligible inserts) ──
  const thresholdEligibleOdds = insertsWithBaseOdds
    .filter((i) => i.baseOddsValue > anchor.value)
    .map((i) => i.baseOddsValue);
  const thresholds = computeDynamicThresholds(thresholdEligibleOdds, anchor.value);

  // ── Pass 3: classify each insert ──
  const spResults: InsertSetResult[] = [];
  const sspResults: InsertSetResult[] = [];

  for (const insert of insertsWithBaseOdds) {
    const ratio = insert.baseOddsValue / anchor.value;

    // Skip inserts easier to pull than the anchor — can never be SP/SSP
    if (insert.baseOddsValue <= anchor.value) {
      skipped.push({
        name: insert.name,
        reason: `easier than anchor (${insert.baseOdds} vs anchor ${anchor.odds})`,
      });
      continue;
    }

    let classification: "sp" | "ssp" | "none" = "none";

    if (insert.baseOddsValue >= thresholds.sspThreshold) {
      classification = "ssp";
    } else if (insert.baseOddsValue >= thresholds.spThreshold) {
      classification = "sp";
    }

    // Limited parallel structure signal — upgrade to SSP
    if (classification !== "ssp") {
      const limitedPars = db
        .prepare(
          "SELECT print_run FROM parallels WHERE insert_set_id = ? AND print_run IS NOT NULL"
        )
        .all(insert.id) as { print_run: number }[];
      if (limitedPars.length > 0 && limitedPars.every((p) => p.print_run <= 5)) {
        classification = "ssp";
      }
    }

    if (classification === "none") continue;

    // Per-tier checklist size guard
    if (classification === "sp" && insert.checklistSize > MAX_SP_CHECKLIST) {
      skipped.push({ name: insert.name, reason: `checklist too large for SP (${insert.checklistSize})` });
      continue;
    }
    if (classification === "ssp" && insert.checklistSize > MAX_SSP_CHECKLIST) {
      skipped.push({ name: insert.name, reason: `checklist too large for SSP (${insert.checklistSize})` });
      continue;
    }

    // Confidence based on margin beyond threshold
    let confidence: "high" | "medium" | "low";
    if (classification === "ssp") {
      const margin = insert.baseOddsValue / thresholds.sspThreshold;
      confidence = margin > 2 ? "high" : margin > 1.3 ? "medium" : "low";
    } else {
      const margin = insert.baseOddsValue / thresholds.spThreshold;
      confidence = margin > 2 ? "high" : margin > 1.3 ? "medium" : "low";
    }

    const entry: InsertSetResult = {
      name: insert.name,
      ratio: Math.round(ratio),
      checklistSize: insert.checklistSize,
      odds: insert.baseOdds,
      anchorOdds: anchor.odds,
      classification,
      confidence,
      boxTypeUsed: insert.boxTypeUsed,
    };

    if (classification === "ssp") sspResults.push(entry);
    else spResults.push(entry);
  }

  if (spResults.length > 0 || sspResults.length > 0) {
    results.push({
      setId: set.id,
      setName: set.name,
      anchorKey: anchor.key,
      anchorOdds: anchor.odds,
      anchorSource: anchor.source,
      spThreshold: thresholds.spThreshold,
      sspThreshold: thresholds.sspThreshold,
      sampleSize: thresholds.sampleSize,
      usedFallback: thresholds.usedFallback,
      sp: spResults,
      ssp: sspResults,
      skipped,
    });
  } else if (skipped.length > 0) {
    // Still show sets with skipped inserts but no results
    results.push({
      setId: set.id,
      setName: set.name,
      anchorKey: anchor.key,
      anchorOdds: anchor.odds,
      anchorSource: anchor.source,
      spThreshold: thresholds.spThreshold,
      sspThreshold: thresholds.sspThreshold,
      sampleSize: thresholds.sampleSize,
      usedFallback: thresholds.usedFallback,
      sp: [],
      ssp: [],
      skipped,
    });
  }
}

// ─── Output ───────────────────────────────────────────────────

console.log("=".repeat(70));
console.log("  SP/SSP DETECTION RESULTS");
console.log("=".repeat(70));

for (const result of results) {
  if (result.sp.length === 0 && result.ssp.length === 0) continue;

  console.log(`\n  ${result.setName}`);
  console.log(`  Anchor: ${result.anchorKey} (${result.anchorOdds}) [${result.anchorSource}]`);
  console.log(
    `  Thresholds: SP > 1:${Math.round(result.spThreshold)} | SSP > 1:${Math.round(result.sspThreshold)} | ${
      result.usedFallback
        ? "fixed ratio fallback"
        : `${result.sampleSize} inserts sampled`
    }`
  );

  if (result.sp.length > 0) {
    console.log(`\n  SHORT PRINTS (SP):`);
    for (const entry of result.sp) {
      const conf =
        entry.confidence === "high" ? "[high]" : entry.confidence === "medium" ? "[med] " : "[low] ";
      console.log(`    ${conf} ${entry.name}`);
      console.log(
        `           Ratio: ${entry.ratio}x | Odds: ${entry.odds} | Checklist: ${entry.checklistSize} | Box: ${entry.boxTypeUsed}`
      );
    }
  }

  if (result.ssp.length > 0) {
    console.log(`\n  SUPER SHORT PRINTS (SSP):`);
    for (const entry of result.ssp) {
      const conf =
        entry.confidence === "high" ? "[high]" : entry.confidence === "medium" ? "[med] " : "[low] ";
      console.log(`    ${conf} ${entry.name}`);
      console.log(
        `           Ratio: ${entry.ratio}x | Checklist: ${entry.checklistSize} | Odds: ${entry.odds} | Box: ${entry.boxTypeUsed}`
      );
    }
  }

  if (result.skipped.length > 0) {
    console.log(`\n  SKIPPED (${result.skipped.length}):`);
    for (const skip of result.skipped.slice(0, 10)) {
      console.log(`    - ${skip.name}: ${skip.reason}`);
    }
    if (result.skipped.length > 10) {
      console.log(`    ... and ${result.skipped.length - 10} more`);
    }
  }
}

// ─── Config suggestion output ──────────────────────────────────

console.log("\n\n" + "=".repeat(70));
console.log("  SUGGESTED spSspConfig.ts ENTRIES");
console.log("  Review all entries before adding to the config file.");
console.log("=".repeat(70));
console.log();

for (const result of results) {
  if (result.sp.length === 0 && result.ssp.length === 0) continue;

  console.log(`  "${result.setName}": {`);

  if (result.sp.length > 0) {
    console.log(`    sp: [`);
    for (const entry of result.sp) {
      const flag = entry.confidence !== "high" ? ` // ${entry.confidence} confidence` : "";
      console.log(`      "${entry.name}",${flag}`);
    }
    console.log(`    ],`);
  } else {
    console.log(`    sp: [],`);
  }

  if (result.ssp.length > 0) {
    console.log(`    ssp: [`);
    for (const entry of result.ssp) {
      const flag = entry.confidence !== "high" ? ` // ${entry.confidence} confidence` : "";
      console.log(`      "${entry.name}",${flag}`);
    }
    console.log(`    ],`);
  } else {
    console.log(`    ssp: [],`);
  }

  console.log(`  },`);
  console.log();
}

// ─── Summary ──────────────────────────────────────────────────

console.log("=".repeat(70));
console.log("  SUMMARY");
console.log("=".repeat(70));
console.log(`  Sets analyzed:     ${sets.length}`);
console.log(`  Sets with results: ${results.filter((r) => r.sp.length > 0 || r.ssp.length > 0).length}`);
console.log(`  Sets excluded:     ${excludedLog.length}`);
console.log(`  Sets skipped:      ${noOddsLog.length}`);
console.log();

if (excludedLog.length > 0) {
  console.log("  Excluded sets:");
  excludedLog.forEach((s) => console.log(`    - ${s}`));
  console.log();
}

if (noOddsLog.length > 0) {
  console.log("  Skipped sets (no usable anchor odds):");
  noOddsLog.forEach((s) => console.log(`    - ${s}`));
  console.log();
}

db.close();
