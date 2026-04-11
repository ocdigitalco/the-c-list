"""
Seed checklist for 2025 Topps Chrome Formula 1 (set id 51).
Appends insert sets, parallels, players, and appearances to the existing set.
Also updates Helix pack odds from 1:700 to 1:900.
Usage: python3 scripts/seed_chrome_f1_2025_checklist.py
"""

import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA foreign_keys=ON")
cur = conn.cursor()

SET_ID = 51
cur.execute("SELECT name FROM sets WHERE id = ?", (SET_ID,))
row = cur.fetchone()
if not row:
    print(f"Set {SET_ID} not found. Aborting.")
    conn.close()
    exit(1)
print(f"Appending checklist to: {row[0]} (id {SET_ID})")

# ─── Helpers ────────────────────────────────────────────────────────────────────

def get_or_create_player(name):
    cur.execute("SELECT id FROM players WHERE set_id = ? AND name = ?", (SET_ID, name))
    r = cur.fetchone()
    if r: return r[0]
    cur.execute("INSERT INTO players (set_id, name, unique_cards, total_print_run, one_of_ones, insert_set_count) VALUES (?, ?, 0, 0, 0, 0)", (SET_ID, name))
    return cur.lastrowid

def create_insert_set(name):
    cur.execute("INSERT INTO insert_sets (set_id, name) VALUES (?, ?)", (SET_ID, name))
    return cur.lastrowid

def create_parallel(is_id, name, pr):
    cur.execute("INSERT INTO parallels (insert_set_id, name, print_run) VALUES (?, ?, ?)", (is_id, name, pr))

def create_appearance(pid, is_id, cn, rookie=False, team=None):
    cur.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)", (pid, is_id, cn, int(rookie), team))
    return cur.lastrowid

def create_co_player(app_id, co_pid):
    cur.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (app_id, co_pid))

ROOKIES = {"Kimi Antonelli", "Liam Lawson", "Isack Hadjar", "Oliver Bearman", "Franco Colapinto", "Gabriel Bortoleto"}

def add_cards(is_id, cards):
    for item in cards:
        cn, name = item[0], item[1]
        team = item[2] if len(item) > 2 else None
        pid = get_or_create_player(name)
        create_appearance(pid, is_id, cn, name in ROOKIES, team)

def add_duo_cards(is_id, cards):
    for cn, pairs in cards:
        app_ids, pids = [], []
        for name, team in pairs:
            pid = get_or_create_player(name)
            aid = create_appearance(pid, is_id, cn, name in ROOKIES, team)
            app_ids.append(aid); pids.append(pid)
        for i, aid in enumerate(app_ids):
            for j, cpid in enumerate(pids):
                if i != j: create_co_player(aid, cpid)

def make_is(name, pars, cards, duo=False):
    is_id = create_insert_set(name)
    for pn, pr in pars: create_parallel(is_id, pn, pr)
    if duo: add_duo_cards(is_id, cards)
    else: add_cards(is_id, cards)
    return is_id

# ─── Parallel definitions ─────────────────────────────────────────────────────

BASE_PARS = [
    ("Refractor", None), ("Checker Flag", None), ("B&W Lazer Refractor", None),
    ("Teal Refractor", None), ("Pink Refractor", 250), ("Pink Checker Flag", None),
    ("Aqua Refractor", 199), ("Aqua Checker Flag", None),
    ("Blue Refractor", 150), ("Blue Checker Flag", None),
    ("Green Refractor", 99), ("Green Checker Flag", None),
    ("F1 75th Anniversary Refractor", 75), ("Gold Refractor", 50), ("Gold Checker Flag", None),
    ("Orange Refractor", 25), ("Orange Checker Flag", None),
    ("Black Refractor", 10), ("Black Checker Flag", 10),
    ("Red Refractor", 5), ("Red Checker Flag", 5),
    ("Superfractor", 1),
    ("Printing Plates Cyan", 1), ("Printing Plates Magenta", 1),
    ("Printing Plates Yellow", 1), ("Printing Plates Black", 1),
]

INSERT_PARS = [
    ("Aqua Refractor", 199), ("Blue Refractor", 150), ("Green Refractor", 99),
    ("F1 75th Anniversary Refractor", 75), ("Gold Refractor", 50),
    ("Orange Refractor", 25), ("Black Refractor", 10),
    ("Red Refractor", 5), ("Superfractor", 1),
]

SD_PARS = [
    ("Aqua Refractor", 199), ("Blue Refractor", 150), ("Green Refractor", 99),
    ("F1 75th Anniversary Refractor", 75), ("Gold Refractor", 50),
    ("Orange Refractor", 25), ("Black Refractor", 10),
    ("Red Refractor", 5), ("Superfractor", 1),
]

TOP_SPEED_PARS = [
    ("Blue Refractor", 150), ("Green Refractor", 99), ("Gold Refractor", 50),
    ("Orange Refractor", 25), ("Black Refractor", 10),
    ("Red Refractor", 5), ("Superfractor", 1),
]

CHROME_AUTO_PARS = [
    ("Green Refractor", 99), ("F1 75th Anniversary Refractor", 75),
    ("Gold Refractor", 50), ("Orange Refractor", 25),
    ("Black Refractor", 10), ("Red Refractor", 5), ("Superfractor", 1),
]

SPEED_WHEEL_SIG_PARS = [
    ("Orange Refractor", 25), ("Red Refractor", 5), ("Superfractor", 1),
]

CMS_PARS = [
    ("F1 75th Anniversary Refractor", 75), ("Gold Refractor", 50),
    ("Orange Refractor", 25), ("Red Refractor", 5), ("Superfractor", 1),
]

FUTURO_AUTO_PARS = [
    ("Orange Refractor", 25), ("Red Refractor", 5), ("Superfractor", 1),
]

ONCARD_PARS = [("Red Refractor", 5), ("Superfractor", 1)]

SUPERFRACTOR_ONLY = [("Superfractor", 1)]

F175_LOGO_PARS = [("Black Refractor", 10), ("Red Refractor", 5), ("Superfractor", 1)]

# ─── Base sets ─────────────────────────────────────────────────────────────────

make_is("Base - F1 Drivers", BASE_PARS, [
    ("1", "Max Verstappen", "Oracle Red Bull Racing"),
    ("2", "Yuki Tsunoda", "Oracle Red Bull Racing"),
    ("3", "Charles Leclerc", "Scuderia Ferrari HP"),
    ("4", "Lewis Hamilton", "Scuderia Ferrari HP"),
    ("5", "Lando Norris", "McLaren Formula 1 Team"),
    ("6", "Oscar Piastri", "McLaren Formula 1 Team"),
    ("7", "George Russell", "Mercedes-AMG PETRONAS Formula One Team"),
    ("8", "Kimi Antonelli", "Mercedes-AMG PETRONAS Formula One Team"),
    ("9", "Fernando Alonso", "Aston Martin Aramco Formula One Team"),
    ("10", "Lance Stroll", "Aston Martin Aramco Formula One Team"),
    ("11", "Liam Lawson", "Visa Cash App RB Formula One Team"),
    ("12", "Isack Hadjar", "Visa Cash App RB Formula One Team"),
    ("13", "Esteban Ocon", "MoneyGram Haas F1 Team"),
    ("14", "Oliver Bearman", "MoneyGram Haas F1 Team"),
    ("15", "Franco Colapinto", "BWT Alpine Formula One Team"),
    ("16", "Pierre Gasly", "BWT Alpine Formula One Team"),
    ("17", "Alex Albon", "Atlassian Williams Racing"),
    ("18", "Carlos Sainz", "Atlassian Williams Racing"),
    ("19", "Nico Hulkenberg", "Stake F1 Team KICK Sauber"),
    ("20", "Gabriel Bortoleto", "Stake F1 Team KICK Sauber"),
])
print("  Base - F1 Drivers: 20 cards")

make_is("Base - F2 Drivers", BASE_PARS, [
    ("21", "Leonardo Fornaroli", "F2"), ("22", "Roman Stan\u011bk", "F2"),
    ("23", "Arvid Lindblad", "F2"), ("24", "Josep Mar\u00eda Mart\u00ed", "F2"),
    ("25", "Richard Verschoor", "F2"), ("26", "Oliver Goethe", "F2"),
    ("27", "Dino Beganovic", "F2"), ("28", "Luke Browning", "F2"),
    ("29", "Gabriele Min\u00ec", "F2"), ("30", "Sebasti\u00e1n Montoya", "F2"),
    ("31", "Jak Crawford", "F2"), ("32", "Kush Maini", "F2"),
    ("33", "Ritomo Miyata", "F2"), ("34", "Victor Martins", "F2"),
    ("35", "Alexander Dunne", "F2"), ("36", "Amaury Cordeel", "F2"),
    ("37", "Joshua D\u00fcrksen", "F2"), ("38", "Cian Shields", "F2"),
    ("39", "Max Esterson", "F2"), ("40", "Sami Meguetounif", "F2"),
    ("41", "John Bennett", "F2"), ("42", "Rafael Villag\u00f3mez", "F2"),
])
print("  Base - F2 Drivers: 22 cards")

make_is("Base - F3 Drivers", BASE_PARS, [
    ("43", "Noel Le\u00f3n", "F3"), ("44", "Brando Badoer", "F3"),
    ("45", "Ugo Ugochukwu", "F3"), ("46", "Noah Str\u00f8msted", "F3"),
    ("47", "Rafael C\u00e2mara", "F3"), ("48", "Charlie Wurz", "F3"),
    ("49", "Tim Tramnitz", "F3"), ("50", "Bruno del Pino", "F3"),
    ("51", "Alessandro Giusti", "F3"), ("52", "Nikola Tsolov", "F3"),
    ("53", "Tasanapol Inthraphuvasak", "F3"), ("54", "Mari Boya", "F3"),
    ("55", "Joshua Dufek", "F3"), ("56", "Gerrard Xie", "F3"),
    ("57", "Martinius Stenshorne", "F3"), ("58", "Th\u00e9ophile Na\u00ebl", "F3"),
    ("59", "Santiago Ramos", "F3"), ("60", "Ivan Domingues", "F3"),
    ("61", "James Wharton", "F3"), ("62", "Tuukka Taponen", "F3"),
    ("63", "Laurens van Hoepen", "F3"), ("64", "Javier Sagrera", "F3"),
    ("65", "Nicola Marinangeli", "F3"), ("66", "Nikita Bedrin", "F3"),
    ("67", "Callum Voisin", "F3"), ("68", "Louis Sharp", "F3"),
    ("69", "Roman Bilinski", "F3"), ("70", "Mat\u00edas Zagazeta", "F3"),
    ("71", "Nicola Lacorte", "F3"), ("72", "Christian Ho", "F3"),
])
print("  Base - F3 Drivers: 30 cards")

make_is("Base - F1 Cars", BASE_PARS, [
    ("73", "Max Verstappen", "Oracle Red Bull Racing"),
    ("74", "Yuki Tsunoda", "Oracle Red Bull Racing"),
    ("75", "Charles Leclerc", "Scuderia Ferrari HP"),
    ("76", "Lewis Hamilton", "Scuderia Ferrari HP"),
    ("77", "Lando Norris", "McLaren Formula 1 Team"),
    ("78", "Oscar Piastri", "McLaren Formula 1 Team"),
    ("79", "George Russell", "Mercedes-AMG PETRONAS Formula One Team"),
    ("80", "Kimi Antonelli", "Mercedes-AMG PETRONAS Formula One Team"),
    ("81", "Fernando Alonso", "Aston Martin Aramco Formula One Team"),
    ("82", "Lance Stroll", "Aston Martin Aramco Formula One Team"),
    ("83", "Liam Lawson", "Visa Cash App RB Formula One Team"),
    ("84", "Isack Hadjar", "Visa Cash App RB Formula One Team"),
    ("85", "Esteban Ocon", "MoneyGram Haas F1 Team"),
    ("86", "Oliver Bearman", "MoneyGram Haas F1 Team"),
    ("87", "Franco Colapinto", "BWT Alpine Formula One Team"),
    ("88", "Pierre Gasly", "BWT Alpine Formula One Team"),
    ("89", "Alex Albon", "Atlassian Williams Racing"),
    ("90", "Carlos Sainz", "Atlassian Williams Racing"),
    ("91", "Nico Hulkenberg", "Stake F1 Team KICK Sauber"),
    ("92", "Gabriel Bortoleto", "Stake F1 Team KICK Sauber"),
])
print("  Base - F1 Cars: 20 cards")

make_is("Base - Grand Prix Winners", BASE_PARS, [
    (str(i), name) for i, name in enumerate([
        "Max Verstappen", "Max Verstappen", "Carlos Sainz", "Max Verstappen",
        "Max Verstappen", "Lando Norris", "Max Verstappen", "Charles Leclerc",
        "Max Verstappen", "Max Verstappen", "George Russell", "Lewis Hamilton",
        "Oscar Piastri", "Lewis Hamilton", "Lando Norris", "Charles Leclerc",
        "Oscar Piastri", "Lando Norris", "Charles Leclerc", "Carlos Sainz",
        "Max Verstappen", "George Russell", "Max Verstappen", "Lando Norris",
    ], 93)
])
print("  Base - Grand Prix Winners: 24 cards")

make_is("Base - Pole Position", BASE_PARS, [
    ("117", "Max Verstappen"), ("118", "Charles Leclerc"), ("119", "George Russell"),
    ("120", "Lando Norris"), ("121", "Carlos Sainz"),
])
print("  Base - Pole Position: 5 cards")

make_is("Base - Grand Prix Driver Of The Day", BASE_PARS, [
    (str(i), name) for i, name in enumerate([
        "Carlos Sainz", "Oliver Bearman", "Carlos Sainz", "Charles Leclerc",
        "Lando Norris", "Lando Norris", "Lando Norris", "Charles Leclerc",
        "Lando Norris", "Lando Norris", "Lando Norris", "Lewis Hamilton",
        "Oscar Piastri", "Lewis Hamilton", "Lando Norris", "Charles Leclerc",
        "Oscar Piastri", "Daniel Ricciardo", "Charles Leclerc", "Carlos Sainz",
        "Max Verstappen", "Lewis Hamilton", "Zhou Guanyu", "Charles Leclerc",
    ], 122)
])
print("  Base - Grand Prix Driver Of The Day: 24 cards")

make_is("Base - F1 Award Winners", BASE_PARS, [
    ("146", "Oracle Red Bull Racing"), ("147", "Lando Norris"), ("148", "Max Verstappen"),
])
print("  Base - F1 Award Winners: 3 cards")

make_is("Base - F1 Legends", BASE_PARS, [
    ("149", "Alain Prost"), ("150", "Damon Hill"), ("151", "David Coulthard"),
    ("152", "Emerson Fittipaldi"), ("153", "Gerhard Berger"), ("154", "Jackie Stewart"),
    ("155", "James Hunt"), ("156", "Juan Pablo Montoya"), ("157", "Kimi R\u00e4ikk\u00f6nen"),
    ("158", "Michael Schumacher"), ("159", "Mika H\u00e4kkinen"), ("160", "Nigel Mansell"),
    ("161", "Mario Andretti"), ("162", "Ayrton Senna"), ("163", "Jacques Villeneuve"),
])
print("  Base - F1 Legends: 15 cards")

# Duo cards
duo_data = [
    ("164", [("Max Verstappen", "Oracle Red Bull Racing"), ("Yuki Tsunoda", "Oracle Red Bull Racing")]),
    ("165", [("Charles Leclerc", "Scuderia Ferrari HP"), ("Lewis Hamilton", "Scuderia Ferrari HP")]),
    ("166", [("Lando Norris", "McLaren Formula 1 Team"), ("Oscar Piastri", "McLaren Formula 1 Team")]),
    ("167", [("George Russell", "Mercedes-AMG PETRONAS Formula One Team"), ("Kimi Antonelli", "Mercedes-AMG PETRONAS Formula One Team")]),
    ("168", [("Fernando Alonso", "Aston Martin Aramco Formula One Team"), ("Lance Stroll", "Aston Martin Aramco Formula One Team")]),
    ("169", [("Liam Lawson", "Visa Cash App RB Formula One Team"), ("Isack Hadjar", "Visa Cash App RB Formula One Team")]),
    ("170", [("Esteban Ocon", "MoneyGram Haas F1 Team"), ("Oliver Bearman", "MoneyGram Haas F1 Team")]),
    ("171", [("Pierre Gasly", "BWT Alpine Formula One Team"), ("Franco Colapinto", "BWT Alpine Formula One Team")]),
    ("172", [("Alex Albon", "Atlassian Williams Racing"), ("Carlos Sainz", "Atlassian Williams Racing")]),
    ("173", [("Nico Hulkenberg", "Stake F1 Team KICK Sauber"), ("Gabriel Bortoleto", "Stake F1 Team KICK Sauber")]),
]
make_is("Base - F1 Duo Cards", BASE_PARS, duo_data, duo=True)
print("  Base - F1 Duo Cards: 10 cards")

make_is("Base - F1 Team Logo Cards", BASE_PARS, [
    ("174", "Oracle Red Bull Racing"), ("175", "Scuderia Ferrari HP"),
    ("176", "McLaren Formula 1 Team"), ("177", "Mercedes-AMG PETRONAS Formula One Team"),
    ("178", "Aston Martin Aramco Formula One Team"), ("179", "Visa Cash App RB Formula One Team"),
    ("180", "MoneyGram Haas F1 Team"), ("181", "BWT Alpine Formula One Team"),
    ("182", "Atlassian Williams Racing"), ("183", "Stake F1 Team KICK Sauber"),
])
print("  Base - F1 Team Logo Cards: 10 cards")

make_is("Base - F1 On The Move", BASE_PARS, [
    ("184", "Yuki Tsunoda", "Oracle Red Bull Racing"),
    ("185", "Kimi Antonelli", "Mercedes-AMG PETRONAS Formula One Team"),
    ("186", "Oliver Bearman", "MoneyGram Haas F1 Team"),
    ("187", "Franco Colapinto", "BWT Alpine Formula One Team"),
    ("188", "Nico Hulkenberg", "Stake F1 Team KICK Sauber"),
    ("189", "Carlos Sainz", "Atlassian Williams Racing"),
    ("190", "Esteban Ocon", "MoneyGram Haas F1 Team"),
    ("191", "Lewis Hamilton", "Scuderia Ferrari HP"),
])
print("  Base - F1 On The Move: 8 cards")

make_is("Base - F1 Team Principals", BASE_PARS, [
    ("192", "Christian Horner", "Oracle Red Bull Racing"),
    ("193", "Fr\u00e9d\u00e9ric Vasseur", "Scuderia Ferrari HP"),
    ("194", "Andrea Stella", "McLaren Formula 1 Team"),
    ("195", "Toto Wolff", "Mercedes-AMG PETRONAS Formula One Team"),
    ("196", "Andy Cowell", "Aston Martin Aramco Formula One Team"),
    ("197", "Laurent Mekies", "Visa Cash App RB Formula One Team"),
    ("198", "Ayao Komatsu", "MoneyGram Haas F1 Team"),
    ("199", "Flavio Briatore", "BWT Alpine Formula One Team"),
    ("200", "James Vowles", "Atlassian Williams Racing"),
])
print("  Base - F1 Team Principals: 9 cards")

# Driver Image Variations — no parallels (SP)
make_is("Driver Image Variations", [], [
    ("2", "Yuki Tsunoda"), ("4", "Lewis Hamilton"), ("5", "Lando Norris"),
    ("8", "Kimi Antonelli"), ("9", "Fernando Alonso"), ("12", "Isack Hadjar"),
    ("14", "Oliver Bearman"), ("15", "Franco Colapinto"), ("18", "Carlos Sainz"),
    ("20", "Gabriel Bortoleto"),
])
print("  Driver Image Variations: 10 cards")

# ─── Autograph sets ────────────────────────────────────────────────────────────

make_is("Chrome Autographs", CHROME_AUTO_PARS, [
    ("CAC-VER", "Max Verstappen"), ("CAC-TSU", "Yuki Tsunoda"),
    ("CAC-HAM", "Lewis Hamilton"), ("CAC-NOR", "Lando Norris"),
    ("CAC-PIA", "Oscar Piastri"), ("CAC-RUS", "George Russell"),
    ("CAC-ANT", "Kimi Antonelli"), ("CAC-ALO", "Fernando Alonso"),
    ("CAC-STR", "Lance Stroll"), ("CAC-LAW", "Liam Lawson"),
    ("CAC-HAD", "Isack Hadjar"), ("CAC-OCO", "Esteban Ocon"),
    ("CAC-BEA", "Oliver Bearman"), ("CAC-COL", "Franco Colapinto"),
    ("CAC-GAS", "Pierre Gasly"), ("CAC-ALB", "Alex Albon"),
    ("CAC-SAI", "Carlos Sainz"), ("CAC-HUL", "Nico Hulkenberg"),
    ("CAC-BOR", "Gabriel Bortoleto"), ("CAC-FOR", "Leonardo Fornaroli"),
    ("CAC-STA", "Roman Stan\u011bk"), ("CAC-LIN", "Arvid Lindblad"),
    ("CAC-MAR", "Josep Mar\u00eda Mart\u00ed"), ("CAC-VERS", "Richard Verschoor"),
    ("CAC-GOE", "Oliver Goethe"), ("CAC-BEG", "Dino Beganovic"),
    ("CAC-BRO", "Luke Browning"), ("CAC-MIN", "Gabriele Min\u00ec"),
    ("CAC-MON", "Sebasti\u00e1n Montoya"), ("CAC-CRA", "Jak Crawford"),
    ("CAC-MAI", "Kush Maini"), ("CAC-MIY", "Ritomo Miyata"),
    ("CAC-MART", "Victor Martins"), ("CAC-DUN", "Alexander Dunne"),
    ("CAC-COR", "Amaury Cordeel"), ("CAC-DUR", "Joshua D\u00fcrksen"),
    ("CAC-SHI", "Cian Shields"), ("CAC-EST", "Max Esterson"),
    ("CAC-MEG", "Sami Meguetounif"), ("CAC-BEN", "John Bennett"),
    ("CAC-VIL", "Rafael Villag\u00f3mez"), ("CAC-BAD", "Brando Badoer"),
    ("CAC-UGO", "Ugo Ugochukwu"), ("CAC-STRO", "Noah Str\u00f8msted"),
    ("CAC-CAM", "Rafael C\u00e2mara"), ("CAC-DEL", "Bruno del Pino"),
    ("CAC-GIU", "Alessandro Giusti"), ("CAC-XIE", "Gerrard Xie"),
    ("CAC-NAE", "Th\u00e9ophile Na\u00ebl"), ("CAC-DOM", "Ivan Domingues"),
    ("CAC-WHA", "James Wharton"), ("CAC-TAP", "Tuukka Taponen"),
    ("CAC-SAG", "Javier Sagrera"), ("CAC-MARI", "Nicola Marinangeli"),
    ("CAC-SHA", "Louis Sharp"), ("CAC-BIL", "Roman Bilinski"),
    ("CAC-LAC", "Nicola Lacorte"), ("CAC-HOR", "Christian Horner"),
    ("CAC-VAS", "Fr\u00e9d\u00e9ric Vasseur"), ("CAC-STE", "Andrea Stella"),
    ("CAC-WOL", "Toto Wolff"), ("CAC-COW", "Andy Cowell"),
    ("CAC-MEK", "Laurent Mekies"), ("CAC-KOM", "Ayao Komatsu"),
    ("CAC-VOW", "James Vowles"), ("CAC-WHE", "Jonathan Wheatley"),
])
print("  Chrome Autographs: 66 cards")

make_is("1975 Speed Wheel Signatures", SPEED_WHEEL_SIG_PARS, [
    ("75A-1", "Max Verstappen"), ("75A-3", "Oscar Piastri"),
    ("75A-4", "George Russell"), ("75A-5", "Lance Stroll"),
    ("75A-6", "Liam Lawson"), ("75A-7", "Esteban Ocon"),
    ("75A-8", "Pierre Gasly"),
])
print("  1975 Speed Wheel Signatures: 7 cards")

make_is("Futuro Chrome Autographs", FUTURO_AUTO_PARS, [
    ("FUT-LAW", "Liam Lawson"), ("FUT-ANT", "Kimi Antonelli"),
    ("FUT-HAD", "Isack Hadjar"), ("FUT-BEA", "Oliver Bearman"),
    ("FUT-COL", "Franco Colapinto"), ("FUT-BOR", "Gabriel Bortoleto"),
    ("FUT-CRA", "Jak Crawford"), ("FUT-VER", "Richard Verschoor"),
    ("FUT-FOR", "Leonardo Fornaroli"), ("FUT-DUR", "Joshua D\u00fcrksen"),
])
print("  Futuro Chrome Autographs: 10 cards")

make_is("Circuit Masters Signatures", CMS_PARS, [
    ("CMS-HIL", "Damon Hill"), ("CMS-FIT", "Emerson Fittipaldi"),
    ("CMS-BER", "Gerhard Berger"), ("CMS-STE", "Jackie Stewart"),
    ("CMS-MON", "Juan Pablo Montoya"), ("CMS-RAI", "Kimi R\u00e4ikk\u00f6nen"),
    ("CMS-MAN", "Nigel Mansell"), ("CMS-MH", "Mika H\u00e4kkinen"),
    ("CMS-MA", "Mario Andretti"), ("CMS-PRO", "Alain Prost"),
])
print("  Circuit Masters Signatures: 10 cards")

make_is("Diamond 75th Anniversary Autographs", CHROME_AUTO_PARS, [
    ("D75A-VER", "Max Verstappen"), ("D75A-TSU", "Yuki Tsunoda"),
    ("D75A-PIA", "Oscar Piastri"), ("D75A-RUS", "George Russell"),
    ("D75A-KIM", "Kimi Antonelli"), ("D75A-ALO", "Fernando Alonso"),
    ("D75A-STR", "Lance Stroll"), ("D75A-LAW", "Liam Lawson"),
    ("D75A-HAD", "Isack Hadjar"), ("D75A-OCO", "Esteban Ocon"),
    ("D75A-BEA", "Oliver Bearman"), ("D75A-COL", "Franco Colapinto"),
    ("D75A-GAS", "Pierre Gasly"), ("D75A-ALB", "Alex Albon"),
    ("D75A-SAI", "Carlos Sainz"), ("D75A-HUL", "Nico Hulkenberg"),
    ("D75A-BOR", "Gabriel Bortoleto"), ("D75A-STE", "Jackie Stewart"),
    ("D75A-COU", "David Coulthard"), ("D75A-RAI", "Kimi R\u00e4ikk\u00f6nen"),
    ("D75A-BER", "Gerhard Berger"), ("D75A-HAK", "Mika H\u00e4kkinen"),
    ("D75A-HAM", "Lewis Hamilton"),
])
print("  Diamond 75th Anniversary Autographs: 23 cards")

make_is("On-Card Chrome Autographs", ONCARD_PARS, [("OC-HAM", "Lewis Hamilton")])
print("  On-Card Chrome Autographs: 1 card")

make_is("F1 Debut Patch Autographs", [], [
    ("20", "Gabriel Bortoleto"), ("12", "Isack Hadjar"),
])
print("  F1 Debut Patch Autographs: 2 cards")

# ─── Relic sets ────────────────────────────────────────────────────────────────

f1_drivers_20 = [
    ("DR-1", "Max Verstappen"), ("DR-2", "Yuki Tsunoda"), ("DR-3", "Charles Leclerc"),
    ("DR-4", "Lewis Hamilton"), ("DR-5", "Lando Norris"), ("DR-6", "Oscar Piastri"),
    ("DR-7", "George Russell"), ("DR-8", "Kimi Antonelli"), ("DR-9", "Fernando Alonso"),
    ("DR-10", "Lance Stroll"), ("DR-11", "Liam Lawson"), ("DR-12", "Isack Hadjar"),
    ("DR-13", "Esteban Ocon"), ("DR-14", "Oliver Bearman"), ("DR-15", "Franco Colapinto"),
    ("DR-16", "Pierre Gasly"), ("DR-17", "Alex Albon"), ("DR-18", "Carlos Sainz"),
    ("DR-19", "Nico Hulkenberg"), ("DR-20", "Gabriel Bortoleto"),
]
make_is("F1 Diamond Anniversary Relic Cards", [], f1_drivers_20)
print("  F1 Diamond Anniversary Relic Cards: 20 cards")

f2_drivers_22 = [(f"DR-{i}", name) for i, name in enumerate([
    "Leonardo Fornaroli", "Roman Stan\u011bk", "Arvid Lindblad",
    "Josep Mar\u00eda Mart\u00ed", "Richard Verschoor", "Oliver Goethe",
    "Dino Beganovic", "Luke Browning", "Gabriele Min\u00ec",
    "Sebasti\u00e1n Montoya", "Jak Crawford", "Kush Maini",
    "Ritomo Miyata", "Victor Martins", "Alexander Dunne",
    "Amaury Cordeel", "Joshua D\u00fcrksen", "Cian Shields",
    "Max Esterson", "Sami Meguetounif", "John Bennett", "Rafael Villag\u00f3mez",
], 21)]
make_is("F2 Diamond Anniversary Relic Cards", [], f2_drivers_22)
print("  F2 Diamond Anniversary Relic Cards: 22 cards")

f3_drivers_30 = [(f"DR-{i}", name) for i, name in enumerate([
    "Noel Le\u00f3n", "Brando Badoer", "Ugo Ugochukwu", "Noah Str\u00f8msted",
    "Rafael C\u00e2mara", "Charlie Wurz", "Tim Tramnitz", "Bruno del Pino",
    "Alessandro Giusti", "Nikola Tsolov", "Tasanapol Inthraphuvasak", "Mari Boya",
    "Joshua Dufek", "Gerrard Xie", "Martinius Stenshorne", "Th\u00e9ophile Na\u00ebl",
    "Ivan Domingues", "Santiago Ramos", "James Wharton", "Tuukka Taponen",
    "Laurens van Hoepen", "Javier Sagrera", "Nicola Marinangeli", "Nikita Bedrin",
    "Callum Voisin", "Louis Sharp", "Roman Bilinski", "Mat\u00edas Zagazeta",
    "Nicola Lacorte", "Christian Ho",
], 43)]
make_is("F3 Diamond Anniversary Relic Cards", [], f3_drivers_30)
print("  F3 Diamond Anniversary Relic Cards: 30 cards")

# ─── Insert sets ───────────────────────────────────────────────────────────────

make_is("1975 Speed Wheels", INSERT_PARS, [
    ("75-RBR", "Yuki Tsunoda", "Oracle Red Bull Racing"),
    ("75-SF", "Charles Leclerc", "Scuderia Ferrari HP"),
    ("75-MCL", "Lando Norris", "McLaren Formula 1 Team"),
    ("75-MAMG", "George Russell", "Mercedes-AMG PETRONAS Formula One Team"),
    ("75-AM", "Lance Stroll", "Aston Martin Aramco Formula One Team"),
    ("75-VCARB", "Isack Hadjar", "Visa Cash App RB Formula One Team"),
    ("75-HF1", "Esteban Ocon", "MoneyGram Haas F1 Team"),
    ("75-ALP", "Pierre Gasly", "BWT Alpine Formula One Team"),
    ("75-WR", "Carlos Sainz", "Atlassian Williams Racing"),
    ("75-KICK", "Gabriel Bortoleto", "Stake F1 Team KICK Sauber"),
])
print("  1975 Speed Wheels: 10 cards")

make_is("Ace Of Trades", INSERT_PARS, [
    ("SCA-1", "George Russell"), ("SCA-2", "Charles Leclerc"),
    ("SCA-3", "Max Verstappen"), ("SCA-4", "Lando Norris"),
    ("SCA-5", "Liam Lawson"), ("SCA-6", "Fernando Alonso"),
    ("SCA-7", "Carlos Sainz"), ("SCA-8", "Esteban Ocon"),
    ("SCA-9", "Pierre Gasly"), ("SCA-10", "Nico Hulkenberg"),
])
print("  Ace Of Trades: 10 cards")

make_is("Speed Demons", SD_PARS, [
    ("SD-1", "Kimi Antonelli"), ("SD-2", "Lewis Hamilton"),
    ("SD-3", "Yuki Tsunoda"), ("SD-4", "Oscar Piastri"),
    ("SD-5", "Isack Hadjar"), ("SD-6", "Lance Stroll"),
    ("SD-7", "Alex Albon"), ("SD-8", "Oliver Bearman"),
    ("SD-9", "Franco Colapinto"), ("SD-10", "Gabriel Bortoleto"),
    ("SD-11", "Kimi R\u00e4ikk\u00f6nen"),
])
print("  Speed Demons: 11 cards")

make_is("Helmet Collection", INSERT_PARS, [
    ("HC-1", "Kimi Antonelli"), ("HC-2", "Lewis Hamilton"),
    ("HC-3", "Yuki Tsunoda"), ("HC-4", "Lando Norris"),
    ("HC-5", "Isack Hadjar"), ("HC-6", "Fernando Alonso"),
    ("HC-7", "Carlos Sainz"), ("HC-8", "Oliver Bearman"),
    ("HC-9", "Franco Colapinto"), ("HC-10", "Gabriel Bortoleto"),
])
print("  Helmet Collection: 10 cards")

make_is("F1 Chrome Diamond Drives", [], [
    ("F175-1", "Formula 1 Canadian Tribute Collector's Edition"),
    ("F175-2", "Formula 1 British Grand Prix 2024"),
    ("F175-3", "Formula 1 Japanese Grand Prix 2024"),
    ("F175-4", "Formula 1 Miami Grand Prix 2024"),
    ("F175-5", "Formula 1 Brazilian Tribute Collector's Edition"),
    ("F175-6", "Formula 1 Chinese Grand Prix 2024"),
    ("F175-7", "Formula 1 American Tribute Collector's Edition"),
    ("F175-8", "Formula 1 United States Grand Prix 2024"),
    ("F175-9", "Formula 1 Las Vegas Grand Prix 2024"),
])
print("  F1 Chrome Diamond Drives: 9 cards")

make_is("Top Speed", TOP_SPEED_PARS, [
    ("TS-1", "Max Verstappen"), ("TS-2", "Lewis Hamilton"),
    ("TS-3", "Oscar Piastri"), ("TS-4", "Kimi Antonelli"),
    ("TS-5", "Fernando Alonso"), ("TS-6", "Liam Lawson"),
    ("TS-7", "Oliver Bearman"), ("TS-8", "Pierre Gasly"),
    ("TS-9", "Alex Albon"), ("TS-10", "Nico Hulkenberg"),
])
print("  Top Speed: 10 cards")

make_is("Four & More", [], [
    ("4N-1", "Max Verstappen"), ("4N-2", "Lewis Hamilton"),
    ("4N-3", "Alain Prost"), ("4N-4", "Michael Schumacher"),
])
print("  Four & More: 4 cards")

make_is("Floor It", INSERT_PARS, [
    ("FI-1", "Alain Prost"), ("FI-2", "Damon Hill"),
    ("FI-3", "Gerhard Berger"), ("FI-4", "Jackie Stewart"),
    ("FI-5", "James Hunt"), ("FI-6", "Kimi R\u00e4ikk\u00f6nen"),
    ("FI-7", "Michael Schumacher"), ("FI-8", "Mika H\u00e4kkinen"),
    ("FI-9", "Nigel Mansell"), ("FI-10", "Ayrton Senna"),
])
print("  Floor It: 10 cards")

make_is("Diamond 75th Anniversary", [], [
    (f"D75-{i}", name) for i, name in enumerate([
        "Max Verstappen", "Yuki Tsunoda", "Charles Leclerc", "Lewis Hamilton",
        "Lando Norris", "Oscar Piastri", "George Russell", "Kimi Antonelli",
        "Fernando Alonso", "Lance Stroll", "Liam Lawson", "Isack Hadjar",
        "Esteban Ocon", "Oliver Bearman", "Franco Colapinto", "Pierre Gasly",
        "Alex Albon", "Carlos Sainz", "Nico Hulkenberg", "Gabriel Bortoleto",
        "Max Verstappen", "Yuki Tsunoda", "Charles Leclerc", "Lewis Hamilton",
        "Lando Norris", "Oscar Piastri", "George Russell", "Kimi Antonelli",
        "Fernando Alonso", "Lance Stroll", "Liam Lawson", "Isack Hadjar",
        "Esteban Ocon", "Oliver Bearman", "Franco Colapinto", "Pierre Gasly",
        "Alex Albon", "Carlos Sainz", "Nico Hulkenberg", "Gabriel Bortoleto",
        "Alain Prost", "Emerson Fittipaldi", "Jackie Stewart", "James Hunt",
        "Juan Pablo Montoya", "Kimi R\u00e4ikk\u00f6nen", "Michael Schumacher",
        "Mika H\u00e4kkinen", "Nigel Mansell", "Ayrton Senna",
    ], 1)
])
print("  Diamond 75th Anniversary: 50 cards")

make_is("Futuro", SUPERFRACTOR_ONLY, [
    ("FUT-1", "Liam Lawson"), ("FUT-2", "Kimi Antonelli"),
    ("FUT-3", "Oliver Bearman"), ("FUT-4", "Gabriel Bortoleto"),
    ("FUT-5", "Franco Colapinto"),
])
print("  Futuro: 5 cards")

make_is("The Chain", SUPERFRACTOR_ONLY, [
    ("CH-1", "Max Verstappen"), ("CH-2", "Charles Leclerc"),
    ("CH-3", "Oscar Piastri"), ("CH-4", "George Russell"),
    ("CH-5", "Lance Stroll"), ("CH-6", "Liam Lawson"),
    ("CH-7", "Esteban Ocon"), ("CH-8", "Pierre Gasly"),
    ("CH-9", "Alex Albon"), ("CH-10", "Nico Hulkenberg"),
])
print("  The Chain: 10 cards")

make_is("Neon Nations", SUPERFRACTOR_ONLY, [
    ("NN-1", "Max Verstappen"), ("NN-2", "Charles Leclerc"),
    ("NN-3", "Oscar Piastri"), ("NN-4", "Kimi Antonelli"),
    ("NN-5", "Fernando Alonso"), ("NN-6", "Isack Hadjar"),
    ("NN-7", "Oliver Bearman"), ("NN-8", "Nico Hulkenberg"),
    ("NN-9", "Alex Albon"),
])
print("  Neon Nations: 9 cards")

make_is("The Grid", SUPERFRACTOR_ONLY, [
    ("TG-1", "Yuki Tsunoda"), ("TG-2", "Kimi Antonelli"),
    ("TG-3", "Lando Norris"), ("TG-4", "Lewis Hamilton"),
    ("TG-5", "Lance Stroll"), ("TG-6", "Isack Hadjar"),
    ("TG-7", "Oliver Bearman"), ("TG-8", "Gabriel Bortoleto"),
    ("TG-9", "Carlos Sainz"), ("TG-10", "Franco Colapinto"),
])
print("  The Grid: 10 cards")

make_is("Ultrasonic", SUPERFRACTOR_ONLY, [
    ("US-1", "Yuki Tsunoda"), ("US-2", "George Russell"),
    ("US-3", "Lando Norris"), ("US-4", "Lewis Hamilton"),
    ("US-5", "Fernando Alonso"), ("US-6", "Liam Lawson"),
    ("US-7", "Esteban Ocon"), ("US-8", "Pierre Gasly"),
    ("US-9", "Nico Hulkenberg"), ("US-10", "Alex Albon"),
    ("US-11", "Emerson Fittipaldi"), ("US-12", "Kimi R\u00e4ikk\u00f6nen"),
    ("US-13", "Damon Hill"), ("US-14", "Gerhard Berger"),
])
print("  Ultrasonic: 14 cards")

make_is("F1 75th Anniversary Logo", F175_LOGO_PARS, [
    ("LOGO-1", "Max Verstappen"), ("LOGO-2", "Oracle Red Bull Racing"),
    ("LOGO-3", "Yuki Tsunoda"), ("LOGO-4", "Charles Leclerc"),
    ("LOGO-5", "Scuderia Ferrari HP"), ("LOGO-6", "Lewis Hamilton"),
    ("LOGO-7", "Lando Norris"), ("LOGO-8", "McLaren Formula 1 Team"),
    ("LOGO-9", "Oscar Piastri"), ("LOGO-10", "George Russell"),
    ("LOGO-11", "Mercedes-AMG PETRONAS Formula One Team"),
    ("LOGO-12", "Kimi Antonelli"), ("LOGO-13", "Fernando Alonso"),
    ("LOGO-14", "Aston Martin Aramco Formula One Team"),
    ("LOGO-15", "Lance Stroll"), ("LOGO-16", "Liam Lawson"),
    ("LOGO-17", "Visa Cash App RB Formula One Team"),
    ("LOGO-18", "Isack Hadjar"), ("LOGO-19", "Esteban Ocon"),
    ("LOGO-20", "MoneyGram Haas F1 Team"), ("LOGO-21", "Oliver Bearman"),
    ("LOGO-22", "Franco Colapinto"), ("LOGO-23", "BWT Alpine Formula One Team"),
    ("LOGO-24", "Pierre Gasly"), ("LOGO-25", "Alex Albon"),
    ("LOGO-26", "Atlassian Williams Racing"), ("LOGO-27", "Carlos Sainz"),
    ("LOGO-28", "Nico Hulkenberg"), ("LOGO-29", "Stake F1 Team KICK Sauber"),
    ("LOGO-30", "Gabriel Bortoleto"),
])
print("  F1 75th Anniversary Logo: 30 cards")

make_is("Vegas At Night", SUPERFRACTOR_ONLY, [
    ("VGS-1", "Oliver Bearman"), ("VGS-2", "Lewis Hamilton"),
    ("VGS-3", "Kimi Antonelli"), ("VGS-4", "Max Verstappen"),
    ("VGS-5", "Lando Norris"),
])
print("  Vegas At Night: 5 cards")

make_is("The Grail", [], [
    ("GrailNo.1", "Max Verstappen"), ("GrailNo.2", "Max Verstappen"),
    ("GrailNo.3", "Max Verstappen"), ("GrailNo.4", "Lando Norris"),
    ("GrailNo.5", "Lando Norris"), ("GrailNo.6", "Lando Norris"),
    ("GrailNo.7", "Charles Leclerc"), ("GrailNo.8", "Charles Leclerc"),
    ("GrailNo.9", "Charles Leclerc"),
])
print("  The Grail: 9 cards")

make_is("Helix", SUPERFRACTOR_ONLY, [
    ("HLX-1", "Max Verstappen"), ("HLX-2", "Yuki Tsunoda"),
    ("HLX-3", "Charles Leclerc"), ("HLX-4", "Lewis Hamilton"),
    ("HLX-5", "Lando Norris"), ("HLX-6", "Oscar Piastri"),
    ("HLX-7", "George Russell"), ("HLX-8", "Kimi Antonelli"),
    ("HLX-9", "Fernando Alonso"), ("HLX-10", "Lance Stroll"),
    ("HLX-11", "Liam Lawson"), ("HLX-12", "Isack Hadjar"),
    ("HLX-13", "Esteban Ocon"), ("HLX-14", "Oliver Bearman"),
    ("HLX-15", "Franco Colapinto"), ("HLX-16", "Pierre Gasly"),
    ("HLX-17", "Alex Albon"), ("HLX-18", "Carlos Sainz"),
    ("HLX-19", "Nico Hulkenberg"), ("HLX-20", "Gabriel Bortoleto"),
])
print("  Helix: 20 cards")

# ─── Update Helix pack odds from 1:700 to 1:900 ──────────────────────────────

cur.execute("SELECT pack_odds FROM sets WHERE id = ?", (SET_ID,))
raw = cur.fetchone()[0]
odds = json.loads(raw)
if "hobby" in odds and "Helix" in odds["hobby"]:
    odds["hobby"]["Helix"] = "1:900"
    cur.execute("UPDATE sets SET pack_odds = ? WHERE id = ?", (json.dumps(odds), SET_ID))
    print("\nUpdated Helix pack odds: 1:700 -> 1:900")

# ─── Compute player stats ─────────────────────────────────────────────────────

print("\nComputing player stats...")
cur.execute("SELECT id FROM players WHERE set_id = ?", (SET_ID,))
player_ids = [r[0] for r in cur.fetchall()]

for pid in player_ids:
    cur.execute("SELECT pa.id, pa.insert_set_id FROM player_appearances pa WHERE pa.player_id = ?", (pid,))
    appearances = cur.fetchall()
    insert_set_ids = set(a[1] for a in appearances)
    unique_cards = 0
    total_print_run = 0
    one_of_ones = 0
    for app_id, is_id in appearances:
        unique_cards += 1
        cur.execute("SELECT name, print_run FROM parallels WHERE insert_set_id = ?", (is_id,))
        for par_name, pr in cur.fetchall():
            unique_cards += 1
            if pr is not None:
                total_print_run += pr
                if pr == 1: one_of_ones += 1
    cur.execute("UPDATE players SET unique_cards = ?, total_print_run = ?, one_of_ones = ?, insert_set_count = ? WHERE id = ?",
                (unique_cards, total_print_run, one_of_ones, len(insert_set_ids), pid))

conn.commit()

# ─── Verify ────────────────────────────────────────────────────────────────────

cur.execute("SELECT COUNT(*) FROM players WHERE set_id = ?", (SET_ID,))
total_players = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id = ?", (SET_ID,))
total_insert_sets = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM player_appearances pa INNER JOIN players p ON p.id = pa.player_id WHERE p.set_id = ?", (SET_ID,))
total_appearances = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM appearance_co_players ac INNER JOIN player_appearances pa ON pa.id = ac.appearance_id INNER JOIN players p ON p.id = pa.player_id WHERE p.set_id = ?", (SET_ID,))
total_co_players = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM parallels par INNER JOIN insert_sets i ON i.id = par.insert_set_id WHERE i.set_id = ?", (SET_ID,))
total_parallels = cur.fetchone()[0]

print(f"\n{'='*50}")
print(f"Set ID:            {SET_ID}")
print(f"Players:           {total_players}")
print(f"Insert Sets:       {total_insert_sets}")
print(f"Appearances:       {total_appearances}")
print(f"Co-player links:   {total_co_players}")
print(f"Parallel types:    {total_parallels}")
print(f"{'='*50}")

conn.close()
print("\nDone!")
