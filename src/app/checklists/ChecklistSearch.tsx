"use client";

import { useState, useMemo, useEffect, useRef } from "react";
import Link from "next/link";

interface SetCard {
  id: number;
  name: string;
  slug: string | null;
  sport: string;
  league: string | null;
  tier: string;
  season: string;
  releaseDate: string | null;
  sampleImageUrl: string | null;
  athleteCount: number;
  cardCount: number;
}

function TierBadge({ tier }: { tier: string }) {
  if (tier === "Prizm") return <span className="shrink-0 text-xs font-semibold px-2 py-0.5 rounded bg-gradient-to-r from-violet-600 via-fuchsia-500 to-pink-500 text-white">Prizm</span>;
  if (tier === "Premium") return <span className="shrink-0 text-xs font-semibold px-2 py-0.5 rounded bg-amber-950 text-amber-300 border border-amber-700/60">Premium</span>;
  if (tier === "Sapphire") return <span className="shrink-0 text-xs font-semibold px-2 py-0.5 rounded bg-blue-950 text-blue-300 border border-blue-700/60">Sapphire</span>;
  if (tier === "Chrome") return <span className="shrink-0 text-xs font-semibold px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-600/50">Chrome</span>;
  return null;
}

export function ChecklistSearch({
  sets,
  activeSport,
}: {
  sets: SetCard[];
  activeSport: string | null;
}) {
  const [query, setQuery] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    function onKeyDown(e: KeyboardEvent) {
      if (e.key === "Escape") {
        setQuery("");
        inputRef.current?.blur();
      }
    }
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, []);

  const filtered = useMemo(() => {
    let results = sets;

    if (query.trim()) {
      const q = query.toLowerCase();
      results = results.filter(
        (s) =>
          s.name?.toLowerCase().includes(q) ||
          s.sport?.toLowerCase().includes(q) ||
          s.league?.toLowerCase().includes(q) ||
          s.tier?.toLowerCase().includes(q) ||
          s.season?.toLowerCase().includes(q)
      );
    }

    // Sort: sets with releaseDate newest first, nulls at end
    return [...results].sort((a, b) => {
      if (!a.releaseDate && !b.releaseDate) return a.name.localeCompare(b.name);
      if (!a.releaseDate) return 1;
      if (!b.releaseDate) return -1;
      return new Date(b.releaseDate).getTime() - new Date(a.releaseDate).getTime();
    });
  }, [sets, query]);

  const label = activeSport ? `${activeSport} Sets` : "All Sets";
  const countLabel = query.trim()
    ? `${filtered.length} set${filtered.length !== 1 ? "s" : ""} matching "${query}"`
    : `${filtered.length} set${filtered.length !== 1 ? "s" : ""}`;

  return (
    <>
      {/* Search bar */}
      <div className="relative">
        <svg
          className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-600 pointer-events-none"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth={2}
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"
          />
        </svg>
        <input
          ref={inputRef}
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search by name, sport, league, or tier..."
          className="w-full rounded-lg border border-zinc-800 bg-zinc-900 text-sm text-zinc-200 placeholder-zinc-600 pl-10 pr-9 py-2.5 focus:outline-none focus:border-zinc-600 transition-colors"
        />
        {query && (
          <button
            onClick={() => setQuery("")}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-zinc-600 hover:text-zinc-400 transition-colors"
            aria-label="Clear search"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        )}
      </div>

      {/* Results */}
      {filtered.length > 0 ? (
        <section>
          <h2 className="text-xs font-semibold text-zinc-500 uppercase tracking-widest mb-4">
            {label}{" "}
            <span className="normal-case font-normal text-zinc-700">
              · {countLabel}
            </span>
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {filtered.map((s) => (
              <Link
                key={s.id}
                href={`/sets/${s.slug ?? s.id}`}
                className="group border border-zinc-800 bg-zinc-900 hover:border-zinc-600 hover:bg-zinc-800/60 transition-colors flex overflow-hidden"
              >
                {s.sampleImageUrl && (
                  <div className="shrink-0 w-20 sm:w-24 self-stretch overflow-hidden bg-zinc-800">
                    <img
                      src={s.sampleImageUrl}
                      alt={s.name}
                      className="w-full h-full object-cover"
                    />
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
                    <TierBadge tier={s.tier} />
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
      ) : (
        <div className="text-center py-16">
          <p className="text-zinc-500 mb-3">
            No checklists found for &ldquo;{query}&rdquo;
          </p>
          <button
            onClick={() => setQuery("")}
            className="text-sm text-amber-400 hover:text-amber-300 transition-colors"
          >
            Clear search
          </button>
        </div>
      )}
    </>
  );
}
