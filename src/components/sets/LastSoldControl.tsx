"use client";

import React, { useState } from "react";
import type { LastSoldSummary } from "./SetDetailClient";

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

type Phase = "button" | "loading" | "priced" | "no_sales" | "capped" | "error";

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

  async function fetchPrice() {
    if (phase === "loading") return;
    setPhase("loading");
    try {
      const res = await fetch("/api/sold-comps", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ set_id: setId, insert_set_id: insertSetId, card_number: cardNumber, player_id: playerId }),
      });
      const data = await res.json().catch(() => null);
      if (data?.status === "ok" && data.summary) {
        setSummary(data.summary as LastSoldSummary);
        setPhase("priced");
        onPriced?.();
      } else if (data?.status === "no_sales") {
        setPhase("no_sales");
      } else if (data?.status === "capped") {
        setPhase("capped");
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
    return (
      <span style={{ flexShrink: 0, textAlign: "right", lineHeight: 1.15 }} aria-label="Last sold price">
        {summary.url ? (
          <a href={summary.url} target="_blank" rel="nofollow noopener"
            style={{ fontFamily: FONT_MONO, fontSize: 13, fontWeight: 700, color: "var(--brand-ink)", textDecoration: "none", whiteSpace: "nowrap" }}>
            {priceLabel(summary.priceCents)} <span style={{ fontWeight: 500, color: "var(--brand-slate)" }}>last sold</span>
          </a>
        ) : (
          <span style={{ fontFamily: FONT_MONO, fontSize: 13, fontWeight: 700, color: "var(--brand-ink)", whiteSpace: "nowrap" }}>
            {priceLabel(summary.priceCents)} <span style={{ fontWeight: 500, color: "var(--brand-slate)" }}>last sold</span>
          </span>
        )}
        <span style={{ display: "block", fontFamily: FONT_MONO, fontSize: 9, color: "var(--brand-slate)" }}>{meta}</span>
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

  if (phase === "capped") {
    return (
      <span style={{ ...chipBase, color: "var(--brand-slate)", background: "var(--brand-track)", border: "1px solid var(--brand-line)" }}
        title="Daily pricing limit reached — try again tomorrow">
        Pricing paused today
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

  // "button" and "error" are both retryable clicks.
  return (
    <button type="button" onClick={fetchPrice}
      style={{
        ...chipBase, cursor: "pointer",
        color: phase === "error" ? "var(--brand-accent-deep)" : "var(--brand-slate)",
        background: "var(--brand-track)", border: "1px solid var(--brand-line)",
      }}
      aria-label={phase === "error" ? "Couldn't price this card — retry" : "Show last sold price"}>
      {phase === "error" ? "Couldn't price this card" : "Last sold"}
    </button>
  );
}
