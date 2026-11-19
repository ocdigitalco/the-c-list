# the-c-list — repo guidance

## Set builds — Phase 0 template

Every new set build (and data fix that reseeds appearances) starts with a read-only
**Phase 0** that reports findings and then **STOPs for a ruling** before any writes.
Phase 0 always includes the following check:

> **Rookie consistency.** Before seeding, report (a) every subject whose rows in the
> file have mixed `rookie` values (flagged on some cards, not on others), with the
> flagged card numbers, and (b) every subject flagged rookie who already has
> `is_rookie = 1` appearances in a set of the same sport with an earlier season
> (e.g., a 2025-26 set when building 2026-27). Both lists are rulings for Tyler, not
> auto-fixes: (a) is usually a manufacturer copy error on the minority cards; (b) is
> usually a manufacturer error unless the sport's convention allows multi-year RC
> status. Gates use the counts after rulings.

## Card-gallery image pass — renumber guard

The gallery image pass (drop cover byte-duplicates, convert PNG → JPEG, re-encode
to sRGB JPEG ≤ 1.5 MB, renumber survivors contiguous `-1…-N`) **must never
renumber a file that any source file references by its name** — unless it updates
every such reference in the **same commit**.

Before committing any renumber, grep the source (at least `src/lib/articles.ts`,
`src/lib/setNotes.ts`, `src/lib/updates.ts`, and anything else) for hard-coded
`/sets/cards/<slug>/<slug>-<n>.(jpg|png|webp)` paths. For each hit, find the image
it pointed at **before** the renumber (the committed file at that name in the prior
commit) and repoint it to that same image's new name. Because the pass re-encodes,
verify the match by dimensions + a perceptual pixel fingerprint (not md5). Article
hero images also feed the page's OpenGraph/Twitter `images` URL, so updating
`heroImage` is enough for those — but confirm it.
