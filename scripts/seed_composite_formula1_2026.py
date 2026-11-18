"""
Seed: 2026 Topps Composite Formula 1 — 862 cards across 32 subsets. Checklist only:
Topps has not published parallels or pack odds, so pack_odds stays NULL and no
parallels are created (matches 903 Finest F1 at launch).

Source:
  scratchpad/cf1.jsonl — 862 card rows: {subset, card_number, subject, team,
                         rookie?, subject_role?, principal?}. One subject per card
                         (no co-players), incl. Triumvirates panels.

Rulings applied (Phase 0 report + go, 2026-11-17):
  - Sport Racing, league F1 (copied from 878). Tier Chrome (878/903 are Chrome;
    the only Composite set, 291 Football, is Standard — Chrome chosen). release_date NULL.
  - Base split into 8 "Base - <brand>" subsets, all is_base=1 (51/878 convention).
    is_base 8 / autograph 5 / relic 5 (Composite Swatch Autographs is auto+relic).
  - No subset renames (878 has no equivalent autograph programs). No parallels, no
    pack_odds, no co-player links.
  - Principals → role athlete (878's stored form); the `principal` hint is dropped.
    Cars (11, subject_role "team") → role team. A&G non-person (9, subject_role
    "event") → role event. No non-person stored as athlete.
  - Team strings mapped to 878 stored forms (standing ruling, so team pages don't
    split): 9 constructors to the ®/™ forms, Hitech → Hitech TGR. F1 Legend and
    Legend → NULL (878 stores legends with no team). McLaren and McLaren Racing as
    printed (no 878/903 form). The other junior teams already match 878 exactly.
  - Rookie: Arvid Lindblad only, flagged on all 24 cards. is_rookie 24.
  - 3 new persons seed as new athletes: Bruce McLaren, Jim Clark, Martin Brundle.

Data model: one player_appearances row per card. Distinct cards 862; appearance
rows 862.

Run post-seed.ts then migrate-to-turso.ts --set 2026-topps-composite-formula-1.
Usage: python3 scripts/seed_composite_formula1_2026.py
"""
import sqlite3, os, json, re, unicodedata

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
JSONL = os.path.join(os.path.dirname(__file__), "..", "scratchpad", "cf1.jsonl")

SET_NAME = "2026 Topps Composite Formula 1"
SET_SLUG = "2026-topps-composite-formula-1"
TOPPS_URL = "https://www.topps.com/pages/topps-composite-formula-1"

# 8 base-brand subsets (all is_base=1)
BASE_SUBSETS = {
    "Base - Paddock Pass", "Base - Paddock Pass Chrome", "Base - Topps Chrome Black",
    "Base - Allen & Ginter", "Base - Topps Cosmic Chrome", "Base - Topps Midnight",
    "Base - World on Wheels", "Base - Resurgence",
}
AUTOGRAPH_SUBSETS = {
    "Paddock Pass Autographs", "Topps Chrome Black Autographs",
    "Allen & Ginter Autographs", "Gilded Autographs", "Composite Swatch Autographs",
}
RELIC_SUBSETS = {
    "Composite Swatch Autographs", "Allen & Ginter Relics", "Push the Limits Relics",
    "Top Crop Relics", "Grand Slam Relics",
}

# file team string -> 878 stored form (®/™ + name fixes); Hitech -> Hitech TGR;
# legend labels -> NULL. Teams not listed are stored as-is.
TEAM_MAP = {
    "Aston Martin Aramco Formula One Team": "Aston Martin Aramco Formula One™ Team",
    "Atlassian Williams F1 Team": "Atlassian Williams F1® Team",
    "Audi Revolut F1 Team": "Audi Revolut F1® Team",
    "BWT Alpine Formula One Team": "BWT Alpine Formula One™ Team",
    "Cadillac Formula 1 Team": "Cadillac Formula 1® Team",
    "McLaren Mastercard Formula 1 Team": "McLaren Mastercard Formula 1® Team",
    "Mercedes-AMG PETRONAS Formula 1 Team": "Mercedes-AMG PETRONAS Formula One™ Team",
    "TGR Haas F1 Team": "TGR Haas F1® Team",
    "VISA Cash App Racing Bulls Formula One Team": "VISA Cash App Racing Bulls Formula One™ Team",
    "Hitech": "Hitech TGR",
    "F1 Legend": None,
    "Legend": None,
}


def map_team(t):
    if t is None:
        return None
    if t in TEAM_MAP:
        return TEAM_MAP[t]
    return t


def slugify(t):
    s = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^\w\s-]", "", s.lower().strip())
    s = re.sub(r"[\s_]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")


def main():
    rows = [json.loads(l) for l in open(JSONL) if l.strip()]
    assert len(rows) == 862, f"expected 862 card rows, got {len(rows)}"

    box_config = json.dumps({
        "hobby": {
            "cards_per_pack": 8, "packs_per_box": 20, "boxes_per_case": 12,
            "notes": "4 numbered parallels, 12 inserts and 36 Chrome cards per box",
        },
        "value_blaster": {
            "cards_per_pack": 8, "packs_per_box": 5, "boxes_per_case": None,
            "notes": "6 inserts and 7 Chrome cards per box",
        },
    })

    # ── ordered subset list: card first-appearance order ──
    subset_order, seen = [], set()
    for r in rows:
        sub = r["subset"]
        if sub not in seen:
            seen.add(sub); subset_order.append(sub)
    assert len(subset_order) == 32, f"expected 32 subsets, got {len(subset_order)}"

    db = sqlite3.connect(DB_PATH)
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA foreign_keys=ON")
    if db.execute("SELECT id FROM sets WHERE name = ?", (SET_NAME,)).fetchone():
        raise SystemExit(f"Set '{SET_NAME}' already exists — aborting.")

    try:
        cur = db.execute(
            """INSERT INTO sets (name, sport, season, league, tier, slug, is_visible,
                   sample_image_url, release_date, box_config, pack_odds, topps_url,
                   related_links, created_at)
               VALUES (?, 'Racing', '2026', 'F1', 'Chrome', ?, 1, ?, NULL, ?, NULL, ?, NULL, ?)""",
            (SET_NAME, SET_SLUG, f"/sets/{SET_SLUG}.jpg", box_config, TOPPS_URL,
             "2026-11-17T12:00:00Z"),
        )
        set_id = cur.lastrowid
        print(f"Created set id {set_id}")

        # ── insert_sets (all 32) ──
        is_ids = {}
        for sub in subset_order:
            is_ids[sub] = db.execute(
                """INSERT INTO insert_sets (set_id, name, is_base, is_autograph, is_relic,
                       is_booklet, print_run, notes)
                   VALUES (?, ?, ?, ?, ?, 0, NULL, NULL)""",
                (set_id, sub,
                 1 if sub in BASE_SUBSETS else 0,
                 1 if sub in AUTOGRAPH_SUBSETS else 0,
                 1 if sub in RELIC_SUBSETS else 0),
            ).lastrowid
        print(f"Created {len(is_ids)} subsets")

        # ── players: role from subject_role ("team"/"event") else athlete ──
        slug_cache = {}

        def goc(name, role):
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

        # ── appearances: one per card; principal hint dropped ──
        for r in rows:
            name = r["subject"].strip()
            role = r.get("subject_role") or "athlete"   # "team" / "event" / athlete
            team = map_team(r.get("team"))
            rookie = 1 if r.get("rookie") else 0
            db.execute(
                """INSERT INTO player_appearances
                       (player_id, insert_set_id, card_number, is_rookie, team, subset_tag, formats)
                   VALUES (?, ?, ?, ?, ?, NULL, NULL)""",
                (goc(name, role), is_ids[r["subset"]], str(r["card_number"]), rookie, team))

        db.commit()

        # ── verification ──
        def q1(sql, *a):
            return db.execute(sql, a).fetchone()[0]

        n_sub = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=?", set_id)
        n_base = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_base=1", set_id)
        n_auto = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_autograph=1", set_id)
        n_relic = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_relic=1", set_id)
        n_bk = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_booklet=1", set_id)
        n_cards = q1("""SELECT COUNT(DISTINCT pa.insert_set_id || ':' || pa.card_number)
                        FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                        WHERE i.set_id=?""", set_id)
        n_app = q1("""SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                      WHERE i.set_id=?""", set_id)
        n_players = q1("SELECT COUNT(*) FROM players WHERE set_id=?", set_id)
        n_rookie = q1("""SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                         WHERE i.set_id=? AND pa.is_rookie=1""", set_id)
        n_team = q1("SELECT COUNT(*) FROM players WHERE set_id=? AND subject_role='team'", set_id)
        n_event = q1("SELECT COUNT(*) FROM players WHERE set_id=? AND subject_role='event'", set_id)
        n_athlete = q1("SELECT COUNT(*) FROM players WHERE set_id=? AND subject_role='athlete'", set_id)
        n_par = q1("""SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id
                      WHERE i.set_id=?""", set_id)
        odds_null = q1("SELECT pack_odds IS NULL FROM sets WHERE id=?", set_id)
        rd_null = q1("SELECT release_date IS NULL FROM sets WHERE id=?", set_id)

        print(f"subsets={n_sub} (base={n_base} auto={n_auto} relic={n_relic} booklet={n_bk})")
        print(f"distinct_cards={n_cards}  appearance_rows={n_app}  players={n_players}  rookie={n_rookie}")
        print(f"roles: athlete={n_athlete} team={n_team} event={n_event}")
        print(f"parallels={n_par}  pack_odds_NULL={odds_null}  release_date_NULL={rd_null}")

        assert (n_sub, n_base, n_auto, n_relic, n_bk) == (32, 8, 5, 5, 0), "subset-flag gate failed"
        assert n_cards == 862 and n_app == 862, "card/appearance gate failed (862 = 862)"
        assert n_players == 93, "player gate failed (expected 93)"
        assert n_rookie == 24, "rookie gate failed (expected 24)"
        assert n_team == 11, "team-role gate failed (expected 11)"
        assert n_event == 9, "event-role gate failed (expected 9)"
        assert n_athlete == 73, "athlete-role gate failed (expected 73)"
        assert n_par == 0, "parallel gate failed (expected 0)"
        assert odds_null == 1 and rd_null == 1, "pack_odds / release_date must be NULL"
        # no non-person stored as athlete (cars/events never athlete)
        bad = db.execute("""SELECT name FROM players WHERE set_id=? AND subject_role='athlete'
                            AND name IN ('MCL40','W17','RB22','SF-26','FW48','VCARB 03','AMR26','VF-26','R26','A526','MAC-26',
                            'Track Marshals','The Checkered Flag','The Grid','Gary The Groundhog','Lionel The Lizard')""", (set_id,)).fetchall()
        assert not bad, f"non-person stored as athlete: {bad}"
        # legend labels mapped to NULL
        leg = db.execute("SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id WHERE i.set_id=? AND pa.team IN ('F1 Legend','Legend')", (set_id,)).fetchone()[0]
        assert leg == 0, "F1 Legend/Legend must map to NULL team"
        # McLaren / McLaren Racing kept as printed
        mc = db.execute("SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id WHERE i.set_id=? AND pa.team IN ('McLaren','McLaren Racing')", (set_id,)).fetchone()[0]
        assert mc == 4, f"McLaren/McLaren Racing as-printed rows = {mc}, expected 4"
        # 878 ®/™ forms present
        for t in ("Mercedes-AMG PETRONAS Formula One™ Team", "McLaren Mastercard Formula 1® Team", "Hitech TGR"):
            c = db.execute("SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id WHERE i.set_id=? AND pa.team=?", (set_id, t)).fetchone()[0]
            assert c > 0, f"mapped team {t!r} not found"
        # The Grail 2/5/8
        grail = sorted(int(x[0]) for x in db.execute("SELECT pa.card_number FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id WHERE i.set_id=? AND i.name='The Grail'", (set_id,)).fetchall())
        assert grail == [2, 5, 8], f"The Grail numbers {grail}, expected [2,5,8]"
        print("ALL LOCAL GATES PASSED.")
        print(f"DONE. set id {set_id}")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
