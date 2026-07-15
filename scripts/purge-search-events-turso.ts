/**
 * One-off, SANCTIONED Turso data op: purge the historical polluted "search"
 * events (they were logged on as-you-type substring matches, not real search
 * selections). After the capture fix, "search" only accrues on genuine search
 * selections, so we start from a clean epoch.
 *
 * Scope: DELETE FROM player_events WHERE event_type = 'search' — and NOTHING
 * else. "view" rows are left untouched (reported before/after to prove it).
 *
 * Usage: npx tsx scripts/purge-search-events-turso.ts
 */
import dotenv from "dotenv";
dotenv.config({ path: ".env.local" });
import { createClient } from "@libsql/client";

const url = process.env.TURSO_DATABASE_URL;
const authToken = process.env.TURSO_AUTH_TOKEN;
if (!url || !authToken) {
  console.error("Missing TURSO_DATABASE_URL / TURSO_AUTH_TOKEN in .env.local");
  process.exit(1);
}
const turso = createClient({ url, authToken });

async function count(eventType: string): Promise<number> {
  const r = await turso.execute({
    sql: "SELECT COUNT(*) AS n FROM player_events WHERE event_type = ?",
    args: [eventType],
  });
  return Number(r.rows[0]?.n ?? 0);
}

async function main() {
  console.log(`Target: ${url}`);
  const searchBefore = await count("search");
  const viewBefore = await count("view");
  console.log(`\nBefore:  search = ${searchBefore}   view = ${viewBefore}`);

  const del = await turso.execute("DELETE FROM player_events WHERE event_type = 'search'");
  console.log(`\nDeleted ${del.rowsAffected} 'search' rows.`);

  const searchAfter = await count("search");
  const viewAfter = await count("view");
  console.log(`\nAfter:   search = ${searchAfter}   view = ${viewAfter}`);

  console.log("\n─── Result ───");
  console.log(`  search: ${searchBefore} → ${searchAfter}  ${searchAfter === 0 ? "✓ purged" : "✗ NOT EMPTY"}`);
  console.log(`  view:   ${viewBefore} → ${viewAfter}  ${viewBefore === viewAfter ? "✓ untouched" : "✗ CHANGED"}`);
}

main().then(() => process.exit(0)).catch((e) => { console.error(e); process.exit(1); });
