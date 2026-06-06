"""
Backfill 686 autograph and relic cards for 2025-26 Topps Motif Basketball (set 851).
All 22 subsets already exist as shells with parallels attached.
Usage: python3 scripts/backfill_motif_basketball_cards.py
"""
import sqlite3, os, re, unicodedata

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
db = sqlite3.connect(DB_PATH)
db.execute("PRAGMA journal_mode=WAL")
db.execute("PRAGMA foreign_keys=ON")

SET_ID = 851

# Build subset ID map from existing shells
subset_map = {}
for row in db.execute("SELECT id, name FROM insert_sets WHERE set_id = ?", (SET_ID,)).fetchall():
    subset_map[row[1]] = row[0]
print(f"Found {len(subset_map)} subsets for set {SET_ID}")

def slugify(t):
    s = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode('ascii')
    s = s.lower().strip(); s = re.sub(r'[^\w\s-]', '', s); s = re.sub(r'[\s_]+', '-', s)
    return re.sub(r'-+', '-', s).strip('-')

_sc = {}
def goc(name):
    name = name.strip()
    row = db.execute("SELECT id FROM players WHERE set_id = ? AND name = ?", (SET_ID, name)).fetchone()
    if row: return row[0]
    slug = slugify(name)
    if not _sc:
        for r in db.execute("SELECT slug FROM players WHERE set_id = ? AND slug IS NOT NULL", (SET_ID,)).fetchall():
            _sc[r[0]] = True
    c = slug; i = 2
    while c in _sc: c = f"{slug}-{i}"; i += 1
    _sc[c] = True
    db.execute("INSERT INTO players (set_id, name, slug, unique_cards, total_print_run, one_of_ones, insert_set_count, subject_role) VALUES (?, ?, ?, 0, 0, 0, 0, 'athlete')",
               (SET_ID, name, c))
    return db.execute("SELECT last_insert_rowid()").fetchone()[0]

def ins(subset_name, cards):
    is_id = subset_map[subset_name]
    for num, name, team, rc in cards:
        pid = goc(name)
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)",
                   (pid, is_id, str(num), 1 if rc else 0, team))
    print(f"  {subset_name}: {len(cards)} cards")

def ins_dual(subset_name, cards):
    is_id = subset_map[subset_name]
    for num, n1, n2 in cards:
        p1, p2 = goc(n1), goc(n2)
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, NULL)", (p1, is_id, str(num)))
        a = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a, p2))
    print(f"  {subset_name}: {len(cards)} cards (dual)")

def ins_triple(subset_name, cards):
    is_id = subset_map[subset_name]
    for num, n1, n2, n3 in cards:
        pids = [goc(n) for n in [n1, n2, n3]]
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, NULL)", (pids[0], is_id, str(num)))
        a = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        for p in pids[1:]:
            db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a, p))
    print(f"  {subset_name}: {len(cards)} cards (triple)")

R = True; F = False

# ═══ SPLATTER SIGNATURES (36) ═══
ins("Splatter Signatures", [
("SS-AB","Ace Bailey","Utah Jazz",R),("SS-AI","Allen Iverson","Philadelphia 76ers",F),("SS-AS","Alex Sarr","Washington Wizards",F),("SS-BM","Brandon Miller","Charlotte Hornets",F),("SS-CC","Cade Cunningham","Detroit Pistons",F),("SS-CF","Cooper Flagg","Dallas Mavericks",R),("SS-CH","Chet Holmgren","Oklahoma City Thunder",F),("SS-DH","Dylan Harper","San Antonio Spurs",R),("SS-DM","Donovan Mitchell","Cleveland Cavaliers",F),("SS-DN","Dirk Nowitzki","Dallas Mavericks",F),
("SS-DW","Dwyane Wade","Miami Heat",F),("SS-ED","Egor D\u00ebmin","Brooklyn Nets",R),("SS-JB","Jalen Brunson","New York Knicks",F),("SS-JG","Jalen Green","Phoenix Suns",F),("SS-JT","Jayson Tatum","Boston Celtics",F),("SS-JW","Jalen Williams","Oklahoma City Thunder",F),("SS-KAT","Karl-Anthony Towns","New York Knicks",F),("SS-KD","Kevin Durant","Houston Rockets",F),("SS-KG","Kevin Garnett","Boston Celtics",F),("SS-KK","Kon Knueppel","Charlotte Hornets",R),
("SS-LB","Larry Bird","Boston Celtics",F),("SS-LBJ","LeBron James","Los Angeles Lakers",F),("SS-MJ","Magic Johnson","Los Angeles Lakers",F),("SS-NJ","Nikola Joki\u0107","Denver Nuggets",F),("SS-PB","Paolo Banchero","Orlando Magic",F),("SS-PS","Pascal Siakam","Indiana Pacers",F),("SS-SC","Stephen Curry","Golden State Warriors",F),("SS-SGA","Shai Gilgeous-Alexander","Oklahoma City Thunder",F),("SS-SO","Shaquille O'Neal","Los Angeles Lakers",F),("SS-STC","Stephon Castle","San Antonio Spurs",F),
("SS-TH","Tyrese Haliburton","Indiana Pacers",F),("SS-TM","Tyrese Maxey","Philadelphia 76ers",F),("SS-TMG","Tracy McGrady","Houston Rockets",F),("SS-VC","Vince Carter","Toronto Raptors",F),("SS-VW","Victor Wembanyama","San Antonio Spurs",F),("SS-ZR","Zaccharie Risacher","Atlanta Hawks",F),
])

# ═══ STATISTICAL SHOWPIECE SIGNATURES (30) ═══
ins("Statistical Showpiece Signatures", [
("STAT-AI","Allen Iverson","Philadelphia 76ers",F),("STAT-AM","Alonzo Mourning","Miami Heat",F),("STAT-CP","Chris Paul","Los Angeles Clippers",F),("STAT-DM","Donovan Mitchell","Cleveland Cavaliers",F),("STAT-DN","Dirk Nowitzki","Dallas Mavericks",F),("STAT-DOW","Dominique Wilkins","Atlanta Hawks",F),("STAT-DR","Dennis Rodman","Chicago Bulls",F),("STAT-DW","Dwyane Wade","Miami Heat",F),("STAT-GH","Grant Hill","Detroit Pistons",F),("STAT-HO","Hakeem Olajuwon","Houston Rockets",F),
("STAT-JH","James Harden","Los Angeles Clippers",F),("STAT-JS","John Stockton","Utah Jazz",F),("STAT-KD","Kevin Durant","Houston Rockets",F),("STAT-KG","Kevin Garnett","Boston Celtics",F),("STAT-LB","Larry Bird","Boston Celtics",F),("STAT-LBJ","LeBron James","Los Angeles Lakers",F),("STAT-MG","Manu Ginobili","San Antonio Spurs",F),("STAT-MJ","Magic Johnson","Los Angeles Lakers",F),("STAT-PP","Paul Pierce","Boston Celtics",F),("STAT-RA","Ray Allen","Boston Celtics",F),
("STAT-RB","Rick Barry","Golden State Warriors",F),("STAT-RP","Robert Parish","Boston Celtics",F),("STAT-SC","Stephen Curry","Golden State Warriors",F),("STAT-SO","Shaquille O'Neal","Los Angeles Lakers",F),("STAT-TM","Tracy McGrady","Houston Rockets",F),("STAT-VC","Vince Carter","Toronto Raptors",F),("STAT-VW","Victor Wembanyama","San Antonio Spurs",F),("STAT-ZL","Zach Lavine","Sacramento Kings",F),("STAT-ZR","Zaccharie Risacher","Atlanta Hawks",F),("STAT-ZRA","Zach Randolph","Memphis Grizzlies",F),
])

# ═══ APPRENTICE NUMERICAL AUTOGRAPHS (30, all RC) ═══
ins("Apprentice Numerical Autographs", [
("APNA-AB","Ace Bailey","Utah Jazz",R),("APNA-AN","Asa Newell","Atlanta Hawks",R),("APNA-AT","Adou Thiero","Los Angeles Lakers",R),("APNA-BS","Ben Saraf","Brooklyn Nets",R),("APNA-CC","Cedric Coward","Memphis Grizzlies",R),("APNA-CF","Cooper Flagg","Dallas Mavericks",R),("APNA-CMB","Collin Murray-Boyles","Toronto Raptors",R),("APNA-DH","Dylan Harper","San Antonio Spurs",R),("APNA-DP","Drake Powell","Brooklyn Nets",R),("APNA-DQ","Derik Queen","New Orleans Pelicans",R),
("APNA-DW","Danny Wolf","Brooklyn Nets",R),("APNA-ED","Egor D\u00ebmin","Brooklyn Nets",R),("APNA-JB","Joan Beringer","Minnesota Timberwolves",R),("APNA-JBR","Johni Broome","Philadelphia 76ers",R),("APNA-JR","Jase Richardson","Orlando Magic",R),("APNA-KJ","Kasparas Jaku\u010dionis","Miami Heat",R),("APNA-KK","Kon Knueppel","Charlotte Hornets",R),("APNA-KM","Khaman Maluach","Phoenix Suns",R),("APNA-NC","Nique Clifford","Sacramento Kings",R),("APNA-NE","Noa Essengue","Chicago Bulls",R),
("APNA-NP","Noah Penda","Orlando Magic",R),("APNA-NT","Nolan Traore","Brooklyn Nets",R),("APNA-RF","Rasheer Fleming","Phoenix Suns",R),("APNA-RK","Ryan Kalkbrenner","Charlotte Hornets",R),("APNA-SJ","Sion James","Charlotte Hornets",R),("APNA-TP","Tyrese Proctor","Cleveland Cavaliers",R),("APNA-TS","Thomas Sorber","Oklahoma City Thunder",R),("APNA-WCJ","Walter Clayton Jr.","Utah Jazz",R),("APNA-WR","Will Riley","Washington Wizards",R),("APNA-YH","Yang Hansen","Portland Trail Blazers",R),
])

# ═══ ABSTRACT INK SIGNATURES (40) ═══
ins("Abstract Ink Signatures", [
("AIS-AB","Ace Bailey","Utah Jazz",R),("AIS-AH","Anfernee Hardaway","Orlando Magic",F),("AIS-AM","Alonzo Mourning","Miami Heat",F),("AIS-AN","Aaron Nesmith","Indiana Pacers",F),("AIS-AT","Adou Thiero","Los Angeles Lakers",R),("AIS-BS","Ben Saraf","Brooklyn Nets",R),("AIS-BSM","Baylor Scheierman","Boston Celtics",F),("AIS-CS","Collin Sexton","Charlotte Hornets",F),("AIS-DW","Danny Wolf","Brooklyn Nets",R),("AIS-DWH","Derrick White","Boston Celtics",F),
("AIS-FW","Franz Wagner","Orlando Magic",F),("AIS-GG","George Gervin","San Antonio Spurs",F),("AIS-GT","Gary Trent Jr.","Milwaukee Bucks",F),("AIS-JB","Johni Broome","Philadelphia 76ers",R),("AIS-JH","Juwan Howard","Washington Bullets",F),("AIS-JJJ","Jaren Jackson Jr.","Memphis Grizzlies",F),("AIS-JK","Jason Kidd","Dallas Mavericks",F),("AIS-JP","Jordan Poole","New Orleans Pelicans",F),("AIS-JR","Jase Richardson","Orlando Magic",R),("AIS-JW","Jalen Williams","Oklahoma City Thunder",F),
("AIS-KM","Khris Middleton","Washington Wizards",F),("AIS-KP","Kristaps Porzingis","Atlanta Hawks",F),("AIS-NP","Noah Penda","Orlando Magic",R),("AIS-PAP","Paul Pierce","Boston Celtics",F),("AIS-PAU","Pau Gasol","Los Angeles Lakers",F),("AIS-PP","Payton Pritchard","Boston Celtics",F),("AIS-RA","Ray Allen","Seattle Supersonics",F),("AIS-RB","Rick Barry","Golden State Warriors",F),("AIS-RD","Rob Dillingham","Minnesota Timberwolves",F),("AIS-RF","Rasheer Fleming","Phoenix Suns",R),
("AIS-RH","Ron Holland II","Detroit Pistons",F),("AIS-RK","Ryan Kalkbrenner","Charlotte Hornets",R),("AIS-SJ","Sion James","Charlotte Hornets",R),("AIS-TDS","Tristan da Silva","Orlando Magic",F),("AIS-TM","Terance Mann","Brooklyn Nets",F),("AIS-TMX","Tyrese Maxey","Philadelphia 76ers",F),("AIS-TP","Tony Parker","San Antonio Spurs",F),("AIS-TS","Terrence Shannon Jr.","Minnesota Timberwolves",F),("AIS-YM","Yves Missi","New Orleans Pelicans",F),("AIS-ZE","Zach Edey","Memphis Grizzlies",F),
])

# ═══ ACRYLIC DRIP AUTOGRAPHS (39) ═══
ins("Acrylic Drip Autographs", [
("ADA-AN","Asa Newell","Atlanta Hawks",R),("ADA-ANE","Herbert Jones","New Orleans Pelicans",F),("ADA-ANS","Anfernee Simons","Boston Celtics",F),("ADA-AS","Alperen Sengun","Houston Rockets",F),("ADA-AT","Adou Thiero","Los Angeles Lakers",R),("ADA-BS","Ben Saraf","Brooklyn Nets",R),("ADA-CD","Clyde Drexler","Portland Trail Blazers",F),("ADA-CJ","Cameron Johnson","Denver Nuggets",F),("ADA-DB","Desmond Bane","Orlando Magic",F),("ADA-DD","Donte DiVincenzo","Minnesota Timberwolves",F),
("ADA-DHA","Dylan Harper","San Antonio Spurs",R),("ADA-DHU","De'Andre Hunter","Cleveland Cavaliers",F),("ADA-DP","Drake Powell","Brooklyn Nets",R),("ADA-DW","Danny Wolf","Brooklyn Nets",R),("ADA-DWI","Dominique Wilkins","Atlanta Hawks",F),("ADA-GH","Grant Hill","Detroit Pistons",F),("ADA-HO","Hakeem Olajuwon","Houston Rockets",F),("ADA-IC","Isaiah Collier","Utah Jazz",F),("ADA-JA","Jarrett Allen","Cleveland Cavaliers",F),("ADA-JB","Johni Broome","Philadelphia 76ers",R),
("ADA-JH","Jrue Holiday","Portland Trail Blazers",F),("ADA-JR","Jase Richardson","Orlando Magic",R),("ADA-JRO","Jalen Rose","Indiana Pacers",F),("ADA-JS","John Stockton","Utah Jazz",F),("ADA-JW","Jason Williams","Sacramento Kings",F),("ADA-KH","Kevin Huerter","Chicago Bulls",F),("ADA-KJ","Kasparas Jaku\u010dionis","Miami Heat",R),("ADA-MT","Myles Turner","Milwaukee Bucks",F),("ADA-NC","Nique Clifford","Sacramento Kings",R),("ADA-NP","Noah Penda","Orlando Magic",R),
("ADA-NR","Naz Reid","Minnesota Timberwolves",F),("ADA-RF","Rasheer Fleming","Phoenix Suns",R),("ADA-RG","Rudy Gobert","Minnesota Timberwolves",F),("ADA-RH","Rip Hamilton","Detroit Pistons",F),("ADA-RK","Ryan Kalkbrenner","Charlotte Hornets",R),("ADA-RP","Robert Parish","Boston Celtics",F),("ADA-SJ","Sion James","Charlotte Hornets",R),("ADA-TK","Tyler Kolek","New York Knicks",F),("ADA-WR","Will Riley","Washington Wizards",R),
])

# ═══ STILL LIFE SIGNATURES (20) ═══
ins("Still Life Signatures", [
("SLS-AB","Ace Bailey","Utah Jazz",R),("SLS-AG","Aaron Gordon","Denver Nuggets",F),("SLS-CA","Carmelo Anthony","New York Knicks",F),("SLS-CC","Cedric Coward","Memphis Grizzlies",R),("SLS-CF","Cooper Flagg","Dallas Mavericks",R),("SLS-CMB","Collin Murray-Boyles","Toronto Raptors",R),("SLS-DH","Dylan Harper","San Antonio Spurs",R),("SLS-DHO","Dwight Howard","Orlando Magic",F),("SLS-DQ","Derik Queen","New Orleans Pelicans",R),("SLS-DR","David Robinson","San Antonio Spurs",F),
("SLS-ED","Egor D\u00ebmin","Brooklyn Nets",R),("SLS-KD","Kevin Durant","Houston Rockets",F),("SLS-KK","Kon Knueppel","Charlotte Hornets",R),("SLS-KM","Khaman Maluach","Phoenix Suns",R),("SLS-NE","Noa Essengue","Chicago Bulls",R),("SLS-PB","Paolo Banchero","Orlando Magic",F),("SLS-RW","Rasheed Wallace","Detroit Pistons",F),("SLS-SC","Stephon Castle","San Antonio Spurs",F),("SLS-VC","Vince Carter","Toronto Raptors",F),("SLS-VW","Victor Wembanyama","San Antonio Spurs",F),
])

# ═══ AQUARELLE AUTOGRAPHS (49) ═══
ins("Aquarelle Autographs", [
("AA-AC","Alex Caruso","Oklahoma City Thunder",F),("AA-AH","Al Horford","Golden State Warriors",F),("AA-AN","Asa Newell","Atlanta Hawks",R),("AA-AT","Adou Thiero","Los Angeles Lakers",R),("AA-BC","Bilal Coulibaly","Washington Wizards",F),("AA-BS","Ben Saraf","Brooklyn Nets",R),("AA-CH","Chet Holmgren","Oklahoma City Thunder",F),("AA-DH","DaRon Holmes II","Denver Nuggets",F),("AA-DL","Dereck Lively II","Dallas Mavericks",F),("AA-DP","Drake Powell","Brooklyn Nets",R),
("AA-DQ","Derik Queen","New Orleans Pelicans",R),("AA-DT","David Thompson","Denver Nuggets",F),("AA-DW","Danny Wolf","Brooklyn Nets",R),("AA-DWI","Deron Williams","Brooklyn Nets",F),("AA-GH","Gordon Hayward","Utah Jazz",F),("AA-JB","Joan Beringer","Minnesota Timberwolves",R),("AA-JBR","Johni Broome","Philadelphia 76ers",R),("AA-JH","James Harden","Los Angeles Clippers",F),("AA-JHA","Josh Hart","New York Knicks",F),("AA-JL","Jake LaRavia","Los Angeles Lakers",F),
("AA-JR","Jase Richardson","Orlando Magic",R),("AA-JRO","Jalen Rose","Indiana Pacers",F),("AA-KAT","Karl-Anthony Towns","New York Knicks",F),("AA-KG","Kyshawn George","Washington Wizards",F),("AA-KJ","Kasparas Jaku\u010dionis","Miami Heat",R),("AA-KK","Kon Knueppel","Charlotte Hornets",R),("AA-KM","Kris Murray","Portland Trail Blazers",F),("AA-KW","Kel'el Ware","Miami Heat",F),("AA-LB","Larry Bird","Boston Celtics",F),("AA-LM","Lauri Markkanen","Utah Jazz",F),
("AA-ME","Monta Ellis","Golden State Warriors",F),("AA-MPJ","Michael Porter Jr.","Brooklyn Nets",F),("AA-MWP","Metta World Peace","Los Angeles Lakers",F),("AA-NC","Nique Clifford","Sacramento Kings",R),("AA-NP","Noah Penda","Orlando Magic",R),("AA-NT","Nolan Traore","Brooklyn Nets",R),("AA-OT","Obi Toppin","Indiana Pacers",F),("AA-PA","Precious Achiuwa","Sacramento Kings",F),("AA-PP","Paul Pierce","Boston Celtics",F),("AA-RD","Ryan Dunn","Phoenix Suns",F),
("AA-RF","Rasheer Fleming","Phoenix Suns",R),("AA-RK","Ryan Kalkbrenner","Charlotte Hornets",R),("AA-SJ","Sion James","Charlotte Hornets",R),("AA-TH","Tim Hardaway","Golden State Warriors",F),("AA-TS","Thomas Sorber","Oklahoma City Thunder",R),("AA-TYH","Tyrese Haliburton","Indiana Pacers",F),("AA-WCJ","Walter Clayton Jr.","Utah Jazz",R),("AA-YH","Yang Hansen","Portland Trail Blazers",R),("AA-ZR","Zach Randolph","Memphis Grizzlies",F),
])

# ═══ DECO-RATED AUTOGRAPHS (49) ═══
ins("Deco-Rated Autographs", [
("DR-AB","Ace Bailey","Utah Jazz",R),("DR-AJJ","AJ Johnson","Washington Wizards",F),("DR-AN","Asa Newell","Atlanta Hawks",R),("DR-ANE","T.J. McConnell","Indiana Pacers",F),("DR-ANS","Aaron Nesmith","Indiana Pacers",F),("DR-AT","Adou Thiero","Los Angeles Lakers",R),("DR-BS","Ben Saraf","Brooklyn Nets",R),("DR-CD","Clyde Drexler","Portland Trail Blazers",F),("DR-CL","Chaz Lanier","Detroit Pistons",R),("DR-DG","Daniel Gafford","Dallas Mavericks",F),
("DR-DJJ","Derrick Jones Jr.","Los Angeles Clippers",F),("DR-DM","Donovan Mitchell","Cleveland Cavaliers",F),("DR-DN","Dirk Nowitzki","Dallas Mavericks",F),("DR-DP","Drake Powell","Brooklyn Nets",R),("DR-DW","Danny Wolf","Brooklyn Nets",R),("DR-GW","Grant Williams","Charlotte Hornets",F),("DR-JB","Johni Broome","Philadelphia 76ers",R),("DR-JBE","Joan Beringer","Minnesota Timberwolves",R),("DR-JG","Jalen Green","Phoenix Suns",F),("DR-JH","Josh Hart","New York Knicks",F),
("DR-JK","Jason Kidd","New Jersey Nets",F),("DR-JR","Jase Richardson","Orlando Magic",R),("DR-JS","Jerry Stackhouse","Dallas Mavericks",F),("DR-JT","Jayson Tatum","Boston Celtics",F),("DR-KG","Kyshawn George","Washington Wizards",F),("DR-MW","Mark Williams","Phoenix Suns",F),("DR-NC","Nic Claxton","Brooklyn Nets",F),("DR-NCL","Nique Clifford","Sacramento Kings",R),("DR-NP","Noah Penda","Orlando Magic",R),("DR-NT","Nolan Traore","Brooklyn Nets",R),
("DR-NTO","Nikola Topi\u0107","Oklahoma City Thunder",F),("DR-PS","Peja Stojakovic","Sacramento Kings",F),("DR-QG","Quentin Grimes","Philadelphia 76ers",F),("DR-RA","Ray Allen","Miami Heat",F),("DR-RB","Rick Barry","Golden State Warriors",F),("DR-RF","Rasheer Fleming","Phoenix Suns",R),("DR-RH","Rip Hamilton","Detroit Pistons",F),("DR-RJ","Richard Jefferson","New Jersey Nets",F),("DR-RK","Ryan Kalkbrenner","Charlotte Hornets",R),("DR-SD","Spencer Dinwiddie","Charlotte Hornets",F),
("DR-SJ","Sion James","Charlotte Hornets",R),("DR-THJ","Tim Hardaway Jr.","Denver Nuggets",F),("DR-TP","Tony Parker","San Antonio Spurs",F),("DR-TS","Thomas Sorber","Oklahoma City Thunder",R),("DR-WCJ","Walter Clayton Jr.","Utah Jazz",R),("DR-WR","Will Riley","Washington Wizards",R),("DR-YH","Yang Hansen","Portland Trail Blazers",R),("DR-ZE","Zach Edey","Memphis Grizzlies",F),("DR-ZR","Zach Randolph","Memphis Grizzlies",F),
])

# ═══ PICK AND POP ART SIGNATURES (30) ═══
ins("Pick and Pop Art Signatures", [
("PPA-AH","Anfernee Hardaway","Orlando Magic",F),("PPA-AT","Adou Thiero","Los Angeles Lakers",R),("PPA-BOG","Bogdan Bogdanovi\u0107","Los Angeles Clippers",F),("PPA-BS","Ben Saraf","Brooklyn Nets",R),("PPA-CA","Cole Anthony","Milwaukee Bucks",F),("PPA-CC","Clint Capela","Houston Rockets",F),("PPA-CL","Chaz Lanier","Detroit Pistons",R),("PPA-DF","De'Aaron Fox","San Antonio Spurs",F),("PPA-DR","Dennis Rodman","Chicago Bulls",F),("PPA-DS","Domantas Sabonis","Sacramento Kings",F),
("PPA-DW","Dwyane Wade","Miami Heat",F),("PPA-DWO","Danny Wolf","Brooklyn Nets",R),("PPA-FVV","Fred VanVleet","Houston Rockets",F),("PPA-JB","Jalen Brunson","New York Knicks",F),("PPA-JBR","Johni Broome","Philadelphia 76ers",R),("PPA-JC","Jordan Clarkson","New York Knicks",F),("PPA-JR","Jase Richardson","Orlando Magic",R),("PPA-JS","Julian Strawther","Denver Nuggets",F),("PPA-JW","Jason Williams","Memphis Grizzlies",F),("PPA-JWI","Jalen Williams","Oklahoma City Thunder",F),
("PPA-MJ","Magic Johnson","Los Angeles Lakers",F),("PPA-NP","Noah Penda","Orlando Magic",R),("PPA-RF","Rasheer Fleming","Phoenix Suns",R),("PPA-RK","Ryan Kalkbrenner","Charlotte Hornets",R),("PPA-SC","Stephen Curry","Golden State Warriors",F),("PPA-SJ","Sion James","Charlotte Hornets",R),("PPA-TM","Tyrese Maxey","Philadelphia 76ers",F),("PPA-VW","Victor Wembanyama","San Antonio Spurs",F),("PPA-ZL","Zach Lavine","Sacramento Kings",F),("PPA-ZR","Zaccharie Risacher","Atlanta Hawks",F),
])

# ═══ CHARCOAL SIGNATURES (30) ═══
ins("Charcoal Signatures", [
("CS-AB","Ace Bailey","Utah Jazz",R),("CS-AI","Allen Iverson","Philadelphia 76ers",F),("CS-AS","Alperen Sengun","Houston Rockets",F),("CS-AT","Alex Toohey","Golden State Warriors",R),("CS-DA","DeAndre Ayton","Los Angeles Lakers",F),("CS-DB","Dillon Brooks","Phoenix Suns",F),("CS-DH","Dylan Harper","San Antonio Spurs",R),("CS-DL","Dereck Lively II","Dallas Mavericks",F),("CS-HO","Hakeem Olajuwon","Houston Rockets",F),("CS-JC","Johnny Furphy","Indiana Pacers",F),
("CS-JG","Jalen Green","Phoenix Suns",F),("CS-JJJ","Jaime Jaquez Jr.","Miami Heat",F),("CS-JK","Jonathan Kuminga","Golden State Warriors",F),("CS-JS","Javon Small","Memphis Grizzlies",R),("CS-JST","Julian Strawther","Denver Nuggets",F),("CS-JT","Jayson Tatum","Boston Celtics",F),("CS-JTO","John Tonje","Utah Jazz",R),("CS-KD","Kevin Durant","Houston Rockets",F),("CS-KK","Kon Knueppel","Charlotte Hornets",R),("CS-LB","Larry Bird","Boston Celtics",F),
("CS-LO","Lachlan Olbrich","Chicago Bulls",R),("CS-MT","Myles Turner","Milwaukee Bucks",F),("CS-PS","Pascal Siakam","Indiana Pacers",F),("CS-SC","Stephon Castle","San Antonio Spurs",F),("CS-SN","Steve Nash","Phoenix Suns",F),("CS-SO","Shaquille O'Neal","Los Angeles Lakers",F),("CS-TP","Tyrese Proctor","Cleveland Cavaliers",R),("CS-TPE","Taelon Peter","Indiana Pacers",R),("CS-WR","Will Richard","Golden State Warriors",R),("CS-ZE","Zach Edey","Memphis Grizzlies",F),
])

# ═══ SPRAY PAINT SIGNATURES (40) ═══
ins("Spray Paint Signatures", [
("SPS-AC","Alex Caruso","Oklahoma City Thunder",F),("SPS-AH","Al Horford","Golden State Warriors",F),("SPS-AM","Alijah Martin","Toronto Raptors",R),("SPS-BB","Brooks Barnhizer","Oklahoma City Thunder",R),("SPS-BJ","Bronny James Jr.","Los Angeles Lakers",F),("SPS-CF","Cooper Flagg","Dallas Mavericks",R),("SPS-CL","Chaz Lanier","Detroit Pistons",R),("SPS-DD","Donte DiVincenzo","Minnesota Timberwolves",F),("SPS-DH","De'Andre Hunter","Cleveland Cavaliers",F),("SPS-DM","Dejounte Murray","New Orleans Pelicans",F),
("SPS-DV","Devin Vassell","San Antonio Spurs",F),("SPS-DW","Dominique Wilkins","Atlanta Hawks",F),("SPS-EH","Elvin Hayes","Houston Rockets",F),("SPS-GD","Gradey Dick","Toronto Raptors",F),("SPS-HJ","Herbert Jones","New Orleans Pelicans",F),("SPS-JA","Jarrett Allen","Cleveland Cavaliers",F),("SPS-JH","Juwan Howard","Washington Wizards",F),("SPS-JK","Jonathan Kuminga","Golden State Warriors",F),("SPS-JM","Jonathan Mogbo","Toronto Raptors",F),("SPS-JMA","Jahmai Mashack","Memphis Grizzlies",R),
("SPS-JS","Jeremy Sochan","San Antonio Spurs",F),("SPS-JT","Jayson Tatum","Boston Celtics",F),("SPS-JW","Jarace Walker","Indiana Pacers",F),("SPS-JWA","Jamir Watkins","Washington Wizards",R),("SPS-KB","Koby Brea","Phoenix Suns",R),("SPS-KCP","Kentavious Caldwell-Pope","Memphis Grizzlies",F),("SPS-KG","Kevin Garnett","Boston Celtics",F),("SPS-KJ","Kam Jones","Indiana Pacers",R),("SPS-KK","Kyle Kuzma","Milwaukee Bucks",F),("SPS-KW","Kel'el Ware","Miami Heat",F),
("SPS-MB","Mikal Bridges","New York Knicks",F),("SPS-MP","Micah Peavy","New Orleans Pelicans",R),("SPS-MPJ","Michael Porter Jr.","Brooklyn Nets",F),("SPS-MR","Maxime Raynaud","Sacramento Kings",R),("SPS-MS","Max Strus","Cleveland Cavaliers",F),("SPS-NS","Nick Smith Jr.","Los Angeles Lakers",F),("SPS-PB","Paolo Banchero","Orlando Magic",F),("SPS-PP","Payton Pritchard","Boston Celtics",F),("SPS-SS","Shaedon Sharpe","Portland Trail Blazers",F),("SPS-TSJ","Terrence Shannon Jr.","Minnesota Timberwolves",F),
])

# ═══ CANVAS CHAMPIONS AUTOGRAPHS (25) ═══
ins("Canvas Champions Autographs", [
("CCA-CH","Chet Holmgren","Oklahoma City Thunder",F),("CCA-DN","Dirk Nowitzki","Dallas Mavericks",F),("CCA-DR","Dennis Rodman","Chicago Bulls",F),("CCA-DW","Dwyane Wade","Miami Heat",F),("CCA-DWI","Derrick White","Boston Celtics",F),("CCA-FVV","Fred VanVleet","Toronto Raptors",F),("CCA-HO","Hakeem Olajuwon","Houston Rockets",F),("CCA-JH","Jrue Holiday","Boston Celtics",F),("CCA-JK","Jason Kidd","Dallas Mavericks",F),("CCA-JM","Jamal Murray","Denver Nuggets",F),
("CCA-JT","Jayson Tatum","Boston Celtics",F),("CCA-JW","Jalen Williams","Oklahoma City Thunder",F),("CCA-JWS","Jamaal Wilkes","Los Angeles Lakers",F),("CCA-KD","Kevin Durant","Golden State Warriors",F),("CCA-KG","Kevin Garnett","Boston Celtics",F),("CCA-LB","Larry Bird","Boston Celtics",F),("CCA-LBJ","LeBron James","Los Angeles Lakers",F),("CCA-MJ","Magic Johnson","Los Angeles Lakers",F),("CCA-PG","Pau Gasol","Los Angeles Lakers",F),("CCA-PP","Paul Pierce","Boston Celtics",F),
("CCA-PS","Pascal Siakam","Toronto Raptors",F),("CCA-RA","Ray Allen","Miami Heat",F),("CCA-SC","Stephen Curry","Golden State Warriors",F),("CCA-SGA","Shai Gilgeous-Alexander","Oklahoma City Thunder",F),("CCA-SO","Shaquille O'Neal","Los Angeles Lakers",F),
])

# ═══ LEGENDS OF THE COURT SIGNATURES (45) ═══
ins("Legends of the Court Signatures", [
("LC-AC","Alex Caruso","Oklahoma City Thunder",F),("LC-AE","Alex English","Denver Nuggets",F),("LC-AH","Al Horford","Golden State Warriors",F),("LC-AI","Allen Iverson","Philadelphia 76ers",F),("LC-AS","Amar'e Stoudemire","Phoenix Suns",F),("LC-BC","Bilal Coulibaly","Washington Wizards",F),("LC-CA","Carmelo Anthony","New York Knicks",F),("LC-CJ","Cameron Johnson","Denver Nuggets",F),("LC-DB","Desmond Bane","Orlando Magic",F),("LC-DC","Devin Carter","Sacramento Kings",F),
("LC-DF","De'Aaron Fox","San Antonio Spurs",F),("LC-DG","Daniel Gafford","Dallas Mavericks",F),("LC-DL","Dereck Lively II","Dallas Mavericks",F),("LC-DM","Donovan Mitchell","Cleveland Cavaliers",F),("LC-DN","Dirk Nowitzki","Dallas Mavericks",F),("LC-DR","D'Angelo Russell","Dallas Mavericks",F),("LC-FW","Franz Wagner","Orlando Magic",F),("LC-GTJ","Gary Trent Jr.","Milwaukee Bucks",F),("LC-JG","Jalen Green","Phoenix Suns",F),("LC-JH","Josh Hart","New York Knicks",F),
("LC-JJJ","Jaime Jaquez Jr.","Miami Heat",F),("LC-JS","Jerry Stackhouse","Detroit Pistons",F),("LC-JSH","Jamal Shead","Toronto Raptors",F),("LC-JT","Jaylon Tyson","Cleveland Cavaliers",F),("LC-JW","Jalen Williams","Oklahoma City Thunder",F),("LC-KAT","Karl-Anthony Towns","New York Knicks",F),("LC-LM","Lauri Markkanen","Utah Jazz",F),("LC-MS","Marcus Smart","Los Angeles Lakers",F),("LC-MT","Myles Turner","Milwaukee Bucks",F),("LC-MWP","Metta World Peace","Los Angeles Lakers",F),
("LC-NR","Naz Reid","Minnesota Timberwolves",F),("LC-PP","Paul Pierce","Boston Celtics",F),("LC-RA","Ray Allen","Seattle Supersonics",F),("LC-RH","Rip Hamilton","Detroit Pistons",F),("LC-RHO","Ron Holland II","Detroit Pistons",F),("LC-SC","Stephon Castle","San Antonio Spurs",F),("LC-SS","Shaedon Sharpe","Portland Trail Blazers",F),("LC-TH","Tyrese Haliburton","Indiana Pacers",F),("LC-THJ","Tim Hardaway Jr.","Denver Nuggets",F),("LC-TJM","T.J. McConnell","Indiana Pacers",F),
("LC-TM","Tyrese Maxey","Philadelphia 76ers",F),("LC-TS","Tidjane Sala\u00fcn","Charlotte Hornets",F),("LC-WK","Walker Kessler","Utah Jazz",F),("LC-ZE","Zach Edey","Memphis Grizzlies",F),("LC-ZR","Zach Randolph","Memphis Grizzlies",F),
])

# ═══ LEGENDS OF THE COURT DUAL SIGNATURES (17 multi-subject) ═══
ins_dual("Legends of the Court Dual Signatures", [
("LCDS-AT","Allen Iverson","Tyrese Maxey"),("LCDS-CD","Cooper Flagg","Dirk Nowitzki"),("LCDS-CS","Chet Holmgren","Shai Gilgeous-Alexander"),("LCDS-DJ","Jason Kidd","Dirk Nowitzki"),("LCDS-HC","Clyde Drexler","Hakeem Olajuwon"),("LCDS-JA","Kevin Durant","Alperen Sengun"),("LCDS-JB","Bogdan Bogdanovi\u0107","James Harden"),("LCDS-JP","Paul Pierce","Jayson Tatum"),("LCDS-JZ","Zach Randolph","Jaren Jackson Jr."),
("LCDS-KJ","Jalen Brunson","Karl-Anthony Towns"),("LCDS-MT","Manu Ginobili","Tony Parker"),("LCDS-PM","Pau Gasol","Metta World Peace"),("LCDS-PT","Paolo Banchero","Tracy McGrady"),("LCDS-SN","Stephen Curry","Steve Nash"),("LCDS-SS","Shaedon Sharpe","Scoot Henderson"),("LCDS-TA","Tyler Herro","Andrew Wiggins"),("LCDS-VS","Stephon Castle","Victor Wembanyama"),
])

# ═══ LEGENDS OF THE COURT TRIPLE SIGNATURES (8 multi-subject) ═══
ins_triple("Legends of the Court Triple Signatures", [
("LCTS-CJA","Jamal Murray","Carmelo Anthony","Alex English"),("LCTS-HCK","Kevin Durant","Hakeem Olajuwon","Clyde Drexler"),("LCTS-JSC","Shai Gilgeous-Alexander","Chet Holmgren","Jalen Williams"),("LCTS-PJK","Paul Pierce","Kevin Garnett","Jayson Tatum"),
("LCTS-PTS","Shaquille O'Neal","Tracy McGrady","Paolo Banchero"),("LCTS-SAJ","Steve Nash","Allen Iverson","John Stockton"),("LCTS-TMD","Manu Ginobili","David Robinson","Tony Parker"),("LCTS-TMP","Myles Turner","Pascal Siakam","Tyrese Haliburton"),
])

# ═══ MOTIF ROOKIE RELIC AUTOGRAPHS (30, all RC) ═══
rra_rookies = [
("RRA-AB","Ace Bailey","Utah Jazz"),("RRA-AN","Asa Newell","Atlanta Hawks"),("RRA-AT","Adou Thiero","Los Angeles Lakers"),("RRA-BS","Ben Saraf","Brooklyn Nets"),("RRA-CC","Cedric Coward","Memphis Grizzlies"),("RRA-CF","Cooper Flagg","Dallas Mavericks"),("RRA-CL","Chaz Lanier","Detroit Pistons"),("RRA-CMB","Collin Murray-Boyles","Toronto Raptors"),("RRA-DH","Dylan Harper","San Antonio Spurs"),("RRA-DP","Drake Powell","Brooklyn Nets"),
("RRA-DQ","Derik Queen","New Orleans Pelicans"),("RRA-DW","Danny Wolf","Brooklyn Nets"),("RRA-ED","Egor D\u00ebmin","Brooklyn Nets"),("RRA-JB","Johni Broome","Philadelphia 76ers"),("RRA-JBE","Joan Beringer","Minnesota Timberwolves"),("RRA-JR","Jase Richardson","Orlando Magic"),("RRA-KJ","Kasparas Jaku\u010dionis","Miami Heat"),("RRA-KK","Kon Knueppel","Charlotte Hornets"),("RRA-KM","Khaman Maluach","Phoenix Suns"),("RRA-NC","Nique Clifford","Sacramento Kings"),
("RRA-NE","Noa Essengue","Chicago Bulls"),("RRA-NP","Noah Penda","Orlando Magic"),("RRA-NT","Nolan Traore","Brooklyn Nets"),("RRA-RF","Rasheer Fleming","Phoenix Suns"),("RRA-RK","Ryan Kalkbrenner","Charlotte Hornets"),("RRA-SJ","Sion James","Charlotte Hornets"),("RRA-TS","Thomas Sorber","Oklahoma City Thunder"),("RRA-WCJ","Walter Clayton Jr.","Utah Jazz"),("RRA-WR","Will Riley","Washington Wizards"),("RRA-YH","Yang Hansen","Portland Trail Blazers"),
]
ins("Motif Rookie Relic Autographs", [(n,nm,t,R) for n,nm,t in rra_rookies])

# RDRA, RTRA use same roster with different prefix
ins("Motif Rookie Dual Relic Autographs", [(n.replace("RRA-","RDRA-"),nm,t,R) for n,nm,t in rra_rookies])
ins("Motif Rookie Triple Relic Autographs", [(n.replace("RRA-","RTRA-"),nm,t,R) for n,nm,t in rra_rookies])

# ═══ MOTIF ROOKIE QUAD RELIC AUTOGRAPHS (10, all RC) ═══
ins("Motif Rookie Quad Relic Autographs", [
("RRTQ-AB","Ace Bailey","Utah Jazz",R),("RRTQ-CC","Cedric Coward","Memphis Grizzlies",R),("RRTQ-CF","Cooper Flagg","Dallas Mavericks",R),("RRTQ-CMB","Collin Murray-Boyles","Toronto Raptors",R),("RRTQ-DH","Dylan Harper","San Antonio Spurs",R),("RRTQ-DQ","Derik Queen","New Orleans Pelicans",R),("RRTQ-ED","Egor D\u00ebmin","Brooklyn Nets",R),("RRTQ-KK","Kon Knueppel","Charlotte Hornets",R),("RRTQ-KM","Khaman Maluach","Phoenix Suns",R),("RRTQ-NE","Noa Essengue","Chicago Bulls",R),
])

# ═══ MOTIF ROOKIE RELICS (39, all RC) ═══
ins("Motif Rookie Relics", [
("MRR-AB","Ace Bailey","Utah Jazz",R),("MRR-AM","Alijah Martin","Toronto Raptors",R),("MRR-AN","Asa Newell","Atlanta Hawks",R),("MRR-AT","Adou Thiero","Los Angeles Lakers",R),("MRR-BS","Ben Saraf","Brooklyn Nets",R),("MRR-CB","Carter Bryant","San Antonio Spurs",R),("MRR-CC","Cedric Coward","Memphis Grizzlies",R),("MRR-CF","Cooper Flagg","Dallas Mavericks",R),("MRR-CL","Chaz Lanier","Detroit Pistons",R),("MRR-CMB","Collin Murray-Boyles","Toronto Raptors",R),
("MRR-DH","Dylan Harper","San Antonio Spurs",R),("MRR-DP","Drake Powell","Brooklyn Nets",R),("MRR-DQ","Derik Queen","New Orleans Pelicans",R),("MRR-DW","Danny Wolf","Brooklyn Nets",R),("MRR-ED","Egor D\u00ebmin","Brooklyn Nets",R),("MRR-HG","Hugo Gonz\u00e1lez","Boston Celtics",R),("MRR-JB","Joan Beringer","Minnesota Timberwolves",R),("MRR-JBR","Johni Broome","Philadelphia 76ers",R),("MRR-JC","Jase Richardson","Orlando Magic",R),("MRR-JF","Jeremiah Fears","New Orleans Pelicans",R),
("MRR-KJ","Kasparas Jaku\u010dionis","Miami Heat",R),("MRR-KJO","Kam Jones","Indiana Pacers",R),("MRR-KK","Kon Knueppel","Charlotte Hornets",R),("MRR-KM","Khaman Maluach","Phoenix Suns",R),("MRR-MP","Micah Peavy","New Orleans Pelicans",R),("MRR-NC","Nique Clifford","Sacramento Kings",R),("MRR-NE","Noa Essengue","Chicago Bulls",R),("MRR-NP","Noah Penda","Orlando Magic",R),("MRR-NT","Nolan Traore","Brooklyn Nets",R),("MRR-RF","Rasheer Fleming","Phoenix Suns",R),
("MRR-RK","Ryan Kalkbrenner","Charlotte Hornets",R),("MRR-SJ","Sion James","Charlotte Hornets",R),("MRR-TJ","Tre Johnson III","Washington Wizards",R),("MRR-TP","Tyrese Proctor","Cleveland Cavaliers",R),("MRR-TS","Thomas Sorber","Oklahoma City Thunder",R),("MRR-VJ","VJ Edgecombe","Philadelphia 76ers",R),("MRR-WCJ","Walter Clayton Jr.","Utah Jazz",R),("MRR-WR","Will Riley","Washington Wizards",R),("MRR-YH","Yang Hansen","Portland Trail Blazers",R),
])

# ═══ MOTIF ROOKIE DUAL RELICS (39, all RC) ═══
ins("Motif Rookie Dual Relics", [
("MRD-AB","Ace Bailey","Utah Jazz",R),("MRD-AM","Alijah Martin","Toronto Raptors",R),("MRD-AN","Asa Newell","Atlanta Hawks",R),("MRD-AT","Adou Thiero","Los Angeles Lakers",R),("MRD-BS","Ben Saraf","Brooklyn Nets",R),("MRD-CB","Carter Bryant","San Antonio Spurs",R),("MRD-CC","Cedric Coward","Memphis Grizzlies",R),("MRD-CF","Cooper Flagg","Dallas Mavericks",R),("MRD-CL","Chaz Lanier","Detroit Pistons",R),("MRD-CMB","Collin Murray-Boyles","Toronto Raptors",R),
("MRD-DH","Dylan Harper","San Antonio Spurs",R),("MRD-DP","Drake Powell","Brooklyn Nets",R),("MRD-DQ","Derik Queen","New Orleans Pelicans",R),("MRD-DW","Danny Wolf","Brooklyn Nets",R),("MRD-ED","Egor D\u00ebmin","Brooklyn Nets",R),("MRD-HG","Hugo Gonz\u00e1lez","Boston Celtics",R),("MRD-JB","Johni Broome","Philadelphia 76ers",R),("MRD-JBE","Joan Beringer","Minnesota Timberwolves",R),("MRD-JF","Jeremiah Fears","New Orleans Pelicans",R),("MRD-JR","Jase Richardson","Orlando Magic",R),
("MRD-KJ","Kam Jones","Indiana Pacers",R),("MRD-KJA","Kasparas Jaku\u010dionis","Miami Heat",R),("MRD-KK","Kon Knueppel","Charlotte Hornets",R),("MRD-KM","Khaman Maluach","Phoenix Suns",R),("MRD-MP","Micah Peavy","New Orleans Pelicans",R),("MRD-NC","Nique Clifford","Sacramento Kings",R),("MRD-NE","Noa Essengue","Chicago Bulls",R),("MRD-NP","Noah Penda","Orlando Magic",R),("MRD-NT","Nolan Traore","Brooklyn Nets",R),("MRD-RF","Rasheer Fleming","Phoenix Suns",R),
("MRD-RK","Ryan Kalkbrenner","Charlotte Hornets",R),("MRD-SJ","Sion James","Charlotte Hornets",R),("MRD-TJ","Tre Johnson III","Washington Wizards",R),("MRD-TP","Tyrese Proctor","Cleveland Cavaliers",R),("MRD-TS","Thomas Sorber","Oklahoma City Thunder",R),("MRD-VJ","VJ Edgecombe","Philadelphia 76ers",R),("MRD-WCJ","Walter Clayton Jr.","Utah Jazz",R),("MRD-WR","Will Riley","Washington Wizards",R),("MRD-YH","Yang Hansen","Portland Trail Blazers",R),
])

# ═══ LEGENDS OF THE COURT RELICS (20) ═══
ins("Legends of the Court Relics", [
("LCR-AE","Anthony Edwards","Minnesota Timberwolves",F),("LCR-BAM","Bam Adebayo","Miami Heat",F),("LCR-DF","De'Aaron Fox","San Antonio Spurs",F),("LCR-DM","Donovan Mitchell","Cleveland Cavaliers",F),("LCR-DS","Domantas Sabonis","Sacramento Kings",F),("LCR-DW","Derrick White","Boston Celtics",F),("LCR-GA","Giannis Antetokounmpo","Milwaukee Bucks",F),("LCR-JB","Jalen Brunson","New York Knicks",F),("LCR-JH","James Harden","Los Angeles Clippers",F),("LCR-JHA","Josh Hart","New York Knicks",F),
("LCR-JJJ","Jaren Jackson Jr.","Memphis Grizzlies",F),("LCR-KAT","Karl-Anthony Towns","New York Knicks",F),("LCR-PB","Paolo Banchero","Orlando Magic",F),("LCR-SC","Stephen Curry","Golden State Warriors",F),("LCR-SH","Scoot Henderson","Portland Trail Blazers",F),("LCR-TH","Tyrese Haliburton","Indiana Pacers",F),("LCR-THO","Tyler Herro","Miami Heat",F),("LCR-TM","Tyrese Maxey","Philadelphia 76ers",F),("LCR-VW","Victor Wembanyama","San Antonio Spurs",F),("LCR-ZR","Zaccharie Risacher","Atlanta Hawks",F),
])

# ═══ BACKFILL IMAGE IDs ═════════════════════════════════════════════════════
db.commit()
updated = db.execute("""
    UPDATE players SET nba_player_id = (SELECT p2.nba_player_id FROM players p2 WHERE p2.name = players.name AND p2.nba_player_id IS NOT NULL LIMIT 1)
    WHERE set_id = ? AND nba_player_id IS NULL AND EXISTS (SELECT 1 FROM players p2 WHERE p2.name = players.name AND p2.nba_player_id IS NOT NULL)
""", (SET_ID,)).rowcount
print(f"\nBackfilled {updated} NBA player IDs")

# ═══ VERIFY ═════════════════════════════════════════════════════════════════
db.commit()
rows = db.execute("""
    SELECT ins.name, (SELECT COUNT(*) FROM player_appearances pa WHERE pa.insert_set_id = ins.id) as cards
    FROM insert_sets ins WHERE ins.set_id = ? AND ins.name != 'Base Set' ORDER BY ins.name
""", (SET_ID,)).fetchall()

total = 0
print("\n--- Verification ---")
for name, cnt in rows:
    print(f"  {name}: {cnt}")
    total += cnt
print(f"\nTotal non-base cards: {total}")
print(f"Total athletes: {db.execute('SELECT COUNT(*) FROM players WHERE set_id = ?', (SET_ID,)).fetchone()[0]}")

db.close()
print("Done!")
