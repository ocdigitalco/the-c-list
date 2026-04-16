import { db, rawQuery } from "@/lib/db";
import { sets, players, playerAppearances } from "@/lib/schema";
import { eq, sql } from "drizzle-orm";
import { PageShell } from "@/components/PageShell";
import { ChecklistSearch } from "./ChecklistSearch";

export const dynamic = "force-dynamic";

export default async function ChecklistsPage() {
  const sportRows = await db
    .selectDistinct({ sport: sets.sport })
    .from(sets)
    .orderBy(sets.sport);
  const allSports = sportRows.map((r) => r.sport);

  const setRows = await db
    .select()
    .from(sets)
    .orderBy(
      sql`CASE WHEN ${sets.releaseDate} IS NULL THEN 1 ELSE 0 END`,
      sql`${sets.releaseDate} DESC`,
      sets.name
    );

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

  // Fetch slugs via rawQuery (slug column not in Drizzle schema)
  let slugMap = new Map<number, string>();
  try {
    const slugRows = await rawQuery.all<{ id: number; slug: string }>(
      "SELECT id, slug FROM sets WHERE slug IS NOT NULL"
    );
    slugMap = new Map(slugRows.map((r) => [r.id, r.slug]));
  } catch { /* slug column may not exist yet */ }

  const setCards = setRows.map((s) => ({
    ...s,
    slug: slugMap.get(s.id) ?? null,
    athleteCount: statsMap.get(s.id)?.athleteCount ?? 0,
    cardCount: statsMap.get(s.id)?.cardCount ?? 0,
  }));

  return (
    <PageShell
      breadcrumb={{ label: "Home", href: "/checklists" }}
      title="Checklists"
      description="Browse all sports card sets in the app"
    >
        <ChecklistSearch sets={setCards} allSports={allSports} />
    </PageShell>
  );
}
