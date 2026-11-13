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
