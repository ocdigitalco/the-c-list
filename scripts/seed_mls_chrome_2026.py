"""
Seed 2026 Topps Chrome Major League Soccer (Phase 1) into local SQLite.
Structure + cards + box config. No parallels, no pack odds (Phase 2 at release).
Local SQLite only — Tyler migrates to Turso separately.

Data:
  scripts/mls_chrome_2026.jsonl        529 single-subject cards
  scripts/mls_chrome_2026_multi.jsonl   14 multi-subject cards (primary + 1 co-player link)

Model decisions (verified vs precedents 863 Chrome Baseball / 866 Chrome Updates):
  * sport="Soccer" (matches existing soccer sets); league="MLS"; tier="Chrome".
  * insert_sets.is_autograph carries is_autograph_subset. No exclusivity column exists
    (labels recorded in the run report for Phase 2).
  * players per-set, distinct by name; subject_role from data (MLS Trophy = 'character').
  * multi-subject: ONE card = primary appearance (team + is_rookie) + appearance_co_players link.
  * MLS Trophy MLS-1 has team NULL (player_appearances.team is nullable).

Usage: python3 scripts/seed_mls_chrome_2026.py
"""
import json, os, sqlite3

DB = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
CARDS = os.path.join(os.path.dirname(__file__), "mls_chrome_2026.jsonl")
MULTI = os.path.join(os.path.dirname(__file__), "mls_chrome_2026_multi.jsonl")

SET = dict(
    name="2026 Topps Chrome Major League Soccer", sport="Soccer", season="2026",
    league="MLS", tier="Chrome",
    sample_image_url="/sets/2026-topps-mls-chrome-soccer.jpg",
    release_date="2026-09-10", slug="2026-topps-mls-chrome-soccer",
    is_visible=1, created_at="2026-08-13T12:00:00Z", topps_url=None,
)

AUTO_SUBSETS = {
    "Chrome Autographs", "Summer Clash Autographs", "MLS All-Timers Autographs",
    "Mania Autographs", "MLS Renaissance Autographs", "Chrome Dual Autographs",
    "National Pairings Dual Autographs", "MLS Debut Patch Autographs",
}

# box config — 863/866 shape (lowercase format keys); TBA stored as null / omitted.
BOX_CONFIG = {
    "hobby": {"cards_per_pack": 4, "packs_per_box": 20, "boxes_per_case": 12, "autos_per_box": 2},
    "value": {"cards_per_pack": 4, "packs_per_box": 7},
    "mania": {"cards_per_pack": None, "packs_per_box": None, "notes": "Configuration TBA"},
}

CARD_GATE = {
    "Base Cards": (200, 49), "Rhythm of the Game": (30, 4), "Wonderkids": (30, 24),
    "Patriotic Passion": (10, 0), "Tide Turner": (30, 3), "Pearlers": (20, 3),
    "Shadow Etch": (20, 3), "Helix": (5, 0), "MLS Trophy": (1, 0), "The Grail": (1, 0),
    "Chrome Autographs": (81, 21), "Summer Clash Autographs": (17, 3),
    "MLS All-Timers Autographs": (19, 0), "Mania Autographs": (4, 0),
    "MLS Renaissance Autographs": (24, 5), "MLS Debut Patch Autographs": (37, 32),
    "Chrome Dual Autographs": (10, 0), "National Pairings Dual Autographs": (4, 0),
}
SUBSET_ORDER = ["Base Cards", "Rhythm of the Game", "Wonderkids", "Patriotic Passion",
    "Tide Turner", "Pearlers", "Shadow Etch", "Helix", "MLS Trophy", "The Grail",
    "Chrome Autographs", "Summer Clash Autographs", "MLS All-Timers Autographs",
    "Mania Autographs", "MLS Renaissance Autographs", "Chrome Dual Autographs",
    "National Pairings Dual Autographs", "MLS Debut Patch Autographs"]


def main():
    single = [json.loads(l) for l in open(CARDS) if l.strip()]
    multi = [json.loads(l) for l in open(MULTI) if l.strip()]
    if len(single) != 529:
        print(f"STOP: {len(single)} single cards, exp 529"); raise SystemExit(1)
    if len(multi) != 14:
        print(f"STOP: {len(multi)} multi cards, exp 14"); raise SystemExit(1)

    db = sqlite3.connect(os.path.abspath(DB))
    if db.execute("SELECT id FROM sets WHERE slug=? OR name=?", (SET["slug"], SET["name"])).fetchone():
        print("STOP: set already exists."); raise SystemExit(1)

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

    # subsets in checklist order
    is_id = {}
    for name in SUBSET_ORDER:
        auto = 1 if name in AUTO_SUBSETS else 0
        is_id[name] = db.execute(
            "INSERT INTO insert_sets (set_id, name, is_autograph) VALUES (?,?,?)",
            (set_id, name, auto)).lastrowid
    print(f"Created {len(is_id)} subsets ({sum(1 for n in is_id if n in AUTO_SUBSETS)} autograph)")

    # players: distinct by name; subject_role from single-subject data, else athlete
    pid = {}
    def player(nm, role="athlete"):
        if nm not in pid:
            pid[nm] = db.execute(
                "INSERT INTO players (set_id, name, subject_role) VALUES (?,?,?)",
                (set_id, nm, role)).lastrowid
        return pid[nm]
    for c in single:
        player(c["player"], c.get("subject_role", "athlete"))
    for m in multi:
        player(m["primary"]["player"])
        player(m["co_player"]["player"])
    print(f"Created {len(pid)} players")

    # appearances (single-subject)
    for c in single:
        db.execute(
            """INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, subset_tag, team)
               VALUES (?,?,?,?,NULL,?)""",
            (pid[c["player"]], is_id[c["subset"]], c["code"],
             1 if c.get("is_rookie") else 0, c.get("team")))

    # appearances (multi) + co-player links
    co_links = 0
    for m in multi:
        p = m["primary"]
        pa = db.execute(
            """INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, subset_tag, team)
               VALUES (?,?,?,?,NULL,?)""",
            (pid[p["player"]], is_id[m["subset"]], m["code"],
             1 if p.get("is_rookie") else 0, p.get("team"))).lastrowid
        db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?,?)",
                   (pa, pid[m["co_player"]["player"]]))
        co_links += 1

    db.commit()

    # ---- integrity gates ----
    fail = []
    n_sub = db.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id=?", (set_id,)).fetchone()[0]
    n_auto = db.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_autograph=1", (set_id,)).fetchone()[0]
    if n_sub != 18: fail.append(f"insert_sets={n_sub} exp 18")
    if n_auto != 8: fail.append(f"autograph subsets={n_auto} exp 8")
    total = db.execute(
        "SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id WHERE i.set_id=?",
        (set_id,)).fetchone()[0]
    if total != 543: fail.append(f"cards={total} exp 543")
    for s, (c, k) in CARD_GATE.items():
        gc = db.execute("SELECT COUNT(*) FROM player_appearances WHERE insert_set_id=?", (is_id[s],)).fetchone()[0]
        gk = db.execute("SELECT COUNT(*) FROM player_appearances WHERE insert_set_id=? AND is_rookie=1", (is_id[s],)).fetchone()[0]
        if gc != c or gk != k: fail.append(f"cards[{s}]={gc}/{gk} exp {c}/{k}")
    rk = db.execute(
        "SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id WHERE i.set_id=? AND pa.is_rookie=1",
        (set_id,)).fetchone()[0]
    if rk != 147: fail.append(f"rookie total={rk} exp 147")
    n_pl = db.execute("SELECT COUNT(*) FROM players WHERE set_id=?", (set_id,)).fetchone()[0]
    if n_pl != 239: fail.append(f"players={n_pl} exp 239")
    n_char = db.execute("SELECT COUNT(*) FROM players WHERE set_id=? AND subject_role='character'", (set_id,)).fetchone()[0]
    if n_char != 1: fail.append(f"character players={n_char} exp 1")
    n_co = db.execute(
        """SELECT COUNT(*) FROM appearance_co_players acp
           JOIN player_appearances pa ON pa.id=acp.appearance_id
           JOIN insert_sets i ON i.id=pa.insert_set_id WHERE i.set_id=?""", (set_id,)).fetchone()[0]
    if n_co != 14: fail.append(f"co_player links={n_co} exp 14")
    n_par = db.execute("SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id WHERE i.set_id=?", (set_id,)).fetchone()[0]
    if n_par != 0: fail.append(f"parallels={n_par} exp 0")
    trophy_team = db.execute(
        "SELECT pa.team FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id WHERE i.set_id=? AND pa.card_number='MLS-1'",
        (set_id,)).fetchone()[0]
    if trophy_team is not None: fail.append(f"MLS-1 team={trophy_team!r} exp NULL")

    print(f"\nTotal cards: {total} | rookie: {rk} | players: {n_pl} (character {n_char}) | co-links: {n_co} | parallels: {n_par}")
    if fail:
        print("INTEGRITY GATE MISMATCHES:")
        for m in fail:
            print("  ", m)
        raise SystemExit(1)
    print("INTEGRITY GATES: all pass. OK.")
    db.close()


if __name__ == "__main__":
    main()
