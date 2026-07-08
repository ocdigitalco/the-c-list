import type { Metadata } from "next";
import { desc } from "drizzle-orm";
import { db } from "@/lib/db";
import { breakSheets, breakSheetPrices } from "@/lib/schema";

// Internal admin analytics — never indexed, never linked from public nav.
export const metadata: Metadata = {
  title: "Saved Break Sheets",
  robots: { index: false, follow: false },
};
export const dynamic = "force-dynamic";

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
  // no/incorrect match → deny without revealing any data.
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

  return (
    <div className="h-full overflow-y-auto bg-zinc-950 text-zinc-200">
      <div className="max-w-5xl mx-auto px-6 py-10">
        <h1 className="text-2xl font-bold text-white tracking-tight mb-1">Saved Break Sheets</h1>
        <p className="text-sm text-zinc-500 mb-8">
          {sheets.length.toLocaleString()} sheet{sheets.length === 1 ? "" : "s"} · newest first · anonymous
        </p>

        {sheets.length === 0 ? (
          <p className="text-sm text-zinc-500">No saved sheets yet.</p>
        ) : (
          <div className="space-y-2">
            {sheets.map((s) => {
              const prices = (pricesBySheet.get(s.id) ?? []).slice().sort((a, b) => b.price - a.price);
              const profitColor = s.profit == null ? "text-zinc-400" : s.profit >= 0 ? "text-emerald-400" : "text-red-400";
              return (
                <details key={s.id} className="rounded-lg border border-zinc-800 bg-zinc-900/60 overflow-hidden">
                  <summary className="cursor-pointer list-none px-4 py-3 flex flex-wrap items-center gap-x-5 gap-y-1 hover:bg-zinc-900">
                    <span className="text-xs font-mono text-zinc-500 w-[132px] shrink-0">{fmtDate(s.createdAt)}</span>
                    <span className="text-sm font-medium text-white min-w-0 flex-1 truncate">{s.setSlug}</span>
                    <span className="text-xs text-zinc-400 w-20">{s.sport}</span>
                    <span className="text-xs text-zinc-400 w-24 tabular-nums">
                      {s.quantity} {s.breakUnit}
                    </span>
                    <span className="text-xs text-zinc-400 w-24 tabular-nums text-right">Cost {usd(s.cost)}</span>
                    <span className="text-xs text-emerald-400 w-24 tabular-nums text-right">Total {usd(s.total)}</span>
                    <span className={`text-xs w-24 tabular-nums text-right ${profitColor}`}>Profit {usd(s.profit)}</span>
                    <span className="text-[10px] text-zinc-600 w-16 text-right">{prices.length} spots</span>
                  </summary>
                  <div className="border-t border-zinc-800 px-4 py-3 bg-zinc-950/50">
                    {prices.length === 0 ? (
                      <p className="text-xs text-zinc-600">No per-spot prices recorded.</p>
                    ) : (
                      <table className="w-full text-xs">
                        <thead>
                          <tr className="text-zinc-500 text-left">
                            <th className="font-medium py-1 pr-4">Subject</th>
                            <th className="font-medium py-1 pr-4">Type</th>
                            <th className="font-medium py-1 text-right">Price</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-zinc-800/60">
                          {prices.map((p) => (
                            <tr key={p.id}>
                              <td className="py-1 pr-4 text-zinc-200">{p.subjectName}</td>
                              <td className="py-1 pr-4 text-zinc-500">{p.subjectType}</td>
                              <td className="py-1 text-right tabular-nums text-zinc-300">{usd(p.price)}</td>
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
