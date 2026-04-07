"""
Match MLB player IDs from the MLB Stats API to players in the local SQLite database.
Updates the mlb_player_id column on the players table for Baseball players.

CDN URL pattern: https://midfield.mlbstatic.com/v1/people/{player_id}/spots/120

Usage: python3 scripts/match_mlb_player_ids.py

Requirements: pip3 install requests rapidfuzz
"""

import sqlite3
import requests
import os
from rapidfuzz import process, fuzz

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
MLB_API_BASE = "https://statsapi.mlb.com/api/v1"
MATCH_THRESHOLD = 85


def normalize(name):
    return name.lower().strip()


def fetch_all_mlb_players():
    """Fetch all players from MLB Stats API across multiple seasons."""
    print("Fetching MLB players from Stats API...")
    players = []
    seen_ids = set()

    seasons = ["2025", "2024", "2023", "2022", "2021", "2020"]

    for season in seasons:
        try:
            url = f"{MLB_API_BASE}/sports/1/players?season={season}&gameType=R"
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                season_players = data.get("people", [])
                new_count = 0
                for p in season_players:
                    if p["id"] not in seen_ids:
                        players.append(p)
                        seen_ids.add(p["id"])
                        new_count += 1
                print(f"  Season {season}: {len(season_players)} total, {new_count} new")
        except Exception as e:
            print(f"  Error fetching season {season}: {e}")

    print(f"Total unique players fetched: {len(players)}")
    return players


def main():
    mlb_players = fetch_all_mlb_players()

    if not mlb_players:
        print("No players fetched. Check API connectivity.")
        return

    # Print sample
    sample = mlb_players[0]
    print(f"\nSample player keys: {list(sample.keys())}")
    print(f"Sample: id={sample.get('id')}, fullName={sample.get('fullName')}")

    # Build lookup: normalized full name -> player_id
    mlb_lookup = {}
    for p in mlb_players:
        full_name = p.get("fullName", "")
        if full_name and p.get("id"):
            mlb_lookup[normalize(full_name)] = p["id"]

    print(f"{len(mlb_lookup)} players with IDs in lookup")
    mlb_names = list(mlb_lookup.keys())

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get all Baseball players without mlb_player_id
    cursor.execute("""
        SELECT DISTINCT p.id, p.name
        FROM players p
        JOIN sets s ON s.id = p.set_id
        WHERE s.sport = 'Baseball'
        AND (p.mlb_player_id IS NULL)
    """)
    rows = cursor.fetchall()
    print(f"\nFound {len(rows)} Baseball players to match\n")

    if not rows:
        print("No Baseball players found needing IDs.")
        conn.close()
        return

    matched = 0
    unmatched = []

    for row_id, name in rows:
        if not name:
            continue
        normalized = normalize(name)

        # Exact match
        if normalized in mlb_lookup:
            cursor.execute(
                "UPDATE players SET mlb_player_id = ? WHERE id = ?",
                (mlb_lookup[normalized], row_id),
            )
            matched += 1
            continue

        # Fuzzy match
        result = process.extractOne(
            normalized, mlb_names, scorer=fuzz.token_sort_ratio
        )
        if result and result[1] >= MATCH_THRESHOLD:
            best_match, score, _ = result
            cursor.execute(
                "UPDATE players SET mlb_player_id = ? WHERE id = ?",
                (mlb_lookup[best_match], row_id),
            )
            matched += 1
        else:
            unmatched.append(name)

    conn.commit()
    conn.close()

    print(f"Done: {matched}/{len(rows)} matched, {len(unmatched)} unmatched")
    if unmatched:
        print(f"\nUnmatched players ({len(unmatched)}):")
        for name in sorted(set(unmatched)):
            print(f"  - {name}")


if __name__ == "__main__":
    main()
