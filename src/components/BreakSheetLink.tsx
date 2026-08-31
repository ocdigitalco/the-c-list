"use client";

import Link from "next/link";

/**
 * Drop-in replacement for the set-page `BreakSheetModal` trigger. Instead of
 * opening the modal it links to the dedicated /break-sheet-builder page with the
 * set pre-selected. Kept prop-compatible with BreakSheetModal (extra props are
 * accepted but unused) so the swap is a one-line change and easy to revert — the
 * modal component itself is left in place until it's removed in a follow-up.
 */
interface BreakSheetLinkProps {
  slug: string;
  // Accepted for parity with BreakSheetModal; intentionally unused here.
  setName?: string;
  sport?: string;
  league?: string | null;
  players?: unknown;
}

export function BreakSheetLink(props: BreakSheetLinkProps) {
  return (
    <Link
      href={`/break-sheet-builder?set=${encodeURIComponent(props.slug)}`}
      className="flex items-center gap-1.5 shrink-0 text-sm font-semibold text-[var(--brand-head)] bg-[var(--brand-accent)] hover:bg-[var(--brand-accent-deep)] px-4 py-2 rounded-lg transition-colors"
      style={{ boxShadow: "var(--brand-shadow-btn)" }}
    >
      <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3"
        />
      </svg>
      Break Sheet
    </Link>
  );
}
