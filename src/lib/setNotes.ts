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
  "2026-topps-pro-debut-baseball": {
    about:
      "2026 Topps Pro Debut Baseball is the official Minor League Baseball release in the Topps line: a 200-card base set of prospects pictured with their minor-league clubs, each with a Chrome version that falls six per pack. Arizona Fall League Stars, Pipeline Pairings and Pro Debut Gamers are new inserts this year, joining Stars of MiLB and Ballpark Promos. Future Cornerstones, Dual and Triple Autographs and Jumbo Autograph Relics return, and every Hobby Jumbo box carries four autographs.",
    faq: [
      {
        q: "What comes in a 2026 Topps Pro Debut Baseball box?",
        a: "A Hobby Jumbo box has 6 packs of 24 cards and 4 autographs. Each pack averages six Base Chrome cards. A case holds 8 boxes.",
      },
      {
        q: "Are there rookie cards in Topps Pro Debut?",
        a: "No. Pro Debut pictures prospects with their Minor League Baseball clubs before they reach the majors, so the cards carry no RC designation.",
      },
      {
        q: "What is new in 2026 Topps Pro Debut Baseball?",
        a: "Three inserts are new: 2025 Arizona Fall League Stars, Pipeline Pairings and Pro Debut Gamers. Stars of MiLB, Ballpark Promos, Future Cornerstones autographs, Dual and Triple Autographs and Jumbo Autograph Relics return.",
      },
      {
        q: "What are the rarest cards in 2026 Topps Pro Debut Baseball?",
        a: "By published odds, the Triple Autographs FoilFractor 1/1 (1:34,888 packs) and Dual Autographs FoilFractor 1/1 (1:32,562) are the hardest pulls, followed by the 2025 Arizona Fall League Stars Autographs FoilFractor 1/1 (1:28,731).",
      },
    ],
  },
  "2025-26-topps-x-bob-ross-the-joy-of-basketball": {
    about:
      "2025-26 Topps x Bob Ross The Joy of Basketball is the first Bob Ross collaboration in basketball cards: 105 current stars, rookies and Hall of Famers set against Ross's painted landscapes. The rookie class includes Cooper Flagg, Kon Knueppel and Dylan Harper, alongside LeBron James, Stephen Curry and Victor Wembanyama and legends such as Bill Russell, Oscar Robertson and Walt Frazier. Parallels are named for Ross's paint colors, from Sap Green to the 1-of-1 Midnight Black. Hobby Collector's Boxes also hold the short prints: Beauty is Everywhere, Peapod the Squirrel, and a Bob Ross card at 1:164 packs.",
    faq: [
      {
        q: "What comes in a Topps x Bob Ross The Joy of Basketball box?",
        a: "A Hobby Collector's Box has 8 packs of 8 cards with 1 autograph, 4 numbered parallels, 2 inserts and 1 SP or SSP variation. A Happy Little Box is a single 8-card pack; inserts fall 1:2 packs, the exclusive Easel parallel 1:4, a numbered parallel 1:3 and autographs 1:15.",
      },
      {
        q: "Which cards are only in Hobby Collector's Boxes?",
        a: "Beauty is Everywhere SP (1:11 packs), Peapod the Squirrel SP (1:41) and the Bob Ross Topps SSP (1:164) are found only in Hobby Collector's Boxes. The Easel parallel is found only in Happy Little Boxes.",
      },
      {
        q: "Are the autographs on-card or sticker?",
        a: "Both exist. Most autograph parallels are sticker autographs. On-card versions exist in Alizarin Crimson, Bright Red and Midnight Black and are far rarer, from 1:6,400 Hobby packs. Topps has not said which players signed on-card.",
      },
      {
        q: "Who are the rookies in Topps x Bob Ross The Joy of Basketball?",
        a: "Sixteen rookies are in the base set, cards 53 to 68, including Cooper Flagg, Kon Knueppel, Dylan Harper, Ace Bailey, VJ Edgecombe and Derik Queen.",
      },
    ],
  },
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
