"""
Seed: 2025-26 Topps Motif Basketball — Base + pack odds + parallels + subset shells.
100 base, 23 subsets (most pending card data), dual-format pack odds (Hobby + FDI).
Usage: python3 scripts/seed_motif_basketball_2025.py
"""
import sqlite3, os, json, re, unicodedata

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
db = sqlite3.connect(DB_PATH)
db.execute("PRAGMA journal_mode=WAL")
db.execute("PRAGMA foreign_keys=ON")

box_config = json.dumps({
    "hobby": {"cards_per_pack": None, "packs_per_box": None, "boxes_per_case": None,
              "notes": "Box configuration TBA"},
    "first_day_issue": {"cards_per_pack": None, "packs_per_box": None, "boxes_per_case": None,
                        "notes": "First Day Issue — box configuration TBA"},
})

# Build pack odds (dual-format nested JSON)
pack_odds_data = {
    "hobby": {
        "Base": "1:2", "Pastel Pink": "1:2", "Quin Gold": "1:4", "Ultramarine Blue": "1:5",
        "Cadmium Orange": "1:7", "Majesty Purple": "1:11", "Winsor Green": "1:16",
        "Pyrrol Scarlet": "1:32", "Platinum": "1:157", "Printing Plate": "1:40",
        # Motif Rookie Relic Autographs + variants
        "Motif Rookie Relic Autographs": "1:8", "Motif Rookie Dual Relic Autographs": "1:8",
        "Motif Rookie Triple Relic Autographs": "1:8", "Motif Rookie Quad Relic Autographs": "1:22",
        "Motif Rookie Relic Autographs Quin Gold": "1:12", "Motif Rookie Dual Relic Autographs Quin Gold": "1:12",
        "Motif Rookie Triple Relic Autographs Quin Gold": "1:12", "Motif Rookie Quad Relic Autographs Quin Gold": "1:34",
        "Motif Rookie Relic Autographs Ultramarine Blue": "1:14", "Motif Rookie Dual Relic Autographs Ultramarine Blue": "1:14",
        "Motif Rookie Triple Relic Autographs Ultramarine Blue": "1:14", "Motif Rookie Quad Relic Autographs Ultramarine Blue": "1:42",
        "Motif Rookie Relic Autographs Cadmium Orange": "1:22", "Motif Rookie Dual Relic Autographs Cadmium Orange": "1:22",
        "Motif Rookie Triple Relic Autographs Cadmium Orange": "1:22", "Motif Rookie Quad Relic Autographs Cadmium Orange": "1:66",
        "Motif Rookie Relic Autographs Winsor Green": "1:55", "Motif Rookie Dual Relic Autographs Winsor Green": "1:55",
        "Motif Rookie Triple Relic Autographs Winsor Green": "1:55", "Motif Rookie Quad Relic Autographs Winsor Green": "1:167",
        "Motif Rookie Relic Autographs Pyrrol Scarlet": "1:111", "Motif Rookie Dual Relic Autographs Pyrrol Scarlet": "1:111",
        "Motif Rookie Triple Relic Autographs Pyrrol Scarlet": "1:111", "Motif Rookie Quad Relic Autographs Pyrrol Scarlet": "1:343",
        "Motif Rookie Relic Autographs Platinum": "1:283", "Motif Rookie Dual Relic Autographs Platinum": "1:597",
        "Motif Rookie Triple Relic Autographs Platinum": "1:597", "Motif Rookie Quad Relic Autographs Platinum": "1:2,303",
        # Splatter, Statistical, Apprentice
        "Splatter Signatures": "1:17", "Statistical Showpiece Signatures": "1:53", "Apprentice Numerical Autographs": "1:25",
        # Abstract Ink, Acrylic Drip, Still Life
        "Abstract Ink Signatures": "1:4", "Acrylic Drip Autographs": "1:4", "Still Life Signatures": "1:15",
        "Abstract Ink Signatures Ultramarine Blue": "1:11", "Acrylic Drip Autographs Ultramarine Blue": "1:11", "Still Life Signatures Ultramarine Blue": "1:23",
        "Abstract Ink Signatures Cadmium Orange": "1:17", "Acrylic Drip Autographs Cadmium Orange": "1:17", "Still Life Signatures Cadmium Orange": "1:33",
        "Abstract Ink Signatures Winsor Green": "1:41", "Acrylic Drip Autographs Winsor Green": "1:41", "Still Life Signatures Winsor Green": "1:83",
        "Abstract Ink Signatures Pyrrol Scarlet": "1:83", "Acrylic Drip Autographs Pyrrol Scarlet": "1:83", "Still Life Signatures Pyrrol Scarlet": "1:167",
        "Abstract Ink Signatures Platinum": "1:436", "Acrylic Drip Autographs Platinum": "1:436", "Still Life Signatures Platinum": "1:949",
        # Aquarelle, Deco-Rated
        "Aquarelle Autographs": "1:4", "Deco-Rated Autographs": "1:4",
        "Aquarelle Autographs Ultramarine Blue": "1:9", "Deco-Rated Autographs Ultramarine Blue": "1:9",
        "Aquarelle Autographs Cadmium Orange": "1:13", "Deco-Rated Autographs Cadmium Orange": "1:14",
        "Aquarelle Autographs Winsor Green": "1:33", "Deco-Rated Autographs Winsor Green": "1:33",
        "Aquarelle Autographs Pyrrol Scarlet": "1:66", "Deco-Rated Autographs Pyrrol Scarlet": "1:66",
        "Aquarelle Autographs Platinum": "1:343", "Deco-Rated Autographs Platinum": "1:343",
        # Pick and Pop Art, Charcoal, Spray Paint
        "Pick and Pop Art Signatures": "1:7", "Charcoal Signatures": "1:8", "Spray Paint Signatures": "1:5",
        "Pick and Pop Art Signatures Ultramarine Blue": "1:14", "Charcoal Signatures Ultramarine Blue": "1:17", "Spray Paint Signatures Ultramarine Blue": "1:11",
        "Pick and Pop Art Signatures Cadmium Orange": "1:22", "Charcoal Signatures Cadmium Orange": "1:22", "Spray Paint Signatures Cadmium Orange": "1:17",
        "Pick and Pop Art Signatures Winsor Green": "1:55", "Charcoal Signatures Winsor Green": "1:55", "Spray Paint Signatures Winsor Green": "1:41",
        "Pick and Pop Art Signatures Pyrrol Scarlet": "1:111", "Charcoal Signatures Pyrrol Scarlet": "1:111", "Spray Paint Signatures Pyrrol Scarlet": "1:83",
        "Pick and Pop Art Signatures Platinum": "1:597", "Charcoal Signatures Platinum": "1:597", "Spray Paint Signatures Platinum": "1:436",
        # Canvas Champions, LC Signatures, LC Dual, LC Triple
        "Canvas Champions Autographs": "1:22", "Legends of the Court Signatures": "1:5",
        "Legends of the Court Dual Signatures": "1:71", "Legends of the Court Triple Signatures": "1:127",
        "Canvas Champions Autographs Ultramarine Blue": "1:29", "Legends of the Court Signatures Ultramarine Blue": "1:11",
        "Canvas Champions Autographs Cadmium Orange": "1:28", "Legends of the Court Signatures Cadmium Orange": "1:15",
        "Canvas Champions Autographs Winsor Green": "1:66", "Legends of the Court Signatures Winsor Green": "1:37",
        "Canvas Champions Autographs Pyrrol Scarlet": "1:134", "Legends of the Court Signatures Pyrrol Scarlet": "1:74",
        "Legends of the Court Dual Signatures Pyrrol Scarlet": "1:167", "Legends of the Court Triple Signatures Pyrrol Scarlet": "1:343",
        "Canvas Champions Autographs Platinum": "1:733", "Legends of the Court Signatures Platinum": "1:384",
        "Legends of the Court Dual Signatures Platinum": "1:949", "Legends of the Court Triple Signatures Platinum": "1:2,303",
        # Relics
        "Motif Rookie Relics": "1:6", "Motif Rookie Dual Relics": "1:6", "Legends of the Court Relics": "1:17",
        "Motif Rookie Relics Quin Gold": "1:9", "Motif Rookie Dual Relics Quin Gold": "1:9",
        "Motif Rookie Relics Ultramarine Blue": "1:11", "Motif Rookie Dual Relics Ultramarine Blue": "1:11", "Legends of the Court Relics Ultramarine Blue": "1:21",
        "Motif Rookie Relics Cadmium Orange": "1:17", "Motif Rookie Dual Relics Cadmium Orange": "1:17", "Legends of the Court Relics Cadmium Orange": "1:32",
        "Motif Rookie Relics Winsor Green": "1:42", "Motif Rookie Dual Relics Winsor Green": "1:42", "Legends of the Court Relics Winsor Green": "1:79",
        "Motif Rookie Relics Pyrrol Scarlet": "1:83", "Motif Rookie Dual Relics Pyrrol Scarlet": "1:83", "Legends of the Court Relics Pyrrol Scarlet": "1:166",
        "Motif Rookie Relics Platinum": "1:411", "Motif Rookie Dual Relics Platinum": "1:411", "Legends of the Court Relics Platinum": "1:934",
    },
    "first_day_issue": {
        "Base": "1:2", "Pastel Pink": "1:2", "Quin Gold": "1:4", "Ultramarine Blue": "1:5",
        "Cadmium Orange": "1:7", "Majesty Purple": "1:11", "Winsor Green": "1:16",
        "Pyrrol Scarlet": "1:32", "Platinum": "1:157", "Printing Plate": "1:38",
        "Motif Rookie Relic Autographs": "1:5", "Motif Rookie Dual Relic Autographs": "1:5",
        "Motif Rookie Triple Relic Autographs": "1:5", "Motif Rookie Quad Relic Autographs": "1:15",
        "Motif Rookie Relic Autographs Quin Gold": "1:8", "Motif Rookie Dual Relic Autographs Quin Gold": "1:8",
        "Motif Rookie Triple Relic Autographs Quin Gold": "1:8", "Motif Rookie Quad Relic Autographs Quin Gold": "1:23",
        "Motif Rookie Relic Autographs Ultramarine Blue": "1:10", "Motif Rookie Dual Relic Autographs Ultramarine Blue": "1:10",
        "Motif Rookie Triple Relic Autographs Ultramarine Blue": "1:10", "Motif Rookie Quad Relic Autographs Ultramarine Blue": "1:28",
        "Motif Rookie Relic Autographs Cadmium Orange": "1:15", "Motif Rookie Dual Relic Autographs Cadmium Orange": "1:15",
        "Motif Rookie Triple Relic Autographs Cadmium Orange": "1:15", "Motif Rookie Quad Relic Autographs Cadmium Orange": "1:44",
        "Motif Rookie Relic Autographs Winsor Green": "1:37", "Motif Rookie Dual Relic Autographs Winsor Green": "1:37",
        "Motif Rookie Triple Relic Autographs Winsor Green": "1:37", "Motif Rookie Quad Relic Autographs Winsor Green": "1:111",
        "Motif Rookie Relic Autographs Pyrrol Scarlet": "1:74", "Motif Rookie Dual Relic Autographs Pyrrol Scarlet": "1:74",
        "Motif Rookie Triple Relic Autographs Pyrrol Scarlet": "1:74", "Motif Rookie Quad Relic Autographs Pyrrol Scarlet": "1:229",
        "Motif Rookie Relic Autographs Platinum": "1:189", "Motif Rookie Dual Relic Autographs Platinum": "1:398",
        "Motif Rookie Triple Relic Autographs Platinum": "1:398", "Motif Rookie Quad Relic Autographs Platinum": "1:1,536",
        "Splatter Signatures": "1:11", "Statistical Showpiece Signatures": "1:53", "Apprentice Numerical Autographs": "1:25",
        "Abstract Ink Signatures": "1:4", "Acrylic Drip Autographs": "1:4", "Still Life Signatures": "1:15",
        "Abstract Ink Signatures Ultramarine Blue": "1:11", "Acrylic Drip Autographs Ultramarine Blue": "1:11", "Still Life Signatures Ultramarine Blue": "1:23",
        "Abstract Ink Signatures Cadmium Orange": "1:11", "Acrylic Drip Autographs Cadmium Orange": "1:11", "Still Life Signatures Cadmium Orange": "1:22",
        "Abstract Ink Signatures Winsor Green": "1:28", "Acrylic Drip Autographs Winsor Green": "1:28", "Still Life Signatures Winsor Green": "1:55",
        "Abstract Ink Signatures Pyrrol Scarlet": "1:55", "Acrylic Drip Autographs Pyrrol Scarlet": "1:55", "Still Life Signatures Pyrrol Scarlet": "1:111",
        "Abstract Ink Signatures Platinum": "1:291", "Acrylic Drip Autographs Platinum": "1:291", "Still Life Signatures Platinum": "1:633",
        "Aquarelle Autographs": "1:4", "Deco-Rated Autographs": "1:4",
        "Aquarelle Autographs Ultramarine Blue": "1:9", "Deco-Rated Autographs Ultramarine Blue": "1:9",
        "Aquarelle Autographs Cadmium Orange": "1:13", "Deco-Rated Autographs Cadmium Orange": "1:9",
        "Aquarelle Autographs Winsor Green": "1:22", "Deco-Rated Autographs Winsor Green": "1:22",
        "Aquarelle Autographs Pyrrol Scarlet": "1:44", "Deco-Rated Autographs Pyrrol Scarlet": "1:44",
        "Aquarelle Autographs Platinum": "1:229", "Deco-Rated Autographs Platinum": "1:229",
        "Pick and Pop Art Signatures": "1:7", "Charcoal Signatures": "1:8", "Spray Paint Signatures": "1:5",
        "Pick and Pop Art Signatures Ultramarine Blue": "1:14", "Charcoal Signatures Ultramarine Blue": "1:17", "Spray Paint Signatures Ultramarine Blue": "1:11",
        "Pick and Pop Art Signatures Cadmium Orange": "1:15", "Charcoal Signatures Cadmium Orange": "1:15", "Spray Paint Signatures Cadmium Orange": "1:11",
        "Pick and Pop Art Signatures Winsor Green": "1:37", "Charcoal Signatures Winsor Green": "1:37", "Spray Paint Signatures Winsor Green": "1:28",
        "Pick and Pop Art Signatures Pyrrol Scarlet": "1:74", "Charcoal Signatures Pyrrol Scarlet": "1:74", "Spray Paint Signatures Pyrrol Scarlet": "1:55",
        "Pick and Pop Art Signatures Platinum": "1:398", "Charcoal Signatures Platinum": "1:398", "Spray Paint Signatures Platinum": "1:291",
        "Canvas Champions Autographs": "1:22", "Legends of the Court Signatures": "1:5",
        "Legends of the Court Dual Signatures": "1:71", "Legends of the Court Triple Signatures": "1:127",
        "Canvas Champions Autographs Ultramarine Blue": "1:29", "Legends of the Court Signatures Ultramarine Blue": "1:11",
        "Canvas Champions Autographs Cadmium Orange": "1:28", "Legends of the Court Signatures Cadmium Orange": "1:15",
        "Canvas Champions Autographs Winsor Green": "1:44", "Legends of the Court Signatures Winsor Green": "1:25",
        "Canvas Champions Autographs Pyrrol Scarlet": "1:89", "Legends of the Court Signatures Pyrrol Scarlet": "1:49",
        "Legends of the Court Dual Signatures Pyrrol Scarlet": "1:111", "Legends of the Court Triple Signatures Pyrrol Scarlet": "1:229",
        "Canvas Champions Autographs Platinum": "1:489", "Legends of the Court Signatures Platinum": "1:256",
        "Legends of the Court Dual Signatures Platinum": "1:633", "Legends of the Court Triple Signatures Platinum": "1:1,536",
        "Motif Rookie Relics": "1:6", "Motif Rookie Dual Relics": "1:6", "Legends of the Court Relics": "1:17",
        "Motif Rookie Relics Quin Gold": "1:9", "Motif Rookie Dual Relics Quin Gold": "1:9",
        "Motif Rookie Relics Ultramarine Blue": "1:11", "Motif Rookie Dual Relics Ultramarine Blue": "1:11", "Legends of the Court Relics Ultramarine Blue": "1:21",
        "Motif Rookie Relics Cadmium Orange": "1:17", "Motif Rookie Dual Relics Cadmium Orange": "1:17", "Legends of the Court Relics Cadmium Orange": "1:32",
        "Motif Rookie Relics Winsor Green": "1:42", "Motif Rookie Dual Relics Winsor Green": "1:42", "Legends of the Court Relics Winsor Green": "1:79",
        "Motif Rookie Relics Pyrrol Scarlet": "1:83", "Motif Rookie Dual Relics Pyrrol Scarlet": "1:83", "Legends of the Court Relics Pyrrol Scarlet": "1:111",
        "Motif Rookie Relics Platinum": "1:411", "Motif Rookie Dual Relics Platinum": "1:411", "Legends of the Court Relics Platinum": "1:623",
    }
}

db.execute("""
    INSERT INTO sets (name, sport, season, tier, slug, is_visible,
                      sample_image_url, release_date, box_config, pack_odds, created_at)
    VALUES ('2025-26 Topps Motif Basketball', 'Basketball', '2025-26', 'Standard',
            '2025-26-topps-motif-basketball', 1,
            '/sets/2025-topps-motif-basketball.jpg', '2026-06-09', ?, ?, '2026-06-04T12:00:00Z')
""", (box_config, json.dumps(pack_odds_data)))
SET_ID = db.execute("SELECT last_insert_rowid()").fetchone()[0]
print(f"Created set ID: {SET_ID}")

def slugify(t):
    s = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode('ascii')
    s = s.lower().strip(); s = re.sub(r'[^\w\s-]', '', s); s = re.sub(r'[\s_]+', '-', s)
    return re.sub(r'-+', '-', s).strip('-')

_sc = {}
def goc(name):
    name = name.strip()
    row = db.execute("SELECT id FROM players WHERE set_id = ? AND name = ?", (SET_ID, name)).fetchone()
    if row: return row[0]
    slug = slugify(name)
    if not _sc:
        for r in db.execute("SELECT slug FROM players WHERE set_id = ? AND slug IS NOT NULL", (SET_ID,)).fetchall():
            _sc[r[0]] = True
    c = slug; i = 2
    while c in _sc: c = f"{slug}-{i}"; i += 1
    _sc[c] = True
    db.execute("INSERT INTO players (set_id, name, slug, unique_cards, total_print_run, one_of_ones, insert_set_count, subject_role) VALUES (?, ?, ?, 0, 0, 0, 0, 'athlete')",
               (SET_ID, name, c))
    return db.execute("SELECT last_insert_rowid()").fetchone()[0]

def ais(name, is_auto=False):
    db.execute("INSERT INTO insert_sets (set_id, name, is_autograph) VALUES (?, ?, ?)", (SET_ID, name, 1 if is_auto else 0))
    return db.execute("SELECT last_insert_rowid()").fetchone()[0]

def ap(is_id, pars):
    for p in pars:
        name, pr = p[0], p[1]
        db.execute("INSERT INTO parallels (insert_set_id, name, print_run, exclusivity) VALUES (?, ?, ?, 'Hobby')", (is_id, name, pr))
    return len(pars)

def ac(is_id, cards):
    for num, name, team, rc in cards:
        pid = goc(name)
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)",
                   (pid, is_id, str(num), 1 if rc else 0, team))

def am(is_id, num, names):
    pids = [goc(n) for n in names]
    db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, NULL)", (pids[0], is_id, str(num)))
    a = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    for p in pids[1:]:
        db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a, p))

F = False

# ═══ BASE SET (100 cards) ═══════════════════════════════════════════════════
base_id = ais("Base Set")
base_pars = [("Pastel Pink",None),("Quin Gold",None),("Ultramarine Blue",None),("Cadmium Orange",None),("Majesty Purple",None),("Winsor Green",None),("Pyrrol Scarlet",None),("Platinum",None),("Printing Plate",1)]
ap(base_id, base_pars)

base = [
(1,"Anthony Edwards","Minnesota Timberwolves",F),(2,"Rudy Gobert","Minnesota Timberwolves",F),(3,"Donte DiVincenzo","Minnesota Timberwolves",F),(4,"Julius Randle","Minnesota Timberwolves",F),(5,"Jayson Tatum","Boston Celtics",F),(6,"Kristaps Porzingis","Atlanta Hawks",F),(7,"Al Horford","Golden State Warriors",F),(8,"Jaylen Brown","Boston Celtics",F),(9,"Jalen Brunson","New York Knicks",F),(10,"Josh Hart","New York Knicks",F),
(11,"OG Anunoby","New York Knicks",F),(12,"Mikal Bridges","New York Knicks",F),(13,"Nikola Jokic","Denver Nuggets",F),(14,"Jamal Murray","Denver Nuggets",F),(15,"Michael Porter Jr.","Brooklyn Nets",F),(16,"Julian Strawther","Denver Nuggets",F),(17,"Joel Embiid","Philadelphia 76ers",F),(18,"Tyrese Maxey","Philadelphia 76ers",F),(19,"Paul George","Philadelphia 76ers",F),(20,"Quentin Grimes","Philadelphia 76ers",F),
(21,"Shai Gilgeous-Alexander","Oklahoma City Thunder",F),(22,"Jalen Williams","Oklahoma City Thunder",F),(23,"Chet Holmgren","Oklahoma City Thunder",F),(24,"Alex Caruso","Oklahoma City Thunder",F),(25,"Tyrese Haliburton","Indiana Pacers",F),(26,"Myles Turner","Milwaukee Bucks",F),(27,"Obi Toppin","Indiana Pacers",F),(28,"Pascal Siakam","Indiana Pacers",F),(29,"Bronny James Jr.","Los Angeles Lakers",F),(30,"LeBron James","Los Angeles Lakers",F),
(31,"Austin Reaves","Los Angeles Lakers",F),(32,"Rui Hachimura","Los Angeles Lakers",F),(33,"Jalen Green","Phoenix Suns",F),(34,"Amen Thompson","Houston Rockets",F),(35,"Alperen Sengun","Houston Rockets",F),(36,"Fred VanVleet","Houston Rockets",F),(37,"Paolo Banchero","Orlando Magic",F),(38,"Jalen Suggs","Orlando Magic",F),(39,"Franz Wagner","Orlando Magic",F),(40,"Anthony Black","Orlando Magic",F),
(41,"Cameron Johnson","Denver Nuggets",F),(42,"Nic Claxton","Brooklyn Nets",F),(43,"Cam Thomas","Brooklyn Nets",F),(44,"Shaedon Sharpe","Portland Trail Blazers",F),(45,"Scoot Henderson","Portland Trail Blazers",F),(46,"DeAndre Ayton","Los Angeles Lakers",F),(47,"Gradey Dick","Toronto Raptors",F),(48,"RJ Barrett","Toronto Raptors",F),(49,"Scottie Barnes","Toronto Raptors",F),(50,"Collin Sexton","Charlotte Hornets",F),
(51,"Lauri Markkanen","Utah Jazz",F),(52,"Walker Kessler","Utah Jazz",F),(53,"Josh Giddey","Chicago Bulls",F),(54,"Nikola Vucevic","Chicago Bulls",F),(55,"Matas Buzelis","Chicago Bulls",F),(56,"Stephen Curry","Golden State Warriors",F),(57,"Draymond Green","Golden State Warriors",F),(58,"Jimmy Butler III","Golden State Warriors",F),(59,"Donovan Mitchell","Cleveland Cavaliers",F),(60,"Darius Garland","Cleveland Cavaliers",F),
(61,"Evan Mobley","Cleveland Cavaliers",F),(62,"Kawhi Leonard","Los Angeles Clippers",F),(63,"James Harden","Los Angeles Clippers",F),(64,"Ivica Zubac","Los Angeles Clippers",F),(65,"Cade Cunningham","Detroit Pistons",F),(66,"Jalen Duren","Detroit Pistons",F),(67,"Ausar Thompson","Detroit Pistons",F),(68,"Kevin Durant","Houston Rockets",F),(69,"Devin Booker","Phoenix Suns",F),(70,"Bradley Beal","Los Angeles Clippers",F),
(71,"Giannis Antetokounmpo","Milwaukee Bucks",F),(72,"Kyle Kuzma","Milwaukee Bucks",F),(73,"Damian Lillard","Portland Trail Blazers",F),(74,"Zach Lavine","Sacramento Kings",F),(75,"Domantas Sabonis","Sacramento Kings",F),(76,"DeMar DeRozan","Sacramento Kings",F),(77,"Trae Young","Atlanta Hawks",F),(78,"Zaccharie Risacher","Atlanta Hawks",F),(79,"Dyson Daniels","Atlanta Hawks",F),(80,"Anthony Davis","Dallas Mavericks",F),
(81,"P.J. Washington Jr.","Dallas Mavericks",F),(82,"Kyrie Irving","Dallas Mavericks",F),(83,"LaMelo Ball","Charlotte Hornets",F),(84,"Miles Bridges","Charlotte Hornets",F),(85,"Mark Williams","Phoenix Suns",F),(86,"Ja Morant","Memphis Grizzlies",F),(87,"Desmond Bane","Orlando Magic",F),(88,"Zach Edey","Memphis Grizzlies",F),(89,"Tyler Herro","Miami Heat",F),(90,"Andrew Wiggins","Miami Heat",F),
(91,"Bam Adebayo","Miami Heat",F),(92,"Alex Sarr","Washington Wizards",F),(93,"Jordan Poole","New Orleans Pelicans",F),(94,"Luka Doncic","Los Angeles Lakers",F),(95,"Dejounte Murray","New Orleans Pelicans",F),(96,"Yves Missi","New Orleans Pelicans",F),(97,"CJ McCollum","Washington Wizards",F),(98,"Victor Wembanyama","San Antonio Spurs",F),(99,"De'Aaron Fox","San Antonio Spurs",F),(100,"Stephon Castle","San Antonio Spurs",F),
]
ac(base_id, base)
print(f"  Base Set: {len(base)} cards, {len(base_pars)} parallels")

# ═══ AUTO/RELIC SUBSET SHELLS (card data pending) ═══════════════════════════
# Common auto parallel ladder
auto_full_pars = [("Ultramarine Blue",None),("Cadmium Orange",None),("Winsor Green",None),("Pyrrol Scarlet",None),("Platinum",None)]
relic_full_pars = [("Quin Gold",None),("Ultramarine Blue",None),("Cadmium Orange",None),("Winsor Green",None),("Pyrrol Scarlet",None),("Platinum",None)]
lc_dual_pars = [("Pyrrol Scarlet",None),("Platinum",None)]

auto_subsets = [
    ("Splatter Signatures", True, []),  # no parallels beyond base for these 3
    ("Statistical Showpiece Signatures", True, []),
    ("Apprentice Numerical Autographs", True, []),
    ("Abstract Ink Signatures", True, auto_full_pars),
    ("Acrylic Drip Autographs", True, auto_full_pars),
    ("Still Life Signatures", True, auto_full_pars),
    ("Aquarelle Autographs", True, auto_full_pars),
    ("Deco-Rated Autographs", True, auto_full_pars),
    ("Pick and Pop Art Signatures", True, auto_full_pars),
    ("Charcoal Signatures", True, auto_full_pars),
    ("Spray Paint Signatures", True, auto_full_pars),
    ("Canvas Champions Autographs", True, auto_full_pars),
    ("Legends of the Court Signatures", True, auto_full_pars),
    ("Legends of the Court Dual Signatures", True, lc_dual_pars),
    ("Legends of the Court Triple Signatures", True, lc_dual_pars),
    ("Motif Rookie Relic Autographs", True, relic_full_pars),
    ("Motif Rookie Dual Relic Autographs", True, relic_full_pars),
    ("Motif Rookie Triple Relic Autographs", True, relic_full_pars),
    ("Motif Rookie Quad Relic Autographs", True, relic_full_pars),
    ("Motif Rookie Relics", False, relic_full_pars),
    ("Motif Rookie Dual Relics", False, relic_full_pars),
    ("Legends of the Court Relics", False, auto_full_pars),
]

for name, is_auto, pars in auto_subsets:
    sid = ais(name, is_auto=is_auto)
    if pars:
        ap(sid, pars)
    print(f"  {name}: shell ({len(pars)} parallels, cards pending)")

# ═══ BACKFILL IMAGE IDs ═════════════════════════════════════════════════════
db.commit()
updated = db.execute("""
    UPDATE players SET nba_player_id = (SELECT p2.nba_player_id FROM players p2 WHERE p2.name = players.name AND p2.nba_player_id IS NOT NULL LIMIT 1)
    WHERE set_id = ? AND nba_player_id IS NULL AND EXISTS (SELECT 1 FROM players p2 WHERE p2.name = players.name AND p2.nba_player_id IS NOT NULL)
""", (SET_ID,)).rowcount
print(f"\nBackfilled {updated} NBA player IDs")

# ═══ SUMMARY ════════════════════════════════════════════════════════════════
db.commit()
tp = db.execute("SELECT COUNT(*) FROM players WHERE set_id = ?", (SET_ID,)).fetchone()[0]
ta = db.execute("SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets ins ON pa.insert_set_id = ins.id WHERE ins.set_id = ?", (SET_ID,)).fetchone()[0]
ts = db.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id = ?", (SET_ID,)).fetchone()[0]
tpar = db.execute("SELECT COUNT(*) FROM parallels p JOIN insert_sets ins ON p.insert_set_id = ins.id WHERE ins.set_id = ?", (SET_ID,)).fetchone()[0]

print(f"\n{'='*50}")
print(f"Set ID: {SET_ID}")
print(f"Total subsets: {ts}")
print(f"Total unique athletes: {tp}")
print(f"Total card appearances: {ta}")
print(f"Total parallels: {tpar}")
print(f"Pack odds: {len(pack_odds_data['hobby'])} Hobby keys + {len(pack_odds_data['first_day_issue'])} FDI keys")
print(f"(22 auto/relic subsets pending card data)")
db.close()
print("Done!")
