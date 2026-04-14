import Database from "better-sqlite3";

const db = new Database("the-c-list.db");
db.pragma("journal_mode = WAL");

const SET_ID = 59; // 2026 Topps Disney Neon

// Get all players in this set
const players = db
  .prepare(
    `SELECT DISTINCT p.id, p.name
     FROM players p
     WHERE p.set_id = ?
     AND (p.image_url IS NULL OR p.image_url = '')
     ORDER BY p.name`
  )
  .all(SET_ID) as { id: number; name: string }[];

console.log(`Found ${players.length} players to look up`);

function normalize(name: string): string {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

async function fetchAllDisneyCharacters() {
  const allCharacters: any[] = [];
  let page = 1;
  let totalPages = 1;

  while (page <= totalPages) {
    const res = await fetch(
      `https://api.disneyapi.dev/character?pageSize=500&page=${page}`
    );
    const data = await res.json();
    allCharacters.push(...data.data);
    totalPages = data.info.totalPages;
    console.log(
      `Fetched page ${page} of ${totalPages} (${allCharacters.length} characters so far)`
    );
    page++;
  }

  return allCharacters;
}

// Manual overrides for names that don't match the API exactly
const NAME_OVERRIDES: Record<string, string> = {
  "Dr. Doofenshmirtz": "Heinz Doofenshmirtz",
  "The Beast": "Beast",
  "WALL-E": "WALL-E",
  "Zurg": "Emperor Zurg",
  "Yzma": "Yzma",
  "Sulley": "James P. \"Sulley\" Sullivan",
  "Scar": "Scar",
  "Genie": "Genie",
  "Gaston": "Gaston",
  "Elsa": "Elsa",
  "Simba": "Simba",
  "Stitch": "Stitch",
  "Mater": "Tow Mater",
  "Merlin": "Merlin",
  "Dumbo": "Dumbo",
  "Pinocchio": "Pinocchio",
  "Anger": "Anger",
  "Fear": "Fear",
  "Joy": "Joy",
  "Sadness": "Sadness",
  "Disgust": "Disgust",
  "Bing Bong": "Bing Bong",
  "Anxiety": "Anxiety",
  "Animal": "Animal",
  "Kermit": "Kermit",
  "Miss Piggy": "Miss Piggy",
  "Gonzo": "Gonzo",
  "Fozzie Bear": "Fozzie Bear",
  "Swedish Chef": "The Swedish Chef",
  "Bolt": "Bolt",
};

function findMatch(
  athleteName: string,
  characters: any[]
): any | null {
  const lookupName = NAME_OVERRIDES[athleteName] ?? athleteName;
  const n = normalize(lookupName);

  // Exact match only — no fuzzy/contains matching
  const exact = characters.find((c) => normalize(c.name) === n);
  return exact || null;
}

async function main() {
  console.log("Fetching Disney API characters...");
  const characters = await fetchAllDisneyCharacters();
  console.log(`Total API characters: ${characters.length}\n`);

  const update = db.prepare("UPDATE players SET image_url = ? WHERE id = ?");
  let matched = 0;
  let missed = 0;
  const missedNames: string[] = [];

  for (const player of players) {
    const match = findMatch(player.name, characters);
    if (match && match.imageUrl) {
      update.run(match.imageUrl, player.id);
      matched++;
      console.log(`✓ ${player.name} → ${match.name} (${match.imageUrl.substring(0, 60)}...)`);
    } else {
      missed++;
      missedNames.push(player.name);
      if (match) {
        console.log(`✗ ${player.name} → matched "${match.name}" but no imageUrl`);
      } else {
        console.log(`✗ ${player.name} → no match`);
      }
    }
  }

  console.log(`\n${"=".repeat(50)}`);
  console.log(`Total processed: ${players.length}`);
  console.log(`Matched with image: ${matched}`);
  console.log(`Not matched: ${missed}`);
  if (missedNames.length > 0) {
    console.log(`\nMissed names:`);
    for (const name of missedNames) {
      console.log(`  - ${name}`);
    }
  }

  db.close();
}

main().catch(console.error);
