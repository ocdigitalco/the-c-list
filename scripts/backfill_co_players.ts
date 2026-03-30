/**
 * One-time backfill: populate appearance_co_players for all existing sets.
 * Safe to re-run — clears and rebuilds all co_player links.
 */
import Database from "better-sqlite3";
import { drizzle } from "drizzle-orm/better-sqlite3";
import { migrate } from "drizzle-orm/better-sqlite3/migrator";
import { eq } from "drizzle-orm";
import path from "path";
import * as schema from "../src/lib/schema";

const { playerAppearances, appearanceCoPlayers, insertSets, sets } = schema;

async function backfill() {
  const dbPath = path.join(process.cwd(), "the-c-list.db");
  const sqlite = new Database(dbPath);
  sqlite.pragma("journal_mode = WAL");
  const db = drizzle(sqlite, { schema });

  console.log("Running migrations...");
  migrate(db, { migrationsFolder: "./drizzle/migrations" });

  // Clear all existing co_player links
  db.delete(appearanceCoPlayers).run();
  console.log("Cleared existing co_player links.");

  // Fetch all appearances
  const allAppearances = db
    .select({
      id: playerAppearances.id,
      insertSetId: playerAppearances.insertSetId,
      cardNumber: playerAppearances.cardNumber,
      playerId: playerAppearances.playerId,
    })
    .from(playerAppearances)
    .all();

  // Group by insertSetId:cardNumber
  const cardGroups = new Map<string, { id: number; playerId: number }[]>();
  for (const a of allAppearances) {
    const key = `${a.insertSetId}:${a.cardNumber}`;
    if (!cardGroups.has(key)) cardGroups.set(key, []);
    cardGroups.get(key)!.push({ id: a.id, playerId: a.playerId });
  }

  let multiCardCount = 0;
  let coPlayerLinkCount = 0;

  for (const group of cardGroups.values()) {
    if (group.length < 2) continue;
    multiCardCount++;
    for (const appearance of group) {
      for (const other of group) {
        if (other.id === appearance.id) continue;
        db.insert(appearanceCoPlayers)
          .values({ appearanceId: appearance.id, coPlayerId: other.playerId })
          .run();
        coPlayerLinkCount++;
      }
    }
  }

  console.log(`Multi-player cards: ${multiCardCount}`);
  console.log(`Co-player links created: ${coPlayerLinkCount}`);

  sqlite.close();
}

backfill().catch((err) => {
  console.error(err);
  process.exit(1);
});
