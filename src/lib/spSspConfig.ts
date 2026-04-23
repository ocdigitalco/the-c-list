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
      "Shadow Etch",
    ],
    ssp: [
      "Helix",
      "Game Genies",
      "Kaiju",
      "Let's Go",
      "Ultra Violet",
      "Lightning Leaders",
      "Fanatical",
    ],
  },

  "2025 Topps Chrome Formula 1": {
    sp: [
      "The Grail",
      "Vegas At Night",
      "The Grid",
    ],
    ssp: [],
  },

  "2025 Topps Chrome UFC": {
    sp: [
      "Hidden Gems",
      "Spitting Venom",
    ],
    ssp: [],
  },

  "2025 Topps Pristine Baseball": {
    sp: [
      "Prowlers",
      "Pearlescent",
      "Amped",
      "Monogram",
    ],
    ssp: [
      "Let's Go",
    ],
  },

  "2025-26 Topps Cosmic Chrome Basketball": {
    sp: [
      "Cosmic Dust",
      "Geocentric",
      "First Light",
      "Re Entry",
      "Starfractor",
    ],
    ssp: [],
  },

  "2025-26 Topps Hoops Basketball": {
    sp: [
      "Dunkumentory",
      "Jam-Packed",
      "Next Episode",
      "Pay Attention",
      "Hoopers",
      "Bounce House",
      "Hardwired",
      "The Buzz",
      "Net to Net",
    ],
    ssp: [
      "Hoops Rookie/Veteran Duals",
      "Joy",
      "Boombastic",
      "Hoops Rookie Duals",
      "Block by Block",
      "Hoops Rookie Triples",
      "Oasis",
      "Checkmate",
      "Hoopnotic",
    ],
  },

  "2025-26 Topps Midnight Basketball": {
    sp: [
      "Twilight",
    ],
    ssp: [],
  },

  "2025-26 Topps UEFA Club Competitions": {
    sp: [
      "Murals",
      "Mindgame",
    ],
    ssp: [
      "Jigsaw",
    ],
  },

  "2024 Topps Chrome U.S. Olympic & Paralympic Team Hopefuls": {
    sp: [
      "Chasing the Rings",
      "Athlete Nouveau",
    ],
    ssp: [
      "Exposé",
    ],
  },

  "2025 Topps Midnight UFC": {
    sp: [
      "Greetings From",
      "Night Vision",
    ],
    ssp: [
      "Twilight",
      "Dream Chasers",
    ],
  },

  "2025-26 Bowman Basketball": {
    sp: [],
    ssp: [
      "Crystallized NBA",
      "Crystallized NIL",
      "Anime NBA",
      "Anime NIL",
      "Bowman Spotlights NBA",
      "Bowman Spotlights NIL",
    ],
  },
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

  // Exact match
  if (SP_SSP_CONFIG[setName]) return SP_SSP_CONFIG[setName];

  // Strict partial match — return the longest (most specific) matching key
  const matches = Object.keys(SP_SSP_CONFIG).filter(
    (key) => setName.includes(key) || key.includes(setName)
  );
  if (matches.length === 0) return null;

  const bestMatch = matches.sort((a, b) => b.length - a.length)[0];
  return SP_SSP_CONFIG[bestMatch];
}
