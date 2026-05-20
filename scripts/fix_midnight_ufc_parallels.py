"""
Attach parallel matrix and pack odds to 2026 Topps Midnight UFC (set 835).
Usage: python3 scripts/fix_midnight_ufc_parallels.py
"""
import sqlite3, os, json

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
db = sqlite3.connect(DB_PATH)
db.execute("PRAGMA journal_mode=WAL")

SET_ID = 835
H = "Hobby"

def get_is_id(name):
    row = db.execute("SELECT id FROM insert_sets WHERE set_id = ? AND name = ?", (SET_ID, name)).fetchone()
    if not row: raise ValueError(f"Insert set '{name}' not found")
    return row[0]

def add_pars(is_id, pars):
    for name, pr in pars:
        db.execute("INSERT INTO parallels (insert_set_id, name, print_run, exclusivity) VALUES (?, ?, ?, ?)",
                   (is_id, name, pr, H))
    return len(pars)

# ─── Base Parallel Ladder (10 parallels) ────────────────────────────────────
base_pars = [
    ("Base", None), ("Zodiac", None), ("Morning", 125), ("Twilight", 99),
    ("Dusk", 75), ("Moon Beam", None), ("Moonrise", 25), ("Midnight", 12),
    ("Daybreak", 5), ("Black Light", 1),
]
n = add_pars(get_is_id("Base Set"), base_pars)
print(f"  Base Set: {n} parallels")

# ─── Standard Insert Ladder (6 parallels × 5 subsets) ──────────────────────
std_insert_pars = [
    ("Base", None), ("Dusk", 75), ("Moonrise", 25), ("Midnight", 12),
    ("Daybreak", 5), ("Black Light", 1),
]
for name in ["Night Watch", "Zero Hour", "Celestial Combos", "Lunar Apex", "Insomnia"]:
    n = add_pars(get_is_id(name), std_insert_pars)
    print(f"  {name}: {n} parallels")

# ─── Case Hit Insert Ladder (3 parallels × 4 subsets) ──────────────────────
case_hit_pars = [("Base", None), ("Daybreak", 5), ("Black Light", 1)]
for name in ["Last One Standing", "Neon Apex", "Twilight", "Cemented"]:
    n = add_pars(get_is_id(name), case_hit_pars)
    print(f"  {name}: {n} parallels")

# ─── Main Autograph Ladder (8 parallels × 4 subsets) ───────────────────────
auto_pars = [
    ("Base", None), ("Twilight", 99), ("Dusk", 75), ("Moon Beam", None),
    ("Moonrise", 25), ("Midnight", 12), ("Daybreak", 5), ("Black Light", 1),
]
for name in ["Rookie Relic Autographs", "Relic Autographs", "Autograph Variation", "Horizon Signatures"]:
    n = add_pars(get_is_id(name), auto_pars)
    print(f"  {name}: {n} parallels")

# ─── Fight Glove Relic Autographs (2 parallels — Daybreak /8, Black Light /1)
fg_pars = [("Daybreak", 8), ("Black Light", 1)]
n = add_pars(get_is_id("Fight Glove Relic Autographs"), fg_pars)
print(f"  Fight Glove Relic Autographs: {n} parallels (Daybreak /8)")

# ─── Pack Odds JSON ─────────────────────────────────────────────────────────
pack_odds = {"hobby": {
    # Base Set parallels
    "Base Set": "1:1", "Base Set Zodiac": "1:4", "Base Set Morning": "1:2",
    "Base Set Twilight": "1:2", "Base Set Dusk": "1:3", "Base Set Moon Beam": "1:14",
    "Base Set Moonrise": "1:8", "Base Set Midnight": "1:17", "Base Set Daybreak": "1:40",
    "Base Set Black Light": "1:198",

    # Night Watch
    "Night Watch": "1:11", "Night Watch Dusk": "1:11", "Night Watch Moonrise": "1:33",
    "Night Watch Midnight": "1:69", "Night Watch Daybreak": "1:164", "Night Watch Black Light": "1:817",

    # Zero Hour
    "Zero Hour": "1:14", "Zero Hour Dusk": "1:14", "Zero Hour Moonrise": "1:41",
    "Zero Hour Midnight": "1:86", "Zero Hour Daybreak": "1:205", "Zero Hour Black Light": "1:1,021",

    # Celestial Combos
    "Celestial Combos": "1:27", "Celestial Combos Dusk": "1:28", "Celestial Combos Moonrise": "1:82",
    "Celestial Combos Midnight": "1:171", "Celestial Combos Daybreak": "1:409", "Celestial Combos Black Light": "1:2,042",

    # Lunar Apex
    "Lunar Apex": "1:14", "Lunar Apex Dusk": "1:14", "Lunar Apex Moonrise": "1:41",
    "Lunar Apex Midnight": "1:86", "Lunar Apex Daybreak": "1:205", "Lunar Apex Black Light": "1:1,021",

    # Insomnia
    "Insomnia": "1:11", "Insomnia Dusk": "1:11", "Insomnia Moonrise": "1:33",
    "Insomnia Midnight": "1:69", "Insomnia Daybreak": "1:164", "Insomnia Black Light": "1:817",

    # Last One Standing (case hit)
    "Last One Standing": "1:32", "Last One Standing Daybreak": "1:148", "Last One Standing Black Light": "1:740",

    # Neon Apex (case hit)
    "Neon Apex": "1:38", "Neon Apex Daybreak": "1:178", "Neon Apex Black Light": "1:887",

    # Twilight (case hit insert subset)
    "Twilight": "1:48", "Twilight Daybreak": "1:222", "Twilight Black Light": "1:1,109",

    # Cemented (case hit)
    "Cemented": "1:38", "Cemented Daybreak": "1:178", "Cemented Black Light": "1:887",

    # Rookie Relic Autographs
    "Rookie Relic Autographs": "1:2", "Rookie Relic Autographs Twilight": "1:5",
    "Rookie Relic Autographs Dusk": "1:6", "Rookie Relic Autographs Moon Beam": "1:29",
    "Rookie Relic Autographs Moonrise": "1:18", "Rookie Relic Autographs Midnight": "1:36",
    "Rookie Relic Autographs Daybreak": "1:87", "Rookie Relic Autographs Black Light": "1:431",

    # Relic Autographs
    "Relic Autographs": "1:10", "Relic Autographs Twilight": "1:10",
    "Relic Autographs Dusk": "1:13", "Relic Autographs Moon Beam": "1:63",
    "Relic Autographs Moonrise": "1:38", "Relic Autographs Midnight": "1:79",
    "Relic Autographs Daybreak": "1:189", "Relic Autographs Black Light": "1:943",

    # Autograph Variation (was "Base Autograph Variations" in prompt, actual DB name is "Autograph Variation")
    "Autograph Variation": "1:2", "Autograph Variation Twilight": "1:4",
    "Autograph Variation Dusk": "1:5", "Autograph Variation Moon Beam": "1:24",
    "Autograph Variation Moonrise": "1:14", "Autograph Variation Midnight": "1:29",
    "Autograph Variation Daybreak": "1:70", "Autograph Variation Black Light": "1:348",

    # Horizon Signatures
    "Horizon Signatures": "1:5", "Horizon Signatures Twilight": "1:8",
    "Horizon Signatures Dusk": "1:11", "Horizon Signatures Moon Beam": "1:52",
    "Horizon Signatures Moonrise": "1:31", "Horizon Signatures Midnight": "1:64",
    "Horizon Signatures Daybreak": "1:153", "Horizon Signatures Black Light": "1:792",

    # Fight Glove Relic Autographs (Daybreak /8, Black Light /1 — source typo corrected)
    "Fight Glove Relic Autographs Daybreak": "1:104",
    "Fight Glove Relic Autographs Black Light": "1:825",
}}

db.execute("UPDATE sets SET pack_odds = ? WHERE id = ?", (json.dumps(pack_odds), SET_ID))
print(f"\nAttached pack odds ({len(pack_odds['hobby'])} keys)")

# ─── Commit & Verify ────────────────────────────────────────────────────────
db.commit()

rows = db.execute("""
    SELECT ins.name, (SELECT COUNT(*) FROM parallels p WHERE p.insert_set_id = ins.id) as cnt
    FROM insert_sets ins WHERE ins.set_id = ? ORDER BY ins.name
""", (SET_ID,)).fetchall()

total = 0
print("\n--- Verification ---")
for name, cnt in rows:
    print(f"  {name}: {cnt}")
    total += cnt
print(f"\nTotal parallels: {total} (expected 86)")

# Verify Fight Glove Daybreak is /8
fg = db.execute("""
    SELECT p.name, p.print_run FROM parallels p
    JOIN insert_sets ins ON p.insert_set_id = ins.id
    WHERE ins.set_id = ? AND ins.name = 'Fight Glove Relic Autographs'
""", (SET_ID,)).fetchall()
print(f"\nFight Glove parallels: {fg}")

db.close()
print("Done!")
