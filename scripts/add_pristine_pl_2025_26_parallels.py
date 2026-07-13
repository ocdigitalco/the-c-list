"""
2025-26 Topps Pristine Premier League (set 855):
  * set tri-pack box config (15 cards/pack, 3 packs/box, boxes/case unknown);
    the two unnumbered base parallels' per-box rates live in box_config
    (refractors_per_box / top_corner_per_box) — no per-parallel ratio field exists.
  * PER-SUBSET REPLACE of parallels with the confirmed numbered spec: for every
    subset in SPEC, delete existing parallels and insert the spec. Subsets not in
    SPEC (The Grail) are left untouched.

Maps to EXISTING subsets only; anything unmatched is reported, never created.
Names normalized to the DB-canonical "Superfractor" spelling.
Local SQLite only. Usage: python3 scripts/add_pristine_pl_2025_26_parallels.py
"""
import json
import os
import sqlite3

SET_ID = 855
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")

BOX_CONFIG = {
    "cards_per_pack": 15,
    "packs_per_box": 3,
    "boxes_per_case": None,      # unknown
    "refractors_per_box": 2,     # unnumbered base Refractor: 2 per tri-pack (box)
    "top_corner_per_box": 1,     # unnumbered base Top Corner: 1 per tri-pack (box)
}

# parallel ladders (name, print_run) — print_run None = unnumbered
BASE = [("Refractor", None), ("Top Corner", None),
        ("Blue Refractor", 75), ("Gold Refractor", 50), ("Orange Refractor", 25),
        ("Pink Refractor", 15), ("PL Trophy Malachite Refractor", 10),
        ("Red Refractor", 5), ("Superfractor", 1)]
INSERT_2 = [("Red Refractor", 5), ("Superfractor", 1)]
CASE_HIT = [("Superfractor", 1)]
PRISTINE_8 = [("Purple Pristine", 99), ("Blue Pristine", 75), ("Gold Pristine", 50),
              ("Orange Pristine", 25), ("Pink Pristine", 15),
              ("PL Trophy Malachite Pristine", 10), ("Red Pristine", 5), ("Black Pristine", 1)]
PRISTINE_3 = [("PL Trophy Malachite Pristine", 10), ("Red Pristine", 5), ("Black Pristine", 1)]
PRISTINE_AUTO_9 = [("Green Pristine", 150)] + PRISTINE_8
PRISTINE_LEGACY_7 = [("Blue Pristine", 75), ("Gold Pristine", 50), ("Orange Pristine", 25),
                     ("Pink Pristine", 15), ("PL Trophy Malachite Pristine", 10),
                     ("Red Pristine", 5), ("Black Pristine", 1)]
REFRACTOR_3 = [("PL Trophy Malachite Refractor", 10), ("Red Refractor", 5), ("Superfractor", 1)]
BIANCO = [("Pristine Bianco", 1)]

# keyed by ACTUAL DB subset name
SPEC = {
    "Base": BASE,
    "Precisionaries": INSERT_2, "Pure Strike": INSERT_2,
    "Generational": INSERT_2, "Perseverance": INSERT_2,
    "Amped": CASE_HIT, "Pearlescent": CASE_HIT, "Pristine Seasons": CASE_HIT,
    "Glacier": CASE_HIT, "Pristine Ivory": CASE_HIT,
    "Popular Demand Autograph Relics": PRISTINE_8,
    "Pristine Pieces Autograph Relics": PRISTINE_8,
    "Pristine From The Pitch": PRISTINE_3,
    "Rookie Jumbo Relic Autographs": PRISTINE_3,
    "Day 1 Pristine": PRISTINE_3,
    "Pristine Autographs": PRISTINE_AUTO_9,
    "Pristine Legacy Autographs": PRISTINE_LEGACY_7,
    "Pristine Pairs Dual Autographs": REFRACTOR_3,        # task: "Pristine Dual Autographs"
    "Pristine Seasons Autograph Edition": REFRACTOR_3,
    "Pristine Personal Endorsements Autographs": REFRACTOR_3,
    "Pristine Bianco": BIANCO,
}


def main():
    db = sqlite3.connect(os.path.abspath(DB_PATH))

    row = db.execute("SELECT box_config FROM sets WHERE id=?", (SET_ID,)).fetchone()
    if row is None:
        print("STOP: set 855 not found."); raise SystemExit(1)
    if row[0]:
        print(f"STOP: box_config already set: {row[0]}"); raise SystemExit(1)

    # box config
    db.execute("UPDATE sets SET box_config=? WHERE id=?", (json.dumps(BOX_CONFIG), SET_ID))

    total_deleted = total_inserted = 0
    skipped = []
    report = []
    for subset, pars in SPEC.items():
        r = db.execute(
            "SELECT id FROM insert_sets WHERE set_id=? AND name=?", (SET_ID, subset)
        ).fetchone()
        if not r:
            skipped.append(subset)
            continue
        is_id = r[0]
        d = db.execute("DELETE FROM parallels WHERE insert_set_id=?", (is_id,)).rowcount
        for name, pr in pars:
            db.execute(
                "INSERT INTO parallels (insert_set_id, name, print_run) VALUES (?,?,?)",
                (is_id, name, pr),
            )
        total_deleted += d
        total_inserted += len(pars)
        numbered = sum(1 for _, pr in pars if pr is not None)
        report.append((subset, d, len(pars), numbered))

    db.commit()

    print("Per-subset replace (subset: deleted -> inserted [numbered]):")
    for subset, d, ins, num in report:
        print(f"  {subset:42s} {d:3d} -> {ins:2d}  [{num} numbered]")
    print(f"\nTOTAL: deleted {total_deleted}, inserted {total_inserted}")
    print("SKIP-AND-REPORT (subset not found):", skipped if skipped else "none")
    # coverage confirmation
    n_numbered = db.execute(
        "SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id "
        "WHERE i.set_id=? AND p.print_run IS NOT NULL", (SET_ID,)).fetchone()[0]
    bc = db.execute("SELECT box_config IS NOT NULL FROM sets WHERE id=?", (SET_ID,)).fetchone()[0]
    print(f"\nCoverage: box_config set = {bool(bc)}; numbered parallels on set = {n_numbered}")
    # untouched subsets (not in SPEC)
    others = db.execute(
        "SELECT i.name, (SELECT COUNT(*) FROM parallels p WHERE p.insert_set_id=i.id) "
        "FROM insert_sets i WHERE i.set_id=? AND i.name NOT IN (%s) ORDER BY i.id"
        % ",".join("?" * len(SPEC)), (SET_ID, *SPEC.keys())).fetchall()
    print("Untouched subsets (not in spec):", [(n, c) for n, c in others])
    db.close()


if __name__ == "__main__":
    main()
