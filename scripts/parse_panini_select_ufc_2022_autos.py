#!/usr/bin/env python3
"""Parser for 2022 Panini Select UFC — autographs, memorabilia, and inserts.

Outputs panini_select_ufc_2022_autos_parsed.json for use with:
  npx tsx scripts/seed.ts panini_select_ufc_2022_autos_parsed.json --append
"""

import json
import re

# ─────────────────────────────────────────────────────────────
# Rookies
# ─────────────────────────────────────────────────────────────

# All fighters listed as rookies in the Rookie Signatures section
ROOKIE_SIGNATURES_PLAYERS = {
    "Tom Aspinall",
    "Daniel Rodriguez",
    "Chris Daukaus",
    "Max Griffin",
    "Paul Craig",
    "Alex Morono",
    "Billy Quarantillo",
    "Grant Dawson",
    "Adrian Yanez",
}

# Also mark base-set RC fighters as rookies when they appear in other sections
BASE_RC_FIGHTERS = {
    "Ilia Topuria",
    "Paddy Pimblett",
    "Tom Aspinall",
    "Shavkat Rakhmonov",
    "Dricus du Plessis",
    "Sean Strickland",
    "Grant Dawson",
    "Karol Rosa",
    "Alonzo Menifield",
    "Billy Quarantillo",
    "Daniel Rodriguez",
    "Thiago Moises",
    "Sean Brady",
    "Alex Morono",
    "Chris Daukaus",
    "Max Griffin",
    "Paul Craig",
    "Adrian Yanez",
}

ALL_ROOKIES = BASE_RC_FIGHTERS | ROOKIE_SIGNATURES_PLAYERS


# ─────────────────────────────────────────────────────────────
# Per-card parallel helpers
# ─────────────────────────────────────────────────────────────

# Players for whom Gold parallel is skipped in mem/swatches sections
GOLD_SKIP_MEM = {"Colby Covington", "Holly Holm", "Amanda Nunes"}

# Tie-Dye per-card overrides for Autographed Memorabilia
AM_TIE_DYE_OVERRIDES = {
    "Holly Holm": 22,
    "Amanda Nunes": 20,
    "Israel Adesanya": 16,
}
AM_TIE_DYE_DEFAULT = 25

# Base print runs for Autographed Memorabilia (per card)
AM_BASE_PRINT_RUN = {
    "Israel Adesanya": 99,
}
AM_BASE_DEFAULT = 199

# Selective Swatches — Tie-Dye per-card print runs
# TODO: exact per-card sub-list was not available; using /25 default for all.
SS_TIE_DYE_OVERRIDES: dict = {}
SS_TIE_DYE_DEFAULT = 25

# Gold skip for Selective Swatches
SS_GOLD_SKIP = {"Colby Covington", "Holly Holm", "Amanda Nunes"}
# O'Malley gets Gold /6 instead of /10
SS_GOLD_OMALLEY = 6
SS_GOLD_DEFAULT = 10

# Sparks — Tie-Dye per-card
SPARKS_TIE_DYE_OVERRIDES = {
    "Henry Cejudo": 15,
    "Cody Garbrandt": 12,
}
SPARKS_TIE_DYE_SKIP = {"Israel Adesanya", "Khabib Nurmagomedov"}
SPARKS_TIE_DYE_DEFAULT = 25
SPARKS_GOLD_SKIP = {"Israel Adesanya"}
SPARKS_GOLD_DEFAULT = 10

# Signatures — skip Flash variants for Aldo, Chiesa, Lewis
SIGS_FLASH_SKIP = {"Jose Aldo", "Michael Chiesa", "Derrick Lewis"}


def am_parallels(player):
    """Per-card parallels for Autographed Memorabilia."""
    tie_dye_run = AM_TIE_DYE_OVERRIDES.get(player, AM_TIE_DYE_DEFAULT)
    result = [{"name": "Tie-Dye", "print_run": tie_dye_run}]
    if player not in GOLD_SKIP_MEM:
        result.append({"name": "Gold", "print_run": 10})
    result.append({"name": "Black", "print_run": 1})
    return result


def sigs_parallels(player):
    """Per-card parallels for Signatures (skip Flash for Aldo/Chiesa/Lewis)."""
    base = [
        {"name": "Disco", "print_run": None},
        {"name": "Red", "print_run": 99},
        {"name": "Blue", "print_run": 49},
        {"name": "Tie-Dye", "print_run": 25},
        {"name": "Gold Disco", "print_run": 10},
        {"name": "Gold", "print_run": 10},
        {"name": "Black Disco", "print_run": 1},
        {"name": "Black", "print_run": 1},
    ]
    if player not in SIGS_FLASH_SKIP:
        # Insert Flash-based parallels
        base.insert(1, {"name": "Flash", "print_run": None})
        base.append({"name": "Gold Flash", "print_run": 10})
        base.append({"name": "Black Flash", "print_run": 1})
    return base


def ss_parallels(player):
    """Per-card parallels for Selective Swatches."""
    tie_dye_run = SS_TIE_DYE_OVERRIDES.get(player, SS_TIE_DYE_DEFAULT)
    result = [{"name": "Tie-Dye", "print_run": tie_dye_run}]
    if player not in SS_GOLD_SKIP:
        gold_run = SS_GOLD_OMALLEY if player == "Sean O'Malley" else SS_GOLD_DEFAULT
        result.append({"name": "Gold", "print_run": gold_run})
    result.append({"name": "Black", "print_run": 1})
    return result


def sparks_parallels(player):
    """Per-card parallels for Sparks."""
    result = []
    if player not in SPARKS_TIE_DYE_SKIP:
        tie_dye_run = SPARKS_TIE_DYE_OVERRIDES.get(player, SPARKS_TIE_DYE_DEFAULT)
        result.append({"name": "Tie-Dye", "print_run": tie_dye_run})
    if player not in SPARKS_GOLD_SKIP:
        result.append({"name": "Gold", "print_run": SPARKS_GOLD_DEFAULT})
    result.append({"name": "Black", "print_run": 1})
    return result


# ─────────────────────────────────────────────────────────────
# Section-level parallels (stored in DB for the insert_set)
# ─────────────────────────────────────────────────────────────

# Octagon Action Signatures / Rookie Signatures
PARALLELS_SIG_STANDARD = [
    {"name": "Disco", "print_run": None},
    {"name": "Flash", "print_run": None},
    {"name": "Red", "print_run": 99},
    {"name": "Blue", "print_run": 49},
    {"name": "Tie-Dye", "print_run": 25},
    {"name": "Gold Disco", "print_run": 10},
    {"name": "Gold Flash", "print_run": 10},
    {"name": "Gold", "print_run": 10},
    {"name": "Black", "print_run": 1},
    {"name": "Black Flash", "print_run": 1},
    {"name": "Black Disco", "print_run": 1},
]

# Autographed Memorabilia — section-level (representative values)
PARALLELS_AUTO_MEM = [
    {"name": "Tie-Dye", "print_run": 25},
    {"name": "Gold", "print_run": 10},
    {"name": "Black", "print_run": 1},
]

# Signatures — section-level (note: Flash skipped for 3 players, but section lists it)
PARALLELS_SIGNATURES = [
    {"name": "Disco", "print_run": None},
    {"name": "Flash", "print_run": None},
    {"name": "Red", "print_run": 99},
    {"name": "Blue", "print_run": 49},
    {"name": "Tie-Dye", "print_run": 25},
    {"name": "Gold Disco", "print_run": 10},
    {"name": "Gold Flash", "print_run": 10},
    {"name": "Gold", "print_run": 10},
    {"name": "Black Disco", "print_run": 1},
    {"name": "Black Flash", "print_run": 1},
    {"name": "Black", "print_run": 1},
]

# Selective Swatches — section-level
PARALLELS_SEL_SWATCHES = [
    {"name": "Tie-Dye", "print_run": 25},
    {"name": "Gold", "print_run": 10},
    {"name": "Black", "print_run": 1},
]

# Sparks — section-level
PARALLELS_SPARKS = [
    {"name": "Tie-Dye", "print_run": 25},
    {"name": "Gold", "print_run": 10},
    {"name": "Black", "print_run": 1},
]

# And NEW!, Global Icons, Phenomenon, Select Numbers
PARALLELS_INSERT = [
    {"name": "Flash", "print_run": None},
    {"name": "Silver", "print_run": None},
    {"name": "Gold", "print_run": 10},
    {"name": "Gold Flash", "print_run": 10},
    {"name": "Black", "print_run": 1},
    {"name": "Black Flash", "print_run": 1},
]

# Artistic Selections — no parallels
PARALLELS_ARTISTIC = []


# ─────────────────────────────────────────────────────────────
# Checklists
# ─────────────────────────────────────────────────────────────

AUTO_MEM_TEXT = """
1 Jiri Prochazka - Light Heavyweight /199
2 Colby Covington - Welterweight /199
3 Rose Namajunas - Strawweight /199
4 Michael Chandler - Lightweight /199
5 Deiveson Figueiredo - Flyweight /199
6 Brandon Moreno - Flyweight /199
7 Amanda Nunes - Bantamweight /199
8 Dustin Poirier - Lightweight /199
9 Stipe Miocic - Heavyweight /199
10 Petr Yan - Bantamweight /199
11 Donald Cerrone - Lightweight /199
12 Valentina Shevchenko - Flyweight /199
13 Zabit Magomedsharipov - Featherweight /199
14 Joanna Jedrzejczyk - Strawweight /199
15 Ciryl Gane - Heavyweight /199
16 Edmen Shahbazyan - Middleweight /199
17 Jessica Andrade - Flyweight /199
18 Tony Ferguson - Lightweight /199
19 Zhang Weili - Strawweight /199
20 Urijah Faber - Bantamweight /199
21 Khabib Nurmagomedov - Lightweight /199
22 Israel Adesanya - Middleweight /99
23 Holly Holm - Bantamweight /199
24 Alexander Volkanovski - Featherweight /199
25 Sean O'Malley - Bantamweight /199
"""

OCTAGON_ACTION_SIGS_TEXT = """
1 Jiri Prochazka - Light Heavyweight
2 Rafael Dos Anjos - Lightweight
3 Tony Ferguson - Lightweight
4 Pedro Munhoz - Bantamweight
5 Deiveson Figueiredo - Flyweight
6 Irene Aldana - Bantamweight
7 Uriah Hall - Middleweight
8 Carla Esparza - Strawweight
9 Vicente Luque - Welterweight
10 Belal Muhammad - Welterweight
11 Charles Oliveira - Lightweight
12 Julianna Pena - Bantamweight
13 Miesha Tate - Bantamweight
14 Jack Hermansson - Middleweight
15 Leon Edwards - Welterweight
16 Tecia Torres - Strawweight
17 Magomed Ankalaev - Light Heavyweight
18 Alex Perez - Flyweight
19 Santiago Ponzinibbio - Welterweight
20 Derek Brunson - Middleweight
21 Colby Covington - Welterweight
22 Edmen Shahbazyan - Middleweight
23 Jair Rozenstruik - Heavyweight
24 Viviane Araujo - Flyweight
25 Stephen Thompson - Welterweight
26 Tatiana Suarez - Strawweight
27 Glover Teixeira - Light Heavyweight
28 Joe Lauzon - Lightweight
29 Rob Font - Bantamweight
30 Chan Sung Jung - Featherweight
31 Rose Namajunas - Strawweight
32 Edson Barboza - Featherweight
33 Jared Cannonier - Middleweight
34 Jessica Andrade - Flyweight
35 Brian Ortega - Featherweight
36 Angela Hill - Strawweight
37 Mike Perry - Welterweight
38 Neil Magny - Welterweight
39 Giga Chikadze - Featherweight
40 Calvin Kattar - Featherweight
41 Michael Chandler - Lightweight
42 Nina Nunes - Strawweight
43 Beneil Dariush - Lightweight
44 Alexa Grasso - Flyweight
45 Aleksandar Rakic - Light Heavyweight
"""

ROOKIE_SIGS_TEXT = """
1 Tom Aspinall - Heavyweight
2 Daniel Rodriguez - Welterweight
3 Chris Daukaus - Heavyweight
4 Max Griffin - Welterweight
5 Paul Craig - Light Heavyweight
6 Alex Morono - Welterweight
7 Billy Quarantillo - Featherweight
8 Grant Dawson - Lightweight
9 Adrian Yanez - Bantamweight
"""

SIGNATURES_TEXT = """
1 Dan Henderson - Middleweight
2 Diego Ferreira - Lightweight
3 Derrick Lewis - Heavyweight
4 Antonio Rodrigo Nogueira - Heavyweight
5 Khabib Nurmagomedov - Lightweight
6 TJ Dillashaw - Bantamweight
7 Israel Adesanya - Middleweight
8 Aljamain Sterling - Bantamweight
9 Chuck Liddell - Light Heavyweight
10 Forrest Griffin - Light Heavyweight
11 Matt Hughes - Welterweight
12 Aspen Ladd - Bantamweight
13 Sean O'Malley - Bantamweight
14 Chael Sonnen - Middleweight
15 Kamaru Usman - Welterweight
16 Shogun Rua - Light Heavyweight
17 Royce Gracie - Welterweight
18 Tank Abbott - Heavyweight
19 Nate Diaz - Welterweight
20 Michael Chiesa - Welterweight
21 Henry Cejudo - Bantamweight
22 Amanda Ribas - Flyweight
23 Cain Velasquez - Heavyweight
24 Dominick Cruz - Bantamweight
25 Brock Lesnar - Heavyweight
26 Mackenzie Dern - Strawweight
27 Jorge Masvidal - Welterweight
28 Ciryl Gane - Heavyweight
29 Tito Ortiz - Light Heavyweight
30 Curtis Blaydes - Heavyweight
31 Justin Gaethje - Lightweight
32 Geoff Neal - Welterweight
33 Cody Garbrandt - Bantamweight
34 Jose Aldo - Bantamweight
35 Georges St-Pierre - Welterweight
36 Mark Coleman - Heavyweight
37 Daniel Cormier - Heavyweight
38 Rich Franklin - Middleweight
39 BJ Penn - Lightweight
40 Marlon Vera - Bantamweight
41 Alexander Volkanovski - Featherweight
42 James Krause - Welterweight
43 Rashad Evans - Light Heavyweight
44 Urijah Faber - Bantamweight
45 Anderson Silva - Middleweight
"""

SEL_SWATCHES_TEXT = """
1 Zhang Weili - Strawweight
2 Francis Ngannou - Heavyweight
3 Jessica Andrade - Flyweight
4 Demian Maia - Welterweight
5 Marlon Moraes - Bantamweight
6 Al Iaquinta - Lightweight
7 Robert Whittaker - Middleweight
8 Colby Covington - Welterweight
9 Thiago Santos - Light Heavyweight
10 Dominick Cruz - Bantamweight
11 Conor McGregor - Welterweight
12 Gilbert Burns - Welterweight
13 Joanna Jedrzejczyk - Strawweight
14 Kelvin Gastelum - Middleweight
15 Max Holloway - Featherweight
16 Amanda Nunes - Featherweight
17 Rose Namajunas - Strawweight
18 Deiveson Figueiredo - Flyweight
19 Tyron Woodley - Welterweight
20 Donald Cerrone - Welterweight
21 Islam Makhachev - Lightweight
22 Holly Holm - Bantamweight
23 Jose Aldo - Bantamweight
24 Marlon Vera - Bantamweight
25 Michael Chiesa - Welterweight
26 Brandon Moreno - Flyweight
27 Sean O'Malley - Bantamweight
28 Diego Ferreira - Lightweight
29 Valentina Shevchenko - Flyweight
30 Edmen Shahbazyan - Middleweight
31 Marvin Vettori - Middleweight
32 Jair Rozenstruik - Heavyweight
33 Kevin Holland - Middleweight
34 Claudia Gadelha - Strawweight
35 Petr Yan - Bantamweight
"""

SPARKS_TEXT = """
1 Alexander Volkanovski - Featherweight
2 Michael Chandler - Lightweight
3 Cody Garbrandt - Bantamweight
4 Rodolfo Vieira - Middleweight
5 Dominick Reyes - Light Heavyweight
6 Tony Ferguson - Lightweight
7 Frankie Edgar - Bantamweight
8 Jan Blachowicz - Light Heavyweight
9 Demian Maia - Welterweight
10 Joseph Benavidez - Flyweight
11 Andrei Arlovski - Heavyweight
12 Paul Felder - Lightweight
13 Dan Ige - Featherweight
14 Ryan Spann - Light Heavyweight
15 Dustin Poirier - Lightweight
16 Urijah Faber - Bantamweight
17 Henry Cejudo - Bantamweight
18 Jiri Prochazka - Light Heavyweight
19 Kelvin Gastelum - Middleweight
20 Khabib Nurmagomedov - Lightweight
21 Ciryl Gane - Heavyweight
22 Robbie Lawler - Welterweight
23 Diego Sanchez - Welterweight
24 Stipe Miocic - Heavyweight
25 Felice Herrig - Strawweight
26 Zabit Magomedsharipov - Featherweight
27 Israel Adesanya - Middleweight
28 Jorge Masvidal - Welterweight
29 Marlon Vera - Bantamweight
30 Matt Schnell - Flyweight
"""

AND_NEW_TEXT = """
1 Conor McGregor - Featherweight
2 Glover Teixeira - Light Heavyweight
3 Brandon Moreno - Flyweight
4 Francis Ngannou - Heavyweight
5 Amanda Nunes - Bantamweight
6 Jan Blachowicz - Light Heavyweight
7 Rose Namajunas - Strawweight
8 Israel Adesanya - Middleweight
9 Alexander Volkanovski - Featherweight
10 Kamaru Usman - Welterweight
"""

ARTISTIC_SELECTIONS_TEXT = """
1 Rose Namajunas - Strawweight
2 Kamaru Usman - Welterweight
3 Jon Jones - Light Heavyweight
4 Alexander Volkanovski - Featherweight
5 Conor McGregor - Lightweight
6 Francis Ngannou - Heavyweight
7 Amanda Nunes - Featherweight
8 Israel Adesanya - Middleweight
9 Valentina Shevchenko - Flyweight
10 Khabib Nurmagomedov - Lightweight
"""

GLOBAL_ICONS_TEXT = """
1 Francis Ngannou - Heavyweight
2 Robert Whittaker - Middleweight
3 Deiveson Figueiredo - Flyweight
4 Conor McGregor - Lightweight
5 Brandon Moreno - Flyweight
6 Khamzat Chimaev - Welterweight
7 Amanda Nunes - Bantamweight
8 Magomed Ankalaev - Light Heavyweight
9 Kamaru Usman - Welterweight
10 Li Jingliang - Welterweight
11 Ciryl Gane - Heavyweight
12 Jan Blachowicz - Light Heavyweight
13 Gilbert Burns - Welterweight
14 Tom Aspinall - Heavyweight
15 Valentina Shevchenko - Flyweight
16 Islam Makhachev - Lightweight
17 Alexander Volkanovski - Featherweight
18 Giga Chikadze - Featherweight
19 Israel Adesanya - Middleweight
20 Anderson Silva - Middleweight
21 Zhang Weili - Strawweight
22 Jessica Andrade - Flyweight
23 Marvin Vettori - Middleweight
24 Jiri Prochazka - Light Heavyweight
25 Petr Yan - Bantamweight
26 Khabib Nurmagomedov - Lightweight
27 Charles Oliveira - Lightweight
28 Paul Craig - Light Heavyweight
29 Glover Teixeira - Light Heavyweight
30 Georges St-Pierre - Welterweight
"""

PHENOMENON_TEXT = """
1 Magomed Ankalaev - Light Heavyweight
2 Adrian Yanez - Bantamweight
3 Darren Till - Middleweight
4 Askar Askarov - Flyweight
5 Sean Brady - Welterweight
6 Rose Namajunas - Strawweight
7 Grant Dawson - Lightweight
8 Bryce Mitchell - Featherweight
9 Tom Aspinall - Heavyweight
10 Yair Rodriguez - Featherweight
11 Aleksandar Rakic - Light Heavyweight
12 Petr Yan - Bantamweight
13 Kevin Holland - Middleweight
14 Aspen Ladd - Bantamweight
15 Michel Pereira - Welterweight
16 Tracy Cortez - Flyweight
17 Rafael Fiziev - Lightweight
18 Arnold Allen - Featherweight
19 Marvin Vettori - Middleweight
20 Song Yadong - Bantamweight
21 Edmen Shahbazyan - Middleweight
22 Cory Sandhagen - Bantamweight
23 Khamzat Chimaev - Welterweight
24 Maycee Barber - Flyweight
25 Paddy Pimblett - Lightweight
26 Mackenzie Dern - Strawweight
27 Chase Hooper - Featherweight
28 Movsar Evloev - Featherweight
29 Jiri Prochazka - Light Heavyweight
30 Sean O'Malley - Bantamweight
"""

SELECT_NUMBERS_TEXT = """
1 Kamaru Usman - Welterweight
2 Nate Diaz - Lightweight
3 Francis Ngannou - Heavyweight
4 Max Holloway - Featherweight
5 Stipe Miocic - Heavyweight
6 Cory Sandhagen - Bantamweight
7 Marvin Vettori - Middleweight
8 Merab Dvalishvili - Bantamweight
9 Israel Adesanya - Middleweight
10 Valentina Shevchenko - Flyweight
11 Georges St-Pierre - Welterweight
12 Khabib Nurmagomedov - Lightweight
13 Cain Velasquez - Heavyweight
14 Alexander Volkanovski - Featherweight
15 Ciryl Gane - Heavyweight
16 Petr Yan - Bantamweight
17 Jon Jones - Light Heavyweight
18 Amanda Nunes - Bantamweight
19 Jorge Masvidal - Welterweight
20 Zhang Weili - Strawweight
21 Conor McGregor - Lightweight
22 Chan Sung Jung - Featherweight
23 Casey O'Neill - Flyweight
24 Zabit Magomedsharipov - Featherweight
25 Anderson Silva - Middleweight
26 TJ Dillashaw - Bantamweight
27 Khamzat Chimaev - Middleweight
28 Holly Holm - Bantamweight
29 BJ Penn - Welterweight
30 Joanna Jedrzejczyk - Strawweight
"""


# ─────────────────────────────────────────────────────────────
# Parsing
# ─────────────────────────────────────────────────────────────

CARD_LINE_RE = re.compile(r'^(\d+)\s+(.+?)(?:\s+/\d+)?\s*$')


def parse_cards(text, subset_tag, rookie_set=None):
    """Parse card lines. rookie_set overrides which players are rookies."""
    if rookie_set is None:
        rookie_set = ALL_ROOKIES
    cards = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        m = CARD_LINE_RE.match(line)
        if not m:
            continue
        card_number = m.group(1)
        rest = m.group(2).strip()
        idx = rest.rfind(" - ")
        if idx == -1:
            continue
        player = rest[:idx].strip()
        cards.append({
            "card_number": card_number,
            "player": player,
            "team": None,
            "is_rookie": player in rookie_set,
            "subset": subset_tag,
        })
    return cards


# ─────────────────────────────────────────────────────────────
# Stats computation
# ─────────────────────────────────────────────────────────────

def compute_stats(appearances):
    unique_cards = 0
    total_print_run = 0
    one_of_ones = 0
    for appearance in appearances:
        unique_cards += 1  # base card
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

def build_output(sections):
    """
    sections is a list of dicts:
      {
        "insert_set": str,
        "parallels": [...],          # section-level parallels for DB
        "cards": [...],              # card list
        "per_card_parallels": fn,    # optional: fn(player) -> parallels list
      }
    """
    player_index = {}

    for section in sections:
        per_card_fn = section.get("per_card_parallels")
        for card in section["cards"]:
            pname = card["player"]
            if pname not in player_index:
                player_index[pname] = {"player": pname, "appearances": []}
            card_parallels = per_card_fn(pname) if per_card_fn else section["parallels"]
            player_index[pname]["appearances"].append({
                "insert_set": section["insert_set"],
                "card_number": card["card_number"],
                "team": card["team"],
                "is_rookie": card["is_rookie"],
                "subset_tag": card["subset"],
                "parallels": card_parallels,
            })

    # Build sections output (strip per_card_parallels fn — not JSON serializable)
    sections_out = []
    for section in sections:
        sections_out.append({
            "insert_set": section["insert_set"],
            "parallels": section["parallels"],
            "cards": section["cards"],
        })

    players_out = []
    for pname in sorted(player_index.keys()):
        data = player_index[pname]
        players_out.append({
            "player": pname,
            "appearances": data["appearances"],
            "stats": compute_stats(data["appearances"]),
        })

    return {
        "set_name": "2022 Panini Select UFC",
        "sport": "MMA",
        "season": "2022",
        "league": "UFC",
        "sections": sections_out,
        "players": players_out,
    }


# ─────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Parsing 2022 Panini Select UFC (autos / memorabilia / inserts)...")

    sections = [
        {
            "insert_set": "Autographed Memorabilia",
            "parallels": PARALLELS_AUTO_MEM,
            "cards": parse_cards(AUTO_MEM_TEXT, "Autographed Memorabilia"),
            "per_card_parallels": am_parallels,
        },
        {
            "insert_set": "Octagon Action Signatures",
            "parallels": PARALLELS_SIG_STANDARD,
            "cards": parse_cards(OCTAGON_ACTION_SIGS_TEXT, "Octagon Action Signatures"),
        },
        {
            "insert_set": "Rookie Signatures",
            "parallels": PARALLELS_SIG_STANDARD,
            "cards": parse_cards(
                ROOKIE_SIGS_TEXT,
                "Rookie Signatures",
                rookie_set=ROOKIE_SIGNATURES_PLAYERS,
            ),
        },
        {
            "insert_set": "Signatures",
            "parallels": PARALLELS_SIGNATURES,
            "cards": parse_cards(SIGNATURES_TEXT, "Signatures"),
            "per_card_parallels": sigs_parallels,
        },
        {
            "insert_set": "Selective Swatches",
            "parallels": PARALLELS_SEL_SWATCHES,
            "cards": parse_cards(SEL_SWATCHES_TEXT, "Selective Swatches"),
            "per_card_parallels": ss_parallels,
        },
        {
            "insert_set": "Sparks",
            "parallels": PARALLELS_SPARKS,
            "cards": parse_cards(SPARKS_TEXT, "Sparks"),
            "per_card_parallels": sparks_parallels,
        },
        {
            "insert_set": "And NEW!",
            "parallels": PARALLELS_INSERT,
            "cards": parse_cards(AND_NEW_TEXT, "And NEW!"),
        },
        {
            "insert_set": "Artistic Selections",
            "parallels": PARALLELS_ARTISTIC,
            "cards": parse_cards(ARTISTIC_SELECTIONS_TEXT, "Artistic Selections"),
        },
        {
            "insert_set": "Global Icons",
            "parallels": PARALLELS_INSERT,
            "cards": parse_cards(GLOBAL_ICONS_TEXT, "Global Icons"),
        },
        {
            "insert_set": "Phenomenon",
            "parallels": PARALLELS_INSERT,
            "cards": parse_cards(PHENOMENON_TEXT, "Phenomenon"),
        },
        {
            "insert_set": "Select Numbers",
            "parallels": PARALLELS_INSERT,
            "cards": parse_cards(SELECT_NUMBERS_TEXT, "Select Numbers"),
        },
    ]

    output = build_output(sections)

    out_path = "panini_select_ufc_2022_autos_parsed.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nSet: {output['set_name']} ({output['season']})")
    print(f"Sections: {len(output['sections'])}")
    for s in output["sections"]:
        print(
            f"  {s['insert_set']:<30} {len(s['cards']):>3} cards  "
            f"{len(s['parallels'])} parallels"
        )

    print(f"\nTotal players (autos/inserts): {len(output['players'])}")

    # ── Spot checks ───────────────────────────────────────────
    player_map = {p["player"]: p for p in output["players"]}

    # Section card counts
    expected = {
        "Autographed Memorabilia": 25,
        "Octagon Action Signatures": 45,
        "Rookie Signatures": 9,
        "Signatures": 45,
        "Selective Swatches": 35,
        "Sparks": 30,
        "And NEW!": 10,
        "Artistic Selections": 10,
        "Global Icons": 30,
        "Phenomenon": 30,
        "Select Numbers": 30,
    }
    for s in output["sections"]:
        n = len(s["cards"])
        exp = expected.get(s["insert_set"])
        status = "OK" if n == exp else f"MISMATCH (expected {exp})"
        print(f"  {s['insert_set']:<30} {n} cards — {status}")

    # Rookie Signatures — all 9 should be is_rookie
    rs = next(
        (s for s in output["sections"] if s["insert_set"] == "Rookie Signatures"), None
    )
    if rs:
        non_rc = [c["player"] for c in rs["cards"] if not c["is_rookie"]]
        if non_rc:
            print(f"\nWARNING: Rookie Signatures with is_rookie=False: {non_rc}")
        else:
            print("\nAll 9 Rookie Signatures correctly marked is_rookie=True")

    # Verify per-card parallel exceptions
    # Autographed Memorabilia: Holm should have Tie-Dye /22, no Gold
    holm_am = player_map.get("Holly Holm")
    if holm_am:
        am_app = next(
            (a for a in holm_am["appearances"] if a["insert_set"] == "Autographed Memorabilia"),
            None,
        )
        if am_app:
            td = next((p for p in am_app["parallels"] if p["name"] == "Tie-Dye"), None)
            gold = next((p for p in am_app["parallels"] if p["name"] == "Gold"), None)
            print(f"\nHolly Holm AM: Tie-Dye={td['print_run'] if td else 'MISSING'}, Gold={'MISSING (correct)' if not gold else gold['print_run']}")

    # Adesanya AM: Tie-Dye /16, Gold /10
    ades_am = player_map.get("Israel Adesanya")
    if ades_am:
        am_app = next(
            (a for a in ades_am["appearances"] if a["insert_set"] == "Autographed Memorabilia"),
            None,
        )
        if am_app:
            td = next((p for p in am_app["parallels"] if p["name"] == "Tie-Dye"), None)
            gold = next((p for p in am_app["parallels"] if p["name"] == "Gold"), None)
            print(f"Israel Adesanya AM: Tie-Dye={td['print_run'] if td else 'MISSING'}, Gold={gold['print_run'] if gold else 'MISSING'}")

    # Signatures: Aldo should have no Flash
    aldo_sigs = player_map.get("Jose Aldo")
    if aldo_sigs:
        sig_app = next(
            (a for a in aldo_sigs["appearances"] if a["insert_set"] == "Signatures"), None
        )
        if sig_app:
            flash = [p["name"] for p in sig_app["parallels"] if "Flash" in p["name"]]
            print(f"\nJose Aldo Signatures Flash parallels: {flash if flash else 'None (correct)'}")

    # Sparks: Adesanya should have no Tie-Dye, no Gold
    ades_sparks = player_map.get("Israel Adesanya")
    if ades_sparks:
        sp_app = next(
            (a for a in ades_sparks["appearances"] if a["insert_set"] == "Sparks"), None
        )
        if sp_app:
            print(f"\nIsrael Adesanya Sparks parallels: {[p['name'] for p in sp_app['parallels']]}")
