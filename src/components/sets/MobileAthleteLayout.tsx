"use client";

import { useEffect, useRef, useState } from "react";
import { AthleteHeadshot } from "./AthleteHeadshot";

interface Tab {
  id: string;
  label: string;
}

interface Props {
  playerName: string;
  teams: string[];
  hasRookie: boolean;
  nbaPlayerId: number | null | undefined;
  ufcImageUrl?: string | null;
  mlbPlayerId?: number | null;
  imageUrl?: string | null;
  stats: { label: string; value: number }[];
  setName: string;
  setHref: string;
  tabs: Tab[];
  /** Rendered inline on the breadcrumb row (right side) */
  leaderboardButton?: React.ReactNode;
  /** Keyed by tab id — only the active tab's content is shown */
  tabContent: Record<string, React.ReactNode>;
  /** Content shown below the tab panel (always visible) */
  children?: React.ReactNode;
}

export function MobileAthleteLayout({
  playerName,
  teams,
  hasRookie,
  nbaPlayerId,
  ufcImageUrl,
  mlbPlayerId,
  imageUrl,
  stats,
  setName,
  setHref,
  tabs,
  leaderboardButton,
  tabContent,
  children,
}: Props) {
  const [showStickyHeader, setShowStickyHeader] = useState(false);
  const [activeTab, setActiveTab] = useState(tabs[0]?.id ?? "");
  const heroRef = useRef<HTMLDivElement>(null);
  const activeIdx = tabs.findIndex((t) => t.id === activeTab);

  // Show sticky header once hero scrolls out of view
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => setShowStickyHeader(!entry.isIntersecting),
      { threshold: 0 }
    );
    if (heroRef.current) observer.observe(heroRef.current);
    return () => observer.disconnect();
  }, []);

  const tabBarEl = (
    <div className="relative">
      <div className="flex">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className="flex-1 py-2.5 text-xs text-center transition-colors"
            style={{
              fontWeight: activeTab === tab.id ? 700 : 400,
              color: activeTab === tab.id ? "var(--v2-text-primary)" : "var(--v2-text-secondary)",
            }}
          >
            {tab.label}
          </button>
        ))}
      </div>
      {/* Sliding underline indicator */}
      <div
        className="absolute bottom-0 h-[2px] transition-transform duration-200 ease-out"
        style={{
          width: `${100 / tabs.length}%`,
          transform: `translateX(${activeIdx * 100}%)`,
          background: "#6366f1",
        }}
      />
      {/* Bottom border for the whole bar */}
      <div className="absolute bottom-0 left-0 right-0 h-[1px]" style={{ background: "var(--v2-border)" }} />
    </div>
  );

  return (
    <div className="md:hidden min-h-screen" style={{ background: "var(--v2-page-bg)" }}>
      {/* Sticky header — appears on scroll */}
      <div
        className="fixed top-0 left-0 right-0 z-50 transition-transform duration-200"
        style={{
          transform: showStickyHeader ? "translateY(0)" : "translateY(-100%)",
          background: "var(--v2-card-bg)",
          borderBottom: "1px solid var(--v2-border)",
        }}
      >
        <div className="flex items-center gap-3 px-4 py-2.5">
          <AthleteHeadshot
            name={playerName}
            nbaPlayerId={nbaPlayerId ?? null}
            ufcImageUrl={ufcImageUrl}
            mlbPlayerId={mlbPlayerId}
            imageUrl={imageUrl}
            size="sm"
          />
          <div className="min-w-0 flex-1">
            <p className="text-sm font-bold truncate" style={{ color: "var(--v2-text-primary)" }}>
              {playerName}
            </p>
            <p className="text-xs truncate" style={{ color: "var(--v2-text-secondary)" }}>
              {setName}
            </p>
          </div>
        </div>
        {/* Tab bar inside sticky header */}
        {tabBarEl}
      </div>

      {/* Breadcrumb row — back link left, leaderboard button right */}
      <div className="flex items-center justify-between px-4 pt-4 pb-2">
        <a
          href={setHref}
          className="flex items-center gap-1 text-sm min-w-0"
          style={{ color: "var(--v2-text-secondary)" }}
        >
          <svg className="w-3.5 h-3.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
          </svg>
          <span className="truncate">{setName}</span>
        </a>
        {leaderboardButton}
      </div>

      {/* Hero section */}
      <div ref={heroRef} className="px-4 pb-4">
        <div className="flex items-center gap-4">
          <AthleteHeadshot
            name={playerName}
            nbaPlayerId={nbaPlayerId ?? null}
            ufcImageUrl={ufcImageUrl}
            mlbPlayerId={mlbPlayerId}
            imageUrl={imageUrl}
            size="lg"
          />
          <div className="flex-1 min-w-0">
            <h1 className="text-2xl font-bold leading-tight" style={{ color: "var(--v2-text-primary)" }}>
              {playerName}
            </h1>
            {teams.length > 0 && (
              <p className="text-sm mt-1" style={{ color: "var(--v2-text-secondary)" }}>
                {teams.join(" · ")}
              </p>
            )}
            {hasRookie && (
              <span
                className="inline-block text-xs font-semibold px-2 py-0.5 rounded mt-1.5"
                style={{ color: "var(--v2-accent)", background: "var(--v2-accent-light)" }}
              >
                Rookie
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Stat strip */}
      <div className="flex overflow-x-auto no-scrollbar px-4 gap-2 pb-4">
        {stats.map((s) => (
          <div
            key={s.label}
            className="shrink-0 flex-1 min-w-[80px] rounded-lg px-3 py-2.5 text-center"
            style={{
              background: "var(--v2-card-bg)",
              border: "1px solid var(--v2-border)",
            }}
          >
            <p
              className="text-lg font-bold"
              style={{ color: "var(--v2-accent)", fontVariantNumeric: "tabular-nums" }}
            >
              {s.value.toLocaleString()}
            </p>
            <p className="text-[10px] font-medium mt-0.5 leading-tight" style={{ color: "var(--v2-text-secondary)" }}>
              {s.label}
            </p>
          </div>
        ))}
      </div>

      {/* Static tab bar (visible until sticky header takes over) */}
      <div
        className="sticky top-0 z-40"
        style={{
          background: "var(--v2-page-bg)",
          display: showStickyHeader ? "none" : undefined,
        }}
      >
        {tabBarEl}
      </div>

      {/* Active tab content */}
      <div className="px-4 py-4 space-y-6">
        {tabContent[activeTab]}
      </div>

      {/* Always-visible content below tabs */}
      {children && (
        <div className="px-4 pb-4 space-y-6">
          {children}
        </div>
      )}
    </div>
  );
}
