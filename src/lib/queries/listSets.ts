import { db, rawQuery } from "@/lib/db";
import { sets, players, playerAppearances } from "@/lib/schema";
import { eq, sql } from "drizzle-orm";

const FIVE_DAYS_MS = 5 * 24 * 60 * 60 * 1000;

export interface SetListItem {
  id: number;
  name: string;
  sport: string;
  season: string;
  league: string | null;
  tier: string;
  sampleImageUrl: string | null;
  packOdds: string | null;
  boxConfig: string | null;
  releaseDate: string | null;
  createdAt: string | null;
  slug: string | null;
  athleteCount: number;
  cardCount: number;
  featured: boolean;
}

export async function listSets(): Promise<{
  sets: SetListItem[];
  allSports: string[];
}> {
  // Hidden sets
  let hiddenIds = new Set<number>();
  try {
    const hidden = await rawQuery.all<{ id: number }>("SELECT id FROM sets WHERE is_visible = 0");
    hiddenIds = new Set(hidden.map((r) => r.id));
  } catch { /* is_visible column may not exist yet */ }

  // All sports
  const sportRows = await db
    .selectDistinct({ sport: sets.sport })
    .from(sets)
    .orderBy(sets.sport);
  const allSports = sportRows.map((r) => r.sport);

  // All sets ordered by release date
  const allSetRows = await db
    .select()
    .from(sets)
    .orderBy(
      sql`COALESCE(${sets.releaseDate}, created_at) DESC`,
      sets.name
    );
  const setRows = allSetRows.filter((s) => !hiddenIds.has(s.id));

  // Stats: athlete count + card count per set
  const statsRows = await db
    .select({
      setId: players.setId,
      athleteCount: sql<number>`cast(count(distinct ${players.id}) as integer)`,
      cardCount: sql<number>`cast(count(${playerAppearances.id}) as integer)`,
    })
    .from(players)
    .leftJoin(playerAppearances, eq(playerAppearances.playerId, players.id))
    .groupBy(players.setId);
  const statsMap = new Map(statsRows.map((r) => [r.setId, r]));

  // Slugs
  let slugMap = new Map<number, string>();
  try {
    const slugRows = await rawQuery.all<{ id: number; slug: string }>(
      "SELECT id, slug FROM sets WHERE slug IS NOT NULL"
    );
    slugMap = new Map(slugRows.map((r) => [r.id, r.slug]));
  } catch { /* slug column may not exist yet */ }

  // created_at for "recently added" badge
  let createdAtMap = new Map<number, string>();
  try {
    const caRows = await rawQuery.all<{ id: number; created_at: string }>(
      "SELECT id, created_at FROM sets WHERE created_at IS NOT NULL"
    );
    createdAtMap = new Map(caRows.map((r) => [r.id, r.created_at]));
  } catch { /* created_at column may not exist yet */ }

  const now = Date.now();
  const fiveDaysAgo = now - FIVE_DAYS_MS;

  const setCards: SetListItem[] = setRows.map((s) => {
    const createdAt = createdAtMap.get(s.id);
    const createdMs = createdAt ? new Date(createdAt).getTime() : 0;
    const isRecent = createdMs > fiveDaysAgo;

    return {
      ...s,
      createdAt: createdAt ?? null,
      slug: slugMap.get(s.id) ?? null,
      athleteCount: statsMap.get(s.id)?.athleteCount ?? 0,
      cardCount: statsMap.get(s.id)?.cardCount ?? 0,
      featured: isRecent,
    };
  });

  return { sets: setCards, allSports };
}
