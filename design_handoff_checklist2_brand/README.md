# Handoff: Checklist² Brand System

## Overview

**Checklist²** ("Checklist Squared") is a brand identity for a sports-card checklist product. This handoff contains the complete brand system: logomark, wordmark, lockup, avatar/app icon variants, color palette, and typography. The "squared" concept is expressed literally — the mark is **two offset solid sports cards**, where the duplicate IS the squaring. The wordmark pairs the word *Checklist* with a red `²` superscript.

This package is the source of truth for implementing the brand in any surface — web app, mobile app, marketing site, social avatars, favicon, app store listings, print.

---

## About the Design Files

The files in this bundle (`Checklist2 Brand Sheet.html`, `brand-system.jsx`) are **design references created in HTML/React** — a self-contained brand sheet showing the intended look, geometry, and color of the system. They are NOT production code to copy directly.

Your task is to **recreate this brand system inside the target codebase** using its established environment, libraries, and patterns. If no environment exists yet, choose the most appropriate framework for the project and implement there.

The HTML brand sheet is the visual spec. The JSX file (`brand-system.jsx`) shows the exact geometry math used to render the mark and avatar — port it 1:1 into your stack (React component, Vue SFC, SwiftUI shape, SVG asset, whatever fits). All numeric ratios in that file are intentional and should be preserved exactly.

---

## Fidelity

**High-fidelity (hifi).** Every color is a final hex. Every typographic value (size, weight, letter-spacing) is final. The mark geometry is locked — card ratio, offset percentages, fill assignments. Implement pixel-perfectly.

---

## The Brand System

### 1. Logomark (the "two cards")

Two solid rectangles drawn at the actual sports-card aspect ratio (**2.5 : 3.5**), offset diagonally so the back card peeks out top-and-right of the front card.

**Geometry (rendered into a square `s × s` viewbox):**

```
cardH    = s * 0.78
cardW    = cardH * (2.5 / 3.5)   // ≈ cardH * 0.7143
offsetY  = 0.18                  // back card revealed by 18% of card height
offsetX  = offsetY * 1.4         // = 0.252; back card revealed by 25.2% of card height to the right

totalW   = cardW * (1 + offsetX)
totalH   = cardH * (1 + offsetY)

// Front card position (centered horizontally, with the back card peeking up-right)
fx       = (s - totalW) / 2
fy       = (s - totalH) / 2 + cardH * offsetY

// Back card position (offset up and right from front)
bx       = fx + cardW * offsetX
by       = fy - cardH * offsetY
```

**Fills:**
- Front card: `Ink` `#0E0E0E`
- Back card: `Card Red` `#D63A20`

**Rules (non-negotiable):**
- **Card ratio is 2.5 : 3.5** — actual sports-card proportion. Never freelance.
- **Always two cards.** The duplicate IS the "squared." Never use a single card.
- **Equal reveals.** The back card shows equal-feeling strips on top and right.
- **Sharp 90° corners.** No `border-radius`, ever, on the mark.
- **Front = Ink, back = Card Red.** Never swap. Never recolor.
- **Mark renders with `shape-rendering: crispEdges`** (or platform equivalent) so the rectangles stay pixel-sharp at small sizes.

A reversed lockup version (used on `Ink` backgrounds) keeps the back card `Card Red` and switches the front card to `Paper` `#F1EDE4`.

### 2. Wordmark

The word **Checklist** set in **Inter Tight 800**, mixed case (capital C, lowercase rest), tightly tracked, followed by a smaller red `²` superscript.

| Property | Value |
|---|---|
| Font family | `Inter Tight` (fallback: `Inter`, `system-ui`, `sans-serif`) |
| Weight (Checklist) | 800 |
| Weight (²) | 900 |
| Case | Mixed (Checklist, not CHECKLIST) |
| Line height | 0.9 |
| Letter-spacing (Checklist) | `-0.042 em` (i.e. `-size * 0.042`) |
| Superscript size | `0.54 ×` the Checklist size |
| Superscript color | `Card Red` `#D63A20` |
| Superscript baseline shift | margin-top `-0.083 em` (raises it to sit above the cap line) |
| Superscript margin-left | `0.02 em` |
| Vertical alignment | `align-items: flex-start` (the ² hangs from the top, not the baseline) |

The wordmark is rendered as inline-flex of two `<span>` elements rather than a `<sup>` tag because the offsets are art-directed.

### 3. Lockup (mark + wordmark)

Horizontal pairing of the mark and wordmark.

```
gap between mark and wordmark = wordmarkSize * 0.19
mark size                     = wordmarkSize * 1.17
vertical alignment            = center
```

Two contexts:
- **Primary · paper** — on `Paper` `#F1EDE4` background. Front card `Ink`, back card `Card Red`, wordmark `Ink` with `Card Red` ².
- **Reversed · ink** — on `Ink` `#0E0E0E` background. Front card `Paper`, back card `Card Red`, wordmark `Paper` with `Card Red` ².

### 4. Avatar / App Icon (C² monogram)

For favicons, social avatars, app icons, and any square-tile context where the full mark is too detailed. A capital **C** with a small red **²** superscript.

Four themes:

| Theme | Tile | C glyph | ² glyph | Use |
|---|---|---|---|---|
| `card` | Two-card geometry (Ink front, Card Red back) | `Paper` (on the front card) | `Card Red` (in upper-right of the front card area) | **Primary** — premium app icon, social avatar |
| `dark` | `Ink` `#0E0E0E` flat tile | `Paper` `#F1EDE4` | `Card Red` `#D63A20` | **Default** — favicon, dark-mode UI |
| `light` | `Paper` `#F1EDE4` flat tile | `Ink` `#0E0E0E` | `Card Red` `#D63A20` | Light-mode UI, paper docs |
| `red` | `Card Red` `#D63A20` flat tile | `Paper` `#F1EDE4` | `Ink` `#0E0E0E` | Brand moments, accent |

**Flat-tile geometry (themes `dark` / `light` / `red`):**

```
C glyph:  fontSize = s * 0.74,  x = s * 0.46,  y = s * 0.55,  letter-spacing = -fontSize * 0.04
² glyph:  fontSize = (s * 0.74) * 0.42,  x = s * 0.80,  y = s * 0.30
```

Both glyphs use `font-family: Inter Tight; font-weight: 900; text-anchor: middle; dominant-baseline: central`.

**Card-tile geometry (theme `card`):**

```
cardH    = s * 0.86
cardW    = cardH * (2.5 / 3.5)
offsetY  = 0.10                  // tighter offset than the standalone mark
offsetX  = offsetY * 1.4 = 0.14

(card positions computed identically to standalone mark)

C glyph:  fontSize = cardH * 0.78,  x = fx + cardW * 0.46,  y = fy + cardH * 0.54
² glyph:  fontSize = (cardH * 0.78) * 0.42,
          x = fx + cardW * 0.84,  y = fy + cardH * 0.24
          fill = Card Red (sits on the front card, in upper-right)
```

The `dark` flat tile must render legibly down to **16px**. Verified sizes: 128, 96, 64, 48, 32, 16.

### 5. Don't (mark misuse)

These are explicitly forbidden:

1. **Recolor the front card.** Front is always `Ink`. Don't use brand blue, gradient, etc.
2. **Swap front and back.** Front is always `Ink`, back is always `Card Red`. Never invert.
3. **Round the corners.** No `border-radius`. The mark is hard-edged.

---

## Color Tokens

The system has **8 colors total**. One ink, one paper, one accent, plus 5 supporting tones. **Card Red is the only saturated color in the system.**

| Token | Hex | RGB | Role |
|---|---|---|---|
| `ink` | `#0E0E0E` | `14, 14, 14` | Primary text · front card · UI structure |
| `paper` | `#F1EDE4` | `241, 237, 228` | Default background · negative space |
| `accent` (Card Red) | `#D63A20` | `214, 58, 32` | Accent · back card · ² · CTAs |
| `inkSoft` | `#2A241C` | `42, 36, 28` | Body copy on paper |
| `paperDeep` | `#E5E0D3` | `229, 224, 211` | Section breaks · cards on paper |
| `accentDeep` | `#B12C18` | `177, 44, 24` | Pressed states · alt accent |
| `slate` | `#5A5247` | `90, 82, 71` | Secondary text · captions |
| `fog` | `#CFC8B8` | `207, 200, 184` | Borders · dividers · disabled |

**`accentSoft` = `#F2A192`** also exists in the source as a tinted accent for backgrounds — use sparingly, not exposed in the swatch grid.

**Usage rules:**
- Default page background: `paper` `#F1EDE4` (warm off-white, NOT pure white).
- Dark surfaces: `ink` `#0E0E0E` (NOT pure black).
- Borders: `fog` `#CFC8B8`, hairline (`1px solid`).
- One accent color only. Don't introduce a secondary brand color. If you need more visual variety, use the `paperDeep` and `inkSoft` neutrals.

---

## Typography Tokens

| Token | Stack | Use |
|---|---|---|
| `fontHead` | `"Inter Tight", "Inter", system-ui, sans-serif` | Wordmark, headings, display, all-caps section labels, button labels |
| `fontBody` | `"Inter", system-ui, sans-serif` | Body copy, lists, descriptive text |
| `fontMono` | `"JetBrains Mono", ui-monospace, Menlo, monospace` | Eyebrow labels, hex codes, RGB values, card numbers (e.g. `#BS-12`), data rows |

**Eyebrow / mono label spec** (used liberally throughout the brand sheet):
```
font-family: JetBrains Mono
font-size: 11px
letter-spacing: 1.6px
text-transform: uppercase
opacity: 0.6
```

**Section-header spec** (e.g. "Logo", "Color"):
```
font-family: Inter Tight
font-weight: 800
font-size: 56px
letter-spacing: -1.6px
text-transform: uppercase
```

**Display spec** (cover headline):
```
font-family: Inter Tight
font-weight: 800
font-size: 156px
letter-spacing: -7px
line-height: 0.86
case: mixed (Checklist, not CHECKLIST)
```

**Required Google Fonts to load:**
```
Inter Tight  weights 500, 600, 700, 800, 900
Inter        weights 400, 500, 600, 700
JetBrains Mono  weights 400, 500, 600, 700
```

---

## Layout Tokens (from the brand sheet)

| Token | Value |
|---|---|
| Section padding (large) | `80px 96px` (top/bottom × left/right) |
| Section padding (cover) | `80px 96px 96px` |
| Card padding | `56px` |
| Application-strip card padding | `32px` |
| Hairline border | `1px solid #CFC8B8` (fog) |
| Grid gap (large) | `24px` |
| Grid gap (medium) | `20px` |
| Eyebrow spacing | `marginBottom: 32px` |

No `border-radius` is used anywhere in the brand surfaces — the entire system is hard-edged.

---

## Files in This Bundle

- `README.md` — this document.
- `Checklist2 Brand Sheet.html` — the rendered brand sheet (cover, logo block with anatomy + avatar grid + size scale + don'ts, color block with 8-swatch palette + 3-panel application strip). Open in a browser to see the system in context.
- `brand-system.jsx` — the React/JSX source for the five brand primitives:
  - `CL2` — token object (colors + font stacks).
  - `CL2Mark` — the two-card logomark (props: `s`, `front`, `back`, `bg`).
  - `CL2Wordmark` — Checklist + ² wordmark (props: `size`, `ink`, `accent`).
  - `CL2Lockup` — mark + wordmark horizontal pairing (props: `size`, `ink`, `accent`, `bg`).
  - `CL2AppIcon` — C² avatar/app icon (props: `s`, `theme`, `radius`).

The geometry math in `brand-system.jsx` is the canonical source. When porting, preserve every numeric ratio exactly — small changes here are visible.

---

## Implementation Checklist

When porting to your codebase:

1. **Add the three font families** (Inter Tight, Inter, JetBrains Mono) to your font loading strategy.
2. **Add the 8 color tokens** to your design-token system (CSS custom props, Tailwind theme extension, design-system constants — whatever pattern your codebase uses).
3. **Build the four brand primitives** as components: `Mark`, `Wordmark`, `Lockup`, `AppIcon`. Use SVG for the mark and app icon (the geometry is exact and must be crisp at all sizes). The wordmark can be HTML+CSS or SVG depending on whether you need it selectable.
4. **Export the app icon** at the canonical sizes (16, 32, 48, 64, 96, 128, 256, 512, 1024 px) for favicon and app-store needs. The `dark` theme is the default favicon; the `card` theme is the premium app icon.
5. **Verify the mark renders crisply** at small sizes — check 16px and 24px favicons, especially. If your platform doesn't honor `shape-rendering: crispEdges`, consider rendering small sizes as PNG.
6. **Audit your existing UI** against the color rules — replace any pure white with `paper`, pure black with `ink`, and consolidate any other accent colors down to `Card Red`.

---

## Notes for the Developer

- **No emoji, no gradients, no rounded corners** in brand surfaces. The system is intentionally austere.
- **Card Red is precious.** Don't dilute it by using it for incidental UI (hover states on neutral elements, subtle highlights, etc.). It belongs to: the back card, the ², CTAs, and key data callouts only.
- **The mark is not a logo + symbol — it's just the symbol.** The wordmark is separate. The lockup is the combined unit. Use the right one for the context (favicon = AppIcon; app header = Lockup; large brand moment = Mark alone or Lockup).
- **Preserve mixed-case "Checklist."** It is NOT all-caps. The previous version of the brand was uppercase; the current direction is mixed case.
