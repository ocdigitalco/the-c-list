/**
 * Pure odds-row resolver shared by the set-scoped athlete page's parallel table.
 *
 * Mirrors the set page's `oddsResolver`: a row resolves against the first format
 * (in preference order) whose odds carry that row's own key. A parallel row
 * resolves ONLY "<Subset> <Parallel>" composites — it never falls back to the
 * main base set's "Base <Parallel>" key or to a bare parallel key, so a subset
 * with no odds in any format renders "—" instead of borrowing the base set's
 * figure. A base row resolves "<Subset>" (+ the legacy "<Subset> Base").
 */
import { findOddsKey } from "./oddsUtils";
import { ODDS_FORMAT_PREFERENCE } from "./boxLabels";

export type OddsFormat = { key: string; odds: Record<string, string | number> };
export type ResolvedOdds = { value: string | number; formatKey: string };

/** Parallel-name spellings to try: strip a trailing " Refractor", RayWave, X-Fractor. */
export function normalizeParallelNameShared(name: string): string[] {
  const candidates = [name];
  if (name.endsWith(" Refractor")) candidates.push(name.replace(/ Refractor$/, ""));
  candidates.push(name.replace("RayWave", "Ray Wave"));
  if (name.includes("X-Fractor")) {
    candidates.push(name.replace(/X-Fractor/g, "Xfractor"));
    if (!name.includes("X-Fractor Refractor")) candidates.push(name.replace("X-Fractor", "X-Fractor Refractor"));
  }
  if (name.includes("Xfractor") && !name.includes("X-Fractor")) {
    candidates.push(name.replace(/Xfractor/g, "X-Fractor"));
    if (!name.includes("Xfractor Refractor")) candidates.push(name.replace("Xfractor", "Xfractor Refractor"));
  }
  return [...new Set(candidates)];
}

/** Resolve a PARALLEL row in one format: composite "<Subset> <Parallel>" only. */
export function lookupParallelIn(
  odds: Record<string, string | number>, subset: string, parallelName: string
): string | number | null {
  const keys = Object.keys(odds);
  for (const n of normalizeParallelNameShared(parallelName)) {
    const composed = `${subset} ${n}`;
    if (odds[composed] != null) return odds[composed];
    const found = findOddsKey(composed, keys);
    if (found && odds[found] != null) return odds[found];
  }
  return null;
}

/** Resolve a BASE row in one format: the subset's own key + legacy "<Subset> Base". */
export function lookupBaseIn(
  odds: Record<string, string | number>, subset: string
): string | number | null {
  const fk = findOddsKey(subset, Object.keys(odds));
  if (fk && odds[fk] != null) return odds[fk];
  if (odds[`${subset} Base`] != null) return odds[`${subset} Base`];
  return null;
}

/**
 * All formats as {key, odds}, ordered: the selected format first (so it is
 * "tried first"), then ODDS_FORMAT_PREFERENCE order, then any remaining formats
 * in their JSON order. Flat (non-nested) pack_odds → one "__flat__" format.
 */
export function buildOrderedFormats(packOddsJson: string | null, selectedFormatKey: string | null): OddsFormat[] {
  if (!packOddsJson) return [];
  let raw: Record<string, unknown>;
  try { raw = JSON.parse(packOddsJson); } catch { return []; }
  const firstVal = Object.values(raw)[0];
  if (firstVal === null || typeof firstVal !== "object") {
    return [{ key: "__flat__", odds: raw as Record<string, string | number> }];
  }
  const keys = Object.keys(raw);
  const sel = selectedFormatKey;
  const order = [
    ...(sel && keys.includes(sel) ? [sel] : []),
    ...ODDS_FORMAT_PREFERENCE.filter((f) => f !== sel && keys.includes(f)),
    ...keys.filter((f) => f !== sel && !ODDS_FORMAT_PREFERENCE.includes(f)),
  ];
  return order.map((k) => ({ key: k, odds: (raw[k] ?? {}) as Record<string, string | number> }));
}

/** First format (in the given order) whose odds carry this row's key. */
export function resolveOddsRow(
  ordered: OddsFormat[], subset: string, parallelName: string | null
): ResolvedOdds | null {
  for (const { key, odds } of ordered) {
    const v = parallelName ? lookupParallelIn(odds, subset, parallelName) : lookupBaseIn(odds, subset);
    if (v != null) return { value: v, formatKey: key };
  }
  return null;
}
