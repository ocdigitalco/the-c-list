import json
import re

# ─────────────────────────────────────────────────────────────
# Fighters whose Topps appearance is a Rookie Card
# (drawn from the Rookie Auto checklist + explicit RC markers)
# ─────────────────────────────────────────────────────────────
ROOKIE_FIGHTERS = {
    "Jonathan Martinez", "Hyunsung Park", "Assu Almabayev", "Kai Asakura",
    "Daniel Zellhuber", "Muhammadjon Naimov", "Nurullo Aliev", "Farid Basharat",
    "Roman Kopylov", "Shamil Gaziev", "Daniel Marcos", "Ailin Perez",
    "Nate Landwehr", "Bogdan Guskov", "Waldo Cortes", "Gabriel Bonfim",
    "Christian Duncan", "Stephen Erceg", "Vitor Petrino", "Myktybek Orolbai",
    "Jose Mariscal", "Rinya Nakamura", "Joshua Van", "Payton Talbott",
    "Vinicius Oliveira", "Jean Silva", "Carlos Prates", "Reinier de Ridder",
    "Mauricio Santos", "Nazim Sadykhov", "Jean Matsumoto",
}

# ─────────────────────────────────────────────────────────────
# Multi-player section names  (cards split on " / ")
# ─────────────────────────────────────────────────────────────
MULTI_PLAYER_SECTIONS = {
    "Dual Auto",
    "Dual Fighter Relic Auto",
    "Triple Auto",
    "Prodigious Pairings",
}

# ─────────────────────────────────────────────────────────────
# Parallel definitions by section type
# ─────────────────────────────────────────────────────────────
PARALLELS_BASE = [
    {"name": "Purple",   "print_run": 35},
    {"name": "Blue",     "print_run": 25},
    {"name": "Red",      "print_run": 15},
    {"name": "Gold",     "print_run": 10},
    {"name": "Green",    "print_run": 5},
    {"name": "Platinum", "print_run": 1},
]

PARALLELS_AUTO_99 = [
    {"name": "Blue",     "print_run": 25},
    {"name": "Gold",     "print_run": 10},
    {"name": "Green",    "print_run": 5},
    {"name": "Platinum", "print_run": 1},
]

PARALLELS_AUTO_25 = [
    {"name": "Green",    "print_run": 5},
    {"name": "Platinum", "print_run": 1},
]

PARALLELS_PLATINUM_ONLY = [
    {"name": "Platinum", "print_run": 1},
]

PARALLELS_NONE = []

PARALLELS_LIQUID_GOLD = [
    {"name": "Liquid Gold", "print_run": 1},
]

SECTION_PARALLELS = {
    "Base Set":                     PARALLELS_BASE,
    # /99 auto sets
    "Auto Jumbo Relic Booklet":     PARALLELS_AUTO_25,
    "Golden Hall Auto":             PARALLELS_AUTO_99,
    "Imperial Ink":                 PARALLELS_AUTO_99,
    "Pursuit of Greatness Signatures": PARALLELS_AUTO_99,
    "Regalia Relic Signatures":     PARALLELS_AUTO_99,
    "Rookie Auto":                  PARALLELS_AUTO_99,
    "Rookie Relic Auto":            PARALLELS_AUTO_99,
    "Royal Precedence":             PARALLELS_AUTO_99,
    "Royalty Auto":                 PARALLELS_AUTO_99,
    "Royalty Relic Signatures":     PARALLELS_AUTO_99,
    "Superior Relic Signatures":    PARALLELS_AUTO_99,
    "Superior Signatures":          PARALLELS_AUTO_99,
    "Supreme Royalty Signatures":   PARALLELS_AUTO_99,
    # /25 auto sets with Green/Platinum
    "Dual Auto":                    PARALLELS_AUTO_25,
    "Dual Fighter Relic Auto":      PARALLELS_AUTO_25,
    "Triple Auto":                  PARALLELS_AUTO_25,
    # /25 no parallels
    "Crowned Champions Auto":       PARALLELS_NONE,
    "Royal Decree Auto":            PARALLELS_NONE,
    "The Time Is Now":              PARALLELS_NONE,
    # Royal Seal Signatures: /25 + Platinum only
    "Royal Seal Signatures":        PARALLELS_PLATINUM_ONLY,
    # Relic-only sets: /99, no parallels
    "Grand Royal Relics":           PARALLELS_NONE,
    "Prodigious Pairings":          PARALLELS_NONE,
    "Regalia Relics":               PARALLELS_NONE,
    "Relic Jewels":                 PARALLELS_NONE,
    "Rookie Jumbo Relics":          PARALLELS_NONE,
    "Star Relics":                  PARALLELS_NONE,
    # Insert
    "Liquid Silver":                PARALLELS_LIQUID_GOLD,
}

# ─────────────────────────────────────────────────────────────
# Section data (cards per section)
# Format: card_number, player (for multi-player: "P1 / P2 / P3")
# ─────────────────────────────────────────────────────────────

SECTIONS_DATA = [
    ("Base Set", [
        ("1",   "Alex Pereira"),
        ("2",   "Georges St-Pierre"),
        ("3",   "Dricus du Plessis"),
        ("4",   "Norma Dumont"),
        ("5",   "Jonathan Martinez"),
        ("6",   "Arman Tsarukyan"),
        ("7",   "Israel Adesanya"),
        ("8",   "Hyunsung Park"),
        ("9",   "Assu Almabayev"),
        ("10",  "Kai Asakura"),
        ("11",  "Merab Dvalishvili"),
        ("12",  "Sean O'Malley"),
        ("13",  "Daniel Zellhuber"),
        ("14",  "Tatiana Suarez"),
        ("15",  "Alexa Grasso"),
        ("16",  "Deiveson Figueiredo"),
        ("17",  "Muhammadjon Naimov"),
        ("18",  "Dana White"),
        ("19",  "Nurullo Aliev"),
        ("20",  "Farid Basharat"),
        ("21",  "Amir Albazi"),
        ("22",  "Magomed Ankalaev"),
        ("23",  "Chase Hooper"),
        ("24",  "Roman Kopylov"),
        ("25",  "Yair Rodríguez"),
        ("26",  "Jiri Prochazka"),
        ("27",  "Zhang Weili"),
        ("28",  "Diego Lopes"),
        ("29",  "Shamil Gaziev"),
        ("30",  "Max Holloway"),
        ("31",  "Carlos Ulberg"),
        ("32",  "Alexander Volkanovski"),
        ("33",  "Daniel Marcos"),
        ("34",  "Ailin Perez"),
        ("35",  "Movsar Evloev"),
        ("36",  "Daniel Hooker"),
        ("37",  "Belal Muhammad"),
        ("38",  "Ian Machado Garry"),
        ("39",  "Leon Edwards"),
        ("40",  "Nate Landwehr"),
        ("41",  "Bogdan Guskov"),
        ("42",  "Justin Gaethje"),
        ("43",  "Maycee Barber"),
        ("44",  "Ketlen Vieira"),
        ("45",  "Alexandre Pantoja"),
        ("46",  "Waldo Cortes"),
        ("47",  "Khamzat Chimaev"),
        ("48",  "Nassourdine Imavov"),
        ("49",  "Conor McGregor"),
        ("50",  "Gabriel Bonfim"),
        ("51",  "Sean Brady"),
        ("52",  "Erin Blanchfield"),
        ("53",  "Virna Jandiroba"),
        ("54",  "José Aldo"),
        ("55",  "Christian Duncan"),
        ("56",  "Jean Matsumoto"),
        ("57",  "Stephen Erceg"),
        ("58",  "Dustin Poirier"),
        ("59",  "Tom Aspinall"),
        ("60",  "Khabib Nurmagomedov"),
        ("61",  "Aljamain Sterling"),
        ("62",  "Vitor Petrino"),
        ("63",  "Kayla Harrison"),
        ("64",  "Caio Borralho"),
        ("65",  "Valentina Shevchenko"),
        ("66",  "Anderson Silva"),
        ("67",  "Ciryl Gane"),
        ("68",  "Myktybek Orolbai"),
        ("69",  "Jose Mariscal"),
        ("70",  "Raquel Pennington"),
        ("71",  "Jack Della Maddalena"),
        ("72",  "Yan Xiaonan"),
        ("73",  "Charles Oliveira"),
        ("74",  "Rinya Nakamura"),
        ("75",  "Joshua Van"),
        ("76",  "Payton Talbott"),
        ("77",  "Bo Nickal"),
        ("78",  "Tracy Cortez"),
        ("79",  "Brandon Royval"),
        ("80",  "Raul Rosas"),
        ("81",  "Vinicius Oliveira"),
        ("82",  "Jean Silva"),
        ("83",  "Carlos Prates"),
        ("84",  "Reinier de Ridder"),
        ("85",  "Julianna Peña"),
        ("86",  "Paddy Pimblett"),
        ("87",  "Islam Makhachev"),
        ("88",  "Sean Strickland"),
        ("89",  "Mackenzie Dern"),
        ("90",  "Mauricio Santos"),
        ("91",  "Brandon Moreno"),
        ("92",  "Colby Covington"),
        ("93",  "Manon Fiorot"),
        ("94",  "Umar Nurmagomedov"),
        ("95",  "Rose Namajunas"),
        ("96",  "Michael Chandler"),
        ("97",  "Ilia Topuria"),
        ("98",  "Shavkat Rakhmonov"),
        ("99",  "Kai Kara-France"),
        ("100", "Jon Jones"),
    ]),

    ("Auto Jumbo Relic Booklet", [
        ("AJR-AG", "Alexa Grasso"),
        ("AJR-AL", "Alexandre Pantoja"),
        ("AJR-AP", "Alex Pereira"),
        ("AJR-AZ", "Ailin Perez"),
        ("AJR-BM", "Belal Muhammad"),
        ("AJR-CB", "Caio Borralho"),
        ("AJR-CH", "Chase Hooper"),
        ("AJR-CO", "Charles Oliveira"),
        ("AJR-CP", "Carlos Prates"),
        ("AJR-DH", "Daniel Hooker"),
        ("AJR-DL", "Diego Lopes"),
        ("AJR-DP", "Dustin Poirier"),
        ("AJR-EB", "Erin Blanchfield"),
        ("AJR-IA", "Israel Adesanya"),
        ("AJR-JG", "Justin Gaethje"),
        ("AJR-JI", "Jiri Prochazka"),
        ("AJR-JM", "Jack Della Maddalena"),
        ("AJR-JP", "Joe Pyfer"),
        ("AJR-JU", "Julianna Peña"),
        ("AJR-KH", "Kayla Harrison"),
        ("AJR-MB", "Maycee Barber"),
        ("AJR-MM", "Michael Morales"),
        ("AJR-MP", "Michael Page"),
        ("AJR-PP", "Paddy Pimblett"),
        ("AJR-PT", "Payton Talbott"),
        ("AJR-RD", "Reinier de Ridder"),
        ("AJR-RR", "Raul Rosas"),
        ("AJR-SE", "Stephen Erceg"),
        ("AJR-SO", "Sean O'Malley"),
        ("AJR-TC", "Tracy Cortez"),
        ("AJR-VO", "Vinicius Oliveira"),
        ("AJR-VS", "Valentina Shevchenko"),
    ]),

    ("Crowned Champions Auto", [
        ("CCA-AP", "Alexandre Pantoja"),
        ("CCA-AS", "Aljamain Sterling"),
        ("CCA-AV", "Alexander Volkanovski"),
        ("CCA-BM", "Belal Muhammad"),
        ("CCA-CM", "Conor McGregor"),
        ("CCA-DD", "Dricus du Plessis"),
        ("CCA-IA", "Israel Adesanya"),
        ("CCA-IM", "Islam Makhachev"),
        ("CCA-IT", "Ilia Topuria"),
        ("CCA-JJ", "Jon Jones"),
        ("CCA-MD", "Merab Dvalishvili"),
        ("CCA-PP", "Alex Pereira"),
        ("CCA-SS", "Sean Strickland"),
        ("CCA-VS", "Valentina Shevchenko"),
        ("CCA-ZW", "Zhang Weili"),
    ]),

    ("Dual Auto", [
        ("DA-AP", "Alexandre Pantoja / Kai Asakura"),
        ("DA-BB", "Ismael Bonfim / Gabriel Bonfim"),
        ("DA-BC", "Daniel Cormier / Michael Bisping"),
        ("DA-CS", "Sean Strickland / Donald Cerrone"),
        ("DA-DP", "Merab Dvalishvili / Ailin Perez"),
        ("DA-DS", "Dricus da Silva / Norma Dumont"),
        ("DA-FI", "Nassourdine Imavov / Manon Fiorot"),
        ("DA-FO", "Urijah Faber / Myktybek Orolbai"),
        ("DA-GA", "Alexa Grasso / Irene Aldana"),
        ("DA-GB", "Jan Błachowicz / Mateusz Gamrot"),
        ("DA-GH", "Daniel Hooker / Justin Gaethje"),
        ("DA-GM", "Ian Machado Garry / Conor McGregor"),
        ("DA-JC", "Daniel Cormier / Jon Jones"),
        ("DA-OD", "Alistair Overeem / Reinier de Ridder"),
        ("DA-OM", "Ian Machado Garry / Charles Oliveira"),
        ("DA-PA", "Paddy Pimblett / Arnold Allen"),
        ("DA-PS", "Cameron Saaiman / Dricus du Plessis"),
        ("DA-RA", "Shavkat Rakhmonov / Assu Almabayev"),
        ("DA-SO", "Valentina Shevchenko / Myktybek Orolbai"),
        ("DA-SP", "Hyunsung Park / Chan Sung Jung"),
        ("DA-TN", "Tatsuro Taira / Rinya Nakamura"),
        ("DA-TV", "Alexander Volkanovski / Ilia Topuria"),
        ("DA-WS", "Zhang Weili / Yadong Song"),
        ("DA-YA", "Yan Xiaonan / Magomed Ankalaev"),
    ]),

    ("Dual Fighter Relic Auto", [
        ("DFA-AW", "Israel Adesanya / Robert Whittaker"),
        ("DFA-EP", "Leon Edwards / Michael Page"),
        ("DFA-HM", "Daniel Hooker / Jack Della Maddalena"),
        ("DFA-HO", "Charles Oliveira / Max Holloway"),
        ("DFA-PJ", "Jon Jones / Alex Pereira"),
        ("DFA-PS", "Carlos Prates / Mauricio Santos"),
        ("DFA-RR", "Christian Rodriguez / Raul Rosas"),
        ("DFA-SB", "Caio Borralho / Jean Silva"),
        ("DFA-TD", "Merab Dvalishvili / Ilia Topuria"),
    ]),

    ("Golden Hall Auto", [
        ("GH-AO", "Alistair Overeem"),
        ("GH-BR", "Bas Rutten"),
        ("GH-DF", "Don Frye"),
        ("GH-DH", "Dan Henderson"),
        ("GH-FE", "Frankie Edgar"),
        ("GH-FM", "Frank Mir"),
        ("GH-JJ", "Joanna Jędrzejczyk"),
        ("GH-LM", "Lyoto Machida"),
        ("GH-MB", "Michael Bisping"),
        ("GH-RE", "Rashad Evans"),
        ("GH-TS", "Tim Sylvia"),
        ("GH-UF", "Urijah Faber"),
        ("GH-WS", "Wanderlei Silva"),
    ]),

    ("Imperial Ink", [
        ("II-AS", "Anderson Silva"),
        ("II-AV", "Alexander Volkanovski"),
        ("II-BJ", "BJ Penn"),
        ("II-CL", "Chuck Liddell"),
        ("II-CS", "Chan Sung Jung"),
        ("II-DC", "Daniel Cormier"),
        ("II-DE", "Donald Cerrone"),
        ("II-GS", "Georges St-Pierre"),
        ("II-GT", "Glover Teixeira"),
        ("II-JA", "José Aldo"),
        ("II-JJ", "Jon Jones"),
        ("II-KN", "Khabib Nurmagomedov"),
        ("II-MC", "Mark Coleman"),
        ("II-RD", "Rafael Dos Anjos"),
        ("II-SM", "Stipe Miocic"),
    ]),

    ("Pursuit of Greatness Signatures", [
        ("POG-AA", "Amir Albazi"),
        ("POG-AP", "Ailin Perez"),
        ("POG-AZ", "Alex Perez"),
        ("POG-BD", "Benoit Saint Denis"),
        ("POG-CB", "Caio Borralho"),
        ("POG-CH", "Chase Hooper"),
        ("POG-DZ", "Daniel Zellhuber"),
        ("POG-JB", "Joaquin Buckley"),
        ("POG-JM", "Jailton Malhadinho"),
        ("POG-JO", "Joanderson Brito"),
        ("POG-JP", "Joe Pyfer"),
        ("POG-JT", "Javid Basharat"),
        ("POG-JV", "Joshua Van"),
        ("POG-KP", "Kyler Phillips"),
        ("POG-LM", "Lerone Murphy"),
        ("POG-MB", "Mario Bautista"),
        ("POG-ME", "Manel Kape"),
        ("POG-MF", "Manon Fiorot"),
        ("POG-MG", "Maria Godinez Gonzalez"),
        ("POG-MK", "Miranda Maverick"),
        ("POG-MM", "Michael Morales"),
        ("POG-MO", "Myktybek Orolbai"),
        ("POG-MP", "Michael Page"),
        ("POG-ND", "Norma Dumont"),
        ("POG-NI", "Nassourdine Imavov"),
        ("POG-PT", "Payton Talbott"),
        ("POG-SE", "Stephen Erceg"),
        ("POG-SM", "Sharabutdin Magomedov"),
        ("POG-TC", "Tracy Cortez"),
        ("POG-TR", "Tabatha Ricci"),
        ("POG-TS", "Tatiana Suarez"),
        ("POG-TT", "Tatsuro Taira"),
        ("POG-TU", "Tagir Ulanbekov"),
        ("POG-VD", "Viktoriia Dudakova"),
        ("POG-VP", "Vitor Petrino"),
    ]),

    ("Regalia Relic Signatures", [
        ("RRS-AA", "Arnold Allen"),
        ("RRS-AG", "Alexa Grasso"),
        ("RRS-AH", "Anthony Smith"),
        ("RRS-AP", "Alexandre Pantoja"),
        ("RRS-AR", "Aleksandar Rakic"),
        ("RRS-AS", "Aljamain Sterling"),
        ("RRS-BA", "Brendan Allen"),
        ("RRS-BD", "Beneil Dariush"),
        ("RRS-BM", "Belal Muhammad"),
        ("RRS-BO", "Brian Ortega"),
        ("RRS-BS", "Benoit Saint Denis"),
        ("RRS-CH", "Chase Hooper"),
        ("RRS-CS", "Cory Sandhagen"),
        ("RRS-CU", "Carlos Ulberg"),
        ("RRS-DC", "Dominick Cruz"),
        ("RRS-DD", "Dricus du Plessis"),
        ("RRS-DH", "Daniel Hooker"),
        ("RRS-DI", "Dan Ige"),
        ("RRS-EB", "Erin Blanchfield"),
        ("RRS-GB", "Gilbert Burns"),
        ("RRS-HC", "Henry Cejudo"),
        ("RRS-IG", "Ian Machado Garry"),
        ("RRS-IM", "Islam Makhachev"),
        ("RRS-JB", "Joaquin Buckley"),
        ("RRS-JG", "Justin Gaethje"),
        ("RRS-JM", "Jailton Malhadinho"),
        ("RRS-JP", "Jiri Prochazka"),
        ("RRS-JR", "Joe Pyfer"),
        ("RRS-KR", "Khalil Rountree Jr."),
        ("RRS-KV", "Ketlen Vieira"),
        ("RRS-LE", "Leon Edwards"),
        ("RRS-MB", "Maycee Barber"),
        ("RRS-MF", "Manon Fiorot"),
        ("RRS-MK", "Manel Kape"),
        ("RRS-MP", "Michael Page"),
        ("RRS-MT", "Miesha Tate"),
        ("RRS-ND", "Norma Dumont"),
        ("RRS-NI", "Nassourdine Imavov"),
        ("RRS-PC", "Paulo Costa"),
        ("RRS-RT", "Rob Font"),
        ("RRS-SM", "Sharabutdin Magomedov"),
        ("RRS-SS", "Serghei Spivac"),
        ("RRS-TS", "Tatiana Suarez"),
        ("RRS-TT", "Tatsuro Taira"),
        ("RRS-VL", "Vicente Luque"),
        ("RRS-VO", "Volkan Oezdemir"),
        ("RRS-YJ", "Yazmin Jauregui"),
    ]),

    ("Rookie Auto", [
        ("RA-AA", "Assu Almabayev"),
        ("RA-AP", "Ailin Perez"),
        ("RA-CD", "Christian Duncan"),
        ("RA-CP", "Carlos Prates"),
        ("RA-DZ", "Daniel Zellhuber"),
        ("RA-GB", "Gabriel Bonfim"),
        ("RA-JL", "Jose Mariscal"),
        ("RA-JS", "Jean Silva"),
        ("RA-JV", "Joshua Van"),
        ("RA-JZ", "Jonathan Martinez"),
        ("RA-KA", "Kai Asakura"),
        ("RA-MN", "Muhammadjon Naimov"),
        ("RA-MO", "Myktybek Orolbai"),
        ("RA-MS", "Mauricio Santos"),
        ("RA-NL", "Nate Landwehr"),
        ("RA-NS", "Nazim Sadykhov"),
        ("RA-PT", "Payton Talbott"),
        ("RA-RK", "Roman Kopylov"),
        ("RA-RN", "Rinya Nakamura"),
        ("RA-RR", "Reinier de Ridder"),
        ("RA-SE", "Stephen Erceg"),
        ("RA-SG", "Shamil Gaziev"),
        ("RA-VO", "Vinicius Oliveira"),
        ("RA-VP", "Vitor Petrino"),
        ("RA-WA", "Waldo Cortes"),
    ]),

    ("Rookie Relic Auto", [
        ("RRA-AA", "Assu Almabayev"),
        ("RRA-AP", "Ailin Perez"),
        ("RRA-BG", "Bogdan Guskov"),
        ("RRA-CD", "Christian Duncan"),
        ("RRA-CJ", "Charles Jourdain"),
        ("RRA-CP", "Carlos Prates"),
        ("RRA-DB", "Danny Barlow"),
        ("RRA-DM", "Daniel Marcos"),
        ("RRA-DZ", "Daniel Zellhuber"),
        ("RRA-EM", "Eduarda Moura"),
        ("RRA-ER", "Esteban Ribovics"),
        ("RRA-FB", "Farid Basharat"),
        ("RRA-GB", "Gabriel Bonfim"),
        ("RRA-HP", "Hyunsung Park"),
        ("RRA-IB", "Ismael Bonfim"),
        ("RRA-JB", "Joanderson Brito"),
        ("RRA-JL", "Jose Mariscal"),
        ("RRA-JS", "Jean Silva"),
        ("RRA-JV", "Joshua Van"),
        ("RRA-JZ", "Jonathan Martinez"),
        ("RRA-KA", "Kai Asakura"),
        ("RRA-LS", "Luana Santos"),
        ("RRA-MB", "Modestas Bukauskas"),
        ("RRA-MC", "Marcus McGhee"),
        ("RRA-MM", "Melissa Mullins"),
        ("RRA-MN", "Muhammadjon Naimov"),
        ("RRA-MO", "Myktybek Orolbai"),
        ("RRA-MS", "Mauricio Santos"),
        ("RRA-NL", "Nate Landwehr"),
        ("RRA-NS", "Nazim Sadykhov"),
        ("RRA-PT", "Payton Talbott"),
        ("RRA-RB", "Rodolfo Bellato"),
        ("RRA-RK", "Roman Kopylov"),
        ("RRA-RN", "Rinya Nakamura"),
        ("RRA-RR", "Reinier de Ridder"),
        ("RRA-SE", "Stephen Erceg"),
        ("RRA-SG", "Shamil Gaziev"),
        ("RRA-TK", "Toshiomi Kazama"),
        ("RRA-TP", "Trevor Peek"),
        ("RRA-TW", "Trey Waters"),
        ("RRA-VH", "Victor Henry"),
        ("RRA-VO", "Vinicius Oliveira"),
        ("RRA-VP", "Vitor Petrino"),
        ("RRA-WA", "Waldo Cortes"),
        ("RRA-WW", "Westin Wilson"),
    ]),

    ("Royal Decree Auto", [
        ("RDA-AG", "Alexa Grasso"),
        ("RDA-BO", "Brian Ortega"),
        ("RDA-CB", "Curtis Blaydes"),
        ("RDA-CO", "Charles Oliveira"),
        ("RDA-CU", "Carlos Ulberg"),
        ("RDA-DI", "Dan Ige"),
        ("RDA-EB", "Erin Blanchfield"),
        ("RDA-GR", "Gregory Rodrigues"),
        ("RDA-IM", "Ian Machado Garry"),
        ("RDA-JB", "Jan Błachowicz"),
        ("RDA-JG", "Justin Gaethje"),
        ("RDA-JH", "Jamahal Hill"),
        ("RDA-JP", "Jiri Prochazka"),
        ("RDA-KC", "Khamzat Chimaev"),
        ("RDA-KH", "Kevin Holland"),
        ("RDA-KK", "Kai Kara-France"),
        ("RDA-MD", "Mackenzie Dern"),
        ("RDA-MH", "Max Holloway"),
        ("RDA-PC", "Paulo Costa"),
        ("RDA-PY", "Petr Yan"),
        ("RDA-RM", "Renato Moicano"),
        ("RDA-RN", "Rose Namajunas"),
        ("RDA-RP", "Raquel Pennington"),
        ("RDA-RW", "Robert Whittaker"),
        ("RDA-SM", "Stipe Miocic"),
        ("RDA-SO", "Sean O'Malley"),
    ]),

    ("Royal Precedence", [
        ("RP-AH", "Angela Hill"),
        ("RP-AL", "Alexandre Pantoja"),
        ("RP-AP", "Alex Pereira"),
        ("RP-AS", "Aljamain Sterling"),
        ("RP-BM", "Belal Muhammad"),
        ("RP-BO", "Brian Ortega"),
        ("RP-BR", "Brandon Moreno"),
        ("RP-CO", "Charles Oliveira"),
        ("RP-CS", "Chael Sonnen"),
        ("RP-CU", "Carlos Ulberg"),
        ("RP-DD", "Dricus du Plessis"),
        ("RP-DI", "Dan Ige"),
        ("RP-DL", "Diego Lopes"),
        ("RP-IA", "Israel Adesanya"),
        ("RP-IG", "Ian Machado Garry"),
        ("RP-IM", "Islam Makhachev"),
        ("RP-IT", "Ilia Topuria"),
        ("RP-JB", "Jan Błachowicz"),
        ("RP-JG", "Justin Gaethje"),
        ("RP-JH", "Jamahal Hill"),
        ("RP-JJ", "Joanna Jędrzejczyk"),
        ("RP-JP", "Jiri Prochazka"),
        ("RP-KC", "Khamzat Chimaev"),
        ("RP-KH", "Kevin Holland"),
        ("RP-KK", "Kai Kara-France"),
        ("RP-LM", "Lyoto Machida"),
        ("RP-MA", "Magomed Ankalaev"),
        ("RP-MB", "Maycee Barber"),
        ("RP-MD", "Merab Dvalishvili"),
        ("RP-MH", "Max Holloway"),
        ("RP-MN", "Mackenzie Dern"),
        ("RP-PP", "Paddy Pimblett"),
        ("RP-PY", "Petr Yan"),
        ("RP-RN", "Rose Namajunas"),
        ("RP-RP", "Raquel Pennington"),
        ("RP-RW", "Robert Whittaker"),
        ("RP-SO", "Sean O'Malley"),
        ("RP-SR", "Shavkat Rakhmonov"),
        ("RP-SS", "Sean Strickland"),
        ("RP-TF", "Tony Ferguson"),
        ("RP-UN", "Umar Nurmagomedov"),
        ("RP-VS", "Valentina Shevchenko"),
        ("RP-ZW", "Zhang Weili"),
    ]),

    ("Royal Seal Signatures", [
        ("RSS-AS", "Anderson Silva"),
        ("RSS-CM", "Conor McGregor"),
        ("RSS-CS", "Chael Sonnen"),
        ("RSS-DC", "Donald Cerrone"),
        ("RSS-DH", "Jon Jones"),
        ("RSS-DW", "Dana White"),
        ("RSS-GS", "Georges St-Pierre"),
        ("RSS-GT", "Glover Teixeira"),
        ("RSS-KN", "Khabib Nurmagomedov"),
        ("RSS-MB", "Daniel Cormier"),
    ]),

    ("Royalty Auto", [
        ("RY-AD", "Ariane da Silva"),
        ("RY-AM", "Andre Muniz"),
        ("RY-AR", "Aleksandar Rakic"),
        ("RY-AS", "Amanda Ribas"),
        ("RY-BA", "Brendan Allen"),
        ("RY-BN", "Bo Nickal"),
        ("RY-CA", "Christian Rodriguez"),
        ("RY-CC", "Chelsea Chandler"),
        ("RY-CG", "Cody Garbrandt"),
        ("RY-CK", "Calvin Kattar"),
        ("RY-CO", "Casey O'Neill"),
        ("RY-GB", "Gilbert Burns"),
        ("RY-JA", "Joel Alvarez"),
        ("RY-JE", "Josh Emmett"),
        ("RY-JH", "Jack Hermansson"),
        ("RY-JJ", "Jack Jenkins"),
        ("RY-JR", "Jim Miller"),
        ("RY-JW", "Johnny Walker"),
        ("RY-LP", "Luana Pinheiro"),
        ("RY-MP", "Michel Pereira"),
        ("RY-MS", "Manuel Torres"),
        ("RY-MT", "Miesha Tate"),
        ("RY-MV", "Marlon Vera"),
        ("RY-ND", "Nicolas Dalby"),
        ("RY-NM", "Neil Magny"),
        ("RY-PR", "Piera Rodriguez"),
        ("RY-RB", "Randy Brown"),
        ("RY-RN", "Ryan Spann"),
        ("RY-RS", "Ricky Simon"),
        ("RY-SB", "Sean Brady"),
        ("RY-TF", "Tony Ferguson"),
        ("RY-TG", "Themba Gorimbo"),
        ("RY-TM", "Thiago Moises"),
        ("RY-VJ", "Virna Jandiroba"),
        ("RY-YJ", "Yazmin Jauregui"),
    ]),

    ("Royalty Relic Signatures", [
        ("RYR-AM", "Alonzo Menifield"),
        ("RYR-AY", "Adrian Yanez"),
        ("RYR-AZ", "Aiemann Zahabi"),
        ("RYR-BH", "Brady Hiestand"),
        ("RYR-CD", "Cody Durden"),
        ("RYR-CR", "Christian Rodriguez"),
        ("RYR-CS", "Cameron Saaiman"),
        ("RYR-DR", "Dominick Reyes"),
        ("RYR-EB", "Edson Barboza"),
        ("RYR-FP", "Fernando Padilla"),
        ("RYR-GC", "Giga Chikadze"),
        ("RYR-GM", "Gabriel Miranda"),
        ("RYR-GN", "Geoff Neal"),
        ("RYR-JA", "Joel Alvarez"),
        ("RYR-JC", "Joshua Culibao"),
        ("RYR-JJ", "Jasmine Jasudavicius"),
        ("RYR-JM", "Jake Matthews"),
        ("RYR-JT", "Jalin Turner"),
        ("RYR-KC", "Khamzat Chimaev"),
        ("RYR-KG", "King Green"),
        ("RYR-KK", "Karolina Kowalkiewicz"),
        ("RYR-KS", "Karine Silva"),
        ("RYR-MA", "Mario Bautista"),
        ("RYR-MB", "Mayra Bueno"),
        ("RYR-MD", "Michael Davis"),
        ("RYR-MM", "Molly McCann"),
        ("RYR-MP", "Michel Pereira"),
        ("RYR-MR", "Mateusz Rębecki"),
        ("RYR-MT", "Marcin Tybura"),
        ("RYR-MV", "Marvin Vettori"),
        ("RYR-MZ", "Marina Rodriguez"),
        ("RYR-PC", "Paul Craig"),
        ("RYR-RF", "Rafael Fiziev"),
        ("RYR-SW", "Sean Woodson"),
        ("RYR-TE", "Tim Elliott"),
        ("RYR-TT", "Tai Tuivasa"),
        ("RYR-YS", "Yadong Song"),
    ]),

    ("Superior Relic Signatures", [
        ("SRS-AA", "Amir Albazi"),
        ("SRS-AL", "Alexander Volkov"),
        ("SRS-AP", "Alex Pereira"),
        ("SRS-AV", "Alexander Volkanovski"),
        ("SRS-BM", "Brandon Moreno"),
        ("SRS-BR", "Brandon Royval"),
        ("SRS-CB", "Curtis Blaydes"),
        ("SRS-CC", "Colby Covington"),
        ("SRS-CG", "Ciryl Gane"),
        ("SRS-IA", "Irene Aldana"),
        ("SRS-IL", "Iasmin Lucindo"),
        ("SRS-IV", "Ikram Aliskerov"),
        ("SRS-JB", "Jan Błachowicz"),
        ("SRS-JJ", "Jon Jones"),
        ("SRS-JO", "José Aldo"),
        ("SRS-JW", "Johnny Walker"),
        ("SRS-KH", "Kevin Holland"),
        ("SRS-MC", "Michael Chandler"),
        ("SRS-MG", "Mateusz Gamrot"),
        ("SRS-MH", "Max Holloway"),
        ("SRS-RD", "Roman Dolidze"),
        ("SRS-RM", "Renato Moicano"),
        ("SRS-RP", "Raquel Pennington"),
        ("SRS-SB", "Sean Brady"),
        ("SRS-TC", "Tracy Cortez"),
        ("SRS-TR", "Tabatha Ricci"),
        ("SRS-VJ", "Virna Jandiroba"),
    ]),

    ("Superior Signatures", [
        ("SS-AA", "Arnold Allen"),
        ("SS-AT", "Arman Tsarukyan"),
        ("SS-BM", "Belal Muhammad"),
        ("SS-CC", "Colby Covington"),
        ("SS-DH", "Daniel Hooker"),
        ("SS-DP", "Dustin Poirier"),
        ("SS-HC", "Hunter Campbell"),
        ("SS-IA", "Ikram Aliskerov"),
        ("SS-IL", "Iasmin Lucindo"),
        ("SS-JM", "Jack Della Maddalena"),
        ("SS-JP", "Julianna Peña"),
        ("SS-KC", "Katlyn Cerminara"),
        ("SS-KH", "Kayla Harrison"),
        ("SS-KV", "Ketlen Vieira"),
        ("SS-LE", "Leon Edwards"),
        ("SS-MC", "Michael Chandler"),
        ("SS-RR", "Raul Rosas"),
        ("SS-TA", "Tom Aspinall"),
    ]),

    ("Supreme Royalty Signatures", [
        ("SUR-AL", "Amanda Lemos"),
        ("SUR-AT", "Arman Tsarukyan"),
        ("SUR-CB", "Caio Borralho"),
        ("SUR-CO", "Charles Oliveira"),
        ("SUR-DL", "Diego Lopes"),
        ("SUR-DP", "Dustin Poirier"),
        ("SUR-IA", "Israel Adesanya"),
        ("SUR-IT", "Ilia Topuria"),
        ("SUR-JB", "Javid Basharat"),
        ("SUR-JH", "Jamahal Hill"),
        ("SUR-JJ", "Jon Jones"),
        ("SUR-JM", "Jack Della Maddalena"),
        ("SUR-JP", "Julianna Peña"),
        ("SUR-KH", "Kayla Harrison"),
        ("SUR-KK", "Kai Kara-France"),
        ("SUR-MD", "Merab Dvalishvili"),
        ("SUR-MN", "Mackenzie Dern"),
        ("SUR-PP", "Paddy Pimblett"),
        ("SUR-RN", "Rose Namajunas"),
        ("SUR-RW", "Robert Whittaker"),
        ("SUR-SM", "Sean O'Malley"),
        ("SUR-SR", "Shavkat Rakhmonov"),
        ("SUR-SS", "Sean Strickland"),
        ("SUR-TA", "Tom Aspinall"),
        ("SUR-UN", "Umar Nurmagomedov"),
        ("SUR-VS", "Valentina Shevchenko"),
        ("SUR-YX", "Yan Xiaonan"),
        ("SUR-ZW", "Zhang Weili"),
    ]),

    ("The Time Is Now", [
        ("TIS-AA", "Assu Almabayev"),
        ("TIS-BN", "Bo Nickal"),
        ("TIS-CP", "Carlos Prates"),
        ("TIS-DL", "Diego Lopes"),
        ("TIS-JM", "Jonathan Martinez"),
        ("TIS-JS", "Jean Silva"),
        ("TIS-KA", "Kai Asakura"),
        ("TIS-MB", "Maycee Barber"),
        ("TIS-PP", "Paddy Pimblett"),
        ("TIS-RK", "Roman Kopylov"),
        ("TIS-RR", "Reinier de Ridder"),
        ("TIS-SG", "Shamil Gaziev"),
        ("TIS-SR", "Shavkat Rakhmonov"),
        ("TIS-UN", "Umar Nurmagomedov"),
        ("TIS-VO", "Vinicius Oliveira"),
    ]),

    ("Triple Auto", [
        ("TA-GHP", "Dustin Poirier / Justin Gaethje / Max Holloway"),
        ("TA-NMN", "Khabib Nurmagomedov / Umar Nurmagomedov / Islam Makhachev"),
        ("TA-RSP", "Anderson Silva / Mauricio Santos / Carlos Prates"),
        ("TA-SJS", "Jon Jones / Anderson Silva / Georges St-Pierre"),
        ("TA-ZSH", "Kayla Harrison / Zhang Weili / Valentina Shevchenko"),
    ]),

    # ── Relic-only sets ──────────────────────────────────────

    ("Grand Royal Relics", [
        ("GR-AL", "Amanda Lemos"),
        ("GR-AP", "Alex Pereira"),
        ("GR-AS", "Aljamain Sterling"),
        ("GR-BM", "Belal Muhammad"),
        ("GR-BR", "Brandon Royval"),
        ("GR-CB", "Caio Borralho"),
        ("GR-DD", "Dricus du Plessis"),
        ("GR-DP", "Dustin Poirier"),
        ("GR-HC", "Henry Cejudo"),
        ("GR-IA", "Israel Adesanya"),
        ("GR-IT", "Ilia Topuria"),
        ("GR-JA", "José Aldo"),
        ("GR-JB", "Jan Błachowicz"),
        ("GR-JJ", "Jon Jones"),
        ("GR-JP", "Jiri Prochazka"),
        ("GR-MA", "Magomed Ankalaev"),
        ("GR-RN", "Rose Namajunas"),
        ("GR-RP", "Raquel Pennington"),
        ("GR-TA", "Tom Aspinall"),
        ("GR-VS", "Valentina Shevchenko"),
    ]),

    ("Prodigious Pairings", [
        ("PRP-AP", "Alex Pereira / Israel Adesanya"),
        ("PRP-AT", "Tatsuro Taira / Kai Asakura"),
        ("PRP-CS", "Sean Strickland / Colby Covington"),
        ("PRP-JA", "Tom Aspinall / Jon Jones"),
        ("PRP-MN", "Umar Nurmagomedov / Islam Makhachev"),
        ("PRP-PB", "Carlos Prates / Caio Borralho"),
        ("PRP-PC", "Michael Chandler / Dustin Poirier"),
        ("PRP-PH", "Julianna Peña / Kayla Harrison"),
        ("PRP-SS", "Mauricio Santos / Jean Silva"),
        ("PRP-TD", "Ilia Topuria / Merab Dvalishvili"),
    ]),

    ("Regalia Relics", [
        ("RR-AL", "Alexander Volkanovski"),
        ("RR-AM", "Alonzo Menifield"),
        ("RR-AV", "Alexander Volkov"),
        ("RR-AZ", "Aiemann Zahabi"),
        ("RR-BA", "Brendan Allen"),
        ("RR-CG", "Ciryl Gane"),
        ("RR-CO", "Charles Oliveira"),
        ("RR-CS", "Cory Sandhagen"),
        ("RR-DH", "Daniel Hooker"),
        ("RR-IA", "Irene Aldana"),
        ("RR-JA", "Jessica Andrade"),
        ("RR-JG", "Justin Gaethje"),
        ("RR-JJ", "Jasmine Jasudavicius"),
        ("RR-KC", "Khamzat Chimaev"),
        ("RR-KH", "Kayla Harrison"),
        ("RR-MC", "Michael Chandler"),
        ("RR-MH", "Max Holloway"),
        ("RR-MK", "Manel Kape"),
        ("RR-MT", "Miesha Tate"),
        ("RR-MV", "Marvin Vettori"),
        ("RR-ND", "Natalia Cristina da Silva"),
        ("RR-PC", "Paul Craig"),
        ("RR-PP", "Paddy Pimblett"),
        ("RR-RF", "Rafael Fiziev"),
        ("RR-SB", "Sean Brady"),
        ("RR-SS", "Serghei Spivac"),
        ("RR-TC", "Tracy Cortez"),
        ("RR-TR", "Tabatha Ricci"),
        ("RR-TT", "Tatsuro Taira"),
        ("RR-YJ", "Yazmin Jauregui"),
        ("RR-YR", "Yair Rodríguez"),
        ("RR-YS", "Yadong Song"),
        ("RR-ZW", "Zhang Weili"),
    ]),

    ("Relic Jewels", [
        ("RJ-AG", "Alexa Grasso"),
        ("RJ-AH", "Angela Hill"),
        ("RJ-AP", "Alex Perez"),
        ("RJ-AR", "Aleksandar Rakic"),
        ("RJ-AS", "Anthony Smith"),
        ("RJ-BH", "Brady Hiestand"),
        ("RJ-CB", "Curtis Blaydes"),
        ("RJ-CC", "Chelsea Chandler"),
        ("RJ-CH", "Chase Hooper"),
        ("RJ-CO", "Casey O'Neill"),
        ("RJ-DL", "Diego Lopes"),
        ("RJ-EB", "Erin Blanchfield"),
        ("RJ-GB", "Gilbert Burns"),
        ("RJ-GN", "Geoff Neal"),
        ("RJ-IA", "Ikram Aliskerov"),
        ("RJ-JM", "Jailton Malhadinho"),
        ("RJ-JP", "Joe Pyfer"),
        ("RJ-JT", "Jalin Turner"),
        ("RJ-KC", "Katlyn Cerminara"),
        ("RJ-KF", "Kai Kara-France"),
        ("RJ-KK", "Karolina Kowalkiewicz"),
        ("RJ-LE", "Leon Edwards"),
        ("RJ-LK", "Ludovit Klein"),
        ("RJ-MB", "Mario Bautista"),
        ("RJ-MD", "Merab Dvalishvili"),
        ("RJ-MK", "Miranda Maverick"),
        ("RJ-MM", "Michael Morales"),
        ("RJ-MT", "Marcin Tybura"),
        ("RJ-ND", "Norma Dumont"),
        ("RJ-NI", "Nassourdine Imavov"),
        ("RJ-NK", "Nikita Krylov"),
        ("RJ-RD", "Roman Dolidze"),
        ("RJ-RF", "Rinat Fakhretdinov"),
        ("RJ-SP", "Sergei Pavlovich"),
        ("RJ-SR", "Shavkat Rakhmonov"),
        ("RJ-SS", "Sean Strickland"),
        ("RJ-TU", "Tagir Ulanbekov"),
    ]),

    ("Rookie Jumbo Relics", [
        ("RJR-AA", "Assu Almabayev"),
        ("RJR-AP", "Ailin Perez"),
        ("RJR-BG", "Bogdan Guskov"),
        ("RJR-CD", "Christian Duncan"),
        ("RJR-CJ", "Charles Jourdain"),
        ("RJR-CP", "Carlos Prates"),
        ("RJR-DB", "Danny Barlow"),
        ("RJR-DM", "Daniel Marcos"),
        ("RJR-DZ", "Daniel Zellhuber"),
        ("RJR-EM", "Eduarda Moura"),
        ("RJR-ER", "Esteban Ribovics"),
        ("RJR-FB", "Farid Basharat"),
        ("RJR-GB", "Gabriel Bonfim"),
        ("RJR-HP", "Hyunsung Park"),
        ("RJR-IB", "Ismael Bonfim"),
        ("RJR-JB", "Joanderson Brito"),
        ("RJR-JL", "Jose Mariscal"),
        ("RJR-JM", "Jean Matsumoto"),
        ("RJR-JS", "Jean Silva"),
        ("RJR-JV", "Joshua Van"),
        ("RJR-JZ", "Jonathan Martinez"),
        ("RJR-KA", "Kai Asakura"),
        ("RJR-LS", "Luana Santos"),
        ("RJR-MB", "Modestas Bukauskas"),
        ("RJR-MC", "Marcus McGhee"),
        ("RJR-MM", "Melissa Mullins"),
        ("RJR-MN", "Muhammadjon Naimov"),
        ("RJR-MO", "Myktybek Orolbai"),
        ("RJR-MS", "Mauricio Santos"),
        ("RJR-NA", "Nurullo Aliev"),
        ("RJR-NL", "Nate Landwehr"),
        ("RJR-NS", "Nazim Sadykhov"),
        ("RJR-PT", "Payton Talbott"),
        ("RJR-RB", "Rodolfo Bellato"),
        ("RJR-RK", "Roman Kopylov"),
        ("RJR-RN", "Rinya Nakamura"),
        ("RJR-RR", "Reinier de Ridder"),
        ("RJR-SE", "Stephen Erceg"),
        ("RJR-SG", "Shamil Gaziev"),
        ("RJR-TK", "Toshiomi Kazama"),
        ("RJR-TP", "Trevor Peek"),
        ("RJR-TW", "Trey Waters"),
        ("RJR-VH", "Victor Henry"),
        ("RJR-VO", "Vinicius Oliveira"),
        ("RJR-VP", "Vitor Petrino"),
        ("RJR-WA", "Waldo Cortes"),
        ("RJR-WW", "Westin Wilson"),
    ]),

    ("Star Relics", [
        ("SR-AA", "Arnold Allen"),
        ("SR-AI", "Amir Albazi"),
        ("SR-AP", "Alexandre Pantoja"),
        ("SR-AT", "Arman Tsarukyan"),
        ("SR-BM", "Brandon Moreno"),
        ("SR-BO", "Brian Ortega"),
        ("SR-BS", "Benoit Saint Denis"),
        ("SR-CA", "Cameron Saaiman"),
        ("SR-CC", "Colby Covington"),
        ("SR-CR", "Christian Rodriguez"),
        ("SR-CU", "Carlos Ulberg"),
        ("SR-DI", "Dan Ige"),
        ("SR-IG", "Ian Machado Garry"),
        ("SR-IL", "Iasmin Lucindo"),
        ("SR-IM", "Islam Makhachev"),
        ("SR-JA", "Jack Della Maddalena"),
        ("SR-JB", "Joaquin Buckley"),
        ("SR-JH", "Jamahal Hill"),
        ("SR-JM", "Jeff Molina"),
        ("SR-JP", "Julianna Peña"),
        ("SR-JW", "Johnny Walker"),
        ("SR-KH", "Kevin Holland"),
        ("SR-KV", "Ketlen Vieira"),
        ("SR-MA", "Michel Pereira"),
        ("SR-MB", "Maycee Barber"),
        ("SR-MD", "Mackenzie Dern"),
        ("SR-ME", "Movsar Evloev"),
        ("SR-MF", "Manon Fiorot"),
        ("SR-MG", "Mateusz Gamrot"),
        ("SR-MO", "Mayra Bueno"),
        ("SR-MP", "Michael Page"),
        ("SR-MR", "Mateusz Rębecki"),
        ("SR-MV", "Marlon Vera"),
        ("SR-PC", "Paulo Costa"),
        ("SR-RM", "Renato Moicano"),
        ("SR-RR", "Raul Rosas"),
        ("SR-RS", "Ryan Spann"),
        ("SR-RW", "Robert Whittaker"),
        ("SR-SM", "Sharabutdin Magomedov"),
        ("SR-SO", "Sean O'Malley"),
        ("SR-ST", "Stephen Thompson"),
        ("SR-TS", "Tatiana Suarez"),
        ("SR-TT", "Tai Tuivasa"),
        ("SR-UN", "Umar Nurmagomedov"),
        ("SR-VL", "Vicente Luque"),
        ("SR-VO", "Volkan Oezdemir"),
        ("SR-YX", "Yan Xiaonan"),
    ]),

    ("Liquid Silver", [
        ("LS-1",  "Islam Makhachev"),
        ("LS-2",  "Alexander Volkanovski"),
        ("LS-3",  "Charles Oliveira"),
        ("LS-4",  "Dricus du Plessis"),
        ("LS-5",  "Merab Dvalishvili"),
        ("LS-6",  "Zhang Weili"),
        ("LS-7",  "Dustin Poirier"),
        ("LS-8",  "Kayla Harrison"),
        ("LS-9",  "Paddy Pimblett"),
        ("LS-10", "Georges St-Pierre"),
    ]),
]


# ─────────────────────────────────────────────────────────────
# Card builder
# ─────────────────────────────────────────────────────────────

def build_cards(section_name: str, raw_cards: list) -> list:
    """Convert raw (card_number, player_str) tuples into card dicts."""
    is_multi = section_name in MULTI_PLAYER_SECTIONS
    cards = []

    for card_number, player_str in raw_cards:
        if is_multi and " / " in player_str:
            parts = [p.strip() for p in player_str.split(" / ")]
            for player in parts:
                is_rc = player in ROOKIE_FIGHTERS
                cards.append({
                    "card_number": card_number,
                    "player": player,
                    "team": "",
                    "is_rookie": is_rc,
                    "subset": None,
                })
        else:
            is_rc = player_str in ROOKIE_FIGHTERS
            cards.append({
                "card_number": card_number,
                "player": player_str,
                "team": "",
                "is_rookie": is_rc,
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
        unique_cards += 1  # base appearance
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
        "set_name": "2025 Topps Royalty UFC",
        "sport": "MMA",
        "season": "2025",
        "league": "UFC",
        "sections": sections,
        "players": players,
    }


# ─────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Parsing 2025 Topps Royalty UFC checklist...")

    sections = []
    for section_name, raw_cards in SECTIONS_DATA:
        parallels = SECTION_PARALLELS.get(section_name, [])
        cards = build_cards(section_name, raw_cards)
        sections.append({
            "insert_set": section_name,
            "parallels": parallels,
            "cards": cards,
        })

    output = build_output(sections)

    out_path = "ufc_royalty_parsed.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nSet: {output['set_name']} ({output['season']})")
    print(f"Sections: {len(output['sections'])}")
    for s in output["sections"]:
        print(f"  {s['insert_set']}: {len(s['cards'])} cards, {len(s['parallels'])} parallels")

    print(f"\nTotal players: {len(output['players'])}")

    # ── Spot-check: Jon Jones ─────────────────────────────────
    player_map = {p["player"]: p for p in output["players"]}
    print("\n=== SPOT CHECK: Jon Jones ===")
    if "Jon Jones" in player_map:
        jj = player_map["Jon Jones"]
        st = jj["stats"]
        print(f"  Insert sets:  {st['insert_sets']}")
        print(f"  Unique cards: {st['unique_cards']}")
        print(f"  1/1s:         {st['one_of_ones']}")
        for a in jj["appearances"]:
            print(f"  [{a['insert_set']}] #{a['card_number']} | parallels={len(a['parallels'])}")

    # ── Spot-check: Rookie count ──────────────────────────────
    base_section = next((s for s in output["sections"] if s["insert_set"] == "Base Set"), None)
    if base_section:
        rc_count = sum(1 for c in base_section["cards"] if c["is_rookie"])
        print(f"\n=== Base Set RC count: {rc_count} ===")

    # ── Spot-check: multi-player co-players ───────────────────
    da_section = next((s for s in output["sections"] if s["insert_set"] == "Dual Auto"), None)
    if da_section:
        from collections import Counter
        nums = Counter(c["card_number"] for c in da_section["cards"])
        multi = {k: v for k, v in nums.items() if v > 1}
        print(f"\n=== Dual Auto multi-player cards: {len(multi)} ===")
        for card_num, count in list(multi.items())[:3]:
            players_on_card = [c["player"] for c in da_section["cards"] if c["card_number"] == card_num]
            print(f"  {card_num}: {' / '.join(players_on_card)}")
