"""
Attach odds + parallels to 2026 Topps Midnight Football (set 893, existing).

Source:
  scratchpad/midodds.jsonl — 213 lines (19 subset-level + 194 parallel), each
  {subset, parallel|null, print_run, odds:{hobby?, fdi?, instant?}, exclusivity?}.
  Odds = official Topps sheet (Hobby/FDI/Instant Wax); print runs = Tyler's list.

Rulings (Phase 0 + go, 2026-11-16):
  - Stored subset name wins: file "Tenebrous Traces Autographs" -> "Tenebrous Traces".
    pack_odds keys use the stored name.
  - pack_odds: 3 formats, keys only where the sheet has a figure (gaps stay gaps).
    hobby 207 / fdi 207 / instant 199 = 613 keys. Merge into existing pack_odds
    (currently NULL) without clobbering any format not in the file.
  - box_config: add missing `instant` key as Configuration TBA (873 precedent:
    all-null numbers + notes "Configuration TBA"); keep hobby/fdi untouched.
  - 194 parallels: print_run from the file; note "unnumbered" on the 14 NULL
    print_run rows (Zodiac + Moon Beam); exclusivity verbatim from the file on
    the 6 one-format rows ("FDI" / "Instant Packs").
  - player_appearances.formats = ["hobby","fdi"] on the four case-hit inserts
    (Celestial Roots, Dream Land, Night Night, Twilight) ONLY — their parent
    subset line has no instant figure. No other appearances touched.

Run post-seed.ts then migrate-to-turso.ts --set 2026-topps-midnight-football after.
Usage: python3 scripts/attach_midnight_football_odds_2026.py
"""
import sqlite3, os, json

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
ODDS = os.path.join(os.path.dirname(__file__), "..", "scratchpad", "midodds.jsonl")

SET_SLUG = "2026-topps-midnight-football"
FORMATS = ("hobby", "fdi", "instant")

SUBSET_RENAME = {"Tenebrous Traces Autographs": "Tenebrous Traces"}
UNNUMBERED = {"Zodiac", "Moon Beam"}
CASE_HIT_INSERTS = {"Celestial Roots", "Dream Land", "Night Night", "Twilight"}


def ren(s):
    return SUBSET_RENAME.get(s, s)


def to_denom(s):
    return int(s.split(":", 1)[1])


def main():
    lines = [json.loads(l) for l in open(ODDS) if l.strip()]
    assert len(lines) == 213, f"expected 213 odds lines, got {len(lines)}"

    db = sqlite3.connect(DB_PATH)
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA foreign_keys=ON")

    row = db.execute("SELECT id, box_config, pack_odds FROM sets WHERE slug=?", (SET_SLUG,)).fetchone()
    if not row:
        raise SystemExit(f"Set {SET_SLUG!r} not found.")
    set_id, box_config_raw, pack_odds_raw = row
    print(f"Set id {set_id}")

    # insert_set id lookup by stored name
    is_ids = {}
    for iid, name in db.execute("SELECT id, name FROM insert_sets WHERE set_id=?", (set_id,)):
        is_ids[name] = iid

    existing_par = db.execute(
        """SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id
           WHERE i.set_id=?""", (set_id,)).fetchone()[0]
    assert existing_par == 0, f"expected 0 existing parallels, found {existing_par} — stop and reconcile"

    # ── build pack_odds (merge into existing) + parallel rows ──
    hobby_odds, fdi_odds, instant_odds = {}, {}, {}
    fmt_map = {"hobby": hobby_odds, "fdi": fdi_odds, "instant": instant_odds}
    parallel_rows = []  # (subset, parallel, print_run, exclusivity, note)
    for l in lines:
        sub = ren(l["subset"])
        assert sub in is_ids, f"subset not in checklist: {sub!r}"
        par = l.get("parallel")
        key = sub if par is None else f"{sub} {par}"
        od = l.get("odds") or {}
        for fmt in FORMATS:
            v = od.get(fmt)
            if v:
                assert key not in fmt_map[fmt], f"duplicate {fmt} key: {key!r}"
                fmt_map[fmt][key] = to_denom(v)
        if par is not None:
            note = "unnumbered" if par in UNNUMBERED else None
            parallel_rows.append((sub, par, l.get("print_run"), l.get("exclusivity"), note))

    assert len(parallel_rows) == 194, f"expected 194 parallels, got {len(parallel_rows)}"
    assert (len(hobby_odds), len(fdi_odds), len(instant_odds)) == (207, 207, 199), \
        f"key counts {len(hobby_odds)}/{len(fdi_odds)}/{len(instant_odds)} != 207/207/199"

    existing_po = json.loads(pack_odds_raw) if pack_odds_raw else {}
    merged_po = dict(existing_po)
    merged_po["hobby"] = hobby_odds
    merged_po["fdi"] = fdi_odds
    merged_po["instant"] = instant_odds
    pack_odds = json.dumps(merged_po)

    # box_config: add instant TBA key, keep others
    bc = json.loads(box_config_raw) if box_config_raw else {}
    assert "instant" not in bc, "instant box key already present — reconcile"
    bc["instant"] = {"cards_per_pack": None, "packs_per_box": None,
                     "boxes_per_case": None, "notes": "Configuration TBA"}
    box_config = json.dumps(bc)

    try:
        for sub, par, pr, excl, note in parallel_rows:
            db.execute(
                """INSERT INTO parallels (insert_set_id, name, print_run, exclusivity, note)
                   VALUES (?, ?, ?, ?, ?)""",
                (is_ids[sub], par, pr, excl, note))

        db.execute("UPDATE sets SET pack_odds=?, box_config=? WHERE id=?",
                   (pack_odds, box_config, set_id))

        # formats = ["hobby","fdi"] on the four case-hit inserts only
        fmt_val = json.dumps(["hobby", "fdi"])
        fmt_set = 0
        for sub in CASE_HIT_INSERTS:
            cur = db.execute(
                "UPDATE player_appearances SET formats=? WHERE insert_set_id=?",
                (fmt_val, is_ids[sub]))
            fmt_set += cur.rowcount

        db.commit()

        # ── verification ──
        def q1(sql, *a):
            return db.execute(sql, a).fetchone()[0]

        n_par = q1("""SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id
                      WHERE i.set_id=?""", set_id)
        n_null = q1("""SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id
                       WHERE i.set_id=? AND p.print_run IS NULL""", set_id)
        n_excl = q1("""SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id
                       WHERE i.set_id=? AND p.exclusivity IS NOT NULL""", set_id)
        n_unnum = q1("""SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id
                        WHERE i.set_id=? AND p.note='unnumbered'""", set_id)
        po = json.loads(q1("SELECT pack_odds FROM sets WHERE id=?", set_id))
        kh, kf, ki = len(po["hobby"]), len(po["fdi"]), len(po["instant"])
        bc2 = json.loads(q1("SELECT box_config FROM sets WHERE id=?", set_id))
        n_fmt = q1("""SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                      WHERE i.set_id=? AND pa.formats IS NOT NULL""", set_id)
        excl_rows = db.execute(
            """SELECT i.name, p.name, p.exclusivity FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id
               WHERE i.set_id=? AND p.exclusivity IS NOT NULL ORDER BY i.name, p.name""", (set_id,)).fetchall()

        print(f"parallels={n_par}  null_print_run={n_null}  exclusivity={n_excl}  unnumbered_note={n_unnum}")
        print(f"pack_odds keys: hobby={kh} fdi={kf} instant={ki}")
        print(f"box_config keys: {sorted(bc2.keys())}  instant.notes={bc2['instant']['notes']!r}")
        print(f"appearances with formats set={n_fmt}")
        print("exclusivity rows:")
        for a, b, c in excl_rows:
            print(f"    {a} | {b} -> {c!r}")

        assert n_par == 194, "parallel gate failed (194)"
        assert n_null == 14, "null print_run gate failed (14)"
        assert n_excl == 6, "exclusivity gate failed (6)"
        assert n_unnum == 14, "unnumbered-note gate failed (14)"
        assert (kh, kf, ki) == (207, 207, 199), "pack_odds key-count gate failed"
        assert bc2["instant"]["notes"] == "Configuration TBA", "instant TBA note gate failed"
        assert bc2["instant"]["cards_per_pack"] is None, "instant should have null numbers"
        # spot-checks
        assert po["hobby"]["Base"] == 1 and po["instant"]["Base"] == 2, "Base spot-check failed"
        assert po["fdi"]["Base Molten Mercury"] == 1, "Base Molten Mercury fdi 1:1 failed"
        assert po["instant"]["Base Hourglass"] == 4, "Base Hourglass instant 1:4 failed"
        assert (po["hobby"]["Base Black Light"], po["fdi"]["Base Black Light"], po["instant"]["Base Black Light"]) == (571, 571, 1974), "Base Black Light failed"
        assert (po["hobby"]["Stroke of Midnight Autographs Black Light"], po["fdi"]["Stroke of Midnight Autographs Black Light"], po["instant"]["Stroke of Midnight Autographs Black Light"]) == (4104, 5965, 12656), "Stroke Black Light failed"
        assert (po["hobby"]["Constellations Morning"], po["fdi"]["Constellations Morning"], po["instant"]["Constellations Morning"]) == (34, 34, 67), "Constellations Morning failed"
        assert po["hobby"]["Twilight"] == 32 and po["fdi"]["Twilight"] == 32 and "Twilight" not in po["instant"], "Twilight subset key failed"
        assert po["hobby"]["Twilight Black Light"] == 2092 and po["fdi"]["Twilight Black Light"] == 2092, "Twilight Black Light failed"
        assert (po["hobby"]["Base Twilight"], po["fdi"]["Base Twilight"], po["instant"]["Base Twilight"]) == (6, 6, 21), "Base Twilight failed"
        # every key resolves to a stored subset or subset + parallel
        valid = set(is_ids.keys())
        par_names = set(p[1] for p in parallel_rows)
        for fmt in FORMATS:
            for key in po[fmt]:
                if key in valid:
                    continue
                ok = any(key == f"{s} {pn}" and s in valid for s in valid for pn in par_names if key.startswith(s + " "))
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
