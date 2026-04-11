"use client";

import { useState } from "react";

const FORMAT_LABELS: Record<string, string> = {
  hobby: "Hobby",
  fdi: "FDI",
  mega: "Mega",
  value: "Value",
  breakers: "Breaker's Delight",
  sapphire: "Sapphire",
  logofractor: "Logofractor",
};

export function ParallelGrid({
  parallels,
}: {
  parallels: Array<{
    name: string;
    printRun: string;
    boxType: string;
    odds: string;
    color: string;
    formats: string[];
  }>;
}) {
  const [filter, setFilter] = useState("all");

  const allFormats = Array.from(
    new Set(parallels.flatMap((p) => p.formats))
  ).sort();

  const filtered =
    filter === "all"
      ? parallels
      : parallels.filter((p) => p.formats.includes(filter));

  return (
    <div className="mb-6">
      <div className="flex flex-wrap gap-1.5 mb-4">
        <button
          onClick={() => setFilter("all")}
          className={`text-xs font-medium px-3 py-1 rounded-full border transition-colors ${
            filter === "all"
              ? "bg-zinc-200 text-zinc-900 border-zinc-300"
              : "bg-zinc-800 text-zinc-400 border-zinc-700 hover:border-zinc-600"
          }`}
        >
          All
        </button>
        {allFormats.map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`text-xs font-medium px-3 py-1 rounded-full border transition-colors ${
              filter === f
                ? "bg-zinc-200 text-zinc-900 border-zinc-300"
                : "bg-zinc-800 text-zinc-400 border-zinc-700 hover:border-zinc-600"
            }`}
          >
            {FORMAT_LABELS[f] ?? f}
          </button>
        ))}
      </div>
      <div className="grid grid-cols-[repeat(auto-fill,minmax(140px,1fr))] gap-2">
        {filtered.map((p) => (
          <div
            key={p.name}
            className="rounded-lg border border-zinc-800 bg-zinc-900 overflow-hidden"
          >
            <div className="h-1" style={{ backgroundColor: p.color }} />
            <div className="px-3 py-2.5">
              <p className="text-sm font-semibold text-zinc-200 leading-tight">
                {p.name}
              </p>
              <p className="text-xs text-zinc-500 mt-1">{p.printRun}</p>
              <p className="text-xs text-zinc-600 mt-0.5">{p.odds}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
