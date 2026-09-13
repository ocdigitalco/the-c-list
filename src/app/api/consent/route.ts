import { NextRequest, NextResponse } from "next/server";
import { rawQuery } from "@/lib/db";
import { CONSENT_COOKIE, isValidConsent } from "@/lib/consent";

// Writes Turso + reads a cookie → Node.js runtime, never static.
export const runtime = "nodejs";
export const dynamic = "force-dynamic";

// ── Per-consent-id rate limit: at most one write per second ───────────────────
// In-memory, per serverless instance (see the note in /api/subscribe). Consent
// writes are low-volume and fire-and-forget, so a per-instance guard is enough
// to shed accidental bursts; it never blocks the cookie write on the client.
const lastWriteAt = new Map<string, number>();
const RATE_MS = 1000;
const MAX_BODY_BYTES = 1024; // reject bodies over 1 KB

function tooSoon(id: string): boolean {
  const now = Date.now();
  const prev = lastWriteAt.get(id);
  if (prev != null && now - prev < RATE_MS) return true;
  lastWriteAt.set(id, now);
  // Opportunistic cleanup so the map can't grow unbounded.
  if (lastWriteAt.size > 5000) {
    for (const [k, t] of lastWriteAt) if (now - t > 60_000) lastWriteAt.delete(k);
  }
  return false;
}

/**
 * POST /api/consent — log one non-identifying consent row.
 * Body is the c2_consent payload plus a `source` ('banner'|'settings'|'gpc-default').
 * Validates shape, inserts one row, returns 204. Never logs any request header,
 * IP, user agent, device, geo, or referrer.
 */
export async function POST(req: NextRequest) {
  // Size guard (header first, then measured).
  const len = Number(req.headers.get("content-length") ?? "0");
  if (len > MAX_BODY_BYTES) return new NextResponse(null, { status: 413 });

  const raw = await req.text();
  if (new TextEncoder().encode(raw).length > MAX_BODY_BYTES) {
    return new NextResponse(null, { status: 413 });
  }

  let body: unknown;
  try { body = JSON.parse(raw); } catch { return new NextResponse(null, { status: 400 }); }

  const o = body as Record<string, unknown> | null;
  const source = o && typeof o.source === "string" ? o.source : "";
  if (!["banner", "settings", "gpc-default"].includes(source)) {
    return new NextResponse(null, { status: 400 });
  }
  if (!isValidConsent(body)) return new NextResponse(null, { status: 400 });

  if (tooSoon(body.id)) return new NextResponse(null, { status: 204 }); // silently drop

  try {
    await rawQuery.run(
      `INSERT INTO consent_events (consent_id, ts, notice_version, analytics, advertising, gpc, source)
       VALUES (?, ?, ?, ?, ?, ?, ?)`,
      body.id, body.ts, body.v,
      body.analytics ? 1 : 0,
      body.advertising ? 1 : 0, // always 0 today
      body.gpc ? 1 : 0,
      source
    );
  } catch {
    // Fire-and-forget from the client: a logging failure must never surface.
    return new NextResponse(null, { status: 204 });
  }
  return new NextResponse(null, { status: 204 });
}

/**
 * DELETE /api/consent — privacy deletion path. Removes every consent_events row
 * for the caller's consent id (from the c2_consent cookie, or a JSON body
 * `{ consent_id }`) and clears the cookie. Returns 204.
 */
export async function DELETE(req: NextRequest) {
  let id: string | undefined = req.cookies.get(CONSENT_COOKIE)?.value;
  if (id) {
    try { id = JSON.parse(id).id; } catch { id = undefined; }
  }
  if (!id) {
    const raw = await req.text().catch(() => "");
    if (raw && new TextEncoder().encode(raw).length <= MAX_BODY_BYTES) {
      try { id = JSON.parse(raw).consent_id; } catch { /* ignore */ }
    }
  }

  const res = new NextResponse(null, { status: 204 });
  // Always clear the cookie, even if we couldn't resolve an id.
  res.cookies.set(CONSENT_COOKIE, "", { path: "/", maxAge: 0 });

  if (typeof id === "string" && id.length > 0 && id.length <= 64) {
    try {
      await rawQuery.run("DELETE FROM consent_events WHERE consent_id = ?", id);
    } catch {
      // deletion best-effort; cookie is already cleared on the response
    }
  }
  return res;
}
