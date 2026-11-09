"""
Seed: 2026 Topps Stadium Club Football — full checklist (1,329 cards, 37 subsets).

Source: scratchpad/scf.jsonl (one card per line: subset, card_number, subject, team,
optional rookie, optional co_players[{subject, team}]).

Rulings applied (Phase 0 report + go, 2026-11-08):
  (a) Base stored as TWO subsets as printed — "Base Cards" (1-200) and "Rookie"
      (201-300) — not one 1-300 Base. Design Variation is is_base=1 (variation of
      base, standing ruling). => 3 base subsets.
  (b) Polaroids is an AUTOGRAPH (is_autograph=1): initials-code numbering (P-AR,
      P-CBE...), 904's "...Polaroid Signatures" precedent, all-41-rookie-flagged.
      => 16 autograph subsets, 18 inserts. Gate: 3 base / 16 auto / 18 insert = 37.
  (c) Triumvirates are 30 individual single-player cards (T-1..T-30), not triples
      (follows 904). Cosigners + Rookie Cosigners are duals: one appearance per
      player on the card; bidirectional co-player links built by grouping
      (insert_set, card_number), matching seed.ts.
  (d) Near-miss subjects seeded under their SHEET spelling so the review queue
      (data/athlete-review-queue.csv) merges them to the stored canonical and the
      sheet form becomes an alias:
        - "A.J. Terrell Jr." -> A.J. Terrell      (existing queue_id 170, premerge)
        - "Tre' Harris III"  -> Tre Harris III    (existing queue_id 182, premerge)
        - "Steve Smith"      -> Steve Smith Sr.   (new queue_id 362, merge)
      The co-player "Steve Smith" on Cosigners CS-SS-MM (w/ Muhsin Muhammad, both
      Panthers) is the WR legend Steve Smith Sr.
  (e) Legends carry their era's team as printed (Los Angeles Raiders, San Diego
      Chargers, St. Louis Rams, Washington Redskins). Two-team subjects (Tom Brady
      Patriots/Buccaneers, Aaron Rodgers Packers/Steelers) store per-appearance team,
      one player row each.

Set facts: tier Standard (every Stadium Club in the DB); league NFL; season 2026;
release_date 2026-12-09 (pre-order 2026-11-09, no pre-order column). box_config a
single `hobby` key with null numbers + "Configuration TBA" (formats unknown; odds
attach later). pack_odds NULL. No parallels. topps_url NULL (Topps page returns 403
bot-block; unconfirmed). Because release is a month out, the Last Sold release guard
gates this set automatically.

Run post-seed.ts (build-athletes -> backfill-headshots --set -> build-athletes)
after this, then migrate-to-turso.ts --set 2026-topps-stadium-club-football.
Usage: python3 scripts/seed_stadium_club_football_2026.py
"""
import sqlite3, os, json, re, unicodedata

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
JSONL = os.path.join(os.path.dirname(__file__), "..", "scratchpad", "scf.jsonl")

SET_NAME = "2026 Topps Stadium Club Football"
SET_SLUG = "2026-topps-stadium-club-football"

# (d) No in-seed NAME_FIX: near-misses keep their sheet spelling and merge via the
# review queue so the sheet form is preserved as an alias. canon() still NFC-folds.
NAME_FIX = {}

# (a) 3 is_base subsets
BASE_SUBSETS = {
    "Base Cards",
    "Rookie",
    "Design Variation",
}
# (b) 16 autograph subsets (Polaroids included)
AUTO_SUBSETS = {
    "Base Cards Autographs",
    "Rookie Autographs",
    "Abstract Autographs",
    "Cosigners",
    "Ink Exposure",
    "Legends of the Lens Autographs",
    "Lonestar Autographs",
    "Rookie Cosigners",
    "Angry Runs Autographs",
    "Concentration Autographs",
    "Design Variation Autographs",
    "First Down Autographs",
    "Framed Greatness Autographs",
    "Stadium Credentials Autographs",
    "Stadium Intros Autographs",
    "Polaroids",
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
    assert len(rows) == 1329, f"expected 1329 rows, got {len(rows)}"

    box_config = json.dumps({
        "hobby": {
            "cards_per_pack": None,
            "packs_per_box": None,
            "boxes_per_case": None,
            "notes": "Configuration TBA",
        },
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
               VALUES (?, 'Football', '2026', 'NFL', 'Standard', ?, 1, ?, ?, ?, NULL, NULL, ?)""",
            (SET_NAME, SET_SLUG, f"/sets/{SET_SLUG}.jpg", "2026-12-09", box_config,
             "2026-11-08T12:00:00Z"),
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
            isid = is_ids[r["subset"]]

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
        base_n = q1("""SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                       WHERE i.set_id=? AND i.name='Base Cards'""", set_id)
        rook_n = q1("""SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                       WHERE i.set_id=? AND i.name='Rookie'""", set_id)

        print(f"subsets={n_sub} (base={n_base} auto={n_auto} inserts={n_ins})")
        print(f"cards(distinct subset:card)={n_cards}  appearances={n_app}  players={n_players}")
        print(f"rookie_appearances={n_rookie}  dual_cards={n_duals}  co_links={link_count}")
        print(f"Base Cards={base_n}  Rookie={rook_n}")

        assert n_sub == 37 and (n_base, n_auto, n_ins) == (3, 16, 18), "subset-flag gate failed"
        assert n_cards == 1329, "card count gate failed"
        assert n_app == 1352, "appearance count gate failed (1329 + 23 co-players)"
        assert n_rookie == 431, "rookie gate failed"
        assert n_duals == 23 and link_count == 46, "dual/link gate failed"
        assert base_n == 200 and rook_n == 100, "base/rookie split gate failed"
        print("ALL LOCAL GATES PASSED.")
        print(f"DONE. set id {set_id}")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
