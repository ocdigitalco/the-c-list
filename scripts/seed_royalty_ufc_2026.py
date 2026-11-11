"""
Seed: 2026 Topps Royalty UFC — full checklist (785 cards, 32 subsets) + odds + parallels.

Sources:
  scratchpad/ufc.jsonl      — one card per line: subset, card_number, subject,
                              team(null), optional rookie, optional co_players[{subject}].
  scratchpad/ufcodds.jsonl  — 136 rows: 32 subset lines (parallel=null) carrying the
                              subset base print_run + hobby odds, and 104 parallel
                              lines (parallel, print_run, hobby odds).

Rulings applied (Phase 0 report + go, 2026-11-10):
  (a) 32 subsets. Flags (corrected from the spec's prose miscounts):
        1 base / 24 autograph / 16 relic / 3 booklet / 1 insert, auto-relic = 10.
      AUTO_RELIC (10) = relic/patch cards that are also signed; three of them are
      booklets (is_booklet=1). PURE_AUTO (14) = signed, no relic. PURE_RELIC (6) =
      relic, no signature. Liquid Silver is the lone plain insert.
  (b) Co-player cards: one appearance per fighter on the card; bidirectional links
      built by grouping (insert_set, card_number), matching seed.ts. 46 duals + 4
      triples => links = 46*2 + 4*6 = 116. (The spec's 118 double-counted DA-WC,
      the Hunter Campbell + Dana White card already inside the 15 Dual Autographs.)
  (c) Three non-fighters carry subject_role='celebrity' (never 'athlete'):
        - Dana White            (main on USA 250 Dual Patch Autographs Booklet;
                                 co on the Dual Autographs DA-WC card)
        - Hunter Campbell       (main on Dual Autographs DA-WC)
        - Donald J. Trump       (co on USA 250 Dual Patch Autographs Booklet)
      Hunter Campbell already carries 5 'athlete' appearances across sets 14/40, so
      his 1 celebrity appearance here loses the most-appearances role vote; a role-
      override queue entry (data/athlete-review-queue.csv) forces role=celebrity.
      Dana White is already celebrity/person; Trump is new.
  (d) Near-miss subjects seeded under their SHEET spelling so the review queue merges
      them to the stored canonical and the sheet form becomes an alias (all existing):
        - Dricus du Plessis  (queue 14)   - Jéssica Andrade  (queue 15)
        - Reinier de Ridder  (queue 21)   - Mateusz Rębecki  (queue 60)
        - JeongYeong Lee     (queue 211)  - Ateba Gautier    (queue 290)
      Genuinely new athletes: Donald J. Trump (celebrity), Melquizael Costa,
      Vitor Belfort.

Set facts: tier Premium (2024/2025 Royalty UFC precedent, sets 47/14); league UFC;
sport MMA; season 2026; release_date 2026-12-13. box_config mirrors set 14's hobby
(10 cards/pack, 1 pack/box, 4 boxes/case, 5 autos + 3 relics, remaining 2 base) with
a notes line. pack_odds.hobby = 135 keys (31 subset + 104 parallel; USA 250 Dual
Patch Autographs Booklet is 1/1 with no odds). 104 numbered parallel rows; 29 subset
base print_runs (Letterman/Welcome to the Club/Liquid Silver unnumbered). topps_url
NULL. Release a month out -> Last Sold guard gates it.

Run post-seed.ts (build-athletes -> backfill-headshots --set -> build-athletes)
after this, then migrate-to-turso.ts --set 2026-topps-royalty-ufc.
Usage: python3 scripts/seed_royalty_ufc_2026.py
"""
import sqlite3, os, json, re, unicodedata

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
JSONL = os.path.join(os.path.dirname(__file__), "..", "scratchpad", "ufc.jsonl")
ODDS = os.path.join(os.path.dirname(__file__), "..", "scratchpad", "ufcodds.jsonl")

SET_NAME = "2026 Topps Royalty UFC"
SET_SLUG = "2026-topps-royalty-ufc"

NAME_FIX = {}  # near-misses keep their sheet spelling; the review queue folds them.

# (c) non-fighters: subject_role='celebrity'
CELEBRITIES = {"Dana White", "Hunter Campbell", "Donald J. Trump"}

# (a) subset-flag classification — 1 base / 24 auto / 16 relic / 3 booklet / 1 insert
BASE_SUBSETS = {"Base"}
AUTO_RELIC = {                                   # is_autograph=1 AND is_relic=1 (10)
    "Rookie Relic Autographs", "Regalia Relic Signatures", "Superior Relic Signatures",
    "Royal Arms Relic Autographs", "Triumph Relic Signatures",
    "Autographed Jumbo Relic Booklets", "Letterman Booklet Autographs",
    "Dual Fighter Relic Autographs", "USA 250 Patch Autographs",
    "USA 250 Dual Patch Autographs Booklet",
}
PURE_AUTO = {                                    # is_autograph=1 only (14)
    "Rookie Autographs", "Regal Ink", "Royalty Autographs", "Superior Signatures",
    "Pursuit of Greatness Autographs", "Royal Precedence Autographs",
    "Golden Hall Autographs", "Royal Heir Autographs", "Dual Autographs",
    "Triple Autographs", "Welcome to the Club Dual Autographs",
    "Crowned Champions Autographs", "Royal Decree Autographs",
    "The Time is Now Autographs",
}
PURE_RELIC = {                                   # is_relic=1 only (6)
    "Rookie Jumbo Relics", "Grand Royal Relics", "Regalia Relics", "Star Relics",
    "Octagon Treasures Relics", "Prodigious Pairings Relics",
}
BOOKLETS = {                                     # is_booklet=1 (3, all within AUTO_RELIC)
    "Autographed Jumbo Relic Booklets", "Letterman Booklet Autographs",
    "USA 250 Dual Patch Autographs Booklet",
}
# plain insert (no flags): "Liquid Silver"

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


def to_denom(s):
    # "1:X" -> int(X)
    return int(s.split(":", 1)[1])


def main():
    rows = [json.loads(l) for l in open(JSONL) if l.strip()]
    assert len(rows) == 785, f"expected 785 rows, got {len(rows)}"
    odds = [json.loads(l) for l in open(ODDS) if l.strip()]
    assert len(odds) == 136, f"expected 136 odds rows, got {len(odds)}"

    # ── derive subset print_runs + pack_odds + parallel rows from the odds file ──
    subset_pr = {}          # subset name -> base print_run (or None)
    hobby_odds = {}         # pack_odds key -> int denominator
    parallel_rows = []      # (subset, parallel, print_run)
    for o in odds:
        sub = o["subset"]
        par = o.get("parallel")
        pr = o.get("print_run")
        hob = (o.get("odds") or {}).get("hobby")
        if not par:
            subset_pr[sub] = pr
            key = sub                       # "Base", "Star Relics", ...
        else:
            parallel_rows.append((sub, par, pr))
            key = f"{sub} {par}"            # "Base Red", "Star Relics Gold", ...
        if hob:
            hobby_odds[key] = to_denom(hob)
    assert len(parallel_rows) == 104, f"expected 104 parallels, got {len(parallel_rows)}"
    assert len(hobby_odds) == 135, f"expected 135 hobby odds keys, got {len(hobby_odds)}"

    box_config = json.dumps({
        "hobby": {
            "cards_per_pack": 10, "packs_per_box": 1, "boxes_per_case": 4,
            "autos_per_box": 5, "memorabilia_cards_per_box": 3,
            "notes": "5 autographs, 3 relics, and 2 base cards per pack",
        },
    })
    pack_odds = json.dumps({"hobby": hobby_odds})

    db = sqlite3.connect(DB_PATH)
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA foreign_keys=ON")

    if db.execute("SELECT id FROM sets WHERE name = ?", (SET_NAME,)).fetchone():
        raise SystemExit(f"Set '{SET_NAME}' already exists — aborting.")

    try:
        cur = db.execute(
            """INSERT INTO sets (name, sport, season, league, tier, slug, is_visible,
                   sample_image_url, release_date, box_config, pack_odds, topps_url, created_at)
               VALUES (?, 'MMA', '2026', 'UFC', 'Premium', ?, 1, ?, ?, ?, ?, NULL, ?)""",
            (SET_NAME, SET_SLUG, f"/sets/{SET_SLUG}.jpg", "2026-12-13", box_config,
             pack_odds, "2026-11-10T12:00:00Z"),
        )
        set_id = cur.lastrowid
        print(f"Created set id {set_id}")

        # ── players (get-or-create per (set, canonical name)); role from CELEBRITIES ──
        slug_cache = {}

        def goc(name):
            name = canon(name)
            r = db.execute("SELECT id FROM players WHERE set_id=? AND name=?", (set_id, name)).fetchone()
            if r:
                return r[0]
            role = "celebrity" if name in CELEBRITIES else "athlete"
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

        # ── insert_sets in JSONL first-appearance order (with flags + base print_run) ──
        is_ids = {}
        for r in rows:
            sub = r["subset"]
            if sub in is_ids:
                continue
            is_ids[sub] = db.execute(
                """INSERT INTO insert_sets (set_id, name, is_base, is_autograph, is_relic,
                       is_booklet, print_run, notes)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (set_id, sub,
                 1 if sub in BASE_SUBSETS else 0,
                 1 if (sub in AUTO_RELIC or sub in PURE_AUTO) else 0,
                 1 if (sub in AUTO_RELIC or sub in PURE_RELIC) else 0,
                 1 if sub in BOOKLETS else 0,
                 subset_pr.get(sub),
                 SUBSET_NOTES.get(sub)),
            ).lastrowid
        print(f"Created {len(is_ids)} subsets")

        # every odds subset / parallel must map to a real insert_set
        for sub in subset_pr:
            assert sub in is_ids, f"odds subset not in checklist: {sub!r}"
        for sub, _, _ in parallel_rows:
            assert sub in is_ids, f"parallel subset not in checklist: {sub!r}"

        # ── parallels ──
        for sub, par, pr in parallel_rows:
            db.execute(
                "INSERT INTO parallels (insert_set_id, name, print_run) VALUES (?, ?, ?)",
                (is_ids[sub], par, pr))

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
        n_relic = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_relic=1", set_id)
        n_bk = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_booklet=1", set_id)
        n_autorelic = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_autograph=1 AND is_relic=1", set_id)
        n_ins = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_base=0 AND is_autograph=0 AND is_relic=0", set_id)
        n_pr = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND print_run IS NOT NULL", set_id)
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
        n_celeb = q1("SELECT COUNT(*) FROM players WHERE set_id=? AND subject_role='celebrity'", set_id)
        n_par = q1("""SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id
                      WHERE i.set_id=?""", set_id)
        n_par_pr = q1("""SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id
                         WHERE i.set_id=? AND p.print_run IS NOT NULL""", set_id)
        base_n = q1("""SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                       WHERE i.set_id=? AND i.name='Base'""", set_id)
        n_oddskeys = len(json.loads(q1("SELECT pack_odds FROM sets WHERE id=?", set_id))["hobby"])

        print(f"subsets={n_sub} (base={n_base} auto={n_auto} relic={n_relic} booklet={n_bk} auto_relic={n_autorelic} insert={n_ins})")
        print(f"subset_print_runs={n_pr}  cards={n_cards}  appearances={n_app}  players={n_players}")
        print(f"rookie_appearances={n_rookie}  dual_cards={n_duals}  triple_cards={n_triples}  co_links={link_count}")
        print(f"celebrity_players={n_celeb}  parallels={n_par} (numbered={n_par_pr})  pack_odds_hobby_keys={n_oddskeys}  Base={base_n}")

        assert n_sub == 32 and (n_base, n_auto, n_relic, n_bk, n_ins) == (1, 24, 16, 3, 1), "subset-flag gate failed"
        assert n_autorelic == 10, "auto-relic gate failed (expected 10)"
        assert n_pr == 29, "subset print_run gate failed (expected 29)"
        assert n_cards == 785, "card count gate failed"
        assert n_app == 839, "appearance count gate failed (785 + 54 co-players)"
        assert n_rookie == 184, "rookie gate failed"
        assert n_duals == 46 and n_triples == 4 and link_count == 116, "dual/triple/link gate failed"
        assert n_celeb == 3, "celebrity-role gate failed (Dana White / Hunter Campbell / Donald J. Trump)"
        assert n_par == 104 and n_par_pr == 104, "parallel gate failed (104, all numbered)"
        assert n_oddskeys == 135, "pack_odds gate failed (135 hobby keys)"
        assert base_n == 100, "base card gate failed (100)"
        print("ALL LOCAL GATES PASSED.")
        print(f"DONE. set id {set_id}")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
