"""
Match UFC fighter images from Octagon API to players in the local SQLite database.
Updates the ufc_image_url column on the players table for MMA fighters.

Usage: python3 scripts/match_ufc_fighter_images.py

Requirements: pip3 install requests rapidfuzz
"""

import sqlite3
import requests
import os
import time
from rapidfuzz import process, fuzz

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
OCTAGON_API_BASE = "https://api.octagon-api.com"
MATCH_THRESHOLD = 85


def normalize(name):
    return name.lower().strip()


def fetch_all_fighters():
    """Fetch all fighters from Octagon API.

    The API returns a dict keyed by slug, e.g.:
    { "ilia-topuria": { "name": "Ilia Topuria", "imgUrl": "https://...", ... }, ... }
    """
    print("Fetching fighters from Octagon API...")

    try:
        response = requests.get(f"{OCTAGON_API_BASE}/fighters", timeout=30)
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict):
                # Convert slug-keyed dict to list of fighter objects
                fighters = list(data.values())
                print(f"  Fetched {len(fighters)} fighters")
                return fighters
            elif isinstance(data, list):
                print(f"  Fetched {len(data)} fighters (list format)")
                return data
    except Exception as e:
        print(f"  Error: {e}")

    return []


def extract_image_url(fighter):
    """Extract image URL from fighter object."""
    for field in [
        "imgUrl", "image_url", "image", "photo_url", "photo",
        "headshot", "thumbnail", "avatar", "picture",
    ]:
        val = fighter.get(field)
        if val and isinstance(val, str) and val.startswith("http"):
            return val
    return None


def extract_name(fighter):
    """Extract full name from fighter object."""
    if "name" in fighter and fighter["name"]:
        return fighter["name"]
    if "full_name" in fighter and fighter["full_name"]:
        return fighter["full_name"]
    first = fighter.get("first_name", "") or fighter.get("firstName", "")
    last = fighter.get("last_name", "") or fighter.get("lastName", "")
    if first and last:
        return f"{first} {last}"
    return None


def main():
    fighters = fetch_all_fighters()

    if not fighters:
        print("\nNo fighters fetched. Trying to inspect API structure...")
        try:
            r = requests.get(OCTAGON_API_BASE, timeout=10)
            print(f"Base URL status: {r.status_code}")
            print(f"Response: {r.text[:1000]}")
        except Exception as e:
            print(f"Could not inspect API: {e}")
        return

    # Print sample fighter to understand structure
    print(f"\nSample fighter object keys: {list(fighters[0].keys())}")
    sample = fighters[0]
    for k, v in sample.items():
        print(f"  {k}: {repr(v)[:100]}")

    # Build lookup: normalized name -> image URL
    api_lookup = {}
    for f in fighters:
        name = extract_name(f)
        image_url = extract_image_url(f)
        if name and image_url:
            api_lookup[normalize(name)] = image_url

    print(f"\n{len(api_lookup)} fighters with images found in API")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get all MMA players without a ufc_image_url
    cursor.execute("""
        SELECT DISTINCT p.id, p.name
        FROM players p
        JOIN sets s ON s.id = p.set_id
        WHERE s.sport = 'MMA'
        AND (p.ufc_image_url IS NULL OR p.ufc_image_url = '')
    """)
    rows = cursor.fetchall()
    print(f"Found {len(rows)} MMA fighters to match\n")

    if not rows:
        print("No MMA fighters found needing images.")
        conn.close()
        return

    api_names = list(api_lookup.keys())
    matched = 0
    unmatched = []

    for row_id, name in rows:
        if not name:
            continue
        normalized = normalize(name)

        # Exact match
        if normalized in api_lookup:
            cursor.execute(
                "UPDATE players SET ufc_image_url = ? WHERE id = ?",
                (api_lookup[normalized], row_id),
            )
            matched += 1
            print(f"  Exact: {name}")
            continue

        # Fuzzy match
        result = process.extractOne(
            normalized, api_names, scorer=fuzz.token_sort_ratio
        )
        if result and result[1] >= MATCH_THRESHOLD:
            best_match, score, _ = result
            cursor.execute(
                "UPDATE players SET ufc_image_url = ? WHERE id = ?",
                (api_lookup[best_match], row_id),
            )
            matched += 1
            print(f"  Fuzzy ({score:.0f}%): {name} -> {best_match}")
        else:
            unmatched.append(name)

    conn.commit()
    conn.close()

    print(f"\nDone: {matched}/{len(rows)} matched, {len(unmatched)} unmatched")
    if unmatched:
        print(f"\nUnmatched fighters ({len(unmatched)}):")
        for name in sorted(set(unmatched)):
            print(f"  - {name}")


if __name__ == "__main__":
    main()
