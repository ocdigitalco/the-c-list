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

// Ordered sport pills — canonical order, extras appended
const SPORT_ORDER = [
  "Basketball", "Baseball", "Soccer", "MMA", "Wrestling",
  "Racing", "Football", "Entertainment",
];

function GridIcon() {
  return (
    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6A2.25 2.25 0 0 1 6 3.75h2.25A2.25 2.25 0 0 1 10.5 6v2.25a2.25 2.25 0 0 1-2.25 2.25H6a2.25 2.25 0 0 1-2.25-2.25V6ZM3.75 15.75A2.25 2.25 0 0 1 6 13.5h2.25a2.25 2.25 0 0 1 2.25 2.25V18a2.25 2.25 0 0 1-2.25 2.25H6A2.25 2.25 0 0 1 3.75 18v-2.25ZM13.5 6a2.25 2.25 0 0 1 2.25-2.25H18A2.25 2.25 0 0 1 20.25 6v2.25A2.25 2.25 0 0 1 18 10.5h-2.25a2.25 2.25 0 0 1-2.25-2.25V6ZM13.5 15.75a2.25 2.25 0 0 1 2.25-2.25H18a2.25 2.25 0 0 1 2.25 2.25V18A2.25 2.25 0 0 1 18 20.25h-2.25a2.25 2.25 0 0 1-2.25-2.25v-2.25Z" />
    </svg>
  );
}

function ListIcon() {
  return (
    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
    </svg>
  );
}

export function ChecklistSearch({
  sets,
  allSports,
}: {
  sets: SetCard[];
  allSports: string[];
}) {
  const [query, setQuery] = useState("");
  const [activeSport, setActiveSport] = useState<string | null>(null);
  const [view, setView] = useState<"grid" | "list">("grid");
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

  // Build ordered sport list
  const orderedSports = useMemo(() => {
    const sportSet = new Set(allSports);
    const ordered: string[] = [];
    for (const s of SPORT_ORDER) {
      if (sportSet.has(s)) {
        ordered.push(s);
        sportSet.delete(s);
      }
    }
    // Append any remaining sports not in the canonical order
    for (const s of allSports) {
      if (sportSet.has(s)) ordered.push(s);
    }
    return ordered;
  }, [allSports]);

  const filtered = useMemo(() => {
    let results = sets;

    if (activeSport) {
      results = results.filter((s) => s.sport === activeSport);
    }

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

    return [...results].sort((a, b) => {
      if (!a.releaseDate && !b.releaseDate) return a.name.localeCompare(b.name);
      if (!a.releaseDate) return 1;
      if (!b.releaseDate) return -1;
      return new Date(b.releaseDate).getTime() - new Date(a.releaseDate).getTime();
    });
  }, [sets, query, activeSport]);

  const label = activeSport ? `${activeSport} Sets` : "All Sets";
  const countLabel = query.trim()
    ? `${filtered.length} set${filtered.length !== 1 ? "s" : ""} matching "${query}"`
    : `${filtered.length} set${filtered.length !== 1 ? "s" : ""}`;

  return (
    <>
      {/* Sport pill filter */}
      <div className="flex items-center gap-3 overflow-x-auto no-scrollbar">
        <span className="hidden sm:block shrink-0 text-[10px] font-semibold uppercase tracking-widest text-zinc-500">
          Sport
        </span>
        <div className="flex gap-1.5 shrink-0">
          <button
            onClick={() => setActiveSport(null)}
            className="shrink-0 px-3 py-1.5 rounded-full text-xs font-medium transition-colors"
            style={
              activeSport === null
                ? { background: "#18181b", color: "#fff" }
                : { color: "#71717a" }
            }
          >
            All
          </button>
          {orderedSports.map((sport) => (
            <button
              key={sport}
              onClick={() => setActiveSport(activeSport === sport ? null : sport)}
              className="shrink-0 px-3 py-1.5 rounded-full text-xs font-medium transition-colors"
              style={
                activeSport === sport
                  ? { background: "#18181b", color: "#fff" }
                  : { color: "#71717a" }
              }
            >
              {sport}
            </button>
          ))}
        </div>
      </div>

      {/* Search bar + view toggle */}
      <div className="flex items-center gap-2">
        <div className="relative flex-1">
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

        {/* View toggle */}
        <div className="flex rounded-lg border border-zinc-800 overflow-hidden shrink-0">
          <button
            onClick={() => setView("grid")}
            className="p-2 transition-colors"
            style={
              view === "grid"
                ? { background: "#27272a", color: "#fff" }
                : { color: "#71717a" }
            }
            aria-label="Grid view"
          >
            <GridIcon />
          </button>
          <button
            onClick={() => setView("list")}
            className="p-2 transition-colors"
            style={
              view === "list"
                ? { background: "#27272a", color: "#fff" }
                : { color: "#71717a" }
            }
            aria-label="List view"
          >
            <ListIcon />
          </button>
        </div>
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

          {view === "grid" ? (
            /* ── Grid view (original horizontal cards) ── */
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
          ) : (
            /* ── List view (vertical TikTok-style cards) ── */
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
              {filtered.map((s) => (
                <Link
                  key={s.id}
                  href={`/sets/${s.slug ?? s.id}`}
                  className="group bg-zinc-900 hover:bg-zinc-800/60 transition-colors flex flex-col"
                >
                  <div className="aspect-[3/4] overflow-hidden bg-zinc-800">
                    {s.sampleImageUrl ? (
                      <img
                        src={s.sampleImageUrl}
                        alt={s.name}
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center text-zinc-700">
                        <svg className="w-10 h-10" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1}>
                          <path strokeLinecap="round" strokeLinejoin="round" d="m2.25 15.75 5.159-5.159a2.25 2.25 0 0 1 3.182 0l5.159 5.159m-1.5-1.5 1.409-1.409a2.25 2.25 0 0 1 3.182 0l2.909 2.909M3.75 21h16.5A2.25 2.25 0 0 0 22.5 18.75V5.25A2.25 2.25 0 0 0 20.25 3H3.75A2.25 2.25 0 0 0 1.5 5.25v13.5A2.25 2.25 0 0 0 3.75 21Z" />
                        </svg>
                      </div>
                    )}
                  </div>
                  <div className="px-2.5 py-2.5 flex flex-col gap-1.5">
                    <p className="font-semibold text-white text-xs leading-snug line-clamp-2 group-hover:text-amber-400 transition-colors">
                      {s.name}
                    </p>
                    <div className="flex items-center gap-1 flex-wrap">
                      <span className="text-[10px] font-medium text-zinc-400 bg-zinc-800 border border-zinc-700 px-1.5 py-0.5 rounded">
                        {s.league ?? s.sport}
                      </span>
                      <TierBadge tier={s.tier} />
                    </div>
                    <div className="flex items-center gap-2 text-[10px] text-zinc-500">
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
          )}
        </section>
      ) : (
        <div className="text-center py-16">
          <p className="text-zinc-500 mb-3">
            No checklists found{query ? <> for &ldquo;{query}&rdquo;</> : activeSport ? <> for {activeSport}</> : null}
          </p>
          <button
            onClick={() => { setQuery(""); setActiveSport(null); }}
            className="text-sm text-amber-400 hover:text-amber-300 transition-colors"
          >
            Clear filters
          </button>
        </div>
      )}
    </>
  );
}
