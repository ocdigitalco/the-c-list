"""
Attach correct parallel matrix to 2025 Topps Finest Football (set 842).
Replaces initial placeholder parallels with exact Hobby + Breaker's Delight ladders.
Also adds Breaker's Delight box config.
Usage: python3 scripts/fix_finest_football_2025_parallels.py
"""
import sqlite3, os, json

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
db = sqlite3.connect(DB_PATH)
db.execute("PRAGMA journal_mode=WAL")

SET_ID = 842

# ─── Step 1: Delete existing parallels for this set ─────────────────────────
db.execute("""
    DELETE FROM parallels WHERE insert_set_id IN (
        SELECT id FROM insert_sets WHERE set_id = ?
    )
""", (SET_ID,))
deleted = db.total_changes
print(f"Deleted {deleted} existing parallels for set {SET_ID}")

# ─── Step 2: Update box config to include Breaker's Delight ─────────────────
box_config = json.dumps({
    "hobby": {
        "cards_per_pack": 10,
        "packs_per_box": 6,
        "boxes_per_case": 8,
        "notes": "Per box: 2 autographs, 11 numbered parallels, 10 inserts"
    },
    "breakers_delight": {
        "cards_per_pack": 10,
        "packs_per_box": 1,
        "boxes_per_case": None,
        "notes": "Per box: 3 autographs, 2 case inserts, 5 geometric parallels"
    }
})
db.execute("UPDATE sets SET box_config = ? WHERE id = ?", (box_config, SET_ID))
print("Updated box config with Breaker's Delight")

# ─── Helpers ─────────────────────────────────────────────────────────────────
def get_is_id(name):
    row = db.execute("SELECT id FROM insert_sets WHERE set_id = ? AND name = ?", (SET_ID, name)).fetchone()
    if not row:
        raise ValueError(f"Insert set '{name}' not found for set {SET_ID}")
    return row[0]

def add_pars(is_id, parallels):
    for name, print_run, excl in parallels:
        db.execute(
            "INSERT INTO parallels (insert_set_id, name, print_run, exclusivity) VALUES (?, ?, ?, ?)",
            (is_id, name, print_run, excl)
        )
    return len(parallels)

H = "Hobby"
D = "Delight"

# ─── Step 3: Base Card Parallels ────────────────────────────────────────────

# Base Common (21 parallels)
base_common_pars = [
    ("Refractor", None, H),
    ("Oil Spill", None, H),
    ("X-Fractor", None, H),
    ("Sky Blue", 325, H),
    ("Purple", 250, H),
    ("Blue", 200, H),
    ("X-Fractor Purple", 150, H),
    ("Purple Geometric", 150, D),
    ("X-Fractor Blue", 99, H),
    ("Blue Geometric", 99, D),
    ("Green", 75, H),
    ("Green Geometric", 75, D),
    ("Gold", 50, H),
    ("Gold Geometric", 50, D),
    ("Orange", 25, H),
    ("Orange Geometric", 25, D),
    ("Black", 20, H),
    ("Black Geometric", 20, D),
    ("Red", 10, H),
    ("Red Geometric", 10, D),
    ("Superfractor", 1, H),
]

# Base Uncommon (20 parallels — no Purple Geometric)
base_uncommon_pars = [
    ("Refractor", None, H),
    ("Oil Spill", None, H),
    ("X-Fractor", None, H),
    ("Sky Blue", 250, H),
    ("Purple", 200, H),
    ("Blue", 150, H),
    ("X-Fractor Purple", 99, H),
    ("X-Fractor Blue", 75, H),
    ("Blue Geometric", 75, D),
    ("Green", 35, H),
    ("Green Geometric", 35, D),
    ("Gold", 25, H),
    ("Gold Geometric", 25, D),
    ("Orange", 20, H),
    ("Orange Geometric", 20, D),
    ("Black", 15, H),
    ("Black Geometric", 15, D),
    ("Red", 5, H),
    ("Red Geometric", 5, D),
    ("Superfractor", 1, H),
]

# Base Rare (19 parallels — no Blue Geometric, no Purple Geometric)
base_rare_pars = [
    ("Refractor", None, H),
    ("Oil Spill", None, H),
    ("X-Fractor", None, H),
    ("Sky Blue", 150, H),
    ("Purple", 125, H),
    ("Blue", 99, H),
    ("X-Fractor Purple", 75, H),
    ("X-Fractor Blue", 49, H),
    ("Green", 25, H),
    ("Green Geometric", 25, D),
    ("Gold", 20, H),
    ("Gold Geometric", 20, D),
    ("Orange", 15, H),
    ("Orange Geometric", 15, D),
    ("Black", 10, H),
    ("Black Geometric", 10, D),
    ("Red", 3, H),
    ("Red Geometric", 3, D),
    ("Superfractor", 1, H),
]

n = add_pars(get_is_id("Base Cards Common"), base_common_pars)
print(f"  Base Cards Common: {n} parallels")
n = add_pars(get_is_id("Base Cards Uncommon"), base_uncommon_pars)
print(f"  Base Cards Uncommon: {n} parallels")
n = add_pars(get_is_id("Base Cards Rare"), base_rare_pars)
print(f"  Base Cards Rare: {n} parallels")

# ─── Step 4: Autograph Parallels (5 subsets × 12 parallels) ─────────────────
auto_pars = [
    ("Refractor", None, H),
    ("Blue", 99, H),
    ("Blue Geometric", 99, D),
    ("Gold", 50, H),
    ("Gold Geometric", 50, D),
    ("Orange", 25, H),
    ("Orange Geometric", 25, D),
    ("Black", 10, H),
    ("Black Geometric", 10, D),
    ("Red", 5, H),
    ("Red Geometric", 5, D),
    ("Superfractor", 1, H),
]

auto_subsets = [
    "Finest Autographs",
    "Rookie Finest Autographs",
    "Flashback Autographs",
    "Finest Freshman Autographs",
    "Finest Greats Autographs",
]
for name in auto_subsets:
    n = add_pars(get_is_id(name), auto_pars)
    print(f"  {name}: {n} parallels")

# ─── Step 5: Insert Ladder A (5 subsets × 14 parallels) ─────────────────────
insert_a_pars = [
    ("Refractor", None, H),
    ("X-Fractor", None, H),
    ("Sky Blue", 150, H),
    ("Purple", 125, H),
    ("Blue", 99, H),
    ("Green", 75, H),
    ("Gold", 50, H),
    ("Orange", 25, H),
    ("Orange Geometric", 25, D),
    ("Black", 10, H),
    ("Black Geometric", 10, D),
    ("Red", 5, H),
    ("Red Geometric", 5, D),
    ("Superfractor", 1, H),
]

insert_a_subsets = ["Reflash", "Torchers", "Power Kings", "Creators", "Team Finest"]
for name in insert_a_subsets:
    n = add_pars(get_is_id(name), insert_a_pars)
    print(f"  {name}: {n} parallels")

# ─── Insert Ladder B (2 subsets × 1 parallel) ───────────────────────────────
insert_b_pars = [
    ("Superfractor", 1, H),
]

insert_b_subsets = ["92 Finest", "Headliners"]
for name in insert_b_subsets:
    n = add_pars(get_is_id(name), insert_b_pars)
    print(f"  {name}: {n} parallels")

# ─── Step 6: Subsets without parallel data (left at 0) ──────────────────────
# TODO: Parallels for these subsets need confirmation from sell sheet:
#   Centurions, The Man, For The Record, Framed White, Nightmare Fuel,
#   Smashing Through, Landmark Metal Series, Finest Moments Autographs,
#   Finest Fans Autographs
no_parallel_subsets = [
    "Centurions", "The Man", "For The Record", "Framed White",
    "Nightmare Fuel", "Smashing Through", "Landmark Metal Series",
    "Finest Moments Autographs", "Finest Fans Autographs",
]
print(f"\n  {len(no_parallel_subsets)} subsets left without parallels (pending confirmation)")

# ─── Commit & Verify ────────────────────────────────────────────────────────
db.commit()

# Verify counts
print("\n--- Verification ---")
rows = db.execute("""
    SELECT ins.name,
           (SELECT COUNT(*) FROM parallels p WHERE p.insert_set_id = ins.id) as cnt
    FROM insert_sets ins
    WHERE ins.set_id = ?
    ORDER BY ins.name
""", (SET_ID,)).fetchall()

total = 0
for name, cnt in rows:
    print(f"  {name}: {cnt}")
    total += cnt

print(f"\nTotal parallels: {total}")

# Exclusivity distribution
excl_rows = db.execute("""
    SELECT p.exclusivity, COUNT(*) FROM parallels p
    JOIN insert_sets ins ON p.insert_set_id = ins.id
    WHERE ins.set_id = ?
    GROUP BY p.exclusivity
""", (SET_ID,)).fetchall()
print("\nExclusivity distribution:")
for excl, cnt in excl_rows:
    print(f"  {excl}: {cnt}")

db.close()
print("\nDone!")
