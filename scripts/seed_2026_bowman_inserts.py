"""
Seed: 2026 Bowman Baseball — Part 4: Insert sets.
Usage: python3 scripts/seed_2026_bowman_inserts.py
"""
import sqlite3, os, re

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA foreign_keys=ON")
cur = conn.cursor()

SET_ID = 52
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

# ─── BOWMAN SCOUTS TOP 100 ───────────────────────────────────────
add_cards("Bowman Scouts Top 100", [
    ("BTP-1","Konnor Griffin","Pittsburgh Pirates",T),("BTP-2","Kevin McGonigle","Detroit Tigers",T),("BTP-3","Leo De Vries","Athletics",T),
    ("BTP-4","Jesus Made","Milwaukee Brewers",T),("BTP-5","JJ Wetherholt","St. Louis Cardinals",T),("BTP-6","Sebastian Walcott","Texas Rangers",T),
    ("BTP-7","Max Clark","Detroit Tigers",T),("BTP-8","Walker Jenkins","Minnesota Twins",T),("BTP-9","Josue De Paula","Los Angeles Dodgers",T),
    ("BTP-10","Ethan Holliday","Colorado Rockies",T),("BTP-11","Eli Willits","Washington Nationals",T),("BTP-12","Colt Emerson","Seattle Mariners",T),
    ("BTP-13","Travis Bazzana","Cleveland Guardians",T),("BTP-14","Luis Pena","Milwaukee Brewers",T),("BTP-15","Zyhir Hope","Los Angeles Dodgers",T),
    ("BTP-16","Andrew Painter","Philadelphia Phillies",T),("BTP-17","George Lombard Jr.","New York Yankees",T),("BTP-18","Aiva Arquette","Miami Marlins",T),
    ("BTP-19","Thomas White","Miami Marlins",T),("BTP-20","Carson Benge","New York Mets",T),("BTP-21","Kade Anderson","Seattle Mariners",T),
    ("BTP-22","Seth Hernandez","Pittsburgh Pirates",T),("BTP-23","Bryce Rainer","Detroit Tigers",T),("BTP-24","Aidan Miller","Philadelphia Phillies",T),
    ("BTP-25","Edward Florentino","Pittsburgh Pirates",T),("BTP-26","Franklin Arias","Boston Red Sox",T),("BTP-27","Josuar Gonzalez","San Francisco Giants",T),
    ("BTP-28","Lazaro Montes","Seattle Mariners",T),("BTP-29","Josue Briceno","Detroit Tigers",T),("BTP-30","Liam Doyle","St. Louis Cardinals",T),
    ("BTP-31","Jamie Arnold","Athletics",T),("BTP-32","Arjun Nimmala","Toronto Blue Jays",T),("BTP-33","Wehiwa Aloy","Baltimore Orioles",T),
    ("BTP-34","Eduardo Quintero","Los Angeles Dodgers",T),("BTP-35","JoJo Parker","Toronto Blue Jays",T),("BTP-36","Charlie Condon","Colorado Rockies",T),
    ("BTP-37","Elian Pena","New York Mets",T),("BTP-38","Rainiel Rodriguez","St. Louis Cardinals",T),("BTP-39","Braden Montgomery","Chicago White Sox",T),
    ("BTP-40","Cooper Pratt","Milwaukee Brewers",T),("BTP-41","Kaelen Culpepper","Minnesota Twins",T),("BTP-42","Robby Snelling","Miami Marlins",T),
    ("BTP-43","Justin Crawford","Philadelphia Phillies",T),("BTP-44","Eduardo Tait","Minnesota Twins",T),("BTP-45","Billy Carlson","Chicago White Sox",T),
    ("BTP-46","Caleb Bonemer","Chicago White Sox",T),("BTP-47","Daniel Pierce","Tampa Bay Rays",T),("BTP-48","Jonny Farmelo","Seattle Mariners",T),
    ("BTP-49","Noah Schultz","Chicago White Sox",T),("BTP-50","Xavier Neyens","Houston Astros",T),("BTP-51","Alfredo Duno","Cincinnati Reds",T),
    ("BTP-52","Nate George","Baltimore Orioles",T),("BTP-53","Marek Houston","Minnesota Twins",T),("BTP-54","Mike Sirota","Los Angeles Dodgers",T),
    ("BTP-55","Ryan Waldschmidt","Arizona Diamondbacks",T),("BTP-56","Blake Mitchell","Kansas City Royals",T),("BTP-57","Ryan Sloan","Seattle Mariners",T),
    ("BTP-58","Angel Genao","Cleveland Guardians",T),("BTP-59","Steele Hall","Cincinnati Reds",T),("BTP-60","Gavin Kilen","San Francisco Giants",T),
    ("BTP-61","Emil Morales","Los Angeles Dodgers",T),("BTP-62","Travis Sykora","Washington Nationals",T),("BTP-63","Kyson Witherspoon","Boston Red Sox",T),
    ("BTP-64","Michael Arroyo","Seattle Mariners",T),("BTP-65","Gavin Fien","Texas Rangers",T),("BTP-66","Tyler Bremner","Los Angeles Angels",T),
    ("BTP-67","Cam Caminiti","Atlanta Braves",T),("BTP-68","Tyson Lewis","Cincinnati Reds",T),("BTP-69","Theo Gillen","Tampa Bay Rays",T),
    ("BTP-70","Hagen Smith","Chicago White Sox",T),("BTP-71","Andrew Fischer","Milwaukee Brewers",T),("BTP-72","Jaxon Wiggins","Chicago Cubs",T),
    ("BTP-73","JR Ritchie","Atlanta Braves",T),("BTP-74","Jarlin Susana","Washington Nationals",T),("BTP-75","Shotaro Morii","Athletics",T),
    ("BTP-76","Jhonny Level","San Francisco Giants",T),("BTP-77","Felnin Celesten","Seattle Mariners",T),("BTP-78","Dax Kilby","New York Yankees",T),
    ("BTP-79","Kayson Cunningham","Arizona Diamondbacks",T),("BTP-80","Bo Davidson","San Francisco Giants",T),("BTP-81","Slade Caldwell","Arizona Diamondbacks",T),
    ("BTP-82","Andrew Salas","Miami Marlins",T),("BTP-83","Spencer Jones","New York Yankees",T),("BTP-84","Ike Irish","Baltimore Orioles",T),
    ("BTP-85","Cris Rodriguez","Detroit Tigers",T),("BTP-86","Roldy Brito","Colorado Rockies",T),("BTP-87","Carlos Lagrange","New York Yankees",T),
    ("BTP-88","Robert Calaz","Colorado Rockies",T),("BTP-89","Gage Jump","Athletics",T),("BTP-90","Ching-Hsien Ko","Los Angeles Dodgers",T),
    ("BTP-91","Dakota Jordan","San Francisco Giants",T),("BTP-92","Tommy Troy","Arizona Diamondbacks",T),("BTP-93","Wei-En Lin","Athletics",T),
    ("BTP-94","Kellon Lindsey","Los Angeles Dodgers",T),("BTP-95","Cam Collier","Cincinnati Reds",T),("BTP-96","Esteban Mejia","Baltimore Orioles",T),
    ("BTP-97","Leonardo Bernal","St. Louis Cardinals",T),("BTP-98","Elmer Rodriguez-Cruz","New York Yankees",T),("BTP-99","Enrique Bradfield Jr.","Baltimore Orioles",T),
    ("BTP-100","Gage Wood","Philadelphia Phillies",T),
])

# ─── BOWMAN STERLING ─────────────────────────────────────────────
add_cards("Bowman Sterling", [
    ("BST-1","Jackson Chourio","Milwaukee Brewers",R),("BST-2","Freddie Freeman","Los Angeles Dodgers",R),("BST-3","Julio Rodriguez","Seattle Mariners",R),
    ("BST-4","Aaron Judge","New York Yankees",R),("BST-5","Max Clark","Detroit Tigers",T),("BST-6","Shohei Ohtani","Los Angeles Dodgers",R),
    ("BST-7","Konnor Griffin","Pittsburgh Pirates",T),("BST-8","Nolan McLean","New York Mets",T),("BST-9","Leo De Vries","Athletics",T),
    ("BST-10","Chase Burns","Cincinnati Reds",T),("BST-11","Ethan Holliday","Colorado Rockies",T),("BST-12","Roman Anthony","Boston Red Sox",T),
    ("BST-13","Jacob Misiorowski","Milwaukee Brewers",T),("BST-14","Jac Caglianone","Kansas City Royals",T),("BST-15","Carson Williams","Tampa Bay Rays",T),
])

# ─── PATCHWORK ────────────────────────────────────────────────────
add_cards("Patchwork", [
    ("P-1","Ceddanne Rafaela","Boston Red Sox",R),("P-2","Josue De Paula","Los Angeles Dodgers",T),("P-3","Jackson Chourio","Milwaukee Brewers",R),
    ("P-4","Colson Montgomery","Chicago White Sox",T),("P-5","Konnor Griffin","Pittsburgh Pirates",T),("P-6","Francisco Lindor","New York Mets",R),
    ("P-7","Shohei Ohtani","Los Angeles Dodgers",R),("P-8","Sebastian Walcott","Texas Rangers",T),("P-9","Vladimir Guerrero Jr.","Toronto Blue Jays",R),
    ("P-10","Yoshinobu Yamamoto","Los Angeles Dodgers",R),("P-11","Bryce Eldridge","San Francisco Giants",T),("P-12","Ichiro","Seattle Mariners",R),
    ("P-13","Cal Ripken Jr.","Baltimore Orioles",R),("P-14","Andrew McCutchen","Pittsburgh Pirates",R),("P-15","Juan Soto","New York Mets",R),
    ("P-16","Manny Machado","San Diego Padres",R),("P-17","Jesus Made","Milwaukee Brewers",T),("P-18","Bryce Harper","Philadelphia Phillies",R),
    ("P-19","Roki Sasaki","Los Angeles Dodgers",R),("P-20","George Lombard Jr.","New York Yankees",T),("P-21","Charlie Condon","Colorado Rockies",T),
    ("P-22","Tony Gwynn","San Diego Padres",R),("P-23","Jac Caglianone","Kansas City Royals",T),("P-24","Fernando Tatis Jr.","San Diego Padres",R),
    ("P-25","Max Clark","Detroit Tigers",T),("P-26","Junior Caminero","Tampa Bay Rays",R),("P-27","Jose Ramirez","Cleveland Guardians",R),
    ("P-28","Jim Thome","Philadelphia Phillies",R),("P-29","JJ Wetherholt","St. Louis Cardinals",T),("P-30","James Wood","Washington Nationals",R),
])

# ─── ELECTRIC SLUGGERS ───────────────────────────────────────────
add_cards("Electric Sluggers", [
    ("ES-1","Francisco Lindor","New York Mets",R),("ES-2","Vladimir Guerrero Jr.","Toronto Blue Jays",R),("ES-3","Fernando Tatis Jr.","San Diego Padres",R),
    ("ES-4","Junior Caminero","Tampa Bay Rays",R),("ES-5","Mookie Betts","Los Angeles Dodgers",R),("ES-6","Bryce Harper","Philadelphia Phillies",R),
    ("ES-7","Juan Soto","New York Mets",R),("ES-8","Ronald Acuna Jr.","Atlanta Braves",R),("ES-9","Elly De La Cruz","Cincinnati Reds",R),
    ("ES-10","Samuel Basallo","Baltimore Orioles",T),("ES-11","Bryce Eldridge","San Francisco Giants",T),("ES-12","JJ Wetherholt","St. Louis Cardinals",T),
    ("ES-13","Ethan Holliday","Colorado Rockies",T),("ES-14","Cal Raleigh","Seattle Mariners",R),("ES-15","Aaron Judge","New York Yankees",R),
    ("ES-16","Roman Anthony","Boston Red Sox",T),("ES-17","Konnor Griffin","Pittsburgh Pirates",T),("ES-18","Shohei Ohtani","Los Angeles Dodgers",R),
    ("ES-19","Bobby Witt Jr.","Kansas City Royals",R),("ES-20","Jesus Made","Milwaukee Brewers",T),("ES-21","Aiva Arquette","Miami Marlins",T),
    ("ES-22","Nick Kurtz","Athletics",T),("ES-23","Jac Caglianone","Kansas City Royals",T),("ES-24","Pete Crow-Armstrong","Chicago Cubs",R),
    ("ES-25","Mike Trout","Los Angeles Angels",R),
])

# ─── UNDER THE RADAR ─────────────────────────────────────────────
add_cards("Under The Radar", [
    ("UR-1","Kevin McGonigle","Detroit Tigers",T),("UR-2","Cam Schlittler","New York Yankees",T),("UR-3","Jhonny Level","San Francisco Giants",T),
    ("UR-4","Colt Emerson","Seattle Mariners",T),("UR-5","Franklin Arias","Boston Red Sox",T),("UR-6","Kyle Teel","Chicago White Sox",T),
    ("UR-7","Rainiel Rodriguez","St. Louis Cardinals",T),("UR-8","Thomas White","Miami Marlins",T),("UR-9","Edward Florentino","Pittsburgh Pirates",T),
    ("UR-10","Ryan Waldschmidt","Arizona Diamondbacks",T),("UR-11","Sal Stewart","Cincinnati Reds",T),("UR-12","Carson Benge","New York Mets",T),
    ("UR-13","Daniel Pierce","Tampa Bay Rays",T),("UR-14","Josue De Paula","Los Angeles Dodgers",T),("UR-15","Trey Yesavage","Toronto Blue Jays",T),
    ("UR-16","Samuel Basallo","Baltimore Orioles",T),("UR-17","Wehiwa Aloy","Baltimore Orioles",T),("UR-18","Caleb Bonemer","Chicago White Sox",T),
    ("UR-19","Connelly Early","Boston Red Sox",T),("UR-20","Kaelen Culpepper","Minnesota Twins",T),
])

# ─── POWER CHORDS ────────────────────────────────────────────────
add_cards("Power Chords", [
    ("PC-1","Aaron Judge","New York Yankees",R),("PC-2","Charlie Condon","Colorado Rockies",T),("PC-3","Ronald Acuna Jr.","Atlanta Braves",R),
    ("PC-4","Jackson Chourio","Milwaukee Brewers",R),("PC-5","JJ Wetherholt","St. Louis Cardinals",T),("PC-6","Nick Kurtz","Athletics",T),
    ("PC-7","Bryce Harper","Philadelphia Phillies",R),("PC-8","Walker Jenkins","Minnesota Twins",T),("PC-9","Vladimir Guerrero Jr.","Toronto Blue Jays",R),
    ("PC-10","Edward Florentino","Pittsburgh Pirates",T),("PC-11","Shohei Ohtani","Los Angeles Dodgers",R),("PC-12","Juan Soto","New York Mets",R),
    ("PC-13","Bobby Witt Jr.","Kansas City Royals",R),("PC-14","Roman Anthony","Boston Red Sox",T),("PC-15","Kevin McGonigle","Detroit Tigers",T),
    ("PC-16","Bryce Eldridge","San Francisco Giants",T),("PC-17","Jac Caglianone","Kansas City Royals",T),("PC-18","Aiva Arquette","Miami Marlins",T),
    ("PC-19","Christian Moore","Los Angeles Angels",T),("PC-20","Ethan Holliday","Colorado Rockies",T),("PC-21","Cal Raleigh","Seattle Mariners",R),
    ("PC-22","Fernando Tatis Jr.","San Diego Padres",R),("PC-23","Junior Caminero","Tampa Bay Rays",R),("PC-24","Mike Trout","Los Angeles Angels",R),
    ("PC-25","Samuel Basallo","Baltimore Orioles",T),
])

# ─── ANIME ────────────────────────────────────────────────────────
ANIME_ROOKIES = {"Ethan Holliday","Tatsuya Imai","Shotaro Morii","Roman Anthony","Eli Willits","Jesus Made",
    "Kazuma Okamoto","Konnor Griffin","Jacob Misiorowski","Samuel Basallo","Jac Caglianone","Nick Kurtz","Munetaka Murakami","Paul Skenes"}
anime_raw = [
    ("BA-1","Sadaharu Oh","Yomiuri Giants"),("BA-2","Cal Raleigh","Seattle Mariners"),("BA-3","Munetaka Murakami","Chicago White Sox"),
    ("BA-4","Aaron Judge","New York Yankees"),("BA-5","Bobby Witt Jr.","Kansas City Royals"),("BA-6","Nick Kurtz","Athletics"),
    ("BA-7","Ethan Holliday","Colorado Rockies"),("BA-8","Tatsuya Imai","Houston Astros"),("BA-9","Shotaro Morii","Athletics"),
    ("BA-10","Manny Ramirez","Boston Red Sox"),("BA-11","Sammy Sosa","Chicago Cubs"),("BA-12","Ken Griffey Jr.","Seattle Mariners"),
    ("BA-13","Roman Anthony","Boston Red Sox"),("BA-14","Eli Willits","Washington Nationals"),("BA-15","Jesus Made","Milwaukee Brewers"),
    ("BA-16","Hideo Nomo","Los Angeles Dodgers"),("BA-17","Kazuma Okamoto","Toronto Blue Jays"),("BA-18","Konnor Griffin","Pittsburgh Pirates"),
    ("BA-19","Jackie Robinson","Brooklyn Dodgers"),("BA-20","Jacob Misiorowski","Milwaukee Brewers"),("BA-21","Juan Soto","New York Mets"),
    ("BA-22","Bo Jackson","Kansas City Royals"),("BA-23","Mike Trout","Los Angeles Angels"),("BA-24","Paul Skenes","Pittsburgh Pirates"),
    ("BA-25","Samuel Basallo","Baltimore Orioles"),("BA-26","Shohei Ohtani","Los Angeles Dodgers"),("BA-27","Jac Caglianone","Kansas City Royals"),
    ("BA-28","Joey Votto","Cincinnati Reds"),("BA-29","Rickey Henderson","Athletics"),
]
anime_is = get_is_id("Anime")
for num, name, team in anime_raw:
    pid = get_or_create_player(name)
    cur.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)",
                (pid, anime_is, num, int(name in ANIME_ROOKIES), team))
print(f"  Anime: {len(anime_raw)} cards")

# ─── ANIME - KANJI VARIATIONS ────────────────────────────────────
kanji_is = get_is_id("Anime - Kanji Variations")
kanji = [("BA-1","Sadaharu Oh","Yomiuri Giants"),("BA-3","Munetaka Murakami","Chicago White Sox"),("BA-8","Tatsuya Imai","Houston Astros"),
    ("BA-9","Shotaro Morii","Athletics"),("BA-16","Hideo Nomo","Los Angeles Dodgers"),("BA-17","Kazuma Okamoto","Toronto Blue Jays"),
    ("BA-26","Shohei Ohtani","Los Angeles Dodgers")]
for num, name, team in kanji:
    pid = get_or_create_player(name)
    cur.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, ?)", (pid, kanji_is, num, team))
print(f"  Anime - Kanji Variations: {len(kanji)} cards")

# ─── FINAL DRAFT ──────────────────────────────────────────────────
add_cards("Final Draft", [
    ("FD-1","Derek Jeter","New York Yankees",R),("FD-2","Ken Griffey Jr.","Seattle Mariners",R),("FD-3","Ethan Holliday","Colorado Rockies",T),
    ("FD-4","Bryce Eldridge","San Francisco Giants",T),("FD-5","Munetaka Murakami","Chicago White Sox",T),("FD-6","Ronald Acuna Jr.","Atlanta Braves",R),
    ("FD-7","Samuel Basallo","Baltimore Orioles",T),("FD-8","Jacob Misiorowski","Milwaukee Brewers",T),("FD-9","Juan Soto","New York Mets",R),
    ("FD-10","Jac Caglianone","Kansas City Royals",T),("FD-11","Shohei Ohtani","Los Angeles Dodgers",R),("FD-12","Nick Kurtz","Athletics",T),
    ("FD-13","Roman Anthony","Boston Red Sox",T),("FD-14","Paul Skenes","Pittsburgh Pirates",R),("FD-15","Manny Ramirez","Boston Red Sox",R),
    ("FD-16","Mark McGwire","St. Louis Cardinals",R),("FD-17","Elly De La Cruz","Cincinnati Reds",R),("FD-18","Konnor Griffin","Pittsburgh Pirates",T),
    ("FD-19","Bryce Harper","Philadelphia Phillies",R),("FD-20","Cal Raleigh","Seattle Mariners",R),
])

# ─── CRYSTALLIZED ─────────────────────────────────────────────────
add_cards("Crystallized", [
    ("BWC-1","Aiva Arquette","Miami Marlins",T),("BWC-2","Ronald Acuna Jr.","Atlanta Braves",R),("BWC-3","Marek Houston","Minnesota Twins",T),
    ("BWC-4","Edward Florentino","Pittsburgh Pirates",T),("BWC-5","Jacob Misiorowski","Milwaukee Brewers",T),("BWC-6","Bryce Eldridge","San Francisco Giants",T),
    ("BWC-7","Bobby Witt Jr.","Kansas City Royals",R),("BWC-8","Aaron Judge","New York Yankees",R),("BWC-9","Samuel Basallo","Baltimore Orioles",T),
    ("BWC-10","Daniel Pierce","Tampa Bay Rays",T),("BWC-11","Sal Stewart","Cincinnati Reds",T),("BWC-12","Vladimir Guerrero Jr.","Toronto Blue Jays",R),
    ("BWC-13","Jac Caglianone","Kansas City Royals",T),("BWC-14","Ethan Holliday","Colorado Rockies",T),("BWC-15","Bubba Chandler","Pittsburgh Pirates",T),
    ("BWC-16","Paul Skenes","Pittsburgh Pirates",R),("BWC-17","Colson Montgomery","Chicago White Sox",T),("BWC-18","Roman Anthony","Boston Red Sox",T),
    ("BWC-19","Shohei Ohtani","Los Angeles Dodgers",R),("BWC-20","Francisco Lindor","New York Mets",R),
])

# ─── BOWMAN SPOTLIGHTS ────────────────────────────────────────────
add_cards("Bowman Spotlights", [
    ("BS-1","Colson Montgomery","Chicago White Sox",T),("BS-2","Nolan McLean","New York Mets",T),("BS-3","Samuel Basallo","Baltimore Orioles",T),
    ("BS-4","Jac Caglianone","Kansas City Royals",T),("BS-5","Cam Schlittler","New York Yankees",T),("BS-6","Roman Anthony","Boston Red Sox",T),
    ("BS-7","Bryce Eldridge","San Francisco Giants",T),("BS-8","Chase Burns","Cincinnati Reds",T),("BS-9","Aiva Arquette","Miami Marlins",T),
    ("BS-10","Edward Florentino","Pittsburgh Pirates",T),("BS-11","Wehiwa Aloy","Baltimore Orioles",T),("BS-12","Bubba Chandler","Pittsburgh Pirates",T),
    ("BS-13","Ethan Holliday","Colorado Rockies",T),("BS-14","Trey Yesavage","Toronto Blue Jays",T),("BS-15","Christian Moore","Los Angeles Angels",T),
])

# ─── Generate slugs for new players ──────────────────────────────
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
print(f"  Total players: {player_count}")
print(f"  Total appearances: {app_count}")
conn.close()
