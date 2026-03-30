import json
import re
import os

# ─────────────────────────────────────────────────────────────
# Parallel blocks
# ─────────────────────────────────────────────────────────────

BASE_PARALLELS = [
    # Hobby base
    {"name": "Rainbow Foilboard", "print_run": None},
    {"name": "Gold", "print_run": 2025},
    {"name": "Purple Rainbow", "print_run": 250},
    {"name": "Blue Rainbow", "print_run": 150},
    {"name": "Green Rainbow", "print_run": 99},
    {"name": "Black", "print_run": 68},
    {"name": "Gold Rainbow", "print_run": 50},
    {"name": "Orange Rainbow", "print_run": 25},
    {"name": "Wood", "print_run": 25},
    {"name": "Black Rainbow", "print_run": 10},
    {"name": "Clear", "print_run": 10},
    {"name": "Red Rainbow", "print_run": 5},
    {"name": "FoilFractor", "print_run": 1},
    {"name": "First Card", "print_run": 1},
    # Hobby SSP
    {"name": "Victory", "print_run": None},
    # Jumbo SSP
    {"name": "Sandglitter", "print_run": None},
    {"name": "Blue Sandglitter", "print_run": None},
    # Retail
    {"name": "Holo Foil", "print_run": None},
    {"name": "Purple Holo Foil", "print_run": 250},
    {"name": "Blue Holo Foil", "print_run": 150},
    {"name": "Green Holo Foil", "print_run": 99},
    {"name": "Gold Holo Foil", "print_run": 50},
    {"name": "Orange Holo Foil", "print_run": 25},
    {"name": "Black Holo Foil", "print_run": 10},
    {"name": "Red Holo Foil", "print_run": 5},
    {"name": "Platinum Holo Foil", "print_run": 1},
]

# Marks of Excellence / Contemporary Marks / Havoc Marks
_ME_CM_HM = [
    {"name": "Rainbow Foilboard", "print_run": None},
    {"name": "Green Rainbow", "print_run": 99},
    {"name": "Gold Rainbow", "print_run": 50},
    {"name": "Orange Rainbow", "print_run": 25},
    {"name": "Black Rainbow", "print_run": 10},
    {"name": "Red Rainbow", "print_run": 5},
    {"name": "FoilFractor", "print_run": 1},
]

# Rookie Photo Shoot Autographs / Dual Autographs
_RP = [
    {"name": "Red", "print_run": 5},
    {"name": "Platinum", "print_run": 1},
]

# The Daily Dribble / New School / Levitation
_DRIBBLE = [
    {"name": "Green Rainbow", "print_run": 99},
    {"name": "Gold Rainbow", "print_run": 50},
    {"name": "Orange Rainbow", "print_run": 25},
    {"name": "Black Rainbow", "print_run": 10},
    {"name": "Red Rainbow", "print_run": 5},
    {"name": "FoilFractor", "print_run": 1},
]

# No Limit / Stars of the NBA / Rise to Stardom / MVP Vault
_NO_LIMIT = [
    {"name": "Rainbow Foilboard", "print_run": None},
    {"name": "Purple Rainbow", "print_run": 250},
    {"name": "Blue Rainbow", "print_run": 150},
    {"name": "Green Rainbow", "print_run": 99},
    {"name": "Gold Rainbow", "print_run": 50},
    {"name": "Orange Rainbow", "print_run": 25},
    {"name": "Black Rainbow", "print_run": 10},
    {"name": "Red Rainbow", "print_run": 5},
    {"name": "FoilFractor", "print_run": 1},
]

# 1980-81 Topps Basketball insert
_80BK = [
    {"name": "Pink", "print_run": None},
    {"name": "Green", "print_run": 99},
    {"name": "Gold", "print_run": 50},
    {"name": "Orange", "print_run": 25},
    {"name": "Black", "print_run": 10},
    {"name": "Red", "print_run": 5},
    {"name": "Platinum", "print_run": 1},
]

# Class of '25
_C25 = [
    {"name": "Red", "print_run": 5},
    {"name": "FoilFractor", "print_run": 1},
]

# Rise to the Occasion Relics / Own The Game / Rookie Roundball Remnants
_RELICS_RAINBOW = [
    {"name": "Rainbow Foilboard", "print_run": None},
    {"name": "Green Rainbow", "print_run": 99},
    {"name": "Gold Rainbow", "print_run": 50},
    {"name": "Orange Rainbow", "print_run": 25},
    {"name": "Black Rainbow", "print_run": 10},
    {"name": "Red Rainbow", "print_run": 5},
    {"name": "FoilFractor", "print_run": 1},
]

# Flagship Real One Relics
_FRO_RELICS = [
    {"name": "Gold", "print_run": 50},
    {"name": "Orange", "print_run": 25},
    {"name": "Black", "print_run": 10},
    {"name": "Red", "print_run": 5},
    {"name": "FoilFractor", "print_run": 1},
]

# Map section name → parallel list (sections absent from this dict get [])
SECTION_PARALLELS: dict = {
    # Base
    "Base Set": BASE_PARALLELS,
    "Combo Cards": BASE_PARALLELS,
    # Autograph sets
    "Marks of Excellence": _ME_CM_HM,
    "Contemporary Marks": _ME_CM_HM,
    "Havoc Marks": _ME_CM_HM,
    "Rookie Photo Shoot Autographs": _RP,
    "Rookie Photo Shoot Dual Autographs": _RP,
    # Insert sets
    "The Daily Dribble": _DRIBBLE,
    "New School": _DRIBBLE,
    "Levitation": _DRIBBLE,
    "No Limit": _NO_LIMIT,
    "Stars of the NBA": _NO_LIMIT,
    "Rise to Stardom": _NO_LIMIT,
    "MVP Vault": _NO_LIMIT,
    "1980-81 Topps Basketball": _80BK,
    "Class of '25": _C25,
    # Relic sets
    "Rise to the Occasion Relics": _RELICS_RAINBOW,
    "Own The Game": _RELICS_RAINBOW,
    "Rookie Roundball Remnants": _RELICS_RAINBOW,
    "Flagship Real One Relics": _FRO_RELICS,
    # Variation sets (section IS the variant; Clear Variation carries its own print run)
    "Golden Mirror Image Variations": [],
    "Team Color Border Variation": [],
    "Clear Variation": [{"name": "Clear Variation", "print_run": 10}],
}

# ─────────────────────────────────────────────────────────────
# Section-level config
# ─────────────────────────────────────────────────────────────

MULTI_PLAYER_SECTIONS = {
    "1980-81 Topps Basketball Triple Autographs",
    "Rookie Photo Shoot Dual Autographs",
}

SECTION_ROOKIE_OVERRIDE = {
    "Contemporary Marks",
    "New Applicants Autographs",
    "Rookie Photo Shoot Autographs",
    "1980-81 Topps Rookie Autographs",
    "Flagship Real Ones Rookie Autographs",
    "1980-81 Topps Chrome Rookie Autographs",
    "Shopping Spree Signatures",
    "Rise to the Occasion Relics",
    "Rookie Roundball Remnants",
    "Franchise Fabrics",
    "New School",
    "Rise to Stardom",
    "Generation Now",
    "Clutch City Prospects",
    "Class of '25",
    "1980-81 Topps Basketball Triple Autographs",
    "Rookie Photo Shoot Dual Autographs",
}

# Variation insert sets that mirror all 300 base cards
VARIATION_SECTIONS = [
    "Golden Mirror Image Variations",
    "Team Color Border Variation",
    "Clear Variation",
]

# ─────────────────────────────────────────────────────────────
# Regexes
# ─────────────────────────────────────────────────────────────

SECTION_HEADER_RE = re.compile(
    r'^(.+?)\s*\((?:\d+\s+cards?|cards\s+\d+)', re.IGNORECASE
)
MULTI_CARD_RE = re.compile(
    r'^([A-Za-z0-9][A-Za-z0-9]*(?:-[A-Za-z0-9]+)*):\s+(.+)$'
)
CARD_LINE_RE = re.compile(
    r'^((?:[A-Za-z0-9]+-[A-Za-z0-9]+|\d+))\s+(.+)$'
)

SKIP_PREFIXES = (
    "base set parallels",
    "unnumbered:",
    "serialized:",
    "autograph sets",
    "memorabilia sets",
    "insert sets",
    "general rules",
    "strip rc",
    "all insert sets",
    "no pack",
    "do not seed",
    "here's",
    "add a new set",
    "1. parser",
    "set sample_image",
)


def should_skip(line: str) -> bool:
    low = line.lower().strip()
    return any(low.startswith(p) for p in SKIP_PREFIXES)


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def extract_section_name(line: str) -> str:
    m = SECTION_HEADER_RE.match(line)
    return m.group(1).strip() if m else line.rstrip(":").strip()


def section_is_all_rookie(line: str, name: str) -> bool:
    return "all is_rookie: true" in line.lower() or name in SECTION_ROOKIE_OVERRIDE


def parse_card_rest(rest: str, force_rookie: bool) -> tuple:
    rest = rest.strip()
    is_rookie = force_rookie
    if rest.endswith(" RC"):
        is_rookie = True
        rest = rest[:-3].strip()
    if "," in rest:
        last_comma = rest.rfind(",")
        player = rest[:last_comma].strip()
        team = rest[last_comma + 1:].strip()
    else:
        player = rest
        team = ""
    return player, team, is_rookie


# ─────────────────────────────────────────────────────────────
# Main parser
# ─────────────────────────────────────────────────────────────

def parse_checklist(text: str) -> list:
    lines = text.split("\n")
    sections = []
    current_name = None
    current_all_rookie = False
    current_multi = False
    current_cards: list = []

    def flush():
        nonlocal current_name, current_cards, current_all_rookie, current_multi
        if current_name and current_cards:
            parallels = SECTION_PARALLELS.get(current_name, [])
            sections.append({
                "insert_set": current_name,
                "parallels": list(parallels),
                "cards": current_cards,
            })
        current_name = None
        current_cards = []
        current_all_rookie = False
        current_multi = False

    for line in lines:
        stripped = line.strip()
        if not stripped or should_skip(stripped):
            continue

        if SECTION_HEADER_RE.match(stripped):
            flush()
            current_name = extract_section_name(stripped)
            current_all_rookie = section_is_all_rookie(stripped, current_name)
            current_multi = current_name in MULTI_PLAYER_SECTIONS
            continue

        if current_name is None:
            continue

        if current_multi:
            m = MULTI_CARD_RE.match(stripped)
            if m:
                card_number = m.group(1)
                content = m.group(2).strip()
                parts = (
                    [p.strip() for p in content.split(" / ")]
                    if " / " in content
                    else [p.strip() for p in content.split(", ")]
                )
                for part in parts:
                    current_cards.append({
                        "card_number": card_number,
                        "player": part,
                        "team": "",
                        "is_rookie": True,
                        "subset": None,
                    })
            continue

        m = CARD_LINE_RE.match(stripped)
        if m:
            player, team, is_rookie = parse_card_rest(m.group(2), current_all_rookie)
            current_cards.append({
                "card_number": m.group(1),
                "player": player,
                "team": team,
                "is_rookie": is_rookie,
                "subset": None,
            })

    flush()
    return sections


# ─────────────────────────────────────────────────────────────
# Variation sections (mirrors all 300 base cards)
# ─────────────────────────────────────────────────────────────

def apply_variation_sections(sections: list) -> list:
    """Append Golden Mirror Image Variations, Team Color Border Variation,
    and Clear Variation — each containing all 300 base cards."""
    base_cards = []
    for s in sections:
        if s["insert_set"] in ("Base Set", "Combo Cards"):
            base_cards.extend(s["cards"])

    for name in VARIATION_SECTIONS:
        sections.append({
            "insert_set": name,
            "parallels": list(SECTION_PARALLELS.get(name, [])),
            "cards": [dict(c) for c in base_cards],
        })
    return sections


# ─────────────────────────────────────────────────────────────
# Build output
# ─────────────────────────────────────────────────────────────

def build_output(sections: list) -> dict:
    # Collect all known RC players
    rc_players: set = set()
    for section in sections:
        for card in section["cards"]:
            if card["is_rookie"]:
                rc_players.add(card["player"])

    # Build player → first-seen team
    player_teams: dict = {}
    for section in sections:
        for card in section["cards"]:
            p = card["player"]
            if card["team"] and p not in player_teams:
                player_teams[p] = card["team"]

    # Propagate is_rookie + fill missing teams
    for section in sections:
        for card in section["cards"]:
            if card["player"] in rc_players:
                card["is_rookie"] = True
            if not card["team"] and card["player"] in player_teams:
                card["team"] = player_teams[card["player"]]

    # Index players
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
                "is_rookie": card["is_rookie"],
                "subset_tag": card["subset"],
                "parallels": section["parallels"],
            })

    players = [
        {
            "player": pname,
            "appearances": data["appearances"],
            "stats": compute_stats(data["appearances"]),
        }
        for pname, data in sorted(player_index.items())
    ]

    return {
        "set_name": "2025-26 Topps Basketball",
        "sport": "Basketball",
        "season": "2025-26",
        "league": "NBA",
        "sections": sections,
        "players": players,
    }


def compute_stats(appearances: list) -> dict:
    unique_cards = total_print_run = one_of_ones = 0
    for app in appearances:
        unique_cards += 1
        for p in app["parallels"]:
            unique_cards += 1
            if p["print_run"]:
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
# Entry point
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    checklist_path = os.path.join(os.path.dirname(__file__), "nba_topps_2526_checklist.txt")
    with open(checklist_path, encoding="utf-8") as f:
        checklist_text = f.read()

    sections = parse_checklist(checklist_text)
    apply_variation_sections(sections)
    output = build_output(sections)

    out_path = os.path.join(os.path.dirname(__file__), "..", "nba_topps_2526_parsed.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Set: {output['set_name']} ({output['season']})")
    print(f"Sections: {len(output['sections'])}")
    for s in output["sections"]:
        print(f"  {s['insert_set']}: {len(s['cards'])} cards, {len(s['parallels'])} parallels")
    print(f"\nTotal players: {len(output['players'])}")

    player_map = {p["player"]: p for p in output["players"]}
    for name in ["Cooper Flagg", "LeBron James", "Jayson Tatum"]:
        if name in player_map:
            p = player_map[name]
            st = p["stats"]
            print(f"\n=== {name} ===")
            print(f"  Insert sets: {st['insert_sets']} | Unique cards: {st['unique_cards']} | "
                  f"Total print run: {st['total_print_run']} | 1/1s: {st['one_of_ones']}")
