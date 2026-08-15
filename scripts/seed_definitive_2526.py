"""
Seed 2025-26 Topps Definitive Basketball (Phase 1) into local SQLite.
Structure + cards + box config. NO parallels, NO pack odds (neither published).
All-hits product: no base subset (legitimate). Local SQLite only — Tyler migrates.

Subset type flags (is_base/is_relic/is_booklet/is_autograph) are set EXPLICITLY
per subset from the checklist section headers (never inferred from names).

Pre-order date Aug 18, 2026 is NOT a release date; release_date left NULL
(no pre-order column in schema). Recorded in the run report instead.

Usage: python3 scripts/seed_definitive_2526.py
Data (scratchpad):
  definitive_single.jsonl   943 single-subject cards
  definitive_multi.jsonl     35 multi-subject cards (platform-first triple autos)
"""
import json, os, sqlite3

DB = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
SCRATCH = "/private/tmp/claude-501/-Users-tyler-Documents-Development-the-c-list/1d898db3-312e-40c2-b51f-b061eade264d/scratchpad"
SINGLE = os.path.join(SCRATCH, "definitive_single.jsonl")
MULTI = os.path.join(SCRATCH, "definitive_multi.jsonl")

SET = dict(
    name="2025-26 Topps Definitive Basketball", sport="Basketball", season="2025-26",
    league="NBA", tier="Premium",
    sample_image_url="/sets/2025-26-topps-definitive-basketball.jpg",
    release_date=None, slug="2025-26-topps-definitive-basketball",
    is_visible=1, created_at="2026-08-14T12:00:00Z", topps_url=None,
)

BOX_CONFIG = {
    "hobby": {"cards_per_pack": None, "packs_per_box": None, "boxes_per_case": None,
              "autos_per_box": None, "notes": "Configuration TBA"},
    "fdi": {"cards_per_pack": 8, "packs_per_box": 1, "boxes_per_case": None, "autos_per_box": 6},
}

# (name, is_base, is_relic, is_booklet, is_autograph) — explicit per SUBSETS block
SUBSETS = [
    ("Definitive Autograph Relics", 0, 1, 0, 1),
    ("Definitive Rookie Patch Autographs", 0, 1, 0, 1),
    ("Authentic Relic Autographs", 0, 1, 0, 1),
    ("Opening Act Rookie Relic Autographs", 0, 1, 0, 1),
    ("Definable Relic Autographs", 0, 1, 0, 1),
    ("Rookie Defining Games Relic Autograph", 0, 1, 0, 1),
    ("Definitive Markers Autographs", 0, 0, 0, 1),
    ("Definitive Moments Collection Autographs", 0, 0, 0, 1),
    ("Dual Rookie Autographs", 0, 0, 0, 1),
    ("Triple Rookie Autographs", 0, 0, 0, 1),
    ("Dual Autographs", 0, 0, 0, 1),
    ("Triple Autographs", 0, 0, 0, 1),
    ("Legendary Autograph Collection", 0, 0, 0, 1),
    ("Decisive Signatures", 0, 0, 0, 1),
    ("Definitive Rookies Autographs", 0, 0, 0, 1),
    ("Definitive Autographs", 0, 0, 0, 1),
    ("Defining Images Autographs", 0, 0, 0, 1),
    ("Definitive Signs", 0, 0, 0, 1),
    ("Noble Ink", 0, 0, 0, 1),
    ("Framed Legends Autograph Collection", 0, 0, 0, 1),
    ("Framed Rookies Autograph Collection", 0, 0, 0, 1),
    ("Framed Veterans Autograph Collection", 0, 0, 0, 1),
    ("Definitive Patch Collection", 0, 1, 0, 0),
    ("Definitive Rookie Patch Collection", 0, 1, 0, 0),
    ("Definitive Relic Collection", 0, 1, 0, 0),
    ("Definitive Nameplate I", 0, 1, 0, 0),
    ("Definitive Nameplate II", 0, 1, 0, 0),
]

CARD_GATE = {  # subset -> (total cards, rookie primaries)
    "Definitive Autograph Relics": (86, 0),
    "Definitive Rookie Patch Autographs": (42, 42),
    "Authentic Relic Autographs": (32, 0),
    "Opening Act Rookie Relic Autographs": (20, 20),
    "Definable Relic Autographs": (22, 0),
    "Rookie Defining Games Relic Autograph": (2, 2),
    "Definitive Markers Autographs": (19, 0),
    "Definitive Moments Collection Autographs": (30, 10),
    "Dual Rookie Autographs": (15, 15),
    "Triple Rookie Autographs": (5, 5),
    "Dual Autographs": (10, 0),
    "Triple Autographs": (5, 0),
    "Legendary Autograph Collection": (15, 0),
    "Decisive Signatures": (30, 5),
    "Definitive Rookies Autographs": (30, 30),
    "Definitive Autographs": (40, 0),
    "Defining Images Autographs": (30, 3),
    "Definitive Signs": (30, 3),
    "Noble Ink": (39, 0),
    "Framed Legends Autograph Collection": (30, 0),
    "Framed Rookies Autograph Collection": (39, 39),
    "Framed Veterans Autograph Collection": (29, 0),
    "Definitive Patch Collection": (56, 0),
    "Definitive Rookie Patch Collection": (38, 38),
    "Definitive Relic Collection": (100, 0),
    "Definitive Nameplate I": (100, 0),
    "Definitive Nameplate II": (84, 60),
}


def main():
    single = [json.loads(l) for l in open(SINGLE, encoding="utf-8") if l.strip()]
    multi = [json.loads(l) for l in open(MULTI, encoding="utf-8") if l.strip()]
    if len(single) != 943:
        print(f"STOP: {len(single)} single cards, exp 943"); raise SystemExit(1)
    if len(multi) != 35:
        print(f"STOP: {len(multi)} multi cards, exp 35"); raise SystemExit(1)

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

    is_id = {}
    for name, b, r, k, a in SUBSETS:
        is_id[name] = db.execute(
            "INSERT INTO insert_sets (set_id, name, is_autograph, is_base, is_relic, is_booklet) VALUES (?,?,?,?,?,?)",
            (set_id, name, a, b, r, k)).lastrowid
    print(f"Created {len(is_id)} subsets")

    pid = {}
    def player(nm):
        if nm not in pid:
            pid[nm] = db.execute(
                "INSERT INTO players (set_id, name, subject_role) VALUES (?,?,'athlete')",
                (set_id, nm)).lastrowid
        return pid[nm]

    for c in single:
        player(c["player"])
    for m in multi:
        player(m["primary"]["player"])
        for co in m["co_players"]:
            player(co["player"])
    print(f"Created {len(pid)} players")

    for c in single:
        db.execute(
            """INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, subset_tag, team)
               VALUES (?,?,?,?,NULL,?)""",
            (pid[c["player"]], is_id[c["subset"]], c["code"],
             1 if c.get("is_rookie") else 0, c.get("team")))

    co_links = 0
    for m in multi:
        p = m["primary"]
        pa = db.execute(
            """INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, subset_tag, team)
               VALUES (?,?,?,?,NULL,?)""",
            (pid[p["player"]], is_id[m["subset"]], m["code"],
             1 if p.get("is_rookie") else 0, p.get("team"))).lastrowid
        for co in m["co_players"]:
            db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?,?)",
                       (pa, pid[co["player"]]))
            co_links += 1

    # ---- integrity gates (run pre-commit; rollback on any mismatch) ----
    fail = []
    n_sub = db.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id=?", (set_id,)).fetchone()[0]
    if n_sub != 27: fail.append(f"insert_sets={n_sub} exp 27")
    fc = db.execute("SELECT SUM(is_relic=1 AND is_autograph=1), SUM(is_autograph=1 AND is_relic=0), SUM(is_relic=1 AND is_autograph=0), SUM(is_base), SUM(is_booklet) FROM insert_sets WHERE set_id=?", (set_id,)).fetchone()
    if fc[0] != 6: fail.append(f"auto+relic subsets={fc[0]} exp 6")
    if fc[1] != 16: fail.append(f"auto-only subsets={fc[1]} exp 16")
    if fc[2] != 5: fail.append(f"relic-only subsets={fc[2]} exp 5")
    if fc[3] != 0: fail.append(f"is_base sum={fc[3]} exp 0")
    if fc[4] != 0: fail.append(f"is_booklet sum={fc[4]} exp 0")

    total = db.execute(
        "SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id WHERE i.set_id=?",
        (set_id,)).fetchone()[0]
    if total != 978: fail.append(f"cards={total} exp 978")

    for s, (c, k) in CARD_GATE.items():
        gc = db.execute("SELECT COUNT(*) FROM player_appearances WHERE insert_set_id=?", (is_id[s],)).fetchone()[0]
        gk = db.execute("SELECT COUNT(*) FROM player_appearances WHERE insert_set_id=? AND is_rookie=1", (is_id[s],)).fetchone()[0]
        if gc != c or gk != k: fail.append(f"cards[{s}]={gc}/{gk} exp {c}/{k}")

    n_co = db.execute(
        """SELECT COUNT(*) FROM appearance_co_players acp
           JOIN player_appearances pa ON pa.id=acp.appearance_id
           JOIN insert_sets i ON i.id=pa.insert_set_id WHERE i.set_id=?""", (set_id,)).fetchone()[0]
    if n_co != 45: fail.append(f"co_player links={n_co} exp 45")

    # rookie flags across ALL appearance rows (primary appearances + co-player entries in source)
    src_rookie = (sum(1 for c in single if c.get("is_rookie"))
                  + sum(1 for m in multi if m["primary"].get("is_rookie"))
                  + sum(1 for m in multi for co in m["co_players"] if co.get("is_rookie")))
    if src_rookie != 297: fail.append(f"rookie flags (primary+co)={src_rookie} exp 297")

    # unique subjects across primary + co-player names
    subjects = set(c["player"] for c in single) \
        | set(m["primary"]["player"] for m in multi) \
        | set(co["player"] for m in multi for co in m["co_players"])
    if len(subjects) != 180: fail.append(f"unique subjects={len(subjects)} exp 180")
    n_pl = db.execute("SELECT COUNT(*) FROM players WHERE set_id=?", (set_id,)).fetchone()[0]
    if n_pl != len(subjects): fail.append(f"players table={n_pl} != unique subjects {len(subjects)}")
    n_nonath = db.execute("SELECT COUNT(*) FROM players WHERE set_id=? AND subject_role!='athlete'", (set_id,)).fetchone()[0]
    if n_nonath != 0: fail.append(f"non-athlete subjects={n_nonath} exp 0")

    n_par = db.execute("SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id WHERE i.set_id=?", (set_id,)).fetchone()[0]
    if n_par != 0: fail.append(f"parallels={n_par} exp 0")

    print(f"\nTotals: cards={total} co-links={n_co} players={n_pl} rookie(src)={src_rookie} parallels={n_par}")
    print(f"Subset flag mix: auto+relic={fc[0]} auto-only={fc[1]} relic-only={fc[2]} base={fc[3]} booklet={fc[4]}")
    if fail:
        db.rollback()
        print("\nINTEGRITY GATE MISMATCHES (rolled back, nothing written):")
        for m in fail:
            print("  ", m)
        raise SystemExit(1)
    db.commit()
    print("\nINTEGRITY GATES: all pass. Committed.")
    db.close()


if __name__ == "__main__":
    main()
