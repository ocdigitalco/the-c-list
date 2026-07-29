"""
Attach pack odds to 2026 Topps Chrome Baseball (set 863). Local SQLite only.

Model (verified against precedent set 860):
  * Odds live in sets.pack_odds as nested JSON {format: {"{subset} {parallel}": "1:X"}}.
  * The UI resolves each parallel ROW via lookupOddsValue(subset, row.name) ->
    key "{subset} {row.name}", so keys are built from parallel row names.
  * A format where the parallel is unavailable => key OMITTED from that format
    object (860 stores no explicit nulls; app reads via `!= null`). Never backfill.
  * Four formats only: hobby, jumbo, value, mega (Breaker/Fanatics dropped).

Row handling:
  * create_and_attach (24): create parallel row (print_run NULL) if absent, then key odds.
  * __BASE__ (46): ensure a "Base" parallel row exists in the subset (create print_run
    NULL if absent); key odds under "{subset} Base".
  * attach concrete (244): must map to an existing parallel row by exact name; else STOP.

Usage: python3 scripts/attach_chrome_baseball_2026_odds.py
"""
import json, os, sqlite3

DB = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
DATA = os.path.join(os.path.dirname(__file__), "chrome_baseball_2026_odds.jsonl")
SLUG = "2026-topps-chrome-baseball"
FORMATS = ("hobby", "jumbo", "value", "mega")


def main():
    rows = [json.loads(l) for l in open(DATA) if l.strip()]
    n_attach = sum(1 for r in rows if r["action"] == "attach")
    n_create = sum(1 for r in rows if r["action"] == "create_and_attach")
    if len(rows) != 314 or n_attach != 290 or n_create != 24:
        print(f"STOP: parsed {len(rows)} rows ({n_attach} attach / {n_create} create), expected 314/290/24.")
        raise SystemExit(1)

    db = sqlite3.connect(os.path.abspath(DB))
    srow = db.execute("SELECT id, pack_odds FROM sets WHERE slug=?", (SLUG,)).fetchone()
    if not srow:
        print(f"STOP: set '{SLUG}' not found."); raise SystemExit(1)
    set_id, existing_odds = srow
    if existing_odds:
        print("STOP: pack_odds already set — refusing to overwrite."); raise SystemExit(1)

    # subset name -> insert_set id
    is_id = {n: i for (i, n) in db.execute("SELECT id, name FROM insert_sets WHERE set_id=?", (set_id,))}
    want_subsets = sorted(set(r["subset"] for r in rows))
    missing = [s for s in want_subsets if s not in is_id]
    if missing:
        print("STOP: target subsets missing:", missing); raise SystemExit(1)

    def row_names(sub):
        return set(n for (n,) in db.execute(
            "SELECT name FROM parallels WHERE insert_set_id=?", (is_id[sub],)))

    pack = {f: {} for f in FORMATS}
    created_parallels = 0     # create_and_attach
    base_rows_created = 0     # __BASE__ ensure "Base" row
    attached = 0
    unmapped = []             # attach rows with no matching parallel (should be 0)
    key_seen = {}             # collision guard on odds keys

    def put_key(subset, row_name, odds, src):
        key = f"{subset} {row_name}"
        if key in key_seen:
            print(f"STOP: duplicate odds key {key!r} (src {src!r} vs {key_seen[key]!r})."); raise SystemExit(1)
        key_seen[key] = src
        for f in FORMATS:
            v = odds.get(f)
            if v is not None:                     # omit unavailable formats (never backfill)
                pack[f][key] = v

    for r in rows:
        sub, par, act, odds, src = r["subset"], r["parallel"], r["action"], r["odds"], r["source_row"]
        iid = is_id[sub]

        if act == "create_and_attach":
            if par not in row_names(sub):
                db.execute("INSERT INTO parallels (insert_set_id, name, print_run, exclusivity) VALUES (?,?,NULL,NULL)",
                           (iid, par))
                created_parallels += 1
            put_key(sub, par, odds, src)
            attached += 1

        elif par == "__BASE__":
            if "Base" not in row_names(sub):
                db.execute("INSERT INTO parallels (insert_set_id, name, print_run, exclusivity) VALUES (?,?,NULL,NULL)",
                           (iid, "Base"))
                base_rows_created += 1
            put_key(sub, "Base", odds, src)
            attached += 1

        else:  # attach concrete — must already exist
            if par not in row_names(sub):
                unmapped.append((sub, par, src)); continue
            put_key(sub, par, odds, src)
            attached += 1

    if unmapped:
        print("STOP: attach rows with no matching parallel row:")
        for s, p, src in unmapped:
            print(f"  [{s}] {p!r}  (src {src})")
        raise SystemExit(1)

    db.execute("UPDATE sets SET pack_odds=? WHERE id=?", (json.dumps(pack), set_id))
    db.commit()

    # ---- reconcile / report -------------------------------------------------
    print(f"Rows processed: {len(rows)} (expect 314)")
    print(f"  attach: {n_attach} (expect 290) | create_and_attach: {n_create} (expect 24)")
    print(f"Parallels created (create_and_attach): {created_parallels} (expect 24)")
    print(f"Base rows created (__BASE__ tiers): {base_rows_created}")
    print(f"Odds rows attached: {attached} (expect 314)")
    print(f"Distinct odds keys: {len(key_seen)}")
    for f in FORMATS:
        print(f"  {f}: {len(pack[f])} keys")
    ok = (created_parallels == 24 and attached == 314 and not unmapped)
    print("\nGATE:", "PASS" if ok else "FAIL")
    if not ok:
        raise SystemExit(1)

    # subsets left odds-less (of all 54)
    all_subsets = set(is_id)
    touched = set(want_subsets)
    print("\nSubsets touched:", len(touched), "of 54")
    print("Subsets with NO odds:", sorted(all_subsets - touched))
    db.close()


if __name__ == "__main__":
    main()
