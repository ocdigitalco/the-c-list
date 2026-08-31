import React from "react";

/**
 * Checklist² wordmark: the word "Checklist" in the display face (Carter One,
 * single weight 400) followed by a red superscript "mark" — the digit "2" on a
 * Card-Red portrait trading card (5:7, i.e. 2.5" × 3.5") with white paper text.
 * The card's bottom edge sits at the cap line; its extra height rises above it,
 * and the "2" sits in the lower ~60% of the card. Shared by header and footer.
 *
 * `size` is the font-size of "Checklist" in px; the mark scales from it.
 */
export function Wordmark({
  size = 24,
  ink = "var(--brand-ink)",
  accent = "var(--brand-accent)",
  paper = "var(--brand-paper)",
}: {
  size?: number;
  ink?: string;
  accent?: string;
  paper?: string;
}) {
  const markW = Math.round(size * 0.34);            // width unchanged from the old square
  const markH = Math.round((markW * 7) / 5);        // 5:7 portrait trading-card proportions
  const markFont = Math.round(size * 0.24);
  const padBottom = Math.round(markH * 0.2);
  const padTop = Math.round(markH * 0.4);           // ≈ 2× padBottom → glyph center ~60% of card
  // Keep the card's BOTTOM edge where the old square sat; the added height grows upward.
  const markMarginTop = Math.round(size * 0.05) + markW - markH;
  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "flex-start",
        fontFamily: "var(--brand-font-head)",
        fontSynthesisWeight: "none",
        lineHeight: 1,
      }}
    >
      <span style={{ fontSize: size, fontWeight: 400, color: ink, lineHeight: 1, letterSpacing: "-0.01em" }}>
        Checklist
      </span>
      <span
        aria-hidden="true"
        style={{
          display: "inline-flex",
          alignItems: "center",
          justifyContent: "center",
          boxSizing: "border-box",
          width: markW,
          height: markH,
          paddingTop: padTop,
          paddingBottom: padBottom,
          marginLeft: Math.round(size * 0.06),
          marginTop: markMarginTop,
          background: accent,
          color: paper,
          fontFamily: "var(--brand-font-head)",
          fontWeight: 400,
          fontSynthesisWeight: "none",
          fontSize: markFont,
          lineHeight: 1,
          borderRadius: 1,
          letterSpacing: 0,
        }}
      >
        2
      </span>
    </span>
  );
}
