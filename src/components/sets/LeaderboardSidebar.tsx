"use client";

import { useState, useMemo, useRef, useEffect } from "react";
import Link from "next/link";
import type { LeaderboardRow } from "./types";
import { getNBAHeadshotUrl } from "@/lib/nba-headshot";
import { getUFCHeadshotUrl } from "@/lib/ufc-headshot";
import { getMLBHeadshotUrl } from "@/lib/mlb-headshot";
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

const DEFAULT_VISIBLE = 50;

function InitialsAvatar({ name }: { name: string }) {
  const initials = name
    .split(" ")
    .map((n) => n[0])
    .slice(0, 2)
    .join("")
    .toUpperCase();
  return (
    <div
      className="w-10 h-10 rounded-full flex items-center justify-center text-sm font-semibold flex-shrink-0"
      style={{ background: "var(--v2-badge-bg)", color: "var(--v2-text-secondary)" }}
    >
      {initials}
    </div>
  );
}

function PlayerAvatar({ name, nbaPlayerId, ufcImageUrl, mlbPlayerId, imageUrl }: { name: string; nbaPlayerId: number | null; ufcImageUrl: string | null; mlbPlayerId: number | null; imageUrl?: string | null }) {
  const [imgError, setImgError] = useState(false);
  const url = getNBAHeadshotUrl(nbaPlayerId) ?? getUFCHeadshotUrl(ufcImageUrl) ?? getMLBHeadshotUrl(mlbPlayerId) ?? (imageUrl || null);

  if (!url || imgError) {
    return <InitialsAvatar name={name} />;
  }

  return (
    <img
      src={url}
      alt={name}
      loading="lazy"
      onError={() => setImgError(true)}
      className="w-10 h-10 rounded-full object-cover object-top flex-shrink-0"
      style={{ border: "2px solid var(--v2-border)" }}
    />
  );
}

export function LeaderboardSidebar({ entries, hasTeamData, setId, setSlug }: Props) {
  const [sortKey, setSortKey] = useState<SortKey>("totalCards");
  const [rookiesOnly, setRookiesOnly] = useState(false);
  const [teamQuery, setTeamQuery] = useState("");
  const [nameQuery, setNameQuery] = useState("");
  const [showAll, setShowAll] = useState(false);
  const searchDebounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    return () => { if (searchDebounceRef.current) clearTimeout(searchDebounceRef.current); };
  }, []);

  const filtered = useMemo(() => {
    let list = entries;
    if (nameQuery.trim()) {
      const q = nameQuery.trim().toLowerCase();
      list = list.filter((e) => e.name.toLowerCase().includes(q));
    }
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
  }, [entries, nameQuery, rookiesOnly, teamQuery, sortKey, hasTeamData]);

  const visible = showAll ? filtered : filtered.slice(0, DEFAULT_VISIBLE);
  const hasMore = filtered.length > DEFAULT_VISIBLE;

  return (
    <div className="flex flex-col h-full" style={{ background: "var(--v2-sidebar-bg)" }}>
      {/* Header + Controls */}
      <div className="shrink-0 px-3 pt-4 pb-2 space-y-2" style={{ borderBottom: "1px solid var(--v2-border)" }}>
        <h2 className="text-base font-semibold px-1" style={{ color: "var(--v2-text-primary)" }}>
          Athletes in Set
        </h2>
        {/* Search */}
        <div className="relative">
          <svg
            className="absolute left-2.5 top-1/2 -translate-y-1/2 w-4 h-4 pointer-events-none"
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
            value={nameQuery}
            onChange={(e) => {
              const q = e.target.value;
              setNameQuery(q);
              if (searchDebounceRef.current) clearTimeout(searchDebounceRef.current);
              if (q.trim().length >= 2) {
                searchDebounceRef.current = setTimeout(() => {
                  const matches = entries.filter((a) => a.name.toLowerCase().includes(q.toLowerCase()));
                  matches.slice(0, 3).forEach((a) => trackEvent(a.id, "search"));
                }, 600);
              }
            }}
            placeholder="Search athletes..."
            autoComplete="off"
            spellCheck={false}
            className="w-full text-base rounded-md pl-8 pr-8 py-2 outline-none transition-colors"
            style={{
              background: "var(--v2-card-bg)",
              border: "1px solid var(--v2-border)",
              color: "var(--v2-text-primary)",
              fontSize: "16px",
            }}
          />
          {nameQuery && (
            <button
              onClick={() => setNameQuery("")}
              className="absolute right-2 top-1/2 -translate-y-1/2 w-5 h-5 flex items-center justify-center rounded-full transition-colors"
              style={{ background: "var(--v2-badge-bg)", color: "var(--v2-text-secondary)" }}
            >
              <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          )}
        </div>
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
                href={`/sets/${setSlug || setId}/athlete/${entry.slug || entry.id}`}
                onClick={() => trackEvent(entry.id, "view")}
                className="grid grid-cols-[auto_auto_1fr_auto] items-center gap-2.5 px-4 py-2.5 transition-colors text-left"
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
                <PlayerAvatar name={entry.name} nbaPlayerId={entry.nbaPlayerId} ufcImageUrl={entry.ufcImageUrl} mlbPlayerId={entry.mlbPlayerId} imageUrl={entry.imageUrl} />
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
