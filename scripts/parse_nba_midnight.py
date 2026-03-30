import json
import re

CHECKLIST_TEXT = """
2025-26 Topps Midnight Basketball

Base Set
100 cards
Parallels

Zodiac (1:2 packs)
Morning /149 (1:4)
Twilight /99 (1:6)
Dusk /75 (1:8)
Summer Solstice /50 (1:12)
Winter Solstice /35 (1:16)
Moon Beam (1:19)
Moonrise /25 (1:23)
Equinox /20 (1:28)
Midnight /12 (1:46)
Daybreak /5 (1:111)
Witching Hour /3 (1:184)
Black Light /1 (1:549)

1 Jayson Tatum, Boston Celtics
2 Jaylen Brown, Boston Celtics
3 Cam Thomas, Brooklyn Nets
4 Cameron Johnson, Brooklyn Nets
5 Scottie Barnes, Toronto Raptors
6 Gradey Dick, Toronto Raptors
7 Joel Embiid, Philadelphia 76ers
8 Tyrese Maxey, Philadelphia 76ers
9 Karl-Anthony Towns, New York Knicks
10 Jalen Brunson, New York Knicks
11 Josh Giddey, Chicago Bulls
12 Lonzo Ball, Chicago Bulls
13 Damian Lillard, Milwaukee Bucks
14 Giannis Antetokounmpo, Milwaukee Bucks
15 Tyrese Haliburton, Indiana Pacers
16 Pascal Siakam, Indiana Pacers
17 Cade Cunningham, Detroit Pistons
18 Ausar Thompson, Detroit Pistons
19 Donovan Mitchell, Cleveland Cavaliers
20 Evan Mobley, Cleveland Cavaliers
21 Trae Young, Atlanta Hawks
22 Zaccharie Risacher, Atlanta Hawks
23 Kawhi Leonard, Los Angeles Clippers
24 James Harden, Los Angeles Clippers
25 Jordan Poole, Washington Wizards
26 Alex Sarr, Washington Wizards
27 LaMelo Ball, Charlotte Hornets
28 Brandon Miller, Charlotte Hornets
29 Jimmy Butler III, Golden State Warriors
30 Stephen Curry, Golden State Warriors
31 Tyler Herro, Miami Heat
32 Kel'el Ware, Miami Heat
33 Franz Wagner, Orlando Magic
34 Paolo Banchero, Orlando Magic
35 Kevin Durant, Phoenix Suns
36 Devin Booker, Phoenix Suns
37 Zach Lavine, Sacramento Kings
38 Domantas Sabonis, Sacramento Kings
39 Austin Reaves, Los Angeles Lakers
40 LeBron James, Los Angeles Lakers
41 Victor Wembanyama, San Antonio Spurs
42 Stephon Castle, San Antonio Spurs
43 Ja Morant, Memphis Grizzlies
44 Desmond Bane, Memphis Grizzlies
45 Jalen Green, Houston Rockets
46 Amen Thompson, Houston Rockets
47 Anthony Davis, Dallas Mavericks
48 Kyrie Irving, Dallas Mavericks
49 Dejounte Murray, New Orleans Pelicans
50 CJ McCollum, New Orleans Pelicans
51 Walker Kessler, Utah Jazz
52 Collin Sexton, Utah Jazz
53 Scoot Henderson, Portland Trail Blazers
54 Anfernee Simons, Portland Trail Blazers
55 Chet Holmgren, Oklahoma City Thunder
56 Shai Gilgeous-Alexander, Oklahoma City Thunder
57 Julius Randle, Minnesota Timberwolves
58 Anthony Edwards, Minnesota Timberwolves
59 Jamal Murray, Denver Nuggets
60 Nikola Jokić, Denver Nuggets
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
92 Adou Thiero, Los Angeles Lakers RC
93 Noah Penda, Orlando Magic RC
94 Ryan Kalkbrenner, Charlotte Hornets RC
95 Johni Broome, Philadelphia 76ers RC
96 Alijah Martin, Toronto Raptors RC
97 Maxime Raynaud, Sacramento Kings RC
98 Tyrese Proctor, Cleveland Cavaliers RC
99 Kam Jones, Indiana Pacers RC
100 Chaz Lanier, Detroit Pistons RC

Autographs
Rookie Jersey Autographs
35 cards
1:5 packs
Parallels

Twilight /199 (1:8 packs)
Dusk /75 (1:21)
Summer Solstice /50 (1:31)
Winter Solstice /35 (1:44)
Moon Beam (1:56)
Moonrise /25 (1:62)
Equinox /20 (1:77)
Midnight /12 (1:128)
Daybreak /5 (1:309)
Witching Hour /3 (1:519)
Black Light /1 (1:1,527)

RJA-AB Ace Bailey, Utah Jazz
RJA-AM Alijah Martin, Toronto Raptors
RJA-AN Asa Newell, Atlanta Hawks
RJA-AT Adou Thiero, Los Angeles Lakers
RJA-BB Brooks Barnhizer, Oklahoma City Thunder
RJA-BS Ben Saraf, Brooklyn Nets
RJA-CC Cedric Coward, Memphis Grizzlies
RJA-CF Cooper Flagg, Dallas Mavericks
RJA-CM Collin Murray-Boyles, Toronto Raptors
RJA-DH Dylan Harper, San Antonio Spurs
RJA-DP Drake Powell, Brooklyn Nets
RJA-DQ Derik Queen, New Orleans Pelicans
RJA-DW Danny Wolf, Brooklyn Nets
RJA-ED Egor Dëmin, Brooklyn Nets
RJA-JB Joan Beringer, Minnesota Timberwolves
RJA-JBR Johni Broome, Philadelphia 76ers
RJA-JR Jase Richardson, Orlando Magic
RJA-KJ Kasparas Jakučionis, Miami Heat
RJA-KJO Kam Jones, Indiana Pacers
RJA-KK Kon Knueppel, Charlotte Hornets
RJA-KM Khaman Maluach, Phoenix Suns
RJA-LM Liam McNeeley, Charlotte Hornets
RJA-MR Maxime Raynaud, Sacramento Kings
RJA-NC Nique Clifford, Sacramento Kings
RJA-NE Noa Essengue, Chicago Bulls
RJA-NP Noah Penda, Orlando Magic
RJA-NT Nolan Traore, Brooklyn Nets
RJA-RF Rasheer Fleming, Phoenix Suns
RJA-RK Ryan Kalkbrenner, Charlotte Hornets
RJA-TP Tyrese Proctor, Cleveland Cavaliers
RJA-TS Thomas Sorber, Oklahoma City Thunder
RJA-WC Walter Clayton Jr., Utah Jazz
RJA-WR Will Riley, Washington Wizards
RJA-YH Yang Hansen, Portland Trail Blazers
RJA-YK Yanic Konan-Niederhäuser, Los Angeles Clippers

Stroke Of Midnight Autographs
41 cards
1:4 packs
Parallels

Twilight /199 (1:9 packs)
Dusk /75 (1:21)
Summer Solstice /50 (1:27)
Moon Beam (1:34)
Winter Solstice /35 (1:38)
Moonrise /25 (1:53)
Equinox /20 (1:66)
Midnight /12 (1:109)
Daybreak /5 (1:261)
Witching Hour /3 (1:435)
Black Light /1 (1:1,304)

SM-AB Adem Bona, Philadelphia 76ers
SM-AD Ayo Dosunmu, Chicago Bulls
SM-AE Alex English, Denver Nuggets
SM-AM Ajay Mitchell, Oklahoma City Thunder
SM-AN Aaron Nesmith, Indiana Pacers
SM-AR Antonio Reeves, New Orleans Pelicans
SM-BM Brandon Miller, Charlotte Hornets
SM-BS Ben Sheppard, Indiana Pacers
SM-CC Cam Christie, Los Angeles Clippers
SM-CM Calvin Murphy, Houston Rockets
SM-CS Cam Spencer, Memphis Grizzlies
SM-DG Daniel Gafford, Dallas Mavericks
SM-DH DaRon Holmes II, Denver Nuggets
SM-DS Day'ron Sharpe, Brooklyn Nets
SM-DW Dominique Wilkins, Atlanta Hawks
SM-FW Franz Wagner, Orlando Magic
SM-GG George Gervin, San Antonio Spurs
SM-HI Harrison Ingram, San Antonio Spurs
SM-JH Josh Hart, New York Knicks
SM-JL Jake LaRavia, Sacramento Kings
SM-JOW Jordan Walsh, Boston Celtics
SM-JP Jalen Pickett, Denver Nuggets
SM-JS Jamal Shead, Toronto Raptors
SM-JW Jalen Wilson, Brooklyn Nets
SM-JWE Jaylen Wells, Memphis Grizzlies
SM-KH Kevin Huerter, Chicago Bulls
SM-MC Maurice Cheeks, Philadelphia 76ers
SM-MS Marcus Sasser, Detroit Pistons
SM-OI Oso Ighodaro, Phoenix Suns
SM-PL Pelle Larsson, Miami Heat
SM-PP Payton Pritchard, Boston Celtics
SM-PS Pascal Siakam, Indiana Pacers
SM-QP Quinten Post, Golden State Warriors
SM-RJ Reggie Jackson, Philadelphia 76ers
SM-RJE Richard Jefferson, New Jersey Nets
SM-RW Rasheed Wallace, Detroit Pistons
SM-TH Tim Hardaway, Miami Heat
SM-TK Tyler Kolek, New York Knicks
SM-TN Tristen Newton, Minnesota Timberwolves
SM-TS Tristan da Silva, Orlando Magic
SM-ZC Zach Collins, Chicago Bulls

Stroke Of Midnight Rookie Autographs
21 cards
1:8 packs
Parallels

Twilight /199 (1:8 packs)
Dusk /75 (1:21)
Summer Solstice /50 (1:31)
Winter Solstice /35 (1:44)
Moon Beam (1:56)
Moonrise /25 (1:62)
Equinox /20 (1:77)
Midnight /12 (1:128)
Daybreak /5 (1:309)
Witching Hour /3 (1:519)
Black Light /1 (1:1,527)

SMR-AN Asa Newell, Atlanta Hawks
SMR-AT Adou Thiero, Los Angeles Lakers
SMR-BB Brooks Barnhizer, Oklahoma City Thunder
SMR-BS Ben Saraf, Brooklyn Nets
SMR-CC Cedric Coward, Memphis Grizzlies
SMR-CL Chaz Lanier, Detroit Pistons
SMR-DH Dylan Harper, San Antonio Spurs
SMR-DP Drake Powell, Brooklyn Nets
SMR-DW Danny Wolf, Brooklyn Nets
SMR-JB Joan Beringer, Minnesota Timberwolves
SMR-JBR Johni Broome, Philadelphia 76ers
SMR-JR Jase Richardson, Orlando Magic
SMR-KB Koby Brea, Phoenix Suns
SMR-KJ Kam Jones, Indiana Pacers
SMR-KM Khaman Maluach, Phoenix Suns
SMR-LM Liam McNeeley, Charlotte Hornets
SMR-MP Micah Peavy, New Orleans Pelicans
SMR-RK Ryan Kalkbrenner, Charlotte Hornets
SMR-SJ Sion James, Charlotte Hornets
SMR-WC Walter Clayton Jr., Utah Jazz
SMR-WR Will Riley, Washington Wizards

Rookie Horizon Signatures
40 cards
1:5 packs
Parallels

Dusk /75 (1:18 packs)
Summer Solstice /50 (1:27)
Moon Beam (1:34)
Winter Solstice /35 (1:39)
Moonrise /25 (1:54)
Equinox /20 (1:68)
Midnight /12 (1:112)
Daybreak /5 (1:268)
Witching Hour /3 (1:450)
Black Light /1 (1:1,337)

RHS-AB Ace Bailey, Utah Jazz
RHS-AM Alijah Martin, Toronto Raptors
RHS-AN Asa Newell, Atlanta Hawks
RHS-AT Adou Thiero, Los Angeles Lakers
RHS-BB Brooks Barnhizer, Oklahoma City Thunder
RHS-BS Ben Saraf, Brooklyn Nets
RHS-CC Cedric Coward, Memphis Grizzlies
RHS-CF Cooper Flagg, Dallas Mavericks
RHS-CL Chaz Lanier, Detroit Pistons
RHS-CM Collin Murray-Boyles, Toronto Raptors
RHS-DH Dylan Harper, San Antonio Spurs
RHS-DP Drake Powell, Brooklyn Nets
RHS-DQ Derik Queen, New Orleans Pelicans
RHS-DW Danny Wolf, Brooklyn Nets
RHS-ED Egor Dëmin, Brooklyn Nets
RHS-JB Joan Beringer, Minnesota Timberwolves
RHS-JBR Johni Broome, Philadelphia 76ers
RHS-JR Jase Richardson, Orlando Magic
RHS-JW Jamir Watkins, Washington Wizards
RHS-KB Koby Brea, Phoenix Suns
RHS-KJ Kasparas Jakučionis, Miami Heat
RHS-KJO Kam Jones, Indiana Pacers
RHS-KK Kon Knueppel, Charlotte Hornets
RHS-KM Khaman Maluach, Phoenix Suns
RHS-LM Liam McNeeley, Charlotte Hornets
RHS-MP Micah Peavy, New Orleans Pelicans
RHS-MR Maxime Raynaud, Sacramento Kings
RHS-NC Nique Clifford, Sacramento Kings
RHS-NE Noa Essengue, Chicago Bulls
RHS-NP Noah Penda, Orlando Magic
RHS-NT Nolan Traore, Brooklyn Nets
RHS-RF Rasheer Fleming, Phoenix Suns
RHS-RK Ryan Kalkbrenner, Charlotte Hornets
RHS-SJ Sion James, Charlotte Hornets
RHS-TP Tyrese Proctor, Cleveland Cavaliers
RHS-TS Thomas Sorber, Oklahoma City Thunder
RHS-WC Walter Clayton Jr., Utah Jazz
RHS-WR Will Riley, Washington Wizards
RHS-YH Yang Hansen, Portland Trail Blazers
RHS-YK Yanic Konan-Niederhäuser, Los Angeles Clippers

Midnight Sun Signatures
39 cards
1:27 packs
Parallels

Winter Solstice /35 (1:59 packs)
Moonrise /25 (1:77)*
Equinox /20 (1:69)*
Midnight /12 (1:115)
Moon Beam (1:191)*
Daybreak /5 (1:275)
Witching Hour /3 (1:457)
Black Light /1 (1:1,371)
*Odds as provided by Topps

MS-AG Aaron Gordon, Denver Nuggets
MS-AH Anfernee Hardaway, Orlando Magic
MS-AS Alex Sarr, Washington Wizards
MS-AW Andrew Wiggins, Miami Heat
MS-BJ Bronny James, Los Angeles Lakers
MS-CA Carmelo Anthony, New York Knicks
MS-CH Chet Holmgren, Oklahoma City Thunder
MS-CM CJ McCollum, Washington Wizards
MS-DB Desmond Bane, Memphis Grizzlies
MS-DF De'Aaron Fox, San Antonio Spurs
MS-DL Dereck Lively II, Dallas Mavericks
MS-DR David Robinson, San Antonio Spurs
MS-DRO Dennis Rodman, Chicago Bulls
MS-DW Dwyane Wade, Miami Heat
MS-FV Fred VanVleet, Houston Rockets
MS-GD Gradey Dick, Toronto Raptors
MS-IC Isaiah Collier, Utah Jazz
MS-JB Jalen Brunson, New York Knicks
MS-JG Jalen Green, Houston Rockets
MS-JK Jason Kidd, New Jersey Nets
MS-JT Jayson Tatum, Boston Celtics
MS-KD Kevin Durant, Phoenix Suns
MS-KG Kevin Garnett, Boston Celtics
MS-KP Kristaps Porzingis, Boston Celtics
MS-LB Larry Bird, Boston Celtics
MS-LJ LeBron James, Los Angeles Lakers
MS-MB Mikal Bridges, New York Knicks
MS-MJ Magic Johnson, Los Angeles Lakers
MS-MP Michael Porter Jr., Denver Nuggets
MS-NT Nikola Topić, Oklahoma City Thunder
MS-OA OG Anunoby, New York Knicks
MS-RD Rob Dillingham, Minnesota Timberwolves
MS-RG Rudy Gobert, Minnesota Timberwolves
MS-SO Shaquille O'Neal, Los Angeles Lakers
MS-TH Tyler Herro, Miami Heat
MS-THA Tyrese Haliburton, Indiana Pacers
MS-VC Vince Carter, Toronto Raptors
MS-VW Victor Wembanyama, San Antonio Spurs
MS-ZE Zach Edey, Memphis Grizzlies

Midnight Sun Rookie Signatures
20 cards
1:9 packs
Parallels

Twilight /199 (1:16 packs)
Dusk /75 (1:38)
Summer Solstice /50 (1:57)
Moon Beam (1:71)
Winter Solstice /35 (1:81)
Moonrise /25 (1:107)
Equinox /20 (1:134)
Midnight /12 (1:224)
Daybreak /5 (1:535)
Witching Hour /3 (1:891)
Black Light /1 (1:2,673)

MSR-AM Alijah Martin, Toronto Raptors
MSR-BS Ben Saraf, Brooklyn Nets
MSR-CC Cedric Coward, Memphis Grizzlies
MSR-DQ Derik Queen, New Orleans Pelicans
MSR-ED Egor Dëmin, Brooklyn Nets
MSR-JB Joan Beringer, Minnesota Timberwolves
MSR-JW Jamir Watkins, Washington Wizards
MSR-KB Koby Brea, Phoenix Suns
MSR-KJ Kasparas Jakučionis, Miami Heat
MSR-KJO Kam Jones, Indiana Pacers
MSR-KM Khaman Maluach, Phoenix Suns
MSR-MP Micah Peavy, New Orleans Pelicans
MSR-MR Maxime Raynaud, Sacramento Kings
MSR-NE Noa Essengue, Chicago Bulls
MSR-NP Noah Penda, Orlando Magic
MSR-NT Nolan Traore, Brooklyn Nets
MSR-RF Rasheer Fleming, Phoenix Suns
MSR-SJ Sion James, Charlotte Hornets
MSR-TS Thomas Sorber, Oklahoma City Thunder
MSR-YH Yang Hansen, Portland Trail Blazers

Dark Marks
24 cards
1:9 packs
Parallels

Dusk /75 (1:40 packs)
Summer Solstice /50 (1:57)
Winter Solstice /35 (1:73)
Moonrise /25 (1:90)
Moon Beam (1:99)
Equinox /20 (1:112)
Midnight /12 (1:186)
Daybreak /5 (1:446)
Witching Hour /3 (1:743)
Black Light /1 (1:2,227)

DM-CD Clyde Drexler, Portland Trail Blazers
DM-CJ Colby Jones, Washington Wizards
DM-CL Christian Laettner, Minnesota Timberwolves
DM-DH De'Andre Hunter, Cleveland Cavaliers
DM-DM Donovan Mitchell, Cleveland Cavaliers
DM-DS Domantas Sabonis, Sacramento Kings
DM-DW Deron Williams, Brooklyn Nets
DM-EG Eric Gordon, Philadelphia 76ers
DM-IH Isaiah Hartenstein, Oklahoma City Thunder
DM-IS Isaiah Stewart, Detroit Pistons
DM-JH Juwan Howard, Washington Bullets
DM-JHO Jett Howard, Orlando Magic
DM-JS John Stockton, Utah Jazz
DM-JT Jae'Sean Tate, Houston Rockets
DM-JV Jarred Vanderbilt, Los Angeles Lakers
DM-KG Kyshawn George, Washington Wizards
DM-MS Max Strus, Cleveland Cavaliers
DM-PP Paul Pierce, Boston Celtics
DM-QG Quentin Grimes, Philadelphia 76ers
DM-RA Ray Allen, Seattle Supersonics
DM-RH Ron Holland II, Detroit Pistons
DM-TM Tracy McGrady, Toronto Raptors
DM-TP Tony Parker, San Antonio Spurs
DM-TS Terrence Shannon Jr., Minnesota Timberwolves

Dark Marks Rookies
10 cards
1:23 packs
Parallels

Twilight /199 (1:20 packs)
Dusk /75 (1:121)*
Summer Solstice /50 (1:121)*
Winter Solstice /35 (1:170)
Moonrise /25 (1:217)
Moon Beam (1:223)
Equinox /20 (1:269)
Midnight /12 (1:446)
Daybreak /5 (1:1,069)
Witching Hour /3 (1:1,782)
Black Light /1 (1:5,345)
*Odds as provided by Topps

DMR-BB Brooks Barnhizer, Oklahoma City Thunder
DMR-CF Cooper Flagg, Dallas Mavericks
DMR-CL Chaz Lanier, Detroit Pistons
DMR-CM Collin Murray-Boyles, Toronto Raptors
DMR-DP Drake Powell, Brooklyn Nets
DMR-JW Jamir Watkins, Washington Wizards
DMR-KJ Kasparas Jakučionis, Miami Heat
DMR-NE Noa Essengue, Chicago Bulls
DMR-NT Nolan Traore, Brooklyn Nets
DMR-TP Tyrese Proctor, Cleveland Cavaliers

Dark Matter Autographs
22 cards
1:17 packs
Parallels

Dusk /75 (1:42 packs)
Summer Solstice /50 (1:57)
Winter Solstice /35 (1:81)
Moonrise /25 (1:107)
Equinox /20 (1:128)
Moon Beam (1:143)
Midnight /12 (1:203)
Daybreak /5 (1:486)
Witching Hour /3 (1:810)
Black Light /1 (1:2,430)

DMA-AI Allen Iverson, Philadelphia 76ers
DMA-BBO Bogdan Bogdanović, Los Angeles Clippers
DMA-BH Bones Hyland, Minnesota Tmberwolves
DMA-CA Cole Anthony, Orlando Magic
DMA-CB Christian Braun, Denver Nuggets
DMA-DB Dillon Brooks, Houston Rockets
DMA-DT David Thompson, Denver Nuggets
DMA-GW Grant Williams, Charlotte Hornets
DMA-JJ Jaren Jackson Jr., Memphis Grizzlies
DMA-JJJ Jaime Jaquez Jr., Miami Heat
DMA-JM Jamal Murray, Denver Nuggets
DMA-JT Jaylon Tyson, Cleveland Cavaliers
DMA-LS Latrell Sprewell, Golden State Warriors
DMA-NB Nicolas Batum, Los Angeles Clippers
DMA-NV Nikola Vučević, Chicago Bulls
DMA-OO Onyeka Okongwu, Atlanta Hawks
DMA-RP Robert Parish, Boston Celtics
DMA-SB Saddiq Bey, Washington Wizards
DMA-SC Stephen Curry, Golden State Warriors
DMA-SCA Stephon Castle, San Antonio Spurs
DMA-SH Scoot Henderson, Portland Trail Blazers
DMA-TS Tyler Smith, Milwaukee Bucks

Dark Matter Rookie Autographs
10 cards
1:21 packs
Parallels

Twilight /199 (1:75 packs)
Dusk /75 (1:80)
Summer Solstice /50 (1:120)
Winter Solstice /35 (1:154)
Moon Beam (1:210)
Moonrise /25 (1:215)
Equinox /20 (1:268)
Midnight /12 (1:450)
Daybreak /5 (1:1,069)
Witching Hour /3 (1:1,782)
Black Light /1 (1:5,345)

DMAR-AB Ace Bailey, Utah Jazz
DMAR-DQ Derik Queen, New Orleans Pelicans
DMAR-JB Joan Beringer, Minnesota Timberwolves
DMAR-JW Jamir Watkins, Washington Wizards
DMAR-LM Liam McNeeley, Charlotte Hornets
DMAR-NC Nique Clifford, Sacramento Kings
DMAR-TS Thomas Sorber, Oklahoma City Thunder
DMAR-WR Will Riley, Washington Wizards
DMAR-YH Yang Hansen, Portland Trail Blazers
DMAR-YK Yanic Konan-Niederhäuser, Los Angeles Clippers

Midnight Oil Marks
24 cards
1:15 packs
Parallels

Dusk /75 (1:45)
Summer Solstice /50 (1:57)
Winter Solstice /35 (1:77)
Moon Beam (1:90)
Moonrise /25 (1:90)
Equinox /20 (1:112)
Midnight /12 (1:186)
Daybreak /5 (1:446)
Witching Hour /3 (1:743)
Black Light /1 (1:2,227)

MO-AM Alonzo Mourning, Miami Heat
MO-AS Anfernee Simons, Portland Trail Blazers
MO-BC Brandon Clarke, Memphis Grizzlies
MO-DD Donte Divincenzo, Minnesota Timberwolves
MO-DG Devonte' Graham, Portland Trail Blazers
MO-DN Dirk Nowitzki, Dallas Mavericks
MO-DW Derrick White, Boston Celtics
MO-HO Hakeem Olajuwon, Houston Rockets
MO-JF Johnny Furphy, Indiana Pacers
MO-JH James Harden, Los Angeles Clippers
MO-JM Jonathan Mogbo, Toronto Raptors
MO-JP Jakob Poeltl, Toronto Raptors
MO-JV Jonas Valančiūnas, Sacramento Kings
MO-KM Kevin McCullar Jr., New York Knicks
MO-KT Karl-Anthony Towns, New York Knicks
MO-MW Metta World Peace, Los Angeles Lakers
MO-NC Nic Claxton, Brooklyn Nets
MO-NR Naz Reid, Minnesota Timberwolves
MO-NT Nikola Topić, Oklahoma City Thunder
MO-PA Precious Achiuwa, New York Knicks
MO-RH Rip Hamilton, Detroit Pistons
MO-SGA Shai Gilgeous-Alexander, Oklahoma City Thunder
MO-WK Walker Kessler, Utah Jazz
MO-ZR Zaccharie Risacher, Atlanta Hawks

Midnight Oil Marks – Rookies
5 cards
1:54 packs
Parallels

Twilight /199 (1:158 packs)
Dusk /75 (1:180)
Summer Solstice /50 (1:268)
Winter Solstice /35 (1:309)
Moon Beam (1:357)
Moonrise /25 (1:428)
Equinox /20 (1:540)
Midnight /12 (1:891)
Daybreak /5 (1:2,227)
Witching Hour /3 (1:3,818)
Black Light /1 (1:10,689)

MOR-JR Jase Richardson, Orlando Magic
MOR-KJ Kasparas Jakučionis, Miami Heat
MOR-KK Kon Knueppel, Charlotte Hornets
MOR-NE Noa Essengue, Chicago Bulls
MOR-TP Tyrese Proctor, Cleveland Cavaliers

Stroke Of Midnight Autographs II
2 cards

SM-GAN Giannis Antetokounmpo, Milwaukee Bucks
SM-NJ Nikola Jokić, Denver Nuggets

Inserts
Night Owls
25 cards
1:8 packs
Parallels

Morning /149 (1:15 packs)
Twilight /99 (1:23)
Dusk /75 (1:30)
Summer Solstice /50 (1:45)
Winter Solstice /35 (1:63)
Moon Beam (1:74)
Moonrise /25 (1:89)
Equinox /20 (1:111)
Midnight /12 (1:184)
Daybreak /5 (1:439)
Witching Hour /3 (1:732)
Black Light /1 (1:2,194)

NO-1 LeBron James, Los Angeles Lakers
NO-2 Anthony Davis, Dallas Mavericks
NO-3 Anthony Edwards, Minnesota Timberwolves
NO-4 Shai Gilgeous-Alexander, Oklahoma City Thunder
NO-5 Paolo Banchero, Orlando Magic
NO-6 Kevin Durant, Phoenix Suns
NO-7 Stephen Curry, Golden State Warriors
NO-8 Jayson Tatum, Boston Celtics
NO-9 Trae Young, Atlanta Hawks
NO-10 Jalen Brunson, New York Knicks
NO-11 Ja Morant, Memphis Grizzlies
NO-12 Amen Thompson, Houston Rockets
NO-13 Giannis Antetokounmpo, Milwaukee Bucks
NO-14 Shaquille O'Neal, Los Angeles Lakers
NO-15 Dwyane Wade, Miami Heat
NO-16 Cooper Flagg, Dallas Mavericks
NO-17 Dylan Harper, San Antonio Spurs
NO-18 VJ Edgecombe, Philadelphia 76ers
NO-19 Kon Knueppel, Charlotte Hornets
NO-20 Ace Bailey, Utah Jazz
NO-21 Tre Johnson III, Washington Wizards
NO-22 Jeremiah Fears, New Orleans Pelicans
NO-23 Khaman Maluach, Phoenix Suns
NO-24 Walter Clayton Jr., Utah Jazz
NO-25 Asa Newell, Atlanta Hawks

Daydreamers
20 cards
1:10 packs
Parallels

Morning /149 (1:19 packs)
Twilight /99 (1:28)
Dusk /75 (1:37)
Summer Solstice /50 (1:56)
Winter Solstice /35 (1:79)
Moon Beam (1:92)
Moonrise /25 (1:111)
Equinox /20 (1:138)
Midnight /12 (1:229)
Daybreak /5 (1:549)
Witching Hour /3 (1:908)
Black Light /1 (1:2,632)

DD-1 Cade Cunningham, Detroit Pistons
DD-2 Karl Anthony-Towns, New York Knicks
DD-3 Jaylen Brown, Boston Celtics
DD-4 Donovan Mitchell, Cleveland Cavaliers
DD-5 LaMelo Ball, Charlotte Hornets
DD-6 Devin Booker, Phoenix Suns
DD-7 Kawhi Leonard, Los Angeles Clippers
DD-8 James Harden, Los Angeles Clippers
DD-9 Jalen Green, Houston Rockets
DD-10 Victor Wembanyama, San Antonio Spurs
DD-11 Kyrie Irving, Dallas Mavericks
DD-12 Damian Lillard, Milwaukee Bucks
DD-13 Joel Embiid, Philadelphia 76ers
DD-14 Larry Bird, Boston Celtics
DD-15 Dirk Nowitzki, Dallas Mavericks
DD-16 Cooper Flagg, Dallas Mavericks
DD-17 Dylan Harper, San Antonio Spurs
DD-18 Kon Knueppel, Charlotte Hornets
DD-19 Egor Dëmin, Brooklyn Nets
DD-20 Noa Essengue, Chicago Bulls

Insomnia
25 cards
1:8 packs
Parallels

Morning /149 (1:15 packs)
Twilight /99 (1:23)
Dusk /75 (1:30)
Summer Solstice /50 (1:45)
Winter Solstice /35 (1:63)
Moon Beam (1:74)
Moonrise /25 (1:89)
Equinox /20 (1:111)
Midnight /12 (1:184)
Daybreak /5 (1:439)
Witching Hour /3 (1:732)
Black Light /1 (1:2,194)

IN-1 Stephon Castle, San Antonio Spurs
IN-2 Devin Booker, Phoenix Suns
IN-3 LaMelo Ball, Charlotte Hornets
IN-4 Cade Cunningham, Detroit Pistons
IN-5 Jalen Brunson, New York Knicks
IN-6 LeBron James, Los Angeles Lakers
IN-7 Tyrese Haliburton, Indiana Pacers
IN-8 Tyler Herro, Miami Heat
IN-9 Jayson Tatum, Boston Celtics
IN-10 Jalen Williams, Oklahoma City Thunder
IN-11 Magic Johnson, Los Angeles Lakers
IN-12 Tracy McGrady, Toronto Raptors
IN-13 Kevin Garnett, Boston Celtics
IN-14 Dwyane Wade, Miami Heat
IN-15 Vince Carter, Toronto Raptors
IN-16 Cooper Flagg, Dallas Mavericks
IN-17 Dylan Harper, San Antonio Spurs
IN-18 Collin Murray-Boyles, Toronto Raptors
IN-19 Cedric Coward, Memphis Grizzlies
IN-20 Carter Bryant, San Antonio Spurs
IN-21 Kasparas Jakučionis, Miami Heat
IN-22 Jase Richardson, Orlando Magic
IN-23 Danny Wolf, Brooklyn Nets
IN-24 Liam McNeeley, Charlotte Hornets
IN-25 Yang Hansen, Portland Trail Blazers

Moonfall
30 cards
1:7 packs
Parallels

Morning /149 (1:13 packs)
Twilight /99 (1:19)
Dusk /75 (1:25)
Summer Solstice /50 (1:37)
Winter Solstice /35 (1:53)
Moon Beam (1:62)
Moonrise /25 (1:74)
Equinox /20 (1:92)
Midnight /12 (1:154)
Daybreak /5 (1:366)
Witching Hour /3 (1:613)
Black Light /1 (1:1,816)

MF-1 Anthony Edwards, Minnesota Timberwolves
MF-2 Paul George, Philadelphia 76ers
MF-3 James Harden, Los Angeles Clippers
MF-4 Stephen Curry, Golden State Warriors
MF-5 Giannis Antetokounmpo, Milwaukee Bucks
MF-6 Nikola Jokić, Denver Nuggets
MF-7 Paolo Banchero, Orlando Magic
MF-8 Donovan Mitchell, Cleveland Cavaliers
MF-9 Jaylen Brown, Boston Celtics
MF-10 Ja Morant, Memphis Grizzlies
MF-11 Anthony Davis, Dallas Mavericks
MF-12 Austin Reaves, Los Angeles Lakers
MF-13 LaMelo Ball, Charlotte Hornets
MF-14 Tyrese Haliburton, Indiana Pacers
MF-15 Jalen Brunson, New York Knicks
MF-16 Dennis Rodman, Chicago Bulls
MF-17 Paul Pierce, Boston Celtics
MF-18 Ray Allen, Miami Heat
MF-19 Allen Iverson, Philadelphia 76ers
MF-20 Ben Wallace, Detroit Pistons
MF-21 Cooper Flagg, Dallas Mavericks
MF-22 Dylan Harper, San Antonio Spurs
MF-23 Derik Queen, New Orleans Pelicans
MF-24 Drake Powell, Brooklyn Nets
MF-25 Thomas Sorber, Oklahoma City Thunder
MF-26 Nolan Traore, Brooklyn Nets
MF-27 Nique Clifford, Sacramento Kings
MF-28 Ben Saraf, Brooklyn Nets
MF-29 Hugo González, Boston Celtics
MF-30 Yanic Konan-Niederhäuser, Los Angeles Clippers

Night Shade
30 cards
1:28 packs
Parallel

Black Light /1 (1:1,816 packs)

NS-1 Trae Young, Atlanta Hawks
NS-2 Paolo Banchero, Orlando Magic
NS-3 Jayson Tatum, Boston Celtics
NS-4 Donovan Mitchell, Cleveland Cavaliers
NS-5 Jalen Brunson, New York Knicks
NS-6 Cade Cunningham, Detroit Pistons
NS-7 Tyrese Haliburton, Indiana Pacers
NS-8 Kevin Durant, Phoenix Suns
NS-9 Kawhi Leonard, Los Angeles Clippers
NS-10 Giannis Antetokounmpo, Milwaukee Bucks
NS-11 Anthony Davis, Dallas Mavericks
NS-12 LeBron James, Los Angeles Lakers
NS-13 Anthony Edwards, Minnesota Timberwolves
NS-14 Shai Gilgeous-Alexander, Oklahoma City Thunder
NS-15 Nikola Jokić, Denver Nuggets
NS-16 Hakeem Olajuwon, Houston Rockets
NS-17 Tracy McGrady, Orlando Magic
NS-18 Tim Duncan, San Antonio Spurs
NS-19 John Stockton, Utah Jazz
NS-20 Patrick Ewing, New York Knicks
NS-21 Cooper Flagg, Dallas Mavericks
NS-22 Dylan Harper, San Antonio Spurs
NS-23 VJ Edgecombe, Philadelphia 76ers
NS-24 Kon Knueppel, Charlotte Hornets
NS-25 Ace Bailey, Utah Jazz
NS-26 Tre Johnson III, Washington Wizards
NS-27 Jeremiah Fears, New Orleans Pelicans
NS-28 Egor Dëmin, Brooklyn Nets
NS-29 Walter Clayton Jr., Utah Jazz
NS-30 Asa Newell, Atlanta Hawks

Dreamland
30 cards
1:28 packs
Parallel

Black Light /1 (1:1,816 packs)

DL-1 LeBron James, Los Angeles Lakers
DL-2 Kevin Durant, Phoenix Suns
DL-3 LaMelo Ball, Charlotte Hornets
DL-4 Kyrie Irving, Dallas Mavericks
DL-5 Tyrese Haliburton, Indiana Pacers
DL-6 Victor Wembanyama, San Antonio Spurs
DL-7 Stephen Curry, Golden State Warriors
DL-8 Paolo Banchero, Orlando Magic
DL-9 Anthony Edwards, Minnesota Timberwolves
DL-10 Magic Johnson, Los Angeles Lakers
DL-11 Dirk Nowitzki, Dallas Mavericks
DL-12 Ray Allen, Seattle Supersonics
DL-13 Allen Iverson, Philadelphia 76ers
DL-14 Vince Carter, Toronto Raptors
DL-15 Dennis Rodman, Chicago Bulls
DL-16 Cooper Flagg, Dallas Mavericks
DL-17 Dylan Harper, San Antonio Spurs
DL-18 VJ Edgecombe, Philadelphia 76ers
DL-19 Kon Knueppel, Charlotte Hornets
DL-20 Ace Bailey, Utah Jazz
DL-21 Tre Johnson III, Washington Wizards
DL-22 Jeremiah Fears, New Orleans Pelicans
DL-23 Khaman Maluach, Phoenix Suns
DL-24 Kasparas Jakučionis, Miami Heat
DL-25 Collin Murray-Boyles, Toronto Raptors
DL-26 Nolan Traore, Brooklyn Nets
DL-27 Jase Richardson, Orlando Magic
DL-28 Danny Wolf, Brooklyn Nets
DL-29 Liam McNeeley, Charlotte Hornets
DL-30 Yang Hansen, Portland Trail Blazers

Night Vision
25 cards
1:33 packs
Parallel

Black Light /1 (1:2,194 packs)

NV-1 Stephen Curry, Golden State Warriors
NV-2 Kawhi Leonard, Los Angeles Clippers
NV-3 Shai Gilgeous-Alexander, Oklahoma City Thunder
NV-4 Anthony Edwards, Minnesota Timberwolves
NV-5 Kyrie Irving, Dallas Mavericks
NV-6 Victor Wembanyama, San Antonio Spurs
NV-7 Jayson Tatum, Boston Celtics
NV-8 LaMelo Ball, Charlotte Hornets
NV-9 James Harden, Los Angeles Clippers
NV-10 Cade Cunningham, Detroit Pistons
NV-11 Giannis Antetokounmpo, Milwaukee Bucks
NV-12 Trae Young, Atlanta Hawks
NV-13 Paolo Banchero, Orlando Magic
NV-14 Ja Morant, Memphis Grizzlies
NV-15 Tyrese Haliburton, Indiana Pacers
NV-16 Jalen Brunson, New York Knicks
NV-17 Nikola Jokić, Denver Nuggets
NV-18 Kevin Durant, Phoenix Suns
NV-19 Donovan Mitchell, Cleveland Cavaliers
NV-20 Jalen Green, Houston Rockets
NV-21 Kevin Garnett, Boston Celtics
NV-22 Dwyane Wade, Miami Heat
NV-23 Shaquille O'Neal, Los Angeles Lakers
NV-24 Larry Bird, Boston Celtics
NV-25 Magic Johnson, Los Angeles Lakers

Twilight
15 cards
1:54 packs

TL-1 LeBron James, Los Angeles Lakers
TL-2 Stephen Curry, Golden State Warriors
TL-3 Anthony Edwards, Minnesota Timberwolves
TL-4 Nikola Jokić, Denver Nuggets
TL-5 Shai Gilgeous-Alexander, Oklahoma City Thunder
TL-6 Tyrese Haliburton, Indiana Pacers
TL-7 Victor Wembanyama, San Antonio Spurs
TL-8 Kevin Durant, Phoenix Suns
TL-9 Jayson Tatum, Boston Celtics
TL-10 Giannis Antetokounmpo, Milwaukee Bucks
TL-11 Cooper Flagg, Dallas Mavericks
TL-12 Dylan Harper, San Antonio Spurs
TL-13 Kon Knueppel, Charlotte Hornets
TL-14 Ace Bailey, Utah Jazz
TL-15 Khaman Maluach, Phoenix Suns
"""


def is_skip_line(line):
    """Lines to ignore: pack odds, footnotes."""
    # Pack odds like "1:5 packs", "1:8 packs", "1:54 packs"
    if re.match(r"^\d+:\d+", line):
        return True
    # Footnotes like "*Odds as provided by Topps"
    if line.startswith("*"):
        return True
    return False


def parse_print_run(text):
    """Extract serialized print run. Returns None for unnumbered or negative values."""
    m = re.search(r"/(-?\d+)", text)
    if m:
        n = int(m.group(1))
        return n if n > 0 else None
    return None


def parse_parallel_name(text):
    """Return clean parallel name: strip N/N or /N suffix, parentheticals, and trailing *."""
    name = re.sub(r"\s*\([^)]*\)", "", text)       # strip parentheticals like "(1:4)"
    name = re.sub(r"\s*\d*/[-]?\d+\b.*", "", name)  # strip N/N or /N suffix
    name = name.rstrip("* \t")                      # strip trailing asterisks (footnote markers)
    return name.strip()


def parse_section(lines, start_idx):
    """
    Parse one section starting at start_idx (the section name line).
    Returns (section_data, next_idx).
    """
    section_name = lines[start_idx].strip()
    idx = start_idx + 1

    # Skip card count line(s), pack-odds lines, and blank lines up to the parallels/cards block
    while idx < len(lines):
        line = lines[idx].strip()
        if re.match(r"^\d+ cards?\.?$", line):
            idx += 1
        elif is_skip_line(line):
            idx += 1
        elif not line:
            idx += 1
            break  # blank line ends the header block
        else:
            break

    # Parse parallels block
    parallels = []
    in_parallels = False
    while idx < len(lines):
        line = lines[idx].strip()

        if not line:
            idx += 1
            continue

        if is_skip_line(line):
            idx += 1
            continue

        if line.lower() in ("parallels", "parallel", "paralles"):
            in_parallels = True
            idx += 1
            continue

        if in_parallels:
            # First card line signals end of parallels block
            if re.match(r"^[A-Z0-9]+-[A-Z0-9A-Za-z0-9]*\s|^\d+\s", line):
                break
            parallels.append({
                "name": parse_parallel_name(line),
                "print_run": parse_print_run(line),
            })
            idx += 1
        else:
            # Before "Parallels" keyword: card line or unrecognised line ends this phase
            if re.match(r"^[A-Z0-9]+-[A-Z0-9A-Za-z0-9]*\s|^\d+\s", line):
                break
            break

    # Parse cards
    cards = []
    while idx < len(lines):
        line = lines[idx].strip()

        if not line:
            idx += 1
            continue

        if is_skip_line(line):
            idx += 1
            continue

        # Detect start of next section: peek ahead for "N cards" line
        peek = idx + 1
        while peek < len(lines) and not lines[peek].strip():
            peek += 1
        if peek < len(lines) and re.match(r"^\d+ cards?\.?$", lines[peek].strip()):
            break

        # Card line: prefixed by alphanumeric code (e.g. "1", "NO-1", "RJA-CF")
        card_match = re.match(
            r"^([A-Z0-9]+-[A-Z0-9A-Za-z0-9]*|\d+)\s+(.+)",
            line,
        )
        if card_match:
            card_number = card_match.group(1)
            rest = card_match.group(2).strip()

            # RC designation (inline on base set cards 61-100)
            is_rookie = bool(re.search(r"\bRC\b", rest))
            rest = re.sub(r"\s+RC\b", "", rest).strip()

            # Split player and team at last comma
            comma_idx = rest.rfind(",")
            if comma_idx != -1:
                player = rest[:comma_idx].strip()
                team = rest[comma_idx + 1:].strip()
                # Strip any trailing /N from team (edge case)
                team = re.sub(r"\s*/\d+\s*$", "", team).strip()
            else:
                player = rest
                team = ""

            cards.append({
                "card_number": card_number,
                "player": player,
                "team": team,
                "is_rookie": is_rookie,
                "subset": None,
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

        # Section header detected by "N cards" on the next non-empty line
        peek = idx + 1
        while peek < len(lines) and not lines[peek].strip():
            peek += 1

        if peek < len(lines) and re.match(r"^\d+ cards?\.?$", lines[peek].strip()):
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
        unique_cards += 1  # base card counts as 1
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
    # Collect all players who are rookies in any section (propagate to all appearances)
    rc_players = set()
    for section in sections:
        for card in section["cards"]:
            if card.get("is_rookie"):
                rc_players.add(card["player"])

    player_index = {}

    for section in sections:
        for card in section["cards"]:
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
        "set_name": "2025-26 Topps Midnight Basketball",
        "sport": "Basketball",
        "season": "2025-26",
        "league": "NBA",
        "sections": sections,
        "players": players,
    }


if __name__ == "__main__":
    print("Parsing 2025-26 Topps Midnight Basketball checklist...")
    sections = parse_checklist(CHECKLIST_TEXT)
    print(f"Raw sections found: {len(sections)}")

    output = build_output(sections)

    with open("nba_midnight_parsed.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nSet: {output['set_name']} ({output['season']})")
    print(f"Sections: {len(output['sections'])}")
    for s in output["sections"]:
        print(f"  {s['insert_set']}: {len(s['cards'])} cards, {len(s['parallels'])} parallels")
    print(f"Players: {len(output['players'])}")

    # Spot-check: Cooper Flagg should appear in Base Set + multiple auto/insert sets
    if "Cooper Flagg" in {p["player"] for p in output["players"]}:
        flagg = next(p for p in output["players"] if p["player"] == "Cooper Flagg")
        print(f"\n=== Cooper Flagg ===")
        print(f"  Insert sets:  {flagg['stats']['insert_sets']}")
        print(f"  Unique cards: {flagg['stats']['unique_cards']}")
        print(f"  1/1s:         {flagg['stats']['one_of_ones']}")
        for a in flagg["appearances"]:
            rc = " [RC]" if a["is_rookie"] else ""
            print(f"    [{a['insert_set']}] #{a['card_number']}  {a['team']}{rc}")

    # Verify RC flag is set for base rookies
    base_section = next(s for s in output["sections"] if s["insert_set"] == "Base Set")
    rookies = [c for c in base_section["cards"] if c["is_rookie"]]
    vets = [c for c in base_section["cards"] if not c["is_rookie"]]
    print(f"\nBase Set: {len(vets)} veterans, {len(rookies)} rookies (RC)")
    print(f"  First RC: #{base_section['cards'][60]['card_number']} {base_section['cards'][60]['player']}")
    print(f"  Last RC:  #{base_section['cards'][99]['card_number']} {base_section['cards'][99]['player']}")
