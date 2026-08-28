#!/usr/bin/env python3
"""Build 2025-26 Topps Chrome Black Basketball — LOCAL SQLite, one transaction, gates before commit."""
import sqlite3, json, os, sys, re

SP = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(os.getcwd(), "the-c-list.db")
L = lambda f: [json.loads(x) for x in open(os.path.join(SP, f)) if x.strip()]
subs, cards, pars = L("subsets.jsonl"), L("cards.jsonl"), L("parallels.jsonl")

SLUG = "2025-26-topps-chrome-black-basketball"
box_config = {
  "hobby": {"cards_per_pack": 6, "packs_per_box": 2, "boxes_per_case": 12, "autos_per_box": 1, "notes": "1 encased autograph per box"},
  "instant": {"cards_per_pack": None, "packs_per_box": None, "boxes_per_case": None,
              "notes": "Base 2.93 (guaranteed 2); Parallels 0.33 (1 in ~3 packs); Instant Parallels 0.36 (1 in ~2.8 packs); Autographs 0.31 (1 in ~3.2 packs); Case Hits 0.07 (1 in ~14 packs)"},
}

def slugify(n): return re.sub(r"[^a-z0-9]+", "-", n.lower()).strip("-")

con = sqlite3.connect(DB); cur = con.cursor()
try:
    # NO pack_odds for this set (odds unpublished) -> NULL
    cur.execute("""INSERT INTO sets(name,sport,season,league,tier,sample_image_url,pack_odds,box_config,release_date,slug,is_visible,created_at,topps_url)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                ("2025-26 Topps Chrome Black Basketball", "Basketball", "2025-26", "NBA", "Chrome Black",
                 f"/sets/{SLUG}.jpg", None, json.dumps(box_config), "2026-08-27", SLUG, 1, "2026-08-28", None))
    set_id = cur.lastrowid

    is_id = {}
    for s in subs:
        cur.execute("INSERT INTO insert_sets(set_id,name,is_autograph,is_base,is_relic,is_booklet,print_run,notes) VALUES(?,?,?,?,0,0,NULL,NULL)",
                    (set_id, s["name"], s["is_autograph"], s["is_base"]))
        is_id[s["name"]] = cur.lastrowid

    # distinct subjects in first-appearance order; reuse identity metadata by exact name
    order = []
    for c in cards:
        for n in c["subjects"]:
            if n not in order: order.append(n)
    pid = {}; linked = created = 0; used_slugs = set()
    for name in order:
        row = cur.execute("""SELECT nba_player_id,image_url,slug,subject_role FROM players WHERE name=?
                             ORDER BY (nba_player_id IS NOT NULL) DESC,(image_url IS NOT NULL) DESC,(slug IS NOT NULL) DESC LIMIT 1""", (name,)).fetchone()
        exists = row is not None
        nba, img, slug, role = (row if row else (None, None, None, None))
        role = role or "athlete"
        slug = slug or slugify(name)
        base, k = slug, 2
        while slug in used_slugs:
            slug = f"{base}-{k}"; k += 1
        used_slugs.add(slug)
        cur.execute("INSERT INTO players(set_id,name,subject_role,nba_player_id,image_url,slug) VALUES(?,?,?,?,?,?)",
                    (set_id, name, role, nba, img, slug))
        pid[name] = cur.lastrowid
        linked += 1 if exists else 0; created += 0 if exists else 1

    for c in cards:
        cur.execute("INSERT INTO player_appearances(player_id,insert_set_id,card_number,is_rookie,subset_tag,team) VALUES(?,?,?,?,NULL,?)",
                    (pid[c["subjects"][0]], is_id[c["subset"]], c["card_number"], 1 if c["rookie"] else 0, c["team"]))
    for p in pars:
        cur.execute("INSERT INTO parallels(insert_set_id,name,print_run,exclusivity,note) VALUES(?,?,?,NULL,?)",
                    (is_id[p["subset"]], p["parallel"], p["print_run"], p.get("note")))

    print(f"subjects: linked(reused metadata)={linked}  created(new name)={created}  total={linked+created}")

    # ── GATES ──
    isids = tuple(is_id.values()); ph = ",".join("?" * len(isids))
    q = lambda s, a=(): cur.execute(s, a).fetchone()[0]
    G = []
    G.append(("subsets 15", q(f"SELECT COUNT(*) FROM insert_sets WHERE set_id={set_id}") == 15))
    G.append(("is_base 1", q(f"SELECT COUNT(*) FROM insert_sets WHERE set_id={set_id} AND is_base=1") == 1))
    G.append(("is_autograph 8", q(f"SELECT COUNT(*) FROM insert_sets WHERE set_id={set_id} AND is_autograph=1") == 8))
    G.append(("is_relic 0", q(f"SELECT COUNT(*) FROM insert_sets WHERE set_id={set_id} AND is_relic=1") == 0))
    G.append(("cards 556", q(f"SELECT COUNT(*) FROM player_appearances WHERE insert_set_id IN ({ph})", isids) == 556))
    G.append(("co-player rows 0", q(f"SELECT COUNT(*) FROM appearance_co_players cp JOIN player_appearances pa ON pa.id=cp.appearance_id WHERE pa.insert_set_id IN ({ph})", isids) == 0))
    G.append(("parallels 88", q(f"SELECT COUNT(*) FROM parallels WHERE insert_set_id IN ({ph})", isids) == 88))
    G.append(("NULL print_run 5", q(f"SELECT COUNT(*) FROM parallels WHERE insert_set_id IN ({ph}) AND print_run IS NULL", isids) == 5))
    G.append(("1/1 rows 15", q(f"SELECT COUNT(*) FROM parallels WHERE insert_set_id IN ({ph}) AND print_run=1", isids) == 15))
    G.append(("pack_odds NULL", cur.execute(f"SELECT pack_odds FROM sets WHERE id={set_id}").fetchone()[0] is None))
    G.append(("subjects 239", q(f"SELECT COUNT(*) FROM players WHERE set_id={set_id}") == 239))
    G.append(("no dup subject names", q(f"SELECT COUNT(*) FROM (SELECT name FROM players WHERE set_id={set_id} GROUP BY name HAVING COUNT(*)>1)") == 0))
    for nm in ["Ronald Holland II", "Alex Sarr", "Liam McNeeley", "Yanic Konan-Niederhäuser"]:
        G.append((f"one subject '{nm}'", q(f"SELECT COUNT(*) FROM players WHERE set_id={set_id} AND name=?", (nm,)) == 1))
    G.append(("rookie-designated 228", q(f"SELECT COUNT(*) FROM player_appearances WHERE insert_set_id IN ({ph}) AND is_rookie=1", isids) == 228))
    G.append(("base rookies 55", q(f"SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id WHERE i.set_id={set_id} AND i.name='Base Cards' AND pa.is_rookie=1") == 55))
    # spot asserts
    def subj(cn, sub=None):
        extra = f" AND i.name='{sub}'" if sub else ""
        r = cur.execute(f"""SELECT p.name,pa.is_rookie FROM player_appearances pa JOIN players p ON p.id=pa.player_id
                            JOIN insert_sets i ON i.id=pa.insert_set_id WHERE i.set_id={set_id} AND pa.card_number=?{extra}""", (cn,)).fetchone()
        return r
    r = subj("101", "Base Cards"); G.append(("spot 101=Cooper Flagg rookie", r and r[0] == "Cooper Flagg" and r[1] == 1))
    r = subj("41", "Base Cards"); G.append(("spot base 41=Hugo González rookie", r and r[0] == "Hugo González" and r[1] == 1))
    r = subj("41", "Rookie Design Variations"); G.append(("spot RDV 41=Hugo González", r and r[0] == "Hugo González"))
    r = subj("AU-SC", "Autograph Cards"); G.append(("spot AU-SC=Stephen Curry", r and r[0] == "Stephen Curry"))
    r = subj("IA-KA", "Ivory Autographs"); G.append(("spot IA-KA=Kareem Abdul-Jabbar", r and r[0] == "Kareem Abdul-Jabbar"))
    hc = cur.execute(f"SELECT par.name,par.print_run FROM parallels par JOIN insert_sets i ON i.id=par.insert_set_id WHERE i.set_id={set_id} AND i.name='Home Court'").fetchall()
    G.append(("spot Home Court parallel Black 1/1", hc == [("Black", 1)]))
    tg = cur.execute(f"SELECT par.print_run,par.note FROM parallels par JOIN insert_sets i ON i.id=par.insert_set_id WHERE i.set_id={set_id} AND i.name='Base Cards' AND par.name='Teal Glitter'").fetchone()
    G.append(("spot Teal Glitter /64 + Instant note", tg == (64, "Instant Rips Exclusive")))
    bc = json.loads(cur.execute(f"SELECT box_config FROM sets WHERE id={set_id}").fetchone()[0])
    G.append(("box_config 2 formats (hobby,instant)", set(bc.keys()) == {"hobby", "instant"}))
    G.append(("hobby autos_per_box=1", bc["hobby"].get("autos_per_box") == 1))
    G.append(("instant notes contains 2.93", "2.93" in (bc["instant"].get("notes") or "")))

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
