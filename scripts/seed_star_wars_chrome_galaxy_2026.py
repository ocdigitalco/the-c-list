"""
Seed 2026 Topps Star Wars Chrome Galaxy (Entertainment / Star Wars / Chrome).

Reads scripts/star_wars_chrome_galaxy_2026_cards.jsonl (540 cards). No pack odds,
box config, or parallels in this pass (deferred).

Modeling (confirmed with the user — actor-as-subject):
  * Art cards (Base + non-auto inserts): subject = artwork/scene title,
    subject_role='character', subset_tag = the "Art by {artist}" tag (verbatim,
    typos preserved). team null.
  * Actor autographs (Galaxy/Dual/Triple/Quad): subject = ACTOR,
    subject_role='celebrity'; the character (role played) is stored in subset_tag
    as "as {character}". FLAG: co_characters (per co-signer) are NOT stored — the
    appearance_co_players table has no character column; co-signers are linked by
    name only.
  * Multi-signer autos: ONE appearance (main signer) + appearance_co_players rows
    for each co-signer (43 links total).
  * Sketch Card Artists: subject = artist, subject_role='celebrity', not autos,
    subset_tag null.
  * card_number holds the printed card_number (Base 1-100) or the code
    (CLOUD-1, GA-33, D-BOUNTY, ...); null for sketch artists.

Local SQLite only. Migrate to Turso separately.
Usage: python3 scripts/seed_star_wars_chrome_galaxy_2026.py
"""
import json
import os
import sqlite3
import collections

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
DATA_PATH = os.path.join(os.path.dirname(__file__), "star_wars_chrome_galaxy_2026_cards.jsonl")

SET = dict(
    name="2026 Topps Star Wars Chrome Galaxy",
    sport="Entertainment",
    season="2026",
    league="Star Wars",
    tier="Chrome",
    sample_image_url="/sets/2026-topps-star-wars-chrome-galaxy.jpg",
    release_date="2026-07-14",
    slug="2026-topps-star-wars-chrome-galaxy",
    is_visible=1,
    created_at="2026-07-10T12:00:00Z",
)

# Subset order (first appearance) → insert_sets rows.
SUBSET_ORDER = [
    "Base Cards", "Duel on Cloud City", "Art of Rogue One", "Art of the Dark Side",
    "Galactic Anthology", "Art of Knights of the Republic", "Topps Chrome Layers Original Art",
    "Comicfractor", "Original Art Puzzle Cards", "Force Energy", "Galaxy Autographs",
    "Dual Autographs", "Triple Autographs", "Quad Autographs", "Sketch Card Artists",
]


def load_rows():
    rows = []
    with open(DATA_PATH) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def main():
    rows = load_rows()
    if len(rows) != 540:
        print(f"STOP: parsed {len(rows)} rows, expected 540.")
        raise SystemExit(1)

    db = sqlite3.connect(os.path.abspath(DB_PATH))

    # Safety: never overwrite an existing set.
    existing = db.execute(
        "SELECT id FROM sets WHERE slug=? OR (name=? AND season=?)",
        (SET["slug"], SET["name"], SET["season"]),
    ).fetchone()
    if existing:
        print(f"STOP: set already exists (id {existing[0]}). Not overwriting.")
        raise SystemExit(1)

    # ── set row ──
    cur = db.execute(
        """INSERT INTO sets (name, sport, season, league, tier, sample_image_url,
                             release_date, slug, is_visible, created_at)
           VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (SET["name"], SET["sport"], SET["season"], SET["league"], SET["tier"],
         SET["sample_image_url"], SET["release_date"], SET["slug"],
         SET["is_visible"], SET["created_at"]),
    )
    set_id = cur.lastrowid
    print(f"Created set id {set_id}: {SET['name']}")

    # ── insert_sets ── is_autograph from the per-card flag (consistent per subset)
    auto_by_subset = {}
    for r in rows:
        auto_by_subset.setdefault(r["subset"], r["is_autograph_subset"])
    is_id = {}
    for name in SUBSET_ORDER:
        c = db.execute(
            "INSERT INTO insert_sets (set_id, name, is_autograph) VALUES (?,?,?)",
            (set_id, name, 1 if auto_by_subset[name] else 0),
        )
        is_id[name] = c.lastrowid

    # ── players ── every distinct subject + every co-signer.
    # subjects carry their record's subject_role; co-signers (actors) are celebrity.
    role_by_name = {}
    for r in rows:
        role_by_name.setdefault(r["player"], r["subject_role"])
    for r in rows:
        for co in r.get("co_players", []):
            role_by_name.setdefault(co, "celebrity")

    player_id = {}
    for name, role in role_by_name.items():
        c = db.execute(
            "INSERT INTO players (set_id, name, subject_role) VALUES (?,?,?)",
            (set_id, name, role),
        )
        player_id[name] = c.lastrowid
    print(f"Created {len(player_id)} players")

    # ── appearances (one per card) + co-player links ──
    def subset_tag_for(r):
        if r.get("tag"):
            return r["tag"]                      # art cards: "Art by {artist}"
        if r.get("character"):
            return "as " + r["character"]        # autographs: "as {character}"
        return None                              # sketch artists: none

    co_links = 0
    for r in rows:
        # card_number is NOT NULL: use printed number, else the code, else the
        # subject name (sketch artists — matches the existing Sketch Cards convention).
        if r.get("card_number") is not None:
            card_no = str(r["card_number"])
        elif r.get("code"):
            card_no = r["code"]
        else:
            card_no = r["player"]
        c = db.execute(
            """INSERT INTO player_appearances (player_id, insert_set_id, card_number,
                                               is_rookie, subset_tag, team)
               VALUES (?,?,?,?,?,?)""",
            (player_id[r["player"]], is_id[r["subset"]], card_no, 0, subset_tag_for(r), None),
        )
        app_id = c.lastrowid
        for co in r.get("co_players", []):
            db.execute(
                "INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?,?)",
                (app_id, player_id[co]),
            )
            co_links += 1

    db.commit()

    # ── report ──
    print(f"\nInserted 540 appearances, {co_links} co-player links.")
    print("\nPer-subset appearance counts (DB):")
    got = db.execute(
        """SELECT i.name, i.is_autograph, COUNT(pa.id)
           FROM insert_sets i LEFT JOIN player_appearances pa ON pa.insert_set_id=i.id
           WHERE i.set_id=? GROUP BY i.id ORDER BY i.id""", (set_id,)
    ).fetchall()
    total = 0
    for name, auto, n in got:
        total += n
        print(f"  {name:35s} {n:4d}  {'[AUTO]' if auto else ''}")
    print(f"  TOTAL {total}")
    auto_subsets = [name for name, auto, n in got if auto]
    print(f"\nAutograph subsets ({len(auto_subsets)}): {auto_subsets}")
    print("players:", db.execute("SELECT COUNT(*) FROM players WHERE set_id=?", (set_id,)).fetchone()[0])
    print("co_player links:", db.execute(
        """SELECT COUNT(*) FROM appearance_co_players cp
           JOIN player_appearances pa ON pa.id=cp.appearance_id
           JOIN players p ON p.id=pa.player_id WHERE p.set_id=?""", (set_id,)).fetchone()[0])
    db.close()


if __name__ == "__main__":
    main()
