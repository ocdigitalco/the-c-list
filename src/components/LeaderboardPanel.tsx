"use client";

import { useState, useMemo } from "react";
import { useRouter } from "next/navigation";

// ─── Types ────────────────────────────────────────────────────────────────────

export interface LeaderboardEntry {
  id: number;
  name: string;
  team: string | null;
  isRookie: boolean;
  totalCards: number;
  autographs: number;
  inserts: number;
  numberedParallels: number;
}

type SortKey = "totalCards" | "autographs" | "inserts" | "numberedParallels";

interface Props {
  entries: LeaderboardEntry[];
  hasTeamData: boolean;
  setId: number;
}

const SORT_TABS: { key: SortKey; label: string }[] = [
  { key: "totalCards", label: "Total Cards" },
  { key: "autographs", label: "Autographs" },
  { key: "inserts", label: "Inserts" },
  { key: "numberedParallels", label: "Numbered" },
];

const DEFAULT_VISIBLE = 50;

// ─── Main Component ───────────────────────────────────────────────────────────

export function LeaderboardPanel({ entries, hasTeamData, setId }: Props) {
  const [open, setOpen] = useState(false);
  const [sortKey, setSortKey] = useState<SortKey>("totalCards");
  const [rookiesOnly, setRookiesOnly] = useState(false);
  const [teamQuery, setTeamQuery] = useState("");
  const [showAll, setShowAll] = useState(false);
  const router = useRouter();

  const filtered = useMemo(() => {
    let list = entries;
    if (rookiesOnly) list = list.filter((e) => e.isRookie);
    if (hasTeamData && teamQuery.trim()) {
      const q = teamQuery.trim().toLowerCase();
      list = list.filter((e) => e.team?.toLowerCase().includes(q));
    }
    return [...list].sort((a, b) => b[sortKey] - a[sortKey]);
  }, [entries, rookiesOnly, teamQuery, sortKey, hasTeamData]);

  const visible = showAll ? filtered : filtered.slice(0, DEFAULT_VISIBLE);
  const hasMore = filtered.length > DEFAULT_VISIBLE;

  function handleRowClick(id: number) {
    setOpen(false);
    router.push(`/sets/${setId}?player=${id}`);
  }

  return (
    <>
      {/* Trigger button */}
      <button
        onClick={() => setOpen(true)}
        className="flex items-center gap-1.5 shrink-0 text-xs font-medium text-zinc-400 hover:text-white border border-zinc-700 hover:border-zinc-500 bg-zinc-900 hover:bg-zinc-800 px-3 py-1.5 rounded-md transition-colors"
      >
        <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 0 1 3 19.875v-6.75ZM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V8.625ZM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V4.125Z" />
        </svg>
        Leaderboard
      </button>

      {/* Backdrop */}
      {open && (
        <div
          className="fixed inset-0 z-40 bg-black/60"
          onClick={() => setOpen(false)}
        />
      )}

      {/* Slide-in drawer */}
      <div
        className={`fixed top-0 right-0 z-50 h-full w-full sm:w-[400px] bg-zinc-900 border-l border-zinc-800 shadow-2xl flex flex-col transition-transform duration-300 ${
          open ? "translate-x-0" : "translate-x-full"
        }`}
      >
        {/* Header */}
        <div className="shrink-0 flex items-center justify-between px-5 py-4 border-b border-zinc-800">
          <div>
            <h2 className="text-sm font-semibold text-white">Athlete Leaderboard</h2>
            <p className="text-xs text-zinc-500 mt-0.5">{entries.length.toLocaleString()} athletes</p>
          </div>
          <button
            onClick={() => setOpen(false)}
            className="p-1.5 rounded-md text-zinc-500 hover:text-white hover:bg-zinc-800 transition-colors"
            aria-label="Close"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18 18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Controls */}
        <div className="shrink-0 px-4 pt-3 pb-2 space-y-2.5 border-b border-zinc-800">
          {/* Sort tabs */}
          <div className="flex gap-1 rounded-lg bg-zinc-800/60 p-0.5">
            {SORT_TABS.map((tab) => (
              <button
                key={tab.key}
                onClick={() => setSortKey(tab.key)}
                className={`flex-1 text-xs py-1.5 rounded-md font-medium transition-colors ${
                  sortKey === tab.key
                    ? "bg-zinc-700 text-white"
                    : "text-zinc-400 hover:text-zinc-200"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* Filters row */}
          <div className="flex items-center gap-2">
            {/* Rookies toggle */}
            <button
              onClick={() => setRookiesOnly((v) => !v)}
              className={`flex items-center gap-1.5 text-xs px-2.5 py-1.5 rounded-md border font-medium transition-colors ${
                rookiesOnly
                  ? "bg-amber-400/10 border-amber-400/40 text-amber-400"
                  : "border-zinc-700 text-zinc-400 hover:text-zinc-200 hover:border-zinc-500"
              }`}
            >
              <span>Rookies Only</span>
            </button>

            {/* Team search */}
            {hasTeamData && (
              <div className="flex-1 relative">
                <svg
                  className="absolute left-2 top-1/2 -translate-y-1/2 w-3 h-3 text-zinc-600 pointer-events-none"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth={2.5}
                >
                  <path strokeLinecap="round" strokeLinejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                </svg>
                <input
                  type="text"
                  value={teamQuery}
                  onChange={(e) => setTeamQuery(e.target.value)}
                  placeholder="Filter by team…"
                  className="w-full bg-zinc-800 border border-zinc-700 text-xs text-white placeholder-zinc-600 rounded-md pl-7 pr-2.5 py-1.5 outline-none focus:border-zinc-500 transition-colors"
                />
              </div>
            )}
          </div>
        </div>

        {/* Table header */}
        <div className="shrink-0 grid grid-cols-[1fr_auto] px-4 py-1.5 text-xs font-semibold text-zinc-600 uppercase tracking-wider border-b border-zinc-800/60">
          <span>Athlete</span>
          <span className="text-right tabular-nums">
            {SORT_TABS.find((t) => t.key === sortKey)?.label}
          </span>
        </div>

        {/* Rows */}
        <div className="flex-1 overflow-y-auto">
          {visible.length === 0 ? (
            <p className="text-xs text-zinc-600 italic text-center py-8">No athletes match.</p>
          ) : (
            <>
              {visible.map((entry, idx) => (
                <button
                  key={entry.id}
                  onClick={() => handleRowClick(entry.id)}
                  className="w-full grid grid-cols-[auto_1fr_auto] items-center gap-3 px-4 py-2.5 hover:bg-zinc-800/50 transition-colors border-b border-zinc-800/40 text-left"
                >
                  <span className="text-xs text-zinc-600 tabular-nums w-5 text-right">{idx + 1}</span>
                  <div className="min-w-0">
                    <div className="flex items-center gap-1.5 min-w-0">
                      <span className="text-sm font-medium text-zinc-200 truncate">{entry.name}</span>
                      {entry.isRookie && (
                        <span className="shrink-0 text-[10px] font-semibold text-amber-400 bg-amber-400/10 px-1 py-0.5 rounded leading-none">
                          RC
                        </span>
                      )}
                    </div>
                    {hasTeamData && entry.team && (
                      <p className="text-xs text-zinc-600 truncate mt-0.5">{entry.team}</p>
                    )}
                  </div>
                  <span className="text-sm font-bold text-white tabular-nums">
                    {entry[sortKey].toLocaleString()}
                  </span>
                </button>
              ))}

              {!showAll && hasMore && (
                <button
                  onClick={() => setShowAll(true)}
                  className="w-full py-3 text-xs font-medium text-zinc-500 hover:text-zinc-300 transition-colors"
                >
                  Show all {filtered.length.toLocaleString()} athletes
                </button>
              )}
            </>
          )}
        </div>
      </div>
    </>
  );
}
