# Requirements: pip install nba_api rapidfuzz
# This script matches athlete names in our DB to NBA player IDs
# and stores the nba_player_id back in the database

import sqlite3
from nba_api.stats.static import players
from rapidfuzz import process, fuzz

DB_PATH = "the-c-list.db"
MATCH_THRESHOLD = 85  # minimum similarity score to accept a match


def normalize(name):
    return name.lower().strip()


def main():
    # Get all NBA players from nba_api
    all_nba_players = players.get_players()
    nba_lookup = {normalize(p["full_name"]): p["id"] for p in all_nba_players}
    nba_names = list(nba_lookup.keys())

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get distinct player names from Basketball sets (NBA + McDonald's)
    cursor.execute("""
        SELECT DISTINCT p.id, p.name
        FROM players p
        JOIN sets s ON p.set_id = s.id
        WHERE s.sport = 'Basketball'
        AND (p.nba_player_id IS NULL)
    """)

    rows = cursor.fetchall()
    print(f"Found {len(rows)} Basketball athletes to match")

    matched = 0
    unmatched = []

    for row_id, name in rows:
        if not name or name == "Team Card":
            continue
        normalized = normalize(name)

        # Try exact match first
        if normalized in nba_lookup:
            player_id = nba_lookup[normalized]
            cursor.execute(
                "UPDATE players SET nba_player_id = ? WHERE id = ?",
                (player_id, row_id),
            )
            matched += 1
            print(f"  ✓ Exact: {name} → {player_id}")
            continue

        # Try fuzzy match
        result = process.extractOne(
            normalized, nba_names, scorer=fuzz.token_sort_ratio
        )
        if result and result[1] >= MATCH_THRESHOLD:
            best_match, score, _ = result
            player_id = nba_lookup[best_match]
            cursor.execute(
                "UPDATE players SET nba_player_id = ? WHERE id = ?",
                (player_id, row_id),
            )
            matched += 1
            print(f"  ✓ Fuzzy ({score:.0f}%): {name} → {best_match} → {player_id}")
        else:
            unmatched.append(name)
            print(f"  ✗ No match: {name}")

    conn.commit()
    conn.close()

    print(f"\nDone: {matched} matched, {len(unmatched)} unmatched")
    if unmatched:
        print(f"\nUnmatched athletes ({len(unmatched)}):")
        for name in sorted(set(unmatched)):
            print(f"  - {name}")


if __name__ == "__main__":
    main()
