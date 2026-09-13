/**
 * Shared cookie-consent contract used by the banner (client) and /api/consent
 * (server). One first-party cookie `c2_consent` holds the visitor's choice; a
 * non-identifying row is logged to consent_events on each choice/change.
 *
 * Categories: only "analytics" is gated today (Google Analytics / gtag). There
 * is no advertising script on the site, so `advertising` is carried in the
 * payload for forward-compatibility but is ALWAYS 0. When an ad script is
 * added, surface an Advertising toggle in the banner AND bump NOTICE_VERSION so
 * everyone is re-prompted.
 */

export const CONSENT_COOKIE = "c2_consent";

/** Notice version. Bump to re-prompt everyone when categories or copy change. */
export const NOTICE_VERSION = 1;

/** 12-month cookie lifetime, in seconds. */
export const CONSENT_MAX_AGE = 60 * 60 * 24 * 365;

export interface ConsentValue {
  id: string; // random UUID, generated on first choice
  v: number; // notice version
  ts: string; // ISO timestamp
  analytics: boolean;
  advertising: boolean; // always false today (no ad script to gate)
  gpc: boolean; // whether Global Privacy Control was present
}

const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

/** Validate the shape of a consent payload (server-side, strict). */
export function isValidConsent(x: unknown): x is ConsentValue {
  if (!x || typeof x !== "object") return false;
  const o = x as Record<string, unknown>;
  return (
    typeof o.id === "string" && UUID_RE.test(o.id) &&
    typeof o.v === "number" && Number.isInteger(o.v) && o.v >= 1 &&
    typeof o.ts === "string" && o.ts.length > 0 && o.ts.length <= 40 &&
    typeof o.analytics === "boolean" &&
    typeof o.advertising === "boolean" &&
    typeof o.gpc === "boolean"
  );
}
