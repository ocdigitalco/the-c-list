"use client";

import React, { useState, useEffect } from "react";
import type { LastSoldSummary } from "./SetDetailClient";

// One sentence shown on the "i" of a rate-limited row.
const RATE_LIMIT_TIP = "Prices come from recent eBay sales and are rate-limited to keep lookups fair.";

const FONT_MONO = "var(--cl-font-mono), 'JetBrains Mono', ui-monospace, monospace";
const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

/** "2026-09-27" → "Sep 27" (string-parsed; no timezone shift). */
function shortDate(soldAt: string | null): string {
  if (!soldAt) return "";
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(soldAt);
  if (!m) return soldAt;
  const mon = MONTHS[Number(m[2]) - 1] ?? "";
  return `${mon} ${Number(m[3])}`.trim();
}

function priceLabel(cents: number): string {
  return `$${Math.round(cents / 100).toLocaleString("en-US")}`;
}

/** Price-basis explanation for the "i" tooltip, or null when the sale type is unknown. */
function basisText(type: LastSoldSummary["type"], boaHydrated?: number | null): string | null {
  switch (type) {
    case "best_offer":
      return boaHydrated === 1
        ? "Best Offer sale. Price shown is the accepted offer."
        : "Best Offer sale. eBay didn't report the accepted amount, so the listed price is shown; the actual sale may have been lower.";
    case "auction": return "Final auction price.";
    case "bin": return "Buy It Now price.";
    default: return null;
  }
}

type Phase = "button" | "loading" | "priced" | "no_sales" | "ip_limit" | "daily_cap" | "upstream_error" | "error";

// Right-cluster "Last sold" control for a checklist row. State 1 is a compact
// chip-height button; State 2 is a two-line price block. The fetch happens ONLY
// on click (never on load/hover/tab switch); page-load summaries arrive via props.
export function LastSoldControl({
  setId, insertSetId, cardNumber, playerId, initial, onPriced,
}: {
  setId: number; insertSetId: number; cardNumber: string; playerId: number;
  initial?: LastSoldSummary | null;
  onPriced?: () => void;
}) {
  const [phase, setPhase] = useState<Phase>(initial?.priceCents != null ? "priced" : "button");
  const [summary, setSummary] = useState<LastSoldSummary | null>(initial ?? null);
  const [tipOpen, setTipOpen] = useState(false); // tap-to-toggle for touch (hover uses title)
  // When a limit was hit, the ms-timestamp the control re-enables itself at.
  const [reEnableAt, setReEnableAt] = useState<number | null>(null);

  // Auto re-enable after a rate-limit window elapses (ip_limit: retryAfterSeconds;
  // daily_cap: resetsAt). Nothing is persisted — a reload resets to the button.
  useEffect(() => {
    if ((phase !== "ip_limit" && phase !== "daily_cap") || reEnableAt == null) return;
    const ms = reEnableAt - Date.now();
    if (ms <= 0) { setPhase("button"); setReEnableAt(null); return; }
    const t = setTimeout(() => { setPhase("button"); setReEnableAt(null); }, ms);
    return () => clearTimeout(t);
  }, [phase, reEnableAt]);

  async function fetchPrice() {
    if (phase === "loading") return;
    setPhase("loading");
    try {
      const res = await fetch("/api/sold-comps", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ set_id: setId, insert_set_id: insertSetId, card_number: cardNumber, player_id: playerId }),
      });
      // The body carries the outcome even on 429/502/503, so we key on `reason`
      // (falling back to `status`), not the HTTP status.
      const data = await res.json().catch(() => null);
      const reason: string | undefined = data?.reason;
      if (data?.status === "ok" && data.summary) {
        setSummary(data.summary as LastSoldSummary);
        setPhase("priced");
        onPriced?.();
      } else if (data?.status === "no_sales") {
        setPhase("no_sales");
      } else if (reason === "ip_limit") {
        const secs = Number(data?.retryAfterSeconds);
        setReEnableAt(Date.now() + (Number.isFinite(secs) && secs > 0 ? secs : 3600) * 1000);
        setPhase("ip_limit");
      } else if (reason === "daily_cap") {
        const t = data?.resetsAt ? Date.parse(data.resetsAt) : NaN;
        setReEnableAt(Number.isFinite(t) ? t : null);
        setPhase("daily_cap");
      } else if (reason === "upstream_error") {
        setPhase("upstream_error");
      } else {
        setPhase("error");
      }
    } catch {
      setPhase("error");
    }
  }

  const chipBase: React.CSSProperties = {
    flexShrink: 0, fontFamily: FONT_MONO, fontSize: 10, fontWeight: 700, letterSpacing: 0.3,
    lineHeight: "16px", padding: "1px 7px", borderRadius: 3, whiteSpace: "nowrap", textAlign: "right",
  };

  if (phase === "priced" && summary) {
    const meta = `${shortDate(summary.soldAt)}${summary.soldAt ? " · " : ""}raw`;
    const tip = basisText(summary.type, summary.boaHydrated);
    return (
      <span style={{ flexShrink: 0, textAlign: "right", lineHeight: 1.15, position: "relative" }} aria-label="Last sold price">
        {/* Price is ALWAYS plain text (never the affiliate link). */}
        <span style={{ fontFamily: FONT_MONO, fontSize: 13, fontWeight: 700, color: "var(--brand-ink)", whiteSpace: "nowrap" }}>
          {priceLabel(summary.priceCents)} <span style={{ fontWeight: 500, color: "var(--brand-slate)" }}>last sold</span>
        </span>
        {tip && (
          <button type="button" aria-label={tip} title={tip}
            onClick={() => setTipOpen((o) => !o)} onBlur={() => setTipOpen(false)}
            style={{
              marginLeft: 4, cursor: "help", border: "none", background: "transparent", padding: 0,
              fontFamily: FONT_MONO, fontSize: 10, fontWeight: 700, color: "var(--brand-slate)", verticalAlign: "middle",
            }}>ⓘ</button>
        )}
        <span style={{ display: "block", fontFamily: FONT_MONO, fontSize: 9, color: "var(--brand-slate)" }}>{meta}</span>
        {summary.url && (
          <a href={summary.url} target="_blank" rel="nofollow noopener sponsored"
            style={{ display: "block", fontFamily: FONT_MONO, fontSize: 10, fontWeight: 600, color: "var(--brand-accent-deep)", textDecoration: "none", whiteSpace: "nowrap" }}>
            View on eBay ↗
          </a>
        )}
        {tip && tipOpen && (
          <span role="tooltip" style={{
            position: "absolute", top: "100%", right: 0, zIndex: 20, marginTop: 4, maxWidth: 240, width: "max-content",
            textAlign: "left", whiteSpace: "normal", fontFamily: FONT_MONO, fontSize: 10, lineHeight: 1.3,
            color: "var(--brand-ink)", background: "var(--brand-card)", border: "1px solid var(--brand-line)",
            borderRadius: 6, padding: "6px 8px", boxShadow: "0 4px 12px rgba(0,0,0,0.12)",
          }}>{tip}</span>
        )}
      </span>
    );
  }

  if (phase === "loading") {
    return (
      <span style={{ ...chipBase, color: "var(--brand-slate)", background: "var(--brand-track)", border: "1px solid var(--brand-line)" }}
        aria-label="Pricing…" aria-busy="true">
        <span className="animate-pulse">pricing…</span>
      </span>
    );
  }

  // A rate-limited row: the reason-specific message, disabled until it re-enables,
  // with an "i" explaining the limit in one sentence.
  if (phase === "ip_limit" || phase === "daily_cap") {
    const message = phase === "ip_limit"
      ? "Pricing limit reached — try again in about an hour"
      : "Daily pricing budget used — back tomorrow";
    return (
      <span style={{ ...chipBase, position: "relative", color: "var(--brand-slate)", background: "var(--brand-track)", border: "1px solid var(--brand-line)" }}
        title={message}>
        {message}
        <button type="button" aria-label={RATE_LIMIT_TIP} title={RATE_LIMIT_TIP}
          onClick={() => setTipOpen((o) => !o)} onBlur={() => setTipOpen(false)}
          style={{
            marginLeft: 4, cursor: "help", border: "none", background: "transparent", padding: 0,
            fontFamily: FONT_MONO, fontSize: 10, fontWeight: 700, color: "var(--brand-slate)", verticalAlign: "middle",
          }}>ⓘ</button>
        {tipOpen && (
          <span role="tooltip" style={{
            position: "absolute", top: "100%", right: 0, zIndex: 20, marginTop: 4, maxWidth: 240, width: "max-content",
            textAlign: "left", whiteSpace: "normal", fontFamily: FONT_MONO, fontSize: 10, lineHeight: 1.3,
            color: "var(--brand-ink)", background: "var(--brand-card)", border: "1px solid var(--brand-line)",
            borderRadius: 6, padding: "6px 8px", boxShadow: "0 4px 12px rgba(0,0,0,0.12)",
          }}>{RATE_LIMIT_TIP}</span>
        )}
      </span>
    );
  }

  if (phase === "no_sales") {
    return (
      <span style={{ ...chipBase, color: "var(--brand-slate)", background: "var(--brand-track)", border: "1px solid var(--brand-line)" }}>
        No recent sales
      </span>
    );
  }

  // "button", "error" and "upstream_error" are all retryable clicks.
  const isError = phase === "error" || phase === "upstream_error";
  const label = phase === "upstream_error"
    ? "Pricing unavailable right now"
    : phase === "error" ? "Couldn't price this card" : "Last sold";
  const aria = phase === "upstream_error"
    ? "Pricing unavailable right now — retry"
    : phase === "error" ? "Couldn't price this card — retry" : "Show last sold price";
  return (
    <button type="button" onClick={fetchPrice}
      style={{
        ...chipBase, cursor: "pointer",
        color: isError ? "var(--brand-accent-deep)" : "var(--brand-slate)",
        background: "var(--brand-track)", border: "1px solid var(--brand-line)",
      }}
      aria-label={aria}>
      {label}
    </button>
  );
}
