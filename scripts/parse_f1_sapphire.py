#!/usr/bin/env python3
"""Parser for 2025 Topps Chrome Sapphire Formula 1."""

import json
import re

# ─────────────────────────────────────────────────────────────
# Team mappings
# ─────────────────────────────────────────────────────────────

F1_TEAMS = {
    "Max Verstappen":      "Oracle Red Bull Racing",
    "Yuki Tsunoda":        "Oracle Red Bull Racing",
    "Charles Leclerc":     "Scuderia Ferrari HP",
    "Lewis Hamilton":      "Scuderia Ferrari HP",
    "Lando Norris":        "McLaren Formula 1 Team",
    "Oscar Piastri":       "McLaren Formula 1 Team",
    "George Russell":      "Mercedes-AMG PETRONAS",
    "Kimi Antonelli":      "Mercedes-AMG PETRONAS",
    "Fernando Alonso":     "Aston Martin Aramco",
    "Lance Stroll":        "Aston Martin Aramco",
    "Liam Lawson":         "Visa Cash App Racing Bulls",
    "Isack Hadjar":        "Visa Cash App Racing Bulls",
    "Esteban Ocon":        "MoneyGram Haas F1 Team",
    "Oliver Bearman":      "MoneyGram Haas F1 Team",
    "Pierre Gasly":        "BWT Alpine F1 Team",
    "Franco Colapinto":    "BWT Alpine F1 Team",
    "Alex Albon":          "Atlassian Williams Racing",
    "Carlos Sainz":        "Atlassian Williams Racing",
    "Nico Hulkenberg":     "Stake F1 Team KICK Sauber",
    "Gabriel Bortoleto":   "Stake F1 Team KICK Sauber",
    "Daniel Ricciardo":    "Visa Cash App Racing Bulls",
    "Zhou Guanyu":         "Stake F1 Team KICK Sauber",
}

F2_TEAMS = {
    "Leonardo Fornaroli":  "Invicta Racing",
    "Roman Staněk":        "Invicta Racing",
    "Arvid Lindblad":      "Campos Racing",
    "Josep María Martí":   "Campos Racing",
    "Richard Verschoor":   "MP Motorsport",
    "Oliver Goethe":       "MP Motorsport",
    "Dino Beganovic":      "Hitech TGR",
    "Luke Browning":       "Hitech TGR",
    "Gabriele Minì":       "PREMA Racing",
    "Sebastián Montoya":   "PREMA Racing",
    "Jak Crawford":        "DAMS Lucas Oil",
    "Kush Maini":          "DAMS Lucas Oil",
    "Ritomo Miyata":       "ART Grand Prix",
    "Victor Martins":      "ART Grand Prix",
    "Alexander Dunne":     "Rodin Motorsport",
    "Amaury Cordeel":      "Rodin Motorsport",
    "Joshua Dürksen":      "AIX Racing",
    "Cian Shields":        "AIX Racing",
    "Max Esterson":        "Trident",
    "Sami Meguetounif":    "Trident",
    "John Bennett":        "Van Amersfoort Racing",
    "Rafael Villagómez":   "Van Amersfoort Racing",
}

F3_TEAMS = {
    "Noel León":           "PREMA Racing",
    "Brando Badoer":       "PREMA Racing",
    "Ugo Ugochukwu":       "PREMA Racing",
    "Noah Strømsted":      "Trident",
    "Rafael Câmara":       "Trident",
    "Charlie Wurz":        "Trident",
    "Tim Tramnitz":        "MP Motorsport",
    "Bruno del Pino":      "MP Motorsport",
    "Alessandro Giusti":   "MP Motorsport",
    "Nikola Tsolov":       "Campos Racing",
    "Tasanapol Inthraphuvasak": "Campos Racing",
    "Mari Boya":           "Campos Racing",
    "Joshua Dufek":        "Hitech TGR",
    "Gerrard Xie":         "Hitech TGR",
    "Martinius Stenshorne": "Hitech TGR",
    "Théophile Naël":      "Van Amersfoort Racing",
    "Santiago Ramos":      "Van Amersfoort Racing",
    "Ivan Domingues":      "Van Amersfoort Racing",
    "James Wharton":       "ART Grand Prix",
    "Tuukka Taponen":      "ART Grand Prix",
    "Laurens van Hoepen":  "ART Grand Prix",
    "Javier Sagrera":      "AIX Racing",
    "Nicola Marinangeli":  "AIX Racing",
    "Nikita Bedrin":       "AIX Racing",
    "Callum Voisin":       "Rodin Motorsport",
    "Louis Sharp":         "Rodin Motorsport",
    "Roman Bilinski":      "Rodin Motorsport",
    "Matías Zagazeta":     "DAMS Lucas Oil",
    "Nicola Lacorte":      "DAMS Lucas Oil",
    "Christian Ho":        "DAMS Lucas Oil",
}

PRINCIPALS_TEAMS = {
    "Christian Horner":    "Oracle Red Bull Racing",
    "Frédéric Vasseur":    "Scuderia Ferrari HP",
    "Andrea Stella":       "McLaren Formula 1 Team",
    "Toto Wolff":          "Mercedes-AMG PETRONAS",
    "Andy Cowell":         "Aston Martin Aramco",
    "Laurent Mekies":      "Visa Cash App Racing Bulls",
    "Ayao Komatsu":        "MoneyGram Haas F1 Team",
    "Flavio Briatore":     "BWT Alpine F1 Team",
    "James Vowles":        "Atlassian Williams Racing",
    "Jonathan Wheatley":   "Stake F1 Team KICK Sauber",
}

# Combined lookup (F1 > F2 > F3 > Principals)
TEAM_MAP: dict[str, str] = {}
TEAM_MAP.update(F3_TEAMS)
TEAM_MAP.update(F2_TEAMS)
TEAM_MAP.update(PRINCIPALS_TEAMS)
TEAM_MAP.update(F1_TEAMS)  # F1 overrides last

# Rookie drivers for this season (marked RC in checklist)
RC_DRIVERS = {
    "Kimi Antonelli",
    "Liam Lawson",
    "Isack Hadjar",
    "Oliver Bearman",
    "Gabriel Bortoleto",
}


def get_team(player: str):
    return TEAM_MAP.get(player)


def is_rc(player: str) -> bool:
    return player in RC_DRIVERS


# ─────────────────────────────────────────────────────────────
# Parallel definitions
# ─────────────────────────────────────────────────────────────

PARALLELS_BASE = [
    {"name": "Yellow Sapphire",       "print_run": 75},
    {"name": "Gold Sapphire",         "print_run": 50},
    {"name": "Orange Sapphire",       "print_run": 25},
    {"name": "B&W Sapphire",          "print_run": 15},
    {"name": "Black Sapphire",        "print_run": 10},
    {"name": "Red Sapphire",          "print_run": 5},
    {"name": "Padparadscha Sapphire", "print_run": 1},
]

PARALLELS_AUTO = [
    {"name": "Orange Sapphire",       "print_run": 25},
    {"name": "Black Sapphire",        "print_run": 10},
    {"name": "Red Sapphire",          "print_run": 5},
    {"name": "Padparadscha Sapphire", "print_run": 1},
]

# /50-base inserts: Gold /50 is the base numbered version
PARALLELS_INSERT = [
    {"name": "Gold Sapphire",         "print_run": 50},
    {"name": "Orange Sapphire",       "print_run": 25},
    {"name": "B&W Sapphire",          "print_run": 15},
    {"name": "Purple Sapphire",       "print_run": 10},
    {"name": "Red Sapphire",          "print_run": 5},
    {"name": "Padparadscha Sapphire", "print_run": 1},
]

PARALLELS_SF = [
    {"name": "Superfractor", "print_run": 1},
]

# ─────────────────────────────────────────────────────────────
# Base set section header → subset_tag mapping
# ─────────────────────────────────────────────────────────────

BASE_SECTION_HEADERS = {
    "F1 Drivers":                "F1 Drivers",
    "F2 Drivers":                "F2 Drivers",
    "F3 Drivers":                "F3 Drivers",
    "F1 Cars":                   "F1 Cars",
    "Grand Prix Winners":        "Grand Prix Winners",
    "Pole Position":             "Pole Position",
    "Grand Prix Driver of the Day": "Grand Prix Driver of the Day",
    "F1 Award Winners":          "F1 Award Winners",
    "F1 Legends":                "F1 Legends",
    "F1 Duo Cards":              "F1 Duo Cards",
    "F1 Team Logo Cards":        "F1 Team Logo Cards",
    "F1 On The Move":            "F1 On The Move",
    "F1 Team Principals":        "F1 Team Principals",
}

# ─────────────────────────────────────────────────────────────
# Embedded checklists
# ─────────────────────────────────────────────────────────────

BASE_TEXT = """
F1 Drivers
1 Max Verstappen
2 Yuki Tsunoda
3 Charles Leclerc
4 Lewis Hamilton
5 Lando Norris
6 Oscar Piastri
7 George Russell
8 Kimi Antonelli RC
9 Fernando Alonso
10 Lance Stroll
11 Liam Lawson RC
12 Isack Hadjar RC
13 Esteban Ocon
14 Oliver Bearman RC
15 Franco Colapinto
16 Pierre Gasly
17 Alex Albon
18 Carlos Sainz
19 Nico Hulkenberg
20 Gabriel Bortoleto RC
F2 Drivers
21 Leonardo Fornaroli
22 Roman Staněk
23 Arvid Lindblad
24 Josep María Martí
25 Richard Verschoor
26 Oliver Goethe
27 Dino Beganovic
28 Luke Browning
29 Gabriele Minì
30 Sebastián Montoya
31 Jak Crawford
32 Kush Maini
33 Ritomo Miyata
34 Victor Martins
35 Alexander Dunne
36 Amaury Cordeel
37 Joshua Dürksen
38 Cian Shields
39 Max Esterson
40 Sami Meguetounif
41 John Bennett
42 Rafael Villagómez
F3 Drivers
43 Noel León
44 Brando Badoer
45 Ugo Ugochukwu
46 Noah Strømsted
47 Rafael Câmara
48 Charlie Wurz
49 Tim Tramnitz
50 Bruno del Pino
51 Alessandro Giusti
52 Nikola Tsolov
53 Tasanapol Inthraphuvasak
54 Mari Boya
55 Joshua Dufek
56 Gerrard Xie
57 Martinius Stenshorne
58 Théophile Naël
59 Santiago Ramos
60 Ivan Domingues
61 James Wharton
62 Tuukka Taponen
63 Laurens van Hoepen
64 Javier Sagrera
65 Nicola Marinangeli
66 Nikita Bedrin
67 Callum Voisin
68 Louis Sharp
69 Roman Bilinski
70 Matías Zagazeta
71 Nicola Lacorte
72 Christian Ho
F1 Cars
73 Max Verstappen
74 Yuki Tsunoda
75 Charles Leclerc
76 Lewis Hamilton
77 Lando Norris
78 Oscar Piastri
79 George Russell
80 Kimi Antonelli RC
81 Fernando Alonso
82 Lance Stroll
83 Liam Lawson RC
84 Isack Hadjar RC
85 Esteban Ocon
86 Oliver Bearman RC
87 Franco Colapinto
88 Pierre Gasly
89 Alex Albon
90 Carlos Sainz
91 Nico Hulkenberg
92 Gabriel Bortoleto RC
Grand Prix Winners
93 Max Verstappen
94 Max Verstappen
95 Carlos Sainz
96 Max Verstappen
97 Max Verstappen
98 Lando Norris
99 Max Verstappen
100 Charles Leclerc
101 Max Verstappen
102 Max Verstappen
103 George Russell
104 Lewis Hamilton
105 Oscar Piastri
106 Lewis Hamilton
107 Lando Norris
108 Charles Leclerc
109 Oscar Piastri
110 Lando Norris
111 Charles Leclerc
112 Carlos Sainz
113 Max Verstappen
114 George Russell
115 Max Verstappen
116 Lando Norris
Pole Position
117 Max Verstappen
118 Charles Leclerc
119 George Russell
120 Lando Norris
121 Carlos Sainz
Grand Prix Driver of the Day
122 Carlos Sainz
123 Oliver Bearman RC
124 Carlos Sainz
125 Charles Leclerc
126 Lando Norris
127 Lando Norris
128 Lando Norris
129 Charles Leclerc
130 Lando Norris
131 Lando Norris
132 Lando Norris
133 Lewis Hamilton
134 Oscar Piastri
135 Lewis Hamilton
136 Lando Norris
137 Charles Leclerc
138 Oscar Piastri
139 Daniel Ricciardo
140 Charles Leclerc
141 Carlos Sainz
142 Max Verstappen
143 Lewis Hamilton
144 Zhou Guanyu
145 Charles Leclerc
F1 Award Winners
146 Oracle Red Bull Racing
147 Lando Norris
148 Max Verstappen
F1 Legends
149 Alain Prost
150 Damon Hill
151 David Coulthard
152 Emerson Fittipaldi
153 Gerhard Berger
154 Jackie Stewart
155 James Hunt
156 Juan Pablo Montoya
157 Kimi Räikkönen
158 Michael Schumacher
159 Mika Häkkinen
160 Nigel Mansell
161 Mario Andretti
162 Ayrton Senna
163 Jacques Villeneuve
F1 Duo Cards
164 Max Verstappen/Yuki Tsunoda
165 Charles Leclerc/Lewis Hamilton
166 Lando Norris/Oscar Piastri
167 George Russell/Kimi Antonelli
168 Fernando Alonso/Lance Stroll
169 Liam Lawson/Isack Hadjar
170 Esteban Ocon/Oliver Bearman
171 Pierre Gasly/Franco Colapinto
172 Alex Albon/Carlos Sainz
173 Nico Hulkenberg/Gabriel Bortoleto
F1 Team Logo Cards
174 Oracle Red Bull Racing
175 Scuderia Ferrari HP
176 McLaren Formula 1 Team
177 Mercedes-AMG PETRONAS
178 Aston Martin Aramco
179 Visa Cash App Racing Bulls
180 MoneyGram Haas F1 Team
181 BWT Alpine F1 Team
182 Atlassian Williams Racing
183 Stake F1 Team KICK Sauber
F1 On The Move
184 Yuki Tsunoda
185 Kimi Antonelli RC
186 Oliver Bearman RC
187 Franco Colapinto
188 Nico Hulkenberg
189 Carlos Sainz
190 Esteban Ocon
191 Lewis Hamilton
F1 Team Principals
192 Christian Horner
193 Frédéric Vasseur
194 Andrea Stella
195 Toto Wolff
196 Andy Cowell
197 Laurent Mekies
198 Ayao Komatsu
199 Flavio Briatore
200 James Vowles
"""

AUTO_TEXT = """
CAC-ALB Alex Albon
CAC-ALO Fernando Alonso
CAC-ANT Kimi Antonelli
CAC-BAD Brando Badoer (F3)
CAC-BEA Oliver Bearman
CAC-BEG Dino Beganovic (F2)
CAC-BEN John Bennett (F2)
CAC-BIL Roman Bilinski (F3)
CAC-BOR Gabriel Bortoleto
CAC-BRO Luke Browning (F2)
CAC-CAM Rafael Câmara (F3)
CAC-COL Franco Colapinto
CAC-COR Amaury Cordeel (F2)
CAC-COW Andy Cowell
CAC-CRA Jak Crawford (F2)
CAC-DEL Bruno del Pino (F3)
CAC-DOM Ivan Domingues (F3)
CAC-DUN Alexander Dunne (F2)
CAC-DUR Joshua Dürksen (F2)
CAC-EST Max Esterson (F2)
CAC-FOR Leonardo Fornaroli (F2)
CAC-GAS Pierre Gasly
CAC-GIU Alessandro Giusti (F3)
CAC-GOE Oliver Goethe (F2)
CAC-HAD Isack Hadjar
CAC-HAM Lewis Hamilton
CAC-HOR Christian Horner
CAC-HUL Nico Hulkenberg
CAC-KOM Ayao Komatsu
CAC-LAC Nicola Lacorte (F3)
CAC-LAW Liam Lawson
CAC-LIN Arvid Lindblad (F2)
CAC-MAI Kush Maini (F2)
CAC-MAR Josep María Martí (F2)
CAC-MARI Nicola Marinangeli (F3)
CAC-MART Victor Martins (F2)
CAC-MEG Sami Meguetounif (F2)
CAC-MEK Laurent Mekies
CAC-MIN Gabriele Minì (F2)
CAC-MIY Ritomo Miyata (F2)
CAC-MON Sebastián Montoya (F2)
CAC-NAE Théophile Naël (F3)
CAC-NOR Lando Norris
CAC-OCO Esteban Ocon
CAC-PIA Oscar Piastri
CAC-RUS George Russell
CAC-SAG Javier Sagrera (F3)
CAC-SAI Carlos Sainz
CAC-SHA Louis Sharp (F3)
CAC-SHI Cian Shields (F2)
CAC-STA Roman Staněk (F2)
CAC-STE Andrea Stella
CAC-STR Lance Stroll
CAC-STRO Noah Strømsted (F3)
CAC-TAP Tuukka Taponen (F3)
CAC-TSU Yuki Tsunoda
CAC-UGO Ugo Ugochukwu (F3)
CAC-VAS Frédéric Vasseur
CAC-VER Max Verstappen
CAC-VERS Richard Verschoor (F2)
CAC-VIL Rafael Villagómez (F2)
CAC-VOW James Vowles
CAC-WHA James Wharton (F3)
CAC-WHE Jonathan Wheatley
CAC-WOL Toto Wolff
CAC-XIE Gerrard Xie (F3)
"""

SPEED_WHEELS_TEXT = """
75-ALP Pierre Gasly
75-AM Lance Stroll
75-HF1 Esteban Ocon
75-KICK Gabriel Bortoleto
75-MAMG George Russell
75-MCL Lando Norris
75-RBR Yuki Tsunoda
75-SF Charles Leclerc
75-VCARB Isack Hadjar
75-WR Carlos Sainz
"""

ACE_TRADES_TEXT = """
SCA-1 George Russell
SCA-2 Charles Leclerc
SCA-3 Max Verstappen
SCA-4 Lando Norris
SCA-5 Liam Lawson
SCA-6 Fernando Alonso
SCA-7 Carlos Sainz
SCA-8 Esteban Ocon
SCA-9 Pierre Gasly
SCA-10 Nico Hulkenberg
"""

FLOOR_IT_TEXT = """
FI-1 Alain Prost
FI-2 Damon Hill
FI-3 Gerhard Berger
FI-4 Jackie Stewart
FI-5 James Hunt
FI-6 Kimi Räikkönen
FI-7 Michael Schumacher
FI-8 Mika Häkkinen
FI-9 Nigel Mansell
FI-10 Ayrton Senna
"""

HELMET_TEXT = """
HC-1 Kimi Antonelli
HC-2 Lewis Hamilton
HC-3 Yuki Tsunoda
HC-4 Lando Norris
HC-5 Isack Hadjar
HC-6 Fernando Alonso
HC-7 Carlos Sainz
HC-8 Oliver Bearman
HC-9 Franco Colapinto
HC-10 Gabriel Bortoleto
"""

INFINITE_TEXT = """
IS-1 Max Verstappen
IS-2 Lewis Hamilton
IS-3 Lando Norris
IS-4 George Russell
IS-5 Fernando Alonso
IS-6 Liam Lawson
IS-7 Esteban Ocon
IS-8 Pierre Gasly
IS-9 Carlos Sainz
IS-10 Nico Hulkenberg
"""

SELECTIONS_TEXT = """
SS-1 Gabriel Bortoleto
SS-2 Charles Leclerc
SS-3 Oscar Piastri
SS-4 Kimi Antonelli
SS-5 Lance Stroll
SS-6 Isack Hadjar
SS-7 Oliver Bearman
SS-8 Franco Colapinto
SS-9 Alex Albon
"""

SPEED_DEMONS_TEXT = """
SD-1 Kimi Antonelli
SD-2 Lewis Hamilton
SD-3 Yuki Tsunoda
SD-4 Oscar Piastri
SD-5 Isack Hadjar
SD-6 Lance Stroll
SD-7 Alex Albon
SD-8 Oliver Bearman
SD-9 Franco Colapinto
SD-10 Gabriel Bortoleto
SD-11 Kimi Räikkönen
"""

# ─────────────────────────────────────────────────────────────
# Parsers
# ─────────────────────────────────────────────────────────────

BASE_CARD_RE = re.compile(r'^(\d+)\s+(.+?)(\s+RC)?\s*$')
INSERT_CARD_RE = re.compile(r'^([A-Z0-9][A-Z0-9]*-[A-Z0-9]+)\s+(.+?)\s*(?:\([A-Z]\d\))?\s*$')
F_SERIES_STRIP = re.compile(r'\s*\([A-Z]\d\)\s*$')


def parse_base_set(text: str) -> list:
    """Parse base set, tracking section headers for subset_tags."""
    cards = []
    current_section = None

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        # Section header detection
        if line in BASE_SECTION_HEADERS:
            current_section = BASE_SECTION_HEADERS[line]
            continue

        m = BASE_CARD_RE.match(line)
        if not m:
            continue

        card_number = m.group(1)
        name_str = m.group(2).strip()
        has_rc_marker = m.group(3) is not None

        if current_section == "F1 Team Logo Cards":
            # Player IS the team name; no RC, no team lookup
            cards.append({
                "card_number": card_number,
                "player": name_str,
                "team": None,
                "is_rookie": False,
                "subset": current_section,
            })

        elif current_section == "F1 Award Winners" and name_str not in TEAM_MAP:
            # #146 Oracle Red Bull Racing team award — player is the team
            cards.append({
                "card_number": card_number,
                "player": name_str,
                "team": None,
                "is_rookie": False,
                "subset": current_section,
            })

        elif current_section == "F1 Duo Cards":
            parts = [p.strip() for p in name_str.split("/")]
            for p in parts:
                cards.append({
                    "card_number": card_number,
                    "player": p,
                    "team": get_team(p),
                    "is_rookie": is_rc(p),
                    "subset": current_section,
                })

        else:
            # Legends get no team
            team = None if current_section == "F1 Legends" else get_team(name_str)
            rookie = has_rc_marker or is_rc(name_str)
            cards.append({
                "card_number": card_number,
                "player": name_str,
                "team": team,
                "is_rookie": rookie,
                "subset": current_section,
            })

    return cards


def parse_insert_section(text: str, force_no_team: bool = False) -> list:
    """Parse a standard insert/auto section (CODE PLAYER [designation])."""
    cards = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if re.search(r'\bon ebay\b', line, re.IGNORECASE):
            continue

        m = INSERT_CARD_RE.match(line)
        if not m:
            continue

        card_number = m.group(1)
        # Strip F2/F3 designation from player name
        player = F_SERIES_STRIP.sub("", m.group(2)).strip()

        team = None if force_no_team else get_team(player)
        cards.append({
            "card_number": card_number,
            "player": player,
            "team": team,
            "is_rookie": is_rc(player),
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
        unique_cards += 1
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
        "set_name": "2025 Topps Chrome Sapphire Formula 1",
        "sport": "Racing",
        "season": "2025",
        "league": "Formula 1",
        "sections": sections,
        "players": players,
    }


# ─────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Parsing 2025 Topps Chrome Sapphire Formula 1 checklist...")

    base_cards = parse_base_set(BASE_TEXT)

    sections = [
        {"insert_set": "Base Set",             "parallels": PARALLELS_BASE,   "cards": base_cards},
        {"insert_set": "Sapphire Autographs",  "parallels": PARALLELS_AUTO,   "cards": parse_insert_section(AUTO_TEXT)},
        {"insert_set": "1975 Speed Wheels",    "parallels": PARALLELS_INSERT, "cards": parse_insert_section(SPEED_WHEELS_TEXT)},
        {"insert_set": "Ace of Trades",        "parallels": PARALLELS_INSERT, "cards": parse_insert_section(ACE_TRADES_TEXT)},
        {"insert_set": "Floor It",             "parallels": PARALLELS_INSERT, "cards": parse_insert_section(FLOOR_IT_TEXT, force_no_team=True)},
        {"insert_set": "Helmet Collection",    "parallels": PARALLELS_INSERT, "cards": parse_insert_section(HELMET_TEXT)},
        {"insert_set": "Infinite Sapphire",    "parallels": PARALLELS_SF,     "cards": parse_insert_section(INFINITE_TEXT)},
        {"insert_set": "Sapphire Selections",  "parallels": PARALLELS_SF,     "cards": parse_insert_section(SELECTIONS_TEXT)},
        {"insert_set": "Speed Demons",         "parallels": PARALLELS_INSERT, "cards": parse_insert_section(SPEED_DEMONS_TEXT)},
    ]

    output = build_output(sections)

    out_path = "f1_sapphire_parsed.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nSet: {output['set_name']} ({output['season']})")
    print(f"Sections: {len(output['sections'])}")
    for s in output["sections"]:
        print(f"  {s['insert_set']:<30} {len(s['cards']):>4} cards  {len(s['parallels'])} parallels")

    print(f"\nTotal players: {len(output['players'])}")

    player_map = {p["player"]: p for p in output["players"]}

    # Base set spot checks
    base = next(s for s in output["sections"] if s["insert_set"] == "Base Set")
    rc_cards = [c for c in base["cards"] if c["is_rookie"]]
    rc_names = sorted({c["player"] for c in rc_cards})
    print(f"\n=== Base Set: {len(base['cards'])} cards total ===")
    print(f"  RC drivers: {rc_names}")

    # Section counts within base set
    from collections import Counter
    subset_counts = Counter(c["subset"] for c in base["cards"])
    for section, count in sorted(subset_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {section:<40} {count}")

    # F1 Duo Cards co_player check
    duo_section = [c for c in base["cards"] if c["subset"] == "F1 Duo Cards"]
    print(f"\n=== F1 Duo Cards: {len(duo_section)} appearances from 10 cards ===")
    from itertools import groupby
    for card_num, group in groupby(sorted(duo_section, key=lambda x: int(x["card_number"])), key=lambda x: x["card_number"]):
        drivers = [(c["player"], c["team"]) for c in group]
        print(f"  #{card_num}: {drivers[0][0]} ({drivers[0][1]}) / {drivers[1][0]} ({drivers[1][1]})")

    # F1 Legends team check
    legends = [c for c in base["cards"] if c["subset"] == "F1 Legends"]
    no_team = [c for c in legends if c["team"] is None]
    print(f"\n=== F1 Legends: {len(legends)} cards, {len(no_team)} with team=null ===")

    # Team Logo Cards
    logo_cards = [c for c in base["cards"] if c["subset"] == "F1 Team Logo Cards"]
    print(f"\n=== F1 Team Logo Cards: {len(logo_cards)} ===")
    for c in logo_cards[:3]:
        print(f"  #{c['card_number']} player='{c['player']}' team={c['team']}")

    # Max Verstappen stats
    if "Max Verstappen" in player_map:
        mv = player_map["Max Verstappen"]
        st = mv["stats"]
        mv_base = sum(1 for a in mv["appearances"] if a["insert_set"] == "Base Set")
        print(f"\n=== Max Verstappen: {mv_base} base appearances, {st['unique_cards']} total unique cards ===")

    # Kimi Räikkönen (Legends, Floor It — team should be null in both)
    if "Kimi Räikkönen" in player_map:
        kr = player_map["Kimi Räikkönen"]
        print(f"\n=== Kimi Räikkönen ===")
        for a in kr["appearances"]:
            print(f"  [{a['insert_set']}] #{a['card_number']} team={a['team']}")

    # Floor It team check
    floor_it = next(s for s in output["sections"] if s["insert_set"] == "Floor It")
    all_null = all(c["team"] is None for c in floor_it["cards"])
    print(f"\n=== Floor It: {len(floor_it['cards'])} cards, all team=null: {all_null} ===")
