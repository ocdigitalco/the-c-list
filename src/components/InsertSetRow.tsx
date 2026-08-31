"use client";

import { useState, Fragment } from "react";
import Link from "next/link";

interface Parallel {
  id: number;
  name: string;
  printRun: number | null;
}

interface Appearance {
  cardNumber: string;
  team: string | null;
  isRookie: boolean;
  subsetTag: string | null;
  coPlayers?: { id: number; name: string }[];
}

interface Props {
  insertSetName: string;
  appearances: Appearance[];
  parallels: Parallel[];
  isTeamCard?: boolean;
  // Set classification for the first-appearance badge label. Optional; when
  // absent the badge reads "Rookie" exactly as before. "Debut" is used only
  // for unambiguously non-athlete Entertainment sets — never for sports/mixed.
  subjectRole?: string;
  isEntertainment?: boolean;
}

function parallelClasses(printRun: number | null): string {
  if (printRun === null)
    return "text-[var(--brand-ink-soft)] bg-[var(--brand-track)] border border-[var(--brand-line)]";
  const abs = Math.abs(printRun);
  if (abs === 1)
    return "text-amber-400 bg-amber-400/10 border border-amber-400/20";
  if (abs <= 10)
    return "text-red-300 bg-red-950/60 border border-red-800/50";
  return "text-sky-300 bg-sky-950/60 border border-sky-800/50";
}

function PrintRun({ printRun }: { printRun: number | null }) {
  if (printRun === null) return <span className="opacity-40">&#8734;</span>;
  if (printRun === 1) return <span className="font-mono opacity-75">1/1</span>;
  if (printRun < 0)
    return <span className="font-mono opacity-75">-{Math.abs(printRun)}</span>;
  return <span className="font-mono opacity-75">/{printRun}</span>;
}

export function InsertSetRow({ insertSetName, appearances, parallels, isTeamCard = false, subjectRole, isEntertainment = false }: Props) {
  const [expanded, setExpanded] = useState(false);
  const hasRookie = !isTeamCard && appearances.some((a) => a.isRookie);
  // Label only, not show/hide: "Debut" for non-athlete Entertainment sets;
  // "Rookie" everywhere else (default). Guarantees sports/mixed sets are unaffected.
  const firstAppearanceLabel = isEntertainment && subjectRole !== "athlete" ? "Debut" : "Rookie";

  return (
    <div className="rounded-xl border border-[var(--brand-line)] bg-[var(--brand-card)] overflow-hidden">
      {/* Collapsed header row */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center justify-between px-5 py-4 hover:bg-[var(--brand-track)] transition-colors text-left group"
      >
        <div className="flex items-center gap-2.5 min-w-0">
          <span className="font-semibold text-[var(--brand-ink)] truncate">{insertSetName}</span>
          {hasRookie && (
            <span className="shrink-0 text-xs font-bold text-amber-400 bg-amber-400/10 border border-amber-400/20 px-1.5 py-0.5 rounded">
              {firstAppearanceLabel}
            </span>
          )}
          <span className="shrink-0 text-xs text-[var(--brand-slate)]">
            {parallels.length > 0
              ? `${parallels.length} parallel${parallels.length !== 1 ? "s" : ""}`
              : "base only"}
          </span>
        </div>
        <svg
          className={`shrink-0 ml-4 w-4 h-4 text-[var(--brand-slate)] transition-transform ${expanded ? "rotate-180" : ""}`}
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth={2}
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {/* Expanded content */}
      {expanded && (
        <div className="px-5 pb-5 border-t border-[var(--brand-line)] space-y-4">
          {/* Card appearances */}
          <div className="pt-4 space-y-2">
            {appearances.map((a, i) => (
              <div key={i} className="space-y-1">
                <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-sm">
                  <span className="font-mono text-[var(--brand-slate)] text-xs">#{a.cardNumber}</span>
                  {!isTeamCard && (
                    a.subsetTag ? (
                      <span className="text-xs text-[var(--brand-slate)] bg-[var(--brand-track)] px-2 py-0.5 rounded">
                        {a.subsetTag}
                      </span>
                    ) : (
                      <span className="text-[var(--brand-ink-soft)]">{a.team}</span>
                    )
                  )}
                  {!isTeamCard && a.isRookie && (
                    <span className="text-xs font-bold text-amber-400 bg-amber-400/10 border border-amber-400/20 px-1.5 py-0.5 rounded">
                      {firstAppearanceLabel}
                    </span>
                  )}
                </div>
                {a.coPlayers && a.coPlayers.length > 0 && (
                  <div className="flex flex-wrap items-center gap-1 text-xs text-[var(--brand-slate)] ml-0.5">
                    <span>↳</span>
                    {a.coPlayers.map((cp, j) => (
                      <Fragment key={cp.id}>
                        {j > 0 && <span className="text-[var(--brand-fog)]">,</span>}
                        <Link
                          href={`?player=${cp.id}`}
                          className="text-[var(--brand-ink-soft)] hover:text-[var(--brand-ink)] transition-colors"
                        >
                          {cp.name}
                        </Link>
                      </Fragment>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Parallels */}
          {parallels.length > 0 && (
            <div>
              <p className="text-xs font-semibold text-[var(--brand-slate)] uppercase tracking-wider mb-2.5">
                Parallels
              </p>
              <div className="flex flex-wrap gap-2">
                {parallels.map((p) => (
                  <div
                    key={p.id}
                    className={`flex items-center gap-1.5 rounded-md px-2.5 py-1.5 text-xs font-medium ${parallelClasses(p.printRun)}`}
                  >
                    <span>{p.name}</span>
                    <PrintRun printRun={p.printRun} />
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
