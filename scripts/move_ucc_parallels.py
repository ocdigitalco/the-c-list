"""
Move insert sets and parallels from set 839 to set 43,
creating missing insert sets as needed. Then delete set 839.
"""
import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
db = sqlite3.connect(DB_PATH)
db.execute("PRAGMA journal_mode=WAL")
db.execute("PRAGMA foreign_keys=OFF")

SOURCE_SET_ID = 839
TARGET_SET_ID = 43

# Get all insert sets from source
source_insert_sets = db.execute(
    "SELECT id, name FROM insert_sets WHERE set_id = ?",
    (SOURCE_SET_ID,)
).fetchall()
print(f"Source insert sets (set {SOURCE_SET_ID}): {len(source_insert_sets)}")

moved_parallels = 0
created_insert_sets = 0
skipped_parallels = 0

for src_id, src_name in source_insert_sets:
    # Find or create matching insert set in target
    target = db.execute(
        "SELECT id FROM insert_sets WHERE set_id = ? AND name = ?",
        (TARGET_SET_ID, src_name)
    ).fetchone()

    if target:
        target_id = target[0]
    else:
        # Create the insert set in set 43
        db.execute(
            "INSERT INTO insert_sets (set_id, name) VALUES (?, ?)",
            (TARGET_SET_ID, src_name)
        )
        target_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        created_insert_sets += 1
        print(f"  CREATED insert set '{src_name}' (ID {target_id}) in set {TARGET_SET_ID}")

    # Get parallels from source insert set
    parallels = db.execute(
        "SELECT name, print_run FROM parallels WHERE insert_set_id = ?",
        (src_id,)
    ).fetchall()

    for p_name, p_print_run in parallels:
        # Check if parallel already exists in target
        exists = db.execute(
            "SELECT id FROM parallels WHERE insert_set_id = ? AND name = ?",
            (target_id, p_name)
        ).fetchone()

        if exists:
            skipped_parallels += 1
            continue

        db.execute(
            "INSERT INTO parallels (insert_set_id, name, print_run) VALUES (?, ?, ?)",
            (target_id, p_name, p_print_run)
        )
        moved_parallels += 1

    if parallels:
        print(f"  {src_name}: {len(parallels)} parallels → target ID {target_id}")

db.commit()
print(f"\nCreated {created_insert_sets} new insert sets in set {TARGET_SET_ID}")
print(f"Moved {moved_parallels} parallels, skipped {skipped_parallels} (already existed)")

# Delete set 839
print(f"\nDeleting set {SOURCE_SET_ID}...")
db.execute("DELETE FROM parallels WHERE insert_set_id IN (SELECT id FROM insert_sets WHERE set_id = ?)", (SOURCE_SET_ID,))
db.execute("DELETE FROM insert_sets WHERE set_id = ?", (SOURCE_SET_ID,))
db.execute("DELETE FROM sets WHERE id = ?", (SOURCE_SET_ID,))
db.commit()
print(f"Set {SOURCE_SET_ID} deleted.")

# Verify
is_count = db.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id = ?", (TARGET_SET_ID,)).fetchone()[0]
par_count = db.execute("SELECT COUNT(*) FROM parallels WHERE insert_set_id IN (SELECT id FROM insert_sets WHERE set_id = ?)", (TARGET_SET_ID,)).fetchone()[0]
gone = db.execute("SELECT COUNT(*) FROM sets WHERE id = ?", (SOURCE_SET_ID,)).fetchone()[0]
print(f"\nSet {TARGET_SET_ID} now has {is_count} insert sets, {par_count} parallels")
print(f"Set {SOURCE_SET_ID} exists: {gone == 1}")

db.close()
print("Done.")
