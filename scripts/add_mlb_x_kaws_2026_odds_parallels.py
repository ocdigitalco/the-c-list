"""
2026 Topps MLB x KAWS (set 862): attach single-format pack odds, 25 serialized
numbered parallels, and box configuration. Maps to EXISTING subsets only.

Odds keys follow the app's lookupOddsValue convention:
  * parallel      → "{subset name} {parallel name}"  (e.g. "Base Set Aqua")
  * subset base   → "{subset name}"                  (e.g. "KAWS Creation")
Denominators are the X of "1:X". Single-format → flat {key: int} object.

The three autograph subsets (Autographs, On-Card Autographs, KAWS Companion SSP
Autos) have NO subset base-odds key by design — every auto exists only as a
serialized parallel, so all their odds live on the parallel rows.

Local SQLite only. Usage: python3 scripts/add_mlb_x_kaws_2026_odds_parallels.py
"""
import json
import os
import sqlite3

SET_ID = 862
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")

BOX_CONFIG = {
    "cards_per_pack": 4,
    "packs_per_box": 3,
    "boxes_per_case": None,  # unknown
    "notes": "Every pack: 3 base cards + 1 hit slot (parallel, KAWS Creation "
             "insert, Companion SP, KAWS SSP autograph, or MLB player autograph).",
}

# (parallel name, print_run | None, odds denominator)  per DB subset name
PARALLELS = {
    "Base Set": [
        ("Unnumbered", None, 3), ("Aqua", 199, 5), ("Blue", 150, 7),
        ("Green", 99, 10), ("Purple", 75, 13), ("Gold", 50, 19),
        ("Orange", 25, 38), ("Black", 10, 93), ("Red", 5, 186),
        ("Foilfractor", 1, 916),
    ],
    "KAWS Creation": [("Foilfractor", 1, 2160)],
    "Autographs": [
        ("Gold", 50, 73), ("Orange", 25, 95), ("Black", 10, 188),
        ("Red", 5, 260), ("Foilfractor", 1, 1174),
    ],
    "On-Card Autographs": [
        ("Gold", 50, 73), ("Orange", 25, 95), ("Black", 10, 188),
        ("Red", 5, 260), ("Foilfractor", 1, 1174),
    ],
    "KAWS Companion SPs": [("Foilfractor", 1, 5400)],
    "KAWS Companion SSP Autos": [
        ("Black", 10, 5400), ("Red", 5, 10800), ("Foilfractor", 1, 54000),
    ],
}

# Subset-level base odds (non-auto inserts only). Auto subsets stay NULL.
SUBSET_BASE_ODDS = {"KAWS Creation": 12, "KAWS Companion SPs": 78}


def main():
    db = sqlite3.connect(os.path.abspath(DB_PATH))

    row = db.execute("SELECT pack_odds, box_config FROM sets WHERE id=?", (SET_ID,)).fetchone()
    if row is None:
        print("STOP: set 862 not found."); raise SystemExit(1)
    n_par = db.execute(
        "SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id WHERE i.set_id=?",
        (SET_ID,)).fetchone()[0]
    if n_par != 0:
        print(f"STOP: set already has {n_par} parallels. Not overwriting."); raise SystemExit(1)
    if row[0] or row[1]:
        print(f"STOP: pack_odds/box_config already set (odds={bool(row[0])}, box={bool(row[1])})."); raise SystemExit(1)

    # resolve subset name → id (map to EXISTING subsets only)
    is_id, skipped = {}, []
    for name in PARALLELS:
        r = db.execute("SELECT id FROM insert_sets WHERE set_id=? AND name=?", (SET_ID, name)).fetchone()
        if r:
            is_id[name] = r[0]
        else:
            skipped.append(name)
    if skipped:
        print("SKIP-AND-REPORT (subset not found):", skipped)
        print("Aborting without writing (never create subsets)."); raise SystemExit(1)

    # build pack_odds (flat single-format object): parallels + subset base odds
    pack_odds = {}
    for subset, pars in PARALLELS.items():
        for pname, _pr, denom in pars:
            pack_odds[f"{subset} {pname}"] = denom
    for subset, denom in SUBSET_BASE_ODDS.items():
        pack_odds[subset] = denom

    # write box_config + pack_odds
    db.execute("UPDATE sets SET box_config=?, pack_odds=? WHERE id=?",
               (json.dumps(BOX_CONFIG), json.dumps(pack_odds), SET_ID))

    # insert parallel rows (odds live in pack_odds, not on the row)
    inserted = 0
    for subset, pars in PARALLELS.items():
        for pname, pr, _denom in pars:
            db.execute(
                "INSERT INTO parallels (insert_set_id, name, print_run) VALUES (?,?,?)",
                (is_id[subset], pname, pr))
            inserted += 1
    db.commit()

    # report
    print(f"Inserted {inserted} parallel rows; pack_odds keys: {len(pack_odds)}; box_config set.\n")
    print("Per-subset (parallels / has-base-odds):")
    for subset in PARALLELS:
        cnt = db.execute("SELECT COUNT(*) FROM parallels WHERE insert_set_id=?", (is_id[subset],)).fetchone()[0]
        base = "base-odds " + str(SUBSET_BASE_ODDS[subset]) if subset in SUBSET_BASE_ODDS else "base-odds NULL"
        print(f"  {subset:26s} {cnt:2d}  ({base})")
    total = db.execute(
        "SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id WHERE i.set_id=?",
        (SET_ID,)).fetchone()[0]
    numbered = db.execute(
        "SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id "
        "WHERE i.set_id=? AND p.print_run IS NOT NULL", (SET_ID,)).fetchone()[0]
    print(f"\nTOTAL parallels: {total}  (numbered: {numbered}, unnumbered: {total - numbered})")
    print("SKIP-AND-REPORT:", skipped if skipped else "none")
    hc = db.execute("SELECT pack_odds IS NOT NULL, box_config IS NOT NULL FROM sets WHERE id=?", (SET_ID,)).fetchone()
    print(f"Coverage: pack_odds set = {bool(hc[0])}; box_config set = {bool(hc[1])}; numbered parallels = {numbered}")
    db.close()


if __name__ == "__main__":
    main()
