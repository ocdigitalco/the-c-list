import { sqliteTable, text, integer, real, uniqueIndex } from "drizzle-orm/sqlite-core";
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
  // slug: text("slug"), // Added via ALTER TABLE, not in Drizzle schema to avoid query errors on Turso pre-migration
});

export const insertSets = sqliteTable("insert_sets", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  setId: integer("set_id")
    .notNull()
    .references(() => sets.id),
  name: text("name").notNull(),
  isAutograph: integer("is_autograph", { mode: "boolean" }).notNull().default(false),
  isBase: integer("is_base", { mode: "boolean" }).notNull().default(false),
  isRelic: integer("is_relic", { mode: "boolean" }).notNull().default(false),
  isBooklet: integer("is_booklet", { mode: "boolean" }).notNull().default(false),
  printRun: integer("print_run"), // subset-level numbered parent ("all cards /X"); null = not a numbered parent
  notes: text("notes"), // subset-level provenance notes / dq
});

export const parallels = sqliteTable("parallels", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  insertSetId: integer("insert_set_id")
    .notNull()
    .references(() => insertSets.id),
  name: text("name").notNull(),
  printRun: integer("print_run"), // null = unlimited
  exclusivity: text("exclusivity"), // null = all products; e.g. "Hobby", "Delight"
  note: text("note"), // per-parallel provenance note (distinct from exclusivity)
});

export const players = sqliteTable("players", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  setId: integer("set_id").notNull().references(() => sets.id),
  name: text("name").notNull(),
  uniqueCards: integer("unique_cards").notNull().default(0),
  totalPrintRun: integer("total_print_run").notNull().default(0),
  oneOfOnes: integer("one_of_ones").notNull().default(0),
  insertSetCount: integer("insert_set_count").notNull().default(0),
  nbaPlayerId: integer("nba_player_id"),
  ufcImageUrl: text("ufc_image_url"),
  mlbPlayerId: integer("mlb_player_id"),
  subjectRole: text("subject_role", { enum: ["athlete", "coach", "celebrity", "character", "sketch_artist", "attraction"] }).notNull().default("athlete"),
  // slug: text("slug"), // Added via ALTER TABLE, not in Drizzle schema to avoid query errors on Turso pre-migration
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

// Production-owned. A saved break sheet, written at CSV-export time. Anonymous
// (no accounts, no PII — do not add IP/fingerprint fields). `config` holds the
// remaining break configuration as JSON; the headline cost/total/profit and the
// unit+quantity are first-class columns so ROI and per-case normalization are
// queryable without parsing JSON.
export const breakSheets = sqliteTable("break_sheets", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  createdAt: integer("created_at").notNull(), // Unix ms timestamp
  setSlug: text("set_slug").notNull(),
  sport: text("sport").notNull(),
  breakUnit: text("break_unit", { enum: ["cases", "boxes"] }).notNull(),
  quantity: integer("quantity").notNull(),
  cost: real("cost"), // what the breaker paid; null when not entered
  total: real("total").notNull(), // sum of per-spot prices at export time
  profit: real("profit"), // total - cost; null when cost is unknown
  config: text("config").notNull(), // JSON: the rest of the break config
});

// Production-owned. Per-spot prices for a saved sheet — one row per athlete/team
// slot. This is the FOUNDATION for a future pricing advisor (e.g. "list Judge at
// ~$500"): storing prices per subject, together with the parent sheet's unit +
// quantity, lets per-case list prices be normalized and aggregated later. No PII.
export const breakSheetPrices = sqliteTable("break_sheet_prices", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  sheetId: integer("sheet_id")
    .notNull()
    .references(() => breakSheets.id),
  subjectName: text("subject_name").notNull(),
  subjectType: text("subject_type", { enum: ["athlete", "team"] }).notNull(),
  price: real("price").notNull(),
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
