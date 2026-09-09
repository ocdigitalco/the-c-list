import { NextResponse } from "next/server";
import { upsertNewsletterContact } from "@/lib/resendContacts";

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

  // Signup attribution — where the form lives (footer / updates-page). Fall back
  // to a generic label rather than trusting arbitrary client input.
  const rawSource = typeof body.source === "string" ? body.source.trim() : "";
  const source = /^[a-z0-9_-]{1,40}$/i.test(rawSource) ? rawSource : "newsletter-form";

  // Global contacts upsert: create with signup_source, segment, and topic
  // opt-in; on "already exists" it reconciles (never leaks membership).
  const result = await upsertNewsletterContact({ email, source });

  if (result.status === "missing_config") {
    return NextResponse.json(
      { error: "Something went wrong. Please try again later." },
      { status: 500 }
    );
  }
  if (result.status === "error") {
    return NextResponse.json(
      { error: "We couldn't sign you up. Please try again later." },
      { status: 502 }
    );
  }
  return NextResponse.json({ ok: true }, { status: 200 });
}
