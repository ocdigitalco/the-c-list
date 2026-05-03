/**
 * Pull all data FROM Turso INTO the local SQLite database.
 *
 * Usage: npx tsx scripts/pull-from-turso.ts
 *
 * This is the reverse of migrate-to-turso.ts. It reads all rows from
 * Turso and upserts them into the local SQLite DB using INSERT OR REPLACE.
 * It does NOT drop any local tables — existing rows are updated, new rows
 * are added.
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
localDb.pragma("journal_mode = WAL");
localDb.pragma("foreign_keys = OFF"); // Disable FK checks during bulk upsert
const turso = createClient({ url: TURSO_URL, authToken: TURSO_TOKEN });

// ── Tables in dependency order ──────────────────────────────────────────────

const TABLES = [
  "sets",                  // no FK dependencies
  "insert_sets",           // depends on sets
  "parallels",             // depends on insert_sets
  "players",               // depends on sets
  "player_appearances",    // depends on players, insert_sets
  "appearance_co_players", // depends on player_appearances, players
  "topps_sets",            // standalone
  "player_events",         // depends on players
];

const BATCH_SIZE = 1000;

// ── Pull a single table from Turso into local SQLite ────────────────────────

async function pullTable(table: string): Promise<number> {
  let totalPulled = 0;
  let offset = 0;

  // First batch — also discover columns
  const firstResult = await turso.execute({
    sql: `SELECT * FROM "${table}" LIMIT ? OFFSET ?`,
    args: [BATCH_SIZE, 0],
  });

  if (firstResult.rows.length === 0) {
    console.log(`  ${table}: 0 rows (empty on Turso)`);
    return 0;
  }

  const columns = firstResult.columns;
  const placeholders = columns.map(() => "?").join(", ");
  const insertSql = `INSERT OR REPLACE INTO "${table}" (${columns.map(c => `"${c}"`).join(", ")}) VALUES (${placeholders})`;

  const insertStmt = localDb.prepare(insertSql);
  const insertMany = localDb.transaction((rows: unknown[][]) => {
    for (const row of rows) {
      insertStmt.run(...row);
    }
  });

  // Process first batch
  const firstRows = firstResult.rows.map((row) =>
    columns.map((col) => {
      const val = row[col];
      if (val === null || val === undefined) return null;
      return val;
    })
  );
  insertMany(firstRows);
  totalPulled += firstRows.length;
  offset += BATCH_SIZE;

  // Continue fetching if there might be more
  while (firstResult.rows.length === BATCH_SIZE || offset === BATCH_SIZE) {
    if (offset === BATCH_SIZE && firstResult.rows.length < BATCH_SIZE) break;

    const result = await turso.execute({
      sql: `SELECT * FROM "${table}" LIMIT ? OFFSET ?`,
      args: [BATCH_SIZE, offset],
    });

    if (result.rows.length === 0) break;

    const rows = result.rows.map((row) =>
      columns.map((col) => {
        const val = row[col];
        if (val === null || val === undefined) return null;
        return val;
      })
    );
    insertMany(rows);
    totalPulled += rows.length;
    offset += BATCH_SIZE;

    if (result.rows.length < BATCH_SIZE) break;
  }

  console.log(`  ${table}: ${totalPulled} rows pulled`);
  return totalPulled;
}

// ── Verification ─────────────────────────────────────────────────────────────

async function verify() {
  console.log("\nVerifying row counts...");

  let allMatch = true;
  for (const table of TABLES) {
    const localCount = (localDb.prepare(`SELECT COUNT(*) AS n FROM "${table}"`).get() as { n: number }).n;
    const tursoResult = await turso.execute(`SELECT COUNT(*) AS n FROM "${table}"`);
    const tursoCount = tursoResult.rows[0]?.n as number;

    const match = localCount >= tursoCount;
    const status = localCount === tursoCount ? "OK" : localCount > tursoCount ? "LOCAL HAS MORE" : "MISMATCH";
    console.log(`  ${table}: local=${localCount} turso=${tursoCount} [${status}]`);
    if (!match) allMatch = false;
  }

  return allMatch;
}

// ── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  console.log(`Pulling data from Turso → local SQLite`);
  console.log(`Source: ${TURSO_URL}\n`);

  console.log("Pulling data...");
  for (const table of TABLES) {
    await pullTable(table);
  }

  localDb.pragma("foreign_keys = ON");
  const ok = await verify();

  localDb.close();

  if (ok) {
    console.log("\nPull complete. Local DB is up to date.");
  } else {
    console.log("\nPull complete. Some tables have fewer rows locally than on Turso — investigate.");
  }
}

main().catch((err) => {
  console.error("Pull failed:", err);
  process.exit(1);
});
