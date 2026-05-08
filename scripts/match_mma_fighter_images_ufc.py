"""
Match MMA fighter images by scraping UFC.com athlete pages.
Fallback for fighters the Octagon API couldn't match.
Updates the ufc_image_url column on the players table.

Usage:
  python3 scripts/match_mma_fighter_images_ufc.py              # all unmatched
  python3 scripts/match_mma_fighter_images_ufc.py --set-id 840 # single set
  python3 scripts/match_mma_fighter_images_ufc.py --dry-run    # preview

Requirements: pip3 install requests
"""

import sqlite3
import requests
import os
import re
import time
import csv
import unicodedata
import argparse

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
UFC_ATHLETE_URL = "https://www.ufc.com/athlete/{slug}"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
REQUEST_DELAY = 0.5
MAX_RETRIES = 3

# ─── Manual overrides: DB name -> UFC.com slug ───────────────────────────────

MANUAL_SLUG_MAP = {
    "BJ Penn": "bj-penn",
    "Patricio Freire": "patricio-pitbull",
    "Jailton Malhadinho": "jailton-almeida",
    "Shogun Rua": "mauricio-shogun-rua",
    "José Aldo": "jose-aldo",
    "Joanna Jędrzejczyk": "joanna-jedrzejczyk",
    "Yair Rodríguez": "yair-rodriguez",
    "Khalil Rountree Jr.": "khalil-rountree-jr",
    "Mingyang Zhang": "mingyang-zhang",
    "Yadong Song": "yadong-song",
    "Seok Hyeon Ko": "seok-hyun-ko",
    "Chang Ho Lee": "chang-ho-lee",
    "Jeong Yeong Lee": "jeong-yeong-lee",
    "JeongYeong Lee": "jeong-yeong-lee",
    "Joo Sang Yoo": "joo-sang-yoo",
    "Hyunsung Park": "hyun-sung-park",
    "Julianna Peña": "julianna-pena",
    "Natalia Cristina da Silva": "natalia-silva",
    "Natalia Cristina Da Silva": "natalia-silva",
    "Stipe Miocic": "stipe-miocic",
    "Georges St-Pierre": "georges-st-pierre",
    "T.J. Dillashaw": "tj-dillashaw",
    "TJ Dillashaw": "tj-dillashaw",
    "Aleksei Oleinik": "aleksei-oleinik",
    "MarQuel Mederos": "marquel-mederos",
    "Marquel Mederos": "marquel-mederos",
    "Da'Mon Blackshear": "damon-blackshear",
    "Lone'er Kavanagh": "loneer-kavanagh",
}

SKIP_LIST = {
    "Dana White",
    "Bruce Buffer",
    "Hunter Campbell",
}

# ─── Helpers ──────────────────────────────────────────────────────────────────

def strip_diacritics(text):
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def name_to_slug(name):
    """Convert a fighter name to a UFC.com URL slug."""
    s = strip_diacritics(name).lower().strip()
    s = re.sub(r"['\"]", "", s)  # Remove apostrophes/quotes
    s = re.sub(r"[^\w\s-]", "", s)  # Remove special chars except hyphens
    s = re.sub(r"[\s_]+", "-", s)  # Spaces to hyphens
    s = re.sub(r"-+", "-", s).strip("-")
    return s


def fetch_athlete_image(slug, retries=MAX_RETRIES):
    """Fetch image URL from UFC.com athlete page."""
    url = UFC_ATHLETE_URL.format(slug=slug)
    headers = {"User-Agent": USER_AGENT}

    for attempt in range(retries):
        try:
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code == 200:
                images = re.findall(
                    r'(https://ufc\.com/images/styles/athlete_bio[^"\']+)',
                    resp.text
                )
                return images[0] if images else None
            elif resp.status_code == 404:
                return None
            elif resp.status_code == 429:
                wait = (2 ** attempt) * 2
                time.sleep(wait)
                continue
            elif resp.status_code >= 500:
                time.sleep(2 ** attempt)
                continue
            else:
                return None
        except requests.RequestException:
            if attempt < retries - 1:
                time.sleep(1)
                continue
            return None
    return None


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Match MMA fighter images via UFC.com scrape")
    parser.add_argument("--set-id", type=int, default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if args.set_id:
        cursor.execute("""
            SELECT DISTINCT p.id, p.name
            FROM players p JOIN sets s ON s.id = p.set_id
            WHERE s.sport = 'MMA' AND p.set_id = ?
            AND (p.ufc_image_url IS NULL OR p.ufc_image_url = '')
        """, (args.set_id,))
    else:
        cursor.execute("""
            SELECT DISTINCT p.id, p.name
            FROM players p JOIN sets s ON s.id = p.set_id
            WHERE s.sport = 'MMA'
            AND (p.ufc_image_url IS NULL OR p.ufc_image_url = '')
        """)

    rows = cursor.fetchall()
    mode = "DRY RUN" if args.dry_run else "LIVE"
    scope = f"set {args.set_id}" if args.set_id else "all MMA sets"
    print(f"UFC.com Fighter Image Scraper [{mode}]")
    print(f"Scope: {scope}")
    print(f"Found {len(rows)} unmatched fighters\n")

    if not rows:
        print("No unmatched fighters. Done.")
        conn.close()
        return

    # Deduplicate by name
    name_to_ids = {}
    for row_id, name in rows:
        if name not in name_to_ids:
            name_to_ids[name] = []
        name_to_ids[name].append(row_id)

    unique_names = sorted(name_to_ids.keys())
    print(f"Unique fighter names: {len(unique_names)}\n")

    matched = 0
    no_match = 0
    skipped = 0
    unmatched_names = []
    matched_records = []

    for i, name in enumerate(unique_names):
        if name in SKIP_LIST:
            print(f"  SKIP: {name}")
            skipped += 1
            continue

        # Determine slug
        slug = MANUAL_SLUG_MAP.get(name, name_to_slug(name))

        # Try primary slug
        image_url = fetch_athlete_image(slug)
        time.sleep(REQUEST_DELAY)

        # If no image, try alternate slugs
        if not image_url:
            alt_slugs = set()
            # Try without Jr./Sr. suffix
            stripped = re.sub(r"\s+(jr|sr|iii|ii)\.?$", "", name, flags=re.IGNORECASE).strip()
            if stripped != name:
                alt_slugs.add(name_to_slug(stripped))
            # Try reversed name for Asian naming conventions
            parts = name.split()
            if len(parts) == 2:
                alt_slugs.add(name_to_slug(f"{parts[1]} {parts[0]}"))
            # Try with diacritics stripped
            alt_slugs.add(name_to_slug(strip_diacritics(name)))
            alt_slugs.discard(slug)  # Don't retry same slug

            for alt in alt_slugs:
                image_url = fetch_athlete_image(alt)
                time.sleep(REQUEST_DELAY)
                if image_url:
                    break

        if not image_url:
            unmatched_names.append(name)
            no_match += 1
            if (i + 1) % 10 == 0 or no_match <= 5:
                print(f"  [{i+1}/{len(unique_names)}] No image: {name} (tried: {slug})")
            continue

        player_ids = name_to_ids[name]

        if args.dry_run:
            print(f"  WOULD WRITE: {name} -> {image_url[:70]}... [{len(player_ids)} rows]")
        else:
            for pid in player_ids:
                cursor.execute("UPDATE players SET ufc_image_url = ? WHERE id = ?", (image_url, pid))
            print(f"  Matched: {name} [{len(player_ids)} rows]")

        matched += 1
        matched_records.append({"name": name, "image_url": image_url, "player_ids": player_ids})

    if not args.dry_run:
        conn.commit()
    conn.close()

    # Write output files
    script_dir = os.path.dirname(__file__)

    if unmatched_names:
        path = os.path.join(script_dir, "unmatched_ufc_scrape.txt")
        with open(path, "w") as f:
            for n in sorted(set(unmatched_names)):
                f.write(n + "\n")
        print(f"\nWrote {len(set(unmatched_names))} unmatched to unmatched_ufc_scrape.txt")

    if matched_records:
        path = os.path.join(script_dir, "matched_ufc_scrape.csv")
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "image_url", "player_ids"])
            for r in matched_records:
                writer.writerow([r["name"], r["image_url"], ";".join(str(x) for x in r["player_ids"])])
        print(f"Wrote {len(matched_records)} matched to matched_ufc_scrape.csv")

    print(f"\n{'='*50}")
    print(f"SUMMARY {'(DRY RUN)' if args.dry_run else ''}")
    print(f"{'='*50}")
    print(f"  Total candidates:  {len(unique_names)}")
    print(f"  Matched & updated: {matched}")
    print(f"  No image found:    {no_match}")
    print(f"  Skipped:           {skipped}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
