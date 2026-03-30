import { sqliteTable, text, integer, uniqueIndex } from "drizzle-orm/sqlite-core";
import { relations } from "drizzle-orm";

export const sets = sqliteTable("sets", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  name: text("name").notNull(),
  sport: text("sport").notNull(),
  season: text("season").notNull(),
  league: text("league"),
  tier: text("tier", { enum: ["Standard", "Chrome", "Sapphire", "Premium", "Prizm"] }).notNull().default("Standard"),
  sampleImageUrl: text("sample_image_url"),
  packOdds: text("pack_odds"),
  boxConfig: text("box_config"),
  releaseDate: text("release_date"),
});

export const insertSets = sqliteTable("insert_sets", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  setId: integer("set_id")
    .notNull()
    .references(() => sets.id),
  name: text("name").notNull(),
});

export const parallels = sqliteTable("parallels", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  insertSetId: integer("insert_set_id")
    .notNull()
    .references(() => insertSets.id),
  name: text("name").notNull(),
  printRun: integer("print_run"), // null = unlimited
});

export const players = sqliteTable("players", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  setId: integer("set_id").notNull().references(() => sets.id),
  name: text("name").notNull(),
  uniqueCards: integer("unique_cards").notNull().default(0),
  totalPrintRun: integer("total_print_run").notNull().default(0),
  oneOfOnes: integer("one_of_ones").notNull().default(0),
  insertSetCount: integer("insert_set_count").notNull().default(0),
}, (t) => [
  uniqueIndex("players_set_name_unique").on(t.setId, t.name),
]);

export const playerAppearances = sqliteTable("player_appearances", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  playerId: integer("player_id")
    .notNull()
    .references(() => players.id),
  insertSetId: integer("insert_set_id")
    .notNull()
    .references(() => insertSets.id),
  cardNumber: text("card_number").notNull(),
  team: text("team"),
  isRookie: integer("is_rookie", { mode: "boolean" }).notNull().default(false),
  subsetTag: text("subset_tag"),
});

export const playerEvents = sqliteTable("player_events", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  playerId: integer("player_id").notNull().references(() => players.id),
  eventType: text("event_type", { enum: ["search", "view"] }).notNull(),
  createdAt: integer("created_at").notNull(), // Unix ms timestamp
});

export const toppsSets = sqliteTable("topps_sets", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  name: text("name").notNull(),
  sport: text("sport").notNull(),
  year: integer("year").notNull(),
  tier: text("tier", { enum: ["Standard", "Chrome", "Sapphire", "Premium", "Prizm"] }).notNull().default("Standard"),
});

export const appearanceCoPlayers = sqliteTable("appearance_co_players", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  appearanceId: integer("appearance_id")
    .notNull()
    .references(() => playerAppearances.id),
  coPlayerId: integer("co_player_id")
    .notNull()
    .references(() => players.id),
});

// Relations
export const setsRelations = relations(sets, ({ many }) => ({
  insertSets: many(insertSets),
  players: many(players),
}));

export const insertSetsRelations = relations(insertSets, ({ one, many }) => ({
  set: one(sets, { fields: [insertSets.setId], references: [sets.id] }),
  parallels: many(parallels),
  playerAppearances: many(playerAppearances),
}));

export const parallelsRelations = relations(parallels, ({ one }) => ({
  insertSet: one(insertSets, {
    fields: [parallels.insertSetId],
    references: [insertSets.id],
  }),
}));

export const playersRelations = relations(players, ({ one, many }) => ({
  set: one(sets, { fields: [players.setId], references: [sets.id] }),
  appearances: many(playerAppearances),
}));

export const playerAppearancesRelations = relations(
  playerAppearances,
  ({ one }) => ({
    player: one(players, {
      fields: [playerAppearances.playerId],
      references: [players.id],
    }),
    insertSet: one(insertSets, {
      fields: [playerAppearances.insertSetId],
      references: [insertSets.id],
    }),
  })
);
