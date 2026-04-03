#!/usr/bin/env python3
"""
Parser for 2025 Topps Chrome Football.
sport: Football, league: NFL, season: 2025
Dual Autographs use co_players logic (same card_number in same insert_set).
"""
import json, os, re

OUTPUT = os.path.join(os.path.dirname(__file__), "chrome_football_2025_parsed.json")

# ── Parallels ──────────────────────────────────────────────────────────────
BASE_PARALLELS = [
    {"name": "Refractor", "print_run": None},
    {"name": "Negative", "print_run": None},
    {"name": "Prism", "print_run": None},
    {"name": "Teal Refractor", "print_run": 199},
    {"name": "Teal Lava", "print_run": 199},
    {"name": "Pink Refractor", "print_run": 175},
    {"name": "Pink Lava Refractor", "print_run": 150},
    {"name": "Aqua Refractor", "print_run": 125},
    {"name": "Aqua Lava Refractor", "print_run": 110},
    {"name": "Blue Refractor", "print_run": 99},
    {"name": "Blue Lava Refractor", "print_run": 80},
    {"name": "Green Refractor", "print_run": 75},
    {"name": "Green Lava Refractor", "print_run": 60},
    {"name": "Purple Refractor", "print_run": 50},
    {"name": "Purple Lava Refractor", "print_run": 45},
    {"name": "Gold Refractor", "print_run": 40},
    {"name": "Gold Lava Refractor", "print_run": 35},
    {"name": "White Refractor", "print_run": 20},
    {"name": "Orange Refractor", "print_run": 15},
    {"name": "Orange Lava Refractor", "print_run": 15},
    {"name": "Black Refractor", "print_run": 5},
    {"name": "Black Lava Refractor", "print_run": 5},
    {"name": "Red Refractor", "print_run": 3},
    {"name": "Red Lava Refractor", "print_run": 3},
    {"name": "Frozenfractor", "print_run": 1},
    {"name": "Superfractor", "print_run": 1},
]

AUTO_PARALLELS = [
    {"name": "Refractor", "print_run": None},
    {"name": "Teal Refractor", "print_run": 199},
    {"name": "Blue Refractor", "print_run": 99},
    {"name": "Green Refractor", "print_run": 75},
    {"name": "Purple Refractor", "print_run": 50},
    {"name": "Gold Refractor", "print_run": 40},
    {"name": "Orange Refractor", "print_run": 15},
    {"name": "Black Refractor", "print_run": 5},
    {"name": "Red Refractor", "print_run": 3},
    {"name": "Superfractor", "print_run": 1},
]

NO_PARALLELS = []

# ── Base Set ──────────────────────────────────────────────────────────────
BASE_RAW = """1 Marvin Harrison Jr., Arizona Cardinals
2 Michael Wilson, Arizona Cardinals
3 Paris Johnson Jr., Arizona Cardinals
4 Trey McBride, Arizona Cardinals
5 Kyler Murray, Arizona Cardinals
6 Garrett Williams, Arizona Cardinals
7 Trey Benson, Arizona Cardinals
8 Budda Baker, Arizona Cardinals
9 Darius Robinson, Arizona Cardinals
10 Josh Sweat, Arizona Cardinals
11 Darnell Mooney, Atlanta Falcons
12 Drake London, Atlanta Falcons
13 Kirk Cousins, Atlanta Falcons
14 Kyle Pitts, Atlanta Falcons
15 Michael Penix Jr., Atlanta Falcons
16 Bijan Robinson, Atlanta Falcons
17 Tyler Allgeier, Atlanta Falcons
18 Leonard Floyd, Atlanta Falcons
19 A.J. Terrell, Atlanta Falcons
20 DeAndre Hopkins, Baltimore Ravens
21 Rashod Bateman, Baltimore Ravens
22 Zay Flowers, Baltimore Ravens
23 Mark Andrews, Baltimore Ravens
24 Lamar Jackson, Baltimore Ravens
25 Derrick Henry, Baltimore Ravens
26 Devontez Walker, Baltimore Ravens
27 Roquan Smith, Baltimore Ravens
28 Nate Wiggins, Baltimore Ravens
29 Kyle Hamilton, Baltimore Ravens
30 Keon Coleman, Buffalo Bills
31 Joshua Palmer, Buffalo Bills
32 Khalil Shakir, Buffalo Bills
33 Dawson Knox, Buffalo Bills
34 Josh Allen, Buffalo Bills
35 James Cook, Buffalo Bills
36 Joey Bosa, Buffalo Bills
37 Dalton Kincaid, Buffalo Bills
38 Xavier Legette, Carolina Panthers
39 Jalen Coker, Carolina Panthers
40 Bryce Young, Carolina Panthers
41 Jaycee Horn, Carolina Panthers
42 Chuba Hubbard, Carolina Panthers
43 Rico Dowdle, Carolina Panthers
44 Tommy Tremble, Carolina Panthers
45 Ja'Tavion Sanders, Carolina Panthers
46 Bobby Brown III, Carolina Panthers
47 Derrick Brown, Carolina Panthers
48 DJ Moore, Chicago Bears
49 Rome Odunze, Chicago Bears
50 Joe Thuney, Chicago Bears
51 Cole Kmet, Chicago Bears
52 Caleb Williams, Chicago Bears
53 D'Andre Swift, Chicago Bears
54 Tyson Bagent, Chicago Bears
55 Roschon Johnson, Chicago Bears
56 Montez Sweat, Chicago Bears
57 Jaylon Johnson, Chicago Bears
58 Ja'Marr Chase, Cincinnati Bengals
59 Tee Higgins, Cincinnati Bengals
60 Andrei Iosivas, Cincinnati Bengals
61 Joe Burrow, Cincinnati Bengals
62 Chase Brown, Cincinnati Bengals
63 Jake Browning, Cincinnati Bengals
64 Evan McPherson, Cincinnati Bengals
65 Trey Hendrickson, Cincinnati Bengals
66 Grant Delpit, Cleveland Browns
67 Cedric Tillman, Cleveland Browns
68 Jerry Jeudy, Cleveland Browns
69 David Njoku, Cleveland Browns
70 Myles Garrett, Cleveland Browns
71 Jerome Ford, Cleveland Browns
72 Quinnen Williams, Dallas Cowboys
73 Kenny Clark, Dallas Cowboys
74 Denzel Ward, Cleveland Browns
75 Jake Ferguson, Dallas Cowboys
76 CeeDee Lamb, Dallas Cowboys
77 Micah Parsons, Green Bay Packers
78 DeMarvion Overshown, Dallas Cowboys
79 Dak Prescott, Dallas Cowboys
80 George Pickens, Dallas Cowboys
81 Brandon Aubrey, Dallas Cowboys
82 DaRon Bland, Dallas Cowboys
83 Trevon Diggs, Dallas Cowboys
84 KaVontae Turpin, Dallas Cowboys
85 Joe Milton III, Dallas Cowboys
86 Courtland Sutton, Denver Broncos
87 Marvin Mims Jr., Denver Broncos
88 Bo Nix, Denver Broncos
89 Jarrett Stidham, Denver Broncos
90 Jaleel McLaughlin, Denver Broncos
91 Troy Franklin, Denver Broncos
92 Evan Engram, Denver Broncos
93 Pat Surtain II, Denver Broncos
94 Talanoa Hufanga, Denver Broncos
95 Zach Allen, Denver Broncos
96 Tim Patrick, Jacksonville Jaguars
97 Jameson Williams, Detroit Lions
98 Amon-Ra St. Brown, Detroit Lions
99 Penei Sewell, Detroit Lions
100 Sam LaPorta, Detroit Lions
101 Jahmyr Gibbs, Detroit Lions
102 Jared Goff, Detroit Lions
103 David Montgomery, Detroit Lions
104 Aidan Hutchinson, Detroit Lions
105 Jake Bates, Detroit Lions
106 Romeo Doubs, Green Bay Packers
107 Jayden Reed, Green Bay Packers
108 Tucker Kraft, Green Bay Packers
109 Jordan Love, Green Bay Packers
110 Josh Jacobs, Green Bay Packers
111 Rashan Gary, Green Bay Packers
112 Christian Watson, Green Bay Packers
113 Xavier McKinney, Green Bay Packers
114 MarShawn Lloyd, Green Bay Packers
115 Nico Collins, Houston Texans
116 Derek Stingley Jr., Houston Texans
117 Christian Kirk, Houston Texans
118 Dalton Schultz, Houston Texans
119 CJ Stroud, Houston Texans
120 Joe Mixon, Houston Texans
121 Will Anderson Jr., Houston Texans
122 Henry To'oTo'o, Houston Texans
123 Tank Dell, Houston Texans
124 Cam Robinson, Cleveland Browns
125 Alec Pierce, Indianapolis Colts
126 Michael Pittman Jr., Indianapolis Colts
127 Josh Downs, Indianapolis Colts
128 Laiatu Latu, Indianapolis Colts
129 Charvarius Ward, Indianapolis Colts
130 Jonathan Taylor, Indianapolis Colts
131 Khalil Herbert, New York Jets
132 Daniel Jones, Indianapolis Colts
133 DeForest Buckner, Indianapolis Colts
134 Braden Smith, Indianapolis Colts
135 Brian Thomas Jr., Jacksonville Jaguars
136 Dyami Brown, Jacksonville Jaguars
137 Brenton Strange, Jacksonville Jaguars
138 Trevor Lawrence, Jacksonville Jaguars
139 Travis Etienne Jr., Jacksonville Jaguars
140 Maason Smith, Jacksonville Jaguars
141 Travon Walker, Jacksonville Jaguars
142 Gabe Davis, Buffalo Bills
143 Tank Bigsby, Philadelphia Eagles
144 Quenton Nelson, Indianapolis Colts
145 Xavier Worthy, Kansas City Chiefs
146 Hollywood Brown, Kansas City Chiefs
147 Rashee Rice, Kansas City Chiefs
148 Patrick Mahomes II, Kansas City Chiefs
149 Isiah Pacheco, Kansas City Chiefs
150 Travis Kelce, Kansas City Chiefs
151 Harrison Butker, Kansas City Chiefs
152 George Karlaftis, Kansas City Chiefs
153 Chris Jones, Kansas City Chiefs
154 Trent McDuffie, Kansas City Chiefs
155 Keenan Allen, Los Angeles Chargers
156 Ladd McConkey, Los Angeles Chargers
157 Joe Alt, Los Angeles Chargers
158 Justin Herbert, Los Angeles Chargers
159 Quentin Johnston, Los Angeles Chargers
160 Khalil Mack, Los Angeles Chargers
161 Najee Harris, Los Angeles Chargers
162 Cameron Dicker, Los Angeles Chargers
163 Tuli Tuipulotu, Los Angeles Chargers
164 Da'Shawn Hand, Los Angeles Chargers
165 Davante Adams, Los Angeles Rams
166 Puka Nacua, Los Angeles Rams
167 Tutu Atwell, Los Angeles Rams
168 Kyren Williams, Los Angeles Rams
169 Matthew Stafford, Los Angeles Rams
170 Steve Avila, Los Angeles Rams
171 Blake Corum, Los Angeles Rams
172 Tyler Higbee, Los Angeles Rams
173 Jared Verse, Los Angeles Rams
174 Kamren Kinchens, Los Angeles Rams
175 Tre Tucker, Las Vegas Raiders
176 Jakobi Meyers, Jacksonville Jaguars
177 Jackson Powers-Johnson, Las Vegas Raiders
178 Brock Bowers, Las Vegas Raiders
179 Geno Smith, Las Vegas Raiders
180 Maxx Crosby, Las Vegas Raiders
181 Robert Spillane, New England Patriots
182 Raheem Mostert, Las Vegas Raiders
183 Kolton Miller, Las Vegas Raiders
184 Jeremy Chinn, Las Vegas Raiders
185 Tyreek Hill, Miami Dolphins
186 Jaylen Waddle, Miami Dolphins
187 Tua Tagovailoa, Miami Dolphins
188 De'Von Achane, Miami Dolphins
189 Zach Wilson, Miami Dolphins
190 Jaylen Wright, Miami Dolphins
191 Jalen Ramsey, Pittsburgh Steelers
192 Jaelan Phillips, Philadelphia Eagles
193 Darren Waller, Miami Dolphins
194 Ashtyn Davis, Miami Dolphins
195 Justin Jefferson, Minnesota Vikings
196 Brian O'Neill, Minnesota Vikings
197 Jonathan Greenard, Minnesota Vikings
198 Andrew Van Ginkel, Minnesota Vikings
199 J.J. McCarthy, Minnesota Vikings
200 T.J. Hockenson, Minnesota Vikings
201 Aaron Jones Sr., Minnesota Vikings
202 Jordan Addison, Minnesota Vikings
203 Will Reichard, Minnesota Vikings
204 Harrison Smith, Minnesota Vikings
205 Stefon Diggs, New England Patriots
206 Mack Hollins, New England Patriots
207 Drake Maye, New England Patriots
208 Terry McLaurin, Washington Commanders
209 Hunter Henry, New England Patriots
210 Rhamondre Stevenson, New England Patriots
211 Kyle Dugger, Pittsburgh Steelers
212 Garrett Bradbury, New England Patriots
213 Jahlani Tavai, New England Patriots
214 Khyiris Tonga, New England Patriots
215 Alvin Kamara, New Orleans Saints
216 Chris Olave, New Orleans Saints
217 Brandin Cooks, Buffalo Bills
218 Rashid Shaheed, Seattle Seahawks
219 Taliese Fuaga, New Orleans Saints
220 Chase Young, New Orleans Saints
221 Cameron Jordan, New Orleans Saints
222 Taysom Hill, New Orleans Saints
223 Erik McCoy, New Orleans Saints
224 Kool-Aid McKinstry, New Orleans Saints
225 Malik Nabers, New York Giants
226 Darius Slayton, New York Giants
227 Wan'Dale Robinson, New York Giants
228 Tyrone Tracy Jr., New York Giants
229 Russell Wilson, New York Giants
230 Dexter Lawrence II, New York Giants
231 Tyler Nubin, New York Giants
232 Micah McFadden, New York Giants
233 Theo Johnson, New York Giants
234 Brian Burns, New York Giants
235 Garrett Wilson, New York Jets
236 Allen Lazard, New York Jets
237 Justin Fields, New York Jets
238 Breece Hall, New York Jets
239 Jeremy Ruckert, New York Jets
240 Braelon Allen, New York Jets
241 Will McDonald IV, New York Jets
242 Sauce Gardner, Indianapolis Colts
243 A.J. Brown, Philadelphia Eagles
244 DeVonta Smith, Philadelphia Eagles
245 Jordan Mailata, Philadelphia Eagles
246 Lane Johnson, Philadelphia Eagles
247 Jalen Hurts, Philadelphia Eagles
248 Saquon Barkley, Philadelphia Eagles
249 Jordan Davis, Philadelphia Eagles
250 Jalen Carter, Philadelphia Eagles
251 Reed Blankenship, Philadelphia Eagles
252 Cooper DeJean, Philadelphia Eagles
253 Jaylen Warren, Pittsburgh Steelers
254 DK Metcalf, Pittsburgh Steelers
255 Aaron Rodgers, Pittsburgh Steelers
256 Troy Fautanu, Pittsburgh Steelers
257 Jonnu Smith, Pittsburgh Steelers
258 T.J. Watt, Pittsburgh Steelers
259 Darius Slay, Pittsburgh Steelers
260 Patrick Queen, Pittsburgh Steelers
261 Ricky Pearsall, San Francisco 49ers
262 Brock Purdy, San Francisco 49ers
263 Christian McCaffrey, San Francisco 49ers
264 Nick Bosa, San Francisco 49ers
265 Trent Williams, San Francisco 49ers
266 Brandon Aiyuk, San Francisco 49ers
267 George Kittle, San Francisco 49ers
268 Fred Warner, San Francisco 49ers
269 Deommodore Lenoir, San Francisco 49ers
270 Kyle Juszczyk, San Francisco 49ers
271 Cooper Kupp, Seattle Seahawks
272 Marquez Valdes-Scantling, Seattle Seahawks
273 Olu Oluwatimi, Seattle Seahawks
274 Noah Fant, Cincinnati Bengals
275 Sam Darnold, Seattle Seahawks
276 Kenneth Walker III, Seattle Seahawks
277 Devon Witherspoon, Seattle Seahawks
278 Riq Woolen, Seattle Seahawks
279 Zach Charbonnet, Seattle Seahawks
280 Jason Myers, Seattle Seahawks
281 Baker Mayfield, Tampa Bay Buccaneers
282 Mike Evans, Tampa Bay Buccaneers
283 Chris Godwin, Tampa Bay Buccaneers
284 Cade Otton, Tampa Bay Buccaneers
285 Bucky Irving, Tampa Bay Buccaneers
286 Vita Vea, Tampa Bay Buccaneers
287 Tristan Wirfs, Tampa Bay Buccaneers
288 Chase McLaughlin, Tampa Bay Buccaneers
289 Jeffery Simmons, Tennessee Titans
290 Tony Pollard, Tennessee Titans
291 Calvin Ridley, Tennessee Titans
292 T'Vondre Sweat, Tennessee Titans
293 Noah Brown, Washington Commanders
294 Deebo Samuel, Washington Commanders
295 Jayden Daniels, Washington Commanders
296 Brian Robinson Jr., San Francisco 49ers
297 Zach Ertz, Washington Commanders
298 Luke McCaffrey, Washington Commanders
299 Bobby Wagner, Washington Commanders
300 Matt Gay, Washington Commanders
301 Shavon Revel Jr., Dallas Cowboys RC
302 Mason Graham, Cleveland Browns RC
303 Shemar Turner, Chicago Bears RC
304 Josh Simmons, Kansas City Chiefs RC
305 Gunnar Helm, Tennessee Titans RC
306 Jaxson Dart, New York Giants RC
307 Kurtis Rourke, San Francisco 49ers RC
308 Dylan Sampson, Cleveland Browns RC
309 Kalel Mullings, Tennessee Titans RC
310 Phil Mafah, Dallas Cowboys RC
311 Brashard Smith, Kansas City Chiefs RC
312 Emeka Egbuka, Tampa Bay Buccaneers RC
313 Pat Bryant, Denver Broncos RC
314 Cam Ward, Tennessee Titans RC
315 Shedeur Sanders, Cleveland Browns RC
316 Quinn Ewers, Miami Dolphins RC
317 Dillon Gabriel, Cleveland Browns RC
318 Riley Leonard, Indianapolis Colts RC
319 Brady Cook, New York Jets RC
320 Isaac TeSlaa, Detroit Lions RC
321 Will Howard, Pittsburgh Steelers RC
322 Ashton Jeanty, Las Vegas Raiders RC
323 Kaleb Johnson, Pittsburgh Steelers RC
324 Omarion Hampton, Los Angeles Chargers RC
325 Quinshon Judkins, Cleveland Browns RC
326 Tetairoa McMillan, Carolina Panthers RC
327 Ollie Gordon II, Miami Dolphins RC
328 TreVeyon Henderson, New England Patriots RC
329 Jordan James, San Francisco 49ers RC
330 RJ Harvey, Denver Broncos RC
331 Cam Skattebo, New York Giants RC
332 Travis Hunter, Jacksonville Jaguars RC
333 Matthew Golden, Green Bay Packers RC
334 Luther Burden III, Chicago Bears RC
335 Terrance Ferguson, Los Angeles Rams RC
336 Elic Ayomanor, Tennessee Titans RC
337 Jalen Royals, Kansas City Chiefs RC
338 Tre Harris III, Los Angeles Chargers RC
339 Harold Fannin Jr., Cleveland Browns RC
340 Savion Williams, Green Bay Packers RC
341 Isaiah Bond, Cleveland Browns RC
342 Tez Johnson, Tampa Bay Buccaneers RC
343 Jayden Higgins, Houston Texans RC
344 Billy Bowman Jr., Atlanta Falcons RC
345 Colston Loveland, Chicago Bears RC
346 Tyler Warren, Indianapolis Colts RC
347 Malaki Starks, Baltimore Ravens RC
348 Nick Emmanwori, Seattle Seahawks RC
349 Will Johnson, Arizona Cardinals RC
350 Abdul Carter, New York Giants RC
351 James Pearce Jr., Atlanta Falcons RC
352 Mykel Williams, San Francisco 49ers RC
353 Nic Scourton, Carolina Panthers RC
354 Jalon Walker, Atlanta Falcons RC
355 Benjamin Morrison, Tampa Bay Buccaneers RC
356 JT Tuimoloau, Indianapolis Colts RC
357 Jack Sawyer, Pittsburgh Steelers RC
358 Landon Jackson, Buffalo Bills RC
359 Jahdae Barron, Denver Broncos RC
360 Deone Walker, Buffalo Bills RC
361 Derrick Harmon, Pittsburgh Steelers RC
362 Kenneth Grant, Miami Dolphins RC
363 Shemar Stewart, Cincinnati Bengals RC
364 Tyleik Williams, Detroit Lions RC
365 Walter Nolen, Arizona Cardinals RC
366 Jihaad Campbell, Philadelphia Eagles RC
367 Darien Porter, Las Vegas Raiders RC
368 Denzel Burke, Arizona Cardinals RC
369 Quincy Riley, New Orleans Saints RC
370 Sebastian Castro, Pittsburgh Steelers RC
371 Trey Amos, Washington Commanders RC
372 Woody Marks, Houston Texans RC
373 Danny Stutsman, New Orleans Saints RC
374 Jaylen Reed, Houston Texans RC
375 Kevin Winston Jr., Tennessee Titans RC
376 Mike Green, Baltimore Ravens RC
377 Princely Umanmielen, Carolina Panthers RC
378 Kelvin Banks Jr., New Orleans Saints RC
379 Will Campbell, New England Patriots RC
380 Jonah Savaiinaea, Miami Dolphins RC
381 Tyler Booker, Dallas Cowboys RC
382 Kyle Monangai, Chicago Bears RC
383 Tate Ratledge, Detroit Lions RC
384 LeQuint Allen Jr., Jacksonville Jaguars RC
385 Dont'e Thornton Jr., Las Vegas Raiders RC
386 Emery Jones Jr., Baltimore Ravens RC
387 Jacory Croskey-Merritt, Washington Commanders RC
388 Jack Bech, Las Vegas Raiders RC
389 Bhayshul Tuten, Jacksonville Jaguars RC
390 DJ Giddens, Indianapolis Colts RC
391 Devin Neal, New Orleans Saints RC
392 Donovan Edwards, New York Jets RC
393 Xavier Watts, Atlanta Falcons RC
394 Kaden Prather, Buffalo Bills RC
395 Tai Felton, Minnesota Vikings RC
396 Elijah Arroyo, Seattle Seahawks RC
397 Jackson Hawes, Buffalo Bills RC
398 Tyler Shough, New Orleans Saints RC
399 Seth Henigan, Jacksonville Jaguars RC
400 Mason Taylor, New York Jets RC"""


# ── Parse base set ────────────────────────────────────────────────────────
def parse_base(raw):
    cards = []
    base_map = {}
    for line in raw.strip().split("\n"):
        m = re.match(r"(\d+)\s+(.+?),\s+(.+?)(?:\s+RC)?$", line.strip())
        if not m:
            continue
        num, player, team = m.group(1), m.group(2), m.group(3)
        is_rc = line.strip().endswith(" RC")
        cards.append({"card_number": num, "player": player, "team": team, "is_rookie": is_rc, "subset": None})
        base_map[num] = (player, team, is_rc)
    return cards, base_map


base_cards, BASE_MAP = parse_base(BASE_RAW)


def card_from_map(n):
    """Build a card dict from BASE_MAP."""
    p, t, rc = BASE_MAP[n]
    return {"card_number": n, "player": p, "team": t, "is_rookie": rc, "subset": None}


# ── Helper for coded insert sets ──────────────────────────────────────────
def parse_coded_line(line):
    """Parse 'CODE Player/Team' or 'CODE Player/Team RC'."""
    line = line.strip()
    if not line:
        return None
    m = re.match(r"(\S+)\s+(.+?)/(.+?)(?:\s+RC)?$", line)
    if not m:
        return None
    code, player, team = m.group(1), m.group(2).strip(), m.group(3).strip()
    is_rc = line.endswith(" RC")
    return {"card_number": code, "player": player, "team": team, "is_rookie": is_rc, "subset": None}


def parse_coded_cards(raw_text):
    """Parse multiple lines of 'CODE Player/Team [RC]'."""
    cards = []
    for line in raw_text.strip().split("\n"):
        c = parse_coded_line(line)
        if c:
            cards.append(c)
    return cards


def parse_dual_cards(raw_lines):
    """Parse dual autograph lines. Each line: 'CODE: Player1/Team1 + Player2/Team2'.
    Returns TWO card entries per line (same card_number → seed.ts co_players)."""
    cards = []
    for line in raw_lines:
        line = line.strip()
        if not line:
            continue
        code, rest = line.split(":", 1)
        code = code.strip()
        parts = rest.split("+")
        for part in parts:
            part = part.strip()
            m = re.match(r"(.+?)/(.+?)(?:\s+RC)?$", part)
            if m:
                player, team = m.group(1).strip(), m.group(2).strip()
                is_rc = part.strip().endswith(" RC")
                cards.append({"card_number": code, "player": player, "team": team, "is_rookie": is_rc, "subset": None})
    return cards


# ── Build all sections ────────────────────────────────────────────────────
def build_sections():
    sections = []

    # 1. Base Set (400 cards)
    sections.append({"insert_set": "Base Set", "parallels": BASE_PARALLELS, "cards": base_cards})

    # 2. Variation sections
    # Camo Variation - exclude 382-387
    camo_exclude = {"382", "383", "384", "385", "386", "387"}
    camo_cards = [c for c in base_cards if c["card_number"] not in camo_exclude]
    sections.append({"insert_set": "Base - Team Camo Variation", "parallels": BASE_PARALLELS, "cards": camo_cards})

    # Lightboard Logo Variation - same 400
    sections.append({"insert_set": "Base - Lightboard Logo Variation", "parallels": BASE_PARALLELS, "cards": list(base_cards)})

    # Chrome Base Etch Variation
    etch_nums = ["1","5","15","16","24","25","34","40","49","52","58","61","69","76","79","88","98","101","109","110","115","119","130","138","148","150","156","158","166","169","178","185","187","195","199","207","215","225","235","237","247","248","254","255","262","263","276","281","291","295"]
    etch_cards = [card_from_map(n) for n in etch_nums if n in BASE_MAP]
    sections.append({"insert_set": "Base - Chrome Base Etch Variation", "parallels": BASE_PARALLELS, "cards": etch_cards})

    # Chrome Rookies Etch Variation - card 313 is Antwane Wells Jr.
    rookies_etch_nums = ["302","306","308","312","314","315","316","317","318","319","320","321","322","323","324","325","326","327","328","329","330","331","332","333","334","336","337","338","340","341","342","343","345","346","347","349","350","351","352","353","355","356","357","379","380","389","390","394","395"]
    rookies_etch_cards = [card_from_map(n) for n in rookies_etch_nums if n in BASE_MAP]
    rookies_etch_cards.append({"card_number": "313", "player": "Antwane Wells Jr.", "team": "New York Giants", "is_rookie": True, "subset": None})
    rookies_etch_cards.sort(key=lambda c: int(c["card_number"]))
    sections.append({"insert_set": "Base - Chrome Rookies Etch Variation", "parallels": BASE_PARALLELS, "cards": rookies_etch_cards})

    # Image Variation
    img_nums = ["4","24","25","34","52","58","61","76","79","88","98","101","109","110","148","150","156","158","166","195","225","247","248","263","295"]
    img_cards = [card_from_map(n) for n in img_nums]
    img_cards.append({"card_number": "401", "player": "Tom Brady", "team": "New England Patriots", "is_rookie": False, "subset": None})
    img_cards.append({"card_number": "402", "player": "Walter Payton", "team": "Chicago Bears", "is_rookie": False, "subset": None})
    img_cards.append({"card_number": "403", "player": "Peyton Manning", "team": "Indianapolis Colts", "is_rookie": False, "subset": None})
    img_cards.append({"card_number": "404", "player": "Barry Sanders", "team": "Detroit Lions", "is_rookie": False, "subset": None})
    img_cards.append({"card_number": "405", "player": "Randy Moss", "team": "Minnesota Vikings", "is_rookie": False, "subset": None})
    sections.append({"insert_set": "Base - Image Variation", "parallels": BASE_PARALLELS, "cards": img_cards})

    # Rookies Image Variation
    rimg_nums = ["306","312","314","315","322","323","324","326","328","330","332","333","334","338","343","345","346","350","388","398"]
    rimg_cards = [card_from_map(n) for n in rimg_nums]
    sections.append({"insert_set": "Base - Rookies Image Variation", "parallels": BASE_PARALLELS, "cards": rimg_cards})

    # ── 3. Insert sets with BASE_PARALLELS ────────────────────────────────

    FUTURE_STARS = """FS-1 Caleb Williams/Chicago Bears
FS-2 Rome Odunze/Chicago Bears
FS-3 Ladd McConkey/Los Angeles Chargers
FS-4 Brian Thomas Jr./Jacksonville Jaguars
FS-5 Xavier Worthy/Kansas City Chiefs
FS-6 Marvin Harrison Jr./Arizona Cardinals
FS-7 Drake Maye/New England Patriots
FS-8 Malik Nabers/New York Giants
FS-9 Bijan Robinson/Atlanta Falcons
FS-10 Jahmyr Gibbs/Detroit Lions
FS-11 Bucky Irving/Tampa Bay Buccaneers
FS-12 De'Von Achane/Miami Dolphins
FS-13 Chase Brown/Cincinnati Bengals
FS-14 Jayden Daniels/Washington Commanders
FS-15 Bo Nix/Denver Broncos
FS-16 CJ Stroud/Houston Texans
FS-17 Bryce Young/Carolina Panthers
FS-18 J.J. McCarthy/Minnesota Vikings
FS-19 Michael Penix Jr./Atlanta Falcons
FS-20 Cooper DeJean/Philadelphia Eagles
FS-21 Brock Bowers/Las Vegas Raiders
FS-22 Pat Surtain II/Denver Broncos
FS-23 Puka Nacua/Los Angeles Rams
FS-24 Jared Verse/Los Angeles Rams
FS-25 Jalen Carter/Philadelphia Eagles"""

    TOPPS_1975 = """1975-1 Marvin Harrison Jr./Arizona Cardinals
1975-2 Michael Penix Jr./Atlanta Falcons
1975-3 Lamar Jackson/Baltimore Ravens
1975-4 Josh Allen/Buffalo Bills
1975-5 Chuba Hubbard/Carolina Panthers
1975-6 Rome Odunze/Chicago Bears
1975-7 Joe Burrow/Cincinnati Bengals
1975-8 Myles Garrett/Cleveland Browns
1975-9 CeeDee Lamb/Dallas Cowboys
1975-10 Dak Prescott/Dallas Cowboys
1975-11 Bo Nix/Denver Broncos
1975-12 Jahmyr Gibbs/Detroit Lions
1975-13 Matthew Golden/Green Bay Packers RC
1975-14 Joe Mixon/Houston Texans
1975-15 Tyler Warren/Indianapolis Colts RC
1975-16 Brian Thomas Jr./Jacksonville Jaguars
1975-17 Travis Kelce/Kansas City Chiefs
1975-18 Justin Herbert/Los Angeles Chargers
1975-19 Puka Nacua/Los Angeles Rams
1975-20 Ashton Jeanty/Las Vegas Raiders RC
1975-21 Tua Tagovailoa/Miami Dolphins
1975-22 J.J. McCarthy/Minnesota Vikings
1975-23 Drake Maye/New England Patriots
1975-24 Alvin Kamara/New Orleans Saints
1975-25 Jaxson Dart/New York Giants RC
1975-26 Justin Fields/New York Jets
1975-27 Cooper DeJean/Philadelphia Eagles
1975-28 Aaron Rodgers/Pittsburgh Steelers
1975-29 Christian McCaffrey/San Francisco 49ers
1975-30 Kenneth Walker III/Seattle Seahawks
1975-31 Baker Mayfield/Tampa Bay Buccaneers
1975-32 Bucky Irving/Tampa Bay Buccaneers
1975-33 Cam Ward/Tennessee Titans RC
1975-34 Jayden Daniels/Washington Commanders
1975-35 Terry McLaurin/Washington Commanders"""

    POWER_PLAYERS = """PP-1 Lamar Jackson/Baltimore Ravens
PP-2 Josh Allen/Buffalo Bills
PP-3 Jayden Daniels/Washington Commanders
PP-4 Jalen Hurts/Philadelphia Eagles
PP-5 Joe Burrow/Cincinnati Bengals
PP-6 Patrick Mahomes II/Kansas City Chiefs
PP-7 Caleb Williams/Chicago Bears
PP-8 Cam Ward/Tennessee Titans RC
PP-9 Bo Nix/Denver Broncos
PP-10 Drake Maye/New England Patriots
PP-11 Bijan Robinson/Atlanta Falcons
PP-12 Jahmyr Gibbs/Detroit Lions
PP-13 Saquon Barkley/Philadelphia Eagles
PP-14 Ashton Jeanty/Las Vegas Raiders RC
PP-15 Christian McCaffrey/San Francisco 49ers
PP-16 Derrick Henry/Baltimore Ravens
PP-17 Omarion Hampton/Los Angeles Chargers RC
PP-18 Bucky Irving/Tampa Bay Buccaneers
PP-19 Chase Brown/Cincinnati Bengals
PP-20 Josh Jacobs/Green Bay Packers
PP-21 Ja'Marr Chase/Cincinnati Bengals
PP-22 Justin Jefferson/Minnesota Vikings
PP-23 CeeDee Lamb/Dallas Cowboys
PP-24 Puka Nacua/Los Angeles Rams
PP-25 Malik Nabers/New York Giants
PP-26 Amon-Ra St. Brown/Detroit Lions
PP-27 Ladd McConkey/Los Angeles Chargers
PP-28 Tetairoa McMillan/Carolina Panthers RC
PP-29 Travis Hunter/Jacksonville Jaguars RC
PP-30 Nico Collins/Houston Texans
PP-31 Brock Bowers/Las Vegas Raiders
PP-32 Trey McBride/Arizona Cardinals
PP-33 George Kittle/San Francisco 49ers
PP-34 Travis Kelce/Kansas City Chiefs
PP-35 Tyler Warren/Indianapolis Colts RC
PP-36 T.J. Hockenson/Minnesota Vikings
PP-37 Maxx Crosby/Las Vegas Raiders
PP-38 Aidan Hutchinson/Detroit Lions
PP-39 T.J. Watt/Pittsburgh Steelers
PP-40 Abdul Carter/New York Giants RC"""

    LEGENDS_GRIDIRON = """LOG-1 Kurt Warner/St. Louis Rams
LOG-2 Michael Vick/Atlanta Falcons
LOG-3 Doug Flutie/Buffalo Bills
LOG-4 Jim Kelly/Buffalo Bills
LOG-5 Jim McMahon/Chicago Bears
LOG-6 Boomer Esiason/Cincinnati Bengals
LOG-7 Troy Aikman/Dallas Cowboys
LOG-8 Joe Montana/San Francisco 49ers
LOG-9 Tom Brady/New England Patriots
LOG-10 Peyton Manning/Indianapolis Colts
LOG-11 Barry Sanders/Detroit Lions
LOG-12 Earl Campbell/Houston Oilers
LOG-13 Eric Dickerson/Los Angeles Rams
LOG-14 Ricky Williams/Miami Dolphins
LOG-15 Adrian Peterson/Minnesota Vikings
LOG-16 Emmitt Smith/Dallas Cowboys
LOG-17 Bo Jackson/Los Angeles Raiders
LOG-18 Frank Gore/San Francisco 49ers
LOG-19 Art Monk/Washington Redskins
LOG-20 Terrell Owens/Philadelphia Eagles
LOG-21 Jerry Rice/San Francisco 49ers
LOG-22 Tim Brown/Oakland Raiders
LOG-23 Keyshawn Johnson/New York Jets
LOG-24 Julian Edelman/New England Patriots
LOG-25 Randy Moss/Minnesota Vikings
LOG-26 Isaac Bruce/St. Louis Rams
LOG-27 Sterling Sharpe/Green Bay Packers
LOG-28 Chad Johnson/Cincinnati Bengals
LOG-29 Rob Gronkowski/New England Patriots
LOG-30 Delanie Walker/Tennessee Titans
LOG-31 Jason Witten/Dallas Cowboys
LOG-32 Antonio Gates/San Diego Chargers
LOG-33 Troy Polamalu/Pittsburgh Steelers
LOG-34 Kam Chancellor/Seattle Seahawks
LOG-35 DeAngelo Hall/Washington Redskins
LOG-36 Richard Sherman/Seattle Seahawks
LOG-37 Devin Hester/Chicago Bears
LOG-38 Brian Dawkins/Philadelphia Eagles
LOG-39 Ray Lewis/Baltimore Ravens
LOG-40 Aaron Donald/Los Angeles Rams"""

    FORTUNE_15 = """F15-1 Lamar Jackson/Baltimore Ravens
F15-2 Ja'Marr Chase/Cincinnati Bengals
F15-3 Saquon Barkley/Philadelphia Eagles
F15-4 Justin Jefferson/Minnesota Vikings
F15-5 Joe Burrow/Cincinnati Bengals
F15-6 Patrick Mahomes II/Kansas City Chiefs
F15-7 Josh Allen/Buffalo Bills
F15-8 Brock Bowers/Las Vegas Raiders
F15-9 CeeDee Lamb/Dallas Cowboys
F15-10 Derrick Henry/Baltimore Ravens
F15-11 Micah Parsons/Green Bay Packers
F15-12 Jahmyr Gibbs/Detroit Lions
F15-13 Amon-Ra St. Brown/Detroit Lions
F15-14 Bijan Robinson/Atlanta Falcons
F15-15 Malik Nabers/New York Giants
F15-16 Caleb Williams/Chicago Bears
F15-17 Jordan Love/Green Bay Packers
F15-18 J.J. McCarthy/Minnesota Vikings
F15-19 Tetairoa McMillan/Carolina Panthers RC
F15-20 Travis Hunter/Jacksonville Jaguars RC
F15-21 Emeka Egbuka/Tampa Bay Buccaneers RC
F15-22 Cam Ward/Tennessee Titans RC
F15-23 Jaxson Dart/New York Giants RC
F15-24 Ashton Jeanty/Las Vegas Raiders RC
F15-25 Omarion Hampton/Los Angeles Chargers RC
F15-26 TreVeyon Henderson/New England Patriots RC
F15-27 Cam Skattebo/New York Giants RC
F15-28 Luther Burden III/Chicago Bears RC
F15-29 Jacory Croskey-Merritt/Washington Commanders RC
F15-30 Tyler Warren/Indianapolis Colts RC
F15-31 Ray Lewis/Baltimore Ravens
F15-32 Lawrence Taylor/New York Giants
F15-33 Peyton Manning/Denver Broncos
F15-34 Walter Payton/Chicago Bears
F15-35 Tom Brady/Tampa Bay Buccaneers"""

    ALL_CHROME_TEAM = """ACT-1 Lamar Jackson/Baltimore Ravens
ACT-2 Josh Allen/Buffalo Bills
ACT-3 Saquon Barkley/Philadelphia Eagles
ACT-4 Derrick Henry/Baltimore Ravens
ACT-5 Ja'Marr Chase/Cincinnati Bengals
ACT-6 Justin Jefferson/Minnesota Vikings
ACT-7 Amon-Ra St. Brown/Detroit Lions
ACT-8 CeeDee Lamb/Dallas Cowboys
ACT-9 Terry McLaurin/Washington Commanders
ACT-10 Brock Bowers/Las Vegas Raiders
ACT-11 George Kittle/San Francisco 49ers
ACT-12 Jordan Mailata/Philadelphia Eagles
ACT-13 Penei Sewell/Detroit Lions
ACT-14 Joe Thuney/Chicago Bears
ACT-15 Myles Garrett/Cleveland Browns
ACT-16 Trey Hendrickson/Cincinnati Bengals
ACT-17 Chris Jones/Kansas City Chiefs
ACT-18 Pat Surtain II/Denver Broncos
ACT-19 Derek Stingley Jr./Houston Texans
ACT-20 Fred Warner/San Francisco 49ers
ACT-21 Roquan Smith/Baltimore Ravens
ACT-22 Zack Baun/Philadelphia Eagles
ACT-23 Kerby Joseph/Detroit Lions
ACT-24 Xavier McKinney/Green Bay Packers
ACT-25 Chris Boswell/Pittsburgh Steelers"""

    CHROME_RAD_ROOKIES = """RR-1 Cam Ward/Tennessee Titans RC
RR-2 Tetairoa McMillan/Carolina Panthers RC
RR-3 Ashton Jeanty/Las Vegas Raiders RC
RR-4 Travis Hunter/Jacksonville Jaguars RC
RR-5 Jaxson Dart/New York Giants RC
RR-6 Colston Loveland/Chicago Bears RC
RR-7 Omarion Hampton/Los Angeles Chargers RC
RR-8 Tyler Warren/Indianapolis Colts RC
RR-9 TreVeyon Henderson/New England Patriots RC
RR-10 Matthew Golden/Green Bay Packers RC
RR-11 Abdul Carter/New York Giants RC
RR-12 Emeka Egbuka/Tampa Bay Buccaneers RC
RR-13 Shedeur Sanders/Cleveland Browns RC
RR-14 Kaleb Johnson/Pittsburgh Steelers RC
RR-15 RJ Harvey/Denver Broncos RC
RR-16 Luther Burden III/Chicago Bears RC
RR-17 Cam Skattebo/New York Giants RC
RR-18 Quinshon Judkins/Cleveland Browns RC
RR-19 Jayden Higgins/Houston Texans RC
RR-20 Jack Bech/Las Vegas Raiders RC"""

    URBAN_LEGENDS = """UL-1 Joe Burrow/Cincinnati Bengals
UL-2 Josh Allen/Buffalo Bills
UL-3 Lamar Jackson/Baltimore Ravens
UL-4 Caleb Williams/Chicago Bears
UL-5 Jordan Love/Green Bay Packers
UL-6 Drake London/Atlanta Falcons
UL-7 Ladd McConkey/Los Angeles Chargers
UL-8 Puka Nacua/Los Angeles Rams
UL-9 Nico Collins/Houston Texans
UL-10 Justin Herbert/Los Angeles Chargers
UL-11 Patrick Mahomes II/Kansas City Chiefs
UL-12 Jalen Hurts/Philadelphia Eagles
UL-13 Josh Jacobs/Green Bay Packers
UL-14 Bijan Robinson/Atlanta Falcons
UL-15 Christian McCaffrey/San Francisco 49ers
UL-16 Ja'Marr Chase/Cincinnati Bengals
UL-17 Emeka Egbuka/Tampa Bay Buccaneers RC
UL-18 Cam Ward/Tennessee Titans RC
UL-19 Jaxson Dart/New York Giants RC
UL-20 Ashton Jeanty/Las Vegas Raiders RC
UL-21 Bo Nix/Denver Broncos
UL-22 Rome Odunze/Chicago Bears
UL-23 Omarion Hampton/Los Angeles Chargers RC
UL-24 Travis Hunter/Jacksonville Jaguars RC
UL-25 Cam Skattebo/New York Giants RC
UL-26 Colston Loveland/Chicago Bears RC
UL-27 Tyler Warren/Indianapolis Colts RC
UL-28 Matthew Golden/Green Bay Packers RC
UL-29 Terrell Owens/Dallas Cowboys
UL-30 Walter Payton/Chicago Bears"""

    HELIX = """HX-1 Tom Brady/Tampa Bay Buccaneers
HX-2 Patrick Mahomes II/Kansas City Chiefs
HX-3 Josh Allen/Buffalo Bills
HX-4 Cam Ward/Tennessee Titans RC
HX-5 Caleb Williams/Chicago Bears
HX-6 Bo Nix/Denver Broncos
HX-7 CeeDee Lamb/Dallas Cowboys
HX-8 Ja'Marr Chase/Cincinnati Bengals
HX-9 Justin Jefferson/Minnesota Vikings
HX-10 Puka Nacua/Los Angeles Rams
HX-11 Bijan Robinson/Atlanta Falcons
HX-12 Brock Purdy/San Francisco 49ers
HX-13 Saquon Barkley/Philadelphia Eagles
HX-14 Omarion Hampton/Los Angeles Chargers RC
HX-15 Luther Burden III/Chicago Bears RC
HX-16 Justin Herbert/Los Angeles Chargers
HX-17 Jayden Daniels/Washington Commanders
HX-18 Joe Burrow/Cincinnati Bengals
HX-19 Jalen Hurts/Philadelphia Eagles
HX-20 Lamar Jackson/Baltimore Ravens
HX-21 Aaron Rodgers/Pittsburgh Steelers
HX-22 J.J. McCarthy/Minnesota Vikings
HX-23 Matthew Golden/Green Bay Packers RC
HX-24 Travis Hunter/Jacksonville Jaguars RC
HX-25 Jaxson Dart/New York Giants RC
HX-26 Ashton Jeanty/Las Vegas Raiders RC
HX-27 Jayden Higgins/Houston Texans RC
HX-28 Abdul Carter/New York Giants RC
HX-29 Derrick Henry/Baltimore Ravens
HX-30 Tetairoa McMillan/Carolina Panthers RC"""

    SHADOW_ETCH = """SE-1 Patrick Mahomes II/Kansas City Chiefs
SE-2 Josh Allen/Buffalo Bills
SE-3 Lamar Jackson/Baltimore Ravens
SE-4 Joe Burrow/Cincinnati Bengals
SE-5 Jalen Hurts/Philadelphia Eagles
SE-6 CJ Stroud/Houston Texans
SE-7 Caleb Williams/Chicago Bears
SE-8 Jayden Daniels/Washington Commanders
SE-9 Cam Ward/Tennessee Titans RC
SE-10 Jordan Love/Green Bay Packers
SE-11 Christian McCaffrey/San Francisco 49ers
SE-12 Bijan Robinson/Atlanta Falcons
SE-13 Jahmyr Gibbs/Detroit Lions
SE-14 Saquon Barkley/Philadelphia Eagles
SE-15 Derrick Henry/Baltimore Ravens
SE-16 Breece Hall/New York Jets
SE-17 Jonathan Taylor/Indianapolis Colts
SE-18 Ashton Jeanty/Las Vegas Raiders RC
SE-19 TreVeyon Henderson/New England Patriots RC
SE-20 Omarion Hampton/Los Angeles Chargers RC
SE-21 Justin Jefferson/Minnesota Vikings
SE-22 Ja'Marr Chase/Cincinnati Bengals
SE-23 CeeDee Lamb/Dallas Cowboys
SE-24 Amon-Ra St. Brown/Detroit Lions
SE-25 Puka Nacua/Los Angeles Rams
SE-26 Malik Nabers/New York Giants
SE-27 Emeka Egbuka/Tampa Bay Buccaneers RC
SE-28 Travis Kelce/Kansas City Chiefs
SE-29 Trey McBride/Arizona Cardinals
SE-30 George Kittle/San Francisco 49ers"""

    GAME_GENIES = """GG-1 Josh Allen/Buffalo Bills
GG-2 Tom Brady/New England Patriots
GG-3 Patrick Mahomes II/Kansas City Chiefs
GG-4 Lamar Jackson/Baltimore Ravens
GG-5 Joe Burrow/Cincinnati Bengals
GG-6 Justin Jefferson/Minnesota Vikings
GG-7 Ja'Marr Chase/Cincinnati Bengals
GG-8 Saquon Barkley/Philadelphia Eagles
GG-9 CeeDee Lamb/Dallas Cowboys
GG-10 Jayden Daniels/Washington Commanders
GG-11 Derrick Henry/Baltimore Ravens
GG-12 Jahmyr Gibbs/Detroit Lions
GG-13 Bo Nix/Denver Broncos
GG-14 Cam Ward/Tennessee Titans RC
GG-15 Ashton Jeanty/Las Vegas Raiders RC
GG-16 Emeka Egbuka/Tampa Bay Buccaneers RC
GG-17 Jaxson Dart/New York Giants RC
GG-18 Bijan Robinson/Atlanta Falcons
GG-19 Omarion Hampton/Los Angeles Chargers RC
GG-20 Travis Hunter/Jacksonville Jaguars RC
GG-21 Jalen Hurts/Philadelphia Eagles
GG-22 Josh Jacobs/Green Bay Packers
GG-23 Caleb Williams/Chicago Bears
GG-24 Jonathan Taylor/Indianapolis Colts
GG-25 Tetairoa McMillan/Carolina Panthers RC"""

    KAIJU = """KAI-1 Tom Brady/New England Patriots
KAI-2 Patrick Mahomes II/Kansas City Chiefs
KAI-3 Jalen Hurts/Philadelphia Eagles
KAI-4 Joe Burrow/Cincinnati Bengals
KAI-5 Caleb Williams/Chicago Bears
KAI-6 Jayden Daniels/Washington Commanders
KAI-7 Josh Allen/Buffalo Bills
KAI-8 Cam Ward/Tennessee Titans RC
KAI-9 Travis Hunter/Jacksonville Jaguars RC
KAI-10 Jaxson Dart/New York Giants RC"""

    LETS_GO = """LG-1 Cam Ward/Tennessee Titans RC
LG-2 Lamar Jackson/Baltimore Ravens
LG-3 Josh Allen/Buffalo Bills
LG-4 Joe Burrow/Cincinnati Bengals
LG-5 Patrick Mahomes II/Kansas City Chiefs"""

    ULTRA_VIOLET = """UV-1 Jaxson Dart/New York Giants RC
UV-2 Cam Ward/Tennessee Titans RC
UV-3 Ashton Jeanty/Las Vegas Raiders RC
UV-4 Abdul Carter/New York Giants RC
UV-5 Tetairoa McMillan/Carolina Panthers RC
UV-6 Tom Brady/New England Patriots
UV-7 Omarion Hampton/Los Angeles Chargers RC
UV-8 Peyton Manning/Indianapolis Colts
UV-9 Bo Nix/Denver Broncos
UV-10 Drake Maye/New England Patriots
UV-11 Lamar Jackson/Baltimore Ravens
UV-12 Brock Purdy/San Francisco 49ers
UV-13 Justin Jefferson/Minnesota Vikings
UV-14 J.J. McCarthy/Minnesota Vikings
UV-15 Patrick Mahomes II/Kansas City Chiefs
UV-16 Ja'Marr Chase/Cincinnati Bengals
UV-17 Joe Burrow/Cincinnati Bengals
UV-18 Bijan Robinson/Atlanta Falcons
UV-19 Jayden Daniels/Washington Commanders
UV-20 Saquon Barkley/Philadelphia Eagles"""

    LIGHTNING_LEADERS = """LL-1 Joe Burrow/Cincinnati Bengals
LL-2 Jared Goff/Detroit Lions
LL-3 Baker Mayfield/Tampa Bay Buccaneers
LL-4 Geno Smith/Las Vegas Raiders
LL-5 Lamar Jackson/Baltimore Ravens
LL-6 Bijan Robinson/Atlanta Falcons
LL-7 Jonathan Taylor/Indianapolis Colts
LL-8 Jahmyr Gibbs/Detroit Lions
LL-9 Saquon Barkley/Philadelphia Eagles
LL-10 Derrick Henry/Baltimore Ravens
LL-11 Ja'Marr Chase/Cincinnati Bengals
LL-12 Justin Jefferson/Minnesota Vikings
LL-13 Brian Thomas Jr./Jacksonville Jaguars
LL-14 Drake London/Atlanta Falcons
LL-15 Amon-Ra St. Brown/Detroit Lions
LL-16 Brock Bowers/Las Vegas Raiders
LL-17 Ladd McConkey/Los Angeles Chargers
LL-18 Myles Garrett/Cleveland Browns
LL-19 Trey Hendrickson/Cincinnati Bengals
LL-20 Josh Jacobs/Green Bay Packers"""

    FANATICAL = """FF-1 Ashton Jeanty/Las Vegas Raiders RC
FF-2 Omarion Hampton/Los Angeles Chargers RC
FF-3 Tetairoa McMillan/Carolina Panthers RC
FF-4 Cam Ward/Tennessee Titans RC
FF-5 Jaxson Dart/New York Giants RC
FF-6 Emeka Egbuka/Tampa Bay Buccaneers RC
FF-7 Luther Burden III/Chicago Bears RC
FF-8 Tyler Warren/Indianapolis Colts RC
FF-9 Quinshon Judkins/Cleveland Browns RC
FF-10 Travis Hunter/Jacksonville Jaguars RC
FF-11 Bijan Robinson/Atlanta Falcons
FF-12 Ja'Marr Chase/Cincinnati Bengals
FF-13 Joe Burrow/Cincinnati Bengals
FF-14 Patrick Mahomes II/Kansas City Chiefs
FF-15 Puka Nacua/Los Angeles Rams
FF-16 Justin Herbert/Los Angeles Chargers
FF-17 Lamar Jackson/Baltimore Ravens
FF-18 Bo Nix/Denver Broncos
FF-19 Justin Jefferson/Minnesota Vikings
FF-20 Tom Brady/Tampa Bay Buccaneers
FF-21 Myles Garrett/Cleveland Browns
FF-22 Maxx Crosby/Las Vegas Raiders
FF-23 Micah Parsons/Green Bay Packers
FF-24 Aidan Hutchinson/Detroit Lions
FF-25 Malik Nabers/New York Giants
FF-26 Aaron Rodgers/Pittsburgh Steelers
FF-27 Baker Mayfield/Tampa Bay Buccaneers
FF-28 CJ Stroud/Houston Texans
FF-29 Travis Kelce/Kansas City Chiefs
FF-30 Christian McCaffrey/San Francisco 49ers"""

    insert_sets_base = [
        ("Future Stars", FUTURE_STARS),
        ("1975 Topps", TOPPS_1975),
        ("Power Players", POWER_PLAYERS),
        ("Legends of the Gridiron", LEGENDS_GRIDIRON),
        ("Fortune 15", FORTUNE_15),
        ("All Chrome Team", ALL_CHROME_TEAM),
        ("Chrome Radiating Rookies", CHROME_RAD_ROOKIES),
        ("Urban Legends", URBAN_LEGENDS),
        ("Helix", HELIX),
        ("Shadow Etch", SHADOW_ETCH),
        ("Game Genies", GAME_GENIES),
        ("Kaiju", KAIJU),
        ("Let's Go", LETS_GO),
        ("Ultra Violet", ULTRA_VIOLET),
        ("Lightning Leaders", LIGHTNING_LEADERS),
        ("Fanatical", FANATICAL),
    ]

    for name, raw in insert_sets_base:
        cards = parse_coded_cards(raw)
        sections.append({"insert_set": name, "parallels": BASE_PARALLELS, "cards": cards})

    # ── 4. Autograph sections with AUTO_PARALLELS ─────────────────────────

    BASE_CARDS_AUTO = """BA-AB A.J. Brown/Philadelphia Eagles
BA-AK Alvin Kamara/New Orleans Saints
BA-AR Aaron Rodgers/Pittsburgh Steelers
BA-AS Amon-Ra St. Brown/Detroit Lions
BA-BB Brock Bowers/Las Vegas Raiders
BA-BH Breece Hall/New York Jets
BA-BI Bucky Irving/Tampa Bay Buccaneers
BA-BN Bo Nix/Denver Broncos
BA-BP Brock Purdy/San Francisco 49ers
BA-BT Brian Thomas Jr./Jacksonville Jaguars
BA-BY Bryce Young/Carolina Panthers
BA-CB Chase Brown/Cincinnati Bengals
BA-CH Chuba Hubbard/Carolina Panthers
BA-CHE Cameron Heyward/Pittsburgh Steelers
BA-CL CeeDee Lamb/Dallas Cowboys
BA-CO Chris Olave/New Orleans Saints
BA-CS CJ Stroud/Houston Texans
BA-CSU Courtland Sutton/Denver Broncos
BA-CT Cedric Tillman/Cleveland Browns
BA-CW Caleb Williams/Chicago Bears
BA-DA De'Von Achane/Miami Dolphins
BA-DAA Davante Adams/Los Angeles Rams
BA-DH Derrick Henry/Baltimore Ravens
BA-DL Drake London/Atlanta Falcons
BA-DMA Drake Maye/New England Patriots
BA-DP Dak Prescott/Dallas Cowboys
BA-DSJ Derek Stingley Jr./Houston Texans
BA-DSW D'Andre Swift/Chicago Bears
BA-GK George Kittle/San Francisco 49ers
BA-GP George Pickens/Dallas Cowboys
BA-GS Geno Smith/Las Vegas Raiders
BA-GW Garrett Wilson/New York Jets
BA-JA Jordan Addison/Minnesota Vikings
BA-JAC James Cook/Buffalo Bills
BA-JAL Josh Allen/Buffalo Bills
BA-JAWI Javonte Williams/Dallas Cowboys
BA-JB Joe Burrow/Cincinnati Bengals
BA-JD Jayden Daniels/Washington Commanders
BA-JG Jahmyr Gibbs/Detroit Lions
BA-JGO Jared Goff/Detroit Lions
BA-JH Jalen Hurts/Philadelphia Eagles
BA-JJ Justin Jefferson/Minnesota Vikings
BA-JJA Josh Jacobs/Green Bay Packers
BA-JJE Jerry Jeudy/Cleveland Browns
BA-JKD J.K. Dobbins/Denver Broncos
BA-JSN Jaxon Smith-Njigba/Seattle Seahawks
BA-JT Jonathan Taylor/Indianapolis Colts
BA-JW Jaylen Waddle/Miami Dolphins
BA-KC Keon Coleman/Buffalo Bills
BA-KW Kenneth Walker III/Seattle Seahawks
BA-LM Ladd McConkey/Los Angeles Chargers
BA-MC Maxx Crosby/Las Vegas Raiders
BA-ME Mike Evans/Tampa Bay Buccaneers
BA-MG Myles Garrett/Cleveland Browns
BA-MH Marvin Harrison Jr./Arizona Cardinals
BA-MN Malik Nabers/New York Giants
BA-MP Michael Penix Jr./Atlanta Falcons
BA-MS Matthew Stafford/Los Angeles Rams
BA-MSW Montez Sweat/Chicago Bears
BA-NC Nico Collins/Houston Texans
BA-PN Puka Nacua/Los Angeles Rams
BA-RO Rome Odunze/Chicago Bears
BA-SB Saquon Barkley/Philadelphia Eagles
BA-SD Sam Darnold/Seattle Seahawks
BA-SG Sauce Gardner/Indianapolis Colts
BA-TE Travis Etienne Jr./Jacksonville Jaguars
BA-TRB Trey Benson/Arizona Cardinals
BA-TT Tyrone Tracy Jr./New York Giants
BA-TTA Tua Tagovailoa/Miami Dolphins
BA-XW Xavier Worthy/Kansas City Chiefs"""

    ROOKIES_AUTO = """RA-AC Abdul Carter/New York Giants RC
RA-AJ Ashton Jeanty/Las Vegas Raiders RC
RA-AW Antwane Wells Jr./New York Giants RC
RA-BCO Brady Cook/New York Jets RC
RA-BM Benjamin Morrison/Tampa Bay Buccaneers RC
RA-BS Brashard Smith/Kansas City Chiefs RC
RA-BT Bhayshul Tuten/Jacksonville Jaguars RC
RA-CL Colston Loveland/Chicago Bears RC
RA-CS Cam Skattebo/New York Giants RC
RA-CWA Cam Ward/Tennessee Titans RC
RA-DB Denzel Burke/Arizona Cardinals RC
RA-DE Donovan Edwards/New York Jets RC
RA-DG DJ Giddens/Indianapolis Colts RC
RA-DGA Dillon Gabriel/Cleveland Browns RC
RA-DH Derrick Harmon/Pittsburgh Steelers RC
RA-DN Devin Neal/New Orleans Saints RC
RA-DP Darien Porter/Las Vegas Raiders RC
RA-DS Danny Stutsman/New Orleans Saints RC
RA-DSA Dylan Sampson/Cleveland Browns RC
RA-DTH Dont'e Thornton Jr./Las Vegas Raiders RC
RA-DW Deone Walker/Buffalo Bills RC
RA-EA Elijah Arroyo/Seattle Seahawks RC
RA-EAY Elic Ayomanor/Tennessee Titans RC
RA-EE Emeka Egbuka/Tampa Bay Buccaneers RC
RA-EJ Emery Jones Jr./Baltimore Ravens RC
RA-GH Gunnar Helm/Tennessee Titans RC
RA-HF Harold Fannin Jr./Cleveland Browns RC
RA-IBO Isaiah Bond/Cleveland Browns RC
RA-ITS Isaac TeSlaa/Detroit Lions RC
RA-JB Jahdae Barron/Denver Broncos RC
RA-JBE Jack Bech/Las Vegas Raiders RC
RA-JC Jihaad Campbell/Philadelphia Eagles RC
RA-JCM Jacory Croskey-Merritt/Washington Commanders RC
RA-JD Jaxson Dart/New York Giants RC
RA-JH Jackson Hawes/Buffalo Bills RC
RA-JHI Jayden Higgins/Houston Texans RC
RA-JJ Jordan James/San Francisco 49ers RC
RA-JR Jaylen Reed/Houston Texans RC
RA-JRO Jalen Royals/Kansas City Chiefs RC
RA-JS Jonah Savaiinaea/Miami Dolphins RC
RA-JSA Jack Sawyer/Pittsburgh Steelers RC
RA-JT JT Tuimoloau/Indianapolis Colts RC
RA-JW Jalon Walker/Atlanta Falcons RC
RA-KB Kelvin Banks Jr./New Orleans Saints RC
RA-KJ Kaleb Johnson/Pittsburgh Steelers RC
RA-KMU Kalel Mullings/Tennessee Titans RC
RA-KP Kaden Prather/Buffalo Bills RC
RA-KW Kevin Winston Jr./Tennessee Titans RC
RA-KYM Kyle Monangai/Chicago Bears RC
RA-LB Luther Burden III/Chicago Bears RC
RA-LEA LeQuint Allen/Jacksonville Jaguars RC
RA-LJ Landon Jackson/Buffalo Bills RC
RA-MG Mike Green/Baltimore Ravens RC
RA-MGO Matthew Golden/Green Bay Packers RC
RA-MGR Mason Graham/Cleveland Browns RC
RA-MS Malaki Starks/Baltimore Ravens RC
RA-MT Mason Taylor/New York Jets RC
RA-MW Mykel Williams/San Francisco 49ers RC
RA-NE Nick Emmanwori/Seattle Seahawks RC
RA-NS Nic Scourton/Carolina Panthers RC
RA-OG Ollie Gordon II/Miami Dolphins RC
RA-OH Omarion Hampton/Los Angeles Chargers RC
RA-PM Phil Mafah/Dallas Cowboys RC
RA-PU Princely Umanmielen/Carolina Panthers RC
RA-QJ Quinshon Judkins/Cleveland Browns RC
RA-QR Quincy Riley/New Orleans Saints RC
RA-RH RJ Harvey/Denver Broncos RC
RA-RL Riley Leonard/Indianapolis Colts RC
RA-SC Sebastian Castro/Pittsburgh Steelers RC
RA-SH Seth Henigan/Jacksonville Jaguars RC
RA-SR Shavon Revel Jr./Dallas Cowboys RC
RA-SS Shemar Stewart/Cincinnati Bengals RC
RA-SSA Shedeur Sanders/Cleveland Browns RC
RA-SW Savion Williams/Green Bay Packers RC
RA-TA Trey Amos/Washington Commanders RC
RA-TB Tyler Booker/Dallas Cowboys RC
RA-TF Tai Felton/Minnesota Vikings RC
RA-TFE Terrance Ferguson/Los Angeles Rams RC
RA-TH Tre Harris III/Los Angeles Chargers RC
RA-THE TreVeyon Henderson/New England Patriots RC
RA-THU Travis Hunter/Jacksonville Jaguars RC
RA-TJ Tez Johnson/Tampa Bay Buccaneers RC
RA-TM Tetairoa McMillan/Carolina Panthers RC
RA-TR Tate Ratledge/Detroit Lions RC
RA-TRHU Travis Hunter/Jacksonville Jaguars RC
RA-TW Tyleik Williams/Detroit Lions RC
RA-TWA Tyler Warren/Indianapolis Colts RC
RA-TYS Tyler Shough/New Orleans Saints RC
RA-WC Will Campbell/New England Patriots RC
RA-WH Will Howard/Pittsburgh Steelers RC
RA-WJ Will Johnson/Arizona Cardinals RC
RA-WMA Woody Marks/Houston Texans RC
RA-WN Walter Nolen/Arizona Cardinals RC
RA-XW Xavier Watts/Atlanta Falcons RC"""

    TOPPS_1990_AUTO = """1990-AK Alvin Kamara/New Orleans Saints
1990-BN Bo Nix/Denver Broncos
1990-CB Chase Brown/Cincinnati Bengals
1990-CD Cooper DeJean/Philadelphia Eagles
1990-CL Colston Loveland/Chicago Bears RC
1990-CW Cam Ward/Tennessee Titans RC
1990-DG Dillon Gabriel/Cleveland Browns RC
1990-DMA Drake Maye/New England Patriots
1990-DP Dak Prescott/Dallas Cowboys
1990-EE Emeka Egbuka/Tampa Bay Buccaneers RC
1990-GK George Kittle/San Francisco 49ers
1990-JA Jordan Addison/Minnesota Vikings
1990-JD Jaxson Dart/New York Giants RC
1990-JDA Jayden Daniels/Washington Commanders
1990-JH Jayden Higgins/Houston Texans RC
1990-JJ Josh Jacobs/Green Bay Packers
1990-JR Jalen Royals/Kansas City Chiefs RC
1990-JW Jaylen Waddle/Miami Dolphins
1990-KC Keon Coleman/Buffalo Bills
1990-LB Luther Burden III/Chicago Bears RC
1990-LM Ladd McConkey/Los Angeles Chargers
1990-MG Matthew Golden/Green Bay Packers RC
1990-MH Marvin Harrison Jr./Arizona Cardinals
1990-MN Malik Nabers/New York Giants
1990-MT Mason Taylor/New York Jets RC
1990-NC Nico Collins/Houston Texans
1990-OH Omarion Hampton/Los Angeles Chargers RC
1990-PN Puka Nacua/Los Angeles Rams
1990-SW Savion Williams/Green Bay Packers RC
1990-THE TreVeyon Henderson/New England Patriots RC
1990-TMB Trey McBride/Arizona Cardinals
1990-TS Tyler Shough/New Orleans Saints RC
1990-TW Tyler Warren/Indianapolis Colts RC
1990-WH Will Howard/Pittsburgh Steelers RC"""

    DUAL_AUTO_LINES = [
        "DA-AK: Josh Allen/Buffalo Bills + Jim Kelly/Buffalo Bills",
        "DA-BJ: Quinshon Judkins/Cleveland Browns RC + Isaiah Bond/Cleveland Browns RC",
        "DA-BW: Brock Bowers/Las Vegas Raiders + Tyler Warren/Indianapolis Colts RC",
        "DA-FB: Kaleb Johnson/Pittsburgh Steelers RC + Jerome Bettis/Pittsburgh Steelers",
        "DA-GE: Emeka Egbuka/Tampa Bay Buccaneers RC + Matthew Golden/Green Bay Packers RC",
        "DA-HB: Pat Bryant/Denver Broncos RC + RJ Harvey/Denver Broncos RC",
        "DA-HH: Tre Harris III/Los Angeles Chargers RC + Omarion Hampton/Los Angeles Chargers RC",
        "DA-HMA: Drake Maye/New England Patriots + TreVeyon Henderson/New England Patriots RC",
        "DA-IE: Bucky Irving/Tampa Bay Buccaneers + Emeka Egbuka/Tampa Bay Buccaneers RC",
        "DA-JS: Ashton Jeanty/Las Vegas Raiders RC + Cam Skattebo/New York Giants RC",
        "DA-LP: CeeDee Lamb/Dallas Cowboys + George Pickens/Dallas Cowboys",
        "DA-NA: Davante Adams/Los Angeles Rams + Puka Nacua/Los Angeles Rams",
        "DA-SD: Cam Skattebo/New York Giants RC + Jaxson Dart/New York Giants RC",
    ]

    FUTURE_STARS_AUTO = """FSA-BB Brock Bowers/Las Vegas Raiders
FSA-BI Bucky Irving/Tampa Bay Buccaneers
FSA-BN Bo Nix/Denver Broncos
FSA-BY Bryce Young/Carolina Panthers
FSA-CB Chase Brown/Cincinnati Bengals
FSA-CD Cooper DeJean/Philadelphia Eagles
FSA-CS CJ Stroud/Houston Texans
FSA-CW Caleb Williams/Chicago Bears
FSA-DA De'Von Achane/Miami Dolphins
FSA-DM Drake Maye/New England Patriots
FSA-JD Jayden Daniels/Washington Commanders
FSA-JG Jahmyr Gibbs/Detroit Lions
FSA-JMC Jalen McMillan/Tampa Bay Buccaneers
FSA-JV Jared Verse/Los Angeles Rams
FSA-JW Jaylen Wright/Miami Dolphins
FSA-KC Keon Coleman/Buffalo Bills
FSA-KH Kyle Hamilton/Baltimore Ravens
FSA-LM Ladd McConkey/Los Angeles Chargers
FSA-MH Marvin Harrison Jr./Arizona Cardinals
FSA-MN Malik Nabers/New York Giants
FSA-PN Puka Nacua/Los Angeles Rams
FSA-PS Pat Surtain II/Denver Broncos
FSA-RP Ricky Pearsall/San Francisco 49ers
FSA-TB Trey Benson/Arizona Cardinals
FSA-TJ Theo Johnson/New York Giants"""

    CHROMOGRAPHS = """CG-AJ Ashton Jeanty/Las Vegas Raiders RC
CG-BB Brock Bowers/Las Vegas Raiders
CG-BN Bo Nix/Denver Broncos
CG-CL Colston Loveland/Chicago Bears RC
CG-CS C.J. Stroud/Houston Texans
CG-CW Caleb Williams/Chicago Bears
CG-CWA Cam Ward/Tennessee Titans RC
CG-DM Drake Maye/New England Patriots
CG-DP Dak Prescott/Dallas Cowboys
CG-JA Josh Allen/Buffalo Bills
CG-JCO James Cook/Buffalo Bills
CG-JD Jayden Daniels/Washington Commanders
CG-JDA Jaxson Dart/New York Giants RC
CG-JJ Justin Jefferson/Minnesota Vikings
CG-JSN Jaxon Smith-Njigba/Seattle Seahawks
CG-JWA Jaylen Waddle/Miami Dolphins
CG-KJ Kaleb Johnson/Pittsburgh Steelers RC
CG-ME Mike Evans/Tampa Bay Buccaneers
CG-MGA Myles Garrett/Cleveland Browns
CG-MGO Matthew Golden/Green Bay Packers RC
CG-PN Puka Nacua/Los Angeles Rams
CG-RJH RJ Harvey/Denver Broncos RC
CG-TJW T.J. Watt/Pittsburgh Steelers
CG-TWA Tyler Warren/Indianapolis Colts RC"""

    CHROME_LEGENDS_AUTO = """CLA-AG A.J. Green/Cincinnati Bengals
CLA-AP Adrian Peterson/Minnesota Vikings
CLA-BU Brian Urlacher/Chicago Bears
CLA-CC Cris Carter/Minnesota Vikings
CLA-CJ Chris Johnson/Tennessee Titans
CLA-DB Drew Brees/New Orleans Saints
CLA-DF Dan Fouts/San Diego Chargers
CLA-DM Dan Marino/Miami Dolphins
CLA-EJ Edgerrin James/Indianapolis Colts
CLA-ER Ed Reed/Baltimore Ravens
CLA-FT Fred Taylor/Jacksonville Jaguars
CLA-GB Gilbert Brown/Green Bay Packers
CLA-HD Hugh Douglas/Philadelphia Eagles
CLA-JC Josh Cribbs/Cleveland Browns
CLA-JK Jim Kelly/Buffalo Bills
CLA-JL Jamal Lewis/Baltimore Ravens
CLA-JP Julius Peppers/Carolina Panthers
CLA-JWI Jason Witten/Dallas Cowboys
CLA-MF Marshall Faulk/St. Louis Rams
CLA-MS Marcus Stroud/Jacksonville Jaguars
CLA-NS Ndamukong Suh/Detroit Lions
CLA-PPR Peerless Price/Buffalo Bills
CLA-TB Tom Brady/Tampa Bay Buccaneers
CLA-TBR Tim Brown/Oakland Raiders
CLA-TD Terrell Davis/Denver Broncos
CLA-TR Tony Romo/Dallas Cowboys
CLA-VD Vernon Davis/San Francisco 49ers
CLA-VW Vince Wilfork/New England Patriots"""

    HALL_OF_CHROME_AUTO = """HOCA-AG Antonio Gates/San Diego Chargers
HOCA-AJ Andre Johnson/Houston Texans
HOCA-BC Bill Cowher/Pittsburgh Steelers
HOCA-BF Brett Favre/Green Bay Packers
HOCA-BS Barry Sanders/Detroit Lions
HOCA-BY Bryant Young/San Francisco 49ers
HOCA-CW Charles Woodson/Oakland Raiders
HOCA-DP Drew Pearson/Dallas Cowboys
HOCA-DR Darrelle Revis/New York Jets
HOCA-DW DeMarcus Ware/Dallas Cowboys
HOCA-EA Eric Allen/Philadelphia Eagles
HOCA-IB Isaac Bruce/St. Louis Rams
HOCA-JA Jared Allen/Minnesota Vikings
HOCA-JE John Elway/Denver Broncos
HOCA-JK Joe Klecko/New York Jets
HOCA-LB LeRoy Butler/Green Bay Packers
HOCA-MS Michael Strahan/New York Giants
HOCA-PM Peyton Manning/Indianapolis Colts
HOCA-RB Ronde Barber/Tampa Bay Buccaneers
HOCA-RL Ray Lewis/Baltimore Ravens
HOCA-RM Randy Moss/Minnesota Vikings
HOCA-RS Richard Seymour/New England Patriots
HOCA-SS Sterling Sharpe/Green Bay Packers
HOCA-TA Troy Aikman/Dallas Cowboys
HOCA-TO Terrell Owens/Philadelphia Eagles
HOCA-TP Troy Polamalu/Pittsburgh Steelers
HOCA-ZT Zach Thomas/Miami Dolphins"""

    ROOKIE_AUTO_VAR = """RRA-ABO Andres Borregales/New England Patriots RC
RRA-ACO Alfred Collins/San Francisco 49ers RC
RRA-AG Ashton Gillotte/Kansas City Chiefs RC
RRA-AM Andrew Mukuba/Philadelphia Eagles RC
RRA-APR Antwaun Powell-Ryland/Philadelphia Eagles RC
RRA-BS Bradyn Swinson/New England Patriots RC
RRA-CB Cobee Bryant/Atlanta Falcons RC
RRA-CDI Chimere Dike/Tennessee Titans RC
RRA-CPJ Chris Paul Jr./Los Angeles Rams RC
RRA-CSC Carson Schwesinger/Cleveland Browns RC
RRA-DE Donovan Ezeiruaku/Dallas Cowboys RC
RRA-DTJ Dont'e Thornton Jr./Las Vegas Raiders RC
RRA-GME Graham Mertz/Houston Texans RC
RRA-JBAS Jeffrey Bassa/Kansas City Chiefs RC
RRA-JBR Jake Briningstool/Kansas City Chiefs RC
RRA-JCA Jamaree Caldwell/Los Angeles Chargers RC
RRA-JCJ Josh Conerly Jr./Washington Commanders RC
RRA-JL Jaylin Lane/Washington Commanders RC
RRA-JMJ Jason Marshall Jr./Miami Dolphins RC
RRA-JST Josaiah Stewart/Los Angeles Rams RC
RRA-KK Kyle Kennard/Los Angeles Chargers RC
RRA-KMCC Kyle McCord/Philadelphia Eagles RC
RRA-LL Luke Lachey/Houston Texans RC
RRA-LRA Lathan Ransom/Carolina Panthers RC
RRA-MH Maxwell Hairston/Buffalo Bills RC
RRA-MM Malachi Moore/New York Jets RC
RRA-NMA Nick Martin/San Francisco 49ers RC
RRA-OGII Oronde Gadsden/Los Angeles Chargers RC
RRA-ONL Omarr Norman-Lott/Kansas City Chiefs RC
RRA-RRS Raheim Sanders/Cleveland Browns RC
RRA-TB Tahj Brooks/Cincinnati Bengals RC
RRA-TE Trevor Etienne/Carolina Panthers RC
RRA-TJS T.J. Sanders/Buffalo Bills RC
RRA-TOH Tory Horton/Seattle Seahawks RC
RRA-TYR Ty Robinson/Philadelphia Eagles RC
RRA-WJ Will Johnson/Arizona Cardinals RC
RRA-WN Walter Nolen/Arizona Cardinals RC
RRA-XRE Xavier Restrepo/Tennessee Titans RC"""

    NFL_HONORS_AUTO = """GSA-JA Josh Allen/Buffalo Bills
GSA-JD Jayden Daniels/Washington Commanders
GSA-JV Jared Verse/Los Angeles Rams
GSA-PSII Pat Surtain II/Denver Broncos
GSA-SB Saquon Barkley/Philadelphia Eagles"""

    auto_sets = [
        ("Base Cards Autograph Variation", BASE_CARDS_AUTO),
        ("Rookies Autograph Variation", ROOKIES_AUTO),
        ("1990 Topps Football Autographs", TOPPS_1990_AUTO),
        ("Future Stars Autographs", FUTURE_STARS_AUTO),
        ("Chromographs", CHROMOGRAPHS),
        ("Chrome Legends Autographs", CHROME_LEGENDS_AUTO),
        ("Hall of Chrome Autographs", HALL_OF_CHROME_AUTO),
        ("Rookie Autographs Variation", ROOKIE_AUTO_VAR),
        ("NFL Honors Gold Shield Autographs", NFL_HONORS_AUTO),
    ]

    for name, raw in auto_sets:
        cards = parse_coded_cards(raw)
        sections.append({"insert_set": name, "parallels": AUTO_PARALLELS, "cards": cards})

    # Dual Autographs (co_players via duplicate card_number)
    dual_cards = parse_dual_cards(DUAL_AUTO_LINES)
    sections.append({"insert_set": "Dual Autographs", "parallels": AUTO_PARALLELS, "cards": dual_cards})

    # ── 5. Relic sections with AUTO_PARALLELS ─────────────────────────────

    ROOKIE_RELICS = """RR-AC Abdul Carter/New York Giants RC
RR-AJ Ashton Jeanty/Las Vegas Raiders RC
RR-CL Colston Loveland/Chicago Bears RC
RR-CS Cam Skattebo/New York Giants RC
RR-CW Cam Ward/Tennessee Titans RC
RR-DG Dillon Gabriel/Cleveland Browns RC
RR-EAY Elic Ayomanor/Tennessee Titans RC
RR-EE Emeka Egbuka/Tampa Bay Buccaneers RC
RR-ERR Elijah Arroyo/Seattle Seahawks RC
RR-JB Jack Bech/Las Vegas Raiders RC
RR-JBL Jaydon Blue/Dallas Cowboys RC
RR-JD Jaxson Dart/New York Giants RC
RR-JH Jayden Higgins/Houston Texans RC
RR-JL Jaylin Lane/Washington Commanders RC
RR-JN Jaylin Noel/Houston Texans RC
RR-JR Jalen Royals/Kansas City Chiefs RC
RR-KJ Kaleb Johnson/Pittsburgh Steelers RC
RR-KM Kyle McCord/Philadelphia Eagles RC
RR-KWI Kyle Williams/New England Patriots RC
RR-LB Luther Burden III/Chicago Bears RC
RR-MG Matthew Golden/Green Bay Packers RC
RR-MT Mason Taylor/New York Jets RC
RR-MW Mykel Williams/San Francisco 49ers RC
RR-OH Omarion Hampton/Los Angeles Chargers RC
RR-PB Pat Bryant/Denver Broncos RC
RR-QJ Quinshon Judkins/Cleveland Browns RC
RR-RH RJ Harvey/Denver Broncos RC
RR-RL Riley Leonard/Indianapolis Colts RC
RR-SW Savion Williams/Green Bay Packers RC
RR-TET Trevor Etienne/Carolina Panthers RC
RR-TF Tai Felton/Minnesota Vikings RC
RR-TFE Terrance Ferguson/Los Angeles Rams RC
RR-TH TreVeyon Henderson/New England Patriots RC
RR-THA Tre Harris III/Los Angeles Chargers RC
RR-TJ Tez Johnson/Tampa Bay Buccaneers RC
RR-TS Tyler Shough/New Orleans Saints RC
RR-TW Tyler Warren/Indianapolis Colts RC
RR-WH Will Howard/Pittsburgh Steelers RC"""

    FIRST_YEAR_FABRIC = """FYF-AC Abdul Carter/New York Giants RC
FYF-AJ Ashton Jeanty/Las Vegas Raiders RC
FYF-CL Colston Loveland/Chicago Bears RC
FYF-CS Cam Skattebo/New York Giants RC
FYF-CW Cam Ward/Tennessee Titans RC
FYF-DG Dillon Gabriel/Cleveland Browns RC
FYF-EE Emeka Egbuka/Tampa Bay Buccaneers RC
FYF-JD Jaxson Dart/New York Giants RC
FYF-JR Jalen Royals/Kansas City Chiefs RC
FYF-KJ Kaleb Johnson/Pittsburgh Steelers RC
FYF-LB Luther Burden III/Chicago Bears RC
FYF-MG Matthew Golden/Green Bay Packers RC
FYF-OH Omarion Hampton/Los Angeles Chargers RC
FYF-RH RJ Harvey/Denver Broncos RC
FYF-TH Tre Harris III/Los Angeles Chargers RC
FYF-THE TreVeyon Henderson/New England Patriots RC
FYF-TS Tyler Shough/New Orleans Saints RC
FYF-TW Tyler Warren/Indianapolis Colts RC
FYF-WH Will Howard/Pittsburgh Steelers RC"""

    NFL_HONORS_RELIC = """HGS-JA Josh Allen/Buffalo Bills
HGS-JD Jayden Daniels/Washington Commanders
HGS-JV Jared Verse/Los Angeles Rams
HGS-PSII Pat Surtain II/Denver Broncos
HGS-SB Saquon Barkley/Philadelphia Eagles"""

    relic_sets = [
        ("Topps Chrome Rookie Relics", ROOKIE_RELICS),
        ("First Year Fabric", FIRST_YEAR_FABRIC),
        ("NFL Honors Gold Shield Relics", NFL_HONORS_RELIC),
    ]

    for name, raw in relic_sets:
        cards = parse_coded_cards(raw)
        sections.append({"insert_set": name, "parallels": AUTO_PARALLELS, "cards": cards})

    # ── 6. Auto-relic sections with AUTO_PARALLELS ────────────────────────

    ROOKIE_PATCH_AUTO = """RPA-AC Abdul Carter/New York Giants RC
RPA-AJ Ashton Jeanty/Las Vegas Raiders RC
RPA-CL Colston Loveland/Chicago Bears RC
RPA-CS Cam Skattebo/New York Giants RC
RPA-CW Cam Ward/Tennessee Titans RC
RPA-DG Dillon Gabriel/Cleveland Browns RC
RPA-EA Elic Ayomanor/Tennessee Titans RC
RPA-EAR Elijah Arroyo/Seattle Seahawks RC
RPA-EE Emeka Egbuka/Tampa Bay Buccaneers RC
RPA-JB Jack Bech/Las Vegas Raiders RC
RPA-JBL Jaydon Blue/Dallas Cowboys RC
RPA-JD Jaxson Dart/New York Giants RC
RPA-JH Jayden Higgins/Houston Texans RC
RPA-JL Jaylin Lane/Washington Commanders RC
RPA-JN Jaylin Noel/Houston Texans RC
RPA-JR Jalen Royals/Kansas City Chiefs RC
RPA-KJ Kaleb Johnson/Pittsburgh Steelers RC
RPA-KM Kyle McCord/Philadelphia Eagles RC
RPA-KW Kyle Williams/New England Patriots RC
RPA-LB Luther Burden III/Chicago Bears RC
RPA-MG Matthew Golden/Green Bay Packers RC
RPA-MT Mason Taylor/New York Jets RC
RPA-MW Mykel Williams/San Francisco 49ers RC
RPA-OH Omarion Hampton/Los Angeles Chargers RC
RPA-PB Pat Bryant/Denver Broncos RC
RPA-QJ Quinshon Judkins/Cleveland Browns RC
RPA-RH RJ Harvey/Denver Broncos RC
RPA-RL Riley Leonard/Indianapolis Colts RC
RPA-SW Savion Williams/Green Bay Packers RC
RPA-TE Trevor Etienne/Carolina Panthers RC
RPA-TF Tai Felton/Minnesota Vikings RC
RPA-TFE Terrance Ferguson/Los Angeles Rams RC
RPA-TH TreVeyon Henderson/New England Patriots RC
RPA-THIII Tre Harris III/Los Angeles Chargers RC
RPA-TJ Tez Johnson/Tampa Bay Buccaneers RC
RPA-TS Tyler Shough/New Orleans Saints RC
RPA-TW Tyler Warren/Indianapolis Colts RC
RPA-WH Will Howard/Pittsburgh Steelers RC"""

    ROOKIE_PREMIERE_PATCH = """RPPA-AC Alfred Collins/San Francisco 49ers RC
RPPA-AE Aireontae Ersery/Houston Texans RC
RPPA-AG Ashton Gillotte/Kansas City Chiefs RC
RPPA-AME Armand Membou/New York Jets RC
RPPA-AT Azareye'h Thomas/New York Jets RC
RPPA-BB Billy Bowman Jr./Atlanta Falcons RC
RPPA-BCA Barrett Carter/Cincinnati Bengals RC
RPPA-BM Benjamin Morrison/Tampa Bay Buccaneers RC
RPPA-BS Brashard Smith/Kansas City Chiefs RC
RPPA-BT Bhayshul Tuten/Jacksonville Jaguars RC
RPPA-CB Cobee Bryant/Atlanta Falcons RC
RPPA-CD Chimere Dike/Tennessee Titans RC
RPPA-CLO Colston Loveland/Chicago Bears RC
RPPA-CS Cam Skattebo/New York Giants RC
RPPA-CSC Carson Schwesinger/Cleveland Browns RC
RPPA-CW Cam Ward/Tennessee Titans RC
RPPA-DA Darius Alexander/New York Giants RC
RPPA-DB Denzel Burke/Arizona Cardinals RC
RPPA-DG DJ Giddens/Indianapolis Colts RC
RPPA-DGA Dillon Gabriel/Cleveland Browns RC
RPPA-DJ Donovan Jackson/Minnesota Vikings RC
RPPA-DP Darien Porter/Las Vegas Raiders RC
RPPA-DS Danny Stutsman/New Orleans Saints RC
RPPA-DSA Dylan Sampson/Cleveland Browns RC
RPPA-DTJ Dont'e Thornton Jr./Las Vegas Raiders RC
RPPA-EA Elic Ayomanor/Tennessee Titans RC
RPPA-EAR Elijah Arroyo/Seattle Seahawks RC
RPPA-EE Emeka Egbuka/Tampa Bay Buccaneers RC
RPPA-GH Gunnar Helm/Tennessee Titans RC
RPPA-GZ Grey Zabel/Seattle Seahawks RC
RPPA-HF Harold Fannin Jr./Cleveland Browns RC
RPPA-IB Isaiah Bond/Cleveland Browns RC
RPPA-IT Isaac TeSlaa/Detroit Lions RC
RPPA-JAH Jayden Higgins/Houston Texans RC
RPPA-JB Jordan Burch/Arizona Cardinals RC
RPPA-JBA Jahdae Barron/Denver Broncos RC
RPPA-JCA Jamaree Caldwell/Los Angeles Chargers RC
RPPA-JD Jaxson Dart/New York Giants RC
RPPA-JEB Jeffrey Bassa/Kansas City Chiefs RC
RPPA-JHI Jay Higgins IV/Baltimore Ravens RC
RPPA-JK Jack Kiser/Jacksonville Jaguars RC
RPPA-JN Jaylin Noel/Houston Texans RC
RPPA-JOS Josaiah Stewart/Los Angeles Rams RC
RPPA-JOSA Jonas Sanker/New Orleans Saints RC
RPPA-JR Jalen Royals/Kansas City Chiefs RC
RPPA-JSA Jonah Savaiinaea/Miami Dolphins RC
RPPA-JSAW Jack Sawyer/Pittsburgh Steelers RC
RPPA-JSI Josh Simmons/Kansas City Chiefs RC
RPPA-JTU JT Tuimoloau/Indianapolis Colts RC
RPPA-JWA Jalon Walker/Atlanta Falcons RC
RPPA-KB Kelvin Banks Jr./New Orleans Saints RC
RPPA-KG Kenneth Grant/Miami Dolphins RC
RPPA-KJ Kaleb Johnson/Pittsburgh Steelers RC
RPPA-KKE Kyle Kennard/Los Angeles Chargers RC
RPPA-KM Kalel Mullings/Tennessee Titans RC
RPPA-KMO Kyle Monangai/Chicago Bears RC
RPPA-KW Kyle Williams/New England Patriots RC
RPPA-LA LeQuint Allen Jr./Jacksonville Jaguars RC
RPPA-LB Luther Burden III/Chicago Bears RC
RPPA-LR Lathan Ransom/Carolina Panthers RC
RPPA-ME Mitchell Evans/Carolina Panthers RC
RPPA-MG Matthew Golden/Green Bay Packers RC
RPPA-MGR Mason Graham/Cleveland Browns RC
RPPA-MGRE Mike Green/Baltimore Ravens RC
RPPA-MMB Marcus Mbow/New York Giants RC
RPPA-MMO Malachi Moore/New York Jets RC
RPPA-MST Malaki Starks/Baltimore Ravens RC
RPPA-MT Mason Taylor/New York Jets RC
RPPA-MW Mykel Williams/San Francisco 49ers RC
RPPA-NM Nick Martin/San Francisco 49ers RC
RPPA-NS Nic Scourton/Carolina Panthers RC
RPPA-OG Ollie Gordon II/Miami Dolphins RC
RPPA-OH Omarion Hampton/Los Angeles Chargers RC
RPPA-ON Omarr Norman-Lott/Kansas City Chiefs RC
RPPA-PB Pat Bryant/Denver Broncos RC
RPPA-QJ Quinshon Judkins/Cleveland Browns RC
RPPA-QR Quincy Riley/New Orleans Saints RC
RPPA-SM Smael Mondon Jr./Philadelphia Eagles RC
RPPA-SS Shedeur Sanders/Cleveland Browns RC
RPPA-SST Shemar Stewart/Cincinnati Bengals RC
RPPA-ST Shemar Turner/Chicago Bears RC
RPPA-SW Savion Williams/Green Bay Packers RC
RPPA-TBR Tahj Brooks/Cincinnati Bengals RC
RPPA-TF Tai Felton/Minnesota Vikings RC
RPPA-TFE Terrance Ferguson/Los Angeles Rams RC
RPPA-TH Tory Horton/Seattle Seahawks RC
RPPA-THA Tre Harris III/Los Angeles Chargers RC
RPPA-THE TreVeyon Henderson/New England Patriots RC
RPPA-THU Travis Hunter/Jacksonville Jaguars RC
RPPA-TM Tetairoa McMillan/Carolina Panthers RC
RPPA-TR Ty Robinson/Philadelphia Eagles RC
RPPA-TRA Tate Ratledge/Detroit Lions RC
RPPA-TS Tyler Shough/New Orleans Saints RC
RPPA-TW Tyler Warren/Indianapolis Colts RC
RPPA-TWI Tyleik Williams/Detroit Lions RC
RPPA-WC Will Campbell/New England Patriots RC
RPPA-WM Woody Marks/Houston Texans RC
RPPA-XW Xavier Watts/Atlanta Falcons RC"""

    auto_relic_sets = [
        ("Topps Chrome Rookie Patch Autographs", ROOKIE_PATCH_AUTO),
        ("Rookie Premiere Patch Autographs", ROOKIE_PREMIERE_PATCH),
    ]

    for name, raw in auto_relic_sets:
        cards = parse_coded_cards(raw)
        sections.append({"insert_set": name, "parallels": AUTO_PARALLELS, "cards": cards})

    # ── 7. Fanatics Authentics Redemption Cards (no codes, no parallels) ──

    FANATICS_RAW = [
        ("", "Drake Maye", "New England Patriots", False),
        ("", "Ricky Williams", "New Orleans Saints", False),
        ("", "Jaxson Dart", "New York Giants", True),
        ("", "Justin Jefferson", "Minnesota Vikings", False),
        ("", "Dan Marino", "Miami Dolphins", False),
        ("", "Justin Herbert", "Los Angeles Chargers", False),
        ("", "Davante Adams", "Los Angeles Rams", False),
        ("", "Garrett Wilson", "New York Jets", False),
        ("", "Jalen Hurts", "Philadelphia Eagles", False),
        ("", "Calvin Ridley", "Tennessee Titans", False),
        ("", "Jayden Daniels", "Washington Commanders", False),
        ("", "Emeka Egbuka", "Tampa Bay Buccaneers", True),
        ("", "Jaxon Smith-Njigba", "Seattle Seahawks", False),
        ("", "Ben Roethlisberger", "Pittsburgh Steelers", False),
        ("", "Brock Purdy", "San Francisco 49ers", False),
        ("", "Ashton Jeanty", "Las Vegas Raiders", True),
        ("", "Xavier Worthy", "Kansas City Chiefs", False),
        ("", "Caleb Williams", "Chicago Bears", False),
        ("", "Joe Burrow", "Cincinnati Bengals", False),
        ("", "Ja'Marr Chase", "Cincinnati Bengals", False),
        ("", "Bryce Young", "Carolina Panthers", False),
        ("", "Dalton Kincaid", "Buffalo Bills", False),
        ("", "Michael Penix Jr.", "Atlanta Falcons", False),
        ("", "Zay Flowers", "Baltimore Ravens", False),
        ("", "Quinshon Judkins", "Cleveland Browns", True),
        ("", "CeeDee Lamb", "Dallas Cowboys", False),
        ("", "Jonathan Taylor", "Indianapolis Colts", False),
        ("", "Trevor Lawrence", "Jacksonville Jaguars", False),
        ("", "CJ Stroud", "Houston Texans", False),
        ("", "Charles Woodson", "Green Bay Packers", False),
        ("", "Bo Nix", "Denver Broncos", False),
        ("", "Jahmyr Gibbs", "Detroit Lions", False),
        ("", "Kyler Murray", "Arizona Cardinals", False),
    ]

    fanatics_cards = []
    for code, player, team, is_rc in FANATICS_RAW:
        fanatics_cards.append({"card_number": code, "player": player, "team": team, "is_rookie": is_rc, "subset": None})
    sections.append({"insert_set": "Fanatics Authentics Redemption Cards", "parallels": NO_PARALLELS, "cards": fanatics_cards})

    return sections


# ── Stats computation ─────────────────────────────────────────────────────
def compute_stats(appearances):
    unique_cards = len(appearances)
    total_print_run = 0
    one_of_ones = 0
    insert_set_names = set()

    for app in appearances:
        insert_set_names.add(app["insert_set"])

        # Add all numbered parallels
        has_superfractor = False
        for p in app["parallels"]:
            if p["print_run"] is not None and p["print_run"] > 0:
                total_print_run += p["print_run"]
                if p["print_run"] == 1:
                    has_superfractor = True

        if has_superfractor:
            one_of_ones += 1

    return {
        "unique_cards": unique_cards,
        "total_print_run": total_print_run,
        "one_of_ones": one_of_ones,
        "insert_sets": len(insert_set_names),
    }


# ── Build output ──────────────────────────────────────────────────────────
def build_output(sections):
    # Collect all rookie players to propagate is_rookie consistently
    rc_players = set()
    for section in sections:
        for card in section["cards"]:
            if card.get("is_rookie"):
                rc_players.add(card["player"])

    # Build player index: player name -> list of appearances
    player_index = {}
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

    players_list = []
    for pname in sorted(player_index.keys()):
        data = player_index[pname]
        players_list.append({
            "player": pname,
            "appearances": data["appearances"],
            "stats": compute_stats(data["appearances"]),
        })

    output_sections = []
    for section in sections:
        output_sections.append({
            "insert_set": section["insert_set"],
            "parallels": section["parallels"],
            "cards": section["cards"],
        })

    return {
        "set_name": "2025 Topps Chrome Football",
        "sport": "Football",
        "season": "2025",
        "league": "NFL",
        "sections": output_sections,
        "players": players_list,
    }


# ── Entry point ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Parsing 2025 Topps Chrome Football...")

    sections = build_sections()
    output = build_output(sections)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nSet: {output['set_name']} ({output['season']})")
    print(f"Sections: {len(output['sections'])}")
    for s in output["sections"]:
        print(f"  {s['insert_set']:<52} {len(s['cards']):>4} cards  {len(s['parallels']):>2} parallels")

    print(f"\nTotal unique players: {len(output['players'])}")

    player_map = {p["player"]: p for p in output["players"]}

    print("\n=== Spot checks ===")
    for name in ["Travis Hunter", "Cam Ward", "Josh Allen", "Patrick Mahomes II", "Tom Brady"]:
        if name in player_map:
            st = player_map[name]["stats"]
            print(f"  {name}: {st['insert_sets']} insert sets, "
                  f"{st['unique_cards']} unique cards, "
                  f"{st['total_print_run']} total print run, "
                  f"{st['one_of_ones']} 1/1s")
        else:
            print(f"  {name}: NOT FOUND")

    # Verify key counts
    section_map = {s["insert_set"]: s for s in output["sections"]}
    expected = {
        "Base Set": 400,
        "Power Players": 40,
        "Legends of the Gridiron": 40,
        "Fortune 15": 35,
        "All Chrome Team": 25,
        "Chrome Radiating Rookies": 20,
        "Urban Legends": 30,
        "Helix": 30,
        "Shadow Etch": 30,
        "Game Genies": 25,
        "Kaiju": 10,
        "Let's Go": 5,
        "Ultra Violet": 20,
        "Lightning Leaders": 20,
        "Fanatical": 30,
        "Base Cards Autograph Variation": 70,
        "Rookies Autograph Variation": 94,
        "1990 Topps Football Autographs": 34,
        "Dual Autographs": 26,  # 13 cards x 2 players each
        "Future Stars Autographs": 25,
        "Chromographs": 24,
        "Chrome Legends Autographs": 28,
        "Hall of Chrome Autographs": 27,
        "Rookie Autographs Variation": 38,
        "NFL Honors Gold Shield Autographs": 5,
        "Topps Chrome Rookie Relics": 38,
        "First Year Fabric": 19,
        "NFL Honors Gold Shield Relics": 5,
        "Topps Chrome Rookie Patch Autographs": 38,
        "Rookie Premiere Patch Autographs": 98,
        "Fanatics Authentics Redemption Cards": 33,
        "Future Stars": 25,
        "1975 Topps": 35,
    }

    print("\n=== Card count verification ===")
    all_ok = True
    for name, exp_count in sorted(expected.items()):
        if name in section_map:
            actual = len(section_map[name]["cards"])
            status = "OK" if actual == exp_count else "MISMATCH"
            if status == "MISMATCH":
                all_ok = False
            print(f"  {name:<52} expected={exp_count:>4}  actual={actual:>4}  {status}")
        else:
            all_ok = False
            print(f"  {name:<52} MISSING")

    if all_ok:
        print("\nAll card counts verified!")
    else:
        print("\nWARNING: Some card counts don't match!")

    print(f"\nOutput written to: {OUTPUT}")
