import { NextResponse } from "next/server";
import { Resend } from "resend";

// Talks to Resend → Node.js runtime, never static.
export const runtime = "nodejs";
export const dynamic = "force-dynamic";

// ── In-memory rate limit ─────────────────────────────────────────────────────
// Max 3 submissions per IP per 10 minutes.
//
// CAVEAT: this Map lives in a single serverless instance's memory. On Vercel's
// Fluid Compute, instances are reused but not shared, so the limit is per-
// instance, not global. Acceptable at current volume; swap for a shared store
// (Upstash Redis / Vercel KV) if abuse appears.
const RATE_LIMIT_MAX = 3;
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

export async function POST(req: Request) {
  let body: Record<string, unknown>;
  try {
    body = (await req.json()) as Record<string, unknown>;
  } catch {
    return NextResponse.json({ error: "Invalid request." }, { status: 400 });
  }

  // Honeypot: real users never fill `website`. Silent 200, no API call.
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

  const apiKey = process.env.RESEND_NEWSLETTER_API_KEY;
  const audienceId = process.env.RESEND_AUDIENCE_ID;
  if (!apiKey || !audienceId) {
    // Never leak which piece of config is missing.
    console.error(
      "[subscribe] Missing env:",
      !apiKey ? "RESEND_NEWSLETTER_API_KEY" : "",
      !audienceId ? "RESEND_AUDIENCE_ID" : ""
    );
    return NextResponse.json(
      { error: "Something went wrong. Please try again later." },
      { status: 500 }
    );
  }

  try {
    const resend = new Resend(apiKey);
    const { data, error } = await resend.contacts.create({
      email,
      audienceId,
      unsubscribed: false,
    });

    if (error) {
      // Already-subscribed / duplicate → treat as success (idempotent; never
      // leak whether an address is already a member).
      const msg = String(
        (error as { message?: string }).message ?? ""
      ).toLowerCase();
      const code = (error as { statusCode?: number }).statusCode;
      const isDuplicate =
        code === 409 || /already|exists|duplicate/i.test(msg);
      if (isDuplicate) {
        return NextResponse.json({ ok: true }, { status: 200 });
      }
      console.error("[subscribe] Resend error:", error);
      return NextResponse.json(
        { error: "We couldn't sign you up. Please try again later." },
        { status: 502 }
      );
    }

    return NextResponse.json({ ok: true, id: data?.id ?? null }, { status: 200 });
  } catch (err) {
    console.error("[subscribe] Resend threw:", err);
    return NextResponse.json(
      { error: "We couldn't sign you up. Please try again later." },
      { status: 502 }
    );
  }
}
