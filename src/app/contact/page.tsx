import type { Metadata } from "next";
import { ContactForm } from "./ContactForm";

export const metadata: Metadata = {
  title: "Contact — Checklist2",
  description:
    "Get in touch with the Checklist² team — questions, corrections, feedback, or partnership inquiries.",
};

export default function ContactPage() {
  return (
    <div className="flex-1" style={{ background: "var(--brand-page)" }}>
      <div className="page-container" style={{ paddingTop: 40, paddingBottom: 80 }}>
        {/* Standard container; the content column is constrained and centered
            within it so the form reads as intentionally placed on wide viewports. */}
        <div style={{ maxWidth: 600, marginInline: "auto" }}>
          <h1 className="page-title" style={{ margin: 0 }}>
            Contact
          </h1>
          <p
            style={{
              fontSize: 15,
              color: "var(--brand-slate)",
              lineHeight: 1.6,
              margin: "12px 0 32px",
            }}
          >
            Questions, corrections, feedback, or partnership inquiries — send a note and
            we&rsquo;ll get back to you by email.
          </p>

          <ContactForm />
        </div>
      </div>
    </div>
  );
}
