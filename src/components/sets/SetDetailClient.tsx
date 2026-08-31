"use client";

import React, { useState, useMemo, useRef, useEffect } from "react";
import Link from "next/link";
import type { LeaderboardRow } from "./types";
import type { BoxConfigSingle, BoxConfigMulti } from "./types";
import { getNBAHeadshotUrl } from "@/lib/nba-headshot";
import { getUFCHeadshotUrl } from "@/lib/ufc-headshot";
import { getMLBHeadshotUrl } from "@/lib/mlb-headshot";
import { trackEvent } from "@/lib/trackEvent";
import { trackEvent as trackGaEvent } from "@/lib/analytics";
import { normalizeOddsObj, denomToDisplay } from "@/lib/parseOdds";
import { type BreakSheetPlayer } from "@/components/BreakSheetModal";
import { BreakSheetLink } from "@/components/BreakSheetLink";
import type { CardGalleryImage } from "@/lib/cardGallery";
import { getTeamLogo } from "@/lib/utils/teamLogo";
import { findOddsKey } from "@/lib/oddsUtils";
import { SubsetCard } from "./SubsetCard";
import type { ParallelRowData } from "./ParallelTable";

// ─── Types & Constants ─────────────────────────────────────────────────────────

type Tab = string;
type SortKey = "totalCards" | "autographs" | "inserts" | "numberedParallels";

// Card-type tabs, in display order. Membership is driven by the explicit
// insert_sets flags (is_base / is_autograph / is_relic / is_booklet).
const CARD_TAB_ORDER = ["Base Cards", "Insert Cards", "Relic Cards", "Autograph Cards", "Booklets"] as const;
type CardTab = typeof CARD_TAB_ORDER[number];
const SORT_CHIPS: { key: SortKey; label: string }[] = [
  { key: "totalCards", label: "Total Cards" },
  { key: "autographs", label: "Autographs" },
  { key: "inserts", label: "Inserts" },
  { key: "numberedParallels", label: "Numbered" },
];

const FONT_DISPLAY = "var(--cl-font-display), 'Inter Tight', sans-serif";
const FONT_MONO = "var(--cl-font-mono), 'JetBrains Mono', ui-monospace, monospace";

interface ParallelInfo {
  name: string;
  printRun: number | null;
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
  subjectLabel?: string;
  teamLabel?: string;
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
  autographSubsetNames: string[];
  featuredArticle?: { slug: string; title: string; description: string; heroImage: string } | null;
  aeoSummary?: string | null;
  faqs?: { q: string; a: string }[];
  /** Card-image gallery, pre-read server-side from public/sets/cards/{slug}/. */
  cardImages?: CardGalleryImage[];
  /** Optional Topps product-page URL for the "About This Set" backlink. */
  toppsUrl?: string | null;
  /** Optional related article links rendered under the Topps backlink. */
  relatedLinks?: RelatedLink[];
  /** Per-subset checklists for the card-type tabs. */
  subsets?: SubsetChecklist[];
}

export interface RelatedLink {
  url: string;
  source: string;
  title: string;
  description: string;
}

export interface SubsetChecklist {
  name: string;
  isAutograph: boolean;
  isBase: boolean;
  isRelic: boolean;
  isBooklet: boolean;
  cards: { code: string; player: string; team: string | null; isRookie: boolean }[];
  parallels: { name: string; printRun: number | null; note?: string | null }[];
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

// Order the Pack Odds column falls through when a parallel's odds live in only
// some formats. Prefers what a typical buyer opens, so the shown value is the
// most representative; the resolver tags the value when it isn't hobby.
const ODDS_FORMAT_PREFERENCE = [
  "hobby", "jumbo", "value", "mega", "hanger", "fat_pack", "fanatics", "london_mega", "walmart_mega",
  // Phase 3 formats (official Topps sheet order); non-hobby → tagged.
  "hobby_silver_pack", "jumbo_silver_pack", "super_box", "super_box_oversized", "bulk_packs",
  "club_super_box", "club_super_box_oversized", "kids_mega", "club_ex_box_sams",
  "club_ex_box_sams_oversized", "gc_white_slip_sheets",
];

function isMultiConfig(cfg: BoxConfigSingle | BoxConfigMulti): cfg is BoxConfigMulti {
  const first = Object.values(cfg)[0];
  return first !== null && typeof first === "object";
}

function getAutosPerBox(fmt: BoxConfigSingle): number | null {
  return fmt.autos_per_box ?? fmt.autos_or_memorabilia_per_box ??
    fmt.autos_or_relics_per_box ?? fmt.autos_or_auto_relics_per_box ?? null;
}

// `autoNames` is the set of lowercased subset names flagged is_autograph in the
// DB — the single source of truth. An odds key belongs to an autograph subset
// when it equals, or is prefixed by, one of those names (e.g. "Cactus Ink" and
// "Cactus Ink Orange Refractor"). This catches autograph subsets whose names
// lack the word "auto"/"signature" (Cactus Ink, Milky Way Marks, Equinox, …).
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

// ─── Avatar ─────────────────────────────────────────────────────────────────────

function InitialsAvatar({ name, size = 30 }: { name: string; size?: number }) {
  const initials = name.split(" ").map((n) => n[0]).slice(0, 2).join("").toUpperCase();
  return (
    <div
      className="rounded-full flex items-center justify-center flex-shrink-0"
      style={{
        width: size, height: size,
        background: "var(--brand-empty)", color: "var(--brand-slate)",
        fontSize: size * 0.35, fontWeight: 600,
      }}
    >
      {initials}
    </div>
  );
}

function TeamLogo({ teamName, sport, size = 24 }: { teamName: string; sport: string; size?: number }) {
  const src = getTeamLogo(teamName, sport);
  const [err, setErr] = useState(false);
  if (!src || err) return <InitialsAvatar name={teamName} size={size} />;
  return (
    <img src={src} alt={`${teamName} logo`} width={size} height={size}
      loading="lazy" decoding="async" className="flex-shrink-0"
      onError={() => setErr(true)}
      style={{ width: size, height: size, objectFit: "contain" }} />
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

interface TeamRow {
  team: string;
  athleteCount: number;
  totalCards: number;
  autographs: number;
  inserts: number;
  numberedParallels: number;
}

function AthletesRail({ entries, hasTeamData, setId, setSlug, isMobile = false, subjectLabel = "Athletes", teamLabel = "Team", sport = "" }: {
  entries: LeaderboardRow[]; hasTeamData: boolean; setId: number; setSlug: string; isMobile?: boolean; subjectLabel?: string; teamLabel?: string; sport?: string;
}) {
  const [sortKey, setSortKey] = useState<SortKey>("totalCards");
  const [rookiesOnly, setRookiesOnly] = useState(false);
  const [query, setQuery] = useState("");
  const [showAll, setShowAll] = useState(false);
  const [viewMode, setViewMode] = useState<"athletes" | "teams">("athletes");

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

  const teamRows = useMemo((): TeamRow[] => {
    if (viewMode !== "teams") return [];
    const map = new Map<string, TeamRow>();
    const source = query.trim()
      ? entries.filter((e) => e.name.toLowerCase().includes(query.trim().toLowerCase()) || (e.team?.toLowerCase().includes(query.trim().toLowerCase())))
      : entries;
    for (const e of source) {
      const t = e.team ?? "Unknown";
      if (!map.has(t)) map.set(t, { team: t, athleteCount: 0, totalCards: 0, autographs: 0, inserts: 0, numberedParallels: 0 });
      const row = map.get(t)!;
      row.athleteCount++;
      row.totalCards += e.totalCards;
      row.autographs += e.autographs;
      row.inserts += e.inserts;
      row.numberedParallels += e.numberedParallels;
    }
    return Array.from(map.values()).sort((a, b) => {
      const diff = b[sortKey] - a[sortKey];
      return diff !== 0 ? diff : a.team.localeCompare(b.team);
    });
  }, [entries, query, sortKey, viewMode]);

  const visible = showAll ? filtered : filtered.slice(0, 50);
  const avatarSize = isMobile ? 34 : 30;
  const rowPy = isMobile ? "12px 4px" : "9px 4px";

  const teamCount = useMemo(() => new Set(entries.map((e) => e.team).filter(Boolean)).size, [entries]);

  return (
    <div className="flex flex-col h-full" style={{ background: "var(--brand-card)" }}>
      {/* Athletes / Teams tabs */}
      {hasTeamData && (
        <div className="shrink-0 flex" style={{
          borderBottom: "1px solid var(--brand-line)",
          padding: isMobile ? "0 16px" : "0 18px",
        }}>
          {([["athletes", `${subjectLabel} (${entries.length})`], ["teams", `${teamLabel}s (${teamCount})`]] as const).map(([mode, label]) => (
            <button key={mode} onClick={() => { setViewMode(mode); setShowAll(false); }}
              style={{
                padding: "12px 16px",
                fontFamily: FONT_DISPLAY,
                fontSize: 16,
                fontWeight: viewMode === mode ? 600 : 500,
                color: viewMode === mode ? "var(--brand-ink)" : "var(--brand-slate)",
                borderBottom: viewMode === mode ? "2px solid var(--brand-accent)" : "2px solid transparent",
                marginBottom: -1,
                background: "transparent",
                cursor: "pointer",
                transition: "all 150ms",
              }}>
              {label}
            </button>
          ))}
        </div>
      )}
      <div className="shrink-0 space-y-3" style={{ padding: isMobile ? "14px 16px 12px" : "14px 18px 12px" }}>
        {/* Search */}
        <div className="relative">
          <svg className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 pointer-events-none" style={{ color: "var(--brand-slate)" }}
            fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
            <path strokeLinecap="round" strokeLinejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
          </svg>
          <input
            type="text" value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder={`Search ${viewMode === "teams" ? `${teamLabel.toLowerCase()}s` : subjectLabel.toLowerCase()}…`}
            autoComplete="off" spellCheck={false}
            className="w-full outline-none"
            style={{
              background: "var(--brand-track)", borderRadius: 8, padding: "7px 10px 7px 30px",
              fontSize: 16, border: "none", color: "var(--brand-ink)",
            }}
          />
        </div>
        {/* Filter chips */}
        <div className="flex flex-wrap gap-1.5">
          {SORT_CHIPS.map((chip) => (
            <button key={chip.key} onClick={() => setSortKey(chip.key)}
              style={{
                borderRadius: isMobile ? 999 : 4, padding: "4px 9px",
                fontSize: 16, fontWeight: 500,
                background: sortKey === chip.key ? "var(--brand-ink)" : "transparent",
                color: sortKey === chip.key ? "var(--brand-page)" : "var(--brand-ink-soft)",
                border: sortKey === chip.key ? "1px solid var(--brand-ink)" : "1px solid var(--brand-line)",
              }}>
              {chip.label}
            </button>
          ))}
        </div>
        {/* Rookies only (hidden in teams view) */}
        {viewMode === "athletes" && (
          <label className="flex items-center gap-1.5 cursor-pointer" style={{ fontSize: 16, color: "var(--brand-ink-soft)" }}>
            <input type="checkbox" checked={rookiesOnly} onChange={() => setRookiesOnly((v) => !v)}
              style={{ accentColor: "var(--brand-ink)" }} />
            Rookies only
          </label>
        )}
      </div>
      {/* Column header */}
      <div className="shrink-0 flex justify-between items-center"
        style={{
          padding: "6px 18px", borderBottom: "1px solid var(--brand-line)",
          fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6, color: "var(--brand-slate)",
          textTransform: "uppercase",
        }}>
        <span>{viewMode === "teams" ? teamLabel.toUpperCase() : "ATHLETE"}</span>
        <span>{SORT_CHIPS.find((c) => c.key === sortKey)?.label}</span>
      </div>
      {/* Rows */}
      <div className="flex-1 overflow-y-auto">
        {viewMode === "athletes" ? (
          /* ── Athletes View ── */
          visible.length === 0 ? (
            <p className="text-center py-8" style={{ fontSize: 16, color: "var(--brand-slate)", fontStyle: "italic" }}>No {subjectLabel.toLowerCase()} match.</p>
          ) : (
            <>
              {visible.map((entry, idx) => (
                <Link key={entry.id}
                  href={`/sets/${setSlug || setId}/athlete/${entry.slug || entry.id}`}
                  // Search selection: fire "search" only when a query is active (a
                  // deliberate pick from the search bar). Plain browsing clicks fire
                  // nothing here — the visit is counted as a "view" on page mount.
                  onClick={() => { if (query.trim()) trackEvent(entry.id, "search"); }}
                  className="flex items-center gap-2 transition-colors"
                  style={{ padding: rowPy, paddingLeft: 18, paddingRight: 18, borderBottom: "1px solid var(--brand-line)" }}
                  onMouseEnter={(e) => { (e.currentTarget as HTMLElement).style.background = "var(--brand-track)"; }}
                  onMouseLeave={(e) => { (e.currentTarget as HTMLElement).style.background = "transparent"; }}>
                  <span style={{ fontFamily: FONT_MONO, fontSize: 16, color: "var(--brand-slate)", width: 18, textAlign: "right", flexShrink: 0 }}>
                    {idx + 1}
                  </span>
                  <PlayerAvatar name={entry.name} nbaPlayerId={entry.nbaPlayerId} ufcImageUrl={entry.ufcImageUrl}
                    mlbPlayerId={entry.mlbPlayerId} imageUrl={entry.imageUrl} size={avatarSize} />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-1.5 min-w-0">
                      <span className="truncate" style={{ fontSize: 16, fontWeight: 500, color: "var(--brand-ink)" }}>{entry.name}</span>
                      {entry.isRookie && (
                        <span className="shrink-0" style={{
                          background: "var(--brand-accent)", color: "var(--brand-head)",
                          fontSize: 14, fontWeight: 700, letterSpacing: 0.6,
                          padding: "1px 4px", borderRadius: 2, lineHeight: 1.2,
                        }}>RC</span>
                      )}
                    </div>
                    {hasTeamData && entry.team && (
                      <p className="truncate" style={{ fontSize: 16, color: "var(--brand-slate)", marginTop: 1 }}>{entry.team}</p>
                    )}
                  </div>
                  <span style={{ fontFamily: FONT_MONO, fontSize: 16, fontWeight: 600, color: "var(--brand-ink)", flexShrink: 0 }}>
                    {entry[sortKey].toLocaleString()}
                  </span>
                </Link>
              ))}
              {!showAll && filtered.length > 50 && (
                <button onClick={() => setShowAll(true)}
                  className="w-full py-3" style={{ fontSize: 16, fontWeight: 600, color: "var(--brand-ink)" }}>
                  Show all {filtered.length.toLocaleString()} {subjectLabel.toLowerCase()}
                </button>
              )}
            </>
          )
        ) : (
          /* ── Teams View ── */
          teamRows.length === 0 ? (
            <p className="text-center py-8" style={{ fontSize: 16, color: "var(--brand-slate)", fontStyle: "italic" }}>No teams match.</p>
          ) : (
            <>
              {(showAll ? teamRows : teamRows.slice(0, 50)).map((tr, idx) => (
                <Link key={tr.team}
                  href={`/sets/${setSlug || setId}/team/${tr.team.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "")}`}
                  className="flex items-center gap-2 transition-colors"
                  style={{ padding: rowPy, paddingLeft: 18, paddingRight: 18, borderBottom: "1px solid var(--brand-line)", textDecoration: "none" }}
                  onMouseEnter={(e) => { (e.currentTarget as HTMLElement).style.background = "var(--brand-track)"; }}
                  onMouseLeave={(e) => { (e.currentTarget as HTMLElement).style.background = "transparent"; }}>
                  <span style={{ fontFamily: FONT_MONO, fontSize: 16, color: "var(--brand-slate)", width: 18, textAlign: "right", flexShrink: 0 }}>
                    {idx + 1}
                  </span>
                  <TeamLogo teamName={tr.team} sport={sport} size={avatarSize} />
                  <div className="flex-1 min-w-0">
                    <span className="truncate block" style={{ fontSize: 16, fontWeight: 500, color: "var(--brand-ink)" }}>{tr.team}</span>
                    <p className="truncate" style={{ fontSize: 16, color: "var(--brand-slate)", marginTop: 1 }}>
                      {tr.athleteCount} {tr.athleteCount === 1 ? "Athlete" : "Athletes"}
                    </p>
                  </div>
                  <span style={{ fontFamily: FONT_MONO, fontSize: 16, fontWeight: 600, color: "var(--brand-ink)", flexShrink: 0 }}>
                    {tr[sortKey].toLocaleString()}
                  </span>
                </Link>
              ))}
              {!showAll && teamRows.length > 50 && (
                <button onClick={() => setShowAll(true)}
                  className="w-full py-3" style={{ fontSize: 16, fontWeight: 600, color: "var(--brand-ink)" }}>
                  Show all {teamRows.length.toLocaleString()} teams
                </button>
              )}
            </>
          )
        )}
      </div>
    </div>
  );
}

// ─── Mobile Drawer ──────────────────────────────────────────────────────────────

function MobileAthletesDrawer({ open, onClose, entries, hasTeamData, setId, setSlug, athleteCount, subjectLabel = "Athletes", teamLabel = "Team", sport = "" }: {
  open: boolean; onClose: () => void;
  entries: LeaderboardRow[]; hasTeamData: boolean; setId: number; setSlug: string; athleteCount: number; subjectLabel?: string; teamLabel?: string; sport?: string;
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
      role="dialog" aria-modal="true" aria-label={`${subjectLabel} in Set`}
      className="fixed inset-0 z-[100]"
      style={{
        background: "var(--brand-card)",
        transform: open ? "translateY(0)" : "translateY(100%)",
        transition: "transform 200ms ease-out",
        pointerEvents: open ? "auto" : "none",
      }}>
      {/* Drawer header */}
      <div className="flex items-center" style={{
        padding: "14px 16px", borderBottom: "none", background: "var(--brand-card)",
      }}>
        <button onClick={onClose} aria-label="Close" className="p-1">
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="var(--brand-ink)" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18 18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      {/* Drawer body */}
      <div className="flex-1" style={{ height: "calc(100% - 56px)", overflowY: "auto" }}>
        <AthletesRail entries={entries} hasTeamData={hasTeamData} setId={setId} setSlug={setSlug} isMobile subjectLabel={subjectLabel} teamLabel={teamLabel} sport={sport} />
      </div>
    </div>
  );
}

// ─── Coverage Card ──────────────────────────────────────────────────────────────

function CoverageCard({ hasChecklist, hasNumberedParallels, hasBoxConfig, hasPackOdds, breakSheetPlayers, setName, sport, league, setSlug }: {
  hasChecklist: boolean; hasNumberedParallels: boolean; hasBoxConfig: boolean; hasPackOdds: boolean;
  breakSheetPlayers: BreakSheetPlayer[]; setName: string; sport: string; league: string | null; setSlug: string;
}) {
  const rows = [
    { label: "Athlete Checklist", ok: hasChecklist },
    { label: "Numbered Parallels", ok: hasNumberedParallels },
    { label: "Box Configuration", ok: hasBoxConfig },
    { label: "Pack Odds", ok: hasPackOdds },
  ];
  return (
    <div style={{
      background: "var(--brand-page)", border: "1px solid var(--brand-line)", borderRadius: 8, padding: "12px 14px",
    }}>
      <div className="flex items-center justify-between" style={{ marginBottom: 10 }}>
        <span style={{ fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6, color: "var(--brand-slate)", textTransform: "uppercase" }}>
          Coverage
        </span>
        <div className="v2-break-sheet-pill">
          <style>{`
            .v2-break-sheet-pill > button, .v2-break-sheet-pill > a {
              background: var(--brand-ink) !important; color: var(--brand-page) !important;
              font-size: 10px !important; font-weight: 600 !important;
              padding: 5px 10px !important; border-radius: 4px !important;
              border: none !important; cursor: pointer !important;
              line-height: 1.2 !important;
            }
            .v2-break-sheet-pill > button:hover, .v2-break-sheet-pill > a:hover { background: #1A1A19 !important; }
          `}</style>
          <BreakSheetLink slug={setSlug} setName={setName} sport={sport} league={league} players={breakSheetPlayers} />
        </div>
      </div>
      <div className="space-y-2">
        {rows.map((r) => (
          <div key={r.label} className="flex items-center justify-between">
            <span style={{ fontSize: 16, color: "var(--brand-ink-soft)" }}>{r.label}</span>
            <span
              aria-label={r.ok ? "Present" : "Missing"}
              style={{
                width: 8, height: 8, borderRadius: "50%",
                background: r.ok ? "var(--brand-ok)" : "var(--brand-fog)",
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
        gridTemplateColumns: "repeat(6, 1fr)", borderBottom: "1px solid var(--brand-line)", background: "var(--brand-card)",
      }}>
        {items.map((item, i) => (
          <div key={item.label} style={{
            padding: "18px 22px",
            borderRight: i < items.length - 1 ? "1px solid var(--brand-line)" : "none",
          }}>
            <div style={{ fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6, color: "var(--brand-slate)", textTransform: "uppercase" }}>
              {item.label}
            </div>
            <div style={{ fontFamily: FONT_DISPLAY, fontSize: 26, fontWeight: 600, letterSpacing: -0.6, color: "var(--brand-ink)", marginTop: 4 }}>
              {item.value.toLocaleString()}
            </div>
          </div>
        ))}
      </div>
      {/* Mobile: 3×2 */}
      <div className="grid min-[1180px]:hidden" style={{
        gridTemplateColumns: "repeat(3, 1fr)", borderBottom: "1px solid var(--brand-line)", background: "var(--brand-card)",
      }}>
        {items.map((item, i) => (
          <div key={item.label} style={{
            padding: "14px 16px",
            borderRight: (i % 3) < 2 ? "1px solid var(--brand-line)" : "none",
            borderBottom: i < 3 ? "1px solid var(--brand-line)" : "none",
          }}>
            <div style={{ fontFamily: FONT_MONO, fontSize: 8, fontWeight: 600, letterSpacing: 1.6, color: "var(--brand-slate)", textTransform: "uppercase" }}>
              {item.label}
            </div>
            <div style={{ fontFamily: FONT_DISPLAY, fontSize: 20, fontWeight: 600, letterSpacing: -0.6, color: "var(--brand-ink)", marginTop: 4 }}>
              {item.value.toLocaleString()}
            </div>
          </div>
        ))}
      </div>
    </>
  );
}

// ─── Tab: Box Config ────────────────────────────────────────────────────────────

// ─── Card Gallery ───────────────────────────────────────────────────────────

// Every gallery card renders at this fixed height; width follows the image's
// intrinsic aspect (vertical 5:7 → 150px wide; horizontal cards render wider).
const CARD_GALLERY_H = 210;

function CardGallery({ images, setName }: { images: CardGalleryImage[]; setName: string }) {
  const scrollRef = useRef<HTMLDivElement>(null);
  const [canLeft, setCanLeft] = useState(false);
  const [canRight, setCanRight] = useState(false);

  // Recompute arrow visibility from the live scroll metrics. Left hides at the
  // start, right hides at the end (1px tolerance for sub-pixel rounding), and
  // when everything fits (scrollWidth <= clientWidth) neither shows.
  const updateArrows = () => {
    const el = scrollRef.current;
    if (!el) return;
    const { scrollLeft, clientWidth, scrollWidth } = el;
    setCanLeft(scrollLeft > 0);
    setCanRight(scrollLeft + clientWidth < scrollWidth - 1);
  };

  useEffect(() => {
    const el = scrollRef.current;
    if (!el) return;
    updateArrows();
    el.addEventListener("scroll", updateArrows, { passive: true });
    const ro = new ResizeObserver(updateArrows);
    ro.observe(el);
    window.addEventListener("resize", updateArrows);
    return () => {
      el.removeEventListener("scroll", updateArrows);
      ro.disconnect();
      window.removeEventListener("resize", updateArrows);
    };
  }, [images.length]);

  // Scroll by one card. Cards can now have different widths (horizontal cards
  // are wider), so step by the *next* card's actual width in the scroll
  // direction (measured live) rather than assuming a uniform card width.
  const scrollByCard = (dir: 1 | -1) => {
    const el = scrollRef.current;
    if (!el) return;
    const cards = Array.from(el.querySelectorAll<HTMLElement>("[data-card]"));
    if (cards.length === 0) return;
    const row = cards[0].parentElement;
    const gap = row ? parseFloat(getComputedStyle(row).columnGap) || 0 : 0;
    const base = cards[0].offsetLeft; // content-relative origin (offsetParent-agnostic)
    const left = el.scrollLeft;
    let target: HTMLElement;
    if (dir === 1) {
      target = cards.find((c) => c.offsetLeft - base > left + 1) ?? cards[cards.length - 1];
    } else {
      target = [...cards].reverse().find((c) => c.offsetLeft - base < left - 1) ?? cards[0];
    }
    el.scrollBy({ left: dir * (target.offsetWidth + gap), behavior: "smooth" });
  };

  const arrowBtn = (dir: 1 | -1) => (
    <button
      type="button"
      aria-label={dir === -1 ? "Scroll gallery left" : "Scroll gallery right"}
      onClick={() => scrollByCard(dir)}
      className="rounded-lg flex items-center justify-center border transition-colors bg-[var(--brand-track)] hover:bg-[var(--brand-line)]"
      style={{ width: 28, height: 28, borderColor: "var(--brand-line)", color: "var(--brand-ink-soft)" }}
    >
      <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d={dir === -1 ? "M15.75 19.5 8.25 12l7.5-7.5" : "m8.25 4.5 7.5 7.5-7.5 7.5"} />
      </svg>
    </button>
  );

  return (
    <section>
      <div className="flex items-center justify-between" style={{ marginBottom: 12 }}>
        <div style={{ fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6, color: "var(--brand-slate)", textTransform: "uppercase" }}>
          Card Gallery
        </div>
        {(canLeft || canRight) && (
          <div className="flex items-center gap-1.5">
            {canLeft && arrowBtn(-1)}
            {canRight && arrowBtn(1)}
          </div>
        )}
      </div>
      {/* Bounded scroll container: constrained to the parent's width and
          scrolls internally. min-w-0 + max-w-full stop the flex contents
          from sizing this wrapper (and the page) wide. */}
      <div ref={scrollRef} className="w-full max-w-full min-w-0 overflow-x-auto no-scrollbar">
        <div className="flex flex-nowrap gap-3" style={{ paddingBottom: 4 }}>
          {images.map(({ src, n, width, height }) => (
            // Fixed HEIGHT, natural width: every card is CARD_GALLERY_H tall and
            // its width follows the image's intrinsic aspect ratio (vertical
            // cards stay 5:7 → 150px; horizontal cards render wider). The
            // aspect-ratio reserves the box before the image loads → no shift.
            <div
              key={src}
              data-card
              className="shrink-0"
              style={{ height: CARD_GALLERY_H, aspectRatio: `${width} / ${height}`, overflow: "hidden", border: "1px solid var(--brand-line)", background: "var(--brand-track)" }}
            >
              <img
                src={src}
                alt={`${setName} card ${n}`}
                width={width}
                height={height}
                loading="lazy"
                decoding="async"
                className="w-full h-full object-cover"
              />
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

// ─── Tab: Overview ──────────────────────────────────────────────────────────

function OverviewContent({ boxConfig, cards, cardTypes, parallelTypes, autographs, autoParallels, totalParallels, athleteCount, releaseDate, hasChecklist, hasNumberedParallels, hasBoxConfig, hasPackOdds, subjectLabel = "Athletes", featuredArticle, setName, aeoSummary, faqs, cardImages, toppsUrl, relatedLinks }: {
  boxConfig: string | null; cards: number; cardTypes: number; parallelTypes: number;
  autographs: number; autoParallels: number; totalParallels: number; athleteCount: number;
  releaseDate: string | null; hasChecklist: boolean; hasNumberedParallels: boolean;
  hasBoxConfig: boolean; hasPackOdds: boolean; subjectLabel?: string;
  featuredArticle?: { slug: string; title: string; description: string; heroImage: string } | null;
  setName: string; aeoSummary?: string | null; faqs?: { q: string; a: string }[];
  cardImages?: CardGalleryImage[]; toppsUrl?: string | null; relatedLinks?: RelatedLink[];
}) {
  const boxRows = boxConfig ? buildBoxRows(boxConfig) : [];

  return (
    <div className="space-y-8">
      {/* Card Gallery — only renders when card images exist in
          public/sets/cards/{slug}/. Display-only horizontal scroll row. */}
      {cardImages && cardImages.length > 0 && (
        <CardGallery images={cardImages} setName={setName} />
      )}

      {/* Set Summary */}
      {(aeoSummary || toppsUrl || (relatedLinks && relatedLinks.length > 0)) && (
        <section>
          <div style={{ fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6, color: "var(--brand-slate)", textTransform: "uppercase", marginBottom: 12 }}>
            About This Set
          </div>
          {aeoSummary && (
            <p style={{ fontSize: 16, lineHeight: 1.65, color: "var(--brand-ink-soft)", margin: 0 }}>
              {aeoSummary.startsWith(setName) ? (
                <>
                  <strong style={{ color: "var(--brand-ink)" }}>{setName}</strong>
                  {aeoSummary.slice(setName.length)}
                </>
              ) : (
                aeoSummary
              )}
            </p>
          )}
          {/* Topps product backlink — only when a URL is set for this set. */}
          {toppsUrl && (
            <a
              href={toppsUrl}
              target="_blank"
              rel="noopener noreferrer"
              style={{
                display: "inline-flex", alignItems: "center", gap: 5,
                marginTop: aeoSummary ? 12 : 0, fontSize: 15, fontWeight: 600,
                color: "var(--brand-accent)", textDecoration: "none",
              }}
            >
              View on Topps website
              <svg width={13} height={13} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 6H5.25A2.25 2.25 0 0 0 3 8.25v10.5A2.25 2.25 0 0 0 5.25 21h10.5A2.25 2.25 0 0 0 18 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25" />
              </svg>
            </a>
          )}
          {/* Related article backlinks (e.g. Topps RIPPED). */}
          {relatedLinks && relatedLinks.length > 0 && (
            <div style={{ marginTop: aeoSummary || toppsUrl ? 20 : 0 }}>
              <div style={{ fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6, color: "var(--brand-slate)", textTransform: "uppercase", marginBottom: 10 }}>
                Read more on {relatedLinks[0].source}
              </div>
              <ul style={{ listStyle: "none", margin: 0, padding: 0, display: "flex", flexDirection: "column", gap: 10 }}>
                {relatedLinks.map((link) => (
                  <li key={link.url}>
                    <a
                      href={link.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{ fontSize: 15, fontWeight: 600, color: "var(--brand-accent)", textDecoration: "none" }}
                    >
                      {link.title}
                    </a>
                    {link.description && (
                      <p style={{ fontSize: 13, lineHeight: 1.55, color: "var(--brand-slate)", margin: "2px 0 0" }}>
                        {link.description}
                      </p>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </section>
      )}

      {/* Quick Stats */}
      <div>
        <div style={{ fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6, color: "var(--brand-slate)", textTransform: "uppercase", marginBottom: 12 }}>
          At a Glance
        </div>
        <div className="grid grid-cols-2 min-[1180px]:grid-cols-3 gap-3">
          {[
            { label: subjectLabel, value: athleteCount, show: athleteCount > 0 },
            { label: "Total Cards", value: cards, show: cards > 0 },
            { label: "Card Types", value: cardTypes, show: cardTypes > 0 },
            { label: "Autographs", value: autographs, show: autographs > 0 },
            { label: "Parallel Types", value: parallelTypes, show: parallelTypes > 0 },
            { label: "Total Parallels", value: totalParallels, show: totalParallels > 0 },
          ].filter(s => s.show).map((s) => (
            <div key={s.label} style={{
              background: "var(--brand-card)", border: "1px solid var(--brand-line)", borderRadius: 8, padding: "14px 16px",
            }}>
              <div style={{ fontFamily: FONT_DISPLAY, fontSize: 26, fontWeight: 600, letterSpacing: -0.6, color: "var(--brand-ink)" }}>
                {s.value.toLocaleString()}
              </div>
              <div style={{ fontSize: 16, color: "var(--brand-slate)", marginTop: 2 }}>{s.label}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Coverage Status */}
      <div>
        <div style={{ fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6, color: "var(--brand-slate)", textTransform: "uppercase", marginBottom: 12 }}>
          Coverage
        </div>
        <div style={{ background: "var(--brand-card)", border: "1px solid var(--brand-line)", borderRadius: 8, padding: "14px 16px" }}>
          <div className="grid grid-cols-2 min-[1180px]:grid-cols-4 gap-3">
            {[
              { label: "Athlete Checklist", ok: hasChecklist },
              { label: "Numbered Parallels", ok: hasNumberedParallels },
              { label: "Box Configuration", ok: hasBoxConfig },
              { label: "Pack Odds", ok: hasPackOdds },
            ].map((r) => (
              <div key={r.label} className="flex items-center gap-2">
                <span aria-label={r.ok ? "Present" : "Missing"} style={{
                  width: 8, height: 8, borderRadius: "50%", flexShrink: 0,
                  background: r.ok ? "var(--brand-ok)" : "var(--brand-fog)",
                }} />
                <span style={{ fontSize: 16, color: "var(--brand-ink-soft)" }}>{r.label}</span>
              </div>
            ))}
          </div>
          {releaseDate && (
            <div className="mt-3 pt-3" style={{ borderTop: "1px solid var(--brand-line)" }}>
              <span style={{ fontSize: 16, color: "var(--brand-slate)" }}>Release Date: </span>
              <span style={{ fontSize: 16, fontWeight: 600, color: "var(--brand-ink)" }}>
                {new Date(releaseDate + "T00:00:00Z").toLocaleDateString("en-US", {
                  month: "long", day: "numeric", year: "numeric", timeZone: "UTC",
                })}
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Box Configuration */}
      {boxRows.length > 0 && (
        <div>
          <div style={{ fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6, color: "var(--brand-slate)", textTransform: "uppercase", marginBottom: 12 }}>
            Box Configuration
          </div>
          {/* Desktop */}
          <div className="hidden min-[1180px]:block">
            <div className="grid gap-3" style={{ gridTemplateColumns: `repeat(${Math.min(boxRows.length, 3)}, 1fr)` }}>
              {boxRows.map((row) => (
                <div key={row.label} style={{
                  background: "var(--brand-card)", border: "1px solid var(--brand-line)", borderRadius: 8, padding: "16px",
                }}>
                  <div style={{ fontFamily: FONT_DISPLAY, fontSize: 16, fontWeight: 600, color: "var(--brand-ink)", marginBottom: 12 }}>
                    {row.label}
                  </div>
                  <div className="space-y-1.5">
                    {row.cardsPerPack != null && (
                      <div style={{ fontSize: 16, color: "var(--brand-ink-soft)" }}>
                        <span style={{ fontFamily: FONT_MONO, fontWeight: 600, color: "var(--brand-ink)" }}>{row.cardsPerPack}</span> cards/pack
                      </div>
                    )}
                    {row.packsPerBox != null && (
                      <div style={{ fontSize: 16, color: "var(--brand-ink-soft)" }}>
                        <span style={{ fontFamily: FONT_MONO, fontWeight: 600, color: "var(--brand-ink)" }}>{row.packsPerBox}</span> packs/box
                      </div>
                    )}
                    {row.boxesPerCase != null && (
                      <div style={{ fontSize: 16, color: "var(--brand-ink-soft)" }}>
                        <span style={{ fontFamily: FONT_MONO, fontWeight: 600, color: "var(--brand-ink)" }}>{row.boxesPerCase}</span> boxes/case
                      </div>
                    )}
                    {row.autosPerBox != null && (
                      <div style={{ fontSize: 16, color: "var(--brand-ink-soft)" }}>
                        <span style={{ fontFamily: FONT_MONO, fontWeight: 600, color: "var(--brand-ink)" }}>{row.autosPerBox}</span> auto{row.autosPerBox !== 1 ? "s" : ""}/box
                      </div>
                    )}
                  </div>
                  {row.notes && (
                    <div style={{ borderTop: "1px solid var(--brand-line)", marginTop: 10, paddingTop: 8, fontSize: 16, fontStyle: "italic", color: "var(--brand-slate)" }}>
                      {row.notes}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
          {/* Mobile */}
          <div className="min-[1180px]:hidden space-y-2">
            {boxRows.map((row) => (
              <div key={row.label} style={{
                background: "var(--brand-card)", border: "1px solid var(--brand-line)", borderRadius: 10, padding: "12px 14px",
              }}>
                <div style={{ fontFamily: FONT_DISPLAY, fontSize: 16, fontWeight: 600, color: "var(--brand-ink)", marginBottom: 8 }}>
                  {row.label}
                </div>
                <div className="grid grid-cols-3 gap-2">
                  {[
                    { l: "CARDS/PK", v: row.cardsPerPack },
                    { l: "PKS/BOX", v: row.packsPerBox },
                    { l: "BXS/CASE", v: row.boxesPerCase },
                  ].map((s) => (
                    <div key={s.l}>
                      <div style={{ fontFamily: FONT_MONO, fontSize: 7, fontWeight: 600, letterSpacing: 1, color: "var(--brand-slate)", textTransform: "uppercase" }}>{s.l}</div>
                      <div style={{ fontFamily: FONT_MONO, fontSize: 16, fontWeight: 600, color: s.v != null ? "var(--brand-ink)" : "var(--brand-fog)", marginTop: 2 }}>{s.v ?? "—"}</div>
                    </div>
                  ))}
                </div>
                {row.notes && (
                  <div style={{ borderTop: "1px solid var(--brand-line)", marginTop: 8, paddingTop: 6, fontSize: 16, fontStyle: "italic", color: "var(--brand-slate)" }}>
                    {row.notes}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Featured Article */}
      {featuredArticle && (
        <div>
          <div style={{ fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6, color: "var(--brand-slate)", textTransform: "uppercase", marginBottom: 12 }}>
            Featured Article
          </div>
          <a
            href={`/articles/${featuredArticle.slug}`}
            style={{
              display: "flex", gap: 16, background: "var(--brand-card)", border: "1px solid var(--brand-line)",
              borderRadius: 8, padding: 16, textDecoration: "none", transition: "box-shadow 0.15s",
            }}
            onMouseEnter={(e) => { (e.currentTarget as HTMLElement).style.boxShadow = "0 4px 14px rgba(15,15,14,0.08)"; }}
            onMouseLeave={(e) => { (e.currentTarget as HTMLElement).style.boxShadow = "none"; }}
          >
            {featuredArticle.heroImage && (
              <img src={featuredArticle.heroImage} alt="" width={100} height={140}
                style={{ width: 100, height: 140, objectFit: "cover", borderRadius: 4, flexShrink: 0 }} />
            )}
            <div style={{ minWidth: 0 }}>
              <div style={{ fontFamily: FONT_DISPLAY, fontSize: 16, fontWeight: 600, color: "var(--brand-ink)", lineHeight: 1.3 }}>
                {featuredArticle.title}
              </div>
              <div style={{ fontSize: 14, color: "var(--brand-slate)", marginTop: 6, lineHeight: 1.5, display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical", overflow: "hidden" }}>
                {featuredArticle.description}
              </div>
              <div style={{ fontFamily: FONT_MONO, fontSize: 11, fontWeight: 600, color: "var(--brand-accent)", marginTop: 10 }}>
                READ FULL ARTICLE &rarr;
              </div>
            </div>
          </a>
        </div>
      )}

      {/* FAQ / Q&A */}
      {faqs && faqs.length > 0 && (
        <section>
          <div style={{ fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6, color: "var(--brand-slate)", textTransform: "uppercase", marginBottom: 12 }}>
            Frequently Asked Questions
          </div>
          <div style={{ background: "var(--brand-card)", border: "1px solid var(--brand-line)", borderRadius: 8 }}>
            {faqs.map((f, i) => (
              <div key={f.q} style={{ padding: "16px", borderTop: i > 0 ? "1px solid var(--brand-line)" : "none" }}>
                <h3 style={{ fontFamily: FONT_DISPLAY, fontSize: 17, fontWeight: 600, color: "var(--brand-ink)", margin: 0, lineHeight: 1.3 }}>
                  {f.q}
                </h3>
                <p style={{ fontSize: 15, lineHeight: 1.6, color: "var(--brand-ink-soft)", margin: "8px 0 0" }}>
                  {f.a}
                </p>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}

// ─── Shared Odds Table ──────────────────────────────────────────────────────────

function EmptyTab({ label }: { label: string }) {
  return (
    <div style={{
      padding: "40px 20px", textAlign: "center", fontSize: 16,
      fontStyle: "italic", color: "var(--brand-slate)",
    }}>{label}</div>
  );
}

// ─── Card-type tabs (Base / Insert / Relic / Autograph / Booklets) ──────────────

/** Membership from explicit flags — Tyler's locked matrix. */
function subsetInTab(s: SubsetChecklist, tab: CardTab): boolean {
  switch (tab) {
    case "Base Cards": return s.isBase;
    case "Autograph Cards": return s.isAutograph;
    case "Relic Cards": return s.isRelic && !s.isAutograph;
    case "Booklets": return s.isBooklet;
    case "Insert Cards": return !s.isBase && !s.isAutograph && !s.isRelic && !s.isBooklet;
    default: return false;
  }
}

/** Chips shown for a subset within a given tab (never removes it from anywhere). */
function chipsFor(s: SubsetChecklist, tab: CardTab): { label: string; accent?: boolean }[] {
  const out: { label: string; accent?: boolean }[] = [];
  if (tab === "Autograph Cards") {
    if (s.isRelic) out.push({ label: "RELIC" });
    if (s.isBooklet) out.push({ label: "BOOKLET", accent: true });
  } else if (tab === "Booklets") {
    if (s.isAutograph) out.push({ label: "AUTO" });
    if (s.isRelic) out.push({ label: "RELIC" });
  } else if (tab === "Relic Cards") {
    if (s.isBooklet) out.push({ label: "BOOKLET" });
  }
  return out;
}

/** One subset on the set page: builds rows + checklist, delegates rendering to the
 *  shared SubsetCard (no shopLink → 3-column table, identical to before). */
function SubsetSection({ subset, tab, showNumbered, oddsFor }: {
  subset: SubsetChecklist; tab: CardTab;
  showNumbered: boolean;
  oddsFor: (parallelName: string) => { denom: number; format: string | null } | null;
}) {
  const chips = chipsFor(subset, tab);
  const pars = subset.parallels;
  const tableRows: ParallelRowData[] = pars.map((p) => {
    const o = oddsFor(p.name);
    return {
      name: p.name,
      printRun: p.printRun,
      note: p.note,
      odds: o ? { text: denomToDisplay(o.denom), tag: o.format && o.format !== "hobby" ? fmtBoxLabel(o.format) : null } : null,
    };
  });

  const checklist = (
    <div style={{ border: "1px solid var(--brand-line)", borderRadius: 8, overflow: "hidden", background: "var(--brand-card)" }}>
      {subset.cards.map((c, i) => (
        <div key={`${c.code}-${i}`} className="flex items-center gap-3"
          style={{ padding: "8px 12px", borderTop: i > 0 ? "1px solid var(--brand-line)" : "none" }}>
          <span style={{ fontFamily: FONT_MONO, fontSize: 13, color: "var(--brand-slate)", minWidth: 54 }}>{c.code}</span>
          <span style={{ fontSize: 15, fontWeight: 500, color: "var(--brand-ink)", flex: 1, minWidth: 0 }}>{c.player}</span>
          {c.isRookie && (
            <span style={{
              flexShrink: 0, fontFamily: FONT_MONO, fontSize: 9, fontWeight: 700, letterSpacing: 0.5,
              color: "var(--brand-accent-deep)", background: "rgba(154,43,20,0.08)", border: "1px solid rgba(154,43,20,0.2)",
              padding: "1px 5px", borderRadius: 3,
            }}>RC</span>
          )}
          {c.team && <span style={{ fontSize: 13, color: "var(--brand-slate)", flexShrink: 0, textAlign: "right" }}>{c.team}</span>}
        </div>
      ))}
    </div>
  );

  return (
    <SubsetCard
      name={subset.name}
      cardsCount={subset.cards.length}
      parallelsCount={pars.length}
      chips={chips}
      checklist={checklist}
      tableRows={tableRows}
      showNumbered={showNumbered}
    />
  );
}

function CardTypeTabContent({ tab, subsets, hasNumberedParallels, oddsResolver }: {
  tab: CardTab; subsets: SubsetChecklist[];
  hasNumberedParallels: boolean;
  oddsResolver: (subsetName: string, parallelName: string) => { denom: number; format: string | null } | null;
}) {
  const members = subsets.filter((s) => subsetInTab(s, tab));
  if (members.length === 0) return <EmptyTab label="No cards in this category" />;
  return (
    <div>
      {members.map((s) => (
        <SubsetSection
          key={s.name}
          subset={s}
          tab={tab}
          showNumbered={hasNumberedParallels}
          oddsFor={(parallelName) => oddsResolver(s.name, parallelName)}
        />
      ))}
    </div>
  );
}

// ─── Main Component ─────────────────────────────────────────────────────────────

export function SetDetailClient({
  setName, sport, league, tier, releaseDate, setId, setSlug, sampleImageUrl,
  cards, cardTypes, parallelTypes, autographs, autoParallels, totalParallels, athleteCount,
  subjectLabel: subjectLabelProp, teamLabel: teamLabelProp,
  hasChecklist, hasNumberedParallels, hasBoxConfig, hasPackOdds,
  boxConfig, packOdds, entries, hasTeamData, breakSheetPlayers, parallelsList, autographSubsetNames, featuredArticle,
  aeoSummary, faqs, cardImages, toppsUrl, relatedLinks, subsets = [],
}: SetDetailClientProps) {
  const subjectLabel = subjectLabelProp ?? "Athletes";
  const teamLabel = teamLabelProp ?? "Team";
  const [tab, setTab] = useState<Tab>("Overview");
  const [drawerOpen, setDrawerOpen] = useState(false);

  function handleSetTabChange(t: Tab) {
    setTab(t);
    trackGaEvent("set_tab_click", {
      set_slug: setSlug ?? "",
      tab_name: t,
    });
  }

  const meta = useMemo(() => extractMeta(setName, sport), [setName, sport]);

  // Primary-format pack-odds lookup (nested → first format; flat → itself),
  // keyed by odds key. Used to resolve a subset's parallel pull odds for the
  // Pack Odds column. Single source; matching tolerates key composition.
  // Per-format normalized odds for the Pack Odds column, ordered by the buyer
  // preference above. A parallel's odds can live in only one format (e.g.
  // Sandglitter is jumbo-only, the Union Jack foils are London Mega-only), so
  // resolving against a single format dropped many parallels to "—". flat
  // (non-nested) pack_odds stays a single unlabeled format → renders as today.
  const oddsByFormat = useMemo<{ format: string | null; odds: Record<string, number> }[] | null>(() => {
    if (!packOdds) return null;
    try {
      const raw = JSON.parse(packOdds) as Record<string, unknown>;
      const firstVal = Object.values(raw)[0];
      const isNested = firstVal !== null && typeof firstVal === "object";
      if (!isNested) return [{ format: null, odds: normalizeOddsObj(raw) }];
      const nested = raw as Record<string, Record<string, unknown>>;
      const ordered = [
        ...ODDS_FORMAT_PREFERENCE.filter((f) => f in nested),
        ...Object.keys(nested).filter((f) => !ODDS_FORMAT_PREFERENCE.includes(f)),
      ];
      return ordered.map((f) => ({ format: f, odds: normalizeOddsObj(nested[f]) }));
    } catch { return null; }
  }, [packOdds]);

  const oddsResolver = useMemo(() => {
    return (subsetName: string, parallelName: string): { denom: number; format: string | null } | null => {
      if (!oddsByFormat) return null;
      const composed = `${subsetName} ${parallelName}`;
      for (const { format, odds } of oddsByFormat) {
        if (odds[composed] != null) return { denom: odds[composed], format };
        const found = findOddsKey(composed, Object.keys(odds));
        if (found && odds[found] != null) return { denom: odds[found], format };
      }
      return null;
    };
  }, [oddsByFormat]);

  // Dynamic tab list: Overview + any card-type tab that has member subsets.
  const cardTabs = useMemo(
    () => CARD_TAB_ORDER.filter((t) => subsets.some((s) => subsetInTab(s, t))),
    [subsets]
  );
  const tabList = useMemo<Tab[]>(() => ["Overview", ...cardTabs], [cardTabs]);
  // If the active tab is no longer valid (e.g. hydration), fall back to Overview.
  const activeTab: Tab = tabList.includes(tab) ? tab : "Overview";

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
    <div style={{ background: "var(--brand-page)", minHeight: "100vh" }}>
      {/* ═══ DESKTOP ═══ */}
      <div className="hidden min-[1180px]:grid" style={{ gridTemplateColumns: "425px 1fr", minHeight: "100vh" }}>
        {/* Left rail */}
        <aside className="sticky top-0 h-screen overflow-y-auto" style={{ borderRight: "1px solid var(--brand-line)" }}>
          <AthletesRail entries={entries} hasTeamData={hasTeamData} setId={setId} setSlug={setSlug} subjectLabel={subjectLabel} teamLabel={teamLabel} sport={sport} />
        </aside>
        {/* Right column — min-w-0 lets this 1fr grid item shrink below its
            content's intrinsic width, so the card gallery scrolls internally
            instead of widening the whole page. */}
        <div className="flex flex-col min-w-0">
          {/* Hero */}
          <div style={{ background: "var(--brand-card)", padding: "30px 36px", borderBottom: "1px solid var(--brand-line)" }}>
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
                <div style={{ fontFamily: FONT_MONO, fontSize: 10, fontWeight: 600, letterSpacing: 2.4, color: "var(--brand-slate)", textTransform: "uppercase" }}>
                  {eyebrow}
                </div>
                <h1 style={{
                  fontFamily: "var(--brand-font-head)", fontSynthesisWeight: "none", fontSize: 34, fontWeight: 400,
                  letterSpacing: -1.2, lineHeight: 1.02, color: "var(--brand-ink)", margin: "8px 0 12px",
                }}>{setName}</h1>
                <div className="flex flex-wrap items-center gap-2">
                  <span style={{ fontSize: 16, fontWeight: 500, padding: "4px 9px", borderRadius: 4, border: "1px solid var(--brand-line)", color: "var(--brand-ink-soft)" }}>
                    {sport}
                  </span>
                  {league && (
                    <span style={{ fontSize: 16, fontWeight: 500, padding: "4px 9px", borderRadius: 4, border: "1px solid var(--brand-line)", color: "var(--brand-ink-soft)" }}>
                      {league}
                    </span>
                  )}
                  <span style={{ fontSize: 16, fontWeight: 600, padding: "4px 9px", borderRadius: 4, background: "var(--brand-ink)", color: "var(--brand-page)" }}>
                    {meta.manufacturer || "Topps"}
                  </span>
                  <span style={{ fontSize: 16, color: "var(--brand-slate)" }}>
                    {athleteCount.toLocaleString()} {subjectLabel.toLowerCase()} tracked
                  </span>
                </div>
              </div>
              {/* Coverage card */}
              <CoverageCard
                hasChecklist={hasChecklist} hasNumberedParallels={hasNumberedParallels}
                hasBoxConfig={hasBoxConfig} hasPackOdds={hasPackOdds}
                breakSheetPlayers={breakSheetPlayers} setName={setName} sport={sport} league={league}
                setSlug={setSlug}
              />
            </div>
          </div>

          {/* Stat strip */}
          <StatStrip items={statItems} />

          {/* Primary tabs — sticky below the site header on scroll */}
          <div role="tablist" className="overflow-x-auto no-scrollbar" style={{
            position: "sticky", top: 0, zIndex: 20,
            background: "var(--brand-page)", padding: "0 36px", borderBottom: "1px solid var(--brand-line)",
            display: "flex", whiteSpace: "nowrap",
          }}>
            {tabList.map((t) => (
              <button key={t} role="tab" aria-selected={activeTab === t}
                onClick={() => handleSetTabChange(t)}
                style={{
                  padding: "14px 20px", flexShrink: 0,
                  fontFamily: FONT_DISPLAY,
                  fontSize: 16, fontWeight: activeTab === t ? 600 : 500,
                  color: activeTab === t ? "var(--brand-ink)" : "var(--brand-slate)",
                  borderBottom: activeTab === t ? "2px solid var(--brand-accent)" : "2px solid transparent",
                  marginBottom: -1, background: "transparent", cursor: "pointer",
                  transition: "all 150ms",
                }}>
                {t}
              </button>
            ))}
          </div>

          {/* Content area */}
          <div style={{ padding: "28px 36px 60px" }}>
            {activeTab === "Overview" ? (
              <OverviewContent boxConfig={boxConfig} cards={cards} cardTypes={cardTypes}
                parallelTypes={parallelTypes} autographs={autographs} autoParallels={autoParallels}
                totalParallels={totalParallels} athleteCount={athleteCount} releaseDate={releaseDate}
                hasChecklist={hasChecklist} hasNumberedParallels={hasNumberedParallels}
                hasBoxConfig={hasBoxConfig} hasPackOdds={hasPackOdds} subjectLabel={subjectLabel}
                featuredArticle={featuredArticle} setName={setName} aeoSummary={aeoSummary} faqs={faqs} cardImages={cardImages} toppsUrl={toppsUrl} relatedLinks={relatedLinks} />
            ) : (
              <CardTypeTabContent tab={activeTab as CardTab} subsets={subsets}
                hasNumberedParallels={hasNumberedParallels} oddsResolver={oddsResolver} />
            )}
          </div>
        </div>
      </div>

      {/* ═══ MOBILE ═══ */}
      <div className="min-[1180px]:hidden">
        {/* Sticky app bar */}
        <div className="sticky top-0 z-10 flex items-center justify-between"
          style={{
            padding: "12px 16px", borderBottom: "1px solid var(--brand-line)",
            background: "rgba(250,250,247,0.92)", backdropFilter: "blur(12px)", WebkitBackdropFilter: "blur(12px)",
          }}>
          <button onClick={() => setDrawerOpen(true)}
            style={{
              display: "flex", alignItems: "center", gap: 6,
              background: "var(--brand-card)", border: "1px solid var(--brand-line)", borderRadius: 8,
              padding: "8px 12px", fontSize: 16, fontWeight: 500, color: "var(--brand-ink)",
            }}>
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M15 19.128a9.38 9.38 0 0 0 2.625.372 9.337 9.337 0 0 0 4.121-.952 4.125 4.125 0 0 0-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128H5.228A2 2 0 0 1 3 17.208V5.792A2 2 0 0 1 5.228 3.872h13.544A2 2 0 0 1 21 5.792v6.625M12 10.5a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0Z" />
            </svg>
            Leaderboard
          </button>
          <div className="v2-break-sheet-pill">
            <BreakSheetLink slug={setSlug} setName={setName} sport={sport} league={league} players={breakSheetPlayers} />
          </div>
        </div>

        {/* Hero */}
        <div style={{ background: "var(--brand-card)", padding: "18px 16px 14px", borderBottom: "1px solid var(--brand-line)" }}>
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
              <div style={{ fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 2, color: "var(--brand-slate)", textTransform: "uppercase" }}>
                {eyebrow}
              </div>
              <h1 style={{
                fontFamily: "var(--brand-font-head)", fontSynthesisWeight: "none", fontSize: 24, fontWeight: 400,
                letterSpacing: -0.6, lineHeight: 1.1, color: "var(--brand-ink)", margin: "6px 0 8px",
              }}>{setName}</h1>
              <div className="flex flex-wrap items-center gap-1.5">
                <span style={{ fontSize: 16, fontWeight: 500, padding: "3px 7px", borderRadius: 4, border: "1px solid var(--brand-line)", color: "var(--brand-ink-soft)" }}>
                  {sport}
                </span>
                {league && (
                  <span style={{ fontSize: 16, fontWeight: 500, padding: "3px 7px", borderRadius: 4, border: "1px solid var(--brand-line)", color: "var(--brand-ink-soft)" }}>
                    {league}
                  </span>
                )}
                <span style={{ fontSize: 16, color: "var(--brand-slate)" }}>
                  {athleteCount.toLocaleString()} {subjectLabel.toLowerCase()}
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
            top: 53, background: "var(--brand-page)", padding: "0 16px",
            borderBottom: "1px solid var(--brand-line)", display: "flex", whiteSpace: "nowrap",
          }}>
          {tabList.map((t) => (
            <button key={t} role="tab" aria-selected={activeTab === t}
              onClick={() => handleSetTabChange(t)}
              style={{
                padding: "12px 14px", flexShrink: 0,
                fontFamily: FONT_DISPLAY,
                fontSize: 16, fontWeight: activeTab === t ? 600 : 500,
                color: activeTab === t ? "var(--brand-ink)" : "var(--brand-slate)",
                borderBottom: activeTab === t ? "2px solid var(--brand-accent)" : "2px solid transparent",
                marginBottom: -1, background: "transparent", cursor: "pointer",
              }}>
              {t}
            </button>
          ))}
        </div>

        {/* Content */}
        <div style={{ padding: 16 }}>
          {activeTab === "Overview" ? (
            <OverviewContent boxConfig={boxConfig} cards={cards} cardTypes={cardTypes}
              parallelTypes={parallelTypes} autographs={autographs} autoParallels={autoParallels}
              totalParallels={totalParallels} athleteCount={athleteCount} releaseDate={releaseDate}
              hasChecklist={hasChecklist} hasNumberedParallels={hasNumberedParallels}
              hasBoxConfig={hasBoxConfig} hasPackOdds={hasPackOdds} subjectLabel={subjectLabel}
              featuredArticle={featuredArticle} setName={setName} aeoSummary={aeoSummary} faqs={faqs} cardImages={cardImages} toppsUrl={toppsUrl} relatedLinks={relatedLinks} />
          ) : (
            <CardTypeTabContent tab={activeTab as CardTab} subsets={subsets}
              hasNumberedParallels={hasNumberedParallels} oddsResolver={oddsResolver} />
          )}
        </div>

        {/* Athletes drawer */}
        <MobileAthletesDrawer
          open={drawerOpen} onClose={() => setDrawerOpen(false)}
          entries={entries} hasTeamData={hasTeamData} setId={setId} setSlug={setSlug}
          athleteCount={athleteCount} subjectLabel={subjectLabel} teamLabel={teamLabel} sport={sport}
        />
      </div>
    </div>
  );
}
