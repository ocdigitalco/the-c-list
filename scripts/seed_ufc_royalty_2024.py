"""
Seed script: 2024 Topps Royalty UFC
Inserts all data into the local SQLite database (the-c-list.db).
Usage: python3 scripts/seed_ufc_royalty_2024.py
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
    """Get existing player or create new one. Returns player id."""
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


# ─── Name normalization ────────────────────────────────────────────────────────
# Map variant spellings to a single canonical name per fighter.
# The FIRST occurrence of a name sets the canonical form.

NAME_ALIASES = {
    "Benoît Saint-Denis": "Benoit Saint Denis",
    "Yair Rodriguez": "Yair Rodríguez",
    "Jiri Prochaska": "Jiri Prochazka",
    "Kai Kara France": "Kai Kara-France",
    "Maria Godinez Gonzalez": "Loopy Godinez",
    "Jiří Procházka": "Jiri Prochazka",
    "Aleksandar Rakić": "Aleksandar Rakic",
    "Brady Heistand": "Brady Hiestand",
    "Natalia Cristina Da Silva": "Natalia Cristina da Silva",
    "Shogun Rua": "Mauricio Rua",
}


def normalize_name(raw_name):
    """Strip RC tag and normalize spelling variants."""
    name = raw_name.strip()
    is_rookie = False
    if name.endswith(" RC"):
        name = name[:-3].strip()
        is_rookie = True
    name = NAME_ALIASES.get(name, name)
    return name, is_rookie


# ─── 1. Create the set ─────────────────────────────────────────────────────────

SET_NAME = "2024 Topps Royalty UFC"

# Check if set already exists
cur.execute("SELECT id FROM sets WHERE name = ?", (SET_NAME,))
existing = cur.fetchone()
if existing:
    print(f"Set '{SET_NAME}' already exists with id {existing[0]}. Aborting.")
    conn.close()
    exit(1)

# Build pack_odds JSON
pack_odds = {
    # Base parallels
    "Base Set": 1,
    "Base Set Purple": 3,
    "Base Set Blue": 4,
    "Base Set Red": 6,
    "Base Set Gold": 9,
    "Base Set Green": 17,
    "Base Set Platinum": 80,
    # Ambassador Autographs
    "Ambassador Autographs": 10,
    "Ambassador Autographs Blue": 46,
    "Ambassador Autographs Gold": 98,
    "Ambassador Autographs Green": 209,
    "Ambassador Autographs Platinum": 963,
    # Autographed Jumbo Relic Booklet
    "Autographed Jumbo Relic Booklet": 14,
    "Autographed Jumbo Relic Booklet Green": 53,
    "Autographed Jumbo Relic Booklet Platinum": 257,
    # Golden Hall Autographs
    "Golden Hall Autographs": 6,
    "Golden Hall Autographs Blue": 18,
    "Golden Hall Autographs Gold": 43,
    "Golden Hall Autographs Green": 86,
    "Golden Hall Autographs Platinum": 428,
    # Imperial Ink
    "Imperial Ink": 6,
    "Imperial Ink Blue": 16,
    "Imperial Ink Gold": 39,
    "Imperial Ink Green": 78,
    "Imperial Ink Platinum": 428,
    # Influential Ink
    "Influential Ink": 5,
    "Influential Ink Blue": 11,
    "Influential Ink Gold": 26,
    "Influential Ink Green": 51,
    "Influential Ink Platinum": 257,
    # Pursuit of Greatness Signatures
    "Pursuit of Greatness Signatures": 5,
    "Pursuit of Greatness Signatures Blue": 10,
    "Pursuit of Greatness Signatures Gold": 24,
    "Pursuit of Greatness Signatures Green": 47,
    "Pursuit of Greatness Signatures Platinum": 227,
    # Regalia Relic Signatures
    "Regalia Relic Signatures": 2,
    "Regalia Relic Signatures Blue": 6,
    "Regalia Relic Signatures Gold": 14,
    "Regalia Relic Signatures Green": 27,
    "Regalia Relic Signatures Platinum": 143,
    # Rookie Autographs
    "Rookie Autographs": 5,
    "Rookie Autographs Blue": 15,
    "Rookie Autographs Gold": 37,
    "Rookie Autographs Green": 73,
    "Rookie Autographs Platinum": 351,
    # Rookie Relic Autographs
    "Rookie Relic Autographs": 4,
    "Rookie Relic Autographs Blue": 14,
    "Rookie Relic Autographs Gold": 33,
    "Rookie Relic Autographs Green": 66,
    "Rookie Relic Autographs Platinum": 321,
    # Royalty Relic Signatures
    "Royalty Relic Signatures": 3,
    "Royalty Relic Signatures Blue": 10,
    "Royalty Relic Signatures Gold": 23,
    "Royalty Relic Signatures Green": 46,
    "Royalty Relic Signatures Platinum": 221,
    # Superior Relic Signatures
    "Superior Relic Signatures": 5,
    "Superior Relic Signatures Blue": 14,
    "Superior Relic Signatures Gold": 33,
    "Superior Relic Signatures Green": 66,
    "Superior Relic Signatures Platinum": 321,
    # Superior Signatures
    "Superior Signatures": 4,
    "Superior Signatures Blue": 10,
    "Superior Signatures Gold": 25,
    "Superior Signatures Green": 49,
    "Superior Signatures Platinum": 249,
    # Triumph Relic Signatures
    "Triumph Relic Signatures": 6,
    "Triumph Relic Signatures Blue": 14,
    "Triumph Relic Signatures Gold": 32,
    "Triumph Relic Signatures Green": 64,
    "Triumph Relic Signatures Platinum": 309,
    # UFC Honors Autographs
    "UFC Honors Autographs": 75,
    "UFC Honors Autographs Platinum": 703,
    # Dual Autographs
    "Dual Autographs": 18,
    "Dual Autographs Platinum": 428,
    # Triple Autographs
    "Triple Autographs": 82,
    "Triple Autographs Platinum": 1926,
    # Dual Fighter Relic Autograph Books
    "Dual Fighter Relic Autograph Books": 53,
    "Dual Fighter Relic Autograph Books Green": 257,
    "Dual Fighter Relic Autograph Books Platinum": 1284,
    # The Coronation
    "The Coronation": 37,
    # Royal Decree
    "Royal Decree": 19,
    # The Time Is Now
    "The Time Is Now": 44,
    # Liquid Silver
    "Liquid Silver": 89,
    "Liquid Silver Gold": 771,
    # Prodigious Pairings
    "Prodigious Pairings": 5,
    "Prodigious Pairings Blue": 17,
    "Prodigious Pairings Gold": 41,
    "Prodigious Pairings Green": 80,
    "Prodigious Pairings Platinum": 386,
    # Regalia Relics
    "Regalia Relics": 2,
    "Regalia Relics Blue": 5,
    "Regalia Relics Gold": 11,
    "Regalia Relics Green": 22,
    "Regalia Relics Platinum": 107,
    # Relic Jewels
    "Relic Jewels": 3,
    "Relic Jewels Blue": 11,
    "Relic Jewels Gold": 27,
    "Relic Jewels Green": 54,
    "Relic Jewels Platinum": 257,
    # Rookie Jumbo Relics
    "Rookie Jumbo Relics": 4,
    "Rookie Jumbo Relics Blue": 13,
    "Rookie Jumbo Relics Gold": 31,
    "Rookie Jumbo Relics Green": 62,
    "Rookie Jumbo Relics Platinum": 297,
    # Star Relics
    "Star Relics": 2,
    "Star Relics Blue": 7,
    "Star Relics Gold": 17,
    "Star Relics Green": 33,
    "Star Relics Platinum": 158,
}

cur.execute(
    "INSERT INTO sets (name, sport, season, league, tier, pack_odds) VALUES (?, ?, ?, ?, ?, ?)",
    (SET_NAME, "MMA", "2024", "UFC", "Premium", json.dumps(pack_odds)),
)
set_id = cur.lastrowid
print(f"Created set '{SET_NAME}' with id {set_id}")

# ─── 2. Standard parallel definitions ──────────────────────────────────────────

# Reusable parallel structures
BASE_PARALLELS = [
    ("Base /99", 99),
    ("Purple", 35),
    ("Blue", 25),
    ("Red", 15),
    ("Gold", 10),
    ("Green", 5),
    ("Platinum", 1),
]

AUTO_99_PARALLELS = [
    ("Base /99", 99),
    ("Blue", 25),
    ("Gold", 10),
    ("Green", 5),
    ("Platinum", 1),
]

AUTO_25_PARALLELS = [
    ("Base /25", 25),
    ("Platinum", 1),
]

RELIC_99_PARALLELS = [
    ("Base /99", 99),
    ("Blue", 25),
    ("Gold", 10),
    ("Green", 5),
    ("Platinum", 1),
]

AJRB_PARALLELS = [
    ("Green", 5),
    ("Platinum", 1),
]

DRA_PARALLELS = [
    ("Green", 5),
    ("Platinum", 1),
]


# ─── 3. Insert sets + parallels + cards ─────────────────────────────────────────

# We'll track all appearances for co-player linking
# Format: { "insert_set_name:card_number": [appearance_id, ...] }
multi_card_appearances = {}
# Track (appearance_id -> player_id) for co-player linking
appearance_player_map = {}


def add_cards(insert_set_id, insert_set_name, cards, default_rookie=False):
    """Add cards to an insert set. cards = [(card_number, raw_name), ...]"""
    for card_number, raw_name in cards:
        name, is_rc = normalize_name(raw_name)
        is_rookie = is_rc or default_rookie
        player_id = get_or_create_player(set_id, name)
        app_id = create_appearance(player_id, insert_set_id, card_number, is_rookie)
        appearance_player_map[app_id] = player_id
    return len(cards)


def add_multi_cards(insert_set_id, insert_set_name, cards, default_rookie=False):
    """Add multi-fighter cards (dual/triple). cards = [(card_number, [name1, name2, ...]), ...]"""
    for card_number, names in cards:
        app_ids = []
        player_ids = []
        for raw_name in names:
            name, is_rc = normalize_name(raw_name)
            is_rookie = is_rc or default_rookie
            player_id = get_or_create_player(set_id, name)
            app_id = create_appearance(player_id, insert_set_id, card_number, is_rookie)
            app_ids.append(app_id)
            player_ids.append(player_id)
            appearance_player_map[app_id] = player_id
        # Link co-players
        for i, app_id in enumerate(app_ids):
            for j, other_player_id in enumerate(player_ids):
                if i != j:
                    create_co_player(app_id, other_player_id)


def make_insert_set(name, parallels_def, cards, default_rookie=False, is_multi=False):
    """Create insert set with parallels and cards."""
    is_id = create_insert_set(set_id, name)
    for par_name, par_pr in parallels_def:
        create_parallel(is_id, par_name, par_pr)
    if is_multi:
        add_multi_cards(is_id, name, cards, default_rookie)
    else:
        add_cards(is_id, name, cards, default_rookie)
    return is_id


# ────────────────────────────────────────────────────────────────────────────────
# BASE SET (100 cards)
# ────────────────────────────────────────────────────────────────────────────────

BASE_CARDS = [
    ("1", "Conor McGregor"),
    ("2", "Robelis Despaigne RC"),
    ("3", "Brian Ortega"),
    ("4", "Paddy Pimblett"),
    ("5", "Amanda Lemos"),
    ("6", "Mackenzie Dern"),
    ("7", "Yan Xiaonan"),
    ("8", "Alexander Volkanovski"),
    ("9", "Tony Ferguson"),
    ("10", "Diego Lopes RC"),
    ("11", "Kevin Holland"),
    ("12", "Natalia Cristina da Silva RC"),
    ("13", "Khabib Nurmagomedov"),
    ("14", "Tatsuro Taira"),
    ("15", "Jiri Prochazka"),
    ("16", "Yadong Song"),
    ("17", "Themba Gorimbo RC"),
    ("18", "Ketlen Vieira"),
    ("19", "Dustin Poirier"),
    ("20", "Zhang Weili"),
    ("21", "Cory Sandhagen"),
    ("22", "Maycee Barber"),
    ("23", "Brunno Ferreira RC"),
    ("24", "Umar Nurmagomedov"),
    ("25", "Alex Pereira"),
    ("26", "Sharaputdin Magomedov RC"),
    ("27", "Jan Błachowicz"),
    ("28", "Aljamain Sterling"),
    ("29", "Leon Edwards"),
    ("30", "Ciryl Gane"),
    ("31", "Jessica Andrade"),
    ("32", "Paulo Costa"),
    ("33", "Jamahal Hill"),
    ("34", "Erin Blanchfield"),
    ("35", "Joanna Jędrzejczyk"),
    ("36", "Molly McCann"),
    ("37", "Tatiana Suarez"),
    ("38", "Manon Fiorot"),
    ("39", "Arnold Allen"),
    ("40", "Jon Jones"),
    ("41", "Brandon Moreno"),
    ("42", "Merab Dvalishvili"),
    ("43", "Frankie Edgar"),
    ("44", "Wanderlei Silva"),
    ("45", "Alexandre Pantoja"),
    ("46", "Raul Rosas"),
    ("47", "Amanda Nunes"),
    ("48", "Michael Page RC"),
    ("49", "Yair Rodríguez"),
    ("50", "Ilia Topuria"),
    ("51", "Marvin Vettori"),
    ("52", "Johnny Walker"),
    ("53", "Michael Chandler"),
    ("54", "Sergei Pavlovich"),
    ("55", "Belal Muhammad"),
    ("56", "Shavkat Rakhmonov"),
    ("57", "Alexa Grasso"),
    ("58", "Raquel Pennington"),
    ("59", "Julianna Peña"),
    ("60", "Anthony Smith"),
    ("61", "Holly Holm"),
    ("62", "Manel Kape RC"),
    ("63", "José Aldo"),
    ("64", "Colby Covington"),
    ("65", "Ian Machado Garry"),
    ("66", "Marlon Vera"),
    ("67", "Tabatha Ricci"),
    ("68", "Movsar Evloev"),
    ("69", "Sean Strickland"),
    ("70", "Kai Kara-France"),
    ("71", "Petr Yan"),
    ("72", "Benoit Saint Denis RC"),
    ("73", "Rose Namajunas"),
    ("74", "Gabriel Miranda RC"),
    ("75", "Robert Whittaker"),
    ("76", "Justin Gaethje"),
    ("77", "Curtis Blaydes"),
    ("78", "Magomed Ankalaev"),
    ("79", "Daniel Cormier"),
    ("80", "Islam Makhachev"),
    ("81", "Jonny Parsons RC"),
    ("82", "Amir Albazi"),
    ("83", "Muhammad Mokaev"),
    ("84", "Valentina Shevchenko"),
    ("85", "Bo Nickal"),
    ("86", "Tom Aspinall"),
    ("87", "Charles Oliveira"),
    ("88", "Khamzat Chimaev"),
    ("89", "Arman Tsarukyan"),
    ("90", "Kayla Harrison RC"),
    ("91", "Anderson Silva"),
    ("92", "Rodrigo Nascimento RC"),
    ("93", "Dricus Du Plessis"),
    ("94", "Max Holloway"),
    ("95", "Jack Della Maddalena"),
    ("96", "Bryan Battle"),
    ("97", "Israel Adesanya"),
    ("98", "Michael Morales"),
    ("99", "Georges St-Pierre"),
    ("100", "Sean O'Malley"),
]

make_insert_set("Base Set", BASE_PARALLELS, BASE_CARDS)
print(f"  Base Set: 100 cards, {len(BASE_PARALLELS)} parallels")

# ────────────────────────────────────────────────────────────────────────────────
# AUTOGRAPH INSERT SETS (17 sets)
# ────────────────────────────────────────────────────────────────────────────────

# Ambassador Autographs (8 cards, /99)
make_insert_set("Ambassador Autographs", AUTO_99_PARALLELS, [
    ("AA-BB1", "Bruce Buffer"),
    ("AA-BB2", "Bruce Buffer"),
    ("AA-CL", "Chuck Liddell"),
    ("AA-DC", "Daniel Cormier"),
    ("AA-DWE", "Dana White"),
    ("AA-GS", "Georges St-Pierre"),
    ("AA-KN", "Khabib Nurmagomedov"),
    ("AA-SO", "Sean O'Malley"),
])
print("  Ambassador Autographs: 8 cards")

# Autographed Jumbo Relic Booklet (32 cards, unnumbered base + Green /5, Platinum /1)
make_insert_set("Autographed Jumbo Relic Booklet", AJRB_PARALLELS, [
    ("JRB-AGO", "Alexa Grasso"),
    ("JRB-BBR", "Bruce Buffer"),
    ("JRB-BDH", "Beneil Dariush"),
    ("JRB-CBO", "Caio Borralho"),
    ("JRB-CCN", "Colby Covington"),
    ("JRB-CEA", "Carla Esparza"),
    ("JRB-CGE", "Ciryl Gane"),
    ("JRB-DDP", "Dricus Du Plessis"),
    ("JRB-DHR", "Daniel Hooker"),
    ("JRB-DRS", "Dominick Reyes"),
    ("JRB-GBS", "Gilbert Burns"),
    ("JRB-GNL", "Aljamain Sterling"),
    ("JRB-IMG", "Ian Machado Garry"),
    ("JRB-JBZ", "Jan Błachowicz"),
    ("JRB-JDM", "Jack Della Maddalena"),
    ("JRB-JGE", "Justin Gaethje"),
    ("JRB-JJK", "Joanna Jędrzejczyk"),
    ("JRB-JJS", "Jasmine Jasudavicius"),
    ("JRB-JRK", "Jair Rozenstruik"),
    ("JRB-KKF", "Kai Kara-France"),
    ("JRB-LES", "Leon Edwards"),
    ("JRB-MBR", "Maycee Barber"),
    ("JRB-MCR", "Michael Chandler"),
    ("JRB-MFT", "Manon Fiorot"),
    ("JRB-MGT", "Mateusz Gamrot"),
    ("JRB-MHY", "Max Holloway"),
    ("JRB-SSC", "Serghei Spivac"),
    ("JRB-STN", "Stephen Thompson"),
    ("JRB-VLE", "Vicente Luque"),
    ("JRB-VOR", "Israel Adesanya"),
    ("JRB-YDS", "Yadong Song"),
    ("JRB-YRZ", "Yair Rodríguez"),
])
print("  Autographed Jumbo Relic Booklet: 32 cards")

# Golden Hall Autographs (19 cards, /99)
make_insert_set("Golden Hall Autographs", AUTO_99_PARALLELS, [
    ("GCLH-", "Chuck Liddell"),
    ("GH-AR", "Antonio Rodrigo Nogueira"),
    ("GH-BR", "Bas Rutten"),
    ("GH-DC", "Daniel Cormier"),
    ("GH-DE", "Donald Cerrone"),
    ("GH-FG", "Forrest Griffin"),
    ("GH-GS", "Georges St-Pierre"),
    ("GH-JA", "José Aldo"),
    ("GH-JP", "Jens Pulver"),
    ("GH-KN", "Khabib Nurmagomedov"),
    ("GH-MB", "Michael Bisping"),
    ("GH-MC", "Mark Coleman"),
    ("GH-MH", "Matt Hughes"),
    ("GH-RE", "Rashad Evans"),
    ("GH-RF", "Rich Franklin"),
    ("GH-RG", "Royce Gracie"),
    ("GH-TO", "Tito Ortiz"),
    ("GH-UF", "Urijah Faber"),
    ("GKSH-", "Ken Shamrock"),
])
print("  Golden Hall Autographs: 19 cards")

# Imperial Ink (22 cards, /99)
make_insert_set("Imperial Ink", AUTO_99_PARALLELS, [
    ("II-AA", "Anderson Silva"),
    ("II-AN", "Amanda Nunes"),
    ("II-AR", "Antonio Rodrigo Nogueira"),
    ("II-AS", "Anthony Smith"),
    ("II-BB", "Bryan Battle"),
    ("II-BF", "Brunno Ferreira"),
    ("II-CK", "Calvin Kattar"),
    ("II-DH", "Daniel Hooker"),
    ("II-DR", "Dominick Reyes"),
    ("II-GN", "Geoff Neal"),
    ("II-JD", "Jack Della Maddalena"),
    ("II-JJ", "Jack Jenkins"),
    ("II-JS", "Junior Dos Santos"),
    ("II-MB", "Michael Bisping"),
    ("II-MT", "Marcin Tybura"),
    ("II-NL", "Natan Levy"),
    ("II-RA", "Rafael Dos Anjos"),
    ("II-RD", "Roman Dolidze"),
    ("II-RR", "Raul Rosas"),
    ("II-SB", "Sean Brady"),
    ("II-UF", "Urijah Faber"),
    ("II-VW", "Val Woodburn"),
])
print("  Imperial Ink: 22 cards")

# Influential Ink (31 cards, /99)
make_insert_set("Influential Ink", AUTO_99_PARALLELS, [
    ("IIA-AAI", "Andrei Arlovski"),
    ("IIA-AGO", "Alexa Grasso"),
    ("IIA-APA", "Alex Pereira"),
    ("IIA-APJ", "Alexandre Pantoja"),
    ("IIA-ASG", "Aljamain Sterling"),
    ("IIA-ASH", "Anthony Smith"),
    ("IIA-AVI", "Alexander Volkanovski"),
    ("IIA-BMD", "Belal Muhammad"),
    ("IIA-BMO", "Brandon Moreno"),
    ("IIA-CEA", "Carla Esparza"),
    ("IIA-COA", "Charles Oliveira"),
    ("IIA-DCZ", "Dominick Cruz"),
    ("IIA-GBS", "Gilbert Burns"),
    ("IIA-HCO", "Henry Cejudo"),
    ("IIA-HHM", "Holly Holm"),
    ("IIA-IAA", "Israel Adesanya"),
    ("IIA-IMV", "Islam Makhachev"),
    ("IIA-JBZ", "Jan Błachowicz"),
    ("IIA-JET", "Josh Emmett"),
    ("IIA-JGE", "Justin Gaethje"),
    ("IIA-JJK", "Joanna Jędrzejczyk"),
    ("IIA-LES", "Leon Edwards"),
    ("IIA-MCR", "Michael Chandler"),
    ("IIA-MHY", "Max Holloway"),
    ("IIA-NMY", "Neil Magny"),
    ("IIA-RES", "Rashad Evans"),
    ("IIA-RNS", "Rose Namajunas"),
    ("IIA-SMC", "Stipe Miocic"),
    ("IIA-STN", "Stephen Thompson"),
    ("IIA-VSO", "Valentina Shevchenko"),
    ("IIA-ZWI", "Zhang Weili"),
])
print("  Influential Ink: 31 cards")

# Pursuit of Greatness Signatures (35 cards, /99)
make_insert_set("Pursuit of Greatness Signatures", AUTO_99_PARALLELS, [
    ("PGS-AAI", "Amir Albazi"),
    ("PGS-BAN", "Brendan Allen"),
    ("PGS-BSD", "Benoit Saint Denis"),
    ("PGS-CCN", "Colby Covington"),
    ("PGS-CGE", "Ciryl Gane"),
    ("PGS-CKR", "Calvin Kattar"),
    ("PGS-CSA", "Cameron Saaiman"),
    ("PGS-CSN", "Cory Sandhagen"),
    ("PGS-DDP", "Dricus Du Plessis"),
    ("PGS-GNL", "Geoff Neal"),
    ("PGS-IAV", "Ikram Aliskerov"),
    ("PGS-IMG", "Ian Machado Garry"),
    ("PGS-JAA", "Jailton Malhadinho"),
    ("PGS-JDM", "Jack Della Maddalena"),
    ("PGS-JML", "Jamahal Hill"),
    ("PGS-JPA", "Julianna Peña"),
    ("PGS-JPY", "Joe Pyfer"),
    ("PGS-JTR", "Jalin Turner"),
    ("PGS-KCV", "Khamzat Chimaev"),
    ("PGS-KHD", "Kevin Holland"),
    ("PGS-MAV", "Magomed Ankalaev"),
    ("PGS-MBR", "Maycee Barber"),
    ("PGS-MDI", "Merab Dvalishvili"),
    ("PGS-MGT", "Mateusz Gamrot"),
    ("PGS-RFV", "Rafael Fiziev"),
    ("PGS-RRS", "Raul Rosas"),
    ("PGS-RSN", "Ryan Spann"),
    ("PGS-SBY", "Sean Brady"),
    ("PGS-SOM", "Sean O'Malley"),
    ("PGS-SPH", "Sergei Pavlovich"),
    ("PGS-TAL", "Tom Aspinall"),
    ("PGS-TTA", "Tatsuro Taira"),
    ("PGS-UNV", "Umar Nurmagomedov"),
    ("PGS-WGS", "William Gomis"),
    ("PGS-YDS", "Yadong Song"),
])
print("  Pursuit of Greatness Signatures: 35 cards")

# Regalia Relic Signatures (61 cards, /99)
make_insert_set("Regalia Relic Signatures", AUTO_99_PARALLELS, [
    ("RRS-AAN", "Jamahal Hill"),
    ("RRS-AGO", "Alexa Grasso"),
    ("RRS-ALS", "Amanda Lemos"),
    ("RRS-APA", "Alexandre Pantoja"),
    ("RRS-APR", "Alex Pereira"),
    ("RRS-ASG", "Aljamain Sterling"),
    ("RRS-BAN", "Brendan Allen"),
    ("RRS-BDH", "Beneil Dariush"),
    ("RRS-BMO", "Brandon Moreno"),
    ("RRS-BOA", "Brian Ortega"),
    ("RRS-BRL", "Brandon Royval"),
    ("RRS-COA", "Charles Oliveira"),
    ("RRS-CUG", "Carlos Ulberg"),
    ("RRS-DDP", "Dricus Du Plessis"),
    ("RRS-DDR", "Drew Dober"),
    ("RRS-DPR", "Dustin Poirier"),
    ("RRS-GBS", "Gilbert Burns"),
    ("RRS-GCE", "Giga Chikadze"),
    ("RRS-GRS", "Gregory Rodrigues"),
    ("RRS-IMV", "Islam Makhachev"),
    ("RRS-JGE", "Justin Gaethje"),
    ("RRS-JPR", "Joe Pyfer"),
    ("RRS-JSE", "Jack Shore"),
    ("RRS-JTR", "Jalin Turner"),
    ("RRS-JWR", "Johnny Walker"),
    ("RRS-KCA", "Katlyn Cerminara"),
    ("RRS-KHD", "Kevin Holland"),
    ("RRS-KKF", "Kai Kara-France"),
    ("RRS-LES", "Leon Edwards"),
    ("RRS-LGZ", "Loopy Godinez"),
    ("RRS-MAV", "Magomed Ankalaev"),
    ("RRS-MBR", "Maycee Barber"),
    ("RRS-MCR", "Michael Chandler"),
    ("RRS-MDI", "Merab Dvalishvili"),
    ("RRS-MDN", "Mackenzie Dern"),
    ("RRS-MFT", "Manon Fiorot"),
    ("RRS-MMC", "Molly McCann"),
    ("RRS-MMT", "Mike Malott"),
    ("RRS-PMZ", "Pedro Munhoz"),
    ("RRS-RFT", "Rob Font"),
    ("RRS-RFV", "Rafael Fiziev"),
    ("RRS-RNS", "Rose Namajunas"),
    ("RRS-RPN", "Raquel Pennington"),
    ("RRS-RRS", "Raul Rosas"),
    ("RRS-RWR", "Robert Whittaker"),
    ("RRS-SBY", "Sean Brady"),
    ("RRS-SMC", "Stipe Miocic"),
    ("RRS-SPH", "Sergei Pavlovich"),
    ("RRS-SRV", "Shavkat Rakhmonov"),
    ("RRS-STN", "Stephen Thompson"),
    ("RRS-TFN", "Tony Ferguson"),
    ("RRS-TPO", "Tyson Pedro"),
    ("RRS-TTA", "Tatsuro Taira"),
    ("RRS-TTU", "Tai Tuivasa"),
    ("RRS-UNV", "Umar Nurmagomedov"),
    ("RRS-VLE", "Vicente Luque"),
    ("RRS-VOR", "Volkan Oezdemir"),
    ("RRS-YDS", "Yadong Song"),
    ("RRS-YRZ", "Yair Rodríguez"),
    ("RRS-YXN", "Yan Xiaonan"),
    ("RRS-ZWI", "Zhang Weili"),
])
print("  Regalia Relic Signatures: 61 cards")

# Rookie Autographs (23 cards, /99, all RC)
make_insert_set("Rookie Autographs", AUTO_99_PARALLELS, [
    ("RA-AP", "Armen Petrosyan RC"),
    ("RA-AZ", "Aiemann Zahabi RC"),
    ("RA-BH", "Brady Hiestand RC"),
    ("RA-BK", "Brad Katona RC"),
    ("RA-BS", "Benoit Saint Denis RC"),
    ("RA-CC", "Chelsea Chandler RC"),
    ("RA-CS", "Cameron Saaiman RC"),
    ("RA-CW", "Choi SeungWoo RC"),
    ("RA-DB", "Da'Mon Blackshear RC"),
    ("RA-DL", "Diego Lopes RC"),
    ("RA-IL", "Iasmin Lucindo RC"),
    ("RA-IM", "Inoue Mizuki RC"),
    ("RA-JH", "Jake Hadley RC"),
    ("RA-JJ", "Jasmine Jasudavicius RC"),
    ("RA-JP", "Jonny Parsons RC"),
    ("RA-JT", "Junior Tafa RC"),
    ("RA-MC", "Melquizael Conceição RC"),
    ("RA-MK", "Manel Kape RC"),
    ("RA-ND", "Natalia Cristina da Silva RC"),
    ("RA-OO", "Ode Osbourne RC"),
    ("RA-TG", "Themba Gorimbo RC"),
    ("RA-WG", "William Gomis RC"),
    ("RA-YJ", "Yazmin Jauregui RC"),
])
print("  Rookie Autographs: 23 cards")

# Rookie Relic Autographs (26 cards, /99, all RC)
make_insert_set("Rookie Relic Autographs", AUTO_99_PARALLELS, [
    ("RRA-AMP", "Armen Petrosyan RC"),
    ("RRA-ANZ", "Aiemann Zahabi RC"),
    ("RRA-BDK", "Brad Katona RC"),
    ("RRA-BNF", "Brunno Ferreira RC"),
    ("RRA-BSD", "Benoit Saint Denis RC"),
    ("RRA-CNS", "Cameron Saaiman RC"),
    ("RRA-CSC", "Chelsea Chandler RC"),
    ("RRA-CSW", "Choi SeungWoo RC"),
    ("RRA-DOL", "Diego Lopes RC"),
    ("RRA-INL", "Iasmin Lucindo RC"),
    ("RRA-JHQ", "Josh Quinlan RC"),
    ("RRA-JKH", "Jake Hadley RC"),
    ("RRA-JKJ", "Jack Jenkins RC"),
    ("RRA-JMJ", "Jasmine Jasudavicius RC"),
    ("RRA-JNP", "Jonny Parsons RC"),
    ("RRA-JNT", "Junior Tafa RC"),
    ("RRA-KHN", "Kayla Harrison RC"),
    ("RRA-MNK", "Manel Kape RC"),
    ("RRA-MPE", "Michael Page RC"),
    ("RRA-MQC", "Melquizael Conceição RC"),
    ("RRA-NCS", "Natalia Cristina da Silva RC"),
    ("RRA-ODO", "Ode Osbourne RC"),
    ("RRA-SRM", "Sharaputdin Magomedov RC"),
    ("RRA-TAG", "Themba Gorimbo RC"),
    ("RRA-WMG", "William Gomis RC"),
    ("RRA-YZJ", "Yazmin Jauregui RC"),
])
print("  Rookie Relic Autographs: 26 cards")

# Royalty Relic Signatures (35 cards, /99)
make_insert_set("Royalty Relic Signatures", AUTO_99_PARALLELS, [
    ("RYS-AAN", "Arnold Allen"),
    ("RYS-AGO", "Ikram Aliskerov"),
    ("RYS-ASH", "Anthony Smith"),
    ("RYS-AVI", "Alexander Volkanovski"),
    ("RYS-BBE", "Bryan Battle"),
    ("RYS-BMD", "Belal Muhammad"),
    ("RYS-CBO", "Caio Borralho"),
    ("RYS-CGE", "Ciryl Gane"),
    ("RYS-CSN", "Cory Sandhagen"),
    ("RYS-CUG", "Carlos Ulberg"),
    ("RYS-DCZ", "Dominick Cruz"),
    ("RYS-DRS", "Dominick Reyes"),
    ("RYS-GCE", "Giga Chikadze"),
    ("RYS-GNL", "Geoff Neal"),
    ("RYS-IAA", "Irene Aldana"),
    ("RYS-IAD", "Israel Adesanya"),
    ("RYS-IGE", "Dan Ige"),
    ("RYS-JDM", "Erin Blanchfield"),
    ("RYS-JPR", "Joe Pyfer"),
    ("RYS-JWS", "Jeremiah Wells"),
    ("RYS-KCV", "Alexander Volkov"),
    ("RYS-MGT", "Mateusz Gamrot"),
    ("RYS-MHY", "Max Holloway"),
    ("RYS-MNU", "Matheus Nicolau"),
    ("RYS-MTA", "Marcin Tybura"),
    ("RYS-NMY", "Neil Magny"),
    ("RYS-PCA", "Rafael Fiziev"),
    ("RYS-RDA", "Rafael Dos Anjos"),
    ("RYS-RRS", "Raul Rosas"),
    ("RYS-RSN", "Ryan Spann"),
    ("RYS-SSC", "Serghei Spivac"),
    ("RYS-TAL", "Tom Aspinall"),
    ("RYS-TFN", "Tony Ferguson"),
    ("RYS-TRI", "Tabatha Ricci"),
    ("RYS-VSO", "Valentina Shevchenko"),
])
print("  Royalty Relic Signatures: 35 cards")

# Superior Relic Signatures (25 cards, /99)
make_insert_set("Superior Relic Signatures", AUTO_99_PARALLELS, [
    ("SRS-AA", "Amir Albazi"),
    ("SRS-AI", "Andrei Arlovski"),
    ("SRS-AR", "Aleksandar Rakic"),
    ("SRS-AV", "Khamzat Chimaev"),
    ("SRS-BB", "Bruce Buffer"),
    ("SRS-CC", "Colby Covington"),
    ("SRS-CK", "Calvin Kattar"),
    ("SRS-DH", "Daniel Hooker"),
    ("SRS-DP", "Dustin Poirier"),
    ("SRS-HC", "Henry Cejudo"),
    ("SRS-HH", "Holly Holm"),
    ("SRS-IG", "Ian Machado Garry"),
    ("SRS-JA", "Jailton Malhadinho"),
    ("SRS-JB", "Jan Błachowicz"),
    ("SRS-JE", "Josh Emmett"),
    ("SRS-JI", "Jiri Prochazka"),
    ("SRS-JJ", "Joanna Jędrzejczyk"),
    ("SRS-JP", "Julianna Peña"),
    ("SRS-JR", "Jair Rozenstruik"),
    ("SRS-MV", "Marvin Vettori"),
    ("SRS-NL", "Natan Levy"),
    ("SRS-NM", "Neil Magny"),
    ("SRS-PP", "Paddy Pimblett"),
    ("SRS-RD", "Roman Dolidze"),
    ("SRS-SO", "Sean O'Malley"),
])
print("  Superior Relic Signatures: 25 cards")

# Superior Signatures (34 cards, /99)
make_insert_set("Superior Signatures", AUTO_99_PARALLELS, [
    ("SS-AAI", "Amir Albazi"),
    ("SS-AAN", "Arnold Allen"),
    ("SS-ATN", "Arman Tsarukyan"),
    ("SS-BAN", "Brendan Allen"),
    ("SS-BOA", "Brian Ortega"),
    ("SS-CSJ", "Chan Sung Jung"),
    ("SS-CSN", "Chael Sonnen"),
    ("SS-DCE", "Donald Cerrone"),
    ("SS-DCZ", "Dominick Cruz"),
    ("SS-DDR", "Drew Dober"),
    ("SS-DHN", "Dan Henderson"),
    ("SS-DIG", "Dan Ige"),
    ("SS-GRS", "Gregory Rodrigues"),
    ("SS-GTA", "Glover Teixeira"),
    ("SS-ITA", "Ilia Topuria"),
    ("SS-JET", "Josh Emmett"),
    ("SS-JPR", "Jens Pulver"),
    ("SS-JQN", "Josh Quinlan"),
    ("SS-JSE", "Jack Shore"),
    ("SS-JTR", "Jalin Turner"),
    ("SS-JWS", "Jeremiah Wells"),
    ("SS-LMA", "Lyoto Machida"),
    ("SS-LRD", "Luke Rockhold"),
    ("SS-MMT", "Mike Malott"),
    ("SS-MNU", "Matheus Nicolau"),
    ("SS-PMZ", "Pedro Munhoz"),
    ("SS-RES", "Rashad Evans"),
    ("SS-RFT", "Rob Font"),
    ("SS-RSN", "Ryan Spann"),
    ("SS-RWR", "Robert Whittaker"),
    ("SS-TPO", "Tyson Pedro"),
    ("SS-TRI", "Tabatha Ricci"),
    ("SS-TWY", "Tyron Woodley"),
    ("SS-VOR", "Volkan Oezdemir"),
])
print("  Superior Signatures: 34 cards")

# Triumph Relic Signatures (26 cards, /99)
make_insert_set("Triumph Relic Signatures", AUTO_99_PARALLELS, [
    ("TRS-AAI", "Andrei Arlovski"),
    ("TRS-APA", "Alexandre Pantoja"),
    ("TRS-ARC", "Aleksandar Rakic"),
    ("TRS-BAN", "Brendan Allen"),
    ("TRS-BMD", "Belal Muhammad"),
    ("TRS-BMO", "Brandon Moreno"),
    ("TRS-BRL", "Brandon Royval"),
    ("TRS-CSN", "Cory Sandhagen"),
    ("TRS-EBD", "Erin Blanchfield"),
    ("TRS-HCO", "Henry Cejudo"),
    ("TRS-IAA", "Irene Aldana"),
    ("TRS-IAV", "Ikram Aliskerov"),
    ("TRS-JAA", "Jailton Malhadinho"),
    ("TRS-JHL", "Jamahal Hill"),
    ("TRS-JWR", "Johnny Walker"),
    ("TRS-KCA", "Katlyn Cerminara"),
    ("TRS-KHD", "Kevin Holland"),
    ("TRS-MAV", "Magomed Ankalaev"),
    ("TRS-MDI", "Merab Dvalishvili"),
    ("TRS-MMC", "Molly McCann"),
    ("TRS-RNS", "Rose Namajunas"),
    ("TRS-RPN", "Raquel Pennington"),
    ("TRS-SPH", "Sergei Pavlovich"),
    ("TRS-TTA", "Tai Tuivasa"),
    ("TRS-UNV", "Umar Nurmagomedov"),
    ("TRS-VSO", "Valentina Shevchenko"),
])
print("  Triumph Relic Signatures: 26 cards")

# UFC Honors Autographs (11 cards, /25)
make_insert_set("UFC Honors Autographs", AUTO_25_PARALLELS, [
    ("UHA-AG", "Alexa Grasso"),
    ("UHA-CM", "Conor McGregor"),
    ("UHA-CO", "Charles Oliveira"),
    ("UHA-IA", "Israel Adesanya"),
    ("UHA-IM", "Islam Makhachev"),
    ("UHA-JG", "Justin Gaethje"),
    ("UHA-KC", "Khamzat Chimaev"),
    ("UHA-LE", "Leon Edwards"),
    ("UHA-MC", "Michael Chandler"),
    ("UHA-SO", "Sean O'Malley"),
    ("UHA-ZW", "Zhang Weili"),
])
print("  UFC Honors Autographs: 11 cards")

# Dual Autographs (21 cards, /25, co_players)
make_insert_set("Dual Autographs", AUTO_25_PARALLELS, [
    ("DA-CB", ["Gilbert Burns", "Khamzat Chimaev"]),
    ("DA-CM", ["Stipe Miocic", "Daniel Cormier"]),
    ("DA-GC", ["Justin Gaethje", "Michael Chandler"]),
    ("DA-GW", ["Alexa Grasso", "Zhang Weili"]),
    ("DA-HS", ["Max Holloway", "Chan Sung Jung"]),
    ("DA-LG", ["Forrest Griffin", "Chuck Liddell"]),
    ("DA-MR", ["Brandon Moreno", "Yair Rodríguez"]),
    ("DA-MV", ["Islam Makhachev", "Alexander Volkanovski"]),
    ("DA-NS", ["Valentina Shevchenko", "Amanda Nunes"]),
    ("DA-PA", ["Israel Adesanya", "Dricus Du Plessis"]),
    ("DA-PM", ["Paddy Pimblett", "Molly McCann"]),
    ("DA-PP", ["Julianna Peña", "Raquel Pennington"]),
    ("DA-RH", ["Mauricio Rua", "Dan Henderson"]),
    ("DA-SD", ["Aljamain Sterling", "Merab Dvalishvili"]),
    ("DA-SH", ["Georges St-Pierre", "Matt Hughes"]),
    ("DA-SS", ["Frank Shamrock", "Ken Shamrock"]),
    ("DA-TP", ["Alex Pereira", "Glover Teixeira"]),
    ("DA-TT", ["Tyson Pedro", "Tai Tuivasa"]),
    ("DA-WB", ["Bruce Buffer", "Dana White"]),
    ("DA-WN", ["Zhang Weili", "Rose Namajunas"]),
    ("DA-WT", ["Chris Weidman", "Stephen Thompson"]),
], is_multi=True)
print("  Dual Autographs: 21 cards")

# Triple Autographs (5 cards, /25, co_players)
make_insert_set("Triple Autographs", AUTO_25_PARALLELS, [
    ("TA-APS", ["Serghei Spivac", "Tom Aspinall", "Sergei Pavlovich"]),
    ("TA-BFB", ["Erin Blanchfield", "Manon Fiorot", "Maycee Barber"]),
    ("TA-MNU", ["Islam Makhachev", "Umar Nurmagomedov", "Tagir Ulanbekov"]),
    ("TA-SSN", ["Daniel Cormier", "Georges St-Pierre", "Khabib Nurmagomedov"]),
    ("TA-WBC", ["Daniel Cormier", "Dana White", "Bruce Buffer"]),
], is_multi=True)
print("  Triple Autographs: 5 cards")

# Dual Fighter Relic Autograph Books (8 cards, co_players where applicable)
# DRA-SD is a single fighter (Tatiana Suarez)
dra_is_id = create_insert_set(set_id, "Dual Fighter Relic Autograph Books")
create_parallel(dra_is_id, "Green", 5)
create_parallel(dra_is_id, "Platinum", 1)

dra_multi = [
    ("DRA-AP", ["Tom Aspinall", "Paddy Pimblett"]),
    ("DRA-MS", ["Sharaputdin Magomedov", "Benoit Saint Denis"]),
    ("DRA-MT", ["Tatsuro Taira", "Muhammad Mokaev"]),
    ("DRA-OC", ["Michael Chandler", "Charles Oliveira"]),
    ("DRA-OV", ["Alexander Volkanovski", "Sean O'Malley"]),
    ("DRA-RE", ["Shavkat Rakhmonov", "Movsar Evloev"]),
    ("DRA-XZ", ["Yan Xiaonan", "Zhang Weili"]),
]
add_multi_cards(dra_is_id, "Dual Fighter Relic Autograph Books", dra_multi)
# Single fighter card
name, is_rc = normalize_name("Tatiana Suarez")
pid = get_or_create_player(set_id, name)
app_id = create_appearance(pid, dra_is_id, "DRA-SD", is_rc)
appearance_player_map[app_id] = pid
print("  Dual Fighter Relic Autograph Books: 8 cards")

# ────────────────────────────────────────────────────────────────────────────────
# PLAIN INSERT SETS (4 sets)
# ────────────────────────────────────────────────────────────────────────────────

# The Coronation (14 cards, no parallels)
make_insert_set("The Coronation", [], [
    ("TC-AG", "Alexa Grasso"),
    ("TC-AN", "Amanda Nunes"),
    ("TC-AP", "Alex Pereira"),
    ("TC-AV", "Alexander Volkanovski"),
    ("TC-CM", "Conor McGregor"),
    ("TC-CO", "Charles Oliveira"),
    ("TC-GS", "Georges St-Pierre"),
    ("TC-IA", "Israel Adesanya"),
    ("TC-IM", "Islam Makhachev"),
    ("TC-JG", "Justin Gaethje"),
    ("TC-KN", "Khabib Nurmagomedov"),
    ("TC-LE", "Leon Edwards"),
    ("TC-SO", "Sean O'Malley"),
    ("TC-ZW", "Zhang Weili"),
])
print("  The Coronation: 14 cards")

# Royal Decree (28 cards, no parallels)
make_insert_set("Royal Decree", [], [
    ("RD-AG", "Alexa Grasso"),
    ("RD-AN", "Amanda Nunes"),
    ("RD-AP", "Alex Pereira"),
    ("RD-AS", "Aljamain Sterling"),
    ("RD-AV", "Alexander Volkanovski"),
    ("RD-BM", "Brandon Moreno"),
    ("RD-CL", "Chuck Liddell"),
    ("RD-CM", "Conor McGregor"),
    ("RD-CO", "Charles Oliveira"),
    ("RD-DC", "Daniel Cormier"),
    ("RD-DP", "Dustin Poirier"),
    ("RD-HC", "Henry Cejudo"),
    ("RD-HH", "Holly Holm"),
    ("RD-IM", "Islam Makhachev"),
    ("RD-JG", "Justin Gaethje"),
    ("RD-JP", "Jiri Prochazka"),
    ("RD-KN", "Khabib Nurmagomedov"),
    ("RD-LE", "Leon Edwards"),
    ("RD-MB", "Michael Bisping"),
    ("RD-MC", "Michael Chandler"),
    ("RD-MD", "Merab Dvalishvili"),
    ("RD-MH", "Max Holloway"),
    ("RD-RG", "Royce Gracie"),
    ("RD-RN", "Rose Namajunas"),
    ("RD-SM", "Stipe Miocic"),
    ("RD-SO", "Sean O'Malley"),
    ("RD-VS", "Valentina Shevchenko"),
    ("RD-ZW", "Zhang Weili"),
])
print("  Royal Decree: 28 cards")

# The Time Is Now (12 cards, no parallels)
make_insert_set("The Time Is Now", [], [
    ("TIN-AT", "Arman Tsarukyan"),
    ("TIN-DD", "Dricus Du Plessis"),
    ("TIN-EB", "Erin Blanchfield"),
    ("TIN-IT", "Ilia Topuria"),
    ("TIN-KC", "Khamzat Chimaev"),
    ("TIN-MA", "Magomed Ankalaev"),
    ("TIN-MF", "Manon Fiorot"),
    ("TIN-PP", "Paddy Pimblett"),
    ("TIN-SP", "Sergei Pavlovich"),
    ("TIN-SR", "Shavkat Rakhmonov"),
    ("TIN-TA", "Tom Aspinall"),
    ("TIN-UN", "Umar Nurmagomedov"),
])
print("  The Time Is Now: 12 cards")

# Liquid Silver (10 cards, Gold parallel unnumbered)
make_insert_set("Liquid Silver", [("Gold", None)], [
    ("LS-1", "Sean O'Malley"),
    ("LS-2", "Conor McGregor"),
    ("LS-3", "Jon Jones"),
    ("LS-4", "Max Holloway"),
    ("LS-5", "Khabib Nurmagomedov"),
    ("LS-6", "Valentina Shevchenko"),
    ("LS-7", "Amanda Nunes"),
    ("LS-8", "Bo Nickal"),
    ("LS-9", "Ilia Topuria"),
    ("LS-10", "Alex Pereira"),
])
print("  Liquid Silver: 10 cards")

# ────────────────────────────────────────────────────────────────────────────────
# MEMORABILIA/RELIC SETS (5 sets)
# ────────────────────────────────────────────────────────────────────────────────

# Prodigious Pairings (20 cards, /99, co_players)
make_insert_set("Prodigious Pairings", RELIC_99_PARALLELS, [
    ("PSP-1", ["Michael Chandler", "Dustin Poirier"]),
    ("PSP-2", ["Max Holloway", "Justin Gaethje"]),
    ("PSP-3", ["Zhang Weili", "Joanna Jędrzejczyk"]),
    ("PSP-4", ["Tom Aspinall", "Leon Edwards"]),
    ("PSP-5", ["Magomed Ankalaev", "Umar Nurmagomedov"]),
    ("PSP-6", ["Diego Lopes", "Benoit Saint Denis"]),
    ("PSP-7", ["Robert Whittaker", "Jack Della Maddalena"]),
    ("PSP-8", ["Charles Oliveira", "José Aldo"]),
    ("PSP-9", ["Natalia Cristina da Silva", "Yazmin Jauregui"]),
    ("PSP-10", ["Alex Pereira", "Israel Adesanya"]),
    ("PSP-11", ["Paddy Pimblett", "Ian Machado Garry"]),
    ("PSP-12", ["Aljamain Sterling", "Merab Dvalishvili"]),
    ("PSP-13", ["Michael Morales", "Marlon Vera"]),
    ("PSP-14", ["Manon Fiorot", "Alexa Grasso"]),
    ("PSP-15", ["Jessica Andrade", "Tatiana Suarez"]),
    ("PSP-16", ["Brandon Moreno", "Deiveson Figueiredo"]),
    ("PSP-17", ["Julianna Peña", "Amanda Nunes"]),
    ("PSP-18", ["Michael Page", "Muhammad Mokaev"]),
    ("PSP-19", ["Taila Santos", "Maycee Barber"]),
    ("PSP-20", ["Jan Błachowicz", "Marcin Tybura"]),
], is_multi=True)
print("  Prodigious Pairings: 20 cards")

# Regalia Relics (74 cards, /99)
make_insert_set("Regalia Relics", RELIC_99_PARALLELS, [
    ("RAR-1", "Islam Makhachev"),
    ("RAR-2", "Stephen Thompson"),
    ("RAR-3", "Dominick Cruz"),
    ("RAR-4", "Volkan Oezdemir"),
    ("RAR-5", "Nikita Krylov"),
    ("RAR-6", "King Green"),
    ("RAR-7", "Rob Font"),
    ("RAR-8", "Jessica Andrade"),
    ("RAR-9", "Vicente Luque"),
    ("RAR-10", "Joe Pyfer"),
    ("RAR-11", "Natan Levy"),
    ("RAR-12", "Dominick Reyes"),
    ("RAR-13", "Jair Rozenstruik"),
    ("RAR-14", "Mayra Bueno"),
    ("RAR-15", "Dan Ige"),
    ("RAR-16", "Paul Craig"),
    ("RAR-17", "Ciryl Gane"),
    ("RAR-18", "Tatsuro Taira"),
    ("RAR-19", "Jack Shore"),
    ("RAR-20", "Amir Albazi"),
    ("RAR-21", "Matheus Nicolau"),
    ("RAR-22", "Cory Sandhagen"),
    ("RAR-23", "Yadong Song"),
    ("RAR-24", "Giga Chikadze"),
    ("RAR-25", "Alexander Volkov"),
    ("RAR-26", "Marvin Vettori"),
    ("RAR-27", "Curtis Blaydes"),
    ("RAR-28", "Rafael Fiziev"),
    ("RAR-29", "Deiveson Figueiredo"),
    ("RAR-30", "Marcin Tybura"),
    ("RAR-31", "Sean O'Malley"),
    ("RAR-32", "Katlyn Cerminara"),
    ("RAR-33", "Pedro Munhoz"),
    ("RAR-34", "Colby Covington"),
    ("RAR-35", "Josh Emmett"),
    ("RAR-36", "Chan Sung Jung"),
    ("RAR-37", "Mike Malott"),
    ("RAR-38", "Arnold Allen"),
    ("RAR-39", "Roman Dolidze"),
    ("RAR-40", "Loopy Godinez"),
    ("RAR-41", "Calvin Kattar"),
    ("RAR-42", "Tyson Pedro"),
    ("RAR-43", "Jim Miller"),
    ("RAR-44", "Bryan Battle"),
    ("RAR-45", "Kai Kara-France"),
    ("RAR-46", "Tatiana Suarez"),
    ("RAR-47", "Jalin Turner"),
    ("RAR-48", "Drew Dober"),
    ("RAR-49", "Manel Kape"),
    ("RAR-50", "Gregory Rodrigues"),
    ("RAR-51", "Andrei Arlovski"),
    ("RAR-52", "Rafael Dos Anjos"),
    ("RAR-53", "Daniel Hooker"),
    ("RAR-54", "Serghei Spivac"),
    ("RAR-55", "Carlos Ulberg"),
    ("RAR-56", "Mateusz Gamrot"),
    ("RAR-57", "Taila Santos"),
    ("RAR-58", "Brendan Allen"),
    ("RAR-59", "Geoff Neal"),
    ("RAR-60", "Belal Muhammad"),
    ("RAR-61", "Kayla Harrison"),
    ("RAR-62", "Neil Magny"),
    ("RAR-63", "Beneil Dariush"),
    ("RAR-64", "Karolina Kowalkiewicz"),
    ("RAR-65", "Anthony Smith"),
    ("RAR-66", "Jailton Malhadinho"),
    ("RAR-67", "Ryan Spann"),
    ("RAR-68", "Jeremiah Wells"),
    ("RAR-69", "Alexander Volkanovski"),
    ("RAR-70", "Jamahal Hill"),
    ("RAR-71", "Caio Borralho"),
    ("RAR-72", "Movsar Evloev"),
    ("RAR-73", "Erin Blanchfield"),
    ("RAR-74", "Raul Rosas"),
])
print("  Regalia Relics: 74 cards")

# Relic Jewels (30 cards, /99)
make_insert_set("Relic Jewels", RELIC_99_PARALLELS, [
    ("RCJ-1", "Stephen Thompson"),
    ("RCJ-2", "Curtis Blaydes"),
    ("RCJ-3", "Islam Makhachev"),
    ("RCJ-4", "Tom Aspinall"),
    ("RCJ-5", "Joanna Jędrzejczyk"),
    ("RCJ-6", "Alexander Volkanovski"),
    ("RCJ-7", "Holly Holm"),
    ("RCJ-8", "Sean O'Malley"),
    ("RCJ-9", "Israel Adesanya"),
    ("RCJ-10", "Amanda Nunes"),
    ("RCJ-11", "Justin Gaethje"),
    ("RCJ-12", "Shavkat Rakhmonov"),
    ("RCJ-13", "Leon Edwards"),
    ("RCJ-14", "Charles Oliveira"),
    ("RCJ-15", "Jiri Prochazka"),
    ("RCJ-16", "Henry Cejudo"),
    ("RCJ-17", "Tony Ferguson"),
    ("RCJ-18", "Dominick Cruz"),
    ("RCJ-19", "Max Holloway"),
    ("RCJ-20", "Chan Sung Jung"),
    ("RCJ-21", "Valentina Shevchenko"),
    ("RCJ-22", "José Aldo"),
    ("RCJ-23", "Umar Nurmagomedov"),
    ("RCJ-24", "Alex Pereira"),
    ("RCJ-25", "Rose Namajunas"),
    ("RCJ-26", "Michael Chandler"),
    ("RCJ-27", "Dustin Poirier"),
    ("RCJ-28", "Zhang Weili"),
    ("RCJ-29", "Alexandre Pantoja"),
    ("RCJ-30", "Jim Miller"),
])
print("  Relic Jewels: 30 cards")

# Rookie Jumbo Relics (26 cards, /99, all RC)
make_insert_set("Rookie Jumbo Relics", RELIC_99_PARALLELS, [
    ("RJR-1", "Diego Lopes RC"),
    ("RJR-2", "Yazmin Jauregui RC"),
    ("RJR-3", "Choi SeungWoo RC"),
    ("RJR-4", "Themba Gorimbo RC"),
    ("RJR-5", "Manel Kape RC"),
    ("RJR-6", "Michael Page RC"),
    ("RJR-7", "Jake Hadley RC"),
    ("RJR-8", "Chelsea Chandler RC"),
    ("RJR-9", "Natalia Cristina da Silva RC"),
    ("RJR-10", "Benoit Saint Denis RC"),
    ("RJR-11", "Jasmine Jasudavicius RC"),
    ("RJR-12", "Robelis Despaigne RC"),
    ("RJR-13", "Brady Hiestand RC"),
    ("RJR-14", "Fernando Padilla RC"),
    ("RJR-15", "Brad Katona RC"),
    ("RJR-16", "Elves Brener RC"),
    ("RJR-17", "William Gomis RC"),
    ("RJR-18", "Nuerdanbieke Shayilan RC"),
    ("RJR-19", "Cameron Saaiman RC"),
    ("RJR-20", "Melquizael Conceição RC"),
    ("RJR-21", "Iasmin Lucindo RC"),
    ("RJR-22", "Armen Petrosyan RC"),
    ("RJR-23", "Jack Jenkins RC"),
    ("RJR-24", "Brunno Ferreira RC"),
    ("RJR-25", "Junior Tafa RC"),
    ("RJR-26", "Luana Carolina RC"),
])
print("  Rookie Jumbo Relics: 26 cards")

# Star Relics (50 cards, /99)
make_insert_set("Star Relics", RELIC_99_PARALLELS, [
    ("SRR-1", "Aleksandar Rakic"),
    ("SRR-2", "Marlon Vera"),
    ("SRR-3", "Jiri Prochazka"),
    ("SRR-4", "Carla Esparza"),
    ("SRR-5", "Gilbert Burns"),
    ("SRR-6", "Rose Namajunas"),
    ("SRR-7", "Magomed Ankalaev"),
    ("SRR-8", "Brian Ortega"),
    ("SRR-9", "Yair Rodríguez"),
    ("SRR-10", "Kevin Holland"),
    ("SRR-11", "Shavkat Rakhmonov"),
    ("SRR-12", "Brandon Moreno"),
    ("SRR-13", "Colby Covington"),
    ("SRR-14", "Jack Della Maddalena"),
    ("SRR-15", "Tabatha Ricci"),
    ("SRR-16", "Miesha Tate"),
    ("SRR-17", "Tai Tuivasa"),
    ("SRR-18", "Mackenzie Dern"),
    ("SRR-19", "Amanda Lemos"),
    ("SRR-20", "Ian Machado Garry"),
    ("SRR-21", "Chris Weidman"),
    ("SRR-22", "Robert Whittaker"),
    ("SRR-23", "Jan Błachowicz"),
    ("SRR-24", "Henry Cejudo"),
    ("SRR-25", "Michael Morales"),
    ("SRR-26", "Stipe Miocic"),
    ("SRR-27", "Movsar Evloev"),
    ("SRR-28", "Johnny Walker"),
    ("SRR-29", "Brandon Royval"),
    ("SRR-30", "Luke Rockhold"),
    ("SRR-31", "Erin Blanchfield"),
    ("SRR-32", "Muhammad Mokaev"),
    ("SRR-33", "Yan Xiaonan"),
    ("SRR-34", "Julianna Peña"),
    ("SRR-35", "Tony Ferguson"),
    ("SRR-36", "Jamahal Hill"),
    ("SRR-37", "Raul Rosas"),
    ("SRR-38", "Aljamain Sterling"),
    ("SRR-39", "Maycee Barber"),
    ("SRR-40", "Raquel Pennington"),
    ("SRR-41", "Alexa Grasso"),
    ("SRR-42", "Molly McCann"),
    ("SRR-43", "Belal Muhammad"),
    ("SRR-44", "Valentina Shevchenko"),
    ("SRR-45", "Merab Dvalishvili"),
    ("SRR-46", "Calvin Kattar"),
    ("SRR-47", "Paddy Pimblett"),
    ("SRR-48", "Alexandre Pantoja"),
    ("SRR-49", "Manon Fiorot"),
    ("SRR-50", "Rafael Dos Anjos"),
])
print("  Star Relics: 50 cards")

# ────────────────────────────────────────────────────────────────────────────────
# COMPUTE PLAYER STATS
# ────────────────────────────────────────────────────────────────────────────────

print("\nComputing player stats...")

cur.execute("SELECT id FROM players WHERE set_id = ?", (set_id,))
player_ids = [r[0] for r in cur.fetchall()]

for pid in player_ids:
    # Get all appearances for this player
    cur.execute(
        """SELECT pa.id, pa.insert_set_id
           FROM player_appearances pa
           WHERE pa.player_id = ?""",
        (pid,),
    )
    appearances = cur.fetchall()

    # Count distinct insert sets
    insert_set_ids = set(a[1] for a in appearances)
    insert_set_count = len(insert_set_ids)

    # For each appearance, count: 1 base card + number of parallels for that insert set
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
