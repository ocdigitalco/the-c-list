import Link from "next/link";
import { Footer } from "@/components/Footer";

export default function LandingPage() {
  return (
    <div className="h-full overflow-y-auto scroll-smooth">

      {/* ── Section 1: Hero ─────────────────────────────────────────────────── */}
      <section className="relative flex flex-col items-center justify-center min-h-[calc(100vh-3.5rem)] px-6 overflow-hidden bg-zinc-950">
        {/* Ambient radial glow */}
        <div
          className="absolute inset-0 pointer-events-none"
          style={{
            background:
              "radial-gradient(ellipse 90% 55% at 50% -5%, rgba(245,158,11,0.10) 0%, transparent 65%)",
          }}
        />

        {/* Decorative floating sport emojis */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none select-none" aria-hidden>
          {(
            [
              { text: "⚾", style: { top: "13%", left: "7%",  opacity: 0.055, fontSize: "5rem" } },
              { text: "🏀", style: { top: "70%", left: "5%",  opacity: 0.045, fontSize: "4rem" } },
              { text: "🏒", style: { top: "18%", right: "6%", opacity: 0.055, fontSize: "4.5rem" } },
              { text: "⚽", style: { top: "62%", right: "9%", opacity: 0.045, fontSize: "4rem" } },
              { text: "🥊", style: { top: "84%", left: "20%", opacity: 0.04,  fontSize: "3rem" } },
              { text: "🏈", style: { top: "38%", right: "3%", opacity: 0.04,  fontSize: "3.5rem" } },
            ] as { text: string; style: React.CSSProperties }[]
          ).map(({ text, style }, i) => (
            <span key={i} className="absolute leading-none" style={style}>
              {text}
            </span>
          ))}
        </div>

        {/* Main content */}
        <div className="relative z-10 text-center max-w-4xl mx-auto">
          {/* Eyebrow pill */}
          <div className="inline-flex items-center gap-2 bg-amber-400/10 border border-amber-400/20 rounded-full px-4 py-1.5 text-xs font-medium text-amber-400 mb-8">
            <span className="w-1.5 h-1.5 rounded-full bg-amber-400 animate-pulse" />
            Sports Card Checklist Platform
          </div>

          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-extrabold text-white tracking-tight leading-[1.08] mb-6">
            Every Card.{" "}
            <span className="text-amber-400">Every Set.</span>
            <br />
            Every Break.
          </h1>

          <p className="text-lg sm:text-xl text-zinc-400 max-w-2xl mx-auto mb-10 leading-relaxed">
            Explore complete checklists for the hottest trading card sets across every sport.
            Built for collectors and breakers who want the data.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              href="/checklists"
              className="inline-flex items-center gap-2 bg-amber-500 hover:bg-amber-400 text-black font-bold text-base px-8 py-3.5 rounded-xl transition-colors shadow-lg shadow-amber-500/20"
            >
              Browse Checklists
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
              </svg>
            </Link>
            <a
              href="#calculator"
              className="inline-flex items-center gap-2 text-zinc-400 hover:text-white text-base font-medium px-6 py-3.5 rounded-xl border border-zinc-800 hover:border-zinc-600 transition-colors"
            >
              Learn More
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
              </svg>
            </a>
          </div>
        </div>

        {/* Bounce indicator */}
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 text-zinc-700 animate-bounce" aria-hidden>
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
          </svg>
        </div>
      </section>

      {/* ── Section 2: Break Hit Calculator ──────────────────────────────────── */}
      <section
        id="calculator"
        className="min-h-[calc(100vh-3.5rem)] flex items-center px-6 py-20"
        style={{ background: "rgba(24,24,27,0.5)" }}
      >
        <div className="max-w-5xl mx-auto w-full grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-20 items-center">

          {/* Left: copy */}
          <div>
            <p className="text-xs font-semibold text-amber-400 uppercase tracking-widest mb-4">
              Break Hit Calculator
            </p>
            <h2 className="text-3xl sm:text-4xl font-bold text-white tracking-tight leading-tight mb-6">
              Know Your Odds Before You Break
            </h2>
            <ul className="space-y-5 mb-10">
              {(
                [
                  [
                    "Calculate pull probability",
                    "Get the statistical likelihood of pulling any specific athlete's card in a break.",
                  ],
                  [
                    "Powered by official data",
                    "Based on official pack odds, serialized print runs, and confirmed box configurations.",
                  ],
                  [
                    "Any card type",
                    "Supports Any Card, Numbered Parallel, and Autograph hit probability calculations.",
                  ],
                  [
                    "Instant updates",
                    "Adjusts in real time as you change case count — plan your break before you spend.",
                  ],
                ] as [string, string][]
              ).map(([title, desc]) => (
                <li key={title} className="flex gap-3">
                  <div className="shrink-0 w-5 h-5 rounded-full bg-amber-500/15 border border-amber-500/30 flex items-center justify-center mt-0.5">
                    <div className="w-1.5 h-1.5 rounded-full bg-amber-500" />
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-white">{title}</p>
                    <p className="text-sm text-zinc-500 mt-0.5">{desc}</p>
                  </div>
                </li>
              ))}
            </ul>
            <Link
              href="/checklists"
              className="inline-flex items-center gap-2 bg-zinc-800 hover:bg-zinc-700 text-white font-semibold text-sm px-6 py-3 rounded-xl border border-zinc-700 hover:border-zinc-500 transition-colors"
            >
              Explore a Set
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
              </svg>
            </Link>
          </div>

          {/* Right: calculator mockup */}
          <div className="bg-zinc-950 rounded-2xl border border-zinc-800 overflow-hidden shadow-2xl">
            {/* Mockup header bar */}
            <div className="bg-zinc-900 border-b border-zinc-800 px-5 py-3.5 flex items-center gap-2">
              <svg className="w-4 h-4 text-amber-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 15.75l-2.489-2.489m0 0a3.375 3.375 0 10-4.773-4.773 3.375 3.375 0 004.773 4.773zM21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span className="text-xs font-semibold text-zinc-300">Break Hit Calculator</span>
            </div>

            <div className="p-5 space-y-4">
              {/* Set name display */}
              <div className="flex items-center justify-between bg-zinc-900 border border-zinc-800 rounded-lg px-4 py-2.5">
                <span className="text-sm text-zinc-300">2025 Topps Chrome Baseball</span>
                <svg className="w-3.5 h-3.5 text-zinc-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
                </svg>
              </div>

              {/* Config row */}
              <div className="flex items-center gap-3">
                <div className="flex-1 bg-zinc-900 border border-zinc-800 rounded-lg px-4 py-2.5">
                  <p className="text-xs text-zinc-600">Cases</p>
                  <p className="text-sm font-semibold text-white">3</p>
                </div>
                <div className="flex-1 bg-zinc-900 border border-zinc-800 rounded-lg px-4 py-2.5">
                  <p className="text-xs text-zinc-600">Boxes / Case</p>
                  <p className="text-sm font-semibold text-white">12</p>
                </div>
              </div>

              {/* Player chip */}
              <div className="flex items-center gap-3 rounded-lg px-4 py-2.5 border border-amber-400/20" style={{ background: "rgba(245,158,11,0.06)" }}>
                <div className="w-7 h-7 rounded-full bg-zinc-700 flex items-center justify-center text-xs font-bold text-zinc-300 shrink-0">
                  JS
                </div>
                <div>
                  <p className="text-sm font-semibold text-white">Juan Soto</p>
                  <p className="text-xs text-zinc-500">New York Mets · Baseball</p>
                </div>
              </div>

              {/* Probability rows */}
              <div className="space-y-3">
                {(
                  [
                    { label: "Any Card", odds: "1:1.3 per case", pct: 78 },
                    { label: "Autograph", odds: "1:16 per case", pct: 34 },
                    { label: "Numbered /25", odds: "1:52 per case", pct: 11 },
                  ] as { label: string; odds: string; pct: number }[]
                ).map(({ label, odds, pct }) => (
                  <div key={label} className="space-y-1.5">
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-zinc-400">{label}</span>
                      <span className="text-xs font-mono font-semibold text-amber-400">{odds}</span>
                    </div>
                    <div className="h-1.5 bg-zinc-800 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-amber-500 rounded-full"
                        style={{ width: `${pct}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── Section 3: Athlete Leaderboard ──────────────────────────────────── */}
      <section
        id="leaderboard"
        className="min-h-[calc(100vh-3.5rem)] flex items-center px-6 py-20 bg-zinc-950"
      >
        <div className="max-w-5xl mx-auto w-full grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-20 items-center">

          {/* Left: leaderboard mockup */}
          <div className="bg-zinc-900 rounded-2xl border border-zinc-700 overflow-hidden shadow-2xl">
            {/* Panel header */}
            <div className="flex items-center justify-between px-5 py-4 border-b border-zinc-800">
              <div>
                <p className="text-sm font-semibold text-white">Athlete Leaderboard</p>
                <p className="text-xs text-zinc-500 mt-0.5">248 athletes</p>
              </div>
              <div className="w-6 h-6 rounded-md bg-zinc-800 flex items-center justify-center">
                <svg className="w-3.5 h-3.5 text-zinc-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </div>
            </div>

            <div className="px-4 pt-3 pb-2 space-y-2.5 border-b border-zinc-800">
              {/* Sort tabs */}
              <div className="flex gap-1 rounded-lg bg-zinc-800/60 p-0.5">
                {["Total Cards", "Autographs", "Inserts", "Numbered"].map((tab, i) => (
                  <div
                    key={tab}
                    className={`flex-1 text-[10px] py-1.5 rounded-md font-medium text-center ${
                      i === 0 ? "bg-zinc-700 text-white" : "text-zinc-500"
                    }`}
                  >
                    {tab}
                  </div>
                ))}
              </div>
              {/* Filter pills */}
              <div className="flex items-center gap-2">
                <div className="text-[10px] px-2.5 py-1.5 rounded-md border border-zinc-700 text-zinc-500">
                  Rookies Only
                </div>
                <div className="flex-1 bg-zinc-800 border border-zinc-700 rounded-md px-2.5 py-1.5 text-[10px] text-zinc-600">
                  Filter by team...
                </div>
              </div>
            </div>

            {/* Athlete rows */}
            <div className="divide-y divide-zinc-800/60">
              {(
                [
                  { rank: 1, name: "Jesus Made", team: "Boston Red Sox", rc: false, val: 96 },
                  { rank: 2, name: "Jac Caglianone", team: "Kansas City Royals", rc: true, val: 95 },
                  { rank: 3, name: "JJ Wetherholt", team: "Washington Nationals", rc: true, val: 91 },
                  { rank: 4, name: "Roki Sasaki", team: "Los Angeles Dodgers", rc: false, val: 87 },
                  { rank: 5, name: "Charlie Condon", team: "Colorado Rockies", rc: true, val: 84 },
                ] as { rank: number; name: string; team: string; rc: boolean; val: number }[]
              ).map(({ rank, name, team, rc, val }) => (
                <div
                  key={rank}
                  className="grid grid-cols-[auto_1fr_auto] items-center gap-3 px-4 py-2.5"
                >
                  <span className="text-xs text-zinc-600 tabular-nums w-4 text-right">{rank}</span>
                  <div>
                    <div className="flex items-center gap-1.5">
                      <span className="text-sm font-medium text-zinc-200">{name}</span>
                      {rc && (
                        <span className="text-[9px] font-semibold text-amber-400 bg-amber-400/10 px-1 py-0.5 rounded leading-none">
                          RC
                        </span>
                      )}
                    </div>
                    <p className="text-[10px] text-zinc-600 mt-0.5">{team}</p>
                  </div>
                  <span className="text-sm font-bold text-white tabular-nums">{val}</span>
                </div>
              ))}
            </div>

            <div className="px-4 py-2.5 border-t border-zinc-800">
              <p className="text-xs text-zinc-600 text-center">Show all 248 athletes</p>
            </div>
          </div>

          {/* Right: copy */}
          <div>
            <p className="text-xs font-semibold text-amber-400 uppercase tracking-widest mb-4">
              Athlete Leaderboard
            </p>
            <h2 className="text-3xl sm:text-4xl font-bold text-white tracking-tight leading-tight mb-6">
              See Who Leads Every Set
            </h2>
            <ul className="space-y-5 mb-10">
              {(
                [
                  [
                    "Rank by cards, autos, inserts, or numbered",
                    "Instantly see which athletes have the most cards, autographs, inserts, and numbered parallels in any set.",
                  ],
                  [
                    "Filter by team",
                    "Smart team search lets you find every athlete from a specific franchise in seconds.",
                  ],
                  [
                    "Rookies only toggle",
                    "Narrow the view to rookie cards only to see which RCs have the deepest checklist presence.",
                  ],
                  [
                    "Jump to any athlete",
                    "Click any row in the leaderboard to open that athlete's full card panel instantly.",
                  ],
                ] as [string, string][]
              ).map(([title, desc]) => (
                <li key={title} className="flex gap-3">
                  <div className="shrink-0 w-5 h-5 rounded-full bg-amber-500/15 border border-amber-500/30 flex items-center justify-center mt-0.5">
                    <div className="w-1.5 h-1.5 rounded-full bg-amber-500" />
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-white">{title}</p>
                    <p className="text-sm text-zinc-500 mt-0.5">{desc}</p>
                  </div>
                </li>
              ))}
            </ul>
            <Link
              href="/checklists"
              className="inline-flex items-center gap-2 bg-zinc-800 hover:bg-zinc-700 text-white font-semibold text-sm px-6 py-3 rounded-xl border border-zinc-700 hover:border-zinc-500 transition-colors"
            >
              Explore a Set
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
              </svg>
            </Link>
          </div>
        </div>
      </section>

      {/* ── Section 4: Pack Odds ──────────────────────────────────────────────── */}
      <section
        id="pack-odds"
        className="min-h-[calc(100vh-3.5rem)] flex items-center px-6 py-20"
        style={{ background: "rgba(24,24,27,0.5)" }}
      >
        <div className="max-w-5xl mx-auto w-full grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-20 items-center">

          {/* Left: copy */}
          <div>
            <p className="text-xs font-semibold text-amber-400 uppercase tracking-widest mb-4">
              Pack Odds &amp; Box Config
            </p>
            <h2 className="text-3xl sm:text-4xl font-bold text-white tracking-tight leading-tight mb-6">
              Know What&apos;s in Every Box
            </h2>
            <ul className="space-y-5 mb-10">
              {(
                [
                  [
                    "Official pack odds for every set",
                    "Full pull rate tables sourced directly from manufacturer data for every set in the app.",
                  ],
                  [
                    "Box and case configuration",
                    "Cards per pack, packs per box, boxes per case, and guaranteed hits per box -- all in one place.",
                  ],
                  [
                    "Grouped by category",
                    "Base parallels, inserts, autographs, and memorabilia each in their own section for easy scanning.",
                  ],
                  [
                    "Most common to most rare",
                    "Every table is sorted from highest pull rate to lowest so the best odds are always at the top.",
                  ],
                ] as [string, string][]
              ).map(([title, desc]) => (
                <li key={title} className="flex gap-3">
                  <div className="shrink-0 w-5 h-5 rounded-full bg-amber-500/15 border border-amber-500/30 flex items-center justify-center mt-0.5">
                    <div className="w-1.5 h-1.5 rounded-full bg-amber-500" />
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-white">{title}</p>
                    <p className="text-sm text-zinc-500 mt-0.5">{desc}</p>
                  </div>
                </li>
              ))}
            </ul>
            <Link
              href="/checklists"
              className="inline-flex items-center gap-2 bg-zinc-800 hover:bg-zinc-700 text-white font-semibold text-sm px-6 py-3 rounded-xl border border-zinc-700 hover:border-zinc-500 transition-colors"
            >
              View Pack Odds
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
              </svg>
            </Link>
          </div>

          {/* Right: odds table mockup */}
          <div className="bg-zinc-950 rounded-2xl border border-zinc-800 overflow-hidden shadow-2xl">
            {/* Mockup header */}
            <div className="bg-zinc-900 border-b border-zinc-800 px-5 py-3.5 flex items-center gap-2">
              <svg className="w-4 h-4 text-amber-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 18 9 11.25l4.306 4.306a11.95 11.95 0 0 1 5.814-5.518l2.74-1.22m0 0-5.94-2.281m5.94 2.28-2.28 5.941" />
              </svg>
              <span className="text-xs font-semibold text-zinc-300">Pack Odds</span>
              <span className="ml-auto text-xs text-zinc-600">2025 Bowman&apos;s Best Baseball</span>
            </div>

            <div className="p-5 space-y-5">
              {/* Box config chips */}
              <div className="grid grid-cols-3 gap-2">
                {[["8", "Cards / Pack"], ["12", "Packs / Box"], ["8", "Boxes / Case"]].map(([val, label]) => (
                  <div key={label} className="rounded-lg border border-zinc-800 bg-zinc-900 px-3 py-2">
                    <p className="text-xs text-zinc-600">{label}</p>
                    <p className="text-sm font-bold text-white tabular-nums">{val}</p>
                  </div>
                ))}
              </div>

              {/* Autographs table */}
              <div>
                <p className="text-[10px] font-semibold text-zinc-500 uppercase tracking-widest mb-1.5">Autographs</p>
                <div className="rounded-lg border border-zinc-800 overflow-hidden">
                  <div className="grid grid-cols-[1fr_auto] bg-zinc-900/60 px-3 py-1.5 border-b border-zinc-800">
                    <span className="text-[10px] text-zinc-600 uppercase tracking-wider">Parallel / Insert</span>
                    <span className="text-[10px] text-zinc-600 uppercase tracking-wider">Odds</span>
                  </div>
                  {[
                    ["Best Performance Autographs", "1:21"],
                    ["Best of 2025 Autographs", "1:24"],
                    ["Best Mix Autograph Diecuts", "1:1,459"],
                    ["Best Mix Autograph Gold /10", "1:5,836"],
                  ].map(([name, odds]) => (
                    <div key={name as string} className="grid grid-cols-[1fr_auto] items-center px-3 py-2 border-b border-zinc-800/60 bg-zinc-900 last:border-0">
                      <span className="text-xs text-zinc-400 truncate pr-3">{name}</span>
                      <span className="text-xs font-mono text-zinc-500 tabular-nums">{odds}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Base parallels table */}
              <div>
                <p className="text-[10px] font-semibold text-zinc-500 uppercase tracking-widest mb-1.5">Base Parallels</p>
                <div className="rounded-lg border border-zinc-800 overflow-hidden">
                  {[
                    ["Base Lazer Refractor", "1:22"],
                    ["Base Purple Refractor", "1:31"],
                    ["Base Blue Refractor", "1:51"],
                  ].map(([name, odds]) => (
                    <div key={name as string} className="grid grid-cols-[1fr_auto] items-center px-3 py-2 border-b border-zinc-800/60 bg-zinc-900 last:border-0">
                      <span className="text-xs text-zinc-400 truncate pr-3">{name}</span>
                      <span className="text-xs font-mono text-zinc-500 tabular-nums">{odds}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── Section 5: Break Sheet Builder ──────────────────────────────────── */}
      <section
        id="break-sheet"
        className="min-h-[calc(100vh-3.5rem)] flex items-center px-6 py-20 bg-zinc-950"
      >
        <div className="max-w-5xl mx-auto w-full grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-20 items-center">

          {/* Left: modal mockup */}
          <div className="bg-zinc-900 rounded-2xl border border-zinc-700 overflow-hidden shadow-2xl">
            {/* Modal header */}
            <div className="flex items-center justify-between px-5 py-4 border-b border-zinc-800 bg-zinc-900">
              <div>
                <p className="text-sm font-semibold text-white">Download Break Sheet</p>
                <p className="text-xs text-zinc-500 mt-0.5">2025 Topps Chrome UFC · 52 rows</p>
              </div>
              <div className="w-6 h-6 rounded-md bg-zinc-800 flex items-center justify-center">
                <svg className="w-3.5 h-3.5 text-zinc-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </div>
            </div>

            <div className="px-5 py-4 space-y-4">
              {/* Description */}
              <div>
                <p className="text-xs text-zinc-500 mb-1.5">Break Description</p>
                <div className="bg-zinc-800 border border-zinc-700 rounded-lg px-3 py-2 text-sm text-zinc-400">
                  3 Cases! 2025 Topps Chrome UFC
                </div>
              </div>

              {/* Listing type */}
              <div>
                <p className="text-xs text-zinc-500 mb-1.5">Listing Type</p>
                <div className="flex rounded-lg border border-zinc-700 overflow-hidden text-xs">
                  <div className="flex-1 py-2 text-center bg-zinc-700 text-white font-semibold">Buy it Now</div>
                  <div className="flex-1 py-2 text-center bg-zinc-800/60 text-zinc-500">Auction</div>
                </div>
              </div>

              {/* Tag labels */}
              <div>
                <p className="text-xs text-zinc-500 mb-1.5">Tag Labels</p>
                <div className="grid grid-cols-4 gap-1.5">
                  {["AUTO", "MEM AUTO", "RELIC", "RC"].map((tag) => (
                    <div
                      key={tag}
                      className="bg-zinc-800 border border-zinc-700 rounded px-2 py-1.5 text-center text-xs font-mono text-zinc-300"
                    >
                      {tag}
                    </div>
                  ))}
                </div>
              </div>

              {/* Title preview */}
              <div>
                <p className="text-xs text-zinc-500 mb-1.5">Title Preview</p>
                <div className="rounded-lg border border-zinc-800 bg-zinc-950 divide-y divide-zinc-800 overflow-hidden">
                  {["Islam Makhachev (AUTO)", "Alex Pereira (AUTO)(RC)", "Jon Jones (MEM AUTO)"].map((title) => (
                    <div key={title} className="px-3 py-2">
                      <p className="text-xs font-mono text-zinc-300">{title}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Download button */}
            <div className="px-5 py-4 border-t border-zinc-800">
              <div className="w-full flex items-center justify-center gap-2 bg-amber-500 text-black font-semibold text-sm py-2.5 rounded-lg">
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
                </svg>
                Download CSV (52 rows)
              </div>
            </div>
          </div>

          {/* Right: copy */}
          <div>
            <p className="text-xs font-semibold text-amber-400 uppercase tracking-widest mb-4">
              Break Sheet Builder
            </p>
            <h2 className="text-3xl sm:text-4xl font-bold text-white tracking-tight leading-tight mb-6">
              Build Your Break Sheet in Seconds
            </h2>
            <ul className="space-y-5 mb-10">
              {(
                [
                  [
                    "Whatnot-ready CSV",
                    "Instantly generate a formatted CSV for any set in the app — ready to upload directly to Whatnot.",
                  ],
                  [
                    "Fully customizable",
                    "Set the break description, listing type, and tag labels (AUTO, MEM AUTO, RELIC, RC) before you download.",
                  ],
                  [
                    "Smart athlete rows",
                    "One row per athlete, pre-filled with their card highlights — autos, relics, rookies — automatically detected.",
                  ],
                  [
                    "List in minutes",
                    "Upload the CSV to Whatnot and your break slots are live. No manual entry required.",
                  ],
                ] as [string, string][]
              ).map(([title, desc]) => (
                <li key={title} className="flex gap-3">
                  <div className="shrink-0 w-5 h-5 rounded-full bg-amber-500/15 border border-amber-500/30 flex items-center justify-center mt-0.5">
                    <div className="w-1.5 h-1.5 rounded-full bg-amber-500" />
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-white">{title}</p>
                    <p className="text-sm text-zinc-500 mt-0.5">{desc}</p>
                  </div>
                </li>
              ))}
            </ul>
            <Link
              href="/checklists"
              className="inline-flex items-center gap-2 bg-amber-500 hover:bg-amber-400 text-black font-bold text-sm px-6 py-3 rounded-xl transition-colors shadow-lg shadow-amber-500/15"
            >
              Try the Break Sheet Builder
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
              </svg>
            </Link>
          </div>
        </div>
      </section>

      {/* ── Section 4: Where to Break ──────────────────────────────────────── */}
      <section className="border-t border-zinc-800 px-6 py-16" style={{ background: "rgba(24,24,27,0.6)" }}>
        <div className="max-w-3xl mx-auto">
          <h2 className="text-lg font-bold text-white text-center mb-10">Break Anywhere</h2>
          <div className="grid grid-cols-3 gap-4">

            {/* Whatnot */}
            <a
              href="https://www.whatnot.com"
              target="_blank"
              rel="noopener noreferrer"
              className="flex flex-col items-center gap-3 bg-zinc-900 border border-zinc-800 hover:border-zinc-600 rounded-2xl px-4 py-8 transition-colors group"
            >
              <div
                className="w-12 h-12 rounded-xl flex items-center justify-center text-white font-extrabold text-2xl"
                style={{ background: "linear-gradient(135deg, #ff3b6b 0%, #ff6b3b 100%)" }}
              >
                W
              </div>
              <span className="text-sm font-semibold text-zinc-300 group-hover:text-white transition-colors">
                Whatnot
              </span>
            </a>

            {/* TikTok */}
            <a
              href="https://www.tiktok.com"
              target="_blank"
              rel="noopener noreferrer"
              className="flex flex-col items-center gap-3 bg-zinc-900 border border-zinc-800 hover:border-zinc-600 rounded-2xl px-4 py-8 transition-colors group"
            >
              <div className="w-12 h-12 rounded-xl bg-zinc-800 flex items-center justify-center">
                <svg className="w-6 h-6 text-white" viewBox="0 0 24 24" fill="currentColor" aria-hidden>
                  <path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-2.88 2.5 2.89 2.89 0 01-2.89-2.89 2.89 2.89 0 012.89-2.89c.28 0 .54.04.79.1V9.01a6.31 6.31 0 00-.79-.05 6.34 6.34 0 00-6.34 6.34 6.34 6.34 0 006.34 6.34 6.34 6.34 0 006.33-6.34V9.05a8.16 8.16 0 004.77 1.52V7.12a4.85 4.85 0 01-1-.43z" />
                </svg>
              </div>
              <span className="text-sm font-semibold text-zinc-300 group-hover:text-white transition-colors">
                TikTok
              </span>
            </a>

            {/* eBay */}
            <a
              href="https://www.ebay.com"
              target="_blank"
              rel="noopener noreferrer"
              className="flex flex-col items-center gap-3 bg-zinc-900 border border-zinc-800 hover:border-zinc-600 rounded-2xl px-4 py-8 transition-colors group"
            >
              <div className="w-12 h-12 rounded-xl bg-zinc-800 flex items-center justify-center">
                <span className="text-lg font-extrabold tracking-tight leading-none">
                  <span className="text-red-400">e</span>
                  <span className="text-blue-400">b</span>
                  <span className="text-amber-400">a</span>
                  <span className="text-green-400">y</span>
                </span>
              </div>
              <span className="text-sm font-semibold text-zinc-300 group-hover:text-white transition-colors">
                eBay
              </span>
            </a>

          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
