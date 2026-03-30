"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useState, useMemo, Suspense } from "react";
import { Footer } from "@/components/Footer";
import type { CoverageRow } from "./page";

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

function formatReleaseDate(iso: string): string {
  const d = new Date(iso + "T00:00:00Z");
  return d.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    timeZone: "UTC",
  });
}

function StatusPill({ ok, label, tooltip }: { ok: boolean; label: string; tooltip?: string }) {
  return (
    <span
      className={`flex items-center gap-1 text-xs font-medium tabular-nums ${
        ok ? "text-emerald-400" : "text-zinc-600"
      }`}
      title={tooltip}
    >
      {ok ? (
        <svg className="w-3.5 h-3.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
        </svg>
      ) : (
        <svg className="w-3.5 h-3.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
        </svg>
      )}
      {label}
    </span>
  );
}

type Manufacturer = "All" | "Topps" | "Panini";
type Sport = string;

const MANUFACTURERS: Manufacturer[] = ["All", "Topps", "Panini"];
const SPORTS: Sport[] = [
  "All",
  "Basketball",
  "Baseball",
  "Soccer",
  "MMA",
  "Wrestling",
  "Racing",
  "Football",
  "Entertainment",
  "Olympics",
  "Other",
];

// ---------------------------------------------------------------------------
// Inner component that reads searchParams
// ---------------------------------------------------------------------------

function SetsCoverageInner({ rows }: { rows: CoverageRow[] }) {
  const searchParams = useSearchParams();
  const initialMfr = (searchParams.get("manufacturer") as Manufacturer) || "All";

  const [manufacturer, setManufacturer] = useState<Manufacturer>(
    MANUFACTURERS.includes(initialMfr) ? initialMfr : "All"
  );
  const [sport, setSport] = useState<Sport>("All");

  const filtered = useMemo(() => {
    return rows.filter((r) => {
      if (manufacturer !== "All" && r.manufacturer !== manufacturer) return false;
      if (sport !== "All" && r.sport !== sport) return false;
      return true;
    });
  }, [rows, manufacturer, sport]);

  // Group by year (descending), then sport within each year
  const { years, byYear, matchedCount } = useMemo(() => {
    const yrs = Array.from(new Set(filtered.map((r) => r.year))).sort((a, b) => b - a);
    const by = new Map<number, { sportOrder: string[]; bySport: Map<string, CoverageRow[]> }>();
    for (const y of yrs) by.set(y, { sportOrder: [], bySport: new Map() });

    for (const row of filtered) {
      const yd = by.get(row.year)!;
      if (!yd.bySport.has(row.sport)) {
        yd.sportOrder.push(row.sport);
        yd.bySport.set(row.sport, []);
      }
      yd.bySport.get(row.sport)!.push(row);
    }

    return { years: yrs, byYear: by, matchedCount: filtered.filter((r) => r.matchedSetId !== null).length };
  }, [filtered]);

  const newestYear = years[0];

  // Collect sports actually present for filter display
  const availableSports = useMemo(() => {
    const s = new Set(rows.map((r) => r.sport));
    return SPORTS.filter((sp) => sp === "All" || s.has(sp));
  }, [rows]);

  return (
    <div className="h-full overflow-y-auto">
      <div className="max-w-[1000px] mx-auto px-6 py-10 space-y-6">
        {/* Header */}
        <div>
          <Link
            href="/checklists"
            className="inline-flex items-center gap-1 text-xs text-zinc-500 hover:text-zinc-300 transition-colors mb-4"
          >
            <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
            </svg>
            Home
          </Link>
          <h1 className="text-2xl font-bold text-white tracking-tight">Sets Coverage</h1>
          <p className="text-sm text-zinc-500 mt-1">
            <span className="font-semibold text-zinc-300">{matchedCount}</span> of{" "}
            <span className="font-semibold text-zinc-300">{filtered.length}</span> sets tracked in the app
          </p>
        </div>

        {/* Filters */}
        <div className="space-y-3">
          {/* Manufacturer filter */}
          <div className="flex items-center gap-3 flex-wrap">
            <span className="text-xs font-medium text-zinc-500 uppercase tracking-wider w-24 shrink-0">Manufacturer</span>
            <div className="flex gap-1 flex-wrap">
              {MANUFACTURERS.map((mfr) => {
                const isActive = manufacturer === mfr;
                const isVisible = isActive || manufacturer === "All";
                if (mfr === "Topps") {
                  return (
                    <button
                      key={mfr}
                      onClick={() => setManufacturer(mfr)}
                      className={`px-2 py-0.5 rounded-md text-xs font-bold transition-all border ${
                        isVisible ? "opacity-100" : "opacity-50 hover:opacity-75"
                      }`}
                      style={{ color: "#CC0000", background: "#FFFFFF", borderColor: isActive ? "#CC0000" : "#e5c6c6" }}
                    >
                      Topps
                    </button>
                  );
                }
                if (mfr === "Panini") {
                  return (
                    <button
                      key={mfr}
                      onClick={() => setManufacturer(mfr)}
                      className={`px-2 py-0.5 rounded-md text-xs font-bold transition-all border ${
                        isVisible ? "opacity-100" : "opacity-50 hover:opacity-75"
                      }`}
                      style={{ color: "#CC0000", background: "#FFDD00", borderColor: isActive ? "#CC0000" : "#e6c700" }}
                    >
                      Panini
                    </button>
                  );
                }
                return (
                  <button
                    key={mfr}
                    onClick={() => setManufacturer(mfr)}
                    className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                      isActive
                        ? "bg-zinc-700 text-white"
                        : "text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800/60"
                    }`}
                  >
                    {mfr}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Sport filter */}
          <div className="flex items-center gap-3 flex-wrap">
            <span className="text-xs font-medium text-zinc-500 uppercase tracking-wider w-24 shrink-0">Sport</span>
            <div className="flex gap-1 flex-wrap">
              {availableSports.map((sp) => (
                <button
                  key={sp}
                  onClick={() => setSport(sp)}
                  className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                    sport === sp
                      ? "bg-zinc-700 text-white"
                      : "text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800/60"
                  }`}
                >
                  {sp}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Year sections */}
        {years.map((year) => {
          const { sportOrder, bySport } = byYear.get(year)!;
          const yearRows = sportOrder.flatMap((s) => bySport.get(s)!);
          const yearMatched = yearRows.filter((r) => r.matchedSetId !== null).length;
          const isNewest = year === newestYear;

          return (
            <details key={year} open={isNewest} className="group">
              <summary className="flex items-center justify-between cursor-pointer list-none select-none py-2 border-b border-zinc-800">
                <div className="flex items-center gap-3">
                  <svg
                    className="w-4 h-4 text-zinc-500 transition-transform group-open:rotate-90"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth={2.5}
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
                  </svg>
                  <span className="text-base font-bold text-white">{year}</span>
                </div>
                <span className="text-xs text-zinc-500 tabular-nums">
                  <span className="text-zinc-400 font-medium">{yearMatched}</span>
                  {" / "}
                  {yearRows.length}
                </span>
              </summary>

              <div className="mt-4 space-y-6 pb-2">
                {sportOrder.map((sp) => {
                  const sportRows = bySport.get(sp)!;
                  return (
                    <section key={sp}>
                      <h2 className="text-xs font-semibold text-zinc-500 uppercase tracking-widest mb-3">
                        {sp}
                      </h2>
                      <div className="rounded-xl border border-zinc-800 bg-zinc-900 overflow-hidden divide-y divide-zinc-800">
                        {sportRows.map((row, i) => {
                          const inApp = row.matchedSetId !== null;
                          const mfrBadge = row.manufacturer === "Topps" ? (
                            <span
                              className="shrink-0 text-[10px] font-bold px-1.5 py-0.5 rounded border"
                              style={{ color: "#CC0000", background: "#FFFFFF", borderColor: "#CC0000" }}
                            >
                              Topps
                            </span>
                          ) : row.manufacturer === "Panini" ? (
                            <span
                              className="shrink-0 text-[10px] font-bold px-1.5 py-0.5 rounded border"
                              style={{ color: "#CC0000", background: "#FFDD00", borderColor: "#e6c700" }}
                            >
                              Panini
                            </span>
                          ) : (
                            <span className="shrink-0 text-[10px] font-semibold uppercase tracking-wider px-1.5 py-0.5 rounded text-zinc-500 bg-zinc-800/50">
                              {row.manufacturer}
                            </span>
                          );
                          const hasRelease = inApp && !!row.releaseDate;
                          const indicators = (
                            <div className="shrink-0 ml-4 flex items-center gap-4">
                              <StatusPill ok={inApp} label="Checklist" />
                              <span
                                className={`flex items-center gap-1 text-xs font-medium tabular-nums ${
                                  hasRelease ? "text-emerald-400" : "text-zinc-600"
                                }`}
                              >
                                {hasRelease ? (
                                  <svg className="w-3.5 h-3.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                                  </svg>
                                ) : (
                                  <svg className="w-3.5 h-3.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                                  </svg>
                                )}
                                {hasRelease ? formatReleaseDate(row.releaseDate!) : "Release Date"}
                              </span>
                              <StatusPill ok={inApp && row.hasParallels} label="Parallels" tooltip="Parallels identify the numbered print runs for each card in a set. They are used by the Break Hit Calculator to determine odds of pulling specific cards." />
                              <StatusPill ok={inApp && row.hasBoxConfig} label="Box Config" />
                              <StatusPill ok={inApp && row.hasPackOdds} label="Pack Odds" />
                            </div>
                          );
                          return inApp ? (
                            <Link
                              key={i}
                              href={`/sets/${row.matchedSetId}`}
                              className="flex items-center justify-between px-5 py-3.5 hover:bg-zinc-800/50 transition-colors group/row"
                            >
                              <div className="flex items-center gap-2.5 min-w-0">
                                {mfrBadge}
                                <span className="text-sm text-white group-hover/row:text-amber-400 transition-colors truncate">
                                  {row.name}
                                </span>
                              </div>
                              {indicators}
                            </Link>
                          ) : (
                            <div key={i} className="flex items-center justify-between px-5 py-3.5">
                              <div className="flex items-center gap-2.5 min-w-0">
                                {mfrBadge}
                                <span className="text-sm text-zinc-500 truncate">{row.name}</span>
                              </div>
                              {indicators}
                            </div>
                          );
                        })}
                      </div>
                    </section>
                  );
                })}
              </div>
            </details>
          );
        })}

        {filtered.length === 0 && (
          <div className="text-center py-12">
            <p className="text-sm text-zinc-500">No sets match the current filters.</p>
          </div>
        )}
      </div>
      <Footer />
    </div>
  );
}

// ---------------------------------------------------------------------------
// Wrapper with Suspense for useSearchParams
// ---------------------------------------------------------------------------

export function SetsCoverageClient({ rows }: { rows: CoverageRow[] }) {
  return (
    <Suspense fallback={null}>
      <SetsCoverageInner rows={rows} />
    </Suspense>
  );
}
