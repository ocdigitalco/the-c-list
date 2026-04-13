"""
Add parallels to 2025-26 Topps Bowman Basketball (set id 34).
Usage: python3 scripts/add_bowman_basketball_parallels.py
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA foreign_keys=ON")
cur = conn.cursor()

count = 0

def add(is_id, name, pr):
    global count
    cur.execute("INSERT INTO parallels (insert_set_id, name, print_run) VALUES (?, ?, ?)", (is_id, name, pr))
    count += 1

# ── Base Set (755) ────────────────────────────────────────────────────────────
IS = 755
add(IS, "Purple Pattern Border", 199)
add(IS, "Pink Border", 175)
add(IS, "Blue Border", 150)
add(IS, "Blue Pattern", 125)
add(IS, "Bowman Logo Pattern Parallel", 100)
add(IS, "Green Border", 99)
add(IS, "Green Pattern Border", 99)
add(IS, "Yellow Border", 75)
add(IS, "Gold Border", 50)
add(IS, "Orange Border", 25)
add(IS, "Black Border", 10)
add(IS, "Black Pattern Border", 10)
add(IS, "Red Border", 5)
add(IS, "Platinum Border (Rainbow Foil)", 1)

# ── Base Chrome Variation (756) ───────────────────────────────────────────────
IS = 756
add(IS, "Geometric", None)
add(IS, "Mojo Refractor", None)
add(IS, "Reptilian Refractor", None)
add(IS, "Mini-Diamond Refractor", None)
add(IS, "Refractor", 499)
add(IS, "Lava Refractor", 399)
add(IS, "Fuchsia Mojo", 299)
add(IS, "Speckle Refractor", 299)
add(IS, "Burgundy Mojo", 275)
add(IS, "Purple Refractor", 250)
add(IS, "Purple Mojo", 250)
add(IS, "Fuchsia Refractor", 199)
add(IS, "Reptilian Fuchsia Refractor", 199)
add(IS, "Pink Mojo", 199)
add(IS, "Navy Mojo", 175)
add(IS, "Blue Refractor", 150)
add(IS, "Reptilian Blue Refractor", 150)
add(IS, "Blue Shimmer", 150)
add(IS, "Blue Mojo", 150)
add(IS, "Aqua Mojo", 125)
add(IS, "Floorboard Refractor", 125)
add(IS, "Steel Metal Refractor", 100)
add(IS, "Green Refractor", 99)
add(IS, "Green Mojo", 99)
add(IS, "Reptilian Green Refractor", 99)
add(IS, "Green Shimmer Refractor", 99)
add(IS, "Green Geometric", 99)
add(IS, "Yellow Refractor", 75)
add(IS, "Yellow X-Fractor", 75)
add(IS, "Yellow Wave Refractor", 75)
add(IS, "Yellow Mojo", 75)
add(IS, "Gold Refractor", 50)
add(IS, "Gold Shimmer Refractor", 50)
add(IS, "Reptilian Gold Refractor", 50)
add(IS, "Gold Mojo", 50)
add(IS, "Gold Geometric", 50)
add(IS, "Orange Refractor", 25)
add(IS, "Orange Shimmer Refractor", 25)
add(IS, "Reptilian Orange Refractor", 25)
add(IS, "Orange Mojo", 25)
add(IS, "Orange Geometric", 25)
add(IS, "Rose Gold Refractor", 15)
add(IS, "Rose Gold Mini-Diamond Refractor", 15)
add(IS, "Rose Gold X-Fractor", 15)
add(IS, "Black Refractor", 10)
add(IS, "Black X-Fractor", 10)
add(IS, "Black Geometric", 10)
add(IS, "Red Refractor", 5)
add(IS, "Red Lava Refractor", 5)
add(IS, "Red Mojo", 5)
add(IS, "Red X-Fractor", 5)
add(IS, "Reptilian Red Refractor", 5)
add(IS, "Red Geometric", 5)
add(IS, "FireFractor", 3)
add(IS, "Superfractor", 1)
add(IS, "Rose Gold Mojo", 1)

# ── Retrofractor Variations (759) ─────────────────────────────────────────────
IS = 759
add(IS, "Gold Refractor", 50)
add(IS, "Orange Refractor", 25)
add(IS, "Red Refractor", 5)
add(IS, "Superfractor", 1)

# ── Base Prospects (760) ──────────────────────────────────────────────────────
IS = 760
add(IS, "Purple Pattern Border", 199)
add(IS, "Pink Border", 175)
add(IS, "Blue Border", 150)
add(IS, "Blue Pattern", 125)
add(IS, "Bowman Logo Pattern Parallel", 100)
add(IS, "Green Border", 99)
add(IS, "Green Pattern Border", 99)
add(IS, "Yellow Border", 75)
add(IS, "Gold Border", 50)
add(IS, "Orange Border", 25)
add(IS, "Black Border", 10)
add(IS, "Black Pattern Border", 10)
add(IS, "Red Border", 5)
add(IS, "Platinum Border (Rainbow Foil)", 1)

# ── Chrome Prospects (761) — Base Chrome Prospects parallels ──────────────────
IS = 761
add(IS, "Geometric Refractor", None)
add(IS, "Mojo Refractor", None)
add(IS, "Reptilian Refractor", None)
add(IS, "Mini-Diamond Refractor", None)
add(IS, "Refractor", 499)
add(IS, "Lava Refractor", 399)
add(IS, "Fuchsia Mojo", 299)
add(IS, "Speckle Refractor", 299)
add(IS, "Burgundy Mojo", 275)
add(IS, "Purple Refractor", 250)
add(IS, "Purple Mojo", 250)
add(IS, "Fuchsia Refractor", 199)
add(IS, "Reptilian Fuchsia Refractor", 199)
add(IS, "Pink Mojo", 199)
add(IS, "Navy Mojo", 175)
add(IS, "Reptilian Blue Refractor", 150)
add(IS, "Blue Refractor", 150)
add(IS, "Blue Mojo", 150)
add(IS, "Aqua Mojo", 125)
add(IS, "Aqua X-Fractor", 125)
add(IS, "Floorboard Refractor", 125)
add(IS, "Steel Metal Refractor", 100)
add(IS, "Green Refractor", 99)
add(IS, "Green Mojo", 99)
add(IS, "Reptilian Green Refractor", 99)
add(IS, "Green Shimmer Refractor", 99)
add(IS, "Green Geometric", 99)
add(IS, "Yellow Refractor", 75)
add(IS, "Yellow X-Fractor", 75)
add(IS, "Yellow Mojo", 75)
add(IS, "Gold Refractor", 50)
add(IS, "Reptilian Gold Refractor", 50)
add(IS, "Gold Geometric", 50)
add(IS, "Gold Mojo", 50)
add(IS, "Orange Refractor", 25)
add(IS, "Reptilian Orange Refractor", 25)
add(IS, "Orange Mojo", 25)
add(IS, "Orange Geometric", 25)
add(IS, "Rose Gold Refractor", 15)
add(IS, "Rose Gold Mini-Diamond Refractor", 15)
add(IS, "Black Refractor", 10)
add(IS, "Black X-Fractor", 10)
add(IS, "Black Geometric", 10)
add(IS, "Red Refractor", 5)
add(IS, "Reptilian Red Refractor", 5)
add(IS, "Red Mojo", 5)
add(IS, "Red Geometric", 5)
add(IS, "Superfractor", 1)
add(IS, "Rose Gold Mojo", 1)

# ── Chrome Prospect Autographs (763) ──────────────────────────────────────────
IS = 763
add(IS, "Refractor", 499)
add(IS, "Speckle Refractor", 299)
add(IS, "Purple Refractor", 250)
add(IS, "Blue Refractor", 150)
add(IS, "Blue X-Fractor", 150)
add(IS, "Mini-Diamond Refractor", 100)
add(IS, "Green Refractor", None)
add(IS, "Green Geometric", 99)
add(IS, "Green Shimmer Refractor", 99)
add(IS, "Reptilian Green Refractor", 99)
add(IS, "Yellow Refractor", 75)
add(IS, "Gold Refractor", 50)
add(IS, "Gold Geometric", 50)
add(IS, "Gold Shimmer Refractor", 50)
add(IS, "Reptilian Orange Refractor", 25)
add(IS, "Orange Refractor", 25)
add(IS, "Orange Geometric", 25)
add(IS, "Orange Shimmer Refractor", 25)
add(IS, "Black Refractor", 10)
add(IS, "Black Geometric", 10)
add(IS, "Black X-Fractor Refractor", 10)
add(IS, "Red Refractor", 5)
add(IS, "Red Geometric", 5)
add(IS, "Red Lava Refractor", 5)
add(IS, "Superfractor", 1)

# ── Chrome Autographs (764) ───────────────────────────────────────────────────
IS = 764
add(IS, "Refractor", 499)
add(IS, "Speckle Refractor", 299)
add(IS, "Purple Refractor", 250)
add(IS, "Blue Refractor", 150)
add(IS, "Blue X-Fractor", 150)
add(IS, "Mini-Diamond Refractor", 100)
add(IS, "Green Refractor", None)
add(IS, "Green Geometric", 99)
add(IS, "Green Shimmer Refractor", 99)
add(IS, "Reptilian Green Refractor", 99)
add(IS, "Yellow Refractor", 75)
add(IS, "Gold Refractor", 50)
add(IS, "Gold Geometric", 50)
add(IS, "Gold Shimmer Refractor", 50)
add(IS, "Reptilian Orange Refractor", 25)
add(IS, "Orange Refractor", 25)
add(IS, "Orange Geometric", 25)
add(IS, "Orange Shimmer Refractor", 25)
add(IS, "Black Refractor", 10)
add(IS, "Black Geometric", 10)
add(IS, "Black X-Fractor Refractor", 10)
add(IS, "Red Refractor", 5)
add(IS, "Red Geometric", 5)
add(IS, "Red Lava Refractor", 5)
add(IS, "Superfractor", 1)

# ── Retrofractor Autographs (765) ─────────────────────────────────────────────
IS = 765
add(IS, "Gold Refractor", 50)
add(IS, "Orange Refractor", 25)
add(IS, "Red Refractor", 5)
add(IS, "FireFractor", 3)
add(IS, "Superfractor", 1)

# ── Future Script Autographs (766) ────────────────────────────────────────────
IS = 766
add(IS, "Gold Refractor", 50)
add(IS, "Orange Refractor", 25)
add(IS, "Black Refractor", 10)
add(IS, "Red Refractor", 5)
add(IS, "Superfractor", 1)

# ── Buzz Factor Autographs (767) ──────────────────────────────────────────────
IS = 767
add(IS, "Gold Refractor", 50)
add(IS, "Orange Refractor", 25)
add(IS, "Black Refractor", 10)
add(IS, "Red Refractor", 5)
add(IS, "Superfractor", 1)

# ── Opening Statement Signatures (768) ────────────────────────────────────────
IS = 768
add(IS, "Gold Refractor", 50)
add(IS, "Orange Refractor", 25)
add(IS, "Black Refractor", 10)
add(IS, "Red Refractor", 5)
add(IS, "Superfractor", 1)

# ── Timeless Touch Signatures (769) ───────────────────────────────────────────
IS = 769
add(IS, "Gold Refractor", 50)
add(IS, "Orange Refractor", 25)
add(IS, "Black Refractor", 10)
add(IS, "Red Refractor", 5)
add(IS, "Superfractor", 1)

# ── Paper Prospect Retail Autographs (770) ────────────────────────────────────
IS = 770
add(IS, "Blue Border", 150)
add(IS, "Green Border", 99)
add(IS, "Gold Border", 50)
add(IS, "Orange Border", 25)
add(IS, "Red Border", 5)
add(IS, "Platinum Border", 1)

# ── Paper Rookie and Veterans Retail Autographs (771) ─────────────────────────
IS = 771
add(IS, "Blue Border", 150)
add(IS, "Green Border", 99)
add(IS, "Gold Border", 50)
add(IS, "Orange Border", 25)
add(IS, "Red Border", 5)
add(IS, "Platinum Border", 1)

# ── Bowman Dual Autographs (772) ──────────────────────────────────────────────
IS = 772
add(IS, "Superfractor", 1)

# ── Shared insert parallels (773-781) ─────────────────────────────────────────
SHARED_INSERT_IDS = [773, 774, 775, 776, 777, 778, 779, 780, 781]
SHARED_PARS = [
    ("Refractor", None),
    ("Geometric Refractor", None),
    ("Purple Refractor", 250),
    ("Fuchsia Refractor", 199),
    ("Mini-Diamond Refractor", 150),
    ("Aqua Refractor", 125),
    ("Green Refractor", 99),
    ("Gold Refractor", 50),
    ("Gold Geometric", 50),
    ("Orange Refractor", 25),
    ("Orange Geometric", 25),
    ("Black Geometric", 10),
    ("Red Refractor", 5),
    ("Red Geometric", 5),
    ("Superfractor", 1),
]
for is_id in SHARED_INSERT_IDS:
    for name, pr in SHARED_PARS:
        add(is_id, name, pr)

# ── Bowman Spotlights NBA (784) ───────────────────────────────────────────────
IS = 784
add(IS, "Red Refractor", 5)
add(IS, "Superfractor", 1)

# ── Bowman Spotlights NIL (785) ───────────────────────────────────────────────
IS = 785
add(IS, "Red Refractor", 5)
add(IS, "Superfractor", 1)

# ── Crystallized NBA (786) ────────────────────────────────────────────────────
IS = 786
add(IS, "Gold Crystal Refractor", 50)
add(IS, "Orange Crystal Refractor", 25)
add(IS, "Red Crystal Refractor", 5)
add(IS, "Superfractor", 1)

# ── Crystallized NIL (787) ────────────────────────────────────────────────────
IS = 787
add(IS, "Gold Crystal Refractor", 50)
add(IS, "Orange Crystal Refractor", 25)
add(IS, "Red Crystal Refractor", 5)
add(IS, "Superfractor", 1)

# ── Anime NBA (788) ──────────────────────────────────────────────────────────
IS = 788
add(IS, "Black Refractor", 10)
add(IS, "Red Refractor", 5)
add(IS, "Superfractor", 1)

# ── Anime NIL (789) ──────────────────────────────────────────────────────────
IS = 789
add(IS, "Black Refractor", 10)
add(IS, "Red Refractor", 5)
add(IS, "Superfractor", 1)

# ── Bowman GPK NBA (790) ─────────────────────────────────────────────────────
IS = 790
add(IS, "Red Refractor", 5)
add(IS, "Superfractor", 1)

# ── Bowman GPK NIL (791) ─────────────────────────────────────────────────────
IS = 791
add(IS, "Red Refractor", 5)
add(IS, "Superfractor", 1)

conn.commit()

# ── Recompute player stats ────────────────────────────────────────────────────
print(f"Added {count} parallels")
print("Recomputing player stats...")

cur.execute("SELECT id FROM players WHERE set_id = 34")
player_ids = [r[0] for r in cur.fetchall()]

for pid in player_ids:
    cur.execute("SELECT pa.id, pa.insert_set_id FROM player_appearances pa WHERE pa.player_id = ?", (pid,))
    appearances = cur.fetchall()
    insert_set_ids = set(a[1] for a in appearances)
    unique_cards = 0
    total_print_run = 0
    one_of_ones = 0
    for app_id, is_id in appearances:
        unique_cards += 1
        cur.execute("SELECT name, print_run FROM parallels WHERE insert_set_id = ?", (is_id,))
        for par_name, pr in cur.fetchall():
            unique_cards += 1
            if pr is not None:
                total_print_run += pr
                if pr == 1: one_of_ones += 1
    cur.execute("UPDATE players SET unique_cards = ?, total_print_run = ?, one_of_ones = ?, insert_set_count = ? WHERE id = ?",
                (unique_cards, total_print_run, one_of_ones, len(insert_set_ids), pid))

conn.commit()
conn.close()
print("Done!")
