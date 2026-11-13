"""
Seed: 2026 Topps Museum Collection Baseball — 1,317 cards across 34 subsets,
hobby-only odds + 150 numbered parallels.

Sources:
  scratchpad/mus.jsonl     — 1,317 card rows: subset, card_number, subject, team,
                             optional rookie, optional co_players:[{subject,team}].
  scratchpad/musodds.jsonl — 180 odds lines: 30 subset-level (parallel=null) + 150
                             parallel lines, each carrying hobby odds, print_run, note?.

Rulings applied (Phase 0 report + go, 2026-11-13):
  - Precedent = set 42 (2025 Topps Museum Collection Baseball): tier Premium, MLB.
    Box-config autograph-relic slot key = `autograph_relics_per_box` (set 42 form).
  - box_config hobby only, per ruling (NO base_parallels/base_cards keys):
    {cards_per_pack 8, packs_per_box 1, boxes_per_case 8, autographs_per_box 1,
     autograph_relics_per_box 1, memorabilia_per_box 1}.
  - Subset renames to the 2025 stored forms (applied to cards AND odds):
      Dual On-Card Autographs -> Dual On Card Autographs
      Showpieces              -> Showpieces Autographs
      Framed Hall of Fame Autographs -> Framed HOF Autographs
      Momentous Material Dual Jumbo Patch Autograph Book -> ... Book Cards
    The three 2026 "Relic" names are KEPT (Museum Framed Autograph Relics,
    Museum Framed Dual Autograph Relic Book, Dual Autographed Jumbo Lumber Bat
    Relic Book) — official-sheet/card-file names, not the 2025 "Patch" forms.
  - Manny fold: file carries both 'Manny Ramírez' (Meaningful Material Relics) and
    'Manny Ramirez' (four subsets). DB stores the UNACCENTED 'Manny Ramirez' (9
    existing Baseball appearances) -> fold both to 'Manny Ramirez'. 354 strings -1 = 353.
  - Caglianone dual MMDPA-WC stays UNFLAGGED (no rookie propagation): 142 rookie rows.
  - Sketch subsets (4, odds-only, 0 cards) and the two 1/1 subsets (Canvas Collection
    Original Player Autographs, Jumbo Lumber Bat Nameplate Relics) store print_run=1;
    sketch flags all 0 (not autographs). All other subsets print_run NULL.
  - Exclusivity: none (single format). Parallel print_run/note carried from the sheet
    ("or less" on hit parallels; MMJR Sapphire = NULL + "#'d" note).

Data model: one player_appearances row PER PERSON PER CARD (duals -> 2 rows, triples
-> 3 rows sharing card_number); co-player links are built by grouping on
(insert_set_id, card_number) into N*(N-1) bidirectional rows (mirrors seed.ts
buildCoPlayerLinks). So raw appearance rows = 1,439 while distinct
(insert_set_id, card_number) = 1,317 and co-links = 264.

Run post-seed.ts after this, then migrate-to-turso.ts --set 2026-topps-museum-collection-baseball.
Usage: python3 scripts/seed_museum_collection_baseball_2026.py
"""
import sqlite3, os, json, re, unicodedata

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
JSONL = os.path.join(os.path.dirname(__file__), "..", "scratchpad", "mus.jsonl")
ODDS = os.path.join(os.path.dirname(__file__), "..", "scratchpad", "musodds.jsonl")

SET_NAME = "2026 Topps Museum Collection Baseball"
SET_SLUG = "2026-topps-museum-collection-baseball"
TOPPS_URL = "https://www.topps.com/pages/topps-museum-collection-baseball"

SUBSET_RENAME = {
    "Dual On-Card Autographs": "Dual On Card Autographs",
    "Showpieces": "Showpieces Autographs",
    "Framed Hall of Fame Autographs": "Framed HOF Autographs",
    "Momentous Material Dual Jumbo Patch Autograph Book":
        "Momentous Material Dual Jumbo Patch Autograph Book Cards",
}

# in-file spelling-twin fold: accented sheet form -> DB's unaccented canonical
NAME_FIX = {"Manny Ramírez": "Manny Ramirez"}

# ── subset-flag classification (post-rename names) ──
BASE_SUBSETS = {"Base"}
AUTOGRAPH_SUBSETS = {
    "Canvas Collection Original Player Autographs", "Archival Autographs",
    "Retrospective Signatures", "Atelier Autographed Book Cards",
    "Showpieces Autographs", "Pastime Portraits", "Dual On Card Autographs",
    "Museum Framed Autographs", "Framed HOF Autographs",
    "Museum Framed Autograph Relics", "Autographed Jumbo Lumber Bat Relics",
    "Lifetime Members Relic Autographs", "Written in History Relic Autographs",
    "Museum Framed Dual Autograph Relic Book",
    "Dual Autographed Jumbo Lumber Bat Relic Book",
    "Momentous Material Jumbo Patch Autographs",
    "Momentous Material Dual Jumbo Patch Autograph Book Cards",
    "Single Player Signature Swatches Dual Relic Autographs",
    "Single Player Signature Swatches Triple Relic Autographs",
    "Dual Player Signature Swatches Dual Relic Autographs",
}
RELIC_SUBSETS = {
    "Museum Framed Autograph Relics", "Autographed Jumbo Lumber Bat Relics",
    "Lifetime Members Relic Autographs", "Written in History Relic Autographs",
    "Museum Framed Dual Autograph Relic Book",
    "Dual Autographed Jumbo Lumber Bat Relic Book",
    "Momentous Material Jumbo Patch Autographs",
    "Momentous Material Dual Jumbo Patch Autograph Book Cards",
    "Single Player Signature Swatches Dual Relic Autographs",
    "Single Player Signature Swatches Triple Relic Autographs",
    "Dual Player Signature Swatches Dual Relic Autographs",
    "Meaningful Material Relics", "Momentous Material Jumbo Relics",
    "Museum Memorabilia I", "Museum Memorabilia II",
    "Jumbo Lumber Bat Nameplate Relics",
    "Single Player Primary Pieces Triple Relics",
    "Three Player Primary Pieces Triple Relics",
    "Dual Player Primary Pieces Dual Relics",
    "Single Player Primary Pieces Dual Relics Legends",
}
BOOKLET_SUBSETS = {
    "Atelier Autographed Book Cards", "Museum Framed Dual Autograph Relic Book",
    "Dual Autographed Jumbo Lumber Bat Relic Book",
    "Momentous Material Dual Jumbo Patch Autograph Book Cards",
}
SKETCH_SUBSETS = [
    "Canvas Collection Originals", "Canvas Collection Originals Iconic Sketches",
    "Canvas Collection Museum Murals", "Faces of Greatness",
]
PRINT_RUN_1 = {
    "Canvas Collection Original Player Autographs", "Jumbo Lumber Bat Nameplate Relics",
    *SKETCH_SUBSETS,
}


def ren(sub):
    return SUBSET_RENAME.get(sub, sub)


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
    assert len(rows) == 1317, f"expected 1317 card rows, got {len(rows)}"
    odds = [json.loads(l) for l in open(ODDS) if l.strip()]
    assert len(odds) == 180, f"expected 180 odds rows, got {len(odds)}"

    # ── derive pack_odds + parallel rows from the odds file (post-rename) ──
    hobby_odds = {}            # pack_odds key -> int denominator
    parallel_rows = []         # (subset, parallel, print_run, note)
    subset_notes = {}          # subset -> note (none expected)
    for o in odds:
        sub = ren(o["subset"])
        par = o.get("parallel")
        hob = (o.get("odds") or {}).get("hobby")
        if par is None:
            key = sub
            if o.get("note"):
                subset_notes[sub] = o["note"]
        else:
            parallel_rows.append((sub, par, o.get("print_run"), o.get("note")))
            key = f"{sub} {par}"
        assert hob, f"odds line missing hobby figure: {o}"
        assert key not in hobby_odds, f"duplicate pack_odds key: {key!r}"
        hobby_odds[key] = to_denom(hob)
    assert len(parallel_rows) == 150, f"expected 150 parallels, got {len(parallel_rows)}"
    assert len(hobby_odds) == 180, f"expected 180 pack_odds keys, got {len(hobby_odds)}"

    box_config = json.dumps({
        "hobby": {
            "cards_per_pack": 8, "packs_per_box": 1, "boxes_per_case": 8,
            "autographs_per_box": 1, "autograph_relics_per_box": 1,
            "memorabilia_per_box": 1,
        },
    })
    pack_odds = json.dumps({"hobby": hobby_odds})

    # ── ordered subset list: card first-appearance order, then odds-only sketches ──
    subset_order = []
    seen = set()
    for r in rows:
        sub = ren(r["subset"])
        if sub not in seen:
            seen.add(sub); subset_order.append(sub)
    for o in odds:
        sub = ren(o["subset"])
        if sub not in seen:
            seen.add(sub); subset_order.append(sub)
    assert len(subset_order) == 34, f"expected 34 subsets, got {len(subset_order)}"

    db = sqlite3.connect(DB_PATH)
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA foreign_keys=ON")
    if db.execute("SELECT id FROM sets WHERE name = ?", (SET_NAME,)).fetchone():
        raise SystemExit(f"Set '{SET_NAME}' already exists — aborting.")

    try:
        cur = db.execute(
            """INSERT INTO sets (name, sport, season, league, tier, slug, is_visible,
                   sample_image_url, release_date, box_config, pack_odds, topps_url, created_at)
               VALUES (?, 'Baseball', '2026', 'MLB', 'Premium', ?, 1, ?, ?, ?, ?, ?, ?)""",
            (SET_NAME, SET_SLUG, f"/sets/{SET_SLUG}.jpg", "2026-11-11", box_config,
             pack_odds, TOPPS_URL, "2026-11-13T12:00:00Z"),
        )
        set_id = cur.lastrowid
        print(f"Created set id {set_id}")

        # ── insert_sets (all 34) ──
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
                 1 if sub in PRINT_RUN_1 else None,
                 subset_notes.get(sub)),
            ).lastrowid
        print(f"Created {len(is_ids)} subsets")

        for sub, par, _, _ in parallel_rows:
            assert sub in is_ids, f"parallel subset not in checklist: {sub!r}"

        # ── players (canon fold), role athlete ──
        slug_cache = {}

        def goc(name):
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
                   VALUES (?, ?, ?, 0, 0, 0, 0, 'athlete')""",
                (set_id, name, c),
            ).lastrowid

        # ── parallels ──
        for sub, par, pr, note in parallel_rows:
            db.execute(
                """INSERT INTO parallels (insert_set_id, name, print_run, exclusivity, note)
                   VALUES (?, ?, ?, NULL, ?)""",
                (is_ids[sub], par, pr, note))

        # ── appearances: one per PERSON per card (primary + each co-player) ──
        for r in rows:
            sub = ren(r["subset"])
            card = str(r["card_number"])
            isid = is_ids[sub]
            # primary
            db.execute(
                """INSERT INTO player_appearances
                       (player_id, insert_set_id, card_number, is_rookie, team, subset_tag)
                   VALUES (?, ?, ?, ?, ?, NULL)""",
                (goc(r["subject"]), isid, card, 1 if r.get("rookie") else 0, r.get("team")))
            # co-players (never rookie-flagged; no propagation)
            for cp in (r.get("co_players") or []):
                db.execute(
                    """INSERT INTO player_appearances
                           (player_id, insert_set_id, card_number, is_rookie, team, subset_tag)
                       VALUES (?, ?, ?, 0, ?, NULL)""",
                    (goc(cp["subject"]), isid, card, cp.get("team")))

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
            # link each appearance to every OTHER appearance's player (bidirectional)
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
        n_pr1 = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND print_run IS NOT NULL", set_id)
        n_cards = q1("""SELECT COUNT(DISTINCT pa.insert_set_id || ':' || pa.card_number)
                        FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                        WHERE i.set_id=?""", set_id)
        n_app = q1("""SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                      WHERE i.set_id=?""", set_id)
        n_players = q1("SELECT COUNT(*) FROM players WHERE set_id=?", set_id)
        n_rookie = q1("""SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                         WHERE i.set_id=? AND pa.is_rookie=1""", set_id)
        n_par = q1("""SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id
                      WHERE i.set_id=?""", set_id)
        n_par_null = q1("""SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id
                           WHERE i.set_id=? AND p.print_run IS NULL""", set_id)
        n_oddskeys = len(json.loads(q1("SELECT pack_odds FROM sets WHERE id=?", set_id))["hobby"])
        manny_bad = q1("SELECT COUNT(*) FROM players WHERE set_id=? AND name='Manny Ramírez'", set_id)
        manny_ok = q1("SELECT COUNT(*) FROM players WHERE set_id=? AND name='Manny Ramirez'", set_id)
        oh_team = q1("""SELECT COUNT(*) FROM player_appearances pa JOIN players p ON p.id=pa.player_id
                        WHERE p.set_id=? AND p.name='Sadaharu Oh' AND pa.team IS NOT NULL""", set_id)
        mmjr_sapphire_pr = db.execute(
            """SELECT p.print_run FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id
               WHERE i.set_id=? AND i.name='Momentous Material Jumbo Relics' AND p.name='Sapphire'""",
            (set_id,)).fetchone()[0]

        po = json.loads(pack_odds)["hobby"]
        print(f"subsets={n_sub} (base={n_base} auto={n_auto} relic={n_relic} both={n_both} booklet={n_bk})")
        print(f"print_run=1 subsets={n_pr1}  distinct_cards={n_cards}  appearance_rows={n_app}")
        print(f"players={n_players}  rookie_appearances={n_rookie}  co_links={colink}")
        print(f"parallels={n_par} (null print_run={n_par_null})  pack_odds_hobby_keys={n_oddskeys}")
        print(f"Manny fold: accented={manny_bad} (want 0)  unaccented={manny_ok} (want 1)")
        print(f"Sadaharu Oh non-null teams={oh_team} (want 0)  MMJR Sapphire print_run={mmjr_sapphire_pr} (want None)")

        assert (n_sub, n_base, n_auto, n_relic, n_both, n_bk) == (34, 1, 20, 20, 11, 4), "subset-flag gate failed"
        assert n_pr1 == 6, "print_run=1 subset gate failed (expected 6)"
        assert n_cards == 1317, "distinct-card gate failed (expected 1317)"
        assert n_app == 1439, "appearance-row gate failed (1205 + 102*2 + 10*3 = 1439)"
        assert n_rookie == 142, "rookie gate failed (expected 142)"
        assert n_players == 353, "player gate failed (354 strings - 1 Manny fold = 353)"
        assert colink == 264, "co-player link gate failed (102*2 + 10*6 = 264)"
        assert n_par == 150 and n_par_null == 1, "parallel gate failed (150 total, 1 null print_run)"
        assert mmjr_sapphire_pr is None, "MMJR Sapphire should have NULL print_run"
        assert n_oddskeys == 180, "pack_odds gate failed (180 hobby keys)"
        # spot-checks (post-rename keys)
        assert po["Base Emerald"] == 456, "spot-check Base Emerald 1:456 failed"
        assert po["Base Printing Plates"] == 114, "spot-check Base Printing Plates 1:114 failed"
        assert po["Framed HOF Autographs Wood Frame"] == 22210, "spot-check Framed HOF Wood Frame 1:22210 failed"
        assert po["Museum Memorabilia II Laundry Tag"] == 245, "spot-check Museum Memorabilia II Laundry Tag 1:245 failed"
        assert po["Faces of Greatness"] == 4376, "spot-check Faces of Greatness 1:4376 failed"
        assert manny_bad == 0 and manny_ok == 1, "Manny fold gate failed"
        assert oh_team == 0, "Sadaharu Oh should have NULL team on all rows"
        print("ALL LOCAL GATES PASSED.")
        print(f"DONE. set id {set_id}")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
