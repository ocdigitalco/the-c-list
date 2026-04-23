// IMPORTANT: Add a new update entry here every time a checklist, box config,
// odds, or feature is added to the app. Keep sorted newest first.

export interface Update {
  id: string;
  title: string;
  date: string; // ISO 8601
  summary: string;
  description: string; // markdown
  tags: string[]; // "checklist" | "box-config" | "odds" | "feature" | "announcement"
  setId?: number;
}

export const updates: Update[] = [
  // ─── April 20, 2026 ──────────────────────────────────────────────────────
  // ─── April 21, 2026 ──────────────────────────────────────────────────────
  // ─── April 22, 2026 ──────────────────────────────────────────────────────
  {
    id: "138-bowman-basketball-rename",
    title: "2025-26 Bowman Basketball — Renamed",
    date: "2026-04-22T14:00:00Z",
    summary: "Removed 'Topps' from set name and slug. URL updated from /sets/2025-26-topps-bowman-basketball to /sets/2025-26-bowman-basketball. Empty duplicate stub deleted.",
    description: `## 2025-26 Bowman Basketball — Renamed

Removed "Topps" from the set name and slug to match official product branding. URL updated from \`/sets/2025-26-topps-bowman-basketball\` to \`/sets/2025-26-bowman-basketball\`. The old numeric URL still redirects. Empty duplicate stub set deleted. SP/SSP config and catalog entry updated to match.`,
    tags: ["feature"],
    setId: 34,
  },
  {
    id: "137-bowman-draft-sapphire",
    title: "2025 Bowman Draft Sapphire Baseball Edition — Verified",
    date: "2026-04-22T12:00:00Z",
    summary: "Verified full checklist: 200 base prospects, 30 Chrome Prospect Autographs, 15 Sapphire Selections Autographs, and 18 Sapphire Selections inserts. 19 parallel tiers, pack odds, and box config confirmed.",
    description: `## 2025 Bowman Draft Sapphire Baseball Edition

Full checklist verified with 263 total cards across 4 insert sets: Base (200 prospects), Chrome Prospect Autographs (30), Sapphire Selections Autographs (15), and Sapphire Selections (18 inserts). 19 parallel tiers including Padparadscha /1 and Superfractor /1. Pack odds and Hobby box config included.`,
    tags: ["checklist", "odds"],
    setId: 41,
  },
  {
    id: "136-donruss-fifa-part3",
    title: "2025-26 Donruss Road to FIFA World Cup 26 — Part 3",
    date: "2026-04-21T20:00:00Z",
    summary: "Seeded all autograph sets: Beautiful Game Autographs (41 cards), Beautiful Game Dual Autographs (9 dual cards), and Signature Series (44 cards). 393 total athletes, 1,001 total appearances.",
    description: `## 2025-26 Donruss Road to FIFA World Cup 26 — Part 3

Seeded all 3 autograph sets: Beautiful Game Autographs (41 players including legends Ronaldo, Luis Figo, Manuel Neuer, Angel Di Maria), Beautiful Game Dual Autographs (9 dual cards with co-player relationships — Harry Kane/Kyle Walker, Buffon/Donnarumma, etc.), and Signature Series (44 players including Lionel Messi, Kylian Mbappe, Harry Kane). Set now has 393 athletes across 1,001 total appearances. Per-player print run data documented in seed script for parallel reference.`,
    tags: ["checklist"],
    setId: 836,
  },
  {
    id: "135-donruss-fifa-part2",
    title: "2025-26 Donruss Road to FIFA World Cup 26 — Part 2",
    date: "2026-04-21T16:00:00Z",
    summary: "Seeded all 12 insert sets and 2 memorabilia sets — 398 total cards added. 348 athletes, 898 total appearances across 18 populated insert sets.",
    description: `## 2025-26 Donruss Road to FIFA World Cup 26 — Part 2

Seeded all 12 insert sets (Animation, Craftsmen, Dominators, Elite Series, Kaboom, Kaboom Oversize, Magicians, Net Marvels, Night Moves, Pitch Kings, Rookie Kings, Zero Gravity) and 2 memorabilia sets (Kit Kings, Kit Series). 398 new cards added bringing the total to 898 appearances across 348 athletes. Includes legends (Pele, Maradona, Beckenbauer, Ronaldo, Neymar) alongside current stars. Autograph sets coming in Part 3.`,
    tags: ["checklist"],
    setId: 836,
  },
  {
    id: "134-donruss-fifa-part1",
    title: "2025-26 Donruss Road to FIFA World Cup 26 — Part 1",
    date: "2026-04-21T12:00:00Z",
    summary: "Set created with box config, all 21 insert sets, 199 parallels, and 500 base cards seeded (250 Donruss + 250 Optic including Rated Rookies). Releases April 22, 2026.",
    description: `## 2025-26 Donruss Road to FIFA World Cup 26 — Part 1

Set created with 4 box formats (Hobby, Hobby International, Blaster, Fat Pack), 21 insert sets, and 199 parallel tiers. 500 base cards seeded: Base (200 veterans), Base - Rated Rookies (50 rookies), Base Optic (200), Base Optic - Rated Rookies (50). Covers 250 athletes across 25+ national teams. Insert and autograph cards coming in Part 2.`,
    tags: ["checklist"],
    setId: 836,
  },
  {
    id: "133-fix-crystallized-keys",
    title: "Fix Crystallized Key Mismatch — Bowman Basketball Odds",
    date: "2026-04-20T23:59:30Z",
    summary: "Corrected spelling of Crystallized NBA/NIL odds keys from single-l to double-l to match DB insert set names.",
    description: `## Fix Crystallized Key Mismatch — Bowman Basketball Odds

Corrected spelling of Crystallized NBA/NIL odds keys from single-l ("Crystalized") to double-l ("Crystallized") across all box types (Hobby, Jumbo, Breaker's Delight, Value) to match the DB insert set names. 24 odds keys renamed total.`,
    tags: ["odds"],
    setId: 34,
  },
  {
    id: "132-detect-dynamic-thresholds",
    title: "SP/SSP Detection Engine — Dynamic Percentile Thresholds",
    date: "2026-04-20T23:59:00Z",
    summary: "Updated detect-sp-ssp.ts to use per-set dynamic thresholds based on each set's own base insert odds distribution.",
    description: `## SP/SSP Detection Engine — Dynamic Percentile Thresholds

Updated \`detect-sp-ssp.ts\` to use per-set dynamic thresholds based on each set's own base insert odds distribution. Engine now focuses exclusively on base insert pull rates (excluding parallels, SuperFractors, and autograph sets). Uses 85th percentile for SP threshold and 95th percentile for SSP threshold, with a minimum sample size of 8 inserts before falling back to fixed ratio thresholds. Existing approved configs in \`spSspConfig.ts\` are unchanged.`,
    tags: ["feature"],
  },
  {
    id: "131-bowman-basketball-ssp",
    title: "2025-26 Topps Bowman Basketball — SSP Classifications Added",
    date: "2026-04-20T23:45:00Z",
    summary: "Added SSP classifications for Crystallized, Anime, and Bowman Spotlights insert sets (NBA and NIL variants). Updated detect-sp-ssp.ts anchor override for Bowman sets.",
    description: `## 2025-26 Topps Bowman Basketball — SSP Classifications Added

Added SSP classifications for Crystallized, Anime, and Bowman Spotlights insert sets (NBA and NIL variants). No SP row — Bowman inserts are generally common pulls with rarity expressed through parallels. Updated \`detect-sp-ssp.ts\` anchor override to use Base Chrome Refractor as anchor for all Bowman sets.`,
    tags: ["feature"],
    setId: 34,
  },
  {
    id: "130-bowman-basketball-odds",
    title: "2025-26 Topps Bowman Basketball — Pack Odds Added",
    date: "2026-04-20T23:30:00Z",
    summary: "Added full pack odds for 2025-26 Topps Bowman Basketball across Hobby, Jumbo, Breaker's Delight, Value, Mega, and Bulk box formats. 1,050 total odds entries.",
    description: `## 2025-26 Topps Bowman Basketball — Pack Odds Added

Added 1,050 pack odds entries across 6 box formats: Hobby (440), Jumbo (271), Breaker's Delight (67), Value (169), Mega (22), and Bulk (81). Covers base Chrome and paper parallels, Chrome Prospect parallels, all insert sets (Talent Tracker, Gen Next, Very Important Prospects, Bowman Verified, ROY Favorites, Hobby Stars, Young Kings, Rockstar Rookies, Greatness Loading), special inserts (Anime, Bowman GPK, Crystalized, Retrofractor, Etched-In Glass, Bowman Spotlights), and all autograph sets.`,
    tags: ["odds"],
    setId: 34,
  },
  {
    id: "129-midnight-ufc-2025-spssp",
    title: "2025 Topps Midnight UFC — SP/SSP Classifications Added",
    date: "2026-04-20T23:00:00Z",
    summary: "Added SP/SSP config for 2025 Topps Midnight UFC. Updated detection engine with per-set anchor overrides and limited parallel structure signal.",
    description: `## 2025 Topps Midnight UFC — SP/SSP Classifications Added

Added SP/SSP config: Greetings From and Night Vision classified as Short Print, Twilight and Dream Chasers classified as Super Short Print. Updated \`detect-sp-ssp.ts\` with per-set anchor key overrides (Midnight → Base Zodiac, Hoops → Base) and limited parallel structure detection signal that upgrades inserts with only /5 or 1/1 parallels to SSP.`,
    tags: ["feature"],
    setId: 8,
  },
  {
    id: "128-midnight-ufc-2025-odds",
    title: "2025 Topps Midnight UFC — Pack Odds Added",
    date: "2026-04-20T22:00:00Z",
    summary: "Added full hobby pack odds for 2025 Topps Midnight UFC including base parallels and all insert/autograph set odds.",
    description: `## 2025 Topps Midnight UFC — Pack Odds Added

Added 91 hobby pack odds entries covering base parallels (Zodiac, Morning, Twilight, Dusk, Moon Beam, Moonrise, Midnight, Daybreak, Black Light) and all insert sets (Nightfall, Lunar Tide, Constellations, The One and Only, Insomnia, Dream Chasers, Greetings From, Twilight, Night Vision) plus autograph sets (Rookie Relic Autographs, Relic Autographs, Stroke of Midnight Autographs, Glimmer Graphs, Horizon Signatures). Also added parallel tiers to all insert sets.`,
    tags: ["odds"],
    setId: 8,
  },
  {
    id: "127-midnight-ufc-2026",
    title: "2026 Topps Midnight UFC — Added",
    date: "2026-04-20T20:00:00Z",
    summary: "Full checklist seeded: 100 base cards, 9 insert sets, and 5 autograph sets including Rookie Relic Autographs, Fight Glove Relic Autographs, and Horizon Signatures. Releases May 22, 2026.",
    description: `## 2026 Topps Midnight UFC

Full checklist seeded with 178 athletes across 15 insert sets. Includes Base Set (100 cards), 9 insert sets (Night Watch, Zero Hour, Celestial Combos, Lunar Apex, Insomnia, Last One Standing, Neon Apex, Twilight, Cemented), and 5 autograph sets (Rookie Relic Autographs, Relic Autographs, Fight Glove Relic Autographs, Autograph Variation, Horizon Signatures). Releases May 22, 2026.`,
    tags: ["checklist"],
    setId: 835,
  },
  {
    id: "126-sp-ssp-global-rollout",
    title: "SP/SSP Classifications — Global Rollout",
    date: "2026-04-20T18:00:00Z",
    summary: "Added Short Print and Super Short Print classifications to the Break Hit Calculator for 9 sets across Football, Basketball, Baseball, Soccer, UFC, F1, and Olympics.",
    description: `## SP/SSP Classifications — Global Rollout

Added Short Print and Super Short Print classifications to the Break Hit Calculator for 9 sets: Chrome Football, Chrome F1, Chrome UFC, Pristine Baseball, Cosmic Chrome Basketball, Hoops Basketball, Midnight Basketball, UEFA Club Competitions, and U.S. Olympic Team Hopefuls. Classifications were generated using the automated detection engine and reviewed before publishing.`,
    tags: ["feature"],
  },
  {
    id: "125-sp-ssp-detection-engine",
    title: "SP/SSP Auto-Detection Engine — Phase 2",
    date: "2026-04-20T16:00:00Z",
    summary: "Added scripts/detect-sp-ssp.ts, an automated classification engine that analyzes insert sets across all sets using a ratio-based approach.",
    description: `## SP/SSP Auto-Detection Engine — Phase 2

Added \`scripts/detect-sp-ssp.ts\`, an automated classification engine that analyzes insert sets across all sets using a ratio-based approach. The script compares insert odds against each set's anchor parallel to suggest SP and Super Short Print classifications. Includes confidence scoring (high/medium/low), fuzzy name matching for odds key resolution, fallback anchor hierarchy for non-standard sets, and exclusion list for entertainment sets. Detected SP/SSP candidates across 10 sets spanning Football, Basketball, Baseball, Soccer, UFC, F1, and Olympics. Run after seeding any new set to generate suggested \`spSspConfig.ts\` entries for review.`,
    tags: ["feature"],
  },
  {
    id: "124-sp-ssp-config-system",
    title: "SP/SSP Classification System — Phase 1",
    date: "2026-04-20T12:00:00Z",
    summary: "Introduced a central SP/SSP config file that drives Short Print and Super Short Print rows in the Break Hit Calculator.",
    description: `## SP/SSP Classification System — Phase 1

Introduced a central SP/SSP config file (\`src/lib/spSspConfig.ts\`) that drives Short Print and Super Short Print rows in the Break Hit Calculator. Classifications are defined per set and reviewed before publishing. Entertainment and non-sport sets are automatically excluded. Currently configured for 2025 Topps Chrome Football with 6 SP insert sets (image variations, team camo, etch variations) and 8 SSP insert sets (Helix, Game Genies, Kaiju, Let's Go, Ultra Violet, Lightning Leaders, Fanatical, Shadow Etch).`,
    tags: ["feature"],
  },
  // ─── April 17, 2026 ──────────────────────────────────────────────────────
  {
    id: "123-chrome-football-superfractor-odds",
    title: "2025 Topps Chrome Football — Superfractor Odds Added",
    date: "2026-04-17T14:00:00Z",
    summary: "Added insert-specific Superfractor odds for Kaiju, Game Genies, Tecmo, Helix, Let's Go, Shadow Etch, and all autograph sets to the pack odds display.",
    description: `## 2025 Topps Chrome Football — Superfractor Odds Added

Added 30 insert-specific Superfractor (1/1) odds entries to the Hobby pack odds for 2025 Topps Chrome Football. Covers all SP/SSP inserts (Kaiju, Game Genies, Tecmo, Helix, Let's Go, Ultraviolet, Lightning Leaders, Shadow Etch), base/rookie variations, all autograph sets, and standard inserts. Superfractors now appear in their own visually distinct section in the pack odds table.`,
    tags: ["odds"],
    setId: 44,
  },
  {
    id: "122-hoops-basketball-image",
    title: "2025-26 Topps Hoops Basketball — Image Added",
    date: "2026-04-17T12:00:00Z",
    summary: "Added set image for 2025-26 Topps Hoops Basketball.",
    description: `## 2025-26 Topps Hoops Basketball — Image Added

Added set image for 2025-26 Topps Hoops Basketball.`,
    tags: ["feature"],
    setId: 834,
  },
  // ─── April 16, 2026 ──────────────────────────────────────────────────────
  {
    id: "121-hoops-basketball-2025-26",
    title: "2025-26 Topps Hoops Basketball — Full Checklist and Odds Added",
    date: "2026-04-16T12:00:00Z",
    summary: "Added 2025-26 Topps Hoops Basketball with complete checklist across all sub-categories including base set (300 cards), 8 autograph sets, and 14 insert sets. Full pack odds loaded for Hobby, Jumbo, Value, Hanger, and Fanatics box formats.",
    description: `## 2025-26 Topps Hoops Basketball

Complete checklist added with 338 athletes across 27 insert sets and 172 parallels. Includes Base Set (260 cards), Base Highlights (10), Base All-Stars (30), plus 8 autograph sets (Hoops Rookie Signatures, Hoops Signs, Hoops Rookie Duals, Hoops Rookie Triples, Hoops Rookie/Veteran Duals, Hoops 1989 Signatures, Hoops Rookie First Signs, Hoops Hyper Signatures) and 14 insert sets (Bounce House, Next Episode, Dunkumentory, Pay Attention, Hoopers, Finals Pursuit, Oasis, Joy, Checkmate, Hoopnotic, Hardwired, The Buzz, Net to Net, Jam-Packed, Block by Block, Boombastic). Full pack odds for Hobby, Jumbo, Value, Hanger, and Fanatics box formats.`,
    tags: ["checklist", "odds", "box-config"],
    setId: 834,
  },
  // ─── April 13, 2026 ──────────────────────────────────────────────────────
  // ─── April 15, 2026 ──────────────────────────────────────────────────────
  {
    id: "120-mobile-athlete-ui-refinements",
    title: "Athlete Page — Mobile UI Refinements",
    date: "2026-04-15T18:00:00Z",
    summary: "Relocated Leaderboard button to breadcrumb row on mobile, converted section pills to a proper sliding tab bar with active underline indicator, and updated Break Hit Calculator box format tabs with active purple fill state.",
    description: `## Athlete Page — Mobile UI Refinements

Relocated the Leaderboard button to sit inline on the breadcrumb row (left: back link, right: Leaderboard button) on mobile. Replaced the old pill-style section tabs with a proper full-width sliding tab bar — active tab shows bold text with a sliding purple underline indicator (CSS transform transition). Tapping a tab now switches visible content inline instead of anchor-scrolling. Break Hit Calculator box format tabs (Hobby/Jumbo/Value/etc.) now use a purple filled background with white text for the active state. Desktop layout unchanged.`,
    tags: ["feature"],
  },
  {
    id: "119-recompute-unique-cards",
    title: "Total Cards Recomputed",
    date: "2026-04-15T16:00:00Z",
    summary: "Recomputed Total Cards count for all 10,727 athletes to correctly include parallels. Added reusable recompute script.",
    description: `## Total Cards Recomputed

All athlete card counts have been recomputed to correctly include base cards plus all parallel tiers. The new \`scripts/recompute-unique-cards.ts\` script can be run after adding parallels to any set to ensure counts stay accurate. Cooper Flagg in Cosmic Chrome now shows 99 total cards (was 14), Cam Ward in Chrome Football shows 214.`,
    tags: ["feature"],
  },
  {
    id: "118-nfl-player-thumbnails",
    title: "NFL Player Thumbnails Added",
    date: "2026-04-15T14:00:00Z",
    summary: "NFL player headshots now display using the Sleeper CDN. 461 players matched by name across all NFL sets.",
    description: `## NFL Player Thumbnails

461 NFL player headshots now display on athlete pages and leaderboard sidebars using the Sleeper CDN. Images are matched by player name from the Sleeper API database of 10,000+ NFL players. Combined with existing NBA, UFC, MLB, and Disney character images, the majority of athletes across the site now have visual headshots.`,
    tags: ["feature"],
  },
  {
    id: "117-chrome-football-parallels-odds",
    title: "2025 Topps Chrome Football — Parallels and Odds Added",
    date: "2026-04-15T12:00:00Z",
    summary: "Added full parallel structure across all insert sets and complete pack odds across 14 box formats including Hobby, FDI, Jumbo, Breaker's Delight, Sapphire, Value, Mega, Hanger, and Fanatics for 2025 Topps Chrome Football.",
    description: `## 2025 Topps Chrome Football

355 parallels added across all insert sets and 421 pack odds entries across 14 box formats. Covers base parallels (Refractor, Wave, Lava, Geometric, Football Leather, X-Fractor, RayWave), all autograph sets (Chrome Autos, Rookies, Legends, Hall of Chrome, 1990 Topps, Chromographs, Future Stars, Dual, Rookie Patch), insert sets (1975 Topps, Power Players, Fortune 15, Legends of the Gridiron, etc.), and format exclusives (Sapphire Selections, Radiating Rookies, Helix, Game Genies, Kaiju, Let's Go, Tecmo, Urban Legends, Fanatical).`,
    tags: ["checklist", "odds"],
    setId: 44,
  },
  // ─── April 14, 2026 ──────────────────────────────────────────────────────
  {
    id: "116-disneyland-70th-image",
    title: "2025 Topps Disneyland 70th Anniversary — Image Added",
    date: "2026-04-14T12:00:00Z",
    summary: "Added set image for 2025 Topps Disneyland 70th Anniversary.",
    description: `Added sample set image for 2025 Topps Disneyland 70th Anniversary.`,
    tags: ["checklist"],
    setId: 50,
  },
  {
    id: "115-disney-neon-2026",
    title: "2026 Topps Disney Neon — Added",
    date: "2026-04-13T23:50:00Z",
    summary: "Full checklist seeded including 200 base cards, 10 autograph sets, and 15 insert sets with parallels, pack odds, box configuration, and set image. Releases April 10, 2026.",
    description: `## 2026 Topps Disney Neon

Complete checklist now available with 753 card appearances across 23 insert sets and 339 characters from 50+ Disney, Pixar, and Muppets properties. Includes Topps Neon Autographs (30 cards), Chrome Neon Etch Autographs (60 cards), Phineas and Ferb Auto Variations, A Goofy Movie 30th Anniversary Autos, Mickey Shorts Dual Autos, Triple Booklet Superfractors (all /1), Chrome Neon Etch (100 cards), Family First (35 dual cards), and Neon Villains. 273 pack odds entries across Hobby, Value, and Mega formats.`,
    tags: ["checklist", "box-config", "odds"],
    setId: 59,
  },
  {
    id: "114-batch-config-updates",
    title: "Box Configs and Release Dates — Batch Update",
    date: "2026-04-13T23:45:00Z",
    summary: "Added box configurations and/or release dates for 2025 Topps Royalty UFC, 2025 Topps Midnight UFC, 2025-26 Topps Midnight Basketball, 2026 Topps Heritage Baseball, 2026 Topps Series 1 Baseball, 2026 Topps Chrome U.S. Winter Olympic and Paralympic Hopefuls, and 2025 Bowman's Best Baseball.",
    description: `## Box Configs and Release Dates — Batch Update

- **2025 Topps Royalty UFC** — Feb 6, 2026. Hobby: 10 cards/pack, 1 pack/box, 5 autos, 3 memorabilia
- **2025 Topps Midnight UFC** — Aug 8, 2025. Hobby: 7 cards/pack, 1 pack/box, 3 autos
- **2025-26 Topps Midnight Basketball** — Jan 29, 2026. Hobby: 7 cards/pack, 1 pack/box, 3 autos
- **2026 Topps Heritage Baseball** — Mar 18, 2026
- **2026 Topps Series 1 Baseball** — Feb 11, 2026
- **2026 Topps Chrome U.S. Winter Olympic and Paralympic Hopefuls** — Jan 15, 2026. Hobby + Value Blaster
- **2025 Bowman's Best Baseball** — Mar 11, 2026`,
    tags: ["box-config"],
  },
  {
    id: "113-chrome-ufc-config",
    title: "2025 Topps Chrome UFC — Box Config Added",
    date: "2026-04-13T23:30:00Z",
    summary: "Added box configuration and release date (June 27, 2025) for 2025 Topps Chrome UFC across Hobby, Mega Box, and Value Blaster formats.",
    description: `## 2025 Topps Chrome UFC

Box configuration and release date now available. Releases June 27, 2025 across Hobby (12 packs, 2 autos, 4 numbered parallels, 20 total parallels), Mega (6 packs), and Value Blaster (6 packs).`,
    tags: ["box-config"],
    setId: 28,
  },
  {
    id: "112-chrome-premier-league-config",
    title: "2026 Topps Chrome Premier League — Box Config Added",
    date: "2026-04-13T23:00:00Z",
    summary: "Added box configuration and release date (February 5, 2026) for 2026 Topps Chrome Premier League across Hobby, Value Blaster, and Breaker's Delight formats.",
    description: `## 2026 Topps Chrome Premier League

Box configuration and release date now available. Releases February 5, 2026 across Hobby (20 packs, 1 auto, 10 inserts, 4 Prism Refractors, 6 base Refractors), Value Blaster (7 packs, 4 RayWave parallels), and Breaker's Delight (1 pack, 2 autos, 3 Geometric parallels).`,
    tags: ["box-config"],
    setId: 13,
  },
  {
    id: "111-ucc-2025-config-odds",
    title: "2025-26 Topps UEFA Club Competitions — Box Config and Odds Added",
    date: "2026-04-13T22:00:00Z",
    summary: "Added box configuration, release date (January 15, 2026), and full pack odds across Hobby, Value, Hanger, London Store, Carnaval, Japan Hobby, Japan Retail, and Spring Tin formats.",
    description: `## 2025-26 Topps UEFA Club Competitions

Box configuration and 621 pack odds entries now available across 8 formats: Hobby (24 packs, 1 auto/memorabilia), Value Blaster (7 packs), Hanger, London Store (Regency Chrome exclusives), Carnaval (Samba parallels), Japan Hobby (Sunflower parallels), Japan Retail (Diamond Plaid parallels), and Spring Tin (seasonal parallels). Releases January 15, 2026.`,
    tags: ["box-config", "odds"],
    setId: 36,
  },
  {
    id: "110-chrome-mls-mania-fix",
    title: "2025 Topps Chrome MLS — Mania Box Config Fixed",
    date: "2026-04-13T21:00:00Z",
    summary: "Fixed Mania box configuration to correctly display 4 autographs per box.",
    description: `## 2025 Topps Chrome MLS — Mania Fix

Updated the Mania box configuration to use the standard \`autos_per_box\` field so the Break Hit Calculator and box config display correctly show 4 autographs per box.`,
    tags: ["box-config"],
    setId: 6,
  },
  {
    id: "109-checklists-search",
    title: "Checklists Page Search",
    date: "2026-04-13T20:00:00Z",
    summary: "Added live search bar to the checklists page. Filter by name, sport, league, or tier. Works in combination with the sport filter tiles.",
    description: `## Checklists Page Search

A live search bar has been added to the /checklists page. Type to filter sets instantly by name, sport, league, or tier. The search works in combination with the sport filter tiles, so you can narrow results like "Basketball Chrome" or "UEFA Sapphire" in real time.`,
    tags: ["feature"],
  },
  {
    id: "108-seo-slug-urls",
    title: "SEO Slug URLs",
    date: "2026-04-13T19:00:00Z",
    summary: "All set and athlete pages now use descriptive slug-based URLs. Numeric ID URLs redirect to the canonical slug.",
    description: `## SEO Slug URLs

All set and athlete pages now use descriptive, SEO-friendly URLs. For example, /sets/2025-26-topps-finest-basketball instead of /sets/25. Old numeric ID URLs automatically redirect to the canonical slug URL. Internal links across the site have been updated to use slugs directly.`,
    tags: ["feature"],
  },
  {
    id: "107-chrome-mls-config",
    title: "2025 Topps Chrome MLS — Box Config Added",
    date: "2026-04-13T18:00:00Z",
    summary: "Added box configuration and release date (February 19, 2026) for 2025 Topps Chrome MLS across Hobby, Blaster, and Mania formats.",
    description: `## 2025 Topps Chrome MLS

Box configuration and release date now available. Releases February 19, 2026 across Hobby (21 packs, 2 autos), Blaster (7 packs, Mini Diamond and RayWave parallels), and Mania (1 pack, 4 encased autos, 6 Mania parallels).`,
    tags: ["box-config"],
    setId: 6,
  },
  {
    id: "106-midnight-ufc-config",
    title: "2024 Topps Midnight UFC — Box Config Added",
    date: "2026-04-13T17:00:00Z",
    summary: "Added box configuration and release date (May 15, 2024) for 2024 Topps Midnight UFC.",
    description: `## 2024 Topps Midnight UFC

Box configuration and release date now available. Hobby box contains 7 cards per pack, 1 pack per box, 12 boxes per case with 3 autographs, 3 inserts or parallels, and 1 base card per box.`,
    tags: ["box-config"],
    setId: 9,
  },
  {
    id: "105-finest-euro-2024",
    title: "2023 Topps Finest Road to UEFA EURO 2024 — Added",
    date: "2026-04-13T16:00:00Z",
    summary: "Full checklist seeded including 100 base cards, 8 autograph sets, and 7 insert sets with parallels, odds, and box configuration.",
    description: `## 2023 Topps Finest Road to UEFA EURO 2024

Complete checklist now available with 240 card appearances across 14 insert sets, 125 players, box configuration, and 76 pack odds entries. Includes Base Autographs, Euro Masters Autographs, Finest Dual Autographs, Prized Footballers Autographs, and Prized Footballers Fusion Variations.`,
    tags: ["checklist", "box-config", "odds"],
    setId: 297,
  },
  {
    id: "104-pristine-euro-2024",
    title: "2023 Topps Pristine Road to Euro 2024 — Added",
    date: "2026-04-13T15:00:00Z",
    summary: "Full checklist seeded including 200 base cards, 9 autograph sets, and 8 insert sets with parallels, odds, and box configuration.",
    description: `## 2023 Topps Pristine Road to Euro 2024

Complete checklist now available with 411 card appearances across 15 insert sets, 235 players, box configuration, and pack odds. Includes Pristine Autographs (64 cards), Pristine Pair Dual Autographs, Pristine Borders Autographs, and Pristine Prodigies Autographs.`,
    tags: ["checklist", "box-config", "odds"],
    setId: 833,
  },
  {
    id: "103-bowman-basketball-parallels",
    title: "2025-26 Topps Bowman Basketball — Parallels Added",
    date: "2026-04-13T14:00:00Z",
    summary: "Added full parallel structure across all insert sets including Base, Chrome, Prospects, Chrome Prospects, autograph sets, and all insert sets.",
    description: `## 2025-26 Topps Bowman Basketball — Parallels

382 parallels added across 31 insert sets covering Base Set, Base Chrome Variation, Base Prospects, Chrome Prospects, Chrome Prospect Autographs, Chrome Autographs, Retrofractor Autographs, and all insert sets including Talent Tracker, Gen Next, Bowman Spotlights, Crystallized, Anime, and GPK.`,
    tags: ["checklist"],
    setId: 34,
  },
  {
    id: "102-bowman-basketball-config",
    title: "2025-26 Topps Bowman Basketball — Box Config Added",
    date: "2026-04-13T13:00:00Z",
    summary: "Added box configuration and release date (April 22, 2026) across Hobby, Jumbo, Mega, Value, and Breaker's Delight formats.",
    description: `## 2025-26 Topps Bowman Basketball — Box Config

Box configuration and release date now available. Releases April 22, 2026 across five formats: Hobby (20 packs, 2 autos), Jumbo (12 packs, 4 autos), Mega (6 packs, 11 Mojo parallels), Value (6 packs, 4 inserts), and Breaker's Delight (1 pack, 3 autos, Geometric exclusives).`,
    tags: ["box-config"],
    setId: 34,
  },
  {
    id: "101-set-catalogue-expanded",
    title: "Set Catalogue Expanded",
    date: "2026-04-13T12:00:00Z",
    summary: "Added 780+ set reference entries spanning 2018 through 2026 across Baseball, Basketball, Football, Soccer, Wrestling, MMA, Racing, and Entertainment.",
    description: `## Set Catalogue Expanded

Added 780+ set reference entries spanning 2018 through 2026 across all major sports and entertainment categories. Sets without full checklists appear as reference entries on the sets page, giving collectors a comprehensive view of the Topps product landscape.

- **Baseball**: Series 1/2, Chrome, Bowman, Heritage, Finest, Dynasty, Transcendent, and more
- **Basketball**: Chrome, Bowman, Finest, Midnight, Cosmic Chrome
- **Football**: Chrome, Bowman University Chrome, Inception, Finest
- **Soccer**: UEFA Chrome, Bundesliga, MLS, Premier League, Merlin, Museum Collection
- **Wrestling**: WWE Chrome, Heritage, Finest, Transcendent
- **MMA**: UFC Chrome, Midnight, Knockout, Museum
- **Racing**: Formula 1 Chrome, Dynasty, Finest
- **Entertainment**: Star Wars, Disney, Marvel, Garbage Pail Kids across Chrome, Sapphire, and Standard tiers`,
    tags: ["checklist"],
  },
  // ─── April 12, 2026 ──────────────────────────────────────────────────────
  {
    id: "100-bowman-basketball-2025-config",
    title: "2025-26 Topps Bowman Basketball",
    date: "2026-04-12T12:00:00Z",
    summary: "Box configuration, release date, and 382 parallels added for 2025-26 Topps Bowman Basketball. Releases April 22, 2026 across Hobby, Jumbo, Mega, Value, and Breaker's Delight formats.",
    description: `## 2025-26 Topps Bowman Basketball

Box configuration and release date now available. Releases April 22, 2026.

- **Hobby**: 8 cards/pack, 20 packs/box, 12 boxes/case. 1 NBA auto + 1 NCAA auto, 12 inserts, 1 Mini-Diamond Chrome Refractor, 6 additional base parallels per box
- **Jumbo**: 24 cards/pack, 12 packs/box, 8 boxes/case. 2 NBA autos + 2 NCAA autos, 18 inserts, 12 base parallels per box
- **Mega**: 7 cards/pack, 6 packs/box, 20 boxes/case. 11 Mojo parallels, 1 insert, 1 Mega Rookies/Prospects insert per box
- **Value**: 10 cards/pack, 6 packs/box, 40 boxes/case. 4 inserts per box
- **Breaker's Delight**: 10 cards/pack, 1 pack/box, 6 boxes/case. 2 NBA autos + 1 NCAA auto, 3 Geometric Chrome cards per box
- **382 parallels** added across 31 insert sets including Base, Chrome, Prospects, Chrome Prospects, and all autograph and insert sets`,
    tags: ["checklist", "box-config"],
    setId: 34,
  },
  // ─── April 11, 2026 ──────────────────────────────────────────────────────
  {
    id: "099-box-break-simulator",
    title: "Box Break Simulator",
    date: "2026-04-11T16:00:00Z",
    summary: "Run 10,000 simulated breaks for any set. See realistic outcome distributions, top athletes by auto frequency, and a randomly generated pull list.",
    description: `## Box Break Simulator

A new Monte Carlo simulation tool is now available at [/resources/break-simulator](/resources/break-simulator). Select any set with pack odds and box configuration, choose a box type and count, and run 10,000 simulated breaks.

- **Summary cards** showing typical, best (top 10%), and worst (bottom 10%) break outcomes
- **Distribution charts** for autographs and numbered parallels across all simulated breaks
- **Top auto athletes** ranked by frequency across 10,000 trials
- **One simulated break** showing a realistic pull list with re-simulate capability
- Linked from every athlete page's Break Hit Calculator via "Run a simulation"`,
    tags: ["feature"],
  },
  {
    id: "098-chrome-f1-2025",
    title: "New Set: 2025 Topps Chrome Formula 1",
    date: "2026-04-11T14:00:00Z",
    summary: "Box configuration and pack odds added for 2025 Topps Chrome Formula 1 with 314 odds entries across 5 box types: Hobby, Sapphire, Value, Logofractor, and Diamond Anniversary.",
    description: `## 2025 Topps Chrome Formula 1

Box configuration and full pack odds now available across five formats.

- **Hobby Box**: 4 cards per pack, 8 packs per box, 10 boxes per case, 4 parallels or short prints per box
- **Pack Odds** across Hobby (121 entries), Sapphire (45 entries), Value (91 entries), Logofractor (42 entries), and Diamond Anniversary (9 entries)
- **Base parallels**: Refractor, Checker Flag, B&W Lazer, Teal through Superfractor with format-exclusive variants (RayWave for Value, Logofractor parallels, Sapphire parallels, Mini Diamond for Diamond Anniversary)
- **Insert Sets**: 1975 Speed Wheels, Ace of Trades, F1 Chrome Diamond Drives, Floor It, Helmet Collection, Speed Demons, Futuro, Helix, Neon Nations, The Chain, The Grid, Ultrasonic, Vegas At Night, The Grail, Four & More, Top Speed
- **Autograph Sets**: Chrome Autographs, 1975 Speed Wheel Signatures, Circuit Masters Signatures, Futuro Chrome Autographs, On-Card Chrome Autographs, F1 Debut Patch Autographs
- **Relic Sets**: F1/F2/F3 Diamond Anniversary Base Relic Cards
- **Special**: F175 Anniversary Logo insert`,
    tags: ["box-config", "odds"],
    setId: 51,
  },
  {
    id: "097-disneyland-70th-2025",
    title: "New Set: 2025 Topps Disneyland 70th Anniversary",
    date: "2026-04-11T12:00:00Z",
    summary: "Full checklist added for 2025 Topps Disneyland 70th Anniversary with 498 cards across 23 insert sets, 480 unique subjects, and pack odds for Hobby, Value, and Disneyland Exclusive formats.",
    description: `## 2025 Topps Disneyland 70th Anniversary

Complete checklist now available with box configurations and pack odds across three formats.

- **150 Base Cards** across four subsets: Then And Now (82), Timeline (17), Snack Time (18), and Concept Art (33) with Rainbow Foil, Green /199, Aqua Electric Dots /150, Blue /99, 70th Anniversary /70, Gold /50, Orange /25, Black /10, Red /5, and Foilfractor /1
- **Attraction Autographs** (19 cards) featuring voice actors including Bret Iwan (Mickey Mouse), Tim Allen (Buzz Lightyear), and Margaret Kerry (Tinker Bell)
- **1955 Topps Disneyland Icons Autographs** (18 cards) with the same voice actor roster in retro design
- **Enchanted Relics** (56 cards) featuring authentic Disney memorabilia including Disney Dollars, vintage tickets, cast member costumes, and park banners
- **Chrome Insert Sets**: 1977 Star Tours (/87), Eighth Wonder (/55), Tomorrowland Cosmic (/77), It's A Small World, A Pirate's Life, Entrance To Magic, Welcome Foolish Mortals, Greetings From The Tiki Room
- **Additional Inserts**: 1954 Disneyland On Wheels, 1955 Disneyland Icons, From Silver Screen To Main Street, Posters, The Lands, Character Nametags (/70)
- **Sketch Cards** (77 artists), Collector's Pin Relic Redemption
- **Pack odds** across Hobby (91 entries), Value (87 entries), and Disneyland Exclusive (104 entries)`,
    tags: ["checklist", "box-config", "odds"],
    setId: 50,
  },
  // ─── April 10, 2026 ──────────────────────────────────────────────────────
  {
    id: "096-chrome-wwe-2026-odds",
    title: "Pack Odds Added: 2026 Topps Chrome WWE",
    date: "2026-04-10T12:00:00Z",
    summary: "Pack odds added for 2026 Topps Chrome WWE with 985 odds entries across 7 box types: Breaker's Delight, Hobby, Logofractor, Mega, Sapphire, Value, and First Day Issue.",
    description: `## 2026 Topps Chrome WWE — Pack Odds

Pack odds now available across all 7 box formats, covering 985 total entries:

- **Breaker's Delight** (7150): Base Geometric and standard parallels, Scope/Viral Shock/Women's Division Geometric variants, all autograph sets with Geometric parallels, GPK, Buybacks, Hidden Gems (Citrine, Alexandrite, Painite)
- **Hobby** (7151): Full base parallel breakdown (Refractor through Superfractor), Prism/Negative/Sonar/Steel Cage/FrozenFractor exclusives, Alternate Persona & Iconic Imprints Image Variations, all insert sets (Scope, Viral Shock, Women's Division, Austin 3:16, Rock Diamond Legacy, Platinum Punk, Family Tree, Embedded), House of Cards, Feel The Pop!, all autograph tiers, Buyback parallels (X-Fractor through Purple)
- **Logofractor** (7152): WWE Logofractor base and parallels (Green through Rose Gold), Wrestlemania Recall/Eras of Excellence/Focus Reel Logofractor variants, Logofractor Autographs
- **Mega Box**: X-Fractor and Mini Diamond base exclusives, Wrestlemania Recall/Eras of Excellence/Focus Reel with full Refractor parallels, all autograph sets
- **Sapphire** (7156): Sapphire base parallels (Yellow through Padparadscha), Sapphire Selections, Infinite insert, Sapphire autograph variants across all brand/premium sets
- **Value Box**: Diamond Plate and RayWave base exclusives, retail insert sets with Refractor parallels, all autograph sets
- **First Day Issue** (7435): FDI Refractor exclusive, Hobby-style parallels, full insert and autograph coverage including FDI-exclusive autos`,
    tags: ["odds"],
    setId: 48,
  },
  // ─── April 9, 2026 ───────────────────────────────────────────────────────
  {
    id: "095-pristine-baseball-2025",
    title: "New Set: 2025 Topps Pristine Baseball",
    date: "2026-04-09T14:00:00Z",
    summary: "Full checklist added for 2025 Topps Pristine Baseball with 300 base cards, 18 insert sets, 339 players, and 90 pack odds entries.",
    description: `## 2025 Topps Pristine Baseball

Complete checklist now available with Hobby box configuration and full pack odds.

- **300 Base Cards** (250 unique players + 50 image variations) with 20 parallel variations including Pristine and standard Refractor lines from Aqua /199 through Pristine Black Refractor /1 and Superfractor /1
- **Pristine Autographs** (96 cards) with 9 parallels from Green Pristine /150 to Black Pristine /1
- **Pristine Pair Autographs** (6 dual-signed cards) featuring iconic pairings like McGwire/Pujols, Holliday/Henderson, and Crews/Wood
- **Plated and Polished Autographs** (20 cards), **Personal Endorsements Autographs** (32 cards), and **Italics Autographs** (15 cards)
- **Auto Relics**: Popular Demand (35 cards), Pristine Pieces (58 cards), All-Star Game Pristine Pieces (27 cards, all /1), and Rookie Jumbo (19 cards, all /25)
- **Insert Sets**: Perseverance (25), Plated & Polished (40), Precisionaries (35), Pearlescent (25), Amped (25), Prowlers (15), Monogram (30), Let's Go (5)
- **90 pack odds entries** covering all base parallels, insert sets, autographs, and auto relics`,
    tags: ["checklist", "box-config", "odds"],
    setId: 49,
  },
  {
    id: "094-chrome-wwe-2026",
    title: "New Set: 2026 Topps Chrome WWE",
    date: "2026-04-09T12:00:00Z",
    summary: "Full checklist added for 2026 Topps Chrome WWE with 201 base cards, 53 insert sets, and 269 wrestlers.",
    description: `## 2026 Topps Chrome WWE

Complete checklist now available with box configurations for Hobby, First Day Issue, Value, Mega, and Breaker's Delight formats.

- **201 Base Cards** across Base I (100), Base II (100), and Base Tier III (1) with 44 parallel variations including Refractor, Diamond Plate, Geometric, X-Fractor, Mini Diamond, RayWave, and FrozenFractor exclusives
- **25 Alternate Personas** and **75 Iconic Imprints** base subsets (Hobby Exclusive, Superfractor /1 only)
- **Chrome Autographs** (91 cards) plus FDI Exclusives and Tier III, with Red/Blue/NXT Brand Autographs (92 cards combined)
- **Premium Autographs**: Marks of Champions, Legendary Chrome, Main Event, 1986 Topps, Hall of Fame, and Future Stars
- **Hobby Exclusive Autographs**: Iconic Imprint Autos (/10), Alternate Personas Autos (/10), Dual Autos, Best In The World, 3D Dual, The People's Champ, Anniversary sets (Austin, Dudley Boyz, CM Punk, Rock, NWO, Lita, Trish), Beast Incarnate, Say His Name
- **Main Roster Debut Patch Autographs** (all /1): Giulia, JC Mateo, Roxanne Perez, Sol Ruca, Stephanie Vaquer
- **Insert Sets**: Scope, Viral Shock, Women's Division, Austin 3:16, Rock Diamond Legacy, Platinum Punk, Family Tree, Embedded, Wrestlemania Recall, Eras of Excellence, Focus Reel, Signalz, Gamut, House of Cards, Helix, Let's Go, Feel The Pop!, GPK, and 2025 Chrome Buybacks`,
    tags: ["checklist", "box-config"],
    setId: 48,
  },
  // ─── April 6, 2026 ───────────────────────────────────────────────────────
  {
    id: "093-midnight-basketball-2025-odds",
    title: "Pack Odds Added: 2025-26 Topps Midnight Basketball",
    date: "2026-04-06T14:00:00Z",
    summary: "Pack odds added for 2025-26 Topps Midnight Basketball with 219 odds entries across base parallels, rookie autographs, veteran autographs, inserts, and memorabilia.",
    description: `## 2025-26 Topps Midnight Basketball — Pack Odds

Pack odds now available for the Hobby box format, covering 219 entries including:

- **Base parallels**: Zodiac (1:2), Morning (1:4), Twilight (1:6), Dusk (1:8), through Black Light (1:549)
- **Rookie Autographs**: Rookie Jersey Autographs (1:5), Rookie Horizon Signatures (1:5), Stroke of Midnight Autographs Rookies (1:8), Midnight Sun Signatures Rookies (1:9) — each with full parallel breakdowns through Black Light
- **Rookie Memorabilia**: Dark Marks Rookies (1:23), Dark Matter Autographs Rookies (1:21), Midnight Oil Marks Rookies (1:54)
- **Veteran Autographs**: Stroke of Midnight Autographs (1:4), Dark Matter Autographs (1:17), Midnight Sun Signatures (1:27), Stroke of Midnight Autographs II
- **Veteran Memorabilia**: Dark Marks (1:9), Midnight Oil Marks (1:15)
- **4 Insert Sets**: Night Owls (1:8), Insomnia (1:8), Moonfall (1:7), Daydreamers (1:10) — each with full parallel breakdowns
- **Short Prints**: Nightshade (1:28), Dreamland (1:28), Night Vision (1:33), Twilight (1:54)`,
    tags: ["odds"],
    setId: 24,
  },
  {
    id: "092-chrome-mcdonalds-basketball-2025-odds",
    title: "Pack Odds Added: 2025 Topps Chrome McDonald's All-American Basketball",
    date: "2026-04-06T12:00:00Z",
    summary: "Pack odds added for 2025 Topps Chrome McDonald's All-American Basketball with 73 odds entries across base parallels, inserts, autographs, and relics.",
    description: `## 2025 Topps Chrome McDonald's All-American Basketball — Pack Odds

Pack odds now available for the Hobby box format, covering 73 entries including:

- **Base parallels**: Refractor (1:1), McFlurry (1:1), Aqua Wave (1:4), Purple (1:5), Red Lava (1:6), Gold (1:15), Tie-Dye (1:30), Orange (1:50), Black (1:75), Red (1:150), Black Wave (1:340), Red Wave (1:678), Superfractor (1:746)
- **4 Insert Sets**: High Rises (1:3), Top Recruits (1:3), Prospect Paths (1:5), Hype to Legacy (1:9) — each with Refractor, Gold, Tie-Dye, Red, and SuperFractor parallels
- **BillBoard Ink Autographs**: Refractor (1:9) through SuperFractor (1:1904)
- **Event Autographs** (1:6), **Golden Patch Autographs**, and **Legends Autographs** with full parallel breakdowns
- **Winning Tags Autographs**: Refractor (1:9) through SuperFractor (1:1904)
- **All-American Drip** insert (1:48)`,
    tags: ["odds"],
    setId: 39,
  },
  // ─── April 5, 2026 ───────────────────────────────────────────────────────
  {
    id: "091-royalty-ufc-2024",
    title: "New Set: 2024 Topps Royalty UFC",
    date: "2026-04-05T12:00:00Z",
    summary: "Full checklist added for 2024 Topps Royalty UFC with 100 base cards, 27 insert sets, and 213 fighters.",
    description: `## 2024 Topps Royalty UFC

Complete checklist now available with 100 base cards, 27 insert and autograph sets, and 213 fighters from across the UFC roster.

Highlights include:
- **Base Set** (100 cards) with 7 parallel levels: /99, Purple /35, Blue /25, Red /15, Gold /10, Green /5, Platinum /1
- **17 Autograph Sets** including UFC Honors Autographs (/25), Dual Autographs (21 pairings), Triple Autographs (5 trios), and Dual Fighter Relic Autograph Books (8 cards)
- **Regalia Relic Signatures** (61 cards), **Pursuit of Greatness Signatures** (35 cards), **Royalty Relic Signatures** (35 cards), and **Superior Signatures** (34 cards)
- **5 Memorabilia/Relic Sets**: Regalia Relics (74 cards), Star Relics (50 cards), Relic Jewels (30 cards), Rookie Jumbo Relics (26 cards), and Prodigious Pairings (20 dual-fighter cards)
- **4 Insert Sets**: Royal Decree (28), The Coronation (14), The Time Is Now (12), Liquid Silver (10)
- Notable fighters include Conor McGregor, Islam Makhachev, Alex Pereira, Sean O'Malley, Khabib Nurmagomedov, Jon Jones, and many more`,
    tags: ["checklist", "odds", "box-config"],
    setId: 47,
  },
  // ─── April 3, 2026 ───────────────────────────────────────────────────────
  {
    id: "090-chrome-deadpool-2025",
    title: "New Set: 2025 Topps Chrome Deadpool",
    date: "2026-04-03T22:00:00Z",
    summary: "Full checklist added for 2025 Topps Chrome Deadpool with 100 base cards across 3 subsets, 22 insert sets, and 131 characters.",
    description: `## 2025 Topps Chrome Deadpool

Complete checklist now available with 100 base cards, 22 insert and autograph sets, and 131 characters from the Deadpool and Wolverine universe.

Highlights include:
- **Base Set** split across Comic Accurate (20), Characters (26), and Multiverse And More (54) with 24 parallel styles
- **Chrome Autographs** (26 cards) signed by cast members including Ryan Reynolds, Hugh Jackman, Emma Corrin, and Henry Cavill
- **Best Bubs Autographs** (13 cards) and **Chrome Dual Autographs** (9 cards)
- **On-Card Dual Inscription Booklet** featuring Wolverine and Deadpool signed by Hugh Jackman and Ryan Reynolds
- **Marvel Comic Book Artist Autographs** (6 cards) featuring Carlo Barberi, Ed McGuinness, Mark Brooks, and more
- **Insert sets**: Comic Book Gold (30), Cover Stars (30), Well You Got Nothing To Say Mouth (10), Future Stars (10), The Void (10), Deadpool Icons (10), and more`,
    tags: ["checklist"],
    setId: 46,
  },
  {
    id: "089-stadium-club-baseball-2025",
    title: "New Set: 2025 Topps Stadium Club Baseball",
    date: "2026-04-03T20:00:00Z",
    summary: "Full checklist added for 2025 Topps Stadium Club Baseball with 200 base cards, 8 autograph sets, 5 insert sets, and 345 players.",
    description: `## 2025 Topps Stadium Club Baseball

Complete checklist now available with 200 base cards, 14 insert and autograph sets, and 345 players.

Highlights include:
- **Base Set** (200 cards) with 15 parallel styles including Sepia, Rainbow Foilboard, and Photographer's Proof
- **Base Autographs** (161 cards) and **Chrome Autographs** (73 cards) covering legends and current stars
- **Savage Sluggers Autographs** (18 cards), **Goin' Yard Autographs** (16 cards), **Abstract Autographs** (14 cards), and **Concentration Autographs** (12 cards)
- **In Case Of Emergency Autographs** (17 cards) and **Dual Autographs** (9 cards) pairing legends with current stars
- **Insert sets**: Beam Team (20 cards), Savage Sluggers (25), Concentration (25), Yours For The Taking (25), In Case Of Emergency (25)
- Notable players include Shohei Ohtani, Aaron Judge, Roki Sasaki, Bobby Witt Jr., Juan Soto, Derek Jeter, and many more`,
    tags: ["checklist"],
    setId: 45,
  },
  {
    id: "088-chrome-uefa-2526-boxconfig-release",
    title: "Box Config & Release Date: Chrome UEFA Club Competitions",
    date: "2026-04-03T18:00:00Z",
    summary: "Updated box configuration and release date (May 7, 2026) for 2025-26 Topps Chrome UEFA Club Competitions across 6 box types.",
    description: `## Box Config & Release Date for 2025-26 Topps Chrome UEFA Club Competitions

Release date set to **May 7, 2026**.

Updated box configuration now available for 6 box types:

- **Hobby** — 20 packs/box, 12 boxes/case, 1 auto/box. 1 Road to Glory auto per case guaranteed. 2x Grail Chase.
- **First Day Issue** — 4 cards/pack, 20 packs/box, 12 boxes/case, 1 auto/box, 2 FDI exclusive parallels/box
- **Breaker's Delight** — 1 pack/box, 6 boxes/case, 2 autos/box. 1 Global Attraction auto per case guaranteed.
- **Jumbo** — 12 packs/box, 8 boxes/case, 3 autos/box
- **Logofractor** — 7 packs/box, 20 boxes/case
- **Sapphire** — 8 packs/box, 10 boxes/case, 1 auto/box`,
    tags: ["box-config"],
    setId: 43,
  },
  {
    id: "087-chrome-football-2025",
    title: "New Set: 2025 Topps Chrome Football",
    date: "2026-04-03T12:00:00Z",
    summary: "Full checklist added for 2025 Topps Chrome Football — 400 base cards, 39 insert sets, and over 540 players.",
    description: `## 2025 Topps Chrome Football

Complete checklist now available with 400 base cards, 39 insert and autograph sets, and 547 players.

Highlights include:
- **Base Set** (400 cards) with 100 rookies and 6 variation sets (Camo, Lightboard Logo, Chrome Etch, Image Variation, and more)
- **16 insert sets** including Future Stars, 1975 Topps, Power Players, Legends of the Gridiron, Fortune 15, Helix, Shadow Etch, Kaiju, and more
- **9 autograph sets** including Base Cards Autograph Variation (70 cards), Rookies Autograph Variation (94 cards), Dual Autographs, Chromographs, Chrome Legends Autographs, and Hall of Chrome Autographs
- **3 relic sets** and **2 autograph relic sets** including Topps Chrome Rookie Patch Autographs and Rookie Premiere Patch Autographs (98 cards)
- **Legends** including Tom Brady, Peyton Manning, Barry Sanders, Jerry Rice, Walter Payton, Ray Lewis, and many more`,
    tags: ["checklist"],
    setId: 44,
  },
  // ─── April 2, 2026 ───────────────────────────────────────────────────────
  {
    id: "086-chrome-uefa-2526-odds",
    title: "Pack Odds & Box Config: Chrome UEFA Club Competitions",
    date: "2026-04-02T18:00:00Z",
    summary: "Full pack odds added for 2025-26 Topps Chrome UEFA Club Competitions across 11 box types: Hobby, Jumbo, Value, Breaker's Delight, Hanger, Sapphire, Mega, First Day Issue, Logofractor, Hongbao, and FFNYC.",
    description: `## Pack Odds for 2025-26 Topps Chrome UEFA Club Competitions

Complete pack odds now available across 11 box types with over 1,200 individual odds entries:

- **Hobby** — 204 entries
- **Jumbo** — 199 entries
- **Value** — 150 entries
- **Breaker's Delight** — 123 entries
- **Hanger** — 100 entries
- **Sapphire** — 37 entries
- **Mega** — 135 entries
- **First Day Issue** — 99 entries
- **Logofractor** — 60 entries
- **Hongbao** — 19 entries
- **FFNYC** — 102 entries

Box configuration added for all 8 purchasable formats. The Break Hit Calculator and Pack Odds page now support all formats.`,
    tags: ["odds", "box-config"],
    setId: 43,
  },
  {
    id: "085-chrome-uefa-2526",
    title: "New Set: 2025-26 Topps Chrome UEFA Club Competitions",
    date: "2026-04-02T12:00:00Z",
    summary: "Full checklist added for 2025-26 Topps Chrome UEFA Club Competitions — 200 base cards, 36 insert sets, and over 350 players.",
    description: `## 2025-26 Topps Chrome UEFA Club Competitions

Complete checklist now available with 200 base cards, 36 insert and autograph sets, and over 350 players spanning UEFA Champions League, Europa League, and Conference League clubs.

Highlights include:
- **Base Set** (200 cards) with a Future Stars subset
- **19 insert sets** including Wonderkids, Shadow Etch, Budapest at Night, Helix, Chrome Anime, and more
- **17 autograph sets** including Chrome Autographs (109 cards), Chrome Legends Autographs (67 cards), Road to Glory Autographs (63 cards), and multi-player cards (Dual, Triple, Quad, and Piece of Club History book cards)
- **UCL Final Performers** featuring Linkin Park members
- **Legends** including Messi, Ronaldinho, Zidane, Beckham, Maldini, and many more`,
    tags: ["checklist"],
    setId: 43,
  },
  // ─── April 1, 2026 ───────────────────────────────────────────────────────
  {
    id: "084-topps-basketball-2526-retail-odds",
    title: "Full Retail Pack Odds: 2025-26 Topps Basketball",
    date: "2026-04-01T12:00:00Z",
    summary: "Break Hit Calculator for 2025-26 Topps Basketball now includes pack odds for all six box types: Hobby, Jumbo, Value, Mega, Fat Pack, and Hanger.",
    description: `## Full Multi-Format Pack Odds

The Break Hit Calculator for 2025-26 Topps Basketball has been updated with complete pack odds across all six box types:

- **Hobby** — 12 cards/pack, 20 packs/box
- **Jumbo** — 40 cards/pack, 10 packs/box
- **Value** — 12 cards/pack, 12 packs/box
- **Mega** — 14 cards/pack, 16 packs/box
- **Fat Pack** — 26 cards/pack, 12 packs/box
- **Hanger** — 40 cards/pack, 1 pack/box

Each box type has its own exclusive insert sets and parallel families. Retail formats (Value, Mega, Fat Pack, Hanger) feature Holo Foil and Diamante parallels, along with retail-exclusive insert sets like 8 Bit Ballers, Generation Now, Power Players, and Clutch City Prospects. Hobby and Jumbo formats carry Rainbow parallels, plus insert sets like The Daily Dribble, New School, Levitation, and more.

All autograph and relic insert sets (Flagship Real One Autographs, 1980-81 Topps Basketball Autographs, Topps Notch Signatures, New Applicants Autographs, Signed and Sealed, Franchise Fabrics, Swish and Stitch Relics, Woven Wonders Relics) now have per-format odds across all six box types.`,
    tags: ["odds", "box-config"],
    setId: 31,
  },
  // ─── March 31, 2026 ──────────────────────────────────────────────────────
  {
    id: "083-finest-pl-production-run",
    title: "Break Hit Calculator: Production Run Accuracy for 2026 Topps Finest Premier League",
    date: "2026-03-31T19:00:00Z",
    summary: "Break Hit Calculator now uses total production run data for more accurate numbered parallel odds on 2026 Topps Finest Premier League.",
    description: `## Production Run Accuracy

The Break Hit Calculator for 2026 Topps Finest Premier League now uses the known total production run to compute exact odds for numbered parallels, replacing the estimate-based approach for cards with known print runs.`,
    tags: ["odds"],
    setId: 33,
  },
  {
    id: "082-cosmic-chrome-production-run",
    title: "Break Hit Calculator: Production Run Accuracy for 2025-26 Topps Cosmic Chrome Basketball",
    date: "2026-03-31T18:00:00Z",
    summary: "Break Hit Calculator now uses total production run data for more accurate numbered parallel odds on 2025-26 Topps Cosmic Chrome Basketball.",
    description: `## Production Run Accuracy

The Break Hit Calculator for 2025-26 Topps Cosmic Chrome Basketball now uses the known total production run (79,440 boxes / 1,588,800 packs) to compute exact odds for numbered parallels.

For cards with known print runs, the calculator now uses the formula:

> per-pack probability = (player copies × print run) / total packs produced

This replaces the estimate-based approach for numbered cards, giving exact odds when production data is available.`,
    tags: ["odds"],
    setId: 35,
  },
  {
    id: "081-cactus-jack-basketball-2526-release-date",
    title: "Release Date: 2025-26 Topps Chrome Cactus Jack Basketball",
    date: "2026-03-31T12:00:00Z",
    summary: "Release date set to February 13, 2026 for 2025-26 Topps Chrome Cactus Jack Basketball.",
    description: `## Release Date: 2025-26 Topps Chrome Cactus Jack Basketball

Release date set to **February 13, 2026**.`,
    tags: ["checklist"],
    setId: 23,
  },
  {
    id: "080-cosmic-chrome-basketball-2526-box-config",
    title: "Box Config & Release Date: 2025-26 Topps Cosmic Chrome Basketball",
    date: "2026-03-31T12:00:00Z",
    summary: "Box configuration and April 29 release date added for 2025-26 Topps Cosmic Chrome Basketball.",
    description: `## Box Config: 2025-26 Topps Cosmic Chrome Basketball

Release date set to **April 29, 2026**.

Two box formats configured:

- **Hobby** — 4 cards/pack, 20 packs/box (mirroring First Day Issue config until hobby config is confirmed)
- **First Day Issue** — 4 cards/pack, 20 packs/box

Break Hit Calculator is now fully active with pack odds and box configuration.`,
    tags: ["box-config"],
    setId: 35,
  },
  // ─── March 30, 2026 ──────────────────────────────────────────────────────
  {
    id: "079-cosmic-chrome-basketball-2526-odds",
    title: "Pack Odds Added: 2025-26 Topps Cosmic Chrome Basketball",
    date: "2026-03-30T12:00:00Z",
    summary: "Pack odds are now live for 2025-26 Topps Cosmic Chrome Basketball with 126 entries across all insert sets and parallels.",
    description: `## Pack Odds: 2025-26 Topps Cosmic Chrome Basketball

126 pack odds entries covering:

- **Base cards** — 15 parallel tiers (Refractor through SuperFractor, plus White Hole, FDI 1, and Lunar)
- **Galaxy Greats** — base + 10 refractor parallels
- **Extraterrestrial Talent** — base + 10 refractor parallels
- **Propulsion** — base + 10 refractor parallels
- **Space Walk** — base + 10 refractor parallels
- **Case hits:** StarFractor (1:609), Re-Entry (1:871), Geocentric (1:1109), First Light (1:1109), each with 4 parallels
- **Hyper Nova** (1:201) and **Cosmic Dust** (1:793)
- **Planetary Pursuit** — 10-tier system (Sun through Pluto)
- **6 autograph sets:** Cosmic Chrome Autograph Variation, Singularity Signatures, Alien Autographs, Electro-Static Signatures, First Flight Signatures, and Cosmic Chrome Autograph Variation II — each with up to 5 refractor parallels

Break Hit Calculator is now active for all Cosmic Chrome Basketball player pages.`,
    tags: ["odds"],
    setId: 35,
  },
  {
    id: "078-finest-basketball-2025-odds",
    title: "Pack Odds Added: 2025-26 Topps Finest Basketball",
    date: "2026-03-30T12:00:00Z",
    summary: "Hobby and Breaker pack odds are now live for 2025-26 Topps Finest Basketball (223 entries).",
    description: `## Pack Odds: 2025-26 Topps Finest Basketball

### Hobby (217 entries)
- Base Common / Uncommon / Rare cards and all parallel tiers (Refractor, Oil Spill, Xfractor, Sky Blue, Purple, Blue, Green, Gold, Orange, Black, Red, SuperFractor)
- Geometric parallels across all base rarities
- Insert sets: Arrivals, Muse, First, Finishers — with all parallel tiers
- Autographs and Rookie Autographs — base through SuperFractor
- Baseline Autographs and Masters Autographs — base through SuperFractor
- Electrifying Signatures and Colossal Shots Autographs — Geometric tiers
- Case hits: Pulse (1:62), The Man (1:480), Headliners (1:648), Aura (1:962)

### Breaker (6 entries)
- Pulse, The Man, Headliners, Aura — base and SuperFractor`,
    tags: ["odds"],
    setId: 25,
  },

  // ─── March 29, 2026 ──────────────────────────────────────────────────────
  {
    id: "077-universe-wwe-2025-box-config",
    title: "Box Config Added: 2025 Topps Universe WWE",
    date: "2026-03-29T12:00:00Z",
    summary: "Hobby and Value Blaster box configurations are now live for 2025 Topps Universe WWE.",
    description: `## Box Configuration: 2025 Topps Universe WWE

### Hobby
- 12 cards per pack · 10 packs per box · 12 boxes per case
- **Guarantees:** 2 autographs, 1 relic, 3 numbered parallels, 1 ring parallel, 3 additional parallels, 12 inserts per box

### Value Blaster
- 6 cards per pack · 6 packs per box · 40 boxes per case
- **Guarantees:** 2 galaxy parallels, 1 numbered card, 3 inserts per box

Release date: February 27, 2026`,
    tags: ["box-config"],
    setId: 20,
  },
  // ─── March 28, 2026 ──────────────────────────────────────────────────────
  {
    id: "076-museum-collection-baseball-2025-box-config",
    title: "Box Config Added: 2025 Topps Museum Collection Baseball",
    date: "2026-03-28T23:50:00Z",
    summary: "Hobby box configuration is now live for 2025 Topps Museum Collection Baseball.",
    description: `## Box Configuration: 2025 Topps Museum Collection Baseball

### Hobby
- 8 cards per pack · 1 pack per box · 8 boxes per case
- **Guarantees:** 1 autograph relic, 1 autograph, 1 memorabilia card, 2 base parallels, 3 base cards per box

Release date: February 5, 2026`,
    tags: ["box-config"],
    setId: 42,
  },
  {
    id: "075-museum-collection-baseball-2025-odds",
    title: "Pack Odds Added: 2025 Topps Museum Collection Baseball",
    date: "2026-03-28T23:45:00Z",
    summary: "Hobby box pack odds are now live for 2025 Topps Museum Collection Baseball with 150 odds entries.",
    description: `## Pack Odds: 2025 Topps Museum Collection Baseball

### Hobby
150 pack odds entries covering base cards, parallels, autographs, relics, framed cards, signature swatches, book cards, cut signatures, and more.`,
    tags: ["odds"],
    setId: 42,
  },
  {
    id: "074-museum-collection-baseball-2025",
    title: "Checklist Added: 2025 Topps Museum Collection Baseball",
    date: "2026-03-28T23:30:00Z",
    summary: "Full checklist for 2025 Topps Museum Collection Baseball is now live with 26 insert sets and 1,079 cards.",
    description: `## Checklist: 2025 Topps Museum Collection Baseball

Premium tier set with 26 insert sets, 1,079 total cards, and 320 unique players.

Includes Base Set, Canvas Collection Original Player Autographs, Archival Autographs, Atelier Autographed Book Cards, Showpieces Autographs, Dual On Card Autographs, Triple On Card Autographs, Museum Framed Autographs, Framed HOF Autographs, Retrospective Signatures, Museum Framed Autograph Patch Cards, Museum Framed Dual Autograph Patch Book Cards, Momentous Material Jumbo Patch Autographs, Momentous Material Dual Jumbo Patch Autograph Book Cards, Single Player Signature Swatches (Dual, Triple, and Quad Relic Autographs), Autographed Jumbo Lumber Bat Relics, Dual Autographed Jumbo Lumber Bat Relics Book Cards, MLB Authenticated Relic Autograph Cards, Meaningful Material Relics, Museum Quality Cut Signatures, Museum Quality Cut Signature Relics, Four Player Primary Pieces Quad Relics, and Dual Player Primary Pieces Quad Relics (including Legends).

No parallels in this set.`,
    tags: ["checklist"],
    setId: 42,
  },
  {
    id: "073-bowman-draft-sapphire-box-config",
    title: "Box Config Added: 2025 Bowman Draft Sapphire Baseball",
    date: "2026-03-28T23:00:00Z",
    summary: "Hobby box configuration is now live for 2025 Bowman Draft Sapphire Baseball.",
    description: `## Box Configuration: 2025 Bowman Draft Sapphire Baseball

### Hobby
- 4 cards per pack · 8 packs per box · 10 boxes per case
- **Guarantees:** 1 auto per box, 3 numbered parallels per box

Release date: February 11, 2026`,
    tags: ["box-config"],
    setId: 41,
  },
  {
    id: "072-bowman-draft-sapphire-2025",
    title: "New Checklist: 2025 Bowman Draft Sapphire Baseball",
    date: "2026-03-28T22:00:00Z",
    summary: "Full checklist for 2025 Bowman Draft Sapphire Baseball is now live — 200 prospects, 263 cards across 4 insert sets with pack odds.",
    description: `## 2025 Bowman Draft Sapphire Baseball

- **200 prospects** from the 2025 MLB Draft class
- **200-card base set** with 6 Sapphire parallel types: Yellow /75, Gold /50, Orange /25, Black /10, Red /5, Padparadscha /1
- **Chrome Prospect Autographs** (30 cards) with 6 parallel tiers down to Padparadscha Sapphire /1
- **Sapphire Selections Autographs** (15 cards) with Orange /25, Red /5, Superfractor /1
- **Sapphire Selections** insert (18 cards) with Gold /50, Orange /25, Red /5, Superfractor /1
- Full pack odds included for all parallels and insert sets`,
    tags: ["checklist"],
    setId: 41,
  },
  {
    id: "071-stadium-club-ufc-box-config",
    title: "Box Config Added: 2025 Topps Stadium Club UFC",
    date: "2026-03-28T20:00:00Z",
    summary: "Hobby, Mega, and Value box configurations are now live for 2025 Topps Stadium Club UFC.",
    description: `## Box Configuration: 2025 Topps Stadium Club UFC

### Hobby
- 8 cards per pack · 16 packs per box · 16 boxes per case
- **Guarantees:** 2 autos per box, 16 Red Foil parallels, 2 Black Foil parallels, 1 Gold parallel, 1 numbered base parallel, 8 inserts, 16 Chrome variations, 2 Chrome Refractors

### Mega
- 10 cards per pack · 6 packs per box · 20 boxes per case
- **Guarantees:** 6 Teal Foil parallels, 3 Orange Foil parallels, 1 Black Foil parallel, 3 Chrome X-Fractor parallels

### Value
- 5 cards per pack · 6 packs per box · 40 boxes per case
- **Guarantees:** 6 Teal Foil parallels, 1 Black Foil parallel, 1 Sepia parallel, 1 Chrome Lava parallel

Release date: January 23, 2026`,
    tags: ["box-config"],
    setId: 40,
  },
  {
    id: "070-stadium-club-ufc-2025",
    title: "New Checklist: 2025 Topps Stadium Club UFC",
    date: "2026-03-28T18:00:00Z",
    summary: "Full checklist for 2025 Topps Stadium Club UFC is now live — 236 fighters, 923 cards across 17 insert sets.",
    description: `## 2025 Topps Stadium Club UFC

- **236 fighters** including legends and current UFC roster
- **200-card base set** with 16 parallel types including Red Foil, Gold Rainbow Foil /1, and Photographer's Proof
- **200-card Base Chrome** mirror with 10 refractor parallels including Superfractor /1
- **50 Base Image Variations** and **50 Rookie Design Variations**
- **6 autograph sets:** Base Autographs (96), Chrome Autographs (91), Beam Team Autographs (25), Co-Signers (9), Lone Star Signatures (29), Power Packed Autographs (35)
- **7 insert sets:** Hype Machines (20), Dynasty And Destiny (20), Instavision (10), Power Packed (20), Special Forces (30), Beam Team (20), Triumvirates (18)
- Co-Signers feature dual-autograph cards with fighter pairings`,
    tags: ["checklist"],
    setId: 40,
  },
  {
    id: "069-mcdonalds-allamerican-box-config",
    title: "Box Config Added: 2025 Topps Chrome McDonald's All-American Basketball",
    date: "2026-03-28T15:00:00Z",
    summary: "Hobby and Mega box configurations are now live for 2025 Topps Chrome McDonald's All-American Basketball.",
    description: `## Box Configuration: 2025 Topps Chrome McDonald's All-American Basketball

### Hobby
- 15 cards per pack · 4 packs per box · 12 boxes per case
- **Guarantees:** 3 autos per box

### Mega
- 10 cards per pack · 5 packs per box · 20 boxes per case

Release date: March 12, 2026`,
    tags: ["box-config"],
    setId: 39,
  },
  {
    id: "068-mcdonalds-allamerican-basketball-2025",
    title: "New Checklist: 2025 Topps Chrome McDonald's All-American Basketball",
    date: "2026-03-28T12:00:00Z",
    summary: "Full checklist for 2025 Topps Chrome McDonald's All-American Basketball is now live — 62 athletes, 400 cards across 12 insert sets.",
    description: `## 2025 Topps Chrome McDonald's All-American Basketball

- **62 athletes** across East and West rosters
- **100-card base set** featuring current high school prospects and McDonald's All-American alumni
- **5 autograph sets:** Billboard Ink, Legends Autographs, Winning Tags, Event Autographs, Golden Patch Autographs (170 auto cards)
- **6 insert sets:** High Rises, Top Recruits, Prospect Paths, Hype To Legacy, All-American Drip, Concrete Canvas (130 insert cards)
- **8 parallel types** per insert set including Refractor, Purple /299, Blue /199, Green /99, Gold /50, Orange /25, Red /5, and SuperFractor 1/1`,
    tags: ["checklist"],
    setId: 39,
  },
  // ─── March 27, 2026 ──────────────────────────────────────────────────────
  {
    id: "067-panini-select-ufc-box-config",
    title: "Box Config Added: 2022 Panini Select UFC",
    date: "2026-03-27T21:00:00Z",
    summary: "Hobby and Hobby Hybrid box configurations are now live for 2022 Panini Select UFC.",
    description: `## Box Configuration: 2022 Panini Select UFC

### Hobby
- 5 cards per pack · 12 packs per box · 12 boxes per case
- **Guarantees:** 2 autos + 1 memorabilia + 12 Prizm parallels per box

### Hobby Hybrid
- 6 cards per pack · 4 packs per box · 20 boxes per case
- **Guarantees:** 6 Prizm parallels per box

Release date: July 1, 2022`,
    tags: ["box-config"],
    setId: 22,
  },
  {
    id: "066-finest-basketball-box-config",
    title: "Box Config Added: 2025-26 Topps Finest Basketball",
    date: "2026-03-27T17:00:00Z",
    summary: "Hobby and Breaker's Delight box configurations are now live for 2025-26 Topps Finest Basketball.",
    description: `## Box Configuration: 2025-26 Topps Finest Basketball

### Hobby
- 10 cards per pack · 6 packs per box · 8 boxes per case
- **Guarantees:** 2 autos, 12 base parallels, 10 inserts, 6 uncommon base, 2 rare base per box

### Breaker's Delight
- 10 cards per pack · 1 pack per box · 8 boxes per case
- **Guarantees:** 3 autos, 5 base geometric parallels, 2 geometric inserts or case hits per box

Release date: February 26, 2026`,
    tags: ["box-config"],
    setId: 25,
  },
  {
    id: "065-topps-three-basketball-box-config",
    title: "Box Config Added: 2025-26 Topps Three Basketball",
    date: "2026-03-27T16:00:00Z",
    summary: "Hobby and First Day Issue box configurations are now live for 2025-26 Topps Three Basketball.",
    description: `## Box Configuration: 2025-26 Topps Three Basketball

### Hobby
- 4 cards per pack · 1 pack per box · 4 boxes per case
- **Guarantees:** 3 autos or auto relics + 1 base or insert per box

### First Day Issue
- 4 cards per pack · 1 pack per box
- **Guarantees:** 3 autos or auto relics + 1 FDI-exclusive Rookie Patch Auto + 1 base or insert per box`,
    tags: ["box-config"],
    setId: 37,
  },
  {
    id: "064-topps-three-basketball-2526",
    title: "New Set: 2025-26 Topps Three Basketball",
    date: "2026-03-27T15:00:00Z",
    summary: "Full checklist and pack odds for 2025-26 Topps Three Basketball — 100-card base set, 20 autograph sets, 7 insert sets, and 1,171 total cards.",
    description: `## 2025-26 Topps Three Basketball

The complete checklist and pack odds for 2025-26 Topps Three Basketball are now live.

### What's Included
- **100-card base set** (60 veterans, 40 rookies) with Bronze, Blue, Gold, Red, and Platinum parallels
- **20 autograph sets** including Rookie 3 Patch (Horizontal & Vertical), Relics Autographs Prime, Triple Relic Autographs, Veteran 3 Patch, Raindrops Signatures, Thunderdunk Signatures, and more
- **7 insert sets:** Ice Water, Flight Path, Architects, 3 And D, Monsters Of The Deep, The Paint, and Game Time Graphs
- **Triple Relic Autographs** feature 3-player cards with co-player links
- **Pack odds** for all 28 sections and their parallels`,
    tags: ["checklist", "odds"],
    setId: 37,
  },
  {
    id: "063-chrome-sapphire-basketball-box-config",
    title: "Box Config Added: 2025-26 Topps Chrome Basketball Sapphire",
    date: "2026-03-27T14:00:00Z",
    summary: "Hobby box configuration and release date are now live for 2025-26 Topps Chrome Basketball Sapphire.",
    description: `## Box Configuration: 2025-26 Topps Chrome Basketball Sapphire

### Hobby
- 4 cards per pack · 8 packs per box · 10 boxes per case
- **Guarantees:** 1 autograph per box

Release date: January 22, 2026`,
    tags: ["box-config"],
    setId: 26,
  },
  {
    id: "062-chrome-sapphire-basketball-pack-odds",
    title: "Pack Odds Added: 2025-26 Topps Chrome Basketball Sapphire",
    date: "2026-03-27T13:00:00Z",
    summary: "Pack odds are now live for 2025-26 Topps Chrome Basketball Sapphire — 43 parallels and autograph variants covered.",
    description: `## Pack Odds: 2025-26 Topps Chrome Basketball Sapphire

Official pack odds are now available for 2025-26 Topps Chrome Basketball Sapphire, covering all parallel tiers and autograph insert sets.

### Coverage
- **Base parallels:** Sapphire, Purple, Gold, Orange, Black, Red, and Padparadscha
- **Autograph sets:** Topps Chrome Autographs, TCAI Rookies, Next Stop Signatures, SKY-Write Signatures, Signature Style
- **Inserts:** Sapphire Selections (all tiers) and Infinity`,
    tags: ["odds"],
    setId: 26,
  },
  {
    id: "061-cosmic-chrome-basketball-2526",
    title: "New Checklist: 2025-26 Topps Cosmic Chrome Basketball",
    date: "2026-03-27T12:00:00Z",
    summary: "2025-26 Topps Cosmic Chrome Basketball is now in the app — 200-card base set plus 17 insert and autograph sets.",
    description: `## 2025-26 Topps Cosmic Chrome Basketball

The full checklist for 2025-26 Topps Cosmic Chrome Basketball is now live.

### What's Included
- **200-card base set** with rookie cards flagged
- **17 insert & autograph sets:** Cosmic Chrome Autographs, Singularity, Alien Autographs, Electro Static Signatures, First Flight Signatures, Galaxy Greats, Extraterrestrial Talent, Propulsion, Space Walk, Starfractor, Re Entry, Geocentric, First Light, Hyper Nova, Cosmic Dust, and Planetary Pursuit
- **Planetary Pursuit** features 10 planet-themed parallels (Sun through Pluto)
- **First Light** — all 30 cards are rookie cards`,
    tags: ["checklist"],
    setId: 35,
  },
  {
    id: "060-bowman-basketball-box-config",
    title: "Box Config Added: 2025-26 Topps Bowman Basketball",
    date: "2026-03-27T11:00:00Z",
    summary: "Hobby, Jumbo, Mega, Value, and Breaker's Delight box configurations are now live for 2025-26 Topps Bowman Basketball.",
    description: `## Box Configuration

Box configs for all five formats of 2025-26 Topps Bowman Basketball are now live. The Break Hit Calculator on the set page supports a Hobby / Jumbo toggle.

### Hobby
- 8 cards per pack · 20 packs per box · 12 boxes per case
- **Guarantees:** 1 NBA auto + 1 NCAA auto per box

### Jumbo
- 24 cards per pack · 12 packs per box · 8 boxes per case
- **Guarantees:** 2 NBA autos + 2 NCAA autos per box

### Mega
- 7 cards per pack · 6 packs per box · 20 boxes per case

### Value
- 10 cards per pack · 6 packs per box

### Breaker's Delight
- **Guarantees:** 2 NBA autos + 1 NCAA auto per box

Set releases **April 23, 2026**.`,
    tags: ["box-config"],
    setId: 34,
  },

  // ─── March 26, 2026 ──────────────────────────────────────────────────────
  {
    id: "059-updates-page",
    title: "Updates & Changelog Launched",
    date: "2026-03-26T15:30:00Z",
    summary: "Checklist2 now has a public changelog. Every checklist, box config, odds update, and feature launch is documented here.",
    description: `## What's New

Checklist2 now has a dedicated Updates page — the one you're reading right now.

Every time a checklist is added, box configs or pack odds are configured, or a new feature ships, an entry will be added here. Updates are sorted newest first and filterable by tag.

## Tags

- **Checklist** — a new card set has been seeded into the database
- **Box Config** — break format details (cards per pack, packs per box, auto guarantees) have been configured for a set
- **Odds** — pack odds data has been added, powering the Break Hit Calculator
- **Feature** — a new tool, page, or UI capability has been launched
- **Announcement** — general news about the platform

## Going Forward

This changelog reflects the full history of the app from initial launch through today. Future updates will be added as they happen.`,
    tags: ["feature", "announcement"],
  },
  // ─── March 25, 2026 ──────────────────────────────────────────────────────
  {
    id: "058-bowman-basketball-2526",
    title: "Checklist Added: 2025-26 Topps Bowman Basketball",
    date: "2026-03-25T17:00:00Z",
    summary: "2025-26 Topps Bowman Basketball is now live with 37 insert sets, 353 players, and 1,503 total cards — including NBA rookies, prospects, and dual autographs.",
    description: `## 2025-26 Topps Bowman Basketball

The full checklist for 2025-26 Topps Bowman Basketball has been seeded.

## Coverage

- **37 insert sets**
- **353 players** (NBA + college prospects)
- **1,503 total card appearances**
- **20 co-player links** (Bowman Dual Autographs)

## Insert Sets

**Base Cards**
- Base Set (200 cards, #1–55 NBA rookies, #56–200 veterans)
- Base Chrome Variation (BCV-1 through BCV-200)
- Red Rookie Variations (50 cards)
- Etched In Glass Variations
- Retrofractor Variations

**Prospects**
- Base Prospects (BPP-1 through BPP-100, college players)
- Chrome Prospects (BCP-1 through BCP-100)
- Chrome Prospects Etched In Glass Variations

**Autographs**
- Chrome Prospect Autographs (99 cards)
- Chrome Autographs (98 NBA players)
- Retrofractor Autographs
- Future Script Autographs
- Buzz Factor Autographs
- Opening Statement Signatures (25 rookies)
- Timeless Touch Signatures
- Paper Prospect Retail Autographs (100 cards)
- Paper Rookie and Veterans Retail Autographs (99 cards)
- Bowman Dual Autographs (10 dual-player cards)

**Inserts**
- Talent Tracker, Gen Next, Very Important Prospects, Bowman Verified
- ROY Favorites, Hobby Stars, Young Kings
- Rockstar Rookies, Greatness Loading, Mega Rookies, Mega Prospects
- Bowman Spotlights NBA & NIL
- Crystallized NBA & NIL
- Anime NBA & NIL
- Bowman GPK NBA & NIL

## Notable Rookies

Cooper Flagg (Dallas), Dylan Harper (San Antonio), Ace Bailey (Utah), VJ Edgecombe (Philadelphia), Kon Knueppel (Charlotte), Jeremiah Fears (New Orleans), and the full 2025 NBA Draft class.

## Prospects

AJ Dybantsa (BYU), Darryn Peterson (Kansas), Koa Peat (Arizona), Juju Watkins (USC), Sienna Betts (UCLA), and 95 more college players across both men's and women's basketball.`,
    tags: ["checklist"],
    setId: 34,
  },
  // ─── March 24, 2026 ──────────────────────────────────────────────────────
  {
    id: "054-topps-sets-coverage",
    title: "Topps Sets Coverage Page Rebuilt",
    date: "2026-03-24T20:00:00Z",
    summary: "The Topps Sets Coverage page now displays all 273 sets from the 2024–2026 catalog, grouped by year and sport, sourced from a static catalog.",
    description: `## Topps Sets Coverage — Full Catalog

The /sets/topps page has been rebuilt with a comprehensive static catalog covering every Topps set tracked on Checklist2.

## Coverage

- **273 sets** total
- **2026**: 26 sets
- **2025**: 130 sets
- **2025-26**: included within year groupings
- **2024**: 117 sets

## Design

- Grouped by year (collapsible sections)
- Sub-grouped by sport within each year
- Three status pills per set: Checklist, Box Config, Odds
- Same filter/search controls as before

## Sports Covered

Baseball, Basketball, Boxing, Entertainment, Football, MMA, Olympics, Racing, Soccer, Wrestling, and more.`,
    tags: ["feature"],
  },
  {
    id: "056-finest-pl-odds",
    title: "Pack Odds Added: 2026 Topps Finest Premier League",
    date: "2026-03-24T18:00:00Z",
    summary: "Pack odds have been configured for 2026 Topps Finest Premier League, covering 133 card types from base refractors to 1-of-1 Superfractors.",
    description: `## Pack Odds: 2026 Topps Finest Premier League

Pack odds are now live for the 2026 Topps Finest Premier League set. The Break Hit Calculator will now show expected hit rates for this set.

## Coverage

133 unique card types, including:

- Base refractor tiers (Common, Uncommon, Rare) with Saturday 3PM Refractors
- All parallel colors: Checkerboard, Blue, Purple, Green, Pearl, Gold, Orange, Black, Red, Superfractor
- Insert sets: Expected Brilliance, Swerve, Arrivals, Clean (all with parallel tiers)
- Swerve Fusion Variations (6 color combinations)
- Rare inserts: Nightmare Fuel, Gusto, Main Attraction, Polka, Aura, Headliners
- Finest Idols (Bronze, Silver, Gold)
- All autograph sets with full parallel runs
- Dual autograph sets (Finest Partnerships)

## Format

Single flat format — no hobby/jumbo split for this set.`,
    tags: ["odds"],
    setId: 33,
  },
  {
    id: "055-finest-pl-2026",
    title: "Checklist Added: 2026 Topps Finest Premier League",
    date: "2026-03-24T15:30:00Z",
    summary: "2026 Topps Finest Premier League is now live — a Chrome-tier soccer set with 21 insert sets, 307 players, and 767 appearances.",
    description: `## 2026 Topps Finest Premier League

The full checklist for 2026 Topps Finest Premier League (season 2025-26) is now live. This is a Chrome-tier soccer set featuring Premier League players.

## Coverage

- **21 insert sets**
- **307 players**
- **767 total card appearances**
- **30 co-player links** (Finest Partnerships dual autographs)

## Key Insert Sets

- Base Set (Common, Uncommon, Rare tiers with full refractor parallels)
- Expected Brilliance, Swerve, Arrivals, Clean
- Swerve Fusion Variations (6 color combos)
- Nightmare Fuel, Gusto, Main Attraction, Polka, Aura, Headliners
- Finest Idols (Bronze /1200, Silver /2400, Gold /4752)
- Finest Autographs with 10 parallel tiers
- Finest Moments Autographs
- Finest Seasons 1995-96
- Finest Partnerships (dual autographs)
- Arrivals Autograph Edition
- Main Attraction Autograph Edition
- Gustographs
- Finest Fans`,
    tags: ["checklist"],
    setId: 33,
  },
  {
    id: "057-logo-updated",
    title: "App Logo Updated",
    date: "2026-03-24T11:00:00Z",
    summary: "Checklist2 has a new SVG logo with proper light/dark mode support — black text on light backgrounds, white text on dark.",
    description: `## New Logo

The Checklist2 wordmark has been updated with new SVG assets that properly support both light and dark mode.

## Details

- **Light mode**: dark logo (black lettering, gold "2")
- **Dark mode**: light logo (white lettering, gold "2")
- Rendered at 40px height in the navbar, 50px in the footer
- 4:1 aspect ratio (6000×1500 viewBox) — width is auto-calculated

The logo appears in the top-left navbar and the footer.`,
    tags: ["feature"],
  },
  // ─── March 23, 2026 ──────────────────────────────────────────────────────
  {
    id: "005-checklists-sorted-newest",
    title: "Feature: Checklists Sorted Newest First",
    date: "2026-03-23T15:30:00Z",
    summary: "The Checklists page now sorts sets by when they were added to the database, newest first — so the most recently seeded sets are always at the top.",
    description: `## Checklists — Sorted Newest First

Sets on the /checklists page are now sorted by database insertion order (newest first), so newly seeded sets immediately surface at the top of the list without any manual reordering.`,
    tags: ["feature"],
  },
  {
    id: "052-topps-basketball-box-config",
    title: "Box Config Added: 2025-26 Topps Basketball",
    date: "2026-03-23T11:00:00Z",
    summary: "Box configuration is now set for 2025-26 Topps Basketball in both hobby (12 cards/pack × 20 packs) and jumbo (40 cards/pack × 10 packs) formats.",
    description: `## Box Config: 2025-26 Topps Basketball

Break format details have been configured for 2025-26 Topps Basketball, enabling the Break Hit Calculator for both hobby and jumbo boxes.

## Hobby Box

- 12 cards per pack
- 20 packs per box
- 12 boxes per case
- 1 auto or relic per box (guaranteed)

## Jumbo Box

- 40 cards per pack
- 10 packs per box
- 8 boxes per case
- 1 auto per box, 1 relic per box (guaranteed)

The Break Hit Calculator now shows a hobby/jumbo toggle for this set.`,
    tags: ["box-config"],
    setId: 31,
  },
  // ─── March 22, 2026 ──────────────────────────────────────────────────────
  {
    id: "053-topps-basketball-odds",
    title: "Pack Odds Added: 2025-26 Topps Basketball",
    date: "2026-03-22T15:00:00Z",
    summary: "Pack odds are now live for 2025-26 Topps Basketball in both hobby and jumbo formats, enabling accurate break hit calculations for both box types.",
    description: `## Pack Odds: 2025-26 Topps Basketball

Hobby and jumbo pack odds are now configured for 2025-26 Topps Basketball. The Break Hit Calculator toggle between hobby and jumbo is now fully functional for this set.

## Format

Nested hobby/jumbo structure — both box formats have distinct odds for every parallel and insert set.

## Coverage

All base parallels, insert sets, and autograph sets including:
- Base Gold, FoilFractor, Purple Rainbow, Rainbow Foilboard
- All insert parallels
- Flagship Real Ones Autographs (hobby and jumbo)
- All signature sub-sets with parallel tiers

## ODDS_KEY_OVERRIDES

17 name-mapping overrides were added to reconcile the database insert set names with the pack odds key naming convention (e.g., plural vs. singular, article differences, "1980-81 Topps Basketball" insert prefix).`,
    tags: ["odds"],
    setId: 31,
  },
  // ─── March 21, 2026 ──────────────────────────────────────────────────────
  {
    id: "051-topps-basketball-2526",
    title: "Checklist Added: 2025-26 Topps Basketball",
    date: "2026-03-21T16:00:00Z",
    summary: "2025-26 Topps Basketball (Flagship) is now live — the full NBA set including Base, Stars of the NBA, All-Rookie Team, and all autograph sub-sets.",
    description: `## 2025-26 Topps Basketball

The complete checklist for 2025-26 Topps Basketball (Flagship tier) is now live.

## Coverage

Full set with all insert sets and parallels, including:

- Base Set (complete roster)
- Stars of the NBA
- All-Rookie Team
- Flagship Real Ones Autographs (with all numbered parallels)
- 1980-81 Topps Basketball (retro insert)
- Rookie Photo Shoot Autographs
- Rookie Photo Shoot Dual Autographs
- And more

## Release Date

October 23, 2025`,
    tags: ["checklist"],
    setId: 31,
  },
  // ─── March 20, 2026 ──────────────────────────────────────────────────────
  {
    id: "046-hobby-jumbo-toggle",
    title: "Feature: Hobby/Jumbo Toggle in Break Hit Calculator",
    date: "2026-03-20T14:00:00Z",
    summary: "The Break Hit Calculator now supports a hobby/jumbo toggle when a set has separate odds for each format, showing side-by-side expected hit rates.",
    description: `## Hobby/Jumbo Toggle

The Break Hit Calculator now supports sets that have separate pack odds for hobby and jumbo boxes.

## How It Works

When a set's pack odds are stored in nested hobby/jumbo format, a toggle appears at the top of the calculator. Switching between the two updates all expected hit rates and slot counts simultaneously.

Sets currently supporting the toggle:
- 2025-26 Topps Basketball
- 2026 Topps Series 1 Baseball

## Implementation

Pack odds stored as nested \`{ "hobby": {...}, "jumbo": {...} }\` automatically activate the toggle. Flat odds sets continue to work as before.`,
    tags: ["feature"],
  },
  // ─── March 19, 2026 ──────────────────────────────────────────────────────
  {
    id: "041-chrome-ufc-hopefuls-2024",
    title: "Checklist Added: 2024 Topps Chrome U.S. Olympic & Paralympic Team Hopefuls",
    date: "2026-03-19T16:00:00Z",
    summary: "The 2024 Topps Chrome U.S. Olympic & Paralympic Team Hopefuls checklist is now live on Checklist2.",
    description: `## 2024 Topps Chrome U.S. Olympic & Paralympic Team Hopefuls

Chrome-tier set tracking U.S. Olympic and Paralympic hopefuls ahead of the Paris 2024 Games. Full checklist now live.`,
    tags: ["checklist"],
    setId: 29,
  },
  {
    id: "050-olympic-hopefuls-2024",
    title: "Checklist Added: 2024 Topps Chrome U.S. Olympic & Paralympic Team Hopefuls",
    date: "2026-03-19T14:30:00Z",
    summary: "2024 Topps Chrome U.S. Olympic & Paralympic Team Hopefuls is now live, covering the full checklist of U.S. hopefuls across all Olympic disciplines.",
    description: `## 2024 Topps Chrome U.S. Olympic & Paralympic Team Hopefuls

The complete checklist for 2024 Topps Chrome U.S. Olympic & Paralympic Team Hopefuls is now live.

This Chrome-tier set covers athletes across the full spectrum of U.S. Olympic and Paralympic sports ahead of the 2024 Paris Games.`,
    tags: ["checklist"],
    setId: 29,
  },
  {
    id: "039-chrome-ufc-2025-odds",
    title: "Pack Odds Added: 2025 Topps Chrome UFC",
    date: "2026-03-19T12:30:00Z",
    summary: "Pack odds are now live for 2025 Topps Chrome UFC, covering all refractor parallels and autograph tiers.",
    description: `## Pack Odds: 2025 Topps Chrome UFC

Full pack odds are now configured for 2025 Topps Chrome UFC. All refractor parallels and autograph tiers are covered.`,
    tags: ["odds"],
    setId: 28,
  },
  {
    id: "040-chrome-ufc-2025-box",
    title: "Box Config Added: 2025 Topps Chrome UFC",
    date: "2026-03-19T12:00:00Z",
    summary: "Box configuration has been added for 2025 Topps Chrome UFC, enabling break hit calculations for this Chrome-tier MMA set.",
    description: `## Box Config: 2025 Topps Chrome UFC

Break format details are now configured for 2025 Topps Chrome UFC, enabling the Break Hit Calculator for this set.`,
    tags: ["box-config"],
    setId: 28,
  },
  {
    id: "049-chrome-ufc-2025",
    title: "Checklist Added: 2025 Topps Chrome UFC",
    date: "2026-03-19T11:00:00Z",
    summary: "2025 Topps Chrome UFC is now live — a Chrome-tier MMA set covering the full UFC roster with refractor parallels.",
    description: `## 2025 Topps Chrome UFC

The complete checklist for 2025 Topps Chrome UFC is now live.

Chrome-tier UFC set featuring the full active roster with the standard Topps Chrome refractor parallel structure.`,
    tags: ["checklist"],
    setId: 28,
  },
  // ─── March 18, 2026 ──────────────────────────────────────────────────────
  {
    id: "048-heritage-baseball-2026",
    title: "Checklist Added: 2026 Topps Heritage Baseball",
    date: "2026-03-18T14:00:00Z",
    summary: "2026 Topps Heritage Baseball is now live, bringing the retro design set's complete checklist to the platform.",
    description: `## 2026 Topps Heritage Baseball

The complete checklist for 2026 Topps Heritage Baseball is now live.

The Heritage set pays homage to classic Topps designs. This Standard-tier set covers the full MLB roster with the vintage aesthetic parallels and short prints characteristic of the Heritage line.`,
    tags: ["checklist"],
    setId: 27,
  },
  {
    id: "038-panini-select-ufc-2022",
    title: "Checklist Added: 2022 Panini Select UFC",
    date: "2026-03-18T12:30:00Z",
    summary: "2022 Panini Select UFC is now live — expanding Checklist2's MMA coverage beyond Topps to include Panini's UFC offering.",
    description: `## 2022 Panini Select UFC

The checklist for 2022 Panini Select UFC is now live. This is the first non-Topps set on Checklist2, expanding coverage to include Panini's premium UFC offering from the 2022 season.`,
    tags: ["checklist"],
    setId: 22,
  },
  {
    id: "037-chrome-sapphire-formula1",
    title: "Checklist Added: 2025 Topps Chrome Sapphire Formula 1",
    date: "2026-03-18T11:00:00Z",
    summary: "2025 Topps Chrome Sapphire Formula 1 is now live — a premium Sapphire-tier F1 set covering the full 2025 grid.",
    description: `## 2025 Topps Chrome Sapphire Formula 1

The Sapphire-tier Chrome set for Formula 1 is now live. Coverage spans the full 2025 F1 grid with the exclusive Sapphire refractor parallel structure unique to this premium product.`,
    tags: ["checklist"],
    setId: 21,
  },
  {
    id: "018-chrome-premier-league-2026",
    title: "Checklist Added: 2026 Topps Chrome Premier League",
    date: "2026-03-18T10:00:00Z",
    summary: "2026 Topps Chrome Premier League is now live — Chrome-tier soccer coverage for the 2025-26 Premier League season.",
    description: `## 2026 Topps Chrome Premier League

The full checklist for 2026 Topps Chrome Premier League (2025-26 season) is now live. Chrome-tier with standard refractor parallels across all cards.`,
    tags: ["checklist"],
    setId: 13,
  },
  // ─── March 17, 2026 ──────────────────────────────────────────────────────
  {
    id: "044-topps-sets-page",
    title: "Feature: Topps Sets Coverage Page",
    date: "2026-03-17T13:00:00Z",
    summary: "A dedicated Topps Sets Coverage page at /sets/topps now shows the full Topps catalog organized by year and sport with checklist/config/odds status indicators.",
    description: `## Topps Sets Coverage

A new page at /sets/topps provides a comprehensive view of the entire Topps catalog tracked on Checklist2.

## Features

- Sets organized by year, then by sport
- Three status pills per set:
  - **Checklist**: whether the full card list is in the database
  - **Box Config**: whether break format details are configured
  - **Odds**: whether pack odds are available for the Break Hit Calculator
- Collapsible year sections
- Sport filter tabs`,
    tags: ["feature"],
  },
  // ─── March 16, 2026 ──────────────────────────────────────────────────────
  {
    id: "022-royalty-ufc-odds",
    title: "Pack Odds Added: 2025 Topps Royalty UFC",
    date: "2026-03-16T15:20:00Z",
    summary: "Pack odds are now live for 2025 Topps Royalty UFC.",
    description: `## Pack Odds: 2025 Topps Royalty UFC

Full pack odds have been configured for 2025 Topps Royalty UFC.`,
    tags: ["odds"],
    setId: 14,
  },
  {
    id: "021-royalty-ufc-box",
    title: "Box Config Added: 2025 Topps Royalty UFC",
    date: "2026-03-16T15:00:00Z",
    summary: "Box configuration has been added for 2025 Topps Royalty UFC.",
    description: `## Box Config: 2025 Topps Royalty UFC

Break format details are now configured for 2025 Topps Royalty UFC, enabling break hit calculations for this premium MMA product.`,
    tags: ["box-config"],
    setId: 14,
  },
  {
    id: "033-series1-baseball-odds",
    title: "Pack Odds Added: 2026 Topps Series 1 Baseball",
    date: "2026-03-16T13:20:00Z",
    summary: "Pack odds are now live for 2026 Topps Series 1 Baseball in both hobby and jumbo formats.",
    description: `## Pack Odds: 2026 Topps Series 1 Baseball

Full hobby and jumbo pack odds are now configured for 2026 Topps Series 1 Baseball. The Break Hit Calculator's hobby/jumbo toggle is active for this set.`,
    tags: ["odds"],
    setId: 18,
  },
  {
    id: "034-series1-baseball-box",
    title: "Box Config Added: 2026 Topps Series 1 Baseball",
    date: "2026-03-16T13:00:00Z",
    summary: "Box configuration is now set for 2026 Topps Series 1 Baseball in hobby and jumbo formats.",
    description: `## Box Config: 2026 Topps Series 1 Baseball

Break format details have been configured for 2026 Topps Series 1 Baseball in both hobby and jumbo formats, enabling the Break Hit Calculator with the hobby/jumbo toggle.`,
    tags: ["box-config"],
    setId: 18,
  },
  {
    id: "028-chrome-sapphire-basketball-odds",
    title: "Pack Odds Added: 2025-26 Topps Chrome Sapphire Basketball",
    date: "2026-03-16T11:20:00Z",
    summary: "Pack odds are now live for 2025-26 Topps Chrome Sapphire Basketball.",
    description: `## Pack Odds: 2025-26 Topps Chrome Sapphire Basketball

Full pack odds are configured for 2025-26 Topps Chrome Sapphire Basketball. All numbered parallel tiers are covered.`,
    tags: ["odds"],
    setId: 26,
  },
  {
    id: "029-chrome-sapphire-basketball-box",
    title: "Box Config Added: 2025-26 Topps Chrome Sapphire Basketball",
    date: "2026-03-16T11:00:00Z",
    summary: "Box configuration has been added for 2025-26 Topps Chrome Sapphire Basketball.",
    description: `## Box Config: 2025-26 Topps Chrome Sapphire Basketball

Break format details are now configured for 2025-26 Topps Chrome Sapphire Basketball, enabling break hit calculations for this premium product.`,
    tags: ["box-config"],
    setId: 26,
  },
  {
    id: "025-finest-basketball-odds",
    title: "Pack Odds Added: 2025-26 Topps Finest Basketball",
    date: "2026-03-16T10:20:00Z",
    summary: "Pack odds are now live for 2025-26 Topps Finest Basketball covering all refractor parallels and autograph tiers.",
    description: `## Pack Odds: 2025-26 Topps Finest Basketball

Full pack odds are configured for 2025-26 Topps Finest Basketball. All refractor parallels and autograph sets are covered.`,
    tags: ["odds"],
    setId: 25,
  },
  {
    id: "026-finest-basketball-box",
    title: "Box Config Added: 2025-26 Topps Finest Basketball",
    date: "2026-03-16T10:00:00Z",
    summary: "Box configuration has been added for 2025-26 Topps Finest Basketball.",
    description: `## Box Config: 2025-26 Topps Finest Basketball

Break format details are now configured for 2025-26 Topps Finest Basketball, enabling the Break Hit Calculator for this Premium-tier Chrome set.`,
    tags: ["box-config"],
    setId: 25,
  },
  // ─── March 15, 2026 ──────────────────────────────────────────────────────
  {
    id: "047-terms-privacy",
    title: "Terms of Use & Privacy Policy Pages Added",
    date: "2026-03-15T15:00:00Z",
    summary: "Terms of Use and Privacy Policy pages are now live at /terms and /privacy.",
    description: `## Legal Pages

Terms of Use (/terms) and Privacy Policy (/privacy) pages are now live.

These pages cover how Checklist2 handles data, what the platform's terms of use are, and user rights regarding any information collected through the site.`,
    tags: ["announcement"],
  },
  {
    id: "045-resources-section",
    title: "Resources Section Launched",
    date: "2026-03-15T11:00:00Z",
    summary: "The Resources section is live at /resources with three guides: Glossary, Break Hit Calculator explainer, and Break Sheet Builder explainer.",
    description: `## Resources

The Resources section (/resources) is now live with three detailed guides:

## Glossary (/resources/glossary)

Definitions for every term and data point used across the app — from print runs to box configs to pack odds.

## Break Hit Calculator Guide (/resources/break-hit-calculator)

Explains how the calculator works, what it means for your breaks, and how to interpret the expected hit rates.

## Break Sheet Builder Guide (/resources/break-sheet-builder)

Documents how the Break Sheet Builder generates Whatnot-ready CSVs, what each column contains, and how to use the output in your streams.`,
    tags: ["feature"],
  },
  // ─── March 14, 2026 ──────────────────────────────────────────────────────
  {
    id: "043-overview-page",
    title: "Feature: Overview Stats Page",
    date: "2026-03-14T17:00:00Z",
    summary: "The Overview page at /overview shows aggregate stats across the entire Checklist2 database — total sets, players, cards, and more.",
    description: `## Overview Stats

The /overview page provides a high-level summary of everything in the Checklist2 database:

- Total sets seeded
- Total players tracked
- Total card appearances
- Breakdown by sport and tier
- Recently added sets`,
    tags: ["feature"],
  },
  {
    id: "042-analytics-page",
    title: "Feature: Analytics / Searches Page",
    date: "2026-03-14T14:30:00Z",
    summary: "The Searches page at /admin/analytics tracks what players and sets users are looking up most, showing search trends across the platform.",
    description: `## Analytics — Top Searches

The /admin/analytics page is now live, showing search trends across the platform.

## What's Tracked

- Top player searches by volume
- Top set views
- Search trends over time (1h, 24h, 7d, 30d time range selector)

This helps identify which players are hot right now and which sets are getting the most interest.`,
    tags: ["feature"],
  },
  {
    id: "020-winter-olympics-2026",
    title: "Checklist Added: 2026 Topps Chrome U.S. Winter Olympics",
    date: "2026-03-14T11:30:00Z",
    summary: "2026 Topps Chrome U.S. Winter Olympics & Paralympic Team Hopefuls is now live, covering U.S. athletes heading to the 2026 Milan-Cortina Games.",
    description: `## 2026 Topps Chrome U.S. Winter Olympics & Paralympic Team Hopefuls

The full checklist is now live for this Chrome-tier Olympics set covering U.S. hopefuls for the 2026 Milan-Cortina Winter Games.`,
    tags: ["checklist"],
    setId: 15,
  },
  {
    id: "019-royalty-ufc-2025",
    title: "Checklist Added: 2025 Topps Royalty UFC",
    date: "2026-03-14T10:00:00Z",
    summary: "2025 Topps Royalty UFC is now live — a Premium-tier MMA set featuring a curated checklist of top UFC fighters with on-card autographs.",
    description: `## 2025 Topps Royalty UFC

The checklist for 2025 Topps Royalty UFC is now live. Royalty is a Premium-tier product focused on top-tier UFC talent with premium on-card autograph content.`,
    tags: ["checklist"],
    setId: 14,
  },
  // ─── March 13, 2026 ──────────────────────────────────────────────────────
  {
    id: "035-series1-baseball-2026",
    title: "Checklist Added: 2026 Topps Series 1 Baseball",
    date: "2026-03-13T18:30:00Z",
    summary: "2026 Topps Series 1 Baseball is now live — the flagship MLB set with the full roster, short prints, and all insert configurations.",
    description: `## 2026 Topps Series 1 Baseball

The flagship Topps baseball set for 2026 is now live. Series 1 covers the full MLB roster with base cards, short prints, and all flagship insert sets.`,
    tags: ["checklist"],
    setId: 18,
  },
  {
    id: "036-universe-wwe-2025",
    title: "Checklist Added: 2025 Topps Universe WWE",
    date: "2026-03-13T17:15:00Z",
    summary: "2025 Topps Universe WWE is now live, bringing professional wrestling coverage to the Checklist2 platform.",
    description: `## 2025 Topps Universe WWE

The full checklist for 2025 Topps Universe WWE is now live. This is Checklist2's first wrestling set, expanding coverage from MMA/UFC into professional wrestling.`,
    tags: ["checklist"],
    setId: 20,
  },
  {
    id: "030-chrome-sapphire-basketball",
    title: "Checklist Added: 2025-26 Topps Chrome Sapphire Basketball",
    date: "2026-03-13T16:00:00Z",
    summary: "2025-26 Topps Chrome Sapphire Basketball is now live — the premium Sapphire-tier version of Chrome NBA, numbered throughout.",
    description: `## 2025-26 Topps Chrome Sapphire Basketball

The Sapphire-tier Chrome set for NBA basketball is now live. All cards in this premium product are numbered, with the Sapphire refractor as the base parallel.`,
    tags: ["checklist"],
    setId: 26,
  },
  {
    id: "027-finest-basketball-2526",
    title: "Checklist Added: 2025-26 Topps Finest Basketball",
    date: "2026-03-13T15:00:00Z",
    summary: "2025-26 Topps Finest Basketball is now live — a Premium-tier Chrome set featuring the full NBA roster with Finest's signature refractor parallels.",
    description: `## 2025-26 Topps Finest Basketball

The full checklist for 2025-26 Topps Finest Basketball is now live. Finest is a Premium-tier Chrome product featuring refractor-based parallels across all inserts.`,
    tags: ["checklist"],
    setId: 25,
  },
  {
    id: "024-midnight-basketball-2526",
    title: "Checklist Added: 2025-26 Topps Midnight Basketball",
    date: "2026-03-13T14:00:00Z",
    summary: "2025-26 Topps Midnight Basketball is now live — a Standard-tier NBA set with Midnight's distinctive dark foil aesthetic.",
    description: `## 2025-26 Topps Midnight Basketball

The checklist for 2025-26 Topps Midnight Basketball is now live. Midnight is a Standard-tier product featuring dark foil aesthetics across base and parallels.`,
    tags: ["checklist"],
    setId: 24,
  },
  {
    id: "023-cactus-jack-basketball",
    title: "Checklist Added: 2025-26 Topps Chrome Cactus Jack Basketball",
    date: "2026-03-13T13:00:00Z",
    summary: "2025-26 Topps Chrome Cactus Jack Basketball is now live — the Travis Scott collaboration Chrome set featuring unique Cactus Jack-themed parallels.",
    description: `## 2025-26 Topps Chrome Cactus Jack Basketball

The full checklist for 2025-26 Topps Chrome Cactus Jack Basketball is now live. This Chrome-tier collaboration set features Cactus Jack (Travis Scott) themed design elements and unique parallel colorways not found in standard Chrome.`,
    tags: ["checklist"],
    setId: 23,
  },
  {
    id: "016-mcdonald-allamerican-2025",
    title: "Checklist Added: 2025 Topps Chrome McDonald's All-American",
    date: "2026-03-13T11:45:00Z",
    summary: "2025 Topps Chrome McDonald's All-American is now live, covering the top high school basketball prospects from the 2025 game.",
    description: `## 2025 Topps Chrome McDonald's All-American

The checklist for 2025 Topps Chrome McDonald's All-American is now live. This Chrome-tier set covers the elite high school basketball prospects who participated in the 2025 McDonald's All-American Game.`,
    tags: ["checklist"],
    setId: 39,
  },
  {
    id: "015-chrome-basketball-2526",
    title: "Checklist Added: 2025-26 Topps Chrome Basketball",
    date: "2026-03-13T11:00:00Z",
    summary: "2025-26 Topps Chrome Basketball is now live — Chrome-tier NBA coverage with the full roster and refractor parallels.",
    description: `## 2025-26 Topps Chrome Basketball

The full checklist for 2025-26 Topps Chrome Basketball is now live. Chrome-tier with standard refractor parallels across the full NBA roster.`,
    tags: ["checklist"],
  },
  {
    id: "017-bowmans-best-2025",
    title: "Checklist Added: 2025 Bowman's Best Baseball",
    date: "2026-03-13T10:00:00Z",
    summary: "2025 Bowman's Best Baseball is now live — a Premium-tier baseball product featuring MLB prospects and veterans with on-card autographs.",
    description: `## 2025 Bowman's Best Baseball

The full checklist for 2025 Bowman's Best Baseball is now live. Bowman's Best is a Premium-tier product featuring both MLB prospects and veterans with on-card autograph content.`,
    tags: ["checklist"],
    setId: 12,
  },
  // ─── March 12, 2026 ──────────────────────────────────────────────────────
  {
    id: "032-break-sheet-builder",
    title: "Feature: Break Sheet Builder Launched",
    date: "2026-03-12T14:30:00Z",
    summary: "The Break Sheet Builder generates Whatnot-ready CSV exports for any set's checklist, formatted for direct import into break streams.",
    description: `## Break Sheet Builder

The Break Sheet Builder is now live, accessible from any set's checklist page.

## What It Does

Generates a Whatnot-compatible CSV file for any card set, structured for direct import into your break stream. Each row represents one slot in the break.

## Columns Included

- Slot number
- Player name
- Team
- Card number
- Insert set
- Rookie status
- Parallel (if applicable)

## How to Use

1. Open any set's checklist
2. Filter to the insert set and parallels you're breaking
3. Click "Build Break Sheet"
4. Download the CSV and import to Whatnot`,
    tags: ["feature"],
  },
  {
    id: "031-pack-odds-page",
    title: "Feature: Pack Odds Page Launched",
    date: "2026-03-12T10:30:00Z",
    summary: "Each set now has a dedicated Pack Odds page showing the pull rate for every card type, powering the Break Hit Calculator.",
    description: `## Pack Odds Page

Every set with odds data now has a dedicated /sets/[id]/odds page showing the full odds table.

## What's Shown

- Card type (insert set + parallel)
- Pack odds denominator (1-in-X)
- Expected hits per hobby box
- Expected hits per jumbo box (where applicable)

The odds data also powers the Break Hit Calculator — no separate setup needed.`,
    tags: ["feature"],
  },
  // ─── March 11, 2026 ──────────────────────────────────────────────────────
  {
    id: "014-athlete-leaderboard",
    title: "Feature: Athlete Leaderboard Launched",
    date: "2026-03-11T15:30:00Z",
    summary: "The Players page now ranks athletes by checklist presence — most unique cards, highest total print run, and most 1-of-1s across all sets.",
    description: `## Athlete Leaderboard

The /players page ranks every athlete in the database by their checklist footprint across all seeded sets.

## Metrics

- **Unique Cards**: total number of distinct card variants (base + all numbered parallels)
- **Total Print Run**: sum of all numbered parallel print runs
- **One-of-Ones**: count of /1 cards
- **Insert Sets**: number of distinct insert sets the player appears in

## Filters

- Filter by sport
- Filter by rookie/veteran status
- Search by player name

Individual player pages at /players/[id] show the full breakdown by set.`,
    tags: ["feature"],
  },
  {
    id: "013-break-hit-calculator",
    title: "Feature: Break Hit Calculator Launched",
    date: "2026-03-11T11:30:00Z",
    summary: "The Break Hit Calculator uses pack odds to show how many autographs, refractors, and key cards you should expect from any box configuration.",
    description: `## Break Hit Calculator

The Break Hit Calculator is now available on every set page that has pack odds configured.

## How It Works

1. Select a box format (hobby, jumbo, mega, etc.)
2. The calculator multiplies pack odds × (cards per box) to derive expected hit counts
3. Results are grouped by card category: autographs, numbered parallels, base inserts

## Key Stats Shown

- Expected autos per box
- Expected numbered cards per box (by color tier)
- Expected 1/1s per case
- Full odds table sorted by rarity

## Sets Supported

Any set with pack odds configured. As more sets get odds data, the calculator automatically works for them.`,
    tags: ["feature"],
  },
  // ─── March 10, 2026 ──────────────────────────────────────────────────────
  {
    id: "008-light-dark-mode",
    title: "Feature: Light/Dark Mode Toggle",
    date: "2026-03-10T17:30:00Z",
    summary: "Checklist2 now supports light and dark mode with a toggle in the top-right corner. Your preference is saved across sessions.",
    description: `## Light/Dark Mode

Checklist2 now supports both light and dark mode. The toggle is in the top-right corner of every page.

## Implementation Details

- Dark mode is the default
- Preference is saved to localStorage
- A blocking script prevents flash-of-unstyled-content (FOUC) on page load
- Light mode inverts the zinc color scale so the app looks natural in either mode
- Smooth 175ms transitions on color changes (excluding images and video)

Your preference persists across sessions and browser restarts.`,
    tags: ["feature"],
  },
  {
    id: "007-set-detail-pages",
    title: "Feature: Set Detail Pages with Player Search",
    date: "2026-03-10T14:00:00Z",
    summary: "Every seeded set now has a detail page with the full card list, insert set navigation, and player search functionality.",
    description: `## Set Detail Pages

Every set in the database has a full detail page at /sets/[id] with:

## Checklist View

- Full card list organized by insert set
- Toggle between insert sets using the sidebar
- Rookie indicator badges
- Card numbers for every card
- Team names

## Player Search

Search any player name to filter the checklist to only their cards. Results highlight every insert set and parallel the player appears in.

## Break Hit Calculator

For sets with pack odds configured, the calculator is embedded directly on the page.

## Pack Odds Tab

Separate tab showing the full odds table for every card type.`,
    tags: ["feature"],
  },
  {
    id: "006-checklists-page",
    title: "Feature: Checklists Browsing Page",
    date: "2026-03-10T11:00:00Z",
    summary: "The Checklists page at /checklists lets you browse all seeded sets, filter by sport, and search by set name — sorted by most recently added.",
    description: `## Checklists Page

The /checklists page is the main entry point for browsing every set in the database.

## Features

- Card grid showing all sets with sample images
- Sport filter tabs (Basketball, Baseball, Soccer, MMA, etc.)
- Set name search
- Tier badges (Chrome, Sapphire, Premium, Prizm, Standard)
- Sorted newest-first so freshly seeded sets appear at the top
- Rookie indicator showing how many RC players are in each set`,
    tags: ["feature"],
  },
  // ─── March 9, 2026 ───────────────────────────────────────────────────────
  {
    id: "012-midnight-ufc-2024",
    title: "Checklist Added: 2024 Topps Midnight UFC",
    date: "2026-03-09T23:48:00Z",
    summary: "2024 Topps Midnight UFC is now live, rounding out the Midnight MMA coverage alongside the 2025 edition.",
    description: `## 2024 Topps Midnight UFC

The checklist for 2024 Topps Midnight UFC is now live alongside the 2025 edition. Both Midnight UFC products are now fully searchable on Checklist2.`,
    tags: ["checklist"],
    setId: 9,
  },
  {
    id: "011-midnight-ufc-2025",
    title: "Checklist Added: 2025 Topps Midnight UFC",
    date: "2026-03-09T23:30:00Z",
    summary: "2025 Topps Midnight UFC is now live — a Standard-tier MMA set featuring UFC's top fighters with Midnight's signature dark aesthetic.",
    description: `## 2025 Topps Midnight UFC

The checklist for 2025 Topps Midnight UFC is now live. Standard-tier MMA product featuring dark foil aesthetics and the full UFC active roster.`,
    tags: ["checklist"],
    setId: 8,
  },
  {
    id: "010-chrome-mls-2025",
    title: "Checklist Added: 2025 Topps Chrome MLS",
    date: "2026-03-09T23:10:00Z",
    summary: "2025 Topps Chrome MLS is now live — Chrome-tier soccer coverage for Major League Soccer's 2025 season.",
    description: `## 2025 Topps Chrome MLS

The full checklist for 2025 Topps Chrome MLS is now live. Chrome-tier product covering the complete MLS roster for the 2025 season with standard refractor parallels.`,
    tags: ["checklist"],
    setId: 6,
  },
  {
    id: "009-uefa-club-competitions-2526",
    title: "Checklist Added: 2025-26 Topps UEFA Club Competitions",
    date: "2026-03-09T22:50:00Z",
    summary: "2025-26 Topps UEFA Club Competitions is now live — comprehensive coverage of the Champions League, Europa League, and Conference League.",
    description: `## 2025-26 Topps UEFA Club Competitions

The full checklist for 2025-26 Topps UEFA Club Competitions is now live. This set covers all three UEFA club competitions: the Champions League, Europa League, and Conference League.`,
    tags: ["checklist"],
    setId: 36,
  },
  {
    id: "004-initial-launch",
    title: "Checklist2 Launched",
    date: "2026-03-09T22:15:00Z",
    summary: "Checklist2 is live — a sports card set explorer built for collectors and breakers, starting with NBA and expanding across sports.",
    description: `## Checklist2 Is Live

Checklist2 is a sports card checklist platform built for collectors and breakers. The initial launch covers the core infrastructure:

## Stack

- **Next.js 15** (App Router) with React Server Components
- **SQLite** via Drizzle ORM (better-sqlite3)
- **Tailwind CSS** with a custom dark-by-default theme
- Python parsers for converting raw checklists into structured database records

## Initial Data Model

- **Sets** — the parent card set (name, sport, season, league, tier)
- **Insert Sets** — sub-sets within a product (Base Set, autograph sets, inserts)
- **Parallels** — numbered or unlimited variants of each card
- **Players** — athletes scoped to each set
- **Player Appearances** — one row per card, linking player to insert set with card number, team, and rookie status

## What's Available on Day One

- Set detail pages with the full card list
- Player search within any set
- Rookie (RC) highlighting throughout`,
    tags: ["announcement", "feature"],
  },
];

export function getUpdateById(id: string): Update | undefined {
  return updates.find((u) => u.id === id);
}

export function getAdjacentUpdates(id: string): { prev: Update | null; next: Update | null } {
  const idx = updates.findIndex((u) => u.id === id);
  return {
    prev: idx > 0 ? updates[idx - 1] : null,         // newer
    next: idx < updates.length - 1 ? updates[idx + 1] : null, // older
  };
}
