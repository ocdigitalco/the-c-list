/**
 * Backfill athlete image ids on `players`, in order:
 *   (a) sibling-copy — copy an id from another player row on the SAME athlete_id
 *       (zero external calls; never overwrites a non-NULL id);
 *   (b) external match per sport for players still NULL — NBA / MLB / Sleeper NFL
 *       / UFC (Entertainment is sibling-copy only; see ruling). Exact
 *       normalized-name first, then fuzzy (token-sort ratio) >= 85. Every fuzzy
 *       (sub-100) match is logged to scratchpad/headshot-fuzzy.csv and every
 *       miss to scratchpad/headshot-unmatched.csv so wrong faces can be caught
 *       before they ship;
 *   (c) normalize ufc_image_url from bare ufc.com -> www.ufc.com.
 *
 * Idempotent: every write targets a NULL/empty column only. Run build-athletes
 * afterwards to recompute athletes.headshot_url.
 *
 * Usage:
 *   npx tsx scripts/backfill-headshots.ts                 # whole DB
 *   npx tsx scripts/backfill-headshots.ts --set <slug>    # one set only
 *   npx tsx scripts/backfill-headshots.ts --no-external   # sibling-copy + UFC only
 */
import Database from "better-sqlite3";
import fs from "fs";
import path from "path";
import { execFileSync } from "child_process";

const DB = path.join(process.cwd(), "the-c-list.db");
const SCRATCH = path.join(process.cwd(), "scratchpad");
const FUZZY_CSV = path.join(SCRATCH, "headshot-fuzzy.csv");
const UNMATCHED_CSV = path.join(SCRATCH, "headshot-unmatched.csv");
const THRESHOLD = 85;

const args = process.argv.slice(2);
const setSlug = args.includes("--set") ? args[args.indexOf("--set") + 1] : null;
const noExternal = args.includes("--no-external");

const db = new Database(DB);
db.pragma("journal_mode = WAL");

let setId: number | null = null;
if (setSlug) {
  const row = db.prepare("SELECT id FROM sets WHERE slug = ?").get(setSlug) as { id: number } | undefined;
  if (!row) { console.error(`No set with slug ${setSlug}`); process.exit(1); }
  setId = row.id;
  console.log(`Scoped to set ${setId} (${setSlug})`);
}

// ── CSV helpers (append; write header once) ──────────────────────────────────
function ensureCsv(file: string, header: string) {
  if (!fs.existsSync(SCRATCH)) fs.mkdirSync(SCRATCH, { recursive: true });
  if (!fs.existsSync(file)) fs.writeFileSync(file, header + "\n");
}
function csvCell(s: string | number | null): string {
  const v = s == null ? "" : String(s);
  return /[",\n]/.test(v) ? `"${v.replace(/"/g, '""')}"` : v;
}
function appendCsv(file: string, cells: (string | number | null)[]) {
  fs.appendFileSync(file, cells.map(csvCell).join(",") + "\n");
}
ensureCsv(FUZZY_CSV, "set,player,sport,matched_name,score,id");
ensureCsv(UNMATCHED_CSV, "set,player,sport,reason");

// ── name normalize + token-sort fuzzy (rapidfuzz-equivalent) ─────────────────
function normalize(name: string): string {
  return name
    .normalize("NFD").replace(/[̀-ͯ]/g, "")
    .toLowerCase().replace(/[^a-z0-9\s]/g, " ").replace(/\s+/g, " ").trim();
}
function sortTokens(s: string): string {
  return s.split(" ").filter(Boolean).sort().join(" ");
}
function levRatio(a: string, b: string): number {
  if (!a.length && !b.length) return 100;
  const m = a.length, n = b.length;
  const d = Array.from({ length: m + 1 }, () => new Array<number>(n + 1).fill(0));
  for (let i = 0; i <= m; i++) d[i][0] = i;
  for (let j = 0; j <= n; j++) d[0][j] = j;
  for (let i = 1; i <= m; i++)
    for (let j = 1; j <= n; j++)
      d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
  const dist = d[m][n];
  return (1 - dist / Math.max(m, n)) * 100;
}
function tokenSortRatio(a: string, b: string): number {
  return levRatio(sortTokens(a), sortTokens(b));
}
/** Exact on normalized name, else best fuzzy >= THRESHOLD. */
function bestMatch(name: string, lookup: Map<string, string>, keys: string[]): { key: string; score: number } | null {
  const n = normalize(name);
  if (lookup.has(n)) return { key: n, score: 100 };
  // Prune: only Levenshtein against keys sharing a >=3-char token (usually the
  // surname). Keeps the fuzzy fallback from scanning the whole lookup each time.
  const toks = n.split(" ").filter((t) => t.length >= 3);
  let best: { key: string; score: number } | null = null;
  for (const k of keys) {
    if (toks.length && !toks.some((t) => k.includes(t))) continue;
    const sc = tokenSortRatio(n, k);
    if (sc >= THRESHOLD && (!best || sc > best.score)) best = { key: k, score: sc };
  }
  return best;
}

// ── (a) sibling-copy ─────────────────────────────────────────────────────────
function siblingCopy(col: string, nonEmpty = false): number {
  const emptyCond = nonEmpty ? `(${col} IS NULL OR ${col} = '')` : `${col} IS NULL`;
  const hasCond = nonEmpty ? `q.${col} IS NOT NULL AND q.${col} != ''` : `q.${col} IS NOT NULL`;
  const setFilter = setId ? ` AND p.set_id = ${setId}` : "";
  const res = db
    .prepare(
      `UPDATE players SET ${col} = (
         SELECT q.${col} FROM players q
         WHERE q.athlete_id = players.athlete_id AND ${hasCond} LIMIT 1)
       WHERE ${emptyCond} AND athlete_id IS NOT NULL${setId ? " AND set_id = " + setId : ""}
         AND EXISTS (SELECT 1 FROM players q WHERE q.athlete_id = players.athlete_id AND ${hasCond})`
    )
    .run();
  void setFilter;
  return res.changes;
}

console.log("\n── (a) sibling-copy (same athlete_id) ──");
const sibNba = siblingCopy("nba_player_id");
const sibMlb = siblingCopy("mlb_player_id");
const sibUfc = siblingCopy("ufc_image_url", true);
const sibImg = siblingCopy("image_url", true);
const sibSleeper = siblingCopy("sleeper_id", true);
console.log(`  nba=${sibNba} mlb=${sibMlb} ufc=${sibUfc} image_url=${sibImg} sleeper_id=${sibSleeper}`);
const siblingTotal = sibNba + sibMlb + sibUfc + sibImg;

// ── (c) UFC normalize bare ufc.com -> www.ufc.com ────────────────────────────
console.log("\n── (c) normalize UFC urls ──");
const ufcNorm =
  db.prepare(`UPDATE players SET ufc_image_url = 'https://www.ufc.com/' || substr(ufc_image_url, 17) WHERE ufc_image_url LIKE 'https://ufc.com/%'`).run().changes +
  db.prepare(`UPDATE players SET ufc_image_url = 'https://www.ufc.com/' || substr(ufc_image_url, 16) WHERE ufc_image_url LIKE 'http://ufc.com/%'`).run().changes;
console.log(`  normalized ${ufcNorm} ufc.com urls`);

// ── (b) external match per sport ─────────────────────────────────────────────
interface NullPlayer { id: number; name: string; set_name: string; }
function nullPlayers(sport: string, col: string, nonEmpty = false): NullPlayer[] {
  const emptyCond = nonEmpty ? `(p.${col} IS NULL OR p.${col} = '')` : `p.${col} IS NULL`;
  return db
    .prepare(
      `SELECT DISTINCT p.id, p.name, s.name AS set_name
       FROM players p JOIN sets s ON s.id = p.set_id
       WHERE s.sport = ? AND ${emptyCond}${setId ? " AND p.set_id = " + setId : ""}`
    )
    .all(sport) as NullPlayer[];
}

async function externalMatch(
  sport: string,
  col: string,
  nonEmpty: boolean,
  buildLookup: () => Promise<Map<string, string>>,
  toValue: (matchedValue: string) => { [k: string]: string | number } // column updates
) {
  const targets = nullPlayers(sport, col, nonEmpty);
  if (targets.length === 0) { console.log(`  ${sport}: 0 to match`); return { matched: 0, fuzzy: 0, unmatched: 0 }; }
  let lookup: Map<string, string>;
  try { lookup = await buildLookup(); }
  catch (e) { console.log(`  ${sport}: source fetch failed (${(e as Error).message}) — skipping`); for (const t of targets) appendCsv(UNMATCHED_CSV, [t.set_name, t.name, sport, "source-fetch-failed"]); return { matched: 0, fuzzy: 0, unmatched: targets.length }; }
  const keys = [...lookup.keys()];
  let matched = 0, fuzzy = 0, unmatched = 0;
  const updaters = new Map<string, ReturnType<typeof db.prepare>>();
  for (const t of targets) {
    if (!t.name || /team card/i.test(t.name)) { unmatched++; appendCsv(UNMATCHED_CSV, [t.set_name, t.name, sport, "skip-nonperson"]); continue; }
    const m = bestMatch(t.name, lookup, keys);
    if (!m) { unmatched++; appendCsv(UNMATCHED_CSV, [t.set_name, t.name, sport, "no-match"]); continue; }
    const value = lookup.get(m.key)!;
    // Only EXACT (normalized) matches are written. Fuzzy (sub-100) matches are
    // logged for review and HELD — they produce wrong faces too often at >=85
    // (e.g. Lauren Jackson -> Jaren Jackson). Approve from the CSV to apply.
    if (m.score < 100) { fuzzy++; appendCsv(FUZZY_CSV, [t.set_name, t.name, sport, m.key, m.score.toFixed(0), String(value)]); continue; }
    const cols = toValue(value);
    const sig = Object.keys(cols).sort().join(",");
    if (!updaters.has(sig)) updaters.set(sig, db.prepare(`UPDATE players SET ${Object.keys(cols).map((c) => `${c} = @${c}`).join(", ")} WHERE id = @id`));
    updaters.get(sig)!.run({ ...cols, id: t.id });
    matched++;
  }
  console.log(`  ${sport}: ${matched}/${targets.length} exact written, ${fuzzy} fuzzy held, ${unmatched} unmatched`);
  return { matched, fuzzy, unmatched };
}

async function run() {
  if (noExternal) { console.log("\n── (b) external: skipped (--no-external) ──"); finish(siblingTotal, 0); return; }
  console.log("\n── (b) external match per sport ──");
  let ext = 0;

  // NBA — static list via nba_api (installed); id -> nba_player_id
  ext += (await externalMatch("Basketball", "nba_player_id", false, async () => {
    const out = execFileSync("python3", ["-c", "from nba_api.stats.static import players; import json,sys; sys.stdout.write(json.dumps(players.get_players()))"], { maxBuffer: 64 * 1024 * 1024 }).toString();
    const list = JSON.parse(out) as { id: number; full_name: string }[];
    const m = new Map<string, string>();
    for (const p of list) m.set(normalize(p.full_name), String(p.id));
    return m;
  }, (v) => ({ nba_player_id: Number(v) }))).matched;

  // MLB — StatsAPI, 6 seasons
  ext += (await externalMatch("Baseball", "mlb_player_id", false, async () => {
    const seasons = ["2026", "2025", "2024", "2023", "2022", "2021"];
    const m = new Map<string, string>();
    for (const s of seasons) {
      const r = await fetch(`https://statsapi.mlb.com/api/v1/sports/1/players?season=${s}&gameType=R`);
      if (!r.ok) continue;
      const d = (await r.json()) as { people?: { id: number; fullName: string }[] };
      for (const p of d.people ?? []) if (p.fullName && !m.has(normalize(p.fullName))) m.set(normalize(p.fullName), String(p.id));
    }
    if (m.size === 0) throw new Error("no MLB players");
    return m;
  }, (v) => ({ mlb_player_id: Number(v) }))).matched;

  // Sleeper NFL — full players json; value = "sleeperId|hasThumb" (we always build thumb url)
  ext += (await externalMatch("Football", "image_url", true, async () => {
    const r = await fetch("https://api.sleeper.app/v1/players/nfl");
    if (!r.ok) throw new Error("sleeper " + r.status);
    const d = (await r.json()) as Record<string, { player_id: string; full_name: string | null }>;
    const m = new Map<string, string>();
    for (const k of Object.keys(d)) { const p = d[k]; if (p.full_name && p.player_id) { const n = normalize(p.full_name); if (!m.has(n)) m.set(n, p.player_id); } }
    return m;
  }, (v) => ({ image_url: `https://sleepercdn.com/content/nfl/players/thumb/${v}.jpg`, sleeper_id: v }))).matched;

  // UFC — Octagon API; value = imgUrl (already www.ufc.com-hosted)
  ext += (await externalMatch("MMA", "ufc_image_url", true, async () => {
    const r = await fetch("https://api.octagon-api.com/fighters");
    if (!r.ok) throw new Error("octagon " + r.status);
    const d = (await r.json()) as Record<string, { name?: string; imgUrl?: string }>;
    const m = new Map<string, string>();
    for (const k of Object.keys(d)) { const f = d[k]; if (f.name && f.imgUrl) { const n = normalize(f.name); if (!m.has(n)) m.set(n, f.imgUrl); } }
    return m;
  }, (v) => ({ ufc_image_url: v }))).matched;

  finish(siblingTotal, ext);
}

function finish(sibling: number, external: number) {
  console.log(`\nDONE. sibling-copy filled ${sibling}, external filled ${external}.`);
  console.log(`  fuzzy log: ${FUZZY_CSV}`);
  console.log(`  unmatched log: ${UNMATCHED_CSV}`);
  db.close();
}

run();
