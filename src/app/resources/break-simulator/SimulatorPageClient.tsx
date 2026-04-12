"use client";

import { useState } from "react";
import { useSearchParams } from "next/navigation";
import { Suspense } from "react";
import { BreakSimulator } from "@/components/simulator/BreakSimulator";

interface SetOption {
  id: number;
  name: string;
  sport: string;
  season: string;
  boxTypes: string[];
}

function SimulatorInner({ sets }: { sets: SetOption[] }) {
  const searchParams = useSearchParams();
  const paramSetId = searchParams.get("setId");
  const paramBoxType = searchParams.get("boxType");

  const defaultSet = paramSetId
    ? sets.find((s) => s.id === Number(paramSetId))
    : sets[0];

  const [selectedSetId, setSelectedSetId] = useState(defaultSet?.id ?? sets[0]?.id);
  const selectedSet = sets.find((s) => s.id === selectedSetId);

  if (sets.length === 0) {
    return (
      <p className="text-sm text-zinc-500 text-center py-12">
        No sets with pack odds and box config are available for simulation.
      </p>
    );
  }

  return (
    <div className="space-y-6">
      {/* Set selector */}
      <div>
        <label className="text-xs font-semibold text-zinc-400 uppercase tracking-widest mb-2 block">
          Select a set
        </label>
        <select
          value={selectedSetId}
          onChange={(e) => setSelectedSetId(Number(e.target.value))}
          className="w-full rounded-lg border border-zinc-700 bg-zinc-900 text-sm text-zinc-200 px-3 py-2 focus:outline-none focus:border-zinc-500"
        >
          {sets.map((s) => (
            <option key={s.id} value={s.id}>
              {s.name} ({s.season})
            </option>
          ))}
        </select>
      </div>

      {selectedSet && (
        <BreakSimulator
          key={selectedSet.id}
          setId={selectedSet.id}
          setName={selectedSet.name}
          boxTypes={selectedSet.boxTypes}
          initialBoxType={paramBoxType ?? undefined}
        />
      )}
    </div>
  );
}

export function SimulatorPageClient({ sets }: { sets: SetOption[] }) {
  return (
    <Suspense fallback={null}>
      <SimulatorInner sets={sets} />
    </Suspense>
  );
}
