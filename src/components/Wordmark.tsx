import React from "react";

/**
 * Checklist² wordmark: the word "Checklist" in the display face (Carter One,
 * single weight 400) followed by a red superscript square "mark" — the digit
 * "2" on a Card-Red tile with white paper text, aligned to the cap height.
 * Shared by the site header and footer.
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
  const box = Math.round(size * 0.34); // square mark ≈ 48% of cap height
  const markFont = Math.round(size * 0.24);
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
          width: box,
          height: box,
          marginLeft: Math.round(size * 0.06),
          marginTop: Math.round(size * 0.05),
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
