"use client";

import { useState } from "react";
import { denomToDisplay } from "@/lib/parseOdds";

type OddsCategory = "Autographs" | "Base Parallels" | "Inserts";

interface OddsRow {
  key: string;
  denom: number;
  category: OddsCategory;
}

interface OddsFormat {
  label: string;
  rows: OddsRow[];
  packsPerBox: number;
}

const CATEGORY_ORDER: OddsCategory[] = ["Base Parallels", "Inserts", "Autographs"];

function OddsTable({ rows, packsPerBox }: { rows: OddsRow[]; packsPerBox: number }) {
  const grouped = CATEGORY_ORDER.reduce(
    (acc, cat) => {
      acc[cat] = rows
        .filter((r) => r.category === cat)
        .sort((a, b) => a.denom - b.denom);
      return acc;
    },
    {} as Record<OddsCategory, OddsRow[]>
  );

  const perBoxLabel = `Per Box (${packsPerBox} packs)`;

  return (
    <div className="space-y-6">
      {CATEGORY_ORDER.map((cat) => {
        const catRows = grouped[cat];
        if (catRows.length === 0) return null;
        return (
          <div key={cat}>
            <h3 className="text-xs font-semibold text-zinc-400 uppercase tracking-widest mb-2">
              {cat}
            </h3>
            <div className="rounded-xl border border-zinc-800 overflow-hidden">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-zinc-800 bg-zinc-900/60">
                    <th className="text-left text-xs font-semibold text-zinc-600 uppercase tracking-wider px-4 py-2.5">
                      Parallel / Insert
                    </th>
                    <th className="text-right text-xs font-semibold text-zinc-600 uppercase tracking-wider px-4 py-2.5">
                      Pack Odds
                    </th>
                    <th className="text-right text-xs font-semibold text-zinc-600 uppercase tracking-wider px-4 py-2.5 hidden sm:table-cell">
                      {perBoxLabel}
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-800/60">
                  {catRows.map((row) => (
                    <tr key={row.key} className="bg-zinc-900 hover:bg-zinc-800/40 transition-colors">
                      <td className="px-4 py-2.5 text-sm text-zinc-300">{row.key}</td>
                      <td className="px-4 py-2.5 text-sm font-mono tabular-nums text-zinc-400 text-right">
                        {denomToDisplay(row.denom)}
                      </td>
                      <td className="px-4 py-2.5 text-xs text-zinc-600 text-right tabular-nums hidden sm:table-cell">
                        {(packsPerBox / row.denom) >= 1
                          ? `~${(packsPerBox / row.denom).toFixed(1)}×`
                          : `1 in ~${(row.denom / packsPerBox).toFixed(1)} boxes`}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        );
      })}
    </div>
  );
}

export function OddsTabView({ formats }: { formats: OddsFormat[] }) {
  const [activeIdx, setActiveIdx] = useState(0);
  const active = formats[activeIdx];

  return (
    <div className="space-y-4">
      <div className="flex gap-1 rounded-lg bg-zinc-800/60 p-0.5 w-fit max-w-full overflow-x-auto">
        {formats.map((f, i) => (
          <button
            key={f.label}
            onClick={() => setActiveIdx(i)}
            className={`px-4 text-xs py-1.5 rounded-md font-semibold transition-colors ${
              i === activeIdx
                ? "bg-zinc-700 text-white"
                : "text-zinc-500 hover:text-zinc-300"
            }`}
          >
            {f.label}
          </button>
        ))}
      </div>
      <OddsTable rows={active.rows} packsPerBox={active.packsPerBox} />
    </div>
  );
}
