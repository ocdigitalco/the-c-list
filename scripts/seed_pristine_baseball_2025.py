"""
Seed script: 2025 Topps Pristine Baseball
Inserts all data into the local SQLite database (the-c-list.db).
Usage: python3 scripts/seed_pristine_baseball_2025.py
"""

import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA foreign_keys=ON")
cur = conn.cursor()

# ─── Helpers ────────────────────────────────────────────────────────────────────


def get_or_create_player(set_id, name):
    cur.execute("SELECT id FROM players WHERE set_id = ? AND name = ?", (set_id, name))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(
        "INSERT INTO players (set_id, name, unique_cards, total_print_run, one_of_ones, insert_set_count) VALUES (?, ?, 0, 0, 0, 0)",
        (set_id, name),
    )
    return cur.lastrowid


def create_insert_set(set_id, name):
    cur.execute("INSERT INTO insert_sets (set_id, name) VALUES (?, ?)", (set_id, name))
    return cur.lastrowid


def create_parallel(insert_set_id, name, print_run):
    cur.execute(
        "INSERT INTO parallels (insert_set_id, name, print_run) VALUES (?, ?, ?)",
        (insert_set_id, name, print_run),
    )
    return cur.lastrowid


def create_appearance(player_id, insert_set_id, card_number, is_rookie=False, team=None):
    cur.execute(
        "INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)",
        (player_id, insert_set_id, card_number, int(is_rookie), team),
    )
    return cur.lastrowid


def create_co_player(appearance_id, co_player_id):
    cur.execute(
        "INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)",
        (appearance_id, co_player_id),
    )


# ─── RC players ───────────────────────────────────────────────────────────────

ROOKIES = {
    "Drew Thorpe", "Chase Petty", "Kumar Rocker", "Ben Rice", "Caden Dana",
    "James Wood", "Nic Enright", "Nacho Alvarez Jr.", "Brooks Lee", "Max Muncy",
    "Spencer Schwellenbach", "Adael Amador", "Luisangel Acuña", "Justyn-Henry Malloy",
    "Rece Hinds", "Trey Sweeney", "Angel Martínez", "Jackson Jobe", "Tyler Locklear",
    "Richard Fitts", "Dylan Crews", "Chase Meidroth", "River Ryan", "Thomas Saggese",
    "Edgar Quero", "Denzel Clarke", "Rhett Lowder", "Coby Mayo", "Alejandro Osuna",
    "Jacob Wilson", "Kevin Alcántara", "Chase Dollander", "Daylen Lile", "Ryan Bliss",
    "Orelvis Martinez", "Nick Yorke", "Jace Jung", "Kristian Campbell", "Tomoyuki Sugano",
    "Hyeseong Kim", "Connor Norby", "Dalton Rushing", "Nick Kurtz", "Jhonkensy Noel",
    "Brooks Baldwin", "Roki Sasaki", "Marcelo Mayer", "Cade Horton", "Aaron Schunk",
    "Victor Mesa Jr.", "Jorbit Vivas", "Caleb Durbin", "Dillon Dingler", "Agustín Ramírez",
    "Logan Evans", "Moisés Ballesteros", "Mick Abel", "Sam Aldegheri", "Niko Kavadas",
    "Griffin Conine", "Luke Keaschall", "Will Warren", "Zac Veen", "Drew Romo",
    "Leo Jiménez", "Alan Roden", "Kameron Misner", "Cam Smith", "Drake Baldwin",
    "Logan Henderson", "Chandler Simpson", "Matt Shaw", "Grant McCray", "Robert Hassell III",
    "Braxton Ashcraft", "Darren Baker", "Ben Williamson",
}


def add_cards(insert_set_id, cards):
    """Add cards. cards = [(card_number, name, team), ...]"""
    for card_number, name, team in cards:
        is_rookie = name in ROOKIES
        player_id = get_or_create_player(set_id, name)
        create_appearance(player_id, insert_set_id, card_number, is_rookie, team)


def add_multi_cards(insert_set_id, cards):
    """Add co-player cards. cards = [(card_number, [(name, team), ...]), ...]"""
    for card_number, players in cards:
        app_ids = []
        player_ids = []
        for name, team in players:
            is_rookie = name in ROOKIES
            player_id = get_or_create_player(set_id, name)
            app_id = create_appearance(player_id, insert_set_id, card_number, is_rookie, team)
            app_ids.append(app_id)
            player_ids.append(player_id)
        for i, app_id in enumerate(app_ids):
            for j, other_player_id in enumerate(player_ids):
                if i != j:
                    create_co_player(app_id, other_player_id)


def make_insert_set(name, parallels_def, cards, is_multi=False):
    is_id = create_insert_set(set_id, name)
    for par_name, par_pr in parallels_def:
        create_parallel(is_id, par_name, par_pr)
    if is_multi:
        add_multi_cards(is_id, cards)
    else:
        add_cards(is_id, cards)
    return is_id


# ─── 1. Create the set ─────────────────────────────────────────────────────────

SET_NAME = "2025 Topps Pristine Baseball"

cur.execute("SELECT id FROM sets WHERE name = ?", (SET_NAME,))
existing = cur.fetchone()
if existing:
    print(f"Set '{SET_NAME}' already exists with id {existing[0]}. Aborting.")
    conn.close()
    exit(1)

box_config = {
    "hobby": {
        "cards_per_pack": 8,
        "packs_per_box": 6,
        "boxes_per_case": 6,
        "autos_per_box": 2,
        "notes": "1 Autograph Relic, 2 Autographs, 4 Pristine Parallels, 6 Refractor Parallels, 6 Numbered Base or Insert Parallels per box",
    },
}

pack_odds = {
    "hobby": {
        "Base Refractor": "1:1",
        "Base Pristine Aqua Refractor": "1:4",
        "Base Pristine Purple Refractor": "1:7",
        "Base Pristine Blue Refractor": "1:9",
        "Base Pristine Gold Refractor": "1:13",
        "Base Pristine Orange Refractor": "1:26",
        "Base Pristine Pink Refractor": "1:43",
        "Base Pristine Primaries Refractor": "1:65",
        "Base Pristine Red Refractor": "1:129",
        "Base Pristine Black Refractor": "1:643",
        "Perseverance": "1:4",
        "Perseverance Purple Refractor": "1:78",
        "Perseverance Blue Refractor": "1:103",
        "Perseverance Gold Refractor": "1:155",
        "Perseverance Orange Refractor": "1:308",
        "Perseverance Red Refractor": "1:1536",
        "Perseverance Superfractor": "1:7740",
        "Plated & Polished": "1:3",
        "Plated & Polished Purple Refractor": "1:49",
        "Plated & Polished Blue Refractor": "1:65",
        "Plated & Polished Gold Refractor": "1:97",
        "Plated & Polished Orange Refractor": "1:193",
        "Plated & Polished Red Refractor": "1:963",
        "Plated & Polished Superfractor": "1:4764",
        "Precisionaries": "1:3",
        "Precisionaries Purple Refractor": "1:56",
        "Precisionaries Blue Refractor": "1:74",
        "Precisionaries Gold Refractor": "1:110",
        "Precisionaries Orange Refractor": "1:220",
        "Precisionaries Red Refractor": "1:1100",
        "Precisionaries Superfractor": "1:5464",
        "Amped": "1:144",
        "Amped Superfractor": "1:7740",
        "Let's Go": "1:770",
        "Let's Go Red Refractor": "1:7740",
        "Let's Go Superfractor": "1:37152",
        "Monogram": "1:120",
        "Monogram Superfractor": "1:6406",
        "Pearlescent": "1:144",
        "Pearlescent Superfractor": "1:7740",
        "Prowlers": "1:242",
        "Prowlers Superfractor": "1:12834",
        "Pristine Autographs": "1:7",
        "Pristine Autographs Green Pristine": "1:16",
        "Pristine Autographs Purple Pristine": "1:22",
        "Pristine Autographs Blue Pristine": "1:28",
        "Pristine Autographs Gold Pristine": "1:41",
        "Pristine Autographs Orange Pristine": "1:82",
        "Pristine Autographs Pink Pristine": "1:133",
        "Pristine Autographs Primaries Pristine": "1:200",
        "Pristine Autographs Red Pristine": "1:398",
        "Pristine Autographs Black Pristine": "1:1998",
        "Italics": "1:322",
        "Italics Blue Refractor": "1:320",
        "Italics Gold Refractor": "1:258",
        "Italics Orange Refractor": "1:509",
        "Italics Red Refractor": "1:2545",
        "Italics Superfractor": "1:12384",
        "Personal Endorsements Autographs": "1:243",
        "Personal Endorsements Autographs Red Refractor": "1:1184",
        "Personal Endorsements Autographs Superfractor": "1:5993",
        "Plated & Polished Autograph Variations": "1:139",
        "Plated & Polished Autograph Variations Blue Refractor": "1:257",
        "Plated & Polished Autograph Variations Gold Refractor": "1:201",
        "Plated & Polished Autograph Variations Orange Refractor": "1:386",
        "Plated & Polished Autograph Variations Red Refractor": "1:1896",
        "Plated & Polished Autograph Variations Superfractor": "1:9776",
        "Popular Demand Auto Relic": "1:100",
        "Popular Demand Auto Relic Blue Refractor": "1:160",
        "Popular Demand Auto Relic Gold Refractor": "1:142",
        "Popular Demand Auto Relic Orange Refractor": "1:226",
        "Popular Demand Auto Relic Pink Refractor": "1:374",
        "Popular Demand Auto Relic Red Refractor": "1:1327",
        "Popular Demand Auto Relic Superfractor": "1:6406",
        "Pristine Pieces Auto Relic": "1:16",
        "Pristine Pieces Auto Relic Pristine Refractor": "1:48",
        "Pristine Pieces Auto Relic Blue Refractor": "1:51",
        "Pristine Pieces Auto Relic Gold Refractor": "1:69",
        "Pristine Pieces Auto Relic Orange Refractor": "1:137",
        "Pristine Pieces Auto Relic Pink Refractor": "1:225",
        "Pristine Pieces Auto Relic Red Refractor": "1:707",
        "Pristine Pieces Auto Relic Superfractor": "1:3573",
        "All Star Game Pristine Pieces Auto Relic": "1:7145",
        "Pristine Pairs Dual Autograph": "1:1300",
        "Pristine Pairs Dual Autograph Red Refractor": "1:6406",
        "Pristine Pairs Dual Autograph Superfractor": "1:30960",
        "Rookie Jumbo Relic Auto": "1:404",
        "Rookie Jumbo Relic Auto Red Refractor": "1:2020",
        "Rookie Jumbo Relic Auto Superfractor": "1:9777",
    },
}

cur.execute(
    "INSERT INTO sets (name, sport, season, league, tier, box_config, release_date, pack_odds) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    (SET_NAME, "Baseball", "2025", "MLB", "Premium", json.dumps(box_config), "2026-02-12", json.dumps(pack_odds)),
)
set_id = cur.lastrowid
print(f"Created set '{SET_NAME}' with id {set_id}")

# ─── 2. Parallel definitions ─────────────────────────────────────────────────

BASE_PARALLELS = [
    ("Refractor", None),
    ("Pristine Refractor", None),
    ("Pristine Aqua Refractor", 199),
    ("Aqua Refractor", 150),
    ("Pristine Purple Refractor", 99),
    ("Purple Refractor", 99),
    ("Pristine Blue Refractor", 75),
    ("Blue Refractor", 75),
    ("Pristine Gold Refractor", 50),
    ("Gold Refractor", 50),
    ("Pristine Orange Refractor", 25),
    ("Orange Refractor", 25),
    ("Pristine Pink Refractor", 15),
    ("Pink Refractor", 15),
    ("Pristine Primaries Refractor", 10),
    ("Primaries Refractor", 10),
    ("Pristine Red Refractor", 5),
    ("Red Refractor", 5),
    ("Pristine Black Refractor", 1),
    ("Superfractor", 1),
]

# Pristine Autographs parallels
PRISTINE_AUTO_PARALLELS = [
    ("Green Pristine", 150),
    ("Purple Pristine", 99),
    ("Blue Pristine", 75),
    ("Gold Pristine", 50),
    ("Orange Pristine", 25),
    ("Pink Pristine", 15),
    ("Primaries Pristine", 10),
    ("Red Pristine", 5),
    ("Black Pristine", 1),
]

# Pristine Pairs parallels
PRISTINE_PAIRS_PARALLELS = [
    ("Red", 5),
    ("Superfractor", 1),
]

# Plated and Polished Autographs parallels
PLATED_AUTO_PARALLELS = [
    ("Blue", 75),
    ("Gold", 50),
    ("Orange", 25),
    ("Red", 5),
    ("Superfractor", 1),
]

# Personal Endorsements parallels
PERSONAL_ENDORSEMENTS_PARALLELS = [
    ("Red", 5),
    ("Superfractor", 1),
]

# Italics parallels
ITALICS_PARALLELS = [
    ("Blue", 75),
    ("Gold", 50),
    ("Orange", 25),
    ("Red", 5),
    ("Superfractor", 1),
]

# Popular Demand Auto Relic parallels
POPULAR_DEMAND_PARALLELS = [
    ("Blue", 75),
    ("Gold", 50),
    ("Orange", 25),
    ("Pink", 15),
    ("Red", 5),
    ("Superfractor", 1),
]

# Pristine Pieces Auto Relic parallels
PRISTINE_PIECES_PARALLELS = [
    ("Pristine Refractor", 99),
    ("Blue", 75),
    ("Gold", 50),
    ("Orange", 25),
    ("Pink", 15),
    ("Red", 5),
    ("Superfractor", 1),
]

# Rookie Jumbo Relic Auto parallels (base /25)
ROOKIE_JUMBO_PARALLELS = [
    ("Base /25", 25),
    ("Red", 5),
    ("Superfractor", 1),
]

# Perseverance parallels
PERSEVERANCE_PARALLELS = [
    ("Purple", 99),
    ("Blue", 75),
    ("Gold", 50),
    ("Orange", 25),
    ("Red", 5),
    ("Superfractor", 1),
]

# Plated & Polished insert parallels
PLATED_INSERT_PARALLELS = [
    ("Purple", 99),
    ("Blue", 75),
    ("Gold", 50),
    ("Orange", 25),
    ("Red", 5),
    ("Superfractor", 1),
]

# Precisionaries parallels
PRECISIONARIES_PARALLELS = [
    ("Purple", 99),
    ("Blue", 75),
    ("Gold", 50),
    ("Orange", 25),
    ("Red", 5),
    ("Superfractor", 1),
]

# Pearlescent / Amped parallels
SUPERFRACTOR_ONLY = [
    ("Superfractor", 1),
]

# Monogram parallels
MONOGRAM_PARALLELS = [
    ("Superfractor", 1),
]

# Let's Go parallels
LETS_GO_PARALLELS = [
    ("Red", 5),
    ("Superfractor", 1),
]

# Prowlers parallels
PROWLERS_PARALLELS = [
    ("Superfractor", 1),
]

# ─── 3. Insert sets + cards ───────────────────────────────────────────────────

# ════════════════════════════════════════════════════════════════════════════════
# BASE SET (300 cards)
# ════════════════════════════════════════════════════════════════════════════════

make_insert_set("Base Set", BASE_PARALLELS, [
    ("1", "Drew Thorpe", "Chicago White Sox"),
    ("2", "Chase Petty", "Cincinnati Reds"),
    ("3", "Kumar Rocker", "Texas Rangers"),
    ("4", "Ben Rice", "New York Yankees"),
    ("5", "Caden Dana", "Los Angeles Angels"),
    ("6", "Pete Crow-Armstrong", "Chicago Cubs"),
    ("7", "Ozzie Albies", "Atlanta Braves"),
    ("8", "James Wood", "Washington Nationals"),
    ("9", "Nic Enright", "Cleveland Guardians"),
    ("10", "Nacho Alvarez Jr.", "Atlanta Braves"),
    ("11", "Shane Bieber", "Toronto Blue Jays"),
    ("12", "Garrett Crochet", "Boston Red Sox"),
    ("13", "Brooks Lee", "Minnesota Twins"),
    ("14", "Cal Ripken Jr.", "Baltimore Orioles"),
    ("15", "Max Muncy", "Athletics"),
    ("16", "Joe Morgan", "Cincinnati Reds"),
    ("17", "Spencer Schwellenbach", "Atlanta Braves"),
    ("18", "Josh Naylor", "Seattle Mariners"),
    ("19", "Adael Amador", "Colorado Rockies"),
    ("20", "Luisangel Acuña", "New York Mets"),
    ("21", "Justyn-Henry Malloy", "Detroit Tigers"),
    ("22", "Rece Hinds", "Cincinnati Reds"),
    ("23", "Brooks Robinson", "Baltimore Orioles"),
    ("24", "Trey Sweeney", "Detroit Tigers"),
    ("25", "Angel Martínez", "Cleveland Guardians"),
    ("26", "Kyle Tucker", "Chicago Cubs"),
    ("27", "Spencer Strider", "Atlanta Braves"),
    ("28", "Nomar Garciaparra", "Boston Red Sox"),
    ("29", "Jackson Jobe", "Detroit Tigers"),
    ("30", "Tyler Locklear", "Arizona Diamondbacks"),
    ("31", "Gunnar Henderson", "Baltimore Orioles"),
    ("32", "Adley Rutschman", "Baltimore Orioles"),
    ("33", "Seiya Suzuki", "Chicago Cubs"),
    ("34", "Randy Johnson", "Arizona Diamondbacks"),
    ("35", "Jarren Duran", "Boston Red Sox"),
    ("36", "Richard Fitts", "Boston Red Sox"),
    ("37", "Kyle Manzardo", "Cleveland Guardians"),
    ("38", "Dylan Crews", "Washington Nationals"),
    ("39", "Ian Happ", "Chicago Cubs"),
    ("40", "Chase Meidroth", "Chicago White Sox"),
    ("41", "Walker Buehler", "Philadelphia Phillies"),
    ("42", "Frank Thomas", "Chicago White Sox"),
    ("43", "Noelvi Marte", "Cincinnati Reds"),
    ("44", "Ceddanne Rafaela", "Boston Red Sox"),
    ("45", "River Ryan", "Los Angeles Dodgers"),
    ("46", "Shota Imanaga", "Chicago Cubs"),
    ("47", "Chipper Jones", "Atlanta Braves"),
    ("48", "Thomas Saggese", "St. Louis Cardinals"),
    ("49", "Edgar Quero", "Chicago White Sox"),
    ("50", "Elly De La Cruz", "Cincinnati Reds"),
    ("51", "Denzel Clarke", "Athletics"),
    ("52", "Steven Kwan", "Cleveland Guardians"),
    ("53", "Chris Sale", "Atlanta Braves"),
    ("54", "Corbin Carroll", "Arizona Diamondbacks"),
    ("55", "Corbin Burnes", "Arizona Diamondbacks"),
    ("56", "Rhett Lowder", "Cincinnati Reds"),
    ("57", "Coby Mayo", "Baltimore Orioles"),
    ("58", "Alejandro Osuna", "Texas Rangers"),
    ("59", "Jordan Lawlar", "Arizona Diamondbacks"),
    ("60", "Jordan Westburg", "Baltimore Orioles"),
    ("61", "Bo Jackson", "Chicago White Sox"),
    ("62", "Luis Robert Jr.", "Chicago White Sox"),
    ("63", "Nico Hoerner", "Chicago Cubs"),
    ("64", "Jacob Wilson", "Athletics"),
    ("65", "Kevin Alcántara", "Chicago Cubs"),
    ("66", "Colton Cowser", "Baltimore Orioles"),
    ("67", "Manny Ramirez", "Boston Red Sox"),
    ("68", "Chase Dollander", "Colorado Rockies"),
    ("69", "Daylen Lile", "Washington Nationals"),
    ("70", "Ketel Marte", "Arizona Diamondbacks"),
    ("71", "Austin Riley", "Atlanta Braves"),
    ("72", "Ernie Banks", "Chicago Cubs"),
    ("73", "Ryan Bliss", "Seattle Mariners"),
    ("74", "Jackson Holliday", "Baltimore Orioles"),
    ("75", "Hunter Greene", "Cincinnati Reds"),
    ("76", "Orelvis Martinez", "Toronto Blue Jays"),
    ("77", "Cedric Mullins", "New York Mets"),
    ("78", "Nick Yorke", "Pittsburgh Pirates"),
    ("79", "Rafael Devers", "San Francisco Giants"),
    ("80", "Jace Jung", "Detroit Tigers"),
    ("81", "Kristian Campbell", "Boston Red Sox"),
    ("82", "Tomoyuki Sugano", "Baltimore Orioles"),
    ("83", "Michael Harris II", "Atlanta Braves"),
    ("84", "Dansby Swanson", "Chicago Cubs"),
    ("85", "Ronald Acuña Jr.", "Atlanta Braves"),
    ("86", "Hyeseong Kim", "Los Angeles Dodgers"),
    ("87", "Carlton Fisk", "Chicago White Sox"),
    ("88", "José Ramírez", "Cleveland Guardians"),
    ("89", "Marcell Ozuna", "Atlanta Braves"),
    ("90", "Connor Norby", "Miami Marlins"),
    ("91", "David Ortiz", "Boston Red Sox"),
    ("92", "Mason Miller", "San Diego Padres"),
    ("93", "Dalton Rushing", "Los Angeles Dodgers"),
    ("94", "Nick Kurtz", "Athletics"),
    ("95", "Brent Rooker", "Athletics"),
    ("96", "Jhonkensy Noel", "Cleveland Guardians"),
    ("97", "Matt Olson", "Atlanta Braves"),
    ("98", "Brooks Baldwin", "Chicago White Sox"),
    ("99", "Lawrence Butler", "Athletics"),
    ("100", "Roki Sasaki", "Los Angeles Dodgers"),
    ("101", "Colt Keith", "Detroit Tigers"),
    ("102", "Edwin Díaz", "New York Mets"),
    ("103", "Marcelo Mayer", "Boston Red Sox"),
    ("104", "Hanley Ramirez", "Florida Marlins"),
    ("105", "Alex Bregman", "Boston Red Sox"),
    ("106", "Bryce Harper", "Philadelphia Phillies"),
    ("107", "Cade Horton", "Chicago Cubs"),
    ("108", "Aaron Schunk", "Colorado Rockies"),
    ("109", "Giancarlo Stanton", "New York Yankees"),
    ("110", "Reggie Jackson", "California Angels"),
    ("111", "Victor Mesa Jr.", "Miami Marlins"),
    ("112", "J.T. Realmuto", "Philadelphia Phillies"),
    ("113", "Larry Walker", "Colorado Rockies"),
    ("114", "Jorbit Vivas", "New York Yankees"),
    ("115", "Pete Alonso", "New York Mets"),
    ("116", "Jeremy Peña", "Houston Astros"),
    ("117", "Salvador Perez", "Kansas City Royals"),
    ("118", "Mike Trout", "Los Angeles Angels"),
    ("119", "Caleb Durbin", "Milwaukee Brewers"),
    ("120", "Cody Bellinger", "New York Yankees"),
    ("121", "Dillon Dingler", "Detroit Tigers"),
    ("122", "Agustín Ramírez", "Miami Marlins"),
    ("123", "Christian Yelich", "Milwaukee Brewers"),
    ("124", "Zack Wheeler", "Philadelphia Phillies"),
    ("125", "Logan Evans", "Seattle Mariners"),
    ("126", "Mike Schmidt", "Philadelphia Phillies"),
    ("127", "Mike Piazza", "New York Mets"),
    ("128", "Brandon Nimmo", "New York Mets"),
    ("129", "Framber Valdez", "Houston Astros"),
    ("130", "Trea Turner", "Philadelphia Phillies"),
    ("131", "Ezequiel Tovar", "Colorado Rockies"),
    ("132", "Cole Ragans", "Kansas City Royals"),
    ("133", "Mookie Betts", "Los Angeles Dodgers"),
    ("134", "William Contreras", "Milwaukee Brewers"),
    ("135", "Roberto Clemente", "Pittsburgh Pirates"),
    ("136", "Jackson Chourio", "Milwaukee Brewers"),
    ("137", "Spencer Torkelson", "Detroit Tigers"),
    ("138", "Vladimir Guerrero", "California Angels"),
    ("139", "Jonathan India", "Kansas City Royals"),
    ("140", "Ben Williamson", "Seattle Mariners"),
    ("141", "Sandy Koufax", "Los Angeles Dodgers"),
    ("142", "Jose Altuve", "Houston Astros"),
    ("143", "Tim Raines", "Montréal Expos"),
    ("144", "Kyle Schwarber", "Philadelphia Phillies"),
    ("145", "Kerry Carpenter", "Detroit Tigers"),
    ("146", "Yordan Alvarez", "Houston Astros"),
    ("147", "Torii Hunter", "Minnesota Twins"),
    ("148", "Jeff Bagwell", "Houston Astros"),
    ("149", "Jasson Domínguez", "New York Yankees"),
    ("150", "Sam Aldegheri", "Los Angeles Angels"),
    ("151", "Francisco Lindor", "New York Mets"),
    ("152", "Niko Kavadas", "Los Angeles Angels"),
    ("153", "Moisés Ballesteros", "Chicago Cubs"),
    ("154", "Mick Abel", "Minnesota Twins"),
    ("155", "Roger Clemens", "Houston Astros"),
    ("156", "Tommy Edman", "Los Angeles Dodgers"),
    ("157", "Paul Skenes", "Pittsburgh Pirates"),
    ("158", "George Brett", "Kansas City Royals"),
    ("159", "Max Fried", "New York Yankees"),
    ("160", "Shohei Ohtani", "Los Angeles Dodgers"),
    ("161", "Bobby Witt Jr.", "Kansas City Royals"),
    ("162", "Tom Seaver", "New York Mets"),
    ("163", "Isaac Paredes", "Houston Astros"),
    ("164", "Gary Carter", "Montréal Expos"),
    ("165", "Griffin Conine", "Miami Marlins"),
    ("166", "Vinnie Pasquantino", "Kansas City Royals"),
    ("167", "Nolan Schanuel", "Los Angeles Angels"),
    ("168", "Luke Keaschall", "Minnesota Twins"),
    ("169", "Will Warren", "New York Yankees"),
    ("170", "Tarik Skubal", "Detroit Tigers"),
    ("171", "Aaron Judge", "New York Yankees"),
    ("172", "Brenton Doyle", "Colorado Rockies"),
    ("173", "Kirby Puckett", "Minnesota Twins"),
    ("174", "Mark Vientos", "New York Mets"),
    ("175", "Carlos Correa", "Houston Astros"),
    ("176", "Yoshinobu Yamamoto", "Los Angeles Dodgers"),
    ("177", "Riley Greene", "Detroit Tigers"),
    ("178", "Byron Buxton", "Minnesota Twins"),
    ("179", "Zac Veen", "Colorado Rockies"),
    ("180", "Blake Snell", "Los Angeles Dodgers"),
    ("181", "Kris Bryant", "Colorado Rockies"),
    ("182", "Royce Lewis", "Minnesota Twins"),
    ("183", "Sandy Alcantara", "Miami Marlins"),
    ("184", "Christian Walker", "Houston Astros"),
    ("185", "Clayton Kershaw", "Los Angeles Dodgers"),
    ("186", "Gleyber Torres", "Detroit Tigers"),
    ("187", "Teoscar Hernández", "Los Angeles Dodgers"),
    ("188", "Alec Bohm", "Philadelphia Phillies"),
    ("189", "Derek Jeter", "New York Yankees"),
    ("190", "Paul Goldschmidt", "New York Yankees"),
    ("191", "Ryan McMahon", "New York Yankees"),
    ("192", "Freddie Freeman", "Los Angeles Dodgers"),
    ("193", "Drew Romo", "Colorado Rockies"),
    ("194", "Freddy Peralta", "Milwaukee Brewers"),
    ("195", "Jimmy Rollins", "Philadelphia Phillies"),
    ("196", "Francisco Alvarez", "New York Mets"),
    ("197", "Sal Frelick", "Milwaukee Brewers"),
    ("198", "Zach Neto", "Los Angeles Angels"),
    ("199", "Jazz Chisholm Jr.", "New York Yankees"),
    ("200", "Juan Soto", "New York Mets"),
    ("201", "Bryan Reynolds", "Pittsburgh Pirates"),
    ("202", "Marcus Semien", "Texas Rangers"),
    ("203", "Jackson Merrill", "San Diego Padres"),
    ("204", "Andrew McCutchen", "Pittsburgh Pirates"),
    ("205", "Julio Rodríguez", "Seattle Mariners"),
    ("206", "Sonny Gray", "St. Louis Cardinals"),
    ("207", "Fernando Tatis Jr.", "San Diego Padres"),
    ("208", "CJ Abrams", "Washington Nationals"),
    ("209", "Xander Bogaerts", "San Diego Padres"),
    ("210", "Vladimir Guerrero Jr.", "Toronto Blue Jays"),
    ("211", "Leo Jiménez", "Toronto Blue Jays"),
    ("212", "Tony Gwynn", "San Diego Padres"),
    ("213", "Yu Darvish", "San Diego Padres"),
    ("214", "Alan Roden", "Minnesota Twins"),
    ("215", "Kameron Misner", "Tampa Bay Rays"),
    ("216", "Manny Machado", "San Diego Padres"),
    ("217", "Albert Pujols", "St. Louis Cardinals"),
    ("218", "Willy Adames", "San Francisco Giants"),
    ("219", "Cam Smith", "Houston Astros"),
    ("220", "Drake Baldwin", "Atlanta Braves"),
    ("221", "Logan Henderson", "Milwaukee Brewers"),
    ("222", "Wyatt Langford", "Texas Rangers"),
    ("223", "Luis Arraez", "San Diego Padres"),
    ("224", "George Springer", "Toronto Blue Jays"),
    ("225", "Chandler Simpson", "Tampa Bay Rays"),
    ("226", "Masyn Winn", "St. Louis Cardinals"),
    ("227", "Matt Shaw", "Chicago Cubs"),
    ("228", "Michael King", "San Diego Padres"),
    ("229", "Evan Carter", "Texas Rangers"),
    ("230", "Luis Castillo", "Seattle Mariners"),
    ("231", "Adolis García", "Texas Rangers"),
    ("232", "Justin Verlander", "San Francisco Giants"),
    ("233", "Junior Caminero", "Tampa Bay Rays"),
    ("234", "Cal Raleigh", "Seattle Mariners"),
    ("235", "Logan Gilbert", "Seattle Mariners"),
    ("236", "Matt Chapman", "San Francisco Giants"),
    ("237", "Jacob deGrom", "Texas Rangers"),
    ("238", "Grant McCray", "San Francisco Giants"),
    ("239", "Randy Arozarena", "Seattle Mariners"),
    ("240", "Oneil Cruz", "Pittsburgh Pirates"),
    ("241", "Corey Seager", "Texas Rangers"),
    ("242", "Jung Hoo Lee", "San Francisco Giants"),
    ("243", "Willie Mays", "San Francisco Giants"),
    ("244", "Robert Hassell III", "Washington Nationals"),
    ("245", "Braxton Ashcraft", "Pittsburgh Pirates"),
    ("246", "Evan Longoria", "Tampa Bay Rays"),
    ("247", "Josh Jung", "Texas Rangers"),
    ("248", "Nolan Arenado", "St. Louis Cardinals"),
    ("249", "Ken Griffey Jr.", "Seattle Mariners"),
    ("250", "Bo Bichette", "Toronto Blue Jays"),
    # Image Variations (251-300)
    ("251", "Darren Baker", "Washington Nationals"),
    ("252", "Marcus Semien", "Texas Rangers"),
    ("253", "Corey Seager", "Texas Rangers"),
    ("254", "Ryan McMahon", "Colorado Rockies"),
    ("255", "Jordan Westburg", "Baltimore Orioles"),
    ("256", "Alec Bohm", "Philadelphia Phillies"),
    ("257", "Ketel Marte", "Arizona Diamondbacks"),
    ("258", "Anthony Santander", "Baltimore Orioles"),
    ("259", "CJ Abrams", "Washington Nationals"),
    ("260", "Yordan Alvarez", "Houston Astros"),
    ("261", "Jarren Duran", "Boston Red Sox"),
    ("262", "Will Smith", "Los Angeles Dodgers"),
    ("263", "Isaac Paredes", "Tampa Bay Rays"),
    ("264", "José Ramírez", "Cleveland Guardians"),
    ("265", "Marcell Ozuna", "Atlanta Braves"),
    ("266", "Jurickson Profar", "San Diego Padres"),
    ("267", "Elly De La Cruz", "Cincinnati Reds"),
    ("268", "Trea Turner", "Philadelphia Phillies"),
    ("269", "Hunter Greene", "Cincinnati Reds"),
    ("270", "Seth Lugo", "Kansas City Royals"),
    ("271", "Garrett Crochet", "Chicago White Sox"),
    ("272", "Vladimir Guerrero Jr.", "Toronto Blue Jays"),
    ("273", "Riley Greene", "Detroit Tigers"),
    ("274", "Max Fried", "Atlanta Braves"),
    ("275", "Logan Webb", "San Francisco Giants"),
    ("276", "Freddie Freeman", "Los Angeles Dodgers"),
    ("277", "Tanner Scott", "Miami Marlins"),
    ("278", "Shota Imanaga", "Chicago Cubs"),
    ("279", "Juan Soto", "New York Yankees"),
    ("280", "Gunnar Henderson", "Baltimore Orioles"),
    ("281", "Shohei Ohtani", "Los Angeles Dodgers"),
    ("282", "Steven Kwan", "Cleveland Guardians"),
    ("283", "Cole Ragans", "Kansas City Royals"),
    ("284", "Salvador Perez", "Kansas City Royals"),
    ("285", "Paul Skenes", "Pittsburgh Pirates"),
    ("286", "Pete Alonso", "New York Mets"),
    ("287", "William Contreras", "Milwaukee Brewers"),
    ("288", "Corbin Burnes", "Baltimore Orioles"),
    ("289", "Christian Yelich", "Milwaukee Brewers"),
    ("290", "Teoscar Hernández", "Los Angeles Dodgers"),
    ("291", "Adley Rutschman", "Baltimore Orioles"),
    ("292", "Jackson Merrill", "San Diego Padres"),
    ("293", "Tarik Skubal", "Detroit Tigers"),
    ("294", "Josh Naylor", "Cleveland Guardians"),
    ("295", "Bobby Witt Jr.", "Kansas City Royals"),
    ("296", "Willi Castro", "Minnesota Twins"),
    ("297", "Mason Miller", "Athletics"),
    ("298", "Bryce Harper", "Philadelphia Phillies"),
    ("299", "Bryan Reynolds", "Pittsburgh Pirates"),
    ("300", "Aaron Judge", "New York Yankees"),
])
print("  Base Set: 300 cards")

# ════════════════════════════════════════════════════════════════════════════════
# AUTOGRAPH INSERT SETS
# ════════════════════════════════════════════════════════════════════════════════

# ────────────────────────────────────────────────────────────────────────────────
# Pristine Autographs (96 cards)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Pristine Autographs", PRISTINE_AUTO_PARALLELS, [
    ("PA-AA", "Adael Amador", "Colorado Rockies"),
    ("PA-AD", "Adrian Del Castillo", "Arizona Diamondbacks"),
    ("PA-AG", "Alex Gordon", "Kansas City Royals"),
    ("PA-AJ", "Andruw Jones", "Atlanta Braves"),
    ("PA-AM", "Adam Mazur", "Miami Marlins"),
    ("PA-AMA", "Angel Martínez", "Cleveland Guardians"),
    ("PA-AMAR", "Austin Martin", "Minnesota Twins"),
    ("PA-AR", "Aramis Ramirez", "Chicago Cubs"),
    ("PA-AW", "Austin Wells", "New York Yankees"),
    ("PA-BB", "Brooks Baldwin", "Chicago White Sox"),
    ("PA-BBR", "Ben Brown", "Chicago Cubs"),
    ("PA-BD", "Brenton Doyle", "Colorado Rockies"),
    ("PA-BL", "Brooks Lee", "Minnesota Twins"),
    ("PA-BM", "Bobby Miller", "Los Angeles Dodgers"),
    ("PA-BR", "Ben Rice", "New York Yankees"),
    ("PA-BS", "Bryson Stott", "Philadelphia Phillies"),
    ("PA-BT", "Brice Turang", "Milwaukee Brewers"),
    ("PA-CAM", "Cam Smith", "Houston Astros"),
    ("PA-CD", "Caden Dana", "Los Angeles Angels"),
    ("PA-CMA", "Coby Mayo", "Baltimore Orioles"),
    ("PA-CN", "Carlos Narvaez", "New York Yankees"),
    ("PA-CNO", "Connor Norby", "Miami Marlins"),
    ("PA-CP", "Cade Povich", "Baltimore Orioles"),
    ("PA-CR", "Carlos Rodriguez", "Milwaukee Brewers"),
    ("PA-CS", "Christian Scott", "New York Mets"),
    ("PA-DB", "Darren Baker", "Washington Nationals"),
    ("PA-DF", "David Festa", "Minnesota Twins"),
    ("PA-DH", "Dustin Harris", "Texas Rangers"),
    ("PA-DHE", "DJ Herz", "Washington Nationals"),
    ("PA-DL", "Derrek Lee", "Chicago Cubs"),
    ("PA-DT", "Drew Thorpe", "Chicago White Sox"),
    ("PA-EM", "Edgar Martinez", "Seattle Mariners"),
    ("PA-GG", "Gordon Graceffo", "St. Louis Cardinals"),
    ("PA-GM", "Grant McCray", "San Francisco Giants"),
    ("PA-GR", "Grayson Rodriguez", "Baltimore Orioles"),
    ("PA-HB", "Hayden Birdsong", "San Francisco Giants"),
    ("PA-HK", "Heston Kjerstad", "Baltimore Orioles"),
    ("PA-HR", "Hanley Ramirez", "Florida Marlins"),
    ("PA-HSK", "Hyeseong Kim", "Los Angeles Dodgers"),
    ("PA-HW", "Hurston Waldrep", "Atlanta Braves"),
    ("PA-JC", "Joe Carter", "Toronto Blue Jays"),
    ("PA-JCA", "Junior Caminero", "Tampa Bay Rays"),
    ("PA-JD", "Jhoan Duran", "Minnesota Twins"),
    ("PA-JDO", "Jasson Domínguez", "New York Yankees"),
    ("PA-JDU", "Jarren Duran", "Boston Red Sox"),
    ("PA-JE", "Jim Edmonds", "Los Angeles Angels"),
    ("PA-JJO", "Jared Jones", "Pittsburgh Pirates"),
    ("PA-JJU", "Jace Jung", "Detroit Tigers"),
    ("PA-JL", "Jack Leiter", "Texas Rangers"),
    ("PA-JLA", "Jordan Lawlar", "Arizona Diamondbacks"),
    ("PA-JM", "Justyn-Henry Malloy", "Detroit Tigers"),
    ("PA-JN", "Jhonkensy Noel", "Cleveland Guardians"),
    ("PA-JO", "Joey Ortiz", "Milwaukee Brewers"),
    ("PA-JW", "Justin Wrobleski", "Los Angeles Dodgers"),
    ("PA-JWI", "Jacob Wilson", "Athletics"),
    ("PA-JWO", "James Wood", "Washington Nationals"),
    ("PA-KA", "Kevin Alcántara", "Chicago Cubs"),
    ("PA-KC", "Kristian Campbell", "Boston Red Sox"),
    ("PA-KM", "Keider Montero", "Detroit Tigers"),
    ("PA-KR", "Kumar Rocker", "Texas Rangers"),
    ("PA-LA", "Luisangel Acuña", "New York Mets"),
    ("PA-LB", "Lawrence Butler", "Athletics"),
    ("PA-LJ", "Leo Jiménez", "Toronto Blue Jays"),
    ("PA-MM", "Marcelo Mayer", "Boston Red Sox"),
    ("PA-MS", "Matt Shaw", "Chicago Cubs"),
    ("PA-MV", "Mark Vientos", "New York Mets"),
    ("PA-MY", "Michael Young", "Texas Rangers"),
    ("PA-NA", "Nacho Alvarez Jr.", "Atlanta Braves"),
    ("PA-NK", "Niko Kavadas", "Los Angeles Angels"),
    ("PA-NKU", "Nick Kurtz", "Athletics"),
    ("PA-NY", "Nick Yorke", "Pittsburgh Pirates"),
    ("PA-OM", "Orelvis Martinez", "Toronto Blue Jays"),
    ("PA-OS", "Ozzie Smith", "St. Louis Cardinals"),
    ("PA-PO", "Paul O'Neill", "New York Yankees"),
    ("PA-RB", "Ryan Bliss", "Seattle Mariners"),
    ("PA-RF", "Rafael Furcal", "Los Angeles Dodgers"),
    ("PA-RH", "Ryan Howard", "Philadelphia Phillies"),
    ("PA-RHI", "Rece Hinds", "Cincinnati Reds"),
    ("PA-RL", "Rhett Lowder", "Cincinnati Reds"),
    ("PA-RR", "River Ryan", "Los Angeles Dodgers"),
    ("PA-RS", "Roki Sasaki", "Los Angeles Dodgers"),
    ("PA-SF", "Sal Frelick", "Milwaukee Brewers"),
    ("PA-SG", "Sonny Gray", "St. Louis Cardinals"),
    ("PA-SK", "Steven Kwan", "Cleveland Guardians"),
    ("PA-SL", "Seth Lugo", "Kansas City Royals"),
    ("PA-SM", "Sean Murphy", "Atlanta Braves"),
    ("PA-SS", "Spencer Schwellenbach", "Atlanta Braves"),
    ("PA-TB", "Tyler Black", "Milwaukee Brewers"),
    ("PA-TL", "Tyler Locklear", "Seattle Mariners"),
    ("PA-TP", "Tony Pérez", "Cincinnati Reds"),
    ("PA-TS", "Thomas Saggese", "St. Louis Cardinals"),
    ("PA-TSW", "Trey Sweeney", "Detroit Tigers"),
    ("PA-WS", "Will Smith", "Los Angeles Dodgers"),
    ("PA-WW", "Will Wagner", "Toronto Blue Jays"),
    ("PA-ZD", "Zach Dezenzo", "Houston Astros"),
    ("PA-ZM", "Zebby Matthews", "Minnesota Twins"),
])
print("  Pristine Autographs: 96 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Pristine Pair Autographs (6 cards — co_players)
# ────────────────────────────────────────────────────────────────────────────────

is_id = create_insert_set(set_id, "Pristine Pair Autographs")
for par_name, par_pr in PRISTINE_PAIRS_PARALLELS:
    create_parallel(is_id, par_name, par_pr)
add_multi_cards(is_id, [
    ("PPDA-AP", [("Mark McGwire", "St. Louis Cardinals"), ("Albert Pujols", "St. Louis Cardinals")]),
    ("PPDA-AW", [("Anthony Volpe", "New York Yankees"), ("Austin Wells", "New York Yankees")]),
    ("PPDA-ED", [("Elly De La Cruz", "Cincinnati Reds"), ("Bobby Witt Jr.", "Kansas City Royals")]),
    ("PPDA-GH", [("Jackson Holliday", "Baltimore Orioles"), ("Gunnar Henderson", "Baltimore Orioles")]),
    ("PPDA-JW", [("Dylan Crews", "Washington Nationals"), ("James Wood", "Washington Nationals")]),
    ("PPDA-RA", [("Chipper Jones", "Atlanta Braves"), ("Ronald Acuña Jr.", "Atlanta Braves")]),
])
print("  Pristine Pair Autographs: 6 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Plated and Polished Autographs (20 cards)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Plated and Polished Autographs", PLATED_AUTO_PARALLELS, [
    ("PAPAV-BB", "Byron Buxton", "Minnesota Twins"),
    ("PAPAV-BR", "Bryan Reynolds", "Pittsburgh Pirates"),
    ("PAPAV-BW", "Bobby Witt Jr.", "Kansas City Royals"),
    ("PAPAV-CC", "Colton Cowser", "Baltimore Orioles"),
    ("PAPAV-CS", "Corey Seager", "Texas Rangers"),
    ("PAPAV-CY", "Christian Yelich", "Milwaukee Brewers"),
    ("PAPAV-FT", "Fernando Tatis Jr.", "San Diego Padres"),
    ("PAPAV-GH", "Gunnar Henderson", "Baltimore Orioles"),
    ("PAPAV-JA", "Jose Altuve", "Houston Astros"),
    ("PAPAV-JR", "José Ramírez", "Cleveland Guardians"),
    ("PAPAV-JS", "Juan Soto", "New York Mets"),
    ("PAPAV-LA", "Luis Arraez", "San Diego Padres"),
    ("PAPAV-MO", "Marcell Ozuna", "Atlanta Braves"),
    ("PAPAV-PA", "Pete Alonso", "New York Mets"),
    ("PAPAV-RA", "Ronald Acuña Jr.", "Atlanta Braves"),
    ("PAPAV-RD", "Rafael Devers", "Boston Red Sox"),
    ("PAPAV-SO", "Shohei Ohtani", "Los Angeles Dodgers"),
    ("PAPAV-VG", "Vladimir Guerrero Jr.", "Toronto Blue Jays"),
    ("PAPAV-WL", "Wyatt Langford", "Texas Rangers"),
    ("PAPAV-YA", "Yordan Alvarez", "Houston Astros"),
])
print("  Plated and Polished Autographs: 20 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Personal Endorsements Autographs (32 cards)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Personal Endorsements Autographs", PERSONAL_ENDORSEMENTS_PARALLELS, [
    ("PPEA-AB", "Alex Bregman", "Houston Astros"),
    ("PPEA-ABE", "Adrian Beltré", "Texas Rangers"),
    ("PPEA-AP", "Albert Pujols", "St. Louis Cardinals"),
    ("PPEA-BL", "Brooks Lee", "Minnesota Twins"),
    ("PPEA-BP", "Buster Posey", "San Francisco Giants"),
    ("PPEA-CB", "Corbin Burnes", "Baltimore Orioles"),
    ("PPEA-CM", "Coby Mayo", "Baltimore Orioles"),
    ("PPEA-CR", "Cal Ripken Jr.", "Baltimore Orioles"),
    ("PPEA-DC", "Dylan Crews", "Washington Nationals"),
    ("PPEA-DM", "Don Mattingly", "New York Yankees"),
    ("PPEA-DO", "David Ortiz", "Boston Red Sox"),
    ("PPEA-DP", "Dustin Pedroia", "Boston Red Sox"),
    ("PPEA-GH", "Gunnar Henderson", "Baltimore Orioles"),
    ("PPEA-I", "Ichiro", "Seattle Mariners"),
    ("PPEA-IR", "Ivan Rodriguez", "Texas Rangers"),
    ("PPEA-JH", "Jackson Holliday", "Baltimore Orioles"),
    ("PPEA-JJU", "Jace Jung", "Detroit Tigers"),
    ("PPEA-JR", "Julio Rodríguez", "Seattle Mariners"),
    ("PPEA-JW", "Jacob Wilson", "Athletics"),
    ("PPEA-KA", "Kevin Alcántara", "Chicago Cubs"),
    ("PPEA-LA", "Luisangel Acuña", "New York Mets"),
    ("PPEA-MM", "Manny Machado", "San Diego Padres"),
    ("PPEA-OA", "Ozzie Albies", "Atlanta Braves"),
    ("PPEA-RJ", "Randy Johnson", "Arizona Diamondbacks"),
    ("PPEA-RL", "Rhett Lowder", "Cincinnati Reds"),
    ("PPEA-SI", "Shota Imanaga", "Chicago Cubs"),
    ("PPEA-SS", "Sammy Sosa", "Chicago Cubs"),
    ("PPEA-TT", "Trea Turner", "Philadelphia Phillies"),
    ("PPEA-VG", "Vladimir Guerrero", "California Angels"),
    ("PPEA-VM", "Victor Martinez", "Detroit Tigers"),
    ("PPEA-WC", "William Contreras", "Milwaukee Brewers"),
    ("PPEA-WL", "Wyatt Langford", "Texas Rangers"),
])
print("  Personal Endorsements Autographs: 32 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Italics Autographs (15 cards)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Italics Autographs", ITALICS_PARALLELS, [
    ("I-AP", "Albert Pujols", "St. Louis Cardinals"),
    ("I-AR", "Adley Rutschman", "Baltimore Orioles"),
    ("I-BW", "Bobby Witt Jr.", "Kansas City Royals"),
    ("I-CC", "Corbin Carroll", "Arizona Diamondbacks"),
    ("I-CP", "Chan Ho Park", "Los Angeles Dodgers"),
    ("I-DJ", "Derek Jeter", "New York Yankees"),
    ("I-EC", "Evan Carter", "Texas Rangers"),
    ("I-ED", "Elly De La Cruz", "Cincinnati Reds"),
    ("I-MT", "Mike Trout", "Los Angeles Angels"),
    ("I-PS", "Paul Skenes", "Pittsburgh Pirates"),
    ("I-RA", "Ronald Acuña Jr.", "Atlanta Braves"),
    ("I-SI", "Shota Imanaga", "Chicago Cubs"),
    ("I-VG", "Vladimir Guerrero Jr.", "Toronto Blue Jays"),
    ("I-YM", "Yadier Molina", "St. Louis Cardinals"),
    ("I-YY", "Yoshinobu Yamamoto", "Los Angeles Dodgers"),
])
print("  Italics Autographs: 15 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Popular Demand Autograph Relics (35 cards)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Popular Demand Autograph Relics", POPULAR_DEMAND_PARALLELS, [
    ("PPDAR-AB", "Adrian Beltré", "Texas Rangers"),
    ("PPDAR-AJ", "Aaron Judge", "New York Yankees"),
    ("PPDAR-AP", "Albert Pujols", "St. Louis Cardinals"),
    ("PPDAR-AR", "Adley Rutschman", "Baltimore Orioles"),
    ("PPDAR-ARO", "Alex Rodriguez", "Seattle Mariners"),
    ("PPDAR-BL", "Brooks Lee", "Minnesota Twins"),
    ("PPDAR-BP", "Buster Posey", "San Francisco Giants"),
    ("PPDAR-BW", "Bobby Witt Jr.", "Kansas City Royals"),
    ("PPDAR-CJ", "Chipper Jones", "Atlanta Braves"),
    ("PPDAR-CK", "Clayton Kershaw", "Los Angeles Dodgers"),
    ("PPDAR-CR", "Cal Ripken Jr.", "Baltimore Orioles"),
    ("PPDAR-CS", "Corey Seager", "Texas Rangers"),
    ("PPDAR-DC", "Dylan Crews", "Washington Nationals"),
    ("PPDAR-FH", "Félix Hernández", "Seattle Mariners"),
    ("PPDAR-GH", "Gunnar Henderson", "Baltimore Orioles"),
    ("PPDAR-I", "Ichiro", "Seattle Mariners"),
    ("PPDAR-IR", "Ivan Rodriguez", "Texas Rangers"),
    ("PPDAR-JA", "Jose Altuve", "Houston Astros"),
    ("PPDAR-JD", "Jasson Domínguez", "New York Yankees"),
    ("PPDAR-JH", "Jackson Holliday", "Baltimore Orioles"),
    ("PPDAR-JM", "Jackson Merrill", "San Diego Padres"),
    ("PPDAR-JR", "Julio Rodríguez", "Seattle Mariners"),
    ("PPDAR-JRO", "Jimmy Rollins", "Philadelphia Phillies"),
    ("PPDAR-JS", "Juan Soto", "New York Mets"),
    ("PPDAR-JW", "James Wood", "Washington Nationals"),
    ("PPDAR-KT", "Kyle Tucker", "Houston Astros"),
    ("PPDAR-MP", "Mike Piazza", "New York Mets"),
    ("PPDAR-MR", "Mariano Rivera", "New York Yankees"),
    ("PPDAR-PS", "Paul Skenes", "Pittsburgh Pirates"),
    ("PPDAR-RA", "Ronald Acuña Jr.", "Atlanta Braves"),
    ("PPDAR-RJ", "Randy Johnson", "New York Yankees"),
    ("PPDAR-SS", "Sammy Sosa", "Chicago Cubs"),
    ("PPDAR-TT", "Trea Turner", "Philadelphia Phillies"),
    ("PPDAR-VG", "Vladimir Guerrero", "California Angels"),
    ("PPDAR-WL", "Wyatt Langford", "Texas Rangers"),
])
print("  Popular Demand Autograph Relics: 35 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Pristine Pieces Autograph Relic (58 cards)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Pristine Pieces Autograph Relic", PRISTINE_PIECES_PARALLELS, [
    ("PPAR-AA", "Adael Amador", "Colorado Rockies"),
    ("PPAR-AB", "Alex Bregman", "Houston Astros"),
    ("PPAR-AP", "Andy Pettitte", "New York Yankees"),
    ("PPAR-AR", "Austin Riley", "Atlanta Braves"),
    ("PPAR-AV", "Anthony Volpe", "New York Yankees"),
    ("PPAR-AW", "Austin Wells", "New York Yankees"),
    ("PPAR-BB", "Byron Buxton", "Minnesota Twins"),
    ("PPAR-BC", "Bartolo Colon", "New York Mets"),
    ("PPAR-BN", "Brandon Nimmo", "New York Mets"),
    ("PPAR-BR", "Ben Rice", "New York Yankees"),
    ("PPAR-BRE", "Bryan Reynolds", "Pittsburgh Pirates"),
    ("PPAR-BRO", "Brent Rooker", "Athletics"),
    ("PPAR-CA", "CJ Abrams", "Washington Nationals"),
    ("PPAR-CB", "Corbin Burnes", "Baltimore Orioles"),
    ("PPAR-CC", "Colton Cowser", "Baltimore Orioles"),
    ("PPAR-CCA", "Corbin Carroll", "Arizona Diamondbacks"),
    ("PPAR-CM", "Cedric Mullins", "Baltimore Orioles"),
    ("PPAR-CP", "Cade Povich", "Baltimore Orioles"),
    ("PPAR-CR", "Ceddanne Rafaela", "Boston Red Sox"),
    ("PPAR-DJ", "David Justice", "Atlanta Braves"),
    ("PPAR-DS", "Dansby Swanson", "Chicago Cubs"),
    ("PPAR-DW", "Dontrelle Willis", "Florida Marlins"),
    ("PPAR-FL", "Francisco Lindor", "New York Mets"),
    ("PPAR-GS", "Gary Sheffield", "Atlanta Braves"),
    ("PPAR-IH", "Ian Happ", "Chicago Cubs"),
    ("PPAR-JC", "Jackson Chourio", "Milwaukee Brewers"),
    ("PPAR-JCA", "Junior Caminero", "Tampa Bay Rays"),
    ("PPAR-JCH", "Jazz Chisholm Jr.", "New York Yankees"),
    ("PPAR-JJ", "Josh Jung", "Texas Rangers"),
    ("PPAR-JR", "J.T. Realmuto", "Philadelphia Phillies"),
    ("PPAR-JRO", "Julio Rodríguez", "Seattle Mariners"),
    ("PPAR-JS", "John Smoltz", "Atlanta Braves"),
    ("PPAR-JV", "Joey Votto", "Cincinnati Reds"),
    ("PPAR-JW", "Jordan Westburg", "Baltimore Orioles"),
    ("PPAR-LB", "Lawrence Butler", "Athletics"),
    ("PPAR-LG", "Luis Gil", "New York Yankees"),
    ("PPAR-LW", "Larry Walker", "Colorado Rockies"),
    ("PPAR-MH", "Michael Harris II", "Atlanta Braves"),
    ("PPAR-MMA", "Manny Machado", "San Diego Padres"),
    ("PPAR-MO", "Matt Olson", "Atlanta Braves"),
    ("PPAR-MY", "Masataka Yoshida", "Boston Red Sox"),
    ("PPAR-NA", "Nolan Arenado", "St. Louis Cardinals"),
    ("PPAR-NM", "Noelvi Marte", "Cincinnati Reds"),
    ("PPAR-PC", "Pete Crow-Armstrong", "Chicago Cubs"),
    ("PPAR-PF", "Prince Fielder", "Detroit Tigers"),
    ("PPAR-PG", "Paul Goldschmidt", "St. Louis Cardinals"),
    ("PPAR-RC", "Rod Carew", "California Angels"),
    ("PPAR-RL", "Royce Lewis", "Minnesota Twins"),
    ("PPAR-SF", "Sal Frelick", "Milwaukee Brewers"),
    ("PPAR-SK", "Steven Kwan", "Cleveland Guardians"),
    ("PPAR-SR", "Scott Rolen", "Cincinnati Reds"),
    ("PPAR-SS", "Spencer Steer", "Cincinnati Reds"),
    ("PPAR-TH", "Torii Hunter", "Minnesota Twins"),
    ("PPAR-TS", "Tarik Skubal", "Detroit Tigers"),
    ("PPAR-TSS", "Ted Simmons", "St. Louis Cardinals"),
    ("PPAR-WC", "Will Clark", "San Francisco Giants"),
    ("PPAR-WS", "Will Smith", "Los Angeles Dodgers"),
    ("PPAR-ZG", "Zack Gelof", "Athletics"),
])
print("  Pristine Pieces Autograph Relic: 58 cards")

# ────────────────────────────────────────────────────────────────────────────────
# All-Star Game Pristine Pieces Autograph Relic (27 cards — all /1)
# ────────────────────────────────────────────────────────────────────────────────

ASGPP_PARALLELS = [
    ("Base /1", 1),
]

make_insert_set("All-Star Game Pristine Pieces Autograph Relic", ASGPP_PARALLELS, [
    ("ASGPP-AB", "Alec Bohm", "Philadelphia Phillies"),
    ("ASGPP-AJ", "Aaron Judge", "New York Yankees"),
    ("ASGPP-BH", "Bryce Harper", "Philadelphia Phillies"),
    ("ASGPP-BR", "Bryan Reynolds", "Pittsburgh Pirates"),
    ("ASGPP-CA", "CJ Abrams", "Washington Nationals"),
    ("ASGPP-CB", "Corbin Burnes", "Baltimore Orioles"),
    ("ASGPP-CSE", "Corey Seager", "Texas Rangers"),
    ("ASGPP-CY", "Christian Yelich", "Milwaukee Brewers"),
    ("ASGPP-GC", "Garrett Crochet", "Chicago White Sox"),
    ("ASGPP-GH", "Gunnar Henderson", "Baltimore Orioles"),
    ("ASGPP-JD", "Jarren Duran", "Boston Red Sox"),
    ("ASGPP-JM", "Jackson Merrill", "San Diego Padres"),
    ("ASGPP-JS", "Juan Soto", "New York Yankees"),
    ("ASGPP-LA", "Luis Arraez", "San Diego Padres"),
    ("ASGPP-MF", "Max Fried", "Atlanta Braves"),
    ("ASGPP-MM", "Mason Miller", "Athletics"),
    ("ASGPP-MO", "Marcell Ozuna", "Atlanta Braves"),
    ("ASGPP-MSE", "Marcus Semien", "Texas Rangers"),
    ("ASGPP-PA", "Pete Alonso", "New York Mets"),
    ("ASGPP-PS", "Paul Skenes", "Pittsburgh Pirates"),
    ("ASGPP-RG", "Riley Greene", "Detroit Tigers"),
    ("ASGPP-SI", "Shota Imanaga", "Chicago Cubs"),
    ("ASGPP-SK", "Steven Kwan", "Cleveland Guardians"),
    ("ASGPP-TS", "Tarik Skubal", "Detroit Tigers"),
    ("ASGPP-VG", "Vladimir Guerrero Jr.", "Toronto Blue Jays"),
    ("ASGPP-WC", "William Contreras", "Milwaukee Brewers"),
    ("ASGPP-YA", "Yordan Alvarez", "Houston Astros"),
])
print("  All-Star Game Pristine Pieces Autograph Relic: 27 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Rookie Jumbo Autograph Relic (19 cards — base /25)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Rookie Jumbo Autograph Relic", ROOKIE_JUMBO_PARALLELS, [
    ("RJAR-BL", "Brooks Lee", "Minnesota Twins"),
    ("RJAR-BR", "Ben Rice", "New York Yankees"),
    ("RJAR-CMA", "Coby Mayo", "Baltimore Orioles"),
    ("RJAR-CN", "Connor Norby", "Miami Marlins"),
    ("RJAR-DC", "Dylan Crews", "Washington Nationals"),
    ("RJAR-DT", "Drew Thorpe", "Chicago White Sox"),
    ("RJAR-GM", "Grant McCray", "San Francisco Giants"),
    ("RJAR-JJ", "Jackson Jobe", "Detroit Tigers"),
    ("RJAR-JJU", "Jace Jung", "Detroit Tigers"),
    ("RJAR-JW", "Jacob Wilson", "Athletics"),
    ("RJAR-JWO", "James Wood", "Washington Nationals"),
    ("RJAR-KA", "Kevin Alcántara", "Chicago Cubs"),
    ("RJAR-KR", "Kumar Rocker", "Texas Rangers"),
    ("RJAR-LA", "Luisangel Acuña", "New York Mets"),
    ("RJAR-NA", "Nacho Alvarez Jr.", "Atlanta Braves"),
    ("RJAR-RH", "Rece Hinds", "Cincinnati Reds"),
    ("RJAR-RL", "Rhett Lowder", "Cincinnati Reds"),
    ("RJAR-RR", "River Ryan", "Los Angeles Dodgers"),
    ("RJAR-SS", "Spencer Schwellenbach", "Atlanta Braves"),
])
print("  Rookie Jumbo Autograph Relic: 19 cards")

# ════════════════════════════════════════════════════════════════════════════════
# INSERT SETS
# ════════════════════════════════════════════════════════════════════════════════

# ────────────────────────────────────────────────────────────────────────────────
# Perseverance (25 cards)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Perseverance", PERSEVERANCE_PARALLELS, [
    ("P-1", "Nolan Ryan", "Texas Rangers"),
    ("P-2", "Rickey Henderson", "Oakland Athletics"),
    ("P-3", "Roger Clemens", "Boston Red Sox"),
    ("P-4", "CC Sabathia", "New York Yankees"),
    ("P-5", "Ty Cobb", "Detroit Tigers"),
    ("P-6", "Willie Mays", "San Francisco Giants"),
    ("P-7", "Hank Aaron", "Atlanta Braves"),
    ("P-8", "Randy Johnson", "Arizona Diamondbacks"),
    ("P-9", "Derek Jeter", "New York Yankees"),
    ("P-10", "Ken Griffey Jr.", "Seattle Mariners"),
    ("P-11", "Cal Ripken Jr.", "Baltimore Orioles"),
    ("P-12", "Albert Pujols", "St. Louis Cardinals"),
    ("P-13", "Ichiro", "Seattle Mariners"),
    ("P-14", "Alex Rodriguez", "New York Yankees"),
    ("P-15", "Babe Ruth", "New York Yankees"),
    ("P-16", "Mike Trout", "Los Angeles Angels"),
    ("P-17", "Adrian Beltré", "Texas Rangers"),
    ("P-18", "Andrew McCutchen", "Pittsburgh Pirates"),
    ("P-19", "Freddie Freeman", "Los Angeles Dodgers"),
    ("P-20", "Giancarlo Stanton", "New York Yankees"),
    ("P-21", "Jose Altuve", "Houston Astros"),
    ("P-22", "Paul Goldschmidt", "New York Yankees"),
    ("P-23", "Bryce Harper", "Philadelphia Phillies"),
    ("P-24", "Manny Machado", "San Diego Padres"),
    ("P-25", "Salvador Perez", "Kansas City Royals"),
])
print("  Perseverance: 25 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Plated & Polished (40 cards)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Plated & Polished", PLATED_INSERT_PARALLELS, [
    ("PP-1", "Dylan Crews", "Washington Nationals"),
    ("PP-2", "Bobby Witt Jr.", "Kansas City Royals"),
    ("PP-3", "Gunnar Henderson", "Baltimore Orioles"),
    ("PP-4", "Elly De La Cruz", "Cincinnati Reds"),
    ("PP-5", "Coby Mayo", "Baltimore Orioles"),
    ("PP-6", "Cam Smith", "Houston Astros"),
    ("PP-7", "Edgar Quero", "Chicago White Sox"),
    ("PP-8", "Juan Soto", "New York Mets"),
    ("PP-9", "José Ramírez", "Cleveland Guardians"),
    ("PP-10", "Corey Seager", "Texas Rangers"),
    ("PP-11", "Yordan Alvarez", "Houston Astros"),
    ("PP-12", "Kristian Campbell", "Boston Red Sox"),
    ("PP-13", "Rafael Devers", "San Francisco Giants"),
    ("PP-14", "Vladimir Guerrero Jr.", "Toronto Blue Jays"),
    ("PP-15", "Francisco Lindor", "New York Mets"),
    ("PP-16", "Ronald Acuña Jr.", "Atlanta Braves"),
    ("PP-17", "Aaron Judge", "New York Yankees"),
    ("PP-18", "Jace Jung", "Detroit Tigers"),
    ("PP-19", "Jackson Merrill", "San Diego Padres"),
    ("PP-20", "Marcelo Mayer", "Boston Red Sox"),
    ("PP-21", "Fernando Tatis Jr.", "San Diego Padres"),
    ("PP-22", "Shohei Ohtani", "Los Angeles Dodgers"),
    ("PP-23", "Jackson Chourio", "Milwaukee Brewers"),
    ("PP-24", "Wyatt Langford", "Texas Rangers"),
    ("PP-25", "Jacob Wilson", "Athletics"),
    ("PP-26", "Mookie Betts", "Los Angeles Dodgers"),
    ("PP-27", "Brooks Lee", "Minnesota Twins"),
    ("PP-28", "Kevin Alcántara", "Chicago Cubs"),
    ("PP-29", "Luisangel Acuña", "New York Mets"),
    ("PP-30", "Dalton Rushing", "Los Angeles Dodgers"),
    ("PP-31", "Mike Trout", "Los Angeles Angels"),
    ("PP-32", "Bryce Harper", "Philadelphia Phillies"),
    ("PP-33", "Kyle Tucker", "Chicago Cubs"),
    ("PP-34", "Jackson Holliday", "Baltimore Orioles"),
    ("PP-35", "Trea Turner", "Philadelphia Phillies"),
    ("PP-36", "Cody Bellinger", "New York Yankees"),
    ("PP-37", "Corbin Carroll", "Arizona Diamondbacks"),
    ("PP-38", "Jung Hoo Lee", "San Francisco Giants"),
    ("PP-39", "Junior Caminero", "Tampa Bay Rays"),
    ("PP-40", "James Wood", "Washington Nationals"),
])
print("  Plated & Polished: 40 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Precisionaries (35 cards)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Precisionaries", PRECISIONARIES_PARALLELS, [
    ("PR-1", "Paul Skenes", "Pittsburgh Pirates"),
    ("PR-2", "Kristian Campbell", "Boston Red Sox"),
    ("PR-3", "Max Fried", "New York Yankees"),
    ("PR-4", "Manny Machado", "San Diego Padres"),
    ("PR-5", "Juan Soto", "New York Mets"),
    ("PR-6", "James Wood", "Washington Nationals"),
    ("PR-7", "Bobby Witt Jr.", "Kansas City Royals"),
    ("PR-8", "Shohei Ohtani", "Los Angeles Dodgers"),
    ("PR-9", "Rafael Devers", "San Francisco Giants"),
    ("PR-10", "Fernando Tatis Jr.", "San Diego Padres"),
    ("PR-11", "Dylan Crews", "Washington Nationals"),
    ("PR-12", "Garrett Crochet", "Boston Red Sox"),
    ("PR-13", "Clayton Kershaw", "Los Angeles Dodgers"),
    ("PR-14", "Francisco Lindor", "New York Mets"),
    ("PR-15", "Ketel Marte", "Arizona Diamondbacks"),
    ("PR-16", "Aaron Judge", "New York Yankees"),
    ("PR-17", "Gunnar Henderson", "Baltimore Orioles"),
    ("PR-18", "Kyle Schwarber", "Philadelphia Phillies"),
    ("PR-19", "Jackson Merrill", "San Diego Padres"),
    ("PR-20", "Tarik Skubal", "Detroit Tigers"),
    ("PR-21", "Cade Horton", "Chicago Cubs"),
    ("PR-22", "Trea Turner", "Philadelphia Phillies"),
    ("PR-23", "Pete Alonso", "New York Mets"),
    ("PR-24", "Ronald Acuña Jr.", "Atlanta Braves"),
    ("PR-25", "Jackson Chourio", "Milwaukee Brewers"),
    ("PR-26", "Shota Imanaga", "Chicago Cubs"),
    ("PR-27", "Chase Dollander", "Colorado Rockies"),
    ("PR-28", "Jackson Jobe", "Detroit Tigers"),
    ("PR-29", "Rhett Lowder", "Cincinnati Reds"),
    ("PR-30", "Yordan Alvarez", "Houston Astros"),
    ("PR-31", "Julio Rodríguez", "Seattle Mariners"),
    ("PR-32", "Jace Jung", "Detroit Tigers"),
    ("PR-33", "José Ramírez", "Cleveland Guardians"),
    ("PR-34", "Freddie Freeman", "Los Angeles Dodgers"),
    ("PR-35", "Elly De La Cruz", "Cincinnati Reds"),
])
print("  Precisionaries: 35 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Pearlescent (25 cards)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Pearlescent", SUPERFRACTOR_ONLY, [
    ("PE-1", "Yoshinobu Yamamoto", "Los Angeles Dodgers"),
    ("PE-2", "Kyle Tucker", "Chicago Cubs"),
    ("PE-3", "James Wood", "Washington Nationals"),
    ("PE-4", "Dylan Crews", "Washington Nationals"),
    ("PE-5", "Jackson Jobe", "Detroit Tigers"),
    ("PE-6", "Rhett Lowder", "Cincinnati Reds"),
    ("PE-7", "Roki Sasaki", "Los Angeles Dodgers"),
    ("PE-8", "Brooks Lee", "Minnesota Twins"),
    ("PE-9", "Coby Mayo", "Baltimore Orioles"),
    ("PE-10", "Aaron Judge", "New York Yankees"),
    ("PE-11", "Juan Soto", "New York Mets"),
    ("PE-12", "Shohei Ohtani", "Los Angeles Dodgers"),
    ("PE-13", "Mike Trout", "Los Angeles Angels"),
    ("PE-14", "Bryce Harper", "Philadelphia Phillies"),
    ("PE-15", "Matt Shaw", "Chicago Cubs"),
    ("PE-16", "Corbin Burnes", "Arizona Diamondbacks"),
    ("PE-17", "Jacob Wilson", "Athletics"),
    ("PE-18", "Ronald Acuña Jr.", "Atlanta Braves"),
    ("PE-19", "Francisco Lindor", "New York Mets"),
    ("PE-20", "Julio Rodríguez", "Seattle Mariners"),
    ("PE-21", "Kristian Campbell", "Boston Red Sox"),
    ("PE-22", "Cam Smith", "Houston Astros"),
    ("PE-23", "Bobby Witt Jr.", "Kansas City Royals"),
    ("PE-24", "Gunnar Henderson", "Baltimore Orioles"),
    ("PE-25", "Manny Machado", "San Diego Padres"),
])
print("  Pearlescent: 25 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Amped (25 cards)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Amped", SUPERFRACTOR_ONLY, [
    ("A-1", "Vladimir Guerrero Jr.", "Toronto Blue Jays"),
    ("A-2", "Mookie Betts", "Los Angeles Dodgers"),
    ("A-3", "Freddie Freeman", "Los Angeles Dodgers"),
    ("A-4", "Julio Rodríguez", "Seattle Mariners"),
    ("A-5", "Jacob Wilson", "Athletics"),
    ("A-6", "Cade Horton", "Chicago Cubs"),
    ("A-7", "Luisangel Acuña", "New York Mets"),
    ("A-8", "Cam Smith", "Houston Astros"),
    ("A-9", "Elly De La Cruz", "Cincinnati Reds"),
    ("A-10", "Roki Sasaki", "Los Angeles Dodgers"),
    ("A-11", "Bobby Witt Jr.", "Kansas City Royals"),
    ("A-12", "Gunnar Henderson", "Baltimore Orioles"),
    ("A-13", "Jackson Holliday", "Baltimore Orioles"),
    ("A-14", "Matt Shaw", "Chicago Cubs"),
    ("A-15", "James Wood", "Washington Nationals"),
    ("A-16", "Dylan Crews", "Washington Nationals"),
    ("A-17", "Paul Skenes", "Pittsburgh Pirates"),
    ("A-18", "Marcelo Mayer", "Boston Red Sox"),
    ("A-19", "Kyle Tucker", "Chicago Cubs"),
    ("A-20", "Wyatt Langford", "Texas Rangers"),
    ("A-21", "Nick Kurtz", "Athletics"),
    ("A-22", "Fernando Tatis Jr.", "San Diego Padres"),
    ("A-23", "Jackson Chourio", "Milwaukee Brewers"),
    ("A-24", "Cody Bellinger", "New York Yankees"),
    ("A-25", "Coby Mayo", "Baltimore Orioles"),
])
print("  Amped: 25 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Prowlers (15 cards)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Prowlers", PROWLERS_PARALLELS, [
    ("PRW-1", "Rickey Henderson", "Oakland Athletics"),
    ("PRW-2", "Elly De La Cruz", "Cincinnati Reds"),
    ("PRW-3", "Corbin Carroll", "Arizona Diamondbacks"),
    ("PRW-4", "Bobby Witt Jr.", "Kansas City Royals"),
    ("PRW-5", "Gunnar Henderson", "Baltimore Orioles"),
    ("PRW-6", "Shohei Ohtani", "Los Angeles Dodgers"),
    ("PRW-7", "Pete Crow-Armstrong", "Chicago Cubs"),
    ("PRW-8", "José Ramírez", "Cleveland Guardians"),
    ("PRW-9", "Jazz Chisholm Jr.", "New York Yankees"),
    ("PRW-10", "Francisco Lindor", "New York Mets"),
    ("PRW-11", "Kristian Campbell", "Boston Red Sox"),
    ("PRW-12", "James Wood", "Washington Nationals"),
    ("PRW-13", "Jackson Chourio", "Milwaukee Brewers"),
    ("PRW-14", "Ichiro", "Seattle Mariners"),
    ("PRW-15", "Wyatt Langford", "Texas Rangers"),
])
print("  Prowlers: 15 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Monogram (30 cards)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Monogram", MONOGRAM_PARALLELS, [
    ("M-1", "Corbin Carroll", "Arizona Diamondbacks"),
    ("M-2", "Jacob Wilson", "Athletics"),
    ("M-3", "Ronald Acuña Jr.", "Atlanta Braves"),
    ("M-4", "Gunnar Henderson", "Baltimore Orioles"),
    ("M-5", "Edgar Quero", "Chicago White Sox"),
    ("M-6", "Marcelo Mayer", "Boston Red Sox"),
    ("M-7", "Matt Shaw", "Chicago Cubs"),
    ("M-8", "Elly De La Cruz", "Cincinnati Reds"),
    ("M-9", "José Ramírez", "Cleveland Guardians"),
    ("M-10", "Chase Dollander", "Colorado Rockies"),
    ("M-11", "Jace Jung", "Detroit Tigers"),
    ("M-12", "Jose Altuve", "Houston Astros"),
    ("M-13", "Bobby Witt Jr.", "Kansas City Royals"),
    ("M-14", "Mike Trout", "Los Angeles Angels"),
    ("M-15", "Mookie Betts", "Los Angeles Dodgers"),
    ("M-16", "Connor Norby", "Miami Marlins"),
    ("M-17", "Jackson Chourio", "Milwaukee Brewers"),
    ("M-18", "Brooks Lee", "Minnesota Twins"),
    ("M-19", "Juan Soto", "New York Mets"),
    ("M-20", "Aaron Judge", "New York Yankees"),
    ("M-21", "Bryce Harper", "Philadelphia Phillies"),
    ("M-22", "Paul Skenes", "Pittsburgh Pirates"),
    ("M-23", "Fernando Tatis Jr.", "San Diego Padres"),
    ("M-24", "Willy Adames", "San Francisco Giants"),
    ("M-25", "Julio Rodríguez", "Seattle Mariners"),
    ("M-26", "Masyn Winn", "St. Louis Cardinals"),
    ("M-27", "Dalton Rushing", "Los Angeles Dodgers"),
    ("M-28", "Cam Smith", "Houston Astros"),
    ("M-29", "Vladimir Guerrero Jr.", "Toronto Blue Jays"),
    ("M-30", "Dylan Crews", "Washington Nationals"),
])
print("  Monogram: 30 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Let's Go (5 cards)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Let's Go", LETS_GO_PARALLELS, [
    ("LGC-6", "Aaron Judge", "New York Yankees"),
    ("LGC-7", "Elly De La Cruz", "Cincinnati Reds"),
    ("LGC-8", "James Wood", "Washington Nationals"),
    ("LGC-9", "Jackson Chourio", "Milwaukee Brewers"),
    ("LGC-10", "Vladimir Guerrero Jr.", "Toronto Blue Jays"),
])
print("  Let's Go: 5 cards")

# ────────────────────────────────────────────────────────────────────────────────
# COMPUTE PLAYER STATS
# ────────────────────────────────────────────────────────────────────────────────

print("\nComputing player stats...")

cur.execute("SELECT id FROM players WHERE set_id = ?", (set_id,))
player_ids = [r[0] for r in cur.fetchall()]

for pid in player_ids:
    cur.execute(
        """SELECT pa.id, pa.insert_set_id
           FROM player_appearances pa
           WHERE pa.player_id = ?""",
        (pid,),
    )
    appearances = cur.fetchall()

    insert_set_ids = set(a[1] for a in appearances)
    insert_set_count = len(insert_set_ids)

    unique_cards = 0
    total_print_run = 0
    one_of_ones = 0

    for app_id, is_id in appearances:
        unique_cards += 1

        cur.execute(
            "SELECT name, print_run FROM parallels WHERE insert_set_id = ?",
            (is_id,),
        )
        pars = cur.fetchall()
        for par_name, pr in pars:
            unique_cards += 1
            if pr is not None:
                total_print_run += pr
                if pr == 1:
                    one_of_ones += 1

    cur.execute(
        "UPDATE players SET unique_cards = ?, total_print_run = ?, one_of_ones = ?, insert_set_count = ? WHERE id = ?",
        (unique_cards, total_print_run, one_of_ones, insert_set_count, pid),
    )

conn.commit()

# ────────────────────────────────────────────────────────────────────────────────
# VERIFY
# ────────────────────────────────────────────────────────────────────────────────

cur.execute("SELECT COUNT(*) FROM players WHERE set_id = ?", (set_id,))
total_players = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id = ?", (set_id,))
total_insert_sets = cur.fetchone()[0]

cur.execute(
    """SELECT COUNT(*) FROM player_appearances pa
       INNER JOIN players p ON p.id = pa.player_id
       WHERE p.set_id = ?""",
    (set_id,),
)
total_appearances = cur.fetchone()[0]

cur.execute(
    """SELECT COUNT(*) FROM appearance_co_players ac
       INNER JOIN player_appearances pa ON pa.id = ac.appearance_id
       INNER JOIN players p ON p.id = pa.player_id
       WHERE p.set_id = ?""",
    (set_id,),
)
total_co_players = cur.fetchone()[0]

cur.execute(
    """SELECT COUNT(*) FROM parallels par
       INNER JOIN insert_sets i ON i.id = par.insert_set_id
       WHERE i.set_id = ?""",
    (set_id,),
)
total_parallels = cur.fetchone()[0]

print(f"\n{'='*50}")
print(f"Set ID:            {set_id}")
print(f"Players:           {total_players}")
print(f"Insert Sets:       {total_insert_sets}")
print(f"Appearances:       {total_appearances}")
print(f"Co-player links:   {total_co_players}")
print(f"Parallel types:    {total_parallels}")
print(f"{'='*50}")

conn.close()
print("\nDone!")
