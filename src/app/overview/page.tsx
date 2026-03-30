import { rawQuery } from "@/lib/db";
import { SportFilter } from "@/components/SportFilter";
import { PageShell } from "@/components/PageShell";

export const dynamic = "force-dynamic";

const AUTO_FILTER = `(
  LOWER(i.name) LIKE '%auto%'
  OR LOWER(i.name) LIKE '%signature%'
  OR LOWER(i.name) LIKE '%signed%'
  OR LOWER(i.name) LIKE '%autograph%'
)`;

async function queryStats(sport: string | null) {
  const sportJoin = "JOIN sets s ON i.set_id = s.id";
  const sportWhere = sport ? "AND s.sport = ?" : "";
  type Arg = string | number | null;
  const arg = (base: Arg[]) => (sport ? [...base, sport] : base);

  const n = async (sql: string, ...args: Arg[]) =>
    ((await rawQuery.get<{ n: number }>(sql, ...args))?.n ?? 0);

  const totalSets = sport
    ? await n(`SELECT COUNT(*) AS n FROM sets WHERE sport = ?`, sport)
    : await n(`SELECT COUNT(*) AS n FROM sets`);

  const totalPlayers = await n(
    `SELECT COUNT(DISTINCT p.id) AS n
     FROM players p
     JOIN sets s ON p.set_id = s.id
     ${sport ? "WHERE s.sport = ?" : ""}`,
    ...sport ? [sport] : []
  );

  const totalCards = await n(
    `SELECT COUNT(*) AS n
     FROM player_appearances pa
     JOIN insert_sets i ON pa.insert_set_id = i.id
     ${sportJoin}
     ${sport ? "WHERE s.sport = ?" : ""}`,
    ...sport ? [sport] : []
  );

  const totalInsertSets = await n(
    `SELECT COUNT(*) AS n
     FROM insert_sets i
     ${sportJoin}
     ${sport ? "WHERE s.sport = ?" : ""}`,
    ...sport ? [sport] : []
  );

  const totalAutographs = await n(
    `SELECT COUNT(*) AS n
     FROM player_appearances pa
     JOIN insert_sets i ON pa.insert_set_id = i.id
     ${sportJoin}
     WHERE ${AUTO_FILTER} ${sportWhere}`,
    ...arg([])
  );

  const totalParallelTypes = await n(
    `SELECT COUNT(DISTINCT p.name) AS n
     FROM parallels p
     JOIN insert_sets i ON p.insert_set_id = i.id
     ${sportJoin}
     ${sport ? "WHERE s.sport = ?" : ""}`,
    ...sport ? [sport] : []
  );

  const totalParallels = await n(
    `SELECT COALESCE(SUM(apps * pars), 0) AS n
     FROM (
       SELECT
         (SELECT COUNT(*) FROM player_appearances WHERE insert_set_id = i.id) AS apps,
         (SELECT COUNT(*) FROM parallels           WHERE insert_set_id = i.id) AS pars
       FROM insert_sets i
       ${sportJoin}
       ${sport ? "WHERE s.sport = ?" : ""}
     )`,
    ...sport ? [sport] : []
  );

  const totalAutoParallels = await n(
    `SELECT COALESCE(SUM(apps * pars), 0) AS n
     FROM (
       SELECT
         (SELECT COUNT(*) FROM player_appearances WHERE insert_set_id = i.id) AS apps,
         (SELECT COUNT(*) FROM parallels           WHERE insert_set_id = i.id) AS pars
       FROM insert_sets i
       ${sportJoin}
       WHERE ${AUTO_FILTER} ${sportWhere}
     )`,
    ...arg([])
  );

  const totalOneOfOnes = await n(
    `SELECT COUNT(*) AS n
     FROM parallels p
     JOIN insert_sets i ON p.insert_set_id = i.id
     ${sportJoin}
     WHERE p.print_run = 1 ${sportWhere}`,
    ...arg([])
  );

  return {
    totalSets,
    totalPlayers,
    totalCards,
    totalInsertSets,
    totalAutographs,
    totalParallelTypes,
    totalParallels,
    totalAutoParallels,
    totalOneOfOnes,
  };
}

async function queryAllSports(): Promise<string[]> {
  const rows = await rawQuery.all<{ sport: string }>(
    `SELECT DISTINCT sport FROM sets ORDER BY sport`
  );
  return rows.map((r) => r.sport);
}

export default async function OverviewPage({
  searchParams,
}: {
  searchParams: Promise<{ sport?: string }>;
}) {
  const { sport: sportParam } = await searchParams;
  const allSports = await queryAllSports();
  const sport = sportParam && allSports.includes(sportParam) ? sportParam : null;

  const stats = await queryStats(sport);

  return (
    <PageShell
      breadcrumb={{ label: "Home", href: "/checklists" }}
      title="Overview"
      description="Stats and insights across all sets in the app"
    >
        {/* Sport filter */}
        <SportFilter sports={allSports} current={sport} path="/overview" />

        {/* Stat grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <StatCard label="Total Sets" value={stats.totalSets} />
          <StatCard label="Total Athletes" value={stats.totalPlayers} />
          <StatCard label="Unique Cards" value={stats.totalCards} />
          <StatCard label="Insert Sets" value={stats.totalInsertSets} />
          <StatCard label="Autographs" value={stats.totalAutographs} />
          <StatCard label="Parallel Types" value={stats.totalParallelTypes} />
          <StatCard label="Total Parallels" value={stats.totalParallels} />
          <StatCard label="Autograph Parallels" value={stats.totalAutoParallels} />
          <StatCard
            label="1-of-1s"
            value={stats.totalOneOfOnes}
            highlight={stats.totalOneOfOnes > 0}
          />
        </div>
    </PageShell>
  );
}

function StatCard({
  label,
  value,
  highlight,
}: {
  label: string;
  value: number;
  highlight?: boolean;
}) {
  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900 px-6 py-5">
      <div
        className={`text-4xl font-bold tabular-nums tracking-tight ${
          highlight ? "text-amber-400" : "text-white"
        }`}
      >
        {value.toLocaleString()}
      </div>
      <div className="text-sm text-zinc-500 mt-1.5 font-medium">{label}</div>
    </div>
  );
}
