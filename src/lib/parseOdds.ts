/**
 * Canonical odds parsing utility.
 *
 * All pack odds parsing across the codebase should use these functions
 * to ensure consistent handling of all formats.
 */

/**
 * Parse a pack odds value (string or number) into a denominator.
 *
 * The denominator represents "1 in X packs" for standard odds.
 * For odds like "3:1" (3 cards per pack), returns a fractional denominator (1/3).
 *
 * Handles:
 *   "1:26"    → 26     (1 card every 26 packs)
 *   "1:1"     → 1      (1 card every pack)
 *   "3:1"     → 0.333  (3 cards per pack → denominator = 1/3)
 *   "2:7"     → 3.5    (2 cards every 7 packs → denominator = 7/2)
 *   "1:1,441" → 1441   (handle commas)
 *   64        → 64     (raw number = 1:64)
 *
 * Returns null if the value cannot be parsed.
 */
export function parseOddsToDenom(v: unknown): number | null {
  if (typeof v === "number") {
    if (v > 0 && isFinite(v)) return v;
    return null;
  }
  if (typeof v === "string") {
    const cleaned = v.replace(/\s/g, "").replace(/,/g, "");
    if (cleaned.includes(":")) {
      const parts = cleaned.split(":");
      if (parts.length !== 2) return null;
      const numerator = parseFloat(parts[0]);
      const denominator = parseFloat(parts[1]);
      if (
        isNaN(numerator) || isNaN(denominator) ||
        !isFinite(numerator) || !isFinite(denominator) ||
        numerator === 0
      ) return null;
      // "1:26" → denom = 26/1 = 26
      // "3:1"  → denom = 1/3 = 0.333
      // "2:7"  → denom = 7/2 = 3.5
      return denominator / numerator;
    }
    const n = parseFloat(cleaned);
    if (!isNaN(n) && n > 0 && isFinite(n)) return n;
  }
  return null;
}

/**
 * Normalize an odds object (from JSON) into a Record<string, number>
 * where each value is the denominator (packs per card).
 *
 * Skips entries that cannot be parsed.
 */
export function normalizeOddsObj(
  obj: Record<string, unknown>
): Record<string, number> {
  const out: Record<string, number> = {};
  for (const [k, v] of Object.entries(obj)) {
    const denom = parseOddsToDenom(v);
    if (denom !== null) out[k] = denom;
  }
  return out;
}
