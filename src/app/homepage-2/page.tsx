"use client";

import { useEffect, useRef, useState, useCallback } from "react";
import Link from "next/link";

/* ─── Google Fonts via <link> (injected once) ─────────────────────────────── */
function useFontLink() {
  useEffect(() => {
    if (document.querySelector("link[data-hp2-fonts]")) return;
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.dataset.hp2Fonts = "1";
    link.href =
      "https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,600;0,700&family=DM+Serif+Display:ital@0;1&display=swap";
    document.head.appendChild(link);
  }, []);
}

/* ─── Palette ─────────────────────────────────────────────────────────────── */
const C = {
  bg: "#0a0a0f",
  accent: "#e8ff47",
  purple: "#7c6dfa",
  text: "#f0f0f5",
  muted: "#6b6b80",
} as const;

/* ─── Feature data ────────────────────────────────────────────────────────── */
interface StatModal {
  value: string;
  label: string;
  accent?: boolean;
}

const FEATURES = [
  {
    icon: (
      <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
      </svg>
    ),
    title: "Athlete Search",
    desc: "Find any athlete across every set instantly. Filter by sport, team, or rookie status. Jump straight to full card breakdowns with a single click.",
    cta: { label: "Search Athletes", href: "/checklists" },
    stats: [
      { value: "159", label: "Unique Cards" },
      { value: "46", label: "Insert Sets" },
      { value: "6,140", label: "Numbered" },
      { value: "19", label: "SuperFractors" },
    ] as StatModal[],
  },
  {
    icon: (
      <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 15.75V18m-7.5-6.75h.008v.008H8.25v-.008zm0 2.25h.008v.008H8.25v-.008zm0 2.25h.008v.008H8.25v-.008zm0 2.25h.008v.008H8.25v-.008zm2.498-6.75h.007v.008h-.007v-.008zm0 2.25h.007v.008h-.007v-.008zm0 2.25h.007v.008h-.007v-.008zm0 2.25h.007v.008h-.007v-.008zm2.504-6.75h.008v.008h-.008v-.008zm0 2.25h.008v.008h-.008v-.008zm0 2.25h.008v.008h-.008v-.008zm0 2.25h.008v.008h-.008v-.008zm2.498-6.75h.008v.008h-.008v-.008zm0 2.25h.008v.008h-.008v-.008zM8.25 6h7.5v2.25h-7.5V6zM12 2.25c-1.892 0-3.758.11-5.593.322C5.307 2.7 4.5 3.65 4.5 4.757V19.5a2.25 2.25 0 002.25 2.25h10.5a2.25 2.25 0 002.25-2.25V4.757c0-1.108-.806-2.057-1.907-2.185A48.507 48.507 0 0012 2.25z" />
      </svg>
    ),
    title: "Break Hit Calculator",
    desc: "Calculate the probability of pulling any athlete's card in a break — any card, numbered, or autograph. Powered by real pack odds and production data.",
    cta: { label: "Try the Calculator", href: "/resources/break-hit-calculator" },
    header: "1 Case",
    stats: [
      { value: "93.8%", label: "Any Card" },
      { value: "37.3%", label: "Numbered Parallel" },
      { value: "22.7%", label: "Autograph" },
    ] as StatModal[],
  },
];

/* Feature panel sticks at vertical center */
const PANEL_STICKY_TOP = "calc(50vh - 140px)";

/* ─── Floating Card Component ─────────────────────────────────────────────── */
function FloatingCard({
  mouseX,
  mouseY,
  size = 280,
}: {
  mouseX: number;
  mouseY: number;
  size?: number;
}) {
  const tiltX = (mouseY - 0.5) * 20;
  const tiltY = (mouseX - 0.5) * -20;
  const shineX = mouseX * 100;
  const shineY = mouseY * 100;
  const h = Math.round(size * (390 / 280));

  return (
    <div
      className="relative overflow-hidden"
      style={{
        width: size,
        height: h,
        transform: `perspective(800px) rotateX(${tiltX}deg) rotateY(${tiltY}deg)`,
        transformStyle: "preserve-3d",
        transition: "transform 0.1s ease-out",
        borderRadius: 0,
      }}
    >
      <img
        src="/hero-card-player.png"
        alt=""
        className="absolute inset-0 w-full h-full"
        style={{ objectFit: "cover", borderRadius: 0 }}
      />
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          background: `radial-gradient(circle at ${shineX}% ${shineY}%, rgba(232,255,71,0.15) 0%, transparent 50%)`,
          mixBlendMode: "screen",
        }}
      />
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          background: `linear-gradient(${135 + tiltY * 2}deg, rgba(124,109,250,0.1) 0%, transparent 40%, rgba(232,255,71,0.08) 100%)`,
        }}
      />
    </div>
  );
}

/* ─── Stat Modals Column ──────────────────────────────────────────────────── */
function StatModals({
  activeFeature,
  visible,
}: {
  activeFeature: number;
  visible: boolean;
}) {
  const feature = FEATURES[activeFeature];
  const stats = feature.stats;
  const header = "header" in feature ? (feature as { header: string }).header : null;
  // When header exists, it animates first (delay 0), then modals stagger after it
  const modalDelayOffset = header ? 1 : 0;

  return (
    <div className="flex flex-col gap-3 w-full">
      {/* Optional header (e.g. "1 Case") */}
      {header && (
        <div
          key={`${activeFeature}-header`}
          style={{
            opacity: visible ? 1 : 0,
            transform: visible ? "translateX(0)" : "translateX(40px)",
            transition: "opacity 0.4s ease-out 0ms, transform 0.4s ease-out 0ms",
            marginBottom: 4,
          }}
        >
          <p
            style={{
              fontSize: 64,
              fontFamily: "'DM Serif Display', serif",
              fontStyle: "italic",
              color: C.purple,
              lineHeight: 1.1,
            }}
          >
            {header}
          </p>
        </div>
      )}

      {/* Stat modals */}
      {stats.map((s, i) => (
        <div
          key={`${activeFeature}-${i}`}
          className="flex flex-col justify-center px-5 py-3"
          style={{
            background: "rgba(240,240,245,0.04)",
            border: "1px solid rgba(240,240,245,0.08)",
            borderRadius: 0,
            opacity: visible ? 1 : 0,
            transform: visible ? "translateX(0)" : "translateX(40px)",
            transition: `opacity 0.4s ease-out ${(i + modalDelayOffset) * 150}ms, transform 0.4s ease-out ${(i + modalDelayOffset) * 150}ms`,
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
            <p
              className="font-bold leading-tight"
              style={{ fontSize: 48, fontFamily: "'DM Serif Display', serif", color: C.accent }}
            >
              {s.value}
            </p>
            <p style={{ fontSize: 24, fontFamily: "'DM Serif Display', serif", color: "#ffffff" }}>
              {s.label}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
}

/* ─── Main Page ───────────────────────────────────────────────────────────── */
export default function Homepage2() {
  useFontLink();

  const [activeFeature, setActiveFeature] = useState(0);
  const [modalsVisible, setModalsVisible] = useState(false);
  const [fadedPanels, setFadedPanels] = useState<Set<number>>(new Set());
  const [mousePos, setMousePos] = useState({ x: 0.5, y: 0.5 });
  const panelRefs = useRef<(HTMLDivElement | null)[]>([]);

  const activeRef = useRef(0);
  const modalsEverShownRef = useRef(false);
  const updateFeature = useCallback((idx: number) => {
    if (idx !== activeRef.current) {
      activeRef.current = idx;
      setActiveFeature(idx);
    }
  }, []);

  /* IntersectionObserver for panel visibility */
  useEffect(() => {
    const scrollRoot = document.querySelector("[data-scroll-root]");
    if (!scrollRoot) return;

    const observer = new IntersectionObserver(
      (entries) => {
        let anyVisible = false;
        let bestIdx = activeRef.current;
        let bestRatio = 0;
        for (const entry of entries) {
          const idx = Number(entry.target.getAttribute("data-panel-idx"));
          if (entry.isIntersecting && entry.intersectionRatio >= 0.5) {
            anyVisible = true;
            if (entry.intersectionRatio > bestRatio) {
              bestRatio = entry.intersectionRatio;
              bestIdx = idx;
            }
          }
        }

        if (anyVisible) {
          modalsEverShownRef.current = true;
          setModalsVisible(true);
        } else if (!modalsEverShownRef.current || activeRef.current > 0) {
          /* Hide modals if they haven't been shown yet, or if we're past F0.
             When activeFeature is 0 and modals have been shown, keep them
             visible through the F0→F1 gap so they don't animate out. */
          setModalsVisible(false);
        }

        if (bestRatio >= 0.5) {
          updateFeature(bestIdx);
        }
      },
      { root: scrollRoot, threshold: [0, 0.25, 0.5, 0.75, 1] },
    );

    for (const ref of panelRefs.current) {
      if (ref) observer.observe(ref);
    }
    return () => observer.disconnect();
  }, [updateFeature]);

  /* Scroll listener — fade features 0 & 1 at 80% scroll progress */
  useEffect(() => {
    const scrollRoot = document.querySelector("[data-scroll-root]");
    if (!scrollRoot) return;

    const handleScroll = () => {
      const rootRect = scrollRoot.getBoundingClientRect();
      const newFaded = new Set<number>();
      for (let i = 0; i < 1; i++) {
        const wrapper = panelRefs.current[i];
        if (!wrapper) continue;
        const rect = wrapper.getBoundingClientRect();
        const scrolledPast = rootRect.top - rect.top;
        const progress = scrolledPast / rect.height;
        if (progress > 0.8) {
          newFaded.add(i);
        }
      }
      setFadedPanels((prev) => {
        if (prev.size === newFaded.size && [...prev].every((v) => newFaded.has(v))) return prev;
        return newFaded;
      });
    };

    scrollRoot.addEventListener("scroll", handleScroll, { passive: true });
    return () => scrollRoot.removeEventListener("scroll", handleScroll);
  }, []);

  /* Mouse tracking for 3D tilt */
  const handleMouseMove = useCallback((e: MouseEvent) => {
    setMousePos({
      x: e.clientX / window.innerWidth,
      y: e.clientY / window.innerHeight,
    });
  }, []);

  useEffect(() => {
    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, [handleMouseMove]);

  return (
    <div
      data-scroll-root
      className="h-full overflow-y-auto scroll-smooth"
      style={{ background: C.bg, fontFamily: "'DM Sans', sans-serif", color: C.text }}
    >
      {/* ── 1. Fixed Nav ─────────────────────────────────────────────────────── */}
      <nav
        className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-6 lg:px-10 h-16"
        style={{
          background: "rgba(10,10,15,0.85)",
          backdropFilter: "blur(12px)",
          borderBottom: "1px solid rgba(107,107,128,0.15)",
        }}
      >
        <Link href="/homepage-2" className="text-xl font-bold" style={{ fontFamily: "'DM Serif Display', serif" }}>
          Checklist<span style={{ color: C.accent }}>&sup2;</span>
        </Link>
        <div className="hidden md:flex items-center gap-8">
          {[
            { label: "Checklists", href: "/checklists" },
            { label: "Sets", href: "/sets" },
            { label: "Resources", href: "/resources" },
            { label: "Articles", href: "/articles" },
          ].map((l) => (
            <Link
              key={l.label}
              href={l.href}
              className="text-sm font-medium transition-colors hover:opacity-100"
              style={{ color: C.muted }}
              onMouseEnter={(e) => (e.currentTarget.style.color = C.text)}
              onMouseLeave={(e) => (e.currentTarget.style.color = C.muted)}
            >
              {l.label}
            </Link>
          ))}
        </div>
        <Link
          href="/checklists"
          className="hidden sm:inline-flex items-center gap-2 px-5 py-2 rounded-lg text-sm font-semibold transition-all"
          style={{ background: C.accent, color: C.bg }}
        >
          Browse Checklists
        </Link>
      </nav>

      {/* ── 2. Hero — centered stacked layout ────────────────────────────────── */}
      <section className="relative pt-32 pb-32 px-6 overflow-hidden">
        {/* Radial gradient glow */}
        <div
          className="absolute inset-0 pointer-events-none"
          style={{
            background:
              "radial-gradient(ellipse 80% 50% at 50% 0%, rgba(124,109,250,0.12) 0%, transparent 60%), radial-gradient(ellipse 60% 40% at 50% 0%, rgba(232,255,71,0.06) 0%, transparent 50%)",
          }}
        />

        <div className="relative z-10 max-w-3xl mx-auto text-center">
          {/* Badge */}
          <div
            className="inline-flex items-center gap-2 rounded-full px-4 py-1.5 text-xs font-medium mb-8"
            style={{ background: "rgba(232,255,71,0.08)", border: "1px solid rgba(232,255,71,0.2)", color: C.accent }}
          >
            <span className="w-1.5 h-1.5 rounded-full animate-pulse" style={{ background: C.accent }} />
            Now Live — 30+ Sets Tracked
          </div>

          {/* H1 */}
          <h1
            className="text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight leading-[1.08] mb-6"
            style={{ fontFamily: "'DM Serif Display', serif" }}
          >
            Every Card.{" "}
            <span style={{ color: C.purple, fontStyle: "italic" }}>Every Set.</span>
            <br />
            Every Break.
          </h1>

          {/* Description */}
          <p className="text-lg sm:text-xl max-w-[600px] mx-auto mb-10 leading-relaxed" style={{ color: C.muted }}>
            The modern sports card checklist. Search any athlete, browse any set, and understand your break odds — all in one place.
          </p>

          {/* CTAs */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-6">
            <Link
              href="/checklists"
              className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl text-base font-bold transition-all shadow-lg"
              style={{ background: C.accent, color: C.bg, boxShadow: "0 8px 32px rgba(232,255,71,0.2)" }}
            >
              Browse Checklists
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
              </svg>
            </Link>
            <Link
              href="#features"
              className="inline-flex items-center gap-2 text-base font-medium px-6 py-3.5 rounded-xl transition-colors"
              style={{ color: C.muted, border: "1px solid rgba(107,107,128,0.3)" }}
            >
              View Break Calculator
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
              </svg>
            </Link>
          </div>

          {/* Spacer between CTAs and card below */}
          <div style={{ height: 120 }} />

          {/* Scroll indicator */}
          <div className="animate-bounce inline-block" style={{ color: "rgba(107,107,128,0.5)" }}>
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
            </svg>
          </div>
        </div>
      </section>

      {/* ── 3. Feature Scroll Section — 3-column: panels | card | modals ─── */}
      <section id="features" className="relative">
        <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-[30fr_40fr_30fr] gap-0">

          {/* LEFT COLUMN (30%) — individual sticky panels that scroll up naturally */}
          <div className="relative px-6 lg:pl-8 lg:pr-4">
            {/* Spacer so first panel starts below the fold */}
            <div style={{ height: 400 }} />

            {FEATURES.map((f, i) => (
              <div
                key={f.title}
                ref={(el) => { panelRefs.current[i] = el; }}
                data-panel-idx={i}
                style={{ height: "150vh" }}
              >
                <div
                  className="sticky"
                  style={{
                    top: PANEL_STICKY_TOP,
                    opacity: fadedPanels.has(i) ? 0 : 1,
                    transition: "opacity 0.3s ease",
                  }}
                >
                  {/* Icon */}
                  <div
                    className="w-12 h-12 rounded-xl flex items-center justify-center mb-6"
                    style={{ background: "rgba(232,255,71,0.08)", color: C.accent }}
                  >
                    {f.icon}
                  </div>

                  {/* Title — hero-weight */}
                  <h3
                    className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-4 tracking-tight"
                    style={{ fontFamily: "'DM Serif Display', serif" }}
                  >
                    {f.title}
                  </h3>

                  {/* Description */}
                  <p
                    className="text-base sm:text-lg leading-relaxed max-w-md mb-6"
                    style={{ color: C.muted }}
                  >
                    {f.desc}
                  </p>

                  {/* CTA */}
                  {"cta" in f && (
                    <Link
                      href={(f as { cta: { label: string; href: string } }).cta.href}
                      className="inline-flex items-center gap-2 text-base font-medium transition-colors"
                      style={{ color: C.muted, borderBottom: "1px solid rgba(107,107,128,0.3)" }}
                      onMouseEnter={(e) => (e.currentTarget.style.color = C.text)}
                      onMouseLeave={(e) => (e.currentTarget.style.color = C.muted)}
                    >
                      {(f as { cta: { label: string; href: string } }).cta.label} &rarr;
                    </Link>
                  )}
                </div>
              </div>
            ))}

            {/* Bottom spacer */}
            <div style={{ height: "40vh" }} />
          </div>

          {/* CENTER COLUMN (40%) — single sticky card */}
          <div className="hidden lg:block relative">
            <div
              className="sticky flex items-center justify-center"
              style={{ top: "50vh", transform: "translateY(-50%)", height: "auto" }}
            >
              <div style={{ animation: "hp2-float 6s ease-in-out infinite" }}>
                <FloatingCard mouseX={mousePos.x} mouseY={mousePos.y} size={320} />
              </div>
            </div>
          </div>

          {/* RIGHT COLUMN (30%) — sticky stat modals */}
          <div className="hidden lg:block relative">
            <div
              className="sticky flex items-center pr-8"
              style={{ top: "50vh", transform: "translateY(-50%)", height: "auto" }}
            >
              <StatModals
                activeFeature={activeFeature}
                visible={modalsVisible}
              />
            </div>
          </div>
        </div>
      </section>

      {/* ── 4. Break Sheet Builder Showcase ──────────────────────────────────── */}
      <section style={{ background: "#111118", padding: "120px 0" }}>
        <div className="max-w-7xl mx-auto px-6 lg:px-10 grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          {/* Left — description */}
          <div>
            <p
              className="text-xs font-semibold uppercase tracking-widest mb-4"
              style={{ color: C.accent }}
            >
              Break Sheet Builder
            </p>
            <h2
              className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-6 tracking-tight"
              style={{ fontFamily: "'DM Serif Display', serif" }}
            >
              Export your break sheet in{" "}
              <span style={{ color: C.purple, fontStyle: "italic" }}>one click</span>
            </h2>
            <p
              className="text-base sm:text-lg leading-relaxed mb-10 max-w-lg"
              style={{ color: C.muted }}
            >
              Generate a Whatnot-ready CSV with every athlete in the set. Customize your listing type, tag autographs and rookies, and download in seconds.
            </p>
            <Link
              href="/checklists"
              className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl text-base font-bold transition-all"
              style={{ background: C.accent, color: C.bg, boxShadow: "0 8px 32px rgba(232,255,71,0.15)" }}
            >
              Build a Break Sheet &rarr;
            </Link>
          </div>

          {/* Right — screenshot */}
          <div className="flex justify-center lg:justify-end">
            <div
              style={{
                transform: "perspective(1200px) rotateY(-4deg) rotateX(2deg)",
                transformStyle: "preserve-3d",
                boxShadow: "0 32px 80px rgba(0,0,0,0.5), 0 0 0 1px rgba(240,240,245,0.06)",
                borderRadius: 0,
                overflow: "hidden",
                maxWidth: 560,
                width: "100%",
              }}
            >
              <img
                src="/break-sheet-preview.png"
                alt="Break Sheet Builder preview"
                className="w-full h-auto block"
                style={{ borderRadius: 0 }}
              />
            </div>
          </div>
        </div>
      </section>

      {/* ── 5. Stats Bar ──────────────────────────────────────────────────────── */}
      <section
        className="px-6 py-20"
        style={{ borderTop: "1px solid rgba(107,107,128,0.15)", borderBottom: "1px solid rgba(107,107,128,0.15)" }}
      >
        <div className="max-w-5xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          {[
            { value: "30+", label: "Sets Tracked" },
            { value: "25k+", label: "Cards Indexed" },
            { value: "7k+", label: "Athletes" },
            { value: "2k+", label: "Parallels Tracked" },
          ].map((s) => (
            <div key={s.label}>
              <p className="text-4xl sm:text-5xl font-bold mb-2" style={{ fontFamily: "'DM Serif Display', serif", color: C.text }}>
                {s.value}
              </p>
              <p className="text-sm" style={{ color: C.muted }}>{s.label}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── 5. How It Works ──────────────────────────────────────────────────── */}
      <section className="px-6 py-24">
        <div className="max-w-5xl mx-auto">
          <p className="text-xs font-semibold uppercase tracking-widest text-center mb-4" style={{ color: C.accent }}>
            How It Works
          </p>
          <h2 className="text-3xl sm:text-4xl font-bold text-center mb-16" style={{ fontFamily: "'DM Serif Display', serif" }}>
            Three steps to smarter breaks
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              { step: "01", title: "Search", desc: "Find any set or athlete across every sport. Full checklists with every base card, insert, and parallel." },
              { step: "02", title: "Review Odds", desc: "See official pack odds, box configuration, and calculate your probability of pulling any athlete's card." },
              { step: "03", title: "Break with Confidence", desc: "Know exactly what you're getting into. Make informed decisions backed by real data, not guesswork." },
            ].map((item) => (
              <div
                key={item.step}
                className="relative rounded-2xl p-8 overflow-hidden"
                style={{ background: "rgba(107,107,128,0.06)", border: "1px solid rgba(107,107,128,0.12)" }}
              >
                <span
                  className="absolute top-4 right-6 text-7xl font-bold pointer-events-none select-none"
                  style={{ fontFamily: "'DM Serif Display', serif", color: "rgba(107,107,128,0.07)" }}
                >
                  {item.step}
                </span>
                <div className="relative z-10">
                  <p className="text-xs font-semibold uppercase tracking-widest mb-4" style={{ color: C.purple }}>
                    Step {item.step}
                  </p>
                  <h3 className="text-xl font-bold mb-3" style={{ fontFamily: "'DM Serif Display', serif" }}>
                    {item.title}
                  </h3>
                  <p className="text-sm leading-relaxed" style={{ color: C.muted }}>{item.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── 6. CTA Section ───────────────────────────────────────────────────── */}
      <section className="px-6 py-24">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-6" style={{ fontFamily: "'DM Serif Display', serif" }}>
            Ready to break <span style={{ color: C.purple, fontStyle: "italic" }}>smarter</span>?
          </h2>
          <p className="text-lg mb-10" style={{ color: C.muted }}>
            Join thousands of collectors using Checklist&sup2; to make better break decisions.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              href="/checklists"
              className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl text-base font-bold transition-all"
              style={{ background: C.accent, color: C.bg }}
            >
              Browse Checklists
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
              </svg>
            </Link>
            <Link
              href="/sets"
              className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl text-base font-medium transition-colors"
              style={{ color: C.muted, border: "1px solid rgba(107,107,128,0.3)" }}
            >
              View All Sets
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
              </svg>
            </Link>
          </div>
        </div>
      </section>

      {/* ── 7. Footer ────────────────────────────────────────────────────────── */}
      <footer
        className="px-6 lg:px-10 py-8 flex items-center justify-between"
        style={{ borderTop: "1px solid rgba(107,107,128,0.15)" }}
      >
        <Link href="/homepage-2" className="text-lg font-bold" style={{ fontFamily: "'DM Serif Display', serif" }}>
          Checklist<span style={{ color: C.accent }}>&sup2;</span>
        </Link>
        <p className="text-xs" style={{ color: C.muted }}>
          &copy; {new Date().getFullYear()} Checklist&sup2;. All rights reserved.
        </p>
      </footer>

      {/* ── Keyframes ────────────────────────────────────────────────────────── */}
      <style jsx global>{`
        @keyframes hp2-float {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-12px); }
        }
      `}</style>
    </div>
  );
}
