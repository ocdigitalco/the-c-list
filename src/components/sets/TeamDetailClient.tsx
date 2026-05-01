"use client";

import React, { useState, useMemo, useRef, useEffect } from "react";
import Link from "next/link";
import { getNBAHeadshotUrl } from "@/lib/nba-headshot";
import { getUFCHeadshotUrl } from "@/lib/ufc-headshot";
import { getMLBHeadshotUrl } from "@/lib/mlb-headshot";
import { trackEvent } from "@/lib/trackEvent";

// ─── Types ──────────────────────────────────────────────────────────────────────

const FONT_DISPLAY = "var(--cl-font-display), 'Inter Tight', sans-serif";
const FONT_MONO = "var(--cl-font-mono), 'JetBrains Mono', ui-monospace, monospace";

type Tab = "Overview" | "Athletes" | "Inserts" | "Autographs" | "Numbered Parallels";
type SortKey = "totalCards" | "autographs" | "inserts" | "numberedParallels" | "name";
type SortDir = "asc" | "desc";

const TABS: Tab[] = ["Overview", "Athletes", "Inserts", "Autographs", "Numbered Parallels"];

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
}

// ─── Helpers ────────────────────────────────────────────────────────────────────

function InitialsAvatar({ name, size = 30, bg = "#EAE6D9", color = "#6B6757" }: {
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
        width: size, height: size, background: "#0B2244", borderRadius: 12,
        color: "#FFFFFF", fontSize: size * 0.3, fontWeight: 700, letterSpacing: 1,
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
        <span style={{ fontFamily: FONT_DISPLAY, fontSize: 16, fontWeight: 600, color: "#0F0F0E" }}>
          Athletes ({sorted.length})
        </span>
        <div className="flex items-center gap-3">
          <label className="flex items-center gap-1.5" style={{ fontSize: 16, color: "#3A372F" }}>
            <input type="checkbox" checked={rookiesOnly} onChange={() => setRookiesOnly((v) => !v)}
              style={{ accentColor: "#0F0F0E" }} />
            Rookies only
          </label>
        </div>
      </div>

      {/* Desktop table */}
      <div className="hidden min-[1180px]:block">
        <table className="w-full" style={{ fontSize: 16, borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ background: "#FAFAF7" }}>
              <th style={{ width: 32, padding: "10px 0 10px 18px", textAlign: "left",
                fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6,
                color: "#8A8677", borderBottom: "1px solid #EDEAE0", textTransform: "uppercase" }}>#</th>
              {columns.map((col) => (
                <th key={col.key} onClick={() => toggleSort(col.key)}
                  style={{
                    textAlign: col.align, padding: "10px 18px", cursor: "pointer",
                    fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6,
                    color: sortKey === col.key ? "#0F0F0E" : "#8A8677",
                    borderBottom: "1px solid #EDEAE0", textTransform: "uppercase",
                  }}>
                  {col.label}{arrow(col.key)}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {sorted.map((a, idx) => (
              <tr key={a.id} style={{ borderBottom: "1px solid #F4F1E8" }}>
                <td style={{ padding: "14px 0 14px 18px", fontFamily: FONT_MONO, fontSize: 16, color: "#8A8677" }}>
                  {idx + 1}
                </td>
                <td style={{ padding: "14px 18px" }}>
                  <Link href={`/sets/${setSlug || setId}/athlete/${a.slug || a.id}`}
                    onClick={() => trackEvent(a.id, "view")}
                    className="flex items-center gap-2.5" style={{ textDecoration: "none" }}>
                    <PlayerAvatar name={a.name} nbaPlayerId={a.nbaPlayerId} ufcImageUrl={a.ufcImageUrl}
                      mlbPlayerId={a.mlbPlayerId} imageUrl={a.imageUrl} size={30} />
                    <span style={{ fontWeight: 500, color: "#0F0F0E" }}>{a.name}</span>
                    {a.isRookie && (
                      <span style={{
                        background: "oklch(0.55 0.17 25)", color: "#FFF8F1",
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
                      color: val === 0 ? "#B7B2A3" : "#0F0F0E",
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
            onClick={() => trackEvent(a.id, "view")}
            style={{
              display: "block", background: "#FFFFFF", border: "1px solid #EDEAE0",
              borderRadius: 10, padding: "12px 14px", textDecoration: "none",
            }}>
            <div className="flex items-center gap-2.5">
              <span style={{ fontFamily: FONT_MONO, fontSize: 16, color: "#8A8677", width: 20 }}>{idx + 1}</span>
              <PlayerAvatar name={a.name} nbaPlayerId={a.nbaPlayerId} ufcImageUrl={a.ufcImageUrl}
                mlbPlayerId={a.mlbPlayerId} imageUrl={a.imageUrl} size={32} />
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-1.5">
                  <span style={{ fontSize: 16, fontWeight: 500, color: "#0F0F0E" }}>{a.name}</span>
                  {a.isRookie && (
                    <span style={{
                      background: "oklch(0.55 0.17 25)", color: "#FFF8F1",
                      fontSize: 9, fontWeight: 700, padding: "1px 5px", borderRadius: 2,
                    }}>RC</span>
                  )}
                </div>
              </div>
            </div>
            <div className="grid grid-cols-4 gap-1 mt-2" style={{
              background: "#FAFAF7", borderRadius: 8, border: "1px solid #EDEAE0", padding: "8px 10px",
            }}>
              {[
                { l: "CARDS", v: a.totalCards },
                { l: "AUTOS", v: a.autographs },
                { l: "INSERTS", v: a.inserts },
                { l: "NUMBERED", v: a.numberedParallels },
              ].map((s) => (
                <div key={s.l} className="text-center">
                  <div style={{ fontFamily: FONT_MONO, fontSize: 8, fontWeight: 600, letterSpacing: 1.2, color: "#8A8677", textTransform: "uppercase" }}>
                    {s.l}
                  </div>
                  <div style={{ fontFamily: FONT_MONO, fontSize: 16, fontWeight: 600, color: s.v === 0 ? "#B7B2A3" : "#0F0F0E", marginTop: 2 }}>
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
        background: "#FFFFFF", transform: open ? "translateY(0)" : "translateY(100%)",
        transition: "transform 200ms ease-out", pointerEvents: open ? "auto" : "none",
      }}>
      <div className="flex items-center justify-between" style={{
        padding: "14px 16px", borderBottom: "1px solid #EDEAE0",
      }}>
        <button onClick={onClose} aria-label="Close" className="p-1">
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="#0F0F0E" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18 18 6M6 6l12 12" />
          </svg>
        </button>
        <span style={{ fontFamily: FONT_DISPLAY, fontSize: 17, fontWeight: 600, letterSpacing: -0.3, color: "#0F0F0E" }}>
          Teams in Set
        </span>
        <span style={{ fontFamily: FONT_MONO, fontSize: 16, color: "#8A8677" }}>{teams.length}</span>
      </div>
      <div className="flex-1 overflow-y-auto" style={{ height: "calc(100% - 56px)" }}>
        {teams.map((t) => (
          <Link key={t.name} href={`/sets/${setSlug || setId}/team/${t.slug}`} onClick={onClose}
            className="flex items-center gap-3 transition-colors"
            style={{
              padding: "12px 16px", borderBottom: "1px solid #F4F1E8", textDecoration: "none",
              background: t.name === currentTeam ? "#F4F1E8" : "transparent",
              borderLeft: t.name === currentTeam ? "2px solid #0F0F0E" : "2px solid transparent",
            }}>
            <TeamCrest name={t.name} size={36} />
            <div className="flex-1 min-w-0">
              <span style={{ fontSize: 16, fontWeight: 500, color: "#0F0F0E" }}>{t.name}</span>
            </div>
            <div className="text-right">
              <div style={{ fontFamily: FONT_MONO, fontSize: 16, fontWeight: 600, color: "#0F0F0E" }}>
                {t.totalCards.toLocaleString()}
              </div>
              <div style={{ fontFamily: FONT_MONO, fontSize: 16, color: "#8A8677" }}>
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

export function TeamDetailClient({
  setName, setSlug, setId, sport, league, teamName, teamSlug,
  athletes, athleteCount, totalCards, numberedParallels, oneOfOnes, teamsInSet,
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
    <div style={{ background: "#FAFAF7", minHeight: "100vh" }}>
      {/* ═══ DESKTOP ═══ */}
      <div className="hidden min-[1180px]:grid" style={{ gridTemplateColumns: "300px 1fr", minHeight: "100vh" }}>
        {/* Left rail — athletes on this team */}
        <aside className="sticky top-0 h-screen overflow-y-auto" style={{ borderRight: "1px solid #EDEAE0", background: "#FFFFFF" }}>
          <div style={{ padding: "22px 18px 12px" }}>
            <h2 style={{ fontFamily: FONT_DISPLAY, fontWeight: 600, fontSize: 16, letterSpacing: -0.2, color: "#0F0F0E", marginBottom: 12 }}>
              Athletes on {teamName}
            </h2>
          </div>
          <div className="flex-1 overflow-y-auto">
            {athletes.map((a, idx) => (
              <Link key={a.id} href={`/sets/${setSlug || setId}/athlete/${a.slug || a.id}`}
                onClick={() => trackEvent(a.id, "view")}
                className="flex items-center gap-2 transition-colors"
                style={{ padding: "9px 18px", borderBottom: "1px solid #F4F1E8", textDecoration: "none" }}
                onMouseEnter={(e) => { (e.currentTarget as HTMLElement).style.background = "#F1EFE9"; }}
                onMouseLeave={(e) => { (e.currentTarget as HTMLElement).style.background = "transparent"; }}>
                <span style={{ fontFamily: FONT_MONO, fontSize: 16, color: "#8A8677", width: 18, textAlign: "right", flexShrink: 0 }}>
                  {idx + 1}
                </span>
                <PlayerAvatar name={a.name} nbaPlayerId={a.nbaPlayerId} ufcImageUrl={a.ufcImageUrl}
                  mlbPlayerId={a.mlbPlayerId} imageUrl={a.imageUrl} size={30} />
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-1.5 min-w-0">
                    <span className="truncate" style={{ fontSize: 16, fontWeight: 500, color: "#0F0F0E" }}>{a.name}</span>
                    {a.isRookie && (
                      <span className="shrink-0" style={{
                        background: "oklch(0.55 0.17 25)", color: "#FFF8F1",
                        fontSize: 9, fontWeight: 700, padding: "1px 5px", borderRadius: 2,
                      }}>RC</span>
                    )}
                  </div>
                </div>
                <span style={{ fontFamily: FONT_MONO, fontSize: 16, fontWeight: 600, color: "#0F0F0E", flexShrink: 0 }}>
                  {a.totalCards.toLocaleString()}
                </span>
              </Link>
            ))}
          </div>
        </aside>

        {/* Right column */}
        <div className="flex flex-col">
          {/* Hero */}
          <div style={{ background: "#FFFFFF", padding: "22px 36px 28px", borderBottom: "1px solid #EDEAE0" }}>
            {/* Breadcrumb */}
            <Link href={`/sets/${setSlug || setId}`} style={{ fontSize: 16, color: "#6B6757", textDecoration: "none", fontFamily: FONT_DISPLAY }}>
              &lsaquo; {setName}
            </Link>
            <div className="grid items-center gap-8 mt-4" style={{ gridTemplateColumns: "96px 1fr 280px" }}>
              <TeamCrest name={teamName} size={96} />
              <div>
                <div style={{ fontFamily: FONT_MONO, fontSize: 10, fontWeight: 600, letterSpacing: 2.4, color: "#8A8677", textTransform: "uppercase" }}>
                  {league ?? sport}
                </div>
                <h1 style={{
                  fontFamily: FONT_DISPLAY, fontSize: 38, fontWeight: 600,
                  letterSpacing: -1, lineHeight: 1.08, color: "#0F0F0E", margin: "6px 0 12px",
                  textWrap: "balance",
                }}>{teamName}</h1>
                <div className="flex flex-wrap items-center gap-2">
                  <span style={{ fontSize: 16, fontWeight: 500, padding: "4px 9px", borderRadius: 4, border: "1px solid #E6E3D9", color: "#3A372F" }}>
                    {sport}
                  </span>
                  {league && (
                    <span style={{ fontSize: 16, fontWeight: 500, padding: "4px 9px", borderRadius: 4, border: "1px solid #E6E3D9", color: "#3A372F" }}>
                      {league}
                    </span>
                  )}
                </div>
              </div>
              {/* Roster Summary */}
              <div style={{ border: "2px solid #F2F0E9", padding: "14px 16px" }}>
                <div style={{ fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6, color: "#8A8677", textTransform: "uppercase", marginBottom: 10 }}>
                  Roster Summary
                </div>
                {[
                  { l: "Athletes", v: athleteCount.toString() },
                  { l: "Total Cards", v: totalCards.toLocaleString() },
                  { l: "Rookies", v: athletes.filter((a) => a.isRookie).length.toString() },
                  { l: "Autographs", v: athletes.reduce((s, a) => s + a.autographs, 0).toString() },
                ].map((r, i, arr) => (
                  <div key={r.l} className="flex items-center justify-between" style={{
                    padding: "6px 0", borderBottom: i < arr.length - 1 ? "1px solid #F4F1E8" : "none",
                  }}>
                    <span style={{ fontSize: 16, color: "#6B6757" }}>{r.l}</span>
                    <span style={{ fontFamily: FONT_MONO, fontSize: 16, fontWeight: 600, color: "#0F0F0E" }}>{r.v}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Stat strip */}
          <div className="grid" style={{
            gridTemplateColumns: "repeat(4, 1fr)", borderBottom: "1px solid #EDEAE0", background: "#FFFFFF",
          }}>
            {statItems.map((item, i) => (
              <div key={item.label} style={{
                padding: "18px 22px", borderRight: i < statItems.length - 1 ? "1px solid #EDEAE0" : "none",
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

          {/* Tabs */}
          <div role="tablist" style={{
            background: "#FAFAF7", padding: "0 36px", borderBottom: "1px solid #EDEAE0", display: "flex",
          }}>
            {TABS.map((t) => (
              <button key={t} role="tab" aria-selected={tab === t} onClick={() => setTab(t)}
                style={{
                  padding: "14px 20px", fontFamily: FONT_DISPLAY,
                  fontSize: 16, fontWeight: tab === t ? 600 : 500,
                  color: tab === t ? "#0F0F0E" : "#8A8677",
                  borderBottom: tab === t ? "2px solid #0F0F0E" : "2px solid transparent",
                  marginBottom: -1, background: "transparent", cursor: "pointer", transition: "all 150ms",
                }}>
                {t}
              </button>
            ))}
          </div>

          {/* Content */}
          <div style={{ padding: "28px 36px 60px" }}>
            {(tab === "Overview" || tab === "Athletes") && (
              <AthletesTable athletes={athletes} setSlug={setSlug} setId={setId} />
            )}
            {tab === "Inserts" && (
              <div style={{ padding: "40px 20px", textAlign: "center", fontSize: 16, fontStyle: "italic", color: "#8A8677" }}>
                Inserts coming soon
              </div>
            )}
            {tab === "Autographs" && (
              <div style={{ padding: "40px 20px", textAlign: "center", fontSize: 16, fontStyle: "italic", color: "#8A8677" }}>
                Autographs coming soon
              </div>
            )}
            {tab === "Numbered Parallels" && (
              <div style={{ padding: "40px 20px", textAlign: "center", fontSize: 16, fontStyle: "italic", color: "#8A8677" }}>
                Numbered parallels coming soon
              </div>
            )}
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
              padding: "8px 12px", fontSize: 16, fontWeight: 500, color: "#0F0F0E",
            }}>
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6A2.25 2.25 0 0 1 6 3.75h2.25A2.25 2.25 0 0 1 10.5 6v2.25a2.25 2.25 0 0 1-2.25 2.25H6a2.25 2.25 0 0 1-2.25-2.25V6ZM3.75 15.75A2.25 2.25 0 0 1 6 13.5h2.25a2.25 2.25 0 0 1 2.25 2.25V18a2.25 2.25 0 0 1-2.25 2.25H6A2.25 2.25 0 0 1 3.75 18v-2.25ZM13.5 6a2.25 2.25 0 0 1 2.25-2.25H18A2.25 2.25 0 0 1 20.25 6v2.25A2.25 2.25 0 0 1 18 10.5h-2.25a2.25 2.25 0 0 1-2.25-2.25V6ZM13.5 15.75a2.25 2.25 0 0 1 2.25-2.25H18a2.25 2.25 0 0 1 2.25 2.25V18A2.25 2.25 0 0 1 18 20.25h-2.25a2.25 2.25 0 0 1-2.25-2.25v-2.25Z" />
            </svg>
            Teams
          </button>
          <Link href={`/sets/${setSlug || setId}`} style={{ fontSize: 16, color: "#6B6757", textDecoration: "none", fontFamily: FONT_DISPLAY }}>
            {setName} &rsaquo;
          </Link>
        </div>

        {/* Hero */}
        <div style={{ background: "#FFFFFF", padding: "18px 16px 14px", borderBottom: "1px solid #EDEAE0" }}>
          <div className="flex items-start gap-4">
            <TeamCrest name={teamName} size={72} />
            <div className="flex-1 min-w-0">
              <div style={{ fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 2, color: "#8A8677", textTransform: "uppercase" }}>
                {league ?? sport}
              </div>
              <h1 style={{
                fontFamily: FONT_DISPLAY, fontSize: 22, fontWeight: 600,
                letterSpacing: -0.6, lineHeight: 1.05, color: "#0F0F0E", margin: "4px 0 8px",
              }}>{teamName}</h1>
              <div className="flex flex-wrap items-center gap-1.5">
                <span style={{ fontSize: 16, fontWeight: 500, padding: "3px 7px", borderRadius: 4, border: "1px solid #E6E3D9", color: "#3A372F" }}>
                  {sport}
                </span>
                {league && (
                  <span style={{ fontSize: 16, fontWeight: 500, padding: "3px 7px", borderRadius: 4, border: "1px solid #E6E3D9", color: "#3A372F" }}>
                    {league}
                  </span>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Stat grid (mobile) */}
        <div className="grid" style={{
          gridTemplateColumns: "repeat(4, 1fr)", borderBottom: "1px solid #EDEAE0", background: "#FFFFFF",
        }}>
          {statItems.map((item, i) => (
            <div key={item.label} style={{
              padding: "12px 10px", borderRight: i < statItems.length - 1 ? "1px solid #EDEAE0" : "none",
            }}>
              <div style={{ fontFamily: FONT_MONO, fontSize: 8, fontWeight: 600, letterSpacing: 1.2, color: "#8A8677", textTransform: "uppercase" }}>
                {item.label}
              </div>
              <div style={{ fontFamily: FONT_DISPLAY, fontSize: 18, fontWeight: 600, letterSpacing: -0.5, color: "#0F0F0E", marginTop: 4 }}>
                {item.value.toLocaleString()}
              </div>
            </div>
          ))}
        </div>

        {/* Sticky tabs */}
        <div role="tablist" className="sticky z-[5] overflow-x-auto no-scrollbar"
          style={{
            top: 53, background: "#FAFAF7", padding: "0 16px",
            borderBottom: "1px solid #EDEAE0", display: "flex", whiteSpace: "nowrap",
          }}>
          {TABS.map((t) => (
            <button key={t} role="tab" aria-selected={tab === t} onClick={() => setTab(t)}
              style={{
                padding: "12px 12px", flexShrink: 0, fontFamily: FONT_DISPLAY,
                fontSize: 16, fontWeight: tab === t ? 600 : 500,
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
          {(tab === "Overview" || tab === "Athletes") && (
            <AthletesTable athletes={athletes} setSlug={setSlug} setId={setId} />
          )}
          {tab === "Inserts" && (
            <div style={{ padding: "40px 20px", textAlign: "center", fontSize: 16, fontStyle: "italic", color: "#8A8677" }}>
              Inserts coming soon
            </div>
          )}
          {tab === "Autographs" && (
            <div style={{ padding: "40px 20px", textAlign: "center", fontSize: 16, fontStyle: "italic", color: "#8A8677" }}>
              Autographs coming soon
            </div>
          )}
          {tab === "Numbered Parallels" && (
            <div style={{ padding: "40px 20px", textAlign: "center", fontSize: 16, fontStyle: "italic", color: "#8A8677" }}>
              Numbered parallels coming soon
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
