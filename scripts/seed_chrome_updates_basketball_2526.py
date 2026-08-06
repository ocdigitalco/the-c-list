"""
Seed 2025-26 Topps Chrome Updates Basketball (Phase 1) into local SQLite.
Structure + cards + parallels + box config. Pack odds are Phase 2 (pack_odds NULL).
Local SQLite only — Tyler migrates to Turso separately.

Card data:      scripts/chrome_updates_basketball_2526.jsonl           (1299 rows)
Parallel data:  scripts/chrome_updates_basketball_2526_parallels.jsonl (359 rows)

Model decisions (verified against precedent set 863 = 2026 Topps Chrome Baseball):
  * insert_sets.is_autograph carries the prompt's is_autograph_subset flag.
  * players.subject_role taken from the JSONL (celebrity for Druski / Spike Lee).
  * players are per-set, distinct by name (T.J. McConnell / P.J. Washington already
    normalized in the JSONL -> 322 unique rows).
  * parallels.exclusivity left NULL in Phase 1 (derivable in Phase 2 from odds).
  * No multi-subject cards -> appearance_co_players gets zero rows.

Usage: python3 scripts/seed_chrome_updates_basketball_2526.py
"""
import json, os, sqlite3

DB = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
CARDS = os.path.join(os.path.dirname(__file__), "chrome_updates_basketball_2526.jsonl")
PARS = os.path.join(os.path.dirname(__file__), "chrome_updates_basketball_2526_parallels.jsonl")

SET = dict(
    name="2025-26 Topps Chrome Updates Basketball", sport="Basketball",
    season="2025-26", league="NBA", tier="Chrome",
    sample_image_url="/sets/2025-26-topps-chrome-updates-basketball.jpg",
    release_date=None, slug="2025-26-topps-chrome-updates-basketball",
    is_visible=1, created_at="2026-08-06T12:00:00Z",
    topps_url="https://launches.topps.com/en-US/launch/2025-26-topps-chromer-updates-basketball-hobby-box",
)

AUTO_SUBSETS = {
    "Topps Chrome Autographs", "Rookie Autographs Lava Lamp", "Havoc Marks",
    "1980-81 Topps Basketball Autographs", "Future Stars Autographs",
    "Chromographs", "NBA Debut Patch Autographs",
}

BOX_CONFIG = {
    "hobby": {"cards_per_pack": 4, "packs_per_box": 20, "autos_per_box": 1},
    "jumbo": {"cards_per_pack": 11, "packs_per_box": 12, "autos_per_box": 3},
    "delight": {"cards_per_pack": 12, "packs_per_box": 1, "autos_per_box": 2},
    "value": {"cards_per_pack": 4, "packs_per_box": 7,
              "notes": "Exclusive Basketball parallel and retail short prints: Glass Canvas, Paradox, Fanatical"},
    "mega": {"cards_per_pack": 6, "packs_per_box": 7,
             "notes": "Exclusive X-Fractor parallel and retail short prints: Glass Canvas, Paradox, Fanatical"},
    "sapphire": {"cards_per_pack": None, "packs_per_box": None,
                 "notes": "Sapphire SKU of this product; box configuration not yet published"},
}

# ---- integrity gates --------------------------------------------------------
CARD_GATE = {
    "Base Cards": (200, 50), "Clutch City": (15, 15), "New Editions": (20, 20),
    "Stratospheric Stars": (25, 0), "Power Players": (25, 0), "Fortune 15": (15, 0),
    "Go Time": (15, 5), "Activators": (20, 0), "Moment in Time": (25, 5),
    "Clutch Gene": (30, 10), "No Limit": (10, 0), "Base Cards Image Variations": (50, 10),
    "Sapphire Selections": (20, 20), "Infinite Sapphire": (20, 5), "Shadow Etch": (15, 5),
    "Celebracion": (15, 0), "Captains": (20, 5), "Radiating Rookies": (15, 15),
    "Helix": (20, 5), "Fanatical": (25, 15), "Glass Canvas": (25, 5), "Paradox": (25, 5),
    "Base Cards Denim Tear": (100, 10), "Alter Egos": (10, 2), "Minionfractor": (5, 1),
    "Topps Chrome Autographs": (100, 40), "Rookie Autographs Lava Lamp": (50, 50),
    "Havoc Marks": (91, 20), "1980-81 Topps Basketball Autographs": (50, 15),
    "Future Stars Autographs": (50, 50), "Chromographs": (94, 50),
    "NBA Debut Patch Autographs": (93, 91), "NBA Debut Patch (Non-Autograph)": (6, 6),
}
PAR_GATE = {
    "Base Cards": 63, "Clutch City": 17, "New Editions": 17, "Stratospheric Stars": 17,
    "Power Players": 17, "Fortune 15": 17, "Go Time": 17, "Activators": 17,
    "Moment in Time": 17, "Clutch Gene": 17, "No Limit": 17,
    "Base Cards Image Variations": 6, "Sapphire Selections": 5, "Shadow Etch": 1,
    "Celebracion": 1, "Captains": 1, "Radiating Rookies": 1, "Helix": 1, "Fanatical": 5,
    "Glass Canvas": 1, "Paradox": 1, "Alter Egos": 1, "Minionfractor": 2,
    "Topps Chrome Autographs": 29, "Rookie Autographs Lava Lamp": 7, "Havoc Marks": 19,
    "1980-81 Topps Basketball Autographs": 19, "Future Stars Autographs": 19, "Chromographs": 7,
}


def main():
    cards = [json.loads(l) for l in open(CARDS) if l.strip()]
    pars = [json.loads(l) for l in open(PARS) if l.strip()]
    if len(cards) != 1299:
        print(f"STOP: parsed {len(cards)} cards, expected 1299."); raise SystemExit(1)
    if len(pars) != 359:
        print(f"STOP: parsed {len(pars)} parallels, expected 359."); raise SystemExit(1)

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

    # subsets in first-appearance (= checklist) order
    subset_order, seen = [], set()
    for c in cards:
        if c["subset"] not in seen:
            seen.add(c["subset"]); subset_order.append(c["subset"])
    is_id = {}
    for name in subset_order:
        auto = 1 if name in AUTO_SUBSETS else 0
        is_id[name] = db.execute(
            "INSERT INTO insert_sets (set_id, name, is_autograph) VALUES (?,?,?)",
            (set_id, name, auto)).lastrowid
    print(f"Created {len(is_id)} subsets ({sum(1 for n in is_id if n in AUTO_SUBSETS)} autograph)")

    # players: per-set, distinct by name; subject_role from first appearance
    pid = {}
    for c in cards:
        nm = c["player"]
        if nm not in pid:
            pid[nm] = db.execute(
                "INSERT INTO players (set_id, name, subject_role) VALUES (?,?,?)",
                (set_id, nm, c.get("subject_role", "athlete"))).lastrowid
    print(f"Created {len(pid)} players")

    # appearances (team + is_rookie per card; card_number as printed)
    for c in cards:
        db.execute(
            """INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, subset_tag, team)
               VALUES (?,?,?,?,?,?)""",
            (pid[c["player"]], is_id[c["subset"]], c["code"],
             1 if c.get("is_rookie") else 0, None, c.get("team")))

    # parallels (existing subsets only, exclusivity NULL in Phase 1)
    par_rows = 0
    for p in pars:
        if p["subset"] not in is_id:
            print(f"STOP: parallel references unknown subset {p['subset']!r}."); raise SystemExit(1)
        db.execute("INSERT INTO parallels (insert_set_id, name, print_run, exclusivity) VALUES (?,?,?,NULL)",
                   (is_id[p["subset"]], p["parallel"], p["print_run"]))
        par_rows += 1
    db.commit()

    # ---- reconciliation against gates ---------------------------------------
    fail = []
    # subsets
    n_sub = db.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id=?", (set_id,)).fetchone()[0]
    n_auto = db.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_autograph=1", (set_id,)).fetchone()[0]
    if n_sub != 33: fail.append(f"insert_sets={n_sub} exp 33")
    if n_auto != 7: fail.append(f"autograph subsets={n_auto} exp 7")
    # cards
    total = db.execute(
        "SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id WHERE i.set_id=?",
        (set_id,)).fetchone()[0]
    if total != 1299: fail.append(f"cards={total} exp 1299")
    for s, (c, k) in CARD_GATE.items():
        gc = db.execute("SELECT COUNT(*) FROM player_appearances WHERE insert_set_id=?", (is_id[s],)).fetchone()[0]
        gk = db.execute("SELECT COUNT(*) FROM player_appearances WHERE insert_set_id=? AND is_rookie=1", (is_id[s],)).fetchone()[0]
        if gc != c or gk != k: fail.append(f"cards[{s}]={gc}/{gk} exp {c}/{k}")
    rk = db.execute(
        "SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id WHERE i.set_id=? AND pa.is_rookie=1",
        (set_id,)).fetchone()[0]
    if rk != 530: fail.append(f"rookie total={rk} exp 530")
    # players
    n_pl = db.execute("SELECT COUNT(*) FROM players WHERE set_id=?", (set_id,)).fetchone()[0]
    n_cel = db.execute("SELECT COUNT(*) FROM players WHERE set_id=? AND subject_role='celebrity'", (set_id,)).fetchone()[0]
    if n_pl != 322: fail.append(f"players={n_pl} exp 322")
    if n_cel != 2: fail.append(f"celebrity players={n_cel} exp 2")
    # parallels
    n_par = db.execute(
        "SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id WHERE i.set_id=?",
        (set_id,)).fetchone()[0]
    if n_par != 359: fail.append(f"parallels={n_par} exp 359")
    n_pr = db.execute(
        "SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id WHERE i.set_id=? AND p.print_run IS NOT NULL",
        (set_id,)).fetchone()[0]
    if n_pr != 37: fail.append(f"numbered parallels={n_pr} exp 37")
    n_pr_base = db.execute(
        "SELECT COUNT(*) FROM parallels WHERE insert_set_id=? AND print_run IS NOT NULL", (is_id["Base Cards"],)).fetchone()[0]
    if n_pr_base != 37: fail.append(f"numbered parallels on Base Cards={n_pr_base} exp 37")
    for s, c in PAR_GATE.items():
        gc = db.execute("SELECT COUNT(*) FROM parallels WHERE insert_set_id=?", (is_id[s],)).fetchone()[0]
        if gc != c: fail.append(f"parallels[{s}]={gc} exp {c}")
    for s in ("Base Cards Denim Tear", "Infinite Sapphire", "NBA Debut Patch Autographs", "NBA Debut Patch (Non-Autograph)"):
        gc = db.execute("SELECT COUNT(*) FROM parallels WHERE insert_set_id=?", (is_id[s],)).fetchone()[0]
        if gc != 0: fail.append(f"parallels[{s}]={gc} exp 0 (zero-parallel subset)")

    print(f"\nTotal cards: {total} | rookie: {rk} | players: {n_pl} (celebrity {n_cel}) | parallels: {n_par} (numbered {n_pr})")
    if fail:
        print("INTEGRITY GATE MISMATCHES:")
        for m in fail:
            print("  ", m)
        print("STOP: gate mismatch — investigate.")
        raise SystemExit(1)
    print("INTEGRITY GATES: all pass. OK.")
    db.close()


if __name__ == "__main__":
    main()
