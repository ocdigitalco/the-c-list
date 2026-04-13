import Database from "better-sqlite3";
import { slugify, generateUniqueSlug } from "../src/lib/slugify";

const db = new Database("the-c-list.db");
db.pragma("journal_mode = WAL");

// Generate set slugs
const sets = db.prepare("SELECT id, name FROM sets ORDER BY id ASC").all() as {
  id: number;
  name: string;
}[];

const usedSetSlugs = new Set<string>();
let setCount = 0;

for (const set of sets) {
  const slug = generateUniqueSlug(set.name, usedSetSlugs);
  usedSetSlugs.add(slug);
  db.prepare("UPDATE sets SET slug = ? WHERE id = ?").run(slug, set.id);
  setCount++;
}
console.log(`Updated ${setCount} set slugs.`);

// Generate player slugs (scoped per set to avoid collisions)
const players = db
  .prepare("SELECT id, name, set_id FROM players ORDER BY id ASC")
  .all() as { id: number; name: string; set_id: number }[];

const usedPlayerSlugs = new Map<number, Set<string>>();
let playerCount = 0;

for (const p of players) {
  if (!usedPlayerSlugs.has(p.set_id)) {
    usedPlayerSlugs.set(p.set_id, new Set());
  }
  const setSlugs = usedPlayerSlugs.get(p.set_id)!;
  const slug = generateUniqueSlug(p.name, setSlugs);
  setSlugs.add(slug);
  db.prepare("UPDATE players SET slug = ? WHERE id = ?").run(slug, p.id);
  playerCount++;
}
console.log(`Updated ${playerCount} player slugs.`);

db.close();
console.log("Done!");
