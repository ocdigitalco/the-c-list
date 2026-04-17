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
  /** Total packs in the entire production run (when known) — used for exact odds on numbered cards */
  totalPacksProduced?: number;
}

interface Props {
  slotsByFormat: Record<string, PackOddsSlot[]>;
  boxFormats: BoxFormat[];
  totalAutoCards: number;
  playerAutoCards: number;
  setId?: number;
  setName?: string;
}

// ─── SP/SSP configuration ────────────────────────────────────────────────────
// Insert sets designated as short-print / super-short-print chase inserts.
// Scoped per set name — only sets listed here will show the SP/SSP row.

const SP_SSP_CONFIG: Record<string, string[]> = {
  "2025 Topps Chrome Football": [
    "Helix",
    "Game Genies",
    "Kaiju",
    "Let's Go",
    "Ultra Violet",
    "Lightning Leaders",
  ],
};

interface SpSspResult {
  hasSpSsp: boolean;
  pSpSsp: number;
  insertSetNames: string[];
  availableInBoxType: boolean;
}

function computeSpSsp(
  slots: PackOddsSlot[],
  spSspNames: string[],
  boxes: number,
  packsPerBox: number,
): SpSspResult {
  const nameSet = new Set(spSspNames.map((n) => n.toLowerCase()));
  const matchingSlots = slots.filter((s) =>
    nameSet.has(s.insertSetName.toLowerCase())
  );

  const insertSetNames = matchingSlots.map((s) => s.insertSetName);
  if (matchingSlots.length === 0) {
    return { hasSpSsp: false, pSpSsp: 0, insertSetNames: [], availableInBoxType: false };
  }

  // Check if any matching slot has pack odds for this box type
  const hasOdds = matchingSlots.some((s) => s.baseOddsDenom !== null);
  if (!hasOdds) {
    return { hasSpSsp: true, pSpSsp: 0, insertSetNames, availableInBoxType: false };
  }

  // Compute per-pack probability across all SP/SSP insert sets
  let pPerPack = 0;
  for (const slot of matchingSlots) {
    if (slot.totalApps === 0 || slot.baseOddsDenom === null) continue;
    const share = slot.playerApps / slot.totalApps;
    pPerPack += share / slot.baseOddsDenom;
  }

  const totalPacks = boxes * packsPerBox;
  const pSpSsp = totalPacks > 0 && pPerPack > 0
    ? 1 - Math.pow(1 - Math.min(pPerPack, 1), totalPacks)
    : 0;

  return { hasSpSsp: true, pSpSsp, insertSetNames, availableInBoxType: true };
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
  /** True when auto odds are computed from pack odds (no guaranteed slots) */
  autoFromPackOdds: boolean;
  /** Number of auto insert sets with pack odds (only when autoFromPackOdds) */
  autoISCount: number;
}

function computeOdds(
  slots: PackOddsSlot[],
  boxes: number,
  packsPerBox: number,
  guaranteedAutos: number,
  totalAutoCards: number,
  playerAutoCards: number,
  totalPacksProduced?: number,
): OddsResult {
  const totalPacks = boxes * packsPerBox;

  // Helper: per-pack probability for a numbered parallel.
  // When total production run is known, use exact formula:
  //   p = (playerApps × printRun) / totalPacksProduced
  // Otherwise fall back to pack-odds ratio:
  //   p = (playerApps / totalApps) / denom
  function parPerPack(
    playerApps: number,
    totalApps: number,
    printRun: number,
    denom: number | null,
  ): number {
    if (totalPacksProduced && totalPacksProduced > 0) {
      return (playerApps * printRun) / totalPacksProduced;
    }
    if (denom === null) return 0;
    return (playerApps / totalApps) / denom;
  }

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
      const pp = parPerPack(slot.playerApps, slot.totalApps, par.printRun, par.denom);
      if (pp <= 0) continue;
      pAnyPerPack += pp;
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
      const pp = parPerPack(slot.playerApps, slot.totalApps, par.printRun, par.denom);
      if (pp <= 0) continue;
      pNumPerPack += pp;
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

  // ── Autograph ──
  // Two models depending on whether the set guarantees auto slots per box:
  //   1) Guaranteed-slot model: P = 1 − (1 − playerAutoCards/totalAutoCards)^slots
  //   2) Pack-odds model (no guaranteed autos): sum auto base+parallel odds per
  //      pack, then compound across packs. Auto odds are already included in
  //      pAnyPerPack and pNumPerPack, so no folding needed.
  let pAuto: number;
  let autoFromPackOdds = false;
  let autoISCount = 0;

  if (guaranteedAutos > 0) {
    // Guaranteed-slot model
    const autoShare = totalAutoCards > 0 ? playerAutoCards / totalAutoCards : 0;
    const autoSlots = guaranteedAutos * boxes;
    pAuto = autoSlots > 0 && autoShare > 0
      ? 1 - Math.pow(1 - autoShare, autoSlots)
      : 0;
  } else {
    // Pack-odds model: compute auto probability from pack odds directly
    autoFromPackOdds = true;
    let pAutoPerPack = 0;
    for (const slot of slots) {
      if (!slot.isAuto || slot.totalApps === 0) continue;
      const share = slot.playerApps / slot.totalApps;
      if (slot.baseOddsDenom !== null) {
        pAutoPerPack += share / slot.baseOddsDenom;
        autoISCount++;
      }
      for (const par of slot.serializedParallels) {
        const pp = parPerPack(slot.playerApps, slot.totalApps, par.printRun, par.denom);
        if (pp <= 0) continue;
        pAutoPerPack += pp;
      }
    }
    pAuto = totalPacks > 0 && pAutoPerPack > 0
      ? 1 - Math.pow(1 - Math.min(pAutoPerPack, 1), totalPacks)
      : 0;
  }

  // ── Combine pack-odds and guaranteed-slot probabilities ──
  // When using guaranteed-slot auto model, auto slots produce hits independent
  // of pack odds, so fold pAuto into the higher tiers to maintain ordering:
  //   Auto ≤ Numbered ≤ Any Card.
  // When using pack-odds auto model, auto odds are already included in
  // pAnyPerPack and pNumPerPack, so no folding needed — ordering holds naturally.
  let pNumbered: number;
  let pAny: number;
  if (autoFromPackOdds) {
    pNumbered = pNumFromPacks;
    pAny = pAnyFromPacks;
  } else {
    pNumbered = 1 - (1 - pNumFromPacks) * (1 - pAuto);
    pAny = 1 - (1 - pAnyFromPacks) * (1 - pAuto);
  }

  const hasPackOdds = pAnyPerPack > 0;

  return { pAny, pNumbered, pAuto, anyISCount, numberedCount, hasPackOdds, autoFromPackOdds, autoISCount };
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
  setId,
  setName,
}: Props) {
  const [boxes, setBoxes] = useState(1);
  const [fmtIdx, setFmtIdx] = useState(0);

  const fmt = boxFormats[fmtIdx] ?? boxFormats[0];
  const { boxesPerCase, packsPerBox, guaranteedAutos, autoRowLabel, note, totalPacksProduced } = fmt;
  const showToggle = boxFormats.length > 1;
  const unit = boxes === 1 ? "box" : "box";

  const slots = slotsByFormat[fmt.label] ?? [];

  // Premium-only formats are box types that physically cannot contain base cards.
  // Only these formats may show the "exclusive inserts" message.
  const PREMIUM_ONLY_FORMATS = ["Breaker's Delight"];
  const isPremiumOnly = PREMIUM_ONLY_FORMATS.includes(fmt.label);

  const { pAny, pNumbered, pAuto, anyISCount, numberedCount, hasPackOdds, autoFromPackOdds, autoISCount } =
    computeOdds(slots, boxes, packsPerBox, guaranteedAutos, totalAutoCards, playerAutoCards, totalPacksProduced);

  // ── Sanity check: SuperFractor (print_run=1) odds validation ──
  if (typeof window !== "undefined" && totalPacksProduced && boxes === 1) {
    for (const slot of slots) {
      for (const par of slot.serializedParallels) {
        if (par.printRun !== 1) continue;
        const expectedPerBox = (slot.playerApps * 1) / totalPacksProduced * packsPerBox;
        const expectedOneIn = 1 / expectedPerBox;
        const totalBoxes = totalPacksProduced / packsPerBox;
        if (Math.abs(expectedOneIn - totalBoxes) / totalBoxes > 0.01) {
          console.warn(
            `[BreakHitCalc] SuperFractor sanity check failed for "${slot.insertSetName} ${par.name}": ` +
            `expected ~1:${totalBoxes.toFixed(0)} per box, got ~1:${expectedOneIn.toFixed(0)}`
          );
        }
      }
    }
  }

  // ── SP/SSP ──
  const spSspNames = setName ? SP_SSP_CONFIG[setName] : undefined;
  const spSsp = spSspNames
    ? computeSpSsp(slots, spSspNames, boxes, packsPerBox)
    : { hasSpSsp: false, pSpSsp: 0, insertSetNames: [] as string[], availableInBoxType: false };

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
    ? autoFromPackOdds
      ? `Based on pack odds across ${autoISCount} auto insert set${autoISCount !== 1 ? "s" : ""}`
      : `${playerAutoCards} of ${totalAutoCards} auto cards · ${guaranteedAutos * boxes} guaranteed slot${guaranteedAutos * boxes !== 1 ? "s" : ""}`
    : undefined;

  return (
    <div className="rounded-xl border border-zinc-700/60 bg-zinc-900 px-5 py-4">
      {/* Box type toggle (only shown for multi-format sets) */}
      {showToggle && (
        <div className="flex gap-1 rounded-lg bg-zinc-800/60 p-0.5 mb-3 overflow-x-auto">
          {boxFormats.map((f, i) => (
            <button
              key={f.label}
              onClick={() => { setFmtIdx(i); setBoxes(1); }}
              className="shrink-0 flex-1 text-xs py-1.5 px-2 rounded-md font-semibold transition-colors"
              style={
                i === fmtIdx
                  ? { background: "#6366f1", color: "#fff" }
                  : { color: "#71717a" }
              }
            >
              {f.label}
            </button>
          ))}
        </div>
      )}

      {/* Header */}
      <div className="flex items-center justify-between mb-1">
        <div>
          <span className="text-xs font-semibold text-zinc-400 uppercase tracking-widest">
            Break Hit Calculator
          </span>
          <div className="flex items-center gap-3 mt-0.5">
            <a
              href="/resources/break-hit-calculator"
              className="text-[12px] text-zinc-600 hover:text-zinc-400 hover:underline transition-colors"
            >
              How is this calculated?
            </a>
          </div>
        </div>

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
      {isPremiumOnly && !hasPackOdds && !hasAuto ? (
        // Full empty state: premium-only format with no matching inserts or autos
        <p className="py-4 text-center text-sm text-zinc-600">
          This player does not appear in {fmt.label} exclusive inserts.
        </p>
      ) : (
        <>
          <OddsRow
            label="Any Card"
            p={hasAny ? pAny : null}
            greyed={!hasAny}
            breakdown={anyBreakdown}
            unit={unit}
          />
          <div className="border-t border-zinc-800/60" />

          <OddsRow
            label="Numbered Parallel"
            p={hasNumbered ? pNumbered : null}
            greyed={!hasNumbered}
            breakdown={numberedBreakdown}
            unit={unit}
          />
          <div className="border-t border-zinc-800/60" />

          {/* Auto always shown (based on guaranteed slots, not pack odds) */}
          <OddsRow
            label={autoRowLabel ?? "Autograph"}
            p={hasAuto ? pAuto : null}
            greyed={!hasAuto}
            breakdown={autoBreakdown}
            unit={unit}
          />

          {/* SP/SSP row — only for sets with configured SP/SSP insert sets */}
          {spSsp.hasSpSsp && (
            <>
              <div className="border-t border-zinc-800/60" />
              {spSsp.availableInBoxType ? (
                <OddsRow
                  label="SP/SSP"
                  p={spSsp.pSpSsp > 0 ? spSsp.pSpSsp : null}
                  greyed={spSsp.pSpSsp <= 0}
                  breakdown={spSsp.insertSetNames.join(" · ")}
                  unit={unit}
                />
              ) : (
                <div className="py-2.5">
                  <div className="flex items-center gap-3">
                    <span className="shrink-0 w-2 h-2 rounded-full bg-zinc-700" />
                    <span className="flex-1 text-sm font-medium text-zinc-300">SP/SSP</span>
                    <span className="text-xs text-zinc-700 italic">Unavailable in this box type</span>
                  </div>
                  <p className="mt-0.5 ml-5 text-xs text-zinc-600 leading-snug">
                    {spSsp.insertSetNames.join(" · ")}
                  </p>
                </div>
              )}
            </>
          )}
        </>
      )}

      {/* Disclaimer */}
      <p className="mt-3 text-xs text-zinc-700 leading-relaxed">
        {autoFromPackOdds
          ? "All probabilities based on official pack ratios."
          : `Any Card and Numbered Parallel based on official pack ratios. Autograph based on ${guaranteedAutos} guaranteed slot${guaranteedAutos !== 1 ? "s" : ""} per box (${totalAutoCards} total auto cards in set).`}
      </p>
      {note && (
        <p className="mt-1.5 text-xs text-zinc-600 leading-relaxed">{note}</p>
      )}
    </div>
  );
}
