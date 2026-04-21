/**
 * SP/SSP Classification Config
 *
 * Defines which insert sets are classified as Short Print (SP) or
 * Super Short Print (SSP) for each set in the system.
 *
 * Insert set names must match the database exactly.
 */

export interface SpSspSetConfig {
  sp: string[];   // Short Print insert set names (exact DB names)
  ssp: string[];  // Super Short Print insert set names (exact DB names)
}

export const SP_SSP_CONFIG: Record<string, SpSspSetConfig> = {
  "2025 Topps Chrome Football": {
    sp: [
      "Base - Image Variation",
      "Base - Rookies Image Variation",
      "Base - Team Camo Variation",
      "Base - Lightboard Logo Variation",
      "Base - Chrome Base Etch Variation",
      "Base - Chrome Rookies Etch Variation",
    ],
    ssp: [
      "Helix",
      "Game Genies",
      "Kaiju",
      "Let's Go",
      "Ultra Violet",
      "Lightning Leaders",
      "Fanatical",
      "Shadow Etch",
    ],
  },
  // Additional sets added here after review
};

/**
 * Sets excluded from SP/SSP classification entirely.
 * Entertainment, non-sport, and sets without traditional parallel structures.
 */
export const SP_SSP_EXCLUDED_SET_KEYWORDS = [
  "Disney",
  "Disneyland",
  "Muppets",
  "Phineas",
  "Goofy Movie",
  "WWE",
  "Deadpool",
  "Marvel",
];

/**
 * Returns the SP/SSP config for a given set name, or null if
 * the set is excluded or has no config defined.
 */
export function getSpSspConfig(setName: string): SpSspSetConfig | null {
  const isExcluded = SP_SSP_EXCLUDED_SET_KEYWORDS.some((keyword) =>
    setName.toLowerCase().includes(keyword.toLowerCase())
  );
  if (isExcluded) return null;

  if (SP_SSP_CONFIG[setName]) return SP_SSP_CONFIG[setName];

  const partialMatch = Object.keys(SP_SSP_CONFIG).find(
    (key) => setName.includes(key) || key.includes(setName)
  );
  if (partialMatch) return SP_SSP_CONFIG[partialMatch];

  return null;
}
