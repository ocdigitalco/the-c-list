import json
import re

# team is stored as empty string for UFC fighters — the DB column is NOT NULL,
# so null cannot be used; "" semantically represents "no team".

CHECKLIST_TEXT = """
2025 Topps Midnight UFC

Base Set
100 cards
Parallels

Zodiac
Morning /125
Twilight /99
Dusk /75
Moon Beam
Moonrise /25
Midnight /12
Daybreak /5
Black Light 1/1

1 Max Holloway
2 Sean Strickland
3 Khamzat Chimaev
4 Alexa Grasso
5 Paddy Pimblett
6 Bo Nickal
7 Yair Rodríguez
8 Erin Blanchfield
9 Payton Talbott RC
10 Georges St-Pierre
11 Ilia Topuria
12 Tom Aspinall
13 Dricus du Plessis
14 Raul Rosas
15 Conor McGregor
16 Sean O'Malley
17 Daniel Hooker
18 Jean Silva RC
19 Islam Makhachev
20 Virna Jandiroba
21 Nassourdine Imavov
22 Alex Pereira
23 Raquel Pennington
24 Anderson Silva
25 Sergei Pavlovich
26 Kayla Harrison
27 Rinya Nakamura RC
28 Jiri Prochazka
29 Ketlen Vieira
30 Colby Covington
31 Vinicius Oliveira RC
32 Hyunsung Park RC
33 Brandon Royval
34 Michael Page
35 Reinier de Ridder RC
36 Jack Della Maddalena
37 Volkan Oezdemir
38 Jéssica Andrade
39 Nate Landwehr RC
40 Christian Duncan RC
41 Shamil Gaziev RC
42 Maycee Barber
43 Zhang Weili
44 Jean Matsumoto RC
45 Yan Xiaonan
46 Assu Almabayev RC
47 Israel Adesanya
48 Kamaru Usman
49 Amir Albazi
50 Justin Gaethje
51 Sharabutdin Magomedov
52 Joshua Van RC
53 Tai Tuivasa
54 Benoit Saint Denis
55 Tatsuro Taira
56 Joaquin Buckley
57 Arman Tsarukyan
58 Mackenzie Dern
59 Jamahal Hill
60 Alexander Volkov
61 Shavkat Rakhmonov
62 Belal Muhammad
63 Myktybek Orolbai RC
64 Tabatha Ricci
65 Ciryl Gane
66 Michael Morales
67 Alexandre Pantoja
68 Tracy Cortez
69 Robert Whittaker
70 Merab Dvalishvili
71 Petr Yan
72 Daniel Zellhuber RC
73 Natalia Cristina Da Silva
74 Charles Oliveira
75 Rose Namajunas
76 Ian Machado Garry
77 Tatiana Suarez
78 Magomed Ankalaev
79 Jan Błachowicz
80 Ailin Perez RC
81 Manon Fiorot
82 Roman Kopylov RC
83 Valentina Shevchenko
84 Dustin Poirier
85 Leon Edwards
86 Stephen Thompson
87 Alexander Volkanovski
88 Julianna Peña
89 Stephen Erceg RC
90 Movsar Evloev
91 Caio Borralho
92 Khabib Nurmagomedov
93 Waldo Cortes RC
94 Michael Chandler
95 Umar Nurmagomedov
96 Kai Asakura RC
97 Chuck Liddell
98 Aljamain Sterling
99 Jon Jones
100 Diego Lopes

Autographs

Stroke of Midnight Autographs
21 cards
Parallels

Twilight /99 or less
Dusk /75 or less
Moon Beam
Moonrise /25 or less
Midnight /12 or less
Daybreak /5
Black Light 1/1

SMA-AP Alexandre Pantoja
SMA-BD Beneil Dariush
SMA-CU Carlos Ulberg
SMA-DC Dominick Cruz
SMA-GN Geoff Neal
SMA-IA Israel Adesanya
SMA-IG Ian Machado Garry
SMA-JA Jeffrey Molina
SMA-JG Justin Gaethje
SMA-JH Jack Hermansson
SMA-JL Jamahal Hill
SMA-JM Jake Matthews
SMA-JP Joe Pyfer
SMA-KK Karolina Kowalkiewicz
SMA-MD Mackenzie Dern
SMA-MT Marcin Tybura
SMA-RF Rafael Fiziev
SMA-RR Raul Rosas
SMA-SS Serghei Spivac
SMA-UF Urijah Faber
SMA-YX Yan Xiaonan

Glimmer Graphs
19 cards
Parallels

Twilight /99 or less
Dusk /75 or less
Moon Beam
Moonrise /25 or less
Midnight /12 or less
Daybreak /5
Black Light 1/1

GRG-AG Alexa Grasso
GRG-AS Anthony Smith
GRG-BM Belal Muhammad
GRG-CM Conor McGregor
GRG-CO Charles Oliveira
GRG-DH Dan Henderson
GRG-HH Holly Holm
GRG-JM Jack Della Maddalena
GRG-KC Khamzat Chimaev
GRG-KF Kai Kara-France
GRG-KH Kevin Holland
GRG-MB Mayra Bueno
GRG-MC Mark Coleman
GRG-MF Manon Fiorot
GRG-NM Neil Magny
GRG-PM Pedro Munhoz
GRG-RF Rob Font
GRG-RN Rich Franklin
GRG-SM Stipe Miocic

Horizon Signatures
60 cards
Parallels

Twilight /99 or less
Dusk /75 or less
Moon Beam
Moonrise /25 or less
Midnight /12 or less
Daybreak /5
Black Light 1/1

HNS-AN Antonio Rodrigo Nogueira
HNS-AT Arman Tsarukyan
HNS-AZ Aiemann Zahabi
HNS-BA Brian Ortega
HNS-BO Brandon Moreno
HNS-BR Bas Rutten
HNS-CC Colby Covington
HNS-CD Cody Durden
HNS-CG Cody Garbrandt
HNS-CK Calvin Kattar
HNS-CR Christian Rodriguez
HNS-CS Cory Sandhagen
HNS-CW Chris Weidman
HNS-DD Dricus Du Plessis
HNS-DH Daniel Hooker
HNS-DP Dustin Poirier
HNS-DR Dominick Reyes
HNS-FE Frankie Edgar
HNS-FM Frank Mir
HNS-GB Gilbert Burns
HNS-GC Giga Chikadze
HNS-HC Henry Cejudo
HNS-JB Javid Basharat
HNS-JD Junior Dos Santos
HNS-JE Josh Emmett
HNS-JJ Jon Jones
HNS-JM Jim Miller
HNS-JP Jiri Prochazka
HNS-JR Jens Pulver
HNS-JT Jalin Turner
HNS-JY Joaquin Buckley
HNS-KN Khabib Nurmagomedov
HNS-KS Ken Shamrock
HNS-LM Lyoto Machida
HNS-LY Lerone Murphy
HNS-MC Michael Chandler
HNS-ME Michael Page
HNS-MG Mateusz Gamrot
HNS-MH Matt Hughes
HNS-MO Movsar Evloev
HNS-MP Michel Pereira
HNS-MV Marvin Vettori
HNS-ND Nicolas Dalby
HNS-NK Nikita Krylov
HNS-PP Paddy Pimblett
HNS-RB Randy Brown
HNS-RD Rafael Dos Anjos
HNS-RE Rashad Evans
HNS-RF Rinat Fakhretdinov
HNS-RL Robbie Lawler
HNS-RN Rose Namajunas
HNS-RW Robert Whittaker
HNS-SR Shogun Rua
HNS-SW Sean Woodson
HNS-TC Tracy Cortez
HNS-TE Tim Elliott
HNS-TR Tabatha Ricci
HNS-VL Vicente Luque
HNS-VO Volkan Oezdemir
HNS-YS Yadong Song

Rookie Relic Autographs
35 cards
Parallels

Twilight /99 or less
Dusk /75 or less
Moon Beam
Moonrise /25 or less
Midnight /12 or less
Daybreak /5
Black Light 1/1

RRA-AP Ailin Perez
RRA-CJ Charles Jourdain
RRA-CM Jose Mariscal
RRA-DB Danny Barlow
RRA-DM Daniel Marcos
RRA-DZ Daniel Zellhuber
RRA-ER Esteban Ribovics
RRA-FB Farid Basharat
RRA-GB Gabriel Bonfim
RRA-HS Hyunsung Park
RRA-JB Joanderson Brito
RRA-JM Jonathan Martinez
RRA-JO Jean Matsumoto
RRA-JS Jean Silva
RRA-JV Joshua Van
RRA-MB Modestas Bukauskas
RRA-MM Marcus McGhee
RRA-MN Muhammadjon Naimov
RRA-MS Melissa Mullins
RRA-NL Nate Landwehr
RRA-NS Nazim Sadykhov
RRA-PT Payton Talbott
RRA-RB Rodolfo Bellato
RRA-RN Rinya Nakamura
RRA-TK Toshiomi Kazama
RRA-TP Trevor Peek
RRA-TW Trey Waters
RRA-VH Victor Henry
RRA-VO Vinicius Oliveira
RRA-VP Vitor Petrino
RRA-WC Waldo Cortes
RRA-WW Westin Wilson
RRR-CP Carlos Prates
RRR-KA Kai Asakura
RRR-RD Reinier de Ridder

Relic Autographs
23 cards
Parallels

Twilight /99 or less
Dusk /75 or less
Moon Beam
Moonrise /25 or less
Midnight /12 or less
Daybreak /5
Black Light 1/1

VRA-AP Alex Pereira
VRA-AR Aleksandar Rakic
VRA-BN Bo Nickal
VRA-CB Caio Borralho
VRA-DI Dan Ige
VRA-DL Diego Lopes
VRA-IM Islam Makhachev
VRA-IT Ilia Topuria
VRA-JP Julianna Peña
VRA-JW Johnny Walker
VRA-KH Kayla Harrison
VRA-LP Maria Godinez Gonzalez
VRA-MA Magomed Ankalaev
VRA-MH Max Holloway
VRA-MT Miesha Tate
VRA-PC Paul Craig
VRA-RD Roman Dolidze
VRA-SM Sharabutdin Magomedov
VRA-SO Sean O'Malley
VRA-SS Sean Strickland
VRA-ST Stephen Thompson
VRA-TA Tom Aspinall
VRA-VS Valentina Shevchenko

Inserts

Nightfall
25 cards
Parallels

Moon Beam
Dusk /75
Moonrise /25
Midnight /12
Daybreak /5
Black Light 1/1

NF-1 Arnold Allen
NF-2 Henry Cejudo
NF-3 Paddy Pimblett
NF-4 Raul Rosas
NF-5 Vinicius Oliveira
NF-6 Justin Gaethje
NF-7 Petr Yan
NF-8 Alex Pereira
NF-9 Alexandre Pantoja
NF-10 Jan Błachowicz
NF-11 Charles Oliveira
NF-12 Assu Almabayev
NF-13 Ian Machado Garry
NF-14 Kamaru Usman
NF-15 José Aldo
NF-16 Manon Fiorot
NF-17 Arman Tsarukyan
NF-18 Michael Page
NF-19 Dustin Poirier
NF-20 Maycee Barber
NF-21 Payton Talbott
NF-22 Alexander Volkanovski
NF-23 Jessica Andrade
NF-24 Stephen Erceg
NF-25 Kayla Harrison

Lunar Tide
20 cards
Parallels

Moon Beam
Dusk /75
Moonrise /25
Midnight /12
Daybreak /5
Black Light 1/1

LT-1 Umar Nurmagomedov
LT-2 Maycee Barber
LT-3 Mackenzie Dern
LT-4 Colby Covington
LT-5 Zhang Weili
LT-6 Shavkat Rakhmonov
LT-7 Valentina Shevchenko
LT-8 Israel Adesanya
LT-9 Tabatha Ricci
LT-10 Rose Namajunas
LT-11 Michael Morales
LT-12 Joanna Jędrzejczyk
LT-13 Sharabutdin Magomedov
LT-14 Belal Muhammad
LT-15 Max Holloway
LT-16 Paddy Pimblett
LT-17 Jessica Andrade
LT-18 Robert Whittaker
LT-19 Michael Chandler
LT-20 Reinier de Ridder

Constellations
20 cards
Parallels

Moon Beam
Dusk /75
Moonrise /25
Midnight /12
Daybreak /5
Black Light 1/1

CS-1 Jean Silva
CS-1 Caio Borralho
CS-2 Sean Strickland
CS-2 Alex Pereira
CS-3 Alexa Grasso
CS-3 Diego Lopes
CS-4 Charles Oliveira
CS-4 Alexandre Pantoja
CS-5 Umar Nurmagomedov
CS-5 Islam Makhachev
CS-6 Tecia Pennington
CS-6 Raquel Pennington
CS-7 Merab Dvalishvili
CS-7 Ilia Topuria
CS-8 Conor McGregor
CS-8 José Aldo
CS-9 Jon Jones
CS-9 Tom Aspinall
CS-10 Rinya Nakamura
CS-10 Tatsuro Taira

The One and Only
20 cards
Parallels

Moon Beam
Dusk /75
Moonrise /25
Midnight /12
Daybreak /5
Black Light 1/1

OO-1 Leon Edwards
OO-2 Arman Tsarukyan
OO-3 Paul Craig
OO-4 Daniel Cormier
OO-5 Islam Makhachev
OO-6 Jack Della Maddalena
OO-7 Tom Aspinall
OO-8 Dustin Poirier
OO-9 Khamzat Chimaev
OO-10 Conor McGregor
OO-11 Paulo Costa
OO-12 Colby Covington
OO-13 Sean Strickland
OO-14 Jamahal Hill
OO-15 Erin Blanchfield
OO-16 Kevin Holland
OO-17 Alexander Volkanovski
OO-18 Tatsuro Taira
OO-19 Caio Borralho
OO-20 Virna Jandiroba

Insomnia
25 cards
Parallels

Moon Beam
Dusk /75
Moonrise /25
Midnight /12
Daybreak /5
Black Light 1/1

IN-1 Bo Nickal
IN-2 Valentina Shevchenko
IN-3 Sharabutdin Magomedov
IN-4 Michael Chandler
IN-5 Sean O'Malley
IN-6 Jiri Prochazka
IN-7 Raquel Pennington
IN-8 Ikram Aliskerov
IN-9 Jean Matsumoto
IN-10 Aljamain Sterling
IN-11 Diego Lopes
IN-12 Stipe Miocic
IN-13 Henry Cejudo
IN-14 Alexandre Pantoja
IN-15 Kamaru Usman
IN-16 Brian Ortega
IN-17 Yan Xiaonan
IN-18 Alexa Grasso
IN-19 Joshua Van
IN-20 Gilbert Burns
IN-21 Raul Rosas
IN-22 Julianna Peña
IN-23 Rinya Nakamura
IN-24 Ilia Topuria
IN-25 Tatiana Suarez

Dream Chasers
30 cards
Parallels

Daybreak /5
Black Light 1/1

DC-1 Rinya Nakamura
DC-2 Jean Silva
DC-3 Bo Nickal
DC-4 Virna Jandiroba
DC-5 Michael Morales
DC-6 Erin Blanchfield
DC-7 Vinicius Oliveira
DC-8 Jean Matsumoto
DC-9 Ian Machado Garry
DC-10 Khamzat Chimaev
DC-11 Tatiana Suarez
DC-12 Umar Nurmagomedov
DC-13 Payton Talbott
DC-14 Reinier de Ridder
DC-15 Joshua Van
DC-16 Diego Lopes
DC-17 Stephen Erceg
DC-18 Kayla Harrison
DC-19 Myktybek Orolbai
DC-20 Raul Rosas
DC-21 Magomed Ankalaev
DC-22 Tabatha Ricci
DC-23 Caio Borralho
DC-24 Shavkat Rakhmonov
DC-25 Paddy Pimblett
DC-26 Hyunsung Park
DC-27 Movsar Evloev
DC-28 Christian Duncan
DC-29 Tatsuro Taira
DC-30 Assu Almabayev

Greetings From
25 cards
Parallels

Daybreak /5
Black Light 1/1

GF-1 Payton Talbott
GF-2 Rose Namajunas
GF-3 Dricus du Plessis
GF-4 Sean O'Malley
GF-5 Jon Jones
GF-6 Dustin Poirier
GF-7 Tom Aspinall
GF-8 Ilia Topuria
GF-9 Max Holloway
GF-10 Alex Pereira
GF-11 Julianna Peña
GF-12 Kamaru Usman
GF-13 Charles Oliveira
GF-14 Merab Dvalishvili
GF-15 Israel Adesanya
GF-16 Zhang Weili
GF-17 Islam Makhachev
GF-18 Khabib Nurmagomedov
GF-19 Belal Muhammad
GF-20 Valentina Shevchenko
GF-21 Michael Chandler
GF-22 Sean Strickland
GF-23 Alexa Grasso
GF-24 Alexander Volkanovski
GF-25 Conor McGregor

Twilight
20 cards
Parallels

Daybreak /5
Black Light 1/1

TL-1 Rose Namajunas
TL-2 Sharabutdin Magomedov
TL-3 Shavkat Rakhmonov
TL-4 Dricus du Plessis
TL-5 Umar Nurmagomedov
TL-6 Joanna Jędrzejczyk
TL-7 Tom Aspinall
TL-8 Islam Makhachev
TL-9 Chuck Liddell
TL-10 Sean Strickland
TL-11 Alex Pereira
TL-12 Max Holloway
TL-13 Ilia Topuria
TL-14 Conor McGregor
TL-15 Sean O'Malley
TL-16 Anderson Silva
TL-17 Diego Lopes
TL-18 Merab Dvalishvili
TL-19 Kayla Harrison
TL-20 Charles Oliveira

Night Vision
25 cards
Parallels

Daybreak /5
Black Light 1/1

NV-1 Valentina Shevchenko
NV-2 Mackenzie Dern
NV-3 Yan Xiaonan
NV-4 Jan Błachowicz
NV-5 Manon Fiorot
NV-6 Belal Muhammad
NV-7 Raquel Pennington
NV-8 Israel Adesanya
NV-9 Alexa Grasso
NV-10 Julianna Peña
NV-11 Sean O'Malley
NV-12 Jiri Prochazka
NV-13 Colby Covington
NV-14 Khamzat Chimaev
NV-15 Zhang Weili
NV-16 Alexandre Pantoja
NV-17 Georges St-Pierre
NV-18 Maycee Barber
NV-19 Justin Gaethje
NV-20 Sharabutdin Magomedov
NV-21 Jon Jones
NV-22 Khabib Nurmagomedov
NV-23 Jéssica Andrade
NV-24 Bo Nickal
NV-25 Leon Edwards
"""


def parse_print_run(text):
    """Extract serialized print run. Returns None for unnumbered or negative values."""
    m = re.search(r"/(-?\d+)", text)
    if m:
        n = int(m.group(1))
        return n if n > 0 else None
    return None


def parse_parallel_name(text):
    """Return clean parallel name: strip N/N or /N suffix and parenthetical descriptions."""
    name = re.sub(r"\s*\([^)]*\)", "", text)      # strip parentheticals
    name = re.sub(r"\s*\d*/[-]?\d+\b.*", "", name)  # strip N/N or /N suffix
    return name.strip()


def parse_section(lines, start_idx):
    """
    Parse one section starting at start_idx (the section name line).
    Returns (section_data, next_idx).

    Constellations lists two fighters on separate lines with the same card number.
    These are parsed as individual card entries — both fighters end up with their
    own appearance for that card number in the player index (no special handling
    needed beyond the standard per-line card parse).
    """
    section_name = lines[start_idx].strip()
    idx = start_idx + 1

    # Skip card count line(s)
    while idx < len(lines) and re.match(r"^\d+ cards?$", lines[idx].strip()):
        idx += 1

    # Parse parallels block
    parallels = []
    in_parallels = False
    while idx < len(lines):
        line = lines[idx].strip()

        if not line:
            idx += 1
            continue

        if line.lower() in ("parallels", "parallel"):
            in_parallels = True
            idx += 1
            continue

        if in_parallels:
            # Card line signals end of parallels block
            if re.match(r"^[A-Z0-9]+-[A-Z0-9]+\s|^\d+\s", line):
                break
            parallels.append({
                "name": parse_parallel_name(line),
                "print_run": parse_print_run(line),
            })
            idx += 1
        else:
            # Before "Parallels" keyword: stop if we hit a card line or anything else
            if re.match(r"^[A-Z0-9]+-[A-Z0-9]+\s|^\d+\s", line):
                break
            break

    # Parse cards
    cards = []
    while idx < len(lines):
        line = lines[idx].strip()

        if not line:
            idx += 1
            continue

        # Detect start of next section: current line is the section name and
        # the next non-empty line is "N cards"
        if idx + 1 < len(lines) and re.match(r"^\d+ cards?$", lines[idx + 1].strip()):
            break

        # Card line: prefixed by an alphanumeric code (e.g. "1", "SMA-AP", "CS-1")
        card_match = re.match(
            r"^([A-Z0-9]+-[A-Z0-9A-Za-z0-9]*|\d+)\s+(.+)",
            line,
        )
        if card_match:
            card_number = card_match.group(1)
            rest = card_match.group(2).strip()

            # RC designation
            is_rookie = bool(re.search(r"\bRC\b", rest))
            rest = re.sub(r"\s+RC\b", "", rest).strip()

            cards.append({
                "card_number": card_number,
                "player": rest,
                "team": "",   # UFC fighters have no team affiliation
                "is_rookie": is_rookie,
                "subset": None,
            })

        idx += 1

    return {"insert_set": section_name, "parallels": parallels, "cards": cards}, idx


def parse_checklist(text):
    lines = text.split("\n")
    sections = []
    idx = 0

    while idx < len(lines):
        line = lines[idx].strip()
        if not line:
            idx += 1
            continue

        # Section header detected by "N cards" on the next non-empty line
        peek = idx + 1
        while peek < len(lines) and not lines[peek].strip():
            peek += 1

        if peek < len(lines) and re.match(r"^\d+ cards?$", lines[peek].strip()):
            section, idx = parse_section(lines, idx)
            if section["cards"]:
                sections.append(section)
        else:
            idx += 1

    return sections


def compute_stats(appearances):
    unique_cards = 0
    total_print_run = 0
    one_of_ones = 0

    for appearance in appearances:
        unique_cards += 1  # base card counts as 1
        for parallel in appearance["parallels"]:
            unique_cards += 1
            if parallel["print_run"] is not None:
                total_print_run += parallel["print_run"]
                if parallel["print_run"] == 1:
                    one_of_ones += 1

    return {
        "unique_cards": unique_cards,
        "total_print_run": total_print_run,
        "one_of_ones": one_of_ones,
        "insert_sets": len(appearances),
    }


def build_output(sections):
    # Collect all players who are rookies in any section (propagate to all appearances)
    rc_players = set()
    for section in sections:
        for card in section["cards"]:
            if card.get("is_rookie"):
                rc_players.add(card["player"])

    player_index = {}

    for section in sections:
        for card in section["cards"]:
            player = card["player"]
            if player not in player_index:
                player_index[player] = {"player": player, "appearances": []}
            player_index[player]["appearances"].append({
                "insert_set": section["insert_set"],
                "card_number": card["card_number"],
                "team": card["team"],
                "is_rookie": card["player"] in rc_players,
                "subset_tag": card["subset"],
                "parallels": section["parallels"],
            })

    players = []
    for player_name in sorted(player_index.keys()):
        data = player_index[player_name]
        stats = compute_stats(data["appearances"])
        players.append({
            "player": player_name,
            "appearances": data["appearances"],
            "stats": stats,
        })

    return {
        "set_name": "2025 Topps Midnight UFC",
        "sport": "MMA",
        "season": "2025",
        "league": "UFC",
        "sections": sections,
        "players": players,
    }


if __name__ == "__main__":
    print("Parsing 2025 Topps Midnight UFC checklist...")
    sections = parse_checklist(CHECKLIST_TEXT)
    print(f"Raw sections found: {len(sections)}")

    output = build_output(sections)

    with open("ufc_midnight_parsed.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nSet: {output['set_name']} ({output['season']})")
    print(f"Sections: {len(output['sections'])}")
    for s in output["sections"]:
        print(f"  {s['insert_set']}: {len(s['cards'])} cards, {len(s['parallels'])} parallels")
    print(f"Players: {len(output['players'])}")

    # Spot-check: Jon Jones should appear across multiple sections
    if "Jon Jones" in {p["player"] for p in output["players"]}:
        jones = next(p for p in output["players"] if p["player"] == "Jon Jones")
        print(f"\n=== Jon Jones ===")
        print(f"  Insert sets:     {jones['stats']['insert_sets']}")
        print(f"  Unique cards:    {jones['stats']['unique_cards']}")
        print(f"  Total print run: {jones['stats']['total_print_run']}")
        print(f"  1/1s:            {jones['stats']['one_of_ones']}")
        for a in jones["appearances"]:
            print(f"  {a['insert_set']} — {a['card_number']} ({len(a['parallels'])} parallels)")

    # Spot-check: Constellations CS-1 should have two fighters
    constellations = next(
        (s for s in output["sections"] if s["insert_set"] == "Constellations"), None
    )
    if constellations:
        cs1_cards = [c for c in constellations["cards"] if c["card_number"] == "CS-1"]
        print(f"\nConstellations CS-1 fighters: {[c['player'] for c in cs1_cards]}")

    print(f"\nSaved to ufc_midnight_parsed.json")
