"""
Attach numbered parallels to 2026 Topps Finest Baseball (set 852).

Numbered parallels ONLY (serial-numbered). No pack odds in this pass.
Maps to EXISTING subsets only — never creates a subset; anything that does not
resolve is reported and skipped.

Data: scripts/finest_baseball_2026_parallels.jsonl (221 rows).
Usage: python3 scripts/add_finest_baseball_2026_numbered_parallels.py
Local SQLite only. Migrate to Turso separately.
"""
import json
import os
import sys
import collections

SET_ID = 852
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
DATA_PATH = os.path.join(os.path.dirname(__file__), "finest_baseball_2026_parallels.jsonl")

# Data subset name -> actual DB subset name (only where they differ).
# Base tiers use the DB's non-dash form; two subsets normalize spelling.
SUBSET_MAP = {
    "Base – Common": "Base Common",
    "Base – Uncommon": "Base Uncommon",
    "Base – Rare": "Base Rare",
    "Base – Super Rare": "Base Super Rare",
    "Finest Rookie Patch Autographs": "Finest Rookie Patch Autograph",  # DB: singular
    "World's Finest": "Worlds Finest",  # DB: no apostrophe
}


def serial_to_print_run(serial: str) -> int:
    s = serial.strip()
    if s == "1/1":
        return 1
    if s.startswith("/"):
        return int(s[1:])
    raise ValueError(f"Unparseable serial: {serial!r}")


def main():
    import sqlite3

    rows = []
    with open(DATA_PATH) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))

    if len(rows) != 221:
        print(f"STOP: parsed {len(rows)} rows, expected 221.")
        sys.exit(1)

    db = sqlite3.connect(os.path.abspath(DB_PATH))

    # Resolve every distinct subset to a DB insert_set id up front.
    is_id_cache = {}
    unmapped = []
    for data_name in sorted({r["subset"] for r in rows}):
        db_name = SUBSET_MAP.get(data_name, data_name)
        row = db.execute(
            "SELECT id FROM insert_sets WHERE set_id = ? AND name = ?", (SET_ID, db_name)
        ).fetchone()
        if row:
            is_id_cache[data_name] = row[0]
        else:
            unmapped.append((data_name, db_name))

    if unmapped:
        print("SKIP-AND-REPORT — these subsets did not resolve to an existing DB subset:")
        for data_name, db_name in unmapped:
            print(f"  '{data_name}' -> '{db_name}' (NOT FOUND)")
        print("Aborting without writing (never create subsets).")
        sys.exit(1)

    added, skipped = 0, 0
    for r in rows:
        is_id = is_id_cache[r["subset"]]
        name = r["parallel"]
        print_run = serial_to_print_run(r["serial"])
        exists = db.execute(
            "SELECT 1 FROM parallels WHERE insert_set_id = ? AND name = ?", (is_id, name)
        ).fetchone()
        if exists:
            skipped += 1
            continue
        db.execute(
            "INSERT INTO parallels (insert_set_id, name, print_run) VALUES (?, ?, ?)",
            (is_id, name, print_run),
        )
        added += 1

    db.commit()
    print(f"\nInserted {added} parallels, skipped {skipped} existing.")

    # Report actual DB counts per subset.
    print("\nActual parallel counts per subset (set 852):")
    got = collections.OrderedDict()
    for data_name in sorted(is_id_cache, key=lambda n: is_id_cache[n]):
        is_id = is_id_cache[data_name]
        db_name = SUBSET_MAP.get(data_name, data_name)
        n = db.execute(
            "SELECT COUNT(*) FROM parallels WHERE insert_set_id = ?", (is_id,)
        ).fetchone()[0]
        got[data_name] = n
        tag = "" if db_name == data_name else f"  (DB: '{db_name}')"
        print(f"  {data_name:42s} {n}{tag}")
    print(f"\nTOTAL parallels on set 852: {sum(got.values())}")
    db.close()


if __name__ == "__main__":
    main()
