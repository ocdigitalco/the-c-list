/**
 * Break Sheet Builder — shared, framework-agnostic logic.
 *
 * This is the single source of truth for the Whatnot CSV output and the
 * shareable-config URL encoding used by /break-sheet-builder. The title and
 * CSV logic are ported 1:1 from the original BreakSheetModal so the new page
 * is a strict superset of the modal's behaviour.
 *
 * Nothing here touches `window` — safe to import on the server.
 */

// ─── Types ────────────────────────────────────────────────────────────────────

/** A player row as returned by the break-sheet data query. */
export interface BreakSheetPlayerRow {
  id: number;
  name: string;
  /** Most-frequent team for this player in the set ("" when unknown). */
  team: string;
  isRookie: boolean;
  /** Distinct pure-autograph insert sets (excludes mem-auto sets). */
  autoCount: number;
  hasMemAuto: boolean;
  hasRelic: boolean;
  /** Appears in at least one non-base / non-auto / non-relic insert. */
  hasInsert: boolean;
  /** Appears in an insert set that has at least one numbered parallel. */
  hasNumbered: boolean;
  /** Non-auto, non-relic, non-base insert set names (for abbreviation tags). */
  insertSetNames: string[];
}

export interface BreakSheetData {
  slug: string;
  setName: string;
  sport: string;
  league: string | null;
  sampleImageUrl: string | null;
  athleteCount: number;
  teamCount: number;
  /** Primary box format's boxes-per-case (null when unknown). */
  boxesPerCase: number | null;
  /** Primary box format's autos-per-box (null when unknown). */
  autosPerBox: number | null;
  players: BreakSheetPlayerRow[];
  teams: string[];
}

/** Editable tag labels, keyed to match the design (AUTO / MEM AUTO / RELIC / RC). */
export interface TagLabels {
  AUTO: string;
  "MEM AUTO": string;
  RELIC: string;
  RC: string;
}

export type ListingType = "Buy it Now" | "Auction";
export type LabelFormat = "Short" | "Long";
export type BreakUnit = "Cases" | "Boxes";
export type RosterMode = "athletes" | "teams";
export type CatFilter = "Total Cards" | "Autographs" | "Inserts" | "Numbered";

/** The full break configuration that is encoded into the shareable URL. */
export interface BreakConfig {
  description: string;
  listingType: ListingType;
  labelFormat: LabelFormat;
  breakUnit: BreakUnit;
  breakQty: number;
  giveaways: number;
  buyersGiveaway: boolean;
  shippingProfile: string;
  offerable: boolean;
  mode: RosterMode;
  catFilter: CatFilter;
  rookiesOnly: boolean;
  tagLabels: TagLabels;
}

// ─── Constants ────────────────────────────────────────────────────────────────

export const DEFAULT_TAG_LABELS: TagLabels = {
  AUTO: "AUTO",
  "MEM AUTO": "MEM AUTO",
  RELIC: "RELIC",
  RC: "RC",
};

export const DEFAULT_SHIPPING = "0-1 oz";

export const SHIPPING_PROFILES = ["0-1 oz", "1-3 oz", "4-7 oz", "8-11 oz", "12-15 oz"];

export const DEFAULT_CONFIG: BreakConfig = {
  description: "",
  listingType: "Buy it Now",
  labelFormat: "Short",
  breakUnit: "Cases",
  breakQty: 1,
  giveaways: 0,
  buyersGiveaway: false,
  shippingProfile: DEFAULT_SHIPPING,
  offerable: false,
  mode: "athletes",
  catFilter: "Total Cards",
  rookiesOnly: false,
  tagLabels: DEFAULT_TAG_LABELS,
};

const SPORT_CATEGORY: Record<string, string> = {
  Baseball: "MLB Breaks",
  Basketball: "NBA Breaks",
  Football: "NFL Breaks",
  Soccer: "Soccer Breaks",
  Hockey: "Hockey Breaks",
  MMA: "UFC Breaks",
  Wrestling: "WWE Breaks",
  Racing: "F1 Breaks",
  Olympics: "Olympics Breaks",
  Golf: "Golf Breaks",
};

export function categoryFor(sport: string): string {
  return SPORT_CATEGORY[sport] ?? `${sport} Breaks`;
}

/** Whatnot bulk-listing column order (mirrors the modal's CSV_HEADER). */
export const CSV_COLUMNS = [
  "Category",
  "Sub Category",
  "Title",
  "Description",
  "Quantity",
  "Type",
  "Price",
  "Shipping Profile",
  "Offerable",
  "Hazmat",
  "Condition",
  "Cost Per Item",
  "SKU",
  "Image URL 1",
  "Image URL 2",
  "Image URL 3",
  "Image URL 4",
  "Image URL 5",
  "Image URL 6",
  "Image URL 7",
  "Image URL 8",
] as const;

export type CsvColumn = (typeof CSV_COLUMNS)[number];

// ─── Title building (ported 1:1 from BreakSheetModal) ──────────────────────────

/** First-letter abbreviation of significant words, max 5 chars. */
function abbreviate(name: string): string {
  const stop = new Set(["a", "an", "the", "of", "in", "at", "for", "and", "or"]);
  const words = name.split(/\s+/).filter((w) => !stop.has(w.toLowerCase()));
  if (words.length === 0) return name.slice(0, 5).toUpperCase();
  if (words.length === 1) return words[0].slice(0, 4).toUpperCase();
  return words
    .map((w) => w[0].toUpperCase())
    .join("")
    .slice(0, 5);
}

function buildLongTitle(p: BreakSheetPlayerRow, labels: TagLabels): string {
  const tags: string[] = [];
  if (p.autoCount > 0) {
    tags.push(p.autoCount > 1 ? `${labels.AUTO}x${p.autoCount}` : labels.AUTO);
  }
  if (p.hasMemAuto) tags.push(labels["MEM AUTO"]);
  if (p.hasRelic) tags.push(labels.RELIC);
  if (p.isRookie) tags.push(labels.RC);
  for (const name of p.insertSetNames) tags.push(abbreviate(name));

  if (tags.length === 0) return p.name;
  return `${p.name} ${tags.map((t) => `(${t})`).join("")}`;
}

function buildShortTitle(p: BreakSheetPlayerRow): string {
  const parts: string[] = [];
  if (p.isRookie) parts.push("RC");
  if (p.autoCount > 0 || p.hasMemAuto) parts.push("AUTO");

  const parallelCount = p.insertSetNames.length;
  if (p.hasRelic && parallelCount === 0) {
    parts.push("1 PARALLEL");
  } else if (parallelCount > 0) {
    parts.push(parallelCount === 1 ? "1 PARALLEL" : `${parallelCount} PARALLELS`);
  }

  if (parts.length === 0) return p.name;
  return `${p.name} (${parts.join(" ")})`;
}

export function buildTitle(
  p: BreakSheetPlayerRow,
  tagLabels: TagLabels,
  labelFormat: LabelFormat
): string {
  return labelFormat === "Short" ? buildShortTitle(p) : buildLongTitle(p, tagLabels);
}

// ─── CSV ──────────────────────────────────────────────────────────────────────

/** Wrap a CSV field in quotes when it contains commas, quotes, or newlines. */
export function csvEsc(v: string): string {
  if (v.includes(",") || v.includes('"') || v.includes("\n") || v.includes("\r")) {
    return `"${v.replace(/"/g, '""')}"`;
  }
  return v;
}

/**
 * Build the Whatnot CSV from ordered row cell-maps. Uses a BOM + CRLF line
 * endings for Excel/Whatnot compatibility, matching the original modal.
 */
export function buildCsv(rows: Array<Record<string, string>>): string {
  const header = CSV_COLUMNS.join(",");
  const lines = rows.map((cells) =>
    CSV_COLUMNS.map((k) => csvEsc(cells[k] ?? "")).join(",")
  );
  return "﻿" + [header, ...lines].join("\r\n");
}

// ─── Box format math ───────────────────────────────────────────────────────────

/** Boxes / guaranteed-autos readout for the Break Format control. */
export function breakInfo(
  unit: BreakUnit,
  qty: number,
  boxesPerCase: number | null,
  autosPerBox: number | null
): { boxes: number; autos: number | null } {
  const bpc = boxesPerCase && boxesPerCase > 0 ? boxesPerCase : 1;
  const boxes = unit === "Cases" ? qty * bpc : qty;
  const autos = autosPerBox != null ? boxes * autosPerBox : null;
  return { boxes, autos };
}

// ─── Shareable config encoding ──────────────────────────────────────────────────
//
// Compact, stable query-param encoding. Only non-default values are written, so
// a freshly-selected set yields just `?set=slug`. Keys are short and versionless
// but individually named (not a base64 blob) so the URL stays legible and
// forward-compatible — unknown keys are simply ignored on decode.

const LISTING_CODES: Record<string, ListingType> = { auc: "Auction", bin: "Buy it Now" };
const CAT_CODES: Record<string, CatFilter> = {
  a: "Autographs",
  i: "Inserts",
  n: "Numbered",
};
const CAT_REVERSE: Record<CatFilter, string> = {
  "Total Cards": "",
  Autographs: "a",
  Inserts: "i",
  Numbered: "n",
};

export function configToParams(c: BreakConfig): Record<string, string> {
  const p: Record<string, string> = {};
  if (c.description) p.d = c.description;
  if (c.listingType === "Auction") p.lt = "auc";
  if (c.labelFormat === "Long") p.lf = "long";
  if (c.breakUnit === "Boxes") p.u = "b";
  if (c.breakQty !== DEFAULT_CONFIG.breakQty) p.q = String(c.breakQty);
  if (c.giveaways > 0) p.g = String(c.giveaways);
  if (c.buyersGiveaway) p.bg = "1";
  if (c.shippingProfile !== DEFAULT_SHIPPING) p.sp = c.shippingProfile;
  if (c.offerable) p.of = "1";
  if (c.mode === "teams") p.m = "t";
  if (c.catFilter !== "Total Cards") p.cf = CAT_REVERSE[c.catFilter];
  if (c.rookiesOnly) p.ro = "1";
  if (c.tagLabels.AUTO !== DEFAULT_TAG_LABELS.AUTO) p.ta = c.tagLabels.AUTO;
  if (c.tagLabels["MEM AUTO"] !== DEFAULT_TAG_LABELS["MEM AUTO"]) p.tm = c.tagLabels["MEM AUTO"];
  if (c.tagLabels.RELIC !== DEFAULT_TAG_LABELS.RELIC) p.tr = c.tagLabels.RELIC;
  if (c.tagLabels.RC !== DEFAULT_TAG_LABELS.RC) p.trc = c.tagLabels.RC;
  return p;
}

type ParamGetter = (key: string) => string | null | undefined;

export function paramsToConfig(get: ParamGetter): BreakConfig {
  const intOr = (key: string, fallback: number, min: number) => {
    const raw = get(key);
    if (raw == null) return fallback;
    const n = parseInt(raw, 10);
    return Number.isFinite(n) && n >= min ? n : fallback;
  };
  const has = (key: string) => get(key) === "1";

  const ltRaw = get("lt");
  const cfRaw = get("cf");

  return {
    description: get("d") ?? DEFAULT_CONFIG.description,
    listingType: (ltRaw && LISTING_CODES[ltRaw]) || DEFAULT_CONFIG.listingType,
    labelFormat: get("lf") === "long" ? "Long" : "Short",
    breakUnit: get("u") === "b" ? "Boxes" : "Cases",
    breakQty: intOr("q", DEFAULT_CONFIG.breakQty, 1),
    giveaways: intOr("g", DEFAULT_CONFIG.giveaways, 0),
    buyersGiveaway: has("bg"),
    shippingProfile: get("sp") ?? DEFAULT_SHIPPING,
    offerable: has("of"),
    mode: get("m") === "t" ? "teams" : "athletes",
    catFilter: (cfRaw && CAT_CODES[cfRaw]) || "Total Cards",
    rookiesOnly: has("ro"),
    tagLabels: {
      AUTO: get("ta") ?? DEFAULT_TAG_LABELS.AUTO,
      "MEM AUTO": get("tm") ?? DEFAULT_TAG_LABELS["MEM AUTO"],
      RELIC: get("tr") ?? DEFAULT_TAG_LABELS.RELIC,
      RC: get("trc") ?? DEFAULT_TAG_LABELS.RC,
    },
  };
}

/** Build the shareable path for a given set + config. */
export function buildSharePath(setSlug: string, config: BreakConfig): string {
  const params = new URLSearchParams({ set: setSlug, ...configToParams(config) });
  return `/break-sheet-builder?${params.toString()}`;
}
