#!/usr/bin/env python3
"""Build 2026 Topps Chrome Samurai Japan Baseball — LOCAL SQLite, one transaction, gates before commit."""
import sqlite3, json, os, sys, re

SP = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(os.getcwd(), "the-c-list.db")
L = lambda f: [json.loads(x) for x in open(os.path.join(SP, f)) if x.strip()]
subs, cards, pars = L("subsets.jsonl"), L("cards.jsonl"), L("parallels.jsonl")
meta = json.load(open(os.path.join(SP, "subjects_meta.json")))

SLUG = "2026-topps-chrome-samurai-japan-baseball"
box_config = {"hobby": {"cards_per_pack": 7, "packs_per_box": 4, "boxes_per_case": 10, "inserts_per_box": 1,
                        "notes": "Guarantees 2 sequentially numbered parallels (/250 or less) and 1 insert per box"}}
# pack_odds: subset-base odds ("{subset} Base") + parallel odds ("{subset} {parallel}")
pack = {"hobby": {}}
for s in subs:
    if s["odds"].get("hobby"):
        pack["hobby"][f'{s["name"]} Base'] = s["odds"]["hobby"]
for p in pars:
    pack["hobby"][f'{p["subset"]} {p["parallel"]}'] = p["odds"]["hobby"]

def slugify(n): return re.sub(r"[^a-z0-9]+", "-", n.lower()).strip("-")

con = sqlite3.connect(DB); cur = con.cursor()
try:
    cur.execute("""INSERT INTO sets(name,sport,season,league,tier,sample_image_url,pack_odds,box_config,release_date,slug,is_visible,created_at,topps_url)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                ("2026 Topps Chrome Samurai Japan Baseball", "Baseball", "2026", "Samurai Japan", "Chrome",
                 f"/sets/{SLUG}.jpg", json.dumps(pack), json.dumps(box_config), "2026-10-16", SLUG, 1, "2026-08-27", None))
    set_id = cur.lastrowid

    is_id = {}
    for s in subs:
        cur.execute("INSERT INTO insert_sets(set_id,name,is_autograph,is_base,is_relic,is_booklet,print_run,notes) VALUES(?,?,?,?,0,0,NULL,?)",
                    (set_id, s["name"], s["is_autograph"], s["is_base"], s.get("note")))
        is_id[s["name"]] = cur.lastrowid

    # distinct subjects in first-appearance order
    order = []
    for c in cards:
        for n in c["subjects"]:
            if n not in order: order.append(n)
    pid = {}; linked = created = 0; used_slugs = set()
    for name in order:
        m = meta.get(name, {})
        slug = m.get("slug") or slugify(name)
        base, k = slug, 2
        while slug in used_slugs:
            slug = f"{base}-{k}"; k += 1
        used_slugs.add(slug)
        cur.execute("INSERT INTO players(set_id,name,subject_role,mlb_player_id,image_url,slug) VALUES(?,?,?,?,?,?)",
                    (set_id, name, "player", m.get("mlb_player_id"), m.get("image_url"), slug))
        pid[name] = cur.lastrowid
        if m.get("existing"): linked += 1
        else: created += 1

    for c in cards:
        cur.execute("INSERT INTO player_appearances(player_id,insert_set_id,card_number,is_rookie,subset_tag,team) VALUES(?,?,?,0,?,?)",
                    (pid[c["subjects"][0]], is_id[c["subset"]], c["card_number"], c.get("tag"), c["team"]))
        aid = cur.lastrowid
        for co in c["subjects"][1:]:
            cur.execute("INSERT INTO appearance_co_players(appearance_id,co_player_id) VALUES(?,?)", (aid, pid[co]))

    for p in pars:
        cur.execute("INSERT INTO parallels(insert_set_id,name,print_run,exclusivity,note) VALUES(?,?,?,NULL,NULL)",
                    (is_id[p["subset"]], p["parallel"], p["print_run"]))

    print(f"subjects: linked(reused metadata)={linked}  created(new name)={created}  total={linked+created}")

    # ── GATES ──
    isids = tuple(is_id.values())
    q1 = lambda s, a=(): cur.execute(s, a).fetchone()[0]
    ph = ",".join("?" * len(isids))
    G = []
    G.append(("subsets 8", q1(f"SELECT COUNT(*) FROM insert_sets WHERE set_id={set_id}") == 8))
    G.append(("is_base 2", q1(f"SELECT COUNT(*) FROM insert_sets WHERE set_id={set_id} AND is_base=1") == 2))
    G.append(("is_autograph 2", q1(f"SELECT COUNT(*) FROM insert_sets WHERE set_id={set_id} AND is_autograph=1") == 2))
    G.append(("is_relic 0", q1(f"SELECT COUNT(*) FROM insert_sets WHERE set_id={set_id} AND is_relic=1") == 0))
    G.append(("cards 124", q1(f"SELECT COUNT(*) FROM player_appearances WHERE insert_set_id IN ({ph})", isids) == 124))
    G.append(("co-player rows 6", q1(f"SELECT COUNT(*) FROM appearance_co_players cp JOIN player_appearances pa ON pa.id=cp.appearance_id WHERE pa.insert_set_id IN ({ph})", isids) == 6))
    G.append(("parallels 23", q1(f"SELECT COUNT(*) FROM parallels WHERE insert_set_id IN ({ph})", isids) == 23))
    G.append(("null print_run 1", q1(f"SELECT COUNT(*) FROM parallels WHERE insert_set_id IN ({ph}) AND print_run IS NULL", isids) == 1))
    G.append(("1/1 parallels 4", q1(f"SELECT COUNT(*) FROM parallels WHERE insert_set_id IN ({ph}) AND print_run=1", isids) == 4))
    G.append(("subjects 37", q1(f"SELECT COUNT(*) FROM players WHERE set_id={set_id}") == 37))
    G.append(("no dup subject names", q1(f"SELECT COUNT(*) FROM (SELECT name FROM players WHERE set_id={set_id} GROUP BY name HAVING COUNT(*)>1)") == 0))
    po = json.loads(cur.execute(f"SELECT pack_odds FROM sets WHERE id={set_id}").fetchone()[0])["hobby"]
    G.append(("pack_odds keys 25", len(po) == 25))
    G.append(("  2 subset-base keys", sum(1 for k in po if k.endswith(" Base")) == 2))
    # spot asserts
    G.append(("spot Base Cards Unnumbered Parallel==1:4", po.get("Base Cards Unnumbered Parallel") == "1:4"))
    G.append(("spot Base Card Short Prints Base==1:15", po.get("Base Card Short Prints Base") == "1:15"))
    G.append(("spot no Base Card Autograph Parallel base key", "Base Card Autograph Parallel Base" not in po))
    G.append(("spot Base Card Autograph Parallel Dark Gold==1:4,027", po.get("Base Card Autograph Parallel Dark Gold") == "1:4,027"))
    r = cur.execute(f"""SELECT p.name FROM player_appearances pa JOIN players p ON p.id=pa.player_id
                        JOIN insert_sets i ON i.id=pa.insert_set_id WHERE i.set_id={set_id} AND pa.card_number='80SP'""").fetchone()
    G.append(("spot 80SP subject Shohei Ohtani", r and r[0] == "Shohei Ohtani"))
    r = cur.execute(f"""SELECT cp2.name FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                        JOIN appearance_co_players cp ON cp.appearance_id=pa.id JOIN players cp2 ON cp2.id=cp.co_player_id
                        WHERE i.set_id={set_id} AND pa.card_number='GG-1A'""").fetchone()
    G.append(("spot GG-1A co-player Sadaharu Oh", r and r[0] == "Sadaharu Oh"))
    G.append(("zero Sluggers/Strikers/Championship subsets", q1(f"SELECT COUNT(*) FROM insert_sets WHERE set_id={set_id} AND (name LIKE '%Sluggers%' OR name LIKE '%Strikers%' OR name LIKE '%Championship%')") == 0))

    allok = all(ok for _, ok in G)
    for n, ok in G: print(f"  [{'OK' if ok else 'FAIL'}] {n}")
    if not allok:
        con.rollback(); print("\nGATE FAILURE -> ROLLED BACK"); sys.exit(1)
    con.commit()
    print(f"\nAll gates pass. COMMITTED. set_id={set_id}")
except Exception as e:
    con.rollback(); print("ERROR -> rolled back:", e); raise
finally:
    con.close()
