"""
Seed: 2026 Topps Chrome Sapphire Tennis — new set (405 cards, 6 subsets) — AND
move Sapphire Infinite + Hidden Gems out of 2026 Topps Chrome Tennis (set 873).

Sapphire is a separate product from Chrome Tennis (873): its own release, box and
parallel ladder. Its official checklist (26TCTN) is the provenance for Sapphire
Infinite and Hidden Gems, which had been sitting in 873 — they move here.

Source: scratchpad/saph.jsonl (one card per line: subset, card_number, subject,
team (always null — tennis), optional rookie).

Rulings applied (Phase 0 + go):
  (a) tier = Sapphire (follows the ~60 Sapphire-edition sets; 873 is Chrome).
  (b) box_config: single `hobby` key, null numbers, notes "Configuration TBA"
      (a Sapphire box is the product's hobby box; matches standalone-Sapphire
      precedent, not an 885-style `sapphire` format key). pack_odds NULL.
  (c) sold_comps for insert_set_ids 2357/2358 are deleted on Turso separately,
      before migrate (handled in a scratchpad script, not here).
  (d) NAME_FIX folds the two diacritic-lost sheet spellings onto 873's canonical
      athlete: Iga Swiatek -> Iga Świątek, Karolina Muchova -> Karolína Muchová.

league NULL and tier/season mirror 873 (league NULL, season 2026). No parallels,
no pack odds, no teams. No multi-player cards in these 6 subsets.

Run post-seed.ts (build-athletes -> backfill-headshots --set -> build-athletes)
after this, then migrate-to-turso.ts (full reload, which recomputes player stats).
Usage: python3 scripts/seed_chrome_sapphire_tennis_2026.py
"""
import sqlite3, os, json, re, unicodedata

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
JSONL = os.path.join(os.path.dirname(__file__), "..", "scratchpad", "saph.jsonl")

SET_NAME = "2026 Topps Chrome Sapphire Tennis"
SET_SLUG = "2026-topps-chrome-sapphire-tennis"

CHROME_SLUG = "2026-topps-chrome-tennis"          # set 873
MOVE_SUBSETS = ("Sapphire Infinite", "Hidden Gems")

# (d) sheet spelling -> 873 stored canonical (applied before NFC).
NAME_FIX = {
    "Iga Swiatek": "Iga Świątek",
    "Karolina Muchova": "Karolína Muchová",
}

BASE_SUBSETS = {"Base Cards", "Base Cards II"}
AUTO_SUBSETS = {"Base Autographs I", "Base Autographs II"}
# Sapphire Infinite, Hidden Gems -> inserts (0/0/0)


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
    assert len(rows) == 405, f"expected 405 rows, got {len(rows)}"

    box_config = json.dumps({
        "hobby": {"cards_per_pack": None, "packs_per_box": None,
                  "boxes_per_case": None, "notes": "Configuration TBA."},
    })

    db = sqlite3.connect(DB_PATH)
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA foreign_keys=ON")

    if db.execute("SELECT id FROM sets WHERE name = ?", (SET_NAME,)).fetchone():
        raise SystemExit(f"Set '{SET_NAME}' already exists — aborting.")
    chrome_id = db.execute("SELECT id FROM sets WHERE slug=?", (CHROME_SLUG,)).fetchone()
    if not chrome_id:
        raise SystemExit(f"Chrome Tennis set '{CHROME_SLUG}' not found — aborting.")
    chrome_id = chrome_id[0]

    try:
        cur = db.execute(
            """INSERT INTO sets (name, sport, season, league, tier, slug, is_visible,
                   sample_image_url, release_date, box_config, pack_odds, topps_url, created_at)
               VALUES (?, 'Tennis', '2026', NULL, 'Sapphire', ?, 1, ?, NULL, ?, NULL, NULL, ?)""",
            (SET_NAME, SET_SLUG, f"/sets/{SET_SLUG}.jpg", box_config, "2026-10-28T12:00:00Z"),
        )
        set_id = cur.lastrowid
        print(f"Created set id {set_id}")

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

        # insert_sets in JSONL first-appearance order
        is_ids = {}
        for r in rows:
            sub = r["subset"]
            if sub in is_ids:
                continue
            is_ids[sub] = db.execute(
                """INSERT INTO insert_sets (set_id, name, is_base, is_autograph, is_relic, notes)
                   VALUES (?, ?, ?, ?, 0, NULL)""",
                (set_id, sub, 1 if sub in BASE_SUBSETS else 0, 1 if sub in AUTO_SUBSETS else 0),
            ).lastrowid
        print(f"Created {len(is_ids)} subsets")

        # appearances
        for r in rows:
            pid = goc(r["subject"])
            db.execute(
                """INSERT INTO player_appearances
                       (player_id, insert_set_id, card_number, is_rookie, team, subset_tag)
                   VALUES (?, ?, ?, ?, NULL, NULL)""",
                (pid, is_ids[r["subset"]], str(r["card_number"]), 1 if r.get("rookie") else 0),
            )

        # ── move the two subsets out of 873 ──
        two = [r[0] for r in db.execute(
            f"SELECT id FROM insert_sets WHERE set_id=? AND name IN ({','.join('?'*len(MOVE_SUBSETS))})",
            (chrome_id, *MOVE_SUBSETS))]
        print(f"873 subsets to remove: {two}")
        ph = ",".join("?" * len(two))
        removed_apps = db.execute(
            f"SELECT COUNT(*) FROM player_appearances WHERE insert_set_id IN ({ph})", two).fetchone()[0]
        db.execute(
            f"""DELETE FROM appearance_co_players WHERE appearance_id IN
                (SELECT id FROM player_appearances WHERE insert_set_id IN ({ph}))""", two)
        db.execute(f"DELETE FROM player_appearances WHERE insert_set_id IN ({ph})", two)
        db.execute(f"DELETE FROM parallels WHERE insert_set_id IN ({ph})", two)
        db.execute(f"DELETE FROM insert_sets WHERE id IN ({ph})", two)
        # any 873 players now orphaned (zero appearances)? Phase 0 said none; enforce.
        orphans = [r[0] for r in db.execute(
            """SELECT p.id FROM players p WHERE p.set_id=? AND NOT EXISTS
               (SELECT 1 FROM player_appearances pa WHERE pa.player_id=p.id)""", (chrome_id,))]
        if orphans:
            print(f"removing {len(orphans)} orphaned 873 players: {orphans}")
            oph = ",".join("?" * len(orphans))
            db.execute(f"DELETE FROM player_events WHERE player_id IN ({oph})", orphans)
            db.execute(f"DELETE FROM players WHERE id IN ({oph})", orphans)
        print(f"Removed {removed_apps} appearances / {len(two)} subsets / {len(orphans)} orphans from 873")

        db.commit()

        # ── verification ──
        def one(sql, args=()):
            return db.execute(sql, args).fetchone()[0]
        n_sub = one("SELECT COUNT(*) FROM insert_sets WHERE set_id=?", (set_id,))
        n_base = one("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_base=1", (set_id,))
        n_auto_apps = one("""SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                             WHERE i.set_id=? AND i.is_autograph=1""", (set_id,))
        n_base_apps = one("""SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                             WHERE i.set_id=? AND i.is_base=1""", (set_id,))
        n_cards = one("""SELECT COUNT(DISTINCT pa.insert_set_id||':'||pa.card_number)
                         FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                         WHERE i.set_id=?""", (set_id,))
        n_app = one("""SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                       WHERE i.set_id=?""", (set_id,))
        n_players = one("SELECT COUNT(*) FROM players WHERE set_id=?", (set_id,))
        n_rookie = one("""SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                          WHERE i.set_id=? AND pa.is_rookie=1""", (set_id,))
        chrome_cards = one("""SELECT COUNT(DISTINCT i.name||':'||pa.card_number)
                              FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                              WHERE i.set_id=?""", (chrome_id,))
        chrome_subs = one("SELECT COUNT(*) FROM insert_sets WHERE set_id=?", (chrome_id,))
        chrome_moved = one(f"""SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND name IN
                               ({','.join('?'*len(MOVE_SUBSETS))})""", (chrome_id, *MOVE_SUBSETS))
        print(f"NEW set {set_id}: subsets={n_sub} (base={n_base}) base_apps={n_base_apps} "
              f"auto_apps={n_auto_apps} rookies={n_rookie}")
        print(f"  cards(distinct)={n_cards} appearances={n_app} players={n_players}")
        print(f"873: subsets={chrome_subs} cards={chrome_cards} moved-subsets-remaining={chrome_moved}")
        print(f"DONE. new set id {set_id}")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
