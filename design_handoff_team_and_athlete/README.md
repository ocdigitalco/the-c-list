# Handoff: Team Detail & Athlete Detail

## Overview
Two new detail pages for a sports trading-card checklist application:

- **Team Detail** — A page for any team within a given set. Shows team-level totals (athletes, total cards, numbered parallels, 1/1s) and a flat sortable table of every athlete on that team in the set, with per-athlete totals (Total Cards, Autographs, Inserts, Numbered Parallels). The team page is **new** — no existing route or page structure for it. The data already exists in the application; this work is to build the page structure and map existing data into it.
- **Athlete Detail** — A page for a single athlete inside a set. Shows athlete-level totals, a Break Hit Calculator, the insert sets they appear in (with parallel chips), an autographs table, base parallels, "also featured in" cross-references, and a left-rail of athletes in the same set. This page may already exist in the codebase in some form; the design here is the target end-state.

Both pages share a visual language ("Option D"): light editorial off-white surface (`#FAFAF7`), monospace caption labels in uppercase letterspaced caps, "Inter Tight" headings, and tabular numerics in JetBrains Mono. They are designed as a matched pair so that navigating from a set → team → athlete (or set → athlete) feels like the same product.

## About the Design Files
The files in this bundle are **design references created in HTML** — interactive prototypes showing intended look and behavior, not production code to ship. The task is to **recreate these designs in the target codebase's existing environment** (whatever framework, component library, and routing the app uses) using its established patterns. Lift the **layouts, styles, copy, interaction model, and data shape** from the references; do not necessarily lift the React/JSX structure verbatim — adapt to the host app's component conventions.

If the codebase has no UI yet, React + a CSS-in-JS or utility-CSS approach matching this prototype style is a fine default, but anything that can render the same visuals works.

## Fidelity
**High-fidelity (hifi).** All colors, typography, spacing, border radii, and interaction states are intentional and final. Match them pixel-perfectly, substituting the codebase's existing tokens **only if they already match** (or are within a hair of) the values listed in [Design Tokens](#design-tokens). Otherwise add the values as new tokens.

## Files in This Bundle

```
design_handoff_team_and_athlete/
├── README.md                        ← this file
├── Preview.html                     ← open in a browser to see all four artboards live
└── design/
    ├── team-detail-D.jsx            ← Team Detail · Desktop (1280w)
    ├── team-detail-D-mobile.jsx     ← Team Detail · Mobile (iOS, 402w)
    ├── team-detail-data.js          ← Sample data + data shapes for Team Detail
    ├── athlete-detail-D.jsx         ← Athlete Detail · Desktop (1280w)
    ├── athlete-detail-D-mobile.jsx  ← Athlete Detail · Mobile (iOS, 402w)
    ├── athlete-detail-data.js       ← Sample data + data shapes for Athlete Detail
    ├── ui-atoms.jsx                 ← Shared <Chip>, <IconChev>, <IconSearch>, <IconX>
    └── ios-frame.jsx                ← iOS device chrome used to host mobile artboards
```

`Preview.html` renders all four artboards on one page. Open it directly in a browser (no build step required) to inspect the designs interactively.

## Screens

### 1. Team Detail · Desktop

**Purpose** — Land here from a set's team list. Get team-level totals at a glance, then drill into individual athletes.

**Layout** — `1280px` wide, two-column grid:
- **Left rail** (`300px`, white, `1px solid #EDEAE0` right border): "Athletes in Set" — the athletes on this team, in this set. Searchable, with quick filter chips and a Rookies-only toggle. Same component pattern as the Athlete Detail rail.
- **Right column** (`1fr`):
  1. **Hero** (white, `22px 36px 28px` padding, bottom border): breadcrumb back to the set; then a 3-column grid (`180px 1fr 280px`, `32px gap`) containing the team crest tile, identity block (eyebrow caps · H1 team name · sport/league chips), and a **Roster Summary** panel (key/value pairs).
  2. **Stat strip** (white, 4 equal columns, `18px 22px` padding, `1px` dividers): `ATHLETES`, `TOTAL CARDS`, `NUMBERED PARALLELS`, `1/1S`. Each cell is a mono caption above an `Inter Tight 26/600` value.
  3. **Primary tabs** (off-white `#FAFAF7`, `0 36px` padding, `1px` bottom border): `Overview · Athletes · Inserts · Autographs · Numbered Parallels`. Active tab has a `2px solid #0F0F0E` underline (sitting on the bottom border via `marginBottom: -1`).
  4. **Filter row** (above the table on the Athletes/Overview tabs): "Athletes (N)" title on the left, then a `POSITION` select (`160px` min) and a "Rookies only" checkbox.
  5. **Athletes table** — see below.

**Athletes table** — Flat, sortable.
Columns: `# · ATHLETE · POS · TOTAL CARDS · AUTOGRAPHS · INSERTS · NUMBERED PARALLELS`
Grid template: `32px 2fr 70px 90px 110px 90px 130px`, `12px gap`.
- Header row: off-white `#FAFAF7` background, mono caption labels, click-to-sort. Active sort column shows `▲`/`▼` and turns `#0F0F0E`. Right-aligned columns are also right-aligned in the header.
- Body rows: white background, `1px solid #F4F1E8` bottom border, `14px 18px` padding. Athlete cell is rank → 30px circular initials avatar → name + RC badge (oklch(0.55 0.17 25) on `#FFF8F1`, 9px/700, 1px 5px). Numeric cells are JetBrains Mono; zeros render as `—` in `#B7B2A3`.
- Whole row is a link.

### 2. Team Detail · Mobile (iOS)

**Layout** — Single column, `402px` wide. Sections from top:
1. **App top bar** (sticky, `rgba(250,250,247,0.92)` + `backdrop-filter: blur(12px)`, bottom border): hamburger button labeled "Teams" (opens drawer) + breadcrumb to set.
2. **Hero** (white, `16px 14px 14px`): `96px` crest tile + identity (`Inter Tight 22/600`, `letter-spacing: -0.6`), eyebrow caps, league + Chrome chip.
3. **Stat grid** (white, 4 equal columns): `ATHLETES · CARDS · NUMBERED · 1/1S`. Mono `8/600/1.2ls` caption + `Inter Tight 18/600` value.
4. **Sticky tabs** (off-white, horizontal scroll): same labels as desktop.
5. **Filter row + sort chips**: position select + Rookies toggle, then a `SORT` label and round-pill chips for Total Cards / Autographs / Inserts / Numbered. Active chip is solid `#0F0F0E` with `▲`/`▼`.
6. **Athletes list** (white card, `border: 1px solid #EDEAE0`, `border-radius: 10px`): one row per athlete. Each row is a tap target containing:
   - Header: rank + 32px initials avatar + name + RC badge + `POS · #JERSEY` mono caption.
   - **4-up stat strip** below header (`#FAFAF7` background, `8px` radius, `1px` border, 4 equal columns): `CARDS / AUTOS / INSERTS / NUMBERED`. This replaces the desktop table on mobile.
7. **Drawer** (full-screen overlay when hamburger tapped): "Teams in Set" team switcher with search and team rows (crest, name, total cards, athletes count). Selected team highlighted with left rail.

### 3. Athlete Detail · Desktop

**Layout** — `1280px` wide, two-column grid (same `300px / 1fr` shell as Team Detail).
- **Left rail**: "Athletes in Set" — every athlete in the **set** (cross-team), with rank/avatar/name/RC badge/team/total cards. Search, filter chips, a `TEAM` select dropdown, Rookies-only toggle. The selected athlete is the page subject.
- **Right column**:
  1. **Hero**: breadcrumb · `180px` square photo placeholder · identity (eyebrow caps `POS · #JERSEY · TEAM`, `Inter Tight 38/600` H1, sport/league/Chrome chips, "featured in N sets" lede) · **Team Details** panel (border: `2px solid #F2F0E9`, key/value rows linking out to the team page).
  2. **Stat strip**: `CARD TYPES · TOTAL CARDS · NUMBERED PARALLELS · 1/1S`.
  3. **Tabs**: `Overview · Card Types · Base Parallels · Inserts · Autographs · Also Featured In`.
  4. **Overview tab content**:
     - **Break Hit Calculator** card (`2px solid #151412`): heading + question, "CASES" and "BOXES" steppers, then 3 rows of (color dot · label/sub · odds · per-box) for "Any Card / Numbered Parallel / Autograph". Bottom: mono summary line.
     - **Insert Sets** accordion list — each row is `name · "N cards · M parallels"`. Open row reveals card number badge, subject, team, then a `PARALLELS` heading and pill chips colored by tone (silver/orange/teal/blue/green/black/red/gold).
     - **Autographs** table — grouped flat table. Each set has a header row (`#cardNumber` badge + name + subject + team + "N PARALLELS" caption) followed by parallel rows (name · print run · pack odds · per-box). Rare rows in `#9A2B14`.
  5. **Other tabs**: condensed parallel tables (Base Parallels, Inserts), Also Featured In table (set/brand/year/cards/autos/parallels).

### 4. Athlete Detail · Mobile (iOS)

Same content as desktop, condensed:
- App bar with hamburger labeled "Athletes" → opens drawer with the cross-team athlete list.
- Hero: `96px` photo + identity.
- 4-up stat grid.
- Sticky horizontal-scroll tabs.
- Overview tab: Break Hit Calculator card (flush-stacked above) + Team Details card (flush-stacked below) + Card Types accordion + Autographs grouped table.
- Card Types tab: full-width accordion.
- Inserts/Autographs tabs: grouped flat tables (set header rows + parallel rows).
- Base Parallels tab: condensed table.
- Also Featured In tab: card-style rows with brand · sport · year + 3-stat strip (His Cards / Autos / Parallels).

## Interactions & Behavior

### Team Detail
- **Sortable table columns** — Click any sortable header to toggle sort. Default sort: `totalCards desc`. String columns default to `asc`, numeric to `desc`. Active column shows arrow.
- **Position filter** — `<select>` filters table to athletes matching position. Default `All Positions`.
- **Rookies-only** — Checkbox; only rows with `rookie === true` when active.
- **Tab switch** — Local state. Inserts/Autographs/Numbered Parallels tabs are placeholders with "coming soon" copy in this design — to be filled by separate ticket / future work.
- **Mobile drawer** — Hamburger opens a full-screen overlay listing all teams in the set; tapping a team navigates to that team's page (and closes the drawer). Drawer has its own close button.
- **Row click** — Whole athlete row is a link to that athlete's detail page.

### Athlete Detail
- **Tab switch** — Local state. Each tab swaps the main content region.
- **Accordion (Insert Sets)** — Single-open behavior; clicking a row toggles, clicking another opens it instead.
- **Break Hit Calculator** — `CASES` and `BOXES` steppers (min 1, no max). Numbers in summary line and (in production) odds/per-box rows should recalculate from pack odds × case/box count.
- **Athletes rail filters** — Search, filter chips, Team dropdown, Rookies-only. Filters are visual-only in this prototype; real implementation should filter the rail list.
- **Mobile drawer** — Hamburger opens "Athletes in Set" overlay (same content as desktop rail).

## State Management

### Team Detail
| State | Type | Default | Notes |
|---|---|---|---|
| `tab` | string | `'Athletes'` | One of: `Overview`, `Athletes`, `Inserts`, `Autographs`, `Numbered Parallels` |
| `sort` | `{ key, dir }` | `{ key: 'totalCards', dir: 'desc' }` | `key` ∈ table columns; `dir` ∈ `'asc' \| 'desc'` |
| `position` | string | `'All Positions'` | Derived options from athlete list |
| `rookiesOnly` | boolean | `false` | |
| `drawerOpen` (mobile) | boolean | `false` | |

### Athlete Detail
| State | Type | Default | Notes |
|---|---|---|---|
| `tab` | string | `'Overview'` | One of: `Overview`, `Card Types`, `Base Parallels`, `Inserts`, `Autographs`, `Also Featured In` |
| `openSet` | string \| null | `'Image Variations'` | Currently-open accordion row in Insert Sets |
| `openInsert` | string \| null | `'Power Players'` | (Reserved — for the Inserts tab if it grows accordions) |
| `cases` / `boxes` | number | `1` / `12` | Break Hit Calculator inputs |
| `team` | string | `'All Teams'` | Rail team filter |
| `athleteFilter` | string | `'Total Cards'` | Rail sort/filter chip |
| `drawerOpen` (mobile) | boolean | `false` | |

## Data Shapes

The application already has all the underlying data; this section maps fields from the prototype data files (`team-detail-data.js`, `athlete-detail-data.js`) to what the page consumes. **Use these as field-name targets when wiring queries**, but expect the real backend column names to differ — adapt accordingly.

### Team Detail

```ts
// Subject team in this set
TeamDetail = {
  id: string;
  team: string;            // "New England Patriots"
  teamShort: string;       // "Patriots"
  league: string;          // "NFL"
  sport: string;           // "Football"
  city: string;            // "Foxborough, MA"
  conference: string;      // "AFC East"
  primary: string;         // hex — team primary brand color
  secondary: string;       // hex — team secondary brand color
  setName: string;
  setHref: string;

  // Aggregates across all this team's cards in this set:
  athletes: number;
  totalCards: number;
  numberedParallels: number;
  oneOfOnes: number;
  rookies: number;
  autographs: number;
};

// Per-athlete row for the main flat table
TeamAthleteRow = {
  rank: number;
  name: string;
  position: string;        // "QB", "RB"…
  jersey: number;
  rookie: boolean;
  totalCards: number;
  autographs: number;
  inserts: number;         // count of distinct insert sets the athlete appears in
  numberedParallels: number;
};

// For the mobile "Teams in Set" drawer (and team-switcher dropdowns)
TeamInSet = {
  name: string;
  short: string;
  athletes: number;
  totalCards: number;
};
```

### Athlete Detail

See `design/athlete-detail-data.js` for full sample. Key shapes:

```ts
AthleteDetail = {
  id: string;
  name: string;
  team: string;
  teamShort: string;
  position: string;
  jersey: number;
  rookie: boolean;
  setName: string;
  setHref: string;
  cardTypes: number;
  totalCards: number;
  numberedParallels: number;
  oneOfOnes: number;
  photoUrl?: string;       // optional — placeholder shown if absent
};

InsertSet = {
  name: string;
  kind: 'base' | 'insert' | 'variation';
  cards: number;
  parallels: number;
  expandable: boolean;
  highlight?: boolean;
  details?: {
    cardNumber: string;    // "#10"
    subject: string;
    team: string;
    parallels: { name: string; run: string; tone: ParallelTone }[];
  };
};
ParallelTone = 'silver' | 'orange' | 'teal' | 'blue' | 'green' | 'black' | 'red' | 'gold';

AutographSet = {
  name: string;
  cardNumber: string;
  subject: string;
  team: string;
  parallels: {
    name: string;
    run: string;          // "/199" | "1/1" | "unnumbered"
    odds: string;         // "1:288"
    per: string;          // "1 in ~14.4 boxes"
    rare?: boolean;       // tints row red
  }[];
};

AlsoAppearsInRow = {
  name: string;
  brand: string;
  year: number;
  sport: string;
  cards: number;
  autos: number;
  parallels: number;
};

BreakHitCalcRow = {
  label: string;
  sub: string;
  odds: string;
  perBox: string;
  tone: 'good' | 'medium' | 'low';   // green/amber/red dot
};
```

## Design Tokens

### Colors
| Token | Value | Use |
|---|---|---|
| Surface (page) | `#FAFAF7` | Main page background |
| Surface (card) | `#FFFFFF` | Hero, panels, table body, accordion rows |
| Surface (subtle) | `#F1EFE9` | Search input bg, card-number pill, rail row hover |
| Surface (selected) | `#F4F1E8` | Selected rail row background |
| Border (default) | `#EDEAE0` | Section dividers, panel borders |
| Border (subtle) | `#F4F1E8` | Row separators inside lists/tables |
| Border (input) | `#E6E3D9` | Input/select chrome |
| Border (panel-strong) | `#F2F0E9` | Roster Summary / Team Details panel (`2px`) |
| Border (callout-strong) | `#151412` | Break Hit Calculator card outline (`2px`) |
| Text (primary) | `#0F0F0E` | Headings, primary body |
| Text (secondary) | `#3A372F` | Body, chip labels |
| Text (muted) | `#6B6757` | Lede copy, meta text |
| Text (caption) | `#8A8677` | Mono caption labels |
| Text (placeholder) | `#B7B2A3` | "—" zeros, unnumbered runs |
| Text (placeholder-strong) | `#C4BEAD` | Photo placeholder initials |
| Accent (rookie) | `oklch(0.55 0.17 25)` on `#FFF8F1` | RC badge |
| Status (good) | `#0E8A4F` | Calculator green dot |
| Status (medium) | `#C28A18` | Calculator amber dot |
| Status (low / rare) | `#9A2B14` | Calculator red dot, rare-parallel rows |

### Typography
| Role | Family | Size · Weight · LH · LS |
|---|---|---|
| H1 (hero, desktop) | Inter Tight | `38/600/1.08/-1.0` (`text-wrap: balance`) |
| H1 (hero, mobile) | Inter Tight | `22-24/600/1.05/-0.6` |
| Section heading | Inter Tight | `16-18/600/—/-0.3` |
| Stat value | Inter Tight | `26/600/—/-0.6` (desktop) · `18/600/—/-0.5` (mobile) |
| Body | Inter | `13/500-600` |
| Body small | Inter | `11-12/400-600` |
| Mono caption (uppercase) | JetBrains Mono | `9/600` letter-spacing `1.6` |
| Mono numeric | JetBrains Mono | `11-16/600` |
| Eyebrow caps (above H1) | JetBrains Mono | `10/600/—/2.4` |

Load: `Inter`, `Inter Tight`, `JetBrains Mono` from Google Fonts (weights 400/500/600/700).

### Spacing
- Section padding (desktop hero): `22px 36px 28px`
- Section padding (mobile): `14-16px`
- Stat strip cell padding: `18px 22px` (desktop) · `12px 10px` (mobile)
- Tab padding: `14px 20px` (desktop) · `12px 12px` (mobile)
- Table row padding: `14px 18px` (desktop) · `12px 14px` (mobile)
- Card-number pill: `3px 7px`, radius `3px`
- Chips: `4-5px 9-11px`, radius `4px` (desktop) / `999px` (mobile pill)
- Accordion row padding: `14px 18px`

### Borders & Radii
- Card / panel / accordion: `1px solid #EDEAE0`, radius `8-10px`
- Hero callout (Break Hit Calculator): `2px solid #151412`, no radius
- Roster / Team Details panel: `2px solid #F2F0E9`, no radius
- Active tab underline: `2px solid #0F0F0E`, sits on `1px` bottom border via `margin-bottom: -1`
- Selected rail row: `2px solid #0F0F0E` left rail, `#F4F1E8` background

### Mobile shell
- Sticky app top bar offset: `top: 54px` (below the iOS status bar)
- Sticky tabs offset: `top: 54 + 41 = 95px`
- Drawer paddingTop: `54px`

## Assets
- **Fonts** — Inter, Inter Tight, JetBrains Mono (Google Fonts).
- **Icons** — Inline SVG. Defined in `design/ui-atoms.jsx`: `IconChev` (4 directions), `IconSearch`, `IconX`. The mobile top bars also have inline SVGs for the "Athletes" and "Teams" hamburger glyphs (people / 4-tile grid).
- **Athlete photo** — Placeholder square (`180×180` desktop, `96×96` mobile) with initials. Production should bind to an athlete-photo CDN URL (`AthleteDetail.photoUrl`).
- **Team crest** — Placeholder geometric tile using team `primary`/`secondary` brand hex, with team initials inside. Production should bind to a team-logo URL when available; the placeholder must remain as the fallback.
- **No raster assets** are bundled — every visual is rendered via CSS/SVG.

## Implementation Notes

1. **Build the Team Detail page structure first.** It does not exist yet. Add a route like `/sets/:setId/teams/:teamId` and wire the data already in the application:
   - The team aggregate stats come from existing per-card / per-athlete data — group cards by `setId + teamId`, then count distinct athletes, sum cards, sum numbered parallels (cards where `printRun != null`), count `printRun == 1` for 1/1s.
   - The athletes table comes from the same dataset filtered by team, with each row's columns being aggregates of that athlete's cards in that set.
2. **Reuse existing components where possible.** Both pages use the same primitives (Chip, IconChev, IconSearch, IconX, accordion, sortable table). If the codebase already has a sortable data table, use it — the "flat athletes table" is intentionally minimal and should map to whatever exists.
3. **The `<Chip>` atom** has two tones: `default` (light surface) and `dark` (`#0F0F0E` bg, `#FAFAF7` text). Do not invent more.
4. **The Break Hit Calculator** odds are presented as fixed strings in this prototype. Real implementation should compute them from pack odds × case/box count. Three rows always: Any Card / Numbered Parallel / Autograph.
5. **Mobile breakpoint** — the mobile artboard is `402px` wide (iOS frame). Treat it as the small-screen target. Anything narrower may need additional tuning.
6. **Photo & crest fallbacks must remain.** The placeholder rendering (initials over a tinted background, with a small `PHOTO` / `CREST` mono caption) is the design's declared empty state.
7. **`text-wrap: balance`** on the desktop H1 prevents the team/athlete name from collding with the chip row when it wraps to two lines. Keep it.

## Open Questions for Product

1. **Tabs that aren't designed yet on the Team page** — Inserts, Autographs, Numbered Parallels show "coming soon" placeholders. Are these expected to come in a follow-up, or should they fall back to the Athletes table filtered to athletes-with-N-of-X-type?
2. **Team brand colors** — the prototype uses placeholder primary/secondary hex per team. Confirm the source of truth for team brand color tokens.
3. **Does each team page need a team logo, or is the geometric crest fine indefinitely?**

## Files Used in the Source Project
The original full prototype lives in the project at `Checklist Detail.html` — it composes these designs into a `<DesignCanvas>` with multiple artboards alongside the broader checklist-detail explorations. Bundled here are just the files required to render Team Detail and Athlete Detail.
