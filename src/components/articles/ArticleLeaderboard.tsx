"use client";

import { useState } from "react";

interface LeaderboardAthlete {
  name: string;
  team: string | null;
  isRookie: boolean;
  totalCards: number;
  autographs: number;
}

const AVATAR_COLORS = [
  "bg-red-500/20 text-red-400",
  "bg-blue-500/20 text-blue-400",
  "bg-green-500/20 text-green-400",
  "bg-amber-500/20 text-amber-400",
  "bg-purple-500/20 text-purple-400",
  "bg-pink-500/20 text-pink-400",
  "bg-cyan-500/20 text-cyan-400",
  "bg-orange-500/20 text-orange-400",
];

function getAvatarColor(name: string) {
  return AVATAR_COLORS[name.charCodeAt(0) % AVATAR_COLORS.length];
}

function getInitials(name: string) {
  const parts = name.split(" ");
  if (parts.length === 1) return parts[0][0];
  return parts[0][0] + parts[parts.length - 1][0];
}

export function ArticleLeaderboard({
  athletes,
  defaultFilter,
}: {
  athletes: LeaderboardAthlete[];
  defaultFilter: "all" | "autographs" | "rookies";
}) {
  const [filter, setFilter] = useState(defaultFilter);

  const filtered = athletes.filter((a) => {
    if (filter === "autographs") return a.autographs > 0;
    if (filter === "rookies") return a.isRookie;
    return true;
  });

  // Sort by the metric relevant to the active filter
  const sortKey = filter === "autographs" ? "autographs" : "totalCards";
  const sorted = [...filtered].sort((a, b) => b[sortKey] - a[sortKey]);
  const top10 = sorted.slice(0, 10);
  const maxValue = top10[0]?.[sortKey] ?? 1;

  return (
    <div className="rounded-xl border border-zinc-800 overflow-hidden mb-6">
      <div className="flex gap-1.5 p-3 border-b border-zinc-800 bg-zinc-900/60">
        {(["all", "autographs", "rookies"] as const).map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`text-xs font-medium px-3 py-1 rounded-full border transition-colors ${
              filter === f
                ? "bg-zinc-200 text-zinc-900 border-zinc-300"
                : "bg-zinc-800 text-zinc-400 border-zinc-700 hover:border-zinc-600"
            }`}
          >
            {f === "all" ? "All Cards" : f === "autographs" ? "Autographs" : "Rookies Only"}
          </button>
        ))}
      </div>
      <div className="divide-y divide-zinc-800/60">
        {top10.map((a, i) => {
          const displayValue = a[sortKey];
          return (
            <div
              key={a.name}
              className="flex items-center gap-3 px-4 py-2.5 bg-zinc-900 hover:bg-zinc-800/40 transition-colors"
            >
              <span className="text-xs text-zinc-600 font-medium tabular-nums w-5 text-right shrink-0">
                {i + 1}
              </span>
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold shrink-0 ${getAvatarColor(a.name)}`}
              >
                {getInitials(a.name)}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-1.5">
                  <p className="text-sm font-semibold text-zinc-200 truncate">
                    {a.name}
                  </p>
                  {a.isRookie && (
                    <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-green-500/15 text-green-400 border border-green-500/30 shrink-0">
                      RC
                    </span>
                  )}
                </div>
                {a.team && (
                  <p className="text-[11px] text-zinc-600 truncate">{a.team}</p>
                )}
              </div>
              <div className="flex items-center gap-2 shrink-0 w-32">
                <div className="flex-1 h-2 bg-zinc-800 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-amber-500/60 rounded-full"
                    style={{ width: `${(displayValue / maxValue) * 100}%` }}
                  />
                </div>
                <span className="text-xs text-zinc-400 tabular-nums w-8 text-right">
                  {displayValue}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
