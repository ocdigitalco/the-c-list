"""Add parallels to 2025 Topps Chrome Football (set 44)."""
import sqlite3, os

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

# Map insert set names to IDs
IS = {}
cur.execute("SELECT id, name FROM insert_sets WHERE set_id = 44")
for r in cur.fetchall():
    IS[r[1]] = r[0]

def get_is(name):
    if name in IS: return IS[name]
    print(f"  WARNING: Could not find insert set '{name}'")
    return None

# ── BASE PARALLELS (shared by Veterans and Rookies) ──────────────────────────

BASE_VETS_PARS = [
    ("Refractor",None),("Geometric Refractor",None),("Football Leather Refractor",None),("Hot Pink X-Fractor Refractor",None),("Lime Green X-Fractor Refractor",None),("Neon Pulse Refractor",None),("Prism Refractor",None),("Pulsar Refractor",None),("RayWave Refractor",None),("Red White and Blue Refractor",None),("Topps Refractor",None),("Touchdown Refractor",None),("X-Fractor",None),
    ("Teal Refractor",299),("Yellow Wave Refractor",275),("Pink Refractor",250),("Pink Wave Refractor",250),("Aqua Refractor",199),("Aqua Wave Refractor",199),("Blue Refractor",150),("Blue Wave Refractor",150),("Green Refractor",99),("Green Lava Refractor",99),("Green Wave Refractor",99),("Football Leather Green",99),("Purple Refractor",75),("Purple Lava Refractor",75),("Purple Wave Refractor",75),("Football Leather Purple",75),("Gold Refractor",50),("Gold Lava Refractor",50),("Gold Wave Refractor",50),("Gold Geometric Refractor",50),("Football Leather Gold",50),("White Refractor",30),("Orange Refractor",25),("Orange Lava Refractor",25),("Orange Wave Refractor",25),("Orange Geometric Refractor",25),("Football Leather Orange",25),("Black Refractor",10),("Black Lava Refractor",10),("Black Wave Refractor",10),("Black Geometric Refractor",10),("Football Leather Black",10),("Molten Mercury First Day Issue Refractor",6),("Red Refractor",5),("Red Lava Refractor",5),("Red Wave Refractor",5),("Red Geometric Refractor",5),("Football Leather Red",5),("Frozenfractor",5),("Tie Dye Geometric Refractor",2),("Superfractor",1),
]

BASE_ROOKIES_PARS = [
    ("Refractor",None),("Geometric Refractor",None),("Football Leather Refractor",None),("Hot Pink X-Fractor Refractor",None),("Lime Green X-Fractor Refractor",None),("Neon Pulse Refractor",None),("Prism Refractor",None),("Pulsar Refractor",None),("RayWave Refractor",None),("Red White and Blue Refractor",None),("Topps Refractor",None),("Touchdown Refractor",None),("X-Fractor",None),
    ("Teal Refractor",299),("Teal Wave Refractor",299),("Yellow Wave Refractor",275),("Pink Refractor",250),("Pink Wave Refractor",250),("Aqua Refractor",199),("Aqua Wave Refractor",199),("Blue Refractor",150),("Blue Wave Refractor",150),("Blue Geometric Refractor",150),("Football Leather Blue",150),("Green Refractor",99),("Green Lava Refractor",99),("Green Wave Refractor",99),("Green Geometric Refractor",99),("Football Leather Green",99),("Purple Refractor",75),("Purple Lava Refractor",75),("Purple Wave Refractor",75),("Purple Geometric Refractor",75),("Football Leather Purple",75),("Gold Refractor",50),("Gold Lava Refractor",50),("Gold Wave Refractor",50),("Gold Geometric Refractor",50),("Football Leather Gold",50),("White Refractor",30),("Orange Refractor",25),("Orange Lava Refractor",25),("Orange Wave Refractor",25),("Orange Geometric Refractor",25),("Football Leather Orange",25),("Black Refractor",10),("Black Lava Refractor",10),("Black Wave Refractor",10),("Black Geometric Refractor",10),("Football Leather Black",10),("Molten Mercury First Day Issue Refractor",6),("Red Refractor",5),("Red Lava Refractor",5),("Red Wave Refractor",5),("Red Geometric Refractor",5),("Football Leather Red",5),("Frozenfractor",5),("Tie Dye Geometric Refractor",2),("Superfractor",1),
]

# Base Set (949) = Veterans
is_id = get_is("Base Set")
if is_id:
    for n, p in BASE_VETS_PARS: add(is_id, n, p)

# Base Cards Autograph Variation (972) = Rookies base
is_id = get_is("Base Cards Autograph Variation")
# Actually need to find the Rookies base. Looking at the IS list, there's no "Base - Rookies".
# The base set likely includes both vets and rookies. Let me check if 972 is the rookies auto or
# if there's a separate rookies base. Since there's "Rookies Autograph Variation" (973), let me
# apply rookies parallels to 973 and vets auto to 972.

# Actually, re-reading the IS list: 949=Base Set covers all base cards (vets+rookies).
# There's no separate "Base - Rookies" insert set. The rookies are part of 949.
# So I'll apply the rookies parallel list to the same Base Set, but since they share most parallels
# and the DB has one parallel list per insert set, the rookies-specific extras (Blue Geometric etc)
# are additions. Let me just add the extras that aren't in the vets list.

# Rookies-only extras (not in vets list):
rookies_extras = [("Teal Wave Refractor",299),("Blue Geometric Refractor",150),("Football Leather Blue",150),("Green Geometric Refractor",99),("Purple Geometric Refractor",75)]
if is_id:
    for n, p in rookies_extras: add(is_id, n, p)

# Base - Chrome Base Etch Variation (952)
is_id = get_is("Base - Chrome Base Etch Variation")
if is_id:
    for n, p in [("Gold",50),("Orange",25),("Black",10),("Red",5),("Superfractor",1)]: add(is_id, n, p)

# Base - Chrome Rookies Etch Variation (953)
is_id = get_is("Base - Chrome Rookies Etch Variation")
if is_id:
    for n, p in [("Gold",50),("Orange",25),("Black",10),("Red",5),("Superfractor",1)]: add(is_id, n, p)

# Base - Image Variation (954)
IMG_VAR_PARS = [("Green Refractor",99),("Green Geometric Refractor",99),("Purple Geometric Refractor",75),("Gold Refractor",50),("Gold Geometric Refractor",50),("White Refractor",30),("Orange Refractor",25),("Orange Geometric Refractor",25),("Black Refractor",10),("Black Geometric Refractor",10),("First Day Issue",6),("Red Refractor",5),("Red Geometric Refractor",5),("Tie Dye Geometric Refractor",2),("Superfractor",1)]
is_id = get_is("Base - Image Variation")
if is_id:
    for n, p in IMG_VAR_PARS: add(is_id, n, p)

# Base - Rookies Image Variation (955)
is_id = get_is("Base - Rookies Image Variation")
if is_id:
    for n, p in IMG_VAR_PARS: add(is_id, n, p)

# Base - Lightboard Logo Variation (951) + Base - Team Camo Variation (950)
is_id = get_is("Base - Lightboard Logo Variation")
if is_id: add(is_id, "Lightboard Logo Variation", None)
is_id = get_is("Base - Team Camo Variation")
if is_id: add(is_id, "Team Camo Variation", None)

# Chrome Autographs (972 = Base Cards Autograph Variation)
CHROME_AUTO_PARS = [("Refractor",499),("Magenta Refractor",399),("Magenta Lava Refractor",399),("Teal Refractor",299),("Teal Lava Refractor",299),("Yellow Refractor",275),("Yellow Lava Refractor",275),("Pink Refractor",250),("Pink Lava Refractor",250),("Aqua Refractor",199),("Aqua Lava Refractor",199),("Blue Refractor",150),("Blue Lava Refractor",150),("Green Refractor",99),("Green Lava Refractor",99),("Green Geometric Refractor",99),("Purple Refractor",75),("Purple Lava Refractor",75),("Purple Geometric Refractor",75),("Gold Refractor",50),("Gold Lava Refractor",50),("Gold Wave Refractor",50),("Gold Geometric Refractor",50),("White Refractor",30),("Orange Refractor",25),("Orange Lava Refractor",25),("Orange Wave Refractor",25),("Orange Geometric Refractor",25),("First Day Issue",14),("Black Refractor",10),("Black Lava Refractor",10),("Black Wave Refractor",10),("Black Geometric Refractor",10),("Red Refractor",5),("Red Lava Refractor",5),("Red Wave Refractor",5),("Red Geometric Refractor",5),("Tie Dye Geometric Refractor",2),("Superfractor",1)]

is_id = get_is("Base Cards Autograph Variation")
if is_id:
    for n, p in CHROME_AUTO_PARS: add(is_id, n, p)

# Rookies Autograph Variation (973)
is_id = get_is("Rookies Autograph Variation")
if is_id:
    for n, p in CHROME_AUTO_PARS: add(is_id, n, p)

# Chrome Legends Autographs (977)
LEGENDS_AUTO_PARS = [("Gold Refractor",50),("Gold Geometric",50),("Orange Refractor",25),("Orange Geometric",25),("Black Refractor",10),("Black Geometric",10),("Red Refractor",5),("Red Geometric",5),("Tie Dye Geometric",2),("Superfractor",1)]
is_id = get_is("Chrome Legends Autographs")
if is_id:
    for n, p in LEGENDS_AUTO_PARS: add(is_id, n, p)

# 1990 Topps Football Autographs (974)
SMALL_AUTO_PARS = [("Orange Refractor",25),("Orange Geometric",25),("Black Refractor",10),("Black Geometric",10),("Red Refractor",5),("Red Geometric",5),("Tie Dye Geometric",2),("Superfractor",1)]
is_id = get_is("1990 Topps Football Autographs")
if is_id:
    for n, p in SMALL_AUTO_PARS: add(is_id, n, p)

# Dual Autographs (981)
is_id = get_is("Dual Autographs")
if is_id:
    for n, p in SMALL_AUTO_PARS: add(is_id, n, p)

# Future Stars Autographs (975)
FSA_PARS = [("Gold Refractor",50)] + SMALL_AUTO_PARS
is_id = get_is("Future Stars Autographs")
if is_id:
    for n, p in FSA_PARS: add(is_id, n, p)

# Chromographs (976)
is_id = get_is("Chromographs")
if is_id:
    for n, p in SMALL_AUTO_PARS: add(is_id, n, p)

# Hall of Chrome Autographs (978)
HOC_PARS = [("Gold Refractor",50),("Gold Geometric",50)] + SMALL_AUTO_PARS
is_id = get_is("Hall of Chrome Autographs")
if is_id:
    for n, p in HOC_PARS: add(is_id, n, p)

# Tecmo Autographs — not in list, might be part of another set. Skip if not found.
# Actually there's no "Tecmo Autographs" in the IS list. The "Tecmo" insert is there but no auto version.
# Skip this one.

# Retail Rookie Autographs Variation (979)
RETAIL_RA_PARS = [("Refractor",499),("Magenta Refractor",399),("Teal Refractor",299),("Teal Lava Refractor",299),("Yellow Refractor",275),("Yellow Lava Refractor",275),("Pink Refractor",250),("Pink Lava Refractor",250),("Aqua Refractor",199),("Aqua Lava Refractor",199),("Blue Refractor",150),("Blue Lava Refractor",150),("Green Refractor",99),("Green Lava Refractor",99),("Purple Refractor",75),("Purple Lava Refractor",75),("Gold Refractor",50),("Gold Lava Refractor",50),("Gold Wave Refractor",50),("White Refractor",30),("Orange Refractor",25),("Orange Lava Refractor",25),("Orange Wave Refractor",25),("Black Refractor",10),("Black Lava Refractor",10),("Black Wave Refractor",10),("Red Refractor",5),("Red Lava Refractor",5),("Red Wave Refractor",5),("Superfractor",1)]
is_id = get_is("Rookie Autographs Variation")
if is_id:
    for n, p in RETAIL_RA_PARS: add(is_id, n, p)

# Topps Chrome Rookie Patch Autographs (985)
is_id = get_is("Topps Chrome Rookie Patch Autographs")
if is_id:
    for n, p in [("Gold Refractor",50),("Orange Refractor",25),("Red Refractor",5),("Superfractor",1)]: add(is_id, n, p)

# Topps Chrome Rookie Relics (982)
is_id = get_is("Topps Chrome Rookie Relics")
if is_id:
    for n, p in [("Green",99),("Gold",50),("Orange",25),("Red",5),("Superfractor",1)]: add(is_id, n, p)

# First Year Fabric (983)
is_id = get_is("First Year Fabric")
if is_id:
    for n, p in [("Green",99),("Gold",50),("Orange",25),("Red",5),("Superfractor",1)]: add(is_id, n, p)

# Shared insert parallels
SHARED_INSERT_PARS = [("Refractor",None),("X-Fractor",None),("Yellow Refractor",275),("Pink Refractor",250),("Aqua Refractor",199),("Blue Refractor",150),("Green Refractor",99),("Gold Refractor",50),("Orange Refractor",25),("Red Refractor",5),("Superfractor",1)]
for name in ["Future Stars","1975 Topps","Power Players","Legends of the Gridiron","Fortune 15","All Chrome Team"]:
    is_id = get_is(name)
    if is_id:
        for n, p in SHARED_INSERT_PARS: add(is_id, n, p)

# Single-superfractor inserts
for name, is_name in [("Chrome Radiating Rookies","Chrome Radiating Rookies"),("Urban Legends","Urban Legends"),("Helix","Helix"),("Game Genies","Game Genies"),("Kaiju","Kaiju"),("Let's Go","Let's Go"),("Ultra Violet","Ultra Violet"),("Lightning Leaders","Lightning Leaders"),("Fanatical","Fanatical")]:
    is_id = get_is(is_name)
    if is_id: add(is_id, "Superfractor", 1)

# Shadow Etch (965)
is_id = get_is("Shadow Etch")
if is_id:
    for n, p in [("Gold Refractor",50),("Orange Refractor",25),("Red Refractor",5),("Superfractor",1)]: add(is_id, n, p)

# Tecmo insert (not auto)
# No "Tecmo" in IS list... checking again
# Actually there IS no "Tecmo" in the list. Skip.

conn.commit()

# Recompute player stats
print(f"Added {count} parallels")
print("Recomputing player stats...")
cur.execute("SELECT id FROM players WHERE set_id = 44")
for (pid,) in cur.fetchall():
    cur.execute("SELECT pa.id, pa.insert_set_id FROM player_appearances pa WHERE pa.player_id = ?", (pid,))
    apps = cur.fetchall()
    is_ids = set(a[1] for a in apps)
    uc, tpr, o1 = 0, 0, 0
    for _, isid in apps:
        uc += 1
        cur.execute("SELECT name, print_run FROM parallels WHERE insert_set_id = ?", (isid,))
        for _, pr in cur.fetchall():
            uc += 1
            if pr is not None:
                tpr += pr
                if pr == 1: o1 += 1
    cur.execute("UPDATE players SET unique_cards=?, total_print_run=?, one_of_ones=?, insert_set_count=? WHERE id=?", (uc, tpr, o1, len(is_ids), pid))
conn.commit()
conn.close()
print("Done!")
