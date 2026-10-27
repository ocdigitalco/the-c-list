import React from "react";
import { initials as toInitials, sportTint } from "@/lib/athletes/util";

const FONT_DISPLAY = "var(--cl-font-display), var(--brand-font-head), system-ui, sans-serif";
const FONT_MONO = "var(--cl-font-mono), 'JetBrains Mono', ui-monospace, monospace";

/**
 * Athlete index tile (5:7). Renders the headshot when one resolved
 * (`headshotUrl`), else a sport-tinted monogram with the subject's initials.
 * Same tile box either way, so photos and monograms mix with no layout shift.
 */
export function AthleteAvatar({
  name,
  sport,
  league,
  trending = false,
  headshotUrl = null,
}: {
  name: string;
  sport: string;
  league?: string | null;
  trending?: boolean;
  headshotUrl?: string | null;
}) {
  const ink = "#ffffff";
  const TrendingBadge = trending ? (
    <span
      style={{
        position: "absolute",
        top: 12,
        left: 0,
        background: "var(--brand-accent)",
        color: "#fff",
        font: `500 9.5px ${FONT_MONO}`,
        letterSpacing: "0.16em",
        padding: "4px 8px",
        zIndex: 2,
      }}
    >
      TRENDING
    </span>
  ) : null;

  if (headshotUrl) {
    return (
      <div
        style={{
          position: "relative",
          aspectRatio: "5 / 7",
          overflow: "hidden",
          borderRadius: 6,
          background: sportTint(sport),
        }}
      >
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={headshotUrl}
          alt=""
          loading="lazy"
          decoding="async"
          style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover", objectPosition: "top center" }}
        />
        {TrendingBadge}
        {/* Scrim + league, for legibility over any photo. */}
        <div
          style={{
            position: "absolute",
            insetInline: 0,
            bottom: 0,
            padding: "22px 12px 10px",
            background: "linear-gradient(to top, rgba(0,0,0,0.55), rgba(0,0,0,0))",
          }}
        >
          <span style={{ font: `500 10px ${FONT_MONO}`, letterSpacing: "0.14em", color: ink, opacity: 0.9 }}>
            {(league ?? sport ?? "").toUpperCase()}
          </span>
        </div>
      </div>
    );
  }

  return (
    <div
      style={{
        position: "relative",
        aspectRatio: "5 / 7",
        overflow: "hidden",
        background: sportTint(sport),
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        padding: 14,
        boxSizing: "border-box",
        borderRadius: 6,
      }}
    >
      {TrendingBadge}
      <span style={{ alignSelf: "flex-end", font: `500 10px ${FONT_MONO}`, letterSpacing: "0.14em", color: ink, opacity: 0.85 }}>
        {(league ?? sport ?? "").toUpperCase()}
      </span>
      <span style={{ font: `italic 800 56px/0.9 ${FONT_DISPLAY}`, letterSpacing: "-0.04em", color: ink }}>
        {toInitials(name)}
      </span>
      <span style={{ font: `600 12px/1.2 ${FONT_DISPLAY}`, color: ink, textTransform: "uppercase", letterSpacing: "0.02em", opacity: 0.95 }}>
        {name}
      </span>
    </div>
  );
}

/** Square master-page header mark: headshot when resolved, else monogram. */
export function AthleteBadge({
  name,
  sport,
  size = 132,
  headshotUrl = null,
}: {
  name: string;
  sport: string;
  size?: number;
  headshotUrl?: string | null;
}) {
  if (headshotUrl) {
    return (
      // eslint-disable-next-line @next/next/no-img-element
      <img
        src={headshotUrl}
        alt=""
        loading="lazy"
        decoding="async"
        style={{
          width: size,
          height: size,
          flex: "none",
          borderRadius: 14,
          objectFit: "cover",
          objectPosition: "top center",
          background: sportTint(sport),
        }}
      />
    );
  }
  return (
    <div
      style={{
        width: size,
        height: size,
        flex: "none",
        borderRadius: 14,
        background: sportTint(sport),
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        color: "#fff",
      }}
      aria-hidden
    >
      <span style={{ font: `italic 800 ${Math.round(size * 0.42)}px/1 ${FONT_DISPLAY}`, letterSpacing: "-0.04em" }}>
        {toInitials(name)}
      </span>
    </div>
  );
}
