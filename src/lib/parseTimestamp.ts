/**
 * Parse a stored set timestamp to epoch ms, always treating a timezone-less
 * value as UTC. Turso/SQLite stores `created_at` in one of three shapes:
 *   - ISO UTC:        "2026-10-23T00:00:00Z"
 *   - datetime('now'): "2026-10-13 12:00:00"  (space-separated, UTC, no tz)
 *   - date only:       "2026-10-13"
 *
 * `new Date("2026-10-13 12:00:00")` parses the space form in the *local*
 * timezone, which makes the 14-day "recently added" window depend on the
 * server's timezone (a PT dev box disagrees with UTC production at the
 * boundary). Normalizing every tz-less value to UTC keeps membership
 * deterministic and identical in dev and prod.
 */
export function parseUtcMs(s: string | null | undefined): number {
  if (!s) return 0;
  let iso = s.trim().replace(" ", "T");
  if (iso.length === 10) iso += "T00:00:00Z"; // date only
  else if (!/([zZ]|[+-]\d\d:?\d\d)$/.test(iso)) iso += "Z"; // no tz → UTC
  const t = new Date(iso).getTime();
  return isNaN(t) ? 0 : t;
}
