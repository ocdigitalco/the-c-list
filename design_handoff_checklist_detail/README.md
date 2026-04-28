# Handoff: Set Detail Page — Option D (web + mobile)

## Overview

This bundle is the design spec for the **Set Detail page** at `/sets/[set-slug]` (e.g. `/sets/2025-topps-chrome-football`). Users hit this page to:

1. Search for an athlete in the set's checklist
2. Get high-level information about the set (release, brand, totals)
3. Drill into granular box configuration and per-format pack odds

It is one of the most-trafficked pages on Checklist². The design replaces the current three-column layout with a hybrid: a **persistent left athlete rail** (what users love about the current page) combined with a **wide right column** containing the hero, full-width 6-stat ticker, and primary tabs (Box Config / Pack Odds / Inserts / Autographs).

---

## About the design files

The files in `reference/` are **design references created in HTML/React (Babel-in-the-browser)** — prototypes showing intended look and behavior, not production code to copy directly. The task is to **recreate this design in the existing Checklist² codebase** using its established patterns, components, fonts, and data layer. If the existing route already has a working data fetcher and athlete-list component, reuse them — only the page layout, hero, stat strip, tab system, drawer, and the per-tab tables/cards are changing.

Open `reference.html` in any modern browser to see the desktop and both mobile states (drawer closed + drawer open) side by side.

---

## Fidelity

**High-fidelity.** Colors, typography, spacing, border-radius values, and exact copy in the prototype are intentional and should be matched. Use the prototype as the source of truth for visual values; use your existing data layer for content.

---

## Screens / Views

There are two delivered screens, plus one drawer state:

### 1. Web — Set Detail (1280px design width)

**Source:** `reference/checklist-detail-D.jsx` (function `OptionD`)

**Layout:** Outer 2-column grid, **`grid-template-columns: 300px 1fr`**, full height, 1px solid `#EDEAE0` divider between columns.

#### Left column — Athletes rail (300px)
Persistent, runs top-to-bottom of the page. Background `#FFFFFF`, padding `22px 18px`. Contains, in order:

- **Heading** "Athletes in Set" — Inter Tight 600, 15px, letter-spacing −0.2, margin-bottom 12px
- **Search field** — `#F1EFE9` background, 8px radius, `7px 10px` padding, search icon + placeholder "Search athletes…", input is borderless and inherits font (13px)
- **Filter chips** — `Total Cards / Autographs / Inserts / Numbered`. Active chip is `#0F0F0E` bg, `#FAFAF7` text; inactive is transparent bg with 1px `#E6E3D9` border, `#3A372F` text. 4px radius, `4px 9px` padding, 11px medium.
- **"Rookies only" checkbox** — 11px, color `#3A372F`, `accent-color: #0F0F0E`
- **Column header row** — `ATHLETE` / `TOTAL CARDS`, JetBrains Mono 9px 600, letter-spacing 1.6, color `#8A8677`, 1px bottom border
- **Athlete rows** (one per athlete in `window.ATHLETES`):
  - Rank number — Mono 11px, color `#8A8677`, fixed 18px width
  - 30×30 avatar circle, bg `#EAE6D9`, fallback is the athlete's initials in `#6B6757`
  - Name + optional `RC` badge (background `oklch(0.55 0.17 25)`, color `#FFF8F1`, 8px 700, 0.6 letter-spacing, 1×4px padding, 2px radius)
  - Team (11px, `#6B6757`)
  - Total cards count (Mono 13px 600)
  - 1px `#F4F1E8` bottom border between rows

#### Right column — Hero / stats / tabs / content
Stacks vertically:

##### Hero (`#FFFFFF`, padding `30px 36px`, 1px bottom border `#EDEAE0`)
3-col grid: `140px 1fr 280px`, 32px gap, items center.

- **Featured card** (left) — 122×172px, rotated −3°, gradient bg `linear-gradient(150deg, #C2102E 0%, #6B0A1B 100%)`, shadow `0 12px 28px rgba(15,15,14,0.18)`. In production, render the actual featured card image; the gradient is a placeholder.
- **Title block** (middle):
  - Eyebrow: "NFL · TOPPS · CHROME · APRIL 15, 2026" — Mono 10px 600, letter-spacing 2.4, color `#8A8677`
  - Title: set name — Inter Tight 600, 42px, letter-spacing −1.2, line-height 1.02, color `#0F0F0E`, margin `8px 0 12px`
  - Chips row: sport, league, brand (use the existing `Chip` component; brand chip is the dark variant) + " 547 athletes tracked" inline copy at 12px `#6B6757`
- **Coverage card** (right) — `#FAFAF7` bg, 1px `#EDEAE0` border, 8px radius, padding `12px 14px`:
  - Header row with "COVERAGE" label (Mono 9px) and `↓ BREAK SHEET` button (`#0F0F0E` bg, `#FAFAF7` text, 4px radius, 10px 600, `5px 10px` padding)
  - 4 status rows (Athlete Checklist / Numbered Parallels / Box Configuration / Pack Odds), each shows label + 8×8 status dot. Dot is `#0E8A4F` when present, `#B7B2A3` when missing. Source of truth is the same coverage signals already used on the Sets Coverage admin page.

##### Stat strip (`#FFFFFF`, 1px bottom border `#EDEAE0`)
6-column grid, equal widths, 1px right divider between cells (none on last). Each cell:
- Padding `18px 22px`
- Label — Mono 9px 600, letter-spacing 1.6, color `#8A8677`, e.g. "CARDS"
- Value — Inter Tight 600, 26px, letter-spacing −0.6, color `#0F0F0E`, margin-top 4px

Stats (in order): `Cards`, `Card Types`, `Parallel Types`, `Autographs`, `Auto Parallels`, `Total Parallels`. All numbers are formatted with thousands separators.

##### Primary tabs (`#FAFAF7`, padding `0 36px`, 1px bottom border `#EDEAE0`)
Underlined-tab pattern. Tabs: `Box Config`, `Pack Odds`, `Inserts`, `Autographs`. Active tab gets a 2px `#0F0F0E` underline (with `margin-bottom: -1px` so it sits on the border), 600 weight, color `#0F0F0E`. Inactive is 500, color `#8A8677`. Padding `14px 20px`.

##### Content area (padding `28px 36px 60px`)
Renders the active tab. See Per-tab spec below.

---

### 2. Mobile — Set Detail (402×874, iPhone)

**Source:** `reference/checklist-detail-D-mobile.jsx` (function `OptionDMobile`)

Top-level container has `padding-top: 54px` to account for the iOS status bar / dynamic island.

- **Sticky app bar** (`top: 54px`, `z-index: 10`, `rgba(250,250,247,0.92)` + 12px backdrop-blur, 1px bottom border `#EDEAE0`, padding `12px 16px`):
  - **Athletes button** (left): white bg, 1px `#E6E3D9` border, 8px radius, 12px 500. Icon = two-people glyph. Label "Athletes · {athleteCount}" (count in `#8A8677`). **Tapping this opens the athletes drawer.**
  - Spacer
  - **Break Sheet button** (right): `#0F0F0E` bg, `#FAFAF7` text, 8px radius, 12px 600

- **Hero** (`#FFFFFF`, padding `18px 16px 14px`, 1px bottom border): 78×108 featured card on the left (rotated −3°), title block on the right. Set title is Inter Tight 600 24px, letter-spacing −0.6. Smaller eyebrow + chips row with a "547 athletes" inline count.

- **Stat grid** (`#FFFFFF`, 1px bottom border): 3×2 grid, same labels/values as web, but value is 20px and label is 8px. 1px dividers between columns; 1px divider on the bottom edge of the first row only.

- **Sticky tabs** (`top: 95px`, padding `0 16px`, `#FAFAF7` bg, 1px bottom border, horizontal scroll). Same underlined-tab pattern. Padding per tab `12px 14px`.

- **Content** (padding 16px). Per-tab content adapts as described below.

---

### 3. Mobile — Athletes drawer (full overlay)

**State:** `drawerOpen === true` in `OptionDMobile`. Rendered as a `position: absolute; inset: 0; z-index: 100` div over the entire phone viewport (the user explicitly asked for full width × full height).

- `padding-top: 54px` to keep the status bar visible
- Drawer header (`#FFFFFF`, 1px bottom border): close button (X icon) + "Athletes in Set" title (Inter Tight 17px 600, letter-spacing −0.3) + count on the right
- Drawer body (`flex: 1`, `overflow-y: auto`, padding `14px 16px 30px`):
  - Search field (same `#F1EFE9` style as web, 14px input)
  - Filter chips (pill shape, `border-radius: 999px`)
  - "Rookies only" checkbox
  - Column header row + athlete rows (slightly larger touch targets than web — 34px avatars, `padding: 12px 4px`)

Closing the drawer (X tap) returns to the previous tab and scroll position.

---

## Per-tab spec (web + mobile)

### Tab: Box Config

**Web:** Single full-width table.
- Header row (Mono 9px 600 labels, 1px bottom border `#EDEAE0`): `BOX TYPE` (left) / `CARDS/PACK` / `PACKS/BOX` / `BOXES/CASE` / `PACKS/CASE` / `AUTOS/BOX` (all right-aligned)
- Data rows: 13px, `padding: 12px 10px`. Box-type label is Inter 600. Numerics use JetBrains Mono. Empty cells render `—` in `#B7B2A3`.
- Row dividers: 1px `#F4F1E8`.
- **Inline exclusives:** when a box type has exclusive parallels, those notes are rendered in a row directly underneath the data row (italic 12px `#6B6757`), and the data row's bottom border is removed so the note appears as a continuation. The exclusive row's `<td colSpan={6}>` carries the `#F4F1E8` bottom border. Default mapping in the prototype:
  - Hobby → "Exclusive Red, White, and Blue Refractors"
  - Jumbo → "Exclusive Hot Pink and Lime Green X-Fractors"
  - Mega → "Exclusive Pulsar Refractors"
  - **In production, this mapping is per-set and should come from your data, not hard-coded.**

**Mobile:** Each box type becomes its own card.
- Card: `#FFFFFF` bg, 1px `#EDEAE0` border, 10px radius, padding `12px 14px`, 10px gap between cards
- Card title: Inter Tight 15px 600
- 5-column grid of mini stats: tiny Mono 7px label + Mono 14px 600 value. `—` rendered as `#B7B2A3` for null fields.
- Exclusives appear at the bottom of the relevant card, separated by a 1px `#F4F1E8` top border, italic 11px `#6B6757`.

### Tab: Pack Odds

Filter chips for box-type — `Hobby`, `First Day Issue`, `Jumbo`, `Breaker's Delight`, `Sapphire`, `Value`, `Mega`, `Hanger`, `Fanatics`. Default selected: `Hobby`. The data shown is the parallel odds **for the selected box type**.

**Web:** Active chip = `#0F0F0E` bg / `#FAFAF7` text, 6px radius, `7px 12px`, 12px 600. Inactive = `#FFFFFF` bg, 1px `#EDEAE0` border, `#3A372F` text.

Data table:
- Section header (Mono 9px 600, letter-spacing 1.6, `#6B6757`, 1px bottom border `#EDEAE0`): `BASE PARALLELS` (left) / `PACK ODDS` (right) / `PER BOX (20 PACKS)` (right)
- 3-column grid: `1fr 100px 160px`. 13px text. Numerics in JetBrains Mono. Per-box copy in `#6B6757`. Rare parallels (defined by `rare: true` in data) are colored `#9A2B14`.

**Mobile:** Chips become a horizontal-scrolling pill row (`border-radius: 999px`). Rows are flex-row instead of grid: name (flex 1) / odds (Mono 12px 500) / per-box (Mono 11px `#6B6757`, fixed 90px right-aligned).

### Tab: Inserts

Same row pattern as Pack Odds, minus the box-type chips. Header `INSERT / PACK ODDS / PER BOX (20 PACKS)`. No rare-row coloring on this tab in the prototype (insert `rare` flag is unused).

### Tab: Autographs

Adds a `NUMBERED` column between name and odds (e.g. `/499`). Web is a 4-column grid `1fr 70px 100px 160px`. Mobile stacks each card into two flex rows (name + odds on top, numbered + per-box on bottom in `#6B6757`). Rare entries (`rare: true`, e.g. Superfractor Auto) colored `#9A2B14`.

---

## Interactions & behavior

| Surface | Interaction | Behavior |
|---|---|---|
| Web tabs | Click | Set active tab, swap content area. Underline animates 150ms. |
| Web Pack-Odds chips | Click | Set active box type, replace odds table. |
| Web athlete row | Click | Navigate to the existing checklist row destination. **Use the route already wired in the codebase — do not invent a new one.** |
| Web athlete search | Type | Client-side filter on name + team substring. Debounce 100ms. |
| Web filter chips | Click | Switch the rank metric (Total Cards / Autographs / Inserts / Numbered). The athlete list re-sorts and the right-hand count column re-labels. |
| "Rookies only" | Toggle | Filter list to `rookie === true`. |
| Mobile Athletes button | Tap | `drawerOpen = true`. Drawer animates up from the bottom (200ms ease-out) — though the prototype shows an instant overlay; please add the slide-up. |
| Mobile drawer X | Tap | `drawerOpen = false`. Return to previous scroll position. |
| Mobile drawer scrim | n/a | Drawer is full-bleed, so no scrim is needed. |
| ↓ Break Sheet button | Click | Triggers existing PDF/print download flow (already implemented). |

---

## State management

State is local to the page; nothing needs to live in a global store.

- `tab: 'Box Config' | 'Pack Odds' | 'Inserts' | 'Autographs'` (default `'Box Config'`)
- `boxTab: string` (default `'Hobby'`) — only used by Pack Odds
- `athleteFilter: 'Total Cards' | 'Autographs' | 'Inserts' | 'Numbered'` (default `'Total Cards'`)
- `rookiesOnly: boolean` (default `false`)
- `athleteQuery: string` (default `''`)
- `drawerOpen: boolean` (mobile only; default `false`)

Data fetching: use the existing set-detail loader. The shape used by the prototype is in `reference/checklist-detail-data.js` — match the field names where possible:

```
SET_DETAIL: { id, name, sport, league, brand, manufacturer,
              releaseDate, released, athletes, cards, cardTypes,
              parallelTypes, autographs, autoParallels, totalParallels,
              coverage: { athleteChecklist, numberedParallels, boxConfig, packOdds } }
BOX_CONFIG: [{ type, cardsPerPack, packsPerBox, boxesPerCase, packsPerCase, autosPerBox }]
BOX_CONFIG_NOTES: string[]   // legacy flat list — replace with per-box-type mapping
PACK_ODDS_TABS: string[]
BASE_PARALLELS: [{ name, odds, per, rare? }]
INSERTS:        [{ name, odds, per }]
AUTOGRAPHS:     [{ name, odds, per, numbered, rare? }]
ATHLETES:       [{ rank, name, team, pos, rookie, totalCards }]
```

The five coverage signals are derived from existing data exactly as on the Sets Coverage admin page — do not add new boolean columns to your schema.

---

## Design tokens

### Colors
| Token | Value | Use |
|---|---|---|
| `bg/page` | `#FAFAF7` | Page background |
| `bg/surface` | `#FFFFFF` | Cards, hero, stat strip |
| `bg/inset` | `#F1EFE9` | Search field background |
| `bg/coverage-card` | `#FAFAF7` | Coverage card background |
| `text/primary` | `#0F0F0E` | Headings, key numbers |
| `text/body` | `#3A372F` | Body text, chip labels |
| `text/secondary` | `#6B6757` | Captions, per-box copy |
| `text/muted` | `#8A8677` | Mono labels, ranks |
| `text/disabled` | `#B7B2A3` | Empty cells (`—`) |
| `text/rare` | `#9A2B14` | Rare parallel rows |
| `border/default` | `#EDEAE0` | Card borders, dividers |
| `border/subtle` | `#F4F1E8` | Row dividers |
| `border/chip` | `#E6E3D9` | Inactive chip borders |
| `accent/dark` | `#0F0F0E` | Active tab, primary buttons |
| `accent/rookie` | `oklch(0.55 0.17 25)` | RC badge bg |
| `accent/rookie-text` | `#FFF8F1` | RC badge text |
| `status/ok` | `#0E8A4F` | Coverage dot — present |
| `status/missing` | `#B7B2A3` | Coverage dot — missing |
| `card/featured-grad` | `linear-gradient(150deg, #C2102E 0%, #6B0A1B 100%)` | Featured card placeholder |
| `card/featured-shadow` | `0 12px 28px rgba(15,15,14,0.18)` | Featured card |

### Typography
- **Display / titles**: Inter Tight, 600. Sizes 42 / 26 / 24 / 18 / 17 / 15 / 14. Letter-spacing −1.2 / −0.6 / −0.5 / −0.4 / −0.3 / −0.2 / −0.2 respectively.
- **Body / UI**: Inter, 400/500/600. Sizes 13 (default), 12 (caption), 11 (small).
- **Mono labels & numerics**: JetBrains Mono (or `ui-monospace` fallback), 600. Sizes 9 (column headers, eyebrows; letter-spacing 1.6–2.4) / 11 / 13 / 14.

### Spacing scale (px)
2, 4, 6, 8, 10, 12, 14, 16, 18, 22, 24, 28, 30, 32, 36

### Radius
- 4 (chips, buttons)
- 6 (mid)
- 8 (cards, search field, coverage card)
- 10 (mobile cards)
- 999 (mobile pill chips)

### Shadows
- Featured card: `0 12px 28px rgba(15,15,14,0.18)` (web), `0 8px 18px rgba(15,15,14,0.18)` (mobile)
- Phone frame (reference only): see `reference.html`

---

## Files

```
reference.html                               # Open in any browser to preview
reference/checklist-detail-D.jsx             # Web layout — function OptionD
reference/checklist-detail-D-mobile.jsx      # Mobile layout — function OptionDMobile + OptionDMobileOpen (drawer pre-open)
reference/checklist-detail-data.js           # Sample shape — replace with real loader
reference/ui-atoms.jsx                       # Chip, IconSearch, IconChev, IconX, IconSliders helpers
```

---

## Implementation notes

1. **Reuse existing components.** If your codebase already has `Chip`, search input, table, sticky tab strip, status pill — use those, even if their styles differ slightly. Match the design's *values* (sizes, colors, spacing) without duplicating the *components*.
2. **Routing.** Preserve the existing row-click → checklist destination already wired on the live page. The prototype does not implement that link.
3. **Coverage signals.** Derive the five signals (player checklist, pack odds, box config, numbered parallels, release date) from existing data — same pattern as the Sets Coverage admin page. Do not add new boolean columns.
4. **Featured card image.** The prototype uses a red gradient as a placeholder. Render the real `featured_card_image_url` when available; fall back to a tinted placeholder using the team's primary color.
5. **Per-box-type exclusives.** The prototype hard-codes Hobby/Jumbo/Mega exclusives. The real data should carry exclusives keyed by box type so each set's mapping is correct.
6. **Performance.** The athlete rail can be 500+ rows. Virtualize if your existing list does — otherwise plain rendering is fine up to ~1000 rows.
7. **Accessibility.** Tabs should be `role="tab"` inside a `role="tablist"`. The mobile drawer is a `role="dialog"` with focus trapped while open and focus returned to the Athletes button on close. Status dots need `aria-label="Present"`/`"Missing"`.
8. **Responsive.** The web layout is designed for ≥1180px. Below that, treat as mobile. There is no intermediate tablet design — confirm with design before shipping a fluid breakpoint.
