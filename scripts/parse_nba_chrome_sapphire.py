#!/usr/bin/env python3
"""Parser for 2025-26 Topps Chrome Sapphire Basketball."""

import json
import re

# ─────────────────────────────────────────────────────────────
# Parallel definitions
# ─────────────────────────────────────────────────────────────

BASE_PARALLELS = [
    {"name": "Purple Sapphire",       "print_run": 75},
    {"name": "Gold Sapphire",         "print_run": 50},
    {"name": "Orange Sapphire",       "print_run": 25},
    {"name": "Black Sapphire",        "print_run": 10},
    {"name": "Red Sapphire",          "print_run": 5},
    {"name": "Padparadscha Sapphire", "print_run": 1},
]

AUTO_PARALLELS = [
    {"name": "Gold",         "print_run": 50},
    {"name": "Orange",       "print_run": 25},
    {"name": "Black",        "print_run": 10},
    {"name": "Red",          "print_run": 5},
    {"name": "Padparadscha", "print_run": 1},
]

SAP_SEL_PARALLELS = [
    {"name": "Gold",         "print_run": 50},
    {"name": "Orange",       "print_run": 25},
    {"name": "Red",          "print_run": 5},
    {"name": "Padparadscha", "print_run": 1},
]

# ─────────────────────────────────────────────────────────────
# Card data — Base Set (300 cards)
# Veterans 1-240, Legends 241-250, Rookies 251-300 (RC)
# ─────────────────────────────────────────────────────────────

BASE_TEXT = """
1 Trae Young - Atlanta Hawks
2 Jalen Johnson - Atlanta Hawks
3 De'Andre Hunter - Atlanta Hawks
4 Dyson Daniels - Atlanta Hawks
5 Onyeka Okongwu - Atlanta Hawks
6 Bogdan Bogdanović - Atlanta Hawks
7 Clint Capela - Atlanta Hawks
8 Zaccharie Risacher - Atlanta Hawks
9 Jayson Tatum - Boston Celtics
10 Jaylen Brown - Boston Celtics
11 Derrick White - Boston Celtics
12 Jrue Holiday - Boston Celtics
13 Al Horford - Boston Celtics
14 Payton Pritchard - Boston Celtics
15 Kristaps Porzingis - Boston Celtics
16 Sam Hauser - Boston Celtics
17 Cam Thomas - Brooklyn Nets
18 Nic Claxton - Brooklyn Nets
19 Cameron Johnson - Brooklyn Nets
20 Ben Simmons - Brooklyn Nets
21 Dennis Schroder - Brooklyn Nets
22 Day'ron Sharpe - Brooklyn Nets
23 Noah Clowney - Brooklyn Nets
24 Trendon Watford - Brooklyn Nets
25 LaMelo Ball - Charlotte Hornets
26 Brandon Miller - Charlotte Hornets
27 Miles Bridges - Charlotte Hornets
28 Mark Williams - Charlotte Hornets
29 Grant Williams - Charlotte Hornets
30 Tre Mann - Charlotte Hornets
31 Nick Richards - Charlotte Hornets
32 Bryce McGowens - Charlotte Hornets
33 Zach LaVine - Chicago Bulls
34 Nikola Vučević - Chicago Bulls
35 Coby White - Chicago Bulls
36 Josh Giddey - Chicago Bulls
37 Patrick Williams - Chicago Bulls
38 Ayo Dosunmu - Chicago Bulls
39 Dalen Terry - Chicago Bulls
40 Torrey Craig - Chicago Bulls
41 Donovan Mitchell - Cleveland Cavaliers
42 Darius Garland - Cleveland Cavaliers
43 Evan Mobley - Cleveland Cavaliers
44 Jarrett Allen - Cleveland Cavaliers
45 Max Strus - Cleveland Cavaliers
46 Isaac Okoro - Cleveland Cavaliers
47 Caris LeVert - Cleveland Cavaliers
48 Sam Merrill - Cleveland Cavaliers
49 Kyrie Irving - Dallas Mavericks
50 Anthony Davis - Dallas Mavericks
51 Dereck Lively II - Dallas Mavericks
52 P.J. Washington - Dallas Mavericks
53 Maxi Kleber - Dallas Mavericks
54 Naji Marshall - Dallas Mavericks
55 Tim Hardaway Jr. - Dallas Mavericks
56 Spencer Dinwiddie - Dallas Mavericks
57 Nikola Jokić - Denver Nuggets
58 Jamal Murray - Denver Nuggets
59 Michael Porter Jr. - Denver Nuggets
60 Aaron Gordon - Denver Nuggets
61 Kentavious Caldwell-Pope - Denver Nuggets
62 Christian Braun - Denver Nuggets
63 Peyton Watson - Denver Nuggets
64 Julian Strawther - Denver Nuggets
65 Cade Cunningham - Detroit Pistons
66 Jalen Duren - Detroit Pistons
67 Ausar Thompson - Detroit Pistons
68 Jaden Ivey - Detroit Pistons
69 Isaiah Stewart - Detroit Pistons
70 Marcus Sasser - Detroit Pistons
71 Ron Holland - Detroit Pistons
72 James Wiseman - Detroit Pistons
73 Stephen Curry - Golden State Warriors
74 Draymond Green - Golden State Warriors
75 Andrew Wiggins - Golden State Warriors
76 Jonathan Kuminga - Golden State Warriors
77 Moses Moody - Golden State Warriors
78 Gary Payton II - Golden State Warriors
79 Brandin Podziemski - Golden State Warriors
80 Jimmy Butler III - Golden State Warriors
81 Alperen Şengün - Houston Rockets
82 Jalen Green - Houston Rockets
83 Fred VanVleet - Houston Rockets
84 Jabari Smith Jr. - Houston Rockets
85 Amen Thompson - Houston Rockets
86 Tari Eason - Houston Rockets
87 Aaron Holiday - Houston Rockets
88 Dillon Brooks - Houston Rockets
89 Tyrese Haliburton - Indiana Pacers
90 Pascal Siakam - Indiana Pacers
91 Myles Turner - Indiana Pacers
92 Bennedict Mathurin - Indiana Pacers
93 Andrew Nembhard - Indiana Pacers
94 Aaron Nesmith - Indiana Pacers
95 T.J. McConnell - Indiana Pacers
96 Obi Toppin - Indiana Pacers
97 Kawhi Leonard - Los Angeles Clippers
98 James Harden - Los Angeles Clippers
99 Norman Powell - Los Angeles Clippers
100 Ivica Zubac - Los Angeles Clippers
101 Terance Mann - Los Angeles Clippers
102 Luke Kennard - Los Angeles Clippers
103 Mason Plumlee - Los Angeles Clippers
104 Amir Coffey - Los Angeles Clippers
105 LeBron James - Los Angeles Lakers
106 Luka Dončić - Los Angeles Lakers
107 Austin Reaves - Los Angeles Lakers
108 Rui Hachimura - Los Angeles Lakers
109 D'Angelo Russell - Los Angeles Lakers
110 Gabe Vincent - Los Angeles Lakers
111 Christian Wood - Los Angeles Lakers
112 Taurean Prince - Los Angeles Lakers
113 Ja Morant - Memphis Grizzlies
114 Desmond Bane - Memphis Grizzlies
115 Jaren Jackson Jr. - Memphis Grizzlies
116 Scottie Pippen Jr. - Memphis Grizzlies
117 Santi Aldama - Memphis Grizzlies
118 Marcus Smart - Memphis Grizzlies
119 GG Jackson II - Memphis Grizzlies
120 John Konchar - Memphis Grizzlies
121 Tyler Herro - Miami Heat
122 Bam Adebayo - Miami Heat
123 Terry Rozier - Miami Heat
124 Caleb Martin - Miami Heat
125 Duncan Robinson - Miami Heat
126 Josh Richardson - Miami Heat
127 Haywood Highsmith - Miami Heat
128 Thomas Bryant - Miami Heat
129 Giannis Antetokounmpo - Milwaukee Bucks
130 Damian Lillard - Milwaukee Bucks
131 Khris Middleton - Milwaukee Bucks
132 Bobby Portis Jr. - Milwaukee Bucks
133 Brook Lopez - Milwaukee Bucks
134 Malik Beasley - Milwaukee Bucks
135 Pat Connaughton - Milwaukee Bucks
136 MarJon Beauchamp - Milwaukee Bucks
137 Anthony Edwards - Minnesota Timberwolves
138 Rudy Gobert - Minnesota Timberwolves
139 Julius Randle - Minnesota Timberwolves
140 Mike Conley - Minnesota Timberwolves
141 Naz Reid - Minnesota Timberwolves
142 Jaden McDaniels - Minnesota Timberwolves
143 Nickeil Alexander-Walker - Minnesota Timberwolves
144 Kyle Anderson - Minnesota Timberwolves
145 Zion Williamson - New Orleans Pelicans
146 Brandon Ingram - New Orleans Pelicans
147 CJ McCollum - New Orleans Pelicans
148 Herb Jones - New Orleans Pelicans
149 Jonas Valančiūnas - New Orleans Pelicans
150 Trey Murphy III - New Orleans Pelicans
151 Dejounte Murray - New Orleans Pelicans
152 Larry Nance Jr. - New Orleans Pelicans
153 Jalen Brunson - New York Knicks
154 Karl-Anthony Towns - New York Knicks
155 OG Anunoby - New York Knicks
156 Josh Hart - New York Knicks
157 Mikal Bridges - New York Knicks
158 Donte DiVincenzo - New York Knicks
159 Mitchell Robinson - New York Knicks
160 Precious Achiuwa - New York Knicks
161 Shai Gilgeous-Alexander - Oklahoma City Thunder
162 Chet Holmgren - Oklahoma City Thunder
163 Jalen Williams - Oklahoma City Thunder
164 Isaiah Hartenstein - Oklahoma City Thunder
165 Lu Dort - Oklahoma City Thunder
166 Isaiah Joe - Oklahoma City Thunder
167 Kenrich Williams - Oklahoma City Thunder
168 Ousmane Dieng - Oklahoma City Thunder
169 Paolo Banchero - Orlando Magic
170 Franz Wagner - Orlando Magic
171 Jalen Suggs - Orlando Magic
172 Cole Anthony - Orlando Magic
173 Wendell Carter Jr. - Orlando Magic
174 Jonathan Isaac - Orlando Magic
175 Goga Bitadze - Orlando Magic
176 Markelle Fultz - Orlando Magic
177 Joel Embiid - Philadelphia 76ers
178 Tyrese Maxey - Philadelphia 76ers
179 Paul George - Philadelphia 76ers
180 Kelly Oubre Jr. - Philadelphia 76ers
181 Tobias Harris - Philadelphia 76ers
182 De'Anthony Melton - Philadelphia 76ers
183 Shake Milton - Philadelphia 76ers
184 Paul Reed - Philadelphia 76ers
185 Kevin Durant - Phoenix Suns
186 Devin Booker - Phoenix Suns
187 Bradley Beal - Phoenix Suns
188 Jusuf Nurkić - Phoenix Suns
189 Grayson Allen - Phoenix Suns
190 David Roddy - Phoenix Suns
191 Josh Okogie - Phoenix Suns
192 Eric Gordon - Phoenix Suns
193 Anfernee Simons - Portland Trail Blazers
194 Scoot Henderson - Portland Trail Blazers
195 Jerami Grant - Portland Trail Blazers
196 Shaedon Sharpe - Portland Trail Blazers
197 Toumani Camara - Portland Trail Blazers
198 Robert Williams III - Portland Trail Blazers
199 Matisse Thybulle - Portland Trail Blazers
200 Malcolm Brogdon - Portland Trail Blazers
201 Domantas Sabonis - Sacramento Kings
202 De'Aaron Fox - Sacramento Kings
203 Keegan Murray - Sacramento Kings
204 Kevin Huerter - Sacramento Kings
205 Harrison Barnes - Sacramento Kings
206 Malik Monk - Sacramento Kings
207 Trey Lyles - Sacramento Kings
208 Alex Len - Sacramento Kings
209 Victor Wembanyama - San Antonio Spurs
210 Stephon Castle - San Antonio Spurs
211 Devin Vassell - San Antonio Spurs
212 Keldon Johnson - San Antonio Spurs
213 Jeremy Sochan - San Antonio Spurs
214 Tre Jones - San Antonio Spurs
215 Zach Collins - San Antonio Spurs
216 Blake Wesley - San Antonio Spurs
217 Scottie Barnes - Toronto Raptors
218 Immanuel Quickley - Toronto Raptors
219 Gradey Dick - Toronto Raptors
220 RJ Barrett - Toronto Raptors
221 Jakob Poeltl - Toronto Raptors
222 Ochai Agbaji - Toronto Raptors
223 Gary Trent Jr. - Toronto Raptors
224 Javon Freeman-Liberty - Toronto Raptors
225 Lauri Markkanen - Utah Jazz
226 Jordan Clarkson - Utah Jazz
227 Walker Kessler - Utah Jazz
228 Keyonte George - Utah Jazz
229 John Collins - Utah Jazz
230 Collin Sexton - Utah Jazz
231 Kris Dunn - Utah Jazz
232 Taylor Hendricks - Utah Jazz
233 Jordan Poole - Washington Wizards
234 Bilal Coulibaly - Washington Wizards
235 Kyle Kuzma - Washington Wizards
236 Deni Avdija - Washington Wizards
237 Alex Sarr - Washington Wizards
238 Daniel Gafford - Washington Wizards
239 Marvin Bagley III - Washington Wizards
240 Johnny Davis - Washington Wizards
241 Michael Jordan - Chicago Bulls
242 Shaquille O'Neal - Los Angeles Lakers
243 Kobe Bryant - Los Angeles Lakers
244 Magic Johnson - Los Angeles Lakers
245 Larry Bird - Boston Celtics
246 Kareem Abdul-Jabbar - Los Angeles Lakers
247 Tim Duncan - San Antonio Spurs
248 Dirk Nowitzki - Dallas Mavericks
249 Allen Iverson - Philadelphia 76ers
250 Kevin Garnett - Minnesota Timberwolves
251 Cooper Flagg - Dallas Mavericks RC
252 Dylan Harper - San Antonio Spurs RC
253 VJ Edgecombe - Philadelphia 76ers RC
254 Kon Knueppel - Charlotte Hornets RC
255 Ace Bailey - Utah Jazz RC
256 Tre Johnson III - Washington Wizards RC
257 Jeremiah Fears - New Orleans Pelicans RC
258 Egor Dëmin - Brooklyn Nets RC
259 Collin Murray-Boyles - Toronto Raptors RC
260 Khaman Maluach - Phoenix Suns RC
261 Cedric Coward - Memphis Grizzlies RC
262 Noa Essengue - Chicago Bulls RC
263 Derik Queen - New Orleans Pelicans RC
264 Carter Bryant - San Antonio Spurs RC
265 Thomas Sorber - Oklahoma City Thunder RC
266 Yang Hansen - Portland Trail Blazers RC
267 Joan Beringer - Minnesota Timberwolves RC
268 Walter Clayton Jr. - Utah Jazz RC
269 Nolan Traore - Brooklyn Nets RC
270 Kasparas Jakučionis - Miami Heat RC
271 Will Riley - Washington Wizards RC
272 Drake Powell - Brooklyn Nets RC
273 Asa Newell - Atlanta Hawks RC
274 Nique Clifford - Sacramento Kings RC
275 Jase Richardson - Orlando Magic RC
276 Ben Saraf - Brooklyn Nets RC
277 Danny Wolf - Brooklyn Nets RC
278 Hugo González - Boston Celtics RC
279 Liam McNeeley - Charlotte Hornets RC
280 Yanic Konan-Niederhäuser - Los Angeles Clippers RC
281 Rasheer Fleming - Phoenix Suns RC
282 Adou Thiero - Los Angeles Lakers RC
283 Noah Penda - Orlando Magic RC
284 Ryan Kalkbrenner - Charlotte Hornets RC
285 Johni Broome - Philadelphia 76ers RC
286 Alijah Martin - Toronto Raptors RC
287 Maxime Raynaud - Sacramento Kings RC
288 Tyrese Proctor - Cleveland Cavaliers RC
289 Kam Jones - Indiana Pacers RC
290 Chaz Lanier - Detroit Pistons RC
291 Micah Peavy - New Orleans Pelicans RC
292 Koby Brea - Phoenix Suns RC
293 Jamir Watkins - Washington Wizards RC
294 Brooks Barnhizer - Oklahoma City Thunder RC
295 Sion James - Charlotte Hornets RC
296 Kobe Sanders - Los Angeles Clippers RC
297 Enrique Freeman - Indiana Pacers RC
298 Tevita Arona - Houston Rockets RC
299 David Skara - Oklahoma City Thunder RC
300 Jalil Bethea - Miami Heat RC
"""

# ─────────────────────────────────────────────────────────────
# Topps Chrome Autographs (25 veterans)
# ─────────────────────────────────────────────────────────────

CHROME_AUTO_TEXT = """
TCSA-NJ Nikola Jokić - Denver Nuggets
TCSA-VW Victor Wembanyama - San Antonio Spurs
TCSA-SC Stephen Curry - Golden State Warriors
TCSA-LJ LeBron James - Los Angeles Lakers
TCSA-GA Giannis Antetokounmpo - Milwaukee Bucks
TCSA-LD Luka Dončić - Los Angeles Lakers
TCSA-JT Jayson Tatum - Boston Celtics
TCSA-AE Anthony Edwards - Minnesota Timberwolves
TCSA-SGA Shai Gilgeous-Alexander - Oklahoma City Thunder
TCSA-KD Kevin Durant - Phoenix Suns
TCSA-CC Cade Cunningham - Detroit Pistons
TCSA-TY Trae Young - Atlanta Hawks
TCSA-JE Joel Embiid - Philadelphia 76ers
TCSA-DB Devin Booker - Phoenix Suns
TCSA-DM Donovan Mitchell - Cleveland Cavaliers
TCSA-JB Jalen Brunson - New York Knicks
TCSA-PB Paolo Banchero - Orlando Magic
TCSA-KAT Karl-Anthony Towns - New York Knicks
TCSA-TH Tyrese Haliburton - Indiana Pacers
TCSA-LB LaMelo Ball - Charlotte Hornets
TCSA-JM Ja Morant - Memphis Grizzlies
TCSA-DL Damian Lillard - Milwaukee Bucks
TCSA-JBR Jaylen Brown - Boston Celtics
TCSA-KL Kawhi Leonard - Los Angeles Clippers
TCSA-ZL Zach LaVine - Chicago Bulls
"""

# ─────────────────────────────────────────────────────────────
# Topps Chrome Autographs Rookies (40 rookies)
# ─────────────────────────────────────────────────────────────

CHROME_AUTO_RC_TEXT = """
TCSAR-CF Cooper Flagg - Dallas Mavericks
TCSAR-DH Dylan Harper - San Antonio Spurs
TCSAR-VJE VJ Edgecombe - Philadelphia 76ers
TCSAR-AB Ace Bailey - Utah Jazz
TCSAR-KK Kon Knueppel - Charlotte Hornets
TCSAR-TJ Tre Johnson III - Washington Wizards
TCSAR-JF Jeremiah Fears - New Orleans Pelicans
TCSAR-ED Egor Dëmin - Brooklyn Nets
TCSAR-CM Collin Murray-Boyles - Toronto Raptors
TCSAR-KM Khaman Maluach - Phoenix Suns
TCSAR-CC Cedric Coward - Memphis Grizzlies
TCSAR-NE Noa Essengue - Chicago Bulls
TCSAR-DQ Derik Queen - New Orleans Pelicans
TCSAR-CB Carter Bryant - San Antonio Spurs
TCSAR-TS Thomas Sorber - Oklahoma City Thunder
TCSAR-YH Yang Hansen - Portland Trail Blazers
TCSAR-JBN Joan Beringer - Minnesota Timberwolves
TCSAR-WC Walter Clayton Jr. - Utah Jazz
TCSAR-NT Nolan Traore - Brooklyn Nets
TCSAR-KJ Kasparas Jakučionis - Miami Heat
TCSAR-WR Will Riley - Washington Wizards
TCSAR-DP Drake Powell - Brooklyn Nets
TCSAR-AN Asa Newell - Atlanta Hawks
TCSAR-NC Nique Clifford - Sacramento Kings
TCSAR-JR Jase Richardson - Orlando Magic
TCSAR-BS Ben Saraf - Brooklyn Nets
TCSAR-DW Danny Wolf - Brooklyn Nets
TCSAR-HG Hugo González - Boston Celtics
TCSAR-LM Liam McNeeley - Charlotte Hornets
TCSAR-YK Yanic Konan-Niederhäuser - Los Angeles Clippers
TCSAR-RF Rasheer Fleming - Phoenix Suns
TCSAR-AT Adou Thiero - Los Angeles Lakers
TCSAR-NP Noah Penda - Orlando Magic
TCSAR-RK Ryan Kalkbrenner - Charlotte Hornets
TCSAR-JBR Johni Broome - Philadelphia 76ers
TCSAR-AM Alijah Martin - Toronto Raptors
TCSAR-MR Maxime Raynaud - Sacramento Kings
TCSAR-TP Tyrese Proctor - Cleveland Cavaliers
TCSAR-KJO Kam Jones - Indiana Pacers
TCSAR-KS Kobe Sanders - Los Angeles Clippers
"""

# ─────────────────────────────────────────────────────────────
# Sky-Write Signatures (33 veterans)
# ─────────────────────────────────────────────────────────────

SKY_WRITE_TEXT = """
SWS-NJ Nikola Jokić - Denver Nuggets
SWS-LJ LeBron James - Los Angeles Lakers
SWS-SC Stephen Curry - Golden State Warriors
SWS-SGA Shai Gilgeous-Alexander - Oklahoma City Thunder
SWS-AE Anthony Edwards - Minnesota Timberwolves
SWS-LD Luka Dončić - Los Angeles Lakers
SWS-VW Victor Wembanyama - San Antonio Spurs
SWS-JT Jayson Tatum - Boston Celtics
SWS-GA Giannis Antetokounmpo - Milwaukee Bucks
SWS-KD Kevin Durant - Phoenix Suns
SWS-TY Trae Young - Atlanta Hawks
SWS-PB Paolo Banchero - Orlando Magic
SWS-JM Ja Morant - Memphis Grizzlies
SWS-JB Jalen Brunson - New York Knicks
SWS-DM Donovan Mitchell - Cleveland Cavaliers
SWS-AS Alperen Şengün - Houston Rockets
SWS-KAT Karl-Anthony Towns - New York Knicks
SWS-DB Devin Booker - Phoenix Suns
SWS-FW Franz Wagner - Orlando Magic
SWS-TH Tyrese Haliburton - Indiana Pacers
SWS-JG Jalen Green - Houston Rockets
SWS-LB LaMelo Ball - Charlotte Hornets
SWS-JH Jrue Holiday - Boston Celtics
SWS-CC Cade Cunningham - Detroit Pistons
SWS-PS Pascal Siakam - Indiana Pacers
SWS-SB Scottie Barnes - Toronto Raptors
SWS-EM Evan Mobley - Cleveland Cavaliers
SWS-CH Chet Holmgren - Oklahoma City Thunder
SWS-AD Anthony Davis - Dallas Mavericks
SWS-KI Kyrie Irving - Dallas Mavericks
SWS-ZW Zion Williamson - New Orleans Pelicans
SWS-DLI Damian Lillard - Milwaukee Bucks
SWS-JBR Jaylen Brown - Boston Celtics
"""

# ─────────────────────────────────────────────────────────────
# Topps Certified Autograph Issue – Rookies (30 rookies)
# ─────────────────────────────────────────────────────────────

TCAI_RC_TEXT = """
TCAIR-CF Cooper Flagg - Dallas Mavericks
TCAIR-DH Dylan Harper - San Antonio Spurs
TCAIR-VJE VJ Edgecombe - Philadelphia 76ers
TCAIR-AB Ace Bailey - Utah Jazz
TCAIR-KK Kon Knueppel - Charlotte Hornets
TCAIR-TJ Tre Johnson III - Washington Wizards
TCAIR-JF Jeremiah Fears - New Orleans Pelicans
TCAIR-ED Egor Dëmin - Brooklyn Nets
TCAIR-CM Collin Murray-Boyles - Toronto Raptors
TCAIR-KM Khaman Maluach - Phoenix Suns
TCAIR-CC Cedric Coward - Memphis Grizzlies
TCAIR-NE Noa Essengue - Chicago Bulls
TCAIR-DQ Derik Queen - New Orleans Pelicans
TCAIR-CB Carter Bryant - San Antonio Spurs
TCAIR-TS Thomas Sorber - Oklahoma City Thunder
TCAIR-WC Walter Clayton Jr. - Utah Jazz
TCAIR-NT Nolan Traore - Brooklyn Nets
TCAIR-KJ Kasparas Jakučionis - Miami Heat
TCAIR-WR Will Riley - Washington Wizards
TCAIR-AN Asa Newell - Atlanta Hawks
TCAIR-JR Jase Richardson - Orlando Magic
TCAIR-LM Liam McNeeley - Charlotte Hornets
TCAIR-RF Rasheer Fleming - Phoenix Suns
TCAIR-AT Adou Thiero - Los Angeles Lakers
TCAIR-NP Noah Penda - Orlando Magic
TCAIR-JBR Johni Broome - Philadelphia 76ers
TCAIR-AM Alijah Martin - Toronto Raptors
TCAIR-TP Tyrese Proctor - Cleveland Cavaliers
TCAIR-KJO Kam Jones - Indiana Pacers
TCAIR-KS Kobe Sanders - Los Angeles Clippers
"""

# ─────────────────────────────────────────────────────────────
# Next Stop Signatures (30 rookies)
# ─────────────────────────────────────────────────────────────

NEXT_STOP_TEXT = """
NSS-CF Cooper Flagg - Dallas Mavericks
NSS-DH Dylan Harper - San Antonio Spurs
NSS-VJE VJ Edgecombe - Philadelphia 76ers
NSS-AB Ace Bailey - Utah Jazz
NSS-KK Kon Knueppel - Charlotte Hornets
NSS-TJ Tre Johnson III - Washington Wizards
NSS-JF Jeremiah Fears - New Orleans Pelicans
NSS-ED Egor Dëmin - Brooklyn Nets
NSS-CM Collin Murray-Boyles - Toronto Raptors
NSS-KM Khaman Maluach - Phoenix Suns
NSS-CC Cedric Coward - Memphis Grizzlies
NSS-NE Noa Essengue - Chicago Bulls
NSS-DQ Derik Queen - New Orleans Pelicans
NSS-CB Carter Bryant - San Antonio Spurs
NSS-TS Thomas Sorber - Oklahoma City Thunder
NSS-YH Yang Hansen - Portland Trail Blazers
NSS-JBN Joan Beringer - Minnesota Timberwolves
NSS-WC Walter Clayton Jr. - Utah Jazz
NSS-NT Nolan Traore - Brooklyn Nets
NSS-KJ Kasparas Jakučionis - Miami Heat
NSS-WR Will Riley - Washington Wizards
NSS-DP Drake Powell - Brooklyn Nets
NSS-AN Asa Newell - Atlanta Hawks
NSS-NC Nique Clifford - Sacramento Kings
NSS-JR Jase Richardson - Orlando Magic
NSS-BS Ben Saraf - Brooklyn Nets
NSS-LM Liam McNeeley - Charlotte Hornets
NSS-NP Noah Penda - Orlando Magic
NSS-AM Alijah Martin - Toronto Raptors
NSS-KS Kobe Sanders - Los Angeles Clippers
"""

# ─────────────────────────────────────────────────────────────
# Signature Style (37 veterans + legends)
# ─────────────────────────────────────────────────────────────

SIG_STYLE_TEXT = """
SIS-NJ Nikola Jokić - Denver Nuggets
SIS-SC Stephen Curry - Golden State Warriors
SIS-LJ LeBron James - Los Angeles Lakers
SIS-GA Giannis Antetokounmpo - Milwaukee Bucks
SIS-VW Victor Wembanyama - San Antonio Spurs
SIS-SGA Shai Gilgeous-Alexander - Oklahoma City Thunder
SIS-AE Anthony Edwards - Minnesota Timberwolves
SIS-LD Luka Dončić - Los Angeles Lakers
SIS-JT Jayson Tatum - Boston Celtics
SIS-KD Kevin Durant - Phoenix Suns
SIS-JM Ja Morant - Memphis Grizzlies
SIS-TY Trae Young - Atlanta Hawks
SIS-DB Devin Booker - Phoenix Suns
SIS-DM Donovan Mitchell - Cleveland Cavaliers
SIS-JB Jalen Brunson - New York Knicks
SIS-LB LaMelo Ball - Charlotte Hornets
SIS-PB Paolo Banchero - Orlando Magic
SIS-JG Jalen Green - Houston Rockets
SIS-CC Cade Cunningham - Detroit Pistons
SIS-AS Alperen Şengün - Houston Rockets
SIS-KAT Karl-Anthony Towns - New York Knicks
SIS-TH Tyrese Haliburton - Indiana Pacers
SIS-AD Anthony Davis - Dallas Mavericks
SIS-KI Kyrie Irving - Dallas Mavericks
SIS-ZW Zion Williamson - New Orleans Pelicans
SIS-FW Franz Wagner - Orlando Magic
SIS-SB Scottie Barnes - Toronto Raptors
SIS-EM Evan Mobley - Cleveland Cavaliers
SIS-JH Jrue Holiday - Boston Celtics
SIS-SO Shaquille O'Neal - Los Angeles Lakers
SIS-MJ Magic Johnson - Los Angeles Lakers
SIS-LBR Larry Bird - Boston Celtics
SIS-AI Allen Iverson - Philadelphia 76ers
SIS-TD Tim Duncan - San Antonio Spurs
SIS-KG Kevin Garnett - Minnesota Timberwolves
SIS-DN Dirk Nowitzki - Dallas Mavericks
SIS-KB Kobe Bryant - Los Angeles Lakers
"""

# ─────────────────────────────────────────────────────────────
# Topps Chrome Autographs II (1 card)
# ─────────────────────────────────────────────────────────────

CHROME_AUTO_II_TEXT = """
TCSA2-NJ Nikola Jokić - Denver Nuggets
"""

# ─────────────────────────────────────────────────────────────
# Sapphire Selections (20 cards)
# ─────────────────────────────────────────────────────────────

SAP_SEL_TEXT = """
SS-1 Nikola Jokić - Denver Nuggets
SS-2 Victor Wembanyama - San Antonio Spurs
SS-3 Stephen Curry - Golden State Warriors
SS-4 LeBron James - Los Angeles Lakers
SS-5 Giannis Antetokounmpo - Milwaukee Bucks
SS-6 Luka Dončić - Los Angeles Lakers
SS-7 Anthony Edwards - Minnesota Timberwolves
SS-8 Shai Gilgeous-Alexander - Oklahoma City Thunder
SS-9 Jayson Tatum - Boston Celtics
SS-10 Kevin Durant - Phoenix Suns
SS-11 Ja Morant - Memphis Grizzlies
SS-12 Devin Booker - Phoenix Suns
SS-13 Donovan Mitchell - Cleveland Cavaliers
SS-14 Jalen Brunson - New York Knicks
SS-15 Joel Embiid - Philadelphia 76ers
SS-16 Trae Young - Atlanta Hawks
SS-17 Paolo Banchero - Orlando Magic
SS-18 Cade Cunningham - Detroit Pistons
SS-19 Karl-Anthony Towns - New York Knicks
SS-20 Cooper Flagg - Dallas Mavericks
"""

# ─────────────────────────────────────────────────────────────
# Infinite Sapphire (20 cards, no parallels)
# ─────────────────────────────────────────────────────────────

INF_SAP_TEXT = """
IS-1 Nikola Jokić - Denver Nuggets
IS-2 LeBron James - Los Angeles Lakers
IS-3 Stephen Curry - Golden State Warriors
IS-4 Giannis Antetokounmpo - Milwaukee Bucks
IS-5 Victor Wembanyama - San Antonio Spurs
IS-6 Anthony Edwards - Minnesota Timberwolves
IS-7 Shai Gilgeous-Alexander - Oklahoma City Thunder
IS-8 Luka Dončić - Los Angeles Lakers
IS-9 Jayson Tatum - Boston Celtics
IS-10 Kevin Durant - Phoenix Suns
IS-11 Ja Morant - Memphis Grizzlies
IS-12 Cade Cunningham - Detroit Pistons
IS-13 Trae Young - Atlanta Hawks
IS-14 Jalen Brunson - New York Knicks
IS-15 Paolo Banchero - Orlando Magic
IS-16 Devin Booker - Phoenix Suns
IS-17 Donovan Mitchell - Cleveland Cavaliers
IS-18 Joel Embiid - Philadelphia 76ers
IS-19 Damian Lillard - Milwaukee Bucks
IS-20 Karl-Anthony Towns - New York Knicks
"""

# ─────────────────────────────────────────────────────────────
# Parser
# ─────────────────────────────────────────────────────────────

CARD_LINE_RE = re.compile(r'^(\d+|[A-Z][A-Z0-9]*-[A-Z0-9]+)\s+(.+)$')


def parse_card_line(line: str, allow_rc: bool = False):
    line = line.strip()
    if not line:
        return None
    m = CARD_LINE_RE.match(line)
    if not m:
        return None

    card_number = m.group(1)
    rest = m.group(2).strip()

    is_rookie = False
    if allow_rc and rest.endswith(" RC"):
        is_rookie = True
        rest = rest[:-3].strip()

    idx = rest.rfind(" - ")
    if idx == -1:
        return None
    player = rest[:idx].strip()
    team = rest[idx + 3:].strip()

    return card_number, player, team, is_rookie


def parse_section(text: str, allow_rc: bool = False) -> list:
    cards = []
    for line in text.splitlines():
        result = parse_card_line(line, allow_rc=allow_rc)
        if result:
            card_number, player, team, is_rookie = result
            cards.append({
                "card_number": card_number,
                "player": player,
                "team": team,
                "is_rookie": is_rookie,
                "subset": None,
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
    rc_players: set = set()
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
                "is_rookie": pname in rc_players,
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
        "set_name": "2025-26 Topps Chrome Sapphire Basketball",
        "sport": "Basketball",
        "season": "2025-26",
        "league": "NBA",
        "sections": sections,
        "players": players,
    }


# ─────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Parsing 2025-26 Topps Chrome Sapphire Basketball...")

    sections = [
        {
            "insert_set": "Base Set",
            "parallels": BASE_PARALLELS,
            "cards": parse_section(BASE_TEXT, allow_rc=True),
        },
        {
            "insert_set": "Topps Chrome Autographs",
            "parallels": AUTO_PARALLELS,
            "cards": parse_section(CHROME_AUTO_TEXT),
        },
        {
            "insert_set": "Topps Chrome Autographs Rookies",
            "parallels": AUTO_PARALLELS,
            "cards": parse_section(CHROME_AUTO_RC_TEXT),
        },
        {
            "insert_set": "Sky-Write Signatures",
            "parallels": AUTO_PARALLELS,
            "cards": parse_section(SKY_WRITE_TEXT),
        },
        {
            "insert_set": "Topps Certified Autograph Issue – Rookies",
            "parallels": AUTO_PARALLELS,
            "cards": parse_section(TCAI_RC_TEXT),
        },
        {
            "insert_set": "Next Stop Signatures",
            "parallels": AUTO_PARALLELS,
            "cards": parse_section(NEXT_STOP_TEXT),
        },
        {
            "insert_set": "Signature Style",
            "parallels": AUTO_PARALLELS,
            "cards": parse_section(SIG_STYLE_TEXT),
        },
        {
            "insert_set": "Topps Chrome Autographs II",
            "parallels": [],
            "cards": parse_section(CHROME_AUTO_II_TEXT),
        },
        {
            "insert_set": "Sapphire Selections",
            "parallels": SAP_SEL_PARALLELS,
            "cards": parse_section(SAP_SEL_TEXT),
        },
        {
            "insert_set": "Infinite Sapphire",
            "parallels": [],
            "cards": parse_section(INF_SAP_TEXT),
        },
    ]

    output = build_output(sections)

    out_path = "nba_chrome_sapphire_parsed.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nSet: {output['set_name']} ({output['season']})")
    print(f"Sections: {len(output['sections'])}")
    for s in output["sections"]:
        rc_count = sum(1 for c in s["cards"] if c["is_rookie"])
        rc_str = f"  ({rc_count} RC)" if rc_count else ""
        print(f"  {s['insert_set']:<45} {len(s['cards']):>3} cards  {len(s['parallels'])} parallels{rc_str}")
    print(f"\nTotal players: {len(output['players'])}")

    player_map = {p["player"]: p for p in output["players"]}

    base_section = next(s for s in output["sections"] if s["insert_set"] == "Base Set")
    rc_count = sum(1 for c in base_section["cards"] if c["is_rookie"])
    print(f"\nBase Set: {len(base_section['cards'])} cards total, {rc_count} RCs")

    print("\n=== Cooper Flagg ===")
    if "Cooper Flagg" in player_map:
        cf = player_map["Cooper Flagg"]
        print(f"  Unique cards: {cf['stats']['unique_cards']}")
        print(f"  1/1s: {cf['stats']['one_of_ones']}")
        print(f"  Insert sets: {cf['stats']['insert_sets']}")
        for a in cf["appearances"]:
            print(f"  [{a['insert_set']}] #{a['card_number']} | rc={a['is_rookie']} | {len(a['parallels'])} parallels")

    print("\n=== Kobe Sanders (new player) ===")
    if "Kobe Sanders" in player_map:
        ks = player_map["Kobe Sanders"]
        for a in ks["appearances"]:
            print(f"  [{a['insert_set']}] #{a['card_number']} | rc={a['is_rookie']}")

    print("\n=== Nikola Jokić ===")
    if "Nikola Jokić" in player_map:
        nj = player_map["Nikola Jokić"]
        print(f"  Insert sets: {nj['stats']['insert_sets']}")
        print(f"  Unique cards: {nj['stats']['unique_cards']}")
