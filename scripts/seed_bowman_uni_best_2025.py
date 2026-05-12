"""
Seed: 2025-26 Bowman University Best Basketball — Full checklist.
100 base, 6 insert subsets, 6 auto subsets, 4 auto-relic subsets, parallels.
Usage: python3 scripts/seed_bowman_uni_best_2025.py
"""
import sqlite3, os, json, re

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
db = sqlite3.connect(DB_PATH)
db.execute("PRAGMA journal_mode=WAL")
db.execute("PRAGMA foreign_keys=ON")

# ─── Create Set ──────────────────────────────────────────────────────────────
box_config = json.dumps({
    "hobby": {
        "cards_per_pack": 10,
        "packs_per_box": 4,
        "boxes_per_case": 12,
        "notes": "Per box: 4 autographs + 1 patch autograph"
    }
})

db.execute("""
    INSERT INTO sets (name, sport, season, tier, slug, is_visible,
                      sample_image_url, release_date, box_config)
    VALUES ('2025-26 Bowman University Best Basketball', 'Basketball', '2025-26', 'Standard',
            '2025-26-bowman-university-best-basketball', 1,
            '/sets/2025-26-bowman-university-best-basketball.jpg', '2026-05-15', ?)
""", (box_config,))
SET_ID = db.execute("SELECT last_insert_rowid()").fetchone()[0]
print(f"Created set ID: {SET_ID}")

H = "Hobby"

def get_or_create(name, role="athlete"):
    row = db.execute("SELECT id FROM players WHERE set_id = ? AND name = ?", (SET_ID, name)).fetchone()
    if row: return row[0]
    db.execute("INSERT INTO players (set_id, name, unique_cards, total_print_run, one_of_ones, insert_set_count, subject_role) VALUES (?, ?, 0, 0, 0, 0, ?)", (SET_ID, name, role))
    return db.execute("SELECT last_insert_rowid()").fetchone()[0]

def add_is(name):
    db.execute("INSERT INTO insert_sets (set_id, name) VALUES (?, ?)", (SET_ID, name))
    return db.execute("SELECT last_insert_rowid()").fetchone()[0]

def add_par(is_id, name, print_run=None, excl=H):
    db.execute("INSERT INTO parallels (insert_set_id, name, print_run, exclusivity) VALUES (?, ?, ?, ?)", (is_id, name, print_run, excl))

def add_pars(is_id, pars):
    for name, pr, excl in pars:
        add_par(is_id, name, pr, excl)
    return len(pars)

def add_cards(is_id, cards, role="athlete"):
    """cards = list of (card_num, name, team)"""
    for num, name, team in cards:
        pid = get_or_create(name, role)
        db.execute(
            "INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, ?)",
            (pid, is_id, str(num), team)
        )

def add_dual_cards(is_id, cards):
    """cards = list of (card_num, name1, name2)"""
    for num, n1, n2 in cards:
        pid1 = get_or_create(n1)
        pid2 = get_or_create(n2)
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, NULL)", (pid1, is_id, str(num)))
        a_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a_id, pid2))

def add_triple_cards(is_id, cards):
    """cards = list of (card_num, name1, name2, name3)"""
    for num, n1, n2, n3 in cards:
        pid1 = get_or_create(n1)
        pid2 = get_or_create(n2)
        pid3 = get_or_create(n3)
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, NULL)", (pid1, is_id, str(num)))
        a_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a_id, pid2))
        db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a_id, pid3))


# ─── BASE SET (100 cards) ───────────────────────────────────────────────────
base_id = add_is("Base Set")

base_pars = [
    ("Base", None, H), ("Base-Refractor", None, H), ("Base-Shimmer", None, H),
    ("Base-Purple", 250, H), ("Base-Aqua Lava", 199, H), ("Base-Blue", 150, H),
    ("Base-Green Mini Diamond", 99, H), ("Base-Yellow Lazer", 75, H),
    ("Base-Gold", 50, H), ("Base-Pearl", 35, H), ("Base-Orange Mini-Diamond", 25, H),
    ("Base-Teal", 15, H), ("Base-Black", 10, H), ("Base-Red", 5, H),
    ("Base-SuperFractor", 1, H),
]
add_pars(base_id, base_pars)

base_cards = [
    (1, "Braden Smith", "Purdue"),
    (2, "Obi Agbim", "Baylor"),
    (3, "Ryan Conwell", "Louisville"),
    (4, "Kam Williams", "Kentucky"),
    (5, "Malik Reneau", "Miami"),
    (6, "Tre Donaldson", "Miami"),
    (7, "Robert McCray V", "Florida State"),
    (8, "Tylis Jordan", "Ole Miss"),
    (9, "AJ Dybantsa", "BYU"),
    (10, "Darryn Peterson", "Kansas"),
    (11, "Koa Peat", "Arizona"),
    (12, "Kiyan Anthony", "Syracuse"),
    (13, "Nate Ament", "Tennessee"),
    (14, "Jasper Johnson", "Kentucky"),
    (15, "Isiah Harwell", "Houston"),
    (16, "Bryson Tiller", "Kansas"),
    (17, "Dwayne Aristode", "Arizona"),
    (18, "Shelton Henderson", "Miami"),
    (19, "Tounde Yessoufou", "Baylor"),
    (20, "Mikel Brown Jr.", "Louisville"),
    (21, "Sienna Betts", "UCLA"),
    (22, "Acaden Lewis", "Villanova"),
    (23, "Madison Booker", "Texas"),
    (24, "Jason Edwards", "Providence"),
    (25, "Josh Dix", "Creighton"),
    (26, "Niko Bundalo", "Ole Miss"),
    (27, "Shon Abaev", "Cincinnati"),
    (28, "Silas Demary Jr.", "UConn"),
    (29, "Trey Kaufman-Renn", "Purdue"),
    (30, "Zuby Ejiofor", "St. John's"),
    (31, "Jaland Lowe", "Kentucky"),
    (32, "Joe Grahovac", "St. Bonaventure"),
    (33, "Kiyomi McMiller", "Penn State"),
    (34, "Michael Rataj", "Baylor"),
    (35, "Reed Bailey", "Indiana"),
    (36, "Xaivian Lee", "Florida"),
    (37, "Braeden Shrewsberry", "Notre Dame"),
    (38, "Cotie McMahon", "Ole Miss"),
    (39, "Serah Williams", "UConn"),
    (40, "Owen Freeman", "Creighton"),
    (41, "Aaliyah Crump", "Texas"),
    (42, "Agot Makeer", "South Carolina"),
    (43, "Coen Carr", "Michigan State"),
    (44, "Darrion Williams", "NC State"),
    (45, "Derek Dixon", "UNC"),
    (46, "Hailee Swain", "Stanford"),
    (47, "Kaylene Smikle", "Maryland"),
    (48, "Milos Uzan", "Houston"),
    (49, "Sadiq White Jr.", "Syracuse"),
    (50, "Tarris Reed Jr.", "UConn"),
    (51, "Wesley Yates III", "Washington Huskies"),
    (52, "Lara Somfai", "Stanford"),
    (53, "Christian Anderson", "Texas Tech"),
    (54, "Davion Hannah", "Alabama"),
    (55, "Davis Fogle", "Gonzaga"),
    (56, "Grace Knox", "LSU"),
    (57, "Isaiah Denis", "UNC"),
    (58, "Addison Deal", "Iowa"),
    (59, "Brayden Burries", "Arizona"),
    (60, "Bryce Lindsay", "Villanova"),
    (61, "Cam Ward", "Michigan State"),
    (62, "Kohl Rosario", "Kansas"),
    (63, "Deniya Prawl", "Tennessee"),
    (64, "Devin McGlockton", "Vanderbilt"),
    (65, "Donald Hand Jr.", "Boston College"),
    (66, "Juju Watkins", "USC"),
    (67, "Jamier Jones", "Providence"),
    (68, "Keyshawn Hall", "Auburn"),
    (69, "Cameron Boozer", "Duke"),
    (70, "Nick Martinelli", "Northwestern"),
    (71, "Nyla Brooks", "UNC"),
    (72, "Pharrel Payne", "Maryland"),
    (73, "Raegan Beers", "Oklahoma"),
    (74, "Richie Saunders", "BYU"),
    (75, "Winters Grady", "Michigan"),
    (76, "Yarden Garzon", "Maryland"),
    (77, "Darianna Alexander", "Cincinnati"),
    (78, "Jeremiah Wilkinson", "Georgia"),
    (79, "Kara Dunn", "USC"),
    (80, "Boopie Miller", "SMU"),
    (81, "ZaKiyah Johnson", "LSU"),
    (82, "Jaida Civil", "Tennessee"),
    (83, "Alexandra Eschmeyer", "Stanford"),
    (84, "Aliyahna Morris", "California"),
    (85, "Otega Oweh", "Kentucky"),
    (86, "John Blackwell", "Wisconsin"),
    (87, "Tobe Awaka", "Arizona"),
    (88, "Sarah Strong", "UConn"),
    (89, "Tre Holloman", "NC State"),
    (90, "Kaelyn Carroll", "Kentucky"),
    (91, "Caleb Wilson", "UNC"),
    (92, "Ayla McDowell", "South Carolina"),
    (93, "Emilee Skinner", "Duke"),
    (94, "Ta'Niya Latson", "South Carolina"),
    (95, "Oziyah Sellers", "St. John's"),
    (96, "Nate Bittle", "Oregon"),
    (97, "Cayden Boozer", "Duke"),
    (98, "Bennett Stirtz", "Iowa"),
    (99, "JT Toppin", "Texas Tech"),
    (100, "Nate Calmese", "Wake Forest"),
]
add_cards(base_id, base_cards)
print(f"  Base Set: {len(base_cards)} cards, {len(base_pars)} parallels")

# ─── INSERT SUBSETS ─────────────────────────────────────────────────────────
insert_pars = [
    ("Base", None, H), ("Refractor", None, H), ("Shimmer", None, H),
    ("Green Mini Diamond", 99, H), ("Yellow Lazer", 75, H),
    ("Gold", 50, H), ("Orange Mini-Diamond", 25, H),
    ("Black", 10, H), ("Red", 5, H), ("SuperFractor", 1, H),
]

case_hit_pars = [("SuperFractor", 1, H)]

def add_insert(name, cards, is_case_hit=False):
    is_id = add_is(name)
    pars = case_hit_pars if is_case_hit else insert_pars
    add_pars(is_id, pars)
    add_cards(is_id, cards)
    print(f"  {name}: {len(cards)} cards, {len(pars)} parallels" + (" [SSP]" if is_case_hit else ""))

# Tone Setters (TS-1 to TS-40)
add_insert("Tone Setters", [
    ("TS-1", "AJ Dybantsa", "BYU"), ("TS-2", "Darryn Peterson", "Kansas"),
    ("TS-3", "Koa Peat", "Arizona"), ("TS-4", "Kiyan Anthony", "Syracuse"),
    ("TS-5", "Nate Ament", "Tennessee"), ("TS-6", "Jasper Johnson", "Kentucky"),
    ("TS-7", "Isiah Harwell", "Houston"), ("TS-8", "Bryson Tiller", "Kansas"),
    ("TS-9", "Dwayne Aristode", "Arizona"), ("TS-10", "Shelton Henderson", "Miami"),
    ("TS-11", "Tounde Yessoufou", "Baylor"), ("TS-12", "Mikel Brown Jr.", "Louisville"),
    ("TS-13", "Sienna Betts", "UCLA"), ("TS-14", "Acaden Lewis", "Villanova"),
    ("TS-15", "Madison Booker", "Texas"), ("TS-16", "Raegan Beers", "Oklahoma"),
    ("TS-17", "Richie Saunders", "BYU"), ("TS-18", "Braden Smith", "Purdue"),
    ("TS-19", "Kohl Rosario", "Kansas"), ("TS-20", "Ja'Kobi Gillespie", "Tennessee"),
    ("TS-21", "Brandon Garrison", "Kentucky"), ("TS-22", "Otega Oweh", "Kentucky"),
    ("TS-23", "Christian Anderson", "Texas Tech"), ("TS-24", "Davion Hannah", "Alabama"),
    ("TS-25", "Davis Fogle", "Gonzaga"), ("TS-26", "Grace Knox", "LSU"),
    ("TS-27", "Isaiah Denis", "UNC"), ("TS-28", "Addison Deal", "Iowa"),
    ("TS-29", "Brayden Burries", "Arizona"), ("TS-30", "Caleb Wilson", "UNC"),
    ("TS-31", "Cam Ward", "Michigan State"), ("TS-32", "Sarah Strong", "UConn"),
    ("TS-33", "Bennett Stirtz", "Iowa"), ("TS-34", "JT Toppin", "Texas Tech"),
    ("TS-35", "Milos Uzan", "Houston"), ("TS-36", "Trey Kaufman-Renn", "Purdue"),
    ("TS-37", "Keyshawn Hall", "Auburn"), ("TS-38", "John Blackwell", "Wisconsin"),
    ("TS-39", "Xaivian Lee", "Florida"), ("TS-40", "Juju Watkins", "USC"),
])

# Bowman Masterpieces (BM-1 to BM-40)
add_insert("Bowman Masterpieces", [
    ("BM-1", "Juju Watkins", "USC"), ("BM-2", "AJ Dybantsa", "BYU"),
    ("BM-3", "Darryn Peterson", "Kansas"), ("BM-4", "Koa Peat", "Arizona"),
    ("BM-5", "Kiyan Anthony", "Syracuse"), ("BM-6", "Nate Ament", "Tennessee"),
    ("BM-7", "Jasper Johnson", "Kentucky"), ("BM-8", "Isiah Harwell", "Houston"),
    ("BM-9", "Bryson Tiller", "Kansas"), ("BM-10", "Dwayne Aristode", "Arizona"),
    ("BM-11", "Shelton Henderson", "Miami"), ("BM-12", "Tounde Yessoufou", "Baylor"),
    ("BM-13", "Mikel Brown Jr.", "Louisville"), ("BM-14", "Sienna Betts", "UCLA"),
    ("BM-15", "Acaden Lewis", "Villanova"), ("BM-16", "Madison Booker", "Texas"),
    ("BM-17", "Raegan Beers", "Oklahoma"), ("BM-18", "Leah Macy", "Notre Dame"),
    ("BM-19", "Nick Martinelli", "Northwestern"), ("BM-20", "Nyla Brooks", "UNC"),
    ("BM-21", "Caleb Wilson", "UNC"), ("BM-22", "Emilee Skinner", "Duke"),
    ("BM-23", "Ta'Niya Latson", "South Carolina"), ("BM-24", "Kiyomi McMiller", "Penn State"),
    ("BM-25", "Cotie McMahon", "Ole Miss"), ("BM-26", "Serah Williams", "UConn"),
    ("BM-27", "Shon Abaev", "Cincinnati"), ("BM-28", "Silas Demary Jr.", "UConn"),
    ("BM-29", "Trey Kaufman-Renn", "Purdue"), ("BM-30", "Zuby Ejiofor", "St. John's"),
    ("BM-31", "Jaland Lowe", "Kentucky"), ("BM-32", "Joe Grahovac", "St. Bonaventure"),
    ("BM-33", "Aaliyah Crump", "Texas"), ("BM-34", "Agot Makeer", "South Carolina"),
    ("BM-35", "Coen Carr", "Michigan State"), ("BM-36", "Darrion Williams", "NC State"),
    ("BM-37", "Derek Dixon", "UNC"), ("BM-38", "Hailee Swain", "Stanford"),
    ("BM-39", "Kaylene Smikle", "Maryland"), ("BM-40", "Milos Uzan", "Houston"),
])

# Breaking Barriers (BB-1 to BB-20)
add_insert("Breaking Barriers", [
    ("BB-1", "Juju Watkins", "USC"), ("BB-2", "Sienna Betts", "UCLA"),
    ("BB-3", "Madison Booker", "Texas"), ("BB-4", "Cotie McMahon", "Ole Miss"),
    ("BB-5", "Serah Williams", "UConn"), ("BB-6", "Agot Makeer", "South Carolina"),
    ("BB-7", "Aaliyah Crump", "Texas"), ("BB-8", "Hailee Swain", "Stanford"),
    ("BB-9", "Kaylene Smikle", "Maryland"), ("BB-10", "Lara Somfai", "Stanford"),
    ("BB-11", "Grace Knox", "LSU"), ("BB-12", "Addison Deal", "Iowa"),
    ("BB-13", "Leah Macy", "Notre Dame"), ("BB-14", "Kara Dunn", "USC"),
    ("BB-15", "Sarah Strong", "UConn"), ("BB-16", "Kiyomi McMiller", "Penn State"),
    ("BB-17", "Aliyahna Morris", "California"), ("BB-18", "Nyla Brooks", "UNC"),
    ("BB-19", "Ayla McDowell", "South Carolina"), ("BB-20", "Emilee Skinner", "Duke"),
])

# Let's Go (LG-1 to LG-5) — Case Hit
add_insert("Let's Go", [
    ("LG-1", "AJ Dybantsa", "BYU"), ("LG-2", "Darryn Peterson", "Kansas"),
    ("LG-3", "Caleb Wilson", "UNC"), ("LG-4", "Mikel Brown Jr.", "Louisville"),
    ("LG-5", "Madison Booker", "Texas"),
], is_case_hit=True)

# Top Billing (TB-1 to TB-10) — Case Hit
add_insert("Top Billing", [
    ("TB-1", "AJ Dybantsa", "BYU"), ("TB-2", "Darryn Peterson", "Kansas"),
    ("TB-3", "Caleb Wilson", "UNC"), ("TB-4", "Mikel Brown Jr.", "Louisville"),
    ("TB-5", "Tounde Yessoufou", "Baylor"), ("TB-6", "Juju Watkins", "USC"),
    ("TB-7", "Koa Peat", "Arizona"), ("TB-8", "Nate Ament", "Tennessee"),
    ("TB-9", "Aaliyah Crump", "Texas"), ("TB-10", "Ta'Niya Latson", "South Carolina"),
], is_case_hit=True)

# Big Energy (BE-1 to BE-20) — Case Hit
add_insert("Big Energy", [
    ("BE-1", "Tarris Reed Jr.", "UConn"), ("BE-2", "Mikel Brown Jr.", "Louisville"),
    ("BE-3", "Madison Booker", "Texas"), ("BE-4", "AJ Dybantsa", "BYU"),
    ("BE-5", "Darryn Peterson", "Kansas"), ("BE-6", "Koa Peat", "Arizona"),
    ("BE-7", "Kiyan Anthony", "Syracuse"), ("BE-8", "Nate Ament", "Tennessee"),
    ("BE-9", "Kiyomi McMiller", "Penn State"), ("BE-10", "ZaKiyah Johnson", "LSU"),
    ("BE-11", "Sarah Strong", "UConn"), ("BE-12", "Juju Watkins", "USC"),
    ("BE-13", "Caleb Wilson", "UNC"), ("BE-14", "Jaida Civil", "Tennessee"),
    ("BE-15", "Braden Smith", "Purdue"), ("BE-16", "Zuby Ejiofor", "St. John's"),
    ("BE-17", "Bennett Stirtz", "Iowa"), ("BE-18", "JT Toppin", "Texas Tech"),
    ("BE-19", "Grace Knox", "LSU"), ("BE-20", "Isiah Harwell", "Houston"),
], is_case_hit=True)


# ─── AUTOGRAPH SUBSETS ──────────────────────────────────────────────────────

# Best of 2025 Autographs parallels (with Base)
ba_pars = [
    ("Base", None, H), ("Refractor", None, H), ("Green Mini Diamond", 99, H),
    ("Yellow Lazer", 75, H), ("Orange Mini-Diamond", 25, H),
    ("Black", 10, H), ("Red", 5, H), ("SuperFractor", 1, H),
]

# Greatness Awaits / Iso Signatures / Coaches Ink parallels (no Base)
ga_pars = [
    ("Refractor", None, H), ("Green Mini Diamond", 99, H),
    ("Yellow Lazer", 75, H), ("Orange Mini-Diamond", 25, H),
    ("Black", 10, H), ("Red", 5, H), ("SuperFractor", 1, H),
]

# Dual/Triple auto parallels
dt_pars = [
    ("Refractor", 25, H), ("Black", 10, H), ("Red", 5, H), ("SuperFractor", 1, H),
]

# Auto-relic parallels
relic_pars = [
    ("Base", None, H), ("Yellow Lazer", 75, H), ("Gold", 50, H),
    ("Orange Mini-Diamond", 25, H), ("Black", 10, H), ("Red", 5, H),
    ("Brand Logo Patch", 2, H), ("Conference Patch", 2, H),
    ("Brand Logo Tag", 2, H), ("Special Patch", 2, H), ("SuperFractor", 1, H),
]

# Best of 2025 Autographs (BA-XX) — 96 cards
ba_id = add_is("Best of 2025 Autographs")
add_pars(ba_id, ba_pars)
ba_cards = [
    ("BA-AC", "Aaliyah Crump", "Texas"), ("BA-AD", "AJ Dybantsa", "BYU"),
    ("BA-AE", "Addison Deal", "Iowa"), ("BA-AL", "Acaden Lewis", "Villanova"),
    ("BA-AM", "Agot Makeer", "South Carolina"), ("BA-AR", "Aliyahna Morris", "California"),
    ("BA-AS", "Alexandra Eschmeyer", "Stanford"), ("BA-AY", "Ayla McDowell", "South Carolina"),
    ("BA-BB", "Brayden Burries", "Arizona"), ("BA-BE", "Boopie Miller", "SMU"),
    ("BA-BL", "Bryce Lindsay", "Villanova"), ("BA-BM", "Brynn McGaughy", "Washington"),
    ("BA-BS", "Braeden Shrewsberry", "Notre Dame"), ("BA-BT", "Bryson Tiller", "Kansas"),
    ("BA-BZ", "Bennett Stirtz", "Iowa"), ("BA-CA", "Christian Anderson", "Texas Tech"),
    ("BA-CC", "Coen Carr", "Michigan State"), ("BA-CI", "CJ Ingram", "Florida"),
    ("BA-CL", "Caleb Wilson", "UNC"), ("BA-CM", "Cotie McMahon", "Ole Miss"),
    ("BA-CR", "Chase Ross", "Marquette"), ("BA-CW", "Cam Ward", "Michigan State"),
    ("BA-DA", "Dwayne Aristode", "Arizona"), ("BA-DD", "Derek Dixon", "UNC"),
    ("BA-DF", "Davis Fogle", "Gonzaga"), ("BA-DH", "Davion Hannah", "Alabama"),
    ("BA-DHJ", "Donald Hand Jr.", "Boston College"), ("BA-DL", "Deniya Prawl", "Tennessee"),
    ("BA-DM", "Devin McGlockton", "Vanderbilt"), ("BA-DP", "Darryn Peterson", "Kansas"),
    ("BA-DW", "Darrion Williams", "NC State"), ("BA-DX", "Darianna Alexander", "Cincinnati"),
    ("BA-ES", "Emilee Skinner", "Duke"), ("BA-GK", "Grace Knox", "LSU"),
    ("BA-HS", "Hailee Swain", "Stanford"), ("BA-ID", "Isaiah Denis", "UNC"),
    ("BA-IH", "Isiah Harwell", "Houston"), ("BA-JB", "John Blackwell", "Wisconsin"),
    ("BA-JC", "Jaida Civil", "Tennessee"), ("BA-JD", "Josh Dix", "Creighton"),
    ("BA-JE", "Jason Edwards", "Providence"), ("BA-JG", "Joe Grahovac", "St. Bonaventure"),
    ("BA-JJ", "Jasper Johnson", "Kentucky"), ("BA-JL", "Jaland Lowe", "Kentucky"),
    ("BA-JO", "Jamier Jones", "Providence"), ("BA-JS", "Jeremiah Wilkinson", "Georgia"),
    ("BA-JT", "JT Toppin", "Texas Tech"), ("BA-JW", "Juju Watkins", "USC"),
    ("BA-KA", "Kiyan Anthony", "Syracuse"), ("BA-KC", "Kaelyn Carroll", "Kentucky"),
    ("BA-KD", "Kara Dunn", "USC"), ("BA-KF", "Kelis Fisher", "UConn"),
    ("BA-KH", "Keyshawn Hall", "Auburn"), ("BA-KM", "Kiyomi McMiller", "Penn State"),
    ("BA-KP", "Koa Peat", "Arizona"), ("BA-KS", "Kaylene Smikle", "Maryland"),
    ("BA-KW", "Kam Williams", "Kentucky"), ("BA-LM", "Leah Macy", "Notre Dame"),
    ("BA-LS", "Lara Somfai", "Stanford"), ("BA-MA", "Michael Rataj", "Baylor"),
    ("BA-MB", "Madison Booker", "Texas"), ("BA-MBJ", "Mikel Brown Jr.", "Louisville"),
    ("BA-MR", "Malik Reneau", "Miami"), ("BA-MU", "Milos Uzan", "Houston"),
    ("BA-NA", "Nate Ament", "Tennessee"), ("BA-NB", "Niko Bundalo", "Ole Miss"),
    ("BA-NC", "Nate Calmese", "Wake Forest"), ("BA-NL", "Nate Bittle", "Oregon"),
    ("BA-NM", "Nick Martinelli", "Northwestern"), ("BA-NR", "Nyla Brooks", "UNC"),
    ("BA-OA", "Obi Agbim", "Baylor"), ("BA-OR", "Owen Freeman", "Creighton"),
    ("BA-OS", "Oziyah Sellers", "St. John's"), ("BA-PP", "Pharrel Payne", "Maryland"),
    ("BA-RB", "Reed Bailey", "Indiana"), ("BA-RC", "Ryan Conwell", "Louisville"),
    ("BA-RE", "Raegan Beers", "Oklahoma"), ("BA-RMC", "Robert McCray V", "Florida State"),
    ("BA-RS", "Richie Saunders", "BYU"), ("BA-SA", "Shon Abaev", "Cincinnati"),
    ("BA-SB", "Sienna Betts", "UCLA"), ("BA-SD", "Silas Demary Jr.", "UConn"),
    ("BA-SH", "Shelton Henderson", "Miami"), ("BA-SS", "Sarah Strong", "UConn"),
    ("BA-ST", "Sadiq White Jr.", "Syracuse"), ("BA-SW", "Serah Williams", "UConn"),
    ("BA-TA", "Tobe Awaka", "Arizona"), ("BA-TD", "Tre Donaldson", "Miami"),
    ("BA-TH", "Tre Holloman", "NC State"), ("BA-TJ", "Tylis Jordan", "Ole Miss"),
    ("BA-TKR", "Trey Kaufman-Renn", "Purdue"), ("BA-TL", "Ta'Niya Latson", "South Carolina"),
    ("BA-TR", "Tarris Reed Jr.", "UConn"), ("BA-TY", "Tounde Yessoufou", "Baylor"),
    ("BA-WG", "Winters Grady", "Michigan"), ("BA-WS", "Wesley Yates III", "Washington Huskies"),
    ("BA-XL", "Xaivian Lee", "Florida"), ("BA-YG", "Yarden Garzon", "Maryland"),
    ("BA-ZE", "Zuby Ejiofor", "St. John's"), ("BA-ZJ", "ZaKiyah Johnson", "LSU"),
]
add_cards(ba_id, ba_cards)
print(f"  Best of 2025 Autographs: {len(ba_cards)} cards, {len(ba_pars)} parallels")

# Greatness Awaits Autographs (GA-XX) — 39 cards
# Note: The prompt lists 40 entries but the header says 39. Let me count... 40 entries.
ga_id = add_is("Greatness Awaits Autographs")
add_pars(ga_id, ga_pars)
ga_cards = [
    ("GA-AC", "Ayla McDowell", "South Carolina"), ("GA-AE", "Alexandra Eschmeyer", "Stanford"),
    ("GA-AF", "Ace Flagg", "Maine"), ("GA-AM", "Aliyahna Morris", "California"),
    ("GA-BG", "Brandon Garrison", "Kentucky"), ("GA-BI", "Braden Smith", "Purdue"),
    ("GA-BM", "Boopie Miller", "SMU"), ("GA-BZ", "Bennett Stirtz", "Iowa"),
    ("GA-CF", "Caleb Foster", "Duke"), ("GA-CI", "CJ Ingram", "Florida"),
    ("GA-CW", "Caleb Wilson", "UNC"), ("GA-DA", "Darianna Alexander", "Cincinnati"),
    ("GA-ES", "Emilee Skinner", "Duke"), ("GA-JB", "John Blackwell", "Wisconsin"),
    ("GA-JC", "Jaida Civil", "Tennessee"), ("GA-JG", "Ja'Kobi Gillespie", "Tennessee"),
    ("GA-JT", "JT Toppin", "Texas Tech"), ("GA-JW", "Jeremiah Wilkinson", "Georgia"),
    ("GA-KC", "Kaelyn Carroll", "Kentucky"), ("GA-KD", "Kara Dunn", "USC"),
    ("GA-KF", "Kelis Fisher", "UConn"), ("GA-KS", "Kohl Rosario", "Kansas"),
    ("GA-LM", "Leah Macy", "Notre Dame"), ("GA-NB", "Nyla Brooks", "UNC"),
    ("GA-NC", "Nate Calmese", "Wake Forest"), ("GA-NL", "Nate Bittle", "Oregon"),
    ("GA-NM", "Nick Martinelli", "Northwestern"), ("GA-OO", "Otega Oweh", "Kentucky"),
    ("GA-OS", "Oziyah Sellers", "St. John's"), ("GA-PY", "Pharrel Payne", "Maryland"),
    ("GA-RB", "Raegan Beers", "Oklahoma"), ("GA-RS", "Richie Saunders", "BYU"),
    ("GA-SS", "Sarah Strong", "UConn"), ("GA-SW", "Sebastian Wilkins", "Duke"),
    ("GA-TA", "Tobe Awaka", "Arizona"), ("GA-TH", "Tre Holloman", "NC State"),
    ("GA-TL", "Ta'Niya Latson", "South Carolina"), ("GA-WG", "Winters Grady", "Michigan"),
    ("GA-YG", "Yarden Garzon", "Maryland"), ("GA-ZJ", "ZaKiyah Johnson", "LSU"),
]
add_cards(ga_id, ga_cards)
print(f"  Greatness Awaits Autographs: {len(ga_cards)} cards, {len(ga_pars)} parallels")

# Iso Signatures (IS-XX) — 25 cards
is_id = add_is("Iso Signatures")
add_pars(is_id, ga_pars)
is_cards = [
    ("IS-AD", "AJ Dybantsa", "BYU"), ("IS-AL", "Addison Deal", "Iowa"),
    ("IS-AS", "Acaden Lewis", "Villanova"), ("IS-BM", "Brynn McGaughy", "Washington"),
    ("IS-BT", "Bryson Tiller", "Kansas"), ("IS-DA", "Dwayne Aristode", "Arizona"),
    ("IS-DP", "Darryn Peterson", "Kansas"), ("IS-IH", "Isiah Harwell", "Houston"),
    ("IS-JI", "Josh Dix", "Creighton"), ("IS-JJ", "Jasper Johnson", "Kentucky"),
    ("IS-JS", "Jason Edwards", "Providence"), ("IS-KA", "Kiyan Anthony", "Syracuse"),
    ("IS-KP", "Koa Peat", "Arizona"), ("IS-KW", "Kam Williams", "Kentucky"),
    ("IS-MBJ", "Mikel Brown Jr.", "Louisville"), ("IS-MO", "Madison Booker", "Texas"),
    ("IS-NA", "Nate Ament", "Tennessee"), ("IS-OA", "Obi Agbim", "Baylor"),
    ("IS-RC", "Ryan Conwell", "Louisville"), ("IS-RMC", "Robert McCray V", "Florida State"),
    ("IS-SB", "Sienna Betts", "UCLA"), ("IS-SH", "Shelton Henderson", "Miami"),
    ("IS-TD", "Tre Donaldson", "Miami"), ("IS-TJ", "Tylis Jordan", "Ole Miss"),
    ("IS-TY", "Tounde Yessoufou", "Baylor"),
]
add_cards(is_id, is_cards)
print(f"  Iso Signatures: {len(is_cards)} cards, {len(ga_pars)} parallels")

# Coaches Ink (CI-XX) — 5 cards (subject_role = 'coach')
ci_id = add_is("Coaches Ink")
add_pars(ci_id, ga_pars)
ci_cards = [
    ("CI-CC", "Cori Close", "UCLA"),
    ("CI-JS", "Jon Scheyer", "Duke"),
    ("CI-KS", "Kelvin Sampson", "Houston"),
    ("CI-LG", "Lindsay Gottlieb", "USC"),
    ("CI-TG", "Todd Golden", "Florida"),
]
for num, name, team in ci_cards:
    pid = get_or_create(name, "coach")
    db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, ?)",
               (pid, ci_id, str(num), team))
print(f"  Coaches Ink: {len(ci_cards)} cards (coaches), {len(ga_pars)} parallels")

# Dual Autographs Refractor (DRA-XX) — 20 cards
dra_id = add_is("Dual Autographs Refractor")
add_pars(dra_id, dt_pars)
dra_cards = [
    ("DRA-AD", "AJ Dybantsa", "Darryn Peterson"),
    ("DRA-AJ", "AJ Dybantsa", "Juju Watkins"),
    ("DRA-AM", "Agot Makeer", "Hailee Swain"),
    ("DRA-BB", "Brayden Burries", "Koa Peat"),
    ("DRA-BZ", "Bennett Stirtz", "JT Toppin"),
    ("DRA-CA", "Christian Anderson", "JT Toppin"),
    ("DRA-CW", "Mikel Brown Jr.", "Caleb Wilson"),
    ("DRA-GK", "ZaKiyah Johnson", "Grace Knox"),
    ("DRA-IH", "Milos Uzan", "Isiah Harwell"),
    ("DRA-JW", "Juju Watkins", "Sarah Strong"),
    ("DRA-KA", "Kiyan Anthony", "Jasper Johnson"),
    ("DRA-KP", "Nate Ament", "Koa Peat"),
    ("DRA-KR", "Braden Smith", "Trey Kaufman-Renn"),
    ("DRA-MB", "Madison Booker", "Aaliyah Crump"),
    ("DRA-NA", "Nate Ament", "Darryn Peterson"),
    ("DRA-NB", "Nyla Brooks", "Caleb Wilson"),
    ("DRA-RB", "Raegan Beers", "Juju Watkins"),
    ("DRA-RS", "AJ Dybantsa", "Richie Saunders"),
    ("DRA-SB", "Sienna Betts", "Aaliyah Crump"),
    ("DRA-SS", "Darryn Peterson", "Sarah Strong"),
]
add_dual_cards(dra_id, dra_cards)
print(f"  Dual Autographs Refractor: {len(dra_cards)} cards, {len(dt_pars)} parallels")

# Triple Autographs Refractor (TRA-XX) — 10 cards
tra_id = add_is("Triple Autographs Refractor")
add_pars(tra_id, dt_pars)
tra_cards = [
    ("TRA-AC", "Raegan Beers", "Aaliyah Crump", "Emilee Skinner"),
    ("TRA-AD", "AJ Dybantsa", "Darryn Peterson", "Nate Ament"),
    ("TRA-DP", "Juju Watkins", "Darryn Peterson", "AJ Dybantsa"),
    ("TRA-KA", "Nate Ament", "Jasper Johnson", "Kiyan Anthony"),
    ("TRA-MB", "Mikel Brown Jr.", "Koa Peat", "Caleb Wilson"),
    ("TRA-MU", "Braden Smith", "Zuby Ejiofor", "Milos Uzan"),
    ("TRA-NB", "Nyla Brooks", "Grace Knox", "Hailee Swain"),
    ("TRA-OO", "Jasper Johnson", "Otega Oweh", "Jaland Lowe"),
    ("TRA-RB", "Juju Watkins", "Raegan Beers", "Sarah Strong"),
    ("TRA-SB", "Emilee Skinner", "Sienna Betts", "Aaliyah Crump"),
]
add_triple_cards(tra_id, tra_cards)
print(f"  Triple Autographs Refractor: {len(tra_cards)} cards, {len(dt_pars)} parallels")


# ─── AUTO-RELIC SUBSETS ─────────────────────────────────────────────────────

def add_relic_subset(name, cards):
    r_id = add_is(name)
    add_pars(r_id, relic_pars)
    add_cards(r_id, cards)
    print(f"  {name}: {len(cards)} cards, {len(relic_pars)} parallels")

# Prospect Jumbo Relic Autographs (PJR-XX) — 37 cards
add_relic_subset("Prospect Jumbo Relic Autographs", [
    ("PJR-AC", "Aaliyah Crump", "Texas"), ("PJR-AD", "AJ Dybantsa", "BYU"),
    ("PJR-AE", "Addison Deal", "Iowa"), ("PJR-AL", "Acaden Lewis", "Villanova"),
    ("PJR-AM", "Agot Makeer", "South Carolina"), ("PJR-BB", "Brayden Burries", "Arizona"),
    ("PJR-BI", "Braden Smith", "Purdue"), ("PJR-BS", "Braeden Shrewsberry", "Notre Dame"),
    ("PJR-CC", "Coen Carr", "Michigan State"), ("PJR-CM", "Cotie McMahon", "Ole Miss"),
    ("PJR-CW", "Caleb Wilson", "UNC"), ("PJR-DH", "Donald Hand Jr.", "Boston College"),
    ("PJR-DP", "Darryn Peterson", "Kansas"), ("PJR-DW", "Darrion Williams", "NC State"),
    ("PJR-ES", "Emilee Skinner", "Duke"), ("PJR-HS", "Hailee Swain", "Stanford"),
    ("PJR-ID", "Isaiah Denis", "UNC"), ("PJR-IH", "Isiah Harwell", "Houston"),
    ("PJR-JW", "Juju Watkins", "USC"), ("PJR-KA", "Kiyan Anthony", "Syracuse"),
    ("PJR-KH", "Sebastian Wilkins", "Duke"), ("PJR-KM", "Kiyomi McMiller", "Penn State"),
    ("PJR-KP", "Koa Peat", "Arizona"), ("PJR-KR", "Kohl Rosario", "Kansas"),
    ("PJR-MO", "Madison Booker", "Texas"), ("PJR-MU", "Milos Uzan", "Houston"),
    ("PJR-NA", "Nate Ament", "Tennessee"), ("PJR-OA", "Obi Agbim", "Baylor"),
    ("PJR-OO", "Otega Oweh", "Kentucky"), ("PJR-RB", "Reed Bailey", "Indiana"),
    ("PJR-RR", "Raegan Beers", "Oklahoma"), ("PJR-SA", "Shon Abaev", "Cincinnati"),
    ("PJR-SS", "Sarah Strong", "UConn"), ("PJR-TKR", "Trey Kaufman-Renn", "Purdue"),
    ("PJR-TY", "Tounde Yessoufou", "Baylor"), ("PJR-WG", "Winters Grady", "Michigan"),
    ("PJR-XL", "Xaivian Lee", "Florida"),
])

# Prospect Dual Relic Autographs (PDA-XX) — 39 cards
add_relic_subset("Prospect Dual Relic Autographs", [
    ("PDA-AC", "Aaliyah Crump", "Texas"), ("PDA-AD", "AJ Dybantsa", "BYU"),
    ("PDA-AK", "Agot Makeer", "South Carolina"), ("PDA-AL", "Addison Deal", "Iowa"),
    ("PDA-AM", "Ayla McDowell", "South Carolina"), ("PDA-BB", "Brayden Burries", "Arizona"),
    ("PDA-BM", "Braden Smith", "Purdue"), ("PDA-BR", "Braeden Shrewsberry", "Notre Dame"),
    ("PDA-BZ", "Bennett Stirtz", "Iowa"), ("PDA-CF", "Caleb Foster", "Duke"),
    ("PDA-CR", "Chase Ross", "Marquette"), ("PDA-CW", "Caleb Wilson", "UNC"),
    ("PDA-DH", "Donald Hand Jr.", "Boston College"), ("PDA-DP", "Darryn Peterson", "Kansas"),
    ("PDA-DW", "Darrion Williams", "NC State"), ("PDA-ES", "Emilee Skinner", "Duke"),
    ("PDA-ID", "Isaiah Denis", "UNC"), ("PDA-JJ", "Jamier Jones", "Providence"),
    ("PDA-JT", "JT Toppin", "Texas Tech"), ("PDA-JW", "Juju Watkins", "USC"),
    ("PDA-KA", "Kiyan Anthony", "Syracuse"), ("PDA-KH", "Keyshawn Hall", "Auburn"),
    ("PDA-KK", "Kaelyn Carroll", "Kentucky"), ("PDA-KM", "Kiyomi McMiller", "Penn State"),
    ("PDA-KP", "Koa Peat", "Arizona"), ("PDA-KR", "Kohl Rosario", "Kansas"),
    ("PDA-MB", "Madison Booker", "Texas"), ("PDA-MU", "Milos Uzan", "Houston"),
    ("PDA-NA", "Nate Ament", "Tennessee"), ("PDA-NB", "Nyla Brooks", "UNC"),
    ("PDA-NM", "Nick Martinelli", "Northwestern"), ("PDA-OO", "Otega Oweh", "Kentucky"),
    ("PDA-RB", "Raegan Beers", "Oklahoma"), ("PDA-RE", "Reed Bailey", "Indiana"),
    ("PDA-SA", "Shon Abaev", "Cincinnati"), ("PDA-SB", "Sebastian Wilkins", "Duke"),
    ("PDA-SS", "Sarah Strong", "UConn"), ("PDA-SW", "Serah Williams", "UConn"),
    ("PDA-TY", "Tounde Yessoufou", "Baylor"),
])

# Let It Rain Relic Autographs (LR-XX) — 18 cards
add_relic_subset("Let It Rain Relic Autographs", [
    ("LR-AD", "AJ Dybantsa", "BYU"), ("LR-AM", "Ayla McDowell", "South Carolina"),
    ("LR-BZ", "Bennett Stirtz", "Iowa"), ("LR-CF", "Caleb Foster", "Duke"),
    ("LR-CR", "Chase Ross", "Marquette"), ("LR-CW", "Caleb Wilson", "UNC"),
    ("LR-DP", "Darryn Peterson", "Kansas"), ("LR-ES", "Emilee Skinner", "Duke"),
    ("LR-IH", "Isiah Harwell", "Houston"), ("LR-JJ", "Jasper Johnson", "Kentucky"),
    ("LR-JO", "Jamier Jones", "Providence"), ("LR-JT", "JT Toppin", "Texas Tech"),
    ("LR-NA", "Nate Ament", "Tennessee"), ("LR-NM", "Nick Martinelli", "Northwestern"),
    ("LR-OA", "Obi Agbim", "Baylor"), ("LR-SW", "Serah Williams", "UConn"),
    ("LR-TKR", "Trey Kaufman-Renn", "Purdue"), ("LR-WG", "Winters Grady", "Michigan"),
])

# Game Graphs (GG-XX) — 85 cards (note: last entry is GGBM with no hyphen)
add_relic_subset("Game Graphs", [
    ("GG-AD", "Addison Deal", "Iowa"), ("GG-AE", "Alexandra Eschmeyer", "Stanford"),
    ("GG-AL", "Acaden Lewis", "Villanova"), ("GG-AM", "Aliyahna Morris", "California"),
    ("GG-AY", "AJ Dybantsa", "BYU"), ("GG-BB", "Brayden Burries", "Arizona"),
    ("GG-BG", "Brandon Garrison", "Kentucky"), ("GG-BH", "Braeden Shrewsberry", "Notre Dame"),
    ("GG-BI", "Braden Smith", "Purdue"), ("GG-BL", "Bryce Lindsay", "Villanova"),
    ("GG-BM", "Boopie Miller", "SMU"), ("GG-BT", "Bryson Tiller", "Kansas"),
    ("GG-BZ", "Bennett Stirtz", "Iowa"), ("GG-CA", "Christian Anderson", "Texas Tech"),
    ("GG-CB", "Cameron Boozer", "Duke"), ("GG-CF", "Caleb Foster", "Duke"),
    ("GG-CI", "CJ Ingram", "Florida"), ("GG-CM", "Cotie McMahon", "Ole Miss"),
    ("GG-CR", "Chase Ross", "Marquette"), ("GG-CW", "Caleb Wilson", "UNC"),
    ("GG-CZ", "Cayden Boozer", "Duke"), ("GG-DD", "Derek Dixon", "UNC"),
    ("GG-DF", "Davis Fogle", "Gonzaga"), ("GG-DH", "Donald Hand Jr.", "Boston College"),
    ("GG-DL", "Deniya Prawl", "Tennessee"), ("GG-DM", "Devin McGlockton", "Vanderbilt"),
    ("GG-DN", "Davion Hannah", "Alabama"), ("GG-DP", "Darryn Peterson", "Kansas"),
    ("GG-DS", "Dwayne Aristode", "Arizona"), ("GG-DW", "Darrion Williams", "NC State"),
    ("GG-ES", "Emilee Skinner", "Duke"), ("GG-GN", "Grace Knox", "LSU"),
    ("GG-HS", "Hailee Swain", "Stanford"), ("GG-ID", "Isaiah Denis", "UNC"),
    ("GG-IH", "Isiah Harwell", "Houston"), ("GG-JB", "John Blackwell", "Wisconsin"),
    ("GG-JC", "Jaida Civil", "Tennessee"), ("GG-JD", "Josh Dix", "Creighton"),
    ("GG-JG", "Ja'Kobi Gillespie", "Tennessee"), ("GG-JI", "Jeremiah Wilkinson", "Georgia"),
    ("GG-JL", "Jaland Lowe", "Kentucky"), ("GG-JO", "Jasper Johnson", "Kentucky"),
    ("GG-JR", "Joe Grahovac", "St. Bonaventure"), ("GG-JT", "JT Toppin", "Texas Tech"),
    ("GG-JW", "Juju Watkins", "USC"), ("GG-KA", "Kiyan Anthony", "Syracuse"),
    ("GG-KC", "Kaelyn Carroll", "Kentucky"), ("GG-KD", "Kara Dunn", "USC"),
    ("GG-KH", "Keyshawn Hall", "Auburn"), ("GG-KM", "Kiyomi McMiller", "Penn State"),
    ("GG-KP", "Koa Peat", "Arizona"), ("GG-KR", "Kohl Rosario", "Kansas"),
    ("GG-KS", "Kaylene Smikle", "Maryland"), ("GG-KW", "Kam Williams", "Kentucky"),
    ("GG-MB", "Mikel Brown Jr.", "Louisville"), ("GG-MR", "Malik Reneau", "Miami"),
    ("GG-MU", "Milos Uzan", "Houston"), ("GG-NA", "Nate Ament", "Tennessee"),
    ("GG-NB", "Nate Bittle", "Oregon"), ("GG-NM", "Nick Martinelli", "Northwestern"),
    ("GG-NR", "Nyla Brooks", "UNC"), ("GG-NU", "Niko Bundalo", "Ole Miss"),
    ("GG-OA", "Obi Agbim", "Baylor"), ("GG-OF", "Owen Freeman", "Creighton"),
    ("GG-OO", "Otega Oweh", "Kentucky"), ("GG-OS", "Oziyah Sellers", "St. John's"),
    ("GG-PY", "Pharrel Payne", "Maryland"), ("GG-RB", "Raegan Beers", "Oklahoma"),
    ("GG-RC", "Ryan Conwell", "Louisville"), ("GG-RM", "Robert McCray V", "Florida State"),
    ("GG-RS", "Richie Saunders", "BYU"), ("GG-SA", "Shon Abaev", "Cincinnati"),
    ("GG-SB", "Sienna Betts", "UCLA"), ("GG-SH", "Shelton Henderson", "Miami"),
    ("GG-SI", "Sadiq White", "Syracuse"), ("GG-SW", "Sebastian Wilkins", "Duke"),
    ("GG-TA", "Tobe Awaka", "Arizona"), ("GG-TD", "Tre Donaldson", "Miami"),
    ("GG-TH", "Tre Holloman", "NC State"), ("GG-TJ", "Tylis Jordan", "Ole Miss"),
    ("GG-TKR", "Trey Kaufman-Renn", "Purdue"), ("GG-TR", "Tarris Reed Jr.", "UConn"),
    ("GG-TY", "Tounde Yessoufou", "Baylor"), ("GG-WY", "Wesley Yates III", "Washington Huskies"),
    ("GG-XL", "Xaivian Lee", "Florida"), ("GG-YG", "Yarden Garzon", "Maryland"),
    ("GG-ZE", "Zuby Ejiofor", "St. John's"), ("GG-ZJ", "ZaKiyah Johnson", "LSU"),
    ("GGBM", "Brynn McGaughy", "Washington"),
])


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

# Verify coaches
coaches = db.execute("SELECT name, subject_role FROM players WHERE set_id = ? AND subject_role = 'coach'", (SET_ID,)).fetchall()
print(f"\nCoaches: {[c[0] for c in coaches]}")

# Verify Cam Ward dedup
cam_wards = db.execute("SELECT p.id, p.name, p.set_id, s.name FROM players p JOIN sets s ON p.set_id = s.id WHERE p.name = 'Cam Ward'").fetchall()
print(f"Cam Ward records: {len(cam_wards)}")
for cw in cam_wards:
    print(f"  ID {cw[0]}: {cw[1]} in {cw[3]} (set {cw[2]})")

# Verify Boozer twins
boozers = db.execute("SELECT id, name FROM players WHERE set_id = ? AND name LIKE '%Boozer%'", (SET_ID,)).fetchall()
print(f"Boozer twins: {[(b[0], b[1]) for b in boozers]}")

print(f"\n{'='*50}")
print(f"Set ID: {SET_ID}")
print(f"Total insert sets: {total_insert_sets}")
print(f"Total unique players: {total_players}")
print(f"Total card appearances: {total_appearances}")
print(f"Total parallels: {total_parallels}")
print(f"Expected: 609 card appearances")
db.close()
print("Done!")
