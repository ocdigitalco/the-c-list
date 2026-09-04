"use client";

import { useId, useState } from "react";
import { Button } from "@/components/Button";
import { trackEvent } from "@/lib/analytics";

/**
 * "Notify me when odds are published" — shown only on set pages whose pack odds
 * are not yet published. Email-only (no account). POSTs to /api/alerts, which
 * stores the address against the set and (optionally) opts it into the weekly
 * newsletter. One email is sent per subscriber when odds are attached.
 */
export function SetOddsAlertForm({ setSlug }: { setSlug: string }) {
  const uid = useId();
  const emailId = `oa-email-${uid}`;
  const hpId = `oa-website-${uid}`;
  const nlId = `oa-news-${uid}`;
  const errId = `oa-error-${uid}`;

  const [email, setEmail] = useState("");
  const [newsletter, setNewsletter] = useState(false);
  const [website, setWebsite] = useState(""); // honeypot
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (submitting) return;
    setSubmitting(true);
    setError(null);
    try {
      const res = await fetch("/api/alerts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, setSlug, newsletter, website }),
      });
      if (res.ok) {
        trackEvent("odds_alert_signup", { set_slug: setSlug, newsletter });
        setSuccess(true);
        return;
      }
      const data = await res.json().catch(() => ({}));
      if (res.status === 400 && data.errors?.email) setError(data.errors.email as string);
      else if (res.status === 404) setError("This set could not be found.");
      else if (res.status === 429) setError(data.error ?? "Too many requests. Please try again shortly.");
      else setError(data.error ?? "Something went wrong. Please try again later.");
    } catch {
      setError("We couldn't reach the server. Please try again.");
    } finally {
      setSubmitting(false);
    }
  }

  const wrap: React.CSSProperties = {
    background: "var(--brand-card)",
    border: "1px solid var(--brand-line)",
    borderRadius: "var(--brand-radius-panel, 12px)",
    padding: "20px 22px",
    fontFamily: "var(--brand-font-body)",
  };

  if (success) {
    return (
      <div style={wrap} role="status" aria-live="polite">
        <p style={{ fontSize: 15, fontWeight: 600, color: "var(--brand-ok)", margin: 0 }}>
          You&rsquo;re on the list.
        </p>
        <p style={{ fontSize: 14, color: "var(--brand-slate)", margin: "6px 0 0", lineHeight: 1.6 }}>
          We&rsquo;ll email you once Topps publishes pack odds for this set.
        </p>
      </div>
    );
  }

  return (
    <div style={wrap}>
      <h2 style={{ fontSize: 17, fontWeight: 700, color: "var(--brand-ink)", margin: "0 0 4px" }}>
        Odds not published yet
      </h2>
      <p style={{ fontSize: 14, color: "var(--brand-slate)", margin: "0 0 14px", lineHeight: 1.6 }}>
        Topps hasn&rsquo;t released pack odds for this set. Get one email when they&rsquo;re added.
      </p>

      <form onSubmit={handleSubmit} noValidate>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 8, alignItems: "flex-start" }}>
          <label htmlFor={emailId} style={srOnly}>Email address</label>
          <input
            id={emailId}
            name="email"
            type="email"
            required
            maxLength={254}
            autoComplete="email"
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            disabled={submitting}
            aria-invalid={error ? true : undefined}
            aria-describedby={error ? errId : undefined}
            style={{
              flex: "1 1 200px",
              minWidth: 0,
              fontFamily: "var(--brand-font-body)",
              fontSize: 14,
              color: "var(--brand-ink)",
              background: "var(--brand-field)",
              border: "1px solid var(--brand-line)",
              borderRadius: "var(--brand-radius-control)",
              padding: "9px 12px",
            }}
          />

          {/* Honeypot */}
          <div aria-hidden="true" style={srOnly}>
            <label htmlFor={hpId}>Leave this field empty</label>
            <input
              id={hpId}
              name="website"
              type="text"
              tabIndex={-1}
              autoComplete="off"
              value={website}
              onChange={(e) => setWebsite(e.target.value)}
            />
          </div>

          <Button variant="pri" size="md" type="submit" disabled={submitting}>
            {submitting ? "…" : "Notify me"}
          </Button>
        </div>

        <label
          htmlFor={nlId}
          style={{ display: "flex", alignItems: "center", gap: 8, marginTop: 12, fontSize: 13.5, color: "var(--brand-slate)", cursor: "pointer" }}
        >
          <input
            id={nlId}
            type="checkbox"
            checked={newsletter}
            onChange={(e) => setNewsletter(e.target.checked)}
            disabled={submitting}
            style={{ width: 15, height: 15, accentColor: "var(--brand-accent)" }}
          />
          Also send me the weekly Checklist² newsletter
        </label>

        {error && (
          <p id={errId} style={{ fontSize: 13, color: "var(--brand-accent)", marginTop: 10 }}>
            {error}
          </p>
        )}
      </form>
    </div>
  );
}

const srOnly: React.CSSProperties = {
  position: "absolute",
  width: 1,
  height: 1,
  overflow: "hidden",
  clip: "rect(0 0 0 0)",
  clipPath: "inset(50%)",
  whiteSpace: "nowrap",
  border: 0,
  padding: 0,
  margin: -1,
};
