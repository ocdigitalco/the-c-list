"""
Seed: 2025-26 Topps Stadium Club Chrome UEFA Champions League — new set
(459 cards, 18 subsets, 110 parallels, three box configs, pack_odds NULL).

Sources:
  scratchpad/scc.jsonl    — 459 cards (subset, card_number, subject, team, optional
                            rookie, co_players, subject_role). Source of truth for cards.
  scratchpad/sccpars.jsonl — 110 parallels (subset, name, print_run, exclusivity).
                            Source for parallels + print runs only.

Rulings applied (Phase 0 + go):
  tier Chrome  — matches the 2024 predecessor (set 268) and the product name
                 ("Stadium Club Chrome"); NOT Standard.
  league UEFA  — matches the UEFA batch (880 etc.).
  NAME_FIX     — "Heung-min Son" -> "Heung-Min Son" (stored canonical; base + DA-SB
                 co-player); "Federico DiMarco" -> "Federico Dimarco" (stored canonical,
                 both CA-FDM and BTA-FDM).
  U+200B strip — 7 "Atlético de Madrid" rows carry a trailing zero-width space; stripped
                 to the stored form.
  coach role   — Luis Enrique only (BTA-LE @ PSG, a manager-only depiction). Guardiola,
                 Deschamps, Simeone stay athlete (Classic Kits = their playing days).
  event role   — UFS-1 Puskás Aréna (subject_role=event, team NULL), per the F1 ruling.
  subset /99   — Classic Kits Autographs and Marks of Excellence base cards are /99
                 (insert_sets.print_run).
  formats      — per-subset availability written to player_appearances.formats (see FORMATS).
  pack_odds    — NULL (none published).

Four Members Only TBA subsets (Champions Club, Image Variations, CC Autographs,
Image Variations Autographs) are OMITTED — no published checklists and no odds.

Run post-seed.ts then migrate-to-turso.ts (full reload, recomputes stats).
Usage: python3 scripts/seed_stadium_club_chrome_ucl_2526.py
"""
import sqlite3, os, json, re, unicodedata

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
JSONL = os.path.join(os.path.dirname(__file__), "..", "scratchpad", "scc.jsonl")
PARS = os.path.join(os.path.dirname(__file__), "..", "scratchpad", "sccpars.jsonl")

SET_NAME = "2025-26 Topps Stadium Club Chrome UEFA Champions League"
SET_SLUG = "2025-26-topps-stadium-club-chrome-uefa-champions-league"
TOPPS_URL = "https://www.topps.com/pages/topps-stadium-club-chrome-uefa-champions-league"

NAME_FIX = {
    "Heung-min Son": "Heung-Min Son",
    "Federico DiMarco": "Federico Dimarco",
}
ROLE_OVERRIDE = {"Luis Enrique": "coach"}

BASE_SUBSETS = {"Base"}
AUTO_SUBSETS = {
    "Chrome Autographs", "Behind the Lens Autographs", "Dual Autographs",
    "Classic Kits Autographs", "Marks of Excellence", "Stadium Spirit Autographed Relics",
}
RELIC_SUBSETS = {"Stadium Spirit Seat Relics", "Stadium Spirit Autographed Relics"}
SUBSET_PRINT_RUN = {"Classic Kits Autographs": 99, "Marks of Excellence": 99}

FORMATS = {
    "Behind the Lens Autographs": ["hobby", "value_blaster"],
    "Dual Autographs": ["hobby", "value_blaster"],
    "UCL Final Stadium": ["hobby", "value_blaster"],
    "Classic Kits Autographs": ["hobby", "members_only"],
    "Stadium Spirit Seat Relics": ["hobby", "members_only"],
    "Stadium Spirit Autographed Relics": ["hobby", "members_only"],
    "The Grail": ["hobby"],
}

SUBSET_NOTES = {
    "The Grail": "Single card (G-6); 'continuation' numbering across Topps UCL products, stored as printed.",
    "Marks of Excellence": "ME-/MOE- continuation numbering as printed; base cards numbered /99.",
    "UCL Final Stadium": "Event card — Puskás Aréna (2025 UCL Final venue); subject stored with role=event, team NULL.",
    "Classic Kits Autographs": "Base cards numbered /99.",
}

BOX_CONFIG = {
    "hobby": {
        "cards_per_pack": 6, "packs_per_box": 20, "boxes_per_case": 12, "autos_per_box": 1,
        "notes": "Per box: 1 autograph, 4 Refractor parallels, 1 numbered Electric Charge "
                 "parallel, 3-4 additional parallels or image variations, and 10 inserts.",
    },
    "members_only": {
        "cards_per_pack": 12, "packs_per_box": 1, "boxes_per_case": 12, "autos_per_box": 2,
        "notes": "Members Only exclusive box. Per box: 1 exclusive stamped autograph + 1 "
                 "additional autograph, 1 exclusive Champions Club insert, 3 exclusive base "
                 "parallels, and 6 exclusive base Refractor parallels.",
    },
    "value_blaster": {
        "cards_per_pack": 4, "packs_per_box": 7, "boxes_per_case": 40,
        "notes": "Value Blaster. Per box: 1 numbered parallel, 4 exclusive Base RayWave "
                 "Refractors, 1 Base Refractor, and 3 inserts.",
    },
}


def canon(name):
    if name is None:
        return None
    name = name.replace("​", "").replace("‌", "").replace("﻿", "")
    name = unicodedata.normalize("NFC", name.strip())
    return NAME_FIX.get(name, name)


def norm_team(t):
    if not t:
        return None
    t = t.replace("​", "").replace("‌", "").replace("﻿", "")
    return unicodedata.normalize("NFC", t.strip())


def slugify(t):
    s = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^\w\s-]", "", s.lower().strip())
    s = re.sub(r"[\s_]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")


def main():
    rows = [json.loads(l) for l in open(JSONL) if l.strip()]
    pars = [json.loads(l) for l in open(PARS) if l.strip()]
    assert len(rows) == 459, f"expected 459 cards, got {len(rows)}"
    assert len(pars) == 110, f"expected 110 parallels, got {len(pars)}"

    db = sqlite3.connect(DB_PATH)
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA foreign_keys=ON")

    if db.execute("SELECT id FROM sets WHERE name = ?", (SET_NAME,)).fetchone():
        raise SystemExit(f"Set '{SET_NAME}' already exists — aborting.")

    try:
        cur = db.execute(
            """INSERT INTO sets (name, sport, season, league, tier, slug, is_visible,
                   sample_image_url, release_date, box_config, pack_odds, topps_url, created_at)
               VALUES (?, 'Soccer', '2025-26', 'UEFA', 'Chrome', ?, 1, ?, ?, ?, NULL, ?, ?)""",
            (SET_NAME, SET_SLUG, f"/sets/{SET_SLUG}.jpg", "2026-11-04",
             json.dumps(BOX_CONFIG), TOPPS_URL, "2026-11-02T12:00:00Z"),
        )
        set_id = cur.lastrowid
        print(f"Created set id {set_id}")

        slug_cache = {}

        def goc(name, role="athlete"):
            name = canon(name)
            r = db.execute("SELECT id FROM players WHERE set_id=? AND name=?", (set_id, name)).fetchone()
            if r:
                return r[0]
            base = slugify(name) or "player"
            c, i = base, 2
            while c in slug_cache:
                c = f"{base}-{i}"; i += 1
            slug_cache[c] = True
            return db.execute(
                """INSERT INTO players (set_id, name, slug, unique_cards, total_print_run,
                       one_of_ones, insert_set_count, subject_role)
                   VALUES (?, ?, ?, 0, 0, 0, 0, ?)""",
                (set_id, name, c, role),
            ).lastrowid

        # insert_sets in first-appearance order
        is_ids = {}
        for r in rows:
            sub = r["subset"]
            if sub in is_ids:
                continue
            is_ids[sub] = db.execute(
                """INSERT INTO insert_sets (set_id, name, is_base, is_autograph, is_relic,
                       print_run, notes)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (set_id, sub, 1 if sub in BASE_SUBSETS else 0,
                 1 if sub in AUTO_SUBSETS else 0, 1 if sub in RELIC_SUBSETS else 0,
                 SUBSET_PRINT_RUN.get(sub), SUBSET_NOTES.get(sub)),
            ).lastrowid
        print(f"Created {len(is_ids)} subsets")

        # appearances (subject + co-players). group[(insert_set_id, card_number)] = [player_id,...]
        groups = {}
        app_count = 0
        for r in rows:
            sub = r["subset"]
            iid = is_ids[sub]
            card = str(r["card_number"])
            fmt = json.dumps(FORMATS[sub]) if sub in FORMATS else None

            def add_appearance(name, team, rookie, role):
                nonlocal app_count
                pid = goc(name, role)
                db.execute(
                    """INSERT INTO player_appearances
                           (player_id, insert_set_id, card_number, is_rookie, team, subset_tag, formats)
                       VALUES (?, ?, ?, ?, ?, NULL, ?)""",
                    (pid, iid, card, 1 if rookie else 0, norm_team(team), fmt),
                )
                app_count += 1
                groups.setdefault((iid, card), []).append(pid)

            role = ROLE_OVERRIDE.get(canon(r["subject"]), r.get("subject_role") or "athlete")
            add_appearance(r["subject"], r.get("team"), r.get("rookie"), role)
            for co in (r.get("co_players") or []):
                crole = ROLE_OVERRIDE.get(canon(co["subject"]), "athlete")
                add_appearance(co["subject"], co.get("team"), False, crole)
        print(f"Inserted {app_count} appearance rows across {len(groups)} distinct cards")

        # co-player links: each appearance -> every other player on the same card
        nlinks = 0
        for (iid, card), pids in groups.items():
            if len(pids) < 2:
                continue
            approws = db.execute(
                "SELECT id, player_id FROM player_appearances WHERE insert_set_id=? AND card_number=?",
                (iid, card)).fetchall()
            for app_id, player_id in approws:
                for other in pids:
                    if other != player_id:
                        db.execute(
                            "INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)",
                            (app_id, other))
                        nlinks += 1
        print(f"Created {nlinks} co-player links")

        # parallels
        npar = 0
        for p in pars:
            db.execute(
                "INSERT INTO parallels (insert_set_id, name, print_run, exclusivity) VALUES (?, ?, ?, ?)",
                (is_ids[p["subset"]], p["name"], p.get("print_run"), p.get("exclusivity")))
            npar += 1
        print(f"Created {npar} parallel rows")

        db.commit()

        # ── verification ──
        def one(sql, args=()):
            return db.execute(sql, args).fetchone()[0]
        n_sub = one("SELECT COUNT(*) FROM insert_sets WHERE set_id=?", (set_id,))
        n_base = one("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_base=1", (set_id,))
        n_auto = one("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_autograph=1", (set_id,))
        n_relic = one("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_relic=1", (set_id,))
        n_ins = one("""SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_base=0
                       AND is_autograph=0 AND is_relic=0""", (set_id,))
        n_cards = one("""SELECT COUNT(DISTINCT pa.insert_set_id||':'||pa.card_number)
                         FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                         WHERE i.set_id=?""", (set_id,))
        base_cards = one("""SELECT COUNT(DISTINCT pa.card_number) FROM player_appearances pa
                            JOIN insert_sets i ON i.id=pa.insert_set_id WHERE i.set_id=? AND i.is_base=1""", (set_id,))
        n_rookie = one("""SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                          WHERE i.set_id=? AND pa.is_rookie=1""", (set_id,))
        n_players = one("SELECT COUNT(*) FROM players WHERE set_id=?", (set_id,))
        dual_cards = one("""SELECT COUNT(DISTINCT pa.card_number) FROM player_appearances pa
                            JOIN insert_sets i ON i.id=pa.insert_set_id
                            WHERE i.set_id=? AND i.name='Dual Autographs'""", (set_id,))
        n_links = one("""SELECT COUNT(*) FROM appearance_co_players acp
                         JOIN player_appearances pa ON pa.id=acp.appearance_id
                         JOIN insert_sets i ON i.id=pa.insert_set_id WHERE i.set_id=?""", (set_id,))
        n_par = one("""SELECT COUNT(*) FROM parallels pr JOIN insert_sets i ON i.id=pr.insert_set_id
                       WHERE i.set_id=?""", (set_id,))
        n_par_num = one("""SELECT COUNT(*) FROM parallels pr JOIN insert_sets i ON i.id=pr.insert_set_id
                           WHERE i.set_id=? AND pr.print_run IS NOT NULL""", (set_id,))
        n_subpr = one("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND print_run IS NOT NULL", (set_id,))
        dup = one("""SELECT COUNT(*) FROM (SELECT pa.insert_set_id, pa.card_number
                     FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                     WHERE i.set_id=? GROUP BY pa.insert_set_id, pa.card_number, pa.player_id HAVING COUNT(*)>1)""", (set_id,))
        event_null = one("""SELECT (SELECT subject_role FROM players WHERE set_id=? AND name='Puskás Aréna')
                            ||'/'|| COALESCE((SELECT team FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                               WHERE i.set_id=? AND pa.card_number='UFS-1'),'NULL')""", (set_id, set_id))
        enrique_role = one("SELECT subject_role FROM players WHERE set_id=? AND name='Luis Enrique'", (set_id,))
        dimarco = one("SELECT COUNT(*) FROM players WHERE set_id=? AND name='Federico Dimarco'", (set_id,))
        son = one("SELECT COUNT(*) FROM players WHERE set_id=? AND name='Heung-Min Son'", (set_id,))
        atletico_zw = one("""SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                             WHERE i.set_id=? AND pa.team LIKE '%'||char(8203)||'%'""", (set_id,))
        print(f"subsets={n_sub} (base={n_base} auto={n_auto} relic={n_relic} insert={n_ins}) "
              f"cards={n_cards} base_cards={base_cards} rookies={n_rookie} players={n_players}")
        print(f"dual_cards={dual_cards} colinks={n_links} parallels={n_par} (numbered={n_par_num}) "
              f"subset_printruns={n_subpr} dup_rows={dup}")
        print(f"spotcheck: UFS-1 role/team={event_null} | Luis Enrique role={enrique_role} | "
              f"Federico Dimarco rows={dimarco} | Heung-Min Son rows={son} | zero-width teams={atletico_zw}")
        print(f"DONE. set id {set_id}")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
