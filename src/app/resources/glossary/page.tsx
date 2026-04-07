import type { Metadata } from "next";
import { PageShell } from "@/components/PageShell";

export const metadata: Metadata = {
  title: "Glossary — Checklist2",
  description: "A reference guide to the terms and data points used throughout Checklist2",
};

const terms: { term: string; definition: string }[] = [
  {
    term: "Athlete Leaderboard",
    definition:
      "A sortable ranking of athletes within a specific card set, showing who has the most cards, autographs, inserts, or numbered parallels in that release. Accessible from any set page via a slide-in panel, the leaderboard helps collectors and breakers quickly identify which athletes have the deepest card presence in a given set. Can be filtered by team and toggled to show rookie cards only.",
  },
  {
    term: "Athletes",
    definition:
      "The total number of unique players, fighters, drivers, wrestlers, or personalities who appear on at least one card in a set. A player appearing in multiple insert sets still counts as one athlete.",
  },
  {
    term: "Autograph Parallels",
    definition:
      "The total count of unique autograph parallel cards across the entire set. Calculated by taking every card appearance in every autograph insert set and multiplying by the number of parallel types attached to it. For example if a Stroke of Midnight Autographs insert set has 40 cards and 7 parallel types, that contributes 280 autograph parallels from that insert set alone. This number is typically in the hundreds for most sets and represents the full scope of autograph parallel production in the product. Parallel versions of the same autograph card are counted individually since each has its own print run and scarcity.",
  },
  {
    term: "Autographs",
    definition:
      "The total count of autograph card appearances across the entire set. This includes all autograph insert sets (single, dual, triple, relic, booklet, and memorabilia autographs) and counts each player appearance individually — meaning a dual autograph counts as two autograph appearances, one per player. Serialized parallel versions of autograph cards are not counted separately here since they are versions of the same autograph card, not additional autograph cards.",
  },
  {
    term: "Base Set",
    definition:
      "The core set of cards in a product, typically featuring the most athletes and serving as the foundation that parallels and inserts build upon. Base set cards are the most commonly pulled cards in a product.",
  },
  {
    term: "Break",
    definition:
      "A group opening of packs or boxes where participants claim teams, players, or spots and receive the cards pulled for their selection. Common across all card sports and entertainment products. Breaks are typically streamed live on platforms such as WhatNot, eBay Live, and YouTube.",
  },
  {
    term: "Break Hit Calculator",
    definition:
      "A tool built into each athlete's card panel that estimates the statistical probability of pulling that athlete's serialized card during a hobby break. Based on official pack odds, serialized print runs, and confirmed box configuration data. See the Break Hit Calculator guide in Resources for full details on how it works.",
  },
  {
    term: "Break Sheet Builder",
    definition:
      "A tool that generates a Whatnot-ready CSV file for any set in the app. Each row represents one athlete slot in a break, pre-filled with the athlete's name and a summary of their cards in the set (autographs, relics, rookie status, and more). Breakers can customize tag labels, add a break description, and select a listing type before downloading. The file can be uploaded directly to Whatnot to list break slots in minutes.",
  },
  {
    term: "Breaker's Delight Box",
    definition:
      "A box format exclusive to certain Topps Chrome releases, designed specifically for live breakers. Contains fewer packs than a standard hobby box but guarantees a higher density of premium hits including multiple autographs per box and exclusive inserts or parallels not available in any other format. In some releases, Breaker's Delight boxes also guarantee one specific premium autograph per case such as a Global Attraction Autograph in 2025-26 Topps Chrome UEFA Club Competitions.",
  },
  {
    term: "Buyback Autograph",
    definition:
      "An original vintage card that has been pulled from packs, authenticated by the manufacturer, signed by the player, and reinserted into new product releases. Buyback autographs are especially sought after because they feature classic card designs signed decades after original production. The Ballon d'Or Buyback Autographs in 2025-26 Topps Chrome UEFA Club Competitions are a notable example.",
  },
  {
    term: "Buyers Giveaway",
    definition:
      "A break slot added to the top of a break sheet reserved for a free giveaway to a buyer, commonly used on Whatnot to reward participants or promote engagement during a live break. The Break Sheet Builder on Checklist2 includes a toggle to automatically add a Buyers Giveaway slot to the generated CSV.",
  },
  {
    term: "Cards",
    definition:
      "The total number of distinct card appearances across the base set, insert sets, autograph sets, and memorabilia sets. One player appearing in 3 different insert sets counts as 3 cards. Parallel versions of the same card are not counted here — see Total Parallels.",
  },
  {
    term: "Case",
    definition:
      "A sealed unit containing multiple boxes of packs. Case configurations vary by product — for example a hobby case may contain 8 or 12 boxes depending on the set. Break buyers often purchase spots in case breaks for better odds at hitting rare cards.",
  },
  {
    term: "First Day Issue (FDI) Box",
    definition:
      "An exclusive early-release hobby box sold directly through Topps.com, typically via a reverse Dutch auction — a pricing model that starts high and drops until the product sells out. FDI boxes ship before the standard hobby release, giving collectors first access to a set's cards. They are distinguished by exclusive low-numbered parallels not found in standard hobby boxes and frequently include additional autograph hits. For example, the 2025-26 Topps Three Basketball FDI box includes an exclusive FDI-only Rookie Patch Autograph on top of the standard autograph guarantees. Conceptually similar to First Off The Line (FOTL) boxes — both offer early access and unique parallels unavailable elsewhere.",
  },
  {
    term: "Giveaway Slot",
    definition:
      "An additional slot added to a break sheet with no associated athlete or card, used for promotional giveaways during a live break. The Break Sheet Builder on Checklist2 allows breakers to add one or more giveaway slots to the end of their break sheet CSV using the Giveaways counter.",
  },
  {
    term: "Hobby Box",
    definition:
      "A premium retail configuration of a card product designed for collectors, typically containing more packs and better odds at hitting rare parallels and autographs compared to retail boxes. Hobby boxes are the standard format used in breaks.",
  },
  {
    term: "Hongbao Box",
    definition:
      "A Topps Chrome box type featuring exclusive foil parallels, typically released in conjunction with Lunar New Year celebrations. Hongbao boxes contain unique parallel variants such as Hongbao Green Foil and Hongbao Red Foil that are not available in any other box format.",
  },
  {
    term: "Insert Sets",
    definition:
      "Named subsets within a product that are separate from the base set, such as autograph collections, memorabilia cards, or themed insert series. Found across all sports and entertainment sets. Examples include Stroke of Midnight Autographs, Constellations, Horizon Signatures, and Arrivals.",
  },
  {
    term: "Lava Refractor",
    definition:
      "A Chrome parallel variant featuring a distinctive lava-texture pattern overlay on the card surface. Available in multiple colors (Aqua, Blue, Green, Purple, Gold, Orange, Black, Red) and typically exclusive to Hobby and Jumbo box formats. Lava Refractors are considered a step up from standard colored Refractors due to their unique texture and box-type exclusivity.",
  },
  {
    term: "Logofractor Box",
    definition:
      "A premium Topps Chrome box type built entirely around the Logofractor and Starball Refractor parallel ecosystem. Cards pulled from Logofractor boxes feature logo-embedded designs across multiple Starball Refractor tiers including Night Vision, Green, Magenta, Gold, Orange, Black, Red, and Rose Gold. These parallels are exclusive to Logofractor boxes and cannot be found in any other format.",
  },
  {
    term: "Memorabilia Card",
    definition:
      "A card that contains an embedded piece of a physical item such as a jersey, patch, glove, ball, or equipment worn or used by the athlete. Also referred to as relic cards. Can appear as standalone memorabilia cards or combined with an autograph (relic autograph).",
  },
  {
    term: "Numbered Parallel",
    definition:
      "A parallel card that has a specific print run stamped on it indicating how many copies were produced (e.g. 45/99 means this is copy number 45 out of 99 total). Also called a serialized card. Numbered parallels are more scarce than unnumbered parallels and their exact population is publicly known. In the Break Hit Calculator, the Numbered Parallel row shows the probability of pulling any numbered card of a specific athlete across all insert sets.",
  },
  {
    term: "One of One (1/1)",
    definition:
      "A card with a print run of exactly 1, making it the only copy in existence. The most scarce card in any set. Often referred to as a \"one of one\" or \"true one of one\" in the hobby community.",
  },
  {
    term: "Pack Odds",
    definition:
      "The official pull rates published by card manufacturers showing how frequently each card type, insert, or parallel appears in hobby packs. Expressed as a ratio (e.g. 1:6 means one card per every 6 packs on average). The Pack Odds page for each set on Checklist2 displays the full odds table grouped by card category alongside the confirmed box and case configuration.",
  },
  {
    term: "Parallel Types",
    definition:
      "The number of distinct named parallel variations that exist within a set, counted once regardless of how many cards or insert sets use them. For example if \"Twilight\" appears as a parallel in the base set, the autograph set, and the insert sets, it still counts as one parallel type. This tells you how many different versions of cards exist in the product.",
  },
  {
    term: "Piece of Club History",
    definition:
      "A multi-autograph booklet card that features six signatures from a combination of legendary and current players representing a single club. Among the most ambitious and valuable cards in any product. Notable examples in 2025-26 Topps Chrome UEFA Club Competitions include booklets for FC Bayern München, FC Barcelona, Arsenal FC, AC Milan, and Liverpool FC spanning iconic players across decades of club history.",
  },
  {
    term: "Print Run",
    definition:
      "The total number of copies produced of a specific card. Serialized cards show this as a number stamped on the card (e.g. /25 means only 25 copies exist worldwide). Cards without a print run are considered unnumbered and their production quantity is not publicly disclosed by the manufacturer.",
  },
  {
    term: "RC (Rookie Card)",
    definition:
      "A player's first officially licensed trading card, typically issued in their debut season. Applies across all sports — basketball, baseball, soccer, MMA, racing, wrestling, and more. Rookie cards are historically among the most sought after cards in the hobby due to their scarcity and long term value potential.",
  },
  {
    term: "Radiating Rookie",
    definition:
      "A featured rookie insert found in Topps Chrome products that highlights the most notable rookies in the set with a distinctive radiating burst design. Radiating Rookies are a subset of the base rookie cards and typically include only the highest-profile first-year players in the release. They carry their own parallel structure and are among the most sought-after cards in Chrome products.",
  },
  {
    term: "RayWave",
    definition:
      "A Chrome parallel variant featuring a ray-wave pattern on the card surface, distinct from standard Refractors and Lava Refractors. Available in select box types depending on the product. Examples include the Gold RayWave and Green/Aqua RayWave parallels found in 2025-26 Topps Chrome UEFA Club Competitions.",
  },
  {
    term: "Sapphire Box",
    definition:
      "A premium Topps Chrome box type featuring an exclusive Sapphire parallel line not available in any other format. Sapphire parallels include Green, Purple, Gold, Orange, Black, and Red Sapphire tiers, with the ultra-rare Padparadscha Sapphire as the rarest pull. Each Sapphire box guarantees at least one autograph.",
  },
  {
    term: "Short Labels / Long Labels",
    definition:
      "A toggle in the Break Sheet Builder that controls how athlete descriptions appear in the generated CSV output. Long Labels (default) uses full descriptive text such as \"Rookie\", \"Autograph\", and \"3 Numbered Parallels\". Short Labels uses abbreviated format such as (RC), (AUTO), and (3 PARALLELS) — ideal for platforms with character limits or breakers who prefer compact slot names.",
  },
  {
    term: "SuperFractor / Padparadscha Sapphire",
    definition:
      "The rarest parallel in Topps products, existing as a true 1/1. Different product lines use different names for this tier — SuperFractor in Chrome products, Padparadscha Sapphire in Sapphire editions. The equivalent in Panini products is typically the Black Prizm /1.",
  },
  {
    term: "Tier",
    definition:
      "The card quality level of a set. Checklist2 uses the following tiers: Standard (base cardstock), Chrome (glossy refractor technology by Topps), Prizm (glossy technology by Panini), Sapphire (premium elevated design), and Premium (thick high-end cardstock such as Topps Midnight and Topps Royalty).",
  },
  {
    term: "Total Parallels",
    definition:
      "The total count of unique parallel cards across the entire set — every card appearance in every subset (base set, insert sets, autograph sets, memorabilia sets) multiplied by the number of parallel types attached to it. For example a set with 100 base cards and 8 parallel types has at minimum 800 base parallels alone, before counting parallels across insert and autograph sets. This number is typically in the hundreds or thousands for most sets and represents the full scope of parallel production in the product.",
  },
  {
    term: "Total Print Run",
    definition:
      "The sum of all serialized (numbered) print runs across every parallel of every card in the set. This represents the total number of physically numbered copies that exist across the entire product. Unnumbered parallels are not included in this figure since their production quantities are not publicly disclosed by manufacturers.",
  },
];

export default function GlossaryPage() {
  return (
    <PageShell
      breadcrumb={{ label: "Resources", href: "/resources" }}
      title="Glossary"
      description="Key terms and concepts for sports card collectors and breakers"
    >
        {/* Terms */}
        <div className="space-y-px">
          {terms.map((item, i) => (
            <div
              key={item.term}
              className={`px-5 py-4 ${
                i % 2 === 0 ? "bg-zinc-900" : "bg-zinc-900/40"
              } ${i === 0 ? "rounded-t-xl" : ""} ${
                i === terms.length - 1 ? "rounded-b-xl" : ""
              } border-x border-t border-zinc-800 ${
                i === terms.length - 1 ? "border-b" : ""
              }`}
            >
              <dt className="text-sm font-semibold text-white mb-1">{item.term}</dt>
              <dd className="text-sm text-zinc-400 leading-relaxed">{item.definition}</dd>
            </div>
          ))}
        </div>
    </PageShell>
  );
}
