"""
Seed 2026 Topps Chrome Baseball (set) into local SQLite, then attach parallels
+ box configuration. Local SQLite only — Tyler migrates to Turso separately.

Card data: scratchpad chrome_bb_2026.jsonl (1601 lines, extracted verbatim from
the task). Co-player subsets store ONE appearance + appearance_co_players links.

Model decisions (verified against precedent set 860 = 2026 Topps Chrome Marvel):
  * Format exclusivity → parallels.exclusivity string (null = all products),
    exactly as 860 stores Hobby/Value/Mega. No numeric odds given → pack_odds
    stays NULL; "unavailable in a format" is carried by the exclusivity tag.
  * Base-version parallel row named "Base" (860 convention; the "{subset} Base"
    in the brief is the odds-key form, moot without odds).
  * card_number null → "" (empty string; precedent set 987 redemptions).

Usage: python3 scripts/seed_chrome_baseball_2026.py
"""
import json, os, sqlite3

DB = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
DATA = os.path.join(os.path.dirname(__file__), "chrome_baseball_2026.jsonl")

SET = dict(
    name="2026 Topps Chrome Baseball", sport="Baseball", season="2026", league="MLB",
    tier="Chrome", sample_image_url="/sets/2026-topps-chrome-baseball.jpg",
    release_date="2026-07-22", slug="2026-topps-chrome-baseball", is_visible=1,
    created_at="2026-07-21T12:00:00Z", topps_url=None,
)

AUTO_SUBSETS = {
    "Rookie Autographs", "Retail Rookie Autographs", "Chrome Autographs",
    "Chrome Legend Autographs", "World Series Champions Autographs",
    "1991 Topps Baseball Chrome Autographs", "Future Stars Autographs",
    "Perspectives Autographs", "Ink Strokes", "75th Diamond Autographs",
    "Chromographs", "2025 World Champions Autograph Refractor",
    "Radiating Rookies Autographs", "Dual Autographs",
    "2025 Chrome MVP Buybacks Autographs", "Cooperstown Calls Autograph Variation",
    "Numbers Live Forever Autograph Variation", "Jerry Seinfeld Autograph",
    "Gold Logoman Autograph Relics", "Gold Logoman Dual Autograph Relics",
}

GATE = {
    "Base Set": 300, "Ultra Violet": 15, "Base Cards Lightboard Logo Variation": 300,
    "2025 Chrome MVP Buybacks": 2, "Numbers Live Forever": 2,
    "Cooperstown Calls Class of 2026": 3, "Cooperstown Calls Class of 2025": 5,
    "Award Winners Base Variation": 6, "Radiating Rookies": 20, "Future Stars": 10,
    "Super Short Prints": 10, "Perspectives": 10, "World Series At Night": 10,
    "Chrome Champion Refractors": 16, "Shadow Etch": 20, "Helix": 15,
    "Static Noise": 15, "Hobby Masters": 19, "Fanatical": 10, "Wild Style": 25,
    "Past To Present": 25, "Topps Chrome Expose": 30, "Base Cards Image Variations": 50,
    "Big Ticket Players": 25, "Wrecking Crew": 25, "1991 Topps Baseball": 30,
    "Diamond Moments": 50, "2025 MLB Commissioners Trophy": 1, "Chrome Rivals - Home": 25,
    "Chrome Rivals - Away": 25, "Fanatics Authentics Redemption Cards": 30, "Minions": 4,
    "Rookie Autographs": 94, "Retail Rookie Autographs": 30, "Chrome Autographs": 6,
    "Chrome Legend Autographs": 47, "World Series Champions Autographs": 33,
    "1991 Topps Baseball Chrome Autographs": 6, "Future Stars Autographs": 8,
    "Perspectives Autographs": 6, "Ink Strokes": 71, "75th Diamond Autographs": 69,
    "Chromographs": 32, "2025 World Champions Autograph Refractor": 17,
    "Radiating Rookies Autographs": 15, "Dual Autographs": 8,
    "2025 Chrome MVP Buybacks Autographs": 2, "Cooperstown Calls Autograph Variation": 3,
    "Numbers Live Forever Autograph Variation": 2, "Jerry Seinfeld Autograph": 1,
    "Gold Logoman Relics": 6, "Gold Logoman Dual Relics": 3,
    "Gold Logoman Dual Autograph Relics": 3, "Gold Logoman Autograph Relics": 6,
}

# ---- parallel ladders (name, print_run, exclusivity) ------------------------
def L(rows, excl=None):
    return [(n, pr, excl) for (n, pr) in rows]

R7 = [("Green", 99), ("Purple", 75), ("Gold", 50), ("Orange", 25), ("Black", 10), ("Red", 5), ("Superfractor", 1)]
W5 = [("Purple Wave", 75), ("Gold Wave", 50), ("Orange Wave", 25), ("Black Wave", 10), ("Red Wave", 5)]
SUPER = [("Superfractor", 1)]
GORB_S = [("Gold", 50), ("Orange", 25), ("Black", 10), ("Red", 5), ("Superfractor", 1)]  # Shadow Etch / Numbers Live Forever
AUTO9 = [("Blue", 150), ("Green", 99), ("Purple", 75), ("Gold", 50), ("White", 30), ("Orange", 25), ("Black", 10), ("Red", 5), ("Superfractor", 1)]
AUTO8 = [("Green", 99), ("Purple", 75), ("Gold", 50), ("White", 30), ("Orange", 25), ("Black", 10), ("Red", 5), ("Superfractor", 1)]

def r7w5():
    return L(R7, None) + L(W5, "Jumbo")

BASE_PARS = [
    ("Base", None, None),
    ("Refractor", None, None), ("Negative Refractor", None, None),
    ("Wave Refractor", None, "Jumbo"), ("X-Fractor", None, "Mega"),
    ("Baseball Seams Refractor", None, "Value"), ("Raywave Refractor", None, "Value"),
    ("Red White and Blue Refractor", None, "Value"),
    ("Pink", 250, None),
    ("Aqua", 199, None), ("Aqua Raywave", 199, "Value"), ("Aqua X-Fractor", 199, "Mega"),
    ("Blue", 150, None), ("Blue Raywave", 150, "Value"), ("Blue Wave", 150, "Jumbo"), ("Blue X-Fractor", 150, "Mega"),
    ("Green", 99, None), ("Green Raywave", 99, "Value"), ("Green Wave", 99, "Jumbo"), ("Green X-Fractor", 99, "Mega"),
    ("75th Anniversary", 75, None),
    ("Purple", 75, None), ("Purple Raywave", 75, "Value"), ("Purple Wave", 75, "Jumbo"), ("Purple X-Fractor", 75, "Mega"),
    ("Gold", 50, None), ("Gold Raywave", 50, "Value"), ("Gold Wave", 50, "Jumbo"), ("Gold X-Fractor", 50, "Mega"),
    ("White", 30, None),
    ("Orange", 25, None), ("Orange Raywave", 25, "Value"), ("Orange Wave", 25, "Jumbo"), ("Orange X-Fractor", 25, "Mega"),
    ("Black", 10, None), ("Black Raywave", 10, "Value"), ("Black Wave", 10, "Jumbo"), ("Black X-Fractor", 10, "Mega"),
    ("Red", 5, None), ("Red Wave", 5, "Jumbo"), ("Frozenfractor", 5, None),
    ("Printing Plates", 1, None), ("Superfractor", 1, None),
]

RETAIL_RA = L([("Refractor", 499), ("Teal", 299), ("Yellow", 275), ("Pink", 250), ("Aqua", 199),
    ("Blue", 150), ("Green", 99), ("Green Raywave", 99), ("Purple", 75), ("Purple Raywave", 75),
    ("Gold", 50), ("Gold Raywave", 50), ("White", 30), ("Orange", 25), ("Orange Raywave", 25),
    ("Black", 10), ("Black Raywave", 10), ("Red", 5), ("Red Raywave", 5),
    ("Printing Plates", 1), ("Superfractor", 1)], None)

ROOKIE_RA = [
    ("Refractor", 499, None), ("Teal", 299, None), ("Yellow", 275, None), ("Pink", 250, None), ("Aqua", 199, None),
    ("Blue", 150, None), ("Green", 99, None), ("Green Raywave", 99, "Retail"), ("Purple", 75, None), ("Purple Raywave", 75, "Retail"),
    ("Gold", 50, None), ("Gold Raywave", 50, "Retail"), ("White", 30, None), ("Orange", 25, None), ("Orange Raywave", 25, "Retail"),
    ("Black", 10, None), ("Black Raywave", 10, "Retail"), ("Red", 5, None), ("Red Raywave", 5, "Retail"),
    ("Printing Plates", 1, None), ("Superfractor", 1, None),
]

PARALLELS = {
    "Base Set": BASE_PARS,
    "Ultra Violet": L(SUPER),
    "Numbers Live Forever": L(GORB_S),
    "Cooperstown Calls Class of 2026": [("Blue Refractor", 150, None)],
    "Cooperstown Calls Class of 2025": [("Green Refractor", 99, None)],
    "Radiating Rookies": L(SUPER),
    "Future Stars": r7w5(),
    "Perspectives": r7w5(),
    "Chrome Champion Refractors": L(SUPER),
    "Shadow Etch": L(GORB_S),
    "Helix": L(SUPER),
    "Hobby Masters": L(SUPER),
    "Wild Style": L(R7),
    "Past To Present": L(R7, "Retail"),
    "Big Ticket Players": r7w5(),
    "Wrecking Crew": r7w5(),
    "1991 Topps Baseball": r7w5(),
    "Diamond Moments": L(R7),
    "Chrome Rivals - Home": L(R7, "Hobby/Jumbo"),
    "Chrome Rivals - Away": L(R7, "Retail"),
    # autograph subsets
    "Jerry Seinfeld Autograph": L([("Black", 10), ("Red", 5), ("Superfractor", 1)]),
    "Numbers Live Forever Autograph Variation": L([("Orange", 25), ("Black", 10), ("Red", 5), ("Superfractor", 1)]),
    "Cooperstown Calls Autograph Variation": L([("Black", 10), ("Red", 5), ("Superfractor", 1)]),
    "Dual Autographs": L([("Black", 10), ("Red", 5), ("Superfractor", 1)]),
    "Chromographs": L([("Orange", 25), ("Black", 10), ("Red", 5), ("Superfractor", 1)]),
    "75th Diamond Autographs": L(AUTO9),
    "Ink Strokes": L(AUTO9),
    "Perspectives Autographs": L(AUTO8),
    "Future Stars Autographs": L(AUTO8),
    "1991 Topps Baseball Chrome Autographs": L(AUTO8),
    "Chrome Legend Autographs": L([("Orange", 25), ("Black", 10), ("Red", 5), ("Superfractor", 1)]),
    "Retail Rookie Autographs": RETAIL_RA,
    "Rookie Autographs": ROOKIE_RA,
}

BOX_CONFIG = {
    "hobby": {"cards_per_pack": 4, "packs_per_box": 20, "boxes_per_case": 12, "autos_per_box": 1, "notes": "1 autograph per box"},
    "jumbo": {"cards_per_pack": 11, "packs_per_box": 12, "boxes_per_case": 8, "autos_per_box": 2, "notes": "2 autographs per box"},
    "mega": {"cards_per_pack": 7, "packs_per_box": 6, "boxes_per_case": 20, "notes": "Mega-exclusive X-Fractor parallels"},
    "value": {"cards_per_pack": 4, "packs_per_box": 7, "boxes_per_case": 40, "notes": "Value-exclusive Baseball Seams & Red/White/Blue Refractor parallels"},
}


def main():
    cards = [json.loads(l) for l in open(DATA) if l.strip()]
    if len(cards) != 1601:
        print(f"STOP: parsed {len(cards)} cards, expected 1601."); raise SystemExit(1)

    db = sqlite3.connect(os.path.abspath(DB))
    if db.execute("SELECT id FROM sets WHERE slug=? OR name=?", (SET["slug"], SET["name"])).fetchone():
        print("STOP: set already exists. Not overwriting."); raise SystemExit(1)

    cur = db.execute(
        """INSERT INTO sets (name, sport, season, league, tier, sample_image_url,
                             release_date, slug, is_visible, created_at, topps_url,
                             box_config, pack_odds)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,NULL)""",
        (SET["name"], SET["sport"], SET["season"], SET["league"], SET["tier"],
         SET["sample_image_url"], SET["release_date"], SET["slug"], SET["is_visible"],
         SET["created_at"], SET["topps_url"], json.dumps(BOX_CONFIG)))
    set_id = cur.lastrowid
    print(f"Created set id {set_id}")

    # subsets in first-appearance order
    subset_order, seen = [], set()
    for c in cards:
        if c["subset"] not in seen:
            seen.add(c["subset"]); subset_order.append(c["subset"])
    is_id = {}
    for name in subset_order:
        auto = 1 if name in AUTO_SUBSETS else 0
        is_id[name] = db.execute("INSERT INTO insert_sets (set_id, name, is_autograph) VALUES (?,?,?)",
                                 (set_id, name, auto)).lastrowid
    print(f"Created {len(is_id)} subsets ({sum(1 for n in is_id if n in AUTO_SUBSETS)} autograph)")

    # players: distinct by name across primary + co-players
    names = {}
    def pid(nm, team):
        if nm not in names:
            names[nm] = db.execute(
                "INSERT INTO players (set_id, name, subject_role) VALUES (?,?,'athlete')", (set_id, nm)).lastrowid
        return names[nm]
    # first pass: create all player rows (primary then co)
    for c in cards:
        pid(c["name"], c.get("team"))
        for co in c.get("co_players", []):
            pid(co["name"], co.get("team"))
    print(f"Created {len(names)} players")

    # appearances + co-links
    co_links = 0
    for c in cards:
        cn = c["card_number"] if c["card_number"] is not None else ""
        pa = db.execute(
            """INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, subset_tag, team)
               VALUES (?,?,?,?,?,?)""",
            (names[c["name"]], is_id[c["subset"]], cn, 1 if c.get("rookie") else 0, None, c.get("team"))).lastrowid
        for co in c.get("co_players", []):
            db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?,?)",
                       (pa, names[co["name"]]))
            co_links += 1

    # parallels (existing subsets only)
    skipped, par_rows = [], 0
    for subset, rows in PARALLELS.items():
        if subset not in is_id:
            skipped.append(subset); continue
        for (pname, pr, excl) in rows:
            db.execute("INSERT INTO parallels (insert_set_id, name, print_run, exclusivity) VALUES (?,?,?,?)",
                       (is_id[subset], pname, pr, excl))
            par_rows += 1
    db.commit()

    # ---- INTEGRITY GATE reconciliation --------------------------------------
    mism = []
    for subset, gate in GATE.items():
        got = db.execute("SELECT COUNT(*) FROM player_appearances WHERE insert_set_id=?", (is_id[subset],)).fetchone()[0]
        if got != gate:
            mism.append((subset, gate, got))
    total = db.execute(
        "SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id WHERE i.set_id=?",
        (set_id,)).fetchone()[0]

    print(f"\nTotal appearances: {total} (expected 1601)")
    print(f"Co-player links: {co_links} (expected 39)")
    print(f"Parallel rows attached: {par_rows} across {len([s for s in PARALLELS if s in is_id])} subsets")
    print("Skip-and-report (unmapped parallel subsets):", skipped if skipped else "none")
    if mism:
        print("INTEGRITY GATE MISMATCHES:")
        for s, g, got in mism:
            print(f"  {s}: gate={g} db={got}")
        print("STOP: gate mismatch — investigate before proceeding.")
    else:
        print("INTEGRITY GATE: all 54 subset counts match. OK.")
    db.close()


if __name__ == "__main__":
    main()
