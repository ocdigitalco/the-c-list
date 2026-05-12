"""
Attach parallel matrix and release date to 2025-26 Topps Signature Class Basketball (set 838).
Usage: python3 scripts/fix_signature_class_2025_parallels.py
"""
import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
db = sqlite3.connect(DB_PATH)
db.execute("PRAGMA journal_mode=WAL")

SET_ID = 838

# ─── Step 1: Release date ───────────────────────────────────────────────────
db.execute("UPDATE sets SET release_date = '2026-05-28' WHERE id = ?", (SET_ID,))
print("Set release date to 2026-05-28")

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

HR = "Hobby/Retail"
H = "Hobby"
R = "Retail"

# ─── Step 4: Base Card Parallels ────────────────────────────────────────────

# Veteran Class (Base I) — 17 parallels
veteran_class_pars = [
    # All SKUs
    ("Magenta", 250, HR), ("Teal", 225, HR), ("Indigo", 175, HR),
    ("Green", 150, HR), ("Purple", 100, HR), ("Pink", 75, HR),
    ("Orange", 50, HR), ("Red", 25, HR), ("Red Lava", 25, HR),
    ("Black", 10, HR), ("Black Gold", 10, HR), ("Blue", 5, HR),
    ("Foilfractor", 1, HR),
    # Retail Exclusive
    ("Blue and Orange", None, R), ("Bronze", None, R),
    ("Yellow", 399, R), ("Coral", 299, R),
]

# Rookie Class (Base II) — 17 parallels
rookie_class_pars = [
    # All SKUs
    ("Yellow", 399, HR), ("Coral", 299, HR),
    ("Magenta", 250, HR), ("Teal", 225, HR), ("Indigo", 175, HR),
    ("Green", 150, HR), ("Purple", 100, HR), ("Pink", 75, HR),
    ("Orange", 50, HR), ("Red", 25, HR), ("Red Lava", 25, HR),
    ("Black", 10, HR), ("Black Gold", 10, HR), ("Blue", 5, HR),
    ("Foilfractor", 1, HR),
    # Retail Exclusive
    ("Blue and Orange", None, R), ("Bronze", None, R),
]

# Veteran Class Chrome (Base I Chrome Variation) — 16 parallels
veteran_chrome_pars = [
    # All SKUs
    ("Refractor", None, HR),
    ("Magenta", 250, HR), ("Teal", 225, HR), ("Indigo", 175, HR),
    ("Green", 150, HR), ("Purple", 100, HR), ("Pink", 75, HR),
    ("Orange", 50, HR), ("Red", 25, HR), ("Red Lava", 25, HR),
    ("Gold", 10, HR), ("Blue", 5, HR), ("SuperFractor", 1, HR),
    # Retail Exclusive
    ("Pandora", None, R), ("Pandora Yellow", None, R), ("Yellow", 275, R),
]

# Rookie Class Chrome (Base II Chrome Variation) — 16 parallels
rookie_chrome_pars = [
    # All SKUs (identical to Veteran Chrome)
    ("Refractor", None, HR),
    ("Magenta", 250, HR), ("Teal", 225, HR), ("Indigo", 175, HR),
    ("Green", 150, HR), ("Purple", 100, HR), ("Pink", 75, HR),
    ("Orange", 50, HR), ("Red", 25, HR), ("Red Lava", 25, HR),
    ("Gold", 10, HR), ("Blue", 5, HR), ("SuperFractor", 1, HR),
    # Retail Exclusive
    ("Pandora", None, R), ("Pandora Yellow", None, R), ("Yellow", 275, R),
]

n = add_pars(get_is_id("Base I"), veteran_class_pars)
print(f"  Base I (Veteran Class): {n} parallels")
n = add_pars(get_is_id("Base II"), rookie_class_pars)
print(f"  Base II (Rookie Class): {n} parallels")
n = add_pars(get_is_id("Base I Chrome Variation"), veteran_chrome_pars)
print(f"  Base I Chrome Variation (Veteran Chrome): {n} parallels")
n = add_pars(get_is_id("Base II Chrome Variation"), rookie_chrome_pars)
print(f"  Base II Chrome Variation (Rookie Chrome): {n} parallels")

# ─── Step 5: Insert Parallels (8 subsets × 5 parallels) ─────────────────────
insert_pars = [
    ("Orange", 50, HR), ("Red", 25, HR), ("Gold", 10, HR),
    ("Blue", 5, HR), ("Black", 1, HR),
]

insert_subsets = [
    "After Image", "High Fidelity", "Pure", "Unfazed",
    "Star Cast", "Algorithm", "Roses", "Fluidity",
]
for name in insert_subsets:
    n = add_pars(get_is_id(name), insert_pars)
    print(f"  {name}: {n} parallels")

# ─── Step 6: Case Hit Parallels ─────────────────────────────────────────────
# Hobby-exclusive case hits
hobby_case_pars = [
    ("Orange", 50, H), ("Red", 25, H), ("Gold", 10, H),
    ("Blue", 5, H), ("Black", 1, H),
]
for name in ["Monarchs of the Game", "Leviathans"]:
    n = add_pars(get_is_id(name), hobby_case_pars)
    print(f"  {name} (Hobby case hit): {n} parallels")

# Retail-exclusive case hits
retail_case_pars = [
    ("Orange", 50, R), ("Red", 25, R), ("Gold", 10, R),
    ("Blue", 5, R), ("Black", 1, R),
]
for name in ["Aristocrats", "Odyssey", "Pressure Points"]:
    n = add_pars(get_is_id(name), retail_case_pars)
    print(f"  {name} (Retail case hit): {n} parallels")

# ─── Step 7: Autograph Parallels ────────────────────────────────────────────
# Paper auto ladder (Veteran Class Autographs + Rookie Class Autographs)
paper_auto_pars = [
    ("Purple", 100, HR), ("Orange", 50, HR), ("Red", 25, HR),
    ("Red Lava", 25, HR), ("Gold", 10, HR), ("White Gold", 10, HR),
    ("Blue", 5, HR), ("Black", 1, HR),
]
for name in ["Veteran Class Autographs", "Rookie Class Autographs"]:
    n = add_pars(get_is_id(name), paper_auto_pars)
    print(f"  {name}: {n} parallels")

# Chrome auto ladder (Veteran Class Chrome Autographs + Rookie Class Chrome Autographs)
chrome_auto_pars = [
    ("Orange", 50, HR), ("Red", 25, HR), ("Red Lava", 25, HR),
    ("Gold", 10, HR), ("Blue", 5, HR), ("SuperFractor", 1, HR),
]
for name in ["Veteran Class Chrome Autographs", "Rookie Class Chrome Autographs"]:
    n = add_pars(get_is_id(name), chrome_auto_pars)
    print(f"  {name}: {n} parallels")

# ─── Subsets without parallel data from sell sheet ───────────────────────────
# These auto subsets have no parallel info in the source:
# - Veteran Class Crystal Clear Autographs
# - Rookie Class Crystal Clear Autographs
# - Legends of Their Class Crystal Clear Autographs
# - Penstroke Signatures
# - Shadow Scripts
# - Signature Blend
# - Eternal Marks
# - Manuscripts
# - Dual Autographs
# - Triple Autographs
# TODO: Retail = Mega + Value combined. Sell sheet doesn't separate them.

# ─── Commit & Verify ────────────────────────────────────────────────────────
db.commit()

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
