import { db, rawQuery } from "@/lib/db";
import { sets, players, playerAppearances } from "@/lib/schema";
import { eq, sql } from "drizzle-orm";
import Link from "next/link";
import { PageShell } from "@/components/PageShell";
import { CardThumbnail } from "@/components/CardThumbnail";
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

export const dynamic = "force-dynamic";

interface SearchParams {
  sport?: string;
}

type Tier = "Standard" | "Chrome" | "Sapphire" | "Premium" | "Prizm" | "Standard / Chrome";

function TierBadge({ tier }: { tier: Tier }) {
  if (tier === "Prizm") {
    return (
      <span className="shrink-0 text-xs font-semibold px-2 py-0.5 rounded bg-gradient-to-r from-violet-600 via-fuchsia-500 to-pink-500 text-white">
        Prizm
      </span>
    );
  }
  if (tier === "Premium") {
    return (
      <span className="shrink-0 text-xs font-semibold px-2 py-0.5 rounded bg-amber-950 text-amber-300 border border-amber-700/60">
        Premium
      </span>
    );
  }
  if (tier === "Sapphire") {
    return (
      <span className="shrink-0 text-xs font-semibold px-2 py-0.5 rounded bg-blue-950 text-blue-300 border border-blue-700/60">
        Sapphire
      </span>
    );
  }
  if (tier === "Chrome") {
    return (
      <span className="shrink-0 text-xs font-semibold px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-600/50">
        Chrome
      </span>
    );
  }
  if (tier === "Standard / Chrome") {
    return (
      <span className="shrink-0 text-xs font-semibold px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-600/50">
        Standard / Chrome
      </span>
    );
  }
  return null;
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

  const showSets = sportParam !== undefined;

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
                showSets && activeSport === null
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

        {/* Set cards */}
        {setCards.length > 0 && (
          <section>
            <h2 className="text-xs font-semibold text-zinc-500 uppercase tracking-widest mb-4">
              {activeSport ? `${activeSport} Sets` : "All Sets"}{" "}
              <span className="normal-case font-normal text-zinc-700">
                · {setCards.length} set{setCards.length !== 1 ? "s" : ""}
              </span>
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {setCards.map((s) => (
                <Link
                  key={s.id}
                  href={`/sets/${s.slug ?? s.id}`}
                  className="group border border-zinc-800 bg-zinc-900 hover:border-zinc-600 hover:bg-zinc-800/60 transition-colors flex overflow-hidden"
                >
                  {s.sampleImageUrl && (
                    <div className="shrink-0 w-20 sm:w-24 self-stretch">
                      <CardThumbnail src={s.sampleImageUrl} alt={s.name} />
                    </div>
                  )}

                  <div className="flex-1 min-w-0 p-4 flex flex-col justify-between gap-3">
                    <p className="font-semibold text-white text-sm leading-snug group-hover:text-amber-400 transition-colors">
                      {s.name}
                    </p>

                    <div className="flex items-center gap-1.5 flex-wrap">
                      <span className="text-xs font-medium text-zinc-400 bg-zinc-800 border border-zinc-700 px-2 py-0.5 rounded">
                        {s.league ?? s.sport}
                      </span>
                      <TierBadge tier={s.tier as Tier} />
                    </div>

                    <div className="flex items-center gap-3 text-xs text-zinc-500">
                      <span>
                        <span className="font-semibold text-zinc-300">{s.athleteCount.toLocaleString()}</span> athletes
                      </span>
                      <span className="text-zinc-700">·</span>
                      <span>
                        <span className="font-semibold text-zinc-300">{s.cardCount.toLocaleString()}</span> cards
                      </span>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </section>
        )}

        {showSets && setCards.length === 0 && (
          <div className="text-center py-16">
            <p className="text-zinc-500">No sets found for {activeSport}.</p>
          </div>
        )}

        {!showSets && allSports.length === 0 && (
          <div className="text-center py-16">
            <p className="text-zinc-500">No sets in the database yet.</p>
          </div>
        )}
    </PageShell>
  );
}
