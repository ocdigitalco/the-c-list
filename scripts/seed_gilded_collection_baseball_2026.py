"""
Seed: 2026 Topps Gilded Collection Baseball — full set (560 cards, 12 subsets).

Source: scratchpad/gil.jsonl (one card per line: subset, card_number, subject,
team, rookie?, source_subject?). Print runs, parallels and box config come from
Tyler's pasted list; where the PDF and list differ the PDF wins.

Rulings applied (Phase 0, confirmed):
  - Tier Premium (the three older Gilded rows are empty shells, not precedent).
  - Base card 199 printed twice (Tony Gwynn, Alex Freeland), no card 110 — seed
    as printed (200 rows / 199 distinct), subset note records it.
  - "Vladimir Guerero" typo: subject already "Vladimir Guerrero"; source_subject
    is provenance only and is dropped. (512505↔522951 dup left alone — follow-up.)
  - Ichiro: stored form "Ichiro". Base 51 / GR-24 / SQ-2 seed as "Ichiro";
    HOFPA-I keeps the printed "Ichiro Suzuki" as its own player row so the athlete
    queue (merge row, qid 366) folds it into Ichiro AND records "Ichiro Suzuki"
    as a durable alias. 273 player rows = 272 people.
  - Three accent folds seeded under stored canonical: Edgar Martínez, Pedro
    Martínez, Tony Pérez.
  - Tony La Russa: new, role coach, team NULL.
  - Skubal / Ballesteros / legends: teams kept as printed.
  - Statuesque: unnumbered parent (print_run NULL); three parallels
    (Gold /1, Gold Variation unnumbered, Gold Variation 1/1 /1).

Run post-seed.ts after this, then migrate-to-turso.ts --set.
Usage: python3 scripts/seed_gilded_collection_baseball_2026.py
"""
import sqlite3, os, json, re, unicodedata

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
JSONL = os.path.join(os.path.dirname(__file__), "..", "scratchpad", "gil.jsonl")

SET_NAME = "2026 Topps Gilded Collection Baseball"
SET_SLUG = "2026-topps-gilded-collection-baseball"

# file subject -> stored player name (accent folds; Ichiro Suzuki kept distinct)
NAME_FIX = {
    "Edgar Martinez": "Edgar Martínez",
    "Pedro Martinez": "Pedro Martínez",
    "Tony Perez": "Tony Pérez",
}
COACH = {"Tony La Russa"}

# subset -> (is_base, is_autograph, is_relic, print_run, note)
SUBSETS = [
    ("Base", 1, 0, 0, 99,
     "Checklist prints two cards numbered 199 (Tony Gwynn, Alex Freeland) and no card 110."),
    ("Gold Regalia", 0, 0, 0, 79, None),
    ("Gold Storm", 0, 0, 0, 26, None),
    ("Statuesque", 0, 0, 0, None, None),
    ("24K", 0, 0, 0, 1, None),
    ("Gold Framed Hall of Famers Autographs", 0, 1, 0, 99, "Numbered /99 or less."),
    ("Topps Gallery of Gold Autographs", 0, 1, 0, 99, "Numbered /99 or less."),
    ("Gilded Champions", 0, 1, 0, 99, "Numbered /99 or less."),
    ("Gilded Ink", 0, 1, 0, 99, "Numbered /99 or less."),
    ("Gold Framed Hall of Famers Plaque Autographs", 0, 1, 0, 25, None),
    ("Topps Chrome Gold Autographs", 0, 1, 0, 99, "Numbered /99 or less."),
    ("Topps Chrome Cast in Gold Variation Autographs", 0, 1, 0, 199, None),
]

# subset -> [(parallel_name, print_run, note)]
AUTO_LADDER = [("Canasite", 75, None), ("Rose Gold", 50, None), ("Emerald", 25, None),
               ("Onyx", 10, None), ("Ruby", 5, None), ("Platinum", 1, None)]
PARALLELS = {
    "Base": [("Gold Wave Refractor", 75, None), ("Gold Mini-Diamond Refractor", 50, None),
             ("Gold RayWave Refractor", 25, None), ("Gold Lava Refractor", 10, None),
             ("Electroblack Refractor", 5, None), ("SuperFractor", 1, None)],
    "Gold Regalia": [("Gold Ingot", 50, None), ("Gold Bullion", 25, None), ("Gold Lava", 10, None),
                     ("Gold Dust", 5, None), ("FoilFractor", 1, None)],
    "Gold Storm": [("Gold", 1, None)],
    "Statuesque": [("Gold", 1, None), ("Gold Variation", None, "unnumbered"),
                   ("Gold Variation 1/1", 1, None)],
    "Gold Framed Hall of Famers Autographs": AUTO_LADDER,
    "Topps Gallery of Gold Autographs": AUTO_LADDER,
    "Gilded Champions": AUTO_LADDER,
    "Gilded Ink": AUTO_LADDER,
    "Gold Framed Hall of Famers Plaque Autographs": [("Onyx", 10, None), ("Ruby", 5, None), ("Platinum", 1, None)],
    "Topps Chrome Gold Autographs": [("Purple Refractor", 79, None), ("Yellow Refractor", 75, None),
                                     ("Blue Refractor", 50, None), ("Orange Refractor", 25, None),
                                     ("Black Refractor", 10, None), ("Red Refractor", 5, None),
                                     ("SuperFractor", 1, None)],
    "Topps Chrome Cast in Gold Variation Autographs": [("SuperFractor", 1, None)],
    "24K": [],
}

BOX_CONFIG = {"hobby": {"cards_per_pack": 4, "packs_per_box": 2, "boxes_per_case": 4, "autos_per_box": 2}}
RELATED = [{"url": "https://ripped.topps.com/topps-gilded-collection-baseball",
            "source": "Topps Ripped", "title": "2026 Topps Gilded Collection Baseball", "description": ""}]
TOPPS_URL = "https://www.topps.com/pages/topps-gilded-collection-baseball"


def slugify(t):
    s = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode("ascii").lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")


def main():
    rows = [json.loads(l) for l in open(JSONL) if l.strip()]
    assert len(rows) == 560, f"expected 560 rows, got {len(rows)}"

    db = sqlite3.connect(DB_PATH)
    db.execute("PRAGMA foreign_keys=ON")

    if db.execute("SELECT id FROM sets WHERE slug=? OR name=?", (SET_SLUG, SET_NAME)).fetchone():
        raise SystemExit(f"Set '{SET_SLUG}' already exists — aborting (expected INSERT of a new row).")

    try:
        cur = db.execute(
            """INSERT INTO sets (name, sport, season, league, tier, slug, is_visible,
                   sample_image_url, release_date, box_config, pack_odds, topps_url,
                   related_links, created_at)
               VALUES (?, 'Baseball', '2026', 'MLB', 'Premium', ?, 1, ?, '2026-12-25', ?, NULL, ?, ?, ?)""",
            (SET_NAME, SET_SLUG, f"/sets/{SET_SLUG}.jpg", json.dumps(BOX_CONFIG),
             TOPPS_URL, json.dumps(RELATED), "2026-11-20T12:00:00Z"),
        )
        set_id = cur.lastrowid
        print(f"Created set id {set_id} (tier Premium)")

        # subsets
        is_ids = {}
        for name, b, a, r, pr, note in SUBSETS:
            is_ids[name] = db.execute(
                """INSERT INTO insert_sets (set_id, name, is_base, is_autograph, is_relic, print_run, notes)
                   VALUES (?,?,?,?,?,?,?)""",
                (set_id, name, b, a, r, pr, note)).lastrowid
        print(f"Created {len(is_ids)} subsets")

        # players (get-or-create per (set, name))
        slug_used = set()

        def goc(name, role="athlete"):
            name = name.strip()
            r = db.execute("SELECT id FROM players WHERE set_id=? AND name=?", (set_id, name)).fetchone()
            if r:
                return r[0]
            base = slugify(name) or "player"
            s, i = base, 2
            while s in slug_used:
                s = f"{base}-{i}"; i += 1
            slug_used.add(s)
            return db.execute(
                """INSERT INTO players (set_id, name, slug, unique_cards, total_print_run,
                       one_of_ones, insert_set_count, subject_role)
                   VALUES (?,?,?,0,0,0,0,?)""",
                (set_id, name, s, role)).lastrowid

        # appearances
        for r in rows:
            subj = r["subject"].strip()
            name = NAME_FIX.get(subj, subj)          # Ichiro Suzuki kept as-is (distinct row)
            role = "coach" if name in COACH else "athlete"
            pid = goc(name, role)
            team = r.get("team")
            team = team.strip() if isinstance(team, str) and team.strip() else None
            db.execute(
                """INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team)
                   VALUES (?,?,?,?,?)""",
                (pid, is_ids[r["subset"]], str(r["card_number"]), 1 if r.get("rookie") else 0, team))

        # parallels
        npar = 0
        for sub, plist in PARALLELS.items():
            for pname, pr, note in plist:
                db.execute(
                    """INSERT INTO parallels (insert_set_id, name, print_run, exclusivity, note)
                       VALUES (?,?,?,?,?)""",
                    (is_ids[sub], pname, pr, None, note))
                npar += 1
        assert npar == 50, f"inserted {npar} parallels, expected 50"

        db.commit()
        np = db.execute("SELECT COUNT(*) FROM players WHERE set_id=?", (set_id,)).fetchone()[0]
        na = db.execute("SELECT COUNT(*) FROM player_appearances pa JOIN players p ON p.id=pa.player_id WHERE p.set_id=?", (set_id,)).fetchone()[0]
        print(f"players={np} appearances={na} parallels={npar}  set id {set_id}")
    except Exception:
        db.rollback(); raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
