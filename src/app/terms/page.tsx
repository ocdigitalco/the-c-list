import type { Metadata } from "next";
import Link from "next/link";
import { PageShell } from "@/components/PageShell";

export const metadata: Metadata = {
  title: "Terms of Use — Checklist2",
  description: "Terms of Use for Checklist2",
};

export default function TermsPage() {
  return (
    <PageShell
      breadcrumb={{ label: "Home", href: "/checklists" }}
      title="Terms of Use"
      description="Please read these terms before using Checklist\u00B2"
    >
        <p className="text-xs text-zinc-600">Effective Date: March 2026</p>

        <Section title="Acceptance of Terms">
          <p>
            By accessing or using Checklist2, you agree to these Terms of Use. If you do not
            agree, do not use the app.
          </p>
        </Section>

        <Section title="What Checklist2 Is">
          <p>
            Checklist2 is a sports card checklist and break tool platform. It is provided for
            informational and commercial purposes. The platform is free to use but may transition
            to paid features in the future.
          </p>
        </Section>

        <Section title="Data Collection and Use">
          <p className="mb-3">
            When you use Checklist2 we may collect information about how you use the app,
            including which athletes and sets you search for and view. This data is used to:
          </p>
          <ul className="space-y-2">
            {[
              "Improve the application and its features",
              "Understand user interest and demand",
              "Inform product decisions",
              "Gather feedback on the platform",
            ].map((item) => (
              <li key={item} className="flex items-start gap-2">
                <span className="shrink-0 text-zinc-600 mt-0.5">--</span>
                {item}
              </li>
            ))}
          </ul>
        </Section>

        <Section title="Commercial Use of Your Data">
          <p className="mb-3">
            We are transparent that Checklist2 is a commercial product. By using this app you
            acknowledge and agree that:
          </p>
          <ul className="space-y-2">
            {[
              "Your usage data and any information you share may be used for commercial purposes",
              "We may share or sell anonymized or aggregated usage data to third parties including card manufacturers, breakers, advertisers, and data partners",
              "We may use your data to develop paid features, advertising products, or other revenue streams",
              "We intend to generate revenue from this platform now or in the future and your use of the app supports that intent",
            ].map((item) => (
              <li key={item} className="flex items-start gap-2">
                <span className="shrink-0 text-zinc-600 mt-0.5">--</span>
                {item}
              </li>
            ))}
          </ul>
        </Section>

        <Section title="No Account Required">
          <p>
            Checklist2 does not currently require account registration. If you choose to contact
            us or provide feedback, any information you share may be retained and used as
            described above.
          </p>
        </Section>

        <Section title="Intellectual Property">
          <p>
            All checklist data, features, tools, and content on Checklist2 are the property of
            Checklist2. Card set names, athlete names, and manufacturer names are the property of
            their respective owners. Checklist2 is not affiliated with Topps, Panini, or any card
            manufacturer.
          </p>
        </Section>

        <Section title="Third Party Links">
          <p>
            Checklist2 may link to third party platforms including Whatnot, eBay, and TikTok. We
            are not responsible for the content or practices of those platforms.
          </p>
        </Section>

        <Section title="Disclaimer of Warranties">
          <p>
            Checklist2 is provided &quot;as is.&quot; We make no guarantees about the accuracy or
            completeness of checklist data, pack odds, or break probability calculations. All odds
            and calculations are estimates based on available data and should not be relied upon as
            guarantees of results.
          </p>
        </Section>

        <Section title="Limitation of Liability">
          <p>
            To the fullest extent permitted by law, Checklist2 and its owners are not liable for
            any damages arising from your use of the platform.
          </p>
        </Section>

        <Section title="Changes to These Terms">
          <p>
            We may update these Terms at any time. Continued use of the app after changes
            constitutes acceptance of the updated Terms.
          </p>
        </Section>

        <Section title="Contact">
          <p>
            For questions about these Terms, contact us at{" "}
            <span className="text-zinc-300">[contact email placeholder]</span>.
          </p>
        </Section>

        <div className="pt-2 pb-4">
          <Link
            href="/privacy"
            className="text-sm text-zinc-500 hover:text-zinc-300 transition-colors"
          >
            View Privacy Policy
          </Link>
        </div>
    </PageShell>
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
      <h2 className="text-base font-semibold text-white mb-3 pb-2 border-b border-zinc-800">
        {title}
      </h2>
      <div className="text-sm text-zinc-400 leading-relaxed space-y-3">{children}</div>
    </section>
  );
}
