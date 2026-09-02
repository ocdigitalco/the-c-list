import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Affiliate Disclosure — Checklist2",
  description: "How Checklist2 uses affiliate links, including the eBay Partner Network.",
};

export default function AffiliateDisclosurePage() {
  return (
    <div className="flex-1">
      <div className="max-w-3xl mx-auto px-6 py-10 space-y-10">
        {/* Header */}
        <div>
          <h1 className="text-2xl font-normal text-[var(--brand-ink)] tracking-tight mb-2" style={{ fontFamily: "var(--brand-font-head)", fontSynthesisWeight: "none" }}>Affiliate Disclosure</h1>
          <p className="text-xs text-[var(--brand-slate)]">Last updated: August 2026</p>
        </div>

        <Section title="Affiliate Disclosure">
          <p>
            Checklist² participates in the eBay Partner Network, an affiliate advertising program.
            Links to eBay on this site — including &quot;Find on eBay&quot; links on checklist and
            athlete pages — are affiliate links. If you click one and make a qualifying purchase,
            Checklist² may earn a commission from eBay. This does not change the price you pay.
          </p>
          <p>
            Affiliate relationships never influence the checklist data, odds, or print runs we
            publish, which come from manufacturer and published sources. If we add other affiliate
            programs in the future, they will be listed here.
          </p>
        </Section>

        <div className="pt-2 pb-4">
          <Link
            href="/privacy"
            className="text-sm text-[var(--brand-slate)] hover:text-[var(--brand-ink-soft)] transition-colors"
          >
            View Privacy Policy
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
