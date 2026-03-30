import json
import re

CHECKLIST_TEXT = """
2025 Topps Chrome MLS Checklist

Base Set
200 cards
Parallels

Blue Lava (Hobby Exclusive – 1 per box)
Mania (Mania Box Exclusive – 6 per box)
Prism (Hobby Exclusive – 4 per box)
Ray Wave (Value Box Exclusive – 4 per box)
Red Lava (Hobby Exclusive – 1:3 boxes)
Refractor (3 per Hobby box)
White Lava (Hobby Exclusive – 1:2 boxes)
Pink Mini Diamonds /250
Aqua Mini Diamonds /199
Aqua Refractor /199
Blue Mini Diamonds /150
Blue Refractor /150
Gold Mini Diamonds /50
Gold Refractor /50
Gold Wave /50
Green Mini Diamonds /99
Green Refractor /99
Purple Mini Diamonds /75
Purple Refractor /75
Purple Wave /75
Black Mini Diamonds /10
Black Refractor /10
Black Wave /10
Orange Mini Diamonds /25
Orange Refractor /25
Orange Wave /25
Pearl /30
Red Mini Diamonds /5
Red Refractor /5
Red Wave /5
Frozenfractor /-5
Superfractor /1

1 Roman Bürki, St. Louis City SC
2 Caden Clark, D.C. United
3 Ryan Gauld, Vancouver Whitecaps FC
4 Djordje Mihailovic, Toronto FC
5 Kristijan Kahlina, Charlotte FC
6 Cavan Sullivan, Philadelphia Union RC
7 David Villa, New York City FC
8 Emil Forsberg, New York Red Bulls
9 Zlatan Ibrahimović, LA Galaxy
10 Lionel Messi, Inter Miami CF
11 Marco Reus, LA Galaxy
12 Steven Moreira, Columbus Crew
13 Olivier Giroud, LAFC
14 Thierry Henry, New York Red Bulls
15 Peyton Miller, New England Revolution RC
16 Julian Hall, New York Red Bulls
17 Eduard Löwen, St. Louis City SC
18 Jeppe Tverskov, San Diego FC
19 Zane Monlouis, Toronto FC RC
20 Edvard Tagseth, Nashville SC RC
21 Pavel Bucha, FC Cincinnati
22 Ryan Kent, Seattle Sounders FC
23 Igor Jesus, LAFC RC
24 Lorenzo Insigne, Toronto FC
25 Jacen Russell-Rowe, Columbus Crew
26 Jack McGlynn, Houston Dynamo
27 Alejandro Alvarado, San Diego FC RC
28 Tadeo Allende, Inter Miami CF RC
29 Rafael Navarro, Colorado Rapids
30 Lucas Sanabria, LA Galaxy RC
31 Luis Suárez, Inter Miami CF
32 Aleksandr Guboglo, CF Montréal RC
33 Hugo Cuypers, Chicago Fire
34 Kelvin Yeboah, Minnesota United
35 Wayne Rooney, D.C. United
36 Hany Mukhtar, Nashville SC
37 Kaick, FC Dallas RC
38 Gabriel Pirani, D.C. United
39 Francis Westfield, Philadelphia Union RC
40 Jay Fortune, Atlanta United
41 Jordi Alba, Inter Miami CF
42 Brandon Vázquez, Austin FC
43 Christian Benteke, D.C. United
44 Alexey Miranchuk, Atlanta United
45 Lucho Acosta, FC Dallas
46 Liel Abada, Charlotte FC
47 Samuel Piette, CF Montréal
48 Cole Bassett, Colorado Rapids
49 Harbor Miller, LA Galaxy RC
50 Hugo Lloris, LAFC
51 Christopher Cupps, Chicago Fire RC
52 Walker Zimmerman, Nashville SC
53 Agustín Ojeda, New York City FC
54 Édier Ocampo, Vancouver Whitecaps FC RC
55 Nicolás Lodeiro, Houston Dynamo
56 Mohammed Sofo, New York Red Bulls RC
57 Tristan Brown, Columbus Crew RC
58 Bongokuhle Hlongwane, Minnesota United
59 Tim Ream, Charlotte FC
60 Kaká, Orlando City SC
61 Petar Musa, FC Dallas
62 Tani Oluwaseyi, Minnesota United
63 Miguel Almirón, Atlanta United
64 Kai Wagner, Philadelphia Union
65 Bastian Schweinsteiger, Chicago Fire
66 Nicolás Dubersarsky, Austin FC RC
67 Jacob Murrell, D.C. United RC
68 Son Heung-Min, LAFC
69 Cole Mrowka, Columbus Crew RC
70 Jonathan Osorio, Toronto FC
71 Dominik Chong Qui, Atlanta United RC
72 Tomás Avilés, Inter Miami CF
73 Matheus Nascimento, LA Galaxy RC
74 Luis Muriel, Orlando City SC
75 David Martínez, LAFC
76 David da Costa, Portland Timbers
77 Owen Wolff, Austin FC
78 Shapi Suleymanov, Sporting Kansas City
79 Jesús Ferreira, Seattle Sounders FC
80 Jonathan Shore, New York City FC RC
81 Sergio Oregel, Chicago Fire RC
82 Diogo Gonçalves, Real Salt Lake
83 Wiktor Bogacz, New York Red Bulls RC
84 Hristo Stoichkov, Chicago Fire
85 Alonso Martínez, New York City FC
86 Quinn Sullivan, Philadelphia Union
87 Kévin Denkey, FC Cincinnati RC
88 Sergio Busquets, Inter Miami CF
89 Brian Gutiérrez, Chicago Fire
90 Benjamín Cremaschi, Inter Miami CF
91 Bartosz Slisz, Atlanta United
92 Philip Zinckernagel, Chicago Fire
93 Riqui Puig, LA Galaxy
94 Omar Valencia, New York Red Bulls RC
95 Dejan Joveljić, Sporting Kansas City
96 Ilay Feingold, New England Revolution RC
97 Thomas Müller, Vancouver Whitecaps FC
98 Hannes Wolf, New York City FC
99 Denis Bouanga, LAFC
100 Carles Gil, New England Revolution
101 Idan Toklomati, Charlotte FC RC
102 Kei Kamara, FC Cincinnati
103 Kevin Kelsy, Portland Timbers
104 Taha Habroune, Columbus Crew RC
105 Tai Baribo, Philadelphia Union
106 Josef Martínez, San Jose Earthquakes
107 Telasco Segovia, Inter Miami CF RC
108 Anders Dreyer, San Diego FC
109 Gerardo Valenzuela, FC Cincinnati RC
110 Jozy Altidore, Toronto FC
111 Eric Maxim Choupo-Moting, New York Red Bulls
112 Maxi Moralez, New York City FC
113 Marco Pašalić, Orlando City SC
114 Joseph Paintsil, LA Galaxy
115 Dániel Gazdag, Columbus Crew
116 Ariath Piol, Real Salt Lake RC
117 Pep Biel, Charlotte FC
118 Kalani Kossa-Rienzi, Seattle Sounders FC RC
119 Evander, FC Cincinnati
120 Beau Leroux, San Jose Earthquakes RC
121 Dayne St. Clair, Minnesota United
122 DaMarcus Beasley, Houston Dynamo
123 Darlington Nagbe, Columbus Crew
124 Cobi Jones, LA Galaxy
125 Jordan Morris, Seattle Sounders FC
126 Onni Valakari, San Diego FC RC
127 Georgi Minoungou, Seattle Sounders FC RC
128 Luca de la Torre, San Diego FC
129 Alex Freeman, Orlando City SC RC
130 Anisse Saidi, San Diego FC RC
131 Didier Drogba, Montreal Impact
132 João Klauss, St. Louis City SC
133 Cristian Espinoza, San Jose Earthquakes
134 Rodrigo De Paul, Inter Miami CF
135 Chucky Lozano, San Diego FC
136 Luca Bombino, San Diego FC RC
137 Cristian Arango, San Jose Earthquakes
138 Osman Bukari, Austin FC
139 Brian White, Vancouver Whitecaps FC
140 Diego Chará, Portland Timbers
141 Jacob Shaffelburg, Nashville SC
142 Tate Johnson, Vancouver Whitecaps FC RC
143 Deandre Kerr, Toronto FC
144 Diego Rossi, Columbus Crew
145 Leonardo Barroso, Chicago Fire RC
146 Gustavo Caraballo, Orlando City SC RC
147 Max Arfsten, Columbus Crew
148 Pedrinho, FC Dallas RC
149 Diego Luna, Real Salt Lake
150 Clint Dempsey, Seattle Sounders FC
151 Gabriel Pec, LA Galaxy
152 Sam Surridge, Nashville SC
153 Emmanuel Latte Lath, Atlanta United RC
154 Andre Blake, Philadelphia Union
155 Ezequiel Ponce, Houston Dynamo
156 Bruno Damiani, Philadelphia Union RC
157 Antony, Portland Timbers
158 MyKhi Joyner, St. Louis City SC RC
159 Martín Ojeda, Orlando City SC
160 Finn Surman, Portland Timbers RC
161 Allen Obando, Inter Miami CF RC
162 Prince Owusu, CF Montréal
163 Zack Steffen, Colorado Rapids
164 Ahmed Qasem, Nashville SC RC
165 Robin Lod, Minnesota United
166 Pedro de la Vega, Seattle Sounders FC
167 Manu García, Sporting Kansas City
168 Marcel Hartel, St. Louis City SC
169 Seymour Reid, New York City FC RC
170 Sebastian Berhalter, Vancouver Whitecaps FC
171 Albert Rusnák, Seattle Sounders FC
172 Wilfried Zaha, Charlotte FC
173 Miles Robinson, FC Cincinnati
174 Myrto Uzuni, Austin FC
175 Jonathan Bamba, Chicago Fire

Base – Pitch Prodiges
25 cards

176 Cavan Sullivan, Philadelphia Union RC
177 Dominik Chong Qui, Atlanta United RC
178 Jonathan Shore, New York City FC RC
179 Matheus Nascimento, LA Galaxy RC
180 Georgi Minoungou, Seattle Sounders FC RC
181 Gustavo Caraballo, Orlando City SC RC
182 Leonardo Barroso, Chicago Fire RC
183 Igor Jesus, LAFC RC
184 Allen Obando, Inter Miami CF RC
185 Peyton Miller, New England Revolution RC
186 MyKhi Joyner, St. Louis City SC RC
187 Alex Freeman, Orlando City SC RC
188 Tristan Brown, Columbus Crew RC
189 Tate Johnson, Vancouver Whitecaps FC RC
190 Mohammed Sofo, New York Red Bulls RC
191 Aleksandr Guboglo, CF Montréal RC
192 Ahmed Qasem, Nashville SC RC
193 Kévin Denkey, FC Cincinnati RC
194 Ariath Piol, Real Salt Lake RC
195 Telasco Segovia, Inter Miami CF RC
196 Seymour Reid, New York City FC RC
197 Ilay Feingold, New England Revolution RC
198 Anisse Saidi, San Diego FC RC
199 Idan Toklomati, Charlotte FC RC
200 Kaick, FC Dallas RC

Base – Super Short Prints
2 cards
Parallels

Gold Refractor /50
Orange Refractor /25
Black Refractor /10
Red Refractor /5
Superfractor /1

68 Son Heung-Min, LAFC
154 Bob Marley

Chrome Autographs
97 cards
Parallels

Aqua Refractor /199
Aqua Wave /199 (Hobby Exclusive)
Blue Refractor /150
Blue Wave /150 (Hobby Exclusive)
Green Refractor /99
Green Wave /99 (Hobby Exclusive)
Pink X-Fractor /99 (Mania Exclusive)
Purple Refractor /75
Purple Wave /75 (Hobby Exclusive)
Gold Refractor /50
Gold Wave /50 (Hobby Exclusive)
Pink Shimmer /50 (Mania Exclusive)
Orange Refractor /25
Orange Wave /25 (Hobby Exclusive)
Pink Pulsar /25 (Mania Exclusive)
Black Refractor /10
Black Wave /10 (Hobby Exclusive)
Pink Refractor /10 (Mania Exclusive)
Red Refractor /5
Red Wave /5 (Hobby Exclusive)
Superfractor /1

CA-AA Alejandro Alvarado, San Diego FC
CA-AB Andre Blake, Philadelphia Union
CA-AD Anders Dreyer, San Diego FC
CA-AM Alexey Miranchuk, Atlanta United
CA-AP Ariath Piol, Real Salt Lake
CA-AQ Ahmed Qasem, Nashville SC
CA-AS Anisse Saidi, San Diego FC
CA-BC Benjamín Cremaschi, Inter Miami CF
CA-BD Bruno Damiani, Philadelphia Union
CA-BV Brandon Vázquez, Austin FC
CA-CA Cristian Arango, San Jose Earthquakes
CA-CB Christian Benteke, D.C. United
CA-CG Carles Gil, New England Revolution
CA-CM Cole Mrowka, Columbus Crew
CA-CQ Dominik Chong Qui, Atlanta United
CA-CS Cavan Sullivan, Philadelphia Union
CA-DB Denis Bouanga, LAFC
CA-DG Dániel Gazdag, Columbus Crew
CA-DL Diego Luna, Real Salt Lake
CA-DM David Martínez, LAFC
CA-DP Rodrigo De Paul, Inter Miami CF
CA-DR Diego Rossi, Columbus Crew
CA-EF Emil Forsberg, New York Red Bulls
CA-EL Emmanuel Latte Lath, Atlanta United
CA-EO Édier Ocampo, Vancouver Whitecaps FC
CA-ET Edvard Tagseth, Nashville SC
CA-FN Alex Freeman, Orlando City SC
CA-FS Finn Surman, Portland Timbers
CA-GC Gustavo Caraballo, Orlando City SC
CA-GM Georgi Minoungou, Seattle Sounders FC
CA-GP Gabriel Pec, LA Galaxy
CA-HC Hugo Cuypers, Chicago Fire
CA-HL Hugo Lloris, LAFC
CA-HM Hany Mukhtar, Nashville SC
CA-HS Son Heung-Min, LAFC
CA-IF Ilay Feingold, New England Revolution
CA-IT Idan Toklomati, Charlotte FC
CA-JA Jordi Alba, Inter Miami CF
CA-JB Jonathan Bamba, Chicago Fire
CA-JF Jesús Ferreira, Seattle Sounders FC
CA-JH Julian Hall, New York Red Bulls
CA-JM Jordan Morris, Seattle Sounders FC
CA-JS Jonathan Shore, New York City FC
CA-KD Kévin Denkey, FC Cincinnati
CA-KK Kaick, FC Dallas
CA-KR Kalani Kossa-Rienzi, Seattle Sounders FC
CA-KY Kelvin Yeboah, Minnesota United
CA-LA Lucho Acosta, FC Dallas
CA-LD Luca de la Torre, San Diego FC
CA-LI Lorenzo Insigne, Toronto FC
CA-LM Lionel Messi, Inter Miami CF
CA-LS Luis Suárez, Inter Miami CF
CA-LZ Chucky Lozano, San Diego FC
CA-MA Miguel Almirón, Atlanta United
CA-MG Manu García, Sporting Kansas City
CA-MH Marcel Hartel, St. Louis City SC
CA-MI Harbor Miller, LA Galaxy
CA-MJ MyKhi Joyner, St. Louis City SC
CA-ML Luis Muriel, Orlando City SC
CA-MP Marco Pašalić, Orlando City SC
CA-MR Marco Reus, LA Galaxy
CA-MS Mohammed Sofo, New York Red Bulls
CA-MT Josef Martínez, San Jose Earthquakes
CA-MU Petar Musa, FC Dallas
CA-MZ Alonso Martínez, New York City FC
CA-ND Nicolás Dubersarsky, Austin FC
CA-OB Osman Bukari, Austin FC
CA-OG Olivier Giroud, LAFC
CA-OL Tani Oluwaseyi, Minnesota United
CA-PD Pedro de la Vega, Seattle Sounders FC
CA-PE Pedrinho, FC Dallas
CA-PM Peyton Miller, New England Revolution
CA-QS Quinn Sullivan, Philadelphia Union
CA-RB Roman Bürki, St. Louis City SC
CA-RG Ryan Gauld, Vancouver Whitecaps FC
CA-RN Rafael Navarro, Colorado Rapids
CA-RO Miles Robinson, FC Cincinnati
CA-RP Riqui Puig, LA Galaxy
CA-SA Lucas Sanabria, LA Galaxy
CA-SB Sergio Busquets, Inter Miami CF
CA-SO Sergio Oregel, Chicago Fire
CA-SR Seymour Reid, New York City FC
CA-SZ Bartosz Slisz, Atlanta United
CA-TA Tadeo Allende, Inter Miami CF
CA-TB Tristan Brown, Columbus Crew
CA-TH Taha Habroune, Columbus Crew
CA-TJ Tate Johnson, Vancouver Whitecaps FC
CA-TM Thomas Müller, Vancouver Whitecaps FC
CA-TO Tai Baribo, Philadelphia Union
CA-TR Tim Ream, Charlotte FC
CA-TS Telasco Segovia, Inter Miami CF
CA-UZ Myrto Uzuni, Austin FC
CA-VK Onni Valakari, San Diego FC
CA-WB Wiktor Bogacz, New York Red Bulls
CA-WZ Wilfried Zaha, Charlotte FC
CA-ZM Zane Monlouis, Toronto FC
CA-ZN Walker Zimmerman, Nashville SC

Chrome Dual Autographs
13 cards
Parallels

Orange Refractor /25
Black Refractor /10
Red Refractor /5
Superfractor /1

DA-BS Son Heung-Min/Gareth Bale, LAFC
DA-FM Jesús Ferreira/Jordan Morris, Seattle Sounders FC
DA-GL Hugo Lloris/Olivier Giroud, LAFC
DA-HY Bongokuhle Hlongwane/Kelvin Yeboah, Minnesota United
DA-JC Josef Martínez/Cristian Arango, San Jose Earthquakes
DA-LA Miguel Almirón/Emmanuel Latte Lath, Atlanta United
DA-LD Anders Dreyer/Chucky Lozano, San Diego FC
DA-MD Lionel Messi/Rodrigo De Paul, Inter Miami CF
DA-MR Thomas Müller/Marco Reus, Vancouver Whitecaps FC/LA Galaxy
DA-RP Riqui Puig/Marco Reus, LA Galaxy
DA-SC Giorgio Chiellini/Luis Suárez, LAFC/Inter Miami CF
DA-SS Quinn Sullivan/Cavan Sullivan, Philadelphia Union
DA-ZN Nani/Wilfried Zaha, Orlando City SC/Charlotte FC

MLS Anniversary Autograph Booklet
1 card

AAB-1 Alessandro Nesta, Montreal Impact
AAB-1 Rafael Márquez, New York Red Bulls
AAB-1 Giorgio Chiellini, LAFC
AAB-1 Bastian Schweinsteiger, Chicago Fire
AAB-1 Andrea Pirlo, New York City FC
AAB-1 Steven Gerrard, LA Galaxy
AAB-1 Thierry Henry, New York Red Bulls
AAB-1 Zlatan Ibrahimović, LA Galaxy
AAB-1 Wayne Rooney, D.C. United
AAB-1 Tony Meola, New York MetroStars
AAB-1 Jeff Agoos, D.C. United
AAB-1 Cobi Jones, LA Galaxy
AAB-1 Taylor Twellman, New England Revolution
AAB-1 Chris Wondolowski, San Jose Earthquakes
AAB-1 Clint Dempsey, Seattle Sounders FC
AAB-1 Lothar Matthäus, New York MetroStars
AAB-1 Hristo Stoichkov, Chicago Fire
AAB-1 Kaká, Orlando City SC
AAB-1 Carlos Valderrama, Colorado Rapids
AAB-1 Preki, Kansas City Wizards
AAB-1 Marco Etcheverry, D.C. United
AAB-1 Carles Gil, New England Revolution
AAB-1 Hany Mukhtar, Nashville SC
AAB-1 Lucho Acosta, FC Dallas
AAB-1 Kévin Denkey, FC Cincinnati
AAB-1 Cavan Sullivan, Philadelphia Union
AAB-1 Telasco Segovia, Inter Miami CF
AAB-1 Lionel Messi, Inter Miami CF
AAB-1 Marco Reus, LA Galaxy
AAB-1 Son Heung-Min, LAFC

Topps 1995 Autographs
30 cards
Hobby Bonus Pack Exclusive
Parallels

Green Donut Holes /99
Purple Donut Holes /75
Gold Donut Holes /50
Pearl Donut Holes /30
Orange Donut Holes /25
Black Donut Holes /10
Red Donut Holes /5
Superfractor /1

NFA-AL Alexi Lalas, LA Galaxy
NFA-BM Brian McBride, Columbus Crew
NFA-BS Bastian Schweinsteiger, Chicago Fire
NFA-CD Clint Dempsey, Seattle Sounders FC
NFA-CJ Cobi Jones, LA Galaxy
NFA-CL Chucky Lozano, San Diego FC
NFA-CS Cavan Sullivan, Philadelphia Union
NFA-CV Carlos Valderrama, Colorado Rapids
NFA-DB Denis Bouanga, LAFC
NFA-DD Didier Drogba, Montreal Impact
NFA-DM DaMarcus Beasley, Houston Dynamo
NFA-DV David Villa, New York City FC
NFA-EP Eddie Pope, D.C. United
NFA-EW Eric Wynalda, San Jose Clash
NFA-FL Frank Lampard, New York City FC
NFA-GB Gareth Bale, LAFC
NFA-GC Giorgio Chiellini, LAFC
NFA-JA Jozy Altidore, Toronto FC
NFA-KB Kyle Beckerman, Real Salt Lake
NFA-KK Kaká, Orlando City SC
NFA-LM Lionel Messi, Inter Miami CF
NFA-LO Lothar Matthäus, New York MetroStars
NFA-LS Luis Suárez, Inter Miami CF
NFA-MA Miguel Almirón, Atlanta United
NFA-MR Marco Reus, LA Galaxy
NFA-NN Nani, Orlando City SC
NFA-TH Thierry Henry, New York Red Bulls
NFA-TT Taylor Twellman, New England Revolution
NFA-WZ Wilfried Zaha, Charlotte FC
NFA-ZI Zlatan Ibrahimović, LA Galaxy

MLS Renaissance Autographs
67 cards
Parallels

Gold /10
Ruby /5
Platinum /1

RA-AL1 Alessandro Nesta, Montreal Impact
RA-AM1 Alexey Miranchuk, Atlanta United
RA-AN1 Miguel Almirón, Atlanta United
RA-AN2 Miguel Almirón, Atlanta United
RA-AP1 Andrea Pirlo, New York City FC
RA-BC1 Benjamín Cremaschi, Inter Miami CF
RA-BM1 Blaise Matuidi, Inter Miami CF
RA-BS1 Bastian Schweinsteiger, Chicago Fire
RA-BV1 Brandon Vázquez, Austin FC
RA-CA1 Cristian Arango, San Jose Earthquakes
RA-CB1 Christian Benteke, D.C. United
RA-CB2 Christian Benteke, D.C. United
RA-CD1 Clint Dempsey, Seattle Sounders FC
RA-CS1 Cavan Sullivan, Philadelphia Union
RA-CS2 Cavan Sullivan, Philadelphia Union
RA-DB1 Denis Bouanga, LAFC
RA-DB2 Denis Bouanga, LAFC
RA-DD1 Didier Drogba, Montreal Impact
RA-DL1 Diego Luna, Real Salt Lake
RA-DR1 Diego Rossi, Columbus Crew
RA-EL1 Emmanuel Latte Lath, Atlanta United
RA-EV1 Evander, FC Cincinnati
RA-EV2 Evander, FC Cincinnati
RA-FL1 Frank Lampard, New York City FC
RA-GB1 Gareth Bale, LAFC
RA-GM1 Georgi Minoungou, Seattle Sounders FC
RA-GP1 Gabriel Pec, LA Galaxy
RA-GP2 Gabriel Pec, LA Galaxy
RA-HC1 Hugo Cuypers, Chicago Fire
RA-HM1 Hany Mukhtar, Nashville SC
RA-HM2 Hany Mukhtar, Nashville SC
RA-IT1 Idan Toklomati, Charlotte FC
RA-JF1 Jesús Ferreira, Seattle Sounders FC
RA-JM1 Josef Martínez, San Jose Earthquakes
RA-KD1 Kévin Denkey, FC Cincinnati
RA-KD2 Kévin Denkey, FC Cincinnati
RA-LI1 Lorenzo Insigne, Toronto FC
RA-LI2 Lorenzo Insigne, Toronto FC
RA-LL1 Hugo Lloris, LAFC
RA-LL2 Hugo Lloris, LAFC
RA-LM1 Lionel Messi, Inter Miami CF
RA-LM2 Lionel Messi, Inter Miami CF
RA-LS1 Luis Suárez, Inter Miami CF
RA-LS2 Luis Suárez, Inter Miami CF
RA-MA1 Alonso Martínez, New York City FC
RA-MJ1 MyKhi Joyner, St. Louis City SC
RA-ML1 Luis Muriel, Orlando City SC
RA-MR1 Marco Reus, LA Galaxy
RA-MR2 Marco Reus, LA Galaxy
RA-MS1 Mohammed Sofo, New York Red Bulls
RA-MU1 Petar Musa, FC Dallas
RA-OB1 Osman Bukari, Austin FC
RA-OG1 Olivier Giroud, LAFC
RA-PM1 Peyton Miller, New England Revolution
RA-RB1 Roman Bürki, St. Louis City SC
RA-RG1 Ryan Gauld, Vancouver Whitecaps FC
RA-RG2 Ryan Gauld, Vancouver Whitecaps FC
RA-RK1 Kaká, Orlando City SC
RA-RM1 Rafael Márquez, New York Red Bulls
RA-RN1 Rafael Navarro, Colorado Rapids
RA-SA1 Telasco Segovia, Inter Miami CF
RA-SB1 Sergio Busquets, Inter Miami CF
RA-TH1 Thierry Henry, New York Red Bulls
RA-TR1 Tim Ream, Charlotte FC
RA-WR1 Wayne Rooney, D.C. United
RA-ZI1 Zlatan Ibrahimović, LA Galaxy
RA-ZN1 Walker Zimmerman, Nashville SC

MLS Renaissance Autographed MLS Logo Patches
2 cards

AR-LM1 Lionel Messi, Inter Miami CF
AR-LM2 Lionel Messi, Inter Miami CF

Rookie Arrival Autographed Patches
1 card
Parallels

Black /14
Blue /5
Gold /1

API-CS Cavan Sullivan, Philadelphia Union

MLS Debut Patch Autographs
157 cards

DPA-AM Alexey Miranchuk, Atlanta United
DPA-BE Boris Enow, D.C. United
DPA-CT Cedric Teuchert, St. Louis City SC
DPA-DC Dylan Chambost, Columbus Crew
DPA-DG Diogo Gonçalves, Real Salt Lake
DPA-DJ Danley Jean Jacques, Philadelphia Union
DPA-EL Evan Louro, FC Cincinnati
DPA-EP Ezequiel Ponce, Houston Dynamo
DPA-JC Josh Cohen, Atlanta United
DPA-KK Kevin Kelsy, FC Cincinnati
DPA-KY Kelvin Yeboah, Minnesota United
DPA-LE Lawrence Ennali, Houston Dynamo
DPA-MD Mikkel Desler, Austin FC
DPA-MH Marcel Hartel, St. Louis City SC
DPA-MR Marco Reus, LA Galaxy
DPA-NH Nicholas Hagen, Columbus Crew
DPA-OB Osman Bukari, Austin FC
DPA-OG Olivier Giroud, LAFC
DPA-PB Pep Biel, Charlotte FC
DPA-BN Ola Brynhildsen, Toronto FC
DPA-BS Besard Sabovic, Austin FC
DPA-DA David da Costa, Portland Timbers
DPA-DR Anders Dreyer, San Diego FC
DPA-FO Mamadou Fofana, New England Revolution
DPA-HK Alexander Hack, New York Red Bulls
DPA-IG Ignatius Ganago, New England Revolution
DPA-JB Jonathan Bamba, Chicago Fire
DPA-JF Joaquín Fernández, Sporting Kansas City
DPA-JT Jeppe Tverskov, San Diego FC
DPA-LD Luca de la Torre, San Diego FC
DPA-MG Manu García, Sporting Kansas City
DPA-MI Marcus Ingvartsen, San Diego FC
DPA-MP Marco Pašalić, Orlando City SC
DPA-MU Myrto Uzuni, Austin FC
DPA-OS Oleksandr Svatok, Austin FC
DPA-OU Oscar Ustari, Inter Miami CF
DPA-OZ Joao Ortiz, Portland Timbers
DPA-PZ Philip Zinckernagel, Chicago Fire
DPA-RC Rafael Cabral, Real Salt Lake
DPA-RI Ramiro, FC Dallas
DPA-RS Kye Rowles, D.C. United
DPA-SU Shapi Suleymanov, Sporting Kansas City
DPA-UE Osaze Urhoghide, FC Dallas
DPA-VL Victor Loturi, CF Montréal
DPA-WZ Wilfried Zaha, Charlotte FC
DPA-ZA Zanka, LA Galaxy
RDPA-AD Andrew Rick, Philadelphia Union
RDPA-AE Adolfo Enriquez, Portland Timbers
RDPA-AH Andrés Herrera, Columbus Crew
RDPA-AL Antino Lopez, Seattle Sounders FC
RDPA-AS Alec Smir, Minnesota United
RDPA-BM Brendan McSorley, St. Louis City SC
RDPA-CG Emiro Garcés, LA Galaxy
RDPA-CH Charlie Sharp, Toronto FC
RDPA-CK Cyprian Kachwele, Vancouver Whitecaps FC
RDPA-CO Christopher Olney Jr., Philadelphia Union
RDPA-CS Cavan Sullivan, Philadelphia Union
RDPA-CW Cole Mrowka, Columbus Crew
RDPA-DB Dawid Bugaj, CF Montréal
RDPA-DI Marcos Dias, New England Revolution
RDPA-DS David Schnegg, D.C. United
RDPA-EM Efraín Morales, Atlanta United
RDPA-FA Forster Ajago, Nashville SC
RDPA-GB Giuseppe Bovalina, Vancouver Whitecaps FC
RDPA-GM Georgi Minoungou, Seattle Sounders FC
RDPA-GT Garrison Tubbs, D.C. United
RDPA-HB Hugo Bacharach, Minnesota United
RDPA-IF Isaiah Foster, FC Cincinnati
RDPA-JD Jefferson Díaz, Minnesota United
RDPA-JM Jimmy Farkarlun, Austin FC
RDPA-JO Javier Otero, Orlando City SC
RDPA-JR Justin Reynolds, Chicago Fire
RDPA-KR Kalani Kossa-Rienzi, Seattle Sounders FC
RDPA-LA London Aghedo, FC Cincinnati
RDPA-LL Luca Langoni, New England Revolution
RDPA-ME Matthew Edwards, Atlanta United
RDPA-MF Malcolm Fry, New England Revolution
RDPA-MJ MyKhi Joyner, St. Louis City SC
RDPA-MM Mohammed Sofo, New York Red Bulls
RDPA-MO Morris Duggan, Minnesota United
RDPA-MW Michael Wentzel, St. Louis City SC
RDPA-NF Nicolas Fleuriau Chateau, Vancouver Whitecaps FC
RDPA-NS Nick Scardina, Charlotte FC
RDPA-OJ Omar Valencia, New York Red Bulls
RDPA-PA Pedro Amador, Atlanta United
RDPA-PE Piero Elias, New York City FC
RDPA-PM Peyton Miller, New England Revolution
RDPA-RJ Kage Romanshyn Jr., Minnesota United
RDPA-RM Anthony Ramírez, FC Dallas
RDPA-RR Rubén Ramos Jr., LA Galaxy
RDPA-SJ Sawyer Jura, Portland Timbers
RDPA-TH Taha Habroune, Columbus Crew
RDPA-TL Tucker Lepley, LA Galaxy
RDPA-TM Tomas Pondeca, FC Dallas
RDPA-TP Tom Pearce, CF Montréal
RDPA-TS Tarik Scott, FC Dallas
RDPA-TY Tyger Smalls, Charlotte FC
RDPA-WF Wayne Frederick, Colorado Rapids
RDPA-YT Yutaro Tsukada, Orlando City SC
RDPA-AA Alhassan Yusuf, New England Revolution
RDPA-AB Adam Beaudry, Colorado Rapids
RDPA-AG Aleksandr Guboglo, CF Montréal
RDPA-AQ Ahmed Qasem, Nashville SC
RDPA-AR Abraham Romero, Columbus Crew
RDPA-AV Alejandro Alvarado, San Diego FC
RDPA-AW Femi Awodesu, Houston Dynamo
RDPA-BC Brayan Ceballos, New England Revolution
RDPA-BD Bruno Damiani, Philadelphia Union
RDPA-BH Belal Halbouni, Vancouver Whitecaps FC
RDPA-BL Beau Leroux, San Jose Earthquakes
RDPA-BT Jacob Bartlett, Sporting Kansas City
RDPA-BW Jeevan Badwal, Vancouver Whitecaps FC
RDPA-CC Markus Cimermancic, Toronto FC
RDPA-CQ Dominik Chong Qui, Atlanta United
RDPA-DD Derek Dodson, D.C. United
RDPA-EN Lukas Engel, FC Cincinnati
RDPA-EO Édier Ocampo, Vancouver Whitecaps FC
RDPA-ET Ervin Torres, Austin FC
RDPA-EU Emmanuel Latte Lath, Atlanta United
RDPA-EW Elijah Wynder, LA Galaxy
RDPA-FG Ilay Feingold, New England Revolution
RDPA-FS Finn Surman, Portland Timbers
RDPA-FW Francis Westfield, Philadelphia Union
RDPA-FY Jimer Fory, Portland Timbers
RDPA-GC Gustavo Caraballo, Orlando City SC
RDPA-GE Owen Gene, Minnesota United
RDPA-GF Gilberto Flores, FC Cincinnati
RDPA-GL Gonzalo Luján, Inter Miami CF
RDPA-HO Harold Osorio, Chicago Fire
RDPA-IP Ian Pilcher, San Diego FC
RDPA-IS Ian Smith, Portland Timbers
RDPA-IT Idan Toklomati, Charlotte FC
RDPA-JL Jovan Lukic, Philadelphia Union
RDPA-JP Joaquín Pereyra, Minnesota United
RDPA-JU Igor Jesus, LAFC
RDPA-KD Kévin Denkey, FC Cincinnati
RDPA-KJ Kim Joon-Hong, D.C. United
RDPA-KM Kenji Mboma Dem, FC Cincinnati
RDPA-LS Lucas Sanabria, LA Galaxy
RDPA-MK Olwethu Makhanya, Philadelphia Union
RDPA-NC Nico Cavallo, New York City FC
RDPA-ND Nicolás Dubersarsky, Austin FC
RDPA-NR Nicolás Rodríguez, Orlando City SC
RDPA-PO Pedrinho, FC Dallas
RDPA-RA Anderson Rosa, Colorado Rapids
RDPA-SC Stefan Chirila, FC Cincinnati
RDPA-SG Telasco Segovia, Inter Miami CF
RDPA-SH Jonathan Shore, New York City FC
RDPA-SR Sam Rogers, Chicago Fire
RDPA-SV Artem Smolyakov, LAFC
RDPA-TC Theo Corbeanu, Toronto FC
RDPA-TG Edvard Tagseth, Nashville SC
RDPA-VI Onni Valakari, San Diego FC
RDPA-WL Conrad Wallem, St. Louis City SC
RDPA-WM Wyatt Meyer, Nashville SC
RDPA-WS Sam Williams, Chicago Fire
RDPA-ZM Zane Monlouis, Toronto FC

MLS x Apple TV Patches Superfractors
60 cards

AP-LL Emmanuel Latte Lath, Atlanta United
AP-MA Miguel Almirón, Atlanta United
AP-BV Brandon Vázquez, Austin FC
AP-OB Osman Bukari, Austin FC
AP-PO Prince Owusu, CF Montréal
AP-SP Samuel Piette, CF Montréal
AP-TR Tim Ream, Charlotte FC
AP-WZ Wilfried Zaha, Charlotte FC
AP-HC Hugo Cuypers, Chicago Fire
AP-JB Jonathan Bamba, Chicago Fire
AP-DM Djordje Mihailovic, Colorado Rapids
AP-NO Rafael Navarro, Colorado Rapids
AP-DR Diego Rossi, Columbus Crew
AP-RR Jacen Russell-Rowe, Columbus Crew
AP-CB Christian Benteke, D.C. United
AP-PI Gabriel Pirani, D.C. United
AP-EV Evander, FC Cincinnati
AP-RN Miles Robinson, FC Cincinnati
AP-LA Lucho Acosta, FC Dallas
AP-PM Petar Musa, FC Dallas
AP-EP Ezequiel Ponce, Houston Dynamo
AP-MN Jack McGlynn, Houston Dynamo
AP-BC Benjamín Cremaschi, Inter Miami CF
AP-LS Luis Suárez, Inter Miami CF
AP-GP Gabriel Pec, LA Galaxy
AP-MR Marco Reus, LA Galaxy
AP-AL Aaron Long, LAFC
AP-DB Denis Bouanga, LAFC
AP-BH Bongokuhle Hlongwane, Minnesota United
AP-KY Kelvin Yeboah, Minnesota United
AP-HM Hany Mukhtar, Nashville SC
AP-ZN Walker Zimmerman, Nashville SC
AP-CG Carles Gil, New England Revolution
AP-LU Luca Langoni, New England Revolution
AP-EF Emil Forsberg, New York Red Bulls
AP-EC Eric Maxim Choupo-Moting, New York Red Bulls
AP-MZ Alonso Martínez, New York City FC
AP-TM Thiago Martins, New York City FC
AP-ML Luis Muriel, Orlando City SC
AP-MP Marco Pašalić, Orlando City SC
AP-CS Cavan Sullivan, Philadelphia Union
AP-DG Dániel Gazdag, Philadelphia Union
AP-DC David da Costa, Portland Timbers
AP-FM Felipe Mora, Portland Timbers
AP-DL Diego Luna, Real Salt Lake
AP-GS Diogo Gonçalves, Real Salt Lake
AP-HL Chucky Lozano, San Diego FC
AP-LD Luca de la Torre, San Diego FC
AP-JM Josef Martínez, San Jose Earthquakes
AP-CA Cristian Arango, San Jose Earthquakes
AP-AR Albert Rusnák, Seattle Sounders FC
AP-JF Jesús Ferreira, Seattle Sounders FC
AP-DJ Dejan Joveljić, Sporting Kansas City
AP-ET Erik Thommy, Sporting Kansas City
AP-EL Eduard Löwen, St. Louis City SC
AP-MH Marcel Hartel, St. Louis City SC
AP-JO Jonathan Osorio, Toronto FC
AP-LI Lorenzo Insigne, Toronto FC
AP-BW Brian White, Vancouver Whitecaps FC
AP-RG Ryan Gauld, Vancouver Whitecaps FC
"""

# Sections to merge into a single base section
BASE_MERGE_SECTIONS = {"Base Set", "Base – Pitch Prodiges", "Base – Super Short Prints"}
BASE_SECTION_NAME = "Base Set Checklist"

# Lines to skip as descriptor/marketing text (checked before AND during parallels)
DESCRIPTOR_PATTERNS = [
    r"^hobby exclusive",
    r"^hobby bonus pack",
    r"^\d+ per hobby",
    r"^mania box exclusive",
    r"^value box exclusive",
    r"^shop for",
]


def is_descriptor(line):
    low = line.lower().strip()
    return any(re.match(p, low) for p in DESCRIPTOR_PATTERNS)


def parse_print_run(text):
    """Extract serialized print run. Returns None for unlimitied or negative values."""
    m = re.search(r"/(-?\d+)", text)
    if m:
        n = int(m.group(1))
        return n if n > 0 else None
    return None


def parse_parallel_name(text):
    """Return clean parallel name: strip /N suffix and parenthetical descriptions."""
    name = re.sub(r"\s*\([^)]*\)", "", text)   # strip parentheticals
    name = re.sub(r"\s*/[-]?\d+.*", "", name)  # strip /N suffix
    return name.strip()


def parse_section(lines, start_idx):
    """
    Parse a section starting at start_idx (the section name line).
    Returns (section_data, next_idx).
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

        # Skip "Shop for" and descriptor lines throughout
        if is_descriptor(line):
            idx += 1
            continue

        if line.lower() in ("parallels", "parallel"):
            in_parallels = True
            idx += 1
            continue

        if in_parallels:
            # Card line → end of parallels block
            if re.match(r"^[A-Z0-9]+-[A-Z0-9]+\s|^\d+\s", line):
                break
            # Otherwise treat as a parallel entry
            parallels.append({
                "name": parse_parallel_name(line),
                "print_run": parse_print_run(line),
            })
            idx += 1
        else:
            # Not yet in parallels; if we see a card line start reading cards
            if re.match(r"^[A-Z0-9]+-[A-Z0-9]+\s|^\d+\s", line):
                break
            # Anything else before "Parallels" keyword that isn't a descriptor → stop
            # (this handles unexpected lines between count and parallels)
            break

    # Parse cards
    cards = []
    while idx < len(lines):
        line = lines[idx].strip()

        if not line:
            idx += 1
            continue

        # Skip descriptor / marketing lines
        if is_descriptor(line) or line.lower().startswith("shop for"):
            idx += 1
            continue

        # Detect start of next section (line followed by "N cards")
        if idx + 1 < len(lines) and re.match(r"^\d+ cards?$", lines[idx + 1].strip()):
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

            # Subset tag in parentheses at end
            subset_tag = None
            subset_m = re.search(r"\(([^)]+)\)$", rest)
            if subset_m:
                subset_tag = subset_m.group(1)
                rest = rest[: subset_m.start()].strip()

            # Split player and team at last comma
            if "," in rest:
                comma_idx = rest.rfind(",")
                player = rest[:comma_idx].strip()
                team = rest[comma_idx + 1 :].strip()
            else:
                player = rest
                team = ""

            cards.append({
                "card_number": card_number,
                "player": player,
                "team": team,
                "is_rookie": is_rookie,
                "subset": subset_tag,
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

        # Section header detected by "N cards" on next non-empty line
        # Peek ahead (skip blank lines)
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
    # Merge base sections into "Base Set Checklist"
    base_parallels = []
    base_cards = []
    other_sections = []

    for s in sections:
        if s["insert_set"] in BASE_MERGE_SECTIONS:
            if s["insert_set"] == "Base Set":
                base_parallels = s["parallels"]
            base_cards.extend(s["cards"])
        else:
            other_sections.append(s)

    merged_sections = []
    if base_cards:
        merged_sections.append({
            "insert_set": BASE_SECTION_NAME,
            "parallels": base_parallels,
            "cards": base_cards,
        })
    merged_sections.extend(other_sections)

    # Collect all players who are rookies in any section (propagate to all appearances)
    rc_players = set()
    for section in merged_sections:
        for card in section["cards"]:
            if card.get("is_rookie"):
                for name in (p.strip() for p in card["player"].split("/")):
                    rc_players.add(name)

    # Build player index
    # For dual autographs (player name contains "/"), split into individual players.
    # Team field may also use "/" to pair teams; otherwise both share the same team.
    player_index = {}
    for section in merged_sections:
        for card in section["cards"]:
            if "/" in card["player"]:
                player_names = [p.strip() for p in card["player"].split("/")]
                team_parts = [t.strip() for t in card["team"].split("/")] if "/" in card["team"] else None
                for i, player_name in enumerate(player_names):
                    team = team_parts[i] if team_parts and i < len(team_parts) else card["team"]
                    if player_name not in player_index:
                        player_index[player_name] = {"player": player_name, "appearances": []}
                    player_index[player_name]["appearances"].append({
                        "insert_set": section["insert_set"],
                        "card_number": card["card_number"],
                        "team": team,
                        "is_rookie": player_name in rc_players,
                        "subset_tag": card["subset"],
                        "parallels": section["parallels"],
                    })
            else:
                player = card["player"]
                if player not in player_index:
                    player_index[player] = {"player": player, "appearances": []}
                player_index[player]["appearances"].append({
                    "insert_set": section["insert_set"],
                    "card_number": card["card_number"],
                    "team": card["team"],
                    "is_rookie": player in rc_players,
                    "subset_tag": card["subset"],
                    "parallels": section["parallels"],
                })

    # Build final player list with stats
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
        "set_name": "2025 Topps Chrome MLS",
        "sport": "Soccer",
        "season": "2025",
        "league": "MLS",
        "sections": merged_sections,
        "players": players,
    }


if __name__ == "__main__":
    print("Parsing 2025 Topps Chrome MLS checklist...")
    sections = parse_checklist(CHECKLIST_TEXT)
    print(f"Raw sections found: {len(sections)}")

    output = build_output(sections)

    with open("mls_chrome_parsed.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nSet: {output['set_name']} ({output['season']})")
    print(f"Sections: {len(output['sections'])}")
    for s in output["sections"]:
        print(f"  {s['insert_set']}: {len(s['cards'])} cards, {len(s['parallels'])} parallels")
    print(f"Players: {len(output['players'])}")

    if "Lionel Messi" in {p["player"] for p in output["players"]}:
        messi = next(p for p in output["players"] if p["player"] == "Lionel Messi")
        print(f"\n=== Lionel Messi ===")
        print(f"  Insert sets:       {messi['stats']['insert_sets']}")
        print(f"  Unique cards:      {messi['stats']['unique_cards']}")
        print(f"  Total print run:   {messi['stats']['total_print_run']}")
        print(f"  1/1s:              {messi['stats']['one_of_ones']}")
        for a in messi["appearances"]:
            print(f"  {a['insert_set']} — {a['card_number']} ({len(a['parallels'])} parallels)")

    print(f"\nSaved to mls_chrome_parsed.json")
