import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Privacy Policy — Checklist2",
  description: "Privacy Policy for Checklist2",
};

export default function PrivacyPage() {
  return (
    <div className="flex-1">
      <div className="max-w-3xl mx-auto px-6 py-10 space-y-10">
        {/* Header */}
        <div>
          <h1 className="text-2xl font-normal text-[var(--brand-ink)] tracking-tight mb-2" style={{ fontFamily: "var(--brand-font-head)", fontSynthesisWeight: "none" }}>Privacy Policy</h1>
          <p className="text-xs text-[var(--brand-slate)]">Effective Date: March 2026</p>
        </div>

        <Section title="Introduction">
          <p>
            Checklist2 (&quot;we&quot;, &quot;us&quot;, &quot;our&quot;) is committed to
            transparency about how we collect and use information. This Privacy Policy explains
            our practices.
          </p>
        </Section>

        <Section title="Information We Collect">
          <ul className="space-y-2">
            {[
              "Usage data: pages viewed, athletes searched, sets explored, features used",
              "Device and browser information: browser type, operating system, screen size",
              "Referring URLs and general location data (country/region level)",
              "Any information voluntarily submitted through feedback or contact forms",
            ].map((item) => (
              <li key={item} className="flex items-start gap-2">
                <span className="shrink-0 text-[var(--brand-slate)] mt-0.5">--</span>
                {item}
              </li>
            ))}
          </ul>
        </Section>

        <Section title="How We Use Your Information">
          <ul className="space-y-2">
            {[
              "To operate and improve the Checklist2 platform",
              "To analyze usage patterns and feature popularity",
              "To inform product and feature development",
              "To generate aggregated insights about collector and breaker interest",
              "For commercial purposes including sharing or selling anonymized data to third parties as described in our Terms of Use",
            ].map((item) => (
              <li key={item} className="flex items-start gap-2">
                <span className="shrink-0 text-[var(--brand-slate)] mt-0.5">--</span>
                {item}
              </li>
            ))}
          </ul>
        </Section>

        <Section title="Cookies and Tracking">
          <p>
            Checklist2 may use cookies or local storage to remember your preferences (such as
            light/dark mode). We may use analytics tools to understand how the app is used. By
            using the app you consent to this use.
          </p>
        </Section>

        <Section title="Third Party Sharing">
          <p>
            We may share anonymized or aggregated usage data with third parties including
            advertising partners, card industry partners, and data buyers. We do not sell
            personally identifiable information unless you have explicitly provided it and
            consented to its sale.
          </p>
        </Section>

        <Section title="Data Retention">
          <p>
            We retain usage data for as long as necessary to operate and improve the platform.
          </p>
        </Section>

        <Section title="Your Choices">
          <p>
            You may stop using Checklist2 at any time. As no account is required, there is no
            personal profile to delete. If you have submitted personal information and wish it
            removed, contact us at{" "}
            <span className="text-[var(--brand-ink-soft)]">[contact email placeholder]</span>.
          </p>
        </Section>

        <Section title="Children's Privacy">
          <p>
            Checklist2 is not directed at children under 13. We do not knowingly collect data
            from children under 13.
          </p>
        </Section>

        <Section title="Security">
          <p>
            We take reasonable measures to protect the data we collect. However no system is
            completely secure and we cannot guarantee absolute security.
          </p>
        </Section>

        <Section title="Changes to This Policy">
          <p>
            We may update this Privacy Policy at any time. Continued use of the app after changes
            constitutes acceptance of the updated policy.
          </p>
        </Section>

        <Section title="Contact">
          <p>
            For privacy questions contact us at{" "}
            <span className="text-[var(--brand-ink-soft)]">[contact email placeholder]</span>.
          </p>
        </Section>

        <div className="pt-2 pb-4">
          <Link
            href="/terms"
            className="text-sm text-[var(--brand-slate)] hover:text-[var(--brand-ink-soft)] transition-colors"
          >
            View Terms of Use
          </Link>
        </div>
      </div>
    </div>
  );
}

function Section({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <section>
      <h2 className="text-base font-semibold text-[var(--brand-ink)] mb-3 pb-2 border-b border-[var(--brand-line)]">
        {title}
      </h2>
      <div className="text-sm text-[var(--brand-ink-soft)] leading-relaxed space-y-3">{children}</div>
    </section>
  );
}
