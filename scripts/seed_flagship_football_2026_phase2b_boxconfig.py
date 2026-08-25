#!/usr/bin/env python3
"""
2026 Topps Flagship Football — Phase 2b: box configs (LOCAL SQLite only; data-only).

Overwrites sets.box_config for set 870 with the seven Tyler-supplied formats and
keeps the four unsupplied format keys present with all-NULL numeric fields.
Idempotent: sets box_config to a fixed value. Migrate to Turso separately.

Hit-guarantee representation (mirrors existing sets / src/components/sets/types.ts):
  Hobby "1 auto OR memorabilia (1 total)" -> autos_or_memorabilia_per_box: 1
  Jumbo "1 auto AND 1 memorabilia"        -> autos_per_box: 1 + memorabilia_per_box: 1
"""
import sqlite3, json, os, sys

SET_ID = 870
DB = os.path.join(os.getcwd(), "the-c-list.db")

BOX_CONFIG = {
    "hobby":     {"cards_per_pack": 12, "packs_per_box": 20, "boxes_per_case": 12, "autos_or_memorabilia_per_box": 1},
    "jumbo":     {"cards_per_pack": 40, "packs_per_box": 10, "boxes_per_case": 6, "autos_per_box": 1, "memorabilia_per_box": 1},
    "value":     {"cards_per_pack": 12, "packs_per_box": 6, "boxes_per_case": 40},
    "mega":      {"cards_per_pack": 15, "packs_per_box": 12, "boxes_per_case": 20},
    "hanger":    {"cards_per_pack": 59, "packs_per_box": 1, "boxes_per_case": 24},
    "fat_pack":  {"cards_per_pack": 36, "packs_per_box": 1, "boxes_per_case": 108},
    "super_box": {"cards_per_pack": 10, "packs_per_box": 14, "boxes_per_case": 12},
    "fanatics":       {"cards_per_pack": None, "packs_per_box": None, "boxes_per_case": None},
    "london_mega":    {"cards_per_pack": None, "packs_per_box": None, "boxes_per_case": None},
    "walmart_mega":   {"cards_per_pack": None, "packs_per_box": None, "boxes_per_case": None},
    "club_super_box": {"cards_per_pack": None, "packs_per_box": None, "boxes_per_case": None},
}

if __name__ == "__main__":
    con = sqlite3.connect(DB)
    cur = con.cursor()
    pack_before = cur.execute("SELECT pack_odds FROM sets WHERE id=?", (SET_ID,)).fetchone()[0]
    cur.execute("UPDATE sets SET box_config=? WHERE id=?", (json.dumps(BOX_CONFIG), SET_ID))
    pack_after = cur.execute("SELECT pack_odds FROM sets WHERE id=?", (SET_ID,)).fetchone()[0]
    assert pack_before == pack_after, "pack_odds changed — aborting"
    assert len(BOX_CONFIG) == 11
    con.commit()
    con.close()
    print("box_config updated (11 format keys, 7 populated, 4 all-NULL); pack_odds unchanged.")
