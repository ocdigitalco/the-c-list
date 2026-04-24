/**
 * Migrate all data from local SQLite to Turso.
 *
 * Usage: npx tsx scripts/migrate-to-turso.ts
 *
 * Requires TURSO_DATABASE_URL and TURSO_AUTH_TOKEN in .env.local
 */

import dotenv from "dotenv";
dotenv.config({ path: ".env.local" });
import Database from "better-sqlite3";
import { createClient } from "@libsql/client";
import path from "path";

// ── Setup ────────────────────────────────────────────────────────────────────

const TURSO_URL = process.env.TURSO_DATABASE_URL;
const TURSO_TOKEN = process.env.TURSO_AUTH_TOKEN;

if (!TURSO_URL || !TURSO_TOKEN) {
  console.error("Missing TURSO_DATABASE_URL or TURSO_AUTH_TOKEN in environment.");
  console.error("Make sure .env.local is set up correctly.");
  process.exit(1);
}

const localDb = new Database(path.join(process.cwd(), "the-c-list.db"));
const turso = createClient({ url: TURSO_URL, authToken: TURSO_TOKEN });

// ── Helpers ──────────────────────────────────────────────────────────────────

async function exec(sql: string) {
  await turso.execute(sql);
}

async function batchInsert(
  table: string,
  rows: Record<string, unknown>[],
  batchSize = 50
) {
  if (rows.length === 0) {
    console.log(`  ${table}: 0 rows (skipped)`);
    return;
  }

  const columns = Object.keys(rows[0]);
  const placeholders = `(${columns.map(() => "?").join(", ")})`;

  let inserted = 0;
  for (let i = 0; i < rows.length; i += batchSize) {
    const batch = rows.slice(i, i + batchSize);
    const stmts = batch.map((row) => ({
      sql: `INSERT OR REPLACE INTO ${table} (${columns.join(", ")}) VALUES ${placeholders}`,
      args: columns.map((col) => {
        const val = row[col];
        if (val === undefined || val === null) return null;
        if (typeof val === "boolean") return val ? 1 : 0;
        return val as string | number;
      }),
    }));
    await turso.batch(stmts);
    inserted += batch.length;
  }
  console.log(`  ${table}: ${inserted} rows`);
}

function readAll(table: string): Record<string, unknown>[] {
  return localDb.prepare(`SELECT * FROM "${table}"`).all() as Record<string, unknown>[];
}

// ── Schema creation from current state ───────────────────────────────────────

async function createSchema() {
  console.log("Creating schema...");

  // Read the current schema from the local DB (reflects all migrations applied)
  const tables = localDb
    .prepare(
      `SELECT sql FROM sqlite_master
       WHERE type='table'
       AND name NOT LIKE 'sqlite_%'
       AND name != '__drizzle_migrations'
       ORDER BY name`
    )
    .all() as { sql: string }[];

  const indexes = localDb
    .prepare(
      `SELECT sql FROM sqlite_master
       WHERE type='index'
       AND sql IS NOT NULL
       AND name NOT LIKE 'sqlite_%'
       ORDER BY name`
    )
    .all() as { sql: string }[];

  // Create tables
  for (const { sql } of tables) {
    try {
      await exec(sql);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : String(err);
      if (msg.includes("already exists")) continue;
      console.warn(`  Warning: ${msg}`);
    }
  }

  // Ensure new columns exist on existing tables (handles schema evolution)
  const alterStmts = [
    "ALTER TABLE sets ADD COLUMN slug TEXT",
    "ALTER TABLE sets ADD COLUMN is_visible INTEGER NOT NULL DEFAULT 1",
    "ALTER TABLE players ADD COLUMN slug TEXT",
    "ALTER TABLE players ADD COLUMN image_url TEXT",
    "ALTER TABLE players ADD COLUMN sleeper_id TEXT",
  ];
  for (const stmt of alterStmts) {
    try {
      await exec(stmt);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : String(err);
      if (msg.includes("duplicate column") || msg.includes("already exists")) continue;
      // Ignore if column already exists
    }
  }

  // Create indexes
  for (const { sql } of indexes) {
    try {
      await exec(sql);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : String(err);
      if (msg.includes("already exists")) continue;
      console.warn(`  Warning: ${msg}`);
    }
  }

  console.log(`  Created ${tables.length} tables, ${indexes.length} indexes`);
}

// ── Data migration ───────────────────────────────────────────────────────────

async function migrateData() {
  console.log("\nMigrating data...");

  // Order matters: parent tables before children (foreign key dependencies)
  // 1. sets (no FK dependencies)
  await batchInsert("sets", readAll("sets"));

  // 2. insert_sets (depends on sets)
  await batchInsert("insert_sets", readAll("insert_sets"));

  // 3. parallels (depends on insert_sets)
  await batchInsert("parallels", readAll("parallels"));

  // 4. players (depends on sets)
  await batchInsert("players", readAll("players"));

  // 5. player_appearances (depends on players, insert_sets)
  await batchInsert("player_appearances", readAll("player_appearances"));

  // 6. appearance_co_players (depends on player_appearances, players)
  await batchInsert("appearance_co_players", readAll("appearance_co_players"));

  // 7. topps_sets (standalone)
  await batchInsert("topps_sets", readAll("topps_sets"));

  // 8. player_events (depends on players) — optional analytics data
  await batchInsert("player_events", readAll("player_events"));
}

// ── Verification ─────────────────────────────────────────────────────────────

async function verify() {
  console.log("\nVerifying row counts...");

  const tables = [
    "sets", "insert_sets", "parallels", "players",
    "player_appearances", "appearance_co_players", "topps_sets", "player_events",
  ];

  let allMatch = true;
  for (const table of tables) {
    const localCount = (localDb.prepare(`SELECT COUNT(*) AS n FROM "${table}"`).get() as { n: number }).n;
    const tursoResult = await turso.execute(`SELECT COUNT(*) AS n FROM "${table}"`);
    const tursoCount = tursoResult.rows[0]?.n as number;

    const match = localCount === tursoCount;
    const status = match ? "OK" : "MISMATCH";
    console.log(`  ${table}: local=${localCount} turso=${tursoCount} [${status}]`);
    if (!match) allMatch = false;
  }

  return allMatch;
}

// ── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  console.log(`Migrating local SQLite → Turso`);
  console.log(`Target: ${TURSO_URL}\n`);

  await createSchema();
  await migrateData();
  const ok = await verify();

  localDb.close();

  if (ok) {
    console.log("\nMigration complete. All row counts match.");
  } else {
    console.error("\nMigration complete but row counts do not match. Please investigate.");
    process.exit(1);
  }
}

main().catch((err) => {
  console.error("Migration failed:", err);
  process.exit(1);
});
