/**
 * Migrate data from local SQLite to Turso.
 *
 * Usage:
 *   npx tsx scripts/migrate-to-turso.ts --set <slug>      (scoped, recommended)
 *   npx tsx scripts/migrate-to-turso.ts <slug>            (shorthand for --set)
 *   npx tsx scripts/migrate-to-turso.ts --full --confirm-outage   (whole-DB reload)
 *
 * Requires TURSO_DATABASE_URL and TURSO_AUTH_TOKEN in .env.local
 *
 * ── Scoped vs full ───────────────────────────────────────────────────────────
 * `--set <slug>` replaces exactly one set's rows ATOMICALLY in a single
 * `client.migrate()` batch (foreign_keys OFF for the batch, all-or-nothing on one
 * HTTP round trip). Production never observes a half-applied set, and there is no
 * blank window — the 16-minute outage that a failed full reload caused on 2026-11
 * cannot happen in scoped mode. Ids are preserved by NATURAL KEY (set slug,
 * insert_set/player name, athlete slug) so the production-owned tables that
 * reference them (sold_comps, player_events, break_listings) keep valid FKs even
 * though a reseed churns local autoincrement ids. A post-commit orphan check
 * confirms no prod-owned row was left dangling.
 *
 * `--full` reloads every content table. At the current size (~174k rows) it
 * fits in one atomic migrate() batch (measured safe to 250k on a prod-snapshot
 * branch), so it too runs atomically with no blank window. Only once the payload
 * exceeds FULL_ATOMIC_CEILING does it fall back to the (non-atomic,
 * brief-blank-window) clear-then-load path, which then REQUIRES
 * `--confirm-outage` so it cannot run by accident. Prefer `--set`.
 *
 * ── Canonical athletes convention (Stage 1 of athlete pages) ─────────────────
 * Every players row must carry a non-null `athlete_id` pointing at the canonical
 * `athletes` table before it is pushed. The mapping is built on the LOCAL db by
 * scripts/build-athletes.ts (idempotent: it rebuilds `athletes`, reassigns every
 * players.athlete_id from data/athlete-review-queue.csv, and writes
 * athletes.headshot_url). After seeding a NEW set, run the full post-seed chain
 * instead of bare build-athletes:
 *
 *     npx tsx scripts/post-seed.ts --set <slug>
 *
 * which does build-athletes → backfill-headshots → build-athletes, then (via its
 * own call) this migration with `--set <slug>`. This script ABORTS if any players
 * row is still missing an athlete_id, so stale/new rows can't ship unlinked.
 *
 * Review-queue actions (data/athlete-review-queue.csv, applied by build-athletes):
 *   premerge      — collapse in-set spelling twins to one player row.
 *   merge         — union rows sharing a `canonical` into one athlete (may span sports).
 *   keep_separate — no edge; one athlete per (name, sport).
 *   split_by_team — split one (name, sport) into two people by team: rows whose teams
 *                   all fall in `team_filter` become their own athlete (`canonical_slug`,
 *                   display `canonical`), with their five image-id columns cleared.
 */

import dotenv from "dotenv";
dotenv.config({ path: ".env.local" });
import Database from "better-sqlite3";
import { createClient, type InStatement } from "@libsql/client";
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

// Keep each statement's bind-parameter count well under SQLite's classic 999
// limit, so multi-row INSERTs stay portable regardless of the remote's cap.
const PARAM_CAP = 900;
// Above this many content rows, a `--full` reload is treated as too big for one
// atomic migrate() batch and must use the clear-then-load path (needs
// --confirm-outage). Measured on a prod-snapshot Turso branch: a single
// migrate() of 250k rows / 2,234 statements committed in ~8.5s with no size
// error, so the current full DB (~174k rows) goes through the atomic path and
// has no blank window. Headroom is deliberate — raise only after re-probing.
const FULL_ATOMIC_CEILING = 250_000;

type Row = Record<string, unknown>;

// ── Helpers ──────────────────────────────────────────────────────────────────

async function exec(sql: string) {
  await turso.execute(sql);
}

function readAll(table: string): Row[] {
  return localDb.prepare(`SELECT * FROM "${table}"`).all() as Row[];
}

function coerce(val: unknown): string | number | null {
  if (val === undefined || val === null) return null;
  if (typeof val === "boolean") return val ? 1 : 0;
  return val as string | number;
}

/**
 * Build multi-row INSERT (or INSERT OR REPLACE) statements for `migrate()`/`batch()`,
 * packing rows per statement so the bind-parameter count stays under PARAM_CAP.
 * All rows must share the same columns (taken from the first row).
 */
function buildInsertStmts(table: string, rows: Row[], replace = false): InStatement[] {
  if (rows.length === 0) return [];
  const columns = Object.keys(rows[0]);
  const rowsPerStmt = Math.max(1, Math.floor(PARAM_CAP / columns.length));
  const verb = replace ? "INSERT OR REPLACE" : "INSERT";
  const tuple = `(${columns.map(() => "?").join(", ")})`;
  const stmts: InStatement[] = [];
  for (let i = 0; i < rows.length; i += rowsPerStmt) {
    const chunk = rows.slice(i, i + rowsPerStmt);
    const sql =
      `${verb} INTO "${table}" (${columns.map((c) => `"${c}"`).join(", ")}) VALUES ` +
      chunk.map(() => tuple).join(", ");
    const args: (string | number | null)[] = [];
    for (const row of chunk) for (const col of columns) args.push(coerce(row[col]));
    stmts.push({ sql, args });
  }
  return stmts;
}

// Chunked INSERT OR REPLACE used by the --full fallback path (one batch per chunk).
async function batchInsert(table: string, rows: Row[], batchSize = 50) {
  if (rows.length === 0) {
    console.log(`  ${table}: 0 rows (skipped)`);
    return;
  }
  const columns = Object.keys(rows[0]);
  const placeholders = `(${columns.map(() => "?").join(", ")})`;
  let inserted = 0;
  for (let i = 0; i < rows.length; i += batchSize) {
    const chunk = rows.slice(i, i + batchSize);
    const stmts = chunk.map((row) => ({
      sql: `INSERT OR REPLACE INTO ${table} (${columns.join(", ")}) VALUES ${placeholders}`,
      args: columns.map((col) => coerce(row[col])),
    }));
    await turso.batch(stmts);
    inserted += chunk.length;
  }
  console.log(`  ${table}: ${inserted} rows`);
}

// ── Schema creation from current state ───────────────────────────────────────

async function createSchema() {
  console.log("Ensuring schema...");

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
    "ALTER TABLE athletes ADD COLUMN headshot_url TEXT",
    "ALTER TABLE insert_sets ADD COLUMN is_autograph INTEGER NOT NULL DEFAULT 0",
    "ALTER TABLE sets ADD COLUMN topps_url TEXT",
    "ALTER TABLE sets ADD COLUMN related_links TEXT",
    "ALTER TABLE sets ADD COLUMN video_url TEXT",
    "ALTER TABLE insert_sets ADD COLUMN is_base INTEGER NOT NULL DEFAULT 0",
    "ALTER TABLE insert_sets ADD COLUMN is_relic INTEGER NOT NULL DEFAULT 0",
    "ALTER TABLE insert_sets ADD COLUMN is_booklet INTEGER NOT NULL DEFAULT 0",
    "ALTER TABLE insert_sets ADD COLUMN print_run INTEGER",
    "ALTER TABLE insert_sets ADD COLUMN notes TEXT",
    "ALTER TABLE parallels ADD COLUMN note TEXT",
    "ALTER TABLE player_appearances ADD COLUMN formats TEXT",
    // sold_comps gained boa_hydrated after its initial create (0025); ensure
    // pre-existing Turso tables get the column (duplicate-column is ignored).
    "ALTER TABLE sold_comps ADD COLUMN boa_hydrated INTEGER",
    // sold_comps_usage gained unreleased (0029); release-date guard counts
    // unreleased hits here. Duplicate-column is ignored.
    "ALTER TABLE sold_comps_usage ADD COLUMN unreleased INTEGER NOT NULL DEFAULT 0",
    // Production-owned table (excluded from data sync below). Ensure Turso has
    // the schema even though we never push rows into it.
    `CREATE TABLE IF NOT EXISTS set_alerts (
      id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      email TEXT NOT NULL,
      set_id INTEGER NOT NULL REFERENCES sets(id),
      token TEXT NOT NULL,
      created_at TEXT NOT NULL DEFAULT (datetime('now')),
      notified_at TEXT
    )`,
    "CREATE UNIQUE INDEX IF NOT EXISTS set_alerts_token_unique ON set_alerts (token)",
    "CREATE UNIQUE INDEX IF NOT EXISTS set_alerts_email_set_unq ON set_alerts (email, set_id)",
    "CREATE INDEX IF NOT EXISTS idx_set_alerts_set_notified ON set_alerts (set_id, notified_at)",
    // Production-owned table (excluded from data sync below). Ensure Turso has
    // the schema; the cron / refresh script populates it directly on Turso.
    `CREATE TABLE IF NOT EXISTS ebay_box_offers (
      id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      set_id INTEGER NOT NULL REFERENCES sets(id),
      format TEXT NOT NULL,
      query TEXT,
      fetched_at TEXT,
      offers TEXT,
      result_count INTEGER,
      error TEXT
    )`,
    "CREATE UNIQUE INDEX IF NOT EXISTS ebay_box_offers_set_format_unq ON ebay_box_offers (set_id, format)",
    // Production-owned table (excluded from data sync below). Ensure Turso has
    // the schema; /api/consent writes rows directly on Turso and they never
    // exist locally. Stores no IP / UA / device / geo / referrer / headers.
    `CREATE TABLE IF NOT EXISTS consent_events (
      id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      consent_id TEXT NOT NULL,
      ts TEXT NOT NULL,
      notice_version INTEGER NOT NULL,
      analytics INTEGER NOT NULL,
      advertising INTEGER NOT NULL,
      gpc INTEGER NOT NULL,
      source TEXT NOT NULL
    )`,
    "CREATE INDEX IF NOT EXISTS idx_consent_events_consent_id ON consent_events (consent_id)",
    // Production-owned tables (excluded from data sync below). Ensure Turso has
    // the schema; /api/sold-comps writes rows directly on Turso and they never
    // need to exist locally except for dev. Prices in cents.
    `CREATE TABLE IF NOT EXISTS sold_comps (
      id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      set_id INTEGER NOT NULL REFERENCES sets(id),
      insert_set_id INTEGER NOT NULL REFERENCES insert_sets(id),
      card_number TEXT NOT NULL,
      player_id INTEGER NOT NULL REFERENCES players(id),
      grade_filter TEXT NOT NULL DEFAULT 'raw',
      keyword TEXT,
      last_sold_price_cents INTEGER,
      last_sold_at TEXT,
      last_sold_url TEXT,
      last_sold_type TEXT,
      median_30d_cents INTEGER,
      count_30d INTEGER,
      low_30d_cents INTEGER,
      high_30d_cents INTEGER,
      boa_hydrated INTEGER,
      raw_items_json TEXT,
      fetched_at TEXT,
      source TEXT NOT NULL DEFAULT 'sold-comps'
    )`,
    "CREATE UNIQUE INDEX IF NOT EXISTS sold_comps_key_unq ON sold_comps (set_id, insert_set_id, card_number, player_id, grade_filter)",
    `CREATE TABLE IF NOT EXISTS sold_comps_usage (
      day TEXT PRIMARY KEY NOT NULL,
      calls INTEGER NOT NULL DEFAULT 0,
      credits_used_estimate INTEGER NOT NULL DEFAULT 0,
      unreleased INTEGER NOT NULL DEFAULT 0,
      last_x_usage_json TEXT
    )`,
    `CREATE TABLE IF NOT EXISTS sold_comps_requests (
      id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      ip_hash TEXT NOT NULL,
      requested_at TEXT NOT NULL,
      cache_key TEXT NOT NULL
    )`,
    "CREATE INDEX IF NOT EXISTS sold_comps_requests_time_idx ON sold_comps_requests (requested_at)",
    "CREATE INDEX IF NOT EXISTS sold_comps_requests_ip_idx ON sold_comps_requests (ip_hash)",
    // Production-owned tables (excluded from data sync below). Ensure Turso has
    // the schema; the cron / on-demand /api/breaks writes rows directly on Turso.
    // Live eBay break spots (category 261334), grouped by seller at read time.
    `CREATE TABLE IF NOT EXISTS break_listings (
      id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      source TEXT NOT NULL DEFAULT 'ebay',
      set_id INTEGER NOT NULL REFERENCES sets(id),
      item_id TEXT NOT NULL,
      seller TEXT,
      seller_feedback_pct REAL,
      title TEXT NOT NULL,
      price_cents INTEGER,
      currency TEXT NOT NULL DEFAULT 'USD',
      buying_option TEXT,
      format_guess TEXT,
      matched_player_ids TEXT,
      item_url TEXT,
      item_web_url TEXT,
      image_url TEXT,
      listed_at TEXT,
      first_seen_at TEXT,
      fetched_at TEXT NOT NULL,
      active INTEGER NOT NULL DEFAULT 1
    )`,
    "CREATE UNIQUE INDEX IF NOT EXISTS break_listings_set_item_unq ON break_listings (set_id, item_id)",
    "CREATE INDEX IF NOT EXISTS break_listings_set_idx ON break_listings (set_id, active)",
    `CREATE TABLE IF NOT EXISTS break_refresh_state (
      set_id INTEGER PRIMARY KEY NOT NULL REFERENCES sets(id),
      last_fetched_at TEXT,
      last_result_count INTEGER,
      last_error TEXT
    )`,
    // Canonical athlete identity (0028). `athletes` is also picked up by the
    // table loop above (new table); listed here so the ALTER + indexes land on a
    // pre-existing Turso `players`. ALTER must precede its index (a swallowed
    // "no such column" would otherwise skip it). Rows are migrated below.
    `CREATE TABLE IF NOT EXISTS athletes (
      id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      slug TEXT NOT NULL,
      name TEXT NOT NULL,
      sport TEXT NOT NULL,
      subject_role TEXT NOT NULL,
      page_kind TEXT NOT NULL,
      aliases TEXT,
      set_count INTEGER NOT NULL DEFAULT 0,
      card_count INTEGER NOT NULL DEFAULT 0,
      first_year INTEGER,
      rookie_year INTEGER,
      created_at TEXT
    )`,
    "CREATE UNIQUE INDEX IF NOT EXISTS athletes_slug_unq ON athletes (slug)",
    "ALTER TABLE players ADD COLUMN athlete_id INTEGER REFERENCES athletes(id)",
    "CREATE INDEX IF NOT EXISTS players_athlete_idx ON players (athlete_id)",
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

  console.log(`  Schema ensured (${tables.length} tables, ${indexes.length} indexes).`);
}

// Tables written by production at runtime (Turso is the source of truth).
// Never cleared, inserted, or verified here — pull-from-turso.ts syncs them down.
// break_sheets / break_sheet_prices hold user-generated break sheets saved on
// CSV export; they MUST stay here so content migrations never clobber them.
const PROD_OWNED_TABLES = ["player_events", "break_sheets", "break_sheet_prices", "set_alerts", "ebay_box_offers", "consent_events", "sold_comps", "sold_comps_usage", "sold_comps_requests", "break_listings", "break_refresh_state"];

// Content tables, child→parent (clear order for --full).
const CONTENT_CLEAR_ORDER = [
  "appearance_co_players", "player_appearances",
  "parallels", "players", "athletes", "insert_sets", "topps_sets", "sets",
];

// ── Orphan check (prod-owned FK integrity) ───────────────────────────────────
// Counts prod-owned rows whose FK no longer resolves. Scoped mode preserves ids
// by natural key so it should never INCREASE these; a removed player/insert_set
// that still has market data can, and that must be surfaced loudly (ruling 1).

const ORPHAN_QUERIES: { label: string; sql: string }[] = [
  { label: "sold_comps.set_id→sets", sql: `SELECT COUNT(*) n FROM sold_comps sc LEFT JOIN sets s ON s.id=sc.set_id WHERE s.id IS NULL` },
  { label: "sold_comps.insert_set_id→insert_sets", sql: `SELECT COUNT(*) n FROM sold_comps sc LEFT JOIN insert_sets i ON i.id=sc.insert_set_id WHERE i.id IS NULL` },
  { label: "sold_comps.player_id→players", sql: `SELECT COUNT(*) n FROM sold_comps sc LEFT JOIN players p ON p.id=sc.player_id WHERE p.id IS NULL` },
  { label: "player_events.player_id→players", sql: `SELECT COUNT(*) n FROM player_events pe LEFT JOIN players p ON p.id=pe.player_id WHERE p.id IS NULL` },
  { label: "break_listings.set_id→sets", sql: `SELECT COUNT(*) n FROM break_listings bl LEFT JOIN sets s ON s.id=bl.set_id WHERE s.id IS NULL` },
];

async function countOrphans(): Promise<Record<string, number>> {
  const out: Record<string, number> = {};
  for (const { label, sql } of ORPHAN_QUERIES) {
    try {
      out[label] = Number((await turso.execute(sql)).rows[0]?.n ?? 0);
    } catch {
      out[label] = -1; // table missing (e.g. fresh test replica) — ignore in diff
    }
  }
  return out;
}

// ── Scoped sync (one set, atomic) ────────────────────────────────────────────

type SyncResult = { ok: boolean; committed: boolean };
const ABORT: SyncResult = { ok: false, committed: false };

async function migrateSet(slug: string): Promise<SyncResult> {
  console.log(`\nScoped sync: set "${slug}"`);

  // ---- LOCAL read ----------------------------------------------------------
  const localSet = localDb.prepare(`SELECT * FROM sets WHERE slug = ?`).get(slug) as Row | undefined;
  if (!localSet) {
    console.error(`✗ No local set with slug "${slug}". Nothing to push.`);
    return ABORT;
  }
  const localSetId = Number(localSet.id);

  const localInsertSets = localDb.prepare(`SELECT * FROM insert_sets WHERE set_id = ?`).all(localSetId) as Row[];
  const localPlayers = localDb.prepare(`SELECT * FROM players WHERE set_id = ?`).all(localSetId) as Row[];
  const localInsertSetIds = localInsertSets.map((r) => Number(r.id));
  const localPlayerIds = localPlayers.map((r) => Number(r.id));

  const inParams = (ids: number[]) => ids.map(() => "?").join(",");
  const localParallels = localInsertSetIds.length
    ? (localDb.prepare(`SELECT * FROM parallels WHERE insert_set_id IN (${inParams(localInsertSetIds)})`).all(...localInsertSetIds) as Row[])
    : [];
  const localAppearances = localPlayerIds.length
    ? (localDb.prepare(`SELECT * FROM player_appearances WHERE player_id IN (${inParams(localPlayerIds)})`).all(...localPlayerIds) as Row[])
    : [];
  const localAppearanceIds = localAppearances.map((r) => Number(r.id));
  const localCoPlayers = localAppearanceIds.length
    ? (localDb.prepare(`SELECT * FROM appearance_co_players WHERE appearance_id IN (${inParams(localAppearanceIds)})`).all(...localAppearanceIds) as Row[])
    : [];

  // Athletes touched by this set = the athletes its players point at.
  const touchedAthleteIds = Array.from(new Set(localPlayers.map((p) => Number(p.athlete_id)).filter((n) => Number.isFinite(n))));
  if (localPlayers.some((p) => p.athlete_id == null)) {
    console.error(`✗ Some players in "${slug}" have a NULL athlete_id — run build-athletes first.`);
    return ABORT;
  }
  const localTouchedAthletes = touchedAthleteIds.length
    ? (localDb.prepare(`SELECT * FROM athletes WHERE id IN (${inParams(touchedAthleteIds)})`).all(...touchedAthleteIds) as Row[])
    : [];
  const touchedSlugs = new Set(localTouchedAthletes.map((a) => String(a.slug)));

  // Guard: insert_set names unique within the set (natural key).
  const isNames = localInsertSets.map((r) => String(r.name));
  if (new Set(isNames).size !== isNames.length) {
    console.error(`✗ Duplicate insert_set name within set "${slug}" — natural-key sync needs unique names.`);
    return ABORT;
  }

  console.log(`  local: ${localInsertSets.length} insert_sets, ${localPlayers.length} players, ${localParallels.length} parallels, ${localAppearances.length} appearances, ${localCoPlayers.length} co-players, ${touchedSlugs.size} athletes touched`);

  // ---- TURSO read: resolve stable target ids by natural key ----------------
  const tRows = async (sql: string, args: (string | number)[] = []) =>
    (await turso.execute({ sql, args })).rows as unknown as Row[];

  const tSet = (await tRows(`SELECT id FROM sets WHERE slug = ?`, [slug]))[0];
  const isNewSet = !tSet;

  const maxId = async (table: string) =>
    Number((await turso.execute(`SELECT COALESCE(MAX(id),0) m FROM "${table}"`)).rows[0]?.m ?? 0);
  const next = {
    sets: (await maxId("sets")) + 1,
    insert_sets: (await maxId("insert_sets")) + 1,
    players: (await maxId("players")) + 1,
    parallels: (await maxId("parallels")) + 1,
    player_appearances: (await maxId("player_appearances")) + 1,
    appearance_co_players: (await maxId("appearance_co_players")) + 1,
    athletes: (await maxId("athletes")) + 1,
  };
  const alloc = (t: keyof typeof next) => next[t]++;

  const tursoSetId = isNewSet ? alloc("sets") : Number(tSet.id);

  // Existing per-set rows on Turso, keyed by natural key → stable id.
  const tInsertSets = isNewSet ? [] : await tRows(`SELECT id, name FROM insert_sets WHERE set_id = ?`, [tursoSetId]);
  const tPlayers = isNewSet ? [] : await tRows(`SELECT id, name FROM players WHERE set_id = ?`, [tursoSetId]);
  const tInsertSetByName = new Map(tInsertSets.map((r) => [String(r.name), Number(r.id)]));
  const tPlayerByName = new Map(tPlayers.map((r) => [String(r.name), Number(r.id)]));

  // Athletes: match by slug across the whole table (global identity).
  const tAthletes = await tRows(`SELECT id, slug FROM athletes`);
  const tAthleteBySlug = new Map(tAthletes.map((r) => [String(r.slug), Number(r.id)]));

  // ---- Drift check (ruling 2): untouched athletes must match by slug+stats --
  if (!(await driftCheckAthletes(touchedSlugs))) return ABORT;

  // ---- Build id maps local→turso ------------------------------------------
  const insertSetMap = new Map<number, number>();
  for (const is of localInsertSets) {
    const name = String(is.name);
    insertSetMap.set(Number(is.id), tInsertSetByName.get(name) ?? alloc("insert_sets"));
  }
  const athleteMap = new Map<number, number>();
  for (const a of localTouchedAthletes) {
    const slugA = String(a.slug);
    athleteMap.set(Number(a.id), tAthleteBySlug.get(slugA) ?? alloc("athletes"));
  }
  const playerMap = new Map<number, number>();
  for (const p of localPlayers) {
    const name = String(p.name);
    playerMap.set(Number(p.id), tPlayerByName.get(name) ?? alloc("players"));
  }
  const appearanceMap = new Map<number, number>();
  for (const ap of localAppearances) appearanceMap.set(Number(ap.id), alloc("player_appearances"));

  // Removed rows: present on Turso for this set, gone locally (by name).
  const localInsertSetNames = new Set(isNames);
  const localPlayerNames = new Set(localPlayers.map((p) => String(p.name)));
  const removedInsertSetIds = tInsertSets.filter((r) => !localInsertSetNames.has(String(r.name))).map((r) => Number(r.id));
  const removedPlayerIds = tPlayers.filter((r) => !localPlayerNames.has(String(r.name))).map((r) => Number(r.id));
  if (removedInsertSetIds.length || removedPlayerIds.length) {
    console.log(`  removing ${removedPlayerIds.length} player(s) and ${removedInsertSetIds.length} insert_set(s) no longer in local (prod market rows referencing them, if any, will be reported by the orphan check)`);
  }

  // Remap guards: every FK we write must resolve.
  for (const ap of localAppearances) {
    if (!playerMap.has(Number(ap.player_id)) || !insertSetMap.has(Number(ap.insert_set_id))) {
      console.error(`✗ appearance ${ap.id} references a player/insert_set outside set "${slug}".`); return ABORT;
    }
  }
  for (const cp of localCoPlayers) {
    if (!appearanceMap.has(Number(cp.appearance_id)) || !playerMap.has(Number(cp.co_player_id))) {
      console.error(`✗ co-player link ${cp.id} references an appearance/player outside set "${slug}".`); return ABORT;
    }
  }

  // ---- Build the atomic batch ---------------------------------------------
  const remap = (row: Row, overrides: Row): Row => ({ ...row, ...overrides });

  const setRow = remap(localSet, { id: tursoSetId });
  const insertSetRows = localInsertSets.map((r) => remap(r, { id: insertSetMap.get(Number(r.id)), set_id: tursoSetId }));
  const athleteRows = localTouchedAthletes.map((r) => remap(r, { id: athleteMap.get(Number(r.id)) }));
  const playerRows = localPlayers.map((r) => remap(r, { id: playerMap.get(Number(r.id)), set_id: tursoSetId, athlete_id: athleteMap.get(Number(r.athlete_id)) }));
  const parallelRows = localParallels.map((r) => remap(r, { id: alloc("parallels"), insert_set_id: insertSetMap.get(Number(r.insert_set_id)) }));
  const appearanceRows = localAppearances.map((r) => remap(r, { id: appearanceMap.get(Number(r.id)), player_id: playerMap.get(Number(r.player_id)), insert_set_id: insertSetMap.get(Number(r.insert_set_id)) }));
  const coPlayerRows = localCoPlayers.map((r) => remap(r, { id: alloc("appearance_co_players"), appearance_id: appearanceMap.get(Number(r.appearance_id)), co_player_id: playerMap.get(Number(r.co_player_id)) }));

  const stmts: InStatement[] = [];

  // 1) Delete this set's content leaves + any removed parents.
  //    (migrate() runs with FK OFF, so delete order is for clarity only.)
  stmts.push({ sql: `DELETE FROM appearance_co_players WHERE appearance_id IN (SELECT id FROM player_appearances WHERE player_id IN (SELECT id FROM players WHERE set_id = ?))`, args: [tursoSetId] });
  stmts.push({ sql: `DELETE FROM player_appearances WHERE player_id IN (SELECT id FROM players WHERE set_id = ?)`, args: [tursoSetId] });
  stmts.push({ sql: `DELETE FROM parallels WHERE insert_set_id IN (SELECT id FROM insert_sets WHERE set_id = ?)`, args: [tursoSetId] });
  if (removedPlayerIds.length) stmts.push({ sql: `DELETE FROM players WHERE id IN (${removedPlayerIds.map(() => "?").join(",")})`, args: removedPlayerIds });
  if (removedInsertSetIds.length) stmts.push({ sql: `DELETE FROM insert_sets WHERE id IN (${removedInsertSetIds.map(() => "?").join(",")})`, args: removedInsertSetIds });

  // 2) Upsert parents (preserve/allocate ids), 3) insert fresh leaves.
  stmts.push(...buildInsertStmts("sets", [setRow], true));
  stmts.push(...buildInsertStmts("insert_sets", insertSetRows, true));
  stmts.push(...buildInsertStmts("athletes", athleteRows, true));
  stmts.push(...buildInsertStmts("players", playerRows, true));
  stmts.push(...buildInsertStmts("parallels", parallelRows));
  stmts.push(...buildInsertStmts("player_appearances", appearanceRows));
  stmts.push(...buildInsertStmts("appearance_co_players", coPlayerRows));

  console.log(`  batch: ${stmts.length} statements (${isNewSet ? "NEW set" : "existing set, ids preserved"})`);

  // ---- Orphan baseline, atomic commit, orphan recheck ----------------------
  const before = await countOrphans();
  try {
    await turso.migrate(stmts);
  } catch (err) {
    console.error(`✗ Atomic batch FAILED and rolled back — Turso unchanged. ${err instanceof Error ? err.message : String(err)}`);
    return ABORT;
  }
  console.log("  ✓ batch committed atomically (foreign_keys off for the transaction).");

  const ok = await verifyScoped(slug, tursoSetId, {
    insertSets: localInsertSets.length, players: localPlayers.length,
    parallels: localParallels.length, appearances: localAppearances.length,
  });
  const orphansClean = await reportOrphans(before);
  return { ok: ok && orphansClean, committed: true };
}

// Drift check: for athletes NOT touched by this set, local and Turso must agree
// on slug membership and content-derived stats. Touched athletes are being
// rewritten, so they're exempt. Ids are NOT compared (they churn freely).
async function driftCheckAthletes(touchedSlugs: Set<string>): Promise<boolean> {
  const cols = "slug, name, sport, subject_role, page_kind, aliases, set_count, card_count, first_year, rookie_year";
  const key = (r: Row) => [r.name, r.sport, r.subject_role, r.page_kind, r.aliases, r.set_count, r.card_count, r.first_year, r.rookie_year].map((v) => v ?? "∅").join("│");
  const local = new Map<string, Row>();
  for (const r of localDb.prepare(`SELECT ${cols} FROM athletes`).all() as Row[]) local.set(String(r.slug), r);
  const remote = new Map<string, Row>();
  try {
    for (const r of (await turso.execute(`SELECT ${cols} FROM athletes`)).rows as unknown as Row[]) remote.set(String(r.slug), r);
  } catch {
    console.log("  drift check: athletes table empty/absent on target (fresh replica) — skipped.");
    return true;
  }
  const allSlugs = new Set([...local.keys(), ...remote.keys()]);
  const issues: string[] = [];
  for (const slug of allSlugs) {
    if (touchedSlugs.has(slug)) continue; // being rewritten
    const l = local.get(slug), r = remote.get(slug);
    if (!l) { issues.push(`only-on-turso: ${slug}`); continue; }
    if (!r) { issues.push(`only-on-local: ${slug}`); continue; }
    if (key(l) !== key(r)) issues.push(`stats-differ: ${slug}`);
  }
  if (issues.length) {
    console.error(`✗ DRIFT: ${issues.length} untouched athlete(s) differ between local and Turso — local content is out of sync with production for sets other than this one. Run a full reload (\`--full --confirm-outage\`) instead of a scoped push.`);
    for (const i of issues.slice(0, 15)) console.error(`    ${i}`);
    if (issues.length > 15) console.error(`    …and ${issues.length - 15} more`);
    return false;
  }
  console.log(`  drift check: OK (${allSlugs.size - touchedSlugs.size} untouched athletes match).`);
  return true;
}

async function verifyScoped(slug: string, tursoSetId: number, local: { insertSets: number; players: number; parallels: number; appearances: number }): Promise<boolean> {
  const n = async (sql: string, args: (string | number)[] = []) => Number((await turso.execute({ sql, args })).rows[0]?.n ?? -1);
  const checks: [string, number, number][] = [
    ["insert_sets", local.insertSets, await n(`SELECT COUNT(*) n FROM insert_sets WHERE set_id = ?`, [tursoSetId])],
    ["players", local.players, await n(`SELECT COUNT(*) n FROM players WHERE set_id = ?`, [tursoSetId])],
    ["parallels", local.parallels, await n(`SELECT COUNT(*) n FROM parallels WHERE insert_set_id IN (SELECT id FROM insert_sets WHERE set_id = ?)`, [tursoSetId])],
    ["player_appearances", local.appearances, await n(`SELECT COUNT(*) n FROM player_appearances WHERE player_id IN (SELECT id FROM players WHERE set_id = ?)`, [tursoSetId])],
  ];
  console.log("\nVerifying set row counts...");
  let allMatch = true;
  for (const [t, l, r] of checks) {
    const match = l === r;
    console.log(`  ${t}: local=${l} turso=${r} [${match ? "OK" : "MISMATCH"}]`);
    if (!match) allMatch = false;
  }
  return allMatch;
}

async function reportOrphans(before: Record<string, number>): Promise<boolean> {
  const after = await countOrphans();
  console.log("\nOrphan check (prod-owned FK integrity)...");
  let clean = true;
  for (const { label } of ORPHAN_QUERIES) {
    const b = before[label], a = after[label];
    if (a < 0) { console.log(`  ${label}: (table absent, skipped)`); continue; }
    const delta = a - b;
    const flag = delta > 0 ? "  ⚠ NEW ORPHANS" : "";
    console.log(`  ${label}: ${a}${delta !== 0 ? ` (was ${b}, Δ${delta >= 0 ? "+" : ""}${delta})` : ` (baseline, unchanged)`}${flag}`);
    if (delta > 0) clean = false;
  }
  if (!clean) {
    console.error("✗ This push created dangling prod-owned rows — a set/insert_set/player with market data was removed or renamed. Investigate before relying on those rows.");
  } else {
    console.log("  ✓ No new orphans (pre-existing baseline left as-is).");
  }
  return clean;
}

// ── Full reload (whole DB) ───────────────────────────────────────────────────

async function migrateFull(confirmOutage: boolean): Promise<SyncResult> {
  const totalRows = CONTENT_CLEAR_ORDER.reduce(
    (sum, t) => sum + Number((localDb.prepare(`SELECT COUNT(*) n FROM "${t}"`).get() as { n: number }).n), 0);
  const atomic = totalRows <= FULL_ATOMIC_CEILING;

  if (!atomic && !confirmOutage) {
    console.error(
      `\n✗ Full reload of ${totalRows} rows is too large for one atomic batch, so it uses the\n` +
      `  clear-then-load path, which briefly blanks live checklists. Re-run with:\n` +
      `      npx tsx scripts/migrate-to-turso.ts --full --confirm-outage\n` +
      `  (Prefer \`--set <slug>\` — scoped pushes are always atomic and have no blank window.)`);
    return ABORT;
  }

  const order = [...CONTENT_CLEAR_ORDER].reverse(); // parent→child for insert
  for (const table of PROD_OWNED_TABLES) console.log(`  ⏭ ${table}: skipped (production-owned table)`);

  if (atomic) {
    console.log(`\nFull reload (atomic, ${totalRows} rows in one migrate() batch)...`);
    const stmts: InStatement[] = CONTENT_CLEAR_ORDER.map((t) => ({ sql: `DELETE FROM "${t}"`, args: [] }));
    for (const table of order) stmts.push(...buildInsertStmts(table, readAll(table)));
    await turso.migrate(stmts);
    console.log("  ✓ committed atomically.");
  } else {
    console.log(`\nFull reload (--confirm-outage; clear-then-load, brief blank window)...`);
    const clearScript = "PRAGMA foreign_keys=OFF;\n" + CONTENT_CLEAR_ORDER.map((t) => `DELETE FROM "${t}";`).join("\n");
    try {
      await turso.executeMultiple(clearScript);
    } catch (err: unknown) {
      console.warn(`  executeMultiple clear failed (${err instanceof Error ? err.message : String(err)}); per-table fallback.`);
      for (const table of CONTENT_CLEAR_ORDER) {
        try { await exec(`DELETE FROM "${table}"`); } catch (e: unknown) { console.warn(`  Warning clearing ${table}: ${e instanceof Error ? e.message : String(e)}`); }
      }
    }
    console.log("  Cleared content tables.");
    for (const table of order) await batchInsert(table, readAll(table));
    await exec("PRAGMA foreign_keys = ON");
  }
  return { ok: await verifyFull(), committed: true };
}

async function verifyFull(): Promise<boolean> {
  console.log("\nVerifying row counts...");
  let allMatch = true;
  for (const table of [...CONTENT_CLEAR_ORDER].reverse()) {
    const localCount = (localDb.prepare(`SELECT COUNT(*) AS n FROM "${table}"`).get() as { n: number }).n;
    const tursoCount = Number((await turso.execute(`SELECT COUNT(*) AS n FROM "${table}"`)).rows[0]?.n);
    const match = localCount === tursoCount;
    console.log(`  ${table}: local=${localCount} turso=${tursoCount} [${match ? "OK" : "MISMATCH"}]`);
    if (!match) allMatch = false;
  }
  return allMatch;
}

// ── Revalidation ─────────────────────────────────────────────────────────────

async function triggerRevalidation(setSlug?: string, athletePaths: string[] = []) {
  const productionUrl = process.env.PRODUCTION_URL ?? "https://www.checklist2.com";
  const secret = process.env.REVALIDATE_SECRET;

  if (!secret) {
    console.warn("⚠ REVALIDATE_SECRET not set — skipping revalidation. Pages will refresh on natural ISR expiry.");
    return;
  }

  try {
    const body = setSlug
      ? { setSlug, paths: athletePaths }
      : { paths: ["/", "/checklists", "/articles"] };
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
      const appearances = getAppearances.all(player.id, player.id) as { id: number; insert_set_id: number }[];
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

// Build a set's athlete master-page paths (for on-demand revalidation).
function athletePathsForSet(slug: string): string[] {
  const KIND_SEG: Record<string, string | null> = {
    player: "athletes", character: "characters", person: "people", team: "teams", none: null,
  };
  try {
    const rows = localDb
      .prepare(
        `SELECT DISTINCT a.slug AS slug, a.page_kind AS page_kind
         FROM athletes a
         JOIN players p ON p.athlete_id = a.id
         JOIN sets s ON s.id = p.set_id
         WHERE s.slug = ? AND a.page_kind != 'none'`
      )
      .all(slug) as { slug: string; page_kind: string }[];
    return rows
      .map((r) => { const seg = KIND_SEG[r.page_kind]; return seg ? `/${seg}/${r.slug}` : null; })
      .filter((p): p is string => p != null);
  } catch {
    return [];
  }
}

// ── Main ─────────────────────────────────────────────────────────────────────

function parseArgs(argv: string[]) {
  let full = false, confirmOutage = false, set: string | undefined;
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--full") full = true;
    else if (a === "--confirm-outage") confirmOutage = true;
    else if (a === "--set") set = argv[++i];
    else if (!a.startsWith("--") && !set) set = a; // bare slug → scoped
  }
  return { full, confirmOutage, set };
}

async function main() {
  const { full, confirmOutage, set } = parseArgs(process.argv.slice(2));

  if (!full && !set) {
    console.error(
      "Specify a mode:\n" +
      "  --set <slug>                     scoped, atomic (recommended)\n" +
      "  --full --confirm-outage          whole-DB reload (brief blank window)");
    localDb.close();
    process.exit(2);
  }

  console.log(`Migrating local SQLite → Turso`);
  console.log(`Target: ${TURSO_URL}`);
  console.log(`Mode: ${full ? "FULL reload" : `scoped set "${set}"`}\n`);

  console.log("Recomputing player stats (local)...");
  recomputePlayerStats();

  // Invariant guard: every players row must be linked to a canonical athlete.
  const nullAthletes = (
    localDb.prepare("SELECT COUNT(*) AS n FROM players WHERE athlete_id IS NULL").get() as { n: number }
  ).n;
  if (nullAthletes > 0) {
    console.error(
      `\n✗ ${nullAthletes} players row(s) have a NULL athlete_id — refusing to migrate.\n` +
      `  Run: npx tsx scripts/build-athletes.ts  (then re-run this migration).`);
    localDb.close();
    process.exit(1);
  }

  await createSchema();

  const athletePaths = set ? athletePathsForSet(set) : [];

  const res = full ? await migrateFull(confirmOutage) : await migrateSet(set!);

  localDb.close();

  if (res.ok) {
    console.log("\nMigration complete.");
  } else {
    console.error("\n⚠ MIGRATION reported a problem (row-count mismatch, drift, orphans, or a refused mode) — see above.");
  }

  // Revalidate cached pages only when content was actually written. An atomic
  // scoped failure or a refused full reload leaves Turso unchanged, so the
  // existing cache is still correct and we skip the revalidation call. A
  // committed-but-flagged push (e.g. new orphans) DID change live content, so
  // it still revalidates.
  if (res.committed) await triggerRevalidation(set, athletePaths);

  if (!res.ok) process.exit(1);
}

main().catch((err) => {
  console.error("Migration failed:", err);
  process.exit(1);
});
