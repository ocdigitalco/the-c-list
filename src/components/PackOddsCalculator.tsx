"use client";

import { useState } from "react";

// ─── Types ────────────────────────────────────────────────────────────────────

export interface PackOddsSlot {
  insertSetName: string;
  playerApps: number;
  totalApps: number;       // total distinct players in this insert set
  baseOddsDenom: number | null;
  isAuto: boolean;
  serializedParallels: {
    name: string;
    printRun: number;
    denom: number | null;
  }[];
}

export interface BoxFormat {
  label: string;
  boxesPerCase: number;
  /** Total packs per case (boxes_per_case × packs_per_box) */
  packsPerCase: number;
  /** Override label for the Autograph row (e.g. "Autograph or Memorabilia") */
  autoRowLabel?: string;
  /** Disclaimer shown below the standard disclaimer */
  note?: string;
}

interface Props {
  slotsByFormat: Record<string, PackOddsSlot[]>;
  boxFormats: BoxFormat[];
}

// ─── Formula ──────────────────────────────────────────────────────────────────
//
//   player_share = 1 / totalApps
//   P_i = 1 − (1 − player_share / denom)^total_packs
//
// Numbered Parallel:
//   - Auto IS:     use baseOddsDenom (auto slot IS the numbered card)
//   - Non-auto IS: use per-parallel denom
// Auto:     per auto IS using base insert set odds (same formula as above)
// Any Card: pNumbered (auto contributions already subsumed in numbered)

function computeOdds(slots: PackOddsSlot[], cases: number, packsPerCase: number) {
  const totalPacks = cases * packsPerCase;

  let pNumberedComplement = 1;
  let pAutoComplement = 1;
  let numberedCount = 0;
  let autoISCount = 0;

  for (const slot of slots) {
    if (slot.totalApps === 0) continue;

    if (slot.isAuto && slot.baseOddsDenom !== null) {
      // Auto IS: totalApps = distinct cards in the set; playerApps = cards this player appears on.
      // Handles multi-player autos (Dual/Triple/Quad) where each card has multiple signers.
      const pHit = 1 - Math.pow(1 - slot.playerApps / (slot.totalApps * slot.baseOddsDenom), totalPacks);
      pNumberedComplement *= 1 - pHit;
      pAutoComplement *= 1 - pHit;
      numberedCount++;
      autoISCount++;
    } else {
      // Non-auto IS: use per-parallel denoms for numbered only
      for (const par of slot.serializedParallels) {
        if (par.denom === null) continue;
        const pHit = 1 - Math.pow(1 - 1 / (slot.totalApps * par.denom), totalPacks);
        pNumberedComplement *= 1 - pHit;
        numberedCount++;
      }
    }
  }

  const pNumbered = 1 - pNumberedComplement;
  const pAuto = 1 - pAutoComplement;
  // pAny = pNumbered: auto contributions are already included in numbered, no double-count
  const pAny = pNumbered;

  return { pNumbered, pAuto, pAny, numberedCount, autoISCount };
}

// ─── Formatting ───────────────────────────────────────────────────────────────

function formatPct(p: number): string {
  if (p < 0.001) return "<0.1%";
  const pct = p * 100;
  if (pct >= 10) return `${pct.toFixed(1)}%`;
  return `${pct.toFixed(2)}%`;
}

function formatOneIn(p: number): string {
  if (p <= 0) return "—";
  if (p >= 1) return `~${p.toFixed(1)}× per case`;
  const x = 1 / p;
  if (x < 2) return "~1 in 1 cases";
  return `~1 in ${x.toFixed(x < 10 ? 1 : 0)} cases`;
}

function oddsColor(p: number): string {
  const pct = p * 100;
  if (pct >= 60) return "text-emerald-400";
  if (pct >= 10) return "text-amber-400";
  return "text-red-400";
}

function dotColor(p: number): string {
  const pct = p * 100;
  if (pct >= 60) return "bg-emerald-500";
  if (pct >= 10) return "bg-amber-500";
  return "bg-red-500";
}

// ─── Row ──────────────────────────────────────────────────────────────────────

function OddsRow({
  label,
  p,
  greyed,
  breakdown,
}: {
  label: string;
  p: number | null;
  greyed: boolean;
  breakdown?: string;
}) {
  const active = !greyed && p !== null && p > 0;

  return (
    <div className={`py-2.5 ${greyed ? "opacity-40" : ""}`}>
      <div className="flex items-center gap-3">
        <span
          className={`shrink-0 w-2 h-2 rounded-full ${
            active ? dotColor(p!) : "bg-zinc-700"
          }`}
        />
        <span
          className={`flex-1 text-sm font-medium ${
            greyed ? "text-zinc-600" : "text-zinc-300"
          }`}
        >
          {label}
        </span>
        {active ? (
          <>
            <span className={`text-sm font-bold tabular-nums ${oddsColor(p!)}`}>
              {formatPct(p!)}
            </span>
            <span className="text-xs text-zinc-500 tabular-nums min-w-[8rem] text-right">
              {formatOneIn(p!)}
            </span>
          </>
        ) : (
          <span className="text-xs text-zinc-700 italic">Pack odds not available</span>
        )}
      </div>
      {active && breakdown && (
        <p className="mt-0.5 ml-5 text-xs text-zinc-600 leading-snug">{breakdown}</p>
      )}
    </div>
  );
}

// ─── Main component ───────────────────────────────────────────────────────────

export function PackOddsCalculator({ slotsByFormat, boxFormats }: Props) {
  const [cases, setCases] = useState(1);
  const [fmtIdx, setFmtIdx] = useState(0);

  const fmt = boxFormats[fmtIdx] ?? boxFormats[0];
  const { boxesPerCase, packsPerCase, autoRowLabel, note } = fmt;
  const showToggle = boxFormats.length > 1;

  const slots = slotsByFormat[fmt.label] ?? [];
  const { pNumbered, pAuto, pAny, numberedCount, autoISCount } = computeOdds(slots, cases, packsPerCase);

  const hasNumbered = pNumbered > 0;
  const hasAuto = pAuto > 0;

  const numberedBreakdown = hasNumbered
    ? `Based on pack odds across ${numberedCount} insert set${numberedCount !== 1 ? "s" : ""}`
    : undefined;

  const autoBreakdown = hasAuto
    ? `Based on pack odds across ${autoISCount} auto insert set${autoISCount !== 1 ? "s" : ""}`
    : undefined;

  return (
    <div className="rounded-xl border border-zinc-700/60 bg-zinc-900 px-5 py-4">
      {/* Box type toggle (only shown for multi-format sets) */}
      {showToggle && (
        <div className="flex gap-1 rounded-lg bg-zinc-800/60 p-0.5 mb-3">
          {boxFormats.map((f, i) => (
            <button
              key={f.label}
              onClick={() => setFmtIdx(i)}
              className={`flex-1 text-xs py-1.5 rounded-md font-semibold transition-colors ${
                i === fmtIdx
                  ? "bg-zinc-700 text-white"
                  : "text-zinc-500 hover:text-zinc-300"
              }`}
            >
              {f.label}
            </button>
          ))}
        </div>
      )}

      {/* Header */}
      <div className="flex items-center justify-between mb-1">
        <span className="text-xs font-semibold text-zinc-400 uppercase tracking-widest">
          Break Hit Calculator
        </span>

        {/* Case stepper */}
        <div className="flex flex-col items-end gap-1">
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
          <p className="text-xs text-zinc-600 tabular-nums">
            {cases * boxesPerCase === 1 ? "1 box" : `${cases * boxesPerCase} boxes`}
            {" = "}
            {cases * packsPerCase === 1 ? "1 pack" : `${(cases * packsPerCase).toLocaleString()} packs`}
          </p>
        </div>
      </div>

      {/* Divider */}
      <div className="border-t border-zinc-800 mb-1" />

      {/* Odds rows */}
      <OddsRow
        label="Any Card"
        p={hasNumbered || hasAuto ? pAny : null}
        greyed={!hasNumbered && !hasAuto}
      />
      <div className="border-t border-zinc-800/60" />
      <OddsRow
        label="Numbered Parallel"
        p={hasNumbered ? pNumbered : null}
        greyed={!hasNumbered}
        breakdown={numberedBreakdown}
      />
      <div className="border-t border-zinc-800/60" />
      <OddsRow
        label={autoRowLabel ?? "Autograph"}
        p={hasAuto ? pAuto : null}
        greyed={!hasAuto}
        breakdown={autoBreakdown}
      />

      {/* Disclaimer */}
      <p className="mt-3 text-xs text-zinc-700 leading-relaxed">
        Odds based on official pack ratios and serialized print runs. Unnumbered cards excluded.
      </p>
      {note && (
        <p className="mt-1.5 text-xs text-zinc-600 leading-relaxed">{note}</p>
      )}
    </div>
  );
}
