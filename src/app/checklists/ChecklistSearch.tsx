"use client";

import { useState, useMemo, useEffect, useRef } from "react";
import Link from "next/link";

// ─── Types ────────────────────────────────────────────────────────────────────

interface SetCard {
  id: number;
  name: string;
  slug: string | null;
  sport: string;
  league: string | null;
  tier: string;
  season: string;
  releaseDate: string | null;
  sampleImageUrl: string | null;
  athleteCount: number;
  cardCount: number;
  featured: boolean;
}

// ─── Design atoms ─────────────────────────────────────────────────────────────

function Chip({ label, tone = "default" }: { label: string; tone?: "default" | "dark" | "accent" }) {
  const styles: Record<string, React.CSSProperties> = {
    default: {
      background: "#F1EFE9",
      color: "#3A372F",
      border: "1px solid #E6E3D9",
    },
    dark: {
      background: "#151412",
      color: "#F6F3EA",
      border: "1px solid #151412",
    },
    accent: {
      background: "oklch(0.55 0.17 25)",
      color: "#FFF8F1",
      border: "1px solid oklch(0.5 0.17 25)",
    },
  };
  return (
    <span
      style={{
        ...styles[tone],
        padding: "3px 9px",
        borderRadius: 4,
        fontSize: 11,
        fontWeight: 500,
        letterSpacing: "0.2px",
        lineHeight: "1.4",
        whiteSpace: "nowrap",
      }}
    >
      {label}
    </span>
  );
}

function Ribbon({ size = "gallery" }: { size?: "gallery" | "compact" | "compact-mobile" }) {
  const s = size === "gallery"
    ? { top: 10, left: -4, padding: "4px 8px 4px 10px", fontSize: 9, letterSpacing: 1.5, clipOff: 4 }
    : size === "compact"
    ? { top: 6, left: -3, padding: "2px 5px 2px 6px", fontSize: 7, letterSpacing: 1, clipOff: 3 }
    : { top: 4, left: -2, padding: "2px 4px 2px 5px", fontSize: 7, letterSpacing: 0.8, clipOff: 2 };

  return (
    <div
      style={{
        position: "absolute",
        top: s.top,
        left: s.left,
        background: "oklch(0.55 0.17 25)",
        color: "#FFF8F1",
        fontFamily: "var(--cl-font-mono)",
        fontSize: s.fontSize,
        fontWeight: 700,
        letterSpacing: s.letterSpacing,
        padding: s.padding,
        clipPath: `polygon(0 0, 100% 0, 100% 100%, 0 100%, ${s.clipOff}px 50%)`,
        boxShadow: "0 2px 6px rgba(0,0,0,0.18)",
        zIndex: 2,
        lineHeight: "1.4",
      }}
    >
      RECENTLY ADDED
    </div>
  );
}

// ─── Constants ────────────────────────────────────────────────────────────────

const SPORT_ORDER = [
  "All", "Basketball", "Baseball", "Soccer", "MMA", "Wrestling",
  "Racing", "Football", "Entertainment", "Boxing", "Hockey", "Olympics",
];

// ─── Component ────────────────────────────────────────────────────────────────

export function ChecklistSearch({
  sets,
  allSports,
}: {
  sets: SetCard[];
  allSports: string[];
}) {
  const [query, setQuery] = useState("");
  const [activeSport, setActiveSport] = useState<string | null>(null);
  const [view, setView] = useState<"gallery" | "compact">("gallery");
  const inputRef = useRef<HTMLInputElement>(null);

  // Persist view to localStorage
  useEffect(() => {
    const saved = localStorage.getItem("cl_view");
    if (saved === "gallery" || saved === "compact") setView(saved);
  }, []);
  useEffect(() => {
    localStorage.setItem("cl_view", view);
  }, [view]);

  useEffect(() => {
    function onKeyDown(e: KeyboardEvent) {
      if (e.key === "Escape") {
        setQuery("");
        inputRef.current?.blur();
      }
    }
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, []);

  const orderedSports = useMemo(() => {
    const sportSet = new Set(allSports);
    const ordered: string[] = [];
    for (const s of SPORT_ORDER) {
      if (s === "All" || sportSet.has(s)) {
        ordered.push(s);
        sportSet.delete(s);
      }
    }
    for (const s of allSports) {
      if (sportSet.has(s)) ordered.push(s);
    }
    return ordered;
  }, [allSports]);

  const filtered = useMemo(() => {
    let results = sets;
    if (activeSport) {
      results = results.filter((s) => s.sport === activeSport);
    }
    if (query.trim()) {
      const q = query.toLowerCase();
      results = results.filter(
        (s) =>
          s.name?.toLowerCase().includes(q) ||
          s.sport?.toLowerCase().includes(q) ||
          s.league?.toLowerCase().includes(q) ||
          s.tier?.toLowerCase().includes(q) ||
          s.season?.toLowerCase().includes(q)
      );
    }
    return [...results].sort((a, b) => {
      if (!a.releaseDate && !b.releaseDate) return a.name.localeCompare(b.name);
      if (!a.releaseDate) return 1;
      if (!b.releaseDate) return -1;
      return new Date(b.releaseDate).getTime() - new Date(a.releaseDate).getTime();
    });
  }, [sets, query, activeSport]);

  const resultLabel = query.trim()
    ? `${filtered.length} SETS MATCHING "${query.toUpperCase()}"`
    : activeSport
    ? `${activeSport.toUpperCase()} SETS`
    : "ALL SETS";
  const countLabel = `${filtered.length} SET${filtered.length !== 1 ? "S" : ""}`;

  return (
    <>
      {/* ── Sport filter chips ── */}
      <div
        className="flex items-center gap-3 overflow-x-auto no-scrollbar"
        style={{ marginTop: 32 }}
      >
        <span
          className="hidden sm:block shrink-0"
          style={{
            fontFamily: "var(--cl-font-mono)",
            fontSize: 10,
            fontWeight: 600,
            letterSpacing: 2,
            color: "var(--cl-text-muted)",
          }}
        >
          SPORT
        </span>
        <div className="flex gap-1.5 shrink-0">
          {orderedSports.map((sport) => {
            const isAll = sport === "All";
            const isActive = isAll ? activeSport === null : activeSport === sport;
            return (
              <button
                key={sport}
                onClick={() => setActiveSport(isAll ? null : sport)}
                className="shrink-0 transition-all"
                style={{
                  padding: isActive ? "8px 16px" : "8px 14px",
                  borderRadius: 999,
                  fontSize: 13,
                  fontWeight: isActive ? 500 : 400,
                  color: isActive ? "#FAFAF7" : "#3A372F",
                  background: isActive ? "#0F0F0E" : "transparent",
                  border: isActive ? "1px solid #0F0F0E" : "1px solid transparent",
                  cursor: "pointer",
                  transitionDuration: "0.15s",
                }}
                onMouseEnter={(e) => {
                  if (!isActive) (e.currentTarget as HTMLElement).style.background = "#F1EFE9";
                }}
                onMouseLeave={(e) => {
                  if (!isActive) (e.currentTarget as HTMLElement).style.background = "transparent";
                }}
              >
                {sport}
              </button>
            );
          })}
        </div>
      </div>

      {/* ── Search + view toggle ── */}
      <div className="flex items-center gap-3" style={{ marginTop: 20 }}>
        <div className="relative flex-1">
          <svg
            className="absolute left-4 top-1/2 -translate-y-1/2 pointer-events-none"
            width={16} height={16} fill="none" viewBox="0 0 24 24"
            stroke="#A19D90" strokeWidth={2}
          >
            <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
          </svg>
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search by name, sport, league, or tier..."
            style={{
              width: "100%",
              height: 48,
              background: "#F1EFE9",
              borderRadius: 10,
              border: "none",
              paddingLeft: 44,
              paddingRight: 40,
              fontSize: 14,
              color: "#0F0F0E",
              outline: "none",
            }}
          />
          {query && (
            <button
              onClick={() => setQuery("")}
              className="absolute right-4 top-1/2 -translate-y-1/2"
              style={{ color: "#A19D90", cursor: "pointer", background: "none", border: "none" }}
              aria-label="Clear search"
            >
              <svg width={16} height={16} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          )}
        </div>

        {/* View toggle */}
        <div className="flex shrink-0" style={{ background: "#F1EFE9", borderRadius: 10, padding: 4 }}>
          <button
            onClick={() => setView("gallery")}
            style={{
              width: 40,
              height: 40,
              borderRadius: 8,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              background: view === "gallery" ? "#0F0F0E" : "transparent",
              color: view === "gallery" ? "#FAFAF7" : "#1A1916",
              border: "none",
              cursor: "pointer",
              transition: "all 0.15s",
            }}
            aria-label="Gallery view"
          >
            <svg width={18} height={18} viewBox="0 0 18 18" fill="currentColor">
              <rect x="0" y="0" width="8" height="8" rx="1.5" />
              <rect x="10" y="0" width="8" height="8" rx="1.5" />
              <rect x="0" y="10" width="8" height="8" rx="1.5" />
              <rect x="10" y="10" width="8" height="8" rx="1.5" />
            </svg>
          </button>
          <button
            onClick={() => setView("compact")}
            style={{
              width: 40,
              height: 40,
              borderRadius: 8,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              background: view === "compact" ? "#0F0F0E" : "transparent",
              color: view === "compact" ? "#FAFAF7" : "#1A1916",
              border: "none",
              cursor: "pointer",
              transition: "all 0.15s",
            }}
            aria-label="Compact view"
          >
            <svg width={18} height={18} viewBox="0 0 18 18" fill="currentColor">
              <rect x="0" y="1" width="18" height="4" rx="1" />
              <rect x="0" y="7" width="18" height="4" rx="1" />
              <rect x="0" y="13" width="18" height="4" rx="1" />
            </svg>
          </button>
        </div>
      </div>

      {/* ── Results header ── */}
      <div style={{ marginTop: 36 }}>
        <span
          style={{
            fontFamily: "var(--cl-font-mono)",
            fontSize: 10,
            fontWeight: 600,
            letterSpacing: 2,
            color: "var(--cl-text-primary)",
          }}
        >
          {query.trim() ? resultLabel : (activeSport ? `${activeSport.toUpperCase()} SETS` : "ALL SETS")}
        </span>
        {!query.trim() && (
          <span
            style={{
              fontFamily: "var(--cl-font-mono)",
              fontSize: 10,
              fontWeight: 600,
              letterSpacing: 2,
              color: "var(--cl-text-faint)",
              marginLeft: 8,
            }}
          >
            {countLabel}
          </span>
        )}
      </div>

      {/* ── Grid / List ── */}
      {filtered.length > 0 ? (
        <div style={{ marginTop: 18 }}>
          {view === "gallery" ? (
            <GalleryView sets={filtered} />
          ) : (
            <CompactView sets={filtered} />
          )}
        </div>
      ) : (
        <div style={{ textAlign: "center", padding: "64px 0", color: "var(--cl-text-tertiary)" }}>
          <p style={{ fontSize: 14, marginBottom: 12 }}>
            No checklists found{query ? ` for "${query}"` : activeSport ? ` for ${activeSport}` : ""}
          </p>
          <button
            onClick={() => { setQuery(""); setActiveSport(null); }}
            style={{
              fontSize: 13,
              fontWeight: 500,
              color: "oklch(0.55 0.17 25)",
              background: "none",
              border: "none",
              cursor: "pointer",
            }}
          >
            Clear filters
          </button>
        </div>
      )}
    </>
  );
}

// ─── Gallery View ─────────────────────────────────────────────────────────────

function GalleryView({ sets }: { sets: SetCard[] }) {
  return (
    <div className="cl-gallery-grid">
      {sets.map((s) => (
        <GalleryCard key={s.id} set={s} />
      ))}
    </div>
  );
}

function GalleryCard({ set: s }: { set: SetCard }) {
  return (
    <Link
      href={`/sets/${s.slug ?? s.id}`}
      className="group block"
      style={{ textDecoration: "none" }}
    >
      {/* Card image */}
      <div
        className="relative overflow-hidden"
        style={{
          aspectRatio: "2/2.8",
          background: "#EAE6D9",
          borderRadius: 0,
          boxShadow: "0 1px 2px rgba(15,15,14,0.06)",
          transition: "all 0.2s ease",
        }}
        onMouseEnter={(e) => {
          const el = e.currentTarget;
          el.style.boxShadow = "0 12px 28px rgba(15,15,14,0.16)";
          el.style.transform = "translateY(-2px)";
        }}
        onMouseLeave={(e) => {
          const el = e.currentTarget;
          el.style.boxShadow = "0 1px 2px rgba(15,15,14,0.06)";
          el.style.transform = "translateY(0)";
        }}
      >
        {s.sampleImageUrl ? (
          <img src={s.sampleImageUrl} alt={s.name} className="w-full h-full object-cover" />
        ) : (
          <div className="w-full h-full flex items-center justify-center" style={{ color: "#B7B2A3" }}>
            <svg width={32} height={32} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1}>
              <path strokeLinecap="round" strokeLinejoin="round" d="m2.25 15.75 5.159-5.159a2.25 2.25 0 0 1 3.182 0l5.159 5.159m-1.5-1.5 1.409-1.409a2.25 2.25 0 0 1 3.182 0l2.909 2.909M3.75 21h16.5A2.25 2.25 0 0 0 22.5 18.75V5.25A2.25 2.25 0 0 0 20.25 3H3.75A2.25 2.25 0 0 0 1.5 5.25v13.5A2.25 2.25 0 0 0 3.75 21Z" />
            </svg>
          </div>
        )}

        {s.featured && <Ribbon size="gallery" />}

        {/* Hover overlay */}
        <div
          className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity"
          style={{
            background: "linear-gradient(to top, rgba(0,0,0,0.5) 0%, rgba(0,0,0,0) 50%)",
            display: "flex",
            alignItems: "flex-end",
            padding: 12,
          }}
        >
          <span
            style={{
              fontFamily: "var(--cl-font-mono)",
              fontSize: 11,
              fontWeight: 600,
              color: "#fff",
              letterSpacing: 0.5,
            }}
          >
            OPEN CHECKLIST &rarr;
          </span>
        </div>
      </div>

      {/* Metadata */}
      <div style={{ paddingTop: 12 }}>
        <p
          style={{
            fontFamily: "var(--cl-font-display)",
            fontSize: 14,
            fontWeight: 600,
            letterSpacing: "-0.2px",
            color: "var(--cl-text-primary)",
            lineHeight: 1.3,
          }}
        >
          {s.name}
        </p>
        <div className="flex flex-wrap gap-[5px]" style={{ marginTop: 8 }}>
          <Chip label={s.league ?? s.sport} />
          {s.tier !== "Standard" && <Chip label={s.tier} tone="dark" />}
        </div>
        <div className="flex gap-[14px]" style={{ marginTop: 10 }}>
          <span style={{ fontFamily: "var(--cl-font-mono)", fontSize: 11, color: "var(--cl-text-primary)", fontWeight: 600 }}>
            {s.athleteCount.toLocaleString()}
            <span style={{ color: "var(--cl-text-faint)", fontWeight: 400 }}> athletes</span>
          </span>
          <span style={{ fontFamily: "var(--cl-font-mono)", fontSize: 11, color: "var(--cl-text-primary)", fontWeight: 600 }}>
            {s.cardCount.toLocaleString()}
            <span style={{ color: "var(--cl-text-faint)", fontWeight: 400 }}> cards</span>
          </span>
        </div>
      </div>
    </Link>
  );
}

// ─── Compact View ─────────────────────────────────────────────────────────────

function CompactView({ sets }: { sets: SetCard[] }) {
  return (
    <div className="flex flex-col gap-2">
      {sets.map((s) => (
        <CompactRow key={s.id} set={s} />
      ))}
    </div>
  );
}

function CompactRow({ set: s }: { set: SetCard }) {
  return (
    <Link
      href={`/sets/${s.slug ?? s.id}`}
      className="flex items-center gap-[18px] transition-all"
      style={{
        padding: "14px 16px",
        background: "#FFFFFF",
        border: "1px solid #EDEAE0",
        borderRadius: 10,
        textDecoration: "none",
        transitionDuration: "0.15s",
      }}
      onMouseEnter={(e) => {
        const el = e.currentTarget;
        el.style.background = "#FDFCF8";
        el.style.boxShadow = "0 4px 14px rgba(15,15,14,0.06)";
      }}
      onMouseLeave={(e) => {
        const el = e.currentTarget;
        el.style.background = "#FFFFFF";
        el.style.boxShadow = "none";
      }}
    >
      {/* Thumbnail */}
      <div
        className="relative shrink-0"
        style={{
          width: 80,
          height: 112,
          borderRadius: 0,
          overflow: "hidden",
          background: "#EAE6D9",
          boxShadow: "0 1px 2px rgba(15,15,14,0.08)",
        }}
      >
        {s.sampleImageUrl ? (
          <img src={s.sampleImageUrl} alt={s.name} className="w-full h-full object-cover" />
        ) : (
          <div className="w-full h-full flex items-center justify-center" style={{ color: "#B7B2A3" }}>
            <svg width={20} height={20} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="m2.25 15.75 5.159-5.159a2.25 2.25 0 0 1 3.182 0l5.159 5.159m-1.5-1.5 1.409-1.409a2.25 2.25 0 0 1 3.182 0l2.909 2.909M3.75 21h16.5A2.25 2.25 0 0 0 22.5 18.75V5.25A2.25 2.25 0 0 0 20.25 3H3.75A2.25 2.25 0 0 0 1.5 5.25v13.5A2.25 2.25 0 0 0 3.75 21Z" />
            </svg>
          </div>
        )}
        {s.featured && <Ribbon size="compact" />}
      </div>

      {/* Title + chips */}
      <div className="flex-1 min-w-0">
        <p
          style={{
            fontFamily: "var(--cl-font-display)",
            fontSize: 15,
            fontWeight: 600,
            letterSpacing: "-0.2px",
            color: "var(--cl-text-primary)",
            lineHeight: 1.3,
          }}
        >
          {s.name}
        </p>
        <div className="flex flex-wrap gap-[5px]" style={{ marginTop: 8 }}>
          <Chip label={s.league ?? s.sport} />
          {s.tier !== "Standard" && <Chip label={s.tier} tone="dark" />}
        </div>
      </div>

      {/* Stats */}
      <div className="hidden md:flex items-center gap-0">
        <div style={{ width: 110, textAlign: "right" }}>
          <p style={{ fontFamily: "var(--cl-font-mono)", fontSize: 12, fontWeight: 600, color: "var(--cl-text-primary)" }}>
            {s.athleteCount.toLocaleString()}
          </p>
          <p style={{ fontFamily: "var(--cl-font-mono)", fontSize: 10, fontWeight: 500, color: "var(--cl-text-faint)", letterSpacing: 1 }}>
            ATHLETES
          </p>
        </div>
        <div style={{ width: 110, textAlign: "right" }}>
          <p style={{ fontFamily: "var(--cl-font-mono)", fontSize: 12, fontWeight: 600, color: "var(--cl-text-primary)" }}>
            {s.cardCount.toLocaleString()}
          </p>
          <p style={{ fontFamily: "var(--cl-font-mono)", fontSize: 10, fontWeight: 500, color: "var(--cl-text-faint)", letterSpacing: 1 }}>
            CARDS
          </p>
        </div>
        <div style={{ width: 60, textAlign: "right" }}>
          <p style={{ fontFamily: "var(--cl-font-mono)", fontSize: 12, fontWeight: 600, color: "var(--cl-text-primary)" }}>
            {s.season}
          </p>
          <p style={{ fontFamily: "var(--cl-font-mono)", fontSize: 10, fontWeight: 500, color: "var(--cl-text-faint)", letterSpacing: 1 }}>
            YEAR
          </p>
        </div>
      </div>

      {/* Chevron */}
      <svg width={14} height={14} fill="none" viewBox="0 0 24 24" stroke="#B7B2A3" strokeWidth={2.5} className="shrink-0 hidden md:block">
        <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
      </svg>
    </Link>
  );
}
