"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useState, useMemo, Suspense } from "react";
import type { CoverageRow } from "./page";

// ─── Helpers ──────────────────────────────────────────────────────────────────

function formatDate(iso: string): string {
  const d = new Date(iso + "T00:00:00Z");
  return d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric", timeZone: "UTC" });
}

function formatDateShort(iso: string): string {
  const d = new Date(iso + "T00:00:00Z");
  return d.toLocaleDateString("en-US", { month: "short", day: "numeric", timeZone: "UTC" });
}

function isComplete(r: CoverageRow): boolean {
  return r.hasChecklist && r.hasPackOdds && r.hasBoxConfig && r.hasParallels && !!r.releaseDate;
}

function missingCount(r: CoverageRow): number {
  return [r.hasChecklist, !!r.releaseDate, r.hasParallels, r.hasBoxConfig, r.hasPackOdds].filter((x) => !x).length;
}

// ─── Coverage mark ────────────────────────────────────────────────────────────

function CoverageMark({ ok, label }: { ok: boolean; label: string }) {
  return (
    <span className="inline-flex items-center gap-[5px] whitespace-nowrap" style={{ fontSize: 13, color: ok ? "#0E8A4F" : "#B7B2A3" }}>
      <span style={{ fontWeight: 600, lineHeight: 1 }}>{ok ? "✓" : "✗"}</span>
      {label}
    </span>
  );
}

// ─── Coverage dot (mobile) ────────────────────────────────────────────────────

function CoverageDot({ ok, letter }: { ok: boolean; letter: string }) {
  return (
    <span
      style={{
        width: 16, height: 16, borderRadius: 4, display: "inline-flex", alignItems: "center", justifyContent: "center",
        fontFamily: "var(--cl-font-mono)", fontSize: 8, fontWeight: 700,
        background: ok ? "rgba(14,138,79,0.12)" : "rgba(183,178,163,0.18)",
        color: ok ? "#0E8A4F" : "#B7B2A3",
      }}
    >
      {letter}
    </span>
  );
}

// ─── Manufacturer pill ────────────────────────────────────────────────────────

function MfrPill({ mfr, compact }: { mfr: string; compact?: boolean }) {
  const p = compact ? "2px 7px" : "4px 10px";
  const fs = compact ? 10 : 11;
  const r = compact ? 3 : 4;
  if (mfr === "Topps") return <span style={{ display: "inline-flex", minWidth: compact ? undefined : 56, padding: p, fontSize: fs, fontWeight: 600, letterSpacing: "0.2px", borderRadius: r, color: "#E11D48", background: "transparent", border: "1px solid #E11D48" }}>Topps</span>;
  if (mfr === "Panini") return <span style={{ display: "inline-flex", minWidth: compact ? undefined : 56, padding: p, fontSize: fs, fontWeight: 600, letterSpacing: "0.2px", borderRadius: r, color: "#1A1916", background: "#F2C230", border: "1px solid #E0B41E" }}>Panini</span>;
  return <span style={{ display: "inline-flex", minWidth: compact ? undefined : 56, padding: p, fontSize: fs, fontWeight: 600, letterSpacing: "0.2px", borderRadius: r, color: "#8A8677", background: "#F1EFE9", border: "1px solid #EDEAE0" }}>{mfr}</span>;
}

// ─── Constants ────────────────────────────────────────────────────────────────

type Manufacturer = "All" | "Topps" | "Panini";
const MANUFACTURERS: Manufacturer[] = ["All", "Topps", "Panini"];
const SPORTS = ["All", "Basketball", "Baseball", "Soccer", "MMA", "Wrestling", "Racing", "Football", "Entertainment", "Other"];

// ─── Inner component ──────────────────────────────────────────────────────────

function SetsCoverageInner({ rows }: { rows: CoverageRow[] }) {
  const searchParams = useSearchParams();
  const initialMfr = (searchParams.get("manufacturer") as Manufacturer) || "All";

  const [manufacturer, setManufacturer] = useState<Manufacturer>(MANUFACTURERS.includes(initialMfr) ? initialMfr : "All");
  const [sport, setSport] = useState("All");
  const [showIncomplete, setShowIncomplete] = useState(false);
  const [openYears, setOpenYears] = useState<Set<number>>(new Set());
  const [initialized, setInitialized] = useState(false);

  const filtered = useMemo(() => {
    return rows.filter((r) => {
      if (manufacturer !== "All" && r.manufacturer !== manufacturer) return false;
      if (sport !== "All" && r.sport !== sport) return false;
      if (showIncomplete && isComplete(r)) return false;
      return true;
    });
  }, [rows, manufacturer, sport, showIncomplete]);

  const { years, byYear } = useMemo(() => {
    const yrs = Array.from(new Set(filtered.map((r) => r.year))).sort((a, b) => b - a);
    const by = new Map<number, { sportOrder: string[]; bySport: Map<string, CoverageRow[]> }>();
    for (const y of yrs) by.set(y, { sportOrder: [], bySport: new Map() });
    for (const row of filtered) {
      const yd = by.get(row.year)!;
      if (!yd.bySport.has(row.sport)) { yd.sportOrder.push(row.sport); yd.bySport.set(row.sport, []); }
      yd.bySport.get(row.sport)!.push(row);
    }
    for (const yd of by.values()) {
      for (const sportRows of yd.bySport.values()) {
        sportRows.sort((a, b) => {
          if (a.releaseDate && b.releaseDate) return b.releaseDate.localeCompare(a.releaseDate);
          if (a.releaseDate) return -1;
          if (b.releaseDate) return 1;
          return a.name.localeCompare(b.name);
        });
      }
    }
    return { years: yrs, byYear: by };
  }, [filtered]);

  // Auto-open newest year on first render
  if (!initialized && years.length > 0) {
    setOpenYears(new Set([years[0]]));
    setInitialized(true);
  }

  const toggleYear = (y: number) => {
    setOpenYears((prev) => {
      const next = new Set(prev);
      if (next.has(y)) next.delete(y); else next.add(y);
      return next;
    });
  };

  const totalComplete = filtered.filter(isComplete).length;
  const availableSports = useMemo(() => {
    const s = new Set(rows.map((r) => r.sport));
    return SPORTS.filter((sp) => sp === "All" || s.has(sp));
  }, [rows]);

  return (
    <div className="h-full overflow-y-auto" style={{ background: "#FAFAF7" }}>
      <div className="mx-auto cl-container" style={{ maxWidth: 1440, padding: "40px 56px 80px" }}>
        {/* Breadcrumb */}
        <a href="/" style={{ fontSize: 13, color: "#6B6757", textDecoration: "none", fontFamily: "var(--cl-font-display)" }}>&lsaquo; Home</a>

        {/* Title */}
        <h1 className="cl-title" style={{ fontFamily: "var(--cl-font-display)", fontSize: 48, fontWeight: 600, letterSpacing: "-1.2px", color: "#0F0F0E", margin: "12px 0 0", lineHeight: 1.1 }}>
          Sets Coverage
        </h1>
        <p style={{ fontSize: 14, color: "#6B6757", margin: "6px 0 0" }}>
          <span style={{ color: "#0F0F0E", fontWeight: 600 }}>{totalComplete}</span> of{" "}
          <span style={{ color: "#0F0F0E", fontWeight: 600 }}>{filtered.length}</span> sets tracked in the app
        </p>

        {/* Required Coverage legend */}
        <div style={{ marginTop: 24, background: "#FFFFFF", border: "1px solid #EDEAE0", borderRadius: 10, padding: "14px 18px", display: "flex", flexWrap: "wrap", alignItems: "center", gap: 24 }}>
          <span style={{ fontFamily: "var(--cl-font-mono)", fontSize: 10, fontWeight: 600, letterSpacing: 2, color: "#3A372F" }}>REQUIRED COVERAGE</span>
          {["Checklist", "Release Date", "Parallels", "Box Config", "Pack Odds"].map((label) => (
            <span key={label} className="inline-flex items-center gap-[6px]" style={{ fontSize: 13, color: "#3A372F" }}>
              <span style={{ width: 6, height: 6, borderRadius: "50%", background: "#0E8A4F", display: "inline-block" }} />
              {label}
            </span>
          ))}
          <span style={{ flex: 1 }} />
          <button
            onClick={() => setShowIncomplete(!showIncomplete)}
            style={{
              padding: "6px 12px", borderRadius: 999, fontSize: 12, fontWeight: 500, cursor: "pointer",
              background: showIncomplete ? "#0F0F0E" : "transparent",
              color: showIncomplete ? "#FAFAF7" : "#3A372F",
              border: showIncomplete ? "1px solid #0F0F0E" : "1px solid #D9D5C7",
            }}
          >
            {showIncomplete ? "✓ " : ""}Show only incomplete
          </button>
        </div>

        {/* Manufacturer filter */}
        <div className="flex items-center gap-3 overflow-x-auto no-scrollbar" style={{ marginTop: 14 }}>
          <span style={{ fontFamily: "var(--cl-font-mono)", fontSize: 10, fontWeight: 500, letterSpacing: 2, color: "#8A8677", width: 110, flexShrink: 0 }}>MANUFACTURER</span>
          {MANUFACTURERS.map((mfr) => {
            const active = manufacturer === mfr;
            let style: React.CSSProperties = { padding: "6px 12px", borderRadius: 999, fontSize: 13, fontWeight: active ? 500 : 400, cursor: "pointer", border: "1px solid transparent", background: "transparent", transition: "all 0.15s" };
            if (mfr === "All") {
              style = { ...style, ...(active ? { background: "#0F0F0E", color: "#FAFAF7", borderColor: "#0F0F0E" } : { color: "#3A372F" }) };
            } else if (mfr === "Topps") {
              style = { ...style, color: "#E11D48", ...(active ? { borderColor: "#E11D48" } : {}) };
            } else {
              style = { ...style, ...(active ? { background: "#F2C230", color: "#1A1916", borderColor: "#E0B41E" } : { color: "#B47A0F" }) };
            }
            return <button key={mfr} onClick={() => setManufacturer(mfr)} style={style}>{mfr}</button>;
          })}
        </div>

        {/* Sport filter */}
        <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar" style={{ marginTop: 18 }}>
          {availableSports.map((sp) => {
            const active = sport === sp;
            return (
              <button
                key={sp}
                onClick={() => setSport(sp)}
                style={{
                  padding: active ? "8px 16px" : "8px 14px", borderRadius: 999, fontSize: 13, fontWeight: active ? 500 : 400,
                  color: active ? "#FAFAF7" : "#3A372F", background: active ? "#0F0F0E" : "transparent",
                  border: active ? "1px solid #0F0F0E" : "1px solid transparent", cursor: "pointer", transition: "all 0.15s", flexShrink: 0,
                }}
                onMouseEnter={(e) => { if (!active) (e.currentTarget as HTMLElement).style.background = "#F1EFE9"; }}
                onMouseLeave={(e) => { if (!active) (e.currentTarget as HTMLElement).style.background = "transparent"; }}
              >
                {sp}
              </button>
            );
          })}
        </div>

        {/* Year sections */}
        {years.map((year) => {
          const { sportOrder, bySport } = byYear.get(year)!;
          const yearRows = sportOrder.flatMap((s) => bySport.get(s)!);
          const yearComplete = yearRows.filter(isComplete).length;
          const isOpen = openYears.has(year);

          return (
            <div key={year} style={{ marginTop: 32 }}>
              <button
                onClick={() => toggleYear(year)}
                style={{ display: "flex", alignItems: "center", justifyContent: "space-between", width: "100%", padding: "10px 0", borderBottom: "1px solid #EDEAE0", background: "none", border: "none", borderBottomStyle: "solid", borderBottomWidth: 1, borderBottomColor: "#EDEAE0", cursor: "pointer" }}
              >
                <div className="flex items-center gap-2">
                  <svg width={12} height={12} viewBox="0 0 24 24" fill="none" stroke="#3A372F" strokeWidth={1.6} style={{ transition: "transform 0.15s ease", transform: isOpen ? "rotate(0deg)" : "rotate(-90deg)" }}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
                  </svg>
                  <span style={{ fontFamily: "var(--cl-font-display)", fontSize: 22, fontWeight: 600, letterSpacing: "-0.5px", color: "#0F0F0E" }}>{year}</span>
                </div>
                <span style={{ fontFamily: "var(--cl-font-mono)", fontSize: 11, color: "#8A8677" }}>
                  <span style={{ fontWeight: 600 }}>{yearComplete}</span> / {yearRows.length} complete
                </span>
              </button>

              {isOpen && (
                <div style={{ marginTop: 22 }} className="space-y-[22px]">
                  {sportOrder.map((sp) => {
                    const sportRows = bySport.get(sp)!;
                    return (
                      <div key={sp}>
                        <div style={{ fontFamily: "var(--cl-font-mono)", fontSize: 10, fontWeight: 600, letterSpacing: 2, color: "#3A372F", padding: "0 4px 10px" }}>
                          {sp.toUpperCase()}
                        </div>
                        <div style={{ background: "#FFFFFF", border: "1px solid #EDEAE0", borderRadius: 10, overflow: "hidden" }}>
                          {sportRows.map((row, i) => {
                            const hasRelease = !!row.releaseDate;
                            const content = (
                              <>
                                {/* Desktop layout */}
                                <div className="hidden md:grid" style={{ gridTemplateColumns: "92px 1fr auto", gap: 18, alignItems: "center" }}>
                                  <MfrPill mfr={row.manufacturer} />
                                  <span style={{ fontFamily: "var(--cl-font-display)", fontSize: 14, fontWeight: 500, letterSpacing: "-0.1px", color: "#0F0F0E", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                                    {row.name}
                                  </span>
                                  <div className="flex items-center gap-[22px]">
                                    <CoverageMark ok={row.hasChecklist} label="Checklist" />
                                    <CoverageMark ok={hasRelease} label={hasRelease ? formatDate(row.releaseDate!) : "No date"} />
                                    <CoverageMark ok={row.hasParallels} label="Parallels" />
                                    <CoverageMark ok={row.hasBoxConfig} label="Box Config" />
                                    <CoverageMark ok={row.hasPackOdds} label="Pack Odds" />
                                  </div>
                                </div>

                                {/* Mobile layout */}
                                <div className="md:hidden">
                                  <div className="flex items-center gap-2" style={{ marginBottom: 6 }}>
                                    <MfrPill mfr={row.manufacturer} compact />
                                    <span style={{ fontFamily: "var(--cl-font-mono)", fontSize: 9, color: "#8A8677", letterSpacing: 0.6 }}>
                                      {hasRelease ? formatDateShort(row.releaseDate!) : "NO DATE"}
                                    </span>
                                    <span style={{ flex: 1 }} />
                                    <span style={{
                                      fontFamily: "var(--cl-font-mono)", fontSize: 9, fontWeight: 600, letterSpacing: 0.6,
                                      color: isComplete(row) ? "#0E8A4F" : "#C2410C",
                                    }}>
                                      {isComplete(row) ? "READY" : `${missingCount(row)} MISSING`}
                                    </span>
                                  </div>
                                  <p style={{ fontFamily: "var(--cl-font-display)", fontSize: 14, fontWeight: 600, letterSpacing: "-0.2px", color: "#0F0F0E", lineHeight: 1.25, marginBottom: 8 }}>
                                    {row.name}
                                  </p>
                                  <div className="flex gap-[3px]">
                                    <CoverageDot ok={row.hasChecklist} letter="C" />
                                    <CoverageDot ok={hasRelease} letter="D" />
                                    <CoverageDot ok={row.hasParallels} letter="P" />
                                    <CoverageDot ok={row.hasBoxConfig} letter="B" />
                                    <CoverageDot ok={row.hasPackOdds} letter="O" />
                                  </div>
                                </div>
                              </>
                            );

                            const linkHref = row.matchedSetSlug ? `/sets/${row.matchedSetSlug}` : row.matchedSetId ? `/sets/${row.matchedSetId}` : null;
                            const rowStyle: React.CSSProperties = {
                              padding: "14px 18px",
                              background: "#FFFFFF",
                              borderTop: i > 0 ? "1px solid #F1EEE3" : undefined,
                              textDecoration: "none",
                              display: "block",
                              transition: "background 0.15s",
                            };

                            return linkHref ? (
                              <Link
                                key={i}
                                href={linkHref}
                                style={rowStyle}
                                onMouseEnter={(e) => { (e.currentTarget as HTMLElement).style.background = "#FDFCF8"; }}
                                onMouseLeave={(e) => { (e.currentTarget as HTMLElement).style.background = "#FFFFFF"; }}
                              >
                                {content}
                              </Link>
                            ) : (
                              <div key={i} style={rowStyle}>{content}</div>
                            );
                          })}
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          );
        })}

        {/* Empty state */}
        {filtered.length === 0 && (
          <div style={{ marginTop: 40, border: "1px dashed #D9D5C7", borderRadius: 12, padding: "80px 20px", textAlign: "center" }}>
            <p style={{ fontSize: 14, fontWeight: 500, color: "#3A372F" }}>No sets match these filters.</p>
            <p style={{ fontSize: 12, color: "#8A8677", marginTop: 8 }}>Try clearing filters or toggling &ldquo;Show only incomplete&rdquo;.</p>
          </div>
        )}
      </div>
    </div>
  );
}

// ─── Wrapper ──────────────────────────────────────────────────────────────────

export function SetsCoverageClient({ rows }: { rows: CoverageRow[] }) {
  return (
    <Suspense fallback={null}>
      <SetsCoverageInner rows={rows} />
    </Suspense>
  );
}
