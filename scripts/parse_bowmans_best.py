import json
import re

CHECKLIST_TEXT = """
2025 Bowman's Best Baseball

Base Set
100 cards
Parallels

Refractor
Wave Refractor
Lazer Refractor /350
Mini-Diamond Refractor /299
Purple Refractor /250
Purple Mojo /250
Purple Lazer /250
Aqua Lava Refractor /199
Aqua Refractor /199
Blue Refractor /150
Blue X-Fractor /150
Blue Lazer /150
Green Refractor /99
Green Mini-Diamond Refractor /99
Yellow Lazer Refractor /75
Yellow Refractor /75
Gold Lava Refractor /50
Gold Refractor /50
Orange Refractor /25
Black Refractor /10
Red Refractor /5
Red Lava Refractor /5
Superfractor /1
Shop for 2025 Bowman's Best Baseball cards on eBay

1 Corey Seager, Texas Rangers
2 Kyle Tucker, Chicago Cubs
3 Garrett Crochet, Boston Red Sox
4 Juan Soto, New York Mets
5 Marcelo Mayer, Boston Red Sox RC
6 Manny Machado, San Diego Padres
7 Jung Hoo Lee, San Francisco Giants
8 Corbin Carroll, Arizona Diamondbacks
9 Kyle Stowers, Miami Marlins
10 Jackson Chourio, Milwaukee Brewers
11 Kristian Campbell, Boston Red Sox RC
12 Tarik Skubal, Detroit Tigers
13 Ronald Acuña Jr., Atlanta Braves
14 José Ramírez, Cleveland Guardians
15 Matt Shaw, Chicago Cubs RC
16 Agustín Ramírez, Miami Marlins RC
17 Jackson Merrill, San Diego Padres
18 Roki Sasaki, Los Angeles Dodgers RC
19 Mason Miller, San Diego Padres
20 Matt Olson, Atlanta Braves
21 Rafael Devers, San Francisco Giants
22 Vladimir Guerrero Jr., Toronto Blue Jays
23 Will Smith, Los Angeles Dodgers
24 James Wood, Washington Nationals RC
25 Andrew Abbott, Cincinnati Reds
26 Mike Trout, Los Angeles Angels
27 Dylan Crews, Washington Nationals RC
28 Jazz Chisholm Jr., New York Yankees
29 Cam Smith, Houston Astros RC
30 Chase Dollander, Colorado Rockies RC
31 Jacob Wilson, Athletics RC
32 Jackson Holliday, Baltimore Orioles
33 Dalton Rushing, Los Angeles Dodgers RC
34 Jeremy Peña, Houston Astros
35 Pete Crow-Armstrong, Chicago Cubs
36 Gunnar Henderson, Baltimore Orioles
37 Elly De La Cruz, Cincinnati Reds
38 Aaron Judge, New York Yankees
39 Bo Bichette, Toronto Blue Jays
40 Paul Skenes, Pittsburgh Pirates
41 Hunter Goodman, Colorado Rockies
42 Nick Kurtz, Athletics RC
43 Seiya Suzuki, Chicago Cubs
44 Masyn Winn, St. Louis Cardinals
45 Hyeseong Kim, Los Angeles Dodgers RC
46 Shohei Ohtani, Los Angeles Dodgers
47 Zach Neto, Los Angeles Angels
48 Byron Buxton, Minnesota Twins
49 Julio Rodríguez, Seattle Mariners
50 Carlos Correa, Houston Astros
51 Pete Alonso, New York Mets
52 Freddie Freeman, Los Angeles Dodgers
53 Junior Caminero, Tampa Bay Rays
54 Fernando Tatis Jr., San Diego Padres
55 Cal Raleigh, Seattle Mariners
56 Kyle Schwarber, Philadelphia Phillies
57 Jacob deGrom, Texas Rangers
58 Francisco Lindor, New York Mets
59 Riley Greene, Detroit Tigers
60 Drake Baldwin, Atlanta Braves RC
61 Steven Kwan, Cleveland Guardians
62 Ketel Marte, Arizona Diamondbacks
63 Wyatt Langford, Texas Rangers
64 Mookie Betts, Los Angeles Dodgers
65 Bryce Harper, Philadelphia Phillies
66 Chandler Simpson, Tampa Bay Rays RC
67 Cristopher Sánchez, Philadelphia Phillies
68 Spencer Schwellenbach, Atlanta Braves RC
69 Bobby Witt Jr., Kansas City Royals
70 Luke Keaschall, Minnesota Twins RC

Base – Top Prospects
30 cards

TP-1 Max Clark, Detroit Tigers
TP-2 Christian Moore, Los Angeles Angels
TP-3 Jac Caglianone, Kansas City Royals
TP-4 Colson Montgomery, Chicago White Sox
TP-5 Travis Bazzana, Cleveland Guardians
TP-6 Kade Anderson, Seattle Mariners
TP-7 Walker Jenkins, Minnesota Twins
TP-8 Charlie Condon, Colorado Rockies
TP-9 Bubba Chandler, Pittsburgh Pirates
TP-10 Carson Williams, Tampa Bay Rays
TP-11 Andrew Painter, Philadelphia Phillies
TP-12 Jacob Misiorowski, Milwaukee Brewers
TP-13 Josuar Gonzalez, San Francisco Giants
TP-14 JJ Wetherholt, St. Louis Cardinals
TP-15 Bryce Eldridge, San Francisco Giants
TP-16 Roman Anthony, Boston Red Sox
TP-17 Jesús Made, Milwaukee Brewers
TP-18 Brice Matthews, Houston Astros
TP-19 Braden Montgomery, Chicago White Sox
TP-20 Eli Willits, Washington Nationals
TP-21 Chase Burns, Cincinnati Reds
TP-22 Carson Benge, New York Mets
TP-23 George Lombard Jr., New York Yankees
TP-24 Luis Peña, Milwaukee Brewers
TP-25 Sebastian Walcott, Texas Rangers
TP-26 Leo De Vries, Athletics
TP-27 Konnor Griffin, Pittsburgh Pirates
TP-28 Kevin McGonigle, Detroit Tigers
TP-29 Eduardo Quintero, Los Angeles Dodgers
TP-30 Slade Caldwell, Arizona Diamondbacks

Autographs
Best Of 2025 Autographs
131 cards
Parallels

Refractor
Blue Refractor /150
Green Refractor /99
Purple Refractor /75
Gold Mini-Diamond Refractor /50
Gold Refractor /50
Orange X-Fractor /25
Orange Refractor /25
Teal Refractor /15
Black Refractor /10
Black X-Fractor /10
Red Refractor /5
Red X-Fractor /5
Superfractor /1
Printing Plates /1 (Each card has Cyan, Magenta, Yellow, and Black versions)
Shop for Best Of 2025 Autographs on eBay

B25-AL Arnaldo Lantigua, Cincinnati Reds
B25-AS Andrew Salas, Miami Marlins
B25-ASA Aidan Smith, Tampa Bay Rays
B25-BB Brody Brecht, Colorado Rockies
B25-BBU Blake Burke, Milwaukee Brewers
B25-BC Bubba Chandler, Pittsburgh Pirates
B25-BCA Billy Carlson, Chicago White Sox
B25-BL Brooks Lee, Minnesota Twins
B25-BM Braden Montgomery, Chicago White Sox
B25-BR Bryce Rainer, Detroit Tigers
B25-CAN Carlos Narváez, Boston Red Sox
B25-CBE Carson Benge, New York Mets
B25-CBO Caleb Bonemer, Chicago White Sox
B25-CC Charlie Condon, Colorado Rockies
B25-CCA Cole Carrigg, Colorado Rockies
B25-CD Caden Dana, Los Angeles Angels
B25-CDAV Charles Davalan, Los Angeles Dodgers
B25-CDO Chase Dollander, Colorado Rockies
B25-CK C.J. Kayfus, Cleveland Guardians
B25-CKO Ching-Hsien Ko, Los Angeles Dodgers
B25-CL Caleb Lomavita, Washington Nationals
B25-CM Coby Mayo, Baltimore Orioles
B25-CMC Charles McAdoo, Toronto Blue Jays
B25-CME Chase Meidroth, Chicago White Sox
B25-CP Chase Petty, Cincinnati Reds
B25-CS Cam Smith, Houston Astros
B25-CSI Chandler Simpson, Tampa Bay Rays
B25-CW Carson Williams, Tampa Bay Rays
B25-DB Drake Baldwin, Atlanta Braves
B25-DC Dylan Crews, Washington Nationals
B25-DCU Dean Curley, Cleveland Guardians
B25-DN Dante Nori, Philadelphia Phillies
B25-DT Diego Tornes, Atlanta Braves
B25-EBI Eric Bitonti, Milwaukee Brewers
B25-EP Elian Peña, New York Mets
B25-ÉP Émilien Pitre, Tampa Bay Rays
B25-EQ Edgar Quero, Chicago White Sox
B25-EQU Eduardo Quintero, Los Angeles Dodgers
B25-EU Engelth Urena, New York Yankees
B25-EV Esmerlyn Valdez, Pittsburgh Pirates
B25-EW Eli Willits, Washington Nationals
B25-FA Franklin Arias, Boston Red Sox
B25-GB Griffin Burkholder, Philadelphia Phillies
B25-GG Gino Groover, Arizona Diamondbacks
B25-GK Gavin Kilen, San Francisco Giants
B25-GL George Lombard Jr., New York Yankees
B25-GW Gage Wood, Philadelphia Phillies
B25-HS Hagen Smith, Chicago White Sox
B25-II Ike Irish, Baltimore Orioles
B25-JA Jamie Arnold, Athletics
B25-JAW Jacob Wilson, Athletics
B25-JB Josue Briceño, Detroit Tigers
B25-JC Jac Caglianone, Kansas City Royals
B25-JCAC Juneiker Caceres, Cleveland Guardians
B25-JE Jaron Elkins, Los Angeles Dodgers
B25-JF Jonny Farmelo, Seattle Mariners
B25-JG Josuar Gonzalez, San Francisco Giants
B25-JGA Jhostynxon Garcia, Boston Red Sox
B25-JH Josh Hammond, Kansas City Royals
B25-JJU Jace Jung, Detroit Tigers
B25-JJW JJ Wetherholt, St. Louis Cardinals
B25-JL Jansel Luis, Arizona Diamondbacks
B25-JLO Jonathon Long, Chicago Cubs
B25-JLU Joswa Lugo, Los Angeles Angels
B25-JM Jesús Made, Milwaukee Brewers
B25-JMA Jake Mangum, Tampa Bay Rays
B25-JMI Jacob Misiorowski, Milwaukee Brewers
B25-JP JoJo Parker, Toronto Blue Jays
B25-JR Jacob Reimer, New York Mets
B25-JTH Jared Thomas, Colorado Rockies
B25-JTO Jonah Tong, New York Mets
B25-JW James Wood, Washington Nationals
B25-JWI Jaxon Wiggins, Chicago Cubs
B25-KA Kevin Alcántara, Chicago Cubs
B25-KAN Kade Anderson, Seattle Mariners
B25-KC Kristian Campbell, Boston Red Sox
B25-KD Kyle DeBarge, Minnesota Twins
B25-KG Konnor Griffin, Pittsburgh Pirates
B25-KL Kellon Lindsey, Los Angeles Dodgers
B25-KM Kevin McGonigle, Detroit Tigers
B25-KMA Kash Mayfield, San Diego Padres
B25-LD Leo De Vries, Athletics
B25-LDI Luke Dickerson, Washington Nationals
B25-LDO Liam Doyle, St. Louis Cardinals
B25-LK Luke Keaschall, Minnesota Twins
B25-LP Luis Peña, Milwaukee Brewers
B25-MA Mick Abel, Minnesota Twins
B25-MC Max Clark, Detroit Tigers
B25-MCE Mani Cedeno, New York Yankees
B25-MM Malcolm Moore, Texas Rangers
B25-MMA Marcelo Mayer, Boston Red Sox
B25-MS Matt Shaw, Chicago Cubs
B25-MSI Mike Sirota, Los Angeles Dodgers
B25-NB Nick Becker, Seattle Mariners
B25-NC Noah Cameron, Kansas City Royals
B25-NG Nate George, Baltimore Orioles
B25-NK Nick Kurtz, Athletics
B25-NS Noah Schultz, Chicago White Sox
B25-PM PJ Morlando, Miami Marlins
B25-QM Quinn Mathews, St. Louis Cardinals
B25-QY Quentin Young, Minnesota Twins
B25-RA Robert Arias, Cleveland Guardians
B25-RAN Roman Anthony, Boston Red Sox
B25-RH Robert Hassell III, Washington Nationals
B25-RL Rhett Lowder, Cincinnati Reds
B25-RR Rainiel Rodriguez, St. Louis Cardinals
B25-RS Roki Sasaki, Los Angeles Dodgers
B25-SC Slade Caldwell, Arizona Diamondbacks
B25-SH Steele Hall, Cincinnati Reds
B25-SK Sean Keys, Toronto Blue Jays
B25-SM Shotaro Morii, Athletics
B25-SMA Stiven Martinez, Baltimore Orioles
B25-SS Spencer Schwellenbach, Atlanta Braves
B25-TB Travis Bazzana, Cleveland Guardians
B25-TBR Tyler Bremner, Los Angeles Angels
B25-TG Theo Gillen, Tampa Bay Rays
B25-TL Thayron Liranzo, Detroit Tigers
B25-TLE Tyson Lewis, Cincinnati Reds
B25-TP Tai Peete, Seattle Mariners
B25-TT Tim Tawa, Arizona Diamondbacks
B25-TW Thomas White, Miami Marlins
B25-TWH Tommy White, Athletics
B25-WJ Walker Jenkins, Minnesota Twins
B25-WJA Walker Janek, Houston Astros
B25-XN Xavier Neyens, Houston Astros
B25-YC Yolfran Castillo, Texas Rangers
B25-YCA Yeremy Cabrera, Texas Rangers
B25-YP Yairo Padilla, St. Louis Cardinals
B25-YR Yandel Ricardo, Kansas City Royals
B25-ZC Zach Cole, Houston Astros
B25-ZH Zyhir Hope, Los Angeles Dodgers

Best Mix Autographs
52 cards

Shop for Best Mix Autographs on eBay

BMA-AB Alex Bregman, Boston Red Sox /10
BMA-AM Aidan Miller, Philadelphia Phillies /10
BMA-AR Austin Riley, Atlanta Braves /10
BMA-ARU Adley Rutschman, Baltimore Orioles /10
BMA-AS Andrew Salas, Miami Marlins /10
BMA-AV Anthony Volpe, New York Yankees /10
BMA-BC Bubba Chandler, Pittsburgh Pirates /10
BMA-BW Bobby Witt Jr., Kansas City Royals /10
BMA-CC Charlie Condon, Colorado Rockies /10
BMA-CCA Corbin Carroll, Arizona Diamondbacks /10
BMA-CHM Christian Moore, Los Angeles Angels /10
BMA-CM Coby Mayo, Baltimore Orioles /10
BMA-CMO Colson Montgomery, Chicago White Sox /10
BMA-CS Corey Seager, Texas Rangers /10
BMA-CW Carson Williams, Tampa Bay Rays /10
BMA-DB Drake Baldwin, Atlanta Braves /10
BMA-DC Dylan Crews, Washington Nationals /10
BMA-EP Elian Peña, New York Mets /10
BMA-FL Francisco Lindor, New York Mets /10
BMA-GH Gunnar Henderson, Baltimore Orioles /10
BMA-JCAG Jac Caglianone, Kansas City Royals /10
BMA-JCJ Jazz Chisholm Jr., New York Yankees /10
BMA-JG Josuar Gonzalez, San Francisco Giants /10
BMA-JH Jackson Holliday, Baltimore Orioles /10
BMA-JJ Jackson Jobe, Detroit Tigers /10
BMA-JJU Jace Jung, Detroit Tigers /10
BMA-JJW JJ Wetherholt, St. Louis Cardinals /10
BMA-JMA Jesús Made, Milwaukee Brewers /10
BMA-JR Julio Rodríguez, Seattle Mariners /10
BMA-JS Juan Soto, New York Mets /10
BMA-JW James Wood, Washington Nationals /10
BMA-JWI Jacob Wilson, Athletics /10
BMA-KC Kristian Campbell, Boston Red Sox /10
BMA-KG Konnor Griffin, Pittsburgh Pirates /10
BMA-KR Kumar Rocker, Texas Rangers /10
BMA-KT Kyle Teel, Chicago White Sox /10
BMA-LD Leo De Vries, San Diego Padres /10
BMA-MS Matt Shaw, Chicago Cubs /10
BMA-MT Mike Trout, Los Angeles Angels /10
BMA-NK Nick Kurtz, Athletics /10
BMA-PC Pete Crow-Armstrong, Chicago Cubs /10
BMA-PS Paul Skenes, Pittsburgh Pirates /10
BMA-RAN Roman Anthony, Boston Red Sox /10
BMA-RS Roki Sasaki, Los Angeles Dodgers /10
BMA-SC Slade Caldwell, Arizona Diamondbacks /10
BMA-SM Shotaro Morii, Athletics /10
BMA-TB Travis Bazzana, Cleveland Guardians /10
BMA-TG Theo Gillen, Tampa Bay Rays /10
BMA-WJ Walker Jenkins, Minnesota Twins /10
BMA-WL Wyatt Langford, Texas Rangers /10
BMA-YP Yairo Padilla, St. Louis Cardinals /10
BMA-ZH Zyhir Hope, Los Angeles Dodgers /10

Best Performance Autographs
20 cards
Parallels

Lava Refractor /50
Mini Diamond Refractor /25
Superfractor /1
Shop for Best Performance Autographs on eBay

BPA-BC Bubba Chandler, Pittsburgh Pirates
BPA-BW Bobby Witt Jr., Kansas City Royals
BPA-CC Corbin Carroll, Arizona Diamondbacks
BPA-CM Christian Moore, Los Angeles Angels
BPA-CW Carson Williams, Tampa Bay Rays
BPA-DB Drake Baldwin, Atlanta Braves
BPA-DC Dylan Crews, Washington Nationals
BPA-JC Jackson Chourio, Milwaukee Brewers
BPA-JCAG Jac Caglianone, Kansas City Royals
BPA-JJW JJ Wetherholt, St. Louis Cardinals
BPA-JMA Jesús Made, Milwaukee Brewers
BPA-JW James Wood, Washington Nationals
BPA-JWI Jacob Wilson, Athletics
BPA-NS Noah Schultz, Chicago White Sox
BPA-PS Paul Skenes, Pittsburgh Pirates
BPA-SB Samuel Basallo, Baltimore Orioles
BPA-SO Shohei Ohtani, Los Angeles Dodgers
BPA-TB Travis Bazzana, Cleveland Guardians
BPA-WJ Walker Jenkins, Minnesota Twins
BPA-WL Wyatt Langford, Texas Rangers

Best Tek Autographs
20 cards
Parallels

Gold /50
Orange /25
Red /5
Black /1
Shop for Best Tek Autographs on eBay

BTA-CC Charlie Condon, Colorado Rockies
BTA-CM Christian Moore, Los Angeles Angels
BTA-CMA Coby Mayo, Baltimore Orioles
BTA-CMO Colson Montgomery, Chicago White Sox
BTA-CW Carson Williams, Tampa Bay Rays
BTA-DC Dylan Crews, Washington Nationals
BTA-JC Jac Caglianone, Kansas City Royals
BTA-JM Jesús Made, Milwaukee Brewers
BTA-JW JJ Wetherholt, St. Louis Cardinals
BTA-JWO James Wood, Washington Nationals
BTA-KA Kevin Alcántara, Chicago Cubs
BTA-KC Kristian Campbell, Boston Red Sox
BTA-LD Leo De Vries, San Diego Padres
BTA-MS Matt Shaw, Chicago Cubs
BTA-MT Mike Trout, Los Angeles Angels
BTA-RA Roman Anthony, Boston Red Sox
BTA-RS Roki Sasaki, Los Angeles Dodgers
BTA-SO Shohei Ohtani, Los Angeles Dodgers
BTA-TB Travis Bazzana, Cleveland Guardians
BTA-WJ Walker Jenkins, Minnesota Twins

Dual Autographs
20 cards
Parallels

Gold Refractor /50
Orange Refractor /25
Red Refractor /5
Superfractor /1
Shop for Dual Autographs on eBay

DA-CG Bubba Chandler/Konnor Griffin, Pittsburgh Pirates /75
DA-CM Owen Murphy/Cam Caminiti, Atlanta Braves /75
DA-CMC Max Clark/Kevin McGonigle, Detroit Tigers /75
DA-CT Charlie Condon/James Tibbs III, Colorado Rockies/Los Angeles Dodgers /75
DA-CW Slade Caldwell/Ryan Waldschmidt, Arizona Diamondbacks /75
DA-GL Jhonny Level/Josuar Gonzalez, San Francisco Giants /75
DA-GP Josuar Gonzalez/Elian Peña, San Francisco Giants/New York Mets /75
DA-HC Billy Carlson/Seth Hernandez, Chicago White Sox/Pittsburgh Pirates /75
DA-KC Nick Kurtz/Jac Caglianone, Athletics/Kansas City Royals /75
DA-MJ Carter Johnson/PJ Morlando, Miami Marlins /75
DA-MN Aidan Miller/Dante Nori, Philadelphia Phillies /75
DA-MP Luis Peña/Jesús Made, Milwaukee Brewers /75
DA-MPA Andrew Painter/Aidan Miller, Philadelphia Phillies /75
DA-OS Roki Sasaki/Shohei Ohtani, Los Angeles Dodgers /75
DA-SOU Tate Southisene/Ty Southisene, Atlanta Braves/Chicago Cubs /75
DA-WC Dylan Crews/James Wood, Washington Nationals /75
DA-WCA Jac Caglianone/Bobby Witt Jr., Kansas City Royals /75
DA-WK Jacob Wilson/Nick Kurtz, Athletics /75
DA-WW JJ Wetherholt/Masyn Winn, St. Louis Cardinals /75
DA-YS Yoshinobu Yamamoto/Roki Sasaki, Los Angeles Dodgers /75

Triple Autographs
17 cards
Parallels

Gold Refractor /50
Orange Refractor /25
Red Refractor /5
Superfractor /1
Shop for Triple Autographs on eBay

TA-ADA Kade Anderson/Liam Doyle/Jamie Arnold, Seattle Mariners/St. Louis Cardinals/Athletics /75
TA-AWM Tommy White/Shotaro Morii/Jamie Arnold, Athletics /75
TA-CCW Ryan Waldschmidt/Slade Caldwell/Kayson Cunningham, Arizona Diamondbacks /75
TA-CEC Bryce Eldridge/Jac Caglianone/Charlie Condon, San Francisco Giants/Kansas City Royals/Colorado Rockies /75
TA-CMR Bryce Rainer/Kevin McGonigle/Max Clark, Detroit Tigers /75
TA-CWM Tommy White/Dylan Crews/Tre' Morgan, Athletics/Washington Nationals/Tampa Bay Rays /75
TA-DWM Jesús Made/Sebastian Walcott/Leo De Vries, Milwaukee Brewers/Texas Rangers/Athletics /75
TA-GMW Kevin McGonigle/JJ Wetherholt/Konnor Griffin, Detroit Tigers/St. Louis Cardinals/Pittsburgh Pirates /75
TA-GPS Elian Peña/Andrew Salas/Josuar Gonzalez, New York Mets/Miami Marlins/San Francisco Giants /75
TA-MAC Roman Anthony/Kristian Campbell/Marcelo Mayer, Boston Red Sox /75
TA-MMJ Jacob Melton/Walker Janek/Brice Matthews, Houston Astros /75
TA-OYS Shohei Ohtani/Roki Sasaki/Yoshinobu Yamamoto, Los Angeles Dodgers /75
TA-PMW Aidan Miller/Gage Wood/Andrew Painter, Philadelphia Phillies /75
TA-PTG Luis Guanipa/Jose Perdomo/Diego Tornes, Atlanta Braves /75
TA-RHG Teoscar Hernández/Cal Raleigh/Vladimir Guerrero Jr., Los Angeles Dodgers/Seattle Mariners/Toronto Blue Jays /75
TA-WBA Tyler Bremner/Kade Anderson/Eli Willits, Los Angeles Angels/Seattle Mariners/Washington Nationals /75
TA-WSM Quinn Mathews/Hagen Smith/Thomas White, St. Louis Cardinals/Chicago White Sox/Miami Marlins /75

Quad Autographs
13 cards
Parallels

Gold Refractor /50
Orange Refractor /25
Red Refractor /5
Superfractor /1
Shop for Quad Autographs on eBay

QA-ADGS Elly De La Cruz/Ronald Acuña Jr./Vladimir Guerrero Jr./Juan Soto, Cincinnati Reds/Atlanta Braves/Toronto Blue Jays/New York Mets /75
QA-AGTR Jhostynxon Garcia/Franklin Arias/Payton Tolle/Yophery Rodriguez, Boston Red Sox /75
QA-BCPM Jacob Misiorowski/Chase Burns/Andrew Painter/Bubba Chandler, Milwaukee Brewers/Cincinnati Reds/Philadelphia Phillies/Pittsburgh Pirates /75
QA-CMSF Ryan Sloan/Lazaro Montes/Felnin Celesten/Jonny Farmelo, Seattle Mariners /75
QA-DWML Leo De Vries/Jesús Made/George Lombard Jr./Sebastian Walcott, Athletics/Milwaukee Brewers/New York Yankees/Texas Rangers /75
QA-GMRS Andrew Salas/Cris Rodriguez/Shotaro Morii/Josuar Gonzalez, Miami Marlins/Detroit Tigers/Athletics/San Francisco Giants /75
QA-GPRS Elian Peña/Cris Rodriguez/Andrew Salas/Josuar Gonzalez, New York Mets/Detroit Tigers/Miami Marlins/San Francisco Giants /75
QA-HSBW Travis Bazzana/Paul Skenes/Jackson Holliday/Eli Willits, Cleveland Guardians/Pittsburgh Pirates/Baltimore Orioles/Washington Nationals /75
QA-MWWL Jesús Made/JJ Wetherholt/George Lombard Jr./Eli Willits, Milwaukee Brewers/St. Louis Cardinals/New York Yankees/Washington Nationals /75
QA-PHCF Steele Hall/JoJo Parker/Gavin Fien/Billy Carlson, Cincinnati Reds/Toronto Blue Jays/Texas Rangers/Chicago White Sox /75
QA-PWLB Jett Williams/Edward Lantigua/Carson Benge/Elian Peña, New York Mets /75
QA-SSFC Garrett Crochet/Max Fried/Tarik Skubal/Paul Skenes, Boston Red Sox/New York Yankees/Detroit Tigers/Pittsburgh Pirates /75
QA-WGSM Theo Gillen/Aidan Smith/Tre' Morgan/Carson Williams, Tampa Bay Rays /75

Family Tree Triple Autographs
2 cards
Parallels

Mini Diamond /10
Superfractor /1

FTA-AAA Luisangel Acuña/Bryan Acuña/Ronald Acuña Jr., New York Mets/Minnesota Twins/Atlanta Braves
FTA-FFF Jadyn Fielder/Prince Fielder/Cecil Fielder, Milwaukee Brewers/Detroit Tigers

Family Tree Dual Autographs
6 cards
Parallels

Mini Diamond /10
Superfractor /1

FDA-AA Ronald Acuña Jr./Luisangel Acuña, Atlanta Braves/New York Mets
FDA-CC Jaison Chourio/Jackson Chourio, Cleveland Guardians/Milwaukee Brewers
FDA-FI Gavin Fien/Dylan Fien, Texas Rangers/Athletics
FDA-GG Vladimir Guerrero Jr./Vladimir Guerrero, Toronto Blue Jays/Montréal Expos
FDA-SA Andrew Salas/Ethan Salas, Miami Marlins/San Diego Padres
FDA-SS Tate Southisene/Ty Southisene, Atlanta Braves/Chicago Cubs

Bowman Showpieces Autographs
8 cards
Parallel

Superfractor /1

BSA-CS Cam Smith, Houston Astros
BSA-JC Jac Caglianone, Kansas City Royals
BSA-JS Juan Soto, New York Mets
BSA-JW James Wood, Washington Nationals
BSA-MT Mike Trout, Los Angeles Angels
BSA-NK Nick Kurtz, Athletics
BSA-PC Pete Crow-Armstrong, Chicago Cubs
BSA-RA Roman Anthony, Boston Red Sox

Circuitry Autographs
9 cards
Parallel

Superfractor /1

CA-CC Charlie Condon, Colorado Rockies
CA-EW Eli Willits, Washington Nationals
CA-JC Jac Caglianone, Kansas City Royals
CA-JW Jacob Wilson, Athletics
CA-LD Leo De Vries, Athletics
CA-NK Nick Kurtz, Athletics
CA-PC Pete Crow-Armstrong, Chicago Cubs
CA-RA Roman Anthony, Boston Red Sox
CA-RS Roki Sasaki, Los Angeles Dodgers

Prospect Patch Autographs
26 cards
Parallels

Orange Refractor /25
Black Refractor /10
Red Refractor /5
Superfractor /1

PPA-ASA Adolfo Sanchez, Cincinnati Reds /50
PPA-ASM Aidan Smith, Tampa Bay Rays /50
PPA-BM Braden Montgomery, Chicago White Sox /50
PPA-BMA Brice Matthews, Houston Astros /50
PPA-BR Bryce Rainer, Detroit Tigers /50
PPA-CB Chase Burns, Cincinnati Reds /50
PPA-CC Charlie Condon, Colorado Rockies /50
PPA-CM Christian Moore, Los Angeles Angels /50
PPA-DJ Dawel Joseph, Seattle Mariners /50
PPA-FA Franklin Arias, Boston Red Sox /50
PPA-GL George Lombard Jr., New York Yankees /50
PPA-HS Hagen Smith, Chicago White Sox /50
PPA-JC Jac Caglianone, Kansas City Royals /50
PPA-JG Josuar Gonzalez, San Francisco Giants /50
PPA-JL Joswa Lugo, Los Angeles Angels /50
PPA-JM Jesús Made, Milwaukee Brewers /50
PPA-JW JJ Wetherholt, St. Louis Cardinals /50
PPA-KG Konnor Griffin, Pittsburgh Pirates /50
PPA-KM Kevin McGonigle, Detroit Tigers /50
PPA-OC Owen Caissie, Chicago Cubs /50
PPA-PM PJ Morlando, Miami Marlins /50
PPA-RC Robert Calaz, Colorado Rockies /50
PPA-SK Seaver King, Washington Nationals /50
PPA-SM Shotaro Morii, Athletics /50
PPA-TB Travis Bazzana, Cleveland Guardians /50
PPA-YM Yohandy Morales, Washington Nationals /50

Inserts
2025 MLB All-Star Futures Game
20 cards
Parallels

Mini Diamond Refractor
Lava Refractor /50
Superfractor /1
Shop for 2025 MLB All-Star Futures Game inserts on eBay

FG-1 Jonah Tong, National League
FG-2 Charlie Condon, National League
FG-3 Leo De Vries, National League
FG-4 Konnor Griffin, National League
FG-5 JJ Wetherholt, National League
FG-6 Slade Caldwell, National League
FG-7 Josue De Paula, National League
FG-8 Zyhir Hope, National League
FG-9 JR Ritchie, National League
FG-10 Jesús Made, National League
FG-11 Kaelen Culpepper, American League
FG-12 C.J. Kayfus, American League
FG-13 Braden Montgomery, American League
FG-14 Tommy White, American League
FG-15 Jhostynxon Garcia, American League
FG-16 Max Clark, American League
FG-17 Sebastian Walcott, American League
FG-18 Kevin McGonigle, American League
FG-19 George Lombard Jr., American League
FG-20 Josue Briceño, American League

Pixel Portraits
25 cards
Parallels

Mini Diamond Refractor
Lava Refractor /50
Superfractor /1
Shop for Pixel Portraits inserts on eBay

P-1 James Wood, Washington Nationals
P-2 Pete Crow-Armstrong, Chicago Cubs
P-3 Liam Doyle, St. Louis Cardinals
P-4 Jacob Wilson, Athletics
P-5 Ronald Acuña Jr., Atlanta Braves
P-6 Charlie Condon, Colorado Rockies
P-7 Roki Sasaki, Los Angeles Dodgers
P-8 Nick Kurtz, Athletics
P-9 Mike Trout, Los Angeles Angels
P-10 Elly De La Cruz, Cincinnati Reds
P-11 Cal Raleigh, Seattle Mariners
P-12 Adley Rutschman, Baltimore Orioles
P-13 Bobby Witt Jr., Kansas City Royals
P-14 Paul Skenes, Pittsburgh Pirates
P-15 Konnor Griffin, Pittsburgh Pirates
P-16 Tarik Skubal, Detroit Tigers
P-17 Jesús Made, Milwaukee Brewers
P-18 Marcelo Mayer, Boston Red Sox
P-19 Cam Smith, Houston Astros
P-20 Francisco Lindor, New York Mets
P-21 Eli Willits, Washington Nationals
P-22 José Ramírez, Cleveland Guardians
P-23 Aaron Judge, New York Yankees
P-24 Bryce Harper, Philadelphia Phillies
P-25 Shohei Ohtani, Los Angeles Dodgers

Circuitry
25 cards
Parallels

Mini Diamond Refractor
Lava Refractor /50
Superfractor /1
Shop for Circuitry inserts on eBay

C-1 Bobby Witt Jr., Kansas City Royals
C-2 Bryce Harper, Philadelphia Phillies
C-3 Roman Anthony, Boston Red Sox
C-4 Jacob Wilson, Athletics
C-5 Liam Doyle, St. Louis Cardinals
C-6 Julio Rodríguez, Seattle Mariners
C-7 Corbin Carroll, Arizona Diamondbacks
C-8 Jac Caglianone, Kansas City Royals
C-9 Junior Caminero, Tampa Bay Rays
C-10 Elly De La Cruz, Cincinnati Reds
C-11 Jacob Misiorowski, Milwaukee Brewers
C-12 Drake Baldwin, Atlanta Braves
C-13 Leo De Vries, Athletics
C-14 Shohei Ohtani, Los Angeles Dodgers
C-15 Charlie Condon, Colorado Rockies
C-16 Nick Kurtz, Athletics
C-17 Tarik Skubal, Detroit Tigers
C-18 Pete Crow-Armstrong, Chicago Cubs
C-19 Cam Smith, Houston Astros
C-20 Gunnar Henderson, Baltimore Orioles
C-21 Paul Skenes, Pittsburgh Pirates
C-22 Fernando Tatis Jr., San Diego Padres
C-23 Eli Willits, Washington Nationals
C-24 Roki Sasaki, Los Angeles Dodgers
C-25 Marcelo Mayer, Boston Red Sox

Best Performance
30 cards
Parallels

Mini Diamond Refractor
Lava Refractor /50
Superfractor /1
Shop for Best Performance inserts on eBay

BP-1 Paul Skenes, Pittsburgh Pirates
BP-2 Bobby Witt Jr., Kansas City Royals
BP-3 Corbin Carroll, Arizona Diamondbacks
BP-4 Wyatt Langford, Texas Rangers
BP-5 Jackson Chourio, Milwaukee Brewers
BP-6 Jackson Merrill, San Diego Padres
BP-7 Dylan Crews, Washington Nationals
BP-8 James Wood, Washington Nationals
BP-9 Hyeseong Kim, Los Angeles Dodgers
BP-10 Carson Williams, Tampa Bay Rays
BP-11 Travis Bazzana, Cleveland Guardians
BP-12 Walker Jenkins, Minnesota Twins
BP-13 Jac Caglianone, Kansas City Royals
BP-14 Leo De Vries, Athletics
BP-15 JJ Wetherholt, St. Louis Cardinals
BP-16 Cam Smith, Houston Astros
BP-17 Bubba Chandler, Pittsburgh Pirates
BP-18 Samuel Basallo, Baltimore Orioles
BP-19 Roman Anthony, Boston Red Sox
BP-20 Jesús Made, Milwaukee Brewers
BP-21 Shohei Ohtani, Los Angeles Dodgers
BP-22 Mike Trout, Los Angeles Angels
BP-23 Roki Sasaki, Los Angeles Dodgers
BP-24 Ronald Acuña Jr., Atlanta Braves
BP-25 Max Clark, Detroit Tigers
BP-26 Kyle Tucker, Chicago Cubs
BP-27 Marcelo Mayer, Boston Red Sox
BP-28 Jacob Wilson, Athletics
BP-29 Christian Moore, Los Angeles Angels
BP-30 Drake Baldwin, Atlanta Braves

Bowman Showpieces
15 cards
Parallels

Mini Diamond Refractor
Lava Refractor /50
Superfractor /1
Shop for Bowman Showpieces inserts on eBay

BS-1 James Wood, Washington Nationals
BS-2 Nick Kurtz, Athletics
BS-3 Marcelo Mayer, Boston Red Sox
BS-4 Cam Smith, Houston Astros
BS-5 Roman Anthony, Boston Red Sox
BS-6 Jac Caglianone, Kansas City Royals
BS-7 Cal Raleigh, Seattle Mariners
BS-8 Pete Crow-Armstrong, Chicago Cubs
BS-9 Mike Trout, Los Angeles Angels
BS-10 Juan Soto, New York Mets
BS-11 JJ Wetherholt, St. Louis Cardinals
BS-12 Shohei Ohtani, Los Angeles Dodgers
BS-13 Aaron Judge, New York Yankees
BS-14 Roki Sasaki, Los Angeles Dodgers
BS-15 Konnor Griffin, Pittsburgh Pirates

Strokes Of Gold
25 cards

Shop for Strokes Of Gold inserts on eBay

SG-1 James Wood, Washington Nationals
SG-2 Jacob Wilson, Athletics
SG-3 Dylan Crews, Washington Nationals
SG-4 Nick Kurtz, Athletics
SG-5 Drake Baldwin, Atlanta Braves
SG-6 Marcelo Mayer, Boston Red Sox
SG-7 Hyeseong Kim, Los Angeles Dodgers
SG-8 Cam Smith, Houston Astros
SG-9 Luke Keaschall, Minnesota Twins
SG-10 Dalton Rushing, Los Angeles Dodgers
SG-11 Aaron Judge, New York Yankees
SG-12 Shohei Ohtani, Los Angeles Dodgers
SG-13 Ronald Acuña Jr., Atlanta Braves
SG-14 Cal Raleigh, Seattle Mariners
SG-15 Pete Crow-Armstrong, Chicago Cubs
SG-16 Elly De La Cruz, Cincinnati Reds
SG-17 George Lombard Jr., New York Yankees
SG-18 Charlie Condon, Colorado Rockies
SG-19 Eli Willits, Washington Nationals
SG-20 Konnor Griffin, Pittsburgh Pirates
SG-21 Jac Caglianone, Kansas City Royals
SG-22 JJ Wetherholt, St. Louis Cardinals
SG-23 Bryce Eldridge, San Francisco Giants
SG-24 Jesús Made, Milwaukee Brewers
SG-25 Josuar Gonzalez, San Francisco Giants

Best Tek
30 cards
Parallels

Blue /75
Gold /50
Orange /25
Red /5
Black /1
Shop for Best Tek inserts on eBay

BT-1 Kevin Alcántara, Chicago Cubs /99
BT-2 James Wood, Washington Nationals /99
BT-3 Mike Trout, Los Angeles Angels /99
BT-4 JJ Wetherholt, St. Louis Cardinals /99
BT-5 Hyeseong Kim, Los Angeles Dodgers /99
BT-6 Dylan Crews, Washington Nationals /99
BT-7 Christian Moore, Los Angeles Angels /99
BT-8 Charlie Condon, Colorado Rockies /99
BT-9 Bobby Witt Jr., Kansas City Royals /99
BT-10 Coby Mayo, Baltimore Orioles /99
BT-11 Aaron Judge, New York Yankees /99
BT-12 Jackson Chourio, Milwaukee Brewers /99
BT-13 Juan Soto, New York Mets /99
BT-14 Jac Caglianone, Kansas City Royals /99
BT-15 Walker Jenkins, Minnesota Twins /99
BT-16 Colt Emerson, Seattle Mariners /99
BT-17 Roman Anthony, Boston Red Sox /99
BT-18 Luisangel Acuña, New York Mets /99
BT-19 Bryce Eldridge, San Francisco Giants /99
BT-20 Colson Montgomery, Chicago White Sox /99
BT-21 Travis Bazzana, Cleveland Guardians /99
BT-22 Matt Shaw, Chicago Cubs /99
BT-23 Roki Sasaki, Los Angeles Dodgers /99
BT-24 Kristian Campbell, Boston Red Sox /99
BT-25 Paul Skenes, Pittsburgh Pirates /99
BT-26 Elly De La Cruz, Cincinnati Reds /99
BT-27 Jesús Made, Milwaukee Brewers /99
BT-28 Shohei Ohtani, Los Angeles Dodgers /99
BT-29 Leo De Vries, Athletics /99
BT-30 Carson Williams, Tampa Bay Rays /99
"""

# League affiliations that appear as "team" in Futures Game — stored as subset_tag
LEAGUE_TAGS = {"National League", "American League"}


def is_skip_line(line):
    return bool(re.match(r"^Shop for\b", line, re.IGNORECASE))


def parse_print_run(text):
    m = re.search(r"/(-?\d+)", text)
    if m:
        n = int(m.group(1))
        return n if n > 0 else None
    return None


def parse_parallel_name(text):
    name = re.sub(r"\s*\([^)]*\)", "", text)       # strip parentheticals
    name = re.sub(r"\s*\d*/[-]?\d+\b.*", "", name)  # strip N/N or /N suffix
    return name.strip()


def parse_multi_player(rest, card_number):
    """
    Parse a multi-player card line (players separated by '/').
    Format: 'P1/P2[/...], T1[/T2[/...]] [/serial]'
    Returns list of card dicts, one per player.
    """
    rest = re.sub(r"\s*/\d+\s*$", "", rest).strip()  # strip trailing /serial

    comma_idx = rest.rfind(",")
    if comma_idx == -1:
        return [{"card_number": card_number, "player": rest.strip(),
                 "team": "", "is_rookie": False, "subset": None}]

    players_str = rest[:comma_idx].strip()
    teams_str = rest[comma_idx + 1:].strip()

    player_names = [p.strip() for p in players_str.split("/")]
    teams = [t.strip() for t in teams_str.split("/")]

    result = []
    for i, name in enumerate(player_names):
        team = teams[min(i, len(teams) - 1)] if teams else ""
        result.append({"card_number": card_number, "player": name,
                       "team": team, "is_rookie": False, "subset": None})
    return result


def parse_section(lines, start_idx):
    section_name = lines[start_idx].strip()
    idx = start_idx + 1

    # Skip card count, then stop at blank or non-matching line
    while idx < len(lines):
        line = lines[idx].strip()
        if re.match(r"^\d+ cards?\.?$", line):
            idx += 1
        elif not line:
            idx += 1
            break
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
        if line.lower() in ("parallels", "parallel"):
            in_parallels = True
            idx += 1
            continue

        if in_parallels:
            if re.match(r"^[A-Z0-9]+-[^\s]*\s|^\d+\s", line):
                break
            parallels.append({
                "name": parse_parallel_name(line),
                "print_run": parse_print_run(line),
            })
            idx += 1
        else:
            if re.match(r"^[A-Z0-9]+-[^\s]*\s|^\d+\s", line):
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

        # Detect next section via peek
        peek = idx + 1
        while peek < len(lines) and not lines[peek].strip():
            peek += 1
        if peek < len(lines) and re.match(r"^\d+ cards?\.?$", lines[peek].strip()):
            break

        # Card line
        card_match = re.match(r"^([A-Z0-9]+-[^\s]+|\d+)\s+(.+)", line)
        if card_match:
            card_number = card_match.group(1)
            rest = card_match.group(2).strip()

            # RC detection (applies to base set)
            is_rookie = bool(re.search(r"\bRC\b", rest))
            rest = re.sub(r"\s+RC\b", "", rest).strip()

            # Detect multi-player: "/" before the last comma
            comma_idx = rest.rfind(",")
            is_multi = comma_idx != -1 and "/" in rest[:comma_idx]

            if is_multi:
                entries = parse_multi_player(rest, card_number)
            else:
                # Single player
                if comma_idx != -1:
                    player = rest[:comma_idx].strip()
                    team = rest[comma_idx + 1:].strip()
                    team = re.sub(r"\s*/\d+\s*$", "", team).strip()
                else:
                    player = rest
                    team = ""

                # Futures Game: league affiliation becomes subset_tag
                if team in LEAGUE_TAGS:
                    entries = [{"card_number": card_number, "player": player,
                                "team": "", "is_rookie": is_rookie, "subset": team}]
                else:
                    entries = [{"card_number": card_number, "player": player,
                                "team": team, "is_rookie": is_rookie, "subset": None}]

            cards.extend(entries)

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

        peek = idx + 1
        while peek < len(lines) and not lines[peek].strip():
            peek += 1

        if peek < len(lines) and re.match(r"^\d+ cards?\.?$", lines[peek].strip()):
            section, idx = parse_section(lines, idx)
            if section["cards"]:
                # Best Mix Autographs: synthetic base /10 parallel (no parallels block in checklist)
                if section["insert_set"] == "Best Mix Autographs":
                    section["parallels"] = [{"name": "Base", "print_run": 10}]
                # Best Tek: prepend synthetic base /99 parallel
                elif section["insert_set"] == "Best Tek":
                    section["parallels"].insert(0, {"name": "Base", "print_run": 99})
                sections.append(section)
        else:
            idx += 1

    # Merge "Base – Top Prospects" cards into "Base Set" (same parallels, one insert group)
    base_idx = next((i for i, s in enumerate(sections) if s["insert_set"] == "Base Set"), None)
    tp_idx = next((i for i, s in enumerate(sections)
                   if s["insert_set"] == "Base – Top Prospects"), None)
    if base_idx is not None and tp_idx is not None:
        sections[base_idx]["cards"].extend(sections[tp_idx]["cards"])
        sections = [s for s in sections if s["insert_set"] != "Base – Top Prospects"]

    return sections


def compute_stats(appearances):
    unique_cards = 0
    total_print_run = 0
    one_of_ones = 0

    for appearance in appearances:
        unique_cards += 1
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
                "is_rookie": card["player"] in rc_players,
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
        "set_name": "2025 Bowman's Best Baseball",
        "sport": "Baseball",
        "season": "2025",
        "league": "MLB",
        "sections": sections,
        "players": players,
    }


if __name__ == "__main__":
    print("Parsing 2025 Bowman's Best Baseball checklist...")
    sections = parse_checklist(CHECKLIST_TEXT)
    print(f"Raw sections found: {len(sections)}")

    output = build_output(sections)

    with open("bowmans_best_parsed.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nSet: {output['set_name']} ({output['season']})")
    print(f"Sections: {len(output['sections'])}")
    for s in output["sections"]:
        print(f"  {s['insert_set']}: {len(s['cards'])} cards, {len(s['parallels'])} parallels")
    print(f"Players: {len(output['players'])}")

    # Spot-checks
    for name in ["Roki Sasaki", "Jesús Made", "Cooper Flagg"]:
        match = next((p for p in output["players"] if p["player"] == name), None)
        if match:
            print(f"\n=== {name} ===")
            print(f"  Sets: {match['stats']['insert_sets']}  Unique: {match['stats']['unique_cards']}  1/1s: {match['stats']['one_of_ones']}")
            rc_apps = [a for a in match["appearances"] if a["is_rookie"]]
            if rc_apps:
                print(f"  RC appearances: {len(rc_apps)}")

    # Base Set RC check
    base = next(s for s in output["sections"] if s["insert_set"] == "Base Set")
    rookies = [c for c in base["cards"] if c["is_rookie"]]
    print(f"\nBase Set: {len(base['cards'])} cards ({len(rookies)} RC)")

    # Futures Game check
    fg = next((s for s in output["sections"] if "Futures" in s["insert_set"]), None)
    if fg:
        nl = [c for c in fg["cards"] if c["subset"] == "National League"]
        al = [c for c in fg["cards"] if c["subset"] == "American League"]
        print(f"Futures Game: {len(nl)} NL + {len(al)} AL")

    # Multi-player check
    da = next((s for s in output["sections"] if s["insert_set"] == "Dual Autographs"), None)
    if da:
        print(f"Dual Autographs raw cards: {len(da['cards'])} (20 cards × 2 players = 40 expected)")
