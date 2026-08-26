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
    "ALTER TABLE parallels ADD COLUMN exclusivity TEXT",
    "ALTER TABLE players ADD COLUMN subject_role TEXT NOT NULL DEFAULT 'athlete'",
    "ALTER TABLE sets ADD COLUMN created_at TEXT",
    "ALTER TABLE insert_sets ADD COLUMN is_autograph INTEGER NOT NULL DEFAULT 0",
    "ALTER TABLE sets ADD COLUMN topps_url TEXT",
    "ALTER TABLE sets ADD COLUMN related_links TEXT",
    "ALTER TABLE insert_sets ADD COLUMN is_base INTEGER NOT NULL DEFAULT 0",
    "ALTER TABLE insert_sets ADD COLUMN is_relic INTEGER NOT NULL DEFAULT 0",
    "ALTER TABLE insert_sets ADD COLUMN is_booklet INTEGER NOT NULL DEFAULT 0",
    "ALTER TABLE insert_sets ADD COLUMN print_run INTEGER",
    "ALTER TABLE insert_sets ADD COLUMN notes TEXT",
    "ALTER TABLE parallels ADD COLUMN note TEXT",
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

// Tables written by production at runtime (Turso is the source of truth).
// Never cleared, inserted, or verified here — pull-from-turso.ts syncs them down.
// break_sheets / break_sheet_prices hold user-generated break sheets saved on
// CSV export; they MUST stay here so content migrations never clobber them.
const PROD_OWNED_TABLES = ["player_events", "break_sheets", "break_sheet_prices"];

async function migrateData() {
  // Disable foreign key checks for bulk migration
  await exec("PRAGMA foreign_keys = OFF");

  console.log("\nClearing Turso tables...");
  const clearOrder = [
    "appearance_co_players", "player_appearances",
    "parallels", "players", "insert_sets", "topps_sets", "sets",
  ];
  for (const table of PROD_OWNED_TABLES) {
    console.log(`  ⏭ ${table}: skipped (production-owned table)`);
  }
  for (const table of clearOrder) {
    try {
      await exec(`DELETE FROM "${table}"`);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : String(err);
      console.warn(`  Warning clearing ${table}: ${msg}`);
    }
  }
  console.log("  Cleared all tables.");

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

  // player_events is production-owned (live analytics writes) — never pushed up.
  for (const table of PROD_OWNED_TABLES) {
    console.log(`  ⏭ ${table}: skipped (production-owned table)`);
  }

  // Re-enable foreign key checks
  await exec("PRAGMA foreign_keys = ON");
}

// ── Verification ─────────────────────────────────────────────────────────────

async function verify() {
  console.log("\nVerifying row counts...");

  const tables = [
    "sets", "insert_sets", "parallels", "players",
    "player_appearances", "appearance_co_players", "topps_sets",
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

// ── Revalidation ─────────────────────────────────────────────────────────────

async function triggerRevalidation(setSlug?: string) {
  const productionUrl = process.env.PRODUCTION_URL ?? "https://www.checklist2.com";
  const secret = process.env.REVALIDATE_SECRET;

  if (!secret) {
    console.warn("⚠ REVALIDATE_SECRET not set — skipping revalidation. Pages will refresh on natural ISR expiry.");
    return;
  }

  try {
    const body = setSlug ? { setSlug } : { paths: ["/", "/checklists", "/articles"] };
    const response = await fetch(`${productionUrl}/api/revalidate`, {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${secret}` },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const text = await response.text();
      console.warn(`⚠ Revalidation request failed (${response.status}): ${text}`);
      return;
    }

    const data = await response.json();
    console.log(`✓ Revalidated ${data.revalidated.length} path(s):`);
    data.revalidated.forEach((p: string) => console.log(`  - ${p}`));
  } catch (err) {
    console.warn("⚠ Revalidation request errored:", err);
  }
}

// ── Recompute player stats ───────────────────────────────────────────────────
// Recompute players.{unique_cards,total_print_run,one_of_ones,insert_set_count}
// on the LOCAL db BEFORE the sync, so freshly-loaded parallels are reflected in
// the rows that get pushed to Turso. Mirrors scripts/recompute-unique-cards.ts.
// Lives here — the single chokepoint every data change crosses before
// production — so a seeder that forgets to recompute can't ship stale stats
// (the bug this guards against). Idempotent: pure function of current data.
function recomputePlayerStats() {
  const players = localDb.prepare("SELECT id FROM players").all() as { id: number }[];
  // A player's cards = their own appearances UNION co-subject links (dedup).
  const getAppearances = localDb.prepare(
    `SELECT id, insert_set_id FROM player_appearances WHERE player_id = ?
     UNION
     SELECT pa.id, pa.insert_set_id
     FROM player_appearances pa
     INNER JOIN appearance_co_players cp ON cp.appearance_id = pa.id
     WHERE cp.co_player_id = ?`
  );
  const getParallels = localDb.prepare(
    "SELECT print_run FROM parallels WHERE insert_set_id = ?"
  );
  const updatePlayer = localDb.prepare(
    "UPDATE players SET unique_cards = ?, total_print_run = ?, one_of_ones = ?, insert_set_count = ? WHERE id = ?"
  );

  const tx = localDb.transaction(() => {
    for (const player of players) {
      const appearances = getAppearances.all(player.id, player.id) as {
        id: number;
        insert_set_id: number;
      }[];
      const insertSetIds = new Set(appearances.map((a) => a.insert_set_id));
      let uniqueCards = 0;
      let totalPrintRun = 0;
      let oneOfOnes = 0;
      for (const { insert_set_id } of appearances) {
        uniqueCards += 1; // base card
        const pars = getParallels.all(insert_set_id) as { print_run: number | null }[];
        for (const par of pars) {
          uniqueCards += 1;
          if (par.print_run !== null) {
            totalPrintRun += 1; // count of numbered parallels, not sum of runs
            if (par.print_run === 1) oneOfOnes += 1;
          }
        }
      }
      updatePlayer.run(uniqueCards, totalPrintRun, oneOfOnes, insertSetIds.size, player.id);
    }
  });
  tx();
  console.log(`  Recomputed stats for ${players.length} players.`);
}

// ── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  console.log(`Migrating local SQLite → Turso`);
  console.log(`Target: ${TURSO_URL}\n`);

  console.log("Recomputing player stats (local)...");
  recomputePlayerStats();

  await createSchema();
  await migrateData();
  const ok = await verify();

  localDb.close();

  if (ok) {
    console.log("\nMigration complete. All row counts match.");
  } else {
    console.error("\n⚠ MIGRATION ROW COUNT MISMATCH — investigate the table(s) above. Revalidating anyway: content is already pushed, and stale caches on top of a mismatch make things worse.");
  }

  // Revalidate cached pages — optional set slug as CLI arg.
  // Must fire even on mismatch: data has already been written to Turso.
  await triggerRevalidation(process.argv[2]);

  if (!ok) process.exit(1);
}

main().catch((err) => {
  console.error("Migration failed:", err);
  process.exit(1);
});
