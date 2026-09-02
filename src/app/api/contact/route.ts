import { NextResponse } from "next/server";
import { Resend } from "resend";

// This route talks to Resend, which requires the Node.js runtime (not edge).
export const runtime = "nodejs";
// Never statically optimize — every submission must hit the handler.
export const dynamic = "force-dynamic";

const CONTACT_FROM = "Checklist² Contact <contact@updates.checklist2.com>";
const CONTACT_TO = "tyler@checklist2.com";

// ── In-memory rate limit ─────────────────────────────────────────────────────
// Max 3 submissions per IP per 10 minutes.
//
// CAVEAT: this Map lives in a single serverless instance's memory. On Vercel's
// Fluid Compute, instances are reused but not shared, so the limit is per-
// instance, not global — a determined spammer hitting different instances can
// exceed it. That is acceptable at current (near-zero) contact volume. If spam
// appears, swap this for a shared store (Upstash Redis / Vercel KV).
const RATE_LIMIT_MAX = 3;
const RATE_LIMIT_WINDOW_MS = 10 * 60 * 1000;
const rateLimitHits = new Map<string, number[]>();

function isRateLimited(ip: string): boolean {
  const now = Date.now();
  const recent = (rateLimitHits.get(ip) ?? []).filter(
    (t) => now - t < RATE_LIMIT_WINDOW_MS
  );
  if (recent.length >= RATE_LIMIT_MAX) {
    rateLimitHits.set(ip, recent); // keep pruned list; do not record this hit
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

// ── Validation ───────────────────────────────────────────────────────────────
// Pragmatic email check: one @, non-empty local part, a dotted domain, no spaces.
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

type Fields = { name: string; email: string; subject: string; message: string };
type FieldErrors = Partial<Record<keyof Fields, string>>;

function validate(body: Record<string, unknown>): {
  fields: Fields;
  errors: FieldErrors;
} {
  const name = typeof body.name === "string" ? body.name.trim() : "";
  const email = typeof body.email === "string" ? body.email.trim() : "";
  const subject = typeof body.subject === "string" ? body.subject.trim() : "";
  const message = typeof body.message === "string" ? body.message.trim() : "";

  const errors: FieldErrors = {};
  if (name.length < 1 || name.length > 100)
    errors.name = "Please enter your name (1–100 characters).";
  if (!EMAIL_RE.test(email) || email.length > 254)
    errors.email = "Please enter a valid email address.";
  if (message.length < 10 || message.length > 5000)
    errors.message = "Please enter a message between 10 and 5000 characters.";

  return { fields: { name, email, subject, message }, errors };
}

export async function POST(req: Request) {
  // Parse JSON defensively.
  let body: Record<string, unknown>;
  try {
    body = (await req.json()) as Record<string, unknown>;
  } catch {
    return NextResponse.json({ error: "Invalid request." }, { status: 400 });
  }

  // Honeypot: real users never fill `website`. Bots that do get a silent 200 —
  // no email sent, no hint that they were caught.
  if (typeof body.website === "string" && body.website.trim() !== "") {
    return NextResponse.json({ ok: true }, { status: 200 });
  }

  // Rate limit before doing any work.
  if (isRateLimited(clientIp(req))) {
    return NextResponse.json(
      { error: "Too many submissions. Please try again in a few minutes." },
      { status: 429 }
    );
  }

  const { fields, errors } = validate(body);
  if (Object.keys(errors).length > 0) {
    return NextResponse.json({ errors }, { status: 400 });
  }

  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) {
    // Never leak that the key is the problem.
    console.error("[contact] RESEND_API_KEY is not set");
    return NextResponse.json(
      { error: "Something went wrong. Please try again later." },
      { status: 500 }
    );
  }

  const submittedAt = new Date().toISOString();
  const subjectLine =
    "[Checklist² Contact] " + (fields.subject || fields.name);

  // Plain-text body (no HTML → no escaping concerns).
  const text = [
    `New contact form submission`,
    ``,
    `Name:    ${fields.name}`,
    `Email:   ${fields.email}`,
    fields.subject ? `Subject: ${fields.subject}` : null,
    `Time:    ${submittedAt}`,
    ``,
    `Message:`,
    fields.message,
  ]
    .filter((l) => l !== null)
    .join("\n");

  try {
    const resend = new Resend(apiKey);
    const { data, error } = await resend.emails.send({
      from: CONTACT_FROM,
      to: CONTACT_TO,
      replyTo: fields.email,
      subject: subjectLine,
      text,
    });

    if (error) {
      console.error("[contact] Resend error:", error);
      return NextResponse.json(
        { error: "We couldn't send your message. Please try again later." },
        { status: 502 }
      );
    }

    return NextResponse.json({ ok: true, id: data?.id ?? null }, { status: 200 });
  } catch (err) {
    console.error("[contact] Resend threw:", err);
    return NextResponse.json(
      { error: "We couldn't send your message. Please try again later." },
      { status: 502 }
    );
  }
}
