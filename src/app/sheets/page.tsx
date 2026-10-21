import type { Metadata } from "next";
import Link from "next/link";
import { desc, gte } from "drizzle-orm";
import { db, rawQuery } from "@/lib/db";
import { breakSheets, breakSheetPrices } from "@/lib/schema";
import { TimeRangeTabs } from "@/components/TimeRangeTabs";
import { VolumeChart, type Bucket, type VolumeStat } from "./VolumeChart";

// Internal admin analytics — never indexed, never linked from public nav.
export const metadata: Metadata = {
  title: "Saved Break Sheets",
  robots: { index: false, follow: false },
};
export const dynamic = "force-dynamic";

const GREEN = "var(--brand-ok)";
const RED = "#C0362C";

const DAY = 86_400_000;
const HOUR = 3_600_000;
const VALID_RANGES = ["24h", "7d", "30d", "1y", "all"] as const;
type Range = (typeof VALID_RANGES)[number];

function cutoffMs(range: Range, now: number): number {
  switch (range) {
    case "24h": return now - 24 * HOUR;
    case "7d":  return now - 7 * DAY;
    case "30d": return now - 30 * DAY;
    case "1y":  return now - 365 * DAY;
    case "all": return 0;
  }
}

function usd(n: number | null): string {
  if (n == null) return "—";
  return "$" + n.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}
function fmtDate(ms: number): string {
  return new Date(ms).toISOString().replace("T", " ").slice(0, 16) + " UTC";
}

// ── Chart aggregation (all buckets are UTC) ──────────────────────────────────
const dayKey = (ms: number) => new Date(ms).toISOString().slice(0, 10);          // YYYY-MM-DD
const hourKey = (ms: number) => new Date(ms).toISOString().slice(0, 13);         // YYYY-MM-DDTHH
const dayMs = (key: string) => Date.parse(key + "T00:00:00Z");
const hourMs = (key: string) => Date.parse(key + ":00:00Z");
const fmtShort = (ms: number) => new Date(ms).toLocaleDateString("en-US", { timeZone: "UTC", month: "short", day: "numeric" });
const fmtFull = (ms: number) => new Date(ms).toLocaleDateString("en-US", { timeZone: "UTC", weekday: "short", month: "short", day: "numeric", year: "numeric" });
const fmtHour = (ms: number) => new Date(ms).toLocaleString("en-US", { timeZone: "UTC", month: "short", day: "numeric", hour: "2-digit", minute: "2-digit", hour12: false });
const plural = (n: number) => `${n.toLocaleString()} sheet${n === 1 ? "" : "s"}`;

interface ChartData {
  buckets: Bucket[];
  caption: string;
  stats: VolumeStat[];
}

async function buildChart(range: Range, now: number, cutoff: number, nameBySlug: Map<string, string>): Promise<ChartData> {
  const hourly = range === "24h";

  // One aggregate for the volume series (server-side GROUP BY, UTC bucket).
  const rows = await rawQuery.all<{ bucket: string; n: number }>(
    hourly
      ? "SELECT strftime('%Y-%m-%dT%H', created_at / 1000, 'unixepoch') AS bucket, COUNT(*) AS n FROM break_sheets WHERE created_at >= ? GROUP BY bucket ORDER BY bucket"
      : "SELECT date(created_at / 1000, 'unixepoch') AS bucket, COUNT(*) AS n FROM break_sheets WHERE created_at >= ? GROUP BY bucket ORDER BY bucket",
    cutoff,
  );
  const counts = new Map<string, number>(rows.map((r) => [r.bucket, r.n]));

  // Zero-fill a continuous axis from the window start to now.
  const step = hourly ? HOUR : DAY;
  const keyer = hourly ? hourKey : dayKey;
  let startMs: number;
  if (cutoff > 0) {
    startMs = Math.floor(cutoff / step) * step;
  } else if (rows.length > 0) {
    startMs = hourly ? hourMs(rows[0].bucket) : dayMs(rows[0].bucket);
  } else {
    startMs = Math.floor(now / step) * step;
  }

  // Base buckets (per day, or per hour for 24h) — stats are computed from these.
  interface Base { ms: number; count: number }
  const base: Base[] = [];
  for (let t = startMs; t <= now; t += step) {
    base.push({ ms: t, count: counts.get(keyer(t)) ?? 0 });
  }

  const total = base.reduce((a, b) => a + b.count, 0);
  const dayCount = hourly ? 1 : base.length;

  // Peak bucket (from base series).
  let peak = base[0] ?? { ms: startMs, count: 0 };
  for (const b of base) if (b.count > peak.count) peak = b;

  // Weekly roll-up for long windows so bars stay legible.
  const weekly = !hourly && (range === "1y" || range === "all") && base.length > 120;

  let buckets: Bucket[];
  let caption: string;
  if (hourly) {
    buckets = base.map((b) => ({
      key: hourKey(b.ms),
      tick: new Date(b.ms).toLocaleTimeString("en-US", { timeZone: "UTC", hour: "2-digit", minute: "2-digit", hour12: false }),
      tooltip: `${fmtHour(b.ms)} UTC — ${plural(b.count)}`,
      count: b.count,
    }));
    caption = "by hour · UTC";
  } else if (weekly) {
    buckets = [];
    for (let i = 0; i < base.length; i += 7) {
      const chunk = base.slice(i, i + 7);
      const c = chunk.reduce((a, b) => a + b.count, 0);
      const first = chunk[0].ms;
      const last = chunk[chunk.length - 1].ms;
      buckets.push({
        key: dayKey(first),
        tick: fmtShort(first),
        tooltip: `Week of ${fmtShort(first)}–${fmtShort(last)} — ${plural(c)}`,
        count: c,
      });
    }
    caption = "by week · UTC";
  } else {
    buckets = base.map((b) => ({
      key: dayKey(b.ms),
      tick: fmtShort(b.ms),
      tooltip: `${fmtFull(b.ms)} — ${plural(b.count)}`,
      count: b.count,
    }));
    caption = "by day · UTC";
  }

  // Top set in the window (separate group-by).
  const topRows = await rawQuery.all<{ slug: string; n: number }>(
    "SELECT set_slug AS slug, COUNT(*) AS n FROM break_sheets WHERE created_at >= ? GROUP BY set_slug ORDER BY n DESC, slug LIMIT 1",
    cutoff,
  );
  const top = topRows[0];

  const avgDen = hourly ? 24 : dayCount;
  const avg = avgDen > 0 ? total / avgDen : 0;
  const avgStr = avg >= 10 ? Math.round(avg).toLocaleString() : avg.toFixed(1);

  const stats: VolumeStat[] = [
    { label: "Total sheets", value: total.toLocaleString() },
    { label: hourly ? "Avg / hour" : "Avg / day", value: avgStr },
    {
      label: hourly ? "Peak hour" : "Peak day",
      value: peak.count.toLocaleString(),
      sub: total > 0 ? (hourly ? `${fmtHour(peak.ms)} UTC` : fmtShort(peak.ms)) : "—",
    },
    top
      ? { label: "Top set", value: nameBySlug.get(top.slug) ?? top.slug, sub: plural(top.n) }
      : { label: "Top set", value: "—" },
  ];

  return { buckets, caption, stats };
}

export default async function SheetsAdminPage({
  searchParams,
}: {
  searchParams: Promise<{ secret?: string | string[]; range?: string | string[] }>;
}) {
  const sp = await searchParams;
  const provided = typeof sp.secret === "string" ? sp.secret : "";
  const expected = process.env.ADMIN_SECRET;
  const rangeParam = typeof sp.range === "string" ? sp.range : "";
  const range: Range = (VALID_RANGES as readonly string[]).includes(rangeParam) ? (rangeParam as Range) : "30d";

  // Gate: query-param secret compared to ADMIN_SECRET (same shape as the
  // REVALIDATE_SECRET check used by /api/revalidate). No secret configured or
  // no/incorrect match → deny without revealing any data. (Unchanged.)
  if (!expected || provided !== expected) {
    return (
      <div className="h-full overflow-y-auto bg-zinc-950 text-zinc-300">
        <div className="max-w-md mx-auto px-6 py-24 text-center">
          <h1 className="text-2xl text-white mb-2" style={{ fontFamily: "var(--brand-font-head)", fontSynthesisWeight: "none", fontWeight: 400 }}>Unauthorized</h1>
          <p className="text-sm text-zinc-500">
            This page requires an admin secret: <code>/sheets?secret=…</code>
          </p>
        </div>
      </div>
    );
  }

  const now = Date.now();
  const cutoff = cutoffMs(range, now);

  const sheets = await db
    .select()
    .from(breakSheets)
    .where(gte(breakSheets.createdAt, cutoff))
    .orderBy(desc(breakSheets.createdAt));
  const allPrices = await db.select().from(breakSheetPrices);
  const pricesBySheet = new Map<number, typeof allPrices>();
  for (const p of allPrices) {
    const list = pricesBySheet.get(p.sheetId) ?? [];
    list.push(p);
    pricesBySheet.set(p.sheetId, list);
  }

  // Resolve display names from slugs (slug isn't on the Drizzle schema, so read
  // it via rawQuery). A saved sheet's slug may no longer match any set (deleted
  // /renamed) → fall back to the raw slug and don't link.
  const slugs = [...new Set(sheets.map((s) => s.setSlug))];
  const nameBySlug = new Map<string, string>();
  if (slugs.length > 0) {
    try {
      const rows = await rawQuery.all<{ slug: string; name: string }>(
        `SELECT slug, name FROM sets WHERE slug IN (${slugs.map(() => "?").join(",")})`,
        ...slugs
      );
      for (const r of rows) nameBySlug.set(r.slug, r.name);
    } catch {
      /* slug column may not exist yet → all fall back to raw slug */
    }
  }

  const chart = await buildChart(range, now, cutoff, nameBySlug);

  return (
    <div className="h-full overflow-y-auto" style={{ background: "var(--brand-page)" }}>
      <div className="mx-auto cl-container" style={{ maxWidth: 1440, padding: "40px 56px 80px" }}>
        {/* Breadcrumb: Home / Sheets */}
        <div style={{ fontFamily: "var(--cl-font-display)", fontSize: 13 }}>
          <Link href="/" style={{ color: "var(--brand-slate)", textDecoration: "none" }}>
            Home
          </Link>
          <span style={{ color: "var(--brand-line)", margin: "0 6px" }}>/</span>
          <span style={{ color: "var(--brand-ink-soft)" }}>Sheets</span>
        </div>

        {/* Title */}
        <h1 className="page-title" style={{ margin: "12px 0 0" }}>
          Saved Break Sheets
        </h1>
        <p style={{ fontSize: 14, color: "var(--brand-slate)", margin: "6px 0 0" }}>
          {sheets.length.toLocaleString()} sheet{sheets.length === 1 ? "" : "s"} · newest first · anonymous
        </p>

        {/* Time range + daily volume chart */}
        <div style={{ marginTop: 24, display: "flex", justifyContent: "flex-end" }}>
          <TimeRangeTabs current={range} basePath="/sheets" params={{ secret: provided }} />
        </div>
        <div style={{ marginTop: 14 }}>
          <VolumeChart buckets={chart.buckets} caption={chart.caption} stats={chart.stats} />
        </div>

        {sheets.length === 0 ? (
          <p style={{ fontSize: 14, color: "var(--brand-slate)", marginTop: 28 }}>
            {range === "all" ? "No saved sheets yet." : "No saved sheets in this window."}
          </p>
        ) : (
          <div className="space-y-2" style={{ marginTop: 28 }}>
            {sheets.map((s) => {
              const prices = (pricesBySheet.get(s.id) ?? []).slice().sort((a, b) => b.price - a.price);
              const displayName = nameBySlug.get(s.setSlug);
              const profitColor = s.profit == null ? "var(--brand-slate)" : s.profit >= 0 ? GREEN : RED;
              return (
                <details key={s.id} className="rounded-lg overflow-hidden" style={{ border: "1px solid var(--brand-line)", background: "var(--brand-card)" }}>
                  <summary
                    className="cursor-pointer list-none flex flex-wrap items-center gap-x-5 gap-y-1.5"
                    style={{ padding: "12px 16px" }}
                  >
                    <span style={{ fontFamily: "var(--cl-font-mono)", fontSize: 11, color: "var(--brand-slate)", width: 132, flexShrink: 0 }}>
                      {fmtDate(s.createdAt)}
                    </span>
                    {/* Set display name (falls back to slug; links when the set exists) */}
                    <span className="min-w-0 flex-1 truncate" style={{ fontSize: 14, fontWeight: 500, minWidth: 140 }} title={displayName ?? s.setSlug}>
                      {displayName ? (
                        <Link href={`/sets/${s.setSlug}`} style={{ color: "var(--brand-ink)", textDecoration: "none" }}>
                          {displayName}
                        </Link>
                      ) : (
                        <span style={{ color: "var(--brand-ink)" }}>{s.setSlug}</span>
                      )}
                    </span>
                    <span style={{ fontSize: 12, color: "var(--brand-slate)", width: 84 }} className="truncate" title={s.sport}>{s.sport}</span>
                    <span style={{ fontSize: 12, color: "var(--brand-slate)", width: 96, fontVariantNumeric: "tabular-nums" }}>
                      {s.quantity} {s.breakUnit}
                    </span>
                    <span style={{ fontSize: 12, color: "var(--brand-ink-soft)", width: 104, textAlign: "right", fontVariantNumeric: "tabular-nums" }}>
                      Cost {usd(s.cost)}
                    </span>
                    <span style={{ fontSize: 12, color: GREEN, width: 104, textAlign: "right", fontVariantNumeric: "tabular-nums" }}>
                      Total {usd(s.total)}
                    </span>
                    <span style={{ fontSize: 12, color: profitColor, width: 112, textAlign: "right", fontVariantNumeric: "tabular-nums" }}>
                      Profit {usd(s.profit)}
                    </span>
                    <span style={{ fontSize: 11, color: "var(--brand-fog)", width: 64, textAlign: "right" }}>{prices.length} spots</span>
                  </summary>
                  <div style={{ borderTop: "1px solid var(--brand-line)", padding: "12px 16px", background: "var(--brand-page)" }}>
                    {prices.length === 0 ? (
                      <p style={{ fontSize: 12, color: "var(--brand-fog)" }}>No per-spot prices recorded.</p>
                    ) : (
                      <table className="w-full" style={{ fontSize: 12, borderCollapse: "collapse" }}>
                        <thead>
                          <tr style={{ color: "var(--brand-slate)", textAlign: "left" }}>
                            <th style={{ fontWeight: 500, padding: "2px 16px 6px 0" }}>Subject</th>
                            <th style={{ fontWeight: 500, padding: "2px 16px 6px 0" }}>Type</th>
                            <th style={{ fontWeight: 500, padding: "2px 0 6px", textAlign: "right" }}>Price</th>
                          </tr>
                        </thead>
                        <tbody>
                          {prices.map((p) => (
                            <tr key={p.id} style={{ borderTop: "1px solid var(--brand-track)" }}>
                              <td style={{ padding: "5px 16px 5px 0", color: "var(--brand-ink)" }}>{p.subjectName}</td>
                              <td style={{ padding: "5px 16px 5px 0", color: "var(--brand-slate)" }}>{p.subjectType}</td>
                              <td style={{ padding: "5px 0", textAlign: "right", color: "var(--brand-ink-soft)", fontVariantNumeric: "tabular-nums" }}>{usd(p.price)}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    )}
                  </div>
                </details>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
