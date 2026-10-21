// Server-rendered, dependency-free SVG bar chart for saved-break-sheet volume.
// No client JS: hover tooltips are native SVG <title> elements. Fixed height so
// nothing shifts on load. Bars scale to fill the full content width.

const MONO = "var(--cl-font-mono)";

export interface Bucket {
  key: string;      // stable id (YYYY-MM-DD / YYYY-MM-DDTHH / week-start)
  tick: string;     // short x-axis label when selected as a tick
  tooltip: string;  // native hover text: full date + count
  count: number;
}

export interface VolumeStat {
  label: string;
  value: string;
  sub?: string;
}

const PLOT_H = 160; // px

export function VolumeChart({
  buckets,
  caption,
  stats,
  tickCount = 7,
}: {
  buckets: Bucket[];
  caption: string;
  stats: VolumeStat[];
  tickCount?: number;
}) {
  const n = buckets.length;
  const max = Math.max(1, ...buckets.map((b) => b.count));

  // Evenly spaced tick indices (always include first + last).
  const tickIdx = new Set<number>();
  if (n > 0) {
    const steps = Math.min(tickCount, n);
    for (let i = 0; i < steps; i++) {
      tickIdx.add(Math.round((i * (n - 1)) / Math.max(1, steps - 1)));
    }
  }

  return (
    <div style={{ border: "1px solid var(--brand-line)", background: "var(--brand-card)", borderRadius: 10, overflow: "hidden" }}>
      {/* Stat strip */}
      <div
        className="grid"
        style={{
          gridTemplateColumns: `repeat(${stats.length}, 1fr)`,
          borderBottom: "1px solid var(--brand-line)",
          background: "var(--brand-card)",
        }}
      >
        {stats.map((s, i) => (
          <div
            key={s.label}
            style={{
              padding: "14px 18px",
              borderRight: i < stats.length - 1 ? "1px solid var(--brand-line)" : "none",
              minWidth: 0,
            }}
          >
            <div style={{ fontFamily: MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6, color: "var(--brand-slate)", textTransform: "uppercase" }}>
              {s.label}
            </div>
            <div style={{ fontFamily: "var(--brand-font-head)", fontSynthesisWeight: "none", fontSize: 24, fontWeight: 400, color: "var(--brand-ink)", marginTop: 4, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }} title={s.value}>
              {s.value}
            </div>
            {s.sub && (
              <div style={{ fontFamily: MONO, fontSize: 10, color: "var(--brand-slate)", marginTop: 3, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }} title={s.sub}>
                {s.sub}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Plot */}
      <div style={{ padding: "16px 18px 10px" }}>
        <div style={{ position: "relative", height: PLOT_H }}>
          {/* y-axis max label */}
          <div style={{ position: "absolute", top: -2, left: 0, fontFamily: MONO, fontSize: 10, color: "var(--brand-slate)" }}>
            {max.toLocaleString()}
          </div>
          <div style={{ position: "absolute", bottom: 14, left: 0, fontFamily: MONO, fontSize: 10, color: "var(--brand-fog)" }}>
            0
          </div>

          <svg
            width="100%"
            height={PLOT_H}
            viewBox={`0 0 ${Math.max(1, n)} 100`}
            preserveAspectRatio="none"
            style={{ display: "block", overflow: "visible" }}
            role="img"
            aria-label="Saved break sheets per bucket"
          >
            {/* gridlines */}
            {[0, 25, 50, 75, 100].map((y) => (
              <line
                key={y}
                x1={0}
                x2={Math.max(1, n)}
                y1={y}
                y2={y}
                style={{ stroke: "var(--brand-fog)", strokeWidth: 1, opacity: y === 100 ? 0.9 : 0.45 }}
                vectorEffect="non-scaling-stroke"
              />
            ))}
            {/* bars + full-height transparent hit area (so zero days still show a tooltip) */}
            {buckets.map((b, i) => {
              const h = b.count > 0 ? (b.count / max) * 100 : 0;
              return (
                <g key={b.key}>
                  {h > 0 && (
                    <rect
                      x={i + 0.12}
                      width={0.76}
                      y={100 - h}
                      height={h}
                      style={{ fill: "var(--brand-accent)" }}
                    />
                  )}
                  <rect x={i} width={1} y={0} height={100} style={{ fill: "transparent" }}>
                    <title>{b.tooltip}</title>
                  </rect>
                </g>
              );
            })}
          </svg>

          {/* x-axis ticks */}
          <div style={{ position: "relative", height: 14, marginTop: 2 }}>
            {buckets.map((b, i) =>
              tickIdx.has(i) ? (
                <span
                  key={b.key}
                  style={{
                    position: "absolute",
                    left: `${((i + 0.5) / Math.max(1, n)) * 100}%`,
                    transform: "translateX(-50%)",
                    fontFamily: MONO,
                    fontSize: 10,
                    color: "var(--brand-slate)",
                    whiteSpace: "nowrap",
                  }}
                >
                  {b.tick}
                </span>
              ) : null,
            )}
          </div>
        </div>

        <div style={{ fontFamily: MONO, fontSize: 10, color: "var(--brand-slate)", marginTop: 8, letterSpacing: 0.5 }}>
          {caption}
        </div>
      </div>
    </div>
  );
}
