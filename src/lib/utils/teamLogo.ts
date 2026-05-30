function slugifyTeam(name: string): string {
  return name
    .toLowerCase()
    .replace(/\./g, "")              // strip periods (St. → st)
    .replace(/[^a-z0-9\s-]/g, "")   // strip other special chars (accents handled by normalize below)
    .trim()
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-+|-+$/g, "");
}

const SPORT_TO_LEAGUE: Record<string, string> = {
  Basketball: "nba",
  Baseball: "mlb",
  // Football: "nfl", Hockey: "nhl", etc. — add as folders are populated
};

// Vintage/historical MLB team names → modern franchise slug
const MLB_TEAM_ALIASES: Record<string, string> = {
  // Angels franchise
  "California Angels": "los-angeles-angels",
  "Anaheim Angels": "los-angeles-angels",
  "Angels": "los-angeles-angels",

  // Athletics franchise
  "Philadelphia Athletics": "oakland-athletics",
  "Kansas City Athletics": "oakland-athletics",
  "Athletics": "oakland-athletics",

  // Braves franchise
  "Boston Braves": "atlanta-braves",
  "Milwaukee Braves": "atlanta-braves",

  // Cleveland franchise
  "Cleveland Indians": "cleveland-guardians",
  "Cleveland": "cleveland-guardians",

  // Dodgers franchise
  "Brooklyn Dodgers": "los-angeles-dodgers",

  // Giants franchise (baseball — sport-scoped, no NFL collision)
  "New York Giants": "san-francisco-giants",

  // Marlins franchise
  "Florida Marlins": "miami-marlins",

  // Nationals franchise
  "Montréal Expos": "washington-nationals",
  "Montreal Expos": "washington-nationals",

  // Orioles franchise
  "St. Louis Browns": "baltimore-orioles",

  // Rays franchise
  "Tampa Bay Devil Rays": "tampa-bay-rays",

  // Astros franchise
  "Houston Colt .45s": "houston-astros",
  "Houston Colts": "houston-astros",

  // Rangers franchise
  "Washington Senators": "texas-rangers",

  // Oilers → Titans (for cards labeled Houston Oilers in football context — won't fire for baseball)
  // San Diego Chargers, Oakland Raiders, etc. handled at NFL level when added
};

/**
 * Returns the public path to a team's SVG logo, or null if no logo is available.
 * Caller should render a placeholder when null (never a broken <img>).
 */
export function getTeamLogo(teamName: string, sport: string): string | null {
  if (!teamName) return null;
  const league = SPORT_TO_LEAGUE[sport];
  if (!league) return null;

  // Check sport-specific alias map first (vintage → modern franchise)
  if (league === "mlb" && MLB_TEAM_ALIASES[teamName]) {
    return `/logos/mlb/${MLB_TEAM_ALIASES[teamName]}-logo.svg`;
  }

  const slug = slugifyTeam(teamName);
  return `/logos/${league}/${slug}-logo.svg`;
}
