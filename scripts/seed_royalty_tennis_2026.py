"""
Seed: 2026 Topps Royalty Tennis — 1,048 cards across 28 subsets, hobby-only odds
+ 83 numbered parallels.

Sources:
  scratchpad/rt.jsonl     — 1,048 card rows: subset, card_number, subject, team(=null),
                            optional rookie, optional subject_role, optional
                            co_players:[{subject, team(=null), optional rookie}].
  scratchpad/rtodds.jsonl — 111 odds lines: 28 subset-level (parallel=null) + 83
                            parallel lines; each carries hobby odds (Sketch Cards has
                            none), print_run, note?.

Rulings applied (Phase 0 report + go, 2026-11-15):
  - Precedent = 911 Royalty UFC / 883 Royalty PL (tier Premium), 881/873/905 Tennis.
    League string for Tennis is "" (empty) — stored empty.
  - box_config hobby only, keys of 911/883: {cards_per_pack 10, packs_per_box 1,
    boxes_per_case 4, autos_per_box 6}. No memorabilia key (no relic guarantee).
    No human `notes` string (ruling 3).
  - related_links: two Ripped-by-Topps objects, approved shape of 885 (ruling 4).
  - Numbered-parent subsets (follow 911, ruling 2): Racket Knob Autographs, Racket
    Knob Relics, Welcome to the Club Dual Autographs stored as BARE print_run=1
    insert_sets with the subset odds key and NO note (the sheet's "Platinum 1/1"
    note is dropped); no Platinum parallel row (the file carries none).
  - /5 subsets: On-Court Shoe Relics and The Grip stored as print_run=5 with the
    subset key (the "Green /5" base) plus their explicit Platinum 1/1 parallel rows
    (Brand Logo / Tongue Logo Platinum; Platinum). Their "base version is Green /5"
    note is kept (ruling named only the three 1/1 subsets for note removal).
  - Prodigious Pairings Relics + Regalia Relics: subset + 4 parallels each have odds
    but NULL print_run, note "print run not published" (8 NULL-print_run parallels).
  - 3 name folds to stored accented canonical (ruling): Bjorn Borg -> Björn Borg,
    Iga Swiatek -> Iga Świątek, Karolina Muchova -> Karolína Muchová. No collapse
    (file carries only the unaccented form) -> players stay 226.
  - 5 rookies appear unflagged on multi-subject cards -> stay as printed (913 ruling);
    co-player is_rookie honored from the file (QA-KBSK quad carries 4 flags).
  - Sketch Cards: George Condo primary, subject_role 'sketch_artist', card_number
    "George Condo" (847 precedent), Novak Djokovic co-subject (athlete). No odds key;
    insert_set print_run 1.
  - Exclusivity: none (single hobby format).

Data model: one player_appearances row PER PERSON PER CARD (dual->2, triple->3,
quad->4 rows sharing card_number); co-player links built by grouping on
(insert_set_id, card_number) into N*(N-1) bidirectional rows (mirrors seed.ts
buildCoPlayerLinks). Distinct cards 1,048; appearance rows 1,147; links 278
(49*2 + 10*6 + 10*12).

Run post-seed.ts after this, then migrate-to-turso.ts --set 2026-topps-royalty-tennis.
Usage: python3 scripts/seed_royalty_tennis_2026.py
"""
import sqlite3, os, json, re, unicodedata

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
JSONL = os.path.join(os.path.dirname(__file__), "..", "scratchpad", "rt.jsonl")
ODDS = os.path.join(os.path.dirname(__file__), "..", "scratchpad", "rtodds.jsonl")

SET_NAME = "2026 Topps Royalty Tennis"
SET_SLUG = "2026-topps-royalty-tennis"
TOPPS_URL = "https://www.topps.com/pages/topps-royalty-tennis"

RELATED_LINKS = [
    {"url": "https://ripped.topps.com/topps-royalty-tennis-history",
     "source": "Ripped by Topps", "title": "Topps Royalty Tennis History",
     "description": "Topps's history of the Royalty Tennis line."},
    {"url": "https://ripped.topps.com/behind-the-design-racket-knob-autographs-2026-topps-royalty-tennis",
     "source": "Ripped by Topps", "title": "Behind the Design: Racket Knob Autographs",
     "description": "How the 1/1 Racket Knob Autographs were made."},
]

# in-file spelling folds: unaccented file form -> stored accented canonical
NAME_FIX = {
    "Bjorn Borg": "Björn Borg",
    "Iga Swiatek": "Iga Świątek",
    "Karolina Muchova": "Karolína Muchová",
}

# drop the sheet's "Platinum 1/1" note on the three numbered-parent subsets (ruling 2)
DROP_NOTE_SUBSETS = {
    "Racket Knob Autographs", "Racket Knob Relics",
    "Welcome to the Club Dual Autographs",
}

# ── subset-flag classification ──
BASE_SUBSETS = {"Base"}
AUTOGRAPH_SUBSETS = {
    "Imperial Ink", "Pursuit of Greatness Autographs", "Rookie Autographs",
    "Royal Decree Autographs", "Superior Signatures", "The Coronation Autographs",
    "The Time is Now Autographs", "Welcome to the Club Dual Autographs",
    "Dual Autographs", "Triple Autographs", "Quad Player Autograph Booklets",
    "Autograph Jumbo Relic Booklets", "Racket Knob Autographs",
    "Regalia Relic Signatures", "Rookie Relic Autographs",
    "Superior Relic Signatures", "Triumph Relic Signatures",
}
RELIC_SUBSETS = {
    "Autograph Jumbo Relic Booklets", "Racket Knob Autographs",
    "Regalia Relic Signatures", "Rookie Relic Autographs",
    "Superior Relic Signatures", "Triumph Relic Signatures",
    "On-Court Shoe Relics", "Prodigious Pairings Relics", "Racket Knob Relics",
    "Regalia Relics", "Relic Jewels", "Rookie Jumbo Relics", "Star Relics",
    "The Grip",
}
BOOKLET_SUBSETS = {
    "Quad Player Autograph Booklets", "Autograph Jumbo Relic Booklets",
}


def canon(name):
    name = unicodedata.normalize("NFC", name.strip())
    return NAME_FIX.get(name, name)


def slugify(t):
    s = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^\w\s-]", "", s.lower().strip())
    s = re.sub(r"[\s_]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")


def to_denom(s):
    return int(s.split(":", 1)[1])


def main():
    rows = [json.loads(l) for l in open(JSONL) if l.strip()]
    assert len(rows) == 1048, f"expected 1048 card rows, got {len(rows)}"
    odds = [json.loads(l) for l in open(ODDS) if l.strip()]
    assert len(odds) == 111, f"expected 111 odds rows, got {len(odds)}"

    # ── derive pack_odds + parallel rows + subset print_runs/notes ──
    hobby_odds = {}          # pack_odds key -> int denominator
    parallel_rows = []       # (subset, parallel, print_run, note)
    subset_pr = {}           # subset -> insert_set print_run (may be None)
    subset_note = {}         # subset -> insert_set note (may be None)
    for o in odds:
        sub = o["subset"]
        par = o.get("parallel")
        hob = (o.get("odds") or {}).get("hobby")
        if par is None:
            subset_pr[sub] = o.get("print_run")
            note = o.get("note")
            subset_note[sub] = None if sub in DROP_NOTE_SUBSETS else note
            if hob:
                key = sub
                assert key not in hobby_odds, f"duplicate pack_odds key: {key!r}"
                hobby_odds[key] = to_denom(hob)
        else:
            parallel_rows.append((sub, par, o.get("print_run"), o.get("note")))
            key = f"{sub} {par}"
            assert hob, f"parallel line missing hobby figure: {o}"
            assert key not in hobby_odds, f"duplicate pack_odds key: {key!r}"
            hobby_odds[key] = to_denom(hob)
    assert len(parallel_rows) == 83, f"expected 83 parallels, got {len(parallel_rows)}"
    assert len(hobby_odds) == 110, f"expected 110 pack_odds keys, got {len(hobby_odds)}"

    box_config = json.dumps({
        "hobby": {
            "cards_per_pack": 10, "packs_per_box": 1, "boxes_per_case": 4,
            "autos_per_box": 6,
        },
    })
    pack_odds = json.dumps({"hobby": hobby_odds})

    # ── ordered subset list: card first-appearance order (all 28 appear in cards) ──
    subset_order = []
    seen = set()
    for r in rows:
        sub = r["subset"]
        if sub not in seen:
            seen.add(sub); subset_order.append(sub)
    for o in odds:  # safety: any odds-only subset (none expected)
        sub = o["subset"]
        if sub not in seen:
            seen.add(sub); subset_order.append(sub)
    assert len(subset_order) == 28, f"expected 28 subsets, got {len(subset_order)}"

    db = sqlite3.connect(DB_PATH)
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA foreign_keys=ON")
    if db.execute("SELECT id FROM sets WHERE name = ?", (SET_NAME,)).fetchone():
        raise SystemExit(f"Set '{SET_NAME}' already exists — aborting.")

    try:
        cur = db.execute(
            """INSERT INTO sets (name, sport, season, league, tier, slug, is_visible,
                   sample_image_url, release_date, box_config, pack_odds, topps_url,
                   related_links, created_at)
               VALUES (?, 'Tennis', '2026', '', 'Premium', ?, 1, ?, ?, ?, ?, ?, ?, ?)""",
            (SET_NAME, SET_SLUG, f"/sets/{SET_SLUG}.jpg", "2026-11-13", box_config,
             pack_odds, TOPPS_URL, json.dumps(RELATED_LINKS), "2026-11-15T12:00:00Z"),
        )
        set_id = cur.lastrowid
        print(f"Created set id {set_id}")

        # ── insert_sets (all 28) ──
        is_ids = {}
        for sub in subset_order:
            is_ids[sub] = db.execute(
                """INSERT INTO insert_sets (set_id, name, is_base, is_autograph, is_relic,
                       is_booklet, print_run, notes)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (set_id, sub,
                 1 if sub in BASE_SUBSETS else 0,
                 1 if sub in AUTOGRAPH_SUBSETS else 0,
                 1 if sub in RELIC_SUBSETS else 0,
                 1 if sub in BOOKLET_SUBSETS else 0,
                 subset_pr.get(sub),
                 subset_note.get(sub)),
            ).lastrowid
        print(f"Created {len(is_ids)} subsets")

        for sub, par, _, _ in parallel_rows:
            assert sub in is_ids, f"parallel subset not in checklist: {sub!r}"

        # ── players (canon fold); role from the row, default athlete ──
        slug_cache = {}

        def goc(name, role="athlete"):
            name = canon(name)
            r = db.execute("SELECT id FROM players WHERE set_id=? AND name=?", (set_id, name)).fetchone()
            if r:
                return r[0]
            base = slugify(name) or "player"
            c, i = base, 2
            while c in slug_cache:
                c = f"{base}-{i}"; i += 1
            slug_cache[c] = True
            return db.execute(
                """INSERT INTO players (set_id, name, slug, unique_cards, total_print_run,
                       one_of_ones, insert_set_count, subject_role)
                   VALUES (?, ?, ?, 0, 0, 0, 0, ?)""",
                (set_id, name, c, role),
            ).lastrowid

        # ── parallels ──
        for sub, par, pr, note in parallel_rows:
            db.execute(
                """INSERT INTO parallels (insert_set_id, name, print_run, exclusivity, note)
                   VALUES (?, ?, ?, NULL, ?)""",
                (is_ids[sub], par, pr, note))

        # ── appearances: one per PERSON per card (primary + each co-player) ──
        for r in rows:
            sub = r["subset"]
            card = str(r["card_number"])
            isid = is_ids[sub]
            db.execute(
                """INSERT INTO player_appearances
                       (player_id, insert_set_id, card_number, is_rookie, team, subset_tag)
                   VALUES (?, ?, ?, ?, ?, NULL)""",
                (goc(r["subject"], r.get("subject_role") or "athlete"), isid, card,
                 1 if r.get("rookie") else 0, r.get("team")))
            for cp in (r.get("co_players") or []):
                db.execute(
                    """INSERT INTO player_appearances
                           (player_id, insert_set_id, card_number, is_rookie, team, subset_tag)
                       VALUES (?, ?, ?, ?, ?, NULL)""",
                    (goc(cp["subject"], cp.get("subject_role") or "athlete"), isid, card,
                     1 if cp.get("rookie") else 0, cp.get("team")))

        # ── co-player links: group by (insert_set_id, card_number), bidirectional ──
        groups = {}
        for aid, isid, card, pid in db.execute(
            """SELECT pa.id, pa.insert_set_id, pa.card_number, pa.player_id
               FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
               WHERE i.set_id=?""", (set_id,)):
            groups.setdefault((isid, card), []).append((aid, pid))
        colink = 0
        for members in groups.values():
            if len(members) < 2:
                continue
            for aid, _ in members:
                for oaid, opid in members:
                    if oaid == aid:
                        continue
                    db.execute(
                        "INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)",
                        (aid, opid))
                    colink += 1

        db.commit()

        # ── verification ──
        def q1(sql, *a):
            return db.execute(sql, a).fetchone()[0]

        n_sub = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=?", set_id)
        n_base = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_base=1", set_id)
        n_auto = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_autograph=1", set_id)
        n_relic = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_relic=1", set_id)
        n_both = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_autograph=1 AND is_relic=1", set_id)
        n_bk = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_booklet=1", set_id)
        n_prset = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND print_run IS NOT NULL", set_id)
        n_cards = q1("""SELECT COUNT(DISTINCT pa.insert_set_id || ':' || pa.card_number)
                        FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                        WHERE i.set_id=?""", set_id)
        n_app = q1("""SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                      WHERE i.set_id=?""", set_id)
        n_players = q1("SELECT COUNT(*) FROM players WHERE set_id=?", set_id)
        n_rookie = q1("""SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                         WHERE i.set_id=? AND pa.is_rookie=1""", set_id)
        n_sketch = q1("SELECT COUNT(*) FROM players WHERE set_id=? AND subject_role='sketch_artist'", set_id)
        n_par = q1("""SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id
                      WHERE i.set_id=?""", set_id)
        n_par_null = q1("""SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id
                           WHERE i.set_id=? AND p.print_run IS NULL""", set_id)
        n_oddskeys = len(json.loads(q1("SELECT pack_odds FROM sets WHERE id=?", set_id))["hobby"])
        condo_card = db.execute(
            """SELECT pa.card_number FROM player_appearances pa JOIN players p ON p.id=pa.player_id
               WHERE p.set_id=? AND p.name='George Condo'""", (set_id,)).fetchone()
        rkauto_pr = q1("SELECT print_run FROM insert_sets WHERE set_id=? AND name='Racket Knob Autographs'", set_id)
        rkauto_note = q1("SELECT notes FROM insert_sets WHERE set_id=? AND name='Racket Knob Autographs'", set_id)

        po = json.loads(pack_odds)["hobby"]
        print(f"subsets={n_sub} (base={n_base} auto={n_auto} relic={n_relic} both={n_both} booklet={n_bk})")
        print(f"print_run set on {n_prset} subsets  distinct_cards={n_cards}  appearance_rows={n_app}")
        print(f"players={n_players}  rookie_appearances={n_rookie}  co_links={colink}  sketch_artist={n_sketch}")
        print(f"parallels={n_par} (null print_run={n_par_null})  pack_odds_hobby_keys={n_oddskeys}")
        print(f"George Condo card_number={condo_card}  Racket Knob Auto print_run={rkauto_pr} note={rkauto_note!r}")

        assert (n_sub, n_base, n_auto, n_relic, n_both, n_bk) == (28, 1, 17, 14, 6, 2), "subset-flag gate failed"
        assert n_prset == 25, "subset print_run gate failed (expected 25 set)"
        assert n_cards == 1048, "distinct-card gate failed (expected 1048)"
        assert n_app == 1147, "appearance-row gate failed (expected 1147)"
        assert n_rookie == 157, "rookie gate failed (expected 157)"
        assert n_players == 226, "player gate failed (expected 226 after folds, no collapse)"
        assert colink == 278, "co-player link gate failed (49*2 + 10*6 + 10*12 = 278)"
        assert n_sketch == 1, "sketch_artist gate failed (expected 1 = George Condo)"
        assert n_par == 83 and n_par_null == 8, "parallel gate failed (83 total, 8 null)"
        assert n_oddskeys == 110, "pack_odds gate failed (110 hobby keys)"
        assert condo_card and condo_card[0] == "George Condo", "George Condo card_number gate failed"
        assert rkauto_pr == 1 and rkauto_note is None, "Racket Knob Auto must be bare print_run=1, no note"
        # spot-checks
        assert po["Base"] == 1, "spot-check Base 1:1 failed"
        assert po["Base Platinum"] == 115, "spot-check Base Platinum 1:115 failed"
        assert po["Racket Knob Autographs"] == 145, "spot-check Racket Knob Autographs 1:145 failed"
        assert po["Welcome to the Club Dual Autographs"] == 3823, "spot-check Welcome to the Club 1:3823 failed"
        assert po["On-Court Shoe Relics Tongue Logo Platinum"] == 244, "spot-check Tongue Logo Platinum 1:244 failed"
        assert po["Liquid Silver Liquid Gold"] == 5734, "spot-check Liquid Gold 1:5734 failed"
        print("ALL LOCAL GATES PASSED.")
        print(f"DONE. set id {set_id}")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
