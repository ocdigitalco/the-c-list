import { db, rawQuery } from "@/lib/db";
import { sets, players, playerAppearances } from "@/lib/schema";
import { eq, sql } from "drizzle-orm";
import Link from "next/link";
import { PageShell } from "@/components/PageShell";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faBaseball,
  faBasketball,
  faFootball,
  faFutbol,
  faHockeyPuck,
  faGolfBallTee,
  faMedal,
  faHandFist,
  faFlagCheckered,
  faStar,
  faGrip,
} from "@fortawesome/free-solid-svg-icons";
import { ChecklistSearch } from "./ChecklistSearch";

export const dynamic = "force-dynamic";

interface SearchParams {
  sport?: string;
}

function SportIcon({ sport }: { sport: string }) {
  switch (sport.toLowerCase()) {
    case "baseball":
      return <FontAwesomeIcon icon={faBaseball} className="w-8 h-8" />;
    case "basketball":
      return <FontAwesomeIcon icon={faBasketball} className="w-8 h-8" />;
    case "football":
      return <FontAwesomeIcon icon={faFootball} className="w-8 h-8" />;
    case "soccer":
      return <FontAwesomeIcon icon={faFutbol} className="w-8 h-8" />;
    case "hockey":
      return <FontAwesomeIcon icon={faHockeyPuck} className="w-8 h-8" />;
    case "golf":
      return <FontAwesomeIcon icon={faGolfBallTee} className="w-8 h-8" />;
    case "olympics":
      return <FontAwesomeIcon icon={faMedal} className="w-8 h-8" />;
    case "mma":
      return <FontAwesomeIcon icon={faHandFist} className="w-8 h-8" />;
    case "racing":
      return <FontAwesomeIcon icon={faFlagCheckered} className="w-8 h-8" />;
    case "wrestling":
      return <FontAwesomeIcon icon={faHandFist} className="w-8 h-8" />;
    case "entertainment":
      return <FontAwesomeIcon icon={faStar} className="w-8 h-8" />;
    default:
      return <FontAwesomeIcon icon={faStar} className="w-8 h-8" />;
  }
}

export default async function ChecklistsPage({
  searchParams,
}: {
  searchParams: Promise<SearchParams>;
}) {
  const { sport: sportParam } = await searchParams;
  const activeSport = sportParam ?? null;

  const sportRows = await db
    .selectDistinct({ sport: sets.sport })
    .from(sets)
    .orderBy(sets.sport);
  const allSports = sportRows.map((r) => r.sport);

  const setRows = await db
    .select()
    .from(sets)
    .where(activeSport ? eq(sets.sport, activeSport) : undefined)
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
        {/* Sport tiles */}
        <section>
          <div className="flex flex-wrap gap-3">
            <Link
              href="/checklists?sport="
              className={`flex flex-col items-center gap-2.5 px-6 py-5 rounded-2xl border transition-colors min-w-[7rem] ${
                activeSport === null
                  ? "border-amber-500/60 bg-amber-500/10 text-amber-400"
                  : "border-zinc-800 bg-zinc-900 text-zinc-400 hover:border-zinc-600 hover:text-zinc-200"
              }`}
            >
              <FontAwesomeIcon icon={faGrip} className="w-8 h-8" />
              <span className="text-sm font-semibold">All</span>
            </Link>

            {allSports.map((sport) => (
              <Link
                key={sport}
                href={`/checklists?sport=${encodeURIComponent(sport)}`}
                className={`flex flex-col items-center gap-2.5 px-6 py-5 rounded-2xl border transition-colors min-w-[7rem] ${
                  activeSport === sport
                    ? "border-amber-500/60 bg-amber-500/10 text-amber-400"
                    : "border-zinc-800 bg-zinc-900 text-zinc-400 hover:border-zinc-600 hover:text-zinc-200"
                }`}
              >
                <SportIcon sport={sport} />
                <span className="text-sm font-semibold">{sport}</span>
              </Link>
            ))}
          </div>
        </section>

        {/* Search + Set cards */}
        <ChecklistSearch sets={setCards} activeSport={activeSport} />
    </PageShell>
  );
}
