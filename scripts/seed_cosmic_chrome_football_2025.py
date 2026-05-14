"""
Seed: 2025 Topps Cosmic Chrome Football — Full checklist (parallels/box config/odds pending).
200 base, 12+ insert subsets (incl. 10 Planetary Pursuit), 4 auto subset shells.
Usage: python3 scripts/seed_cosmic_chrome_football_2025.py
"""
import sqlite3, os, json

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
db = sqlite3.connect(DB_PATH)
db.execute("PRAGMA journal_mode=WAL")
db.execute("PRAGMA foreign_keys=ON")

# ─── Create Set ──────────────────────────────────────────────────────────────
# TODO: Box config, pack odds, and parallel matrix pending sell sheet
db.execute("""
    INSERT INTO sets (name, sport, season, tier, slug, is_visible,
                      sample_image_url, release_date, created_at)
    VALUES ('2025 Topps Cosmic Chrome Football', 'Football', '2025', 'Chrome',
            '2025-topps-cosmic-chrome-football', 1,
            '/sets/2025-topps-cosmic-chrome-football.jpg', '2026-05-18', '2026-05-13T12:00:00Z')
""")
SET_ID = db.execute("SELECT last_insert_rowid()").fetchone()[0]
print(f"Created set ID: {SET_ID}")

def get_or_create(name):
    row = db.execute("SELECT id FROM players WHERE set_id = ? AND name = ?", (SET_ID, name)).fetchone()
    if row: return row[0]
    db.execute("INSERT INTO players (set_id, name, unique_cards, total_print_run, one_of_ones, insert_set_count) VALUES (?, ?, 0, 0, 0, 0)", (SET_ID, name))
    return db.execute("SELECT last_insert_rowid()").fetchone()[0]

def add_is(name):
    db.execute("INSERT INTO insert_sets (set_id, name) VALUES (?, ?)", (SET_ID, name))
    return db.execute("SELECT last_insert_rowid()").fetchone()[0]

def add_cards(is_id, cards):
    """cards = list of (card_num, name, team, is_rookie)"""
    for num, name, team, rookie in cards:
        pid = get_or_create(name)
        db.execute(
            "INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)",
            (pid, is_id, str(num), 1 if rookie else 0, team))

def add_dual_cards(is_id, cards):
    """cards = list of (card_num, name1, name2)"""
    for num, n1, n2 in cards:
        pid1 = get_or_create(n1)
        pid2 = get_or_create(n2)
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, NULL)", (pid1, is_id, str(num)))
        a_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a_id, pid2))

R = True
F = False

# ─── BASE VETERANS (1-100) ──────────────────────────────────────────────────
base_id = add_is("Base Set")
vet_cards = [
    (1,"Kyler Murray","Arizona Cardinals",F),(2,"Trey Benson","Arizona Cardinals",F),
    (3,"Marvin Harrison Jr.","Arizona Cardinals",F),(4,"Bijan Robinson","Atlanta Falcons",F),
    (5,"Drake London","Atlanta Falcons",F),(6,"Kyle Pitts","Atlanta Falcons",F),
    (7,"Lamar Jackson","Baltimore Ravens",F),(8,"Derrick Henry","Baltimore Ravens",F),
    (9,"Zay Flowers","Baltimore Ravens",F),(10,"Josh Allen","Buffalo Bills",F),
    (11,"James Cook","Buffalo Bills",F),(12,"Keon Coleman","Buffalo Bills",F),
    (13,"Bryce Young","Carolina Panthers",F),(14,"Rico Dowdle","Carolina Panthers",F),
    (15,"Jaycee Horn","Carolina Panthers",F),(16,"Caleb Williams","Chicago Bears",F),
    (17,"D'Andre Swift","Chicago Bears",F),(18,"Rome Odunze","Chicago Bears",F),
    (19,"Joe Burrow","Cincinnati Bengals",F),(20,"Ja'Marr Chase","Cincinnati Bengals",F),
    (21,"Tee Higgins","Cincinnati Bengals",F),(22,"Jerry Jeudy","Cleveland Browns",F),
    (23,"David Njoku","Cleveland Browns",F),(24,"Myles Garrett","Cleveland Browns",F),
    (25,"Dak Prescott","Dallas Cowboys",F),(26,"CeeDee Lamb","Dallas Cowboys",F),
    (27,"George Pickens","Dallas Cowboys",F),(28,"Bo Nix","Denver Broncos",F),
    (29,"Courtland Sutton","Denver Broncos",F),(30,"Pat Surtain II","Denver Broncos",F),
    (31,"Jared Goff","Detroit Lions",F),(32,"Jahmyr Gibbs","Detroit Lions",F),
    (33,"Amon-Ra St. Brown","Detroit Lions",F),(34,"Aidan Hutchinson","Detroit Lions",F),
    (35,"Jordan Love","Green Bay Packers",F),(36,"Josh Jacobs","Green Bay Packers",F),
    (37,"Micah Parsons","Green Bay Packers",F),(38,"CJ Stroud","Houston Texans",F),
    (39,"Nico Collins","Houston Texans",F),(40,"Dalton Schultz","Houston Texans",F),
    (41,"Daniel Jones","Indianapolis Colts",F),(42,"Jonathan Taylor","Indianapolis Colts",F),
    (43,"Sauce Gardner","Indianapolis Colts",F),(44,"Trevor Lawrence","Jacksonville Jaguars",F),
    (45,"Travis Etienne Jr.","Jacksonville Jaguars",F),(46,"Brian Thomas Jr.","Jacksonville Jaguars",F),
    (47,"Patrick Mahomes II","Kansas City Chiefs",F),(48,"Xavier Worthy","Kansas City Chiefs",F),
    (49,"Travis Kelce","Kansas City Chiefs",F),(50,"Geno Smith","Las Vegas Raiders",F),
    (51,"Brock Bowers","Las Vegas Raiders",F),(52,"Maxx Crosby","Las Vegas Raiders",F),
    (53,"Justin Herbert","Los Angeles Chargers",F),(54,"Ladd McConkey","Los Angeles Chargers",F),
    (55,"Derwin James Jr.","Los Angeles Chargers",F),(56,"Matthew Stafford","Los Angeles Rams",F),
    (57,"Kyren Williams","Los Angeles Rams",F),(58,"Puka Nacua","Los Angeles Rams",F),
    (59,"Tua Tagovailoa","Miami Dolphins",F),(60,"De'Von Achane","Miami Dolphins",F),
    (61,"Jaylen Waddle","Miami Dolphins",F),(62,"Tyreek Hill","Miami Dolphins",F),
    (63,"J.J. McCarthy","Minnesota Vikings",F),(64,"Aaron Jones Sr.","Minnesota Vikings",F),
    (65,"Justin Jefferson","Minnesota Vikings",F),(66,"Drake Maye","New England Patriots",F),
    (67,"Stefon Diggs","New England Patriots",F),(68,"Christian Gonzalez","New England Patriots",F),
    (69,"Alvin Kamara","New Orleans Saints",F),(70,"Chris Olave","New Orleans Saints",F),
    (71,"Taysom Hill","New Orleans Saints",F),(72,"Malik Nabers","New York Giants",F),
    (73,"Theo Johnson","New York Giants",F),(74,"Dexter Lawrence II","New York Giants",F),
    (75,"Justin Fields","New York Jets",F),(76,"Breece Hall","New York Jets",F),
    (77,"Quincy Williams","New York Jets",F),(78,"Jalen Hurts","Philadelphia Eagles",F),
    (79,"Saquon Barkley","Philadelphia Eagles",F),(80,"A.J. Brown","Philadelphia Eagles",F),
    (81,"Dallas Goedert","Philadelphia Eagles",F),(82,"Aaron Rodgers","Pittsburgh Steelers",F),
    (83,"DK Metcalf","Pittsburgh Steelers",F),(84,"T.J. Watt","Pittsburgh Steelers",F),
    (85,"Brock Purdy","San Francisco 49ers",F),(86,"Christian McCaffrey","San Francisco 49ers",F),
    (87,"Ricky Pearsall","San Francisco 49ers",F),(88,"George Kittle","San Francisco 49ers",F),
    (89,"Sam Darnold","Seattle Seahawks",F),(90,"Kenneth Walker III","Seattle Seahawks",F),
    (91,"Jaxon Smith-Njigba","Seattle Seahawks",F),(92,"Baker Mayfield","Tampa Bay Buccaneers",F),
    (93,"Bucky Irving","Tampa Bay Buccaneers",F),(94,"Mike Evans","Tampa Bay Buccaneers",F),
    (95,"Tony Pollard","Tennessee Titans",F),(96,"Calvin Ridley","Tennessee Titans",F),
    (97,"T'Vondre Sweat","Tennessee Titans",F),(98,"Jayden Daniels","Washington Commanders",F),
    (99,"Terry McLaurin","Washington Commanders",F),(100,"Deebo Samuel","Washington Commanders",F),
]
add_cards(base_id, vet_cards)

# ─── BASE ROOKIES (101-200) ─────────────────────────────────────────────────
rc_cards = [
    (101,"Walter Nolen","Arizona Cardinals",R),(102,"Will Johnson","Arizona Cardinals",R),
    (103,"Jordan Burch","Arizona Cardinals",R),(104,"Jalon Walker","Atlanta Falcons",R),
    (105,"Billy Bowman Jr.","Atlanta Falcons",R),(106,"Xavier Watts","Atlanta Falcons",R),
    (107,"Malaki Starks","Baltimore Ravens",R),(108,"Mike Green","Baltimore Ravens",R),
    (109,"Teddye Buchanan","Baltimore Ravens",R),(110,"Maxwell Hairston","Buffalo Bills",R),
    (111,"T.J. Sanders","Buffalo Bills",R),(112,"Landon Jackson","Buffalo Bills",R),
    (113,"Tetairoa McMillan","Carolina Panthers",R),(114,"Nic Scourton","Carolina Panthers",R),
    (115,"Trevor Etienne","Carolina Panthers",R),(116,"Colston Loveland","Chicago Bears",R),
    (117,"Luther Burden III","Chicago Bears",R),(118,"Kyle Monangai","Chicago Bears",R),
    (119,"Shemar Stewart","Cincinnati Bengals",R),(120,"Demetrius Knight Jr.","Cincinnati Bengals",R),
    (121,"Barrett Carter","Cincinnati Bengals",R),(122,"Mason Graham","Cleveland Browns",R),
    (123,"Carson Schwesinger","Cleveland Browns",R),(124,"Quinshon Judkins","Cleveland Browns",R),
    (125,"Harold Fannin Jr.","Cleveland Browns",R),(126,"Dillon Gabriel","Cleveland Browns",R),
    (127,"Shedeur Sanders","Cleveland Browns",R),(128,"Tyler Booker","Dallas Cowboys",R),
    (129,"Donovan Ezeiruaku","Dallas Cowboys",R),(130,"Shavon Revel Jr.","Dallas Cowboys",R),
    (131,"Jahdae Barron","Denver Broncos",R),(132,"RJ Harvey","Denver Broncos",R),
    (133,"Pat Bryant","Denver Broncos",R),(134,"Tyleik Williams","Detroit Lions",R),
    (135,"Tate Ratledge","Detroit Lions",R),(136,"Isaac TeSlaa","Detroit Lions",R),
    (137,"Matthew Golden","Green Bay Packers",R),(138,"Anthony Belton","Green Bay Packers",R),
    (139,"Savion Williams","Green Bay Packers",R),(140,"Jayden Higgins","Houston Texans",R),
    (141,"Jaylin Noel","Houston Texans",R),(142,"Woody Marks","Houston Texans",R),
    (143,"Tyler Warren","Indianapolis Colts",R),(144,"JT Tuimoloau","Indianapolis Colts",R),
    (145,"Riley Leonard","Indianapolis Colts",R),(146,"Travis Hunter","Jacksonville Jaguars",R),
    (147,"Bhayshul Tuten","Jacksonville Jaguars",R),(148,"Jack Kiser","Jacksonville Jaguars",R),
    (149,"Josh Simmons","Kansas City Chiefs",R),(150,"Omarr Norman-Lott","Kansas City Chiefs",R),
    (151,"Jalen Royals","Kansas City Chiefs",R),(152,"Ashton Jeanty","Las Vegas Raiders",R),
    (153,"Jack Bech","Las Vegas Raiders",R),(154,"Dont'e Thornton Jr.","Las Vegas Raiders",R),
    (155,"Omarion Hampton","Los Angeles Chargers",R),(156,"Tre Harris III","Los Angeles Chargers",R),
    (157,"Jamaree Caldwell","Los Angeles Chargers",R),(158,"Terrance Ferguson","Los Angeles Rams",R),
    (159,"Josaiah Stewart","Los Angeles Rams",R),(160,"Ty Hamilton","Los Angeles Rams",R),
    (161,"Kenneth Grant","Miami Dolphins",R),(162,"Ollie Gordon II","Miami Dolphins",R),
    (163,"Quinn Ewers","Miami Dolphins",R),(164,"Donovan Jackson","Minnesota Vikings",R),
    (165,"Tai Felton","Minnesota Vikings",R),(166,"Tyrion Ingram-Dawkins","Minnesota Vikings",R),
    (167,"Will Campbell","New England Patriots",R),(168,"TreVeyon Henderson","New England Patriots",R),
    (169,"Kyle Williams","New England Patriots",R),(170,"Kelvin Banks Jr.","New Orleans Saints",R),
    (171,"Tyler Shough","New Orleans Saints",R),(172,"Jonas Sanker","New Orleans Saints",R),
    (173,"Abdul Carter","New York Giants",R),(174,"Jaxson Dart","New York Giants",R),
    (175,"Darius Alexander","New York Giants",R),(176,"Cam Skattebo","New York Giants",R),
    (177,"Armand Membou","New York Jets",R),(178,"Mason Taylor","New York Jets",R),
    (179,"Malachi Moore","New York Jets",R),(180,"Jihaad Campbell","Philadelphia Eagles",R),
    (181,"Andrew Mukuba","Philadelphia Eagles",R),(182,"Kyle McCord","Philadelphia Eagles",R),
    (183,"Derrick Harmon","Pittsburgh Steelers",R),(184,"Kaleb Johnson","Pittsburgh Steelers",R),
    (185,"Will Howard","Pittsburgh Steelers",R),(186,"Mykel Williams","San Francisco 49ers",R),
    (187,"Alfred Collins","San Francisco 49ers",R),(188,"Upton Stout","San Francisco 49ers",R),
    (189,"Nick Emmanwori","Seattle Seahawks",R),(190,"Elijah Arroyo","Seattle Seahawks",R),
    (191,"Jalen Milroe","Seattle Seahawks",R),(192,"Emeka Egbuka","Tampa Bay Buccaneers",R),
    (193,"Benjamin Morrison","Tampa Bay Buccaneers",R),(194,"Tez Johnson","Tampa Bay Buccaneers",R),
    (195,"Cam Ward","Tennessee Titans",R),(196,"Elic Ayomanor","Tennessee Titans",R),
    (197,"Gunnar Helm","Tennessee Titans",R),(198,"Josh Conerly Jr.","Washington Commanders",R),
    (199,"Jaylin Lane","Washington Commanders",R),(200,"Jacory Croskey-Merritt","Washington Commanders",R),
]
add_cards(base_id, rc_cards)
print(f"  Base Set: {len(vet_cards)+len(rc_cards)} cards")

# ─── INSERT SUBSETS ─────────────────────────────────────────────────────────
def add_insert(name, cards):
    is_id = add_is(name)
    add_cards(is_id, cards)
    print(f"  {name}: {len(cards)} cards")
    return is_id

# Light Speed (LS-1 to LS-35)
add_insert("Light Speed", [
    ("LS-1","Kyler Murray","Arizona Cardinals",F),("LS-2","Lamar Jackson","Baltimore Ravens",F),
    ("LS-3","Josh Allen","Buffalo Bills",F),("LS-4","Caleb Williams","Chicago Bears",F),
    ("LS-5","CJ Stroud","Houston Texans",F),("LS-6","Patrick Mahomes II","Kansas City Chiefs",F),
    ("LS-7","Justin Herbert","Los Angeles Chargers",F),("LS-8","Drake Maye","New England Patriots",F),
    ("LS-9","Jalen Hurts","Philadelphia Eagles",F),("LS-10","Jayden Daniels","Washington Commanders",F),
    ("LS-11","Trey Benson","Arizona Cardinals",F),("LS-12","Bijan Robinson","Atlanta Falcons",F),
    ("LS-13","Derrick Henry","Baltimore Ravens",F),("LS-14","James Cook","Buffalo Bills",F),
    ("LS-15","Jahmyr Gibbs","Detroit Lions",F),("LS-16","Jonathan Taylor","Indianapolis Colts",F),
    ("LS-17","De'Von Achane","Miami Dolphins",F),("LS-18","Breece Hall","New York Jets",F),
    ("LS-19","Saquon Barkley","Philadelphia Eagles",F),("LS-20","Christian McCaffrey","San Francisco 49ers",F),
    ("LS-21","Kenneth Walker III","Seattle Seahawks",F),("LS-22","Bucky Irving","Tampa Bay Buccaneers",F),
    ("LS-23","Ja'Marr Chase","Cincinnati Bengals",F),("LS-24","CeeDee Lamb","Dallas Cowboys",F),
    ("LS-25","Jameson Williams","Detroit Lions",F),("LS-26","Brian Thomas Jr.","Jacksonville Jaguars",F),
    ("LS-27","Nico Collins","Houston Texans",F),("LS-28","Xavier Worthy","Kansas City Chiefs",F),
    ("LS-29","Puka Nacua","Los Angeles Rams",F),("LS-30","Tyreek Hill","Miami Dolphins",F),
    ("LS-31","Jaylen Waddle","Miami Dolphins",F),("LS-32","Justin Jefferson","Minnesota Vikings",F),
    ("LS-33","Malik Nabers","New York Giants",F),("LS-34","Jaxon Smith-Njigba","Seattle Seahawks",F),
    ("LS-35","Terry McLaurin","Washington Commanders",F),
])

# Extraterrestrial Talent (ET-1 to ET-25)
add_insert("Extraterrestrial Talent", [
    ("ET-1","Cam Ward","Tennessee Titans",R),("ET-2","Jaxson Dart","New York Giants",R),
    ("ET-3","Ashton Jeanty","Las Vegas Raiders",R),("ET-4","Cam Skattebo","New York Giants",R),
    ("ET-5","Tetairoa McMillan","Carolina Panthers",R),("ET-6","Travis Hunter","Jacksonville Jaguars",R),
    ("ET-7","Josh Allen","Buffalo Bills",F),("ET-8","Dak Prescott","Dallas Cowboys",F),
    ("ET-9","Patrick Mahomes II","Kansas City Chiefs",F),("ET-10","James Cook","Buffalo Bills",F),
    ("ET-11","Josh Jacobs","Green Bay Packers",F),("ET-12","Breece Hall","New York Jets",F),
    ("ET-13","Drake London","Atlanta Falcons",F),("ET-14","George Pickens","Dallas Cowboys",F),
    ("ET-15","Jaylen Waddle","Miami Dolphins",F),("ET-16","Trey McBride","Arizona Cardinals",F),
    ("ET-17","Travis Kelce","Kansas City Chiefs",F),("ET-18","Dexter Lawrence II","New York Giants",F),
    ("ET-19","Aidan Hutchinson","Detroit Lions",F),("ET-20","T.J. Watt","Pittsburgh Steelers",F),
    ("ET-21","Fred Warner","San Francisco 49ers",F),("ET-22","Pat Surtain II","Denver Broncos",F),
    ("ET-23","Derek Stingley Jr.","Houston Texans",F),("ET-24","Kyle Hamilton","Baltimore Ravens",F),
    ("ET-25","Derwin James Jr.","Los Angeles Chargers",F),
])

# Stars in the Night (STN-1 to STN-25)
add_insert("Stars in the Night", [
    ("STN-1","Cam Ward","Tennessee Titans",R),("STN-2","Jaxson Dart","New York Giants",R),
    ("STN-3","Shedeur Sanders","Cleveland Browns",R),("STN-4","Ashton Jeanty","Las Vegas Raiders",R),
    ("STN-5","Cam Skattebo","New York Giants",R),("STN-6","Tetairoa McMillan","Carolina Panthers",R),
    ("STN-7","Luther Burden III","Chicago Bears",R),("STN-8","Emeka Egbuka","Tampa Bay Buccaneers",R),
    ("STN-9","Travis Hunter","Jacksonville Jaguars",R),("STN-10","Tyler Warren","Indianapolis Colts",R),
    ("STN-11","Lamar Jackson","Baltimore Ravens",F),("STN-12","Josh Allen","Buffalo Bills",F),
    ("STN-13","Joe Burrow","Cincinnati Bengals",F),("STN-14","Patrick Mahomes II","Kansas City Chiefs",F),
    ("STN-15","Jahmyr Gibbs","Detroit Lions",F),("STN-16","Saquon Barkley","Philadelphia Eagles",F),
    ("STN-17","Ja'Marr Chase","Cincinnati Bengals",F),("STN-18","CeeDee Lamb","Dallas Cowboys",F),
    ("STN-19","Justin Jefferson","Minnesota Vikings",F),("STN-20","Jaxon Smith-Njigba","Seattle Seahawks",F),
    ("STN-21","Brock Bowers","Las Vegas Raiders",F),("STN-22","George Kittle","San Francisco 49ers",F),
    ("STN-23","Myles Garrett","Cleveland Browns",F),("STN-24","Micah Parsons","Green Bay Packers",F),
    ("STN-25","Pat Surtain II","Denver Broncos",F),
])

# Star Clusters (SC-1 to SC-15) — Dual-subject
sc_id = add_is("Star Clusters")
sc_duals = [
    ("SC-1","Cam Ward","Caleb Williams"),("SC-2","Travis Hunter","Shedeur Sanders"),
    ("SC-3","TreVeyon Henderson","Omarion Hampton"),("SC-4","Baker Mayfield","Kyler Murray"),
    ("SC-5","Jayden Daniels","Lamar Jackson"),("SC-6","Tetairoa McMillan","Bryce Young"),
    ("SC-7","Joe Burrow","Ja'Marr Chase"),("SC-8","CeeDee Lamb","George Pickens"),
    ("SC-9","David Montgomery","Jahmyr Gibbs"),("SC-10","Matthew Golden","Jordan Love"),
    ("SC-11","Nico Collins","CJ Stroud"),("SC-12","Travis Kelce","Patrick Mahomes II"),
    ("SC-13","Ashton Jeanty","Brock Bowers"),("SC-14","Cam Skattebo","Jaxson Dart"),
    ("SC-15","A.J. Brown","Jalen Hurts"),
]
add_dual_cards(sc_id, sc_duals)
print(f"  Star Clusters: {len(sc_duals)} cards (dual-subject)")

# Light Years (LY-1 to LY-20) — Legends
add_insert("Light Years", [
    ("LY-1","John Elway","Denver Broncos",F),("LY-2","Peyton Manning","Indianapolis Colts",F),
    ("LY-3","Tom Brady","New England Patriots",F),("LY-4","Joe Montana","San Francisco 49ers",F),
    ("LY-5","Walter Payton","Chicago Bears",F),("LY-6","Barry Sanders","Detroit Lions",F),
    ("LY-7","Emmitt Smith","Dallas Cowboys",F),("LY-8","Earl Campbell","Houston Oilers",F),
    ("LY-9","Chad Johnson","Cincinnati Bengals",F),("LY-10","Randy Moss","Minnesota Vikings",F),
    ("LY-11","Dan Marino","Miami Dolphins",F),("LY-12","Jerry Rice","San Francisco 49ers",F),
    ("LY-13","Jason Witten","Dallas Cowboys",F),("LY-14","Rob Gronkowski","New England Patriots",F),
    ("LY-15","Aaron Donald","Los Angeles Rams",F),("LY-16","Ray Lewis","Baltimore Ravens",F),
    ("LY-17","Lawrence Taylor","New York Giants",F),("LY-18","Charles Woodson","Green Bay Packers",F),
    ("LY-19","Darrelle Revis","New York Jets",F),("LY-20","Troy Polamalu","Pittsburgh Steelers",F),
])

# Cosmic Dust (CD-1 to CD-20)
add_insert("Cosmic Dust", [
    ("CD-1","Cam Ward","Tennessee Titans",R),("CD-2","Jaxson Dart","New York Giants",R),
    ("CD-3","Shedeur Sanders","Cleveland Browns",R),("CD-4","Ashton Jeanty","Las Vegas Raiders",R),
    ("CD-5","Cam Skattebo","New York Giants",R),("CD-6","Tetairoa McMillan","Carolina Panthers",R),
    ("CD-7","Luther Burden III","Chicago Bears",R),("CD-8","Emeka Egbuka","Tampa Bay Buccaneers",R),
    ("CD-9","Josh Allen","Buffalo Bills",F),("CD-10","Bo Nix","Denver Broncos",F),
    ("CD-11","Patrick Mahomes II","Kansas City Chiefs",F),("CD-12","Jalen Hurts","Philadelphia Eagles",F),
    ("CD-13","Jahmyr Gibbs","Detroit Lions",F),("CD-14","Saquon Barkley","Philadelphia Eagles",F),
    ("CD-15","Ja'Marr Chase","Cincinnati Bengals",F),("CD-16","CeeDee Lamb","Dallas Cowboys",F),
    ("CD-17","Justin Jefferson","Minnesota Vikings",F),("CD-18","Brock Bowers","Las Vegas Raiders",F),
    ("CD-19","George Kittle","San Francisco 49ers",F),("CD-20","Micah Parsons","Green Bay Packers",F),
])

# Cos Play (CP-1 to CP-25)
add_insert("Cos Play", [
    ("CP-1","Cam Ward","Tennessee Titans",R),("CP-2","Jaxson Dart","New York Giants",R),
    ("CP-3","Shedeur Sanders","Cleveland Browns",R),("CP-4","Ashton Jeanty","Las Vegas Raiders",R),
    ("CP-5","Quinshon Judkins","Cleveland Browns",R),("CP-6","Cam Skattebo","New York Giants",R),
    ("CP-7","Tetairoa McMillan","Carolina Panthers",R),("CP-8","Luther Burden III","Chicago Bears",R),
    ("CP-9","Emeka Egbuka","Tampa Bay Buccaneers",R),("CP-10","Travis Hunter","Jacksonville Jaguars",R),
    ("CP-11","Tyler Warren","Indianapolis Colts",R),("CP-12","Lamar Jackson","Baltimore Ravens",F),
    ("CP-13","Josh Allen","Buffalo Bills",F),("CP-14","Joe Burrow","Cincinnati Bengals",F),
    ("CP-15","Patrick Mahomes II","Kansas City Chiefs",F),("CP-16","Bijan Robinson","Atlanta Falcons",F),
    ("CP-17","Jonathan Taylor","Indianapolis Colts",F),("CP-18","Christian McCaffrey","San Francisco 49ers",F),
    ("CP-19","Ja'Marr Chase","Cincinnati Bengals",F),("CP-20","CeeDee Lamb","Dallas Cowboys",F),
    ("CP-21","Amon-Ra St. Brown","Detroit Lions",F),("CP-22","Justin Jefferson","Minnesota Vikings",F),
    ("CP-23","Trey McBride","Arizona Cardinals",F),("CP-24","Micah Parsons","Green Bay Packers",F),
    ("CP-25","Pat Surtain II","Denver Broncos",F),
])

# Supernova (SPN-1 to SPN-25)
add_insert("Supernova", [
    ("SPN-1","Cam Ward","Tennessee Titans",R),("SPN-2","Jaxson Dart","New York Giants",R),
    ("SPN-3","Shedeur Sanders","Cleveland Browns",R),("SPN-4","Ashton Jeanty","Las Vegas Raiders",R),
    ("SPN-5","Omarion Hampton","Los Angeles Chargers",R),("SPN-6","Cam Skattebo","New York Giants",R),
    ("SPN-7","Tetairoa McMillan","Carolina Panthers",R),("SPN-8","Luther Burden III","Chicago Bears",R),
    ("SPN-9","Emeka Egbuka","Tampa Bay Buccaneers",R),("SPN-10","Travis Hunter","Jacksonville Jaguars",R),
    ("SPN-11","Tyler Warren","Indianapolis Colts",R),("SPN-12","Lamar Jackson","Baltimore Ravens",F),
    ("SPN-13","Josh Allen","Buffalo Bills",F),("SPN-14","Joe Burrow","Cincinnati Bengals",F),
    ("SPN-15","Patrick Mahomes II","Kansas City Chiefs",F),("SPN-16","Derrick Henry","Baltimore Ravens",F),
    ("SPN-17","Saquon Barkley","Philadelphia Eagles",F),("SPN-18","Ja'Marr Chase","Cincinnati Bengals",F),
    ("SPN-19","CeeDee Lamb","Dallas Cowboys",F),("SPN-20","Justin Jefferson","Minnesota Vikings",F),
    ("SPN-21","Jaxon Smith-Njigba","Seattle Seahawks",F),("SPN-22","Travis Kelce","Kansas City Chiefs",F),
    ("SPN-23","George Kittle","San Francisco 49ers",F),("SPN-24","Myles Garrett","Cleveland Browns",F),
    ("SPN-25","T.J. Watt","Pittsburgh Steelers",F),
])

# ─── PLANETARY PURSUIT (10 subsets × 10 cards each) ─────────────────────────
pp_planets = [
    ("PPSU", "Planetary Pursuit - Sun"),
    ("PPM", "Planetary Pursuit - Mercury"),
    ("PPV", "Planetary Pursuit - Venus"),
    ("PPEA", "Planetary Pursuit - Earth"),
    ("PPMA", "Planetary Pursuit - Mars"),
    ("PPJ", "Planetary Pursuit - Jupiter"),
    ("PPS", "Planetary Pursuit - Saturn"),
    ("PPU", "Planetary Pursuit - Uranus"),
    ("PPN", "Planetary Pursuit - Neptune"),
    ("PPP", "Planetary Pursuit - Pluto"),
]
pp_players = [
    ("AJ","Ashton Jeanty","Las Vegas Raiders",R),
    ("CS","Cam Skattebo","New York Giants",R),
    ("CW","Cam Ward","Tennessee Titans",R),
    ("EE","Emeka Egbuka","Tampa Bay Buccaneers",R),
    ("JA","Josh Allen","Buffalo Bills",F),
    ("JB","Joe Burrow","Cincinnati Bengals",F),
    ("JD","Jaxson Dart","New York Giants",R),
    ("JJ","Justin Jefferson","Minnesota Vikings",F),
    ("PM","Patrick Mahomes II","Kansas City Chiefs",F),
    ("SB","Saquon Barkley","Philadelphia Eagles",F),
]
for prefix, subset_name in pp_planets:
    is_id = add_is(subset_name)
    cards = [(f"{prefix}-{code}", name, team, rc) for code, name, team, rc in pp_players]
    add_cards(is_id, cards)
    print(f"  {subset_name}: {len(cards)} cards")

# Base Cards Constellation Variation (BCV-1 to BCV-100)
add_insert("Base Cards Constellation Variation", [
    ("BCV-1","Kyler Murray","Arizona Cardinals",F),("BCV-2","Marvin Harrison Jr.","Arizona Cardinals",F),
    ("BCV-3","Bijan Robinson","Atlanta Falcons",F),("BCV-4","Drake London","Atlanta Falcons",F),
    ("BCV-5","Lamar Jackson","Baltimore Ravens",F),("BCV-6","Derrick Henry","Baltimore Ravens",F),
    ("BCV-7","Josh Allen","Buffalo Bills",F),("BCV-8","James Cook","Buffalo Bills",F),
    ("BCV-9","Bryce Young","Carolina Panthers",F),("BCV-10","Caleb Williams","Chicago Bears",F),
    ("BCV-11","Rome Odunze","Chicago Bears",F),("BCV-12","Joe Burrow","Cincinnati Bengals",F),
    ("BCV-13","Ja'Marr Chase","Cincinnati Bengals",F),("BCV-14","Myles Garrett","Cleveland Browns",F),
    ("BCV-15","Dak Prescott","Dallas Cowboys",F),("BCV-16","CeeDee Lamb","Dallas Cowboys",F),
    ("BCV-17","Bo Nix","Denver Broncos",F),("BCV-18","Pat Surtain II","Denver Broncos",F),
    ("BCV-19","Jahmyr Gibbs","Detroit Lions",F),("BCV-20","Amon-Ra St. Brown","Detroit Lions",F),
    ("BCV-21","Jordan Love","Green Bay Packers",F),("BCV-22","Micah Parsons","Green Bay Packers",F),
    ("BCV-23","CJ Stroud","Houston Texans",F),("BCV-24","Nico Collins","Houston Texans",F),
    ("BCV-25","Daniel Jones","Indianapolis Colts",F),("BCV-26","Jonathan Taylor","Indianapolis Colts",F),
    ("BCV-27","Trevor Lawrence","Jacksonville Jaguars",F),("BCV-28","Patrick Mahomes II","Kansas City Chiefs",F),
    ("BCV-29","Travis Kelce","Kansas City Chiefs",F),("BCV-30","Brock Bowers","Las Vegas Raiders",F),
    ("BCV-31","Maxx Crosby","Las Vegas Raiders",F),("BCV-32","Justin Herbert","Los Angeles Chargers",F),
    ("BCV-33","Matthew Stafford","Los Angeles Rams",F),("BCV-34","Puka Nacua","Los Angeles Rams",F),
    ("BCV-35","De'Von Achane","Miami Dolphins",F),("BCV-36","Jaylen Waddle","Miami Dolphins",F),
    ("BCV-37","Justin Jefferson","Minnesota Vikings",F),("BCV-38","Drake Maye","New England Patriots",F),
    ("BCV-39","Alvin Kamara","New Orleans Saints",F),("BCV-40","Chris Olave","New Orleans Saints",F),
    ("BCV-41","Malik Nabers","New York Giants",F),("BCV-42","Breece Hall","New York Jets",F),
    ("BCV-43","Jalen Hurts","Philadelphia Eagles",F),("BCV-44","Saquon Barkley","Philadelphia Eagles",F),
    ("BCV-45","Aaron Rodgers","Pittsburgh Steelers",F),("BCV-46","DK Metcalf","Pittsburgh Steelers",F),
    ("BCV-47","T.J. Watt","Pittsburgh Steelers",F),("BCV-48","Brock Purdy","San Francisco 49ers",F),
    ("BCV-49","Christian McCaffrey","San Francisco 49ers",F),("BCV-50","Jaxon Smith-Njigba","Seattle Seahawks",F),
    ("BCV-51","Baker Mayfield","Tampa Bay Buccaneers",F),("BCV-52","Bucky Irving","Tampa Bay Buccaneers",F),
    ("BCV-53","Tony Pollard","Tennessee Titans",F),("BCV-54","Jayden Daniels","Washington Commanders",F),
    ("BCV-55","Deebo Samuel","Washington Commanders",F),
    ("BCV-56","Tetairoa McMillan","Carolina Panthers",R),("BCV-57","Trevor Etienne","Carolina Panthers",R),
    ("BCV-58","Colston Loveland","Chicago Bears",R),("BCV-59","Luther Burden III","Chicago Bears",R),
    ("BCV-60","Quinshon Judkins","Cleveland Browns",R),("BCV-61","Dillon Gabriel","Cleveland Browns",R),
    ("BCV-62","Shedeur Sanders","Cleveland Browns",R),("BCV-63","Donovan Ezeiruaku","Dallas Cowboys",R),
    ("BCV-64","RJ Harvey","Denver Broncos",R),("BCV-65","Pat Bryant","Denver Broncos",R),
    ("BCV-66","Isaac TeSlaa","Detroit Lions",R),("BCV-67","Matthew Golden","Green Bay Packers",R),
    ("BCV-68","Savion Williams","Green Bay Packers",R),("BCV-69","Jayden Higgins","Houston Texans",R),
    ("BCV-70","Jaylin Noel","Houston Texans",R),("BCV-71","Woody Marks","Houston Texans",R),
    ("BCV-72","Tyler Warren","Indianapolis Colts",R),("BCV-73","Riley Leonard","Indianapolis Colts",R),
    ("BCV-74","Travis Hunter","Jacksonville Jaguars",R),("BCV-75","Jalen Royals","Kansas City Chiefs",R),
    ("BCV-76","Ashton Jeanty","Las Vegas Raiders",R),("BCV-77","Jack Bech","Las Vegas Raiders",R),
    ("BCV-78","Omarion Hampton","Los Angeles Chargers",R),("BCV-79","Tre Harris III","Los Angeles Chargers",R),
    ("BCV-80","Terrance Ferguson","Los Angeles Rams",R),("BCV-81","Ollie Gordon II","Miami Dolphins",R),
    ("BCV-82","Quinn Ewers","Miami Dolphins",R),("BCV-83","Tai Felton","Minnesota Vikings",R),
    ("BCV-84","TreVeyon Henderson","New England Patriots",R),("BCV-85","Tyler Shough","New Orleans Saints",R),
    ("BCV-86","Abdul Carter","New York Giants",R),("BCV-87","Jaxson Dart","New York Giants",R),
    ("BCV-88","Cam Skattebo","New York Giants",R),("BCV-89","Mason Taylor","New York Jets",R),
    ("BCV-90","Jihaad Campbell","Philadelphia Eagles",R),("BCV-91","Kaleb Johnson","Pittsburgh Steelers",R),
    ("BCV-92","Will Howard","Pittsburgh Steelers",R),("BCV-93","Elijah Arroyo","Seattle Seahawks",R),
    ("BCV-94","Jalen Milroe","Seattle Seahawks",R),("BCV-95","Emeka Egbuka","Tampa Bay Buccaneers",R),
    ("BCV-96","Tez Johnson","Tampa Bay Buccaneers",R),("BCV-97","Cam Ward","Tennessee Titans",R),
    ("BCV-98","Elic Ayomanor","Tennessee Titans",R),("BCV-99","Jaylin Lane","Washington Commanders",R),
    ("BCV-100","Jacory Croskey-Merritt","Washington Commanders",R),
])

# Starfractor (SF-1 to SF-100)
add_insert("Starfractor", [
    ("SF-1","Kyler Murray","Arizona Cardinals",F),("SF-2","Marvin Harrison Jr.","Arizona Cardinals",F),
    ("SF-3","Bijan Robinson","Atlanta Falcons",F),("SF-4","Drake London","Atlanta Falcons",F),
    ("SF-5","Lamar Jackson","Baltimore Ravens",F),("SF-6","Derrick Henry","Baltimore Ravens",F),
    ("SF-7","Josh Allen","Buffalo Bills",F),("SF-8","James Cook","Buffalo Bills",F),
    ("SF-9","Bryce Young","Carolina Panthers",F),("SF-10","Caleb Williams","Chicago Bears",F),
    ("SF-11","Rome Odunze","Chicago Bears",F),("SF-12","Joe Burrow","Cincinnati Bengals",F),
    ("SF-13","Ja'Marr Chase","Cincinnati Bengals",F),("SF-14","Myles Garrett","Cleveland Browns",F),
    ("SF-15","Dak Prescott","Dallas Cowboys",F),("SF-16","CeeDee Lamb","Dallas Cowboys",F),
    ("SF-17","Bo Nix","Denver Broncos",F),("SF-18","Pat Surtain II","Denver Broncos",F),
    ("SF-19","David Montgomery","Detroit Lions",F),("SF-20","Amon-Ra St. Brown","Detroit Lions",F),
    ("SF-21","Jordan Love","Green Bay Packers",F),("SF-22","Micah Parsons","Green Bay Packers",F),
    ("SF-23","CJ Stroud","Houston Texans",F),("SF-24","Nico Collins","Houston Texans",F),
    ("SF-25","Jonathan Taylor","Indianapolis Colts",F),("SF-26","Trevor Lawrence","Jacksonville Jaguars",F),
    ("SF-27","Patrick Mahomes II","Kansas City Chiefs",F),("SF-28","Travis Kelce","Kansas City Chiefs",F),
    ("SF-29","Brock Bowers","Las Vegas Raiders",F),("SF-30","Maxx Crosby","Las Vegas Raiders",F),
    ("SF-31","Justin Herbert","Los Angeles Chargers",F),("SF-32","Puka Nacua","Los Angeles Rams",F),
    ("SF-33","De'Von Achane","Miami Dolphins",F),("SF-34","Jaylen Waddle","Miami Dolphins",F),
    ("SF-35","Justin Jefferson","Minnesota Vikings",F),("SF-36","Drake Maye","New England Patriots",F),
    ("SF-37","Alvin Kamara","New Orleans Saints",F),("SF-38","Chris Olave","New Orleans Saints",F),
    ("SF-39","Malik Nabers","New York Giants",F),("SF-40","Breece Hall","New York Jets",F),
    ("SF-41","Jalen Hurts","Philadelphia Eagles",F),("SF-42","Saquon Barkley","Philadelphia Eagles",F),
    ("SF-43","Aaron Rodgers","Pittsburgh Steelers",F),("SF-44","DK Metcalf","Pittsburgh Steelers",F),
    ("SF-45","T.J. Watt","Pittsburgh Steelers",F),("SF-46","Brock Purdy","San Francisco 49ers",F),
    ("SF-47","Christian McCaffrey","San Francisco 49ers",F),("SF-48","Jaxon Smith-Njigba","Seattle Seahawks",F),
    ("SF-49","Baker Mayfield","Tampa Bay Buccaneers",F),("SF-50","Bucky Irving","Tampa Bay Buccaneers",F),
    ("SF-51","Tony Pollard","Tennessee Titans",F),("SF-52","Jayden Daniels","Washington Commanders",F),
    ("SF-53","Deebo Samuel","Washington Commanders",F),
    ("SF-54","Tetairoa McMillan","Carolina Panthers",R),("SF-55","Colston Loveland","Chicago Bears",R),
    ("SF-56","Luther Burden III","Chicago Bears",R),("SF-57","Quinshon Judkins","Cleveland Browns",R),
    ("SF-58","Dillon Gabriel","Cleveland Browns",R),("SF-59","Shedeur Sanders","Cleveland Browns",R),
    ("SF-60","RJ Harvey","Denver Broncos",R),("SF-61","Pat Bryant","Denver Broncos",R),
    ("SF-62","Isaac TeSlaa","Detroit Lions",R),("SF-63","Matthew Golden","Green Bay Packers",R),
    ("SF-64","Jayden Higgins","Houston Texans",R),("SF-65","Jaylin Noel","Houston Texans",R),
    ("SF-66","Woody Marks","Houston Texans",R),("SF-67","Tyler Warren","Indianapolis Colts",R),
    ("SF-68","Travis Hunter","Jacksonville Jaguars",R),("SF-69","Jalen Royals","Kansas City Chiefs",R),
    ("SF-70","Ashton Jeanty","Las Vegas Raiders",R),("SF-71","Omarion Hampton","Los Angeles Chargers",R),
    ("SF-72","Tre Harris III","Los Angeles Chargers",R),("SF-73","Terrance Ferguson","Los Angeles Rams",R),
    ("SF-74","Quinn Ewers","Miami Dolphins",R),("SF-75","Tai Felton","Minnesota Vikings",R),
    ("SF-76","TreVeyon Henderson","New England Patriots",R),("SF-77","Tyler Shough","New Orleans Saints",R),
    ("SF-78","Abdul Carter","New York Giants",R),("SF-79","Jaxson Dart","New York Giants",R),
    ("SF-80","Cam Skattebo","New York Giants",R),("SF-81","Mason Taylor","New York Jets",R),
    ("SF-82","Jihaad Campbell","Philadelphia Eagles",R),("SF-83","Kaleb Johnson","Pittsburgh Steelers",R),
    ("SF-84","Elijah Arroyo","Seattle Seahawks",R),("SF-85","Jalen Milroe","Seattle Seahawks",R),
    ("SF-86","Emeka Egbuka","Tampa Bay Buccaneers",R),("SF-87","Tez Johnson","Tampa Bay Buccaneers",R),
    ("SF-88","Cam Ward","Tennessee Titans",R),("SF-89","Elic Ayomanor","Tennessee Titans",R),
    ("SF-90","Jacory Croskey-Merritt","Washington Commanders",R),
    ("SF-91","Ray Lewis","Baltimore Ravens",F),("SF-92","Jim McMahon","Chicago Bears",F),
    ("SF-93","Chad Johnson","Cincinnati Bengals",F),("SF-94","Michael Irvin","Dallas Cowboys",F),
    ("SF-95","John Elway","Denver Broncos",F),("SF-96","Brett Favre","Green Bay Packers",F),
    ("SF-97","Peyton Manning","Indianapolis Colts",F),("SF-98","Dan Marino","Miami Dolphins",F),
    ("SF-99","Randy Moss","Minnesota Vikings",F),("SF-100","Tom Brady","New England Patriots",F),
])

# Planetarium (PL-1 to PL-25)
add_insert("Planetarium", [
    ("PL-1","Cam Ward","Tennessee Titans",R),("PL-2","Jaxson Dart","New York Giants",R),
    ("PL-3","Shedeur Sanders","Cleveland Browns",R),("PL-4","Ashton Jeanty","Las Vegas Raiders",R),
    ("PL-5","TreVeyon Henderson","New England Patriots",R),("PL-6","Cam Skattebo","New York Giants",R),
    ("PL-7","Tetairoa McMillan","Carolina Panthers",R),("PL-8","Luther Burden III","Chicago Bears",R),
    ("PL-9","Emeka Egbuka","Tampa Bay Buccaneers",R),("PL-10","Travis Hunter","Jacksonville Jaguars",R),
    ("PL-11","Tyler Warren","Indianapolis Colts",R),("PL-12","Lamar Jackson","Baltimore Ravens",F),
    ("PL-13","Josh Allen","Buffalo Bills",F),("PL-14","Patrick Mahomes II","Kansas City Chiefs",F),
    ("PL-15","Drake Maye","New England Patriots",F),("PL-16","Jahmyr Gibbs","Detroit Lions",F),
    ("PL-17","Saquon Barkley","Philadelphia Eagles",F),("PL-18","Ja'Marr Chase","Cincinnati Bengals",F),
    ("PL-19","CeeDee Lamb","Dallas Cowboys",F),("PL-20","Puka Nacua","Los Angeles Rams",F),
    ("PL-21","Justin Jefferson","Minnesota Vikings",F),("PL-22","Brock Bowers","Las Vegas Raiders",F),
    ("PL-23","George Kittle","San Francisco 49ers",F),("PL-24","Myles Garrett","Cleveland Browns",F),
    ("PL-25","Micah Parsons","Green Bay Packers",F),
])

# ─── AUTOGRAPH SUBSET SHELLS (no card data — "(See source)" not provided) ───
# TODO: Auto checklists pending — CCA (68), SFS (26), EQA (29), FFS (25) = 148 cards
for auto_name in [
    "Cosmic Chrome Autograph Variation",
    "Solar Flares Signatures",
    "Equinox Autographs",
    "First Flight Signatures",
]:
    add_is(auto_name)
    print(f"  {auto_name}: 0 cards (checklist pending)")

# ─── Summary ────────────────────────────────────────────────────────────────
db.commit()

total_players = db.execute("SELECT COUNT(*) FROM players WHERE set_id = ?", (SET_ID,)).fetchone()[0]
total_appearances = db.execute("""
    SELECT COUNT(*) FROM player_appearances pa
    JOIN insert_sets ins ON pa.insert_set_id = ins.id WHERE ins.set_id = ?
""", (SET_ID,)).fetchone()[0]
total_subsets = db.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id = ?", (SET_ID,)).fetchone()[0]

print(f"\n{'='*50}")
print(f"Set ID: {SET_ID}")
print(f"Total subsets: {total_subsets}")
print(f"Total unique players: {total_players}")
print(f"Total card appearances: {total_appearances}")
print(f"Expected: 715 (863 minus 148 pending auto checklists)")
print(f"0 parallels (pending sell sheet)")
db.close()
print("Done!")
