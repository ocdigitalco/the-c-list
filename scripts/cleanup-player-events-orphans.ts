/**
 * One-time cleanup of orphaned player_events rows on Turso (production).
 *
 * The orphan audit found 11 player_events rows whose player_id no longer
 * resolves to a players row — dead analytics leftovers from old full reseeds
 * that churned player ids before the scoped natural-key sync landed. They are
 * harmless but untidy; this removes them.
 *
 * ONLY player_events is touched. No other table is referenced or modified.
 * Prints the count before, the number deleted, and the count after (must be 0).
 *
 * Requires TURSO_DATABASE_URL and TURSO_AUTH_TOKEN in .env.local.
 * Run once:  npx tsx scripts/cleanup-player-events-orphans.ts
 */
import dotenv from "dotenv";
dotenv.config({ path: ".env.local" });
import { createClient } from "@libsql/client";

const TURSO_URL = process.env.TURSO_DATABASE_URL;
const TURSO_TOKEN = process.env.TURSO_AUTH_TOKEN;

if (!TURSO_URL || !TURSO_TOKEN) {
  console.error("Missing TURSO_DATABASE_URL or TURSO_AUTH_TOKEN in environment.");
  process.exit(1);
}

const turso = createClient({ url: TURSO_URL, authToken: TURSO_TOKEN });

const ORPHAN_WHERE =
  "player_events WHERE player_id NOT IN (SELECT id FROM players)";

async function count(where: string): Promise<number> {
  const res = await turso.execute(`SELECT COUNT(*) AS v FROM ${where}`);
  return Number(res.rows[0]!.v);
}

async function main() {
  console.log(`Target: ${TURSO_URL}`);

  const before = await count(ORPHAN_WHERE);
  console.log(`orphaned player_events before: ${before}`);

  const del = await turso.execute(`DELETE FROM ${ORPHAN_WHERE}`);
  const deleted = del.rowsAffected;
  console.log(`rows deleted:                  ${deleted}`);

  const after = await count(ORPHAN_WHERE);
  console.log(`orphaned player_events after:  ${after}`);

  if (after !== 0) {
    console.error(`\n✗ Expected 0 orphans after cleanup, found ${after}.`);
    process.exit(1);
  }
  console.log("\n✓ Cleanup complete — no orphaned player_events remain.");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
