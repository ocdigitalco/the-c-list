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

function isSuperfractor(key: string): boolean {
  return key.toLowerCase().includes("superfractor");
}

function OddsTableSection({
  title,
  rows,
  packsPerBox,
  accent,
}: {
  title: string;
  rows: OddsRow[];
  packsPerBox: number;
  accent?: boolean;
}) {
  if (rows.length === 0) return null;
  return (
    <div>
      <h3 className="text-xs font-semibold uppercase tracking-widest mb-2" style={{ color: accent ? "#d97706" : undefined }}>
        {!accent && <span className="text-zinc-400">{title}</span>}
        {accent && title}
      </h3>
      <div className="rounded-xl border overflow-hidden" style={{ borderColor: accent ? "#d9770633" : undefined }}>
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
                Per Box ({packsPerBox} packs)
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-800/60">
            {rows.map((row) => (
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
}

function OddsTable({ rows, packsPerBox }: { rows: OddsRow[]; packsPerBox: number }) {
  const regularRows = rows.filter((r) => !isSuperfractor(r.key));
  const superfractorRows = rows.filter((r) => isSuperfractor(r.key)).sort((a, b) => a.denom - b.denom);

  const grouped = CATEGORY_ORDER.reduce(
    (acc, cat) => {
      acc[cat] = regularRows.filter((r) => r.category === cat).sort((a, b) => a.denom - b.denom);
      return acc;
    },
    {} as Record<OddsCategory, OddsRow[]>
  );

  return (
    <div className="space-y-6">
      {CATEGORY_ORDER.map((cat) => (
        <OddsTableSection key={cat} title={cat} rows={grouped[cat]} packsPerBox={packsPerBox} />
      ))}
      {superfractorRows.length > 0 && (
        <OddsTableSection
          title="Superfractors (1/1)"
          rows={superfractorRows}
          packsPerBox={packsPerBox}
          accent
        />
      )}
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
