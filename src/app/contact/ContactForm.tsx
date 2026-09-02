"use client";

import { useState } from "react";
import { Button } from "@/components/Button";

type FieldErrors = Partial<Record<"name" | "email" | "message", string>>;

const labelStyle: React.CSSProperties = {
  display: "block",
  fontSize: 13,
  fontWeight: 600,
  color: "var(--brand-ink)",
  marginBottom: 6,
};

const controlStyle: React.CSSProperties = {
  width: "100%",
  fontFamily: "var(--brand-font-body)",
  fontSize: 15,
  color: "var(--brand-ink)",
  background: "var(--brand-field)",
  border: "1px solid var(--brand-line)",
  borderRadius: "var(--brand-radius-control)",
  padding: "10px 12px",
};

export function ContactForm() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [subject, setSubject] = useState("");
  const [message, setMessage] = useState("");
  const [website, setWebsite] = useState(""); // honeypot

  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({});

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (submitting) return;
    setSubmitting(true);
    setFormError(null);
    setFieldErrors({});

    try {
      const res = await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, subject, message, website }),
      });

      if (res.ok) {
        setSuccess(true);
        return;
      }

      const data = await res.json().catch(() => ({}));
      if (res.status === 400 && data.errors) {
        setFieldErrors(data.errors as FieldErrors);
        setFormError("Please fix the highlighted fields and try again.");
      } else if (res.status === 429) {
        setFormError(
          data.error ?? "Too many submissions. Please try again in a few minutes."
        );
      } else {
        setFormError(
          data.error ?? "Something went wrong. Please try again later."
        );
      }
    } catch {
      setFormError(
        "We couldn't reach the server. Please check your connection and try again."
      );
    } finally {
      setSubmitting(false);
    }
  }

  if (success) {
    return (
      <div
        role="status"
        aria-live="polite"
        style={{
          background: "var(--brand-card)",
          border: "1px solid var(--brand-line)",
          borderRadius: "var(--brand-radius-panel)",
          padding: "28px 24px",
          maxWidth: 640,
        }}
      >
        <h2
          style={{
            fontFamily: "var(--brand-font-head)",
            fontWeight: 400,
            fontSynthesisWeight: "none",
            fontSize: 24,
            color: "var(--brand-ink)",
            margin: "0 0 8px",
          }}
        >
          Thanks — message sent.
        </h2>
        <p style={{ fontSize: 15, color: "var(--brand-slate)", margin: 0, lineHeight: 1.6 }}>
          Your message is on its way to the Checklist² team. We&rsquo;ll reply to the
          email address you provided as soon as we can.
        </p>
      </div>
    );
  }

  const errorTextStyle: React.CSSProperties = {
    fontSize: 13,
    color: "var(--brand-accent)",
    marginTop: 6,
  };

  return (
    <form onSubmit={handleSubmit} noValidate style={{ maxWidth: 640 }}>
      {formError && (
        <div
          role="alert"
          style={{
            fontSize: 14,
            color: "var(--brand-accent)",
            background: "var(--brand-card)",
            border: "1px solid var(--brand-line)",
            borderRadius: "var(--brand-radius-control)",
            padding: "10px 12px",
            marginBottom: 18,
          }}
        >
          {formError}
        </div>
      )}

      {/* Name */}
      <div style={{ marginBottom: 18 }}>
        <label htmlFor="contact-name" style={labelStyle}>
          Name
        </label>
        <input
          id="contact-name"
          name="name"
          type="text"
          required
          maxLength={100}
          autoComplete="name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          disabled={submitting}
          aria-invalid={fieldErrors.name ? true : undefined}
          aria-describedby={fieldErrors.name ? "contact-name-error" : undefined}
          style={controlStyle}
        />
        {fieldErrors.name && (
          <p id="contact-name-error" style={errorTextStyle}>
            {fieldErrors.name}
          </p>
        )}
      </div>

      {/* Email */}
      <div style={{ marginBottom: 18 }}>
        <label htmlFor="contact-email" style={labelStyle}>
          Email
        </label>
        <input
          id="contact-email"
          name="email"
          type="email"
          required
          maxLength={254}
          autoComplete="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          disabled={submitting}
          aria-invalid={fieldErrors.email ? true : undefined}
          aria-describedby={fieldErrors.email ? "contact-email-error" : undefined}
          style={controlStyle}
        />
        {fieldErrors.email && (
          <p id="contact-email-error" style={errorTextStyle}>
            {fieldErrors.email}
          </p>
        )}
      </div>

      {/* Subject (optional) */}
      <div style={{ marginBottom: 18 }}>
        <label htmlFor="contact-subject" style={labelStyle}>
          Subject{" "}
          <span style={{ fontWeight: 400, color: "var(--brand-slate)" }}>
            (optional)
          </span>
        </label>
        <input
          id="contact-subject"
          name="subject"
          type="text"
          maxLength={150}
          value={subject}
          onChange={(e) => setSubject(e.target.value)}
          disabled={submitting}
          style={controlStyle}
        />
      </div>

      {/* Message */}
      <div style={{ marginBottom: 18 }}>
        <label htmlFor="contact-message" style={labelStyle}>
          Message
        </label>
        <textarea
          id="contact-message"
          name="message"
          required
          minLength={10}
          maxLength={5000}
          rows={7}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          disabled={submitting}
          aria-invalid={fieldErrors.message ? true : undefined}
          aria-describedby={fieldErrors.message ? "contact-message-error" : undefined}
          style={{ ...controlStyle, resize: "vertical" as const, lineHeight: 1.5 }}
        />
        {fieldErrors.message && (
          <p id="contact-message-error" style={errorTextStyle}>
            {fieldErrors.message}
          </p>
        )}
      </div>

      {/* Honeypot: visually hidden, off-screen, hidden from a11y tree + tab order.
          Real users never see or fill this; bots that auto-fill it are silently
          dropped by the API. */}
      <div
        aria-hidden="true"
        style={{
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
        }}
      >
        <label htmlFor="contact-website">Leave this field empty</label>
        <input
          id="contact-website"
          name="website"
          type="text"
          tabIndex={-1}
          autoComplete="off"
          value={website}
          onChange={(e) => setWebsite(e.target.value)}
        />
      </div>

      <Button variant="pri" type="submit" disabled={submitting}>
        {submitting ? "Sending…" : "Send message"}
      </Button>
    </form>
  );
}
