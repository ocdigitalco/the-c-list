import { rawQuery } from "@/lib/db";
import { SearchesClient } from "./SearchesClient";

export const revalidate = 300; // 5 minutes

const VALID_RANGES = ["24h", "7d", "30d", "1y", "all"] as const;
type Range = (typeof VALID_RANGES)[number];

function cutoffMs(range: Range): number {
  const now = Date.now();
  switch (range) {
    case "24h": return now - 24 * 60 * 60 * 1000;
    case "7d":  return now - 7 * 24 * 60 * 60 * 1000;
    case "30d": return now - 30 * 24 * 60 * 60 * 1000;
    case "1y":  return now - 365 * 24 * 60 * 60 * 1000;
    case "all": return 0;
  }
}

export interface LeaderboardEntry {
  playerName: string;
  sport: string;
  setName: string;
  eventCount: number;
  nbaPlayerId: number | null;
  ufcImageUrl: string | null;
  mlbPlayerId: number | null;
  imageUrl: string | null;
  slug: string | null;
  setSlug: string | null;
}

async function queryLeaderboard(
  eventType: "search" | "view",
  cutoff: number,
  sport: string | null,
): Promise<LeaderboardEntry[]> {
  const sportClause = sport ? "AND s.sport = ?" : "";
  const args: (string | number)[] = sport
    ? [eventType, cutoff, sport]
    : [eventType, cutoff];

  const rows = await rawQuery.all<{
    player_name: string;
    sport: string;
    set_name: string;
    event_count: number;
    nba_player_id: number | null;
    ufc_image_url: string | null;
    mlb_player_id: number | null;
    image_url: string | null;
    slug: string | null;
    set_slug: string | null;
  }>(
    `SELECT
      p.name AS player_name,
      s.sport,
      s.name AS set_name,
      COUNT(DISTINCT pe.created_at / 1000) AS event_count,
      p.nba_player_id,
      p.ufc_image_url,
      p.mlb_player_id,
      p.image_url,
      p.slug,
      s.slug AS set_slug
    FROM player_events pe
    JOIN players p ON pe.player_id = p.id
    JOIN sets s ON p.set_id = s.id
    WHERE pe.event_type = ? AND pe.created_at >= ? ${sportClause}
    GROUP BY p.name
    ORDER BY event_count DESC
    LIMIT 20`,
    ...args,
  );

  return rows.map((r) => ({
    playerName: r.player_name,
    sport: r.sport,
    setName: r.set_name,
    eventCount: r.event_count,
    nbaPlayerId: r.nba_player_id,
    ufcImageUrl: r.ufc_image_url,
    mlbPlayerId: r.mlb_player_id,
    imageUrl: r.image_url,
    slug: r.slug,
    setSlug: r.set_slug,
  }));
}

async function queryAllSports(): Promise<string[]> {
  const rows = await rawQuery.all<{ sport: string }>(
    "SELECT DISTINCT sport FROM sets ORDER BY sport",
  );
  return rows.map((r) => r.sport);
}

export default async function SearchesPage({
  searchParams,
}: {
  searchParams: Promise<{ range?: string; sport?: string }>;
}) {
  const { range: rangeParam, sport: sportParam } = await searchParams;
  const range: Range = VALID_RANGES.includes(rangeParam as Range)
    ? (rangeParam as Range)
    : "7d";

  const allSports = await queryAllSports();
  const sport =
    sportParam && allSports.includes(sportParam) ? sportParam : null;

  const cutoff = cutoffMs(range);
  const views = await queryLeaderboard("view", cutoff, sport);
  const searches = await queryLeaderboard("search", cutoff, sport);

  return (
    <SearchesClient
      views={views}
      searches={searches}
      allSports={allSports}
      currentRange={range}
      currentSport={sport}
    />
  );
}
