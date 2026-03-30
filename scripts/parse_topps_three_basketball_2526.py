#!/usr/bin/env python3
"""Parser for 2025-26 Topps Three Basketball."""
import json
from collections import defaultdict

SET_NAME = "2025-26 Topps Three Basketball"
SPORT = "Basketball"
LEAGUE = "NBA"
SEASON = "2025-26"

# ---------------------------------------------------------------------------
# Name normalization
# ---------------------------------------------------------------------------
NAME_FIXES = {
    "nique clifford":       "Nique Clifford",
    "karl anthony-towns":   "Karl-Anthony Towns",
    "zach lavine":          "Zach LaVine",
    "peja stojaković":      "Peja Stojakovic",
    "bennedict mathurin":   "Bennedict Mathurin",
}

def fix_name(raw):
    s = raw.strip()
    return NAME_FIXES.get(s.lower(), s)

# ---------------------------------------------------------------------------
# Parallel definitions (all odds-based, no fixed print runs)
# ---------------------------------------------------------------------------
def pars(*names):
    return [{"name": n, "print_run": None} for n in names]

BASE_PARS    = pars("Bronze", "Blue", "Gold", "Red", "Platinum")
FDI_PARS     = pars("Emerald FDI", "Holo Gold FDI", "Bronze", "Blue", "Gold", "Red", "Platinum")
STD_PARS     = pars("Bronze", "Blue", "Gold", "Red", "Platinum")
TRA_PARS     = pars("Gold", "Red", "Platinum")
HOLO_PARS    = pars("Holo Gold", "Platinum")
RHP_PARS     = pars("Red", "Holo Gold", "Platinum")

# Team overrides for players only appearing in Triple Relic Autographs
TRA_TEAM_OVERRIDES = {
    "Onyeka Okongwu": "Atlanta Hawks",
}

# ---------------------------------------------------------------------------
# Raw card data
# ---------------------------------------------------------------------------

BASE_RAW = """
1 Trae Young, Atlanta Hawks
2 Zaccharie Risacher, Atlanta Hawks
3 Donovan Mitchell, Cleveland Cavaliers
4 Evan Mobley, Cleveland Cavaliers
5 Amen Thompson, Houston Rockets
6 Kevin Durant, Houston Rockets
7 Jaime Jaquez Jr., Miami Heat
8 Kel'el Ware, Miami Heat
9 Shai Gilgeous-Alexander, Oklahoma City Thunder
10 Chet Holmgren, Oklahoma City Thunder
11 Zach LaVine, Sacramento Kings
12 DeMar DeRozan, Sacramento Kings
13 Jayson Tatum, Boston Celtics
14 Jaylen Brown, Boston Celtics
15 Kyrie Irving, Dallas Mavericks
16 Anthony Davis, Dallas Mavericks
17 Tyrese Haliburton, Indiana Pacers
18 Pascal Siakam, Indiana Pacers
19 Giannis Antetokounmpo, Milwaukee Bucks
20 Kyle Kuzma, Milwaukee Bucks
21 Anthony Black, Orlando Magic
22 Paolo Banchero, Orlando Magic
23 Stephon Castle, San Antonio Spurs
24 Victor Wembanyama, San Antonio Spurs
25 Cam Thomas, Brooklyn Nets
26 Noah Clowney, Brooklyn Nets
27 Nikola Jokić, Denver Nuggets
28 Russell Westbrook, Denver Nuggets
29 James Harden, Los Angeles Clippers
30 Kawhi Leonard, Los Angeles Clippers
31 Mike Conley, Minnesota Timberwolves
32 Anthony Edwards, Minnesota Timberwolves
33 Tyrese Maxey, Philadelphia 76ers
34 Joel Embiid, Philadelphia 76ers
35 Gradey Dick, Toronto Raptors
36 Scottie Barnes, Toronto Raptors
37 LaMelo Ball, Charlotte Hornets
38 Brandon Miller, Charlotte Hornets
39 Cade Cunningham, Detroit Pistons
40 Jaden Ivey, Detroit Pistons
41 Luka Dončić, Los Angeles Lakers
42 LeBron James, Los Angeles Lakers
43 Herbert Jones, New Orleans Pelicans
44 Jordan Hawkins, New Orleans Pelicans
45 Devin Booker, Phoenix Suns
46 Grayson Allen, Phoenix Suns
47 Lauri Markkanen, Utah Jazz
48 Isaiah Collier, Utah Jazz
49 Josh Giddey, Chicago Bulls
50 Ayo Dosunmu, Chicago Bulls
51 Stephen Curry, Golden State Warriors
52 Brandin Podziemski, Golden State Warriors
53 Ja Morant, Memphis Grizzlies
54 Jaren Jackson Jr., Memphis Grizzlies
55 Jalen Brunson, New York Knicks
56 Karl-Anthony Towns, New York Knicks
57 Scoot Henderson, Portland Trail Blazers
58 Jerami Grant, Portland Trail Blazers
59 Bub Carrington, Washington Wizards
60 Alex Sarr, Washington Wizards
61 Cooper Flagg, Dallas Mavericks RC
62 Dylan Harper, San Antonio Spurs RC
63 VJ Edgecombe, Philadelphia 76ers RC
64 Kon Knueppel, Charlotte Hornets RC
65 Ace Bailey, Utah Jazz RC
66 Tre Johnson III, Washington Wizards RC
67 Jeremiah Fears, New Orleans Pelicans RC
68 Egor Dëmin, Brooklyn Nets RC
69 Collin Murray-Boyles, Toronto Raptors RC
70 Khaman Maluach, Phoenix Suns RC
71 Cedric Coward, Memphis Grizzlies RC
72 Noa Essengue, Chicago Bulls RC
73 Derik Queen, New Orleans Pelicans RC
74 Carter Bryant, San Antonio Spurs RC
75 Thomas Sorber, Oklahoma City Thunder RC
76 Yang Hansen, Portland Trail Blazers RC
77 Joan Beringer, Minnesota Timberwolves RC
78 Walter Clayton Jr., Utah Jazz RC
79 Nolan Traore, Brooklyn Nets RC
80 Kasparas Jakučionis, Miami Heat RC
81 Will Riley, Washington Wizards RC
82 Drake Powell, Brooklyn Nets RC
83 Asa Newell, Atlanta Hawks RC
84 Nique Clifford, Sacramento Kings RC
85 Jase Richardson, Orlando Magic RC
86 Ben Saraf, Brooklyn Nets RC
87 Danny Wolf, Brooklyn Nets RC
88 Hugo González, Boston Celtics RC
89 Liam McNeeley, Charlotte Hornets RC
90 Yanic Konan-Niederhäuser, Los Angeles Clippers RC
91 Rasheer Fleming, Phoenix Suns RC
92 Noah Penda, Orlando Magic RC
93 Sion James, Charlotte Hornets RC
94 Ryan Kalkbrenner, Charlotte Hornets RC
95 Johni Broome, Philadelphia 76ers RC
96 Adou Thiero, Los Angeles Lakers RC
97 Chaz Lanier, Detroit Pistons RC
98 Kam Jones, Indiana Pacers RC
99 Alijah Martin, Toronto Raptors RC
100 Micah Peavy, New Orleans Pelicans RC
"""

RPH_RAW = """
RPH-AB Ace Bailey, Utah Jazz
RPH-AM Alijah Martin, Toronto Raptors
RPH-AN Asa Newell, Atlanta Hawks
RPH-AT Adou Thiero, Los Angeles Lakers
RPH-BB Brooks Barnhizer, Oklahoma City Thunder
RPH-BS Ben Saraf, Brooklyn Nets
RPH-CC Cedric Coward, Memphis Grizzlies
RPH-CF Cooper Flagg, Dallas Mavericks
RPH-CL Chaz Lanier, Detroit Pistons
RPH-CM Collin Murray-Boyles, Toronto Raptors
RPH-DH Dylan Harper, San Antonio Spurs
RPH-DP Drake Powell, Brooklyn Nets
RPH-DQ Derik Queen, New Orleans Pelicans
RPH-DW Danny Wolf, Brooklyn Nets
RPH-ED Egor Dëmin, Brooklyn Nets
RPH-JB Joan Beringer, Minnesota Timberwolves
RPH-JBR Johni Broome, Philadelphia 76ers
RPH-JR Jase Richardson, Orlando Magic
RPH-JW Jamir Watkins, Washington Wizards
RPH-KB Koby Brea, Phoenix Suns
RPH-KJ Kasparas Jakučionis, Miami Heat
RPH-KJO Kam Jones, Indiana Pacers
RPH-KK Kon Knueppel, Charlotte Hornets
RPH-KM Khaman Maluach, Phoenix Suns
RPH-LM Liam McNeeley, Charlotte Hornets
RPH-MP Micah Peavy, New Orleans Pelicans
RPH-MR Maxime Raynaud, Sacramento Kings
RPH-NC Nique Clifford, Sacramento Kings
RPH-NE Noa Essengue, Chicago Bulls
RPH-NP Noah Penda, Orlando Magic
RPH-NT Nolan Traore, Brooklyn Nets
RPH-RF Rasheer Fleming, Phoenix Suns
RPH-RK Ryan Kalkbrenner, Charlotte Hornets
RPH-SJ Sion James, Charlotte Hornets
RPH-TP Tyrese Proctor, Cleveland Cavaliers
RPH-TS Thomas Sorber, Oklahoma City Thunder
RPH-WC Walter Clayton Jr., Utah Jazz
RPH-WR Will Riley, Washington Wizards
RPH-YH Yang Hansen, Portland Trail Blazers
RPH-YK Yanic Konan-Niederhäuser, Los Angeles Clippers
"""

RPV_RAW = """
RPV-AB Ace Bailey, Utah Jazz
RPV-AM Alijah Martin, Toronto Raptors
RPV-AN Asa Newell, Atlanta Hawks
RPV-AT Adou Thiero, Los Angeles Lakers
RPV-BB Brooks Barnhizer, Oklahoma City Thunder
RPV-BS Ben Saraf, Brooklyn Nets
RPV-CC Cedric Coward, Memphis Grizzlies
RPV-CF Cooper Flagg, Dallas Mavericks
RPV-CL Chaz Lanier, Detroit Pistons
RPV-CM Collin Murray-Boyles, Toronto Raptors
RPV-DH Dylan Harper, San Antonio Spurs
RPV-DP Drake Powell, Brooklyn Nets
RPV-DQ Derik Queen, New Orleans Pelicans
RPV-DW Danny Wolf, Brooklyn Nets
RPV-ED Egor Dëmin, Brooklyn Nets
RPV-JB Joan Beringer, Minnesota Timberwolves
RPV-JBR Johni Broome, Philadelphia 76ers
RPV-JR Jase Richardson, Orlando Magic
RPV-JW Jamir Watkins, Washington Wizards
RPV-KB Koby Brea, Phoenix Suns
RPV-KJ Kasparas Jakučionis, Miami Heat
RPV-KJO Kam Jones, Indiana Pacers
RPV-KK Kon Knueppel, Charlotte Hornets
RPV-KM Khaman Maluach, Phoenix Suns
RPV-LM Liam McNeeley, Charlotte Hornets
RPV-MP Micah Peavy, New Orleans Pelicans
RPV-MR Maxime Raynaud, Sacramento Kings
RPV-NC Nique Clifford, Sacramento Kings
RPV-NE Noa Essengue, Chicago Bulls
RPV-NP Noah Penda, Orlando Magic
RPV-NT Nolan Traore, Brooklyn Nets
RPV-RF Rasheer Fleming, Phoenix Suns
RPV-RK Ryan Kalkbrenner, Charlotte Hornets
RPV-SJ Sion James, Charlotte Hornets
RPV-TP Tyrese Proctor, Cleveland Cavaliers
RPV-TS Thomas Sorber, Oklahoma City Thunder
RPV-WC Walter Clayton Jr., Utah Jazz
RPV-WR Will Riley, Washington Wizards
RPV-YH Yang Hansen, Portland Trail Blazers
RPV-YK Yanic Konan-Niederhäuser, Los Angeles Clippers
"""

RAP_RAW = """
RAP-AB Ace Bailey, Utah Jazz
RAP-AN Asa Newell, Atlanta Hawks
RAP-CC Cedric Coward, Memphis Grizzlies
RAP-CF Cooper Flagg, Dallas Mavericks
RAP-CM Collin Murray-Boyles, Toronto Raptors
RAP-DH Dylan Harper, San Antonio Spurs
RAP-DP Drake Powell, Brooklyn Nets
RAP-DQ Derik Queen, New Orleans Pelicans
RAP-GO Egor Dëmin, Brooklyn Nets
RAP-JB Joan Beringer, Minnesota Timberwolves
RAP-KJ Kasparas Jakučionis, Miami Heat
RAP-KK Kon Knueppel, Charlotte Hornets
RAP-KM Khaman Maluach, Phoenix Suns
RAP-NC Nique Clifford, Sacramento Kings
RAP-NE Noa Essengue, Chicago Bulls
RAP-NT Nolan Traore, Brooklyn Nets
RAP-TS Thomas Sorber, Oklahoma City Thunder
RAP-WC Walter Clayton Jr., Utah Jazz
RAP-WR Will Riley, Washington Wizards
RAP-YH Yang Hansen, Portland Trail Blazers
"""

TRA_RAW = """
TRA-BAD: Dylan Harper / Brandon Miller / Alex Sarr
TRA-CAG: Collin Murray-Boyles / Gradey Dick / Alijah Martin
TRA-CDA: Ace Bailey / Cooper Flagg / Dylan Harper
TRA-CKK: Kon Knueppel / Khaman Maluach / Cooper Flagg
TRA-CLA: Asa Newell / Cooper Flagg / Liam McNeeley
TRA-DNE: Egor Dëmin / Nolan Traore / Drake Powell
TRA-JBT: Jarace Walker / Tyrese Haliburton / Bennedict Mathurin
TRA-JPC: Jayson Tatum / Paolo Banchero / Cooper Flagg
TRA-JZC: Cedric Coward / Jaren Jackson Jr. / Zach Edey
TRA-NYN: Yang Hansen / Nolan Traore / Noa Essengue
TRA-OZA: Onyeka Okongwu / Zaccharie Risacher / Asa Newell
TRA-SJZ: Stephon Castle / Zach LaVine / Jaime Jaquez Jr.
TRA-SKJ: Stephen Curry / Jayson Tatum / Kevin Durant
TRA-SPK: Paolo Banchero / Kevin Durant / Stephon Castle
TRA-TMD: Tony Parker / Dylan Harper / Manu Ginobili
TRA-WCA: Chaz Lanier / Alijah Martin / Walter Clayton Jr.
TRA-WKN: Walter Clayton Jr. / Kasparas Jakučionis / Nolan Traore
"""

RRA_RAW = """
RRA-AB Ace Bailey, Utah Jazz
RRA-AM Alijah Martin, Toronto Raptors
RRA-AN Asa Newell, Atlanta Hawks
RRA-AT Adou Thiero, Los Angeles Lakers
RRA-BB Brooks Barnhizer, Oklahoma City Thunder
RRA-BS Ben Saraf, Brooklyn Nets
RRA-CC Cedric Coward, Memphis Grizzlies
RRA-CF Cooper Flagg, Dallas Mavericks
RRA-CL Chaz Lanier, Detroit Pistons
RRA-CM Collin Murray-Boyles, Toronto Raptors
RRA-DH Dylan Harper, San Antonio Spurs
RRA-DP Drake Powell, Brooklyn Nets
RRA-DQ Derik Queen, New Orleans Pelicans
RRA-DW Danny Wolf, Brooklyn Nets
RRA-ED Egor Dëmin, Brooklyn Nets
RRA-JB Joan Beringer, Minnesota Timberwolves
RRA-JBR Johni Broome, Philadelphia 76ers
RRA-JR Jase Richardson, Orlando Magic
RRA-JW Jamir Watkins, Washington Wizards
RRA-KB Koby Brea, Phoenix Suns
RRA-KJ Kasparas Jakučionis, Miami Heat
RRA-KJO Kam Jones, Indiana Pacers
RRA-KK Kon Knueppel, Charlotte Hornets
RRA-KM Khaman Maluach, Phoenix Suns
RRA-LM Liam McNeeley, Charlotte Hornets
RRA-MP Micah Peavy, New Orleans Pelicans
RRA-MR Maxime Raynaud, Sacramento Kings
RRA-NC Nique Clifford, Sacramento Kings
RRA-NE Noa Essengue, Chicago Bulls
RRA-NP Noah Penda, Orlando Magic
RRA-NT Nolan Traore, Brooklyn Nets
RRA-RF Rasheer Fleming, Phoenix Suns
RRA-RK Ryan Kalkbrenner, Charlotte Hornets
RRA-SJ Sion James, Charlotte Hornets
RRA-TP Tyrese Proctor, Cleveland Cavaliers
RRA-TS Thomas Sorber, Oklahoma City Thunder
RRA-WC Walter Clayton Jr., Utah Jazz
RRA-WR Will Riley, Washington Wizards
RRA-YH Yang Hansen, Portland Trail Blazers
RRA-YK Yanic Konan-Niederhäuser, Los Angeles Clippers
"""

V3A_RAW = """
V3A-AB Anthony Black, Orlando Magic
V3A-AD Ayo Dosunmu, Chicago Bulls
V3A-AG Aaron Gordon, Denver Nuggets
V3A-AM Ajay Mitchell, Oklahoma City Thunder
V3A-AS Alex Sarr, Washington Wizards
V3A-BC Bilal Coulibaly, Washington Wizards
V3A-BM Brandon Miller, Charlotte Hornets
V3A-BRJ Bronny James, Los Angeles Lakers
V3A-BSH Ben Sheppard, Indiana Pacers
V3A-CH Chet Holmgren, Oklahoma City Thunder
V3A-CJ Cameron Johnson, Brooklyn Nets
V3A-CM CJ McCollum, New Orleans Pelicans
V3A-CP Chris Paul, San Antonio Spurs
V3A-CW Cam Whitmore, Houston Rockets
V3A-CWI Cody Williams, Utah Jazz
V3A-DG Daniel Gafford, Dallas Mavericks
V3A-DL Dereck Lively II, Dallas Mavericks
V3A-DMI Donovan Mitchell, Cleveland Cavaliers
V3A-DR D'Angelo Russell, Brooklyn Nets
V3A-DV Devin Vassell, San Antonio Spurs
V3A-DW Derrick White, Boston Celtics
V3A-FW Franz Wagner, Orlando Magic
V3A-GA Giannis Antetokounmpo, Milwaukee Bucks
V3A-GD Gradey Dick, Toronto Raptors
V3A-GT Gary Trent Jr., Milwaukee Bucks
V3A-HJ Herbert Jones, New Orleans Pelicans
V3A-IC Isaiah Collier, Utah Jazz
V3A-JA Jarrett Allen, Cleveland Cavaliers
V3A-JB Jalen Brunson, New York Knicks
V3A-JH James Harden, Los Angeles Clippers
V3A-JHA Jordan Hawkins, New Orleans Pelicans
V3A-JHO Jrue Holiday, Boston Celtics
V3A-JJ Jaime Jaquez Jr., Miami Heat
V3A-JJJ Jaren Jackson Jr., Memphis Grizzlies
V3A-JM Jamal Murray, Denver Nuggets
V3A-JT Jayson Tatum, Boston Celtics
V3A-JW Jalen Williams, Oklahoma City Thunder
V3A-KF Kyle Filipowski, Utah Jazz
V3A-KP Kristaps Porzingis, Boston Celtics
V3A-KW Kel'el Ware, Miami Heat
V3A-LJ LeBron James, Los Angeles Lakers
V3A-LM Lauri Markkanen, Utah Jazz
V3A-MB Mikal Bridges, New York Knicks
V3A-MP Michael Porter Jr., Denver Nuggets
V3A-MT Myles Turner, Indiana Pacers
V3A-NC Nic Claxton, Brooklyn Nets
V3A-OA OG Anunoby, New York Knicks
V3A-OT Obi Toppin, Indiana Pacers
V3A-PB Paolo Banchero, Orlando Magic
V3A-PP Payton Pritchard, Boston Celtics
V3A-RD Ryan Dunn, Phoenix Suns
V3A-RDI Rob Dillingham, Minnesota Timberwolves
V3A-RG Rudy Gobert, Minnesota Timberwolves
V3A-RH Ronald Holland II, Detroit Pistons
V3A-SC Stephen Curry, Golden State Warriors
V3A-SCA Stephon Castle, San Antonio Spurs
V3A-SGA Shai Gilgeous-Alexander, Oklahoma City Thunder
V3A-SH Scoot Henderson, Portland Trail Blazers
V3A-SS Shaedon Sharpe, Portland Trail Blazers
V3A-TDS Tristan da Silva, Orlando Magic
V3A-THA Tyrese Haliburton, Indiana Pacers
V3A-THD Taylor Hendricks, Utah Jazz
V3A-TM Tyrese Maxey, Philadelphia 76ers
V3A-TS Tyler Smith, Milwaukee Bucks
V3A-TSA Tidjane Salaün, Charlotte Hornets
V3A-TSJ Terrence Shannon Jr., Minnesota Timberwolves
V3A-VW Victor Wembanyama, San Antonio Spurs
V3A-WK Walker Kessler, Utah Jazz
V3A-YM Yves Missi, New Orleans Pelicans
V3A-ZE Zach Edey, Memphis Grizzlies
V3A-ZR Zaccharie Risacher, Atlanta Hawks
"""

FFR_RAW = """
FFR-AB Ace Bailey, Utah Jazz
FFR-AM Alijah Martin, Toronto Raptors
FFR-AN Asa Newell, Atlanta Hawks
FFR-AT Adou Thiero, Los Angeles Lakers
FFR-BB Brooks Barnhizer, Oklahoma City Thunder
FFR-BS Ben Saraf, Brooklyn Nets
FFR-CC Cedric Coward, Memphis Grizzlies
FFR-CF Cooper Flagg, Dallas Mavericks
FFR-CL Chaz Lanier, Detroit Pistons
FFR-CM Collin Murray-Boyles, Toronto Raptors
FFR-DH Dylan Harper, San Antonio Spurs
FFR-DP Drake Powell, Brooklyn Nets
FFR-DQ Derik Queen, New Orleans Pelicans
FFR-DW Danny Wolf, Brooklyn Nets
FFR-ED Egor Dëmin, Brooklyn Nets
FFR-JB Joan Beringer, Minnesota Timberwolves
FFR-JBR Johni Broome, Philadelphia 76ers
FFR-JR Jase Richardson, Orlando Magic
FFR-JW Jamir Watkins, Washington Wizards
FFR-KB Koby Brea, Phoenix Suns
FFR-KJ Kasparas Jakučionis, Miami Heat
FFR-KJO Kam Jones, Indiana Pacers
FFR-KK Kon Knueppel, Charlotte Hornets
FFR-KM Khaman Maluach, Phoenix Suns
FFR-LM Liam McNeeley, Charlotte Hornets
FFR-MP Micah Peavy, New Orleans Pelicans
FFR-MR Maxime Raynaud, Sacramento Kings
FFR-NC Nique Clifford, Sacramento Kings
FFR-NE Noa Essengue, Chicago Bulls
FFR-NP Noah Penda, Orlando Magic
FFR-NT Nolan Traore, Brooklyn Nets
FFR-RF Rasheer Fleming, Phoenix Suns
FFR-RK Ryan Kalkbrenner, Charlotte Hornets
FFR-SJ Sion James, Charlotte Hornets
FFR-TP Tyrese Proctor, Cleveland Cavaliers
FFR-TS Thomas Sorber, Oklahoma City Thunder
FFR-WC Walter Clayton Jr., Utah Jazz
FFR-WR Will Riley, Washington Wizards
FFR-YH Yang Hansen, Portland Trail Blazers
FFR-YK Yanic Konan-Niederhäuser, Los Angeles Clippers
"""

RS_RAW = """
RS-AB Ace Bailey, Utah Jazz RC
RS-AI Allen Iverson, Philadelphia 76ers
RS-AS Alex Sarr, Washington Wizards
RS-BJ Bronny James, Los Angeles Lakers
RS-CC Cedric Coward, Memphis Grizzlies RC
RS-CF Cooper Flagg, Dallas Mavericks RC
RS-CM Collin Murray-Boyles, Toronto Raptors RC
RS-CW Cam Whitmore, Houston Rockets
RS-DH Dylan Harper, San Antonio Spurs RC
RS-DN Dirk Nowitzki, Dallas Mavericks
RS-ED Egor Dëmin, Brooklyn Nets RC
RS-GD Gradey Dick, Toronto Raptors
RS-GH Grant Hill, Detroit Pistons
RS-IC Isaiah Collier, Utah Jazz
RS-JH James Harden, Los Angeles Clippers
RS-JHA Jordan Hawkins, New Orleans Pelicans
RS-JHO Jrue Holiday, Boston Celtics
RS-JHS Jalen Hood-Schifino, Philadelphia 76ers
RS-JHW Jett Howard, Orlando Magic
RS-JJ Jaren Jackson Jr., Memphis Grizzlies
RS-JT Jayson Tatum, Boston Celtics
RS-JW Jarace Walker, Indiana Pacers
RS-KA Kareem Abdul-Jabbar, Los Angeles Lakers
RS-KD Kevin Durant, Phoenix Suns
RS-KG Kevin Garnett, Boston Celtics
RS-KKN Kon Knueppel, Charlotte Hornets RC
RS-KL Kevin Love, Miami Heat
RS-KM Khris Middleton, Washington Wizards
RS-KMM Khaman Maluach, Phoenix Suns RC
RS-KP Kristaps Porzingis, Boston Celtics
RS-NE Noa Essengue, Chicago Bulls RC
RS-PB Paolo Banchero, Orlando Magic
RS-PG Pau Gasol, Los Angeles Lakers
RS-PP Paul Pierce, Boston Celtics
RS-RA Ray Allen, Boston Celtics
RS-RD Rob Dillingham, Minnesota Timberwolves
RS-RH Ronald Holland II, Detroit Pistons
RS-SC Stephen Curry, Golden State Warriors
RS-SCA Stephon Castle, San Antonio Spurs
RS-SH Scoot Henderson, Portland Trail Blazers
RS-SO Shaquille O'Neal, Los Angeles Lakers
RS-TH Taylor Hendricks, Utah Jazz
RS-TM Tyrese Maxey, Philadelphia 76ers
RS-TS Tidjane Salaün, Charlotte Hornets
RS-VC Vince Carter, Toronto Raptors
RS-VW Victor Wembanyama, San Antonio Spurs
RS-YH Yang Hansen, Portland Trail Blazers RC
RS-ZR Zaccharie Risacher, Atlanta Hawks
"""

SS_RAW = """
SS-AB Anthony Black, Orlando Magic
SS-BJ Bronny James, Los Angeles Lakers
SS-BM Brandon Miller, Charlotte Hornets
SS-CA Carmelo Anthony, Denver Nuggets
SS-CH Chet Holmgren, Oklahoma City Thunder
SS-CW Cam Whitmore, Houston Rockets
SS-DH Dwight Howard, Orlando Magic
SS-DMI Donovan Mitchell, Cleveland Cavaliers
SS-DQ Derik Queen, New Orleans Pelicans RC
SS-DW Dwyane Wade, Miami Heat
SS-GD Gradey Dick, Toronto Raptors
SS-IC Isaiah Collier, Utah Jazz
SS-JB Joan Beringer, Minnesota Timberwolves RC
SS-JBR Johni Broome, Philadelphia 76ers RC
SS-JH Jalen Hood-Schifino, Philadelphia 76ers
SS-JHA Jordan Hawkins, New Orleans Pelicans
SS-JHO Jrue Holiday, Boston Celtics
SS-JHW Jett Howard, Orlando Magic
SS-JJ Jaren Jackson Jr., Memphis Grizzlies
SS-JM Jamal Murray, Denver Nuggets
SS-JS John Stockton, Utah Jazz
SS-JW Jarace Walker, Indiana Pacers
SS-KJ Kasparas Jakučionis, Miami Heat RC
SS-KL Kevin Love, Miami Heat
SS-KM Khris Middleton, Washington Wizards
SS-KMA Karl Malone, Utah Jazz
SS-KP Kristaps Porzingis, Boston Celtics
SS-KT Karl-Anthony Towns, New York Knicks
SS-LB Larry Bird, Boston Celtics
SS-LM Liam McNeeley, Charlotte Hornets RC
SS-MG Manu Ginobili, San Antonio Spurs
SS-MJ Magic Johnson, Los Angeles Lakers
SS-NC Nique Clifford, Sacramento Kings RC
SS-NE Noa Essengue, Chicago Bulls RC
SS-RD Rob Dillingham, Minnesota Timberwolves
SS-SC Stephon Castle, San Antonio Spurs
SS-THA Tyrese Haliburton, Indiana Pacers
SS-THE Taylor Hendricks, Utah Jazz
SS-TM Tracy McGrady, Toronto Raptors
SS-WC Walter Clayton Jr., Utah Jazz RC
SS-YH Yang Hansen, Portland Trail Blazers RC
SS-YK Yanic Konan-Niederhäuser, Los Angeles Clippers RC
SS-ZL Zach LaVine, Sacramento Kings
SS-ZR Zaccharie Risacher, Atlanta Hawks
"""

RM_RAW = """
RM-AJ AJ Johnson, Washington Wizards
RM-AM Alijah Martin, Toronto Raptors RC
RM-AT Adou Thiero, Los Angeles Lakers RC
RM-BB Brooks Barnhizer, Oklahoma City Thunder RC
RM-CK Corey Kispert, Washington Wizards
RM-CL Chaz Lanier, Detroit Pistons RC
RM-DG Daniel Gafford, Dallas Mavericks
RM-DH DaRon Holmes II, Denver Nuggets
RM-DR Duncan Robinson, Miami Heat
RM-JB Johni Broome, Philadelphia 76ers RC
RM-JJ Jaime Jaquez Jr., Miami Heat
RM-JR Jalen Rose, Indiana Pacers
RM-JSA Jerry Stackhouse, Detroit Pistons
RM-JV Jarred Vanderbilt, Los Angeles Lakers
RM-JW Jamir Watkins, Washington Wizards RC
RM-KB Koby Brea, Phoenix Suns RC
RM-KG Kyshawn George, Washington Wizards
RM-KJ Kam Jones, Indiana Pacers RC
RM-KM Kris Murray, Portland Trail Blazers
RM-KW Kel'el Ware, Miami Heat
RM-MP Micah Peavy, New Orleans Pelicans RC
RM-MR Maxime Raynaud, Sacramento Kings RC
RM-MW Metta World Peace, Los Angeles Lakers
RM-NB Nicolas Batum, Los Angeles Clippers
RM-NP Noah Penda, Orlando Magic RC
RM-PS Peja Stojakovic, Sacramento Kings
RM-RD Ryan Dunn, Phoenix Suns
RM-RF Rasheer Fleming, Phoenix Suns RC
RM-RH Rip Hamilton, Detroit Pistons
RM-RHO Robert Horry, Los Angeles Lakers
RM-RJ Richard Jefferson, Cleveland Cavaliers
RM-RK Ryan Kalkbrenner, Charlotte Hornets RC
RM-SH Sam Hauser, Boston Celtics
RM-SJ Sion James, Charlotte Hornets RC
RM-SW Spud Webb, Atlanta Hawks
RM-TD Tristan da Silva, Orlando Magic
RM-TP Tyrese Proctor, Cleveland Cavaliers RC
RM-TS Tyler Smith, Milwaukee Bucks
RM-TSJ Terrence Shannon Jr., Minnesota Timberwolves
RM-YM Yves Missi, New Orleans Pelicans
RM-ZR Zach Randolph, Memphis Grizzlies
"""

FS_RAW = """
FS-AH Al Horford, Boston Celtics
FS-AM Alijah Martin, Toronto Raptors RC
FS-AT Adou Thiero, Los Angeles Lakers RC
FS-BB Brooks Barnhizer, Oklahoma City Thunder RC
FS-CL Chaz Lanier, Detroit Pistons RC
FS-CW Cody Williams, Utah Jazz
FS-GD Gradey Dick, Toronto Raptors
FS-JH Jrue Holiday, Boston Celtics
FS-JJ Jaime Jaquez Jr., Miami Heat
FS-JR Jalen Rose, Indiana Pacers
FS-JS Jerry Stackhouse, Detroit Pistons
FS-JT Jaylon Tyson, Cleveland Cavaliers
FS-JW Jamir Watkins, Washington Wizards RC
FS-KB Koby Brea, Phoenix Suns RC
FS-KF Kyle Filipowski, Utah Jazz
FS-KJ Kam Jones, Indiana Pacers RC
FS-KP Kristaps Porzingis, Boston Celtics
FS-KT Karl-Anthony Towns, New York Knicks
FS-KW Kel'el Ware, Miami Heat
FS-LM Lauri Markkanen, Utah Jazz
FS-MB Mikal Bridges, New York Knicks
FS-MPA Micah Peavy, New Orleans Pelicans RC
FS-MR Maxime Raynaud, Sacramento Kings RC
FS-MS Marcus Smart, Washington Wizards
FS-MW Metta World Peace, Los Angeles Lakers
FS-NT Nikola Topić, Oklahoma City Thunder
FS-PS Peja Stojakovic, Sacramento Kings
FS-RD Ryan Dunn, Phoenix Suns
FS-RH Ronald Holland II, Detroit Pistons
FS-RHO Robert Horry, Los Angeles Lakers
FS-RJ Richard Jefferson, Cleveland Cavaliers
FS-SW Spud Webb, Atlanta Hawks
FS-TH Tyrese Haliburton, Indiana Pacers
FS-TM Tyrese Maxey, Philadelphia 76ers
FS-TP Tyrese Proctor, Cleveland Cavaliers RC
FS-TS Tidjane Salaün, Charlotte Hornets
FS-TSM Tyler Smith, Milwaukee Bucks
FS-ZE Zach Edey, Memphis Grizzlies
FS-ZL Zach LaVine, Sacramento Kings
FS-ZR Zach Randolph, Memphis Grizzlies
"""

HM_RAW = """
HM-AB Ace Bailey, Utah Jazz RC
HM-AI Allen Iverson, Philadelphia 76ers
HM-AS Alex Sarr, Washington Wizards
HM-CA Carmelo Anthony, Denver Nuggets
HM-CF Cooper Flagg, Dallas Mavericks RC
HM-CJ Cameron Johnson, Brooklyn Nets
HM-CM CJ McCollum, New Orleans Pelicans
HM-CMB Collin Murray-Boyles, Toronto Raptors RC
HM-DH Dylan Harper, San Antonio Spurs RC
HM-DMI Donovan Mitchell, Cleveland Cavaliers
HM-DR Dennis Rodman, Chicago Bulls
HM-DW Dwyane Wade, Miami Heat
HM-ED Egor Dëmin, Brooklyn Nets RC
HM-GD Gradey Dick, Toronto Raptors
HM-JH James Harden, Los Angeles Clippers
HM-JK Jason Kidd, Dallas Mavericks
HM-JT Jayson Tatum, Boston Celtics
HM-KD Kevin Durant, Phoenix Suns
HM-KJ Kasparas Jakučionis, Miami Heat RC
HM-KK Kon Knueppel, Charlotte Hornets RC
HM-KL Kevin Love, Miami Heat
HM-KM Khris Middleton, Washington Wizards
HM-KP Kristaps Porzingis, Boston Celtics
HM-LB Larry Bird, Boston Celtics
HM-LM Liam McNeeley, Charlotte Hornets RC
HM-MG Manu Ginobili, San Antonio Spurs
HM-MJ Magic Johnson, Los Angeles Lakers
HM-MP Michael Porter Jr., Denver Nuggets
HM-NT Nolan Traore, Brooklyn Nets RC
HM-PB Paolo Banchero, Orlando Magic
HM-PP Paul Pierce, Boston Celtics
HM-RA Ray Allen, Boston Celtics
HM-SC Stephon Castle, San Antonio Spurs
HM-SCU Stephen Curry, Golden State Warriors
HM-THA Tyrese Haliburton, Indiana Pacers
HM-TM Tyrese Maxey, Philadelphia 76ers
HM-TP Tony Parker, San Antonio Spurs
HM-VW Victor Wembanyama, San Antonio Spurs
HM-WC Walter Clayton Jr., Utah Jazz RC
HM-ZL Zach LaVine, Sacramento Kings
HM-ZR Zaccharie Risacher, Atlanta Hawks
"""

TPA_RAW = """
TP-AB Anthony Black, Orlando Magic
TP-AH Al Horford, Boston Celtics
TP-AJ AJ Johnson, Washington Wizards
TP-AM Alonzo Mourning, Miami Heat
TP-AMA Alijah Martin, Toronto Raptors RC
TP-AW Amari Williams, Boston Celtics
TP-BB Brooks Barnhizer, Oklahoma City Thunder RC
TP-BC Brandon Clarke, Memphis Grizzlies
TP-CL Chaz Lanier, Detroit Pistons RC
TP-DG Daniel Gafford, Dallas Mavericks
TP-DH DaRon Holmes II, Denver Nuggets
TP-DR Dennis Rodman, Chicago Bulls
TP-DRO David Robinson, San Antonio Spurs
TP-HO Hakeem Olajuwon, Houston Rockets
TP-JH Jrue Holiday, Boston Celtics
TP-JJ Jaime Jaquez Jr., Miami Heat
TP-JK Jason Kidd, Dallas Mavericks
TP-JS Jeremy Sochan, San Antonio Spurs
TP-JSM Javon Small, Memphis Grizzlies RC
TP-JW Jamir Watkins, Washington Wizards RC
TP-KB Koby Brea, Phoenix Suns RC
TP-KF Kyle Filipowski, Utah Jazz
TP-KG Kyshawn George, Washington Wizards
TP-KJ Kam Jones, Indiana Pacers RC
TP-KM Khris Middleton, Washington Wizards
TP-KMU Kris Murray, Portland Trail Blazers
TP-KW Kel'el Ware, Miami Heat
TP-LM Lauri Markkanen, Utah Jazz
TP-MB Mikal Bridges, New York Knicks
TP-MP Micah Peavy, New Orleans Pelicans RC
TP-MR Maxime Raynaud, Sacramento Kings RC
TP-MS Marcus Smart, Washington Wizards
TP-NT Nikola Topić, Oklahoma City Thunder
TP-PP Payton Pritchard, Boston Celtics
TP-PPI Paul Pierce, Boston Celtics
TP-RA Ray Allen, Boston Celtics
TP-RD Ryan Dunn, Phoenix Suns
TP-RH Ronald Holland II, Detroit Pistons
TP-TK Tyler Kolek, New York Knicks
TP-TS Tidjane Salaün, Charlotte Hornets
TP-TSJ Terrence Shannon Jr., Minnesota Timberwolves
TP-TSM Tyler Smith, Milwaukee Bucks
TP-Td Tristan da Silva, Orlando Magic
TP-VC Vince Carter, Toronto Raptors
TP-YM Yves Missi, New Orleans Pelicans
TP-ZE Zach Edey, Memphis Grizzlies
"""

RA_RAW = """
RA-AB Ace Bailey, Utah Jazz
RA-AM Alijah Martin, Toronto Raptors
RA-AN Asa Newell, Atlanta Hawks
RA-AT Adou Thiero, Los Angeles Lakers
RA-BB Brooks Barnhizer, Oklahoma City Thunder
RA-BS Ben Saraf, Brooklyn Nets
RA-CC Cedric Coward, Memphis Grizzlies
RA-CF Cooper Flagg, Dallas Mavericks
RA-CL Chaz Lanier, Detroit Pistons
RA-CM Collin Murray-Boyles, Toronto Raptors
RA-DH Dylan Harper, San Antonio Spurs
RA-DP Drake Powell, Brooklyn Nets
RA-DQ Derik Queen, New Orleans Pelicans
RA-DW Danny Wolf, Brooklyn Nets
RA-ED Egor Dëmin, Brooklyn Nets
RA-JB Joan Beringer, Minnesota Timberwolves
RA-JBR Johni Broome, Philadelphia 76ers
RA-JR Jase Richardson, Orlando Magic
RA-JW Jamir Watkins, Washington Wizards
RA-KB Koby Brea, Phoenix Suns
RA-KJ Kasparas Jakučionis, Miami Heat
RA-KJO Kam Jones, Indiana Pacers
RA-KK Kon Knueppel, Charlotte Hornets
RA-KM Khaman Maluach, Phoenix Suns
RA-LM Liam McNeeley, Charlotte Hornets
RA-MP Micah Peavy, New Orleans Pelicans
RA-MR Maxime Raynaud, Sacramento Kings
RA-NC Nique Clifford, Sacramento Kings
RA-NE Noa Essengue, Chicago Bulls
RA-NP Noah Penda, Orlando Magic
RA-NT Nolan Traore, Brooklyn Nets
RA-RF Rasheer Fleming, Phoenix Suns
RA-RK Ryan Kalkbrenner, Charlotte Hornets
RA-SJ Sion James, Charlotte Hornets
RA-TP Tyrese Proctor, Cleveland Cavaliers
RA-TS Thomas Sorber, Oklahoma City Thunder
RA-WC Walter Clayton Jr., Utah Jazz
RA-WR Will Riley, Washington Wizards
RA-YH Yang Hansen, Portland Trail Blazers
RA-YK Yanic Konan-Niederhäuser, Los Angeles Clippers
"""

TD_RAW = """
TD-AB Ace Bailey, Utah Jazz RC
TD-AE Alex English, Denver Nuggets
TD-AG Aaron Gordon, Denver Nuggets
TD-AH Anfernee Hardaway, Orlando Magic
TD-AHO Al Horford, Boston Celtics
TD-AN Asa Newell, Atlanta Hawks RC
TD-AS Alex Sarr, Washington Wizards
TD-BM Brandon Miller, Charlotte Hornets
TD-CD Clyde Drexler, Portland Trail Blazers
TD-CF Cooper Flagg, Dallas Mavericks RC
TD-CH Chet Holmgren, Oklahoma City Thunder
TD-DH Dwight Howard, Orlando Magic
TD-DHR Dylan Harper, San Antonio Spurs RC
TD-DM Donovan Mitchell, Cleveland Cavaliers
TD-DP Drake Powell, Brooklyn Nets RC
TD-DQ Derik Queen, New Orleans Pelicans RC
TD-DR David Robinson, San Antonio Spurs
TD-DT David Thompson, Denver Nuggets
TD-DW Dwyane Wade, Miami Heat
TD-DWL Dominique Wilkins, Atlanta Hawks
TD-GG George Gervin, San Antonio Spurs
TD-GH Grant Hill, Detroit Pistons
TD-HO Hakeem Olajuwon, Houston Rockets
TD-JH James Harden, Los Angeles Clippers
TD-JJ Jaime Jaquez Jr., Miami Heat
TD-JR Jase Richardson, Orlando Magic RC
TD-JS Jerry Stackhouse, Detroit Pistons
TD-JT Jayson Tatum, Boston Celtics
TD-JTY Jaylon Tyson, Cleveland Cavaliers
TD-JW Jarace Walker, Indiana Pacers
TD-KD Kevin Durant, Phoenix Suns
TD-KG Kevin Garnett, Boston Celtics
TD-KGO Kyshawn George, Washington Wizards
TD-KW Kel'el Ware, Miami Heat
TD-LJ LeBron James, Los Angeles Lakers
TD-LJO Larry Johnson, New York Knicks
TD-LM Liam McNeeley, Charlotte Hornets RC
TD-MP Michael Porter Jr., Denver Nuggets
TD-NE Noa Essengue, Chicago Bulls RC
TD-PB Paolo Banchero, Orlando Magic
TD-RH Rip Hamilton, Detroit Pistons
TD-SC Stephon Castle, San Antonio Spurs
TD-SO Shaquille O'Neal, Los Angeles Lakers
TD-SW Spud Webb, Atlanta Hawks
TD-TD Tristan da Silva, Orlando Magic
TD-TH Tyrese Haliburton, Indiana Pacers
TD-TM Tracy McGrady, Toronto Raptors
TD-VC Vince Carter, Toronto Raptors
TD-VW Victor Wembanyama, San Antonio Spurs
TD-WC Walter Clayton Jr., Utah Jazz RC
TD-YM Yves Missi, New Orleans Pelicans
TD-ZE Zach Edey, Memphis Grizzlies
TD-ZL Zach LaVine, Sacramento Kings
TD-ZR Zaccharie Risacher, Atlanta Hawks
"""

RV_RAW = """
RV-AB Ace Bailey, Utah Jazz
RV-AM Alijah Martin, Toronto Raptors
RV-AN Asa Newell, Atlanta Hawks
RV-AT Adou Thiero, Los Angeles Lakers
RV-BB Brooks Barnhizer, Oklahoma City Thunder
RV-BS Ben Saraf, Brooklyn Nets
RV-CC Cedric Coward, Memphis Grizzlies
RV-CF Cooper Flagg, Dallas Mavericks
RV-CL Chaz Lanier, Detroit Pistons
RV-CM Collin Murray-Boyles, Toronto Raptors
RV-DH Dylan Harper, San Antonio Spurs
RV-DP Drake Powell, Brooklyn Nets
RV-DQ Derik Queen, New Orleans Pelicans
RV-DW Danny Wolf, Brooklyn Nets
RV-ED Egor Dëmin, Brooklyn Nets
RV-JB Joan Beringer, Minnesota Timberwolves
RV-JBR Johni Broome, Philadelphia 76ers
RV-JR Jase Richardson, Orlando Magic
RV-JW Jamir Watkins, Washington Wizards
RV-KB Koby Brea, Phoenix Suns
RV-KJ Kasparas Jakučionis, Miami Heat
RV-KJO Kam Jones, Indiana Pacers
RV-KK Kon Knueppel, Charlotte Hornets
RV-KM Khaman Maluach, Phoenix Suns
RV-LM Liam McNeeley, Charlotte Hornets
RV-MP Micah Peavy, New Orleans Pelicans
RV-MR Maxime Raynaud, Sacramento Kings
RV-NC Nique Clifford, Sacramento Kings
RV-NE Noa Essengue, Chicago Bulls
RV-NP Noah Penda, Orlando Magic
RV-NT Nolan Traore, Brooklyn Nets
RV-RF Rasheer Fleming, Phoenix Suns
RV-RK Ryan Kalkbrenner, Charlotte Hornets
RV-SJ Sion James, Charlotte Hornets
RV-TP Tyrese Proctor, Cleveland Cavaliers
RV-TS Thomas Sorber, Oklahoma City Thunder
RV-WC Walter Clayton Jr., Utah Jazz
RV-WRI Will Riley, Washington Wizards
RV-YH Yang Hansen, Portland Trail Blazers
RV-YK Yanic Konan-Niederhäuser, Los Angeles Clippers
"""

RR_RAW = """
RR-AB Ace Bailey, Utah Jazz RC
RR-AN Asa Newell, Atlanta Hawks RC
RR-AS Alex Sarr, Washington Wizards
RR-CF Cooper Flagg, Dallas Mavericks RC
RR-CH Chet Holmgren, Oklahoma City Thunder
RR-CW Cody Williams, Utah Jazz
RR-DH Dwight Howard, Orlando Magic
RR-DHR Dylan Harper, San Antonio Spurs RC
RR-DM Donovan Mitchell, Cleveland Cavaliers
RR-DN Dirk Nowitzki, Dallas Mavericks
RR-DQ Derik Queen, New Orleans Pelicans RC
RR-DR David Robinson, San Antonio Spurs
RR-DW Dominique Wilkins, Atlanta Hawks
RR-ED Egor Dëmin, Brooklyn Nets RC
RR-GD Gradey Dick, Toronto Raptors
RR-HO Hakeem Olajuwon, Houston Rockets
RR-JH Jrue Holiday, Boston Celtics
RR-JJ Jaren Jackson Jr., Memphis Grizzlies
RR-JS Jerry Stackhouse, Detroit Pistons
RR-KA Kareem Abdul-Jabbar, Los Angeles Lakers
RR-KD Kevin Durant, Phoenix Suns
RR-KJ Kasparas Jakučionis, Miami Heat RC
RR-KM Karl Malone, Utah Jazz
RR-KMA Khaman Maluach, Phoenix Suns RC
RR-KP Kristaps Porzingis, Boston Celtics
RR-KW Kel'el Ware, Miami Heat
RR-LJ Larry Johnson, New York Knicks
RR-NE Noa Essengue, Chicago Bulls RC
RR-NT Nikola Topić, Oklahoma City Thunder
RR-PG Pau Gasol, Los Angeles Lakers
RR-RHO Ronald Holland II, Detroit Pistons
RR-SC Stephon Castle, San Antonio Spurs
RR-TD Tristan da Silva, Orlando Magic
RR-VW Victor Wembanyama, San Antonio Spurs
RR-YH Yang Hansen, Portland Trail Blazers RC
RR-ZE Zach Edey, Memphis Grizzlies
RR-ZR Zaccharie Risacher, Atlanta Hawks
"""

QG_RAW = """
QG-AB Ace Bailey, Utah Jazz
QG-AN Asa Newell, Atlanta Hawks
QG-BS Ben Saraf, Brooklyn Nets
QG-CC Cedric Coward, Memphis Grizzlies
QG-CF Cooper Flagg, Dallas Mavericks
QG-CM Collin Murray-Boyles, Toronto Raptors
QG-DH Dylan Harper, San Antonio Spurs
QG-DP Drake Powell, Brooklyn Nets
QG-DQ Derik Queen, New Orleans Pelicans
QG-DW Danny Wolf, Brooklyn Nets
QG-ED Egor Dëmin, Brooklyn Nets
QG-JB Joan Beringer, Minnesota Timberwolves
QG-JR Jase Richardson, Orlando Magic
QG-KJ Kasparas Jakučionis, Miami Heat
QG-KK Kon Knueppel, Charlotte Hornets
QG-KM Khaman Maluach, Phoenix Suns
QG-KO Kam Jones, Indiana Pacers
QG-LM Liam McNeeley, Charlotte Hornets
QG-NC Nique Clifford, Sacramento Kings
QG-NE Noa Essengue, Chicago Bulls
QG-NP Noah Penda, Orlando Magic
QG-NT Nolan Traore, Brooklyn Nets
QG-RF Rasheer Fleming, Phoenix Suns
QG-RK Ryan Kalkbrenner, Charlotte Hornets
QG-SJ Sion James, Charlotte Hornets
QG-TS Thomas Sorber, Oklahoma City Thunder
QG-WC Walter Clayton Jr., Utah Jazz
QG-WR Will Riley, Washington Wizards
QG-YH Yang Hansen, Portland Trail Blazers
QG-YK Yanic Konan-Niederhäuser, Los Angeles Clippers
"""

CD_RAW = """
CD-AB Ace Bailey, Utah Jazz RC
CD-BM Brandon Miller, Charlotte Hornets
CD-CC Cedric Coward, Memphis Grizzlies RC
CD-CF Cooper Flagg, Dallas Mavericks RC
CD-CM Collin Murray-Boyles, Toronto Raptors RC
CD-DH Dylan Harper, San Antonio Spurs RC
CD-DQ Derik Queen, New Orleans Pelicans RC
CD-ED Egor Dëmin, Brooklyn Nets RC
CD-HO Hakeem Olajuwon, Houston Rockets
CD-JK Jason Kidd, Dallas Mavericks
CD-JS Jerry Stackhouse, Detroit Pistons
CD-KK Kon Knueppel, Charlotte Hornets RC
CD-KM Khaman Maluach, Phoenix Suns RC
CD-KP Kristaps Porzingis, Boston Celtics
CD-KW Kel'el Ware, Miami Heat
CD-MW Metta World Peace, Los Angeles Lakers
CD-NE Noa Essengue, Chicago Bulls RC
CD-PB Paolo Banchero, Orlando Magic
CD-PS Peja Stojakovic, Sacramento Kings
CD-RB Rick Barry, Golden State Warriors
CD-RH Robert Horry, Los Angeles Lakers
CD-SC Stephen Curry, Golden State Warriors
CD-SCA Stephon Castle, San Antonio Spurs
CD-SW Spud Webb, Atlanta Hawks
CD-TH Tyrese Haliburton, Indiana Pacers
CD-TM Tyrese Maxey, Philadelphia 76ers
CD-TP Tony Parker, San Antonio Spurs
CD-ZR Zach Randolph, Memphis Grizzlies
"""

NF_RAW = """
NF-AB Ace Bailey, Utah Jazz
NF-AM Alijah Martin, Toronto Raptors
NF-BB Brooks Barnhizer, Oklahoma City Thunder
NF-BS Ben Saraf, Brooklyn Nets
NF-CC Cedric Coward, Memphis Grizzlies
NF-CF Cooper Flagg, Dallas Mavericks
NF-CL Chaz Lanier, Detroit Pistons
NF-CM Collin Murray-Boyles, Toronto Raptors
NF-DH Dylan Harper, San Antonio Spurs
NF-DP Drake Powell, Brooklyn Nets
NF-DW Danny Wolf, Brooklyn Nets
NF-ED Egor Dëmin, Brooklyn Nets
NF-JB Joan Beringer, Minnesota Timberwolves
NF-JBR Johni Broome, Philadelphia 76ers
NF-JR Jase Richardson, Orlando Magic
NF-JW Jamir Watkins, Washington Wizards
NF-KB Koby Brea, Phoenix Suns
NF-KJ Kasparas Jakučionis, Miami Heat
NF-KJO Kam Jones, Indiana Pacers
NF-KK Kon Knueppel, Charlotte Hornets
NF-KM Khaman Maluach, Phoenix Suns
NF-LM Liam McNeeley, Charlotte Hornets
NF-MP Micah Peavy, New Orleans Pelicans
NF-MR Maxime Raynaud, Sacramento Kings
NF-NE Noa Essengue, Chicago Bulls
NF-NP Noah Penda, Orlando Magic
NF-NT Nolan Traore, Brooklyn Nets
NF-RK Ryan Kalkbrenner, Charlotte Hornets
NF-SJ Sion James, Charlotte Hornets
NF-TP Tyrese Proctor, Cleveland Cavaliers
NF-TS Thomas Sorber, Oklahoma City Thunder
"""

GT_RAW = """
GT-AB Anthony Black, Orlando Magic
GT-ABA Ace Bailey, Utah Jazz RC
GT-AE Alex English, Denver Nuggets
GT-AH Al Horford, Boston Celtics
GT-AM Alonzo Mourning, Miami Heat
GT-CC Cedric Coward, Memphis Grizzlies RC
GT-CD Clyde Drexler, Portland Trail Blazers
GT-CM Collin Murray-Boyles, Toronto Raptors RC
GT-DD Donte DiVincenzo, Minnesota Timberwolves
GT-DR Dennis Rodman, Chicago Bulls
GT-ED Egor Dëmin, Brooklyn Nets RC
GT-GD Gradey Dick, Toronto Raptors
GT-HO Hakeem Olajuwon, Houston Rockets
GT-JH Jordan Hawkins, New Orleans Pelicans
GT-JHO Jrue Holiday, Boston Celtics
GT-JHS Jalen Hood-Schifino, Philadelphia 76ers
GT-JJ Jaren Jackson Jr., Memphis Grizzlies
GT-JJJ Jaime Jaquez Jr., Miami Heat
GT-JM Jamal Murray, Denver Nuggets
GT-JS Jerry Stackhouse, Detroit Pistons
GT-JSO Jeremy Sochan, San Antonio Spurs
GT-JT Jaylon Tyson, Cleveland Cavaliers
GT-KF Kyle Filipowski, Utah Jazz
GT-KK Kon Knueppel, Charlotte Hornets RC
GT-KM Khaman Maluach, Phoenix Suns RC
GT-KP Kristaps Porzingis, Boston Celtics
GT-KT Karl-Anthony Towns, New York Knicks
GT-KW Kel'el Ware, Miami Heat
GT-LJ Larry Johnson, New York Knicks
GT-MP Michael Porter Jr., Denver Nuggets
GT-MS Marcus Smart, Washington Wizards
GT-MW Metta World Peace, Los Angeles Lakers
GT-NE Noa Essengue, Chicago Bulls RC
GT-NT Nolan Traore, Brooklyn Nets RC
GT-PS Peja Stojakovic, Sacramento Kings
GT-RB Rick Barry, Golden State Warriors
GT-RD Ryan Dunn, Phoenix Suns
GT-RHL Ronald Holland II, Detroit Pistons
GT-RHO Robert Horry, Los Angeles Lakers
GT-SC Stephon Castle, San Antonio Spurs
GT-SW Spud Webb, Atlanta Hawks
GT-TH Taylor Hendricks, Utah Jazz
GT-TP Tony Parker, San Antonio Spurs
GT-TS Tidjane Salaün, Charlotte Hornets
GT-TSM Tyler Smith, Milwaukee Bucks
GT-TSO Thomas Sorber, Oklahoma City Thunder RC
GT-ZE Zach Edey, Memphis Grizzlies
GT-ZR Zaccharie Risacher, Atlanta Hawks
GT-ZRA Zach Randolph, Memphis Grizzlies
"""

IW_RAW = """
IW-1 Cooper Flagg, Dallas Mavericks RC
IW-2 Dylan Harper, San Antonio Spurs RC
IW-3 Kon Knueppel, Charlotte Hornets RC
IW-4 VJ Edgecombe, Philadelphia 76ers RC
IW-5 Ace Bailey, Utah Jazz RC
IW-6 Tre Johnson III, Washington Wizards RC
IW-7 Jeremiah Fears, New Orleans Pelicans RC
IW-8 Egor Dëmin, Brooklyn Nets RC
IW-9 Collin Murray-Boyles, Toronto Raptors RC
IW-10 Cedric Coward, Memphis Grizzlies RC
IW-11 Walter Clayton Jr., Utah Jazz RC
IW-12 Luka Dončić, Los Angeles Lakers
IW-13 Nikola Jokić, Denver Nuggets
IW-14 Shai Gilgeous-Alexander, Oklahoma City Thunder
IW-15 Giannis Antetokounmpo, Milwaukee Bucks
IW-16 Stephen Curry, Golden State Warriors
IW-17 Anthony Edwards, Minnesota Timberwolves
IW-18 Tyrese Haliburton, Indiana Pacers
IW-19 Donovan Mitchell, Cleveland Cavaliers
IW-20 Jalen Brunson, New York Knicks
IW-21 Jayson Tatum, Boston Celtics
IW-22 Victor Wembanyama, San Antonio Spurs
IW-23 LeBron James, Los Angeles Lakers
IW-24 Anthony Davis, Dallas Mavericks
IW-25 Kevin Durant, Phoenix Suns
IW-26 Cade Cunningham, Detroit Pistons
IW-27 Kawhi Leonard, Los Angeles Clippers
IW-28 Paolo Banchero, Orlando Magic
IW-29 Trae Young, Atlanta Hawks
IW-30 Tyrese Maxey, Philadelphia 76ers
IW-31 LaMelo Ball, Charlotte Hornets
IW-32 Allen Iverson, Philadelphia 76ers
IW-33 Magic Johnson, Los Angeles Lakers
IW-34 Larry Bird, Boston Celtics
IW-35 Carmelo Anthony, Denver Nuggets
IW-36 Tracy McGrady, Toronto Raptors
IW-37 Jason Kidd, Dallas Mavericks
IW-38 Dennis Rodman, Chicago Bulls
IW-39 Paul Pierce, Boston Celtics
IW-40 John Stockton, Utah Jazz
"""

FP_RAW = """
FP-1 Cooper Flagg, Dallas Mavericks RC
FP-2 VJ Edgecombe, Philadelphia 76ers RC
FP-3 Nique Clifford, Sacramento Kings RC
FP-4 Derik Queen, New Orleans Pelicans RC
FP-5 Ryan Kalkbrenner, Charlotte Hornets RC
FP-6 Adou Thiero, Los Angeles Lakers RC
FP-7 Noa Essengue, Chicago Bulls RC
FP-8 Khaman Maluach, Phoenix Suns RC
FP-9 Asa Newell, Atlanta Hawks RC
FP-10 Rasheer Fleming, Phoenix Suns RC
FP-11 Anthony Edwards, Minnesota Timberwolves
FP-12 Ja Morant, Memphis Grizzlies
FP-13 Giannis Antetokounmpo, Milwaukee Bucks
FP-14 Jalen Green, Houston Rockets
FP-15 Donovan Mitchell, Cleveland Cavaliers
FP-16 Jaylen Brown, Boston Celtics
FP-17 LeBron James, Los Angeles Lakers
FP-18 Jayson Tatum, Boston Celtics
FP-19 Paolo Banchero, Orlando Magic
FP-20 Zach LaVine, Sacramento Kings
FP-21 Vince Carter, Toronto Raptors
FP-22 Dominique Wilkins, Atlanta Hawks
FP-23 Shawn Kemp, Cleveland Cavaliers
FP-24 Dwight Howard, Orlando Magic
FP-25 Shaquille O'Neal, Los Angeles Lakers
FP-26 Clyde Drexler, Portland Trail Blazers
FP-27 Richard Jefferson, Cleveland Cavaliers
FP-28 Kevin Garnett, Boston Celtics
FP-29 Tracy McGrady, Toronto Raptors
FP-30 Dwyane Wade, Miami Heat
"""

AR_RAW = """
AR-1 Cooper Flagg, Dallas Mavericks RC
AR-2 Dylan Harper, San Antonio Spurs RC
AR-3 VJ Edgecombe, Philadelphia 76ers RC
AR-4 Ace Bailey, Utah Jazz RC
AR-5 Tre Johnson III, Washington Wizards RC
AR-6 Cedric Coward, Memphis Grizzlies RC
AR-7 Kon Knueppel, Charlotte Hornets RC
AR-8 Khaman Maluach, Phoenix Suns RC
AR-9 Walter Clayton Jr., Utah Jazz RC
AR-10 Nolan Traore, Brooklyn Nets RC
AR-11 Stephen Curry, Golden State Warriors
AR-12 LeBron James, Los Angeles Lakers
AR-13 Nikola Jokić, Denver Nuggets
AR-14 Giannis Antetokounmpo, Milwaukee Bucks
AR-15 Joel Embiid, Philadelphia 76ers
AR-16 Luka Dončić, Los Angeles Lakers
AR-17 Jayson Tatum, Boston Celtics
AR-18 Jimmy Butler III, Golden State Warriors
AR-19 Kevin Durant, Phoenix Suns
AR-20 Damian Lillard, Milwaukee Bucks
AR-21 Tyrese Haliburton, Indiana Pacers
AR-22 Anthony Edwards, Minnesota Timberwolves
AR-23 Kawhi Leonard, Los Angeles Clippers
AR-24 Devin Booker, Phoenix Suns
AR-25 Jalen Brunson, New York Knicks
AR-26 Magic Johnson, Los Angeles Lakers
AR-27 John Stockton, Utah Jazz
AR-28 Jason Kidd, New Jersey Nets
AR-29 Larry Bird, Boston Celtics
AR-30 Tony Parker, San Antonio Spurs
"""

THREE_D_RAW = """
3D-1 Carter Bryant, San Antonio Spurs RC
3D-2 Cedric Coward, Memphis Grizzlies RC
3D-3 VJ Edgecombe, Philadelphia 76ers RC
3D-4 Collin Murray-Boyles, Toronto Raptors RC
3D-5 Noah Penda, Orlando Magic RC
3D-6 Cooper Flagg, Dallas Mavericks RC
3D-7 Dylan Harper, San Antonio Spurs RC
3D-8 Ace Bailey, Utah Jazz RC
3D-9 Kon Knueppel, Charlotte Hornets RC
3D-10 Jeremiah Fears, New Orleans Pelicans RC
3D-11 Paul George, Philadelphia 76ers
3D-12 Desmond Bane, Memphis Grizzlies
3D-13 Jalen Williams, Oklahoma City Thunder
3D-14 Derrick White, Boston Celtics
3D-15 Khris Middleton, Washington Wizards
3D-16 Cam Johnson, Brooklyn Nets
3D-17 Kawhi Leonard, Los Angeles Clippers
3D-18 Jrue Holiday, Boston Celtics
3D-19 Mikal Bridges, New York Knicks
3D-20 Jimmy Butler III, Golden State Warriors
3D-21 Anthony Edwards, Minnesota Timberwolves
3D-22 Shai Gilgeous-Alexander, Oklahoma City Thunder
3D-23 Tyrese Haliburton, Indiana Pacers
3D-24 Franz Wagner, Orlando Magic
3D-25 Tyler Herro, Miami Heat
3D-26 Payton Pritchard, Boston Celtics
3D-27 Stephen Curry, Golden State Warriors
3D-28 Victor Wembanyama, San Antonio Spurs
3D-29 Alex Caruso, Oklahoma City Thunder
3D-30 Stephon Castle, San Antonio Spurs
3D-31 Ray Allen, Boston Celtics
3D-32 Larry Bird, Boston Celtics
3D-33 Rick Barry, Golden State Warriors
3D-34 Peja Stojakovic, Sacramento Kings
3D-35 Paul Pierce, Boston Celtics
3D-36 Manu Ginobili, San Antonio Spurs
3D-37 Metta World Peace, Los Angeles Lakers
3D-38 Vince Carter, Toronto Raptors
3D-39 Tony Parker, San Antonio Spurs
3D-40 Jerry West, Los Angeles Lakers
"""

MD_RAW = """
MD-1 Klay Thompson, Dallas Mavericks
MD-2 Trae Young, Atlanta Hawks
MD-3 Jayson Tatum, Boston Celtics
MD-4 Giannis Antetokounmpo, Milwaukee Bucks
MD-5 Victor Wembanyama, San Antonio Spurs
MD-6 Damian Lillard, Milwaukee Bucks
MD-7 Donovan Mitchell, Cleveland Cavaliers
MD-8 Kyrie Irving, Dallas Mavericks
MD-9 James Harden, Los Angeles Clippers
MD-10 Tyrese Haliburton, Indiana Pacers
MD-11 Joel Embiid, Philadelphia 76ers
MD-12 Kevin Durant, Phoenix Suns
MD-13 Alex Sarr, Washington Wizards
MD-14 Zaccharie Risacher, Atlanta Hawks
MD-15 Luka Dončić, Los Angeles Lakers
MD-16 Cooper Flagg, Dallas Mavericks RC
MD-17 Dylan Harper, San Antonio Spurs RC
MD-18 VJ Edgecombe, Philadelphia 76ers RC
MD-19 Kon Knueppel, Charlotte Hornets RC
MD-20 Ace Bailey, Utah Jazz RC
MD-21 Tre Johnson III, Washington Wizards RC
MD-22 Jeremiah Fears, New Orleans Pelicans RC
MD-23 Egor Dëmin, Brooklyn Nets RC
MD-24 Collin Murray-Boyles, Toronto Raptors RC
MD-25 Khaman Maluach, Phoenix Suns RC
MD-26 Shaquille O'Neal, Los Angeles Lakers
MD-27 Kareem Abdul-Jabbar, Los Angeles Lakers
MD-28 Artis Gilmore, Chicago Bulls
MD-29 Pau Gasol, Los Angeles Lakers
MD-30 Dirk Nowitzki, Dallas Mavericks
"""

PAINT_RAW = """
TP-1 Shai Gilgeous-Alexander, Oklahoma City Thunder
TP-2 Giannis Antetokounmpo, Milwaukee Bucks
TP-3 Nikola Jokić, Denver Nuggets
TP-4 Anthony Edwards, Minnesota Timberwolves
TP-5 Jayson Tatum, Boston Celtics
TP-6 Cade Cunningham, Detroit Pistons
TP-7 Devin Booker, Phoenix Suns
TP-8 Stephen Curry, Golden State Warriors
TP-9 Ja Morant, Memphis Grizzlies
TP-10 LeBron James, Los Angeles Lakers
TP-11 Cooper Flagg, Dallas Mavericks RC
TP-12 Dylan Harper, San Antonio Spurs RC
TP-13 Ace Bailey, Utah Jazz RC
TP-14 VJ Edgecombe, Philadelphia 76ers RC
TP-15 Tre Johnson III, Washington Wizards RC
TP-16 Derik Queen, New Orleans Pelicans RC
TP-17 Khaman Maluach, Phoenix Suns RC
TP-18 Walter Clayton Jr., Utah Jazz RC
TP-19 Nolan Traore, Brooklyn Nets RC
TP-20 Jeremiah Fears, New Orleans Pelicans RC
TP-21 Shaquille O'Neal, Los Angeles Lakers
TP-22 Dwyane Wade, Miami Heat
TP-23 Allen Iverson, Philadelphia 76ers
TP-24 David Robinson, San Antonio Spurs
TP-25 Hakeem Olajuwon, Houston Rockets
TP-26 Dominique Wilkins, Atlanta Hawks
TP-27 Kevin Garnett, Boston Celtics
TP-28 Carmelo Anthony, Denver Nuggets
TP-29 Vince Carter, Toronto Raptors
TP-30 Tracy McGrady, Toronto Raptors
"""

# ---------------------------------------------------------------------------
# Section definitions: (name, force_rookie, parallels, raw_data)
# ---------------------------------------------------------------------------
SECTIONS = [
    ("Base Set",                                False, BASE_PARS, BASE_RAW),
    ("Rookie 3 Patch Autographs Horizontal",    True,  FDI_PARS,  RPH_RAW),
    ("Rookie 3 Patch Autographs Vertical",      True,  FDI_PARS,  RPV_RAW),
    ("Relics Autographs Prime",                 True,  STD_PARS,  RAP_RAW),
    ("Rookie Relic Autographs",                 True,  STD_PARS,  RRA_RAW),
    ("Veteran 3 Patch Autographs",              False, STD_PARS,  V3A_RAW),
    ("Fresh Force Relic Autographs",            True,  STD_PARS,  FFR_RAW),
    ("Raindrops Signatures",                    False, STD_PARS,  RS_RAW),
    ("Serendipitous Sigs",                      False, STD_PARS,  SS_RAW),
    ("Re-Markable",                             False, STD_PARS,  RM_RAW),
    ("Full Court Signs",                        False, STD_PARS,  FS_RAW),
    ("Hit The Mark",                            False, STD_PARS,  HM_RAW),
    ("Triple Power Autographs",                 False, STD_PARS,  TPA_RAW),
    ("Rookie Autographs",                       True,  STD_PARS,  RA_RAW),
    ("Thunderdunk Signatures",                  False, STD_PARS,  TD_RAW),
    ("Rookie-Verse Signatures",                 True,  STD_PARS,  RV_RAW),
    ("Rim Reapers Signatures",                  False, HOLO_PARS, RR_RAW),
    ("Quest For Glory Autographs",              True,  HOLO_PARS, QG_RAW),
    ("City Drip Signatures",                    False, HOLO_PARS, CD_RAW),
    ("Next Feature Signatures",                 True,  STD_PARS,  NF_RAW),
    ("Game Time Graphs",                        False, STD_PARS,  GT_RAW),
    ("Ice Water",                               False, STD_PARS,  IW_RAW),
    ("Flight Path",                             False, STD_PARS,  FP_RAW),
    ("Architects",                              False, STD_PARS,  AR_RAW),
    ("3 And D",                                 False, RHP_PARS,  THREE_D_RAW),
    ("Monsters Of The Deep",                    False, RHP_PARS,  MD_RAW),
    ("The Paint",                               False, RHP_PARS,  PAINT_RAW),
]

# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def parse_code_line(line):
    """Parse 'CODE Player, Team RC' → (code, player, team, is_rookie)."""
    line = line.strip()
    if not line:
        return None
    parts = line.split(" ", 1)
    code = parts[0]
    rest = parts[1]
    is_rookie = rest.endswith(" RC")
    if is_rookie:
        rest = rest[:-3]
    comma = rest.rfind(", ")
    player = fix_name(rest[:comma])
    team = rest[comma + 2:]
    return code, player, team, is_rookie

def parse_base_line(line):
    """Parse 'N Player, Team RC' — also sets is_rookie for cards 61-100."""
    result = parse_code_line(line)
    if result is None:
        return None
    num, player, team, is_rookie = result
    # Cards 61-100 are rookies regardless of RC tag
    if num.isdigit() and int(num) >= 61:
        is_rookie = True
    return num, player, team, is_rookie

def parse_raw(raw, force_rookie=False, base_mode=False):
    """Parse a multiline block into list of (code, player, team, is_rookie)."""
    cards = []
    for line in raw.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        if base_mode:
            result = parse_base_line(line)
        else:
            result = parse_code_line(line)
        if result:
            code, player, team, is_rookie = result
            if force_rookie:
                is_rookie = True
            cards.append((code, player, team, is_rookie))
    return cards

# ---------------------------------------------------------------------------
# Main processing
# ---------------------------------------------------------------------------

# Pass 1: parse all non-TRA sections, build player→team lookup
sections_data = []  # (name, parallels, cards_list)
player_team_lookup = {}
rc_players = set()

for name, force_rookie, section_pars, raw in SECTIONS:
    base_mode = (name == "Base Set")
    cards = parse_raw(raw, force_rookie=force_rookie, base_mode=base_mode)
    sections_data.append((name, section_pars, cards))
    for _code, player, team, is_rookie in cards:
        player_team_lookup[player] = team
        if is_rookie:
            rc_players.add(player)

# Pass 2: parse Triple Relic Autographs
tra_cards = []
for line in TRA_RAW.strip().splitlines():
    line = line.strip()
    if not line:
        continue
    code_part, players_part = line.split(": ", 1)
    player_names = [fix_name(p) for p in players_part.split(" / ")]
    for player in player_names:
        team = player_team_lookup.get(player, TRA_TEAM_OVERRIDES.get(player, ""))
        is_rookie = player in rc_players
        tra_cards.append((code_part, player, team, is_rookie))

sections_data.append(("Triple Relic Autographs", TRA_PARS, tra_cards))

# Update player_team_lookup with TRA teams
for _code, player, team, is_rookie in tra_cards:
    if player not in player_team_lookup:
        player_team_lookup[player] = team
    if is_rookie:
        rc_players.add(player)

# ---------------------------------------------------------------------------
# RC propagation
# ---------------------------------------------------------------------------
for i, (name, section_pars, cards) in enumerate(sections_data):
    updated = []
    for code, player, team, is_rookie in cards:
        if player in rc_players:
            is_rookie = True
        updated.append((code, player, team, is_rookie))
    sections_data[i] = (name, section_pars, updated)

# ---------------------------------------------------------------------------
# Build sections and player entries for JSON
# ---------------------------------------------------------------------------

# sections for JSON
json_sections = []
for name, section_pars, cards in sections_data:
    json_cards = []
    for code, player, team, is_rookie in cards:
        json_cards.append({
            "card_number": code,
            "player": player,
            "team": team,
            "is_rookie": is_rookie,
            "subset": None,
        })
    json_sections.append({
        "insert_set": name,
        "parallels": section_pars,
        "cards": json_cards,
    })

# Player aggregation
player_appearances = defaultdict(list)  # player → list of appearances
player_insert_sets = defaultdict(set)

for name, section_pars, cards in sections_data:
    for code, player, team, is_rookie in cards:
        player_appearances[player].append({
            "insert_set": name,
            "card_number": code,
            "team": team,
            "is_rookie": is_rookie,
            "subset_tag": None,
            "parallels": [],
        })
        player_insert_sets[player].add(name)

json_players = []
for player in sorted(player_appearances.keys()):
    apps = player_appearances[player]
    json_players.append({
        "player": player,
        "appearances": apps,
        "stats": {
            "unique_cards": len(apps),
            "total_print_run": 0,
            "one_of_ones": 0,
            "insert_sets": len(player_insert_sets[player]),
        },
    })

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

output = {
    "set_name": SET_NAME,
    "sport": SPORT,
    "season": SEASON,
    "league": LEAGUE,
    "sections": json_sections,
    "players": json_players,
}

out_file = "topps_three_basketball_2526_parsed.json"
with open(out_file, "w") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

total_cards = sum(len(s["cards"]) for s in json_sections)
print(f"Written: {out_file}")
print(f"Sections:    {len(json_sections)}")
print(f"Total cards: {total_cards}")
print(f"Players:     {len(json_players)}")
