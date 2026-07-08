import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { breakSheets, breakSheetPrices } from "@/lib/schema";

/**
 * Save a break sheet + its per-spot prices when the user exports the CSV.
 * Writes to the production DB (Turso in prod, local SQLite in dev). Anonymous —
 * no accounts, no PII. Called fire-and-forget from the client, so a failure
 * here must never affect the user's download.
 */

interface PriceInput {
  subjectName: string;
  subjectType: "athlete" | "team";
  price: number;
}

function num(v: unknown): number | null {
  const n = typeof v === "number" ? v : typeof v === "string" ? parseFloat(v) : NaN;
  return Number.isFinite(n) ? n : null;
}

export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => null);
  if (!body || typeof body !== "object") {
    return NextResponse.json({ error: "invalid json" }, { status: 400 });
  }

  const setSlug = typeof body.setSlug === "string" ? body.setSlug : null;
  const sport = typeof body.sport === "string" ? body.sport : null;
  const breakUnit = body.breakUnit === "cases" || body.breakUnit === "boxes" ? body.breakUnit : null;
  const quantity = num(body.quantity);
  const total = num(body.total);
  if (!setSlug || !sport || !breakUnit || quantity == null || total == null) {
    return NextResponse.json({ error: "missing required fields" }, { status: 400 });
  }
  const cost = num(body.cost); // nullable
  const profit = num(body.profit); // nullable

  const rawPrices: unknown[] = Array.isArray(body.prices) ? body.prices : [];
  const prices: PriceInput[] = [];
  for (const p of rawPrices) {
    if (!p || typeof p !== "object") continue;
    const rec = p as Record<string, unknown>;
    const price = num(rec.price);
    const subjectName = typeof rec.subjectName === "string" ? rec.subjectName : null;
    const subjectType = rec.subjectType === "athlete" || rec.subjectType === "team" ? rec.subjectType : null;
    if (subjectName && subjectType && price != null) {
      prices.push({ subjectName, subjectType, price });
    }
  }

  const config = typeof body.config === "string" ? body.config : JSON.stringify(body.config ?? {});

  const [inserted] = await db
    .insert(breakSheets)
    .values({
      createdAt: Date.now(),
      setSlug,
      sport,
      breakUnit,
      quantity: Math.round(quantity),
      cost,
      total,
      profit,
      config,
    })
    .returning({ id: breakSheets.id });

  if (inserted && prices.length > 0) {
    await db.insert(breakSheetPrices).values(
      prices.map((p) => ({
        sheetId: inserted.id,
        subjectName: p.subjectName,
        subjectType: p.subjectType,
        price: p.price,
      }))
    );
  }

  return NextResponse.json({ ok: true, id: inserted?.id ?? null });
}
