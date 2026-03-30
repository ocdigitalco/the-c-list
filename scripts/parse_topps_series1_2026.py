import json
import re
from pathlib import Path

# ─────────────────────────────────────────────────────────────
# Load checklist
# ─────────────────────────────────────────────────────────────
_HERE = Path(__file__).parent
CHECKLIST = (_HERE / "topps_series1_2026_checklist.txt").read_text(encoding="utf-8")

# ─────────────────────────────────────────────────────────────
# Parallel block definitions (hardcoded per section)
# ─────────────────────────────────────────────────────────────

BASE_PARALLELS = [
    {"name": "Diamante Foil", "print_run": None},
    {"name": "Holo Foil", "print_run": None},
    {"name": "Pink Diamante Foil", "print_run": None},
    {"name": "Rainbow Foil", "print_run": None},
    {"name": "Sandglitter", "print_run": None},
    {"name": "Silver Crackleboard Foil Board", "print_run": None},
    {"name": "Spring Training", "print_run": None},
    {"name": "Topps Foil Pattern", "print_run": None},
    {"name": "Aqua Rainbow Foil", "print_run": None},
    {"name": "Aqua Holo Foil", "print_run": None},
    {"name": "Gold", "print_run": 2026},
    {"name": "Pink Holo Foil", "print_run": 800},
    {"name": "Yellow Holo Foil", "print_run": 399},
    {"name": "Yellow Rainbow Foil", "print_run": 399},
    {"name": "Purple Holo Foil", "print_run": 250},
    {"name": "Purple Rainbow Foil", "print_run": 250},
    {"name": "Blue Holo Foil", "print_run": 150},
    {"name": "Blue Rainbow Foil", "print_run": 150},
    {"name": "Cherry Blossom", "print_run": 99},
    {"name": "Green Diamante Foil", "print_run": 99},
    {"name": "Green Holo Foil", "print_run": None},
    {"name": "Green Rainbow Foil", "print_run": 99},
    {"name": "Green Spring Training", "print_run": 99},
    {"name": "Independence Day", "print_run": 76},
    {"name": "75 Years of Topps", "print_run": 75},
    {"name": "Black Border", "print_run": 75},
    {"name": "Gold Diamante Foil", "print_run": 50},
    {"name": "Gold Holo Foil", "print_run": 50},
    {"name": "Gold Rainbow Foil", "print_run": 50},
    {"name": "Gold Sandglitter", "print_run": 50},
    {"name": "Gold Spring Training", "print_run": 50},
    {"name": "Canvas", "print_run": 50},
    {"name": "Memorial Day Camo", "print_run": 25},
    {"name": "Orange Diamante Foil", "print_run": 25},
    {"name": "Orange Holo Foil", "print_run": 25},
    {"name": "Orange Rainbow Foil", "print_run": 25},
    {"name": "Orange Sandglitter", "print_run": 25},
    {"name": "Orange Spring Training", "print_run": 25},
    {"name": "Wood", "print_run": 25},
    {"name": "Black Diamante Foil", "print_run": 10},
    {"name": "Black Holo Foil", "print_run": 10},
    {"name": "Black Rainbow Foil", "print_run": 10},
    {"name": "Black Sandglitter", "print_run": 10},
    {"name": "Black Spring Training", "print_run": 10},
    {"name": "Red Diamante Foil", "print_run": 5},
    {"name": "Red Holo Foil", "print_run": 5},
    {"name": "Red Rainbow Foil", "print_run": 5},
    {"name": "Red Sandglitter", "print_run": 5},
    {"name": "Red Spring Training", "print_run": 5},
    {"name": "First Card", "print_run": 1},
    {"name": "Foilfractor", "print_run": 1},
    {"name": "Rose Gold Holo Foil", "print_run": 1},
    {"name": "Rose Gold Spring Training", "print_run": 1},
    {"name": "Printing Plates", "print_run": 1},
]

PARALLELS_INSERT_STD = [
    {"name": "Pink Foil", "print_run": None},
    {"name": "Blue Foil", "print_run": 150},
    {"name": "Green Foil", "print_run": 99},
    {"name": "Gold Foil", "print_run": 50},
    {"name": "Orange Foil", "print_run": 25},
    {"name": "Black Foil", "print_run": 10},
    {"name": "Red Foil", "print_run": 5},
    {"name": "Foilfractor", "print_run": 1},
]

PARALLELS_AUTO_STD = [
    {"name": "Blue Foil", "print_run": 150},
    {"name": "Green Foil", "print_run": 99},
    {"name": "Gold Foil", "print_run": 50},
    {"name": "Orange Foil", "print_run": 25},
    {"name": "Black Foil", "print_run": 10},
    {"name": "Red Foil", "print_run": 5},
    {"name": "Foilfractor", "print_run": 1},
]

PARALLELS_RELIC_STD = [
    {"name": "Blue", "print_run": 150},
    {"name": "Green", "print_run": 99},
    {"name": "Gold", "print_run": 50},
    {"name": "Orange", "print_run": 25},
    {"name": "Black", "print_run": 10},
    {"name": "Red", "print_run": 5},
    {"name": "Platinum", "print_run": 1},
]

PARALLELS_RELIC_NO_BLUE = [
    {"name": "Gold", "print_run": 50},
    {"name": "Orange", "print_run": 25},
    {"name": "Black", "print_run": 10},
    {"name": "Red", "print_run": 5},
    {"name": "Foilfractor", "print_run": 1},
]

PARALLELS_CRACKLEBOARD = [
    {"name": "Crackleboard Foil", "print_run": None},
    {"name": "Green", "print_run": 99},
    {"name": "Green Crackleboard Foil", "print_run": 99},
    {"name": "Gold", "print_run": 50},
    {"name": "Gold Crackleboard Foil", "print_run": 50},
    {"name": "Orange", "print_run": 25},
    {"name": "Orange Crackleboard Foil", "print_run": 25},
    {"name": "Black", "print_run": 10},
    {"name": "Black Crackleboard Foil", "print_run": 10},
    {"name": "Red", "print_run": 5},
    {"name": "Red Crackleboard Foil", "print_run": 5},
    {"name": "Foilfractor", "print_run": 1},
]

SECTION_PARALLELS = {
    "Base Set": BASE_PARALLELS,
    "Base \u2013 Golden Mirror Variation": BASE_PARALLELS,
    "Base \u2013 Vintage Stock Variations": [{"name": "Base", "print_run": 99}],
    "Base \u2013 Clear Variation": [{"name": "Base", "print_run": 10}],
    "Base \u2013 Holiday Variation": [],
    "Base \u2013 True Photo Variation": [],
    "Base \u2013 Player Number Variations": [],
    "Base \u2013 Team Color Border Variation": [],
    "Base \u2013 1952 Topps Rookie Variations": [],
    "Base \u2013 Golden Mirror Legend Variations": [],
    "Through The Years Golden Mirror Variations": [],
    "Base \u2013 Canadian Independence Day Variations": [{"name": "Base", "print_run": 67}],
    "Flagship Real One Autographs": [
        {"name": "Green Foil", "print_run": 99},
        {"name": "75th Anniversary", "print_run": 75},
        {"name": "Gold Foil", "print_run": 50},
        {"name": "Orange Foil", "print_run": 25},
        {"name": "Black Foil", "print_run": 10},
        {"name": "Red Foil", "print_run": 5},
        {"name": "Foilfractor", "print_run": 1},
    ],
    "75 Years Of Topps Die-Cut Autographs": [
        {"name": "Gold Foil", "print_run": 50},
        {"name": "Orange Foil", "print_run": 25},
        {"name": "Black Foil", "print_run": 10},
        {"name": "Red Foil", "print_run": 5},
        {"name": "Foilfractor", "print_run": 1},
    ],
    "Baseball Stars Autographs": PARALLELS_AUTO_STD,
    "1991 Topps Baseball Autographs": PARALLELS_AUTO_STD,
    "1991 Topps Baseball Chrome Autographs": [],
    "Cover Athlete Autographs": [],
    "1952 Base Rookies Variation Autographs": [
        {"name": "Red", "print_run": 5},
        {"name": "Black", "print_run": 1},
    ],
    "Major League Material Autographs": [
        {"name": "Orange", "print_run": 25},
        {"name": "Black", "print_run": 10},
        {"name": "Red", "print_run": 5},
        {"name": "Platinum", "print_run": 1},
    ],
    "Major League Materials Dual Autographs": [
        {"name": "Orange", "print_run": 25},
        {"name": "Black", "print_run": 10},
        {"name": "Red", "print_run": 5},
        {"name": "Platinum", "print_run": 1},
    ],
    "Heavy Lumber Autographed Relics": [],
    "City Connect Swatch Collection Autographed Relics": [
        {"name": "Gold", "print_run": 50},
        {"name": "Orange", "print_run": 25},
        {"name": "Black", "print_run": 10},
        {"name": "Red", "print_run": 5},
        {"name": "Platinum", "print_run": 1},
    ],
    "Topps Flagship Autographed Patches": [
        {"name": "Bronze", "print_run": 25},
        {"name": "Black", "print_run": 10},
        {"name": "Red", "print_run": 5},
        {"name": "Platinum", "print_run": 1},
    ],
    "Funko Pop Autographs": [],
    "Signature Tunes Dual Autograph": [],
    "First Pitch Autographs": [
        {"name": "Gold", "print_run": 50},
        {"name": "Orange", "print_run": 25},
        {"name": "Black", "print_run": 10},
        {"name": "Red", "print_run": 5},
        {"name": "Foilfractor", "print_run": 1},
    ],
    "75 Years Of Topps Autographs": [
        {"name": "Foilfractor", "print_run": 1},
    ],
    "Topps Autograph Jerry Seinfeid": [],
    "Major League Material": PARALLELS_RELIC_STD,
    "1991 Topps Baseball Relics": PARALLELS_RELIC_STD,
    "City Connect Swatch Collection": PARALLELS_RELIC_STD,
    "Real One Relics": PARALLELS_RELIC_NO_BLUE,
    "In The Name Relics": [{"name": "Base", "print_run": 1}],
    "2025 All-Topps Team": PARALLELS_INSERT_STD,
    "2025 Greatest Hits": PARALLELS_INSERT_STD,
    "Topps Profiles": PARALLELS_INSERT_STD,
    "Big Ticket Players": PARALLELS_INSERT_STD,
    "First Pitch": PARALLELS_INSERT_STD,
    "Heavy Lumber": [],
    "Home Field Advantage": [],
    "Cover Athlete Cards": [],
    "All Aces": [{"name": "Gold", "print_run": 1}],
    "All Kings": [{"name": "Gold", "print_run": 1}],
    "1991 Topps Baseball": [
        {"name": "Pink", "print_run": None},
        {"name": "Crackleboard Foil", "print_run": None},
        {"name": "Koi Fish", "print_run": None},
        {"name": "Pink Crackleboard Foil", "print_run": None},
        {"name": "Blue", "print_run": 150},
        {"name": "Blue Crackleboard Foil", "print_run": 150},
        {"name": "Green", "print_run": 99},
        {"name": "Green Crackleboard Foil", "print_run": 99},
        {"name": "The Real One", "print_run": 91},
        {"name": "Gold", "print_run": 50},
        {"name": "Gold Crackleboard Foil", "print_run": 50},
        {"name": "Koi Fish Gold", "print_run": 50},
        {"name": "Orange", "print_run": 25},
        {"name": "Orange Crackleboard Foil", "print_run": 25},
        {"name": "Koi Fish Orange", "print_run": 25},
        {"name": "Black", "print_run": 10},
        {"name": "Black Crackleboard Foil", "print_run": 10},
        {"name": "Koi Fish Black", "print_run": 10},
        {"name": "Red", "print_run": 5},
        {"name": "Red Crackleboard Foil", "print_run": 5},
        {"name": "Koi Fish Red", "print_run": 5},
        {"name": "Foilfractor", "print_run": 1},
    ],
    "1991 Topps Baseball Chrome": [],
    "Stars Of MLB": PARALLELS_CRACKLEBOARD,
    "Titans Of The Game": PARALLELS_CRACKLEBOARD,
    "Oversized 2026 Topps Baseball": [],
    "Companion Cards": [],
    "Funko Base Cards": [],
    "75 Years Of Topps Gifts": [],
    "Fanatics Authentics Redemption Cards": [],
    "Through The Years Buyback Cards": [],
}

# ─────────────────────────────────────────────────────────────
# Section type flags
# ─────────────────────────────────────────────────────────────
BASE_TAG_SECTIONS = {"Base Set", "Base \u2013 Golden Mirror Variation"}
MULTI_PLAYER_SECTIONS = {"Major League Materials Dual Autographs", "Signature Tunes Dual Autograph"}
NO_TEAM_SECTIONS = {"75 Years Of Topps Autographs"}
CANADIAN_SECTION = "Base \u2013 Canadian Independence Day Variations"

# ─────────────────────────────────────────────────────────────
# Skip patterns
# ─────────────────────────────────────────────────────────────
SKIP_PATTERNS = [
    r"^shop for .+",          # "Shop for X on eBay" and bare "X on eBay" lines
    r".+\bon ebay$",          # e.g. "1991 Topps Baseball Chrome inserts on eBay"
    r"^all cards are /",
    r"^base versions are numbered",
    r"^hobby and jumbo",
    r"^hobby exclusive$",
    r"^retail exclusive$",
    r"^retail tin exclusive$",
    r"^super box exclusive$",
    r"^fanatics blaster exclusive$",
    r"^blue jays exclusive$",
]

def should_skip(line: str) -> bool:
    low = line.lower().strip()
    return any(re.match(p, low) for p in SKIP_PATTERNS)

# ─────────────────────────────────────────────────────────────
# Card line regex
# Handles: 41T, 75YA-AD, 91A-ABB, MLMA-AJ, FP-1, plain numbers
# ─────────────────────────────────────────────────────────────
CARD_LINE_RE = re.compile(
    r"^((?:\d+[A-Z][A-Z0-9]*|[A-Z][A-Z0-9]*)-[^\s]+|\d+[A-Z]|\d+)\s+(.+)"
)

def is_card_line(line: str) -> bool:
    return bool(CARD_LINE_RE.match(line.strip()))

# ─────────────────────────────────────────────────────────────
# Section boundary detection
# ─────────────────────────────────────────────────────────────
def next_nonempty(lines, start):
    i = start
    while i < len(lines) and not lines[i].strip():
        i += 1
    return i

def is_section_start(lines, idx):
    peek = next_nonempty(lines, idx + 1)
    if peek < len(lines) and re.match(r"^\d+ cards?\.?$", lines[peek].strip()):
        return True
    return False

# ─────────────────────────────────────────────────────────────
# Card line parsers
# ─────────────────────────────────────────────────────────────

def split_player_team(rest: str):
    """'PlayerName, Team' → (player, team). Splits on last ', '."""
    if ", " in rest:
        idx = rest.rfind(", ")
        return rest[:idx].strip(), rest[idx + 2:].strip()
    return rest.strip(), None


def parse_base_card_line(card_number: str, rest: str) -> list:
    """Parse base-set card lines with optional tags (RC, Future Stars, etc.)."""
    rest = rest.strip()
    is_rookie = False
    subset = None

    # Check for trailing parenthetical tag
    m_tag = re.search(r"\(([^)]+)\)\s*$", rest)
    tag = m_tag.group(1).strip() if m_tag else None
    if m_tag:
        rest = rest[: m_tag.start()].strip()

    # RC without parens: "PlayerName, Team RC"
    if rest.endswith(" RC"):
        is_rookie = True
        rest = rest[:-3].strip()

    if tag == "League Leaders":
        player, team = split_player_team(rest)
        return [{"card_number": card_number, "player": player, "team": team,
                 "is_rookie": False, "subset": "League Leaders"}]

    if tag == "Future Stars":
        player, team = split_player_team(rest)
        return [{"card_number": card_number, "player": player, "team": team,
                 "is_rookie": is_rookie, "subset": "Future Stars"}]

    if tag == "Combo Card/Checklist":
        player, team = split_player_team(rest)
        return [{"card_number": card_number, "player": player, "team": team,
                 "is_rookie": False, "subset": "Combo Card/Checklist"}]

    if tag == "Team Card":
        _, team = split_player_team(rest)
        return [{"card_number": card_number, "player": "Team Card", "team": team,
                 "is_rookie": False, "subset": None}]

    player, team = split_player_team(rest)
    return [{"card_number": card_number, "player": player, "team": team,
             "is_rookie": is_rookie, "subset": None}]


def parse_standard_card_line(card_number: str, rest: str,
                              team_override=None, force_no_team=False) -> list:
    """Standard card line (no base-set tags), strip inline /N."""
    rest = rest.strip()

    # Strip inline /N suffix (Canadian /67, ITN /1)
    rest = re.sub(r"\s*/\d+\s*$", "", rest).strip()

    # RC tag in variations
    is_rookie = False
    if rest.endswith(" RC"):
        is_rookie = True
        rest = rest[:-3].strip()

    # Team Card tag in variations
    m_tag = re.search(r"\(([^)]+)\)\s*$", rest)
    if m_tag:
        tag = m_tag.group(1)
        rest = rest[: m_tag.start()].strip()
        if tag == "Team Card":
            _, team = split_player_team(rest)
            return [{"card_number": card_number, "player": "Team Card",
                     "team": team_override or team, "is_rookie": False, "subset": None}]

    player, team = split_player_team(rest)
    if team_override:
        team = team_override
    if force_no_team:
        team = None
    return [{"card_number": card_number, "player": player, "team": team,
             "is_rookie": is_rookie, "subset": None}]


def parse_multi_player_card_line(card_number: str, rest: str, section_name: str) -> list:
    """Parse multi-player lines (MLMDA, Signature Tunes)."""
    rest = rest.strip()

    if "/" not in rest:
        player, team = split_player_team(rest)
        return [{"card_number": card_number, "player": player, "team": team,
                 "is_rookie": False, "subset": None}]

    slash_idx = rest.index("/")
    player1_raw = rest[:slash_idx].strip()
    remainder = rest[slash_idx + 1:].strip()
    player2, team2 = split_player_team(remainder)

    if section_name == "Signature Tunes Dual Autograph":
        # Harper gets team (Philadelphia Phillies from card), Moby gets null
        player1_name, team1 = split_player_team(player1_raw)
        if not team1:
            team1 = team2
        return [
            {"card_number": card_number, "player": player1_name, "team": team1,
             "is_rookie": False, "subset": None},
            {"card_number": card_number, "player": player2, "team": None,
             "is_rookie": False, "subset": None},
        ]

    # MLMDA: both players get the same team
    player1_name, team1 = split_player_team(player1_raw)
    if not team1:
        team1 = team2
    return [
        {"card_number": card_number, "player": player1_name, "team": team1,
         "is_rookie": False, "subset": None},
        {"card_number": card_number, "player": player2, "team": team2,
         "is_rookie": False, "subset": None},
    ]

# ─────────────────────────────────────────────────────────────
# Special section parsers
# ─────────────────────────────────────────────────────────────

BUYBACK_RE = re.compile(
    r"^(\d{4})\s+[Tt][a-z]*\s+(.+?)\s+Card\s+#(\w+)(?:\s+\(Graded\))?,\s+(.+)$"
)

def parse_buyback_line(raw_line: str, card_num: int):
    line = raw_line.strip()
    if not line:
        return None
    m = BUYBACK_RE.match(line)
    if m:
        player_raw = m.group(2).strip()
        card_number = m.group(3)
        team = m.group(4).strip()
        # Clean "No Name" annotation
        player_raw = re.sub(r"\bNo Name\b", "", player_raw).strip()
        return {"card_number": card_number, "player": player_raw,
                "team": team, "is_rookie": False, "subset": None}
    return {"card_number": f"BUYBACK-{card_num}", "player": "Redemption",
            "team": None, "is_rookie": False, "subset": None}

def parse_fanatics_line(raw_line: str, card_num: int):
    line = raw_line.strip()
    if not line:
        return None
    player, team = split_player_team(line)
    return {"card_number": f"FA-{card_num}", "player": player,
            "team": team, "is_rookie": False, "subset": None}

def parse_gifts_line(raw_line: str, card_num: int):
    line = raw_line.strip()
    if not line:
        return None
    return {"card_number": f"GIFT-{card_num}", "player": "Redemption",
            "team": None, "is_rookie": False, "subset": None}

# ─────────────────────────────────────────────────────────────
# Main checklist parser
# ─────────────────────────────────────────────────────────────

# Known section names (used as boundaries even without "N cards" header)
_KNOWN_SECTION_NAMES = set(SECTION_PARALLELS.keys())

def is_boundary(lines, idx):
    """True if this line starts a new section."""
    line = lines[idx].strip()
    if line in _KNOWN_SECTION_NAMES:
        return True
    peek = next_nonempty(lines, idx + 1)
    if peek < len(lines) and re.match(r"^\d+ cards?\.?$", lines[peek].strip()):
        return True
    return False


def _collect_section_lines(lines, start_idx, n):
    """Collect all non-empty, non-skip lines for a section until next boundary.

    Handles the "Parallels" block: lines between a "Parallels" / "Parallel"
    header and the first card line (identified by having ", " in it) are
    skipped to avoid parallel annotations like "75 Years of Topps /75"
    being mis-parsed as card entries.

    Returns (list_of_lines, next_idx).
    """
    raw = []
    idx = start_idx
    in_parallels = False

    while idx < n:
        ln = lines[idx].strip()
        if not ln:
            idx += 1; continue
        if is_boundary(lines, idx):
            break
        idx += 1

        low = ln.lower()

        # "Parallels" / "Parallel" header → enter parallel block
        if low in ("parallels", "parallel"):
            in_parallels = True
            continue

        if should_skip(ln):
            continue

        if in_parallels:
            # Exit parallel block on the first real card line.
            # Real card lines are identified by either:
            #   (a) a hyphenated card code (e.g. 75YTA-AN, FP-1, MLMA-AJ), or
            #   (b) a plain number + ", " (player, Team format like "1 Aaron Judge, NYY")
            # Parallel annotation lines look like "75 Years of Topps /75" — plain
            # number prefix, no comma — and are skipped.
            m = CARD_LINE_RE.match(ln)
            if m:
                card_number = m.group(1)
                rest = m.group(2)
                is_real_card = ("-" in card_number) or (", " in rest)
                if is_real_card:
                    in_parallels = False
                    raw.append(ln)
            # else: parallel annotation or non-card line, skip
        else:
            raw.append(ln)

    return raw, idx


def _parse_section_cards(section_name: str, raw_lines: list) -> list:
    """Dispatch to the appropriate card-line parser for a section."""
    cards = []

    if section_name == "75 Years Of Topps Gifts":
        for i, ln in enumerate(raw_lines, 1):
            c = parse_gifts_line(ln, i)
            if c: cards.append(c)

    elif section_name == "Fanatics Authentics Redemption Cards":
        for i, ln in enumerate(raw_lines, 1):
            c = parse_fanatics_line(ln, i)
            if c: cards.append(c)

    elif section_name == "Through The Years Buyback Cards":
        for i, ln in enumerate(raw_lines, 1):
            c = parse_buyback_line(ln, i)
            if c: cards.append(c)

    else:
        for ln in raw_lines:
            if not is_card_line(ln):
                continue
            m = CARD_LINE_RE.match(ln)
            if not m:
                continue
            card_number = m.group(1)
            rest = m.group(2).strip()

            if section_name in BASE_TAG_SECTIONS:
                new_cards = parse_base_card_line(card_number, rest)
            elif section_name in MULTI_PLAYER_SECTIONS:
                new_cards = parse_multi_player_card_line(card_number, rest, section_name)
            elif section_name == CANADIAN_SECTION:
                new_cards = parse_standard_card_line(
                    card_number, rest, team_override="Toronto Blue Jays")
            elif section_name in NO_TEAM_SECTIONS:
                new_cards = parse_standard_card_line(
                    card_number, rest, force_no_team=True)
            else:
                new_cards = parse_standard_card_line(card_number, rest)

            cards.extend(new_cards)

    return cards


def parse_checklist(text: str) -> list:
    lines = text.split("\n")
    sections = []
    idx = 0
    n = len(lines)

    while idx < n:
        line = lines[idx].strip()
        if not line:
            idx += 1
            continue

        if not is_boundary(lines, idx):
            idx += 1
            continue

        section_name = line
        parallels = SECTION_PARALLELS.get(section_name, [])
        idx += 1  # advance past section name

        # Skip "N cards" line if present
        peek = next_nonempty(lines, idx)
        if peek < n and re.match(r"^\d+ cards?\.?$", lines[peek].strip()):
            idx = peek + 1

        # Collect all content lines for this section
        raw_lines, idx = _collect_section_lines(lines, idx, n)

        # Parse cards
        cards = _parse_section_cards(section_name, raw_lines)

        # First Pitch Autographs: base is /99
        if section_name == "First Pitch Autographs":
            parallels = [{"name": "Base", "print_run": 99}] + parallels

        sections.append({"insert_set": section_name,
                         "parallels": parallels, "cards": cards})

    return sections

# ─────────────────────────────────────────────────────────────
# Stats
# ─────────────────────────────────────────────────────────────

def compute_stats(appearances: list) -> dict:
    unique_cards = 0
    total_print_run = 0
    one_of_ones = 0
    for app in appearances:
        unique_cards += 1
        for p in app["parallels"]:
            unique_cards += 1
            if p["print_run"] and p["print_run"] > 0:
                total_print_run += p["print_run"]
                if p["print_run"] == 1:
                    one_of_ones += 1
    return {
        "unique_cards": unique_cards,
        "total_print_run": total_print_run,
        "one_of_ones": one_of_ones,
        "insert_sets": len(appearances),
    }

# ─────────────────────────────────────────────────────────────
# Build output
# ─────────────────────────────────────────────────────────────

def build_output(sections: list) -> dict:
    # Collect all players who are rookies in any section (propagate to all appearances)
    rc_players = set()
    for section in sections:
        for card in section["cards"]:
            if card.get("is_rookie"):
                rc_players.add(card["player"])

    player_index: dict = {}

    for section in sections:
        for card in section["cards"]:
            pname = card["player"]
            if pname not in player_index:
                player_index[pname] = {"player": pname, "appearances": []}
            player_index[pname]["appearances"].append({
                "insert_set": section["insert_set"],
                "card_number": card["card_number"],
                "team": card["team"],
                "is_rookie": card["player"] in rc_players,
                "subset_tag": card["subset"],
                "parallels": section["parallels"],
            })

    players = []
    for pname in sorted(player_index.keys()):
        data = player_index[pname]
        players.append({
            "player": pname,
            "appearances": data["appearances"],
            "stats": compute_stats(data["appearances"]),
        })

    return {
        "set_name": "2026 Topps Series 1 Baseball",
        "sport": "Baseball",
        "season": "2026",
        "league": "MLB",
        "sections": sections,
        "players": players,
    }

# ─────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Parsing 2026 Topps Series 1 Baseball checklist...")

    sections = parse_checklist(CHECKLIST)
    output = build_output(sections)

    out_path = "topps_series1_2026_parsed.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nSet: {output['set_name']} ({output['season']})")
    print(f"Sections: {len(output['sections'])}")
    for s in output["sections"]:
        print(f"  {s['insert_set']:<55} {len(s['cards']):>4} cards  {len(s['parallels']):>2} parallels")

    print(f"\nTotal players: {len(output['players'])}")

    player_map = {p["player"]: p for p in output["players"]}

    print("\n=== Spot checks ===")
    for name in ["Aaron Judge", "Paul Skenes", "Shohei Ohtani"]:
        if name in player_map:
            st = player_map[name]["stats"]
            print(f"  {name}: {st['insert_sets']} appearances, "
                  f"{st['unique_cards']} unique cards, {st['one_of_ones']} 1/1s")

    print("\n=== League Leaders card #11 ===")
    base_sec = next((s for s in sections if s["insert_set"] == "Base Set"), None)
    if base_sec:
        ll11 = [c for c in base_sec["cards"] if c["card_number"] == "11"]
        print(f"  Players: {[c['player'] for c in ll11]}")
        print(f"  Subsets: {[c['subset'] for c in ll11]}")

    print("\n=== MLMDA dual autos ===")
    mlmda = next((s for s in sections if s["insert_set"] == "Major League Materials Dual Autographs"), None)
    if mlmda:
        from collections import Counter
        nums = list(dict.fromkeys(c["card_number"] for c in mlmda["cards"]))
        for cn in nums:
            pls = [c["player"] for c in mlmda["cards"] if c["card_number"] == cn]
            print(f"  {cn}: {pls}")

    print("\n=== Signature Tunes ===")
    st_sec = next((s for s in sections if s["insert_set"] == "Signature Tunes Dual Autograph"), None)
    if st_sec:
        for c in st_sec["cards"]:
            print(f"  {c['card_number']} {c['player']} (team={c['team']})")

    print("\n=== Through The Years Buyback (first 5) ===")
    tty = next((s for s in sections if s["insert_set"] == "Through The Years Buyback Cards"), None)
    if tty:
        for c in tty["cards"][:5]:
            print(f"  #{c['card_number']} {c['player']} ({c['team']})")

    print("\n=== 75 Years Of Topps Gifts ===")
    gifts = next((s for s in sections if s["insert_set"] == "75 Years Of Topps Gifts"), None)
    if gifts:
        print(f"  {len(gifts['cards'])} entries, all player='Redemption': "
              f"{all(c['player'] == 'Redemption' for c in gifts['cards'])}")
