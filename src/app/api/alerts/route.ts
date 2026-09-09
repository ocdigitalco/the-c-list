import { NextResponse } from "next/server";
import { randomBytes } from "crypto";
import { db, rawQuery } from "@/lib/db";
import { setAlerts } from "@/lib/schema";
import { upsertNewsletterContact } from "@/lib/resendContacts";

// Writes to the production-owned set_alerts table (Turso is source of truth).
export const runtime = "nodejs";
export const dynamic = "force-dynamic";

// ── In-memory rate limit ─────────────────────────────────────────────────────
// Max 5 submissions per IP per 10 minutes. Same pattern as the contact/subscribe
// routes. CAVEAT: per-serverless-instance memory, not global — fine at current
// volume; swap for a shared store (Upstash / Vercel KV) if abuse appears.
const RATE_LIMIT_MAX = 5;
const RATE_LIMIT_WINDOW_MS = 10 * 60 * 1000;
const rateLimitHits = new Map<string, number[]>();

function isRateLimited(ip: string): boolean {
  const now = Date.now();
  const recent = (rateLimitHits.get(ip) ?? []).filter(
    (t) => now - t < RATE_LIMIT_WINDOW_MS
  );
  if (recent.length >= RATE_LIMIT_MAX) {
    rateLimitHits.set(ip, recent);
    return true;
  }
  recent.push(now);
  rateLimitHits.set(ip, recent);
  return false;
}

function clientIp(req: Request): string {
  const fwd = req.headers.get("x-forwarded-for");
  if (fwd) return fwd.split(",")[0].trim();
  return req.headers.get("x-real-ip")?.trim() || "unknown";
}

// Pragmatic email check: one @, non-empty local part, a dotted domain, no spaces.
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

async function subscribeToNewsletter(email: string, setSlug: string): Promise<void> {
  // Attribution: source "odds-alert" and the set slug as signup_set. Best-effort;
  // any failure here must NOT fail the alert insert.
  const result = await upsertNewsletterContact({ email, source: "odds-alert", set: setSlug });
  if (result.status !== "ok") {
    console.error("[alerts] newsletter opt-in non-fatal failure:", result.status, result.error ?? "");
  }
}

export async function POST(req: Request) {
  let body: Record<string, unknown>;
  try {
    body = (await req.json()) as Record<string, unknown>;
  } catch {
    return NextResponse.json({ error: "Invalid request." }, { status: 400 });
  }

  // Honeypot: real users never fill `website`. Silent 200, no work.
  if (typeof body.website === "string" && body.website.trim() !== "") {
    return NextResponse.json({ ok: true }, { status: 200 });
  }

  if (isRateLimited(clientIp(req))) {
    return NextResponse.json(
      { error: "Too many requests. Please try again in a few minutes." },
      { status: 429 }
    );
  }

  const email = typeof body.email === "string" ? body.email.trim() : "";
  if (!EMAIL_RE.test(email) || email.length > 254) {
    return NextResponse.json(
      { errors: { email: "Please enter a valid email address." } },
      { status: 400 }
    );
  }

  const setSlug = typeof body.setSlug === "string" ? body.setSlug.trim() : "";
  const set = await rawQuery.get<{ id: number }>(
    "SELECT id FROM sets WHERE slug = ?",
    setSlug
  );
  if (!set) {
    return NextResponse.json({ error: "Set not found." }, { status: 404 });
  }

  const token = randomBytes(32).toString("hex"); // 64 hex chars

  try {
    // On (email, set_id) — or token — conflict, do nothing and still return 200
    // so we never leak whether the address was already subscribed.
    await db
      .insert(setAlerts)
      .values({ email, setId: set.id, token })
      .onConflictDoNothing();
  } catch (err) {
    console.error("[alerts] insert failed:", err);
    return NextResponse.json(
      { error: "Something went wrong. Please try again later." },
      { status: 500 }
    );
  }

  // Optional newsletter opt-in — best-effort; never fails the alert.
  if (body.newsletter === true) {
    await subscribeToNewsletter(email, setSlug);
  }

  return NextResponse.json({ ok: true }, { status: 200 });
}
