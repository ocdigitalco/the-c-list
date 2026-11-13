import { test } from "node:test";
import assert from "node:assert/strict";
import { subsetChipModel } from "./athleteSubsetChips";

// A stand-in for boxLabels.label() — only the keys these cases use.
const label = (k: string) =>
  (({
    hobby: "Hobby",
    hanger_se: "Hanger",
    promo_silver: "Promo Silver Packs",
    fanatics_value_blaster: "Fanatics Value Blaster",
  }) as Record<string, string>)[k] ?? k;

test("(a) all figured rows share one format → header '<X> only', no row chips", () => {
  const m = subsetChipModel(
    [{ formatKey: "promo_silver" }, { formatKey: "promo_silver" }, { formatKey: "promo_silver" }],
    "hobby",
    label,
  );
  assert.deepEqual(m.header, { text: "Promo Silver Packs only", dark: false });
  assert.deepEqual(m.rows, [null, null, null]);
});

test("(b) mixed formats → header '<selected> odds' (dark), only differing rows chipped", () => {
  const m = subsetChipModel(
    [{ formatKey: "hobby" }, { formatKey: "hobby" }, { formatKey: "hanger_se" }],
    "hobby",
    label,
  );
  assert.deepEqual(m.header, { text: "Hobby odds", dark: true });
  assert.equal(m.rows[0], null);
  assert.equal(m.rows[1], null);
  assert.deepEqual(m.rows[2], { text: "Hanger only", dashed: false });
});

test("(c) keyless row WITH exclusivity → dashed '<Exclusivity> only'", () => {
  const m = subsetChipModel(
    [{ formatKey: "hobby" }, { formatKey: null, exclusivity: "Fanatics Value Blaster" }],
    "hobby",
    label,
  );
  assert.equal(m.rows[0], null);
  assert.deepEqual(m.rows[1], { text: "Fanatics Value Blaster only", dashed: true });
});

test("(d) keyless row WITHOUT exclusivity → dashed 'No published odds'", () => {
  const m = subsetChipModel(
    [{ formatKey: "hobby" }, { formatKey: null }],
    "hobby",
    label,
  );
  assert.deepEqual(m.rows[1], { text: "No published odds", dashed: true });
});

test("flat odds render no chips at all", () => {
  const m = subsetChipModel(
    [{ formatKey: "__flat__" }, { formatKey: "__flat__" }, { formatKey: null }],
    "hobby",
    label,
    { flat: true },
  );
  assert.equal(m.header, null);
  assert.deepEqual(m.rows, [null, null, null]);
});
