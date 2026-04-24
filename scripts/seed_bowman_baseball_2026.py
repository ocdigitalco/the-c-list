"""
Seed: 2026 Bowman Baseball — Part 1
Set metadata, insert sets, and all parallels.
Usage: python3 scripts/seed_bowman_baseball_2026.py
"""
import sqlite3, json, os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA foreign_keys=ON")
cur = conn.cursor()

SET_ID = 52

# ─── Update set metadata ─────────────────────────────────────────
box_config = {
    "hobby": {"cards_per_pack": 8, "packs_per_box": 20, "boxes_per_case": 12, "autos_per_box": 1},
    "jumbo": {"cards_per_pack": 28, "packs_per_box": 12, "boxes_per_case": 8, "autos_per_box": 3},
    "mega": {"cards_per_pack": 7, "packs_per_box": 6, "boxes_per_case": 20},
    "value": {"cards_per_pack": 10, "packs_per_box": 6},
    "breakers_delight": {"cards_per_pack": 10, "packs_per_box": 1, "boxes_per_case": 6},
}
cur.execute("UPDATE sets SET release_date = ?, sample_image_url = ?, box_config = ? WHERE id = ?",
            ("2026-05-13", "/sets/2026-bowman-baseball.jpg", json.dumps(box_config), SET_ID))
print(f"Updated set metadata for ID {SET_ID}")

# ─── Helper ──────────────────────────────────────────────────────
def create_is(name):
    cur.execute("INSERT INTO insert_sets (set_id, name) VALUES (?, ?)", (SET_ID, name))
    return cur.lastrowid

def add_pars(is_id, pars):
    for name, pr in pars:
        cur.execute("INSERT INTO parallels (insert_set_id, name, print_run) VALUES (?, ?, ?)", (is_id, name, pr))

# ─── Insert sets + parallels ─────────────────────────────────────

# Base / Base Prospects share same parallels
BASE_PARS = [
    ("Sky Blue", None), ("Neon Green", None), ("Fuchsia", None),
    ("Purple", None), ("Purple Pattern", None), ("Pink", None),
    ("Blue", None), ("Blue Pattern", None),
    ("Green", None), ("Green Pattern", None),
    ("Yellow", None), ("Yellow Pattern", None),
    ("Gold", None), ("Gold Pattern", None),
    ("Orange", None), ("Orange Pattern", None),
    ("Black", None), ("Black Pattern", None),
    ("Red", None), ("Platinum Border Rainbow Foil", None),
    ("Printing Plates", 1), ("Bowman Logo Pattern", None),
]

base_id = create_is("Base")
add_pars(base_id, BASE_PARS)

create_is("Base - Etched In Glass Variations")  # no parallels
create_is("Base - Red RC Variations")  # no parallels

bp_id = create_is("Base Prospects")
add_pars(bp_id, BASE_PARS)

# Chrome Prospects
CHROME_PARS = [
    ("League Logofractor", None), ("Mini Diamond", None), ("Lazer Refractor", None),
    ("X-Fractor", None), ("Gum Ball Refractor", None), ("Sunflower Seeds Refractor", None),
    ("Peanuts Refractor", None), ("Pop Corn Refractor", None),
    ("Reptilian Refractor", None), ("Refractor", None), ("Lava", None), ("Wave", None),
    ("Speckle", None), ("Purple Refractor", None), ("Purple Raywave", None), ("Purple Geometric", None),
    ("Fuchsia Wave Refractor", None), ("Fuchsia Refractor", None), ("Reptilian Fuchsia Refractor", None),
    ("Blue Geometric", None), ("Blue Refractor", None), ("Blue Shimmer", None),
    ("Blue Raywave", None), ("Reptilian Blue Refractor", None),
    ("Aqua X-Fractor", None), ("Aqua Shimmer", None), ("Aqua Geometric", None),
    ("Steel Metal", None),
    ("Green Refractor", None), ("Green Grass", None), ("Green Shimmer", None),
    ("Reptilian Green Refractor", None), ("Green Geometric", None),
    ("Packfractor Variation", None),
    ("Yellow Refractor", None), ("Yellow X-Fractor", None), ("Yellow Wave", None),
    ("Gold Refractor", None), ("Gold Shimmer", None), ("Reptilian Gold Refractor", None), ("Gold Geometric", None),
    ("Bowman Logofractor", None),
    ("Orange", None), ("Orange Shimmer", None), ("Reptilian Orange Refractor", None), ("Orange Geometric", None),
    ("Black Refractor", None), ("Black X-Fractor Refractor", None), ("Black Geometric", None),
    ("Rose Gold", None), ("Rose Gold X-Fractor", None),
    ("Red Geometric", None), ("Red Refractor", None), ("Red Lava", None), ("Reptilian Red Refractor", None),
    ("Firefractor", None), ("Superfractor", 1), ("Printing Plates", 1),
]
cp_id = create_is("Chrome Prospects")
add_pars(cp_id, CHROME_PARS)

create_is("Chrome Prospects - Packfractor Variation")  # no parallels
create_is("Chrome Prospects - Etched In Glass Variations")  # no parallels

# Standard insert parallels (shared by several sets)
STANDARD_INSERT_PARS = [
    ("Mini-Diamond Refractor", None), ("Aqua Refractor", None),
    ("Green Refractor", None), ("Gold Refractor", None),
    ("Orange Refractor", None), ("Red Refractor", None), ("Superfractor", 1),
]

for name in ["Bowman Scouts Top 100", "Bowman Sterling", "Electric Sluggers", "Under The Radar", "Power Chords"]:
    is_id = create_is(name)
    add_pars(is_id, STANDARD_INSERT_PARS)

pw_id = create_is("Patchwork")
add_pars(pw_id, [("Red Refractor", None), ("Superfractor", 1)])

ANIME_PARS = [("Black Refractor", None), ("Red Refractor", None), ("Superfractor", 1)]
anime_id = create_is("Anime")
add_pars(anime_id, ANIME_PARS)

create_is("Anime - Kanji Variations")  # no parallels

fd_id = create_is("Final Draft")
add_pars(fd_id, ANIME_PARS)

cryst_id = create_is("Crystallized")
add_pars(cryst_id, [("Gold Refractor", None), ("Orange Refractor", None), ("Red Refractor", None), ("Superfractor", 1)])

spot_id = create_is("Bowman Spotlights")
add_pars(spot_id, [("Red Refractor", None), ("Superfractor", 1)])

# Chrome Prospect Autographs
CPA_PARS = [
    ("Refractor", None), ("Speckle Refractor", None), ("Purple Refractor", None),
    ("Blue Refractor", None), ("Blue X-Fractor Refractor", None), ("Aqua Refractor", None),
    ("Mini-Diamond Refractor", None),
    ("Green Refractor", None), ("Green Grass Refractor", None),
    ("Reptilian Green Refractor", None), ("Green Shimmer Refractor", None),
    ("Packfractor Variation", None),
    ("Yellow Refractor", None), ("Yellow X-Fractor", None),
    ("Gold Refractor", None), ("Gold Shimmer Refractor", None),
    ("Bowman Logofractor", None),
    ("Orange Refractor", None), ("Orange X-Fractor", None), ("Orange Shimmer Refractor", None),
    ("Black Refractor", None), ("Black X-Fractor", None),
    ("Gum Ball Refractor", None), ("Sunflower Seeds Refractor", None),
    ("Peanuts Refractor", None), ("Pop Corn Refractor", None),
    ("Red Refractor", None), ("Red Lava Refractor", None),
    ("Firefractor", None), ("Superfractor", 1), ("Printing Plates", 1),
    ("HTA Choice Refractor", None), ("Green Lava Refractor", None),
    ("Gold Lava Refractor", None), ("Orange Wave Refractor", None),
    ("Red X-Fractor", None), ("Gold Ink Variation", None),
    ("Black And White Shimmer Refractor", None),
]
cpa_id = create_is("Chrome Prospect Autographs")
add_pars(cpa_id, CPA_PARS)

create_is("Chrome Prospect Gold Ink Autographs")  # no parallels
create_is("Chrome Prospect Packfractor Autographs")  # no parallels

# Chrome Rookie Autographs
CRA_PARS = [
    ("Refractor", None), ("Blue Refractor", None), ("Mini-Diamond Refractor", None),
    ("Green Refractor", None), ("Yellow Refractor", None), ("Gold Refractor", None),
    ("Orange Refractor", None), ("Red Refractor", None), ("Superfractor", 1), ("Printing Plates", 1),
]
cra_id = create_is("Chrome Rookie Autographs")
add_pars(cra_id, CRA_PARS)

dpp_id = create_is("Draft Pick Pairings")
add_pars(dpp_id, [("Red Refractor", None), ("Superfractor", 1)])

# Sterling/Electric/UTR/Power Chords Autographs (same structure)
AUTO_INSERT_PARS = [("Gold Refractor", None), ("Orange Refractor", None), ("Red Refractor", None), ("Superfractor", 1)]
for name in ["Bowman Sterling Autographs", "Electric Sluggers Autographs", "Under The Radar Autographs", "Power Chords Autographs"]:
    is_id = create_is(name)
    add_pars(is_id, AUTO_INSERT_PARS)

# Base Retail Autographs
RETAIL_AUTO_PARS = [("Purple", None), ("Blue", None), ("Green", None), ("Gold", None), ("Orange", None), ("Red", None), ("Platinum", None)]
for name in ["Base Prospect Retail Autographs", "Base Rookie And Veteran Retail Autographs"]:
    is_id = create_is(name)
    add_pars(is_id, RETAIL_AUTO_PARS)

create_is("Ultimate Autograph Booklet")  # no parallels

aag_id = create_is("All-America Game Autographs")
add_pars(aag_id, [("Red Ink", None)])

conn.commit()

# Stats
is_count = cur.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id = ?", (SET_ID,)).fetchone()[0]
par_count = cur.execute("SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON p.insert_set_id = i.id WHERE i.set_id = ?", (SET_ID,)).fetchone()[0]

print(f"\nDone! Set ID: {SET_ID}")
print(f"  Insert sets: {is_count}")
print(f"  Parallels: {par_count}")
conn.close()
