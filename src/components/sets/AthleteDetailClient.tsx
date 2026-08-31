"use client";

import React, { useState, useMemo, useRef, useEffect } from "react";
import Link from "next/link";
import type { LeaderboardRow, InsertSetDetail } from "./types";
import { PackOddsCalculator, type PackOddsSlot, type BoxFormat } from "@/components/PackOddsCalculator";
import { getNBAHeadshotUrl } from "@/lib/nba-headshot";
import { getUFCHeadshotUrl } from "@/lib/ufc-headshot";
import { getMLBHeadshotUrl } from "@/lib/mlb-headshot";
import { trackEvent } from "@/lib/trackEvent";
import { trackEvent as trackGaEvent } from "@/lib/analytics";
import { getTeamLogo } from "@/lib/utils/teamLogo";
import { findOddsKey, lookupOddsValue } from "@/lib/oddsUtils";
import { SubsetCard } from "./SubsetCard";
import type { ParallelRowData } from "./ParallelTable";
import { buildEbaySearchUrl } from "@/lib/ebay/searchUrl";

// ─── Constants ──────────────────────────────────────────────────────────────────

const FONT_DISPLAY = "var(--cl-font-display), 'Inter Tight', sans-serif";
const FONT_MONO = "var(--cl-font-mono), 'JetBrains Mono', ui-monospace, monospace";

type Tab = "Overview" | "Card Types" | "Base Parallels" | "Inserts" | "Autographs" | "Also Featured In";
type SortKey = "totalCards" | "autographs" | "inserts" | "numberedParallels";
const TABS: Tab[] = ["Overview", "Card Types", "Base Parallels", "Inserts", "Autographs", "Also Featured In"];
const SORT_CHIPS: { key: SortKey; label: string }[] = [
  { key: "totalCards", label: "Total Cards" },
  { key: "autographs", label: "Autos" },
  { key: "inserts", label: "Inserts" },
  { key: "numberedParallels", label: "Numbered" },
];

// ─── Types ──────────────────────────────────────────────────────────────────────

interface OtherSet {
  id: number;
  name: string;
  slug: string | null;
  sport: string;
  totalCards: number;
  autographs: number;
  parallels: number;
}

export interface AthleteDetailClientProps {
  // Athlete identity
  athleteName: string;
  athleteId: number;
  athleteSlug: string | null;
  teams: string[];
  hasRookie: boolean;
  nbaPlayerId: number | null;
  ufcImageUrl: string | null;
  mlbPlayerId: number | null;
  imageUrl: string | null;
  // Set context
  setName: string;
  setSlug: string;
  setId: number;
  sport: string;
  league: string | null;
  // Stats
  cardTypes: number;
  totalCards: number;
  autographs: number;
  autoParallels: number;
  numberedParallels: number;
  oneOfOnes: number;
  // Data
  insertSets: InsertSetDetail[];
  otherSets: OtherSet[];
  // Pack odds and box config (raw JSON)
  packOddsJson: string | null;
  boxConfigJson: string | null;
  epnCampaignId: string | null;
  // Break Hit Calculator
  packOddsSlotsByFormat: Record<string, PackOddsSlot[]>;
  boxFormats: BoxFormat[];
  totalAutoCards: number;
  playerAutoCards: number;
  hasBreakCalc: boolean;
  // Leaderboard
  entries: LeaderboardRow[];
  hasTeamData: boolean;
  subjectLabel?: string;
  subjectRole?: string;
  teamLabel?: string;
}

// ─── Helpers ────────────────────────────────────────────────────────────────────

function InitialsAvatar({ name, size = 30 }: { name: string; size?: number }) {
  const initials = name.split(" ").map((n) => n[0]).slice(0, 2).join("").toUpperCase();
  return (
    <div className="rounded-full flex items-center justify-center flex-shrink-0"
      style={{ width: size, height: size, background: "#EAE6D9", color: "#C4BEAD", fontSize: size * 0.35, fontWeight: 600 }}>
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

function displayOdds(odds: string | number | null): string {
  if (odds == null) return "—";
  if (typeof odds === "number") return `1:${odds.toLocaleString()}`;
  return String(odds);
}

function parallelTone(name: string): string {
  const l = name.toLowerCase();
  if (l.includes("gold") || l.includes("superfractor")) return "#B8860B";
  if (l.includes("red")) return "#9A2B14";
  if (l.includes("black")) return "#1A1A1A";
  if (l.includes("green")) return "#0E8A4F";
  if (l.includes("blue") || l.includes("aqua") || l.includes("teal")) return "#1E6B8A";
  if (l.includes("orange")) return "#C28A18";
  if (l.includes("purple")) return "#6B3FA0";
  return "#8A8677";
}

// ─── Athletes Rail ──────────────────────────────────────────────────────────────

function TeamLogoAvatar({ teamName, sport, size = 24 }: { teamName: string; sport: string; size?: number }) {
  const src = getTeamLogo(teamName, sport);
  const [err, setErr] = useState(false);
  if (!src || err) return <InitialsAvatar name={teamName} size={size} />;
  return <img src={src} alt={`${teamName} logo`} width={size} height={size}
    loading="lazy" decoding="async" className="flex-shrink-0"
    onError={() => setErr(true)} style={{ width: size, height: size, objectFit: "contain" }} />;
}

function AthletesRail({ entries, hasTeamData, setId, setSlug, currentAthleteId, subjectLabel = "Athletes", teamLabel = "Team", sport = "" }: {
  entries: LeaderboardRow[]; hasTeamData: boolean; setId: number; setSlug: string; currentAthleteId: number; subjectLabel?: string; teamLabel?: string; sport?: string;
}) {
  const [sortKey, setSortKey] = useState<SortKey>("totalCards");
  const [rookiesOnly, setRookiesOnly] = useState(false);
  const [viewMode, setViewMode] = useState<"athletes" | "teams">("athletes");
  const [query, setQuery] = useState("");
  const [showAll, setShowAll] = useState(false);

  const filtered = useMemo(() => {
    let list = entries;
    if (query.trim()) {
      const q = query.trim().toLowerCase();
      list = list.filter((e) => e.name.toLowerCase().includes(q) || (e.team?.toLowerCase().includes(q)));
    }
    if (viewMode === "athletes" && rookiesOnly) list = list.filter((e) => e.isRookie);
    return [...list].sort((a, b) => {
      const diff = b[sortKey] - a[sortKey];
      return diff !== 0 ? diff : a.name.localeCompare(b.name);
    });
  }, [entries, query, rookiesOnly, sortKey, viewMode]);

  const teamRows = useMemo(() => {
    if (viewMode !== "teams") return [];
    const map = new Map<string, { team: string; athleteCount: number; totalCards: number; autographs: number; inserts: number; numberedParallels: number }>();
    const source = query.trim()
      ? entries.filter((e) => e.name.toLowerCase().includes(query.trim().toLowerCase()) || (e.team?.toLowerCase().includes(query.trim().toLowerCase())))
      : entries;
    for (const e of source) {
      const t = e.team ?? "Unknown";
      if (!map.has(t)) map.set(t, { team: t, athleteCount: 0, totalCards: 0, autographs: 0, inserts: 0, numberedParallels: 0 });
      const r = map.get(t)!;
      r.athleteCount++; r.totalCards += e.totalCards; r.autographs += e.autographs; r.inserts += e.inserts; r.numberedParallels += e.numberedParallels;
    }
    return Array.from(map.values()).sort((a, b) => b[sortKey] - a[sortKey] || a.team.localeCompare(b.team));
  }, [entries, query, sortKey, viewMode]);

  const teamCount = useMemo(() => new Set(entries.map((e) => e.team).filter(Boolean)).size, [entries]);
  const visible = showAll ? filtered : filtered.slice(0, 50);

  return (
    <div className="flex flex-col h-full" style={{ background: "#FFFFFF" }}>
      {hasTeamData && (
        <div className="shrink-0 flex" style={{ borderBottom: "1px solid #EDEAE0", padding: "0 18px" }}>
          {([["athletes", `${subjectLabel} (${entries.length})`], ["teams", `${teamLabel}s (${teamCount})`]] as const).map(([mode, label]) => (
            <button key={mode} onClick={() => { setViewMode(mode); setShowAll(false); }}
              style={{
                padding: "12px 16px", fontFamily: FONT_DISPLAY, fontSize: 16,
                fontWeight: viewMode === mode ? 600 : 500,
                color: viewMode === mode ? "var(--brand-ink)" : "#8A8677",
                borderBottom: viewMode === mode ? "2px solid var(--brand-accent)" : "2px solid transparent",
                marginBottom: -1, background: "transparent", cursor: "pointer", transition: "all 150ms",
              }}>{label}</button>
          ))}
        </div>
      )}
      <div className="shrink-0 space-y-3" style={{ padding: "14px 18px 12px" }}>
        <div className="relative">
          <svg className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 pointer-events-none" style={{ color: "#8A8677" }}
            fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
            <path strokeLinecap="round" strokeLinejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
          </svg>
          <input type="text" value={query} onChange={(e) => setQuery(e.target.value)}
            placeholder={viewMode === "teams" ? `Search ${teamLabel.toLowerCase()}s…` : `Search ${subjectLabel.toLowerCase()}…`}
            autoComplete="off" spellCheck={false} className="w-full outline-none"
            style={{ background: "#F1EFE9", borderRadius: 8, padding: "7px 10px 7px 30px", fontSize: 16, border: "none", color: "var(--brand-ink)" }} />
        </div>
        <div className="flex flex-wrap gap-1.5">
          {SORT_CHIPS.map((chip) => (
            <button key={chip.key} onClick={() => setSortKey(chip.key)}
              style={{
                borderRadius: 4, padding: "4px 9px", fontSize: 16, fontWeight: 500,
                background: sortKey === chip.key ? "var(--brand-ink)" : "transparent",
                color: sortKey === chip.key ? "#FAFAF7" : "#3A372F",
                border: sortKey === chip.key ? "1px solid var(--brand-ink)" : "1px solid #E6E3D9",
              }}>{chip.label}</button>
          ))}
        </div>
        {viewMode === "athletes" && (
          <label className="flex items-center gap-1.5 cursor-pointer" style={{ fontSize: 16, color: "#3A372F" }}>
            <input type="checkbox" checked={rookiesOnly} onChange={() => setRookiesOnly((v) => !v)} style={{ accentColor: "var(--brand-ink)" }} />
            Rookies only
          </label>
        )}
      </div>
      <div className="shrink-0 flex justify-between items-center" style={{
        padding: "6px 18px", borderBottom: "1px solid #EDEAE0",
        fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6, color: "#8A8677", textTransform: "uppercase",
      }}>
        <span>{viewMode === "teams" ? teamLabel.toUpperCase() : "ATHLETE"}</span>
        <span>{SORT_CHIPS.find((c) => c.key === sortKey)?.label}</span>
      </div>
      <div className="flex-1 overflow-y-auto">
        {viewMode === "athletes" ? (
          visible.length === 0 ? <p className="text-center py-8" style={{ fontSize: 16, color: "#8A8677", fontStyle: "italic" }}>No {subjectLabel.toLowerCase()} match.</p> : (
            <>
              {visible.map((entry, idx) => {
                const isActive = entry.id === currentAthleteId;
                return (
                  <Link key={entry.id} href={`/sets/${setSlug || setId}/athlete/${entry.slug || entry.id}`}
                    // Search selection → "search" only when a query is active; the
                    // page visit itself is counted as a "view" on mount.
                    onClick={() => { if (query.trim()) trackEvent(entry.id, "search"); }}
                    className="flex items-center gap-2 transition-colors"
                    style={{
                      padding: "9px 18px", borderBottom: "1px solid #F4F1E8", textDecoration: "none",
                      background: isActive ? "#F4F1E8" : "transparent",
                      borderLeft: isActive ? "2px solid var(--brand-ink)" : "2px solid transparent",
                    }}>
                    <span style={{ fontFamily: FONT_MONO, fontSize: 16, color: "#8A8677", width: 18, textAlign: "right", flexShrink: 0 }}>{idx + 1}</span>
                    <PlayerAvatar name={entry.name} nbaPlayerId={entry.nbaPlayerId} ufcImageUrl={entry.ufcImageUrl}
                      mlbPlayerId={entry.mlbPlayerId} imageUrl={entry.imageUrl} size={30} />
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-1.5 min-w-0">
                        <span className="truncate" style={{ fontSize: 16, fontWeight: 500, color: "var(--brand-ink)" }}>{entry.name}</span>
                        {entry.isRookie && (
                          <span className="shrink-0" style={{ background: "oklch(0.55 0.17 25)", color: "#FFF8F1", fontSize: 9, fontWeight: 700, padding: "1px 5px", borderRadius: 2 }}>RC</span>
                        )}
                      </div>
                      {hasTeamData && entry.team && <p className="truncate" style={{ fontSize: 16, color: "#6B6757", marginTop: 1 }}>{entry.team}</p>}
                    </div>
                    <span style={{ fontFamily: FONT_MONO, fontSize: 16, fontWeight: 600, color: "var(--brand-ink)", flexShrink: 0 }}>{entry[sortKey].toLocaleString()}</span>
                  </Link>
                );
              })}
              {!showAll && filtered.length > 50 && <button onClick={() => setShowAll(true)} className="w-full py-3" style={{ fontSize: 16, fontWeight: 600, color: "var(--brand-ink)" }}>Show all {filtered.length} {subjectLabel.toLowerCase()}</button>}
            </>
          )
        ) : (
          teamRows.length === 0 ? <p className="text-center py-8" style={{ fontSize: 16, color: "#8A8677", fontStyle: "italic" }}>No teams match.</p> : (
            (showAll ? teamRows : teamRows.slice(0, 50)).map((tr, idx) => (
              <Link key={tr.team} href={`/sets/${setSlug || setId}/team/${tr.team.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "")}`}
                className="flex items-center gap-2 transition-colors"
                style={{ padding: "9px 18px", borderBottom: "1px solid #F4F1E8", textDecoration: "none" }}
                onMouseEnter={(e) => { (e.currentTarget as HTMLElement).style.background = "#F1EFE9"; }}
                onMouseLeave={(e) => { (e.currentTarget as HTMLElement).style.background = "transparent"; }}>
                <span style={{ fontFamily: FONT_MONO, fontSize: 16, color: "#8A8677", width: 18, textAlign: "right", flexShrink: 0 }}>{idx + 1}</span>
                <TeamLogoAvatar teamName={tr.team} sport={sport} size={30} />
                <div className="flex-1 min-w-0">
                  <span className="truncate block" style={{ fontSize: 16, fontWeight: 500, color: "var(--brand-ink)" }}>{tr.team}</span>
                  <p className="truncate" style={{ fontSize: 16, color: "#6B6757", marginTop: 1 }}>{tr.athleteCount} {tr.athleteCount === 1 ? "Athlete" : "Athletes"}</p>
                </div>
                <span style={{ fontFamily: FONT_MONO, fontSize: 16, fontWeight: 600, color: "var(--brand-ink)", flexShrink: 0 }}>{tr[sortKey].toLocaleString()}</span>
              </Link>
            ))
          )
        )}
      </div>
    </div>
  );
}

// ─── Insert Sets Accordion (Overview Tab) ───────────────────────────────────────

function InsertSetsAccordion({ insertSets, setSlug, setId }: {
  insertSets: InsertSetDetail[]; setSlug: string; setId: number;
}) {
  const [openSet, setOpenSet] = useState<string | null>(insertSets[0]?.insertSetName ?? null);

  return (
    <div>
      <h3 style={{ fontFamily: FONT_DISPLAY, fontSize: 16, fontWeight: 600, color: "var(--brand-ink)", marginBottom: 12 }}>
        Card Types ({insertSets.length})
      </h3>
      <div style={{ border: "1px solid #EDEAE0", borderRadius: 8, overflow: "hidden" }}>
        {insertSets.map((is) => {
          const isOpen = openSet === is.insertSetName;
          return (
            <div key={is.insertSetId} style={{ borderBottom: "1px solid #F4F1E8" }}>
              <button onClick={() => setOpenSet(isOpen ? null : is.insertSetName)}
                className="w-full flex items-center justify-between"
                style={{ padding: "14px 18px", background: "#FFFFFF", textAlign: "left", cursor: "pointer", border: "none" }}>
                <span style={{ fontSize: 16, fontWeight: 500, color: "var(--brand-ink)" }}>{is.insertSetName}</span>
                <div className="flex items-center gap-3">
                  <span style={{ fontFamily: FONT_MONO, fontSize: 16, color: "#8A8677" }}>
                    {is.appearances.length} card{is.appearances.length !== 1 ? "s" : ""} · {is.parallels.length} parallels
                  </span>
                  <svg style={{ transform: isOpen ? "rotate(180deg)" : "rotate(0)", transition: "transform 150ms" }}
                    width={12} height={12} fill="none" viewBox="0 0 24 24" stroke="#8A8677" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
                  </svg>
                </div>
              </button>
              {isOpen && (
                <div style={{ padding: "0 18px 14px", background: "#FFFFFF" }}>
                  {is.appearances.map((app) => (
                    <div key={`${is.insertSetId}-${app.cardNumber}`} style={{ padding: "8px 0", borderTop: "1px solid #F4F1E8" }}>
                      <div className="flex items-center gap-2">
                        <span style={{
                          fontFamily: FONT_MONO, fontSize: 16, fontWeight: 600,
                          background: "#F1EFE9", padding: "3px 7px", borderRadius: 3, color: "var(--brand-ink)",
                        }}>#{app.cardNumber}</span>
                        <span style={{ fontSize: 16, color: "#3A372F" }}>{app.team}</span>
                        {app.subsetTag && <span style={{ fontSize: 16, color: "#8A8677" }}>({app.subsetTag})</span>}
                      </div>
                      {is.parallels.length > 0 && (
                        <div className="flex flex-wrap gap-1.5 mt-2">
                          {is.parallels.map((p) => (
                            <span key={p.id} style={{
                              fontSize: 16, fontWeight: 500, padding: "3px 8px", borderRadius: 4,
                              background: parallelTone(p.name) + "18", color: parallelTone(p.name),
                              border: `1px solid ${parallelTone(p.name)}30`,
                            }}>
                              {p.name}{p.printRun != null ? ` /${p.printRun}` : ""}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ─── Shared Odds Helpers ─────────────────────────────────────────────────────────

const BOX_LABEL_MAP: Record<string, string> = {
  hobby: "Hobby", jumbo: "Jumbo", breakers_delight: "Breaker's Delight",
  fdi: "First Day Issue", sapphire: "Sapphire", fanatics: "Fanatics",
  value_se: "Value", value_ea: "Value", value_cee: "Value", value: "Value",
  mega_se: "Mega", mega_ea: "Mega", mega_cee: "Mega", mega: "Mega",
  hanger_se: "Hanger", hanger_ea: "Hanger", hanger: "Hanger",
};

const BOX_FORMAT_ORDER = [
  { key: "hobby", label: "Hobby" },
  { key: "fdi", label: "FDI" },
  { key: "jumbo", label: "Jumbo" },
  { key: "breakers_delight", label: "Breaker's" },
  { key: "value_se", label: "Value" }, { key: "value_ea", label: "Value" },
  { key: "value_cee", label: "Value" }, { key: "value", label: "Value" },
  { key: "mega_se", label: "Mega" }, { key: "mega_ea", label: "Mega" },
  { key: "mega_cee", label: "Mega" }, { key: "mega", label: "Mega" },
  { key: "hanger_se", label: "Hanger" }, { key: "hanger_ea", label: "Hanger" },
  { key: "hanger", label: "Hanger" },
  { key: "fanatics", label: "Fanatics" },
  { key: "sapphire", label: "Sapphire" },
];

// Sets that get the multi-column odds layout
function normalizeParallelNameShared(name: string): string[] {
  const candidates = [name];
  if (name.endsWith(" Refractor")) candidates.push(name.replace(/ Refractor$/, ""));
  candidates.push(name.replace("RayWave", "Ray Wave"));
  // X-Fractor (hyphen) → Xfractor (no hyphen) and vice versa
  if (name.includes("X-Fractor")) {
    candidates.push(name.replace(/X-Fractor/g, "Xfractor"));
    if (!name.includes("X-Fractor Refractor"))
      candidates.push(name.replace("X-Fractor", "X-Fractor Refractor"));
  }
  if (name.includes("Xfractor") && !name.includes("X-Fractor")) {
    candidates.push(name.replace(/Xfractor/g, "X-Fractor"));
    if (!name.includes("Xfractor Refractor"))
      candidates.push(name.replace("Xfractor", "Xfractor Refractor"));
  }
  return [...new Set(candidates)];
}

// ─── Subset tab (shared checklist table + eBay affiliate column) ─────────────────

function AthleteShopDisclosure() {
  return (
    <p style={{ fontSize: 12, color: "#8A8677", marginTop: 4 }}>
      Checklist² earns a commission on qualifying eBay purchases through these links.
    </p>
  );
}

/**
 * One athlete tab (Card Types / Base Parallels / Inserts / Autographs). Groups the
 * player's rows by subset in set-page order and renders each with the shared
 * SubsetCard + ParallelTable (identical to the set page) plus an eBay affiliate
 * column. The format chip strip selects which format's odds show; there is no
 * per-box computation.
 */
function AthleteSubsetTab({ insertSets, packOddsJson, playerName, setName, setId, athleteId, epnCampaignId }: {
  insertSets: InsertSetDetail[]; packOddsJson: string | null;
  playerName: string; setName: string; setId: number; athleteId: number; epnCampaignId: string | null;
}) {
  const [activeIdx, setActiveIdx] = useState(0);

  const formats = useMemo(() => {
    const fmts: { key: string; label: string }[] = [];
    if (packOddsJson) {
      try {
        const raw = JSON.parse(packOddsJson);
        const firstVal = Object.values(raw)[0];
        if (typeof firstVal === "object" && firstVal !== null) {
          const seen = new Set<string>();
          for (const key of Object.keys(raw)) {
            const label = BOX_LABEL_MAP[key] ?? key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
            if (!seen.has(label)) { seen.add(label); fmts.push({ key, label }); }
          }
        } else {
          fmts.push({ key: "hobby", label: "Hobby" });
        }
      } catch { /* ignore */ }
    }
    return fmts;
  }, [packOddsJson]);

  const activeFormat = formats[activeIdx] ?? formats[0];
  const activeOdds = useMemo(() => {
    if (!packOddsJson || !activeFormat) return {} as Record<string, string | number>;
    try {
      const raw = JSON.parse(packOddsJson);
      const firstVal = Object.values(raw)[0];
      if (typeof firstVal === "object" && firstVal !== null) return (raw[activeFormat.key] ?? {}) as Record<string, string | number>;
      return raw as Record<string, string | number>;
    } catch { return {} as Record<string, string | number>; }
  }, [packOddsJson, activeFormat]);

  function lookupOdds(cardType: string, parallelName: string | null): string | number | null {
    const names = parallelName ? normalizeParallelNameShared(parallelName) : [null];
    for (const n of names) {
      const r = lookupOddsValue(activeOdds, cardType, n as string | null);
      if (r != null) return r;
      if (n) {
        const b = lookupOddsValue(activeOdds, "Base", n);
        if (b != null) return b;
        const fk = findOddsKey(n, Object.keys(activeOdds));
        if (fk && activeOdds[fk] != null) return activeOdds[fk];
      }
    }
    return null;
  }

  const subsets = useMemo(() => [...insertSets].sort((a, b) => a.insertSetId - b.insertSetId), [insertSets]);
  if (subsets.length === 0) return (
    <div style={{ padding: "40px 20px", textAlign: "center", fontSize: 16, fontStyle: "italic", color: "#8A8677" }}>
      No cards in this category
    </div>
  );

  return (
    <div className="space-y-4">
      {formats.length > 1 && (
        <div className="flex flex-wrap gap-1.5">
          {formats.map((f, i) => (
            <button key={f.key} onClick={() => setActiveIdx(i)}
              style={{
                borderRadius: 999, padding: "7px 12px", fontSize: 16, fontWeight: 600,
                background: i === activeIdx ? "var(--brand-ink)" : "#FFFFFF",
                color: i === activeIdx ? "#FAFAF7" : "#3A372F",
                border: i === activeIdx ? "1px solid var(--brand-ink)" : "1px solid #EDEAE0",
              }}>{f.label}</button>
          ))}
        </div>
      )}

      {subsets.map((is) => {
        const isBaseSubset = /^base cards/i.test(is.insertSetName);
        const hasBaseParallel = is.parallels.some((p) => p.name.toLowerCase() === "base");
        const shopFor = (parallel: string, printRun: number | null, parallelId: number | null) =>
          buildEbaySearchUrl({
            setName, player: playerName, subset: isBaseSubset ? null : is.insertSetName,
            parallel, printRun, athleteId, setId, insertSetId: is.insertSetId, parallelId,
          }, epnCampaignId);

        const tableRows: ParallelRowData[] = [];
        if (!hasBaseParallel) {
          const o = lookupOdds(is.insertSetName, null);
          tableRows.push({ name: "Base", printRun: null, odds: o != null ? { text: displayOdds(o) } : null, shopUrl: shopFor("Base", null, null) });
        }
        for (const p of is.parallels) {
          const o = lookupOdds(is.insertSetName, p.name);
          const rare = p.name.toLowerCase().includes("superfractor") || (p.printRun != null && p.printRun <= 5);
          tableRows.push({ name: p.name, printRun: p.printRun, rare, odds: o != null ? { text: displayOdds(o) } : null, shopUrl: shopFor(p.name, p.printRun, p.id) });
        }

        const checklist = (
          <div style={{ border: "1px solid #EDEAE0", borderRadius: 8, overflow: "hidden", background: "#FFFFFF" }}>
            {is.appearances.map((app, i) => (
              <div key={`${is.insertSetId}-${app.cardNumber}-${i}`} className="flex items-center gap-3"
                style={{ padding: "8px 12px", borderTop: i > 0 ? "1px solid #F4F1E8" : "none" }}>
                <span style={{ fontFamily: FONT_MONO, fontSize: 13, color: "#8A8677", minWidth: 54 }}>#{app.cardNumber}</span>
                <span style={{ fontSize: 15, fontWeight: 500, color: "var(--brand-ink)", flex: 1, minWidth: 0 }}>{playerName}</span>
                {app.isRookie && (
                  <span style={{ flexShrink: 0, fontFamily: FONT_MONO, fontSize: 9, fontWeight: 700, letterSpacing: 0.5,
                    color: "#9A2B14", background: "rgba(154,43,20,0.08)", border: "1px solid rgba(154,43,20,0.2)", padding: "1px 5px", borderRadius: 3 }}>RC</span>
                )}
                {app.team && <span style={{ fontSize: 13, color: "#6B6757", flexShrink: 0, textAlign: "right" }}>{app.team}</span>}
              </div>
            ))}
          </div>
        );

        return (
          <SubsetCard key={is.insertSetId} name={is.insertSetName} cardsCount={is.appearances.length}
            parallelsCount={is.parallels.length} checklist={checklist} tableRows={tableRows} showNumbered />
        );
      })}

      {/* Disclosure sits directly below the subset tables, shown only when the
          eBay column is present (i.e. affiliate links were generated). */}
      {epnCampaignId && <AthleteShopDisclosure />}
    </div>
  );
}


// ─── Also Featured In ───────────────��───────────────────────────────────────────

function AlsoFeaturedIn({ otherSets }: { otherSets: OtherSet[] }) {
  if (otherSets.length === 0) return (
    <div style={{ padding: "40px 20px", textAlign: "center", fontSize: 16, fontStyle: "italic", color: "#8A8677" }}>
      Not featured in any other sets
    </div>
  );

  return (
    <div>
      {/* Desktop */}
      <div className="hidden min-[1180px]:block">
        <table className="w-full" style={{ fontSize: 16 }}>
          <thead>
            <tr>
              {["SET", "SPORT", "CARDS", "AUTOS", "PARALLELS"].map((h, i) => (
                <th key={h} style={{
                  textAlign: i === 0 ? "left" : "right", padding: "10px",
                  fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6,
                  color: "#8A8677", borderBottom: "1px solid #EDEAE0", textTransform: "uppercase",
                }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {otherSets.map((s) => (
              <tr key={s.id} style={{ borderBottom: "1px solid #F4F1E8" }}>
                <td style={{ padding: "12px 10px" }}>
                  <Link href={`/sets/${s.slug ?? s.id}`} style={{ color: "var(--brand-ink)", fontWeight: 500, textDecoration: "none" }}>
                    {s.name}
                  </Link>
                </td>
                <td style={{ padding: "12px 10px", textAlign: "right", color: "#6B6757" }}>{s.sport}</td>
                <td style={{ padding: "12px 10px", textAlign: "right", fontFamily: FONT_MONO, fontWeight: 600 }}>{s.totalCards}</td>
                <td style={{ padding: "12px 10px", textAlign: "right", fontFamily: FONT_MONO, fontWeight: 600, color: s.autographs === 0 ? "#B7B2A3" : "var(--brand-ink)" }}>
                  {s.autographs === 0 ? "—" : s.autographs}
                </td>
                <td style={{ padding: "12px 10px", textAlign: "right", fontFamily: FONT_MONO, fontWeight: 600 }}>{s.parallels}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {/* Mobile */}
      <div className="min-[1180px]:hidden space-y-2">
        {otherSets.map((s) => (
          <Link key={s.id} href={`/sets/${s.slug ?? s.id}`} style={{
            display: "block", background: "#FFFFFF", border: "1px solid #EDEAE0",
            borderRadius: 10, padding: "12px 14px", textDecoration: "none",
          }}>
            <div style={{ fontSize: 16, fontWeight: 500, color: "var(--brand-ink)" }}>{s.name}</div>
            <div style={{ fontSize: 16, color: "#6B6757", marginTop: 2 }}>{s.sport}</div>
            <div className="grid grid-cols-3 gap-2 mt-2" style={{
              background: "#FAFAF7", borderRadius: 8, border: "1px solid #EDEAE0", padding: "8px 10px",
            }}>
              {[{ l: "CARDS", v: s.totalCards }, { l: "AUTOS", v: s.autographs }, { l: "PARALLELS", v: s.parallels }].map((st) => (
                <div key={st.l} className="text-center">
                  <div style={{ fontFamily: FONT_MONO, fontSize: 8, fontWeight: 600, letterSpacing: 1.2, color: "#8A8677", textTransform: "uppercase" }}>{st.l}</div>
                  <div style={{ fontFamily: FONT_MONO, fontSize: 16, fontWeight: 600, color: st.v === 0 ? "#B7B2A3" : "var(--brand-ink)", marginTop: 2 }}>
                    {st.v === 0 ? "—" : st.v.toLocaleString()}
                  </div>
                </div>
              ))}
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}

// ─── Mobile Drawer ──────────────────────────────────────────────────────────────

function MobileAthletesDrawer({ open, onClose, entries, hasTeamData, setId, setSlug, currentAthleteId, athleteCount, subjectLabel = "Athletes", teamLabel = "Team", sport = "" }: {
  open: boolean; onClose: () => void; entries: LeaderboardRow[]; hasTeamData: boolean;
  setId: number; setSlug: string; currentAthleteId: number; athleteCount: number; subjectLabel?: string; teamLabel?: string; sport?: string;
}) {
  useEffect(() => {
    if (!open) return;
    document.body.style.overflow = "hidden";
    function onKey(e: KeyboardEvent) { if (e.key === "Escape") onClose(); }
    window.addEventListener("keydown", onKey);
    return () => { document.body.style.overflow = ""; window.removeEventListener("keydown", onKey); };
  }, [open, onClose]);

  return (
    <div role="dialog" aria-modal="true" className="fixed inset-0 z-[100]"
      style={{
        background: "#FFFFFF", transform: open ? "translateY(0)" : "translateY(100%)",
        transition: "transform 200ms ease-out", pointerEvents: open ? "auto" : "none",
      }}>
      <div className="flex items-center justify-between" style={{ padding: "14px 16px", borderBottom: "1px solid #EDEAE0" }}>
        <button onClick={onClose} aria-label="Close" className="p-1">
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="#0F0F0E" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18 18 6M6 6l12 12" />
          </svg>
        </button>
        <span style={{ fontFamily: FONT_DISPLAY, fontSize: 17, fontWeight: 600, letterSpacing: -0.3, color: "var(--brand-ink)" }}>
          {subjectLabel} in Set
        </span>
        <span style={{ fontFamily: FONT_MONO, fontSize: 16, color: "#8A8677" }}>{athleteCount}</span>
      </div>
      <div style={{ height: "calc(100% - 56px)", overflowY: "auto" }}>
        <AthletesRail entries={entries} hasTeamData={hasTeamData} setId={setId} setSlug={setSlug} currentAthleteId={currentAthleteId} subjectLabel={subjectLabel} teamLabel={teamLabel} sport={sport} />
      </div>
    </div>
  );
}

// ─── Main Component ─────────────────────────────────────────────────────────────

export function AthleteDetailClient({
  athleteName, athleteId, athleteSlug, teams, hasRookie,
  nbaPlayerId, ufcImageUrl, mlbPlayerId, imageUrl,
  setName, setSlug, setId, sport, league,
  cardTypes, totalCards, autographs, autoParallels, numberedParallels, oneOfOnes,
  insertSets, otherSets, packOddsJson, boxConfigJson, epnCampaignId,
  packOddsSlotsByFormat, boxFormats, totalAutoCards, playerAutoCards, hasBreakCalc,
  entries, hasTeamData, subjectLabel: subjectLabelProp, subjectRole, teamLabel: teamLabelProp,
}: AthleteDetailClientProps) {
  const subjectLabel = subjectLabelProp ?? "Athletes";
  const teamLabel = teamLabelProp ?? "Team";
  const [tab, setTab] = useState<Tab>("Overview");
  const [drawerOpen, setDrawerOpen] = useState(false);

  // Record exactly one "view" per actual page visit, regardless of entry path
  // (search selection, browse click, direct/deep link, or shared URL). The ref
  // guard survives React Strict Mode's double-invoked mount effect and any
  // re-render; it re-fires only if the athlete being viewed changes.
  const viewedRef = useRef<number | null>(null);
  useEffect(() => {
    if (viewedRef.current === athleteId) return;
    viewedRef.current = athleteId;
    trackEvent(athleteId, "view");
  }, [athleteId]);

  function handleAthleteTabChange(t: Tab) {
    setTab(t);
    trackGaEvent("athlete_tab_click", {
      athlete_slug: athleteSlug ?? "",
      tab_name: t,
    });
  }

  // Subset-grouped tab content shared by desktop + mobile (same component/styling
  // as the set page). Filters mirror the set page's card-type tabs.
  const baseSubsets = insertSets.filter((is) => is.insertSetName.toLowerCase().includes("base"));
  const insertSubsets = insertSets.filter((is) => {
    const l = is.insertSetName.toLowerCase();
    return !l.includes("base") && !is.isAutograph;
  });
  const autoSubsets = insertSets.filter((is) => is.isAutograph);
  const subsetTab = (list: InsertSetDetail[]) => (
    <AthleteSubsetTab
      insertSets={list}
      packOddsJson={packOddsJson}
      playerName={athleteName}
      setName={setName}
      setId={setId}
      athleteId={athleteId}
      epnCampaignId={epnCampaignId}
    />
  );

  const statItems = [
    { label: "Card Types", value: cardTypes },
    { label: "Total Cards", value: totalCards },
    { label: "Autographs", value: autographs },
    { label: "Auto Parallels", value: autoParallels },
    { label: "Numbered", value: numberedParallels },
    { label: "1/1s", value: oneOfOnes },
  ];

  const teamStr = teams.join(" · ");
  const eyebrow = [teams[0], league || sport].filter(Boolean).join(" · ");

  return (
    <div style={{ background: "#FAFAF7", minHeight: "100vh" }}>
      {/* ═══ DESKTOP ═══ */}
      <div className="hidden min-[1180px]:grid" style={{ gridTemplateColumns: "425px 1fr", minHeight: "100vh" }}>
        <aside className="sticky top-0 h-screen overflow-y-auto" style={{ borderRight: "1px solid #EDEAE0" }}>
          <AthletesRail entries={entries} hasTeamData={hasTeamData} setId={setId} setSlug={setSlug} currentAthleteId={athleteId} subjectLabel={subjectLabel} teamLabel={teamLabel} sport={sport} />
        </aside>

        <div className="flex flex-col">
          {/* Hero */}
          <div style={{ background: "#FFFFFF", padding: "22px 36px 28px", borderBottom: "1px solid #EDEAE0" }}>
            <Link href={`/sets/${setSlug || setId}`} style={{ fontSize: 16, color: "#6B6757", textDecoration: "none", fontFamily: FONT_DISPLAY }}>
              &lsaquo; {setName}
            </Link>
            <div className="grid items-center gap-8 mt-4" style={{ gridTemplateColumns: "140px 1fr 300px" }}>
              {/* Photo */}
              <div className="flex items-center justify-center" style={{
                width: 140, height: 140, background: "#EAE6D9", borderRadius: 12, overflow: "hidden",
              }}>
                {(() => {
                  const url = getNBAHeadshotUrl(nbaPlayerId) ?? getUFCHeadshotUrl(ufcImageUrl) ?? getMLBHeadshotUrl(mlbPlayerId) ?? (imageUrl || null);
                  if (url) return <img src={url} alt={athleteName} className="w-full h-full object-cover object-top" />;
                  return (
                    <div className="flex flex-col items-center justify-center" style={{ color: "#C4BEAD" }}>
                      <span style={{ fontSize: 48, fontWeight: 600 }}>
                        {athleteName.split(" ").map((n) => n[0]).slice(0, 2).join("").toUpperCase()}
                      </span>
                      <span style={{ fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6, textTransform: "uppercase", marginTop: 4 }}>PHOTO</span>
                    </div>
                  );
                })()}
              </div>
              {/* Identity */}
              <div>
                <div style={{ fontFamily: FONT_MONO, fontSize: 10, fontWeight: 600, letterSpacing: 2.4, color: "#8A8677", textTransform: "uppercase" }}>
                  {eyebrow}
                </div>
                <h1 style={{
                  fontFamily: "var(--brand-font-head)", fontSynthesisWeight: "none", fontSize: 38, fontWeight: 400,
                  letterSpacing: -1, lineHeight: 1.08, color: "var(--brand-ink)", margin: "6px 0 12px",
                  textWrap: "balance",
                }}>{athleteName}</h1>
                <div className="flex flex-wrap items-center gap-2">
                  <span style={{ fontSize: 16, fontWeight: 500, padding: "4px 9px", borderRadius: 4, border: "1px solid #E6E3D9", color: "#3A372F" }}>
                    {sport}
                  </span>
                  {league && (
                    <span style={{ fontSize: 16, fontWeight: 500, padding: "4px 9px", borderRadius: 4, border: "1px solid #E6E3D9", color: "#3A372F" }}>
                      {league}
                    </span>
                  )}
                  {hasRookie && (
                    <span style={{
                      background: "oklch(0.55 0.17 25)", color: "#FFF8F1",
                      fontSize: 16, fontWeight: 700, padding: "4px 9px", borderRadius: 4,
                    }}>RC</span>
                  )}
                  <span style={{ fontSize: 16, color: "#6B6757" }}>
                    featured in {otherSets.length + 1} set{otherSets.length !== 0 ? "s" : ""}
                  </span>
                </div>
              </div>
              {/* Team Details panel */}
              {teams.length > 0 && (
                <div style={{ border: "2px solid #F2F0E9", padding: "14px 16px", alignSelf: "start" }}>
                  <div style={{ fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6, color: "#8A8677", textTransform: "uppercase", marginBottom: 10 }}>
                    {teamLabel} Details
                  </div>
                  {teams.map((t, i) => (
                    <div key={t} className="flex items-center justify-between" style={{
                      padding: "6px 0", borderBottom: i < teams.length - 1 ? "1px solid #F4F1E8" : "none",
                    }}>
                      <span style={{ fontSize: 16, color: "#6B6757" }}>{t}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Stat strip */}
          <div className="grid" style={{
            gridTemplateColumns: "repeat(6, 1fr)", borderBottom: "1px solid #EDEAE0", background: "#FFFFFF",
          }}>
            {statItems.map((item, i) => (
              <div key={item.label} style={{
                padding: "18px 16px", borderRight: i < statItems.length - 1 ? "1px solid #EDEAE0" : "none",
              }}>
                <div style={{ fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6, color: "#8A8677", textTransform: "uppercase" }}>
                  {item.label}
                </div>
                <div style={{ fontFamily: FONT_DISPLAY, fontSize: 26, fontWeight: 600, letterSpacing: -0.6, color: "var(--brand-ink)", marginTop: 4 }}>
                  {item.value.toLocaleString()}
                </div>
              </div>
            ))}
          </div>

          {/* Tabs */}
          <div role="tablist" style={{
            position: "sticky", top: 0, zIndex: 10,
            background: "#FAFAF7", padding: "0 36px", borderBottom: "1px solid #EDEAE0", display: "flex",
          }}>
            {TABS.map((t) => (
              <button key={t} role="tab" aria-selected={tab === t} onClick={() => handleAthleteTabChange(t)}
                style={{
                  padding: "14px 20px", fontFamily: FONT_DISPLAY,
                  fontSize: 16, fontWeight: tab === t ? 600 : 500,
                  color: tab === t ? "var(--brand-ink)" : "#8A8677",
                  borderBottom: tab === t ? "2px solid var(--brand-accent)" : "2px solid transparent",
                  marginBottom: -1, background: "transparent", cursor: "pointer", transition: "all 150ms",
                }}>
                {t}
              </button>
            ))}
          </div>

          {/* Content */}
          <div style={{ padding: "28px 36px 60px" }}>
            {tab === "Overview" && (
              <div className="space-y-8">
                {hasBreakCalc && (
                  <div style={{ padding: "18px 20px" }}>
                    <PackOddsCalculator
                      slotsByFormat={packOddsSlotsByFormat}
                      boxFormats={boxFormats}
                      totalAutoCards={totalAutoCards}
                      playerAutoCards={playerAutoCards}
                      setId={setId}
                      setName={setName}
                      setSlug={setSlug}
                    />
                  </div>
                )}
                <InsertSetsAccordion insertSets={insertSets} setSlug={setSlug} setId={setId} />
              </div>
            )}
            {tab === "Card Types" && subsetTab(insertSets)}
            {tab === "Base Parallels" && subsetTab(baseSubsets)}
            {tab === "Inserts" && subsetTab(insertSubsets)}
            {tab === "Autographs" && subsetTab(autoSubsets)}
            {tab === "Also Featured In" && <AlsoFeaturedIn otherSets={otherSets} />}
          </div>
        </div>
      </div>

      {/* ═══ MOBILE ═══ */}
      <div className="min-[1180px]:hidden">
        <div className="sticky top-0 z-10 flex items-center justify-between"
          style={{
            padding: "12px 16px", borderBottom: "1px solid #EDEAE0",
            background: "rgba(250,250,247,0.92)", backdropFilter: "blur(12px)", WebkitBackdropFilter: "blur(12px)",
          }}>
          <button onClick={() => setDrawerOpen(true)}
            style={{
              display: "flex", alignItems: "center", gap: 6,
              background: "#FFFFFF", border: "1px solid #E6E3D9", borderRadius: 8,
              padding: "8px 12px", fontSize: 16, fontWeight: 500, color: "var(--brand-ink)",
            }}>
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M15 19.128a9.38 9.38 0 0 0 2.625.372 9.337 9.337 0 0 0 4.121-.952 4.125 4.125 0 0 0-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128H5.228A2 2 0 0 1 3 17.208V5.792A2 2 0 0 1 5.228 3.872h13.544A2 2 0 0 1 21 5.792v6.625M12 10.5a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0Z" />
            </svg>
            Athletes
          </button>
          <Link href={`/sets/${setSlug || setId}`} style={{ fontSize: 16, color: "#6B6757", textDecoration: "none", fontFamily: FONT_DISPLAY }}>
            {setName} &rsaquo;
          </Link>
        </div>

        {/* Hero */}
        <div style={{ background: "#FFFFFF", padding: "18px 16px 14px", borderBottom: "1px solid #EDEAE0" }}>
          <div className="flex items-start gap-4">
            <div className="flex items-center justify-center flex-shrink-0" style={{
              width: 96, height: 96, background: "#EAE6D9", borderRadius: 12, overflow: "hidden",
            }}>
              {(() => {
                const url = getNBAHeadshotUrl(nbaPlayerId) ?? getUFCHeadshotUrl(ufcImageUrl) ?? getMLBHeadshotUrl(mlbPlayerId) ?? (imageUrl || null);
                if (url) return <img src={url} alt={athleteName} className="w-full h-full object-cover object-top" />;
                return (
                  <span style={{ fontSize: 28, fontWeight: 600, color: "#C4BEAD" }}>
                    {athleteName.split(" ").map((n) => n[0]).slice(0, 2).join("").toUpperCase()}
                  </span>
                );
              })()}
            </div>
            <div className="flex-1 min-w-0">
              <div style={{ fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 2, color: "#8A8677", textTransform: "uppercase" }}>
                {eyebrow}
              </div>
              <h1 style={{
                fontFamily: "var(--brand-font-head)", fontSynthesisWeight: "none", fontSize: 22, fontWeight: 400,
                letterSpacing: -0.6, lineHeight: 1.05, color: "var(--brand-ink)", margin: "4px 0 8px",
              }}>{athleteName}</h1>
              <div className="flex flex-wrap items-center gap-1.5">
                <span style={{ fontSize: 16, fontWeight: 500, padding: "3px 7px", borderRadius: 4, border: "1px solid #E6E3D9", color: "#3A372F" }}>
                  {sport}
                </span>
                {hasRookie && (
                  <span style={{
                    background: "oklch(0.55 0.17 25)", color: "#FFF8F1",
                    fontSize: 16, fontWeight: 700, padding: "3px 7px", borderRadius: 4,
                  }}>RC</span>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Stat grid */}
        <div className="flex overflow-x-auto no-scrollbar" style={{
          borderBottom: "1px solid #EDEAE0", background: "#FFFFFF",
        }}>
          {statItems.map((item, i) => (
            <div key={item.label} style={{
              padding: "12px 10px", borderRight: i < statItems.length - 1 ? "1px solid #EDEAE0" : "none",
              minWidth: "16.67%", flex: "1 0 auto",
            }}>
              <div style={{ fontFamily: FONT_MONO, fontSize: 7, fontWeight: 600, letterSpacing: 1, color: "#8A8677", textTransform: "uppercase" }}>
                {item.label}
              </div>
              <div style={{ fontFamily: FONT_DISPLAY, fontSize: 16, fontWeight: 600, letterSpacing: -0.5, color: "var(--brand-ink)", marginTop: 4 }}>
                {item.value.toLocaleString()}
              </div>
            </div>
          ))}
        </div>

        {/* Tabs */}
        <div role="tablist" className="sticky z-[5] overflow-x-auto no-scrollbar"
          style={{
            top: 53, background: "#FAFAF7", padding: "0 16px",
            borderBottom: "1px solid #EDEAE0", display: "flex", whiteSpace: "nowrap",
          }}>
          {TABS.map((t) => (
            <button key={t} role="tab" aria-selected={tab === t} onClick={() => handleAthleteTabChange(t)}
              style={{
                padding: "12px 12px", flexShrink: 0, fontFamily: FONT_DISPLAY,
                fontSize: 16, fontWeight: tab === t ? 600 : 500,
                color: tab === t ? "var(--brand-ink)" : "#8A8677",
                borderBottom: tab === t ? "2px solid var(--brand-accent)" : "2px solid transparent",
                marginBottom: -1, background: "transparent", cursor: "pointer",
              }}>
              {t}
            </button>
          ))}
        </div>

        {/* Content */}
        <div style={{ padding: 16 }}>
          {tab === "Overview" && (
            <div className="space-y-6">
              {hasBreakCalc && (
                <div style={{ padding: "14px 16px" }}>
                  <PackOddsCalculator
                    slotsByFormat={packOddsSlotsByFormat}
                    boxFormats={boxFormats}
                    totalAutoCards={totalAutoCards}
                    playerAutoCards={playerAutoCards}
                    setId={setId}
                    setName={setName}
                    setSlug={setSlug}
                  />
                </div>
              )}
              <InsertSetsAccordion insertSets={insertSets} setSlug={setSlug} setId={setId} />
            </div>
          )}
          {tab === "Card Types" && subsetTab(insertSets)}
          {tab === "Base Parallels" && subsetTab(baseSubsets)}
          {tab === "Inserts" && subsetTab(insertSubsets)}
          {tab === "Autographs" && subsetTab(autoSubsets)}
          {tab === "Also Featured In" && <AlsoFeaturedIn otherSets={otherSets} />}
        </div>

        <MobileAthletesDrawer open={drawerOpen} onClose={() => setDrawerOpen(false)}
          entries={entries} hasTeamData={hasTeamData} setId={setId} setSlug={setSlug}
          currentAthleteId={athleteId} athleteCount={entries.length} subjectLabel={subjectLabel} teamLabel={teamLabel} sport={sport} />
      </div>
    </div>
  );
}
