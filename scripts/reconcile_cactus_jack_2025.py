#!/usr/bin/env python3
"""
Reconcile 2025-26 Topps Chrome Cactus Jack Basketball against the official
Topps checklist.

The existing DB data was built from a wrong-source parser
(parse_nba_cactus_jack.py): the Base Set holds the wrong 100 players and two
PHANTOM subsets ("All-Star Game Autographs", "Sicko Stars") exist that are not
in the official product.

This script (DRY-RUN by default; pass --commit to write):
  - Rebuilds the Base Set with the official 100 cards (clear + insert).
  - Populates the 7 official subset shells (Utopia Highlights, Jacked Up,
    LA Flame Legends, Astrovision, Cactus Mode, Base Autograph Variation,
    Cactus Ink) — adding cards only, preserving their existing parallels/odds.
  - Reuses existing set-scoped player rows by (set_id, name); creates new ones
    (subject_role=athlete) for players not yet present in this set.
  - Does NOT touch the phantom subsets (they have parallels) — they are FLAGGED
    for Tyler's separate decision.

After --commit, run:
    npx tsx scripts/generate-slugs.ts
    npx tsx scripts/recompute-unique-cards.ts
    python3 scripts/match_nba_player_ids.py   (optional, for new-player images)
"""

import sqlite3
import sys
import os

DB = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
SET_SLUG = "2025-26-topps-chrome-cactus-jack-basketball"

# Subsets to populate, by exact official name → expected card count is derived
# from the parsed data. Base is handled specially (clear + rebuild).
PHANTOM_NAMES = {"All-Star Game Autographs", "Sicko Stars"}

# ─────────────────────────────────────────────────────────────
# Official checklist (authoritative, from Topps PDF)
# Format per line: "<code> <Player Name> — <Team>" with optional trailing [RC].
# Player-name normalizations applied for set-scoped identity reuse:
#   "Zach Lavine" (JU-25, lowercased in PDF) → "Zach LaVine"
#   "Portland Trailblazers" (CI-YH) → "Portland Trail Blazers"
# Card-number codes preserved verbatim (incl. lowercase "BV-Lm").
# ─────────────────────────────────────────────────────────────

BASE = """
1 Jayson Tatum — Boston Celtics
2 Jaylen Brown — Boston Celtics
3 Cam Thomas — Brooklyn Nets
4 Jalen Brunson — New York Knicks
5 Karl-Anthony Towns — New York Knicks
6 Tyrese Maxey — Philadelphia 76ers
7 Joel Embiid — Philadelphia 76ers
8 Jared McCain — Philadelphia 76ers
9 Gradey Dick — Toronto Raptors
10 Scottie Barnes — Toronto Raptors
11 Matas Buzelis — Chicago Bulls
12 Josh Giddey — Chicago Bulls
13 Cade Cunningham — Detroit Pistons
14 Ausar Thompson — Detroit Pistons
15 Tyrese Haliburton — Indiana Pacers
16 Bennedict Mathurin — Indiana Pacers
17 Giannis Antetokounmpo — Milwaukee Bucks
18 Damian Lillard — Milwaukee Bucks
19 Trae Young — Atlanta Hawks
20 Zaccharie Risacher — Atlanta Hawks
21 LaMelo Ball — Charlotte Hornets
22 Brandon Miller — Charlotte Hornets
23 Tyler Herro — Miami Heat
24 Bam Adebayo — Miami Heat
25 Donovan Mitchell — Cleveland Cavaliers
26 Darius Garland — Cleveland Cavaliers
27 Paolo Banchero — Orlando Magic
28 Franz Wagner — Orlando Magic
29 Alex Sarr — Washington Wizards
30 Bub Carrington — Washington Wizards
31 Nikola Jokić — Denver Nuggets
32 Jamal Murray — Denver Nuggets
33 Anthony Edwards — Minnesota Timberwolves
34 Terrence Shannon Jr. — Minnesota Timberwolves
35 Shai Gilgeous-Alexander — Oklahoma City Thunder
36 Jalen Williams — Oklahoma City Thunder
37 Chet Holmgren — Oklahoma City Thunder
38 Scoot Henderson — Portland Trail Blazers
39 Shaedon Sharpe — Portland Trail Blazers
40 Lauri Markkanen — Utah Jazz
41 Keyonte George — Utah Jazz
42 Stephen Curry — Golden State Warriors
43 Jimmy Butler III — Golden State Warriors
44 Kawhi Leonard — Los Angeles Clippers
45 James Harden — Los Angeles Clippers
46 LeBron James — Los Angeles Lakers
47 Luka Dončić — Los Angeles Lakers
48 Devin Booker — Phoenix Suns
49 Kevin Durant — Houston Rockets
50 DeMar DeRozan — Sacramento Kings
51 Zach LaVine — Sacramento Kings
52 Kyrie Irving — Dallas Mavericks
53 Anthony Davis — Dallas Mavericks
54 Jalen Green — Phoenix Suns
55 Amen Thompson — Houston Rockets
56 Ja Morant — Memphis Grizzlies
57 Jaren Jackson Jr. — Memphis Grizzlies
58 Trey Murphy III — New Orleans Pelicans
59 Victor Wembanyama — San Antonio Spurs
60 De'Aaron Fox — San Antonio Spurs
61 Cooper Flagg — Dallas Mavericks [RC]
62 Dylan Harper — San Antonio Spurs [RC]
63 VJ Edgecombe — Philadelphia 76ers [RC]
64 Kon Knueppel — Charlotte Hornets [RC]
65 Ace Bailey — Utah Jazz [RC]
66 Tre Johnson III — Washington Wizards [RC]
67 Jeremiah Fears — New Orleans Pelicans [RC]
68 Egor Dëmin — Brooklyn Nets [RC]
69 Collin Murray-Boyles — Toronto Raptors [RC]
70 Khaman Maluach — Phoenix Suns [RC]
71 Cedric Coward — Memphis Grizzlies [RC]
72 Noa Essengue — Chicago Bulls [RC]
73 Derik Queen — New Orleans Pelicans [RC]
74 Carter Bryant — San Antonio Spurs [RC]
75 Thomas Sorber — Oklahoma City Thunder [RC]
76 Yang Hansen — Portland Trail Blazers [RC]
77 Joan Beringer — Minnesota Timberwolves [RC]
78 Walter Clayton Jr. — Utah Jazz [RC]
79 Nolan Traore — Brooklyn Nets [RC]
80 Kasparas Jakučionis — Miami Heat [RC]
81 Will Riley — Washington Wizards [RC]
82 Drake Powell — Brooklyn Nets [RC]
83 Asa Newell — Atlanta Hawks [RC]
84 Nique Clifford — Sacramento Kings [RC]
85 Jase Richardson — Orlando Magic [RC]
86 Ben Saraf — Brooklyn Nets [RC]
87 Danny Wolf — Brooklyn Nets [RC]
88 Hugo González — Boston Celtics [RC]
89 Liam McNeeley — Charlotte Hornets [RC]
90 Yanic Konan-Niederhäuser — Los Angeles Clippers [RC]
91 Rasheer Fleming — Phoenix Suns [RC]
92 Noah Penda — Orlando Magic [RC]
93 Sion James — Charlotte Hornets [RC]
94 Ryan Kalkbrenner — Charlotte Hornets [RC]
95 Johni Broome — Philadelphia 76ers [RC]
96 Adou Thiero — Los Angeles Lakers [RC]
97 Will Richard — Golden State Warriors [RC]
98 Chaz Lanier — Detroit Pistons [RC]
99 Kam Jones — Indiana Pacers [RC]
100 Alijah Martin — Toronto Raptors [RC]
"""

UTOPIA = """
UH-1 Jayson Tatum — Boston Celtics
UH-2 Jalen Brunson — New York Knicks
UH-3 Tyrese Maxey — Philadelphia 76ers
UH-4 Tyrese Haliburton — Indiana Pacers
UH-5 Giannis Antetokounmpo — Milwaukee Bucks
UH-6 Donovan Mitchell — Cleveland Cavaliers
UH-7 Nikola Jokić — Denver Nuggets
UH-8 Paolo Banchero — Orlando Magic
UH-9 Anthony Edwards — Minnesota Timberwolves
UH-10 Shai Gilgeous-Alexander — Oklahoma City Thunder
UH-11 Stephen Curry — Golden State Warriors
UH-12 LeBron James — Los Angeles Lakers
UH-13 Devin Booker — Phoenix Suns
UH-14 Kyrie Irving — Dallas Mavericks
UH-15 Ja Morant — Memphis Grizzlies
UH-16 Victor Wembanyama — San Antonio Spurs
UH-17 Amen Thompson — Houston Rockets
UH-18 Kevin Durant — Houston Rockets
UH-19 LaMelo Ball — Charlotte Hornets
UH-20 Luka Dončić — Los Angeles Lakers
UH-21 Cooper Flagg — Dallas Mavericks [RC]
UH-22 Dylan Harper — San Antonio Spurs [RC]
UH-23 VJ Edgecombe — Philadelphia 76ers [RC]
UH-24 Kon Knueppel — Charlotte Hornets [RC]
UH-25 Ace Bailey — Utah Jazz [RC]
UH-26 Tre Johnson III — Washington Wizards [RC]
UH-27 Jeremiah Fears — New Orleans Pelicans [RC]
UH-28 Egor Dëmin — Brooklyn Nets [RC]
UH-29 Collin Murray-Boyles — Toronto Raptors [RC]
UH-30 Khaman Maluach — Phoenix Suns [RC]
UH-31 Cedric Coward — Memphis Grizzlies [RC]
UH-32 Noa Essengue — Chicago Bulls [RC]
UH-33 Derik Queen — New Orleans Pelicans [RC]
UH-34 Carter Bryant — San Antonio Spurs [RC]
UH-35 Thomas Sorber — Oklahoma City Thunder [RC]
UH-36 Yang Hansen — Portland Trail Blazers [RC]
UH-37 Joan Beringer — Minnesota Timberwolves [RC]
UH-38 Walter Clayton Jr. — Utah Jazz [RC]
UH-39 Nolan Traore — Brooklyn Nets [RC]
UH-40 Kasparas Jakučionis — Miami Heat [RC]
"""

JACKED_UP = """
JU-1 Cooper Flagg — Dallas Mavericks [RC]
JU-2 VJ Edgecombe — Philadelphia 76ers [RC]
JU-3 Ace Bailey — Utah Jazz [RC]
JU-4 Collin Murray-Boyles — Toronto Raptors [RC]
JU-5 Khaman Maluach — Phoenix Suns [RC]
JU-6 Derik Queen — New Orleans Pelicans [RC]
JU-7 Carter Bryant — San Antonio Spurs [RC]
JU-8 Thomas Sorber — Oklahoma City Thunder [RC]
JU-9 Yang Hansen — Portland Trail Blazers [RC]
JU-10 Joan Beringer — Minnesota Timberwolves [RC]
JU-11 Jayson Tatum — Boston Celtics
JU-12 Jaylen Brown — Boston Celtics
JU-13 Karl-Anthony Towns — New York Knicks
JU-14 Joel Embiid — Philadelphia 76ers
JU-15 Scottie Barnes — Toronto Raptors
JU-16 Cade Cunningham — Detroit Pistons
JU-17 Brandon Miller — Charlotte Hornets
JU-18 Donovan Mitchell — Cleveland Cavaliers
JU-19 Paolo Banchero — Orlando Magic
JU-20 Anthony Edwards — Minnesota Timberwolves
JU-21 Scoot Henderson — Portland Trail Blazers
JU-22 Jalen Williams — Oklahoma City Thunder
JU-23 Kawhi Leonard — Los Angeles Clippers
JU-24 Kevin Durant — Houston Rockets
JU-25 Zach LaVine — Sacramento Kings
JU-26 Anthony Davis — Dallas Mavericks
JU-27 Alex Sarr — Washington Wizards
JU-28 Jalen Johnson — Atlanta Hawks
JU-29 Pascal Siakam — Indiana Pacers
JU-30 Giannis Antetokounmpo — Milwaukee Bucks
JU-31 Amen Thompson — Houston Rockets
JU-32 Ja Morant — Memphis Grizzlies
JU-33 Victor Wembanyama — San Antonio Spurs
JU-34 Vince Carter — Toronto Raptors
JU-35 Tracy McGrady — Orlando Magic
JU-36 Dwyane Wade — Miami Heat
JU-37 Kevin Garnett — Minnesota Timberwolves
JU-38 Clyde Drexler — Portland Trail Blazers
JU-39 Hakeem Olajuwon — Houston Rockets
JU-40 Dominique Wilkins — Atlanta Hawks
"""

LFL = """
LFL-1 Ray Allen — Miami Heat
LFL-2 Robert Horry — Los Angeles Lakers
LFL-3 Larry Bird — Boston Celtics
LFL-4 Magic Johnson — Los Angeles Lakers
LFL-5 Dirk Nowitzki — Dallas Mavericks
LFL-6 Vince Carter — Toronto Raptors
LFL-7 Tracy McGrady — Houston Rockets
LFL-8 Dwyane Wade — Miami Heat
LFL-9 Kevin Garnett — Minnesota Timberwolves
LFL-10 Allen Iverson — Philadelphia 76ers
LFL-11 Shaquille O'Neal — Orlando Magic
LFL-12 Carmelo Anthony — New York Knicks
LFL-13 Paul Pierce — Boston Celtics
LFL-14 John Stockton — Utah Jazz
LFL-15 Isiah Thomas — Detroit Pistons
LFL-16 David Robinson — San Antonio Spurs
LFL-17 Hakeem Olajuwon — Houston Rockets
LFL-18 James Worthy — Los Angeles Lakers
LFL-19 Clyde Drexler — Portland Trail Blazers
LFL-20 Gary Payton — Seattle Supersonics
"""

ASTRO = """
AST-1 Cooper Flagg — Dallas Mavericks [RC]
AST-2 Dylan Harper — San Antonio Spurs [RC]
AST-3 VJ Edgecombe — Philadelphia 76ers [RC]
AST-4 Kon Knueppel — Charlotte Hornets [RC]
AST-5 Ace Bailey — Utah Jazz [RC]
AST-6 Tre Johnson III — Washington Wizards [RC]
AST-7 Jeremiah Fears — New Orleans Pelicans [RC]
AST-8 Egor Dëmin — Brooklyn Nets [RC]
AST-9 Collin Murray-Boyles — Toronto Raptors [RC]
AST-10 Khaman Maluach — Phoenix Suns [RC]
AST-11 Tyrese Haliburton — Indiana Pacers
AST-12 Giannis Antetokounmpo — Milwaukee Bucks
AST-13 Victor Wembanyama — San Antonio Spurs
AST-14 LaMelo Ball — Charlotte Hornets
AST-15 Nikola Jokić — Denver Nuggets
AST-16 Paolo Banchero — Orlando Magic
AST-17 Anthony Edwards — Minnesota Timberwolves
AST-18 Shai Gilgeous-Alexander — Oklahoma City Thunder
AST-19 Stephen Curry — Golden State Warriors
AST-20 Luka Dončić — Los Angeles Lakers
"""

CACTUS_MODE = """
CM-1 Cooper Flagg — Dallas Mavericks [RC]
CM-2 Dylan Harper — San Antonio Spurs [RC]
CM-3 VJ Edgecombe — Philadelphia 76ers [RC]
CM-4 Kon Knueppel — Charlotte Hornets [RC]
CM-5 Ace Bailey — Utah Jazz [RC]
CM-6 Walter Clayton Jr. — Utah Jazz [RC]
CM-7 Kasparas Jakučionis — Miami Heat [RC]
CM-8 Yang Hansen — Portland Trail Blazers [RC]
CM-9 Egor Dëmin — Brooklyn Nets [RC]
CM-10 Collin Murray-Boyles — Toronto Raptors [RC]
CM-11 Shai Gilgeous-Alexander — Oklahoma City Thunder
CM-12 Stephen Curry — Golden State Warriors
CM-13 Luka Dončić — Los Angeles Lakers
CM-14 Devin Booker — Phoenix Suns
CM-15 Kyrie Irving — Dallas Mavericks
CM-16 Ja Morant — Memphis Grizzlies
CM-17 Donovan Mitchell — Cleveland Cavaliers
CM-18 Nikola Jokić — Denver Nuggets
CM-19 LeBron James — Los Angeles Lakers
CM-20 Jalen Brunson — New York Knicks
"""

BASE_AUTO_VAR = """
BV-AB Ace Bailey — Utah Jazz [RC]
BV-AE Anthony Edwards — Minnesota Timberwolves
BV-AN Asa Newell — Atlanta Hawks [RC]
BV-AS Alex Sarr — Washington Wizards
BV-BM Brandon Miller — Charlotte Hornets
BV-BS Ben Saraf — Brooklyn Nets [RC]
BV-CC Cedric Coward — Memphis Grizzlies [RC]
BV-CF Cooper Flagg — Dallas Mavericks [RC]
BV-CH Chet Holmgren — Oklahoma City Thunder
BV-CMB Collin Murray-Boyles — Toronto Raptors [RC]
BV-CU Cade Cunningham — Detroit Pistons
BV-DH Dylan Harper — San Antonio Spurs [RC]
BV-DP Drake Powell — Brooklyn Nets [RC]
BV-DQ Derik Queen — New Orleans Pelicans [RC]
BV-DW Danny Wolf — Brooklyn Nets [RC]
BV-ED Egor Dëmin — Brooklyn Nets [RC]
BV-GA Giannis Antetokounmpo — Milwaukee Bucks
BV-GD Gradey Dick — Toronto Raptors
BV-JB Joan Beringer — Minnesota Timberwolves [RC]
BV-JH James Harden — Los Angeles Clippers
BV-JM Jamal Murray — Denver Nuggets
BV-JR Jase Richardson — Orlando Magic [RC]
BV-JT Jayson Tatum — Boston Celtics
BV-JU Jalen Brunson — New York Knicks
BV-JW Jalen Williams — Oklahoma City Thunder
BV-KD Kevin Durant — Houston Rockets
BV-KJ Kasparas Jakučionis — Miami Heat [RC]
BV-KK Kon Knueppel — Charlotte Hornets [RC]
BV-KM Khaman Maluach — Phoenix Suns [RC]
BV-LBJ LeBron James — Los Angeles Lakers
BV-Lm Liam McNeeley — Charlotte Hornets [RC]
BV-MT Myles Turner — Indiana Pacers
BV-NC Nique Clifford — Sacramento Kings [RC]
BV-NE Noa Essengue — Chicago Bulls [RC]
BV-NJ Nikola Jokić — Denver Nuggets
BV-NT Nolan Traore — Brooklyn Nets [RC]
BV-PB Paolo Banchero — Orlando Magic
BV-SC Stephen Curry — Golden State Warriors
BV-SGA Shai Gilgeous-Alexander — Oklahoma City Thunder
BV-SH Scoot Henderson — Portland Trail Blazers
BV-TA Tyrese Haliburton — Indiana Pacers
BV-TS Thomas Sorber — Oklahoma City Thunder [RC]
BV-VW Victor Wembanyama — San Antonio Spurs
BV-WC Walter Clayton Jr. — Utah Jazz [RC]
BV-WR Will Riley — Washington Wizards [RC]
BV-YH Yang Hansen — Portland Trail Blazers [RC]
BV-YK Yanic Konan-Niederhäuser — Los Angeles Clippers [RC]
BV-ZL Zach LaVine — Sacramento Kings
BV-ZR Zaccharie Risacher — Atlanta Hawks
"""

CACTUS_INK = """
CI-AB Ace Bailey — Utah Jazz [RC]
CI-AL Anthony Black — Orlando Magic
CI-AM Alijah Martin — Toronto Raptors [RC]
CI-AN Asa Newell — Atlanta Hawks [RC]
CI-AT Adou Thiero — Los Angeles Lakers [RC]
CI-BB Brooks Barnhizer — Oklahoma City Thunder [RC]
CI-BJ Bronny James Jr. — Los Angeles Lakers
CI-BS Ben Saraf — Brooklyn Nets [RC]
CI-CC Cedric Coward — Memphis Grizzlies [RC]
CI-CF Cooper Flagg — Dallas Mavericks [RC]
CI-CL Chaz Lanier — Detroit Pistons [RC]
CI-CMB Collin Murray-Boyles — Toronto Raptors [RC]
CI-CW Cam Whitmore — Houston Rockets
CI-DH Dylan Harper — San Antonio Spurs [RC]
CI-DP Drake Powell — Brooklyn Nets [RC]
CI-DQ Derik Queen — New Orleans Pelicans [RC]
CI-DW Danny Wolf — Brooklyn Nets [RC]
CI-ED Egor Dëmin — Brooklyn Nets [RC]
CI-IC Isaiah Collier — Utah Jazz
CI-JA Jarace Walker — Indiana Pacers
CI-JB Joan Beringer — Minnesota Timberwolves [RC]
CI-JE Jaylen Wells — Memphis Grizzlies
CI-JH Jett Howard — Orlando Magic
CI-JR Jase Richardson — Orlando Magic [RC]
CI-JT Jaylon Tyson — Cleveland Cavaliers
CI-JW Jamir Watkins — Washington Wizards [RC]
CI-KB Koby Brea — Phoenix Suns [RC]
CI-KJ Kasparas Jakučionis — Miami Heat [RC]
CI-KK Kon Knueppel — Charlotte Hornets [RC]
CI-KM Khaman Maluach — Phoenix Suns [RC]
CI-KO Kam Jones — Indiana Pacers [RC]
CI-LM Liam McNeeley — Charlotte Hornets [RC]
CI-MP Micah Peavy — New Orleans Pelicans [RC]
CI-MR Maxime Raynaud — Sacramento Kings [RC]
CI-NC Nique Clifford — Sacramento Kings [RC]
CI-NE Noa Essengue — Chicago Bulls [RC]
CI-NP Noah Penda — Orlando Magic [RC]
CI-NT Nolan Traore — Brooklyn Nets [RC]
CI-RF Rasheer Fleming — Phoenix Suns [RC]
CI-RK Ryan Kalkbrenner — Charlotte Hornets [RC]
CI-SJ Sion James — Charlotte Hornets [RC]
CI-TA Tidjane Salaün — Charlotte Hornets
CI-TH Taylor Hendricks — Utah Jazz
CI-TP Tyrese Proctor — Cleveland Cavaliers [RC]
CI-TS Thomas Sorber — Oklahoma City Thunder [RC]
CI-WC Walter Clayton Jr. — Utah Jazz [RC]
CI-WR Will Riley — Washington Wizards [RC]
CI-YH Yang Hansen — Portland Trail Blazers [RC]
CI-YK Yanic Konan-Niederhäuser — Los Angeles Clippers [RC]
"""

# subset official name → checklist text
SUBSETS = [
    ("Utopia Highlights", UTOPIA),
    ("Jacked Up", JACKED_UP),
    ("LA Flame Legends", LFL),
    ("Astrovision", ASTRO),
    ("Cactus Mode", CACTUS_MODE),
    ("Base Autograph Variation", BASE_AUTO_VAR),
    ("Cactus Ink", CACTUS_INK),
]


def parse(text):
    """Yield (card_number, player_name, team, is_rookie)."""
    out = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        is_rc = False
        if line.endswith("[RC]"):
            is_rc = True
            line = line[:-4].strip()
        # split code from the rest on first whitespace
        code, _, rest = line.partition(" ")
        # split name/team on the em dash
        if "—" not in rest:
            raise ValueError(f"No em-dash in line: {raw!r}")
        name, _, team = rest.rpartition("—")
        out.append((code.strip(), name.strip(), team.strip(), is_rc))
    return out


def main():
    commit = "--commit" in sys.argv
    con = sqlite3.connect(DB)
    cur = con.cursor()

    set_id = cur.execute("SELECT id FROM sets WHERE slug=?", (SET_SLUG,)).fetchone()[0]

    # Resolve subset ids by name.
    sub_rows = cur.execute(
        "SELECT id, name FROM insert_sets WHERE set_id=?", (set_id,)
    ).fetchall()
    name_to_subid = {n: i for i, n in sub_rows}

    base_id = name_to_subid["Base Set"]

    # Existing set-scoped players: name → id.
    player_rows = cur.execute(
        "SELECT id, name FROM players WHERE set_id=?", (set_id,)
    ).fetchall()
    name_to_pid = {n: i for i, n in player_rows}

    # Plan accumulation.
    new_players = set()
    appearances = []  # (subset_id, card_number, name, team, is_rookie)

    def stage(subset_id, parsed):
        for code, name, team, rc in parsed:
            if name not in name_to_pid and name not in new_players:
                new_players.add(name)
            appearances.append((subset_id, code, name, team, 1 if rc else 0))

    base_parsed = parse(BASE)
    stage(base_id, base_parsed)
    for official_name, text in SUBSETS:
        sid = name_to_subid[official_name]
        stage(sid, parse(text))

    # Report counts.
    print(f"Set id: {set_id}  Base subset id: {base_id}")
    print(f"{'COMMIT' if commit else 'DRY RUN'}\n")
    print("Per-subset card counts to write:")
    print(f"  Base Set                  {len(base_parsed)}")
    for official_name, text in SUBSETS:
        print(f"  {official_name:<25} {len(parse(text))}")
    print(f"\nExisting set players: {len(name_to_pid)}")
    print(f"New players to create: {len(new_players)}")
    print(f"Total appearances to write: {len(appearances)}")

    # Phantom subsets: FLAG, do not touch.
    print("\nPHANTOM subsets (NOT modified — flagged, have parallels):")
    for pn in sorted(PHANTOM_NAMES):
        if pn in name_to_subid:
            sid = name_to_subid[pn]
            cards = cur.execute(
                "SELECT COUNT(*) FROM player_appearances WHERE insert_set_id=?", (sid,)
            ).fetchone()[0]
            pars = cur.execute(
                "SELECT COUNT(*) FROM parallels WHERE insert_set_id=?", (sid,)
            ).fetchone()[0]
            print(f"  {pn} (id {sid}): {cards} cards, {pars} parallels — LEFT INTACT")

    if not commit:
        print("\nDry run complete. Re-run with --commit to write.")
        con.close()
        return

    # ── Write ────────────────────────────────────────────────
    # Create new players (set-scoped). subject_role defaults to 'athlete'.
    for name in sorted(new_players):
        cur.execute(
            "INSERT INTO players (set_id, name, subject_role) VALUES (?, ?, 'athlete')",
            (set_id, name),
        )
        name_to_pid[name] = cur.lastrowid

    # Clear + rebuild base; populate the 7 shells (clear-first for idempotency).
    target_subset_ids = [base_id] + [name_to_subid[n] for n, _ in SUBSETS]
    for sid in target_subset_ids:
        cur.execute("DELETE FROM player_appearances WHERE insert_set_id=?", (sid,))

    for subset_id, code, name, team, rc in appearances:
        cur.execute(
            "INSERT INTO player_appearances "
            "(player_id, insert_set_id, card_number, is_rookie, subset_tag, team) "
            "VALUES (?, ?, ?, ?, '', ?)",
            (name_to_pid[name], subset_id, code, rc, team),
        )

    con.commit()
    print("\nCOMMITTED.")

    # Post-write verification.
    print("\nFinal per-subset counts:")
    rows = cur.execute(
        """SELECT ins.name, COUNT(pa.id)
           FROM insert_sets ins
           LEFT JOIN player_appearances pa ON pa.insert_set_id=ins.id
           WHERE ins.set_id=? GROUP BY ins.id ORDER BY ins.name""",
        (set_id,),
    ).fetchall()
    for n, c in rows:
        print(f"  {n:<28} {c}")
    con.close()
    print("\nNow run: npx tsx scripts/generate-slugs.ts && "
          "npx tsx scripts/recompute-unique-cards.ts")


if __name__ == "__main__":
    main()
