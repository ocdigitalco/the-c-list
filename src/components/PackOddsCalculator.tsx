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
  /** Packs per single box */
  packsPerBox: number;
  /** Guaranteed auto (or auto/relic) slots per box */
  guaranteedAutos: number;
  /** Override label for the Autograph row (e.g. "Autograph or Memorabilia") */
  autoRowLabel?: string;
  /** Disclaimer shown below the standard disclaimer */
  note?: string;
}

interface Props {
  slotsByFormat: Record<string, PackOddsSlot[]>;
  boxFormats: BoxFormat[];
  totalAutoCards: number;
  playerAutoCards: number;
}

// ─── Probability model ───────────────────────────────────────────────────────
//
// "Any Card" — per-pack expected hit rate, then compound across packs:
//   For each insert set the player appears in:
//     cards_per_pack = 1 / denom
//     player_share   = playerApps / totalApps
//     p_component    = cards_per_pack × player_share
//   p_per_pack = Σ p_component  (across base odds + all parallel odds)
//   P(box)     = 1 − (1 − p_per_pack)^packs_per_box
//
// "Numbered Parallel" — same model but only for:
//   - serialized parallels (print_run IS NOT NULL) with pack odds
//   - auto base odds (auto cards count as numbered)
//
// "Autograph" — guaranteed-slot model (not pack odds):
//   player_share = player_auto_cards / total_auto_cards_in_set
//   P(box)       = 1 − (1 − player_share)^guaranteed_auto_slots
//
// Ordering guarantee: Auto ≤ Numbered ≤ Any Card

interface OddsResult {
  pAny: number;
  pNumbered: number;
  pAuto: number;
  anyISCount: number;
  numberedCount: number;
  /** Whether this format has any usable pack odds for this player */
  hasPackOdds: boolean;
}

function computeOdds(
  slots: PackOddsSlot[],
  boxes: number,
  packsPerBox: number,
  guaranteedAutos: number,
  totalAutoCards: number,
  playerAutoCards: number,
): OddsResult {
  const totalPacks = boxes * packsPerBox;

  // ── Any Card: base odds + all parallel odds ──
  let pAnyPerPack = 0;
  let anyISCount = 0;

  for (const slot of slots) {
    if (slot.totalApps === 0) continue;
    const share = slot.playerApps / slot.totalApps;

    if (slot.baseOddsDenom !== null) {
      pAnyPerPack += share / slot.baseOddsDenom;
      anyISCount++;
    }
    for (const par of slot.serializedParallels) {
      if (par.denom === null) continue;
      pAnyPerPack += share / par.denom;
    }
  }

  // ── Numbered Parallel: numbered parallels + auto base ──
  let pNumPerPack = 0;
  let numberedCount = 0;

  for (const slot of slots) {
    if (slot.totalApps === 0) continue;
    const share = slot.playerApps / slot.totalApps;

    // Auto base odds count as numbered (auto cards are serialized hits)
    if (slot.isAuto && slot.baseOddsDenom !== null) {
      pNumPerPack += share / slot.baseOddsDenom;
    }
    for (const par of slot.serializedParallels) {
      if (par.denom === null) continue;
      pNumPerPack += share / par.denom;
      numberedCount++;
    }
  }

  // ── Convert per-pack rates to probability across all packs ──
  // Cap at 1.0 to avoid NaN from (1 - p)^n when p > 1
  const pAnyFromPacks = totalPacks > 0
    ? 1 - Math.pow(1 - Math.min(pAnyPerPack, 1), totalPacks)
    : 0;
  const pNumFromPacks = totalPacks > 0
    ? 1 - Math.pow(1 - Math.min(pNumPerPack, 1), totalPacks)
    : 0;

  // ── Autograph: guaranteed-slot model ──
  const autoShare = totalAutoCards > 0 ? playerAutoCards / totalAutoCards : 0;
  const autoSlots = guaranteedAutos * boxes;
  const pAuto = autoSlots > 0 && autoShare > 0
    ? 1 - Math.pow(1 - autoShare, autoSlots)
    : 0;

  // ── Combine pack-odds and guaranteed-slot probabilities ──
  // Auto slots also produce "any card" and "numbered" hits (auto cards are
  // serialized hits), so fold pAuto into the higher tiers to guarantee
  // the ordering constraint: Auto ≤ Numbered ≤ Any Card.
  const pNumbered = 1 - (1 - pNumFromPacks) * (1 - pAuto);
  const pAny = 1 - (1 - pAnyFromPacks) * (1 - pAuto);

  const hasPackOdds = pAnyPerPack > 0;

  return { pAny, pNumbered, pAuto, anyISCount, numberedCount, hasPackOdds };
}

// ─── Formatting ───────────────────────────────────────────────────────────────

function formatPct(p: number): string {
  if (p < 0.001) return "<0.1%";
  const pct = p * 100;
  if (pct >= 10) return `${pct.toFixed(1)}%`;
  return `${pct.toFixed(2)}%`;
}

function formatOneIn(p: number, unit: string): string {
  if (p <= 0) return "—";
  if (p >= 1) return `~${p.toFixed(1)}× per ${unit}`;
  const x = 1 / p;
  if (x < 2) return `~1 in 1 ${unit}s`;
  return `~1 in ${x.toFixed(x < 10 ? 1 : 0)} ${unit}s`;
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
  unit,
}: {
  label: string;
  p: number | null;
  greyed: boolean;
  breakdown?: string;
  unit: string;
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
              {formatOneIn(p!, unit)}
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

export function PackOddsCalculator({
  slotsByFormat,
  boxFormats,
  totalAutoCards,
  playerAutoCards,
}: Props) {
  const [boxes, setBoxes] = useState(1);
  const [fmtIdx, setFmtIdx] = useState(0);

  const fmt = boxFormats[fmtIdx] ?? boxFormats[0];
  const { boxesPerCase, packsPerBox, guaranteedAutos, autoRowLabel, note } = fmt;
  const showToggle = boxFormats.length > 1;
  const unit = boxes === 1 ? "box" : "box";

  const slots = slotsByFormat[fmt.label] ?? [];

  const { pAny, pNumbered, pAuto, anyISCount, numberedCount, hasPackOdds } =
    computeOdds(slots, boxes, packsPerBox, guaranteedAutos, totalAutoCards, playerAutoCards);

  const hasAny = pAny > 0;
  const hasNumbered = pNumbered > 0;
  const hasAuto = pAuto > 0;

  const anyBreakdown = hasAny
    ? `Based on pack odds across ${anyISCount} insert set${anyISCount !== 1 ? "s" : ""}`
    : undefined;

  const numberedBreakdown = hasNumbered
    ? `Based on pack odds across ${numberedCount} numbered parallel${numberedCount !== 1 ? "s" : ""}`
    : undefined;

  const autoBreakdown = hasAuto
    ? `${playerAutoCards} of ${totalAutoCards} auto cards · ${guaranteedAutos * boxes} guaranteed slot${guaranteedAutos * boxes !== 1 ? "s" : ""}`
    : undefined;

  return (
    <div className="rounded-xl border border-zinc-700/60 bg-zinc-900 px-5 py-4">
      {/* Box type toggle (only shown for multi-format sets) */}
      {showToggle && (
        <div className="flex gap-1 rounded-lg bg-zinc-800/60 p-0.5 mb-3">
          {boxFormats.map((f, i) => (
            <button
              key={f.label}
              onClick={() => { setFmtIdx(i); setBoxes(1); }}
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

        {/* Box stepper */}
        <div className="flex flex-col items-end gap-1">
          <div className="flex items-center gap-2">
            <button
              onClick={() => setBoxes((b) => Math.max(1, b - 1))}
              disabled={boxes <= 1}
              className="w-6 h-6 flex items-center justify-center rounded border border-zinc-700 text-zinc-400 hover:border-zinc-500 hover:text-zinc-200 disabled:opacity-30 disabled:cursor-not-allowed transition-colors text-sm leading-none"
              aria-label="Decrease boxes"
            >
              −
            </button>
            <span className="text-sm font-semibold text-white tabular-nums w-16 text-center">
              {boxes === 1 ? "1 box" : `${boxes} boxes`}
            </span>
            <button
              onClick={() => setBoxes((b) => Math.min(boxesPerCase * 5, b + 1))}
              disabled={boxes >= boxesPerCase * 5}
              className="w-6 h-6 flex items-center justify-center rounded border border-zinc-700 text-zinc-400 hover:border-zinc-500 hover:text-zinc-200 disabled:opacity-30 disabled:cursor-not-allowed transition-colors text-sm leading-none"
              aria-label="Increase boxes"
            >
              +
            </button>
          </div>
          <p className="text-xs text-zinc-600 tabular-nums">
            {boxes * packsPerBox === 1 ? "1 pack" : `${(boxes * packsPerBox).toLocaleString()} packs`}
            {boxes >= boxesPerCase && (
              <> · {Math.floor(boxes / boxesPerCase) === 1
                ? "1 case"
                : `${Math.floor(boxes / boxesPerCase)} cases`}
                {boxes % boxesPerCase > 0 && ` + ${boxes % boxesPerCase}`}
              </>
            )}
          </p>
        </div>
      </div>

      {/* Divider */}
      <div className="border-t border-zinc-800 mb-1" />

      {/* Odds rows */}
      {!hasPackOdds && !hasAuto ? (
        // Full empty state: no pack odds AND no auto odds
        <p className="py-4 text-center text-sm text-zinc-600">
          This player does not appear in {fmt.label} exclusive inserts.
        </p>
      ) : (
        <>
          {/* Any Card: may be empty for breaker formats where player has no matching inserts */}
          {!hasPackOdds ? (
            <div className="py-2.5">
              <p className="text-xs text-zinc-600 italic">
                This player does not appear in {fmt.label} exclusive inserts.
              </p>
            </div>
          ) : (
            <OddsRow
              label="Any Card"
              p={hasAny ? pAny : null}
              greyed={!hasAny}
              breakdown={anyBreakdown}
              unit={unit}
            />
          )}
          <div className="border-t border-zinc-800/60" />

          {!hasPackOdds ? (
            <div className="py-2.5 opacity-40">
              <div className="flex items-center gap-3">
                <span className="shrink-0 w-2 h-2 rounded-full bg-zinc-700" />
                <span className="flex-1 text-sm font-medium text-zinc-600">Numbered Parallel</span>
                <span className="text-xs text-zinc-700 italic">N/A for this format</span>
              </div>
            </div>
          ) : (
            <OddsRow
              label="Numbered Parallel"
              p={hasNumbered ? pNumbered : null}
              greyed={!hasNumbered}
              breakdown={numberedBreakdown}
              unit={unit}
            />
          )}
          <div className="border-t border-zinc-800/60" />

          {/* Auto always shown (based on guaranteed slots, not pack odds) */}
          <OddsRow
            label={autoRowLabel ?? "Autograph"}
            p={hasAuto ? pAuto : null}
            greyed={!hasAuto}
            breakdown={autoBreakdown}
            unit={unit}
          />
        </>
      )}

      {/* Disclaimer */}
      <p className="mt-3 text-xs text-zinc-700 leading-relaxed">
        Any Card and Numbered Parallel based on official pack ratios.
        Autograph based on {guaranteedAutos} guaranteed slot{guaranteedAutos !== 1 ? "s" : ""} per box ({totalAutoCards} total auto cards in set).
      </p>
      {note && (
        <p className="mt-1.5 text-xs text-zinc-600 leading-relaxed">{note}</p>
      )}
    </div>
  );
}
