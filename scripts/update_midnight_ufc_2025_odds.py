"""
Add pack odds to 2025 Topps Midnight UFC (set ID 8).
Also adds parallels to all insert sets.
Usage: python3 scripts/update_midnight_ufc_2025_odds.py
"""
import sqlite3, json

db = sqlite3.connect('the-c-list.db')

cursor = db.execute("SELECT id, name FROM sets WHERE name LIKE '%Midnight%UFC%' AND name LIKE '%2025%'")
row = cursor.fetchone()
if not row:
    print("Set not found!")
    exit(1)

set_id, set_name = row
print(f"Updating: {set_name} (ID: {set_id})")

# ─── Pack Odds ────────────────────────────────────────────────────
pack_odds = {
  "hobby": {
    # Base parallels
    "Base Zodiac": "1:4",
    "Base Morning": "1:2",
    "Base Twilight": "1:2",
    "Base Dusk": "1:3",
    "Base Moon Beam": "1:24",
    "Base Moonrise": "1:8",
    "Base Midnight": "1:17",
    "Base Daybreak": "1:40",
    "Base Black Light": "1:196",

    # Nightfall
    "Nightfall Moon Beam": "1:14",
    "Nightfall Dusk": "1:11",
    "Nightfall Moonrise": "1:32",
    "Nightfall Midnight": "1:66",
    "Nightfall Daybreak": "1:157",
    "Nightfall Black Light": "1:782",

    # Lunar Tide
    "Lunar Tide Moon Beam": "1:17",
    "Lunar Tide Dusk": "1:14",
    "Lunar Tide Moonrise": "1:40",
    "Lunar Tide Midnight": "1:82",
    "Lunar Tide Daybreak": "1:196",
    "Lunar Tide Black Light": "1:978",

    # Constellations
    "Constellations Moon Beam": "1:34",
    "Constellations Dusk": "1:27",
    "Constellations Moonrise": "1:79",
    "Constellations Midnight": "1:163",
    "Constellations Daybreak": "1:391",
    "Constellations Black Light": "1:1,955",

    # The One and Only (matching DB name — lowercase "and")
    "The One and Only Moon Beam": "1:17",
    "The One and Only Dusk": "1:14",
    "The One and Only Moonrise": "1:40",
    "The One and Only Midnight": "1:82",
    "The One and Only Daybreak": "1:196",
    "The One and Only Black Light": "1:978",

    # Insomnia
    "Insomnia Moon Beam": "1:14",
    "Insomnia Dusk": "1:11",
    "Insomnia Moonrise": "1:32",
    "Insomnia Midnight": "1:66",
    "Insomnia Daybreak": "1:157",
    "Insomnia Black Light": "1:782",

    # Dream Chasers
    "Dream Chasers": "1:35",
    "Dream Chasers Daybreak": "1:142",
    "Dream Chasers Black Light": "1:708",

    # Greetings From
    "Greetings From": "1:42",
    "Greetings From Daybreak": "1:170",
    "Greetings From Black Light": "1:850",

    # Twilight
    "Twilight": "1:52",
    "Twilight Daybreak": "1:213",
    "Twilight Black Light": "1:1,062",

    # Night Vision
    "Night Vision": "1:42",
    "Night Vision Daybreak": "1:170",
    "Night Vision Black Light": "1:850",

    # Rookie Relic Autographs
    "Rookie Relic Autographs": "1:3",
    "Rookie Relic Autographs Twilight": "1:6",
    "Rookie Relic Autographs Dusk": "1:8",
    "Rookie Relic Autographs Moon Beam": "1:61",
    "Rookie Relic Autographs Moonrise": "1:22",
    "Rookie Relic Autographs Midnight": "1:46",
    "Rookie Relic Autographs Daybreak": "1:109",
    "Rookie Relic Autographs Black Light": "1:542",

    # Relic Autographs
    "Relic Autographs": "1:7",
    "Relic Autographs Twilight": "1:10",
    "Relic Autographs Dusk": "1:12",
    "Relic Autographs Moon Beam": "1:92",
    "Relic Autographs Moonrise": "1:33",
    "Relic Autographs Midnight": "1:69",
    "Relic Autographs Daybreak": "1:165",
    "Relic Autographs Black Light": "1:825",

    # Stroke of Midnight Autographs
    "Stroke of Midnight Autographs": "1:7",
    "Stroke of Midnight Autographs Twilight": "1:10",
    "Stroke of Midnight Autographs Dusk": "1:13",
    "Stroke of Midnight Autographs Moon Beam": "1:105",
    "Stroke of Midnight Autographs Moonrise": "1:37",
    "Stroke of Midnight Autographs Midnight": "1:76",
    "Stroke of Midnight Autographs Daybreak": "1:183",
    "Stroke of Midnight Autographs Black Light": "1:903",

    # Glimmer Graphs (DB name — no "Autographs" suffix)
    "Glimmer Graphs": "1:8",
    "Glimmer Graphs Twilight": "1:11",
    "Glimmer Graphs Dusk": "1:15",
    "Glimmer Graphs Moon Beam": "1:111",
    "Glimmer Graphs Moonrise": "1:41",
    "Glimmer Graphs Midnight": "1:85",
    "Glimmer Graphs Daybreak": "1:207",
    "Glimmer Graphs Black Light": "1:998",

    # Horizon Signatures (DB name — no "Autographs" suffix)
    "Horizon Signatures": "1:3",
    "Horizon Signatures Twilight": "1:4",
    "Horizon Signatures Dusk": "1:5",
    "Horizon Signatures Moon Beam": "1:36",
    "Horizon Signatures Moonrise": "1:13",
    "Horizon Signatures Midnight": "1:27",
    "Horizon Signatures Daybreak": "1:64",
    "Horizon Signatures Black Light": "1:327",
  }
}

db.execute("UPDATE sets SET pack_odds = ? WHERE id = ?", (json.dumps(pack_odds), set_id))
print(f"Pack odds updated: {len(pack_odds['hobby'])} entries")

# ─── Add parallels ────────────────────────────────────────────────
# Get all insert sets
cursor = db.execute("SELECT id, name FROM insert_sets WHERE set_id = ?", (set_id,))
insert_sets = cursor.fetchall()

# Check existing parallels
existing = set()
for is_id, is_name in insert_sets:
    rows = db.execute("SELECT name FROM parallels WHERE insert_set_id = ?", (is_id,)).fetchall()
    for r in rows:
        existing.add((is_id, r[0]))

AUTO_KEYWORDS = ["autograph", "signature", "relic", "glimmer", "stroke"]
BASE_PARALLELS = [
    ("Zodiac", None), ("Morning", None), ("Twilight", None), ("Dusk", None),
    ("Moon Beam", None), ("Moonrise", None), ("Midnight", None),
    ("Daybreak", None), ("Black Light", None),
]
INSERT_PARALLELS = [
    ("Dusk", None), ("Moon Beam", None), ("Moonrise", None),
    ("Midnight", None), ("Daybreak", None), ("Black Light", None),
]
AUTO_PARALLELS = [
    ("Twilight", None), ("Dusk", None), ("Moon Beam", None),
    ("Moonrise", None), ("Midnight", None), ("Daybreak", None), ("Black Light", None),
]

added = 0
for is_id, is_name in insert_sets:
    is_auto = any(kw in is_name.lower() for kw in AUTO_KEYWORDS)

    if is_name == "Base Set":
        pars = BASE_PARALLELS
    elif is_auto:
        pars = AUTO_PARALLELS
    else:
        pars = INSERT_PARALLELS

    for par_name, print_run in pars:
        if (is_id, par_name) not in existing:
            db.execute("INSERT INTO parallels (insert_set_id, name, print_run) VALUES (?, ?, ?)",
                       (is_id, par_name, print_run))
            added += 1

print(f"Parallels added: {added}")

db.commit()
print("Done!")
db.close()
