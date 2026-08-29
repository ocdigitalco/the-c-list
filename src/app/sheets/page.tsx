import type { Metadata } from "next";
import Link from "next/link";
import { desc } from "drizzle-orm";
import { db, rawQuery } from "@/lib/db";
import { breakSheets, breakSheetPrices } from "@/lib/schema";

// Internal admin analytics — never indexed, never linked from public nav.
export const metadata: Metadata = {
  title: "Saved Break Sheets",
  robots: { index: false, follow: false },
};
export const dynamic = "force-dynamic";

const GREEN = "#0E8A4F";
const RED = "#C0362C";

function usd(n: number | null): string {
  if (n == null) return "—";
  return "$" + n.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}
function fmtDate(ms: number): string {
  return new Date(ms).toISOString().replace("T", " ").slice(0, 16) + " UTC";
}

export default async function SheetsAdminPage({
  searchParams,
}: {
  searchParams: Promise<{ secret?: string | string[] }>;
}) {
  const sp = await searchParams;
  const provided = typeof sp.secret === "string" ? sp.secret : "";
  const expected = process.env.ADMIN_SECRET;

  // Gate: query-param secret compared to ADMIN_SECRET (same shape as the
  // REVALIDATE_SECRET check used by /api/revalidate). No secret configured or
  // no/incorrect match → deny without revealing any data. (Unchanged.)
  if (!expected || provided !== expected) {
    return (
      <div className="h-full overflow-y-auto bg-zinc-950 text-zinc-300">
        <div className="max-w-md mx-auto px-6 py-24 text-center">
          <h1 className="text-lg font-semibold text-white mb-2">Unauthorized</h1>
          <p className="text-sm text-zinc-500">
            This page requires an admin secret: <code>/sheets?secret=…</code>
          </p>
        </div>
      </div>
    );
  }

  const sheets = await db.select().from(breakSheets).orderBy(desc(breakSheets.createdAt));
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

  return (
    <div className="h-full overflow-y-auto" style={{ background: "#FAFAF7" }}>
      <div className="mx-auto cl-container" style={{ maxWidth: 1440, padding: "40px 56px 80px" }}>
        {/* Breadcrumb: Home / Sheets */}
        <div style={{ fontFamily: "var(--cl-font-display)", fontSize: 13 }}>
          <Link href="/" style={{ color: "#6B6757", textDecoration: "none" }}>
            Home
          </Link>
          <span style={{ color: "#D9D5C7", margin: "0 6px" }}>/</span>
          <span style={{ color: "#3A372F" }}>Sheets</span>
        </div>

        {/* Title */}
        <h1
          className="cl-title"
          style={{ fontFamily: "var(--cl-font-display)", fontSize: 48, fontWeight: 600, letterSpacing: "-1.2px", color: "var(--brand-ink)", margin: "12px 0 0", lineHeight: 1.1 }}
        >
          Saved Break Sheets
        </h1>
        <p style={{ fontSize: 14, color: "#6B6757", margin: "6px 0 0" }}>
          {sheets.length.toLocaleString()} sheet{sheets.length === 1 ? "" : "s"} · newest first · anonymous
        </p>

        {sheets.length === 0 ? (
          <p style={{ fontSize: 14, color: "#8A8677", marginTop: 28 }}>No saved sheets yet.</p>
        ) : (
          <div className="space-y-2" style={{ marginTop: 28 }}>
            {sheets.map((s) => {
              const prices = (pricesBySheet.get(s.id) ?? []).slice().sort((a, b) => b.price - a.price);
              const displayName = nameBySlug.get(s.setSlug);
              const profitColor = s.profit == null ? "#8A8677" : s.profit >= 0 ? GREEN : RED;
              return (
                <details key={s.id} className="rounded-lg overflow-hidden" style={{ border: "1px solid #EDEAE0", background: "#FFFFFF" }}>
                  <summary
                    className="cursor-pointer list-none flex flex-wrap items-center gap-x-5 gap-y-1.5"
                    style={{ padding: "12px 16px" }}
                  >
                    <span style={{ fontFamily: "var(--cl-font-mono)", fontSize: 11, color: "#8A8677", width: 132, flexShrink: 0 }}>
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
                    <span style={{ fontSize: 12, color: "#6B6757", width: 84 }} className="truncate" title={s.sport}>{s.sport}</span>
                    <span style={{ fontSize: 12, color: "#6B6757", width: 96, fontVariantNumeric: "tabular-nums" }}>
                      {s.quantity} {s.breakUnit}
                    </span>
                    <span style={{ fontSize: 12, color: "#3A372F", width: 104, textAlign: "right", fontVariantNumeric: "tabular-nums" }}>
                      Cost {usd(s.cost)}
                    </span>
                    <span style={{ fontSize: 12, color: GREEN, width: 104, textAlign: "right", fontVariantNumeric: "tabular-nums" }}>
                      Total {usd(s.total)}
                    </span>
                    <span style={{ fontSize: 12, color: profitColor, width: 112, textAlign: "right", fontVariantNumeric: "tabular-nums" }}>
                      Profit {usd(s.profit)}
                    </span>
                    <span style={{ fontSize: 11, color: "#B7B2A3", width: 64, textAlign: "right" }}>{prices.length} spots</span>
                  </summary>
                  <div style={{ borderTop: "1px solid #EDEAE0", padding: "12px 16px", background: "#FAFAF7" }}>
                    {prices.length === 0 ? (
                      <p style={{ fontSize: 12, color: "#B7B2A3" }}>No per-spot prices recorded.</p>
                    ) : (
                      <table className="w-full" style={{ fontSize: 12, borderCollapse: "collapse" }}>
                        <thead>
                          <tr style={{ color: "#8A8677", textAlign: "left" }}>
                            <th style={{ fontWeight: 500, padding: "2px 16px 6px 0" }}>Subject</th>
                            <th style={{ fontWeight: 500, padding: "2px 16px 6px 0" }}>Type</th>
                            <th style={{ fontWeight: 500, padding: "2px 0 6px", textAlign: "right" }}>Price</th>
                          </tr>
                        </thead>
                        <tbody>
                          {prices.map((p) => (
                            <tr key={p.id} style={{ borderTop: "1px solid #F1EEE3" }}>
                              <td style={{ padding: "5px 16px 5px 0", color: "var(--brand-ink)" }}>{p.subjectName}</td>
                              <td style={{ padding: "5px 16px 5px 0", color: "#8A8677" }}>{p.subjectType}</td>
                              <td style={{ padding: "5px 0", textAlign: "right", color: "#3A372F", fontVariantNumeric: "tabular-nums" }}>{usd(p.price)}</td>
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
