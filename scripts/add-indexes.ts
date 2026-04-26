/**
 * Add missing indexes to the local SQLite database.
 * Safe to run multiple times (uses IF NOT EXISTS).
 *
 * Usage: npx tsx scripts/add-indexes.ts
 */
import Database from "better-sqlite3";

const db = new Database("the-c-list.db");
db.pragma("journal_mode = WAL");

const indexes = [
  // Foreign keys on player_appearances (38K+ rows — most queried table)
  "CREATE INDEX IF NOT EXISTS idx_pa_player_id ON player_appearances (player_id)",
  "CREATE INDEX IF NOT EXISTS idx_pa_insert_set_id ON player_appearances (insert_set_id)",
  "CREATE INDEX IF NOT EXISTS idx_pa_is_rookie ON player_appearances (is_rookie)",

  // Foreign keys on insert_sets
  "CREATE INDEX IF NOT EXISTS idx_is_set_id ON insert_sets (set_id)",

  // Foreign keys on parallels
  "CREATE INDEX IF NOT EXISTS idx_par_insert_set_id ON parallels (insert_set_id)",

  // Foreign keys on players
  "CREATE INDEX IF NOT EXISTS idx_players_set_id ON players (set_id)",
  "CREATE INDEX IF NOT EXISTS idx_players_name ON players (name)",
  "CREATE INDEX IF NOT EXISTS idx_players_nba_player_id ON players (nba_player_id)",
  "CREATE INDEX IF NOT EXISTS idx_players_mlb_player_id ON players (mlb_player_id)",
  "CREATE INDEX IF NOT EXISTS idx_players_slug ON players (slug)",

  // Sets lookups
  "CREATE INDEX IF NOT EXISTS idx_sets_sport ON sets (sport)",
  "CREATE INDEX IF NOT EXISTS idx_sets_slug ON sets (slug)",
  "CREATE INDEX IF NOT EXISTS idx_sets_release_date ON sets (release_date)",

  // Composite index for player lookup by set + name (common pattern)
  "CREATE UNIQUE INDEX IF NOT EXISTS idx_players_set_name ON players (set_id, name)",

  // appearance_co_players foreign keys
  "CREATE INDEX IF NOT EXISTS idx_acp_appearance_id ON appearance_co_players (appearance_id)",
  "CREATE INDEX IF NOT EXISTS idx_acp_co_player_id ON appearance_co_players (co_player_id)",
];

console.log(`Adding ${indexes.length} indexes...\n`);

let added = 0;
for (const sql of indexes) {
  const name = sql.match(/idx_\w+/)?.[0] ?? sql;
  try {
    db.exec(sql);
    added++;
    console.log(`  ✓ ${name}`);
  } catch (err) {
    console.log(`  ✗ ${name}: ${err instanceof Error ? err.message : err}`);
  }
}

console.log(`\nDone. ${added}/${indexes.length} indexes applied.`);
db.close();
