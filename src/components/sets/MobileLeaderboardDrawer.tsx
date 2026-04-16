"use client";

import { useState, useEffect } from "react";
import { LeaderboardSidebar } from "./LeaderboardSidebar";
import type { LeaderboardRow } from "./types";

interface Props {
  entries: LeaderboardRow[];
  hasTeamData: boolean;
  setId: number;
  setSlug?: string | null;
}

export function MobileLeaderboardDrawer({ entries, hasTeamData, setId, setSlug }: Props) {
  const [open, setOpen] = useState(false);

  useEffect(() => {
    if (!open) return;
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") setOpen(false);
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open]);

  return (
    <>
      <button
        onClick={() => setOpen(true)}
        className="flex items-center gap-1.5 text-sm font-medium px-2.5 py-1.5 rounded-lg transition-colors shrink-0"
        style={{
          background: "var(--v2-card-bg)",
          border: "1px solid var(--v2-border)",
          color: "var(--v2-text-secondary)",
        }}
      >
        <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 0 1 3 19.875v-6.75ZM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V8.625ZM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V4.125Z" />
        </svg>
        Leaderboard
      </button>

      {open && (
        <div className="fixed inset-0 z-50">
          <div className="absolute inset-0 bg-black/50" onClick={() => setOpen(false)} />
          <div
            className="absolute top-0 left-0 h-full w-full md:w-[320px] md:max-w-[85vw] shadow-2xl"
            style={{ background: "var(--v2-sidebar-bg)" }}
          >
            <div className="flex items-center justify-end px-3 pt-3">
              <button
                onClick={() => setOpen(false)}
                className="p-1.5 rounded-md transition-colors"
                style={{ color: "var(--v2-text-secondary)" }}
                aria-label="Close"
              >
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6 18 18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div className="h-[calc(100%-44px)]">
              <LeaderboardSidebar entries={entries} hasTeamData={hasTeamData} setId={setId} setSlug={setSlug} />
            </div>
          </div>
        </div>
      )}
    </>
  );
}
