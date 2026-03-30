import json
import re

CHECKLIST = """\
Base Set
200 cards
Parallels

Refractor
Red, White & Blue Refractor (Value Exclusive)
Pink Refractor /250
Aqua Refractor /199
Blue Refractor /150
Green Refractor /99
USA Flag Refractor /76
Purple Refractor /75
Gold Refractor /50
Orange Refractor /25
Black Refractor /10
Red Refractor /5
Superfractor /1
1 Dusty Henricksen
2 Noah Elliott
3 Ashley Wagner
4 Nick Goepper
5 Mikaela Shiffrin
6 Grace Henderson
7 Alysa Liu
8 Jaelin Kauf
9 Ryan Cochran-Siegle
10 John Shuster
11 Bode Miller
12 Lauren Macuga
13 Amber Glenn
14 Judd Henkes
15 Nina O'Brien
16 Chloe Kim
17 Jason Brown
18 Kelly Clark
19 Red Gerard
20 Maddie Mastro
21 Alex Ferreira
22 Winter Vinecki
23 Kaysha Love
24 Jordan Stolz
25 Breezy Johnson
26 Nathan Chen
27 Brittany Bowe
28 Jamie Anderson
29 Dani Aravich
30 Ross Powers
31 Joey Okesson
32 Hilary Knight
33 Erin Jackson
34 Rosie Brennan
35 Chris Klug
36 Mac Forehand
37 Jack Hughes
38 Shani Davis
39 Jessie Diggins
40 Aaron Blunck
41 Evan Lysacek
42 Kristen Santos-Griswold
43 Devin Logan
44 Evan Bates
45 Madison Chock
46 Jack Wallace
47 Brittani Coury
48 Hannah Teter
49 Julia Marino
50 Tristan Feinberg
51 Alex Hall
52 Oksana Masters
53 Elana Meyers Taylor
54 Ollie Martin
55 Hunter Henderson
56 Brenna Huckaby
57 Konnor Ralph
58 Meryl Davis
59 Hanna Faulhaber
60 Charlie White
61 Seth Wescott
62 Katie Uhlaender
63 Keely Cashman
64 Hannah Kearney
65 Liz Lemley
66 Ted Ligety
67 Alli Macuga
68 Sam Macuga
69 Paula Moltzan
70 Sam Morse
71 Kikkan Randall
72 Ava Sunshine
73 Isabeau Levito
74 Christopher Lillis
75 Jen Lee
76 Dan Cnossen
77 Evan Strong
78 Malik Jones
79 Jack Eichel
80 Jake Guentzel
81 Jake Oettinger
82 Alex Carpenter
83 Colby Stevenson
84 Hailey Langland
85 River Radamus
86 Apolo Ohno
87 Aerin Frankel
88 Cayla Barnes
89 Haley Winn
90 Hannah Bilka
91 Hayley Scamurra
92 Ilia Malinin
93 Jack O'Callahan
94 Jake Canter
95 Kristi Yamaguchi
96 Lindsey Vonn
97 Mike Eruzione
98 Shaun White
99 Tessa Janecke
100 Julia Mancuso
101 Dusty Henricksen
102 Noah Elliott
103 Ashley Wagner
104 Nick Goepper
105 Mikaela Shiffrin
106 Grace Henderson
107 Alysa Liu
108 Jaelin Kauf
109 Ryan Cochran-Siegle
110 John Shuster
111 Bode Miller
112 Lauren Macuga
113 Amber Glenn
114 Judd Henkes
115 Nina O'Brien
116 Chloe Kim
117 Jason Brown
118 Kelly Clark
119 Red Gerard
120 Maddie Mastro
121 Alex Ferreira
122 Winter Vinecki
123 Kaysha Love
124 Jordan Stolz
125 Breezy Johnson
126 Nathan Chen
127 Brittany Bowe
128 Jamie Anderson
129 Dani Aravich
130 Ross Powers
131 Joey Okesson
132 Hilary Knight
133 Erin Jackson
134 Rosie Brennan
135 Chris Klug
136 Mac Forehand
137 Aaron Pike
138 Shani Davis
139 Jessie Diggins
140 Aaron Blunck
141 Evan Lysacek
142 Kristen Santos-Griswold
143 Devin Logan
144 Evan Bates
145 Madison Chock
146 Jack Wallace
147 Brittani Coury
148 Hannah Teter
149 Julia Marino
150 Tristan Feinberg
151 Alex Hall
152 Oksana Masters
153 Elana Meyers Taylor
154 Ollie Martin
155 Hunter Henderson
156 Brenna Huckaby
157 Konnor Ralph
158 Meryl Davis
159 Hanna Faulhaber
160 Charlie White
161 Seth Wescott
162 Katie Uhlaender
163 Keely Cashman
164 Hannah Kearney
165 Liz Lemley
166 Ted Ligety
167 Alli Macuga
168 Sam Macuga
169 Paula Moltzan
170 Sam Morse
171 Kikkan Randall
172 Ava Sunshine
173 Isabeau Levito
174 Christopher Lillis
175 Jen Lee
176 Dan Cnossen
177 Evan Strong
178 Malik Jones
179 Brock Crouch
180 Andrew Kurka
181 Batoyun Oyuna Uranchimeg
182 Alex Carpenter
183 Colby Stevenson
184 Hailey Langland
185 River Radamus
186 Apolo Ohno
187 Aerin Frankel
188 Cayla Barnes
189 Haley Winn
190 Hannah Bilka
191 Hayley Scamurra
192 Ilia Malinin
193 Jack O'Callahan
194 Jake Canter
195 Kristi Yamaguchi
196 Lindsey Vonn
197 Mike Eruzione
198 Shaun White
199 Tessa Janecke
200 Julia Mancuso

Autographs
Base Autographs
99 cards
Parallels

Green Refractor /99
USA Flag Refractor /76
Gold Refractor /50
Orange Refractor /25
Black Refractor /10
Red Refractor /5
Superfractor /1
BCA-ABL Aaron Blunck
BCA-ACA Alex Carpenter
BCA-AFE Alex Ferreira
BCA-AFR Aerin Frankel
BCA-AGL Amber Glenn
BCA-AHA Alex Hall
BCA-ALI Alysa Liu
BCA-AMA Alli Macuga
BCA-AOH Apolo Ohno
BCA-ASU Ava Sunshine
BCA-AWA Ashley Wagner
BCA-BBO Brittany Bowe
BCA-BCH Brock Crouch
BCA-BCO Brittani Coury
BCA-BHU Brenna Huckaby
BCA-BJO Breezy Johnson
BCA-BMI Bode Miller
BCA-CBA Cayla Barnes
BCA-CKI Chloe Kim
BCA-CKL Chris Klug
BCA-CLI Christopher Lillis
BCA-CST Colby Stevenson
BCA-CWI Charlie White
BCA-DAR Dani Aravich
BCA-DCN Dan Cnossen
BCA-DHE Dusty Henricksen
BCA-DLO Devin Logan
BCA-EBA Evan Bates
BCA-EJA Erin Jackson
BCA-ELY Evan Lysacek
BCA-EMT Elana Meyers Taylor
BCA-EST Evan Strong
BCA-GHE Grace Henderson
BCA-HBI Hannah Bilka
BCA-HFA Hanna Faulhaber
BCA-HHE Hunter Henderson
BCA-HKE Hannah Kearney
BCA-HKN Hilary Knight
BCA-HLA Hailey Langland
BCA-HSC Hayley Scamurra
BCA-HWI Haley Winn
BCA-ILE Isabeau Levito
BCA-IMA Ilia Malinin
BCA-JAN Jamie Anderson
BCA-JBR Jason Brown
BCA-JCA Jake Canter
BCA-JDI Jessie Diggins
BCA-JEI Jack Eichel
BCA-JGU Jake Guentzel
BCA-JHE Judd Henkes
BCA-JHU Jack Hughes
BCA-JKA Jaelin Kauf
BCA-JLE Jen Lee
BCA-JMA Julia Mancuso
BCA-JMO Julia Marino
BCA-JOC Jack O'Callahan
BCA-JOE Jake Oettinger
BCA-JOK Joey Okesson
BCA-JSH John Shuster
BCA-JST Jordan Stolz
BCA-JWA Jack Wallace
BCA-KCA Keely Cashman
BCA-KCL Kelly Clark
BCA-KLO Kaysha Love
BCA-KRA Konnor Ralph
BCA-KRL Kikkan Randall
BCA-KSG Kristen Santos-Griswold
BCA-KUH Katie Uhlaender
BCA-KYA Kristi Yamaguchi
BCA-LLE Liz Lemley
BCA-LMA Lauren Macuga
BCA-LVO Lindsey Vonn
BCA-MCH Madison Chock
BCA-MDA Meryl Davis
BCA-MER Mike Eruzione
BCA-MFO Mac Forehand
BCA-MMA Maddie Mastro
BCA-MSH Mikaela Shiffrin
BCA-NEL Noah Elliott
BCA-NGO Nick Goepper
BCA-NOB Nina O'Brien
BCA-OMA Oksana Masters
BCA-OMN Ollie Martin
BCA-PMO Paula Moltzan
BCA-RBR Rosie Brennan
BCA-RCS Ryan Cochran-Siegle
BCA-RGE Red Gerard
BCA-RPO Ross Powers
BCA-RRA River Radamus
BCA-SDA Shani Davis
BCA-SMA Sam Macuga
BCA-SMO Sam Morse
BCA-SWE Seth Wescott
BCA-SWH Shaun White
BCA-TFE Tristan Feinberg
BCA-THE Hannah Teter
BCA-TJA Tessa Janecke
BCA-TLI Ted Ligety
BCA-WVI Winter Vinecki

Olympic Champions Autographs
12 cards
Base versions are numbered to /100 or fewer
Parallels

USA Flag Refractor /76
Gold Refractor /50
Orange Refractor /25
Black Refractor /10
Red Refractor /5
Superfractor /1
OC-AO Apolo Ohno
OC-BM Bode Miller
OC-CK Chloe Kim
OC-IM Ilia Malinin
OC-JD Jessie Diggins
OC-KY Kristi Yamaguchi
OC-LV Lindsey Vonn
OC-ME Mike Eruzione
OC-MS Mikaela Shiffrin
OC-NC Nathan Chen
OC-RG Red Gerard
OC-SW Shaun White

1986 Topps Autographs
10 cards
Base versions are numbered to /100 or fewer
Parallels

USA Flag Refractor /76
Gold Refractor /50
Orange Refractor /25
Black Refractor /10
Red Refractor /5
Superfractor /1
86TA-AF Alex Ferreira
86TA-AL Alysa Liu
86TA-BC Brock Crouch
86TA-EJ Erin Jackson
86TA-EM Elana Meyers Taylor
86TA-HK Hilary Knight
86TA-HL Hailey Langland
86TA-IL Isabeau Levito
86TA-JS Jordan Stolz
86TA-NC Nathan Chen

Dual Autographs
6 cards
Base versions are numbered to /25 or fewer
Parallels

Red Refractor /5
Superfractor /1
DA-BC Evan Bates/Madison Chock
DA-GL Red Gerard/Hailey Langland
DA-KA Jamie Anderson/Chloe Kim
DA-LG Alysa Liu/Amber Glenn
DA-OS Jordan Stolz/Apolo Ohno
DA-VS Mikaela Shiffrin/Lindsey Vonn

Topps Dynasty Patch Autographs
15 cards
Base versions are numbered to /10 or fewer
Parallels

Silver /5
Gold /1
DAP-AF Alex Ferreira
DAP-AG Amber Glenn
DAP-AO Apolo Ohno
DAP-CK Chloe Kim
DAP-EJ Erin Jackson
DAP-HK Hilary Knight
DAP-IM Ilia Malinin
DAP-JD Jessie Diggins
DAP-JE Jack Eichel
DAP-JH Jack Hughes
DAP-JS Jordan Stolz
DAP-LV Lindsey Vonn
DAP-MS Mikaela Shiffrin
DAP-RG Red Gerard
DAP-SW Shaun White

Memorabilia
Team USA Memorabilia Pieces
78 cards
Parallels

Gold Refractor /50
Orange Refractor /25
Red Refractor /5
Superfractor /1
USM-AB Aaron Blunck
USM-AC Alex Carpenter
USM-AF Alex Ferreira
USM-AG Amber Glenn
USM-AH Alex Hall
USM-AM Alli Macuga
USM-AO Apolo Ohno
USM-AS Ava Sunshine
USM-AW Ashley Wagner
USM-BB Brittany Bowe
USM-BC Brittani Coury
USM-BH Brenna Huckaby
USM-BJ Breezy Johnson
USM-BM Bode Miller
USM-BR Brock Crouch
USM-CK Chloe Kim
USM-CS Colby Stevenson
USM-CW Charlie White
USM-DA Dani Aravich
USM-DC Dan Cnossen
USM-DH Dusty Henricksen
USM-DL Devin Logan
USM-EJ Erin Jackson
USM-EM Elana Meyers Taylor
USM-ES Evan Strong
USM-GH Grace Henderson
USM-HF Hanna Faulhaber
USM-HH Hunter Henderson
USM-HK Hilary Knight
USM-HS Hayley Scamurra
USM-HT Hannah Teter
USM-HW Haley Winn
USM-HY Hannah Kearney
USM-IM Ilia Malinin
USM-JA Jamie Anderson
USM-JB Jason Brown
USM-JC Jake Canter
USM-JD Jessie Diggins
USM-JH Jack Hughes
USM-JK Jaelin Kauf
USM-JL Jen Lee
USM-JM Julia Marino
USM-JN Joey Okesson
USM-JR John Shuster
USM-JS Judd Henkes
USM-JU Julia Mancuso
USM-JW Jack Wallace
USM-JZ Jordan Stolz
USM-KC Kelly Clark
USM-KE Keely Cashman
USM-KI Kikkan Randall
USM-KL Kaysha Love
USM-KR Konnor Ralph
USM-KS Kristen Santos-Griswold
USM-KU Katie Uhlaender
USM-LL Liz Lemley
USM-LM Lauren Macuga
USM-LV Lindsey Vonn
USM-MD Meryl Davis
USM-MF Mac Forehand
USM-MM Maddie Mastro
USM-MS Mikaela Shiffrin
USM-NE Noah Elliott
USM-NG Nick Goepper
USM-NO Nina O'Brien
USM-OM Ollie Martin
USM-PM Paula Moltzan
USM-RB Rosie Brennan
USM-RC Ryan Cochran-Siegle
USM-RG Red Gerard
USM-RP Ross Powers
USM-RR River Radamus
USM-SA Sam Macuga
USM-SD Shani Davis
USM-SM Sam Morse
USM-SW Shaun White
USM-TF Tristan Feinberg
USM-TL Ted Ligety

Team USA Jumbo Memorabilia Pieces
81 cards

USJ-AB Aaron Blunck /1
USJ-AC Alex Carpenter /1
USJ-AE Aerin Frankel /1
USJ-AF Alex Ferreira /1
USJ-AG Amber Glenn /1
USJ-AH Alex Hall /1
USJ-AM Alli Macuga /1
USJ-AO Apolo Ohno /1
USJ-AS Ava Sunshine /1
USJ-AW Ashley Wagner /1
USJ-BB Brittany Bowe /1
USJ-BC Brittani Coury /1
USJ-BH Brenna Huckaby /1
USJ-BJ Breezy Johnson /1
USJ-BM Bode Miller /1
USJ-BR Brock Crouch /1
USJ-CB Cayla Barnes /1
USJ-CK Chloe Kim /1
USJ-CS Colby Stevenson /1
USJ-CW Charlie White /1
USJ-DA Dani Aravich /1
USJ-DC Dan Cnossen /1
USJ-DH Dusty Henricksen /1
USJ-DL Devin Logan /1
USJ-EJ Erin Jackson /1
USJ-EM Elana Meyers Taylor /1
USJ-ES Evan Strong /1
USJ-GH Grace Henderson /1
USJ-HF Hanna Faulhaber /1
USJ-HH Hunter Henderson /1
USJ-HK Hilary Knight /1
USJ-HS Hayley Scamurra /1
USJ-HT Hannah Teter /1
USJ-HW Haley Winn /1
USJ-HY Hannah Kearney /1
USJ-IM Ilia Malinin /1
USJ-JA Jamie Anderson /1
USJ-JB Jason Brown /1
USJ-JC Jake Canter /1
USJ-JD Jessie Diggins /1
USJ-JE Jack Eichel /1
USJ-JH Jack Hughes /1
USJ-JK Jaelin Kauf /1
USJ-JL Jen Lee /1
USJ-JM Julia Marino /1
USJ-JN Joey Okesson /1
USJ-JR John Shuster /1
USJ-JS Judd Henkes /1
USJ-JU Julia Mancuso /1
USJ-JW Jack Wallace /1
USJ-JZ Jordan Stolz /1
USJ-KC Kelly Clark /1
USJ-KE Keely Cashman /1
USJ-KI Kikkan Randall /1
USJ-KL Kaysha Love /1
USJ-KR Konnor Ralph /1
USJ-KS Kristen Santos-Griswold /1
USJ-KU Katie Uhlaender /1
USJ-LL Liz Lemley /1
USJ-LM Lauren Macuga /1
USJ-LV Lindsey Vonn /1
USJ-MD Meryl Davis /1
USJ-MF Mac Forehand /1
USJ-MM Maddie Mastro /1
USJ-MS Mikaela Shiffrin /1
USJ-NE Noah Elliott /1
USJ-NG Nick Goepper /1
USJ-NO Nina O'Brien /1
USJ-OM Ollie Martin /1
USJ-PM Paula Moltzan /1
USJ-RB Rosie Brennan /1
USJ-RC Ryan Cochran-Siegle /1
USJ-RG Red Gerard /1
USJ-RP Ross Powers /1
USJ-RR River Radamus /1
USJ-SA Sam Macuga /1
USJ-SD Shani Davis /1
USJ-SM Sam Morse /1
USJ-SW Shaun White /1
USJ-TF Tristan Feinberg /1
USJ-TL Ted Ligety /1

Inserts
Buongiorno
20 cards
Parallels

USA Flag Refractor /76
Gold Refractor /50
Orange Refractor /25
Black Refractor /10
Red Refractor /5
Superfractor /1
BU-1 Hilary Knight
BU-2 Alysa Liu
BU-3 Ilia Malinin
BU-4 Mikaela Shiffrin
BU-5 Nathan Chen
BU-6 Lindsey Vonn
BU-7 Apolo Ohno
BU-8 Jessie Diggins
BU-9 Chloe Kim
BU-10 Shaun White
BU-11 Jordan Stolz
BU-12 Red Gerard
BU-13 Hailey Langland
BU-14 Evan Bates
BU-15 Madison Chock
BU-16 Erin Jackson
BU-17 Amber Glenn
BU-18 Alex Ferreira
BU-19 Isabeau Levito
BU-20 Bode Miller

For Pride And Country
25 cards
Parallels

USA Flag Refractor /76
Gold Refractor /50
Orange Refractor /25
Black Refractor /10
Red Refractor /5
Superfractor /1
PC-1 Hilary Knight
PC-2 Alysa Liu
PC-3 Ilia Malinin
PC-4 Mikaela Shiffrin
PC-5 Nathan Chen
PC-6 Lindsey Vonn
PC-7 Apolo Ohno
PC-8 Jessie Diggins
PC-9 Chloe Kim
PC-10 Shaun White
PC-11 Jordan Stolz
PC-12 Red Gerard
PC-13 Hailey Langland
PC-14 Evan Bates
PC-15 Madison Chock
PC-16 Erin Jackson
PC-17 Amber Glenn
PC-18 Alex Ferreira
PC-19 Isabeau Levito
PC-20 Brittany Bowe
PC-21 Bode Miller
PC-22 Kristi Yamaguchi
PC-23 Mike Eruzione
PC-24 Elana Meyers Taylor
PC-25 Jamie Anderson

1986 Topps
40 cards
Parallels

USA Flag Refractor /76
Gold Refractor /50
Orange Refractor /25
Black Refractor /10
Red Refractor /5
Superfractor /1
T86-1 Hilary Knight
T86-2 Alysa Liu
T86-3 Ilia Malinin
T86-4 Mikaela Shiffrin
T86-5 Nathan Chen
T86-6 Lindsey Vonn
T86-7 Apolo Ohno
T86-8 Jessie Diggins
T86-9 Chloe Kim
T86-10 Shaun White
T86-11 Jordan Stolz
T86-12 Red Gerard
T86-13 Hailey Langland
T86-14 Evan Bates
T86-15 Madison Chock
T86-16 Erin Jackson
T86-17 Amber Glenn
T86-18 Alex Ferreira
T86-19 Isabeau Levito
T86-20 Brittany Bowe
T86-21 Bode Miller
T86-22 Kristi Yamaguchi
T86-23 Mike Eruzione
T86-24 Elana Meyers Taylor
T86-25 Jamie Anderson
T86-26 Noah Elliott
T86-27 Ashley Wagner
T86-28 Nick Goepper
T86-29 Jaelin Kauf
T86-30 Winter Vinecki
T86-31 Kristen Santos-Griswold
T86-32 Oksana Masters
T86-33 Colby Stevenson
T86-34 Breezy Johnson
T86-35 Tristan Feinberg
T86-36 Lauren Macuga
T86-37 John Shuster
T86-38 Alex Hall
T86-39 River Radamus
T86-40 Christopher Lillis

Winter Blizzard
15 cards
Parallels

USA Flag Refractor /76
Gold Refractor /50
Orange Refractor /25
Black Refractor /10
Red Refractor /5
Superfractor /1
WB-1 Alysa Liu
WB-2 Ilia Malinin
WB-3 Mikaela Shiffrin
WB-4 Nathan Chen
WB-5 Lindsey Vonn
WB-6 Apolo Ohno
WB-7 Jessie Diggins
WB-8 Chloe Kim
WB-9 Shaun White
WB-10 Jordan Stolz
WB-11 Red Gerard
WB-12 Bode Miller
WB-13 Amber Glenn
WB-14 Alex Ferreira
WB-15 Isabeau Levito

Chasing The Rings
50 cards
Parallel

Superfractor /1
CR-1 Ilia Malinin
CR-2 Ilia Malinin
CR-3 Ilia Malinin
CR-4 Ilia Malinin
CR-5 Ilia Malinin
CR-6 Mikaela Shiffrin
CR-7 Mikaela Shiffrin
CR-8 Mikaela Shiffrin
CR-9 Mikaela Shiffrin
CR-10 Mikaela Shiffrin
CR-11 Lindsey Vonn
CR-12 Lindsey Vonn
CR-13 Lindsey Vonn
CR-14 Lindsey Vonn
CR-15 Lindsey Vonn
CR-16 Apolo Ohno
CR-17 Apolo Ohno
CR-18 Apolo Ohno
CR-19 Apolo Ohno
CR-20 Apolo Ohno
CR-21 Chloe Kim
CR-22 Chloe Kim
CR-23 Chloe Kim
CR-24 Chloe Kim
CR-25 Chloe Kim
CR-26 Shaun White
CR-27 Shaun White
CR-28 Shaun White
CR-29 Shaun White
CR-30 Shaun White
CR-31 Jordan Stolz
CR-32 Jordan Stolz
CR-33 Jordan Stolz
CR-34 Jordan Stolz
CR-35 Jordan Stolz
CR-36 Red Gerard
CR-37 Red Gerard
CR-38 Red Gerard
CR-39 Red Gerard
CR-40 Red Gerard
CR-41 Alex Ferreira
CR-42 Alex Ferreira
CR-43 Alex Ferreira
CR-44 Alex Ferreira
CR-45 Alex Ferreira
CR-46 Bode Miller
CR-47 Bode Miller
CR-48 Bode Miller
CR-49 Bode Miller
CR-50 Bode Miller

Hidden Gems
5 cards

HG-1 Ilia Malinin
HG-2 Mikaela Shiffrin
HG-3 Lindsey Vonn
HG-4 Shaun White
HG-5 Chloe Kim

Let's Go
25 cards
Parallel

Superfractor /1
LG-1 Hilary Knight
LG-2 Alysa Liu
LG-3 Ilia Malinin
LG-4 Mikaela Shiffrin
LG-5 Nathan Chen
LG-6 Lindsey Vonn
LG-7 Apolo Ohno
LG-8 Jessie Diggins
LG-9 Chloe Kim
LG-10 Shaun White
LG-11 Jordan Stolz
LG-12 Red Gerard
LG-13 Hailey Langland
LG-14 Evan Bates
LG-15 Madison Chock
LG-16 Erin Jackson
LG-17 Amber Glenn
LG-18 Alex Ferreira
LG-20 Brittany Bowe
LG-21 Bode Miller
LG-22 Jaelin Kauf
LG-23 Winter Vinecki
LG-24 Elana Meyers Taylor
LG-25 Jamie Anderson

Helix
20 cards

HX-1 Hilary Knight
HX-2 Alysa Liu
HX-3 Ilia Malinin
HX-4 Mikaela Shiffrin
HX-5 Nathan Chen
HX-6 Lindsey Vonn
HX-7 Apolo Ohno
HX-8 Jessie Diggins
HX-9 Chloe Kim
HX-10 Shaun White
HX-11 Jordan Stolz
HX-12 Red Gerard
HX-13 Hailey Langland
HX-14 Jamie Anderson
HX-15 Elana Meyers Taylor
HX-16 Erin Jackson
HX-17 Amber Glenn
HX-18 Alex Ferreira
HX-19 Isabeau Levito
HX-20 Bode Miller

Milano Cortina
1 card
Parallel

Superfractor /1
MC-1 Milano Cortina
"""

# ─────────────────────────────────────────────────────────────
# Multi-player sections (card line has "Name1/Name2" format)
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
# Card line regex — handles "86TA-AF" style prefixes too
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

    # Strip inline /N suffix (Jumbo Memorabilia "/1")
    rest = re.sub(r"\s*/\d+\s*$", "", rest).strip()

    # Multi-player: split on "/" (no spaces around slash in this set)
    if section_name in MULTI_PLAYER_SECTIONS and "/" in rest:
        parts = [p.strip() for p in rest.split("/")]
        return [
            {"card_number": card_number, "player": p,
             "team": "U.S. Olympic Team", "is_rookie": False, "subset": None}
            for p in parts
        ]

    return [{"card_number": card_number, "player": rest,
             "team": "U.S. Olympic Team", "is_rookie": False, "subset": None}]


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
# Post-processing: Jumbo Memorabilia /1
# ─────────────────────────────────────────────────────────────

def apply_synthetic_parallels(sections: list):
    for section in sections:
        if section["insert_set"] == "Team USA Jumbo Memorabilia Pieces":
            section["parallels"] = [{"name": "Base", "print_run": 1}]


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
        "set_name": "2026 Topps Chrome U.S. Winter Olympics & Paralympic Team Hopefuls",
        "sport": "Olympics",
        "season": "2026",
        "league": "2026 Winter Olympics",
        "sections": sections,
        "players": players,
    }


# ─────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Parsing 2026 Topps Chrome U.S. Winter Olympics checklist...")

    sections = parse_checklist(CHECKLIST)
    apply_synthetic_parallels(sections)

    output = build_output(sections)

    out_path = "olympics_chrome_parsed.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nSet: {output['set_name']} ({output['season']})")
    print(f"Sections: {len(output['sections'])}")
    for s in output["sections"]:
        print(f"  {s['insert_set']}: {len(s['cards'])} cards, {len(s['parallels'])} parallels")

    print(f"\nTotal players: {len(output['players'])}")

    player_map = {p["player"]: p for p in output["players"]}

    print("\n=== SPOT CHECK: Mikaela Shiffrin ===")
    if "Mikaela Shiffrin" in player_map:
        ms = player_map["Mikaela Shiffrin"]
        st = ms["stats"]
        print(f"  Insert sets:  {st['insert_sets']}")
        print(f"  Unique cards: {st['unique_cards']}")
        print(f"  1/1s:         {st['one_of_ones']}")

    print("\n=== SPOT CHECK: Dual Autograph co-players ===")
    da = next((s for s in output["sections"] if s["insert_set"] == "Dual Autographs"), None)
    if da:
        from collections import Counter
        nums = Counter(c["card_number"] for c in da["cards"])
        for cn, count in nums.items():
            players_on = [c["player"] for c in da["cards"] if c["card_number"] == cn]
            print(f"  {cn}: {' / '.join(players_on)}")

    print("\n=== SPOT CHECK: Chasing The Rings (Ilia Malinin) ===")
    if "Ilia Malinin" in player_map:
        im = player_map["Ilia Malinin"]
        cr_apps = [a for a in im["appearances"] if a["insert_set"] == "Chasing The Rings"]
        print(f"  CR appearances: {len(cr_apps)} (expected 5)")
        for a in cr_apps:
            print(f"    #{a['card_number']} | parallels={len(a['parallels'])}")

    print("\n=== SPOT CHECK: 1986 Topps Autographs card numbers ===")
    t86a = next((s for s in output["sections"] if s["insert_set"] == "1986 Topps Autographs"), None)
    if t86a:
        print(f"  Cards: {len(t86a['cards'])}")
        print(f"  Sample: {t86a['cards'][0]['card_number']} {t86a['cards'][0]['player']}")

    print("\n=== SPOT CHECK: Base Set unique athletes ===")
    base = next((s for s in output["sections"] if s["insert_set"] == "Base Set"), None)
    if base:
        unique_athletes = {c["player"] for c in base["cards"]}
        print(f"  Total cards: {len(base['cards'])} | Unique athletes: {len(unique_athletes)}")
        # Athletes only in 101-200
        athletes_1_100 = {c["player"] for c in base["cards"] if int(c["card_number"]) <= 100}
        athletes_101_200 = {c["player"] for c in base["cards"] if int(c["card_number"]) >= 101}
        only_101_200 = athletes_101_200 - athletes_1_100
        print(f"  Athletes only in 101-200: {sorted(only_101_200)}")
