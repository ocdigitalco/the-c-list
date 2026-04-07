"use client";

import { useState } from "react";

// ─── Types ────────────────────────────────────────────────────────────────────

export interface BreakSheetPlayer {
  id: number;
  name: string;
  /** Count of distinct PURE-AUTO insert sets (excludes mem-auto sets) */
  autoCount: number;
  /** Has any autograph+memorabilia/relic insert set appearance */
  hasMemAuto: boolean;
  /** Has any relic/memorabilia-only (non-auto) insert set appearance */
  hasRelic: boolean;
  isRookie: boolean;
  /** Non-auto, non-relic, non-base insert set names (for abbreviation tags) */
  insertSetNames: string[];
}

interface Labels {
  auto: string;
  memAuto: string;
  relic: string;
  rookie: string;
}

interface Props {
  setName: string;
  sport: string;
  league: string | null;
  players: BreakSheetPlayer[];
}

type LabelMode = "long" | "short";

// ─── Constants ────────────────────────────────────────────────────────────────

const SPORT_CATEGORY: Record<string, string> = {
  Baseball:   "MLB Breaks",
  Basketball: "NBA Breaks",
  Football:   "NFL Breaks",
  Soccer:     "Soccer Breaks",
  Hockey:     "Hockey Breaks",
  MMA:        "UFC Breaks",
  Wrestling:  "WWE Breaks",
  Racing:     "F1 Breaks",
  Olympics:   "Olympics Breaks",
  Golf:       "Golf Breaks",
};

const CSV_HEADER =
  "Category,Sub Category,Title,Description,Quantity,Type,Price," +
  "Shipping Profile,Offerable,Hazmat,Condition,Cost Per Item,SKU," +
  "Image URL 1,Image URL 2,Image URL 3,Image URL 4," +
  "Image URL 5,Image URL 6,Image URL 7,Image URL 8";

const PREVIEW_COUNT = 5;

// ─── Helpers ──────────────────────────────────────────────────────────────────

/** First-letter abbreviation of significant words, max 5 chars. */
function abbreviate(name: string): string {
  const stop = new Set(["a", "an", "the", "of", "in", "at", "for", "and", "or"]);
  const words = name.split(/\s+/).filter((w) => !stop.has(w.toLowerCase()));
  if (words.length === 0) return name.slice(0, 5).toUpperCase();
  if (words.length === 1) return words[0].slice(0, 4).toUpperCase();
  return words.map((w) => w[0].toUpperCase()).join("").slice(0, 5);
}

/** Wrap CSV field value in quotes if it contains commas, quotes, or newlines. */
function csvEsc(v: string): string {
  if (v.includes(",") || v.includes('"') || v.includes("\n") || v.includes("\r")) {
    return `"${v.replace(/"/g, '""')}"`;
  }
  return v;
}

function buildTitle(player: BreakSheetPlayer, labels: Labels, labelMode: LabelMode): string {
  if (labelMode === "short") {
    return buildShortTitle(player);
  }
  return buildLongTitle(player, labels);
}

function buildLongTitle(player: BreakSheetPlayer, labels: Labels): string {
  const tags: string[] = [];

  if (player.autoCount > 0) {
    tags.push(player.autoCount > 1 ? `${labels.auto}x${player.autoCount}` : labels.auto);
  }
  if (player.hasMemAuto) {
    tags.push(labels.memAuto);
  }
  if (player.hasRelic) {
    tags.push(labels.relic);
  }
  if (player.isRookie) {
    tags.push(labels.rookie);
  }
  for (const name of player.insertSetNames) {
    tags.push(abbreviate(name));
  }

  if (tags.length === 0) return player.name;
  return `${player.name} ${tags.map((t) => `(${t})`).join("")}`;
}

function buildShortTitle(player: BreakSheetPlayer): string {
  const parts: string[] = [];

  if (player.isRookie) parts.push("RC");
  if (player.autoCount > 0 || player.hasMemAuto) parts.push("AUTO");

  // Count numbered parallels from insert set names — use relic as proxy for parallels
  // In short mode: relic → counted as parallel-like
  const parallelCount = player.insertSetNames.length;
  if (player.hasRelic && parallelCount === 0) {
    // Just a relic, show as parallel
    parts.push("1 PARALLEL");
  } else if (parallelCount > 0) {
    parts.push(parallelCount === 1 ? "1 PARALLEL" : `${parallelCount} PARALLELS`);
  }

  if (parts.length === 0) return player.name;
  return `${player.name} (${parts.join(" ")})`;
}

// ─── Component ────────────────────────────────────────────────────────────────

export function BreakSheetModal({ setName, sport, league, players }: Props) {
  const [open, setOpen] = useState(false);
  const [description, setDescription] = useState("");
  const [listingType, setListingType] = useState<"Buy it Now" | "Auction">("Buy it Now");
  const [labelMode, setLabelMode] = useState<LabelMode>("long");
  const [giveaways, setGiveaways] = useState(0);
  const [buyersGiveaway, setBuyersGiveaway] = useState(false);
  const [labels, setLabels] = useState<Labels>({
    auto: "AUTO",
    memAuto: "MEM AUTO",
    relic: "RELIC",
    rookie: "RC",
  });

  const category = SPORT_CATEGORY[sport] ?? `${sport} Breaks`;
  const subCategory = league ?? sport;

  function buildRow(title: string): string {
    const fields = [
      category,
      subCategory,
      title,
      description,
      "1",
      listingType,
      "",          // Price
      "",          // Shipping Profile
      "TRUE",      // Offerable
      "Not Hazmat",
      "New",       // Condition
      "",          // Cost Per Item
      "",          // SKU
      "", "", "", "", "", "", "", "", // Image URLs 1–8
    ];
    return fields.map(csvEsc).join(",");
  }

  function buildPlayerRow(player: BreakSheetPlayer): string {
    return buildRow(buildTitle(player, labels, labelMode));
  }

  function downloadCSV() {
    const dataRows: string[] = [];

    // Buyers Giveaway at the top
    if (buyersGiveaway) {
      dataRows.push(buildRow("Buyers Giveaway"));
    }

    // Player rows
    for (const p of players) {
      dataRows.push(buildPlayerRow(p));
    }

    // Giveaway rows at the end
    for (let i = 0; i < giveaways; i++) {
      dataRows.push(buildRow("Giveaway"));
    }

    const rows = [CSV_HEADER, ...dataRows];
    const blob = new Blob(["\uFEFF" + rows.join("\r\n")], {
      type: "text/csv;charset=utf-8;",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${setName} - Break Sheet.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  const totalRows = players.length + giveaways + (buyersGiveaway ? 1 : 0);
  const previewPlayers = players.slice(0, PREVIEW_COUNT);

  return (
    <>
      {/* ── Trigger button ── */}
      <button
        onClick={() => setOpen(true)}
        className="flex items-center gap-1.5 shrink-0 text-base font-medium text-zinc-400 hover:text-white border border-zinc-700 hover:border-zinc-500 bg-zinc-900 hover:bg-zinc-800 px-3 py-1.5 rounded-md transition-colors"
      >
        <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
        </svg>
        Break Sheet
      </button>

      {/* ── Modal ── */}
      {open && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center p-4"
          style={{ background: "rgba(0,0,0,0.75)" }}
          onClick={(e) => { if (e.target === e.currentTarget) setOpen(false); }}
        >
          <div className="relative bg-zinc-900 border border-zinc-700 rounded-2xl w-full max-w-2xl mx-4 max-h-[90vh] overflow-y-auto shadow-2xl">

            {/* Header */}
            <div className="sticky top-0 bg-zinc-900 flex items-center justify-between px-5 py-3 border-b border-zinc-800 rounded-t-2xl z-10">
              <div>
                <h2 className="text-base font-semibold text-white">Break Sheet Builder</h2>
                <p className="text-base text-zinc-500 mt-0.5">{setName} · {players.length.toLocaleString()} athletes</p>
              </div>
              <button
                onClick={() => setOpen(false)}
                className="p-1.5 rounded-md text-zinc-500 hover:text-white hover:bg-zinc-800 transition-colors"
                aria-label="Close"
              >
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6 18 18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Body */}
            <div className="px-5 py-4 space-y-3">

              {/* Break Description */}
              <div>
                <label className="block text-base font-medium text-zinc-400 mb-1">
                  Break Description
                </label>
                <input
                  type="text"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder={`e.g. "3 Cases! ${setName}"`}
                  className="w-full bg-zinc-800 border border-zinc-700 text-base text-white placeholder-zinc-600 rounded-lg px-3 py-1.5 outline-none focus:border-zinc-500 transition-colors"
                />
                <p className="text-base text-zinc-600 mt-0.5">Optional — goes into the Description column for every row.</p>
              </div>

              {/* Row 1: Listing Type + Label Format */}
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-base font-medium text-zinc-400 mb-1">
                    Listing Type
                  </label>
                  <div className="flex rounded-lg border border-zinc-700 overflow-hidden text-base">
                    {(["Buy it Now", "Auction"] as const).map((type) => (
                      <button
                        key={type}
                        onClick={() => setListingType(type)}
                        className={`flex-1 py-1.5 font-medium transition-colors ${
                          listingType === type
                            ? "bg-zinc-700 text-white"
                            : "bg-zinc-800/60 text-zinc-400 hover:text-zinc-200"
                        }`}
                      >
                        {type}
                      </button>
                    ))}
                  </div>
                </div>
                <div>
                  <label className="block text-base font-medium text-zinc-400 mb-1">
                    Label Format
                  </label>
                  <div className="flex rounded-lg border border-zinc-700 overflow-hidden text-base">
                    {(["short", "long"] as const).map((mode) => (
                      <button
                        key={mode}
                        onClick={() => setLabelMode(mode)}
                        className={`flex-1 py-1.5 font-medium transition-colors ${
                          labelMode === mode
                            ? "bg-zinc-700 text-white"
                            : "bg-zinc-800/60 text-zinc-400 hover:text-zinc-200"
                        }`}
                      >
                        {mode === "short" ? "Short" : "Long"}
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              {/* Row 2: Giveaways + Buyers Giveaway */}
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-base font-medium text-zinc-400 mb-1">
                    Giveaways
                  </label>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => setGiveaways((v) => Math.max(0, v - 1))}
                      disabled={giveaways === 0}
                      className={`w-8 h-8 flex items-center justify-center rounded-md text-base font-bold transition-colors ${
                        giveaways === 0
                          ? "bg-zinc-800/40 text-zinc-700 cursor-not-allowed"
                          : "bg-zinc-800 text-zinc-300 hover:bg-zinc-700 hover:text-white"
                      }`}
                    >
                      −
                    </button>
                    <span className="text-base font-bold text-white tabular-nums w-8 text-center">
                      {giveaways}
                    </span>
                    <button
                      onClick={() => setGiveaways((v) => v + 1)}
                      className="w-8 h-8 flex items-center justify-center rounded-md bg-zinc-800 text-zinc-300 hover:bg-zinc-700 hover:text-white text-base font-bold transition-colors"
                    >
                      +
                    </button>
                  </div>
                </div>
                <div>
                  <label className="block text-base font-medium text-zinc-400 mb-1">
                    Buyers Giveaway
                  </label>
                  <button
                    onClick={() => setBuyersGiveaway((v) => !v)}
                    className="flex items-center gap-2"
                  >
                    <div
                      className="relative w-11 h-6 rounded-full transition-colors"
                      style={{
                        background: buyersGiveaway ? "#f59e0b" : "#3f3f46",
                      }}
                    >
                      <div
                        className="absolute top-0.5 w-5 h-5 rounded-full bg-white shadow transition-transform"
                        style={{
                          transform: buyersGiveaway ? "translateX(22px)" : "translateX(2px)",
                        }}
                      />
                    </div>
                    <span className="text-base text-zinc-400">
                      {buyersGiveaway ? "On" : "Off"}
                    </span>
                  </button>
                </div>
              </div>

              {/* Row 3: Tag Labels — full width */}
              <div>
                <label className="block text-base font-medium text-zinc-400 mb-1">
                  Tag Labels
                </label>
                <div className="grid grid-cols-4 gap-2">
                  {(
                    [
                      ["Autograph", "auto"],
                      ["Mem Auto", "memAuto"],
                      ["Relic", "relic"],
                      ["Rookie", "rookie"],
                    ] as [string, keyof Labels][]
                  ).map(([display, key]) => (
                    <div key={key} className="text-center">
                      <p className="text-base text-zinc-600 mb-0.5 truncate">{display}</p>
                      <input
                        type="text"
                        value={labels[key]}
                        onChange={(e) =>
                          setLabels((l) => ({ ...l, [key]: e.target.value }))
                        }
                        className="w-full bg-zinc-800 border border-zinc-700 text-base text-white rounded px-1.5 py-1 outline-none focus:border-zinc-500 transition-colors text-center font-mono"
                      />
                    </div>
                  ))}
                </div>
              </div>

              {/* Row 4: Title Preview */}
              {previewPlayers.length > 0 && (
                <div>
                  <label className="block text-base font-medium text-zinc-400 mb-1">
                    Title Preview
                  </label>
                  <div className="rounded-lg border border-zinc-800 bg-zinc-950 divide-y divide-zinc-800 overflow-hidden">
                    {buyersGiveaway && (
                      <div className="px-3 py-1.5">
                        <p className="text-base font-mono text-amber-400 break-all">
                          Buyers Giveaway
                        </p>
                      </div>
                    )}
                    {previewPlayers.map((p) => (
                      <div key={p.id} className="px-3 py-1.5">
                        <p className="text-base font-mono text-zinc-300 break-all">
                          {buildTitle(p, labels, labelMode)}
                        </p>
                      </div>
                    ))}
                    {(players.length > PREVIEW_COUNT || giveaways > 0) && (
                      <div className="px-3 py-1.5">
                        <p className="text-base text-zinc-600 italic">
                          +{(players.length - PREVIEW_COUNT + giveaways).toLocaleString()} more rows…
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>

            {/* Footer */}
            <div className="px-5 py-3 border-t border-zinc-800">
              <button
                onClick={downloadCSV}
                className="w-full flex items-center justify-center gap-2 bg-amber-500 hover:bg-amber-400 text-black font-semibold text-base py-2 rounded-lg transition-colors"
              >
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
                </svg>
                Download CSV ({totalRows.toLocaleString()} rows)
              </button>
              <div className="flex items-center justify-center gap-1.5 mt-2">
                <span className="text-base text-zinc-500">Built for</span>
                <img
                  src="/logos/whatnot-logo.png"
                  alt="Whatnot"
                  className="h-6 object-contain"
                />
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
