#!/usr/bin/env python3
"""Attach numbered parallels to 14 existing subsets of 2026 Topps Cosmic Chrome WWE.
Print runs only; no pack odds, no card/role/subset-name changes. Keyed by subset id.
"""
import sqlite3

db = sqlite3.connect("the-c-list.db")

# color name -> print_run (None = unnumbered)
PR = {
    "Refractor": None,
    "Nucleus Refractor": None,
    "Magenta Cosmos Refractor": 299,
    "Purple Nebula Refractor": 150,
    "Blue Moon Refractor": 99,
    "Green Space Dust Refractor": 75,
    "Gold Interstellar Refractor": 50,
    "Orange Galactic Refractor": 25,
    "Black Eclipse Refractor": 10,
    "Red Flare Refractor": 5,
    "Superfractor": 1,
}

BASE = ["Refractor", "Nucleus Refractor", "Magenta Cosmos Refractor", "Purple Nebula Refractor",
        "Blue Moon Refractor", "Green Space Dust Refractor", "Gold Interstellar Refractor",
        "Orange Galactic Refractor", "Black Eclipse Refractor", "Red Flare Refractor", "Superfractor"]
SIX = ["Blue Moon Refractor", "Gold Interstellar Refractor", "Orange Galactic Refractor",
       "Black Eclipse Refractor", "Red Flare Refractor", "Superfractor"]
FOUR = ["Orange Galactic Refractor", "Black Eclipse Refractor", "Red Flare Refractor", "Superfractor"]
ONE = ["Superfractor"]

# subset_id -> rung list  (mapping confirmed by id, names verbatim from DB)
PLAN = {
    1723: BASE,   # Base Set
    1734: FOUR,   # Cosmic Chrome Autograph Variation  (target: Cosmic Chrome Autographs)
    1735: FOUR,   # Milky Way Marks
    1736: FOUR,   # Equinox Autographs
    1737: FOUR,   # Solar Flares Signatures  (target: Solar Flare Autographs)
    1733: FOUR,   # Starfractor
    1724: SIX,    # Galaxy Greats
    1725: SIX,    # Extraterrestrial Talent  (target: Extraterrestrial Talents)
    1726: SIX,    # Galactic Showdown
    1727: SIX,    # Star Clusters
    1729: ONE,    # Light Years
    1730: ONE,    # Cosmic Dust
    1731: ONE,    # Hyper Nova
    1732: ONE,    # Geocentric
}

SET_ID = db.execute("SELECT id FROM sets WHERE slug = '2026-topps-cosmic-chrome-wwe'").fetchone()[0]

# Safety: every planned id must belong to this set and currently have zero parallels.
for sid in PLAN:
    row = db.execute("SELECT set_id FROM insert_sets WHERE id = ?", (sid,)).fetchone()
    assert row and row[0] == SET_ID, f"subset {sid} not in set {SET_ID}"
    n = db.execute("SELECT COUNT(*) FROM parallels WHERE insert_set_id = ?", (sid,)).fetchone()[0]
    assert n == 0, f"subset {sid} already has {n} parallels — aborting to avoid dupes"

inserted = 0
for sid, rungs in PLAN.items():
    for pname in rungs:
        db.execute(
            "INSERT INTO parallels (insert_set_id, name, print_run, exclusivity) VALUES (?, ?, ?, NULL)",
            (sid, pname, PR[pname]))
        inserted += 1
db.commit()
print(f"Inserted {inserted} parallel rows (expected 59) across {len(PLAN)} subsets.")
