/**
 * Turn a raw eBay break-spot title into a short, human spot label, and pull out a
 * trailing "Break #1026-14"-style identifier as `breakRef` (used to split one
 * seller's listings into distinct breaks). Set-agnostic: the tokens stripped are
 * derived from the set's own name, not a hardcoded brand list.
 *
 * Cleanup order (see the Phase 0 report): extract break_ref → strip the breaker's
 * common prefix/suffix boilerplate → strip the set's year + distinctive tokens →
 * strip "break"/"box break"/"case break" → strip emoji/decoration → collapse
 * whitespace. Falls back to the truncated raw title when nothing meaningful remains.
 */

function cleanName(name: string): string {
  return name.replace(/[®™]/g, "").replace(/\([^)]*\)/g, "").replace(/\s+/g, " ").trim();
}

function yearToken(name: string): string {
  const m = name.match(/\b(19|20)\d{2}(-\d{2})?\b/);
  return m ? m[0] : "";
}

function escapeRe(s: string): string {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

/** Distinctive tokens of a set name (year + <3-char words + "the" removed), lowercased. */
export function setNameTokens(setName: string): string[] {
  const clean = cleanName(setName);
  const year = yearToken(clean).toLowerCase();
  return clean
    .toLowerCase()
    .replace(year, " ")
    .split(/[^a-z0-9]+/)
    .filter((w) => w.length >= 3 && w !== "the");
}

/**
 * Pull a trailing "Break #<id>" identifier off a title. Returns the ref (e.g.
 * "1026-14") and the title with that identifier — and a trailing "Break" word —
 * removed. No trailing `#id` → { breakRef: null, rest: trimmed title }.
 */
export function extractBreakRef(title: string): { breakRef: string | null; rest: string } {
  const m = title.match(/#\s*([A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)\s*$/);
  if (!m || m.index == null) return { breakRef: null, rest: title.trim() };
  const rest = title.slice(0, m.index).replace(/\bbreak(?:ing|s)?\b\s*$/i, "").trim();
  return { breakRef: m[1], rest };
}

/** Longest common prefix and suffix across a set of strings (both "" for <2). */
export function commonAffix(strs: string[]): { prefix: string; suffix: string } {
  if (strs.length < 2) return { prefix: "", suffix: "" };
  let prefix = strs[0];
  let suffix = strs[0];
  for (const x of strs) {
    while (prefix && !x.startsWith(prefix)) prefix = prefix.slice(0, -1);
    while (suffix && !x.endsWith(suffix)) suffix = suffix.slice(1);
  }
  return { prefix, suffix };
}

/**
 * Clean one title into a spot label. `commonPrefix`/`commonSuffix` are the
 * breaker's shared boilerplate (compute with `commonAffix` over the breaker's
 * break-ref-stripped titles) and are only applied when ≥3 chars.
 */
export function spotLabel(
  title: string,
  ctx: { setName: string; commonPrefix?: string; commonSuffix?: string }
): { label: string; breakRef: string | null; fallback: boolean } {
  const { breakRef, rest } = extractBreakRef(title);
  let s = rest;

  const cp = ctx.commonPrefix ?? "";
  const cs = ctx.commonSuffix ?? "";
  if (cp.length >= 3 && s.startsWith(cp)) s = s.slice(cp.length);
  if (cs.length >= 3 && s.endsWith(cs)) s = s.slice(0, -cs.length);

  const year = yearToken(cleanName(ctx.setName));
  if (year) s = s.replace(new RegExp(escapeRe(year), "gi"), " ");
  for (const tok of setNameTokens(ctx.setName)) s = s.replace(new RegExp(`\\b${escapeRe(tok)}\\b`, "gi"), " ");

  s = s.replace(/\b(box\s+break|case\s+break|break(?:ing|s)?)\b/gi, " ");
  s = s.replace(/[^\p{L}\p{N}\s#/&'.-]/gu, " "); // emoji / decorative chars
  s = s.replace(/\s+/g, " ").replace(/^[\s·,|/#-]+|[\s·,|/#-]+$/g, "").trim();

  const meaningful = s.replace(/[^\p{L}\p{N}]/gu, "").length >= 2;
  if (!meaningful) {
    const raw = title.length > 40 ? title.slice(0, 39).trimEnd() + "…" : title;
    return { label: raw, breakRef, fallback: true };
  }
  return { label: s, breakRef, fallback: false };
}
