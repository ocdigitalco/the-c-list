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
  "2026-topps-gilded-collection-baseball": {
    about:
      "Gilded Collection is Topps' gold-themed premium baseball release. The 2026 edition has a 200-card chrome base set mixing current stars, the rookie class and legends, with every base card numbered to 99 and six rarer refractor parallels down to a one-of-one SuperFractor. Inserts are Gold Regalia (100 cards), Gold Storm (25) and Statuesque (4), which pictures player statues that stand outside MLB ballparks. New this year is 24K, a 24-card insert where every card is a one-of-one made of gold. Hobby boxes hold two packs of four cards and guarantee two autographs. Seven autograph subsets cover 207 cards, led by Topps Chrome Gold Autographs (67) and two Hall of Fame programs, plus the new Gilded Ink, signed in gold ink.",
    faq: [
      {
        q: "When does 2026 Topps Gilded Collection Baseball release?",
        a: "December 25, 2026.",
      },
      {
        q: "How many cards are in the set?",
        a: "The checklist has 560 cards across 12 subsets: 200 base, 153 inserts and 207 autographs.",
      },
      {
        q: "What is the 24K insert?",
        a: "A new 24-card insert for 2026. Topps describes each card as a one-of-one made of gold.",
      },
      {
        q: "What is in a hobby box?",
        a: "Two packs of four cards, with two autographs guaranteed per box. A case holds four boxes.",
      },
      {
        q: "Is every card numbered?",
        a: "Nearly. Base cards are numbered to 99, Gold Regalia to 79, Gold Storm to 26, and the autographs to 199, 99 or 25 depending on the subset. Only the four-card Statuesque insert is unnumbered in its standard version.",
      },
      {
        q: "Have pack odds been published?",
        a: "Not yet. This page will be updated when Topps releases the odds sheet.",
      },
    ],
  },
  "2026-topps-chrome-football": {
    about:
      "2026 Topps Chrome Football is the flagship chrome release for the NFL: a 400-card base set with 100 rookies from the 2026 draft class, including Fernando Mendoza, Jeremiyah Love, Carnell Tate, Jordyn Tyson and Caleb Downs. Each box type has its own refractor family, from Prism in Hobby and Wave in Jumbo to Geometric in Breaker Delight, RayWave and Football Leather in Value Blasters, Pulsar in Hangers and X-Fractors in Megas. Short-print inserts Kaiju, Helix, Ultra Violet, Tecmo and Game Genies return, joined by Glass Canvas, Madden 99 Club and Super Bowl at Night. Autographs include 1/1 Prem1ere Patch Autographs from the 2023 and 2024 rookie classes and NFL Honors Gold Shield Autographs.",
    faq: [
      {
        q: "When does 2026 Topps Chrome Football release?",
        a: "Hobby and retail formats release November 18, 2026. First Day Issue boxes released November 13, 2026, and Mega boxes follow on December 2, 2026.",
      },
      {
        q: "How many autographs are in a 2026 Topps Chrome Football box?",
        a: "A Hobby box has 1 autograph. A Jumbo box has 2. A First Day Issue Jumbo box has 3, one of them a Molten Mercury autograph. A Breaker Delight box has 2, one of them a Geometric autograph. Mega, Value Blaster and Hanger boxes have no guaranteed autograph.",
      },
      {
        q: "Which parallels are exclusive to each 2026 Topps Chrome Football box?",
        a: "Prism Refractors are Hobby only. Molten Mercury /11 is First Day Issue only. Wave Refractors are in Jumbo and First Day Issue. Geometric Refractors are Breaker Delight only. RayWave, Red White & Blue and Football Leather are Value Blaster only. Pulsar Refractors are Hanger only. X-Fractors are Mega only. LogoFractors are in Fanatics boxes.",
      },
      {
        q: "What are the rarest cards in 2026 Topps Chrome Football?",
        a: "The Gold Shield Dual Autograph of Josh Allen and Matthew Stafford is a 1/1 at 1:9,717,960 Hobby packs. The Lombardi Trophy SuperFractor is a Hobby-only 1/1 at 1:2,776,560 packs, and the 2023 and 2024 Prem1ere Patch Autographs are all 1/1s.",
      },
    ],
  },
  "2026-topps-composite-formula-1": {
    about:
      "2026 Topps Composite Formula 1 puts seven Topps brands into one F1 release: Paddock Pass, Chrome Black, Allen & Ginter, Cosmic Chrome, Midnight, Heritage and Resurgence each contribute their own design across a 225-card base set. The checklist covers all 22 current drivers, including rookie Arvid Lindblad, along with team principals and legends from Fangio to Räikkönen. The Allen & Ginter section adds circuit landmarks and two paddock animals, Gary the Groundhog and Lionel the Lizard, and The Grail continues with three new cards. Parallels and pack odds will be added when Topps publishes them.",
    faq: [
      {
        q: "What comes in a 2026 Topps Composite Formula 1 box?",
        a: "A Hobby box has 20 packs of 8 cards with 4 numbered parallels, 12 inserts and 36 Chrome cards; a case holds 12 boxes. A Value Blaster box has 5 packs of 8 cards with 6 inserts and 7 Chrome cards.",
      },
      {
        q: "Which brands are in Topps Composite Formula 1?",
        a: "The base set is built from Paddock Pass, Chrome Black, Allen & Ginter, Cosmic Chrome, Midnight, World on Wheels and Resurgence designs, with Heritage represented in the F1 Flashbacks insert.",
      },
      {
        q: "What is exclusive to Value Blaster boxes?",
        a: "Topps lists Base Chrome Resurgence Purple & Yellow Static and Sky Blue & Pink Shock parallels as Value Box exclusives.",
      },
      {
        q: "What autographs and relics are in Topps Composite Formula 1?",
        a: "Autographs come in Paddock Pass, Chrome Black, Allen & Ginter and Gilded designs. Composite Swatch Autographs combine a signature and a relic, and there are four relic sets: Allen & Ginter Relics, Push the Limits, Top Crop and the jumbo Grand Slam Relics.",
      },
      {
        q: "Are parallels and pack odds available for 2026 Topps Composite Formula 1?",
        a: "Not yet. Topps has published the checklist and box configuration; parallels and odds will be added when released.",
      },
    ],
  },
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
