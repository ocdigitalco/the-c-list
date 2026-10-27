/**
 * Single source of truth for athlete/player headshot URLs. Self-contained (no
 * imports) so build scripts can use it too. The per-source helpers are the same
 * URL patterns the app has always used; `resolveHeadshot` is the precedence
 * chain that was previously duplicated inline across the set-page components.
 *
 * Precedence: NBA → UFC → MLB → generic image_url (Sleeper NFL / Wikia).
 */

export function getNBAHeadshotUrl(nbaPlayerId: number | null | undefined): string | null {
  if (!nbaPlayerId) return null;
  return `https://cdn.nba.com/headshots/nba/latest/1040x760/${nbaPlayerId}.png`;
}

export function getMLBHeadshotUrl(mlbPlayerId: number | null | undefined): string | null {
  if (!mlbPlayerId) return null;
  return `https://midfield.mlbstatic.com/v1/people/${mlbPlayerId}/spots/120`;
}

export function getUFCHeadshotUrl(ufcImageUrl: string | null | undefined): string | null {
  if (!ufcImageUrl) return null;
  return ufcImageUrl;
}

export interface HeadshotInputs {
  nbaPlayerId?: number | null;
  ufcImageUrl?: string | null;
  mlbPlayerId?: number | null;
  imageUrl?: string | null;
}

/** First non-null headshot URL by source precedence, or null for no source. */
export function resolveHeadshot(p: HeadshotInputs): string | null {
  return (
    getNBAHeadshotUrl(p.nbaPlayerId) ??
    getUFCHeadshotUrl(p.ufcImageUrl) ??
    getMLBHeadshotUrl(p.mlbPlayerId) ??
    (p.imageUrl || null)
  );
}
