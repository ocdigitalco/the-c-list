import { test } from "node:test";
import assert from "node:assert/strict";
import { pickAliasRedirectTarget, athleteHref, type AliasCandidate } from "./util";

// The merge keeps the Cyrillic spelling "Egor Dёmin" as an alias of the Latin
// canonical. The app's slugify maps that Cyrillic form to the OLD slug
// "egor-d-min" (Cyrillic ё is not [a-z], so it drops to a dash), while the Latin
// forms map to "egor-demin".
const EGOR: AliasCandidate = {
  slug: "egor-demin",
  pageKind: "player",
  name: "Egor Dëmin",
  aliases: ["Egor Demin", "Egor Dëmin", "Egor Dёmin"], // U+0451 Cyrillic ё
};

test("old Cyrillic slug egor-d-min → canonical /athletes/egor-demin", () => {
  const target = pickAliasRedirectTarget("egor-d-min", [EGOR]);
  assert.deepEqual(target, { pageKind: "player", slug: "egor-demin" });
  assert.equal(athleteHref(target!.pageKind, target!.slug), "/athletes/egor-demin");
});

test("canonical slug itself still resolves to its own page (one target)", () => {
  const target = pickAliasRedirectTarget("egor-demin", [EGOR]);
  assert.deepEqual(target, { pageKind: "player", slug: "egor-demin" });
});

test("unknown slug → null (caller 404s)", () => {
  assert.equal(pickAliasRedirectTarget("nobody-here", [EGOR]), null);
});

test("multiple alias forms of the SAME athlete count as one target", () => {
  const c: AliasCandidate = {
    slug: "bob-lee",
    pageKind: "person",
    name: "Bob Lee",
    aliases: ["Bob Lee", "Bobby Lee"],
  };
  const target = pickAliasRedirectTarget("bob-lee", [c]);
  assert.deepEqual(target, { pageKind: "person", slug: "bob-lee" });
});

test("ambiguous alias (two distinct athletes) → null (caller 404s)", () => {
  const a: AliasCandidate = { slug: "jon-smith", pageKind: "player", name: "Jon Smith", aliases: ["Jon Smith"] };
  const b: AliasCandidate = { slug: "jonathan-smith", pageKind: "person", name: "Jonathan Smith", aliases: ["Jon Smith"] };
  assert.equal(pickAliasRedirectTarget("jon-smith", [a, b]), null);
});

test("cross-kind redirect uses the matched athlete's own page_kind", () => {
  const character: AliasCandidate = {
    slug: "jabba-the-hutt",
    pageKind: "character",
    name: "Jabba the Hutt",
    aliases: ["Jabba the Hutt", "Jabba The Hutt"],
  };
  const target = pickAliasRedirectTarget("jabba-the-hutt", [character]);
  assert.equal(athleteHref(target!.pageKind, target!.slug), "/characters/jabba-the-hutt");
});
