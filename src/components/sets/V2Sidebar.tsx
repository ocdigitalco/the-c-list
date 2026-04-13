"use client";

import { useState, useRef, useEffect } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useV2Theme } from "./V2ThemeProvider";
import type { SidebarPlayer, BoxFormatSummary } from "./types";

interface Props {
  setId: number;
  setSlug?: string | null;
  setName: string;
  sport: string;
  league: string | null;
  season: string;
  tier: string;
  releaseDate: string | null;
  sampleImageUrl: string | null;
  boxFormats: BoxFormatSummary[];
  players: SidebarPlayer[];
  onNavigate?: () => void;
}

function formatDate(iso: string): string {
  const d = new Date(iso + "T00:00:00Z");
  return d.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    timeZone: "UTC",
  });
}

function MetaRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between text-xs">
      <span className="text-zinc-500 uppercase tracking-wider font-medium">{label}</span>
      <span className="text-zinc-300 font-semibold">{value}</span>
    </div>
  );
}

export function V2Sidebar({
  setId,
  setSlug,
  setName,
  sport,
  league,
  season,
  tier,
  releaseDate,
  sampleImageUrl,
  boxFormats,
  players,
  onNavigate,
}: Props) {
  const [query, setQuery] = useState("");
  const selectedRef = useRef<HTMLAnchorElement>(null);
  const { theme, toggle } = useV2Theme();
  const params = useParams();
  const activeAthleteId = params.athleteId ? parseInt(params.athleteId as string, 10) : null;

  const filtered = query.trim()
    ? players.filter((p) => p.name.toLowerCase().includes(query.toLowerCase()))
    : players;

  useEffect(() => {
    selectedRef.current?.scrollIntoView({ block: "center", behavior: "instant" });
  }, [activeAthleteId]);

  return (
    <div className="flex flex-col h-full w-full">
      {/* Set info */}
      <div className="px-4 pt-4 pb-3 space-y-3 border-b border-zinc-800">
        <Link
          href={`/sets/${setSlug || setId}`}
          className="block text-base font-bold text-white leading-tight hover:text-amber-400 transition-colors"
          onClick={onNavigate}
        >
          {setName}
        </Link>

        <div className="space-y-1.5">
          <MetaRow label="Sport" value={sport} />
          {league && <MetaRow label="League" value={league} />}
          <MetaRow label="Season" value={season} />
          <MetaRow label="Tier" value={tier} />
          <MetaRow label="Release" value={releaseDate ? formatDate(releaseDate) : "TBA"} />
        </div>

        {/* Box config summary */}
        {boxFormats.length > 0 ? (
          <div className="space-y-1">
            <p className="text-[10px] text-zinc-600 uppercase tracking-wider font-semibold">Box Types</p>
            <div className="flex flex-wrap gap-1">
              {boxFormats.map((bf) => (
                <span
                  key={bf.label}
                  className="text-[10px] font-medium px-1.5 py-0.5 rounded bg-zinc-800 text-zinc-400 border border-zinc-700"
                  title={bf.notes ?? `${bf.packsPerBox} packs${bf.autosPerBox ? `, ${bf.autosPerBox} auto` : ""}`}
                >
                  {bf.label}
                </span>
              ))}
            </div>
          </div>
        ) : (
          <p className="text-[10px] text-zinc-600 italic">Box config coming soon</p>
        )}

        {/* Sample image */}
        {sampleImageUrl && (
          <img
            src={sampleImageUrl}
            alt={setName}
            className="w-full rounded-lg border border-zinc-800 mt-2"
          />
        )}
      </div>

      {/* Search */}
      <div className="px-4 py-2 border-b border-zinc-800">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search athletes..."
          className="w-full text-xs px-3 py-2 rounded-lg bg-zinc-800/60 border border-zinc-700 text-white placeholder-zinc-500 focus:outline-none focus:border-zinc-500"
        />
      </div>

      {/* Player list */}
      <div className="flex-1 overflow-y-auto">
        {filtered.map((p) => {
          const isActive = p.id === activeAthleteId;
          return (
            <Link
              key={p.id}
              ref={isActive ? selectedRef : undefined}
              href={`/sets/${setSlug || setId}/athlete/${p.slug || p.id}`}
              onClick={onNavigate}
              className={`flex items-center justify-between px-4 py-2 text-xs transition-colors ${
                isActive
                  ? "bg-indigo-500/10 text-indigo-400 border-l-2 border-indigo-500"
                  : "text-zinc-400 hover:bg-zinc-800/60 hover:text-zinc-200 border-l-2 border-transparent"
              }`}
            >
              <span className="truncate">
                {p.name}
                {p.hasRookie && (
                  <span className="ml-1.5 text-[9px] font-bold text-amber-400">RC</span>
                )}
              </span>
              <span className="shrink-0 ml-2 text-zinc-600 tabular-nums">{p.totalCards}</span>
            </Link>
          );
        })}
        {filtered.length === 0 && (
          <p className="px-4 py-6 text-xs text-zinc-600 text-center">No athletes found</p>
        )}
      </div>

      {/* Theme toggle */}
      <div className="px-4 py-3 border-t border-zinc-800">
        <button
          onClick={toggle}
          className="flex items-center gap-2 text-xs text-zinc-500 hover:text-zinc-300 transition-colors"
        >
          {theme === "light" ? (
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M21.752 15.002A9.72 9.72 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z" />
            </svg>
          ) : (
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" />
            </svg>
          )}
          {theme === "light" ? "Dark mode" : "Light mode"}
        </button>
      </div>
    </div>
  );
}
