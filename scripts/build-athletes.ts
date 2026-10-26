/**
 * Build the canonical `athletes` identity layer (Stage 1 of athlete pages) on the
 * LOCAL SQLite DB. Reproducible and idempotent: clears and rebuilds `athletes`,
 * then sets `players.athlete_id` on every players row from the reviewed merge
 * queue in `data/athlete-review-queue.csv`.
 *
 * Usage: npx tsx scripts/build-athletes.ts
 *
 * Pipeline:
 *   1. Pre-step — in-set spelling twins (queue action=premerge): within any ONE
 *      set that lists a subject under 2+ spellings, repoint appearances/co-links
 *      /events to the keeper player row and delete the orphan rows. Keeper =
 *      canonical form if present, else most-appearances (tie → lowest id).
 *   2. Group every (name, sport) into a canonical athlete via union-find. A queue
 *      group's merge/premerge rows sharing a `canonical` are unioned together
 *      (so merges may span sports — celebrity/cross-sport cameos); keep_separate
 *      rows add no edge; everything else defaults to one athlete per (name,sport).
 *   3. Canonical role = most-frequent subject_role across the athlete's rows, with
 *      player→athlete folded first and attraction↔character → character; a queue
 *      note of the form "role <x>" overrides it. page_kind is derived from role.
 *   4. slug = kebab(canonical name), diacritics stripped; explicit slugs in the
 *      queue note win; collisions get `-<sport>` then `-2`, `-3`, …
 *
 * READ-ONLY on Turso (never connects). Run before migrate-to-turso.ts, which
 * full-reloads the result up. Re-run after seeding a new set so its players get
 * an athlete_id (see the migrate-to-turso.ts header convention).
 */

import Database from "better-sqlite3";
import fs from "fs";
import path from "path";

const db = new Database(path.join(process.cwd(), "the-c-list.db"));
// Controlled local rebuild (repoint + delete orphan player rows); mirror the
// migrate script and bulk-move rows with FK enforcement off, cleaning up any
// orphaned co-player links by hand afterward.
db.pragma("foreign_keys = OFF");
const CSV = path.join(process.cwd(), "data", "athlete-review-queue.csv");

// ── CSV (RFC-4180, quoted fields with "" escapes) ────────────────────────────
function parseCSV(text: string): string[][] {
  const rows: string[][] = [];
  let row: string[] = [];
  let field = "";
  let inQ = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (inQ) {
      if (c === '"') {
        if (text[i + 1] === '"') { field += '"'; i++; }
        else inQ = false;
      } else field += c;
    } else if (c === '"') inQ = true;
    else if (c === ",") { row.push(field); field = ""; }
    else if (c === "\n") { row.push(field); rows.push(row); row = []; field = ""; }
    else if (c === "\r") { /* skip */ }
    else field += c;
  }
  if (field.length > 0 || row.length > 0) { row.push(field); rows.push(row); }
  return rows.filter((r) => r.length > 1 || (r.length === 1 && r[0] !== ""));
}

// ── Name helpers ─────────────────────────────────────────────────────────────
function stripDiacritics(s: string): string {
  return s.normalize("NFD").replace(/[̀-ͯ]/g, "");
}
function kebab(name: string): string {
  return stripDiacritics(name)
    .toLowerCase()
    .replace(/['’.]/g, "")
    .replace(/&/g, " and ")
    .replace(/"/g, " ")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}
function yearOf(season: string | null): number | null {
  if (!season) return null;
  const m = season.match(/(19|20)\d{2}/);
  return m ? parseInt(m[0], 10) : null;
}

// ── Load queue ───────────────────────────────────────────────────────────────
const table = parseCSV(fs.readFileSync(CSV, "utf8"));
const H = table[0];
const col = Object.fromEntries(H.map((h, k) => [h, k])) as Record<string, number>;
type QRow = { qid: string; sport: string; name: string; action: string; canonical: string; note: string };
const queue: QRow[] = table.slice(1).map((r) => ({
  qid: r[col.queue_id],
  sport: r[col.sport],
  name: r[col.exact_name],
  action: r[col.action],
  canonical: r[col.canonical],
  note: r[col.note],
}));

// ── Union-find over (name, sport) keys ───────────────────────────────────────
const key = (name: string, sport: string) => `${name}\u0000${sport}`;
const parent = new Map<string, string>();
function find(x: string): string {
  if (!parent.has(x)) parent.set(x, x);
  let r = x;
  while (parent.get(r) !== r) r = parent.get(r)!;
  while (parent.get(x) !== r) { const n = parent.get(x)!; parent.set(x, r); x = n; }
  return r;
}
function union(a: string, b: string) { const ra = find(a), rb = find(b); if (ra !== rb) parent.set(ra, rb); }

// Seed a node for every (name, sport) currently in players (post pre-step runs below,
// so we defer seeding until after the premerge dedup).

// ════════════════════════════════════════════════════════════════════════════
const run = db.transaction(() => {
  // ── 1. PRE-STEP: in-set spelling-twin dedup at the players level ───────────
  const premergeGroups = new Map<string, { names: Set<string>; sport: string; canonical: string }>();
  for (const q of queue) {
    if (q.action !== "premerge") continue;
    const g = premergeGroups.get(q.qid) ?? { names: new Set(), sport: q.sport, canonical: q.canonical };
    g.names.add(q.name);
    if (q.canonical) g.canonical = q.canonical;
    premergeGroups.set(q.qid, g);
  }

  const selPlayers = db.prepare(
    `SELECT p.id, p.name, p.set_id, COUNT(pa.id) AS apps
     FROM players p LEFT JOIN player_appearances pa ON pa.player_id = p.id
     JOIN sets s ON p.set_id = s.id
     WHERE p.name = ? AND s.sport = ?
     GROUP BY p.id`
  );
  const repointApp = db.prepare("UPDATE player_appearances SET player_id = ? WHERE player_id = ?");
  const repointCo = db.prepare("UPDATE appearance_co_players SET co_player_id = ? WHERE co_player_id = ?");
  const repointEvt = db.prepare("UPDATE player_events SET player_id = ? WHERE player_id = ?");
  const delPlayer = db.prepare("DELETE FROM players WHERE id = ?");

  let twinsMerged = 0;
  for (const g of premergeGroups.values()) {
    // Gather all player rows for the group's variant names, grouped by set.
    const bySet = new Map<number, { id: number; name: string; apps: number }[]>();
    for (const name of g.names) {
      for (const r of selPlayers.all(name, g.sport) as { id: number; name: string; set_id: number; apps: number }[]) {
        const arr = bySet.get(r.set_id) ?? [];
        arr.push({ id: r.id, name: r.name, apps: r.apps });
        bySet.set(r.set_id, arr);
      }
    }
    for (const rows of bySet.values()) {
      if (rows.length < 2) continue; // only sets that list the subject twice
      rows.sort((a, b) =>
        (a.name === g.canonical ? -1 : 0) - (b.name === g.canonical ? -1 : 0) ||
        b.apps - a.apps || a.id - b.id
      );
      const keeper = rows[0];
      for (const orphan of rows.slice(1)) {
        repointApp.run(keeper.id, orphan.id);
        repointCo.run(keeper.id, orphan.id);
        repointEvt.run(keeper.id, orphan.id);
        delPlayer.run(orphan.id);
        twinsMerged++;
      }
    }
  }
  console.log(`  Pre-step: merged ${twinsMerged} in-set spelling-twin player row(s).`);

  // De-dup appearances / co-links that became identical after repointing. Drop
  // co-links pointing at the removed duplicate appearances first (FKs are off),
  // then collapse duplicate co-links.
  db.exec(`
    DELETE FROM player_appearances WHERE id NOT IN (
      SELECT MIN(id) FROM player_appearances
      GROUP BY player_id, insert_set_id, card_number, IFNULL(subset_tag,''), IFNULL(team,'')
    );
    DELETE FROM appearance_co_players WHERE appearance_id NOT IN (SELECT id FROM player_appearances);
    DELETE FROM appearance_co_players WHERE id NOT IN (
      SELECT MIN(id) FROM appearance_co_players GROUP BY appearance_id, co_player_id
    );
  `);

  // ── 2. Union (name, sport) into canonical athletes ─────────────────────────
  const allPlayers = db
    .prepare(
      `SELECT p.id, p.name, p.set_id, p.subject_role AS role, s.sport AS sport, s.season AS season
       FROM players p JOIN sets s ON p.set_id = s.id`
    )
    .all() as { id: number; name: string; set_id: number; role: string; sport: string; season: string | null }[];

  for (const p of allPlayers) find(key(p.name, p.sport)); // seed one node per (name,sport)

  // Union merge/premerge rows that share a canonical within a queue group.
  const byQidCanon = new Map<string, QRow[]>();
  for (const q of queue) {
    if (q.action !== "merge" && q.action !== "premerge") continue;
    const k = `${q.qid}\u0000${q.canonical}`;
    (byQidCanon.get(k) ?? byQidCanon.set(k, []).get(k)!).push(q);
  }
  for (const rows of byQidCanon.values()) {
    const nodes = rows.map((q) => key(q.name, q.sport)).filter((n) => parent.has(n));
    for (let i = 1; i < nodes.length; i++) union(nodes[0], nodes[i]);
  }

  // Votes per component: canonical name, role override. Explicit slugs in a note
  // are keyed by the quoted name they annotate ("<name>" … (slug <slug>)), so a
  // note that names two slugs (Byron Murphy) assigns each to the right athlete.
  const canonVote = new Map<string, Map<string, number>>(); // root -> canon -> count
  const roleOverride = new Map<string, string>();
  const noPage = new Set<string>(); // roots a reviewer marked "no page"
  const nameSlug = new Map<string, string>(); // canonical name -> explicit slug
  for (const q of queue) {
    const node = key(q.name, q.sport);
    if (!parent.has(node)) continue;
    const root = find(node);
    if ((q.action === "merge" || q.action === "premerge") && q.canonical) {
      const m = canonVote.get(root) ?? new Map();
      m.set(q.canonical, (m.get(q.canonical) ?? 0) + 1);
      canonVote.set(root, m);
    }
    const roleM = q.note.match(/\brole\s+([a-z_]+)/i);
    if (roleM) roleOverride.set(root, roleM[1].toLowerCase());
    if (/no page/i.test(q.note)) noPage.add(root);
    for (const m of q.note.matchAll(/"([^"]+)"[^"]*?\(slug\s+([a-z0-9-]+)\)/g)) {
      nameSlug.set(m[1], m[2]);
    }
  }

  // Per-root aggregation.
  type Agg = {
    players: typeof allPlayers;
    names: Set<string>;
    sportApps: Map<string, number>;
    sportSets: Map<string, Set<number>>;
    roleCount: Map<string, number>;
  };
  const appsOf = db.prepare("SELECT COUNT(*) AS n FROM player_appearances WHERE player_id = ?");
  const rookieYears = db.prepare(
    `SELECT MIN(CAST(substr(s.season,1,4) AS INTEGER)) AS y
     FROM player_appearances pa JOIN players p ON pa.player_id = p.id
     JOIN sets s ON p.set_id = s.id
     WHERE pa.player_id = ? AND pa.is_rookie = 1`
  );
  const agg = new Map<string, Agg>();
  for (const p of allPlayers) {
    const root = find(key(p.name, p.sport));
    const a = agg.get(root) ?? {
      players: [] as typeof allPlayers, names: new Set<string>(),
      sportApps: new Map(), sportSets: new Map(), roleCount: new Map(),
    };
    a.players.push(p);
    a.names.add(p.name);
    const napps = (appsOf.get(p.id) as { n: number }).n;
    a.sportApps.set(p.sport, (a.sportApps.get(p.sport) ?? 0) + napps);
    const ss = a.sportSets.get(p.sport) ?? new Set<number>(); ss.add(p.set_id); a.sportSets.set(p.sport, ss);
    const role = p.role === "player" ? "athlete" : p.role; // fold player→athlete
    a.roleCount.set(role, (a.roleCount.get(role) ?? 0) + napps);
    agg.set(root, a);
  }

  const ROLE_PRECEDENCE = ["character", "attraction", "celebrity", "sketch_artist", "coach", "athlete", "team", "event"];
  const PAGE_KIND: Record<string, string> = {
    athlete: "player", coach: "player",
    character: "character", attraction: "character",
    celebrity: "person", sketch_artist: "person",
    team: "team", event: "none",
  };

  const insAthlete = db.prepare(
    `INSERT INTO athletes (slug, name, sport, subject_role, page_kind, aliases, set_count, card_count, first_year, rookie_year, created_at)
     VALUES (@slug, @name, @sport, @subject_role, @page_kind, @aliases, @set_count, @card_count, @first_year, @rookie_year, @created_at)`
  );
  const setAthleteId = db.prepare("UPDATE players SET athlete_id = ? WHERE id = ?");

  // Deterministic order so slug collisions resolve stably (bigger athlete wins the bare slug).
  const roots = [...agg.keys()].map((root) => {
    const a = agg.get(root)!;
    // canonical name
    let name: string;
    const votes = canonVote.get(root);
    if (votes && votes.size) {
      name = [...votes.entries()].sort((x, y) => y[1] - x[1] || (x[0] < y[0] ? -1 : 1))[0][0];
    } else {
      name = a.players[0].name; // default singleton / pure keep_separate
    }
    // sport: most card appearances, tie → most sets, tie → lexicographic
    const sport = [...a.sportApps.keys()].sort((x, y) =>
      (a.sportApps.get(y)! - a.sportApps.get(x)!) ||
      ((a.sportSets.get(y)?.size ?? 0) - (a.sportSets.get(x)?.size ?? 0)) ||
      (x < y ? -1 : 1)
    )[0];
    const cardCount = [...a.sportApps.values()].reduce((s, n) => s + n, 0);
    return { root, a, name, sport, cardCount };
  });
  roots.sort((x, y) => y.cardCount - x.cardCount || (x.name < y.name ? -1 : 1) || (x.sport < y.sport ? -1 : 1));

  const usedSlugs = new Set<string>();
  let created = 0;
  const nowIso = new Date().toISOString();
  for (const { root, a, name, sport, cardCount } of roots) {
    // role
    let role = roleOverride.get(root);
    if (!role) {
      const counts = new Map(a.roleCount);
      if (counts.has("character") && counts.has("attraction")) {
        counts.set("character", (counts.get("character") ?? 0) + (counts.get("attraction") ?? 0));
        counts.delete("attraction");
      }
      role = [...counts.entries()].sort((x, y) =>
        y[1] - x[1] || ROLE_PRECEDENCE.indexOf(x[0]) - ROLE_PRECEDENCE.indexOf(y[0])
      )[0][0];
    }
    const pageKind = noPage.has(root) ? "none" : (PAGE_KIND[role] ?? "person");

    // slug
    let slug = nameSlug.get(name) ?? kebab(name);
    if (usedSlugs.has(slug)) {
      const withSport = `${kebab(name)}-${kebab(sport)}`;
      if (!usedSlugs.has(withSport)) slug = withSport;
      else { let i = 2; while (usedSlugs.has(`${kebab(name)}-${i}`)) i++; slug = `${kebab(name)}-${i}`; }
    }
    usedSlugs.add(slug);

    // year stats
    const setIds = new Set(a.players.map((p) => p.set_id));
    const years = a.players.map((p) => yearOf(p.season)).filter((y): y is number => y != null);
    const firstYear = years.length ? Math.min(...years) : null;
    let rookieYear: number | null = null;
    for (const p of a.players) {
      const y = (rookieYears.get(p.id) as { y: number | null }).y;
      if (y != null) rookieYear = rookieYear == null ? y : Math.min(rookieYear, y);
    }

    const aliases = JSON.stringify([...a.names].sort());
    const info = insAthlete.run({
      slug, name, sport, subject_role: role, page_kind: pageKind, aliases,
      set_count: setIds.size, card_count: cardCount,
      first_year: firstYear, rookie_year: rookieYear, created_at: nowIso,
    });
    const athleteId = Number(info.lastInsertRowid);
    for (const p of a.players) setAthleteId.run(athleteId, p.id);
    created++;
  }
  console.log(`  Built ${created} canonical athletes; assigned athlete_id to ${allPlayers.length} players rows.`);
});

db.exec("DELETE FROM athletes");
db.exec("UPDATE players SET athlete_id = NULL");
run();

// ── Report ───────────────────────────────────────────────────────────────────
const nulls = (db.prepare("SELECT COUNT(*) AS n FROM players WHERE athlete_id IS NULL").get() as { n: number }).n;
const nath = (db.prepare("SELECT COUNT(*) AS n FROM athletes").get() as { n: number }).n;
const byKind = db.prepare("SELECT page_kind, COUNT(*) AS n FROM athletes GROUP BY page_kind ORDER BY n DESC").all();
console.log(`\n  athletes=${nath}  players_with_null_athlete_id=${nulls}`);
console.log("  page_kind:", JSON.stringify(byKind));
db.close();
