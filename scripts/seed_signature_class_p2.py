"""
Seed: 2025-26 Topps Signature Class Basketball — Part 2
Base I, Base II, Base I Chrome Variation, Base II Chrome Variation.
Usage: python3 scripts/seed_signature_class_p2.py
"""
import sqlite3, os, re

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA foreign_keys=ON")
cur = conn.cursor()

SET_ID = 838
T = True; R = False

def get_or_create_player(name):
    cur.execute("SELECT id FROM players WHERE set_id = ? AND name = ?", (SET_ID, name))
    row = cur.fetchone()
    if row: return row[0]
    cur.execute("INSERT INTO players (set_id, name, unique_cards, total_print_run, one_of_ones, insert_set_count) VALUES (?, ?, 0, 0, 0, 0)", (SET_ID, name))
    return cur.lastrowid

def get_is_id(name):
    return cur.execute("SELECT id FROM insert_sets WHERE set_id = ? AND name = ?", (SET_ID, name)).fetchone()[0]

def add_cards(is_id, cards):
    for num, name, team, rookie in cards:
        pid = get_or_create_player(name)
        cur.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)",
                    (pid, is_id, str(num), int(rookie), team))

# ─── BASE I (1-100, #68 missing) ─────────────────────────────────
base1_id = get_is_id("Base I")
base1 = [
    (1,"Bronny James Jr.","Los Angeles Lakers",R),(2,"Chris Paul","San Antonio Spurs",R),(3,"Brandon Miller","Charlotte Hornets",R),
    (4,"Jarace Walker","Indiana Pacers",R),(5,"Isaiah Collier","Utah Jazz",R),(6,"Gradey Dick","Toronto Raptors",R),
    (7,"Pelle Larsson","Miami Heat",R),(8,"Bradley Beal","Phoenix Suns",R),(9,"Rui Hachimura","Los Angeles Lakers",R),
    (10,"Coby White","Chicago Bulls",R),(11,"Dillon Jones","Oklahoma City Thunder",R),(12,"Khris Middleton","Washington Wizards",R),
    (13,"CJ McCollum","New Orleans Pelicans",R),(14,"Ty Jerome","Cleveland Cavaliers",R),(15,"Kevin Love","Miami Heat",R),
    (16,"D'Angelo Russell","Brooklyn Nets",R),(17,"Cody Williams","Utah Jazz",R),(18,"Tyrese Maxey","Philadelphia 76ers",R),
    (19,"Andrew Wiggins","Miami Heat",R),(20,"Jrue Holiday","Boston Celtics",R),(21,"Ron Holland II","Detroit Pistons",R),
    (22,"Deandre Ayton","Portland Trail Blazers",R),(23,"Zach Edey","Memphis Grizzlies",R),(24,"Lauri Markkanen","Utah Jazz",R),
    (25,"Shaedon Sharpe","Portland Trail Blazers",R),(26,"Dyson Daniels","Atlanta Hawks",R),(27,"Marcus Smart","Washington Wizards",R),
    (28,"Mike Conley","Minnesota Timberwolves",R),(29,"Cameron Johnson","Brooklyn Nets",R),(30,"Kel'el Ware","Miami Heat",R),
    (31,"Cason Wallace","Oklahoma City Thunder",R),(32,"Cole Anthony","Orlando Magic",R),(33,"Obi Toppin","Indiana Pacers",R),
    (34,"Devin Vassell","San Antonio Spurs",R),(35,"Al Horford","Boston Celtics",R),(36,"Brandon Ingram","Toronto Raptors",R),
    (37,"Jaime Jaquez Jr.","Miami Heat",R),(38,"Herbert Jones","New Orleans Pelicans",R),(39,"Grant Williams","Charlotte Hornets",R),
    (40,"Walker Kessler","Utah Jazz",R),(41,"Isaiah Hartenstein","Oklahoma City Thunder",R),(42,"Payton Pritchard","Boston Celtics",R),
    (43,"Tristan da Silva","Orlando Magic",R),(44,"Yves Missi","New Orleans Pelicans",R),(45,"Josh Giddey","Chicago Bulls",R),
    (46,"Naz Reid","Minnesota Timberwolves",R),(47,"Nikola Topic","Oklahoma City Thunder",R),(48,"Clint Capela","Atlanta Hawks",R),
    (49,"Terance Mann","Atlanta Hawks",R),(50,"Anthony Black","Orlando Magic",R),
    (51,"LeBron James","Los Angeles Lakers",R),(52,"Stephen Curry","Golden State Warriors",R),(53,"Stephon Castle","San Antonio Spurs",R),
    (54,"Shai Gilgeous-Alexander","Oklahoma City Thunder",R),(55,"Victor Wembanyama","San Antonio Spurs",R),
    (56,"Giannis Antetokounmpo","Milwaukee Bucks",R),(57,"Kevin Durant","Houston Rockets",R),(58,"Jalen Brunson","New York Knicks",R),
    (59,"Jayson Tatum","Boston Celtics",R),(60,"Rob Dillingham","Minnesota Timberwolves",R),(61,"Zaccharie Risacher","Atlanta Hawks",R),
    (62,"James Harden","Los Angeles Clippers",R),(63,"Karl-Anthony Towns","New York Knicks",R),(64,"Paolo Banchero","Orlando Magic",R),
    (65,"Jamal Murray","Denver Nuggets",R),(66,"Alex Sarr","Washington Wizards",R),(67,"Jalen Green","Houston Rockets",R),
    (69,"Cam Whitmore","Houston Rockets",R),(70,"Anfernee Simons","Portland Trail Blazers",R),
    (71,"Tyrese Haliburton","Indiana Pacers",R),(72,"Kris Dunn","Los Angeles Clippers",R),(73,"Donovan Mitchell","Cleveland Cavaliers",R),
    (74,"Dorian Finney-Smith","Los Angeles Lakers",R),(75,"Scoot Henderson","Portland Trail Blazers",R),
    (76,"Chet Holmgren","Oklahoma City Thunder",R),(77,"Aaron Gordon","Denver Nuggets",R),(78,"Jaren Jackson Jr.","Memphis Grizzlies",R),
    (79,"Tidjane Salaun","Charlotte Hornets",R),(80,"Desmond Bane","Memphis Grizzlies",R),(81,"Michael Porter Jr.","Denver Nuggets",R),
    (82,"Grayson Allen","Phoenix Suns",R),(83,"Luka Doncic","Los Angeles Lakers",R),(84,"Mikal Bridges","New York Knicks",R),
    (85,"Collin Sexton","Utah Jazz",R),(86,"Dereck Lively II","Dallas Mavericks",R),(87,"Jalen Williams","Oklahoma City Thunder",R),
    (88,"Kristaps Porzingis","Boston Celtics",R),(89,"Zach LaVine","Sacramento Kings",R),(90,"Franz Wagner","Orlando Magic",R),
    (91,"Donte DiVincenzo","Minnesota Timberwolves",R),(92,"Myles Turner","Indiana Pacers",R),(93,"Alperen Sengun","Houston Rockets",R),
    (94,"Bogdan Bogdanovic","Los Angeles Clippers",R),(95,"Nikola Jokic","Denver Nuggets",R),(96,"Rudy Gobert","Minnesota Timberwolves",R),
    (97,"Alex Caruso","Oklahoma City Thunder",R),(98,"Derrick White","Boston Celtics",R),(99,"Jarrett Allen","Cleveland Cavaliers",R),
    (100,"Jordan Clarkson","Utah Jazz",R),
]
add_cards(base1_id, base1)
print(f"  Base I: {len(base1)} cards")

# ─── BASE II (101-149, rookies) ───────────────────────────────────
base2_id = get_is_id("Base II")
base2 = [
    (101,"Cooper Flagg","Dallas Mavericks",T),(102,"Dylan Harper","San Antonio Spurs",T),(103,"Kon Knueppel","Charlotte Hornets",T),
    (104,"Ace Bailey","Utah Jazz",T),(105,"Egor Demin","Brooklyn Nets",T),(106,"Collin Murray-Boyles","Toronto Raptors",T),
    (107,"Khaman Maluach","Phoenix Suns",T),(108,"Cedric Coward","Memphis Grizzlies",T),(109,"Noa Essengue","Chicago Bulls",T),
    (110,"Derik Queen","New Orleans Pelicans",T),(111,"Thomas Sorber","Oklahoma City Thunder",T),(112,"Yang Hansen","Portland Trail Blazers",T),
    (113,"Joan Beringer","Minnesota Timberwolves",T),(114,"Walter Clayton Jr.","Utah Jazz",T),(115,"Nolan Traore","Brooklyn Nets",T),
    (116,"Kasparas Jakucionis","Miami Heat",T),(117,"Will Riley","Washington Wizards",T),(118,"Drake Powell","Brooklyn Nets",T),
    (119,"Asa Newell","Atlanta Hawks",T),(120,"Nique Clifford","Sacramento Kings",T),(121,"Jase Richardson","Orlando Magic",T),
    (122,"Ben Saraf","Brooklyn Nets",T),(123,"Danny Wolf","Brooklyn Nets",T),(124,"Rasheer Fleming","Phoenix Suns",T),
    (125,"Noah Penda","Orlando Magic",T),(126,"Sion James","Charlotte Hornets",T),(127,"Ryan Kalkbrenner","Charlotte Hornets",T),
    (128,"Johni Broome","Philadelphia 76ers",T),(129,"Adou Thiero","Los Angeles Lakers",T),(130,"Chaz Lanier","Detroit Pistons",T),
    (131,"Kam Jones","Indiana Pacers",T),(132,"Alijah Martin","Toronto Raptors",T),(133,"Micah Peavy","New Orleans Pelicans",T),
    (134,"Koby Brea","Phoenix Suns",T),(135,"Maxime Raynaud","Sacramento Kings",T),(136,"Jamir Watkins","Washington Wizards",T),
    (137,"Brooks Barnhizer","Oklahoma City Thunder",T),(138,"Jahmai Mashack","Memphis Grizzlies",T),
    (139,"Liam McNeeley","Charlotte Hornets",T),(140,"Javon Small","Memphis Grizzlies",T),(141,"Tyrese Proctor","Cleveland Cavaliers",T),
    (142,"Yanic Konan-Niederhauser","Los Angeles Clippers",T),(143,"Alex Toohey","Golden State Warriors",T),
    (144,"John Tonje","Utah Jazz",T),(145,"Lachlan Olbrich","Chicago Bulls",T),(146,"Will Richard","Golden State Warriors",T),
    (147,"VJ Edgecombe","Philadelphia 76ers",T),(148,"Hugo Gonzalez","Boston Celtics",T),(149,"Tre Johnson III","Washington Wizards",T),
]
add_cards(base2_id, base2)
print(f"  Base II: {len(base2)} cards")

# ─── BASE I CHROME VARIATION (copy Base I + add #68) ──────────────
base1c_id = get_is_id("Base I Chrome Variation")
rows = cur.execute("SELECT player_id, card_number, is_rookie, team FROM player_appearances WHERE insert_set_id = ?", (base1_id,)).fetchall()
for pid, cn, ir, team in rows:
    cur.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)",
                (pid, base1c_id, cn, ir, team))
# Add #68 Nick Smith Jr. (Chrome Variation only)
nick_id = get_or_create_player("Nick Smith Jr.")
cur.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, '68', 0, 'Charlotte Hornets')",
            (nick_id, base1c_id))
print(f"  Base I Chrome Variation: {len(rows) + 1} cards")

# ─── BASE II CHROME VARIATION (101-150, different checklist) ──────
base2c_id = get_is_id("Base II Chrome Variation")
base2c = [
    (101,"Cooper Flagg","Dallas Mavericks",T),(102,"Dylan Harper","San Antonio Spurs",T),(103,"Kon Knueppel","Charlotte Hornets",T),
    (104,"Ace Bailey","Utah Jazz",T),(105,"Egor Demin","Brooklyn Nets",T),(106,"Collin Murray-Boyles","Toronto Raptors",T),
    (107,"Khaman Maluach","Phoenix Suns",T),(108,"Cedric Coward","Memphis Grizzlies",T),(109,"Noa Essengue","Chicago Bulls",T),
    (110,"Derik Queen","New Orleans Pelicans",T),(111,"Thomas Sorber","Oklahoma City Thunder",T),(112,"Yang Hansen","Portland Trail Blazers",T),
    (113,"Joan Beringer","Minnesota Timberwolves",T),(114,"Walter Clayton Jr.","Utah Jazz",T),(115,"Nolan Traore","Brooklyn Nets",T),
    (116,"Kasparas Jakucionis","Miami Heat",T),(117,"Will Riley","Washington Wizards",T),(118,"Drake Powell","Brooklyn Nets",T),
    (119,"Asa Newell","Atlanta Hawks",T),(120,"Nique Clifford","Sacramento Kings",T),(121,"Jase Richardson","Orlando Magic",T),
    (122,"Ben Saraf","Brooklyn Nets",T),(123,"Danny Wolf","Brooklyn Nets",T),(124,"Rasheer Fleming","Phoenix Suns",T),
    (125,"Noah Penda","Orlando Magic",T),(126,"Sion James","Charlotte Hornets",T),(127,"Ryan Kalkbrenner","Charlotte Hornets",T),
    (128,"Johni Broome","Philadelphia 76ers",T),(129,"Adou Thiero","Los Angeles Lakers",T),(130,"VJ Edgecombe","Philadelphia 76ers",T),
    (131,"Chaz Lanier","Detroit Pistons",T),(132,"Kam Jones","Indiana Pacers",T),(133,"Alijah Martin","Toronto Raptors",T),
    (134,"Micah Peavy","New Orleans Pelicans",T),(135,"Koby Brea","Phoenix Suns",T),(136,"Maxime Raynaud","Sacramento Kings",T),
    (137,"Jamir Watkins","Washington Wizards",T),(138,"Brooks Barnhizer","Oklahoma City Thunder",T),
    (139,"Jahmai Mashack","Memphis Grizzlies",T),(140,"Tre Johnson III","Washington Wizards",T),
    (141,"Liam McNeeley","Charlotte Hornets",T),(142,"Javon Small","Memphis Grizzlies",T),(143,"Tyrese Proctor","Cleveland Cavaliers",T),
    (144,"Hugo Gonzalez","Boston Celtics",T),(145,"Yanic Konan-Niederhauser","Los Angeles Clippers",T),
    (146,"Alex Toohey","Golden State Warriors",T),(147,"John Tonje","Utah Jazz",T),(148,"Carter Bryant","San Antonio Spurs",T),
    (149,"Lachlan Olbrich","Chicago Bulls",T),(150,"Will Richard","Golden State Warriors",T),
]
add_cards(base2c_id, base2c)
print(f"  Base II Chrome Variation: {len(base2c)} cards")

# ─── Generate slugs ──────────────────────────────────────────────
def slugify(text):
    s = text.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_]+', '-', s)
    return re.sub(r'-+', '-', s).strip('-')

cur.execute("SELECT id, name FROM players WHERE set_id = ? AND slug IS NULL", (SET_ID,))
new_players = cur.fetchall()
existing_slugs = set(r[0] for r in cur.execute("SELECT slug FROM players WHERE set_id = ? AND slug IS NOT NULL", (SET_ID,)).fetchall())
for pid, pname in new_players:
    slug = slugify(pname)
    if slug in existing_slugs:
        i = 2
        while f"{slug}-{i}" in existing_slugs: i += 1
        slug = f"{slug}-{i}"
    existing_slugs.add(slug)
    cur.execute("UPDATE players SET slug = ? WHERE id = ?", (slug, pid))

conn.commit()
player_count = cur.execute("SELECT COUNT(*) FROM players WHERE set_id = ?", (SET_ID,)).fetchone()[0]
app_count = cur.execute("SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON pa.insert_set_id = i.id WHERE i.set_id = ?", (SET_ID,)).fetchone()[0]
print(f"\nDone! Set ID: {SET_ID}")
print(f"  Players: {player_count}")
print(f"  Appearances: {app_count}")
conn.close()
