"""
Seed: 2026 Bowman Football Sapphire Edition — new standalone Sapphire set
(608 cards, 11 subsets, 44 numbered/NULL parallels, 54 hobby odds keys).

Chrome parent: 2026 Bowman Football (set 874). Sapphire is its own product, so it
is a new set (tier Sapphire), not formats on 874.

Sources:
  scratchpad/bwfs.jsonl     — 608 cards (subset, card_number, subject, team as
                              printed incl. ®/™, optional rookie).
  scratchpad/bwfsodds.jsonl — 54 odds lines (subset, parallel [null=base], odds
                              "1:X", format "hobby", print_run).

Rulings applied (Phase 0 + go):
  (1) league NULL — matches 874 (874's league is NULL, not "NFL").
  (2) Gladding fix (option B): 874 stored the name truncated as
      "Na'eem Abdul-Rahim Gladdi"; this run corrects 874's player row to the full
      "Na'eem Abdul-Rahim Gladding" so build-athletes rebuilds one correct athlete,
      and Sapphire seeds the same full name.
  (3) Sapphire Selections Autographs NIL = 9 (the sheet's authoritative count).
  (4) Bo Jackson here is the Ohio State prospect — a *new Football athlete*,
      distinct from the Baseball legend; build-athletes gives the loser of the
      bare-slug collision a "-<sport>" slug (never auto-merges across sport).

Teams normalized to 874's stored forms: strip ®/™, plus specials
  "Texas A&M University" -> "Texas A&M", "Uconn" -> "UConn".
subject_role = 'athlete' for everyone (matches 874). No relics.

Parallels created ONLY where the odds sheet lists them (standing rule): 44 rows,
40 numbered + 4 NULL (Hidden Gems Emerald/Onyx/Ruby/Padparadscha). Hidden Gems is
a versions-only subset (no base odds key). Odds keys: "<Subset> Base" for the base
version, "<Subset> <Parallel>" for parallels (matches 874's convention).

Run post-seed.ts then migrate-to-turso.ts (full reload, recomputes stats).
Usage: python3 scripts/seed_bowman_football_sapphire_2026.py
"""
import sqlite3, os, json, re, unicodedata

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
JSONL = os.path.join(os.path.dirname(__file__), "..", "scratchpad", "bwfs.jsonl")
ODDS = os.path.join(os.path.dirname(__file__), "..", "scratchpad", "bwfsodds.jsonl")

SET_NAME = "2026 Bowman Football Sapphire Edition"
SET_SLUG = "2026-bowman-football-sapphire-edition"
TOPPS_URL = "https://www.topps.com/pages/bowman-football-sapphire-edition"
CHROME_ID = 874

# (2) 874 truncation fix
GLADDI_WRONG = "Na'eem Abdul-Rahim Gladdi"
GLADDI_RIGHT = "Na'eem Abdul-Rahim Gladding"

TEAM_SPECIAL = {"Texas A&M University": "Texas A&M", "Uconn": "UConn"}

BASE_SUBSETS = {"Chrome Prospects", "Chrome NFL Base", "Chrome Rookie Base"}
AUTO_SUBSETS = {
    "Base Chrome Autographs", "Base Chrome Rookie Autographs",
    "Chrome Prospect Autographs", "Sapphire Selections Autographs NFL",
    "Sapphire Selections Autographs NIL",
}
# inserts: Hidden Gems, Treasured Talent NFL, Treasured Talent NIL

SUBSET_NOTES = {
    "Hidden Gems": "Versions-only subset: no base Sapphire version — exists only as "
                   "Emerald / Onyx / Ruby / Padparadscha. Those four print runs are not "
                   "published (Padparadscha here is named without 'Sapphire' and is not "
                   "assumed 1/1).",
}


def canon(name):
    return unicodedata.normalize("NFC", name.strip())


def norm_team(t):
    if not t:
        return None
    t = t.replace("®", "").replace("™", "").strip()  # ® ™
    t = re.sub(r"^(The )?University of ", "", t).strip()       # -> "Oklahoma", "South Carolina"
    return TEAM_SPECIAL.get(t, t)


def slugify(t):
    s = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^\w\s-]", "", s.lower().strip())
    s = re.sub(r"[\s_]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")


def odds_denom(s):
    return int(s.split(":")[1])


def main():
    rows = [json.loads(l) for l in open(JSONL) if l.strip()]
    odds = [json.loads(l) for l in open(ODDS) if l.strip()]
    assert len(rows) == 608, f"expected 608 cards, got {len(rows)}"
    assert len(odds) == 54, f"expected 54 odds lines, got {len(odds)}"

    box_config = json.dumps({
        "hobby": {"cards_per_pack": 4, "packs_per_box": 8, "boxes_per_case": 10,
                  "autos_per_box": 1},
    })
    # pack_odds.hobby: base + parallel keys
    hobby = {}
    for o in odds:
        key = f"{o['subset']} Base" if o["parallel"] is None else f"{o['subset']} {o['parallel']}"
        hobby[key] = odds_denom(o["odds"])
    assert len(hobby) == 54, f"expected 54 odds keys, got {len(hobby)}"
    pack_odds = json.dumps({"hobby": hobby})

    db = sqlite3.connect(DB_PATH)
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA foreign_keys=ON")

    if db.execute("SELECT id FROM sets WHERE name = ?", (SET_NAME,)).fetchone():
        raise SystemExit(f"Set '{SET_NAME}' already exists — aborting.")

    try:
        # (2) fix 874's truncated Gladding player row(s)
        gl = db.execute("SELECT id, slug FROM players WHERE set_id=? AND name=?",
                        (CHROME_ID, GLADDI_WRONG)).fetchall()
        for pid, _ in gl:
            db.execute("UPDATE players SET name=?, slug=? WHERE id=?",
                       (GLADDI_RIGHT, slugify(GLADDI_RIGHT), pid))
        print(f"874 Gladding fix: updated {len(gl)} player row(s) -> '{GLADDI_RIGHT}'")

        cur = db.execute(
            """INSERT INTO sets (name, sport, season, league, tier, slug, is_visible,
                   sample_image_url, release_date, box_config, pack_odds, topps_url, created_at)
               VALUES (?, 'Football', '2026', NULL, 'Sapphire', ?, 1, ?, ?, ?, ?, ?, ?)""",
            (SET_NAME, SET_SLUG, f"/sets/{SET_SLUG}.jpg", "2026-11-29", box_config,
             pack_odds, TOPPS_URL, "2026-11-01T12:00:00Z"),
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

        # insert_sets in first-appearance order
        is_ids = {}
        for r in rows:
            sub = r["subset"]
            if sub in is_ids:
                continue
            is_ids[sub] = db.execute(
                """INSERT INTO insert_sets (set_id, name, is_base, is_autograph, is_relic, notes)
                   VALUES (?, ?, ?, ?, 0, ?)""",
                (set_id, sub, 1 if sub in BASE_SUBSETS else 0, 1 if sub in AUTO_SUBSETS else 0,
                 SUBSET_NOTES.get(sub)),
            ).lastrowid
        print(f"Created {len(is_ids)} subsets")

        # appearances
        for r in rows:
            pid = goc(r["subject"])
            db.execute(
                """INSERT INTO player_appearances
                       (player_id, insert_set_id, card_number, is_rookie, team, subset_tag)
                   VALUES (?, ?, ?, ?, ?, NULL)""",
                (pid, is_ids[r["subset"]], str(r["card_number"]),
                 1 if r.get("rookie") else 0, norm_team(r.get("team"))),
            )

        # parallels: one row per (subset, parallel) from the odds sheet
        npar = 0
        for o in odds:
            if o["parallel"] is None:
                continue
            db.execute(
                "INSERT INTO parallels (insert_set_id, name, print_run) VALUES (?, ?, ?)",
                (is_ids[o["subset"]], o["parallel"], o.get("print_run")),
            )
            npar += 1
        print(f"Created {npar} parallel rows")

        db.commit()

        # ── verification ──
        def one(sql, args=()):
            return db.execute(sql, args).fetchone()[0]
        n_sub = one("SELECT COUNT(*) FROM insert_sets WHERE set_id=?", (set_id,))
        n_base = one("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_base=1", (set_id,))
        n_auto = one("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_autograph=1", (set_id,))
        n_ins = one("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_base=0 AND is_autograph=0", (set_id,))
        n_cards = one("""SELECT COUNT(DISTINCT pa.insert_set_id||':'||pa.card_number)
                         FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                         WHERE i.set_id=?""", (set_id,))
        base_apps = one("""SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                           WHERE i.set_id=? AND i.is_base=1""", (set_id,))
        n_rookie = one("""SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                          WHERE i.set_id=? AND pa.is_rookie=1""", (set_id,))
        n_players = one("SELECT COUNT(*) FROM players WHERE set_id=?", (set_id,))
        n_par = one("""SELECT COUNT(*) FROM parallels pr JOIN insert_sets i ON i.id=pr.insert_set_id
                       WHERE i.set_id=?""", (set_id,))
        n_par_num = one("""SELECT COUNT(*) FROM parallels pr JOIN insert_sets i ON i.id=pr.insert_set_id
                           WHERE i.set_id=? AND pr.print_run IS NOT NULL""", (set_id,))
        hg_base = one("""SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND name='Hidden Gems'""", (set_id,))
        dup = one("""SELECT COUNT(*) FROM (SELECT pa.insert_set_id, pa.card_number
                     FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                     WHERE i.set_id=? GROUP BY pa.insert_set_id, pa.card_number HAVING COUNT(*)>1)""", (set_id,))
        print(f"subsets={n_sub} (base={n_base} auto={n_auto} insert={n_ins}) cards={n_cards} "
              f"base_apps={base_apps} rookies={n_rookie} players={n_players}")
        print(f"parallels={n_par} (numbered={n_par_num} null={n_par-n_par_num}) odds_keys={len(hobby)} "
              f"dups={dup} hidden_gems_exists={hg_base}")
        print(f"DONE. set id {set_id}")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
