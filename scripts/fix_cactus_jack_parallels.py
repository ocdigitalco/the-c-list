"""
Attach parallel matrix and pack odds to 2025-26 Topps Chrome Cactus Jack Basketball (set 23).
Replaces existing parallels with correct sell sheet data.
Missing subsets (Utopia Highlights, Jacked Up, LA Flame Legends, Astrovision, Cactus Mode,
Base Autograph Variation, Cactus Ink) are created as empty shells — card data pending.
Usage: python3 scripts/fix_cactus_jack_parallels.py
"""
import sqlite3, os, json

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
db = sqlite3.connect(DB_PATH)
db.execute("PRAGMA journal_mode=WAL")

SET_ID = 23
H = "Hobby"

def get_is_id(name):
    row = db.execute("SELECT id FROM insert_sets WHERE set_id = ? AND name = ?", (SET_ID, name)).fetchone()
    if row: return row[0]
    # Create if missing
    db.execute("INSERT INTO insert_sets (set_id, name, is_autograph) VALUES (?, ?, 0)", (SET_ID, name))
    is_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    print(f"  CREATED insert set: {name} (ID {is_id})")
    return is_id

def get_auto_is_id(name):
    row = db.execute("SELECT id FROM insert_sets WHERE set_id = ? AND name = ?", (SET_ID, name)).fetchone()
    if row:
        db.execute("UPDATE insert_sets SET is_autograph = 1 WHERE id = ?", (row[0],))
        return row[0]
    db.execute("INSERT INTO insert_sets (set_id, name, is_autograph) VALUES (?, ?, 1)", (SET_ID, name))
    is_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    print(f"  CREATED auto insert set: {name} (ID {is_id})")
    return is_id

def add_pars(is_id, pars):
    for name, pr in pars:
        db.execute("INSERT INTO parallels (insert_set_id, name, print_run, exclusivity) VALUES (?, ?, ?, ?)",
                   (is_id, name, pr, H))
    return len(pars)

# ─── Clear existing parallels ───────────────────────────────────────────────
deleted = db.execute("""
    DELETE FROM parallels WHERE insert_set_id IN (
        SELECT id FROM insert_sets WHERE set_id = ?
    )
""", (SET_ID,)).rowcount
print(f"Deleted {deleted} existing parallels")

# ─── Mark existing auto subsets ─────────────────────────────────────────────
db.execute("UPDATE insert_sets SET is_autograph = 1 WHERE set_id = ? AND name = 'All-Star Game Autographs'", (SET_ID,))

# ─── Base Parallel Ladder (19 parallels) ────────────────────────────────────
base_pars = [
    ("Base", None), ("White", None), ("Refractor", None), ("LogoFractor", None),
    ("Teal Speckle Refractor", 299), ("Pink Refractor", 250), ("Aqua Shimmer", 199),
    ("Lasers", 175), ("Blue Refractor", 150), ("Sonar", 125),
    ("Green Refractor", 99), ("Purple Mini-Diamond", 75), ("Gold Refractor", 50),
    ("Cactus Jack Refractor", 41), ("Orange Refractor", 25), ("Black Refractor", 10),
    ("Red Refractor", 5), ("Red Mini-Diamond Refractor", 5), ("SuperFractor", 1),
]
n = add_pars(get_is_id("Base Set"), base_pars)
print(f"  Base Set: {n} parallels")

# ─── Insert Ladder (9 parallels × 3 subsets) ───────────────────────────────
insert_pars = [
    ("Base", None), ("Blue Refractor", 150), ("Green Refractor", 99),
    ("Purple Mini-Diamond", 75), ("Gold Refractor", 50), ("Orange Refractor", 25),
    ("Black Refractor", 10), ("Red Refractor", 5), ("SuperFractor", 1),
]
for name in ["Utopia Highlights", "Jacked Up", "LA Flame Legends"]:
    n = add_pars(get_is_id(name), insert_pars)
    print(f"  {name}: {n} parallels")

# Also apply to existing Sicko Stars (same tier as standard inserts)
n = add_pars(get_is_id("Sicko Stars"), insert_pars)
print(f"  Sicko Stars: {n} parallels")

# ─── Case Hit Ladder (2 parallels × 2 subsets) ─────────────────────────────
case_pars = [("Base", None), ("SuperFractor", 1)]
for name in ["Astrovision", "Cactus Mode"]:
    n = add_pars(get_is_id(name), case_pars)
    print(f"  {name}: {n} parallels")

# ─── Autograph Ladder (5 parallels × 2 subsets) ────────────────────────────
auto_pars = [
    ("Base", None), ("Orange Refractor", 25), ("Black Refractor", 10),
    ("Red Refractor", 5), ("SuperFractor", 1),
]
for name in ["Base Autograph Variation", "Cactus Ink"]:
    n = add_pars(get_auto_is_id(name), auto_pars)
    print(f"  {name}: {n} parallels")

# Also apply to existing All-Star Game Autographs
n = add_pars(get_is_id("All-Star Game Autographs"), auto_pars)
print(f"  All-Star Game Autographs: {n} parallels")

# ─── Pack Odds JSON ─────────────────────────────────────────────────────────
pack_odds = {"hobby": {
    # Base
    "Base": "4:1", "White": "1:7", "Refractor": "1:10", "LogoFractor": "1:20",
    "Teal Speckle Refractor": "1:26", "Pink Refractor": "1:31", "Aqua Shimmer": "1:38",
    "Lasers": "1:44", "Blue Refractor": "1:51", "Sonar": "1:61",
    "Green Refractor": "1:77", "Purple Mini-Diamond": "1:101", "Gold Refractor": "1:151",
    "Cactus Jack Refractor": "1:184", "Orange Refractor": "1:302", "Black Refractor": "1:754",
    "Red Refractor": "1:1,509", "Red Mini-Diamond Refractor": "1:1,509", "SuperFractor": "1:7,575",

    # Utopia Highlights
    "Utopia Highlights": "1:8", "Utopia Highlights Blue Refractor": "1:126",
    "Utopia Highlights Green Refractor": "1:191", "Utopia Highlights Purple Mini-Diamond": "1:252",
    "Utopia Highlights Gold Refractor": "1:377", "Utopia Highlights Orange Refractor": "1:754",
    "Utopia Highlights Black Refractor": "1:1,884", "Utopia Highlights Red Refractor": "1:3,768",
    "Utopia Highlights SuperFractor": "1:19,137",

    # Jacked Up
    "Jacked Up": "1:8", "Jacked Up Blue Refractor": "1:126",
    "Jacked Up Green Refractor": "1:191", "Jacked Up Purple Mini-Diamond": "1:252",
    "Jacked Up Gold Refractor": "1:377", "Jacked Up Orange Refractor": "1:754",
    "Jacked Up Black Refractor": "1:1,884", "Jacked Up Red Refractor": "1:3,768",
    "Jacked Up SuperFractor": "1:19,137",

    # LA Flame Legends
    "LA Flame Legends": "1:15", "LA Flame Legends Blue Refractor": "1:252",
    "LA Flame Legends Green Refractor": "1:381", "LA Flame Legends Purple Mini-Diamond": "1:503",
    "LA Flame Legends Gold Refractor": "1:754", "LA Flame Legends Orange Refractor": "1:1,509",
    "LA Flame Legends Black Refractor": "1:3,768", "LA Flame Legends Red Refractor": "1:7,575",
    "LA Flame Legends SuperFractor": "1:38,274",

    # Astrovision (case hit)
    "Astrovision": "1:305", "Astrovision SuperFractor": "1:42,777",

    # Cactus Mode (case hit)
    "Cactus Mode": "1:1,200", "Cactus Mode SuperFractor": "1:42,777",

    # Base Autograph Variation
    "Base Autograph Variation": "1:208", "Base Autograph Variation Orange Refractor": "1:1,064",
    "Base Autograph Variation Black Refractor": "1:2,664", "Base Autograph Variation Red Refractor": "1:5,348",
    "Base Autograph Variation SuperFractor": "1:26,934",

    # Cactus Ink
    "Cactus Ink": "1:208", "Cactus Ink Orange Refractor": "1:1,064",
    "Cactus Ink Black Refractor": "1:2,664", "Cactus Ink Red Refractor": "1:5,348",
    "Cactus Ink SuperFractor": "1:26,934",
}}

db.execute("UPDATE sets SET pack_odds = ? WHERE id = ?", (json.dumps(pack_odds), SET_ID))
print(f"\nAttached pack odds ({len(pack_odds['hobby'])} keys)")

# ─── Commit & Verify ────────────────────────────────────────────────────────
db.commit()

rows = db.execute("""
    SELECT ins.name, (SELECT COUNT(*) FROM parallels p WHERE p.insert_set_id = ins.id) as cnt,
           (SELECT COUNT(*) FROM player_appearances pa WHERE pa.insert_set_id = ins.id) as cards
    FROM insert_sets ins WHERE ins.set_id = ? ORDER BY ins.name
""", (SET_ID,)).fetchall()

total_pars = 0
print("\n--- Verification ---")
for name, cnt, cards in rows:
    flag = " (empty shell)" if cards == 0 else ""
    print(f"  {name}: {cnt} parallels, {cards} cards{flag}")
    total_pars += cnt
print(f"\nTotal parallels: {total_pars}")

# Verify special print runs
special = db.execute("""
    SELECT ins.name, p.name, p.print_run FROM parallels p
    JOIN insert_sets ins ON p.insert_set_id = ins.id
    WHERE ins.set_id = ? AND p.name IN ('Cactus Jack Refractor', 'Red Mini-Diamond Refractor')
""", (SET_ID,)).fetchall()
print(f"\nSpecial parallels: {special}")

db.close()
print("Done!")
