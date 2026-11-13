import { test } from "node:test";
import assert from "node:assert/strict";
import { buildOrderedFormats, resolveOddsRow } from "./athleteOddsResolver";
import { label } from "./boxLabels";

// Fixture modeled on set 896's "1981-82 Topps Chrome Basketball" lines: the
// subset's real odds live only in promo_silver, while the MAIN base set carries
// a "Base Aqua Refractor" = 1 in hobby (the key the old resolver wrongly borrowed).
const PACK_ODDS = JSON.stringify({
  hobby: { Base: 2, "Base Aqua Refractor": 1, "Base Blue Refractor": 1 },
  promo_silver: {
    "1981-82 Topps Chrome Basketball": 1,
    "1981-82 Topps Chrome Basketball Aqua Refractor": 18,
    "1981-82 Topps Chrome Basketball Blue Refractor": 24,
  },
});
const SUB = "1981-82 Topps Chrome Basketball";

// The component tags a figure when it comes from a format other than the chip.
const tagFor = (formatKey: string, selected: string) =>
  formatKey !== "__flat__" && formatKey !== selected ? label(formatKey) : null;

test("hobby chip selected: subset falls through to promo_silver, tagged", () => {
  const ordered = buildOrderedFormats(PACK_ODDS, "hobby");

  const base = resolveOddsRow(ordered, SUB, null);
  assert.equal(base?.value, 1); // 1:1
  assert.equal(base?.formatKey, "promo_silver");
  assert.equal(tagFor(base!.formatKey, "hobby"), "Promo Silver Packs");

  const aqua = resolveOddsRow(ordered, SUB, "Aqua Refractor");
  assert.equal(aqua?.value, 18); // 1:18 — NOT the base set's "Base Aqua Refractor" = 1
  assert.equal(aqua?.formatKey, "promo_silver");
  assert.equal(tagFor(aqua!.formatKey, "hobby"), "Promo Silver Packs");

  // A parallel with no key in any format renders "—".
  assert.equal(resolveOddsRow(ordered, SUB, "Nonexistent Refractor"), null);
});

test("promo_silver chip selected: same figures, untagged", () => {
  const ordered = buildOrderedFormats(PACK_ODDS, "promo_silver");

  const base = resolveOddsRow(ordered, SUB, null);
  assert.equal(base?.value, 1);
  assert.equal(base?.formatKey, "promo_silver");
  assert.equal(tagFor(base!.formatKey, "promo_silver"), null); // from the selected format → no tag

  const aqua = resolveOddsRow(ordered, SUB, "Aqua Refractor");
  assert.equal(aqua?.value, 18);
  assert.equal(tagFor(aqua!.formatKey, "promo_silver"), null);
});

test("base row never borrows a parallel key; parallel never borrows the subset base", () => {
  const ordered = buildOrderedFormats(PACK_ODDS, "hobby");
  // Base resolves the subset key (1), not any parallel figure.
  assert.equal(resolveOddsRow(ordered, SUB, null)?.value, 1);
  // Blue parallel resolves its own 24, not the subset base (1) or base-set "Base Blue Refractor" (1).
  assert.equal(resolveOddsRow(ordered, SUB, "Blue Refractor")?.value, 24);
});
