/**
 * Seed script: 2025-26 Topps Hoops Basketball — FULL CHECKLIST
 * Deletes existing data for set 834, re-inserts all cards cleanly.
 *
 * Usage: npx tsx scripts/seed-hoops-2025-26.ts
 */
import Database from "better-sqlite3";

const db = new Database("the-c-list.db");
db.pragma("journal_mode = WAL");
db.pragma("foreign_keys = ON");

const SET_ID = 834;

// Verify set exists
const setRow = db.prepare("SELECT id, name FROM sets WHERE id = ?").get(SET_ID) as
  | { id: number; name: string }
  | undefined;
if (!setRow) {
  console.error(`Set ${SET_ID} not found!`);
  process.exit(1);
}
console.log(`Resetting data for: ${setRow.name} (ID ${SET_ID})`);

// ─── Delete existing data ────────────────────────────────────────────────────

const existingIS = db
  .prepare("SELECT id FROM insert_sets WHERE set_id = ?")
  .all(SET_ID) as { id: number }[];
const isIds = existingIS.map((r) => r.id);

if (isIds.length > 0) {
  const placeholders = isIds.map(() => "?").join(",");

  // Get appearance IDs for co-player cleanup
  const appIds = db
    .prepare(
      `SELECT id FROM player_appearances WHERE insert_set_id IN (${placeholders})`
    )
    .all(...isIds) as { id: number }[];

  if (appIds.length > 0) {
    const appPlaceholders = appIds.map(() => "?").join(",");
    db.prepare(
      `DELETE FROM appearance_co_players WHERE appearance_id IN (${appPlaceholders})`
    ).run(...appIds.map((a) => a.id));
  }

  db.prepare(
    `DELETE FROM player_appearances WHERE insert_set_id IN (${placeholders})`
  ).run(...isIds);
  db.prepare(
    `DELETE FROM parallels WHERE insert_set_id IN (${placeholders})`
  ).run(...isIds);
  db.prepare(`DELETE FROM insert_sets WHERE set_id = ?`).run(SET_ID);
}

db.prepare("DELETE FROM players WHERE set_id = ?").run(SET_ID);
console.log("  Cleared existing players, appearances, parallels, insert sets.");

// ─── Helpers ──────────────────────────────────────────────────────────────────

const insertPlayer = db.prepare(
  "INSERT INTO players (set_id, name, unique_cards, total_print_run, one_of_ones, insert_set_count) VALUES (?, ?, 0, 0, 0, 0)"
);
const findPlayer = db.prepare(
  "SELECT id FROM players WHERE set_id = ? AND name = ?"
);
const insertIS = db.prepare(
  "INSERT INTO insert_sets (set_id, name) VALUES (?, ?)"
);
const insertPar = db.prepare(
  "INSERT INTO parallels (insert_set_id, name, print_run) VALUES (?, ?, ?)"
);
const insertApp = db.prepare(
  "INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)"
);
const insertCo = db.prepare(
  "INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)"
);

function getOrCreatePlayer(name: string): number {
  const row = findPlayer.get(SET_ID, name) as { id: number } | undefined;
  if (row) return row.id;
  const result = insertPlayer.run(SET_ID, name);
  return Number(result.lastInsertRowid);
}

function createInsertSet(name: string): number {
  const result = insertIS.run(SET_ID, name);
  return Number(result.lastInsertRowid);
}

function createParallel(
  isId: number,
  name: string,
  printRun: number | null
): void {
  insertPar.run(isId, name, printRun);
}

function createAppearance(
  playerId: number,
  isId: number,
  cardNumber: string,
  isRookie: boolean,
  team: string | null
): number {
  const result = insertApp.run(playerId, isId, cardNumber, isRookie ? 1 : 0, team);
  return Number(result.lastInsertRowid);
}

type Card = [string, string, string, boolean?]; // [cardNumber, name, team, isRookie?]
type MultiCard = [string, [string, string][]]; // [cardNumber, [[name, team], ...]]

function addCards(isId: number, cards: Card[]): void {
  for (const [num, name, team, rookie] of cards) {
    const pid = getOrCreatePlayer(name);
    createAppearance(pid, isId, num, rookie ?? false, team);
  }
}

function addMultiCards(isId: number, cards: MultiCard[]): void {
  for (const [num, players] of cards) {
    const appIds: number[] = [];
    const playerIds: number[] = [];
    for (const [name, team] of players) {
      const pid = getOrCreatePlayer(name);
      const appId = createAppearance(pid, isId, num, true, team);
      appIds.push(appId);
      playerIds.push(pid);
    }
    for (let i = 0; i < appIds.length; i++) {
      for (let j = 0; j < playerIds.length; j++) {
        if (i !== j) insertCo.run(appIds[i], playerIds[j]);
      }
    }
  }
}

function addMultiCardsNoRookie(isId: number, cards: MultiCard[]): void {
  for (const [num, players] of cards) {
    const appIds: number[] = [];
    const playerIds: number[] = [];
    for (const [name, team] of players) {
      const pid = getOrCreatePlayer(name);
      const appId = createAppearance(pid, isId, num, false, team);
      appIds.push(appId);
      playerIds.push(pid);
    }
    for (let i = 0; i < appIds.length; i++) {
      for (let j = 0; j < playerIds.length; j++) {
        if (i !== j) insertCo.run(appIds[i], playerIds[j]);
      }
    }
  }
}

// ─── Parallel definitions ─────────────────────────────────────────────────────

const BASE_PARS: [string, number | null][] = [
  ["Rainbow", null],
  ["Pixel Burst", null],
  ["Rainbow Yellow", null],
  ["Rainbow Green and Blue", null],
  ["Rainbow Gold and Green", null],
  ["Pixel Burst Blue", null],
  ["Pixel Burst Purple", 199],
  ["Pixel Burst Green", 149],
  ["Pixel Burst Gold", 99],
  ["Pixel Burst Orange", 49],
  ["Pixel Burst Black", 25],
  ["Pixel Burst Red", 10],
  ["Pixel Burst Platinum", 1],
];

const HOBBY_INSERT_PARS: [string, number | null][] = [
  ["Rainbow", null],
  ["Pixel Burst", null],
  ["Pixel Burst Purple", 199],
  ["Pixel Burst Green", 149],
  ["Pixel Burst Gold", 99],
  ["Pixel Burst Orange", 49],
  ["Pixel Burst Black", 25],
  ["Pixel Burst Red", 10],
  ["Pixel Burst Platinum", 1],
];

const RETAIL_INSERT_PARS: [string, number | null][] = [
  ["Green Hoops", null],
  ["Orange Hoops", null],
  ["Light Burst", null],
  ["Light Burst Purple", 199],
  ["Light Burst Green", 149],
  ["Light Burst Gold", 99],
  ["Light Burst Orange", 49],
  ["Light Burst Black", 25],
  ["Light Burst Red", 10],
  ["Light Burst Platinum", 1],
];

const HRS_PARS: [string, number | null][] = [
  ["Pixel Burst Purple", 199],
  ["Pixel Burst Green", 149],
  ["Pixel Burst Gold", 99],
  ["Pixel Burst Orange", 49],
  ["Pixel Burst Black", 25],
  ["Pixel Burst Red", 10],
  ["Pixel Burst Platinum", 1],
];

const HS_PARS = HRS_PARS;

const DUAL_PARS: [string, number | null][] = [
  ["Pixel Burst Black", 25],
  ["Pixel Burst Red", 10],
  ["Pixel Burst Platinum", 1],
];

const SIG89_PARS: [string, number | null][] = [
  ["Green Hoops", null],
  ["Light Burst", null],
  ["Pixel Burst Black", 25],
  ["Pixel Burst Red", 10],
  ["Pixel Burst Platinum", 1],
];

const HFS_PARS: [string, number | null][] = [
  ["Light Burst Purple", 199],
  ["Light Burst Green", 149],
  ["Light Burst Gold", 99],
  ["Light Burst Orange", 49],
  ["Light Burst Black", 25],
  ["Light Burst Red", 10],
  ["Light Burst Platinum", 1],
];

const HHS_PARS = HFS_PARS;

const PLAT_ONLY: [string, number | null][] = [["Platinum", 1]];

// ─── Insert all data in a transaction ─────────────────────────────────────────

const seedAll = db.transaction(() => {
  // ═══════════════════════════════════════════════════════════════════════════
  // BASE SET (#1–260)
  // ═══════════════════════════════════════════════════════════════════════════
  const baseIS = createInsertSet("Base Set");
  for (const [n, pr] of BASE_PARS) createParallel(baseIS, n, pr);

  const baseCards: Card[] = [
    ["1","Rui Hachimura","Los Angeles Lakers"],["2","Saddiq Bey","Washington Wizards"],["3","OG Anunoby","New York Knicks"],["4","Tyler Herro","Miami Heat"],["5","Deandre Ayton","Portland Trail Blazers"],["6","Yang Hansen","Portland Trail Blazers",true],["7","Dylan Harper","San Antonio Spurs",true],["8","Luka Dončić","Los Angeles Lakers"],["9","Joel Embiid","Philadelphia 76ers"],["10","Pascal Siakam","Indiana Pacers"],["11","Myles Turner","Indiana Pacers"],["12","Kam Jones","Indiana Pacers",true],["13","Jalen Suggs","Orlando Magic"],["14","Austin Reaves","Los Angeles Lakers"],["15","Brandon Williams","Dallas Mavericks"],["16","Malik Beasley","Detroit Pistons"],["17","Koby Brea","Phoenix Suns",true],["18","De'Aaron Fox","San Antonio Spurs"],["19","Jamir Watkins","Washington Wizards",true],["20","Joan Beringer","Minnesota Timberwolves",true],["21","Jalen Williams","Oklahoma City Thunder"],["22","Marcus Smart","Washington Wizards"],["23","Keldon Johnson","San Antonio Spurs"],["24","Alex Caruso","Oklahoma City Thunder"],["25","Kyrie Irving","Dallas Mavericks"],["26","Naz Reid","Minnesota Timberwolves"],["27","Max Strus","Cleveland Cavaliers"],["28","Evan Mobley","Cleveland Cavaliers"],["29","Nic Claxton","Brooklyn Nets"],["30","Victor Wembanyama","San Antonio Spurs"],
    ["31","Ivica Zubac","Los Angeles Clippers"],["32","Alijah Martin","Toronto Raptors",true],["33","AJ Green","Milwaukee Bucks"],["34","Al Horford","Boston Celtics"],["35","Cooper Flagg","Dallas Mavericks",true],["36","Onyeka Okungwu","Atlanta Hawks"],["37","Bam Adebayo","Miami Heat"],["38","Ace Bailey","Utah Jazz",true],["39","Jrue Holiday","Boston Celtics"],["40","Franz Wagner","Orlando Magic"],["41","Donte DiVincenzo","Minnesota Timberwolves"],["42","Gary Payton II","Golden State Warriors"],["43","Reed Sheppard","Houston Rockets"],["44","Larry Nance Jr.","Atlanta Hawks"],["45","Keyonte George","Utah Jazz"],["46","Devin Carter","Sacramento Kings"],["47","Stephon Castle","San Antonio Spurs"],["48","Jeremiah Fears","New Orleans Pelicans",true],["49","Josh Giddey","Chicago Bulls"],["50","Jalen Johnson","Atlanta Hawks"],["51","Andrew Nembhard","Indiana Pacers"],["52","Asa Newell","Atlanta Hawks",true],["53","Devin Booker","Phoenix Suns"],["54","Quentin Grimes","Philadelphia 76ers"],["55","Jamal Murray","Denver Nuggets"],["56","Kyshawn George","Washington Wizards"],["57","Ryan Dunn","Phoenix Suns"],["58","Alex Sarr","Washington Wizards"],["59","Ben Saraf","Brooklyn Nets",true],["60","Andre Drummond","Philadelphia 76ers"],
    ["61","Chet Holmgren","Oklahoma City Thunder"],["62","Derik Queen","New Orleans Pelicans",true],["63","Steven Adams","Houston Rockets"],["64","Jakob Poeltl","Toronto Raptors"],["65","Coby White","Chicago Bulls"],["66","Khaman Maluach","Phoenix Suns",true],["67","Kon Knueppel","Charlotte Hornets",true],["68","Bennedict Mathurin","Indiana Pacers"],["69","DeMar DeRozan","Sacramento Kings"],["70","Noa Essengue","Chicago Bulls",true],["71","James Harden","Los Angeles Clippers"],["72","Hugo González","Boston Celtics",true],["73","Kawhi Leonard","Los Angeles Clippers"],["74","Will Riley","Washington Wizards",true],["75","Kasparas Jakučionis","Miami Heat",true],["76","Donovan Mitchell","Cleveland Cavaliers"],["77","Cole Anthony","Orlando Magic"],["78","Trey Murphy III","New Orleans Pelicans"],["79","Bobby Portis","Milwaukee Bucks"],["80","Brandon Miller","Charlotte Hornets"],["81","Cade Cunningham","Detroit Pistons"],["82","Nikola Jokić","Denver Nuggets"],["83","Keegan Murray","Sacramento Kings"],["84","LeBron James","Los Angeles Lakers"],["85","Scoot Henderson","Portland Trail Blazers"],["86","Shai Gilgeous-Alexander","Oklahoma City Thunder"],["87","Matisse Thybulle","Portland Trail Blazers"],["88","Thomas Sorber","Oklahoma City Thunder",true],["89","Deni Avdija","Portland Trail Blazers"],["90","Cedric Coward","Memphis Grizzlies",true],
    ["91","Andrew Wiggins","Miami Heat"],["92","Taurean Prince","Milwaukee Bucks"],["93","Drake Powell","Brooklyn Nets",true],["94","Jaden McDaniels","Minnesota Timberwolves"],["95","Anfernee Simons","Portland Trail Blazers"],["96","Jaylen Wells","Memphis Grizzlies"],["97","Brandin Podziemski","Golden State Warriors"],["98","Lonzo Ball","Chicago Bulls"],["99","Jalen Duren","Detroit Pistons"],["100","Mikal Bridges","New York Knicks"],["101","Jae Crowder","Sacramento Kings"],["102","Jalen Green","Houston Rockets"],["103","Ronald Holland II","Detroit Pistons"],["104","Klay Thompson","Dallas Mavericks"],["105","Zaccharie Risacher","Atlanta Hawks"],["106","Jaxson Hayes","Los Angeles Lakers"],["107","Dereck Lively II","Dallas Mavericks"],["108","Anthony Davis","Dallas Mavericks"],["109","Dyson Daniels","Atlanta Hawks"],["110","Donovan Clingan","Portland Trail Blazers"],["111","Alperen Sengun","Houston Rockets"],["112","Brandon Clarke","Memphis Grizzlies"],["113","Max Christie","Dallas Mavericks"],["114","Nikola Jović","Miami Heat"],["115","Sam Hauser","Boston Celtics"],["116","Mark Williams","Charlotte Hornets"],["117","Anthony Black","Orlando Magic"],["118","Jimmy Butler III","Golden State Warriors"],["119","Lauri Markkanen","Utah Jazz"],["120","Draymond Green","Golden State Warriors"],
    ["121","Cody Williams","Utah Jazz"],["122","Gary Trent Jr.","Milwaukee Bucks"],["123","Amen Thompson","Houston Rockets"],["124","Josh Hart","New York Knicks"],["125","RJ Barrett","Toronto Raptors"],["126","Darius Garland","Cleveland Cavaliers"],["127","Tre Mann","Charlotte Hornets"],["128","Egor Dëmin","Brooklyn Nets",true],["129","Alex Toohey","Golden State Warriors",true],["130","Paul George","Philadelphia 76ers"],["131","Nick Smith Jr.","Charlotte Hornets"],["132","Noah Penda","Orlando Magic",true],["133","Nolan Traore","Brooklyn Nets",true],["134","Nickeil Alexander-Walker","Minnesota Timberwolves"],["135","Jaylen Brown","Boston Celtics"],["136","Damian Lillard","Milwaukee Bucks"],["137","Miles McBride","New York Knicks"],["138","Xavier Tillman","Boston Celtics"],["139","Jordan Hawkins","New Orleans Pelicans"],["140","Zach LaVine","Sacramento Kings"],["141","Stephen Curry","Golden State Warriors"],["142","Jase Richardson","Orlando Magic",true],["143","Christian Braun","Denver Nuggets"],["144","Collin Murray-Boyles","Toronto Raptors",true],["145","Harrison Barnes","San Antonio Spurs"],["146","Aaron Gordon","Denver Nuggets"],["147","T.J. McConnell","Indiana Pacers"],["148","Mitchell Robinson","New York Knicks"],["149","Tyrese Haliburton","Indiana Pacers"],["150","De'Andre Hunter","Cleveland Cavaliers"],
    ["151","Sion James","Charlotte Hornets",true],["152","Nicolas Batum","Los Angeles Clippers"],["153","Naji Marshall","Dallas Mavericks"],["154","Jeremy Sochan","San Antonio Spurs"],["155","Julian Phillips","Chicago Bulls"],["156","Matas Buzelis","Chicago Bulls"],["157","Rudy Gobert","Minnesota Timberwolves"],["158","Brooks Barnhizer","Oklahoma City Thunder",true],["159","Johni Broome","Philadelphia 76ers",true],["160","Rob Dillingham","Minnesota Timberwolves"],["161","Grant Williams","Charlotte Hornets"],["162","John Tonje","Utah Jazz",true],["163","Scotty Pippen Jr.","Memphis Grizzlies"],["164","Jamal Shead","Toronto Raptors"],["165","Giannis Antetokounmpo","Milwaukee Bucks"],["166","Immanuel Quickley","Toronto Raptors"],["167","Tobias Harris","Detroit Pistons"],["168","Walker Kessler","Utah Jazz"],["169","Rocco Zikarsky","Minnesota Timberwolves",true],["170","Bilal Coulibaly","Washington Wizards"],["171","Jonas Valančiūnas","Washington Wizards"],["172","Kel'el Ware","Miami Heat"],["173","Walter Clayton Jr.","Utah Jazz",true],["174","Kentavious Caldwell-Pope","Orlando Magic"],["175","Khris Middleton","Washington Wizards"],["176","Zach Collins","Chicago Bulls"],["177","Derrick White","Boston Celtics"],["178","Aaron Nesmith","Indiana Pacers"],["179","Kyle Filipowski","Utah Jazz"],["180","Gradey Dick","Toronto Raptors"],
    ["181","Carter Bryant","San Antonio Spurs",true],["182","Adou Thiero","Los Angeles Lakers",true],["183","Michael Porter Jr.","Denver Nuggets"],["184","Kyle Kuzma","Milwaukee Bucks"],["185","LaMelo Ball","Charlotte Hornets"],["186","Grayson Allen","Phoenix Suns"],["187","Jaden Ivey","Detroit Pistons"],["188","Jaren Jackson Jr.","Memphis Grizzlies"],["189","P.J. Washington Jr.","Dallas Mavericks"],["190","Jalen Brunson","New York Knicks"],["191","Kris Murray","Portland Trail Blazers"],["192","Jordan Clarkson","Utah Jazz"],["193","Julius Randle","Minnesota Timberwolves"],["194","Paolo Banchero","Orlando Magic"],["195","Anthony Edwards","Minnesota Timberwolves"],["196","Isaiah Hartenstein","Oklahoma City Thunder"],["197","Jared McCain","Philadelphia 76ers"],["198","Jarrett Allen","Cleveland Cavaliers"],["199","Fred VanVleet","Houston Rockets"],["200","CJ McCollum","New Orleans Pelicans"],["201","Kristaps Porziņģis","Boston Celtics"],["202","Luguentz Dort","Oklahoma City Thunder"],["203","John Collins","Los Angeles Clippers"],["204","Domantas Sabonis","Sacramento Kings"],["205","Malik Monk","Sacramento Kings"],["206","Jonathan Kuminga","Golden State Warriors"],["207","Ryan Kalkbrenner","Charlotte Hornets",true],["208","Jabari Smith Jr.","Houston Rockets"],["209","Johnny Furphy","Indiana Pacers"],["210","Maxime Raynaud","Sacramento Kings",true],
    ["211","Cam Thomas","Brooklyn Nets"],["212","Jonathan Isaac","Orlando Magic"],["213","Payton Pritchard","Boston Celtics"],["214","Desmond Bane","Memphis Grizzlies"],["215","Tyrese Proctor","Cleveland Cavaliers",true],["216","Caris LeVert","Atlanta Hawks"],["217","DaRon Holmes II","Denver Nuggets"],["218","Chaz Lanier","Detroit Pistons",true],["219","Cason Wallace","Oklahoma City Thunder"],["220","Ja Morant","Memphis Grizzlies"],["221","Kevin Durant","Houston Rockets"],["222","Norman Powell","Miami Heat"],["223","Jaime Jaquez Jr.","Miami Heat"],["224","Brandon Ingram","Toronto Raptors"],["225","Obi Toppin","Indiana Pacers"],["226","Tre Johnson III","Washington Wizards",true],["227","Dorian Finney-Smith","Los Angeles Lakers"],["228","Jayson Tatum","Boston Celtics"],["229","Micah Peavy","New Orleans Pelicans",true],["230","Zach Edey","Memphis Grizzlies"],["231","Dejounte Murray","New Orleans Pelicans"],["232","Liam McNeeley","Charlotte Hornets",true],["233","Devin Vassell","San Antonio Spurs"],["234","Scottie Barnes","Toronto Raptors"],["235","Cameron Johnson","Denver Nuggets"],["236","Bub Carrington","Washington Wizards"],["237","Kyle Lowry","Philadelphia 76ers"],["238","Yanic Konan-Niederhäuser","Los Angeles Clippers",true],["239","Buddy Hield","Golden State Warriors"],["240","Ausar Thompson","Detroit Pistons"],
    ["241","Nique Clifford","Sacramento Kings",true],["242","Tristan da Silva","Orlando Magic"],["243","Shaedon Sharpe","Portland Trail Blazers"],["244","VJ Edgecombe","Philadelphia 76ers",true],["245","Patrick Williams","Chicago Bulls"],["246","Danny Wolf","Brooklyn Nets",true],["247","Chris Paul","San Antonio Spurs"],["248","Jae'Sean Tate","Houston Rockets"],["249","Karl-Anthony Towns","New York Knicks"],["250","Russell Westbrook","Denver Nuggets"],["251","Bruce Brown","New Orleans Pelicans"],["252","Ayo Dosunmu","Chicago Bulls"],["253","Oso Ighodaro","Phoenix Suns"],["254","Bradley Beal","Phoenix Suns"],["255","Rasheer Fleming","Phoenix Suns",true],["256","Derrick Jones Jr.","Los Angeles Clippers"],["257","Herbert Jones","New Orleans Pelicans"],["258","Tyrese Maxey","Philadelphia 76ers"],["259","Trae Young","Atlanta Hawks"],["260","Dalton Knecht","Los Angeles Lakers"],
  ];
  addCards(baseIS, baseCards);
  console.log(`  Base Set: ${baseCards.length} cards`);

  // ═══════════════════════════════════════════════════════════════════════════
  // BASE HIGHLIGHTS (#261–270)
  // ═══════════════════════════════════════════════════════════════════════════
  const hlIS = createInsertSet("Base Highlights");
  for (const [n, pr] of BASE_PARS) createParallel(hlIS, n, pr);

  const hlCards: Card[] = [
    ["261","Stephen Curry","Golden State Warriors"],["262","Tyrese Haliburton","Indiana Pacers"],["263","Jayson Tatum","Boston Celtics"],["264","Ja Morant","Memphis Grizzlies"],["265","Pascal Siakam","Indiana Pacers"],["266","Aaron Gordon","Denver Nuggets"],["267","Shaedon Sharpe","Portland Trail Blazers"],["268","Shai Gilgeous-Alexander","Oklahoma City Thunder"],["269","Luka Dončić","Los Angeles Lakers"],["270","Anthony Edwards","Minnesota Timberwolves"],
  ];
  addCards(hlIS, hlCards);
  console.log(`  Base Highlights: ${hlCards.length} cards`);

  // ═══════════════════════════════════════════════════════════════════════════
  // BASE ALL-STARS (#271–300)
  // ═══════════════════════════════════════════════════════════════════════════
  const asIS = createInsertSet("Base All-Stars");
  for (const [n, pr] of BASE_PARS) createParallel(asIS, n, pr);

  const asCards: Card[] = [
    ["271","Jaylen Brown","Boston Celtics"],["272","Kevin Durant","Phoenix Suns"],["273","Kyrie Irving","Dallas Mavericks"],["274","Damian Lillard","Milwaukee Bucks"],["275","Stephen Curry","Golden State Warriors"],["276","James Harden","Los Angeles Clippers"],["277","Jayson Tatum","Boston Celtics"],["278","Jalen Brunson","New York Knicks"],["279","Anthony Edwards","Minnesota Timberwolves"],["280","Tyler Herro","Miami Heat"],["281","Evan Mobley","Cleveland Cavaliers"],["282","Cade Cunningham","Detroit Pistons"],["283","Darius Garland","Cleveland Cavaliers"],["284","Jaren Jackson Jr.","Memphis Grizzlies"],["285","Jalen Williams","Oklahoma City Thunder"],["286","Shai Gilgeous-Alexander","Oklahoma City Thunder"],["287","Donovan Mitchell","Cleveland Cavaliers"],["288","Pascal Siakam","Indiana Pacers"],["289","Victor Wembanyama","San Antonio Spurs"],["290","Nikola Jokić","Denver Nuggets"],["291","Alperen Sengun","Houston Rockets"],["292","Karl-Anthony Towns","New York Knicks"],["293","Trae Young","Atlanta Hawks"],["294","Stephon Castle","San Antonio Spurs"],["295","Jaylen Wells","Memphis Grizzlies"],["296","Zach Edey","Memphis Grizzlies"],["297","Ryan Dunn","Phoenix Suns"],["298","Dalton Knecht","Los Angeles Lakers"],["299","Keyonte George","Utah Jazz"],["300","Amen Thompson","Houston Rockets"],
  ];
  addCards(asIS, asCards);
  console.log(`  Base All-Stars: ${asCards.length} cards`);

  // ═══════════════════════════════════════════════════════════════════════════
  // HOOPS ROOKIE SIGNATURES
  // ═══════════════════════════════════════════════════════════════════════════
  const hrsIS = createInsertSet("Hoops Rookie Signatures");
  for (const [n, pr] of HRS_PARS) createParallel(hrsIS, n, pr);

  const hrsCards: Card[] = [
    ["HRS-AB","Ace Bailey","Utah Jazz",true],["HRS-AM","Alijah Martin","Toronto Raptors",true],["HRS-AN","Asa Newell","Atlanta Hawks",true],["HRS-AT","Adou Thiero","Los Angeles Lakers",true],["HRS-ATO","Alex Toohey","Golden State Warriors",true],["HRS-BB","Brooks Barnhizer","Oklahoma City Thunder",true],["HRS-BS","Ben Saraf","Brooklyn Nets",true],["HRS-CC","Cedric Coward","Memphis Grizzlies",true],["HRS-CF","Cooper Flagg","Dallas Mavericks",true],["HRS-CL","Chaz Lanier","Detroit Pistons",true],["HRS-CM","Collin Murray-Boyles","Toronto Raptors",true],["HRS-DH","Dylan Harper","San Antonio Spurs",true],["HRS-DP","Drake Powell","Brooklyn Nets",true],["HRS-DQ","Derik Queen","New Orleans Pelicans",true],["HRS-DW","Danny Wolf","Brooklyn Nets",true],["HRS-ED","Egor Dëmin","Brooklyn Nets",true],["HRS-JB","Joan Beringer","Minnesota Timberwolves",true],["HRS-JBR","Johni Broome","Philadelphia 76ers",true],["HRS-JR","Jase Richardson","Orlando Magic",true],["HRS-JS","Javon Small","Memphis Grizzlies",true],["HRS-JT","John Tonje","Utah Jazz",true],["HRS-JW","Jamir Watkins","Washington Wizards",true],["HRS-KJ","Kasparas Jakučionis","Miami Heat",true],["HRS-KK","Kon Knueppel","Charlotte Hornets",true],["HRS-KM","Khaman Maluach","Phoenix Suns",true],["HRS-KS","Kobe Sanders","Los Angeles Clippers",true],["HRS-LM","Liam McNeeley","Charlotte Hornets",true],["HRS-MR","Maxime Raynaud","Sacramento Kings",true],["HRS-NC","Nique Clifford","Sacramento Kings",true],["HRS-NE","Noa Essengue","Chicago Bulls",true],["HRS-NT","Nolan Traore","Brooklyn Nets",true],["HRS-RF","Rasheer Fleming","Phoenix Suns",true],["HRS-RK","Ryan Kalkbrenner","Charlotte Hornets",true],["HRS-SJ","Sion James","Charlotte Hornets",true],["HRS-TP","Tyrese Proctor","Cleveland Cavaliers",true],["HRS-TS","Thomas Sorber","Oklahoma City Thunder",true],["HRS-WC","Walter Clayton Jr.","Utah Jazz",true],["HRS-WR","Will Riley","Washington Wizards",true],["HRS-YH","Yang Hansen","Portland Trail Blazers",true],["HRS-YK","Yanic Konan-Niederhäuser","Los Angeles Clippers",true],
  ];
  addCards(hrsIS, hrsCards);
  console.log(`  Hoops Rookie Signatures: ${hrsCards.length} cards`);

  // ═══════════════════════════════════════════════════════════════════════════
  // HOOPS SIGNS
  // ═══════════════════════════════════════════════════════════════════════════
  const hsIS = createInsertSet("Hoops Signs");
  for (const [n, pr] of HS_PARS) createParallel(hsIS, n, pr);

  const hsCards: Card[] = [
    ["HS-AE","Alex English","Denver Nuggets"],["HS-AED","Anthony Edwards","Minnesota Timberwolves"],["HS-AH","Al Horford","Boston Celtics"],["HS-AM","Ajay Mitchell","Oklahoma City Thunder"],["HS-BC","Brandon Clarke","Memphis Grizzlies"],["HS-BM","Brandon Miller","Charlotte Hornets"],["HS-CJ","Cameron Johnson","Brooklyn Nets"],["HS-CK","Corey Kispert","Washington Wizards"],["HS-DD","Donte DiVincenzo","Minnesota Timberwolves"],["HS-DG","Daniel Gafford","Dallas Mavericks"],["HS-DJ","Derrick Jones Jr.","Los Angeles Clippers"],["HS-DR","Duncan Robinson","Miami Heat"],["HS-GD","Gradey Dick","Toronto Raptors"],["HS-GG","George Gervin","San Antonio Spurs"],["HS-GV","Gabe Vincent","Los Angeles Lakers"],["HS-HJ","Herbert Jones","New Orleans Pelicans"],["HS-JAW","Jalen Wilson","Brooklyn Nets"],["HS-JH","Juwan Howard","Washington Wizards"],["HS-JJ","Jaime Jaquez Jr.","Miami Heat"],["HS-JS","Jamal Shead","Toronto Raptors"],["HS-JT","Jaylon Tyson","Cleveland Cavaliers"],["HS-JW","Jaylen Wells","Memphis Grizzlies"],["HS-JWI","Jason Williams","Sacramento Kings"],["HS-KF","Kyle Filipowski","Utah Jazz"],["HS-KG","Kyshawn George","Washington Wizards"],["HS-KH","Kevin Huerter","Chicago Bulls"],["HS-KM","Kris Murray","Portland Trail Blazers"],["HS-KW","Kel'el Ware","Miami Heat"],["HS-LHU","Larry Hughes","Washington Wizards"],["HS-LJ","Larry Johnson","New York Knicks"],["HS-MS","Marcus Sasser","Detroit Pistons"],["HS-MST","Max Strus","Cleveland Cavaliers"],["HS-NENE","Nenê","Denver Nuggets"],["HS-NJ","Nikola Jokić","Denver Nuggets"],["HS-PD","Pacôme Dadiet","New York Knicks"],["HS-PL","Pelle Larsson","Miami Heat"],["HS-PP","Payton Pritchard","Boston Celtics"],["HS-PS","Peja Stojakovic","Sacramento Kings"],["HS-QP","Quinten Post","Golden State Warriors"],["HS-RD","Ryan Dunn","Phoenix Suns"],["HS-RH","Ronald Holland II","Detroit Pistons"],["HS-RHO","Robert Horry","Los Angeles Lakers"],["HS-RJ","Richard Jefferson","New Jersey Nets"],["HS-RR","Rayan Rupert","Portland Trail Blazers"],["HS-SFR","Steve Francis","Houston Rockets"],["HS-SGA","Shai Gilgeous-Alexander","Oklahoma City Thunder"],["HS-TK","Tyler Kolek","New York Knicks"],["HS-TMU","Trey Murphy III","New Orleans Pelicans"],["HS-TS","Terrence Shannon Jr.","Minnesota Timberwolves"],["HS-Td","Tristan da Silva","Orlando Magic"],["HS-UH","Udonis Haslem","Miami Heat"],["HS-VW","Victor Wembanyama","San Antonio Spurs"],["HS-YM","Yves Missi","New Orleans Pelicans"],["HS-ZE","Zach Edey","Memphis Grizzlies"],
  ];
  addCards(hsIS, hsCards);
  console.log(`  Hoops Signs: ${hsCards.length} cards`);

  // ═══════════════════════════════════════════════════════════════════════════
  // HOOPS ROOKIE DUALS
  // ═══════════════════════════════════════════════════════════════════════════
  const hrdIS = createInsertSet("Hoops Rookie Duals");
  for (const [n, pr] of DUAL_PARS) createParallel(hrdIS, n, pr);

  const hrdCards: MultiCard[] = [
    ["HRD-AL",[["Liam McNeeley","Charlotte Hornets"],["Asa Newell","Atlanta Hawks"]]],
    ["HRD-ALA",[["Alex Toohey","Golden State Warriors"],["Lachlan Olbrich","Chicago Bulls"]]],
    ["HRD-AM",[["Amari Williams","Boston Celtics"],["Max Shulga","Boston Celtics"]]],
    ["HRD-AW",[["Walter Clayton Jr.","Utah Jazz"],["Ace Bailey","Utah Jazz"]]],
    ["HRD-AWI",[["Will Richard","Golden State Warriors"],["Alex Toohey","Golden State Warriors"]]],
    ["HRD-BD",[["Danny Wolf","Brooklyn Nets"],["Ben Saraf","Brooklyn Nets"]]],
    ["HRD-CD",[["Dylan Harper","San Antonio Spurs"],["Cooper Flagg","Dallas Mavericks"]]],
    ["HRD-CK",[["Kon Knueppel","Charlotte Hornets"],["Cooper Flagg","Dallas Mavericks"]]],
    ["HRD-CN",[["Noa Essengue","Chicago Bulls"],["Collin Murray-Boyles","Toronto Raptors"]]],
    ["HRD-CNI",[["Nique Clifford","Sacramento Kings"],["Cedric Coward","Memphis Grizzlies"]]],
    ["HRD-DA",[["Ace Bailey","Utah Jazz"],["Dylan Harper","San Antonio Spurs"]]],
    ["HRD-DAS",[["Asa Newell","Atlanta Hawks"],["Derik Queen","New Orleans Pelicans"]]],
    ["HRD-DJ",[["Drake Powell","Brooklyn Nets"],["Jase Richardson","Orlando Magic"]]],
    ["HRD-EN",[["Egor Dëmin","Brooklyn Nets"],["Nolan Traore","Brooklyn Nets"]]],
    ["HRD-KD",[["Khaman Maluach","Phoenix Suns"],["Derik Queen","New Orleans Pelicans"]]],
    ["HRD-KL",[["Liam McNeeley","Charlotte Hornets"],["Kon Knueppel","Charlotte Hornets"]]],
    ["HRD-KT",[["Tyrese Proctor","Cleveland Cavaliers"],["Khaman Maluach","Phoenix Suns"]]],
    ["HRD-KTA",[["Taelon Peter","Indiana Pacers"],["Kam Jones","Indiana Pacers"]]],
    ["HRD-KW",[["Will Riley","Washington Wizards"],["Kasparas Jakučionis","Miami Heat"]]],
    ["HRD-RN",[["Rasheer Fleming","Phoenix Suns"],["Noah Penda","Orlando Magic"]]],
    ["HRD-SR",[["Sion James","Charlotte Hornets"],["Ryan Kalkbrenner","Charlotte Hornets"]]],
    ["HRD-TB",[["Thomas Sorber","Oklahoma City Thunder"],["Brooks Barnhizer","Oklahoma City Thunder"]]],
    ["HRD-WA",[["Walter Clayton Jr.","Utah Jazz"],["Alijah Martin","Toronto Raptors"]]],
    ["HRD-YJ",[["Yang Hansen","Portland Trail Blazers"],["Joan Beringer","Minnesota Timberwolves"]]],
    ["HRD-YK",[["Kobe Sanders","Los Angeles Clippers"],["Yanic Konan-Niederhäuser","Los Angeles Clippers"]]],
  ];
  addMultiCards(hrdIS, hrdCards);
  console.log(`  Hoops Rookie Duals: ${hrdCards.length} cards`);

  // ═══════════════════════════════════════════════════════════════════════════
  // HOOPS ROOKIE TRIPLES
  // ═══════════════════════════════════════════════════════════════════════════
  const hrtIS = createInsertSet("Hoops Rookie Triples");
  for (const [n, pr] of DUAL_PARS) createParallel(hrtIS, n, pr);

  const hrtCards: MultiCard[] = [
    ["HRT-AEG",[["Egor Dëmin","Brooklyn Nets"],["Collin Murray-Boyles","Toronto Raptors"],["Ace Bailey","Utah Jazz"]]],
    ["HRT-CDA",[["Dylan Harper","San Antonio Spurs"],["Cooper Flagg","Dallas Mavericks"],["Ace Bailey","Utah Jazz"]]],
    ["HRT-CDK",[["Cooper Flagg","Dallas Mavericks"],["Dylan Harper","San Antonio Spurs"],["Kon Knueppel","Charlotte Hornets"]]],
    ["HRT-DAL",[["Derik Queen","New Orleans Pelicans"],["Asa Newell","Atlanta Hawks"],["Liam McNeeley","Charlotte Hornets"]]],
    ["HRT-DBD",[["Ben Saraf","Brooklyn Nets"],["Drake Powell","Brooklyn Nets"],["Danny Wolf","Brooklyn Nets"]]],
    ["HRT-DKK",[["Kon Knueppel","Charlotte Hornets"],["Cooper Flagg","Dallas Mavericks"],["Khaman Maluach","Phoenix Suns"]]],
    ["HRT-KJT",[["Tyrese Proctor","Cleveland Cavaliers"],["Jase Richardson","Orlando Magic"],["Kasparas Jakučionis","Miami Heat"]]],
    ["HRT-NJN",[["Joan Beringer","Minnesota Timberwolves"],["Nolan Traore","Brooklyn Nets"],["Noa Essengue","Chicago Bulls"]]],
    ["HRT-NWA",[["Will Riley","Washington Wizards"],["Nique Clifford","Sacramento Kings"],["Adou Thiero","Los Angeles Lakers"]]],
    ["HRT-WCA",[["Chaz Lanier","Detroit Pistons"],["Walter Clayton Jr.","Utah Jazz"],["Alijah Martin","Toronto Raptors"]]],
  ];
  addMultiCards(hrtIS, hrtCards);
  console.log(`  Hoops Rookie Triples: ${hrtCards.length} cards`);

  // ═══════════════════════════════════════════════════════════════════════════
  // HOOPS ROOKIE/VETERAN DUALS
  // ═══════════════════════════════════════════════════════════════════════════
  const rvdIS = createInsertSet("Hoops Rookie/Veteran Duals");
  for (const [n, pr] of DUAL_PARS) createParallel(rvdIS, n, pr);

  const rvdCards: MultiCard[] = [
    ["RVD-CG",[["Collin Murray-Boyles","Toronto Raptors"],["Gradey Dick","Toronto Raptors"]]],
    ["RVD-CL",[["Dirk Nowitzki","Dallas Mavericks"],["Cooper Flagg","Dallas Mavericks"]]],
    ["RVD-DS",[["Stephon Castle","San Antonio Spurs"],["Dylan Harper","San Antonio Spurs"]]],
    ["RVD-KB",[["Brandon Miller","Charlotte Hornets"],["Kon Knueppel","Charlotte Hornets"]]],
    ["RVD-KR",[["Khaman Maluach","Phoenix Suns"],["Rudy Gobert","Minnesota Timberwolves"]]],
  ];
  addMultiCardsNoRookie(rvdIS, rvdCards);
  console.log(`  Hoops Rookie/Veteran Duals: ${rvdCards.length} cards`);

  // ═══════════════════════════════════════════════════════════════════════════
  // HOOPS 1989 SIGNATURES
  // ═══════════════════════════════════════════════════════════════════════════
  const s89IS = createInsertSet("Hoops 1989 Signatures");
  for (const [n, pr] of SIG89_PARS) createParallel(s89IS, n, pr);

  const s89Cards: Card[] = [
    ["89S-AB","Ace Bailey","Utah Jazz"],["89S-AFA","Al-Farouq Aminu","Portland Trail Blazers"],["89S-AH","Al Horford","Boston Celtics"],["89S-AI","Allen Iverson","Philadelphia 76ers"],["89S-AJ","AJ Johnson","Washington Wizards"],["89S-AN","Asa Newell","Atlanta Hawks"],["89S-AW","Amari Williams","Boston Celtics"],["89S-CD","Clyde Drexler","Portland Trail Blazers"],["89S-CF","Cooper Flagg","Dallas Mavericks"],["89S-CH","Chet Holmgren","Oklahoma City Thunder"],["89S-DC","Devin Carter","Sacramento Kings"],["89S-DH","Dylan Harper","San Antonio Spurs"],["89S-DM","Donovan Mitchell","Cleveland Cavaliers"],["89S-DN","Dirk Nowitzki","Dallas Mavericks"],["89S-DR","David Robinson","San Antonio Spurs"],["89S-DRO","Dennis Rodman","Chicago Bulls"],["89S-DW","Danny Wolf","Brooklyn Nets"],["89S-EH","Elvin Hayes","Houston Rockets"],["89S-HO","Hakeem Olajuwon","Houston Rockets"],["89S-IS","Isaiah Stewart","Detroit Pistons"],["89S-JH","James Harden","Los Angeles Clippers"],["89S-JJB","JJ Barea","Dallas Mavericks"],["89S-JM","Jahmai Mashack","Memphis Grizzlies"],["89S-JS","Jerry Stackhouse","Detroit Pistons"],["89S-JSO","Jeremy Sochan","San Antonio Spurs"],["89S-JT","Jayson Tatum","Boston Celtics"],["89S-JTY","Jaylon Tyson","Cleveland Cavaliers"],["89S-KB","Koby Brea","Phoenix Suns"],["89S-KD","Kevin Durant","Houston Rockets"],["89S-KJ","Kam Jones","Indiana Pacers"],["89S-KK","Kon Knueppel","Charlotte Hornets"],["89S-KM","Khaman Maluach","Phoenix Suns"],["89S-KMS","Kenyon Martin Sr.","New Jersey Nets"],["89S-KT","Karl-Anthony Towns","New York Knicks"],["89S-LB","Larry Bird","Boston Celtics"],["89S-LJ","LeBron James","Los Angeles Lakers"],["89S-LMC","Liam McNeeley","Charlotte Hornets"],["89S-LO","Lachlan Olbrich","Chicago Bulls"],["89S-MB","Mikal Bridges","New York Knicks"],["89S-MJ","Magic Johnson","Los Angeles Lakers"],["89S-MJA","Mark Jackson","New York Knicks"],["89S-MP","Michael Porter Jr.","Denver Nuggets"],["89S-MPE","Micah Peavy","New Orleans Pelicans"],["89S-MS","Marcus Smart","Memphis Grizzlies"],["89S-MSH","Max Shulga","Boston Celtics"],["89S-MW","Metta World Peace","Los Angeles Lakers"],["89S-NB","Nicolas Batum","Los Angeles Clippers"],["89S-NE","Noa Essengue","Chicago Bulls"],["89S-NP","Noah Penda","Orlando Magic"],["89S-PB","Paolo Banchero","Orlando Magic"],["89S-PP","Paul Pierce","Boston Celtics"],["89S-SB","Saddiq Bey","Washington Wizards"],["89S-SC","Stephen Curry","Golden State Warriors"],["89S-SO","Shaquille O'Neal","Los Angeles Lakers"],["89S-TM","Tracy McGrady","Toronto Raptors"],["89S-TP","Taelon Peter","Indiana Pacers"],["89S-VC","Vince Carter","Toronto Raptors"],["89S-WC","Walter Clayton Jr.","Utah Jazz"],["89S-WR","Will Richard","Golden State Warriors"],["89S-ZR","Zach Randolph","Memphis Grizzlies"],
  ];
  addCards(s89IS, s89Cards);
  console.log(`  Hoops 1989 Signatures: ${s89Cards.length} cards`);

  // ═══════════════════════════════════════════════════════════════════════════
  // HOOPS ROOKIE FIRST SIGNS
  // ═══════════════════════════════════════════════════════════════════════════
  const hfsIS = createInsertSet("Hoops Rookie First Signs");
  for (const [n, pr] of HFS_PARS) createParallel(hfsIS, n, pr);

  const hfsCards: Card[] = [
    ["HFS-AB","Ace Bailey","Utah Jazz",true],["HFS-AM","Alijah Martin","Toronto Raptors",true],["HFS-AN","Asa Newell","Atlanta Hawks",true],["HFS-AT","Adou Thiero","Los Angeles Lakers",true],["HFS-ATO","Alex Toohey","Golden State Warriors",true],["HFS-AW","Amari Williams","Boston Celtics",true],["HFS-BB","Brooks Barnhizer","Oklahoma City Thunder",true],["HFS-BS","Ben Saraf","Brooklyn Nets",true],["HFS-CC","Cedric Coward","Memphis Grizzlies",true],["HFS-CF","Cooper Flagg","Dallas Mavericks",true],["HFS-CL","Chaz Lanier","Detroit Pistons",true],["HFS-CM","Collin Murray-Boyles","Toronto Raptors",true],["HFS-DH","Dylan Harper","San Antonio Spurs",true],["HFS-DP","Drake Powell","Brooklyn Nets",true],["HFS-DQ","Derik Queen","New Orleans Pelicans",true],["HFS-DW","Danny Wolf","Brooklyn Nets",true],["HFS-ED","Egor Dëmin","Brooklyn Nets",true],["HFS-JB","Joan Beringer","Minnesota Timberwolves",true],["HFS-JBR","Johni Broome","Philadelphia 76ers",true],["HFS-JM","Jahmai Mashack","Memphis Grizzlies",true],["HFS-JR","Jase Richardson","Orlando Magic",true],["HFS-JS","Javon Small","Memphis Grizzlies",true],["HFS-JT","John Tonje","Utah Jazz",true],["HFS-JW","Jamir Watkins","Washington Wizards",true],["HFS-KB","Koby Brea","Phoenix Suns",true],["HFS-KJ","Kasparas Jakučionis","Miami Heat",true],["HFS-KJO","Kam Jones","Indiana Pacers",true],["HFS-KK","Kon Knueppel","Charlotte Hornets",true],["HFS-KM","Khaman Maluach","Phoenix Suns",true],["HFS-KS","Kobe Sanders","Los Angeles Clippers",true],["HFS-LM","Liam McNeeley","Charlotte Hornets",true],["HFS-LO","Lachlan Olbrich","Chicago Bulls",true],["HFS-MP","Micah Peavy","New Orleans Pelicans",true],["HFS-MR","Maxime Raynaud","Sacramento Kings",true],["HFS-MS","Max Shulga","Boston Celtics",true],["HFS-NC","Nique Clifford","Sacramento Kings",true],["HFS-NE","Noa Essengue","Chicago Bulls",true],["HFS-NP","Noah Penda","Orlando Magic",true],["HFS-NT","Nolan Traore","Brooklyn Nets",true],["HFS-RF","Rasheer Fleming","Phoenix Suns",true],["HFS-RK","Ryan Kalkbrenner","Charlotte Hornets",true],["HFS-SJ","Sion James","Charlotte Hornets",true],["HFS-TP","Tyrese Proctor","Cleveland Cavaliers",true],["HFS-TPE","Taelon Peter","Indiana Pacers",true],["HFS-TS","Thomas Sorber","Oklahoma City Thunder",true],["HFS-WC","Walter Clayton Jr.","Utah Jazz",true],["HFS-WR","Will Riley","Washington Wizards",true],["HFS-WRI","Will Richard","Golden State Warriors",true],["HFS-YH","Yang Hansen","Portland Trail Blazers",true],["HFS-YK","Yanic Konan-Niederhäuser","Los Angeles Clippers",true],
  ];
  addCards(hfsIS, hfsCards);
  console.log(`  Hoops Rookie First Signs: ${hfsCards.length} cards`);

  // ═══════════════════════════════════════════════════════════════════════════
  // HOOPS HYPER SIGNATURES
  // ═══════════════════════════════════════════════════════════════════════════
  const hhsIS = createInsertSet("Hoops Hyper Signatures");
  for (const [n, pr] of HHS_PARS) createParallel(hhsIS, n, pr);

  const hhsCards: Card[] = [
    ["HHS-AB","Anthony Black","Orlando Magic"],["HHS-ABO","Adem Bona","Philadelphia 76ers"],["HHS-AED","Anthony Edwards","Minnesota Timberwolves"],["HHS-AJ","AJ Johnson","Washington Wizards"],["HHS-AJJ","Andre Jackson Jr.","Milwaukee Bucks"],["HHS-AM","Ajay Mitchell","Oklahoma City Thunder"],["HHS-CC","Cam Christie","Los Angeles Clippers"],["HHS-CS","Cam Spencer","Memphis Grizzlies"],["HHS-CW","Cody Williams","Utah Jazz"],["HHS-DH","DaRon Holmes II","Denver Nuggets"],["HHS-DJ","Dillon Jones","Oklahoma City Thunder"],["HHS-GD","Gradey Dick","Toronto Raptors"],["HHS-GJ","GG Jackson II","Memphis Grizzlies"],["HHS-GN","Georges Niang","Atlanta Hawks"],["HHS-JH","Jordan Hawkins","New Orleans Pelicans"],["HHS-JHO","Jett Howard","Orlando Magic"],["HHS-JHS","Jalen Hood-Schifino","Philadelphia 76ers"],["HHS-JM","Jonathan Mogbo","Toronto Raptors"],["HHS-JS","Jamal Shead","Toronto Raptors"],["HHS-JT","Jayson Tatum","Boston Celtics"],["HHS-JTA","Jae'Sean Tate","Houston Rockets"],["HHS-JW","Jarace Walker","Indiana Pacers"],["HHS-JWE","Jaylen Wells","Memphis Grizzlies"],["HHS-JWI","Jaylin Williams","Oklahoma City Thunder"],["HHS-KD","Kevin Durant","Houston Rockets"],["HHS-KM","Kevin McCullar Jr.","New York Knicks"],["HHS-MS","Marcus Sasser","Detroit Pistons"],["HHS-NJ","Nikola Jokić","Denver Nuggets"],["HHS-NS","Nick Smith Jr.","Charlotte Hornets"],["HHS-NT","Nikola Topić","Oklahoma City Thunder"],["HHS-PL","Pelle Larsson","Miami Heat"],["HHS-QP","Quinten Post","Golden State Warriors"],["HHS-RH","Ronald Holland II","Detroit Pistons"],["HHS-RR","Rayan Rupert","Portland Trail Blazers"],["HHS-SC","Stephen Curry","Golden State Warriors"],["HHS-SCA","Stephon Castle","San Antonio Spurs"],["HHS-SGA","Shai Gilgeous-Alexander","Oklahoma City Thunder"],["HHS-SH","Scoot Henderson","Portland Trail Blazers"],["HHS-SP","Scotty Pippen Jr.","Memphis Grizzlies"],["HHS-TK","Tyler Kolek","New York Knicks"],["HHS-TS","Tyler Smith","Milwaukee Bucks"],["HHS-TSA","Tidjane Salaün","Charlotte Hornets"],["HHS-TSH","Terrence Shannon Jr.","Minnesota Timberwolves"],["HHS-VW","Victor Wembanyama","San Antonio Spurs"],["HHS-XT","Xavier Tillman","Boston Celtics"],["HHS-YM","Yves Missi","New Orleans Pelicans"],["HHS-ZW","Ziaire Williams","Brooklyn Nets"],
  ];
  addCards(hhsIS, hhsCards);
  console.log(`  Hoops Hyper Signatures: ${hhsCards.length} cards`);

  // ═══════════════════════════════════════════════════════════════════════════
  // BOUNCE HOUSE
  // ═══════════════════════════════════════════════════════════════════════════
  const bhIS = createInsertSet("Bounce House");
  for (const [n, pr] of HOBBY_INSERT_PARS) createParallel(bhIS, n, pr);

  const bhCards: Card[] = [
    ["BH-1","Anthony Edwards","Minnesota Timberwolves"],["BH-2","LeBron James","Los Angeles Lakers"],["BH-3","Victor Wembanyama","San Antonio Spurs"],["BH-4","Ja Morant","Memphis Grizzlies"],["BH-5","Giannis Antetokounmpo","Milwaukee Bucks"],["BH-6","Aaron Gordon","Denver Nuggets"],["BH-7","Shaedon Sharpe","Portland Trail Blazers"],["BH-8","Tyrese Haliburton","Indiana Pacers"],["BH-9","Anthony Davis","Dallas Mavericks"],["BH-10","Jayson Tatum","Boston Celtics"],["BH-11","Donovan Mitchell","Cleveland Cavaliers"],["BH-12","Kevin Durant","Houston Rockets"],["BH-13","Jalen Williams","Oklahoma City Thunder"],["BH-14","Zach LaVine","Sacramento Kings"],["BH-15","Jalen Johnson","Atlanta Hawks"],["BH-16","Cooper Flagg","Dallas Mavericks",true],["BH-17","Dylan Harper","San Antonio Spurs",true],["BH-18","VJ Edgecombe","Philadelphia 76ers",true],["BH-19","Kon Knueppel","Charlotte Hornets",true],["BH-20","Ace Bailey","Utah Jazz",true],["BH-21","Tre Johnson III","Washington Wizards",true],["BH-22","Jeremiah Fears","New Orleans Pelicans",true],["BH-23","Kasparas Jakučionis","Miami Heat",true],["BH-24","Asa Newell","Atlanta Hawks",true],["BH-25","Jase Richardson","Orlando Magic",true],
  ];
  addCards(bhIS, bhCards);
  console.log(`  Bounce House: ${bhCards.length} cards`);

  // ═══════════════════════════════════════════════════════════════════════════
  // NEXT EPISODE
  // ═══════════════════════════════════════════════════════════════════════════
  const neIS = createInsertSet("Next Episode");
  for (const [n, pr] of HOBBY_INSERT_PARS) createParallel(neIS, n, pr);

  const neCards: Card[] = [
    ["NE-1","Cooper Flagg","Dallas Mavericks",true],["NE-2","Dylan Harper","San Antonio Spurs",true],["NE-3","VJ Edgecombe","Philadelphia 76ers",true],["NE-4","Kon Knueppel","Charlotte Hornets",true],["NE-5","Ace Bailey","Utah Jazz",true],["NE-6","Tre Johnson III","Washington Wizards",true],["NE-7","Jeremiah Fears","New Orleans Pelicans",true],["NE-8","Egor Dëmin","Brooklyn Nets",true],["NE-9","Collin Murray-Boyles","Toronto Raptors",true],["NE-10","Khaman Maluach","Phoenix Suns",true],["NE-11","Cedric Coward","Memphis Grizzlies",true],["NE-12","Noa Essengue","Chicago Bulls",true],["NE-13","Derik Queen","New Orleans Pelicans",true],["NE-14","Carter Bryant","San Antonio Spurs",true],["NE-15","Asa Newell","Atlanta Hawks",true],["NE-16","Yang Hansen","Portland Trail Blazers",true],["NE-17","Joan Beringer","Minnesota Timberwolves",true],["NE-18","Walter Clayton Jr.","Utah Jazz",true],["NE-19","Jase Richardson","Orlando Magic",true],["NE-20","Kasparas Jakučionis","Miami Heat",true],
  ];
  addCards(neIS, neCards);
  console.log(`  Next Episode: ${neCards.length} cards`);

  // ═══════════════════════════════════════════════════════════════════════════
  // DUNKUMENTORY
  // ═══════════════════════════════════════════════════════════════════════════
  const dIS = createInsertSet("Dunkumentory");
  for (const [n, pr] of HOBBY_INSERT_PARS) createParallel(dIS, n, pr);

  const dCards: Card[] = [
    ["D-1","Anthony Edwards","Minnesota Timberwolves"],["D-2","Ja Morant","Memphis Grizzlies"],["D-3","Giannis Antetokounmpo","Milwaukee Bucks"],["D-4","LeBron James","Los Angeles Lakers"],["D-5","Pascal Siakam","Indiana Pacers"],["D-6","Vince Carter","Toronto Raptors"],["D-7","Spud Webb","Atlanta Hawks"],["D-8","Dominique Wilkins","Atlanta Hawks"],["D-9","Clyde Drexler","Portland Trail Blazers"],["D-10","Tracy McGrady","Orlando Magic"],["D-11","Cooper Flagg","Dallas Mavericks",true],["D-12","Dylan Harper","San Antonio Spurs",true],["D-13","VJ Edgecombe","Philadelphia 76ers",true],["D-14","Ace Bailey","Utah Jazz",true],["D-15","Khaman Maluach","Phoenix Suns",true],
  ];
  addCards(dIS, dCards);
  console.log(`  Dunkumentory: ${dCards.length} cards`);

  // ═══════════════════════════════════════════════════════════════════════════
  // PAY ATTENTION
  // ═══════════════════════════════════════════════════════════════════════════
  const paIS = createInsertSet("Pay Attention");
  for (const [n, pr] of HOBBY_INSERT_PARS) createParallel(paIS, n, pr);

  const paCards: Card[] = [
    ["PA-1","Anthony Edwards","Minnesota Timberwolves"],["PA-2","Victor Wembanyama","San Antonio Spurs"],["PA-3","Ja Morant","Memphis Grizzlies"],["PA-4","Giannis Antetokounmpo","Milwaukee Bucks"],["PA-5","Tyrese Haliburton","Indiana Pacers"],["PA-6","Jayson Tatum","Boston Celtics"],["PA-7","Donovan Mitchell","Cleveland Cavaliers"],["PA-8","Kevin Durant","Houston Rockets"],["PA-9","Luka Dončić","Los Angeles Lakers"],["PA-10","Nikola Jokić","Denver Nuggets"],["PA-11","Cade Cunningham","Detroit Pistons"],["PA-12","Shai Gilgeous-Alexander","Oklahoma City Thunder"],["PA-13","Jalen Brunson","New York Knicks"],["PA-14","Paolo Banchero","Orlando Magic"],["PA-15","Devin Booker","Phoenix Suns"],["PA-16","Cooper Flagg","Dallas Mavericks",true],["PA-17","Dylan Harper","San Antonio Spurs",true],["PA-18","VJ Edgecombe","Philadelphia 76ers",true],["PA-19","Kon Knueppel","Charlotte Hornets",true],["PA-20","Ace Bailey","Utah Jazz",true],
  ];
  addCards(paIS, paCards);
  console.log(`  Pay Attention: ${paCards.length} cards`);

  // ═══════════════════════════════════════════════════════════════════════════
  // HOOPERS
  // ═══════════════════════════════════════════════════════════════════════════
  const hIS = createInsertSet("Hoopers");
  for (const [n, pr] of HOBBY_INSERT_PARS) createParallel(hIS, n, pr);

  const hCards: Card[] = [
    ["H-1","Nikola Jokić","Denver Nuggets"],["H-2","Shai Gilgeous-Alexander","Oklahoma City Thunder"],["H-3","Luka Dončić","Los Angeles Lakers"],["H-4","Giannis Antetokounmpo","Milwaukee Bucks"],["H-5","Stephen Curry","Golden State Warriors"],["H-6","Anthony Edwards","Minnesota Timberwolves"],["H-7","Tyrese Haliburton","Indiana Pacers"],["H-8","Donovan Mitchell","Cleveland Cavaliers"],["H-9","Jalen Brunson","New York Knicks"],["H-10","Jayson Tatum","Boston Celtics"],["H-11","Victor Wembanyama","San Antonio Spurs"],["H-12","LeBron James","Los Angeles Lakers"],["H-13","Anthony Davis","Dallas Mavericks"],["H-14","Kevin Durant","Houston Rockets"],["H-15","Cade Cunningham","Detroit Pistons"],["H-16","Cooper Flagg","Dallas Mavericks",true],["H-17","Dylan Harper","San Antonio Spurs",true],["H-18","Kon Knueppel","Charlotte Hornets",true],["H-19","Ace Bailey","Utah Jazz",true],["H-20","Egor Dëmin","Brooklyn Nets",true],
  ];
  addCards(hIS, hCards);
  console.log(`  Hoopers: ${hCards.length} cards`);

  // ═══════════════════════════════════════════════════════════════════════════
  // FINALS PURSUIT — placeholder with key stars (no explicit checklist provided)
  // ═══════════════════════════════════════════════════════════════════════════
  const fpIS = createInsertSet("Finals Pursuit");
  // No parallels — tiers are odds keys

  const fpCards: Card[] = [
    ["FP-1","Jayson Tatum","Boston Celtics"],["FP-2","Jaylen Brown","Boston Celtics"],["FP-3","Jrue Holiday","Boston Celtics"],["FP-4","Derrick White","Boston Celtics"],["FP-5","Luka Dončić","Los Angeles Lakers"],["FP-6","Kyrie Irving","Dallas Mavericks"],["FP-7","Nikola Jokić","Denver Nuggets"],["FP-8","Shai Gilgeous-Alexander","Oklahoma City Thunder"],["FP-9","Anthony Edwards","Minnesota Timberwolves"],["FP-10","Giannis Antetokounmpo","Milwaukee Bucks"],["FP-11","Jimmy Butler III","Golden State Warriors"],["FP-12","Stephen Curry","Golden State Warriors"],["FP-13","Kevin Durant","Houston Rockets"],["FP-14","Victor Wembanyama","San Antonio Spurs"],["FP-15","LeBron James","Los Angeles Lakers"],["FP-16","Donovan Mitchell","Cleveland Cavaliers"],["FP-17","Jalen Brunson","New York Knicks"],["FP-18","Devin Booker","Phoenix Suns"],["FP-19","Tyrese Haliburton","Indiana Pacers"],["FP-20","Ja Morant","Memphis Grizzlies"],
  ];
  addCards(fpIS, fpCards);
  console.log(`  Finals Pursuit: ${fpCards.length} cards`);

  // ═══════════════════════════════════════════════════════════════════════════
  // OASIS
  // ═══════════════════════════════════════════════════════════════════════════
  const oIS = createInsertSet("Oasis");
  for (const [n, pr] of PLAT_ONLY) createParallel(oIS, n, pr);

  const oCards: Card[] = [
    ["O-1","Shai Gilgeous-Alexander","Oklahoma City Thunder"],["O-2","Nikola Jokić","Denver Nuggets"],["O-3","Luka Dončić","Los Angeles Lakers"],["O-4","Anthony Edwards","Minnesota Timberwolves"],["O-5","Jalen Brunson","New York Knicks"],["O-6","VJ Edgecombe","Philadelphia 76ers",true],["O-7","Kevin Durant","Houston Rockets"],["O-8","Giannis Antetokounmpo","Milwaukee Bucks"],["O-9","Stephen Curry","Golden State Warriors"],["O-10","Donovan Mitchell","Cleveland Cavaliers"],["O-11","LeBron James","Los Angeles Lakers"],["O-12","Cade Cunningham","Detroit Pistons"],["O-13","Tyrese Haliburton","Indiana Pacers"],["O-14","Jayson Tatum","Boston Celtics"],["O-15","Kyrie Irving","Dallas Mavericks"],["O-16","Devin Booker","Phoenix Suns"],["O-17","Paolo Banchero","Orlando Magic"],["O-18","Ja Morant","Memphis Grizzlies"],["O-19","Bam Adebayo","Miami Heat"],["O-20","Trae Young","Atlanta Hawks"],["O-21","Cooper Flagg","Dallas Mavericks",true],["O-22","Dylan Harper","San Antonio Spurs",true],["O-23","Kon Knueppel","Charlotte Hornets",true],["O-24","Ace Bailey","Utah Jazz",true],["O-25","Yang Hansen","Portland Trail Blazers",true],
  ];
  addCards(oIS, oCards);
  console.log(`  Oasis: ${oCards.length} cards`);

  // ═══════════════════════════════════════════════════════════════════════════
  // JOY
  // ═══════════════════════════════════════════════════════════════════════════
  const joyIS = createInsertSet("Joy");
  for (const [n, pr] of PLAT_ONLY) createParallel(joyIS, n, pr);

  const joyCards: Card[] = [
    ["JOY-1","Nikola Jokić","Denver Nuggets"],["JOY-2","Luka Dončić","Los Angeles Lakers"],["JOY-3","Anthony Edwards","Minnesota Timberwolves"],["JOY-4","Victor Wembanyama","San Antonio Spurs"],["JOY-5","Giannis Antetokounmpo","Milwaukee Bucks"],["JOY-6","Stephen Curry","Golden State Warriors"],["JOY-7","LeBron James","Los Angeles Lakers"],["JOY-8","Tyrese Haliburton","Indiana Pacers"],["JOY-9","Jayson Tatum","Boston Celtics"],["JOY-10","Devin Booker","Phoenix Suns"],
  ];
  addCards(joyIS, joyCards);
  console.log(`  Joy: ${joyCards.length} cards`);

  // ═══════════════════════════════════════════════════════════════════════════
  // CHECKMATE
  // ═══════════════════════════════════════════════════════════════════════════
  const cIS = createInsertSet("Checkmate");
  for (const [n, pr] of PLAT_ONLY) createParallel(cIS, n, pr);

  const cCards: Card[] = [
    ["C-1","Nikola Jokić","Denver Nuggets"],["C-2","Shai Gilgeous-Alexander","Oklahoma City Thunder"],["C-3","Luka Dončić","Los Angeles Lakers"],["C-4","Giannis Antetokounmpo","Milwaukee Bucks"],["C-5","Stephen Curry","Golden State Warriors"],["C-6","Anthony Edwards","Minnesota Timberwolves"],["C-7","Tyrese Haliburton","Indiana Pacers"],["C-8","Donovan Mitchell","Cleveland Cavaliers"],["C-9","Jalen Brunson","New York Knicks"],["C-10","Jayson Tatum","Boston Celtics"],["C-11","Victor Wembanyama","San Antonio Spurs"],["C-12","LeBron James","Los Angeles Lakers"],["C-13","Anthony Davis","Dallas Mavericks"],["C-14","Kevin Durant","Houston Rockets"],["C-15","Cade Cunningham","Detroit Pistons"],["C-16","Brandon Miller","Charlotte Hornets"],["C-17","Trae Young","Atlanta Hawks"],["C-18","Kawhi Leonard","Los Angeles Clippers"],["C-19","Ja Morant","Memphis Grizzlies"],["C-20","Bam Adebayo","Miami Heat"],["C-21","Darius Garland","Cleveland Cavaliers"],["C-22","Devin Booker","Phoenix Suns"],["C-23","Kyrie Irving","Dallas Mavericks"],["C-24","Tyrese Maxey","Philadelphia 76ers"],["C-25","Paolo Banchero","Orlando Magic"],["C-26","Jalen Williams","Oklahoma City Thunder"],["C-27","Jaylen Brown","Boston Celtics"],["C-28","Pascal Siakam","Indiana Pacers"],["C-29","Karl-Anthony Towns","New York Knicks"],["C-30","LaMelo Ball","Charlotte Hornets"],
  ];
  addCards(cIS, cCards);
  console.log(`  Checkmate: ${cCards.length} cards`);

  // ═══════════════════════════════════════════════════════════════════════════
  // HOOPNOTIC
  // ═══════════════════════════════════════════════════════════════════════════
  const hnIS = createInsertSet("Hoopnotic");
  for (const [n, pr] of PLAT_ONLY) createParallel(hnIS, n, pr);

  const hnCards: Card[] = [
    ["HN-1","Anthony Edwards","Minnesota Timberwolves"],["HN-2","Cade Cunningham","Detroit Pistons"],["HN-3","Devin Booker","Phoenix Suns"],["HN-4","Donovan Mitchell","Cleveland Cavaliers"],["HN-5","Giannis Antetokounmpo","Milwaukee Bucks"],["HN-6","Jalen Brunson","New York Knicks"],["HN-7","Jayson Tatum","Boston Celtics"],["HN-8","Kevin Durant","Houston Rockets"],["HN-9","LeBron James","Los Angeles Lakers"],["HN-10","Luka Dončić","Los Angeles Lakers"],["HN-11","Nikola Jokić","Denver Nuggets"],["HN-12","Shai Gilgeous-Alexander","Oklahoma City Thunder"],["HN-13","Stephen Curry","Golden State Warriors"],["HN-14","Tyrese Haliburton","Indiana Pacers"],["HN-15","Victor Wembanyama","San Antonio Spurs"],["HN-16","Ja Morant","Memphis Grizzlies"],["HN-17","Kyrie Irving","Dallas Mavericks"],["HN-18","Paolo Banchero","Orlando Magic"],["HN-19","Pascal Siakam","Indiana Pacers"],["HN-20","James Harden","Los Angeles Clippers"],["HN-21","Dirk Nowitzki","Dallas Mavericks"],["HN-22","Allen Iverson","Philadelphia 76ers"],["HN-23","Shaquille O'Neal","Los Angeles Lakers"],["HN-24","Kevin Garnett","Minnesota Timberwolves"],["HN-25","Larry Bird","Boston Celtics"],["HN-26","Cooper Flagg","Dallas Mavericks",true],["HN-27","Dylan Harper","San Antonio Spurs",true],["HN-28","VJ Edgecombe","Philadelphia 76ers",true],["HN-29","Kon Knueppel","Charlotte Hornets",true],["HN-30","Ace Bailey","Utah Jazz",true],["HN-31","Tre Johnson III","Washington Wizards",true],["HN-32","Jeremiah Fears","New Orleans Pelicans",true],["HN-33","Egor Dëmin","Brooklyn Nets",true],["HN-34","Collin Murray-Boyles","Toronto Raptors",true],["HN-35","Khaman Maluach","Phoenix Suns",true],
  ];
  addCards(hnIS, hnCards);
  console.log(`  Hoopnotic: ${hnCards.length} cards`);

  // ═══════════════════════════════════════════════════════════════════════════
  // HARDWIRED
  // ═══════════════════════════════════════════════════════════════════════════
  const hwIS = createInsertSet("Hardwired");
  for (const [n, pr] of RETAIL_INSERT_PARS) createParallel(hwIS, n, pr);

  const hwCards: Card[] = [
    ["HW-1","Shai Gilgeous-Alexander","Oklahoma City Thunder"],["HW-2","Nikola Jokić","Denver Nuggets"],["HW-3","Luka Dončić","Los Angeles Lakers"],["HW-4","Anthony Edwards","Minnesota Timberwolves"],["HW-5","Jalen Brunson","New York Knicks"],["HW-6","Victor Wembanyama","San Antonio Spurs"],["HW-7","Kevin Durant","Houston Rockets"],["HW-8","Giannis Antetokounmpo","Milwaukee Bucks"],["HW-9","Stephen Curry","Golden State Warriors"],["HW-10","Donovan Mitchell","Cleveland Cavaliers"],["HW-11","LeBron James","Los Angeles Lakers"],["HW-12","Cade Cunningham","Detroit Pistons"],["HW-13","Tyrese Haliburton","Indiana Pacers"],["HW-14","Jayson Tatum","Boston Celtics"],["HW-15","Devin Booker","Phoenix Suns"],["HW-16","Paolo Banchero","Orlando Magic"],["HW-17","Anthony Davis","Dallas Mavericks"],["HW-18","Evan Mobley","Cleveland Cavaliers"],["HW-19","De'Aaron Fox","San Antonio Spurs"],["HW-20","Tyrese Maxey","Philadelphia 76ers"],["HW-21","Cooper Flagg","Dallas Mavericks",true],["HW-22","Dylan Harper","San Antonio Spurs",true],["HW-23","VJ Edgecombe","Philadelphia 76ers",true],["HW-24","Kon Knueppel","Charlotte Hornets",true],["HW-25","Ace Bailey","Utah Jazz",true],
  ];
  addCards(hwIS, hwCards);
  console.log(`  Hardwired: ${hwCards.length} cards`);

  // ═══════════════════════════════════════════════════════════════════════════
  // THE BUZZ
  // ═══════════════════════════════════════════════════════════════════════════
  const tbIS = createInsertSet("The Buzz");
  for (const [n, pr] of RETAIL_INSERT_PARS) createParallel(tbIS, n, pr);

  const tbCards: Card[] = [
    ["TB-1","Cooper Flagg","Dallas Mavericks",true],["TB-2","Dylan Harper","San Antonio Spurs",true],["TB-3","VJ Edgecombe","Philadelphia 76ers",true],["TB-4","Kon Knueppel","Charlotte Hornets",true],["TB-5","Ace Bailey","Utah Jazz",true],["TB-6","Tre Johnson III","Washington Wizards",true],["TB-7","Jeremiah Fears","New Orleans Pelicans",true],["TB-8","Egor Dëmin","Brooklyn Nets",true],["TB-9","Collin Murray-Boyles","Toronto Raptors",true],["TB-10","Khaman Maluach","Phoenix Suns",true],["TB-11","Cedric Coward","Memphis Grizzlies",true],["TB-12","Noa Essengue","Chicago Bulls",true],["TB-13","Derik Queen","New Orleans Pelicans",true],["TB-14","Carter Bryant","San Antonio Spurs",true],["TB-15","Thomas Sorber","Oklahoma City Thunder",true],["TB-16","Yang Hansen","Portland Trail Blazers",true],["TB-17","Joan Beringer","Minnesota Timberwolves",true],["TB-18","Walter Clayton Jr.","Utah Jazz",true],["TB-19","Nolan Traore","Brooklyn Nets",true],["TB-20","Kasparas Jakučionis","Miami Heat",true],["TB-21","Will Riley","Washington Wizards",true],["TB-22","Drake Powell","Brooklyn Nets",true],["TB-23","Asa Newell","Atlanta Hawks",true],["TB-24","Nique Clifford","Sacramento Kings",true],["TB-25","Jase Richardson","Orlando Magic",true],["TB-26","Ben Saraf","Brooklyn Nets",true],["TB-27","Danny Wolf","Brooklyn Nets",true],["TB-28","Hugo González","Boston Celtics",true],["TB-29","Liam McNeeley","Charlotte Hornets",true],["TB-30","Yanic Konan-Niederhäuser","Los Angeles Clippers",true],
  ];
  addCards(tbIS, tbCards);
  console.log(`  The Buzz: ${tbCards.length} cards`);

  // ═══════════════════════════════════════════════════════════════════════════
  // NET 2 NET
  // ═══════════════════════════════════════════════════════════════════════════
  const ntnIS = createInsertSet("Net to Net");
  for (const [n, pr] of RETAIL_INSERT_PARS) createParallel(ntnIS, n, pr);

  const ntnCards: Card[] = [
    ["NTN-1","Bam Adebayo","Miami Heat"],["NTN-2","Giannis Antetokounmpo","Milwaukee Bucks"],["NTN-3","LaMelo Ball","Charlotte Hornets"],["NTN-4","Paolo Banchero","Orlando Magic"],["NTN-5","Devin Booker","Phoenix Suns"],["NTN-6","Jaylen Brown","Boston Celtics"],["NTN-7","Jalen Brunson","New York Knicks"],["NTN-8","Cade Cunningham","Detroit Pistons"],["NTN-9","Stephen Curry","Golden State Warriors"],["NTN-10","Anthony Davis","Dallas Mavericks"],["NTN-11","Luka Dončić","Los Angeles Lakers"],["NTN-12","Kevin Durant","Houston Rockets"],["NTN-13","Anthony Edwards","Minnesota Timberwolves"],["NTN-14","Shai Gilgeous-Alexander","Oklahoma City Thunder"],["NTN-15","Tyrese Haliburton","Indiana Pacers"],["NTN-16","Kyrie Irving","Dallas Mavericks"],["NTN-17","LeBron James","Los Angeles Lakers"],["NTN-18","Nikola Jokić","Denver Nuggets"],["NTN-19","Kawhi Leonard","Los Angeles Clippers"],["NTN-20","Tyrese Maxey","Philadelphia 76ers"],["NTN-21","Brandon Miller","Charlotte Hornets"],["NTN-22","Donovan Mitchell","Cleveland Cavaliers"],["NTN-23","Ja Morant","Memphis Grizzlies"],["NTN-24","Domantas Sabonis","Sacramento Kings"],["NTN-25","Pascal Siakam","Indiana Pacers"],["NTN-26","Jayson Tatum","Boston Celtics"],["NTN-27","Karl-Anthony Towns","New York Knicks"],["NTN-28","Victor Wembanyama","San Antonio Spurs"],["NTN-29","Jalen Williams","Oklahoma City Thunder"],["NTN-30","Trae Young","Atlanta Hawks"],
  ];
  addCards(ntnIS, ntnCards);
  console.log(`  Net to Net: ${ntnCards.length} cards`);

  // ═══════════════════════════════════════════════════════════════════════════
  // JAM PACKED
  // ═══════════════════════════════════════════════════════════════════════════
  const jpIS = createInsertSet("Jam-Packed");
  for (const [n, pr] of RETAIL_INSERT_PARS) createParallel(jpIS, n, pr);

  const jpCards: Card[] = [
    ["JP-1","Anthony Edwards","Minnesota Timberwolves"],["JP-2","Ja Morant","Memphis Grizzlies"],["JP-3","Giannis Antetokounmpo","Milwaukee Bucks"],["JP-4","LeBron James","Los Angeles Lakers"],["JP-5","Obi Toppin","Indiana Pacers"],["JP-6","Donovan Mitchell","Cleveland Cavaliers"],["JP-7","Aaron Gordon","Denver Nuggets"],["JP-8","Zach LaVine","Sacramento Kings"],["JP-9","Shaedon Sharpe","Portland Trail Blazers"],["JP-10","Derrick Jones Jr.","Los Angeles Clippers"],["JP-11","Cooper Flagg","Dallas Mavericks",true],["JP-12","Dylan Harper","San Antonio Spurs",true],["JP-13","Ace Bailey","Utah Jazz",true],["JP-14","Yang Hansen","Portland Trail Blazers",true],["JP-15","Asa Newell","Atlanta Hawks",true],
  ];
  addCards(jpIS, jpCards);
  console.log(`  Jam-Packed: ${jpCards.length} cards`);

  // ═══════════════════════════════════════════════════════════════════════════
  // BLOCK BY BLOCK
  // ═══════════════════════════════════════════════════════════════════════════
  const bybIS = createInsertSet("Block by Block");
  for (const [n, pr] of PLAT_ONLY) createParallel(bybIS, n, pr);

  const bybCards: Card[] = [
    ["BYB-1","Cooper Flagg","Dallas Mavericks",true],["BYB-2","Dylan Harper","San Antonio Spurs",true],["BYB-3","VJ Edgecombe","Philadelphia 76ers",true],["BYB-4","Kon Knueppel","Charlotte Hornets",true],["BYB-5","Ace Bailey","Utah Jazz",true],["BYB-6","Tre Johnson III","Washington Wizards",true],["BYB-7","Jeremiah Fears","New Orleans Pelicans",true],["BYB-8","Egor Dëmin","Brooklyn Nets",true],["BYB-9","Collin Murray-Boyles","Toronto Raptors",true],["BYB-10","Khaman Maluach","Phoenix Suns",true],["BYB-11","Cedric Coward","Memphis Grizzlies",true],["BYB-12","Noa Essengue","Chicago Bulls",true],["BYB-13","Derik Queen","New Orleans Pelicans",true],["BYB-14","Carter Bryant","San Antonio Spurs",true],["BYB-15","Thomas Sorber","Oklahoma City Thunder",true],["BYB-16","Yang Hansen","Portland Trail Blazers",true],["BYB-17","Joan Beringer","Minnesota Timberwolves",true],["BYB-18","Walter Clayton Jr.","Utah Jazz",true],["BYB-19","Nolan Traore","Brooklyn Nets",true],["BYB-20","Kasparas Jakučionis","Miami Heat",true],["BYB-21","Will Riley","Washington Wizards",true],["BYB-22","Drake Powell","Brooklyn Nets",true],["BYB-23","Asa Newell","Atlanta Hawks",true],["BYB-24","Nique Clifford","Sacramento Kings",true],["BYB-25","Jase Richardson","Orlando Magic",true],["BYB-26","Ben Saraf","Brooklyn Nets",true],["BYB-27","Danny Wolf","Brooklyn Nets",true],["BYB-28","Hugo González","Boston Celtics",true],["BYB-29","Liam McNeeley","Charlotte Hornets",true],["BYB-30","Yanic Konan-Niederhäuser","Los Angeles Clippers",true],["BYB-31","Rasheer Fleming","Phoenix Suns",true],["BYB-32","Noah Penda","Orlando Magic",true],["BYB-33","Sion James","Charlotte Hornets",true],["BYB-34","Ryan Kalkbrenner","Charlotte Hornets",true],["BYB-35","Johni Broome","Philadelphia 76ers",true],["BYB-36","Adou Thiero","Los Angeles Lakers",true],["BYB-37","Chaz Lanier","Detroit Pistons",true],["BYB-38","Kam Jones","Indiana Pacers",true],["BYB-39","Alijah Martin","Toronto Raptors",true],["BYB-40","Maxime Raynaud","Sacramento Kings",true],
  ];
  addCards(bybIS, bybCards);
  console.log(`  Block by Block: ${bybCards.length} cards`);

  // ═══════════════════════════════════════════════════════════════════════════
  // BOOM SHAKA LAKA
  // ═══════════════════════════════════════════════════════════════════════════
  const boIS = createInsertSet("Boombastic");
  for (const [n, pr] of PLAT_ONLY) createParallel(boIS, n, pr);

  const boCards: Card[] = [
    ["BO-1","Nikola Jokić","Denver Nuggets"],["BO-2","Shai Gilgeous-Alexander","Oklahoma City Thunder"],["BO-3","Luka Dončić","Los Angeles Lakers"],["BO-4","Giannis Antetokounmpo","Milwaukee Bucks"],["BO-5","Stephen Curry","Golden State Warriors"],["BO-6","Anthony Edwards","Minnesota Timberwolves"],["BO-7","Jalen Brunson","New York Knicks"],["BO-8","Victor Wembanyama","San Antonio Spurs"],["BO-9","Kevin Durant","Houston Rockets"],["BO-10","Cooper Flagg","Dallas Mavericks",true],
  ];
  addCards(boIS, boCards);
  console.log(`  Boombastic: ${boCards.length} cards`);
});

// ─── Execute ──────────────────────────────────────────────────────────────────
seedAll();

// ─── Generate slugs ───────────────────────────────────────────────────────────
function slugify(text: string): string {
  return text
    .toLowerCase()
    .trim()
    .replace(/[^\w\s-]/g, "")
    .replace(/[\s_]+/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "");
}

const allPlayers = db
  .prepare("SELECT id, name FROM players WHERE set_id = ?")
  .all(SET_ID) as { id: number; name: string }[];

const usedSlugs = new Set<string>();
const updateSlug = db.prepare("UPDATE players SET slug = ? WHERE id = ?");
for (const p of allPlayers) {
  let slug = slugify(p.name);
  if (usedSlugs.has(slug)) {
    let i = 2;
    while (usedSlugs.has(`${slug}-${i}`)) i++;
    slug = `${slug}-${i}`;
  }
  usedSlugs.add(slug);
  updateSlug.run(slug, p.id);
}

// ─── Stats ────────────────────────────────────────────────────────────────────
const playerCount = (
  db.prepare("SELECT COUNT(*) as n FROM players WHERE set_id = ?").get(SET_ID) as { n: number }
).n;
const appCount = (
  db
    .prepare(
      "SELECT COUNT(*) as n FROM player_appearances pa JOIN insert_sets i ON pa.insert_set_id = i.id WHERE i.set_id = ?"
    )
    .get(SET_ID) as { n: number }
).n;
const isCount = (
  db.prepare("SELECT COUNT(*) as n FROM insert_sets WHERE set_id = ?").get(SET_ID) as { n: number }
).n;
const parCount = (
  db
    .prepare(
      "SELECT COUNT(*) as n FROM parallels p JOIN insert_sets i ON p.insert_set_id = i.id WHERE i.set_id = ?"
    )
    .get(SET_ID) as { n: number }
).n;

console.log(`\nDone! Set ID: ${SET_ID}`);
console.log(`  Players: ${playerCount}`);
console.log(`  Appearances: ${appCount}`);
console.log(`  Insert sets: ${isCount}`);
console.log(`  Parallels: ${parCount}`);

db.close();
