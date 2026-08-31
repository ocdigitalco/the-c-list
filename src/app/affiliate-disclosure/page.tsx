import type { Metadata } from "next";
import Link from "next/link";
import { Footer } from "@/components/Footer";

export const metadata: Metadata = {
  title: "Affiliate Disclosure — Checklist2",
  description: "How Checklist2 uses affiliate links, including the eBay Partner Network.",
};

export default function AffiliateDisclosurePage() {
  return (
    <div className="h-full overflow-y-auto">
      <div className="max-w-3xl mx-auto px-6 py-10 space-y-10">
        {/* Header */}
        <div>
          <h1 className="text-2xl font-normal text-white tracking-tight mb-2" style={{ fontFamily: "var(--brand-font-head)", fontSynthesisWeight: "none" }}>Affiliate Disclosure</h1>
          <p className="text-xs text-zinc-600">Last updated: August 2026</p>
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
            className="text-sm text-zinc-500 hover:text-zinc-300 transition-colors"
          >
            View Privacy Policy
          </Link>
        </div>
      </div>
      <Footer />
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
      <h2 className="text-base font-semibold text-white mb-3 pb-2 border-b border-zinc-800">
        {title}
      </h2>
      <div className="text-sm text-zinc-400 leading-relaxed space-y-3">{children}</div>
    </section>
  );
}
