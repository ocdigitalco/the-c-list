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
  hobby_box_topper: "Box Topper",
  jumbo: "Jumbo",
  hobby_jumbo: "Hobby Jumbo",
  mega: "Mega",
  blaster: "Blaster",
  value: "Value",
  fat_pack: "Fat Pack",
  hanger: "Hanger",
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
