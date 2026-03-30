import json
import re

# ─────────────────────────────────────────────────────────────
# Parallel definitions
# ─────────────────────────────────────────────────────────────

BASE_PARALLELS = [
    {"name": "Black Bordered", "print_run": None},
    {"name": "Dark Gray Bordered", "print_run": None},
    {"name": "Dark Green Bordered", "print_run": None},
    {"name": "Dark Yellow Bordered", "print_run": None},
    {"name": "Deckle Edge", "print_run": None},
    {"name": "Flip Stock", "print_run": None},
    {"name": "Light Purple Bordered", "print_run": None},
    {"name": "Red Bordered", "print_run": None},
    {"name": "Color of the Year Heritage Orange", "print_run": 77},
]

CHROME_PARALLELS = [
    {"name": "Refractor", "print_run": None},
    {"name": "Aqua Sparkle", "print_run": None},
    {"name": "Burgundy Sparkle", "print_run": None},
    {"name": "Light Blue Sparkle", "print_run": None},
    {"name": "Pink Sparkle", "print_run": None},
    {"name": "Silver Sparkle", "print_run": None},
    {"name": "Blue Bordered", "print_run": 150},
    {"name": "Green Bordered", "print_run": 99},
    {"name": "Black Bordered", "print_run": 77},   # Chrome Black Bordered /77 — distinct from base
    {"name": "Gold Bordered", "print_run": 50},
    {"name": "Orange Bordered", "print_run": 25},
    {"name": "Red Bordered", "print_run": 5},
    {"name": "Superfractor", "print_run": 1},
]

PARALLELS_RED_INK = [{"name": "Red Ink", "print_run": 77}]

PARALLELS_CHROME_AUTO = [
    {"name": "Gold Bordered", "print_run": 50},
    {"name": "Orange Bordered", "print_run": 25},
    {"name": "Red Bordered", "print_run": 5},
    {"name": "Superfractor", "print_run": 1},
]

PARALLELS_PATCH = [{"name": "Patch", "print_run": None}]

PARALLELS_RED_PATCH = [
    {"name": "Red", "print_run": 77},
    {"name": "Patch", "print_run": None},
]

# ─────────────────────────────────────────────────────────────
# Base-set card number ranges with special handling
# ─────────────────────────────────────────────────────────────

LEAGUE_LEADERS_NUMS   = {str(i) for i in range(1,   9)}
RECORD_BREAKERS_NUMS  = {str(i) for i in range(231, 235)}
TEAM_CARD_NUMS        = {"276", "277", "311", "312", "313"}
TBTC_NUMS             = {str(i) for i in range(333, 338)}
ROOKIE_COMBO_NUMS     = {str(i) for i in range(372, 380)} | {str(i) for i in range(387, 395)}

# ─────────────────────────────────────────────────────────────
# Skip patterns (same as other parsers)
# ─────────────────────────────────────────────────────────────

SKIP_RE = re.compile(
    r"^shop for .+|.+\bon ebay$|^\d+ cards?\.?$|^parallels?$|^parallel$"
    r"|^hobby.*exclusive$|^hobby – ",
    re.IGNORECASE,
)

def should_skip(line):
    return bool(SKIP_RE.match(line.strip()))

# ─────────────────────────────────────────────────────────────
# Card line helpers
# ─────────────────────────────────────────────────────────────

CARD_RE = re.compile(r"^([A-Za-z0-9][A-Za-z0-9-]*)\s+(.+)")

def parse_multi_player(card_number, rest, is_rookie=False, subset_tag=None):
    """Parse 'Player1/Player2/..., Team1/Team2/...[RC][*]' into multiple card dicts."""
    rest = rest.strip()
    if rest.endswith("*"):
        rest = rest[:-1].strip()
    if rest.endswith(" RC"):
        is_rookie = True
        rest = rest[:-3].strip()
    if rest.endswith("*"):
        rest = rest[:-1].strip()

    if ", " in rest:
        idx = rest.rindex(", ")
        players_part = rest[:idx]
        teams_part   = rest[idx + 2:]
    else:
        players_part = rest
        teams_part   = ""

    players  = [p.strip() for p in players_part.split("/")]
    teams_raw = [t.strip() for t in teams_part.split("/")] if teams_part else []

    result = []
    for i, player in enumerate(players):
        team = teams_raw[i] if i < len(teams_raw) else (teams_raw[-1] if teams_raw else None)
        result.append({
            "card_number": card_number,
            "player":      player,
            "team":        team,
            "is_rookie":   is_rookie,
            "subset":      subset_tag,
        })
    return result


def parse_league_leaders(card_number, rest):
    """Parse 'P1/P2 T1/T2 (League Leaders)' — no comma between players and teams."""
    rest = re.sub(r"\s*\([^)]+\)\s*$", "", rest).strip()
    parts = [p.strip() for p in rest.split("/")]

    if len(parts) < 3:
        return [{"card_number": card_number, "player": rest,
                 "team": None, "is_rookie": False, "subset": "League Leaders"}]

    player1 = parts[0]
    team2   = parts[-1]
    # Middle: "Player2_First Player2_Last Team1_words..."
    middle_words = parts[1].split()
    player2 = " ".join(middle_words[:2])
    team1   = " ".join(middle_words[2:])

    return [
        {"card_number": card_number, "player": player1, "team": team1,
         "is_rookie": False, "subset": "League Leaders"},
        {"card_number": card_number, "player": player2, "team": team2,
         "is_rookie": False, "subset": "League Leaders"},
    ]


def parse_base_line(line):
    """Parse one base-set card line into a list of card dicts."""
    line = line.strip()
    if not line or should_skip(line):
        return []

    m = re.match(r"^(\d+)\s+(.+)", line)
    if not m:
        return []

    num  = m.group(1)
    rest = m.group(2).strip()

    if num in LEAGUE_LEADERS_NUMS:
        return parse_league_leaders(num, rest)

    if num in ROOKIE_COMBO_NUMS:
        return parse_multi_player(num, rest, is_rookie=True, subset_tag="Rookie Combo")

    # Strip trailing * (short print)
    is_sp = False
    if rest.endswith("*"):
        is_sp = True
        rest = rest[:-1].strip()

    # Extract parenthetical tag BEFORE stripping RC (tag can contain team info)
    m_tag = re.search(r"\(([^)]+)\)\s*$", rest)
    tag   = m_tag.group(1).strip() if m_tag else None
    if m_tag:
        rest = rest[:m_tag.start()].strip()

    # Strip * that might be before parenthetical
    if rest.endswith("*"):
        is_sp = True
        rest = rest[:-1].strip()

    is_rookie = False
    if rest.endswith(" RC"):
        is_rookie = True
        rest = rest[:-3].strip()

    # Determine subset_tag (priority order)
    if num in RECORD_BREAKERS_NUMS:
        subset_tag = "Record Breakers"
    elif num in TBTC_NUMS:
        subset_tag = "Turn Back The Clock"
    elif is_sp:
        subset_tag = "Short Print"
    else:
        subset_tag = None

    # Team Card
    if num in TEAM_CARD_NUMS:
        if ", " in rest:
            team = rest.split(", ", 1)[1].strip()
        else:
            team = rest.strip()
        return [{"card_number": num, "player": "Team Card", "team": team,
                 "is_rookie": False, "subset": None}]

    # Regular card — split on last ", "
    if ", " in rest:
        idx    = rest.rindex(", ")
        player = rest[:idx].strip()
        team   = rest[idx + 2:].strip()
    else:
        player = rest.strip()
        team   = None

    return [{"card_number": num, "player": player, "team": team,
             "is_rookie": is_rookie, "subset": subset_tag}]


def parse_standard_line(line):
    """Parse a standard non-base card line: 'CODE-XX Player, Team'."""
    line = line.strip()
    if not line or should_skip(line):
        return []
    m = CARD_RE.match(line)
    if not m:
        return []
    card_number = m.group(1)
    rest = m.group(2).strip()

    is_rookie = False
    if rest.endswith(" RC"):
        is_rookie = True
        rest = rest[:-3].strip()

    if ", " in rest:
        idx    = rest.rindex(", ")
        player = rest[:idx].strip()
        team   = rest[idx + 2:].strip()
    else:
        player = rest.strip()
        team   = None

    return [{"card_number": card_number, "player": player, "team": team,
             "is_rookie": is_rookie, "subset": None}]


def parse_multi_player_line(line):
    """Parse a multi-player standard line: 'CODE-XX P1/P2, T1/T2'."""
    line = line.strip()
    if not line or should_skip(line):
        return []
    m = CARD_RE.match(line)
    if not m:
        return []
    return parse_multi_player(m.group(1), m.group(2))


# ─────────────────────────────────────────────────────────────
# Checklist data (embedded — no external file needed)
# ─────────────────────────────────────────────────────────────

BASE_SET_RAW = """
1 Aaron Judge/Trea Turner New York Yankees/Philadelphia Phillies (League Leaders)
2 Kyle Schwarber/Cal Raleigh Philadelphia Phillies/Seattle Mariners (League Leaders)
3 Kyle Schwarber/Cal Raleigh Philadelphia Phillies/Seattle Mariners (League Leaders)
4 Oneil Cruz/José Caballero Pittsburgh Pirates/New York Yankees (League Leaders)
5 Freddy Peralta/Max Fried Milwaukee Brewers/New York Yankees (League Leaders)
6 Logan Webb/Garrett Crochet San Francisco Giants/Boston Red Sox (League Leaders)
7 Paul Skenes/Tarik Skubal Pittsburgh Pirates/Detroit Tigers (League Leaders)
8 Robert Suarez/Carlos Estevéz San Diego Padres/Kansas City Royals (League Leaders)
9 Josh Hader, Houston Astros
10 Aaron Judge, New York Yankees
11 Jose Altuve, Houston Astros
12 Mookie Betts, Los Angeles Dodgers
13 Agustín Ramírez, Miami Marlins
14 Jhoan Duran, Philadelphia Phillies*
15 Jarren Duran, Boston Red Sox
16 Kyle Bradish, Baltimore Orioles
17 Jacob Wilson, Athletics
18 Eury Pérez, Miami Marlins
19 Brett Baty, New York Mets
20 Jonathan Aranda, Tampa Bay Rays*
21 Ernie Clement, Toronto Blue Jays*
22 Kris Bryant, Colorado Rockies
23 Garrett Crochet, Boston Red Sox
24 Luis Castillo, Seattle Mariners*
25 Yordan Alvarez, Houston Astros
26 Jaden Hill, Colorado Rockies*
27 Casey Schmitt, San Francisco Giants
28 Nico Hoerner, Chicago Cubs
29 Eugenio Suárez, Seattle Mariners
30 Connor Norby, Miami Marlins*
31 Andrew Abbott, Cincinnati Reds
32 Andre Granillo, St. Louis Cardinals RC
33 Paul Skenes, Pittsburgh Pirates
34 Ryan Pepiot, Tampa Bay Rays
35 Yoán Moncada, Angels
36 Edwin Díaz, Los Angeles Dodgers
37 Jorge Soler, Angels
38 Taj Bradley, Minnesota Twins
39 Roki Sasaki, Los Angeles Dodgers
40 Nathan Eovaldi, Texas Rangers
41 Spencer Strider, Atlanta Braves
42 Jo Adell, Angels
43 Luis García Jr., Washington Nationals
44 Austin Martin, Minnesota Twins
45 Michael A. Taylor, Chicago White Sox
46 Vladimir Guerrero Jr., Toronto Blue Jays
47 Yandy Díaz, Tampa Bay Rays
48 Dylan Beavers, Baltimore Orioles RC
49 Coby Mayo, Baltimore Orioles
50 Robert Hassell III, Washington Nationals
51 Jurickson Profar, Atlanta Braves
52 José Ramírez, Cleveland Guardians
53 Hunter Greene, Cincinnati Reds
54 Jeff McNeil, New York Mets
55 Ronald Acuña Jr., Atlanta Braves
56 José Berríos, Toronto Blue Jays*
57 Patrick Bailey, San Francisco Giants
58 Chandler Simpson, Tampa Bay Rays
59 Harry Ford, Seattle Mariners RC
60 Brooks Lee, Minnesota Twins
61 Miguel Vargas, Chicago White Sox*
62 Rafael Devers, San Francisco Giants
63 Mike Yastrzemski, Kansas City Royals
64 Mitch Keller, Pittsburgh Pirates*
65 Mason Miller, San Diego Padres
66 Darell Hernaiz, Athletics*
67 Luis Morales, Athletics RC
68 Cade Cavalli, Washington Nationals
69 Cam Smith, Houston Astros
70 Elly De La Cruz, Cincinnati Reds RC
71 Reese Olson, Detroit Tigers*
72 Bryce Harper, Philadelphia Phillies
73 Dillon Dingler, Detroit Tigers
74 Tanner Bibee, Cleveland Guardians RC
75 Dane Myers, Miami Marlins
76 Sandy Alcantara, Miami Marlins
77 Mark Vientos, New York Mets
78 Noah Cameron, Kansas City Royals
79 Carson Whisenhunt, San Francisco Giants RC
80 Austin Hays, Cincinnati Reds*
81 Alec Bohm, Philadelphia Phillies
82 Logan Webb, San Francisco Giants
83 Bradley Blalock, Colorado Rockies
84 Maikel Garcia, Kansas City Royals*
85 Royce Lewis, Minnesota Twins
86 Roman Anthony, Boston Red Sox RC
87 Slade Cecconi, Cleveland Guardians
88 Owen Caissie, Chicago Cubs RC
89 Ramón Laureano, San Diego Padres
90 Mike Tauchman, Chicago White Sox
91 Chase Dollander, Colorado Rockies
92 Kyle Freeland, Colorado Rockies
93 Teoscar Hernández, Los Angeles Dodgers*
94 Lawrence Butler, Athletics
95 Brendan Donovan, St. Louis Cardinals
96 Mike Burrows, Pittsburgh Pirates*
97 Dansby Swanson, Chicago Cubs*
98 Jacob deGrom, Texas Rangers
99 Bryan Woo, Seattle Mariners
100 Noelvi Marte, Cincinnati Reds
101 Tyler Soderstrom, Athletics*
102 Isaac Collins, Milwaukee Brewers
103 Brent Rooker, Athletics
104 Jasson Domínguez, New York Yankees
105 Max Muncy, Athletics
106 Spencer Torkelson, Detroit Tigers*
107 Javier Báez, Detroit Tigers
108 George Springer, Toronto Blue Jays
109 Caleb Durbin, Milwaukee Brewers*
110 Cristopher Sánchez, Philadelphia Phillies
111 Robbie Ray, San Francisco Giants*
112 Jhostynxon Garcia, Boston Red Sox RC
113 Cole Ragans, Kansas City Royals
114 Matt Chapman, San Francisco Giants
115 Jack Dreyer, Los Angeles Dodgers*
116 Luke Keaschall, Minnesota Twins
117 Nolan Schanuel, Angels
118 Brandon Sproat, New York Mets RC
119 Brandon Nimmo, Texas Rangers
120 Yu Darvish, San Diego Padres
121 Caden Dana, Angels*
122 Bo Bichette, Toronto Blue Jays*
123 Luis Gil, New York Yankees
124 Daylen Lile, Washington Nationals
125 Ha-Seong Kim, Atlanta Braves
126 Brandon Pfaadt, Arizona Diamondbacks
127 Gavin Sheets, San Diego Padres*
128 Anthony Seigler, Milwaukee Brewers RC
129 Josh Naylor, Seattle Mariners
130 Max Fried, New York Yankees
131 Ryan Mountcastle, Baltimore Orioles
132 Luisangel Acuña, New York Mets
133 Kyle Manzardo, Cleveland Guardians
134 Braxton Ashcraft, Pittsburgh Pirates
135 Jorge Polanco, Seattle Mariners*
136 Jac Caglianone, Kansas City Royals RC
137 Jonah Tong, New York Mets RC
138 Tyler Stephenson, Cincinnati Reds*
139 Steven Kwan, Cleveland Guardians
140 Victor Robles, Seattle Mariners
141 Jared Jones, Pittsburgh Pirates
142 Cole Young, Seattle Mariners RC
143 Manny Machado, San Diego Padres
144 Jacob Misiorowski, Milwaukee Brewers RC
145 Hurston Waldrep, Atlanta Braves*
146 Francisco Lindor, New York Mets
147 Jordan Beck, Colorado Rockies*
148 Bradgley Rodríguez, San Diego Padres RC
149 Luis Rengifo, Angels
150 Nolan McLean, New York Mets RC
151 Ke'Bryan Hayes, Cincinnati Reds
152 Riley Greene, Detroit Tigers
153 Brady House, Washington Nationals RC
154 Carlos Correa, Houston Astros
155 Cole Wilcox, Seattle Mariners RC
156 Willson Contreras, St. Louis Cardinals
157 Kevin Alcántara, Chicago Cubs
158 Max Muncy, Los Angeles Dodgers*
159 Kyle Schwarber, Philadelphia Phillies
160 Bobby Witt Jr., Kansas City Royals
161 Carson Williams, Tampa Bay Rays RC
162 Sonny Gray, Boston Red Sox*
163 Mike Trout, Angels
164 Jackson Jobe, Detroit Tigers
165 Alec Burleson, St. Louis Cardinals
166 Luis Robert Jr., Chicago White Sox
167 Yusei Kikuchi, Angels
168 Jesús Luzardo, Philadelphia Phillies
169 Edward Cabrera, Miami Marlins
170 Hunter Brown, Houston Astros
171 Jung Hoo Lee, San Francisco Giants
172 Jordan Lawlar, Arizona Diamondbacks
173 Bryan Reynolds, Pittsburgh Pirates
174 Robert Suarez, San Diego Padres
175 Samuel Basallo, Baltimore Orioles RC
176 Jesús Sánchez, Houston Astros
177 Angel Martínez, Cleveland Guardians
178 Emmet Sheehan, Los Angeles Dodgers
179 Ezequiel Tovar, Colorado Rockies
180 Adley Rutschman, Baltimore Orioles
181 Ian Seymour, Tampa Bay Rays RC*
182 Kyle Teel, Chicago White Sox RC
183 Trea Turner, Philadelphia Phillies
184 Jordan Westburg, Baltimore Orioles
185 Ronel Blanco, Houston Astros*
186 Zack Gelof, Athletics
187 Kyle Tucker, Chicago Cubs
188 Zach Neto, Angels*
189 Ben Rice, New York Yankees
190 Clayton Kershaw, Los Angeles Dodgers
191 Josh Jung, Texas Rangers*
192 Seth Lugo, Kansas City Royals
193 Matt Strahm, Philadelphia Phillies
194 Matt Olson, Atlanta Braves
195 Sal Frelick, Milwaukee Brewers
196 Jazz Chisholm Jr., New York Yankees
197 Jhonkensy Noel, Cleveland Guardians
198 Lars Nootbaar, St. Louis Cardinals*
199 Carter Jensen, Kansas City Royals RC
200 Simeon Woods Richardson, Minnesota Twins*
201 Keibert Ruiz, Washington Nationals*
202 Shota Imanaga, Chicago Cubs
203 Trey Sweeney, Detroit Tigers
204 Jack Flaherty, Detroit Tigers RC
205 Christian Montes De Oca, Arizona Diamondbacks RC
206 Luis Severino, Athletics
207 David Bednar, New York Yankees
208 Parker Meadows, Detroit Tigers
209 Drake Baldwin, Atlanta Braves
210 Shane Bieber, Toronto Blue Jays
211 Andrew Hoffman, Arizona Diamondbacks RC
212 Chase Burns, Cincinnati Reds RC
213 Starling Marte, New York Mets*
214 William Contreras, Milwaukee Brewers*
215 Ryan O'Hearn, San Diego Padres
216 Geraldo Perdomo, Arizona Diamondbacks*
217 Christian Walker, Houston Astros
218 Jackson Holliday, Baltimore Orioles
219 Yainer Diaz, Houston Astros*
220 Ketel Marte, Arizona Diamondbacks
221 Sal Stewart, Cincinnati Reds RC
222 Cam Schlittler, New York Yankees RC*
223 Daulton Varsho, Toronto Blue Jays
224 Davis Schneider, Toronto Blue Jays
225 Dominic Smith, San Francisco Giants*
226 Ryan Jeffers, Minnesota Twins
227 Jake Mangum, Tampa Bay Rays
228 Connelly Early, Boston Red Sox RC*
229 Kenley Jansen, Angels
230 Thomas Saggese, St. Louis Cardinals
231 Cal Raleigh, Seattle Mariners (Record Breakers)
232 Pete Alonso, New York Mets (Record Breakers)
233 Elly De La Cruz, Cincinnati Reds (Record Breakers)
234 Riley Greene, Detroit Tigers (Record Breakers)
235 Andy Pages, Los Angeles Dodgers
236 JJ Bleday, Athletics
237 Trevor Rogers, Baltimore Orioles*
238 Corbin Burnes, Arizona Diamondbacks
239 Edgar Quero, Chicago White Sox
240 Julio Rodríguez, Seattle Mariners
241 Seiya Suzuki, Chicago Cubs
242 Parker Messick, Cleveland Guardians RC*
243 Gleyber Torres, Detroit Tigers
244 Evan Carter, Texas Rangers
245 Trey Yesavage, Toronto Blue Jays RC
246 Dalton Rushing, Los Angeles Dodgers
247 Moisés Ballesteros, Chicago Cubs
248 Carlos Narváez, Boston Red Sox*
249 Christian Moore, Angels RC
250 Giancarlo Stanton, New York Yankees
251 Joey Cantillo, Cleveland Guardians*
252 Matt McLain, Cincinnati Reds*
253 Byron Buxton, Minnesota Twins
254 Zac Gallen, Arizona Diamondbacks
255 Joe Ryan, Minnesota Twins*
256 Bo Naylor, Cleveland Guardians*
257 Victor Mesa Jr., Miami Marlins
258 Taylor Ward, Baltimore Orioles
259 Miguel Andujar, Cincinnati Reds
260 Dylan Cease, Toronto Blue Jays*
261 Pete Crow-Armstrong, Chicago Cubs
262 Adam Frazier, Kansas City Royals*
263 Justin Martinez, Arizona Diamondbacks
264 Ozzie Albies, Atlanta Braves
265 Bubba Chandler, Pittsburgh Pirates RC
266 Spencer Horwitz, Pittsburgh Pirates
267 Jorge Mateo, Baltimore Orioles*
268 Hyeseong Kim, Los Angeles Dodgers
269 Cal Raleigh, Seattle Mariners
270 Andrew McCutchen, Pittsburgh Pirates
271 Austin Riley, Atlanta Braves
272 Jackson Chourio, Milwaukee Brewers
273 Sean Murphy, Atlanta Braves*
274 Brooks Baldwin, Chicago White Sox
275 Nick Kurtz, Athletics
276 Toronto Blue Jays, Toronto Blue Jays (AL Champions)
277 Los Angeles Dodgers, Los Angeles Dodgers (NL Champions)
278 Chris Sale, Atlanta Braves
279 Jacob Young, Washington Nationals
280 Trevor Larnach, Minnesota Twins*
281 Tarik Skubal, Detroit Tigers
282 Will Smith, Los Angeles Dodgers
283 Jeremy Peña, Houston Astros
284 Cedric Mullins, Tampa Bay Rays
285 Lane Thomas, Cleveland Guardians
286 Randy Arozarena, Seattle Mariners
287 Gunnar Henderson, Baltimore Orioles
288 Eduardo Rodriguez, Arizona Diamondbacks*
289 J.P. Crawford, Seattle Mariners*
290 Shohei Ohtani, Los Angeles Dodgers
291 Freddy Peralta, Milwaukee Brewers
292 Mick Abel, Minnesota Twins
293 Luis Arraez, San Diego Padres*
294 MacKenzie Gore, Washington Nationals*
295 James Wood, Washington Nationals
296 TJ Friedl, Cincinnati Reds
297 Anthony Volpe, New York Yankees
298 Chase Meidroth, Chicago White Sox
299 Matt Shaw, Chicago Cubs
300 Orion Kerkering, Philadelphia Phillies*
301 Josh Smith, Texas Rangers
302 Corey Seager, Texas Rangers
303 Curtis Mead, Chicago White Sox
304 Jack Leiter, Texas Rangers
305 Michael Busch, Chicago Cubs*
306 Juan Soto, New York Mets
307 Ryan Weathers, Miami Marlins
308 Oneil Cruz, Pittsburgh Pirates
309 Andrew Vaughn, Milwaukee Brewers
310 Bryce Eldridge, San Francisco Giants RC
311 Los Angeles Dodgers, Los Angeles Dodgers (World Series Highlights)*
312 Toronto Blue Jays, Toronto Blue Jays (World Series Highlights)*
313 Los Angeles Dodgers, Los Angeles Dodgers (World Series Highlights)*
314 Carlos Estévez, Kansas City Royals
315 Robinson Piña, Toronto Blue Jays RC
316 Merrill Kelly, Texas Rangers*
317 Kodai Senga, New York Mets*
318 Victor Scott II, St. Louis Cardinals
319 Matt Wallner, Minnesota Twins
320 Salvador Perez, Kansas City Royals
321 Kody Clemens, Minnesota Twins
322 Fernando Tatis Jr., San Diego Padres
323 Heriberto Hernández, Miami Marlins RC
324 Denzel Clarke, Athletics
325 Brice Turang, Milwaukee Brewers
326 Carson Kelly, Chicago Cubs*
327 Willy Adames, San Francisco Giants
328 José Caballero, New York Yankees
329 Grant Taylor, Chicago White Sox RC*
330 Cristian Javier, Houston Astros
331 Rhys Hoskins, Milwaukee Brewers
332 Christian Yelich, Milwaukee Brewers
333 Miguel Cabrera, Detroit Tigers (Turn Back The Clock)*
334 Carlos Beltrán, New York Yankees (Turn Back The Clock)*
335 Derek Jeter, New York Yankees (Turn Back The Clock)*
336 Mike Piazza, San Diego Padres (Turn Back The Clock)*
337 Ichiro, Seattle Mariners (Turn Back The Clock)*
338 Colton Cowser, Baltimore Orioles
339 Lenyn Sosa, Chicago White Sox
340 Wyatt Langford, Texas Rangers
341 Alejandro Kirk, Toronto Blue Jays*
342 Michael Harris II, Atlanta Braves
343 Kerry Carpenter, Detroit Tigers*
344 David Hamilton, Boston Red Sox*
345 Otto Lopez, Miami Marlins
346 Hunter Goodman, Colorado Rockies
347 Danny Jansen, Milwaukee Brewers*
348 Shane Baz, Tampa Bay Rays*
349 CJ Abrams, Washington Nationals
350 Freddie Freeman, Los Angeles Dodgers
351 Jackson Merrill, San Diego Padres
352 Gavin Lux, Cincinnati Reds
353 Shane Smith, Chicago White Sox*
354 Joey Loperfido, Toronto Blue Jays
355 Brenton Doyle, Colorado Rockies
356 Marcelo Mayer, Boston Red Sox
357 Harrison Bader, Philadelphia Phillies
358 Masyn Winn, St. Louis Cardinals
359 Aroldis Chapman, Boston Red Sox RC
360 Owen Caissie, Chicago Cubs RC*
361 Gabriel Moreno, Arizona Diamondbacks
362 Wilyer Abreu, Boston Red Sox
363 Nick Castellanos, Philadelphia Phillies
364 C.J. Kayfus, Cleveland Guardians RC
365 Kyle Isbel, Kansas City Royals
366 Marcus Semien, Texas Rangers
367 Kristian Campbell, Boston Red Sox
368 Brayan Rocchio, Cleveland Guardians
369 Brandon Lowe, Tampa Bay Rays
370 Addison Barger, Toronto Blue Jays
371 Yoshinobu Yamamoto, Los Angeles Dodgers
372 Philip Abner/Eduarniel Núñez/Didier Fuentes/Jonathan Pintaro, Arizona Diamondbacks/Athletics/Atlanta Braves/New York Mets RC*
373 Nathan Church/Troy Johnston/Jacob Melton/Carlos Cortes, St. Louis Cardinals/Miami Marlins/Houston Astros/Athletics RC*
374 Cam Devanney/Chad Stevens/Brice Matthews/Ryan Ritter, Pittsburgh Pirates/Angels/Houston Astros/Colorado Rockies RC*
375 Zachary Maxwell/Dylan Smith/Paul Gervase/Jack Perkins, Cincinnati Reds/Detroit Tigers/Los Angeles Dodgers/Athletics RC*
376 Will Banfield/C.J. Stubbs/Jimmy Crooks/Rafael Flores, Cincinnati Reds/Washington Nationals/St. Louis Cardinals/Pittsburgh Pirates RC*
377 Cody Freeman/Otto Kemp/Jeremiah Jackson/Bob Seymour, Texas Rangers/Philadelphia Phillies/Baltimore Orioles/Tampa Bay Rays RC*
378 Andry Lara/Wikelman González/Juan Burgos/Jacob Palisch, Washington Nationals/Chicago White Sox/Arizona Diamondbacks RC*
379 George Valera/Will Robertson/Colby Thomas/Tristin English, Cleveland Guardians/Pittsburgh Pirates/Athletics/Arizona Diamondbacks RC*
380 Junior Caminero, Tampa Bay Rays
381 Ryan McMahon, New York Yankees
382 Bryson Stott, Philadelphia Phillies
383 Corbin Carroll, Arizona Diamondbacks
384 Adolis García, Texas Rangers
385 Carlos Rodón, New York Yankees*
386 Payton Tolle, Boston Red Sox RC
387 Dugan Darnell/Nick Raquet/Troy Melton/Jack Little, Colorado Rockies/St. Louis Cardinals/Detroit Tigers/Los Angeles Dodgers RC*
388 Justin Dean/Tristan Peters/Kenedy Corona/Drew Gilbert, Los Angeles Dodgers/Tampa Bay Rays/Houston Astros/San Francisco Giants RC*
389 Alan Rangel/Elvis Alvarado/Carson Seymour/Joe Rock, Philadelphia Phillies/Athletics/San Francisco Giants/Tampa Bay Rays RC*
390 Denzer Guzman/Maximo Acosta/Alex Freeland/Colson Montgomery, Angels/Miami Marlins/Los Angeles Dodgers/Chicago White Sox RC*
391 Taylor Rashi/Shinnosuke Ogasawara/Luinder Avila/PJ Poulin, Arizona Diamondbacks/Washington Nationals/Kansas City Royals RC*
392 Zach Cole/Jakob Marsee/Yanquiel Fernández/Petey Halpin, Houston Astros/Miami Marlins/Colorado Rockies/Cleveland Guardians RC*
393 Mitch Farris/Andrew Alvarez/Joel Peguero/Kyle Backhus, Angels/Washington Nationals/San Francisco Giants/Arizona Diamondbacks RC*
394 Jack Winkler/Warming Bernabel/Kyle Karros/César Prieto, Miami Marlins/Colorado Rockies/St. Louis Cardinals RC*
395 Kyle Stowers, Miami Marlins*
396 Cade Horton, Chicago Cubs
397 Ceddanne Rafaela, Boston Red Sox
398 Zach McKinstry, Detroit Tigers
399 Jordan Walker, St. Louis Cardinals
400 Mickey Moniak, Colorado Rockies*
"""

ALL_STAR_LOGO_RAW = """
10 Aaron Judge, New York Yankees
17 Jacob Wilson, Athletics
33 Paul Skenes, Pittsburgh Pirates
46 Vladimir Guerrero Jr., Toronto Blue Jays
55 Ronald Acuña Jr., Atlanta Braves
107 Javier Báez, Detroit Tigers
143 Manny Machado, San Diego Padres
146 Francisco Lindor, New York Mets
152 Riley Greene, Detroit Tigers
187 Kyle Tucker, Chicago Cubs
215 Ryan O'Hearn, San Diego Padres
220 Ketel Marte, Arizona Diamondbacks
243 Gleyber Torres, Detroit Tigers
261 Pete Crow-Armstrong, Chicago Cubs
269 Cal Raleigh, Seattle Mariners
281 Tarik Skubal, Detroit Tigers
282 Will Smith, Los Angeles Dodgers
290 Shohei Ohtani, Los Angeles Dodgers
350 Freddie Freeman, Los Angeles Dodgers
380 Junior Caminero, Tampa Bay Rays
"""

IMAGE_VAR_RAW = """
10 Aaron Judge, New York Yankees
11 Jose Altuve, Houston Astros
12 Mookie Betts, Los Angeles Dodgers
18 Eury Pérez, Miami Marlins
33 Paul Skenes, Pittsburgh Pirates
46 Vladimir Guerrero Jr., Toronto Blue Jays
52 José Ramírez, Cleveland Guardians
55 Ronald Acuña Jr., Atlanta Braves
62 Rafael Devers, San Francisco Giants
70 Elly De La Cruz, Cincinnati Reds
72 Bryce Harper, Philadelphia Phillies
86 Roman Anthony, Boston Red Sox
136 Jac Caglianone, Kansas City Royals
137 Jonah Tong, New York Mets
143 Manny Machado, San Diego Padres
144 Jacob Misiorowski, Milwaukee Brewers
146 Francisco Lindor, New York Mets
150 Nolan McLean, New York Mets
159 Kyle Schwarber, Philadelphia Phillies
160 Bobby Witt Jr., Kansas City Royals
163 Mike Trout, Los Angeles Angels
175 Samuel Basallo, Baltimore Orioles
182 Kyle Teel, Chicago White Sox
190 Clayton Kershaw, Los Angeles Dodgers
212 Chase Burns, Cincinnati Reds
240 Julio Rodríguez, Seattle Mariners
250 Giancarlo Stanton, New York Yankees
253 Byron Buxton, Minnesota Twins
261 Pete Crow-Armstrong, Chicago Cubs
265 Bubba Chandler, Pittsburgh Pirates
270 Andrew McCutchen, Pittsburgh Pirates
272 Jackson Chourio, Milwaukee Brewers
275 Nick Kurtz, Athletics
281 Tarik Skubal, Detroit Tigers
286 Randy Arozarena, Seattle Mariners
287 Gunnar Henderson, Baltimore Orioles
290 Shohei Ohtani, Los Angeles Dodgers
295 James Wood, Washington Nationals
302 Corey Seager, Texas Rangers
306 Juan Soto, New York Mets
322 Fernando Tatis Jr., San Diego Padres
332 Christian Yelich, Milwaukee Brewers
340 Wyatt Langford, Texas Rangers
349 CJ Abrams, Washington Nationals
350 Freddie Freeman, Los Angeles Dodgers
358 Masyn Winn, St. Louis Cardinals
371 Yoshinobu Yamamoto, Los Angeles Dodgers
380 Junior Caminero, Tampa Bay Rays
383 Corbin Carroll, Arizona Diamondbacks
396 Cade Horton, Chicago Cubs
"""

ALT_BANNER_RAW = """
13 Agustín Ramírez, Miami Marlins
25 Yordan Alvarez, Houston Astros
39 Roki Sasaki, Los Angeles Dodgers
53 Hunter Greene, Cincinnati Reds
65 Mason Miller, San Diego Padres
98 Jacob deGrom, Texas Rangers
108 George Springer, Toronto Blue Jays
116 Luke Keaschall, Minnesota Twins
130 Max Fried, New York Yankees
152 Riley Greene, Detroit Tigers
153 Brady House, Washington Nationals
161 Carson Williams, Tampa Bay Rays
171 Jung Hoo Lee, San Francisco Giants
183 Trea Turner, Philadelphia Phillies
209 Drake Baldwin, Atlanta Braves
218 Jackson Holliday, Baltimore Orioles
269 Cal Raleigh, Seattle Mariners
291 Freddy Peralta, Milwaukee Brewers
308 Oneil Cruz, Pittsburgh Pirates
396 Cade Horton, Chicago Cubs
"""

NICKNAME_VAR_RAW = """
86 Roman Anthony, Boston Red Sox
129 Josh Naylor, Seattle Mariners
136 Jac Caglianone, Kansas City Royals
137 Jonah Tong, New York Mets
159 Kyle Schwarber, Philadelphia Phillies
160 Bobby Witt Jr., Kansas City Royals
168 Jesús Luzardo, Philadelphia Phillies
261 Pete Crow-Armstrong, Chicago Cubs
269 Cal Raleigh, Seattle Mariners
380 Junior Caminero, Tampa Bay Rays
"""

THROWBACK_JERSEYS_RAW = """
20 Jonathan Aranda, Tampa Bay Rays
58 Chandler Simpson, Tampa Bay Rays
72 Bryce Harper, Philadelphia Phillies
117 Nolan Schanuel, Los Angeles Angels
159 Kyle Schwarber, Philadelphia Phillies
163 Mike Trout, Los Angeles Angels
168 Jesús Luzardo, Philadelphia Phillies
183 Trea Turner, Philadelphia Phillies
188 Zach Neto, Los Angeles Angels
380 Junior Caminero, Tampa Bay Rays
"""

BW_IMAGE_VAR_RAW = """
13 Agustín Ramírez, Miami Marlins
28 Nico Hoerner, Chicago Cubs
29 Eugenio Suárez, Seattle Mariners
31 Andrew Abbott, Cincinnati Reds
36 Edwin Díaz, Los Angeles Dodgers
59 Harry Ford, Seattle Mariners
60 Brooks Lee, Minnesota Twins
73 Dillon Dingler, Detroit Tigers
81 Alec Bohm, Philadelphia Phillies
82 Logan Webb, San Francisco Giants
91 Chase Dollander, Colorado Rockies
98 Jacob deGrom, Texas Rangers
100 Noelvi Marte, Cincinnati Reds
103 Brent Rooker, Athletics
112 Jhostynxon Garcia, Boston Red Sox
124 Daylen Lile, Washington Nationals
133 Kyle Manzardo, Cleveland Guardians
139 Steven Kwan, Cleveland Guardians
154 Carlos Correa, Houston Astros
170 Hunter Brown, Houston Astros
172 Jordan Lawlar, Arizona Diamondbacks
173 Bryan Reynolds, Pittsburgh Pirates
174 Robert Suarez, San Diego Padres
178 Emmet Sheehan, Los Angeles Dodgers
180 Adley Rutschman, Baltimore Orioles
194 Matt Olson, Atlanta Braves
196 Jazz Chisholm Jr., New York Yankees
210 Shane Bieber, Toronto Blue Jays
241 Seiya Suzuki, Chicago Cubs
258 Taylor Ward, Baltimore Orioles
301 Josh Smith, Texas Rangers
310 Bryce Eldridge, San Francisco Giants
314 Carlos Estévez, Kansas City Royals
318 Victor Scott II, St. Louis Cardinals
320 Salvador Perez, Kansas City Royals
323 Heriberto Hernández, Miami Marlins
325 Brice Turang, Milwaukee Brewers
339 Lenyn Sosa, Chicago White Sox
359 Aroldis Chapman, Boston Red Sox
369 Brandon Lowe, Tampa Bay Rays
"""

REAL_ONE_AUTOS_RAW = """
77RO-AD Andre Dawson, Montréal Expos
77RO-DM Dale Murphy, Atlanta Braves
77RO-FL Fred Lynn, Boston Red Sox
77RO-GB George Brett, Kansas City Royals
77RO-GF George Foster, Cincinnati Reds
77RO-JB Johnny Bench, Cincinnati Reds
77RO-JP Jim Palmer, Baltimore Orioles
77RO-JR Jim Rice, Boston Red Sox
77RO-MS Mike Schmidt, Philadelphia Phillies
77RO-RF Rollie Fingers, Oakland Athletics
77RO-RJ Reggie Jackson, New York Yankees
77RO-SC Steve Carlton, Philadelphia Phillies
77RO-WR Willie Randolph, New York Yankees
ROA-AB Addison Barger, Toronto Blue Jays
ROA-AF Alex Freeland, Los Angeles Dodgers
ROA-AJ Aaron Judge, New York Yankees
ROA-AMC Andrew McCutchen, Pittsburgh Pirates
ROA-AR Agustín Ramírez, Miami Marlins
ROA-AV Anthony Volpe, New York Yankees
ROA-BB Bert Blyleven, Texas Rangers
ROA-BBU Byron Buxton, Minnesota Twins
ROA-BC Bubba Chandler, Pittsburgh Pirates
ROA-BD Brendan Donovan, St. Louis Cardinals
ROA-BE Bryce Eldridge, San Francisco Giants
ROA-BM Brice Matthews, Houston Astros
ROA-BR Ben Rice, New York Yankees
ROA-BRO Brent Rooker, Athletics
ROA-BST Bryson Stott, Philadelphia Phillies
ROA-BT Brice Turang, Milwaukee Brewers
ROA-CBU Chase Burns, Cincinnati Reds
ROA-CE Connelly Early, Boston Red Sox
ROA-CF Carlton Fisk, Boston Red Sox
ROA-CJ Carter Jensen, Kansas City Royals
ROA-CJK C.J. Kayfus, Cleveland Guardians
ROA-CME Chase Meidroth, Chicago White Sox
ROA-CMO Christian Moore, Los Angeles Angels
ROA-CMON Colson Montgomery, Chicago White Sox
ROA-CS Chandler Simpson, Tampa Bay Rays
ROA-CSC Cam Schlittler, New York Yankees
ROA-CT Colby Thomas, Athletics
ROA-CW Carson Williams, Tampa Bay Rays
ROA-CWH Carson Whisenhunt, San Francisco Giants
ROA-DBA Drake Baldwin, Atlanta Braves
ROA-DE Dennis Eckersley, Cleveland
ROA-DF Didier Fuentes, Atlanta Braves
ROA-DG Drew Gilbert, San Francisco Giants
ROA-DW Dave Winfield, San Diego Padres
ROA-EQ Edgar Quero, Chicago White Sox
ROA-FJ Fergie Jenkins, Boston Red Sox
ROA-FTJ Fernando Tatis Jr., San Diego Padres
ROA-GC Garrett Crochet, Boston Red Sox
ROA-GH Gunnar Henderson, Baltimore Orioles
ROA-GT Grant Taylor, Chicago White Sox
ROA-GV George Valera, Cleveland Guardians
ROA-HF Harry Ford, Seattle Mariners
ROA-HH Heriberto Hernández, Miami Marlins
ROA-HK Hyeseong Kim, Los Angeles Dodgers
ROA-IS Ian Seymour, Tampa Bay Rays
ROA-JA Jose Altuve, Houston Astros
ROA-JCA Junior Caminero, Tampa Bay Rays
ROA-JCAG Jac Caglianone, Kansas City Royals
ROA-JCJ Jazz Chisholm Jr., New York Yankees
ROA-JH Jackson Holliday, Baltimore Orioles
ROA-JHG Jhostynxon Garcia, Boston Red Sox
ROA-JK Jim Kaat, Philadelphia Phillies
ROA-JM Jacob Misiorowski, Milwaukee Brewers
ROA-JMA Jakob Marsee, Miami Marlins
ROA-JME Jacob Melton, Houston Astros
ROA-JP Jack Perkins, Athletics
ROA-JTO Jonah Tong, New York Mets
ROA-JTR J.T. Realmuto, Philadelphia Phillies
ROA-JWI Jacob Wilson, Athletics
ROA-KC Kerry Carpenter, Detroit Tigers
ROA-KCA Kristian Campbell, Boston Red Sox
ROA-KGS Ken Griffey, Cincinnati Reds
ROA-KK Kyle Karros, Colorado Rockies
ROA-KT Kyle Teel, Chicago White Sox
ROA-LP Lou Piniella, New York Yankees
ROA-MA Maximo Acosta, Miami Marlins
ROA-MH Michael Harris II, Atlanta Braves
ROA-MM Mason Miller, San Diego Padres
ROA-MSH Matt Shaw, Chicago Cubs
ROA-MT Mike Trout, Los Angeles Angels
ROA-NH Nico Hoerner, Chicago Cubs
ROA-NK Nick Kurtz, Athletics
ROA-NM Noelvi Marte, Cincinnati Reds
ROA-NMC Nolan McLean, New York Mets
ROA-OC Owen Caissie, Chicago Cubs
ROA-OK Otto Kemp, Philadelphia Phillies
ROA-PS Paul Skenes, Pittsburgh Pirates
ROA-PT Payton Tolle, Boston Red Sox
ROA-RAN Roman Anthony, Boston Red Sox
ROA-RC Rod Carew, Minnesota Twins
ROA-RE Rawly Eastwick, Cincinnati Reds
ROA-RG Ron Guidry, New York Yankees
ROA-RGO Rich Gossage, Chicago White Sox
ROA-RH Robert Hassell III, Washington Nationals
ROA-RL Royce Lewis, Minnesota Twins
ROA-RR Ryan Ritter, Colorado Rockies
ROA-RS Roki Sasaki, Los Angeles Dodgers
ROA-RY Robin Yount, Milwaukee Brewers
ROA-SBA Samuel Basallo, Baltimore Orioles
ROA-SF Sal Frelick, Milwaukee Brewers
ROA-SG Steve Garvey, Los Angeles Dodgers
ROA-SK Steven Kwan, Cleveland Guardians
ROA-SO Shohei Ohtani, Los Angeles Dodgers
ROA-SST Sal Stewart, Cincinnati Reds
ROA-TJ Troy Johnston, Miami Marlins
ROA-TP Tony Perez, Cincinnati Reds
ROA-VGJ Vladimir Guerrero Jr., Toronto Blue Jays
ROA-WB Warming Bernabel, Colorado Rockies
ROA-WS Will Smith, Los Angeles Dodgers
ROA-YF Yanquiel Fernández, Colorado Rockies
ROA-YY Yoshinobu Yamamoto, Los Angeles Dodgers
"""

REAL_ONE_DUAL_RAW = """
RODA-BC Jac Caglianone/George Brett, Kansas City Royals
RODA-CF George Foster/Rod Carew, Cincinnati Reds/Minnesota Twins
RODA-LA Roman Anthony/Fred Lynn, Boston Red Sox
RODA-RS Paul Skenes/Nolan Ryan, Pittsburgh Pirates/California Angels
"""

REAL_ONE_QUAD_RAW = """
ROQA-BWCW Jac Caglianone/Frank White/George Brett/Bobby Witt Jr., Kansas City Royals
ROQA-FYRL Fred Lynn/Jim Rice/Carl Yastrzemski/Carlton Fisk, Boston Red Sox
ROQA-YYCM Jacob Misiorowski/Jackson Chourio/Christian Yelich/Robin Yount, Milwaukee Brewers
"""

EXPANSION_AUTOS_RAW = """
EA-AW Al Woods, Toronto Blue Jays
EA-DL Dave Lemanczyk, Toronto Blue Jays
EA-DR Doug Rader, Toronto Blue Jays
EA-GA Glenn Abbott, Seattle Mariners
EA-GW Gary Wheelock, Seattle Mariners
EA-OV Otto Vélez, Toronto Blue Jays
EA-RH Roy Howell, Toronto Blue Jays
EA-SB Steve Braun, Seattle Mariners
"""

TBTC_AUTOS_RAW = """
TBA-AP Albert Pujols, St. Louis Cardinals
TBA-BB Barry Bonds, San Francisco Giants
TBA-DJ Derek Jeter, New York Yankees
TBA-FH Félix Hernández, Seattle Mariners
TBA-I Ichiro, Seattle Mariners
TBA-MP Mike Piazza, San Diego Padres
TBA-SO Shohei Ohtani, Angels
"""

CHROME_AUTOS_RAW = """
ROAC-BC Bubba Chandler, Pittsburgh Pirates
ROAC-BE Bryce Eldridge, San Francisco Giants
ROAC-CB Chase Burns, Cincinnati Reds
ROAC-CMO Colson Montgomery, Chicago White Sox
ROAC-FTJ Fernando Tatis Jr., San Diego Padres
ROAC-JCA Jac Caglianone, Kansas City Royals
ROAC-JM Jacob Misiorowski, Milwaukee Brewers
ROAC-MT Mike Trout, Los Angeles Angels
ROAC-NK Nick Kurtz, Athletics
ROAC-NM Nolan McLean, New York Mets
ROAC-PS Paul Skenes, Pittsburgh Pirates
ROAC-RA Roman Anthony, Boston Red Sox
ROAC-SO Shohei Ohtani, Los Angeles Dodgers
"""

CC_AUTO_RELICS_RAW = """
CCAR-BB Byron Buxton, Minnesota Twins
CCAR-CH Cade Horton, Chicago Cubs
CCAR-CJA CJ Abrams, Washington Nationals
CCAR-CY Christian Yelich, Milwaukee Brewers
CCAR-FTJ Fernando Tatis Jr., San Diego Padres
CCAR-GB George Brett, Kansas City Royals
CCAR-GH Gunnar Henderson, Baltimore Orioles
CCAR-JA Jose Altuve, Houston Astros
CCAR-JB Johnny Bench, Cincinnati Reds
CCAR-JCA Jac Caglianone, Kansas City Royals
CCAR-JCJ Jazz Chisholm Jr., New York Yankees
CCAR-JW Jacob Wilson, Athletics
CCAR-KTE Kyle Teel, Chicago White Sox
CCAR-MS Mike Schmidt, Philadelphia Phillies
CCAR-MT Mike Trout, Los Angeles Angels
CCAR-NA Nolan Arenado, St. Louis Cardinals
CCAR-PS Paul Skenes, Pittsburgh Pirates
CCAR-RC Rod Carew, Minnesota Twins
CCAR-RJ Reggie Jackson, New York Yankees
CCAR-RS Roki Sasaki, Los Angeles Dodgers
CCAR-SC Steve Carlton, Philadelphia Phillies
CCAR-TT Trea Turner, Philadelphia Phillies
CCAR-VGJ Vladimir Guerrero Jr., Toronto Blue Jays
"""

CC_DUAL_AUTO_RELICS_RAW = """
CCDR-JJ Aaron Judge/Reggie Jackson, New York Yankees
CCDR-YC Jackson Chourio/Robin Yount, Milwaukee Brewers
"""

FLASHBACKS_AUTO_RELICS_RAW = """
FAR-CY Carl Yastrzemski, Boston Red Sox
FAR-GB George Brett, Kansas City Royals
FAR-MS Mike Schmidt, Philadelphia Phillies
FAR-RJ Reggie Jackson, New York Yankees
FAR-RY Robin Yount, Milwaukee Brewers
FAR-SC Steve Carlton, Philadelphia Phillies
"""

THERE_ONCE_AUTO_RELICS_RAW = """
TMA-CF Carlton Fisk, Boston Red Sox
TMA-GB George Brett, Kansas City Royals
TMA-MS Mike Schmidt, Philadelphia Phillies
TMA-RJ Reggie Jackson, Oakland Athletics
TMA-RY Robin Yount, Milwaukee Brewers
TMA-SC Steve Carlton, Philadelphia Phillies
"""

CC_RELICS_RAW = """
CCR-AA Andrew Abbott, Cincinnati Reds
CCR-AB Alex Bregman, Boston Red Sox
CCR-AG Adolis García, Texas Rangers
CCR-AJ Aaron Judge, New York Yankees
CCR-AM Andrew McCutchen, Pittsburgh Pirates
CCR-AR Agustín Ramírez, Miami Marlins
CCR-ARI Austin Riley, Atlanta Braves
CCR-ARU Adley Rutschman, Baltimore Orioles
CCR-BB Bo Bichette, Toronto Blue Jays
CCR-BBU Byron Buxton, Minnesota Twins
CCR-BH Bryce Harper, Philadelphia Phillies
CCR-BL Brooks Lee, Minnesota Twins
CCR-BLO Brandon Lowe, Tampa Bay Rays
CCR-BN Brandon Nimmo, New York Mets
CCR-BR Ben Rice, New York Yankees
CCR-BW Bryan Woo, Seattle Mariners
CCR-BWI Bobby Witt Jr., Kansas City Royals
CCR-CA CJ Abrams, Washington Nationals
CCR-CB Cody Bellinger, New York Yankees
CCR-CC Carlos Correa, Houston Astros
CCR-CCA Corbin Carroll, Arizona Diamondbacks
CCR-CH Cade Horton, Chicago Cubs
CCR-CM Colson Montgomery, Chicago White Sox
CCR-CR Cal Raleigh, Seattle Mariners
CCR-CSE Corey Seager, Texas Rangers
CCR-CY Christian Yelich, Milwaukee Brewers
CCR-DB Drake Baldwin, Atlanta Braves
CCR-DC Dylan Crews, Washington Nationals
CCR-DCE Dylan Cease, San Diego Padres
CCR-EP Eury Pérez, Miami Marlins
CCR-ET Ezequiel Tovar, Colorado Rockies
CCR-FF Freddie Freeman, Los Angeles Dodgers
CCR-FL Francisco Lindor, New York Mets
CCR-FT Fernando Tatis Jr., San Diego Padres
CCR-GC Garrett Crochet, Boston Red Sox
CCR-GH Gunnar Henderson, Baltimore Orioles
CCR-GS George Springer, Toronto Blue Jays
CCR-HG Hunter Goodman, Colorado Rockies
CCR-JA Jose Altuve, Houston Astros
CCR-JB Jordan Beck, Colorado Rockies
CCR-JC Junior Caminero, Tampa Bay Rays
CCR-JCA Jac Caglianone, Kansas City Royals
CCR-JCH Jackson Chourio, Milwaukee Brewers
CCR-JCJ Jazz Chisholm Jr., New York Yankees
CCR-JD Jarren Duran, Boston Red Sox
CCR-JH Jackson Holliday, Baltimore Orioles
CCR-JL Jung Hoo Lee, San Francisco Giants
CCR-JLA Jordan Lawlar, Arizona Diamondbacks
CCR-JM Jeff McNeil, New York Mets
CCR-JME Jackson Merrill, San Diego Padres
CCR-JP Jeremy Peña, Houston Astros
CCR-JR Julio Rodríguez, Seattle Mariners
CCR-JRA José Ramírez, Cleveland Guardians
CCR-JRE J.T. Realmuto, Philadelphia Phillies
CCR-JS Juan Soto, New York Mets
CCR-JW James Wood, Washington Nationals
CCR-JWI Jacob Wilson, Athletics
CCR-KM Ketel Marte, Arizona Diamondbacks
CCR-KS Kyle Schwarber, Philadelphia Phillies
CCR-LA Luis Arraez, San Diego Padres
CCR-LB Lawrence Butler, Athletics
CCR-LR Luis Robert Jr., Chicago White Sox
CCR-MB Mookie Betts, Los Angeles Dodgers
CCR-MC Matt Chapman, San Francisco Giants
CCR-MM Manny Machado, San Diego Padres
CCR-MO Matt Olson, Atlanta Braves
CCR-MS Marcus Semien, Texas Rangers
CCR-MSH Matt Shaw, Chicago Cubs
CCR-MT Mike Trout, Los Angeles Angels
CCR-MW Masyn Winn, St. Louis Cardinals
CCR-NA Nolan Arenado, St. Louis Cardinals
CCR-NC Nick Castellanos, Philadelphia Phillies
CCR-NE Nathan Eovaldi, Texas Rangers
CCR-NK Nick Kurtz, Athletics
CCR-OA Ozzie Albies, Atlanta Braves
CCR-OC Oneil Cruz, Pittsburgh Pirates
CCR-PA Pete Alonso, New York Mets
CCR-PC Pete Crow-Armstrong, Chicago Cubs
CCR-PG Paul Goldschmidt, New York Yankees
CCR-PL Pablo López, Minnesota Twins
CCR-PS Paul Skenes, Pittsburgh Pirates
CCR-RA Ronald Acuña Jr., Atlanta Braves
CCR-RAR Randy Arozarena, Seattle Mariners
CCR-RG Riley Greene, Detroit Tigers
CCR-RL Royce Lewis, Minnesota Twins
CCR-SF Sal Frelick, Milwaukee Brewers
CCR-SP Salvador Perez, Kansas City Royals
CCR-SS Seiya Suzuki, Chicago Cubs
CCR-ST Spencer Torkelson, Detroit Tigers
CCR-TS Tarik Skubal, Detroit Tigers
CCR-TSO Tyler Soderstrom, Athletics
CCR-TT Trea Turner, Philadelphia Phillies
CCR-VG Vladimir Guerrero Jr., Toronto Blue Jays
CCR-WA Willy Adames, San Francisco Giants
CCR-WC William Contreras, Milwaukee Brewers
CCR-WS Will Smith, Los Angeles Dodgers
CCR-YA Yordan Alvarez, Houston Astros
CCR-ZN Zach Neto, Los Angeles Angels
"""

REAL_ONE_RELICS_RAW = """
ROR-AJ Aaron Judge, New York Yankees
ROR-AM Andrew McCutchen, Pittsburgh Pirates
ROR-BB Bo Bichette, Toronto Blue Jays
ROR-BBU Byron Buxton, Minnesota Twins
ROR-BH Bryce Harper, Philadelphia Phillies
ROR-BS Bryson Stott, Philadelphia Phillies
ROR-BW Bobby Witt Jr., Kansas City Royals
ROR-CC Corbin Carroll, Arizona Diamondbacks
ROR-CK Clayton Kershaw, Los Angeles Dodgers
ROR-CR Cal Raleigh, Seattle Mariners
ROR-CS Chris Sale, Atlanta Braves
ROR-DB Drake Baldwin, Atlanta Braves
ROR-FL Francisco Lindor, New York Mets
ROR-FT Fernando Tatis Jr., San Diego Padres
ROR-GC Garrett Crochet, Boston Red Sox
ROR-HG Hunter Greene, Cincinnati Reds
ROR-IH Ian Happ, Chicago Cubs
ROR-JA Jose Altuve, Houston Astros
ROR-JC Junior Caminero, Tampa Bay Rays
ROR-JCH Jackson Chourio, Milwaukee Brewers
ROR-JCJ Jazz Chisholm Jr., New York Yankees
ROR-JH Jackson Holliday, Baltimore Orioles
ROR-JM Jackson Merrill, San Diego Padres
ROR-JR José Ramírez, Cleveland Guardians
ROR-JRO Julio Rodríguez, Seattle Mariners
ROR-JS Juan Soto, New York Mets
ROR-JW James Wood, Washington Nationals
ROR-JWI Jacob Wilson, Athletics
ROR-KM Ketel Marte, Arizona Diamondbacks
ROR-LA Luis Arraez, San Diego Padres
ROR-LK Luke Keaschall, Minnesota Twins
ROR-MB Mookie Betts, Los Angeles Dodgers
ROR-MF Max Fried, New York Yankees
ROR-MO Matt Olson, Atlanta Braves
ROR-MS Matt Shaw, Chicago Cubs
ROR-MT Mike Trout, Los Angeles Angels
ROR-MW Masyn Winn, St. Louis Cardinals
ROR-NA Nolan Arenado, St. Louis Cardinals
ROR-OA Ozzie Albies, Atlanta Braves
ROR-OC Oneil Cruz, Pittsburgh Pirates
ROR-PA Pete Alonso, New York Mets
ROR-PC Pete Crow-Armstrong, Chicago Cubs
ROR-RA Ronald Acuña Jr., Atlanta Braves
ROR-RL Royce Lewis, Minnesota Twins
ROR-TS Tarik Skubal, Detroit Tigers
ROR-TT Trea Turner, Philadelphia Phillies
ROR-VG Vladimir Guerrero Jr., Toronto Blue Jays
ROR-WS Will Smith, Los Angeles Dodgers
ROR-YY Yoshinobu Yamamoto, Los Angeles Dodgers
ROR-ZN Zach Neto, Los Angeles Angels
"""

FLASHBACK_RELICS_RAW = """
FBR-AD Andre Dawson, Montréal Expos
FBR-CY Carl Yastrzemski, Boston Red Sox
FBR-DW Dave Winfield, San Diego Padres
FBR-GB George Brett, Kansas City Royals
FBR-GF George Foster, Cincinnati Reds
FBR-JR Jim Rice, Boston Red Sox
FBR-KG Ken Griffey, Cincinnati Reds
FBR-KH Keith Hernandez, St. Louis Cardinals
FBR-MS Mike Schmidt, Philadelphia Phillies
FBR-RC Rod Carew, Minnesota Twins
FBR-RJ Reggie Jackson, New York Yankees
FBR-RY Robin Yount, Milwaukee Brewers
FBR-SC Steve Carlton, Philadelphia Phillies
FBR-SG Steve Garvey, Los Angeles Dodgers
FBR-TP Tony Perez, Montréal Expos
FBR-TS Ted Simmons, St. Louis Cardinals
"""

CC_DUAL_RELICS_RAW = """
CCDR-BW George Brett/Bobby Witt Jr., Kansas City Royals
CCDR-CB Rod Carew/Byron Buxton, Minnesota Twins
CCDR-CW Zack Wheeler/Steve Carlton, Philadelphia Phillies
CCDR-DW Andre Dawson/James Wood, Washington Nationals
CCDR-GS Steve Garvey/Will Smith, Los Angeles Dodgers
CCDR-HA Keith Hernandez/Nolan Arenado, St. Louis Cardinals
CCDR-JJ Aaron Judge/Reggie Jackson, New York Yankees
CCDR-LA Roman Anthony/Fred Lynn, Boston Red Sox
CCDR-MO Dale Murphy/Matt Olson, Atlanta Braves
CCDR-RR Ceddanne Rafaela/Jim Rice, Boston Red Sox
CCDR-SH Mike Schmidt/Bryce Harper, Philadelphia Phillies
CCDR-TA Joe Torre/Pete Alonso, New York Mets
CCDR-WT Dave Winfield/Fernando Tatis Jr., San Diego Padres
CCDR-YB Alex Bregman/Carl Yastrzemski, Boston Red Sox
CCDR-YY Robin Yount/Christian Yelich, Milwaukee Brewers
"""

CC_QUAD_RELICS_RAW = """
CCQR-BWPC George Brett/Salvador Perez/Jac Caglianone/Bobby Witt Jr., Kansas City Royals
CCQR-DWCH Andre Dawson/Dylan Crews/James Wood/Brady House, Washington Nationals
CCQR-JJSB Giancarlo Stanton/Cody Bellinger/Aaron Judge/Reggie Jackson, New York Yankees
CCQR-RLAM Marcelo Mayer/Jim Rice/Fred Lynn/Roman Anthony, Boston Red Sox
CCQR-SHCW Bryce Harper/Mike Schmidt/Steve Carlton/Zack Wheeler, Philadelphia Phillies
"""

READY_AND_ACTION_RAW = """
RA-AJ Aaron Judge, New York Yankees
RA-BC Bubba Chandler, Pittsburgh Pirates
RA-BH Bryce Harper, Philadelphia Phillies
RA-BW Bobby Witt Jr., Kansas City Royals
RA-CY Carl Yastrzemski, Boston Red Sox
RA-DP Dave Parker, Pittsburgh Pirates
RA-ED Elly De La Cruz, Cincinnati Reds
RA-FL Francisco Lindor, New York Mets
RA-GB George Brett, Kansas City Royals
RA-GF George Foster, Cincinnati Reds
RA-GH Gunnar Henderson, Baltimore Orioles
RA-JB Johnny Bench, Cincinnati Reds
RA-KT Kyle Teel, Chicago White Sox
RA-MM Manny Machado, San Diego Padres
RA-MS Mike Schmidt, Philadelphia Phillies
RA-MT Mike Trout, Los Angeles Angels
RA-NM Nolan McLean, New York Mets
RA-NR Nolan Ryan, California Angels
RA-OC Owen Caissie, Chicago Cubs
RA-PC Pete Crow-Armstrong, Chicago Cubs
RA-RC Rod Carew, Minnesota Twins
RA-RJ Reggie Jackson, New York Yankees
RA-SB Samuel Basallo, Baltimore Orioles
RA-SO Shohei Ohtani, Los Angeles Dodgers
RA-WM Willie McCovey, San Francisco Giants
"""

THE_ENTERPRISE_RAW = """
TE-BB Bo Bichette, Toronto Blue Jays
TE-BBU Byron Buxton, Minnesota Twins
TE-BH Brady House, Washington Nationals
TE-CB Chase Burns, Cincinnati Reds
TE-CK C.J. Kayfus, Cleveland Guardians
TE-CM Colson Montgomery, Chicago White Sox
TE-CMO Christian Moore, Los Angeles Angels
TE-EP Eury Pérez, Miami Marlins
TE-ET Ezequiel Tovar, Colorado Rockies
TE-FL Francisco Lindor, New York Mets
TE-JC Junior Caminero, Tampa Bay Rays
TE-JCA Jac Caglianone, Kansas City Royals
TE-JCJ Jazz Chisholm Jr., New York Yankees
TE-JH Jackson Holliday, Baltimore Orioles
TE-JM Jackson Merrill, San Diego Padres
TE-JMI Jacob Misiorowski, Milwaukee Brewers
TE-JR Julio Rodríguez, Seattle Mariners
TE-JW Jacob Wilson, Athletics
TE-KM Ketel Marte, Arizona Diamondbacks
TE-MB Mookie Betts, Los Angeles Dodgers
TE-MC Matt Chapman, San Francisco Giants
TE-MW Masyn Winn, St. Louis Cardinals
TE-PC Pete Crow-Armstrong, Chicago Cubs
TE-PS Paul Skenes, Pittsburgh Pirates
TE-RA Roman Anthony, Boston Red Sox
TE-RAJ Ronald Acuña Jr., Atlanta Braves
TE-RG Riley Greene, Detroit Tigers
TE-TT Trea Turner, Philadelphia Phillies
TE-WL Wyatt Langford, Texas Rangers
TE-YA Yordan Alvarez, Houston Astros
"""

RAW_POWER_RAW = """
RP-AJ Aaron Judge, New York Yankees
RP-CR Cal Raleigh, Seattle Mariners
RP-JC Jac Caglianone, Kansas City Royals
RP-JCA Junior Caminero, Tampa Bay Rays
RP-JW James Wood, Washington Nationals
RP-KS Kyle Schwarber, Philadelphia Phillies
RP-NK Nick Kurtz, Athletics
RP-PA Pete Alonso, New York Mets
RP-RA Roman Anthony, Boston Red Sox
RP-SO Shohei Ohtani, Los Angeles Dodgers
"""

# ─────────────────────────────────────────────────────────────
# Section builders
# ─────────────────────────────────────────────────────────────

def parse_cards_from_raw(raw, parser_fn):
    """Apply parser_fn to each non-empty, non-skip line."""
    cards = []
    for line in raw.strip().splitlines():
        line = line.strip()
        if line and not should_skip(line):
            cards.extend(parser_fn(line))
    return cards


def make_section(name, parallels, cards):
    return {"insert_set": name, "parallels": parallels, "cards": cards}


def build_sections():
    sections = []

    # Base Set
    base_cards = parse_cards_from_raw(BASE_SET_RAW, parse_base_line)
    sections.append(make_section("Base Set", BASE_PARALLELS, base_cards))

    # Base Chrome — same cards, Chrome parallels
    sections.append(make_section("Base Chrome", CHROME_PARALLELS, base_cards))

    # Variation sets (no parallels, standard card line parser)
    variations = [
        ("All-Star Logo Variations",         ALL_STAR_LOGO_RAW),
        ("Image Variations",                 IMAGE_VAR_RAW),
        ("Alternate Banner Variations",      ALT_BANNER_RAW),
        ("Nickname Variations",              NICKNAME_VAR_RAW),
        ("Throwback Jerseys Variations",     THROWBACK_JERSEYS_RAW),
        ("Black and White Image Variations", BW_IMAGE_VAR_RAW),
    ]
    for name, raw in variations:
        cards = parse_cards_from_raw(raw, parse_standard_line)
        sections.append(make_section(name, [], cards))

    # Autograph sets
    sections.append(make_section(
        "Real One Autographs", PARALLELS_RED_INK,
        parse_cards_from_raw(REAL_ONE_AUTOS_RAW, parse_standard_line)
    ))
    sections.append(make_section(
        "Real One Dual Autographs", [],
        parse_cards_from_raw(REAL_ONE_DUAL_RAW, parse_multi_player_line)
    ))
    sections.append(make_section(
        "Real One Quad Autographs", [],
        parse_cards_from_raw(REAL_ONE_QUAD_RAW, parse_multi_player_line)
    ))
    sections.append(make_section(
        "Expansion Autographs", PARALLELS_RED_INK,
        parse_cards_from_raw(EXPANSION_AUTOS_RAW, parse_standard_line)
    ))
    sections.append(make_section(
        "Turn Back The Clock Autographs", [],
        parse_cards_from_raw(TBTC_AUTOS_RAW, parse_standard_line)
    ))
    sections.append(make_section(
        "Base Chrome Autographs", PARALLELS_CHROME_AUTO,
        parse_cards_from_raw(CHROME_AUTOS_RAW, parse_standard_line)
    ))
    sections.append(make_section(
        "Clubhouse Collection Autographed Relics", PARALLELS_PATCH,
        parse_cards_from_raw(CC_AUTO_RELICS_RAW, parse_standard_line)
    ))
    sections.append(make_section(
        "Clubhouse Collection Dual Autographed Relics", PARALLELS_PATCH,
        parse_cards_from_raw(CC_DUAL_AUTO_RELICS_RAW, parse_multi_player_line)
    ))
    sections.append(make_section(
        "Flashbacks Autographed Relics", PARALLELS_PATCH,
        parse_cards_from_raw(FLASHBACKS_AUTO_RELICS_RAW, parse_standard_line)
    ))
    sections.append(make_section(
        "There Once Was A Man Autographed Relics", PARALLELS_PATCH,
        parse_cards_from_raw(THERE_ONCE_AUTO_RELICS_RAW, parse_standard_line)
    ))

    # Memorabilia sets
    sections.append(make_section(
        "Clubhouse Collection Relics", PARALLELS_RED_PATCH,
        parse_cards_from_raw(CC_RELICS_RAW, parse_standard_line)
    ))
    sections.append(make_section(
        "Real One Relics", PARALLELS_RED_PATCH,
        parse_cards_from_raw(REAL_ONE_RELICS_RAW, parse_standard_line)
    ))
    sections.append(make_section(
        "Flashback Relics", PARALLELS_PATCH,
        parse_cards_from_raw(FLASHBACK_RELICS_RAW, parse_standard_line)
    ))
    sections.append(make_section(
        "Clubhouse Collection Dual Player Relics", PARALLELS_PATCH,
        parse_cards_from_raw(CC_DUAL_RELICS_RAW, parse_multi_player_line)
    ))
    sections.append(make_section(
        "Clubhouse Collection Quad Player Relics", PARALLELS_PATCH,
        parse_cards_from_raw(CC_QUAD_RELICS_RAW, parse_multi_player_line)
    ))

    # Insert sets (no parallels)
    sections.append(make_section(
        "Ready And Action", [],
        parse_cards_from_raw(READY_AND_ACTION_RAW, parse_standard_line)
    ))
    sections.append(make_section(
        "The Enterprise", [],
        parse_cards_from_raw(THE_ENTERPRISE_RAW, parse_standard_line)
    ))
    sections.append(make_section(
        "Raw Power", [],
        parse_cards_from_raw(RAW_POWER_RAW, parse_standard_line)
    ))

    return sections


# ─────────────────────────────────────────────────────────────
# Stats
# ─────────────────────────────────────────────────────────────

def compute_stats(appearances):
    unique_cards  = 0
    total_print_run = 0
    one_of_ones   = 0
    for app in appearances:
        unique_cards += 1
        for p in app["parallels"]:
            unique_cards += 1
            if p["print_run"] and p["print_run"] > 0:
                total_print_run += p["print_run"]
                if p["print_run"] == 1:
                    one_of_ones += 1
    return {
        "unique_cards":    unique_cards,
        "total_print_run": total_print_run,
        "one_of_ones":     one_of_ones,
        "insert_sets":     len(appearances),
    }


# ─────────────────────────────────────────────────────────────
# Build output
# ─────────────────────────────────────────────────────────────

def build_output(sections):
    # Collect rookies (propagate is_rookie to all appearances)
    rc_players = set()
    for section in sections:
        for card in section["cards"]:
            if card.get("is_rookie"):
                rc_players.add(card["player"])

    player_index = {}
    for section in sections:
        for card in section["cards"]:
            pname = card["player"]
            if pname not in player_index:
                player_index[pname] = {"player": pname, "appearances": []}
            player_index[pname]["appearances"].append({
                "insert_set":  section["insert_set"],
                "card_number": card["card_number"],
                "team":        card["team"],
                "is_rookie":   pname in rc_players,
                "subset_tag":  card["subset"],
                "parallels":   section["parallels"],
            })

    players = []
    for pname in sorted(player_index.keys()):
        data = player_index[pname]
        players.append({
            "player":      pname,
            "appearances": data["appearances"],
            "stats":       compute_stats(data["appearances"]),
        })

    return {
        "set_name": "2026 Topps Heritage Baseball",
        "sport":    "Baseball",
        "season":   "2026",
        "league":   "MLB",
        "sections": sections,
        "players":  players,
    }


# ─────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Parsing 2026 Topps Heritage Baseball...")

    sections = build_sections()
    output   = build_output(sections)

    out_path = "topps_heritage_2026_parsed.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nSet: {output['set_name']} ({output['season']})")
    print(f"Sections: {len(output['sections'])}")
    for s in output["sections"]:
        print(f"  {s['insert_set']:<52} {len(s['cards']):>4} cards  {len(s['parallels']):>2} parallels")

    print(f"\nTotal unique players: {len(output['players'])}")

    player_map = {p["player"]: p for p in output["players"]}

    print("\n=== Spot checks ===")
    for name in ["Aaron Judge", "Paul Skenes", "Shohei Ohtani", "George Brett"]:
        if name in player_map:
            st = player_map[name]["stats"]
            print(f"  {name}: {st['insert_sets']} insert sets, "
                  f"{st['unique_cards']} unique cards, "
                  f"{st['total_print_run']} total print run, "
                  f"{st['one_of_ones']} 1/1s")

    print("\n=== League Leaders cards 1–8 ===")
    base = next(s for s in sections if s["insert_set"] == "Base Set")
    for cn in [str(i) for i in range(1, 9)]:
        players_on_card = [c["player"] for c in base["cards"] if c["card_number"] == cn]
        print(f"  Card {cn}: {players_on_card}")

    print("\n=== Rookie Combo sample (card 372) ===")
    rc372 = [c for c in base["cards"] if c["card_number"] == "372"]
    for c in rc372:
        print(f"  {c['player']} ({c['team']}) rc={c['is_rookie']} subset={c['subset']}")

    print("\n=== Record Breakers (231-234) ===")
    for cn in ["231", "232", "233", "234"]:
        cards = [c for c in base["cards"] if c["card_number"] == cn]
        for c in cards:
            print(f"  {cn}: {c['player']} subset={c['subset']}")

    print("\n=== Turn Back The Clock (333-337) ===")
    for cn in ["333", "334", "335", "336", "337"]:
        cards = [c for c in base["cards"] if c["card_number"] == cn]
        for c in cards:
            print(f"  {cn}: {c['player']} subset={c['subset']}")

    print("\n=== Team Cards ===")
    for cn in ["276", "277", "311", "312", "313"]:
        cards = [c for c in base["cards"] if c["card_number"] == cn]
        for c in cards:
            print(f"  {cn}: player={c['player']} team={c['team']}")

    print("\n=== Real One Dual Autographs ===")
    roda = next(s for s in sections if s["insert_set"] == "Real One Dual Autographs")
    for c in roda["cards"]:
        print(f"  {c['card_number']}: {c['player']} ({c['team']})")
