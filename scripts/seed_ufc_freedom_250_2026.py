#!/usr/bin/env python3
"""Seed 2026 Topps UFC Freedom 250 — 117 cards, 6 subsets, flat pack odds.

Box config TBA (follow-up task). Print runs NULL (serial-numbered, unpublished).
Source label corrections (Topps errors, confirmed): "Presidental Seal" -> "Stamp of
Approval" (SO-); "Sticker Autographs" -> "Autographs". Odds typo: 126UFCWH = 26UFCWH
(Autographs Purple 1:12). Non-monotonic Autographs ladder (Green 1:71 > Gold 1:11)
preserved as printed. UFC Dollar has no Blue parallel (encoded by key absence).
After running: npx tsx scripts/recompute-unique-cards.ts
"""
import json, re, sqlite3, unicodedata

db = sqlite3.connect("the-c-list.db")

pack_odds = json.dumps({
    "Base Blue": "1:2",
    "Base Green": "1:2",
    "Base Red/White/Blue": "1:3",
    "Base Purple": "1:3",
    "Base Gold": "1:5",
    "Base Orange": "1:10",
    "Base Black": "1:24",
    "Base Red": "1:48",
    "Base Foilfractor": "1:234",
    "UFC Dollar Green": "1:3",
    "UFC Dollar Red/White/Blue": "1:3",
    "UFC Dollar Purple": "1:3",
    "UFC Dollar Gold": "1:5",
    "UFC Dollar Orange": "1:10",
    "UFC Dollar Black": "1:24",
    "UFC Dollar Red": "1:48",
    "UFC Dollar Foilfractor": "1:234",
    "Founding Fighters Red/White/Blue": "1:19",
    "Founding Fighters Purple": "1:20",
    "Founding Fighters Gold": "1:29",
    "Founding Fighters Orange": "1:58",
    "Founding Fighters Black": "1:143",
    "Founding Fighters Red": "1:280",
    "Founding Fighters Foilfractor": "1:1400",
    "Stamp of Approval Purple": "1:5",
    "Stamp of Approval Gold": "1:8",
    "Stamp of Approval Orange": "1:15",
    "Stamp of Approval Black": "1:36",
    "Stamp of Approval Red": "1:72",
    "Stamp of Approval Foilfractor": "1:350",
    "Relics Blue": "1:5",
    "Relics Green": "1:8",
    "Relics Red/White/Blue": "1:10",
    "Relics Purple": "1:10",
    "Relics Gold": "1:15",
    "Relics Orange": "1:29",
    "Relics Black": "1:72",
    "Relics Red": "1:143",
    "Relics Foilfractor": "1:700",
    "Autographs Green": "1:71",
    "Autographs Red/White/Blue": "1:24",
    "Autographs Purple": "1:12",
    "Autographs Gold": "1:11",
    "Autographs Orange": "1:18",
    "Autographs Black": "1:42",
    "Autographs Red": "1:65",
    "Autographs Foilfractor": "1:319",
})

existing = db.execute("SELECT id FROM sets WHERE slug = '2026-topps-ufc-freedom-250'").fetchone()
if existing:
    raise SystemExit(f"ABORT: set already exists (id={existing[0]})")

db.execute("""
    INSERT INTO sets (name, sport, season, league, tier, slug, is_visible,
                      sample_image_url, release_date, box_config, pack_odds, created_at)
    VALUES ('2026 Topps UFC Freedom 250', 'MMA', '2026', 'UFC', 'Standard',
            '2026-topps-ufc-freedom-250', 1,
            '/sets/2026-topps-ufc-freedom-250.jpg', '2026-06-12', NULL, ?, '2026-06-11T12:00:00Z')
""", (pack_odds,))
SET_ID = db.execute("SELECT last_insert_rowid()").fetchone()[0]
print(f"Created set ID: {SET_ID}")

def slugify(t):
    s = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode('ascii')
    s = s.lower().strip(); s = re.sub(r'[^\w\s-]', '', s); s = re.sub(r'[\s_]+', '-', s)
    return re.sub(r'-+', '-', s).strip('-')

_sc = {}
def goc(name, role="athlete"):
    name = name.strip()
    row = db.execute("SELECT id FROM players WHERE set_id = ? AND name = ?", (SET_ID, name)).fetchone()
    if row: return row[0]
    slug = slugify(name)
    c = slug; i = 2
    while c in _sc: c = f"{slug}-{i}"; i += 1
    _sc[c] = True
    db.execute("INSERT INTO players (set_id, name, slug, unique_cards, total_print_run, one_of_ones, insert_set_count, subject_role) VALUES (?, ?, ?, 0, 0, 0, 0, ?)",
               (SET_ID, name, c, role))
    return db.execute("SELECT last_insert_rowid()").fetchone()[0]

def ins(name, cards, is_auto=False):
    db.execute("INSERT INTO insert_sets (set_id, name, is_autograph) VALUES (?, ?, ?)", (SET_ID, name, 1 if is_auto else 0))
    is_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    for num, pname in cards:
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, NULL)",
                   (goc(pname), is_id, str(num)))
    print(f"  {name}: {len(cards)} cards")
    return is_id

def par(is_id, names):
    for pname in names:
        db.execute("INSERT INTO parallels (insert_set_id, name, print_run, exclusivity) VALUES (?, ?, NULL, NULL)",
                   (is_id, pname))

ROSTER = [
    "Conor McGregor", "Georges St-Pierre", "Anderson Silva", "Khabib Nurmagomedov",
    "Alexander Volkanovski", "Ilia Topuria", "Alex Pereira", "Max Holloway",
    "Dominick Cruz", "Matt Hughes", "Henry Cejudo", "Dustin Poirier",
    "Khamzat Chimaev", "Kayla Harrison", "Erin Blanchfield", "Kamaru Usman",
    "Bo Nickal", "Amanda Nunes", "Ciryl Gane", "Sean O'Malley",
    "Aiemann Zahabi", "Mauricio Ruffy", "Michael Chandler", "Sean Strickland",
    "BJ Penn", "Diego Lopes", "Mackenzie Dern", "Justin Gaethje",
    "Jon Jones", "Chuck Liddell",
]

# ═══ BASE (30) ═══
base_id = ins("Base", [(i + 1, n) for i, n in enumerate(ROSTER)])
par(base_id, ["Blue", "Green", "Red/White/Blue", "Purple", "Gold", "Orange", "Black", "Red", "Foilfractor"])

# ═══ UFC DOLLAR (UD-, 30) — mirrors base roster; no Blue parallel (as printed) ═══
ud_id = ins("UFC Dollar", [(f"UD-{i + 1}", n) for i, n in enumerate(ROSTER)])
par(ud_id, ["Green", "Red/White/Blue", "Purple", "Gold", "Orange", "Black", "Red", "Foilfractor"])

# ═══ FOUNDING FIGHTERS (FF-, 5) ═══
ff_id = ins("Founding Fighters", [
    ("FF-1", "Jon Jones"), ("FF-2", "Conor McGregor"), ("FF-3", "Chuck Liddell"),
    ("FF-4", "Georges St-Pierre"), ("FF-5", "Amanda Nunes"),
])
par(ff_id, ["Red/White/Blue", "Purple", "Gold", "Orange", "Black", "Red", "Foilfractor"])

# ═══ STAMP OF APPROVAL (SO-, 20) — Topps mislabel "Presidental Seal" corrected ═══
so_id = ins("Stamp of Approval", [
    ("SO-1", "Conor McGregor"), ("SO-2", "Georges St-Pierre"), ("SO-3", "Anderson Silva"),
    ("SO-4", "Khabib Nurmagomedov"), ("SO-5", "Alexander Volkanovski"), ("SO-6", "Ilia Topuria"),
    ("SO-7", "Alex Pereira"), ("SO-8", "Max Holloway"), ("SO-9", "Justin Gaethje"),
    ("SO-10", "Sean O'Malley"), ("SO-11", "Bo Nickal"), ("SO-12", "Dustin Poirier"),
    ("SO-13", "Jon Jones"), ("SO-14", "Chuck Liddell"), ("SO-15", "Amanda Nunes"),
    ("SO-16", "Matt Hughes"), ("SO-17", "Khamzat Chimaev"), ("SO-18", "Kamaru Usman"),
    ("SO-19", "Erin Blanchfield"), ("SO-20", "Dominick Cruz"),
])
par(so_id, ["Purple", "Gold", "Orange", "Black", "Red", "Foilfractor"])

# ═══ RELICS (10) — suffix numbering {base#}-R; gaps as printed ═══
re_id = ins("Relics", [
    ("6-R", "Ilia Topuria"), ("7-R", "Alex Pereira"), ("17-R", "Bo Nickal"),
    ("19-R", "Ciryl Gane"), ("20-R", "Sean O'Malley"), ("21-R", "Aiemann Zahabi"),
    ("22-R", "Mauricio Ruffy"), ("23-R", "Michael Chandler"), ("26-R", "Diego Lopes"),
    ("28-R", "Justin Gaethje"),
])
par(re_id, ["Blue", "Green", "Red/White/Blue", "Purple", "Gold", "Orange", "Black", "Red", "Foilfractor"])

# ═══ AUTOGRAPHS (22) — suffix numbering {base#}-A; gaps as printed ═══
# Source label "Sticker Autographs" = autograph type, not subset name.
au_id = ins("Autographs", [
    ("1-A", "Conor McGregor"), ("2-A", "Georges St-Pierre"), ("3-A", "Anderson Silva"),
    ("4-A", "Khabib Nurmagomedov"), ("5-A", "Alexander Volkanovski"), ("6-A", "Ilia Topuria"),
    ("7-A", "Alex Pereira"), ("8-A", "Max Holloway"), ("9-A", "Dominick Cruz"),
    ("10-A", "Matt Hughes"), ("11-A", "Henry Cejudo"), ("12-A", "Dustin Poirier"),
    ("13-A", "Khamzat Chimaev"), ("14-A", "Kayla Harrison"), ("15-A", "Erin Blanchfield"),
    ("17-A", "Bo Nickal"), ("19-A", "Ciryl Gane"), ("20-A", "Sean O'Malley"),
    ("21-A", "Aiemann Zahabi"), ("22-A", "Mauricio Ruffy"), ("24-A", "Sean Strickland"),
    ("29-A", "Jon Jones"),
], is_auto=True)
par(au_id, ["Green", "Red/White/Blue", "Purple", "Gold", "Orange", "Black", "Red", "Foilfractor"])

db.commit()

# ═══ VERIFICATION ═══
print("\n" + "=" * 50)
expected = {"Base": 30, "UFC Dollar": 30, "Founding Fighters": 5,
            "Stamp of Approval": 20, "Relics": 10, "Autographs": 22}
total = 0
ok = True
for name, cnt in db.execute("""
    SELECT is2.name, COUNT(pa.id) FROM insert_sets is2
    LEFT JOIN player_appearances pa ON pa.insert_set_id = is2.id
    WHERE is2.set_id = ? GROUP BY is2.id ORDER BY is2.id""", (SET_ID,)).fetchall():
    total += cnt
    status = "OK" if expected.get(name) == cnt else f"MISMATCH (expected {expected.get(name)})"
    if expected.get(name) != cnt: ok = False
    print(f"  {name}: {cnt} [{status}]")
n_players = db.execute("SELECT COUNT(*) FROM players WHERE set_id = ?", (SET_ID,)).fetchone()[0]
n_pars = db.execute("SELECT COUNT(*) FROM parallels WHERE insert_set_id IN (SELECT id FROM insert_sets WHERE set_id = ?)", (SET_ID,)).fetchone()[0]
print(f"Set ID: {SET_ID}")
print(f"Total cards: {total} (expected 117) [{'OK' if total == 117 else 'MISMATCH'}]")
print(f"Players: {n_players} (expected 30)")
print(f"Parallel rows: {n_pars} (expected 47)")

# Pack odds key sanity check: every key's subset prefix must match an inserted subset name
subset_names = sorted([r[0] for r in db.execute("SELECT name FROM insert_sets WHERE set_id = ?", (SET_ID,)).fetchall()], key=len, reverse=True)
bad = [k for k in json.loads(pack_odds)
       if not any(k == n or k.startswith(n + " ") for n in subset_names)]
if bad:
    print("PACK ODDS KEY MISMATCHES:")
    for b in bad: print(f"  {b}")
else:
    print("Pack odds key sanity check: all 47 keys match subset names. OK")
print("Done!" if ok and total == 117 else "VERIFY FAILED — investigate before migrating")
