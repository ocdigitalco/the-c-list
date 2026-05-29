"""
Seed: 2026 Topps Cosmic Chrome WWE — Full checklist.
200 base, 10 insert subsets (incl. Planetary Pursuit 10x12), 4 auto subsets.
Parallels/pack odds pending.
Usage: python3 scripts/seed_cosmic_chrome_wwe_2026.py
"""
import sqlite3, os, json, re, unicodedata

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
db = sqlite3.connect(DB_PATH)
db.execute("PRAGMA journal_mode=WAL")
db.execute("PRAGMA foreign_keys=ON")

box_config = json.dumps({"hobby": {"cards_per_pack": 4, "packs_per_box": 20, "boxes_per_case": 8}})

db.execute("""
    INSERT INTO sets (name, sport, season, tier, slug, is_visible,
                      sample_image_url, release_date, box_config, created_at)
    VALUES ('2026 Topps Cosmic Chrome WWE', 'Wrestling', '2026', 'Chrome',
            '2026-topps-cosmic-chrome-wwe', 1,
            '/sets/2026-topps-cosmic-chrome-wwe.jpg', '2026-06-04', ?, '2026-05-29T14:00:00Z')
""", (box_config,))
SET_ID = db.execute("SELECT last_insert_rowid()").fetchone()[0]
print(f"Created set ID: {SET_ID}")

def slugify(t):
    s = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode('ascii')
    s = s.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_]+', '-', s)
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
    c = slug
    i = 2
    while c in _sc:
        c = f"{slug}-{i}"; i += 1
    _sc[c] = True
    db.execute("INSERT INTO players (set_id, name, slug, unique_cards, total_print_run, one_of_ones, insert_set_count, subject_role) VALUES (?, ?, ?, 0, 0, 0, 0, ?)",
               (SET_ID, name, c, role))
    return db.execute("SELECT last_insert_rowid()").fetchone()[0]

def ais(name, is_auto=False):
    db.execute("INSERT INTO insert_sets (set_id, name, is_autograph) VALUES (?, ?, ?)", (SET_ID, name, 1 if is_auto else 0))
    return db.execute("SELECT last_insert_rowid()").fetchone()[0]

def ac(is_id, cards):
    for num, name, team, rc in cards:
        pid = goc(name.strip())
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)",
                   (pid, is_id, str(num), 1 if rc else 0, team))

def ad(is_id, cards):
    for num, n1, n2 in cards:
        p1, p2 = goc(n1), goc(n2)
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, NULL)", (p1, is_id, str(num)))
        a = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a, p2))

def am(is_id, num, names):
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

R = True; F = False

# ─── BASE SET (200) ─────────────────────────────────────────────────────────
base_id = ais("Base Set")
base = [
(1,'"The American Nightmare" Cody Rhodes',"Smackdown",F),(2,"Jey Uso","Raw",F),
(3,"Stephanie Vaquer","Raw",F),(4,"Dante Chen","NXT",F),(5,"Jacob Fatu","Smackdown",F),
(6,"John Cena","Legend",F),(7,"Roman Reigns","Raw",F),
(8,'Bobby "The Brain" Heenan',"Legend",F),(9,'"Rowdy" Roddy Piper',"Legend",F),
(10,'Bret "Hit Man" Hart',"Legend",F),(11,"Rikishi","Legend",F),(12,"Iyo Sky","Raw",F),
(13,"Zaria","NXT",F),(14,"R-Truth","Smackdown",F),(15,"Becky Lynch","Raw",F),
(16,'"Stone Cold" Steve Austin',"Legend",F),(17,"Mosh","Legend",F),
(18,"Thrasher","Legend",F),(19,"Jacy Jayne","NXT",F),(20,"Joe Gacy","Smackdown",F),
(21,"Candice LeRae","Smackdown",F),(22,"Penta","Raw",F),(23,"Pete Dunne","Raw",F),
(24,"Lita","Legend",F),(25,"Hulk Hogan","Legend",F),(26,"Cruz Del Toro","Raw",F),
(27,"Dragon Lee","Raw",F),(28,"Joaquin Wilde","Raw",F),(29,"Natalya","Raw",F),
(30,"CM Punk","Raw",F),(31,"Brock Lesnar","WWE",F),(32,"Ethan Page","NXT",F),
(33,"AJ Styles","Raw",F),(34,"Kofi Kingston","Raw",F),(35,"Xavier Woods","Raw",F),
(36,"Myles Borne","NXT",F),(37,"Montez Ford","Smackdown",F),
(38,"Tyler Bate","Raw",F),(39,"Ricky Saints","NXT",F),
(40,"Drew McIntyre","Smackdown",F),(41,"Izzi Dame","NXT",F),
(42,"Bronson Reed","Raw",F),(43,"El Grande Americano","Raw",F),
(44,"Gunther","Raw",F),(45,"Ilja Dragunov","Smackdown",F),(46,"Rusev","Raw",F),
(47,"Ivy Nile","Raw",F),(48,"Elton Prince","Smackdown",F),
(49,"Kiana James","Smackdown",F),(50,"Undertaker","Legend",F),
(51,"Raquel Rodriguez","Raw",F),(52,"Roxanne Perez","Raw",F),
(53,"Brutus Creed","Raw",F),(54,"Julius Creed","Raw",F),(55,"Sheamus","Raw",F),
(56,"Finn Balor","Raw",F),(57,"JD McDonagh","Raw",F),
(58,"Uriah Connors","NXT",R),(59,"Osiris Griffin","NXT",R),
(60,"Fallon Henley","NXT",F),(61,'Jake "The Snake" Roberts',"Legend",F),
(62,"Nikki Cross","Smackdown",F),(63,"Shawn Michaels","Legend",F),
(64,"Solo Sikoa","Smackdown",F),(65,"Damian Priest","Smackdown",F),
(66,"AJ Lee","Raw",F),(67,"Kurt Angle","Legend",F),
(68,'Jesse "The Body" Ventura',"Legend",F),(69,"Rey Mysterio","Raw",F),
(70,"Dominik Mysterio","Raw",F),(71,"Hank Walker","NXT",F),
(72,"Tank Ledger","NXT",F),(73,"Kane","Legend",F),(74,"Stacy Keibler","Legend",F),
(75,"Triple H","Legend",F),(76,"Ludwig Kaiser","Raw",F),
(77,"Bray Wyatt","Legend",F),(78,"Ivar","Raw",F),(79,"Erik","Raw",F),
(80,"Bron Breakker","Raw",F),(81,"Jaida Parker","NXT",F),
(82,"Paul Heyman","Raw",F),(83,"Je'Von Evans","NXT",F),
(84,"Dexter Lumis","Smackdown",F),(85,"Sami Zayn","Smackdown",F),
(86,"Wendy Choo","NXT",F),(87,"The Rock","Legend",F),
(88,"Bubba Ray Dudley","Legend",F),(89,"D-Von Dudley","Legend",F),
(90,"Seth Rollins","Raw",F),(91,"X-Pac","Legend",F),
(92,"Kit Wilson","Smackdown",F),(93,"Kevin Owens","Smackdown",F),
(94,'Channing "Stacks" Lorenzo',"NXT",F),(95,"Trish Stratus","Legend",F),
(96,"Cutler James","NXT",R),(97,"Bronco Nima","NXT",F),(98,"IRS","Legend",F),
(99,'"Million Dollar Man" Ted DiBiase',"Legend",F),(100,"Rhea Ripley","Raw",F),
(101,"Mark Henry","Legend",F),(102,"Shiloh Hill","NXT",R),
(103,'"Mr. Perfect" Curt Hennig',"Legend",F),(104,"Brooks Jensen","NXT",F),
(105,"Sid Vicious","Legend",F),(106,"Jimmy Uso","Smackdown",F),
(107,"Jordynne Grace","NXT",F),(108,"Jasper Troy","NXT",R),
(109,"Bianca Belair","Smackdown",F),(110,"Zelina Vega","Smackdown",F),
(111,"Sol Ruca","NXT",F),(112,"Blake Monroe","NXT",F),
(113,"Skylar Raye","NXT",F),(114,"Arianna Grace","NXT",F),
(115,"Liv Morgan","Raw",F),(116,"Luca Crusifino","NXT",F),
(117,"Tyriek Igwe","NXT",F),(118,"Kendal Grey","NXT",F),
(119,"Talla Tonga","Smackdown",R),(120,"Trick Williams","NXT",F),
(121,"The Miz","Smackdown",F),(122,"Bayley","Raw",F),
(123,"Kelani Jordan","NXT",F),(124,"Tyson Dupont","NXT",F),
(125,"Randy Orton","Smackdown",F),(126,"Josh Briggs","NXT",F),
(127,"Tonga Loa","Smackdown",F),(128,"Yokozuna","Legend",F),
(129,"Zoey Stark","Raw",F),(130,"Tama Tonga","Smackdown",F),
(131,"Tatum Paxley","NXT",F),(132,"Kairi Sane","Raw",F),
(133,"Lash Legend","NXT",F),(134,"Lyra Valkyria","Raw",F),
(135,"Nikki Bella","Raw",F),(136,"Angel","Smackdown",F),
(137,"Berto","Smackdown",F),(138,"Thea Hail","NXT",F),
(139,"Charlie Dempsey","NXT",F),(140,"William Regal","Legend",F),
(141,"LA Knight","Raw",F),(142,"Lexis King","NXT",F),
(143,"Michin","Smackdown",F),(144,"Grayson Waller","Raw",F),
(145,"Maxxine Dupri","Raw",F),(146,"Otis","Raw",F),
(147,"Akira Tozawa","Raw",F),(148,'"Road Dogg" Jesse James',"Legend",F),
(149,"Lola Vice","NXT",F),(150,"Alexa Bliss","Smackdown",F),
(151,"Johnny Gargano","Smackdown",F),(152,"Karmen Petrovic","NXT",F),
(153,"Lainey Reid","NXT",R),(154,"Dion Lennox","NXT",F),
(155,"Andre Chase","NXT",F),(156,"Chelsea Green","Smackdown",F),
(157,"Kale Dixon","NXT",R),(158,"Faarooq","Legend",F),
(159,"Adriana Rizzo","NXT",F),(160,"Tiffany Stratton","Smackdown",F),
(161,"Wren Sinclair","NXT",F),(162,"Alba Fyre","Smackdown",F),
(163,"Giulia","Smackdown",F),(164,"Lucien Price","NXT",F),
(165,"The Godfather","Legend",F),(166,"Carmelo Hayes","Smackdown",F),
(167,"Malik Blade","NXT",F),(168,"B-Fab","Smackdown",F),
(169,"Joe Hendry","NXT",R),(170,"Tavion Heights","NXT",F),
(171,"Nikkita Lyons","NXT",F),(172,"Tyra Mae Steele","NXT",R),
(173,"Shinsuke Nakamura","Smackdown",F),(174,"Niko Vance","NXT",F),
(175,"Charlotte Flair","Smackdown",F),(176,"Shawn Spears","NXT",F),
(177,"Jade Cargill","Smackdown",F),(178,"Noam Dar","NXT",F),
(179,"Angelo Dawkins","Smackdown",F),(180,"Eddie Guerrero","Legend",F),
(181,"Oba Femi","NXT",F),(182,"Aleister Black","Smackdown",F),
(183,"Diesel","Legend",F),(184,"Axiom","Smackdown",F),
(185,"Nathan Frazer","Smackdown",F),(186,"Asuka","Raw",F),
(187,"Naomi","Raw",F),(188,"Austin Theory","Raw",F),
(189,"JC Mateo","Smackdown",F),(190,"Tatanka","Legend",F),
(191,"Rey Fenix","Smackdown",F),(192,"Uncle Howdy","Smackdown",F),
(193,"Jimmy Hart","Legend",F),(194,"Piper Niven","Smackdown",F),
(195,"Tony D'Angelo","NXT",F),(196,"Nia Jax","Smackdown",F),
(197,"Saquon Shugars","NXT",R),(198,"Alex Shelley","Smackdown",F),
(199,"Chris Sabin","Smackdown",F),(200,"Erick Rowan","Smackdown",F),
]
ac(base_id, base)
print(f"  Base Set: {len(base)} cards")

# ─── INSERT SUBSETS ─────────────────────────────────────────────────────────
ins("Galaxy Greats", [
("GG-1",'"Stone Cold" Steve Austin',"Legend",F),("GG-2","Alexa Bliss","Smackdown",F),
("GG-3","Hulk Hogan","Legend",F),("GG-4","CM Punk","Raw",F),
("GG-5","Bray Wyatt","Legend",F),("GG-6","Roman Reigns","Raw",F),
("GG-7","Jacob Fatu","Smackdown",F),("GG-8",'Bret "Hit Man" Hart',"Legend",F),
("GG-9","Seth Rollins","Raw",F),("GG-10","AJ Styles","Raw",F),
("GG-11","John Cena","Legend",F),("GG-12","Sami Zayn","Smackdown",F),
("GG-13","Jey Uso","Raw",F),("GG-14","LA Knight","Raw",F),
("GG-15","Randy Orton","Smackdown",F),("GG-16","Liv Morgan","Raw",F),
("GG-17","Dominik Mysterio","Raw",F),("GG-18","Kurt Angle","Legend",F),
("GG-19",'"The American Nightmare" Cody Rhodes',"Smackdown",F),
("GG-20","Solo Sikoa","Smackdown",F),("GG-21","Charlotte Flair","Smackdown",F),
("GG-22","Becky Lynch","Raw",F),("GG-23","Rhea Ripley","Raw",F),
("GG-24","Bron Breakker","Raw",F),("GG-25","Undertaker","Legend",F),
("GG-26","Kevin Owens","Smackdown",F),("GG-27","Brock Lesnar","WWE",F),
("GG-28","Iyo Sky","Raw",F),("GG-29","Lyra Valkyria","Raw",F),
("GG-30","Shawn Michaels","Legend",F),("GG-31","Zelina Vega","Smackdown",F),
("GG-32","The Rock","Legend",F),("GG-33","Tiffany Stratton","Smackdown",F),
("GG-34","Mark Henry","Legend",F),("GG-35","Drew McIntyre","Smackdown",F),
("GG-36",'"Ravishing" Rick Rude',"Legend",F),("GG-37","Gunther","Raw",F),
("GG-38",'"Rowdy" Roddy Piper',"Legend",F),("GG-39","Bianca Belair","Smackdown",F),
("GG-40","Triple H","Legend",F),
])

ins("Extraterrestrial Talent", [
("ET-1",'"The American Nightmare" Cody Rhodes',"Smackdown",F),("ET-2","Drew McIntyre","Smackdown",F),
("ET-3","Seth Rollins","Raw",F),("ET-4","Jey Uso","Raw",F),
("ET-5","Roman Reigns","Raw",F),("ET-6","Dominik Mysterio","Raw",F),
("ET-7","CM Punk","Raw",F),("ET-8","Alexa Bliss","Smackdown",F),
("ET-9","Tiffany Stratton","Smackdown",F),("ET-10","Sami Zayn","Smackdown",F),
("ET-11","Bianca Belair","Smackdown",F),("ET-12","Rhea Ripley","Raw",F),
("ET-13","Liv Morgan","Raw",F),("ET-14","John Cena","Legend",F),
("ET-15","Iyo Sky","Raw",F),("ET-16","Gunther","Raw",F),
("ET-17","Bron Breakker","Raw",F),("ET-18","Becky Lynch","Raw",F),
("ET-19","Stephanie Vaquer","Raw",F),("ET-20","Lyra Valkyria","Raw",F),
("ET-21","AJ Styles","Raw",F),("ET-22","Damian Priest","Smackdown",F),
("ET-23","Zelina Vega","Smackdown",F),("ET-24","Jacob Fatu","Smackdown",F),
("ET-25","Kevin Owens","Smackdown",F),
])

# Galactic Showdown (20 dual-subject)
gs_id = ais("Galactic Showdown")
ad(gs_id, [
("GS-1",'"Stone Cold" Steve Austin',"The Rock"),("GS-2","Bron Breakker","Sami Zayn"),
("GS-3","Becky Lynch","Charlotte Flair"),("GS-4","John Cena","CM Punk"),
("GS-5","Aleister Black","Damian Priest"),("GS-6","Roman Reigns",'"The American Nightmare" Cody Rhodes'),
("GS-7","Hulk Hogan",'"Rowdy" Roddy Piper'),("GS-8","Rey Mysterio","Eddie Guerrero"),
("GS-9","LA Knight","Jacob Fatu"),("GS-10","Seth Rollins","CM Punk"),
("GS-11","Jey Uso","Roman Reigns"),("GS-12","Hulk Hogan","Ultimate Warrior"),
("GS-13",'"Stone Cold" Steve Austin','Bret "Hit Man" Hart'),
("GS-14","Kurt Angle","Eddie Guerrero"),("GS-15","John Cena","Bray Wyatt"),
("GS-16","Undertaker","Kane"),("GS-17",'"Ravishing" Rick Rude',"Ultimate Warrior"),
("GS-18","John Cena","Randy Orton"),("GS-19","Lita","Trish Stratus"),
("GS-20",'Bret "Hit Man" Hart',"Shawn Michaels"),
])
print(f"  Galactic Showdown: 20 cards (dual)")

# Star Clusters (15 multi-subject)
sc_id = ais("Star Clusters")
am(sc_id, "SC-1", ['Jim "The Anvil" Neidhart', 'Bret "Hit Man" Hart'])
am(sc_id, "SC-2", ["Kevin Nash", "Scott Hall", "Hulk Hogan"])  # Hollywood Hulk Hogan → Hulk Hogan
am(sc_id, "SC-3", ["Iron Sheik", "Nikolai Volkoff"])
am(sc_id, "SC-4", ["Montez Ford", "Angelo Dawkins"])
am(sc_id, "SC-5", ["Billy Gunn", '"Road Dogg" Jesse James'])
am(sc_id, "SC-6", ["Kofi Kingston", "Xavier Woods"])
am(sc_id, "SC-7", ["D-Von Dudley", "Bubba Ray Dudley"])
am(sc_id, "SC-8", ["Raquel Rodriguez", "JD McDonagh", "Roxanne Perez", "Finn Balor", "Dominik Mysterio"])
am(sc_id, "SC-9", ["Maxxine Dupri", "Otis", "Akira Tozawa"])
am(sc_id, "SC-10", ["Bray Wyatt", "Alexa Bliss"])
am(sc_id, "SC-11", ["Nikki Cross", "Joe Gacy", "Erick Rowan", "Uncle Howdy", "Dexter Lumis"])
am(sc_id, "SC-12", ["Tony D'Angelo", "Adriana Rizzo", "Luca Crusifino"])
am(sc_id, "SC-13", ['"Million Dollar Man" Ted DiBiase', "IRS"])
am(sc_id, "SC-14", ["Erik", "Ivar"])
am(sc_id, "SC-15", ["Kit Wilson", "Elton Prince"])
print(f"  Star Clusters: 15 cards (multi-subject)")

# Planetary Pursuit (10 prefixes × 12 athletes = 120 cards)
pp_id = ais("Planetary Pursuit")
pp_prefixes = ["PPE","PPJ","PPM","PPMR","PPN","PPP","PPS","PPST","PPU","PPV"]
pp_athletes = [
    ('"The American Nightmare" Cody Rhodes',"Smackdown",F),("Jey Uso","Raw",F),
    ("Seth Rollins","Raw",F),("CM Punk","Raw",F),("Dominik Mysterio","Raw",F),
    ("Roman Reigns","Raw",F),("Becky Lynch","Raw",F),("Alexa Bliss","Smackdown",F),
    ("John Cena","Legend",F),("AJ Lee","Raw",F),("Brock Lesnar","WWE",F),
    ("Joe Hendry","NXT",R),
]
for prefix in pp_prefixes:
    for i, (name, team, rc) in enumerate(pp_athletes, 1):
        pid = goc(name)
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)",
                   (pid, pp_id, f"{prefix}-{i}", 1 if rc else 0, team))
print(f"  Planetary Pursuit: 120 cards (10 prefixes × 12)")

ins("Light Years", [
("LY-1",'"Stone Cold" Steve Austin',"Legend",F),("LY-2","Becky Lynch","Raw",F),
("LY-3","The Rock","Legend",F),("LY-4","Undertaker","Legend",F),
("LY-5","Seth Rollins","Raw",F),("LY-6","Hulk Hogan","Legend",F),
("LY-7","Triple H","Legend",F),("LY-8",'Bret "Hit Man" Hart',"Legend",F),
("LY-9","Trish Stratus","Legend",F),("LY-10","Kurt Angle","Legend",F),
("LY-11","Randy Orton","Smackdown",F),("LY-12","Shawn Michaels","Legend",F),
("LY-13","CM Punk","Raw",F),("LY-14","Mark Henry","Legend",F),
("LY-15","Charlotte Flair","Smackdown",F),("LY-16",'"The American Nightmare" Cody Rhodes',"Smackdown",F),
("LY-17",'"Rowdy" Roddy Piper',"Legend",F),("LY-18","Roman Reigns","Raw",F),
("LY-19","Eddie Guerrero","Legend",F),("LY-20","John Cena","Legend",F),
])

ins("Cosmic Dust", [
("CD-1","Roman Reigns","Raw",F),("CD-2","John Cena","Legend",F),
("CD-3","Stephanie Vaquer","Raw",F),("CD-4","Dominik Mysterio","Raw",F),
("CD-5","Liv Morgan","Raw",F),("CD-6","The Rock","Legend",F),
("CD-7","Jey Uso","Raw",F),("CD-8","Triple H","Legend",F),
("CD-9","Tiffany Stratton","Smackdown",F),("CD-10",'"The American Nightmare" Cody Rhodes',"Smackdown",F),
("CD-11","Rhea Ripley","Raw",F),("CD-12","Giulia","Smackdown",F),
("CD-13","Becky Lynch","Raw",F),("CD-14","Randy Orton","Smackdown",F),
("CD-15","Charlotte Flair","Smackdown",F),("CD-16",'"Stone Cold" Steve Austin',"Legend",F),
("CD-17","Undertaker","Legend",F),("CD-18","Seth Rollins","Raw",F),
("CD-19","Hulk Hogan","Legend",F),("CD-20","CM Punk","Raw",F),
])

ins("Hyper Nova", [
("HN-1","Oba Femi","NXT",F),("HN-2","Bron Breakker","Raw",F),
("HN-3","Jaida Parker","NXT",F),("HN-4","Giulia","Smackdown",F),
("HN-5","Joe Hendry","NXT",R),("HN-6","Sol Ruca","NXT",F),
("HN-7","Izzi Dame","NXT",F),("HN-8","Je'Von Evans","NXT",F),
("HN-9","Jordynne Grace","NXT",F),("HN-10","Stephanie Vaquer","Raw",F),
("HN-11","Tank Ledger","NXT",F),("HN-12","Ethan Page","NXT",F),
("HN-13","Kelani Jordan","NXT",F),("HN-14","Lexis King","NXT",F),
("HN-15","Josh Briggs","NXT",F),("HN-16","Ricky Saints","NXT",F),
("HN-17","Hank Walker","NXT",F),("HN-18","Axiom","Smackdown",F),
("HN-19","Trick Williams","NXT",F),("HN-20","Nathan Frazer","Smackdown",F),
])

ins("Geocentric", [
("GC-1","Hulk Hogan","Legend",F),("GC-2","Lyra Valkyria","Raw",F),
("GC-3","Roman Reigns","Raw",F),("GC-4","Sol Ruca","NXT",F),
("GC-5","Becky Lynch","Raw",F),("GC-6",'"Stone Cold" Steve Austin',"Legend",F),
("GC-7","Oba Femi","NXT",F),("GC-8","CM Punk","Raw",F),
("GC-9","Dominik Mysterio","Raw",F),("GC-10","The Rock","Legend",F),
("GC-11","Zelina Vega","Smackdown",F),("GC-12","Jey Uso","Raw",F),
("GC-13","Undertaker","Legend",F),("GC-14","Tiffany Stratton","Smackdown",F),
("GC-15","Naomi","Raw",F),("GC-16","Iyo Sky","Raw",F),
("GC-17","Randy Orton","Smackdown",F),("GC-18","Jacob Fatu","Smackdown",F),
("GC-19","Seth Rollins","Raw",F),("GC-20","John Cena","Legend",F),
("GC-21","Brock Lesnar","WWE",F),
])

ins("Starfractor", [
("SF-1","Seth Rollins","Raw",F),("SF-2","Bayley","Raw",F),
("SF-3","Bray Wyatt","Legend",F),("SF-4",'Bret "Hit Man" Hart',"Legend",F),
("SF-5",'"Stone Cold" Steve Austin',"Legend",F),("SF-6","Dominik Mysterio","Raw",F),
("SF-7","Jade Cargill","Smackdown",F),("SF-8","Liv Morgan","Raw",F),
("SF-9","Rhea Ripley","Raw",F),("SF-10","Jacob Fatu","Smackdown",F),
("SF-11","Bianca Belair","Smackdown",F),("SF-12","Damian Priest","Smackdown",F),
("SF-13","Jey Uso","Raw",F),("SF-14","Stephanie Vaquer","Raw",F),
("SF-15","Kevin Owens","Smackdown",F),("SF-16","Iyo Sky","Raw",F),
("SF-17","The Rock","Legend",F),("SF-18","CM Punk","Raw",F),
("SF-19","Asuka","Raw",F),("SF-20","Randy Orton","Smackdown",F),
("SF-21","Finn Balor","Raw",F),("SF-22",'"The American Nightmare" Cody Rhodes',"Smackdown",F),
("SF-23","Carmelo Hayes","Smackdown",F),("SF-24","Zelina Vega","Smackdown",F),
("SF-25","Bronson Reed","Raw",F),("SF-26","Rusev","Raw",F),
("SF-27","Penta","Raw",F),("SF-28","El Grande Americano","Raw",F),
("SF-29","Roman Reigns","Raw",F),("SF-30","Charlotte Flair","Smackdown",F),
("SF-31","Solo Sikoa","Smackdown",F),("SF-32","Bron Breakker","Raw",F),
("SF-33","The Miz","Smackdown",F),("SF-34","Sami Zayn","Smackdown",F),
("SF-35","Giulia","Smackdown",F),("SF-36","Gunther","Raw",F),
("SF-37","Becky Lynch","Raw",F),("SF-38","Roxanne Perez","Raw",F),
("SF-39","Jimmy Uso","Smackdown",F),("SF-40","Naomi","Raw",F),
("SF-41","Alexa Bliss","Smackdown",F),("SF-42","AJ Styles","Raw",F),
("SF-43","Drew McIntyre","Smackdown",F),("SF-44","Oba Femi","NXT",F),
("SF-45","LA Knight","Raw",F),("SF-46","Lyra Valkyria","Raw",F),
("SF-47","Austin Theory","Raw",F),("SF-48","John Cena","Legend",F),
("SF-49","Undertaker","Legend",F),("SF-50","Tiffany Stratton","Smackdown",F),
])

# ─── AUTOGRAPH SUBSETS ──────────────────────────────────────────────────────
ins("Cosmic Chrome Autograph Variation", [
("CCA-ARZ","Adriana Rizzo","NXT",F),("CCA-ATO","Akira Tozawa","Raw",F),
("CCA-AUS","Austin Theory","Raw",F),("CCA-BAY","Bayley","Raw",F),
("CCA-BKR","Bron Breakker","Raw",F),("CCA-BRD","Bubba Ray Dudley","Legend",F),
("CCA-BRM","Kane","Legend",F),("CCA-CDE","Charlie Dempsey","NXT",F),
("CCA-CHU","Andre Chase","NXT",F),("CCA-CLR","Candice LeRae","Smackdown",F),
("CCA-CMP","CM Punk","Raw",F),("CCA-DLU","Dexter Lumis","Smackdown",F),
("CCA-DLX","Dion Lennox","NXT",F),("CCA-DMI","Drew McIntyre","Smackdown",F),
("CCA-DMP","Damian Priest","Smackdown",F),("CCA-DOM","Dominik Mysterio","Raw",F),
("CCA-DVD","D-Von Dudley","Legend",F),("CCA-DWK","Angelo Dawkins","Smackdown",F),
("CCA-EOT","Asuka","Raw",F),("CCA-ERK","Erik","Raw",F),
("CCA-ERO","Erick Rowan","Smackdown",F),("CCA-EST","Bianca Belair","Smackdown",F),
("CCA-FLN","Fallon Henley","NXT",F),("CCA-GIU","Giulia","Smackdown",F),
("CCA-GRY","Grayson Waller","Raw",F),("CCA-HBK","Shawn Michaels","Legend",F),
("CCA-HHH","Triple H","Legend",F),("CCA-HMH",'Bret "Hit Man" Hart',"Legend",F),
("CCA-HOW","Uncle Howdy","Smackdown",F),("CCA-IRS","IRS","Legend",F),
("CCA-IVR","Ivar","Raw",F),("CCA-IYO","Iyo Sky","Raw",F),
("CCA-JBV",'Jesse "The Body" Ventura',"Legend",F),("CCA-JCE","John Cena","Legend",F),
("CCA-JCF","Jacob Fatu","Smackdown",F),("CCA-JDC","Jade Cargill","Smackdown",F),
("CCA-JEY","Jey Uso","Raw",F),("CCA-JGC","Joe Gacy","Smackdown",F),
("CCA-KRS","Kairi Sane","Raw",F),("CCA-KVO","Kevin Owens","Smackdown",F),
("CCA-KWI","Kit Wilson","Smackdown",F),("CCA-LIV","Liv Morgan","Raw",F),
("CCA-LMB","Alexa Bliss","Smackdown",F),("CCA-LRD","Lainey Reid","NXT",R),
("CCA-LTA","Lita","Legend",F),("CCA-LUC","Luca Crusifino","NXT",F),
("CCA-LUK","Ludwig Kaiser","Raw",F),("CCA-LYR","Lyra Valkyria","Raw",F),
("CCA-MAN","Becky Lynch","Raw",F),("CCA-MDM",'"Million Dollar Man" Ted DiBiase',"Legend",F),
("CCA-MOF","Montez Ford","Smackdown",F),("CCA-MXD","Maxxine Dupri","Raw",F),
("CCA-MYB","Myles Borne","NXT",F),("CCA-NKI","Nikki Cross","Smackdown",F),
("CCA-OSG","Osiris Griffin","NXT",R),("CCA-OTS","Otis","Raw",F),
("CCA-PAC","X-Pac","Legend",F),("CCA-RCK","The Rock","Legend",F),
("CCA-RDJ",'"Road Dogg" Jesse James',"Legend",F),("CCA-REY","Rey Mysterio","Raw",F),
("CCA-RIK","Rikishi","Legend",F),("CCA-RIP","Rhea Ripley","Raw",F),
("CCA-RKO","Randy Orton","Smackdown",F),("CCA-RKY","Ricky Saints","NXT",F),
("CCA-ROR","Roman Reigns","Raw",F),("CCA-RQR","Raquel Rodriguez","Raw",F),
("CCA-SCA",'"Stone Cold" Steve Austin',"Legend",F),("CCA-SHN","Joe Hendry","NXT",R),
("CCA-SKO","Solo Sikoa","Smackdown",F),("CCA-SOL","Sol Ruca","NXT",F),
("CCA-SQS","Saquon Shugars","NXT",R),("CCA-SRO","Seth Rollins","Raw",F),
("CCA-STK","Stacy Keibler","Legend",F),("CCA-STV","Stephanie Vaquer","Raw",F),
("CCA-SZA","Sami Zayn","Smackdown",F),
("CCA-TAN",'"The American Nightmare" Cody Rhodes',"Smackdown",F),
("CCA-TBI","Brock Lesnar","WWE",F),("CCA-TCW","Sheamus","Raw",F),
("CCA-TD","Tony D'Angelo","NXT",F),("CCA-TDM","Undertaker","Legend",F),
("CCA-TIF","Tiffany Stratton","Smackdown",F),("CCA-TRG","Gunther","Raw",F),
("CCA-TRU","Kurt Angle","Legend",F),("CCA-TST","Trish Stratus","Legend",F),
("CCA-TVH","Tavion Heights","NXT",F),("CCA-USO","Jimmy Uso","Smackdown",F),
("CCA-WOO","Charlotte Flair","Smackdown",F),("CCA-WRN","Wren Sinclair","NXT",F),
("CCA-ZVG","Zelina Vega","Smackdown",F),
], is_auto=True)

ins("Milky Way Marks", [
("MWM-AJL","AJ Lee","Raw",F),("MWM-ASU","Asuka","Raw",F),
("MWM-AXB","Alexa Bliss","Smackdown",F),("MWM-BAY","Bayley","Raw",F),
("MWM-BKL","Becky Lynch","Raw",F),("MWM-CFL","Charlotte Flair","Smackdown",F),
("MWM-CMP","CM Punk","Raw",F),("MWM-DMC","Drew McIntyre","Smackdown",F),
("MWM-DOM","Dominik Mysterio","Raw",F),("MWM-DPR","Damian Priest","Smackdown",F),
("MWM-DTA",'"Stone Cold" Steve Austin',"Legend",F),("MWM-GNT","Gunther","Raw",F),
("MWM-HBK","Shawn Michaels","Legend",F),("MWM-HHH","Triple H","Legend",F),
("MWM-HMH",'Bret "Hit Man" Hart',"Legend",F),("MWM-III","Kurt Angle","Legend",F),
("MWM-IYS","Iyo Sky","Raw",F),("MWM-JAF","Jacob Fatu","Smackdown",F),
("MWM-JEU","Jey Uso","Raw",F),("MWM-JOC","John Cena","Legend",F),
("MWM-KVO","Kevin Owens","Smackdown",F),("MWM-LVM","Liv Morgan","Raw",F),
("MWM-LYV","Lyra Valkyria","Raw",F),("MWM-NAT","Natalya","Raw",F),
("MWM-RBR","Rhea Ripley","Raw",F),("MWM-RKO","Randy Orton","Smackdown",F),
("MWM-RMY","Rey Mysterio","Raw",F),("MWM-ROR","Roman Reigns","Raw",F),
("MWM-SFR","Seth Rollins","Raw",F),("MWM-SZN","Sami Zayn","Smackdown",F),
("MWM-TAN",'"The American Nightmare" Cody Rhodes',"Smackdown",F),
("MWM-TPC","The Rock","Legend",F),("MWM-TST","Tiffany Stratton","Smackdown",F),
("MWM-UDT","Undertaker","Legend",F),
], is_auto=True)

ins("Equinox Autographs", [
("EA-AKT","Akira Tozawa","Raw",F),("EA-ALB","Aleister Black","Smackdown",F),
("EA-ANG","Angelo Dawkins","Smackdown",F),("EA-AUT","Austin Theory","Raw",F),
("EA-BBL","Bianca Belair","Smackdown",F),("EA-BRB","Bron Breakker","Raw",F),
("EA-BRO","Bronson Reed","Raw",F),("EA-CHA","Carmelo Hayes","Smackdown",F),
("EA-EGA","El Grande Americano","Raw",F),("EA-ERK","Erik","Raw",F),
("EA-FAB","B-Fab","Smackdown",F),("EA-FBA","Finn Balor","Raw",F),
("EA-IVR","Ivar","Raw",F),("EA-JAC","Jade Cargill","Smackdown",F),
("EA-JYU","Jimmy Uso","Smackdown",F),("EA-KOK","Kofi Kingston","Raw",F),
("EA-LAK","LA Knight","Raw",F),("EA-MIC","Michin","Smackdown",F),
("EA-MIZ","The Miz","Smackdown",F),("EA-MOF","Montez Ford","Smackdown",F),
("EA-MXD","Maxxine Dupri","Raw",F),("EA-NIJ","Nia Jax","Smackdown",F),
("EA-NKC","Nikki Cross","Smackdown",F),("EA-OTS","Otis","Raw",F),
("EA-PEN","Penta","Raw",F),("EA-RSV","Rusev","Raw",F),
("EA-RYF","Rey Fenix","Smackdown",F),("EA-SHN","Shinsuke Nakamura","Smackdown",F),
("EA-SMS","Sheamus","Raw",F),("EA-SOS","Solo Sikoa","Smackdown",F),
("EA-TTO","Tama Tonga","Smackdown",F),("EA-UNC","Uncle Howdy","Smackdown",F),
("EA-XVW","Xavier Woods","Raw",F),("EA-ZOS","Zoey Stark","Raw",F),
], is_auto=True)

ins("Solar Flares Signatures", [
("SFS-AXI","Axiom","Smackdown",F),("SFS-BMO","Blake Monroe","NXT",F),
("SFS-CGR","Chelsea Green","Smackdown",F),("SFS-CLR","Candice LeRae","Smackdown",F),
("SFS-CSL",'Channing "Stacks" Lorenzo',"NXT",F),("SFS-ETP","Ethan Page","NXT",F),
("SFS-GLA","Giulia","Smackdown",F),("SFS-HKW","Hank Walker","NXT",F),
("SFS-IZZ","Izzi Dame","NXT",F),("SFS-JCJ","Jacy Jayne","NXT",F),
("SFS-JCM","JC Mateo","Smackdown",F),("SFS-JDG","Jordynne Grace","NXT",F),
("SFS-JDM","JD McDonagh","Raw",F),("SFS-JVE","Je'Von Evans","NXT",F),
("SFS-KLJ","Kelani Jordan","NXT",F),("SFS-LLE","Lash Legend","NXT",F),
("SFS-LNR","Lainey Reid","NXT",R),("SFS-LOV","Lola Vice","NXT",F),
("SFS-MYB","Myles Borne","NXT",F),("SFS-OBA","Oba Femi","NXT",F),
("SFS-RKS","Ricky Saints","NXT",F),("SFS-RQR","Raquel Rodriguez","Raw",F),
("SFS-RXP","Roxanne Perez","Raw",F),("SFS-SOR","Sol Ruca","NXT",F),
("SFS-STV","Stephanie Vaquer","Raw",F),("SFS-TKL","Tank Ledger","NXT",F),
("SFS-TRW","Trick Williams","NXT",F),("SFS-TTO","Talla Tonga","Smackdown",R),
("SFS-ZAR","Zaria","NXT",F),("SFS-ZVG","Zelina Vega","Smackdown",F),
], is_auto=True)

# ─── Summary ────────────────────────────────────────────────────────────────
db.commit()
tp = db.execute("SELECT COUNT(*) FROM players WHERE set_id = ?", (SET_ID,)).fetchone()[0]
ta = db.execute("SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets ins ON pa.insert_set_id = ins.id WHERE ins.set_id = ?", (SET_ID,)).fetchone()[0]
ts = db.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id = ?", (SET_ID,)).fetchone()[0]

# Verify Hulk Hogan dedupe
hh = db.execute("SELECT COUNT(*) FROM players WHERE set_id = ? AND name = 'Hulk Hogan'", (SET_ID,)).fetchone()[0]
print(f"\nHulk Hogan records: {hh} (should be 1)")

print(f"\n{'='*50}")
print(f"Set ID: {SET_ID}")
print(f"Total subsets: {ts}")
print(f"Total unique wrestlers: {tp}")
print(f"Total card appearances: {ta}")
print(f"Expected: 737 cards")
db.close()
print("Done!")
