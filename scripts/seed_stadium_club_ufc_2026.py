"""
Seed 2026 Topps Stadium Club UFC (set) into local SQLite + attach parallels.
Local SQLite only; Tyler migrates to Turso separately.

888 cards / 19 subsets. Teams NULL (UFC). Co-player subset: Dual Autographs
(one appearance + appearance_co_players link). No pack odds this release —
all parallels get odds NULL; print_run per serial; exclusivity from labels.

Base-tier row named "{subset} Base" per task (differs from the bare "Base"
used on set 863 — flagged in report). Parallel names stored as-printed/full.

Usage: python3 scripts/seed_stadium_club_ufc_2026.py
"""
import json, os, sqlite3

DB = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
DATA = os.path.join(os.path.dirname(__file__), "stadium_club_ufc_2026.jsonl")

SET = dict(
    name="2026 Topps Stadium Club UFC", sport="MMA", season="2026", league="UFC",
    tier="Standard", sample_image_url="/sets/2026-topps-stadium-club-ufc.jpg",
    release_date="2026-08-14", slug="2026-topps-stadium-club-ufc", is_visible=1,
    created_at="2026-08-01T12:00:00Z", topps_url="https://www.topps.com/pages/topps-stadium-club-ufc",
)

BOX_CONFIG = {
    "hobby": {"cards_per_pack": 8, "packs_per_box": 16, "boxes_per_case": 12, "autos_per_box": 2, "notes": "2 autographs per box"},
    "mega":  {"cards_per_pack": 10, "packs_per_box": 6, "boxes_per_case": 20, "notes": "Light Blue parallels (Mega-exclusive)"},
    "value": {"cards_per_pack": 5, "packs_per_box": 6, "boxes_per_case": 40, "notes": "Lime Green parallels (Value-exclusive)"},
}

AUTO_SUBSETS = {
    "Base Cards Autograph Variation", "Base Cards Chrome Autograph Variation",
    "Fight Motion Autographs", "The Aftermath Autographs", "Dual Autographs",
    "Main Stage Autographs", "Abstract Autographs", "Concentration Autographs",
}

GATE = {
    "Base Cards I": 100, "Base Cards II": 100, "Chrome Base Cards I": 100, "Chrome Base Cards II": 100,
    "Beam Team": 20, "Fight Motion": 25, "Concentration": 25, "The Aftermath": 25, "Main Stage": 25,
    "Triumvirates": 60, "Triumvirates Nickname": 39, "Base Cards Autograph Variation": 90,
    "Base Cards Chrome Autograph Variation": 85, "Fight Motion Autographs": 19, "The Aftermath Autographs": 20,
    "Dual Autographs": 8, "Main Stage Autographs": 19, "Abstract Autographs": 15, "Concentration Autographs": 13,
}

# ---- parallel ladders: (name, print_run|None, exclusivity|None) --------------
BASE_LADDER = [
    ("Black and White", None, "Hobby"), ("Bronze", None, "Hobby"), ("Gold", None, "Hobby"),
    ("Lime Green", None, "Retail"), ("Light Blue", None, "Mega"), ("Members Only", None, None),
    ("Photographer's Proof", None, None), ("Red", None, "Hobby"), ("Sepia", None, "Retail"),
    ("Green", 299, None), ("Turquoise", 99, None), ("Purple", 75, None), ("Blue", 50, None),
    ("Rainbow Foilboard", 25, None), ("Gold Rainbow Foilboard", 1, None), ("Printing Plate", 1, "Hobby"),
]
CHROME_LADDER = [
    ("Orange Refractor", None, None), ("Red White and Blue Refractor", None, "Hobby"),
    ("Refractor", None, None), ("Tie-Dye Refractor", None, "Retail"), ("Gold Minted", None, None),
    ("Turquoise Refractor", 99, None), ("Purple Refractor", 75, None), ("Blue Refractor", 50, None),
    ("Pearl White Refractor", 30, None), ("Superfractor", 1, None),
]
BASE_AUTO_LADDER = [
    ("Yellow", None, None), ("Turquoise", 99, None), ("Gold", 50, None),
    ("Rainbow Foilboard", 25, None), ("Green", 5, None), ("Gold Rainbow Foilboard", 1, None),
]
BASE_CHROME_AUTO_LADDER = [
    ("Turquoise Refractor", 99, None), ("Red Refractor", 50, None),
    ("Orange Refractor", 25, None), ("Superfractor", 1, None),
]
SHARED_AUTO_LADDER = [
    ("Turquoise", 99, None), ("Purple", 25, None), ("Green", 5, None), ("Gold Rainbow Foilboard", 1, None),
]
INSERT_A = [  # Fight Motion / Concentration / The Aftermath / Main Stage
    ("Red", None, "Mega"), ("Turquoise", 99, None), ("Blue", 50, None), ("Gold Rainbow Foilboard", 1, None),
]
INSERT_B = [  # Triumvirates / Triumvirates Nickname
    ("Red", None, "Hobby"), ("Black", 99, None), ("Green", 50, None), ("Superfractor", 1, None),
]

# subset -> ladder (parallel-bearing subsets only; each also gets a "{subset} Base" row)
LADDERS = {
    "Base Cards I": BASE_LADDER, "Base Cards II": BASE_LADDER,
    "Chrome Base Cards I": CHROME_LADDER, "Chrome Base Cards II": CHROME_LADDER,
    "Base Cards Autograph Variation": BASE_AUTO_LADDER,
    "Base Cards Chrome Autograph Variation": BASE_CHROME_AUTO_LADDER,
    "Fight Motion Autographs": SHARED_AUTO_LADDER, "The Aftermath Autographs": SHARED_AUTO_LADDER,
    "Main Stage Autographs": SHARED_AUTO_LADDER, "Abstract Autographs": SHARED_AUTO_LADDER,
    "Concentration Autographs": SHARED_AUTO_LADDER,
    "Fight Motion": INSERT_A, "Concentration": INSERT_A, "The Aftermath": INSERT_A, "Main Stage": INSERT_A,
    "Triumvirates": INSERT_B, "Triumvirates Nickname": INSERT_B,
}
NO_PARALLELS = {"Beam Team", "Dual Autographs"}


def main():
    cards = [json.loads(l) for l in open(DATA) if l.strip()]
    if len(cards) != 888:
        print(f"STOP: parsed {len(cards)} cards, expected 888."); raise SystemExit(1)

    db = sqlite3.connect(os.path.abspath(DB))
    if db.execute("SELECT id FROM sets WHERE slug=? OR name=?", (SET["slug"], SET["name"])).fetchone():
        print("STOP: set already exists."); raise SystemExit(1)

    cur = db.execute(
        """INSERT INTO sets (name, sport, season, league, tier, sample_image_url, release_date,
                             slug, is_visible, created_at, topps_url, box_config, pack_odds)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,NULL)""",
        (SET["name"], SET["sport"], SET["season"], SET["league"], SET["tier"], SET["sample_image_url"],
         SET["release_date"], SET["slug"], SET["is_visible"], SET["created_at"], SET["topps_url"],
         json.dumps(BOX_CONFIG)))
    set_id = cur.lastrowid
    print(f"Created set id {set_id}")

    # subsets in first-appearance order
    order, seen = [], set()
    for c in cards:
        if c["subset"] not in seen:
            seen.add(c["subset"]); order.append(c["subset"])
    is_id = {}
    for name in order:
        auto = 1 if name in AUTO_SUBSETS else 0
        is_id[name] = db.execute("INSERT INTO insert_sets (set_id, name, is_autograph) VALUES (?,?,?)",
                                 (set_id, name, auto)).lastrowid
    print(f"Created {len(is_id)} subsets ({sum(1 for n in is_id if n in AUTO_SUBSETS)} autograph)")

    # players (distinct by name, primary + co)
    names = {}
    def pid(nm):
        if nm not in names:
            names[nm] = db.execute("INSERT INTO players (set_id, name, subject_role) VALUES (?,?,'athlete')",
                                   (set_id, nm)).lastrowid
        return names[nm]
    for c in cards:
        pid(c["name"])
        for co in c.get("co_players", []):
            pid(co["name"])
    print(f"Created {len(names)} players")

    # appearances + co-links
    co_links = 0
    for c in cards:
        pa = db.execute(
            """INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, subset_tag, team)
               VALUES (?,?,?,?,NULL,NULL)""",
            (names[c["name"]], is_id[c["subset"]], c["card_number"], 1 if c.get("rookie") else 0)).lastrowid
        for co in c.get("co_players", []):
            db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?,?)",
                       (pa, names[co["name"]]))
            co_links += 1

    # parallels (existing subsets only) + "{subset} Base" row each
    par_rows, skipped = 0, []
    for subset, ladder in LADDERS.items():
        if subset not in is_id:
            skipped.append(subset); continue
        iid = is_id[subset]
        db.execute("INSERT INTO parallels (insert_set_id, name, print_run, exclusivity) VALUES (?,?,NULL,NULL)",
                   (iid, f"{subset} Base"))
        par_rows += 1
        for (pname, pr, excl) in ladder:
            db.execute("INSERT INTO parallels (insert_set_id, name, print_run, exclusivity) VALUES (?,?,?,?)",
                       (iid, pname, pr, excl))
            par_rows += 1
    db.commit()

    # ---- reconcile ----------------------------------------------------------
    mism = []
    for subset, gate in GATE.items():
        got = db.execute("SELECT COUNT(*) FROM player_appearances WHERE insert_set_id=?", (is_id[subset],)).fetchone()[0]
        if got != gate:
            mism.append((subset, gate, got))
    total = db.execute(
        "SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id WHERE i.set_id=?",
        (set_id,)).fetchone()[0]
    numbered = db.execute(
        "SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id WHERE i.set_id=? AND p.print_run IS NOT NULL",
        (set_id,)).fetchone()[0]

    print(f"\nTotal appearances: {total} (expect 888)")
    print(f"Co-player links: {co_links} (expect 8)")
    print(f"Parallel rows attached/created: {par_rows} (expect 123)")
    print(f"  numbered parallels: {numbered}")
    print(f"Subsets with no parallels (by design): {sorted(NO_PARALLELS)}")
    print(f"Skip-and-report (unmapped parallel subsets): {skipped if skipped else 'none'}")
    if mism:
        print("INTEGRITY GATE MISMATCH:")
        for s, g, got in mism: print(f"  {s}: gate={g} db={got}")
        print("STOP."); raise SystemExit(1)
    print("INTEGRITY GATE: all 19 subset counts match. OK.")
    db.close()


if __name__ == "__main__":
    main()
