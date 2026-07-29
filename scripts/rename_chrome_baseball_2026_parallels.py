"""
Seed correction for set 863 (2026 Topps Chrome Baseball): rename BARE parallel
names to their FULL as-printed names (Green -> Green Refractor, etc.), matching
the source doc + set 860 convention. Rename only; touches parallels.name only.

Subset-scoped with a collision guard: never rename onto an existing name in the
same insert_set_id. Exact-match only (no blind suffix rule). X-Fractor rows and
all already-full rows are left untouched. Local SQLite only.

Usage: python3 scripts/rename_chrome_baseball_2026_parallels.py
"""
import os, sqlite3

DB = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
SLUG = "2026-topps-chrome-baseball"

RENAMES = {
    "75th Anniversary": "75th Anniversary Refractor",
    "Aqua": "Aqua Refractor",
    "Aqua Raywave": "Aqua Raywave Refractor",
    "Black": "Black Refractor",
    "Black Raywave": "Black Raywave Refractor",
    "Black Wave": "Black Wave Refractor",
    "Blue": "Blue Refractor",
    "Blue Raywave": "Blue Raywave Refractor",
    "Blue Wave": "Blue Wave Refractor",
    "Gold": "Gold Refractor",
    "Gold Raywave": "Gold Raywave Refractor",
    "Gold Wave": "Gold Wave Refractor",
    "Green": "Green Refractor",
    "Green Raywave": "Green Raywave Refractor",
    "Green Wave": "Green Wave Refractor",
    "Orange": "Orange Refractor",
    "Orange Raywave": "Orange Raywave Refractor",
    "Orange Wave": "Orange Wave Refractor",
    "Pink": "Pink Refractor",
    "Purple": "Purple Refractor",
    "Purple Raywave": "Purple Raywave Refractor",
    "Purple Wave": "Purple Wave Refractor",
    "Red": "Red Refractor",
    "Red Raywave": "Red Raywave Refractor",
    "Red Wave": "Red Wave Refractor",
    "Teal": "Teal Refractor",
    "White": "White Refractor",
    "Yellow": "Yellow Refractor",
}


def main():
    db = sqlite3.connect(os.path.abspath(DB))

    row = db.execute("SELECT id FROM sets WHERE slug=?", (SLUG,)).fetchone()
    if not row:
        print(f"STOP: set '{SLUG}' not found."); raise SystemExit(1)
    set_id = row[0]
    print(f"Set id: {set_id}")

    total_before = db.execute(
        "SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON p.insert_set_id=i.id WHERE i.set_id=?",
        (set_id,)).fetchone()[0]
    print(f"Total parallel rows: {total_before} (expect 260)")
    if total_before != 260:
        print("STOP: unexpected parallel-row count."); raise SystemExit(1)

    # rows eligible for rename (name exactly matches a 'from')
    targets = db.execute(
        """SELECT p.id, p.insert_set_id, i.name, p.name
           FROM parallels p JOIN insert_sets i ON p.insert_set_id=i.id
           WHERE i.set_id=? AND p.name IN ({})""".format(",".join("?" * len(RENAMES))),
        (set_id, *RENAMES.keys())).fetchall()

    # collision guard: does the 'to' name already exist in the SAME subset?
    collisions = []
    for pid, is_id, subset, frm in targets:
        to = RENAMES[frm]
        exists = db.execute(
            "SELECT 1 FROM parallels WHERE insert_set_id=? AND name=?", (is_id, to)).fetchone()
        if exists:
            collisions.append((subset, frm, to))
    if collisions:
        print("STOP: rename-target collisions (target name already exists in same subset):")
        for subset, frm, to in collisions:
            print(f"  [{subset}] {frm!r} -> {to!r}")
        print("No renames performed."); raise SystemExit(1)

    # apply renames (rename only; name column only)
    renamed = 0
    for pid, is_id, subset, frm in targets:
        db.execute("UPDATE parallels SET name=? WHERE id=?", (RENAMES[frm], pid))
        renamed += 1
    db.commit()

    # ---- count gate ----------------------------------------------------------
    total_after = db.execute(
        "SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON p.insert_set_id=i.id WHERE i.set_id=?",
        (set_id,)).fetchone()[0]
    untouched = total_after - renamed
    remaining_bare = db.execute(
        """SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON p.insert_set_id=i.id
           WHERE i.set_id=? AND p.name IN ({})""".format(",".join("?" * len(RENAMES))),
        (set_id, *RENAMES.keys())).fetchone()[0]

    print(f"\nRows renamed: {renamed} (expect 206)")
    print(f"Rows untouched: {untouched} (expect 54)")
    print(f"Total rows after: {total_after} (expect 260, unchanged)")
    print(f"Collisions hit: {len(collisions)} (expect 0)")
    print(f"Bare 'from' names remaining in set: {remaining_bare} (expect 0)")

    ok = (renamed == 206 and untouched == 54 and total_after == 260
          and len(collisions) == 0 and remaining_bare == 0)
    print("\nGATE:", "PASS" if ok else "FAIL — investigate")
    if not ok:
        raise SystemExit(1)
    db.close()


if __name__ == "__main__":
    main()
