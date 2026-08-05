"""
Seed 2026 Topps Chrome Marvel Comics Sapphire Edition into local SQLite +
attach base parallels. Local SQLite only; Tyler migrates to Turso separately.

242 cards / 8 subsets. All subjects are Marvel characters (subject_role
='character'), team NULL. 17 "(DEBUT)" cards stored as is_rookie=1 (matches
Marvel 860 / Disney 846 precedent). Multi-subject Facsimile autos store ONE
appearance + appearance_co_players links (2/3/4 subjects per card).

Base parallels (Green/99 ... Padparadscha/1) attach to Characters I AND II
with a "{subset} Base" base-tier row each; odds NULL (none published).

Usage: python3 scripts/seed_marvel_comics_sapphire_2026.py
"""
import json, os, sqlite3

DB = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
DATA = os.path.join(os.path.dirname(__file__), "marvel_comics_sapphire_2026.jsonl")

SET = dict(
    name="2026 Topps Chrome Marvel Comics Sapphire Edition", sport="Entertainment",
    season="2026", league="Marvel", tier="Sapphire",
    sample_image_url="/sets/2026-topps-chrome-marvel-comics-sapphire-edition.jpg",
    release_date="2026-08-05", slug="2026-topps-chrome-marvel-comics-sapphire-edition",
    is_visible=1, created_at="2026-08-04T12:00:00Z",
    topps_url="https://www.topps.com/pages/topps-chrome-sapphire-marvel",
)

BOX_CONFIG = {
    "hobby": {"cards_per_pack": 4, "packs_per_box": 8, "boxes_per_case": 10,
              "notes": "4 numbered parallels per box (expectation)"},
}

AUTO_SUBSETS = {
    "Marvel Facsimile Autographs", "Marvel Facsimile Dual Autographs",
    "Marvel Facsimile Triple Autographs", "Marvel Facsimile Quad Autographs",
}

GATE = {
    "Characters I": 100, "Characters II": 100, "Hidden Gems": 5,
    "Marvel Facsimile Autographs": 15, "Marvel Facsimile Dual Autographs": 6,
    "Marvel Facsimile Triple Autographs": 4, "Marvel Facsimile Quad Autographs": 2,
    "Infinite": 10,
}

# base parallel ladder (name, print_run) — attach to Characters I and II
BASE_LADDER = [("Green", 99), ("Purple", 75), ("Gold", 50), ("Orange", 25), ("Black", 10), ("Padparadscha", 1)]
PARALLEL_SUBSETS = ["Characters I", "Characters II"]


def main():
    cards = [json.loads(l) for l in open(DATA) if l.strip()]
    if len(cards) != 242:
        print(f"STOP: parsed {len(cards)} cards, expected 242."); raise SystemExit(1)

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

    # players: distinct by name (primary + co), all subject_role 'character'
    names = {}
    def pid(nm):
        if nm not in names:
            names[nm] = db.execute("INSERT INTO players (set_id, name, subject_role) VALUES (?,?,'character')",
                                   (set_id, nm)).lastrowid
        return names[nm]
    for c in cards:
        pid(c["name"])
        for co in c.get("co_players", []):
            pid(co["name"])
    print(f"Created {len(names)} players (all subject_role='character')")

    # appearances + co-links
    co_links = 0
    for c in cards:
        pa = db.execute(
            """INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, subset_tag, team)
               VALUES (?,?,?,?,NULL,NULL)""",
            (names[c["name"]], is_id[c["subset"]], c["card_number"], 1 if c.get("is_rookie") else 0)).lastrowid
        for co in c.get("co_players", []):
            db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?,?)",
                       (pa, names[co["name"]]))
            co_links += 1

    # base parallels on Characters I and II + "{subset} Base" base-tier row
    par_rows = 0
    for subset in PARALLEL_SUBSETS:
        iid = is_id[subset]
        db.execute("INSERT INTO parallels (insert_set_id, name, print_run, exclusivity) VALUES (?,?,NULL,NULL)",
                   (iid, f"{subset} Base"))
        par_rows += 1
        for (pname, pr) in BASE_LADDER:
            db.execute("INSERT INTO parallels (insert_set_id, name, print_run, exclusivity) VALUES (?,?,?,NULL)",
                       (iid, pname, pr))
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
    debut = db.execute(
        "SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id WHERE i.set_id=? AND pa.is_rookie=1",
        (set_id,)).fetchone()[0]
    concrete = db.execute(
        "SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id WHERE i.set_id=? AND p.name NOT LIKE '% Base'",
        (set_id,)).fetchone()[0]
    basetier = par_rows - concrete

    print(f"\nTotal appearances: {total} (expect 242)")
    print(f"Debut flags (is_rookie=1): {debut} (expect 17)")
    print(f"Co-player links: {co_links} (expect 20)")
    print(f"Parallel rows: {par_rows} (expect 14 = {concrete} concrete + {basetier} base-tier)")
    if mism:
        print("INTEGRITY GATE MISMATCH:")
        for s, g, got in mism: print(f"  {s}: gate={g} db={got}")
        print("STOP."); raise SystemExit(1)
    print("INTEGRITY GATE: all 8 subset counts match. OK.")
    db.close()


if __name__ == "__main__":
    main()
