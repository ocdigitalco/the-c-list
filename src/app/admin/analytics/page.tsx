import { rawQuery } from "@/lib/db";
import { TimeRangeSelector } from "./TimeRangeSelector";
import { SportFilter } from "@/components/SportFilter";
import { PageShell } from "@/components/PageShell";

export const dynamic = "force-dynamic";

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


interface LeaderboardRow {
  player_name: string;
  sports: string;
  set_names: string;
  event_count: number;
}

async function queryLeaderboard(eventType: "search" | "view", cutoff: number, sport: string | null): Promise<LeaderboardRow[]> {
  const sportClause = sport ? "AND s.sport = ?" : "";
  const args: (string | number)[] = sport
    ? [eventType, cutoff, sport]
    : [eventType, cutoff];
  return rawQuery.all<LeaderboardRow>(
    `SELECT
      p.name AS player_name,
      GROUP_CONCAT(DISTINCT s.sport) AS sports,
      GROUP_CONCAT(DISTINCT s.name) AS set_names,
      COUNT(pe.id) AS event_count
    FROM player_events pe
    JOIN players p ON pe.player_id = p.id
    JOIN sets s ON p.set_id = s.id
    WHERE pe.event_type = ? AND pe.created_at >= ? ${sportClause}
    GROUP BY p.name
    ORDER BY event_count DESC
    LIMIT 25`,
    ...args
  );
}

async function totalEvents(eventType: "search" | "view", cutoff: number, sport: string | null): Promise<number> {
  const sportClause = sport ? "AND s.sport = ?" : "";
  const args: (string | number)[] = sport
    ? [eventType, cutoff, sport]
    : [eventType, cutoff];
  const row = await rawQuery.get<{ n: number }>(
    `SELECT COUNT(*) AS n
     FROM player_events pe
     JOIN players p ON pe.player_id = p.id
     JOIN sets s ON p.set_id = s.id
     WHERE pe.event_type = ? AND pe.created_at >= ? ${sportClause}`,
    ...args
  );
  return row?.n ?? 0;
}

async function queryAllSports(): Promise<string[]> {
  const rows = await rawQuery.all<{ sport: string }>(
    `SELECT DISTINCT sport FROM sets ORDER BY sport`
  );
  return rows.map((r) => r.sport);
}

export default async function AnalyticsPage({
  searchParams,
}: {
  searchParams: Promise<{ range?: string; sport?: string }>;
}) {
  const { range: rangeParam, sport: sportParam } = await searchParams;
  const range: Range = VALID_RANGES.includes(rangeParam as Range)
    ? (rangeParam as Range)
    : "7d";

  const allSports = await queryAllSports();
  const sport = sportParam && allSports.includes(sportParam) ? sportParam : null;

  const cutoff = cutoffMs(range);
  const searches = await queryLeaderboard("search", cutoff, sport);
  const views = await queryLeaderboard("view", cutoff, sport);
  const totalSearches = await totalEvents("search", cutoff, sport);
  const totalViews = await totalEvents("view", cutoff, sport);

  return (
    <PageShell
      breadcrumb={{ label: "Home", href: "/checklists" }}
      title="Searches"
      description="Recent search activity across the app"
    >
        <div className="flex justify-end -mt-4">
          <TimeRangeSelector current={range} sport={sport} />
        </div>

        {/* Sport filter */}
        <SportFilter sports={allSports} current={sport} path="/admin/analytics" extraParams={{ range }} />

        {/* Leaderboards */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Leaderboard
            title="Most Searched"
            icon={
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-4.35-4.35M17 11A6 6 0 1 1 5 11a6 6 0 0 1 12 0z" />
              </svg>
            }
            rows={searches}
            total={totalSearches}
            countLabel="searches"
          />
          <Leaderboard
            title="Most Viewed"
            icon={
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.964-7.178z" />
                <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            }
            rows={views}
            total={totalViews}
            countLabel="views"
          />
        </div>
    </PageShell>
  );
}

function Leaderboard({
  title,
  icon,
  rows,
  total,
  countLabel,
}: {
  title: string;
  icon: React.ReactNode;
  rows: LeaderboardRow[];
  total: number;
  countLabel: string;
}) {
  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900 overflow-hidden">
      {/* Section header */}
      <div className="flex items-center justify-between px-5 py-4 border-b border-zinc-800">
        <div className="flex items-center gap-2 text-white font-semibold">
          <span className="text-zinc-400">{icon}</span>
          {title}
        </div>
        <span className="text-xs text-zinc-500 tabular-nums">
          {total.toLocaleString()} {countLabel} total
        </span>
      </div>

      {rows.length === 0 ? (
        <div className="px-5 py-12 text-center">
          <p className="text-sm text-zinc-600">No data for this time range</p>
        </div>
      ) : (
        <div className="divide-y divide-zinc-800">
          {rows.map((row, i) => {
            const sets = row.set_names.split(",").map((s) => s.trim());
            const sport = row.sports.split(",")[0].trim();
            return (
              <div key={row.player_name} className="flex items-center gap-4 px-5 py-3.5">
                {/* Rank */}
                <span
                  className={`w-6 shrink-0 text-sm font-bold tabular-nums text-right ${
                    i === 0
                      ? "text-amber-400"
                      : i === 1
                      ? "text-zinc-300"
                      : i === 2
                      ? "text-amber-700"
                      : "text-zinc-600"
                  }`}
                >
                  {i + 1}
                </span>

                {/* Player info */}
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-white truncate">{row.player_name}</p>
                  <div className="flex items-center gap-2 mt-0.5 flex-wrap">
                    <span className="text-xs text-zinc-500">{sport}</span>
                    <span className="text-zinc-700 text-xs">·</span>
                    <span className="text-xs text-zinc-600 truncate">
                      {sets.length > 2
                        ? `${sets[0]}, +${sets.length - 1} more`
                        : sets.join(", ")}
                    </span>
                  </div>
                </div>

                {/* Count */}
                <span className="shrink-0 text-sm font-bold tabular-nums text-zinc-200">
                  {row.event_count.toLocaleString()}
                </span>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
