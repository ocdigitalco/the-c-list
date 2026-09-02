"use client";

import { useId, useState } from "react";
import { Button } from "@/components/Button";

/**
 * Newsletter subscribe form → POST /api/subscribe → Resend Audience.
 * Self-contained: email input + Subscribe button, hidden honeypot, inline
 * success/error states. Uses only --brand-* tokens; compact enough for the
 * footer, and reused in a card on /updates. useId() keeps field ids unique so
 * multiple instances (footer + page) can coexist on one route.
 */
export function NewsletterSignup() {
  const uid = useId();
  const emailId = `nl-email-${uid}`;
  const hpId = `nl-website-${uid}`;
  const errId = `nl-error-${uid}`;

  const [email, setEmail] = useState("");
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
      const res = await fetch("/api/subscribe", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, website }),
      });
      if (res.ok) {
        setSuccess(true);
        return;
      }
      const data = await res.json().catch(() => ({}));
      if (res.status === 400 && data.errors?.email) {
        setError(data.errors.email as string);
      } else if (res.status === 429) {
        setError(data.error ?? "Too many requests. Please try again shortly.");
      } else {
        setError(data.error ?? "Something went wrong. Please try again later.");
      }
    } catch {
      setError("We couldn't reach the server. Please try again.");
    } finally {
      setSubmitting(false);
    }
  }

  if (success) {
    return (
      <p
        role="status"
        aria-live="polite"
        style={{ fontSize: 14, color: "var(--brand-ok)", fontWeight: 600, margin: 0 }}
      >
        You&rsquo;re on the list.
      </p>
    );
  }

  return (
    <form onSubmit={handleSubmit} noValidate>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 8, alignItems: "flex-start" }}>
        <label htmlFor={emailId} className="sr-only" style={srOnly}>
          Email address
        </label>
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
            flex: "1 1 180px",
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

        {/* Honeypot: off-screen, out of a11y tree + tab order. */}
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

        <Button variant="pri" type="submit" disabled={submitting}>
          {submitting ? "…" : "Subscribe"}
        </Button>
      </div>

      {error && (
        <p id={errId} style={{ fontSize: 13, color: "var(--brand-accent)", marginTop: 6 }}>
          {error}
        </p>
      )}
    </form>
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
