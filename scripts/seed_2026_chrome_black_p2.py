"""
Seed: 2026 Topps Chrome Black Baseball — Part 2
Base cards and all autograph sets.
Usage: python3 scripts/seed_2026_chrome_black_p2.py
"""
import sqlite3, os, re

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA foreign_keys=ON")
cur = conn.cursor()

SET_ID = 837
T = True; R = False

def get_or_create_player(name):
    cur.execute("SELECT id FROM players WHERE set_id = ? AND name = ?", (SET_ID, name))
    row = cur.fetchone()
    if row: return row[0]
    cur.execute("INSERT INTO players (set_id, name, unique_cards, total_print_run, one_of_ones, insert_set_count) VALUES (?, ?, 0, 0, 0, 0)", (SET_ID, name))
    return cur.lastrowid

def get_is_id(name):
    return cur.execute("SELECT id FROM insert_sets WHERE set_id = ? AND name = ?", (SET_ID, name)).fetchone()[0]

def add_cards(is_id, cards):
    for num, name, team, rookie in cards:
        pid = get_or_create_player(name)
        cur.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)",
                    (pid, is_id, num, int(rookie), team))

def add_dual_cards(is_id, cards):
    for num, n1, t1, n2, t2 in cards:
        p1 = get_or_create_player(n1)
        p2 = get_or_create_player(n2)
        a1 = cur.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, ?)",
                    (p1, is_id, num, t1)).lastrowid
        a2 = cur.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, ?)",
                    (p2, is_id, num, t2)).lastrowid
        cur.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a1, p2))
        cur.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a2, p1))

# ─── BASE (200 cards) ─────────────────────────────────────────────
base_id = get_is_id("Base")
base = [
    ("1","Shohei Ohtani","Los Angeles Dodgers",R),("2","Mike Trout","Los Angeles Angels",R),("3","Ronald Acuna Jr.","Atlanta Braves",R),
    ("4","Mookie Betts","Los Angeles Dodgers",R),("5","Freddie Freeman","Los Angeles Dodgers",R),("6","Juan Soto","New York Mets",R),
    ("7","Julio Rodriguez","Seattle Mariners",R),("8","Aaron Judge","New York Yankees",R),("9","Jose Ramirez","Cleveland Guardians",R),
    ("10","Yordan Alvarez","Houston Astros",R),("11","Gunnar Henderson","Baltimore Orioles",R),("12","Alex Bregman","Boston Red Sox",R),
    ("13","Jac Caglianone","Kansas City Royals",T),("14","Brendan Donovan","St. Louis Cardinals",R),("15","Matt Olson","Atlanta Braves",R),
    ("16","Kyle Tucker","Chicago Cubs",R),("17","Bubba Chandler","Pittsburgh Pirates",T),("18","Pete Alonso","Baltimore Orioles",R),
    ("19","Francisco Lindor","New York Mets",R),("20","Teoscar Hernandez","Los Angeles Dodgers",R),("21","Jacob Misiorowski","Milwaukee Brewers",T),
    ("22","Shota Imanaga","Chicago Cubs",R),("23","Jhostynxon Garcia","Pittsburgh Pirates",T),("24","Jose Altuve","Houston Astros",R),
    ("25","Nolan Arenado","St. Louis Cardinals",R),("26","Payton Tolle","Boston Red Sox",T),("27","Jakob Marsee","Miami Marlins",T),
    ("28","Alex Freeland","Los Angeles Dodgers",T),("29","Marcelo Mayer","Boston Red Sox",R),("30","Sal Stewart","Cincinnati Reds",T),
    ("31","Cade Horton","Chicago Cubs",R),("32","Chris Sale","Atlanta Braves",R),("33","Jung Hoo Lee","San Francisco Giants",R),
    ("34","Jordan Beck","Colorado Rockies",R),("35","Paul Skenes","Pittsburgh Pirates",R),("36","Jeremy Pena","Houston Astros",R),
    ("37","Kyle Stowers","Miami Marlins",R),("38","Chase Burns","Cincinnati Reds",T),("39","Jazz Chisholm Jr.","New York Yankees",R),
    ("40","Zach Neto","Los Angeles Angels",R),("41","Samuel Basallo","Baltimore Orioles",T),("42","Christian Yelich","Milwaukee Brewers",R),
    ("43","Jacob Melton","Houston Astros",T),("44","C.J. Kayfus","Cleveland Guardians",T),("45","Tarik Skubal","Detroit Tigers",R),
    ("46","Nathan Church","St. Louis Cardinals",T),("47","Cal Raleigh","Seattle Mariners",R),("48","Jonah Tong","New York Mets",T),
    ("49","Yoshinobu Yamamoto","Los Angeles Dodgers",R),("50","Bryce Eldridge","San Francisco Giants",T),
    ("51","Owen Caissie","Chicago Cubs",T),("52","Parker Messick","Cleveland Guardians",T),("53","Willson Contreras","St. Louis Cardinals",R),
    ("54","Matt Chapman","San Francisco Giants",R),("55","Roki Sasaki","Los Angeles Dodgers",R),("56","Roman Anthony","Boston Red Sox",T),
    ("57","Agustin Ramirez","Miami Marlins",R),("58","Carter Jensen","Kansas City Royals",T),("59","Randy Arozarena","Seattle Mariners",R),
    ("60","Colson Montgomery","Chicago White Sox",T),("61","Masyn Winn","St. Louis Cardinals",R),("62","Andrew Abbott","Cincinnati Reds",R),
    ("63","Andrew McCutchen","Pittsburgh Pirates",R),("64","Xavier Edwards","Miami Marlins",R),("65","Nolan McLean","New York Mets",T),
    ("66","Dillon Dingler","Detroit Tigers",R),("67","Steven Kwan","Cleveland Guardians",R),("68","Cole Young","Seattle Mariners",T),
    ("69","Denzer Guzman","Los Angeles Angels",T),("70","Dylan Beavers","Baltimore Orioles",T),("71","Salvador Perez","Kansas City Royals",R),
    ("72","Warming Bernabel","Colorado Rockies",T),("73","Bobby Witt Jr.","Kansas City Royals",R),("74","Brandon Sproat","New York Mets",T),
    ("75","Brice Matthews","Houston Astros",T),("76","Chase Dollander","Colorado Rockies",R),("77","Christian Moore","Los Angeles Angels",T),
    ("78","Ryan Ritter","Colorado Rockies",T),("79","Harry Ford","Washington Nationals",T),("80","J.P. Crawford","Seattle Mariners",R),
    ("81","Drake Baldwin","Atlanta Braves",R),("82","Luis Robert Jr.","Chicago White Sox",R),("83","Javier Baez","Detroit Tigers",R),
    ("84","Cody Bellinger","New York Yankees",R),("85","Kyle Teel","Chicago White Sox",T),("86","Matt Shaw","Chicago Cubs",R),
    ("87","Pete Crow-Armstrong","Chicago Cubs",R),("88","Jackson Holliday","Baltimore Orioles",R),("89","Spencer Torkelson","Detroit Tigers",R),
    ("90","Riley Greene","Detroit Tigers",R),("91","Jackson Chourio","Milwaukee Brewers",R),("92","Troy Melton","Detroit Tigers",T),
    ("93","Elly De La Cruz","Cincinnati Reds",R),("94","Kris Bryant","Colorado Rockies",R),("95","Edgar Quero","Chicago White Sox",R),
    ("96","Alec Burleson","St. Louis Cardinals",R),("97","Connelly Early","Boston Red Sox",T),("98","Cam Schlittler","New York Yankees",T),
    ("99","Jimmy Crooks","St. Louis Cardinals",T),("100","Fernando Tatis Jr.","San Diego Padres",R),
    ("101","Carson Williams","Tampa Bay Rays",T),("102","Gabriel Moreno","Arizona Diamondbacks",R),("103","Anthony Volpe","New York Yankees",R),
    ("104","Zack Wheeler","Philadelphia Phillies",R),("105","Bryce Harper","Philadelphia Phillies",R),("106","Will Banfield","Cincinnati Reds",T),
    ("107","Jacob deGrom","Texas Rangers",R),("108","Wyatt Langford","Texas Rangers",R),("109","Byron Buxton","Minnesota Twins",R),
    ("110","Jasson Dominguez","New York Yankees",R),("111","Vladimir Guerrero Jr.","Toronto Blue Jays",R),("112","Carlos Correa","Houston Astros",R),
    ("113","Isaac Collins","Kansas City Royals",R),("114","Luis Arraez","San Diego Padres",R),("115","Bryson Stott","Philadelphia Phillies",R),
    ("116","Nick Kurtz","Athletics",R),("117","Seiya Suzuki","Chicago Cubs",R),("118","Ketel Marte","Arizona Diamondbacks",R),
    ("119","Kodai Senga","New York Mets",R),("120","Xander Bogaerts","San Diego Padres",R),("121","Heriberto Hernandez","Miami Marlins",T),
    ("122","Max Fried","New York Yankees",R),("123","Carson Whisenhunt","San Francisco Giants",T),("124","Mason Miller","San Diego Padres",R),
    ("125","George Springer","Toronto Blue Jays",R),("126","Corey Seager","Texas Rangers",R),("127","Corbin Carroll","Arizona Diamondbacks",R),
    ("128","Spencer Schwellenbach","Atlanta Braves",R),("129","Brooks Lee","Minnesota Twins",R),("130","Cody Freeman","Texas Rangers",T),
    ("131","Trey Yesavage","Toronto Blue Jays",T),("132","Kyle Karros","Colorado Rockies",T),("133","Colby Thomas","Athletics",T),
    ("134","Garrett Crochet","Boston Red Sox",R),("135","Coby Mayo","Baltimore Orioles",R),("136","Giancarlo Stanton","New York Yankees",R),
    ("137","Zach Cole","Houston Astros",T),("138","Hyeseong Kim","Los Angeles Dodgers",R),("139","Trea Turner","Philadelphia Phillies",R),
    ("140","Manny Machado","San Diego Padres",R),("141","Will Smith","Los Angeles Dodgers",R),("142","Ozzie Albies","Atlanta Braves",R),
    ("143","Shinnosuke Ogasawara","Washington Nationals",T),("144","Adley Rutschman","Baltimore Orioles",R),("145","Junior Caminero","Tampa Bay Rays",R),
    ("146","Otto Kemp","Philadelphia Phillies",T),("147","Andres Gimenez","Toronto Blue Jays",R),("148","Mick Abel","Minnesota Twins",R),
    ("149","Bo Bichette","Toronto Blue Jays",R),("150","Dalton Rushing","Los Angeles Dodgers",R),("151","Geraldo Perdomo","Arizona Diamondbacks",R),
    ("152","Brent Rooker","Athletics",R),("153","Justin Verlander","San Francisco Giants",R),("154","Freddy Peralta","Milwaukee Brewers",R),
    ("155","Dylan Crews","Washington Nationals",R),("156","James Wood","Washington Nationals",R),("157","Tyler Soderstrom","Athletics",R),
    ("158","Willy Adames","San Francisco Giants",R),("159","Jackson Jobe","Detroit Tigers",R),("160","Brady House","Washington Nationals",T),
    ("161","Ezequiel Tovar","Colorado Rockies",R),("162","CJ Abrams","Washington Nationals",R),("163","Adolis Garcia","Philadelphia Phillies",R),
    ("164","Zac Gallen","Arizona Diamondbacks",R),("165","Carlos Rodon","New York Yankees",R),("166","Logan Webb","San Francisco Giants",R),
    ("167","Kristian Campbell","Boston Red Sox",R),("168","Brice Turang","Milwaukee Brewers",R),("169","Mason Barnett","Athletics",T),
    ("170","Brandon Lowe","Tampa Bay Rays",R),("171","MacKenzie Gore","Washington Nationals",R),("172","Gerrit Cole","New York Yankees",R),
    ("173","Jacob Wilson","Athletics",R),("174","Drew Gilbert","San Francisco Giants",T),("175","Nico Hoerner","Chicago Cubs",R),
    ("176","Chris Bassitt","Toronto Blue Jays",R),("177","Jackson Merrill","San Diego Padres",R),("178","Paul Goldschmidt","New York Yankees",R),
    ("179","Rafael Devers","San Francisco Giants",R),("180","Alec Bohm","Philadelphia Phillies",R),("181","William Contreras","Milwaukee Brewers",R),
    ("182","Mickey Moniak","Colorado Rockies",R),("183","Royce Lewis","Minnesota Twins",R),("184","Michael Harris II","Atlanta Braves",R),
    ("185","Jonathan Aranda","Tampa Bay Rays",R),("186","Yanquiel Fernandez","Colorado Rockies",T),("187","Maximo Acosta","Miami Marlins",T),
    ("188","Carlos Narvaez","Boston Red Sox",R),("189","Max Scherzer","Toronto Blue Jays",R),("190","Grant Taylor","Chicago White Sox",T),
    ("191","Sal Frelick","Milwaukee Brewers",R),("192","Marcus Semien","New York Mets",R),("193","Cristopher Sanchez","Philadelphia Phillies",R),
    ("194","Cam Smith","Houston Astros",R),("195","Lawrence Butler","Athletics",R),("196","Luis Morales","Athletics",T),
    ("197","Oneil Cruz","Pittsburgh Pirates",R),("198","Jarren Duran","Boston Red Sox",R),("199","Eugenio Suarez","Seattle Mariners",R),
    ("200","Kyle Schwarber","Philadelphia Phillies",R),
]
add_cards(base_id, base)
print(f"  Base: {len(base)} cards")

# ─── BASE - ROOKIE DESIGN VARIATIONS ─────────────────────────────
rdv_id = get_is_id("Base - Rookie Design Variations")
rdv_nums = [13,17,21,23,26,27,28,30,38,41,43,44,48,51,52,56,58,60,65,68,70,74,75,77,79,85,98,99,101,160]
base_lookup = {int(num): (name, team) for num, name, team, _ in base}
for n in rdv_nums:
    name, team = base_lookup[n]
    pid = get_or_create_player(name)
    cur.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 1, ?)",
                (pid, rdv_id, str(n), team))
print(f"  Base - Rookie Design Variations: {len(rdv_nums)} cards")

# ─── CHROME BLACK AUTOGRAPHS (111 cards) ──────────────────────────
cba_id = get_is_id("Chrome Black Autographs")
cba = [
    ("CBA-AF","Alex Freeland","Los Angeles Dodgers",T),("CBA-AGI","Andres Gimenez","Toronto Blue Jays",R),
    ("CBA-AJ","Aaron Judge","New York Yankees",R),("CBA-AM","Andrew McCutchen","Pittsburgh Pirates",R),
    ("CBA-AP","Albert Pujols","St. Louis Cardinals",R),("CBA-ARA","Agustin Ramirez","Miami Marlins",R),
    ("CBA-BB","Barry Bonds","Pittsburgh Pirates",R),("CBA-BBU","Byron Buxton","Minnesota Twins",R),
    ("CBA-BC","Bubba Chandler","Pittsburgh Pirates",T),("CBA-BE","Bryce Eldridge","San Francisco Giants",T),
    ("CBA-BH","Brady House","Washington Nationals",T),("CBA-BM","Brice Matthews","Houston Astros",T),
    ("CBA-BR","Brent Rooker","Athletics",R),("CBA-BT","Brice Turang","Milwaukee Brewers",R),
    ("CBA-BW","Bryan Woo","Seattle Mariners",R),("CBA-BZ","Barry Zito","Oakland Athletics",R),
    ("CBA-CA","CJ Abrams","Washington Nationals",R),("CBA-CAG","Jac Caglianone","Kansas City Royals",T),
    ("CBA-CB","Chase Burns","Cincinnati Reds",T),("CBA-CBL","Charlie Blackmon","Colorado Rockies",R),
    ("CBA-CC","Corbin Carroll","Arizona Diamondbacks",R),("CBA-CD","Chase Dollander","Colorado Rockies",R),
    ("CBA-CDE","Chase DeLauter","Cleveland Guardians",R),("CBA-CF","Cody Freeman","Texas Rangers",T),
    ("CBA-CH","Cade Horton","Chicago Cubs",R),("CBA-CJ","C.J. Kayfus","Cleveland Guardians",T),
    ("CBA-CM","Christian Moore","Los Angeles Angels",T),("CBA-CME","Chase Meidroth","Chicago White Sox",R),
    ("CBA-CMO","Colson Montgomery","Chicago White Sox",T),("CBA-CR","Cal Raleigh","Seattle Mariners",R),
    ("CBA-CT","Colby Thomas","Athletics",T),("CBA-CWH","Carson Whisenhunt","San Francisco Giants",T),
    ("CBA-CY","Cole Young","Seattle Mariners",T),("CBA-CYE","Christian Yelich","Milwaukee Brewers",R),
    ("CBA-DB","Drake Baldwin","Atlanta Braves",R),("CBA-DBE","Dylan Beavers","Baltimore Orioles",T),
    ("CBA-DF","Didier Fuentes","Atlanta Braves",R),("CBA-DG","Dwight Gooden","New York Mets",R),
    ("CBA-DGI","Drew Gilbert","San Francisco Giants",T),("CBA-DJ","Derek Jeter","New York Yankees",R),
    ("CBA-DL","Derrek Lee","Chicago Cubs",R),("CBA-DR","Dalton Rushing","Los Angeles Dodgers",R),
    ("CBA-DW","Dave Winfield","San Diego Padres",R),("CBA-ED","Elly De La Cruz","Cincinnati Reds",R),
    ("CBA-EM","Eddie Murray","Baltimore Orioles",R),("CBA-EQ","Edgar Quero","Chicago White Sox",R),
    ("CBA-FT","Frank Thomas","Chicago White Sox",R),("CBA-FTJ","Fernando Tatis Jr.","San Diego Padres",R),
    ("CBA-HK","Hyeseong Kim","Los Angeles Dodgers",R),("CBA-HP","Hunter Pence","San Francisco Giants",R),
    ("CBA-HR","Hanley Ramirez","Florida Marlins",R),("CBA-IC","Isaac Collins","Milwaukee Brewers",R),
    ("CBA-JA","Jonathan Aranda","Tampa Bay Rays",R),("CBA-JB","Johnny Bench","Cincinnati Reds",R),
    ("CBA-JCA","Jose Canseco","Oakland Athletics",R),("CBA-JCJ","Jazz Chisholm Jr.","New York Yankees",R),
    ("CBA-JD","Jasson Dominguez","New York Yankees",R),("CBA-JDA","Johnny Damon","Tampa Bay Rays",R),
    ("CBA-JI","Jimmy Crooks","St. Louis Cardinals",T),("CBA-JLE","Jack Leiter","Texas Rangers",R),
    ("CBA-JM","Jacob Melton","Houston Astros",T),("CBA-JMA","Jakob Marsee","Miami Marlins",T),
    ("CBA-JMI","Jacob Misiorowski","Milwaukee Brewers",T),("CBA-JR","Julio Rodriguez","Seattle Mariners",R),
    ("CBA-JRE","Jose Reyes","New York Mets",R),("CBA-JRO","Jimmy Rollins","Philadelphia Phillies",R),
    ("CBA-JS","Johan Santana","New York Mets",R),("CBA-JT","Jonah Tong","New York Mets",T),
    ("CBA-JWE","Jordan Westburg","Baltimore Orioles",R),("CBA-KCA","Kristian Campbell","Boston Red Sox",R),
    ("CBA-KK","Kyle Karros","Colorado Rockies",T),("CBA-KO","Kazuma Okamoto","Toronto Blue Jays",R),
    ("CBA-KS","Kodai Senga","New York Mets",R),("CBA-KW","Kerry Wood","Chicago Cubs",R),
    ("CBA-LA","Luis Arraez","San Diego Padres",R),("CBA-LG","Luis Gonzalez","Arizona Diamondbacks",R),
    ("CBA-LW","Logan Webb","San Francisco Giants",R),("CBA-LWA","Larry Walker","Colorado Rockies",R),
    ("CBA-MHA","Michael Harris II","Atlanta Braves",R),("CBA-MM","Mark McGwire","St. Louis Cardinals",R),
    ("CBA-MT","Mike Trout","Los Angeles Angels",R),("CBA-MU","Munetaka Murakami","Chicago White Sox",R),
    ("CBA-NC","Nathan Church","St. Louis Cardinals",T),("CBA-NK","Nick Kurtz","Athletics",R),
    ("CBA-NM","Nolan McLean","New York Mets",T),("CBA-OC","Owen Caissie","Chicago Cubs",T),
    ("CBA-OH","Orlando Hernandez","New York Yankees",R),("CBA-OK","Otto Kemp","Philadelphia Phillies",T),
    ("CBA-PO","Paul O'Neill","New York Yankees",R),("CBA-PS","Paul Skenes","Pittsburgh Pirates",R),
    ("CBA-RA","Roman Anthony","Boston Red Sox",T),("CBA-RAJ","Ronald Acuna Jr.","Atlanta Braves",R),
    ("CBA-RAR","Randy Arozarena","Seattle Mariners",R),("CBA-RRI","Ryan Ritter","Colorado Rockies",T),
    ("CBA-RS","Roki Sasaki","Los Angeles Dodgers",R),("CBA-SB","Samuel Basallo","Baltimore Orioles",T),
    ("CBA-SC","Cam Schlittler","New York Yankees",T),("CBA-SK","Sandy Koufax","Los Angeles Dodgers",R),
    ("CBA-SOG","Shinnosuke Ogasawara","Washington Nationals",T),("CBA-SS","Sal Stewart","Cincinnati Reds",T),
    ("CBA-TI","Tatsuya Imai","Houston Astros",R),("CBA-TM","Troy Melton","Detroit Tigers",T),
    ("CBA-TS","Ted Simmons","St. Louis Cardinals",R),("CBA-TY","Trey Yesavage","Toronto Blue Jays",T),
    ("CBA-VG","Vladimir Guerrero Jr.","Toronto Blue Jays",R),("CBA-VW","Vernon Wells","Toronto Blue Jays",R),
    ("CBA-WB","Wade Boggs","Boston Red Sox",R),("CBA-WBE","Warming Bernabel","Colorado Rockies",T),
    ("CBA-WC","Will Clark","San Francisco Giants",R),("CBA-YF","Yanquiel Fernandez","Colorado Rockies",T),
    ("CBA-ZNE","Zach Neto","Los Angeles Angels",R),
]
add_cards(cba_id, cba)
print(f"  Chrome Black Autographs: {len(cba)} cards")

# ─── IVORY AUTOGRAPHS (36 cards) ──────────────────────────────────
iva_id = get_is_id("Ivory Autographs")
iva = [
    ("IVA-BB","Barry Bonds","San Francisco Giants",R),("IVA-BC","Bubba Chandler","Pittsburgh Pirates",T),
    ("IVA-CB","Chase Burns","Cincinnati Reds",T),("IVA-CJ","Chipper Jones","Atlanta Braves",R),
    ("IVA-CM","Christian Moore","Los Angeles Angels",T),("IVA-CS","CC Sabathia","New York Yankees",R),
    ("IVA-DJ","Derek Jeter","New York Yankees",R),("IVA-DM","Dale Murphy","Atlanta Braves",R),
    ("IVA-DMA","Don Mattingly","New York Yankees",R),("IVA-DO","David Ortiz","Boston Red Sox",R),
    ("IVA-FT","Fernando Tatis Jr.","San Diego Padres",R),("IVA-GB","George Brett","Kansas City Royals",R),
    ("IVA-I","Ichiro","Seattle Mariners",R),("IVA-JC","Jac Caglianone","Kansas City Royals",T),
    ("IVA-JS","Juan Soto","New York Mets",R),("IVA-JV","Joey Votto","Cincinnati Reds",R),
    ("IVA-KC","Kristian Campbell","Boston Red Sox",R),("IVA-KT","Kyle Teel","Chicago White Sox",T),
    ("IVA-MC","Miguel Cabrera","Florida Marlins",R),("IVA-MM","Mark McGwire","St. Louis Cardinals",R),
    ("IVA-MS","Mike Schmidt","Philadelphia Phillies",R),("IVA-NR","Nolan Ryan","Texas Rangers",R),
    ("IVA-OC","Owen Caissie","Chicago Cubs",T),("IVA-OH","Orel Hershiser","Los Angeles Dodgers",R),
    ("IVA-RA","Ronald Acuna Jr.","Atlanta Braves",R),("IVA-RAN","Roman Anthony","Boston Red Sox",T),
    ("IVA-RC","Roger Clemens","Boston Red Sox",R),("IVA-RJ","Randy Johnson","Seattle Mariners",R),
    ("IVA-RJA","Reggie Jackson","Oakland Athletics",R),("IVA-RY","Robin Yount","Milwaukee Brewers",R),
    ("IVA-SB","Samuel Basallo","Baltimore Orioles",T),("IVA-SC","Steve Carlton","Philadelphia Phillies",R),
    ("IVA-SK","Sandy Koufax","Brooklyn Dodgers",R),("IVA-SO","Shohei Ohtani","Los Angeles Dodgers",R),
    ("IVA-SS","Sammy Sosa","Chicago Cubs",R),("IVA-YY","Yoshinobu Yamamoto","Los Angeles Dodgers",R),
]
add_cards(iva_id, iva)
print(f"  Ivory Autographs: {len(iva)} cards")

# ─── PITCH BLACK PAIRINGS DUAL AUTOGRAPHS (14 dual cards) ────────
pbp_id = get_is_id("Pitch Black Pairings Dual Autographs")
pbp = [
    ("PDPA-AC","Kristian Campbell","Boston Red Sox","Roman Anthony","Boston Red Sox"),
    ("PDPA-AJ","Chipper Jones","Atlanta Braves","Ronald Acuna Jr.","Atlanta Braves"),
    ("PDPA-BC","Wade Boggs","Boston Red Sox","Roger Clemens","Boston Red Sox"),
    ("PDPA-JG","Ken Griffey Jr.","Seattle Mariners","Randy Johnson","Seattle Mariners"),
    ("PDPA-JI","Ichiro","Seattle Mariners","Derek Jeter","New York Yankees"),
    ("PDPA-KP","Hyeseong Kim","Los Angeles Dodgers","Chan Ho Park","Los Angeles Dodgers"),
    ("PDPA-OY","Yoshinobu Yamamoto","Los Angeles Dodgers","Shohei Ohtani","Los Angeles Dodgers"),
    ("PDPA-PM","Mark McGwire","St. Louis Cardinals","Albert Pujols","St. Louis Cardinals"),
    ("PDPA-SC","Bubba Chandler","Pittsburgh Pirates","Paul Skenes","Pittsburgh Pirates"),
    ("PDPA-SD","Sammy Sosa","Chicago Cubs","Andre Dawson","Chicago Cubs"),
    ("PDPA-TJ","Mike Trout","Los Angeles Angels","Reggie Jackson","Los Angeles Angels"),
    ("PDPA-TK","Frank Thomas","Chicago White Sox","Paul Konerko","Chicago White Sox"),
    ("PDPA-WG","Vladimir Guerrero","Montreal Expos","Larry Walker","Montreal Expos"),
    ("PDPA-WW","Jack Wilson","Pittsburgh Pirates","Jacob Wilson","Athletics"),
]
add_dual_cards(pbp_id, pbp)
print(f"  Pitch Black Pairings: {len(pbp)} dual cards")

# ─── SUPER FUTURES AUTOGRAPHS (22 cards) ──────────────────────────
sfa_id = get_is_id("Super Futures Autographs")
sfa = [
    ("SFA-AF","Alex Freeland","Los Angeles Dodgers",T),("SFA-AR","Agustin Ramirez","Miami Marlins",R),
    ("SFA-BC","Bubba Chandler","Pittsburgh Pirates",T),("SFA-BL","Brooks Lee","Minnesota Twins",R),
    ("SFA-BM","Brice Matthews","Houston Astros",T),("SFA-CAG","Jac Caglianone","Kansas City Royals",T),
    ("SFA-CB","Chase Burns","Cincinnati Reds",T),("SFA-CM","Christian Moore","Los Angeles Angels",T),
    ("SFA-CSI","Chandler Simpson","Tampa Bay Rays",R),("SFA-CY","Cole Young","Seattle Mariners",T),
    ("SFA-DB","Dylan Beavers","Baltimore Orioles",T),("SFA-DR","Dalton Rushing","Los Angeles Dodgers",R),
    ("SFA-JM","Jacob Melton","Houston Astros",T),("SFA-JMA","Jakob Marsee","Miami Marlins",T),
    ("SFA-KC","Kristian Campbell","Boston Red Sox",R),("SFA-KT","Kyle Teel","Chicago White Sox",T),
    ("SFA-NK","Nick Kurtz","Athletics",R),("SFA-NM","Nolan McLean","New York Mets",T),
    ("SFA-OC","Owen Caissie","Chicago Cubs",T),("SFA-RS","Roki Sasaki","Los Angeles Dodgers",R),
    ("SFA-SB","Samuel Basallo","Baltimore Orioles",T),("SFA-SS","Sal Stewart","Cincinnati Reds",T),
]
add_cards(sfa_id, sfa)
print(f"  Super Futures Autographs: {len(sfa)} cards")

# ─── PAINT IT (19 cards) ──────────────────────────────────────────
pi_id = get_is_id("Paint It")
pi = [
    ("PIA-AP","Albert Pujols","St. Louis Cardinals",R),("PIA-BC","Bubba Chandler","Pittsburgh Pirates",T),
    ("PIA-CB","Chase Burns","Cincinnati Reds",T),("PIA-CM","Christian Moore","Los Angeles Angels",T),
    ("PIA-CMO","Colson Montgomery","Chicago White Sox",T),("PIA-CS","CC Sabathia","New York Yankees",R),
    ("PIA-DJ","Derek Jeter","New York Yankees",R),("PIA-GB","George Brett","Kansas City Royals",R),
    ("PIA-I","Ichiro","Seattle Mariners",R),("PIA-JC","Jac Caglianone","Kansas City Royals",T),
    ("PIA-KC","Kristian Campbell","Boston Red Sox",R),("PIA-KS","Kodai Senga","New York Mets",R),
    ("PIA-KT","Kyle Teel","Chicago White Sox",T),("PIA-MT","Mike Trout","Los Angeles Angels",R),
    ("PIA-NK","Nick Kurtz","Athletics",R),("PIA-NR","Nolan Ryan","Texas Rangers",R),
    ("PIA-OC","Owen Caissie","Chicago Cubs",T),("PIA-RAN","Roman Anthony","Boston Red Sox",T),
    ("PIA-YY","Yoshinobu Yamamoto","Los Angeles Dodgers",R),
]
add_cards(pi_id, pi)
print(f"  Paint It: {len(pi)} cards")

# ─── Generate slugs ──────────────────────────────────────────────
def slugify(text):
    s = text.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_]+', '-', s)
    return re.sub(r'-+', '-', s).strip('-')

cur.execute("SELECT id, name FROM players WHERE set_id = ? AND slug IS NULL", (SET_ID,))
new_players = cur.fetchall()
existing_slugs = set(r[0] for r in cur.execute("SELECT slug FROM players WHERE set_id = ? AND slug IS NOT NULL", (SET_ID,)).fetchall())
for pid, pname in new_players:
    slug = slugify(pname)
    if slug in existing_slugs:
        i = 2
        while f"{slug}-{i}" in existing_slugs: i += 1
        slug = f"{slug}-{i}"
    existing_slugs.add(slug)
    cur.execute("UPDATE players SET slug = ? WHERE id = ?", (slug, pid))

conn.commit()
player_count = cur.execute("SELECT COUNT(*) FROM players WHERE set_id = ?", (SET_ID,)).fetchone()[0]
app_count = cur.execute("SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON pa.insert_set_id = i.id WHERE i.set_id = ?", (SET_ID,)).fetchone()[0]
print(f"\nDone! Set ID: {SET_ID}")
print(f"  Players: {player_count}")
print(f"  Appearances: {app_count}")
conn.close()
