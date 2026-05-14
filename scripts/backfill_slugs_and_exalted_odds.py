"""
Fix two bugs:
1. Attach pack odds to 2025 Topps Exalted WWE (set 60)
2. Backfill missing player slugs across all sets

Usage: python3 scripts/backfill_slugs_and_exalted_odds.py
"""
import sqlite3, os, json, re, unicodedata

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
db = sqlite3.connect(DB_PATH)
db.execute("PRAGMA journal_mode=WAL")

# ═══════════════════════════════════════════════════════════════════════════════
# BUG 1: Exalted WWE Pack Odds
# ═══════════════════════════════════════════════════════════════════════════════

EXALTED_ID = 60

pack_odds = {
    "hobby": {
        # Base Cards
        "Base Set": "1:1",
        "Base Set Aqua": "1:4",
        "Base Set Green": "1:7",
        "Base Set Blue": "1:13",
        "Base Set White": "1:3",
        "Base Set Purple": "1:31",
        "Base Set Red": "1:61",
        "Base Set Black": "1:302",
        # Exalted Autographs
        "Exalted Autographs": "1:4",
        "Exalted Autographs Aqua": "1:7",
        "Exalted Autographs Green": "1:13",
        "Exalted Autographs Blue": "1:26",
        "Exalted Autographs Red": "1:130",
        "Exalted Autographs Black": "1:644",
        # Ambient Autographs
        "Ambient Autographs": "1:8",
        "Ambient Autographs Aqua": "1:16",
        "Ambient Autographs Green": "1:31",
        "Ambient Autographs Blue": "1:63",
        "Ambient Autographs Red": "1:293",
        "Ambient Autographs Black": "1:1,463",
        # Streamline Signatures
        "Streamline Signatures": "1:9",
        "Streamline Signatures Aqua": "1:15",
        "Streamline Signatures Green": "1:29",
        "Streamline Signatures Blue": "1:58",
        "Streamline Signatures Red": "1:289",
        "Streamline Signatures Black": "1:1,441",
        # Apparition Autographs
        "Apparition Autographs": "1:6",
        "Apparition Autographs Aqua": "1:15",
        "Apparition Autographs Green": "1:29",
        "Apparition Autographs Blue": "1:59",
        "Apparition Autographs Red": "1:294",
        "Apparition Autographs Black": "1:1,441",
        # Black and White Signatures
        "Black and White Signatures": "1:7",
        "Black and White Signatures Aqua": "1:17",
        "Black and White Signatures Green": "1:32",
        "Black and White Signatures Blue": "1:68",
        "Black and White Signatures Red": "1:319",
        "Black and White Signatures Black": "1:1,682",
        # Elevated Ink
        "Elevated Ink": "1:5",
        "Elevated Ink Aqua": "1:11",
        "Elevated Ink Green": "1:21",
        "Elevated Ink Blue": "1:43",
        "Elevated Ink Red": "1:211",
        "Elevated Ink Black": "1:1,044",
        # Insignia Ink
        "Insignia Ink": "1:17",
        "Insignia Ink Aqua": "1:19",
        "Insignia Ink Green": "1:34",
        "Insignia Ink Blue": "1:65",
        "Insignia Ink Red": "1:319",
        "Insignia Ink Black": "1:1,593",
        # Exalted Relics
        "Exalted Relics": "1:4",
        "Exalted Relics Aqua": "1:7",
        "Exalted Relics Green": "1:13",
        "Exalted Relics Blue": "1:25",
        "Exalted Relics Red": "1:124",
        "Exalted Relics Black": "1:618",
        # Mega Materials
        "Mega Materials": "1:7",
        "Mega Materials Aqua": "1:13",
        "Mega Materials Green": "1:25",
        "Mega Materials Blue": "1:49",
        "Mega Materials Red": "1:243",
        "Mega Materials Black": "1:1,211",
        # Quad Relics
        "Quad Relics": "1:31",
        "Quad Relics Aqua": "1:62",
        "Quad Relics Green": "1:122",
        "Quad Relics Blue": "1:243",
        "Quad Relics Red": "1:1,211",
        "Quad Relics Black": "1:6,052",
        # Rivaled Relics
        "Rivaled Relics": "1:17",
        "Rivaled Relics Aqua": "1:31",
        "Rivaled Relics Green": "1:61",
        "Rivaled Relics Blue": "1:122",
        "Rivaled Relics Red": "1:606",
        "Rivaled Relics Black": "1:3,026",
        # Tag Team Relics
        "Tag Team Relics": "1:16",
        "Tag Team Relics Aqua": "1:31",
        "Tag Team Relics Green": "1:61",
        "Tag Team Relics Blue": "1:122",
        "Tag Team Relics Red": "1:606",
        "Tag Team Relics Black": "1:3,026",
        # John Cena: The Last Time Is Now Autograph
        "John Cena: The Last Time Is Now Autograph Green": "1:606",
        "John Cena: The Last Time Is Now Autograph Blue": "1:1,211",
        "John Cena: The Last Time Is Now Autograph Red": "1:10,087",
        "John Cena: The Last Time Is Now Autograph Black": "1:30,260",
        # John Cena: The Last Time Is Now Relic
        "John Cena: The Last Time Is Now Relic Aqua": "1:306",
        "John Cena: The Last Time Is Now Relic Green": "1:606",
        "John Cena: The Last Time Is Now Relic Blue": "1:1,211",
        "John Cena: The Last Time Is Now Relic Red": "1:6,052",
        "John Cena: The Last Time Is Now Relic Black": "1:30,260",
        # Celebrating Cena Autographs
        "Celebrating Cena Autographs": "1:757",
        # Superstar Rivalry Signatures
        "Superstar Rivalry Signatures": "1:3,026",
        "Superstar Rivalry Signatures Superfractor": "1:15,130",
        # Superstar Rivalry Variation Signatures
        "Superstar Rivalry Variation Signatures": "1:1,261",
        "Superstar Rivalry Variation Signatures Black Refractor": "1:3,026",
        "Superstar Rivalry Variation Signatures Red Refractor": "1:6,052",
        "Superstar Rivalry Variation Signatures Superfractor": "1:30,260",
        # The Rock Retrospective Autographs
        "The Rock Retrospective Autographs": "1:1,513",
        "The Rock Retrospective Autographs Red Refractor": "1:3,026",
        "The Rock Retrospective Autographs Superfractor": "1:15,130",
        # Triple H Tribute Autographs
        "Triple H Tribute Autographs": "1:1,009",
    }
}

db.execute("UPDATE sets SET pack_odds = ? WHERE id = ?", (json.dumps(pack_odds), EXALTED_ID))
print(f"Bug 1: Attached pack odds to set {EXALTED_ID} (2025 Topps Exalted WWE)")

# ═══════════════════════════════════════════════════════════════════════════════
# BUG 2: Backfill Missing Player Slugs
# ═══════════════════════════════════════════════════════════════════════════════

def slugify(text):
    """Generate a URL-safe slug from a name. Strips diacritics, quotes, apostrophes."""
    # Normalize unicode (strip diacritics: é→e, á→a, etc.)
    s = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    s = s.lower().strip()
    # Remove non-alphanumeric except spaces and hyphens
    s = re.sub(r'[^\w\s-]', '', s)
    # Replace whitespace/underscores with hyphens
    s = re.sub(r'[\s_]+', '-', s)
    # Collapse multiple hyphens
    return re.sub(r'-+', '-', s).strip('-')

# Find all players missing slugs
missing = db.execute("SELECT id, set_id, name FROM players WHERE slug IS NULL OR slug = ''").fetchall()
print(f"\nBug 2: Found {len(missing)} players missing slugs")

# Group by set for collision detection
from collections import defaultdict
by_set = defaultdict(list)
for pid, sid, name in missing:
    by_set[sid].append((pid, name))

updated = 0
for sid, players_list in by_set.items():
    # Get existing slugs for this set
    existing = set(
        r[0] for r in db.execute(
            "SELECT slug FROM players WHERE set_id = ? AND slug IS NOT NULL AND slug != ''", (sid,)
        ).fetchall()
    )
    for pid, name in players_list:
        slug = slugify(name)
        candidate = slug
        i = 2
        while candidate in existing:
            candidate = f"{slug}-{i}"
            i += 1
        existing.add(candidate)
        db.execute("UPDATE players SET slug = ? WHERE id = ?", (candidate, pid))
        updated += 1

print(f"  Updated {updated} player slugs across {len(by_set)} sets")

db.commit()

# Verify
remaining = db.execute("SELECT COUNT(*) FROM players WHERE slug IS NULL OR slug = ''").fetchone()[0]
print(f"  Remaining missing slugs: {remaining}")

# Spot-check
spot_checks = [
    ("CM Punk", 60),
    ('"Stone Cold" Steve Austin', 60),
    ('Bret "Hit Man" Hart', 60),
    ("Finn Balor", 60),
    ("Cam Ward", 842),
    ("Cam Ward", 844),
]
print("\nSpot checks:")
for name, sid in spot_checks:
    row = db.execute("SELECT name, slug FROM players WHERE name = ? AND set_id = ?", (name, sid)).fetchone()
    if row:
        print(f"  {row[0]} (set {sid}): {row[1]}")

db.close()
print("\nDone!")
