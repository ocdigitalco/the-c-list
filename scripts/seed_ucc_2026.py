"""
Seed: 2026 Topps UEFA Club Competitions
Set creation, insert sets, and parallels.
Usage: python3 scripts/seed_ucc_2026.py
"""
import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
db = sqlite3.connect(DB_PATH)
db.execute("PRAGMA journal_mode=WAL")
db.execute("PRAGMA foreign_keys=ON")

# ─── Create Set ──────────────────────────────────────────────────────────────────
db.execute("""
    INSERT INTO sets (name, sport, league, season, tier, slug, is_visible)
    VALUES ('2026 Topps UEFA Club Competitions', 'Soccer', 'UEFA', '2025-26', 'Standard',
            '2026-topps-uefa-club-competitions', 1)
""")
SET_ID = db.execute("SELECT last_insert_rowid()").fetchone()[0]
print(f"Created set ID: {SET_ID}")

def add_is(name):
    db.execute("INSERT INTO insert_sets (set_id, name) VALUES (?, ?)", (SET_ID, name))
    return db.execute("SELECT last_insert_rowid()").fetchone()[0]

def add_parallel(is_id, name, print_run=None):
    db.execute("INSERT INTO parallels (insert_set_id, name, print_run) VALUES (?, ?, ?)",
               (is_id, name, print_run))

# ─── Base Set + Parallels ────────────────────────────────────────────────────────
base_id = add_is("Base Set")
base_parallels = [
    ("Raindrops Parallels", None),
    ("Neon Yellow FlowFractor Parallel", None),
    ("Neon Pink FlowFractor Parallel", None),
    ("Neon Blue FlowFractor Parallel", None),
    ("Neon Purple FlowFractor Parallel", None),
    ("Neon Green FlowFractor Parallel", None),
    ("Aqua Foil Parallel", None),
    ("Purple Foil Parallel", 250),
    ("Purple Raindrops Parallel", 250),
    ("Blue Foil Parallel", 150),
    ("Blue Raindrops Parallel", 150),
    ("Green Foil Parallel", 99),
    ("Green Raindrops Parallel", 99),
    ("Black and White Foil Parallel", 75),
    ("Black and White Raindrops Parallel", 75),
    ("Gold Foil Parallel", 50),
    ("Gold Raindrops Parallel", 50),
    ("Orange Foil Parallel", 25),
    ("Orange Raindrops Parallel", 25),
    ("Black Foil Parallel", 10),
    ("Black Raindrops Parallel", 10),
    ("Red Foil Parallel", 5),
    ("Red Raindrops Parallel", 5),
    ("FoilFractor Parallel", 1),
    ("Printing Plates", 1),
    ("First Card", 1),
]
for name, pr in base_parallels:
    add_parallel(base_id, name, pr)
print(f"  Base Set: {len(base_parallels)} parallels")

# ─── Base Card Short Print Subsets ───────────────────────────────────────────────
sp_id = add_is("Base Card Short Prints")
ssp_id = add_is("Base Card Super Short Prints")
print("  Base Card Short Prints + Super Short Prints created")

# ─── Insert Cards (shared parallel ladder) ───────────────────────────────────────
insert_parallels = [
    ("Green Foil Parallel", 99),
    ("Gold Foil Parallel", 50),
    ("Orange Foil Parallel", 25),
    ("Black Foil Parallel", 10),
    ("Red Foil Parallel", 5),
    ("FoilFractor Parallel", 1),
]

insert_names = [
    "Roots",
    "Trophy Chasers",
    "Best of the Best: Legendary Numbers",
    "Born Champ",
    "8Bit Shots",
]

for ins_name in insert_names:
    is_id = add_is(ins_name)
    for par_name, pr in insert_parallels:
        add_parallel(is_id, par_name, pr)
    print(f"  {ins_name}: 6 parallels")

# ─── Chase Insert Cards ──────────────────────────────────────────────────────────
hpa_id = add_is("Home Pitch Advantage")
add_parallel(hpa_id, "Red Foil Parallel", 5)
add_parallel(hpa_id, "FoilFractor Parallel", 1)
print("  Home Pitch Advantage: 2 parallels")

for chase_name in ["Mindgame", "Murals", "JIGSAW", "HYPE", "The Grail"]:
    add_is(chase_name)
    print(f"  {chase_name}: no parallels")

sketch_id = add_is("Topps UCL Sketch Cards")
print("  Topps UCL Sketch Cards (1/1)")

messi_id = add_is("Gold Framed Messi Anniversary Sketch Cards")
print("  Gold Framed Messi Anniversary Sketch Cards (1/1)")

# ─── Autograph Cards ─────────────────────────────────────────────────────────────
auto_base_parallels = [
    ("Blue Foil Parallel", 150),
    ("Green Foil Parallel", 99),
    ("Black and White Foil Parallel", 75),
    ("Gold Foil Parallel", 50),
    ("Orange Foil Parallel", 25),
    ("Black Foil Parallel", 10),
    ("Red Foil Parallel", 5),
    ("FoilFractor Parallel", 1),
]

# Base Card Autograph Variations
bca_id = add_is("Base Card Autograph Variations")
for par_name, pr in auto_base_parallels:
    add_parallel(bca_id, par_name, pr)
print("  Base Card Autograph Variations: 8 parallels")

# Future Stars Autograph Variations
fsa_id = add_is("Future Stars Autograph Variations")
for par_name, pr in auto_base_parallels:
    add_parallel(fsa_id, par_name, pr)
print("  Future Stars Autograph Variations: 8 parallels")

# Teammates Dual Autographs
tda_id = add_is("Teammates Dual Autographs")
for par_name, pr in [("Orange Foil Parallel", 25), ("Black Foil Parallel", 10), ("Red Foil Parallel", 5), ("FoilFractor Parallel", 1)]:
    add_parallel(tda_id, par_name, pr)
print("  Teammates Dual Autographs: 4 parallels")

# Roots Autograph Variations
ra_id = add_is("Roots Autograph Variations")
add_parallel(ra_id, "FoilFractor Parallel", 1)
print("  Roots Autograph Variations: 1 parallel")

# Best of the Best: Legendary Numbers Autograph Variations
botb_a_id = add_is("Best of the Best: Legendary Numbers Autograph Variations")
add_parallel(botb_a_id, "FoilFractor Parallel", 1)
print("  Best of the Best: Legendary Numbers Autograph Variations: 1 parallel")

# Topps 1955 Autographs (Hobby Exclusive)
t55_id = add_is("Topps 1955 Autographs")
for par_name, pr in [("Green Refractor Parallel", 99), ("Gold Refractor Parallel", 50),
                      ("Orange Refractor Parallel", 25), ("Black Refractor Parallel", 10),
                      ("Red Refractor Parallel", 5), ("Superfractor Parallel", 1)]:
    add_parallel(t55_id, par_name, pr)
print("  Topps 1955 Autographs: 6 parallels (Hobby Exclusive)")

# Marks of Excellence (On-Card)
moe_id = add_is("Marks of Excellence")
for par_name, pr in [("Green Foil Parallel", 99), ("Gold Foil Parallel", 50),
                      ("Orange Foil Parallel", 25), ("Purple Foil Parallel", 10),
                      ("Red Foil Parallel", 5), ("Black Foil Parallel", 1)]:
    add_parallel(moe_id, par_name, pr)
print("  Marks of Excellence: 6 parallels")

# ─── Relic & Autograph Relic Cards ───────────────────────────────────────────────
# Topps Superstar Relics (Hobby Exclusive)
tsr_id = add_is("Topps Superstar Relics")
for par_name, pr in [("Purple Foil Parallel", 250), ("Blue Foil Parallel", 150),
                      ("Green Foil Parallel", 99), ("Gold Foil Parallel", 50),
                      ("Orange Foil Parallel", 25), ("Black Foil Parallel", 10),
                      ("Red Foil Parallel", 5), ("FoilFractor Parallel", 1)]:
    add_parallel(tsr_id, par_name, pr)
print("  Topps Superstar Relics: 8 parallels (Hobby Exclusive)")

# Premium Class Relics (Hobby Exclusive)
pcr_id = add_is("Premium Class Relics")
add_parallel(pcr_id, "Red Foil Parallel", 5)
add_parallel(pcr_id, "FoilFractor Parallel", 1)
print("  Premium Class Relics: 2 parallels (Hobby Exclusive)")

# Topps Superstar Autographed Relics (Hobby Exclusive)
tsar_id = add_is("Topps Superstar Autographed Relics")
for par_name, pr in [("Green Foil Parallel", 99), ("Gold Foil Parallel", 50),
                      ("Orange Foil Parallel", 25), ("Black Foil Parallel", 10),
                      ("Red Foil Parallel", 5), ("FoilFractor Parallel", 1)]:
    add_parallel(tsar_id, par_name, pr)
print("  Topps Superstar Autographed Relics: 6 parallels (Hobby Exclusive)")

# Premium Class Autograph Relics (Hobby Exclusive)
pcar_id = add_is("Premium Class Autograph Relics")
add_parallel(pcar_id, "Red Foil Parallel", 5)
add_parallel(pcar_id, "FoilFractor Parallel", 1)
print("  Premium Class Autograph Relics: 2 parallels (Hobby Exclusive)")

# Griezmann UCL Milestone On-card Auto Relic Cards (Hobby Exclusive)
# TODO(checklist): Sell sheet lists FoilFractor 1/1 three times — likely 3 separate milestone cards.
# Verify exact card count when official checklist is published.
griz_id = add_is("Griezmann UCL Milestone On-card Auto Relic Cards")
add_parallel(griz_id, "FoilFractor Parallel", 1)
print("  Griezmann UCL Milestone Auto Relic Cards: 1 parallel (Hobby Exclusive)")

# ─── Silver Packs ────────────────────────────────────────────────────────────────
# Ultimate Stage Chrome Cards
usc_id = add_is("Ultimate Stage Chrome Cards")
for par_name, pr in [("Aqua Refractor Parallel", 199), ("Blue Refractor Parallel", 150),
                      ("Green Refractor Parallel", 99), ("Purple Refractor Parallel", 75),
                      ("Gold Refractor Parallel", 50), ("Orange Refractor Parallel", 25),
                      ("Black Refractor Parallel", 10), ("Red Refractor Parallel", 5),
                      ("Superfractor Parallel", 1)]:
    add_parallel(usc_id, par_name, pr)
print("  Ultimate Stage Chrome Cards: 9 parallels")

# Ultimate Stage Chrome Cards Autograph Variations
usca_id = add_is("Ultimate Stage Chrome Autograph Variations")
add_parallel(usca_id, "Red Refractor Parallel", 5)
add_parallel(usca_id, "Superfractor Parallel", 1)
print("  Ultimate Stage Chrome Autograph Variations: 2 parallels")

# ─── Summary ─────────────────────────────────────────────────────────────────────
db.commit()
is_count = db.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id = ?", (SET_ID,)).fetchone()[0]
par_count = db.execute("SELECT COUNT(*) FROM parallels WHERE insert_set_id IN (SELECT id FROM insert_sets WHERE set_id = ?)", (SET_ID,)).fetchone()[0]
print(f"\nDone! Set ID: {SET_ID}")
print(f"  Insert sets: {is_count}")
print(f"  Parallels: {par_count}")
db.close()
