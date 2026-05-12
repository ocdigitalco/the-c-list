"""
Add full parallel matrix to 2025-26 Topps Hoops Basketball (set 834).
Adds Retail parallels alongside existing Hobby parallels.
Creates missing insert/auto subsets.
Usage: python3 scripts/fix_hoops_2025_parallels.py
"""
import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
db = sqlite3.connect(DB_PATH)
db.execute("PRAGMA journal_mode=WAL")

SET_ID = 834
print(f"Set ID: {SET_ID}")

def get_is_id(name):
    row = db.execute("SELECT id FROM insert_sets WHERE set_id = ? AND name = ?", (SET_ID, name)).fetchone()
    if row: return row[0]
    # Create if missing
    db.execute("INSERT INTO insert_sets (set_id, name) VALUES (?, ?)", (SET_ID, name))
    is_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    print(f"  CREATED insert set: {name} (ID {is_id})")
    return is_id

def add_par(is_id, name, print_run=None):
    # Check if already exists
    exists = db.execute("SELECT id FROM parallels WHERE insert_set_id = ? AND name = ?", (is_id, name)).fetchone()
    if exists:
        return False
    db.execute("INSERT INTO parallels (insert_set_id, name, print_run) VALUES (?, ?, ?)", (is_id, name, print_run))
    return True

def add_parallels_to_subset(is_name, parallels):
    is_id = get_is_id(is_name)
    added = 0
    for name, pr in parallels:
        if add_par(is_id, name, pr):
            added += 1
    total = db.execute("SELECT COUNT(*) FROM parallels WHERE insert_set_id = ?", (is_id,)).fetchone()[0]
    print(f"  {is_name}: +{added} new ({total} total)")

# ─── Fix Dunkumentory → Dunk-Umentory spelling ──────────────────────────────
row = db.execute("SELECT id FROM insert_sets WHERE set_id = ? AND name = 'Dunkumentory'", (SET_ID,)).fetchone()
if row:
    db.execute("UPDATE insert_sets SET name = 'Dunk-Umentory' WHERE id = ?", (row[0],))
    print("  Renamed Dunkumentory → Dunk-Umentory")

# Fix Boombastic → Boom Shaka Laka (if needed — check spec)
# Actually "Boombastic" is a separate Retail case hit per the existing DB.
# The spec lists "Boom Shaka Laka" as a different subset. Keep both.

# ─── RETAIL BASE PARALLELS ──────────────────────────────────────────────────
# Add to Base Set, Base Highlights, Base All-Stars
retail_base_parallels = [
    ("Base Green Hoops", None),           # Value Box exclusive
    ("Base Orange Hoops", None),          # Hanger Box exclusive
    ("Base Rainbow Teal", 299),
    ("Base Rainbow Blue and Yellow", 275),
    ("Base Rainbow Red and Orange", 249),
    ("Base Rainbow Purple and Blue", 199),
    ("Base Light Burst Blue", 149),
    ("Base Light Burst Purple", 99),
    ("Base Light Burst Green", 75),
    ("Base Light Burst Gold", 50),
    ("Base Light Burst Orange", 25),
    ("Base Light Burst Black", 10),
    ("Base Light Burst Red", 5),
    ("Base Light Burst Platinum", 1),
]

# Fix existing hobby parallels — add print runs where missing
hobby_numbered = {
    "Rainbow Yellow": 275,
    "Rainbow Green and Blue": 249,
    "Rainbow Gold and Green": 199,
    "Pixel Burst Blue": 149,
    "Pixel Burst Purple": 99,
    "Pixel Burst Green": 75,
    "Pixel Burst Gold": 50,
    "Pixel Burst Orange": 25,
    "Pixel Burst Black": 10,
    "Pixel Burst Red": 5,
    "Pixel Burst Platinum": 1,
}

for base_subset in ["Base Set", "Base Highlights", "Base All-Stars"]:
    is_id = get_is_id(base_subset)
    # Update print runs on existing Hobby parallels
    for par_name, pr in hobby_numbered.items():
        db.execute("UPDATE parallels SET print_run = ? WHERE insert_set_id = ? AND name = ? AND print_run IS NULL",
                   (pr, is_id, par_name))
    # Add Retail parallels
    add_parallels_to_subset(base_subset, retail_base_parallels)

# ─── GROUP H: Hobby Insert Parallels ─────────────────────────────────────────
hobby_insert_parallels = [
    ("Rainbow", None),
    ("Pixel Burst", None),
    ("Pixel Burst Purple", 99),
    ("Pixel Burst Green", 75),
    ("Pixel Burst Gold", 50),
    ("Pixel Burst Orange", 25),
    ("Pixel Burst Black", 10),
    ("Pixel Burst Red", 5),
    ("Pixel Burst Platinum", 1),
]
for name in ["Bounce House", "Next Episode", "Dunk-Umentory", "Pay Attention", "Hoopers"]:
    add_parallels_to_subset(name, hobby_insert_parallels)

# ─── GROUP R: Retail Insert Parallels ────────────────────────────────────────
retail_insert_parallels = [
    ("Green Hoops", None),
    ("Light Burst", None),
    ("Light Burst Purple", 99),
    ("Light Burst Green", 75),
    ("Light Burst Gold", 50),
    ("Light Burst Orange", 25),
    ("Light Burst Black", 10),
    ("Light Burst Red", 5),
    ("Light Burst Platinum", 1),
]
for name in ["Hardwired", "The Buzz", "Net to Net", "Jam-Packed"]:
    add_parallels_to_subset(name, retail_insert_parallels)

# ─── CASE HITS ───────────────────────────────────────────────────────────────
# Hobby case hits: Platinum 1/1 only
for name in ["Oasis", "Joy", "Checkmate", "Hoopnotic"]:
    add_parallels_to_subset(name, [("Platinum", 1)])

# Retail case hits: Platinum 1/1 only
for name in ["Block by Block", "Boom Shaka Laka"]:
    is_id = get_is_id(name)
    add_parallels_to_subset(name, [("Platinum", 1)])

# Finals Pursuit — multi-tier subset
# The named tiers (First Round through Finals MVP) are individual cards, not parallels.
# TODO(checklist): Finals Pursuit has 7 named tier cards (First Round, Second Round,
# Semi-Finals, The Finals, Champions Team, Champions Players, Finals MVP).
# These are modeled as cards within the subset, not as parallel tiers.
fp_id = get_is_id("Finals Pursuit")
print(f"  Finals Pursuit: exists (tier cards to be added with checklist)")

# ─── AUTOGRAPH PARALLELS ────────────────────────────────────────────────────
# Group AUTO-H1: Full Hobby auto ladder
auto_h1 = [
    ("Pixel Burst Purple", 99),
    ("Pixel Burst Green", 75),
    ("Pixel Burst Gold", 50),
    ("Pixel Burst Orange", 25),
    ("Pixel Burst Black", 10),
    ("Pixel Burst Red", 5),
    ("Pixel Burst Platinum", 1),
]
for name in ["Hoops Rookie Signatures", "Hoops Signs"]:
    add_parallels_to_subset(name, auto_h1)

# Group AUTO-H2: Limited Hobby auto ladder
auto_h2 = [
    ("Pixel Burst Black", 10),
    ("Pixel Burst Red", 5),
    ("Pixel Burst Platinum", 1),
]
for name in ["Hoops Rookie Duals", "Hoops Rookie Triples", "Hoops 1989 Signatures"]:
    add_parallels_to_subset(name, auto_h2)

# Also add Hoops Rookie/Veteran Duals with limited ladder
add_parallels_to_subset("Hoops Rookie/Veteran Duals", auto_h2)

# Group AUTO-R1: Full Retail auto ladder
auto_r1 = [
    ("Light Burst Purple", 99),
    ("Light Burst Green", 75),
    ("Light Burst Gold", 50),
    ("Light Burst Orange", 25),
    ("Light Burst Black", 10),
    ("Light Burst Red", 5),
    ("Light Burst Platinum", 1),
]
for name in ["Hoops Rookie First Signs", "Hoops Hyper Signatures"]:
    add_parallels_to_subset(name, auto_r1)

# Group AUTO-R2: Hoops 1989 Signatures Retail (single parallel)
add_parallels_to_subset("Hoops 1989 Signatures", [("Green Hoops", None)])

# ─── Summary ─────────────────────────────────────────────────────────────────
db.commit()
new_count = db.execute("""
    SELECT COUNT(*) FROM parallels
    WHERE insert_set_id IN (SELECT id FROM insert_sets WHERE set_id = ?)
""", (SET_ID,)).fetchone()[0]
is_count = db.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id = ?", (SET_ID,)).fetchone()[0]

print(f"\nDone! Set ID: {SET_ID}")
print(f"  Insert sets: {is_count}")
print(f"  Total parallels: {new_count} (was 172)")
db.close()
