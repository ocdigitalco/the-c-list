#!/usr/bin/env python3
"""
2026 Topps Flagship Football — Phase 2: attach parallels + odds (LOCAL SQLite only).

Attach-only. Does NOT touch cards, subset card membership, or co-player rows.
- parallel rows  -> parallels(insert_set_id, name, print_run, note)
- odds           -> sets.pack_odds JSON: {format: {"<DBsubset> <Parallel>" | "<DBsubset> Base": "1:X"}}
- numbered parent-> insert_sets.print_run  (META numbered_parent)
- subset notes   -> insert_sets.notes      (META note/dq + GMIV tier notes)
- box configs    -> sets.box_config: add 7 new format keys (presence-only)
- 1957 Rookie Variation: existing subset (2275) -> attach odds + set is_base=1 (do NOT create/insert cards)

Usage: python3 scripts/seed_flagship_football_2026_phase2.py <data_dir>   (<data_dir>/data.jsonl)
"""
import json, os, sqlite3, sys, re, collections

SET_ID = 870
DB = os.path.join(os.getcwd(), "the-c-list.db")

FMT_KEY = {
    "Hobby": "hobby", "Jumbo": "jumbo", "Hanger": "hanger", "Fat Pack": "fat_pack",
    "Value": "value", "Mega": "mega", "Fanatics": "fanatics",
    "London Mega": "london_mega", "Walmart Mega": "walmart_mega",
}
NEW_BOX_FORMATS = ["hanger", "fat_pack", "fanatics", "london_mega", "walmart_mega", "super_box", "club_super_box"]

BASE_NUMBERED_DB = ["Base Cards I", "Future Stars", "Team Cards", "League Leaders", "Combo Cards", "Rookies"]

# DATA subset name -> DB subset name(s). Variation families map to base+rookie.
EXPLICIT_MAP = {
    "Base Cards I": ["Base Cards I"],  # builder fans out to all six base-numbered
    "Base – Vintage Stock Variation": ["Base Cards Vintage Stock Variation", "Rookie Card Vintage Stock Variation"],
    "Base – Clear Variation": ["Base Cards Clear Variation", "Rookie Card Clear Variation"],
    "Base – Team Color Border Variation": ["Base Cards Team Color Border Variations", "Rookie Card Team Color Border Variation"],
    "Base – Player Number Variation": ["Base Cards Player Number Variations", "Rookie Card Player Number Variations"],
    "Base – True Photo Variation": ["Base Cards True Photo Variations", "Rookie Card True Photo Variation"],
    "1957 Rookie Variation": ["1957 Rookie Variation"],
    "Real One Autographs": ["Real One Autographs"],
    "Rookie Real One Autographs": ["Rookie Real One Autographs"],
    "Flagship First Signatures": ["Flagship First Signatures"],
    "Flagship First Dual Signatures": ["Flagship First Dual Signatures"],
    "NFL Stars Autographs": ["NFL Stars Autographs"],
    "NFL Stars Dual Autographs": ["NFL Stars Dual Autographs"],
    "NFL Stars Triple Autographs": ["NFL Stars Triple Autographs"],
    "1991 Topps Football Autographs": ["1991 Topps Football Autograph Cards"],
    "1991 Topps Football Rookie Autographs": ["1991 Topps Football Rookie Autograph Cards"],
    "1991 Super Rookies Autographs": ["1991 Super Rookies Autographs"],
    "Victory Ink": ["Victory Ink"],
    "Mascot Autographs": ["Mascot Autographs"],
    "Island Ink": ["Island Ink"],
    "2025 All Topps Team Autographs": ["2025 All Topps Team Autographs"],
    "Super Bowl Champion Signatures": ["Super Bowl Champion Signatures"],
    "Ring Of Honor Signatures": ["Ring of Honor Signatures"],
    "Rookie Premiere Autographs": ["Rookie Premiere Autographs"],
    "NFL Material Autographs": ["NFL Material Autograph Cards"],
    "NFL Rookie Material Autographs": ["NFL Rookie Material Autograph Cards"],
    "NFL Material Dual Relic Autographs": ["NFL Material Dual Relic Autographs"],
    "Field Fit Swatch Collection Autograph Relics": ["Field Fit Swatch Collection Autograph Relic"],
    "Topps Autograph Patch Cards": ["Topps Autograph Patch Cards"],
    "Topps Autograph Rookie Patch Cards": ["Topps Autograph Rookie Patch Cards"],
    "Real One Relics": ["Real One Relics"],
    "Rookie Real One Relics": ["Rookie Real One Relics"],
    "NFL Material": ["NFL Material Cards"],
    "NFL Rookies Material": ["NFL Rookies Material Cards"],
    "NFL Material Dual Relics": ["NFL Material Dual Relic Cards"],
    "Field Fit Swatch Collection": ["Field Fit Swatch Collection"],
    "1991 Topps Football Relics": ["1991 Topps Football Relics"],
    "1991 Topps Football Rookie Relics": ["1991 Topps Football Rookie Relics"],
    "2025 All Topps Team": ["2025 All Topps Team"],
    "Ring Of Honor": ["Ring of Honor"],
    "Topps Profiles": ["Topps Profiles"],
    "Big Ticket Players": ["Big Ticket Players"],
    "2025 Greatest Hits": ["2025 Greatest Hits"],
    "Class Of ’26": ["Class of 26"],
    "Touchdown Machines": ["Touchdown Machines"],
    "1000 Yard Club": ["1000 Yard Club"],
    "4000 Yard Club": ["4000 Yard Club"],
    "Wild Card Moments": ["Wild Card Moments"],
    "Divisional Dominance": ["Divisional Dominance"],
    "Conference Kings": ["Conference Kings"],
    "All Hail The Champ": ["All Hail the Champ"],
    "1991 Topps Football": ["1991 Topps Football"],
    "1991 Topps Football Chrome": ["1991 Topps Football Chrome Base Cards"],
    "1991 Topps Rookies Football": ["1991 Topps Rookies Football"],
    "1991 Topps Rookies Football Chrome": ["1991 Topps Rookies Football Chrome Base Cards"],
    "NFL Stars": ["NFL Stars"],
    "Pressure Cookers": ["Pressure Cookers"],
    "Greats Of The Game": ["Greats of the Game"],
    "Struttin’": ["Struttin"],
    "Billboard Material": ["Billboard Material"],
    "Touchdown": ["Touchdown"],
    "All Kings": ["All Kings"],
    "Fanatics Authentics Redemptions": ["Fanatics Authentic Redemptions Cards"],
}
SKIP_SUBSETS = {"Base – Golden Mirror Variations"}  # handled by GMIV block

# META (numbered_parent -> print_run; note/dq -> notes)
META = {
    "Real One Autographs": {"numbered_parent": 250},
    "Rookie Real One Autographs": {"numbered_parent": 250},
    "NFL Stars Dual Autographs": {"numbered_parent": 10},
    "NFL Stars Triple Autographs": {"numbered_parent": 5},
    "2025 All Topps Team Autographs": {"numbered_parent": 250},
    "NFL Material Autographs": {"numbered_parent": 99},
    "NFL Rookie Material Autographs": {"numbered_parent": 99},
    "NFL Material Dual Relic Autographs": {"numbered_parent": 250, "note": "Parallels published without odds"},
    "Field Fit Swatch Collection Autograph Relics": {"numbered_parent": 99, "dq": "Base odds identical to NFL Material Autographs in source — stored verbatim"},
    "Topps Autograph Patch Cards": {"numbered_parent": 99},
    "Topps Autograph Rookie Patch Cards": {"numbered_parent": 99},
    "Base – Vintage Stock Variation": {"numbered_parent": 99},
    "Base – Clear Variation": {"numbered_parent": 10},
    "Base – Player Number Variation": {"numbered_parent": 20},
    "1991 Topps Football Chrome": {"note": "Hobby/Jumbo Silver Pack Exclusive — parallel odds are Silver Pack odds attached to Hobby/Jumbo"},
    "1991 Topps Rookies Football Chrome": {"note": "Hobby/Jumbo Silver Pack Exclusive — parallel odds are Silver Pack odds attached to Hobby/Jumbo"},
    "All Kings": {"note": "Conflicting odds provided by Topps — no base odds published; unnumbered base plus Gold 1/1 (Hobby/Jumbo exclusive)"},
    "Rookie Premiere Autographs": {"note": "Green Ink / Red Ink are versions, not parallels; no base line, no print runs published"},
    "Flagship First Dual Signatures": {"dq": "Odds identical to Flagship First Signatures in source — stored verbatim"},
    "1991 Super Rookies Autographs": {"dq": "Base odds identical to own Orange /25 and to 2025 All Topps Team Autographs base odds in source — stored verbatim"},
    "1991 Topps Football Rookie Relics": {"dq": "Parallel odds identical to NFL Rookies Material (except Platinum) in source — stored verbatim"},
    "NFL Material Dual Relics": {"dq": "Fat Pack 1:38,775 is an outlier vs other columns in source — stored verbatim"},
    "Pressure Cookers": {"dq": "Source lists Red Crackle /5 but no Red /5; not inferred"},
    "Fanatics Authentics Redemptions": {"note": "Source card list truncates after FAR-1"},
    "Base – Golden Mirror Variations": {"note": "Source publishes one 400-card line (= Insider Tier I); Insider tier lines attached per GMIV block"},
    "1957 Rookie Variation": {"note": "NEW subset this pass; 50-card checklist supplied by Tyler, odds from source 2"},
}

# GMIV block (Checklist Insider). odds -> Tier I; tiers II/III -> notes on Golden Mirror Image Variations.
GMIV_TIER1 = {"Hobby": "1:3,444", "Jumbo": "1:689", "Value": "1:4,133", "Mega": "1:4,133", "Fanatics": "1:3,100", "Hanger": "1:689", "Fat Pack": "1:1,378", "London Mega": "1:4,133"}
GMIV_TIER2 = "Tier II: Hobby 1:5,166; Jumbo 1:1,034; Value 1:6,199; Mega 1:6,199; Fanatics 1:4,650; Hanger 1:1,034; Fat Pack 1:2,067"
GMIV_TIER3 = "Tier III: Hobby 1:17,218; Jumbo 1:3,444; Value 1:20,662; Mega 1:20,662; Fanatics 1:15,497; Hanger 1:3,444; Fat Pack 1:6,888"
GMIV_ROOKIE = {"Hobby": "1:20,683", "Jumbo": "1:4,137", "Value": "1:24,821", "Mega": "1:24,821", "Fanatics": "1:18,616", "Hanger": "1:4,137", "Fat Pack": "1:8,274"}
GMIV_THEMED = {"Hobby": "1:34,495", "Jumbo": "1:6,900", "Value": "1:41,391", "Mega": "1:41,391", "Fanatics": "1:31,047", "Hanger": "1:6,900", "Fat Pack": "1:13,799"}


def norm(s):
    return re.sub(r"\s+", " ", s.lower().replace("’", "'").replace("'", "")).strip()


def main():
    data_dir = sys.argv[1]
    recs = []
    with open(os.path.join(data_dir, "data.jsonl")) as f:
        for ln in f:
            ln = ln.strip()
            if ln:
                recs.append(json.loads(ln))

    con = sqlite3.connect(DB)
    cur = con.cursor()

    # DB subset name -> insert_set id
    sid = {name: iid for iid, name in cur.execute(
        "SELECT id, name FROM insert_sets WHERE set_id=?", (SET_ID,)).fetchall()}
    norm_to_db = {norm(n): n for n in sid}

    # ── build DATA subset -> [DB subset names] map, halt if unmapped ──────────
    def map_subset(data_name):
        if data_name in SKIP_SUBSETS:
            return []
        if data_name in EXPLICIT_MAP:
            return EXPLICIT_MAP[data_name]
        db = norm_to_db.get(norm(data_name))
        return [db] if db else None

    data_subsets = sorted({r["subset"] for r in recs})
    print("===== NAME MAP (DATA subset -> DB subset[s]) =====")
    unmapped = []
    for ds in data_subsets:
        tgt = map_subset(ds)
        if tgt is None or any(t not in sid for t in (tgt or [])):
            unmapped.append(ds)
        label = "SKIP (GMIV block)" if ds in SKIP_SUBSETS else (tgt if tgt else "!! UNMAPPED")
        # base-numbered fan-out note
        if ds == "Base Cards I":
            label = BASE_NUMBERED_DB
        print(f"  {ds!r:55s} -> {label}")
    if unmapped:
        con.close(); sys.exit(f"HALT: unmapped/ambiguous DATA subsets: {unmapped}")

    # DB subsets receiving nothing (informational)
    receiving = set()
    GMIV_DB = ["Golden Mirror Image Variations", "Golden Mirror Rookie Image Variations",
               "Future Stars Golden Mirror Image Variations", "Team Cards Golden Mirror Image Variations",
               "League Leaders Golden Mirror Image Variations", "Combo Cards Golden Mirror Image Variations"]
    for ds in data_subsets:
        if ds in SKIP_SUBSETS: continue
        tgt = BASE_NUMBERED_DB if ds == "Base Cards I" else map_subset(ds)
        receiving.update(tgt)
    receiving.update(GMIV_DB)
    print("\n  DB subsets receiving NOTHING (expected):", sorted(set(sid) - receiving))

    # ── apply ─────────────────────────────────────────────────────────────────
    pack = {}  # format_key -> {oddskey: oddsstr}
    subset_notes = collections.defaultdict(list)   # db subset -> [notes]
    subset_printrun = {}                           # db subset -> print_run
    n_parallel_rows = 0
    odds_keys_expected = set()

    def add_odds(dbsubset, keysuffix, odds):
        # keysuffix: parallel name, or "Base"
        key = f"{dbsubset} {keysuffix}"
        if odds:
            odds_keys_expected.add((None, key))  # logical distinct key
        for fmt, val in odds.items():
            fk = FMT_KEY[fmt]
            pack.setdefault(fk, {})[key] = val

    for r in recs:
        ds = r["subset"]
        if ds in SKIP_SUBSETS:
            continue
        targets = BASE_NUMBERED_DB if ds == "Base Cards I" else map_subset(ds)
        for db in targets:
            iid = sid[db]
            if r["parallel"] is None:
                add_odds(db, "Base", r["odds"])
            else:
                cur.execute(
                    "INSERT INTO parallels (insert_set_id, name, print_run, note) VALUES (?,?,?,?)",
                    (iid, r["parallel"], r["print_run"], r["note"]))
                n_parallel_rows += 1
                add_odds(db, r["parallel"], r["odds"])

    # ── GMIV block ─────────────────────────────────────────────────────────────
    add_odds("Golden Mirror Image Variations", "Base", GMIV_TIER1)
    subset_notes["Golden Mirror Image Variations"].append("Tier I published; tier membership unknown")
    subset_notes["Golden Mirror Image Variations"].append(GMIV_TIER2)
    subset_notes["Golden Mirror Image Variations"].append(GMIV_TIER3)
    add_odds("Golden Mirror Rookie Image Variations", "Base", GMIV_ROOKIE)
    for db in ["Future Stars Golden Mirror Image Variations", "Team Cards Golden Mirror Image Variations",
               "League Leaders Golden Mirror Image Variations", "Combo Cards Golden Mirror Image Variations"]:
        add_odds(db, "Base", GMIV_THEMED)
        subset_notes[db].append("combined line published for all four")

    # ── META: numbered_parent -> print_run ; note/dq -> notes ─────────────────
    for key, m in META.items():
        targets = BASE_NUMBERED_DB if key == "Base Cards I" else (
            GMIV_DB[:1] if key == "Base – Golden Mirror Variations" else map_subset(key))
        if targets is None:
            con.close(); sys.exit(f"HALT: META key unmapped: {key}")
        for db in targets:
            if "numbered_parent" in m:
                subset_printrun[db] = m["numbered_parent"]
            parts = []
            if m.get("note"): parts.append(m["note"])
            if m.get("dq"): parts.append(m["dq"])
            if parts:
                subset_notes[db].extend(parts)

    # write subset print_run + notes
    for db, pr in subset_printrun.items():
        cur.execute("UPDATE insert_sets SET print_run=? WHERE id=?", (pr, sid[db]))
    for db, notes in subset_notes.items():
        cur.execute("UPDATE insert_sets SET notes=? WHERE id=?", ("; ".join(notes), sid[db]))

    # 1957: set is_base=1
    cur.execute("UPDATE insert_sets SET is_base=1 WHERE id=?", (sid["1957 Rookie Variation"],))

    # pack_odds JSON
    cur.execute("UPDATE sets SET pack_odds=? WHERE id=?", (json.dumps(pack), SET_ID))

    # box_config: add 7 presence-only format keys
    bc = json.loads(cur.execute("SELECT box_config FROM sets WHERE id=?", (SET_ID,)).fetchone()[0])
    added = []
    for fk in NEW_BOX_FORMATS:
        if fk not in bc:
            bc[fk] = {"cards_per_pack": None, "packs_per_box": None}
            added.append(fk)
    cur.execute("UPDATE sets SET box_config=? WHERE id=?", (json.dumps(bc), SET_ID))
    print("\n  Box config formats added:", added)

    # ── GATES (run on pending transaction; commit only if all pass) ───────────
    print("\n===== GATES =====")
    ok = True
    def check(label, got, exp):
        nonlocal ok
        s = "PASS" if got == exp else "FAIL"
        if got != exp: ok = False
        print(f"  [{s}] {label}: {got} (expected {exp})")

    subs = cur.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id=?", (SET_ID,)).fetchone()[0]
    cards = cur.execute("""SELECT COUNT(*) FROM (SELECT DISTINCT insert_set_id, card_number
        FROM player_appearances pa JOIN insert_sets i ON pa.insert_set_id=i.id WHERE i.set_id=?)""", (SET_ID,)).fetchone()[0]
    coplayer = cur.execute("""SELECT (SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON pa.insert_set_id=i.id WHERE i.set_id=?)
        - (SELECT COUNT(*) FROM (SELECT DISTINCT insert_set_id, card_number FROM player_appearances pa JOIN insert_sets i ON pa.insert_set_id=i.id WHERE i.set_id=?))""", (SET_ID, SET_ID)).fetchone()[0]
    b = cur.execute("SELECT COALESCE(SUM(is_base),0), COALESCE(SUM(is_autograph),0), COALESCE(SUM(is_relic),0) FROM insert_sets WHERE set_id=?", (SET_ID,)).fetchone()
    npar = cur.execute("SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON p.insert_set_id=i.id WHERE i.set_id=?", (SET_ID,)).fetchone()[0]
    npar_null = cur.execute("SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON p.insert_set_id=i.id WHERE i.set_id=? AND p.print_run IS NULL", (SET_ID,)).fetchone()[0]
    n_plates = cur.execute("SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON p.insert_set_id=i.id WHERE i.set_id=? AND p.name LIKE '%Printing Plate'", (SET_ID,)).fetchone()[0]
    n_printrun_subsets = cur.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND print_run IS NOT NULL", (SET_ID,)).fetchone()[0]
    # base-numbered parallels
    base6 = cur.execute(f"""SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON p.insert_set_id=i.id
        WHERE i.set_id=? AND i.name IN ({','.join('?'*6)})""", (SET_ID, *BASE_NUMBERED_DB)).fetchone()[0]

    check("Subsets", subs, 87)
    check("Cards", cards, 4042)
    check("Co-player rows", coplayer, 129)
    check("is_base subsets", b[0], 18)
    check("is_autograph subsets", b[1], 23)
    check("is_relic subsets", b[2], 14)
    check("Parallel rows", npar, 725)
    check("  on six base-numbered subsets", base6, 384)
    check("  Printing Plate rows", n_plates, 24)
    check("  NULL print_run parallels", npar_null, 148)
    check("Subset print_run non-null count", n_printrun_subsets, 17)

    # pack_odds keys with a value (distinct union across formats) == expected
    all_keys = set()
    po = json.loads(cur.execute("SELECT pack_odds FROM sets WHERE id=?", (SET_ID,)).fetchone()[0])
    for fk, d in po.items():
        all_keys.update(d.keys())
    check("pack_odds distinct keys == records w/ odds", len(all_keys), len(odds_keys_expected))
    print(f"    (expected count computed = {len(odds_keys_expected)})")

    # spot-asserts (verbatim) via pack_odds
    def spot(label, fmt, key, exp):
        nonlocal ok
        got = po.get(fmt, {}).get(key)
        s = "PASS" if got == exp else "FAIL"
        if got != exp: ok = False
        print(f"  [{s}] {label}: {got!r} (expected {exp!r})")
    spot("Rookie Real One Autographs Base fanatics", "fanatics", "Rookie Real One Autographs Base", "1:568,182")
    spot("Real One Autographs Gold fanatics", "fanatics", "Real One Autographs Gold", "1:4,193,549")
    spot("Base Cards I Union Jack Rainbow Foil london_mega", "london_mega", "Base Cards I Union Jack Rainbow Foil", "1:1")
    spot("NFL Material Dual Relic Cards Base fat_pack", "fat_pack", "NFL Material Dual Relic Cards Base", "1:38,775")

    # names sanity: start uppercase, no "/" no "1:"
    bad = cur.execute("""SELECT p.name FROM parallels p JOIN insert_sets i ON p.insert_set_id=i.id
        WHERE i.set_id=? AND (p.name NOT GLOB '[A-Z]*' OR p.name LIKE '%/%' OR p.name LIKE '%1:%')""", (SET_ID,)).fetchall()
    check("Parallel names malformed (up/no-slash/no-1:)", len(bad), 0)

    print("\n  17 subsets with print_run:")
    for name, pr in cur.execute("SELECT name, print_run FROM insert_sets WHERE set_id=? AND print_run IS NOT NULL ORDER BY name", (SET_ID,)).fetchall():
        print(f"    /{pr:<4} {name}")

    print("\n===== " + ("ALL GATES PASS — committing" if ok else "GATES FAILED — rolling back") + " =====")
    if not ok:
        con.rollback()
        con.close(); sys.exit(1)
    con.commit()
    con.close()
    sys.exit(0)


if __name__ == "__main__":
    main()
