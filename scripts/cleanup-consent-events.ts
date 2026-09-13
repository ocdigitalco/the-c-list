/**
 * Consent-log retention cleanup (documented runner).
 *
 *   npx tsx scripts/cleanup-consent-events.ts
 *
 * Deletes consent_events rows older than 24 months (see RETENTION_MONTHS in
 * src/lib/consentRetention.ts). Writes to whatever @/lib/db targets — set
 * TURSO_DATABASE_URL / TURSO_AUTH_TOKEN in .env.local to run against production.
 *
 * This same deletion also runs automatically as the last step of the 09:00 UTC
 * eBay-offers cron (src/app/api/cron/ebay-offers/route.ts), guarded so a failure
 * there cannot affect the offers walk. Run this script only for a manual/ad-hoc
 * sweep or a one-off backfill.
 */
import { config } from "dotenv";
config({ path: ".env.local" });

(async () => {
  // Dynamic import AFTER dotenv so db.ts reads the TURSO env (ESM hoists static
  // imports above the config() call otherwise).
  const { deleteExpiredConsentEvents, retentionCutoffIso } = await import("../src/lib/consentRetention");
  const cutoff = retentionCutoffIso();
  const removed = await deleteExpiredConsentEvents();
  console.log(`consent_events cleanup: removed ${removed} row(s) older than ${cutoff}.`);
})();
