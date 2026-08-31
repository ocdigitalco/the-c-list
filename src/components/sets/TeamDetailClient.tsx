"use client";

import React, { useState, useMemo, useRef, useEffect } from "react";
import Link from "next/link";
import { getNBAHeadshotUrl } from "@/lib/nba-headshot";
import { getUFCHeadshotUrl } from "@/lib/ufc-headshot";
import { getMLBHeadshotUrl } from "@/lib/mlb-headshot";
import { getTeamLogo } from "@/lib/utils/teamLogo";
import { trackEvent } from "@/lib/trackEvent";
import { PackOddsCalculator, type PackOddsSlot, type BoxFormat } from "@/components/PackOddsCalculator";

// ─── Types ──────────────────────────────────────────────────────────────────────

const FONT_DISPLAY = "var(--cl-font-display), 'Inter Tight', sans-serif";
const FONT_MONO = "var(--cl-font-mono), 'JetBrains Mono', ui-monospace, monospace";

type Tab = "Athletes" | "Calculator";
type SortKey = "totalCards" | "autographs" | "inserts" | "numberedParallels" | "name";
type SortDir = "asc" | "desc";

const TABS: Tab[] = ["Athletes", "Calculator"];

interface TeamAthlete {
  id: number;
  name: string;
  slug: string | null;
  team: string;
  isRookie: boolean;
  totalCards: number;
  autographs: number;
  inserts: number;
  numberedParallels: number;
  nbaPlayerId: number | null;
  ufcImageUrl: string | null;
  mlbPlayerId: number | null;
  imageUrl: string | null;
}

interface TeamInSet {
  name: string;
  slug: string;
  athletes: number;
  totalCards: number;
}

interface LeaderboardEntry {
  id: number; name: string; slug: string | null; team: string | null;
  isRookie: boolean; totalCards: number; autographs: number; inserts: number;
  numberedParallels: number; nbaPlayerId: number | null; ufcImageUrl: string | null;
  mlbPlayerId: number | null; imageUrl: string | null;
}

export interface TeamDetailClientProps {
  setName: string;
  setSlug: string;
  setId: number;
  sport: string;
  league: string | null;
  teamName: string;
  teamSlug: string;
  athletes: TeamAthlete[];
  athleteCount: number;
  totalCards: number;
  numberedParallels: number;
  oneOfOnes: number;
  teamsInSet: TeamInSet[];
  leaderboardEntries?: LeaderboardEntry[];
  hasLeaderboardTeamData?: boolean;
  packOddsJson?: string | null;
  boxConfigJson?: string | null;
  packOddsSlotsByFormat?: Record<string, PackOddsSlot[]>;
  boxFormats?: BoxFormat[];
  totalAutoCards?: number;
  teamAutoCards?: number;
  hasBreakCalc?: boolean;
}

// ─── Helpers ────────────────────────────────────────────────────────────────────

function InitialsAvatar({ name, size = 30, bg = "var(--brand-empty)", color = "var(--brand-slate)" }: {
  name: string; size?: number; bg?: string; color?: string;
}) {
  const initials = name.split(" ").map((n) => n[0]).slice(0, 2).join("").toUpperCase();
  return (
    <div className="rounded-full flex items-center justify-center flex-shrink-0"
      style={{ width: size, height: size, background: bg, color, fontSize: size * 0.35, fontWeight: 600 }}>
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

function TeamCrest({ name, size = 96 }: { name: string; size?: number }) {
  const initials = name.split(" ").map((n) => n[0]).slice(0, 3).join("").toUpperCase();
  return (
    <div className="flex items-center justify-center flex-shrink-0"
      style={{
        width: size, height: size, background: "var(--brand-ink)", borderRadius: 12,
        color: "var(--brand-card)", fontSize: size * 0.3, fontWeight: 700, letterSpacing: 1,
      }}>
      {initials}
    </div>
  );
}

// ─── Sortable Athletes Table (Desktop) ──────────────────────────────────────────

function AthletesTable({ athletes, setSlug, setId }: {
  athletes: TeamAthlete[]; setSlug: string; setId: number;
}) {
  const [sortKey, setSortKey] = useState<SortKey>("totalCards");
  const [sortDir, setSortDir] = useState<SortDir>("desc");
  const [position, setPosition] = useState("All Positions");
  const [rookiesOnly, setRookiesOnly] = useState(false);

  const positions = useMemo(() => {
    const posSet = new Set<string>();
    // We don't have position data in the current schema
    return ["All Positions"];
  }, []);

  const sorted = useMemo(() => {
    let list = [...athletes];
    if (rookiesOnly) list = list.filter((a) => a.isRookie);
    list.sort((a, b) => {
      if (sortKey === "name") {
        return sortDir === "asc" ? a.name.localeCompare(b.name) : b.name.localeCompare(a.name);
      }
      const diff = sortDir === "desc" ? b[sortKey] - a[sortKey] : a[sortKey] - b[sortKey];
      return diff !== 0 ? diff : a.name.localeCompare(b.name);
    });
    return list;
  }, [athletes, sortKey, sortDir, rookiesOnly]);

  function toggleSort(key: SortKey) {
    if (sortKey === key) {
      setSortDir((d) => (d === "asc" ? "desc" : "asc"));
    } else {
      setSortKey(key);
      setSortDir(key === "name" ? "asc" : "desc");
    }
  }

  const arrow = (key: SortKey) => sortKey === key ? (sortDir === "asc" ? " ▲" : " ▼") : "";

  const columns: { key: SortKey; label: string; align: "left" | "right"; width: string }[] = [
    { key: "name", label: "ATHLETE", align: "left", width: "2fr" },
    { key: "totalCards", label: "TOTAL CARDS", align: "right", width: "90px" },
    { key: "autographs", label: "AUTOGRAPHS", align: "right", width: "110px" },
    { key: "inserts", label: "INSERTS", align: "right", width: "90px" },
    { key: "numberedParallels", label: "NUMBERED PARALLELS", align: "right", width: "130px" },
  ];

  return (
    <div>
      {/* Filter row */}
      <div className="flex items-center justify-between" style={{ marginBottom: 16 }}>
        <span style={{ fontFamily: FONT_DISPLAY, fontSize: 16, fontWeight: 600, color: "var(--brand-ink)" }}>
          Athletes ({sorted.length})
        </span>
        <div className="flex items-center gap-3">
          <label className="flex items-center gap-1.5" style={{ fontSize: 16, color: "var(--brand-ink-soft)" }}>
            <input type="checkbox" checked={rookiesOnly} onChange={() => setRookiesOnly((v) => !v)}
              style={{ accentColor: "var(--brand-ink)" }} />
            Rookies only
          </label>
        </div>
      </div>

      {/* Desktop table */}
      <div className="hidden min-[1180px]:block">
        <table className="w-full" style={{ fontSize: 16, borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ background: "var(--brand-page)" }}>
              <th style={{ width: 32, padding: "10px 0 10px 18px", textAlign: "left",
                fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6,
                color: "var(--brand-slate)", borderBottom: "1px solid var(--brand-line)", textTransform: "uppercase" }}>#</th>
              {columns.map((col) => (
                <th key={col.key} onClick={() => toggleSort(col.key)}
                  style={{
                    textAlign: col.align, padding: "10px 18px", cursor: "pointer",
                    fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6,
                    color: sortKey === col.key ? "var(--brand-ink)" : "var(--brand-slate)",
                    borderBottom: "1px solid var(--brand-line)", textTransform: "uppercase",
                  }}>
                  {col.label}{arrow(col.key)}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {sorted.map((a, idx) => (
              <tr key={a.id} style={{ borderBottom: "1px solid var(--brand-line)" }}>
                <td style={{ padding: "14px 0 14px 18px", fontFamily: FONT_MONO, fontSize: 16, color: "var(--brand-slate)" }}>
                  {idx + 1}
                </td>
                <td style={{ padding: "14px 18px" }}>
                  <Link href={`/sets/${setSlug || setId}/athlete/${a.slug || a.id}`}
                    className="flex items-center gap-2.5" style={{ textDecoration: "none" }}>
                    <PlayerAvatar name={a.name} nbaPlayerId={a.nbaPlayerId} ufcImageUrl={a.ufcImageUrl}
                      mlbPlayerId={a.mlbPlayerId} imageUrl={a.imageUrl} size={30} />
                    <span style={{ fontWeight: 500, color: "var(--brand-ink)" }}>{a.name}</span>
                    {a.isRookie && (
                      <span style={{
                        background: "var(--brand-accent)", color: "var(--brand-head)",
                        fontSize: 9, fontWeight: 700, padding: "1px 5px", borderRadius: 2, letterSpacing: 0.5,
                      }}>RC</span>
                    )}
                  </Link>
                </td>
                {["totalCards", "autographs", "inserts", "numberedParallels"].map((key) => {
                  const val = a[key as keyof TeamAthlete] as number;
                  return (
                    <td key={key} style={{
                      padding: "14px 18px", textAlign: "right",
                      fontFamily: FONT_MONO, fontSize: 16, fontWeight: 600,
                      color: val === 0 ? "var(--brand-fog)" : "var(--brand-ink)",
                    }}>
                      {val === 0 ? "—" : val.toLocaleString()}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Mobile cards */}
      <div className="min-[1180px]:hidden space-y-2">
        {sorted.map((a, idx) => (
          <Link key={a.id} href={`/sets/${setSlug || setId}/athlete/${a.slug || a.id}`}
            style={{
              display: "block", background: "var(--brand-card)", border: "1px solid var(--brand-line)",
              borderRadius: 10, padding: "12px 14px", textDecoration: "none",
            }}>
            <div className="flex items-center gap-2.5">
              <span style={{ fontFamily: FONT_MONO, fontSize: 16, color: "var(--brand-slate)", width: 20 }}>{idx + 1}</span>
              <PlayerAvatar name={a.name} nbaPlayerId={a.nbaPlayerId} ufcImageUrl={a.ufcImageUrl}
                mlbPlayerId={a.mlbPlayerId} imageUrl={a.imageUrl} size={32} />
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-1.5">
                  <span style={{ fontSize: 16, fontWeight: 500, color: "var(--brand-ink)" }}>{a.name}</span>
                  {a.isRookie && (
                    <span style={{
                      background: "var(--brand-accent)", color: "var(--brand-head)",
                      fontSize: 9, fontWeight: 700, padding: "1px 5px", borderRadius: 2,
                    }}>RC</span>
                  )}
                </div>
              </div>
            </div>
            <div className="grid grid-cols-4 gap-1 mt-2" style={{
              background: "var(--brand-page)", borderRadius: 8, border: "1px solid var(--brand-line)", padding: "8px 10px",
            }}>
              {[
                { l: "CARDS", v: a.totalCards },
                { l: "AUTOS", v: a.autographs },
                { l: "INSERTS", v: a.inserts },
                { l: "NUMBERED", v: a.numberedParallels },
              ].map((s) => (
                <div key={s.l} className="text-center">
                  <div style={{ fontFamily: FONT_MONO, fontSize: 8, fontWeight: 600, letterSpacing: 1.2, color: "var(--brand-slate)", textTransform: "uppercase" }}>
                    {s.l}
                  </div>
                  <div style={{ fontFamily: FONT_MONO, fontSize: 16, fontWeight: 600, color: s.v === 0 ? "var(--brand-fog)" : "var(--brand-ink)", marginTop: 2 }}>
                    {s.v === 0 ? "—" : s.v.toLocaleString()}
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

// ─── Mobile Teams Drawer ────────────────────────────────────────────────────────

function TeamsDrawer({ open, onClose, teams, currentTeam, setSlug, setId }: {
  open: boolean; onClose: () => void; teams: TeamInSet[];
  currentTeam: string; setSlug: string; setId: number;
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
        background: "var(--brand-card)", transform: open ? "translateY(0)" : "translateY(100%)",
        transition: "transform 200ms ease-out", pointerEvents: open ? "auto" : "none",
      }}>
      <div className="flex items-center justify-between" style={{
        padding: "14px 16px", borderBottom: "1px solid var(--brand-line)",
      }}>
        <button onClick={onClose} aria-label="Close" className="p-1">
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="var(--brand-ink)" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18 18 6M6 6l12 12" />
          </svg>
        </button>
        <span style={{ fontFamily: FONT_DISPLAY, fontSize: 17, fontWeight: 600, letterSpacing: -0.3, color: "var(--brand-ink)" }}>
          Teams in Set
        </span>
        <span style={{ fontFamily: FONT_MONO, fontSize: 16, color: "var(--brand-slate)" }}>{teams.length}</span>
      </div>
      <div className="flex-1 overflow-y-auto" style={{ height: "calc(100% - 56px)" }}>
        {teams.map((t) => (
          <Link key={t.name} href={`/sets/${setSlug || setId}/team/${t.slug}`} onClick={onClose}
            className="flex items-center gap-3 transition-colors"
            style={{
              padding: "12px 16px", borderBottom: "1px solid var(--brand-line)", textDecoration: "none",
              background: t.name === currentTeam ? "var(--brand-line)" : "transparent",
              borderLeft: t.name === currentTeam ? "2px solid var(--brand-ink)" : "2px solid transparent",
            }}>
            <TeamCrest name={t.name} size={36} />
            <div className="flex-1 min-w-0">
              <span style={{ fontSize: 16, fontWeight: 500, color: "var(--brand-ink)" }}>{t.name}</span>
            </div>
            <div className="text-right">
              <div style={{ fontFamily: FONT_MONO, fontSize: 16, fontWeight: 600, color: "var(--brand-ink)" }}>
                {t.totalCards.toLocaleString()}
              </div>
              <div style={{ fontFamily: FONT_MONO, fontSize: 16, color: "var(--brand-slate)" }}>
                {t.athletes} athletes
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}

// ─── Main Component ─────────────────────────────────────────────────────────────

// ─── Set-Wide Leaderboard (matches AthletesRail from SetDetailClient) ────────

type LBSortKey = "totalCards" | "autographs" | "inserts" | "numberedParallels";
const LB_CHIPS: { key: LBSortKey; label: string }[] = [
  { key: "totalCards", label: "Total Cards" },
  { key: "autographs", label: "Autographs" },
  { key: "inserts", label: "Inserts" },
  { key: "numberedParallels", label: "Numbered" },
];

function SetWideLeaderboard({ entries, hasTeamData, setId, setSlug, sport = "" }: {
  entries: LeaderboardEntry[]; hasTeamData: boolean; setId: number; setSlug: string; sport?: string;
}) {
  const [sortKey, setSortKey] = useState<LBSortKey>("totalCards");
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
    <div className="flex flex-col h-full" style={{ background: "var(--brand-card)" }}>
      {hasTeamData && (
        <div className="shrink-0 flex" style={{ borderBottom: "1px solid var(--brand-line)", padding: "0 18px" }}>
          {([["athletes", `Athletes (${entries.length})`], ["teams", `Teams (${teamCount})`]] as const).map(([mode, label]) => (
            <button key={mode} onClick={() => { setViewMode(mode); setShowAll(false); }}
              style={{
                padding: "12px 16px", fontFamily: FONT_DISPLAY, fontSize: 16,
                fontWeight: viewMode === mode ? 600 : 500,
                color: viewMode === mode ? "var(--brand-ink)" : "var(--brand-slate)",
                borderBottom: viewMode === mode ? "2px solid var(--brand-ink)" : "2px solid transparent",
                marginBottom: -1, background: "transparent", cursor: "pointer", transition: "all 150ms",
              }}>{label}</button>
          ))}
        </div>
      )}
      <div className="shrink-0 space-y-3" style={{ padding: "14px 18px 12px" }}>
        <div className="relative">
          <svg className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 pointer-events-none" style={{ color: "var(--brand-slate)" }}
            fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
            <path strokeLinecap="round" strokeLinejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
          </svg>
          <input type="text" value={query} onChange={(e) => setQuery(e.target.value)}
            placeholder={viewMode === "teams" ? "Search teams…" : "Search athletes…"}
            autoComplete="off" spellCheck={false} className="w-full outline-none"
            style={{ background: "var(--brand-track)", borderRadius: 8, padding: "7px 10px 7px 30px", fontSize: 16, border: "none", color: "var(--brand-ink)" }} />
        </div>
        <div className="flex flex-wrap gap-1.5">
          {LB_CHIPS.map((chip) => (
            <button key={chip.key} onClick={() => setSortKey(chip.key)}
              style={{
                borderRadius: 4, padding: "4px 9px", fontSize: 16, fontWeight: 500,
                background: sortKey === chip.key ? "var(--brand-ink)" : "transparent",
                color: sortKey === chip.key ? "var(--brand-page)" : "var(--brand-ink-soft)",
                border: sortKey === chip.key ? "1px solid var(--brand-ink)" : "1px solid var(--brand-line)",
              }}>{chip.label}</button>
          ))}
        </div>
        {viewMode === "athletes" && (
          <label className="flex items-center gap-1.5 cursor-pointer" style={{ fontSize: 16, color: "var(--brand-ink-soft)" }}>
            <input type="checkbox" checked={rookiesOnly} onChange={() => setRookiesOnly((v) => !v)} style={{ accentColor: "var(--brand-ink)" }} />
            Rookies only
          </label>
        )}
      </div>
      <div className="shrink-0 flex justify-between items-center"
        style={{ padding: "6px 18px", borderBottom: "1px solid var(--brand-line)", fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6, color: "var(--brand-slate)", textTransform: "uppercase" }}>
        <span>{viewMode === "teams" ? "TEAM" : "ATHLETE"}</span>
        <span>{LB_CHIPS.find((c) => c.key === sortKey)?.label}</span>
      </div>
      <div className="flex-1 overflow-y-auto">
        {viewMode === "athletes" ? (
          visible.length === 0 ? <p className="text-center py-8" style={{ fontSize: 16, color: "var(--brand-slate)", fontStyle: "italic" }}>No athletes match.</p> : (
            <>
              {visible.map((entry, idx) => (
                <Link key={entry.id} href={`/sets/${setSlug || setId}/athlete/${entry.slug || entry.id}`}
                  // Search selection → "search" only when a query is active; the
                  // page visit itself is counted as a "view" on mount.
                  onClick={() => { if (query.trim()) trackEvent(entry.id, "search"); }}
                  className="flex items-center gap-2 transition-colors"
                  style={{ padding: "9px 18px", borderBottom: "1px solid var(--brand-line)", textDecoration: "none" }}
                  onMouseEnter={(e) => { (e.currentTarget as HTMLElement).style.background = "var(--brand-track)"; }}
                  onMouseLeave={(e) => { (e.currentTarget as HTMLElement).style.background = "transparent"; }}>
                  <span style={{ fontFamily: FONT_MONO, fontSize: 16, color: "var(--brand-slate)", width: 18, textAlign: "right", flexShrink: 0 }}>{idx + 1}</span>
                  <PlayerAvatar name={entry.name} nbaPlayerId={entry.nbaPlayerId} ufcImageUrl={entry.ufcImageUrl} mlbPlayerId={entry.mlbPlayerId} imageUrl={entry.imageUrl} size={30} />
                  <div className="flex-1 min-w-0">
                    <span className="truncate block" style={{ fontSize: 16, fontWeight: 500, color: "var(--brand-ink)" }}>{entry.name}</span>
                    {hasTeamData && entry.team && <p className="truncate" style={{ fontSize: 16, color: "var(--brand-slate)", marginTop: 1 }}>{entry.team}</p>}
                  </div>
                  <span style={{ fontFamily: FONT_MONO, fontSize: 16, fontWeight: 600, color: "var(--brand-ink)", flexShrink: 0 }}>{entry[sortKey].toLocaleString()}</span>
                </Link>
              ))}
              {!showAll && filtered.length > 50 && <button onClick={() => setShowAll(true)} className="w-full py-3" style={{ fontSize: 16, fontWeight: 600, color: "var(--brand-ink)" }}>Show all {filtered.length} athletes</button>}
            </>
          )
        ) : (
          teamRows.length === 0 ? <p className="text-center py-8" style={{ fontSize: 16, color: "var(--brand-slate)", fontStyle: "italic" }}>No teams match.</p> : (
            <>
              {(showAll ? teamRows : teamRows.slice(0, 50)).map((tr, idx) => (
                <Link key={tr.team} href={`/sets/${setSlug || setId}/team/${tr.team.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "")}`}
                  className="flex items-center gap-2 transition-colors"
                  style={{ padding: "9px 18px", borderBottom: "1px solid var(--brand-line)", textDecoration: "none" }}
                  onMouseEnter={(e) => { (e.currentTarget as HTMLElement).style.background = "var(--brand-track)"; }}
                  onMouseLeave={(e) => { (e.currentTarget as HTMLElement).style.background = "transparent"; }}>
                  <span style={{ fontFamily: FONT_MONO, fontSize: 16, color: "var(--brand-slate)", width: 18, textAlign: "right", flexShrink: 0 }}>{idx + 1}</span>
                  <TeamLogo teamName={tr.team} sport={sport} size={30} />
                  <div className="flex-1 min-w-0">
                    <span className="truncate block" style={{ fontSize: 16, fontWeight: 500, color: "var(--brand-ink)" }}>{tr.team}</span>
                    <p className="truncate" style={{ fontSize: 16, color: "var(--brand-slate)", marginTop: 1 }}>{tr.athleteCount} {tr.athleteCount === 1 ? "Athlete" : "Athletes"}</p>
                  </div>
                  <span style={{ fontFamily: FONT_MONO, fontSize: 16, fontWeight: 600, color: "var(--brand-ink)", flexShrink: 0 }}>{tr[sortKey].toLocaleString()}</span>
                </Link>
              ))}
            </>
          )
        )}
      </div>
    </div>
  );
}

export function TeamDetailClient({
  setName, setSlug, setId, sport, league, teamName, teamSlug,
  athletes, athleteCount, totalCards, numberedParallels, oneOfOnes, teamsInSet,
  leaderboardEntries = [], hasLeaderboardTeamData = false,
  packOddsJson, boxConfigJson,
  packOddsSlotsByFormat = {}, boxFormats = [], totalAutoCards = 0, teamAutoCards = 0, hasBreakCalc = false,
}: TeamDetailClientProps) {
  const [tab, setTab] = useState<Tab>("Athletes");
  const [drawerOpen, setDrawerOpen] = useState(false);

  const statItems = [
    { label: "Athletes", value: athleteCount },
    { label: "Total Cards", value: totalCards },
    { label: "Numbered Parallels", value: numberedParallels },
    { label: "1/1s", value: oneOfOnes },
  ];

  return (
    <div style={{ background: "var(--brand-page)", minHeight: "100vh" }}>
      {/* ═══ DESKTOP ═══ */}
      <div className="hidden min-[1180px]:grid" style={{ gridTemplateColumns: "425px 1fr", minHeight: "100vh" }}>
        {/* Left rail — set-wide leaderboard */}
        <aside className="sticky top-0 h-screen overflow-y-auto" style={{ borderRight: "1px solid var(--brand-line)", background: "var(--brand-card)" }}>
          <SetWideLeaderboard entries={leaderboardEntries} hasTeamData={hasLeaderboardTeamData} setId={setId} setSlug={setSlug} sport={sport} />
        </aside>

        {/* Right column */}
        <div className="flex flex-col">
          {/* Hero */}
          <div style={{ background: "var(--brand-card)", padding: "22px 36px 28px", borderBottom: "1px solid var(--brand-line)" }}>
            {/* Breadcrumb */}
            <Link href={`/sets/${setSlug || setId}`} style={{ fontSize: 16, color: "var(--brand-slate)", textDecoration: "none", fontFamily: FONT_DISPLAY }}>
              &lsaquo; {setName}
            </Link>
            <div className="grid items-center gap-8 mt-4" style={{ gridTemplateColumns: "96px 1fr 280px" }}>
              <TeamLogo teamName={teamName} sport={sport} size={96} />
              <div>
                <div style={{ fontFamily: FONT_MONO, fontSize: 10, fontWeight: 600, letterSpacing: 2.4, color: "var(--brand-slate)", textTransform: "uppercase" }}>
                  {league ?? sport}
                </div>
                <h1 style={{
                  fontFamily: "var(--brand-font-head)", fontSynthesisWeight: "none", fontSize: 38, fontWeight: 400,
                  letterSpacing: -1, lineHeight: 1.08, color: "var(--brand-ink)", margin: "6px 0 12px",
                  textWrap: "balance",
                }}>{teamName}</h1>
                <div className="flex flex-wrap items-center gap-2">
                  <span style={{ fontSize: 16, fontWeight: 500, padding: "4px 9px", borderRadius: 4, border: "1px solid var(--brand-line)", color: "var(--brand-ink-soft)" }}>
                    {sport}
                  </span>
                  {league && (
                    <span style={{ fontSize: 16, fontWeight: 500, padding: "4px 9px", borderRadius: 4, border: "1px solid var(--brand-line)", color: "var(--brand-ink-soft)" }}>
                      {league}
                    </span>
                  )}
                </div>
              </div>
              {/* Roster Summary */}
              <div style={{ border: "2px solid var(--brand-track)", padding: "14px 16px" }}>
                <div style={{ fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6, color: "var(--brand-slate)", textTransform: "uppercase", marginBottom: 10 }}>
                  Roster Summary
                </div>
                {[
                  { l: "Athletes", v: athleteCount.toString() },
                  { l: "Total Cards", v: totalCards.toLocaleString() },
                  { l: "Rookies", v: athletes.filter((a) => a.isRookie).length.toString() },
                  { l: "Autographs", v: athletes.reduce((s, a) => s + a.autographs, 0).toString() },
                ].map((r, i, arr) => (
                  <div key={r.l} className="flex items-center justify-between" style={{
                    padding: "6px 0", borderBottom: i < arr.length - 1 ? "1px solid var(--brand-line)" : "none",
                  }}>
                    <span style={{ fontSize: 16, color: "var(--brand-slate)" }}>{r.l}</span>
                    <span style={{ fontFamily: FONT_MONO, fontSize: 16, fontWeight: 600, color: "var(--brand-ink)" }}>{r.v}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Stat strip */}
          <div className="grid" style={{
            gridTemplateColumns: "repeat(4, 1fr)", borderBottom: "1px solid var(--brand-line)", background: "var(--brand-card)",
          }}>
            {statItems.map((item, i) => (
              <div key={item.label} style={{
                padding: "18px 22px", borderRight: i < statItems.length - 1 ? "1px solid var(--brand-line)" : "none",
              }}>
                <div style={{ fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6, color: "var(--brand-slate)", textTransform: "uppercase" }}>
                  {item.label}
                </div>
                <div style={{ fontFamily: "var(--brand-font-head)", fontSynthesisWeight: "none", fontSize: 26, fontWeight: 400, color: "var(--brand-ink)", marginTop: 4 }}>
                  {item.value.toLocaleString()}
                </div>
              </div>
            ))}
          </div>

          {/* Tabs */}
          <div role="tablist" style={{
            background: "var(--brand-page)", padding: "0 36px", borderBottom: "1px solid var(--brand-line)", display: "flex",
          }}>
            {TABS.map((t) => (
              <button key={t} role="tab" aria-selected={tab === t} onClick={() => setTab(t)}
                style={{
                  padding: "14px 20px", fontFamily: FONT_DISPLAY,
                  fontSize: 16, fontWeight: tab === t ? 600 : 500,
                  color: tab === t ? "var(--brand-ink)" : "var(--brand-slate)",
                  borderBottom: tab === t ? "2px solid var(--brand-ink)" : "2px solid transparent",
                  marginBottom: -1, background: "transparent", cursor: "pointer", transition: "all 150ms",
                }}>
                {t}
              </button>
            ))}
          </div>

          {/* Content */}
          <div style={{ padding: "28px 36px 60px" }}>
            {tab === "Athletes" && (
              <AthletesTable athletes={athletes} setSlug={setSlug} setId={setId} />
            )}
            {tab === "Calculator" && (
              hasBreakCalc ? (
                <PackOddsCalculator
                  slotsByFormat={packOddsSlotsByFormat}
                  boxFormats={boxFormats}
                  totalAutoCards={totalAutoCards}
                  playerAutoCards={teamAutoCards}
                  setId={setId}
                  setName={setName}
                  setSlug={setSlug}
                />
              ) : (
                <div style={{ padding: "40px 20px", textAlign: "center", fontSize: 16, color: "var(--brand-slate)" }}>
                  <p style={{ fontStyle: "italic" }}>Pack odds not yet available for this set.</p>
                  <p style={{ fontSize: 14, marginTop: 8 }}>Once pack odds are published, the Break Hit Calculator will appear here.</p>
                </div>
              )
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
            background: "color-mix(in srgb, var(--brand-head) 92%, transparent)", backdropFilter: "blur(12px)", WebkitBackdropFilter: "blur(12px)",
          }}>
          <button onClick={() => setDrawerOpen(true)}
            style={{
              display: "flex", alignItems: "center", gap: 6,
              background: "var(--brand-card)", border: "1px solid var(--brand-line)", borderRadius: 8,
              padding: "8px 12px", fontSize: 16, fontWeight: 500, color: "var(--brand-ink)",
            }}>
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6A2.25 2.25 0 0 1 6 3.75h2.25A2.25 2.25 0 0 1 10.5 6v2.25a2.25 2.25 0 0 1-2.25 2.25H6a2.25 2.25 0 0 1-2.25-2.25V6ZM3.75 15.75A2.25 2.25 0 0 1 6 13.5h2.25a2.25 2.25 0 0 1 2.25 2.25V18a2.25 2.25 0 0 1-2.25 2.25H6A2.25 2.25 0 0 1 3.75 18v-2.25ZM13.5 6a2.25 2.25 0 0 1 2.25-2.25H18A2.25 2.25 0 0 1 20.25 6v2.25A2.25 2.25 0 0 1 18 10.5h-2.25a2.25 2.25 0 0 1-2.25-2.25V6ZM13.5 15.75a2.25 2.25 0 0 1 2.25-2.25H18a2.25 2.25 0 0 1 2.25 2.25V18A2.25 2.25 0 0 1 18 20.25h-2.25a2.25 2.25 0 0 1-2.25-2.25v-2.25Z" />
            </svg>
            Teams
          </button>
          <Link href={`/sets/${setSlug || setId}`} style={{ fontSize: 16, color: "var(--brand-slate)", textDecoration: "none", fontFamily: FONT_DISPLAY }}>
            {setName} &rsaquo;
          </Link>
        </div>

        {/* Hero */}
        <div style={{ background: "var(--brand-card)", padding: "18px 16px 14px", borderBottom: "1px solid var(--brand-line)" }}>
          <div className="flex items-start gap-4">
            <TeamLogo teamName={teamName} sport={sport} size={72} />
            <div className="flex-1 min-w-0">
              <div style={{ fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 2, color: "var(--brand-slate)", textTransform: "uppercase" }}>
                {league ?? sport}
              </div>
              <h1 style={{
                fontFamily: "var(--brand-font-head)", fontSynthesisWeight: "none", fontSize: 22, fontWeight: 400,
                letterSpacing: -0.6, lineHeight: 1.05, color: "var(--brand-ink)", margin: "4px 0 8px",
              }}>{teamName}</h1>
              <div className="flex flex-wrap items-center gap-1.5">
                <span style={{ fontSize: 16, fontWeight: 500, padding: "3px 7px", borderRadius: 4, border: "1px solid var(--brand-line)", color: "var(--brand-ink-soft)" }}>
                  {sport}
                </span>
                {league && (
                  <span style={{ fontSize: 16, fontWeight: 500, padding: "3px 7px", borderRadius: 4, border: "1px solid var(--brand-line)", color: "var(--brand-ink-soft)" }}>
                    {league}
                  </span>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Stat grid (mobile) */}
        <div className="grid" style={{
          gridTemplateColumns: "repeat(4, 1fr)", borderBottom: "1px solid var(--brand-line)", background: "var(--brand-card)",
        }}>
          {statItems.map((item, i) => (
            <div key={item.label} style={{
              padding: "12px 10px", borderRight: i < statItems.length - 1 ? "1px solid var(--brand-line)" : "none",
            }}>
              <div style={{ fontFamily: FONT_MONO, fontSize: 8, fontWeight: 600, letterSpacing: 1.2, color: "var(--brand-slate)", textTransform: "uppercase" }}>
                {item.label}
              </div>
              <div style={{ fontFamily: "var(--brand-font-head)", fontSynthesisWeight: "none", fontSize: 18, fontWeight: 400, color: "var(--brand-ink)", marginTop: 4 }}>
                {item.value.toLocaleString()}
              </div>
            </div>
          ))}
        </div>

        {/* Sticky tabs */}
        <div role="tablist" className="sticky z-[5] overflow-x-auto no-scrollbar"
          style={{
            top: 53, background: "var(--brand-page)", padding: "0 16px",
            borderBottom: "1px solid var(--brand-line)", display: "flex", whiteSpace: "nowrap",
          }}>
          {TABS.map((t) => (
            <button key={t} role="tab" aria-selected={tab === t} onClick={() => setTab(t)}
              style={{
                padding: "12px 12px", flexShrink: 0, fontFamily: FONT_DISPLAY,
                fontSize: 16, fontWeight: tab === t ? 600 : 500,
                color: tab === t ? "var(--brand-ink)" : "var(--brand-slate)",
                borderBottom: tab === t ? "2px solid var(--brand-ink)" : "2px solid transparent",
                marginBottom: -1, background: "transparent", cursor: "pointer",
              }}>
              {t}
            </button>
          ))}
        </div>

        {/* Content */}
        <div style={{ padding: 16 }}>
          {tab === "Athletes" && (
            <AthletesTable athletes={athletes} setSlug={setSlug} setId={setId} />
          )}
          {tab === "Calculator" && (
            <div style={{ padding: "40px 20px", textAlign: "center", fontSize: 16, fontStyle: "italic", color: "var(--brand-slate)" }}>
              Break Hit Calculator coming soon.
            </div>
          )}
        </div>

        {/* Teams drawer */}
        <TeamsDrawer open={drawerOpen} onClose={() => setDrawerOpen(false)}
          teams={teamsInSet} currentTeam={teamName} setSlug={setSlug} setId={setId} />
      </div>
    </div>
  );
}
