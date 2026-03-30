#!/usr/bin/env python3
"""Parser for 2022 Panini Select UFC — base set (400 cards, 4 tiers)."""

import json
import re

# ─────────────────────────────────────────────────────────────
# Rookies
# ─────────────────────────────────────────────────────────────

RC_FIGHTERS = {
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

# ─────────────────────────────────────────────────────────────
# Parallels per base tier
# ─────────────────────────────────────────────────────────────

PARALLELS_CONCOURSE = [
    {"name": "Blue",            "print_run": None},
    {"name": "Disco",           "print_run": None},
    {"name": "Elephant",        "print_run": None},
    {"name": "Green & Purple",  "print_run": None},
    {"name": "Orange Flash",    "print_run": None},
    {"name": "Scope",           "print_run": None},
    {"name": "Silver",          "print_run": None},
    {"name": "Tiger",           "print_run": None},
    {"name": "Tri-Color",       "print_run": None},
    {"name": "Zebra",           "print_run": None},
    {"name": "Light Blue",      "print_run": 199},
    {"name": "Red",             "print_run": 99},
    {"name": "Red Disco",       "print_run": 99},
    {"name": "White",           "print_run": 75},
    {"name": "Blue Disco",      "print_run": 49},
    {"name": "Neon Green",      "print_run": 49},
    {"name": "Teal & Pink",     "print_run": 49},
    {"name": "Tie-Dye",         "print_run": 25},
    {"name": "Gold",            "print_run": 10},
    {"name": "Gold Disco",      "print_run": 10},
    {"name": "Gold Flash",      "print_run": 10},
    {"name": "Lucky Envelopes", "print_run": 8},
    {"name": "Green",           "print_run": 5},
    {"name": "Green Disco",     "print_run": 5},
    {"name": "Black",           "print_run": 1},
    {"name": "Black & Gold",    "print_run": 1},
    {"name": "Black Disco",     "print_run": 1},
    {"name": "Black Flash",     "print_run": 1},
]

PARALLELS_PREMIER = [
    {"name": "Blue",            "print_run": None},
    {"name": "Disco",           "print_run": None},
    {"name": "Elephant",        "print_run": None},
    {"name": "Green & Purple",  "print_run": None},
    {"name": "Orange Flash",    "print_run": None},
    {"name": "Scope",           "print_run": None},
    {"name": "Silver",          "print_run": None},
    {"name": "Tiger",           "print_run": None},
    {"name": "Tri-Color",       "print_run": None},
    {"name": "Zebra",           "print_run": None},
    {"name": "Bronze",          "print_run": 175},
    {"name": "Maroon",          "print_run": 125},
    {"name": "Red Disco",       "print_run": 99},
    {"name": "Purple",          "print_run": 60},
    {"name": "Blue Disco",      "print_run": 49},
    {"name": "Teal & Pink",     "print_run": 49},
    {"name": "Orange",          "print_run": 35},
    {"name": "Tie-Dye",         "print_run": 25},
    {"name": "Gold",            "print_run": 10},
    {"name": "Gold Disco",      "print_run": 10},
    {"name": "Gold Flash",      "print_run": 10},
    {"name": "Lucky Envelopes", "print_run": 8},
    {"name": "Green",           "print_run": 5},
    {"name": "Green Disco",     "print_run": 5},
    {"name": "Black",           "print_run": 1},
    {"name": "Black & Gold",    "print_run": 1},
    {"name": "Black Disco",     "print_run": 1},
    {"name": "Black Flash",     "print_run": 1},
]

PARALLELS_OCTAGONSIDE = [
    {"name": "Blue",            "print_run": None},
    {"name": "Disco",           "print_run": None},
    {"name": "Elephant",        "print_run": None},
    {"name": "Orange Flash",    "print_run": None},
    {"name": "Scope",           "print_run": None},
    {"name": "Silver",          "print_run": None},
    {"name": "Tiger",           "print_run": None},
    {"name": "Tri-Color",       "print_run": None},
    {"name": "Zebra",           "print_run": None},
    {"name": "Red Disco",       "print_run": 99},
    {"name": "Blue Disco",      "print_run": 49},
    {"name": "Tie-Dye",         "print_run": 25},
    {"name": "Gold",            "print_run": 10},
    {"name": "Gold Disco",      "print_run": 10},
    {"name": "Gold Flash",      "print_run": 10},
    {"name": "Cracked Ice",     "print_run": 8},
    {"name": "Lucky Envelopes", "print_run": 8},
    {"name": "Green",           "print_run": 5},
    {"name": "Green Disco",     "print_run": 5},
    {"name": "Black",           "print_run": 1},
    {"name": "Black & Gold",    "print_run": 1},
    {"name": "Black Disco",     "print_run": 1},
    {"name": "Black Flash",     "print_run": 1},
]

PARALLELS_MEZZANINE = [
    {"name": "Silver",  "print_run": None},
    {"name": "Tie-Dye", "print_run": 25},
    {"name": "Gold",    "print_run": 10},
    {"name": "Green",   "print_run": 5},
    {"name": "Black",   "print_run": 1},
]

# ─────────────────────────────────────────────────────────────
# Embedded checklists
# ─────────────────────────────────────────────────────────────

CONCOURSE_TEXT = """
1 Grant Dawson - Lightweight
2 Anderson Silva - Middleweight
3 Karol Rosa - Bantamweight
4 Alonzo Menifield - Light Heavyweight
5 Kamaru Usman - Welterweight
6 Brandon Royval - Flyweight
7 Petr Yan - Bantamweight
8 Jared Cannonier - Middleweight
9 Zhang Weili - Strawweight
10 Mackenzie Dern - Strawweight
11 Sean Strickland - Middleweight
12 Daniel Cormier - Heavyweight
13 Billy Quarantillo - Featherweight
14 Shamil Gamzatov - Light Heavyweight
15 Alexander Volkanovski - Featherweight
16 Matt Schnell - Flyweight
17 Glover Teixeira - Light Heavyweight
18 Paulo Costa - Middleweight
19 Holly Holm - Bantamweight
20 Tai Tuivasa - Heavyweight
21 Daniel Rodriguez - Welterweight
22 Tito Ortiz - Light Heavyweight
23 Ilia Topuria - Featherweight
24 Thiago Moises - Lightweight
25 Israel Adesanya - Middleweight
26 Merab Dvalishvili - Bantamweight
27 Robert Whittaker - Middleweight
28 Darren Till - Middleweight
29 Islam Makhachev - Lightweight
30 Michelle Waterson - Strawweight
31 Sean Brady - Welterweight
32 Dan Henderson - Middleweight
33 Lerone Murphy - Featherweight
34 Andre Muniz - Middleweight
35 Francis Ngannou - Heavyweight
36 Marlon Vera - Bantamweight
37 Jan Blachowicz - Light Heavyweight
38 Kelvin Gastelum - Middleweight
39 Khamzat Chimaev - Welterweight
40 Angela Hill - Strawweight
41 Rafael Fiziev - Lightweight
42 Henry Cejudo - Bantamweight
43 Movsar Evloev - Featherweight
44 Dricus du Plessis - Middleweight
45 Charles Oliveira - Lightweight
46 Pedro Munhoz - Bantamweight
47 Ciryl Gane - Heavyweight
48 Dominick Reyes - Light Heavyweight
49 Khabib Nurmagomedov - Lightweight
50 Taila Santos - Flyweight
51 Ian Garry - Welterweight
52 Rashad Evans - Light Heavyweight
53 Casey O'Neill - Flyweight
54 Nate Diaz - Welterweight
55 Jon Jones - Light Heavyweight
56 Rafael Dos Anjos - Lightweight
57 Aljamain Sterling - Bantamweight
58 Nikita Krylov - Light Heavyweight
59 Adrian Yanez - Bantamweight
60 Viviane Araujo - Flyweight
61 Paddy Pimblett - Lightweight
62 Chael Sonnen - Middleweight
63 Rogerio Bontorin - Flyweight
64 Abubakar Nurmagomedov - Welterweight
65 Max Holloway - Featherweight
66 Dan Hooker - Lightweight
67 Valentina Shevchenko - Flyweight
68 Jamahal Hill - Light Heavyweight
69 Manon Fiorot - Flyweight
70 Cynthia Calvillo - Flyweight
71 Pannie Kianzad - Bantamweight
72 Rich Franklin - Middleweight
73 Mudaerji Su - Flyweight
74 Li Jingliang - Welterweight
75 Dustin Poirier - Lightweight
76 Vicente Luque - Welterweight
77 Rose Namajunas - Strawweight
78 Jimmy Crute - Light Heavyweight
79 Chris Daukaus - Heavyweight
80 Yana Kunitskaya - Bantamweight
81 Umar Nurmagomedov - Bantamweight
82 Michael Bisping - Middleweight
83 Matheus Nicolau - Flyweight
84 Shavkat Rakhmonov - Welterweight
85 Stipe Miocic - Heavyweight
86 Neil Magny - Welterweight
87 Julianna Pena - Bantamweight
88 Jair Rozenstruik - Heavyweight
89 Marcin Tybura - Heavyweight
90 Sara McMann - Bantamweight
91 Julia Avila - Bantamweight
92 Alex Perez - Flyweight
93 Conor McGregor - Lightweight
94 Alexandre Pantoja - Flyweight
95 Brandon Moreno - Flyweight
96 Belal Muhammad - Welterweight
97 Amanda Nunes - Featherweight
98 Tom Aspinall - Heavyweight
99 Paul Craig - Light Heavyweight
100 Brock Lesnar - Heavyweight
"""

PREMIER_TEXT = """
101 Kamaru Usman - Welterweight
102 Nate Diaz - Welterweight
103 Petr Yan - Bantamweight
104 Santiago Ponzinibbio - Welterweight
105 Zhang Weili - Strawweight
106 Augusto Sakai - Heavyweight
107 Grant Dawson - Lightweight
108 Georges St-Pierre - Welterweight
109 Ricky Simon - Bantamweight
110 Conor McGregor - Lightweight
111 Alexander Volkanovski - Featherweight
112 Kai Kara-France - Flyweight
113 Glover Teixeira - Light Heavyweight
114 Derek Brunson - Middleweight
115 Holly Holm - Bantamweight
116 Nina Nunes - Strawweight
117 Sean Strickland - Middleweight
118 Royce Gracie - Welterweight
119 Steven Peterson - Featherweight
120 Claudio Puelles - Lightweight
121 Israel Adesanya - Middleweight
122 Rob Font - Bantamweight
123 Robert Whittaker - Middleweight
124 Jack Hermansson - Middleweight
125 Islam Makhachev - Lightweight
126 Tecia Torres - Strawweight
127 Daniel Rodriguez - Welterweight
128 Chuck Liddell - Light Heavyweight
129 Tucker Lutz - Featherweight
130 Fares Ziam - Lightweight
131 Francis Ngannou - Heavyweight
132 Dominick Cruz - Bantamweight
133 Jan Blachowicz - Light Heavyweight
134 Uriah Hall - Middleweight
135 Khamzat Chimaev - Welterweight
136 Amanda Ribas - Flyweight
137 Sean Brady - Welterweight
138 BJ Penn - Lightweight
139 Amir Albazi - Flyweight
140 Jalin Turner - Lightweight
141 Charles Oliveira - Lightweight
142 Marlon Moraes - Bantamweight
143 Ciryl Gane - Heavyweight
144 Thiago Santos - Light Heavyweight
145 Khabib Nurmagomedov - Lightweight
146 Jennifer Maia - Flyweight
147 Rafael Fiziev - Lightweight
148 Matt Hughes - Welterweight
149 Jeffrey Molina - Flyweight
150 Joel Alvarez - Lightweight
151 Jon Jones - Light Heavyweight
152 Frankie Edgar - Bantamweight
153 Aljamain Sterling - Bantamweight
154 Volkan Oezdemir - Light Heavyweight
155 Adrian Yanez - Bantamweight
156 Joanne Wood - Flyweight
157 Ian Garry - Welterweight
158 Cain Velasquez - Heavyweight
159 Raulian Paiva - Bantamweight
160 Mateusz Gamrot - Lightweight
161 Max Holloway - Featherweight
162 Tony Ferguson - Lightweight
163 Valentina Shevchenko - Flyweight
164 Johnny Walker - Light Heavyweight
165 Manon Fiorot - Flyweight
166 Andrea Lee - Flyweight
167 Paddy Pimblett - Lightweight
168 Antonio Rodrigo Nogueira - Heavyweight
169 Alexandr Romanov - Heavyweight
170 Julian Marquez - Middleweight
171 Dustin Poirier - Lightweight
172 Brad Riddell - Lightweight
173 Rose Namajunas - Strawweight
174 Ryan Spann - Light Heavyweight
175 Chris Daukaus - Heavyweight
176 Ketlen Vieira - Bantamweight
177 Bea Malecki - Bantamweight
178 Mark Coleman - Heavyweight
179 Da-un Jung - Light Heavyweight
180 Phil Hawes - Middleweight
181 Stipe Miocic - Heavyweight
182 Stephen Thompson - Welterweight
183 Julianna Pena - Bantamweight
184 Curtis Blaydes - Heavyweight
185 Tom Aspinall - Heavyweight
186 Raquel Pennington - Bantamweight
187 Jack Shore - Bantamweight
188 Forrest Griffin - Light Heavyweight
189 Dustin Jacoby - Light Heavyweight
190 Cory McKenna - Strawweight
191 Brandon Moreno - Flyweight
192 Michael Chiesa - Welterweight
193 Amanda Nunes - Featherweight
194 Shamil Abdurakhimov - Heavyweight
195 Paul Craig - Light Heavyweight
196 Macy Chiasson - Bantamweight
197 Austin Lingo - Featherweight
198 Tatiana Suarez - Strawweight
199 Kennedy Nzechukwu - Light Heavyweight
200 Alex Morono - Welterweight
"""

OCTAGONSIDE_TEXT = """
201 Petr Yan - Bantamweight
202 Billy Quarantillo - Featherweight
203 Jessica Andrade - Flyweight
204 Manon Fiorot - Flyweight
205 Askar Askarov - Flyweight
206 Mudaerji Su - Flyweight
207 Islam Makhachev - Lightweight
208 Jiri Prochazka - Light Heavyweight
209 Kamaru Usman - Welterweight
210 Tecia Torres - Strawweight
211 Glover Teixeira - Light Heavyweight
212 Casey O'Neill - Flyweight
213 Holly Holm - Bantamweight
214 Pannie Kianzad - Bantamweight
215 Aljamain Sterling - Bantamweight
216 Thiago Moises - Lightweight
217 Michael Chandler - Lightweight
218 Aleksandar Rakic - Light Heavyweight
219 Alexander Volkanovski - Featherweight
220 Katlyn Chookagian - Flyweight
221 Jan Blachowicz - Light Heavyweight
222 Chris Daukaus - Heavyweight
223 Carla Esparza - Strawweight
224 Paul Craig - Light Heavyweight
225 TJ Dillashaw - Bantamweight
226 Tom Aspinall - Heavyweight
227 Colby Covington - Welterweight
228 Anthony Smith - Light Heavyweight
229 Israel Adesanya - Middleweight
230 Miesha Tate - Bantamweight
231 Ciryl Gane - Heavyweight
232 Daniel Rodriguez - Welterweight
233 Marina Rodriguez - Strawweight
234 Rafael Fiziev - Lightweight
235 Jose Aldo - Bantamweight
236 Umar Nurmagomedov - Bantamweight
237 Gilbert Burns - Welterweight
238 Magomed Ankalaev - Light Heavyweight
239 Francis Ngannou - Heavyweight
240 Maycee Barber - Flyweight
241 Robert Whittaker - Middleweight
242 Dricus du Plessis - Middleweight
243 Yan Xiaonan - Strawweight
244 Rogerio Bontorin - Flyweight
245 Cory Sandhagen - Bantamweight
246 Julia Avila - Bantamweight
247 Leon Edwards - Welterweight
248 Derrick Lewis - Heavyweight
249 Charles Oliveira - Lightweight
250 Ian Garry - Welterweight
251 Valentina Shevchenko - Flyweight
252 Grant Dawson - Lightweight
253 Irene Aldana - Bantamweight
254 Sean Brady - Welterweight
255 Brian Ortega - Featherweight
256 Karol Rosa - Bantamweight
257 Jorge Masvidal - Welterweight
258 Curtis Blaydes - Heavyweight
259 Jon Jones - Light Heavyweight
260 Paddy Pimblett - Lightweight
261 Rose Namajunas - Strawweight
262 Ilia Topuria - Featherweight
263 Mackenzie Dern - Strawweight
264 Sean Strickland - Middleweight
265 Yair Rodriguez - Featherweight
266 Movsar Evloev - Featherweight
267 Conor McGregor - Lightweight
268 Alexander Volkov - Heavyweight
269 Max Holloway - Featherweight
270 Abubakar Nurmagomedov - Welterweight
271 Amanda Nunes - Featherweight
272 Lerone Murphy - Featherweight
273 Lauren Murphy - Flyweight
274 Serghei Spivac - Heavyweight
275 Chan Sung Jung - Featherweight
276 Matheus Nicolau - Flyweight
277 Khamzat Chimaev - Welterweight
278 Tai Tuivasa - Heavyweight
279 Dustin Poirier - Lightweight
280 Adrian Yanez - Bantamweight
281 Julianna Pena - Bantamweight
282 Li Jingliang - Welterweight
283 Aspen Ladd - Bantamweight
284 Khabib Nurmagomedov - Lightweight
285 Justin Gaethje - Lightweight
286 Arman Tsarukyan - Lightweight
287 Sean O'Malley - Bantamweight
288 Nina Nunes - Strawweight
289 Stipe Miocic - Heavyweight
290 Alonzo Menifield - Light Heavyweight
291 Zhang Weili - Strawweight
292 Nate Diaz - Welterweight
293 Deiveson Figueiredo - Flyweight
294 Shavkat Rakhmonov - Welterweight
295 Beneil Dariush - Lightweight
296 Joel Alvarez - Lightweight
297 Marvin Vettori - Middleweight
298 Jamahal Hill - Light Heavyweight
299 Brandon Moreno - Flyweight
300 Andre Muniz - Middleweight
"""

MEZZANINE_TEXT = """
301 Glover Teixeira - Light Heavyweight
302 Amanda Nunes - Featherweight
303 Jan Blachowicz - Light Heavyweight
304 Julianna Pena - Bantamweight
305 Ciryl Gane - Heavyweight
306 Zhang Weili - Strawweight
307 Robert Whittaker - Middleweight
308 Valentina Shevchenko - Flyweight
309 Petr Yan - Bantamweight
310 Rose Namajunas - Strawweight
311 Casey O'Neill - Flyweight
312 Lerone Murphy - Featherweight
313 Chris Daukaus - Heavyweight
314 Li Jingliang - Welterweight
315 Daniel Rodriguez - Welterweight
316 Nate Diaz - Welterweight
317 Dricus du Plessis - Middleweight
318 Grant Dawson - Lightweight
319 Billy Quarantillo - Featherweight
320 Ilia Topuria - Featherweight
321 Holly Holm - Bantamweight
322 Lauren Murphy - Flyweight
323 Carla Esparza - Strawweight
324 Aspen Ladd - Bantamweight
325 Marina Rodriguez - Strawweight
326 Deiveson Figueiredo - Flyweight
327 Yan Xiaonan - Strawweight
328 Irene Aldana - Bantamweight
329 Jessica Andrade - Flyweight
330 Mackenzie Dern - Strawweight
331 Pannie Kianzad - Bantamweight
332 Serghei Spivac - Heavyweight
333 Paul Craig - Light Heavyweight
334 Shamil Gamzatov - Light Heavyweight
335 Rafael Fiziev - Lightweight
336 Shavkat Rakhmonov - Welterweight
337 Rogerio Bontorin - Flyweight
338 Sean Brady - Welterweight
339 Manon Fiorot - Flyweight
340 Sean Strickland - Middleweight
341 Aljamain Sterling - Bantamweight
342 Chan Sung Jung - Featherweight
343 TJ Dillashaw - Bantamweight
344 Justin Gaethje - Lightweight
345 Jose Aldo - Bantamweight
346 Beneil Dariush - Lightweight
347 Cory Sandhagen - Bantamweight
348 Brian Ortega - Featherweight
349 Askar Askarov - Flyweight
350 Yair Rodriguez - Featherweight
351 Thiago Moises - Lightweight
352 Matheus Nicolau - Flyweight
353 Tom Aspinall - Heavyweight
354 Arman Tsarukyan - Lightweight
355 Umar Nurmagomedov - Bantamweight
356 Joel Alvarez - Lightweight
357 Julia Avila - Bantamweight
358 Karol Rosa - Bantamweight
359 Mudaerji Su - Flyweight
360 Movsar Evloev - Featherweight
361 Michael Chandler - Lightweight
362 Khamzat Chimaev - Welterweight
363 Colby Covington - Welterweight
364 Sean O'Malley - Bantamweight
365 Gilbert Burns - Welterweight
366 Marvin Vettori - Middleweight
367 Leon Edwards - Welterweight
368 Jorge Masvidal - Welterweight
369 Islam Makhachev - Lightweight
370 Conor McGregor - Lightweight
371 Aleksandar Rakic - Light Heavyweight
372 Tai Tuivasa - Heavyweight
373 Anthony Smith - Light Heavyweight
374 Nina Nunes - Strawweight
375 Magomed Ankalaev - Light Heavyweight
376 Khabib Nurmagomedov - Lightweight
377 Derrick Lewis - Heavyweight
378 Curtis Blaydes - Heavyweight
379 Jiri Prochazka - Light Heavyweight
380 Alexander Volkov - Heavyweight
381 Alexander Volkanovski - Featherweight
382 Dustin Poirier - Lightweight
383 Israel Adesanya - Middleweight
384 Stipe Miocic - Heavyweight
385 Francis Ngannou - Heavyweight
386 Brandon Moreno - Flyweight
387 Charles Oliveira - Lightweight
388 Jon Jones - Light Heavyweight
389 Kamaru Usman - Welterweight
390 Max Holloway - Featherweight
391 Katlyn Chookagian - Flyweight
392 Adrian Yanez - Bantamweight
393 Miesha Tate - Bantamweight
394 Alonzo Menifield - Light Heavyweight
395 Maycee Barber - Flyweight
396 Andre Muniz - Middleweight
397 Ian Garry - Welterweight
398 Paddy Pimblett - Lightweight
399 Tecia Torres - Strawweight
400 Abubakar Nurmagomedov - Welterweight
"""

# ─────────────────────────────────────────────────────────────
# Parser
# ─────────────────────────────────────────────────────────────

CARD_LINE_RE = re.compile(r'^(\d+)\s+(.+)$')


def parse_cards(text: str, subset_tag: str) -> list:
    """Parse card lines; team is always null for this set."""
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
            "is_rookie": player in RC_FIGHTERS,
            "subset": subset_tag,
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
        "set_name": "2022 Panini Select UFC",
        "sport": "MMA",
        "season": "2022",
        "league": "UFC",
        "sections": sections,
        "players": players,
    }


# ─────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Parsing 2022 Panini Select UFC (base set)...")

    sections = [
        {
            "insert_set": "Concourse",
            "parallels": PARALLELS_CONCOURSE,
            "cards": parse_cards(CONCOURSE_TEXT, "Concourse"),
        },
        {
            "insert_set": "Premier Level",
            "parallels": PARALLELS_PREMIER,
            "cards": parse_cards(PREMIER_TEXT, "Premier Level"),
        },
        {
            "insert_set": "Octagonside",
            "parallels": PARALLELS_OCTAGONSIDE,
            "cards": parse_cards(OCTAGONSIDE_TEXT, "Octagonside"),
        },
        {
            "insert_set": "Mezzanine",
            "parallels": PARALLELS_MEZZANINE,
            "cards": parse_cards(MEZZANINE_TEXT, "Mezzanine"),
        },
    ]

    output = build_output(sections)

    out_path = "panini_select_ufc_2022_base_parsed.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nSet: {output['set_name']} ({output['season']})")
    print(f"Sections: {len(output['sections'])}")
    for s in output["sections"]:
        print(f"  {s['insert_set']:<20} {len(s['cards']):>3} cards  {len(s['parallels'])} parallels")

    print(f"\nTotal players: {len(output['players'])}")

    # ── Spot checks ───────────────────────────────────────────
    player_map = {p["player"]: p for p in output["players"]}

    # Section card counts
    for s in output["sections"]:
        assert len(s["cards"]) == 100, f"{s['insert_set']} has {len(s['cards'])} cards, expected 100"
    print("\n=== Card counts: all 4 sections have 100 cards ===")

    # Rookie check
    rc_found = [p for p in output["players"] if any(a["is_rookie"] for a in p["appearances"])]
    print(f"\n=== Rookies ({len(rc_found)}): {', '.join(p['player'] for p in rc_found)} ===")

    # Conor McGregor — appears in all 4 tiers
    cmg = player_map.get("Conor McGregor")
    if cmg:
        st = cmg["stats"]
        sections_found = [a["insert_set"] for a in cmg["appearances"]]
        print(f"\n=== Conor McGregor: {len(cmg['appearances'])} appearances ({', '.join(sections_found)}) ===")
        print(f"  unique_cards={st['unique_cards']}  1/1s={st['one_of_ones']}  insert_sets={st['insert_sets']}")

    # Fighters only in Mezzanine (smaller parallel block)
    mez_only = [p for p in output["players"]
                if all(a["insert_set"] == "Mezzanine" for a in p["appearances"])]
    print(f"\n=== Mezzanine-only fighters: {len(mez_only)} ===")
    if mez_only:
        ex = mez_only[0]
        st = ex["stats"]
        print(f"  e.g. {ex['player']}: unique_cards={st['unique_cards']} (1 base + {len(PARALLELS_MEZZANINE)} parallels)")
