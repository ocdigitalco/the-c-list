import Database from "better-sqlite3";
import { drizzle } from "drizzle-orm/better-sqlite3";
import { migrate } from "drizzle-orm/better-sqlite3/migrator";
import { eq, inArray } from "drizzle-orm";
import { readFileSync } from "fs";
import path from "path";
import * as schema from "../src/lib/schema";

const {
  sets,
  insertSets,
  parallels,
  players,
  playerAppearances,
  playerEvents,
  appearanceCoPlayers,
} = schema;

interface Parallel {
  name: string;
  print_run: number | null;
}

interface Card {
  card_number: string;
  player: string;
  team: string;
  is_rookie: boolean;
  subset: string | null;
}

interface Section {
  insert_set: string;
  parallels: Parallel[];
  cards: Card[];
}

interface PlayerAppearance {
  insert_set: string;
  card_number: string;
  team: string;
  is_rookie: boolean;
  subset_tag: string | null;
  parallels: Parallel[];
}

interface PlayerStats {
  unique_cards: number;
  total_print_run: number;
  one_of_ones: number;
  insert_sets: number;
}

interface PlayerEntry {
  player: string;
  appearances: PlayerAppearance[];
  stats: PlayerStats;
}

interface ParsedData {
  set_name: string;
  sport: string;
  season: string;
  league?: string;
  sections: Section[];
  players: PlayerEntry[];
}

function inferTier(name: string): "Standard" | "Chrome" | "Sapphire" | "Premium" | "Prizm" {
  if (/chrome sapphire|sapphire/i.test(name)) return "Sapphire";
  if (/chrome/i.test(name)) return "Chrome";
  if (/midnight|royalty|finest/i.test(name)) return "Premium";
  if (/prizm|select/i.test(name)) return "Prizm";
  return "Standard";
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function buildCoPlayerLinks(db: any, setId: number): number {
  // Delete existing co_player links for all players in this set
  const allPlayerRows = db
    .select({ id: players.id })
    .from(players)
    .where(eq(players.setId, setId))
    .all();
  const allPlayerIds = allPlayerRows.map((p: { id: number }) => p.id);

  if (allPlayerIds.length > 0) {
    // Delete links where coPlayerId is a player in this set
    db.delete(appearanceCoPlayers)
      .where(inArray(appearanceCoPlayers.coPlayerId, allPlayerIds))
      .run();
    // Delete links where the appearance belongs to a player in this set
    const allAppearanceRows = db
      .select({ id: playerAppearances.id })
      .from(playerAppearances)
      .where(inArray(playerAppearances.playerId, allPlayerIds))
      .all();
    const allAppearanceIds = allAppearanceRows.map((a: { id: number }) => a.id);
    if (allAppearanceIds.length > 0) {
      db.delete(appearanceCoPlayers)
        .where(inArray(appearanceCoPlayers.appearanceId, allAppearanceIds))
        .run();
    }
  }

  // Rebuild co_player links from all appearances in this set
  const allAppearances = db
    .select({
      id: playerAppearances.id,
      insertSetId: playerAppearances.insertSetId,
      cardNumber: playerAppearances.cardNumber,
      playerId: playerAppearances.playerId,
    })
    .from(playerAppearances)
    .innerJoin(insertSets, eq(playerAppearances.insertSetId, insertSets.id))
    .where(eq(insertSets.setId, setId))
    .all();

  const cardGroups = new Map<string, { id: number; playerId: number }[]>();
  for (const a of allAppearances) {
    const key = `${a.insertSetId}:${a.cardNumber}`;
    if (!cardGroups.has(key)) cardGroups.set(key, []);
    cardGroups.get(key)!.push({ id: a.id, playerId: a.playerId });
  }

  let count = 0;
  for (const group of cardGroups.values()) {
    if (group.length < 2) continue;
    for (const appearance of group) {
      for (const other of group) {
        if (other.id === appearance.id) continue;
        db.insert(appearanceCoPlayers)
          .values({ appearanceId: appearance.id, coPlayerId: other.playerId })
          .run();
        count++;
      }
    }
  }
  return count;
}

async function seed() {
  const dbPath = path.join(process.cwd(), "the-c-list.db");
  const sqlite = new Database(dbPath);
  sqlite.pragma("journal_mode = WAL");
  const db = drizzle(sqlite, { schema });

  // Run migrations
  console.log("Running migrations...");
  migrate(db, { migrationsFolder: "./drizzle/migrations" });

  // Load JSON — accept file path as CLI arg (first non-flag arg), default to ucc_parsed.json
  const jsonFile =
    process.argv.slice(2).find((a) => !a.startsWith("--")) ?? "ucc_parsed.json";
  const jsonPath = path.join(process.cwd(), jsonFile);
  const raw = readFileSync(jsonPath, "utf-8");
  const data: ParsedData = JSON.parse(raw);

  const isAppend = process.argv.includes("--append");

  console.log(`Seeding: ${data.set_name} (${data.season})${isAppend ? " [APPEND]" : ""}`);

  // ── APPEND MODE ────────────────────────────────────────────────────────────
  if (isAppend) {
    const existingSet = db
      .select()
      .from(sets)
      .where(eq(sets.name, data.set_name))
      .all()
      .find((s) => s.season === data.season);

    if (!existingSet) {
      throw new Error(
        `Append mode: set not found in DB: "${data.set_name}" (${data.season})`
      );
    }

    console.log(`Found existing set id=${existingSet.id}`);

    // Insert new insert_sets and parallels (skip any that already exist)
    const insertSetMap = new Map<string, number>();
    const existingInsertSetRows = db
      .select()
      .from(insertSets)
      .where(eq(insertSets.setId, existingSet.id))
      .all();
    for (const row of existingInsertSetRows) {
      insertSetMap.set(row.name, row.id);
    }

    let newInsertSetCount = 0;
    for (const section of data.sections) {
      if (insertSetMap.has(section.insert_set)) {
        console.log(`  Skipping existing insert_set: "${section.insert_set}"`);
        continue;
      }
      const [insertSet] = db
        .insert(insertSets)
        .values({ setId: existingSet.id, name: section.insert_set })
        .returning()
        .all();
      insertSetMap.set(section.insert_set, insertSet.id);
      newInsertSetCount++;

      if (section.parallels.length > 0) {
        db.insert(parallels)
          .values(
            section.parallels.map((p) => ({
              insertSetId: insertSet.id,
              name: p.name,
              printRun: p.print_run ?? null,
            }))
          )
          .run();
      }
      console.log(
        `  Insert set: "${section.insert_set}" — ${section.parallels.length} parallels, ${section.cards.length} cards`
      );
    }

    // Upsert players and insert their appearances
    let newPlayerCount = 0;
    let updatedPlayerCount = 0;
    let appearanceCount = 0;

    const existingPlayerRows = db
      .select()
      .from(players)
      .where(eq(players.setId, existingSet.id))
      .all();
    const existingPlayerMap = new Map(existingPlayerRows.map((p) => [p.name, p]));

    for (const entry of data.players) {
      let playerId: number;
      const existing = existingPlayerMap.get(entry.player);

      if (existing) {
        // Update stats by adding increments
        db.update(players)
          .set({
            uniqueCards: existing.uniqueCards + entry.stats.unique_cards,
            totalPrintRun: existing.totalPrintRun + entry.stats.total_print_run,
            oneOfOnes: existing.oneOfOnes + entry.stats.one_of_ones,
            insertSetCount: existing.insertSetCount + entry.stats.insert_sets,
          })
          .where(eq(players.id, existing.id))
          .run();
        playerId = existing.id;
        updatedPlayerCount++;
      } else {
        const [player] = db
          .insert(players)
          .values({
            setId: existingSet.id,
            name: entry.player,
            uniqueCards: entry.stats.unique_cards,
            totalPrintRun: entry.stats.total_print_run,
            oneOfOnes: entry.stats.one_of_ones,
            insertSetCount: entry.stats.insert_sets,
          })
          .returning()
          .all();
        playerId = player.id;
        newPlayerCount++;
      }

      for (const appearance of entry.appearances) {
        const insertSetId = insertSetMap.get(appearance.insert_set);
        if (!insertSetId) {
          console.warn(
            `  Warning: insert_set "${appearance.insert_set}" not found for player ${entry.player}`
          );
          continue;
        }
        db.insert(playerAppearances)
          .values({
            playerId,
            insertSetId,
            cardNumber: appearance.card_number,
            team: appearance.team,
            isRookie: appearance.is_rookie,
            subsetTag: appearance.subset_tag ?? null,
          })
          .run();
        appearanceCount++;
      }
    }

    const coPlayerLinkCount = buildCoPlayerLinks(db, existingSet.id);

    console.log(`\nDone (append)!`);
    console.log(`  New insert sets:  ${newInsertSetCount}`);
    console.log(`  New players:      ${newPlayerCount}`);
    console.log(`  Updated players:  ${updatedPlayerCount}`);
    console.log(`  Appearances:      ${appearanceCount}`);
    if (coPlayerLinkCount > 0) {
      console.log(`  Co-player links:  ${coPlayerLinkCount}`);
    }

    sqlite.close();
    return;
  }

  // ── FULL SEED MODE ─────────────────────────────────────────────────────────
  // Delete existing data for this set (by name + season), leaving other sets intact
  const existingSet = db
    .select()
    .from(sets)
    .where(eq(sets.name, data.set_name))
    .all()
    .find((s) => s.season === data.season);

  if (existingSet) {
    console.log(`Removing existing data for set id=${existingSet.id}...`);

    // Get insert_set ids for this set
    const existingInsertSets = db
      .select({ id: insertSets.id })
      .from(insertSets)
      .where(eq(insertSets.setId, existingSet.id))
      .all();
    const insertSetIds = existingInsertSets.map((r) => r.id);

    // Delete player appearances (and their co_player links) for players in this set
    const existingPlayers = db
      .select({ id: players.id })
      .from(players)
      .where(eq(players.setId, existingSet.id))
      .all();

    const existingPlayerIds = existingPlayers.map((p) => p.id);

    // Delete co_player links referencing any player in this set
    if (existingPlayerIds.length > 0) {
      db.delete(appearanceCoPlayers)
        .where(inArray(appearanceCoPlayers.coPlayerId, existingPlayerIds))
        .run();
    }

    for (const p of existingPlayers) {
      db.delete(playerAppearances)
        .where(eq(playerAppearances.playerId, p.id))
        .run();
      db.delete(playerEvents)
        .where(eq(playerEvents.playerId, p.id))
        .run();
    }

    // Delete parallels for insert sets in this set
    for (const isId of insertSetIds) {
      db.delete(parallels).where(eq(parallels.insertSetId, isId)).run();
    }

    db.delete(players).where(eq(players.setId, existingSet.id)).run();
    db.delete(insertSets).where(eq(insertSets.setId, existingSet.id)).run();
    db.delete(sets).where(eq(sets.id, existingSet.id)).run();
  }

  // Insert set
  const [set] = db
    .insert(sets)
    .values({
      name: data.set_name,
      sport: data.sport,
      season: data.season,
      league: data.league ?? null,
      tier: inferTier(data.set_name),
    })
    .returning()
    .all();

  console.log(`Created set: ${set.name} (id=${set.id})`);

  // Insert insert_sets and parallels from sections
  const insertSetMap = new Map<string, number>(); // insert_set name -> id

  for (const section of data.sections) {
    const [insertSet] = db
      .insert(insertSets)
      .values({ setId: set.id, name: section.insert_set })
      .returning()
      .all();

    insertSetMap.set(section.insert_set, insertSet.id);

    if (section.parallels.length > 0) {
      db.insert(parallels)
        .values(
          section.parallels.map((p) => ({
            insertSetId: insertSet.id,
            name: p.name,
            printRun: p.print_run ?? null,
          }))
        )
        .run();
    }

    console.log(
      `  Insert set: "${section.insert_set}" — ${section.parallels.length} parallels, ${section.cards.length} cards`
    );
  }

  // Insert players and their appearances
  let playerCount = 0;
  let appearanceCount = 0;

  for (const entry of data.players) {
    const [player] = db
      .insert(players)
      .values({
        setId: set.id,
        name: entry.player,
        uniqueCards: entry.stats.unique_cards,
        totalPrintRun: entry.stats.total_print_run,
        oneOfOnes: entry.stats.one_of_ones,
        insertSetCount: entry.stats.insert_sets,
      })
      .returning()
      .all();

    playerCount++;

    for (const appearance of entry.appearances) {
      const insertSetId = insertSetMap.get(appearance.insert_set);
      if (!insertSetId) {
        console.warn(
          `  Warning: insert_set "${appearance.insert_set}" not found for player ${entry.player}`
        );
        continue;
      }

      db.insert(playerAppearances)
        .values({
          playerId: player.id,
          insertSetId,
          cardNumber: appearance.card_number,
          team: appearance.team,
          isRookie: appearance.is_rookie,
          subsetTag: appearance.subset_tag ?? null,
        })
        .run();

      appearanceCount++;
    }
  }

  const coPlayerLinkCount = buildCoPlayerLinks(db, set.id);

  console.log(`\nDone!`);
  console.log(`  Players:          ${playerCount}`);
  console.log(`  Appearances:      ${appearanceCount}`);
  console.log(`  Insert sets:      ${insertSetMap.size}`);
  if (coPlayerLinkCount > 0) {
    console.log(`  Co-player links:  ${coPlayerLinkCount}`);
  }

  sqlite.close();
}

seed().catch((err) => {
  console.error(err);
  process.exit(1);
});
