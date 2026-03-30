import json

# ─────────────────────────────────────────────────────────────
# Parallel definitions
# ─────────────────────────────────────────────────────────────

BASE_PARALLELS = [
    {"name": "Refractor",       "print_run": None},
    {"name": "Magenta",         "print_run": None},
    {"name": "Negative",        "print_run": None},
    {"name": "Prism",           "print_run": None},
    {"name": "Purple",          "print_run": None},
    {"name": "Sepia",           "print_run": None},
    {"name": "X-Fractor",       "print_run": None},
    {"name": "Speckle",         "print_run": 299},
    {"name": "Aqua",            "print_run": 199},
    {"name": "Blue",            "print_run": 150},
    {"name": "Green",           "print_run": 99},
    {"name": "Blue Wave",       "print_run": 75},
    {"name": "Gold",            "print_run": 50},
    {"name": "Orange",          "print_run": 25},
    {"name": "Black",           "print_run": 10},
    {"name": "Red",             "print_run": 5},
    {"name": "Superfractor",    "print_run": 1},
]

AUTO_PAR_REFRACTOR_NUMBERED = [
    {"name": "Refractor",    "print_run": 150},
    {"name": "Gold",         "print_run": 50},
    {"name": "Orange",       "print_run": 25},
    {"name": "Black",        "print_run": 10},
    {"name": "Red",          "print_run": 5},
    {"name": "Superfractor", "print_run": 1},
]

AUTO_PAR_REFRACTOR_UNNUMBERED = [
    {"name": "Refractor",    "print_run": None},
    {"name": "Gold",         "print_run": 50},
    {"name": "Orange",       "print_run": 25},
    {"name": "Black",        "print_run": 10},
    {"name": "Red",          "print_run": 5},
    {"name": "Superfractor", "print_run": 1},
]

YQS_PAR = [
    {"name": "Superfractor", "print_run": 1},
]

INSERT_PAR_WITH_REF = [
    {"name": "Refractor",    "print_run": None},
    {"name": "Gold",         "print_run": 50},
    {"name": "Black",        "print_run": 10},
    {"name": "Red",          "print_run": 5},
    {"name": "Superfractor", "print_run": 1},
]

INSERT_PAR_NO_REF = [
    {"name": "Gold",         "print_run": 50},
    {"name": "Black",        "print_run": 10},
    {"name": "Red",          "print_run": 5},
    {"name": "Superfractor", "print_run": 1},
]

SUPERFRACTOR_ONLY = [
    {"name": "Superfractor", "print_run": 1},
]

# ─────────────────────────────────────────────────────────────
# Name normalizations
# ─────────────────────────────────────────────────────────────

NAME_FIXES = {
    "Alexsandar Rakic":  "Aleksandar Rakic",
    "Dricus DU Plessis": "Dricus Du Plessis",
    "Movsar Evolev":     "Movsar Evloev",
    "Volkanovksi":       "Volkanovski",
}


def fix_name(name):
    return NAME_FIXES.get(name, name)


# ─────────────────────────────────────────────────────────────
# Raw checklist data
# ─────────────────────────────────────────────────────────────

BASE_SET_RAW = """
1 Brad Katona RC
2 Adrian Yanez
3 Brunno Ferreira RC
4 Alex Pereira
5 Alex Perez
6 Alexa Grasso
7 Alexander Volkanovski
8 Alexander Volkov
9 Alexandr Romanov
10 Alexandre Pantoja
11 Alexsandar Rakic
12 Aljamain Sterling
13 Allan Nascimento
14 Amanda Lemos
15 Amanda Nunes
16 Amir Albazi
17 Anderson Silva
18 Anshul Jubli
19 Anthony Smith
20 Arman Tsarukyan
21 Da'Mon Blackshear RC
22 Arnold Allen
23 Azamat Murzakanov
24 Belal Muhammad
25 Beneil Dariush
26 Diego Lopes RC
27 Bill Algeo
28 Blagoy Ivanov
29 Elves Brener RC
30 Brandon Moreno
31 Brandon Royval
32 Brendan Allen
33 Brian Ortega
34 Jamie Pickett RC
35 Fernando Padilla RC
36 Bryce Mitchell
37 Calvin Kattar
38 Gabriel Miranda RC
39 Carla Esparza
40 Carlston Harris
41 Chan Sung Jung
42 Charles Oliveira
43 Iasmin Lucindo RC
44 Chris Gutierrez
45 Jake Hadley RC
46 Chuck Liddell
47 Ciryl Gane
48 Colby Covington
49 Conor McGregor
50 Cory Sandhagen
51 Curtis Blaydes
52 Damir Ismagulov
53 Ludovit Klein
54 Dan Hooker
55 Dan Ige
56 Daniel Cormier
57 Deiveson Figueiredo
58 Cody Garbrandt
59 Derrick Lewis
60 Dominick Cruz
61 Dominick Reyes
62 Dricus Du Plessis
63 Dusko Todorovic
64 Dustin Poirier
65 Erin Blanchfield
66 Montserrat Conejo RC
67 Geoff Neal
68 Georges St-Pierre
69 Giga Chikadze
70 Gilbert Burns
71 Grant Dawson
72 Jonny Parsons RC
73 Henry Cejudo
74 Holly Holm
75 Ian Machado Garry
76 Josh Quinlan RC
77 Ilia Topuria
78 Irene Aldana
79 Irina Alekseeva
80 Islam Makhachev
81 Israel Adesanya
82 Jack Della Maddalena
83 Jack Hermansson
84 Jack Jenkins
85 Jacob Malkoun
86 Jailton Almeida
87 Jair Rozenstruik
88 Jalin Turner
89 Jamahal Hill
90 Jamall Emmers
91 Jan Błachowicz
92 Jared Cannonier
93 Luana Carolina RC
94 Jessica Andrade
95 Jiri Prochazka
96 Johnny Walker
97 Jon Jones
98 Melquizael Conceição RC
99 Joselyne Edwards
100 Josh Emmett
101 Joshua Culibao
102 Julianna Peña
103 Ariane Lipski
104 Justin Gaethje
105 Justin Tafa
106 Kai Kara-France
107 Katlyn Cerminara
108 Kamaru Usman
109 Ottman Azaitar
110 Kelvin Gastelum
111 Ketlen Vieira
112 Khabib Nurmagomedov
113 Khalil Rountree Jr.
114 Khamzat Chimaev
115 Leon Edwards
116 Inoue Mizuki RC
117 Mackenzie Dern
118 Magomed Ankalaev
119 Manel Kape
120 Manon Fiorot
121 Manuel Torres
122 Marcin Tybura
123 Marcos Rogério De Lima
124 Marlon Vera
125 Marvin Vettori
126 Mateusz Gamrot
127 Mateusz Rebecki
128 Matheus Nicolau
129 Matt Schnell
130 Shogun Rua
131 Max Holloway
132 Maycee Barber
133 Ode Osbourne RC
134 Melissa Gatto
135 Merab Dvalishvili
136 Michael Chandler
137 Michael Chiesa
138 Michel Pereira
139 Mike Davis
140 Miles Johns
141 Shara Magomedov RC
142 Parker Porter RC
143 Movsar Evloev
144 Muhammad Mokaev
145 Nassourdine Imavov
146 Natalia Cristina da Silva
147 Choi SeungWoo RC
148 Neil Magny
149 Nicolas Dalby
150 Nikita Krylov
151 Paddy Pimblett
152 Pannie Kianzad
153 Paul Craig
154 Paulo Costa
155 Pedro Munhoz
156 Petr Yan
157 Rafa Garcia
158 Rafael Dos Anjos
159 Rafael Fiziev
160 Raquel Pennington
161 Raul Rosas
162 Renato Moicano
163 Ricky Simon
164 Rob Font
165 Robbie Lawler
166 Rodrigo Nascimento
167 Roman Dolidze
168 Alonzo Menifield
169 Rose Namajunas
170 Royce Gracie
171 Ryan Spann
172 Sean Brady
173 Sean O'Malley
174 Sean Strickland
175 Sergei Pavlovich
176 Serghei Spivac
177 Shavkat Rakhmonov
178 Sodiq Yusuff
179 Yadong Song
180 Stephen Thompson
181 Stipe Miocic
182 Shayilan Nuerdanbieke RC
183 Tai Tuivasa
184 Taila Santos
185 Tim Elliott
186 Tito Ortiz
187 Tom Aspinall
188 Themba Gorimbo RC
189 Umar Nurmagomedov
190 Valentina Shevchenko
191 Vanessa Demopoulos
192 Vicente Luque
193 Val Woodburn RC
194 Virna Jandiroba
195 Volkan Oezdemir
196 Malcolm Gordon RC
197 Yair Rodríguez
198 Yan Xiaonan
199 William Gomis RC
200 Zhang Weili
"""

CHROME_ROOKIE_AUTOS_RAW = """
CRA-BKA Brad Katona
CRA-DLO Diego Lopes
CRA-DMB Da'Mon Blackshear
CRA-EBR Elves Brener
CRA-FPA Fernando Padilla
CRA-GMI Gabriel Miranda
CRA-ILU Iasmin Lucindo
CRA-JHA Jake Hadley
CRA-JJE Jack Jenkins
CRA-JPA Jonny Parsons
CRA-JQU Josh Quinlan
CRA-JTA Junior Tafa
CRA-LCA Luana Carolina
CRA-MCO Melquizael Conceição
CRA-MIN Inoue Mizuki
CRA-MKA Manel Kape
CRA-NSI Natalia Cristina da Silva
CRA-OOS Ode Osbourne
CRA-PPO Parker Porter
CRA-SNU Nuerdanbieke Shayilan
CRA-SWC Choi SeungWoo
CRA-TGO Themba Gorimbo
CRA-VWO Val Woodburn
CRA-WGO William Gomis
"""

CHROME_VETERAN_AUTOS_RAW = """
CVA-ARA Aleksandar Rakic
CVA-AVO Alexander Volkov
CVA-BAL Brendan Allen
CVA-BBA Bryan Battle
CVA-BDA Beneil Dariush
CVA-BOR Brian Ortega
CVA-BRO Brandon Royval
CVA-CBO Caio Borralho
CVA-CES Carla Esparza
CVA-CSA Cory Sandhagen
CVA-CUL Carlos Ulberg
CVA-DBR Derek Brunson
CVA-DRE Dominick Reyes
CVA-GNE Geoff Neal
CVA-IAL Irene Aldana
CVA-JAN Jessica Andrade
CVA-JHI Jamahal Hill
CVA-JJE Joanna Jędrzejczyk
CVA-JPE Julianna Peña
CVA-JPY Joe Pyfer
CVA-JWA Johnny Walker
CVA-KCH Katlyn Cerminara
CVA-MBA Maycee Barber
CVA-MCH Michael Chandler
CVA-MDV Merab Dvalishvili
CVA-MMA Mike Malott
CVA-MMO Michael Morales
CVA-MTY Marcin Tybura
CVA-MVE Marlon Vera
CVA-NLE Natan Levy
CVA-PYA Petr Yan
CVA-RDA Rafael Dos Anjos
CVA-RFO Rob Font
CVA-RPE Raquel Pennington
CVA-RSP Ryan Spann
CVA-SSP Serghei Spivac
CVA-VLU Vicente Luque
CVA-VOE Volkan Oezdemir
"""

FUTURE_STARS_AUTOS_RAW = """
FSA-AAL Arnold Allen
FSA-APE Alex Pereira
FSA-DDP Dricus Du Plessis
FSA-EBL Erin Blanchfield
FSA-IGA Ian Machado Garry
FSA-JAL Jailton Almeida
FSA-JDM Jack Della Maddalena
FSA-JSH Jack Shore
FSA-KCH Khamzat Chimaev
FSA-MAN Magomed Ankalaev
FSA-MEV Movsar Evloev
FSA-MMO Muhammad Mokaev
FSA-PPI Paddy Pimblett
FSA-RRO Raul Rosas
FSA-SRA Shavkat Rakhmonov
FSA-TAS Tom Aspinall
FSA-TRI Tabatha Ricci
FSA-TSU Tatiana Suarez
FSA-TTA Tatsuro Taira
FSA-UNU Umar Nurmagomedov
"""

HALL_OF_FAME_AUTOS_RAW = """
HFA-BRU Bas Rutten
HFA-CLI Chuck Liddell
HFA-DCE Donald Cerrone
HFA-FGR Forrest Griffin
HFA-KSH Ken Shamrock
HFA-MBI Michael Bisping
HFA-MCO Mark Coleman
HFA-MHU Matt Hughes
HFA-MSE Matt Serra
HFA-RFR Rich Franklin
HFA-RGR Royce Gracie
HFA-TOR Tito Ortiz
HFA-UFA Urijah Faber
"""

MAIN_EVENT_AUTOS_RAW = """
MEA-AGR Alexa Grasso
MEA-APA Alexandre Pantoja
MEA-AST Aljamain Sterling
MEA-AVO Alexander Volkanovski
MEA-BLE Brock Lesnar
MEA-CCO Colby Covington
MEA-COL Charles Oliveira
MEA-DPO Dustin Poirier
MEA-GBU Gilbert Burns
MEA-GTE Glover Teixeira
MEA-JBL Jan Błachowicz
MEA-JGA Justin Gaethje
MEA-JPR Jiri Prochazka
MEA-MHO Max Holloway
MEA-RNA Rose Namajunas
MEA-RWH Robert Whittaker
MEA-SOM Sean O'Malley
MEA-VSH Valentina Shevchenko
"""

MARKS_OF_CHAMPIONS_AUTOS_RAW = """
MOC-ANU Amanda Nunes
MOC-AST Aljamain Sterling
MOC-BMO Brandon Moreno
MOC-DCO Daniel Cormier
MOC-GSP Georges St-Pierre
MOC-HCE Henry Cejudo
MOC-IAD Israel Adesanya
MOC-IMA Islam Makhachev
MOC-KNU Khabib Nurmagomedov
MOC-LED Leon Edwards
MOC-SMI Stipe Miocic
MOC-ZWE Zhang Weili
"""

OCTAGON_LEGENDS_AUTOS_RAW = """
OLA-AAR Andrei Arlovski
OLA-ARN Antonio Rodrigo Nogueira
OLA-BRU Bas Rutten
OLA-CSO Chael Sonnen
OLA-CWE Chris Weidman
OLA-DCR Dominick Cruz
OLA-DHE Dan Henderson
OLA-FED Frankie Edgar
OLA-FMI Frank Mir
OLA-FSH Frank Shamrock
OLA-JDS Junior dos Santos
OLA-JPU Jens Pulver
OLA-LMA Lyoto Machida
OLA-REV Rashad Evans
OLA-RLA Robbie Lawler
OLA-TFE Tony Ferguson
OLA-TWO Tyron Woodley
"""

UFC_SIGNATURES_RAW = """
FNA-AAL Amir Albazi
FNA-ASM Anthony Smith
FNA-BMU Belal Muhammad
FNA-CBL Curtis Blaydes
FNA-CGA Ciryl Gane
FNA-CKA Calvin Kattar
FNA-CSJ Chan Sung Jung
FNA-DHO Dan Hooker
FNA-DIG Dan Ige
FNA-GCH Giga Chikadze
FNA-HHO Holly Holm
FNA-JEM Josh Emmett
FNA-JTU Jalin Turner
FNA-KHO Kevin Holland
FNA-KKF Kai Kara-France
FNA-MDE Mackenzie Dern
FNA-MGA Mateusz Gamrot
FNA-MMC Molly McCann
FNA-MNI Matheus Nicolau
FNA-MVE Marvin Vettori
FNA-NMA Neil Magny
FNA-PMU Pedro Munhoz
FNA-RFI Rafael Fiziev
FNA-STH Stephen Thompson
FNA-SYA Yadong Song
FNA-TSA Taila Santos
FNA-TTU Tai Tuivasa
FNA-YRO Yair Rodríguez
FNA-YXI Yan Xiaonan
"""

YOUTHQUAKE_SIGNATURES_RAW = """
YQS-AAL Arnold Allen /10
YQS-DDP Dricus Du Plessis /10
YQS-EBL Erin Blanchfield /10
YQS-JDM Jack Della Maddalena /10
YQS-MMO Muhammad Mokaev /10
YQS-RRO Raul Rosas /10
YQS-SRA Shavkat Rakhmonov /10
YQS-TTA Tatsuro Taira /10
"""

TOPPS_1954_RAW = """
FFT-1 Georges St-Pierre
FFT-2 Royce Gracie
FFT-3 Valentina Shevchenko
FFT-4 Donald Cerrone
FFT-5 Tito Ortiz
FFT-6 Don Frye
FFT-7 Stipe Miocic
FFT-8 Islam Makhachev
FFT-9 Max Holloway
FFT-10 Forrest Griffin
FFT-11 Tony Ferguson
FFT-12 Lyoto Machida
FFT-13 Michael Bisping
FFT-14 Dominick Cruz
FFT-15 Chael Sonnen
FFT-16 Robbie Lawler
FFT-17 Rich Franklin
FFT-18 Dan Henderson
FFT-19 Angela Hill
FFT-20 Amanda Nunes
FFT-21 Khabib Nurmagomedov
FFT-22 Rashad Evans
FFT-23 Charles Oliveira
FFT-24 Joanna Jędrzejczyk
FFT-25 Henry Cejudo
"""

AKA_RAW = """
AKA-1 Deiveson Figueiredo – "Deus da Guerra"
AKA-2 Chuck Liddell – "The Iceman"
AKA-3 Lyoto Machida – "The Dragon"
AKA-4 Shogun Rua – "Shogun"
AKA-5 Rose Namajunas – "Thug"
AKA-6 Israel Adesanya – "The Last Stylebender"
AKA-7 Robert Whittaker – "The Reaper"
AKA-8 Conor McGregor – "The Notorious"
AKA-9 Robbie Lawler – "Ruthless"
AKA-10 Kamaru Usman – "Nigerian Nightmare"
AKA-11 Jon Jones – "Bones"
AKA-12 Stephen Thompson – "Wonderboy"
AKA-13 Chan Sung Jung – "The Korean Zombie"
AKA-14 Donald Cerrone – "Cowboy"
AKA-15 Alexander Volkanovski – "The Great"
AKA-16 Paddy Pimblett – "The Baddy"
AKA-17 Valentina Shevchenko – "Bullet"
AKA-18 Tai Tuivasa – "Bam Bam"
AKA-19 Anderson Silva – "The Spider"
AKA-20 Urijah Faber – "The California Kid"
"""

ALL_THE_GLORY_RAW = """
ATG-1 Michael Chandler
ATG-2 Bo Nickal
ATG-3 Alexa Grasso
ATG-4 Jon Jones
ATG-5 Israel Adesanya
ATG-6 Amanda Nunes
ATG-7 Joanna Jędrzejczyk
ATG-8 Ilia Topuria
ATG-9 Khabib Nurmagomedov
ATG-10 Robbie Lawler
ATG-11 Robert Whittaker
ATG-12 Jake Hadley
ATG-13 Conor McGregor
ATG-14 Islam Makhachev
ATG-15 Urijah Faber
"""

ALLEN_AND_GINTER_RAW = """
AAG-1 Alexandre Pantoja
AAG-2 Jon Jones
AAG-3 Khabib Nurmagomedov
AAG-4 Alexander Volkanovski
AAG-5 Aljamain Sterling
AAG-6 Glover Teixeira
AAG-7 Israel Adesanya
AAG-8 Amanda Nunes
AAG-9 Conor McGregor
AAG-10 Robert Whittaker
AAG-11 Islam Makhachev
AAG-12 Roman Dolidze
AAG-13 Donald Cerrone
AAG-14 Elves Brener
AAG-15 Alex Pereira
AAG-16 Max Holloway
AAG-17 Georges St-Pierre
AAG-18 Colby Covington
AAG-19 Mackenzie Dern
AAG-20 Dominick Cruz
AAG-21 Chuck Liddell
AAG-22 Khamzat Chimaev
AAG-23 Sean O'Malley
AAG-24 Tatiana Suarez
AAG-25 Anderson Silva
AAG-26 Stipe Miocic
AAG-27 Kamaru Usman
AAG-28 Iasmin Lucindo
AAG-29 Daniel Cormier
AAG-30 Valentina Shevchenko
"""

BRICK_BY_BRICK_RAW = """
BYB-1 Tom Aspinall
BYB-2 Ilia Topuria
BYB-3 Rafael Fiziev
BYB-4 Muhammad Mokaev
BYB-5 Maycee Barber
BYB-6 Umar Nurmagomedov
BYB-7 Ian Machado Garry
BYB-8 Movsar Evloev
BYB-9 Arnold Allen
BYB-10 Jailton Almeida
BYB-11 Shavkat Rakhmonov
BYB-12 Bo Nickal
BYB-13 Paddy Pimblett
BYB-14 Arman Tsarukyan
BYB-15 Manon Fiorot
BYB-16 Khamzat Chimaev
BYB-17 Dricus Du Plessis
BYB-18 Erin Blanchfield
BYB-19 Grant Dawson
BYB-20 Sean O'Malley
"""

COUNTDOWN_RAW = """
COU-1 Kamaru Usman
COU-2 Shavkat Rakhmonov
COU-3 Paul Craig
COU-4 Islam Makhachev
COU-5 Gilbert Burns
COU-6 Sean O'Malley
COU-7 Jared Cannonier
COU-8 Robbie Lawler
COU-9 Colby Covington
COU-10 Ciryl Gane
COU-11 Derrick Lewis
COU-12 Sean Strickland
COU-13 Johnny Walker
COU-14 Amanda Nunes
COU-15 Robert Whittaker
COU-16 Tito Ortiz
COU-17 Valentina Shevchenko
COU-18 Conor McGregor
COU-19 Ken Shamrock
COU-20 Dan Henderson
COU-21 Forrest Griffin
COU-22 Brandon Moreno
COU-23 Israel Adesanya
COU-24 Max Holloway
COU-25 Brian Ortega
COU-26 Mackenzie Dern
COU-27 Rafael Fiziev
COU-28 Khabib Nurmagomedov
COU-29 Tom Aspinall
COU-30 Charles Oliveira
"""

EMBEDDED_RAW = """
EMB-1 Daniel Cormier
EMB-2 Khabib Nurmagomedov
EMB-3 Tito Ortiz
EMB-4 Georges St-Pierre
EMB-5 Donald Cerrone
EMB-6 Jens Pulver
EMB-7 Michael Bisping
EMB-8 Anderson Silva
EMB-9 Forrest Griffin
EMB-10 Chuck Liddell
"""

ENERGIZED_RAW = """
TME-1 Aljamain Sterling
TME-2 Raul Rosas
TME-3 Da'Mon Blackshear
TME-4 Erin Blanchfield
TME-5 Alexandre Pantoja
TME-6 Raquel Pennington
TME-7 Max Holloway
TME-8 Tatsuro Taira
TME-9 Jamahal Hill
TME-10 Michael Morales
TME-11 Bo Nickal
TME-12 Maycee Barber
TME-13 Muhammad Mokaev
TME-14 Dricus Du Plessis
TME-15 Roman Dolidze
"""

FIRED_UP_RAW = """
FDP-1 Julianna Peña
FDP-2 Miesha Tate
FDP-3 Alexa Grasso
FDP-4 Maycee Barber
FDP-5 Zhang Weili
FDP-6 Rose Namajunas
FDP-7 Jailton Almeida
FDP-8 Derrick Lewis
FDP-9 Jiri Prochazka
FDP-10 Carlos Ulberg
FDP-11 Justin Tafa
FDP-12 Dricus Du Plessis
FDP-13 Leon Edwards
FDP-14 Gilbert Burns
FDP-15 Ian Machado Garry
FDP-16 Charles Oliveira
FDP-17 Jamahal Hill
FDP-18 Paul Craig
FDP-19 Dan Hooker
FDP-20 Justin Gaethje
FDP-21 Dustin Poirier
FDP-22 Ilia Topuria
FDP-23 Paddy Pimblett
FDP-24 Bo Nickal
FDP-25 Aljamain Sterling
"""

FISTS_OF_FURY_RAW = """
FOF-1 Max Holloway
FOF-2 Angela Hill
FOF-3 Frankie Edgar
FOF-4 Dustin Poirier
FOF-5 Sean Strickland
FOF-6 Casey O'Neill
FOF-7 Sergei Pavlovich
FOF-8 Sean O'Malley
FOF-9 Georges St-Pierre
FOF-10 Kamaru Usman
FOF-11 Israel Adesanya
FOF-12 Anderson Silva
FOF-13 Lyoto Machida
FOF-14 Conor McGregor
FOF-15 Derrick Lewis
"""

GENERATION_NOW_RAW = """
GNW-1 Alexander Volkanovski
GNW-2 Jon Jones
GNW-3 Islam Makhachev
GNW-4 Leon Edwards
GNW-5 Israel Adesanya
GNW-6 Aljamain Sterling
GNW-7 Charles Oliveira
GNW-8 Kamaru Usman
GNW-9 Alexandre Pantoja
GNW-10 Jiri Prochazka
GNW-11 Alex Pereira
GNW-12 Max Holloway
GNW-13 Dustin Poirier
GNW-14 Jamahal Hill
GNW-15 Brandon Moreno
GNW-16 Alexa Grasso
GNW-17 Valentina Shevchenko
GNW-18 Zhang Weili
GNW-19 Rose Namajunas
GNW-20 Julianna Peña
GNW-21 Carla Esparza
GNW-22 Gilbert Burns
GNW-23 Justin Gaethje
GNW-24 Colby Covington
GNW-25 Belal Muhammad
"""

HIDDEN_GEMS_RAW = """
HG-1 Conor McGregor
HG-2 Jon Jones
HG-3 Sean O'Malley
HG-4 Georges St-Pierre
HG-5 Khabib Nurmagomedov
"""

INTERNATIONAL_FLAIR_RAW = """
IFL-1 Amir Albazi
IFL-2 Umar Nurmagomedov
IFL-3 Movsar Evloev
IFL-4 Rafael Fiziev
IFL-5 Shavkat Rakhmonov
IFL-6 Marvin Vettori
IFL-7 Jan Błachowicz
IFL-8 Tom Aspinall
IFL-9 Yan Xiaonan
IFL-10 Manon Fiorot
"""

KINGS_AND_QUEENS_RAW = """
KAQ-1 Amanda Nunes
KAQ-2 Conor McGregor
KAQ-3 Khabib Nurmagomedov
KAQ-4 Israel Adesanya
KAQ-5 Alexa Grasso
KAQ-6 Georges St-Pierre
KAQ-7 Miesha Tate
KAQ-8 Jon Jones
KAQ-9 Chuck Liddell
KAQ-10 Zhang Weili
KAQ-11 Alexander Volkanovski
KAQ-12 Holly Holm
KAQ-13 Islam Makhachev
KAQ-14 Royce Gracie
KAQ-15 Valentina Shevchenko
"""

LETS_GO_RAW = """
LGO-1 Jon Jones
LGO-2 Yair Rodríguez
LGO-3 Mayra Bueno
LGO-4 Dricus Du Plessis
LGO-5 Israel Adesanya
LGO-6 Conor McGregor
LGO-7 Brandon Moreno
LGO-8 Michael Chandler
LGO-9 Khamzat Chimaev
LGO-10 Sean Strickland
LGO-11 Robert Whittaker
LGO-12 Jiri Prochazka
LGO-13 Valentina Shevchenko
LGO-14 Ilia Topuria
LGO-15 Tai Tuivasa
"""

PATHBLAZERS_RAW = """
PTH-1 Forrest Griffin
PTH-2 Alexander Volkanovski
PTH-3 Georges St-Pierre
PTH-4 Conor McGregor
PTH-5 Colby Covington
PTH-6 Israel Adesanya
PTH-7 Tai Tuivasa
PTH-8 Chuck Liddell
PTH-9 Royce Gracie
PTH-10 Donald Cerrone
PTH-11 Anderson Silva
PTH-12 Urijah Faber
PTH-13 Dan Henderson
PTH-14 Michel Pereira
PTH-15 Jon Jones
"""

REPRESENTING_RAW = """
REP-1 Royce Gracie
REP-2 Zhang Weili
REP-3 Raul Rosas
REP-4 Henry Cejudo
REP-5 Anderson Silva
REP-6 Conor McGregor
REP-7 Georges St-Pierre
REP-8 Dominick Cruz
REP-9 Michael Bisping
REP-10 Amanda Nunes
REP-11 Valentina Shevchenko
REP-12 Alexander Volkanovski
REP-13 Khamzat Chimaev
REP-14 Jon Jones
REP-15 Daniel Cormier
REP-16 Max Holloway
REP-17 Cameron Saaiman
REP-18 Khabib Nurmagomedov
REP-19 Dustin Poirier
REP-20 Themba Gorimbo
"""

SPITTING_VENOM_RAW = """
SPV-1 Sean O'Malley
SPV-2 Israel Adesanya
SPV-3 Colby Covington
SPV-4 Sean Strickland
SPV-5 Kevin Holland
SPV-6 Conor McGregor
SPV-7 Paddy Pimblett
SPV-8 Khamzat Chimaev
SPV-9 Jon Jones
SPV-10 Alex Pereira
"""

SUPERGIANT_RAW = """
SUG-1 Jon Jones
SUG-2 Israel Adesanya
SUG-3 Georges St-Pierre
SUG-4 Khabib Nurmagomedov
SUG-5 Alexander Volkanovski
SUG-6 Amanda Nunes
SUG-7 Khamzat Chimaev
SUG-8 Conor McGregor
SUG-9 Chuck Liddell
SUG-10 Valentina Shevchenko
SUG-11 Jiri Prochazka
SUG-12 Sean O'Malley
SUG-13 Anderson Silva
SUG-14 Kamaru Usman
SUG-15 Zhang Weili
"""

TALE_OF_THE_TAPE_RAW = """
TFT-1 Brandon Moreno
TFT-2 Deiveson Figueiredo
TFT-3 Kai Kara-France
TFT-4 Merab Dvalishvili
TFT-5 Sean O'Malley
TFT-6 Henry Cejudo
TFT-7 Alexander Volkanovski
TFT-8 Brian Ortega
TFT-9 Yair Rodríguez
TFT-10 Islam Makhachev
TFT-11 Beneil Dariush
TFT-12 Michael Chandler
TFT-13 Kamaru Usman
TFT-14 Gilbert Burns
TFT-15 Belal Muhammad
TFT-16 Khamzat Chimaev
TFT-17 Conor McGregor
TFT-18 Israel Adesanya
TFT-19 Jared Cannonier
TFT-20 Jiri Prochazka
TFT-21 Magomed Ankalaev
TFT-22 Johnny Walker
TFT-23 Jon Jones
TFT-24 Stipe Miocic
TFT-25 Tai Tuivasa
TFT-26 Carla Esparza
TFT-27 Jessica Andrade
TFT-28 Angela Hill
TFT-29 Valentina Shevchenko
TFT-30 Holly Holm
"""

UFC_FIGHT_NIGHT_RAW = """
UFN-1 Tom Aspinall
UFN-2 Jack Della Maddalena
UFN-3 Sean Strickland
UFN-4 Ilia Topuria
UFN-5 Jailton Almeida
UFN-6 Ian Machado Garry
UFN-7 Carlos Ulberg
UFN-8 Sergei Pavlovich
UFN-9 Max Holloway
UFN-10 Islam Makhachev
UFN-11 Merab Dvalishvili
UFN-12 Mike Malott
UFN-13 Tatiana Suarez
UFN-14 Erin Blanchfield
UFN-15 Umar Nurmagomedov
"""

YOUTHQUAKE_RAW = """
YQK-1 Erin Blanchfield
YQK-2 Tatsuro Taira
YQK-3 Muhammad Mokaev
YQK-4 Bo Nickal
YQK-5 Raul Rosas
YQK-6 Ian Machado Garry
YQK-7 Brad Katona
YQK-8 Shavkat Rakhmonov
YQK-9 Ilia Topuria
YQK-10 Michael Morales
"""

# ─────────────────────────────────────────────────────────────
# Parsing helpers
# ─────────────────────────────────────────────────────────────

def parse_base_set(raw):
    """Parse base set lines: '1 Player Name RC' → card dicts."""
    cards = []
    for line in raw.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        # Match: number then rest
        parts = line.split(None, 1)
        if len(parts) < 2:
            continue
        card_number = parts[0]
        rest = parts[1].strip()

        is_rookie = False
        if rest.endswith(" RC"):
            is_rookie = True
            rest = rest[:-3].strip()

        player = fix_name(rest)
        cards.append({
            "card_number": card_number,
            "player":      player,
            "team":        None,
            "is_rookie":   is_rookie,
            "subset":      None,
        })
    return cards


def parse_auto_line(raw, is_rookie=False):
    """Parse autograph lines: 'CRA-BKA Player Name' → card dicts."""
    cards = []
    for line in raw.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(None, 1)
        if len(parts) < 2:
            continue
        card_number = parts[0]
        player = fix_name(parts[1].strip())
        cards.append({
            "card_number": card_number,
            "player":      player,
            "team":        None,
            "is_rookie":   is_rookie,
            "subset":      None,
        })
    return cards


def parse_insert_line(raw, is_rookie=False):
    """Parse standard insert lines: 'INS-1 Player Name' → card dicts."""
    return parse_auto_line(raw, is_rookie=is_rookie)


def parse_aka_line(raw):
    """Parse AKA lines: 'AKA-1 Player Name – "Nickname"' → card dicts (strip nickname)."""
    cards = []
    for line in raw.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(None, 1)
        if len(parts) < 2:
            continue
        card_number = parts[0]
        rest = parts[1].strip()
        # Strip " – ..." nickname portion
        if " \u2013 " in rest:
            rest = rest[:rest.index(" \u2013 ")].strip()
        elif " - " in rest:
            rest = rest[:rest.index(" - ")].strip()
        player = fix_name(rest)
        cards.append({
            "card_number": card_number,
            "player":      player,
            "team":        None,
            "is_rookie":   False,
            "subset":      None,
        })
    return cards


def parse_yqs_line(raw):
    """Parse Youthquake Signatures lines: 'YQS-AAL Player Name /10' → strip /10."""
    cards = []
    for line in raw.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(None, 1)
        if len(parts) < 2:
            continue
        card_number = parts[0]
        rest = parts[1].strip()
        # Strip trailing /number
        import re
        rest = re.sub(r"\s*/\d+\s*$", "", rest).strip()
        player = fix_name(rest)
        cards.append({
            "card_number": card_number,
            "player":      player,
            "team":        None,
            "is_rookie":   False,
            "subset":      None,
        })
    return cards


# ─────────────────────────────────────────────────────────────
# Build sections
# ─────────────────────────────────────────────────────────────

def build_sections():
    sections = []

    # Section 1: Base Set
    sections.append({
        "insert_set":    "Base Set",
        "parallels":     BASE_PARALLELS,
        "base_print_run": None,
        "cards":         parse_base_set(BASE_SET_RAW),
    })

    # Section 2: Chrome Rookie Autographs
    sections.append({
        "insert_set":    "Chrome Rookie Autographs",
        "parallels":     AUTO_PAR_REFRACTOR_NUMBERED,
        "base_print_run": None,
        "cards":         parse_auto_line(CHROME_ROOKIE_AUTOS_RAW, is_rookie=True),
    })

    # Section 3: Chrome Veteran Autographs
    sections.append({
        "insert_set":    "Chrome Veteran Autographs",
        "parallels":     AUTO_PAR_REFRACTOR_NUMBERED,
        "base_print_run": None,
        "cards":         parse_auto_line(CHROME_VETERAN_AUTOS_RAW, is_rookie=False),
    })

    # Section 4: Future Stars Autographs
    sections.append({
        "insert_set":    "Future Stars Autographs",
        "parallels":     AUTO_PAR_REFRACTOR_NUMBERED,
        "base_print_run": None,
        "cards":         parse_auto_line(FUTURE_STARS_AUTOS_RAW, is_rookie=False),
    })

    # Section 5: Hall of Fame Autographs
    sections.append({
        "insert_set":    "Hall of Fame Autographs",
        "parallels":     AUTO_PAR_REFRACTOR_NUMBERED,
        "base_print_run": None,
        "cards":         parse_auto_line(HALL_OF_FAME_AUTOS_RAW, is_rookie=False),
    })

    # Section 6: Main Event Autographs
    sections.append({
        "insert_set":    "Main Event Autographs",
        "parallels":     AUTO_PAR_REFRACTOR_NUMBERED,
        "base_print_run": None,
        "cards":         parse_auto_line(MAIN_EVENT_AUTOS_RAW, is_rookie=False),
    })

    # Section 7: Marks of Champions Autographs
    sections.append({
        "insert_set":    "Marks of Champions Autographs",
        "parallels":     AUTO_PAR_REFRACTOR_NUMBERED,
        "base_print_run": None,
        "cards":         parse_auto_line(MARKS_OF_CHAMPIONS_AUTOS_RAW, is_rookie=False),
    })

    # Section 8: Octagon Legends Autographs
    sections.append({
        "insert_set":    "Octagon Legends Autographs",
        "parallels":     AUTO_PAR_REFRACTOR_UNNUMBERED,
        "base_print_run": None,
        "cards":         parse_auto_line(OCTAGON_LEGENDS_AUTOS_RAW, is_rookie=False),
    })

    # Section 9: UFC Signatures
    sections.append({
        "insert_set":    "UFC Signatures",
        "parallels":     AUTO_PAR_REFRACTOR_UNNUMBERED,
        "base_print_run": None,
        "cards":         parse_auto_line(UFC_SIGNATURES_RAW, is_rookie=False),
    })

    # Section 10: Youthquake Signatures
    sections.append({
        "insert_set":    "Youthquake Signatures",
        "parallels":     YQS_PAR,
        "base_print_run": 10,
        "cards":         parse_yqs_line(YOUTHQUAKE_SIGNATURES_RAW),
    })

    # Section 11: 1954 Topps
    sections.append({
        "insert_set":    "1954 Topps",
        "parallels":     INSERT_PAR_WITH_REF,
        "base_print_run": None,
        "cards":         parse_insert_line(TOPPS_1954_RAW, is_rookie=False),
    })

    # Section 12: AKA
    sections.append({
        "insert_set":    "AKA",
        "parallels":     INSERT_PAR_NO_REF,
        "base_print_run": None,
        "cards":         parse_aka_line(AKA_RAW),
    })

    # Section 13: All the Glory
    sections.append({
        "insert_set":    "All the Glory",
        "parallels":     [],
        "base_print_run": None,
        "cards":         parse_insert_line(ALL_THE_GLORY_RAW, is_rookie=False),
    })

    # Section 14: Allen & Ginter
    sections.append({
        "insert_set":    "Allen & Ginter",
        "parallels":     INSERT_PAR_WITH_REF,
        "base_print_run": None,
        "cards":         parse_insert_line(ALLEN_AND_GINTER_RAW, is_rookie=False),
    })

    # Section 15: Brick by Brick
    sections.append({
        "insert_set":    "Brick by Brick",
        "parallels":     INSERT_PAR_WITH_REF,
        "base_print_run": None,
        "cards":         parse_insert_line(BRICK_BY_BRICK_RAW, is_rookie=False),
    })

    # Section 16: Countdown
    sections.append({
        "insert_set":    "Countdown",
        "parallels":     SUPERFRACTOR_ONLY,
        "base_print_run": None,
        "cards":         parse_insert_line(COUNTDOWN_RAW, is_rookie=False),
    })

    # Section 17: Embedded
    sections.append({
        "insert_set":    "Embedded",
        "parallels":     INSERT_PAR_WITH_REF,
        "base_print_run": None,
        "cards":         parse_insert_line(EMBEDDED_RAW, is_rookie=False),
    })

    # Section 18: Energized
    sections.append({
        "insert_set":    "Energized",
        "parallels":     [],
        "base_print_run": None,
        "cards":         parse_insert_line(ENERGIZED_RAW, is_rookie=False),
    })

    # Section 19: Fired Up
    sections.append({
        "insert_set":    "Fired Up",
        "parallels":     INSERT_PAR_WITH_REF,
        "base_print_run": None,
        "cards":         parse_insert_line(FIRED_UP_RAW, is_rookie=False),
    })

    # Section 20: Fists of Fury
    sections.append({
        "insert_set":    "Fists of Fury",
        "parallels":     SUPERFRACTOR_ONLY,
        "base_print_run": None,
        "cards":         parse_insert_line(FISTS_OF_FURY_RAW, is_rookie=False),
    })

    # Section 21: Generation Now
    sections.append({
        "insert_set":    "Generation Now",
        "parallels":     SUPERFRACTOR_ONLY,
        "base_print_run": None,
        "cards":         parse_insert_line(GENERATION_NOW_RAW, is_rookie=False),
    })

    # Section 22: Hidden Gems
    sections.append({
        "insert_set":    "Hidden Gems",
        "parallels":     SUPERFRACTOR_ONLY,
        "base_print_run": 50,
        "cards":         parse_insert_line(HIDDEN_GEMS_RAW, is_rookie=False),
    })

    # Section 23: International Flair
    sections.append({
        "insert_set":    "International Flair",
        "parallels":     INSERT_PAR_WITH_REF,
        "base_print_run": None,
        "cards":         parse_insert_line(INTERNATIONAL_FLAIR_RAW, is_rookie=False),
    })

    # Section 24: Kings and Queens
    sections.append({
        "insert_set":    "Kings and Queens",
        "parallels":     [],
        "base_print_run": None,
        "cards":         parse_insert_line(KINGS_AND_QUEENS_RAW, is_rookie=False),
    })

    # Section 25: Let's Go
    sections.append({
        "insert_set":    "Let's Go",
        "parallels":     [],
        "base_print_run": None,
        "cards":         parse_insert_line(LETS_GO_RAW, is_rookie=False),
    })

    # Section 26: Pathblazers
    sections.append({
        "insert_set":    "Pathblazers",
        "parallels":     INSERT_PAR_WITH_REF,
        "base_print_run": None,
        "cards":         parse_insert_line(PATHBLAZERS_RAW, is_rookie=False),
    })

    # Section 27: Representing
    sections.append({
        "insert_set":    "Representing",
        "parallels":     SUPERFRACTOR_ONLY,
        "base_print_run": None,
        "cards":         parse_insert_line(REPRESENTING_RAW, is_rookie=False),
    })

    # Section 28: Spitting Venom
    sections.append({
        "insert_set":    "Spitting Venom",
        "parallels":     [],
        "base_print_run": None,
        "cards":         parse_insert_line(SPITTING_VENOM_RAW, is_rookie=False),
    })

    # Section 29: Supergiant
    sections.append({
        "insert_set":    "Supergiant",
        "parallels":     INSERT_PAR_WITH_REF,
        "base_print_run": None,
        "cards":         parse_insert_line(SUPERGIANT_RAW, is_rookie=False),
    })

    # Section 30: Tale of the Tape
    sections.append({
        "insert_set":    "Tale of the Tape",
        "parallels":     INSERT_PAR_WITH_REF,
        "base_print_run": None,
        "cards":         parse_insert_line(TALE_OF_THE_TAPE_RAW, is_rookie=False),
    })

    # Section 31: UFC Fight Night
    sections.append({
        "insert_set":    "UFC Fight Night",
        "parallels":     [],
        "base_print_run": None,
        "cards":         parse_insert_line(UFC_FIGHT_NIGHT_RAW, is_rookie=False),
    })

    # Section 32: Youthquake
    sections.append({
        "insert_set":    "Youthquake",
        "parallels":     SUPERFRACTOR_ONLY,
        "base_print_run": None,
        "cards":         parse_insert_line(YOUTHQUAKE_RAW, is_rookie=False),
    })

    return sections


# ─────────────────────────────────────────────────────────────
# Player stats computation
# ─────────────────────────────────────────────────────────────

def compute_stats(appearances):
    """
    unique_cards:    total number of appearances (1 per appearance/section)
    total_print_run: sum of base_print_run (if set) + all numbered parallel print_runs
                     per appearance
    one_of_ones:     count of appearances where a Superfractor /1 parallel exists
                     (or base_print_run == 1)
    insert_sets:     count of distinct insert set names
    """
    unique_cards    = len(appearances)
    total_print_run = 0
    one_of_ones     = 0
    insert_set_names = set()

    for app in appearances:
        insert_set_names.add(app["insert_set"])

        # Add base_print_run contribution
        bpr = app.get("base_print_run")
        if bpr is not None:
            total_print_run += bpr
            if bpr == 1:
                one_of_ones += 1

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
        "unique_cards":    unique_cards,
        "total_print_run": total_print_run,
        "one_of_ones":     one_of_ones,
        "insert_sets":     len(insert_set_names),
    }


# ─────────────────────────────────────────────────────────────
# Build output
# ─────────────────────────────────────────────────────────────

def build_output(sections):
    # Collect all rookie players to propagate is_rookie consistently
    rc_players = set()
    for section in sections:
        for card in section["cards"]:
            if card.get("is_rookie"):
                rc_players.add(card["player"])

    # Build player index: player name → list of appearances
    player_index = {}
    for section in sections:
        for card in section["cards"]:
            pname = card["player"]
            if pname not in player_index:
                player_index[pname] = {"player": pname, "appearances": []}
            player_index[pname]["appearances"].append({
                "insert_set":    section["insert_set"],
                "card_number":   card["card_number"],
                "team":          card["team"],
                "is_rookie":     pname in rc_players,
                "subset_tag":    card["subset"],
                "parallels":     section["parallels"],
                "base_print_run": section.get("base_print_run"),
            })

    players_list = []
    for pname in sorted(player_index.keys()):
        data = player_index[pname]
        players_list.append({
            "player":      pname,
            "appearances": data["appearances"],
            "stats":       compute_stats(data["appearances"]),
        })

    # Strip internal base_print_run from appearances in output
    # (seed.ts doesn't use it — it's only for stat computation)
    for entry in players_list:
        for app in entry["appearances"]:
            app.pop("base_print_run", None)

    # Build output sections — strip base_print_run from section dicts for JSON output
    output_sections = []
    for section in sections:
        output_sections.append({
            "insert_set": section["insert_set"],
            "parallels":  section["parallels"],
            "cards":      section["cards"],
        })

    return {
        "set_name": "2025 Topps Chrome UFC",
        "sport":    "MMA",
        "season":   "2025",
        "league":   "UFC",
        "sections": output_sections,
        "players":  players_list,
    }


# ─────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Parsing 2025 Topps Chrome UFC...")

    sections = build_sections()
    output   = build_output(sections)

    out_path = "ufc_chrome_2025_parsed.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nSet: {output['set_name']} ({output['season']})")
    print(f"Sections: {len(output['sections'])}")
    for s in output["sections"]:
        print(f"  {s['insert_set']:<52} {len(s['cards']):>4} cards  {len(s['parallels']):>2} parallels")

    print(f"\nTotal unique players: {len(output['players'])}")

    player_map = {p["player"]: p for p in output["players"]}

    print("\n=== Spot checks ===")
    for name in ["Jon Jones", "Conor McGregor", "Khabib Nurmagomedov"]:
        if name in player_map:
            st = player_map[name]["stats"]
            print(f"  {name}: {st['insert_sets']} insert sets, "
                  f"{st['unique_cards']} unique cards, "
                  f"{st['total_print_run']} total print run, "
                  f"{st['one_of_ones']} 1/1s")
        else:
            print(f"  {name}: NOT FOUND")

    print(f"\nOutput written to: {out_path}")
