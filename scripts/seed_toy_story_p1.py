"""
Seed: 2025 Topps 30 Years of Toy Story — Part 1
Set config, insert sets, parallels, and pack odds.
Usage: python3 scripts/seed_toy_story_p1.py
"""
import sqlite3, json, os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
db = sqlite3.connect(DB_PATH)
db.execute("PRAGMA journal_mode=WAL")
db.execute("PRAGMA foreign_keys=ON")

SET_ID = 66

# Update set metadata
db.execute("""
    UPDATE sets SET
        release_date = '2026-05-06',
        sample_image_url = '/sets/2025-topps-30-years-of-toy-story.jpg',
        tier = 'Base',
        box_config = ?
    WHERE id = ?
""", (json.dumps({
    "hobby": {
        "cards_per_pack": 4,
        "packs_per_box": 8,
        "boxes_per_case": 12,
        "note": "3 base + 1 insert per pack. Per box: 4 numbered base/insert parallels, 1 auto or sketch, 1 base image variation, 8 inserts. Per case: 1 Pizza Planet Variation, 1 of: Topps 1995/Als Toy Barn/To Infinity/Toy Taaffeite."
    }
}), SET_ID))
print(f"Set ID: {SET_ID} — metadata updated")

# ─── Insert Sets ─────────────────────────────────────────────────────────────
insert_sets = [
    ('Base', 0),
    ('Image Variations', 0),
    ('Pizza Planet Variation', 0),
    ('Cone Variation', 0),
    ('Pixar Ball Variation', 0),
    ('30 Years And Beyond', 0),
    ("You've Got A Friend In Me", 0),
    ('Falling With Style', 0),
    ('So Play Nice', 0),
    ('Topps 1995', 0),
    ("Al's Toy Barn", 0),
    ('To Infinity…', 0),
    ('…And Beyond', 0),
    ('Toy Taaffeite', 0),
    ('Art Of Toy Story', 0),
    ('Sid Has Your Cards', 0),
    ("Andy's Cards Shadowbox", 0),
    ('The Claw Shadowbox', 0),
    ('You. Are. A. Toy... Story Autographs', 1),
    ("You've Got A Friend In Me Dual Autographs", 1),
    ('Golden Toys Shadowbox Autographs', 1),
    ('Toy Story Sketch Cards', 1),
    ('Studio Creations Sketch Cards', 1),
    ('Executive Studio Creations Sketch Cards', 1),
]

for name, is_auto in insert_sets:
    db.execute("INSERT INTO insert_sets (set_id, name) VALUES (?, ?)", (SET_ID, name))
print(f"  Created {len(insert_sets)} insert sets")

def get_is_id(name):
    row = db.execute("SELECT id FROM insert_sets WHERE set_id = ? AND name = ?", (SET_ID, name)).fetchone()
    if not row:
        raise ValueError(f"Insert set not found: {name}")
    return row[0]

def add_parallel(insert_set_id, name, print_run=None):
    db.execute("INSERT INTO parallels (insert_set_id, name, print_run) VALUES (?, ?, ?)",
               (insert_set_id, name, print_run))

# ─── Base Parallels ──────────────────────────────────────────────────────────
base_id = get_is_id('Base')
for name, pr in [
    ('Aqua Foil', 199), ('Blue Foil', 150), ('Green Foil', 99),
    ('Purple Foil', 75), ('Rose Gold Foil', 50), ('Orange Foil', 25),
    ('Black Foil', 10), ('Red Foil', 5), ('Gold Foil', 1),
]:
    add_parallel(base_id, name, pr)
print("  Base: 9 parallels")

# ─── Standard Insert Parallels (shared set) ──────────────────────────────────
standard_insert_parallels = [
    ("Woody's Cowboy Hat Brown Shimmer", 99),
    ('Gold Refractor', 50),
    ('Toy Story 30th Anniversary Refractor', 30),
    ('Orange Refractor', 25),
    ('Black Refractor', 10),
    ('Red Refractor', 5),
    ('Superfractor', 1),
]

for ins_name in ['30 Years And Beyond', "You've Got A Friend In Me", 'Falling With Style', 'So Play Nice']:
    ins_id = get_is_id(ins_name)
    for par_name, pr in standard_insert_parallels:
        add_parallel(ins_id, par_name, pr)
    print(f"  {ins_name}: 7 parallels")

# ─── Case Hit Inserts ────────────────────────────────────────────────────────
case_hit_parallels = [('Black Refractor', 10), ('Red Refractor', 5), ('Superfractor', 1)]
for ins_name in ["Topps 1995", "Al's Toy Barn", "To Infinity…", "…And Beyond", "Toy Taaffeite"]:
    ins_id = get_is_id(ins_name)
    for par_name, pr in case_hit_parallels:
        add_parallel(ins_id, par_name, pr)
    print(f"  {ins_name}: 3 parallels")

# ─── Art Of Toy Story ────────────────────────────────────────────────────────
art_id = get_is_id('Art Of Toy Story')
for par_name, pr in case_hit_parallels:
    add_parallel(art_id, par_name, pr)
print("  Art Of Toy Story: 3 parallels")

# ─── Shadowbox Sets ──────────────────────────────────────────────────────────
for ins_name in ["Andy's Cards Shadowbox", "The Claw Shadowbox"]:
    ins_id = get_is_id(ins_name)
    for par_name, pr in case_hit_parallels:
        add_parallel(ins_id, par_name, pr)
    print(f"  {ins_name}: 3 parallels")

# ─── Autograph Parallels ─────────────────────────────────────────────────────
yrt_id = get_is_id('You. Are. A. Toy... Story Autographs')
for par_name, pr in [
    ('Blue Sky Refractor', 150),
    ("Woody's Cowboy Hat Brown Shimmer Refractor", 99),
    ('Buzz Lightyear Shimmer Refractor', 75),
    ('Gold Refractor', 50),
    ('Toy Story 30th Anniversary Refractor', 30),
    ('Orange Refractor', 25),
    ('Black Refractor', 10),
    ('Red Refractor', 5),
    ('Superfractor', 1),
]:
    add_parallel(yrt_id, par_name, pr)
print("  You. Are. A. Toy... Story Autographs: 9 parallels")

ygfda_id = get_is_id("You've Got A Friend In Me Dual Autographs")
for par_name, pr in [
    ('Toy Story 30th Anniversary Refractor', 30),
    ('Orange Refractor', 25),
    ('Black Refractor', 10),
    ('Red Refractor', 5),
    ('Superfractor', 1),
]:
    add_parallel(ygfda_id, par_name, pr)
print("  You've Got A Friend In Me Dual Autographs: 5 parallels")

gt_id = get_is_id('Golden Toys Shadowbox Autographs')
for par_name, pr in case_hit_parallels:
    add_parallel(gt_id, par_name, pr)
print("  Golden Toys Shadowbox Autographs: 3 parallels")

# ─── Pack Odds ───────────────────────────────────────────────────────────────
pack_odds = {
    "hobby": {
        "Base Cards": "1:1",
        "Base Cards Aqua Foil Parallel": "1:8",
        "Base Cards Blue Foil Parallel": "1:11",
        "Base Cards Green Foil Parallel": "1:16",
        "Base Cards Purple Foil Parallel": "1:21",
        "Base Cards Rose Gold Foil Parallel": "1:31",
        "Base Cards Orange Foil Parallel": "1:61",
        "Base Cards Black Foil Parallel": "1:152",
        "Base Cards Red Foil Parallel": "1:304",
        "Base Cards Gold Foil Parallel": "1:1,522",
        "Image Variations": "1:8",
        "Pizza Planet Variation": "1:96",
        "Cone Variation": "1:5,845",
        "Pixar Ball Variation": "1:4,714",
        "30 Years And Beyond": "1:2",
        "30 Years And Beyond Woody's Cowboy Hat Shimmer Refractor": "1:44",
        "30 Years And Beyond Gold Refractor": "1:87",
        "30 Years And Beyond Toy Story 30th Anniversary Refractor": "1:145",
        "30 Years And Beyond Orange Refractor": "1:174",
        "30 Years And Beyond Black Refractor": "1:434",
        "30 Years And Beyond Red Refractor": "1:870",
        "30 Years And Beyond Superfractor": "1:4,566",
        "You've Got A Friend In Me": "1:5",
        "You've Got A Friend In Me Woody's Cowboy Hat Shimmer": "1:103",
        "You've Got A Friend In Me Gold Refractor": "1:202",
        "You've Got A Friend In Me Toy Story 30th Anniversary Refractor": "1:338",
        "You've Got A Friend In Me Orange Refractor": "1:405",
        "You've Got A Friend In Me Black Refractor": "1:1,015",
        "You've Got A Friend In Me Red Refractor": "1:2,058",
        "You've Got A Friend In Me Superfractor": "1:12,176",
        "Falling With Style": "1:7",
        "Falling With Style Woody's Cowboy Hat Shimmer": "1:153",
        "Falling With Style Gold Refractor": "1:304",
        "Falling With Style Toy Story 30th Anniversary Refractor": "1:506",
        "Falling With Style Orange Refractor": "1:609",
        "Falling With Style Black Refractor": "1:1,522",
        "Falling With Style Red Refractor": "1:3,109",
        "Falling With Style Superfractor": "1:20,874",
        "So Play Nice": "1:7",
        "So Play Nice Woody's Cowboy Hat Shimmer": "1:153",
        "So Play Nice Gold Refractor": "1:304",
        "So Play Nice Toy Story 30th Anniversary Refractor": "1:506",
        "So Play Nice Orange Refractor": "1:609",
        "So Play Nice Black Refractor": "1:1,522",
        "So Play Nice Red Refractor": "1:3,109",
        "So Play Nice Superfractor": "1:20,874",
        "Topps 1995": "1:281",
        "Topps 1995 Black Refractor": "1:590",
        "Topps 1995 Red Refractor": "1:1,179",
        "Topps 1995 Superfractor": "1:5,845",
        "Al's Toy Barn": "1:1,462",
        "Al's Toy Barn Black Refractor": "1:3,044",
        "Al's Toy Barn Red Refractor": "1:6,088",
        "Al's Toy Barn Superfractor": "1:29,223",
        "To Infinity…": "1:3,653",
        "To Infinity… Black Refractor": "1:7,691",
        "To Infinity… Red Refractor": "1:14,612",
        "To Infinity… Superfractor": "1:73,056",
        "…And Beyond": "1:3,653",
        "…And Beyond Black Refractor": "1:7,691",
        "…And Beyond Red Refractor": "1:14,612",
        "…And Beyond Superfractor": "1:73,056",
        "Toy Taaffeite": "1:975",
        "Toy Taaffeite Black Refractor": "1:1,539",
        "Toy Taaffeite Red Refractor": "1:3,044",
        "Toy Taaffeite Superfractor": "1:14,612",
        "Art Of Toy Story": "1:192",
        "Art Of Toy Story Black Refractor": "1:765",
        "Art Of Toy Story Red Refractor": "1:1,539",
        "Art Of Toy Story Superfractor": "1:7,691",
        "Sid Has Your Cards": "1:2,923",
        "Andy's Cards Shadowbox": "1:765",
        "Andy's Cards Shadowbox Black Refractor": "1:1,539",
        "Andy's Cards Shadowbox Red Refractor": "1:3,044",
        "Andy's Cards Shadowbox Superfractor": "1:14,612",
        "The Claw Shadowbox": "1:765",
        "The Claw Shadowbox Black Refractor": "1:1,539",
        "The Claw Shadowbox Red Refractor": "1:3,044",
        "The Claw Shadowbox Superfractor": "1:14,612",
        "You. Are. A. Toy... Story Autograph Card": "1:33",
        "You. Are. A. Toy... Story Autograph Card Blue Sky Refractor": "1:45",
        "You. Are. A. Toy... Story Autograph Card Woody's Cowboy Hat Shimmer": "1:69",
        "You. Are. A. Toy... Story Autograph Card Buzz Lightyear Shimmer": "1:86",
        "You. Are. A. Toy... Story Autograph Card Gold Refractor": "1:129",
        "You. Are. A. Toy... Story Autograph Card Toy Story 30th Anniversary Refractor": "1:179",
        "You. Are. A. Toy... Story Autograph Card Orange Refractor": "1:212",
        "You. Are. A. Toy... Story Autograph Card Black Refractor": "1:530",
        "You. Are. A. Toy... Story Autograph Card Red Refractor": "1:1,024",
        "You. Are. A. Toy... Story Autograph Card Superfractor": "1:5,116",
        "You've Got A Friend In Me Dual Autograph": "1:371",
        "You've Got A Friend In Me Dual Autograph Toy Story 30th Anniversary Refractor": "1:707",
        "You've Got A Friend In Me Dual Autograph Orange Refractor": "1:848",
        "You've Got A Friend In Me Dual Autograph Black Refractor": "1:1,142",
        "You've Got A Friend In Me Dual Autograph Red Refractor": "1:2,283",
        "You've Got A Friend In Me Dual Autograph Superfractor": "1:11,411",
        "Golden Toys Shadowbox Autograph": "1:1,239",
        "Golden Toys Shadowbox Autograph Black Refractor": "1:1,491",
        "Golden Toys Shadowbox Autograph Red Refractor": "1:2,982",
        "Golden Toys Shadowbox Autograph Superfractor": "1:14,612",
        "Toy Story Sketch Card": "1:114",
        "Toy Story Sketch Card Black Foil": "1:122",
        "Toy Story Sketch Card Gold Foil": "1:238",
        "Toy Story Sketch Card Silver Foil": "1:900",
        "Studio Creations Sketch Card Black And Gold Foil": "1:1,010",
    }
}

db.execute("UPDATE sets SET pack_odds = ? WHERE id = ?", (json.dumps(pack_odds), SET_ID))

db.commit()

# Verify
is_count = db.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id = ?", (SET_ID,)).fetchone()[0]
par_count = db.execute("SELECT COUNT(*) FROM parallels WHERE insert_set_id IN (SELECT id FROM insert_sets WHERE set_id = ?)", (SET_ID,)).fetchone()[0]
has_odds = db.execute("SELECT pack_odds IS NOT NULL FROM sets WHERE id = ?", (SET_ID,)).fetchone()[0]
print(f"\nDone! Set ID: {SET_ID}")
print(f"  Insert sets: {is_count}")
print(f"  Parallels: {par_count}")
print(f"  Pack odds: {'yes' if has_odds else 'no'}")

db.close()
