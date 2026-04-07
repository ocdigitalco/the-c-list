"use client";

import { BreakSheetModal, type BreakSheetPlayer } from "@/components/BreakSheetModal";

interface Props {
  setName: string;
  sport: string;
  league: string | null;
  tier: string;
  athleteCount: number;
  breakSheetPlayers: BreakSheetPlayer[];
}

export function SetMetadataBar({ setName, sport, league, tier, athleteCount, breakSheetPlayers }: Props) {
  return (
    <div>
      <h1 className="text-3xl font-bold" style={{ color: "var(--v2-text-primary)" }}>
        {setName}
      </h1>
      <div className="flex flex-wrap items-center gap-2 mt-3">
        <span
          className="text-base font-medium px-4 py-1 rounded-md"
          style={{ border: "1px solid var(--v2-border)", color: "var(--v2-text-primary)" }}
        >
          {sport}
        </span>
        {league && (
          <span
            className="text-base font-medium px-4 py-1 rounded-md"
            style={{ border: "1px solid var(--v2-border)", color: "var(--v2-text-primary)" }}
          >
            {league}
          </span>
        )}
        {tier && tier !== "Standard" && (
          <span
            className="text-base font-medium px-4 py-1 rounded-md"
            style={{ background: "var(--v2-accent-light)", color: "var(--v2-accent)", border: "1px solid var(--v2-accent)" }}
          >
            {tier}
          </span>
        )}
        <span
          className="text-base font-medium px-4 py-1 rounded-md"
          style={{ border: "1px solid var(--v2-border)", color: "var(--v2-text-secondary)" }}
        >
          {athleteCount.toLocaleString()} Athletes
        </span>
        <div className="v2-break-sheet-pill">
          <style>{`
            .v2-break-sheet-pill > button {
              background: var(--v2-break-sheet-bg, #111827) !important;
              color: #FFFFFF !important;
              font-size: 1rem !important;
              font-weight: 500 !important;
              padding: 0.25rem 1rem !important;
              border-radius: 0.375rem !important;
              border: none !important;
              line-height: 1.5 !important;
              cursor: pointer !important;
              transition: background 150ms ease, box-shadow 150ms ease !important;
            }
            .v2-break-sheet-pill > button:hover {
              background: var(--v2-break-sheet-hover-bg, #1F2937) !important;
              box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
            }
          `}</style>
          <BreakSheetModal
            setName={setName}
            sport={sport}
            league={league}
            players={breakSheetPlayers}
          />
        </div>
      </div>
    </div>
  );
}
