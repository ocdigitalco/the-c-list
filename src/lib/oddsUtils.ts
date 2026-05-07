/**
 * Shared odds key matching utilities.
 *
 * Used by both server-side BHC slot building (page.tsx) and
 * client-side odds table rendering (AthleteDetailClient.tsx).
 */

/**
 * Find the best matching odds key for a given insert set name.
 * Tries exact match, singular/plural, suffix variations, and
 * case-insensitive fallback.
 */
export function findOddsKey(name: string, oddsKeys: string[]): string | undefined {
  const keySet = new Set(oddsKeys);
  // 1. Exact match
  if (keySet.has(name)) return name;
  // 2. Build variations
  const variations = [name];
  // Singular/plural: add/remove trailing "s"
  if (name.endsWith("s")) variations.push(name.slice(0, -1));
  else variations.push(name + "s");
  // "Autographs" → "Autograph Card", "Autograph Cards"
  if (name.endsWith(" Autographs")) {
    variations.push(name.replace(/ Autographs$/, " Autograph Card"));
    variations.push(name.replace(/ Autographs$/, " Autograph Cards"));
  }
  if (name.endsWith(" Autograph")) {
    variations.push(name.replace(/ Autograph$/, " Autograph Card"));
    variations.push(name.replace(/ Autograph$/, " Autograph Cards"));
  }
  // "Cards" ↔ "Card"
  if (name.endsWith(" Cards")) variations.push(name.replace(/ Cards$/, " Card"));
  if (name.endsWith(" Card")) variations.push(name.replace(/ Card$/, " Cards"));
  // "Sketch Cards" → "Sketch Card"
  if (name.includes(" Sketch Cards")) variations.push(name.replace(" Sketch Cards", " Sketch Card"));
  if (name.includes(" Sketch Card") && !name.includes(" Sketch Cards"))
    variations.push(name.replace(" Sketch Card", " Sketch Cards"));
  // "Base" ↔ "Base Cards"
  if (name === "Base" || name === "Base Set" || name === "Base Set Checklist") {
    variations.push("Base", "Base Cards", "Base Set", "Base Set Checklist");
  }
  if (name.startsWith("Base")) {
    variations.push("Base Cards", "Base");
  }
  // " Cards" suffix addition (e.g. "Chrome Autographs" → "Chrome Autograph Cards")
  if (!name.endsWith(" Cards") && !name.endsWith(" Card")) {
    if (name.endsWith("s")) variations.push(name.slice(0, -1) + " Cards");
    variations.push(name + " Cards");
    variations.push(name + " Card");
  }
  // Try all variations — exact first, then case-insensitive
  for (const v of variations) {
    if (keySet.has(v)) return v;
  }
  const lowerMap = new Map(oddsKeys.map((k) => [k.toLowerCase(), k]));
  for (const v of variations) {
    const found = lowerMap.get(v.toLowerCase());
    if (found) return found;
  }
  return undefined;
}

/**
 * Look up an odds value for a given insert set + optional parallel suffix
 * in a flat odds object (e.g., packOddsJson[activeFormat]).
 *
 * Combines findOddsKey matching with parallel suffix key construction.
 */
export function lookupOddsValue(
  activeOdds: Record<string, string | number>,
  insertSetName: string,
  parallelName: string | null,
): string | number | null {
  const oddsKeys = Object.keys(activeOdds);
  const base = insertSetName.trim();
  const suffix = parallelName?.trim() || null;

  if (suffix) {
    // Build composite keys: "insertSetName parallelName"
    const compositeNames = [
      `${base} ${suffix}`,
      `${base} ${suffix} Parallel`,
    ];
    // Also try with findOddsKey variations on the base name
    const baseVariations = findOddsKeyVariations(base);
    for (const bv of baseVariations) {
      compositeNames.push(`${bv} ${suffix}`);
      compositeNames.push(`${bv} ${suffix} Parallel`);
    }
    // Try each composite key
    for (const ck of compositeNames) {
      if (activeOdds[ck] != null) return activeOdds[ck];
    }
    // Case-insensitive fallback on composites
    const lowerMap = new Map(oddsKeys.map((k) => [k.toLowerCase(), k]));
    for (const ck of compositeNames) {
      const found = lowerMap.get(ck.toLowerCase());
      if (found && activeOdds[found] != null) return activeOdds[found];
    }
  }

  // Look up the base insert set name (no parallel suffix)
  const foundKey = findOddsKey(base, oddsKeys);
  if (foundKey && activeOdds[foundKey] != null) return activeOdds[foundKey];

  return null;
}

/**
 * Generate name variations for findOddsKey matching (without doing the lookup).
 * Used internally by lookupOddsValue to build composite keys.
 */
function findOddsKeyVariations(name: string): string[] {
  const variations: string[] = [];
  // Singular/plural
  if (name.endsWith("s")) variations.push(name.slice(0, -1));
  else variations.push(name + "s");
  // "Autographs" → "Autograph Card/Cards"
  if (name.endsWith(" Autographs")) {
    variations.push(name.replace(/ Autographs$/, " Autograph Card"));
    variations.push(name.replace(/ Autographs$/, " Autograph Cards"));
  }
  if (name.endsWith(" Autograph")) {
    variations.push(name.replace(/ Autograph$/, " Autograph Card"));
    variations.push(name.replace(/ Autograph$/, " Autograph Cards"));
  }
  // "Cards" ↔ "Card"
  if (name.endsWith(" Cards")) variations.push(name.replace(/ Cards$/, " Card"));
  if (name.endsWith(" Card")) variations.push(name.replace(/ Card$/, " Cards"));
  // " Cards" suffix
  if (!name.endsWith(" Cards") && !name.endsWith(" Card")) {
    if (name.endsWith("s")) variations.push(name.slice(0, -1) + " Cards");
    variations.push(name + " Cards");
    variations.push(name + " Card");
  }
  return variations;
}
