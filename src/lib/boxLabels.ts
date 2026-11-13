/**
 * Canonical box-format key → display label, shared by every surface that
 * renders a box/odds format (set page, athlete & team pages, box-config and
 * pack-odds tables, break simulator, SEO summaries, article parallel grids).
 *
 * Add a format key here ONCE; every consumer picks it up. The `label()` helper
 * also applies the historical Title-Case fallback for any key not listed.
 */
export const BOX_LABELS: Record<string, string> = {
  hobby: "Hobby",
  nycc: "NYCC", // New York Comic Con exclusive box (Mint Disney set 897)
  members_only: "Members Only", // Stadium Club Chrome UCL exclusive box
  hobby_box_topper: "Box Topper",
  jumbo: "Jumbo",
  hobby_jumbo: "Hobby Jumbo",
  mega: "Mega",
  blaster: "Blaster",
  value: "Value",
  fat_pack: "Fat Pack",
  hanger: "Hanger",
  all_star_mega: "All-Star Game Mega",
  black_friday_value: "Black Friday Value Blaster",
  fanatics_value: "Fanatics Value Blaster",
  // Flagship Basketball (set 896) retail/regional formats
  promo_silver: "Promo Silver Packs",
  costco: "Costco Flagship Collection",
  china_wave1: "China Exclusive Wave 1",
  china_wave2: "China Exclusive Wave 2",
  sams_club: "Sam's Club Box",
  super_box: "Super Box",
  super_box_bonus: "Super Box Bonus Pack",
  tin: "Collector Tin",
  advent: "Advent Calendar",
  // Topps Vault Disney publishes odds per pack slot, not per box format.
  pack_1: "Pack #1 (Relics & Sketches)",
  pack_2: "Pack #2 (Autographs)",
  topper: "Box Topper",
  // All Breaker's Delight key spellings render "Breaker Delight" — the form
  // Topps uses on its product listings (the apostrophe version was ours).
  breakers_delight: "Breaker Delight",
  breakers: "Breaker Delight", // legacy article key
  delight: "Breaker Delight",
  breaker: "Breaker Delight", // legacy alias → same label
  first_day_issue: "First Day Issue",
  fdi: "First Day Issue",
  hobby_hybrid: "Hobby Hybrid",
  sapphire: "Sapphire",
  hongbao: "Hongbao",
  logofractor: "Logofractor",
  ffnyc: "FFNYC",
  mania: "Mania",
  instant: "Instant Packs",
  fanatics: "Fanatics",
  diamond_anniversary: "Diamond Anniversary",
  // Retail SE/EA/CEE variants fold into their base box type
  value_se: "Value", value_ea: "Value", value_cee: "Value",
  mega_se: "Mega", mega_ea: "Mega", mega_cee: "Mega",
  hanger_se: "Hanger", hanger_ea: "Hanger", hanger_cee: "Hanger",
};

/** Display label for a box-format key, with Title-Case fallback for unknowns. */
export function label(key: string): string {
  return BOX_LABELS[key] ?? key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

/**
 * Buyer-preference order the Pack Odds column falls through when a row's key
 * lives in only some formats. The curated head encodes "what a typical buyer
 * opens" (hobby first); the tail appends every other format key seen in any
 * set's pack_odds, in boxLabels.ts order (keys absent from BOX_LABELS trail).
 * Any format still not listed is appended per-set in its JSON order by the
 * resolvers, so every format is always reachable.
 *
 * Single source of truth, shared by the set page and the set-scoped athlete
 * page so both resolve an odds figure the same way.
 */
export const ODDS_FORMAT_PREFERENCE: string[] = [
  "hobby", "members_only", "hobby_box_topper", "jumbo", "value", "mega", "tin", "advent", "hanger", "fat_pack", "fanatics", "london_mega", "walmart_mega",
  "fanatics_value", "all_star_mega", "black_friday_value", "promo_silver", "costco", "sams_club", "china_wave1", "china_wave2",
  "hobby_silver_pack", "jumbo_silver_pack", "super_box", "super_box_bonus", "super_box_oversized", "bulk_packs",
  "club_super_box", "club_super_box_oversized", "kids_mega", "club_ex_box_sams", "club_ex_box_sams_oversized", "gc_white_slip_sheets",
  "pack_1", "pack_2", "topper",
  // Every remaining format key present in some set's pack_odds, in boxLabels.ts
  // order (keys with no BOX_LABELS entry trail, alphabetical).
  "nycc", "hobby_jumbo", "blaster", "breakers_delight", "delight", "breaker", "first_day_issue", "fdi", "sapphire", "hongbao", "logofractor", "ffnyc", "mania", "instant", "diamond_anniversary",
  "value_se", "value_ea", "value_cee", "mega_se", "mega_ea", "mega_cee", "hanger_se", "hanger_ea",
  "Hobby", "Mega Box CEE", "Mega Box EA", "Mega Box SE", "Value", "Value Box CEE", "Value Box EA", "Value Box SE",
  "bulk", "carnaval", "disneyland_exclusive", "fat_pack_ea", "fat_pack_se", "hat_trick", "japan_hobby", "japan_retail", "london_store", "lunar", "spring_tin", "target_mega", "value_blaster",
];
