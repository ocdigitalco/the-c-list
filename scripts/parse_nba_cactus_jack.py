#!/usr/bin/env python3
"""Parser for 2025-26 Topps Chrome Cactus Jack X NBA All-Star Game Basketball."""

import json
import re

# ─────────────────────────────────────────────────────────────
# Parallel definitions
# ─────────────────────────────────────────────────────────────

PARALLELS_BASE = [
    {"name": "Orange Refractor", "print_run": 50},
    {"name": "Laser Refractor",  "print_run": 25},
    {"name": "Black Refractor",  "print_run": 10},
    {"name": "Red Refractor",    "print_run": 5},
    {"name": "Superfractor",     "print_run": 1},
]

# All-Star Game Autographs: base is /25, parallels are rarer numbered versions
PARALLELS_AUTO = [
    {"name": "Base",             "print_run": 25},
    {"name": "Black Refractor",  "print_run": 10},
    {"name": "Red Refractor",    "print_run": 5},
    {"name": "Superfractor",     "print_run": 1},
]

# ─────────────────────────────────────────────────────────────
# Embedded checklists
# ─────────────────────────────────────────────────────────────

# Format: CARD_NUM PLAYER_NAME - TEAM [RC]
BASE_TEXT = """
1 Stephon Castle - San Antonio Spurs
2 Victor Wembanyama - San Antonio Spurs
3 Dejounte Murray - New Orleans Pelicans
4 Ja Morant - Memphis Grizzlies
5 Jaren Jackson Jr. - Memphis Grizzlies
6 Amen Thompson - Houston Rockets
7 Reed Sheppard - Houston Rockets
8 Kyrie Irving - Dallas Mavericks
9 Anthony Davis - Dallas Mavericks
10 Domantas Sabonis - Sacramento Kings
11 Zach LaVine - Sacramento Kings
12 Devin Booker - Phoenix Suns
13 Kevin Durant - Houston Rockets
14 LeBron James - Los Angeles Lakers
15 Luka Dončić - Los Angeles Lakers
16 Kawhi Leonard - Los Angeles Clippers
17 James Harden - Los Angeles Clippers
18 Stephen Curry - Golden State Warriors
19 Jimmy Butler III - Golden State Warriors
20 Lauri Markkanen - Utah Jazz
21 Isaiah Collier - Utah Jazz
22 Toumani Camara - Portland Trail Blazers
23 Scoot Henderson - Portland Trail Blazers
24 Shai Gilgeous-Alexander - Oklahoma City Thunder
25 Jalen Williams - Oklahoma City Thunder
26 Anthony Edwards - Minnesota Timberwolves
27 Naz Reid - Minnesota Timberwolves
28 Nikola Jokić - Denver Nuggets
29 Jamal Murray - Denver Nuggets
30 Bilal Coulibaly - Washington Wizards
31 Alex Sarr - Washington Wizards
32 Paolo Banchero - Orlando Magic
33 Franz Wagner - Orlando Magic
34 Donovan Mitchell - Cleveland Cavaliers
35 Darius Garland - Cleveland Cavaliers
36 Evan Mobley - Cleveland Cavaliers
37 Tyler Herro - Miami Heat
38 Bam Adebayo - Miami Heat
39 LaMelo Ball - Charlotte Hornets
40 Brandon Miller - Charlotte Hornets
41 Jalen Johnson - Atlanta Hawks
42 Trae Young - Atlanta Hawks
43 Giannis Antetokounmpo - Milwaukee Bucks
44 Damian Lillard - Milwaukee Bucks
45 Tyrese Haliburton - Indiana Pacers
46 Andrew Nembhard - Indiana Pacers
47 Cade Cunningham - Detroit Pistons
48 Jaden Ivey - Detroit Pistons
49 Coby White - Chicago Bulls
50 Josh Giddey - Chicago Bulls
51 Gradey Dick - Toronto Raptors
52 Scottie Barnes - Toronto Raptors
53 Tyrese Maxey - Philadelphia 76ers
54 Joel Embiid - Philadelphia 76ers
55 Jalen Brunson - New York Knicks
56 OG Anunoby - New York Knicks
57 Jayson Tatum - Boston Celtics
58 Jaylen Brown - Boston Celtics
59 Cam Thomas - Brooklyn Nets
60 Derrick White - Boston Celtics
61 Cooper Flagg - Dallas Mavericks RC
62 Dylan Harper - San Antonio Spurs RC
63 VJ Edgecombe - Philadelphia 76ers RC
64 Kon Knueppel - Charlotte Hornets RC
65 Ace Bailey - Utah Jazz RC
66 Tre Johnson III - Washington Wizards RC
67 Jeremiah Fears - New Orleans Pelicans RC
68 Egor Dëmin - Brooklyn Nets RC
69 Collin Murray-Boyles - Toronto Raptors RC
70 Khaman Maluach - Phoenix Suns RC
71 Cedric Coward - Memphis Grizzlies RC
72 Noa Essengue - Chicago Bulls RC
73 Derik Queen - New Orleans Pelicans RC
74 Carter Bryant - San Antonio Spurs RC
75 Thomas Sorber - Oklahoma City Thunder RC
76 Yang Hansen - Portland Trail Blazers RC
77 Joan Beringer - Minnesota Timberwolves RC
78 Walter Clayton Jr. - Utah Jazz RC
79 Nolan Traore - Brooklyn Nets RC
80 Kasparas Jakučionis - Miami Heat RC
81 Will Riley - Washington Wizards RC
82 Drake Powell - Brooklyn Nets RC
83 Asa Newell - Atlanta Hawks RC
84 Nique Clifford - Sacramento Kings RC
85 Jase Richardson - Orlando Magic RC
86 Ben Saraf - Brooklyn Nets RC
87 Danny Wolf - Brooklyn Nets RC
88 Hugo González - Boston Celtics RC
89 Liam McNeeley - Charlotte Hornets RC
90 Yanic Konan-Niederhäuser - Los Angeles Clippers RC
91 Micah Peavy - New Orleans Pelicans RC
92 Koby Brea - Phoenix Suns RC
93 Maxime Raynaud - Sacramento Kings RC
94 Jamir Watkins - Washington Wizards RC
95 Brooks Barnhizer - Oklahoma City Thunder RC
96 Naji Marshall - Dallas Mavericks
97 Ochai Agbaji - Toronto Raptors
98 Jaden McDaniels - Minnesota Timberwolves
99 GG Jackson II - Memphis Grizzlies
100 Tyrese Proctor - Cleveland Cavaliers RC
"""

# Format: CARD_CODE PLAYER_NAME - TEAM
AUTO_TEXT = """
ASGV-AB Ace Bailey - Utah Jazz
ASGV-AI Allen Iverson - Philadelphia 76ers
ASGV-BM Brandon Miller - Charlotte Hornets
ASGV-CF Cooper Flagg - Dallas Mavericks
ASGV-DH Dylan Harper - San Antonio Spurs
ASGV-GA Giannis Antetokounmpo - Milwaukee Bucks
ASGV-JB Jalen Brunson - New York Knicks
ASGV-JG Jalen Green - Phoenix Suns
ASGV-JT Jayson Tatum - Boston Celtics
ASGV-KD Kevin Durant - Houston Rockets
ASGV-KG Kevin Garnett - Minnesota Timberwolves
ASGV-KK Kon Knueppel - Charlotte Hornets
ASGV-KM Khaman Maluach - Phoenix Suns
ASGV-NJ Nikola Jokić - Denver Nuggets
ASGV-SC Stephen Curry - Golden State Warriors
ASGV-SGA Shai Gilgeous-Alexander - Oklahoma City Thunder
ASGV-TH Tyrese Haliburton - Indiana Pacers
ASGV-TM Tracy McGrady - Orlando Magic
ASGV-VC Vince Carter - Toronto Raptors
ASGV-VW Victor Wembanyama - San Antonio Spurs
"""

# Format: CARD_CODE PLAYER_NAME - TEAM
SICKO_TEXT = """
SS-1 LeBron James - Cleveland Cavaliers
SS-2 Zach LaVine - Minnesota Timberwolves
SS-3 Aaron Gordon - Orlando Magic
SS-4 Allen Iverson - Philadelphia 76ers
SS-5 Vince Carter - Toronto Raptors
SS-6 Jaylen Brown - Boston Celtics
SS-7 Larry Bird - Boston Celtics
SS-8 Stephen Curry - Golden State Warriors
SS-9 Dwight Howard - Orlando Magic
SS-10 Dominique Wilkins - Atlanta Hawks
SS-11 Donovan Mitchell - Cleveland Cavaliers
SS-12 Damian Lillard - Milwaukee Bucks
SS-13 Kevin Durant - Oklahoma City Thunder
SS-14 Dwyane Wade - Miami Heat
SS-15 Magic Johnson - Los Angeles Lakers
SS-16 Victor Wembanyama - San Antonio Spurs
SS-17 Devin Booker - Phoenix Suns
SS-18 Shaquille O'Neal - Phoenix Suns
SS-19 Giannis Antetokounmpo - Milwaukee Bucks
SS-20 Kyrie Irving - Cleveland Cavaliers
SS-21 Carmelo Anthony - Denver Nuggets
SS-22 Jason Richardson - Golden State Warriors
SS-23 Isiah Thomas - Detroit Pistons
SS-24 Russell Westbrook - Oklahoma City Thunder
SS-25 Jason Williams - Sacramento Kings
"""

# ─────────────────────────────────────────────────────────────
# Parser
# ─────────────────────────────────────────────────────────────

# Matches: CARD_NUM_OR_CODE  PLAYER_NAME - TEAM [RC]
CARD_LINE_RE = re.compile(r'^(\d+|[A-Z][A-Z0-9]*-[A-Z0-9]+)\s+(.+)$')


def parse_card_line(line: str, allow_rc: bool = False):
    """Parse a single card line. Returns (card_number, player, team, is_rookie) or None."""
    line = line.strip()
    if not line:
        return None
    m = CARD_LINE_RE.match(line)
    if not m:
        return None

    card_number = m.group(1)
    rest = m.group(2).strip()

    # Strip RC suffix (only meaningful for base set)
    is_rookie = False
    if allow_rc and rest.endswith(" RC"):
        is_rookie = True
        rest = rest[:-3].strip()

    # Split player and team on last " - "
    idx = rest.rfind(" - ")
    if idx == -1:
        return None
    player = rest[:idx].strip()
    team = rest[idx + 3:].strip()

    return card_number, player, team, is_rookie


def parse_section(text: str, allow_rc: bool = False) -> list:
    """Parse all card lines from a checklist text block."""
    cards = []
    for line in text.splitlines():
        result = parse_card_line(line, allow_rc=allow_rc)
        if result:
            card_number, player, team, is_rookie = result
            cards.append({
                "card_number": card_number,
                "player": player,
                "team": team,
                "is_rookie": is_rookie,
                "subset": None,
            })
    return cards


# ─────────────────────────────────────────────────────────────
# Stats
# ─────────────────────────────────────────────────────────────

def compute_stats(appearances: list) -> dict:
    unique_cards = 0
    total_print_run = 0
    one_of_ones = 0
    for appearance in appearances:
        unique_cards += 1  # base appearance
        for parallel in appearance["parallels"]:
            unique_cards += 1
            if parallel["print_run"] is not None and parallel["print_run"] > 0:
                total_print_run += parallel["print_run"]
                if parallel["print_run"] == 1:
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
    rc_players: set = set()
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
                "is_rookie": pname in rc_players,
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
        "set_name": "2025-26 Topps Chrome Cactus Jack Basketball",
        "sport": "Basketball",
        "season": "2025-26",
        "league": "NBA",
        "sections": sections,
        "players": players,
    }


# ─────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Parsing 2025-26 Topps Chrome Cactus Jack Basketball checklist...")

    sections = [
        {
            "insert_set": "Base Set",
            "parallels": PARALLELS_BASE,
            "cards": parse_section(BASE_TEXT, allow_rc=True),
        },
        {
            "insert_set": "All-Star Game Autographs",
            "parallels": PARALLELS_AUTO,
            "cards": parse_section(AUTO_TEXT),
        },
        {
            "insert_set": "Sicko Stars",
            "parallels": PARALLELS_BASE,
            "cards": parse_section(SICKO_TEXT),
        },
    ]

    output = build_output(sections)

    out_path = "nba_cactus_jack_parsed.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nSet: {output['set_name']} ({output['season']})")
    print(f"Sections: {len(output['sections'])}")
    for s in output["sections"]:
        print(f"  {s['insert_set']:<35} {len(s['cards']):>3} cards  {len(s['parallels'])} parallels")

    print(f"\nTotal players: {len(output['players'])}")

    # ── Spot checks ───────────────────────────────────────────
    player_map = {p["player"]: p for p in output["players"]}

    base_section = next(s for s in output["sections"] if s["insert_set"] == "Base Set")
    rc_count = sum(1 for c in base_section["cards"] if c["is_rookie"])
    print(f"\n=== Base Set: {len(base_section['cards'])} cards, {rc_count} RCs ===")

    auto_section = next(s for s in output["sections"] if s["insert_set"] == "All-Star Game Autographs")
    print(f"\n=== All-Star Game Autographs: {len(auto_section['cards'])} cards ===")
    for c in auto_section["cards"][:3]:
        print(f"  {c['card_number']} {c['player']} ({c['team']})")

    sicko_section = next(s for s in output["sections"] if s["insert_set"] == "Sicko Stars")
    print(f"\n=== Sicko Stars: {len(sicko_section['cards'])} cards ===")
    for c in sicko_section["cards"][:3]:
        print(f"  {c['card_number']} {c['player']} ({c['team']})")

    print("\n=== Cooper Flagg ===")
    if "Cooper Flagg" in player_map:
        cf = player_map["Cooper Flagg"]
        for a in cf["appearances"]:
            print(f"  [{a['insert_set']}] #{a['card_number']} | team={a['team']} | rc={a['is_rookie']}")

    print("\n=== Allen Iverson (historic teams) ===")
    if "Allen Iverson" in player_map:
        ai = player_map["Allen Iverson"]
        for a in ai["appearances"]:
            print(f"  [{a['insert_set']}] #{a['card_number']} | team={a['team']}")

    print("\n=== LeBron James ===")
    if "LeBron James" in player_map:
        lj = player_map["LeBron James"]
        st = lj["stats"]
        print(f"  insert_sets={st['insert_sets']}  unique_cards={st['unique_cards']}  1/1s={st['one_of_ones']}")
