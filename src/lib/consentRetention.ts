/**
 * Consent-log retention: delete consent_events rows older than 24 months.
 *
 * `ts` is stored as an ISO-8601 string, which sorts lexicographically in the
 * same order as chronologically, so a string comparison against the cutoff is
 * correct. Runs against whatever @/lib/db targets (Turso in production).
 */
import { rawQuery } from "./db";

export const RETENTION_MONTHS = 24;

/** ISO cutoff = now minus RETENTION_MONTHS. Pass `now` for deterministic tests. */
export function retentionCutoffIso(now: Date = new Date()): string {
  const d = new Date(now);
  d.setMonth(d.getMonth() - RETENTION_MONTHS);
  return d.toISOString();
}

/** Delete rows older than the cutoff. Returns the number of rows removed. */
export async function deleteExpiredConsentEvents(now: Date = new Date()): Promise<number> {
  const cutoff = retentionCutoffIso(now);
  const res = await rawQuery.run("DELETE FROM consent_events WHERE ts < ?", cutoff);
  // libsql exposes affected rows as rowsAffected.
  return (res as { rowsAffected?: number })?.rowsAffected ?? 0;
}
