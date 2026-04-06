"""
Parser for 2025 Topps Chrome Deadpool.

sport: Entertainment, league: Marvel, season: 2025, tier: Chrome
No is_rookie tagging (all False).
Character names as "player" field.
Actor names on autograph cards stored in subset_tag.
Dual autographs, Cover Stars multi-char, Deadpool Reflections use co_players logic.
Comic Book Artist Autographs: artist name as player.
Cover Stars: comic title as card name (stored in subset_tag), characters as players.
Skip Sketch Cards entirely.
Card FO-8 missing from 10005 Fire.
Card NC-7 missing from Best Bubs.
"""

from __future__ import annotations
import json


SET_NAME = "2025 Topps Chrome Deadpool"
SPORT = "Entertainment"
SEASON = "2025"
LEAGUE = "Marvel"


def make_parallels(items: list[tuple[str, int | None]]) -> list[dict]:
    return [{"name": n, "print_run": pr} for n, pr in items]


# ── Parallel definitions ─────────────────────────────────────────────────────

BASE_PARALLELS = make_parallels([
    ("Refractor", None),
    ("Prism Refractor", None),
    ("Mini Diamonds", None),
    ("Yellow Wave", 399),
    ("Pink Shimmer", 299),
    ("Purple Mini Diamonds", 250),
    ("Purple Wave", 250),
    ("Aqua Refractor", 199),
    ("Green/Aqua RayWave", 150),
    ("Blue Mini Diamonds", 125),
    ("Green Refractor", 99),
    ("Green Lava", 99),
    ("Dogpool Refractor", 75),
    ("Gold Lava", 50),
    ("Gold RayWave", 50),
    ("TVA Takeover", 40),
    ("Human Torch Lava", 39),
    ("Orange Shimmer", 25),
    ("Wolverine Yellow and Blue X-Fractor", 15),
    ("Black Refractor", 10),
    ("Black Lava", 10),
    ("Deadpool Red and Black Wave", 5),
    ("Red Refractor", 5),
    ("Superfractor", 1),
])

CHROME_AUTO_PARALLELS = make_parallels([
    ("Aqua Refractor", 199),
    ("Green/Aqua RayWave", 150),
    ("Green Refractor", 99),
    ("Dogpool Refractor", 75),
    ("Gold RayWave", 50),
    ("Human Torch Lava", 39),
    ("Orange Shimmer", 25),
    ("Wolverine Yellow and Blue X-Fractor", 15),
    ("Black Refractor", 10),
    ("Deadpool Red and Black Wave", 5),
    ("Red Refractor", 5),
    ("Superfractor", 1),
])

BEST_BUBS_AUTO_PARALLELS = make_parallels([
    ("Orange Shimmer", 25),
    ("Wolverine Yellow and Blue X-Fractor", 15),
    ("Black Refractor", 10),
    ("Deadpool Red and Black Wave", 5),
    ("Red Refractor", 5),
    ("Superfractor", 1),
])

ON_CARD_DUAL_PARALLELS = make_parallels([
    ("Black Refractor", 10),
    ("Red Refractor", 5),
    ("Superfractor", 1),
])

CHROME_DUAL_AUTO_PARALLELS = make_parallels([
    ("Gold RayWave", 50),
    ("Human Torch Lava", 39),
    ("Orange Shimmer", 25),
    ("Wolverine Yellow and Blue X-Fractor", 15),
    ("Black Refractor", 10),
    ("Deadpool Red and Black Wave", 5),
    ("Red Refractor", 5),
    ("Superfractor", 1),
])

MARVEL_ARTIST_AUTO_PARALLELS = make_parallels([
    ("Green Refractor", 99),
    ("Gold RayWave", 50),
    ("Human Torch Lava", 39),
    ("Orange Shimmer", 25),
    ("Wolverine Yellow and Blue X-Fractor", 15),
    ("Black Refractor", 10),
    ("Deadpool Red and Black Wave", 5),
    ("Red Refractor", 5),
    ("Superfractor", 1),
])

COMIC_BOOK_GOLD_PARALLELS = make_parallels([
    ("Gold RayWave", 50),
    ("Orange Shimmer", 25),
    ("Wolverine Yellow and Blue X-Fractor", 15),
    ("Black Refractor", 10),
    ("Deadpool Red and Black Wave", 5),
    ("Red Refractor", 5),
    ("Superfractor", 1),
])

COVER_STARS_PARALLELS = COMIC_BOOK_GOLD_PARALLELS

WELL_YOU_GOT_PARALLELS = COMIC_BOOK_GOLD_PARALLELS

FUTURE_STARS_PARALLELS = COMIC_BOOK_GOLD_PARALLELS

TOPPS_ORIGINALS_PARALLELS = make_parallels([
    ("Orange Shimmer", 25),
    ("Wolverine Yellow and Blue X-Fractor", 15),
    ("Black Refractor", 10),
    ("Deadpool Red and Black Wave", 5),
    ("Red Refractor", 5),
    ("Superfractor", 1),
])

FIRE_PARALLELS = make_parallels([
    ("Wolverine Yellow and Blue X-Fractor", 15),
    ("Black Refractor", 10),
    ("Deadpool Red and Black Wave", 5),
    ("Red Refractor", 5),
    ("Superfractor", 1),
])

BEST_BUBS_PARALLELS = FIRE_PARALLELS

LOOKING_FOR_LOGAN_PARALLELS = FIRE_PARALLELS

INDESTRUCTIBLE_PARALLELS = make_parallels([
    ("Red Lazer", 5),
    ("Superfractor", 1),
])

DEADPOOL_REFLECTIONS_PARALLELS = make_parallels([
    ("Kaleidoscope", 25),
    ("Shimmer", 10),
    ("RayWave", 5),
    ("Superfractor", 1),
])

THE_VOID_PARALLELS = FIRE_PARALLELS


# ── Card data ─────────────────────────────────────────────────────────────────

# Base - Comic Accurate (20 cards)
BASE_COMIC_ACCURATE_RAW = [
    ("1", "Deadpool"), ("2", "Old Man Logan"), ("3", "Cable"), ("4", "Domino"),
    ("5", "Wolverine"), ("6", "Colossus"), ("7", "Sabretooth"), ("8", "Psylocke"),
    ("9", "Juggernaut"), ("10", "Gambit"), ("11", "Pyro"), ("12", "Toad"),
    ("13", "Lady Deathstrike"), ("14", "Blob"), ("15", "X-23"), ("16", "Weapon X"),
    ("17", "Elektra"), ("18", "Blade"), ("19", "Bullseye"), ("20", "Patch"),
]

# Base - Characters (26 cards)
BASE_CHARACTERS_RAW = [
    ("21", "Deadpool"), ("22", "Mr. Paradox"), ("23", "Peter"), ("24", "Headpool"),
    ("25", "Pyro"), ("26", "Negasonic Teenage Warhead"), ("27", "Ladypool"),
    ("28", "Dogpool"), ("29", "Happy Hogan"), ("30", "Wolverine"),
    ("31", "Wade Wilson"), ("32", "Blind Al"), ("33", "Juggernaut"),
    ("34", "Russian"), ("35", "B-15"), ("36", "Cowboypool"), ("37", "Welshpool"),
    ("38", "Kidpool"), ("39", "Babypool"), ("40", "Toad"), ("41", "Sabretooth"),
    ("42", "X-23"), ("43", "Dopinder"), ("44", "Shatterstar"), ("45", "Quill"),
    ("46", "Cassandra Nova"),
]

# Base - Multiverse And More (54 cards)
BASE_MULTIVERSE_RAW = [
    ("47", "The Adventure Begins"), ("48", "Searching for Logan"),
    ("49", "Minutemen In Pursuit"), ("50", "Hiding From The TVA"),
    ("51", "Deadpool Strikes Back"), ("52", "An All-Out Brawl"),
    ("53", "Taking Matters Into His Own Hands"), ("54", "Advanced Weaponry"),
    ("55", "Wade's Big Interview"), ("56", "The Scheming Mr. Paradox"),
    ("57", "The TVA Office"), ("58", "Fashion and Function"),
    ("59", "Enjoying His New Threads"), ("60", "Face-To-Face With The Hulk"),
    ("61", "Finding The Cavillrine"), ("62", "Deadpool Finds His Logan"),
    ("63", "Fleeing The TVA"), ("64", "First Tango With Wolverine"),
    ("65", "Patrolling The Void"), ("66", "The FantastiCar"),
    ("67", "A Fiery Entrance"), ("68", "Pyro's Fury"),
    ("69", "Fighting Fire With Fire"), ("70", "Magnet Trap"),
    ("71", "The Nefarious Cassandra Nova"), ("72", "Deadpool's Baby Knife"),
    ("73", "Dogpool Taking A Stroll"), ("74", "A Pool's Best Friend"),
    ("75", "Ready For Round 2"), ("76", "Aftermath"),
    ("77", "Waking Up In A Den of Rebels"), ("78", "A Reminder Of What You Are"),
    ("79", "Fracas In The Fortress"), ("80", "All Or Nothing"),
    ("81", "Unstoppable"), ("82", "Battle Prowess"),
    ("83", "Special Delivery"), ("84", "Caught In The Action"),
    ("85", "Subdued by Cassandra"), ("86", "The Coup Gone Wrong"),
    ("87", "Cassandra's Wrath"), ("88", "Into Logan's Mind"),
    ("89", "A Way Back"), ("90", "A Daring Escape"),
    ("91", "Cassandra Exits The Void"), ("92", "A Dire Situation"),
    ("93", "Standoff with Cowboypool"), ("94", "Mercenary Melee"),
    ("95", "Variant Madness"), ("96", "A Momentary Pause In Chaos"),
    ("97", "An Army of Two"), ("98", "Accessing The Time Ripper"),
    ("99", "Destroying All Timelines"), ("100", "Disrupting Cassandra's Plot"),
]

# Chrome Autographs (26 cards)
CHROME_AUTOS_RAW = [
    ("TC-AR", "Juggernaut", "Signed by Aaron W. Reed"),
    ("TC-AS", "Pyro", "Signed by Aaron Stanford"),
    ("TC-BC", "Russian", "Signed by Billy Clements"),
    ("TC-BH", "Negasonic Teenage Warhead", "Signed by Brianna Hildebrand"),
    ("TC-CS", "Bullseye", "Signed by Curtis Small"),
    ("TC-DK", "X-23", "Signed by Dafne Keen"),
    ("TC-DR", "Toad", "Signed by Daniel Medina Ramos"),
    ("TC-EC", "Cassandra Nova", "Signed by Emma Corrin"),
    ("TC-EM", "Azazel", "Signed by Eduardo Gago Muñoz"),
    ("TC-HC", "The Cavillrine", "Signed by Henry Cavill"),
    ("TC-HJ", "Wolverine", "Signed by Hugh Jackman"),
    ("TC-JB", "Cable", "Signed by Josh Brolin"),
    ("TC-JD", "TVA Tech", "Signed by James Dryden"),
    ("TC-JL", "Lady Deathstrike", "Signed by Jade Lye"),
    ("TC-KS", "Dopinder", "Signed by Karan Soni"),
    ("TC-LT", "Shatterstar", "Signed by Lewis Tan"),
    ("TC-LU", "Blind Al", "Signed by Leslie Uggams"),
    ("TC-NC", "Quill", "Signed by Nilly Cetin"),
    ("TC-NF", "Headpool", "Signed by Nathan Fillion"),
    ("TC-PM", "Welshpool", "Signed by Paul Mullin"),
    ("TC-RB", "Peter", "Signed by Rob Delaney"),
    ("TC-RR", "Deadpool", "Signed by Ryan Reynolds"),
    ("TC-SZ", "Colossus", "Signed by Stefan Kapičić"),
    ("TC-TC", "Bedlam", "Signed by Terry Crews"),
    ("TC-TM", "Sabretooth", "Signed by Tyler Mane"),
    ("TC-WB", "B-15", "Signed by Wunmi Mosaku"),
]

# Best Bubs Autographs (13 cards)
BEST_BUBS_AUTOS_RAW = [
    ("NA-AS", "Pyro", "Signed by Aaron Stanford"),
    ("NA-BH", "Negasonic Teenage Warhead", "Signed by Brianna Hildebrand"),
    ("NA-CE", "Johnny Storm", "Signed by Chris Evans"),
    ("NA-DK", "X-23", "Signed by Dafne Keen"),
    ("NA-EC", "Cassandra Nova", "Signed by Emma Corrin"),
    ("NA-HC", "The Cavillrine", "Signed by Henry Cavill"),
    ("NA-HJ", "Wolverine", "Signed by Hugh Jackman"),
    ("NA-KS", "Dopinder", "Signed by Karan Soni"),
    ("NA-LU", "Blind Al", "Signed by Leslie Uggams"),
    ("NA-NF", "Headpool", "Signed by Nathan Fillion"),
    ("NA-PM", "Welshpool", "Signed by Paul Mullin"),
    ("NA-RD", "Peter", "Signed by Rob Delaney"),
    ("NA-RR", "Deadpool", "Signed by Ryan Reynolds"),
]

# On-Card Dual Inscription Booklet (1 card, co_players)
ON_CARD_DUAL_RAW = [
    ("OC-RH", [("Wolverine", "Signed by Hugh Jackman and Ryan Reynolds"),
               ("Deadpool", "Signed by Hugh Jackman and Ryan Reynolds")]),
]

# Chrome Dual Autographs (9 cards, co_players)
CHROME_DUAL_AUTOS_RAW = [
    ("TD-AD", [("Toad", "Signed by Daniel Medina Ramos and Aaron Stanford"),
               ("Pyro", "Signed by Daniel Medina Ramos and Aaron Stanford")]),
    ("TD-AE", [("Cassandra Nova", "Signed by Emma Corrin and Aaron Stanford"),
               ("Pyro", "Signed by Emma Corrin and Aaron Stanford")]),
    ("TD-HD", [("Wolverine", "Signed by Hugh Jackman and Dafne Keen"),
               ("X-23", "Signed by Hugh Jackman and Dafne Keen")]),
    ("TD-HH", [("The Cavillrine", "Signed by Henry Cavill and Hugh Jackman"),
               ("Wolverine", "Signed by Henry Cavill and Hugh Jackman")]),
    ("TD-LK", [("Dopinder", "Signed by Karan Soni and Leslie Uggams"),
               ("Blind Al", "Signed by Karan Soni and Leslie Uggams")]),
    ("TD-LR", [("Blind Al", "Signed by Leslie Uggams and Rob Delaney"),
               ("Peter", "Signed by Leslie Uggams and Rob Delaney")]),
    ("TD-RC", [("Deadpool", "Signed by Ryan Reynolds and Henry Cavill"),
               ("The Cavillrine", "Signed by Ryan Reynolds and Henry Cavill")]),
    ("TD-RH", [("Deadpool", "Signed by Ryan Reynolds and Hugh Jackman"),
               ("Wolverine", "Signed by Ryan Reynolds and Hugh Jackman")]),
    ("TH-TA", [("Pyro", "Signed by Aaron Stanford and Tyler Mane"),
               ("Sabretooth", "Signed by Aaron Stanford and Tyler Mane")]),
]

# Marvel Comic Book Artist Autographs (6 cards)
MARVEL_ARTIST_AUTOS_RAW = [
    ("MCBA-CB", "Carlo Barberi"),
    ("MCBA-EMC", "Ed McGuinness"),
    ("MCBA-MB", "Mark Brooks"),
    ("MCBA-MM", "Mike McKone"),
    ("MCBA-PM", "Paco Medina"),
    ("MCBA-RB", "Ryan Brown"),
]

# Deadpool Autographs (1 card, no parallels)
DEADPOOL_AUTOS_RAW = [
    ("TC-D", "Dogpool", "Signed by Peggy the Dog"),
]

# Comic Book Gold (30 cards)
COMIC_BOOK_GOLD_RAW = [
    ("CB-1", "Deadpool"), ("CB-2", "Deadpool"), ("CB-3", "Deadpool"),
    ("CB-4", "Wade Wilson"), ("CB-5", "Wild Thing"), ("CB-6", "Wolverine"),
    ("CB-7", "Wolverine"), ("CB-8", "Wolverine"), ("CB-9", "Old Man Logan"),
    ("CB-10", "Weapon X"), ("CB-11", "Ultimate Wolverine"), ("CB-12", "Patch"),
    ("CB-13", "Cable"), ("CB-14", "Evil Deadpool"), ("CB-15", "Archangel"),
    ("CB-16", "Colossus"), ("CB-17", "Domino"), ("CB-18", "X-23"),
    ("CB-19", "Professor X"), ("CB-20", "Lady Deadpool"), ("CB-21", "Headpool"),
    ("CB-22", "Kidpool"), ("CB-23", "King Deadpool"), ("CB-24", "Zenpool"),
    ("CB-25", "Deadpool 2099"), ("CB-26", "Ultimate Deadpool"),
    ("CB-27", "Fantomex"), ("CB-28", "Dreadpool"), ("CB-29", "Psylocke"),
    ("CB-30", "Nightcrawler"),
]

# Cover Stars (30 cards, co_players for multi-character)
# Format: (card_number, comic_title, [characters])
COVER_STARS_RAW = [
    ("CS-1", "Deadpool / Wolverine #2", ["Deadpool", "Wolverine"]),
    ("CS-2", "Deadpool #27", ["Deadpool"]),
    ("CS-3", "Deadpool & Wolverine: WWIII #3", ["Deadpool", "Wolverine"]),
    ("CS-4", "Deadpool & Wolverine: WWIII #1", ["Deadpool", "Wolverine"]),
    ("CS-5", "Deadpool #1", ["Deadpool"]),
    ("CS-6", "Deadpool #4", ["Deadpool"]),
    ("CS-7", "Wolverine: Deep Cut #1", ["Wolverine"]),
    ("CS-8", "The Avengers #16", ["Avengers"]),
    ("CS-9", "X-Men: Heir of Apocalypse #3", ["X-Men"]),
    ("CS-10", "X-Men: Blood Hunt \u2013 Laura Kinney The Wolverine #1", ["X-23", "Wolverine"]),
    ("CS-11", "Hellverine #3", ["Wolverine"]),
    ("CS-12", "Wolverine #20", ["Wolverine"]),
    ("CS-13", "The Immortal Thor #13", ["Thor"]),
    ("CS-14", "The Avengers #17", ["Avengers"]),
    ("CS-15", "Captain America #11", ["Captain America"]),
    ("CS-16", "Fantastic Four #22", ["Fantastic Four"]),
    ("CS-17", "The Spectacular Spider-Men #6", ["Spider-Man"]),
    ("CS-18", "Spider-Gwen: The Ghost-Spider #3", ["Spider-Gwen"]),
    ("CS-19", "X-Men #2", ["X-Men"]),
    ("CS-20", "Deadpool Vs. Wolverine: Slash 'Em Up Infinity Comic #1", ["Deadpool", "Wolverine"]),
    ("CS-21", "Deadpool #1", ["Deadpool"]),
    ("CS-22", "Deadpool Vs. Wolverine: Slash 'Em Up Infinity Comic #3", ["Deadpool", "Wolverine"]),
    ("CS-23", "Deadpool / Wolverine #7", ["Deadpool", "Wolverine"]),
    ("CS-24", "Deadpool / Wolverine #1", ["Deadpool", "Wolverine"]),
    ("CS-25", "Wolverine: Origins #25", ["Wolverine"]),
    ("CS-26", "Wolverines & Deadpools #1", ["Deadpool", "Wolverine"]),
    ("CS-27", "Wolverines & Deadpools #1", ["Deadpool", "Wolverine"]),
    ("CS-28", "Wolverines & Deadpools #2", ["Deadpool", "Wolverine"]),
    ("CS-29", "The New Mutants #98", ["Deadpool"]),
    ("CS-30", "The Incredible Hulk #181", ["Wolverine", "Hulk"]),
]

# Well You Got Nothing To Say Mouth (10 cards)
WELL_YOU_GOT_RAW = [
    ("WM-01", "Deadpool"), ("WM-02", "Wolverine"), ("WM-03", "Deadpool"),
    ("WM-04", "Deadpool"), ("WM-05", "Deadpool"), ("WM-06", "Wolverine"),
    ("WM-07", "Deadpool"), ("WM-08", "Deadpool"), ("WM-09", "Cassandra Nova"),
    ("WM-10", "Wolverine"),
]

# Future Stars (10 cards)
FUTURE_STARS_RAW = [
    ("FS-1", "Cowboypool"), ("FS-2", "Welshpool"), ("FS-3", "Babypool"),
    ("FS-4", "Golden Age Deadpool"), ("FS-5", "Deadpool 2099"),
    ("FS-6", "Headpool"), ("FS-7", "Kidpool"), ("FS-8", "Dogpool"),
    ("FS-9", "Ladypool"), ("FS-10", "Zenpool"),
]

# Topps Originals (10 cards)
TOPPS_ORIGINALS_RAW = [
    ("TO-1", "Deadpool"), ("TO-2", "Psylocke"), ("TO-3", "Lady Deadpool"),
    ("TO-4", "Juggernaut"), ("TO-5", "Wolverine"), ("TO-6", "Cable"),
    ("TO-7", "Colossus"), ("TO-8", "Gambit"), ("TO-9", "X-23"),
    ("TO-10", "Sabretooth"),
]

# 10005 Fire (9 cards, FO-8 missing)
FIRE_RAW = [
    ("FO-1", "Pyro"), ("FO-2", "Cassandra Nova"), ("FO-3", "X-23"),
    ("FO-4", "Juggernaut"), ("FO-5", "Colossus"), ("FO-6", "Sabretooth"),
    ("FO-7", "Peter"), ("FO-9", "Negasonic Teenage Warhead"),
    ("FO-10", "Mr. Paradox"),
]

# Best Bubs (9 cards, NC-7 missing)
BEST_BUBS_RAW = [
    ("NC-1", "Deadpool"), ("NC-2", "Wolverine"), ("NC-3", "Blind Al"),
    ("NC-4", "Dogpool"), ("NC-5", "Vanessa"), ("NC-6", "Peter"),
    ("NC-8", "Negasonic Teenage Warhead"), ("NC-9", "X-23"),
    ("NC-10", "Johnny Storm"),
]

# Looking For Logan (5 cards)
LOOKING_FOR_LOGAN_RAW = [
    ("LL-1", "Classic Brown-and-Tan Wolverine"), ("LL-2", "The Cavillrine"),
    ("LL-3", "Short King Wolverine"), ("LL-4", "Fever Dream Wolverine"),
    ("LL-5", "Wolverine"),
]

# Indestructible (5 cards)
INDESTRUCTIBLE_RAW = [
    ("I-1", "Wolverine"), ("I-2", "Dogpool"), ("I-3", "X-23"),
    ("I-4", "Juggernaut"), ("I-5", "Deadpool"),
]

# Deadpool Reflections (5 cards, co_players)
DEADPOOL_REFLECTIONS_RAW = [
    ("DE-1", ["Psylocke", "Deadpool"]),
    ("DE-2", ["Wolverine", "Deadpool"]),
    ("DE-3", ["Cable", "Deadpool"]),
    ("DE-4", ["Deadpool", "Colossus"]),
    ("DE-5", ["Wolverine", "Gambit"]),
]

# Hidden Gems (5 cards, no parallels)
HIDDEN_GEMS_RAW = [
    ("HG-1", "Deadpool"), ("HG-2", "Wolverine"), ("HG-3", "Cassandra Nova"),
    ("HG-4", "X-23"), ("HG-5", "Pyro"),
]

# The Void (10 cards)
THE_VOID_RAW = [
    ("TV-1", "Deadpool"), ("TV-2", "Wolverine"), ("TV-3", "Cassandra Nova"),
    ("TV-4", "Pyro"), ("TV-5", "Juggernaut"), ("TV-6", "X-23"),
    ("TV-7", "Sabretooth"), ("TV-8", "Toad"), ("TV-9", "Azazel"),
    ("TV-10", "Russian"),
]

# Deadpool Icons (10 cards, Value Box Exclusive, no parallels)
DEADPOOL_ICONS_RAW = [
    ("DI-1", "Deadpool"), ("DI-2", "Cable"), ("DI-3", "Domino"),
    ("DI-4", "Gambit"), ("DI-5", "X-23"), ("DI-6", "Nightcrawler"),
    ("DI-7", "Elektra"), ("DI-8", "Blade"), ("DI-9", "Rogue"),
    ("DI-10", "Wolverine"),
]


# ── Build helpers ─────────────────────────────────────────────────────────────

def build_simple_cards(raw: list[tuple[str, str]], subset: str | None = None) -> list[dict]:
    """Build card dicts from (card_number, player) tuples."""
    return [{
        "card_number": num,
        "player": player,
        "team": "",
        "is_rookie": False,
        "subset": subset,
    } for num, player in raw]


def build_auto_cards(raw: list[tuple[str, str, str]]) -> list[dict]:
    """Build card dicts for autographs: (card_number, character, note)."""
    return [{
        "card_number": num,
        "player": player,
        "team": "",
        "is_rookie": False,
        "subset": note,
    } for num, player, note in raw]


def build_artist_auto_cards(raw: list[tuple[str, str]]) -> list[dict]:
    """Build card dicts for artist autographs: (card_number, artist_name)."""
    return [{
        "card_number": num,
        "player": artist,
        "team": "",
        "is_rookie": False,
        "subset": None,
    } for num, artist in raw]


def build_dual_auto_cards(raw: list[tuple[str, list[tuple[str, str]]]]) -> list[dict]:
    """Build card dicts for dual autographs with co_players.
    Each player gets their own entry with the same card_number."""
    cards = []
    for num, players_list in raw:
        for player, note in players_list:
            cards.append({
                "card_number": num,
                "player": player,
                "team": "",
                "is_rookie": False,
                "subset": note,
            })
    return cards


def build_cover_star_cards(raw: list[tuple[str, str, list[str]]]) -> list[dict]:
    """Build card dicts for Cover Stars.
    Comic title stored in subset, each character gets its own entry for co_players."""
    cards = []
    for num, comic_title, characters in raw:
        for char in characters:
            cards.append({
                "card_number": num,
                "player": char,
                "team": "",
                "is_rookie": False,
                "subset": comic_title,
            })
    return cards


def build_reflections_cards(raw: list[tuple[str, list[str]]]) -> list[dict]:
    """Build card dicts for Deadpool Reflections with co_players."""
    cards = []
    for num, characters in raw:
        for char in characters:
            cards.append({
                "card_number": num,
                "player": char,
                "team": "",
                "is_rookie": False,
                "subset": None,
            })
    return cards


# ── Sections ──────────────────────────────────────────────────────────────────

SECTIONS: list[tuple[str, list[dict], list[dict]]] = [
    ("Base - Comic Accurate", build_simple_cards(BASE_COMIC_ACCURATE_RAW), BASE_PARALLELS),
    ("Base - Characters", build_simple_cards(BASE_CHARACTERS_RAW), BASE_PARALLELS),
    ("Base - Multiverse And More", build_simple_cards(BASE_MULTIVERSE_RAW), BASE_PARALLELS),
    ("Chrome Autographs", build_auto_cards(CHROME_AUTOS_RAW), CHROME_AUTO_PARALLELS),
    ("Best Bubs Autographs", build_auto_cards(BEST_BUBS_AUTOS_RAW), BEST_BUBS_AUTO_PARALLELS),
    ("On-Card Dual Inscription Booklet", build_dual_auto_cards(ON_CARD_DUAL_RAW), ON_CARD_DUAL_PARALLELS),
    ("Chrome Dual Autographs", build_dual_auto_cards(CHROME_DUAL_AUTOS_RAW), CHROME_DUAL_AUTO_PARALLELS),
    ("Marvel Comic Book Artist Autographs", build_artist_auto_cards(MARVEL_ARTIST_AUTOS_RAW), MARVEL_ARTIST_AUTO_PARALLELS),
    ("Deadpool Autographs", build_auto_cards(DEADPOOL_AUTOS_RAW), []),
    ("Comic Book Gold", build_simple_cards(COMIC_BOOK_GOLD_RAW), COMIC_BOOK_GOLD_PARALLELS),
    ("Cover Stars", build_cover_star_cards(COVER_STARS_RAW), COVER_STARS_PARALLELS),
    ("Well You Got Nothing To Say Mouth", build_simple_cards(WELL_YOU_GOT_RAW), WELL_YOU_GOT_PARALLELS),
    ("Future Stars", build_simple_cards(FUTURE_STARS_RAW), FUTURE_STARS_PARALLELS),
    ("Topps Originals", build_simple_cards(TOPPS_ORIGINALS_RAW), TOPPS_ORIGINALS_PARALLELS),
    ("10005 Fire", build_simple_cards(FIRE_RAW), FIRE_PARALLELS),
    ("Best Bubs", build_simple_cards(BEST_BUBS_RAW), BEST_BUBS_PARALLELS),
    ("Looking For Logan", build_simple_cards(LOOKING_FOR_LOGAN_RAW), LOOKING_FOR_LOGAN_PARALLELS),
    ("Indestructible", build_simple_cards(INDESTRUCTIBLE_RAW), INDESTRUCTIBLE_PARALLELS),
    ("Deadpool Reflections", build_reflections_cards(DEADPOOL_REFLECTIONS_RAW), DEADPOOL_REFLECTIONS_PARALLELS),
    ("Hidden Gems", build_simple_cards(HIDDEN_GEMS_RAW), []),
    ("The Void", build_simple_cards(THE_VOID_RAW), THE_VOID_PARALLELS),
    ("Deadpool Icons", build_simple_cards(DEADPOOL_ICONS_RAW), []),
]


# ── Player aggregation and stats ─────────────────────────────────────────────

def compute_print_run_for_appearance(section_parallels: list[dict]) -> tuple[int, int]:
    """Return (total_print_run, one_of_ones) for a single card appearance.
    total_print_run = sum of all numbered parallel print runs.
    one_of_ones = count of parallels with print_run == 1."""
    total = 0
    ones = 0
    for p in section_parallels:
        pr = p["print_run"]
        if pr is not None:
            total += pr
            if pr == 1:
                ones += 1
    return total, ones


def main() -> None:
    sections_out: list[dict] = []
    players_map: dict[str, dict] = {}  # keyed by player name (case-sensitive for display)

    for section_name, cards, section_parallels in SECTIONS:
        sections_out.append({
            "insert_set": section_name,
            "parallels": section_parallels,
            "cards": cards,
        })

        pr_total, pr_ones = compute_print_run_for_appearance(section_parallels)

        for card in cards:
            key = card["player"].lower()
            if key not in players_map:
                players_map[key] = {
                    "player": card["player"],
                    "appearances": [],
                    "insert_sets_seen": set(),
                    "total_print_run": 0,
                    "one_of_ones": 0,
                }
            entry = players_map[key]
            entry["appearances"].append({
                "insert_set": section_name,
                "card_number": card["card_number"],
                "team": card["team"],
                "is_rookie": card["is_rookie"],
                "subset_tag": card.get("subset"),
                "parallels": section_parallels,
            })
            entry["insert_sets_seen"].add(section_name)
            entry["total_print_run"] += pr_total
            entry["one_of_ones"] += pr_ones

    # Build player list with stats
    players_out: list[dict] = []
    for entry in sorted(players_map.values(), key=lambda e: e["player"]):
        unique_cards = len(entry["appearances"])
        insert_sets = len(entry["insert_sets_seen"])

        players_out.append({
            "player": entry["player"],
            "appearances": entry["appearances"],
            "stats": {
                "unique_cards": unique_cards,
                "total_print_run": entry["total_print_run"],
                "one_of_ones": entry["one_of_ones"],
                "insert_sets": insert_sets,
            },
        })

    output = {
        "set_name": SET_NAME,
        "sport": SPORT,
        "season": SEASON,
        "league": LEAGUE,
        "sections": sections_out,
        "players": players_out,
    }

    total_cards = sum(len(s["cards"]) for s in sections_out)
    print(f"Sections: {len(sections_out)}")
    print(f"Total cards (incl. co-player entries): {total_cards}")
    print(f"Unique players: {len(players_out)}")

    out_path = "chrome_deadpool_2025_parsed.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"Written to {out_path}")


if __name__ == "__main__":
    main()
