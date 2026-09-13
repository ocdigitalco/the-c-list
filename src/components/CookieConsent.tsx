"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import Script from "next/script";
import {
  CONSENT_COOKIE,
  CONSENT_MAX_AGE,
  NOTICE_VERSION,
  type ConsentValue,
} from "@/lib/consent";

const GA_ID = "G-3T45WWZ64Y";

// Only "analytics" is gated today (Google Analytics). There is no advertising
// script on the site, so `advertising` is always false. When an ad script is
// added: surface an Advertising toggle below AND bump NOTICE_VERSION in
// src/lib/consent.ts so every visitor is re-prompted.

// ── Cookie + choice helpers (client-only) ─────────────────────────────────────
type Choice = { analytics: boolean };
type Source = "banner" | "settings" | "gpc-default";

function readConsent(): ConsentValue | null {
  if (typeof document === "undefined") return null;
  const m = document.cookie.match(/(?:^|;\s*)c2_consent=([^;]+)/);
  if (!m) return null;
  try {
    const v = JSON.parse(decodeURIComponent(m[1]));
    if (v && typeof v.id === "string" && typeof v.analytics === "boolean" && typeof v.v === "number") {
      return v as ConsentValue;
    }
  } catch { /* ignore malformed */ }
  return null;
}

function writeConsent(v: ConsentValue) {
  const val = encodeURIComponent(JSON.stringify(v));
  document.cookie = `${CONSENT_COOKIE}=${val}; Path=/; Max-Age=${CONSENT_MAX_AGE}; SameSite=Lax; Secure`;
}

/** Fire-and-forget consent log. Never throws, never blocks the UI. */
function logConsent(v: ConsentValue, source: Source) {
  try {
    void fetch("/api/consent", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...v, source }),
      keepalive: true,
    }).catch(() => {});
  } catch { /* ignore */ }
}

// ── Google Analytics (Consent Mode v2) ────────────────────────────────────────
// gtag is loaded ONLY after analytics consent (no hard-coded load). When it
// loads we set denied defaults then immediately grant analytics_storage.
function initGtagConsent(granted: boolean) {
  const w = window as unknown as { dataLayer?: unknown[]; gtag?: (...a: unknown[]) => void };
  w.dataLayer = w.dataLayer || [];
  function gtag(...args: unknown[]) { w.dataLayer!.push(args); }
  w.gtag = w.gtag || (gtag as (...a: unknown[]) => void);
  w.gtag("consent", "default", {
    ad_storage: "denied",
    ad_user_data: "denied",
    ad_personalization: "denied",
    analytics_storage: "denied",
  });
  if (granted) w.gtag("consent", "update", { analytics_storage: "granted" });
  w.gtag("js", new Date());
  w.gtag("config", GA_ID);
}

export function CookieConsent() {
  const [mounted, setMounted] = useState(false);
  const [open, setOpen] = useState(false);
  const [manage, setManage] = useState(false);
  const [analytics, setAnalytics] = useState(false);
  const [loadGa, setLoadGa] = useState(false);
  const idRef = useRef<string>("");
  const gpcRef = useRef<boolean>(false);

  const persist = useCallback((choice: Choice, source: Source) => {
    const value: ConsentValue = {
      id: idRef.current || crypto.randomUUID(),
      v: NOTICE_VERSION,
      ts: new Date().toISOString(),
      analytics: choice.analytics,
      advertising: false, // no ad script to gate today
      gpc: gpcRef.current,
    };
    idRef.current = value.id;
    writeConsent(value);
    logConsent(value, source);
    if (choice.analytics) setLoadGa(true); // gtag loads only after consent
    setOpen(false);
    setManage(false);
  }, []);

  // Post-hydration only — never in prerender.
  useEffect(() => {
    setMounted(true);
    const gpc = (navigator as unknown as { globalPrivacyControl?: boolean }).globalPrivacyControl === true;
    gpcRef.current = gpc;

    const existing = readConsent();
    if (existing && existing.v === NOTICE_VERSION) {
      idRef.current = existing.id;
      setAnalytics(existing.analytics);
      if (existing.analytics) setLoadGa(true);
      return; // valid current choice → no banner
    }

    // No valid choice yet. GPC present → default non-essential off, show banner
    // in "Necessary only" state, and log a gpc-default record so honoring the
    // signal is demonstrable (without writing a cookie, so the banner still shows).
    idRef.current = crypto.randomUUID();
    setAnalytics(false);
    if (gpc) {
      logConsent(
        { id: idRef.current, v: NOTICE_VERSION, ts: new Date().toISOString(), analytics: false, advertising: false, gpc: true },
        "gpc-default"
      );
    }
    setOpen(true);
  }, []);

  // Footer "Cookie settings" reopens the banner with current choices.
  useEffect(() => {
    function reopen() {
      const cur = readConsent();
      setAnalytics(cur?.analytics ?? false);
      if (cur?.id) idRef.current = cur.id;
      setManage(true);
      setOpen(true);
    }
    window.addEventListener("c2:open-consent", reopen);
    return () => window.removeEventListener("c2:open-consent", reopen);
  }, []);

  const deleteRecord = useCallback(() => {
    try {
      void fetch("/api/consent", { method: "DELETE", keepalive: true }).catch(() => {});
    } catch { /* ignore */ }
    document.cookie = `${CONSENT_COOKIE}=; Path=/; Max-Age=0; SameSite=Lax; Secure`;
    idRef.current = "";
    setAnalytics(false);
    setLoadGa(false);
    setManage(false);
    setOpen(true); // re-prompt with a fresh (necessary-only) state
  }, []);

  return (
    <>
      {loadGa && (
        <>
          <Script
            id="ga-loader"
            src={`https://www.googletagmanager.com/gtag/js?id=${GA_ID}`}
            strategy="afterInteractive"
            onLoad={() => initGtagConsent(analytics)}
          />
          {/* Ensure consent defaults/update run even if onLoad already fired. */}
          <Script id="ga-consent-init" strategy="afterInteractive">
            {`window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}window.gtag=window.gtag||gtag;
gtag('consent','default',{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied'});
gtag('consent','update',{analytics_storage:'granted'});
gtag('js',new Date());gtag('config','${GA_ID}');`}
          </Script>
        </>
      )}

      {mounted && open && (
        <div
          role="dialog"
          aria-label="Cookie consent"
          style={{
            position: "fixed", left: 0, right: 0, bottom: 0, zIndex: 50,
            background: "var(--brand-head)", borderTop: "1px solid var(--brand-line)",
            boxShadow: "0 -2px 12px rgba(0,0,0,0.06)", maxHeight: "34vh", overflowY: "auto",
          }}
        >
          <style>{`
            @media (max-width: 640px) {
              .c2-actions { width: 100%; flex-direction: column; align-items: stretch; }
              .c2-actions button { width: 100%; }
            }
          `}</style>
          <div style={{ maxWidth: 1100, margin: "0 auto", padding: "16px 20px" }}>
            <div style={{ display: "flex", flexWrap: "wrap", alignItems: "center", gap: 16, justifyContent: "space-between" }}>
              <div style={{ flex: "1 1 320px", minWidth: 260 }}>
                <p style={{ fontFamily: "var(--brand-font-head)", fontSize: 16, fontWeight: 600, color: "var(--brand-ink)", margin: "0 0 4px" }}>
                  Cookies on Checklist²
                </p>
                <p style={{ fontSize: 14, color: "var(--brand-slate)", lineHeight: 1.5, margin: 0 }}>
                  We use cookies for analytics and to remember your preferences.{" "}
                  <Link href="/privacy" style={{ color: "var(--brand-ink-soft)", textDecoration: "underline" }}>
                    Privacy Policy
                  </Link>
                </p>
              </div>

              <div className="c2-actions" style={{ display: "flex", flexWrap: "wrap", gap: 8, alignItems: "center" }}>
                <button onClick={() => setManage((m) => !m)} aria-expanded={manage} style={btnStyle("ghost")}>
                  Manage
                </button>
                <button onClick={() => persist({ analytics: false }, manage ? "settings" : "banner")} style={btnStyle("ghost")}>
                  Necessary only
                </button>
                <button onClick={() => persist({ analytics: true }, manage ? "settings" : "banner")} style={btnStyle("solid")}>
                  Accept all
                </button>
              </div>
            </div>

            {manage && (
              <div style={{ marginTop: 14, paddingTop: 14, borderTop: "1px solid var(--brand-line)" }}>
                <label style={{ display: "flex", alignItems: "center", gap: 10, cursor: "pointer" }}>
                  <input type="checkbox" checked={analytics} onChange={(e) => setAnalytics(e.target.checked)} />
                  <span style={{ fontSize: 14, color: "var(--brand-ink)" }}>
                    <strong>Analytics</strong> — anonymous usage measurement (Google Analytics). Off by default.
                  </span>
                </label>
                <div className="c2-actions" style={{ display: "flex", flexWrap: "wrap", gap: 8, marginTop: 12 }}>
                  <button onClick={() => persist({ analytics }, "settings")} style={btnStyle("solid")}>
                    Save choices
                  </button>
                  <button onClick={deleteRecord} style={btnStyle("ghost")}>
                    Delete my consent record
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </>
  );
}

function btnStyle(kind: "solid" | "ghost"): React.CSSProperties {
  const base: React.CSSProperties = {
    fontFamily: "var(--brand-font-body)", fontSize: 14, fontWeight: 600,
    padding: "9px 16px", borderRadius: 8, cursor: "pointer", whiteSpace: "nowrap",
    transition: "background 120ms ease, color 120ms ease",
  };
  if (kind === "solid") {
    return { ...base, background: "var(--brand-ink)", color: "var(--brand-head)", border: "1px solid var(--brand-ink)" };
  }
  return { ...base, background: "transparent", color: "var(--brand-ink)", border: "1px solid var(--brand-line)" };
}
