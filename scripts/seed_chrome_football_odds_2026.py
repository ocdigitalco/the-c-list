"""
Modify: attach odds, parallels, eight-format box configs and the final-checklist
delta to 2026 Topps Chrome Football (set 898). Append-only — the set already
exists (built 2026-10-16); this does NOT recreate it.

Sources:
  scratchpad/tcfadd.jsonl  — 112 final-checklist delta cards:
        {subset, card_number, subject, team, rookie, co_players?:[{subject,team,rookie}]}
  scratchpad/tcfodds.jsonl — 588 odds lines: 57 subset-level (parallel=null) + 531
        parallel lines; each carries odds{8 formats?}, print_run, note?.

Rulings applied (Phase 0 report + go, 2026-11-18):
  - 3 new subsets: 2023 Prem1ere Patch Autograph (47), 2024 Prem1ere Patch
    Autograph (59), Gold Shield Dual Autograph (1, Stafford/Allen). All three
    is_autograph 1, is_relic 1, print_run 1.
  - 4 new cards in existing subsets (BVA-DM, BVA-PM, DA-MB dual Brady/Maye,
    TA-DM) + 1 redemption FAR-94 (Mahomes II, appended after FAR-93).
    112 delta rows -> 114 appearance rows (DA-MB + GSDA-AS add a 2nd subject),
    4 new co-player links. 64 subjects fold into existing players, 46 new.
  - Lombardi Trophy LT-1 left as-is (stored no team).
  - Subset print_run on 15 subsets (numbered-parent rule) from the odds file.
  - 531 parallels: print_run + note from file (46 NULL "unnumbered"; FrozenFractor
    pr=5 note "serial numbered -5/0"). Exclusivity = single-format label (163
    rows); Wave ladder (jumbo+fdi) gets none.
  - pack_odds: 8 formats, 2,603 keys, stored as RAW odds strings (838/874
    convention; "X:1" per-pack forms must survive parseOddsToDenom).
  - formats stamped on the 35 subsets whose own odds line covers <8 formats
    (set-wide: existing + new appearances). Base Cards / Base Variation
    Autographs have no subset line (all-format base) -> no stamp.
  - box_config: 8 keys. hobby 4x20 (12/case, 1 auto); hobby_jumbo 11x12 (2);
    fdi 11x12 (3, notes rewritten); delight 12x1 (2); mega 7x6; value_blaster
    4x7; hanger 14x1 (note: education sheet prints 20); fanatics 7x6 (existing
    key/label "Fanatics", shared with 44/834/870). release_date 2026-11-18;
    FDI 2026-11-13 + Mega 2026-12-02 in their box notes.

Usage: python3 scripts/seed_chrome_football_odds_2026.py
"""
import sqlite3, os, json

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
ADD = os.path.join(os.path.dirname(__file__), "..", "scratchpad", "tcfadd.jsonl")
ODDS = os.path.join(os.path.dirname(__file__), "..", "scratchpad", "tcfodds.jsonl")

SET_SLUG = "2026-topps-chrome-football"
RELEASE_DATE = "2026-11-18"

FMT = ["hobby", "hobby_jumbo", "delight", "fdi", "hanger", "value_blaster", "mega", "fanatics"]
EXCL_LABEL = {
    "hobby": "Hobby", "hobby_jumbo": "Hobby Jumbo", "delight": "Breaker Delight",
    "fdi": "First Day Issue", "hanger": "Hanger", "value_blaster": "Value Blaster",
    "mega": "Mega", "fanatics": "Fanatics",
}
NEW_SUBSETS = ["2023 Prem1ere Patch Autograph", "2024 Prem1ere Patch Autograph",
               "Gold Shield Dual Autograph"]

BOX_CONFIG = {
    "hobby": {"cards_per_pack": 4, "packs_per_box": 20, "boxes_per_case": 12, "autos_per_box": 1},
    "hobby_jumbo": {"cards_per_pack": 11, "packs_per_box": 12, "boxes_per_case": None, "autos_per_box": 2},
    "fdi": {"cards_per_pack": 11, "packs_per_box": 12, "boxes_per_case": None, "autos_per_box": 3,
            "notes": "1 FDI Molten Mercury autograph, 2 additional autographs, 2 FDI Molten Mercury "
                     "parallels, 2 additional parallels. First Day Issue boxes released November 13, 2026."},
    "delight": {"cards_per_pack": 12, "packs_per_box": 1, "boxes_per_case": None, "autos_per_box": 2,
                "notes": "1 Geometric autograph and 1 additional autograph."},
    "mega": {"cards_per_pack": 7, "packs_per_box": 6, "boxes_per_case": None,
             "notes": "Mega boxes release December 2, 2026."},
    "value_blaster": {"cards_per_pack": 4, "packs_per_box": 7, "boxes_per_case": None},
    "hanger": {"cards_per_pack": 14, "packs_per_box": 1, "boxes_per_case": None,
               "notes": "Topps's education sheet prints 20 cards per Hanger pack."},
    "fanatics": {"cards_per_pack": 7, "packs_per_box": 6, "boxes_per_case": None},
}


def main():
    add = [json.loads(l) for l in open(ADD) if l.strip()]
    odds = [json.loads(l) for l in open(ODDS) if l.strip()]
    assert len(add) == 112, f"expected 112 add rows, got {len(add)}"
    assert len(odds) == 588, f"expected 588 odds rows, got {len(odds)}"

    # ── derive pack_odds / parallels / subset meta / formats stamp ──
    pack_odds = {f: {} for f in FMT}
    parallel_rows = []        # (subset, parallel, print_run, note, formats_list)
    subset_pr = {}            # subset -> print_run (subset lines only)
    subset_formats = {}       # subset -> [formats] when subset line < 8 formats
    for o in odds:
        sub = o["subset"]
        par = o.get("parallel")
        od = o.get("odds") or {}
        key = sub if par is None else f"{sub} {par}"
        for f, v in od.items():
            assert f in pack_odds, f"unknown format {f!r}"
            assert key not in pack_odds[f], f"dup odds key {key!r} in {f}"
            pack_odds[f][key] = v            # raw string
        present = [f for f in FMT if f in od]
        if par is None:
            if o.get("print_run") is not None:
                subset_pr[sub] = o["print_run"]
            if len(present) != 8:
                subset_formats[sub] = present
        else:
            present_excl = [f for f in od]   # formats this parallel is priced in
            excl = EXCL_LABEL[present_excl[0]] if len(present_excl) == 1 else None
            parallel_rows.append((sub, par, o.get("print_run"), o.get("note"), excl))

    key_counts = {f: len(pack_odds[f]) for f in FMT}
    total_keys = sum(key_counts.values())
    assert len(parallel_rows) == 531, f"expected 531 parallels, got {len(parallel_rows)}"
    assert key_counts == {"hobby": 331, "hobby_jumbo": 345, "delight": 269, "fdi": 352,
                          "hanger": 332, "value_blaster": 362, "mega": 345, "fanatics": 267}, \
        f"per-format key counts off: {key_counts}"
    assert total_keys == 2603, f"expected 2603 odds keys, got {total_keys}"
    assert len(subset_formats) == 35, f"expected 35 formats-stamp subsets, got {len(subset_formats)}"
    assert len(subset_pr) == 15, f"expected 15 subset print_runs, got {len(subset_pr)}"

    db = sqlite3.connect(DB_PATH)
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA foreign_keys=ON")
    row = db.execute("SELECT id FROM sets WHERE slug=?", (SET_SLUG,)).fetchone()
    assert row, f"set {SET_SLUG} not found"
    set_id = row[0]
    # guard: append-only preconditions
    pre = db.execute("""SELECT
        (SELECT COUNT(*) FROM insert_sets WHERE set_id=?),
        (SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id WHERE i.set_id=?),
        (SELECT pack_odds FROM sets WHERE id=?)""", (set_id, set_id, set_id)).fetchone()
    assert pre[0] == 56, f"expected 56 existing subsets, got {pre[0]}"
    assert pre[1] == 0, f"expected 0 existing parallels, got {pre[1]}"
    assert pre[2] is None, "pack_odds already set — aborting"
    print(f"set id {set_id}; pre-state OK (56 subsets, 0 parallels, pack_odds NULL)")

    try:
        # ── insert_set id map (existing) ──
        is_ids = {n: i for (i, n) in
                  db.execute("SELECT id, name FROM insert_sets WHERE set_id=?", (set_id,))}

        # ── 3 new subsets (autograph + relic + print_run 1) ──
        for sub in NEW_SUBSETS:
            assert sub not in is_ids, f"new subset already present: {sub}"
            is_ids[sub] = db.execute(
                """INSERT INTO insert_sets (set_id, name, is_base, is_autograph, is_relic,
                       is_booklet, print_run, notes)
                   VALUES (?, ?, 0, 1, 1, 0, 1, NULL)""", (set_id, sub)).lastrowid
        print(f"created {len(NEW_SUBSETS)} new subsets")

        # ── subset print_run on the 15 (3 new already set; update the rest) ──
        for sub, pr in subset_pr.items():
            db.execute("UPDATE insert_sets SET print_run=? WHERE id=?", (pr, is_ids[sub]))

        # ── players (fold by name; new ones role athlete, slug NULL per set convention) ──
        def goc(name):
            name = name.strip()
            r = db.execute("SELECT id FROM players WHERE set_id=? AND name=?", (set_id, name)).fetchone()
            if r:
                return r[0]
            return db.execute(
                """INSERT INTO players (set_id, name, unique_cards, total_print_run,
                       one_of_ones, insert_set_count, subject_role)
                   VALUES (?, ?, 0, 0, 0, 0, 'athlete')""", (set_id, name)).lastrowid

        players_before = db.execute("SELECT COUNT(*) FROM players WHERE set_id=?", (set_id,)).fetchone()[0]

        # ── 531 parallels ──
        for sub, par, pr, note, excl in parallel_rows:
            assert sub in is_ids, f"parallel subset not in checklist: {sub!r}"
            db.execute(
                """INSERT INTO parallels (insert_set_id, name, print_run, exclusivity, note)
                   VALUES (?, ?, ?, ?, ?)""", (is_ids[sub], par, pr, excl, note))

        # ── 114 appearance rows (112 cards + 2 duals' 2nd subject); formats stamped later ──
        new_app_ids = []    # (insert_set_id, card_number, appearance_id)
        for r in add:
            sub = r["subset"]
            card = str(r["card_number"])
            isid = is_ids[sub]
            subjects = [(r["subject"], r.get("team"), int(r.get("rookie") or 0))]
            for cp in r.get("co_players", []):
                subjects.append((cp["subject"], cp.get("team"), int(cp.get("rookie") or 0)))
            for name, team, rk in subjects:
                aid = db.execute(
                    """INSERT INTO player_appearances
                           (player_id, insert_set_id, card_number, is_rookie, team, subset_tag, formats)
                       VALUES (?, ?, ?, ?, ?, NULL, NULL)""",
                    (goc(name), isid, card, rk, team)).lastrowid
                new_app_ids.append((isid, card, aid))

        # ── co-player links: only the NEW multi-subject cards, bidirectional ──
        groups = {}
        for isid, card, aid in new_app_ids:
            pid = db.execute("SELECT player_id FROM player_appearances WHERE id=?", (aid,)).fetchone()[0]
            groups.setdefault((isid, card), []).append((aid, pid))
        nlinks = 0
        for grp in groups.values():
            if len(grp) < 2:
                continue
            for aid, _ in grp:
                for oid, opid in grp:
                    if oid != aid:
                        db.execute(
                            "INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)",
                            (aid, opid))
                        nlinks += 1

        # ── formats stamp: set-wide for the 35 partial-format subsets ──
        for sub, flist in subset_formats.items():
            db.execute("UPDATE player_appearances SET formats=? WHERE insert_set_id=?",
                       (json.dumps(flist), is_ids[sub]))

        # ── set fields ──
        db.execute("UPDATE sets SET pack_odds=?, box_config=?, release_date=? WHERE id=?",
                   (json.dumps(pack_odds), json.dumps(BOX_CONFIG), RELEASE_DATE, set_id))

        db.commit()

        # ── gates ──
        def q1(sql, *a):
            return db.execute(sql, a).fetchone()[0]

        n_sub = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=?", set_id)
        n_new_flagged = q1("""SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND name IN (?,?,?)
                              AND is_autograph=1 AND is_relic=1 AND print_run=1""",
                           set_id, *NEW_SUBSETS)
        n_prset = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND print_run IS NOT NULL", set_id)
        n_cards = q1("""SELECT COUNT(DISTINCT pa.insert_set_id || ':' || pa.card_number)
                        FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                        WHERE i.set_id=?""", set_id)
        n_app = q1("""SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                      WHERE i.set_id=?""", set_id)
        n_players = q1("SELECT COUNT(*) FROM players WHERE set_id=?", set_id)
        n_par = q1("""SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id
                      WHERE i.set_id=?""", set_id)
        n_par_null = q1("""SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id
                           WHERE i.set_id=? AND p.print_run IS NULL""", set_id)
        n_excl = q1("""SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id
                       WHERE i.set_id=? AND p.exclusivity IS NOT NULL""", set_id)
        n_frozen = q1("""SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id
                         WHERE i.set_id=? AND p.name='FrozenFractor' AND p.print_run=5
                         AND p.note='serial numbered -5/0'""", set_id)
        n_far = q1("""SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                      WHERE i.set_id=? AND i.name='Fanatics Authentics Redemption Card'""", set_id)
        far_max = q1("""SELECT MAX(CAST(replace(pa.card_number,'FAR-','') AS INT))
                        FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                        WHERE i.set_id=? AND i.name='Fanatics Authentics Redemption Card'""", set_id)
        n_fmt_stamped = q1("""SELECT COUNT(DISTINCT pa.insert_set_id)
                              FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                              WHERE i.set_id=? AND pa.formats IS NOT NULL""", set_id)
        # links scoped to the two NEW dual cards (set 898 has 30 pre-existing links)
        n_links = q1("""SELECT COUNT(*) FROM appearance_co_players acp
                        JOIN player_appearances pa ON pa.id=acp.appearance_id
                        JOIN insert_sets i ON i.id=pa.insert_set_id
                        WHERE i.set_id=? AND ((i.name='Dual Autographs' AND pa.card_number='DA-MB')
                              OR (i.name='Gold Shield Dual Autograph' AND pa.card_number='GSDA-AS'))""", set_id)
        po = json.loads(q1("SELECT pack_odds FROM sets WHERE id=?", set_id))
        bc = json.loads(q1("SELECT box_config FROM sets WHERE id=?", set_id))
        rd = q1("SELECT release_date FROM sets WHERE id=?", set_id)

        print(f"subsets={n_sub} (new flagged auto+relic+pr1: {n_new_flagged}/3; print_run_set={n_prset})")
        print(f"distinct_cards={n_cards}  appearance_rows={n_app}  players={n_players} (+{n_players-players_before} new)")
        print(f"parallels={n_par} (null={n_par_null}; exclusivity={n_excl}; FrozenFractor@5={n_frozen})")
        print(f"FAR count={n_far} max=FAR-{far_max}  co_player_links={n_links}")
        print(f"formats-stamped subsets={n_fmt_stamped}  box_config keys={len(bc)}  release_date={rd}")
        print(f"pack_odds per-format: {key_counts} total={total_keys}")

        assert n_sub == 59, "subset gate (59)"
        assert n_new_flagged == 3, "new-subset flag gate"
        assert n_prset == 15, "subset print_run gate (15)"
        assert n_cards == 2479, f"distinct-card gate (2479), got {n_cards}"
        assert n_app == 2496, f"appearance-row gate (2496), got {n_app}"
        assert n_players == players_before + 46, f"player gate (+46), got +{n_players-players_before}"
        assert n_par == 531 and n_par_null == 46, "parallel gate (531; 46 null)"
        assert n_excl == 163, f"exclusivity gate (163), got {n_excl}"
        assert n_frozen == 2, "FrozenFractor gate (2 @ /5)"
        assert n_far == 94 and far_max == 94, "FAR gate (94 cards, max FAR-94)"
        assert n_fmt_stamped == 35, f"formats-stamp gate (35), got {n_fmt_stamped}"
        assert n_links == 4, f"co-player link gate (4), got {n_links}"
        assert len(bc) == 8 and set(bc) == set(FMT), "box_config 8-key gate"
        assert rd == RELEASE_DATE, "release_date gate"
        assert set(po) == set(FMT), "pack_odds format-key gate"
        assert {f: len(po[f]) for f in FMT} == key_counts, "pack_odds count gate"

        # FAR-1..93 unchanged (contiguous, still present)
        far_ints = sorted(int(c.split("-")[1]) for (c,) in db.execute(
            """SELECT pa.card_number FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
               WHERE i.set_id=? AND i.name='Fanatics Authentics Redemption Card'""", (set_id,)))
        assert far_ints == list(range(1, 95)), "FAR not contiguous 1..94"

        # spot-check odds (raw strings survive parseOddsToDenom round-trip on the page)
        spot = {
            ("hobby", "Base Cards Refractor"): "1:3", ("delight", "Base Cards Refractor"): "3:1",
            ("fdi", "Base Cards Molten Mercury Refractor"): "1:8",
            ("hobby", "Rookie"): "1:1", ("hobby_jumbo", "Rookie"): "2:1",
            ("hobby", "Rookie Neon Burst Refractor"): "1:120",
            ("hobby", "Base Cards SuperFractor"): "1:22096",
            ("hobby", "Lombardi Trophy Superfractor"): "1:2776560",
            ("hobby", "Gold Shield Dual Autograph"): "1:9717960",
            ("fanatics", "Fanatics Authentics Redemption Card"): "1:240",
            ("hobby", "MVP Buyback Football Leather Refractor"): "1:378712",
        }
        for (f, k), exp in spot.items():
            got = po[f].get(k)
            assert got == exp, f"spot {f}/{k!r} = {got!r}, want {exp!r}"
        # single-format-only keys really are single-format
        assert set(po["fdi"].keys()) & {"Base Cards Molten Mercury Refractor"} and \
            "Base Cards Molten Mercury Refractor" not in po["hobby"], "Molten Mercury should be FDI-only"
        assert "Lombardi Trophy Superfractor" not in po["hobby_jumbo"], "Lombardi should be hobby-only"
        assert set(po["fanatics"].keys()) >= {"Fanatics Authentics Redemption Card"} and \
            "Fanatics Authentics Redemption Card" not in po["mega"], "FAR should be fanatics-only"
        assert "Base Cards" not in po["hobby"], "Base Cards base-line must have no key"

        # every pack_odds key resolves to a stored subset or subset+parallel
        valid = set(is_ids.keys())
        par_names = {p[1] for p in parallel_rows}
        for f in FMT:
            for key in po[f]:
                if key in valid:
                    continue
                ok = any(key == f"{s} {pn}" for s in valid for pn in par_names if key.startswith(s + " "))
                assert ok, f"unresolvable pack_odds key: {key!r}"

        print("ALL LOCAL GATES PASSED.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
