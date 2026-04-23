"use client";

import { useState, useRef, useEffect } from "react";
import Link from "next/link";

export interface SidebarPlayer {
  id: number;
  name: string;
  totalCards: number;
  hasRookie: boolean;
}

interface Props {
  players: SidebarPlayer[];
  selectedPlayerId: number | null;
  setId: number;
  setSlug?: string | null;
}

export function PlayerSidebar({ players, selectedPlayerId, setId, setSlug }: Props) {
  const [query, setQuery] = useState("");
  const selectedRef = useRef<HTMLAnchorElement>(null);

  const filtered = query.trim()
    ? players.filter((p) =>
        p.name.toLowerCase().includes(query.toLowerCase())
      )
    : players;

  // Scroll selected player into view on initial render
  useEffect(() => {
    if (selectedRef.current) {
      selectedRef.current.scrollIntoView({ block: "nearest" });
    }
  }, []);

  function trackSearch(playerId: number) {
    if (!query.trim()) return;
    fetch("/api/events", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ playerId, eventType: "search" }),
    }).catch(() => {});
  }

  return (
    <aside className="w-72 shrink-0 flex flex-col border-r border-zinc-800 bg-zinc-950">
      {/* Search input */}
      <div className="p-3 border-b border-zinc-800">
        <div className="relative">
          <svg
            className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-zinc-500 pointer-events-none"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={2.5}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M21 21l-4.35-4.35M17 11A6 6 0 1 1 5 11a6 6 0 0 1 12 0z"
            />
          </svg>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search players..."
            className="w-full bg-zinc-900 border border-zinc-700 rounded-lg pl-8 pr-3 py-2 text-sm text-zinc-100 placeholder-zinc-600 focus:outline-none focus:border-zinc-500 transition-colors"
          />
          {query && (
            <button
              onClick={() => setQuery("")}
              className="absolute right-2.5 top-1/2 -translate-y-1/2 text-zinc-500 hover:text-zinc-300 transition-colors"
            >
              <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          )}
        </div>
        {query && (
          <p className="text-xs text-zinc-600 mt-1.5 px-0.5">
            {filtered.length} of {players.length} players
          </p>
        )}
      </div>

      {/* Player list */}
      <div className="flex-1 overflow-y-auto">
        {filtered.length === 0 ? (
          <div className="px-4 py-10 text-center">
            <p className="text-sm text-zinc-600">No players found</p>
          </div>
        ) : (
          filtered.map((player) => {
            const isSelected = player.id === selectedPlayerId;
            return (
              <Link
                key={player.id}
                href={`/sets/${setSlug ?? setId}?player=${player.id}`}
                ref={isSelected ? selectedRef : null}
                onClick={() => trackSearch(player.id)}
                className={`flex items-center justify-between gap-2 px-4 py-3 border-b border-zinc-800/40 hover:bg-zinc-900 transition-colors ${
                  isSelected
                    ? "bg-zinc-900 border-l-2 border-l-amber-500"
                    : "border-l-2 border-l-transparent"
                }`}
              >
                <div className="min-w-0">
                  <p
                    className={`text-sm font-medium truncate ${
                      isSelected ? "text-white" : "text-zinc-300"
                    }`}
                  >
                    {player.name}
                  </p>
                  <p className="text-xs text-zinc-600 mt-0.5">
                    {player.totalCards} card{player.totalCards !== 1 ? "s" : ""}
                  </p>
                </div>
                {player.hasRookie && (
                  <span className="shrink-0 text-xs font-bold text-amber-400 bg-amber-400/10 border border-amber-400/20 px-1.5 py-0.5 rounded">
                    Rookie
                  </span>
                )}
              </Link>
            );
          })
        )}
      </div>

      {/* Footer */}
      <div className="px-4 py-2.5 border-t border-zinc-800 shrink-0">
        <p className="text-xs text-zinc-700">{players.length} players total</p>
      </div>
    </aside>
  );
}
