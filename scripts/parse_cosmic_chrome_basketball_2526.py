#!/usr/bin/env python3
"""Parser for 2025-26 Topps Cosmic Chrome Basketball."""
import json
import re
from collections import defaultdict

# ---------------------------------------------------------------------------
# Name normalization
# ---------------------------------------------------------------------------
NAME_FIXES = {
    "alperun sengun":        "Alperen Sengun",
    "bennedict mathurin":    "Bennedict Mathurin",
    "paul pierce":           "Paul Pierce",
    "peja stojakovic":       "Peja Stojakovic",
}

def fix_name(raw: str) -> str:
    s = raw.strip()
    key = s.lower()
    return NAME_FIXES.get(key, s)

# ---------------------------------------------------------------------------
# Parallels
# ---------------------------------------------------------------------------
PLANETARY_PURSUIT_PARALLELS = [
    {"name": "Sun",     "print_run": None},
    {"name": "Mercury", "print_run": None},
    {"name": "Venus",   "print_run": None},
    {"name": "Earth",   "print_run": None},
    {"name": "Mars",    "print_run": None},
    {"name": "Jupiter", "print_run": None},
    {"name": "Saturn",  "print_run": None},
    {"name": "Uranus",  "print_run": None},
    {"name": "Neptune", "print_run": None},
    {"name": "Pluto",   "print_run": None},
]

NO_PARALLELS = []

# ---------------------------------------------------------------------------
# Base Set (200 cards)
# Each tuple: (card_number, player_name, team, is_rookie)
# Card #101 (Nikola Jović) is stored as card number "48" per the sequence;
# the Topps label of #101 is ignored.
# ---------------------------------------------------------------------------
BASE_SET_RAW = [
    ("1",   "Jaren Jackson Jr.",          "Memphis Grizzlies",         False),
    ("2",   "RJ Barrett",                 "Toronto Raptors",           False),
    ("3",   "Quentin Grimes",             "Philadelphia 76ers",        False),
    ("4",   "Jaden McDaniels",            "Minnesota Timberwolves",    False),
    ("5",   "Buddy Hield",                "Golden State Warriors",     False),
    ("6",   "Jaime Jaquez Jr.",           "Miami Heat",                False),
    ("7",   "Cedric Coward",              "Memphis Grizzlies",         True),
    ("8",   "Jalen Brunson",              "New York Knicks",           False),
    ("9",   "Ivica Zubac",                "Los Angeles Clippers",      False),
    ("10",  "Dereck Lively II",           "Dallas Mavericks",          False),
    ("11",  "Shai Gilgeous-Alexander",    "Oklahoma City Thunder",     False),
    ("12",  "Cooper Flagg",               "Dallas Mavericks",          True),
    ("13",  "Ryan Kalkbrenner",           "Charlotte Hornets",         True),
    ("14",  "Christian Braun",            "Denver Nuggets",            False),
    ("15",  "Trae Young",                 "Atlanta Hawks",             False),
    ("16",  "Kris Murray",                "Portland Trail Blazers",    False),
    ("17",  "Khaman Maluach",             "Phoenix Suns",              True),
    ("18",  "Stephen Curry",              "Golden State Warriors",     False),
    ("19",  "Lonzo Ball",                 "Chicago Bulls",             False),
    ("20",  "Anthony Black",              "Orlando Magic",             False),
    ("21",  "Jaden Ivey",                 "Detroit Pistons",           False),
    ("22",  "Klay Thompson",              "Dallas Mavericks",          False),
    ("23",  "Keegan Murray",              "Sacramento Kings",          False),
    ("24",  "Bennedict Mathurin",         "Indiana Pacers",            False),
    ("25",  "Jeremy Sochan",              "San Antonio Spurs",         False),
    ("26",  "Alex Sarr",                  "Washington Wizards",        False),
    ("27",  "Jonathan Kuminga",           "Golden State Warriors",     False),
    ("28",  "Joel Embiid",                "Philadelphia 76ers",        False),
    ("29",  "Jalen Johnson",              "Atlanta Hawks",             False),
    ("30",  "Stephon Castle",             "San Antonio Spurs",         False),
    ("31",  "Kam Jones",                  "Indiana Pacers",            True),
    ("32",  "Jamal Murray",               "Denver Nuggets",            False),
    ("33",  "Jalen Green",                "Houston Rockets",           False),
    ("34",  "Grant Williams",             "Charlotte Hornets",         False),
    ("35",  "VJ Edgecombe",               "Philadelphia 76ers",        True),
    ("36",  "OG Anunoby",                 "New York Knicks",           False),
    ("37",  "Dyson Daniels",              "Atlanta Hawks",             False),
    ("38",  "Jayson Tatum",               "Boston Celtics",            False),
    ("39",  "Egor Dëmin",                 "Brooklyn Nets",             True),
    ("40",  "Adou Thiero",                "Los Angeles Lakers",        True),
    ("41",  "DeMar DeRozan",              "Sacramento Kings",          False),
    ("42",  "Franz Wagner",               "Orlando Magic",             False),
    ("43",  "Russell Westbrook",          "Denver Nuggets",            False),
    ("44",  "Alperen Sengun",             "Houston Rockets",           False),
    ("45",  "Dejounte Murray",            "New Orleans Pelicans",      False),
    ("46",  "Pascal Siakam",              "Indiana Pacers",            False),
    ("47",  "Paolo Banchero",             "Orlando Magic",             False),
    ("48",  "Nikola Jović",               "Miami Heat",                False),
    ("49",  "Jeremiah Fears",             "New Orleans Pelicans",      True),
    ("50",  "Mark Williams",              "Charlotte Hornets",         False),
    ("51",  "Scotty Pippen Jr.",           "Memphis Grizzlies",         False),
    ("52",  "Zaccharie Risacher",         "Atlanta Hawks",             False),
    ("53",  "Thomas Sorber",              "Oklahoma City Thunder",     True),
    ("54",  "Naz Reid",                   "Minnesota Timberwolves",    False),
    ("55",  "Matas Buzelis",              "Chicago Bulls",             False),
    ("56",  "Gary Trent Jr.",             "Milwaukee Bucks",           False),
    ("57",  "Tyrese Maxey",               "Philadelphia 76ers",        False),
    ("58",  "Tyler Herro",                "Miami Heat",                False),
    ("59",  "Andrew Nembhard",            "Indiana Pacers",            False),
    ("60",  "Michael Porter Jr.",         "Denver Nuggets",            False),
    ("61",  "Drake Powell",               "Brooklyn Nets",             True),
    ("62",  "DaRon Holmes II",            "Denver Nuggets",            False),
    ("63",  "Aaron Gordon",               "Denver Nuggets",            False),
    ("64",  "Trey Murphy III",            "New Orleans Pelicans",      False),
    ("65",  "Max Christie",               "Dallas Mavericks",          False),
    ("66",  "Luka Dončić",                "Los Angeles Lakers",        False),
    ("67",  "Ryan Dunn",                  "Phoenix Suns",              False),
    ("68",  "Payton Pritchard",           "Boston Celtics",            False),
    ("69",  "Bradley Beal",               "Phoenix Suns",              False),
    ("70",  "Noa Essengue",               "Chicago Bulls",             True),
    ("71",  "Deni Avdija",                "Portland Trail Blazers",    False),
    ("72",  "Brandon Miller",             "Charlotte Hornets",         False),
    ("73",  "Yang Hansen",                "Portland Trail Blazers",    True),
    ("74",  "Evan Mobley",                "Cleveland Cavaliers",       False),
    ("75",  "Alijah Martin",              "Toronto Raptors",           True),
    ("76",  "Cole Anthony",               "Orlando Magic",             False),
    ("77",  "Rui Hachimura",              "Los Angeles Lakers",        False),
    ("78",  "James Harden",               "Los Angeles Clippers",      False),
    ("79",  "Josh Hart",                  "New York Knicks",           False),
    ("80",  "Mikal Bridges",              "New York Knicks",           False),
    ("81",  "Domantas Sabonis",           "Sacramento Kings",          False),
    ("82",  "Ben Saraf",                  "Brooklyn Nets",             True),
    ("83",  "Kawhi Leonard",              "Los Angeles Clippers",      False),
    ("84",  "Donte DiVincenzo",           "Minnesota Timberwolves",    False),
    ("85",  "Jared McCain",               "Philadelphia 76ers",        False),
    ("86",  "Zach Collins",               "Chicago Bulls",             False),
    ("87",  "Asa Newell",                 "Atlanta Hawks",             True),
    ("88",  "Malik Monk",                 "Sacramento Kings",          False),
    ("89",  "Zach LaVine",                "Sacramento Kings",          False),
    ("90",  "Tyrese Haliburton",          "Indiana Pacers",            False),
    ("91",  "Jakob Poeltl",               "Toronto Raptors",           False),
    ("92",  "Derik Queen",                "New Orleans Pelicans",      True),
    ("93",  "Gradey Dick",                "Toronto Raptors",           False),
    ("94",  "Jaxson Hayes",               "Los Angeles Lakers",        False),
    ("95",  "Nikola Jokić",               "Denver Nuggets",            False),
    ("96",  "Myles Turner",               "Indiana Pacers",            False),
    ("97",  "Kasparas Jakučionis",        "Miami Heat",                True),
    ("98",  "Kyshawn George",             "Washington Wizards",        False),
    ("99",  "Nique Clifford",             "Sacramento Kings",          True),
    ("100", "Collin Murray-Boyles",       "Toronto Raptors",           True),
    ("101", "Darius Garland",             "Cleveland Cavaliers",       False),
    ("102", "Donovan Mitchell",           "Cleveland Cavaliers",       False),
    ("103", "Alex Caruso",                "Oklahoma City Thunder",     False),
    ("104", "Walter Clayton Jr.",         "Utah Jazz",                 True),
    ("105", "Derrick White",              "Boston Celtics",            False),
    ("106", "Tobias Harris",              "Detroit Pistons",           False),
    ("107", "Khris Middleton",            "Washington Wizards",        False),
    ("108", "Kyle Kuzma",                 "Milwaukee Bucks",           False),
    ("109", "Paul George",                "Philadelphia 76ers",        False),
    ("110", "Danny Wolf",                 "Brooklyn Nets",             True),
    ("111", "Draymond Green",             "Golden State Warriors",     False),
    ("112", "Jaylen Brown",               "Boston Celtics",            False),
    ("113", "Terrence Shannon Jr.",       "Minnesota Timberwolves",    False),
    ("114", "Jabari Smith Jr.",           "Houston Rockets",           False),
    ("115", "Tre Johnson III",            "Washington Wizards",        True),
    ("116", "Yanic Konan-Niederhäuser",   "Los Angeles Clippers",      True),
    ("117", "Andrew Wiggins",             "Miami Heat",                False),
    ("118", "Josh Giddey",                "Chicago Bulls",             False),
    ("119", "Will Riley",                 "Washington Wizards",        True),
    ("120", "Walker Kessler",             "Utah Jazz",                 False),
    ("121", "John Tonje",                 "Utah Jazz",                 True),
    ("122", "Naji Marshall",              "Dallas Mavericks",          False),
    ("123", "De'Aaron Fox",               "San Antonio Spurs",         False),
    ("124", "LaMelo Ball",                "Charlotte Hornets",         False),
    ("125", "Johni Broome",               "Philadelphia 76ers",        True),
    ("126", "Chet Holmgren",              "Oklahoma City Thunder",     False),
    ("127", "Micah Peavy",                "New Orleans Pelicans",      True),
    ("128", "Jamir Watkins",              "Washington Wizards",        True),
    ("129", "Damian Lillard",             "Milwaukee Bucks",           False),
    ("130", "Jalen Williams",             "Oklahoma City Thunder",     False),
    ("131", "Ja Morant",                  "Memphis Grizzlies",         False),
    ("132", "Bam Adebayo",                "Miami Heat",                False),
    ("133", "Maxime Raynaud",             "Sacramento Kings",          True),
    ("134", "Ausar Thompson",             "Detroit Pistons",           False),
    ("135", "Ayo Dosunmu",                "Chicago Bulls",             False),
    ("136", "Fred VanVleet",              "Houston Rockets",           False),
    ("137", "Cade Cunningham",            "Detroit Pistons",           False),
    ("138", "Max Strus",                  "Cleveland Cavaliers",       False),
    ("139", "Carter Bryant",              "San Antonio Spurs",         True),
    ("140", "Tyrese Proctor",             "Cleveland Cavaliers",       True),
    ("141", "Coby White",                 "Chicago Bulls",             False),
    ("142", "Al Horford",                 "Boston Celtics",            False),
    ("143", "Kristaps Porzingis",         "Boston Celtics",            False),
    ("144", "Jase Richardson",            "Orlando Magic",             True),
    ("145", "Anthony Davis",              "Dallas Mavericks",          False),
    ("146", "Chris Paul",                 "San Antonio Spurs",         False),
    ("147", "Koby Brea",                  "Phoenix Suns",              True),
    ("148", "Julius Randle",              "Minnesota Timberwolves",    False),
    ("149", "Victor Wembanyama",          "San Antonio Spurs",         False),
    ("150", "Cam Thomas",                 "Brooklyn Nets",             False),
    ("151", "Anfernee Simons",            "Portland Trail Blazers",    False),
    ("152", "Brooks Barnhizer",           "Oklahoma City Thunder",     True),
    ("153", "Liam McNeeley",              "Charlotte Hornets",         True),
    ("154", "Brandin Podziemski",         "Golden State Warriors",     False),
    ("155", "Bobby Portis",               "Milwaukee Bucks",           False),
    ("156", "Sion James",                 "Charlotte Hornets",         True),
    ("157", "LeBron James",               "Los Angeles Lakers",        False),
    ("158", "Kyrie Irving",               "Dallas Mavericks",          False),
    ("159", "Austin Reaves",              "Los Angeles Lakers",        False),
    ("160", "Steven Adams",               "Houston Rockets",           False),
    ("161", "Jaylen Wells",               "Memphis Grizzlies",         False),
    ("162", "Joan Beringer",              "Minnesota Timberwolves",    True),
    ("163", "Brandon Ingram",             "New Orleans Pelicans",      False),
    ("164", "Keyonte George",             "Utah Jazz",                 False),
    ("165", "Anthony Edwards",            "Minnesota Timberwolves",    False),
    ("166", "Desmond Bane",               "Memphis Grizzlies",         False),
    ("167", "Karl-Anthony Towns",         "New York Knicks",           False),
    ("168", "Shaedon Sharpe",             "Portland Trail Blazers",    False),
    ("169", "Johnny Furphy",              "Indiana Pacers",            False),
    ("170", "Yves Missi",                 "New Orleans Pelicans",      False),
    ("171", "Ace Bailey",                 "Utah Jazz",                 True),
    ("172", "Hugo González",              "Boston Celtics",            True),
    ("173", "Zach Edey",                  "Memphis Grizzlies",         False),
    ("174", "Kevin Durant",               "Houston Rockets",           False),
    ("175", "Tristan da Silva",           "Orlando Magic",             False),
    ("176", "Jarrett Allen",              "Cleveland Cavaliers",       False),
    ("177", "Amen Thompson",              "Houston Rockets",           False),
    ("178", "Herbert Jones",              "New Orleans Pelicans",      False),
    ("179", "Scottie Barnes",             "Toronto Raptors",           False),
    ("180", "Jimmy Butler III",           "Golden State Warriors",     False),
    ("181", "Kel'el Ware",                "Miami Heat",                False),
    ("182", "Noah Penda",                 "Orlando Magic",             True),
    ("183", "T.J. McConnell",             "Indiana Pacers",            False),
    ("184", "Devin Booker",               "Phoenix Suns",              False),
    ("185", "Scoot Henderson",            "Portland Trail Blazers",    False),
    ("186", "Dylan Harper",               "San Antonio Spurs",         True),
    ("187", "Nolan Traore",               "Brooklyn Nets",             True),
    ("188", "Rasheer Fleming",            "Phoenix Suns",              True),
    ("189", "Jalen Duren",                "Detroit Pistons",           False),
    ("190", "Giannis Antetokounmpo",      "Milwaukee Bucks",           False),
    ("191", "Donovan Clingan",            "Portland Trail Blazers",    False),
    ("192", "Reed Sheppard",              "Houston Rockets",           False),
    ("193", "Luguentz Dort",              "Oklahoma City Thunder",     False),
    ("194", "Bub Carrington",             "Washington Wizards",        False),
    ("195", "Dalton Knecht",              "Los Angeles Lakers",        False),
    ("196", "Miles McBride",              "New York Knicks",           False),
    ("197", "Kon Knueppel",               "Charlotte Hornets",         True),
    ("198", "Lauri Markkanen",            "Utah Jazz",                 False),
    ("199", "Chaz Lanier",                "Detroit Pistons",           True),
    ("200", "Ronald Holland II",          "Detroit Pistons",           False),
]

# ---------------------------------------------------------------------------
# Insert / Autograph sets — raw lines
# Each line: "CARD_NUM Player Name, Team [RC]"
# ---------------------------------------------------------------------------

COSMIC_CHROME_AUTOS_RAW = """CCA-AB Ace Bailey, Utah Jazz RC
CCA-AN Asa Newell, Atlanta Hawks RC
CCA-AT Adou Thiero, Los Angeles Lakers RC
CCA-BS Ben Saraf, Brooklyn Nets RC
CCA-CC Cedric Coward, Memphis Grizzlies RC
CCA-CF Cooper Flagg, Dallas Mavericks RC
CCA-CH Chet Holmgren, Oklahoma City Thunder
CCA-CM Collin Murray-Boyles, Toronto Raptors RC
CCA-DH Dylan Harper, San Antonio Spurs RC
CCA-DP Drake Powell, Brooklyn Nets RC
CCA-DQ Derik Queen, New Orleans Pelicans RC
CCA-DW Danny Wolf, Brooklyn Nets RC
CCA-ED Egor Dëmin, Brooklyn Nets RC
CCA-JB Jalen Brunson, New York Knicks
CCA-JBE Joan Beringer, Minnesota Timberwolves RC
CCA-JG Jalen Green, Houston Rockets
CCA-JH James Harden, Los Angeles Clippers
CCA-JJ Jaime Jaquez Jr., Miami Heat
CCA-JM Jamal Murray, Denver Nuggets
CCA-JR Jase Richardson, Orlando Magic RC
CCA-JS Jeremy Sochan, San Antonio Spurs
CCA-JT Jayson Tatum, Boston Celtics
CCA-KAT Karl-Anthony Towns, New York Knicks
CCA-KD Kevin Durant, Houston Rockets
CCA-KJ Kasparas Jakučionis, Miami Heat RC
CCA-KK Kon Knueppel, Charlotte Hornets RC
CCA-KM Khaman Maluach, Phoenix Suns RC
CCA-LJ LeBron James, Los Angeles Lakers
CCA-LM Liam McNeeley, Charlotte Hornets RC
CCA-MR Maxime Raynaud, Sacramento Kings RC
CCA-MS Max Strus, Cleveland Cavaliers
CCA-NC Nique Clifford, Sacramento Kings RC
CCA-NE Noa Essengue, Chicago Bulls RC
CCA-NP Noah Penda, Orlando Magic RC
CCA-NT Nolan Traore, Brooklyn Nets RC
CCA-PB Paolo Banchero, Orlando Magic
CCA-RF Rasheer Fleming, Phoenix Suns RC
CCA-SC Stephen Curry, Golden State Warriors
CCA-TH Tyrese Haliburton, Indiana Pacers
CCA-TP Tyrese Proctor, Cleveland Cavaliers RC
CCA-TS Terrence Shannon Jr., Minnesota Timberwolves
CCA-TSO Thomas Sorber, Oklahoma City Thunder RC
CCA-VW Victor Wembanyama, San Antonio Spurs
CCA-WC Walter Clayton Jr., Utah Jazz RC
CCA-WR Will Riley, Washington Wizards RC
CCA-YH Yang Hansen, Portland Trail Blazers RC
CCA-YK Yanic Konan-Niederhäuser, Los Angeles Clippers RC
CCA-YM Yves Missi, New Orleans Pelicans"""

COSMIC_CHROME_AUTOS_II_RAW = """CCAV-NJ Nikola Jokić, Denver Nuggets
CCAV-SGA Shai Gilgeous-Alexander, Oklahoma City Thunder"""

SINGULARITY_RAW = """SS-AM Alijah Martin, Toronto Raptors RC
SS-AN Aaron Nesmith, Indiana Pacers
SS-AT Adou Thiero, Los Angeles Lakers RC
SS-ATO Alex Toohey, Golden State Warriors RC
SS-AW Amari Williams, Boston Celtics
SS-BB Brooks Barnhizer, Oklahoma City Thunder RC
SS-CD Clyde Drexler, Portland Trail Blazers
SS-CJ Cameron Johnson, Brooklyn Nets
SS-CL Chaz Lanier, Detroit Pistons RC
SS-CM Collin Murray-Boyles, Toronto Raptors RC
SS-CW Cody Williams, Utah Jazz
SS-DDA Dyson Daniels, Atlanta Hawks
SS-DR Dennis Rodman, Chicago Bulls
SS-DRO David Robinson, San Antonio Spurs
SS-ED Egor Dëmin, Brooklyn Nets RC
SS-GDI Gradey Dick, Toronto Raptors
SS-HJ Herbert Jones, New Orleans Pelicans
SS-HO Hakeem Olajuwon, Houston Rockets
SS-JAL Jarrett Allen, Cleveland Cavaliers
SS-JGI Josh Giddey, Chicago Bulls
SS-JJ Jaren Jackson Jr., Memphis Grizzlies
SS-JK Jason Kidd, Dallas Mavericks
SS-JS Jamal Shead, Toronto Raptors
SS-JSM Javon Small, Memphis Grizzlies RC
SS-JT Jaylon Tyson, Cleveland Cavaliers
SS-JTO John Tonje, Utah Jazz RC
SS-JW Jamir Watkins, Washington Wizards RC
SS-KF Kyle Filipowski, Utah Jazz
SS-KJ Kam Jones, Indiana Pacers RC
SS-KK Kon Knueppel, Charlotte Hornets RC
SS-KMA Karl Malone, Utah Jazz
SS-KP Kristaps Porzingis, Boston Celtics
SS-LB Larry Bird, Boston Celtics
SS-LJ Larry Johnson, New York Knicks
SS-MJ Magic Johnson, Los Angeles Lakers
SS-NC Nique Clifford, Sacramento Kings RC
SS-NP Noah Penda, Orlando Magic RC
SS-NTO Nikola Topić, Oklahoma City Thunder
SS-RF Rasheer Fleming, Phoenix Suns RC
SS-RH Ronald Holland II, Detroit Pistons
SS-RHO Robert Horry, Los Angeles Lakers
SS-RK Ryan Kalkbrenner, Charlotte Hornets RC
SS-TS Tidjane Salaün, Charlotte Hornets
SS-WR Will Riley, Washington Wizards RC
SS-YK Yanic Konan-Niederhäuser, Los Angeles Clippers RC
SS-ZE Zach Edey, Memphis Grizzlies"""

ALIEN_AUTOS_RAW = """AA-AH Anfernee Hardaway, Orlando Magic
AA-AHO Aaron Holiday, Houston Rockets
AA-AI Allen Iverson, Philadelphia 76ers
AA-AN Asa Newell, Atlanta Hawks RC
AA-BC Bilal Coulibaly, Washington Wizards
AA-BJ Bronny James Jr., Los Angeles Lakers
AA-CM C.J. McCollum, New Orleans Pelicans
AA-CMU Collin Murray-Boyles, Toronto Raptors RC
AA-DG Daniel Gafford, Dallas Mavericks
AA-DW Dominique Wilkins, Atlanta Hawks
AA-DWO Danny Wolf, Brooklyn Nets RC
AA-ED Egor Dëmin, Brooklyn Nets RC
AA-FWA Franz Wagner, Orlando Magic
AA-GG George Gervin, San Antonio Spurs
AA-JR Jalen Rose, Indiana Pacers
AA-JS Jerry Stackhouse, Detroit Pistons
AA-JW Jason Williams, Sacramento Kings
AA-JWE Jaylen Wells, Memphis Grizzlies
AA-KG Kyshawn George, Washington Wizards
AA-MB Mikal Bridges, New York Knicks
AA-NC Nique Clifford, Sacramento Kings RC
AA-PP Paul Pierce, Boston Celtics
AA-PPR Payton Pritchard, Boston Celtics
AA-PS Peja Stojakovic, Sacramento Kings
AA-RD Ryan Dunn, Phoenix Suns
AA-RF Rasheer Fleming, Phoenix Suns RC
AA-TJE Ty Jerome, Cleveland Cavaliers
AA-TK Tyler Kolek, New York Knicks
AA-TP Tyrese Proctor, Cleveland Cavaliers RC
AA-VW Victor Wembanyama, San Antonio Spurs
AA-WC Walter Clayton Jr., Utah Jazz RC
AA-YK Yanic Konan-Niederhäuser, Los Angeles Clippers RC"""

ELECTRO_STATIC_SIGS_RAW = """ESS-AB Ace Bailey, Utah Jazz RC
ESS-AG Aaron Gordon, Denver Nuggets
ESS-AS Alperen Sengun, Houston Rockets
ESS-AT Alex Toohey, Golden State Warriors RC
ESS-BB Brooks Barnhizer, Oklahoma City Thunder RC
ESS-CA Carmelo Anthony, Denver Nuggets
ESS-CF Cooper Flagg, Dallas Mavericks RC
ESS-CH Chet Holmgren, Oklahoma City Thunder
ESS-CM Collin Murray-Boyles, Toronto Raptors RC
ESS-DD Donte DiVincenzo, Minnesota Timberwolves
ESS-DG Daniel Gafford, Dallas Mavericks
ESS-DH Dylan Harper, San Antonio Spurs RC
ESS-DN Dirk Nowitzki, Dallas Mavericks
ESS-DW Derrick White, Boston Celtics
ESS-GSA Gui Santos, Golden State Warriors
ESS-JH Jett Howard, Orlando Magic
ESS-KG Kevin Garnett, Boston Celtics
ESS-KK Kon Knueppel, Charlotte Hornets RC
ESS-KL Kevin Love, Miami Heat
ESS-KS Kobe Sanders, Los Angeles Clippers RC
ESS-KW Kel'el Ware, Miami Heat
ESS-LWI Lindy Waters III, Detroit Pistons
ESS-MP Micah Peavy, New Orleans Pelicans RC
ESS-NB Nicolas Batum, Los Angeles Clippers
ESS-NR Naz Reid, Minnesota Timberwolves
ESS-SO Shaquille O'Neal, Los Angeles Lakers
ESS-TD Tristan da Silva, Orlando Magic
ESS-TM Tracy McGrady, Toronto Raptors
ESS-YM Yves Missi, New Orleans Pelicans
ESS-ZL Zach LaVine, Sacramento Kings"""

FIRST_FLIGHT_SIGS_RAW = """FF-AB Ace Bailey, Utah Jazz RC
FF-AH Al Horford, Boston Celtics
FF-AM Ajay Mitchell, Oklahoma City Thunder
FF-CF Cooper Flagg, Dallas Mavericks RC
FF-CL Chaz Lanier, Detroit Pistons RC
FF-CM Collin Murray-Boyles, Toronto Raptors RC
FF-DH Dylan Harper, San Antonio Spurs RC
FF-DM Donovan Mitchell, Cleveland Cavaliers
FF-ED Egor Dëmin, Brooklyn Nets RC
FF-IC Isaiah Collier, Utah Jazz
FF-JB Joan Beringer, Minnesota Timberwolves RC
FF-JT Jayson Tatum, Boston Celtics
FF-JW Jaylen Wells, Memphis Grizzlies
FF-KD Kevin Durant, Houston Rockets
FF-KG Kyshawn George, Washington Wizards
FF-KJ Kam Jones, Indiana Pacers RC
FF-KK Kon Knueppel, Charlotte Hornets RC
FF-LO Lachlan Olbrich, Chicago Bulls RC
FF-PB Paolo Banchero, Orlando Magic
FF-RH Ronald Holland II, Detroit Pistons
FF-SC Stephen Curry, Golden State Warriors
FF-SJ Sion James, Charlotte Hornets RC
FF-TS Tristan da Silva, Orlando Magic
FF-TSO Thomas Sorber, Oklahoma City Thunder RC
FF-VW Victor Wembanyama, San Antonio Spurs
FF-WR Will Richard, Golden State Warriors RC
FF-WRI Will Riley, Washington Wizards RC
FF-YH Yang Hansen, Portland Trail Blazers RC
FF-ZE Zach Edey, Memphis Grizzlies"""

GALAXY_GREATS_RAW = """GG-1 Allen Iverson, Philadelphia 76ers
GG-2 David Robinson, San Antonio Spurs
GG-3 Dirk Nowitzki, Dallas Mavericks
GG-4 Dwyane Wade, Miami Heat
GG-5 Hakeem Olajuwon, Houston Rockets
GG-6 Karl Malone, Utah Jazz
GG-7 Kevin Garnett, Minnesota Timberwolves
GG-8 Shaquille O'Neal, Los Angeles Lakers
GG-9 Vince Carter, Toronto Raptors
GG-10 Larry Bird, Boston Celtics
GG-11 Carmelo Anthony, New York Knicks
GG-12 Spud Webb, Atlanta Hawks
GG-13 Clyde Drexler, Portland Trail Blazers
GG-14 Alonzo Mourning, Miami Heat
GG-15 Grant Hill, Orlando Magic
GG-16 Larry Johnson, Charlotte Hornets
GG-17 Dwight Howard, Orlando Magic
GG-18 Chris Bosh, Toronto Raptors
GG-19 Robert Horry, Los Angeles Lakers
GG-20 Steve Francis, Houston Rockets
GG-21 John Stockton, Utah Jazz
GG-22 Kareem Abdul-Jabbar, Los Angeles Lakers
GG-23 Tracy McGrady, Toronto Raptors
GG-24 Ray Allen, Miami Heat
GG-25 Manu Ginobili, San Antonio Spurs
GG-26 Vince Carter, Toronto Raptors
GG-27 Paul Pierce, Boston Celtics
GG-28 Jason Kidd, New Jersey Nets
GG-29 Jalen Rose, Indiana Pacers
GG-30 Magic Johnson, Los Angeles Lakers
GG-31 Metta World Peace, Indiana Pacers
GG-32 Tony Parker, San Antonio Spurs
GG-33 Ben Wallace, Detroit Pistons
GG-34 Pau Gasol, Los Angeles Lakers
GG-35 Rasheed Wallace, Portland Trail Blazers"""

EXTRATERRESTRIAL_TALENT_RAW = """ET-1 Shai Gilgeous-Alexander, Oklahoma City Thunder
ET-2 Anthony Edwards, Minnesota Timberwolves
ET-3 Giannis Antetokounmpo, Milwaukee Bucks
ET-4 Nikola Jokić, Denver Nuggets
ET-5 Stephen Curry, Golden State Warriors
ET-6 Paolo Banchero, Orlando Magic
ET-7 Victor Wembanyama, San Antonio Spurs
ET-8 LeBron James, Los Angeles Lakers
ET-9 Kevin Durant, Houston Rockets
ET-10 Cade Cunningham, Detroit Pistons
ET-11 Cooper Flagg, Dallas Mavericks RC
ET-12 Dylan Harper, San Antonio Spurs RC
ET-13 Ace Bailey, Utah Jazz RC
ET-14 Kon Knueppel, Charlotte Hornets RC
ET-15 VJ Edgecombe, Philadelphia 76ers RC
ET-16 Tre Johnson III, Washington Wizards RC
ET-17 Jeremiah Fears, New Orleans Pelicans RC
ET-18 Egor Dëmin, Brooklyn Nets RC
ET-19 Collin Murray-Boyles, Toronto Raptors RC
ET-20 Asa Newell, Atlanta Hawks RC
ET-21 Yang Hansen, Portland Trail Blazers RC
ET-22 Liam McNeeley, Charlotte Hornets RC
ET-23 Khaman Maluach, Phoenix Suns RC
ET-24 Jase Richardson, Orlando Magic RC
ET-25 Nique Clifford, Sacramento Kings RC"""

PROPULSION_RAW = """PRP-1 Shai Gilgeous-Alexander, Oklahoma City Thunder
PRP-2 Donovan Mitchell, Cleveland Cavaliers
PRP-3 Stephen Curry, Golden State Warriors
PRP-4 Jalen Brunson, New York Knicks
PRP-5 Cade Cunningham, Detroit Pistons
PRP-6 Jalen Williams, Oklahoma City Thunder
PRP-7 De'Aaron Fox, San Antonio Spurs
PRP-8 Ja Morant, Memphis Grizzlies
PRP-9 Tyrese Maxey, Philadelphia 76ers
PRP-10 Tyrese Haliburton, Indiana Pacers
PRP-11 Kyrie Irving, Dallas Mavericks
PRP-12 Desmond Bane, Memphis Grizzlies
PRP-13 LaMelo Ball, Charlotte Hornets
PRP-14 Devin Booker, Phoenix Suns
PRP-15 Anthony Edwards, Minnesota Timberwolves
PRP-16 Cooper Flagg, Dallas Mavericks RC
PRP-17 Dylan Harper, San Antonio Spurs RC
PRP-18 VJ Edgecombe, Philadelphia 76ers RC
PRP-19 Kon Knueppel, Charlotte Hornets RC
PRP-20 Ace Bailey, Utah Jazz RC
PRP-21 Tre Johnson III, Washington Wizards RC
PRP-22 Jeremiah Fears, New Orleans Pelicans RC
PRP-23 Egor Dëmin, Brooklyn Nets RC
PRP-24 Walter Clayton Jr., Utah Jazz RC
PRP-25 Kasparas Jakučionis, Miami Heat RC"""

SPACE_WALK_RAW = """SW-1 LeBron James, Los Angeles Lakers
SW-2 Giannis Antetokounmpo, Milwaukee Bucks
SW-3 Ja Morant, Memphis Grizzlies
SW-4 Jayson Tatum, Boston Celtics
SW-5 Anthony Edwards, Minnesota Timberwolves
SW-6 Cooper Flagg, Dallas Mavericks RC
SW-7 Dylan Harper, San Antonio Spurs RC
SW-8 Collin Murray-Boyles, Toronto Raptors RC
SW-9 Carter Bryant, San Antonio Spurs RC
SW-10 Walter Clayton Jr., Utah Jazz RC
SW-11 Drake Powell, Brooklyn Nets RC
SW-12 Rasheer Fleming, Phoenix Suns RC
SW-13 Cedric Coward, Memphis Grizzlies RC
SW-14 VJ Edgecombe, Philadelphia 76ers RC
SW-15 Noa Essengue, Chicago Bulls RC"""

STARFRACTOR_RAW = """SF-1 Shai Gilgeous-Alexander, Oklahoma City Thunder
SF-2 Nikola Jokić, Denver Nuggets
SF-3 Giannis Antetokounmpo, Milwaukee Bucks
SF-4 Luka Dončić, Los Angeles Lakers
SF-5 Stephen Curry, Golden State Warriors
SF-6 Anthony Edwards, Minnesota Timberwolves
SF-7 Tyrese Haliburton, Indiana Pacers
SF-8 Donovan Mitchell, Cleveland Cavaliers
SF-9 Victor Wembanyama, San Antonio Spurs
SF-10 Jayson Tatum, Boston Celtics
SF-11 Jalen Brunson, New York Knicks
SF-12 Anthony Davis, Dallas Mavericks
SF-13 LeBron James, Los Angeles Lakers
SF-14 Kawhi Leonard, Los Angeles Clippers
SF-15 Kevin Durant, Houston Rockets
SF-16 Cade Cunningham, Detroit Pistons
SF-17 Devin Booker, Phoenix Suns
SF-18 Jalen Williams, Oklahoma City Thunder
SF-19 Paolo Banchero, Orlando Magic
SF-20 Pascal Siakam, Indiana Pacers
SF-21 Jimmy Butler III, Golden State Warriors
SF-22 LaMelo Ball, Charlotte Hornets
SF-23 Bam Adebayo, Miami Heat
SF-24 Ja Morant, Memphis Grizzlies
SF-25 Evan Mobley, Cleveland Cavaliers
SF-26 Jaylen Brown, Boston Celtics
SF-27 Trae Young, Atlanta Hawks
SF-28 Tyrese Maxey, Philadelphia 76ers
SF-29 James Harden, Los Angeles Clippers
SF-30 De'Aaron Fox, San Antonio Spurs
SF-31 Cooper Flagg, Dallas Mavericks RC
SF-32 Dylan Harper, San Antonio Spurs RC
SF-33 VJ Edgecombe, Philadelphia 76ers RC
SF-34 Kon Knueppel, Charlotte Hornets RC
SF-35 Ace Bailey, Utah Jazz RC
SF-36 Tre Johnson III, Washington Wizards RC
SF-37 Jeremiah Fears, New Orleans Pelicans RC
SF-38 Egor Dëmin, Brooklyn Nets RC
SF-39 Collin Murray-Boyles, Toronto Raptors RC
SF-40 Khaman Maluach, Phoenix Suns RC
SF-41 Carter Bryant, San Antonio Spurs RC
SF-42 Walter Clayton Jr., Utah Jazz RC
SF-43 Kasparas Jakučionis, Miami Heat RC
SF-44 Asa Newell, Atlanta Hawks RC
SF-45 Jase Richardson, Orlando Magic RC
SF-46 Kevin Garnett, Minnesota Timberwolves
SF-47 Allen Iverson, Philadelphia 76ers
SF-48 Larry Bird, Boston Celtics
SF-49 Shaquille O'Neal, Los Angeles Lakers
SF-50 Dirk Nowitzki, Dallas Mavericks"""

RE_ENTRY_RAW = """REE-1 LeBron James, Los Angeles Lakers
REE-2 Kevin Durant, Houston Rockets
REE-3 Victor Wembanyama, San Antonio Spurs
REE-4 Anthony Edwards, Minnesota Timberwolves
REE-5 Shai Gilgeous-Alexander, Oklahoma City Thunder
REE-6 Luka Dončić, Los Angeles Lakers
REE-7 Giannis Antetokounmpo, Milwaukee Bucks
REE-8 Stephen Curry, Golden State Warriors
REE-9 Tyrese Haliburton, Indiana Pacers
REE-10 Jayson Tatum, Boston Celtics
REE-11 Nikola Jokić, Denver Nuggets
REE-12 Anthony Davis, Dallas Mavericks
REE-13 Karl-Anthony Towns, New York Knicks
REE-14 Evan Mobley, Cleveland Cavaliers
REE-15 Paolo Banchero, Orlando Magic
REE-16 Chet Holmgren, Oklahoma City Thunder
REE-17 Pascal Siakam, Indiana Pacers
REE-18 Ja Morant, Memphis Grizzlies
REE-19 Devin Booker, Phoenix Suns
REE-20 Cade Cunningham, Detroit Pistons
REE-21 Cooper Flagg, Dallas Mavericks RC
REE-22 Dylan Harper, San Antonio Spurs RC
REE-23 VJ Edgecombe, Philadelphia 76ers RC
REE-24 Kon Knueppel, Charlotte Hornets RC
REE-25 Ace Bailey, Utah Jazz RC
REE-26 Tre Johnson III, Washington Wizards RC
REE-27 Jeremiah Fears, New Orleans Pelicans RC
REE-28 Egor Dëmin, Brooklyn Nets RC
REE-29 Collin Murray-Boyles, Toronto Raptors RC
REE-30 Khaman Maluach, Phoenix Suns RC
REE-31 Noa Essengue, Chicago Bulls RC
REE-32 Derik Queen, New Orleans Pelicans RC
REE-33 Carter Bryant, San Antonio Spurs RC
REE-34 Yang Hansen, Portland Trail Blazers RC
REE-35 Joan Beringer, Minnesota Timberwolves RC
REE-36 Walter Clayton Jr., Utah Jazz RC
REE-37 Will Riley, Washington Wizards RC
REE-38 Asa Newell, Atlanta Hawks RC
REE-39 Jase Richardson, Orlando Magic RC
REE-40 Liam McNeeley, Charlotte Hornets RC"""

GEOCENTRIC_RAW = """GE-1 Stephen Curry, Golden State Warriors
GE-2 LeBron James, Los Angeles Lakers
GE-3 Shai Gilgeous-Alexander, Oklahoma City Thunder
GE-4 Tyrese Haliburton, Indiana Pacers
GE-5 Anthony Edwards, Minnesota Timberwolves
GE-6 Jalen Brunson, New York Knicks
GE-7 Donovan Mitchell, Cleveland Cavaliers
GE-8 Kevin Durant, Houston Rockets
GE-9 Giannis Antetokounmpo, Milwaukee Bucks
GE-10 Nikola Jokić, Denver Nuggets
GE-11 Victor Wembanyama, San Antonio Spurs
GE-12 Cade Cunningham, Detroit Pistons
GE-13 Anthony Davis, Dallas Mavericks
GE-14 Paolo Banchero, Orlando Magic
GE-15 Devin Booker, Phoenix Suns
GE-16 Jayson Tatum, Boston Celtics
GE-17 Kawhi Leonard, Los Angeles Clippers
GE-18 Ja Morant, Memphis Grizzlies
GE-19 Tyrese Maxey, Philadelphia 76ers
GE-20 LaMelo Ball, Charlotte Hornets
GE-21 Cooper Flagg, Dallas Mavericks RC
GE-22 Dylan Harper, San Antonio Spurs RC
GE-23 Kon Knueppel, Charlotte Hornets RC
GE-24 Ace Bailey, Utah Jazz RC
GE-25 Egor Dëmin, Brooklyn Nets RC
GE-26 Collin Murray-Boyles, Toronto Raptors RC
GE-27 Khaman Maluach, Phoenix Suns RC
GE-28 Noa Essengue, Chicago Bulls RC
GE-29 Derik Queen, New Orleans Pelicans RC
GE-30 Asa Newell, Atlanta Hawks RC"""

# First Light — all rookies (no RC suffix in data; is_rookie forced True)
FIRST_LIGHT_RAW = """FL-1 Cooper Flagg, Dallas Mavericks
FL-2 Dylan Harper, San Antonio Spurs
FL-3 VJ Edgecombe, Philadelphia 76ers
FL-4 Kon Knueppel, Charlotte Hornets
FL-5 Ace Bailey, Utah Jazz
FL-6 Tre Johnson III, Washington Wizards
FL-7 Jeremiah Fears, New Orleans Pelicans
FL-8 Egor Dëmin, Brooklyn Nets
FL-9 Collin Murray-Boyles, Toronto Raptors
FL-10 Khaman Maluach, Phoenix Suns
FL-11 Cedric Coward, Memphis Grizzlies
FL-12 Noa Essengue, Chicago Bulls
FL-13 Derik Queen, New Orleans Pelicans
FL-14 Carter Bryant, San Antonio Spurs
FL-15 Thomas Sorber, Oklahoma City Thunder
FL-16 Yang Hansen, Portland Trail Blazers
FL-17 Joan Beringer, Minnesota Timberwolves
FL-18 Walter Clayton Jr., Utah Jazz
FL-19 Nolan Traore, Brooklyn Nets
FL-20 Kasparas Jakučionis, Miami Heat
FL-21 Will Riley, Washington Wizards
FL-22 Drake Powell, Brooklyn Nets
FL-23 Asa Newell, Atlanta Hawks
FL-24 Nique Clifford, Sacramento Kings
FL-25 Jase Richardson, Orlando Magic
FL-26 Ben Saraf, Brooklyn Nets
FL-27 Danny Wolf, Brooklyn Nets
FL-28 Hugo González, Boston Celtics
FL-29 Liam McNeeley, Charlotte Hornets
FL-30 Yanic Konan-Niederhäuser, Los Angeles Clippers"""

HYPER_NOVA_RAW = """HN-1 Shai Gilgeous-Alexander, Oklahoma City Thunder
HN-2 Nikola Jokić, Denver Nuggets
HN-3 Giannis Antetokounmpo, Milwaukee Bucks
HN-4 Stephen Curry, Golden State Warriors
HN-5 Anthony Edwards, Minnesota Timberwolves
HN-6 Pascal Siakam, Indiana Pacers
HN-7 Jalen Brunson, New York Knicks
HN-8 Luka Dončić, Los Angeles Lakers
HN-9 Jayson Tatum, Boston Celtics
HN-10 Victor Wembanyama, San Antonio Spurs
HN-11 Kyrie Irving, Dallas Mavericks
HN-12 Kevin Durant, Houston Rockets
HN-13 Cade Cunningham, Detroit Pistons
HN-14 Paolo Banchero, Orlando Magic
HN-15 Donovan Mitchell, Cleveland Cavaliers
HN-16 Cooper Flagg, Dallas Mavericks RC
HN-17 Dylan Harper, San Antonio Spurs RC
HN-18 VJ Edgecombe, Philadelphia 76ers RC
HN-19 Kon Knueppel, Charlotte Hornets RC
HN-20 Ace Bailey, Utah Jazz RC"""

COSMIC_DUST_RAW = """CD-1 LeBron James, Los Angeles Lakers
CD-2 Tyrese Haliburton, Indiana Pacers
CD-3 Anthony Davis, Dallas Mavericks
CD-4 Shai Gilgeous-Alexander, Oklahoma City Thunder
CD-5 Giannis Antetokounmpo, Milwaukee Bucks
CD-6 Stephen Curry, Golden State Warriors
CD-7 Victor Wembanyama, San Antonio Spurs
CD-8 Cade Cunningham, Detroit Pistons
CD-9 Anthony Edwards, Minnesota Timberwolves
CD-10 Jalen Brunson, New York Knicks
CD-11 Shaquille O'Neal, Los Angeles Lakers
CD-12 Kevin Garnett, Minnesota Timberwolves
CD-13 Dirk Nowitzki, Dallas Mavericks
CD-14 Allen Iverson, Philadelphia 76ers
CD-15 Bill Russell, Boston Celtics
CD-16 Cooper Flagg, Dallas Mavericks RC
CD-17 Dylan Harper, San Antonio Spurs RC
CD-18 VJ Edgecombe, Philadelphia 76ers RC
CD-19 Kon Knueppel, Charlotte Hornets RC
CD-20 Ace Bailey, Utah Jazz RC"""

PLANETARY_PURSUIT_RAW = """PPE-1 Shai Gilgeous-Alexander, Oklahoma City Thunder
PPE-2 LeBron James, Los Angeles Lakers
PPE-3 Stephen Curry, Golden State Warriors
PPE-4 Giannis Antetokounmpo, Milwaukee Bucks
PPE-5 Anthony Edwards, Minnesota Timberwolves
PPE-6 Victor Wembanyama, San Antonio Spurs
PPE-7 Luka Dončić, Los Angeles Lakers
PPE-8 Cooper Flagg, Dallas Mavericks RC
PPE-9 Dylan Harper, San Antonio Spurs RC
PPE-10 Kon Knueppel, Charlotte Hornets RC"""

# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------

def parse_lines(raw: str, force_rookie: bool = False) -> list:
    cards = []
    for line in raw.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        # Split on first space to get card number
        space_idx = line.index(' ')
        card_number = line[:space_idx]
        rest = line[space_idx + 1:]

        is_rookie = force_rookie or rest.endswith(' RC')
        if rest.endswith(' RC'):
            rest = rest[:-3]

        # Split on last ', ' to separate name from team
        # (handles names like "T.J. McConnell" safely)
        comma_idx = rest.rfind(', ')
        if comma_idx == -1:
            raise ValueError(f"Cannot parse line: {line!r}")
        player = fix_name(rest[:comma_idx])
        team = rest[comma_idx + 2:]

        cards.append({
            "card_number": card_number,
            "player": player,
            "team": team,
            "is_rookie": is_rookie,
            "subset": None,
        })
    return cards

def make_section(insert_set_name: str, parallels: list, cards: list) -> dict:
    return {"insert_set": insert_set_name, "parallels": parallels, "cards": cards}

# ---------------------------------------------------------------------------
# Build sections
# ---------------------------------------------------------------------------

def build_base_set_cards() -> list:
    cards = []
    for card_number, player, team, is_rookie in BASE_SET_RAW:
        cards.append({
            "card_number": card_number,
            "player": fix_name(player),
            "team": team,
            "is_rookie": is_rookie,
            "subset": None,
        })
    return cards

sections = [
    make_section("Base Set",                    NO_PARALLELS, build_base_set_cards()),
    make_section("Cosmic Chrome Autographs",     NO_PARALLELS, parse_lines(COSMIC_CHROME_AUTOS_RAW)),
    make_section("Cosmic Chrome Autographs II",  NO_PARALLELS, parse_lines(COSMIC_CHROME_AUTOS_II_RAW)),
    make_section("Singularity",                  NO_PARALLELS, parse_lines(SINGULARITY_RAW)),
    make_section("Alien Autographs",             NO_PARALLELS, parse_lines(ALIEN_AUTOS_RAW)),
    make_section("Electro Static Signatures",    NO_PARALLELS, parse_lines(ELECTRO_STATIC_SIGS_RAW)),
    make_section("First Flight Signatures",      NO_PARALLELS, parse_lines(FIRST_FLIGHT_SIGS_RAW)),
    make_section("Galaxy Greats",                NO_PARALLELS, parse_lines(GALAXY_GREATS_RAW)),
    make_section("Extraterrestrial Talent",      NO_PARALLELS, parse_lines(EXTRATERRESTRIAL_TALENT_RAW)),
    make_section("Propulsion",                   NO_PARALLELS, parse_lines(PROPULSION_RAW)),
    make_section("Space Walk",                   NO_PARALLELS, parse_lines(SPACE_WALK_RAW)),
    make_section("Starfractor",                  NO_PARALLELS, parse_lines(STARFRACTOR_RAW)),
    make_section("Re Entry",                     NO_PARALLELS, parse_lines(RE_ENTRY_RAW)),
    make_section("Geocentric",                   NO_PARALLELS, parse_lines(GEOCENTRIC_RAW)),
    make_section("First Light",                  NO_PARALLELS, parse_lines(FIRST_LIGHT_RAW, force_rookie=True)),
    make_section("Hyper Nova",                   NO_PARALLELS, parse_lines(HYPER_NOVA_RAW)),
    make_section("Cosmic Dust",                  NO_PARALLELS, parse_lines(COSMIC_DUST_RAW)),
    make_section("Planetary Pursuit",            PLANETARY_PURSUIT_PARALLELS, parse_lines(PLANETARY_PURSUIT_RAW)),
]

# ---------------------------------------------------------------------------
# Build player aggregations
# ---------------------------------------------------------------------------

# player_name -> { appearances: [...], insert_sets: set(), unique_cards: int,
#                  total_print_run: int, one_of_ones: int }
player_map = defaultdict(lambda: {
    "appearances": [],
    "insert_sets": set(),
    "unique_cards": 0,
    "total_print_run": 0,
    "one_of_ones": 0,
})

# Collect rc_players so we can propagate is_rookie across all appearances
rc_players = set()
for section in sections:
    for card in section["cards"]:
        if card["is_rookie"]:
            rc_players.add(card["player"])

for section in sections:
    for card in section["cards"]:
        name = card["player"]
        is_rookie = name in rc_players
        pm = player_map[name]
        pm["appearances"].append({
            "insert_set": section["insert_set"],
            "card_number": card["card_number"],
            "team": card["team"],
            "is_rookie": is_rookie,
            "subset_tag": card["subset"],
            "parallels": section["parallels"],
        })
        pm["insert_sets"].add(section["insert_set"])
        pm["unique_cards"] += 1
        # Serialized parallels contribute to total_print_run
        for p in section["parallels"]:
            if p["print_run"] is not None:
                pm["total_print_run"] += p["print_run"]
                if p["print_run"] == 1:
                    pm["one_of_ones"] += 1

players_out = []
for name, pm in sorted(player_map.items()):
    players_out.append({
        "player": name,
        "appearances": pm["appearances"],
        "stats": {
            "unique_cards": pm["unique_cards"],
            "total_print_run": pm["total_print_run"],
            "one_of_ones": pm["one_of_ones"],
            "insert_sets": len(pm["insert_sets"]),
        },
    })

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

output = {
    "set_name": "2025-26 Topps Cosmic Chrome Basketball",
    "sport": "Basketball",
    "season": "2025-26",
    "league": "NBA",
    "sections": sections,
    "players": players_out,
}

out_path = "cosmic_chrome_basketball_2526_parsed.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Written: {out_path}")
print(f"Sections:    {len(sections)}")
print(f"Total cards: {sum(len(s['cards']) for s in sections)}")
print(f"Players:     {len(players_out)}")
