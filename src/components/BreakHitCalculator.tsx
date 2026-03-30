"use client";

import { useState } from "react";

// ─── Box config: 2025 Topps Midnight UFC ──────────────────────────────────────
const BOXES_PER_CASE = 8;
const CARDS_PER_CASE = BOXES_PER_CASE * 1 * 7; // 56
const AUTOS_PER_BOX = 3;

// ─── Set-level constants (queried at build time, passed as props) ──────────────
export interface BreakSetConfig {
  totalAppearances: number;        // all player_appearances in set
  totalSerializedPrintRun: number; // SUM(appearances_in_insertSet × SUM(numbered_printRuns))
  totalAutoAppearances: number;    // appearances in auto/signature/graph/relic insert_sets
}

interface Props {
  playerTotalAppearances: number;
  playerSerializedPrintRun: number;  // player.totalPrintRun
  playerAutoAppearances: number;
  setConfig: BreakSetConfig;
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

function expectedHits(
  playerNum: number,
  setDenom: number,
  multiplier: number
): number | null {
  if (setDenom === 0 || playerNum === 0) return null;
  return (playerNum / setDenom) * multiplier;
}

function formatPct(expected: number): string {
  const pct = expected * 100;
  if (pct >= 100) return `${pct.toFixed(0)}%`;
  if (pct >= 10) return `${pct.toFixed(1)}%`;
  return `${pct.toFixed(2)}%`;
}

function formatOneIn(expected: number): string {
  if (expected >= 2) return `~${expected.toFixed(1)}× expected`;
  if (expected >= 1) return `~1 in 1`;
  const x = Math.round(1 / expected);
  return `~1 in ${x.toLocaleString()}`;
}

function oddsColor(expected: number | null, greyed: boolean): string {
  if (greyed || expected === null) return "text-zinc-600";
  const pct = expected * 100;
  if (pct >= 60) return "text-emerald-400";
  if (pct >= 10) return "text-amber-400";
  return "text-red-400";
}

function dotColor(expected: number | null, greyed: boolean): string {
  if (greyed || expected === null) return "bg-zinc-700";
  const pct = expected * 100;
  if (pct >= 60) return "bg-emerald-500";
  if (pct >= 10) return "bg-amber-500";
  return "bg-red-500";
}

// ─── Row ──────────────────────────────────────────────────────────────────────

function OddsRow({
  label,
  expected,
  greyed,
}: {
  label: string;
  expected: number | null;
  greyed: boolean;
}) {
  const active = !greyed && expected !== null;
  const color = oddsColor(expected, greyed);

  return (
    <div className={`flex items-center gap-3 py-2.5 ${greyed ? "opacity-40" : ""}`}>
      {/* Dot */}
      <span className={`shrink-0 w-2 h-2 rounded-full ${dotColor(expected, greyed)}`} />

      {/* Label */}
      <span className={`flex-1 text-sm font-medium ${greyed ? "text-zinc-600" : "text-zinc-300"}`}>
        {label}
      </span>

      {active ? (
        <>
          {/* Percentage */}
          <span className={`text-sm font-bold tabular-nums ${color}`}>
            {formatPct(expected!)}
          </span>
          {/* 1-in-X */}
          <span className="text-xs text-zinc-500 tabular-nums min-w-[7rem] text-right">
            {formatOneIn(expected!)}
          </span>
        </>
      ) : (
        <span className="text-xs text-zinc-700 italic">no cards</span>
      )}
    </div>
  );
}

// ─── Main component ───────────────────────────────────────────────────────────

export function BreakHitCalculator({
  playerTotalAppearances,
  playerSerializedPrintRun,
  playerAutoAppearances,
  setConfig,
}: Props) {
  const [cases, setCases] = useState(1);

  const boxesInBreak = cases * BOXES_PER_CASE;
  const cardsInBreak = cases * CARDS_PER_CASE;

  const anyCard = expectedHits(
    playerTotalAppearances,
    setConfig.totalAppearances,
    cardsInBreak
  );

  const serialized = expectedHits(
    playerSerializedPrintRun,
    setConfig.totalSerializedPrintRun,
    boxesInBreak
  );

  const auto = expectedHits(
    playerAutoAppearances,
    setConfig.totalAutoAppearances,
    AUTOS_PER_BOX * boxesInBreak
  );

  return (
    <div className="rounded-xl border border-zinc-700/60 bg-zinc-900 px-5 py-4">

      {/* Header */}
      <div className="flex items-center justify-between mb-1">
        <span className="text-xs font-semibold text-zinc-400 uppercase tracking-widest">
          Break Hit Calculator
        </span>

        {/* Case stepper */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => setCases((c) => Math.max(1, c - 1))}
            disabled={cases <= 1}
            className="w-6 h-6 flex items-center justify-center rounded border border-zinc-700 text-zinc-400 hover:border-zinc-500 hover:text-zinc-200 disabled:opacity-30 disabled:cursor-not-allowed transition-colors text-sm leading-none"
            aria-label="Decrease cases"
          >
            −
          </button>
          <span className="text-sm font-semibold text-white tabular-nums w-16 text-center">
            {cases === 1 ? "1 case" : `${cases} cases`}
          </span>
          <button
            onClick={() => setCases((c) => Math.min(20, c + 1))}
            disabled={cases >= 20}
            className="w-6 h-6 flex items-center justify-center rounded border border-zinc-700 text-zinc-400 hover:border-zinc-500 hover:text-zinc-200 disabled:opacity-30 disabled:cursor-not-allowed transition-colors text-sm leading-none"
            aria-label="Increase cases"
          >
            +
          </button>
        </div>
      </div>

      {/* Divider */}
      <div className="border-t border-zinc-800 mb-1" />

      {/* Odds rows */}
      <OddsRow
        label="Any Card"
        expected={anyCard}
        greyed={playerTotalAppearances === 0}
      />
      <div className="border-t border-zinc-800/60" />
      <OddsRow
        label="Numbered Parallel"
        expected={serialized}
        greyed={playerSerializedPrintRun === 0}
      />
      <div className="border-t border-zinc-800/60" />
      <OddsRow
        label="Autograph"
        expected={auto}
        greyed={playerAutoAppearances === 0}
      />

      {/* Disclaimer */}
      <p className="mt-3 text-xs text-zinc-700 leading-relaxed">
        Odds are estimates based on print runs and pack ratios
      </p>
    </div>
  );
}
