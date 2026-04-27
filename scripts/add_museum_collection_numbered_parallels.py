"""
Add numbered parallels to 2025 Topps Museum Collection Baseball (set 42).
Usage: python3 scripts/add_museum_collection_numbered_parallels.py
"""
import sqlite3

db = sqlite3.connect('the-c-list.db')
SET_ID = 42

def get_is_id(name):
    row = db.execute("SELECT id FROM insert_sets WHERE set_id = ? AND name = ?", (SET_ID, name)).fetchone()
    if not row:
        print(f"  WARNING: Insert set not found: '{name}'")
        return None
    return row[0]

def add_par(is_id, name, print_run):
    if is_id is None: return
    exists = db.execute("SELECT 1 FROM parallels WHERE insert_set_id = ? AND name = ?", (is_id, name)).fetchone()
    if exists:
        print(f"  SKIP (exists): {name} /{print_run}")
        return
    db.execute("INSERT INTO parallels (insert_set_id, name, print_run) VALUES (?, ?, ?)", (is_id, name, print_run))

added = 0

# Base Set
is_id = get_is_id("Base Set")
if is_id:
    for n, pr in [("Bronze", 35), ("Blue Topaz", 25), ("Black Diamond", 10), ("Diamond", 5), ("Emerald", 1), ("Printing Plates", 1)]:
        add_par(is_id, n, pr); added += 1

# Meaningful Material Relics
is_id = get_is_id("Meaningful Material Relics")
if is_id:
    for n, pr in [("Gold", 75), ("Sapphire", 50), ("Amethyst", 25), ("Ruby", 15), ("Black Diamond", 5), ("Emerald", 1)]:
        add_par(is_id, n, pr); added += 1

# Momentous Material Jumbo Patch Autographs (note: DB has "Momentous" not "Momentus")
is_id = get_is_id("Momentous Material Jumbo Patch Autographs")
if is_id:
    for n, pr in [("Gold", 15), ("Amethyst", 10), ("Ruby", 5), ("Emerald", 1)]:
        add_par(is_id, n, pr); added += 1

# Single Player Signature Swatches Dual Relic Autographs
is_id = get_is_id("Single Player Signature Swatches Dual Relic Autographs")
if is_id:
    for n, pr in [("Gold", 50), ("Sapphire", 25), ("Amethyst", 20), ("Ruby", 15), ("Black Diamond", 10), ("Emerald", 1)]:
        add_par(is_id, n, pr); added += 1

# Single Player Signature Swatches Triple Relic Autographs
is_id = get_is_id("Single Player Signature Swatches Triple Relic Autographs")
if is_id:
    for n, pr in [("Gold", 50), ("Sapphire", 25), ("Amethyst", 20), ("Ruby", 15), ("Black Diamond", 10), ("Emerald", 1)]:
        add_par(is_id, n, pr); added += 1

# Single Player Signature Swatches Quad Relic Autographs
is_id = get_is_id("Single Player Signature Swatches Quad Relic Autographs")
if is_id:
    for n, pr in [("Gold", 50), ("Sapphire", 25), ("Amethyst", 20), ("Ruby", 15), ("Black Diamond", 10), ("Emerald", 1)]:
        add_par(is_id, n, pr); added += 1

# Dual Player Primary Pieces Quad Relics
is_id = get_is_id("Dual Player Primary Pieces Quad Relics")
if is_id:
    for n, pr in [("Gold", 50), ("Sapphire", 25), ("Amethyst", 20), ("Ruby", 10), ("Emerald", 1)]:
        add_par(is_id, n, pr); added += 1

# Dual Player Primary Pieces Quad Relics Legends
is_id = get_is_id("Dual Player Primary Pieces Quad Relics Legends")
if is_id:
    for n, pr in [("Gold", 50), ("Sapphire", 25), ("Amethyst", 20), ("Ruby", 10), ("Emerald", 1)]:
        add_par(is_id, n, pr); added += 1

# Four Player Primary Pieces Quad Relics
is_id = get_is_id("Four Player Primary Pieces Quad Relics")
if is_id:
    for n, pr in [("Gold", 50), ("Sapphire", 25), ("Amethyst", 20), ("Ruby", 10), ("Emerald", 1)]:
        add_par(is_id, n, pr); added += 1

# Archival Autographs
is_id = get_is_id("Archival Autographs")
if is_id:
    for n, pr in [("Amethyst", 25), ("Ruby", 20), ("Blue Topaz", 15), ("Black", 10), ("Emerald", 1)]:
        add_par(is_id, n, pr); added += 1

# Showpieces Autographs
is_id = get_is_id("Showpieces Autographs")
if is_id:
    for n, pr in [("Gold", 10), ("Ruby", 5), ("Emerald", 1)]:
        add_par(is_id, n, pr); added += 1

# Retrospective Signatures
is_id = get_is_id("Retrospective Signatures")
if is_id:
    for n, pr in [("Gold", 75), ("Pink Sapphire", 50), ("Amethyst", 25), ("Ruby", 15), ("Blue Topaz", 10), ("Black", 5), ("Emerald", 1)]:
        add_par(is_id, n, pr); added += 1

# Museum Framed Autographs
is_id = get_is_id("Museum Framed Autographs")
if is_id:
    for n, pr in [("Bronze", 25), ("Silver", 20), ("Gold", 10), ("Black", 5), ("Wood", 1)]:
        add_par(is_id, n, pr); added += 1

# Framed HOF Autographs
is_id = get_is_id("Framed HOF Autographs")
if is_id:
    for n, pr in [("Bronze", 25), ("Silver", 20), ("Gold", 10), ("Black", 5), ("Wood", 1)]:
        add_par(is_id, n, pr); added += 1

# Dual On Card Autographs
is_id = get_is_id("Dual On Card Autographs")
if is_id:
    for n, pr in [("Gold", 10), ("Ruby", 5), ("Emerald", 1)]:
        add_par(is_id, n, pr); added += 1

# Triple On Card Autographs
is_id = get_is_id("Triple On Card Autographs")
if is_id:
    for n, pr in [("Gold", 10), ("Ruby", 5), ("Emerald", 1)]:
        add_par(is_id, n, pr); added += 1

# Museum Framed Autograph Patch Cards
is_id = get_is_id("Museum Framed Autograph Patch Cards")
if is_id:
    for n, pr in [("Gold", 10), ("Black", 5), ("Silver", 1)]:
        add_par(is_id, n, pr); added += 1

# Museum Framed Dual Autograph Patch Book Cards
is_id = get_is_id("Museum Framed Dual Autograph Patch Book Cards")
if is_id:
    for n, pr in [("Gold", 10), ("Black", 5), ("Silver", 1)]:
        add_par(is_id, n, pr); added += 1

# Autographed Jumbo Lumber Bat Relics
is_id = get_is_id("Autographed Jumbo Lumber Bat Relics")
if is_id:
    for n, pr in [("Gold", 10)]:
        add_par(is_id, n, pr); added += 1

# Dual Autographed Jumbo Lumber Bat Relics Book Cards
is_id = get_is_id("Dual Autographed Jumbo Lumber Bat Relics Book Cards")
if is_id:
    for n, pr in [("Gold", 10), ("Emerald", 1)]:
        add_par(is_id, n, pr); added += 1

# Momentous Material Dual Jumbo Patch Autograph Book Cards
is_id = get_is_id("Momentous Material Dual Jumbo Patch Autograph Book Cards")
if is_id:
    for n, pr in [("Gold", 10), ("Emerald", 1)]:
        add_par(is_id, n, pr); added += 1

# MLB Authenticated Relic Autograph Cards
is_id = get_is_id("MLB Authenticated Relic Autograph Cards")
if is_id:
    for n, pr in [("Ruby", 5), ("Emerald", 1)]:
        add_par(is_id, n, pr); added += 1

# Museum Quality Cut Signatures
is_id = get_is_id("Museum Quality Cut Signatures")
if is_id:
    for n, pr in [("Base", 5)]:
        add_par(is_id, n, pr); added += 1

# Museum Quality Cut Signature Relics
is_id = get_is_id("Museum Quality Cut Signature Relics")
if is_id:
    for n, pr in [("Base", 5)]:
        add_par(is_id, n, pr); added += 1

db.commit()
print(f"\nDone. {added} parallels added.")
db.close()
