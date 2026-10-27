/**
 * Shared helpers for the canonical athlete pages (Stage 2).
 *
 * Route ↔ page_kind mapping (set in Stage 1's build-athletes.ts):
 *   player    → /athletes/<slug>
 *   character → /characters/<slug>
 *   person    → /people/<slug>
 *   team      → /teams/<slug>
 *   none      → no page (events, "Team Card"); excluded from indexes + sitemap.
 */

export type PageKind = "player" | "character" | "person" | "team" | "none";

const KIND_TO_SEGMENT: Record<PageKind, string | null> = {
  player: "athletes",
  character: "characters",
  person: "people",
  team: "teams",
  none: null,
};

const SEGMENT_TO_KIND: Record<string, PageKind> = {
  athletes: "player",
  characters: "character",
  people: "person",
  teams: "team",
};

/** URL for an athlete given its canonical page_kind + slug, or null for `none`. */
export function athleteHref(pageKind: string, slug: string): string | null {
  const seg = KIND_TO_SEGMENT[pageKind as PageKind];
  return seg ? `/${seg}/${slug}` : null;
}

/** The page_kind a given route segment serves (e.g. "characters" → "character"). */
export function segmentToPageKind(segment: string): PageKind | null {
  return SEGMENT_TO_KIND[segment] ?? null;
}

/** First + last initial, diacritics stripped, uppercased (monogram tile). */
export function initials(name: string): string {
  const words = name
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .split(/\s+/)
    .filter(Boolean);
  if (words.length === 0) return "?";
  if (words.length === 1) return words[0].slice(0, 2).toUpperCase();
  return (words[0][0] + words[words.length - 1][0]).toUpperCase();
}

// Sport → hue (OKLCH). Mirrors the index design's palette; any unmapped sport
// (incl. Entertainment) falls back to a neutral ink tint.
const SPORT_HUE: Record<string, number> = {
  Baseball: 25,
  Basketball: 55,
  Football: 145,
  Soccer: 250,
  Tennis: 110,
  Hockey: 220,
  MMA: 0,
  Racing: 300,
  Wrestling: 330,
  Golf: 150,
  Olympics: 200,
};

/** Sport-tinted background for the monogram tile (deep, white ink reads on it). */
export function sportTint(sport: string | null | undefined): string {
  const hue = sport ? SPORT_HUE[sport] : undefined;
  if (hue === undefined) return "#1d1c1a"; // Entertainment / Other → near-ink
  return `oklch(0.42 0.11 ${hue})`;
}

/** The label the page uses for the subject's cards ("His cards" has no place with
 * mixed/unknown gender or non-players, so we stay neutral everywhere). */
export function cardsLabel(): string {
  return "Cards";
}

/** Rookie chip rule: rookie_year within the last 2 years of `now`. */
export function isRecentRookie(rookieYear: number | null | undefined, now = new Date()): boolean {
  if (!rookieYear) return false;
  return rookieYear >= now.getUTCFullYear() - 2;
}
