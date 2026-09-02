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
    <span className="inline-flex items-center gap-[5px] whitespace-nowrap" style={{ fontSize: 13, color: ok ? "var(--brand-ok)" : "var(--brand-fog)" }}>
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
        background: ok
          ? "color-mix(in srgb, var(--brand-ok) 12%, transparent)"
          : "color-mix(in srgb, var(--brand-fog) 24%, transparent)",
        color: ok ? "var(--brand-ok)" : "var(--brand-fog)",
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
  const r = compact ? 4 : 5;
  // All manufacturers use the theme's inverted brand tag (.tag.k): ink fill, --head text, 5px radius.
  return <span style={{ display: "inline-flex", justifyContent: "center", minWidth: compact ? undefined : 56, padding: p, fontSize: fs, fontWeight: 600, letterSpacing: "0.2px", borderRadius: r, color: "var(--brand-head)", background: "var(--brand-ink)" }}>{mfr}</span>;
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
          // Mirror the SQL index sort: COALESCE(release_date, created_at) DESC,
          // name ASC. Both fields are ISO text, so codepoint comparison gives
          // calendar order; undated sets fall back to created_at.
          const ka = a.releaseDate ?? a.createdAt;
          const kb = b.releaseDate ?? b.createdAt;
          if (!ka && !kb) return a.name.localeCompare(b.name);
          if (!ka) return 1;
          if (!kb) return -1;
          if (ka < kb) return 1;
          if (ka > kb) return -1;
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
    <div className="flex-1" style={{ background: "var(--brand-page)" }}>
      <div className="page-container" style={{ paddingTop: 40, paddingBottom: 80 }}>
        {/* Breadcrumb */}
        <a href="/" style={{ fontSize: 13, color: "var(--brand-slate)", textDecoration: "none", fontFamily: "var(--cl-font-display)" }}>&lsaquo; Home</a>

        {/* Title */}
        <h1 className="page-title" style={{ margin: "12px 0 0" }}>
          Sets Coverage
        </h1>
        <p style={{ fontSize: 14, color: "var(--brand-slate)", margin: "6px 0 0" }}>
          <span style={{ color: "var(--brand-ink)", fontWeight: 600 }}>{totalComplete}</span> of{" "}
          <span style={{ color: "var(--brand-ink)", fontWeight: 600 }}>{filtered.length}</span> sets tracked in the app
        </p>

        {/* Required Coverage legend */}
        <div style={{ marginTop: 24, background: "var(--brand-card)", border: "1px solid var(--brand-line)", borderRadius: 10, padding: "14px 18px", display: "flex", flexWrap: "wrap", alignItems: "center", gap: 24 }}>
          <span style={{ fontFamily: "var(--cl-font-mono)", fontSize: 10, fontWeight: 600, letterSpacing: 2, color: "var(--brand-ink-soft)" }}>REQUIRED COVERAGE</span>
          {["Checklist", "Release Date", "Parallels", "Box Config", "Pack Odds"].map((label) => (
            <span key={label} className="inline-flex items-center gap-[6px]" style={{ fontSize: 13, color: "var(--brand-ink-soft)" }}>
              <span style={{ width: 6, height: 6, borderRadius: "50%", background: "var(--brand-ok)", display: "inline-block" }} />
              {label}
            </span>
          ))}
          <span style={{ flex: 1 }} />
          <button
            onClick={() => setShowIncomplete(!showIncomplete)}
            style={{
              padding: "6px 12px", borderRadius: 999, fontSize: 12, fontWeight: 500, cursor: "pointer",
              background: showIncomplete ? "var(--brand-ink)" : "transparent",
              color: showIncomplete ? "var(--brand-page)" : "var(--brand-ink-soft)",
              border: showIncomplete ? "1px solid var(--brand-ink)" : "1px solid var(--brand-line)",
            }}
          >
            {showIncomplete ? "✓ " : ""}Show only incomplete
          </button>
        </div>

        {/* Manufacturer filter */}
        <div className="flex items-center gap-3 overflow-x-auto no-scrollbar" style={{ marginTop: 14 }}>
          <span style={{ fontFamily: "var(--cl-font-mono)", fontSize: 10, fontWeight: 500, letterSpacing: 2, color: "var(--brand-slate)", width: 110, flexShrink: 0 }}>MANUFACTURER</span>
          {MANUFACTURERS.map((mfr) => {
            const active = manufacturer === mfr;
            // Uniform theme pill for every manufacturer — no per-manufacturer colors.
            const style: React.CSSProperties = {
              padding: "6px 12px", borderRadius: 999, fontSize: 13, fontWeight: active ? 500 : 400,
              cursor: "pointer", transition: "all 0.15s",
              border: active ? "1px solid var(--brand-ink)" : "1px solid var(--brand-line)",
              background: active ? "var(--brand-ink)" : "transparent",
              color: active ? "var(--brand-head)" : "var(--brand-ink-soft)",
            };
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
                  color: active ? "var(--brand-page)" : "var(--brand-ink-soft)", background: active ? "var(--brand-ink)" : "transparent",
                  border: active ? "1px solid var(--brand-ink)" : "1px solid transparent", cursor: "pointer", transition: "all 0.15s", flexShrink: 0,
                }}
                onMouseEnter={(e) => { if (!active) (e.currentTarget as HTMLElement).style.background = "var(--brand-track)"; }}
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
                style={{ display: "flex", alignItems: "center", justifyContent: "space-between", width: "100%", padding: "10px 0", borderBottom: "1px solid var(--brand-line)", background: "none", border: "none", borderBottomStyle: "solid", borderBottomWidth: 1, borderBottomColor: "var(--brand-line)", cursor: "pointer" }}
              >
                <div className="flex items-center gap-2">
                  <svg width={12} height={12} viewBox="0 0 24 24" fill="none" stroke="var(--brand-ink-soft)" strokeWidth={1.6} style={{ transition: "transform 0.15s ease", transform: isOpen ? "rotate(0deg)" : "rotate(-90deg)" }}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
                  </svg>
                  <span style={{ fontFamily: "var(--cl-font-display)", fontSize: 22, fontWeight: 600, letterSpacing: "-0.5px", color: "var(--brand-ink)" }}>{year}</span>
                </div>
                <span style={{ fontFamily: "var(--cl-font-mono)", fontSize: 11, color: "var(--brand-slate)" }}>
                  <span style={{ fontWeight: 600 }}>{yearComplete}</span> / {yearRows.length} complete
                </span>
              </button>

              {isOpen && (
                <div style={{ marginTop: 22 }} className="space-y-[22px]">
                  {sportOrder.map((sp) => {
                    const sportRows = bySport.get(sp)!;
                    return (
                      <div key={sp}>
                        <div style={{ fontFamily: "var(--cl-font-mono)", fontSize: 10, fontWeight: 600, letterSpacing: 2, color: "var(--brand-ink-soft)", padding: "0 4px 10px" }}>
                          {sp.toUpperCase()}
                        </div>
                        <div style={{ background: "var(--brand-card)", border: "1px solid var(--brand-line)", borderRadius: 10, overflow: "hidden" }}>
                          {sportRows.map((row, i) => {
                            const hasRelease = !!row.releaseDate;
                            const content = (
                              <>
                                {/* Desktop layout */}
                                <div className="hidden md:grid" style={{ gridTemplateColumns: "92px 1fr auto", gap: 18, alignItems: "center" }}>
                                  <MfrPill mfr={row.manufacturer} />
                                  <span style={{ fontFamily: "var(--cl-font-display)", fontSize: 14, fontWeight: 500, letterSpacing: "-0.1px", color: "var(--brand-ink)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
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
                                    <span style={{ fontFamily: "var(--cl-font-mono)", fontSize: 9, color: "var(--brand-slate)", letterSpacing: 0.6 }}>
                                      {hasRelease ? formatDateShort(row.releaseDate!) : "NO DATE"}
                                    </span>
                                    <span style={{ flex: 1 }} />
                                    <span style={{
                                      fontFamily: "var(--cl-font-mono)", fontSize: 9, fontWeight: 600, letterSpacing: 0.6,
                                      color: isComplete(row) ? "var(--brand-ok)" : "var(--brand-accent-deep)",
                                    }}>
                                      {isComplete(row) ? "READY" : `${missingCount(row)} MISSING`}
                                    </span>
                                  </div>
                                  <p style={{ fontFamily: "var(--cl-font-display)", fontSize: 14, fontWeight: 600, letterSpacing: "-0.2px", color: "var(--brand-ink)", lineHeight: 1.25, marginBottom: 8 }}>
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
                              background: "var(--brand-card)",
                              borderTop: i > 0 ? "1px solid var(--brand-track)" : undefined,
                              textDecoration: "none",
                              display: "block",
                              transition: "background 0.15s",
                            };

                            return linkHref ? (
                              <Link
                                key={i}
                                href={linkHref}
                                style={rowStyle}
                                onMouseEnter={(e) => { (e.currentTarget as HTMLElement).style.background = "var(--brand-sel)"; }}
                                onMouseLeave={(e) => { (e.currentTarget as HTMLElement).style.background = "var(--brand-card)"; }}
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
          <div style={{ marginTop: 40, border: "1px dashed var(--brand-line)", borderRadius: 12, padding: "80px 20px", textAlign: "center" }}>
            <p style={{ fontSize: 14, fontWeight: 500, color: "var(--brand-ink-soft)" }}>No sets match these filters.</p>
            <p style={{ fontSize: 12, color: "var(--brand-slate)", marginTop: 8 }}>Try clearing filters or toggling &ldquo;Show only incomplete&rdquo;.</p>
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
