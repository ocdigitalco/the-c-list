"""
2025 Topps Resurgence Football (set 859): attach parallels + four-format pack
odds, set box config + release date, and fix one autograph flag. Local SQLite
only; Tyler migrates to Turso separately.

Parallels -> parallels table (name, print_run, exclusivity).
Odds -> sets.pack_odds nested {format: {"{subset} {parallel}": "1:X"}}; base-tier
keyed "{subset} Base" (row named "Base"). A format where the parallel is
unavailable omits the key (matches 863; never backfilled).
Exclusivity: derived from single-format availability (exactly one non-null
format -> that format's label; else NULL). No cards/players/appearances touched.

Usage: python3 scripts/attach_resurgence_football_2025.py
"""
import json, os, sqlite3

DB = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
DATA = os.path.join(os.path.dirname(__file__), "resurgence_football_2025_odds.jsonl")
SET_ID = 859
FORMATS = ("hobby", "delight", "value", "mega")
EXCL_LABEL = {"hobby": "Hobby", "delight": "Delight", "value": "Value", "mega": "Mega"}
AUTO_FLIP_ID = 2001  # Radial Rookie Relics -> is_autograph = 1

BOX_CONFIG = {
    "hobby": {"cards_per_pack": 6, "packs_per_box": 12, "boxes_per_case": 12,
              "autos_per_box": 1, "rookie_relic_autos_per_box": 1,
              "notes": "1 autograph + 1 rookie relic autograph per box"},
    "mega":  {"cards_per_pack": 8, "packs_per_box": 6, "boxes_per_case": 20},
    "value": {"cards_per_pack": 4, "packs_per_box": 8, "boxes_per_case": 40},
    "delight": {"cards_per_pack": 8, "packs_per_box": 16, "boxes_per_case": None},
}
RELEASE_DATE = "2026-07-31"

GATE = {"Base": 32, "Rookies": 32, "Electro Lights": 1, "Perfect Fits": 1, "Wired": 1,
        "String Theory": 1, "Conductors": 20, "Protonyx": 20, "Voltaic": 20, "Circuit Breakers": 20,
        "Base Signatures": 15, "Rookie Signatures": 20, "Arc Flash Autographs": 8, "Molecular Marks": 8,
        "Neon Initiates": 8, "Thermal Red Ink Autographs": 3, "Resurgence Rookie Relic Signatures": 13,
        "Amped Up Rookie Relic Autographs": 13, "Radial Rookie Relics": 13}


def exclusivity(odds):
    nn = [f for f in FORMATS if odds.get(f) is not None]
    return EXCL_LABEL[nn[0]] if len(nn) == 1 else None


def main():
    rows = [json.loads(l) for l in open(DATA) if l.strip()]
    if len(rows) != 249:
        print(f"STOP: parsed {len(rows)} rows, expected 249."); raise SystemExit(1)

    db = sqlite3.connect(os.path.abspath(DB))
    srow = db.execute("SELECT pack_odds, box_config FROM sets WHERE id=?", (SET_ID,)).fetchone()
    if srow is None:
        print("STOP: set 859 not found."); raise SystemExit(1)
    if srow[0] or srow[1]:
        print(f"STOP: pack_odds/box_config already set (odds={bool(srow[0])}, box={bool(srow[1])})."); raise SystemExit(1)

    # subset name -> insert_set id (must all exist)
    is_id = {n: i for (i, n) in db.execute("SELECT id, name FROM insert_sets WHERE set_id=?", (SET_ID,))}
    missing = [s for s in GATE if s not in is_id]
    if missing:
        print("STOP: subsets missing:", missing); raise SystemExit(1)
    # guard against pre-existing parallels
    n_par = db.execute(
        "SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id WHERE i.set_id=?",
        (SET_ID,)).fetchone()[0]
    if n_par != 0:
        print(f"STOP: set already has {n_par} parallels."); raise SystemExit(1)

    pack = {f: {} for f in FORMATS}
    key_seen = {}
    created = 0
    base_rows = 0

    def put(subset, row_name, odds, is_base):
        key = f"{subset} {row_name}"
        if key in key_seen:
            print(f"STOP: duplicate odds key {key!r}."); raise SystemExit(1)
        key_seen[key] = True
        for f in FORMATS:
            v = odds.get(f)
            if v is not None:
                pack[f][key] = v

    for r in rows:
        sub, par, pr, odds = r["subset"], r["parallel"], r["print_run"], r["odds"]
        iid = is_id[sub]
        if par == "__BASE__":
            row_name, excl = "Base", exclusivity(odds)
            base_rows += 1
        else:
            row_name, excl = par, exclusivity(odds)
        db.execute("INSERT INTO parallels (insert_set_id, name, print_run, exclusivity) VALUES (?,?,?,?)",
                   (iid, row_name, pr, excl))
        created += 1
        put(sub, row_name, odds, par == "__BASE__")

    # write set-level: pack_odds, box_config, release_date
    db.execute("UPDATE sets SET pack_odds=?, box_config=?, release_date=? WHERE id=?",
               (json.dumps(pack), json.dumps(BOX_CONFIG), RELEASE_DATE, SET_ID))
    # autograph flag fix
    before = db.execute("SELECT is_autograph FROM insert_sets WHERE id=?", (AUTO_FLIP_ID,)).fetchone()[0]
    db.execute("UPDATE insert_sets SET is_autograph=1 WHERE id=?", (AUTO_FLIP_ID,))
    after = db.execute("SELECT is_autograph FROM insert_sets WHERE id=?", (AUTO_FLIP_ID,)).fetchone()[0]
    db.commit()

    # ---- reconcile ----------------------------------------------------------
    mism = []
    for subset, gate in GATE.items():
        got = db.execute("SELECT COUNT(*) FROM parallels WHERE insert_set_id=?", (is_id[subset],)).fetchone()[0]
        if got != gate:
            mism.append((subset, gate, got))
    total = db.execute(
        "SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id WHERE i.set_id=?",
        (SET_ID,)).fetchone()[0]
    numbered = db.execute(
        "SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id WHERE i.set_id=? AND p.print_run IS NOT NULL",
        (SET_ID,)).fetchone()[0]

    print(f"Parallel rows created: {created} (expect 249; {base_rows} base-tier + {created-base_rows} concrete)")
    print(f"Total parallels on set: {total} | numbered: {numbered}")
    print(f"pack_odds keys per format: " + ", ".join(f"{f}={len(pack[f])}" for f in FORMATS))
    print(f"box_config set (4 formats); release_date -> {RELEASE_DATE}")
    print(f"Auto-flag flip id {AUTO_FLIP_ID} (Radial Rookie Relics): is_autograph {before} -> {after}")
    excl_counts = {}
    for (n, e) in db.execute(
        "SELECT COALESCE(p.exclusivity,'(all)'), COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id WHERE i.set_id=? GROUP BY p.exclusivity", (SET_ID,)):
        excl_counts[n] = e
    print("exclusivity distribution:", excl_counts)
    if mism:
        print("GATE MISMATCH:")
        for s, g, got in mism: print(f"  {s}: gate={g} db={got}")
        print("STOP."); raise SystemExit(1)
    print("INTEGRITY GATE: all 19 subset parallel counts match. OK.")
    db.close()


if __name__ == "__main__":
    main()
