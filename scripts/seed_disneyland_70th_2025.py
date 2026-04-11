"""
Seed script: 2025 Topps Disneyland 70th Anniversary
Inserts all data into the local SQLite database (the-c-list.db).
Usage: python3 scripts/seed_disneyland_70th_2025.py
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

def create_appearance(player_id, insert_set_id, card_number, is_rookie=False, team=None):
    cur.execute(
        "INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)",
        (player_id, insert_set_id, card_number, int(is_rookie), team),
    )
    return cur.lastrowid

def add_cards(insert_set_id, cards):
    """cards = [(card_number, name), ...] or [(card_number, name, team), ...]"""
    for item in cards:
        if len(item) == 3:
            card_number, name, team = item
        else:
            card_number, name = item
            team = None
        player_id = get_or_create_player(set_id, name)
        create_appearance(player_id, insert_set_id, card_number, False, team)

def make_insert_set(name, parallels_def, cards):
    is_id = create_insert_set(set_id, name)
    for par_name, par_pr in parallels_def:
        create_parallel(is_id, par_name, par_pr)
    add_cards(is_id, cards)
    return is_id

# ─── 1. Create the set ─────────────────────────────────────────────────────────

SET_NAME = "2025 Topps Disneyland 70th Anniversary"

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
        "autos_per_box": None,
        "rainbow_parallels_per_box": 6,
        "numbered_parallels_per_box": 2,
        "inserts_per_box": 8,
    },
    "value": {
        "cards_per_pack": 5,
        "packs_per_box": 7,
        "boxes_per_case": 40,
        "autos_per_box": None,
        "pink_shimmer_per_box": 2,
        "rainbow_parallels_per_box": 2,
        "inserts_per_box": 2,
    },
}

pack_odds = {
    "hobby": {
        "Base Set": "1:1",
        "Base Set Rainbow Foil": "1:2",
        "Base Set Green Foil": "1:21",
        "Base Set Aqua Electric Dots Foil": "1:27",
        "Base Set Blue Foil": "1:42",
        "Base Set 70th Anniversary Foil": "1:60",
        "Base Set Gold Foil": "1:79",
        "Base Set Orange Foil": "1:157",
        "Base Set Black Foil": "1:392",
        "Base Set Red Foil": "1:785",
        "Base Set Foilfractor": "1:3,942",
        "Base Set Variation Hidden Mickey": "1:72",
        "1954 Topps Disneyland On Wheels": "1:3",
        "1954 Topps Disneyland On Wheels Gold Foil": "1:471",
        "1954 Topps Disneyland On Wheels Orange Foil": "1:938",
        "1954 Topps Disneyland On Wheels Black Foil": "1:2,358",
        "1954 Topps Disneyland On Wheels Red Foil": "1:4,672",
        "1954 Topps Disneyland On Wheels Foilfractor": "1:24,028",
        "1955 Topps Disneyland Icons": "1:3",
        "1955 Topps Disneyland Icons Gold Foil": "1:453",
        "1955 Topps Disneyland Icons Orange Foil": "1:905",
        "1955 Topps Disneyland Icons Black Foil": "1:2,263",
        "1955 Topps Disneyland Icons Red Foil": "1:4,546",
        "From Silver Screen To Main Street": "1:3",
        "From Silver Screen To Main Street Gold Foil": "1:471",
        "From Silver Screen To Main Street Orange Foil": "1:938",
        "From Silver Screen To Main Street Black Foil": "1:2,358",
        "From Silver Screen To Main Street Red Foil": "1:4,672",
        "From Silver Screen To Main Street Foilfractor": "1:24,028",
        "Posters": "1:9",
        "Posters PETG Variation": "1:764",
        "Posters Gold Foil": "1:840",
        "Posters Orange Foil": "1:1,682",
        "Posters Black Foil": "1:4,205",
        "Posters Red Foil": "1:8,272",
        "Posters Foilfractor": "1:42,048",
        "The Lands": "1:12",
        "The Lands Gold Foil": "1:1,177",
        "The Lands Orange Foil": "1:2,358",
        "The Lands Black Foil": "1:5,937",
        "1977 Topps Star Tours Chrome": "1:520",
        "1977 Topps Star Tours Chrome Orange Wave Refractor": "1:1,809",
        "1977 Topps Star Tours Chrome Black Refractor": "1:4,546",
        "1977 Topps Star Tours Chrome Red Refractor": "1:9,011",
        "A Pirate's Life Chrome": "1:876",
        "A Pirate's Life Chrome Orange Wave Refractor": "1:2,358",
        "A Pirate's Life Chrome Black Refractor": "1:5,937",
        "Eighth Wonder Chrome": "1:1,530",
        "Eighth Wonder Chrome Orange Wave Refractor": "1:3,364",
        "Eighth Wonder Chrome Black Refractor": "1:8,272",
        "Entrance To Magic Chrome": "1:144",
        "Entrance To Magic Chrome Orange Wave Refractor": "1:24,028",
        "Greetings From The Tiki Room Chrome": "1:2,336",
        "Greetings From The Tiki Room Chrome Orange Wave Refractor": "1:5,937",
        "It's A Small World Chrome": "1:636",
        "It's A Small World Chrome Orange Wave Refractor": "1:1,682",
        "It's A Small World Chrome Black Refractor": "1:4,205",
        "It's A Small World Chrome Red Refractor": "1:8,272",
        "It's A Small World Chrome Superfractor": "1:42,048",
        "Tomorrowland Cosmic Chrome": "1:545",
        "Tomorrowland Cosmic Chrome Orange Wave Refractor": "1:1,682",
        "Tomorrowland Cosmic Chrome Black Refractor": "1:4,205",
        "Tomorrowland Cosmic Chrome Red Refractor": "1:8,272",
        "Tomorrowland Cosmic Chrome Superfractor": "1:42,048",
        "Welcome Foolish Mortals Chrome": "1:2,121",
        "Character Nametags": "1:840",
        "Collector's Pin Relic Redemption": "1:12,307",
        "Collector's Pin Relic Redemption Red Foil": "1:168,192",
        "Enchanted Relics": "1:274",
        "Enchanted Relics 70th Anniversary Foil": "1:347",
        "Enchanted Relics Gold Foil": "1:873",
        "Enchanted Relics Orange Foil": "1:944",
        "Enchanted Relics Black Foil": "1:2,130",
        "Enchanted Relics Red Foil": "1:4,241",
        "Enchanted Relics Foilfractor": "1:18,688",
        "Attraction Autographs": "1:237",
        "Attraction Autographs 70th Anniversary Foil": "1:719",
        "Attraction Autographs Gold Foil": "1:1,142",
        "Attraction Autographs Orange Foil": "1:2,011",
        "Attraction Autographs Black Foil": "1:4,761",
        "Attraction Autographs Red Foil": "1:9,011",
        "Attraction Autographs Foilfractor": "1:45,871",
        "1955 Topps Disneyland Icons Autographs": "1:389",
        "1955 Topps Disneyland Icons Autographs 70th Anniversary Foil": "1:1,020",
        "1955 Topps Disneyland Icons Autographs Gold Foil": "1:1,222",
        "1955 Topps Disneyland Icons Autographs Orange Foil": "1:2,139",
        "1955 Topps Disneyland Icons Autographs Black Foil": "1:4,996",
        "1955 Topps Disneyland Icons Autographs Red Foil": "1:9,521",
        "1955 Topps Disneyland Icons Autographs Foilfractor": "1:45,871",
        "Sketch Cards": "1:171",
    },
    "value": {
        "Base Set": "1:1",
        "Base Set Rainbow Foil": "2:7",
        "Base Set Pink Shimmer Foil": "2:7",
        "Base Set Green Foil": "1:487",
        "Base Set Aqua Electric Dots Foil": "1:646",
        "Base Set Blue Foil": "1:979",
        "Base Set 70th Anniversary Foil": "1:1,383",
        "Base Set Gold Foil": "1:1,937",
        "Base Set Orange Foil": "1:3,873",
        "Base Set Black Foil": "1:9,667",
        "Base Set Red Foil": "1:19,468",
        "Base Set Foilfractor": "1:100,120",
        "Base Set Variation Hidden Mickey": "1:1,761",
        "1954 Topps Disneyland On Wheels": "1:7",
        "1954 Topps Disneyland On Wheels Gold Foil": "1:11,585",
        "1954 Topps Disneyland On Wheels Orange Foil": "1:23,362",
        "1954 Topps Disneyland On Wheels Black Foil": "1:58,404",
        "1954 Topps Disneyland On Wheels Red Foil": "1:116,807",
        "1954 Topps Disneyland On Wheels Foilfractor": "1:700,840",
        "1955 Topps Disneyland Icons": "1:7",
        "1955 Topps Disneyland Icons Gold Foil": "1:11,214",
        "1955 Topps Disneyland Icons Orange Foil": "1:22,249",
        "1955 Topps Disneyland Icons Black Foil": "1:56,068",
        "1955 Topps Disneyland Icons Red Foil": "1:107,822",
        "From Silver Screen To Main Street": "1:7",
        "From Silver Screen To Main Street Gold Foil": "1:11,585",
        "From Silver Screen To Main Street Orange Foil": "1:23,362",
        "From Silver Screen To Main Street Black Foil": "1:58,404",
        "From Silver Screen To Main Street Red Foil": "1:116,807",
        "From Silver Screen To Main Street Foilfractor": "1:700,840",
        "Posters": "1:21",
        "Posters PETG Variation": "1:18,942",
        "Posters Gold Foil": "1:20,921",
        "Posters Orange Foil": "1:41,226",
        "Posters Black Foil": "1:100,120",
        "Posters Red Foil": "1:233,614",
        "Posters Foilfractor": "1:1,401,680",
        "The Lands": "1:28",
        "The Lands Gold Foil": "1:29,202",
        "The Lands Orange Foil": "1:58,404",
        "The Lands Black Foil": "1:140,168",
        "1977 Topps Star Tours Chrome": "1:12,860",
        "1977 Topps Star Tours Chrome Orange Wave Refractor": "1:45,216",
        "1977 Topps Star Tours Chrome Black Refractor": "1:107,822",
        "1977 Topps Star Tours Chrome Red Refractor": "1:233,614",
        "A Pirate's Life Chrome": "1:21,565",
        "A Pirate's Life Chrome Orange Wave Refractor": "1:58,404",
        "A Pirate's Life Chrome Black Refractor": "1:140,168",
        "Eighth Wonder Chrome": "1:37,884",
        "Eighth Wonder Chrome Orange Wave Refractor": "1:82,452",
        "Eighth Wonder Chrome Black Refractor": "1:233,614",
        "Entrance To Magic Chrome": "1:560",
        "Entrance To Magic Chrome Orange Wave Refractor": "1:700,840",
        "Greetings From The Tiki Room Chrome": "1:58,404",
        "Greetings From The Tiki Room Chrome Orange Wave Refractor": "1:140,168",
        "It's A Small World Chrome": "1:15,750",
        "It's A Small World Chrome Orange Wave Refractor": "1:41,226",
        "It's A Small World Chrome Black Refractor": "1:100,120",
        "It's A Small World Chrome Red Refractor": "1:233,614",
        "It's A Small World Chrome Superfractor": "1:1,401,680",
        "Tomorrowland Cosmic Chrome": "1:13,478",
        "Tomorrowland Cosmic Chrome Orange Wave Refractor": "1:41,226",
        "Tomorrowland Cosmic Chrome Black Refractor": "1:100,120",
        "Tomorrowland Cosmic Chrome Red Refractor": "1:233,614",
        "Tomorrowland Cosmic Chrome Superfractor": "1:1,401,680",
        "Welcome Foolish Mortals Chrome": "1:53,911",
        "Character Nametags": "1:20,921",
        "Collector's Pin Relic Redemption": "1:77,872",
        "Collector's Pin Relic Redemption Red Foil": "1:1,401,680",
        "Enchanted Relics": "1:1,689",
        "Enchanted Relics 70th Anniversary Foil": "1:2,137",
        "Enchanted Relics Gold Foil": "1:5,392",
        "Enchanted Relics Orange Foil": "1:5,817",
        "Enchanted Relics Black Foil": "1:13,100",
        "Enchanted Relics Red Foil": "1:26,447",
        "Enchanted Relics Foilfractor": "1:116,807",
        "Attraction Autographs": "1:1,462",
        "Attraction Autographs 70th Anniversary Foil": "1:4,436",
        "Attraction Autographs Gold Foil": "1:7,044",
        "Attraction Autographs Orange Foil": "1:12,405",
        "Attraction Autographs Black Foil": "1:29,202",
        "Attraction Autographs Red Foil": "1:56,068",
        "Attraction Autographs Foilfractor": "1:280,336",
        "1955 Topps Disneyland Icons Autographs": "1:2,397",
        "1955 Topps Disneyland Icons Autographs 70th Anniversary Foil": "1:6,286",
        "1955 Topps Disneyland Icons Autographs Gold Foil": "1:7,536",
        "1955 Topps Disneyland Icons Autographs Orange Foil": "1:13,224",
        "1955 Topps Disneyland Icons Autographs Black Foil": "1:30,472",
        "1955 Topps Disneyland Icons Autographs Red Foil": "1:58,404",
        "1955 Topps Disneyland Icons Autographs Foilfractor": "1:280,336",
    },
    "disneyland_exclusive": {
        "Base Set": "1:1",
        "Base Set Rainbow Foil": "1:2",
        "Base Set Purple Glitter Foil": "1:5",
        "Base Set Green Foil": "1:128",
        "Base Set Aqua Electric Dots Foil": "1:141",
        "Base Set Blue Foil": "1:157",
        "Base Set 70th Anniversary Foil": "1:168",
        "Base Set Gold Confetti Foil": "1:13",
        "Base Set Gold Foil": "1:1,397",
        "Base Set Orange Foil": "1:2,794",
        "Base Set Black Foil": "1:7,183",
        "Base Set Red Foil": "1:12,570",
        "Base Set Foilfractor": "1:50,280",
        "Base Set Variation Hidden Mickey": "1:1,257",
        "Base Set Variation Red/White Bulb": "1:140",
        "1954 Topps Disneyland On Wheels": "1:3",
        "1954 Topps Disneyland On Wheels Gold Confetti Foil": "1:76",
        "1954 Topps Disneyland On Wheels Gold Foil": "1:8,380",
        "1954 Topps Disneyland On Wheels Orange Foil": "1:16,760",
        "1954 Topps Disneyland On Wheels Black Foil": "1:33,520",
        "1954 Topps Disneyland On Wheels Red Foil": "1:100,560",
        "1954 Topps Disneyland On Wheels Foilfractor": "1:100,560",
        "1955 Topps Disneyland Icons": "1:3",
        "1955 Topps Disneyland Icons Gold Confetti Foil": "1:73",
        "1955 Topps Disneyland Icons Gold Foil": "1:7,736",
        "1955 Topps Disneyland Icons Orange Foil": "1:16,760",
        "1955 Topps Disneyland Icons Black Foil": "1:33,520",
        "1955 Topps Disneyland Icons Red Foil": "1:100,560",
        "From Silver Screen To Main Street": "1:3",
        "From Silver Screen To Main Street Gold Confetti Foil": "1:76",
        "From Silver Screen To Main Street Gold Foil": "1:8,380",
        "From Silver Screen To Main Street Orange Foil": "1:16,760",
        "From Silver Screen To Main Street Black Foil": "1:33,520",
        "From Silver Screen To Main Street Red Foil": "1:100,560",
        "From Silver Screen To Main Street Foilfractor": "1:100,560",
        "Posters": "1:8",
        "Posters Gold Confetti Foil": "1:136",
        "Posters Gold Foil": "1:14,366",
        "Posters Orange Foil": "1:33,520",
        "Posters Black Foil": "1:100,560",
        "Posters Red Foil": "1:100,560",
        "Posters Foilfractor": "1:100,560",
        "Posters PETG Variation": "1:12,570",
        "The Lands": "1:10",
        "The Lands Gold Confetti Foil": "1:190",
        "The Lands Gold Foil": "1:20,112",
        "The Lands Orange Foil": "1:33,520",
        "The Lands Black Foil": "1:100,560",
        "1977 Topps Star Tours Chrome": "1:9,142",
        "1977 Topps Star Tours Chrome Orange Wave Refractor": "1:25,140",
        "1977 Topps Star Tours Chrome Black Refractor": "1:100,560",
        "1977 Topps Star Tours Chrome Red Refractor": "1:100,560",
        "A Pirate's Life Chrome": "1:16,760",
        "A Pirate's Life Chrome Orange Wave Refractor": "1:33,520",
        "A Pirate's Life Chrome Black Refractor": "1:100,560",
        "Eighth Wonder Chrome": "1:25,140",
        "Eighth Wonder Chrome Orange Wave Refractor": "1:50,280",
        "Eighth Wonder Chrome Black Refractor": "1:100,560",
        "Entrance To Magic Chrome": "1:120",
        "Entrance To Magic Chrome Orange Wave Refractor": "1:100,560",
        "Greetings From The Tiki Room Chrome": "1:33,520",
        "Greetings From The Tiki Room Chrome Orange Wave Refractor": "1:100,560",
        "Happy Haunts Chrome": "1:76",
        "Happy Haunts Chrome Black Refractor": "1:745",
        "Happy Haunts Chrome Red Refractor": "1:1,479",
        "Happy Haunts Chrome Superfractor": "1:7,183",
        "It's A Small World Chrome": "1:11,174",
        "It's A Small World Chrome Orange Wave Refractor": "1:33,520",
        "It's A Small World Chrome Black Refractor": "1:100,560",
        "It's A Small World Chrome Red Refractor": "1:100,560",
        "It's A Small World Chrome Superfractor": "1:100,560",
        "Tomorrowland Cosmic Chrome": "1:9,142",
        "Tomorrowland Cosmic Chrome Orange Wave Refractor": "1:33,520",
        "Tomorrowland Cosmic Chrome Black Refractor": "1:100,560",
        "Tomorrowland Cosmic Chrome Red Refractor": "1:100,560",
        "Tomorrowland Cosmic Chrome Superfractor": "1:100,560",
        "Unsigned On-Site Autographs": "1:10",
        "Unsigned On-Site Autographs 70th Anniversary Foil": "1:40",
        "Unsigned On-Site Autographs Gold Foil": "1:55",
        "Unsigned On-Site Autographs Orange Foil": "1:110",
        "Unsigned On-Site Autographs Black Foil": "1:275",
        "Unsigned On-Site Autographs Red Foil": "1:550",
        "Unsigned On-Site Autographs Foilfractor": "1:2,718",
        "Welcome Foolish Mortals Chrome": "1:33,520",
        "Character Nametags": "1:14,366",
        "Collector's Pin Relic Redemption": "1:12,570",
        "Collector's Pin Relic Redemption Red Foil": "1:100,560",
        "Enchanted Relics": "1:270",
        "Enchanted Relics 70th Anniversary Foil": "1:341",
        "Enchanted Relics Gold Confetti Foil": "1:107",
        "Enchanted Relics Gold Foil": "1:860",
        "Enchanted Relics Orange Foil": "1:932",
        "Enchanted Relics Black Foil": "1:2,095",
        "Enchanted Relics Red Foil": "1:4,190",
        "Enchanted Relics Foilfractor": "1:20,112",
        "Attraction Autographs": "1:234",
        "Attraction Autographs 70th Anniversary Foil": "1:709",
        "Attraction Autographs Gold Foil": "1:1,118",
        "Attraction Autographs Orange Foil": "1:1,972",
        "Attraction Autographs Black Foil": "1:4,571",
        "Attraction Autographs Red Foil": "1:8,380",
        "Attraction Autographs Foilfractor": "1:33,520",
        "1955 Topps Disneyland Icons Autographs": "1:383",
        "1955 Topps Disneyland Icons Autographs 70th Anniversary Foil": "1:1,006",
        "1955 Topps Disneyland Icons Autographs Gold Foil": "1:1,198",
        "1955 Topps Disneyland Icons Autographs Orange Foil": "1:2,095",
        "1955 Topps Disneyland Icons Autographs Black Foil": "1:5,028",
        "1955 Topps Disneyland Icons Autographs Red Foil": "1:9,142",
        "1955 Topps Disneyland Icons Autographs Foilfractor": "1:50,280",
        "Sketch Cards": "1:503",
    },
}

cur.execute(
    "INSERT INTO sets (name, sport, season, league, tier, box_config, release_date, pack_odds) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    (SET_NAME, "Entertainment", "2025", "Disney", "Standard", json.dumps(box_config), "2026-03-13", json.dumps(pack_odds)),
)
set_id = cur.lastrowid
print(f"Created set '{SET_NAME}' with id {set_id}")

# ─── 2. Parallel definitions ─────────────────────────────────────────────────

BASE_PARALLELS = [
    ("Rainbow Foil", None),
    ("Green Foil", 199),
    ("Aqua Electric Dots Foil", 150),
    ("Blue Foil", 99),
    ("70th Anniversary Foil", 70),
    ("Gold Foil", 50),
    ("Orange Foil", 25),
    ("Black Foil", 10),
    ("Red Foil", 5),
    ("Foilfractor", 1),
]

# Insert parallels shared by 1954, From Silver Screen
INSERT_FOIL_PARALLELS = [
    ("Gold Foil", 50),
    ("Orange Foil", 25),
    ("Black Foil", 10),
    ("Red Foil", 5),
    ("Foilfractor", 1),
]

# 1955 Icons — same but no Foilfractor
ICONS_PARALLELS = [
    ("Gold Foil", 50),
    ("Orange Foil", 25),
    ("Black Foil", 10),
    ("Red Foil", 5),
]

# Posters
POSTER_PARALLELS = [
    ("PETG Variation", None),
    ("Gold Foil", 50),
    ("Orange Foil", 25),
    ("Black Foil", 10),
    ("Red Foil", 5),
    ("Foilfractor", 1),
]

# The Lands
LANDS_PARALLELS = [
    ("Gold Foil", 50),
    ("Orange Foil", 25),
    ("Black Foil", 10),
]

# Star Tours Chrome
STAR_TOURS_PARALLELS = [
    ("Orange Wave Refractor", 25),
    ("Black Refractor", 10),
    ("Red Refractor", 5),
]

# Pirate's Life
PIRATE_PARALLELS = [
    ("Orange Wave Refractor", 25),
    ("Black Refractor", 10),
]

# Eighth Wonder
EIGHTH_PARALLELS = [
    ("Orange Wave Refractor", 25),
    ("Black Refractor", 10),
]

# Entrance To Magic
ENTRANCE_PARALLELS = [
    ("Orange Wave Refractor", 25),
]

# Tiki Room
TIKI_PARALLELS = [
    ("Orange Wave Refractor", 25),
]

# It's A Small World
IASW_PARALLELS = [
    ("Orange Wave Refractor", 25),
    ("Black Refractor", 10),
    ("Red Refractor", 5),
    ("Superfractor", 1),
]

# Tomorrowland Cosmic
COSMIC_PARALLELS = [
    ("Orange Wave Refractor", 25),
    ("Black Refractor", 10),
    ("Red Refractor", 5),
    ("Superfractor", 1),
]

# Enchanted Relics
RELIC_PARALLELS = [
    ("70th Anniversary Foil", 70),
    ("Gold Foil", 50),
    ("Orange Foil", 25),
    ("Black Foil", 10),
    ("Red Foil", 5),
    ("Foilfractor", 1),
]

# Attraction Autographs
AUTO_PARALLELS = [
    ("70th Anniversary Foil", 70),
    ("Gold Foil", 50),
    ("Orange Foil", 25),
    ("Black Foil", 10),
    ("Red Foil", 5),
    ("Foilfractor", 1),
]

# 1955 Icons Autographs
ICONS_AUTO_PARALLELS = [
    ("70th Anniversary Foil", 70),
    ("Gold Foil", 50),
    ("Orange Foil", 25),
    ("Black Foil", 10),
    ("Red Foil", 5),
    ("Foilfractor", 1),
]

# Collector's Pin Relic
PIN_PARALLELS = [
    ("Red Foil", 5),
]

# ─── 3. Insert sets + cards ───────────────────────────────────────────────────

# ── BASE SETS ─────────────────────────────────────────────────────────────────

make_insert_set("Base - Then And Now", BASE_PARALLELS, [
    ("1", "Disneyland Railroad (THEN-Main Street, U.S.A.)"),
    ("2", "Disneyland Railroad (NOW-Main Street, U.S.A.)"),
    ("3", "Main Street, U.S.A. (NOW-Main Street, U.S.A.)"),
    ("4", "Great Moments with Mr. Lincoln (THEN-Main Street, U.S.A.)"),
    ("5", "Great Moments with Mr. Lincoln (NOW-Main Street, U.S.A.)"),
    ("6", "The Hub (THEN-Main Street, U.S.A.)"),
    ("7", "Primeval World (THEN-Main Street, U.S.A.)"),
    ("8", "Walt Disney's Enchanted Tiki Room (THEN-Adventureland)"),
    ("9", "The Jungle Cruise (THEN-Adventureland)"),
    ("10", "The Jungle Cruise (NOW-Adventureland)"),
    ("11", "The One, The Only, Backside of Water (THEN-Adventureland)"),
    ("12", "Don't Worry, They Have Their Trunks On (THEN-Adventureland)"),
    ("13", "Indiana Jones Adventure (THEN-Adventureland)"),
    ("14", "Look Not into the Eyes of the Idol (NOW-Adventureland)"),
    ("15", "Indiana Jones Contains the Spirit (NOW-Adventureland)"),
    ("16", "Stage Coach Ride (THEN-Frontierland)"),
    ("17", "Mine Train Through Nature's Wonderland (THEN-Frontierland)"),
    ("18", "Cascade Peak (THEN-Frontierland)"),
    ("19", "Big Thunder Mountain (NOW-Frontierland)"),
    ("20", "Rivers of America and the Living Desert (THEN-Frontierland)"),
    ("21", "Mark Twain Riverboat (NOW-Frontierland)"),
    ("22", "Country Bear Jamboree (THEN-Bayou Country)"),
    ("23", "The Many Adventures of Winnie the Pooh (NOW-Bayou Country)"),
    ("24", "Black Spire Outpost, Batuu (NOW-Star Wars: Galaxy's Edge)"),
    ("25", "Millennium Falcon: Smugglers Run (NOW-Star Wars: Galaxy's Edge)"),
    ("26", "Star Wars: Rise of the Resistance (NOW-Star Wars: Galaxy's Edge)"),
    ("27", "Toontown Five & Dime and The Gag Factory (THEN-Toontown)"),
    ("28", "The El CapiTOON Theater (NOW-Toontown)"),
    ("29", "Nothing Can Stop Us Now (NOW-Toontown)"),
    ("30", '"it\'s a small world" (THEN-Fantasyland)'),
    ("31", "Storybook Land Canal Boats (THEN-Fantasyland)"),
    ("32", "Storybook Land Lighthouse Ticket Booth (THEN-Fantasyland)"),
    ("33", "Dumbo Flying Elephants (THEN-Fantasyland)"),
    ("34", "Dumbo the Flying Elephant (NOW-Fantasyland)"),
    ("35", "Off to Never Land (NOW-Fantasyland)"),
    ("36", "Mermaid Lagoon (THEN-Fantasyland)"),
    ("37", "Fantasyland Skyway Station (THEN-Fantasyland)"),
    ("38", "Skyway Buckets (THEN-Fantasyland)"),
    ("39", "Matterhorn (NOW-Fantasyland)"),
    ("40", "Something Lurks Inside the Mountain (NOW-Fantasyland)"),
    ("41", "The Abominable Snowman (THEN-Fantasyland)"),
    ("42", "The Abominable Snowman (NOW-Fantasyland)"),
    ("43", "Mad Tea Party (THEN-Fantasyland)"),
    ("44", "Mad Tea Party (NOW-Fantasyland)"),
    ("45", "A Very Merry Unbirthday (NOW-Fantasyland)"),
    ("46", "A Great Big Beautiful Tomorrow (THEN-Tomorrowland)"),
    ("47", "Imagination and Beyond (THEN-Tomorrowland)"),
    ("48", "Space Mountain (THEN-Tomorrowland)"),
    ("49", "Space Mountain (THEN-Tomorrowland)"),
    ("50", "Space Mountain (NOW-Tomorrowland)"),
    ("51", "Adventure Thru Inner Space (THEN-Tomorrowland)"),
    ("52", "Star Tours (THEN-Tomorrowland)"),
    ("53", "Star Tours: The Adventures Continue (NOW-Tomorrowland)"),
    ("54", "Rocket to the Moon (THEN-Tomorrowland)"),
    ("55", "Redd Rockett's Pizza Port (THEN-Tomorrowland)"),
    ("56", "Alien Pizza Planet (NOW-Tomorrowland)"),
    ("57", "The Moonliner and Astro-Jets (THEN-Tomorrowland)"),
    ("58", "Rocket Jets (THEN-Tomorrowland)"),
    ("59", "Observatron (NOW-Tomorrowland)"),
    ("60", "Astro Orbitor (NOW-Tomorrowland)"),
    ("61", "Autopia (THEN-Tomorrowland)"),
    ("62", "Kinetic Energy: Monorail Over Submarine Lagoon (THEN-Tomorrowland)"),
    ("63", "Submarine Voyage (THEN-Tomorrowland)"),
    ("64", "Finding Nemo Submarine Voyage (NOW-Tomorrowland)"),
    ("65", "Carousel of Progress (THEN-Tomorrowland)"),
    ("66", "America Sings (THEN-Tomorrowland)"),
    ("67", "Innoventions (THEN-Tomorrowland)"),
    ("68", "Neon Astronaut Mickey (THEN-Tomorrowland)"),
    ("69", "The PeopleMover (THEN-Tomorrowland)"),
    ("70", "Rocket Rods (THEN-Tomorrowland)"),
    ("71", "Pirates of the Caribbean (THEN-New Orleans Square)"),
    ("72", "Pirates of the Caribbean (NOW-New Orleans Square)"),
    ("73", "Piles of Treasure (THEN-New Orleans Square)"),
    ("74", "Dead Men Tell No Tales (NOW-New Orleans Square)"),
    ("75", "Pillaging and Plundering (THEN-New Orleans Square)"),
    ("76", "Come on, have a nice bone, eh? (THEN-New Orleans Square)"),
    ("77", "The Blue Bayou (NOW-New Orleans Square)"),
    ("78", "The Haunted Mansion (NOW-New Orleans Square)"),
    ("79", "The Mansion's Organ (THEN-New Orleans Square)"),
    ("80", "A Swinging Wake (THEN-New Orleans Square)"),
    ("81", "Grim Grinning Ghosts Come Out to Socialize (THEN-New Orleans Square)"),
    ("82", "Beware of Hitchhiking Ghosts (NOW-New Orleans Square)"),
])
print("  Base - Then And Now: 82 cards")

make_insert_set("Base - Timeline", BASE_PARALLELS, [
    ("83", "Sleeping Beauty Castle Construction"),
    ("84", "Mickey and Donald Celebrate the Grand Opening"),
    ("85", "Autopia Cars Zoom in the First Parade"),
    ("86", "Lillian's Petrified Tree \"Gift\""),
    ("87", "Walt's Plans to Take the Park to New Heights"),
    ("88", "Disneyland Tenth Anniversary on TV"),
    ("89", "The Primeval World Meets the Modern World"),
    ("90", "it's a small world Debuts After the World's Fair"),
    ("91", "Walt and Mickey in Engine No. 1"),
    ("92", "Developing Pirates of the Caribbean in Miniature"),
    ("93", "A Happy Haunt Materializes"),
    ("94", "Space Mountain Shoots for the Stars"),
    ("95", "Big Thunder Hosts its First Wild Ride"),
    ("96", "The Land that Toons Built"),
    ("97", "The Temple of Mara Opens to Tourists"),
    ("98", "New Tomorrowland"),
    ("99", "Buzz Lightyear to Star Command"),
])
print("  Base - Timeline: 17 cards")

make_insert_set("Base - Snack Time", BASE_PARALLELS, [
    ("100", "Mickey's Premium Ice Cream Bar"),
    ("101", "Caramel Corn and Kettle Corn"),
    ("102", "Classic Mickey-Shaped Beignets"),
    ("103", "Turkey Leg"),
    ("104", "Churro"),
    ("105", "70th Anniversary Minnie Caramel Apple"),
    ("106", "Mickey Waffle"),
    ("107", "Pineapple Soft Serve"),
    ("108", "Grey Stuff"),
    ("109", "Blue Milk and Green Milk"),
    ("110", "Ronto Morning Wrap"),
    ("111", "Popcorn"),
    ("112", "Celebration Matterhorn Macaroon"),
    ("113", "Mickey Mouse Pretzel"),
    ("114", "Corn Dog"),
    ("115", "Seasonal: Evil Queen Caramel Apple"),
    ("116", "Seasonal: Mickey Gingerbread"),
    ("117", "Balloon Mickey Marshmallow Pop"),
])
print("  Base - Snack Time: 18 cards")

make_insert_set("Base - Concept Art", BASE_PARALLELS, [
    ("118", "A Dream of the Happiest Place on Earth"),
    ("119", "Town Square"),
    ("120", "Main Street, U.S.A."),
    ("121", "Carnation Caf\u00e9"),
    ("122", "Shopping at the Bazaar"),
    ("123", "The Jungle Cruise"),
    ("124", "The Haunted Mansion"),
    ("125", "The Bride"),
    ("126", "Rowboat Ghost"),
    ("127", "The Mansion's Organist"),
    ("128", "Entering Isla Tesoro Jail"),
    ("129", "How's About a Nice, Juicy Bone?"),
    ("130", "Thar Be Treasure"),
    ("131", "Singing Pirates"),
    ("132", "Frontierland Aerial"),
    ("133", "Mark Twain Riverboat"),
    ("134", "Uranium Hunt"),
    ("135", "Sleeping Beauty Castle"),
    ("136", "Matterhorn Mountain"),
    ("137", "Fantasyland Duck Bumps"),
    ("138", "Riding the Jolly Roger"),
    ("139", "King Arthur Carrousel"),
    ("140", "Snow White's Adventures with Dopey"),
    ("141", "Casey Jr. Circus Train"),
    ("142", "Monstro the Whale"),
    ("143", "Dumbo Flying Elephants"),
    ("144", "Mad Tea Party"),
    ("145", "The Land that Toons Built"),
    ("146", "A Vista into a World of Wondrous Ideas"),
    ("147", "Highway of the Future"),
    ("148", "The PeopleMover and \"Spaceport & Rocket Flight\""),
    ("149", "Space Mountain"),
    ("150", "Magic from the Sky"),
])
print("  Base - Concept Art: 33 cards")

# ── AUTOGRAPHS ────────────────────────────────────────────────────────────────

make_insert_set("Attraction Autographs", AUTO_PARALLELS, [
    ("AA-BI", "Bret Iwan (Mickey Mouse-Fantasmic!)"),
    ("AA-CD", "Chris Diamantopoulos (Mickey Mouse-Mickey and Minnie's Runaway Railway)"),
    ("AA-ANR", "Anika Noni Rose (Princess Tiana-Tiana's Bayou Adventure)"),
    ("AA-JL", "Jenifer Lewis (Mama Odie-Tiana's Bayou Adventure)"),
    ("AA-MLW", "Michael-Leon Wooley (Louis-Tiana's Bayou Adventure)"),
    ("AA-JC", "Jim Cummings (Winnie the Pooh-The Many Adventures of Winnie the Pooh)"),
    ("AA-JCT", "Jim Cummings (Tigger-The Many Adventures of Winnie the Pooh)"),
    ("AA-PW", "Patrick Warburton (G2-4T-Star Tours: The Adventures Continue)"),
    ("AA-BB", "Ben Burtt (R2-D2-Star Tours: The Adventures Continue)"),
    ("AA-JP", "Jeff Pidgeon (Aliens-Buzz Lightyear Astro Blasters)"),
    ("AA-TA", "Tim Allen (Buzz Lightyear-Buzz Lightyear Astro Blasters)"),
    ("AA-ASZ", "Andrew Stanton (Zurg-Buzz Lightyear Astro Blasters)"),
    ("AA-AB", "Albert Brooks (Marlin-Finding Nemo Submarine Voyage)"),
    ("AA-AG", "Alexander Gould (Nemo-Finding Nemo Submarine Voyage)"),
    ("AA-DW", "Debra Wilson (Bridge Officer-Finding Nemo Submarine Voyage)"),
    ("AA-BJ", "Bob Joles (Conductor-Disneyland Railroad)"),
    ("AA-TCC", "TC Carson (Captain-Mark Twain Riverboat)"),
    ("AA-AV", "Alex Verde (Monorail Narrator-Disneyland Monorail)"),
    ("AA-MK", "Margaret Kerry (Tinker Bell-Peter Pan's Flight & Nighttime Spectaculars)"),
])
print("  Attraction Autographs: 19 cards")

make_insert_set("1955 Topps Disneyland Icons Autographs", ICONS_AUTO_PARALLELS, [
    ("T55A-BI", "Bret Iwan (Sorcerer's Apprentice Mickey-Fantasmic!)"),
    ("T55A-CD", "Chris Diamantopoulos (Mickey Mouse-Mickey and Minnie's Runaway Railway)"),
    ("T55A-BF", "Bill Farmer (Pluto-Mickey and Minnie's Runaway Railway)"),
    ("T55A-ANR", "Anika Noni Rose (Tiana-Tiana's Bayou Adventure)"),
    ("T55A-JL", "Jenifer Lewis (Mama Odie-Tiana's Bayou Adventure)"),
    ("T55A-MLW", "Michael-Leon Wooley (Louis-Bayou Adventure)"),
    ("T55A-JC", "Jim Cummings (Winnie the Pooh-The Many Adventures of Winnie the Pooh)"),
    ("T55A-JCT", "Jim Cummings (Tigger-The Many Adventures of Winnie the Pooh)"),
    ("T55A-JCH", "Jim Cummings (Hondo Ohnaka-Millennium Falcon: Smugglers Run)"),
    ("T55A-PW", "Patrick Warburton (G2-4T-Star Tours: The Adventures Continue)"),
    ("T55A-BB", "Ben Burtt (R2-D2-Star Tours: The Adventures Continue)"),
    ("T55A-JP", "Jeff Pidgeon (Aliens-Buzz Lightyear Astro Blasters)"),
    ("T55A-TA", "Tim Allen (Buzz Lightyear-Buzz Lightyear Astro Blasters)"),
    ("T55A-ASZ", "Andrew Stanton (Zurg-Buzz Lightyear Astro Blasters)"),
    ("T55A-ASC", "Andrew Stanton (Crush-Finding Nemo Submarine Voyage)"),
    ("T55A-AB", "Albert Brooks (Marlin-Finding Nemo Submarine Voyage)"),
    ("T55A-AG", "Alexander Gould (Nemo-Finding Nemo Submarine Voyage)"),
    ("T55A-MK", "Margaret Kerry (Tinker Bell-Original Pantomime Model)"),
])
print("  1955 Topps Disneyland Icons Autographs: 18 cards")

# ── RELICS ────────────────────────────────────────────────────────────────────

make_insert_set("Collector's Pin Relic Redemption", PIN_PARALLELS, [
    ("CP-70", "Collector's Pin Relic Card /70"),
])
print("  Collector's Pin Relic Redemption: 1 card")

make_insert_set("Enchanted Relics", RELIC_PARALLELS, [
    ("ER-DD", "Disney Dollar"),
    ("ER-DDM", "Disney Dollar Mickey"),
    ("ER-DDMT", "Disney Dollar Mark Twain Riverboat"),
    ("ER-DDG", "Disney Dollar Goofy"),
    ("ER-DDS", "Disney Dollar Stitch"),
    ("ER-DDC", "Disney Dollar 50th Anniversary Castle"),
    ("ER-57NYE", "1957 New Year's Eve Ticket"),
    ("ER-58NYE", "1958 New Year's Eve Ticket"),
    ("ER-59DN", "1959 Date Nite Pass"),
    ("ER-60OFP", "1960 An Old Fashioned Picnic Ticket"),
    ("ER-60SA", "1960 Special Admission Ticket"),
    ("ER-61GN", "1961 First Annual Grad Nite Party Ticket"),
    ("ER-61MKC", "1961 Magic Kingdom Club Special Guest Card"),
    ("ER-61PD", "1961 Passport to Disneyland Guided Tour Ticket"),
    ("ER-61GT", "1961 Magic Kingdom Guided Tour Ticket"),
    ("ER-61NYE", "1961 New Year's Eve Ticket"),
    ("ER-62SF", "1962 Spring Fling Ticket"),
    ("ER-05U", "2005 Disneyland 50th Anniversary Umbrella"),
    ("ER-15SBC", "2015 Disneyland 60th Anniversary Sleeping Beauty Castle Banner"),
    ("ER-MSEP", "2017 Main Street Electrical Parade Banner"),
    ("ER-23SBC", "2023 Disney100 Sleeping Beauty Castle Drawbridge Banner"),
    ("ER-HGC", "Hitchhiking Ghost Phineas Costume"),
    ("ER-HGH", "Hitchhiking Ghost Phineas Hat"),
    ("ER-CHD", "Constance Hatchaway Dress"),
    ("ER-FCD", "Frozen Live Coronation Ball Ensemble Dress"),
    ("ER-HMC", "Haunted Mansion Cast Member Costume"),
    ("ER-HMSK", "Haunted Mansion Cast Member Skirt"),
    ("ER-HMS", "Haunted Mansion Cast Member Shirt"),
    ("ER-HMT", "Haunted Mansion Cast Member Trousers"),
    ("ER-PTC", "Pirates of the Caribbean Cast Member Shirt"),
    ("ER-PTCB", "Pirates of the Caribbean Cast Member Blouse"),
    ("ER-PTCT", "Pirates of the Caribbean Cast Member Trousers"),
    ("ER-FS", "Fantasyland Cast Member Shirt"),
    ("ER-FB", "Fantasyland Cast Member Blouse"),
    ("ER-FT", "Fantasyland Cast Member Trousers"),
    ("ER-ISW", "it's a small world Cast Member Costume"),
    ("ER-ISWH", "it's a small world Cast Member Hat"),
    ("ER-ISWT", "it's a small world Cast Member Trousers"),
    ("ER-SMC", "Space Mountain Cast Member Costume"),
    ("ER-SMT", "Space Mountain Cast Member Trousers"),
    ("ER-ABC", "Buzz Lightyear Astro Blasters Cast Member Costume"),
    ("ER-ABT", "Buzz Lightyear Astro Blasters Cast Member Trousers"),
    ("ER-STC", "Star Tours Cast Member Costume"),
    ("ER-STCC", "Star Tours Cast Member Costume (Alt)"),
    ("ER-STT", "Star Tours Cast Member Trousers"),
    ("ER-TTC", "Toontown Cast Member Costume"),
    ("ER-TTB", "Toontown Cast Member Costume (Alt)"),
    ("ER-TTP", "Toontown Cast Member Costume (Alt 2)"),
    ("ER-TTT", "Toontown Cast Member Trousers"),
    ("ER-TTS", "Toontown Cast Member Skirt"),
    ("ER-TTV", "Toontown Cast Member Vest"),
    ("ER-CDGC", "Chip 'n' Dale's GADGETcoaster Cast Member Costume"),
    ("ER-RRC", "Mickey & Minnie's Runaway Railway Cast Member Costume"),
    ("ER-TTA", "Toontown Cast Member Accessory"),
    ("ER-TFB", "Toontown Food & Beverage Cast Member Apron"),
    ("ER-TFBA", "Toontown Food & Beverage Cast Member Apron (Alt)"),
])
print("  Enchanted Relics: 56 cards")

# ── INSERT SETS ───────────────────────────────────────────────────────────────

make_insert_set("1954 Topps Disneyland On Wheels", INSERT_FOIL_PARALLELS, [
    ("T54-1", "Mine Train"), ("T54-2", "Tramp Steamer"), ("T54-3", "Mark II Monorail"),
    ("T54-4", "Mark V Monorail"), ("T54-5", "Doom Buggy"), ("T54-6", "Canoe"),
    ("T54-7", "Log Raft"), ("T54-8", "Sailing Ship"), ("T54-9", "Riverboat"),
    ("T54-10", "PeopleMover"), ("T54-11", "Rocket Rod"), ("T54-12", "Rocket Ship"),
    ("T54-13", "Car"), ("T54-14", "Submarine"), ("T54-15", "Moonliner"),
    ("T54-16", "StarSpeeder"), ("T54-17", "Fleet Transport"), ("T54-18", "Beehive"),
    ("T54-19", "Canal Boat"), ("T54-20", "Pirate Galleon"), ("T54-21", "Skyway Gondola"),
    ("T54-22", "Bobsled"), ("T54-23", "Teacup"), ("T54-24", "Flying Elephant"),
    ("T54-25", "Locomotive"),
])
print("  1954 Topps Disneyland On Wheels: 25 cards")

make_insert_set("1955 Topps Disneyland Icons", ICONS_PARALLELS, [
    ("T55-1", "Walt Disney"), ("T55-2", "Sorcerer's Apprentice Mickey"),
    ("T55-3", "Aliens"), ("T55-4", "Redd"), ("T55-5", "Bathing Elephants"),
    ("T55-6", "Indiana Jones"), ("T55-7", "Hondo Ohnaka"), ("T55-8", "The Abominable Snowman"),
    ("T55-9", "Tom Morrow"), ("T55-10", "Mickey Mouse"), ("T55-11", "Minnie Mouse"),
    ("T55-12", "Pluto"), ("T55-13", "C-3PO"), ("T55-14", "Kylo Ren"),
    ("T55-15", "Tiana"), ("T55-16", "Mama Odie"), ("T55-17", "Winnie the Pooh"),
    ("T55-18", "Tigger"), ("T55-19", "Henry"), ("T55-20", "The Caretaker"),
    ("T55-21", "The Bride"), ("T55-22", "Phineas"), ("T55-23", "Ezra"),
    ("T55-24", "Gus"), ("T55-25", "Alice"), ("T55-26", "Mickey Mouse (Disneyland)"),
])
print("  1955 Topps Disneyland Icons: 26 cards")

make_insert_set("From Silver Screen To Main Street", INSERT_FOIL_PARALLELS, [
    ("MS-1", "The First Parade"), ("MS-2", "Blue Fairy"),
    ("MS-3", "Casey Jr. Train and the Drum"), ("MS-4", "The Jolly Roger"),
    ("MS-5", "Pete's Dragon Elliott"), ("MS-6", "To Honor America"),
    ("MS-7", "Mickey & Friends"), ("MS-8", "Fantasia Magic Brooms"),
    ("MS-9", "Mickey, Minnie, and Donald Balloons"), ("MS-10", "I Just Can't Wait To Be King"),
    ("MS-11", "Rafiki and Zazu"), ("MS-12", "Mushu"),
    ("MS-13", "Dream of Laughter - Geppetto"), ("MS-14", "Dream of Enchantment - Cogsworth"),
    ("MS-15", "Gingerbread House - Goofy"), ("MS-16", "The Toy Soldiers"),
    ("MS-17", "Tinker Bell and Peter Pan"), ("MS-18", "Genie, Tigger, and Lumi\u00e8re"),
    ("MS-19", "Monsters, Inc. Dance Party - Mike Wazowski"),
    ("MS-20", "Monsters, Inc. Dance Party - Sulley"),
    ("MS-21", "Cars Electric Roadway Jam - Mack"),
    ("MS-22", "Frozen Fractals - Anna and Elsa"),
    ("MS-23", "Mickey & Friends Lightastic Finale - Donald Duck"),
    ("MS-24", "A Swirl of Magic - Mickey"), ("MS-25", "Celebrate Happy Cavalcade"),
])
print("  From Silver Screen To Main Street: 25 cards")

make_insert_set("Posters", POSTER_PARALLELS, [
    ("P-1", "Jungle Cruise"), ("P-2", "Mad Tea Party, Dumbo, & King Arthur Carrousel"),
    ("P-3", "Mr. Toad's Wild Ride"), ("P-4", "Space Station X-1"),
    ("P-5", "Peter Pan's Flight"), ("P-6", "Red Wagon Inn"),
    ("P-7", "Storybook Land Canal Boats"), ("P-8", "Rocket to the Moon"),
    ("P-9", "Rainbow Caverns"), ("P-10", "Disneyland Monorail"),
    ("P-11", "Flying Saucers"), ("P-12", "it's a small world"),
    ("P-13", "PeopleMover"), ("P-14", "Adventure Thru Inner Space"),
])
print("  Posters: 14 cards")

make_insert_set("The Lands", LANDS_PARALLELS, [
    ("LNDS-1", "Main Street, USA"), ("LNDS-2", "Adventureland"),
    ("LNDS-3", "Tomorrowland"), ("LNDS-4", "Frontierland"),
    ("LNDS-5", "Fantasyland"), ("LNDS-6", "New Orleans Square"),
    ("LNDS-7", "Bayou Country / Bear Country"), ("LNDS-8", "Mickey's Toontown"),
    ("LNDS-9", "Star Wars: Galaxy's Edge / Big Thunder Ranch"),
    ("LNDS-10", "Sleeping Beauty Castle"),
])
print("  The Lands: 10 cards")

# Chrome insert sets with numbered print runs noted
STAR_TOURS_87 = [("Base /87", 87)] + STAR_TOURS_PARALLELS
make_insert_set("1977 Topps Star Tours Chrome", STAR_TOURS_87, [
    ("77ST-1", "Enter A Galaxy Far, Far Away"), ("77ST-2", "C-3PO"),
    ("77ST-3", "StarSpeeder 3000"), ("77ST-4", "StarSpeeder 3000 Cabin"),
    ("77ST-5", "RX-24"), ("77ST-6", "G2-4T"), ("77ST-7", "R2-D2"),
    ("77ST-8", "StarSpeeder 1000"), ("77ST-9", "StarSpeeder 1000 Cabin"),
    ("77ST-10", "Darth Vader"), ("77ST-11", "Podracing on Tatooine"),
    ("77ST-12", "AT-AT Battle on Hoth"), ("77ST-13", "Lightspeed to Endor"),
])
print("  1977 Topps Star Tours Chrome: 13 cards")

make_insert_set("A Pirate's Life Chrome", PIRATE_PARALLELS, [
    ("POTC-1", "Helmsman"), ("POTC-2", "Island Skeleton"), ("POTC-3", "Ned Low"),
    ("POTC-4", "Captain Charles Gibbs"), ("POTC-5", "Sir Henry Mainwaring"),
    ("POTC-6", "Sir Francis Verney"), ("POTC-7", "Anne Bonny & Mary Read"),
    ("POTC-8", "Pirate Robber"), ("POTC-9", "Auctioneer"), ("POTC-10", "Pirate Redd"),
])
print("  A Pirate's Life Chrome: 10 cards")

EIGHTH_55 = [("Base /55", 55)] + EIGHTH_PARALLELS
make_insert_set("Eighth Wonder Chrome", EIGHTH_55, [
    ("EW-1", "Wave Goodbye to the Folks on the Dock"),
    ("EW-2", "This is your skipper speaking. First time? Me too."),
    ("EW-3", "Ugh, the Ancient Temple is Ruined"),
    ("EW-4", "Rooted in History"),
    ("EW-5", "Schweitzer Falls and the Eighth Wonder of the World"),
    ("EW-6", "The Most Dangerous Animal in the Jungle: the Hippo"),
    ("EW-7", "The Cruise that Goes on for Niles and Niles"),
])
print("  Eighth Wonder Chrome: 7 cards")

make_insert_set("Entrance To Magic Chrome", ENTRANCE_PARALLELS, [
    ("EM-1", "Entrance to Magic"),
])
print("  Entrance To Magic Chrome: 1 card")

make_insert_set("Greetings From The Tiki Room Chrome", TIKI_PARALLELS, [
    ("ETR-1", "Jos\u00e9"), ("ETR-2", "Michael"), ("ETR-3", "Pierre"), ("ETR-4", "Fritz"),
])
print("  Greetings From The Tiki Room Chrome: 4 cards")

make_insert_set("It's A Small World Chrome", IASW_PARALLELS, [
    ("IASW-1", "Hello!"), ("IASW-2", "Bonjour!"), ("IASW-3", "Dia Duit!"),
    ("IASW-4", "Hallo!"), ("IASW-5", "Ciao!"), ("IASW-6", "Privet!"),
    ("IASW-7", "Sawadee!"), ("IASW-8", "Jambo!"), ("IASW-9", "\u00a1Hola!"),
    ("IASW-10", "Aloha!"), ("IASW-11", "Howdy!"), ("IASW-12", "Goodbye!"),
    ("IASW-13", "Farewell!"), ("IASW-14", "See You Later!"),
])
print("  It's A Small World Chrome: 14 cards")

COSMIC_77 = [("Base /77", 77)] + COSMIC_PARALLELS
make_insert_set("Tomorrowland Cosmic Chrome", COSMIC_77, [
    ("TCC-1", "Moonliner"), ("TCC-3", "Astronaut Pluto"),
    ("TCC-4", "Astronaut Donald Duck"), ("TCC-5", "Neon Mickey Mouse"),
    ("TCC-6", "Space Mountain Robot"), ("TCC-7", "Astronauts Chip 'n' Dale"),
    ("TCC-8", "Astronaut Goofy"), ("TCC-9", "Autopia Robot"),
    ("TCC-10", "Astronaut Mickey Mouse"), ("TCC-11", "Stitch"),
    ("TCC-11B", "Buzz Lightyear"), ("TCC-12", "Emperor Zurg"),
    ("TCC-13", "Green Alien"), ("TCC-14", "Ghost Galaxy"),
])
print("  Tomorrowland Cosmic Chrome: 14 cards")

make_insert_set("Welcome Foolish Mortals Chrome", [], [
    ("WFM-1", "Sally Slater"), ("WFM-2", "Alexander Nitrokoff"),
    ("WFM-3", "Constance"), ("WFM-4", "Three Unfortunate Men in Quicksand"),
])
print("  Welcome Foolish Mortals Chrome: 4 cards")

CN_70 = [("Base /70", 70)]
make_insert_set("Character Nametags", CN_70, [
    ("CN-HM", "Ghost Host"), ("CN-SM", "Astronaut"), ("CN-POTC", "Pirate"),
    ("CN-MB", "Bobsledder"), ("CN-MTP", "Hatter"), ("CN-ETR", "Lucky People"),
    ("CN-IASW", "World Traveler"), ("CN-MTWR", "Driver"), ("CN-DFE", "Flyer"),
    ("CN-MFSR", "Rebel"),
])
print("  Character Nametags: 10 cards")

# Sketch Cards — each artist is a unique card
make_insert_set("Sketch Cards", [], [
    ("SK-1", "Aaron Laurich"), ("SK-2", "Aaron Roberts Art"), ("SK-3", "Alex Mines"),
    ("SK-4", "Anthony Pietszak"), ("SK-5", "Antni Ellison"), ("SK-6", "Ariel Mamani"),
    ("SK-7", "Ashley Marsh"), ("SK-8", "Bean"), ("SK-9", "Ben Jones"),
    ("SK-10", "Benjamin Lombart"), ("SK-11", "Brandon Klein"), ("SK-12", "Brent Ragland"),
    ("SK-13", "Charlie Cody"), ("SK-14", "Chris Colyer"), ("SK-15", "Chris Thorne"),
    ("SK-16", "Cisco Rivera"), ("SK-17", "Cyrus Sherkat"), ("SK-18", "Dan Cooney"),
    ("SK-19", "Dan Gorman"), ("SK-20", "Darrin Pepe"), ("SK-21", "David Willingham"),
    ("SK-22", "Dawn Murphy"), ("SK-23", "DMN"), ("SK-24", "DYJ"),
    ("SK-25", "Eddie Rhodes III"), ("SK-26", "El Smetch\u00f6"), ("SK-27", "Eric Lehtonen"),
    ("SK-28", "Eric Medina"), ("SK-29", "Fox Layng"), ("SK-30", "Frank Sansone"),
    ("SK-31", "Franklim Teixeira"), ("SK-32", "Getatom"), ("SK-33", "Greg Treize"),
    ("SK-34", "Halsey Camera"), ("SK-35", "Ian McKesson"), ("SK-36", "James Harris"),
    ("SK-37", "Jason Rodriguez"), ("SK-38", "Jason Saldajeno"), ("SK-39", "Jason Sobol"),
    ("SK-40", "Jay Manchand"), ("SK-41", "Jeffrey C. Benitez"), ("SK-42", "Jessica Hickman"),
    ("SK-43", "Jessica Van Dusen"), ("SK-44", "Julie-Anne"), ("SK-45", "Kevin Graham"),
    ("SK-46", "Kimber Grobman"), ("SK-47", "Lindsey Greyling"), ("SK-48", "Louis Womble"),
    ("SK-49", "Lucas"), ("SK-50", "Madison Emerick"), ("SK-51", "Marlo Martos"),
    ("SK-52", "Mathilde Machuel"), ("SK-53", "Matthew Maldonado"),
    ("SK-54", "Michael Mastermaker"), ("SK-55", "Mike Stephens"), ("SK-56", "Neil Camera"),
    ("SK-57", "Nick Gribbon"), ("SK-58", "Nik Muggli"), ("SK-59", "Ni\u00f1o John Benitez"),
    ("SK-60", "Phillip Trujillo"), ("SK-61", 'Rich "RAM" Molinelli'),
    ("SK-62", "Rich Hennemann"), ("SK-63", "RJ Tomascik"), ("SK-64", "Rob Demers"),
    ("SK-65", "Ryan Finley"), ("SK-66", "Ryan Johnston"), ("SK-67", "Ryan Thompson"),
    ("SK-68", "Sandy Meeks"), ("SK-69", "Semra Bulut"), ("SK-70", "Shyla Lee"),
    ("SK-71", "Stephanie Swanger"), ("SK-72", "Steve Alce"), ("SK-73", "Ted Dastick Jr"),
    ("SK-74", "Todd Aaron Smith"), ("SK-75", "Tom Amici"), ("SK-76", "Zach Woolsey"),
    ("SK-77", "\u30b8\u30a7\u30a4\u30bd\u30f3 (Jason)"),
])
print("  Sketch Cards: 77 cards")

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
print(f"Parallel types:    {total_parallels}")
print(f"{'='*50}")

conn.close()
print("\nDone!")
