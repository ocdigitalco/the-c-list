import React from "react";
import { initials as toInitials, sportTint } from "@/lib/athletes/util";

const FONT_DISPLAY = "var(--cl-font-display), var(--brand-font-head), system-ui, sans-serif";
const FONT_MONO = "var(--cl-font-mono), 'JetBrains Mono', ui-monospace, monospace";

/**
 * Sport-tinted monogram tile — the no-image stand-in used on the Athletes index
 * (5:7 tile with name + league) and, in `badge` form, as the master-page header
 * mark in place of a headshot. No card images exist in Stage 2, so every subject
 * uses this.
 */
export function MonogramTile({
  name,
  sport,
  league,
  trending = false,
}: {
  name: string;
  sport: string;
  league?: string | null;
  trending?: boolean;
}) {
  const ink = "#ffffff";
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
      {trending && (
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
          }}
        >
          TRENDING
        </span>
      )}
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

/** Square monogram mark for the master-page header (replaces the headshot). */
export function MonogramBadge({ name, sport, size = 132 }: { name: string; sport: string; size?: number }) {
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
