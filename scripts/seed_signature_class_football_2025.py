"""
Seed: 2025 Topps Signature Class Football — Full checklist.
500 base (250 Standard + 250 Chrome), ~594 autograph cards across 16 subsets,
20 Paramount Pairings (multi-subject), 19 insert subset shells.
Parallels/pack odds deferred.
Usage: python3 scripts/seed_signature_class_football_2025.py
"""
import sqlite3, os, json, re, unicodedata

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
db = sqlite3.connect(DB_PATH)
db.execute("PRAGMA journal_mode=WAL")
db.execute("PRAGMA foreign_keys=ON")

box_config = json.dumps({
    "hobby": {"cards_per_pack": 4, "packs_per_box": 8, "boxes_per_case": 12, "autos_per_box": 2, "notes": "Per box: 2 autographs"},
    "hobby_jumbo": {"cards_per_pack": 10, "packs_per_box": 4, "boxes_per_case": 6, "autos_per_box": 4, "notes": "Per box: 4 autographs"},
    "value": {"cards_per_pack": 7, "packs_per_box": 6, "boxes_per_case": None},
    "mega": {"cards_per_pack": 8, "packs_per_box": 10, "boxes_per_case": None},
})

db.execute("""
    INSERT INTO sets (name, sport, season, tier, slug, is_visible,
                      sample_image_url, release_date, box_config, created_at)
    VALUES ('2025 Topps Signature Class Football', 'Football', '2025', 'Standard',
            '2025-topps-signature-class-football', 1,
            '/sets/2025-topps-signature-class-football.jpg', '2026-06-05', ?, '2026-05-29T20:00:00Z')
""", (box_config,))
SET_ID = db.execute("SELECT last_insert_rowid()").fetchone()[0]
print(f"Created set ID: {SET_ID}")

def slugify(t):
    s = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode('ascii')
    s = s.lower().strip(); s = re.sub(r'[^\w\s-]', '', s); s = re.sub(r'[\s_]+', '-', s)
    return re.sub(r'-+', '-', s).strip('-')

_sc = {}
def goc(name, role="athlete"):
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
    db.execute("INSERT INTO players (set_id, name, slug, unique_cards, total_print_run, one_of_ones, insert_set_count, subject_role) VALUES (?, ?, ?, 0, 0, 0, 0, ?)",
               (SET_ID, name, c, role))
    return db.execute("SELECT last_insert_rowid()").fetchone()[0]

def ais(name, is_auto=False):
    db.execute("INSERT INTO insert_sets (set_id, name, is_autograph) VALUES (?, ?, ?)", (SET_ID, name, 1 if is_auto else 0))
    return db.execute("SELECT last_insert_rowid()").fetchone()[0]

def ac(is_id, cards):
    for num, name, team, rc in cards:
        pid = goc(name)
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)",
                   (pid, is_id, str(num), 1 if rc else 0, team))

def ad(is_id, cards):
    for num, n1, n2 in cards:
        p1, p2 = goc(n1), goc(n2)
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, NULL)", (p1, is_id, str(num)))
        a = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a, p2))

def at(is_id, num, names):
    pids = [goc(n) for n in names]
    db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, NULL)", (pids[0], is_id, str(num)))
    a = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    for p in pids[1:]:
        db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a, p))

def ins(name, cards, is_auto=False):
    is_id = ais(name, is_auto)
    ac(is_id, cards)
    print(f"  {name}: {len(cards)} cards")
    return is_id

T = True; F = False

# ─── VETERANS CLASS BASE (Standard, 100 cards) ─────────────────────────────
vets = [
(1,"Trey McBride","Arizona Cardinals",F),(2,"Kyler Murray","Arizona Cardinals",F),(3,"Michael Penix Jr.","Atlanta Falcons",F),(4,"Bijan Robinson","Atlanta Falcons",F),(5,"Lamar Jackson","Baltimore Ravens",F),(6,"Derrick Henry","Baltimore Ravens",F),(7,"Josh Allen","Buffalo Bills",F),(8,"James Cook","Buffalo Bills",F),(9,"Bryce Young","Carolina Panthers",F),(10,"Rome Odunze","Chicago Bears",F),
(11,"Caleb Williams","Chicago Bears",F),(12,"Ja'Marr Chase","Cincinnati Bengals",F),(13,"Joe Burrow","Cincinnati Bengals",F),(14,"Myles Garrett","Cleveland Browns",F),(15,"Dak Prescott","Dallas Cowboys",F),(16,"CeeDee Lamb","Dallas Cowboys",F),(17,"Courtland Sutton","Denver Broncos",F),(18,"Bo Nix","Denver Broncos",F),(19,"Amon-Ra St. Brown","Detroit Lions",F),(20,"Jahmyr Gibbs","Detroit Lions",F),
(21,"Jordan Love","Green Bay Packers",F),(22,"Josh Jacobs","Green Bay Packers",F),(23,"CJ Stroud","Houston Texans",F),(24,"Michael Pittman Jr.","Indianapolis Colts",F),(25,"Jonathan Taylor","Indianapolis Colts",F),(26,"Trevor Lawrence","Jacksonville Jaguars",F),(27,"Travis Etienne Jr.","Jacksonville Jaguars",F),(28,"Xavier Worthy","Kansas City Chiefs",F),(29,"Patrick Mahomes II","Kansas City Chiefs",F),(30,"Justin Herbert","Los Angeles Chargers",F),
(31,"Quentin Johnston","Los Angeles Chargers",F),(32,"Matthew Stafford","Los Angeles Rams",F),(33,"Puka Nacua","Los Angeles Rams",F),(34,"Brock Bowers","Las Vegas Raiders",F),(35,"De'Von Achane","Miami Dolphins",F),(36,"Justin Jefferson","Minnesota Vikings",F),(37,"J.J. McCarthy","Minnesota Vikings",F),(38,"Drake Maye","New England Patriots",F),(39,"Chris Olave","New Orleans Saints",F),(40,"Malik Nabers","New York Giants",F),
(41,"Garrett Wilson","New York Jets",F),(42,"Jalen Hurts","Philadelphia Eagles",F),(43,"Saquon Barkley","Philadelphia Eagles",F),(44,"Aaron Rodgers","Pittsburgh Steelers",F),(45,"Jaylen Warren","Pittsburgh Steelers",F),(46,"Jaxon Smith-Njigba","Seattle Seahawks",F),(47,"Sam Darnold","Seattle Seahawks",F),(48,"Brock Purdy","San Francisco 49ers",F),(49,"Christian McCaffrey","San Francisco 49ers",F),(50,"Baker Mayfield","Tampa Bay Buccaneers",F),
(51,"Mike Evans","Tampa Bay Buccaneers",F),(52,"Bucky Irving","Tampa Bay Buccaneers",F),(53,"George Kittle","San Francisco 49ers",F),(54,"Tony Pollard","Tennessee Titans",F),(55,"Terry McLaurin","Washington Commanders",F),(56,"Deebo Samuel","Washington Commanders",F),(57,"Jayden Daniels","Washington Commanders",F),(58,"Jared Goff","Detroit Lions",F),(59,"Daniel Jones","Indianapolis Colts",F),(60,"Javonte Williams","Dallas Cowboys",F),
(61,"Marvin Harrison Jr.","Arizona Cardinals",F),(62,"Drake London","Atlanta Falcons",F),(63,"DeAndre Hopkins","Baltimore Ravens",F),(64,"Keon Coleman","Buffalo Bills",F),(65,"Xavier Legette","Carolina Panthers",F),(66,"Chuba Hubbard","Carolina Panthers",F),(67,"DJ Moore","Chicago Bears",F),(68,"Cole Kmet","Chicago Bears",F),(69,"Tee Higgins","Cincinnati Bengals",F),(70,"Jerry Jeudy","Cleveland Browns",F),
(71,"David Njoku","Cleveland Browns",F),(72,"George Pickens","Dallas Cowboys",F),(73,"Marvin Mims Jr.","Denver Broncos",F),(74,"Aidan Hutchinson","Detroit Lions",F),(75,"Jayden Reed","Green Bay Packers",F),(76,"Nico Collins","Houston Texans",F),(77,"Joe Mixon","Houston Texans",F),(78,"Alec Pierce","Indianapolis Colts",F),(79,"Brian Thomas Jr.","Jacksonville Jaguars",F),(80,"Travis Kelce","Kansas City Chiefs",F),
(81,"Ladd McConkey","Los Angeles Chargers",F),(82,"Davante Adams","Los Angeles Rams",F),(83,"Maxx Crosby","Las Vegas Raiders",F),(84,"Geno Smith","Las Vegas Raiders",F),(85,"Tua Tagovailoa","Miami Dolphins",F),(86,"Tyreek Hill","Miami Dolphins",F),(87,"Jordan Addison","Minnesota Vikings",F),(88,"Jaylen Waddle","Miami Dolphins",F),(89,"Stefon Diggs","New England Patriots",F),(90,"Alvin Kamara","New Orleans Saints",F),
(91,"Sauce Gardner","Indianapolis Colts",F),(92,"Breece Hall","New York Jets",F),(93,"A.J. Brown","Philadelphia Eagles",F),(94,"DeVonta Smith","Philadelphia Eagles",F),(95,"DK Metcalf","Pittsburgh Steelers",F),(96,"T.J. Watt","Pittsburgh Steelers",F),(97,"Cooper Kupp","Seattle Seahawks",F),(98,"Ricky Pearsall","San Francisco 49ers",F),(99,"Calvin Ridley","Tennessee Titans",F),(100,"Zach Ertz","Washington Commanders",F),
]

# Rookie Class Base (Standard, 50 cards, #101-150)
rookies1 = [
(101,"Cam Ward","Tennessee Titans",T),(102,"Ashton Jeanty","Las Vegas Raiders",T),(103,"Dillon Gabriel","Cleveland Browns",T),(104,"Tyler Shough","New Orleans Saints",T),(105,"Emeka Egbuka","Tampa Bay Buccaneers",T),(106,"Jaxson Dart","New York Giants",T),(107,"Will Howard","Pittsburgh Steelers",T),(108,"Kyle McCord","Philadelphia Eagles",T),(109,"Omarion Hampton","Los Angeles Chargers",T),(110,"Tyler Warren","Indianapolis Colts",T),
(111,"Matthew Golden","Green Bay Packers",T),(112,"Dylan Sampson","Cleveland Browns",T),(113,"Colston Loveland","Chicago Bears",T),(114,"Kaleb Johnson","Pittsburgh Steelers",T),(115,"Quinshon Judkins","Cleveland Browns",T),(116,"Riley Leonard","Indianapolis Colts",T),(117,"TreVeyon Henderson","New England Patriots",T),(118,"Abdul Carter","New York Giants",T),(119,"Cam Skattebo","New York Giants",T),(120,"Elic Ayomanor","Tennessee Titans",T),
(121,"Jalon Walker","Atlanta Falcons",T),(122,"Jayden Higgins","Houston Texans",T),(123,"Mykel Williams","San Francisco 49ers",T),(124,"Tez Johnson","Tampa Bay Buccaneers",T),(125,"Jalen Royals","Kansas City Chiefs",T),(126,"Ollie Gordon II","Miami Dolphins",T),(127,"RJ Harvey","Denver Broncos",T),(128,"Tre Harris III","Los Angeles Chargers",T),(129,"Jack Bech","Las Vegas Raiders",T),(130,"James Pearce Jr.","Atlanta Falcons",T),
(131,"Isaac TeSlaa","Detroit Lions",T),(132,"Nic Scourton","Carolina Panthers",T),(133,"Shemar Stewart","Cincinnati Bengals",T),(134,"Tai Felton","Minnesota Vikings",T),(135,"Will Johnson","Arizona Cardinals",T),(136,"Elijah Arroyo","Seattle Seahawks",T),(137,"Jack Sawyer","Pittsburgh Steelers",T),(138,"Jahdae Barron","Denver Broncos",T),(139,"Kenneth Grant","Miami Dolphins",T),(140,"Malaki Starks","Baltimore Ravens",T),
(141,"Mason Graham","Cleveland Browns",T),(142,"Mason Taylor","New York Jets",T),(143,"Maxwell Hairston","Buffalo Bills",T),(144,"Savion Williams","Green Bay Packers",T),(145,"Tory Horton","Seattle Seahawks",T),(146,"Walter Nolen","Arizona Cardinals",T),(147,"Kyle Williams","New England Patriots",T),(148,"Benjamin Morrison","Tampa Bay Buccaneers",T),(149,"Brady Cook","New York Jets",T),(150,"Derrick Harmon","Pittsburgh Steelers",T),
]

# Rookie Class Base II (Standard, 100 cards, #151-250)
rookies2 = [
(151,"Jalen Milroe","Seattle Seahawks",T),(152,"Harold Fannin Jr.","Cleveland Browns",T),(153,"Jihaad Campbell","Philadelphia Eagles",T),(154,"Kelvin Banks Jr.","New Orleans Saints",T),(155,"Mike Green","Baltimore Ravens",T),(156,"Trey Amos","Washington Commanders",T),(157,"Tyleik Williams","Detroit Lions",T),(158,"Will Campbell","New England Patriots",T),(159,"Xavier Restrepo","Tennessee Titans",T),(160,"Pat Bryant","Denver Broncos",T),
(161,"Quincy Riley","New Orleans Saints",T),(162,"Andrew Mukuba","Philadelphia Eagles",T),(163,"Armand Membou","New York Jets",T),(164,"Bhayshul Tuten","Jacksonville Jaguars",T),(165,"Denzel Burke","Arizona Cardinals",T),(166,"Gunnar Helm","Tennessee Titans",T),(167,"JT Tuimoloau","Indianapolis Colts",T),(168,"Jaylen Reed","Houston Texans",T),(169,"Jordan Burch","Arizona Cardinals",T),(170,"Jordan James","San Francisco 49ers",T),
(171,"Kaden Prather","Buffalo Bills",T),(172,"Kalel Mullings","Tennessee Titans",T),(173,"Landon Jackson","Buffalo Bills",T),(174,"Nick Emmanwori","Seattle Seahawks",T),(175,"Princely Umanmielen","Carolina Panthers",T),(176,"Tyler Baron","New York Jets",T),(177,"Tahj Brooks","Cincinnati Bengals",T),(178,"Terrance Ferguson","Los Angeles Rams",T),(179,"Trevor Etienne","Carolina Panthers",T),(180,"Tyler Booker","Dallas Cowboys",T),
(181,"Dont'e Thornton Jr.","Las Vegas Raiders",T),(182,"Chimere Dike","Tennessee Titans",T),(183,"Damien Martinez","Seattle Seahawks",T),(184,"Danny Stutsman","New Orleans Saints",T),(185,"Devin Neal","New Orleans Saints",T),(186,"Josh Simmons","Kansas City Chiefs",T),(187,"Luke Lachey","Houston Texans",T),(188,"Phil Mafah","Dallas Cowboys",T),(189,'Raheim "Rocket" Sanders',"Los Angeles Chargers",T),(190,"Ricky White III","Seattle Seahawks",T),
(191,"Jay Higgins IV","Baltimore Ravens",T),(192,"Mitchell Evans","Carolina Panthers",T),(193,"Sebastian Castro","Pittsburgh Steelers",T),(194,"Ahmed Hassanein","Detroit Lions",T),(195,"Aireontae Ersery","Houston Texans",T),(196,"Alfred Collins","San Francisco 49ers",T),(197,"Ashton Gillotte","Kansas City Chiefs",T),(198,"Azareye'h Thomas","New York Jets",T),(199,"Barrett Carter","Cincinnati Bengals",T),(200,"Billy Bowman Jr.","Atlanta Falcons",T),
(201,"Bradyn Swinson","New England Patriots",T),(202,"Brashard Smith","Kansas City Chiefs",T),(203,"Cameron Williams","Philadelphia Eagles",T),(204,"Darien Porter","Las Vegas Raiders",T),(205,"Deone Walker","Buffalo Bills",T),(206,"Donovan Ezeiruaku","Dallas Cowboys",T),(207,"Jackson Hawes","Buffalo Bills",T),(208,"Jaylin Noel","Houston Texans",T),(209,"Woody Marks","Houston Texans",T),(210,"Jonas Sanker","New Orleans Saints",T),
(211,"Josaiah Stewart","Los Angeles Rams",T),(212,"Kevin Winston Jr.","Tennessee Titans",T),(213,"Kyle Kennard","Los Angeles Chargers",T),(214,"Malachi Moore","New York Jets",T),(215,"Nick Martin","San Francisco 49ers",T),(216,"Quinn Ewers","Miami Dolphins",T),(217,"Smael Mondon Jr.","Philadelphia Eagles",T),(218,"T.J. Sanders","Buffalo Bills",T),(219,"Tate Ratledge","Detroit Lions",T),(220,"Ty Robinson","Philadelphia Eagles",T),
(221,"Xavier Watts","Atlanta Falcons",T),(222,"Carson Schwesinger","Cleveland Browns",T),(223,"Grey Zabel","Seattle Seahawks",T),(224,"Travis Hunter","Jacksonville Jaguars",T),(225,"Jaydon Blue","Dallas Cowboys",T),(226,"Josh Conerly Jr.","Washington Commanders",T),(227,"Oronde Gadsden II","Los Angeles Chargers",T),(228,"Shedeur Sanders","Cleveland Browns",T),(229,"Darius Alexander","New York Giants",T),(230,"Tetairoa McMillan","Carolina Panthers",T),
(231,"Jaylin Lane","Washington Commanders",T),(232,"Luther Burden III","Chicago Bears",T),(233,"Chris Paul Jr.","Los Angeles Rams",T),(234,"Cobee Bryant","Atlanta Falcons",T),(235,"Jacory Croskey-Merritt","Washington Commanders",T),(236,"Tommy Mellott","Las Vegas Raiders",T),(237,"Jonah Savaiinaea","Miami Dolphins",T),(238,"Lathan Ransom","Carolina Panthers",T),(239,"Omarr Norman-Lott","Kansas City Chiefs",T),(240,"Shemar Turner","Chicago Bears",T),
(241,"Donovan Jackson","Minnesota Vikings",T),(242,"Nick Nash","Atlanta Falcons",T),(243,"Ja'Corey Brooks","Washington Commanders",T),(244,"Marcus Mbow","New York Giants",T),(245,"Beaux Collins","New York Giants",T),(246,"Antwaun Powell-Ryland","Philadelphia Eagles",T),(247,"Caden Prieskorn","Denver Broncos",T),(248,"Kobe Hudson","Carolina Panthers",T),(249,"Wyatt Milum","Jacksonville Jaguars",T),(250,"Jabbar Muhammad","Jacksonville Jaguars",T),
]

# Insert Standard base subsets
ins("Veterans Class Base", vets)
ins("Rookie Class Base", rookies1)
ins("Rookie Class Base II", rookies2)

# Insert Chrome base subsets (same athletes, different card rows)
ins("Veterans Class Chrome Base", vets)  # includes #57 Jayden Daniels
ins("Rookie Class Chrome Base", rookies1)
ins("Rookie Class Chrome Base II", rookies2)

# ─── STANDARD AUTO SUBSETS ──────────────────────────────────────────────────
# Veteran Class Autograph Variation (~74 cards) - use card numbers from source
vet_auto_nums = [1,3,6,7,8,9,10,11,13,14,15,16,17,18,19,20,22,23,24,25,26,27,30,32,33,34,35,36,38,39,40,41,42,44,46,47,48,49,51,52,53,55,57,58,59,60,62,64,66,67,68,70,71,73,74,75,76,78,79,81,82,83,84,85,86,87,90,91,92,93,94,96,99]
vet_auto_cards = [(num, name, team, rc) for num, name, team, rc in vets if num in vet_auto_nums]
ins("Veteran Class Autograph Variation", vet_auto_cards, is_auto=True)

# Rookie Class Autograph Variation I (43 cards)
rc1_auto_nums = [101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,119,120,122,123,124,125,126,127,128,129,133,134,135,136,137,138,139,140,141,142,143,144,145,147,148,149]
rc1_auto_cards = [(num, name, team, rc) for num, name, team, rc in rookies1 if num in rc1_auto_nums]
ins("Rookie Class Autograph Variation I", rc1_auto_cards, is_auto=True)

# Rookie Class Autograph Variation II (~73 cards)
rc2_auto_nums = [153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,176,177,178,179,180,181,182,184,185,187,188,190,191,192,193,194,196,197,199,201,202,203,204,205,206,207,208,209,210,212,213,215,217,218,219,220,221,222,223,224,226,227,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,249,250]
rc2_auto_cards = [(num, name, team, rc) for num, name, team, rc in rookies2 if num in rc2_auto_nums]
ins("Rookie Class Autograph Variation II", rc2_auto_cards, is_auto=True)

# ─── CHROME AUTO SUBSETS ────────────────────────────────────────────────────
# Veterans Class Chrome Autographs (~67 cards)
vet_chrome_auto_nums = [1,3,6,7,8,9,10,11,13,14,15,16,18,19,20,22,23,25,26,27,28,30,32,33,34,35,36,38,39,40,41,42,43,44,46,47,48,49,51,52,53,55,57,58,59,60,62,64,66,67,70,71,74,76,78,79,81,82,83,87,90,91,92,93,94,96]
vet_chrome_auto_cards = [(num, name, team, rc) for num, name, team, rc in vets if num in vet_chrome_auto_nums]
ins("Veterans Class Chrome Autographs", vet_chrome_auto_cards, is_auto=True)

# Rookie Class Chrome Autographs (42 cards - includes #150)
rc1_chrome_auto_nums = [101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,119,120,122,123,124,125,126,127,128,129,133,135,136,137,139,140,141,142,143,144,145,147,148,149,150]
rc1_chrome_auto_cards = [(num, name, team, rc) for num, name, team, rc in rookies1 if num in rc1_chrome_auto_nums]
ins("Rookie Class Chrome Autographs", rc1_chrome_auto_cards, is_auto=True)

# Rookie Class Chrome Autographs II (~63 cards)
rc2_chrome_auto_nums = [153,154,156,157,160,163,164,165,166,167,169,170,171,172,174,176,177,178,179,180,181,182,184,185,188,190,191,192,193,194,196,199,202,203,204,205,206,207,209,212,215,217,218,221,222,223,224,225,228,230,231,232,235,236,237,238,239,241,242,243,245,247,249,250]
rc2_chrome_auto_cards = [(num, name, team, rc) for num, name, team, rc in rookies2 if num in rc2_chrome_auto_nums]
ins("Rookie Class Chrome Autographs II", rc2_chrome_auto_cards, is_auto=True)

# ─── SPECIALTY AUTO SUBSETS ─────────────────────────────────────────────────
ins("Rookie Class Crystal Clear Autographs", [
("RCCL-AJ","Ashton Jeanty","Las Vegas Raiders",T),("RCCL-CL","Colston Loveland","Chicago Bears",T),("RCCL-CS","Cam Skattebo","New York Giants",T),("RCCL-CW","Cam Ward","Tennessee Titans",T),("RCCL-DG","Dillon Gabriel","Cleveland Browns",T),("RCCL-DS","Dylan Sampson","Cleveland Browns",T),("RCCL-EA","Elic Ayomanor","Tennessee Titans",T),("RCCL-EE","Emeka Egbuka","Tampa Bay Buccaneers",T),("RCCL-ITES","Isaac TeSlaa","Detroit Lions",T),("RCCL-JD","Jaxson Dart","New York Giants",T),
("RCCL-JH","Jayden Higgins","Houston Texans",T),("RCCL-JJ","Jordan James","San Francisco 49ers",T),("RCCL-JR","Jalen Royals","Kansas City Chiefs",T),("RCCL-KJ","Kaleb Johnson","Pittsburgh Steelers",T),("RCCL-KMC","Kyle McCord","Philadelphia Eagles",T),("RCCL-LB","Luther Burden III","Chicago Bears",T),("RCCL-MG","Matthew Golden","Green Bay Packers",T),("RCCL-MT","Mason Taylor","New York Jets",T),("RCCL-OG","Ollie Gordon II","Miami Dolphins",T),("RCCL-OH","Omarion Hampton","Los Angeles Chargers",T),
("RCCL-QJ","Quinshon Judkins","Cleveland Browns",T),("RCCL-RH","RJ Harvey","Denver Broncos",T),("RCCL-RIL","Riley Leonard","Indianapolis Colts",T),("RCCL-SW","Savion Williams","Green Bay Packers",T),("RCCL-TH","TreVeyon Henderson","New England Patriots",T),("RCCL-THA","Tre Harris III","Los Angeles Chargers",T),("RCCL-THU","Travis Hunter","Jacksonville Jaguars",T),("RCCL-TJ","Tez Johnson","Tampa Bay Buccaneers",T),("RCCL-TW","Tyler Warren","Indianapolis Colts",T),("RCCL-WH","Will Howard","Pittsburgh Steelers",T),
("RCCL-WMA","Woody Marks","Houston Texans",T),
], is_auto=True)

ins("Veterans Class Crystal Clear Autographs", [
("VCCCA-AP","Adrian Peterson","Minnesota Vikings",F),("VCCCA-BB","Brock Bowers","Las Vegas Raiders",F),("VCCCA-BE","Boomer Esiason","Cincinnati Bengals",F),("VCCCA-BN","Bo Nix","Denver Broncos",F),("VCCCA-BY","Bryce Young","Carolina Panthers",F),("VCCCA-CS","CJ Stroud","Houston Texans",F),("VCCCA-CW","Caleb Williams","Chicago Bears",F),("VCCCA-DB","Drew Bledsoe","New England Patriots",F),("VCCCA-DC","Daunte Culpepper","Minnesota Vikings",F),("VCCCA-DM","Drake Maye","New England Patriots",F),
("VCCCA-DMA","Dan Marino","Miami Dolphins",F),("VCCCA-EM","Eli Manning","New York Giants",F),("VCCCA-GB","Gilbert Brown","Green Bay Packers",F),("VCCCA-JD","Jayden Daniels","Washington Commanders",F),("VCCCA-JH","Jack Ham","Pittsburgh Steelers",F),("VCCCA-JJ","Jim Jeffcoat","Dallas Cowboys",F),("VCCCA-KJ","Keyshawn Johnson","New York Jets",F),("VCCCA-LB","LeRoy Butler","Green Bay Packers",F),("VCCCA-MA","Mike Alstott","Tampa Bay Buccaneers",F),("VCCCA-MN","Malik Nabers","New York Giants",F),
("VCCCA-PB","Plaxico Burress","New York Giants",F),("VCCCA-PM","Peyton Manning","Indianapolis Colts",F),("VCCCA-SA","Shaun Alexander","Seattle Seahawks",F),("VCCCA-XW","Xavier Worthy","Kansas City Chiefs",F),("VCCCA-ZT","Zach Thomas","Miami Dolphins",F),
], is_auto=True)

ins("Legends of Their Class Crystal Clear Autographs", [
("LTCA-BD","Brian Dawkins","Philadelphia Eagles",F),("LTCA-BF","Brett Favre","Green Bay Packers",F),("LTCA-CW","Charles Woodson","Oakland Raiders",F),("LTCA-DF","Doug Flutie","Chicago Bears",F),("LTCA-ES","Emmitt Smith","Dallas Cowboys",F),("LTCA-FG","Frank Gore","San Francisco 49ers",F),("LTCA-HL","Howie Long","Oakland Raiders",F),("LTCA-HW","Hines Ward","Pittsburgh Steelers",F),("LTCA-JE","John Elway","Denver Broncos",F),("LTCA-JM","Joe Montana","San Francisco 49ers",F),
("LTCA-JR","Jerry Rice","San Francisco 49ers",F),("LTCA-LT","Lawrence Taylor","New York Giants",F),("LTCA-RG","Rob Gronkowski","New England Patriots",F),("LTCA-SS","Sterling Sharpe","Green Bay Packers",F),("LTCA-TB","Tom Brady","New England Patriots",F),("LTCA-WP","William Perry","Chicago Bears",F),
], is_auto=True)

ins("Signature Class Autographs", [
("SCL-BB","Brock Bowers","Las Vegas Raiders",F),("SCL-BF","Barry Foster","Pittsburgh Steelers",F),("SCL-BI","Bucky Irving","Tampa Bay Buccaneers",F),("SCL-BN","Bo Nix","Denver Broncos",F),("SCL-BS","Barry Sanders","Detroit Lions",F),("SCL-BY","Bryce Young","Carolina Panthers",F),("SCL-CL","Chris Long","Philadelphia Eagles",F),("SCL-CS","CJ Stroud","Houston Texans",F),("SCL-CW","Caleb Williams","Chicago Bears",F),("SCL-GK","George Kittle","San Francisco 49ers",F),
("SCL-JG","Jahmyr Gibbs","Detroit Lions",F),("SCL-JJ","Justin Jefferson","Minnesota Vikings",F),("SCL-JM","J.J. McCarthy","Minnesota Vikings",F),("SCL-JP","Julius Peppers","Chicago Bears",F),("SCL-JR","Jerry Rice","San Francisco 49ers",F),("SCL-JW","Jason Witten","Dallas Cowboys",F),("SCL-RG","Rob Gronkowski","New England Patriots",F),("SCL-RM","Randy Moss","Minnesota Vikings",F),("SCL-RO","Rome Odunze","Chicago Bears",F),("SCL-TB","Tom Brady","New England Patriots",F),
("SCL-TO","Terrell Owens","Philadelphia Eagles",F),("SCL-TP","Troy Polamalu","Pittsburgh Steelers",F),("SCL-WM","Warren Moon","Houston Oilers",F),("SCL-WP","William Perry","Chicago Bears",F),
], is_auto=True)

ins("HOF Signs", [
("HOF-AP","Adrian Peterson","Minnesota Vikings",F),("HOF-BD","Brian Dawkins","Philadelphia Eagles",F),("HOF-BF","Brett Favre","Green Bay Packers",F),("HOF-CT","Charles Tillman","Chicago Bears",F),("HOF-CW","Charles Woodson","Green Bay Packers",F),("HOF-DB","Drew Bledsoe","New England Patriots",F),("HOF-DBR","Drew Brees","New Orleans Saints",F),("HOF-ES","Emmitt Smith","Dallas Cowboys",F),("HOF-JE","John Elway","Denver Broncos",F),("HOF-JED","Julian Edelman","New England Patriots",F),
("HOF-JT","Jason Taylor","Miami Dolphins",F),("HOF-KW","Kurt Warner","St. Louis Rams",F),("HOF-LT","Lawrence Taylor","New York Giants",F),("HOF-MV","Michael Vick","Atlanta Falcons",F),("HOF-RM","Randy Moss","Minnesota Vikings",F),("HOF-SY","Steve Young","San Francisco 49ers",F),("HOF-TB","Tedy Bruschi","New England Patriots",F),("HOF-TBR","Tim Brown","Oakland Raiders",F),("HOF-TO","Terrell Owens","Philadelphia Eagles",F),
], is_auto=True)

ins("Supreme Signers", [
("SS-AD","Aaron Donald","Los Angeles Rams",F),("SS-AJ","Ashton Jeanty","Las Vegas Raiders",T),("SS-BB","Brock Bowers","Las Vegas Raiders",F),("SS-BF","Brett Favre","Green Bay Packers",F),("SS-BN","Bo Nix","Denver Broncos",F),("SS-BS","Barry Sanders","Detroit Lions",F),("SS-BY","Bryce Young","Carolina Panthers",F),("SS-CS","CJ Stroud","Houston Texans",F),("SS-CW","Caleb Williams","Chicago Bears",F),("SS-CWA","Cam Ward","Tennessee Titans",T),
("SS-DG","Dillon Gabriel","Cleveland Browns",T),("SS-DJ","DeSean Jackson","Philadelphia Eagles",F),("SS-DM","Drake Maye","New England Patriots",F),("SS-DS","Dylan Sampson","Cleveland Browns",T),("SS-EE","Emeka Egbuka","Tampa Bay Buccaneers",T),("SS-JD","Jayden Daniels","Washington Commanders",F),("SS-JDA","Jaxson Dart","New York Giants",T),("SS-JLO","James Lofton","Green Bay Packers",F),("SS-JM","Joe Montana","San Francisco 49ers",F),("SS-JP","Julius Peppers","Chicago Bears",F),
("SS-JR","Jerry Rice","San Francisco 49ers",F),("SS-MN","Malik Nabers","New York Giants",F),("SS-SW","Savion Williams","Green Bay Packers",T),("SS-TB","Tom Brady","New England Patriots",F),("SS-TH","Travis Hunter","Jacksonville Jaguars",T),("SS-XW","Xavier Worthy","Kansas City Chiefs",F),
], is_auto=True)

ins("Signature Classics", [
("SC-AJ","Ashton Jeanty","Las Vegas Raiders",T),("SC-BB","Brock Bowers","Las Vegas Raiders",F),("SC-BN","Bo Nix","Denver Broncos",F),("SC-CL","Carnell Lake","Pittsburgh Steelers",F),("SC-CW","Caleb Williams","Chicago Bears",F),("SC-CWA","Cam Ward","Tennessee Titans",T),("SC-DM","Drake Maye","New England Patriots",F),("SC-EE","Emeka Egbuka","Tampa Bay Buccaneers",T),("SC-EM","Eli Manning","New York Giants",F),("SC-JD","Jayden Daniels","Washington Commanders",F),
("SC-JDA","Jaxson Dart","New York Giants",T),("SC-KW","Kurt Warner","Arizona Cardinals",F),("SC-MA","Mike Alstott","Tampa Bay Buccaneers",F),("SC-MJ","Maurice Jones-Drew","Jacksonville Jaguars",F),("SC-PM","Peyton Manning","Indianapolis Colts",F),("SC-RS","Roger Staubach","Dallas Cowboys",F),("SC-TH","Travis Hunter","Jacksonville Jaguars",T),
], is_auto=True)

ins("Preeminent Ink", [
("PI-AF","Antonio Freeman","Green Bay Packers",F),("PI-AG","Ahman Green","Green Bay Packers",F),("PI-BF","Barry Foster","Pittsburgh Steelers",F),("PI-BJ","Brent Jones","San Francisco 49ers",F),("PI-BS","Billy Sims","Detroit Lions",F),("PI-CF","Chuck Foreman","Minnesota Vikings",F),("PI-CJO","Charlie Joiner","San Diego Chargers",F),("PI-CL","Carnell Lake","Pittsburgh Steelers",F),("PI-CLO","Chris Long","Philadelphia Eagles",F),("PI-CO","Christian Okoye","Kansas City Chiefs",F),
("PI-DC","Daunte Culpepper","Minnesota Vikings",F),("PI-DCH","Deron Cherry","Kansas City Chiefs",F),("PI-DH","Dante Hall","Kansas City Chiefs",F),("PI-DHA","Dan Hampton","Chicago Bears",F),("PI-DR","Dave Robinson","Green Bay Packers",F),("PI-DS","Dwight Stephenson","Miami Dolphins",F),("PI-DSM","Dennis Smith","Denver Broncos",F),("PI-EA","Eric Allen","Philadelphia Eagles",F),("PI-EJ",'Ed "Too Tall" Jones',"Dallas Cowboys",F),("PI-EM","Eric Metcalf","Cleveland Browns",F),
("PI-GB","Gilbert Brown","Green Bay Packers",F),("PI-GL","Greg Lloyd","Pittsburgh Steelers",F),("PI-HG","Hugh Green","Miami Dolphins",F),("PI-HM","Herman Moore","Detroit Lions",F),("PI-IF","Irving Fryar","New England Patriots",F),("PI-JA","Jamal Anderson","Atlanta Falcons",F),("PI-JC","Joe Cribbs","Buffalo Bills",F),("PI-JE","Jason Elam","Denver Broncos",F),("PI-JHI","Jay Hilgenberg","Chicago Bears",F),("PI-JJ","John Jefferson","San Diego Chargers",F),
("PI-JJE","Jim Jeffcoat","Dallas Cowboys",F),("PI-JK","Jevon Kearse","Tennessee Titans",F),("PI-LB","Lance Briggs","Chicago Bears",F),("PI-MH","Merton Hanks","San Francisco 49ers",F),("PI-MR","Mike Rozier","Houston Oilers",F),("PI-MV","Michael Vick","Atlanta Falcons",F),("PI-NA","Neal Anderson","Chicago Bears",F),("PI-NC","Nolan Cromwell","Los Angeles Rams",F),("PI-NS","Neil Smith","Kansas City Chiefs",F),("PI-ON","Ozzie Newsome","Cleveland Browns",F),
("PI-PBU","Plaxico Burress","New York Giants",F),("PI-RH","Rodney Hampton","New York Giants",F),("PI-RY","Ron Yary","Minnesota Vikings",F),("PI-SG","Steve Grogan","New England Patriots",F),("PI-SM","Santana Moss","Washington Redskins",F),("PI-SMO","Stanley Morgan","New England Patriots",F),("PI-ST","Steve Tasker","Buffalo Bills",F),("PI-TM","Tony Mandarich","Green Bay Packers",F),("PI-TN","Terence Newman","Dallas Cowboys",F),
], is_auto=True)

# ─── MULTI-SUBJECT AUTOS ───────────────────────────────────────────────────
scds_id = ais("Signature Class Dual Signatures", is_auto=True)
ad(scds_id, [
("SCDS-BJ","Ashton Jeanty","Brock Bowers"),("SCDS-DS","Jaxson Dart","Cam Skattebo"),
("SCDS-GS","Mason Graham","Carson Schwesinger"),("SCDS-HT","Brian Thomas Jr.","Travis Hunter"),
("SCDS-IE","Emeka Egbuka","Bucky Irving"),("SCDS-LB","Luther Burden III","Colston Loveland"),
("SCDS-MY","Tetairoa McMillan","Bryce Young"),("SCDS-NM","Peyton Manning","Bo Nix"),
("SCDS-PK","George Kittle","Brock Purdy"),("SCDS-WL","Tyler Warren","Riley Leonard"),
])
print(f"  Signature Class Dual Signatures: 10 cards (dual)")

scts_id = ais("Signature Class Triple Signatures", is_auto=True)
for num, names in [
    ("SCTS-BEG",["Matthew Golden","Emeka Egbuka","Luther Burden III"]),
    ("SCTS-CMT",["Colston Loveland","Tyler Warren","Mason Taylor"]),
    ("SCTS-JDB",["Drake Maye","Bo Nix","Jayden Daniels"]),
    ("SCTS-KBM",["Brad Johnson","Mike Alstott","Keyshawn Johnson"]),
    ("SCTS-ROK",["George Kittle","Jerry Rice","Terrell Owens"]),
    ("SCTS-WWY",["Cam Ward","Bryce Young","Caleb Williams"]),
]:
    at(scts_id, num, names)
print(f"  Signature Class Triple Signatures: 6 cards (triple)")

# ─── PARAMOUNT PAIRINGS (20 dual-subject inserts) ──────────────────────────
pp_id = ais("Paramount Pairings")
ad(pp_id, [
("PP-1","Caleb Williams","Rome Odunze"),("PP-2","Cam Skattebo","Jaxson Dart"),
("PP-3","Courtland Sutton","Bo Nix"),("PP-4","Drake Maye","Stefon Diggs"),
("PP-5","Saquon Barkley","Jalen Hurts"),("PP-6","Sam Darnold","Jaxon Smith-Njigba"),
("PP-7","Jonathan Taylor","Daniel Jones"),("PP-8","David Montgomery","Jahmyr Gibbs"),
("PP-9","Baker Mayfield","Emeka Egbuka"),("PP-10","Ladd McConkey","Justin Herbert"),
("PP-11","Patrick Mahomes II","Travis Kelce"),("PP-12","James Cook","Josh Allen"),
("PP-13","CeeDee Lamb","George Pickens"),("PP-14","Ja'Marr Chase","Joe Burrow"),
("PP-15","Fred Warner","Nick Bosa"),("PP-16","Terry McLaurin","Jayden Daniels"),
("PP-17","Bijan Robinson","Michael Penix Jr."),("PP-18","Derrick Henry","Lamar Jackson"),
("PP-19","Aaron Rodgers","DK Metcalf"),("PP-20","Josh Jacobs","Jordan Love"),
])
print(f"  Paramount Pairings: 20 cards (dual)")

# ─── INSERT SUBSET SHELLS (card data pending) ──────────────────────────────
for name in ["Zone Out","After Image","Star Cast","Fluidity","Roses","Shattered",
             "Monarchs of the Game","Leviathans","First Class","Class Action",
             "Odyssey","The Pick","In Session","Class Icons","Sunday Showcase","Draft Dreams"]:
    ais(name)
    print(f"  {name}: 0 cards (shell, data pending)")

# ─── BACKFILL IMAGE IDs ────────────────────────────────────────────────────
db.commit()
updated = db.execute("""
    UPDATE players SET nba_player_id = (SELECT p2.nba_player_id FROM players p2 WHERE p2.name = players.name AND p2.nba_player_id IS NOT NULL LIMIT 1)
    WHERE set_id = ? AND nba_player_id IS NULL AND EXISTS (SELECT 1 FROM players p2 WHERE p2.name = players.name AND p2.nba_player_id IS NOT NULL)
""", (SET_ID,)).rowcount
print(f"\nBackfilled {updated} image IDs")

# ─── SUMMARY ────────────────────────────────────────────────────────────────
db.commit()
tp = db.execute("SELECT COUNT(*) FROM players WHERE set_id = ?", (SET_ID,)).fetchone()[0]
ta = db.execute("SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets ins ON pa.insert_set_id = ins.id WHERE ins.set_id = ?", (SET_ID,)).fetchone()[0]
ts = db.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id = ?", (SET_ID,)).fetchone()[0]

print(f"\n{'='*50}")
print(f"Set ID: {SET_ID}")
print(f"Total subsets: {ts}")
print(f"Total unique athletes: {tp}")
print(f"Total card appearances: {ta}")
print(f"(Insert subset card data pending for 16 subsets)")
db.close()
print("Done!")
