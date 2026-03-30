#!/usr/bin/env python3
"""Parser for 2025 Topps Universe WWE."""

import json
import re

# ─────────────────────────────────────────────────────────────
# Parallel definitions
# ─────────────────────────────────────────────────────────────

PARALLELS_BASE = [
    {"name": "Flare",                "print_run": None},
    {"name": "Galaxy",               "print_run": None},
    {"name": "Red/White/Blue Stars", "print_run": None},
    {"name": "Rings",                "print_run": None},
    {"name": "Purple Glass",         "print_run": 399},
    {"name": "Blue Pulse",           "print_run": 175},
    {"name": "Green Electric",       "print_run": 125},
    {"name": "Gold Stone",           "print_run": 99},
    {"name": "Blast",                "print_run": 50},
    {"name": "Orange Warp",          "print_run": 25},
    {"name": "Red Magma",            "print_run": 10},
    {"name": "Foilfractor",          "print_run": 1},
]

PARALLELS_AUTO = [
    {"name": "Blue Pulse",     "print_run": 199},
    {"name": "Green Electric", "print_run": 99},
    {"name": "Gold Stone",     "print_run": 50},
    {"name": "Orange Warp",    "print_run": 25},
    {"name": "Red Magma",      "print_run": 10},
    {"name": "Foilfractor",    "print_run": 1},
]

PARALLELS_RELIC_AUTO = [
    {"name": "Gold Stone",  "print_run": 50},
    {"name": "Orange Warp", "print_run": 25},
    {"name": "Red Magma",   "print_run": 10},
    {"name": "Foilfractor", "print_run": 1},
]

PARALLELS_MEM = [
    {"name": "Green Electric", "print_run": 99},
    {"name": "Gold Stone",     "print_run": 50},
    {"name": "Orange Warp",    "print_run": 25},
    {"name": "Red Magma",      "print_run": 10},
    {"name": "Foilfractor",    "print_run": 1},
]

PARALLELS_INSERT = [
    {"name": "Galaxy",         "print_run": None},
    {"name": "Green Electric", "print_run": 99},
    {"name": "Gold Stone",     "print_run": 75},
    {"name": "Orange Warp",    "print_run": 25},
    {"name": "Red Magma",      "print_run": 10},
    {"name": "Foilfractor",    "print_run": 1},
]

PARALLELS_NONE = []

# ─────────────────────────────────────────────────────────────
# Normalizations — fix known checklist typos
# ─────────────────────────────────────────────────────────────

# Applied to the raw line before parsing
LINE_FIXES = {
    "UNR-RDJ Road Dogg Jesse James Legend,": "UNR-RDJ Road Dogg Jesse James, Legend",
}

# Applied to parsed player names
NAME_FIXES = {
    'Jake "The Snake Roberts': 'Jake "The Snake" Roberts',
}

# ─────────────────────────────────────────────────────────────
# Embedded checklists
# ─────────────────────────────────────────────────────────────

BASE_TEXT = """
1 Ivar, Raw
2 The Miz, Raw
3 Rob Gronkowski, WWE
4 Pete Dunne, Raw
5 Joe Gacy, Raw
6 Zelina Vega, Raw
7 Bronson Reed, Raw
8 Uncle Howdy, Raw
9 Ivy Nile, Raw
10 Shaquille O'Neal, WWE
11 Dexter Lumis, Raw
12 Seth "Freakin" Rollins, Raw
13 Katana Chance, Raw
14 Otis, Raw
15 Akira Tozawa, Raw
16 Kiana James, Raw
17 Zoey Stark, Raw
18 "Dirty" Dominik Mysterio, Raw
19 Iyo Sky, Raw
20 Raquel Rodriguez, Raw
21 Brutus Creed, Raw
22 Liv Morgan, Raw
23 Bron Breakker, Raw
24 Dragon Lee, Raw
25 Sami Zayn, Raw
26 Carlito, Raw
27 Scarlett, Raw
28 Drew McIntyre, Smackdown
29 Rey Mysterio, Raw
30 Alba Fyre, Raw
31 Maxxine Dupri, Raw
32 JD McDonagh, Raw
33 Shayna Baszler, Raw
34 Chad Gable, Raw
35 Ludwig Kaiser, Raw
36 Kairi Sane, Raw
37 Erick Rowan, Raw
38 Natalya, Raw
39 Alexa Bliss, Raw
40 Karrion Kross, Raw
41 Pete Rose, WWE
42 CM Punk, Raw
43 Kofi Kingston, Raw
44 Erik, Raw
45 Damian Priest, Smackdown
46 Julius Creed, Raw
47 Asuka, Raw
48 Sheamus, Raw
49 Jey Uso, Raw
50 Cruz Del Toro, Raw
51 Kayden Carter, Raw
52 Finn Bálor, Raw
53 Nikki Cross, Raw
54 Becky Lynch, Raw
55 Tyler Bate, Raw
56 Gunther, Raw
57 Rhea Ripley, Raw
58 Dakota Kai, Raw
59 Lyra Valkyria, Raw
60 Ilja Dragunov, Raw
61 Xavier Woods, Raw
62 Joaquin Wilde, Raw
63 Braun Strowman, Raw
64 Mike Tyson, WWE
65 Kevin Owens, Smackdown
66 Angelo Dawkins, Smackdown
67 Michael Cole, Raw
68 Floyd Mayweather, WWE
69 Big E, Smackdown
70 Johnny Gargano, Smackdown
71 Roman Reigns, Smackdown
72 "The American Nightmare" Cody Rhodes, Smackdown
73 Santos Escobar, Smackdown
74 Jason Kelce, WWE
75 Michin, Smackdown
76 Shotzi, Smackdown
77 Apollo Crews, Smackdown
78 Jacob Fatu, Smackdown
79 Kit Wilson, Smackdown
80 Berto, Smackdown
81 Elton Prince, Smackdown
82 Montez Ford, Smackdown
83 AJ Styles, Smackdown
84 Shinsuke Nakamura, Smackdown
85 Byron Saxton, Smackdown
86 Jade Cargill, Smackdown
87 Naomi, Smackdown
88 Austin Theory, Smackdown
89 Solo Sikoa, Smackdown
90 Candice LeRae, Smackdown
91 LA Knight, Smackdown
92 Bayley, Smackdown
93 Jimmy Uso, Smackdown
94 Nia Jax, Smackdown
95 Andrade, Smackdown
96 Tama Tonga, Smackdown
97 Corey Graves, Smackdown
98 Nick Aldis, Smackdown
99 Bianca Belair, Smackdown
100 Grayson Waller, Smackdown
101 B-Fab, Smackdown
102 Michael Cole, Raw
103 Carmelo Hayes, Smackdown
104 Alex Shelley, Smackdown
105 Piper Niven, Smackdown
106 Angel, Smackdown
107 Randy Orton, Smackdown
108 Cathy Kelley, Raw
109 Zaria, NXT RC
110 Chris Sabin, Smackdown
111 Tiffany Stratton, Smackdown
112 R-Truth, Smackdown
113 Tonga Loa, Smackdown
114 Tommaso Ciampa, Smackdown
115 Chelsea Green, Smackdown
116 Charlotte Flair, Smackdown
117 Stephanie Vaquer, NXT
118 Jordynne Grace, NXT RC
119 Tatum Paxley, NXT
120 Wes Lee, NXT
121 Tony D'Angelo, NXT
122 Axiom, NXT
123 Arianna Grace, NXT
124 Dante Chen, NXT
125 Joe Coffey, NXT
126 Penta, Raw
127 Cora Jade, NXT
128 Lexis King, NXT
129 Oba Femi, NXT
130 Ethan Page, NXT
131 Nathan Frazer, NXT
132 Ridge Holland, NXT
133 Jakara Jackson, NXT
134 Kelani Jordan, NXT
135 Jacy Jayne, NXT
136 Mark Coffey, NXT
137 Trick Williams, NXT
138 Lash Legend, NXT
139 Ricky Saints, NXT
140 Thea Hail, NXT
141 Bronco Nima, NXT
142 Nikkita Lyons, NXT
143 Channing "Stacks" Lorenzo, NXT
144 Roxanne Perez, NXT
145 Noam Dar, NXT
146 Lola Vice, NXT
147 Charlie Dempsey, NXT
148 Gigi Dolin, NXT
149 Riley Osborne, NXT
150 Giulia, Smackdown
151 The Sandman, Legends
152 Diesel, Legends
153 Stone Cold Steve Austin, Legends
154 The Rock, Legends
155 Razor Ramon, Legends
156 Faarooq, Legends
157 Tatanka, Legends
158 Chief Jay Strongbow, Legends
159 Rick Steiner, Legends
160 Jim "The Anvil" Neidhart, Legends
161 Virgil, Legends
162 British Bulldog, Legends
163 Terry Funk, Legends
164 Eddie Guerrero, Legends
165 Rikishi, Legends
166 Bruno Sammartino, Legends
167 Vader, Legends
168 JBL, Legends
169 Road Dogg Jesse James, Legends
170 X-Pac, Legends
171 Kurt Angle, Legends
172 Shockmaster, Legends
173 Diamond Dallas Page, Legends
174 Million Dollar Man Ted DiBiase, Legends
175 Brian Pillman, Legends
176 Lita, Legends
177 Michelle McCool, Legends
178 Brutus Beefcake, Legends
179 Paul Bearer, Legends
180 Rob Van Dam, Legends
181 Batista, Legends
182 Stacy Keibler, Legends
183 Godfather, Legends
184 Rocky Johnson, Legends
185 Chyna, Legends
186 Kane, Legends
187 Shawn Michaels, Legends
188 Billy Gunn, Legends
189 Samu, Legends
190 D'Lo Brown, Legends
191 Torrie Wilson, Legends
192 Mankind, Legends
193 William Regal, Legends
194 Dusty Rhodes, Legends
195 Triple H, Legends
196 The Boogeyman, Legends
197 The Hurricane, Legends
198 Great Muta, Legends
199 Scott Steiner, Legends
200 Booker T, Legends
"""

EVENT_VAR_TEXT = """
201 John Cena, Legend
202 "The American Nightmare" Cody Rhodes, Smackdown
203 Hulk Hogan, Legend
204 Batista, Legend
205 Triple H, Legend
206 Drew McIntyre, Smackdown
207 Becky Lynch, Raw
208 Randy Orton, Smackdown
209 Yokozuna, Legend
210 Undertaker, Legend
211 Eddie Guerrero, Legend
212 Shinsuke Nakamura, Smackdown
213 Shawn Michaels, Legend
214 Asuka, Raw
215 Stone Cold Steve Austin, Legend
216 John Cena, Legend
217 Charlotte Flair, Smackdown
218 Sami Zayn, Raw
219 Hulk Hogan, Legend
220 Mankind, Legend
221 Big John Studd, Legend
222 Umaga, Legend
223 Ken Shamrock, Legend
224 Rhea Ripley, Raw
225 AJ Styles, Smackdown
226 The Rock, Legend
227 Jey Uso, Raw
228 Ultimate Warrior, Legend
229 Kevin Owens, Smackdown
230 Trish Stratus, Legend
231 Bray Wyatt, Legend
232 Bret "Hit Man" Hart, Legend
233 Cowboy Bob Orton, Legend
234 Rowdy Roddy Piper, Legend
235 Undertaker, Legend
236 Kofi Kingston, Raw
237 Kurt Angle, Legend
238 Bam Bam Bigelow, Legend
239 Razor Ramon, Legend
240 Seth "Freakin" Rollins, Raw
241 D-Von Dudley, Legend
242 The Miz, Raw
243 Eddie Guerrero, Legend
244 Randy Orton, Smackdown
245 Stone Cold Steve Austin, Legend
246 Jimmy Uso, Smackdown
247 Triple H, Legend
248 Sycho Sid, Legend
249 Bubba Ray Dudley, Legend
250 Bianca Belair, Smackdown
251 Rey Mysterio, Raw
252 Hollywood Hulk Hogan, Legend
253 Roman Reigns, Smackdown
254 "The American Nightmare" Cody Rhodes, Smackdown
255 Shawn Michaels, Legend
256 "The American Nightmare" Cody Rhodes, Smackdown
257 Rob Van Dam, Legend
258 Damian Priest, Smackdown
259 Randy Orton, Smackdown
260 Sheamus, Raw
261 Alexa Bliss, Raw
262 CM Punk, Raw
263 Iyo Sky, Raw
264 Seth "Freakin" Rollins, Raw
265 Austin Theory, Smackdown
266 The Miz, Raw
267 Damian Priest, Smackdown
268 Asuka, Raw
269 John Cena, Legend
270 Tiffany Stratton, Smackdown
271 Roman Reigns, Smackdown
272 Triple H, Legend
273 Bret "Hit Man" Hart, Legend
274 The Fiend Bray Wyatt, Legend
275 Stone Cold Steve Austin, Legend
276 Seth "Freakin" Rollins, Raw
277 Lex Luger, Legend
278 John Cena, Legend
279 Mr. Perfect, Legend
280 Ultimate Warrior, Legend
281 Randy Orton, Smackdown
282 Dirty Dominik Mysterio, Raw
283 Trish Stratus, Legend
284 Shawn Michaels, Legend
285 Ravishing Rick Rude, Legend
286 Becky Lynch, Raw
287 Finn Bálor, Raw
288 Ultimate Warrior, Legend
289 Big Boss Man, Legend
290 Undertaker, Legend
291 Kane, Legend
292 Kurt Angle, Legend
293 Sheamus, Raw
294 The Rock, Legend
295 Stone Cold Steve Austin, Legend
296 Sycho Sid, Legend
297 Undertaker, Legend
298 Batista, Legend
299 Shawn Michaels, Legend
300 Bret "Hit Man" Hart, Legend
"""

UNIVERSE_AUTO_TEXT = """
UNA-ADP Adam Pearce, Raw
UNA-ALB Albert, Legends
UNA-ARI Adriana Rizzo, NXT
UNA-AVA Ava, NXT
UNA-BFA B-Fab, Smackdown
UNA-BIG Big E, Smackdown
UNA-BJE Brooks Jensen, NXT
UNA-BLO Brother Love, Legends
UNA-BLU Buschwhacker Luke, Legends
UNA-BNI Bronco Nima, NXT
UNA-CKE Cathy Kelley, Raw
UNA-CLR Candice LeRae, Smackdown
UNA-EEN Edris Enofe, NXT
UNA-EPA Ethan Page, NXT
UNA-FHE Fallon Henley, NXT
UNA-GMU Great Muta, Legends
UNA-HWA Hank Walker, NXT
UNA-IVA Ivar, Raw
UNA-JBE Javier Bernal, NXT
UNA-JGA Joe Gacy, Raw
UNA-JLA Jerry Lawler, Legends
UNA-KJA Kiana James, Raw
UNA-KSH Ken Shamrock, Legends
UNA-LLE Lash Legend, NXT
UNA-MBL Malik Blade, NXT
UNA-MCC Michelle McCool, Legends
UNA-MCO Mark Coffey, NXT
UNA-MIC Michael Cole, Raw
UNA-NAL Nick Aldis, Smackdown
UNA-OME Oro Mensah, NXT
UNA-RDO Road Dogg Jesse James, Legends
UNA-RHO Ridge Holland, NXT
UNA-RRO Raquel Rodriguez, Raw
UNA-SHO Shotzi, Smackdown
UNA-SVR Stephanie Vaquer, NXT
UNA-TBO The Boogeyman, Legends
UNA-TBR Tyler Breeze, Legends
UNA-TGF The Godfather, Legends
UNA-THA Thea Hail, NXT
UNA-TLO Teddy Long, Legends
UNA-TOL Tanga Loa, Smackdown
UNA-TPA Tatum Paxley, NXT
UNA-TYP Typhoon, Legends
"""

LEGENDS_AUTO_TEXT = """
LGA-BHM Bret "Hit Man" Hart, Legends
LGA-BOT Booker T, Legends
LGA-BRA Bradshaw, Legends
LGA-BRD Bubba Ray Dudley, Legends
LGA-CBO Cowboy Bob Orton, Legends
LGA-DDP Diamond Dallas Page, Legends
LGA-DVD D-Von Dudley, Legends
LGA-FAA Faarooq, Legends
LGA-HUH Hulk Hogan, Legends
LGA-JCE John Cena, Legends
LGA-JRO Jake "The Snake" Roberts, Legends
LGA-KAN Kane, Legends
LGA-KNA Kevin Nash, Legends
LGA-KUA Kurt Angle, Legends
LGA-LIT Lita, Legends
LGA-LLU Lex Luger, Legends
LGA-MAN Mankind, Legends
LGA-PAC X-Pac, Legends
LGA-RIK Rikishi, Legends
LGA-RST Rick Steiner, Legends
LGA-RVD Rob Van Dam, Legends
LGA-SCA Stone Cold Steve Austin, Legends
LGA-SKI Stacy Keibler, Legends
LGA-SMI Shawn Michaels, Legends
LGA-TSA The Sandman, Legends
LGA-TST Trish Stratus, Legends
LGA-TWI Torrie Wilson, Legends
LGA-UND Undertaker, Legends
LGA-WBA Wade Barrett, Legends
LGA-WRE William Regal, Legends
"""

NEXT_LEVEL_AUTO_TEXT = """
NLA-ACH Andre Chase, NXT
NLA-AGR Arianna Grace, NXT
NLA-CDE Charlie Dempsey, NXT
NLA-DCH Dante Chen, NXT
NLA-ETH Eddy Thorpe, NXT
NLA-GDO Gigi Dolin, NXT
NLA-JJA Jacy Jayne, NXT
NLA-JPA Jaida Parker, NXT
NLA-JVE Je'Von Evans, NXT
NLA-LCR Luca Crusifino, NXT
NLA-LKI Lexis King, NXT
NLA-LVI Lola Vice, NXT
NLA-NDA Noam Dar, NXT
NLA-NLY Nikkita Lyons, NXT
NLA-SRU Sol Ruca, NXT
NLA-SSP Shawn Spears, NXT
NLA-TDA Tony D'Angelo, NXT
NLA-TWI Trick Williams, NXT
NLA-WLE Wes Lee, NXT
"""

CENA_AUTO_TEXT = """
CCA-10 John Cena, WWE
CCA-11 John Cena, WWE
CCA-12 John Cena, WWE
CCA-13 John Cena, WWE
"""

ROCK_RETRO_TEXT = """
RRA-4 The Rock, Legend
"""

TRIPLE_H_TRIBUTE_TEXT = """
TTA-3 Triple H, Legend
TTA-4 Triple H, Legend
TTA-5 Triple H, Legend
"""

RIVALRY_SIG_TEXT = """
SSR-TC Triple H, Legend
SSR-TH Triple H, Legend
"""

SRS_TEXT = """
SRS-ABI Alexa Bliss, Raw
SRS-AJS AJ Styles, Smackdown
SRS-ATA Ashante "Thee" Adonis, Smackdown
SRS-BBR Bron Breakker, Smackdown
SRS-BST Braun Strowman, Raw
SRS-CFL Charlotte Flair, Smackdown
SRS-CGA Chad Gable, Raw
SRS-CHA Carmelo Hayes, Smackdown
SRS-CMP CM Punk, Raw
SRS-DLE Dragon Lee, Raw
SRS-DMY Dirty Dominik Mysterio, Raw
SRS-INI Ivy Nile, Raw
SRS-ISK Iyo Sky, Raw
SRS-JCE Jade Cargill, Smackdown
SRS-JEU Jey Uso, Raw
SRS-JIU Jimmy Uso, Smackdown
SRS-JWI Joaquin Wilde, Raw
SRS-KKR Karrion Kross, Raw
SRS-LVA Lyra Valkyria, Raw
SRS-MDU Maxxine Dupri, Raw
SRS-MIC Michin, Smackdown
SRS-NAO Naomi, Smackdown
SRS-PNI Piper Niven, Smackdown
SRS-RMY Rey Mysterio, Raw
SRS-ROR Randy Orton, Smackdown
SRS-SCA Scarlett, Raw
SRS-SFR Seth "Freakin" Rollins, Raw
SRS-SSI Solo Sikoa, Smackdown
SRS-TST Tiffany Stratton, Smackdown
SRS-ZST Zoey Stark, Raw
SRS-ZVE Zelina Vega, Raw
"""

WORLDWIDE_RELIC_TEXT = """
WRA-ALB Alba Fyre, Raw
WRA-AND Andrade, Smackdown
WRA-ASU Asuka, Raw
WRA-ATO Akira Tozawa, Raw
WRA-BLY Becky Lynch, Raw
WRA-CAR Carlito, Raw
WRA-DLE Dragon Lee, Raw
WRA-DMI Drew McIntyre, Smackdown
WRA-FBA Finn Bálor, Raw
WRA-KOW Kevin Owens, Smackdown
WRA-LKA Ludwig Kaiser, Raw
WRA-NAT Natalya, Raw
WRA-OMO Omos, Raw
WRA-RRI Rhea Ripley, Raw
WRA-SES Santos Escobar, Smackdown
WRA-SHE Sheamus, Raw
WRA-TRW Trick Williams, NXT
"""

TAG_TEAM_TEXT = """
TTA-AB Angel/Berto, Smackdown
TTA-AKS Asuka/Kairi Sane, Raw
TTA-ANF Nathan Frazer/Axiom, NXT
TTA-ATO Akira Tozawa/Otis, Raw
TTA-BC Bianca Belair/Jade Cargill, Smackdown
TTA-BMD Finn Bálor/JD McDonagh, Raw
TTA-CC Julius Creed/Brutus Creed, Raw
TTA-DB Tyler Bate/Pete Dunne, Raw
TTA-DF Angelo Dawkins/Montez Ford, Smackdown
TTA-FT Tama Tonga/Jacob Fatu, Smackdown
TTA-GC Johnny Gargano/Tommaso Ciampa, Smackdown
TTA-GN Chelsea Green/Piper Niven, Smackdown
TTA-KCC Kayden Carter/Katana Chance, Raw
TTA-OGB Jimmy Uso/Jey Uso, Smackdown/Raw
TTA-PW Kit Wilson/Elton Prince, Smackdown
TTA-TW Grayson Waller/Austin Theory, Smackdown
"""

TITLE_MARKS_TEXT = """
TMA-ANC "The American Nightmare" Cody Rhodes, Smackdown
TMA-AND Andrade, Smackdown
TMA-BAY Bayley, Smackdown
TMA-BBR Bron Breakker, Smackdown
TMA-BLY Becky Lynch, Raw
TMA-DPR Damian Priest, Smackdown
TMA-EPA Ethan Page, NXT
TMA-GUN Gunther, Raw
TMA-KJO Kelani Jordan, NXT
TMA-LAK LA Knight, Smackdown
TMA-LMO Liv Morgan, Raw
TMA-NJA Nia Jax, Smackdown
TMA-OFE Oba Femi, NXT
TMA-RPE Roxanne Perez, NXT
TMA-RRE Roman Reigns, Smackdown
"""

UNIVERSE_RELICS_TEXT = """
UNR-ATO Akira Tozawa, Raw
UNR-BAT Batista, Legend
UNR-BCR Brutus Creed, Raw
UNR-BDA Bo Dallas, Raw
UNR-BGU Billy Gunn, Legend
UNR-BRD Bubba Ray Dudley, Legend
UNR-BWY Bray Wyatt, Legend
UNR-CDT Cruz Del Toro, Raw
UNR-DVD D-Von Dudley, Legend
UNR-EPA Ethan Page, NXT
UNR-JCE John Cena, Legend
UNR-JCR Julius Creed, Raw
UNR-JEU Jey Uso, Raw
UNR-JIU Jimmy Uso, Smackdown
UNR-KAN Kane, Legend
UNR-KJO Kelani Jordan, NXT
UNR-KKR Karrion Kross, Raw
UNR-LIT Lita, Legend
UNR-LKA Ludwig Kaiser, Raw
UNR-NAO Naomi, Smackdown
UNR-NAT Natalya, Raw
UNR-NLY Nikkita Lyons, NXT
UNR-OTI Otis, Raw
UNR-RDJ Road Dogg Jesse James, Legend
UNR-ROR Randy Orton, Smackdown
UNR-RPE Roxanne Perez, NXT
UNR-RVD Rob Van Dam, Legend
UNR-SMS Sheamus, Raw
UNR-STA Stardust, Smackdown
UNR-TDA Tony D'Angelo, NXT
UNR-TST Trish Stratus, Legend
UNR-TWI Trick Williams, NXT
UNR-WBA Wade Barrett, Legend
"""

TRIPLE_RELIC_TEXT = """
TRS-BBR Bron Breakker, Raw
TRS-BRE Bronson Reed, Raw
TRS-BST Braun Strowman, Raw
TRS-CGA Chad Gable, Raw
TRS-CMP CM Punk, Raw
TRS-DMI Drew McIntyre, Smackdown
TRS-DMY Dirty Dominik Mysterio, Raw
TRS-DPR Damian Priest, Smackdown
TRS-JUS Jey Uso, Raw
TRS-KKI Kofi Kingston, Raw
TRS-LMO Liv Morgan, Raw
TRS-RMY Rey Mysterio, Raw
TRS-RRI Rhea Ripley, Raw
TRS-SFR Seth "Freakin" Rollins, Raw
TRS-SZA Sami Zayn, Raw
"""

WWE_AUTH_TEXT = """
WAU-AJS AJ Styles, Smackdown
WAU-ATH Austin Theory, Smackdown
WAU-BAT Batista, Legend
WAU-BAY Bayley, Smackdown
WAU-BBE Bianca Belair, Smackdown
WAU-BLY Becky Lynch, Raw
WAU-BWY The Fiend Bray Wyatt, Legend
WAU-CMP CM Punk, Raw
WAU-CRH "The American Nightmare" Cody Rhodes, Smackdown
WAU-GUN Gunther, Raw
WAU-KAN Kane, Legend
WAU-LAK LA Knight, Smackdown
WAU-RKO Randy Orton, Smackdown
WAU-RRE Roman Reigns, Smackdown
WAU-RRI Rhea Ripley, Raw
WAU-SCS Stone Cold Steve Austin, Legend
WAU-SFR Seth "Freakin" Rollins, Raw
WAU-TRH Triple H, Legend
WAU-TRO The Rock, Legend
WAU-TST Trish Stratus, Legend
WAU-UND Undertaker, Legend
"""

RINGSIDE_TEXT = """
RSR-ABI Alexa Bliss, Raw
RSR-AJS AJ Styles, Smackdown
RSR-ASU Asuka, Raw
RSR-BAY Bayley, Smackdown
RSR-BLY Becky Lynch, Raw
RSR-DKA Dakota Kai, Raw
RSR-FBA Finn Bálor, Raw
RSR-JCE John Cena, Legend
RSR-JGA Johnny Gargano, Smackdown
RSR-KAN Kane, Legend
RSR-KKI Kofi Kingston, Raw
RSR-KOW Kevin Owens, Smackdown
RSR-RKO Randy Orton, Smackdown
RSR-RRE Roman Reigns, Smackdown
RSR-SFR Seth "Freakin" Rollins, Raw
RSR-SHE Sheamus, Smackdown
RSR-SZA Sami Zayn, Raw
RSR-TRH Triple H, Legend
RSR-TRO The Rock, Legend
RSR-UND Undertaker, Legend
"""

RING_LEADERS_TEXT = """
RL-1 Mick Foley, Legends
RL-2 Bret "Hit Man" Hart, Legends
RL-3 Trish Stratus, Legends
RL-4 Undertaker, Legends
RL-5 Stone Cold Steve Austin, Legends
RL-6 Becky Lynch, Raw
RL-7 The Rock, Legends
RL-8 Batista, Legends
RL-9 Asuka, Raw
RL-10 Bruno Sammartino, Legends
RL-11 Charlotte Flair, WWE
RL-12 Roman Reigns, Smackdown
RL-13 Alexa Bliss, Smackdown
RL-14 Hulk Hogan, Legends
RL-15 CM Punk, Raw
RL-16 Seth "Freakin" Rollins, Raw
RL-17 The Sandman, Legends
RL-18 Bayley, Smackdown
RL-19 John Cena, Legends
RL-20 Kane, Legends
RL-21 Kurt Angle, Legends
RL-22 Braun Strowman, Smackdown
RL-23 Triple H, Legends
RL-24 Kofi Kingston, Raw
RL-25 Kevin Nash, Legends
RL-26 Bianca Belair, Smackdown
RL-27 Randy Orton, Smackdown
RL-28 The Miz, Smackdown
RL-29 Rhea Ripley, Raw
RL-30 Booker T, Legends
"""

STAR_PORTAL_TEXT = """
SPO-1 Liv Morgan, Raw
SPO-2 "The American Nightmare" Cody Rhodes, Smackdown
SPO-3 Bayley, Raw
SPO-4 Finn Bálor, Raw
SPO-5 Cora Jade, NXT
SPO-6 Jey Uso, Raw
SPO-7 Oba Femi, NXT
SPO-8 Kevin Owens, Smackdown
SPO-9 Bron Breakker, Raw
SPO-10 Bianca Belair, Smackdown
SPO-11 Gunther, Raw
SPO-12 Austin Theory, Raw
SPO-13 CM Punk, Raw
SPO-14 Solo Sikoa, Smackdown
SPO-15 Rhea Ripley, Raw
SPO-16 Roman Reigns, Smackdown
SPO-17 Trick Williams, NXT
SPO-18 Braun Strowman, Raw
SPO-19 Roxanne Perez, NXT
SPO-20 Jade Cargill, Smackdown
SPO-21 LA Knight, Smackdown
SPO-22 Asuka, Raw
SPO-23 Tiffany Stratton, Smackdown
SPO-24 Ethan Page, NXT
SPO-25 Seth "Freakin" Rollins, Raw
"""

INTL_IMPACT_TEXT = """
IIM-1 Gunther, Raw
IIM-2 Seth "Freakin" Rollins, Raw
IIM-3 British Bulldog, Legend
IIM-4 Damian Priest, Smackdown
IIM-5 Rhea Ripley, Raw
IIM-6 Xavier Woods, Raw
IIM-7 Sami Zayn, Raw
IIM-8 Randy Orton, Smackdown
IIM-9 Drew McIntyre, Smackdown
IIM-10 John Cena, Legend
IIM-11 Zelina Vega, Raw
IIM-12 Austin Theory, Smackdown
IIM-13 Becky Lynch, Raw
IIM-14 Iyo Sky, Raw
IIM-15 Big E, Smackdown
IIM-16 Asuka, Raw
IIM-17 Triple H, Legend
IIM-18 Roman Reigns, Smackdown
IIM-19 Cactus Jack, Legend
IIM-20 Bret "Hit Man" Hart, Legend
"""

DAZZLING_TEXT = """
DDE-1 John Cena, Legend
DDE-2 Roman Reigns, Smackdown
DDE-3 Jade Cargill, Smackdown
DDE-4 Kane, Legend
DDE-5 Wyatt Sicks, Raw
DDE-6 Solo Sikoa, Smackdown
DDE-7 Great Khali, Legend
DDE-8 Undertaker, Legend
DDE-9 The Rock, Legend
DDE-10 Shinsuke Nakamura, Smackdown
DDE-11 Seth "Freakin" Rollins, Raw
DDE-12 Kevin Owens, Smackdown
DDE-13 Carlito, Raw
DDE-14 Umaga, Legend
DDE-15 Braun Strowman, Raw
DDE-16 Rey Mysterio, Raw
DDE-17 Vader, Legend
DDE-18 Asuka, Raw
DDE-19 Scott Hall, Legend
DDE-20 AJ Styles, Smackdown
"""

FACTIONS_TEXT = """
FFA-1 D-Generation X, Legend
FFA-2 The Bloodline, Smackdown
FFA-3 The New Day, Raw
FFA-4 nWo, Legend
FFA-5 Wyatt Sicks, Raw
"""

RAGE_TEXT = """
RA-1 Braun Strowman, Raw
RA-2 Ken Shamrock, Legend
RA-3 Uncle Howdy, Smackdown
RA-4 Nia Jax, Smackdown
RA-5 Kevin Owens, Smackdown
RA-6 Drew McIntyre, Smackdown
RA-7 Asuka, Raw
RA-8 CM Punk, Raw
RA-9 "The American Nightmare" Cody Rhodes, Smackdown
RA-10 Kurt Angle, Legend
RA-11 Triple H, Legend
RA-12 Stone Cold Steve Austin, Legend
RA-13 Bronson Reed, Raw
RA-14 Batista, Legend
RA-15 Sheamus, Raw
RA-16 Randy Orton, Smackdown
RA-17 Sycho Sid, Legend
RA-18 Kane, Legend
RA-19 Charlotte Flair, Smackdown
RA-20 Undertaker, Legend
RA-21 Becky Lynch, Raw
RA-22 Otis, Raw
RA-23 John Cena, Legend
RA-24 Ultimate Warrior, Legend
RA-25 Shinsuke Nakamura, Smackdown
RA-26 Rhea Ripley, Raw
RA-27 Finn Bálor, Raw
RA-28 Karrion Kross, Raw
RA-29 Roman Reigns, Smackdown
RA-30 Gunther, Raw
"""

NAMESAKES_TEXT = """
NMS-1 Charlotte Flair, Smackdown
NMS-2 CM Punk, Raw
NMS-3 Rikishi, Legend
NMS-4 John Cena, Legend
NMS-5 Lita, Legend
NMS-6 Vader, Legend
NMS-7 Kurt Angle, Legend
NMS-8 Kane, Legend
NMS-9 Booker T, Legend
NMS-10 Hulk Hogan, Legend
NMS-11 Seth "Freakin" Rollins, Raw
NMS-12 Alexa Bliss, Raw
NMS-13 Undertaker, Legend
NMS-14 AJ Styles, Smackdown
NMS-15 Roman Reigns, Smackdown
NMS-16 Jake "The Snake" Roberts, Legend
NMS-17 Asuka, Raw
NMS-18 Stone Cold Steve Austin, Legend
NMS-19 Chyna, Legend
NMS-20 Batista, Legend
NMS-21 Rowdy Roddy Piper, Legend
NMS-22 Razor Ramon, Legend
NMS-23 Kofi Kingston, Raw
NMS-24 Randy Orton, Smackdown
NMS-25 Becky Lynch, Raw
NMS-26 Rob Van Dam, Legend
NMS-27 Shawn Michaels, Legend
NMS-28 Rhea Ripley, Raw
NMS-29 Rey Mysterio, Raw
NMS-30 Ultimate Warrior, Legend
NMS-31 Natalya, Raw
NMS-32 Bret "Hit Man" Hart, Legend
NMS-33 Trish Stratus, Legend
NMS-34 Naomi, Smackdown
NMS-35 Mick Foley, Legend
NMS-36 Stephanie Vaquer, NXT
NMS-37 Mr. Perfect, Legend
NMS-38 The Rock, Legend
NMS-39 Bray Wyatt, Legend
NMS-40 Triple H, Legend
"""

FOREIGN_OBJ_TEXT = """
FOB-1 Triple H, Legend
FOB-2 The Boogeyman, Legend
FOB-3 D-Von Dudley, Legend
FOB-4 Honky Tonk Man, Legend
FOB-5 Mankind, Legend
FOB-6 Paul Bearer, Legend
FOB-7 Seth "Freakin" Rollins, Raw
FOB-8 Randy Orton, Smackdown
FOB-9 Shawn Michaels, Legend
FOB-10 Undertaker, Legend
FOB-11 Mick Foley, Legend
FOB-12 Alexa Bliss, Raw
FOB-13 Bray Wyatt, Legend
FOB-14 Cactus Jack, Legend
FOB-15 Jake "The Snake" Roberts, Legend
FOB-16 Xavier Woods, Raw
FOB-17 Braun Strowman, Raw
FOB-18 Sami Zayn, Raw
FOB-19 The Sandman, Legend
FOB-20 Bayley, Smackdown
"""

REMARKABLE_TEXT = """
RRE-1 The Rock, Legend
RRE-2 "The American Nightmare" Cody Rhodes, Smackdown
RRE-3 Diesel, Legend
RRE-4 Seth "Freakin" Rollins, Raw
RRE-5 Ultimate Warrior, Legend
RRE-6 Roman Reigns, Smackdown
RRE-7 Undertaker, Legend
RRE-8 John Cena, Legend
RRE-9 Bray Wyatt, Legend
RRE-10 CM Punk, Raw
"""

WWE_THEN_TEXT = """
WTH-1 Stone Cold Steve Austin, Legend
WTH-2 The Rock, Legend
WTH-3 Undertaker, Legend
WTH-4 Hulk Hogan, Legend
WTH-5 John Cena, Legend
"""

WWE_NOW_TEXT = """
WNO-1 LA Knight, Smackdown
WNO-2 Seth "Freakin" Rollins, Raw
WNO-3 Bron Breakker, Raw
WNO-4 Bianca Belair, Smackdown
WNO-5 Drew McIntyre, Raw
WNO-6 Uncle Howdy, Raw
WNO-7 Rhea Ripley, Raw
WNO-8 "The American Nightmare" Cody Rhodes, Smackdown
WNO-9 Finn Bálor, Raw
WNO-10 Becky Lynch, Raw
WNO-11 Gunther, Raw
WNO-12 Randy Orton, Smackdown
WNO-13 Jade Cargill, Smackdown
WNO-14 Roman Reigns, Smackdown
WNO-15 Tiffany Stratton, Smackdown
WNO-16 CM Punk, Raw
WNO-17 Charlotte Flair, Smackdown
WNO-18 Kevin Owens, Smackdown
WNO-19 The Miz, Smackdown
WNO-20 Liv Morgan, Raw
"""

WWE_FOREVER_TEXT = """
WFO-1 Eddie Guerrero, Legend
WFO-2 Yokozuna, Legend
WFO-3 Ultimate Warrior, Legend
WFO-4 Bruno Sammartino, Legend
WFO-5 Bray Wyatt, Legend
"""

WWE_TOGETHER_TEXT = """
WTO-1 Shawn Michaels/Triple H, Legend
WTO-2 The Rock/Mankind, Legend
WTO-3 D-Von Dudley/Bubba Ray Dudley, Legend
WTO-4 Jimmy Uso/Jey Uso, Smackdown
WTO-5 Undertaker/Kane, Legend
WTO-6 Rick Steiner/Scott Steiner, Legend
WTO-7 Road Dogg Jesse James/Billy Gunn, Legend
WTO-8 Jim Neidhart/Bret "Hit Man" Hart, Legend
WTO-9 Johnny Gargano/Tommaso Ciampa, Smackdown
WTO-10 Montez Ford/Angelo Dawkins, Smackdown
"""

MASKED_TEXT = """
MAS-1 Dragon Lee, Raw
MAS-2 Kane, Legend
MAS-3 Mankind, Legend
MAS-4 Uncle Howdy, Smackdown
MAS-5 Rey Mysterio, Legend
MAS-6 The Ultimate Warrior, Legend
MAS-7 Demon Finn Bálor, Raw
MAS-8 The Fiend Bray Wyatt, Legend
MAS-9 The Boogeyman, Legend
MAS-10 Axiom, Smackdown
"""

# ─────────────────────────────────────────────────────────────
# Section definitions
# ─────────────────────────────────────────────────────────────
# (name, text, parallels, allow_rc, multi_player)

SECTION_DEFS = [
    ("Base Set",                          BASE_TEXT,             PARALLELS_BASE,     True,  False),
    ("Event Variations",                  EVENT_VAR_TEXT,        PARALLELS_NONE,     False, False),
    ("Universe Autographs",               UNIVERSE_AUTO_TEXT,    PARALLELS_AUTO,     False, False),
    ("Legends Autographs",                LEGENDS_AUTO_TEXT,     PARALLELS_AUTO,     False, False),
    ("Next Level Autographs",             NEXT_LEVEL_AUTO_TEXT,  PARALLELS_AUTO,     False, False),
    ("Celebrating Cena Autographs",       CENA_AUTO_TEXT,        PARALLELS_NONE,     False, False),
    ("The Rock Retrospective Autographs", ROCK_RETRO_TEXT,       PARALLELS_NONE,     False, False),
    ("Triple H Tribute Autographs",       TRIPLE_H_TRIBUTE_TEXT, PARALLELS_NONE,     False, False),
    ("Superstar Rivalry Signatures",      RIVALRY_SIG_TEXT,      PARALLELS_NONE,     False, False),
    ("Superstar Relic Signatures",        SRS_TEXT,              PARALLELS_RELIC_AUTO, False, False),
    ("Worldwide Relic Autographs",        WORLDWIDE_RELIC_TEXT,  PARALLELS_RELIC_AUTO, False, False),
    ("Tag Team Dual Autographs",          TAG_TEAM_TEXT,         PARALLELS_RELIC_AUTO, False, True),
    ("Title Marks Relic Autographs",      TITLE_MARKS_TEXT,      PARALLELS_RELIC_AUTO, False, False),
    ("Universe Relics",                   UNIVERSE_RELICS_TEXT,  PARALLELS_MEM,      False, False),
    ("Triple Superstar Relics",           TRIPLE_RELIC_TEXT,     PARALLELS_MEM,      False, False),
    ("WWE Authentics",                    WWE_AUTH_TEXT,         PARALLELS_MEM,      False, False),
    ("Ringside Relics",                   RINGSIDE_TEXT,         PARALLELS_MEM,      False, False),
    ("Ring Leaders",                      RING_LEADERS_TEXT,     PARALLELS_INSERT,   False, False),
    ("Star Portal",                       STAR_PORTAL_TEXT,      PARALLELS_INSERT,   False, False),
    ("International Impact",              INTL_IMPACT_TEXT,      PARALLELS_INSERT,   False, False),
    ("Dazzling Debuts",                   DAZZLING_TEXT,         PARALLELS_INSERT,   False, False),
    ("Forever Factions",                  FACTIONS_TEXT,         PARALLELS_INSERT,   False, False),
    ("Rage",                              RAGE_TEXT,             PARALLELS_INSERT,   False, False),
    ("Namesakes",                         NAMESAKES_TEXT,        PARALLELS_INSERT,   False, False),
    ("Foreign Objects",                   FOREIGN_OBJ_TEXT,      PARALLELS_INSERT,   False, False),
    ("Remarkable Returns",                REMARKABLE_TEXT,       PARALLELS_INSERT,   False, False),
    ("WWE Then",                          WWE_THEN_TEXT,         PARALLELS_NONE,     False, False),
    ("WWE Now",                           WWE_NOW_TEXT,          PARALLELS_NONE,     False, False),
    ("WWE Forever",                       WWE_FOREVER_TEXT,      PARALLELS_NONE,     False, False),
    ("WWE Together",                      WWE_TOGETHER_TEXT,     PARALLELS_NONE,     False, True),
    ("Masked",                            MASKED_TEXT,           PARALLELS_NONE,     False, False),
]

# ─────────────────────────────────────────────────────────────
# Parser
# ─────────────────────────────────────────────────────────────

CARD_LINE_RE = re.compile(r'^(\d+|[A-Z][A-Z0-9]*-[A-Z0-9]+)\s+(.+)$')


def parse_card_line(raw_line: str, allow_rc: bool, multi_player: bool):
    """
    Parse a single card line.
    Returns a list of card dicts (one per player, >1 for multi-player cards),
    or empty list if the line should be skipped.
    """
    line = raw_line.strip()
    if not line:
        return []

    # Apply known line fixes
    line = LINE_FIXES.get(line, line)

    m = CARD_LINE_RE.match(line)
    if not m:
        return []

    card_number = m.group(1)
    rest = m.group(2).strip()

    # Split player(s) and brand(s) on the LAST ", "
    idx = rest.rfind(", ")
    if idx == -1:
        return []

    players_str = rest[:idx].strip()
    brands_str = rest[idx + 2:].strip()

    # RC detection (only for base set)
    is_rookie = False
    if allow_rc and brands_str.endswith(" RC"):
        is_rookie = True
        brands_str = brands_str[:-3].strip()

    if multi_player and "/" in players_str:
        player_names = [p.strip() for p in players_str.split("/")]
        if "/" in brands_str:
            brand_list = [b.strip() for b in brands_str.split("/")]
        else:
            brand_list = [brands_str] * len(player_names)

        cards = []
        for player, brand in zip(player_names, brand_list):
            player = NAME_FIXES.get(player, player)
            cards.append({
                "card_number": card_number,
                "player": player,
                "team": brand,
                "is_rookie": False,
                "subset": None,
            })
        return cards
    else:
        player = NAME_FIXES.get(players_str, players_str)
        return [{
            "card_number": card_number,
            "player": player,
            "team": brands_str,
            "is_rookie": is_rookie,
            "subset": None,
        }]


def parse_section(text: str, allow_rc: bool = False, multi_player: bool = False) -> list:
    cards = []
    for line in text.splitlines():
        cards.extend(parse_card_line(line, allow_rc=allow_rc, multi_player=multi_player))
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

    players = []
    for pname in sorted(player_index.keys()):
        data = player_index[pname]
        players.append({
            "player": pname,
            "appearances": data["appearances"],
            "stats": compute_stats(data["appearances"]),
        })

    return {
        "set_name": "2025 Topps Universe WWE",
        "sport": "Wrestling",
        "season": "2025",
        "league": "WWE",
        "sections": sections,
        "players": players,
    }


# ─────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Parsing 2025 Topps Universe WWE checklist...")

    sections = []
    for name, text, parallels, allow_rc, multi_player in SECTION_DEFS:
        cards = parse_section(text, allow_rc=allow_rc, multi_player=multi_player)
        sections.append({
            "insert_set": name,
            "parallels": parallels,
            "cards": cards,
        })

    output = build_output(sections)

    out_path = "wwe_universe_parsed.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nSet: {output['set_name']} ({output['season']})")
    print(f"Sections: {len(output['sections'])}")
    for s in output["sections"]:
        n = len(s["cards"])
        p = len(s["parallels"])
        print(f"  {s['insert_set']:<40} {n:>4} cards  {p} parallels")

    print(f"\nTotal players: {len(output['players'])}")

    player_map = {p["player"]: p for p in output["players"]}

    # Base set spot checks
    base = next(s for s in output["sections"] if s["insert_set"] == "Base Set")
    ev = next(s for s in output["sections"] if s["insert_set"] == "Event Variations")
    rc_count = sum(1 for c in base["cards"] if c["is_rookie"])
    print(f"\n=== Base Set: {len(base['cards'])} cards, {rc_count} RCs ===")
    print(f"=== Event Variations: {len(ev['cards'])} cards ===")

    # RC players
    rc_players = [c["player"] for c in base["cards"] if c["is_rookie"]]
    print(f"  RC players: {rc_players}")

    # Tag Team Dual Autographs
    tta = next(s for s in output["sections"] if s["insert_set"] == "Tag Team Dual Autographs")
    print(f"\n=== Tag Team Dual Autographs: {len(tta['cards'])} appearances from 16 cards ===")
    uso = [(c["player"], c["team"]) for c in tta["cards"] if "Uso" in c["player"]]
    print(f"  Usos (TTA-OGB): {uso}")

    # WWE Together
    wto = next(s for s in output["sections"] if s["insert_set"] == "WWE Together")
    print(f"\n=== WWE Together: {len(wto['cards'])} appearances from 10 cards ===")
    for c in wto["cards"][:4]:
        print(f"  {c['card_number']} {c['player']} ({c['team']})")

    # John Cena appearances (high count due to Cena autos + event variations)
    if "John Cena" in player_map:
        jc = player_map["John Cena"]
        st = jc["stats"]
        cena_ev = sum(1 for a in jc["appearances"] if a["insert_set"] == "Event Variations")
        print(f"\n=== John Cena: {st['insert_sets']} appearances, {cena_ev} in Event Variations ===")

    # Stardust check
    if "Stardust" in player_map:
        sd = player_map["Stardust"]
        print(f"\n=== Stardust: {sd['appearances'][0]['insert_set']} #{sd['appearances'][0]['card_number']} ===")

    # Forever Factions check
    factions = next(s for s in output["sections"] if s["insert_set"] == "Forever Factions")
    print(f"\n=== Forever Factions: {len(factions['cards'])} faction cards ===")
    for c in factions["cards"]:
        print(f"  {c['card_number']} player='{c['player']}' team='{c['team']}'")
