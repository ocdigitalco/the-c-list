import Database from "better-sqlite3";

const db = new Database("the-c-list.db");
db.pragma("journal_mode = WAL");

async function main() {
// Get all NFL players who don't have an image yet
const nflPlayers = db
  .prepare(
    `SELECT DISTINCT p.id, p.name
     FROM players p
     JOIN player_appearances pa ON pa.player_id = p.id
     JOIN insert_sets i ON i.id = pa.insert_set_id
     JOIN sets s ON s.id = i.set_id
     WHERE s.sport = 'Football'
     AND (p.image_url IS NULL OR p.image_url = '')
     AND (p.sleeper_id IS NULL OR p.sleeper_id = '')
     ORDER BY p.name`
  )
  .all() as { id: number; name: string }[];

console.log(`Found ${nflPlayers.length} NFL players without images`);

// Fetch all players from Sleeper API
console.log("Fetching Sleeper NFL player database...");
const response = await fetch("https://api.sleeper.app/v1/players/nfl");
const sleeperPlayers = (await response.json()) as Record<
  string,
  {
    player_id: string;
    full_name: string | null;
    first_name: string | null;
    last_name: string | null;
    position: string | null;
    team: string | null;
    search_full_name: string | null;
  }
>;

console.log(`Loaded ${Object.keys(sleeperPlayers).length} Sleeper players`);

function normalize(name: string): string {
  return name
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9\s]/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

// Build lookup: normalized name -> sleeper player_id
const sleeperByName = new Map<string, string>();
for (const [pid, player] of Object.entries(sleeperPlayers)) {
  if (player.full_name) {
    sleeperByName.set(normalize(player.full_name), pid);
  }
}

// Sleeper headshot URL format
function sleeperHeadshot(playerId: string): string {
  return `https://sleepercdn.com/content/nfl/players/thumb/${playerId}.jpg`;
}

const update = db.prepare(
  "UPDATE players SET image_url = ?, sleeper_id = ? WHERE id = ?"
);
const updateIdOnly = db.prepare(
  "UPDATE players SET sleeper_id = ? WHERE id = ?"
);

let matched = 0;
let idOnly = 0;
const unmatched: string[] = [];

for (const player of nflPlayers) {
  const n = normalize(player.name);
  const sleeperId = sleeperByName.get(n);

  if (sleeperId) {
    const url = sleeperHeadshot(sleeperId);
    update.run(url, sleeperId, player.id);
    matched++;
  } else {
    unmatched.push(player.name);
  }
}

console.log(`\nMatched with image: ${matched}`);
console.log(`ID only (no avatar): ${idOnly}`);
console.log(`Unmatched: ${unmatched.length}`);
if (unmatched.length > 0 && unmatched.length <= 50) {
  console.log("\nUnmatched:");
  for (const name of unmatched) console.log(`  - ${name}`);
} else if (unmatched.length > 50) {
  console.log(`\nFirst 50 unmatched:`);
  for (const name of unmatched.slice(0, 50)) console.log(`  - ${name}`);
}

db.close();
console.log("\nDone!");
}

main().catch(console.error);
