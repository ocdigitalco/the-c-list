"""
Seed: 2026 Bowman Baseball — Part 3: All autograph sets.
Usage: python3 scripts/seed_2026_bowman_autographs.py
"""
import sqlite3, os, re

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA foreign_keys=ON")
cur = conn.cursor()

SET_ID = 52

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
        a1 = cur.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, ?)", (p1, is_id, num, t1)).lastrowid
        a2 = cur.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, ?)", (p2, is_id, num, t2)).lastrowid
        cur.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a1, p2))
        cur.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a2, p1))

T = True; R = False

# ─── CHROME PROSPECT AUTOGRAPHS (87 cards) ───────────────────────
cpa_id = get_is_id("Chrome Prospect Autographs")
cpa = [
    ("CPA-AA","Aiva Arquette","Miami Marlins",T),("CPA-AF","Andrew Fischer","Milwaukee Brewers",T),("CPA-AFR","Anthony Frobose","New York Mets",T),
    ("CPA-AG","Adrian Gil","Chicago White Sox",T),("CPA-ANA","Anderson Araujo","Philadelphia Phillies",T),("CPA-AT","Andrew Tess","Baltimore Orioles",T),
    ("CPA-BA","Brailyn Antunez","Milwaukee Brewers",T),("CPA-BB","Blaine Bullard","Toronto Blue Jays",T),("CPA-BC","Billy Carlson","Chicago White Sox",T),
    ("CPA-BG","Breyson Guedez","Athletics",T),("CPA-BI","Brent Iredale","Pittsburgh Pirates",T),("CPA-BT","Brendan Tunink","Los Angeles Dodgers",T),
    ("CPA-CC","Charlie Condon","Colorado Rockies",T),("CPA-CGU","Carlos Gutierrez","San Francisco Giants",T),("CPA-CJ","Coy James","Washington Nationals",T),
    ("CPA-CSC","Caden Scarborough","Texas Rangers",T),("CPA-CV","Carlos Virahonda","Arizona Diamondbacks",T),("CPA-DD","Daniel Dickinson","Milwaukee Brewers",T),
    ("CPA-DDA","David Davalillo","Texas Rangers",T),("CPA-DF","Dauri Fernandez","Cleveland Guardians",T),("CPA-DH","Dasan Hill","Minnesota Twins",T),
    ("CPA-DL","Dillon Lewis","New York Yankees",T),("CPA-DOR","Deniel Ortiz","St. Louis Cardinals",T),("CPA-DP","Daniel Pierce","Tampa Bay Rays",T),
    ("CPA-DSH","David Shields","Kansas City Royals",T),("CPA-EDO","Ethan Dorchies","Milwaukee Brewers",T),("CPA-EF","Edward Florentino","Pittsburgh Pirates",T),
    ("CPA-EH","Ethan Holliday","Colorado Rockies",T),("CPA-EHA","Eric Hartman","Atlanta Braves",T),("CPA-EM","Edgar Montero","Athletics",T),
    ("CPA-EME","Esteban Mejia","Baltimore Orioles",T),("CPA-EW","Eli Willits","Washington Nationals",T),("CPA-GJ","Gage Jump","Athletics",T),
    ("CPA-GL","George Lombard Jr.","New York Yankees",T),("CPA-GR","Gabriel Rodriguez","Cleveland Guardians",T),("CPA-GS","Gage Stanifer","Toronto Blue Jays",T),
    ("CPA-HE","Handelfry Encarnacion","Milwaukee Brewers",T),("CPA-HL","Henry Lalane","New York Yankees",T),("CPA-HR","Hector Ramos","Boston Red Sox",T),
    ("CPA-IJ","Isaiah Jackson","Los Angeles Angels",T),("CPA-JG","Justin Gonzales","Boston Red Sox",T),("CPA-JJ","Jared Jones","Pittsburgh Pirates",T),
    ("CPA-JK","Josh Knoth","Milwaukee Brewers",T),("CPA-JM","Jase Mitchell","Houston Astros",T),("CPA-JQ","Jorge Quintana","San Diego Padres",T),
    ("CPA-JQU","James Quinn-Irons","Tampa Bay Rays",T),("CPA-JS","Juan Sanchez","Toronto Blue Jays",T),("CPA-JSL","Jean Carlos Sio","San Francisco Giants",T),
    ("CPA-JU","Jose Urbina","Tampa Bay Rays",T),("CPA-JW","Jude Warwick","Detroit Tigers",T),("CPA-JWH","Jack Wheeler","Texas Rangers",T),
    ("CPA-KAN","Kade Anderson","Seattle Mariners",T),("CPA-KC","Kendry Chourio","Kansas City Royals",T),("CPA-KG","Konnor Griffin","Pittsburgh Pirates",T),
    ("CPA-KH","Kenly Hunter","St. Louis Cardinals",T),("CPA-KHE","Kehden Hettiger","Philadelphia Phillies",T),("CPA-KMC","Kevin McGonigle","Detroit Tigers",T),
    ("CPA-KSN","Kade Snell","Chicago Cubs",T),("CPA-LA","Luis Arana","Miami Marlins",T),("CPA-LDE","Leo De Vries","Athletics",T),
    ("CPA-MC","Max Clark","Detroit Tigers",T),("CPA-MCH","Moises Chace","Philadelphia Phillies",T),("CPA-MF","Matthew Ferrara","Philadelphia Phillies",T),
    ("CPA-MG","Marconi German","Washington Nationals",T),("CPA-MHO","Marek Houston","Minnesota Twins",T),("CPA-MS","Seojun Moon","Toronto Blue Jays",T),
    ("CPA-NM","Nick Monistere","Houston Astros",T),("CPA-NT","Nelly Taylor","Boston Red Sox",T),("CPA-OC","Owen Carey","Atlanta Braves",T),
    ("CPA-PI","Pedro Ibarguen","Milwaukee Brewers",T),("CPA-PN","Pablo Nunez","Cincinnati Reds",T),("CPA-RB","Roldy Brito","Colorado Rockies",T),
    ("CPA-RC","Ricardo Cova","Seattle Mariners",T),("CPA-RN","Riley Nelson","Cleveland Guardians",T),("CPA-SK","Seong-Jun Kim","Texas Rangers",T),
    ("CPA-SP","Sam Petersen","Washington Nationals",T),("CPA-TB","Travis Bazzana","Cleveland Guardians",T),("CPA-TGI","Trey Gibson","Baltimore Orioles",T),
    ("CPA-TM","Truitt Madonna","San Diego Padres",T),("CPA-TR","T.J. Rumfield","New York Yankees",T),("CPA-TW","Thomas White","Miami Marlins",T),
    ("CPA-VA","Victor Arias","Toronto Blue Jays",T),("CPA-VF","Victor Figueroa","Baltimore Orioles",T),("CPA-WA","Wehiwa Aloy","Baltimore Orioles",T),
    ("CPA-WL","Wei-En Lin","Athletics",T),("CPA-WS","Wyatt Sanford","Pittsburgh Pirates",T),("CPA-YCA","Yojancel Cabrera","Los Angeles Angels",T),
]
add_cards(cpa_id, cpa)
print(f"  Chrome Prospect Autographs: {len(cpa)} cards")

# Build lookup for mirroring
cpa_lookup = {}
for num, name, team, _ in cpa:
    cpa_lookup[num] = get_or_create_player(name)

# ─── CHROME PROSPECT GOLD INK AUTOGRAPHS (47 cards) ──────────────
gi_id = get_is_id("Chrome Prospect Gold Ink Autographs")
gi_codes = ['CPA-AA','CPA-AF','CPA-ANA','CPA-BA','CPA-BB','CPA-BG','CPA-BT','CPA-CJ','CPA-DF','CPA-DH','CPA-DL','CPA-DOR',
    'CPA-DP','CPA-DSH','CPA-EF','CPA-EH','CPA-EM','CPA-EME','CPA-EW','CPA-GJ','CPA-GR','CPA-HE','CPA-HL','CPA-HR',
    'CPA-IJ','CPA-JG','CPA-JQ','CPA-JS','CPA-JW','CPA-KC','CPA-KG','CPA-KH','CPA-KMC','CPA-LA','CPA-LDE','CPA-MG',
    'CPA-MHO','CPA-MS','CPA-NT','CPA-OC','CPA-RB','CPA-SK','CPA-VA','CPA-VF','CPA-WA','CPA-WL','CPA-WS']
for code in gi_codes:
    # Get team from CPA card
    row = cur.execute("SELECT team FROM player_appearances WHERE insert_set_id = ? AND card_number = ?", (cpa_id, code)).fetchone()
    cur.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 1, ?)",
                (cpa_lookup[code], gi_id, code, row[0] if row else None))
print(f"  Chrome Prospect Gold Ink Autographs: {len(gi_codes)} cards")

# ─── CHROME PROSPECT PACKFRACTOR AUTOGRAPHS (39 cards) ────────────
pfa_id = get_is_id("Chrome Prospect Packfractor Autographs")
pfa_codes = ['CPA-AA','CPA-AF','CPA-BA','CPA-BG','CPA-BT','CPA-CJ','CPA-DF','CPA-DH','CPA-DOR','CPA-DP','CPA-DSH','CPA-EF',
    'CPA-EH','CPA-EM','CPA-EW','CPA-GJ','CPA-GR','CPA-HE','CPA-HL','CPA-HR','CPA-JG','CPA-JQ','CPA-JS','CPA-JW',
    'CPA-KC','CPA-KG','CPA-KMC','CPA-LA','CPA-LDE','CPA-MG','CPA-MHO','CPA-MS','CPA-NT','CPA-OC','CPA-RB','CPA-SK',
    'CPA-WA','CPA-WL','CPA-WS']
for code in pfa_codes:
    row = cur.execute("SELECT team FROM player_appearances WHERE insert_set_id = ? AND card_number = ?", (cpa_id, code)).fetchone()
    cur.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 1, ?)",
                (cpa_lookup[code], pfa_id, code, row[0] if row else None))
print(f"  Chrome Prospect Packfractor Autographs: {len(pfa_codes)} cards")

# ─── CHROME ROOKIE AUTOGRAPHS (13 cards) ──────────────────────────
cra_id = get_is_id("Chrome Rookie Autographs")
cra = [
    ("CRA-AF","Alex Freeland","Los Angeles Dodgers",T),("CRA-BH","Brady House","Washington Nationals",T),
    ("CRA-CAG","Jac Caglianone","Kansas City Royals",T),("CRA-CB","Chase Burns","Cincinnati Reds",T),
    ("CRA-CJ","Carter Jensen","Kansas City Royals",T),("CRA-CK","C.J. Kayfus","Cleveland Guardians",T),
    ("CRA-CM","Christian Moore","Los Angeles Angels",T),("CRA-JT","Jonah Tong","New York Mets",T),
    ("CRA-KO","Kazuma Okamoto","Toronto Blue Jays",T),("CRA-MM","Munetaka Murakami","Chicago White Sox",T),
    ("CRA-RA","Roman Anthony","Boston Red Sox",T),("CRA-SS","Sal Stewart","Cincinnati Reds",T),
    ("CRA-TI","Tatsuya Imai","Houston Astros",T),
]
add_cards(cra_id, cra)
print(f"  Chrome Rookie Autographs: {len(cra)} cards")

# ─── DRAFT PICK PAIRINGS (16 dual cards) ──────────────────────────
dpp_id = get_is_id("Draft Pick Pairings")
dpp = [
    ("DPPA-BB","Byron Buxton","Minnesota Twins","Kris Bryant","Colorado Rockies"),
    ("DPPA-BBR","Chase Burns","Cincinnati Reds","Tyler Bremner","Los Angeles Angels"),
    ("DPPA-BC","Dylan Crews","Washington Nationals","Alex Bregman","Houston Astros"),
    ("DPPA-BW","Alex Bregman","Houston Astros","Bobby Witt Jr.","Kansas City Royals"),
    ("DPPA-BWI","Travis Bazzana","Cleveland Guardians","Eli Willits","Washington Nationals"),
    ("DPPA-CA","Kade Anderson","Seattle Mariners","Charlie Condon","Colorado Rockies"),
    ("DPPA-GR","Alex Rodriguez","Seattle Mariners","Ken Griffey Jr.","Seattle Mariners"),
    ("DPPA-JC","Jackson Jobe","Detroit Tigers","Max Clark","Detroit Tigers"),
    ("DPPA-LK","Wyatt Langford","Texas Rangers","Nick Kurtz","Athletics"),
    ("DPPA-LM","Evan Longoria","Tampa Bay Rays","Manny Machado","San Diego Padres"),
    ("DPPA-MS","Max Scherzer","Arizona Diamondbacks","Andrew McCutchen","Pittsburgh Pirates"),
    ("DPPA-RH","Adley Rutschman","Baltimore Orioles","Jackson Holliday","Baltimore Orioles"),
    ("DPPA-SD","Hagen Smith","Chicago White Sox","Liam Doyle","St. Louis Cardinals"),
    ("DPPA-SS","Stephen Strasburg","Washington Nationals","Paul Skenes","Pittsburgh Pirates"),
    ("DPPA-WC","Jac Caglianone","Kansas City Royals","Jacob Wilson","Athletics"),
    ("DPPA-WL","Dave Winfield","San Diego Padres","Barry Larkin","Cincinnati Reds"),
]
add_dual_cards(dpp_id, dpp)
print(f"  Draft Pick Pairings: {len(dpp)} dual cards")

# ─── BOWMAN STERLING AUTOGRAPHS (10 cards) ────────────────────────
bsa_id = get_is_id("Bowman Sterling Autographs")
bsa = [("BSA-1","Max Clark","Detroit Tigers",T),("BSA-2","Julio Rodriguez","Seattle Mariners",R),("BSA-3","Konnor Griffin","Pittsburgh Pirates",T),
    ("BSA-4","Freddie Freeman","Los Angeles Dodgers",R),("BSA-5","Leo De Vries","Athletics",T),("BSA-6","Ethan Holliday","Colorado Rockies",T),
    ("BSA-7","Chase Burns","Cincinnati Reds",T),("BSA-8","Jac Caglianone","Kansas City Royals",T),("BSA-9","Roman Anthony","Boston Red Sox",T),
    ("BSA-10","Jacob Misiorowski","Milwaukee Brewers",T)]
add_cards(bsa_id, bsa)
print(f"  Bowman Sterling Autographs: {len(bsa)} cards")

# ─── ELECTRIC SLUGGERS AUTOGRAPHS (14 cards) ──────────────────────
esa_id = get_is_id("Electric Sluggers Autographs")
esa = [("ESA-1","Samuel Basallo","Baltimore Orioles",T),("ESA-2","Bryce Eldridge","San Francisco Giants",T),("ESA-3","Ethan Holliday","Colorado Rockies",T),
    ("ESA-4","Konnor Griffin","Pittsburgh Pirates",T),("ESA-5","Jesus Made","Milwaukee Brewers",T),("ESA-6","JJ Wetherholt","St. Louis Cardinals",T),
    ("ESA-7","Roman Anthony","Boston Red Sox",T),("ESA-8","Jac Caglianone","Kansas City Royals",T),("ESA-9","Vladimir Guerrero Jr.","Toronto Blue Jays",R),
    ("ESA-10","Juan Soto","New York Mets",R),("ESA-11","Ronald Acuna Jr.","Atlanta Braves",R),("ESA-12","Cal Raleigh","Seattle Mariners",R),
    ("ESA-13","Nick Kurtz","Athletics",T),("ESA-14","Mike Trout","Los Angeles Angels",R)]
add_cards(esa_id, esa)
print(f"  Electric Sluggers Autographs: {len(esa)} cards")

# ─── UNDER THE RADAR AUTOGRAPHS (13 cards) ────────────────────────
ura_id = get_is_id("Under The Radar Autographs")
ura = [("URA-1","Connelly Early","Boston Red Sox",T),("URA-2","Samuel Basallo","Baltimore Orioles",T),("URA-3","Cam Schlittler","New York Yankees",T),
    ("URA-4","Trey Yesavage","Toronto Blue Jays",T),("URA-5","Carson Benge","New York Mets",T),("URA-6","Kyle Teel","Chicago White Sox",T),
    ("URA-7","Sal Stewart","Cincinnati Reds",T),("URA-8","Franklin Arias","Boston Red Sox",T),("URA-9","Josue De Paula","Los Angeles Dodgers",T),
    ("URA-10","Kaelen Culpepper","Minnesota Twins",T),("URA-11","Edward Florentino","Pittsburgh Pirates",T),("URA-12","Colt Emerson","Seattle Mariners",T),
    ("URA-13","Kevin McGonigle","Detroit Tigers",T)]
add_cards(ura_id, ura)
print(f"  Under The Radar Autographs: {len(ura)} cards")

# ─── POWER CHORDS AUTOGRAPHS (15 cards) ───────────────────────────
pca_id = get_is_id("Power Chords Autographs")
pca = [("PCA-1","Mike Trout","Los Angeles Angels",R),("PCA-2","Ronald Acuna Jr.","Atlanta Braves",R),("PCA-3","Juan Soto","New York Mets",R),
    ("PCA-4","Junior Caminero","Tampa Bay Rays",R),("PCA-5","Kevin McGonigle","Detroit Tigers",T),("PCA-6","JJ Wetherholt","St. Louis Cardinals",T),
    ("PCA-7","Cal Raleigh","Seattle Mariners",R),("PCA-8","Bryce Eldridge","San Francisco Giants",T),("PCA-9","Walker Jenkins","Minnesota Twins",T),
    ("PCA-10","Edward Florentino","Pittsburgh Pirates",T),("PCA-11","Christian Moore","Los Angeles Angels",T),("PCA-12","Samuel Basallo","Baltimore Orioles",T),
    ("PCA-13","Roman Anthony","Boston Red Sox",T),("PCA-14","Jac Caglianone","Kansas City Royals",T),("PCA-15","Ethan Holliday","Colorado Rockies",T)]
add_cards(pca_id, pca)
print(f"  Power Chords Autographs: {len(pca)} cards")

# ─── BASE PROSPECT RETAIL AUTOGRAPHS (31 cards) ──────────────────
bpra_id = get_is_id("Base Prospect Retail Autographs")
bpra = [("BPA-AA","Aiva Arquette","Miami Marlins",T),("BPA-AF","Andrew Fischer","Milwaukee Brewers",T),("BPA-AG","Angel Guzman","San Francisco Giants",T),
    ("BPA-AL","Arnaldo Lantigua","Cincinnati Reds",T),("BPA-BM","Blake Mitchell","Kansas City Royals",T),("BPA-CB","Caleb Bonemer","Chicago White Sox",T),
    ("BPA-CBE","Carson Benge","New York Mets",T),("BPA-CE","Colt Emerson","Seattle Mariners",T),("BPA-CJ","Coy James","Washington Nationals",T),
    ("BPA-DP","Daniel Pierce","Tampa Bay Rays",T),("BPA-DT","Diego Tornes","Atlanta Braves",T),("BPA-EC","Ethan Conrad","Chicago Cubs",T),
    ("BPA-EF","Edward Florentino","Pittsburgh Pirates",T),("BPA-EH","Ethan Holliday","Colorado Rockies",T),("BPA-GS","Grant Shepardson","Miami Marlins",T),
    ("BPA-GT","Gavin Turley","Athletics",T),("BPA-JP","Jose Perdomo","Atlanta Braves",T),("BPA-JT","James Tibbs III","Los Angeles Dodgers",T),
    ("BPA-KC","Kaelen Culpepper","Minnesota Twins",T),("BPA-KD","Korbyn Dickerson","Seattle Mariners",T),("BPA-KG","Konnor Griffin","Pittsburgh Pirates",T),
    ("BPA-LP","Luis Pena","Milwaukee Brewers",T),("BPA-MH","Marek Houston","Minnesota Twins",T),("BPA-PM","PJ Morlando","Miami Marlins",T),
    ("BPA-QM","Quinn Mathews","St. Louis Cardinals",T),("BPA-SH","Steele Hall","Cincinnati Reds",T),("BPA-SKI","Seaver King","Washington Nationals",T),
    ("BPA-SM","Shotaro Morii","Athletics",T),("BPA-WA","Wehiwa Aloy","Baltimore Orioles",T),("BPA-WJ","Walker Jenkins","Minnesota Twins",T),
    ("BPA-ZE","Zach Ehrhard","Los Angeles Dodgers",T)]
add_cards(bpra_id, bpra)
print(f"  Base Prospect Retail Autographs: {len(bpra)} cards")

# ─── BASE ROOKIE AND VETERAN RETAIL AUTOGRAPHS (35 cards) ────────
rvra_id = get_is_id("Base Rookie And Veteran Retail Autographs")
rvra = [("PRV-AF","Alex Freeland","Los Angeles Dodgers",T),("PRV-AR","Adley Rutschman","Baltimore Orioles",R),("PRV-AS","AJ Smith-Shawver","Atlanta Braves",R),
    ("PRV-BC","Bubba Chandler","Pittsburgh Pirates",T),("PRV-BE","Bryce Eldridge","San Francisco Giants",T),("PRV-CC","Corbin Carroll","Arizona Diamondbacks",R),
    ("PRV-CE","Connelly Early","Boston Red Sox",T),("PRV-CF","Cody Freeman","Texas Rangers",R),("PRV-CM","Colson Montgomery","Chicago White Sox",T),
    ("PRV-CS","Cam Schlittler","New York Yankees",T),("PRV-CW","Carson Williams","Tampa Bay Rays",T),("PRV-DBE","David Bednar","New York Yankees",R),
    ("PRV-DF","Didier Fuentes","Atlanta Braves",R),("PRV-FT","Fernando Tatis Jr.","San Diego Padres",R),("PRV-HF","Harry Ford","Washington Nationals",T),
    ("PRV-HG","Hunter Goodman","Colorado Rockies",R),("PRV-JC","Jac Caglianone","Kansas City Royals",T),("PRV-JD","Justin Dean","Los Angeles Dodgers",R),
    ("PRV-JM","Jacob Misiorowski","Milwaukee Brewers",T),("PRV-JMA","Jakob Marsee","Miami Marlins",T),("PRV-KB","Kris Bryant","Colorado Rockies",R),
    ("PRV-KK","Kyle Karros","Colorado Rockies",R),("PRV-KT","Kyle Teel","Chicago White Sox",T),("PRV-MT","Mike Trout","Los Angeles Angels",R),
    ("PRV-NK","Nick Kurtz","Athletics",T),("PRV-NL","Nathan Lukes","Toronto Blue Jays",R),("PRV-NM","Nolan McLean","New York Mets",T),
    ("PRV-PT","Payton Tolle","Boston Red Sox",T),("PRV-RA","Roman Anthony","Boston Red Sox",T),("PRV-RAC","Ronald Acuna Jr.","Atlanta Braves",R),
    ("PRV-SB","Samuel Basallo","Baltimore Orioles",T),("PRV-TY","Trey Yesavage","Toronto Blue Jays",T),("PRV-VG","Vladimir Guerrero Jr.","Toronto Blue Jays",R),
    ("PRV-WB","Walker Buehler","Philadelphia Phillies",R),("PRV-WK","Will Klein","Los Angeles Dodgers",R)]
add_cards(rvra_id, rvra)
print(f"  Base Rookie And Veteran Retail Autographs: {len(rvra)} cards")

# ─── ULTIMATE AUTOGRAPH BOOKLET (24 athlete entries on UAC-1) ─────
uab_id = get_is_id("Ultimate Autograph Booklet")
uab_names = [("Josuar Gonzalez","San Francisco Giants"),("Edward Florentino","Pittsburgh Pirates"),("Luis Pena","Milwaukee Brewers"),
    ("Zyhir Hope","Los Angeles Dodgers"),("Carson Benge","New York Mets"),("JoJo Parker","Toronto Blue Jays"),
    ("Steele Hall","Cincinnati Reds"),("Seth Hernandez","Pittsburgh Pirates"),("Liam Doyle","St. Louis Cardinals"),
    ("Kade Anderson","Seattle Mariners"),("Billy Carlson","Chicago White Sox"),("George Lombard Jr.","New York Yankees"),
    ("Charlie Condon","Colorado Rockies"),("JJ Wetherholt","St. Louis Cardinals"),("Jesus Made","Milwaukee Brewers"),
    ("Leo De Vries","Athletics"),("Kevin McGonigle","Detroit Tigers"),("Walker Jenkins","Minnesota Twins"),
    ("Travis Bazzana","Cleveland Guardians"),("Bryce Rainer","Detroit Tigers"),("Ethan Holliday","Colorado Rockies"),
    ("Eli Willits","Washington Nationals"),("Colt Emerson","Seattle Mariners"),("Konnor Griffin","Pittsburgh Pirates")]
for name, team in uab_names:
    pid = get_or_create_player(name)
    cur.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, 'UAC-1', 1, ?)", (pid, uab_id, team))
print(f"  Ultimate Autograph Booklet: {len(uab_names)} entries")

# ─── ALL-AMERICA GAME AUTOGRAPHS (1 card) ────────────────────────
aag_id = get_is_id("All-America Game Autographs")
pid = get_or_create_player("Ethan Holliday")
cur.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, 'AAG-1', 1, 'Colorado Rockies')", (pid, aag_id))
print("  All-America Game Autographs: 1 card")

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
print(f"  Total players: {player_count}")
print(f"  Total appearances: {app_count}")
conn.close()
