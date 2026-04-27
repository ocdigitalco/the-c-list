"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import type { LeaderboardEntry } from "./page";

// ─── Types ────────────────────────────────────────────────────────────────────

interface Props {
  views: LeaderboardEntry[];
  searches: LeaderboardEntry[];
  allSports: string[];
  currentRange: string;
  currentSport: string | null;
}

// ─── Headshot helpers ─────────────────────────────────────────────────────────

function getHeadshotUrl(e: LeaderboardEntry): string | null {
  if (e.nbaPlayerId) return `https://cdn.nba.com/headshots/nba/latest/1040x760/${e.nbaPlayerId}.png`;
  if (e.ufcImageUrl) return e.ufcImageUrl;
  if (e.mlbPlayerId) return `https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:67:current.png/w_213,q_auto:best/v1/people/${e.mlbPlayerId}/headshot/67/current`;
  if (e.imageUrl) return e.imageUrl;
  return null;
}

function Initials({ name }: { name: string }) {
  const initials = name.split(" ").map((n) => n[0]).slice(0, 2).join("").toUpperCase();
  return (
    <div
      className="w-10 h-10 rounded-full flex items-center justify-center text-sm font-semibold shrink-0"
      style={{ background: "#F1EFE9", color: "#8A8677" }}
    >
      {initials}
    </div>
  );
}

function Avatar({ entry }: { entry: LeaderboardEntry }) {
  const url = getHeadshotUrl(entry);
  if (!url) return <Initials name={entry.playerName} />;
  return (
    <img
      src={url}
      alt={entry.playerName}
      className="w-10 h-10 rounded-full object-cover object-top shrink-0"
      style={{ border: "2px solid #EDEAE0" }}
      onError={(e) => { (e.currentTarget as HTMLImageElement).style.display = "none"; }}
    />
  );
}

// ─── Constants ────────────────────────────────────────────────────────────────

const RANGES = [
  { label: "24h", value: "24h" },
  { label: "7 days", value: "7d" },
  { label: "30 days", value: "30d" },
  { label: "1 year", value: "1y" },
  { label: "All time", value: "all" },
];

const SPORTS = [
  "All", "Basketball", "Baseball", "Soccer", "MMA", "Wrestling",
  "Racing", "Football", "Entertainment", "Other",
];

// ─── Component ────────────────────────────────────────────────────────────────

export function SearchesClient({
  views,
  searches,
  allSports,
  currentRange,
  currentSport,
}: Props) {
  const router = useRouter();
  const availableSports = SPORTS.filter((s) => s === "All" || allSports.includes(s));

  function navigate(range: string, sport: string | null) {
    const params = new URLSearchParams();
    params.set("range", range);
    if (sport) params.set("sport", sport);
    router.push(`/searches?${params.toString()}`);
  }

  return (
    <div className="h-full overflow-y-auto" style={{ background: "#FAFAF7" }}>
      <div className="mx-auto cl-container" style={{ maxWidth: 1440, padding: "40px 56px 80px" }}>
        {/* Breadcrumb */}
        <a href="/" style={{ fontSize: 13, color: "#6B6757", textDecoration: "none", fontFamily: "var(--cl-font-display)" }}>
          &lsaquo; Home
        </a>

        {/* Title */}
        <h1
          className="cl-title"
          style={{ fontFamily: "var(--cl-font-display)", fontSize: 48, fontWeight: 600, letterSpacing: "-1.2px", color: "#0F0F0E", margin: "12px 0 0", lineHeight: 1.1 }}
        >
          Searches
        </h1>
        <p style={{ fontSize: 14, color: "#6B6757", margin: "6px 0 0" }}>
          Athletes being searched and viewed across Checklist&sup2;
        </p>

        {/* Time range pills */}
        <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar" style={{ marginTop: 24 }}>
          {RANGES.map((r) => {
            const active = currentRange === r.value;
            return (
              <button
                key={r.value}
                onClick={() => navigate(r.value, currentSport)}
                style={{
                  padding: active ? "8px 16px" : "8px 14px",
                  borderRadius: 999, fontSize: 13,
                  fontWeight: active ? 500 : 400,
                  color: active ? "#FAFAF7" : "#3A372F",
                  background: active ? "#0F0F0E" : "transparent",
                  border: active ? "1px solid #0F0F0E" : "1px solid transparent",
                  cursor: "pointer", transition: "all 0.15s", flexShrink: 0,
                }}
                onMouseEnter={(e) => { if (!active) (e.currentTarget as HTMLElement).style.background = "#F1EFE9"; }}
                onMouseLeave={(e) => { if (!active) (e.currentTarget as HTMLElement).style.background = "transparent"; }}
              >
                {r.label}
              </button>
            );
          })}
        </div>

        {/* Sport filter */}
        <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar" style={{ marginTop: 12 }}>
          {availableSports.map((sp) => {
            const active = sp === "All" ? !currentSport : currentSport === sp;
            return (
              <button
                key={sp}
                onClick={() => navigate(currentRange, sp === "All" ? null : sp)}
                style={{
                  padding: active ? "8px 16px" : "8px 14px",
                  borderRadius: 999, fontSize: 13,
                  fontWeight: active ? 500 : 400,
                  color: active ? "#FAFAF7" : "#3A372F",
                  background: active ? "#0F0F0E" : "transparent",
                  border: active ? "1px solid #0F0F0E" : "1px solid transparent",
                  cursor: "pointer", transition: "all 0.15s", flexShrink: 0,
                }}
                onMouseEnter={(e) => { if (!active) (e.currentTarget as HTMLElement).style.background = "#F1EFE9"; }}
                onMouseLeave={(e) => { if (!active) (e.currentTarget as HTMLElement).style.background = "transparent"; }}
              >
                {sp}
              </button>
            );
          })}
        </div>

        {/* Sections */}
        <div className="space-y-10" style={{ marginTop: 36 }}>
          <Section title="Most Viewed" entries={views} countLabel="views" />
          <Section title="Most Searched" entries={searches} countLabel="searches" />
        </div>
      </div>
    </div>
  );
}

// ─── Section ──────────────────────────────────────────────────────────────────

function Section({
  title,
  entries,
  countLabel,
}: {
  title: string;
  entries: LeaderboardEntry[];
  countLabel: string;
}) {
  if (entries.length === 0) {
    return (
      <div>
        <h2 style={{ fontFamily: "var(--cl-font-mono)", fontSize: 10, fontWeight: 600, letterSpacing: 2, color: "#3A372F", marginBottom: 12 }}>
          {title.toUpperCase()}
        </h2>
        <div style={{ border: "1px dashed #D9D5C7", borderRadius: 12, padding: "60px 20px", textAlign: "center" }}>
          <p style={{ fontSize: 14, fontWeight: 500, color: "#3A372F" }}>No data for this time range</p>
          <p style={{ fontSize: 12, color: "#8A8677", marginTop: 6 }}>Try selecting a longer range or clearing filters.</p>
        </div>
      </div>
    );
  }

  return (
    <div>
      <h2 style={{ fontFamily: "var(--cl-font-mono)", fontSize: 10, fontWeight: 600, letterSpacing: 2, color: "#3A372F", marginBottom: 12 }}>
        {title.toUpperCase()}
        <span style={{ color: "#B7B2A3", marginLeft: 8 }}>{entries.length} ATHLETES</span>
      </h2>
      <div style={{ background: "#FFFFFF", border: "1px solid #EDEAE0", borderRadius: 10, overflow: "hidden" }}>
        {entries.map((entry, i) => {
          const href = entry.setSlug && entry.slug
            ? `/sets/${entry.setSlug}/athlete/${entry.slug}`
            : null;

          const content = (
            <div className="flex items-center gap-3" style={{ padding: "12px 18px", borderTop: i > 0 ? "1px solid #F1EEE3" : undefined }}>
              {/* Rank */}
              <span
                style={{
                  fontFamily: "var(--cl-font-mono)", fontSize: 12, fontWeight: 600, width: 24, textAlign: "right", flexShrink: 0,
                  color: i === 0 ? "#D97706" : i === 1 ? "#6B6757" : i === 2 ? "#92400E" : "#B7B2A3",
                }}
              >
                {i + 1}
              </span>

              {/* Avatar */}
              <Avatar entry={entry} />

              {/* Info */}
              <div className="flex-1 min-w-0">
                <p style={{ fontFamily: "var(--cl-font-display)", fontSize: 14, fontWeight: 500, color: "#0F0F0E", letterSpacing: "-0.1px" }} className="truncate">
                  {entry.playerName}
                </p>
                <div className="flex items-center gap-1.5" style={{ marginTop: 2 }}>
                  <span style={{ fontSize: 11, color: "#8A8677" }}>{entry.sport}</span>
                  <span style={{ fontSize: 11, color: "#D9D5C7" }}>·</span>
                  <span style={{ fontSize: 11, color: "#B7B2A3" }} className="truncate">{entry.setName}</span>
                </div>
              </div>

              {/* Count */}
              <span style={{ fontFamily: "var(--cl-font-mono)", fontSize: 12, fontWeight: 600, color: "#0F0F0E", flexShrink: 0 }}>
                {entry.eventCount.toLocaleString()}
                <span style={{ color: "#B7B2A3", fontWeight: 400, marginLeft: 4 }}>{countLabel}</span>
              </span>
            </div>
          );

          return href ? (
            <Link
              key={i}
              href={href}
              style={{ display: "block", textDecoration: "none", transition: "background 0.15s" }}
              onMouseEnter={(e) => { (e.currentTarget as HTMLElement).style.background = "#FDFCF8"; }}
              onMouseLeave={(e) => { (e.currentTarget as HTMLElement).style.background = "#FFFFFF"; }}
            >
              {content}
            </Link>
          ) : (
            <div key={i}>{content}</div>
          );
        })}
      </div>
    </div>
  );
}
