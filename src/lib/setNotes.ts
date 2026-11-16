/**
 * Per-set custom copy (human-written), keyed by set slug.
 *
 * `about` renders as a paragraph under the "About This Set" header on the set
 * page's Overview tab, above the data-computed summary. `faq` entries are
 * appended to the generated Q&A and are included in the FAQPage JSON-LD, so the
 * visible Q&A and the structured data stay in sync.
 *
 * Everything the data can compute already lives in setSeo.ts; this file is only
 * for prose the data cannot derive. Keep it generic — any set may add an entry.
 */

export interface SetNote {
  about?: string;
  faq?: { q: string; a: string }[];
}

export const SET_NOTES: Record<string, SetNote> = {
  "2026-topps-royalty-tennis": {
    about:
      "2026 Topps Royalty Tennis is the premium, hit-driven end of the Topps tennis line: one 10-card pack per box with six autographs, every base card numbered to 99, and a checklist that runs from current champions and rising players to legends like Nadal, Graf, Agassi and Borg. Memorabilia is the centerpiece. Racket Knob Relics and Racket Knob Autographs return as 1/1s built around the butt cap of a player's racket, The Grip and Superior Relic Signatures are back, and On-Court Shoe Relics are new for 2026 with pieces of match-used shoes. Dual, Triple and Quad autographs round out the signature content.",
    faq: [
      {
        q: "How much does a 2026 Topps Royalty Tennis hobby box cost?",
        a: "Topps opened presales on October 13, 2026 through an EQL raffle at $579.99 per hobby box. Release-day pricing on November 13, 2026 was $599.99.",
      },
      {
        q: "What is new in 2026 Topps Royalty Tennis?",
        a: "On-Court Shoe Relics are new for 2026, featuring match-used shoe pieces numbered to 5 with Brand Logo and Tongue Logo 1/1 versions. Racket Knob Relics, Racket Knob Autographs, The Grip and Superior Relic Signatures return.",
      },
      {
        q: "What are Racket Knob cards in Topps Royalty Tennis?",
        a: "Racket Knob Relics (81 cards) and Racket Knob Autographs (83 cards) each embed the knob from a player's racket. Every card is a 1/1; hobby odds are 1:149 and 1:145 packs.",
      },
    ],
  },
};

export function getSetNote(slug: string | null | undefined): SetNote | undefined {
  return slug ? SET_NOTES[slug] : undefined;
}
