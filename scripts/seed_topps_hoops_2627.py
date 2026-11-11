"""
Seed: 2026-27 Topps Hoops Basketball — full checklist (1,115 cards, 35 subsets).

Source: scratchpad/hoops.jsonl (one card per line: subset, card_number, subject,
team, optional rookie, optional co_players[{subject, team}], optional subject_role).
Parsed from the official Topps checklist CheckList_26HOOP_FINAL.pdf.

Rulings applied (Phase 0 report + go, 2026-11-10):
  (a) 3 base subsets as printed: Base Cards (1-200, rookies 211-260 flagged),
      Base Cards Highlights (261-270), Base Cards All Stars (271-300) — one
      continuous 1-300 numbering, stored as three subsets (834 / 909 precedent).
  (b) 10 autograph subsets (is_autograph=1). Rookie Duals / Rookie Triples /
      Rookie-Veteran Duals are AUTOGRAPHS per the go-ruling — prior Hoops 834
      stored them as plain inserts (is_autograph=0); the prompt overrides, as
      these are signed cards. Gate: 3 base / 10 auto / 22 insert = 35.
  (c) Finals Pursuit kept as SEVEN subsets as printed (First Round, Second Round,
      Semi Finals, The Finals, NBA Championship Players, NBA Championship Team,
      Final MVP) — 834 collapsed them into one; prompt overrides. The shared FP-
      numbering stays unique because (insert_set, card_number) is unique.
  (d) Duals/triples use one appearance per player on the card; bidirectional
      co-player links built by grouping (insert_set, card_number), matching
      seed.ts. 10 Rookie Duals + 5 Rookie-Veteran Duals (2 members each) + 5
      Rookie Triples (3 members each) => links = 10*2 + 5*6 + 5*2 = 60.
  (e) FP-99 NBA Championship Team (New York Knicks) carries subject_role='team'
      (row-level). All other subjects are 'athlete'. Builds to a page_kind='team'
      athlete, like the existing Racing/NFL team rows.
  (f) Near-miss subjects seeded under their SHEET spelling so the review queue
      (data/athlete-review-queue.csv) merges them to the stored canonical and the
      sheet form becomes an alias:
        - "Jimmy Butler"           -> Jimmy Butler III   (new queue_id 363, merge)
        - "Zach Lavine"            -> Zach LaVine         (existing queue_id 104)
        - "Kristaps Porzingis"     -> Kristaps Porziņģis  (existing queue_id 110)
        - "Alperen Sengun"         -> Alperen Şengün      (existing queue_id 115)
        - "P.J. Washington"        -> P.J. Washington Jr. (existing queue_id 123)
        - "Christian Anderson Jr." -> Christian Anderson  (existing queue_id 138)
      All other near-misses matched an existing canonical or alias exactly; the
      ~26 genuinely new athletes are the 2026 draft class + first-time legends.

Set facts: tier Standard (Hoops 834 precedent); league NBA; season 2026-27;
release_date 2026-12-10. box_config four formats (hobby/mega/value/hanger). No
pack odds, no parallels yet (release a month out -> Last Sold guard gates it).
pack_odds NULL. topps_url NULL (not supplied).

Run post-seed.ts (build-athletes -> backfill-headshots --set -> build-athletes)
after this, then migrate-to-turso.ts --set 2026-27-topps-hoops-basketball.
Usage: python3 scripts/seed_topps_hoops_2627.py
"""
import sqlite3, os, json, re, unicodedata

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
JSONL = os.path.join(os.path.dirname(__file__), "..", "scratchpad", "hoops.jsonl")

SET_NAME = "2026-27 Topps Hoops Basketball"
SET_SLUG = "2026-27-topps-hoops-basketball"

# (f) No in-seed NAME_FIX: near-misses keep their sheet spelling and merge via the
# review queue so the sheet form is preserved as an alias. canon() still NFC-folds.
NAME_FIX = {}

# (a) 3 is_base subsets
BASE_SUBSETS = {
    "Base Cards",
    "Base Cards Highlights",
    "Base Cards All Stars",
}
# (b) 10 autograph subsets (incl. Rookie Duals / Triples / Rookie-Veteran Duals)
AUTO_SUBSETS = {
    "Base Hoops Signatures",
    "Base Hoops Signatures Rookies",
    "Curated Signatures",
    "Hoops Hyper Signatures",
    "Hoops Rookie First Signs",
    "Hoops Rookie Signatures",
    "Hoops Signs",
    "Hoops Rookie Duals",
    "Hoops Rookie Triples",
    "Hoops Rookie Veteran Duals",
}
# no relic subsets
RELIC_SUBSETS = set()

SUBSET_NOTES = {}


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
    assert len(rows) == 1115, f"expected 1115 rows, got {len(rows)}"

    box_config = json.dumps({
        "hobby":  {"cards_per_pack": 6,  "packs_per_box": 20, "boxes_per_case": 12, "autos_per_box": 1},
        "mega":   {"cards_per_pack": 6,  "packs_per_box": 12, "boxes_per_case": 20},
        "value":  {"cards_per_pack": 6,  "packs_per_box": 7},
        "hanger": {"cards_per_pack": 20, "packs_per_box": 1},
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
               VALUES (?, 'Basketball', '2026-27', 'NBA', 'Standard', ?, 1, ?, ?, ?, NULL, NULL, ?)""",
            (SET_NAME, SET_SLUG, f"/sets/{SET_SLUG}.jpg", "2026-12-10", box_config,
             "2026-11-10T12:00:00Z"),
        )
        set_id = cur.lastrowid
        print(f"Created set id {set_id}")

        # ── players (get-or-create per (set, canonical name)); role from row ──
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
            isid = is_ids[r["subset"]]

            pid = goc(r["subject"], r.get("subject_role") or "athlete")
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

        db.commit()

        # ── verification ──
        def q1(sql, *a):
            return db.execute(sql, a).fetchone()[0]

        n_sub = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=?", set_id)
        n_base = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_base=1", set_id)
        n_auto = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_autograph=1", set_id)
        n_ins = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_base=0 AND is_autograph=0", set_id)
        n_cards = q1("""SELECT COUNT(DISTINCT pa.insert_set_id || ':' || pa.card_number)
                        FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                        WHERE i.set_id=?""", set_id)
        n_app = q1("""SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                      WHERE i.set_id=?""", set_id)
        n_players = q1("SELECT COUNT(*) FROM players WHERE set_id=?", set_id)
        n_rookie = q1("""SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                         WHERE i.set_id=? AND pa.is_rookie=1""", set_id)
        n_duals = q1("""SELECT COUNT(*) FROM (
                          SELECT pa.insert_set_id, pa.card_number
                          FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                          WHERE i.set_id=? GROUP BY pa.insert_set_id, pa.card_number
                          HAVING COUNT(*)=2)""", set_id)
        n_triples = q1("""SELECT COUNT(*) FROM (
                          SELECT pa.insert_set_id, pa.card_number
                          FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                          WHERE i.set_id=? GROUP BY pa.insert_set_id, pa.card_number
                          HAVING COUNT(*)=3)""", set_id)
        n_team = q1("SELECT COUNT(*) FROM players WHERE set_id=? AND subject_role='team'", set_id)
        base_n = q1("""SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                       WHERE i.set_id=? AND i.name='Base Cards'""", set_id)
        hi_n = q1("""SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                     WHERE i.set_id=? AND i.name='Base Cards Highlights'""", set_id)
        as_n = q1("""SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                     WHERE i.set_id=? AND i.name='Base Cards All Stars'""", set_id)

        print(f"subsets={n_sub} (base={n_base} auto={n_auto} inserts={n_ins})")
        print(f"cards(distinct subset:card)={n_cards}  appearances={n_app}  players={n_players}")
        print(f"rookie_appearances={n_rookie}  dual_cards={n_duals}  triple_cards={n_triples}  co_links={link_count}")
        print(f"team_role_players={n_team}  Base={base_n}  Highlights={hi_n}  AllStars={as_n}")

        assert n_sub == 35 and (n_base, n_auto, n_ins) == (3, 10, 22), "subset-flag gate failed"
        assert n_cards == 1115, "card count gate failed"
        assert n_app == 1140, "appearance count gate failed (1115 + 25 co-players)"
        assert n_rookie == 268, "rookie gate failed"
        assert n_duals == 15 and n_triples == 5 and link_count == 60, "dual/triple/link gate failed"
        assert n_team == 1, "team-role gate failed (FP-99 New York Knicks)"
        assert base_n == 260 and hi_n == 10 and as_n == 30, "base split gate failed (260/10/30)"
        print("ALL LOCAL GATES PASSED.")
        print(f"DONE. set id {set_id}")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
