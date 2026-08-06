"""
Phase 2: attach pack odds + derive parallel exclusivities for
2025-26 Topps Chrome Updates Basketball (set 866). Local SQLite only.

Source odds:   scripts/chrome_updates_basketball_2526_odds.json (389 keys, key-outer)
Storage shape: sets.pack_odds is FORMAT-OUTER nested, matching set 863
               (2026 Topps Chrome Baseball): {"hobby": {key: "1:X"}, ...}.
Exclusivity:   derived — a non-base parallel key present in exactly one format
               sets parallels.exclusivity to that format. Everything else NULL.

Usage: python3 scripts/attach_chrome_updates_basketball_2526_odds.py
"""
import json, os, sqlite3

DB = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
ODDS = os.path.join(os.path.dirname(__file__), "chrome_updates_basketball_2526_odds.json")
SLUG = "2025-26-topps-chrome-updates-basketball"

FORMATS = ["Hobby", "Jumbo", "Delight", "Sapphire", "Value", "Mega"]
FMT_KEY = {f: f.lower() for f in FORMATS}  # -> box_config/pack_odds format keys

# gates
EXPECT_KEYS = 389
EXPECT_BASE_KEYS = 31
EXPECT_FMT = {"Hobby": 216, "Jumbo": 214, "Delight": 148, "Sapphire": 34, "Value": 187, "Mega": 186}
EXPECT_EXCL_TOTAL = 154
EXPECT_EXCL_BY_FMT = {"Delight": 98, "Sapphire": 32, "Mega": 11, "Value": 10, "Hobby": 2, "Jumbo": 1}


def main():
    odds = json.load(open(ODDS))
    fail = []

    db = sqlite3.connect(os.path.abspath(DB))
    row = db.execute("SELECT id, pack_odds FROM sets WHERE slug=?", (SLUG,)).fetchone()
    if not row:
        print("STOP: set not found."); raise SystemExit(1)
    set_id, cur_odds = row
    if cur_odds not in (None, "", "null"):
        print("STOP: pack_odds already populated. Not overwriting."); raise SystemExit(1)

    # structural preflight
    n_sub = db.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id=?", (set_id,)).fetchone()[0]
    n_par = db.execute("SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id WHERE i.set_id=?", (set_id,)).fetchone()[0]
    n_card = db.execute("SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id WHERE i.set_id=?", (set_id,)).fetchone()[0]
    if (n_sub, n_card, n_par) != (33, 1299, 359):
        print(f"STOP: structure mismatch subsets/cards/parallels={n_sub}/{n_card}/{n_par}, expected 33/1299/359."); raise SystemExit(1)

    # DB lookup structures
    subsets = {r[0]: r[1] for r in db.execute("SELECT name, id FROM insert_sets WHERE set_id=?", (set_id,))}
    # (subset, parallel) -> parallel row id
    par_id = {}
    for is_name, is_id in subsets.items():
        for pr in db.execute("SELECT id, name FROM parallels WHERE insert_set_id=?", (is_id,)):
            par_id[(is_name, pr[1])] = pr[0]
    # valid full keys
    base_keys = {f"{s} Base" for s in subsets}
    parallel_fullkey = {f"{s} {p}": (s, p) for (s, p) in par_id}

    # ---- gate: key counts + format counts + decomposition -------------------
    if len(odds) != EXPECT_KEYS:
        fail.append(f"keys={len(odds)} exp {EXPECT_KEYS}")
    n_base = sum(1 for k in odds if k.endswith(" Base"))
    if n_base != EXPECT_BASE_KEYS:
        fail.append(f"base-tier keys={n_base} exp {EXPECT_BASE_KEYS}")
    fmt_counts = {f: 0 for f in FORMATS}
    for k, v in odds.items():
        for f, val in v.items():
            if f not in FORMATS:
                fail.append(f"unknown format {f!r} in key {k!r}")
            elif val is not None:
                fmt_counts[f] += 1
    for f in FORMATS:
        if fmt_counts[f] != EXPECT_FMT[f]:
            fail.append(f"format {f} non-null={fmt_counts[f]} exp {EXPECT_FMT[f]}")

    # decomposition: every key maps to real subset base tier or real parallel
    unmappable = []
    for k in odds:
        if k.endswith(" Base"):
            if k not in base_keys:
                unmappable.append(k)
        else:
            if k not in parallel_fullkey:
                unmappable.append(k)
    if unmappable:
        for k in unmappable:
            print("UNMAPPABLE KEY:", k)
        fail.append(f"{len(unmappable)} unmappable keys")

    # ---- derive exclusivity (single-format non-base keys) -------------------
    excl = {}  # (subset, parallel) -> format
    for k, v in odds.items():
        if k.endswith(" Base"):
            continue
        formats_present = [f for f, val in v.items() if val is not None]
        if len(formats_present) == 1:
            s, p = parallel_fullkey[k]
            excl[(s, p)] = formats_present[0]
    excl_by_fmt = {}
    for f in excl.values():
        excl_by_fmt[f] = excl_by_fmt.get(f, 0) + 1
    if len(excl) != EXPECT_EXCL_TOTAL:
        fail.append(f"exclusivity rows={len(excl)} exp {EXPECT_EXCL_TOTAL}")
    for f, c in EXPECT_EXCL_BY_FMT.items():
        if excl_by_fmt.get(f, 0) != c:
            fail.append(f"exclusivity[{f}]={excl_by_fmt.get(f, 0)} exp {c}")
    for f in excl_by_fmt:
        if f not in EXPECT_EXCL_BY_FMT:
            fail.append(f"unexpected exclusivity format {f}={excl_by_fmt[f]}")

    if fail:
        print("INTEGRITY GATE FAILURES (no writes):")
        for m in fail:
            print("  ", m)
        raise SystemExit(1)

    # ---- transform to format-outer shape (863 convention) -------------------
    nested = {FMT_KEY[f]: {} for f in FORMATS}
    for k, v in odds.items():
        for f, val in v.items():
            if val is not None:
                nested[FMT_KEY[f]][k] = val
    # drop any format with no keys (keep all six here; all have keys)
    nested = {fk: d for fk, d in nested.items() if d}

    # ---- write pack_odds ----------------------------------------------------
    db.execute("UPDATE sets SET pack_odds=? WHERE id=?", (json.dumps(nested), set_id))

    # ---- write exclusivity --------------------------------------------------
    updated = 0
    for (s, p), f in excl.items():
        db.execute("UPDATE parallels SET exclusivity=? WHERE id=?", (f, par_id[(s, p)]))
        updated += 1
    db.commit()

    # ---- verify ------------------------------------------------------------
    n_excl_db = db.execute(
        "SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id WHERE i.set_id=? AND p.exclusivity IS NOT NULL",
        (set_id,)).fetchone()[0]
    stored = json.loads(db.execute("SELECT pack_odds FROM sets WHERE id=?", (set_id,)).fetchone()[0])
    print(f"pack_odds formats: { {k: len(v) for k, v in stored.items()} }")
    print(f"exclusivity rows written: {updated} (db non-null: {n_excl_db})")
    print(f"exclusivity by format: {excl_by_fmt}")
    if n_excl_db != EXPECT_EXCL_TOTAL:
        print("STOP: exclusivity row count mismatch after write."); raise SystemExit(1)
    print("INTEGRITY GATES: all pass. OK.")
    db.close()


if __name__ == "__main__":
    main()
