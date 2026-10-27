"""
Seed: 2026 Topps Finest Formula 1 — full checklist (736 cards, 25 subsets).

Source: scratchpad/finest.jsonl (one card per line). Structure:
  - Base: four is_base=1 tiers (Common/Uncommon/Rare 100 each, Super Rare 25),
    numbered continuously 1-325.
  - 10 inserts, 5 autograph subsets, 5 relic subsets (Finest Autograph Relics is
    both autograph AND relic). No parallels, no pack odds (release date TBA).

Rulings applied (see Phase 0):
  - Team names match set 878's stored form, not the Finest sheet: Mercedes-AMG
    PETRONAS Formula 1(R) Team -> ...Formula One(TM) Team, and Hitech -> Hitech TGR
    (TEAM_FIX). Keeps team chips / /teams/ pages from splitting one team in two.
  - Legend / Cars rows carry their label in player_appearances.subset_tag; legends
    have team=NULL. Cars reuse the driver's player row (same athlete).
  - Emerson Fittipaldi: the five AIX Racing rows (the F2 grandson) are stored as
    "Emerson Fittipaldi Jr."; the Legend rows stay "Emerson Fittipaldi". Two
    players -> the two existing athletes (878 precedent).
  - "Worlds Finest" renders as "World's Finest".
  - subject_role is athlete for every subject (drivers, cars, principals, F2,
    legends), matching 878.

Run build-athletes.ts after this, then migrate-to-turso.ts (full reload).
Usage: python3 scripts/seed_finest_f1_2026.py
"""
import sqlite3, os, json, re, unicodedata

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
JSONL = os.path.join(os.path.dirname(__file__), "..", "scratchpad", "finest.jsonl")

SET_NAME = "2026 Topps Finest Formula 1"
SET_SLUG = "2026-topps-finest-formula"

# Team-string normalization to 878's stored form (SmackDown-casing ruling).
TEAM_FIX = {
    "Mercedes-AMG PETRONAS Formula 1® Team": "Mercedes-AMG PETRONAS Formula One™ Team",
    "Hitech": "Hitech TGR",
}
SUBSET_RENAME = {"Worlds Finest": "World's Finest"}

BASE_SUBSETS = {"Base Common", "Base Uncommon", "Base Rare", "Base Super Rare"}
AUTO_SUBSETS = {
    "Finest Autographs", "Finest Duos Signatures", "Starting Grid Signatures",
    "Signature Fashion", "Finest Drivers Autographs", "Finest Autograph Relics",
}
RELIC_SUBSETS = {
    "Finest Autograph Relics", "F1 Relics", "Track Attack Relics",
    "Raceday Relics", "Finest Relics",
}


def slugify(t):
    s = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode("ascii")
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")


def fix_team(t):
    if t is None:
        return None
    return TEAM_FIX.get(t, t)


def stored_name(subject, label):
    # The F2 grandson (AIX Racing rows, no Legend label) is "Emerson Fittipaldi Jr."
    if subject == "Emerson Fittipaldi" and label != "Legend":
        return "Emerson Fittipaldi Jr."
    return subject


def main():
    rows = [json.loads(l) for l in open(JSONL)]
    assert len(rows) == 736, f"expected 736 rows, got {len(rows)}"

    db = sqlite3.connect(DB_PATH)
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA foreign_keys=ON")

    if db.execute("SELECT id FROM sets WHERE name = ?", (SET_NAME,)).fetchone():
        raise SystemExit(f"Set '{SET_NAME}' already exists — aborting.")

    box_config = json.dumps({
        "hobby": {
            "cards_per_pack": 10, "packs_per_box": 6, "boxes_per_case": 8,
            "autos_or_relics_per_box": 1,
            "notes": "Per box: 1 relic or autograph",
        }
    })

    try:
        cur = db.execute(
            """INSERT INTO sets (name, sport, season, league, tier, slug, is_visible,
                   sample_image_url, release_date, box_config, pack_odds, created_at)
               VALUES (?, 'Racing', '2026', 'F1', 'Chrome', ?, 1, ?, NULL, ?, NULL, ?)""",
            (SET_NAME, SET_SLUG, f"/sets/{SET_SLUG}.jpg", box_config, "2026-10-27T12:00:00Z"),
        )
        set_id = cur.lastrowid
        print(f"Created set id {set_id}")

        # ── players (get-or-create per (set, name)) ──
        slug_cache = {}

        def goc(name, role="athlete"):
            name = name.strip()
            r = db.execute("SELECT id FROM players WHERE set_id=? AND name=?", (set_id, name)).fetchone()
            if r:
                return r[0]
            base = slugify(name)
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
            name = SUBSET_RENAME.get(sub, sub)
            is_ids[sub] = db.execute(
                """INSERT INTO insert_sets (set_id, name, is_base, is_autograph, is_relic)
                   VALUES (?, ?, ?, ?, ?)""",
                (set_id, name,
                 1 if sub in BASE_SUBSETS else 0,
                 1 if sub in AUTO_SUBSETS else 0,
                 1 if sub in RELIC_SUBSETS else 0),
            ).lastrowid
        print(f"Created {len(is_ids)} subsets")

        # ── appearances + co-players ──
        for r in rows:
            label = r.get("label")
            name = stored_name(r["subject"], label)
            pid = goc(name)
            team = fix_team(r.get("team"))
            app = db.execute(
                """INSERT INTO player_appearances
                       (player_id, insert_set_id, card_number, is_rookie, team, subset_tag)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (pid, is_ids[r["subset"]], str(r["card_number"]),
                 1 if r.get("rookie") else 0, team, label),
            ).lastrowid
            for cp in (r.get("co_players") or []):
                cpid = goc(stored_name(cp["subject"], cp.get("label")))
                db.execute(
                    "INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)",
                    (app, cpid),
                )

        db.commit()
        n_players = db.execute("SELECT COUNT(*) FROM players WHERE set_id=?", (set_id,)).fetchone()[0]
        n_app = db.execute(
            "SELECT COUNT(*) FROM player_appearances pa JOIN players p ON p.id=pa.player_id WHERE p.set_id=?",
            (set_id,)).fetchone()[0]
        print(f"players={n_players}  appearances={n_app}")
        print(f"DONE. set id {set_id}")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
