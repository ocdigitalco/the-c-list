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
          <p className="text-xs text-[var(--brand-slate)]">Effective date: September 13, 2026</p>
          <p className="text-xs text-[var(--brand-slate)] mt-1">Previous version: March 2026</p>
          <p className="text-sm text-[var(--brand-ink-soft)] leading-relaxed mt-4">
            <strong>What changed in this version:</strong> we added a cookie consent banner and a
            consent log, and expanded this policy to cover email subscriptions, the service
            providers we use, the legal bases for processing, and the rights available to visitors
            in the EU/UK and California.
          </p>
        </div>

        <Section title="Who we are">
          <p>
            Checklist² (checklist2.com) is operated by Tyler Lawrence, a sole proprietor based in
            Orange County, California, USA (&quot;Checklist2&quot;, &quot;we&quot;, &quot;us&quot;,
            &quot;our&quot;). We are the controller of the personal data described in this policy.
          </p>
          <p>
            For any privacy question or request, contact <strong>privacy@checklist2.com</strong>.
          </p>
        </Section>

        <Section title="The short version">
          <ul className="space-y-2">
            {[
              "You can use the entire site without an account and without accepting any non-essential cookies.",
              "Analytics runs only if you turn it on in the cookie banner.",
              "If you subscribe to set alerts or the newsletter, we keep your email address to send you what you asked for, and you can unsubscribe at any time.",
              "We do not sell personal information.",
            ].map((item) => (
              <li key={item} className="flex items-start gap-2">
                <span className="shrink-0 text-[var(--brand-slate)] mt-0.5">--</span>
                {item}
              </li>
            ))}
          </ul>
        </Section>

        <Section title="Information we collect">
          <p className="font-semibold text-[var(--brand-ink)]">Information you give us</p>
          <ul className="space-y-2">
            <li className="flex items-start gap-2">
              <span className="shrink-0 text-[var(--brand-slate)] mt-0.5">--</span>
              <span><em>Email address</em>, if you subscribe to set alerts or the weekly newsletter through the signup forms on the site. We also record which page or set you signed up from, so we can send you the right alerts.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="shrink-0 text-[var(--brand-slate)] mt-0.5">--</span>
              <span><em>Anything you send us</em> through the contact or feedback forms or by email.</span>
            </li>
          </ul>
          <p className="font-semibold text-[var(--brand-ink)] mt-4">Information collected automatically</p>
          <ul className="space-y-2">
            <li className="flex items-start gap-2">
              <span className="shrink-0 text-[var(--brand-slate)] mt-0.5">--</span>
              <span><em>Analytics data, only with your consent.</em> If you enable Analytics in the cookie banner, Google Analytics collects pages viewed, sets and athletes explored, features used, approximate location (country or region), browser type, operating system, and screen size, and the site that referred you. This data is pseudonymous: it is tied to a random client identifier in a cookie, not to your name or email, and Google Analytics 4 does not store IP addresses. If you do not enable Analytics, none of this is collected.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="shrink-0 text-[var(--brand-slate)] mt-0.5">--</span>
              <span><em>Hosting and security logs.</em> Our hosting provider records standard server logs (including IP address, requested URL, and user agent) for a short period to operate the service and protect it from abuse. We do not use these logs to identify or profile visitors.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="shrink-0 text-[var(--brand-slate)] mt-0.5">--</span>
              <span><em>Your cookie choice</em>, as described under &quot;Cookies and consent&quot; below.</span>
            </li>
          </ul>
          <p>
            We do not collect payment information, and we do not require or offer user accounts.
          </p>
        </Section>

        <Section title="How we use your information and on what legal basis">
          <PolicyTable
            headers={["Purpose", "Data used", "Legal basis (GDPR)"]}
            rows={[
              ["Sending set alerts and the newsletter you subscribed to", "Email address, signup source", "Consent (Art. 6(1)(a)) — withdraw by unsubscribing"],
              ["Responding to your messages", "Whatever you send us", "Legitimate interest in replying to you (Art. 6(1)(f))"],
              ["Understanding how the site is used and improving it", "Analytics data", "Consent (Art. 6(1)(a)) — given via the cookie banner"],
              ["Keeping the site running and secure", "Hosting and security logs", "Legitimate interest in operating a secure service (Art. 6(1)(f))"],
              ["Remembering and demonstrating your cookie choice", <><code>c2_consent</code> cookie and the consent log</>, "Legal obligation to be able to demonstrate consent (Art. 6(1)(c)) and legitimate interest (Art. 6(1)(f))"],
              ["Producing aggregated statistics about collector and breaker interest", "Analytics data, aggregated so that no individual can be identified", "Legitimate interest (Art. 6(1)(f)); aggregated statistics are not personal data"],
            ]}
          />
        </Section>

        <Section title="Cookies and consent">
          <p>
            When you first visit, a non-blocking banner lets you choose which cookies we may use.
            Cookies fall into two categories:
          </p>
          <ul className="space-y-2 mt-3">
            <li className="flex items-start gap-2">
              <span className="shrink-0 text-[var(--brand-slate)] mt-0.5">--</span>
              <span><strong>Strictly necessary</strong> — required for the site to function and to remember your cookie choice itself. These are always on and cannot be turned off.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="shrink-0 text-[var(--brand-slate)] mt-0.5">--</span>
              <span><strong>Analytics</strong> — pseudonymous usage measurement via Google Analytics, which helps us understand how the site is used. Off by default; loaded only if you turn it on. We use Google Consent Mode v2 with denied defaults, so no analytics cookies are set until you consent.</span>
            </li>
          </ul>
          <p className="mt-3">
            There is currently no advertising or ad-targeting cookie on the site. Your choice is
            stored in a single first-party cookie named <code>c2_consent</code> for 12 months
            (<code>SameSite=Lax</code>, <code>Secure</code>). It holds a random identifier, the
            notice version, a timestamp, your category choices, and whether your browser sent a
            Global Privacy Control (GPC) signal. If GPC is present we default analytics off. You
            can change or withdraw your choice at any time via Cookie settings in the footer.
            Rejecting analytics is as easy as accepting it: the banner offers &quot;Accept all&quot;
            and &quot;Reject all&quot; side by side, and we will not show the banner again for 12
            months whichever you choose.
          </p>
        </Section>

        <Section title="Consent log">
          <p>
            To be able to demonstrate that consent was given, we keep a minimal, non-identifying
            record of each choice. Each entry stores only: the random consent identifier from your{" "}
            <code>c2_consent</code> cookie, a timestamp, the notice version, your analytics and
            advertising choices, whether a GPC signal was present, and whether the choice came from
            the banner, the settings panel, or a GPC default.
          </p>
          <p>
            The consent log deliberately does not store your IP address, user agent, device or
            browser details, geolocation, referring URL, or any request headers. Records are
            automatically deleted after 24 months. Because the identifier is random and unlinked to
            any personal data, these entries are not tied to your identity.
          </p>
          <p>
            You can delete your consent record at any time: open Cookie settings in the footer and
            choose Delete my consent record. This removes all log entries for your consent
            identifier and clears the <code>c2_consent</code> cookie.
          </p>
        </Section>

        <Section title="Email subscriptions">
          <p>
            If you subscribe to set alerts or the weekly newsletter, we store your email address
            and the page or set you signed up from. We use this only to send you the alerts and
            issues you asked for, and to let you manage which topics you receive. Every email
            includes an unsubscribe link, and you can also unsubscribe by writing to
            privacy@checklist2.com. When you unsubscribe from everything, we delete your address
            from our mailing list.
          </p>
          <p>
            We do not share subscriber email addresses with anyone other than the email delivery
            provider listed below, and we do not use them for advertising.
          </p>
        </Section>

        <Section title="Service providers">
          <p>
            We use the following companies to run the site. Each acts as a processor on our behalf,
            under a contract, and may only use the data to provide its service to us.
          </p>
          <PolicyTable
            headers={["Provider", "What it does", "Data it handles"]}
            rows={[
              ["Vercel", "Hosts the website", "Hosting and security logs"],
              ["Turso", "Hosts our database", "Consent log entries; no visitor identities"],
              ["Resend", "Sends set alerts, newsletters, and contact-form messages", "Email addresses and signup source"],
              ["Google (Google Analytics 4)", "Usage analytics, only with your consent", "Pseudonymous analytics data"],
            ]}
          />
          <p>
            These providers are based in, or process data in, the United States. For visitors in
            the EU, UK, and Switzerland, transfers to these providers rely on their certification
            under the EU–US Data Privacy Framework (and its UK and Swiss extensions), supplemented
            by standard contractual clauses where applicable.
          </p>
        </Section>

        <Section title="Sharing of information">
          <p>
            We may publish or share <strong>aggregated statistics</strong> — for example, which
            sets or athletes are drawing the most interest — with card-industry partners or the
            public. Aggregated statistics do not identify any individual and are not personal data.
          </p>
          <p>
            Beyond the service providers above, we do not share personal information with third
            parties, and we <strong>do not sell personal information</strong>. We would disclose
            personal information only if required by law, or to protect the rights, safety, or
            property of Checklist2 or others.
          </p>
        </Section>

        <Section title="Data retention">
          <ul className="space-y-2">
            <li className="flex items-start gap-2">
              <span className="shrink-0 text-[var(--brand-slate)] mt-0.5">--</span>
              <span><strong>Email addresses:</strong> until you unsubscribe from all topics, after which the address is deleted from our list.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="shrink-0 text-[var(--brand-slate)] mt-0.5">--</span>
              <span><strong>Analytics data:</strong> retained in Google Analytics for up to 14 months, then automatically deleted or aggregated.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="shrink-0 text-[var(--brand-slate)] mt-0.5">--</span>
              <span><strong>Consent log:</strong> 24 months, then automatically deleted; deletable earlier by you at any time.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="shrink-0 text-[var(--brand-slate)] mt-0.5">--</span>
              <span><strong>Cookie choice (<code>c2_consent</code>):</strong> 12 months on your device.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="shrink-0 text-[var(--brand-slate)] mt-0.5">--</span>
              <span><strong>Hosting and security logs:</strong> retained briefly by our hosting provider for operational and security purposes.</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="shrink-0 text-[var(--brand-slate)] mt-0.5">--</span>
              <span><strong>Messages you send us:</strong> for as long as needed to respond and for a reasonable period afterward.</span>
            </li>
          </ul>
        </Section>

        <Section title="Your rights">
          <p><strong>If you are in the EU, EEA, UK, or Switzerland</strong>, you have the right to:</p>
          <ul className="space-y-2">
            {[
              "ask what personal data we hold about you and receive a copy (access);",
              "have inaccurate data corrected (rectification);",
              "have your data deleted (erasure);",
              "restrict or object to processing based on legitimate interest;",
              "receive the data you gave us in a portable format;",
              "withdraw consent at any time — via Cookie settings for analytics, or the unsubscribe link for email — without affecting processing that happened before withdrawal; and",
              "lodge a complaint with your national data protection authority.",
            ].map((item) => (
              <li key={item} className="flex items-start gap-2">
                <span className="shrink-0 text-[var(--brand-slate)] mt-0.5">--</span>
                {item}
              </li>
            ))}
          </ul>
          <p>
            <strong>If you are a California resident</strong>, you have the right to know what
            personal information we collect and how it is used, to request deletion, to correct
            inaccurate information, and to opt out of the sale or sharing of personal information.
            We do not sell or share personal information as defined by California law, and we honor
            the Global Privacy Control signal as an opt-out. You will not be treated differently
            for exercising these rights.
          </p>
          <p>
            <strong>Everyone else</strong> can make the same requests, and we will honor them where
            we reasonably can.
          </p>
          <p>
            To exercise any right, email <strong>privacy@checklist2.com</strong>. Because we do not
            hold accounts, we may ask you to confirm the email address or consent identifier the
            request relates to so we can find the right records. We respond within one month (or
            the shorter period your local law requires).
          </p>
        </Section>

        <Section title="Children's privacy">
          <p>
            Checklist2 is not directed at children under 16, and we do not knowingly collect
            personal data from them. If you believe a child has subscribed to our emails, contact
            us and we will delete the address.
          </p>
        </Section>

        <Section title="Security">
          <p>
            We take reasonable technical and organizational measures to protect the data we hold,
            including encryption in transit, access limited to the site operator, and minimal data
            collection by design. No system is completely secure, and we cannot guarantee absolute
            security.
          </p>
        </Section>

        <Section title="Changes to this policy">
          <p>
            When we change this policy, we update the effective date at the top and summarize what
            changed. For material changes that affect how we use your data, we will notify you
            through a notice on the site or, if you are a subscriber, by email. Earlier versions
            are available on request.
          </p>
        </Section>

        <Section title="Contact">
          <p><strong>privacy@checklist2.com</strong></p>
          <p>Checklist2 · Tyler Lawrence · Orange County, California, USA</p>
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

function PolicyTable({
  headers,
  rows,
}: {
  headers: string[];
  rows: React.ReactNode[][];
}) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm border-collapse">
        <thead>
          <tr>
            {headers.map((h) => (
              <th
                key={h}
                className="text-left font-semibold text-[var(--brand-ink)] align-top py-2 pr-4 border-b border-[var(--brand-line)]"
              >
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => (
            <tr key={i}>
              {row.map((cell, j) => (
                <td
                  key={j}
                  className="align-top py-2 pr-4 border-b border-[var(--brand-line)] text-[var(--brand-ink-soft)]"
                >
                  {cell}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
