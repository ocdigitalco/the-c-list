"""
Seed: 2025-26 Topps Stadium Club Basketball — full checklist (1,554 cards, 38 subsets).

Source: scratchpad/scb.jsonl (one card per line: subset, card_number, subject, team,
optional rookie, optional co_players[{subject, team}]).

Rulings applied (see Phase 0 + go):
  (a) is_base: Base + the 1-200 alternate-number subsets (Members Only I/II, Members
      Only Rookie Photo Variation, Image Variation, Design Variation) are is_base=1.
      The Stadium Club Collection *sub-brand* base runs (SBC / SCA numbering) are
      is_base=0 inserts — following Flagship Basketball 896, not WWE 902. => 6 base.
  (b) Near-miss subjects seeded under the stored canonical spelling so they merge to
      the existing athlete (NAME_FIX + NFC-normalize). Includes the two co-player
      typo fixes: Cyrillic "Egor Dёmin" -> "Egor Dëmin" and "Paolo banchero" ->
      "Paolo Banchero".
  (c) Payton Pritchard #113 moved from Base Members Only into Base Members Only II
      (where the number belongs); both land at 100 cards. Note on MO II.
  (d) Members Only Cuts is_relic=0 ("Cuts" is a design name, not a cut-signature relic).

Teams stored as printed (even apparent offseason moves / errors). No parallels, no
pack odds. Cosigners are duals: one appearance per player on the card; bidirectional
co-player links built by grouping (insert_set, card_number), matching seed.ts.

Run post-seed.ts (build-athletes -> backfill-headshots --set -> build-athletes) after
this, then migrate-to-turso.ts (full reload).
Usage: python3 scripts/seed_stadium_club_basketball_2526.py
"""
import sqlite3, os, json, re, unicodedata

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
JSONL = os.path.join(os.path.dirname(__file__), "..", "scratchpad", "scb.jsonl")

SET_NAME = "2025-26 Topps Stadium Club Basketball"
SET_SLUG = "2025-26-topps-stadium-club-basketball"
TOPPS_URL = "https://www.topps.com/pages/topps-stadium-club-basketball"

# (b) sheet spelling -> stored canonical (applied before NFC). Egor key is Cyrillic ё (U+0451).
NAME_FIX = {
    "Alperen Sengun": "Alperen Şengün",
    "Dante Exum": "Danté Exum",
    "Manu Ginobili": "Manu Ginóbili",
    "Zach Lavine": "Zach LaVine",
    "Lebron James": "LeBron James",
    "Paolo banchero": "Paolo Banchero",
    "Egor Dёmin": "Egor Dëmin",
}

# Approved fuzzy headshot matches (reviewed in scratchpad/headshot-fuzzy.csv).
# backfill-headshots holds sub-100 matches; these were human-approved and are
# written here so a fresh re-seed reproduces them (and backfill then skips them,
# since the id is no longer NULL). J.R. Smith -> nba id 2747 ("jr smith", 89).
APPROVED_NBA_IDS = {
    "J.R. Smith": 2747,
}

# (a) 6 is_base subsets
BASE_SUBSETS = {
    "Base",
    "Base Members Only",
    "Base Members Only II",
    "Base Members Only Rookie Photo Variation",
    "Base Cards Image Variation",
    "Base Cards Design Variation",
}
# 13 autograph subsets
AUTO_SUBSETS = {
    "Base Cards I Autograph Variation",
    "Base Cards II Autograph Variation",
    "Fresh Frames Autographs",
    "Legends of the Lens Autographs",
    "Ink Exposure",
    "Abstract Autographs",
    "Cosigners",
    "Lonestar Autographs",
    "Rookie Photoshoot Polaroid Signatures",
    "Rookie Takeover Autograph Parallel",
    "Base Members Only Photo Variation Autographs",
    "Stadium Club Collection Chrome Base Card Autographs",
    "Members Only Marks",
}
# no relic subsets ((d) Members Only Cuts is_relic=0)
RELIC_SUBSETS = set()

SUBSET_NOTES = {
    "Base Members Only II": "Includes #113 (Payton Pritchard), which the official sheet "
                            "listed under Members Only I; stored here where the number belongs.",
    "Oversized Stadium Club Basketball Card": "Oversized box-topper-style cards; the "
                            "configuration sheet does not state which box carries them, so no "
                            "format restriction is stored.",
}


def canon(name):
    name = name.strip()
    name = NAME_FIX.get(name, name)
    return unicodedata.normalize("NFC", name)


def slugify(t):
    s = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode("ascii")
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")


def main():
    rows = [json.loads(l) for l in open(JSONL) if l.strip()]
    assert len(rows) == 1554, f"expected 1554 rows, got {len(rows)}"

    box_config = json.dumps({
        "hobby": {"cards_per_pack": 8, "packs_per_box": 16, "autos_per_box": 1},
        "mega": {"cards_per_pack": 10, "packs_per_box": 10},
        "value_blaster": {"cards_per_pack": 10, "packs_per_box": 6},
    })

    db = sqlite3.connect(DB_PATH)
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA foreign_keys=ON")

    if db.execute("SELECT id FROM sets WHERE name = ?", (SET_NAME,)).fetchone():
        raise SystemExit(f"Set '{SET_NAME}' already exists — aborting.")

    try:
        cur = db.execute(
            """INSERT INTO sets (name, sport, season, league, tier, slug, is_visible,
                   sample_image_url, release_date, box_config, pack_odds, topps_url, created_at)
               VALUES (?, 'Basketball', '2025-26', 'NBA', 'Standard', ?, 1, ?, ?, ?, NULL, ?, ?)""",
            (SET_NAME, SET_SLUG, f"/sets/{SET_SLUG}.jpg", "2026-11-25", box_config,
             TOPPS_URL, "2026-10-27T12:00:00Z"),
        )
        set_id = cur.lastrowid
        print(f"Created set id {set_id}")

        # ── players (get-or-create per (set, canonical name)) ──
        slug_cache = {}

        def goc(name):
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
                   VALUES (?, ?, ?, 0, 0, 0, 0, 'athlete')""",
                (set_id, name, c),
            ).lastrowid

        # ── insert_sets in JSONL first-appearance order ──
        is_ids = {}
        for r in rows:
            sub = r["subset"]
            if sub in is_ids:
                continue
            is_ids[sub] = db.execute(
                """INSERT INTO insert_sets (set_id, name, is_base, is_autograph, is_relic, notes)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (set_id, sub,
                 1 if sub in BASE_SUBSETS else 0,
                 1 if sub in AUTO_SUBSETS else 0,
                 1 if sub in RELIC_SUBSETS else 0,
                 SUBSET_NOTES.get(sub)),
            ).lastrowid
        print(f"Created {len(is_ids)} subsets")

        # ── appearances (main + per co-player) ──
        for r in rows:
            card = str(r["card_number"])
            sub = r["subset"]
            # (c) move Members Only #113 into Members Only II
            if sub == "Base Members Only" and card == "113":
                sub = "Base Members Only II"
            isid = is_ids[sub]

            pid = goc(r["subject"])
            db.execute(
                """INSERT INTO player_appearances
                       (player_id, insert_set_id, card_number, is_rookie, team, subset_tag)
                   VALUES (?, ?, ?, ?, ?, NULL)""",
                (pid, isid, card, 1 if r.get("rookie") else 0, r.get("team")),
            )
            for cp in (r.get("co_players") or []):
                cpid = goc(cp["subject"])
                db.execute(
                    """INSERT INTO player_appearances
                           (player_id, insert_set_id, card_number, is_rookie, team, subset_tag)
                       VALUES (?, ?, ?, ?, ?, NULL)""",
                    (cpid, isid, card, 1 if cp.get("rookie") else 0, cp.get("team")),
                )

        # ── bidirectional co-player links (group by insert_set, card_number) ──
        groups = {}
        for app_id, isid, card, pid in db.execute(
            """SELECT pa.id, pa.insert_set_id, pa.card_number, pa.player_id
               FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
               WHERE i.set_id=?""", (set_id,)):
            groups.setdefault((isid, card), []).append((app_id, pid))
        link_count = 0
        for members in groups.values():
            if len(members) < 2:
                continue
            for app_id, _ in members:
                for other_id, other_pid in members:
                    if other_id == app_id:
                        continue
                    db.execute(
                        "INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)",
                        (app_id, other_pid))
                    link_count += 1

        # ── approved fuzzy headshot matches (see APPROVED_NBA_IDS) ──
        for approved_name, nba_id in APPROVED_NBA_IDS.items():
            db.execute(
                "UPDATE players SET nba_player_id=? WHERE set_id=? AND name=?",
                (nba_id, set_id, canon(approved_name)))

        db.commit()

        # ── verification ──
        n_sub = db.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id=?", (set_id,)).fetchone()[0]
        n_base = db.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_base=1", (set_id,)).fetchone()[0]
        n_auto = db.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_autograph=1", (set_id,)).fetchone()[0]
        n_ins = db.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_base=0 AND is_autograph=0", (set_id,)).fetchone()[0]
        n_cards = db.execute(
            """SELECT COUNT(DISTINCT pa.insert_set_id || ':' || pa.card_number)
               FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
               WHERE i.set_id=?""", (set_id,)).fetchone()[0]
        n_app = db.execute(
            """SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
               WHERE i.set_id=?""", (set_id,)).fetchone()[0]
        n_players = db.execute("SELECT COUNT(*) FROM players WHERE set_id=?", (set_id,)).fetchone()[0]
        n_rookie = db.execute(
            """SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
               WHERE i.set_id=? AND pa.is_rookie=1""", (set_id,)).fetchone()[0]
        mo1 = db.execute("""SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                            WHERE i.set_id=? AND i.name='Base Members Only'""", (set_id,)).fetchone()[0]
        mo2 = db.execute("""SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                            WHERE i.set_id=? AND i.name='Base Members Only II'""", (set_id,)).fetchone()[0]
        print(f"subsets={n_sub} (base={n_base} auto={n_auto} inserts={n_ins})")
        print(f"cards(distinct subset:card)={n_cards}  appearances={n_app}  players={n_players}")
        print(f"rookie_appearances={n_rookie}  co_links={link_count}")
        print(f"Members Only I={mo1}  Members Only II={mo2}")
        print(f"DONE. set id {set_id}")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
