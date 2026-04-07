export function getMLBHeadshotUrl(mlbPlayerId: number | null | undefined): string | null {
  if (!mlbPlayerId) return null;
  return `https://midfield.mlbstatic.com/v1/people/${mlbPlayerId}/spots/120`;
}
