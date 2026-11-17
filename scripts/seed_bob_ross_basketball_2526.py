"""
Seed: 2025-26 Topps x Bob Ross The Joy of Basketball — 245 cards across 8 subsets,
two box formats (Hobby Collector's Box + Happy Little Box) + 17 numbered parallels.

Sources:
  scratchpad/bob.jsonl     — 245 card rows: {subset, card_number, subject, team,
                             rookie?, subject_role?}. Single-person cards (no co-players).
  scratchpad/bobodds.jsonl — 23 odds lines: 6 subset-level (parallel=null) + 17
                             parallel lines; each carries odds {hobby?, happy_little_box?},
                             print_run, exclusivity?, note?.

Rulings applied (Phase 0 report + go, 2026-11-17):
  - Precedent = set 93 "2025 Topps x Bob Ross The Joy of Baseball" (tier Standard,
    skeleton — empty box_config/pack_odds, no subsets). Tier Standard adopted.
  - Box config, two formats: hobby (Hobby Collector's Box) 8 cards/pack, 8 packs/box,
    autos_per_box 1, boxes_per_case null; happy_little_box (Happy Little Box, NEW key)
    8 cards/pack, 1 pack/box, no hit guarantee. Notes per spec. "Happy Little Box"
    label added to boxLabels.ts; happy_little_box appended to ODDS_FORMAT_PREFERENCE.
  - is_base on Base and Beauty is Everywhere SP (image variation of base cards);
    Peapod the Squirrel SP is_base 0. is_autograph on Base Autographs only.
    No relics, booklets, co-players or subset print runs.
  - formats = ["hobby"] on the three Hobby-only subsets (Beauty is Everywhere SP,
    Peapod the Squirrel SP, Bob Ross Topps SSP = 31 appearances); others NULL.
  - Rookie: flag the 12 unflagged N-A autograph rookies (default yes). Implemented by
    propagating is_rookie to every appearance of any subject flagged rookie on any
    card (verified identical to the targeted flag: 39 printed + 12 = 51 rows, and no
    flagged subject has a non-autograph unflagged row).
  - Name folds to stored canonical (ruling): "Egor Dёmin" (Cyrillic ё U+0451) ->
    "Egor Dëmin" (Latin ë, athlete 374279, slug egor-demin); "Manu Ginobili" ->
    "Manu Ginóbili" (athlete 375129). Jokić / Dončić / Jakučionis already exact.
    Stray athlete 377859 (Cyrillic "Egor Dёmin", slug egor-d-min) left untouched.
    Blake Griffin and Bob Ross seed as new (Bob Ross subject_role celebrity).
  - Parallels: print_run 1 on the three Midnight Black rows; others NULL.
    exclusivity "Happy Little Box" on Base Easel only (from the file).
    note = the file's note verbatim where present (sticker / on-card autograph on the
    9 Base Autographs parallels); for the remaining NULL-print-run parallels with no
    file note (the 7 Base non-Midnight-Black parallels) -> "numbered, print run not
    published" per the spec's print-run paragraph; Base Midnight Black (1/1, no file
    note) -> NULL.

Data model: one player_appearances row per card (no co-players). Distinct cards 245;
appearance rows 245.

Run post-seed.ts then migrate-to-turso.ts --set 2025-26-topps-x-bob-ross-the-joy-of-basketball.
Usage: python3 scripts/seed_bob_ross_basketball_2526.py
"""
import sqlite3, os, json, re, unicodedata

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
JSONL = os.path.join(os.path.dirname(__file__), "..", "scratchpad", "bob.jsonl")
ODDS = os.path.join(os.path.dirname(__file__), "..", "scratchpad", "bobodds.jsonl")

SET_NAME = "2025-26 Topps x Bob Ross The Joy of Basketball"
SET_SLUG = "2025-26-topps-x-bob-ross-the-joy-of-basketball"
TOPPS_URL = "https://www.topps.com/pages/topps-x-bob-ross-the-joy-of-basketball"

# in-file spelling folds: file form -> stored accented canonical
NAME_FIX = {
    "Egor Dёmin": "Egor Dëmin",   # Cyrillic ё -> Latin ë (athlete 374279)
    "Manu Ginobili": "Manu Ginóbili",  # -> accented canonical (athlete 375129)
}

BASE_SUBSETS = {"Base", "Beauty is Everywhere SP"}
AUTOGRAPH_SUBSETS = {"Base Autographs"}
HOBBY_ONLY_SUBSETS = {
    "Beauty is Everywhere SP", "Peapod the Squirrel SP", "Bob Ross Topps SSP",
}

FORMATS = ("hobby", "happy_little_box")


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
    assert len(rows) == 245, f"expected 245 card rows, got {len(rows)}"
    odds = [json.loads(l) for l in open(ODDS) if l.strip()]
    assert len(odds) == 23, f"expected 23 odds rows, got {len(odds)}"

    # ── derive pack_odds (per format) + parallel rows ──
    fmt_odds = {f: {} for f in FORMATS}
    parallel_rows = []  # (subset, parallel, print_run, exclusivity, note)
    for o in odds:
        sub = o["subset"]
        par = o.get("parallel")
        od = o.get("odds") or {}
        key = sub if par is None else f"{sub} {par}"
        for f in FORMATS:
            v = od.get(f)
            if v:
                assert key not in fmt_odds[f], f"duplicate {f} key: {key!r}"
                fmt_odds[f][key] = to_denom(v)
        if par is not None:
            file_note = o.get("note")
            pr = o.get("print_run")
            note = file_note if file_note else (
                "numbered, print run not published" if pr is None else None)
            parallel_rows.append((sub, par, pr, o.get("exclusivity"), note))

    assert len(parallel_rows) == 17, f"expected 17 parallels, got {len(parallel_rows)}"
    assert (len(fmt_odds["hobby"]), len(fmt_odds["happy_little_box"])) == (22, 20), \
        f"pack_odds key counts {len(fmt_odds['hobby'])}/{len(fmt_odds['happy_little_box'])} != 22/20"

    box_config = json.dumps({
        "hobby": {
            "cards_per_pack": 8, "packs_per_box": 8, "boxes_per_case": None,
            "autos_per_box": 1,
            "notes": "4 numbered parallels, 2 inserts and 1 SP/SSP variation per box",
        },
        "happy_little_box": {
            "cards_per_pack": 8, "packs_per_box": 1, "boxes_per_case": None,
            "notes": "Inserts 1:2 packs, exclusive Easel parallel 1:4, numbered parallel 1:3, autographs 1:15",
        },
    })
    pack_odds = json.dumps({f: fmt_odds[f] for f in FORMATS})

    # ── ordered subset list: card first-appearance order ──
    subset_order, seen = [], set()
    for r in rows:
        sub = r["subset"]
        if sub not in seen:
            seen.add(sub); subset_order.append(sub)
    assert len(subset_order) == 8, f"expected 8 subsets, got {len(subset_order)}"

    # ── rookie propagation: flagged on any card -> flagged on all appearances ──
    rookie_subjects = {r["subject"] for r in rows if r.get("rookie")}

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
               VALUES (?, 'Basketball', '2025-26', 'NBA', 'Standard', ?, 1, ?, ?, ?, ?, ?, NULL, ?)""",
            (SET_NAME, SET_SLUG, f"/sets/{SET_SLUG}.jpg", "2026-11-16", box_config,
             pack_odds, TOPPS_URL, "2026-11-17T12:00:00Z"),
        )
        set_id = cur.lastrowid
        print(f"Created set id {set_id}")

        # ── insert_sets (all 8) ──
        is_ids = {}
        for sub in subset_order:
            is_ids[sub] = db.execute(
                """INSERT INTO insert_sets (set_id, name, is_base, is_autograph, is_relic,
                       is_booklet, print_run, notes)
                   VALUES (?, ?, ?, ?, 0, 0, NULL, NULL)""",
                (set_id, sub,
                 1 if sub in BASE_SUBSETS else 0,
                 1 if sub in AUTOGRAPH_SUBSETS else 0),
            ).lastrowid
        print(f"Created {len(is_ids)} subsets")

        for sub, par, _, _, _ in parallel_rows:
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
        for sub, par, pr, excl, note in parallel_rows:
            db.execute(
                """INSERT INTO parallels (insert_set_id, name, print_run, exclusivity, note)
                   VALUES (?, ?, ?, ?, ?)""",
                (is_ids[sub], par, pr, excl, note))

        # ── appearances: one per card; formats on Hobby-only subsets ──
        for r in rows:
            sub = r["subset"]
            fmt = json.dumps(["hobby"]) if sub in HOBBY_ONLY_SUBSETS else None
            rookie = 1 if (r.get("rookie") or r["subject"] in rookie_subjects) else 0
            db.execute(
                """INSERT INTO player_appearances
                       (player_id, insert_set_id, card_number, is_rookie, team, subset_tag, formats)
                   VALUES (?, ?, ?, ?, ?, NULL, ?)""",
                (goc(r["subject"], r.get("subject_role") or "athlete"), is_ids[sub],
                 str(r["card_number"]), rookie, r.get("team"), fmt))

        db.commit()

        # ── verification ──
        def q1(sql, *a):
            return db.execute(sql, a).fetchone()[0]

        n_sub = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=?", set_id)
        n_base = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_base=1", set_id)
        n_auto = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_autograph=1", set_id)
        n_relic = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_relic=1", set_id)
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
        n_celeb = q1("SELECT COUNT(*) FROM players WHERE set_id=? AND subject_role='celebrity'", set_id)
        n_fmt = q1("""SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                      WHERE i.set_id=? AND pa.formats IS NOT NULL""", set_id)
        n_par = q1("""SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id
                      WHERE i.set_id=?""", set_id)
        n_par_pr1 = q1("""SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id
                          WHERE i.set_id=? AND p.print_run=1""", set_id)
        n_par_null = q1("""SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id
                           WHERE i.set_id=? AND p.print_run IS NULL""", set_id)
        n_par_excl = q1("""SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id
                           WHERE i.set_id=? AND p.exclusivity IS NOT NULL""", set_id)
        po = json.loads(q1("SELECT pack_odds FROM sets WHERE id=?", set_id))
        kh, kb = len(po["hobby"]), len(po["happy_little_box"])
        bob = db.execute(
            """SELECT p.subject_role, p.slug FROM players p
               WHERE p.set_id=? AND p.name='Bob Ross'""", (set_id,)).fetchone()

        print(f"subsets={n_sub} (base={n_base} auto={n_auto} relic={n_relic} booklet={n_bk} print_run_set={n_prset})")
        print(f"distinct_cards={n_cards}  appearance_rows={n_app}  players={n_players}  celebrity={n_celeb}")
        print(f"rookie_appearances={n_rookie}  formats_set={n_fmt}")
        print(f"parallels={n_par} (print_run=1:{n_par_pr1} null:{n_par_null} exclusivity:{n_par_excl})")
        print(f"pack_odds keys: hobby={kh} happy_little_box={kb}")
        print(f"Bob Ross role={bob and bob[0]!r} slug={bob and bob[1]!r}")

        assert (n_sub, n_base, n_auto, n_relic, n_bk) == (8, 2, 1, 0, 0), "subset-flag gate failed"
        assert n_prset == 0, "no subset print_run expected"
        assert n_cards == 245 and n_app == 245, "card/appearance gate failed (245=245)"
        assert n_players == 106, "player gate failed (expected 106)"
        assert n_celeb == 1, "celebrity gate failed (expected 1 = Bob Ross)"
        assert n_rookie == 51, "rookie gate failed (expected 51 after flagging the 12 autographs)"
        assert n_fmt == 31, "formats gate failed (expected 31 Hobby-only appearances)"
        assert n_par == 17 and n_par_pr1 == 3 and n_par_null == 14 and n_par_excl == 1, \
            "parallel gate failed (17; pr1=3; null=14; excl=1)"
        assert (kh, kb) == (22, 20), "pack_odds key-count gate failed (22/20)"
        assert bob and bob[0] == "celebrity", "Bob Ross must be subject_role celebrity"
        # spot-checks
        assert po["happy_little_box"]["Base Easel"] == 4 and "Base Easel" not in po["hobby"], \
            "spot-check Base Easel hlb 1:4 / no hobby key failed"
        assert po["hobby"]["Base Midnight Black"] == 525 and po["happy_little_box"]["Base Midnight Black"] == 714, \
            "spot-check Base Midnight Black 1:525/1:714 failed"
        assert po["hobby"]["Bob Ross Topps SSP"] == 164, "spot-check Bob Ross Topps SSP hobby 1:164 failed"
        assert po["hobby"]["Base Autographs On-Card Midnight Black"] == 32000 and \
            po["happy_little_box"]["Base Autographs On-Card Midnight Black"] == 30000, \
            "spot-check On-Card Midnight Black 1:32000/1:30000 failed"
        assert po["hobby"]["Budding Talent"] == 6 and po["happy_little_box"]["Budding Talent"] == 4, \
            "spot-check Budding Talent 1:6/1:4 failed"
        # every pack_odds key resolves to a stored subset or subset + parallel
        valid = set(is_ids.keys())
        par_names = {p[1] for p in parallel_rows}
        for f in FORMATS:
            for key in po[f]:
                if key in valid:
                    continue
                ok = any(key == f"{s} {pn}" for s in valid for pn in par_names if key.startswith(s + " "))
                assert ok, f"unresolvable pack_odds key: {key!r}"
        print("ALL LOCAL GATES PASSED.")
        print(f"DONE. set id {set_id}")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
