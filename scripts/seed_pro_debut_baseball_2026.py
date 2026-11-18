"""
Seed: 2026 Topps Pro Debut Baseball — 977 cards across 16 subsets, one box format
(Hobby Jumbo) + 80 numbered parallels, 95 pack_odds keys.

Sources:
  scratchpad/pd.jsonl     — 977 card rows: {subset, card_number, subject, team,
                            co_players?:[{subject, team}]}. Duals/triples carry
                            co_players; one appearance per subject.
  scratchpad/pdodds.jsonl — 96 odds lines: 16 subset-level (parallel=null) + 80
                            parallel lines; each carries odds {hobby_jumbo},
                            print_run, note?.

Rulings applied (Phase 0 report + go, 2026-11-17):
  - Precedent: all 8 Pro Debut sets are empty shells (no subsets/box/odds). So no
    stored precedent for subset names, team casing, box key or Chrome is_base.
  - League "MiLB" for THIS set only (the 8 shell rows store "MLB", left untouched).
    Tier Standard (matches every Pro Debut row). Season "2026".
  - Box key hobby_jumbo (already in boxLabels.ts + ODDS_FORMAT_PREFERENCE): 24
    cards/pack, 6 packs/box, 8 boxes/case, 4 autos/box.
  - is_base on Base and Base Chrome (902 Chrome-is-base ruling). is_autograph on
    the 9 autograph subsets; is_relic on Jumbo Autograph Relic. No booklets.
    Subset-level print_run on 3: Future Cornerstones Autographs /99 ("/99 or less"),
    Dual Autographs /25, Triple Autographs /25.
  - No subset renames (file forms kept). Charleston Riverdogs -> Charleston
    RiverDogs fixed in the file (9 rows); all 112 clubs stored as printed.
  - Names as printed with diacritics. 184 exact matches to existing Baseball
    athletes, 0 folds, 43 new prospects (incl. Jose Anderson). RC: nothing flagged
    here (is_rookie 0 everywhere); 91 subjects carry RC in other sets — left as-is.
  - pack_odds values stored as raw odds strings (recent-set convention, e.g. 838/874):
    "1:X" and the single per-pack "6:1" (Base Chrome). Base base-line has no key.
  - Parallels: print_run + note from the file. X-Fractor (Base Chrome) is the one
    NULL-print_run parallel, note "unnumbered". No exclusivity (single format).

Data model: one player_appearances row per subject; co-player links grouped by
(insert_set_id, card_number), bidirectional. Distinct cards 977; appearance rows
1,044; links 162.

Run post-seed.ts then migrate-to-turso.ts --set 2026-topps-pro-debut-baseball.
Usage: python3 scripts/seed_pro_debut_baseball_2026.py
"""
import sqlite3, os, json, re, unicodedata

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
JSONL = os.path.join(os.path.dirname(__file__), "..", "scratchpad", "pd.jsonl")
ODDS = os.path.join(os.path.dirname(__file__), "..", "scratchpad", "pdodds.jsonl")

SET_NAME = "2026 Topps Pro Debut Baseball"
SET_SLUG = "2026-topps-pro-debut-baseball"
TOPPS_URL = "https://www.topps.com/pages/topps-pro-debut-baseball"
FORMAT = "hobby_jumbo"

BASE_SUBSETS = {"Base", "Base Chrome"}
AUTOGRAPH_SUBSETS = {
    "Base Autographs", "Base Chrome Autographs",
    "2025 Arizona Fall League Stars Autographs", "Pro Debut Gamers Autographs",
    "Stars of MiLB Autographs", "Future Cornerstones Autographs",
    "Dual Autographs", "Triple Autographs", "Jumbo Autograph Relic",
}
RELIC_SUBSETS = {"Jumbo Autograph Relic"}


def slugify(t):
    s = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^\w\s-]", "", s.lower().strip())
    s = re.sub(r"[\s_]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")


def odds_value(s):
    """Store the raw odds string; '1:X' and the one per-pack '6:1' both round-trip
    through parseOddsToDenom. parseInt denominators would mangle '6:1' -> 1:1."""
    return s


def main():
    rows = [json.loads(l) for l in open(JSONL) if l.strip()]
    assert len(rows) == 977, f"expected 977 card rows, got {len(rows)}"
    odds = [json.loads(l) for l in open(ODDS) if l.strip()]
    assert len(odds) == 96, f"expected 96 odds rows, got {len(odds)}"

    # ── derive pack_odds + parallel rows + subset-level print_run/notes ──
    fmt_odds = {}
    parallel_rows = []           # (subset, parallel, print_run, note)
    subset_meta = {}             # subset -> {print_run, notes}
    for o in odds:
        sub = o["subset"]
        par = o.get("parallel")
        od = o.get("odds") or {}
        key = sub if par is None else f"{sub} {par}"
        v = od.get(FORMAT)
        if v:
            assert key not in fmt_odds, f"duplicate odds key: {key!r}"
            fmt_odds[key] = odds_value(v)
        if par is None:
            pr = o.get("print_run")
            note = o.get("note")
            # the file's "or less" annotation becomes the human "/<pr> or less"
            if note == "or less" and pr is not None:
                note = f"/{pr} or less"
            subset_meta[sub] = {"print_run": pr, "notes": note}
        else:
            parallel_rows.append((sub, par, o.get("print_run"), o.get("note")))

    assert len(parallel_rows) == 80, f"expected 80 parallels, got {len(parallel_rows)}"
    assert len(fmt_odds) == 95, f"expected 95 pack_odds keys, got {len(fmt_odds)}"

    box_config = json.dumps({
        FORMAT: {
            "cards_per_pack": 24, "packs_per_box": 6, "boxes_per_case": 8,
            "autos_per_box": 4,
        },
    })
    pack_odds = json.dumps({FORMAT: fmt_odds})

    # ── ordered subset list: card first-appearance order ──
    subset_order, seen = [], set()
    for r in rows:
        sub = r["subset"]
        if sub not in seen:
            seen.add(sub); subset_order.append(sub)
    assert len(subset_order) == 16, f"expected 16 subsets, got {len(subset_order)}"

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
               VALUES (?, 'Baseball', '2026', 'MiLB', 'Standard', ?, 1, ?, ?, ?, ?, ?, NULL, ?)""",
            (SET_NAME, SET_SLUG, f"/sets/{SET_SLUG}.jpg", "2026-11-18", box_config,
             pack_odds, TOPPS_URL, "2026-11-17T12:00:00Z"),
        )
        set_id = cur.lastrowid
        print(f"Created set id {set_id}")

        # ── insert_sets (all 16) ──
        is_ids = {}
        for sub in subset_order:
            meta = subset_meta.get(sub, {})
            is_ids[sub] = db.execute(
                """INSERT INTO insert_sets (set_id, name, is_base, is_autograph, is_relic,
                       is_booklet, print_run, notes)
                   VALUES (?, ?, ?, ?, ?, 0, ?, ?)""",
                (set_id, sub,
                 1 if sub in BASE_SUBSETS else 0,
                 1 if sub in AUTOGRAPH_SUBSETS else 0,
                 1 if sub in RELIC_SUBSETS else 0,
                 meta.get("print_run"), meta.get("notes")),
            ).lastrowid
        print(f"Created {len(is_ids)} subsets")

        for sub, par, _, _ in parallel_rows:
            assert sub in is_ids, f"parallel subset not in checklist: {sub!r}"

        # ── players (name as printed); role default athlete ──
        slug_cache = {}

        def goc(name):
            name = name.strip()
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

        # ── appearances: one per subject (primary + co_players); single format ──
        for r in rows:
            sub = r["subset"]
            card = str(r["card_number"])
            subjects = [(r["subject"], r.get("team"))]
            for cp in r.get("co_players", []):
                subjects.append((cp["subject"], cp.get("team")))
            for name, team in subjects:
                db.execute(
                    """INSERT INTO player_appearances
                           (player_id, insert_set_id, card_number, is_rookie, team, subset_tag, formats)
                       VALUES (?, ?, ?, 0, ?, NULL, NULL)""",
                    (goc(name), is_ids[sub], card, team))

        # ── co-player links: group by (insert_set_id, card_number), bidirectional ──
        groups = {}
        for aid, isid, card, pid in db.execute(
            """SELECT pa.id, pa.insert_set_id, pa.card_number, pa.player_id
               FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
               WHERE i.set_id=?""", (set_id,)).fetchall():
            groups.setdefault((isid, card), []).append((aid, pid))
        nlinks = 0
        for grp in groups.values():
            if len(grp) < 2:
                continue
            for aid, _ in grp:
                for oid, opid in grp:
                    if oid == aid:
                        continue
                    db.execute(
                        "INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)",
                        (aid, opid))
                    nlinks += 1

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
        n_par = q1("""SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id
                      WHERE i.set_id=?""", set_id)
        n_par_null = q1("""SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id
                           WHERE i.set_id=? AND p.print_run IS NULL""", set_id)
        n_links = q1("""SELECT COUNT(*) FROM appearance_co_players acp
                        JOIN player_appearances pa ON pa.id=acp.appearance_id
                        JOIN insert_sets i ON i.id=pa.insert_set_id WHERE i.set_id=?""", set_id)
        po = json.loads(q1("SELECT pack_odds FROM sets WHERE id=?", set_id))[FORMAT]

        print(f"subsets={n_sub} (base={n_base} auto={n_auto} relic={n_relic} booklet={n_bk} print_run_set={n_prset})")
        print(f"distinct_cards={n_cards}  appearance_rows={n_app}  players={n_players}  rookie={n_rookie}")
        print(f"parallels={n_par} (null_print_run:{n_par_null})  co_player_links={n_links} (built {nlinks})")
        print(f"pack_odds keys: {len(po)}")

        assert (n_sub, n_base, n_auto, n_relic, n_bk) == (16, 2, 9, 1, 0), "subset-flag gate failed"
        assert n_prset == 3, "expected subset print_run on 3 (Future Cornerstones/Dual/Triple)"
        assert n_cards == 977 and n_app == 1044, "card/appearance gate failed (977 / 1044)"
        assert n_players == 227, "player gate failed (expected 227)"
        assert n_rookie == 0, "rookie gate failed (expected 0)"
        assert n_par == 80 and n_par_null == 1, "parallel gate failed (80; 1 null = X-Fractor)"
        assert n_links == 162, "co-player link gate failed (expected 162)"
        assert len(po) == 95, "pack_odds key-count gate failed (95)"
        # spot-checks (display forms resolve from the stored raw strings)
        spot = {
            "Base Chrome": "6:1", "Base FoilFractor": "1:2493",
            "Base Chrome SuperFractor": "1:2493", "Base Autographs": "1:5",
            "Triple Autographs FoilFractor": "1:34888", "Jumbo Autograph Relic": "1:104",
            "Stars of MiLB": "1:6",
        }
        for k, exp in spot.items():
            assert po.get(k) == exp, f"spot-check {k!r} = {po.get(k)!r}, expected {exp!r}"
        assert "Base" not in po, "Base base-line must have NO pack_odds key"
        # subset print_run / note spot-checks
        fc = db.execute("SELECT print_run, notes FROM insert_sets WHERE set_id=? AND name='Future Cornerstones Autographs'", (set_id,)).fetchone()
        assert fc == (99, "/99 or less"), f"Future Cornerstones meta {fc!r}"
        xf = db.execute("""SELECT p.print_run, p.note FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id
                           WHERE i.set_id=? AND i.name='Base Chrome' AND p.name='X-Fractor'""", (set_id,)).fetchone()
        assert xf == (None, "unnumbered"), f"X-Fractor meta {xf!r}"
        # every pack_odds key resolves to a stored subset or subset + parallel
        valid = set(is_ids.keys())
        par_names = {p[1] for p in parallel_rows}
        for key in po:
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
