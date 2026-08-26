#!/usr/bin/env python3
"""Phase 3 classifier/builder (read-only compute). Reads data.jsonl + db_structure.json,
applies rulings A-D, classifies every row, halts on unmapped, and emits build.json."""
import json, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
rows = [json.loads(l) for l in open(os.path.join(HERE, "data.jsonl")) if l.strip()]
db = json.load(open(os.path.join(HERE, "db_structure.json")))
SUB_BY_NAME = {s["name"]: s for s in db["subsets"]}
PARSET = {s["name"]: {p["name"] for p in s["parallels"]} for s in db["subsets"]}

# ---- ruling A-D transforms on the raw row list ----
xrows = []
for r in rows:
    n = r["name"]
    if n == "Island Ink Foilfractor Mascot Autographs - 1:3,448,276 - 1: - 1: 1: 1: 1: - - - -1:20,000,000 1:100,000,000 - - - 1:12,500,000 - - - - Foilfractor":
        continue  # ruling C: discard merged row (two clean rows appended below)
    if n == "FUTURE STARS" and r["odds"] == {"Super Box": "1:9"}:
        r = dict(r); r["name"] = "FUTURE STARS Silver Crackle"  # ruling A
    if n == "Funko Base Cards Physical Funko Figurine NOT":
        r = dict(r); r["_skip_informational"] = True  # ruling D
    xrows.append(r)
# ruling C: two clean split rows
xrows.append({"name": "Island Ink Foilfractor", "variant": None, "odds": {"Hobby":"1:571,429","Jumbo":"1:178,254","Hanger":"1:1,162,791","Fat Pack":"1:3,125,000","Value":"1:5,882,353","Mega":"1:5,882,353","Bulk Packs":"1:3,571,429","London Mega":"1:20,000,000","Walmart Mega":"1:2,222,223"}})
xrows.append({"name": "Mascot Autographs Foilfractor", "variant": None, "odds": {"Hobby":"1:3,448,276","Jumbo":"1:1,063,830","Hanger":"1:7,142,858","Fat Pack":"1:20,000,000","Value":"1:33,333,334","Mega":"1:33,333,334","Bulk Packs":"1:20,000,000","London Mega":"1:100,000,000","Walmart Mega":"1:12,500,000"}})
print(f"rows after ruling A-D transforms: {len(xrows)} (was {len(rows)}; -1 merged +2 split = +1 => expect 933)")

# ---- format key map ----
FMT = {"Hobby Silver Pack":"hobby_silver_pack","Hobby":"hobby","Jumbo Silver Pack":"jumbo_silver_pack","Jumbo":"jumbo",
"Hanger":"hanger","Fat Pack":"fat_pack","Value":"value","Mega":"mega","Super Box":"super_box","Super Box Oversized":"super_box_oversized",
"Fanatics":"fanatics","Bulk Packs":"bulk_packs","London Mega":"london_mega","Club Exclusive Box":"club_super_box",
"Club Exclusive Box Oversized":"club_super_box_oversized","Kids Mega":"kids_mega","Walmart Mega":"walmart_mega",
"Club Ex Box Sams":"club_ex_box_sams","Club Ex Box Sams Oversized":"club_ex_box_sams_oversized","GC White Slip Sheets":"gc_white_slip_sheets"}

# ---- subset prefix -> db subset name (or FOLLOWUP / GMIV tier) ----
FOLLOWUP = "__FOLLOWUP__"
PREFIX = {
 "Real One Autographs":"Real One Autographs","Rookie Real One Autographs":"Rookie Real One Autographs",
 "Base Cards Vintage Stock Variation":"Base Cards Vintage Stock Variation","Base Cards Clear Variation":"Base Cards Clear Variation",
 "Base Cards Team Color Border Variations":"Base Cards Team Color Border Variations","Base Cards Player Number Variations":"Base Cards Player Number Variations",
 "Base Cards True Photo Variations":"Base Cards True Photo Variations","Base Cards":"Base Cards I",
 "FUTURE STARS FUTURE STARS REAL ONE AUTOGRAPHS":FOLLOWUP,"FUTURE STARS":"Future Stars",
 "Team Cards Golden Mirror Image Variations":"Team Cards Golden Mirror Image Variations","Team Cards":"Team Cards",
 "League Leaders Golden Mirror Image Variations":"League Leaders Golden Mirror Image Variations","League Leaders":"League Leaders",
 "Combo Cards Golden Mirror Image Variations":"Combo Cards Golden Mirror Image Variations","Combo Cards":"Combo Cards",
 "Future Stars Golden Mirror Image Variations":"Future Stars Golden Mirror Image Variations",
 "ROOKIES":"Rookies",
 "Golden Mirror Image Variations I":("Golden Mirror Image Variations","I"),
 "Golden Mirror Image Variations II":("Golden Mirror Image Variations","II"),
 "Golden Mirror Image Variations III":("Golden Mirror Image Variations","III"),
 "GOLDEN MIRROR ROOKIE IMAGE VARIATIONS":"Golden Mirror Rookie Image Variations",
 "2025 All Topps Team Autographs":"2025 All Topps Team Autographs","2025 All Topps Team":"2025 All Topps Team",
 "Topps Profiles":"Topps Profiles","Big Ticket Players":"Big Ticket Players","2025 Greatest Hits":"2025 Greatest Hits",
 "Ring of Honor Signatures":"Ring of Honor Signatures","Ring of Honor":"Ring of Honor",
 "Class of 26":"Class of 26","Touchdown Machines":"Touchdown Machines","1000 Yard Club":"1000 Yard Club","4000 Yard Club":"4000 Yard Club",
 "Wild Card Moments":"Wild Card Moments","Divisional Dominance":"Divisional Dominance","Conference Kings":"Conference Kings","All Hail the Champ":"All Hail the Champ",
 "Struttin":"Struttin","Billboard Material":"Billboard Material","Touchdown":"Touchdown",
 "1991 Topps Football Rookie Autograph Cards":"1991 Topps Football Rookie Autograph Cards",
 "1991 Topps Football Rookie Relics":"1991 Topps Football Rookie Relics",
 "1991 Topps Football Relics":"1991 Topps Football Relics","1991 Topps Football":"1991 Topps Football",
 "NFL Stars Autographs":"NFL Stars Autographs","NFL Stars Dual Autographs":"NFL Stars Dual Autographs","NFL Stars Triple Autographs":"NFL Stars Triple Autographs","NFL Stars":"NFL Stars",
 "Pressure Cookers":"Pressure Cookers","Greats of the Game":"Greats of the Game","All Kings":"All Kings",
 "1991 TOPPS FOOTBALL CHROME BASE CARDS":"1991 Topps Football Chrome Base Cards","1957 Rookie Variation":"1957 Rookie Variation",
 "NFL Material Autograph Cards":"NFL Material Autograph Cards","NFL Material Dual Relic Autographs":"NFL Material Dual Relic Autographs",
 "NFL Material Dual Relic Cards":"NFL Material Dual Relic Cards","NFL Material Cards":"NFL Material Cards",
 "Field Fit Swatch Collection Autograph Relic":"Field Fit Swatch Collection Autograph Relic","Field Fit Swatch Collection":"Field Fit Swatch Collection",
 "Real One Relics":"Real One Relics","TOPPS AUTOGRAPH PATCH CARDS":"Topps Autograph Patch Cards",
 "SUPER BOWL CHAMPION SIGNATURES":"Super Bowl Champion Signatures","1991 TOPPS FOOTBALL AUTOGRAPH CARDS I":"1991 Topps Football Autograph Cards",
 "Victory Ink":"Victory Ink","Island Ink":"Island Ink","Mascot Autographs":"Mascot Autographs",
 "Super Bowl Halftime Headliners Autographs":FOLLOWUP,
 "1991 Topps Rookies Football Chrome Base Cards":"1991 Topps Rookies Football Chrome Base Cards","1991 Topps Rookies Football":"1991 Topps Rookies Football",
 "1991 Super Rookie Autographs":"1991 Super Rookies Autographs",
 "Super Box Oversized Base Card":"Super Box Oversized Base Card","Companion Cards":"Companion Cards","Funko Base Cards":"Funko Base Cards",
 "Fanatics Authentic Redemptions Cards":"Fanatics Authentic Redemptions Cards","Marketing Card":FOLLOWUP,
 "Rookie Premiere Autographs":"Rookie Premiere Autographs","Lenticular London":FOLLOWUP,
 "Rookie Card Vintage Stock Variation":"Rookie Card Vintage Stock Variation","Rookie Card Clear Variation":"Rookie Card Clear Variation",
 "Rookie Card Team Color Border Variation":"Rookie Card Team Color Border Variation","Rookie Card Player Number Variations":"Rookie Card Player Number Variations",
 "Rookie Card True Photo Variation":"Rookie Card True Photo Variation",
 "NFL Rookies Material Cards":"NFL Rookies Material Cards","NFL Rookie Material Autograph Cards":"NFL Rookie Material Autograph Cards",
 "Rookie Real One Relics":"Rookie Real One Relics","Topps Autograph Rookie Patch Cards":"Topps Autograph Rookie Patch Cards",
 "The Flagship Collection Chrome":"The Flagship Collection Chrome","The Flagship Collection":"The Flagship Collection",
 "Big Time Players":"Big Time Players","Highlight Reels":"Highlight Reels","Club Exclusive Oversized Card":"Club Exclusive Oversized Card",
 "Flagship First Dual Signatures":"Flagship First Dual Signatures","Flagship First Signatures":"Flagship First Signatures",
 "GC White Slip Sheets":FOLLOWUP,
}
PREFIXES_SORTED = sorted(PREFIX.keys(), key=len, reverse=True)

PAR_ALIAS = {"Printing Plate Cyan Print":"Cyan Printing Plate","Printing Plate Magenta Print":"Magenta Printing Plate",
 "Printing Plate Black Print":"Black Printing Plate","Printing Plate Yellow Print":"Yellow Printing Plate",
 "Football Parallel":"Football","FUNKO BASE CARDS AUTOGRAPH PARALLEL":"Autograph Parallel",
 # approved aliases: sheet shorthand -> DB parallel name (attach, do not rename)
 "Crackle":"Crackle Foil","London Union Jack":"Union Jack","London Big Ben":"Big Ben",
 "London Tudor Rose":"Tudor Rose","London Crown Jewels":"Crown Jewels"}

def match_prefix(name):
    for p in PREFIXES_SORTED:
        if name == p or name.startswith(p + " "):
            return p, name[len(p):].strip()
    return None, None

# ---- classify ----
pack = {}  # fmt_key -> {odds_key: val}
inserts = {}  # (subset, parallel) -> note
notes = {}  # subset -> list of note strings
unmapped = []
actions = {"attach":0,"insert-parallel":0,"subset-base":0,"notes-only":0,"skip-no-odds":0,"follow-up":0,"skip-informational":0}
followups = set()
dupe_conflicts = []
keyed_subpar = set()  # (subset, parallel-or-None) referenced by keys

def put(subset, parname, odds):
    okey = f"{subset} {parname}"
    keyed_subpar.add((subset, None if parname=="Base" else parname))
    for dfmt, val in odds.items():
        fk = FMT[dfmt]
        pack.setdefault(fk, {})
        if okey in pack[fk] and pack[fk][okey] != val:
            dupe_conflicts.append((fk, okey, pack[fk][okey], val))
        pack[fk].setdefault(okey, val)  # first wins (ruling B)

for r in xrows:
    name, odds, variant = r["name"], r["odds"], r["variant"]
    if r.get("_skip_informational"): actions["skip-informational"]+=1; continue
    pfx, rem = match_prefix(name)
    if pfx is None:
        unmapped.append(name); continue
    target = PREFIX[pfx]
    if target == FOLLOWUP:
        actions["follow-up"]+=1; followups.add(pfx); continue
    tier = None
    if isinstance(target, tuple): target, tier = target
    sub = target
    # empty odds -> skip
    if not odds: actions["skip-no-odds"]+=1; continue
    # GMIV tier II/III -> notes only
    if tier in ("II","III"):
        notes.setdefault(sub, []).append(f"Golden Mirror Image Variations Tier {tier}: " + ", ".join(f"{k} {v}" for k,v in odds.items()))
        actions["notes-only"]+=1; continue
    # variant handling
    if variant == "topps_conflicting_odds_line_2":
        notes.setdefault(sub, []).append("Topps publishes two conflicting lines. Line 2: " + f"{rem or 'Base'} " + ", ".join(f"{k} {v}" for k,v in odds.items()))
        actions["notes-only"]+=1; continue
    if variant in ("veterans_only_line","second_line_unlabeled"):
        lbl = {"veterans_only_line":"Veterans-only line","second_line_unlabeled":"Second (unlabeled) line"}[variant]
        notes.setdefault(sub, []).append(f"{lbl}: {rem or 'Base'} " + ", ".join(f"{k} {v}" for k,v in odds.items()))
        actions["notes-only"]+=1; continue
    # variant topps_conflicting_odds_line_1 -> attach (falls through)
    par = rem if rem else "Base"
    par = PAR_ALIAS.get(par, par)
    if par == "Base":
        put(sub, "Base", odds); actions["subset-base"]+=1; continue
    if par in PARSET.get(sub, set()):
        put(sub, par, odds); actions["attach"]+=1
    else:
        note = "added from official Topps odds sheet"
        if sub == "Base Cards I" and par == "Silver Crackle":
            note += ". Topps sheet also prints a third Base Cards Silver Crackle line at Super Box 1:2"
        inserts[(sub,par)] = note
        put(sub, par, odds); actions["insert-parallel"]+=1

# ---- report ----
print("\n=== UNMAPPED (halt if any) ===")
print("NONE" if not unmapped else "\n".join(unmapped))
print("\n=== ACTION COUNTS ===")
for k,v in actions.items(): print(f"  {k}: {v}")
print("  TOTAL classified:", sum(actions.values()))
print("\n=== FOLLOW-UPS ==="); [print("  "+f) for f in sorted(followups)]
print("\n=== NEW PARALLELS TO INSERT ({}) ===".format(len(inserts)))
for (s,p),nt in sorted(inserts.items()): print(f"  [{s}] :: {p}")
print("\n=== DUPLICATE KEY CONFLICTS (first-wins applied) ===")
print("NONE" if not dupe_conflicts else "\n".join(f"  {fk} | {ok} | kept {a} dropped {b}" for fk,ok,a,b in dupe_conflicts))
print("\n=== NOTES (insert_sets.notes) subsets:", len(notes), "===")
for s,ns in sorted(notes.items()): print(f"  [{s}] {len(ns)} note-line(s)")

# existing DB parallels receiving NO odds
recv = set()
for fk,d in pack.items():
    for ok in d: recv.add(ok)
noodds = []
for s in db["subsets"]:
    for p in s["parallels"]:
        if f"{s['name']} {p['name']}" not in recv:
            noodds.append((s["name"], p["name"]))
print(f"\n=== EXISTING DB PARALLELS WITH NO OFFICIAL ODDS ({len(noodds)}) ===")
for s,p in noodds: print(f"  [{s}] {p}")

# key count
allkeys = set()
for d in pack.values(): allkeys.update(d.keys())
print(f"\n=== pack_odds: formats={len(pack)} distinct_keys={len(allkeys)} ===")
print("  formats:", sorted(pack.keys()))

# referential integrity (post-insert): every keyed (subset,parallel) exists
POST_PAR = {s:set(PARSET.get(s,set())) for s in SUB_BY_NAME}
for (s,p) in inserts: POST_PAR.setdefault(s,set()).add(p)
bad=[]
for (s,p) in keyed_subpar:
    if s not in SUB_BY_NAME: bad.append(("SUBSET_MISSING",s,p)); continue
    if p is not None and p not in POST_PAR[s]: bad.append(("PAR_MISSING",s,p))
print(f"\n=== REFERENTIAL INTEGRITY (bad refs, expect 0): {len(bad)} ===")
for b in bad: print("  ",b)

# spot gates
def g(fk, key): return pack.get(fk,{}).get(key)
spots = [
 ("hobby","Base Cards I Rainbow Foil","1:68"),
 ("hobby","Future Stars Rainbow Foil","1:406"),
 ("hobby","Rookies Rainbow Foil","1:41"),
 ("hobby","Real One Autographs Base","1:3,181"),
 ("fanatics","Rookie Real One Autographs Base","1:568,182"),
 ("hobby_silver_pack","1991 Topps Football Chrome Base Cards Superfractor","1:6,556"),
 ("london_mega","Base Cards I Union Jack Rainbow Foil","1:1"),
]
print("\n=== SPOT GATES ===")
allok=True
for fk,key,exp in spots:
    got=g(fk,key); ok = got==exp
    allok &= ok
    print(f"  [{'OK' if ok else 'FAIL'}] {fk} | {key} == {exp!r} (got {got!r})")
print("  Marketing Card is NOT a subset:", "Marketing Card" not in SUB_BY_NAME)

# emit build.json
json.dump({"pack":pack,"inserts":[{"subset":s,"parallel":p,"note":n} for (s,p),n in inserts.items()],
 "notes":notes,"distinct_keys":len(allkeys)}, open(os.path.join(HERE,"build.json"),"w"))
print("\nwrote build.json; halt_needed =", bool(unmapped or bad or not allok))
