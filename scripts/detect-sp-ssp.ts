/**
 * SP/SSP Auto-Detection Script
 *
 * Analyzes pack odds ratios for all sets in the DB and suggests
 * SP/SSP classifications for insert sets.
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

// ─── Thresholds ───────────────────────────────────────────────
const SSP_RATIO_THRESHOLD = 400; // X times rarer than anchor = SSP
const SP_RATIO_THRESHOLD = 50; // X times rarer than anchor = SP
const MAX_SSP_CHECKLIST = 35; // max athletes in insert for SSP
const MAX_SP_CHECKLIST = 75; // max athletes in insert for SP

// ─── Anchor odds fallback hierarchy ───────────────────────────
const ANCHOR_KEYS = [
  "Base Refractor",
  "Refractor",
  "Chrome Refractor",
  "Base Chrome Refractor",
  "Base Prizm",
  "Prizm",
  "Base",
];

// ─── Per-set anchor overrides ─────────────────────────────────
const ANCHOR_KEY_OVERRIDES: Record<string, string> = {
  "Midnight": "Base Zodiac",
  "Hoops": "Base",
  "Pristine": "Base Refractor",
};

function getAnchorKeyOverride(setName: string): string | null {
  for (const [keyword, anchorKey] of Object.entries(ANCHOR_KEY_OVERRIDES)) {
    if (setName.toLowerCase().includes(keyword.toLowerCase())) return anchorKey;
  }
  return null;
}

// ─── Exclusion keywords ────────────────────────────────────────
const EXCLUDED_KEYWORDS = [
  "disney",
  "disneyland",
  "muppets",
  "phineas",
  "goofy movie",
  "wwe",
  "deadpool",
  "marvel",
  "neon",
];

// ─── Auto keywords (to skip autograph insert sets) ─────────────
const AUTO_KEYWORDS = ["auto", "signature", "graph", "relic", "redemption"];

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
  sp: InsertSetResult[];
  ssp: InsertSetResult[];
  skipped: { name: string; reason: string }[];
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
    return den / num; // "1:26" → 26, "3:1" → 0.333
  }
  const n = parseFloat(cleaned);
  return !isNaN(n) && n > 0 ? n : null;
}

function isAutoInsert(name: string): boolean {
  const lower = name.toLowerCase();
  return AUTO_KEYWORDS.some((kw) => lower.includes(kw));
}

function findAnchorOdds(
  packOdds: Record<string, Record<string, unknown>>,
  setName: string = "",
): { key: string; odds: string; value: number } | null {
  const hobbyOdds = packOdds["hobby"] ?? {};

  // Check per-set override first
  const overrideKey = getAnchorKeyOverride(setName);
  if (overrideKey) {
    const match = findOddsKey(hobbyOdds, overrideKey);
    if (match) {
      const value = parseOdds(match.raw);
      if (value && value > 0) return { key: match.key, odds: String(match.raw), value };
    }
  }

  // Try named anchors
  for (const anchorKey of ANCHOR_KEYS) {
    const match = findOddsKey(hobbyOdds, anchorKey);
    if (match) {
      const value = parseOdds(match.raw);
      if (value && value > 0) return { key: match.key, odds: String(match.raw), value };
    }
  }

  // Fallback: find cheapest parallel-sounding key
  const parallelEntries = Object.entries(hobbyOdds)
    .filter(([k]) => /teal|pink|aqua|prism|neon pulse/i.test(k))
    .map(([k, v]) => ({ key: k, odds: String(v), value: parseOdds(v) }))
    .filter((p) => p.value !== null && p.value > 0)
    .sort((a, b) => (a.value ?? 0) - (b.value ?? 0));

  if (parallelEntries.length > 0) {
    const best = parallelEntries[0];
    return { key: best.key, odds: best.odds, value: best.value! };
  }

  return null;
}

function normalizeForMatch(s: string): string {
  return s
    .toLowerCase()
    .replace(/\s*-\s*/g, " ")  // "Base - Image Variation" → "Base Image Variation"
    .replace(/\s+/g, " ")
    .trim();
}

function findOddsKey(
  boxOdds: Record<string, unknown>,
  insertName: string
): { key: string; raw: unknown } | null {
  // Direct match
  if (boxOdds[insertName] !== undefined) {
    return { key: insertName, raw: boxOdds[insertName] };
  }

  // Normalized match (handles "Base - Image Variation" vs "Base Image Variation")
  const normName = normalizeForMatch(insertName);
  for (const [k, v] of Object.entries(boxOdds)) {
    if (normalizeForMatch(k) === normName) return { key: k, raw: v };
  }

  // Collapsed match (handles "Ultra Violet" vs "Ultraviolet")
  const collapsed = normName.replace(/\s/g, "");
  for (const [k, v] of Object.entries(boxOdds)) {
    if (normalizeForMatch(k).replace(/\s/g, "") === collapsed) return { key: k, raw: v };
  }

  return null;
}

function getOddsForInsert(
  packOdds: Record<string, Record<string, unknown>>,
  insertName: string,
  boxTypes: string[] = [
    "hobby",
    "jumbo",
    "fdi",
    "breakers_delight",
    "sapphire",
    "value_se",
    "mega_se",
    "hanger_se",
    "fanatics",
  ]
): { odds: string; value: number; boxType: string } | null {
  for (const bt of boxTypes) {
    const box = packOdds[bt];
    if (!box) continue;
    const match = findOddsKey(box, insertName);
    if (match) {
      const value = parseOdds(match.raw);
      if (value && value > 0) return { odds: String(match.raw), value, boxType: bt };
    }
  }
  return null;
}

function getConfidence(
  ratio: number,
  checklistSize: number,
  classification: "sp" | "ssp"
): "high" | "medium" | "low" {
  if (classification === "ssp") {
    if (ratio > SSP_RATIO_THRESHOLD * 1.5 && checklistSize <= 20) return "high";
    if (ratio > SSP_RATIO_THRESHOLD * 1.2 || checklistSize <= 25) return "medium";
    return "low";
  } else {
    if (ratio > SP_RATIO_THRESHOLD * 1.5 && checklistSize <= 50) return "high";
    if (ratio > SP_RATIO_THRESHOLD * 1.2 || checklistSize <= 60) return "medium";
    return "low";
  }
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

  // Detect flat vs nested odds
  const firstVal = Object.values(packOdds)[0];
  const isNested = firstVal !== null && typeof firstVal === "object" && !Array.isArray(firstVal);
  if (!isNested) {
    // Flat odds — wrap in a "hobby" key for uniform processing
    packOdds = { hobby: packOdds as unknown as Record<string, unknown> };
  }

  const anchor = findAnchorOdds(packOdds, set.name);
  if (!anchor) {
    noOddsLog.push(`${set.name} — no anchor odds found`);
    continue;
  }

  // Get all non-auto insert sets with their checklist sizes
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

  const result: SetResult = {
    setId: set.id,
    setName: set.name,
    anchorKey: anchor.key,
    anchorOdds: anchor.odds,
    sp: [],
    ssp: [],
    skipped: [],
  };

  for (const insertSet of insertSets) {
    // Skip base sets (unless they're variations/etch)
    const lower = insertSet.name.toLowerCase();
    if (
      (lower === "base set" || lower === "base cards" || lower.startsWith("base -") && !lower.includes("variation") && !lower.includes("etch"))
    ) {
      continue;
    }

    // Skip autograph insert sets
    if (isAutoInsert(insertSet.name)) continue;

    // Try to find odds — use the insert set name directly
    const oddsResult = getOddsForInsert(packOdds, insertSet.name);
    if (!oddsResult) {
      result.skipped.push({
        name: insertSet.name,
        reason: "no odds found in any box type",
      });
      continue;
    }

    const ratio = oddsResult.value / anchor.value;

    let classification: "sp" | "ssp" | "none" = "none";
    if (
      ratio >= SSP_RATIO_THRESHOLD &&
      insertSet.checklist_size <= MAX_SSP_CHECKLIST
    ) {
      classification = "ssp";
    } else if (
      ratio >= SSP_RATIO_THRESHOLD &&
      insertSet.checklist_size <= MAX_SP_CHECKLIST
    ) {
      classification = "sp";
    } else if (
      ratio >= SP_RATIO_THRESHOLD &&
      insertSet.checklist_size <= MAX_SP_CHECKLIST
    ) {
      classification = "sp";
    }

    // Check if insert has only extremely limited parallels (≤ /5) — upgrade to SSP
    if (classification !== "ssp") {
      const limitedPars = db
        .prepare(
          "SELECT print_run FROM parallels WHERE insert_set_id = ? AND print_run IS NOT NULL"
        )
        .all(insertSet.id) as { print_run: number }[];
      if (
        limitedPars.length > 0 &&
        limitedPars.every((p) => p.print_run <= 5)
      ) {
        classification = "ssp";
      }
    }

    if (classification === "none") continue;

    const confidence = getConfidence(
      ratio,
      insertSet.checklist_size,
      classification
    );

    const entry: InsertSetResult = {
      name: insertSet.name,
      ratio: Math.round(ratio),
      checklistSize: insertSet.checklist_size,
      odds: oddsResult.odds,
      anchorOdds: anchor.odds,
      classification,
      confidence,
      boxTypeUsed: oddsResult.boxType,
    };

    if (classification === "ssp") result.ssp.push(entry);
    else result.sp.push(entry);
  }

  if (result.sp.length > 0 || result.ssp.length > 0) {
    results.push(result);
  }
}

// ─── Output ───────────────────────────────────────────────────

console.log("=".repeat(70));
console.log("  SP/SSP DETECTION RESULTS");
console.log("=".repeat(70));

for (const result of results) {
  console.log(`\n  ${result.setName}`);
  console.log(`  Anchor: ${result.anchorKey} (${result.anchorOdds})`);

  if (result.sp.length > 0) {
    console.log(`\n  SHORT PRINTS (SP):`);
    for (const entry of result.sp) {
      const conf =
        entry.confidence === "high"
          ? "[high]"
          : entry.confidence === "medium"
          ? "[med] "
          : "[low] ";
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
        entry.confidence === "high"
          ? "[high]"
          : entry.confidence === "medium"
          ? "[med] "
          : "[low] ";
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
  console.log(`  "${result.setName}": {`);

  if (result.sp.length > 0) {
    console.log(`    sp: [`);
    for (const entry of result.sp) {
      const flag =
        entry.confidence !== "high"
          ? ` // ${entry.confidence} confidence`
          : "";
      const name = entry.name.includes("'")
        ? `"${entry.name}"`
        : `"${entry.name}"`;
      console.log(`      ${name},${flag}`);
    }
    console.log(`    ],`);
  } else {
    console.log(`    sp: [],`);
  }

  if (result.ssp.length > 0) {
    console.log(`    ssp: [`);
    for (const entry of result.ssp) {
      const flag =
        entry.confidence !== "high"
          ? ` // ${entry.confidence} confidence`
          : "";
      const name = entry.name.includes("'")
        ? `"${entry.name}"`
        : `"${entry.name}"`;
      console.log(`      ${name},${flag}`);
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
console.log(`  Sets with results: ${results.length}`);
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
