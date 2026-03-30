import json
import re

CHECKLIST = """\
Base Set
200 cards
Parallels

Refractor
Pink Refractor
Aqua Refractor /199
Blue Refractor /150
Green Refractor /99
US Flag Refractor /76
Gold Refractor /50
Orange Refractor /25
Black Refractor /10
Red Refractor /5
Printing Plates /1
Superfractor /1
1 Katie Ledecky
2 Jessica Long
3 Alexander Massialas
4 Jaleen Roberts
5 Konnor McClain
6 CJ Nickolas
7 Steve Serio
8 Maggie Steffens
9 Kyle Dake
10 Jalen Neal
11 Ilona Maher
12 Alex Morgan
13 Jennifer Lozano
14 Carl Lewis
15 Howard Shu
16 Chuck Aoki
17 Torri Huske
18 Lilly King
19 Perry Baker
20 Mikal Bridges
21 Tom Schaar
22 Valarie Allman
23 Tara Davis-Woodhall
24 Grant Holloway
25 Chloé Dygert
26 Michael Andrew
27 Tyler Downs
28 Katie Grimes
29 Paxten Aaronson
30 Vashti Cunningham
31 Michael Cherry
32 Ryan Crouser
33 Tahl Leibovitz
34 Minna Stess
35 Colleen Young
36 Jadin O'Brien
37 Caroline Marks
38 Shilese Jones
39 David Taylor
40 Steph Curry
41 Hannah Roberts
42 Caity Simmers
43 Anna Hall
44 Carson Foster
45 Mark Spitz
46 Morgan Stickney
47 Fred Kerley
48 Roderick Townsend
49 Cade Cowell
50 Xander Schauffele
51 Gabby Thomas
52 Catarina Macario
53 Tanner Wright
54 Nick Mayhugh
55 Hunter Woodhall
56 Lilia Vu
57 Ashley Sessa
58 Kate Vibert
59 Vernon Norwood
60 Colin Duffy
61 Taryn Kloth
62 Kieran Smith
63 Brady Ellison
64 Sunny Choi
65 Jeffrey Louis
66 Kevin Durant
67 Issac Jean-Paul
68 Noelle Lambert
69 Sophia Smith
70 Niko Tsakiris
71 Ryan Murphy
72 Regan Smith
73 Sara Hughes
74 Kelly Cheng
75 Bobby Finke
76 Jimmer Fredette
77 Brody Malone
78 Casey Eichfeld
79 Kevon Williams
80 Jack McGlynn
81 Jake Ilardi
82 Kristen Nuss
83 Hailey Hernandez
84 Dwyane Wade
85 Jaydin Blackwell
86 Evy Leibfarth
87 Claire Curzan
88 Griffin Colapinto
89 David Robinson
90 Brittni Mason
91 Oksana Masters
92 Christian Laettner
93 Sandi Morris
94 Jason Kidd
95 Trenten Merrill
96 Mallory Swanson
97 Caeleb Dressel
98 Quinn Sullivan
99 Eric Bennett
100 Michael Phelps
101 Katie Ledecky
102 Breanna Clark
103 Vincent Hancock
104 Tanner Wright
105 Chloé Dygert
106 Alex Morgan
107 Colin Duffy
108 Cade Cowell
109 Ashley Sessa
110 Kevin Mather
111 Kevon Williams
112 Mallory Swanson
113 Shilese Jones
114 Jaydin Blackwell
115 Blake Haxton
116 Jimmer Fredette
117 Oksana Masters
118 Hunter Woodhall
119 Steph Curry
120 Lilia Vu
121 Brady Ellison
122 Regan Smith
123 Julia Gaffney
124 Jake Ilardi
125 Hannah Roberts
126 Michael Cherry
127 Ilona Maher
128 Jalen Neal
129 Tyler Downs
130 Roderick Townsend
131 Sophia Smith
132 Jack McGlynn
133 Taryn Kloth
134 Anna Hall
135 Ryan Crouser
136 Mohamed Lahna
137 Mark Spitz
138 Kieran Smith
139 Konnor McClain
140 Jessica Parratto
141 Gabby Thomas
142 Kelly Cheng
143 Lilly King
144 Hailey Hernandez
145 Eric Bennett
146 Vashti Cunningham
147 Jeffrey Louis
148 Sarah Adam
149 Sandi Morris
150 Xander Schauffele
151 Carmelo Anthony
152 Carly Patterson
153 Michael Andrew
154 Sara Hughes
155 Kristen Nuss
156 John John Florence
157 Dana Mathewson
158 Jessica Long
159 Kate Vibert
160 Casey Eichfeld
161 Mallory Weggeman
162 David Taylor
163 Alexander Massialas
164 Kevin Durant
165 Carl Lewis
166 Katie Grimes
167 Natalie Schneider
168 Claire Curzan
169 Quinn Sullivan
170 Torri Huske
171 Fred Kerley
172 Ahalya Lettenberger
173 Dwyane Wade
174 Catarina Macario
175 Bobby Finke
176 Sunny Choi
177 Caity Simmers
178 Niko Tsakiris
179 Howard Shu
180 Mikal Bridges
181 Tom Schaar
182 Kyle Dake
183 Taleah Williams
184 Ryan Murphy
185 Vince Carter
186 Caroline Marks
187 Magic Johnson
188 Vernon Norwood
189 Griffin Colapinto
190 Valarie Allman
191 Paxten Aaronson
192 Minna Stess
193 Perry Baker
194 Caeleb Dressel
195 Kevin Polish
196 Maggie Steffens
197 Tara Davis-Woodhall
198 Grant Holloway
199 Trenten Merrill
200 Michael Phelps

Base Autographs
81 cards
Parallels

Green Refractor /99
US Flag Refractor /76
Gold Refractor /50
Red Refractor /5
Superfractor /1
AU-AH Anna Hall
AU-AM Alexander Massialas
AU-AMO Alex Morgan
AU-AS Ashley Sessa
AU-BE Brady Ellison
AU-BF Bobby Finke
AU-CC Cade Cowell
AU-CCU Claire Curzan
AU-CD Colin Duffy
AU-CDR Caeleb Dressel
AU-CDY Chloé Dygert
AU-CF Carson Foster
AU-CL Carl Lewis
AU-CM Catarina Macario
AU-CMA Caroline Marks
AU-CN CJ Nickolas
AU-CS Caity Simmers
AU-DT David Taylor
AU-EL Evy Leibfarth
AU-FK Fred Kerley
AU-GC Griffin Colapinto
AU-GH Grant Holloway
AU-GT Gabby Thomas
AU-HH Hailey Hernandez
AU-HR Hannah Roberts
AU-HS Howard Shu
AU-HW Hunter Woodhall
AU-IM Ilona Maher
AU-JB Jaydin Blackwell
AU-JF Jimmer Fredette
AU-JI Jake Ilardi
AU-JJF John John Florence
AU-JL Jeffrey Louis
AU-JLO Jessica Long
AU-JM Jack McGlynn
AU-JN Jalen Neal
AU-JO Jadin O'Brien
AU-KC Kelly Cheng
AU-KD Kyle Dake
AU-KG Katie Grimes
AU-KL Katie Ledecky
AU-KM Konnor McClain
AU-KN Kristen Nuss
AU-KS Kieran Smith
AU-KV Kate Vibert
AU-KW Kevon Williams
AU-LK Lilly King
AU-LV Lilia Vu
AU-MA Michael Andrew
AU-MC Michael Cherry
AU-MP Michael Phelps
AU-MS Minna Stess
AU-MSP Mark Spitz
AU-MST Maggie Steffens
AU-MSW Mallory Swanson
AU-NL Noelle Lambert
AU-NM Nick Mayhugh
AU-NS Natalie Schneider
AU-NT Niko Tsakiris
AU-OM Oksana Masters
AU-PA Paxten Aaronson
AU-PB Perry Baker
AU-QS Quinn Sullivan
AU-RC Ryan Crouser
AU-RM Ryan Murphy
AU-RS Regan Smith
AU-RT Roderick Townsend
AU-SC Sunny Choi
AU-SH Sara Hughes
AU-SJ Shilese Jones
AU-SM Sandi Morris
AU-SS Steve Serio
AU-SSM Sophia Smith
AU-TD Tara Davis-Woodhall
AU-TH Torri Huske
AU-TK Taryn Kloth
AU-TS Tom Schaar
AU-VA Valarie Allman
AU-VC Vashti Cunningham
AU-VN Vernon Norwood
AU-XS Xander Schauffele

1984 Topps Autographs
9 cards
Base versions are numbered to /99
Parallels

US Flag Refractor /76
Gold Refractor /50
Red Refractor /5
Superfractor /1
84A-CC Claire Curzan
84A-CD Chloé Dygert
84A-FK Fred Kerley
84A-GH Grant Holloway
84A-GT Gabby Thomas
84A-HH Hailey Hernandez
84A-KM Konnor McClain
84A-TH Torri Huske
84A-VC Vashti Cunningham

Olympic Champions Autographs
8 cards
Base versions are numbered to /99
Parallels

US Flag Refractor /76
Gold Refractor /50
Red Refractor /5
Superfractor /1
OCA-CD Caeleb Dressel
OCA-CL Carl Lewis
OCA-KL Katie Ledecky
OCA-MC Michael Cherry
OCA-MP Michael Phelps
OCA-MS Mark Spitz
OCA-RM Ryan Murphy
OCA-XS Xander Schauffele

Dual Autographs
9 cards
Base versions are numbered to /25
Parallels

Red Refractor /5
Superfractor /1
DA-AC Paxten Aaronson/Cade Cowell
DA-DM Ryan Murphy/Caeleb Dressel
DA-HC Kelly Cheng/Sara Hughes
DA-LC Jeffrey Louis/Sunny Choi
DA-NK Kristen Nuss/Taryn Kloth
DA-SC Caity Simmers/Griffin Colapinto
DA-SS Mallory Swanson/Sophia Smith
DA-SV Xander Schauffele/Lilia Vu
DA-WD Hunter Woodhall/Tara Davis-Woodhall

Ledecky Legacy Autographs
10 cards
Base versions are numbered to /10
Parallels

Superfractor /1
KLA-KL1 Katie Ledecky
KLA-KL2 Katie Ledecky
KLA-KL3 Katie Ledecky
KLA-KL4 Katie Ledecky
KLA-KL5 Katie Ledecky
KLA-KL6 Katie Ledecky
KLA-KL7 Katie Ledecky
KLA-KL8 Katie Ledecky
KLA-KL9 Katie Ledecky
KLA-KL10 Katie Ledecky

Topps Dynasty Autograph Patch
13 cards
Base versions are numbered to /10
Parallels

Silver /5
Gold /1
DPA-KL Katie Ledecky
DPA-KL1 Katie Ledecky
DPA-KL2 Katie Ledecky
DPA-KM Konnor McClain
DPA-KM1 Konnor McClain
DPA-LV Lilia Vu
DPA-LV1 Lilia Vu
DPA-LV2 Lilia Vu
DPA-RM Ryan Murphy
DPA-RM1 Ryan Murphy
DPA-XS Xander Schauffele
DPA-XS1 Xander Schauffele
DPA-XS2 Xander Schauffele

Team USA Memorabilia Pieces
59 cards
Parallels

Gold Refractor /50
Orange Refractor /25
Red Refractor /5
Superfractor /1
USA-AH Anna Hall
USA-AMO Alex Morgan
USA-AS Ashley Sessa
USA-BE Brady Ellison
USA-BF Bobby Finke
USA-CC Cade Cowell
USA-CCU Claire Curzan
USA-CD Colin Duffy
USA-CDR Caeleb Dressel
USA-CDY Chloé Dygert
USA-CF Carson Foster
USA-CM Caroline Marks
USA-CS Caity Simmers
USA-EL Evy Leibfarth
USA-GC Griffin Colapinto
USA-GH Grant Holloway
USA-GT Gabby Thomas
USA-HH Hailey Hernandez
USA-HR Hannah Roberts
USA-HS Howard Shu
USA-HW Hunter Woodhall
USA-IM Ilona Maher
USA-JB Jaydin Blackwell
USA-JF Jimmer Fredette
USA-JI Jake Ilardi
USA-JL Jeffrey Louis
USA-JLO Jessica Long
USA-JM Jack McGlynn
USA-JN Jalen Neal
USA-KC Kelly Cheng
USA-KG Katie Grimes
USA-KL Katie Ledecky
USA-KM Konnor McClain
USA-KS Kieran Smith
USA-KV Kate Vibert
USA-KW Kevon Williams
USA-LK Lilly King
USA-LV Lilia Vu
USA-MA Michael Andrew
USA-MC Michael Cherry
USA-MS Minna Stess
USA-MST Maggie Steffens
USA-NL Noelle Lambert
USA-NM Nick Mayhugh
USA-NT Niko Tsakiris
USA-PA Paxten Aaronson
USA-PB Perry Baker
USA-QS Quinn Sullivan
USA-RM Ryan Murphy
USA-RT Roderick Townsend
USA-SC Sunny Choi
USA-SH Sara Hughes
USA-SJ Shilese Jones
USA-SS Steve Serio
USA-SSM Sophia Smith
USA-TD Tara Davis-Woodhall
USA-TH Torri Huske
USA-TS Tom Schaar
USA-XS Xander Schauffele

Team USA Jumbo Memorabilia Pieces
94 cards

USAJ-AMO Alex Morgan
USAJ-AMO1 Alex Morgan
USAJ-AS Ashley Sessa
USAJ-AS1 Ashley Sessa
USAJ-BE Brady Ellison
USAJ-BE1 Brady Ellison
USAJ-BF Bobby Finke
USAJ-BF1 Bobby Finke
USAJ-CC Claire Curzan
USAJ-CC1 Claire Curzan
USAJ-CCO Cade Cowell
USAJ-CCO1 Cade Cowell
USAJ-CD Caeleb Dressel
USAJ-CD1 Caeleb Dressel
USAJ-CDU Colin Duffy
USAJ-CDU1 Colin Duffy
USAJ-CDY Chloé Dygert
USAJ-CDY1 Chloé Dygert
USAJ-CF Carson Foster
USAJ-CF1 Carson Foster
USAJ-CM Caroline Marks
USAJ-CM1 Caroline Marks
USAJ-CS Caity Simmers
USAJ-CS1 Caity Simmers
USAJ-GC Griffin Colapinto
USAJ-GC1 Griffin Colapinto
USAJ-GH Grant Holloway
USAJ-GH1 Grant Holloway
USAJ-GT Gabby Thomas
USAJ-GT1 Gabby Thomas
USAJ-HH Hailey Hernandez
USAJ-HH1 Hailey Hernandez
USAJ-HS Howard Shu
USAJ-HS1 Howard Shu
USAJ-HW Hunter Woodhall
USAJ-HW1 Hunter Woodhall
USAJ-IM Ilona Maher
USAJ-IM1 Ilona Maher
USAJ-JF Jimmer Fredette
USAJ-JF1 Jimmer Fredette
USAJ-JI Jake Ilardi
USAJ-JI1 Jake Ilardi
USAJ-JL Jessica Long
USAJ-JL1 Jessica Long
USAJ-KC Kelly Cheng
USAJ-KC1 Kelly Cheng
USAJ-KD Kyle Dake
USAJ-KD1 Kyle Dake
USAJ-KG Katie Grimes
USAJ-KG1 Katie Grimes
USAJ-KL Katie Ledecky
USAJ-KL1 Katie Ledecky
USAJ-KN Kristen Nuss
USAJ-KN1 Kristen Nuss
USAJ-KV Kate Vibert
USAJ-KV1 Kate Vibert
USAJ-LK Lilly King
USAJ-LK1 Lilly King
USAJ-LV Lilia Vu
USAJ-LV1 Lilia Vu
USAJ-MA Michael Andrew
USAJ-MA1 Michael Andrew
USAJ-MC Michael Cherry
USAJ-MC1 Michael Cherry
USAJ-MST Minna Stess
USAJ-MST1 Minna Stess
USAJ-PA Paxten Aaronson
USAJ-PA1 Paxten Aaronson
USAJ-PB Perry Baker
USAJ-PB1 Perry Baker
USAJ-RM Ryan Murphy
USAJ-RM1 Ryan Murphy
USAJ-RS Regan Smith
USAJ-RS1 Regan Smith
USAJ-SC Sunny Choi
USAJ-SC1 Sunny Choi
USAJ-SH Sara Hughes
USAJ-SH1 Sara Hughes
USAJ-SJ Shilese Jones
USAJ-SJ1 Shilese Jones
USAJ-SS Sophia Smith
USAJ-SS1 Sophia Smith
USAJ-TD Tara Davis-Woodhall
USAJ-TD1 Tara Davis-Woodhall
USAJ-TH Torri Huske
USAJ-TH1 Torri Huske
USAJ-TK Taryn Kloth
USAJ-TK1 Taryn Kloth
USAJ-TS Tom Schaar
USAJ-TS1 Tom Schaar
USAJ-VC Vashti Cunningham
USAJ-VC1 Vashti Cunningham
USAJ-XS Xander Schauffele
USAJ-XS1 Xander Schauffele

1984 Topps
20 cards
Parallels

Green Refractor /99
US Flag Refractor /76
Gold Refractor /50
Orange Refractor /25
Black Refractor /10
Red Refractor /5
Superfractor /1
84T-1 Katie Ledecky
84T-2 Xander Schauffele
84T-3 Caeleb Dressel
84T-4 Kevin Durant
84T-5 Michael Phelps
84T-6 Catarina Macario
84T-7 Ashley Sessa
84T-8 Fred Kerley
84T-9 Vashti Cunningham
84T-10 Perry Baker
84T-11 Kyle Dake
84T-12 Kelly Cheng
84T-13 Alexander Massialas
84T-14 Griffin Colapinto
84T-15 Claire Curzan
84T-16 Brady Ellison
84T-17 Lilly King
84T-18 Paxten Aaronson
84T-19 Howard Shu
84T-20 Steve Serio

Athlete Nouveau
20 cards
Parallels

Red Refractor /5
Superfractor /1
AN-1 Lilia Vu
AN-2 Mikal Bridges
AN-3 Jimmer Fredette
AN-4 Konnor McClain
AN-5 Cade Cowell
AN-6 Carson Foster
AN-7 Hailey Hernandez
AN-8 John John Florence
AN-9 Anna Hall
AN-10 Kristen Nuss
AN-11 Taryn Kloth
AN-12 Shilese Jones
AN-13 Minna Stess
AN-14 Tom Schaar
AN-15 CJ Nickolas
AN-16 Jadin O'Brien
AN-17 Jeffrey Louis
AN-18 Sunny Choi
AN-19 Evy Leibfarth
AN-20 Perry Baker

Chasing the Rings
25 cards
Parallel

Superfractor /1
CR-1 Katie Ledecky
CR-2 Katie Ledecky
CR-3 Katie Ledecky
CR-4 Katie Ledecky
CR-5 Katie Ledecky
CR-6 Xander Schauffele
CR-7 Xander Schauffele
CR-8 Xander Schauffele
CR-9 Xander Schauffele
CR-10 Xander Schauffele
CR-11 Sophia Smith
CR-12 Sophia Smith
CR-13 Sophia Smith
CR-14 Sophia Smith
CR-15 Sophia Smith
CR-16 Steph Curry
CR-17 Steph Curry
CR-18 Steph Curry
CR-19 Steph Curry
CR-20 Steph Curry
CR-21 Michael Phelps
CR-22 Michael Phelps
CR-23 Michael Phelps
CR-24 Michael Phelps
CR-25 Michael Phelps

Exposé
30 cards
Parallels

Red Refractor /5
Superfractor /1
TCE-1 Katie Ledecky
TCE-2 Xander Schauffele
TCE-3 Lilia Vu
TCE-4 Alex Morgan
TCE-5 Kevin Durant
TCE-6 Steph Curry
TCE-7 Mikal Bridges
TCE-8 Michael Phelps
TCE-9 Mark Spitz
TCE-10 Catarina Macario
TCE-11 Carl Lewis
TCE-12 John John Florence
TCE-13 Bobby Finke
TCE-14 Sophia Smith
TCE-15 Mallory Swanson
TCE-16 Kristen Nuss
TCE-17 Taryn Kloth
TCE-18 Kelly Cheng
TCE-19 Sara Hughes
TCE-20 Kyle Dake
TCE-21 Caity Simmers
TCE-22 Griffin Colapinto
TCE-23 Brady Ellison
TCE-24 Jessica Long
TCE-25 Steve Serio
TCE-26 Lilly King
TCE-27 Michael Andrew
TCE-28 Fred Kerley
TCE-29 Michael Cherry
TCE-30 Tara Davis-Woodhall

Flames
10 cards
Parallels

Green Refractor /99
US Flag Refractor /76
Gold Refractor /50
Orange Refractor /25
Black Refractor /10
Red Refractor /5
Superfractor /1
F-1 Katie Ledecky
F-2 Lilia Vu
F-3 Alex Morgan
F-4 Catarina Macario
F-5 Mark Spitz
F-6 Jimmer Fredette
F-7 Xander Schauffele
F-8 Jake Ilardi
F-9 Michael Phelps
F-10 Jessica Long

For Pride and Country
19 cards
Parallels

Green Refractor /99
US Flag Refractor /76
Gold Refractor /50
Orange Refractor /25
Black Refractor /10
Red Refractor /5
Superfractor /1
PC-1 Katie Ledecky
PC-2 Xander Schauffele
PC-3 Caeleb Dressel
PC-4 Steph Curry
PC-5 Michael Phelps
PC-6 Catarina Macario
PC-7 Hailey Hernandez
PC-8 Bobby Finke
PC-9 Sunny Choi
PC-10 Tom Schaar
PC-11 CJ Nickolas
PC-12 Konnor McClain
PC-13 Jessica Long
PC-14 Michael Andrew
PC-15 Ryan Murphy
PC-16 Vernon Norwood
PC-17 Gabby Thomas
PC-18 Katie Grimes
PC-19 Jadin O'Brien

Ledecky Legacy
10 cards
Parallels

Green Refractor /99
US Flag Refractor /76
Gold Refractor /50
Orange Refractor /25
Black Refractor /10
Red Refractor /5
Superfractor /1
KL-1 Katie Ledecky
KL-2 Katie Ledecky
KL-3 Katie Ledecky
KL-4 Katie Ledecky
KL-5 Katie Ledecky
KL-6 Katie Ledecky
KL-7 Katie Ledecky
KL-8 Katie Ledecky
KL-9 Katie Ledecky
KL-10 Katie Ledecky

To Paris With Love
15 cards
Parallels

Green Refractor /99
US Flag Refractor /76
Gold Refractor /50
Orange Refractor /25
Black Refractor /10
Red Refractor /5
Superfractor /1
PL-1 Katie Ledecky
PL-2 Xander Schauffele
PL-3 Caeleb Dressel
PL-4 Steph Curry
PL-5 Chloé Dygert
PL-6 Jeffrey Louis
PL-7 Sandi Morris
PL-8 Sara Hughes
PL-9 Caity Simmers
PL-10 Minna Stess
PL-11 Jimmer Fredette
PL-12 Torri Huske
PL-13 Shilese Jones
PL-14 Kate Vibert
PL-15 Regan Smith
"""

# ─────────────────────────────────────────────────────────────
# Multi-player sections
# ─────────────────────────────────────────────────────────────
MULTI_PLAYER_SECTIONS = {"Dual Autographs"}

# ─────────────────────────────────────────────────────────────
# Lines to skip
# ─────────────────────────────────────────────────────────────
SKIP_PATTERNS = [
    r"^shop for .+ on ebay",
    r"^base versions are numbered to",
]


def should_skip(line: str) -> bool:
    low = line.lower().strip()
    return any(re.match(p, low) for p in SKIP_PATTERNS)


# ─────────────────────────────────────────────────────────────
# Parallel helpers
# ─────────────────────────────────────────────────────────────

def parse_print_run(text: str):
    if re.search(r"\b1/1\b", text):
        return 1
    m = re.search(r"/(-\d+)", text)
    if m:
        return int(m.group(1))
    m = re.search(r"/(\d+)", text)
    if m:
        return int(m.group(1))
    return None


def parse_parallel_line(line: str) -> dict:
    pr = parse_print_run(line)
    name = re.sub(r"\s*\([^)]*\)\s*$", "", line).strip()
    name = re.sub(r"\s*/[-]?\d+.*$", "", name).strip()
    name = re.sub(r"\s*\b1/1\b.*$", "", name).strip()
    return {"name": name, "print_run": pr}


# ─────────────────────────────────────────────────────────────
# Card line regex — handles prefixes like "84A-", "USAJ-", "KLA-KL1"
# ─────────────────────────────────────────────────────────────
CARD_LINE_RE = re.compile(
    r"^((?:\d+[A-Z][A-Z0-9]*|[A-Z][A-Z0-9]*)-[^\s]+|\d+)\s+(.+)"
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
# Card line parser
# ─────────────────────────────────────────────────────────────

def parse_card_line(line: str, section_name: str) -> list:
    line = line.strip()
    m = CARD_LINE_RE.match(line)
    if not m:
        return []

    card_number = m.group(1)
    rest = m.group(2).strip()

    # Strip inline /N suffix (e.g. Jumbo Memorabilia "/1")
    rest = re.sub(r"\s*/\d+\s*$", "", rest).strip()

    # Multi-player: split on "/" (no spaces around slash)
    if section_name in MULTI_PLAYER_SECTIONS and "/" in rest:
        parts = [p.strip() for p in rest.split("/")]
        return [
            {"card_number": card_number, "player": p,
             "team": "Team USA", "is_rookie": False, "subset": None}
            for p in parts
        ]

    return [{"card_number": card_number, "player": rest,
             "team": "Team USA", "is_rookie": False, "subset": None}]


# ─────────────────────────────────────────────────────────────
# Main checklist parser
# ─────────────────────────────────────────────────────────────

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

        if not is_section_start(lines, idx):
            idx += 1
            continue

        section_name = line

        # Skip past "N cards" line
        idx = next_nonempty(lines, idx + 1) + 1

        # Parse parallels
        parallels = []
        in_parallels = False

        while idx < n:
            ln = lines[idx].strip()

            if not ln:
                idx += 1
                continue

            if should_skip(ln):
                idx += 1
                continue

            if ln.lower() in ("parallels", "parallel"):
                in_parallels = True
                idx += 1
                continue

            if in_parallels:
                if is_card_line(ln):
                    break
                if is_section_start(lines, idx):
                    break
                parallels.append(parse_parallel_line(ln))
                idx += 1
            else:
                if is_card_line(ln):
                    break
                if is_section_start(lines, idx):
                    break
                idx += 1

        # Parse cards
        cards = []
        while idx < n:
            ln = lines[idx].strip()

            if not ln:
                idx += 1
                continue

            if should_skip(ln):
                idx += 1
                continue

            if is_section_start(lines, idx):
                break

            if is_card_line(ln):
                cards.extend(parse_card_line(ln, section_name))

            idx += 1

        sections.append({"insert_set": section_name, "parallels": parallels, "cards": cards})

    return sections


# ─────────────────────────────────────────────────────────────
# Post-processing: synthetic parallels for serialized sets
# ─────────────────────────────────────────────────────────────

def apply_synthetic_parallels(sections: list):
    for section in sections:
        name = section["insert_set"]

        if name == "Team USA Jumbo Memorabilia Pieces":
            # Every card is a 1/1 — no additional parallels
            section["parallels"] = [{"name": "Base", "print_run": 1}]

        elif name in ("1984 Topps Autographs", "Olympic Champions Autographs"):
            # Base cards numbered /99
            section["parallels"] = [{"name": "Base", "print_run": 99}] + section["parallels"]

        elif name == "Dual Autographs":
            # Base cards numbered /25
            section["parallels"] = [{"name": "Base", "print_run": 25}] + section["parallels"]

        elif name in ("Ledecky Legacy Autographs", "Topps Dynasty Autograph Patch"):
            # Base cards numbered /10
            section["parallels"] = [{"name": "Base", "print_run": 10}] + section["parallels"]


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
    rc_players: set = set()  # no RC tags in this set

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
                "is_rookie": False,
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
        "set_name": "2024 Topps Chrome U.S. Olympic & Paralympic Team Hopefuls",
        "sport": "Olympics",
        "season": "2024",
        "league": "Olympics",
        "sections": sections,
        "players": players,
    }


# ─────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Parsing 2024 Topps Chrome U.S. Olympic & Paralympic Team Hopefuls...")

    sections = parse_checklist(CHECKLIST)
    apply_synthetic_parallels(sections)

    output = build_output(sections)

    out_path = "olympics_chrome_2024_parsed.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nSet: {output['set_name']} ({output['season']})")
    print(f"Sections: {len(output['sections'])}")
    for s in output["sections"]:
        print(f"  {s['insert_set']}: {len(s['cards'])} cards, {len(s['parallels'])} parallels")

    print(f"\nTotal players: {len(output['players'])}")

    player_map = {p["player"]: p for p in output["players"]}

    print("\n=== SPOT CHECK: Katie Ledecky ===")
    if "Katie Ledecky" in player_map:
        kl = player_map["Katie Ledecky"]
        st = kl["stats"]
        print(f"  Insert sets:  {st['insert_sets']}")
        print(f"  Unique cards: {st['unique_cards']}")
        print(f"  1/1s:         {st['one_of_ones']}")
        for a in kl["appearances"]:
            print(f"    {a['insert_set']} #{a['card_number']} | {len(a['parallels'])} parallels")

    print("\n=== SPOT CHECK: Dual Autographs co-players ===")
    da = next((s for s in output["sections"] if s["insert_set"] == "Dual Autographs"), None)
    if da:
        from collections import Counter
        nums = Counter(c["card_number"] for c in da["cards"])
        for cn, count in sorted(nums.items()):
            players_on = [c["player"] for c in da["cards"] if c["card_number"] == cn]
            print(f"  {cn}: {' / '.join(players_on)}")

    print("\n=== SPOT CHECK: Ledecky Legacy Autographs ===")
    kla = next((s for s in output["sections"] if s["insert_set"] == "Ledecky Legacy Autographs"), None)
    if kla:
        print(f"  Cards: {len(kla['cards'])}")
        print(f"  Parallels: {kla['parallels']}")

    print("\n=== SPOT CHECK: Jumbo Memorabilia ===")
    jumbo = next((s for s in output["sections"] if s["insert_set"] == "Team USA Jumbo Memorabilia Pieces"), None)
    if jumbo:
        print(f"  Cards: {len(jumbo['cards'])}")
        print(f"  Parallels: {jumbo['parallels']}")
        print(f"  Sample: {jumbo['cards'][0]['card_number']} {jumbo['cards'][0]['player']}")
        print(f"          {jumbo['cards'][1]['card_number']} {jumbo['cards'][1]['player']}")

    print("\n=== SPOT CHECK: Base Set ===")
    base = next((s for s in output["sections"] if s["insert_set"] == "Base Set"), None)
    if base:
        unique_athletes = {c["player"] for c in base["cards"]}
        print(f"  Total cards: {len(base['cards'])} | Unique athletes: {len(unique_athletes)}")
        print(f"  Parallels: {len(base['parallels'])}")
