"""
Seed: 2025 Topps Chrome WWE x Cactus Jack — Full checklist.
100 base, 6 insert subsets, 6 auto subsets, parallels, pack odds.
Usage: python3 scripts/seed_chrome_wwe_cactus_jack_2025.py
"""
import sqlite3, os, json, re, unicodedata

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
db = sqlite3.connect(DB_PATH)
db.execute("PRAGMA journal_mode=WAL")
db.execute("PRAGMA foreign_keys=ON")

SET_ID = 111
H = "Hobby"

# Update set metadata
box_config = json.dumps({
    "hobby": {"cards_per_pack": 4, "packs_per_box": 20, "boxes_per_case": 12,
              "notes": "Estimated pack odds (community-calculated from print runs)"}
})
db.execute("UPDATE sets SET sample_image_url = '/sets/2025-topps-chrome-wwe-x-cactus-jack.jpg', release_date = '2025-08-29', box_config = ?, created_at = '2026-05-29T12:00:00Z' WHERE id = ?", (box_config, SET_ID))
print(f"Updated set ID: {SET_ID}")

def slugify(text):
    s = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    s = s.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_]+', '-', s)
    return re.sub(r'-+', '-', s).strip('-')

_slug_cache = {}
def get_or_create(name, role="athlete"):
    row = db.execute("SELECT id FROM players WHERE set_id = ? AND name = ?", (SET_ID, name)).fetchone()
    if row: return row[0]
    slug = slugify(name)
    if not _slug_cache:
        existing = set(r[0] for r in db.execute("SELECT slug FROM players WHERE set_id = ? AND slug IS NOT NULL", (SET_ID,)).fetchall())
        _slug_cache.update({s: True for s in existing})
    candidate = slug
    i = 2
    while candidate in _slug_cache:
        candidate = f"{slug}-{i}"
        i += 1
    _slug_cache[candidate] = True
    db.execute("INSERT INTO players (set_id, name, slug, unique_cards, total_print_run, one_of_ones, insert_set_count, subject_role) VALUES (?, ?, ?, 0, 0, 0, 0, ?)",
               (SET_ID, name, candidate, role))
    return db.execute("SELECT last_insert_rowid()").fetchone()[0]

def add_is(name, is_auto=False):
    db.execute("INSERT INTO insert_sets (set_id, name, is_autograph) VALUES (?, ?, ?)", (SET_ID, name, 1 if is_auto else 0))
    return db.execute("SELECT last_insert_rowid()").fetchone()[0]

def add_pars(is_id, pars):
    for name, pr in pars:
        db.execute("INSERT INTO parallels (insert_set_id, name, print_run, exclusivity) VALUES (?, ?, ?, ?)", (is_id, name, pr, H))
    return len(pars)

def add_cards(is_id, cards):
    for num, name, team, rookie in cards:
        pid = get_or_create(name, "celebrity" if name == "Travis Scott" else "athlete")
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)",
                   (pid, is_id, str(num), 1 if rookie else 0, team))

R = True
F = False

# ─── BASE SET (100 cards) ───────────────────────────────────────────────────
base_id = add_is("Base Set")
base_pars = [
    ("Refractor", None), ("Red and Black Refractor", None), ("White Refractor", None),
    ("Black and Yellow Refractor", None), ("Speckle Refractor", 299),
    ("Purple Refractor", 250), ("Aqua Shimmer Refractor", 199),
    ("Teal Lasers Refractor", 175), ("Blue Refractor", 150),
    ("Blue Sonar Refractor", 125), ("Green Refractor", 99),
    ("Yellow Mini Diamonds Refractor", 75), ("Gold Refractor", 50),
    ("Cactus Jack Refractor", 41), ("Orange Refractor", 25),
    ("Black Refractor", 10), ("Red Refractor", 5), ("SuperFractor", 1),
]
add_pars(base_id, base_pars)

base_cards = [
(1,"John Cena","WWE",F),(2,"Rhea Ripley","Raw",F),(3,"Jey Uso","Raw",F),
(4,"Kevin Owens","Smackdown",F),(5,"Liv Morgan","Raw",F),(6,"Rey Mysterio","Raw",F),
(7,"Randy Orton","WWE",F),(8,"CM Punk","Raw",F),(9,"Trish Stratus","Legend",F),
(10,'"The American Nightmare" Cody Rhodes',"Smackdown",F),
(11,"Bianca Belair","Smackdown",F),(12,"LA Knight","Smackdown",F),
(13,"Nia Jax","Smackdown",F),(14,"Andrade","Smackdown",F),(15,"Gunther","Raw",F),
(16,"Tiffany Stratton","Smackdown",F),(17,'Seth "Freakin" Rollins',"Raw",F),
(18,"Xavier Woods","Raw",F),(19,"Kairi Sane","Raw",F),(20,"AJ Styles","Raw",F),
(21,"Asuka","Raw",F),(22,"Kofi Kingston","Raw",F),(23,"Penta","Raw",F),
(24,"Ricky Saints","NXT",F),(25,"Roman Reigns","Smackdown",F),
(26,"Jimmy Uso","Smackdown",F),(27,"Roxanne Perez","NXT",F),
(28,"Uncle Howdy","Smackdown",F),(29,"Karmen Petrovic","NXT",F),
(30,"Triple H","Legend",F),(31,"Bron Breakker","Raw",F),(32,"Trick Williams","NXT",F),
(33,"Alexa Bliss","WWE",F),(34,"Candice LeRae","Smackdown",F),
(35,"Lash Legend","NXT",F),(36,"Oba Femi","NXT",F),(37,"Tonga Loa","Smackdown",F),
(38,"Zelina Vega","Smackdown",F),(39,"Drew McIntyre","Smackdown",F),
(40,"Undertaker","Legend",F),(41,"Shinsuke Nakamura","Smackdown",F),
(42,"Nikkita Lyons","NXT",F),(43,"Finn Balor","Raw",F),(44,"Ivar","Raw",F),
(45,"Lola Vice","NXT",F),(46,"Alex Shelley","Smackdown",F),(47,"Bayley","Raw",F),
(48,"Jacob Fatu","Smackdown",F),(49,"Raquel Rodriguez","Raw",F),
(50,"Cactus Jack","Legend",F),(51,"Lyra Valkyria","Raw",F),
(52,"Jade Cargill","Smackdown",F),(53,"IYO SKY","Raw",F),
(54,"Jaida Parker","NXT",F),(55,"Tommaso Ciampa","Smackdown",F),
(56,'"Dirty" Dominik Mysterio',"Raw",F),(57,"Kelani Jordan","NXT",F),
(58,"Giulia","NXT",F),(59,"Becky Lynch","WWE",F),(60,"Hulk Hogan","Legend",F),
(61,"Chelsea Green","Smackdown",F),(62,'Bret "Hit Man" Hart',"Legend",F),
(63,"Charlotte Flair","WWE",F),(64,"Montez Ford","Smackdown",F),
(65,"Tama Tonga","Smackdown",F),(66,"Ludwig Kaiser","Raw",F),
(67,"Axiom","NXT",F),(68,"Braun Strowman","Smackdown",F),
(69,"Jordynne Grace","NXT",R),(70,'"Stone Cold" Steve Austin',"Legend",F),
(71,"Dragon Lee","Raw",F),(72,"Sami Zayn","Raw",F),(73,"Cora Jade","NXT",F),
(74,"Carmelo Hayes","Smackdown",F),(75,"The Rock","Legend",F),
(76,"Ethan Page","NXT",F),(77,"Solo Sikoa","Smackdown",F),
(78,"Fallon Henley","NXT",F),(79,"Stephanie Vaquer","NXT",F),
(80,"Shawn Michaels","Legend",F),(81,"Gigi Dolin","NXT",F),
(82,"Izzi Dame","NXT",F),(83,"Chris Sabin","Smackdown",F),
(84,"Johnny Gargano","Smackdown",F),(85,"Dakota Kai","Raw",F),
(86,"Jakara Jackson","NXT",F),(87,"Erik","Raw",F),(88,"Chad Gable","Raw",F),
(89,"Bronson Reed","Raw",F),(90,"Tony D'Angelo","NXT",F),
(91,"Jazmyn Nyx","NXT",F),(92,"Naomi","Smackdown",F),(93,"Sol Ruca","NXT",F),
(94,"Damian Priest","Smackdown",F),(95,"Zaria","NXT",R),
(96,"The Miz","Smackdown",F),(97,"Nathan Frazer","NXT",F),
(98,"Sheamus","Raw",F),(99,"Angelo Dawkins","Smackdown",F),
(100,"Travis Scott","None",F),
]
add_cards(base_id, base_cards)
print(f"  Base Set: {len(base_cards)} cards, {len(base_pars)} parallels")

# ─── INSERT SUBSETS ─────────────────────────────────────────────────────────
std_insert_pars = [("Base", None), ("Green Refractor", 99), ("Gold Refractor", 50), ("Orange Refractor", 25), ("Black Refractor", 10), ("Red Refractor", 5), ("SuperFractor", 1)]
rodeo_pars = [("Base", None), ("Green Refractor", 75), ("Gold Refractor", 50), ("Orange Refractor", 25), ("Black Refractor", 10), ("Red Refractor", 5), ("SuperFractor", 1)]
case_hit_pars = [("Base", 1), ("SuperFractor", 1)]

def ins(name, cards, pars=None, is_auto=False):
    is_id = add_is(name, is_auto=is_auto)
    if pars: add_pars(is_id, pars)
    add_cards(is_id, cards)
    print(f"  {name}: {len(cards)} cards" + (f", {len(pars)} parallels" if pars else ""))
    return is_id

# AstroKnights (60)
ins("AstroKnights", [
("AOK-1","Chelsea Green","Smackdown",F),("AOK-2","Ethan Page","NXT",F),
("AOK-3","Gigi Dolin","NXT",F),("AOK-4","Shinsuke Nakamura","Smackdown",F),
("AOK-5","Brutus Creed","Raw",F),("AOK-6","Kit Wilson","Smackdown",F),
("AOK-7","Erick Rowan","Smackdown",F),("AOK-8","Kelani Jordan","NXT",F),
("AOK-9","Trick Williams","NXT",F),("AOK-10","Izzi Dame","NXT",F),
("AOK-11","Dani Palmer","NXT",F),("AOK-12","Dragon Lee","Raw",F),
("AOK-13","Karmen Petrovic","NXT",F),("AOK-14","Johnny Gargano","Smackdown",F),
("AOK-15","Jazmyn Nyx","NXT",F),("AOK-16","Lexis King","NXT",F),
("AOK-17","Ivy Nile","Raw",F),("AOK-18","Noam Dar","NXT",F),
("AOK-19","Nikkita Lyons","NXT",F),("AOK-20","Giulia","NXT",F),
("AOK-21","Charlie Dempsey","NXT",F),("AOK-22","Elton Prince","Smackdown",F),
("AOK-23","Tama Tonga","Smackdown",F),("AOK-24","Santos Escobar","Smackdown",F),
("AOK-25","Dexter Lumis","Smackdown",F),("AOK-26","Axiom","NXT",F),
("AOK-27","Shayna Baszler","Raw",F),("AOK-28","Tatum Paxley","NXT",F),
("AOK-29","Ivar","Raw",F),("AOK-30","AJ Styles","Raw",F),
("AOK-31","Wes Lee","NXT",F),("AOK-32","Jaida Parker","NXT",F),
("AOK-33","Erik","Raw",F),("AOK-34","Grayson Waller","Smackdown",F),
("AOK-35","Nathan Frazer","NXT",F),("AOK-36","Ilja Dragunov","Raw",F),
("AOK-37","Tonga Loa","Smackdown",F),("AOK-38","Julius Creed","Raw",F),
("AOK-39","Tony D'Angelo","NXT",F),("AOK-40","Shawn Spears","NXT",F),
("AOK-41","Je'Von Evans","NXT",F),("AOK-42","Ricky Saints","NXT",F),
("AOK-43","Cora Jade","NXT",F),("AOK-44","Sheamus","Raw",F),
("AOK-45","Sol Ruca","NXT",F),("AOK-46","Joe Gacy","Smackdown",F),
("AOK-47","Eddy Thorpe","NXT",F),("AOK-48","Sami Zayn","Raw",F),
("AOK-49","Liv Morgan","Raw",F),("AOK-50","Fallon Henley","NXT",F),
("AOK-51","LA Knight","Smackdown",F),("AOK-52","Drew McIntyre","Smackdown",F),
("AOK-53","Jey Uso","Raw",F),("AOK-54","Rhea Ripley","Raw",F),
("AOK-55","The Miz","Smackdown",F),("AOK-56","Gunther","Raw",F),
("AOK-57","Stephanie Vaquer","NXT",F),("AOK-58","IYO SKY","Raw",F),
("AOK-59","Bayley","Raw",F),("AOK-60","Tommaso Ciampa","Smackdown",F),
], std_insert_pars)

# Trance Tacticians (40, case hit)
ins("Trance Tacticians", [
("TRT-1","Kurt Angle","Legend",F),("TRT-2","Chad Gable","Raw",F),
("TRT-3","Penta","Raw",F),("TRT-4","Gunther","Raw",F),
("TRT-5","Tiffany Stratton","Smackdown",F),("TRT-6","AJ Styles","Raw",F),
("TRT-7","Stephanie Vaquer","NXT",F),("TRT-8",'Bret "Hit Man" Hart',"Legend",F),
("TRT-9","CM Punk","Raw",F),("TRT-10","IYO SKY","Raw",F),
("TRT-11","Iron Sheik","Legend",F),("TRT-12","Eddie Guerrero","Legend",F),
("TRT-13","Pete Dunne","Smackdown",F),("TRT-14",'"The American Nightmare" Cody Rhodes',"Smackdown",F),
("TRT-15",'"Mr. Perfect" Curt Hennig',"Legend",F),("TRT-16","John Cena","WWE",F),
("TRT-17","Kevin Owens","Smackdown",F),("TRT-18","Liv Morgan","Raw",F),
("TRT-19","Roman Reigns","Smackdown",F),("TRT-20","Bianca Belair","Smackdown",F),
("TRT-21","Lyra Valkyria","Raw",F),("TRT-22","Charlotte Flair","WWE",F),
("TRT-23","Bayley","Raw",F),("TRT-24","Lola Vice","NXT",F),
("TRT-25","Solo Sikoa","Smackdown",F),("TRT-26","Finn Balor","Raw",F),
("TRT-27",'Seth "Freakin" Rollins',"Raw",F),("TRT-28","Chelsea Green","Smackdown",F),
("TRT-29","Naomi","Smackdown",F),("TRT-30","Becky Lynch","WWE",F),
("TRT-31","Ludwig Kaiser","Raw",F),("TRT-32","Damian Priest","Smackdown",F),
("TRT-33","Roxanne Perez","NXT",F),("TRT-34",'"Dirty" Dominik Mysterio',"Raw",F),
("TRT-35","Drew McIntyre","Raw",F),("TRT-36","LA Knight","Smackdown",F),
("TRT-37","Jacob Fatu","Smackdown",F),("TRT-38","Jey Uso","Raw",F),
("TRT-39","Bron Breakker","Raw",F),("TRT-40","Randy Orton","Smackdown",F),
], case_hit_pars)

# Famed Phantoms (50)
ins("Famed Phantoms", [
("FMP-1","Roman Reigns","Smackdown",F),("FMP-2",'"The American Nightmare" Cody Rhodes',"Smackdown",F),
("FMP-3","Trish Stratus","Legend",F),("FMP-4",'Bret "Hit Man" Hart',"Legend",F),
("FMP-5","Damian Priest","Smackdown",F),("FMP-6","Jakara Jackson","NXT",F),
("FMP-7","Andrade","Smackdown",F),("FMP-8","John Cena","WWE",F),
("FMP-9","Ethan Page","NXT",F),("FMP-10","X-Pac","Legend",F),
("FMP-11",'"Stone Cold" Steve Austin',"Legend",F),("FMP-12","Shayna Baszler","Raw",F),
("FMP-13","Jade Cargill","Smackdown",F),("FMP-14","The Rock","Legend",F),
("FMP-15","Randy Orton","Smackdown",F),("FMP-16","Kane","Legend",F),
("FMP-17","Shawn Michaels","Legend",F),("FMP-18","Jordynne Grace","NXT",F),
("FMP-19","Undertaker","Legend",F),("FMP-20","Asuka","Raw",F),
("FMP-21",'"Dirty" Dominik Mysterio',"Raw",F),("FMP-22","Natalya","Raw",F),
("FMP-23","Uncle Howdy","Smackdown",F),("FMP-24","Tiffany Stratton","Smackdown",F),
("FMP-25","Oba Femi","NXT",F),("FMP-26","Becky Lynch","WWE",F),
("FMP-27","Akira Tozawa","Raw",F),("FMP-28","Finn Balor","Raw",F),
("FMP-29","Jacob Fatu","Smackdown",F),("FMP-30",'Seth "Freakin" Rollins',"Raw",F),
("FMP-31","CM Punk","Raw",F),("FMP-32","Bronson Reed","Raw",F),
("FMP-33","Maxxine Dupri","Raw",F),("FMP-34","Angelo Dawkins","Smackdown",F),
("FMP-35","Kairi Sane","Raw",F),("FMP-36","Piper Niven","Smackdown",F),
("FMP-37","Johnny Gargano","Smackdown",F),("FMP-38","Sheamus","Raw",F),
("FMP-39","Nikki Cross","Smackdown",F),("FMP-40","Michin","Smackdown",F),
("FMP-41","Ivar","Raw",F),("FMP-42","Montez Ford","Smackdown",F),
("FMP-43","Alexa Bliss","Smackdown",F),("FMP-44","Kevin Nash","Legend",F),
("FMP-45","Xavier Woods","Raw",F),("FMP-46","Erik","Raw",F),
("FMP-47","Braun Strowman","Smackdown",F),("FMP-48","Dakota Kai","Raw",F),
("FMP-49","Jimmy Uso","Smackdown",F),("FMP-50","Austin Theory","Smackdown",F),
], std_insert_pars)

# Rodeo Rebels (50, Green /75)
ins("Rodeo Rebels", [
("RDR-1",'"Stone Cold" Steve Austin',"Legend",F),("RDR-2","Cactus Jack","Legend",F),
("RDR-3","Undertaker","Legend",F),("RDR-4","Becky Lynch","WWE",F),
("RDR-5","Sami Zayn","Raw",F),("RDR-6","Liv Morgan","Raw",F),
("RDR-7","Shawn Michaels","Legend",F),("RDR-8","Trish Stratus","Legend",F),
("RDR-9","Maryse","Legend",F),("RDR-10","Kelani Jordan","NXT",F),
("RDR-11",'Jake "The Snake" Roberts',"Legend",F),("RDR-12",'"Dirty" Dominik Mysterio',"Raw",F),
("RDR-13","Jaida Parker","NXT",F),("RDR-14","Rhea Ripley","Raw",F),
("RDR-15","Roxanne Perez","NXT",F),("RDR-16","Road Dogg Jesse James","Legend",F),
("RDR-17","Gigi Dolin","NXT",F),("RDR-18","Torrie Wilson","Legend",F),
("RDR-19","Solo Sikoa","Smackdown",F),("RDR-20","Razor Ramon","Legend",F),
("RDR-21","The Miz","Smackdown",F),("RDR-22","Trick Williams","NXT",F),
("RDR-23","Bubba Ray Dudley","Legend",F),("RDR-24","Cora Jade","NXT",F),
("RDR-25","Nia Jax","Smackdown",F),("RDR-26","Billy Gunn","Legend",F),
("RDR-27","Michelle McCool","Legend",F),("RDR-28","Fallon Henley","NXT",F),
("RDR-29","Uncle Howdy","Smackdown",F),("RDR-30","Cowboy Bob Orton","Legend",F),
("RDR-31","JD McDonagh","Raw",F),("RDR-32","Tony D'Angelo","NXT",F),
("RDR-33","Kofi Kingston","Raw",F),("RDR-34","Oba Femi","NXT",F),
("RDR-35","Finn Balor","Raw",F),("RDR-36","Sheamus","Raw",F),
("RDR-37","Bianca Belair","Smackdown",F),("RDR-38","Lyra Valkyria","Raw",F),
("RDR-39",'Seth "Freakin" Rollins',"Raw",F),("RDR-40","Zelina Vega","Raw",F),
("RDR-41","Tiffany Stratton","Smackdown",F),("RDR-42","Jordynne Grace","NXT",F),
("RDR-43","Austin Theory","Smackdown",F),("RDR-44","Berto","Smackdown",F),
("RDR-45","Damian Priest","Smackdown",F),("RDR-46","Sol Ruca","NXT",F),
("RDR-47","Bronson Reed","Raw",F),("RDR-48","Otis","Raw",F),
("RDR-49","Dragon Lee","Raw",F),("RDR-50","Kevin Owens","Smackdown",F),
], rodeo_pars)

# Kings of the Night (60, case hit)
ins("Kings of the Night", [
("KON-1","Hulk Hogan","Legend",F),("KON-2","Eddie Guerrero","Legend",F),
("KON-3","The Rock","Legend",F),("KON-4","Triple H","Legend",F),
("KON-5","Bray Wyatt","Legend",F),("KON-6","John Cena","WWE",F),
("KON-7","CM Punk","Raw",F),("KON-8","Gunther","Raw",F),
("KON-9","Kurt Angle","Legend",F),("KON-10","Drew McIntyre","Smackdown",F),
("KON-11","Jey Uso","Raw",F),("KON-12","Kofi Kingston","Raw",F),
("KON-13",'Bret "Hit Man" Hart',"Legend",F),("KON-14","Karrion Kross","Raw",F),
("KON-15","Tommaso Ciampa","Smackdown",F),("KON-16","Carlito","Raw",F),
("KON-17","Diesel","Legend",F),("KON-18","Jacob Fatu","Smackdown",F),
("KON-19","Braun Strowman","Raw",F),("KON-20","Damian Priest","Smackdown",F),
("KON-21","Jimmy Uso","Smackdown",F),("KON-22","Batista","Legend",F),
("KON-23","Oba Femi","NXT",F),("KON-24","Randy Orton","Smackdown",F),
("KON-25","Rob Van Dam","Legend",F),("KON-26","Shinsuke Nakamura","Smackdown",F),
("KON-27","Roman Reigns","Smackdown",F),("KON-28","Sheamus","Raw",F),
("KON-29","British Bulldog","Legend",F),("KON-30",'Seth "Freakin" Rollins',"Raw",F),
("KON-31","Kevin Owens","Smackdown",F),("KON-32","Rey Mysterio","Raw",F),
("KON-33","LA Knight","Smackdown",F),("KON-34","Big Boss Man","Legend",F),
("KON-35","Johnny Gargano","Smackdown",F),("KON-36","Finn Balor","Raw",F),
("KON-37","Ultimate Warrior","Legend",F),("KON-38",'"The American Nightmare" Cody Rhodes',"Smackdown",F),
("KON-39","Bron Breakker","Raw",F),("KON-40","Booker T","Legend",F),
("KON-41","Carmelo Hayes","Smackdown",F),("KON-42","Ludwig Kaiser","Raw",F),
("KON-43","Ax","Legend",F),("KON-44","Smash","Legend",F),
("KON-45","Bob Backlund","Legend",F),("KON-46","Crush","Legend",F),
("KON-47","Hacksaw Jim Duggan","Legend",F),("KON-48","Jimmy Snuka","Legend",F),
("KON-49","Junkyard Dog","Legend",F),("KON-50","Kamala","Legend",F),
("KON-51","King Kong Bundy","Legend",F),("KON-52","Koko B. Ware","Legend",F),
("KON-53","Mr. Fuji","Legend",F),("KON-54",'"Mr. Wonderful" Paul Orndorff',"Legend",F),
("KON-55","Steve Blackman","Legend",F),("KON-56","Tito Santana","Legend",F),
("KON-57","Tonga Kid","Legend",F),("KON-58","Hornswoggle","Legend",F),
("KON-59","JD McDonagh","Raw",F),("KON-60","Umaga","Legend",F),
], case_hit_pars)

# Festival Fury (40)
ins("Festival Fury", [
("FVF-1","Penta","Raw",F),("FVF-2","Alexa Bliss","WWE",F),
("FVF-3","Bianca Belair","Smackdown",F),("FVF-4","CM Punk","Raw",F),
("FVF-5","Bray Wyatt","Legend",F),("FVF-6","Liv Morgan","Raw",F),
("FVF-7","Jey Uso","Raw",F),("FVF-8","Chelsea Green","Smackdown",F),
("FVF-9","Rhea Ripley","Raw",F),("FVF-10","Stephanie Vaquer","NXT",F),
("FVF-11","Damian Priest","Smackdown",F),("FVF-12","LA Knight","Smackdown",F),
("FVF-13","Undertaker","Legend",F),("FVF-14","Gunther","Raw",F),
("FVF-15","The Rock","Legend",F),("FVF-16","Roman Reigns","Smackdown",F),
("FVF-17","Charlotte Flair","WWE",F),("FVF-18","Kevin Owens","Smackdown",F),
("FVF-19","Randy Orton","Raw",F),("FVF-20","Zaria","NXT",F),
("FVF-21",'Seth "Freakin" Rollins',"Raw",F),("FVF-22","John Cena","Legend",F),
("FVF-23","Drew McIntyre","Smackdown",F),("FVF-24",'"The American Nightmare" Cody Rhodes',"Smackdown",F),
("FVF-25","Triple H","Legend",F),("FVF-26","Jacob Fatu","Smackdown",F),
("FVF-27","Solo Sikoa","Smackdown",F),("FVF-28","Tiffany Stratton","Smackdown",F),
("FVF-29","Becky Lynch","WWE",F),("FVF-30","Giulia","NXT",F),
("FVF-31","R-Truth","Smackdown",F),("FVF-32","Asuka","WWE",F),
("FVF-33","Chad Gable","Raw",F),("FVF-34","Rey Mysterio","Raw",F),
("FVF-35","Nia Jax","Smackdown",F),("FVF-36","Candice LeRae","Smackdown",F),
("FVF-37","Alex Shelley","Smackdown",F),("FVF-38","Big E","WWE",F),
("FVF-39","Raquel Rodriguez","Raw",F),("FVF-40","Chris Sabin","Smackdown",F),
], std_insert_pars)

# ─── AUTOGRAPH SUBSETS ──────────────────────────────────────────────────────
auto_pars = [("Refractor", None), ("Orange Refractor", 25), ("Black Refractor", 10), ("Red Refractor", 5), ("SuperFractor", 1)]

# Base Cards Autograph Variation (33)
ins("Base Cards Autograph Variation", [
("BAV-BKR","Bron Breakker","Raw",F),("BAV-BLR","Bianca Belair","Smackdown",F),
("BAV-BLS","Alexa Bliss","Smackdown",F),("BAV-DWK","Angelo Dawkins","Smackdown",F),
("BAV-FLR","Charlotte Flair","WWE",F),("BAV-FRD","Montez Ford","Smackdown",F),
("BAV-GBL","Chad Gable","Raw",F),("BAV-GRC","Jordynne Grace","NXT",F),
("BAV-HGN","Hulk Hogan","Legend",F),("BAV-HYS","Carmelo Hayes","Smackdown",F),
("BAV-JAX","Nia Jax","Smackdown",F),("BAV-JCK","Cactus Jack","Legend",F),
("BAV-KNG","Kofi Kingston","Raw",F),("BAV-KSR","Ludwig Kaiser","Raw",F),
("BAV-LGD","Lash Legend","NXT",F),("BAV-LRE","Candice LeRae","Smackdown",F),
("BAV-MYS","Rey Mysterio","Raw",F),("BAV-NMI","Naomi","Smackdown",F),
("BAV-OWN","Kevin Owens","Smackdown",F),("BAV-PNK","CM Punk","Raw",F),
("BAV-PNT","Penta","Raw",F),("BAV-PRZ","Roxanne Perez","NXT",F),
("BAV-RDZ","Raquel Rodriguez","Raw",F),("BAV-SAB","Chris Sabin","Smackdown",F),
("BAV-SKA","Solo Sikoa","Smackdown",F),("BAV-SLL","Alex Shelley","Smackdown",F),
("BAV-SNE","Zelina Vega","Smackdown",F),("BAV-SNT","Ricky Saints","NXT",F),
("BAV-TVS","Travis Scott","None",F),("BAV-USO","Jimmy Uso","Smackdown",F),
("BAV-VIC","Lola Vice","NXT",F),("BAV-VLK","Lyra Valkyria","Raw",F),
("BAV-ZRA","Zaria","NXT",F),
], auto_pars, is_auto=True)

# Famed Phantoms Autographs (25)
ins("Famed Phantoms Autographs", [
("FPA-AND","Andrade","Smackdown",F),("FPA-ASU","Asuka","Raw",F),
("FPA-BEC","Becky Lynch","WWE",F),("FPA-BRE",'Bret "Hit Man" Hart',"Legend",F),
("FPA-COD",'"The American Nightmare" Cody Rhodes',"Smackdown",F),
("FPA-DAM","Damian Priest","Smackdown",F),("FPA-DIR",'"Dirty" Dominik Mysterio',"Raw",F),
("FPA-ETH","Ethan Page","NXT",F),("FPA-FIN","Finn Balor","Raw",F),
("FPA-JAC","Jacob Fatu","Smackdown",F),("FPA-JAD","Jade Cargill","Smackdown",F),
("FPA-JOH","John Cena","WWE",F),("FPA-KAN","Kane","Legend",F),
("FPA-NAT","Natalya","Raw",F),("FPA-OBA","Oba Femi","NXT",F),
("FPA-RAN","Randy Orton","WWE",F),("FPA-ROM","Roman Reigns","Smackdown",F),
("FPA-SCA",'"Stone Cold" Steve Austin',"Legend",F),
("FPA-SET",'Seth "Freakin" Rollins',"Raw",F),("FPA-SHA","Shawn Michaels","Legend",F),
("FPA-THE","The Rock","Legend",F),("FPA-TIF","Tiffany Stratton","Smackdown",F),
("FPA-TRI","Trish Stratus","Legend",F),("FPA-UNC","Uncle Howdy","Smackdown",F),
("FPA-UND","Undertaker","Legend",F),
], auto_pars, is_auto=True)

# AstroKnights Autographs (37)
ins("AstroKnights Autographs", [
("AKA-AJS","AJ Styles","Raw",F),("AKA-BYY","Bayley","Raw",F),
("AKA-CGN","Chelsea Green","Smackdown",F),("AKA-DME","Drew McIntyre","Smackdown",F),
("AKA-EPE","Elton Prince","Smackdown",F),("AKA-ERK","Erik","Raw",F),
("AKA-FHY","Fallon Henley","NXT",F),("AKA-GLA","Giulia","NXT",F),
("AKA-GTR","Gunther","Raw",F),("AKA-IDE","Izzi Dame","NXT",F),
("AKA-ISY","IYO SKY","Raw",F),("AKA-IVR","Ivar","Raw",F),
("AKA-JES","Je'Von Evans","NXT",F),("AKA-JGO","Johnny Gargano","Smackdown",F),
("AKA-JNX","Jazmyn Nyx","NXT",F),("AKA-JPR","Jaida Parker","NXT",F),
("AKA-JUO","Jey Uso","Raw",F),("AKA-KJN","Kelani Jordan","NXT",F),
("AKA-KPC","Karmen Petrovic","NXT",F),("AKA-KWN","Kit Wilson","Smackdown",F),
("AKA-LAK","LA Knight","Smackdown",F),("AKA-LKG","Lexis King","NXT",F),
("AKA-LMN","Liv Morgan","Raw",F),("AKA-NLS","Nikkita Lyons","NXT",F),
("AKA-RRY","Rhea Ripley","Raw",F),("AKA-SER","Santos Escobar","Smackdown",F),
("AKA-SMS","Sheamus","Raw",F),("AKA-SNA","Shinsuke Nakamura","Smackdown",F),
("AKA-SRA","Sol Ruca","NXT",F),("AKA-SSS","Shawn Spears","NXT",F),
("AKA-SVR","Stephanie Vaquer","NXT",F),("AKA-SZN","Sami Zayn","Raw",F),
("AKA-TCA","Tommaso Ciampa","Smackdown",F),("AKA-TDO","Tony D'Angelo","NXT",F),
("AKA-TMZ","The Miz","Smackdown",F),("AKA-TWS","Trick Williams","NXT",F),
("AKA-WLE","Wes Lee","NXT",F),
], auto_pars, is_auto=True)

# The Rock Retrospective (1 card, no parallels)
ins("The Rock Retrospective Autographs", [("RRA-3","The Rock","Legend",F)], is_auto=True)

# Celebrating Cena Autographs (4 cards, no parallels)
ins("Celebrating Cena Autographs", [
("CCA-6","John Cena","Legend",F),("CCA-7","John Cena","Legend",F),
("CCA-8","John Cena","Legend",F),("CCA-9","John Cena","Legend",F),
], is_auto=True)

# Triple H Tribute Autographs (2 cards, no parallels)
ins("Triple H Tribute Autographs", [("TTA-1","Triple H","Legend",F),("TTA-2","Triple H","Legend",F)], is_auto=True)

# ─── PACK ODDS ──────────────────────────────────────────────────────────────
pack_odds = {"hobby": {
    "Refractor": "1:10", "Red and Black Refractor": "1:20", "White Refractor": "1:20",
    "Black and Yellow Refractor": "1:20", "Speckle Refractor": "1:25",
    "Purple Refractor": "1:30", "Aqua Shimmer Refractor": "1:38",
    "Teal Lasers Refractor": "1:43", "Blue Refractor": "1:50",
    "Blue Sonar Refractor": "1:60", "Green Refractor": "1:76",
    "Yellow Mini Diamonds Refractor": "1:100", "Gold Refractor": "1:150",
    "Cactus Jack Refractor": "1:183", "Orange Refractor": "1:301",
    "Black Refractor": "1:752", "Red Refractor": "1:1,504", "SuperFractor": "1:7,520",
    "AstroKnights Green Refractor": "1:127", "AstroKnights Gold Refractor": "1:251",
    "AstroKnights Orange Refractor": "1:501", "AstroKnights Black Refractor": "1:1,253",
    "AstroKnights Red Refractor": "1:2,506", "AstroKnights SuperFractor": "1:12,533",
    "Festival Fury Green Refractor": "1:190", "Festival Fury Gold Refractor": "1:376",
    "Festival Fury Orange Refractor": "1:752", "Festival Fury Black Refractor": "1:1,860",
    "Festival Fury Red Refractor": "1:3,760", "Festival Fury SuperFractor": "1:18,800",
    "Famed Phantoms Green Refractor": "1:152", "Famed Phantoms Gold Refractor": "1:301",
    "Famed Phantoms Orange Refractor": "1:602", "Famed Phantoms Black Refractor": "1:1,504",
    "Famed Phantoms Red Refractor": "1:3,008", "Famed Phantoms SuperFractor": "1:15,040",
    "Rodeo Rebels Green Refractor": "1:201", "Rodeo Rebels Gold Refractor": "1:301",
    "Rodeo Rebels Orange Refractor": "1:602", "Rodeo Rebels Black Refractor": "1:1,504",
    "Rodeo Rebels Red Refractor": "1:3,008", "Rodeo Rebels SuperFractor": "1:15,040",
    "Kings of the Night Base": "1:248", "Kings of the Night SuperFractor": "1:7,520",
    "Trance Tacticians Base": "1:248", "Trance Tacticians SuperFractor": "1:7,520",
}}
db.execute("UPDATE sets SET pack_odds = ? WHERE id = ?", (json.dumps(pack_odds), SET_ID))
print(f"\nAttached pack odds ({len(pack_odds['hobby'])} keys)")

# ─── Backfill image IDs from other sets ─────────────────────────────────────
updated = db.execute("""
    UPDATE players SET nba_player_id = (SELECT p2.nba_player_id FROM players p2 WHERE p2.name = players.name AND p2.nba_player_id IS NOT NULL LIMIT 1)
    WHERE set_id = ? AND nba_player_id IS NULL AND EXISTS (SELECT 1 FROM players p2 WHERE p2.name = players.name AND p2.nba_player_id IS NOT NULL)
""", (SET_ID,)).rowcount
print(f"Backfilled {updated} image IDs")

# ─── Summary ────────────────────────────────────────────────────────────────
db.commit()
total_players = db.execute("SELECT COUNT(*) FROM players WHERE set_id = ?", (SET_ID,)).fetchone()[0]
total_appearances = db.execute("SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets ins ON pa.insert_set_id = ins.id WHERE ins.set_id = ?", (SET_ID,)).fetchone()[0]
total_subsets = db.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id = ?", (SET_ID,)).fetchone()[0]
total_parallels = db.execute("SELECT COUNT(*) FROM parallels p JOIN insert_sets ins ON p.insert_set_id = ins.id WHERE ins.set_id = ?", (SET_ID,)).fetchone()[0]

print(f"\n{'='*50}")
print(f"Set ID: {SET_ID}")
print(f"Total subsets: {total_subsets}")
print(f"Total unique wrestlers: {total_players}")
print(f"Total card appearances: {total_appearances}")
print(f"Total parallels: {total_parallels}")
print(f"Expected: 502 cards, 65 parallels")
db.close()
print("Done!")
