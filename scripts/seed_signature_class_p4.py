"""
Seed: 2025-26 Topps Signature Class Basketball — Part 4: All autograph sets.
Usage: python3 scripts/seed_signature_class_p4.py
"""
import sqlite3, os, re

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA foreign_keys=ON")
cur = conn.cursor()

SET_ID = 838
T = True; R = False

def get_or_create_player(name):
    cur.execute("SELECT id FROM players WHERE set_id = ? AND name = ?", (SET_ID, name))
    row = cur.fetchone()
    if row: return row[0]
    cur.execute("INSERT INTO players (set_id, name, unique_cards, total_print_run, one_of_ones, insert_set_count) VALUES (?, ?, 0, 0, 0, 0)", (SET_ID, name))
    return cur.lastrowid

def get_is_id(name):
    return cur.execute("SELECT id FROM insert_sets WHERE set_id = ? AND name = ?", (SET_ID, name)).fetchone()[0]

def add_cards(is_name, cards):
    is_id = get_is_id(is_name)
    for num, name, team, rookie in cards:
        pid = get_or_create_player(name)
        cur.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)",
                    (pid, is_id, num, int(rookie), team))
    print(f"  {is_name}: {len(cards)} cards")

def add_dual_cards(is_name, cards):
    is_id = get_is_id(is_name)
    for entry in cards:
        num = entry[0]
        p1n, p1t, p1r = entry[1], entry[2], entry[3]
        p2n, p2t, p2r = entry[4], entry[5], entry[6]
        p1 = get_or_create_player(p1n)
        p2 = get_or_create_player(p2n)
        a1 = cur.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)",
                    (p1, is_id, num, int(p1r), p1t)).lastrowid
        a2 = cur.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)",
                    (p2, is_id, num, int(p2r), p2t)).lastrowid
        cur.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a1, p2))
        cur.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a2, p1))
    print(f"  {is_name}: {len(cards)} dual cards")

def add_triple_cards(is_name, cards):
    is_id = get_is_id(is_name)
    for num, players in cards:
        pids, aids = [], []
        for name, team, rookie in players:
            pid = get_or_create_player(name)
            aid = cur.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)",
                        (pid, is_id, num, int(rookie), team)).lastrowid
            pids.append(pid); aids.append(aid)
        for i in range(len(aids)):
            for j in range(len(pids)):
                if i != j:
                    cur.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (aids[i], pids[j]))
    print(f"  {is_name}: {len(cards)} triple cards")

# ─── VETERAN CLASS AUTOGRAPHS ────────────────────────────────────
add_cards("Veteran Class Autographs", [
    ("VCA-AB","Anthony Black","Orlando Magic",R),("VCA-AH","Al Horford","Boston Celtics",R),("VCA-AW","Andrew Wiggins","Miami Heat",R),
    ("VCA-BB","Bradley Beal","Phoenix Suns",R),("VCA-BM","Brandon Miller","Charlotte Hornets",R),("VCA-CA","Cole Anthony","Orlando Magic",R),
    ("VCA-CBE","Coby White","Chicago Bulls",R),("VCA-CC","Clint Capela","Atlanta Hawks",R),("VCA-CJ","Cameron Johnson","Brooklyn Nets",R),
    ("VCA-CM","CJ McCollum","New Orleans Pelicans",R),("VCA-CP","Chris Paul","San Antonio Spurs",R),("VCA-CW","Cason Wallace","Oklahoma City Thunder",R),
    ("VCA-CWI","Cody Williams","Utah Jazz",R),("VCA-DA","Deandre Ayton","Portland Trail Blazers",R),("VCA-DD","Dyson Daniels","Atlanta Hawks",R),
    ("VCA-DJ","Dillon Jones","Oklahoma City Thunder",R),("VCA-DR","D'Angelo Russell","Brooklyn Nets",R),("VCA-DV","Devin Vassell","San Antonio Spurs",R),
    ("VCA-GD","Gradey Dick","Toronto Raptors",R),("VCA-GW","Grant Williams","Charlotte Hornets",R),("VCA-HJ","Herbert Jones","New Orleans Pelicans",R),
    ("VCA-IC","Isaiah Collier","Utah Jazz",R),("VCA-IH","Isaiah Hartenstein","Oklahoma City Thunder",R),("VCA-JG","Josh Giddey","Chicago Bulls",R),
    ("VCA-JH","Jrue Holiday","Boston Celtics",R),("VCA-JJ","Jaime Jaquez Jr.","Miami Heat",R),("VCA-JW","Jarace Walker","Indiana Pacers",R),
    ("VCA-KL","Kevin Love","Miami Heat",R),("VCA-KM","Khris Middleton","Washington Wizards",R),("VCA-KW","Kel'el Ware","Miami Heat",R),
    ("VCA-LM","Lauri Markkanen","Utah Jazz",R),("VCA-MS","Marcus Smart","Washington Wizards",R),("VCA-NR","Naz Reid","Minnesota Timberwolves",R),
    ("VCA-NT","Nikola Topic","Oklahoma City Thunder",R),("VCA-OT","Obi Toppin","Indiana Pacers",R),("VCA-PL","Pelle Larsson","Miami Heat",R),
    ("VCA-PP","Payton Pritchard","Boston Celtics",R),("VCA-RH","Ron Holland II","Detroit Pistons",R),("VCA-RUI","Rui Hachimura","Los Angeles Lakers",R),
    ("VCA-SS","Shaedon Sharpe","Portland Trail Blazers",R),("VCA-TDS","Tristan da Silva","Orlando Magic",R),("VCA-TJ","Ty Jerome","Cleveland Cavaliers",R),
    ("VCA-TMA","Tyrese Maxey","Philadelphia 76ers",R),("VCA-TMN","Terance Mann","Atlanta Hawks",R),("VCA-WK","Walker Kessler","Utah Jazz",R),
    ("VCA-ZE","Zach Edey","Memphis Grizzlies",R),
])

# ─── VETERAN CLASS CHROME AUTOGRAPHS ─────────────────────────────
add_cards("Veteran Class Chrome Autographs", [
    ("VCC-AG","Aaron Gordon","Denver Nuggets",R),("VCC-AS","Alex Sarr","Washington Wizards",R),("VCC-ASE","Alperen Sengun","Houston Rockets",R),
    ("VCC-BM","Brandon Miller","Charlotte Hornets",R),("VCC-CH","Chet Holmgren","Oklahoma City Thunder",R),("VCC-CS","Collin Sexton","Utah Jazz",R),
    ("VCC-CW","Cam Whitmore","Houston Rockets",R),("VCC-DD","Donte DiVincenzo","Minnesota Timberwolves",R),("VCC-DFS","Dorian Finney-Smith","Los Angeles Lakers",R),
    ("VCC-DL","Dereck Lively II","Dallas Mavericks",R),("VCC-DM","Donovan Mitchell","Cleveland Cavaliers",R),("VCC-DW","Derrick White","Boston Celtics",R),
    ("VCC-FW","Franz Wagner","Orlando Magic",R),("VCC-GRA","Grayson Allen","Phoenix Suns",R),("VCC-JA","Jarrett Allen","Cleveland Cavaliers",R),
    ("VCC-JB","Jalen Brunson","New York Knicks",R),("VCC-JC","Jordan Clarkson","Utah Jazz",R),("VCC-JG","Jalen Green","Houston Rockets",R),
    ("VCC-JH","James Harden","Los Angeles Clippers",R),("VCC-JJJ","Jaren Jackson Jr.","Memphis Grizzlies",R),("VCC-JM","Jamal Murray","Denver Nuggets",R),
    ("VCC-JT","Jayson Tatum","Boston Celtics",R),("VCC-JW","Jalen Williams","Oklahoma City Thunder",R),("VCC-KAT","Karl-Anthony Towns","New York Knicks",R),
    ("VCC-KD","Kevin Durant","Houston Rockets",R),("VCC-KDU","Kris Dunn","Los Angeles Clippers",R),("VCC-KP","Kristaps Porzingis","Boston Celtics",R),
    ("VCC-LBJ","LeBron James","Los Angeles Lakers",R),("VCC-LK","Luke Kennard","Memphis Grizzlies",R),("VCC-MB","Mikal Bridges","New York Knicks",R),
    ("VCC-MPJ","Michael Porter Jr.","Denver Nuggets",R),("VCC-MT","Myles Turner","Indiana Pacers",R),("VCC-NJ","Nikola Jokic","Denver Nuggets",R),
    ("VCC-NSJ","Nick Smith Jr.","Charlotte Hornets",R),("VCC-PB","Paolo Banchero","Orlando Magic",R),("VCC-RD","Rob Dillingham","Minnesota Timberwolves",R),
    ("VCC-RG","Rudy Gobert","Minnesota Timberwolves",R),("VCC-SC","Stephen Curry","Golden State Warriors",R),("VCC-SGA","Shai Gilgeous-Alexander","Oklahoma City Thunder",R),
    ("VCC-SH","Scoot Henderson","Portland Trail Blazers",R),("VCC-STC","Stephon Castle","San Antonio Spurs",R),("VCC-THA","Tyrese Haliburton","Indiana Pacers",R),
    ("VCC-TS","Tidjane Salaun","Charlotte Hornets",R),("VCC-VW","Victor Wembanyama","San Antonio Spurs",R),("VCC-ZL","Zach LaVine","Sacramento Kings",R),
    ("VCC-ZR","Zaccharie Risacher","Atlanta Hawks",R),
])

# ─── VETERAN CLASS CRYSTAL CLEAR AUTOGRAPHS ──────────────────────
add_cards("Veteran Class Crystal Clear Autographs", [
    ("CCA-AG","Aaron Gordon","Denver Nuggets",R),("CCA-AS","Alex Sarr","Washington Wizards",R),("CCA-CH","Chet Holmgren","Oklahoma City Thunder",R),
    ("CCA-CS","Collin Sexton","Utah Jazz",R),("CCA-CW","Cam Whitmore","Houston Rockets",R),("CCA-DFS","Dorian Finney-Smith","Los Angeles Lakers",R),
    ("CCA-DL","Dereck Lively II","Dallas Mavericks",R),("CCA-DM","Donovan Mitchell","Cleveland Cavaliers",R),("CCA-FW","Franz Wagner","Orlando Magic",R),
    ("CCA-GA","Giannis Antetokounmpo","Milwaukee Bucks",R),("CCA-GRA","Grayson Allen","Phoenix Suns",R),("CCA-JB","Jalen Brunson","New York Knicks",R),
    ("CCA-JG","Jalen Green","Houston Rockets",R),("CCA-JH","James Harden","Los Angeles Clippers",R),("CCA-JJJ","Jaren Jackson Jr.","Memphis Grizzlies",R),
    ("CCA-JM","Jamal Murray","Denver Nuggets",R),("CCA-JT","Jayson Tatum","Boston Celtics",R),("CCA-JW","Jalen Williams","Oklahoma City Thunder",R),
    ("CCA-KAT","Karl-Anthony Towns","New York Knicks",R),("CCA-KD","Kevin Durant","Houston Rockets",R),("CCA-KDU","Kris Dunn","Los Angeles Clippers",R),
    ("CCA-KP","Kristaps Porzingis","Boston Celtics",R),("CCA-LBJ","LeBron James","Los Angeles Lakers",R),("CCA-MB","Mikal Bridges","New York Knicks",R),
    ("CCA-MPJ","Michael Porter Jr.","Denver Nuggets",R),("CCA-NJ","Nikola Jokic","Denver Nuggets",R),("CCA-PB","Paolo Banchero","Orlando Magic",R),
    ("CCA-RD","Rob Dillingham","Minnesota Timberwolves",R),("CCA-SC","Stephen Curry","Golden State Warriors",R),("CCA-SGA","Shai Gilgeous-Alexander","Oklahoma City Thunder",R),
    ("CCA-SH","Scoot Henderson","Portland Trail Blazers",R),("CCA-STC","Stephon Castle","San Antonio Spurs",R),("CCA-TH","Tyrese Haliburton","Indiana Pacers",R),
    ("CCA-TS","Tidjane Salaun","Charlotte Hornets",R),("CCA-VW","Victor Wembanyama","San Antonio Spurs",R),("CCA-ZL","Zach LaVine","Sacramento Kings",R),
    ("CCA-ZR","Zaccharie Risacher","Atlanta Hawks",R),
])

# ─── ROOKIE CLASS AUTOGRAPHS ─────────────────────────────────────
add_cards("Rookie Class Autographs", [
    ("RCA-AB","Ace Bailey","Utah Jazz",T),("RCA-AM","Alijah Martin","Toronto Raptors",T),("RCA-AN","Asa Newell","Atlanta Hawks",T),
    ("RCA-AT","Alex Toohey","Golden State Warriors",T),("RCA-ATH","Adou Thiero","Los Angeles Lakers",T),("RCA-BB","Brooks Barnhizer","Oklahoma City Thunder",T),
    ("RCA-BS","Ben Saraf","Brooklyn Nets",T),("RCA-CC","Cedric Coward","Memphis Grizzlies",T),("RCA-CF","Cooper Flagg","Dallas Mavericks",T),
    ("RCA-CL","Chaz Lanier","Detroit Pistons",T),("RCA-CMB","Collin Murray-Boyles","Toronto Raptors",T),("RCA-DH","Dylan Harper","San Antonio Spurs",T),
    ("RCA-DP","Drake Powell","Brooklyn Nets",T),("RCA-DQ","Derik Queen","New Orleans Pelicans",T),("RCA-DW","Danny Wolf","Brooklyn Nets",T),
    ("RCA-ED","Egor Demin","Brooklyn Nets",T),("RCA-JB","Johni Broome","Philadelphia 76ers",T),("RCA-JBE","Joan Beringer","Minnesota Timberwolves",T),
    ("RCA-JR","Jase Richardson","Orlando Magic",T),("RCA-JS","Javon Small","Memphis Grizzlies",T),("RCA-JT","John Tonje","Utah Jazz",T),
    ("RCA-JW","Jamir Watkins","Washington Wizards",T),("RCA-KB","Koby Brea","Phoenix Suns",T),("RCA-KJ","Kam Jones","Indiana Pacers",T),
    ("RCA-KJA","Kasparas Jakucionis","Miami Heat",T),("RCA-KK","Kon Knueppel","Charlotte Hornets",T),("RCA-KM","Khaman Maluach","Phoenix Suns",T),
    ("RCA-LM","Liam McNeeley","Charlotte Hornets",T),("RCA-LO","Lachlan Olbrich","Chicago Bulls",T),("RCA-MP","Micah Peavy","New Orleans Pelicans",T),
    ("RCA-MR","Maxime Raynaud","Sacramento Kings",T),("RCA-NC","Nique Clifford","Sacramento Kings",T),("RCA-NE","Noa Essengue","Chicago Bulls",T),
    ("RCA-NP","Noah Penda","Orlando Magic",T),("RCA-NT","Nolan Traore","Brooklyn Nets",T),("RCA-RF","Rasheer Fleming","Phoenix Suns",T),
    ("RCA-RK","Ryan Kalkbrenner","Charlotte Hornets",T),("RCA-RZ","Jahmai Mashack","Memphis Grizzlies",T),("RCA-SJ","Sion James","Charlotte Hornets",T),
    ("RCA-TH","Yang Hansen","Portland Trail Blazers",T),("RCA-TPR","Tyrese Proctor","Cleveland Cavaliers",T),("RCA-TS","Thomas Sorber","Oklahoma City Thunder",T),
    ("RCA-WCJ","Walter Clayton Jr.","Utah Jazz",T),("RCA-WR","Will Riley","Washington Wizards",T),("RCA-WRI","Will Richard","Golden State Warriors",T),
    ("RCA-YKN","Yanic Konan-Niederhauser","Los Angeles Clippers",T),
])

# ─── ROOKIE CLASS CHROME AUTOGRAPHS ──────────────────────────────
add_cards("Rookie Class Chrome Autographs", [
    ("RCC-AB","Ace Bailey","Utah Jazz",T),("RCC-AM","Alijah Martin","Toronto Raptors",T),("RCC-AN","Asa Newell","Atlanta Hawks",T),
    ("RCC-AT","Adou Thiero","Los Angeles Lakers",T),("RCC-ATO","Alex Toohey","Golden State Warriors",T),("RCC-BB","Brooks Barnhizer","Oklahoma City Thunder",T),
    ("RCC-BS","Ben Saraf","Brooklyn Nets",T),("RCC-CC","Cedric Coward","Memphis Grizzlies",T),("RCC-CF","Cooper Flagg","Dallas Mavericks",T),
    ("RCC-CL","Chaz Lanier","Detroit Pistons",T),("RCC-CMB","Collin Murray-Boyles","Toronto Raptors",T),("RCC-DH","Dylan Harper","San Antonio Spurs",T),
    ("RCC-DP","Drake Powell","Brooklyn Nets",T),("RCC-DQ","Derik Queen","New Orleans Pelicans",T),("RCC-DW","Danny Wolf","Brooklyn Nets",T),
    ("RCC-ED","Egor Demin","Brooklyn Nets",T),("RCC-JB","Johni Broome","Philadelphia 76ers",T),("RCC-JBE","Joan Beringer","Minnesota Timberwolves",T),
    ("RCC-JR","Jase Richardson","Orlando Magic",T),("RCC-JS","Javon Small","Memphis Grizzlies",T),("RCC-JT","John Tonje","Utah Jazz",T),
    ("RCC-JW","Jamir Watkins","Washington Wizards",T),("RCC-KB","Koby Brea","Phoenix Suns",T),("RCC-KJ","Kam Jones","Indiana Pacers",T),
    ("RCC-KJA","Kasparas Jakucionis","Miami Heat",T),("RCC-KK","Kon Knueppel","Charlotte Hornets",T),("RCC-KM","Khaman Maluach","Phoenix Suns",T),
    ("RCC-LM","Liam McNeeley","Charlotte Hornets",T),("RCC-LO","Lachlan Olbrich","Chicago Bulls",T),("RCC-MP","Micah Peavy","New Orleans Pelicans",T),
    ("RCC-MR","Maxime Raynaud","Sacramento Kings",T),("RCC-NC","Nique Clifford","Sacramento Kings",T),("RCC-NE","Noa Essengue","Chicago Bulls",T),
    ("RCC-NP","Noah Penda","Orlando Magic",T),("RCC-NT","Nolan Traore","Brooklyn Nets",T),("RCC-RF","Rasheer Fleming","Phoenix Suns",T),
    ("RCC-RJ","Ryan Kalkbrenner","Charlotte Hornets",T),("RCC-RZ","Jahmai Mashack","Memphis Grizzlies",T),("RCC-SJ","Sion James","Charlotte Hornets",T),
    ("RCC-TP","Tyrese Proctor","Cleveland Cavaliers",T),("RCC-TS","Thomas Sorber","Oklahoma City Thunder",T),("RCC-WCJ","Walter Clayton Jr.","Utah Jazz",T),
    ("RCC-WR","Will Richard","Golden State Warriors",T),("RCC-WRI","Will Riley","Washington Wizards",T),("RCC-YH","Yang Hansen","Portland Trail Blazers",T),
    ("RCC-YKN","Yanic Konan-Niederhauser","Los Angeles Clippers",T),
])

# ─── ROOKIE CLASS CRYSTAL CLEAR AUTOGRAPHS ───────────────────────
add_cards("Rookie Class Crystal Clear Autographs", [
    ("CCA-AB","Ace Bailey","Utah Jazz",T),("CCA-AM","Alijah Martin","Toronto Raptors",T),("CCA-AN","Asa Newell","Atlanta Hawks",T),
    ("CCA-AT","Alex Toohey","Golden State Warriors",T),("CCA-ATH","Adou Thiero","Los Angeles Lakers",T),("CCA-BB","Brooks Barnhizer","Oklahoma City Thunder",T),
    ("CCA-BS","Ben Saraf","Brooklyn Nets",T),("CCA-CC","Cedric Coward","Memphis Grizzlies",T),("CCA-CF","Cooper Flagg","Dallas Mavericks",T),
    ("CCA-CL","Chaz Lanier","Detroit Pistons",T),("CCA-CMB","Collin Murray-Boyles","Toronto Raptors",T),("CCA-DH","Dylan Harper","San Antonio Spurs",T),
    ("CCA-DP","Drake Powell","Brooklyn Nets",T),("CCA-DQ","Derik Queen","New Orleans Pelicans",T),("CCA-DW","Danny Wolf","Brooklyn Nets",T),
    ("CCA-ED","Egor Demin","Brooklyn Nets",T),("CCA-JBE","Joan Beringer","Minnesota Timberwolves",T),("CCA-JR","Jase Richardson","Orlando Magic",T),
    ("CCA-JS","Javon Small","Memphis Grizzlies",T),("CCA-JT","John Tonje","Utah Jazz",T),("CCA-JW","Jamir Watkins","Washington Wizards",T),
    ("CCA-KB","Koby Brea","Phoenix Suns",T),("CCA-KJ","Kam Jones","Indiana Pacers",T),("CCA-KJA","Kasparas Jakucionis","Miami Heat",T),
    ("CCA-KK","Kon Knueppel","Charlotte Hornets",T),("CCA-KM","Khaman Maluach","Phoenix Suns",T),("CCA-LM","Liam McNeeley","Charlotte Hornets",T),
    ("CCA-LO","Lachlan Olbrich","Chicago Bulls",T),("CCA-MP","Micah Peavy","New Orleans Pelicans",T),("CCA-MR","Maxime Raynaud","Sacramento Kings",T),
    ("CCA-NC","Nique Clifford","Sacramento Kings",T),("CCA-NE","Noa Essengue","Chicago Bulls",T),("CCA-NP","Noah Penda","Orlando Magic",T),
    ("CCA-NT","Nolan Traore","Brooklyn Nets",T),("CCA-RF","Rasheer Fleming","Phoenix Suns",T),("CCA-RK","Ryan Kalkbrenner","Charlotte Hornets",T),
    ("CCA-RZ","Jahmai Mashack","Memphis Grizzlies",T),("CCA-SJ","Sion James","Charlotte Hornets",T),("CCA-TPR","Tyrese Proctor","Cleveland Cavaliers",T),
    ("CCA-TS","Thomas Sorber","Oklahoma City Thunder",T),("CCA-WCJ","Walter Clayton Jr.","Utah Jazz",T),("CCA-WR","Will Riley","Washington Wizards",T),
    ("CCA-WRI","Will Richard","Golden State Warriors",T),("CCA-YH","Yang Hansen","Portland Trail Blazers",T),("CCA-YKN","Yanic Konan-Niederhauser","Los Angeles Clippers",T),
])

# ─── LEGENDS OF THEIR CLASS CRYSTAL CLEAR AUTOGRAPHS ─────────────
add_cards("Legends of Their Class Crystal Clear Autographs", [
    ("LOTC-AI","Allen Iverson","Philadelphia 76ers",R),("LOTC-DN","Dirk Nowitzki","Dallas Mavericks",R),("LOTC-DW","Dwyane Wade","Miami Heat",R),
    ("LOTC-HO","Hakeem Olajuwon","Houston Rockets",R),("LOTC-KG","Kevin Garnett","Boston Celtics",R),("LOTC-LB","Larry Bird","Boston Celtics",R),
    ("LOTC-MJ","Magic Johnson","Los Angeles Lakers",R),("LOTC-SO","Shaquille O'Neal","Los Angeles Lakers",R),("LOTC-TM","Tracy McGrady","Houston Rockets",R),
    ("LOTC-VC","Vince Carter","Toronto Raptors",R),
])

# ─── SIGNATURE BLEND ─────────────────────────────────────────────
add_cards("Signature Blend", [
    ("SB-AH","Anfernee Hardaway","Orlando Magic",R),("SB-AT","Adou Thiero","Los Angeles Lakers",T),("SB-BJ","Bronny James Jr.","Los Angeles Lakers",R),
    ("SB-BM","Brandon Miller","Charlotte Hornets",R),("SB-CA","Carmelo Anthony","New York Knicks",R),("SB-CAN","Cole Anthony","Orlando Magic",R),
    ("SB-CJ","Cameron Johnson","Brooklyn Nets",R),("SB-CW","Coby White","Chicago Bulls",R),("SB-DQ","Derik Queen","New Orleans Pelicans",T),
    ("SB-IZ","Ivica Zubac","Los Angeles Clippers",R),("SB-JB","Johni Broome","Philadelphia 76ers",T),("SB-JH","Jrue Holiday","Boston Celtics",R),
    ("SB-JK","Jason Kidd","Dallas Mavericks",R),("SB-JW","Jason Williams","Sacramento Kings",R),("SB-KB","Koby Brea","Phoenix Suns",T),
    ("SB-KCP","Kentavious Caldwell-Pope","Orlando Magic",R),("SB-MP","Micah Peavy","New Orleans Pelicans",T),("SB-NE","Noa Essengue","Chicago Bulls",T),
    ("SB-PG","Pau Gasol","Los Angeles Lakers",R),("SB-SS","Shaedon Sharpe","Portland Trail Blazers",R),("SB-TM","Tyrese Maxey","Philadelphia 76ers",R),
    ("SB-TP","Tyrese Proctor","Cleveland Cavaliers",T),("SB-WCJ","Walter Clayton Jr.","Utah Jazz",T),("SB-WR","Will Riley","Washington Wizards",T),
    ("SB-YH","Yang Hansen","Portland Trail Blazers",T),
])

# ─── SHADOW SCRIPTS ───────────────────────────────────────────────
add_cards("Shadow Scripts", [
    ("SS-AS","Alex Sarr","Washington Wizards",R),("SS-AT","Adou Thiero","Los Angeles Lakers",T),("SS-BB","Bradley Beal","Phoenix Suns",R),
    ("SS-CJM","CJ McCollum","New Orleans Pelicans",R),("SS-DQ","Derik Queen","New Orleans Pelicans",T),("SS-DR","Dennis Rodman","Chicago Bulls",R),
    ("SS-DW","Dominique Wilkins","Atlanta Hawks",R),("SS-GD","Gradey Dick","Toronto Raptors",R),("SS-HJ","Herbert Jones","New Orleans Pelicans",R),
    ("SS-HO","Hakeem Olajuwon","Houston Rockets",R),("SS-IC","Isaiah Collier","Utah Jazz",R),("SS-JC","Kristaps Porzingis","Boston Celtics",R),
    ("SS-JJJ","Jaren Jackson Jr.","Memphis Grizzlies",R),("SS-JS","Javon Small","Memphis Grizzlies",T),("SS-KB","Koby Brea","Phoenix Suns",T),
    ("SS-KK","Kon Knueppel","Charlotte Hornets",T),("SS-KM","Khris Middleton","Washington Wizards",R),("SS-MP","Micah Peavy","New Orleans Pelicans",T),
    ("SS-NAW","Nickeil Alexander-Walker","Minnesota Timberwolves",R),("SS-NE","Noa Essengue","Chicago Bulls",T),("SS-RP","Robert Parish","Boston Celtics",R),
    ("SS-SJ","Sion James","Charlotte Hornets",T),("SS-TP","Tyrese Proctor","Cleveland Cavaliers",T),("SS-WCJ","Walter Clayton Jr.","Utah Jazz",T),
    ("SS-ZR","Zach Randolph","Memphis Grizzlies",R),
])

# ─── PENSTROKE SIGNATURES ────────────────────────────────────────
add_cards("Penstroke Signatures", [
    ("PS-AH","Al Horford","Boston Celtics",R),("PS-AW","Andrew Wiggins","Miami Heat",R),("PS-BJ","Bronny James Jr.","Los Angeles Lakers",R),
    ("PS-CD","Clyde Drexler","Portland Trail Blazers",R),("PS-CP","Chris Paul","San Antonio Spurs",R),("PS-DQ","Derik Queen","New Orleans Pelicans",T),
    ("PS-DV","Devin Vassell","San Antonio Spurs",R),("PS-JB","Joan Beringer","Minnesota Timberwolves",T),("PS-JC","Jordan Clarkson","Utah Jazz",R),
    ("PS-JH","Jordan Hawkins","New Orleans Pelicans",R),("PS-JP","Jakob Poeltl","Toronto Raptors",R),("PS-JW","Jarace Walker","Indiana Pacers",R),
    ("PS-KJ","Kasparas Jakucionis","Miami Heat",T),("PS-KW","Kel'el Ware","Miami Heat",R),("PS-LM","Lauri Markkanen","Utah Jazz",R),
    ("PS-MS","Marcus Smart","Washington Wizards",R),("PS-NE","Noa Essengue","Chicago Bulls",T),("PS-NT","Nolan Traore","Brooklyn Nets",T),
    ("PS-RA","Ray Allen","Boston Celtics",R),("PS-RB","Rick Barry","Golden State Warriors",R),("PS-RH","Rip Hamilton","Detroit Pistons",R),
    ("PS-RHO","Ron Holland II","Detroit Pistons",R),("PS-RK","Ryan Kalkbrenner","Charlotte Hornets",T),("PS-SH","Scoot Henderson","Portland Trail Blazers",R),
    ("PS-TS","Thomas Sorber","Oklahoma City Thunder",T),("PS-WCJ","Walter Clayton Jr.","Utah Jazz",T),("PS-WR","Will Riley","Washington Wizards",T),
    ("PS-YS","Yang Hansen","Portland Trail Blazers",T),("PS-ZE","Zach Edey","Memphis Grizzlies",R),
])

# ─── ETERNAL MARKS ────────────────────────────────────────────────
add_cards("Eternal Marks", [
    ("EM-AM","Alonzo Mourning","Miami Heat",R),("EM-CP","Chris Paul","San Antonio Spurs",R),("EM-DH","Dwight Howard","Orlando Magic",R),
    ("EM-DR","David Robinson","San Antonio Spurs",R),("EM-DT","David Thompson","Denver Nuggets",R),("EM-DW","Deron Williams","Brooklyn Nets",R),
    ("EM-GG","George Gervin","San Antonio Spurs",R),("EM-GH","Gordon Hayward","Utah Jazz",R),("EM-GHL","Grant Hill","Detroit Pistons",R),
    ("EM-JR","Jalen Rose","Indiana Pacers",R),("EM-JS","John Stockton","Utah Jazz",R),("EM-KL","Kevin Love","Miami Heat",R),
    ("EM-LBJ","LeBron James","Los Angeles Lakers",R),("EM-MWP","Metta World Peace","Los Angeles Lakers",R),("EM-PP","Paul Pierce","Boston Celtics",R),
    ("EM-RJ","Richard Jefferson","New Jersey Nets",R),("EM-SW","Spud Webb","Sacramento Kings",R),("EM-TH","Tim Hardaway","Golden State Warriors",R),
    ("EM-ZR","Zach Randolph","Memphis Grizzlies",R),
])

# ─── MANUSCRIPTS ──────────────────────────────────────────────────
add_cards("Manuscripts", [
    ("MS-AD","Ayo Dosunmu","Chicago Bulls",R),("MS-AH","Aaron Holiday","Houston Rockets",R),("MS-AJ","Andre Jackson Jr.","Milwaukee Bucks",R),
    ("MS-AJJ","AJ Johnson","Washington Wizards",R),("MS-AM","Alijah Martin","Toronto Raptors",T),("MS-AN","Aaron Nesmith","Indiana Pacers",R),
    ("MS-AS","Alex Sarr","Washington Wizards",R),("MS-AT","Adou Thiero","Los Angeles Lakers",T),("MS-AW","Amari Williams","Boston Celtics",T),
    ("MS-BB","Brooks Barnhizer","Oklahoma City Thunder",T),("MS-BJ","Bronny James Jr.","Los Angeles Lakers",R),("MS-BM","Brandon Miller","Charlotte Hornets",R),
    ("MS-BS","Baylor Scheierman","Boston Celtics",R),("MS-BSH","Ben Sheppard","Indiana Pacers",R),("MS-CC","Clint Capela","Atlanta Hawks",R),
    ("MS-CLA","Chaz Lanier","Detroit Pistons",T),("MS-DG","Daniel Gafford","Dallas Mavericks",R),("MS-DH","DaRon Holmes II","Denver Nuggets",R),
    ("MS-EG","Eric Gordon","Philadelphia 76ers",R),("MS-GTJ","Gary Trent Jr.","Milwaukee Bucks",R),("MS-GW","Grant Williams","Charlotte Hornets",R),
    ("MS-IH","Isaiah Hartenstein","Oklahoma City Thunder",R),("MS-IS","Isaiah Stewart","Detroit Pistons",R),("MS-JC","Jaylen Clark","Minnesota Timberwolves",R),
    ("MS-JF","Johnny Furphy","Indiana Pacers",R),("MS-JG","Josh Giddey","Chicago Bulls",R),("MS-JJJ","Jaime Jaquez Jr.","Miami Heat",R),
    ("MS-JP","Jakob Poeltl","Toronto Raptors",R),("MS-JS","Javon Small","Memphis Grizzlies",T),("MS-JSO","Jeremy Sochan","San Antonio Spurs",R),
    ("MS-JT","Jayson Tatum","Boston Celtics",R),("MS-JV","Jonas Valanciunas","Sacramento Kings",R),("MS-JVA","Jarred Vanderbilt","Los Angeles Lakers",R),
    ("MS-JW","Jamir Watkins","Washington Wizards",T),("MS-JWE","Jaylen Wells","Memphis Grizzlies",R),("MS-JWI","Jalen Williams","Oklahoma City Thunder",R),
    ("MS-KB","Koby Brea","Phoenix Suns",T),("MS-KG","Kyshawn George","Washington Wizards",R),("MS-KH","Kevin Huerter","Chicago Bulls",R),
    ("MS-KJ","Kam Jones","Indiana Pacers",T),("MS-KM","Kris Murray","Portland Trail Blazers",R),("MS-LM","Liam McNeeley","Charlotte Hornets",T),
    ("MS-MP","Micah Peavy","New Orleans Pelicans",T),("MS-MR","Maxime Raynaud","Sacramento Kings",T),("MS-MS","Marcus Sasser","Detroit Pistons",R),
    ("MS-MSH","Max Shulga","Boston Celtics",T),("MS-MST","Max Strus","Cleveland Cavaliers",R),("MS-MW","Mark Williams","Charlotte Hornets",R),
    ("MS-NB","Nicolas Batum","Los Angeles Clippers",R),("MS-NC","Nic Claxton","Brooklyn Nets",R),("MS-NR","Naz Reid","Minnesota Timberwolves",R),
    ("MS-OI","Oso Ighodaro","Phoenix Suns",R),("MS-OO","Onyeka Okongwu","Atlanta Hawks",R),("MS-OT","Obi Toppin","Indiana Pacers",R),
    ("MS-PD","Pacome Dadiet","New York Knicks",R),("MS-PP","Payton Pritchard","Boston Celtics",R),("MS-QP","Quinten Post","Golden State Warriors",R),
    ("MS-RZ","Jahmai Mashack","Memphis Grizzlies",T),("MS-SC","Seth Curry","Charlotte Hornets",R),("MS-SD","Spencer Dinwiddie","Dallas Mavericks",R),
    ("MS-SH","Scoot Henderson","Portland Trail Blazers",R),("MS-TDS","Tristan da Silva","Orlando Magic",R),("MS-TJD","Trayce Jackson-Davis","Golden State Warriors",R),
    ("MS-TK","Tyler Kolek","New York Knicks",R),("MS-TM","Terance Mann","Atlanta Hawks",R),("MS-TP","Tyrese Proctor","Cleveland Cavaliers",T),
    ("MS-TSM","Tyler Smith","Milwaukee Bucks",R),("MS-WK","Walker Kessler","Utah Jazz",R),("MS-YM","Yves Missi","New Orleans Pelicans",R),
    ("MS-ZR","Zaccharie Risacher","Atlanta Hawks",R),
])

# ─── DUAL AUTOGRAPHS ─────────────────────────────────────────────
add_dual_cards("Dual Autographs", [
    ("DA-AN","Nique Clifford","Sacramento Kings",T,"Asa Newell","Atlanta Hawks",T),
    ("DA-CD","Cooper Flagg","Dallas Mavericks",T,"Dylan Harper","San Antonio Spurs",T),
    ("DA-CJ","Jalen Brunson","New York Knicks",R,"Carmelo Anthony","New York Knicks",R),
    ("DA-EC","Egor Demin","Brooklyn Nets",T,"Collin Murray-Boyles","Toronto Raptors",T),
    ("DA-KA","Ace Bailey","Utah Jazz",T,"Kon Knueppel","Charlotte Hornets",T),
    ("DA-KC","Cedric Coward","Memphis Grizzlies",T,"Khaman Maluach","Phoenix Suns",T),
    ("DA-KH","Hakeem Olajuwon","Houston Rockets",R,"Kevin Durant","Houston Rockets",R),
    ("DA-KJ","Nolan Traore","Brooklyn Nets",T,"Kasparas Jakucionis","Miami Heat",T),
    ("DA-KP","Paul Pierce","Boston Celtics",R,"Kevin Garnett","Boston Celtics",R),
    ("DA-ND","Noa Essengue","Chicago Bulls",T,"Derik Queen","New Orleans Pelicans",T),
    ("DA-TO","Obi Toppin","Indiana Pacers",R,"Tyrese Haliburton","Indiana Pacers",R),
    ("DA-TW","Tyrese Proctor","Cleveland Cavaliers",T,"Walter Clayton Jr.","Utah Jazz",T),
    ("DA-TY","Thomas Sorber","Oklahoma City Thunder",T,"Yang Hansen","Portland Trail Blazers",T),
    ("DA-VS","Victor Wembanyama","San Antonio Spurs",R,"Stephon Castle","San Antonio Spurs",R),
    ("DA-WD","Drake Powell","Brooklyn Nets",T,"Will Riley","Washington Wizards",T),
])

# ─── TRIPLE AUTOGRAPHS ───────────────────────────────────────────
add_triple_cards("Triple Autographs", [
    ("TA-ACM",[("Adou Thiero","Los Angeles Lakers",T),("Cedric Coward","Memphis Grizzlies",T),("Micah Peavy","New Orleans Pelicans",T)]),
    ("TA-CAD",[("Ace Bailey","Utah Jazz",T),("Cooper Flagg","Dallas Mavericks",T),("Dylan Harper","San Antonio Spurs",T)]),
    ("TA-CKK",[("Khaman Maluach","Phoenix Suns",T),("Cooper Flagg","Dallas Mavericks",T),("Kon Knueppel","Charlotte Hornets",T)]),
    ("TA-CSJ",[("Chet Holmgren","Oklahoma City Thunder",R),("Shai Gilgeous-Alexander","Oklahoma City Thunder",R),("Jalen Williams","Oklahoma City Thunder",R)]),
    ("TA-ETW",[("Tyrese Proctor","Cleveland Cavaliers",T),("Egor Demin","Brooklyn Nets",T),("Walter Clayton Jr.","Utah Jazz",T)]),
    ("TA-GKJ",[("Jayson Tatum","Boston Celtics",R),("Giannis Antetokounmpo","Milwaukee Bucks",R),("Kevin Durant","Houston Rockets",R)]),
    ("TA-LSK",[("Kevin Durant","Houston Rockets",R),("LeBron James","Los Angeles Lakers",R),("Stephen Curry","Golden State Warriors",R)]),
    ("TA-NDC",[("Derik Queen","New Orleans Pelicans",T),("Collin Murray-Boyles","Toronto Raptors",T),("Noa Essengue","Chicago Bulls",T)]),
    ("TA-PTS",[("Shaquille O'Neal","Orlando Magic",R),("Tracy McGrady","Orlando Magic",R),("Paolo Banchero","Orlando Magic",R)]),
    ("TA-SZA",[("Zaccharie Risacher","Atlanta Hawks",R),("Alex Sarr","Washington Wizards",R),("Stephon Castle","San Antonio Spurs",R)]),
])

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
