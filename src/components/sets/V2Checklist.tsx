"use client";

import { useState, Fragment } from "react";
import Link from "next/link";
import type { InsertSetDetail } from "./types";

interface Props {
  setId: number;
  setSlug?: string | null;
  insertSets: InsertSetDetail[];
}

function parallelClasses(printRun: number | null): string {
  if (printRun === null)
    return "text-zinc-400 bg-zinc-800 border border-zinc-700";
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
  return <span className="font-mono opacity-75">/{printRun}</span>;
}

function AccordionRow({ setId, setSlug, is }: { setId: number; setSlug?: string | null; is: InsertSetDetail }) {
  const [expanded, setExpanded] = useState(false);
  const hasRookie = is.appearances.some((a) => a.isRookie);

  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900 overflow-hidden">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center justify-between px-5 py-4 hover:bg-zinc-800/50 transition-colors text-left"
      >
        <div className="flex items-center gap-2.5 min-w-0">
          <span className="font-semibold text-white truncate">{is.insertSetName}</span>
          {hasRookie && (
            <span className="shrink-0 text-xs font-bold text-amber-400 bg-amber-400/10 border border-amber-400/20 px-1.5 py-0.5 rounded">
              Rookie
            </span>
          )}
          <span className="shrink-0 text-xs text-zinc-600">
            {is.appearances.length} card{is.appearances.length !== 1 ? "s" : ""}
          </span>
          {is.parallels.length > 0 && (
            <span className="shrink-0 text-xs text-zinc-600">
              · {is.parallels.length} parallel{is.parallels.length !== 1 ? "s" : ""}
            </span>
          )}
        </div>
        <svg
          className={`shrink-0 ml-4 w-4 h-4 text-zinc-500 transition-transform ${expanded ? "rotate-180" : ""}`}
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth={2}
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {expanded && (
        <div className="px-5 pb-5 border-t border-zinc-800 space-y-4">
          <div className="pt-4 space-y-2">
            {is.appearances.map((a, i) => (
              <div key={i} className="space-y-1">
                <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-sm">
                  <span className="font-mono text-zinc-500 text-xs">#{a.cardNumber}</span>
                  <Link
                    href={`/sets/${setSlug || setId}/athlete/${0}`}
                    className="text-zinc-300 hover:text-indigo-400 transition-colors"
                  >
                    {a.team}
                  </Link>
                  {a.isRookie && (
                    <span className="text-xs font-bold text-amber-400 bg-amber-400/10 border border-amber-400/20 px-1.5 py-0.5 rounded">
                      Rookie
                    </span>
                  )}
                  {a.subsetTag && (
                    <span className="text-xs text-zinc-500 bg-zinc-800 px-2 py-0.5 rounded">
                      {a.subsetTag}
                    </span>
                  )}
                </div>
                {a.coPlayers.length > 0 && (
                  <div className="flex flex-wrap items-center gap-1 text-xs text-zinc-600 ml-0.5">
                    <span>with</span>
                    {a.coPlayers.map((cp, j) => (
                      <Fragment key={cp.id}>
                        {j > 0 && <span className="text-zinc-700">,</span>}
                        <Link
                          href={`/sets/${setSlug || setId}/athlete/${cp.id}`}
                          className="text-zinc-400 hover:text-indigo-400 transition-colors"
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

          {is.parallels.length > 0 && (
            <div>
              <p className="text-xs font-semibold text-zinc-600 uppercase tracking-wider mb-2.5">
                Parallels
              </p>
              <div className="flex flex-wrap gap-2">
                {is.parallels.map((p) => (
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

export function V2Checklist({ setId, setSlug, insertSets }: Props) {
  return (
    <div className="space-y-3">
      {insertSets.map((is) => (
        <AccordionRow key={is.insertSetId} setId={setId} setSlug={setSlug} is={is} />
      ))}
      {insertSets.length === 0 && (
        <p className="text-base text-center py-8" style={{ color: "var(--v2-text-secondary)" }}>
          No insert sets found
        </p>
      )}
    </div>
  );
}
