function slugifyTeam(name: string): string {
  return name
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .replace(/-+/g, "-");
}

function leagueFolder(sport: string): string | null {
  const map: Record<string, string> = {
    Basketball: "nba",
    // Football: "nfl", Baseball: "mlb", etc. — add as folders are populated
  };
  return map[sport] ?? null;
}

/**
 * Returns the public path to a team's SVG logo, or null if no logo is available.
 * Caller should render a placeholder when null (never a broken <img>).
 */
export function getTeamLogo(teamName: string, sport: string): string | null {
  if (!teamName) return null;
  const league = leagueFolder(sport);
  if (!league) return null;
  const slug = slugifyTeam(teamName);
  return `/logos/${league}/${slug}-logo.svg`;
}
