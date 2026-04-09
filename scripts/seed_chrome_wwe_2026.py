"""
Seed script: 2026 Topps Chrome WWE
Inserts all data into the local SQLite database (the-c-list.db).
Usage: python3 scripts/seed_chrome_wwe_2026.py
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


# ─── Rookies ──────────────────────────────────────────────────────────────────

ROOKIES = {
    "Talla Tonga", "Lainey Reid", "Tyra Mae Steele", "Saquon Shugars",
    "Cutler James", "Osiris Griffin", "Joe Hendry",
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


def add_gpk_cards(insert_set_id, cards):
    """Add GPK cards. cards = [(card_number, gpk_name, athlete_name, team), ...]
    GPK character name stored as card name via subset_tag, athlete as player."""
    for card_number, gpk_name, athlete_name, team in cards:
        is_rookie = athlete_name in ROOKIES
        player_id = get_or_create_player(set_id, athlete_name)
        cur.execute(
            "INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team, subset_tag) VALUES (?, ?, ?, ?, ?, ?)",
            (player_id, insert_set_id, card_number, int(is_rookie), team, gpk_name),
        )


def make_insert_set(name, parallels_def, cards, is_multi=False, is_gpk=False):
    is_id = create_insert_set(set_id, name)
    for par_name, par_pr in parallels_def:
        create_parallel(is_id, par_name, par_pr)
    if is_gpk:
        add_gpk_cards(is_id, cards)
    elif is_multi:
        add_multi_cards(is_id, cards)
    else:
        add_cards(is_id, cards)
    return is_id


def make_single_wrestler_set(name, parallels_def, count, prefix, wrestler_name, team):
    """For sets where every card features the same wrestler (Austin 3:16, etc.)"""
    is_id = create_insert_set(set_id, name)
    for par_name, par_pr in parallels_def:
        create_parallel(is_id, par_name, par_pr)
    is_rookie = wrestler_name in ROOKIES
    player_id = get_or_create_player(set_id, wrestler_name)
    for i in range(1, count + 1):
        create_appearance(player_id, is_id, f"{prefix}-{i}", is_rookie, team)
    return is_id


# ─── 1. Create the set ─────────────────────────────────────────────────────────

SET_NAME = "2026 Topps Chrome WWE"

cur.execute("SELECT id FROM sets WHERE name = ?", (SET_NAME,))
existing = cur.fetchone()
if existing:
    print(f"Set '{SET_NAME}' already exists with id {existing[0]}. Aborting.")
    conn.close()
    exit(1)

box_config = {
    "hobby": {
        "cards_per_pack": 8,
        "packs_per_box": 12,
        "boxes_per_case": 12,
        "autos_per_box": 2,
        "notes": "2 Autographs, 12 Refractors, 12 Inserts, 4 Numbered Parallels per box",
    },
    "first_day_issue": {
        "cards_per_pack": 8,
        "packs_per_box": 12,
        "boxes_per_case": 12,
        "autos_per_box": 2,
        "notes": "2 Total Autographs (including 1 FDI-Exclusive Auto), 2 FDI-Exclusive Parallels per box",
    },
    "value": {
        "cards_per_pack": 4,
        "packs_per_box": 7,
        "boxes_per_case": 40,
        "notes": "3 Diamond Plate Refractors, 1 Base Refractor, 7 Inserts per box",
    },
    "mega": {
        "cards_per_pack": 8,
        "packs_per_box": 6,
        "boxes_per_case": 20,
        "notes": "10 X-Fractors, 1 Numbered Parallel, 6 Inserts per box",
    },
    "breakers_delight": {
        "cards_per_pack": 12,
        "packs_per_box": 1,
        "boxes_per_case": 6,
    },
}

cur.execute(
    "INSERT INTO sets (name, sport, season, league, tier, box_config, release_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
    (SET_NAME, "Wrestling", "2026", "WWE", "Chrome", json.dumps(box_config), "2026-04-10"),
)
set_id = cur.lastrowid
print(f"Created set '{SET_NAME}' with id {set_id}")

# ─── 2. Parallel definitions ─────────────────────────────────────────────────

BASE_PARALLELS = [
    ("Refractor", None),
    ("Diamond Plate Refractor", None),       # Value Exclusive
    ("Geometric", None),                      # Breaker Exclusive
    ("Negative Refractor", None),             # Hobby Exclusive
    ("Prism Refractor", None),                # Hobby Exclusive
    ("Sonar Refractor", None),                # Hobby Exclusive
    ("Steel Cage Refractor", None),           # Hobby Exclusive
    ("X-Fractor", None),                      # Mega Exclusive
    ("Magenta Refractor", 399),
    ("Teal Refractor", 299),
    ("Yellow Refractor", 275),
    ("Pink Refractor", 250),
    ("Pink Mini Diamond Refractor", 250),     # Mega Exclusive
    ("Aqua Refractor", 199),
    ("Blue Refractor", 150),
    ("Blue Geometric", 150),                  # Breaker Exclusive
    ("Blue Mini Diamond Refractor", 150),     # Mega Exclusive
    ("Blue RayWave Refractor", 150),          # Value Exclusive
    ("Green Refractor", 99),
    ("Green Mini Diamond Refractor", 99),     # Mega Exclusive
    ("Green RayWave Refractor", 99),          # Value Exclusive
    ("Purple Refractor", 75),
    ("Purple Mini Diamond Refractor", 75),    # Mega Exclusive
    ("Purple RayWave Refractor", 75),         # Value Exclusive
    ("Gold Refractor", 50),
    ("Gold Geometric", 50),                   # Breaker Exclusive
    ("Gold Mini Diamond Refractor", 50),      # Mega Exclusive
    ("Gold RayWave Refractor", 50),           # Value Exclusive
    ("Orange Refractor", 25),
    ("Orange Geometric", 25),                 # Breaker Exclusive
    ("Orange Mini Diamond Refractor", 25),    # Mega Exclusive
    ("Orange RayWave Refractor", 25),         # Value Exclusive
    ("FDI Refractor", 12),
    ("Black Refractor", 10),
    ("Black Mini Diamond Refractor", 10),     # Mega Exclusive
    ("Black RayWave Refractor", 10),          # Value Exclusive
    ("Purple Geometric", 10),                 # Breaker Exclusive
    ("Red Refractor", 5),
    ("Red Geometric", 5),                     # Breaker Exclusive
    ("Red Mini Diamond Refractor", 5),        # Mega Exclusive
    ("Red RayWave Refractor", 5),             # Value Exclusive
    ("FrozenFractor", 5),                     # Hobby Exclusive
    ("Black Geometric", 2),                   # Breaker Exclusive
    ("Superfractor", 1),
]

# Alternate Personas and Iconic Imprints: Superfractor /1 only
SUPERFRACTOR_ONLY = [
    ("Superfractor", 1),
]

# Chrome Autographs parallels
CHROME_AUTO_PARALLELS = [
    ("Geometric Refractor", None),  # Breaker
    ("Blue", 150),
    ("Gold", 50),
    ("Gold Geometric", 50),         # Breaker
    ("Orange", 25),
    ("Orange Geometric", 25),       # Breaker
    ("FDI", 12),
    ("Black", 10),
    ("Purple Geometric", 10),       # Breaker
    ("Red", 5),
    ("Red Geometric", 5),           # Breaker
    ("Black Geometric", 2),         # Breaker
    ("Superfractor", 1),
]

# Red/Blue/NXT Brand Autographs parallels
BRAND_AUTO_PARALLELS = [
    ("Refractor", None),
    ("Geometric", None),            # Breaker
    ("Blue", 150),
    ("Gold", 50),
    ("Gold Geometric", 50),         # Breaker
    ("Orange", 25),
    ("Orange Geometric", 25),       # Breaker
    ("Black", 10),
    ("Purple Geometric", 10),       # Breaker
    ("Red", 5),
    ("Red Geometric", 5),           # Breaker
    ("Black Geometric", 2),         # Breaker
    ("Superfractor", 1),
]

# Marks of Champions, Legendary Chrome, Main Event, 1986 Topps, HOF, Future Stars parallels
PREMIUM_AUTO_PARALLELS = [
    ("Gold", 50),
    ("Gold Geometric", 50),         # Breaker
    ("Orange", 25),
    ("Orange Geometric", 25),       # Breaker
    ("Black", 10),
    ("Purple Geometric", 10),       # Breaker
    ("Red", 5),
    ("Red Geometric", 5),           # Breaker
    ("Black Geometric", 2),         # Breaker
    ("Superfractor", 1),
]

# Iconic Imprint Autos, Alternate Personas Autos, Dual Autos, etc. (Hobby /10)
HOBBY_10_PARALLELS = [
    ("Red", 5),
    ("Superfractor", 1),
]

# Scope, Viral Shock, Women's Division parallels
SCOPE_PARALLELS = [
    ("Refractor", None),
    ("Geometric", None),            # Breaker
    ("Blue", 150),
    ("Blue Geometric", 150),        # Breaker
    ("Green", 99),
    ("Gold", 50),
    ("Gold Geometric", 50),         # Breaker
    ("Orange", 25),
    ("Orange Geometric", 25),       # Breaker
    ("Black", 10),
    ("Purple Geometric", 10),       # Breaker
    ("Red", 5),
    ("Black Geometric", 2),         # Breaker
    ("Superfractor", 1),
]

# Austin 3:16, Rock Diamond Legacy, Platinum Punk, Family Tree, Embedded parallels
HOBBY_INSERT_PARALLELS = [
    ("Gold", 50),
    ("Black", 10),
    ("Red", 5),
    ("Superfractor", 1),
]

# Wrestlemania Recall, Eras of Excellence, Focus Reel parallels (Retail)
RETAIL_INSERT_PARALLELS = [
    ("Refractor", None),
    ("Aqua", 199),
    ("Blue", 150),
    ("Green", 99),
    ("Gold", 50),
    ("Orange", 25),
    ("Black", 10),
    ("Red", 5),
    ("Superfractor", 1),
]

# GPK parallels
GPK_PARALLELS = [
    ("Black", 10),
    ("Red", 5),
    ("Superfractor", 1),
]

# Buyback parallels
BUYBACK_PARALLELS = [
    ("X-Fractors", 300),
    ("Prism Refractors", 250),
    ("Sepia Refractors", 175),
    ("Refractors", 150),
    ("Pink Shimmer Refractors", 125),
    ("Neon Green & Black Refractors", 99),
    ("Red & Blue Refractors", 75),
    ("Purple Refractors", 50),
]

# Helix parallels
HELIX_PARALLELS = [
    ("Superfractor", 1),  # Hobby/Breaker Exclusive
]

# ─── 3. Insert sets + cards ───────────────────────────────────────────────────

# ────────────────────────────────────────────────────────────────────────────────
# BASE CARDS I (100 cards)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Base Cards I", BASE_PARALLELS, [
    ("1", "The Rock", "Legend"),
    ("2", "John Cena", "Legend"),
    ("3", "Undertaker", "Legend"),
    ("4", "Triple H", "Legend"),
    ("5", "Finn Bálor", "Raw"),
    ("6", "Kane", "Legend"),
    ("7", "Stone Cold Steve Austin", "Legend"),
    ("8", "Gunther", "Raw"),
    ("9", "JD McDonagh", "Raw"),
    ("10", "JBL", "Legend"),
    ("11", "Becky Lynch", "Raw"),
    ("12", "Ludwig Kaiser", "Raw"),
    ("13", "Uncle Howdy", "Smackdown"),
    ("14", "Ron Killings", "Smackdown"),
    ("15", "Johnny Gargano", "Smackdown"),
    ("16", "Tonga Loa", "Smackdown"),
    ("17", "Liv Morgan", "Raw"),
    ("18", "Roman Reigns", "Smackdown"),
    ("19", "Bayley", "Raw"),
    ("20", "Rhea Ripley", "Raw"),
    ("21", "The American Nightmare Cody Rhodes", "Smackdown"),
    ("22", "Billy Gunn", "Legend"),
    ("23", "Road Dogg Jesse James", "Legend"),
    ("24", "Kevin Nash", "Legend"),
    ("25", "Hulk Hogan", "Legend"),
    ("26", "Tony D'Angelo", "NXT"),
    ("27", "Asuka", "Raw"),
    ("28", "Aleister Black", "Smackdown"),
    ("29", "Tiffany Stratton", "Smackdown"),
    ("30", "Bret Hit Man Hart", "Legend"),
    ("31", "Jimmy Uso", "Smackdown"),
    ("32", "Michin", "Smackdown"),
    ("33", "Bianca Belair", "Smackdown"),
    ("34", "Sol Ruca", "NXT"),
    ("35", "Iyo Sky", "Raw"),
    ("36", "Shinsuke Nakamura", "Smackdown"),
    ("37", "Nia Jax", "Smackdown"),
    ("38", "Izzi Dame", "NXT"),
    ("39", "Nikkita Lyons", "NXT"),
    ("40", "Seth Rollins", "Raw"),
    ("41", "Penta", "Raw"),
    ("42", "X-Pac", "Legend"),
    ("43", "Damian Priest", "Smackdown"),
    ("44", "Paul Heyman", "Smackdown"),
    ("45", "Jade Cargill", "Smackdown"),
    ("46", "Shawn Spears", "NXT"),
    ("47", "AJ Styles", "Raw"),
    ("48", "The Miz", "Smackdown"),
    ("49", "CM Punk", "Raw"),
    ("50", "Rusev", "Raw"),
    ("51", "Kevin Owens", "Smackdown"),
    ("52", "Trick Williams", "NXT"),
    ("53", "Bronson Reed", "Raw"),
    ("54", "Karmen Petrovic", "NXT"),
    ("55", "Jacob Fatu", "Smackdown"),
    ("56", "Jordynne Grace", "NXT"),
    ("57", "Maxxine Dupri", "Raw"),
    ("58", "Chad Gable", "Raw"),
    ("59", "Shawn Michaels", "Legend"),
    ("60", "Zoey Stark", "Raw"),
    ("61", "Lita", "Legend"),
    ("62", "Pete Dunne", "Raw"),
    ("63", "Solo Sikoa", "Smackdown"),
    ("64", "Alexa Bliss", "Smackdown"),
    ("65", "Roxanne Perez", "Raw"),
    ("66", "Torrie Wilson", "Legend"),
    ("67", "Sami Zayn", "Smackdown"),
    ("68", "Lyra Valkyria", "Raw"),
    ("69", "Sheamus", "Raw"),
    ("70", "Carmelo Hayes", "Smackdown"),
    ("71", "Booker T", "Legend"),
    ("72", "Randy Orton", "Smackdown"),
    ("73", "Dominik Mysterio", "Raw"),
    ("74", "Stephanie Vaquer", "Raw"),
    ("75", "Otis", "Raw"),
    ("76", "Bray Wyatt", "Legend"),
    ("77", "Austin Theory", "Raw"),
    ("78", "Kit Wilson", "Smackdown"),
    ("79", "Rey Fenix", "Smackdown"),
    ("80", "Chelsea Green", "Smackdown"),
    ("81", "Elton Prince", "Smackdown"),
    ("82", "Kiana James", "Smackdown"),
    ("83", "Jey Uso", "Raw"),
    ("84", "Raquel Rodriguez", "Raw"),
    ("85", "Chyna", "Legend"),
    ("86", "Tommaso Ciampa", "Smackdown"),
    ("87", "LA Knight", "Raw"),
    ("88", "Akira Tozawa", "Raw"),
    ("89", "Charlotte Flair", "Smackdown"),
    ("90", "Candice LeRae", "Smackdown"),
    ("91", "Tyler Breeze", "Legend"),
    ("92", "Rikishi", "Legend"),
    ("93", "Bron Breakker", "Raw"),
    ("94", "Ricky Saints", "NXT"),
    ("95", "Kelani Jordan", "NXT"),
    ("96", "Drew McIntyre", "Smackdown"),
    ("97", "Rey Mysterio", "Raw"),
    ("98", "Lola Vice", "NXT"),
    ("99", "Batista", "Legend"),
    ("100", "JC Mateo", "Smackdown"),
])
print("  Base Cards I: 100 cards")

# ────────────────────────────────────────────────────────────────────────────────
# BASE CARDS II (100 cards)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Base Cards II", BASE_PARALLELS, [
    ("101", "Lash Legend", "NXT"),
    ("102", "Junkyard Dog", "Legend"),
    ("103", "Bronco Nima", "NXT"),
    ("104", "Brooks Jensen", "NXT"),
    ("105", "AJ Lee", "Raw"),
    ("106", "Earthquake", "Legend"),
    ("107", "Lucien Price", "NXT"),
    ("108", "Angelo Dawkins", "Smackdown"),
    ("109", "Talla Tonga", "Smackdown"),
    ("110", "New Jack", "Legend"),
    ("111", "Ivar", "Raw"),
    ("112", "Tyler Bate", "Raw"),
    ("113", "Koko B. Ware", "Legend"),
    ("114", "Victoria", "Legend"),
    ("115", "Trish Stratus", "Legend"),
    ("116", "Lexis King", "NXT"),
    ("117", "Lainey Reid", "NXT"),
    ("118", "Arianna Grace", "NXT"),
    ("119", "Typhoon", "Legend"),
    ("120", "Oba Femi", "NXT"),
    ("121", "Stacy Keibler", "Legend"),
    ("122", "Berto", "Smackdown"),
    ("123", "Kurt Angle", "Legend"),
    ("124", "Chris Sabin", "Smackdown"),
    ("125", "Lex Luger", "Legend"),
    ("126", "Edris Enofé", "NXT"),
    ("127", "Andre Chase", "NXT"),
    ("128", "Ridge Holland", "NXT"),
    ("129", "Natalya", "Raw"),
    ("130", "Noam Dar", "NXT"),
    ("131", "Axiom", "Smackdown"),
    ("132", "Nikki Cross", "Smackdown"),
    ("133", "Ethan Page", "NXT"),
    ("134", "Wren Sinclair", "NXT"),
    ("135", "Mick Foley", "Legend"),
    ("136", "Angel", "Smackdown"),
    ("137", "Grayson Waller", "Raw"),
    ("138", "Mark Henry", "Legend"),
    ("139", "Erik", "Raw"),
    ("140", "Brutus Creed", "Raw"),
    ("141", "Myles Borne", "NXT"),
    ("142", "Malik Blade", "NXT"),
    ("143", "B-Fab", "Smackdown"),
    ("144", "Tyra Mae Steele", "NXT"),
    ("145", "Erick Rowan", "Smackdown"),
    ("146", "Nathan Frazer", "Smackdown"),
    ("147", "Stevie Turner", "NXT"),
    ("148", "Kendal Grey", "NXT"),
    ("149", "Brinley Reece", "NXT"),
    ("150", "Montez Ford", "Smackdown"),
    ("151", "Joaquin Wilde", "Raw"),
    ("152", "Alex Shelley", "Smackdown"),
    ("153", "Joe Gacy", "Smackdown"),
    ("154", "Saquon Shugars", "NXT"),
    ("155", "Dragon Lee", "Raw"),
    ("156", "Naomi", "Raw"),
    ("157", "Cutler James", "NXT"),
    ("158", "Zaria", "NXT"),
    ("159", "Carlee Bright", "NXT"),
    ("160", "Dion Lennox", "NXT"),
    ("161", "Jacy Jayne", "NXT"),
    ("162", "Piper Niven", "Smackdown"),
    ("163", "Charlie Dempsey", "NXT"),
    ("164", "Santos Escobar", "Smackdown"),
    ("165", "Fallon Henley", "NXT"),
    ("166", "Kofi Kingston", "Raw"),
    ("167", "Adriana Rizzo", "NXT"),
    ("168", "Brock Lesnar", "WWE"),
    ("169", "Giulia", "Smackdown"),
    ("170", "Osiris Griffin", "NXT"),
    ("171", "Dexter Lumis", "Smackdown"),
    ("172", "Bubba Ray Dudley", "Legend"),
    ("173", "Ilja Dragunov", "Raw"),
    ("174", "Kairi Sane", "Raw"),
    ("175", "Apollo Crews", "Smackdown"),
    ("176", "Blake Monroe", "NXT"),
    ("177", "Luca Crusifino", "NXT"),
    ("178", "Julius Creed", "Raw"),
    ("179", "Cruz Del Toro", "Raw"),
    ("180", "Wes Lee", "NXT"),
    ("181", "Ivy Nile", "Raw"),
    ("182", "Lilian Garcia", "Smackdown"),
    ("183", "Thea Hail", "NXT"),
    ("184", "Alba Fyre", "Smackdown"),
    ("185", "Tank Ledger", "NXT"),
    ("186", "Je'Von Evans", "NXT"),
    ("187", "Josh Briggs", "NXT"),
    ("188", "Channing Stacks Lorenzo", "NXT"),
    ("189", "Zelina Vega", "Smackdown"),
    ("190", "Tyriek Igwe", "NXT"),
    ("191", "Tatum Paxley", "NXT"),
    ("192", "Xavier Woods", "Raw"),
    ("193", "Wendy Choo", "NXT"),
    ("194", "Nikki Bella", "Raw"),
    ("195", "Hank Walker", "NXT"),
    ("196", "Tavion Heights", "NXT"),
    ("197", "Tama Tonga", "Smackdown"),
    ("198", "D-Von Dudley", "Legend"),
    ("199", "Tyson Dupont", "NXT"),
    ("200", "Jaida Parker", "NXT"),
])
print("  Base Cards II: 100 cards")

# ────────────────────────────────────────────────────────────────────────────────
# BASE TIER III (1 card)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Base Tier III", BASE_PARALLELS, [
    ("301", "Joe Hendry", "NXT"),
])
print("  Base Tier III: 1 card")

# ────────────────────────────────────────────────────────────────────────────────
# Base - Alternate Personas (25 cards — Hobby Exclusive, Superfractor /1 only)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Base - Alternate Personas", SUPERFRACTOR_ONLY, [
    ("201", "Rocky Maivia", "Legend"),
    ("202", "The Prototype", "Legend"),
    ("203", "Mean Mark Callous", "Legend"),
    ("204", "Terra Ryzing", "Legend"),
    ("205", "The Demon Finn Bálor", "Raw"),
    ("206", "Isaac Yankem DDS", "Legend"),
    ("207", "The Ringmaster", "Legend"),
    ("208", "Walter", "Raw"),
    ("209", "Jordan Devlin", "Raw"),
    ("210", "Justin Hawk Bradshaw", "Legend"),
    ("211", "The Sultan", "Legend"),
    ("212", "Marcel Barthel", "Raw"),
    ("213", "Bo Dallas", "Smackdown"),
    ("214", "K-Kwik", "Raw"),
    ("215", "The Zodiac", "Legend"),
    ("216", "Camacho", "Smackdown"),
    ("217", "El Matador", "Legend"),
    ("218", "Roman Leakee", "Smackdown"),
    ("219", "Repo Man", "Legend"),
    ("220", "El Grande Americano", "Raw"),
    ("221", "Stardust", "Smackdown"),
    ("222", "Rockabilly", "Legend"),
    ("223", "The Roadie", "Legend"),
    ("224", "Vinny Vegas", "Legend"),
    ("225", "Mr. America", "Legend"),
])
print("  Base - Alternate Personas: 25 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Base - Iconic Imprints (75 cards — Hobby Exclusive, Superfractor /1 only)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Base - Iconic Imprints", SUPERFRACTOR_ONLY, [
    ("226", "Tony D'Angelo", "NXT"),
    ("227", "Asuka", "Raw"),
    ("228", "Aleister Black", "Smackdown"),
    ("229", "Tiffany Stratton", "Smackdown"),
    ("230", "Bret Hit Man Hart", "Legend"),
    ("231", "Jimmy Uso", "Smackdown"),
    ("232", "Michin", "Smackdown"),
    ("233", "Bianca Belair", "Smackdown"),
    ("234", "Sol Ruca", "NXT"),
    ("235", "Iyo Sky", "Raw"),
    ("236", "Shinsuke Nakamura", "Smackdown"),
    ("237", "Nia Jax", "Smackdown"),
    ("238", "Izzi Dame", "NXT"),
    ("239", "Nikkita Lyons", "NXT"),
    ("240", "Seth Rollins", "Raw"),
    ("241", "Penta", "Raw"),
    ("242", "X-Pac", "Legend"),
    ("243", "Damian Priest", "Smackdown"),
    ("244", "Paul Heyman", "Smackdown"),
    ("245", "Jade Cargill", "Smackdown"),
    ("246", "Shawn Spears", "NXT"),
    ("247", "AJ Styles", "Raw"),
    ("248", "The Miz", "Smackdown"),
    ("249", "CM Punk", "Raw"),
    ("250", "Rusev", "Raw"),
    ("251", "Kevin Owens", "Smackdown"),
    ("252", "Trick Williams", "NXT"),
    ("253", "Bronson Reed", "Raw"),
    ("254", "Karmen Petrovic", "NXT"),
    ("255", "Jacob Fatu", "Smackdown"),
    ("256", "Jordynne Grace", "NXT"),
    ("257", "Maxxine Dupri", "Raw"),
    ("258", "Chad Gable", "Raw"),
    ("259", "Shawn Michaels", "Legend"),
    ("260", "Zoey Stark", "Raw"),
    ("261", "Lita", "Legend"),
    ("262", "Pete Dunne", "Raw"),
    ("263", "Solo Sikoa", "Smackdown"),
    ("264", "Alexa Bliss", "Smackdown"),
    ("265", "Roxanne Perez", "Raw"),
    ("266", "Torrie Wilson", "Legend"),
    ("267", "Sami Zayn", "Smackdown"),
    ("268", "Lyra Valkyria", "Raw"),
    ("269", "Sheamus", "Raw"),
    ("270", "Carmelo Hayes", "Smackdown"),
    ("271", "Booker T", "Legend"),
    ("272", "Randy Orton", "Smackdown"),
    ("273", "Dominik Mysterio", "Raw"),
    ("274", "Stephanie Vaquer", "Raw"),
    ("275", "Otis", "Raw"),
    ("276", "Bray Wyatt", "Legend"),
    ("277", "Austin Theory", "Raw"),
    ("278", "Kit Wilson", "Smackdown"),
    ("279", "Rey Fenix", "Smackdown"),
    ("280", "Chelsea Green", "Smackdown"),
    ("281", "Elton Prince", "Smackdown"),
    ("282", "Kiana James", "Smackdown"),
    ("283", "Jey Uso", "Raw"),
    ("284", "Raquel Rodriguez", "Raw"),
    ("285", "Chyna", "Legend"),
    ("286", "Tommaso Ciampa", "Smackdown"),
    ("287", "LA Knight", "Raw"),
    ("288", "Akira Tozawa", "Raw"),
    ("289", "Charlotte Flair", "Smackdown"),
    ("290", "Candice LeRae", "Smackdown"),
    ("291", "Tyler Breeze", "Legend"),
    ("292", "Rikishi", "Legend"),
    ("293", "Bron Breakker", "Raw"),
    ("294", "Ricky Saints", "NXT"),
    ("295", "Kelani Jordan", "NXT"),
    ("296", "Drew McIntyre", "Smackdown"),
    ("297", "Rey Mysterio", "Raw"),
    ("298", "Lola Vice", "NXT"),
    ("299", "Batista", "Legend"),
    ("300", "Jacy Jayne", "NXT"),
])
print("  Base - Iconic Imprints: 75 cards")

# ════════════════════════════════════════════════════════════════════════════════
# AUTOGRAPH INSERT SETS
# ════════════════════════════════════════════════════════════════════════════════

# ────────────────────────────────────────────────────────────────────────────────
# Chrome Autographs (91 cards)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Chrome Autographs", CHROME_AUTO_PARALLELS, [
    ("BCA-ADR", "Adriana Rizzo", "NXT"),
    ("BCA-AKT", "Akira Tozawa", "Raw"),
    ("BCA-ALB", "Aleister Black", "Smackdown"),
    ("BCA-ALF", "Alba Fyre", "Smackdown"),
    ("BCA-ALS", "Alex Shelley", "Smackdown"),
    ("BCA-ANC", "Andre Chase", "NXT"),
    ("BCA-ANE", "Angel", "Smackdown"),
    ("BCA-ARG", "Arianna Grace", "NXT"),
    ("BCA-ASK", "Asuka", "Raw"),
    ("BCA-AUT", "Austin Theory", "Raw"),
    ("BCA-AXI", "Axiom", "Smackdown"),
    ("BCA-BEL", "Becky Lynch", "Raw"),
    ("BCA-BER", "Berto", "Smackdown"),
    ("BCA-BFB", "B-Fab", "Smackdown"),
    ("BCA-BRC", "Brutus Creed", "Raw"),
    ("BCA-CDT", "Cruz Del Toro", "Raw"),
    ("BCA-CHD", "Charlie Dempsey", "NXT"),
    ("BCA-CHF", "Charlotte Flair", "Smackdown"),
    ("BCA-CHS", "Chris Sabin", "Smackdown"),
    ("BCA-CSL", "Channing Stacks Lorenzo", "NXT"),
    ("BCA-DEL", "Dexter Lumis", "Smackdown"),
    ("BCA-DRL", "Dragon Lee", "Raw"),
    ("BCA-ELP", "Elton Prince", "Smackdown"),
    ("BCA-ERI", "Erik", "Raw"),
    ("BCA-ERO", "Erick Rowan", "Smackdown"),
    ("BCA-ETP", "Ethan Page", "NXT"),
    ("BCA-FAH", "Fallon Henley", "NXT"),
    ("BCA-GIU", "Giulia", "Smackdown"),
    ("BCA-HUH", "Hulk Hogan", "Legend"),
    ("BCA-ILD", "Ilja Dragunov", "Raw"),
    ("BCA-IVA", "Ivar", "Raw"),
    ("BCA-IVN", "Ivy Nile", "Raw"),
    ("BCA-JAJ", "Jacy Jayne", "NXT"),
    ("BCA-JAP", "Jaida Parker", "NXT"),
    ("BCA-JCM", "JC Mateo", "Smackdown"),
    ("BCA-JEE", "Je'Von Evans", "NXT"),
    ("BCA-JOC", "John Cena", "Legend"),
    ("BCA-JOG", "Joe Gacy", "Smackdown"),
    ("BCA-JOW", "Joaquin Wilde", "Raw"),
    ("BCA-JUC", "Julius Creed", "Raw"),
    ("BCA-KAS", "Kairi Sane", "Raw"),
    ("BCA-KEN", "Kevin Nash", "Legend"),
    ("BCA-KIJ", "Kiana James", "Smackdown"),
    ("BCA-KIW", "Kit Wilson", "Smackdown"),
    ("BCA-KOK", "Kofi Kingston", "Raw"),
    ("BCA-LAL", "Lash Legend", "NXT"),
    ("BCA-LEK", "Lexis King", "NXT"),
    ("BCA-LIM", "Liv Morgan", "Raw"),
    ("BCA-LIT", "Lita", "Legend"),
    ("BCA-LNY", "Lainey Reid", "NXT"),
    ("BCA-LUC", "Luca Crusifino", "NXT"),
    ("BCA-MAD", "Maxxine Dupri", "Raw"),
    ("BCA-MOF", "Montez Ford", "Smackdown"),
    ("BCA-MYB", "Myles Borne", "NXT"),
    ("BCA-NAF", "Nathan Frazer", "Smackdown"),
    ("BCA-NAO", "Naomi", "Raw"),
    ("BCA-NAT", "Natalya", "Raw"),
    ("BCA-NIC", "Nikki Cross", "Smackdown"),
    ("BCA-NOD", "Noam Dar", "NXT"),
    ("BCA-OBF", "Oba Femi", "NXT"),
    ("BCA-OTI", "Otis", "Raw"),
    ("BCA-PED", "Pete Dunne", "Raw"),
    ("BCA-REF", "Rey Fenix", "Smackdown"),
    ("BCA-RIK", "Rikishi", "Legend"),
    ("BCA-ROJ", "Road Dogg Jesse James", "Legend"),
    ("BCA-ROX", "Roxanne Perez", "Raw"),
    ("BCA-RSV", "Rusev", "Raw"),
    ("BCA-RTR", "Ron Killings", "Smackdown"),
    ("BCA-SHM", "Shawn Michaels", "Legend"),
    ("BCA-STA", "Stone Cold Steve Austin", "Legend"),
    ("BCA-STK", "Stacy Keibler", "Legend"),
    ("BCA-TAP", "Tatum Paxley", "NXT"),
    ("BCA-TAT", "Tama Tonga", "Smackdown"),
    ("BCA-TBT", "Tyler Bate", "Raw"),
    ("BCA-THH", "Thea Hail", "NXT"),
    ("BCA-THR", "The Rock", "Legend"),
    ("BCA-TOL", "Tonga Loa", "Smackdown"),
    ("BCA-TOW", "Torrie Wilson", "Legend"),
    ("BCA-TRS", "Trish Stratus", "Legend"),
    ("BCA-TTA", "Talla Tonga", "Smackdown"),
    ("BCA-TYB", "Tyler Breeze", "Legend"),
    ("BCA-TYP", "Typhoon", "Legend"),
    ("BCA-UNH", "Uncle Howdy", "Smackdown"),
    ("BCA-UNT", "Undertaker", "Legend"),
    ("BCA-VIC", "Victoria", "Legend"),
    ("BCA-WRS", "Wren Sinclair", "NXT"),
    ("BCA-XAW", "Xavier Woods", "Raw"),
    ("BCA-XPA", "X-Pac", "Legend"),
    ("BCA-ZAR", "Zaria", "NXT"),
    ("BCA-ZEV", "Zelina Vega", "Smackdown"),
    ("BCA-ZOS", "Zoey Stark", "Raw"),
])
print("  Chrome Autographs: 91 cards")

# Chrome Autographs FDI Exclusives (3 cards — same insert set name, flagged FDI exclusive)
# These are additional appearances within the Chrome Autographs insert set
# but we store them as a separate insert set since they have different exclusivity
make_insert_set("Chrome Autographs FDI Exclusives", CHROME_AUTO_PARALLELS, [
    ("BCA-TYB", "Tyler Breeze", "Legend"),
    ("BCA-VIC", "Victoria", "Legend"),
    ("BCA-XPA", "X-Pac", "Legend"),
])
print("  Chrome Autographs FDI Exclusives: 3 cards")

# Chrome Autographs III (2 cards)
make_insert_set("Chrome Autographs III", CHROME_AUTO_PARALLELS, [
    ("BCA-BRK", "Brock Lesnar", "WWE"),
    ("BCA-SHN", "Joe Hendry", "NXT"),
])
print("  Chrome Autographs III: 2 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Red Brand Autographs (36 cards)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Red Brand Autographs", BRAND_AUTO_PARALLELS, [
    ("RBA-AJS", "AJ Styles", "Raw"),
    ("RBA-BAY", "Bayley", "Raw"),
    ("RBA-BRO", "Bron Breakker", "Raw"),
    ("RBA-BRU", "Brutus Creed", "Raw"),
    ("RBA-CHA", "Chad Gable", "Raw"),
    ("RBA-CMP", "CM Punk", "Raw"),
    ("RBA-DOM", "Dominik Mysterio", "Raw"),
    ("RBA-DRA", "Dragon Lee", "Raw"),
    ("RBA-ERI", "Erik", "Raw"),
    ("RBA-FIN", "Finn Bálor", "Raw"),
    ("RBA-GUN", "Gunther", "Raw"),
    ("RBA-ILJ", "Ilja Dragunov", "Raw"),
    ("RBA-IVA", "Ivar", "Raw"),
    ("RBA-IVY", "Ivy Nile", "Raw"),
    ("RBA-IYO", "Iyo Sky", "Raw"),
    ("RBA-JDM", "JD McDonagh", "Raw"),
    ("RBA-JEY", "Jey Uso", "Raw"),
    ("RBA-JUL", "Julius Creed", "Raw"),
    ("RBA-KAI", "Kairi Sane", "Raw"),
    ("RBA-KOF", "Kofi Kingston", "Raw"),
    ("RBA-LAK", "LA Knight", "Raw"),
    ("RBA-LUD", "Ludwig Kaiser", "Raw"),
    ("RBA-LYR", "Lyra Valkyria", "Raw"),
    ("RBA-MAX", "Maxxine Dupri", "Raw"),
    ("RBA-NAT", "Natalya", "Raw"),
    ("RBA-PEN", "Penta", "Raw"),
    ("RBA-RAQ", "Raquel Rodriguez", "Raw"),
    ("RBA-REE", "Bronson Reed", "Raw"),
    ("RBA-REY", "Rey Mysterio", "Raw"),
    ("RBA-RHE", "Rhea Ripley", "Raw"),
    ("RBA-ROX", "Roxanne Perez", "Raw"),
    ("RBA-RSV", "Rusev", "Raw"),
    ("RBA-SET", "Seth Rollins", "Raw"),
    ("RBA-SHE", "Sheamus", "Raw"),
    ("RBA-STE", "Stephanie Vaquer", "Raw"),
    ("RBA-XAV", "Xavier Woods", "Raw"),
])
print("  Red Brand Autographs: 36 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Blue Brand Autographs (32 cards)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Blue Brand Autographs", BRAND_AUTO_PARALLELS, [
    ("BBA-ALB", "Alba Fyre", "Smackdown"),
    ("BBA-ALE", "Alex Shelley", "Smackdown"),
    ("BBA-AXI", "Axiom", "Smackdown"),
    ("BBA-BIA", "Bianca Belair", "Smackdown"),
    ("BBA-BLI", "Alexa Bliss", "Smackdown"),
    ("BBA-CAN", "Candice LeRae", "Smackdown"),
    ("BBA-CAR", "Carmelo Hayes", "Smackdown"),
    ("BBA-CHE", "Chelsea Green", "Smackdown"),
    ("BBA-CHR", "Chris Sabin", "Smackdown"),
    ("BBA-COD", "The American Nightmare Cody Rhodes", "Smackdown"),
    ("BBA-DAM", "Damian Priest", "Smackdown"),
    ("BBA-DRE", "Drew McIntyre", "Smackdown"),
    ("BBA-GIU", "Giulia", "Smackdown"),
    ("BBA-JAC", "Jacob Fatu", "Smackdown"),
    ("BBA-JAD", "Jade Cargill", "Smackdown"),
    ("BBA-JOH", "Johnny Gargano", "Smackdown"),
    ("BBA-KEV", "Kevin Owens", "Smackdown"),
    ("BBA-MIC", "Michin", "Smackdown"),
    ("BBA-MON", "Montez Ford", "Smackdown"),
    ("BBA-NAT", "Nathan Frazer", "Smackdown"),
    ("BBA-NIA", "Nia Jax", "Smackdown"),
    ("BBA-RAN", "Randy Orton", "Smackdown"),
    ("BBA-REY", "Rey Fenix", "Smackdown"),
    ("BBA-ROM", "Roman Reigns", "Smackdown"),
    ("BBA-RON", "Ron Killings", "Smackdown"),
    ("BBA-SAM", "Sami Zayn", "Smackdown"),
    ("BBA-SHI", "Shinsuke Nakamura", "Smackdown"),
    ("BBA-SOL", "Solo Sikoa", "Smackdown"),
    ("BBA-TAL", "Talla Tonga", "Smackdown"),
    ("BBA-TIF", "Tiffany Stratton", "Smackdown"),
    ("BBA-TON", "Tonga Loa", "Smackdown"),
    ("BBA-ZEL", "Zelina Vega", "Smackdown"),
])
print("  Blue Brand Autographs: 32 cards")

# ────────────────────────────────────────────────────────────────────────────────
# NXT Autographs (24 cards)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("NXT Autographs", BRAND_AUTO_PARALLELS, [
    ("NXT-ARI", "Arianna Grace", "NXT"),
    ("NXT-BRO", "Bronco Nima", "NXT"),
    ("NXT-CHA", "Charlie Dempsey", "NXT"),
    ("NXT-ETH", "Ethan Page", "NXT"),
    ("NXT-FAL", "Fallon Henley", "NXT"),
    ("NXT-IZZ", "Izzi Dame", "NXT"),
    ("NXT-JAI", "Jaida Parker", "NXT"),
    ("NXT-JEV", "Je'Von Evans", "NXT"),
    ("NXT-JOR", "Jordynne Grace", "NXT"),
    ("NXT-KAR", "Karmen Petrovic", "NXT"),
    ("NXT-KEL", "Kelani Jordan", "NXT"),
    ("NXT-LAI", "Lainey Reid", "NXT"),
    ("NXT-LEX", "Lexis King", "NXT"),
    ("NXT-LOL", "Lola Vice", "NXT"),
    ("NXT-LUC", "Lucien Price", "NXT"),
    ("NXT-NIK", "Nikkita Lyons", "NXT"),
    ("NXT-OBA", "Oba Femi", "NXT"),
    ("NXT-RIC", "Ricky Saints", "NXT"),
    ("NXT-SHA", "Shawn Spears", "NXT"),
    ("NXT-SOL", "Sol Ruca", "NXT"),
    ("NXT-TAT", "Tatum Paxley", "NXT"),
    ("NXT-TON", "Tony D'Angelo", "NXT"),
    ("NXT-TRI", "Trick Williams", "NXT"),
    ("NXT-ZAR", "Zaria", "NXT"),
])
print("  NXT Autographs: 24 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Marks of Champions (15 cards)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Marks of Champions", PREMIUM_AUTO_PARALLELS, [
    ("MOC-AB", "Alexa Bliss", "Smackdown"),
    ("MOC-BL", "Becky Lynch", "Raw"),
    ("MOC-CF", "Charlotte Flair", "Smackdown"),
    ("MOC-IS", "Iyo Sky", "Raw"),
    ("MOC-KA", "Kurt Angle", "Legend"),
    ("MOC-KO", "Kevin Owens", "Smackdown"),
    ("MOC-LA", "LA Knight", "Raw"),
    ("MOC-OF", "Oba Femi", "NXT"),
    ("MOC-RR", "Rhea Ripley", "Raw"),
    ("MOC-SR", "Seth Rollins", "Raw"),
    ("MOC-SV", "Stephanie Vaquer", "Raw"),
    ("MOC-TM", "The Miz", "Smackdown"),
    ("MOC-TR", "The Rock", "Legend"),
    ("MOC-TS", "Tiffany Stratton", "Smackdown"),
    ("MOC-UT", "Undertaker", "Legend"),
])
print("  Marks of Champions: 15 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Legendary Chrome Autographs (12 cards)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Legendary Chrome Autographs", PREMIUM_AUTO_PARALLELS, [
    ("LCA-AL", "Albert", "Legend"),
    ("LCA-BB", "Brutus Beefcake", "Legend"),
    ("LCA-CB", "Cowboy Bob Orton", "Legend"),
    ("LCA-DL", "D'Lo Brown", "Legend"),
    ("LCA-FL", "Finlay", "Legend"),
    ("LCA-HD", "Hacksaw Jim Duggan", "Legend"),
    ("LCA-HJ", "Hillbilly Jim", "Legend"),
    ("LCA-HW", "Hornswoggle", "Legend"),
    ("LCA-JS", "Jerry Sags", "Legend"),
    ("LCA-KW", "Koko B. Ware", "Legend"),
    ("LCA-TW", "Torrie Wilson", "Legend"),
    ("LCA-WB", "Wade Barrett", "Legend"),
])
print("  Legendary Chrome Autographs: 12 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Main Event Autographs (14 cards)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Main Event Autographs", PREMIUM_AUTO_PARALLELS, [
    ("MEA-AS", "Asuka", "Raw"),
    ("MEA-BB", "Bianca Belair", "Smackdown"),
    ("MEA-BH", "Bret Hit Man Hart", "Legend"),
    ("MEA-BY", "Bayley", "Raw"),
    ("MEA-CR", "The American Nightmare Cody Rhodes", "Smackdown"),
    ("MEA-DM", "Drew McIntyre", "Smackdown"),
    ("MEA-DP", "Damian Priest", "Smackdown"),
    ("MEA-GT", "Gunther", "Raw"),
    ("MEA-KN", "Kane", "Legend"),
    ("MEA-SA", "Stone Cold Steve Austin", "Legend"),
    ("MEA-SM", "Shawn Michaels", "Legend"),
    ("MEA-SR", "Seth Rollins", "Raw"),
    ("MEA-SZ", "Sami Zayn", "Smackdown"),
    ("MEA-UT", "Undertaker", "Legend"),
])
print("  Main Event Autographs: 14 cards")

# ────────────────────────────────────────────────────────────────────────────────
# 1986 Topps Autographs (30 cards)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("1986 Topps Autographs", PREMIUM_AUTO_PARALLELS, [
    ("86T-AB", "Alexa Bliss", "Smackdown"),
    ("86T-BB", "Bianca Belair", "Smackdown"),
    ("86T-BY", "Bayley", "Raw"),
    ("86T-CF", "Charlotte Flair", "Smackdown"),
    ("86T-CG", "Chelsea Green", "Smackdown"),
    ("86T-CM", "CM Punk", "Raw"),
    ("86T-CR", "The American Nightmare Cody Rhodes", "Smackdown"),
    ("86T-DM", "Drew McIntyre", "Smackdown"),
    ("86T-DP", "Damian Priest", "Smackdown"),
    ("86T-FB", "Finn Bálor", "Raw"),
    ("86T-GT", "Gunther", "Raw"),
    ("86T-IS", "Iyo Sky", "Raw"),
    ("86T-JC", "John Cena", "Legend"),
    ("86T-JF", "Jacob Fatu", "Smackdown"),
    ("86T-JL", "Jade Cargill", "Smackdown"),
    ("86T-JY", "Jey Uso", "Raw"),
    ("86T-KO", "Kevin Owens", "Smackdown"),
    ("86T-LA", "LA Knight", "Raw"),
    ("86T-LM", "Liv Morgan", "Raw"),
    ("86T-NJ", "Nia Jax", "Smackdown"),
    ("86T-PT", "Penta", "Raw"),
    ("86T-RF", "Rey Fenix", "Smackdown"),
    ("86T-RO", "Randy Orton", "Smackdown"),
    ("86T-SA", "Stone Cold Steve Austin", "Legend"),
    ("86T-SM", "Shawn Michaels", "Legend"),
    ("86T-SS", "Solo Sikoa", "Smackdown"),
    ("86T-TH", "Triple H", "Legend"),
    ("86T-TR", "The Rock", "Legend"),
    ("86T-TS", "Tiffany Stratton", "Smackdown"),
    ("86T-UT", "Undertaker", "Legend"),
])
print("  1986 Topps Autographs: 30 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Hall of Fame Autographs (10 cards)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Hall of Fame Autographs", PREMIUM_AUTO_PARALLELS, [
    ("HOF-BH", "Bret Hit Man Hart", "Legend"),
    ("HOF-BN", "Bull Nakano", "Legend"),
    ("HOF-DF", "Dory Funk Jr.", "Legend"),
    ("HOF-LL", "Lex Luger", "Legend"),
    ("HOF-MM", "Michelle McCool", "Legend"),
    ("HOF-MR", "Mike Rotunda", "Legend"),
    ("HOF-PH", "Paul Heyman", "Smackdown"),
    ("HOF-SC", "Stone Cold Steve Austin", "Legend"),
    ("HOF-TG", "Tugboat", "Legend"),
    ("HOF-TH", "Triple H", "Legend"),
])
print("  Hall of Fame Autographs: 10 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Future Stars Autographs (9 cards)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Future Stars Autographs", PREMIUM_AUTO_PARALLELS, [
    ("FSA-BLA", "Blake Monroe", "NXT"),
    ("FSA-ETH", "Ethan Page", "NXT"),
    ("FSA-FAL", "Fallon Henley", "NXT"),
    ("FSA-JEV", "Je'Von Evans", "NXT"),
    ("FSA-JOR", "Jordynne Grace", "NXT"),
    ("FSA-KAR", "Karmen Petrovic", "NXT"),
    ("FSA-MYL", "Myles Borne", "NXT"),
    ("FSA-RIC", "Ricky Saints", "NXT"),
    ("FSA-ZAR", "Zaria", "NXT"),
])
print("  Future Stars Autographs: 9 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Iconic Imprint Autographs (61 cards — Hobby Exclusive, all /10)
# ────────────────────────────────────────────────────────────────────────────────

# Base is /10, stored as parallel. Plus Red /5 and Superfractor /1.
IIA_PARALLELS = [
    ("Base /10", 10),
    ("Red", 5),
    ("Superfractor", 1),
]

make_insert_set("Iconic Imprint Autographs", IIA_PARALLELS, [
    ("IIA-ABK", "Aleister Black", "Smackdown"),
    ("IIA-AJS", "AJ Styles", "Raw"),
    ("IIA-ALE", "Alexa Bliss", "Smackdown"),
    ("IIA-ASU", "Asuka", "Raw"),
    ("IIA-AUS", "Austin Theory", "Raw"),
    ("IIA-BIA", "Bianca Belair", "Smackdown"),
    ("IIA-BOT", "Booker T", "Legend"),
    ("IIA-BRE", "Bret Hit Man Hart", "Legend"),
    ("IIA-BRK", "Bron Breakker", "Raw"),
    ("IIA-BRO", "Bronson Reed", "Raw"),
    ("IIA-CAN", "Candice LeRae", "Smackdown"),
    ("IIA-CAR", "Carmelo Hayes", "Smackdown"),
    ("IIA-CHA", "Chad Gable", "Raw"),
    ("IIA-CHE", "Chelsea Green", "Smackdown"),
    ("IIA-CHL", "Charlotte Flair", "Smackdown"),
    ("IIA-CMP", "CM Punk", "Raw"),
    ("IIA-DAM", "Damian Priest", "Smackdown"),
    ("IIA-DDM", "Dominik Mysterio", "Raw"),
    ("IIA-DRE", "Drew McIntyre", "Smackdown"),
    ("IIA-FEN", "Rey Fenix", "Smackdown"),
    ("IIA-HBK", "Shawn Michaels", "Legend"),
    ("IIA-IYO", "Iyo Sky", "Raw"),
    ("IIA-IZZ", "Izzi Dame", "NXT"),
    ("IIA-JAC", "Jacob Fatu", "Smackdown"),
    ("IIA-JAD", "Jade Cargill", "Smackdown"),
    ("IIA-JEY", "Jey Uso", "Raw"),
    ("IIA-JIM", "Jimmy Uso", "Smackdown"),
    ("IIA-JJA", "Jacy Jayne", "NXT"),
    ("IIA-JOR", "Jordynne Grace", "NXT"),
    ("IIA-KEL", "Kelani Jordan", "NXT"),
    ("IIA-KEV", "Kevin Owens", "Smackdown"),
    ("IIA-KIA", "Kiana James", "Smackdown"),
    ("IIA-LAK", "LA Knight", "Raw"),
    ("IIA-LIA", "Lita", "Legend"),
    ("IIA-LOL", "Lola Vice", "NXT"),
    ("IIA-LYR", "Lyra Valkyria", "Raw"),
    ("IIA-MAX", "Maxxine Dupri", "Raw"),
    ("IIA-MIZ", "The Miz", "Smackdown"),
    ("IIA-NIK", "Nikkita Lyons", "NXT"),
    ("IIA-OTI", "Otis", "Raw"),
    ("IIA-PAU", "Paul Heyman", "Smackdown"),
    ("IIA-PEN", "Penta", "Raw"),
    ("IIA-PET", "Pete Dunne", "Raw"),
    ("IIA-RAQ", "Raquel Rodriguez", "Raw"),
    ("IIA-REY", "Rey Mysterio", "Raw"),
    ("IIA-RIC", "Ricky Saints", "NXT"),
    ("IIA-RIK", "Rikishi", "Legend"),
    ("IIA-RUS", "Rusev", "Raw"),
    ("IIA-SAM", "Sami Zayn", "Smackdown"),
    ("IIA-SET", "Seth Rollins", "Raw"),
    ("IIA-SHA", "Shawn Spears", "NXT"),
    ("IIA-SHE", "Sheamus", "Raw"),
    ("IIA-SHI", "Shinsuke Nakamura", "Smackdown"),
    ("IIA-SKA", "Solo Sikoa", "Smackdown"),
    ("IIA-SOL", "Sol Ruca", "NXT"),
    ("IIA-STE", "Stephanie Vaquer", "Raw"),
    ("IIA-TIF", "Tiffany Stratton", "Smackdown"),
    ("IIA-TOR", "Torrie Wilson", "Legend"),
    ("IIA-TRI", "Trick Williams", "NXT"),
    ("IIA-TYL", "Tyler Breeze", "Legend"),
    ("IIA-XPA", "X-Pac", "Legend"),
])
print("  Iconic Imprint Autographs: 61 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Alternate Personas Autographs (25 cards — Hobby Exclusive, all /10)
# ────────────────────────────────────────────────────────────────────────────────

APA_PARALLELS = [
    ("Base /10", 10),
    ("Red", 5),
    ("Superfractor", 1),
]

make_insert_set("Alternate Personas Autographs", APA_PARALLELS, [
    ("APA-BD", "Bo Dallas", "Smackdown"),
    ("APA-CM", "Camacho", "Smackdown"),
    ("APA-EG", "El Grande Americano", "Raw"),
    ("APA-EM", "El Matador", "Legend"),
    ("APA-FB", "The Demon Finn Bálor", "Raw"),
    ("APA-IY", "Isaac Yankem DDS", "Legend"),
    ("APA-JD", "Jordan Devlin", "Raw"),
    ("APA-JH", "Justin Hawk Bradshaw", "Legend"),
    ("APA-KK", "K-Kwik", "Smackdown"),
    ("APA-MB", "Marcel Barthel", "Raw"),
    ("APA-MC", "Mean Mark Callous", "Legend"),
    ("APA-RB", "Rockabilly", "Legend"),
    ("APA-RG", "The Ringmaster", "Legend"),
    ("APA-RL", "Roman Leakee", "Smackdown"),
    ("APA-RM", "Rocky Maivia", "Legend"),
    ("APA-RP", "Repo Man", "Legend"),
    ("APA-SD", "Stardust", "Smackdown"),
    ("APA-TB", "Mr. America", "Legend"),
    ("APA-TE", "The Roadie", "Legend"),
    ("APA-TP", "The Prototype", "Legend"),
    ("APA-TR", "Terra Ryzing", "Legend"),
    ("APA-TS", "The Sultan", "Legend"),
    ("APA-TZ", "The Zodiac", "Legend"),
    ("APA-VV", "Vinny Vegas", "Legend"),
    ("APA-WT", "Walter", "Raw"),
])
print("  Alternate Personas Autographs: 25 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Dual Autographs (10 cards — co_players, Hobby Exclusive, /10)
# ────────────────────────────────────────────────────────────────────────────────

DAU_PARALLELS = [
    ("Base /10", 10),
    ("Red", 5),
    ("Superfractor", 1),
]

is_id = create_insert_set(set_id, "Dual Autographs")
for par_name, par_pr in DAU_PARALLELS:
    create_parallel(is_id, par_name, par_pr)
add_multi_cards(is_id, [
    ("DAU-CG", [("Tommaso Ciampa", "Smackdown"), ("Johnny Gargano", "Smackdown")]),
    ("DAU-FB", [("Montez Ford", "Smackdown"), ("Bianca Belair", "Smackdown")]),
    ("DAU-MM", [("The Miz", "Smackdown"), ("Maryse", "Legend")]),
    ("DAU-MR", [("Liv Morgan", "Raw"), ("Raquel Rodriguez", "Raw")]),
    ("DAU-RC", [("John Cena", "Legend"), ("The Rock", "Legend")]),
    ("DAU-RL", [("Seth Rollins", "Raw"), ("Becky Lynch", "Raw")]),
    ("DAU-SL", [("Lita", "Legend"), ("Trish Stratus", "Legend")]),
    ("DAU-UN", [("Undertaker", "Legend"), ("Michelle McCool", "Legend")]),
    ("DAU-VG", [("Giulia", "Smackdown"), ("Stephanie Vaquer", "Raw")]),
    ("DAU-WP", [("Elton Prince", "Smackdown"), ("Kit Wilson", "Smackdown")]),
])
print("  Dual Autographs: 10 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Best In The World Autograph (1 card — Hobby Exclusive, /10)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Best In The World Autograph", HOBBY_10_PARALLELS, [
    ("BIW-CM", "CM Punk", "Raw"),
])
print("  Best In The World Autograph: 1 card")

# ────────────────────────────────────────────────────────────────────────────────
# 3D Dual Autograph (1 card — co_players, Hobby Exclusive, /10)
# ────────────────────────────────────────────────────────────────────────────────

DYB_PARALLELS = [
    ("Base /10", 10),
    ("Red", 5),
    ("Superfractor", 1),
]

is_id = create_insert_set(set_id, "3D Dual Autograph")
for par_name, par_pr in DYB_PARALLELS:
    create_parallel(is_id, par_name, par_pr)
add_multi_cards(is_id, [
    ("DYB-BD", [("D-Von Dudley", "Legend"), ("Bubba Ray Dudley", "Legend")]),
])
print("  3D Dual Autograph: 1 card")

# ────────────────────────────────────────────────────────────────────────────────
# The People's Champ Autograph (1 card — Hobby Exclusive, /10)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("The People's Champ Autograph", HOBBY_10_PARALLELS, [
    ("TPC-TR", "The Rock", "Legend"),
])
print("  The People's Champ Autograph: 1 card")

# ────────────────────────────────────────────────────────────────────────────────
# Stone Cold Steve Austin 30th Anniversary Autographs (2 cards — Hobby Exclusive, /10)
# ────────────────────────────────────────────────────────────────────────────────

SCA_PARALLELS = [
    ("Base /10", 10),
]

make_insert_set("Stone Cold Steve Austin 30th Anniversary Autographs", SCA_PARALLELS, [
    ("SCA-1", "Stone Cold Steve Austin", "Legend"),
    ("SCA-2", "Stone Cold Steve Austin", "Legend"),
])
print("  Stone Cold Steve Austin 30th Anniversary Autographs: 2 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Dudley Boyz 30th Anniversary Autographs (2 cards — Hobby Exclusive, /10)
# ────────────────────────────────────────────────────────────────────────────────

DUD_PARALLELS = [
    ("Base /10", 10),
]

make_insert_set("Dudley Boyz 30th Anniversary Autographs", DUD_PARALLELS, [
    ("DUD-BRD1", "Bubba Ray Dudley", "Legend"),
    ("DUD-DV1", "D-Von Dudley", "Legend"),
])
print("  Dudley Boyz 30th Anniversary Autographs: 2 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Dudley Boyz 30th Anniversary Dual Autograph (1 card — co_players, Hobby Exclusive, /10)
# ────────────────────────────────────────────────────────────────────────────────

DUD_DUAL_PARALLELS = [
    ("Base /10", 10),
]

is_id = create_insert_set(set_id, "Dudley Boyz 30th Anniversary Dual Autograph")
for par_name, par_pr in DUD_DUAL_PARALLELS:
    create_parallel(is_id, par_name, par_pr)
add_multi_cards(is_id, [
    ("DUD-1", [("D-Von Dudley", "Legend"), ("Bubba Ray Dudley", "Legend")]),
])
print("  Dudley Boyz 30th Anniversary Dual Autograph: 1 card")

# ────────────────────────────────────────────────────────────────────────────────
# CM Punk 20th Anniversary Autographs (2 cards — Hobby Exclusive, /10)
# ────────────────────────────────────────────────────────────────────────────────

CMP_PARALLELS = [
    ("Base /10", 10),
]

make_insert_set("CM Punk 20th Anniversary Autographs", CMP_PARALLELS, [
    ("CMP-1", "CM Punk", "Raw"),
    ("CMP-2", "CM Punk", "Raw"),
])
print("  CM Punk 20th Anniversary Autographs: 2 cards")

# ────────────────────────────────────────────────────────────────────────────────
# The Rock 30th Anniversary Autographs (2 cards — Hobby Exclusive, /10)
# ────────────────────────────────────────────────────────────────────────────────

TRA_PARALLELS = [
    ("Base /10", 10),
]

make_insert_set("The Rock 30th Anniversary Autographs", TRA_PARALLELS, [
    ("TRA-1", "The Rock", "Legend"),
    ("TRA-2", "The Rock", "Legend"),
])
print("  The Rock 30th Anniversary Autographs: 2 cards")

# ────────────────────────────────────────────────────────────────────────────────
# NWO 30th Anniversary Autographs (3 cards — Hobby Exclusive, /10)
# ────────────────────────────────────────────────────────────────────────────────

NWO_PARALLELS = [
    ("Base /10", 10),
]

make_insert_set("NWO 30th Anniversary Autographs", NWO_PARALLELS, [
    ("NWO-HH", "Hollywood Hulk Hogan", "Legend"),
    ("NWO-KN", "Kevin Nash", "Legend"),
    ("NWO-SX", "Syxx", "Legend"),
])
print("  NWO 30th Anniversary Autographs: 3 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Lita 25th Anniversary Autographs (2 cards — Hobby Exclusive, /10)
# ────────────────────────────────────────────────────────────────────────────────

LIT_PARALLELS = [
    ("Base /10", 10),
]

make_insert_set("Lita 25th Anniversary Autographs", LIT_PARALLELS, [
    ("LIT1", "Lita", "Legend"),
    ("LIT2", "Lita", "Legend"),
])
print("  Lita 25th Anniversary Autographs: 2 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Trish Stratus 25th Anniversary Autographs (2 cards — Hobby Exclusive, /10)
# ────────────────────────────────────────────────────────────────────────────────

TRS_PARALLELS = [
    ("Base /10", 10),
]

make_insert_set("Trish Stratus 25th Anniversary Autographs", TRS_PARALLELS, [
    ("TRS1", "Trish Stratus", "Legend"),
    ("TRS2", "Trish Stratus", "Legend"),
])
print("  Trish Stratus 25th Anniversary Autographs: 2 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Beast Incarnate Autograph (1 card — Hobby Exclusive)
# No numbered parallels listed
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Beast Incarnate Autograph", [], [
    ("BIA-BL", "Brock Lesnar", "WWE"),
])
print("  Beast Incarnate Autograph: 1 card")

# ────────────────────────────────────────────────────────────────────────────────
# Say His Name Autograph (1 card — Hobby Exclusive)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Say His Name Autograph", [], [
    ("SHN-JH", "Joe Hendry", "NXT"),
])
print("  Say His Name Autograph: 1 card")

# ────────────────────────────────────────────────────────────────────────────────
# Main Roster Debut Patch Autographs (5 cards — all /1, is_autograph + is_relic)
# ────────────────────────────────────────────────────────────────────────────────

MRD_PARALLELS = [
    ("Base /1", 1),
]

make_insert_set("Main Roster Debut Patch Autographs", MRD_PARALLELS, [
    ("MRD-GL", "Giulia", "Smackdown"),
    ("MRD-JC", "JC Mateo", "Smackdown"),
    ("MRD-RP", "Roxanne Perez", "Raw"),
    ("MRD-SR", "Sol Ruca", "NXT"),
    ("MRD-SV", "Stephanie Vaquer", "Raw"),
])
print("  Main Roster Debut Patch Autographs: 5 cards")

# ════════════════════════════════════════════════════════════════════════════════
# INSERT SETS
# ════════════════════════════════════════════════════════════════════════════════

# ────────────────────────────────────────────────────────────────────────────────
# Scope (40 cards — Hobby/Breaker/FDI Exclusive)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Scope", SCOPE_PARALLELS, [
    ("SCO-1", "The American Nightmare Cody Rhodes", "Smackdown"),
    ("SCO-2", "Tiffany Stratton", "Smackdown"),
    ("SCO-3", "Rhea Ripley", "Raw"),
    ("SCO-4", "Drew McIntyre", "Smackdown"),
    ("SCO-5", "John Cena", "Legend"),
    ("SCO-6", "LA Knight", "Raw"),
    ("SCO-7", "Tommaso Ciampa", "Smackdown"),
    ("SCO-8", "Jey Uso", "Raw"),
    ("SCO-9", "Shinsuke Nakamura", "Smackdown"),
    ("SCO-10", "Uncle Howdy", "Smackdown"),
    ("SCO-11", "Gunther", "Raw"),
    ("SCO-12", "Tony D'Angelo", "NXT"),
    ("SCO-13", "Angelo Dawkins", "Smackdown"),
    ("SCO-14", "Iyo Sky", "Raw"),
    ("SCO-15", "Randy Orton", "Smackdown"),
    ("SCO-16", "Jimmy Uso", "Smackdown"),
    ("SCO-17", "Sol Ruca", "NXT"),
    ("SCO-18", "The Miz", "Smackdown"),
    ("SCO-19", "Solo Sikoa", "Smackdown"),
    ("SCO-20", "Jade Cargill", "Smackdown"),
    ("SCO-21", "Ludwig Kaiser", "Raw"),
    ("SCO-22", "Sheamus", "Raw"),
    ("SCO-23", "Maxxine Dupri", "Raw"),
    ("SCO-24", "Kevin Owens", "Smackdown"),
    ("SCO-25", "Montez Ford", "Smackdown"),
    ("SCO-26", "Rey Mysterio", "Raw"),
    ("SCO-27", "Triple H", "Legend"),
    ("SCO-28", "Rey Fenix", "Smackdown"),
    ("SCO-29", "Sami Zayn", "Smackdown"),
    ("SCO-30", "Michin", "Smackdown"),
    ("SCO-31", "Finn Bálor", "Raw"),
    ("SCO-32", "Damian Priest", "Smackdown"),
    ("SCO-33", "Trick Williams", "NXT"),
    ("SCO-34", "Liv Morgan", "Raw"),
    ("SCO-35", "Shawn Spears", "NXT"),
    ("SCO-36", "The Rock", "Legend"),
    ("SCO-37", "Jordynne Grace", "NXT"),
    ("SCO-38", "Johnny Gargano", "Smackdown"),
    ("SCO-39", "Naomi", "Raw"),
    ("SCO-40", "CM Punk", "Raw"),
])
print("  Scope: 40 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Viral Shock (20 cards — Hobby/Breaker/FDI Exclusive)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Viral Shock", SCOPE_PARALLELS, [
    ("VIR-1", "John Cena", "Legend"),
    ("VIR-2", "AJ Styles", "Raw"),
    ("VIR-3", "The American Nightmare Cody Rhodes", "Smackdown"),
    ("VIR-4", "The Rock", "Legend"),
    ("VIR-5", "Mankind", "Legend"),
    ("VIR-6", "CM Punk", "Raw"),
    ("VIR-7", "Seth Rollins", "Raw"),
    ("VIR-8", "Shawn Michaels", "Legend"),
    ("VIR-9", "Undertaker", "Legend"),
    ("VIR-10", "Randy Orton", "Smackdown"),
    ("VIR-11", "Stone Cold Steve Austin", "Legend"),
    ("VIR-12", "Kofi Kingston", "Raw"),
    ("VIR-13", "Hollywood Hulk Hogan", "Legend"),
    ("VIR-14", "Kane", "Legend"),
    ("VIR-15", "Joe Hendry", "NXT"),
    ("VIR-16", "Solo Sikoa", "Smackdown"),
    ("VIR-17", "Jordynne Grace", "NXT"),
    ("VIR-18", "AJ Lee", "Raw"),
    ("VIR-19", "Roman Reigns", "Smackdown"),
    ("VIR-20", "Sami Zayn", "Smackdown"),
])
print("  Viral Shock: 20 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Women's Division (40 cards — Hobby/Breaker/FDI Exclusive)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Women's Division", SCOPE_PARALLELS, [
    ("WDV-1", "Alexa Bliss", "Smackdown"),
    ("WDV-2", "Candice LeRae", "Smackdown"),
    ("WDV-3", "Natalya", "Raw"),
    ("WDV-4", "Giulia", "Smackdown"),
    ("WDV-5", "Iyo Sky", "Raw"),
    ("WDV-6", "Jordynne Grace", "NXT"),
    ("WDV-7", "Jacy Jayne", "NXT"),
    ("WDV-8", "Lyra Valkyria", "Raw"),
    ("WDV-9", "Becky Lynch", "Raw"),
    ("WDV-10", "Liv Morgan", "Raw"),
    ("WDV-11", "Sol Ruca", "NXT"),
    ("WDV-12", "Thea Hail", "NXT"),
    ("WDV-13", "Stephanie Vaquer", "Raw"),
    ("WDV-14", "Piper Niven", "Smackdown"),
    ("WDV-15", "Bianca Belair", "Smackdown"),
    ("WDV-16", "Michin", "Smackdown"),
    ("WDV-17", "Kiana James", "Smackdown"),
    ("WDV-18", "Chelsea Green", "Smackdown"),
    ("WDV-19", "Kelani Jordan", "NXT"),
    ("WDV-20", "Izzi Dame", "NXT"),
    ("WDV-21", "Fallon Henley", "NXT"),
    ("WDV-22", "Zaria", "NXT"),
    ("WDV-23", "Tiffany Stratton", "Smackdown"),
    ("WDV-24", "Bayley", "Raw"),
    ("WDV-25", "Nikki Cross", "Smackdown"),
    ("WDV-26", "Jade Cargill", "Smackdown"),
    ("WDV-27", "Lola Vice", "NXT"),
    ("WDV-28", "Raquel Rodriguez", "Raw"),
    ("WDV-29", "Charlotte Flair", "Smackdown"),
    ("WDV-30", "Karmen Petrovic", "NXT"),
    ("WDV-31", "Jaida Parker", "NXT"),
    ("WDV-32", "Naomi", "Raw"),
    ("WDV-33", "Ivy Nile", "Raw"),
    ("WDV-34", "Roxanne Perez", "Raw"),
    ("WDV-35", "B-Fab", "Smackdown"),
    ("WDV-36", "Rhea Ripley", "Raw"),
    ("WDV-37", "Nia Jax", "Smackdown"),
    ("WDV-38", "Lash Legend", "NXT"),
    ("WDV-39", "Wren Sinclair", "NXT"),
    ("WDV-40", "Zelina Vega", "Smackdown"),
])
print("  Women's Division: 40 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Austin 3:16 (25 cards — single wrestler, Hobby/FDI Exclusive)
# ────────────────────────────────────────────────────────────────────────────────

make_single_wrestler_set("Austin 3:16", HOBBY_INSERT_PARALLELS, 25, "3:16",
                         "Stone Cold Steve Austin", "Legend")
print("  Austin 3:16: 25 cards")

# ────────────────────────────────────────────────────────────────────────────────
# The Rock Diamond Legacy (25 cards — single wrestler, Hobby/FDI Exclusive)
# ────────────────────────────────────────────────────────────────────────────────

make_single_wrestler_set("The Rock Diamond Legacy", HOBBY_INSERT_PARALLELS, 25, "RDL",
                         "The Rock", "Legend")
print("  The Rock Diamond Legacy: 25 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Platinum Punk (20 cards — single wrestler, Hobby/FDI Exclusive)
# ────────────────────────────────────────────────────────────────────────────────

make_single_wrestler_set("Platinum Punk", HOBBY_INSERT_PARALLELS, 20, "PLP",
                         "CM Punk", "Raw")
print("  Platinum Punk: 20 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Family Tree (15 cards — co_players, Hobby/FDI Exclusive)
# ────────────────────────────────────────────────────────────────────────────────

is_id = create_insert_set(set_id, "Family Tree")
for par_name, par_pr in HOBBY_INSERT_PARALLELS:
    create_parallel(is_id, par_name, par_pr)
add_multi_cards(is_id, [
    ("FAM-AC", [("CM Punk", "Raw"), ("AJ Lee", "Raw")]),
    ("FAM-BA", [("Berto", "Smackdown"), ("Angel", "Smackdown")]),
    ("FAM-CB", [("Brandi Rhodes", "Legend"), ("The American Nightmare Cody Rhodes", "Smackdown")]),
    ("FAM-GL", [("Johnny Gargano", "Smackdown"), ("Candice LeRae", "Smackdown")]),
    ("FAM-HM", [("Stephanie McMahon", "Legend"), ("Triple H", "Legend")]),
    ("FAM-HN", [("Bret Hit Man Hart", "Legend"), ("Natalya", "Raw")]),
    ("FAM-JN", [("Jimmy Uso", "Smackdown"), ("Naomi", "Raw")]),
    ("FAM-JR", [("Rocky Johnson", "Legend"), ("The Rock", "Legend")]),
    ("FAM-ML", [("Jerry The King Lawler", "Legend"), ("The Honky Tonk Man", "Legend")]),
    ("FAM-RD", [("William Regal", "Legend"), ("Charlie Dempsey", "NXT")]),
    ("FAM-RL", [("Becky Lynch", "Raw"), ("Seth Rollins", "Raw")]),
    ("FAM-RS", [("Solo Sikoa", "Smackdown"), ("Rikishi", "Legend")]),
    ("FAM-SS", [("Scott Steiner", "Legend"), ("Rick Steiner", "Legend")]),
    ("FAM-TR", [("Stevie Ray", "Legend"), ("Booker T", "Legend")]),
    ("FAM-UM", [("Michelle McCool", "Legend"), ("Undertaker", "Legend")]),
])
print("  Family Tree: 15 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Embedded (15 cards — Hobby/FDI Exclusive)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Embedded", HOBBY_INSERT_PARALLELS, [
    ("EMB-1", "Triple H", "Legend"),
    ("EMB-2", "Michelle McCool", "Legend"),
    ("EMB-3", "Lex Luger", "Legend"),
    ("EMB-4", "Typhoon", "Legend"),
    ("EMB-5", "Earthquake", "Legend"),
    ("EMB-6", "Bret Hit Man Hart", "Legend"),
    ("EMB-7", "Stone Cold Steve Austin", "Legend"),
    ("EMB-8", "Bull Nakano", "Legend"),
    ("EMB-9", "Paul Heyman", "Smackdown"),
    ("EMB-10", "Mike Rotunda", "Legend"),
    ("EMB-11", "Great Muta", "Legend"),
    ("EMB-12", "Rick Steiner", "Legend"),
    ("EMB-13", "Scott Steiner", "Legend"),
    ("EMB-14", "Rob Van Dam", "Legend"),
    ("EMB-15", "Bret Hit Man Hart", "Legend"),
])
print("  Embedded: 15 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Wrestlemania Recall (15 cards — Retail Exclusive)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Wrestlemania Recall", RETAIL_INSERT_PARALLELS, [
    ("WMR-1", "Don Muraco", "Legend"),
    ("WMR-2", "Mr. Fuji", "Legend"),
    ("WMR-3", "George The Animal Steele", "Legend"),
    ("WMR-4", "Jake The Snake Roberts", "Legend"),
    ("WMR-5", "Mr. Wonderful Paul Orndorff", "Legend"),
    ("WMR-6", "Nikolai Volkoff", "Legend"),
    ("WMR-7", "Big John Studd", "Legend"),
    ("WMR-8", "Hillbilly Jim", "Legend"),
    ("WMR-9", "Bruno Sammartino", "Legend"),
    ("WMR-10", "Brutus Beefcake", "Legend"),
    ("WMR-11", "British Bulldog", "Legend"),
    ("WMR-12", "Tito Santana", "Legend"),
    ("WMR-13", "Junkyard Dog", "Legend"),
    ("WMR-14", "King Kong Bundy", "Legend"),
    ("WMR-15", "Hulk Hogan", "Legend"),
])
print("  Wrestlemania Recall: 15 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Eras of Excellence (40 cards — Retail Exclusive)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Eras of Excellence", RETAIL_INSERT_PARALLELS, [
    ("ERA-1", "The Miz", "Smackdown"),
    ("ERA-2", "Hulk Hogan", "Legend"),
    ("ERA-3", "Kofi Kingston", "Raw"),
    ("ERA-4", "Rey Mysterio", "Raw"),
    ("ERA-5", "Natalya", "Raw"),
    ("ERA-6", "Sheamus", "Raw"),
    ("ERA-7", "Shawn Michaels", "Legend"),
    ("ERA-8", "Kane", "Legend"),
    ("ERA-9", "The American Nightmare Cody Rhodes", "Smackdown"),
    ("ERA-10", "Charlotte Flair", "Smackdown"),
    ("ERA-11", "Seth Rollins", "Raw"),
    ("ERA-12", "The Rock", "Legend"),
    ("ERA-13", "Undertaker", "Legend"),
    ("ERA-14", "John Cena", "Legend"),
    ("ERA-15", "Randy Orton", "Smackdown"),
    ("ERA-16", "Sami Zayn", "Smackdown"),
    ("ERA-17", "Kevin Owens", "Smackdown"),
    ("ERA-18", "Roman Reigns", "Smackdown"),
    ("ERA-19", "Finn Bálor", "Raw"),
    ("ERA-20", "Jey Uso", "Raw"),
    ("ERA-21", "Bret Hit Man Hart", "Legend"),
    ("ERA-22", "CM Punk", "Raw"),
    ("ERA-23", "Bray Wyatt", "Legend"),
    ("ERA-24", "Triple H", "Legend"),
    ("ERA-25", "Chyna", "Legend"),
    ("ERA-26", "AJ Styles", "Raw"),
    ("ERA-27", "Rhea Ripley", "Raw"),
    ("ERA-28", "R-Truth", "Smackdown"),
    ("ERA-29", "Rusev", "Raw"),
    ("ERA-30", "Rowdy Roddy Piper", "Legend"),
    ("ERA-31", "Naomi", "Raw"),
    ("ERA-32", "Drew McIntyre", "Smackdown"),
    ("ERA-33", "Becky Lynch", "Raw"),
    ("ERA-34", "Shinsuke Nakamura", "Smackdown"),
    ("ERA-35", "Trish Stratus", "Legend"),
    ("ERA-36", "Kurt Angle", "Legend"),
    ("ERA-37", "Alexa Bliss", "Smackdown"),
    ("ERA-38", "Batista", "Legend"),
    ("ERA-39", "Bayley", "Raw"),
    ("ERA-40", "Stone Cold Steve Austin", "Legend"),
])
print("  Eras of Excellence: 40 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Focus Reel (40 cards — Retail Exclusive)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Focus Reel", RETAIL_INSERT_PARALLELS, [
    ("FR-1", "Ricky Saints", "NXT"),
    ("FR-2", "Izzi Dame", "NXT"),
    ("FR-3", "Roxanne Perez", "Raw"),
    ("FR-4", "Chelsea Green", "Smackdown"),
    ("FR-5", "Solo Sikoa", "Smackdown"),
    ("FR-6", "LA Knight", "Raw"),
    ("FR-7", "Carmelo Hayes", "Smackdown"),
    ("FR-8", "Rey Fenix", "Smackdown"),
    ("FR-9", "Je'Von Evans", "NXT"),
    ("FR-10", "Chad Gable", "Raw"),
    ("FR-11", "Shawn Spears", "NXT"),
    ("FR-12", "Lyra Valkyria", "Raw"),
    ("FR-13", "Bronson Reed", "Raw"),
    ("FR-14", "Fallon Henley", "NXT"),
    ("FR-15", "Oba Femi", "NXT"),
    ("FR-16", "Candice LeRae", "Smackdown"),
    ("FR-17", "Ludwig Kaiser", "Raw"),
    ("FR-18", "Liv Morgan", "Raw"),
    ("FR-19", "Tiffany Stratton", "Smackdown"),
    ("FR-20", "Jordynne Grace", "NXT"),
    ("FR-21", "Nikki Bella", "Raw"),
    ("FR-22", "Zaria", "NXT"),
    ("FR-23", "Stephanie Vaquer", "Raw"),
    ("FR-24", "Montez Ford", "Smackdown"),
    ("FR-25", "Alex Shelley", "Smackdown"),
    ("FR-26", "Lash Legend", "NXT"),
    ("FR-27", "Aleister Black", "Smackdown"),
    ("FR-28", "Chris Sabin", "Smackdown"),
    ("FR-29", "Rhea Ripley", "Raw"),
    ("FR-30", "Damian Priest", "Smackdown"),
    ("FR-31", "Santos Escobar", "Smackdown"),
    ("FR-32", "Giulia", "Smackdown"),
    ("FR-33", "Bron Breakker", "Raw"),
    ("FR-34", "Iyo Sky", "Raw"),
    ("FR-35", "JD McDonagh", "Raw"),
    ("FR-36", "Dragon Lee", "Raw"),
    ("FR-37", "Johnny Gargano", "Smackdown"),
    ("FR-38", "Angelo Dawkins", "Smackdown"),
    ("FR-39", "Brock Lesnar", "WWE"),
    ("FR-40", "Tommaso Ciampa", "Smackdown"),
])
print("  Focus Reel: 40 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Signalz (30 cards — no parallels)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Signalz", [], [
    ("SGZ-1", "Roman Reigns", "Smackdown"),
    ("SGZ-2", "Shawn Michaels", "Legend"),
    ("SGZ-3", "The American Nightmare Cody Rhodes", "Smackdown"),
    ("SGZ-4", "Undertaker", "Legend"),
    ("SGZ-5", "Shinsuke Nakamura", "Smackdown"),
    ("SGZ-6", "Finn Bálor", "Raw"),
    ("SGZ-7", "Triple H", "Legend"),
    ("SGZ-8", "AJ Lee", "Raw"),
    ("SGZ-9", "Seth Rollins", "Raw"),
    ("SGZ-10", "Rhea Ripley", "Raw"),
    ("SGZ-11", "Bronson Reed", "Raw"),
    ("SGZ-12", "Stone Cold Steve Austin", "Legend"),
    ("SGZ-13", "Kevin Owens", "Smackdown"),
    ("SGZ-14", "Jacob Fatu", "Smackdown"),
    ("SGZ-15", "Randy Orton", "Smackdown"),
    ("SGZ-16", "Sheamus", "Raw"),
    ("SGZ-17", "Jimmy Uso", "Smackdown"),
    ("SGZ-18", "AJ Styles", "Raw"),
    ("SGZ-19", "Solo Sikoa", "Smackdown"),
    ("SGZ-20", "Iyo Sky", "Raw"),
    ("SGZ-21", "Tiffany Stratton", "Smackdown"),
    ("SGZ-22", "John Cena", "Legend"),
    ("SGZ-23", "Drew McIntyre", "Smackdown"),
    ("SGZ-24", "Sami Zayn", "Smackdown"),
    ("SGZ-25", "Penta", "Raw"),
    ("SGZ-26", "Bron Breakker", "Raw"),
    ("SGZ-27", "CM Punk", "Raw"),
    ("SGZ-28", "Stephanie Vaquer", "Raw"),
    ("SGZ-29", "Gunther", "Raw"),
    ("SGZ-30", "Jey Uso", "Raw"),
])
print("  Signalz: 30 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Gamut (20 cards — no parallels)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Gamut", [], [
    ("GAM-1", "Alexa Bliss", "Smackdown"),
    ("GAM-2", "Bayley", "Raw"),
    ("GAM-3", "Bianca Belair", "Smackdown"),
    ("GAM-4", "Bron Breakker", "Raw"),
    ("GAM-5", "CM Punk", "Raw"),
    ("GAM-6", "The American Nightmare Cody Rhodes", "Smackdown"),
    ("GAM-7", "Damian Priest", "Smackdown"),
    ("GAM-8", "Drew McIntyre", "Smackdown"),
    ("GAM-9", "Finn Bálor", "Raw"),
    ("GAM-10", "Jacob Fatu", "Smackdown"),
    ("GAM-11", "Jey Uso", "Raw"),
    ("GAM-12", "John Cena", "Legend"),
    ("GAM-13", "Kevin Owens", "Smackdown"),
    ("GAM-14", "Liv Morgan", "Raw"),
    ("GAM-15", "Penta", "Raw"),
    ("GAM-16", "Randy Orton", "Smackdown"),
    ("GAM-17", "Roman Reigns", "Smackdown"),
    ("GAM-18", "Seth Rollins", "Raw"),
    ("GAM-19", "Tiffany Stratton", "Smackdown"),
    ("GAM-20", "The Rock", "Legend"),
])
print("  Gamut: 20 cards")

# ────────────────────────────────────────────────────────────────────────────────
# House of Cards (20 cards — Hobby Exclusive, no parallels)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("House of Cards", [], [
    ("HOC-1", "Brock Lesnar", "WWE"),
    ("HOC-2", "Seth Rollins", "Raw"),
    ("HOC-3", "Jacob Fatu", "Smackdown"),
    ("HOC-4", "The American Nightmare Cody Rhodes", "Smackdown"),
    ("HOC-5", "Alexa Bliss", "Smackdown"),
    ("HOC-6", "Tiffany Stratton", "Smackdown"),
    ("HOC-7", "Becky Lynch", "Raw"),
    ("HOC-8", "Gunther", "Raw"),
    ("HOC-9", "CM Punk", "Raw"),
    ("HOC-10", "Sheamus", "Raw"),
    ("HOC-11", "Jade Cargill", "Smackdown"),
    ("HOC-12", "Rhea Ripley", "Raw"),
    ("HOC-13", "Bianca Belair", "Smackdown"),
    ("HOC-14", "Nia Jax", "Smackdown"),
    ("HOC-15", "Zelina Vega", "Smackdown"),
    ("HOC-16", "Drew McIntyre", "Smackdown"),
    ("HOC-17", "Charlotte Flair", "Smackdown"),
    ("HOC-18", "Iyo Sky", "Raw"),
    ("HOC-19", "The Miz", "Smackdown"),
    ("HOC-20", "Randy Orton", "Smackdown"),
])
print("  House of Cards: 20 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Helix (7 cards)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Helix", HELIX_PARALLELS, [
    ("HLX-1", "Seth Rollins", "Raw"),
    ("HLX-2", "Jacob Fatu", "Smackdown"),
    ("HLX-3", "John Cena", "Legend"),
    ("HLX-4", "Roman Reigns", "Smackdown"),
    ("HLX-5", "Stephanie Vaquer", "Raw"),
    ("HLX-6", "Brock Lesnar", "WWE"),
    ("HLX-7", "Joe Hendry", "NXT"),
])
print("  Helix: 7 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Let's Go (5 cards)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Let's Go", HELIX_PARALLELS, [
    ("LG-1", "Jacob Fatu", "Smackdown"),
    ("LG-2", "LA Knight", "Raw"),
    ("LG-3", "Rhea Ripley", "Raw"),
    ("LG-4", "Bianca Belair", "Smackdown"),
    ("LG-5", "Penta", "Raw"),
])
print("  Let's Go: 5 cards")

# ────────────────────────────────────────────────────────────────────────────────
# Feel The Pop! (5 cards — Hobby/FDI Exclusive, no parallels)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("Feel The Pop!", [], [
    ("FTP-CM", "CM Punk", "Raw"),
    ("FTP-CR", "The American Nightmare Cody Rhodes", "Smackdown"),
    ("FTP-RR", "Roman Reigns", "Smackdown"),
    ("FTP-RY", "Rhea Ripley", "Raw"),
    ("FTP-UT", "Undertaker", "Legend"),
])
print("  Feel The Pop!: 5 cards")

# ────────────────────────────────────────────────────────────────────────────────
# GPK (25 cards)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("GPK", GPK_PARALLELS, [
    ("GPK-AB", "Unstitched Bliss", "Alexa Bliss", "Smackdown"),
    ("GPK-BB", "Braid-est Bianca", "Bianca Belair", "Smackdown"),
    ("GPK-BL", "Bad Girl Bayley", "Bayley", "Raw"),
    ("GPK-CG", "Chelsea Shhhush!", "Chelsea Green", "Smackdown"),
    ("GPK-CM", "Potty Mouth Punk", "CM Punk", "Raw"),
    ("GPK-CR", "Cody Bomb", "The American Nightmare Cody Rhodes", "Smackdown"),
    ("GPK-DK", "Dirty Dominik", "Dominik Mysterio", "Raw"),
    ("GPK-DM", "Drafty Drew", "Drew McIntyre", "Smackdown"),
    ("GPK-DP", "Damaged Damian", "Damian Priest", "Smackdown"),
    ("GPK-IY", "Soaring Sky", "Iyo Sky", "Raw"),
    ("GPK-JC", "John See? Nah!", "John Cena", "Legend"),
    ("GPK-JF", "Feral Fatu", "Jacob Fatu", "Smackdown"),
    ("GPK-JU", "Jey Yeesh!", "Jey Uso", "Raw"),
    ("GPK-LA", "Boogie Knight", "LA Knight", "Raw"),
    ("GPK-LM", "Liv It Up", "Liv Morgan", "Raw"),
    ("GPK-LV", "Ladybird Lyra", "Lyra Valkyria", "Raw"),
    ("GPK-LY", "Disarm Her Becky", "Becky Lynch", "Raw"),
    ("GPK-PT", "Pop-Out Penta", "Penta", "Raw"),
    ("GPK-RH", "Ripped Rhea", "Rhea Ripley", "Raw"),
    ("GPK-RO", "Reptilian Randy", "Randy Orton", "Smackdown"),
    ("GPK-RP", "Popped Roxanne", "Roxanne Perez", "Raw"),
    ("GPK-RR", "Roman Empire", "Roman Reigns", "Smackdown"),
    ("GPK-SR", "Supersized Seth", "Seth Rollins", "Raw"),
    ("GPK-TR", "Finally! The Rock (Has Come Back to GPK!)", "The Rock", "Legend"),
    ("GPK-TS", "Tiffany Time", "Tiffany Stratton", "Smackdown"),
], is_gpk=True)
print("  GPK: 25 cards")

# ────────────────────────────────────────────────────────────────────────────────
# 2025 Topps Chrome Buybacks (2 cards)
# ────────────────────────────────────────────────────────────────────────────────

make_insert_set("2025 Topps Chrome Buybacks", BUYBACK_PARALLELS, [
    ("106", "Jey Uso", "Raw"),
    ("182", "Tiffany Stratton", "Smackdown"),
])
print("  2025 Topps Chrome Buybacks: 2 cards")

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
        unique_cards += 1  # The base card itself

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

cur.execute(
    "SELECT COUNT(*) FROM insert_sets WHERE set_id = ?", (set_id,)
)
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
