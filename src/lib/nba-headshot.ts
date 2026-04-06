export function getNBAHeadshotUrl(nbaPlayerId: number | null | undefined): string | null {
  if (!nbaPlayerId) return null;
  return `https://cdn.nba.com/headshots/nba/latest/1040x760/${nbaPlayerId}.png`;
}

export const NBA_HEADSHOT_FALLBACK = null; // show initials avatar if no headshot
