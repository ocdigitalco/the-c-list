/**
 * Sync ufc_image_url values from local SQLite to Turso.
 *
 * Usage: npx tsx scripts/sync-turso-ufc-images.ts
 *
 * Requires TURSO_DATABASE_URL and TURSO_AUTH_TOKEN in .env.local
 */

import dotenv from "dotenv";
dotenv.config({ path: ".env.local" });
import Database from "better-sqlite3";
import { createClient } from "@libsql/client";
import path from "path";

const TURSO_URL = process.env.TURSO_DATABASE_URL;
const TURSO_TOKEN = process.env.TURSO_AUTH_TOKEN;

if (!TURSO_URL || !TURSO_TOKEN) {
  console.error("Missing TURSO_DATABASE_URL or TURSO_AUTH_TOKEN in environment.");
  process.exit(1);
}

const localDb = new Database(path.join(process.cwd(), "the-c-list.db"));
const turso = createClient({ url: TURSO_URL, authToken: TURSO_TOKEN });

async function main() {
  console.log("Syncing ufc_image_url to Turso...\n");

  // Step 1: Ensure column exists on Turso
  try {
    await turso.execute("ALTER TABLE players ADD COLUMN ufc_image_url TEXT");
    console.log("  Added ufc_image_url column to Turso players table.");
  } catch (err: unknown) {
    const msg = err instanceof Error ? err.message : String(err);
    if (msg.includes("duplicate column") || msg.includes("already exists")) {
      console.log("  Column ufc_image_url already exists on Turso.");
    } else {
      throw err;
    }
  }

  // Step 2: Read local players with ufc_image_url set
  const localRows = localDb
    .prepare("SELECT id, ufc_image_url FROM players WHERE ufc_image_url IS NOT NULL")
    .all() as { id: number; ufc_image_url: string }[];

  console.log(`  Found ${localRows.length} local players with ufc_image_url\n`);

  if (localRows.length === 0) {
    console.log("Nothing to sync.");
    localDb.close();
    return;
  }

  // Step 3: Batch update Turso
  const BATCH_SIZE = 50;
  let updated = 0;

  for (let i = 0; i < localRows.length; i += BATCH_SIZE) {
    const batch = localRows.slice(i, i + BATCH_SIZE);
    const stmts = batch.map((row) => ({
      sql: "UPDATE players SET ufc_image_url = ? WHERE id = ? AND (ufc_image_url IS NULL OR ufc_image_url != ?)",
      args: [row.ufc_image_url, row.id, row.ufc_image_url],
    }));
    const results = await turso.batch(stmts);
    updated += results.reduce((sum, r) => sum + r.rowsAffected, 0);
  }

  console.log(`  Updated ${updated} rows on Turso.`);

  // Step 4: Verify
  const tursoResult = await turso.execute(
    "SELECT COUNT(*) AS n FROM players WHERE ufc_image_url IS NOT NULL"
  );
  const tursoCount = tursoResult.rows[0]?.n as number;
  console.log(`  Turso now has ${tursoCount} players with ufc_image_url (local: ${localRows.length})`);

  localDb.close();
  console.log("\nDone.");
}

main().catch((err) => {
  console.error("Sync failed:", err);
  process.exit(1);
});
