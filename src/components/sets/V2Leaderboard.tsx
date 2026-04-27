"use client";

import { useState, useMemo } from "react";
import Link from "next/link";
import type { LeaderboardRow } from "./types";
import { trackEvent } from "@/lib/trackEvent";

type SortKey = "totalCards" | "autographs" | "inserts" | "numberedParallels";

interface Props {
  entries: LeaderboardRow[];
  hasTeamData: boolean;
  setId: number;
  setSlug?: string | null;
}

const SORT_TABS: { key: SortKey; label: string }[] = [
  { key: "totalCards", label: "Total Cards" },
  { key: "autographs", label: "Autographs" },
  { key: "inserts", label: "Inserts" },
  { key: "numberedParallels", label: "Numbered" },
];

const DEFAULT_VISIBLE = 25;

export function V2Leaderboard({ entries, hasTeamData, setId, setSlug }: Props) {
  const [sortKey, setSortKey] = useState<SortKey>("totalCards");
  const [showAll, setShowAll] = useState(false);

  const sorted = useMemo(() => {
    return [...entries].sort((a, b) => {
      const diff = b[sortKey] - a[sortKey];
      if (diff !== 0) return diff;
      return a.name.localeCompare(b.name);
    });
  }, [entries, sortKey]);

  const visible = showAll ? sorted : sorted.slice(0, DEFAULT_VISIBLE);

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h2 className="text-base font-semibold text-white">Leaderboard</h2>
        <div className="flex gap-1">
          {SORT_TABS.map((tab) => (
            <button
              key={tab.key}
              onClick={() => setSortKey(tab.key)}
              className={`text-xs px-2.5 py-1 rounded-md font-medium transition-colors ${
                sortKey === tab.key
                  ? "bg-indigo-500/10 text-indigo-400 border border-indigo-500/20"
                  : "text-zinc-500 hover:text-zinc-300"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      <div className="rounded-xl border border-zinc-800 overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-zinc-800 bg-zinc-900/50">
              <th className="text-left text-xs font-medium text-zinc-500 uppercase tracking-wider px-4 py-2.5 w-8">#</th>
              <th className="text-left text-xs font-medium text-zinc-500 uppercase tracking-wider px-4 py-2.5">Athlete</th>
              {hasTeamData && (
                <th className="text-left text-xs font-medium text-zinc-500 uppercase tracking-wider px-4 py-2.5 hidden sm:table-cell">Team</th>
              )}
              <th className="text-right text-xs font-medium text-zinc-500 uppercase tracking-wider px-4 py-2.5">Cards</th>
              <th className="text-right text-xs font-medium text-zinc-500 uppercase tracking-wider px-4 py-2.5 hidden sm:table-cell">Autos</th>
              <th className="text-right text-xs font-medium text-zinc-500 uppercase tracking-wider px-4 py-2.5 hidden sm:table-cell">Inserts</th>
              <th className="text-right text-xs font-medium text-zinc-500 uppercase tracking-wider px-4 py-2.5 hidden sm:table-cell">Numbered</th>
            </tr>
          </thead>
          <tbody>
            {visible.map((entry, i) => (
              <tr key={entry.id} className="border-b border-zinc-800/50 hover:bg-zinc-800/30 transition-colors">
                <td className="px-4 py-2 text-xs text-zinc-600 tabular-nums">{i + 1}</td>
                <td className="px-4 py-2">
                  <Link
                    href={`/sets/${setSlug || setId}/athlete/${entry.slug || entry.id}`}
                    onClick={() => trackEvent(entry.id, "view")}
                    className="text-zinc-300 hover:text-indigo-400 transition-colors font-medium"
                  >
                    {entry.name}
                    {entry.isRookie && (
                      <span className="ml-1.5 text-[9px] font-bold text-amber-400">RC</span>
                    )}
                  </Link>
                </td>
                {hasTeamData && (
                  <td className="px-4 py-2 text-xs text-zinc-500 hidden sm:table-cell">{entry.team ?? "—"}</td>
                )}
                <td className="px-4 py-2 text-right tabular-nums text-zinc-300">{entry.totalCards}</td>
                <td className="px-4 py-2 text-right tabular-nums text-zinc-500 hidden sm:table-cell">{entry.autographs}</td>
                <td className="px-4 py-2 text-right tabular-nums text-zinc-500 hidden sm:table-cell">{entry.inserts}</td>
                <td className="px-4 py-2 text-right tabular-nums text-zinc-500 hidden sm:table-cell">{entry.numberedParallels}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {entries.length > DEFAULT_VISIBLE && (
        <div className="text-center">
          <button
            onClick={() => setShowAll(!showAll)}
            className="text-xs text-indigo-400 hover:text-indigo-300 transition-colors"
          >
            {showAll ? "Show less" : `Show all ${entries.length} athletes`}
          </button>
        </div>
      )}
    </div>
  );
}
