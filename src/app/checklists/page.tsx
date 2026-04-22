import { db, rawQuery } from "@/lib/db";
import { sets, players, playerAppearances } from "@/lib/schema";
import { eq, sql } from "drizzle-orm";
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

  let slugMap = new Map<number, string>();
  try {
    const slugRows = await rawQuery.all<{ id: number; slug: string }>(
      "SELECT id, slug FROM sets WHERE slug IS NOT NULL"
    );
    slugMap = new Map(slugRows.map((r) => [r.id, r.slug]));
  } catch { /* slug column may not exist yet */ }

  // Determine "recently added" — sets with release_date in last 30 days or added recently
  const now = new Date();
  const thirtyDaysAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);

  const setCards = setRows.map((s) => {
    const rd = s.releaseDate ? new Date(s.releaseDate) : null;
    const isRecent = rd && rd >= thirtyDaysAgo && rd <= new Date(now.getTime() + 90 * 24 * 60 * 60 * 1000);
    return {
      ...s,
      slug: slugMap.get(s.id) ?? null,
      athleteCount: statsMap.get(s.id)?.athleteCount ?? 0,
      cardCount: statsMap.get(s.id)?.cardCount ?? 0,
      featured: !!isRecent,
    };
  });

  return (
    <div
      className="h-full overflow-y-auto"
      style={{ background: "var(--cl-bg-page)" }}
    >
      <div
        className="mx-auto cl-container"
        style={{ maxWidth: 1440, padding: "40px 56px 80px" }}
      >
        {/* Breadcrumb */}
        <a
          href="/"
          style={{
            fontSize: 13,
            color: "var(--cl-text-tertiary)",
            textDecoration: "none",
            fontFamily: "var(--cl-font-display)",
          }}
        >
          &lsaquo; Home
        </a>

        {/* Title */}
        <h1
          className="cl-title"
          style={{
            fontFamily: "var(--cl-font-display)",
            fontSize: 48,
            fontWeight: 600,
            letterSpacing: "-1.2px",
            color: "var(--cl-text-primary)",
            margin: "12px 0 0",
            lineHeight: 1.1,
          }}
        >
          Checklists
        </h1>

        {/* Subtitle */}
        <p
          style={{
            fontSize: 14,
            color: "var(--cl-text-tertiary)",
            margin: "6px 0 0",
          }}
        >
          Browse all sports card sets in the app
        </p>

        <ChecklistSearch sets={setCards} allSports={allSports} />
      </div>
    </div>
  );
}
