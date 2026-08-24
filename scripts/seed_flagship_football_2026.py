#!/usr/bin/env python3
"""
Seed 2026 Topps Flagship Football — Phase 1 (checklist only; no parallels, no odds).

Writes ONLY to the local SQLite DB (the-c-list.db). Turso migration is run
separately by scripts/migrate-to-turso.ts.

Usage:
    python3 scripts/seed_flagship_football_2026.py <data_dir>

<data_dir> must contain:
    subsets.json   — 87 subsets, display_order + type flags
    cards.jsonl    — 4042 card lines (one JSON object per line)

Co-player model mirrors seed.ts/buildCoPlayerLinks: each co_player becomes its
own player_appearance row sharing (insert_set_id, card_number) with the primary;
appearance_co_players links are then built from those groups.
"""
import json
import os
import sqlite3
import sys

SLUG = "2026-topps-flagship-football"
SET_NAME = "2026 Topps Flagship Football"
SPORT = "Football"
SEASON = "2026"
LEAGUE = "NFL"
TIER = "Standard"
RELEASE_DATE = "2026-08-21"
CREATED_AT = "2026-08-24T00:00:00Z"

BOX_CONFIG = {
    "hobby": {
        "cards_per_pack": 12, "packs_per_box": 20, "boxes_per_case": None,
        "autos_or_relics_per_box": 1,
        "notes": "1 autograph or relic card per box",
    },
    "jumbo": {
        "cards_per_pack": 40, "packs_per_box": 10, "boxes_per_case": 6,
        "autos_per_box": 1, "relics_per_box": 1,
        "notes": "1 autograph and 1 relic card per box",
    },
    "value": {
        "cards_per_pack": 12, "packs_per_box": 6, "boxes_per_case": None,
        "price_usd": 24.99,
        "note": "'Look for autograph and relic cards' is marketing, not a guarantee; hits stored NULL",
    },
    "mega": {
        "cards_per_pack": 15, "packs_per_box": 12, "boxes_per_case": 20,
        "price_usd": 49.99,
        "note": "Education sheet listed 14 cards / 14 packs; topps.com product page (15 cards / 12 packs) wins",
    },
}

EXPECTED_SUBSET_COUNTS = {
    "Base Cards I": 260, "Future Stars": 10, "Team Cards": 10, "League Leaders": 10,
    "Combo Cards": 10, "Rookies": 100, "Golden Mirror Image Variations": 260,
    "Future Stars Golden Mirror Image Variations": 10,
    "Team Cards Golden Mirror Image Variations": 10,
    "League Leaders Golden Mirror Image Variations": 10,
    "Combo Cards Golden Mirror Image Variations": 10,
    "Golden Mirror Rookie Image Variations": 100,
    "Base Cards Vintage Stock Variation": 100, "Rookie Card Vintage Stock Variation": 100,
    "Base Cards Clear Variation": 100, "Rookie Card Clear Variation": 100,
    "Base Cards Team Color Border Variations": 100, "Rookie Card Team Color Border Variation": 100,
    "Base Cards Player Number Variations": 100, "Rookie Card Player Number Variations": 100,
    "Base Cards True Photo Variations": 100, "Rookie Card True Photo Variation": 100,
    "2025 All Topps Team": 20, "Ring of Honor": 5, "Topps Profiles": 25,
    "Big Ticket Players": 25, "2025 Greatest Hits": 25, "Class of 26": 5,
    "Touchdown Machines": 52, "1000 Yard Club": 37, "4000 Yard Club": 6,
    "Wild Card Moments": 35, "Divisional Dominance": 25, "Conference Kings": 20,
    "All Hail the Champ": 20, "Struttin": 30, "Billboard Material": 30, "Touchdown": 40,
    "1991 Topps Football": 50, "1991 Topps Rookies Football": 50, "NFL Stars": 40,
    "Pressure Cookers": 30, "Greats of the Game": 30, "All Kings": 30,
    "1991 Topps Football Chrome Base Cards": 50,
    "1991 Topps Rookies Football Chrome Base Cards": 50, "1957 Rookie Variation": 50,
    "Fanatics Authentic Redemptions Cards": 32, "Super Box Oversized Base Card": 16,
    "Companion Cards": 25, "Funko Base Cards": 10, "The Flagship Collection": 90,
    "Big Time Players": 10, "The Flagship Collection Chrome": 90, "Highlight Reels": 10,
    "Club Exclusive Oversized Card": 16, "Flagship First Signatures": 38,
    "Flagship First Dual Signatures": 10, "NFL Stars Autographs": 67,
    "NFL Stars Dual Autographs": 27, "NFL Stars Triple Autographs": 26,
    "1991 Topps Football Autograph Cards": 97,
    "1991 Topps Football Rookie Autograph Cards": 46, "Victory Ink": 36,
    "Mascot Autographs": 3, "Island Ink": 19, "Real One Autographs": 134,
    "Rookie Real One Autographs": 77, "2025 All Topps Team Autographs": 15,
    "1991 Super Rookies Autographs": 11, "Super Bowl Champion Signatures": 48,
    "Ring of Honor Signatures": 4, "Rookie Premiere Autographs": 40,
    "NFL Material Cards": 48, "NFL Rookies Material Cards": 40,
    "NFL Material Dual Relic Cards": 34, "Field Fit Swatch Collection": 41,
    "1991 Topps Football Relics": 26, "1991 Topps Football Rookie Relics": 40,
    "Real One Relics": 32, "Rookie Real One Relics": 42,
    "NFL Material Autograph Cards": 22, "NFL Rookie Material Autograph Cards": 39,
    "NFL Material Dual Relic Autographs": 9,
    "Field Fit Swatch Collection Autograph Relic": 27,
    "Topps Autograph Patch Cards": 25, "Topps Autograph Rookie Patch Cards": 40,
}

EXPECTED = {
    "total_cards": 4042, "total_subsets": 87, "co_player_rows": 129,
    "rookie_cards": 1281, "character_cards": 43,
    "is_base": 17, "is_autograph": 23, "is_relic": 14, "is_booklet": 0,
}


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: seed_flagship_football_2026.py <data_dir>")
    data_dir = sys.argv[1]
    db_path = os.path.join(os.getcwd(), "the-c-list.db")

    with open(os.path.join(data_dir, "subsets.json")) as f:
        subsets = json.load(f)
    cards = []
    with open(os.path.join(data_dir, "cards.jsonl")) as f:
        for ln in f:
            ln = ln.strip()
            if ln:
                cards.append(json.loads(ln))

    print(f"Loaded {len(subsets)} subsets, {len(cards)} card lines from {data_dir}")

    con = sqlite3.connect(db_path)
    con.execute("PRAGMA foreign_keys = OFF")
    cur = con.cursor()

    # ── PREFLIGHT ────────────────────────────────────────────────────────────
    row = cur.execute(
        "SELECT id FROM sets WHERE slug=? OR (name=? AND season=?)",
        (SLUG, SET_NAME, SEASON),
    ).fetchone()
    if row:
        con.close()
        sys.exit(f"PREFLIGHT STOP: set already exists (id={row[0]}). Refusing to modify.")

    # ── SET ──────────────────────────────────────────────────────────────────
    cur.execute(
        """INSERT INTO sets (name, sport, season, league, tier, box_config,
                             release_date, slug, is_visible, created_at)
           VALUES (?,?,?,?,?,?,?,?,1,?)""",
        (SET_NAME, SPORT, SEASON, LEAGUE, TIER, json.dumps(BOX_CONFIG),
         RELEASE_DATE, SLUG, CREATED_AT),
    )
    set_id = cur.lastrowid
    print(f"Created set id={set_id}")

    # ── SUBSETS ──────────────────────────────────────────────────────────────
    subset_id = {}
    for s in sorted(subsets, key=lambda x: x["display_order"]):
        cur.execute(
            """INSERT INTO insert_sets (set_id, name, is_autograph, is_base, is_relic, is_booklet)
               VALUES (?,?,?,?,?,?)""",
            (set_id, s["name"], s["is_autograph_subset"], s["is_base"],
             s["is_relic"], s["is_booklet"]),
        )
        subset_id[s["name"]] = cur.lastrowid

    # ── PLAYERS (distinct names; subject_role from character cards) ───────────
    character_names = set()
    all_names = set()
    for c in cards:
        all_names.add(c["name"])
        if c.get("subject_role") == "character":
            character_names.add(c["name"])
        for cp in c.get("co_players", []):
            all_names.add(cp["name"])

    player_id = {}
    for name in sorted(all_names):
        role = "character" if name in character_names else "athlete"
        cur.execute(
            """INSERT INTO players (set_id, name, unique_cards, total_print_run,
                                    one_of_ones, insert_set_count, subject_role)
               VALUES (?,?,0,0,0,0,?)""",
            (set_id, name, role),
        )
        player_id[name] = cur.lastrowid

    # ── APPEARANCES (primary + co_player rows sharing card_number) ───────────
    for c in cards:
        sid = subset_id[c["subset"]]
        rookie = 1 if c.get("is_rookie") else 0
        cur.execute(
            """INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team)
               VALUES (?,?,?,?,?)""",
            (player_id[c["name"]], sid, c["card_number"], rookie, c.get("team")),
        )
        for cp in c.get("co_players", []):
            cur.execute(
                """INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team)
                   VALUES (?,?,?,?,?)""",
                (player_id[cp["name"]], sid, c["card_number"], rookie, cp.get("team")),
            )

    # ── CO-PLAYER LINKS (mirror buildCoPlayerLinks: directed pairs) ──────────
    groups = {}
    for aid, isid, cn, pid in cur.execute(
        """SELECT pa.id, pa.insert_set_id, pa.card_number, pa.player_id
           FROM player_appearances pa
           JOIN insert_sets i ON pa.insert_set_id = i.id
           WHERE i.set_id=?""", (set_id,)).fetchall():
        groups.setdefault((isid, cn), []).append((aid, pid))
    link_count = 0
    for members in groups.values():
        if len(members) < 2:
            continue
        for aid, _ in members:
            for oid, opid in members:
                if oid == aid:
                    continue
                cur.execute(
                    "INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?,?)",
                    (aid, opid))
                link_count += 1

    # ── PLAYER STATS (unique_cards = appearance count; insert_set_count) ──────
    for name, pid in player_id.items():
        cur.execute(
            """UPDATE players SET
                 unique_cards = (SELECT COUNT(*) FROM player_appearances WHERE player_id=?),
                 insert_set_count = (SELECT COUNT(DISTINCT insert_set_id) FROM player_appearances WHERE player_id=?)
               WHERE id=?""", (pid, pid, pid))

    con.commit()

    # ── GATES ────────────────────────────────────────────────────────────────
    print("\n===== INTEGRITY GATES =====")
    ok = True

    def check(label, got, exp):
        nonlocal ok
        status = "PASS" if got == exp else "FAIL"
        if got != exp:
            ok = False
        print(f"  [{status}] {label}: {got} (expected {exp})")

    total_cards = cur.execute(
        """SELECT COUNT(*) FROM (SELECT DISTINCT insert_set_id, card_number
             FROM player_appearances pa JOIN insert_sets i ON pa.insert_set_id=i.id
             WHERE i.set_id=?)""", (set_id,)).fetchone()[0]
    total_appearances = cur.execute(
        """SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i
           ON pa.insert_set_id=i.id WHERE i.set_id=?""", (set_id,)).fetchone()[0]
    total_subsets = cur.execute(
        "SELECT COUNT(*) FROM insert_sets WHERE set_id=?", (set_id,)).fetchone()[0]
    rookie_cards = cur.execute(
        """SELECT COUNT(*) FROM (SELECT DISTINCT insert_set_id, card_number
             FROM player_appearances pa JOIN insert_sets i ON pa.insert_set_id=i.id
             WHERE i.set_id=? AND pa.is_rookie=1)""", (set_id,)).fetchone()[0]
    character_cards = cur.execute(
        """SELECT COUNT(*) FROM player_appearances pa
           JOIN insert_sets i ON pa.insert_set_id=i.id
           JOIN players p ON pa.player_id=p.id
           WHERE i.set_id=? AND p.subject_role='character'""", (set_id,)).fetchone()[0]
    b = cur.execute("SELECT COALESCE(SUM(is_base),0), COALESCE(SUM(is_autograph),0), COALESCE(SUM(is_relic),0), COALESCE(SUM(is_booklet),0) FROM insert_sets WHERE set_id=?", (set_id,)).fetchone()

    check("Total cards", total_cards, EXPECTED["total_cards"])
    check("Total subsets", total_subsets, EXPECTED["total_subsets"])
    check("Co-player rows (appearances - cards)", total_appearances - total_cards, EXPECTED["co_player_rows"])
    check("appearance_co_players link rows", link_count, link_count)  # informational
    check("Rookie-flagged cards", rookie_cards, EXPECTED["rookie_cards"])
    check("subject_role=character cards", character_cards, EXPECTED["character_cards"])
    check("is_base subsets", b[0], EXPECTED["is_base"])
    check("is_autograph subsets", b[1], EXPECTED["is_autograph"])
    check("is_relic subsets", b[2], EXPECTED["is_relic"])
    check("is_booklet subsets", b[3], EXPECTED["is_booklet"])

    # per-subset distinct-card counts
    print("\n  Per-subset card counts:")
    per = dict(cur.execute(
        """SELECT i.name, COUNT(DISTINCT pa.card_number)
           FROM insert_sets i LEFT JOIN player_appearances pa ON pa.insert_set_id=i.id
           WHERE i.set_id=? GROUP BY i.name""", (set_id,)).fetchall())
    bad = 0
    for name, exp in EXPECTED_SUBSET_COUNTS.items():
        got = per.get(name, 0)
        if got != exp:
            bad += 1
            ok = False
            print(f"    [FAIL] {name}: {got} (expected {exp})")
    print(f"    {len(EXPECTED_SUBSET_COUNTS) - bad}/{len(EXPECTED_SUBSET_COUNTS)} subset counts match")

    # spot checks
    print("\n  Spot checks:")
    def spot(label, sql, params, exp):
        nonlocal ok
        got = cur.execute(sql, params).fetchone()
        got = got[0] if got else None
        status = "PASS" if got == exp else "FAIL"
        if got != exp:
            ok = False
        print(f"    [{status}] {label}: {got!r} (expected {exp!r})")

    q = """SELECT pa.team FROM player_appearances pa JOIN insert_sets i ON pa.insert_set_id=i.id
           JOIN players p ON pa.player_id=p.id
           WHERE i.set_id=? AND i.name=? AND pa.card_number=? AND p.name=?"""
    spot("Base Cards I #246 team", q, (set_id, "Base Cards I", "246", "Wan'Dale Robinson"), "New York Giants")
    spot("GMIV #246 team", q, (set_id, "Golden Mirror Image Variations", "246", "Wan'Dale Robinson"), "Tennessee Titans")
    spot("Team Cards #271 name",
         """SELECT p.name FROM player_appearances pa JOIN insert_sets i ON pa.insert_set_id=i.id
            JOIN players p ON pa.player_id=p.id WHERE i.set_id=? AND i.name='Team Cards' AND pa.card_number='271'""",
         (set_id,), "Chicago Bears")
    spot("Team Cards #271 role",
         """SELECT p.subject_role FROM player_appearances pa JOIN insert_sets i ON pa.insert_set_id=i.id
            JOIN players p ON pa.player_id=p.id WHERE i.set_id=? AND i.name='Team Cards' AND pa.card_number='271'""",
         (set_id,), "character")
    spot("FAR-5 name",
         """SELECT p.name FROM player_appearances pa JOIN insert_sets i ON pa.insert_set_id=i.id
            JOIN players p ON pa.player_id=p.id WHERE i.set_id=? AND i.name='Fanatics Authentic Redemptions Cards' AND pa.card_number='FAR-5'""",
         (set_id,), "Tetairoa McMillan")
    # League Leaders #284 co-players
    ll = cur.execute(
        """SELECT p.name, pa.team FROM player_appearances pa JOIN insert_sets i ON pa.insert_set_id=i.id
           JOIN players p ON pa.player_id=p.id
           WHERE i.set_id=? AND i.name='League Leaders' AND pa.card_number='284' ORDER BY pa.id""",
        (set_id,)).fetchall()
    print(f"    League Leaders #284 subjects: {ll}")

    # no dup card_number within subset
    dups = cur.execute(
        """SELECT i.name, pa.card_number, COUNT(*) c FROM player_appearances pa
           JOIN insert_sets i ON pa.insert_set_id=i.id
           JOIN players p ON pa.player_id=p.id
           WHERE i.set_id=?
           GROUP BY i.id, pa.card_number, pa.player_id HAVING COUNT(*)>1""",
        (set_id,)).fetchall()
    check("Duplicate (subset,card,player) rows", len(dups), 0)

    # zero parallels / odds
    npar = cur.execute(
        "SELECT COUNT(*) FROM parallels par JOIN insert_sets i ON par.insert_set_id=i.id WHERE i.set_id=?",
        (set_id,)).fetchone()[0]
    check("Parallels for set", npar, 0)
    pack_odds = cur.execute("SELECT pack_odds FROM sets WHERE id=?", (set_id,)).fetchone()[0]
    check("pack_odds is NULL", pack_odds is None, True)

    print("\n===== " + ("ALL GATES PASS" if ok else "GATES FAILED") + " =====")
    con.close()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
