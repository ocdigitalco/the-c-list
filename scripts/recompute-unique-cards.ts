/**
 * Recompute unique_cards, total_print_run, one_of_ones, and insert_set_count
 * for all players across all sets. Run after adding parallels to any set.
 *
 * Usage: npx tsx scripts/recompute-unique-cards.ts
 */
import Database from "better-sqlite3";

const db = new Database("the-c-list.db");
db.pragma("journal_mode = WAL");

const allPlayers = db
  .prepare("SELECT id, name, set_id FROM players ORDER BY set_id, id")
  .all() as { id: number; name: string; set_id: number }[];

console.log(`Recomputing stats for ${allPlayers.length} players...`);

const getAppearances = db.prepare(
  "SELECT id, insert_set_id FROM player_appearances WHERE player_id = ?"
);
const getParallels = db.prepare(
  "SELECT name, print_run FROM parallels WHERE insert_set_id = ?"
);
const updatePlayer = db.prepare(
  "UPDATE players SET unique_cards = ?, total_print_run = ?, one_of_ones = ?, insert_set_count = ? WHERE id = ?"
);

const updateTx = db.transaction(() => {
  let processed = 0;
  for (const player of allPlayers) {
    const appearances = getAppearances.all(player.id) as {
      id: number;
      insert_set_id: number;
    }[];

    const insertSetIds = new Set(appearances.map((a) => a.insert_set_id));
    let uniqueCards = 0;
    let totalPrintRun = 0;
    let oneOfOnes = 0;

    for (const { insert_set_id } of appearances) {
      uniqueCards += 1; // base card
      const pars = getParallels.all(insert_set_id) as {
        name: string;
        print_run: number | null;
      }[];
      for (const par of pars) {
        uniqueCards += 1;
        if (par.print_run !== null) {
          totalPrintRun += par.print_run;
          if (par.print_run === 1) oneOfOnes += 1;
        }
      }
    }

    updatePlayer.run(
      uniqueCards,
      totalPrintRun,
      oneOfOnes,
      insertSetIds.size,
      player.id
    );
    processed++;
    if (processed % 2000 === 0) {
      console.log(`  ${processed}/${allPlayers.length}...`);
    }
  }
  return processed;
});

const updated = updateTx();
console.log(`Updated ${updated} players.`);

// Sanity check
const stats = db
  .prepare(
    `SELECT
       MIN(unique_cards) as min_val,
       MAX(unique_cards) as max_val,
       ROUND(AVG(unique_cards), 1) as avg_val,
       COUNT(*) as total_players
     FROM players
     WHERE unique_cards > 0`
  )
  .get() as { min_val: number; max_val: number; avg_val: number; total_players: number };

console.log(`\nSanity check:`);
console.log(`  Players with cards: ${stats.total_players}`);
console.log(`  Min total cards: ${stats.min_val}`);
console.log(`  Max total cards: ${stats.max_val}`);
console.log(`  Avg total cards: ${stats.avg_val}`);

// Spot checks
const flagg = db
  .prepare("SELECT name, unique_cards FROM players WHERE name = 'Cooper Flagg' AND set_id = 35")
  .get() as { name: string; unique_cards: number } | undefined;
if (flagg) console.log(`  Cooper Flagg (Cosmic Chrome): ${flagg.unique_cards}`);

const ward = db
  .prepare("SELECT name, unique_cards FROM players WHERE name = 'Cam Ward' AND set_id = 44")
  .get() as { name: string; unique_cards: number } | undefined;
if (ward) console.log(`  Cam Ward (Chrome Football): ${ward.unique_cards}`);

db.close();
console.log("\nDone!");
