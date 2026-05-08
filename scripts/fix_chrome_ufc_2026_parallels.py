"""
Fix parallels for 2026 Topps Chrome UFC (set 840).
Replaces auto-generated parallels with correct per-subset parallel ladders.
Also sets box_config.

Usage: python3 scripts/fix_chrome_ufc_2026_parallels.py
"""
import sqlite3, json, os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
db = sqlite3.connect(DB_PATH)
db.execute("PRAGMA journal_mode=WAL")

SET_ID = 840

# ─── Verify set ──────────────────────────────────────────────────────────────
row = db.execute("SELECT id, name FROM sets WHERE id = ?", (SET_ID,)).fetchone()
if not row:
    print(f"Set {SET_ID} not found!")
    exit(1)
print(f"Set: {row[1]} (ID {row[0]})")

# ─── Count existing parallels ────────────────────────────────────────────────
old_count = db.execute("""
    SELECT COUNT(*) FROM parallels
    WHERE insert_set_id IN (SELECT id FROM insert_sets WHERE set_id = ?)
""", (SET_ID,)).fetchone()[0]
print(f"Existing parallels: {old_count}")

# ─── Delete all existing parallels for this set ──────────────────────────────
db.execute("""
    DELETE FROM parallels
    WHERE insert_set_id IN (SELECT id FROM insert_sets WHERE set_id = ?)
""", (SET_ID,))
print(f"Deleted {old_count} parallels")

# ─── Helper ──────────────────────────────────────────────────────────────────
def get_is_id(name):
    row = db.execute("SELECT id FROM insert_sets WHERE set_id = ? AND name = ?", (SET_ID, name)).fetchone()
    if not row:
        raise ValueError(f"Insert set not found: '{name}'")
    return row[0]

def add_parallels(is_name, parallels):
    is_id = get_is_id(is_name)
    for name, print_run in parallels:
        db.execute("INSERT INTO parallels (insert_set_id, name, print_run) VALUES (?, ?, ?)",
                   (is_id, name, print_run))
    print(f"  {is_name}: {len(parallels)} parallels")

# ─── BASE SET PARALLELS (39 parallels) ───────────────────────────────────────
# Note: FrozenFractor displays as "/-5" but numeric print_run = 5.
# The display override is handled in the UI, not the DB.
# Note: Printing Plates are NOT listed on the 2026 sell sheet. Omitting per spec.
add_parallels("Base Set", [
    ("Refractor", None),
    ("Negative Refractor", None),
    ("Prism Refractor", None),
    ("Sonar Refractor", None),
    ("UFC Glove Refractor", None),      # Value exclusive
    ("X-Fractor", None),                # Mega exclusive
    ("Magenta Refractor", 399),
    ("Teal Refractor", 299),
    ("Yellow Refractor", 275),
    ("Pink Refractor", 250),
    ("Aqua Refractor", 199),
    ("Blue Refractor", 150),
    ("Blue RayWave Refractor", 150),    # Value exclusive
    ("Blue Mini Diamonds Refractor", 150),  # Mega exclusive
    ("Blue Geometric Refractor", 99),   # Delight exclusive
    ("Green Refractor", 99),
    ("Green Geometric Refractor", 75),  # Delight exclusive
    ("Purple RayWave Refractor", 75),   # Value exclusive
    ("Purple Mini Diamonds Refractor", 75),  # Mega exclusive
    ("Gold Refractor", 50),
    ("Gold Geometric Refractor", 50),   # Delight exclusive
    ("Gold RayWave Refractor", 50),     # Value exclusive
    ("Gold Mini Diamonds Refractor", 50),  # Mega exclusive
    ("Orange Refractor", 25),
    ("Orange Geometric Refractor", 25), # Delight exclusive
    ("Orange RayWave Refractor", 25),   # Value exclusive
    ("Orange Mini Diamonds Refractor", 25),  # Mega exclusive
    ("Black Refractor", 10),
    ("Purple Geometric Refractor", 10), # Delight exclusive
    ("Black RayWave Refractor", 10),    # Value exclusive
    ("Black Mini Diamonds Refractor", 10),  # Mega exclusive
    ("OctaFractor", 8),                 # Hobby exclusive
    ("Red Refractor", 5),
    ("Red Geometric Refractor", 5),     # Delight exclusive
    ("Red RayWave Refractor", 5),       # Value exclusive
    ("Red Mini Diamonds Refractor", 5), # Mega exclusive
    ("FrozenFractor", 5),              # Hobby exclusive; displays as "/-5"
    ("Black Geometric Refractor", 2),   # Delight exclusive
    ("Superfractor", 1),
])

# ─── GROUP A: Standard Insert Parallels ──────────────────────────────────────
# Applies to: All Action, 1986 Topps, Striking Distance
GROUP_A = [
    ("Refractor", None),
    ("Geometric Refractor", None),      # Delight exclusive
    ("Blue Refractor", 150),
    ("Green Refractor", 99),
    ("Gold Refractor", 50),
    ("Gold Geometric Refractor", 50),   # Delight exclusive
    ("Orange Refractor", 25),
    ("Black Refractor", 10),
    ("Purple Geometric Refractor", 10), # Delight exclusive
    ("Red Refractor", 5),
    ("Black Geometric Refractor", 2),   # Delight exclusive
    ("Superfractor", 1),
]
for name in ["All Action", "1986 Topps", "Striking Distance"]:
    add_parallels(name, GROUP_A)

# ─── GROUP B: Hobby-Exclusive Insert Parallels ──────────────────────────────
GROUP_B = [
    ("Gold Refractor", 50),
    ("Black Refractor", 10),
    ("Red Refractor", 5),
    ("Superfractor", 1),
]
for name in ["Big Ticket", "Split Decision", "Fight Night Flashback", "Pulse Check", "Youthquake"]:
    add_parallels(name, GROUP_B)

# ─── GROUP C: Retail-Exclusive Insert Parallels ─────────────────────────────
GROUP_C = [
    ("Refractor", None),
    ("Aqua Refractor", 199),
    ("Blue Refractor", 150),
    ("Green Refractor", 99),
    ("Gold Refractor", 50),
    ("Orange Refractor", 25),
    ("Black Refractor", 10),
    ("Red Refractor", 5),
    ("Superfractor", 1),
]
for name in ["Global Warriors", "Allen and Ginter", "Manifesting Moments", "In Your Face", "Impact Point"]:
    add_parallels(name, GROUP_C)

# ─── GROUP D: SuperFractor-Only Inserts ──────────────────────────────────────
for name in ["Helix", "Let's Go"]:
    add_parallels(name, [("Superfractor", 1)])

# ─── GROUP E: No Parallels ──────────────────────────────────────────────────
# Immortal Force, Radiating Rookies, Hidden Gems — no parallels added
print("  Immortal Force: 0 parallels (none per spec)")
print("  Radiating Rookies: 0 parallels (none per spec)")
print("  Hidden Gems: 0 parallels (none per spec)")

# ─── GROUP F: Kings and Queens — Hobby exclusive, no parallels per spec ──────
# Prior Chrome UFC sets (2025) had no parallels for Kings and Queens either.
print("  Kings and Queens: 0 parallels (Hobby exclusive, none listed on sell sheet)")

# ─── Sapphire Selections, Infinite — check existing convention ───────────────
# These are chase inserts, not listed in the parallel groups above.
# Prior 2025 Chrome UFC had: Refractor(unnumbered), Gold/50, Black/10, Red/5, Superfractor/1
# Keep the same pattern as they're standard hobby inserts.
for name in ["Sapphire Selections", "Infinite"]:
    add_parallels(name, GROUP_B)  # Same as Hobby-exclusive

# ─── AUTO GROUP A: Standard Auto Parallels ───────────────────────────────────
AUTO_A = [
    ("Refractor", None),
    ("Geometric Refractor", None),      # Delight exclusive, unnumbered per spec
    ("Blue Refractor", 150),
    ("Gold Refractor", 50),
    ("Gold Geometric Refractor", 50),   # Delight exclusive
    ("Orange Refractor", 25),
    ("Orange Geometric Refractor", 25), # Delight exclusive
    ("Black Refractor", 10),
    ("Purple Geometric Refractor", 10), # Delight exclusive
    ("Red Refractor", 5),
    ("Red Geometric Refractor", 5),     # Delight exclusive
    ("Black Geometric Refractor", 2),   # Delight exclusive
    ("Superfractor", 1),
]
for name in ["Base Cards Autograph Variations", "1986 Topps Signatures",
             "Chrome Lineage Autographs", "Marks of Champions",
             "Octagon Legends Autographs", "Future Stars Autographs"]:
    add_parallels(name, AUTO_A)

# ─── AUTO GROUP B: Limited Auto Parallels ────────────────────────────────────
# Sell sheet doesn't specify product exclusivity. Defaulting to Hobby/Mega/Value.
AUTO_B = [
    ("Red Refractor", 5),
    ("Superfractor", 1),
]
for name in ["Quoted Autographs", "Topps 2009 Variation Signatures", "Vanquisher Ink"]:
    add_parallels(name, AUTO_B)

# ─── Box Config ──────────────────────────────────────────────────────────────
box_config = {
    "hobby": {
        "cards_per_pack": 8,
        "packs_per_box": 12,
        "boxes_per_case": 12,
        "autos_per_box": 2,
        "notes": "Per box: 2 autos, 4 numbered base parallels, 12 unnumbered base parallels, 12 inserts"
    },
    "mega": {
        "cards_per_pack": 8,
        "packs_per_box": 6,
        "boxes_per_case": 20,
        "notes": "Per box: 10 base X-Fractor parallels, 1 numbered base parallel, 6 inserts"
    },
    "value": {
        "cards_per_pack": 4,
        "packs_per_box": 6,
        "boxes_per_case": 40,
        "notes": "Per box: 3 UFC Glove Refractors, 2 base refractors, 6 inserts"
    },
}

db.execute("UPDATE sets SET box_config = ?, release_date = '2026-05-08' WHERE id = ?",
           (json.dumps(box_config), SET_ID))
print(f"\n  Box config updated (Hobby/Mega/Value)")

# ─── Summary ─────────────────────────────────────────────────────────────────
db.commit()
new_count = db.execute("""
    SELECT COUNT(*) FROM parallels
    WHERE insert_set_id IN (SELECT id FROM insert_sets WHERE set_id = ?)
""", (SET_ID,)).fetchone()[0]

print(f"\nDone! Replaced {old_count} → {new_count} parallels")

# Per-group breakdown
for group_name, is_names in [
    ("Base Set", ["Base Set"]),
    ("Group A (Standard Insert)", ["All Action", "1986 Topps", "Striking Distance"]),
    ("Group B (Hobby Exclusive)", ["Big Ticket", "Split Decision", "Fight Night Flashback", "Pulse Check", "Youthquake", "Sapphire Selections", "Infinite"]),
    ("Group C (Retail Exclusive)", ["Global Warriors", "Allen and Ginter", "Manifesting Moments", "In Your Face", "Impact Point"]),
    ("Group D (SuperFractor Only)", ["Helix", "Let's Go"]),
    ("Auto Group A", ["Base Cards Autograph Variations", "1986 Topps Signatures", "Chrome Lineage Autographs", "Marks of Champions", "Octagon Legends Autographs", "Future Stars Autographs"]),
    ("Auto Group B", ["Quoted Autographs", "Topps 2009 Variation Signatures", "Vanquisher Ink"]),
]:
    ids = []
    for n in is_names:
        r = db.execute("SELECT id FROM insert_sets WHERE set_id = ? AND name = ?", (SET_ID, n)).fetchone()
        if r: ids.append(r[0])
    if ids:
        placeholders = ",".join("?" * len(ids))
        cnt = db.execute(f"SELECT COUNT(*) FROM parallels WHERE insert_set_id IN ({placeholders})", ids).fetchone()[0]
        print(f"  {group_name}: {cnt} parallels across {len(ids)} subsets")

db.close()
