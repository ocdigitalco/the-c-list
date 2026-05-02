import type { Metadata } from "next";
import Link from "next/link";
import { PageShell } from "@/components/PageShell";

export const metadata: Metadata = {
  title: "About — Checklist2",
  description:
    "Checklist² was born out of frustration. Built to fix it. Learn about the platform that combines set checklists, box configurations, and pack odds in one place.",
};

const FEATURES = [
  {
    label: "Set Checklists",
    description: "Complete player and card listings for every set.",
    icon: (
      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 002.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 00-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75 2.25 2.25 0 00-.1-.664m-5.8 0A2.251 2.251 0 0113.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25zM6.75 12h.008v.008H6.75V12zm0 3h.008v.008H6.75V15zm0 3h.008v.008H6.75V18z" />
      </svg>
    ),
  },
  {
    label: "Break Hit Calculator",
    description: "Pull probability for any athlete across any number of cases.",
    icon: (
      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 18L9 11.25l4.306 4.306a11.95 11.95 0 015.814-5.518l2.74-1.22m0 0l-5.94-2.281m5.94 2.28l-2.28 5.941" />
      </svg>
    ),
  },
  {
    label: "Pack Odds",
    description: "Official odds by insert set, parallel, and box format.",
    icon: (
      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 3v11.25A2.25 2.25 0 006 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0118 16.5h-2.25m-7.5 0h7.5m-7.5 0l-1 3m8.5-3l1 3m0 0l.5 1.5m-.5-1.5h-9.5m0 0l-.5 1.5" />
      </svg>
    ),
  },
  {
    label: "Athlete Leaderboard",
    description: "See which athletes appear most across all insert sets in a release.",
    icon: (
      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 18.75h-9m9 0a3 3 0 013 3h-15a3 3 0 013-3m9 0v-3.375c0-.621-.503-1.125-1.125-1.125h-.871M7.5 18.75v-3.375c0-.621.504-1.125 1.125-1.125h.872m5.007 0H9.497m5.007 0a7.454 7.454 0 01-.982-3.172M9.497 14.25a7.454 7.454 0 00.981-3.172M5.25 4.236c-.982.143-1.954.317-2.916.52A6.003 6.003 0 007.73 9.728M5.25 4.236V4.5c0 2.108.966 3.99 2.48 5.228M5.25 4.236V2.721C7.456 2.41 9.71 2.25 12 2.25c2.291 0 4.545.16 6.75.47v1.516M7.73 9.728a6.726 6.726 0 002.748 1.35m8.272-6.842V4.5c0 2.108-.966 3.99-2.48 5.228m2.48-5.492a46.32 46.32 0 012.916.52 6.003 6.003 0 01-5.395 4.972m0 0a6.726 6.726 0 01-2.749 1.35m0 0a6.772 6.772 0 01-3.044 0" />
      </svg>
    ),
  },
  {
    label: "Break Sheet Builder",
    description: "Generate Whatnot-ready break sheets in one click.",
    icon: (
      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
      </svg>
    ),
  },
];

export default function AboutPage() {
  return (
    <PageShell
      breadcrumb={{ label: "Home", href: "/checklists" }}
      title="About"
      description={"The story behind Checklist\u00B2"}
    >
      <div className="space-y-20">

        {/* ── The Problem ───────────────────────────────────────────────────────── */}
        <section>
          <div className="flex items-center gap-3 mb-6">
            <span className="shrink-0 w-7 h-7 rounded-lg bg-[#D63A20]/10 border border-[#D63A20]/20 flex items-center justify-center">
              <svg className="w-3.5 h-3.5 text-[#D63A20]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
              </svg>
            </span>
            <h2 className="text-xs font-semibold text-[#D63A20] uppercase tracking-widest">The Problem</h2>
          </div>
          <p className="text-base text-zinc-400 leading-relaxed">
            Navigating box configurations, new release checklists, and pull odds is difficult and time-consuming — even for experienced hobby enthusiasts. Without a way to combine the odds of a set with its full checklist, collectors are left sifting through PDFs and building their own spreadsheets just to understand what's available and what their chances are.
          </p>
        </section>

        <div className="h-px bg-zinc-800" />

        {/* ── What We Built ─────────────────────────────────────────────────────── */}
        <section>
          <div className="flex items-center gap-3 mb-6">
            <span className="shrink-0 w-7 h-7 rounded-lg bg-[#D63A20]/10 border border-[#D63A20]/20 flex items-center justify-center">
              <svg className="w-3.5 h-3.5 text-[#D63A20]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
              </svg>
            </span>
            <h2 className="text-xs font-semibold text-[#D63A20] uppercase tracking-widest">What We Built</h2>
          </div>
          <p className="text-base text-zinc-400 leading-relaxed">
            Checklist² combines set checklists, box configurations, and pack odds into a single easy lookup. Search for any athlete, browse any set, and instantly understand what cards exist and how likely you are to pull them. No spreadsheets. No PDFs. Just answers.
          </p>
        </section>

        <div className="h-px bg-zinc-800" />

        {/* ── Who It's For ──────────────────────────────────────────────────────── */}
        <section>
          <div className="flex items-center gap-3 mb-8">
            <span className="shrink-0 w-7 h-7 rounded-lg bg-[#D63A20]/10 border border-[#D63A20]/20 flex items-center justify-center">
              <svg className="w-3.5 h-3.5 text-[#D63A20]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" />
              </svg>
            </span>
            <h2 className="text-xs font-semibold text-[#D63A20] uppercase tracking-widest">Who It's For</h2>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {/* Collectors */}
            <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6">
              <div className="w-9 h-9 rounded-xl bg-[#D63A20]/10 border border-[#D63A20]/20 flex items-center justify-center mb-4">
                <svg className="w-4.5 h-4.5 text-[#D63A20]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
                </svg>
              </div>
              <h3 className="text-base font-semibold text-white mb-2">Collectors</h3>
              <p className="text-sm text-zinc-400 leading-relaxed">
                Find the cards you want, understand how many cards an athlete has in a set, and make smarter decisions about what to pursue.
              </p>
            </div>
            {/* Breakers */}
            <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-6">
              <div className="w-9 h-9 rounded-xl bg-[#D63A20]/10 border border-[#D63A20]/20 flex items-center justify-center mb-4">
                <svg className="w-4.5 h-4.5 text-[#D63A20]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 3v11.25A2.25 2.25 0 006 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0118 16.5h-2.25m-7.5 0h7.5m-7.5 0l-1 3m8.5-3l1 3m0 0l.5 1.5m-.5-1.5h-9.5m0 0l-.5 1.5M9 11.25v1.5M12 9v3.75m3-6v6" />
                </svg>
              </div>
              <h3 className="text-base font-semibold text-white mb-2">Breakers</h3>
              <p className="text-sm text-zinc-400 leading-relaxed">
                Access tools that make setting up breaks faster and pricing athletes easier — including downloadable break sheets formatted for Whatnot.
              </p>
            </div>
          </div>
        </section>

        <div className="h-px bg-zinc-800" />

        {/* ── Mission Pull Quote ─────────────────────────────────────────────────── */}
        <section>
          <blockquote className="relative rounded-2xl border border-[#D63A20]/20 bg-[#D63A20]/5 px-8 py-10 text-center">
            {/* Decorative quote mark */}
            <div className="absolute -top-4 left-1/2 -translate-x-1/2 w-8 h-8 rounded-full bg-zinc-900 border border-[#D63A20]/30 flex items-center justify-center">
              <svg className="w-4 h-4 text-[#D63A20]" fill="currentColor" viewBox="0 0 24 24">
                <path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z" />
              </svg>
            </div>
            <p className="text-lg sm:text-xl font-medium text-white leading-relaxed">
              Checklist² believes that finding a card or athlete shouldn't mean sifting through PDFs. It should be easier than that.{" "}
              <span className="text-[#D63A20]">Straightforward. Built for everyone in the hobby.</span>
            </p>
          </blockquote>
        </section>

        <div className="h-px bg-zinc-800" />

        {/* ── Feature Highlights ────────────────────────────────────────────────── */}
        <section>
          <div className="flex items-center gap-3 mb-8">
            <span className="shrink-0 w-7 h-7 rounded-lg bg-[#D63A20]/10 border border-[#D63A20]/20 flex items-center justify-center">
              <svg className="w-3.5 h-3.5 text-[#D63A20]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z" />
              </svg>
            </span>
            <h2 className="text-xs font-semibold text-[#D63A20] uppercase tracking-widest">Features</h2>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {FEATURES.map((f) => (
              <div
                key={f.label}
                className="flex items-start gap-3 rounded-xl border border-zinc-800 bg-zinc-900 px-4 py-4"
              >
                <span className="shrink-0 w-8 h-8 rounded-lg bg-[#D63A20]/10 border border-[#D63A20]/20 flex items-center justify-center text-[#D63A20]">
                  {f.icon}
                </span>
                <div>
                  <p className="text-sm font-semibold text-white">{f.label}</p>
                  <p className="text-xs text-zinc-500 mt-0.5 leading-relaxed">{f.description}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* ── CTA ───────────────────────────────────────────────────────────────── */}
        <section className="text-center pt-4">
          <Link
            href="/checklists"
            className="inline-flex items-center gap-2 bg-[#D63A20] hover:bg-[#B12C18] text-white font-bold text-base px-8 py-3.5 rounded-xl transition-colors shadow-lg shadow-[#D63A20]/20"
          >
            Browse Checklists
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
            </svg>
          </Link>
        </section>

      </div>
    </PageShell>
  );
}
