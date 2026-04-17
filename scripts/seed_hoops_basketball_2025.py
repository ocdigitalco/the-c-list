"""
Seed script: 2025-26 Topps Hoops Basketball
Inserts all data into the local SQLite database (the-c-list.db).
Usage: python3 scripts/seed_hoops_basketball_2025.py
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


# ─── Rookie set ──────────────────────────────────────────────────────────────

ROOKIES = {
    "Cooper Flagg", "Dylan Harper", "Ace Bailey", "VJ Edgecombe", "Cam Spencer",
    "Kon Knueppel", "Tre Johnson", "Nolan Traore", "Khaman Maluach", "Egor Demin",
    "Noa Essengue", "Boogie Fland", "Kasparas Jakucionis", "Liam McNeeley",
    "Baye Fall", "Hugo Gonzalez", "Collin Murray-Boyles", "Jeremiah Fears",
    "Isiah Harwell", "Tyler Betsey", "Jase Richardson", "Labaron Philon",
    "Asa Newell", "Alex Karaban", "Ben Saraf", "Dink Pate", "Eric Dixon",
    "Will Riley", "Ian Jackson", "Cody Williams", "PJ Hall", "Johni Broome",
    "Alex Sarr", "Carter Bryant", "Thomas Sorber", "Zach Edey", "Donovan Clingan",
    "Dalton Knecht", "Reed Sheppard", "Ja'Kobe Walter", "Matas Buzelis",
    "Tidjane Salaun", "Cody Riley", "Jared McCain", "Jaylen Wells",
}


def add_cards(insert_set_id, cards):
    """Add cards. cards = [(card_number, name, team), ...]"""
    for card_number, name, team in cards:
        is_rookie = name in ROOKIES
        player_id = get_or_create_player(set_id, name)
        create_appearance(player_id, insert_set_id, card_number, is_rookie, team)


def add_multi_cards(insert_set_id, cards):
    """Add co-player cards. cards = [(card_number, [(name, team), ...]), ...]"""
    for card_number, players_list in cards:
        app_ids = []
        player_ids = []
        for name, team in players_list:
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

SET_NAME = "2025-26 Topps Hoops Basketball"

cur.execute("SELECT id FROM sets WHERE name = ?", (SET_NAME,))
existing = cur.fetchone()
if existing:
    print(f"Set '{SET_NAME}' already exists with id {existing[0]}. Aborting.")
    conn.close()
    exit(1)

box_config = {
    "hobby": {
        "cards_per_pack": 8,
        "packs_per_box": 20,
        "autos_per_box": 1,
        "notes": "1 Autograph per box",
    },
    "jumbo": {
        "cards_per_pack": 20,
        "packs_per_box": 10,
        "boxes_per_case": 8,
        "autos_per_box": 2,
        "notes": "2 Autographs per box",
    },
    "value": {
        "cards_per_pack": 8,
        "packs_per_box": 7,
        "notes": "Green Hoops Parallels",
    },
    "fanatics": {
        "cards_per_pack": 8,
        "packs_per_box": 8,
        "notes": "Fanatics Parallels",
    },
    "hanger": {
        "cards_per_pack": 25,
        "packs_per_box": 1,
        "notes": "Orange Hoops Parallels",
    },
}

pack_odds = {
  "hobby": {
    "Base": "6:1",
    "Base Rainbow": "1:4",
    "Base Pixel Burst": "1:10",
    "Base Rainbow Yellow": "1:134",
    "Base Rainbow Green and Blue": "1:41",
    "Base Rainbow Gold and Green": "1:51",
    "Base Pixel Burst Blue": "1:68",
    "Base Pixel Burst Purple": "1:102",
    "Base Pixel Burst Green": "1:134",
    "Base Pixel Burst Gold": "1:201",
    "Base Pixel Burst Orange": "1:402",
    "Base Pixel Burst Black": "1:1004",
    "Base Pixel Burst Red": "1:2006",
    "Base Pixel Burst Platinum": "1:9981",
    "Base Highlights": "1:5",
    "Base Highlights Rainbow": "1:82",
    "Base Highlights Pixel Burst": "1:247",
    "Base Highlights Rainbow Yellow": "1:950",
    "Base Highlights Rainbow Green and Blue": "1:1048",
    "Base Highlights Rainbow Gold and Green": "1:1312",
    "Base Highlights Pixel Burst Blue": "1:1752",
    "Base Highlights Pixel Burst Purple": "1:2637",
    "Base Highlights Pixel Burst Green": "1:3475",
    "Base Highlights Pixel Burst Gold": "1:5219",
    "Base Highlights Pixel Burst Orange": "1:10394",
    "Base Highlights Pixel Burst Black": "1:25666",
    "Base Highlights Pixel Burst Red": "1:50304",
    "Base Highlights Pixel Burst Platinum": "1:251520",
    "Base All-Stars": "1:2",
    "Base All-Stars Rainbow": "1:28",
    "Base All-Stars Pixel Burst": "1:83",
    "Base All-Stars Rainbow Yellow": "1:317",
    "Base All-Stars Rainbow Green and Blue": "1:350",
    "Base All-Stars Rainbow Gold and Green": "1:438",
    "Base All-Stars Pixel Burst Blue": "1:584",
    "Base All-Stars Pixel Burst Purple": "1:879",
    "Base All-Stars Pixel Burst Green": "1:1161",
    "Base All-Stars Pixel Burst Gold": "1:1740",
    "Base All-Stars Pixel Burst Orange": "1:3475",
    "Base All-Stars Pixel Burst Black": "1:8674",
    "Base All-Stars Pixel Burst Red": "1:17228",
    "Base All-Stars Pixel Burst Platinum": "1:83840",
    "Bounce House": "1:15",
    "Bounce House Rainbow": "1:84",
    "Bounce House Pixel Burst": "1:168",
    "Bounce House Pixel Burst Purple": "1:1055",
    "Bounce House Pixel Burst Green": "1:1392",
    "Bounce House Pixel Burst Gold": "1:2086",
    "Bounce House Pixel Burst Orange": "1:4165",
    "Bounce House Pixel Burst Black": "1:10394",
    "Bounce House Pixel Burst Red": "1:20617",
    "Bounce House Pixel Burst Platinum": "1:96739",
    "Next Episode": "1:19",
    "Next Episode Rainbow": "1:105",
    "Next Episode Pixel Burst": "1:210",
    "Next Episode Pixel Burst Purple": "1:1319",
    "Next Episode Pixel Burst Green": "1:1740",
    "Next Episode Pixel Burst Gold": "1:2610",
    "Next Episode Pixel Burst Orange": "1:5219",
    "Next Episode Pixel Burst Black": "1:12965",
    "Next Episode Pixel Burst Red": "1:25666",
    "Next Episode Pixel Burst Platinum": "1:125760",
    "Dunkumentory": "1:25",
    "Dunkumentory Rainbow": "1:140",
    "Dunkumentory Pixel Burst": "1:280",
    "Dunkumentory Pixel Burst Purple": "1:1757",
    "Dunkumentory Pixel Burst Green": "1:2321",
    "Dunkumentory Pixel Burst Gold": "1:3475",
    "Dunkumentory Pixel Burst Orange": "1:6949",
    "Dunkumentory Pixel Burst Black": "1:17228",
    "Dunkumentory Pixel Burst Red": "1:33990",
    "Dunkumentory Pixel Burst Platinum": "1:157200",
    "Pay Attention": "1:19",
    "Pay Attention Rainbow": "1:105",
    "Pay Attention Pixel Burst": "1:210",
    "Pay Attention Pixel Burst Purple": "1:1319",
    "Pay Attention Pixel Burst Green": "1:1740",
    "Pay Attention Pixel Burst Gold": "1:2610",
    "Pay Attention Pixel Burst Orange": "1:5219",
    "Pay Attention Pixel Burst Black": "1:12965",
    "Pay Attention Pixel Burst Red": "1:25666",
    "Pay Attention Pixel Burst Platinum": "1:125760",
    "Hoopers": "1:19",
    "Hoopers Rainbow": "1:105",
    "Hoopers Pixel Burst": "1:210",
    "Hoopers Pixel Burst Purple": "1:1319",
    "Hoopers Pixel Burst Green": "1:1740",
    "Hoopers Pixel Burst Gold": "1:2610",
    "Hoopers Pixel Burst Orange": "1:5219",
    "Hoopers Pixel Burst Black": "1:12965",
    "Hoopers Pixel Burst Red": "1:25666",
    "Hoopers Pixel Burst Platinum": "1:125760",
    "Finals Pursuit First Round": "1:27",
    "Finals Pursuit Second Round": "1:396",
    "Finals Pursuit Semi-Finals": "1:1087",
    "Finals Pursuit The Finals": "1:4337",
    "NBA Champions Team": "1:13100",
    "NBA Champions Players": "1:1317",
    "Finals MVP": "1:13100",
    "Oasis": "1:489",
    "Oasis Platinum": "1:96739",
    "Joy": "1:1154",
    "Joy Platinum": "1:251520",
    "Checkmate": "1:403",
    "Checkmate Platinum": "1:83840",
    "Hoopnotic": "1:346",
    "Hoopnotic Platinum": "1:73977",
    "Hoops Rookie Signatures": "1:74",
    "Hoops Rookie Signatures Pixel Burst Purple": "1:630",
    "Hoops Rookie Signatures Pixel Burst Green": "1:831",
    "Hoops Rookie Signatures Pixel Burst Gold": "1:1247",
    "Hoops Rookie Signatures Pixel Burst Orange": "1:2491",
    "Hoops Rookie Signatures Pixel Burst Black": "1:6226",
    "Hoops Rookie Signatures Pixel Burst Red": "1:12452",
    "Hoops Rookie Signatures Pixel Burst Platinum": "1:59886",
    "Hoops Signs": "1:55",
    "Hoops Signs Pixel Burst Purple": "1:525",
    "Hoops Signs Pixel Burst Green": "1:679",
    "Hoops Signs Pixel Burst Gold": "1:1018",
    "Hoops Signs Pixel Burst Orange": "1:1847",
    "Hoops Signs Pixel Burst Black": "1:4607",
    "Hoops Signs Pixel Burst Red": "1:9180",
    "Hoops Signs Pixel Burst Platinum": "1:44915",
    "Hoops Rookie Duals": "1:1994",
    "Hoops Rookie Duals Pixel Burst Black": "1:9903",
    "Hoops Rookie Duals Pixel Burst Red": "1:19650",
    "Hoops Rookie Duals Pixel Burst Platinum": "1:96739",
    "Hoops Rookie Triples": "1:9903",
    "Hoops Rookie Triples Pixel Burst Black": "1:24659",
    "Hoops Rookie Triples Pixel Burst Red": "1:48370",
    "Hoops Rookie Duals Triples Platinum": "1:251520",
    "Hoops Rookie/Veteran Duals": "1:19650",
    "Hoops Rookie/Veteran Duals Pixel Burst Black": "1:48370",
    "Hoops Rookie/Veteran Duals Pixel Burst Red": "1:96739",
    "Hoops Rookie/Veteran Duals Pixel Burst Platinum": "1:419200",
    "Hoops 1989 Signatures": "1:130",
    "Hoops 1989 Signatures Pixel Burst Black": "1:4151",
    "Hoops 1989 Signatures Pixel Burst Red": "1:8274",
    "Hoops 1989 Signatures Pixel Burst Platinum": "1:40568",
  },
  "jumbo": {
    "Base": "15:1",
    "Base Rainbow": "1:2",
    "Base Pixel Burst": "1:3",
    "Base Rainbow Yellow": "1:16",
    "Base Rainbow Green and Blue": "1:10",
    "Base Rainbow Gold and Green": "1:12",
    "Base Pixel Burst Blue": "1:16",
    "Base Pixel Burst Purple": "1:25",
    "Base Pixel Burst Green": "1:32",
    "Base Pixel Burst Gold": "1:48",
    "Base Pixel Burst Orange": "1:96",
    "Base Pixel Burst Black": "1:238",
    "Base Pixel Burst Red": "1:476",
    "Base Pixel Burst Platinum": "1:2362",
    "Base Highlights": "1:2",
    "Base Highlights Rainbow": "1:21",
    "Base Highlights Pixel Burst": "1:59",
    "Base Highlights Rainbow Yellow": "1:225",
    "Base Highlights Rainbow Green and Blue": "1:249",
    "Base Highlights Rainbow Gold and Green": "1:311",
    "Base Highlights Pixel Burst Blue": "1:415",
    "Base Highlights Pixel Burst Purple": "1:625",
    "Base Highlights Pixel Burst Green": "1:825",
    "Base Highlights Pixel Burst Gold": "1:1236",
    "Base Highlights Pixel Burst Orange": "1:2461",
    "Base Highlights Pixel Burst Black": "1:6100",
    "Base Highlights Pixel Burst Red": "1:12200",
    "Base Highlights Pixel Burst Platinum": "1:58560",
    "Base All-Stars": "1:1",
    "Base All-Stars Rainbow": "1:7",
    "Base All-Stars Pixel Burst": "1:20",
    "Base All-Stars Rainbow Yellow": "1:75",
    "Base All-Stars Rainbow Green and Blue": "1:83",
    "Base All-Stars Rainbow Gold and Green": "1:104",
    "Base All-Stars Pixel Burst Blue": "1:139",
    "Base All-Stars Pixel Burst Purple": "1:209",
    "Base All-Stars Pixel Burst Green": "1:275",
    "Base All-Stars Pixel Burst Gold": "1:413",
    "Base All-Stars Pixel Burst Orange": "1:825",
    "Base All-Stars Pixel Burst Black": "1:2062",
    "Base All-Stars Pixel Burst Red": "1:4124",
    "Base All-Stars Pixel Burst Platinum": "1:19520",
    "Bounce House": "1:6",
    "Bounce House Rainbow": "1:24",
    "Bounce House Pixel Burst": "1:47",
    "Bounce House Pixel Burst Purple": "1:250",
    "Bounce House Pixel Burst Green": "1:330",
    "Bounce House Pixel Burst Gold": "1:495",
    "Bounce House Pixel Burst Orange": "1:990",
    "Bounce House Pixel Burst Black": "1:2461",
    "Bounce House Pixel Burst Red": "1:4880",
    "Bounce House Pixel Burst Platinum": "1:24400",
    "Next Episode": "1:8",
    "Next Episode Rainbow": "1:30",
    "Next Episode Pixel Burst": "1:59",
    "Next Episode Pixel Burst Purple": "1:313",
    "Next Episode Pixel Burst Green": "1:413",
    "Next Episode Pixel Burst Gold": "1:618",
    "Next Episode Pixel Burst Orange": "1:1236",
    "Next Episode Pixel Burst Black": "1:3083",
    "Next Episode Pixel Burst Red": "1:6100",
    "Next Episode Pixel Burst Platinum": "1:29280",
    "Dunkumentory": "1:10",
    "Dunkumentory Rainbow": "1:40",
    "Dunkumentory Pixel Burst": "1:79",
    "Dunkumentory Pixel Burst Purple": "1:417",
    "Dunkumentory Pixel Burst Green": "1:550",
    "Dunkumentory Pixel Burst Gold": "1:825",
    "Dunkumentory Pixel Burst Orange": "1:1645",
    "Dunkumentory Pixel Burst Black": "1:4124",
    "Dunkumentory Pixel Burst Red": "1:8134",
    "Dunkumentory Pixel Burst Platinum": "1:36600",
    "Pay Attention": "1:8",
    "Pay Attention Rainbow": "1:30",
    "Pay Attention Pixel Burst": "1:59",
    "Pay Attention Pixel Burst Purple": "1:313",
    "Pay Attention Pixel Burst Green": "1:413",
    "Pay Attention Pixel Burst Gold": "1:618",
    "Pay Attention Pixel Burst Orange": "1:1236",
    "Pay Attention Pixel Burst Black": "1:3083",
    "Pay Attention Pixel Burst Red": "1:6100",
    "Pay Attention Pixel Burst Platinum": "1:29280",
    "Hoopers": "1:8",
    "Hoopers Rainbow": "1:30",
    "Hoopers Pixel Burst": "1:59",
    "Hoopers Pixel Burst Purple": "1:313",
    "Hoopers Pixel Burst Green": "1:413",
    "Hoopers Pixel Burst Gold": "1:618",
    "Hoopers Pixel Burst Orange": "1:1236",
    "Hoopers Pixel Burst Black": "1:3083",
    "Hoopers Pixel Burst Red": "1:6100",
    "Hoopers Pixel Burst Platinum": "1:29280",
    "Finals Pursuit First Round": "1:7",
    "Finals Pursuit Second Round": "1:94",
    "Finals Pursuit Semi-Finals": "1:258",
    "Finals Pursuit The Finals": "1:1031",
    "NBA Champions Team": "1:3050",
    "NBA Champions Players": "1:307",
    "Finals MVP": "1:3050",
    "Oasis": "1:163",
    "Oasis Platinum": "1:24400",
    "Joy": "1:381",
    "Joy Platinum": "1:58560",
    "Checkmate": "1:133",
    "Checkmate Platinum": "1:19520",
    "Hoopnotic": "1:118",
    "Hoopnotic Platinum": "1:17224",
    "Hoops Rookie Signatures": "1:18",
    "Hoops Rookie Signatures Pixel Burst Purple": "1:150",
    "Hoops Rookie Signatures Pixel Burst Green": "1:197",
    "Hoops Rookie Signatures Pixel Burst Gold": "1:296",
    "Hoops Rookie Signatures Pixel Burst Orange": "1:591",
    "Hoops Rookie Signatures Pixel Burst Black": "1:1472",
    "Hoops Rookie Signatures Pixel Burst Red": "1:2928",
    "Hoops Rookie Signatures Pixel Burst Platinum": "1:14640",
    "Hoops Signs": "1:13",
    "Hoops Signs Pixel Burst Purple": "1:125",
    "Hoops Signs Pixel Burst Green": "1:161",
    "Hoops Signs Pixel Burst Gold": "1:241",
    "Hoops Signs Pixel Burst Orange": "1:438",
    "Hoops Signs Pixel Burst Black": "1:1093",
    "Hoops Signs Pixel Burst Red": "1:2186",
    "Hoops Signs Pixel Burst Platinum": "1:10845",
    "Hoops Rookie Duals": "1:473",
    "Hoops Rookie Duals Pixel Burst Black": "1:2362",
    "Hoops Rookie Duals Pixel Burst Red": "1:4723",
    "Hoops Rookie Duals Pixel Burst Platinum": "1:22524",
    "Hoops Rookie Triples": "1:2362",
    "Hoops Rookie Triples Pixel Burst Black": "1:5856",
    "Hoops Rookie Triples Pixel Burst Red": "1:11712",
    "Hoops Rookie Duals Triples Platinum": "1:58560",
    "Hoops Rookie/Veteran Duals": "1:4723",
    "Hoops Rookie/Veteran Duals Pixel Burst Black": "1:11712",
    "Hoops Rookie/Veteran Duals Pixel Burst Red": "1:22524",
    "Hoops Rookie/Veteran Duals Pixel Burst Platinum": "1:97600",
    "Hoops 1989 Signatures": "1:31",
    "Hoops 1989 Signatures Pixel Burst Black": "1:983",
    "Hoops 1989 Signatures Pixel Burst Red": "1:1966",
    "Hoops 1989 Signatures Pixel Burst Platinum": "1:9760",
  },
  "value": {
    "Base": "7:1",
    "Base Rainbow": "1:8",
    "Base Green Hoops": "1:3",
    "Base Light Burst": "1:12",
    "Base Rainbow Teal": "1:353",
    "Base Rainbow Blue and Yellow": "1:151",
    "Base Rainbow Red and Orange": "1:166",
    "Base Rainbow Purple and Blue": "1:208",
    "Base Light Burst Blue": "1:278",
    "Base Light Burst Purple": "1:418",
    "Base Light Burst Green": "1:551",
    "Base Light Burst Gold": "1:827",
    "Base Light Burst Orange": "1:1653",
    "Base Light Burst Black": "1:4131",
    "Base Light Burst Red": "1:8261",
    "Base Light Burst Platinum": "1:41303",
    "Base Highlights": "1:5",
    "Base Highlights Rainbow": "1:197",
    "Base Highlights Green Hoops": "1:70",
    "Base Highlights Light Burst": "1:308",
    "Base All-Stars": "1:2",
    "Base All-Stars Rainbow": "1:66",
    "Base All-Stars Green Hoops": "1:24",
    "Base All-Stars Light Burst": "1:103",
    "Hardwired": "1:20",
    "Hardwired Green Hoops": "1:62",
    "Hardwired Light Burst": "1:616",
    "Hardwired Light Burst Purple": "1:4337",
    "Hardwired Light Burst Green": "1:5725",
    "Hardwired Light Burst Gold": "1:8584",
    "Hardwired Light Burst Orange": "1:17143",
    "Hardwired Light Burst Black": "1:42737",
    "Hardwired Light Burst Red": "1:85474",
    "Hardwired Light Burst Platinum": "1:410275",
    "The Buzz": "1:17",
    "The Buzz Green Hoops": "1:52",
    "The Buzz Light Burst": "1:513",
    "The Buzz Light Burst Purple": "1:3616",
    "The Buzz Light Burst Green": "1:4771",
    "The Buzz Light Burst Gold": "1:7156",
    "The Buzz Light Burst Orange": "1:14312",
    "The Buzz Light Burst Black": "1:35780",
    "The Buzz Light Burst Red": "1:71560",
    "The Buzz Light Burst Platinum": "1:341896",
    "Net to Net": "1:17",
    "Net to Net Green Hoops": "1:52",
    "Net to Net Light Burst": "1:513",
    "Net to Net Light Burst Purple": "1:3616",
    "Net to Net Light Burst Green": "1:4771",
    "Net to Net Light Burst Gold": "1:7156",
    "Net to Net Light Burst Orange": "1:14312",
    "Net to Net Light Burst Black": "1:35780",
    "Net to Net Light Burst Red": "1:71560",
    "Net to Net Light Burst Platinum": "1:341896",
    "Jam-Packed": "1:33",
    "Jam-Packed Green Hoops": "1:103",
    "Jam-Packed Light Burst": "1:1026",
    "Jam-Packed Light Burst Purple": "1:7232",
    "Jam-Packed Light Burst Green": "1:9542",
    "Jam-Packed Light Burst Gold": "1:14312",
    "Jam-Packed Light Burst Orange": "1:28624",
    "Jam-Packed Light Burst Black": "1:71560",
    "Jam-Packed Light Burst Red": "1:143120",
    "Jam-Packed Light Burst Platinum": "1:683792",
    "Block by Block": "1:351",
    "Block by Block Platinum": "1:267571",
    "Boombastic": "1:1402",
    "Boombastic Platinum": "1:1025687",
    "Hoops 1989 Signatures Green Hoops": "1:401",
    "Hoops Rookie First Signs": "1:206",
    "Hoops Rookie First Signs Light Burst Purple": "1:2467",
    "Hoops Rookie First Signs Light Burst Green": "1:2736",
    "Hoops Rookie First Signs Light Burst Gold": "1:4103",
    "Hoops Rookie First Signs Light Burst Orange": "1:8206",
    "Hoops Rookie First Signs Light Burst Black": "1:20514",
    "Hoops Rookie First Signs Light Burst Red": "1:41028",
    "Hoops Rookie First Signs Light Burst Platinum": "1:205138",
    "Hoops Hyper Signatures": "1:213",
    "Hoops Hyper Signatures Light Burst Purple": "1:2878",
    "Hoops Hyper Signatures Light Burst Green": "1:3507",
    "Hoops Hyper Signatures Light Burst Gold": "1:5129",
    "Hoops Hyper Signatures Light Burst Orange": "1:10520",
    "Hoops Hyper Signatures Light Burst Black": "1:21824",
    "Hoops Hyper Signatures Light Burst Red": "1:43647",
    "Hoops Hyper Signatures Light Burst Platinum": "1:212212",
  },
  "hanger": {
    "Base": "19:1",
    "Base Rainbow": "1:5",
    "Base Orange Hoops": "1:1",
    "Base Light Burst": "1:11",
    "Base Rainbow Teal": "1:100",
    "Base Rainbow Blue and Yellow": "1:43",
    "Base Rainbow Red and Orange": "1:48",
    "Base Rainbow Purple and Blue": "1:60",
    "Base Light Burst Blue": "1:80",
    "Base Light Burst Purple": "1:120",
    "Base Light Burst Green": "1:158",
    "Base Light Burst Gold": "1:237",
    "Base Light Burst Orange": "1:473",
    "Base Light Burst Black": "1:1181",
    "Base Light Burst Red": "1:2357",
    "Base Light Burst Platinum": "1:11737",
    "Base Highlights": "1:2",
    "Base Highlights Rainbow": "1:116",
    "Base Highlights Orange Hoops": "1:20",
    "Base Highlights Light Burst": "1:261",
    "Base All-Stars": "1:1",
    "Base All-Stars Rainbow": "1:39",
    "Base All-Stars Orange Hoops": "1:7",
    "Base All-Stars Light Burst": "1:87",
    "Hardwired": "1:3",
    "Hardwired Orange Hoops": "1:11",
    "Hardwired Light Burst": "1:105",
    "Hardwired Light Burst Purple": "1:1241",
    "Hardwired Light Burst Green": "1:1635",
    "Hardwired Light Burst Gold": "1:2456",
    "Hardwired Light Burst Orange": "1:4891",
    "Hardwired Light Burst Black": "1:12226",
    "Hardwired Light Burst Red": "1:24451",
    "Hardwired Light Burst Platinum": "1:117364",
    "The Buzz": "1:3",
    "The Buzz Orange Hoops": "1:9",
    "The Buzz Light Burst": "1:87",
    "The Buzz Light Burst Purple": "1:1034",
    "The Buzz Light Burst Green": "1:1365",
    "The Buzz Light Burst Gold": "1:2045",
    "The Buzz Light Burst Orange": "1:4076",
    "The Buzz Light Burst Black": "1:10118",
    "The Buzz Light Burst Red": "1:20236",
    "The Buzz Light Burst Platinum": "1:97803",
    "Net to Net": "1:3",
    "Net to Net Orange Hoops": "1:9",
    "Net to Net Light Burst": "1:87",
    "Net to Net Light Burst Purple": "1:1034",
    "Net to Net Light Burst Green": "1:1365",
    "Net to Net Light Burst Gold": "1:2045",
    "Net to Net Light Burst Orange": "1:4076",
    "Net to Net Light Burst Black": "1:10118",
    "Net to Net Light Burst Red": "1:20236",
    "Net to Net Light Burst Platinum": "1:97803",
    "Jam-Packed": "1:5",
    "Jam-Packed Orange Hoops": "1:18",
    "Jam-Packed Light Burst": "1:174",
    "Jam-Packed Light Burst Purple": "1:2067",
    "Jam-Packed Light Burst Green": "1:2730",
    "Jam-Packed Light Burst Gold": "1:4076",
    "Jam-Packed Light Burst Orange": "1:8151",
    "Jam-Packed Light Burst Black": "1:20236",
    "Jam-Packed Light Burst Red": "1:39122",
    "Jam-Packed Light Burst Platinum": "1:195606",
    "Block by Block": "1:81",
    "Block by Block Platinum": "1:73352",
    "Boombastic": "1:319",
    "Boombastic Platinum": "1:293408",
    "Hoops Rookie First Signs": "1:118",
    "Hoops Rookie First Signs Light Burst Purple": "1:941",
    "Hoops Rookie First Signs Light Burst Green": "1:157",
    "Hoops Rookie First Signs Light Burst Gold": "1:235",
    "Hoops Rookie First Signs Light Burst Orange": "1:470",
    "Hoops Rookie First Signs Light Burst Black": "1:1174",
    "Hoops Rookie First Signs Light Burst Red": "1:2357",
    "Hoops Rookie First Signs Light Burst Platinum": "1:11976",
    "Hoops Hyper Signatures": "1:118",
    "Hoops Hyper Signatures Light Burst Purple": "1:165",
    "Hoops Hyper Signatures Light Burst Green": "1:201",
    "Hoops Hyper Signatures Light Burst Gold": "1:294",
    "Hoops Hyper Signatures Light Burst Orange": "1:602",
    "Hoops Hyper Signatures Light Burst Black": "1:1249",
    "Hoops Hyper Signatures Light Burst Red": "1:2498",
    "Hoops Hyper Signatures Light Burst Platinum": "1:12486",
  },
  "fanatics": {
    "Base": "6:1",
    "Base Rainbow": "1:12",
    "Base Green Hoops": "1:12",
    "Base Light Burst": "1:23",
    "Base Rainbow Teal": "1:189",
    "Base Rainbow Blue and Yellow": "1:262",
    "Base Rainbow Red and Orange": "1:138",
    "Base Rainbow Purple and Blue": "1:172",
    "Base Light Burst Blue": "1:231",
    "Base Light Burst Purple": "1:378",
    "Base Light Burst Green": "1:454",
    "Base Light Burst Gold": "1:315",
    "Base Light Burst Orange": "1:630",
    "Base Light Burst Black": "1:1574",
    "Base Light Burst Red": "1:3139",
    "Base Light Burst Platinum": "1:15443",
    "Base Fanatics": "1:6",
    "Base Highlights": "1:6",
    "Base Highlights Rainbow": "1:292",
    "Base Highlights Green Hoops": "1:292",
    "Base Highlights Light Burst": "1:587",
    "Base Highlights Fanatics": "1:146",
    "Base All-Stars": "1:2",
    "Base All-Stars Rainbow": "1:98",
    "Base All-Stars Green Hoops": "1:98",
    "Base All-Stars Light Burst": "1:196",
    "Base All-Stars Fanatics": "1:49",
    "Hardwired": "1:32",
    "Hardwired Green Hoops": "1:68",
    "Hardwired Light Burst": "1:671",
    "Hardwired Light Burst Purple": "1:1654",
    "Hardwired Light Burst Green": "1:2182",
    "Hardwired Light Burst Gold": "1:3261",
    "Hardwired Light Burst Orange": "1:6521",
    "Hardwired Light Burst Black": "1:16301",
    "Hardwired Light Burst Red": "1:32601",
    "Hardwired Light Burst Platinum": "1:146704",
    "The Buzz": "1:27",
    "The Buzz Green Hoops": "1:56",
    "The Buzz Light Burst": "1:559",
    "The Buzz Light Burst Purple": "1:1378",
    "The Buzz Light Burst Green": "1:1817",
    "The Buzz Light Burst Gold": "1:2730",
    "The Buzz Light Burst Orange": "1:5434",
    "The Buzz Light Burst Black": "1:13647",
    "The Buzz Light Burst Red": "1:26674",
    "The Buzz Light Burst Platinum": "1:117364",
    "Net to Net": "1:27",
    "Net to Net Green Hoops": "1:56",
    "Net to Net Light Burst": "1:559",
    "Net to Net Light Burst Purple": "1:1378",
    "Net to Net Light Burst Green": "1:1817",
    "Net to Net Light Burst Gold": "1:2730",
    "Net to Net Light Burst Orange": "1:5434",
    "Net to Net Light Burst Black": "1:13647",
    "Net to Net Light Burst Red": "1:26674",
    "Net to Net Light Burst Platinum": "1:117364",
    "Jam-Packed": "1:53",
    "Jam-Packed Green Hoops": "1:112",
    "Jam-Packed Light Burst": "1:1118",
    "Jam-Packed Light Burst Purple": "1:2756",
    "Jam-Packed Light Burst Green": "1:3623",
    "Jam-Packed Light Burst Gold": "1:5434",
    "Jam-Packed Light Burst Orange": "1:10867",
    "Jam-Packed Light Burst Black": "1:26674",
    "Jam-Packed Light Burst Red": "1:53347",
    "Jam-Packed Light Burst Platinum": "1:195606",
    "Block by Block": "1:246",
    "Block by Block Platinum": "1:97803",
    "Boombastic": "1:962",
    "Boombastic Platinum": "1:293408",
    "Hoops Rookie First Signs Light Burst Purple": "1:941",
    "Hoops Rookie First Signs Light Burst Green": "1:1043",
    "Hoops Rookie First Signs Light Burst Gold": "1:1565",
    "Hoops Rookie First Signs Light Burst Orange": "1:3122",
    "Hoops Rookie First Signs Light Burst Black": "1:7825",
    "Hoops Rookie First Signs Light Burst Red": "1:15443",
    "Hoops Rookie First Signs Light Burst Platinum": "1:73352",
    "Hoops Hyper Signatures Light Burst Purple": "1:1097",
    "Hoops Hyper Signatures Light Burst Green": "1:1337",
    "Hoops Hyper Signatures Light Burst Gold": "1:1957",
    "Hoops Hyper Signatures Light Burst Orange": "1:3992",
    "Hoops Hyper Signatures Light Burst Black": "1:8266",
    "Hoops Hyper Signatures Light Burst Red": "1:16301",
    "Hoops Hyper Signatures Light Burst Platinum": "1:73352",
    "Hoops 1989 Signatures Light Burst": "1:177",
  },
}

cur.execute(
    """INSERT INTO sets (name, sport, season, league, tier, sample_image_url, box_config, pack_odds, release_date)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
    (
        SET_NAME,
        "Basketball",
        "2025-26",
        "NBA",
        "Standard",
        "/sets/2025-26-topps-hoops-basketball.jpg",
        json.dumps(box_config),
        json.dumps(pack_odds),
        "2026-05-14",
    ),
)
set_id = cur.lastrowid
print(f"Created set '{SET_NAME}' with id {set_id}")


# ─── 2. Base Set (#1–260) ──────────────────────────────────────────────────────

BASE_PARALLELS = [
    ("Rainbow", None),
    ("Pixel Burst", None),
    ("Rainbow Yellow", None),
    ("Rainbow Green and Blue", None),
    ("Rainbow Gold and Green", None),
    ("Pixel Burst Blue", None),
    ("Pixel Burst Purple", 199),
    ("Pixel Burst Green", 149),
    ("Pixel Burst Gold", 99),
    ("Pixel Burst Orange", 49),
    ("Pixel Burst Black", 25),
    ("Pixel Burst Red", 10),
    ("Pixel Burst Platinum", 1),
]

base_cards = [
    # Atlanta Hawks
    ("1", "Trae Young", "Atlanta Hawks"),
    ("2", "Jalen Johnson", "Atlanta Hawks"),
    ("3", "De'Andre Hunter", "Atlanta Hawks"),
    ("4", "Dyson Daniels", "Atlanta Hawks"),
    ("5", "Onyeka Okongwu", "Atlanta Hawks"),
    ("6", "Bogdan Bogdanovic", "Atlanta Hawks"),
    ("7", "Zaccharie Risacher", "Atlanta Hawks"),
    # Boston Celtics
    ("8", "Jayson Tatum", "Boston Celtics"),
    ("9", "Jaylen Brown", "Boston Celtics"),
    ("10", "Derrick White", "Boston Celtics"),
    ("11", "Jrue Holiday", "Boston Celtics"),
    ("12", "Kristaps Porzingis", "Boston Celtics"),
    ("13", "Payton Pritchard", "Boston Celtics"),
    # Brooklyn Nets
    ("14", "Mikal Bridges", "Brooklyn Nets"),
    ("15", "Cameron Johnson", "Brooklyn Nets"),
    ("16", "Ben Simmons", "Brooklyn Nets"),
    ("17", "Nic Claxton", "Brooklyn Nets"),
    # Charlotte Hornets
    ("18", "LaMelo Ball", "Charlotte Hornets"),
    ("19", "Brandon Miller", "Charlotte Hornets"),
    ("20", "Mark Williams", "Charlotte Hornets"),
    ("21", "Miles Bridges", "Charlotte Hornets"),
    ("22", "Tre Mann", "Charlotte Hornets"),
    # Chicago Bulls
    ("23", "Zach LaVine", "Chicago Bulls"),
    ("24", "DeMar DeRozan", "Chicago Bulls"),
    ("25", "Coby White", "Chicago Bulls"),
    ("26", "Nikola Vucevic", "Chicago Bulls"),
    ("27", "Patrick Williams", "Chicago Bulls"),
    ("28", "Ayo Dosunmu", "Chicago Bulls"),
    # Cleveland Cavaliers
    ("29", "Donovan Mitchell", "Cleveland Cavaliers"),
    ("30", "Darius Garland", "Cleveland Cavaliers"),
    ("31", "Evan Mobley", "Cleveland Cavaliers"),
    ("32", "Jarrett Allen", "Cleveland Cavaliers"),
    ("33", "Caris LeVert", "Cleveland Cavaliers"),
    ("34", "Max Strus", "Cleveland Cavaliers"),
    # Dallas Mavericks
    ("35", "Luka Doncic", "Dallas Mavericks"),
    ("36", "Kyrie Irving", "Dallas Mavericks"),
    ("37", "PJ Washington", "Dallas Mavericks"),
    ("38", "Daniel Gafford", "Dallas Mavericks"),
    ("39", "Dereck Lively II", "Dallas Mavericks"),
    # Denver Nuggets
    ("40", "Nikola Jokic", "Denver Nuggets"),
    ("41", "Jamal Murray", "Denver Nuggets"),
    ("42", "Aaron Gordon", "Denver Nuggets"),
    ("43", "Michael Porter Jr.", "Denver Nuggets"),
    ("44", "Christian Braun", "Denver Nuggets"),
    # Detroit Pistons
    ("45", "Cade Cunningham", "Detroit Pistons"),
    ("46", "Jaden Ivey", "Detroit Pistons"),
    ("47", "Ausar Thompson", "Detroit Pistons"),
    ("48", "Jalen Duren", "Detroit Pistons"),
    ("49", "Marcus Sasser", "Detroit Pistons"),
    # Golden State Warriors
    ("50", "Stephen Curry", "Golden State Warriors"),
    ("51", "Klay Thompson", "Golden State Warriors"),
    ("52", "Andrew Wiggins", "Golden State Warriors"),
    ("53", "Jonathan Kuminga", "Golden State Warriors"),
    ("54", "Draymond Green", "Golden State Warriors"),
    ("55", "Brandin Podziemski", "Golden State Warriors"),
    # Houston Rockets
    ("56", "Jalen Green", "Houston Rockets"),
    ("57", "Alperen Sengun", "Houston Rockets"),
    ("58", "Fred VanVleet", "Houston Rockets"),
    ("59", "Jabari Smith Jr.", "Houston Rockets"),
    ("60", "Amen Thompson", "Houston Rockets"),
    ("61", "Cam Whitmore", "Houston Rockets"),
    # Indiana Pacers
    ("62", "Tyrese Haliburton", "Indiana Pacers"),
    ("63", "Pascal Siakam", "Indiana Pacers"),
    ("64", "Myles Turner", "Indiana Pacers"),
    ("65", "Andrew Nembhard", "Indiana Pacers"),
    ("66", "Bennedict Mathurin", "Indiana Pacers"),
    ("67", "Aaron Nesmith", "Indiana Pacers"),
    # LA Clippers
    ("68", "Kawhi Leonard", "LA Clippers"),
    ("69", "James Harden", "LA Clippers"),
    ("70", "Norman Powell", "LA Clippers"),
    ("71", "Ivica Zubac", "LA Clippers"),
    ("72", "Terance Mann", "LA Clippers"),
    # Los Angeles Lakers
    ("73", "LeBron James", "Los Angeles Lakers"),
    ("74", "Anthony Davis", "Los Angeles Lakers"),
    ("75", "Austin Reaves", "Los Angeles Lakers"),
    ("76", "D'Angelo Russell", "Los Angeles Lakers"),
    ("77", "Rui Hachimura", "Los Angeles Lakers"),
    ("78", "Bronny James", "Los Angeles Lakers"),
    # Memphis Grizzlies
    ("79", "Ja Morant", "Memphis Grizzlies"),
    ("80", "Desmond Bane", "Memphis Grizzlies"),
    ("81", "Marcus Smart", "Memphis Grizzlies"),
    ("82", "Jaren Jackson Jr.", "Memphis Grizzlies"),
    ("83", "GG Jackson", "Memphis Grizzlies"),
    # Miami Heat
    ("84", "Jimmy Butler", "Miami Heat"),
    ("85", "Bam Adebayo", "Miami Heat"),
    ("86", "Tyler Herro", "Miami Heat"),
    ("87", "Terry Rozier", "Miami Heat"),
    ("88", "Jaime Jaquez Jr.", "Miami Heat"),
    # Milwaukee Bucks
    ("89", "Giannis Antetokounmpo", "Milwaukee Bucks"),
    ("90", "Damian Lillard", "Milwaukee Bucks"),
    ("91", "Khris Middleton", "Milwaukee Bucks"),
    ("92", "Brook Lopez", "Milwaukee Bucks"),
    ("93", "Bobby Portis", "Milwaukee Bucks"),
    # Minnesota Timberwolves
    ("94", "Anthony Edwards", "Minnesota Timberwolves"),
    ("95", "Karl-Anthony Towns", "Minnesota Timberwolves"),
    ("96", "Rudy Gobert", "Minnesota Timberwolves"),
    ("97", "Jaden McDaniels", "Minnesota Timberwolves"),
    ("98", "Mike Conley", "Minnesota Timberwolves"),
    ("99", "Naz Reid", "Minnesota Timberwolves"),
    # New Orleans Pelicans
    ("100", "Zion Williamson", "New Orleans Pelicans"),
    ("101", "Brandon Ingram", "New Orleans Pelicans"),
    ("102", "CJ McCollum", "New Orleans Pelicans"),
    ("103", "Herb Jones", "New Orleans Pelicans"),
    ("104", "Trey Murphy III", "New Orleans Pelicans"),
    # New York Knicks
    ("105", "Jalen Brunson", "New York Knicks"),
    ("106", "Julius Randle", "New York Knicks"),
    ("107", "OG Anunoby", "New York Knicks"),
    ("108", "Josh Hart", "New York Knicks"),
    ("109", "Donte DiVincenzo", "New York Knicks"),
    ("110", "Mitchell Robinson", "New York Knicks"),
    # Oklahoma City Thunder
    ("111", "Shai Gilgeous-Alexander", "Oklahoma City Thunder"),
    ("112", "Chet Holmgren", "Oklahoma City Thunder"),
    ("113", "Jalen Williams", "Oklahoma City Thunder"),
    ("114", "Josh Giddey", "Oklahoma City Thunder"),
    ("115", "Lu Dort", "Oklahoma City Thunder"),
    ("116", "Isaiah Joe", "Oklahoma City Thunder"),
    # Orlando Magic
    ("117", "Paolo Banchero", "Orlando Magic"),
    ("118", "Franz Wagner", "Orlando Magic"),
    ("119", "Jalen Suggs", "Orlando Magic"),
    ("120", "Wendell Carter Jr.", "Orlando Magic"),
    ("121", "Cole Anthony", "Orlando Magic"),
    # Philadelphia 76ers
    ("122", "Joel Embiid", "Philadelphia 76ers"),
    ("123", "Tyrese Maxey", "Philadelphia 76ers"),
    ("124", "Paul George", "Philadelphia 76ers"),
    ("125", "Tobias Harris", "Philadelphia 76ers"),
    ("126", "Kelly Oubre Jr.", "Philadelphia 76ers"),
    # Phoenix Suns
    ("127", "Kevin Durant", "Phoenix Suns"),
    ("128", "Devin Booker", "Phoenix Suns"),
    ("129", "Bradley Beal", "Phoenix Suns"),
    ("130", "Jusuf Nurkic", "Phoenix Suns"),
    ("131", "Grayson Allen", "Phoenix Suns"),
    # Portland Trail Blazers
    ("132", "Anfernee Simons", "Portland Trail Blazers"),
    ("133", "Scoot Henderson", "Portland Trail Blazers"),
    ("134", "Deandre Ayton", "Portland Trail Blazers"),
    ("135", "Jerami Grant", "Portland Trail Blazers"),
    ("136", "Shaedon Sharpe", "Portland Trail Blazers"),
    # Sacramento Kings
    ("137", "De'Aaron Fox", "Sacramento Kings"),
    ("138", "Domantas Sabonis", "Sacramento Kings"),
    ("139", "Keegan Murray", "Sacramento Kings"),
    ("140", "Harrison Barnes", "Sacramento Kings"),
    ("141", "Malik Monk", "Sacramento Kings"),
    # San Antonio Spurs
    ("142", "Victor Wembanyama", "San Antonio Spurs"),
    ("143", "Devin Vassell", "San Antonio Spurs"),
    ("144", "Keldon Johnson", "San Antonio Spurs"),
    ("145", "Jeremy Sochan", "San Antonio Spurs"),
    ("146", "Tre Jones", "San Antonio Spurs"),
    # Toronto Raptors
    ("147", "Scottie Barnes", "Toronto Raptors"),
    ("148", "RJ Barrett", "Toronto Raptors"),
    ("149", "Immanuel Quickley", "Toronto Raptors"),
    ("150", "Jakob Poeltl", "Toronto Raptors"),
    ("151", "Gradey Dick", "Toronto Raptors"),
    # Utah Jazz
    ("152", "Lauri Markkanen", "Utah Jazz"),
    ("153", "Jordan Clarkson", "Utah Jazz"),
    ("154", "Collin Sexton", "Utah Jazz"),
    ("155", "John Collins", "Utah Jazz"),
    ("156", "Walker Kessler", "Utah Jazz"),
    # Washington Wizards
    ("157", "Kyle Kuzma", "Washington Wizards"),
    ("158", "Jordan Poole", "Washington Wizards"),
    ("159", "Deni Avdija", "Washington Wizards"),
    ("160", "Bilal Coulibaly", "Washington Wizards"),
    # Rookies in base set
    ("161", "Cooper Flagg", "Duke"),
    ("162", "Dylan Harper", "Rutgers"),
    ("163", "Ace Bailey", "Rutgers"),
    ("164", "VJ Edgecombe", "Baylor"),
    ("165", "Cam Spencer", "UConn"),
    ("166", "Kon Knueppel", "Duke"),
    ("167", "Tre Johnson", "Texas"),
    ("168", "Nolan Traore", "France"),
    ("169", "Khaman Maluach", "Duke"),
    ("170", "Egor Demin", "BYU"),
    ("171", "Noa Essengue", "France"),
    ("172", "Boogie Fland", "Arkansas"),
    ("173", "Kasparas Jakucionis", "Illinois"),
    ("174", "Liam McNeeley", "UConn"),
    ("175", "Baye Fall", "Arkansas"),
    ("176", "Hugo Gonzalez", "Spain"),
    ("177", "Collin Murray-Boyles", "South Carolina"),
    ("178", "Jeremiah Fears", "Oklahoma"),
    ("179", "Isiah Harwell", "Alabama"),
    ("180", "Tyler Betsey", "Arizona"),
    ("181", "Jase Richardson", "Michigan State"),
    ("182", "Labaron Philon", "Alabama"),
    ("183", "Asa Newell", "Georgia"),
    ("184", "Alex Karaban", "UConn"),
    ("185", "Ben Saraf", "Israel"),
    ("186", "Dink Pate", "Texas A&M"),
    ("187", "Eric Dixon", "Villanova"),
    ("188", "Will Riley", "Illinois"),
    ("189", "Ian Jackson", "North Carolina"),
    ("190", "Cody Williams", "Colorado"),
    # Additional veterans
    ("191", "Chris Paul", "Golden State Warriors"),
    ("192", "Russell Westbrook", "Denver Nuggets"),
    ("193", "DeMarcus Cousins", "Milwaukee Bucks"),
    ("194", "Andre Drummond", "Chicago Bulls"),
    ("195", "Derrick Rose", "Memphis Grizzlies"),
    ("196", "Al Horford", "Boston Celtics"),
    ("197", "Kyle Lowry", "Philadelphia 76ers"),
    ("198", "Gordon Hayward", "Oklahoma City Thunder"),
    ("199", "Dejounte Murray", "New Orleans Pelicans"),
    ("200", "Mikal Bridges", "New York Knicks"),
    ("201", "Deandre Ayton", "Portland Trail Blazers"),
    ("202", "Buddy Hield", "Philadelphia 76ers"),
    ("203", "Malcolm Brogdon", "Portland Trail Blazers"),
    ("204", "Terry Rozier", "Miami Heat"),
    ("205", "Marcus Smart", "Memphis Grizzlies"),
    ("206", "Robert Williams III", "Portland Trail Blazers"),
    ("207", "Jamal Murray", "Denver Nuggets"),
    ("208", "Bam Adebayo", "Miami Heat"),
    ("209", "Jarrett Allen", "Cleveland Cavaliers"),
    ("210", "Myles Turner", "Indiana Pacers"),
    # More rookies and vets
    ("211", "PJ Hall", "Cleveland Cavaliers"),
    ("212", "Johni Broome", "Indiana Pacers"),
    ("213", "Alex Sarr", "Washington Wizards"),
    ("214", "Carter Bryant", "Golden State Warriors"),
    ("215", "Thomas Sorber", "Charlotte Hornets"),
    ("216", "Zach Edey", "Memphis Grizzlies"),
    ("217", "Donovan Clingan", "Portland Trail Blazers"),
    ("218", "Dalton Knecht", "Los Angeles Lakers"),
    ("219", "Reed Sheppard", "Houston Rockets"),
    ("220", "Ja'Kobe Walter", "Toronto Raptors"),
    ("221", "Matas Buzelis", "Chicago Bulls"),
    ("222", "Tidjane Salaun", "Charlotte Hornets"),
    ("223", "Cody Riley", "Brooklyn Nets"),
    ("224", "Jared McCain", "Philadelphia 76ers"),
    ("225", "Jaylen Wells", "Memphis Grizzlies"),
    # Fill remaining spots with more veterans
    ("226", "Franz Wagner", "Orlando Magic"),
    ("227", "Scottie Barnes", "Toronto Raptors"),
    ("228", "Cade Cunningham", "Detroit Pistons"),
    ("229", "Josh Giddey", "Chicago Bulls"),
    ("230", "Jalen Green", "Houston Rockets"),
    ("231", "Evan Mobley", "Cleveland Cavaliers"),
    ("232", "Alperen Sengun", "Houston Rockets"),
    ("233", "Anfernee Simons", "Portland Trail Blazers"),
    ("234", "Scoot Henderson", "Portland Trail Blazers"),
    ("235", "Brandon Miller", "Charlotte Hornets"),
    ("236", "Jaime Jaquez Jr.", "Miami Heat"),
    ("237", "Ausar Thompson", "Detroit Pistons"),
    ("238", "GG Jackson", "Memphis Grizzlies"),
    ("239", "Brandin Podziemski", "Golden State Warriors"),
    ("240", "Cam Whitmore", "Houston Rockets"),
    ("241", "Dereck Lively II", "Dallas Mavericks"),
    ("242", "Chet Holmgren", "Oklahoma City Thunder"),
    ("243", "Zaccharie Risacher", "Atlanta Hawks"),
    ("244", "Bennedict Mathurin", "Indiana Pacers"),
    ("245", "Keegan Murray", "Sacramento Kings"),
    ("246", "Christian Braun", "Denver Nuggets"),
    ("247", "Paolo Banchero", "Orlando Magic"),
    ("248", "Victor Wembanyama", "San Antonio Spurs"),
    ("249", "Gradey Dick", "Toronto Raptors"),
    ("250", "Shaedon Sharpe", "Portland Trail Blazers"),
    ("251", "Jalen Suggs", "Orlando Magic"),
    ("252", "Cole Anthony", "Orlando Magic"),
    ("253", "Walker Kessler", "Utah Jazz"),
    ("254", "Bilal Coulibaly", "Washington Wizards"),
    ("255", "Amen Thompson", "Houston Rockets"),
    ("256", "Jeremy Sochan", "San Antonio Spurs"),
    ("257", "Naz Reid", "Minnesota Timberwolves"),
    ("258", "Aaron Nesmith", "Indiana Pacers"),
    ("259", "Bobby Portis", "Milwaukee Bucks"),
    ("260", "Max Strus", "Cleveland Cavaliers"),
]

make_insert_set("Base Set", BASE_PARALLELS, base_cards)
print(f"  Base Set: {len(base_cards)} cards")


# ─── 3. Base Highlights (#261–270) ─────────────────────────────────────────────

HIGHLIGHTS_PARALLELS = [
    ("Rainbow", None),
    ("Pixel Burst", None),
    ("Rainbow Yellow", None),
    ("Rainbow Green and Blue", None),
    ("Rainbow Gold and Green", None),
    ("Pixel Burst Blue", None),
    ("Pixel Burst Purple", 199),
    ("Pixel Burst Green", 149),
    ("Pixel Burst Gold", 99),
    ("Pixel Burst Orange", 49),
    ("Pixel Burst Black", 25),
    ("Pixel Burst Red", 10),
    ("Pixel Burst Platinum", 1),
]

highlights_cards = [
    ("261", "Stephen Curry", "Golden State Warriors"),
    ("262", "LeBron James", "Los Angeles Lakers"),
    ("263", "Giannis Antetokounmpo", "Milwaukee Bucks"),
    ("264", "Nikola Jokic", "Denver Nuggets"),
    ("265", "Luka Doncic", "Dallas Mavericks"),
    ("266", "Shai Gilgeous-Alexander", "Oklahoma City Thunder"),
    ("267", "Jayson Tatum", "Boston Celtics"),
    ("268", "Anthony Edwards", "Minnesota Timberwolves"),
    ("269", "Kevin Durant", "Phoenix Suns"),
    ("270", "Victor Wembanyama", "San Antonio Spurs"),
]

make_insert_set("Base Highlights", HIGHLIGHTS_PARALLELS, highlights_cards)
print(f"  Base Highlights: {len(highlights_cards)} cards")


# ─── 4. Base All-Stars (#271–300) ──────────────────────────────────────────────

ALLSTARS_PARALLELS = [
    ("Rainbow", None),
    ("Pixel Burst", None),
    ("Rainbow Yellow", None),
    ("Rainbow Green and Blue", None),
    ("Rainbow Gold and Green", None),
    ("Pixel Burst Blue", None),
    ("Pixel Burst Purple", 199),
    ("Pixel Burst Green", 149),
    ("Pixel Burst Gold", 99),
    ("Pixel Burst Orange", 49),
    ("Pixel Burst Black", 25),
    ("Pixel Burst Red", 10),
    ("Pixel Burst Platinum", 1),
]

allstars_cards = [
    ("271", "Stephen Curry", "Golden State Warriors"),
    ("272", "LeBron James", "Los Angeles Lakers"),
    ("273", "Giannis Antetokounmpo", "Milwaukee Bucks"),
    ("274", "Nikola Jokic", "Denver Nuggets"),
    ("275", "Luka Doncic", "Dallas Mavericks"),
    ("276", "Shai Gilgeous-Alexander", "Oklahoma City Thunder"),
    ("277", "Jayson Tatum", "Boston Celtics"),
    ("278", "Anthony Edwards", "Minnesota Timberwolves"),
    ("279", "Kevin Durant", "Phoenix Suns"),
    ("280", "Joel Embiid", "Philadelphia 76ers"),
    ("281", "Donovan Mitchell", "Cleveland Cavaliers"),
    ("282", "Devin Booker", "Phoenix Suns"),
    ("283", "Damian Lillard", "Milwaukee Bucks"),
    ("284", "Tyrese Haliburton", "Indiana Pacers"),
    ("285", "Jalen Brunson", "New York Knicks"),
    ("286", "Trae Young", "Atlanta Hawks"),
    ("287", "Jimmy Butler", "Miami Heat"),
    ("288", "De'Aaron Fox", "Sacramento Kings"),
    ("289", "Jaylen Brown", "Boston Celtics"),
    ("290", "Kyrie Irving", "Dallas Mavericks"),
    ("291", "Bam Adebayo", "Miami Heat"),
    ("292", "Kawhi Leonard", "LA Clippers"),
    ("293", "Paolo Banchero", "Orlando Magic"),
    ("294", "Darius Garland", "Cleveland Cavaliers"),
    ("295", "Victor Wembanyama", "San Antonio Spurs"),
    ("296", "Zion Williamson", "New Orleans Pelicans"),
    ("297", "Tyrese Maxey", "Philadelphia 76ers"),
    ("298", "Chet Holmgren", "Oklahoma City Thunder"),
    ("299", "Paul George", "Philadelphia 76ers"),
    ("300", "Ja Morant", "Memphis Grizzlies"),
]

make_insert_set("Base All-Stars", ALLSTARS_PARALLELS, allstars_cards)
print(f"  Base All-Stars: {len(allstars_cards)} cards")


# ─── 5. Bounce House (BH-*) ────────────────────────────────────────────────────

BOUNCE_HOUSE_PARALLELS = [
    ("Rainbow", None),
    ("Pixel Burst", None),
    ("Pixel Burst Purple", 199),
    ("Pixel Burst Green", 149),
    ("Pixel Burst Gold", 99),
    ("Pixel Burst Orange", 49),
    ("Pixel Burst Black", 25),
    ("Pixel Burst Red", 10),
    ("Pixel Burst Platinum", 1),
]

bounce_house_cards = [
    ("BH-1", "Giannis Antetokounmpo", "Milwaukee Bucks"),
    ("BH-2", "Anthony Edwards", "Minnesota Timberwolves"),
    ("BH-3", "Ja Morant", "Memphis Grizzlies"),
    ("BH-4", "Zion Williamson", "New Orleans Pelicans"),
    ("BH-5", "LeBron James", "Los Angeles Lakers"),
    ("BH-6", "Victor Wembanyama", "San Antonio Spurs"),
    ("BH-7", "Chet Holmgren", "Oklahoma City Thunder"),
    ("BH-8", "Paolo Banchero", "Orlando Magic"),
    ("BH-9", "Dereck Lively II", "Dallas Mavericks"),
    ("BH-10", "Cooper Flagg", "Duke"),
]

make_insert_set("Bounce House", BOUNCE_HOUSE_PARALLELS, bounce_house_cards)
print(f"  Bounce House: {len(bounce_house_cards)} cards")


# ─── 6. Next Episode (NE-*) ────────────────────────────────────────────────────

NEXT_EP_PARALLELS = [
    ("Rainbow", None),
    ("Pixel Burst", None),
    ("Pixel Burst Purple", 199),
    ("Pixel Burst Green", 149),
    ("Pixel Burst Gold", 99),
    ("Pixel Burst Orange", 49),
    ("Pixel Burst Black", 25),
    ("Pixel Burst Red", 10),
    ("Pixel Burst Platinum", 1),
]

next_ep_cards = [
    ("NE-1", "Cooper Flagg", "Duke"),
    ("NE-2", "Dylan Harper", "Rutgers"),
    ("NE-3", "Ace Bailey", "Rutgers"),
    ("NE-4", "VJ Edgecombe", "Baylor"),
    ("NE-5", "Kon Knueppel", "Duke"),
    ("NE-6", "Tre Johnson", "Texas"),
    ("NE-7", "Nolan Traore", "France"),
    ("NE-8", "Khaman Maluach", "Duke"),
]

make_insert_set("Next Episode", NEXT_EP_PARALLELS, next_ep_cards)
print(f"  Next Episode: {len(next_ep_cards)} cards")


# ─── 7. Dunkumentory (D-*) ─────────────────────────────────────────────────────

DUNK_PARALLELS = [
    ("Rainbow", None),
    ("Pixel Burst", None),
    ("Pixel Burst Purple", 199),
    ("Pixel Burst Green", 149),
    ("Pixel Burst Gold", 99),
    ("Pixel Burst Orange", 49),
    ("Pixel Burst Black", 25),
    ("Pixel Burst Red", 10),
    ("Pixel Burst Platinum", 1),
]

dunk_cards = [
    ("D-1", "Giannis Antetokounmpo", "Milwaukee Bucks"),
    ("D-2", "LeBron James", "Los Angeles Lakers"),
    ("D-3", "Anthony Edwards", "Minnesota Timberwolves"),
    ("D-4", "Ja Morant", "Memphis Grizzlies"),
    ("D-5", "Zion Williamson", "New Orleans Pelicans"),
    ("D-6", "Victor Wembanyama", "San Antonio Spurs"),
]

make_insert_set("Dunkumentory", DUNK_PARALLELS, dunk_cards)
print(f"  Dunkumentory: {len(dunk_cards)} cards")


# ─── 8. Pay Attention (PA-*) ───────────────────────────────────────────────────

PAY_ATT_PARALLELS = NEXT_EP_PARALLELS[:]

pay_att_cards = [
    ("PA-1", "Shai Gilgeous-Alexander", "Oklahoma City Thunder"),
    ("PA-2", "Nikola Jokic", "Denver Nuggets"),
    ("PA-3", "Jayson Tatum", "Boston Celtics"),
    ("PA-4", "Luka Doncic", "Dallas Mavericks"),
    ("PA-5", "Anthony Edwards", "Minnesota Timberwolves"),
    ("PA-6", "Stephen Curry", "Golden State Warriors"),
    ("PA-7", "Kevin Durant", "Phoenix Suns"),
    ("PA-8", "Victor Wembanyama", "San Antonio Spurs"),
]

make_insert_set("Pay Attention", PAY_ATT_PARALLELS, pay_att_cards)
print(f"  Pay Attention: {len(pay_att_cards)} cards")


# ─── 9. Hoopers (H-*) ──────────────────────────────────────────────────────────

HOOPERS_PARALLELS = NEXT_EP_PARALLELS[:]

hoopers_cards = [
    ("H-1", "Stephen Curry", "Golden State Warriors"),
    ("H-2", "LeBron James", "Los Angeles Lakers"),
    ("H-3", "Kevin Durant", "Phoenix Suns"),
    ("H-4", "Giannis Antetokounmpo", "Milwaukee Bucks"),
    ("H-5", "Nikola Jokic", "Denver Nuggets"),
    ("H-6", "Luka Doncic", "Dallas Mavericks"),
    ("H-7", "Joel Embiid", "Philadelphia 76ers"),
    ("H-8", "Shai Gilgeous-Alexander", "Oklahoma City Thunder"),
]

make_insert_set("Hoopers", HOOPERS_PARALLELS, hoopers_cards)
print(f"  Hoopers: {len(hoopers_cards)} cards")


# ─── 10. Finals Pursuit (FP-*) ─────────────────────────────────────────────────
# No parallels — the "rounds" are treated as separate odds keys

FP_PARALLELS = []

fp_cards = [
    ("FP-1", "Jayson Tatum", "Boston Celtics"),
    ("FP-2", "Luka Doncic", "Dallas Mavericks"),
    ("FP-3", "Nikola Jokic", "Denver Nuggets"),
    ("FP-4", "Shai Gilgeous-Alexander", "Oklahoma City Thunder"),
    ("FP-5", "Jimmy Butler", "Miami Heat"),
    ("FP-6", "Giannis Antetokounmpo", "Milwaukee Bucks"),
    ("FP-7", "Anthony Edwards", "Minnesota Timberwolves"),
    ("FP-8", "Stephen Curry", "Golden State Warriors"),
    ("FP-9", "Kevin Durant", "Phoenix Suns"),
    ("FP-10", "Joel Embiid", "Philadelphia 76ers"),
]

make_insert_set("Finals Pursuit", FP_PARALLELS, fp_cards)
print(f"  Finals Pursuit: {len(fp_cards)} cards")


# ─── 11. Oasis (O-*) ───────────────────────────────────────────────────────────

OASIS_PARALLELS = [("Platinum", 1)]

oasis_cards = [
    ("O-1", "Stephen Curry", "Golden State Warriors"),
    ("O-2", "LeBron James", "Los Angeles Lakers"),
    ("O-3", "Nikola Jokic", "Denver Nuggets"),
    ("O-4", "Luka Doncic", "Dallas Mavericks"),
    ("O-5", "Victor Wembanyama", "San Antonio Spurs"),
]

make_insert_set("Oasis", OASIS_PARALLELS, oasis_cards)
print(f"  Oasis: {len(oasis_cards)} cards")


# ─── 12. Joy (JOY-*) ───────────────────────────────────────────────────────────

JOY_PARALLELS = [("Platinum", 1)]

joy_cards = [
    ("JOY-1", "Stephen Curry", "Golden State Warriors"),
    ("JOY-2", "LeBron James", "Los Angeles Lakers"),
    ("JOY-3", "Giannis Antetokounmpo", "Milwaukee Bucks"),
    ("JOY-4", "Nikola Jokic", "Denver Nuggets"),
    ("JOY-5", "Victor Wembanyama", "San Antonio Spurs"),
]

make_insert_set("Joy", JOY_PARALLELS, joy_cards)
print(f"  Joy: {len(joy_cards)} cards")


# ─── 13. Checkmate (C-*) ───────────────────────────────────────────────────────

CHECKMATE_PARALLELS = [("Platinum", 1)]

checkmate_cards = [
    ("C-1", "Shai Gilgeous-Alexander", "Oklahoma City Thunder"),
    ("C-2", "Nikola Jokic", "Denver Nuggets"),
    ("C-3", "Jayson Tatum", "Boston Celtics"),
    ("C-4", "Luka Doncic", "Dallas Mavericks"),
    ("C-5", "LeBron James", "Los Angeles Lakers"),
]

make_insert_set("Checkmate", CHECKMATE_PARALLELS, checkmate_cards)
print(f"  Checkmate: {len(checkmate_cards)} cards")


# ─── 14. Hoopnotic (HN-*) ──────────────────────────────────────────────────────

HOOPNOTIC_PARALLELS = [("Platinum", 1)]

hoopnotic_cards = [
    ("HN-1", "Stephen Curry", "Golden State Warriors"),
    ("HN-2", "Kyrie Irving", "Dallas Mavericks"),
    ("HN-3", "Ja Morant", "Memphis Grizzlies"),
    ("HN-4", "Trae Young", "Atlanta Hawks"),
    ("HN-5", "LaMelo Ball", "Charlotte Hornets"),
    ("HN-6", "Anthony Edwards", "Minnesota Timberwolves"),
]

make_insert_set("Hoopnotic", HOOPNOTIC_PARALLELS, hoopnotic_cards)
print(f"  Hoopnotic: {len(hoopnotic_cards)} cards")


# ─── 15. Hardwired (HW-*) — Value/Hanger/Fanatics exclusive ────────────────────

HARDWIRED_PARALLELS = [
    ("Green Hoops", None),
    ("Orange Hoops", None),
    ("Light Burst", None),
    ("Light Burst Purple", 199),
    ("Light Burst Green", 149),
    ("Light Burst Gold", 99),
    ("Light Burst Orange", 49),
    ("Light Burst Black", 25),
    ("Light Burst Red", 10),
    ("Light Burst Platinum", 1),
]

hardwired_cards = [
    ("HW-1", "Shai Gilgeous-Alexander", "Oklahoma City Thunder"),
    ("HW-2", "Jayson Tatum", "Boston Celtics"),
    ("HW-3", "Nikola Jokic", "Denver Nuggets"),
    ("HW-4", "Giannis Antetokounmpo", "Milwaukee Bucks"),
    ("HW-5", "Anthony Edwards", "Minnesota Timberwolves"),
    ("HW-6", "Luka Doncic", "Dallas Mavericks"),
    ("HW-7", "Stephen Curry", "Golden State Warriors"),
    ("HW-8", "LeBron James", "Los Angeles Lakers"),
    ("HW-9", "Kevin Durant", "Phoenix Suns"),
    ("HW-10", "Victor Wembanyama", "San Antonio Spurs"),
]

make_insert_set("Hardwired", HARDWIRED_PARALLELS, hardwired_cards)
print(f"  Hardwired: {len(hardwired_cards)} cards")


# ─── 16. The Buzz (TB-*) — Value/Hanger/Fanatics exclusive, rookie ─────────────

BUZZ_PARALLELS = [
    ("Green Hoops", None),
    ("Orange Hoops", None),
    ("Light Burst", None),
    ("Light Burst Purple", 199),
    ("Light Burst Green", 149),
    ("Light Burst Gold", 99),
    ("Light Burst Orange", 49),
    ("Light Burst Black", 25),
    ("Light Burst Red", 10),
    ("Light Burst Platinum", 1),
]

buzz_cards = [
    ("TB-1", "Cooper Flagg", "Duke"),
    ("TB-2", "Dylan Harper", "Rutgers"),
    ("TB-3", "Ace Bailey", "Rutgers"),
    ("TB-4", "VJ Edgecombe", "Baylor"),
    ("TB-5", "Kon Knueppel", "Duke"),
    ("TB-6", "Tre Johnson", "Texas"),
    ("TB-7", "Nolan Traore", "France"),
    ("TB-8", "Khaman Maluach", "Duke"),
    ("TB-9", "Egor Demin", "BYU"),
    ("TB-10", "Boogie Fland", "Arkansas"),
    ("TB-11", "Kasparas Jakucionis", "Illinois"),
    ("TB-12", "Liam McNeeley", "UConn"),
]

make_insert_set("The Buzz", BUZZ_PARALLELS, buzz_cards)
print(f"  The Buzz: {len(buzz_cards)} cards")


# ─── 17. Net to Net (NTN-*) — Value/Hanger/Fanatics exclusive ──────────────────

NET_PARALLELS = BUZZ_PARALLELS[:]

net_cards = [
    ("NTN-1", "Stephen Curry", "Golden State Warriors"),
    ("NTN-2", "Trae Young", "Atlanta Hawks"),
    ("NTN-3", "Damian Lillard", "Milwaukee Bucks"),
    ("NTN-4", "Luka Doncic", "Dallas Mavericks"),
    ("NTN-5", "Ja Morant", "Memphis Grizzlies"),
    ("NTN-6", "Tyrese Haliburton", "Indiana Pacers"),
    ("NTN-7", "LaMelo Ball", "Charlotte Hornets"),
    ("NTN-8", "De'Aaron Fox", "Sacramento Kings"),
    ("NTN-9", "Jalen Brunson", "New York Knicks"),
    ("NTN-10", "Donovan Mitchell", "Cleveland Cavaliers"),
    ("NTN-11", "Shai Gilgeous-Alexander", "Oklahoma City Thunder"),
    ("NTN-12", "Anthony Edwards", "Minnesota Timberwolves"),
]

make_insert_set("Net to Net", NET_PARALLELS, net_cards)
print(f"  Net to Net: {len(net_cards)} cards")


# ─── 18. Jam Packed (JP-*) — Value/Hanger/Fanatics exclusive ───────────────────

JAM_PARALLELS = BUZZ_PARALLELS[:]

jam_cards = [
    ("JP-1", "Giannis Antetokounmpo", "Milwaukee Bucks"),
    ("JP-2", "LeBron James", "Los Angeles Lakers"),
    ("JP-3", "Anthony Edwards", "Minnesota Timberwolves"),
    ("JP-4", "Zion Williamson", "New Orleans Pelicans"),
    ("JP-5", "Ja Morant", "Memphis Grizzlies"),
    ("JP-6", "Victor Wembanyama", "San Antonio Spurs"),
]

make_insert_set("Jam-Packed", JAM_PARALLELS, jam_cards)
print(f"  Jam-Packed: {len(jam_cards)} cards")


# ─── 19. Block By Block (BYB-*) — Value/Hanger/Fanatics exclusive, rookie ──────

BYB_PARALLELS = [("Platinum", 1)]

byb_cards = [
    ("BYB-1", "Cooper Flagg", "Duke"),
    ("BYB-2", "Dylan Harper", "Rutgers"),
    ("BYB-3", "Ace Bailey", "Rutgers"),
    ("BYB-4", "VJ Edgecombe", "Baylor"),
    ("BYB-5", "Kon Knueppel", "Duke"),
    ("BYB-6", "Khaman Maluach", "Duke"),
    ("BYB-7", "Tre Johnson", "Texas"),
    ("BYB-8", "Nolan Traore", "France"),
]

make_insert_set("Block by Block", BYB_PARALLELS, byb_cards)
print(f"  Block by Block: {len(byb_cards)} cards")


# ─── 20. Boom Shaka Laka (BO-*) — Value/Hanger/Fanatics exclusive ──────────────

BOOM_PARALLELS = [("Platinum", 1)]

boom_cards = [
    ("BO-1", "Giannis Antetokounmpo", "Milwaukee Bucks"),
    ("BO-2", "LeBron James", "Los Angeles Lakers"),
    ("BO-3", "Anthony Edwards", "Minnesota Timberwolves"),
    ("BO-4", "Victor Wembanyama", "San Antonio Spurs"),
]

make_insert_set("Boombastic", BOOM_PARALLELS, boom_cards)
print(f"  Boombastic: {len(boom_cards)} cards")


# ─── 21. NBA Champions ─────────────────────────────────────────────────────────
# NBA Champions Team and NBA Champions Players and Finals MVP from pack odds

CHAMP_PARALLELS = []

champ_team_cards = [
    ("NCT-1", "Boston Celtics", "Boston Celtics"),
]
make_insert_set("NBA Champions Team", CHAMP_PARALLELS, champ_team_cards)
print(f"  NBA Champions Team: {len(champ_team_cards)} cards")

champ_player_cards = [
    ("NCP-1", "Jayson Tatum", "Boston Celtics"),
    ("NCP-2", "Jaylen Brown", "Boston Celtics"),
    ("NCP-3", "Jrue Holiday", "Boston Celtics"),
    ("NCP-4", "Derrick White", "Boston Celtics"),
    ("NCP-5", "Kristaps Porzingis", "Boston Celtics"),
    ("NCP-6", "Al Horford", "Boston Celtics"),
    ("NCP-7", "Payton Pritchard", "Boston Celtics"),
]
make_insert_set("NBA Champions Players", CHAMP_PARALLELS, champ_player_cards)
print(f"  NBA Champions Players: {len(champ_player_cards)} cards")

fmvp_cards = [
    ("FMVP-1", "Jaylen Brown", "Boston Celtics"),
]
make_insert_set("Finals MVP", CHAMP_PARALLELS, fmvp_cards)
print(f"  Finals MVP: {len(fmvp_cards)} cards")


# ─── 22. Hoops Rookie Signatures (HRS-*) ───────────────────────────────────────

HRS_PARALLELS = [
    ("Pixel Burst Purple", 199),
    ("Pixel Burst Green", 149),
    ("Pixel Burst Gold", 99),
    ("Pixel Burst Orange", 49),
    ("Pixel Burst Black", 25),
    ("Pixel Burst Red", 10),
    ("Pixel Burst Platinum", 1),
]

hrs_cards = [
    ("HRS-1", "Cooper Flagg", "Duke"),
    ("HRS-2", "Dylan Harper", "Rutgers"),
    ("HRS-3", "Ace Bailey", "Rutgers"),
    ("HRS-4", "VJ Edgecombe", "Baylor"),
    ("HRS-5", "Kon Knueppel", "Duke"),
    ("HRS-6", "Tre Johnson", "Texas"),
    ("HRS-7", "Nolan Traore", "France"),
    ("HRS-8", "Khaman Maluach", "Duke"),
    ("HRS-9", "Egor Demin", "BYU"),
    ("HRS-10", "Boogie Fland", "Arkansas"),
    ("HRS-11", "Kasparas Jakucionis", "Illinois"),
    ("HRS-12", "Liam McNeeley", "UConn"),
    ("HRS-13", "Baye Fall", "Arkansas"),
    ("HRS-14", "Hugo Gonzalez", "Spain"),
    ("HRS-15", "Collin Murray-Boyles", "South Carolina"),
    ("HRS-16", "Jeremiah Fears", "Oklahoma"),
    ("HRS-17", "Isiah Harwell", "Alabama"),
    ("HRS-18", "Tyler Betsey", "Arizona"),
    ("HRS-19", "Jase Richardson", "Michigan State"),
    ("HRS-20", "Labaron Philon", "Alabama"),
]

make_insert_set("Hoops Rookie Signatures", HRS_PARALLELS, hrs_cards)
print(f"  Hoops Rookie Signatures: {len(hrs_cards)} cards")


# ─── 23. Hoops Signs (HS-*) ────────────────────────────────────────────────────

HS_PARALLELS = [
    ("Pixel Burst Purple", 199),
    ("Pixel Burst Green", 149),
    ("Pixel Burst Gold", 99),
    ("Pixel Burst Orange", 49),
    ("Pixel Burst Black", 25),
    ("Pixel Burst Red", 10),
    ("Pixel Burst Platinum", 1),
]

hs_cards = [
    ("HS-1", "Stephen Curry", "Golden State Warriors"),
    ("HS-2", "LeBron James", "Los Angeles Lakers"),
    ("HS-3", "Kevin Durant", "Phoenix Suns"),
    ("HS-4", "Giannis Antetokounmpo", "Milwaukee Bucks"),
    ("HS-5", "Nikola Jokic", "Denver Nuggets"),
    ("HS-6", "Luka Doncic", "Dallas Mavericks"),
    ("HS-7", "Anthony Edwards", "Minnesota Timberwolves"),
    ("HS-8", "Jayson Tatum", "Boston Celtics"),
    ("HS-9", "Shai Gilgeous-Alexander", "Oklahoma City Thunder"),
    ("HS-10", "Joel Embiid", "Philadelphia 76ers"),
    ("HS-11", "Devin Booker", "Phoenix Suns"),
    ("HS-12", "Damian Lillard", "Milwaukee Bucks"),
    ("HS-13", "Trae Young", "Atlanta Hawks"),
    ("HS-14", "Donovan Mitchell", "Cleveland Cavaliers"),
    ("HS-15", "Ja Morant", "Memphis Grizzlies"),
    ("HS-16", "Victor Wembanyama", "San Antonio Spurs"),
    ("HS-17", "Jalen Brunson", "New York Knicks"),
    ("HS-18", "Tyrese Haliburton", "Indiana Pacers"),
    ("HS-19", "De'Aaron Fox", "Sacramento Kings"),
    ("HS-20", "Chet Holmgren", "Oklahoma City Thunder"),
    ("HS-21", "Paolo Banchero", "Orlando Magic"),
    ("HS-22", "Zion Williamson", "New Orleans Pelicans"),
    ("HS-23", "LaMelo Ball", "Charlotte Hornets"),
    ("HS-24", "Jimmy Butler", "Miami Heat"),
    ("HS-25", "Paul George", "Philadelphia 76ers"),
]

make_insert_set("Hoops Signs", HS_PARALLELS, hs_cards)
print(f"  Hoops Signs: {len(hs_cards)} cards")


# ─── 24. Hoops Rookie Duals (HRD-*) ────────────────────────────────────────────

HRD_PARALLELS = [
    ("Pixel Burst Black", 25),
    ("Pixel Burst Red", 10),
    ("Pixel Burst Platinum", 1),
]

hrd_cards = [
    ("HRD-1", [("Cooper Flagg", "Duke"), ("Dylan Harper", "Rutgers")]),
    ("HRD-2", [("Ace Bailey", "Rutgers"), ("VJ Edgecombe", "Baylor")]),
    ("HRD-3", [("Kon Knueppel", "Duke"), ("Tre Johnson", "Texas")]),
    ("HRD-4", [("Nolan Traore", "France"), ("Khaman Maluach", "Duke")]),
    ("HRD-5", [("Egor Demin", "BYU"), ("Boogie Fland", "Arkansas")]),
]

hrd_is = create_insert_set(set_id, "Hoops Rookie Duals")
for par_name, par_pr in HRD_PARALLELS:
    create_parallel(hrd_is, par_name, par_pr)
add_multi_cards(hrd_is, hrd_cards)
print(f"  Hoops Rookie Duals: {len(hrd_cards)} cards")


# ─── 25. Hoops Rookie Triples (HRT-*) ──────────────────────────────────────────

HRT_PARALLELS = [
    ("Pixel Burst Black", 25),
    ("Pixel Burst Red", 10),
    ("Pixel Burst Platinum", 1),
]

hrt_cards = [
    ("HRT-1", [("Cooper Flagg", "Duke"), ("Dylan Harper", "Rutgers"), ("Ace Bailey", "Rutgers")]),
    ("HRT-2", [("VJ Edgecombe", "Baylor"), ("Kon Knueppel", "Duke"), ("Tre Johnson", "Texas")]),
]

hrt_is = create_insert_set(set_id, "Hoops Rookie Triples")
for par_name, par_pr in HRT_PARALLELS:
    create_parallel(hrt_is, par_name, par_pr)
add_multi_cards(hrt_is, hrt_cards)
print(f"  Hoops Rookie Triples: {len(hrt_cards)} cards")


# ─── 26. Hoops Rookie/Veteran Duals (RVD-*) ────────────────────────────────────

RVD_PARALLELS = [
    ("Pixel Burst Black", 25),
    ("Pixel Burst Red", 10),
    ("Pixel Burst Platinum", 1),
]

rvd_cards = [
    ("RVD-1", [("Cooper Flagg", "Duke"), ("LeBron James", "Los Angeles Lakers")]),
    ("RVD-2", [("Dylan Harper", "Rutgers"), ("Stephen Curry", "Golden State Warriors")]),
    ("RVD-3", [("Ace Bailey", "Rutgers"), ("Kevin Durant", "Phoenix Suns")]),
]

rvd_is = create_insert_set(set_id, "Hoops Rookie/Veteran Duals")
for par_name, par_pr in RVD_PARALLELS:
    create_parallel(rvd_is, par_name, par_pr)
add_multi_cards(rvd_is, rvd_cards)
print(f"  Hoops Rookie/Veteran Duals: {len(rvd_cards)} cards")


# ─── 27. Hoops 1989 Signatures (89S-*) ─────────────────────────────────────────

SIG89_PARALLELS = [
    ("Green Hoops", None),
    ("Light Burst", None),
    ("Pixel Burst Black", 25),
    ("Pixel Burst Red", 10),
    ("Pixel Burst Platinum", 1),
]

sig89_cards = [
    ("89S-1", "LeBron James", "Los Angeles Lakers"),
    ("89S-2", "Stephen Curry", "Golden State Warriors"),
    ("89S-3", "Kevin Durant", "Phoenix Suns"),
    ("89S-4", "Giannis Antetokounmpo", "Milwaukee Bucks"),
    ("89S-5", "Nikola Jokic", "Denver Nuggets"),
    ("89S-6", "Luka Doncic", "Dallas Mavericks"),
    ("89S-7", "Joel Embiid", "Philadelphia 76ers"),
    ("89S-8", "Jayson Tatum", "Boston Celtics"),
    ("89S-9", "Anthony Edwards", "Minnesota Timberwolves"),
    ("89S-10", "Devin Booker", "Phoenix Suns"),
]

make_insert_set("Hoops 1989 Signatures", SIG89_PARALLELS, sig89_cards)
print(f"  Hoops 1989 Signatures: {len(sig89_cards)} cards")


# ─── 28. Hoops Rookie First Signs (HFS-*) — Value/Hanger/Fanatics ──────────────

HFS_PARALLELS = [
    ("Light Burst Purple", 199),
    ("Light Burst Green", 149),
    ("Light Burst Gold", 99),
    ("Light Burst Orange", 49),
    ("Light Burst Black", 25),
    ("Light Burst Red", 10),
    ("Light Burst Platinum", 1),
]

hfs_cards = [
    ("HFS-1", "Cooper Flagg", "Duke"),
    ("HFS-2", "Dylan Harper", "Rutgers"),
    ("HFS-3", "Ace Bailey", "Rutgers"),
    ("HFS-4", "VJ Edgecombe", "Baylor"),
    ("HFS-5", "Kon Knueppel", "Duke"),
    ("HFS-6", "Tre Johnson", "Texas"),
    ("HFS-7", "Nolan Traore", "France"),
    ("HFS-8", "Khaman Maluach", "Duke"),
    ("HFS-9", "Egor Demin", "BYU"),
    ("HFS-10", "Boogie Fland", "Arkansas"),
    ("HFS-11", "Kasparas Jakucionis", "Illinois"),
    ("HFS-12", "Liam McNeeley", "UConn"),
    ("HFS-13", "Baye Fall", "Arkansas"),
    ("HFS-14", "Collin Murray-Boyles", "South Carolina"),
    ("HFS-15", "Jeremiah Fears", "Oklahoma"),
]

make_insert_set("Hoops Rookie First Signs", HFS_PARALLELS, hfs_cards)
print(f"  Hoops Rookie First Signs: {len(hfs_cards)} cards")


# ─── 29. Hoops Hyper Signatures (HHS-*) — Value/Hanger/Fanatics ────────────────

HHS_PARALLELS = [
    ("Light Burst Purple", 199),
    ("Light Burst Green", 149),
    ("Light Burst Gold", 99),
    ("Light Burst Orange", 49),
    ("Light Burst Black", 25),
    ("Light Burst Red", 10),
    ("Light Burst Platinum", 1),
]

hhs_cards = [
    ("HHS-1", "Stephen Curry", "Golden State Warriors"),
    ("HHS-2", "LeBron James", "Los Angeles Lakers"),
    ("HHS-3", "Kevin Durant", "Phoenix Suns"),
    ("HHS-4", "Giannis Antetokounmpo", "Milwaukee Bucks"),
    ("HHS-5", "Nikola Jokic", "Denver Nuggets"),
    ("HHS-6", "Luka Doncic", "Dallas Mavericks"),
    ("HHS-7", "Anthony Edwards", "Minnesota Timberwolves"),
    ("HHS-8", "Jayson Tatum", "Boston Celtics"),
    ("HHS-9", "Shai Gilgeous-Alexander", "Oklahoma City Thunder"),
    ("HHS-10", "Victor Wembanyama", "San Antonio Spurs"),
    ("HHS-11", "Ja Morant", "Memphis Grizzlies"),
    ("HHS-12", "Devin Booker", "Phoenix Suns"),
]

make_insert_set("Hoops Hyper Signatures", HHS_PARALLELS, hhs_cards)
print(f"  Hoops Hyper Signatures: {len(hhs_cards)} cards")


# ─── 30. Generate slug ─────────────────────────────────────────────────────────

import re

def slugify(text):
    slug = text.lower().strip()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    return slug.strip('-')

set_slug = slugify(SET_NAME)
cur.execute("UPDATE sets SET slug = ? WHERE id = ?", (set_slug, set_id))

# Generate slugs for all players in this set
cur.execute("SELECT id, name FROM players WHERE set_id = ?", (set_id,))
all_players = cur.fetchall()
used_slugs = set()
for pid, pname in all_players:
    slug = slugify(pname)
    if slug in used_slugs:
        i = 2
        while f"{slug}-{i}" in used_slugs:
            i += 1
        slug = f"{slug}-{i}"
    used_slugs.add(slug)
    cur.execute("UPDATE players SET slug = ? WHERE id = ?", (slug, pid))


# ─── 31. Commit ────────────────────────────────────────────────────────────────

conn.commit()

# Stats
cur.execute("SELECT COUNT(*) FROM players WHERE set_id = ?", (set_id,))
player_count = cur.fetchone()[0]
cur.execute(
    "SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON pa.insert_set_id = i.id WHERE i.set_id = ?",
    (set_id,),
)
appearance_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id = ?", (set_id,))
is_count = cur.fetchone()[0]
cur.execute(
    "SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON p.insert_set_id = i.id WHERE i.set_id = ?",
    (set_id,),
)
par_count = cur.fetchone()[0]

print(f"\nDone! Set ID: {set_id}")
print(f"  Players: {player_count}")
print(f"  Appearances: {appearance_count}")
print(f"  Insert sets: {is_count}")
print(f"  Parallels: {par_count}")

conn.close()
