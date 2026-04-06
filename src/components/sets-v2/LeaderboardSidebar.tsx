"use client";

import { useState, useMemo } from "react";
import Link from "next/link";
import type { LeaderboardRow } from "./types";

type SortKey = "totalCards" | "autographs" | "inserts" | "numberedParallels";

interface Props {
  entries: LeaderboardRow[];
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

export function LeaderboardSidebar({ entries, hasTeamData, setId }: Props) {
  const [sortKey, setSortKey] = useState<SortKey>("totalCards");
  const [rookiesOnly, setRookiesOnly] = useState(false);
  const [teamQuery, setTeamQuery] = useState("");
  const [showAll, setShowAll] = useState(false);

  const filtered = useMemo(() => {
    let list = entries;
    if (rookiesOnly) list = list.filter((e) => e.isRookie);
    if (hasTeamData && teamQuery.trim()) {
      const q = teamQuery.trim().toLowerCase();
      list = list.filter((e) => e.team?.toLowerCase().includes(q));
    }
    return [...list].sort((a, b) => {
      const diff = b[sortKey] - a[sortKey];
      if (diff !== 0) return diff;
      return a.name.localeCompare(b.name);
    });
  }, [entries, rookiesOnly, teamQuery, sortKey, hasTeamData]);

  const visible = showAll ? filtered : filtered.slice(0, DEFAULT_VISIBLE);
  const hasMore = filtered.length > DEFAULT_VISIBLE;

  return (
    <div className="flex flex-col h-full" style={{ background: "var(--v2-sidebar-bg)" }}>
      {/* Header */}
      <div className="shrink-0 px-4 pt-4 pb-3" style={{ borderBottom: "1px solid var(--v2-border)" }}>
        <h2 className="text-base font-semibold" style={{ color: "var(--v2-text-primary)" }}>
          Athlete Leaderboard
        </h2>
      </div>

      {/* Controls */}
      <div className="shrink-0 px-3 pt-3 pb-2 space-y-2" style={{ borderBottom: "1px solid var(--v2-border)" }}>
        {/* Sort tabs */}
        <div className="flex gap-0.5 rounded-lg p-0.5" style={{ background: "var(--v2-badge-bg)" }}>
          {SORT_TABS.map((tab) => (
            <button
              key={tab.key}
              onClick={() => setSortKey(tab.key)}
              className="flex-1 text-base py-1.5 rounded-md font-medium transition-colors"
              style={{
                background: sortKey === tab.key ? "var(--v2-accent)" : "transparent",
                color: sortKey === tab.key ? "#FFFFFF" : "var(--v2-text-secondary)",
              }}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Filters */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => setRookiesOnly((v) => !v)}
            className="flex items-center gap-1 text-base px-2 py-1.5 rounded-md font-medium transition-colors"
            style={{
              background: rookiesOnly ? "var(--v2-accent-light)" : "transparent",
              color: rookiesOnly ? "var(--v2-accent)" : "var(--v2-text-secondary)",
              border: `1px solid ${rookiesOnly ? "var(--v2-accent)" : "var(--v2-border)"}`,
            }}
          >
            Rookies Only
          </button>
          {hasTeamData && (
            <div className="flex-1 relative">
              <svg
                className="absolute left-2 top-1/2 -translate-y-1/2 w-3.5 h-3.5 pointer-events-none"
                style={{ color: "var(--v2-text-secondary)" }}
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
                placeholder="Filter by team..."
                className="w-full text-base rounded-md pl-7 pr-2 py-1.5 outline-none transition-colors"
                style={{
                  background: "var(--v2-card-bg)",
                  border: "1px solid var(--v2-border)",
                  color: "var(--v2-text-primary)",
                }}
              />
            </div>
          )}
        </div>
      </div>

      {/* Table header */}
      <div
        className="shrink-0 grid grid-cols-[1fr_auto] px-4 py-1.5 text-base font-medium uppercase tracking-wide"
        style={{ color: "var(--v2-text-secondary)", borderBottom: "1px solid var(--v2-border)" }}
      >
        <span>Athlete</span>
        <span className="text-right tabular-nums">
          {SORT_TABS.find((t) => t.key === sortKey)?.label}
        </span>
      </div>

      {/* Rows */}
      <div className="flex-1 overflow-y-auto">
        {visible.length === 0 ? (
          <p
            className="text-base italic text-center py-8"
            style={{ color: "var(--v2-text-secondary)" }}
          >
            No athletes match.
          </p>
        ) : (
          <>
            {visible.map((entry, idx) => (
              <Link
                key={entry.id}
                href={`/sets-v2/${setId}/athlete/${entry.id}`}
                className="grid grid-cols-[auto_1fr_auto] items-center gap-2.5 px-4 py-2.5 transition-colors text-left"
                style={{ borderBottom: "1px solid var(--v2-border)" }}
                onMouseEnter={(e) => {
                  (e.currentTarget as HTMLElement).style.background = "var(--v2-accent-light)";
                }}
                onMouseLeave={(e) => {
                  (e.currentTarget as HTMLElement).style.background = "transparent";
                }}
              >
                <span
                  className="text-base tabular-nums w-6 text-right"
                  style={{ color: "var(--v2-text-secondary)" }}
                >
                  {idx + 1}
                </span>
                <div className="min-w-0">
                  <div className="flex items-center gap-1.5 min-w-0">
                    <span
                      className="text-base font-medium truncate"
                      style={{ color: "var(--v2-text-primary)" }}
                    >
                      {entry.name}
                    </span>
                    {entry.isRookie && (
                      <span
                        className="shrink-0 text-[10px] font-bold px-1 py-0.5 rounded leading-none"
                        style={{ color: "#F59E0B", background: "rgba(245,158,11,0.1)" }}
                      >
                        RC
                      </span>
                    )}
                  </div>
                  {hasTeamData && entry.team && (
                    <p
                      className="text-base truncate mt-0.5"
                      style={{ color: "var(--v2-text-secondary)" }}
                    >
                      {entry.team}
                    </p>
                  )}
                </div>
                <span
                  className="text-base font-bold tabular-nums"
                  style={{ color: "var(--v2-accent)" }}
                >
                  {entry[sortKey].toLocaleString()}
                </span>
              </Link>
            ))}

            {!showAll && hasMore && (
              <button
                onClick={() => setShowAll(true)}
                className="w-full py-3 text-base font-medium transition-colors"
                style={{ color: "var(--v2-accent)" }}
              >
                Show all {filtered.length.toLocaleString()} athletes
              </button>
            )}
          </>
        )}
      </div>
    </div>
  );
}
