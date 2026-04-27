"""
Seed: 2026 Topps Chrome Black Baseball — Part 3: Insert sets.
Usage: python3 scripts/seed_2026_chrome_black_p3.py
"""
import sqlite3, os, re

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA foreign_keys=ON")
cur = conn.cursor()

SET_ID = 837
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

# ─── DAMASCUS ─────────────────────────────────────────────────────
add_cards("Damascus", [
    ("DAM-1","Shohei Ohtani","Los Angeles Dodgers",R),("DAM-2","Aaron Judge","New York Yankees",R),
    ("DAM-3","Ronald Acuna Jr.","Atlanta Braves",R),("DAM-4","Bobby Witt Jr.","Kansas City Royals",R),
    ("DAM-5","Juan Soto","New York Mets",R),("DAM-6","Cal Raleigh","Seattle Mariners",R),
    ("DAM-7","Pete Crow-Armstrong","Chicago Cubs",R),("DAM-8","Paul Skenes","Pittsburgh Pirates",R),
    ("DAM-9","Nick Kurtz","Athletics",R),("DAM-10","Kyle Schwarber","Philadelphia Phillies",R),
    ("DAM-11","Fernando Tatis Jr.","San Diego Padres",R),("DAM-12","Francisco Lindor","New York Mets",R),
    ("DAM-13","Elly De La Cruz","Cincinnati Reds",R),("DAM-14","Bryce Harper","Philadelphia Phillies",R),
    ("DAM-15","Vladimir Guerrero Jr.","Toronto Blue Jays",R),("DAM-16","Tarik Skubal","Detroit Tigers",R),
    ("DAM-17","Jac Caglianone","Kansas City Royals",T),("DAM-18","Roman Anthony","Boston Red Sox",T),
    ("DAM-19","Colson Montgomery","Chicago White Sox",T),("DAM-20","Kyle Teel","Chicago White Sox",T),
    ("DAM-21","Jacob Misiorowski","Milwaukee Brewers",T),("DAM-22","Christian Moore","Los Angeles Angels",T),
    ("DAM-23","Chase Burns","Cincinnati Reds",T),("DAM-24","Owen Caissie","Chicago Cubs",T),
    ("DAM-25","Samuel Basallo","Baltimore Orioles",T),("DAM-26","Bubba Chandler","Pittsburgh Pirates",T),
    ("DAM-27","Sal Stewart","Cincinnati Reds",T),("DAM-28","Harry Ford","Seattle Mariners",T),
    ("DAM-30","Payton Tolle","Boston Red Sox",T),("DAM-31","Carson Williams","Tampa Bay Rays",T),
])

# ─── NOCTURNAL ────────────────────────────────────────────────────
add_cards("Nocturnal", [
    ("NOC-1","Jac Caglianone","Kansas City Royals",T),("NOC-2","Roman Anthony","Boston Red Sox",T),
    ("NOC-3","Colson Montgomery","Chicago White Sox",T),("NOC-4","Kyle Teel","Chicago White Sox",T),
    ("NOC-5","Jacob Misiorowski","Milwaukee Brewers",T),("NOC-6","Christian Moore","Los Angeles Angels",T),
    ("NOC-7","Chase Burns","Cincinnati Reds",T),("NOC-8","Owen Caissie","Chicago Cubs",T),
    ("NOC-9","Samuel Basallo","Baltimore Orioles",T),("NOC-10","Bubba Chandler","Pittsburgh Pirates",T),
    ("NOC-11","Sal Stewart","Cincinnati Reds",T),("NOC-12","Harry Ford","Seattle Mariners",T),
    ("NOC-13","Alex Freeland","Los Angeles Dodgers",T),("NOC-14","Payton Tolle","Boston Red Sox",T),
    ("NOC-15","Carson Williams","Tampa Bay Rays",T),("NOC-16","Manny Machado","San Diego Padres",R),
    ("NOC-17","Mookie Betts","Los Angeles Dodgers",R),("NOC-18","Freddie Freeman","Los Angeles Dodgers",R),
    ("NOC-19","Shohei Ohtani","Los Angeles Dodgers",R),("NOC-20","Aaron Judge","New York Yankees",R),
    ("NOC-21","Yoshinobu Yamamoto","Los Angeles Dodgers",R),("NOC-22","Nolan Arenado","St. Louis Cardinals",R),
    ("NOC-23","Bo Bichette","Toronto Blue Jays",R),("NOC-24","Junior Caminero","Tampa Bay Rays",R),
    ("NOC-25","Bryce Harper","Philadelphia Phillies",R),("NOC-26","Juan Soto","New York Mets",R),
    ("NOC-27","Ronald Acuna Jr.","Atlanta Braves",R),("NOC-28","James Wood","Washington Nationals",R),
    ("NOC-29","Yordan Alvarez","Houston Astros",R),("NOC-30","Julio Rodriguez","Seattle Mariners",R),
    ("NOC-31","Jose Ramirez","Cleveland Guardians",R),("NOC-32","Riley Greene","Detroit Tigers",R),
    ("NOC-33","Pete Crow-Armstrong","Chicago Cubs",R),("NOC-34","Paul Skenes","Pittsburgh Pirates",R),
    ("NOC-35","Nick Kurtz","Athletics",R),("NOC-36","Jacob Wilson","Athletics",R),
    ("NOC-37","Mike Trout","Los Angeles Angels",R),("NOC-38","Elly De La Cruz","Cincinnati Reds",R),
    ("NOC-39","Corbin Carroll","Arizona Diamondbacks",R),("NOC-40","Trea Turner","Philadelphia Phillies",R),
])

# ─── DEPTH OF DARKNESS ────────────────────────────────────────────
add_cards("Depth Of Darkness", [
    ("DOD-1","Jac Caglianone","Kansas City Royals",T),("DOD-2","Roman Anthony","Boston Red Sox",T),
    ("DOD-3","Colson Montgomery","Chicago White Sox",T),("DOD-4","Samuel Basallo","Baltimore Orioles",T),
    ("DOD-5","Bubba Chandler","Pittsburgh Pirates",T),("DOD-6","Bryce Eldridge","San Francisco Giants",T),
    ("DOD-7","Carson Williams","Tampa Bay Rays",T),("DOD-8","Shohei Ohtani","Los Angeles Dodgers",R),
    ("DOD-9","Aaron Judge","New York Yankees",R),("DOD-10","Bryce Harper","Philadelphia Phillies",R),
    ("DOD-11","Juan Soto","New York Mets",R),("DOD-12","Pete Crow-Armstrong","Chicago Cubs",R),
    ("DOD-13","Paul Skenes","Pittsburgh Pirates",R),("DOD-14","Mike Trout","Los Angeles Angels",R),
    ("DOD-15","Elly De La Cruz","Cincinnati Reds",R),("DOD-16","Cal Raleigh","Seattle Mariners",R),
    ("DOD-17","Bobby Witt Jr.","Kansas City Royals",R),("DOD-18","Francisco Lindor","New York Mets",R),
    ("DOD-19","Ronald Acuna Jr.","Atlanta Braves",R),("DOD-20","Fernando Tatis Jr.","San Diego Padres",R),
])

# ─── HOME FIELD ───────────────────────────────────────────────────
add_cards("Home Field", [
    ("CBHA-1","Jac Caglianone","Kansas City Royals",T),("CBHA-2","Roman Anthony","Boston Red Sox",T),
    ("CBHA-3","Aaron Judge","New York Yankees",R),("CBHA-4","Kyle Teel","Chicago White Sox",T),
    ("CBHA-5","Shohei Ohtani","Los Angeles Dodgers",R),("CBHA-6","Harry Ford","Seattle Mariners",T),
    ("CBHA-7","Bobby Witt Jr.","Kansas City Royals",R),("CBHA-8","Pete Crow-Armstrong","Chicago Cubs",R),
    ("CBHA-9","Bryce Harper","Philadelphia Phillies",R),("CBHA-10","Trey Yesavage","Toronto Blue Jays",T),
    ("CBHA-11","Owen Caissie","Chicago Cubs",T),("CBHA-12","Honus Wagner","Pittsburgh Pirates",R),
    ("CBHA-13","Bubba Chandler","Pittsburgh Pirates",T),("CBHA-14","Jacob Misiorowski","Milwaukee Brewers",T),
    ("CBHA-15","Samuel Basallo","Baltimore Orioles",T),("CBHA-16","Chase Burns","Cincinnati Reds",T),
    ("CBHA-17","Cal Raleigh","Seattle Mariners",R),("CBHA-18","Ken Griffey Jr.","Seattle Mariners",R),
    ("CBHA-19","Bryce Eldridge","San Francisco Giants",T),("CBHA-20","Colson Montgomery","Chicago White Sox",T),
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
