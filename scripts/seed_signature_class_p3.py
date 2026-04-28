"""
Seed: 2025-26 Topps Signature Class Basketball — Part 3: All insert sets.
Usage: python3 scripts/seed_signature_class_p3.py
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

def add_cards(is_name, cards):
    is_id = get_is_id(is_name)
    for num, name, team, rookie in cards:
        pid = get_or_create_player(name)
        cur.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)",
                    (pid, is_id, num, int(rookie), team))
    print(f"  {is_name}: {len(cards)} cards")

add_cards("After Image", [
    ("AF-1","Cooper Flagg","Dallas Mavericks",T),("AF-2","Dylan Harper","San Antonio Spurs",T),("AF-3","VJ Edgecombe","Philadelphia 76ers",T),
    ("AF-4","Kon Knueppel","Charlotte Hornets",T),("AF-5","Ace Bailey","Utah Jazz",T),("AF-6","Tre Johnson III","Washington Wizards",T),
    ("AF-7","Jeremiah Fears","New Orleans Pelicans",T),("AF-8","Egor Demin","Brooklyn Nets",T),("AF-9","Collin Murray-Boyles","Toronto Raptors",T),
    ("AF-10","Khaman Maluach","Phoenix Suns",T),("AF-11","Jayson Tatum","Boston Celtics",R),("AF-12","Kyrie Irving","Dallas Mavericks",R),
    ("AF-13","Austin Reaves","Los Angeles Lakers",R),("AF-14","Paolo Banchero","Orlando Magic",R),("AF-15","Kevin Durant","Houston Rockets",R),
    ("AF-16","Kawhi Leonard","Los Angeles Clippers",R),("AF-17","Victor Wembanyama","San Antonio Spurs",R),("AF-18","LaMelo Ball","Charlotte Hornets",R),
    ("AF-19","Devin Booker","Phoenix Suns",R),("AF-20","Tyrese Haliburton","Indiana Pacers",R),("AF-21","Tyler Herro","Miami Heat",R),
    ("AF-22","Cade Cunningham","Detroit Pistons",R),("AF-23","Ja Morant","Memphis Grizzlies",R),("AF-24","Paul George","Philadelphia 76ers",R),
    ("AF-25","Damian Lillard","Milwaukee Bucks",R),
])

add_cards("High Fidelity", [
    ("HF-1","Cooper Flagg","Dallas Mavericks",T),("HF-2","Dylan Harper","San Antonio Spurs",T),("HF-3","VJ Edgecombe","Philadelphia 76ers",T),
    ("HF-4","Kon Knueppel","Charlotte Hornets",T),("HF-5","Ace Bailey","Utah Jazz",T),("HF-6","Tre Johnson III","Washington Wizards",T),
    ("HF-7","Jeremiah Fears","New Orleans Pelicans",T),("HF-8","Egor Demin","Brooklyn Nets",T),("HF-9","Collin Murray-Boyles","Toronto Raptors",T),
    ("HF-10","Khaman Maluach","Phoenix Suns",T),("HF-11","Cedric Coward","Memphis Grizzlies",T),("HF-12","Noa Essengue","Chicago Bulls",T),
    ("HF-13","Derik Queen","New Orleans Pelicans",T),("HF-14","Carter Bryant","San Antonio Spurs",T),("HF-15","Thomas Sorber","Oklahoma City Thunder",T),
    ("HF-16","Yang Hansen","Portland Trail Blazers",T),("HF-17","Joan Beringer","Minnesota Timberwolves",T),("HF-18","Walter Clayton Jr.","Utah Jazz",T),
    ("HF-19","Nolan Traore","Brooklyn Nets",T),("HF-20","Anthony Davis","Dallas Mavericks",R),("HF-21","Nikola Jokic","Denver Nuggets",R),
    ("HF-22","Giannis Antetokounmpo","Milwaukee Bucks",R),("HF-23","Jaylen Brown","Boston Celtics",R),("HF-24","Shai Gilgeous-Alexander","Oklahoma City Thunder",R),
    ("HF-25","Donovan Mitchell","Cleveland Cavaliers",R),("HF-26","Jalen Green","Houston Rockets",R),("HF-27","Stephen Curry","Golden State Warriors",R),
    ("HF-28","Tyrese Maxey","Philadelphia 76ers",R),("HF-29","Cade Cunningham","Detroit Pistons",R),("HF-30","Tyrese Haliburton","Indiana Pacers",R),
])

add_cards("Pure", [
    ("PU-1","LeBron James","Los Angeles Lakers",R),("PU-2","Shai Gilgeous-Alexander","Oklahoma City Thunder",R),
    ("PU-3","Giannis Antetokounmpo","Milwaukee Bucks",R),("PU-4","Tyrese Haliburton","Indiana Pacers",R),
    ("PU-5","Donovan Mitchell","Cleveland Cavaliers",R),("PU-6","Jayson Tatum","Boston Celtics",R),
    ("PU-7","James Harden","Los Angeles Clippers",R),("PU-8","Paolo Banchero","Orlando Magic",R),
    ("PU-9","Stephon Castle","San Antonio Spurs",R),("PU-10","Stephen Curry","Golden State Warriors",R),
    ("PU-11","Magic Johnson","Los Angeles Lakers",R),("PU-12","Jason Kidd","New Jersey Nets",R),
    ("PU-13","John Stockton","Utah Jazz",R),("PU-14","Dwyane Wade","Miami Heat",R),("PU-15","Ray Allen","Seattle Supersonics",R),
    ("PU-16","Cooper Flagg","Dallas Mavericks",T),("PU-17","Dylan Harper","San Antonio Spurs",T),("PU-18","VJ Edgecombe","Philadelphia 76ers",T),
    ("PU-19","Kon Knueppel","Charlotte Hornets",T),("PU-20","Ace Bailey","Utah Jazz",T),("PU-21","Tre Johnson III","Washington Wizards",T),
    ("PU-22","Jeremiah Fears","New Orleans Pelicans",T),("PU-23","Egor Demin","Brooklyn Nets",T),("PU-24","Collin Murray-Boyles","Toronto Raptors",T),
    ("PU-25","Tyrese Proctor","Cleveland Cavaliers",T),
])

add_cards("Unfazed", [
    ("FAZE-1","Anthony Edwards","Minnesota Timberwolves",R),("FAZE-2","Victor Wembanyama","San Antonio Spurs",R),
    ("FAZE-3","Ja Morant","Memphis Grizzlies",R),("FAZE-4","Anthony Davis","Dallas Mavericks",R),
    ("FAZE-5","Pascal Siakam","Indiana Pacers",R),("FAZE-6","Tyler Herro","Miami Heat",R),
    ("FAZE-7","Nikola Jokic","Denver Nuggets",R),("FAZE-8","James Harden","Los Angeles Clippers",R),
    ("FAZE-9","Tyrese Haliburton","Indiana Pacers",R),("FAZE-10","Kevin Durant","Houston Rockets",R),
    ("FAZE-11","Cooper Flagg","Dallas Mavericks",T),("FAZE-12","Dylan Harper","San Antonio Spurs",T),
    ("FAZE-13","VJ Edgecombe","Philadelphia 76ers",T),("FAZE-14","Kon Knueppel","Charlotte Hornets",T),
    ("FAZE-15","Ace Bailey","Utah Jazz",T),("FAZE-16","Tre Johnson III","Washington Wizards",T),
    ("FAZE-17","Jeremiah Fears","New Orleans Pelicans",T),("FAZE-18","Egor Demin","Brooklyn Nets",T),
    ("FAZE-19","Collin Murray-Boyles","Toronto Raptors",T),("FAZE-20","Tyrese Proctor","Cleveland Cavaliers",T),
])

add_cards("Star Cast", [
    ("SC-1","Stephen Curry","Golden State Warriors",R),("SC-2","Trae Young","Atlanta Hawks",R),("SC-3","Cade Cunningham","Detroit Pistons",R),
    ("SC-4","Jalen Brunson","New York Knicks",R),("SC-5","Paolo Banchero","Orlando Magic",R),("SC-6","Jaylen Brown","Boston Celtics",R),
    ("SC-7","Austin Reaves","Los Angeles Lakers",R),("SC-8","Joel Embiid","Philadelphia 76ers",R),("SC-9","De'Aaron Fox","San Antonio Spurs",R),
    ("SC-10","Devin Booker","Phoenix Suns",R),("SC-11","Jimmy Butler III","Golden State Warriors",R),("SC-12","Jamal Murray","Denver Nuggets",R),
    ("SC-13","Jalen Green","Houston Rockets",R),("SC-14","Kyrie Irving","Dallas Mavericks",R),("SC-15","Jalen Williams","Oklahoma City Thunder",R),
    ("SC-16","Larry Bird","Boston Celtics",R),("SC-17","Shaquille O'Neal","Los Angeles Lakers",R),("SC-18","Vince Carter","Toronto Raptors",R),
    ("SC-19","Manu Ginobili","San Antonio Spurs",R),("SC-20","Dirk Nowitzki","Dallas Mavericks",R),
    ("SC-21","Cooper Flagg","Dallas Mavericks",T),("SC-22","Dylan Harper","San Antonio Spurs",T),("SC-23","Jeremiah Fears","New Orleans Pelicans",T),
    ("SC-24","Kon Knueppel","Charlotte Hornets",T),("SC-25","Tre Johnson III","Washington Wizards",T),
])

add_cards("Algorithm", [
    ("AL-1","Jason Kidd","New Jersey Nets",R),("AL-2","John Stockton","Utah Jazz",R),("AL-3","Paul Pierce","Boston Celtics",R),
    ("AL-4","Steve Nash","Phoenix Suns",R),("AL-5","Rajon Rondo","Boston Celtics",R),("AL-6","Gary Payton","Seattle Supersonics",R),
    ("AL-7","Allen Iverson","Philadelphia 76ers",R),("AL-8","Anfernee Hardaway","Orlando Magic",R),("AL-9","Manu Ginobili","San Antonio Spurs",R),
    ("AL-10","Jamal Crawford","Los Angeles Clippers",R),("AL-11","Chris Paul","San Antonio Spurs",R),("AL-12","LeBron James","Los Angeles Lakers",R),
    ("AL-13","Russell Westbrook","Denver Nuggets",R),("AL-14","Nikola Jokic","Denver Nuggets",R),("AL-15","Kawhi Leonard","Los Angeles Clippers",R),
    ("AL-16","James Harden","Los Angeles Clippers",R),("AL-17","De'Aaron Fox","San Antonio Spurs",R),("AL-18","Shai Gilgeous-Alexander","Oklahoma City Thunder",R),
    ("AL-19","Kyrie Irving","Dallas Mavericks",R),("AL-20","Jalen Brunson","New York Knicks",R),
    ("AL-21","Cooper Flagg","Dallas Mavericks",T),("AL-22","Dylan Harper","San Antonio Spurs",T),("AL-23","Kon Knueppel","Charlotte Hornets",T),
    ("AL-24","Ace Bailey","Utah Jazz",T),("AL-25","Tyrese Proctor","Cleveland Cavaliers",T),
])

add_cards("Roses", [
    ("R-1","Derrick Rose","Chicago Bulls",R),("R-2","Shaquille O'Neal","Los Angeles Lakers",R),("R-3","Magic Johnson","Los Angeles Lakers",R),
    ("R-4","Dennis Rodman","Chicago Bulls",R),("R-5","Tracy McGrady","Houston Rockets",R),("R-6","LaMelo Ball","Charlotte Hornets",R),
    ("R-7","Tyler Herro","Miami Heat",R),("R-8","Kyrie Irving","Dallas Mavericks",R),("R-9","Giannis Antetokounmpo","Milwaukee Bucks",R),
    ("R-10","Paul George","Philadelphia 76ers",R),("R-11","Paolo Banchero","Orlando Magic",R),("R-12","James Harden","Los Angeles Clippers",R),
    ("R-13","Ja Morant","Memphis Grizzlies",R),("R-14","Zaccharie Risacher","Atlanta Hawks",R),("R-15","Scoot Henderson","Portland Trail Blazers",R),
    ("R-16","Cooper Flagg","Dallas Mavericks",T),("R-17","Dylan Harper","San Antonio Spurs",T),("R-18","Kon Knueppel","Charlotte Hornets",T),
    ("R-19","Ace Bailey","Utah Jazz",T),("R-20","Egor Demin","Brooklyn Nets",T),("R-21","Collin Murray-Boyles","Toronto Raptors",T),
    ("R-22","Khaman Maluach","Phoenix Suns",T),("R-23","Tyrese Proctor","Cleveland Cavaliers",T),("R-24","Noa Essengue","Chicago Bulls",T),
    ("R-25","Derik Queen","New Orleans Pelicans",T),
])

add_cards("Aristocrats", [
    ("AR-1","Stephen Curry","Golden State Warriors",R),("AR-2","Ja Morant","Memphis Grizzlies",R),("AR-3","Paolo Banchero","Orlando Magic",R),
    ("AR-4","Kyrie Irving","Dallas Mavericks",R),("AR-5","Jayson Tatum","Boston Celtics",R),("AR-6","Jalen Green","Houston Rockets",R),
    ("AR-7","Donovan Mitchell","Cleveland Cavaliers",R),("AR-8","Austin Reaves","Los Angeles Lakers",R),("AR-9","Damian Lillard","Milwaukee Bucks",R),
    ("AR-10","Vince Carter","Toronto Raptors",R),("AR-11","Jalen Brunson","New York Knicks",R),("AR-12","Dwyane Wade","Miami Heat",R),
    ("AR-13","Allen Iverson","Philadelphia 76ers",R),("AR-14","Cade Cunningham","Detroit Pistons",R),("AR-15","Tyrese Haliburton","Indiana Pacers",R),
    ("AR-21","Cooper Flagg","Dallas Mavericks",T),("AR-22","Dylan Harper","San Antonio Spurs",T),("AR-23","VJ Edgecombe","Philadelphia 76ers",T),
    ("AR-24","Kon Knueppel","Charlotte Hornets",T),("AR-25","Ace Bailey","Utah Jazz",T),
])

add_cards("Monarchs of the Game", [
    ("MOTG-1","LeBron James","Los Angeles Lakers",R),("MOTG-2","Anthony Edwards","Minnesota Timberwolves",R),
    ("MOTG-3","Stephen Curry","Golden State Warriors",R),("MOTG-4","Giannis Antetokounmpo","Milwaukee Bucks",R),
    ("MOTG-5","Shai Gilgeous-Alexander","Oklahoma City Thunder",R),("MOTG-6","Kyrie Irving","Dallas Mavericks",R),
    ("MOTG-7","Jayson Tatum","Boston Celtics",R),("MOTG-8","Victor Wembanyama","San Antonio Spurs",R),
    ("MOTG-9","Nikola Jokic","Denver Nuggets",R),("MOTG-10","Kevin Durant","Houston Rockets",R),
    ("MOTG-11","Hakeem Olajuwon","Houston Rockets",R),("MOTG-12","Tim Duncan","San Antonio Spurs",R),
    ("MOTG-13","Dirk Nowitzki","Dallas Mavericks",R),("MOTG-14","Allen Iverson","Philadelphia 76ers",R),
    ("MOTG-15","Tracy McGrady","Houston Rockets",R),
    ("MOTG-16","Cooper Flagg","Dallas Mavericks",T),("MOTG-17","Dylan Harper","San Antonio Spurs",T),
    ("MOTG-18","Kon Knueppel","Charlotte Hornets",T),("MOTG-19","Ace Bailey","Utah Jazz",T),("MOTG-20","Egor Demin","Brooklyn Nets",T),
    ("MOTG-21","Collin Murray-Boyles","Toronto Raptors",T),("MOTG-22","Khaman Maluach","Phoenix Suns",T),
    ("MOTG-23","Cedric Coward","Memphis Grizzlies",T),("MOTG-24","Noa Essengue","Chicago Bulls",T),("MOTG-25","Derik Queen","New Orleans Pelicans",T),
    ("MOTG-26","Thomas Sorber","Oklahoma City Thunder",T),("MOTG-27","Yang Hansen","Portland Trail Blazers",T),
    ("MOTG-28","Joan Beringer","Minnesota Timberwolves",T),("MOTG-29","Walter Clayton Jr.","Utah Jazz",T),("MOTG-30","Nolan Traore","Brooklyn Nets",T),
])

add_cards("Fluidity", [
    ("FD-1","LeBron James","Los Angeles Lakers",R),("FD-2","Nikola Jokic","Denver Nuggets",R),
    ("FD-3","Shai Gilgeous-Alexander","Oklahoma City Thunder",R),("FD-4","Anthony Edwards","Minnesota Timberwolves",R),
    ("FD-5","Paolo Banchero","Orlando Magic",R),("FD-6","Tyrese Haliburton","Indiana Pacers",R),
    ("FD-7","Kevin Durant","Houston Rockets",R),("FD-8","Kyrie Irving","Dallas Mavericks",R),
    ("FD-9","Kawhi Leonard","Los Angeles Clippers",R),("FD-10","LaMelo Ball","Charlotte Hornets",R),
    ("FD-11","Jalen Brunson","New York Knicks",R),("FD-12","Victor Wembanyama","San Antonio Spurs",R),
    ("FD-13","Magic Johnson","Los Angeles Lakers",R),("FD-14","John Stockton","Utah Jazz",R),("FD-15","Vince Carter","Toronto Raptors",R),
    ("FD-16","Tim Duncan","San Antonio Spurs",R),("FD-17","Dwyane Wade","Miami Heat",R),
    ("FD-18","Cooper Flagg","Dallas Mavericks",T),("FD-19","Dylan Harper","San Antonio Spurs",T),("FD-20","VJ Edgecombe","Philadelphia 76ers",T),
])

add_cards("Leviathans", [
    ("LEV-1","LeBron James","Los Angeles Lakers",R),("LEV-2","Jayson Tatum","Boston Celtics",R),
    ("LEV-3","Stephen Curry","Golden State Warriors",R),("LEV-4","Jalen Brunson","New York Knicks",R),
    ("LEV-5","Giannis Antetokounmpo","Milwaukee Bucks",R),("LEV-6","Anthony Edwards","Minnesota Timberwolves",R),
    ("LEV-7","Trae Young","Atlanta Hawks",R),("LEV-8","Kawhi Leonard","Los Angeles Clippers",R),
    ("LEV-9","Bam Adebayo","Miami Heat",R),("LEV-10","Tyrese Haliburton","Indiana Pacers",R),
    ("LEV-11","Cooper Flagg","Dallas Mavericks",T),("LEV-12","Dylan Harper","San Antonio Spurs",T),
    ("LEV-13","Kon Knueppel","Charlotte Hornets",T),("LEV-14","Ace Bailey","Utah Jazz",T),("LEV-15","Egor Demin","Brooklyn Nets",T),
    ("LEV-16","Collin Murray-Boyles","Toronto Raptors",T),("LEV-17","Khaman Maluach","Phoenix Suns",T),
    ("LEV-18","Cedric Coward","Memphis Grizzlies",T),("LEV-19","Noa Essengue","Chicago Bulls",T),("LEV-20","Walter Clayton Jr.","Utah Jazz",T),
])

add_cards("Odyssey", [
    ("ODY-1","Cooper Flagg","Dallas Mavericks",T),("ODY-2","Dylan Harper","San Antonio Spurs",T),("ODY-3","Kon Knueppel","Charlotte Hornets",T),
    ("ODY-4","Ace Bailey","Utah Jazz",T),("ODY-5","Egor Demin","Brooklyn Nets",T),("ODY-6","Collin Murray-Boyles","Toronto Raptors",T),
    ("ODY-7","Khaman Maluach","Phoenix Suns",T),("ODY-8","Cedric Coward","Memphis Grizzlies",T),("ODY-9","Noa Essengue","Chicago Bulls",T),
    ("ODY-10","Derik Queen","New Orleans Pelicans",T),("ODY-11","Thomas Sorber","Oklahoma City Thunder",T),
    ("ODY-12","Yang Hansen","Portland Trail Blazers",T),("ODY-13","Joan Beringer","Minnesota Timberwolves",T),
    ("ODY-14","Walter Clayton Jr.","Utah Jazz",T),("ODY-15","Nolan Traore","Brooklyn Nets",T),("ODY-16","Kasparas Jakucionis","Miami Heat",T),
    ("ODY-17","Will Riley","Washington Wizards",T),("ODY-18","Drake Powell","Brooklyn Nets",T),("ODY-19","Asa Newell","Atlanta Hawks",T),
    ("ODY-20","Tyrese Proctor","Cleveland Cavaliers",T),
])

add_cards("Pressure Points", [
    ("PP-1","Cooper Flagg","Dallas Mavericks",T),("PP-2","Stephen Curry","Golden State Warriors",R),
    ("PP-3","Nikola Jokic","Denver Nuggets",R),("PP-4","Giannis Antetokounmpo","Milwaukee Bucks",R),
    ("PP-5","LeBron James","Los Angeles Lakers",R),("PP-6","Jayson Tatum","Boston Celtics",R),
    ("PP-7","James Harden","Los Angeles Clippers",R),("PP-8","Cade Cunningham","Detroit Pistons",R),
    ("PP-9","Ja Morant","Memphis Grizzlies",R),("PP-10","Trae Young","Atlanta Hawks",R),
])

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
