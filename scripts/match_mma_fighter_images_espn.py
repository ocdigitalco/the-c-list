"""
Match MMA fighter images from ESPN search API for fighters the Octagon API missed.
Updates the ufc_image_url column on the players table for MMA fighters.

This is a fallback script — run AFTER match_ufc_fighter_images.py.
It only touches players where ufc_image_url IS NULL or empty.

Usage:
  python3 scripts/match_mma_fighter_images_espn.py              # all unmatched MMA fighters
  python3 scripts/match_mma_fighter_images_espn.py --set-id 840 # single set only
  python3 scripts/match_mma_fighter_images_espn.py --dry-run    # preview without writing

Requirements: pip3 install requests
"""

import sqlite3
import requests
import os
import sys
import time
import csv
import unicodedata
import re
import argparse

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
ESPN_SEARCH_URL = "https://site.api.espn.com/apis/common/v3/search"
ESPN_HEADSHOT_TEMPLATE = "https://a.espncdn.com/i/headshots/mma/players/full/{espn_id}.png"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

REQUEST_DELAY = 0.3  # seconds between requests
MAX_RETRIES = 3
FUZZY_THRESHOLD = 0.92

# ─── Manual overrides ────────────────────────────────────────────────────────

MANUAL_NAME_MAP = {
    # DB name -> ESPN search query
    "BJ Penn": "B.J. Penn",
    "Joanna Jędrzejczyk": "Joanna Jedrzejczyk",
    "Yair Rodríguez": "Yair Rodriguez",
    "José Aldo": "Jose Aldo",
    "Patricio Freire": "Patricio Pitbull",
    "Khalil Rountree Jr.": "Khalil Rountree",
    "Jailton Malhadinho": "Jailton Almeida",
    "Shogun Rua": "Mauricio Rua",
    "Mingyang Zhang": "Zhang Mingyang",
    "Yadong Song": "Song Yadong",
    "Seok Hyeon Ko": "Ko Seok Hyeon",
    "Chang Ho Lee": "Lee Chang Ho",
    "Jeong Yeong Lee": "Lee Jeong Yeong",
    "JeongYeong Lee": "Lee Jeong Yeong",
    "Joo Sang Yoo": "Yoo Joo Sang",
    "Hyunsung Park": "Park Hyunsung",
}

SKIP_LIST = {
    "Dana White",      # promoter, not a fighter
    "Bruce Buffer",    # announcer
    "Hunter Campbell",  # UFC executive
}

# ─── Helpers ──────────────────────────────────────────────────────────────────

def normalize(name):
    return name.lower().strip()


def strip_diacritics(text):
    """Remove diacritics: José → Jose, Jędrzejczyk → Jedrzejczyk."""
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def strip_suffixes(name):
    """Remove Jr., Sr., III, II from the end."""
    return re.sub(r"\s+(Jr\.?|Sr\.?|III|II)\s*$", "", name, flags=re.IGNORECASE).strip()


def names_match(db_name, espn_name):
    """Check if two names match using progressive relaxation."""
    a = normalize(db_name)
    b = normalize(espn_name)

    # Exact
    if a == b:
        return True

    # Strip diacritics
    a_stripped = normalize(strip_diacritics(db_name))
    b_stripped = normalize(strip_diacritics(espn_name))
    if a_stripped == b_stripped:
        return True

    # Strip suffixes
    a_no_suffix = normalize(strip_suffixes(strip_diacritics(db_name)))
    b_no_suffix = normalize(strip_suffixes(strip_diacritics(espn_name)))
    if a_no_suffix == b_no_suffix:
        return True

    return False


def fuzzy_ratio(a, b):
    """Simple sequence matcher ratio."""
    from difflib import SequenceMatcher
    return SequenceMatcher(None, normalize(strip_diacritics(a)),
                           normalize(strip_diacritics(b))).ratio()


def search_espn(query, retries=MAX_RETRIES):
    """Search ESPN for an MMA athlete. Returns list of player results."""
    params = {
        "query": query,
        "limit": 10,
        "type": "player",
        "sport": "mma",
    }
    headers = {"User-Agent": USER_AGENT}

    for attempt in range(retries):
        try:
            resp = requests.get(ESPN_SEARCH_URL, params=params, headers=headers, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                players = []
                for result_group in data.get("results", []):
                    for item in result_group.get("contents", []):
                        if item.get("type") == "player":
                            sport = (item.get("sport") or "").lower()
                            if sport in ("mma", "mixed martial arts"):
                                players.append(item)
                return players
            elif resp.status_code == 429:
                wait = (2 ** attempt) * 2
                print(f"    Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            elif resp.status_code >= 500:
                wait = (2 ** attempt)
                print(f"    Server error {resp.status_code}, retrying in {wait}s...")
                time.sleep(wait)
                continue
            else:
                return []
        except requests.RequestException as e:
            if attempt < retries - 1:
                time.sleep(1)
                continue
            print(f"    Request error: {e}")
            return []
    return []


def verify_headshot(espn_id):
    """Check if the ESPN headshot URL actually exists (HEAD request)."""
    url = ESPN_HEADSHOT_TEMPLATE.format(espn_id=espn_id)
    try:
        resp = requests.head(url, headers={"User-Agent": USER_AGENT}, timeout=10,
                             allow_redirects=True)
        return resp.status_code == 200
    except requests.RequestException:
        return False


def extract_espn_id(item):
    """Extract ESPN athlete ID from a search result item."""
    # Try 'id' field directly
    eid = item.get("id")
    if eid:
        return str(eid)
    # Try parsing from uid: "s:3300~a:2335639"
    uid = item.get("uid", "")
    match = re.search(r"a:(\d+)", uid)
    if match:
        return match.group(1)
    return None


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Match MMA fighter images via ESPN search")
    parser.add_argument("--set-id", type=int, default=None, help="Scope to a single set ID")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing to DB")
    args = parser.parse_args()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Build query
    if args.set_id:
        cursor.execute("""
            SELECT DISTINCT p.id, p.name
            FROM players p
            JOIN sets s ON s.id = p.set_id
            WHERE s.sport = 'MMA'
            AND p.set_id = ?
            AND (p.ufc_image_url IS NULL OR p.ufc_image_url = '')
        """, (args.set_id,))
    else:
        cursor.execute("""
            SELECT DISTINCT p.id, p.name
            FROM players p
            JOIN sets s ON s.id = p.set_id
            WHERE s.sport = 'MMA'
            AND (p.ufc_image_url IS NULL OR p.ufc_image_url = '')
        """)

    rows = cursor.fetchall()
    scope = f"set {args.set_id}" if args.set_id else "all MMA sets"
    mode = "DRY RUN" if args.dry_run else "LIVE"
    print(f"ESPN MMA Fighter Image Matcher [{mode}]")
    print(f"Scope: {scope}")
    print(f"Found {len(rows)} unmatched fighters\n")

    if not rows:
        print("No unmatched fighters. Done.")
        conn.close()
        return

    # Deduplicate by name (same fighter across sets → one search)
    name_to_ids = {}
    for row_id, name in rows:
        if name not in name_to_ids:
            name_to_ids[name] = []
        name_to_ids[name].append(row_id)

    unique_names = sorted(name_to_ids.keys())
    print(f"Unique fighter names: {len(unique_names)}\n")

    # Stats
    matched = 0
    headshot_404 = 0
    no_match = 0
    skipped = 0
    errors = 0
    unmatched_names = []
    matched_records = []

    for i, name in enumerate(unique_names):
        if name in SKIP_LIST:
            print(f"  SKIP: {name} (skip list)")
            skipped += 1
            continue

        # Determine search query
        search_query = MANUAL_NAME_MAP.get(name, name)

        # Search ESPN
        results = search_espn(search_query)
        time.sleep(REQUEST_DELAY)

        if not results:
            # Try without diacritics if original had them
            alt_query = strip_diacritics(search_query)
            if alt_query != search_query:
                results = search_espn(alt_query)
                time.sleep(REQUEST_DELAY)

        if not results:
            unmatched_names.append(name)
            no_match += 1
            if (i + 1) % 20 == 0:
                print(f"  [{i+1}/{len(unique_names)}] No match: {name}")
            continue

        # Find best match
        best = None
        best_score = 0

        for item in results:
            display_name = item.get("displayName", "")
            if names_match(name, display_name) or names_match(search_query, display_name):
                espn_id = extract_espn_id(item)
                if espn_id:
                    best = (espn_id, display_name, 1.0)
                    break

        if not best:
            # Try fuzzy
            candidates = []
            for item in results:
                display_name = item.get("displayName", "")
                espn_id = extract_espn_id(item)
                if not espn_id:
                    continue
                score = max(fuzzy_ratio(name, display_name),
                           fuzzy_ratio(search_query, display_name))
                candidates.append((espn_id, display_name, score))

            candidates.sort(key=lambda x: x[2], reverse=True)
            if candidates and candidates[0][2] >= FUZZY_THRESHOLD:
                # Only auto-accept if single strong match
                if len(candidates) == 1 or candidates[0][2] - candidates[1][2] > 0.05:
                    best = candidates[0]

        if not best:
            unmatched_names.append(name)
            no_match += 1
            continue

        espn_id, espn_name, score = best

        # Verify headshot exists
        if not verify_headshot(espn_id):
            headshot_404 += 1
            print(f"  404: {name} -> ESPN:{espn_name} (ID:{espn_id}) headshot missing")
            unmatched_names.append(name)
            continue

        image_url = ESPN_HEADSHOT_TEMPLATE.format(espn_id=espn_id)
        player_ids = name_to_ids[name]

        if args.dry_run:
            print(f"  WOULD WRITE: {name} -> {espn_name} (ID:{espn_id}) [{len(player_ids)} rows]")
        else:
            for pid in player_ids:
                cursor.execute("UPDATE players SET ufc_image_url = ? WHERE id = ?", (image_url, pid))
            print(f"  Matched: {name} -> {espn_name} (ID:{espn_id}) [{len(player_ids)} rows]")

        matched += 1
        matched_records.append({
            "name": name,
            "espn_name": espn_name,
            "espn_id": espn_id,
            "image_url": image_url,
            "player_ids": player_ids,
            "score": score,
        })

    if not args.dry_run:
        conn.commit()
    conn.close()

    # Write output files
    script_dir = os.path.dirname(__file__)

    if unmatched_names:
        unmatched_path = os.path.join(script_dir, "unmatched_espn.txt")
        with open(unmatched_path, "w") as f:
            for n in sorted(set(unmatched_names)):
                f.write(n + "\n")
        print(f"\nWrote {len(set(unmatched_names))} unmatched names to unmatched_espn.txt")

    if matched_records:
        matched_path = os.path.join(script_dir, "matched_espn.csv")
        with open(matched_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "espn_name", "espn_id", "image_url", "player_ids", "score"])
            for r in matched_records:
                writer.writerow([r["name"], r["espn_name"], r["espn_id"], r["image_url"],
                                 ";".join(str(x) for x in r["player_ids"]), f"{r['score']:.3f}"])
        print(f"Wrote {len(matched_records)} matched records to matched_espn.csv")

    # Summary
    total = len(unique_names)
    print(f"\n{'='*50}")
    print(f"SUMMARY {'(DRY RUN)' if args.dry_run else ''}")
    print(f"{'='*50}")
    print(f"  Total candidates:  {total}")
    print(f"  Matched & updated: {matched}")
    print(f"  Headshot 404:      {headshot_404}")
    print(f"  No ESPN match:     {no_match}")
    print(f"  Skipped:           {skipped}")
    print(f"  Errors:            {errors}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
