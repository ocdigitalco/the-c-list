#!/usr/bin/env python3
"""Phase 3 DB writer — LOCAL the-c-list.db only, single transaction, gates before commit."""
import sqlite3, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(os.getcwd(), "the-c-list.db")
SET_ID = 870
b = json.load(open(os.path.join(HERE, "build.json")))
pack = b["pack"]; inserts = b["inserts"]; notes = b["notes"]
EXPECT_KEYS = b["distinct_keys"]  # 829

con = sqlite3.connect(DB); cur = con.cursor()
subid = {row[0]: row[1] for row in cur.execute("SELECT name,id FROM insert_sets WHERE set_id=?", (SET_ID,))}

# capture invariants BEFORE
before = {
 "cards": cur.execute("SELECT COUNT(*) FROM (SELECT DISTINCT pa.insert_set_id,pa.card_number FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id WHERE i.set_id=?)", (SET_ID,)).fetchone()[0],
 "appearances": cur.execute("SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id WHERE i.set_id=?", (SET_ID,)).fetchone()[0],
 "subsets": cur.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id=?", (SET_ID,)).fetchone()[0],
 "parallels": cur.execute("SELECT COUNT(*) FROM parallels par JOIN insert_sets i ON i.id=par.insert_set_id WHERE i.set_id=?", (SET_ID,)).fetchone()[0],
 "pr_subsets": cur.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND print_run IS NOT NULL", (SET_ID,)).fetchone()[0],
}
print("BEFORE:", before)

try:
    # 1) insert new parallels
    for ins in inserts:
        sid = subid[ins["subset"]]
        cur.execute("INSERT INTO parallels(insert_set_id,name,print_run,exclusivity,note) VALUES(?,?,?,?,?)",
                    (sid, ins["parallel"], None, None, ins["note"]))
    # 2) note the two accepted no-odds existing parallels
    for sub, par in [("Team Cards", "Sandglitter Red"), ("NFL Material Dual Relic Autographs", "Foilfractor")]:
        cur.execute("UPDATE parallels SET note=? WHERE insert_set_id=? AND name=?",
                    ("no odds published on official Topps sheet", subid[sub], par))
    # 3) replace pack_odds wholesale (verbatim strings)
    cur.execute("UPDATE sets SET pack_odds=? WHERE id=?", (json.dumps(pack), SET_ID))
    # 4) box_config: keep existing, add 9 presence-only formats
    bc = json.loads(cur.execute("SELECT box_config FROM sets WHERE id=?", (SET_ID,)).fetchone()[0])
    NEW_FMT = ["hobby_silver_pack","jumbo_silver_pack","super_box_oversized","bulk_packs",
               "club_super_box_oversized","kids_mega","club_ex_box_sams","club_ex_box_sams_oversized","gc_white_slip_sheets"]
    for f in NEW_FMT:
        bc.setdefault(f, {"cards_per_pack": None, "packs_per_box": None, "boxes_per_case": None})
    cur.execute("UPDATE sets SET box_config=? WHERE id=?", (json.dumps(bc), SET_ID))
    # 5) insert_sets.notes for the 4 notes-only subsets (replace)
    for sub, lines in notes.items():
        cur.execute("UPDATE insert_sets SET notes=? WHERE id=?", (" | ".join(lines), subid[sub]))

    # ---- GATES (before commit) ----
    after = {
     "cards": cur.execute("SELECT COUNT(*) FROM (SELECT DISTINCT pa.insert_set_id,pa.card_number FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id WHERE i.set_id=?)", (SET_ID,)).fetchone()[0],
     "appearances": cur.execute("SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id WHERE i.set_id=?", (SET_ID,)).fetchone()[0],
     "subsets": cur.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id=?", (SET_ID,)).fetchone()[0],
     "parallels": cur.execute("SELECT COUNT(*) FROM parallels par JOIN insert_sets i ON i.id=par.insert_set_id WHERE i.set_id=?", (SET_ID,)).fetchone()[0],
     "pr_subsets": cur.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND print_run IS NOT NULL", (SET_ID,)).fetchone()[0],
    }
    print("AFTER: ", after)
    coplayer = after["appearances"] - after["cards"]
    G = []
    G.append(("cards 4042", after["cards"] == 4042))
    G.append(("subsets 87", after["subsets"] == 87))
    G.append(("co-player 129", coplayer == 129))
    G.append(("print_run subsets 17 (unchanged)", after["pr_subsets"] == 17 == before["pr_subsets"]))
    G.append(("cards unchanged", after["cards"] == before["cards"]))
    G.append(("appearances unchanged", after["appearances"] == before["appearances"]))
    G.append(("parallels 787", after["parallels"] == 787))
    # pack_odds distinct keys
    po = json.loads(cur.execute("SELECT pack_odds FROM sets WHERE id=?", (SET_ID,)).fetchone()[0])
    keys = set()
    for d in po.values(): keys.update(d.keys())
    G.append((f"pack_odds distinct keys == {EXPECT_KEYS}", len(keys) == EXPECT_KEYS))
    # spot asserts
    def g(fk, k): return po.get(fk, {}).get(k)
    for fk, k, exp in [("hobby","Base Cards I Rainbow Foil","1:68"),("hobby","Future Stars Rainbow Foil","1:406"),
                       ("hobby","Rookies Rainbow Foil","1:41"),("hobby","Real One Autographs Base","1:3,181"),
                       ("fanatics","Rookie Real One Autographs Base","1:568,182"),
                       ("hobby_silver_pack","1991 Topps Football Chrome Base Cards Superfractor","1:6,556"),
                       ("london_mega","Base Cards I Union Jack Rainbow Foil","1:1")]:
        G.append((f"spot {fk}|{k}=={exp}", g(fk, k) == exp))
    G.append(("Marketing Card not a subset", "Marketing Card" not in subid))
    # referential: every key resolves to existing subset+parallel (or Base)
    parset = {}
    for (sn, pn) in cur.execute("SELECT i.name,par.name FROM insert_sets i LEFT JOIN parallels par ON par.insert_set_id=i.id WHERE i.set_id=?", (SET_ID,)):
        parset.setdefault(sn, set()).add(pn)
    subnames = set(subid.keys())
    # sort subset names longest-first to split "subset parallel"
    order = sorted(subnames, key=len, reverse=True)
    bad = 0
    for k in keys:
        matched = False
        for sn in order:
            if k == sn + " Base":
                matched = (sn in subnames); break
            if k.startswith(sn + " "):
                pn = k[len(sn)+1:]
                matched = pn in parset.get(sn, set()); break
        if not matched: bad += 1
    G.append(("referential: all keys resolve (0 bad)", bad == 0))
    # box_config keys
    G.append(("box_config 20 keys", len(bc) == 20))

    allok = all(ok for _, ok in G)
    for name, ok in G:
        print(f"  [{'OK' if ok else 'FAIL'}] {name}")
    if not allok:
        con.rollback(); print("\nGATE FAILURE -> ROLLED BACK, no changes written."); sys.exit(1)
    con.commit()
    print("\nAll gates pass. COMMITTED to local DB. parallels=%d pack_keys=%d" % (after["parallels"], len(keys)))
except Exception as e:
    con.rollback(); print("ERROR -> rolled back:", e); raise
finally:
    con.close()
