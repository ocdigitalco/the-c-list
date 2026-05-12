"""
Seed: 2025 Topps Finest Football — Full checklist.
300 base cards (3 tiers: Common/Uncommon/Rare), 16 insert subsets, 7 autograph subsets.
Parallel ladder mirrors 2025-26 Topps Finest Basketball (set 25).
Usage: python3 scripts/seed_finest_football_2025.py
"""
import sqlite3, os, json

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
db = sqlite3.connect(DB_PATH)
db.execute("PRAGMA journal_mode=WAL")
db.execute("PRAGMA foreign_keys=ON")

# ─── Create Set ──────────────────────────────────────────────────────────────
box_config = json.dumps({
    "hobby": {
        "cards_per_pack": 10,
        "packs_per_box": 6,
        "boxes_per_case": 8,
        "notes": "Per box: 2 autographs, 11 numbered parallels, 10 inserts"
    }
})

db.execute("""
    INSERT INTO sets (name, sport, season, tier, slug, is_visible,
                      sample_image_url, release_date, box_config)
    VALUES ('2025 Topps Finest Football', 'Football', '2025', 'Finest',
            '2025-topps-finest-football', 1,
            '/sets/2025-topps-finest-football.jpg', '2026-05-15', ?)
""", (box_config,))
SET_ID = db.execute("SELECT last_insert_rowid()").fetchone()[0]
print(f"Created set ID: {SET_ID}")

def get_or_create(name):
    row = db.execute("SELECT id FROM players WHERE set_id = ? AND name = ?", (SET_ID, name)).fetchone()
    if row: return row[0]
    db.execute("INSERT INTO players (set_id, name, unique_cards, total_print_run, one_of_ones, insert_set_count) VALUES (?, ?, 0, 0, 0, 0)", (SET_ID, name))
    return db.execute("SELECT last_insert_rowid()").fetchone()[0]

def add_is(name):
    db.execute("INSERT INTO insert_sets (set_id, name) VALUES (?, ?)", (SET_ID, name))
    return db.execute("SELECT last_insert_rowid()").fetchone()[0]

def add_par(is_id, name, print_run=None):
    db.execute("INSERT INTO parallels (insert_set_id, name, print_run) VALUES (?, ?, ?)", (is_id, name, print_run))

def add_cards(is_id, cards):
    """cards = list of (card_num, name, team, is_rookie)"""
    for num, name, team, rookie in cards:
        pid = get_or_create(name)
        db.execute(
            "INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)",
            (pid, is_id, str(num), 1 if rookie else 0, team)
        )

# ─── BASE PARALLELS (mirroring Finest Basketball) ───────────────────────────
# Unnumbered parallels shared across all base tiers
base_unnumbered = [
    ("Refractor", None),
    ("X-Fractor", None),
    ("Geometric", None),
    ("Oil Spill", None),
]

# Numbered parallels — tiered by rarity (Common gets highest, Rare gets lowest)
# Common (cards 1-100)
base_common_numbered = [
    ("Sky Blue", 350),
    ("Purple", 250),
    ("Blue", 200),
    ("Purple X-Fractor", 150),
    ("Blue Geometric", 100),
    ("Blue X-Fractor", 99),
    ("Green", 75),
    ("Gold", 50),
    ("Gold Geometric", 50),
    ("Orange", 25),
    ("Red/Black Geometric", 25),
    ("Red Geometric", 10),
    ("Red", 5),
    ("Black Geometric", 1),
    ("Superfractor", 1),
]

# Uncommon (cards 101-200)
base_uncommon_numbered = [
    ("Sky Blue", 250),
    ("Purple", 200),
    ("Blue", 150),
    ("Purple X-Fractor", 99),
    ("Purple Geometric", 100),
    ("Blue X-Fractor", 75),
    ("Green", 35),
    ("Gold", 25),
    ("Gold Geometric", 25),
    ("Orange", 20),
    ("Red/Black Geometric", 10),
    ("Red Geometric", 5),
    ("Red", 3),
    ("Black Geometric", 1),
    ("Superfractor", 1),
]

# Rare (cards 201-300)
base_rare_numbered = [
    ("Sky Blue", 150),
    ("Purple", 99),
    ("Blue", 99),
    ("Purple X-Fractor", 75),
    ("Blue X-Fractor", 49),
    ("Blue Geometric", 25),
    ("Green", 25),
    ("Gold", 20),
    ("Gold Geometric", 10),
    ("Orange", 15),
    ("Red/Black Geometric", 5),
    ("Red Geometric", 3),
    ("Red", 3),
    ("Black", 5),
    ("Black Geometric", 1),
    ("Superfractor", 1),
]

# Insert parallels (same as Finest Basketball "Arrivals" ladder)
insert_parallels = [
    ("Refractor", None),
    ("X-Fractor", None),
    ("Geometric", None),
    ("Sky Blue", 150),
    ("Purple", 125),
    ("Blue", 99),
    ("Blue Geometric", 75),
    ("Gold", 50),
    ("Gold Geometric", 50),
    ("Orange", 25),
    ("Red/Black Geometric", 25),
    ("Red Geometric", 10),
    ("Red", 5),
    ("Black Geometric", 1),
    ("Superfractor", 1),
]

# Autograph parallels (same as Finest Basketball "Finest Autographs" ladder)
auto_parallels = [
    ("Blue X-Fractor", 99),
    ("Green Geometric", 75),
    ("Gold", 50),
    ("Gold Geometric", 50),
    ("Orange", 25),
    ("Black Geometric", 25),
    ("Red/Black Geometric", 10),
    ("Red", 5),
    ("Red Geometric", 5),
    ("Superfractor", 1),
]


# ─── BASE CARDS COMMON (1-100) ──────────────────────────────────────────────
R = True  # rookie flag shortcut
base_common_id = add_is("Base Cards Common")
for n, pr in base_unnumbered + base_common_numbered:
    add_par(base_common_id, n, pr)

base_common_cards = [
    (1, "Cam Ward", "Tennessee Titans", R),
    (2, "Jaxson Dart", "New York Giants", R),
    (3, "Tyler Shough", "New Orleans Saints", R),
    (4, "Jalen Milroe", "Seattle Seahawks", R),
    (5, "Dillon Gabriel", "Cleveland Browns", R),
    (6, "Shedeur Sanders", "Cleveland Browns", R),
    (7, "Kyle McCord", "Philadelphia Eagles", R),
    (8, "Will Howard", "Pittsburgh Steelers", R),
    (9, "Riley Leonard", "Indianapolis Colts", R),
    (10, "Quinn Ewers", "Miami Dolphins", R),
    (11, "Ashton Jeanty", "Las Vegas Raiders", R),
    (12, "Omarion Hampton", "Los Angeles Chargers", R),
    (13, "Quinshon Judkins", "Cleveland Browns", R),
    (14, "TreVeyon Henderson", "New England Patriots", R),
    (15, "RJ Harvey", "Denver Broncos", R),
    (16, "Kaleb Johnson", "Pittsburgh Steelers", R),
    (17, "Bhayshul Tuten", "Jacksonville Jaguars", R),
    (18, "Cam Skattebo", "New York Giants", R),
    (19, "Trevor Etienne", "Carolina Panthers", R),
    (20, "Woody Marks", "Houston Texans", R),
    (21, "Jacory Croskey-Merritt", "Washington Commanders", R),
    (22, "Travis Hunter", "Jacksonville Jaguars", R),
    (23, "Tetairoa McMillan", "Carolina Panthers", R),
    (24, "Emeka Egbuka", "Tampa Bay Buccaneers", R),
    (25, "Matthew Golden", "Green Bay Packers", R),
    (26, "Jayden Higgins", "Houston Texans", R),
    (27, "Luther Burden III", "Chicago Bears", R),
    (28, "Tre Harris III", "Los Angeles Chargers", R),
    (29, "Jack Bech", "Las Vegas Raiders", R),
    (30, "Kyle Williams", "New England Patriots", R),
    (31, "Isaac TeSlaa", "Detroit Lions", R),
    (32, "Colston Loveland", "Chicago Bears", R),
    (33, "Tyler Warren", "Indianapolis Colts", R),
    (34, "Mason Taylor", "New York Jets", R),
    (35, "Will Campbell", "New England Patriots", R),
    (36, "Armand Membou", "New York Jets", R),
    (37, "Abdul Carter", "New York Giants", R),
    (38, "Mykel Williams", "San Francisco 49ers", R),
    (39, "Mason Graham", "Cleveland Browns", R),
    (40, "Kenneth Grant", "Miami Dolphins", R),
    (41, "Jalon Walker", "Atlanta Falcons", R),
    (42, "Jihaad Campbell", "Philadelphia Eagles", R),
    (43, "Jahdae Barron", "Denver Broncos", R),
    (44, "Maxwell Hairston", "Buffalo Bills", R),
    (45, "Malaki Starks", "Baltimore Ravens", R),
    (46, "Kyler Murray", "Arizona Cardinals", False),
    (47, "Lamar Jackson", "Baltimore Ravens", False),
    (48, "Josh Allen", "Buffalo Bills", False),
    (49, "Bryce Young", "Carolina Panthers", False),
    (50, "Caleb Williams", "Chicago Bears", False),
    (51, "Joe Burrow", "Cincinnati Bengals", False),
    (52, "Dak Prescott", "Dallas Cowboys", False),
    (53, "Bo Nix", "Denver Broncos", False),
    (54, "Jared Goff", "Detroit Lions", False),
    (55, "Jordan Love", "Green Bay Packers", False),
    (56, "CJ Stroud", "Houston Texans", False),
    (57, "Daniel Jones", "Indianapolis Colts", False),
    (58, "Patrick Mahomes II", "Kansas City Chiefs", False),
    (59, "Justin Herbert", "Los Angeles Chargers", False),
    (60, "Matthew Stafford", "Los Angeles Rams", False),
    (61, "J.J. McCarthy", "Minnesota Vikings", False),
    (62, "Drake Maye", "New England Patriots", False),
    (63, "Jalen Hurts", "Philadelphia Eagles", False),
    (64, "Aaron Rodgers", "Pittsburgh Steelers", False),
    (65, "Brock Purdy", "San Francisco 49ers", False),
    (66, "Baker Mayfield", "Tampa Bay Buccaneers", False),
    (67, "Jayden Daniels", "Washington Commanders", False),
    (68, "James Conner", "Arizona Cardinals", False),
    (69, "Bijan Robinson", "Atlanta Falcons", False),
    (70, "Derrick Henry", "Baltimore Ravens", False),
    (71, "James Cook", "Buffalo Bills", False),
    (72, "D'Andre Swift", "Chicago Bears", False),
    (73, "Chase Brown", "Cincinnati Bengals", False),
    (74, "Javonte Williams", "Dallas Cowboys", False),
    (75, "Jahmyr Gibbs", "Detroit Lions", False),
    (76, "Josh Jacobs", "Green Bay Packers", False),
    (77, "Jonathan Taylor", "Indianapolis Colts", False),
    (78, "Saquon Barkley", "Philadelphia Eagles", False),
    (79, "Christian McCaffrey", "San Francisco 49ers", False),
    (80, "Marvin Harrison Jr.", "Arizona Cardinals", False),
    (81, "Drake London", "Atlanta Falcons", False),
    (82, "Zay Flowers", "Baltimore Ravens", False),
    (83, "Keon Coleman", "Buffalo Bills", False),
    (84, "Rome Odunze", "Chicago Bears", False),
    (85, "Ja'Marr Chase", "Cincinnati Bengals", False),
    (86, "Jerry Jeudy", "Cleveland Browns", False),
    (87, "CeeDee Lamb", "Dallas Cowboys", False),
    (88, "Courtland Sutton", "Denver Broncos", False),
    (89, "Puka Nacua", "Los Angeles Rams", False),
    (90, "Justin Jefferson", "Minnesota Vikings", False),
    (91, "Malik Nabers", "New York Giants", False),
    (92, "DK Metcalf", "Pittsburgh Steelers", False),
    (93, "Mike Evans", "Tampa Bay Buccaneers", False),
    (94, "Travis Kelce", "Kansas City Chiefs", False),
    (95, "Brock Bowers", "Las Vegas Raiders", False),
    (96, "George Kittle", "San Francisco 49ers", False),
    (97, "Myles Garrett", "Cleveland Browns", False),
    (98, "Micah Parsons", "Green Bay Packers", False),
    (99, "T.J. Watt", "Pittsburgh Steelers", False),
    (100, "Tom Brady", "New England Patriots", False),
]
add_cards(base_common_id, base_common_cards)
print(f"  Base Cards Common: {len(base_common_cards)} cards")


# ─── BASE CARDS UNCOMMON (101-200) ──────────────────────────────────────────
base_uncommon_id = add_is("Base Cards Uncommon")
for n, pr in base_unnumbered + base_uncommon_numbered:
    add_par(base_uncommon_id, n, pr)

base_uncommon_cards = [
    (101, "Cam Ward", "Tennessee Titans", R),
    (102, "Jaxson Dart", "New York Giants", R),
    (103, "Tyler Shough", "New Orleans Saints", R),
    (104, "Jalen Milroe", "Seattle Seahawks", R),
    (105, "Dillon Gabriel", "Cleveland Browns", R),
    (106, "Shedeur Sanders", "Cleveland Browns", R),
    (107, "Quinn Ewers", "Miami Dolphins", R),
    (108, "Ashton Jeanty", "Las Vegas Raiders", R),
    (109, "Omarion Hampton", "Los Angeles Chargers", R),
    (110, "Quinshon Judkins", "Cleveland Browns", R),
    (111, "TreVeyon Henderson", "New England Patriots", R),
    (112, "RJ Harvey", "Denver Broncos", R),
    (113, "Cam Skattebo", "New York Giants", R),
    (114, "Travis Hunter", "Jacksonville Jaguars", R),
    (115, "Tetairoa McMillan", "Carolina Panthers", R),
    (116, "Emeka Egbuka", "Tampa Bay Buccaneers", R),
    (117, "Matthew Golden", "Green Bay Packers", R),
    (118, "Jayden Higgins", "Houston Texans", R),
    (119, "Luther Burden III", "Chicago Bears", R),
    (120, "Tyler Warren", "Indianapolis Colts", R),
    (121, "Abdul Carter", "New York Giants", R),
    (122, "Kyler Murray", "Arizona Cardinals", False),
    (123, "Michael Penix Jr.", "Atlanta Falcons", False),
    (124, "Lamar Jackson", "Baltimore Ravens", False),
    (125, "Josh Allen", "Buffalo Bills", False),
    (126, "Bryce Young", "Carolina Panthers", False),
    (127, "Caleb Williams", "Chicago Bears", False),
    (128, "Joe Burrow", "Cincinnati Bengals", False),
    (129, "Dak Prescott", "Dallas Cowboys", False),
    (130, "Bo Nix", "Denver Broncos", False),
    (131, "Jared Goff", "Detroit Lions", False),
    (132, "Jordan Love", "Green Bay Packers", False),
    (133, "CJ Stroud", "Houston Texans", False),
    (134, "Daniel Jones", "Indianapolis Colts", False),
    (135, "Trevor Lawrence", "Jacksonville Jaguars", False),
    (136, "Patrick Mahomes II", "Kansas City Chiefs", False),
    (137, "Geno Smith", "Las Vegas Raiders", False),
    (138, "Justin Herbert", "Los Angeles Chargers", False),
    (139, "Matthew Stafford", "Los Angeles Rams", False),
    (140, "Tua Tagovailoa", "Miami Dolphins", False),
    (141, "J.J. McCarthy", "Minnesota Vikings", False),
    (142, "Drake Maye", "New England Patriots", False),
    (143, "Justin Fields", "New York Jets", False),
    (144, "Jalen Hurts", "Philadelphia Eagles", False),
    (145, "Aaron Rodgers", "Pittsburgh Steelers", False),
    (146, "Brock Purdy", "San Francisco 49ers", False),
    (147, "Sam Darnold", "Seattle Seahawks", False),
    (148, "Baker Mayfield", "Tampa Bay Buccaneers", False),
    (149, "Jayden Daniels", "Washington Commanders", False),
    (150, "Bijan Robinson", "Atlanta Falcons", False),
    (151, "Derrick Henry", "Baltimore Ravens", False),
    (152, "Jahmyr Gibbs", "Detroit Lions", False),
    (153, "Joe Mixon", "Houston Texans", False),
    (154, "Jonathan Taylor", "Indianapolis Colts", False),
    (155, "Travis Etienne", "Jacksonville Jaguars", False),
    (156, "Isiah Pacheco", "Kansas City Chiefs", False),
    (157, "Kyren Williams", "Los Angeles Rams", False),
    (158, "De'Von Achane", "Miami Dolphins", False),
    (159, "Aaron Jones Sr.", "Minnesota Vikings", False),
    (160, "Alvin Kamara", "New Orleans Saints", False),
    (161, "Saquon Barkley", "Philadelphia Eagles", False),
    (162, "Ja'Marr Chase", "Cincinnati Bengals", False),
    (163, "CeeDee Lamb", "Dallas Cowboys", False),
    (164, "Amon-Ra St. Brown", "Detroit Lions", False),
    (165, "Nico Collins", "Houston Texans", False),
    (166, "Michael Pittman Jr.", "Indianapolis Colts", False),
    (167, "Brian Thomas Jr.", "Jacksonville Jaguars", False),
    (168, "Xavier Worthy", "Kansas City Chiefs", False),
    (169, "Ladd McConkey", "Los Angeles Chargers", False),
    (170, "Puka Nacua", "Los Angeles Rams", False),
    (171, "Jaylen Waddle", "Miami Dolphins", False),
    (172, "Justin Jefferson", "Minnesota Vikings", False),
    (173, "Stefon Diggs", "New England Patriots", False),
    (174, "Chris Olave", "New Orleans Saints", False),
    (175, "Malik Nabers", "New York Giants", False),
    (176, "Garrett Wilson", "New York Jets", False),
    (177, "Jaxon Smith-Njigba", "Seattle Seahawks", False),
    (178, "Mark Andrews", "Baltimore Ravens", False),
    (179, "Dalton Kincaid", "Buffalo Bills", False),
    (180, "David Njoku", "Cleveland Browns", False),
    (181, "Travis Kelce", "Kansas City Chiefs", False),
    (182, "Brock Bowers", "Las Vegas Raiders", False),
    (183, "Dallas Goedert", "Philadelphia Eagles", False),
    (184, "George Kittle", "San Francisco 49ers", False),
    (185, "Myles Garrett", "Cleveland Browns", False),
    (186, "Aidan Hutchinson", "Detroit Lions", False),
    (187, "Micah Parsons", "Green Bay Packers", False),
    (188, "Maxx Crosby", "Las Vegas Raiders", False),
    (189, "T.J. Watt", "Pittsburgh Steelers", False),
    (190, "Jalen Carter", "Philadelphia Eagles", False),
    (191, "Dexter Lawrence", "New York Giants", False),
    (192, "Will Anderson Jr.", "Houston Texans", False),
    (193, "Fred Warner", "San Francisco 49ers", False),
    (194, "Pat Surtain II", "Denver Broncos", False),
    (195, "Sauce Gardner", "Indianapolis Colts", False),
    (196, "Kyle Hamilton", "Baltimore Ravens", False),
    (197, "Tom Brady", "New England Patriots", False),
    (198, "Peyton Manning", "Indianapolis Colts", False),
    (199, "Emmitt Smith", "Dallas Cowboys", False),
    (200, "Jerry Rice", "San Francisco 49ers", False),
]
add_cards(base_uncommon_id, base_uncommon_cards)
print(f"  Base Cards Uncommon: {len(base_uncommon_cards)} cards")


# ─── BASE CARDS RARE (201-300) ──────────────────────────────────────────────
base_rare_id = add_is("Base Cards Rare")
for n, pr in base_unnumbered + base_rare_numbered:
    add_par(base_rare_id, n, pr)

base_rare_cards = [
    (201, "Cam Ward", "Tennessee Titans", R),
    (202, "Jaxson Dart", "New York Giants", R),
    (203, "Tyler Shough", "New Orleans Saints", R),
    (204, "Jalen Milroe", "Seattle Seahawks", R),
    (205, "Dillon Gabriel", "Cleveland Browns", R),
    (206, "Shedeur Sanders", "Cleveland Browns", R),
    (207, "Ashton Jeanty", "Las Vegas Raiders", R),
    (208, "Omarion Hampton", "Los Angeles Chargers", R),
    (209, "Quinshon Judkins", "Cleveland Browns", R),
    (210, "TreVeyon Henderson", "New England Patriots", R),
    (211, "RJ Harvey", "Denver Broncos", R),
    (212, "Cam Skattebo", "New York Giants", R),
    (213, "Jacory Croskey-Merritt", "Washington Commanders", R),
    (214, "Travis Hunter", "Jacksonville Jaguars", R),
    (215, "Tetairoa McMillan", "Carolina Panthers", R),
    (216, "Emeka Egbuka", "Tampa Bay Buccaneers", R),
    (217, "Matthew Golden", "Green Bay Packers", R),
    (218, "Jayden Higgins", "Houston Texans", R),
    (219, "Luther Burden III", "Chicago Bears", R),
    (220, "Tyler Warren", "Indianapolis Colts", R),
    (221, "Abdul Carter", "New York Giants", R),
    (222, "Mason Graham", "Cleveland Browns", R),
    (223, "Kyler Murray", "Arizona Cardinals", False),
    (224, "Michael Penix Jr.", "Atlanta Falcons", False),
    (225, "Lamar Jackson", "Baltimore Ravens", False),
    (226, "Josh Allen", "Buffalo Bills", False),
    (227, "Bryce Young", "Carolina Panthers", False),
    (228, "Caleb Williams", "Chicago Bears", False),
    (229, "Joe Burrow", "Cincinnati Bengals", False),
    (230, "Dak Prescott", "Dallas Cowboys", False),
    (231, "Bo Nix", "Denver Broncos", False),
    (232, "Jared Goff", "Detroit Lions", False),
    (233, "Jordan Love", "Green Bay Packers", False),
    (234, "CJ Stroud", "Houston Texans", False),
    (235, "Daniel Jones", "Indianapolis Colts", False),
    (236, "Trevor Lawrence", "Jacksonville Jaguars", False),
    (237, "Patrick Mahomes II", "Kansas City Chiefs", False),
    (238, "Geno Smith", "Las Vegas Raiders", False),
    (239, "Justin Herbert", "Los Angeles Chargers", False),
    (240, "Matthew Stafford", "Los Angeles Rams", False),
    (241, "Tua Tagovailoa", "Miami Dolphins", False),
    (242, "J.J. McCarthy", "Minnesota Vikings", False),
    (243, "Drake Maye", "New England Patriots", False),
    (244, "Justin Fields", "New York Jets", False),
    (245, "Jalen Hurts", "Philadelphia Eagles", False),
    (246, "Aaron Rodgers", "Pittsburgh Steelers", False),
    (247, "Brock Purdy", "San Francisco 49ers", False),
    (248, "Sam Darnold", "Seattle Seahawks", False),
    (249, "Baker Mayfield", "Tampa Bay Buccaneers", False),
    (250, "Jayden Daniels", "Washington Commanders", False),
    (251, "Derrick Henry", "Baltimore Ravens", False),
    (252, "David Montgomery", "Detroit Lions", False),
    (253, "Tyrone Tracy Jr.", "New York Giants", False),
    (254, "Breece Hall", "New York Jets", False),
    (255, "Saquon Barkley", "Philadelphia Eagles", False),
    (256, "Jaylen Warren", "Pittsburgh Steelers", False),
    (257, "Christian McCaffrey", "San Francisco 49ers", False),
    (258, "Kenneth Walker III", "Seattle Seahawks", False),
    (259, "Bucky Irving", "Tampa Bay Buccaneers", False),
    (260, "Tony Pollard", "Tennessee Titans", False),
    (261, "Marvin Harrison Jr.", "Arizona Cardinals", False),
    (262, "Ja'Marr Chase", "Cincinnati Bengals", False),
    (263, "CeeDee Lamb", "Dallas Cowboys", False),
    (264, "Justin Jefferson", "Minnesota Vikings", False),
    (265, "A.J. Brown", "Philadelphia Eagles", False),
    (266, "DeVonta Smith", "Philadelphia Eagles", False),
    (267, "DK Metcalf", "Pittsburgh Steelers", False),
    (268, "Ricky Pearsall", "San Francisco 49ers", False),
    (269, "Jaxon Smith-Njigba", "Seattle Seahawks", False),
    (270, "Mike Evans", "Tampa Bay Buccaneers", False),
    (271, "Deebo Samuel", "Washington Commanders", False),
    (272, "Trey McBride", "Arizona Cardinals", False),
    (273, "Kyle Pitts", "Atlanta Falcons", False),
    (274, "Jake Ferguson", "Dallas Cowboys", False),
    (275, "Sam LaPorta", "Detroit Lions", False),
    (276, "Travis Kelce", "Kansas City Chiefs", False),
    (277, "Brock Bowers", "Las Vegas Raiders", False),
    (278, "George Kittle", "San Francisco 49ers", False),
    (279, "Myles Garrett", "Cleveland Browns", False),
    (280, "Aidan Hutchinson", "Detroit Lions", False),
    (281, "Micah Parsons", "Green Bay Packers", False),
    (282, "Maxx Crosby", "Las Vegas Raiders", False),
    (283, "T.J. Watt", "Pittsburgh Steelers", False),
    (284, "Chris Jones", "Kansas City Chiefs", False),
    (285, "Jalen Carter", "Philadelphia Eagles", False),
    (286, "Roquan Smith", "Baltimore Ravens", False),
    (287, "Fred Warner", "San Francisco 49ers", False),
    (288, "Pat Surtain II", "Denver Broncos", False),
    (289, "Sauce Gardner", "Indianapolis Colts", False),
    (290, "Derwin James Jr.", "Los Angeles Chargers", False),
    (291, "Brett Favre", "Green Bay Packers", False),
    (292, "Peyton Manning", "Indianapolis Colts", False),
    (293, "Tom Brady", "New England Patriots", False),
    (294, "Walter Payton", "Chicago Bears", False),
    (295, "Emmitt Smith", "Dallas Cowboys", False),
    (296, "Randy Moss", "Minnesota Vikings", False),
    (297, "Jerry Rice", "San Francisco 49ers", False),
    (298, "Tony Gonzalez", "Atlanta Falcons", False),
    (299, "Pat Tillman", "Arizona Cardinals", False),
    (300, "Sean Taylor", "Washington Redskins", False),
]
add_cards(base_rare_id, base_rare_cards)
print(f"  Base Cards Rare: {len(base_rare_cards)} cards")


# ─── INSERT SUBSETS ─────────────────────────────────────────────────────────
def add_insert_subset(name, cards):
    is_id = add_is(name)
    for n, pr in insert_parallels:
        add_par(is_id, n, pr)
    add_cards(is_id, cards)
    print(f"  {name}: {len(cards)} cards")
    return is_id


# Reflash (RF-1 to RF-20)
add_insert_subset("Reflash", [
    ("RF-1", "Michael Penix Jr.", "Atlanta Falcons", False),
    ("RF-2", "Caleb Williams", "Chicago Bears", False),
    ("RF-3", "Bo Nix", "Denver Broncos", False),
    ("RF-4", "J.J. McCarthy", "Minnesota Vikings", False),
    ("RF-5", "Drake Maye", "New England Patriots", False),
    ("RF-6", "Jayden Daniels", "Washington Commanders", False),
    ("RF-7", "Tyrone Tracy Jr.", "New York Giants", False),
    ("RF-8", "Braelon Allen", "New York Jets", False),
    ("RF-9", "Bucky Irving", "Tampa Bay Buccaneers", False),
    ("RF-10", "Marvin Harrison Jr.", "Arizona Cardinals", False),
    ("RF-11", "Keon Coleman", "Buffalo Bills", False),
    ("RF-12", "Rome Odunze", "Chicago Bears", False),
    ("RF-13", "Brian Thomas Jr.", "Jacksonville Jaguars", False),
    ("RF-14", "Xavier Worthy", "Kansas City Chiefs", False),
    ("RF-15", "Ladd McConkey", "Los Angeles Chargers", False),
    ("RF-16", "Malik Nabers", "New York Giants", False),
    ("RF-17", "Ricky Pearsall", "San Francisco 49ers", False),
    ("RF-18", "Brock Bowers", "Las Vegas Raiders", False),
    ("RF-19", "Jared Verse", "Los Angeles Rams", False),
    ("RF-20", "Cooper DeJean", "Philadelphia Eagles", False),
])

# Torchers (T-1 to T-30)
add_insert_subset("Torchers", [
    ("T-1", "Dillon Gabriel", "Cleveland Browns", R),
    ("T-2", "Shedeur Sanders", "Cleveland Browns", R),
    ("T-3", "Tyler Shough", "New Orleans Saints", R),
    ("T-4", "Jaxson Dart", "New York Giants", R),
    ("T-5", "Cam Ward", "Tennessee Titans", R),
    ("T-6", "Jalen Milroe", "Seattle Seahawks", R),
    ("T-7", "Kyler Murray", "Arizona Cardinals", False),
    ("T-8", "Michael Penix Jr.", "Atlanta Falcons", False),
    ("T-9", "Lamar Jackson", "Baltimore Ravens", False),
    ("T-10", "Josh Allen", "Buffalo Bills", False),
    ("T-11", "Bryce Young", "Carolina Panthers", False),
    ("T-12", "Caleb Williams", "Chicago Bears", False),
    ("T-13", "Joe Burrow", "Cincinnati Bengals", False),
    ("T-14", "Dak Prescott", "Dallas Cowboys", False),
    ("T-15", "Bo Nix", "Denver Broncos", False),
    ("T-16", "Jared Goff", "Detroit Lions", False),
    ("T-17", "Jordan Love", "Green Bay Packers", False),
    ("T-18", "CJ Stroud", "Houston Texans", False),
    ("T-19", "Trevor Lawrence", "Jacksonville Jaguars", False),
    ("T-20", "Patrick Mahomes II", "Kansas City Chiefs", False),
    ("T-21", "Justin Herbert", "Los Angeles Chargers", False),
    ("T-22", "Matthew Stafford", "Los Angeles Rams", False),
    ("T-23", "Tua Tagovailoa", "Miami Dolphins", False),
    ("T-24", "J.J. McCarthy", "Minnesota Vikings", False),
    ("T-25", "Drake Maye", "New England Patriots", False),
    ("T-26", "Jalen Hurts", "Philadelphia Eagles", False),
    ("T-27", "Aaron Rodgers", "Pittsburgh Steelers", False),
    ("T-28", "Brock Purdy", "San Francisco 49ers", False),
    ("T-29", "Baker Mayfield", "Tampa Bay Buccaneers", False),
    ("T-30", "Jayden Daniels", "Washington Commanders", False),
])

# Power Kings (PK-1 to PK-10)
add_insert_subset("Power Kings", [
    ("PK-1", "Derrick Henry", "Baltimore Ravens", False),
    ("PK-2", "Josh Jacobs", "Green Bay Packers", False),
    ("PK-3", "Ashton Jeanty", "Las Vegas Raiders", R),
    ("PK-4", "A.J. Brown", "Philadelphia Eagles", False),
    ("PK-5", "Mike Evans", "Tampa Bay Buccaneers", False),
    ("PK-6", "DK Metcalf", "Pittsburgh Steelers", False),
    ("PK-7", "Deebo Samuel", "Washington Commanders", False),
    ("PK-8", "Travis Kelce", "Kansas City Chiefs", False),
    ("PK-9", "Brock Bowers", "Las Vegas Raiders", False),
    ("PK-10", "George Kittle", "San Francisco 49ers", False),
])

# Centurions (C-1 to C-15)
add_insert_subset("Centurions", [
    ("C-1", "Derrick Henry", "Baltimore Ravens", False),
    ("C-2", "Josh Allen", "Buffalo Bills", False),
    ("C-3", "Tetairoa McMillan", "Carolina Panthers", R),
    ("C-4", "Caleb Williams", "Chicago Bears", False),
    ("C-5", "Joe Burrow", "Cincinnati Bengals", False),
    ("C-6", "Myles Garrett", "Cleveland Browns", False),
    ("C-7", "Dak Prescott", "Dallas Cowboys", False),
    ("C-8", "Amon-Ra St. Brown", "Detroit Lions", False),
    ("C-9", "Jordan Love", "Green Bay Packers", False),
    ("C-10", "Patrick Mahomes II", "Kansas City Chiefs", False),
    ("C-11", "Justin Jefferson", "Minnesota Vikings", False),
    ("C-12", "Drake Maye", "New England Patriots", False),
    ("C-13", "Saquon Barkley", "Philadelphia Eagles", False),
    ("C-14", "Cam Ward", "Tennessee Titans", R),
    ("C-15", "Jayden Daniels", "Washington Commanders", False),
])

# The Man (TM-1 to TM-20)
add_insert_subset("The Man", [
    ("TM-1", "Josh Allen", "Buffalo Bills", False),
    ("TM-2", "Joe Burrow", "Cincinnati Bengals", False),
    ("TM-3", "Jordan Love", "Green Bay Packers", False),
    ("TM-4", "Patrick Mahomes II", "Kansas City Chiefs", False),
    ("TM-5", "Jaxson Dart", "New York Giants", R),
    ("TM-6", "Cam Ward", "Tennessee Titans", R),
    ("TM-7", "Bijan Robinson", "Atlanta Falcons", False),
    ("TM-8", "Derrick Henry", "Baltimore Ravens", False),
    ("TM-9", "Ashton Jeanty", "Las Vegas Raiders", R),
    ("TM-10", "De'Von Achane", "Miami Dolphins", False),
    ("TM-11", "Cam Skattebo", "New York Giants", R),
    ("TM-12", "Saquon Barkley", "Philadelphia Eagles", False),
    ("TM-13", "Ja'Marr Chase", "Cincinnati Bengals", False),
    ("TM-14", "CeeDee Lamb", "Dallas Cowboys", False),
    ("TM-15", "Amon-Ra St. Brown", "Detroit Lions", False),
    ("TM-16", "Justin Jefferson", "Minnesota Vikings", False),
    ("TM-17", "Brock Bowers", "Las Vegas Raiders", False),
    ("TM-18", "George Kittle", "San Francisco 49ers", False),
    ("TM-19", "Myles Garrett", "Cleveland Browns", False),
    ("TM-20", "T.J. Watt", "Pittsburgh Steelers", False),
])

# For The Record (FTR-1 to FTR-10)
add_insert_subset("For The Record", [
    ("FTR-1", "Lamar Jackson", "Baltimore Ravens", False),
    ("FTR-2", "Aaron Rodgers", "Pittsburgh Steelers", False),
    ("FTR-3", "Jayden Daniels", "Washington Commanders", False),
    ("FTR-4", "Derrick Henry", "Baltimore Ravens", False),
    ("FTR-5", "Saquon Barkley", "Philadelphia Eagles", False),
    ("FTR-6", "Xavier Worthy", "Kansas City Chiefs", False),
    ("FTR-7", "Malik Nabers", "New York Giants", False),
    ("FTR-8", "Mike Evans", "Tampa Bay Buccaneers", False),
    ("FTR-9", "Travis Kelce", "Kansas City Chiefs", False),
    ("FTR-10", "Brock Bowers", "Las Vegas Raiders", False),
])

# Framed White (FW-1 to FW-25)
add_insert_subset("Framed White", [
    ("FW-1", "Michael Penix Jr.", "Atlanta Falcons", False),
    ("FW-2", "Derrick Henry", "Baltimore Ravens", False),
    ("FW-3", "Josh Allen", "Buffalo Bills", False),
    ("FW-4", "Bryce Young", "Carolina Panthers", False),
    ("FW-5", "Luther Burden III", "Chicago Bears", R),
    ("FW-6", "Ja'Marr Chase", "Cincinnati Bengals", False),
    ("FW-7", "Shedeur Sanders", "Cleveland Browns", R),
    ("FW-8", "Dak Prescott", "Dallas Cowboys", False),
    ("FW-9", "Bo Nix", "Denver Broncos", False),
    ("FW-10", "Jahmyr Gibbs", "Detroit Lions", False),
    ("FW-11", "Matthew Golden", "Green Bay Packers", R),
    ("FW-12", "CJ Stroud", "Houston Texans", False),
    ("FW-13", "Travis Kelce", "Kansas City Chiefs", False),
    ("FW-14", "Ashton Jeanty", "Las Vegas Raiders", R),
    ("FW-15", "Matthew Stafford", "Los Angeles Rams", False),
    ("FW-16", "Jaylen Waddle", "Miami Dolphins", False),
    ("FW-17", "J.J. McCarthy", "Minnesota Vikings", False),
    ("FW-18", "TreVeyon Henderson", "New England Patriots", R),
    ("FW-19", "Jaxson Dart", "New York Giants", R),
    ("FW-20", "Jalen Hurts", "Philadelphia Eagles", False),
    ("FW-21", "DK Metcalf", "Pittsburgh Steelers", False),
    ("FW-22", "Christian McCaffrey", "San Francisco 49ers", False),
    ("FW-23", "Emeka Egbuka", "Tampa Bay Buccaneers", R),
    ("FW-24", "Cam Ward", "Tennessee Titans", R),
    ("FW-25", "Deebo Samuel", "Washington Commanders", False),
])

# Creators (CR-1 to CR-30)
add_insert_subset("Creators", [
    ("CR-1", "James Conner", "Arizona Cardinals", False),
    ("CR-2", "Drake London", "Atlanta Falcons", False),
    ("CR-3", "Lamar Jackson", "Baltimore Ravens", False),
    ("CR-4", "Josh Allen", "Buffalo Bills", False),
    ("CR-5", "Tetairoa McMillan", "Carolina Panthers", R),
    ("CR-6", "Rome Odunze", "Chicago Bears", False),
    ("CR-7", "Joe Burrow", "Cincinnati Bengals", False),
    ("CR-8", "Dak Prescott", "Dallas Cowboys", False),
    ("CR-9", "Courtland Sutton", "Denver Broncos", False),
    ("CR-10", "David Montgomery", "Detroit Lions", False),
    ("CR-11", "Jordan Love", "Green Bay Packers", False),
    ("CR-12", "CJ Stroud", "Houston Texans", False),
    ("CR-13", "Jonathan Taylor", "Indianapolis Colts", False),
    ("CR-14", "Travis Hunter", "Jacksonville Jaguars", R),
    ("CR-15", "Xavier Worthy", "Kansas City Chiefs", False),
    ("CR-16", "Ashton Jeanty", "Las Vegas Raiders", R),
    ("CR-17", "Justin Herbert", "Los Angeles Chargers", False),
    ("CR-18", "Puka Nacua", "Los Angeles Rams", False),
    ("CR-19", "Tyreek Hill", "Miami Dolphins", False),
    ("CR-20", "Justin Jefferson", "Minnesota Vikings", False),
    ("CR-21", "Drake Maye", "New England Patriots", False),
    ("CR-22", "Malik Nabers", "New York Giants", False),
    ("CR-23", "Garrett Wilson", "New York Jets", False),
    ("CR-24", "DeVonta Smith", "Philadelphia Eagles", False),
    ("CR-25", "Aaron Rodgers", "Pittsburgh Steelers", False),
    ("CR-26", "Christian McCaffrey", "San Francisco 49ers", False),
    ("CR-27", "Jaxon Smith-Njigba", "Seattle Seahawks", False),
    ("CR-28", "Emeka Egbuka", "Tampa Bay Buccaneers", R),
    ("CR-29", "Cam Ward", "Tennessee Titans", R),
    ("CR-30", "Jayden Daniels", "Washington Commanders", False),
])

# Nightmare Fuel (NF-1 to NF-15)
add_insert_subset("Nightmare Fuel", [
    ("NF-1", "Chris Jones", "Kansas City Chiefs", False),
    ("NF-2", "Trey Hendrickson", "Cincinnati Bengals", False),
    ("NF-3", "Myles Garrett", "Cleveland Browns", False),
    ("NF-4", "Aidan Hutchinson", "Detroit Lions", False),
    ("NF-5", "Micah Parsons", "Green Bay Packers", False),
    ("NF-6", "Maxx Crosby", "Las Vegas Raiders", False),
    ("NF-7", "T.J. Watt", "Pittsburgh Steelers", False),
    ("NF-8", "Fred Warner", "San Francisco 49ers", False),
    ("NF-9", "Pat Surtain II", "Denver Broncos", False),
    ("NF-10", "Sauce Gardner", "Indianapolis Colts", False),
    ("NF-11", "Lawrence Taylor", "New York Giants", False),
    ("NF-12", "Reggie White", "Philadelphia Eagles", False),
    ("NF-13", "Ray Lewis", "Baltimore Ravens", False),
    ("NF-14", "Troy Polamalu", "Pittsburgh Steelers", False),
    ("NF-15", "Brian Urlacher", "Chicago Bears", False),
])

# Smashing Through (ST-1 to ST-15)
add_insert_subset("Smashing Through", [
    ("ST-1", "Bijan Robinson", "Atlanta Falcons", False),
    ("ST-2", "Lamar Jackson", "Baltimore Ravens", False),
    ("ST-3", "Josh Allen", "Buffalo Bills", False),
    ("ST-4", "Caleb Williams", "Chicago Bears", False),
    ("ST-5", "Joe Burrow", "Cincinnati Bengals", False),
    ("ST-6", "Micah Parsons", "Green Bay Packers", False),
    ("ST-7", "Patrick Mahomes II", "Kansas City Chiefs", False),
    ("ST-8", "Ashton Jeanty", "Las Vegas Raiders", R),
    ("ST-9", "Justin Herbert", "Los Angeles Chargers", False),
    ("ST-10", "Jaxson Dart", "New York Giants", R),
    ("ST-11", "Cam Skattebo", "New York Giants", R),
    ("ST-12", "A.J. Brown", "Philadelphia Eagles", False),
    ("ST-13", "Aaron Rodgers", "Pittsburgh Steelers", False),
    ("ST-14", "Brock Purdy", "San Francisco 49ers", False),
    ("ST-15", "Cam Ward", "Tennessee Titans", R),
])

# Landmark Metal Series (LMS-1 to LMS-20)
add_insert_subset("Landmark Metal Series", [
    ("LMS-1", "Cam Ward", "Tennessee Titans", R),
    ("LMS-2", "Jaxson Dart", "New York Giants", R),
    ("LMS-3", "Shedeur Sanders", "Cleveland Browns", R),
    ("LMS-4", "Ashton Jeanty", "Las Vegas Raiders", R),
    ("LMS-5", "Tetairoa McMillan", "Carolina Panthers", R),
    ("LMS-6", "Emeka Egbuka", "Tampa Bay Buccaneers", R),
    ("LMS-7", "Travis Hunter", "Jacksonville Jaguars", R),
    ("LMS-8", "Patrick Mahomes II", "Kansas City Chiefs", False),
    ("LMS-9", "Josh Allen", "Buffalo Bills", False),
    ("LMS-10", "Joe Burrow", "Cincinnati Bengals", False),
    ("LMS-11", "Lamar Jackson", "Baltimore Ravens", False),
    ("LMS-12", "Jalen Hurts", "Philadelphia Eagles", False),
    ("LMS-13", "Jayden Daniels", "Washington Commanders", False),
    ("LMS-14", "Saquon Barkley", "Philadelphia Eagles", False),
    ("LMS-15", "Derrick Henry", "Baltimore Ravens", False),
    ("LMS-16", "Justin Jefferson", "Minnesota Vikings", False),
    ("LMS-17", "Ja'Marr Chase", "Cincinnati Bengals", False),
    ("LMS-18", "CeeDee Lamb", "Dallas Cowboys", False),
    ("LMS-19", "Travis Kelce", "Kansas City Chiefs", False),
    ("LMS-20", "George Kittle", "San Francisco 49ers", False),
])

# 92 Finest (92-1 to 92-44)
add_insert_subset("92 Finest", [
    ("92-1", "Trey McBride", "Arizona Cardinals", False),
    ("92-2", "Bijan Robinson", "Atlanta Falcons", False),
    ("92-3", "Kyle Hamilton", "Baltimore Ravens", False),
    ("92-4", "James Cook", "Buffalo Bills", False),
    ("92-5", "Bryce Young", "Carolina Panthers", False),
    ("92-6", "Tetairoa McMillan", "Carolina Panthers", R),
    ("92-7", "Caleb Williams", "Chicago Bears", False),
    ("92-8", "Tee Higgins", "Cincinnati Bengals", False),
    ("92-9", "Quinshon Judkins", "Cleveland Browns", R),
    ("92-10", "Shedeur Sanders", "Cleveland Browns", R),
    ("92-11", "CeeDee Lamb", "Dallas Cowboys", False),
    ("92-12", "Dak Prescott", "Dallas Cowboys", False),
    ("92-13", "Bo Nix", "Denver Broncos", False),
    ("92-14", "Jared Goff", "Detroit Lions", False),
    ("92-15", "Matthew Golden", "Green Bay Packers", R),
    ("92-16", "Nico Collins", "Houston Texans", False),
    ("92-17", "Michael Pittman Jr.", "Indianapolis Colts", False),
    ("92-18", "Travis Hunter", "Jacksonville Jaguars", R),
    ("92-19", "Travis Kelce", "Kansas City Chiefs", False),
    ("92-20", "Xavier Worthy", "Kansas City Chiefs", False),
    ("92-21", "Ashton Jeanty", "Las Vegas Raiders", R),
    ("92-22", "Omarion Hampton", "Los Angeles Chargers", R),
    ("92-23", "Jared Verse", "Los Angeles Rams", False),
    ("92-24", "Kyren Williams", "Los Angeles Rams", False),
    ("92-25", "De'Von Achane", "Miami Dolphins", False),
    ("92-26", "J.J. McCarthy", "Minnesota Vikings", False),
    ("92-27", "Drake Maye", "New England Patriots", False),
    ("92-28", "TreVeyon Henderson", "New England Patriots", R),
    ("92-29", "Chris Olave", "New Orleans Saints", False),
    ("92-30", "Jaxson Dart", "New York Giants", R),
    ("92-31", "Sauce Gardner", "Indianapolis Colts", False),
    ("92-32", "A.J. Brown", "Philadelphia Eagles", False),
    ("92-33", "Cooper DeJean", "Philadelphia Eagles", False),
    ("92-34", "Cameron Heyward", "Pittsburgh Steelers", False),
    ("92-35", "Brock Purdy", "San Francisco 49ers", False),
    ("92-36", "Brandon Aiyuk", "San Francisco 49ers", False),
    ("92-37", "Jalen Milroe", "Seattle Seahawks", R),
    ("92-38", "Kenneth Walker III", "Seattle Seahawks", False),
    ("92-39", "Chris Godwin Jr.", "Tampa Bay Buccaneers", False),
    ("92-40", "Emeka Egbuka", "Tampa Bay Buccaneers", R),
    ("92-41", "Cam Ward", "Tennessee Titans", R),
    ("92-42", "Tony Pollard", "Tennessee Titans", False),
    ("92-43", "Terry McLaurin", "Washington Commanders", False),
    ("92-44", "Jayden Daniels", "Washington Commanders", False),
])

# Headliners (H-1 to H-15)
add_insert_subset("Headliners", [
    ("H-1", "Josh Allen", "Buffalo Bills", False),
    ("H-2", "Joe Burrow", "Cincinnati Bengals", False),
    ("H-3", "Jordan Love", "Green Bay Packers", False),
    ("H-4", "Patrick Mahomes II", "Kansas City Chiefs", False),
    ("H-5", "Tom Brady", "New England Patriots", False),
    ("H-6", "Jaxson Dart", "New York Giants", R),
    ("H-7", "Cam Ward", "Tennessee Titans", R),
    ("H-8", "Derrick Henry", "Baltimore Ravens", False),
    ("H-9", "Ashton Jeanty", "Las Vegas Raiders", R),
    ("H-10", "Cam Skattebo", "New York Giants", R),
    ("H-11", "Saquon Barkley", "Philadelphia Eagles", False),
    ("H-12", "CeeDee Lamb", "Dallas Cowboys", False),
    ("H-13", "Amon-Ra St. Brown", "Detroit Lions", False),
    ("H-14", "Justin Jefferson", "Minnesota Vikings", False),
    ("H-15", "George Kittle", "San Francisco 49ers", False),
])

# Team Finest (TF-1 to TF-10)
add_insert_subset("Team Finest", [
    ("TF-1", "Josh Allen", "Buffalo Bills", False),
    ("TF-2", "Joe Burrow", "Cincinnati Bengals", False),
    ("TF-3", "Patrick Mahomes II", "Kansas City Chiefs", False),
    ("TF-4", "Derrick Henry", "Baltimore Ravens", False),
    ("TF-5", "Saquon Barkley", "Philadelphia Eagles", False),
    ("TF-6", "Ja'Marr Chase", "Cincinnati Bengals", False),
    ("TF-7", "CeeDee Lamb", "Dallas Cowboys", False),
    ("TF-8", "Justin Jefferson", "Minnesota Vikings", False),
    ("TF-9", "Brock Bowers", "Las Vegas Raiders", False),
    ("TF-10", "Micah Parsons", "Green Bay Packers", False),
])


# ─── AUTOGRAPH SUBSETS ──────────────────────────────────────────────────────
def add_auto_subset(name, cards):
    is_id = add_is(name)
    for n, pr in auto_parallels:
        add_par(is_id, n, pr)
    add_cards(is_id, cards)
    print(f"  {name}: {len(cards)} cards")
    return is_id


# Finest Autographs (FA-XX) — 39 cards
add_auto_subset("Finest Autographs", [
    ("FA-AJS", "Aaron Jones Sr.", "Minnesota Vikings", False),
    ("FA-AR", "Anthony Richardson", "Indianapolis Colts", False),
    ("FA-ASB", "Amon-Ra St. Brown", "Detroit Lions", False),
    ("FA-BB", "Brock Bowers", "Las Vegas Raiders", False),
    ("FA-BC", "Blake Corum", "Los Angeles Rams", False),
    ("FA-BI", "Bucky Irving", "Tampa Bay Buccaneers", False),
    ("FA-BN", "Bo Nix", "Denver Broncos", False),
    ("FA-BY", "Bryce Young", "Carolina Panthers", False),
    ("FA-CB", "Chase Brown", "Cincinnati Bengals", False),
    ("FA-CD", "CeeDee Lamb", "Dallas Cowboys", False),
    ("FA-CDJ", "Cooper DeJean", "Philadelphia Eagles", False),
    ("FA-CJS", "CJ Stroud", "Houston Texans", False),
    ("FA-CO", "Chris Olave", "New Orleans Saints", False),
    ("FA-CW", "Caleb Williams", "Chicago Bears", False),
    ("FA-DA", "De'Von Achane", "Miami Dolphins", False),
    ("FA-DL", "Drake London", "Atlanta Falcons", False),
    ("FA-DM", "Drake Maye", "New England Patriots", False),
    ("FA-DN", "David Njoku", "Cleveland Browns", False),
    ("FA-JB", "Joey Bosa", "Buffalo Bills", False),
    ("FA-JD", "Jayden Daniels", "Washington Commanders", False),
    ("FA-JH", "Justin Herbert", "Los Angeles Chargers", False),
    ("FA-JL", "Jordan Love", "Green Bay Packers", False),
    ("FA-JSN", "Jaxon Smith-Njigba", "Seattle Seahawks", False),
    ("FA-JT", "Jonathan Taylor", "Indianapolis Colts", False),
    ("FA-KC", "Keon Coleman", "Buffalo Bills", False),
    ("FA-KH", "Kyle Hamilton", "Baltimore Ravens", False),
    ("FA-MHJ", "Marvin Harrison Jr.", "Arizona Cardinals", False),
    ("FA-MN", "Malik Nabers", "New York Giants", False),
    ("FA-PN", "Puka Nacua", "Los Angeles Rams", False),
    ("FA-PS", "Pat Surtain II", "Denver Broncos", False),
    ("FA-QW", "Quinnen Williams", "New York Jets", False),
    ("FA-RP", "Ricky Pearsall", "San Francisco 49ers", False),
    ("FA-SL", "Sam LaPorta", "Detroit Lions", False),
    ("FA-TBR", "Tom Brady", "New England Patriots", False),
    ("FA-TH", "Trey Hendrickson", "Cincinnati Bengals", False),
    ("FA-TMC", "Trey McBride", "Arizona Cardinals", False),
    ("FA-TS", "T'Vondre Sweat", "Tennessee Titans", False),
    ("FA-XW", "Xavier Worthy", "Kansas City Chiefs", False),
    ("FA-ZC", "Zach Charbonnet", "Seattle Seahawks", False),
])

# Rookie Finest Autographs (RFA-XX) — 51 cards
add_auto_subset("Rookie Finest Autographs", [
    ("RFA-AC", "Abdul Carter", "New York Giants", R),
    ("RFA-AJ", "Ashton Jeanty", "Las Vegas Raiders", R),
    ("RFA-BM", "Benjamin Morrison", "Tampa Bay Buccaneers", R),
    ("RFA-CL", "Colston Loveland", "Chicago Bears", R),
    ("RFA-CS", "Cam Skattebo", "New York Giants", R),
    ("RFA-CW", "Cam Ward", "Tennessee Titans", R),
    ("RFA-DG", "Dillon Gabriel", "Cleveland Browns", R),
    ("RFA-EA", "Elic Ayomanor", "Tennessee Titans", R),
    ("RFA-EAR", "Elijah Arroyo", "Seattle Seahawks", R),
    ("RFA-EE", "Emeka Egbuka", "Tampa Bay Buccaneers", R),
    ("RFA-IT", "Isaac TeSlaa", "Detroit Lions", R),
    ("RFA-JBE", "Jack Bech", "Las Vegas Raiders", R),
    ("RFA-JBL", "Jaydon Blue", "Dallas Cowboys", R),
    ("RFA-JC", "Jihaad Campbell", "Philadelphia Eagles", R),
    ("RFA-JD", "Jaxson Dart", "New York Giants", R),
    ("RFA-JHI", "Jayden Higgins", "Houston Texans", R),
    ("RFA-JL", "Jaylin Lane", "Washington Commanders", R),
    ("RFA-JN", "Jaylin Noel", "Houston Texans", R),
    ("RFA-JR", "Jalen Royals", "Kansas City Chiefs", R),
    ("RFA-JW", "Jalon Walker", "Atlanta Falcons", R),
    ("RFA-KJ", "Kaleb Johnson", "Pittsburgh Steelers", R),
    ("RFA-KM", "Kyle McCord", "Philadelphia Eagles", R),
    ("RFA-KW", "Kyle Williams", "New England Patriots", R),
    ("RFA-LB", "Luther Burden III", "Chicago Bears", R),
    ("RFA-MG", "Mason Graham", "Cleveland Browns", R),
    ("RFA-MGO", "Matthew Golden", "Green Bay Packers", R),
    ("RFA-MH", "Maxwell Hairston", "Buffalo Bills", R),
    ("RFA-MS", "Malaki Starks", "Baltimore Ravens", R),
    ("RFA-MT", "Mason Taylor", "New York Jets", R),
    ("RFA-MW", "Mykel Williams", "San Francisco 49ers", R),
    ("RFA-OH", "Omarion Hampton", "Los Angeles Chargers", R),
    ("RFA-PB", "Pat Bryant", "Denver Broncos", R),
    ("RFA-QJ", "Quinshon Judkins", "Cleveland Browns", R),
    ("RFA-RJH", "RJ Harvey", "Denver Broncos", R),
    ("RFA-RL", "Riley Leonard", "Indianapolis Colts", R),
    ("RFA-SRJ", "Shavon Revel Jr.", "Dallas Cowboys", R),
    ("RFA-SS", "Shedeur Sanders", "Cleveland Browns", R),
    ("RFA-SST", "Shemar Stewart", "Cincinnati Bengals", R),
    ("RFA-SW", "Savion Williams", "Green Bay Packers", R),
    ("RFA-TE", "Trevor Etienne", "Carolina Panthers", R),
    ("RFA-TF", "Terrance Ferguson", "Los Angeles Rams", R),
    ("RFA-TFE", "Tai Felton", "Minnesota Vikings", R),
    ("RFA-TH", "Tre Harris III", "Los Angeles Chargers", R),
    ("RFA-THU", "Travis Hunter", "Jacksonville Jaguars", R),
    ("RFA-TM", "Tetairoa McMillan", "Carolina Panthers", R),
    ("RFA-TS", "Tyler Shough", "New Orleans Saints", R),
    ("RFA-TVH", "TreVeyon Henderson", "New England Patriots", R),
    ("RFA-TW", "Tyleik Williams", "Detroit Lions", R),
    ("RFA-TWA", "Tyler Warren", "Indianapolis Colts", R),
    ("RFA-TZJ", "Tez Johnson", "Tampa Bay Buccaneers", R),
    ("RFA-WH", "Will Howard", "Pittsburgh Steelers", R),
    ("RFA-WJ", "Will Johnson", "Arizona Cardinals", R),
])

# Flashback Autographs (FBA-XX) — 38 cards
add_auto_subset("Flashback Autographs", [
    ("FBA-AJ", "Ashton Jeanty", "Las Vegas Raiders", R),
    ("FBA-AJS", "Aaron Jones Sr.", "Minnesota Vikings", False),
    ("FBA-BB", "Brock Bowers", "Las Vegas Raiders", False),
    ("FBA-BN", "Bo Nix", "Denver Broncos", False),
    ("FBA-BY", "Bryce Young", "Carolina Panthers", False),
    ("FBA-CB", "Chase Brown", "Cincinnati Bengals", False),
    ("FBA-CDL", "CeeDee Lamb", "Dallas Cowboys", False),
    ("FBA-CMC", "Christian McCaffrey", "San Francisco 49ers", False),
    ("FBA-CS", "Courtland Sutton", "Denver Broncos", False),
    ("FBA-CW", "Cam Ward", "Tennessee Titans", R),
    ("FBA-DH", "Derrick Henry", "Baltimore Ravens", False),
    ("FBA-EE", "Emeka Egbuka", "Tampa Bay Buccaneers", R),
    ("FBA-IP", "Rashee Rice", "Kansas City Chiefs", False),
    ("FBA-JA", "Jordan Addison", "Minnesota Vikings", False),
    ("FBA-JD", "Jayden Daniels", "Washington Commanders", False),
    ("FBA-JG", "Jahmyr Gibbs", "Detroit Lions", False),
    ("FBA-JH", "Jalen Hurts", "Philadelphia Eagles", False),
    ("FBA-JJ", "Jerry Jeudy", "Cleveland Browns", False),
    ("FBA-JV", "Jared Verse", "Los Angeles Rams", False),
    ("FBA-JXD", "Jaxson Dart", "New York Giants", R),
    ("FBA-KW", "Kyren Williams", "Los Angeles Rams", False),
    ("FBA-LBU", "Luther Burden III", "Chicago Bears", R),
    ("FBA-LM", "Ladd McConkey", "Los Angeles Chargers", False),
    ("FBA-MG", "Myles Garrett", "Cleveland Browns", False),
    ("FBA-MHJ", "Marvin Harrison Jr.", "Arizona Cardinals", False),
    ("FBA-MT", "Mason Taylor", "New York Jets", R),
    ("FBA-NB", "Nick Bosa", "San Francisco 49ers", False),
    ("FBA-NC", "Nico Collins", "Houston Texans", False),
    ("FBA-NW", "Nate Wiggins", "Baltimore Ravens", False),
    ("FBA-OH", "Omarion Hampton", "Los Angeles Chargers", R),
    ("FBA-RS", "Rashid Shaheed", "New Orleans Saints", False),
    ("FBA-SD", "Sam Darnold", "Seattle Seahawks", False),
    ("FBA-TB", "Trey Benson", "Arizona Cardinals", False),
    ("FBA-TEJ", "Travis Etienne Jr.", "Jacksonville Jaguars", False),
    ("FBA-TT", "Tua Tagovailoa", "Miami Dolphins", False),
    ("FBA-TVH", "TreVeyon Henderson", "New England Patriots", R),
    ("FBA-TW", "Tyler Warren", "Indianapolis Colts", R),
    ("FBA-XW", "Xavier Worthy", "Kansas City Chiefs", False),
])

# Finest Freshman Autographs (FFA-XX) — 10 cards
add_auto_subset("Finest Freshman Autographs", [
    ("FFA-AJ", "Ashton Jeanty", "Las Vegas Raiders", R),
    ("FFA-CS", "Cam Skattebo", "New York Giants", R),
    ("FFA-CW", "Cam Ward", "Tennessee Titans", R),
    ("FFA-EE", "Emeka Egbuka", "Tampa Bay Buccaneers", R),
    ("FFA-JD", "Jaxson Dart", "New York Giants", R),
    ("FFA-LB", "Luther Burden III", "Chicago Bears", R),
    ("FFA-MG", "Matthew Golden", "Green Bay Packers", R),
    ("FFA-OH", "Omarion Hampton", "Los Angeles Chargers", R),
    ("FFA-TH", "TreVeyon Henderson", "New England Patriots", R),
    ("FFA-TW", "Tyler Warren", "Indianapolis Colts", R),
])

# Finest Greats Autographs (FGA-XX) — 35 cards
# Historical team names preserved verbatim
add_auto_subset("Finest Greats Autographs", [
    ("FGA-AF", "Arian Foster", "Houston Texans", False),
    ("FGA-AM", "Archie Manning", "New Orleans Saints", False),
    ("FGA-BE", "Boomer Esiason", "Cincinnati Bengals", False),
    ("FGA-CB", "Champ Bailey", "Denver Broncos", False),
    ("FGA-CO", "Christian Okoye", "Kansas City Chiefs", False),
    ("FGA-CT", "Charles Tillman", "Chicago Bears", False),
    ("FGA-CW", "Charles Woodson", "Green Bay Packers", False),
    ("FGA-DF", "Dwight Freeney", "Indianapolis Colts", False),
    ("FGA-DR", "Darrelle Revis", "New York Jets", False),
    ("FGA-DS", "Darren Sproles", "San Diego Chargers", False),
    ("FGA-ED", "Eric Dickerson", "Los Angeles Rams", False),
    ("FGA-EM", "Eli Manning", "New York Giants", False),
    ("FGA-EW", "Eric Weddle", "Baltimore Ravens", False),
    ("FGA-HL", "Howie Long", "Oakland Raiders", False),
    ("FGA-HW", "Hines Ward", "Pittsburgh Steelers", False),
    ("FGA-JIK", "Jim Kelly", "Buffalo Bills", False),
    ("FGA-JJ", "Julio Jones", "Atlanta Falcons", False),
    ("FGA-JP", "Julius Peppers", "Carolina Panthers", False),
    ("FGA-JR", "Jerry Rice", "San Francisco 49ers", False),
    ("FGA-JTA", "Jason Taylor", "Miami Dolphins", False),
    ("FGA-JTU", "Justin Tuck", "New York Giants", False),
    ("FGA-JVK", "Jevon Kearse", "Tennessee Titans", False),
    ("FGA-JW", "Jason Witten", "Dallas Cowboys", False),
    ("FGA-KC", "Kam Chancellor", "Seattle Seahawks", False),
    ("FGA-KJ", "Keyshawn Johnson", "New York Jets", False),
    ("FGA-KW", "Kellen Winslow", "San Diego Chargers", False),
    ("FGA-LK", "Luke Kuechly", "Carolina Panthers", False),
    ("FGA-MA", "Mike Alstott", "Tampa Bay Buccaneers", False),
    ("FGA-MJD", "Maurice Jones-Drew", "Jacksonville Jaguars", False),
    ("FGA-RC", "Randall Cunningham", "Minnesota Vikings", False),
    ("FGA-RW", "Ricky Williams", "Miami Dolphins", False),
    ("FGA-SM", "Santana Moss", "Washington Redskins", False),
    ("FGA-TA", "Troy Aikman", "Dallas Cowboys", False),
    ("FGA-TBR", "Tedy Bruschi", "New England Patriots", False),
    ("FGA-VD", "Vernon Davis", "San Francisco 49ers", False),
])

# Finest Moments Autographs (FMA-XX) — 26 cards
add_auto_subset("Finest Moments Autographs", [
    ("FMA-BB", "Brock Bowers", "Las Vegas Raiders", False),
    ("FMA-BJ", "Bo Jackson", "Los Angeles Raiders", False),
    ("FMA-BN", "Bo Nix", "Denver Broncos", False),
    ("FMA-BP", "Brock Purdy", "San Francisco 49ers", False),
    ("FMA-CJS", "CJ Stroud", "Houston Texans", False),
    ("FMA-CW", "Caleb Williams", "Chicago Bears", False),
    ("FMA-DH", "Devin Hester", "Chicago Bears", False),
    ("FMA-DM", "Drake Maye", "New England Patriots", False),
    ("FMA-DP", "Dak Prescott", "Dallas Cowboys", False),
    ("FMA-ER", "Ed Reed", "Baltimore Ravens", False),
    ("FMA-JA", "Josh Allen", "Buffalo Bills", False),
    ("FMA-JB", "Joe Burrow", "Cincinnati Bengals", False),
    ("FMA-JD", "Jayden Daniels", "Washington Commanders", False),
    ("FMA-JG", "Jared Goff", "Detroit Lions", False),
    ("FMA-JH", "James Harrison", "Pittsburgh Steelers", False),
    ("FMA-LB", "LeRoy Butler", "Green Bay Packers", False),
    ("FMA-ML", "Marshawn Lynch", "Seattle Seahawks", False),
    ("FMA-MM", "Mario Manningham", "New York Giants", False),
    ("FMA-NF", "Nick Foles", "Philadelphia Eagles", False),
    ("FMA-PM", "Peyton Manning", "Indianapolis Colts", False),
    ("FMA-RG", "Rob Gronkowski", "Tampa Bay Buccaneers", False),
    ("FMA-RM", "Randy Moss", "Minnesota Vikings", False),
    ("FMA-SB", "Saquon Barkley", "Philadelphia Eagles", False),
    ("FMA-TH", "Taysom Hill", "New Orleans Saints", False),
    ("FMA-TJW", "T.J. Watt", "Pittsburgh Steelers", False),
    ("FMA-VD", "Vernon Davis", "San Francisco 49ers", False),
])

# Finest Fans Autographs (FAN-XX) — 9 cards (celebrity fans)
# These are added as regular players in the athletes table per project convention
fans_id = add_is("Finest Fans Autographs")
for n, pr in auto_parallels:
    add_par(fans_id, n, pr)
fan_cards = [
    ("FAN-AH", "Anne Hathaway", "Philadelphia Eagles", False),
    ("FAN-BS", "Brenda Song", "Los Angeles Rams", False),
    ("FAN-DJK", "DJ Khaled", "Miami Dolphins", False),
    ("FAN-DW", "Dwyane Wade", "Chicago Bears", False),
    ("FAN-KD", "Kevin Durant", "Washington Commanders", False),
    ("FAN-MG", "Mike Greenberg", "New York Jets", False),
    ("FAN-MT", "Mike Trout", "Philadelphia Eagles", False),
    ("FAN-RL", "Rob Lowe", "Indianapolis Colts", False),
    ("FAN-SC", "Stephen Curry", "Carolina Panthers", False),
]
add_cards(fans_id, fan_cards)
print(f"  Finest Fans Autographs: {len(fan_cards)} cards (celebrity fans)")


# ─── Summary ────────────────────────────────────────────────────────────────
db.commit()

total_players = db.execute("SELECT COUNT(*) FROM players WHERE set_id = ?", (SET_ID,)).fetchone()[0]
total_appearances = db.execute("""
    SELECT COUNT(*) FROM player_appearances pa
    JOIN insert_sets ins ON pa.insert_set_id = ins.id
    WHERE ins.set_id = ?
""", (SET_ID,)).fetchone()[0]
total_insert_sets = db.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id = ?", (SET_ID,)).fetchone()[0]
total_parallels = db.execute("""
    SELECT COUNT(*) FROM parallels p
    JOIN insert_sets ins ON p.insert_set_id = ins.id
    WHERE ins.set_id = ?
""", (SET_ID,)).fetchone()[0]

print(f"\n{'='*50}")
print(f"Set ID: {SET_ID}")
print(f"Total insert sets (subsets): {total_insert_sets}")
print(f"Total unique players: {total_players}")
print(f"Total card appearances: {total_appearances}")
print(f"Total parallels: {total_parallels}")
print(f"Expected: ~787 card appearances (300 base + 279 inserts + 208 autos)")
db.close()
print("Done!")
