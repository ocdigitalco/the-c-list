import json
import re

# team is stored as empty string for UFC fighters — the DB column is NOT NULL,
# so null cannot be used; "" semantically represents "no team".

CHECKLIST_TEXT = """
2024 Topps Midnight UFC

Base Set
100 cards.

Parallels:

Morning – /125 (1:3 packs)
Twilight – /99 (1:3 packs)
Dusk – /75 (1:4 packs)
Moon Beam – (1:6 packs)
Moonrise – /25 (1:11 packs)
Midnight – /12 (1:23 packs)
Daybreak – /5 (1:54 packs)
Black Light – 1/1 (1:262 packs)

1 Conor McGregor
2 Nuerdanbieke Shayilan RC
3 Julianna Peña
4 Robert Whittaker
5 Kamaru Usman
6 Movsar Evloev
7 Charles Oliveira
8 Alexandre Pantoja
9 Brandon Moreno
10 Jasmine Jasudavicius RC
11 Jonny Parsons RC
12 Dricus Du Plessis
13 Ian Machado Garry
14 Manel Kape RC
15 Cameron Saaiman RC
16 Stipe Miocic
17 Erin Blanchfield
18 Jan Błachowicz
19 Ode Osbourne RC
20 Petr Yan
21 Derrick Lewis
22 Jack Jenkins RC
23 Henry Cejudo
24 Shavkat Rakhmonov
25 Chuck Liddell
26 Diego Lopes RC
27 Chelsea Chandler RC
28 Sean Strickland
29 Josh Quinlan RC
30 Mackenzie Dern
31 Sean O'Malley
32 Jack Della Maddalena
33 Jake Hadley RC
34 Tom Aspinall
35 Amanda Nunes
36 Jamie Pickett RC
37 Alexander Volkanovski
38 Gilbert Burns
39 Da'Mon Blackshear RC
40 Montserrat Conejo RC
41 Valentina Shevchenko
42 Justin Gaethje
43 Gabriel Miranda RC
44 Dustin Poirier
45 Islam Makhachev
46 Deiveson Figueiredo
47 Natalia Cristina da Silva RC
48 Merab Dvalishvili
49 Sergei Pavlovich
50 Khabib Nurmagomedov

51 Ciryl Gane
52 Umar Nurmagomedov
53 Brad Katona RC
54 Khamzat Chimaev
55 Alex Pereira
56 Melquizael Conceição RC
57 Shara Magomedov RC
58 Leon Edwards
59 Iasmin Lucindo RC
60 Yair Rodríguez
61 Manon Fiorot
62 Inoue Mizuki RC
63 Tatsuro Taira
64 Yazmin Jauregui RC
65 Fernando Padilla RC
66 Michael Chandler
67 Israel Adesanya
68 Bo Nickal
69 Val Woodburn RC
70 Muhammad Mokaev
71 Jamahal Hill
72 Magomed Ankalaev
73 Jailton Almeida
74 William Gomis RC
75 Georges St-Pierre
76 Aiemann Zahabi RC
77 Max Holloway
78 Armen Petrosyan RC
79 Choi SeungWoo RC
80 Benoit Saint-Denis RC
81 Alexa Grasso
82 Ilia Topuria
83 Brady Hiestand RC
84 Junior Tafa RC
85 Raul Rosas
86 Zhang Weili
87 Paddy Pimblett
88 Malcolm Gordon RC
89 Luana Carolina RC
90 Yan Xiaonan
91 Arnold Allen
92 Elves Brener RC
93 Colby Covington
94 Mayra Bueno
95 Brunno Ferreira RC
96 Aljamain Sterling
97 Jiri Prochazka
98 Arman Tsarukyan
99 Themba Gorimbo RC
100 Jon Jones

Autographs

Glimmer Graphs Checklist
30 cards.
1:5 packs.

Parallels:

Twilight – /99 or less (1:9 packs)
Moon Beam – /49 or less (1:19 packs)
Moonrise – /25 or less (1:37 packs)
Midnight – /12 or less (1:72 packs)
Daybreak – /5 (1:171 packs)
Black Light – 1/1 (1:847 packs)

GG-ANS Amanda Nunes
GG-APA Alex Pereira
GG-BMD Belal Muhammad
GG-CLL Chuck Liddell
GG-COA Charles Oliveira
GG-DCR Daniel Cormier
GG-FGN Forrest Griffin
GG-GBS Gilbert Burns
GG-GSP Georges St-Pierre
GG-IGY Ian Machado Garry
GG-JET Josh Emmett
GG-JPA Jiri Prochazka
GG-KKF Kai Kara-France
GG-KMV Khabib Nurmagomedov
GG-LES Leon Edwards
GG-MDN Mackenzie Dern
GG-MGT Mateusz Gamrot
GG-MHY Max Holloway
GG-MMN Molly McCann
GG-MVA Marlon Vera
GG-PPT Paddy Pimblett
GG-RGE Royce Gracie
GG-RLR Robbie Lawler
GG-RRS Raul Rosas
GG-SMC Stipe Miocic
GG-TAL Tom Aspinall
GG-TOZ Tito Ortiz
GG-UMV Umar Nurmagomedov
GG-VLE Vicente Luque
GG-YXN Yan Xiaonan

Horizon Signatures Checklist
63 cards.
1:3 packs.

Parallels:

Twilight – /99 or less (1:5 packs)
Moon Beam – /49 or less (1:9 packs)
Moonrise – /25 or less (1:17 packs)
Midnight – /12 or less (1:34 packs)
Daybreak – /5 (1:82 packs)
Black Light – 1/1 (1:404 packs)

HS-AAI Amir Albazi
HS-ALS Amanda Lemos
HS-APA Alexandre Pantoja
HS-AVV Alexander Volkov
HS-AZI Aiemann Zahabi
HS-BAN Brendan Allen
HS-BBE Bryan Battle
HS-BDH Beneil Dariush
HS-BFA Brunno Ferreira
HS-BKA Brad Katona
HS-BMO Brandon Moreno
HS-CCR Chelsea Chandler
HS-CKR Calvin Kattar
HS-CSJ Chan Sung Jung
HS-CSN Cory Sandhagen
HS-CUG Carlos Ulberg
HS-DHN Dan Henderson
HS-DLS Diego Lopes
HS-DRS Dominick Reyes
HS-EBR Elves Brener
HS-FDA Fernando Padilla
HS-FMR Frank Mir
HS-GNL Geoff Neal
HS-GTA Glover Teixeira
HS-HHM Holly Holm
HS-ILO Iasmin Lucindo
HS-JDM Jack Della Maddalena
HS-JHL Jamahal Hill
HS-JJK Joanna Jędrzejczyk
HS-JJS Jasmine Jasudavicius
HS-JPA Julianna Peña
HS-JPR Jens Pulver
HS-JPS Jonny Parsons
HS-JQN Josh Quinlan
HS-JRK Jair Rozenstruik
HS-JWR Johnny Walker
HS-JWS Jeremiah Wells
HS-LCA Luana Carolina
HS-LRD Luke Rockhold
HS-MAV Magomed Ankalaev
HS-MBG Michael Bisping
HS-MBR Maycee Barber
HS-MCA Melquizael Conceição
HS-MEV Movsar Evloev
HS-MIE Inoue Mizuki
HS-MMS Michael Morales
HS-MVI Marvin Vettori
HS-NMY Neil Magny
HS-OOE Ode Osbourne
HS-PPR Parker Porter
HS-RFV Rafael Fiziev
HS-RWR Robert Whittaker
HS-SNE Nuerdanbieke Shayilan
HS-SRV Shavkat Rakhmonov
HS-SWC Choi SeungWoo
HS-TFN Tony Ferguson
HS-TSS Taila Santos
HS-TTA Tatsuro Taira
HS-UFR Urijah Faber
HS-VWN Val Woodburn
HS-WGS William Gomis
HS-WSA Wanderlei Silva
HS-YJI Yazmin Jauregui

Relic Autographs Checklist
28 cards.
1:2 packs.

Parallels:

Twilight – /99 or less (1:10 packs)
Moon Beam – /49 or less (1:19 packs)
Moonrise – /25 or less (1:37 packs)
Midnight – /12 or less (1:77 packs)
Daybreak – /5 (1:183 packs)
Black Light – 1/1 (1:908 packs)

RCA-AGR Alexa Grasso
RCA-APA Alexandre Pantoja
RCA-APE Alex Pereira
RCA-APN Armen Petrosyan
RCA-AST Aljamain Sterling
RCA-AVO Alexander Volkanovski
RCA-BHD Brady Hiestand
RCA-BMU Belal Muhammad
RCA-BSD Benoit Saint-Denis
RCA-CCO Colby Covington
RCA-EBL Erin Blanchfield
RCA-IMA Islam Makhachev
RCA-JAL Jailton Almeida
RCA-JBL Jan Błachowicz
RCA-JHA Jake Hadley
RCA-JHI Jamahal Hill
RCA-JTA Junior Tafa
RCA-LES Leon Edwards
RCA-MCH Michael Chandler
RCA-MKA Manel Kape
RCA-MMO Muhammad Mokaev
RCA-RDO Roman Dolidze
RCA-SOM Sean O'Malley
RCA-SSP Serghei Spivac
RCA-TGO Themba Gorimbo
RCA-TSU Tatiana Suarez
RCA-VSH Valentina Shevchenko
RCA-YRO Yair Rodríguez

Stroke of Midnight Autographs Checklist
54 cards.
1:2 packs.

Parallels:

Twilight – /99 or less (1:7 packs)
Moon Beam – /49 or less (1:10 packs)
Moonrise – /25 or less (1:20 packs)
Midnight – /12 or less (1:40 packs)
Daybreak – /5 (1:95 packs)
Black Light – 1/1 (1:471 packs)

SMA-AAN Arnold Allen
SMA-ANS Anderson Silva
SMA-ARC Aleksandar Rakic
SMA-ARN Antonio Rodrigo Nogueira
SMA-ASH Anthony Smith
SMA-AZI Aiemann Zahabi
SMA-BJP BJ Penn
SMA-BOA Brian Ortega
SMA-BRL Brandon Royval
SMA-BRN Bas Rutten
SMA-CBO Caio Borralho
SMA-CBS Curtis Blaydes
SMA-CGE Ciryl Gane
SMA-CSA Cameron Saaiman
SMA-CSN Chael Sonnen
SMA-CWN Chris Weidman
SMA-DCE Donald Cerrone
SMA-DCZ Dominick Cruz
SMA-DHR Dan Hooker
SMA-DIE Dan Ige
SMA-FER Frankie Edgar
SMA-FSK Frank Shamrock
SMA-GCE Giga Chikadze
SMA-HCO Henry Cejudo
SMA-IAA Irene Aldana
SMA-JAE Jessica Andrade
SMA-JAO José Aldo
SMA-JPR Joe Pyfer
SMA-JSE Jack Shore
SMA-JTR Jalin Turner
SMA-KCN Katlyn Cerminara
SMA-KHD Kevin Holland
SMA-LMA Lyoto Machida
SMA-MCN Mark Coleman
SMA-MDI Merab Dvalishvili
SMA-MMT Mike Malott
SMA-MNU Matheus Nicolau
SMA-MTA Marcin Tybura
SMA-NLY Natan Levy
SMA-PMZ Pedro Munhoz
SMA-RDA Rafael Dos Anjos
SMA-RES Rashad Evans
SMA-RFT Rob Font
SMA-RNS Rose Namajunas
SMA-RPN Raquel Pennington
SMA-RSN Ryan Spann
SMA-STN Stephen Thompson
SMA-TPO Tyson Pedro
SMA-TRI Tabatha Ricci
SMA-TTA Tai Tuivasa
SMA-TWY Tyron Woodley
SMA-VOR Volkan Oezdemir
SMA-YDS Yadong Song
SMA-YJI Yazmin Jauregui

Inserts

After Hours Checklist
25 cards.
1:64 packs.

Parallels:

Daybreak – /5 (1:210 packs)
Black Light – 1/1 (1:1,016 packs)

AH-1 Deiveson Figueiredo
AH-2 Bo Nickal
AH-3 Tito Ortiz
AH-4 Shavkat Rakhmonov
AH-5 Conor McGregor
AH-6 Daniel Cormier
AH-7 Anderson Silva
AH-8 Khabib Nurmagomedov
AH-9 Tatsuro Taira
AH-10 Ian Machado Garry
AH-11 Charles Oliveira
AH-12 Amanda Nunes
AH-13 Tom Aspinall
AH-14 Mayra Bueno
AH-15 Israel Adesanya
AH-16 Erin Blanchfield
AH-17 Gilbert Burns
AH-18 Alexander Volkanovski
AH-19 Ilia Topuria
AH-20 Henry Cejudo
AH-21 Muhammad Mokaev
AH-22 Jon Jones
AH-23 Diego Lopes
AH-24 Valentina Shevchenko
AH-25 Sean O'Malley

Constellations Checklist
25 cards.
1:5 packs.

Parallels:

Twilight – /99 (1:11 packs)
Moon Beam – (1:31 packs)
Moonrise – /25 (1:43 packs)
Midnight – /12 (1:89 packs)
Daybreak – /5 (1:210 packs)
Black Light – 1/1 (1:1,016 packs)

CO-1 Khabib Nurmagomedov / Islam Makhachev
CO-2 Anderson Silva / Israel Adesanya
CO-3 Brian Ortega / Max Holloway
CO-4 Amanda Nunes / Mayra Bueno
CO-5 Henry Cejudo / Deiveson Figueiredo
CO-6 Dominick Cruz / Sean O'Malley
CO-7 Leon Edwards / Kamaru Usman
CO-8 Dustin Poirier / Jens Pulver
CO-9 Tony Ferguson / Charles Oliveira
CO-10 Jon Jones / Daniel Cormier
CO-11 Chael Sonnen / Justin Gaethje
CO-12 Mohammed Usman / Kamaru Usman
CO-13 Justin Tafa / Junior Tafa
CO-14 Ken Shamrock / Frank Shamrock
CO-15 Stephen Thompson / Chris Weidman
CO-16 Tai Tuivasa / Tyson Pedro
CO-17 Yan Xiaonan / Zhang Weili
CO-18 Kai Kara-France / Alexander Volkanovski
CO-19 Merab Dvalishvili / Aljamain Sterling
CO-20 T.J. Dillashaw / Cody Garbrandt
CO-21 Alex Pereira / Glover Teixeira
CO-22 Valentina Shevchenko / Alexa Grasso
CO-23 Ian Machado Garry / Conor McGregor
CO-24 Alexander Volkanovski / Israel Adesanya
CO-25 Conor McGregor / Khabib Nurmagomedov

Dream Chasers Checklist
30 cards.
1:53 packs.

Parallels:

Daybreak – /5 (1:176 packs)
Black Light – 1/1 (1:847 packs)

DC-1 Paddy Pimblett
DC-2 Bo Nickal
DC-3 Jack Della Maddalena
DC-4 Ian Machado Garry
DC-5 Jailton Almeida
DC-6 Erin Blanchfield
DC-7 Raul Rosas
DC-8 Muhammad Mokaev
DC-9 Roman Dolidze
DC-10 Shavkat Rakhmonov
DC-11 Tom Aspinall
DC-12 Umar Nurmagomedov
DC-13 Manon Fiorot
DC-14 Sergei Pavlovich
DC-15 Magomed Ankalaev
DC-16 Dricus Du Plessis
DC-17 Khamzat Chimaev
DC-18 Mateusz Gamrot
DC-19 Gilbert Burns
DC-20 Carlos Ulberg
DC-21 Rafael Fiziev
DC-22 Ilia Topuria
DC-23 Amir Albazi
DC-24 Mayra Bueno
DC-25 Tatsuro Taira
DC-26 Taila Santos
DC-27 Arman Tsarukyan
DC-28 Jack Shore
DC-29 Shara Magomedov
DC-30 Maycee Barber

Lunar Tide Checklist
15 cards.
1:9 packs.

Parallels:

Twilight – /99 (1:18 packs)
Moon Beam – (1:52 packs)
Moonrise – /25 (1:71 packs)
Midnight – /12 (1:146 packs)
Daybreak – /5 (1:348 packs)
Black Light – 1/1 (1:1,694 packs)

LT-1 Rose Namajunas
LT-2 Stipe Miocic
LT-3 Ilia Topuria
LT-4 Petr Yan
LT-5 Umar Nurmagomedov
LT-6 Raquel Pennington
LT-7 Jon Jones
LT-8 Molly McCann
LT-9 Jiri Prochazka
LT-10 Yair Rodríguez
LT-11 Max Holloway
LT-12 Sean O'Malley
LT-13 Ciryl Gane
LT-14 Khamzat Chimaev
LT-15 Taila Santos

Moonfall Checklist
25 cards.
1:64 packs.

Parallels:

Daybreak – /5 (1:210 packs)
Black Light – 1/1 (1:1,016 packs)

MF-1 Jon Jones
MF-2 Conor McGregor
MF-3 Islam Makhachev
MF-4 Khabib Nurmagomedov
MF-5 Valentina Shevchenko
MF-6 Kamaru Usman
MF-7 Georges St-Pierre
MF-8 Anderson Silva
MF-9 Sean O'Malley
MF-10 Alexander Volkanovski
MF-11 Tom Aspinall
MF-12 Sean Strickland
MF-13 Amanda Nunes
MF-14 Israel Adesanya
MF-15 Alex Pereira
MF-16 Jamahal Hill
MF-17 Jiri Prochazka
MF-18 Alexa Grasso
MF-19 Khamzat Chimaev
MF-20 Leon Edwards
MF-21 Max Holloway
MF-22 Justin Gaethje
MF-23 Charles Oliveira
MF-24 Alexandre Pantoja
MF-25 Zhang Weili

Night Stars Checklist
30 cards.
1:5 packs.

Parallels:

Twilight – /99 (1:9 packs)
Moon Beam – (1:26 packs)
Moonrise – /25 (1:36 packs)
Midnight – /12 (1:74 packs)
Daybreak – /5 (1:176 packs)
Black Light – 1/1 (1:847 packs)

NS-1 Amanda Nunes
NS-2 Caio Borralho
NS-3 Derrick Lewis
NS-4 Mackenzie Dern
NS-5 Irene Aldana
NS-6 Justin Gaethje
NS-7 Magomed Ankalaev
NS-8 Belal Muhammad
NS-9 Gilbert Burns
NS-10 Jessica Andrade
NS-11 Manel Kape
NS-12 Rafael Fiziev
NS-13 Tabatha Ricci
NS-14 Jalin Turner
NS-15 Paulo Costa
NS-16 Chan Sung Jung
NS-17 Geoff Neal
NS-18 Holly Holm
NS-19 Joe Pyfer
NS-20 Brian Ortega
NS-21 Kamaru Usman
NS-22 Julianna Peña
NS-23 Maria Godinez Gonzalez
NS-24 Charles Oliveira
NS-25 Jasmine Jasudavicius
NS-26 Paddy Pimblett
NS-27 Arnold Allen
NS-28 Dustin Poirier
NS-29 Colby Covington
NS-30 Brandon Moreno

The One and Only Checklist
30 cards.
1:5 packs.

Parallels:

Twilight – /99 (1:9 packs)
Moon Beam – (1:26 packs)
Moonrise – /25 (1:36 packs)
Midnight – /12 (1:74 packs)
Daybreak – /5 (1:176 packs)
Black Light – 1/1 (1:847 packs)

TO-1 Khamzat Chimaev
TO-2 Jamahal Hill
TO-3 Israel Adesanya
TO-4 Kamaru Usman
TO-5 Bo Nickal
TO-6 Chuck Liddell
TO-7 Mayra Bueno
TO-8 Alexander Volkanovski
TO-9 Tai Tuivasa
TO-10 Michael Bisping
TO-11 Khabib Nurmagomedov
TO-12 Sean O'Malley
TO-13 Tito Ortiz
TO-14 Islam Makhachev
TO-15 Forrest Griffin
TO-16 Valentina Shevchenko
TO-17 Manon Fiorot
TO-18 Justin Gaethje
TO-19 Conor McGregor
TO-20 Dan Hooker
TO-21 Robert Whittaker
TO-22 Wanderlei Silva
TO-23 Yan Xiaonan
TO-24 Robbie Lawler
TO-25 Sean Strickland
TO-26 Alexa Grasso
TO-27 Jon Jones
TO-28 Zhang Weili
TO-29 Cory Sandhagen
TO-30 Tom Aspinall

Twilight Checklist
20 cards.
1:80 packs.

Parallels:

Daybreak – /5 (1:262 packs)
Black Light – 1/1 (1:1,270 packs)

TT-1 Conor McGregor
TT-2 Sean O'Malley
TT-3 Dustin Poirier
TT-4 Alexa Grasso
TT-5 Georges St-Pierre
TT-6 Jailton Almeida
TT-7 Ian Machado Garry
TT-8 Zhang Weili
TT-9 Israel Adesanya
TT-10 Valentina Shevchenko
TT-11 Michael Chandler
TT-12 Alex Pereira
TT-13 Bo Nickal
TT-14 Jon Jones
TT-15 Jiri Prochazka
TT-16 Khamzat Chimaev
TT-17 Colby Covington
TT-18 Khabib Nurmagomedov
TT-19 Mackenzie Dern
TT-20 Alexander Volkanovski
"""


def parse_print_run(text):
    """Extract serialized print run. Returns None for unnumbered or negative values."""
    m = re.search(r"/(-?\d+)", text)
    if m:
        n = int(m.group(1))
        return n if n > 0 else None
    return None


def parse_parallel_name(text):
    """Return clean parallel name: strip em/en dashes, N/N or /N suffixes,
    'or less' qualifiers, and parenthetical descriptions."""
    name = re.sub(r"\s*\([^)]*\)", "", text)        # strip parentheticals like "(1:3 packs)"
    name = re.sub(r"\s*\d*/[-]?\d+\b.*", "", name)  # strip N/N or /N suffix (and anything after)
    name = re.sub(r"\s*[–—-]+\s*$", "", name)        # strip trailing em/en/regular dashes
    return name.strip()


def is_skip_line(line):
    """Lines to ignore during section parsing: pack odds like '1:5 packs.'"""
    return bool(re.match(r"^\d+:\d+", line.strip()))


def parse_section(lines, start_idx):
    """
    Parse one section starting at start_idx (the section name line).
    Returns (section_data, next_idx).

    - Strips trailing ' Checklist' from section names.
    - Handles 'Parallels:' (with colon) and 'N cards.' (with period).
    - Skips pack-odds lines like '1:5 packs.' between the card count and parallels.
    - Dual-fighter Constellations cards ('CO-1 Fighter A / Fighter B') are stored
      with the full slash-delimited player string; build_output splits them.
    """
    raw_name = lines[start_idx].strip()
    section_name = re.sub(r"\s+Checklist$", "", raw_name).strip()
    idx = start_idx + 1

    # Skip card count line(s) ("N cards." or "N cards") and pack-odds lines
    while idx < len(lines):
        line = lines[idx].strip()
        if not line:
            idx += 1
            continue
        if re.match(r"^\d+ cards?\.?$", line) or is_skip_line(line):
            idx += 1
            continue
        break

    # Parse parallels block
    parallels = []
    in_parallels = False
    while idx < len(lines):
        line = lines[idx].strip()

        if not line:
            idx += 1
            continue

        if is_skip_line(line):
            idx += 1
            continue

        # "Parallels:" or "Parallels" (with or without trailing colon)
        if re.match(r"^parallels?:?$", line, re.IGNORECASE):
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

        if is_skip_line(line):
            idx += 1
            continue

        # Detect start of next section: current line is its header and next is "N cards."
        if idx + 1 < len(lines) and re.match(r"^\d+ cards?\.?$", lines[idx + 1].strip()):
            break

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

            # Dual-fighter cards have " / " — stored as-is; build_output splits them
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

        # Section header: followed by "N cards." or "N cards" on the next non-empty line
        peek = idx + 1
        while peek < len(lines) and not lines[peek].strip():
            peek += 1

        if peek < len(lines) and re.match(r"^\d+ cards?\.?$", lines[peek].strip()):
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
        unique_cards += 1  # base card
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
            # Dual-fighter cards (Constellations) have " / " in the player field —
            # split and give each fighter their own appearance for the same card number
            if "/" in card["player"]:
                player_names = [p.strip() for p in card["player"].split("/") if p.strip()]
            else:
                player_names = [card["player"]]

            for player_name in player_names:
                if player_name not in player_index:
                    player_index[player_name] = {"player": player_name, "appearances": []}
                player_index[player_name]["appearances"].append({
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
        "set_name": "2024 Topps Midnight UFC",
        "sport": "MMA",
        "season": "2024",
        "league": "UFC",
        "sections": sections,
        "players": players,
    }


if __name__ == "__main__":
    print("Parsing 2024 Topps Midnight UFC checklist...")
    sections = parse_checklist(CHECKLIST_TEXT)
    print(f"Raw sections found: {len(sections)}")

    output = build_output(sections)

    with open("ufc_midnight_2024_parsed.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nSet: {output['set_name']} ({output['season']})")
    print(f"Sections: {len(output['sections'])}")
    for s in output["sections"]:
        print(f"  {s['insert_set']}: {len(s['cards'])} cards, {len(s['parallels'])} parallels")
    print(f"Players: {len(output['players'])}")

    # Spot-check: Jon Jones across multiple sections
    if "Jon Jones" in {p["player"] for p in output["players"]}:
        jones = next(p for p in output["players"] if p["player"] == "Jon Jones")
        print(f"\n=== Jon Jones ===")
        print(f"  Insert sets:     {jones['stats']['insert_sets']}")
        print(f"  Unique cards:    {jones['stats']['unique_cards']}")
        print(f"  Total print run: {jones['stats']['total_print_run']}")
        print(f"  1/1s:            {jones['stats']['one_of_ones']}")
        for a in jones["appearances"]:
            print(f"  {a['insert_set']} — {a['card_number']} ({len(a['parallels'])} parallels)")

    # Spot-check: Constellations CO-1 dual fighters
    constellations = next(
        (s for s in output["sections"] if s["insert_set"] == "Constellations"), None
    )
    if constellations:
        co1 = [c for c in constellations["cards"] if c["card_number"] == "CO-1"]
        print(f"\nConstellations CO-1 raw player field: {[c['player'] for c in co1]}")
        for name in ["Khabib Nurmagomedov", "Islam Makhachev"]:
            p = next((x for x in output["players"] if x["player"] == name), None)
            if p:
                apps = [a for a in p["appearances"] if a["insert_set"] == "Constellations"]
                print(f"  {name} Constellations cards: {[a['card_number'] for a in apps]}")

    print(f"\nSaved to ufc_midnight_2024_parsed.json")
