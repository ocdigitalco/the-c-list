"""
Seed: 2026 Bowman Baseball — Part 2
Base, Base Prospects, Chrome Prospects, and variations.
Usage: python3 scripts/seed_bowman_baseball_2026_part2.py
"""
import sqlite3, os, re

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA foreign_keys=ON")
cur = conn.cursor()

SET_ID = 52
R = False; T = True

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

def copy_cards(src_is, dst_is, num_prefix_from=None, num_prefix_to=None):
    rows = cur.execute("SELECT player_id, card_number, is_rookie, team FROM player_appearances WHERE insert_set_id = ?", (src_is,)).fetchall()
    for pid, cn, ir, team in rows:
        new_cn = cn.replace(num_prefix_from, num_prefix_to) if num_prefix_from and num_prefix_to else cn
        cur.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)",
                    (pid, dst_is, new_cn, ir, team))
    return len(rows)

# ─── BASE (100 cards) ─────────────────────────────────────────────
RC_NUMS = {3,6,9,12,16,18,19,26,28,33,35,36,37,39,40,41,45,49,53,56,57,58,62,65,66,68,69,70,74,75,78,83,84,85,86,87,91,92,93,98,99}

base_raw = [
    (1,"Aaron Judge","New York Yankees"),(2,"Yoshinobu Yamamoto","Los Angeles Dodgers"),(3,"Chase Burns","Cincinnati Reds"),
    (4,"Jackson Chourio","Milwaukee Brewers"),(5,"Julio Rodriguez","Seattle Mariners"),(6,"Sal Stewart","Cincinnati Reds"),
    (7,"Bryce Harper","Philadelphia Phillies"),(8,"Ernie Clement","Toronto Blue Jays"),(9,"Munetaka Murakami","Chicago White Sox"),
    (10,"Nick Kurtz","Athletics"),(11,"Corey Seager","Texas Rangers"),(12,"Jhostynxon Garcia","Pittsburgh Pirates"),
    (13,"Cal Raleigh","Seattle Mariners"),(14,"Drake Baldwin","Atlanta Braves"),(15,"Max Fried","New York Yankees"),
    (16,"Carson Whisenhunt","San Francisco Giants"),(17,"Francisco Lindor","New York Mets"),(18,"Roman Anthony","Boston Red Sox"),
    (19,"Kyle Teel","Chicago White Sox"),(20,"Kyle Schwarber","Philadelphia Phillies"),(21,"Michael Harris II","Atlanta Braves"),
    (22,"Andrew McCutchen","Pittsburgh Pirates"),(23,"Ronald Acuna Jr.","Atlanta Braves"),(24,"Will Smith","Los Angeles Dodgers"),
    (25,"Bobby Witt Jr.","Kansas City Royals"),(26,"Payton Tolle","Boston Red Sox"),(27,"Bo Bichette","Toronto Blue Jays"),
    (28,"Kazuma Okamoto","Toronto Blue Jays"),(29,"Geraldo Perdomo","Arizona Diamondbacks"),(30,"Brice Turang","Milwaukee Brewers"),
    (31,"Pete Crow-Armstrong","Chicago Cubs"),(32,"Ketel Marte","Arizona Diamondbacks"),(33,"Brandon Sproat","New York Mets"),
    (34,"Kyle Stowers","Miami Marlins"),(35,"Jacob Misiorowski","Milwaukee Brewers"),(36,"Jimmy Crooks","St. Louis Cardinals"),
    (37,"Chase DeLauter","Cleveland Guardians"),(38,"Matt Olson","Atlanta Braves"),(39,"Carson Williams","Tampa Bay Rays"),
    (40,"Drew Gilbert","San Francisco Giants"),(41,"Trey Yesavage","Toronto Blue Jays"),(42,"Zach Neto","Los Angeles Angels"),
    (43,"Jackson Holliday","Baltimore Orioles"),(44,"Elly De La Cruz","Cincinnati Reds"),(45,"Connelly Early","Boston Red Sox"),
    (46,"Freddie Freeman","Los Angeles Dodgers"),(47,"Fernando Tatis Jr.","San Diego Padres"),(48,"Riley Greene","Detroit Tigers"),
    (49,"Luis Morales","Athletics"),(50,"Jackson Merrill","San Diego Padres"),(51,"Garrett Crochet","Boston Red Sox"),
    (52,"Shohei Ohtani","Los Angeles Dodgers"),(53,"Cam Schlittler","New York Yankees"),(54,"Dylan Crews","Washington Nationals"),
    (55,"Cristopher Sanchez","Philadelphia Phillies"),(56,"Brice Matthews","Houston Astros"),(57,"Luke Keaschall","Minnesota Twins"),
    (58,"Bryce Eldridge","San Francisco Giants"),(59,"Junior Caminero","Tampa Bay Rays"),(60,"Manny Machado","San Diego Padres"),
    (61,"Vladimir Guerrero Jr.","Toronto Blue Jays"),(62,"Owen Caissie","Chicago Cubs"),(63,"Roki Sasaki","Los Angeles Dodgers"),
    (64,"Jacob deGrom","Texas Rangers"),(65,"Jonah Tong","New York Mets"),(66,"Carter Jensen","Kansas City Royals"),
    (67,"Yordan Alvarez","Houston Astros"),(68,"Colson Montgomery","Chicago White Sox"),(69,"Dylan Beavers","Baltimore Orioles"),
    (70,"Alex Freeland","Los Angeles Dodgers"),(71,"Trea Turner","Philadelphia Phillies"),(72,"Masyn Winn","St. Louis Cardinals"),
    (73,"Gunnar Henderson","Baltimore Orioles"),(74,"Tatsuya Imai","Houston Astros"),(75,"Jac Caglianone","Kansas City Royals"),
    (76,"Tarik Skubal","Detroit Tigers"),(77,"Jose Ramirez","Cleveland Guardians"),(78,"Cole Young","Seattle Mariners"),
    (79,"James Wood","Washington Nationals"),(80,"Corbin Carroll","Arizona Diamondbacks"),(81,"Mookie Betts","Los Angeles Dodgers"),
    (82,"Hunter Goodman","Colorado Rockies"),(83,"Bubba Chandler","Pittsburgh Pirates"),(84,"Harry Ford","Washington Nationals"),
    (85,"Nolan McLean","New York Mets"),(86,"Jakob Marsee","Miami Marlins"),(87,"Jacob Melton","Tampa Bay Rays"),
    (88,"Wyatt Langford","Texas Rangers"),(89,"Rafael Devers","San Francisco Giants"),(90,"Marcelo Mayer","Boston Red Sox"),
    (91,"Yanquiel Fernandez","Colorado Rockies"),(92,"Brady House","Washington Nationals"),(93,"Samuel Basallo","Baltimore Orioles"),
    (94,"Byron Buxton","Minnesota Twins"),(95,"George Springer","Toronto Blue Jays"),(96,"Jacob Wilson","Athletics"),
    (97,"Juan Soto","New York Mets"),(98,"C.J. Kayfus","Cleveland Guardians"),(99,"Christian Moore","Los Angeles Angels"),
    (100,"Mike Trout","Los Angeles Angels"),
]

base_cards = [(str(n), name, team, n in RC_NUMS) for n, name, team in base_raw]
add_cards(get_is_id("Base"), base_cards)
print(f"  Base: {len(base_cards)} cards")

# ─── BASE - ETCHED IN GLASS VARIATIONS ───────────────────────────
eig_nums = [3,18,35,39,58,68,75,83,84,85,93,99]
eig_is = get_is_id("Base - Etched In Glass Variations")
for n, name, team in base_raw:
    if n in eig_nums:
        pid = get_or_create_player(name)
        cur.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)",
                    (pid, eig_is, str(n), 1, team))
print(f"  Base - Etched In Glass Variations: {len(eig_nums)} cards")

# ─── BASE - RED RC VARIATIONS ────────────────────────────────────
red_rc_nums = sorted(RC_NUMS)
red_rc_is = get_is_id("Base - Red RC Variations")
for n, name, team in base_raw:
    if n in RC_NUMS:
        pid = get_or_create_player(name)
        cur.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)",
                    (pid, red_rc_is, str(n), 1, team))
print(f"  Base - Red RC Variations: {len(RC_NUMS)} cards")

# ─── BASE PROSPECTS (150 cards) ───────────────────────────────────
bp_cards = [
    ("BP-1","Ethan Holliday","Colorado Rockies",T),("BP-2","Max Clark","Detroit Tigers",T),("BP-3","Yojancel Cabrera","Los Angeles Angels",T),
    ("BP-4","James Quinn-Irons","Tampa Bay Rays",T),("BP-5","Tyson Lewis","Cincinnati Reds",T),("BP-6","Jared Jones","Pittsburgh Pirates",T),
    ("BP-7","Kendry Chourio","Kansas City Royals",T),("BP-8","Anderson Araujo","Philadelphia Phillies",T),("BP-9","Tyler Bremner","Los Angeles Angels",T),
    ("BP-10","Liam Doyle","St. Louis Cardinals",T),("BP-11","David Shields","Kansas City Royals",T),("BP-12","Jase Mitchell","Houston Astros",T),
    ("BP-13","Blake Mitchell","Kansas City Royals",T),("BP-14","Carlos Gutierrez","San Francisco Giants",T),("BP-15","Gage Jump","Athletics",T),
    ("BP-16","Marek Houston","Minnesota Twins",T),("BP-17","Caden Scarborough","Texas Rangers",T),("BP-18","Blaine Bullard","Toronto Blue Jays",T),
    ("BP-19","Kade Anderson","Seattle Mariners",T),("BP-20","Theo Gillen","Tampa Bay Rays",T),("BP-21","Roldy Brito","Colorado Rockies",T),
    ("BP-22","Deniel Ortiz","St. Louis Cardinals",T),("BP-23","Enddy Azocar","Boston Red Sox",T),("BP-24","Edward Duran","Toronto Blue Jays",T),
    ("BP-25","Juan Sanchez","Toronto Blue Jays",T),("BP-26","Sean Paul Linan","Washington Nationals",T),("BP-27","Franklin Arias","Boston Red Sox",T),
    ("BP-28","Carlos Virahonda","Arizona Diamondbacks",T),("BP-29","Victor Arias","Toronto Blue Jays",T),("BP-30","Alimber Santa","Houston Astros",T),
    ("BP-31","Brent Iredale","Pittsburgh Pirates",T),("BP-32","Breyson Guedez","Athletics",T),("BP-33","Coy James","Washington Nationals",T),
    ("BP-34","Cristopher Polanco","Toronto Blue Jays",T),("BP-35","Travis Bazzana","Cleveland Guardians",T),("BP-36","Moises Chace","Philadelphia Phillies",T),
    ("BP-37","Gage Stanifer","Toronto Blue Jays",T),("BP-38","Luis Cova","Miami Marlins",T),("BP-39","Ryan Waldschmidt","Arizona Diamondbacks",T),
    ("BP-40","Aiva Arquette","Miami Marlins",T),("BP-41","Brailyn Antunez","Milwaukee Brewers",T),("BP-42","David Davalillo","Texas Rangers",T),
    ("BP-43","Parks Harber","San Francisco Giants",T),("BP-44","Billy Carlson","Chicago White Sox",T),("BP-45","Seong-Jun Kim","Texas Rangers",T),
    ("BP-46","Charlie Condon","Colorado Rockies",T),("BP-47","Handelfry Encarnacion","Milwaukee Brewers",T),("BP-48","Shotaro Morii","Athletics",T),
    ("BP-49","Aidan Miller","Philadelphia Phillies",T),("BP-50","Daniel Dickinson","Milwaukee Brewers",T),("BP-51","Sebastian Walcott","Texas Rangers",T),
    ("BP-52","Ethan Dorchies","Milwaukee Brewers",T),("BP-53","Braden Montgomery","Chicago White Sox",T),("BP-54","Rainiel Rodriguez","St. Louis Cardinals",T),
    ("BP-55","Andrew Salas","Miami Marlins",T),("BP-56","Josuar Gonzalez","San Francisco Giants",T),("BP-57","Felnin Celesten","Seattle Mariners",T),
    ("BP-58","Jude Warwick","Detroit Tigers",T),("BP-59","Brendan Tunink","Los Angeles Dodgers",T),("BP-60","Isaiah Jackson","Los Angeles Angels",T),
    ("BP-61","Chris Arroyo","Miami Marlins",T),("BP-62","Josh Owens","Texas Rangers",T),("BP-63","Leo De Vries","Athletics",T),
    ("BP-64","George Lombard Jr.","New York Yankees",T),("BP-65","Nelly Taylor","Boston Red Sox",T),("BP-66","Wyatt Sanford","Pittsburgh Pirates",T),
    ("BP-67","Arjun Nimmala","Toronto Blue Jays",T),("BP-68","Ike Irish","Baltimore Orioles",T),("BP-69","Owen Carey","Atlanta Braves",T),
    ("BP-70","Kash Mayfield","San Diego Padres",T),("BP-71","Enyervert Perez","Arizona Diamondbacks",T),("BP-72","Luis Arana","Miami Marlins",T),
    ("BP-73","Charles Davalan","Los Angeles Dodgers",T),("BP-74","Jack Wheeler","Texas Rangers",T),("BP-75","Juan Torres","New York Yankees",T),
    ("BP-76","Esmerlyn Valdez","Pittsburgh Pirates",T),("BP-77","Daniel Pierce","Tampa Bay Rays",T),("BP-78","Dax Kilby","New York Yankees",T),
    ("BP-79","Esteban Mejia","Baltimore Orioles",T),("BP-80","Thomas White","Miami Marlins",T),("BP-81","Jose Urbina","Tampa Bay Rays",T),
    ("BP-82","Edward Florentino","Pittsburgh Pirates",T),("BP-83","Josue De Paula","Los Angeles Dodgers",T),("BP-84","David Hagaman","Arizona Diamondbacks",T),
    ("BP-85","Anthony Frobose","New York Mets",T),("BP-86","Zyhir Hope","Los Angeles Dodgers",T),("BP-87","Jean Carlos Sio","San Francisco Giants",T),
    ("BP-88","Dasan Hill","Minnesota Twins",T),("BP-89","Kendry Martinez","Seattle Mariners",T),("BP-90","Andrew Tess","Baltimore Orioles",T),
    ("BP-91","Elian Pena","New York Mets",T),("BP-92","Konnor Griffin","Pittsburgh Pirates",T),("BP-93","Jorge Quintana","San Diego Padres",T),
    ("BP-94","Ricardo Cova","Seattle Mariners",T),("BP-95","Eli Willits","Washington Nationals",T),("BP-96","Jesus Made","Milwaukee Brewers",T),
    ("BP-97","Daniel Hernandez","Washington Nationals",T),("BP-98","Walker Jenkins","Minnesota Twins",T),("BP-99","Bryce Rainer","Detroit Tigers",T),
    ("BP-100","Marconi German","Washington Nationals",T),("BP-101","Kehden Hettiger","Philadelphia Phillies",T),("BP-102","Eric Hartman","Atlanta Braves",T),
    ("BP-103","Nick Monistere","Houston Astros",T),("BP-104","Henry Lalane","New York Yankees",T),("BP-105","Kade Snell","Chicago Cubs",T),
    ("BP-106","Francisco Espinoza","Los Angeles Dodgers",T),("BP-107","Miguel Mendez","San Diego Padres",T),("BP-108","Colt Emerson","Seattle Mariners",T),
    ("BP-109","Truitt Madonna","San Diego Padres",T),("BP-110","Matthew Ferrara","Philadelphia Phillies",T),("BP-111","Carson Benge","New York Mets",T),
    ("BP-112","Jamie Arnold","Athletics",T),("BP-113","Josh Knoth","Milwaukee Brewers",T),("BP-114","Argenis Cayama","San Francisco Giants",T),
    ("BP-115","JJ Wetherholt","St. Louis Cardinals",T),("BP-116","Dauri Fernandez","Cleveland Guardians",T),("BP-117","Victor Figueroa","Baltimore Orioles",T),
    ("BP-118","Gabriel Rodriguez","Cleveland Guardians",T),("BP-119","Mathias Lacombe","Chicago White Sox",T),("BP-120","Luis Pena","Milwaukee Brewers",T),
    ("BP-121","Keaton Anthony","Philadelphia Phillies",T),("BP-122","Sam Petersen","Washington Nationals",T),("BP-123","JR Ritchie","Atlanta Braves",T),
    ("BP-124","Riley Nelson","Cleveland Guardians",T),("BP-125","Wei-En Lin","Athletics",T),("BP-126","Gavin Fien","Texas Rangers",T),
    ("BP-127","Seojun Moon","Toronto Blue Jays",T),("BP-128","Hector Ramos","Boston Red Sox",T),("BP-129","Seaver King","Washington Nationals",T),
    ("BP-130","Kenly Hunter","St. Louis Cardinals",T),("BP-131","Walker Janek","Houston Astros",T),("BP-132","Keyner Martinez","San Francisco Giants",T),
    ("BP-133","Xavier Neyens","Houston Astros",T),("BP-134","T.J. Rumfield","New York Yankees",T),("BP-135","Wehiwa Aloy","Baltimore Orioles",T),
    ("BP-136","Gavin Kilen","San Francisco Giants",T),("BP-137","Braden Nett","Athletics",T),("BP-138","Patrick Copen","Los Angeles Dodgers",T),
    ("BP-139","Edgar Montero","Athletics",T),("BP-140","Pedro Ibarguen","Milwaukee Brewers",T),("BP-141","Justin Gonzales","Boston Red Sox",T),
    ("BP-142","Brady Ebel","Milwaukee Brewers",T),("BP-143","Kaelen Culpepper","Minnesota Twins",T),("BP-144","Colby Shelton","Chicago White Sox",T),
    ("BP-145","Kevin McGonigle","Detroit Tigers",T),("BP-146","Matt Klein","Colorado Rockies",T),("BP-147","JoJo Parker","Toronto Blue Jays",T),
    ("BP-148","Dillon Lewis","New York Yankees",T),("BP-149","Andrew Fischer","Milwaukee Brewers",T),("BP-150","Wilder Dalis","Colorado Rockies",T),
]
add_cards(get_is_id("Base Prospects"), bp_cards)
print(f"  Base Prospects: {len(bp_cards)} cards")

# ─── CHROME PROSPECTS (mirror from Base Prospects) ────────────────
bp_is = get_is_id("Base Prospects")
cp_is = get_is_id("Chrome Prospects")
n = copy_cards(bp_is, cp_is, "BP-", "BCP-")
print(f"  Chrome Prospects: {n} cards (mirrored)")

# ─── CHROME PROSPECTS - PACKFRACTOR VARIATION (mirror from Chrome) ─
pf_is = get_is_id("Chrome Prospects - Packfractor Variation")
n2 = copy_cards(cp_is, pf_is)
print(f"  Chrome Prospects - Packfractor Variation: {n2} cards (mirrored)")

# ─── CHROME PROSPECTS - ETCHED IN GLASS VARIATIONS ────────────────
eig_chrome_nums = ["BCP-1","BCP-16","BCP-25","BCP-40","BCP-45","BCP-77","BCP-82","BCP-100","BCP-135","BCP-139","BCP-149"]
eig_chrome_is = get_is_id("Chrome Prospects - Etched In Glass Variations")
# Get player_ids from Chrome Prospects
for cn in eig_chrome_nums:
    row = cur.execute("SELECT player_id, is_rookie, team FROM player_appearances WHERE insert_set_id = ? AND card_number = ?", (cp_is, cn)).fetchone()
    if row:
        cur.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)",
                    (row[0], eig_chrome_is, cn, row[1], row[2]))
print(f"  Chrome Prospects - Etched In Glass Variations: {len(eig_chrome_nums)} cards")

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

# Stats
player_count = cur.execute("SELECT COUNT(*) FROM players WHERE set_id = ?", (SET_ID,)).fetchone()[0]
app_count = cur.execute("SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON pa.insert_set_id = i.id WHERE i.set_id = ?", (SET_ID,)).fetchone()[0]

print(f"\nDone! Set ID: {SET_ID}")
print(f"  Players: {player_count}")
print(f"  Appearances: {app_count}")
conn.close()
