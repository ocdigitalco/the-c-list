"""
Seed 2026 Topps MLB x KAWS (Baseball / MLB). 146 cards across 6 subsets.

Modeling (per task):
  * Teams are NULL on every card (not in source).
  * Base / KAWS Creation / Autographs / On-Card Autographs subjects = athletes.
  * "KAWS Companion" SP subject = the Companion character (role character).
  * "KAWS" SSP-auto subject = the artist (role celebrity).
  * Autograph subsets (is_autograph=1): KAWS Companion SSP Autos, Autographs,
    On-Card Autographs. The N-A code scheme spans both auto subsets without
    collision (On-Card holds 1,2,7,14,15) — kept as separate subsets, not merged.

No pack odds / box config / parallels (deferred). Local SQLite only.
Usage: python3 scripts/seed_mlb_x_kaws_2026.py
"""
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")

SET = dict(
    name="2026 Topps MLB x KAWS",
    sport="Baseball",
    season="2026",
    league="MLB",
    tier="Standard",
    sample_image_url="/sets/2026-topps-mlb-x-kaws.jpg",
    release_date="2026-07-20",
    slug="2026-topps-mlb-x-kaws",
    is_visible=1,
    created_at="2026-07-18T12:00:00Z",
    topps_url="https://www.topps.com/pages/topps-mlb-x-kaws",
)

BASE = [
    "Shohei Ohtani", "Aaron Judge", "Carlton Fisk", "Frank Thomas", "Bobby Witt Jr.",
    "Mike Trout", "Derek Jeter", "Juan Marichal", "Gunnar Henderson", "Albert Pujols",
    "Cam Schlittler", "Ichiro", "Jac Caglianone", "Yoshinobu Yamamoto", "Roki Sasaki",
    "Payton Tolle", "Mookie Betts", "Alex Rodriguez", "Cal Ripken Jr.", "José Ramírez",
    "Jackson Chourio", "Elly De La Cruz", "Roman Anthony", "Ken Griffey Jr.", "Francisco Lindor",
    "Pedro Martínez", "Roger Clemens", "Trea Turner", "Kyle Tucker", "Bryce Harper",
    "Fernando Tatis Jr.", "Vladimir Guerrero Jr.", "Carson Williams", "Konnor Griffin", "Reggie Jackson",
    "Bubba Chandler", "Logan Webb", "David Ortiz", "Samuel Basallo", "Jacob Misiorowski",
    "Colson Montgomery", "Corbin Carroll", "Chipper Jones", "Paul Skenes", "Julio Rodríguez",
    "Jonah Tong", "Darryl Strawberry", "Juan Soto", "Tarik Skubal", "Ronald Acuña Jr.",
    "Wyatt Langford", "Cal Raleigh", "Nick Kurtz", "Randy Johnson", "Junior Caminero",
    "Mike Piazza", "James Wood", "Jacob Wilson", "Max Fried", "Clayton Kershaw",
]  # card_number = index+1 (1..60)

KAWS_CREATION = [
    ("KC-1", "Shohei Ohtani"), ("KC-2", "Aaron Judge"), ("KC-3", "Yoshinobu Yamamoto"),
    ("KC-4", "Paul Skenes"), ("KC-5", "Elly De La Cruz"), ("KC-6", "Juan Soto"),
    ("KC-7", "Roman Anthony"), ("KC-8", "Derek Jeter"), ("KC-9", "Ronald Acuña Jr."),
    ("KC-10", "Jacob Misiorowski"), ("KC-11", "Roki Sasaki"), ("KC-12", "Max Fried"),
    ("KC-13", "Mookie Betts"), ("KC-14", "Bobby Witt Jr."), ("KC-15", "Tarik Skubal"),
    ("KC-16", "Cal Raleigh"), ("KC-17", "Julio Rodríguez"), ("KC-18", "Vladimir Guerrero Jr."),
    ("KC-19", "Fernando Tatis Jr."), ("KC-20", "Kyle Tucker"), ("KC-21", "Francisco Lindor"),
    ("KC-22", "Junior Caminero"), ("KC-23", "Nick Kurtz"), ("KC-24", "Wyatt Langford"),
    ("KC-25", "Bryce Harper"),
]

SP_CODES = [f"SP-K{i}" for i in range(1, 11)]          # 10 — subject "KAWS Companion"
SSP_CODES = [f"SSP-K{i}" for i in range(11, 16)]       # 5  — subject "KAWS"

AUTOS = [
    ("3-A", "Carlton Fisk"), ("4-A", "Frank Thomas"), ("5-A", "Bobby Witt Jr."),
    ("6-A", "Mike Trout"), ("8-A", "Juan Marichal"), ("9-A", "Gunnar Henderson"),
    ("10-A", "Albert Pujols"), ("12-A", "Ichiro"), ("13-A", "Jac Caglianone"),
    ("16-A", "Payton Tolle"), ("19-A", "Cal Ripken Jr."), ("20-A", "José Ramírez"),
    ("22-A", "Elly De La Cruz"), ("24-A", "Ken Griffey Jr."), ("25-A", "Francisco Lindor"),
    ("26-A", "Pedro Martínez"), ("27-A", "Roger Clemens"), ("28-A", "Trea Turner"),
    ("29-A", "Kyle Tucker"), ("32-A", "Vladimir Guerrero Jr."), ("33-A", "Carson Williams"),
    ("35-A", "Reggie Jackson"), ("38-A", "David Ortiz"), ("40-A", "Jacob Misiorowski"),
    ("42-A", "Corbin Carroll"), ("43-A", "Chipper Jones"), ("44-A", "Paul Skenes"),
    ("45-A", "Julio Rodríguez"), ("46-A", "Jonah Tong"), ("47-A", "Darryl Strawberry"),
    ("48-A", "Juan Soto"), ("49-A", "Tarik Skubal"), ("51-A", "Wyatt Langford"),
    ("53-A", "Nick Kurtz"), ("54-A", "Randy Johnson"), ("55-A", "Junior Caminero"),
    ("56-A", "Mike Piazza"), ("57-A", "James Wood"), ("58-A", "Jacob Wilson"),
    ("59-A", "Max Fried"), ("60-A", "Clayton Kershaw"),
]

ON_CARD = [
    ("1-A", "Shohei Ohtani"), ("2-A", "Aaron Judge"), ("7-A", "Derek Jeter"),
    ("14-A", "Yoshinobu Yamamoto"), ("15-A", "Roki Sasaki"),
]

# (subset_name, is_autograph, [(card_number, player, subject_role), ...])
SUBSETS = [
    ("Base Set", 0, [(str(i + 1), n, "athlete") for i, n in enumerate(BASE)]),
    ("KAWS Creation", 0, [(c, n, "athlete") for c, n in KAWS_CREATION]),
    ("KAWS Companion SPs", 0, [(c, "KAWS Companion", "character") for c in SP_CODES]),
    ("KAWS Companion SSP Autos", 1, [(c, "KAWS", "celebrity") for c in SSP_CODES]),
    ("Autographs", 1, [(c, n, "athlete") for c, n in AUTOS]),
    ("On-Card Autographs", 1, [(c, n, "athlete") for c, n in ON_CARD]),
]


def main():
    total = sum(len(cards) for _, _, cards in SUBSETS)
    if total != 146:
        print(f"STOP: parsed {total} cards, expected 146.")
        raise SystemExit(1)

    db = sqlite3.connect(os.path.abspath(DB_PATH))

    if db.execute("SELECT id FROM sets WHERE slug=? OR name=?", (SET["slug"], SET["name"])).fetchone():
        print("STOP: set already exists. Not overwriting.")
        raise SystemExit(1)

    cur = db.execute(
        """INSERT INTO sets (name, sport, season, league, tier, sample_image_url,
                             release_date, slug, is_visible, created_at, topps_url)
           VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        (SET["name"], SET["sport"], SET["season"], SET["league"], SET["tier"],
         SET["sample_image_url"], SET["release_date"], SET["slug"], SET["is_visible"],
         SET["created_at"], SET["topps_url"]),
    )
    set_id = cur.lastrowid
    print(f"Created set id {set_id}: {SET['name']}")

    # players (set-scoped, unique by name); role is consistent per subject name
    role_by_name = {}
    for _, _, cards in SUBSETS:
        for _, name, role in cards:
            role_by_name.setdefault(name, role)
    player_id = {}
    for name, role in role_by_name.items():
        c = db.execute("INSERT INTO players (set_id, name, subject_role) VALUES (?,?,?)", (set_id, name, role))
        player_id[name] = c.lastrowid
    print(f"Created {len(player_id)} players")

    for subset_name, is_auto, cards in SUBSETS:
        c = db.execute("INSERT INTO insert_sets (set_id, name, is_autograph) VALUES (?,?,?)", (set_id, subset_name, is_auto))
        is_id = c.lastrowid
        for card_number, name, _role in cards:
            db.execute(
                """INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, subset_tag, team)
                   VALUES (?,?,?,?,?,?)""",
                (player_id[name], is_id, card_number, 0, None, None),
            )
    db.commit()

    # report
    print("\nPer-subset card counts (DB):")
    rows = db.execute(
        """SELECT i.name, i.is_autograph, COUNT(pa.id)
           FROM insert_sets i LEFT JOIN player_appearances pa ON pa.insert_set_id=i.id
           WHERE i.set_id=? GROUP BY i.id ORDER BY i.id""", (set_id,)).fetchall()
    grand = 0
    for name, auto, n in rows:
        grand += n
        print(f"  {name:28s} {n:4d}  {'[AUTO]' if auto else ''}")
    print(f"  TOTAL {grand}")
    print("autograph subsets:", sum(1 for _, a, _ in rows if a))
    print("players:", db.execute("SELECT COUNT(*) FROM players WHERE set_id=?", (set_id,)).fetchone()[0])
    print("teams non-null:", db.execute(
        "SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id "
        "WHERE i.set_id=? AND pa.team IS NOT NULL", (set_id,)).fetchone()[0])
    db.close()


if __name__ == "__main__":
    main()
