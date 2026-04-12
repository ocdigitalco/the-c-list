import type { Metadata } from "next";
import Link from "next/link";
import { Footer } from "@/components/Footer";

export const metadata: Metadata = {
  title: "How the Break Hit Calculator Works — Checklist2",
  description:
    "Learn how the Break Hit Calculator computes per-athlete hit probabilities using official pack odds, box guarantees, and weighted card pools.",
};

export default function BreakHitCalculatorPage() {
  return (
    <div className="h-full overflow-y-auto">
      <div style={{ maxWidth: 680, margin: "0 auto", padding: "48px 24px 80px" }}>
        {/* Back link */}
        <Link
          href="/sets"
          className="inline-flex items-center gap-1 text-xs text-zinc-500 hover:text-zinc-300 transition-colors mb-8"
        >
          <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
          </svg>
          Back
        </Link>

        <h1 className="text-2xl font-bold text-white tracking-tight mb-4">
          How the Break Hit Calculator Works
        </h1>
        <p className="text-[16px] text-zinc-400 leading-[1.75] mb-10">
          The Break Hit Calculator gives you the most accurate per-athlete hit
          probabilities available for any set on Checklist2. Here is what goes
          into it.
        </p>

        {/* Three Types of Odds */}
        <h2 className="text-lg font-bold text-white mt-12 mb-4">
          Three Types of Odds
        </h2>

        <h3 className="text-base font-semibold text-zinc-300 mt-8 mb-2">
          Any Card
        </h3>
        <p className="text-[16px] text-zinc-400 leading-[1.75] mb-6">
          The probability of pulling any card featuring this athlete in a single
          box. This includes base cards, inserts, numbered parallels, and
          autographs, every card in the checklist weighted by its official pack
          odds.
        </p>

        <h3 className="text-base font-semibold text-zinc-300 mt-8 mb-2">
          Numbered Parallel
        </h3>
        <p className="text-[16px] text-zinc-400 leading-[1.75] mb-6">
          The probability of pulling a numbered card for this athlete. Each
          numbered parallel tier (/299, /199, /99, /50, /25, /10, /5, /1)
          carries its own weight based on official pack odds. Athletes with more
          numbered cards across more tiers have a higher combined probability.
        </p>

        <h3 className="text-base font-semibold text-zinc-300 mt-8 mb-2">
          Autograph
        </h3>
        <p className="text-[16px] text-zinc-400 leading-[1.75] mb-6">
          The probability of pulling an autograph for this athlete. If a box
          guarantees one or more autographs, that guarantee is used as the pull
          floor. The percentage then reflects this athlete&apos;s share of the full
          autograph pool, weighted by the odds of each auto insert set they
          appear in.
        </p>

        {/* How the Math Works */}
        <h2 className="text-lg font-bold text-white mt-12 mb-4">
          How the Math Works
        </h2>
        <p className="text-[16px] text-zinc-400 leading-[1.75] mb-6">
          Every card in the checklist is assigned a weight based on its official
          pack odds. A card at 1:10 packs carries more weight than a card at
          1:500 packs. An athlete&apos;s hit percentage is their share of the total
          pool weight for that card type, adjusted for the number of packs in a
          box and any box guarantees.
        </p>
        <p className="text-[16px] text-zinc-400 leading-[1.75] mb-6">
          This means two things matter beyond just the odds number: how many
          cards an athlete has in the set, and how those cards are distributed
          across insert sets and parallel tiers. An athlete with one autograph
          at 1:26 and another at 1:500 has a higher combined auto probability
          than an athlete with only the 1:26 entry.
        </p>

        {/* Box Guarantees */}
        <h2 className="text-lg font-bold text-white mt-12 mb-4">
          Box Guarantees
        </h2>
        <p className="text-[16px] text-zinc-400 leading-[1.75] mb-6">
          When a box guarantees autographs or numbered cards, those guarantees
          are factored in as the minimum number of pulls from that pool. The
          athlete percentage then reflects their likelihood of being the one you
          pull from that guaranteed slot, not a 100% chance across all athletes.
        </p>

        {/* Why It Doesn't Appear */}
        <h2 className="text-lg font-bold text-white mt-12 mb-4">
          Why the Calculator Sometimes Does Not Appear
        </h2>
        <p className="text-[16px] text-zinc-400 leading-[1.75] mb-6">
          The calculator requires three things to generate reliable results: a
          complete checklist, official pack odds, and a box configuration. If any
          of these are missing or incomplete for a set, the calculator will not
          display rather than show numbers that could be misleading.
        </p>
        <p className="text-[16px] text-zinc-400 leading-[1.75] mb-6">
          As checklists and odds are added and verified, the calculator becomes
          available automatically.
        </p>

        {/* Box Type Selector */}
        <h2 className="text-lg font-bold text-white mt-12 mb-4">
          Box Type Selector
        </h2>
        <p className="text-[16px] text-zinc-400 leading-[1.75] mb-6">
          Different box types (Hobby, Value, Sapphire, Blaster, etc.) have
          different pack counts, odds sheets, and guarantees. Switching box types
          recalculates all three probabilities using the configuration and odds
          for that specific format.
        </p>
      </div>
      <Footer />
    </div>
  );
}
