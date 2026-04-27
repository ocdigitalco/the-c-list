"""
Seed: 2026 Topps Chrome Black Baseball — Part 1
Set creation, insert sets, and all parallels.
Usage: python3 scripts/seed_chrome_black_2026.py
"""
import sqlite3, json, os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA foreign_keys=ON")
cur = conn.cursor()

SET_NAME = "2026 Topps Chrome Black Baseball"
cur.execute("SELECT id FROM sets WHERE name = ?", (SET_NAME,))
if cur.fetchone():
    print(f"Set '{SET_NAME}' already exists. Aborting.")
    conn.close()
    exit(1)

box_config = {
    "hobby": {
        "cards_per_pack": 6,
        "packs_per_box": 2,
        "boxes_per_case": 12,
        "autos_per_box": 1,
        "parallels_per_box": 2,
        "note": "2 standard packs plus 1 encased autograph per box",
    }
}

cur.execute(
    "INSERT INTO sets (name, sport, season, league, tier, sample_image_url, box_config, release_date, slug) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
    (SET_NAME, "Baseball", "2026", "MLB", "Chrome Black", "/sets/2026-topps-chrome-black.jpg", json.dumps(box_config), "2026-04-29", "2026-topps-chrome-black-baseball"),
)
set_id = cur.lastrowid
print(f"Created set '{SET_NAME}' with id {set_id}")

def create_is(name):
    cur.execute("INSERT INTO insert_sets (set_id, name) VALUES (?, ?)", (set_id, name))
    return cur.lastrowid

def add_pars(is_id, pars):
    for name, pr in pars:
        cur.execute("INSERT INTO parallels (insert_set_id, name, print_run) VALUES (?, ?, ?)", (is_id, name, pr))

# ─── Insert sets + parallels ─────────────────────────────────────

# Base
base_id = create_is("Base")
add_pars(base_id, [
    ("Refractor", 199), ("Blue Refractor", 150), ("Green Refractor", 99),
    ("Purple Refractor", 75), ("Purple Mini Diamond Refractor", 75), ("Purple Wave Refractor", 75),
    ("Gold Refractor", 50), ("Gold Mini Diamond Refractor", 50), ("Gold Wave Refractor", 50),
    ("Orange Refractor", 25), ("Orange Mini Diamond Refractor", 25), ("Orange Wave Refractor", 25),
    ("Rose Gold Refractor", 10), ("Rose Gold Mini Diamond Refractor", 10), ("Rose Gold Wave Refractor", 10),
    ("Red Refractor", 5), ("Red Mini Diamond Refractor", 5), ("Red Wave Refractor", 5),
    ("Superfractor", 1),
])

# Base - Rookie Design Variations
rdv_id = create_is("Base - Rookie Design Variations")
add_pars(rdv_id, [
    ("Purple Refractor", 75), ("Gold Refractor", 50), ("Orange Refractor", 25),
    ("Rose Gold Refractor", 10), ("Red Refractor", 5), ("Superfractor", 1),
])

# Chrome Black Autographs
cba_id = create_is("Chrome Black Autographs")
add_pars(cba_id, [
    ("Refractor", 199), ("Blue Refractor", 150), ("Green Refractor", 99),
    ("Purple Refractor", 75), ("Gold Refractor", 50), ("Gold Mini Diamond Refractor", 50),
    ("Orange Refractor", 25), ("Orange Mini Diamond Refractor", 25),
    ("Rose Gold Refractor", 10), ("Rose Gold Mini Diamond Refractor", 10),
    ("Red Refractor", 5), ("Red Mini Diamond Refractor", 5), ("Superfractor", 1),
])

# Ivory Autographs
ia_id = create_is("Ivory Autographs")
add_pars(ia_id, [("Orange Trim Refractor", 25), ("Red Trim Refractor", 5), ("Superfractor", 1)])

# Pitch Black Pairings Dual Autographs
pbp_id = create_is("Pitch Black Pairings Dual Autographs")
add_pars(pbp_id, [("Orange Refractor", 25), ("Rose Gold Refractor", 10), ("Red Refractor", 5), ("Superfractor", 1)])

# Super Futures Autographs
sfa_id = create_is("Super Futures Autographs")
add_pars(sfa_id, [("Gold Refractor", 50), ("Orange Refractor", 25), ("Rose Gold Refractor", 10), ("Red Refractor", 5), ("Superfractor", 1)])

# Paint It
pi_id = create_is("Paint It")
add_pars(pi_id, [("Red Refractor", 5), ("Superfractor", 1)])

# Damascus
dam_id = create_is("Damascus")
add_pars(dam_id, [("Superfractor", 1)])

# Nocturnal
noc_id = create_is("Nocturnal")
add_pars(noc_id, [("Superfractor", 1)])

# Depth Of Darkness
dod_id = create_is("Depth Of Darkness")
add_pars(dod_id, [("Red Refractor", 5), ("Superfractor", 1)])

# Home Field
hf_id = create_is("Home Field")
add_pars(hf_id, [("Superfractor", 1)])

conn.commit()

is_count = cur.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id = ?", (set_id,)).fetchone()[0]
par_count = cur.execute("SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON p.insert_set_id = i.id WHERE i.set_id = ?", (set_id,)).fetchone()[0]

print(f"\nDone! Set ID: {set_id}")
print(f"  Insert sets: {is_count}")
print(f"  Parallels: {par_count}")
conn.close()
