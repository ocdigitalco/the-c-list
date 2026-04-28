"use client";

import React, { useState, useMemo, useRef, useEffect } from "react";
import Link from "next/link";
import type { LeaderboardRow } from "./types";
import type { BoxConfigSingle, BoxConfigMulti } from "./types";
import { getNBAHeadshotUrl } from "@/lib/nba-headshot";
import { getUFCHeadshotUrl } from "@/lib/ufc-headshot";
import { getMLBHeadshotUrl } from "@/lib/mlb-headshot";
import { trackEvent } from "@/lib/trackEvent";
import { normalizeOddsObj, denomToDisplay } from "@/lib/parseOdds";
import { BreakSheetModal, type BreakSheetPlayer } from "@/components/BreakSheetModal";

// ─── Types & Constants ─────────────────────────────────────────────────────────

type Tab = "Box Config" | "Pack Odds" | "Inserts" | "Autographs";
type SortKey = "totalCards" | "autographs" | "inserts" | "numberedParallels";

const TABS: Tab[] = ["Box Config", "Pack Odds", "Inserts", "Autographs"];
const SORT_CHIPS: { key: SortKey; label: string }[] = [
  { key: "totalCards", label: "Total Cards" },
  { key: "autographs", label: "Autographs" },
  { key: "inserts", label: "Inserts" },
  { key: "numberedParallels", label: "Numbered" },
];

const FONT_DISPLAY = "var(--cl-font-display), 'Inter Tight', sans-serif";
const FONT_MONO = "var(--cl-font-mono), 'JetBrains Mono', ui-monospace, monospace";

interface OddsRow {
  name: string;
  denom: number;
  rare: boolean;
  printRun?: number | null;
}

interface ParallelInfo {
  name: string;
  printRun: number | null;
}

interface OddsFormat {
  key: string;
  label: string;
  packsPerBox: number;
  baseParallels: OddsRow[];
  inserts: OddsRow[];
  autographs: OddsRow[];
}

interface BoxRow {
  label: string;
  cardsPerPack: number | null;
  packsPerBox: number | null;
  boxesPerCase: number | null;
  packsPerCase: string;
  autosPerBox: number | null;
  notes?: string;
}

export interface SetDetailClientProps {
  setName: string;
  sport: string;
  league: string | null;
  tier: string;
  releaseDate: string | null;
  setId: number;
  setSlug: string;
  sampleImageUrl: string | null;
  cards: number;
  cardTypes: number;
  parallelTypes: number;
  autographs: number;
  autoParallels: number;
  totalParallels: number;
  athleteCount: number;
  hasChecklist: boolean;
  hasNumberedParallels: boolean;
  hasBoxConfig: boolean;
  hasPackOdds: boolean;
  boxConfig: string | null;
  packOdds: string | null;
  entries: LeaderboardRow[];
  hasTeamData: boolean;
  breakSheetPlayers: BreakSheetPlayer[];
  parallelsList: ParallelInfo[];
}

// ─── Helpers ────────────────────────────────────────────────────────────────────

const BOX_LABEL_MAP: Record<string, string> = {
  hobby: "Hobby", jumbo: "Jumbo", mega: "Mega", blaster: "Blaster",
  value: "Value", fat_pack: "Fat Pack", hanger: "Hanger",
  breakers_delight: "Breaker's Delight", first_day_issue: "First Day Issue",
  breaker: "Breaker", hobby_hybrid: "Hobby Hybrid", sapphire: "Sapphire",
  hongbao: "Hongbao", logofractor: "Logofractor", ffnyc: "FFNYC", fdi: "First Day Issue",
  value_se: "Value", value_ea: "Value", value_cee: "Value",
  mega_se: "Mega", mega_ea: "Mega", mega_cee: "Mega",
  hanger_se: "Hanger", hanger_ea: "Hanger", hanger_cee: "Hanger",
};

function fmtBoxLabel(key: string): string {
  return BOX_LABEL_MAP[key] ?? key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function isMultiConfig(cfg: BoxConfigSingle | BoxConfigMulti): cfg is BoxConfigMulti {
  const first = Object.values(cfg)[0];
  return first !== null && typeof first === "object";
}

function getAutosPerBox(fmt: BoxConfigSingle): number | null {
  return fmt.autos_per_box ?? fmt.autos_or_memorabilia_per_box ??
    fmt.autos_or_relics_per_box ?? fmt.autos_or_auto_relics_per_box ?? null;
}

function categorize(key: string): "base" | "insert" | "auto" {
  const l = key.toLowerCase();
  if (l.includes("auto") || l.includes("autograph") || l.includes("signature")) return "auto";
  if (l.startsWith("base")) return "base";
  return "insert";
}

function isRare(name: string, denom: number): boolean {
  return name.toLowerCase().includes("superfractor") || denom >= 5000;
}

function perBoxStr(denom: number, ppb: number): string {
  const v = ppb / denom;
  if (v >= 1) return `~${v.toFixed(1)}×`;
  return `~${v.toFixed(2)}×`;
}

function formatDate(iso: string): string {
  const d = new Date(iso + "T00:00:00Z");
  return d.toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric", timeZone: "UTC" });
}

function formatDateShort(iso: string): string {
  const d = new Date(iso + "T00:00:00Z");
  return d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric", timeZone: "UTC" }).toUpperCase();
}

function extractMeta(name: string, sport: string) {
  let rest = name.replace(/^\d{4}(-\d{2})?\s+/, "");
  const mfrs = ["Topps", "Panini", "Upper Deck", "Bowman", "Leaf"];
  let manufacturer = "";
  for (const m of mfrs) {
    if (rest.toLowerCase().startsWith(m.toLowerCase() + " ")) {
      manufacturer = m;
      rest = rest.slice(m.length + 1);
      break;
    }
  }
  // Remove sport suffix
  const sportWords = sport.split(" ");
  const restWords = rest.split(" ");
  while (sportWords.length > 0 && restWords.length > 0 &&
    restWords[restWords.length - 1].toLowerCase() === sportWords[sportWords.length - 1].toLowerCase()) {
    restWords.pop();
    sportWords.pop();
  }
  return { manufacturer: manufacturer.toUpperCase(), brand: restWords.join(" ").toUpperCase() || manufacturer.toUpperCase() };
}

function buildBoxRows(boxConfig: string): BoxRow[] {
  const raw = JSON.parse(boxConfig) as BoxConfigSingle | BoxConfigMulti;
  if (isMultiConfig(raw)) {
    return Object.entries(raw).map(([key, fmt]) => {
      const ppb = fmt.packs_per_box ?? null;
      const bpc = fmt.boxes_per_case ?? null;
      return {
        label: fmtBoxLabel(key),
        cardsPerPack: fmt.cards_per_pack ?? null,
        packsPerBox: ppb,
        boxesPerCase: bpc,
        packsPerCase: ppb != null && bpc != null ? (ppb * bpc).toLocaleString() : "—",
        autosPerBox: getAutosPerBox(fmt),
        notes: fmt.notes ?? fmt.note ?? undefined,
      };
    });
  }
  const fmt = raw as BoxConfigSingle;
  const ppb = fmt.packs_per_box ?? null;
  const bpc = fmt.boxes_per_case ?? null;
  return [{
    label: "Hobby",
    cardsPerPack: fmt.cards_per_pack ?? null,
    packsPerBox: ppb,
    boxesPerCase: bpc,
    packsPerCase: ppb != null && bpc != null ? (ppb * bpc).toLocaleString() : "—",
    autosPerBox: getAutosPerBox(fmt),
    notes: fmt.notes ?? fmt.note ?? undefined,
  }];
}

function matchPrintRun(oddsKey: string, parallelsList: ParallelInfo[]): number | null | undefined {
  const key = oddsKey.toLowerCase().trim();

  // Step 1 — Exact match (entire key equals parallel name)
  const exact = parallelsList.find(p => p.name.toLowerCase().trim() === key);
  if (exact) return exact.printRun;

  // Step 2 — Suffix match: odds key ends with the parallel name
  // e.g. "Base Gold Refractor" ends with "Gold Refractor" → /50
  // e.g. "Rookie Variation Autographs Superfractor" ends with "Superfractor" → /1
  // Pick the LONGEST parallel name that matches as a suffix (most specific)
  const suffixMatches = parallelsList.filter(p => {
    const pName = p.name.toLowerCase().trim();
    return key.endsWith(pName) || key.endsWith(" " + pName);
  });

  if (suffixMatches.length > 0) {
    suffixMatches.sort((a, b) => b.name.length - a.name.length);
    return suffixMatches[0].printRun;
  }

  // Step 3 — No match found (unnumbered base insert)
  return undefined;
}

function buildOddsFormats(packOdds: string, boxConfig: string | null, parallelsList: ParallelInfo[]): OddsFormat[] {
  const rawOdds = JSON.parse(packOdds);
  const firstVal = Object.values(rawOdds)[0];
  const isNested = firstVal !== null && typeof firstVal === "object";

  // Build packs-per-box lookup from box config
  const ppbMap: Record<string, number> = {};
  if (boxConfig) {
    const rawBox = JSON.parse(boxConfig);
    if (isMultiConfig(rawBox)) {
      for (const [key, cfg] of Object.entries(rawBox as BoxConfigMulti)) {
        ppbMap[fmtBoxLabel(key).toLowerCase()] = cfg.packs_per_box ?? 12;
      }
    } else {
      ppbMap["hobby"] = (rawBox as BoxConfigSingle).packs_per_box ?? 12;
    }
  }

  function ppbFor(label: string): number {
    return ppbMap[label.toLowerCase()] ?? 12;
  }

  function buildRows(data: Record<string, unknown>): { base: OddsRow[]; ins: OddsRow[]; auto: OddsRow[] } {
    const normalized = normalizeOddsObj(data);
    const base: OddsRow[] = [];
    const ins: OddsRow[] = [];
    const auto: OddsRow[] = [];
    for (const [key, denom] of Object.entries(normalized)) {
      const printRun = matchPrintRun(key, parallelsList);
      const row = { name: key, denom, rare: isRare(key, denom), printRun };
      const cat = categorize(key);
      if (cat === "base") base.push(row);
      else if (cat === "auto") auto.push(row);
      else ins.push(row);
    }
    base.sort((a, b) => a.denom - b.denom);
    ins.sort((a, b) => a.denom - b.denom);
    auto.sort((a, b) => a.denom - b.denom);
    return { base, ins, auto };
  }

  const formats: OddsFormat[] = [];
  if (isNested) {
    const seenLabels = new Set<string>();
    for (const [key, data] of Object.entries(rawOdds as Record<string, Record<string, unknown>>)) {
      const label = fmtBoxLabel(key);
      if (seenLabels.has(label)) continue;
      seenLabels.add(label);
      const { base, ins, auto } = buildRows(data);
      formats.push({ key, label, packsPerBox: ppbFor(label), baseParallels: base, inserts: ins, autographs: auto });
    }
  } else {
    const { base, ins, auto } = buildRows(rawOdds as Record<string, unknown>);
    const label = Object.keys(ppbMap).length === 1
      ? Object.keys(ppbMap)[0].replace(/\b\w/g, c => c.toUpperCase())
      : "Hobby";
    formats.push({ key: "default", label, packsPerBox: ppbFor(label), baseParallels: base, inserts: ins, autographs: auto });
  }
  return formats;
}

// ─── Avatar ─────────────────────────────────────────────────────────────────────

function InitialsAvatar({ name, size = 30 }: { name: string; size?: number }) {
  const initials = name.split(" ").map((n) => n[0]).slice(0, 2).join("").toUpperCase();
  return (
    <div
      className="rounded-full flex items-center justify-center flex-shrink-0"
      style={{
        width: size, height: size,
        background: "#EAE6D9", color: "#6B6757",
        fontSize: size * 0.35, fontWeight: 600,
      }}
    >
      {initials}
    </div>
  );
}

function PlayerAvatar({ name, nbaPlayerId, ufcImageUrl, mlbPlayerId, imageUrl, size = 30 }: {
  name: string; nbaPlayerId: number | null; ufcImageUrl: string | null;
  mlbPlayerId: number | null; imageUrl?: string | null; size?: number;
}) {
  const [err, setErr] = useState(false);
  const url = getNBAHeadshotUrl(nbaPlayerId) ?? getUFCHeadshotUrl(ufcImageUrl) ?? getMLBHeadshotUrl(mlbPlayerId) ?? (imageUrl || null);
  if (!url || err) return <InitialsAvatar name={name} size={size} />;
  return (
    <img src={url} alt={name} loading="lazy" onError={() => setErr(true)}
      className="rounded-full object-cover object-top flex-shrink-0"
      style={{ width: size, height: size }} />
  );
}

// ─── Athletes Rail ──────────────────────────────────────────────────────────────

function AthletesRail({ entries, hasTeamData, setId, setSlug, isMobile = false }: {
  entries: LeaderboardRow[]; hasTeamData: boolean; setId: number; setSlug: string; isMobile?: boolean;
}) {
  const [sortKey, setSortKey] = useState<SortKey>("totalCards");
  const [rookiesOnly, setRookiesOnly] = useState(false);
  const [query, setQuery] = useState("");
  const [showAll, setShowAll] = useState(false);
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => () => { if (debounceRef.current) clearTimeout(debounceRef.current); }, []);

  const filtered = useMemo(() => {
    let list = entries;
    if (query.trim()) {
      const q = query.trim().toLowerCase();
      list = list.filter((e) => e.name.toLowerCase().includes(q) || (e.team?.toLowerCase().includes(q)));
    }
    if (rookiesOnly) list = list.filter((e) => e.isRookie);
    return [...list].sort((a, b) => {
      const diff = b[sortKey] - a[sortKey];
      return diff !== 0 ? diff : a.name.localeCompare(b.name);
    });
  }, [entries, query, rookiesOnly, sortKey]);

  const visible = showAll ? filtered : filtered.slice(0, 50);
  const avatarSize = isMobile ? 34 : 30;
  const rowPy = isMobile ? "12px 4px" : "9px 4px";

  return (
    <div className="flex flex-col h-full" style={{ background: "#FFFFFF" }}>
      <div className="shrink-0 space-y-3" style={{ padding: isMobile ? "14px 16px 12px" : "22px 18px 12px" }}>
        {!isMobile && (
          <h2 style={{ fontFamily: FONT_DISPLAY, fontWeight: 600, fontSize: 15, letterSpacing: -0.2, color: "#0F0F0E", marginBottom: 12 }}>
            Athletes in Set
          </h2>
        )}
        {/* Search */}
        <div className="relative">
          <svg className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 pointer-events-none" style={{ color: "#8A8677" }}
            fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
            <path strokeLinecap="round" strokeLinejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
          </svg>
          <input
            type="text" value={query}
            onChange={(e) => {
              const q = e.target.value;
              setQuery(q);
              if (debounceRef.current) clearTimeout(debounceRef.current);
              if (q.trim().length >= 2) {
                debounceRef.current = setTimeout(() => {
                  entries.filter((a) => a.name.toLowerCase().includes(q.toLowerCase()))
                    .slice(0, 3).forEach((a) => trackEvent(a.id, "search"));
                }, 100);
              }
            }}
            placeholder="Search athletes…"
            autoComplete="off" spellCheck={false}
            className="w-full outline-none"
            style={{
              background: "#F1EFE9", borderRadius: 8, padding: "7px 10px 7px 30px",
              fontSize: isMobile ? 14 : 13, border: "none", color: "#0F0F0E",
            }}
          />
        </div>
        {/* Filter chips */}
        <div className="flex flex-wrap gap-1.5">
          {SORT_CHIPS.map((chip) => (
            <button key={chip.key} onClick={() => setSortKey(chip.key)}
              style={{
                borderRadius: isMobile ? 999 : 4, padding: "4px 9px",
                fontSize: 11, fontWeight: 500,
                background: sortKey === chip.key ? "#0F0F0E" : "transparent",
                color: sortKey === chip.key ? "#FAFAF7" : "#3A372F",
                border: sortKey === chip.key ? "1px solid #0F0F0E" : "1px solid #E6E3D9",
              }}>
              {chip.label}
            </button>
          ))}
        </div>
        {/* Rookies only */}
        <label className="flex items-center gap-1.5 cursor-pointer" style={{ fontSize: 11, color: "#3A372F" }}>
          <input type="checkbox" checked={rookiesOnly} onChange={() => setRookiesOnly((v) => !v)}
            style={{ accentColor: "#0F0F0E" }} />
          Rookies only
        </label>
      </div>
      {/* Column header */}
      <div className="shrink-0 flex justify-between items-center"
        style={{
          padding: "6px 18px", borderBottom: "1px solid #EDEAE0",
          fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6, color: "#8A8677",
          textTransform: "uppercase",
        }}>
        <span>ATHLETE</span>
        <span>{SORT_CHIPS.find((c) => c.key === sortKey)?.label}</span>
      </div>
      {/* Rows */}
      <div className="flex-1 overflow-y-auto">
        {visible.length === 0 ? (
          <p className="text-center py-8" style={{ fontSize: 13, color: "#8A8677", fontStyle: "italic" }}>No athletes match.</p>
        ) : (
          <>
            {visible.map((entry, idx) => (
              <Link key={entry.id}
                href={`/sets/${setSlug || setId}/athlete/${entry.slug || entry.id}`}
                onClick={() => trackEvent(entry.id, "view")}
                className="flex items-center gap-2 transition-colors"
                style={{ padding: rowPy, paddingLeft: 18, paddingRight: 18, borderBottom: "1px solid #F4F1E8" }}
                onMouseEnter={(e) => { (e.currentTarget as HTMLElement).style.background = "#F1EFE9"; }}
                onMouseLeave={(e) => { (e.currentTarget as HTMLElement).style.background = "transparent"; }}>
                <span style={{ fontFamily: FONT_MONO, fontSize: 11, color: "#8A8677", width: 18, textAlign: "right", flexShrink: 0 }}>
                  {idx + 1}
                </span>
                <PlayerAvatar name={entry.name} nbaPlayerId={entry.nbaPlayerId} ufcImageUrl={entry.ufcImageUrl}
                  mlbPlayerId={entry.mlbPlayerId} imageUrl={entry.imageUrl} size={avatarSize} />
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-1.5 min-w-0">
                    <span className="truncate" style={{ fontSize: 13, fontWeight: 500, color: "#0F0F0E" }}>{entry.name}</span>
                    {entry.isRookie && (
                      <span className="shrink-0" style={{
                        background: "oklch(0.55 0.17 25)", color: "#FFF8F1",
                        fontSize: 8, fontWeight: 700, letterSpacing: 0.6,
                        padding: "1px 4px", borderRadius: 2, lineHeight: 1.2,
                      }}>RC</span>
                    )}
                  </div>
                  {hasTeamData && entry.team && (
                    <p className="truncate" style={{ fontSize: 11, color: "#6B6757", marginTop: 1 }}>{entry.team}</p>
                  )}
                </div>
                <span style={{ fontFamily: FONT_MONO, fontSize: 13, fontWeight: 600, color: "#0F0F0E", flexShrink: 0 }}>
                  {entry[sortKey].toLocaleString()}
                </span>
              </Link>
            ))}
            {!showAll && filtered.length > 50 && (
              <button onClick={() => setShowAll(true)}
                className="w-full py-3" style={{ fontSize: 13, fontWeight: 600, color: "#0F0F0E" }}>
                Show all {filtered.length.toLocaleString()} athletes
              </button>
            )}
          </>
        )}
      </div>
    </div>
  );
}

// ─── Mobile Drawer ──────────────────────────────────────────────────────────────

function MobileAthletesDrawer({ open, onClose, entries, hasTeamData, setId, setSlug, athleteCount }: {
  open: boolean; onClose: () => void;
  entries: LeaderboardRow[]; hasTeamData: boolean; setId: number; setSlug: string; athleteCount: number;
}) {
  const triggerRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (!open) return;
    function onKey(e: KeyboardEvent) { if (e.key === "Escape") onClose(); }
    document.body.style.overflow = "hidden";
    window.addEventListener("keydown", onKey);
    return () => {
      document.body.style.overflow = "";
      window.removeEventListener("keydown", onKey);
    };
  }, [open, onClose]);

  return (
    <div
      role="dialog" aria-modal="true" aria-label="Athletes in Set"
      className="fixed inset-0 z-[100]"
      style={{
        background: "#FFFFFF",
        transform: open ? "translateY(0)" : "translateY(100%)",
        transition: "transform 200ms ease-out",
        pointerEvents: open ? "auto" : "none",
      }}>
      {/* Drawer header */}
      <div className="flex items-center justify-between" style={{
        padding: "14px 16px", borderBottom: "1px solid #EDEAE0", background: "#FFFFFF",
      }}>
        <button onClick={onClose} aria-label="Close" className="p-1">
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="#0F0F0E" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18 18 6M6 6l12 12" />
          </svg>
        </button>
        <span style={{ fontFamily: FONT_DISPLAY, fontSize: 17, fontWeight: 600, letterSpacing: -0.3, color: "#0F0F0E" }}>
          Athletes in Set
        </span>
        <span style={{ fontFamily: FONT_MONO, fontSize: 12, color: "#8A8677" }}>{athleteCount}</span>
      </div>
      {/* Drawer body */}
      <div className="flex-1" style={{ height: "calc(100% - 56px)", overflowY: "auto" }}>
        <AthletesRail entries={entries} hasTeamData={hasTeamData} setId={setId} setSlug={setSlug} isMobile />
      </div>
    </div>
  );
}

// ─── Coverage Card ──────────────────────────────────────────────────────────────

function CoverageCard({ hasChecklist, hasNumberedParallels, hasBoxConfig, hasPackOdds, breakSheetPlayers, setName, sport, league }: {
  hasChecklist: boolean; hasNumberedParallels: boolean; hasBoxConfig: boolean; hasPackOdds: boolean;
  breakSheetPlayers: BreakSheetPlayer[]; setName: string; sport: string; league: string | null;
}) {
  const rows = [
    { label: "Athlete Checklist", ok: hasChecklist },
    { label: "Numbered Parallels", ok: hasNumberedParallels },
    { label: "Box Configuration", ok: hasBoxConfig },
    { label: "Pack Odds", ok: hasPackOdds },
  ];
  return (
    <div style={{
      background: "#FAFAF7", border: "1px solid #EDEAE0", borderRadius: 8, padding: "12px 14px",
    }}>
      <div className="flex items-center justify-between" style={{ marginBottom: 10 }}>
        <span style={{ fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6, color: "#8A8677", textTransform: "uppercase" }}>
          Coverage
        </span>
        <div className="v2-break-sheet-pill">
          <style>{`
            .v2-break-sheet-pill > button {
              background: #0F0F0E !important; color: #FAFAF7 !important;
              font-size: 10px !important; font-weight: 600 !important;
              padding: 5px 10px !important; border-radius: 4px !important;
              border: none !important; cursor: pointer !important;
              line-height: 1.2 !important;
            }
            .v2-break-sheet-pill > button:hover { background: #1A1A19 !important; }
          `}</style>
          <BreakSheetModal setName={setName} sport={sport} league={league} players={breakSheetPlayers} />
        </div>
      </div>
      <div className="space-y-2">
        {rows.map((r) => (
          <div key={r.label} className="flex items-center justify-between">
            <span style={{ fontSize: 12, color: "#3A372F" }}>{r.label}</span>
            <span
              aria-label={r.ok ? "Present" : "Missing"}
              style={{
                width: 8, height: 8, borderRadius: "50%",
                background: r.ok ? "#0E8A4F" : "#B7B2A3",
              }}
            />
          </div>
        ))}
      </div>
    </div>
  );
}

// ─── Stat Strip ─────────────────────────────────────────────────────────────────

function StatStrip({ items }: { items: { label: string; value: number }[] }) {
  return (
    <>
      {/* Desktop: 6-col */}
      <div className="hidden min-[1180px]:grid" style={{
        gridTemplateColumns: "repeat(6, 1fr)", borderBottom: "1px solid #EDEAE0", background: "#FFFFFF",
      }}>
        {items.map((item, i) => (
          <div key={item.label} style={{
            padding: "18px 22px",
            borderRight: i < items.length - 1 ? "1px solid #EDEAE0" : "none",
          }}>
            <div style={{ fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6, color: "#8A8677", textTransform: "uppercase" }}>
              {item.label}
            </div>
            <div style={{ fontFamily: FONT_DISPLAY, fontSize: 26, fontWeight: 600, letterSpacing: -0.6, color: "#0F0F0E", marginTop: 4 }}>
              {item.value.toLocaleString()}
            </div>
          </div>
        ))}
      </div>
      {/* Mobile: 3×2 */}
      <div className="grid min-[1180px]:hidden" style={{
        gridTemplateColumns: "repeat(3, 1fr)", borderBottom: "1px solid #EDEAE0", background: "#FFFFFF",
      }}>
        {items.map((item, i) => (
          <div key={item.label} style={{
            padding: "14px 16px",
            borderRight: (i % 3) < 2 ? "1px solid #EDEAE0" : "none",
            borderBottom: i < 3 ? "1px solid #EDEAE0" : "none",
          }}>
            <div style={{ fontFamily: FONT_MONO, fontSize: 8, fontWeight: 600, letterSpacing: 1.6, color: "#8A8677", textTransform: "uppercase" }}>
              {item.label}
            </div>
            <div style={{ fontFamily: FONT_DISPLAY, fontSize: 20, fontWeight: 600, letterSpacing: -0.6, color: "#0F0F0E", marginTop: 4 }}>
              {item.value.toLocaleString()}
            </div>
          </div>
        ))}
      </div>
    </>
  );
}

// ─── Tab: Box Config ────────────────────────────────────────────────────────────

function BoxConfigContent({ boxConfig }: { boxConfig: string | null }) {
  if (!boxConfig) return <EmptyTab label="Box configuration coming soon" />;
  const rows = buildBoxRows(boxConfig);

  return (
    <>
      {/* Desktop table */}
      <div className="hidden min-[1180px]:block">
        <table className="w-full" style={{ fontSize: 13 }}>
          <thead>
            <tr>
              {["BOX TYPE", "CARDS/PACK", "PACKS/BOX", "BOXES/CASE", "PACKS/CASE", "AUTOS/BOX"].map((h, i) => (
                <th key={h} style={{
                  textAlign: i === 0 ? "left" : "right", padding: "10px 10px",
                  fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6,
                  color: "#8A8677", borderBottom: "1px solid #EDEAE0", textTransform: "uppercase",
                }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <React.Fragment key={row.label}>
                <tr>
                  <td style={{ padding: "12px 10px", fontWeight: 600, fontFamily: FONT_DISPLAY, color: "#0F0F0E",
                    borderBottom: row.notes ? "none" : "1px solid #F4F1E8" }}>{row.label}</td>
                  {[row.cardsPerPack, row.packsPerBox, row.boxesPerCase].map((v, j) => (
                    <td key={j} style={{ padding: "12px 10px", textAlign: "right",
                      fontFamily: FONT_MONO, color: v != null ? "#0F0F0E" : "#B7B2A3",
                      borderBottom: row.notes ? "none" : "1px solid #F4F1E8" }}>
                      {v ?? "—"}
                    </td>
                  ))}
                  <td style={{ padding: "12px 10px", textAlign: "right", fontFamily: FONT_MONO,
                    color: row.packsPerCase !== "—" ? "#0F0F0E" : "#B7B2A3",
                    borderBottom: row.notes ? "none" : "1px solid #F4F1E8" }}>
                    {row.packsPerCase}
                  </td>
                  <td style={{ padding: "12px 10px", textAlign: "right", fontFamily: FONT_MONO,
                    color: row.autosPerBox != null ? "#0F0F0E" : "#B7B2A3",
                    borderBottom: row.notes ? "none" : "1px solid #F4F1E8" }}>
                    {row.autosPerBox ?? "—"}
                  </td>
                </tr>
                {row.notes && (
                  <tr>
                    <td colSpan={6} style={{
                      padding: "4px 10px 12px", fontStyle: "italic", fontSize: 12,
                      color: "#6B6757", borderBottom: "1px solid #F4F1E8",
                    }}>{row.notes}</td>
                  </tr>
                )}
              </React.Fragment>
            ))}
          </tbody>
        </table>
      </div>
      {/* Mobile cards */}
      <div className="min-[1180px]:hidden space-y-2.5">
        {rows.map((row) => (
          <div key={row.label} style={{
            background: "#FFFFFF", border: "1px solid #EDEAE0", borderRadius: 10, padding: "12px 14px",
          }}>
            <div style={{ fontFamily: FONT_DISPLAY, fontSize: 15, fontWeight: 600, color: "#0F0F0E", marginBottom: 10 }}>
              {row.label}
            </div>
            <div className="grid grid-cols-5 gap-2">
              {[
                { l: "CARDS/PK", v: row.cardsPerPack },
                { l: "PKS/BOX", v: row.packsPerBox },
                { l: "BXS/CASE", v: row.boxesPerCase },
                { l: "PKS/CASE", v: row.packsPerCase === "—" ? null : row.packsPerCase },
                { l: "AUTOS/BX", v: row.autosPerBox },
              ].map((s) => (
                <div key={s.l}>
                  <div style={{ fontFamily: FONT_MONO, fontSize: 7, fontWeight: 600, letterSpacing: 1, color: "#8A8677", textTransform: "uppercase" }}>
                    {s.l}
                  </div>
                  <div style={{ fontFamily: FONT_MONO, fontSize: 14, fontWeight: 600, color: s.v != null ? "#0F0F0E" : "#B7B2A3", marginTop: 2 }}>
                    {s.v ?? "—"}
                  </div>
                </div>
              ))}
            </div>
            {row.notes && (
              <div style={{ borderTop: "1px solid #F4F1E8", marginTop: 10, paddingTop: 8, fontSize: 11, fontStyle: "italic", color: "#6B6757" }}>
                {row.notes}
              </div>
            )}
          </div>
        ))}
      </div>
    </>
  );
}

// ─── Tab: Pack Odds ─────────────────────────────────────────────────────────────

function PackOddsContent({ formats }: { formats: OddsFormat[] }) {
  const [activeIdx, setActiveIdx] = useState(0);
  if (formats.length === 0) return <EmptyTab label="Pack odds coming soon" />;
  const active = formats[activeIdx] ?? formats[0];
  const rows = active.baseParallels;
  const ppb = active.packsPerBox;

  return (
    <div className="space-y-4">
      {/* Box type chips */}
      {formats.length > 1 && (
        <div className="flex flex-wrap gap-1.5 min-[1180px]:gap-2">
          {formats.map((f, i) => (
            <button key={f.key} onClick={() => setActiveIdx(i)}
              className="min-[1180px]:rounded-md"
              style={{
                borderRadius: 999, padding: "7px 12px", fontSize: 12, fontWeight: 600,
                background: i === activeIdx ? "#0F0F0E" : "#FFFFFF",
                color: i === activeIdx ? "#FAFAF7" : "#3A372F",
                border: i === activeIdx ? "1px solid #0F0F0E" : "1px solid #EDEAE0",
              }}>
              {f.label}
            </button>
          ))}
        </div>
      )}
      {rows.length === 0 ? (
        <EmptyTab label={`No base parallel odds for ${active.label}`} />
      ) : (
        <OddsTable rows={rows} ppb={ppb} headers={["BASE PARALLELS", "PACK ODDS", `PER BOX (${ppb} PACKS)`]} showNumbered />
      )}
    </div>
  );
}

// ─── Tab: Inserts ───────────────────────────────────────────────────────────────

function InsertsContent({ formats }: { formats: OddsFormat[] }) {
  if (formats.length === 0) return <EmptyTab label="Pack odds coming soon" />;
  const active = formats[0]; // hobby / first format
  const rows = active.inserts;
  const ppb = active.packsPerBox;
  if (rows.length === 0) return <EmptyTab label="No insert odds available" />;
  return <OddsTable rows={rows} ppb={ppb} headers={["INSERT", "PACK ODDS", `PER BOX (${ppb} PACKS)`]} showNumbered />;
}

// ─── Tab: Autographs ────────────────────────────────────────────────────────────

function AutosContent({ formats }: { formats: OddsFormat[] }) {
  if (formats.length === 0) return <EmptyTab label="Pack odds coming soon" />;
  const active = formats[0];
  const rows = active.autographs;
  const ppb = active.packsPerBox;
  if (rows.length === 0) return <EmptyTab label="No autograph odds available" />;

  return (
    <>
      {/* Desktop */}
      <div className="hidden min-[1180px]:block">
        <table className="w-full" style={{ fontSize: 13 }}>
          <thead>
            <tr>
              {["AUTOGRAPH", "NUMBERED", "PACK ODDS", `PER BOX (${ppb} PACKS)`].map((h, i) => (
                <th key={h} style={{
                  textAlign: i === 0 ? "left" : "right", padding: "10px 10px",
                  fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6,
                  color: "#6B6757", borderBottom: "1px solid #EDEAE0", textTransform: "uppercase",
                  width: i === 0 ? undefined : i === 1 ? 70 : i === 2 ? 100 : 160,
                }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.name} style={{ borderBottom: "1px solid #F4F1E8" }}>
                <td style={{ padding: "12px 10px", color: row.rare ? "#9A2B14" : "#0F0F0E" }}>{row.name}</td>
                <td style={{ padding: "12px 10px", textAlign: "right", fontFamily: FONT_MONO, color: "#B7B2A3" }}>
                  {printRunDisplay(row.printRun)}
                </td>
                <td style={{ padding: "12px 10px", textAlign: "right", fontFamily: FONT_MONO, color: "#0F0F0E" }}>
                  {denomToDisplay(row.denom)}
                </td>
                <td style={{ padding: "12px 10px", textAlign: "right", fontFamily: FONT_MONO, color: "#6B6757" }}>
                  {perBoxStr(row.denom, ppb)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {/* Mobile */}
      <div className="min-[1180px]:hidden space-y-0">
        {rows.map((row) => (
          <div key={row.name} className="flex flex-col gap-0.5" style={{
            padding: "10px 0", borderBottom: "1px solid #F4F1E8",
          }}>
            <div className="flex items-center justify-between">
              <span style={{ fontSize: 13, color: row.rare ? "#9A2B14" : "#0F0F0E", flex: 1 }}>{row.name}</span>
              <span style={{ fontFamily: FONT_MONO, fontSize: 12, fontWeight: 500, color: "#0F0F0E" }}>
                {denomToDisplay(row.denom)}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span style={{ fontFamily: FONT_MONO, fontSize: 11, color: "#B7B2A3" }}>
                {printRunDisplay(row.printRun)}
              </span>
              <span style={{ fontFamily: FONT_MONO, fontSize: 11, color: "#6B6757", width: 90, textAlign: "right" }}>
                {perBoxStr(row.denom, ppb)}
              </span>
            </div>
          </div>
        ))}
      </div>
    </>
  );
}

// ─── Shared Odds Table ──────────────────────────────────────────────────────────

function printRunDisplay(pr: number | null | undefined): string {
  if (pr === undefined || pr === null) return "—";
  if (pr === 1) return "1/1";
  return `/${pr}`;
}

function OddsTable({ rows, ppb, headers, showNumbered = false }: {
  rows: OddsRow[]; ppb: number; headers: [string, string, string]; showNumbered?: boolean;
}) {
  return (
    <>
      {/* Desktop */}
      <div className="hidden min-[1180px]:block">
        <table className="w-full" style={{ fontSize: 13 }}>
          <thead>
            <tr>
              <th style={{
                textAlign: "left", padding: "10px 10px",
                fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6,
                color: "#6B6757", borderBottom: "1px solid #EDEAE0", textTransform: "uppercase",
              }}>{headers[0]}</th>
              {showNumbered && (
                <th style={{
                  textAlign: "right", padding: "10px 10px",
                  fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6,
                  color: "#6B6757", borderBottom: "1px solid #EDEAE0", textTransform: "uppercase",
                  width: 70,
                }}>NUMBERED</th>
              )}
              <th style={{
                textAlign: "right", padding: "10px 10px",
                fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6,
                color: "#6B6757", borderBottom: "1px solid #EDEAE0", textTransform: "uppercase",
                width: 100,
              }}>{headers[1]}</th>
              <th style={{
                textAlign: "right", padding: "10px 10px",
                fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6,
                color: "#6B6757", borderBottom: "1px solid #EDEAE0", textTransform: "uppercase",
                width: 160,
              }}>{headers[2]}</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.name} style={{ borderBottom: "1px solid #F4F1E8" }}>
                <td style={{ padding: "12px 10px", color: row.rare ? "#9A2B14" : "#0F0F0E" }}>{row.name}</td>
                {showNumbered && (
                  <td style={{ padding: "12px 10px", textAlign: "right", fontFamily: FONT_MONO, color: "#B7B2A3" }}>
                    {printRunDisplay(row.printRun)}
                  </td>
                )}
                <td style={{ padding: "12px 10px", textAlign: "right", fontFamily: FONT_MONO, color: row.rare ? "#9A2B14" : "#0F0F0E" }}>
                  {denomToDisplay(row.denom)}
                </td>
                <td style={{ padding: "12px 10px", textAlign: "right", fontFamily: FONT_MONO, color: "#6B6757" }}>
                  {perBoxStr(row.denom, ppb)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {/* Mobile */}
      <div className="min-[1180px]:hidden space-y-0">
        {rows.map((row) => (
          <div key={row.name} className="flex flex-col gap-0.5" style={{
            padding: "10px 0", borderBottom: "1px solid #F4F1E8",
          }}>
            <div className="flex items-center">
              <span style={{ flex: 1, fontSize: 13, color: row.rare ? "#9A2B14" : "#0F0F0E" }}>{row.name}</span>
              <span style={{ fontFamily: FONT_MONO, fontSize: 12, fontWeight: 500, color: row.rare ? "#9A2B14" : "#0F0F0E" }}>
                {denomToDisplay(row.denom)}
              </span>
            </div>
            <div className="flex items-center justify-between">
              {showNumbered && (
                <span style={{ fontFamily: FONT_MONO, fontSize: 11, color: "#B7B2A3" }}>
                  {printRunDisplay(row.printRun)}
                </span>
              )}
              <span style={{ fontFamily: FONT_MONO, fontSize: 11, color: "#6B6757", width: 90, textAlign: "right", marginLeft: "auto" }}>
                {perBoxStr(row.denom, ppb)}
              </span>
            </div>
          </div>
        ))}
      </div>
    </>
  );
}

function EmptyTab({ label }: { label: string }) {
  return (
    <div style={{
      padding: "40px 20px", textAlign: "center", fontSize: 13,
      fontStyle: "italic", color: "#8A8677",
    }}>{label}</div>
  );
}

// ─── Main Component ─────────────────────────────────────────────────────────────

export function SetDetailClient({
  setName, sport, league, tier, releaseDate, setId, setSlug, sampleImageUrl,
  cards, cardTypes, parallelTypes, autographs, autoParallels, totalParallels, athleteCount,
  hasChecklist, hasNumberedParallels, hasBoxConfig, hasPackOdds,
  boxConfig, packOdds, entries, hasTeamData, breakSheetPlayers, parallelsList,
}: SetDetailClientProps) {
  const [tab, setTab] = useState<Tab>("Box Config");
  const [drawerOpen, setDrawerOpen] = useState(false);

  const meta = useMemo(() => extractMeta(setName, sport), [setName, sport]);
  const oddsFormats = useMemo(
    () => packOdds ? buildOddsFormats(packOdds, boxConfig, parallelsList) : [],
    [packOdds, boxConfig, parallelsList]
  );

  const statItems = [
    { label: "Cards", value: cards },
    { label: "Card Types", value: cardTypes },
    { label: "Parallel Types", value: parallelTypes },
    { label: "Autographs", value: autographs },
    { label: "Auto Parallels", value: autoParallels },
    { label: "Total Parallels", value: totalParallels },
  ];

  const eyebrow = [
    league || sport,
    meta.manufacturer,
    meta.brand !== meta.manufacturer ? meta.brand : null,
    releaseDate ? formatDateShort(releaseDate) : null,
  ].filter(Boolean).join(" · ");

  return (
    <div style={{ background: "#FAFAF7", minHeight: "100vh" }}>
      {/* ═══ DESKTOP ═══ */}
      <div className="hidden min-[1180px]:grid" style={{ gridTemplateColumns: "425px 1fr", minHeight: "100vh" }}>
        {/* Left rail */}
        <aside className="sticky top-0 h-screen overflow-y-auto" style={{ borderRight: "1px solid #EDEAE0" }}>
          <AthletesRail entries={entries} hasTeamData={hasTeamData} setId={setId} setSlug={setSlug} />
        </aside>
        {/* Right column */}
        <div className="flex flex-col">
          {/* Hero */}
          <div style={{ background: "#FFFFFF", padding: "30px 36px", borderBottom: "1px solid #EDEAE0" }}>
            <div className="grid items-center gap-8" style={{
              gridTemplateColumns: sampleImageUrl ? "140px 1fr 280px" : "1fr 280px",
            }}>
              {/* Featured card */}
              {sampleImageUrl && (
                <div className="flex items-center justify-center">
                  <img src={sampleImageUrl} alt={setName}
                    style={{
                      width: 122, height: 172, objectFit: "cover",
                      transform: "rotate(-3deg)",
                      boxShadow: "0 12px 28px rgba(15,15,14,0.18)",
                    }} />
                </div>
              )}
              {/* Title block */}
              <div>
                <div style={{ fontFamily: FONT_MONO, fontSize: 10, fontWeight: 600, letterSpacing: 2.4, color: "#8A8677", textTransform: "uppercase" }}>
                  {eyebrow}
                </div>
                <h1 style={{
                  fontFamily: FONT_DISPLAY, fontSize: 42, fontWeight: 600,
                  letterSpacing: -1.2, lineHeight: 1.02, color: "#0F0F0E", margin: "8px 0 12px",
                }}>{setName}</h1>
                <div className="flex flex-wrap items-center gap-2">
                  <span style={{ fontSize: 12, fontWeight: 500, padding: "4px 9px", borderRadius: 4, border: "1px solid #E6E3D9", color: "#3A372F" }}>
                    {sport}
                  </span>
                  {league && (
                    <span style={{ fontSize: 12, fontWeight: 500, padding: "4px 9px", borderRadius: 4, border: "1px solid #E6E3D9", color: "#3A372F" }}>
                      {league}
                    </span>
                  )}
                  <span style={{ fontSize: 12, fontWeight: 600, padding: "4px 9px", borderRadius: 4, background: "#0F0F0E", color: "#FAFAF7" }}>
                    {meta.manufacturer || "Topps"}
                  </span>
                  <span style={{ fontSize: 12, color: "#6B6757" }}>
                    {athleteCount.toLocaleString()} athletes tracked
                  </span>
                </div>
              </div>
              {/* Coverage card */}
              <CoverageCard
                hasChecklist={hasChecklist} hasNumberedParallels={hasNumberedParallels}
                hasBoxConfig={hasBoxConfig} hasPackOdds={hasPackOdds}
                breakSheetPlayers={breakSheetPlayers} setName={setName} sport={sport} league={league}
              />
            </div>
          </div>

          {/* Stat strip */}
          <StatStrip items={statItems} />

          {/* Primary tabs */}
          <div role="tablist" style={{
            background: "#FAFAF7", padding: "0 36px", borderBottom: "1px solid #EDEAE0",
            display: "flex",
          }}>
            {TABS.map((t) => (
              <button key={t} role="tab" aria-selected={tab === t}
                onClick={() => setTab(t)}
                style={{
                  padding: "14px 20px",
                  fontFamily: FONT_DISPLAY,
                  fontSize: 14, fontWeight: tab === t ? 600 : 500,
                  color: tab === t ? "#0F0F0E" : "#8A8677",
                  borderBottom: tab === t ? "2px solid #0F0F0E" : "2px solid transparent",
                  marginBottom: -1, background: "transparent", cursor: "pointer",
                  transition: "all 150ms",
                }}>
                {t}
              </button>
            ))}
          </div>

          {/* Content area */}
          <div style={{ padding: "28px 36px 60px" }}>
            {tab === "Box Config" && <BoxConfigContent boxConfig={boxConfig} />}
            {tab === "Pack Odds" && <PackOddsContent formats={oddsFormats} />}
            {tab === "Inserts" && <InsertsContent formats={oddsFormats} />}
            {tab === "Autographs" && <AutosContent formats={oddsFormats} />}
          </div>
        </div>
      </div>

      {/* ═══ MOBILE ═══ */}
      <div className="min-[1180px]:hidden">
        {/* Sticky app bar */}
        <div className="sticky top-0 z-10 flex items-center justify-between"
          style={{
            padding: "12px 16px", borderBottom: "1px solid #EDEAE0",
            background: "rgba(250,250,247,0.92)", backdropFilter: "blur(12px)", WebkitBackdropFilter: "blur(12px)",
          }}>
          <button onClick={() => setDrawerOpen(true)}
            style={{
              display: "flex", alignItems: "center", gap: 6,
              background: "#FFFFFF", border: "1px solid #E6E3D9", borderRadius: 8,
              padding: "8px 12px", fontSize: 12, fontWeight: 500, color: "#0F0F0E",
            }}>
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M15 19.128a9.38 9.38 0 0 0 2.625.372 9.337 9.337 0 0 0 4.121-.952 4.125 4.125 0 0 0-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128H5.228A2 2 0 0 1 3 17.208V5.792A2 2 0 0 1 5.228 3.872h13.544A2 2 0 0 1 21 5.792v6.625M12 10.5a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0Z" />
            </svg>
            Athletes <span style={{ color: "#8A8677" }}>· {athleteCount}</span>
          </button>
          <div className="v2-break-sheet-pill">
            <BreakSheetModal setName={setName} sport={sport} league={league} players={breakSheetPlayers} />
          </div>
        </div>

        {/* Hero */}
        <div style={{ background: "#FFFFFF", padding: "18px 16px 14px", borderBottom: "1px solid #EDEAE0" }}>
          <div className="flex items-start gap-4">
            {sampleImageUrl && (
              <div className="flex-shrink-0">
                <img src={sampleImageUrl} alt={setName}
                  style={{
                    width: 78, height: 108, objectFit: "cover",
                    transform: "rotate(-3deg)",
                    boxShadow: "0 8px 18px rgba(15,15,14,0.18)",
                  }} />
              </div>
            )}
            <div className="flex-1 min-w-0">
              <div style={{ fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 2, color: "#8A8677", textTransform: "uppercase" }}>
                {eyebrow}
              </div>
              <h1 style={{
                fontFamily: FONT_DISPLAY, fontSize: 24, fontWeight: 600,
                letterSpacing: -0.6, lineHeight: 1.1, color: "#0F0F0E", margin: "6px 0 8px",
              }}>{setName}</h1>
              <div className="flex flex-wrap items-center gap-1.5">
                <span style={{ fontSize: 11, fontWeight: 500, padding: "3px 7px", borderRadius: 4, border: "1px solid #E6E3D9", color: "#3A372F" }}>
                  {sport}
                </span>
                {league && (
                  <span style={{ fontSize: 11, fontWeight: 500, padding: "3px 7px", borderRadius: 4, border: "1px solid #E6E3D9", color: "#3A372F" }}>
                    {league}
                  </span>
                )}
                <span style={{ fontSize: 11, color: "#6B6757" }}>
                  {athleteCount.toLocaleString()} athletes
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Stat grid (mobile) */}
        <StatStrip items={statItems} />

        {/* Sticky tabs */}
        <div role="tablist" className="sticky z-[5] overflow-x-auto no-scrollbar"
          style={{
            top: 53, background: "#FAFAF7", padding: "0 16px",
            borderBottom: "1px solid #EDEAE0", display: "flex", whiteSpace: "nowrap",
          }}>
          {TABS.map((t) => (
            <button key={t} role="tab" aria-selected={tab === t}
              onClick={() => setTab(t)}
              style={{
                padding: "12px 14px", flexShrink: 0,
                fontFamily: FONT_DISPLAY,
                fontSize: 14, fontWeight: tab === t ? 600 : 500,
                color: tab === t ? "#0F0F0E" : "#8A8677",
                borderBottom: tab === t ? "2px solid #0F0F0E" : "2px solid transparent",
                marginBottom: -1, background: "transparent", cursor: "pointer",
              }}>
              {t}
            </button>
          ))}
        </div>

        {/* Content */}
        <div style={{ padding: 16 }}>
          {tab === "Box Config" && <BoxConfigContent boxConfig={boxConfig} />}
          {tab === "Pack Odds" && <PackOddsContent formats={oddsFormats} />}
          {tab === "Inserts" && <InsertsContent formats={oddsFormats} />}
          {tab === "Autographs" && <AutosContent formats={oddsFormats} />}
        </div>

        {/* Athletes drawer */}
        <MobileAthletesDrawer
          open={drawerOpen} onClose={() => setDrawerOpen(false)}
          entries={entries} hasTeamData={hasTeamData} setId={setId} setSlug={setSlug}
          athleteCount={athleteCount}
        />
      </div>
    </div>
  );
}
