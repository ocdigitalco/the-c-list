# Handoff: Sets Coverage — Admin Set Completeness View

## Overview
An **admin-facing** page at `/sets` that shows, at a glance, which card sets are fully ready to function as checklists on the site and which are missing required data. For a set to be considered "complete," it must have all five of:

1. **Player Checklist** — the card-by-card list of athletes
2. **Pack Odds** — pull rates / insertion ratios
3. **Box Configuration** — packs per box, cards per pack, etc.
4. **Numbered Parallels** — the parallel print runs
5. **Release Date** — the official release date

Sets are grouped by year, then by sport, with a compact per-row coverage strip showing exactly which signals are present and which are missing. Both desktop and mobile (iOS) layouts are included.

This page reuses the same visual system as the Checklists page (warm off-white palette, Inter Tight headlines, JetBrains Mono labels). Recreate it inside the production codebase using its existing components and styling.

## About the Design Files
The files in `/design/` are **design references created in HTML** — prototypes showing intended look and behavior, not production code to copy directly. The task is to **recreate these designs in the target codebase's existing environment** (React, Vue, SwiftUI, native, etc.) using its established patterns and libraries.

The HTML prototypes use inline React + Babel for iteration speed. Production should use the codebase's component system, state management, styling solution, and icon library.

## ⚠️ Preserve Existing Row → Checklist Navigation
Each row in both prototypes is a clickable `<a>` that writes the set ID to `localStorage.cl_openId` and navigates to `Checklists.html`. **This linking pattern is a placeholder.**

The production codebase **already wires each set in the coverage view to its corresponding checklist detail screen.** That existing routing — whatever the codebase uses (React Router, Next.js `<Link>`, native navigation stack, etc.) — must be preserved exactly as-is. Do not rip it out, do not replace it with the prototype's `localStorage` hack, and do not introduce a new route table for this.

When you adapt the prototype, the only thing to carry over from the link behavior is **"the whole row is clickable and goes to that set's checklist."** Everything else — the URL, the navigation mechanism, route guards, deep linking — already exists; leave it alone.

## ⚠️ Use Existing Data — Do Not Port the Sample Content
All set names, IDs, dates, and coverage flags in `/design/coverage-data.js` are **placeholder data** fabricated to populate the prototype. They must not ship.

**Do this:**
- Bind every field in the design to the corresponding field already in the production database / API:
  - Set name → existing checklist name
  - Manufacturer (Topps / Panini) → existing manufacturer field
  - Sport category → existing sport field
  - Year → existing release year
  - Release Date → existing release date column
  - Player Checklist coverage → derive from "does this set have a populated player checklist?"
  - Pack Odds coverage → derive from "does this set have pack odds data?"
  - Box Configuration coverage → derive from "does this set have a box config record?"
  - Numbered Parallels coverage → derive from "does this set have parallels defined?"
- Coverage flags should be **computed live** from the existing schema, not stored as new boolean columns.

**Do not do this:**
- Do not use the fictional set names or coverage flags from `coverage-data.js`.
- Do not create new boolean columns (`has_checklist`, `has_pack_odds`, etc.) — these should be derived/computed from the underlying data's existence.
- Do not invent a new `manufacturer` taxonomy if one already exists.

Use `/design/coverage-data.js` only to understand what **types and shapes** of fields the UI needs, and map those onto the real schema.

## Fidelity
**High-fidelity (hifi).** Colors, typography, spacing, corner radii, and interaction states are final. Recreate pixel-perfectly using the codebase's existing libraries and patterns.

---

## Screens

### 1. Sets Coverage (Desktop)

**Purpose:** Admin sees, at a glance, which sets are fully ready to publish as functioning checklists and which are missing required data.

**Layout**
- Centered content column, max-width `1440px`, horizontal padding `56px`, top padding `40px`, bottom padding `80px`.
- Background `#FAFAF7` (warm off-white).
- Vertical stack:
  1. Back breadcrumb ("‹ Home") — `13px`, color `#6B6757`
  2. Page title "Sets Coverage" — `Inter Tight 48/600`, letter-spacing `-1.2px`, color `#0F0F0E`
  3. Subtitle "**N** of **M** sets tracked in the app" — `14px`, color `#6B6757` (numbers in `#0F0F0E` weight 600). N = sets with a complete record; M = total sets in app.
  4. Required Coverage legend strip — top margin `24px`
  5. Manufacturer filter row — top margin `14px`
  6. Sport filter row — top margin `18px`
  7. Year sections — top margin `32px` per section

**Required Coverage legend strip**
- White card, `1px` border `#EDEAE0`, radius `10px`, padding `14px 18px`, gap `24px`, flex-wrap.
- Mono label "REQUIRED COVERAGE" — `JetBrains Mono 10/600`, letter-spacing `2px`, color `#3A372F`.
- Five legend items, each: `6×6px` green dot (`#0E8A4F`) + label (`13px`, color `#3A372F`):
  - Checklist
  - Release Date
  - Parallels
  - Box Config
  - Pack Odds
- Right-aligned: **"Show only incomplete"** toggle button.
  - Inactive: transparent bg, `#3A372F` text, `1px` border `#D9D5C7`, padding `6px 12px`, radius `999px`, `12px/500`.
  - Active: bg `#0F0F0E`, text `#FAFAF7`, prefixed with `✓ `.

**Manufacturer filter chips**
- Pill shape, padding `6px 12px` (inactive) / `6px 14px` (active), radius `999px`.
- Mono label "MANUFACTURER" left of chips — `JetBrains Mono 10/500`, letter-spacing `2px`, color `#8A8677`, width `110px`.
- Three options: **All**, **Topps**, **Panini**.
- Inactive Topps: text `#E11D48`, transparent bg/border.
- Inactive Panini: text `#B47A0F`, transparent bg/border.
- Active **All**: bg `#0F0F0E`, text `#FAFAF7`, border `#0F0F0E`.
- Active **Topps**: text `#E11D48`, transparent bg, `1px` border `#E11D48`.
- Active **Panini**: bg `#F2C230`, text `#1A1916`, `1px` border `#E0B41E`.
- Selecting "All" deactivates the others; selecting Topps or Panini filters the list.

**Sport filter chips**
- Same shape and behavior as on Checklists.
- Inactive: transparent bg, `#3A372F` text, transparent border, `13px/400`.
- Active: bg `#0F0F0E`, text `#FAFAF7`, `1px` border `#0F0F0E`, `13px/500`.
- Hover (inactive): bg `#F1EFE9`.
- Categories (in order): All, Basketball, Baseball, Soccer, MMA, Wrestling, Racing, Football, Entertainment, Other.
- Use the same canonical sport list as Checklists; do not invent a separate taxonomy.

**Year section**
- Header: full-width `<button>` row, padding `10px 0`, bottom border `1px #EDEAE0`.
  - Caret icon (`12×12`, `#3A372F`, `1.6px` stroke), rotates `0deg` open / `-90deg` closed, `0.15s ease`.
  - Year label — `Inter Tight 22/600`, letter-spacing `-0.5px`, color `#0F0F0E`.
  - Right-aligned counter: "**N / M complete**" — `JetBrains Mono 11`, color `#8A8677`. N = sets in this year with all 5 signals; M = total sets in this year (after filters).
- Default state: only the most recent year (top one) is open; older years collapsed.
- Inside an open year, sport sub-groups stacked top margin `22px` apart.

**Sport sub-group**
- Mono label (e.g. "BASKETBALL") above the card — `JetBrains Mono 10/600`, letter-spacing `2px`, color `#3A372F`, padding `0 4px 10px`.
- Card: white bg, `1px` border `#EDEAE0`, radius `10px`, overflow hidden.
- Each set is one row, separated by `1px` `#F1EEE3` top border.

**Set row**
- 3-column grid: `92px | 1fr | auto`, gap `18px`, padding `14px 18px`, bg `#FFFFFF`.
- Hover: bg `#FDFCF8` (very subtle warm-up).
- The whole row is a link to that set's checklist (use existing routing — see ⚠️ note above).
- Column 1: **Manufacturer pill** (see below).
- Column 2: **Set name** — `Inter Tight 14/500`, letter-spacing `-0.1px`, color `#0F0F0E`. Truncate with ellipsis if needed.
- Column 3: **Coverage strip** — flex row, gap `22px`, 5 items in this order:
  1. ✓ Checklist
  2. ✓ [Release Date, formatted as "May 14, 2026"] / ✗ "No date"
  3. ✓ Parallels
  4. ✓ Box Config
  5. ✓ Pack Odds

**Coverage mark (per item)**
- Inline-flex, gap `5px`, font-size `13px`, no-wrap.
- Present (`ok=true`): icon `✓` + label, color `#0E8A4F` (green).
- Missing (`ok=false`): icon `✗` + label, color `#B7B2A3` (gray).
- Date item: when present, label is the formatted date (`MMM D, YYYY`); when missing, label is `"No date"`.
- Icon: `13px/600`, line-height `1`.

**Manufacturer pill**
- Inline-flex, min-width `56px`, padding `4px 10px`, font-size `11/600`, letter-spacing `0.2px`, radius `4px`.
- **Topps**: transparent bg, text `#E11D48`, `1px` border `#E11D48`.
- **Panini**: bg `#F2C230`, text `#1A1916`, `1px` border `#E0B41E`.

**Empty state**
- Shown when the filter combination matches no sets.
- Centered, `1px` dashed border `#D9D5C7`, radius `12px`, padding `80px 20px`, top margin `40px`.
- "No sets match these filters." (`14/500`, `#3A372F`) + smaller hint "Try clearing filters or toggling 'Show only incomplete'." (`12`, `#8A8677`).

---

### 2. Sets Coverage (Mobile)

**Purpose:** Same admin task on a phone — quickly triage which sets are missing data while away from a desk.

Rendered inside an iOS device frame in the prototype. **Production should render at the device's natural width**, not inside the frame component (the frame is a preview tool only).

**Layout**
- Top padding `54px` (under status bar), bottom padding `40px`.
- Background `#FAFAF7`.
- Body font: `-apple-system, system-ui, sans-serif`.

**Header**
- Back breadcrumb "‹ Home" — `15px`, color `#6B6757`, padding `10px 20px 0`.
- Title "Sets Coverage" — `Inter Tight 30/700`, letter-spacing `-0.8px`, line-height `1`, top margin `12px`.
- Subtitle "**N** of **M** sets tracked" — `13px`, color `#6B6757`, numbers `#0F0F0E/600`.

**Required Coverage legend (collapsible)**
- Padding `14px 20px 0`.
- Collapsed state: white card, `1px` border `#EDEAE0`, radius `10px`, padding `10px 12px`. Shows the 5 example dot-letters (all green) + "REQUIRED COVERAGE" label + chevron.
- Expanded: second card below with 2-column grid of `[colored letter] [label]` pairs (gap `8px` row, `10px` col).
- Letters: `C` Checklist, `D` Release Date, `P` Parallels, `B` Box Config, `O` Pack Odds.

**Manufacturer chips row**
- Horizontal scroll, gap `6px`, padding `14px 20px 0`, no scrollbar.
- Mono label "MFR" at start (`JetBrains Mono 9`, letter-spacing `1.4px`, color `#8A8677`).
- Chip styling matches desktop manufacturer pills (Topps red outline, Panini yellow fill when active), but on a white card-style background `#FFFFFF` with `1px` border `#E6E3D9` when inactive. Padding `7px 12px`, radius `999px`, `13px`.

**Sport chips row**
- Horizontal scroll, gap `6px`, padding `8px 20px 0`, no scrollbar.
- Mono label "SPORT" at start, same style as MFR label.
- Same chip styling as Checklists Mobile sport chips (white card inactive, dark active).

**Show only incomplete toggle**
- Padding `12px 20px 0`.
- Pill button with leading checkbox-glyph: `14×14` square with `1px` border (`#B7B2A3` inactive / `#FAFAF7` active) and `✓` glyph when active.
- Inactive: bg `#FFFFFF`, text `#3A372F`, border `#E6E3D9`.
- Active: bg `#0F0F0E`, text `#FAFAF7`, border `#0F0F0E`.

**Year section**
- Header `<button>`, padding `10px 14px`, bottom border `1px #EDEAE0`, top margin `24px`.
  - `11×11` caret (`0deg` open / `-90deg` closed, `0.15s ease`).
  - Year label — `Inter Tight 18/700`, letter-spacing `-0.4px`.
  - Right counter "N/M" — `JetBrains Mono 10`, color `#8A8677`.
- Default open: most recent year only.

**Sport sub-group**
- Mono label (e.g. "BASKETBALL") — `JetBrains Mono 9/600`, letter-spacing `1.6px`, color `#3A372F`, padding `0 14px 8px`.
- White card with `1px` border `#EDEAE0`, radius `10px`, margin `0 14px`, overflow hidden.

**Set row (mobile)**
- Padding `12px 14px`, white bg, `1px` top border `#F1EEE3`.
- The whole row is a link (preserve existing routing — see ⚠️ note above).
- **Top meta line** (flex, gap `8px`, margin-bottom `6px`):
  - Manufacturer pill (compact: padding `2px 7px`, font-size `10/600`, radius `3px`, same color rules as desktop).
  - Date label — `JetBrains Mono 9`, color `#8A8677`, letter-spacing `0.6px`. Format `"MMM D"` if present, else `"NO DATE"`.
  - Right-aligned status tag — `JetBrains Mono 9/600`, letter-spacing `0.6px`. **READY** in green `#0E8A4F` if all 5 signals present; **N MISSING** in red `#C2410C` otherwise.
- **Set name** — `Inter Tight 14/600`, letter-spacing `-0.2px`, color `#0F0F0E`, line-height `1.25`, margin-bottom `8px`.
- **Coverage dots strip** (5 mini chips, gap `3px`):
  - Each chip: `16×16` square, radius `4px`, contains a single uppercase letter (C/D/P/B/O), `JetBrains Mono 8/700`.
  - Present: bg `rgba(14,138,79,0.12)`, text `#0E8A4F`.
  - Missing: bg `rgba(183,178,163,0.18)`, text `#B7B2A3`.
  - Order: C, D, P, B, O (same field order as the legend).

**Empty state**
- Same copy as desktop. Margin `30px 20px`, padding `40px 20px`, dashed border `1px #D9D5C7`, radius `12px`, centered, `13px`, `#8A8677`.

---

## Interactions & Behavior

- **Manufacturer filter**: single-select. "All" clears the filter.
- **Sport filter**: single-select. "All" clears the filter.
- **Show only incomplete**: toggle. When on, hides any set that has all 5 signals present (i.e. shows only sets needing admin attention).
- **Year section toggle**: clicking the year header expands/collapses that year. Most recent year defaults open; older years default collapsed.
- **Row click → checklist**: navigates to that set's checklist detail. **Use the existing routing already wired in the codebase.**
- **Year counter** ("N / M complete") and the page-level "**N** of **M** sets tracked" should both update live as filters change. M = total in scope (after filters); N = subset that has all 5 coverage signals.
- **Hover states**: rows lighten to `#FDFCF8`; chip hover behaviors match Checklists page.

---

## Type System

Same as Checklists. Recap:
- **Display**: Inter Tight (500/600/700) — page titles, set names
- **Body**: Inter (400/500/600) — chips, buttons, labels
- **Mono**: JetBrains Mono (400/500/600/700) — taxonomy labels, counts, status tags
- **System fallbacks** on mobile: `-apple-system, system-ui, sans-serif`

Key sizes:

| Use | Size / weight / tracking |
|---|---|
| Desktop page title | `48 / 600 / -1.2` |
| Mobile page title | `30 / 700 / -0.8` |
| Year header (desktop) | `22 / 600 / -0.5` |
| Year header (mobile) | `18 / 700 / -0.4` |
| Set name (desktop) | `14 / 500 / -0.1` |
| Set name (mobile) | `14 / 600 / -0.2` |
| Coverage label | `13 / 400` |
| Coverage dot letter (mobile) | `8 / 700` (mono) |
| Section/category label (mono) | `10 / 600` letter-spacing `2` (desktop), `9 / 600` LS `1.6` (mobile) |
| Filter chip text | `13` (`/500` active, `/400` inactive) |
| "READY" / "N MISSING" tag (mobile) | `9 / 600` LS `0.6` (mono) |

---

## Color Tokens

Same warm palette as Checklists. Recap of what this page uses:

| Token | Hex | Use |
|---|---|---|
| Background | `#FAFAF7` | page bg |
| Surface | `#FFFFFF` | cards, rows |
| Surface hover | `#FDFCF8` | row hover |
| Border | `#EDEAE0` | card borders, dividers |
| Border subtle | `#F1EEE3` | inter-row dividers |
| Border muted | `#D9D5C7` | dashed empty-state border |
| Text primary | `#0F0F0E` | titles, set names |
| Text secondary | `#3A372F` | chips, labels |
| Text muted | `#6B6757` | breadcrumb, subtitle |
| Text faint | `#8A8677` | counters, mono captions |
| Text faintest | `#B7B2A3` | "missing" gray, secondary mono |
| Accent dark | `#0F0F0E` | active chip bg, primary button |
| Coverage green | `#0E8A4F` | ✓ marks, "READY" tag, legend dots |
| Coverage gray | `#B7B2A3` | ✗ marks |
| Status red (mobile) | `#C2410C` | "N MISSING" tag |
| Topps red | `#E11D48` | Topps pill border + text |
| Panini yellow | `#F2C230` | Panini pill bg |
| Panini border | `#E0B41E` | Panini pill border |
| Panini ink | `#1A1916` | Panini pill text |
| Panini muted text | `#B47A0F` | inactive Panini chip text |

---

## Spacing, Radii, Shadows

- **Container max-width**: `1440px` (desktop), full width (mobile).
- **Container padding**: `40px 56px 80px` (desktop), `0` (mobile — children pad themselves).
- **Card radius**: `10px` (rows, legend, sport sub-group cards).
- **Pill chip radius**: `999px`.
- **Manufacturer pill radius**: `4px` (desktop), `3px` (mobile).
- **Coverage dot radius**: `4px`.
- **Empty-state radius**: `12px`.
- No drop shadows on this page; rely on borders and bg-tint hover.

---

## Coverage Logic

A set is **complete** (counts toward "N complete" and the green "READY" tag) iff all of:

```
hasPlayerChecklist === true
hasPackOdds === true
hasBoxConfig === true
hasNumberedParallels === true
releaseDate != null
```

Otherwise it is **incomplete**. The mobile "**N MISSING**" tag is the count of those five fields that evaluate false/null for that set.

These flags should be **derived from the existing data model**, not stored as new boolean columns. For example:

- `hasPlayerChecklist` ← `set.checklist_cards.count > 0`
- `hasPackOdds` ← `set.pack_odds.exists`
- `hasBoxConfig` ← `set.box_config.exists`
- `hasNumberedParallels` ← `set.parallels.count > 0`
- `releaseDate` ← `set.released_at`

(The exact field names will depend on the production schema — these are illustrative.)

---

## Files in this bundle

- `design/Sets Coverage.html` — desktop entry
- `design/Sets Coverage Mobile.html` — mobile entry
- `design/coverage-app.jsx` — desktop app (filters + year sections + rows)
- `design/coverage-mobile-app.jsx` — mobile app
- `design/coverage-data.js` — **placeholder** sets, manufacturers, sports, and field list (reference shape only; bind UI to existing production data)
- `design/ios-frame.jsx` — iOS device frame used only for mobile preview (not production)
