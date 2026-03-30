import type { Metadata } from "next";
import { PageShell } from "@/components/PageShell";

export const metadata: Metadata = {
  title: "Break Hit Calculator — Checklist2",
  description:
    "Learn how the break hit calculator works and what it means for your breaks",
};

const includes = [
  "All numbered (serialized) parallel cards with a known print run",
  "All autograph insert set appearances and their serialized parallels",
  "Official pack odds as published by the manufacturer (Topps, Panini, etc.)",
  "Confirmed box and case configuration (cards per pack, packs per box, boxes per case)",
  "Multi-player cards (dual, triple autos): the athlete's appearance is counted individually",
];

const excludes = [
  {
    item: "Unnumbered / base cards",
    reason:
      "Cards without a print run cannot be accurately calculated because total production quantities are not publicly disclosed by manufacturers.",
  },
  {
    item: "Unnumbered parallels",
    reason:
      "Same reason as above, e.g. standard Refractors, Silver Prizms.",
  },
  {
    item: "Sets without confirmed box configuration",
    reason:
      "If a set does not have verified pack/box/case data, the calculator will not appear.",
  },
  {
    item: "Secondary market supply",
    reason:
      "The calculator reflects original production odds, not current market availability or how many copies have already been graded, sold, or destroyed.",
  },
  {
    item: "Pack distribution variance",
    reason:
      "Real-world breaks can deviate from statistical expectations. The calculator reflects mathematical probability, not a guarantee.",
  },
];

export default function BreakHitCalculatorPage() {
  return (
    <PageShell
      breadcrumb={{ label: "Resources", href: "/resources" }}
      title="Break Hit Calculator"
      description="Calculate your odds of hitting any card across a case or box"
    >
        {/* What is it */}
        <Section title="What is the Break Hit Calculator?">
          <p>
            The Break Hit Calculator is a tool built into each athlete&apos;s card panel on set
            pages. It estimates the statistical probability of pulling a specific athlete&apos;s
            card during a hobby break, based on real checklist data, official pack odds, and
            box configuration.
          </p>
        </Section>

        {/* Where does it appear */}
        <Section title="Where does it appear?">
          <p>
            The calculator appears at the top of every athlete&apos;s card panel on a set page,
            provided that set has confirmed box configuration data. It is scoped to the
            specific set you are viewing: the odds shown are for that set only.
          </p>
        </Section>

        {/* Formula */}
        <Section title="How is the percentage calculated?">
          <p className="mb-4">
            The calculator uses the following formula:
          </p>

          <div className="rounded-lg border border-zinc-700 bg-zinc-950 px-5 py-4 font-mono text-sm text-zinc-200 leading-relaxed mb-4">
            <div className="text-zinc-500 text-xs mb-2 font-sans uppercase tracking-widest">Formula</div>
            <div>P = 1 − (1 − player_share / denom)^total_packs</div>
          </div>

          <div className="rounded-lg border border-zinc-800 bg-zinc-900 px-5 py-4 space-y-2 text-sm text-zinc-400 mb-4">
            <div className="flex gap-3">
              <span className="font-mono text-zinc-300 shrink-0">player_share</span>
              <span>= 1 ÷ total players appearing in that insert set</span>
            </div>
            <div className="flex gap-3">
              <span className="font-mono text-zinc-300 shrink-0">denom</span>
              <span>= the pack odds denominator for that specific parallel or auto insert set (e.g. for 1:10 odds, denom = 10)</span>
            </div>
            <div className="flex gap-3">
              <span className="font-mono text-zinc-300 shrink-0">total_packs</span>
              <span>= cases × boxes per case × packs per box</span>
            </div>
          </div>

          <p>
            For each card type (parallels, autographs), the pack odds provided by the
            manufacturer are used alongside the athlete&apos;s share of that insert set to
            determine their individual probability. Each parallel type and auto insert set is
            calculated independently, then combined using:
          </p>

          <div className="rounded-lg border border-zinc-700 bg-zinc-950 px-5 py-4 font-mono text-sm text-zinc-200 mt-4">
            <div className="text-zinc-500 text-xs mb-2 font-sans uppercase tracking-widest">Combined probability</div>
            <div>P_total = 1 − Π(1 − P_i)</div>
          </div>

          <p className="mt-4">
            This gives the probability of hitting <span className="text-white font-medium">at least one</span> of
            the athlete&apos;s cards across the entire break, not just in a single pack.
          </p>
        </Section>

        {/* Result rows */}
        <Section title="What does each result row mean?">
          <div className="space-y-4">
            <ResultRow
              label="Any Card"
              color="text-amber-400"
              dot="bg-amber-500"
            >
              A combined probability that factors in both serialized parallels and autographs.
              This represents the broadest possible chance of pulling any serialized card of
              this athlete in the break.
            </ResultRow>

            <ResultRow
              label="Numbered Parallels"
              color="text-amber-400"
              dot="bg-amber-500"
            >
              The probability of pulling any numbered parallel card of this athlete.
              This includes all numbered (serialized) parallel versions across all insert sets and
              the base set (e.g. /199, /99, /25, /10, /5, /3, /1). Each parallel version is
              counted individually using its known print run.
            </ResultRow>

            <ResultRow
              label="Autographs"
              color="text-amber-400"
              dot="bg-amber-500"
            >
              The probability of pulling any autograph card of this athlete. This includes all
              autograph insert sets (e.g. Stroke of Midnight Autographs, Horizon Signatures,
              Relic Autographs) and their serialized parallel versions. The pack odds for each
              auto insert set are used to determine expected auto pulls per case.
            </ResultRow>
          </div>
        </Section>

        {/* Includes / Excludes */}
        <Section title="What the calculator includes and excludes">
          <div className="space-y-3 mb-6">
            {includes.map((item) => (
              <div key={item} className="flex items-start gap-3">
                <span className="shrink-0 w-4 h-4 rounded-full bg-emerald-500/15 border border-emerald-500/40 flex items-center justify-center mt-0.5">
                  <svg className="w-2.5 h-2.5 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                  </svg>
                </span>
                <span className="text-sm text-zinc-300">{item}</span>
              </div>
            ))}
          </div>

          <div className="space-y-3">
            {excludes.map((item) => (
              <div key={item.item} className="flex items-start gap-3">
                <span className="shrink-0 w-4 h-4 rounded-full bg-red-500/15 border border-red-500/40 flex items-center justify-center mt-0.5">
                  <svg className="w-2.5 h-2.5 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </span>
                <div>
                  <span className="text-sm font-medium text-zinc-300">{item.item}:</span>
                  {" "}
                  <span className="text-sm text-zinc-500">{item.reason}</span>
                </div>
              </div>
            ))}
          </div>
        </Section>

        {/* Color coding */}
        <Section title="Color coding">
          <div className="space-y-3">
            <div className="flex items-start gap-4 rounded-lg border border-zinc-800 bg-zinc-900 px-4 py-3">
              <span className="shrink-0 w-2.5 h-2.5 rounded-full bg-emerald-500 mt-1" />
              <div>
                <span className="text-sm font-semibold text-emerald-400">Green: 60% or higher</span>
                <p className="text-sm text-zinc-400 mt-0.5">
                  Strong chance. You would statistically expect to hit this athlete more often
                  than not across breaks of this size.
                </p>
              </div>
            </div>
            <div className="flex items-start gap-4 rounded-lg border border-zinc-800 bg-zinc-900 px-4 py-3">
              <span className="shrink-0 w-2.5 h-2.5 rounded-full bg-amber-500 mt-1" />
              <div>
                <span className="text-sm font-semibold text-amber-400">Yellow: 10% to 59%</span>
                <p className="text-sm text-zinc-400 mt-0.5">
                  Moderate chance. Realistic but not guaranteed.
                </p>
              </div>
            </div>
            <div className="flex items-start gap-4 rounded-lg border border-zinc-800 bg-zinc-900 px-4 py-3">
              <span className="shrink-0 w-2.5 h-2.5 rounded-full bg-red-500 mt-1" />
              <div>
                <span className="text-sm font-semibold text-red-400">Red: below 10%</span>
                <p className="text-sm text-zinc-400 mt-0.5">
                  Low chance. This athlete is rare in this configuration, and a hit would be a
                  notable pull.
                </p>
              </div>
            </div>
          </div>
        </Section>

        {/* Disclaimers */}
        <Section title="Important disclaimers">
          <ul className="space-y-2 text-sm text-zinc-400">
            {[
              "Odds are based on serialized print runs and official pack ratios only.",
              "Unnumbered cards are excluded from all calculations.",
              "Results are statistical estimates, not guarantees.",
              "Box configuration data is verified per set: if configuration data changes or is corrected, odds will update automatically.",
              "The calculator is intended as a planning and reference tool for break buyers, not a guarantee of results.",
            ].map((d) => (
              <li key={d} className="flex items-start gap-2">
                <span className="shrink-0 text-zinc-600 mt-0.5">–</span>
                {d}
              </li>
            ))}
          </ul>
        </Section>
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

function ResultRow({
  label,
  color,
  dot,
  children,
}: {
  label: string;
  color: string;
  dot: string;
  children: React.ReactNode;
}) {
  return (
    <div className="rounded-lg border border-zinc-800 bg-zinc-900 px-4 py-3">
      <div className="flex items-center gap-2 mb-1.5">
        <span className={`shrink-0 w-2 h-2 rounded-full ${dot}`} />
        <span className={`text-sm font-semibold ${color}`}>{label}</span>
      </div>
      <p className="text-sm text-zinc-400 leading-relaxed">{children}</p>
    </div>
  );
}
