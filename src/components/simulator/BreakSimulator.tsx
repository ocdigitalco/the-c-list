"use client";

import { useState, useCallback } from "react";
import type { SimConfig, SimulationResult, BreakTrial, PackPull } from "@/lib/breakSimulatorClient";
import { runSimulation } from "@/lib/breakSimulatorClient";

// ─── Sub-components ──────────────────────────────────────────────────────────

function SummaryCard({
  label,
  trial,
  accent,
}: {
  label: string;
  trial: BreakTrial;
  accent: string;
}) {
  return (
    <div className="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
      <p className="text-[11px] font-bold uppercase tracking-widest mb-3" style={{ color: accent }}>
        {label}
      </p>
      <div className="space-y-1.5">
        <div className="flex justify-between text-sm">
          <span className="text-zinc-400">Autos</span>
          <span className="text-white font-semibold tabular-nums">{trial.autoCount}</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-zinc-400">Numbered</span>
          <span className="text-white font-semibold tabular-nums">{trial.numberedCount}</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-zinc-400">Total cards</span>
          <span className="text-zinc-500 tabular-nums">{trial.totalCards}</span>
        </div>
      </div>
    </div>
  );
}

function DistBar({ label, pct }: { label: string; pct: number }) {
  return (
    <div className="flex items-center gap-3 py-1">
      <span className="text-xs text-zinc-400 w-24 shrink-0 text-right tabular-nums">{label}</span>
      <div className="flex-1 h-3 bg-zinc-800 rounded-full overflow-hidden">
        <div
          className="h-full bg-amber-500/60 rounded-full transition-all duration-300"
          style={{ width: `${Math.max(pct * 100, 0.5)}%` }}
        />
      </div>
      <span className="text-xs text-zinc-500 w-12 shrink-0 tabular-nums">
        {(pct * 100).toFixed(1)}%
      </span>
    </div>
  );
}

function PullRow({ pull }: { pull: PackPull }) {
  const tag = pull.isAuto
    ? "AUTO"
    : pull.isNumbered
      ? "NUMBERED"
      : "INSERT";
  const tagColor = pull.isAuto
    ? "text-amber-400"
    : pull.isNumbered
      ? "text-blue-400"
      : "text-zinc-500";
  return (
    <div className="flex items-center gap-3 py-1.5 border-b border-zinc-800/60 last:border-0">
      <span className="text-[10px] text-zinc-600 tabular-nums w-12 shrink-0">
        Pack {pull.packNumber}
      </span>
      <span className={`text-[10px] font-bold uppercase tracking-wide w-16 shrink-0 ${tagColor}`}>
        {tag}
      </span>
      <span className="text-sm text-zinc-300 truncate">
        {pull.athleteName}
      </span>
      <span className="text-xs text-zinc-600 truncate ml-auto">
        {pull.insertSetName}
        {pull.parallelName ? ` — ${pull.parallelName}` : ""}
      </span>
    </div>
  );
}

// ─── Main component ──────────────────────────────────────────────────────────

interface Props {
  setId: number;
  setName: string;
  boxTypes: string[];
  initialBoxType?: string;
  highlightAthleteName?: string;
}

const BOX_LABELS: Record<string, string> = {
  hobby: "Hobby", jumbo: "Jumbo", mega: "Mega", blaster: "Blaster",
  value: "Value", hanger: "Hanger", breakers_delight: "Breaker's Delight",
  first_day_issue: "First Day Issue", sapphire: "Sapphire",
  logofractor: "Logofractor", diamond_anniversary: "Diamond Anniversary",
};

const BOX_COUNTS = [1, 3, 6, 12];

export function BreakSimulator({
  setId,
  setName,
  boxTypes,
  initialBoxType,
  highlightAthleteName,
}: Props) {
  const [boxType, setBoxType] = useState(initialBoxType ?? boxTypes[0] ?? "hobby");
  const [boxCount, setBoxCount] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<SimulationResult | null>(null);
  const [simConfig, setSimConfig] = useState<SimConfig | null>(null);

  const runSim = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`/api/sim-pool?setId=${setId}&boxType=${boxType}`);
      if (!res.ok) {
        const data = await res.json();
        setError(data.error ?? "Simulation not available");
        setLoading(false);
        return;
      }
      const config: SimConfig = await res.json();
      setSimConfig(config);

      // Run simulation in chunks to keep UI responsive
      await new Promise((r) => setTimeout(r, 10));
      const simResult = runSimulation(config, boxCount, 10000);
      setResult(simResult);
    } catch {
      setError("Failed to run simulation");
    }
    setLoading(false);
  }, [setId, boxType, boxCount]);

  const reSimSingle = useCallback(() => {
    if (!simConfig) return;
    const trial = runSimulation(simConfig, boxCount, 1).singleRandomTrial;
    setResult((prev) => prev ? { ...prev, singleRandomTrial: trial } : prev);
  }, [simConfig, boxCount]);

  // Notable pulls for "Your Break" display
  const notablePulls = result?.singleRandomTrial.pulls.filter(
    (p) => p.isAuto || p.isNumbered
  ) ?? [];

  return (
    <div className="space-y-6">
      {/* Controls */}
      <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-4 space-y-4">
        <div>
          <p className="text-xs font-semibold text-zinc-400 uppercase tracking-widest mb-1">
            {setName}
          </p>
        </div>

        {/* Box type pills */}
        {boxTypes.length > 1 && (
          <div className="flex flex-wrap gap-1.5">
            {boxTypes.map((bt) => (
              <button
                key={bt}
                onClick={() => { setBoxType(bt); setResult(null); }}
                className={`text-xs font-medium px-3 py-1 rounded-full border transition-colors ${
                  boxType === bt
                    ? "bg-zinc-200 text-zinc-900 border-zinc-300"
                    : "bg-zinc-800 text-zinc-400 border-zinc-700 hover:border-zinc-600"
                }`}
              >
                {BOX_LABELS[bt] ?? bt}
              </button>
            ))}
          </div>
        )}

        {/* Box count + Run button */}
        <div className="flex items-center gap-3">
          <div className="flex gap-1">
            {BOX_COUNTS.map((n) => (
              <button
                key={n}
                onClick={() => { setBoxCount(n); setResult(null); }}
                className={`text-xs font-medium px-2.5 py-1 rounded border transition-colors ${
                  boxCount === n
                    ? "bg-zinc-200 text-zinc-900 border-zinc-300"
                    : "bg-zinc-800 text-zinc-400 border-zinc-700 hover:border-zinc-600"
                }`}
              >
                {n} {n === 1 ? "box" : "boxes"}
              </button>
            ))}
          </div>
          <button
            onClick={runSim}
            disabled={loading}
            className="ml-auto px-4 py-1.5 rounded-lg bg-amber-500 text-zinc-900 text-xs font-bold hover:bg-amber-400 disabled:opacity-50 transition-colors"
          >
            {loading ? "Simulating..." : "Run Simulation"}
          </button>
        </div>

        {loading && (
          <div className="h-1 bg-zinc-800 rounded-full overflow-hidden">
            <div className="h-full bg-amber-500/60 rounded-full animate-pulse" style={{ width: "60%" }} />
          </div>
        )}
      </div>

      {error && (
        <p className="text-sm text-red-400 text-center py-4">{error}</p>
      )}

      {result && (
        <>
          {/* Summary cards */}
          <div className="grid grid-cols-3 gap-3">
            <SummaryCard label="Typical Break" trial={result.medianTrial} accent="#A8A8A8" />
            <SummaryCard label="Great Break (top 10%)" trial={result.bestTrial} accent="#10B981" />
            <SummaryCard label="Rough Break (bottom 10%)" trial={result.worstTrial} accent="#EF4444" />
          </div>

          <p className="text-[11px] text-zinc-600 text-center">
            Based on {result.config.trials.toLocaleString()} simulated breaks
          </p>

          {/* Auto distribution */}
          <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-4">
            <p className="text-xs font-semibold text-zinc-400 uppercase tracking-widest mb-3">
              Auto Distribution
            </p>
            {Object.keys(result.distributions.autos).length === 0 ? (
              <p className="text-xs text-zinc-600">No autographs available in this format</p>
            ) : (
              Object.entries(result.distributions.autos)
                .sort(([a], [b]) => Number(a) - Number(b))
                .map(([count, pct]) => (
                  <DistBar key={count} label={`${count} auto${Number(count) !== 1 ? "s" : ""}`} pct={pct} />
                ))
            )}
          </div>

          {/* Numbered distribution */}
          <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-4">
            <p className="text-xs font-semibold text-zinc-400 uppercase tracking-widest mb-3">
              Numbered Parallel Distribution
            </p>
            {Object.entries(result.distributions.numbered)
              .sort(([a], [b]) => Number(a) - Number(b))
              .slice(0, 8)
              .map(([count, pct]) => (
                <DistBar key={count} label={`${count} numbered`} pct={pct} />
              ))}
          </div>

          {/* Top auto athletes */}
          {result.topAutoAthletes.length > 0 && (
            <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-4">
              <p className="text-xs font-semibold text-zinc-400 uppercase tracking-widest mb-3">
                Most Likely Autos
              </p>
              <div className="space-y-1.5">
                {result.topAutoAthletes.map((a, i) => {
                  const isHighlighted = highlightAthleteName && a.athleteName === highlightAthleteName;
                  return (
                    <div key={a.athleteName} className="flex items-center gap-3">
                      <span className="text-xs text-zinc-600 w-5 text-right tabular-nums shrink-0">
                        {i + 1}
                      </span>
                      <span className={`text-sm flex-1 truncate ${isHighlighted ? "text-amber-400 font-semibold" : "text-zinc-300"}`}>
                        {a.athleteName}
                      </span>
                      <div className="w-24 h-2 bg-zinc-800 rounded-full overflow-hidden shrink-0">
                        <div
                          className="h-full bg-amber-500/60 rounded-full"
                          style={{ width: `${Math.min(a.autoPercentage * 2, 100)}%` }}
                        />
                      </div>
                      <span className="text-xs text-zinc-500 tabular-nums w-12 text-right shrink-0">
                        {a.autoPercentage}%
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* Your Break */}
          <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-4">
            <div className="flex items-center justify-between mb-3">
              <p className="text-xs font-semibold text-zinc-400 uppercase tracking-widest">
                One Simulated Break
              </p>
              <button
                onClick={reSimSingle}
                className="text-[11px] text-zinc-500 hover:text-zinc-300 transition-colors"
              >
                Re-simulate &rarr;
              </button>
            </div>

            {highlightAthleteName && (
              <p className="text-xs text-zinc-500 mb-2">
                {notablePulls.some((p) => p.athleteName === highlightAthleteName)
                  ? `You pulled ${highlightAthleteName}!`
                  : `${highlightAthleteName} did not appear in this break.`}
              </p>
            )}

            {notablePulls.length > 0 ? (
              <div>
                {notablePulls.map((pull, i) => (
                  <PullRow key={i} pull={pull} />
                ))}
                {result.singleRandomTrial.totalCards - notablePulls.length > 0 && (
                  <p className="text-[11px] text-zinc-700 mt-2">
                    + {result.singleRandomTrial.totalCards - notablePulls.length} base/insert cards
                  </p>
                )}
              </div>
            ) : (
              <p className="text-xs text-zinc-600">No notable pulls in this break. All base cards.</p>
            )}
          </div>
        </>
      )}
    </div>
  );
}
