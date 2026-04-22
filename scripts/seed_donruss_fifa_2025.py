"""
Seed: 2025-26 Donruss Road to FIFA World Cup 26 — Part 1
Set creation, parallels, base cards (250 Donruss + 250 Optic).
Usage: python3 scripts/seed_donruss_fifa_2025.py
"""
import sqlite3, json, os, re

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA foreign_keys=ON")
cur = conn.cursor()

# ─── Helpers ──────────────────────────────────────────────────────

def get_or_create_player(set_id, name):
    cur.execute("SELECT id FROM players WHERE set_id = ? AND name = ?", (set_id, name))
    row = cur.fetchone()
    if row: return row[0]
    cur.execute("INSERT INTO players (set_id, name, unique_cards, total_print_run, one_of_ones, insert_set_count) VALUES (?, ?, 0, 0, 0, 0)", (set_id, name))
    return cur.lastrowid

def create_insert_set(set_id, name):
    cur.execute("INSERT INTO insert_sets (set_id, name) VALUES (?, ?)", (set_id, name))
    return cur.lastrowid

def create_parallel(is_id, name, print_run):
    cur.execute("INSERT INTO parallels (insert_set_id, name, print_run) VALUES (?, ?, ?)", (is_id, name, print_run))

def create_appearance(player_id, is_id, card_number, is_rookie=False, team=None):
    cur.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)", (player_id, is_id, card_number, int(is_rookie), team))
    return cur.lastrowid

def add_cards(is_id, cards):
    for num, name, team, rookie in cards:
        pid = get_or_create_player(set_id, name)
        create_appearance(pid, is_id, num, rookie, team)

def slugify(text):
    s = text.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_]+', '-', s)
    return re.sub(r'-+', '-', s).strip('-')

# ─── Check existing ──────────────────────────────────────────────
SET_NAME = "2025-26 Donruss Road to FIFA World Cup 26"
cur.execute("SELECT id FROM sets WHERE name = ?", (SET_NAME,))
if cur.fetchone():
    print(f"Set '{SET_NAME}' already exists. Aborting.")
    conn.close()
    exit(1)

# ─── Create set ──────────────────────────────────────────────────
box_config = {
    "hobby": {
        "cards_per_pack": 12, "packs_per_box": 30, "boxes_per_case": 12,
        "autos_per_box": 1, "memorabilia_per_box": 1, "numbered_per_box": 6,
    },
    "hobby_international": {
        "cards_per_pack": 12, "packs_per_box": 30, "boxes_per_case": 12,
        "autos_per_box": 1, "numbered_per_box": 3,
    },
    "blaster": {
        "cards_per_pack": 15, "packs_per_box": 6, "boxes_per_case": 20,
    },
    "fat_pack": {
        "cards_per_pack": 25, "packs_per_box": 12, "boxes_per_case": 12,
    },
}

cur.execute(
    "INSERT INTO sets (name, sport, season, league, tier, sample_image_url, box_config, release_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    (SET_NAME, "Soccer", "2025-26", "International", "Standard", "/sets/2025-26-donruss-road-to-fifa-world-cup-26.jpg", json.dumps(box_config), "2026-04-22"),
)
set_id = cur.lastrowid
cur.execute("UPDATE sets SET slug = ? WHERE id = ?", ("2025-26-donruss-road-to-fifa-world-cup-26", set_id))
print(f"Created set '{SET_NAME}' with id {set_id}")

# ─── Insert Sets ─────────────────────────────────────────────────
insert_sets = {}
for name in [
    "Base", "Base - Rated Rookies", "Base Optic", "Base Optic - Rated Rookies",
    "Animation", "Craftsmen", "Dominators", "Elite Series", "Kaboom", "Kaboom Oversize",
    "Magicians", "Net Marvels", "Night Moves", "Pitch Kings", "Rookie Kings", "Zero Gravity",
    "Kit Kings", "Kit Series",
    "Beautiful Game Autographs", "Beautiful Game Dual Autographs", "Signature Series",
]:
    insert_sets[name] = create_insert_set(set_id, name)
print(f"  Created {len(insert_sets)} insert sets")

# ─── Parallels ───────────────────────────────────────────────────

# Base / Base - Rated Rookies
BASE_PARS = [
    ("Bronze", None), ("Cubic", None), ("Diamond", None), ("Maze", None),
    ("Red and Blue Maze", None), ("Red and Gold", None), ("Red and Green", None), ("Silver", None),
    ("Blue Swirl", 399), ("Green and Blue Maze", 270), ("Blue Cubic", 205), ("Teal", 199),
    ("Orange", 99), ("Blue Pyramids", 95), ("Pink Swirl", 89), ("Red Swirl", 79), ("Red", 75),
    ("Red Cubic", 50), ("Blue", 49), ("Pink Cubic", 45), ("Pink Diamond", 25), ("Purple", 25),
    ("Red Pyramids", 20), ("Gold", 10), ("Gold Diamond", 10), ("Green", 5), ("Black", 1),
]
for is_name in ["Base", "Base - Rated Rookies"]:
    for pname, pr in BASE_PARS:
        create_parallel(insert_sets[is_name], pname, pr)

# Base Optic / Base Optic - Rated Rookies
OPTIC_PARS = [
    ("Argyle", None), ("Holo", None), ("Ice", None), ("Pink Velocity", None),
    ("Plum Blossom", None), ("Velocity", None),
    ("Orange Velocity", 199), ("Red", 199), ("Orange", 99), ("Orange Ice", 99),
    ("Pink Velocity Numbered", 99), ("Blue", 75), ("Electricity", 75), ("Teal Mojo", 49),
    ("Pink Ice", 25), ("Purple Mojo", 25), ("Gold", 10), ("Dragon", 8), ("Green", 5),
    ("Black", 1), ("Black Pandora", 1), ("Gold Vinyl", 1),
]
for is_name in ["Base Optic", "Base Optic - Rated Rookies"]:
    for pname, pr in OPTIC_PARS:
        create_parallel(insert_sets[is_name], pname, pr)

# Standard insert parallels
STANDARD_INSERT_PARS = [
    ("Red", None), ("Silver", None), ("Blue", 199), ("Purple", 99),
    ("Pink", 25), ("Gold", 10), ("Green", 5), ("Black", 1),
]
for is_name in ["Craftsmen", "Dominators", "Elite Series", "Magicians", "Net Marvels", "Pitch Kings", "Rookie Kings", "Zero Gravity"]:
    for pname, pr in STANDARD_INSERT_PARS:
        create_parallel(insert_sets[is_name], pname, pr)

# Kaboom
create_parallel(insert_sets["Kaboom"], "Gold", 10)
create_parallel(insert_sets["Kaboom"], "Black", 1)

# Kit Kings / Kit Series
KIT_PARS = [("Silver", 99), ("Blue", 49), ("Gold", 10), ("Black", 1)]
for is_name in ["Kit Kings", "Kit Series"]:
    for pname, pr in KIT_PARS:
        create_parallel(insert_sets[is_name], pname, pr)

# Beautiful Game Autographs
BGA_PARS = [
    ("Pink Ice", None), ("Pink Velocity", None), ("Dragon", 299), ("Blue", 199),
    ("Purple", 99), ("Red", 49), ("Gold", 10), ("Green", 5), ("Black", 1),
]
for pname, pr in BGA_PARS:
    create_parallel(insert_sets["Beautiful Game Autographs"], pname, pr)

# Beautiful Game Dual Autographs
BGDA_PARS = [
    ("Pink Ice", None), ("Pink Velocity", None), ("Dragon", 99), ("Blue", 75),
    ("Purple", 49), ("Red", 25), ("Gold", 10), ("Green", 5), ("Black", 1),
]
for pname, pr in BGDA_PARS:
    create_parallel(insert_sets["Beautiful Game Dual Autographs"], pname, pr)

# Signature Series
SS_PARS = [
    ("Pink Ice", None), ("Pink Velocity", None), ("Dragon", 299), ("Blue", 199),
    ("Purple", 99), ("Red", 49), ("Gold", 10), ("Green", 5), ("Black", 1),
]
for pname, pr in SS_PARS:
    create_parallel(insert_sets["Signature Series"], pname, pr)

par_count = cur.execute("SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON p.insert_set_id = i.id WHERE i.set_id = ?", (set_id,)).fetchone()[0]
print(f"  Created {par_count} parallels")

# ─── Base Set (1-200) ────────────────────────────────────────────
R = False
base_cards = [
    ("1","Brennan Johnson","Cymru",R),("2","Neco Williams","Cymru",R),("3","Daniel James","Cymru",R),("4","Harry Wilson","Cymru",R),
    ("5","Iliman Ndiaye","Senegal",R),("6","Nicolas Jackson","Senegal",R),("7","Sadio Mane","Senegal",R),
    ("8","David Raya","Spain",R),("9","Dean Huijsen","Spain",R),("10","Lamine Yamal","Spain",R),("11","Pedri","Spain",R),
    ("12","Nico Williams","Spain",R),("13","Dani Olmo","Spain",R),("14","Martin Zubimendi","Spain",R),
    ("15","Mikel Oyarzabal","Spain",R),("16","Pau Cubarsi","Spain",R),("17","Fabian Ruiz","Spain",R),
    ("18","Alvaro Morata","Spain",R),("19","Unai Simon","Spain",R),
    ("20","Yunus Musah","United States",R),("21","Timothy Weah","United States",R),("22","Tyler Adams","United States",R),
    ("23","Joe Scally","United States",R),("24","Weston McKennie","United States",R),("25","Christian Pulisic","United States",R),
    ("26","Diego Luna","United States",R),("27","Malik Tillman","United States",R),("28","Matt Freese","United States",R),
    ("29","Antonio Rudiger","Germany",R),("30","Maximilian Beier","Germany",R),("31","Karim Adeyemi","Germany",R),
    ("32","Oliver Baumann","Germany",R),("33","Deniz Undav","Germany",R),("34","Maximilian Mittelstadt","Germany",R),
    ("35","Niclas Fullkrug","Germany",R),("36","Kai Havertz","Germany",R),("37","Leroy Sane","Germany",R),
    ("38","Serge Gnabry","Germany",R),("39","Joshua Kimmich","Germany",R),("40","Jamal Musiala","Germany",R),
    ("41","Marc-Andre ter Stegen","Germany",R),("42","Robert Andrich","Germany",R),("43","Florian Wirtz","Germany",R),
    ("44","Jonathan Burkardt","Germany",R),
    ("45","Jamie Donley","Northern Ireland",R),("46","Trai Hume","Northern Ireland",R),("47","Callum Marshall","Northern Ireland",R),
    ("48","Maximiliano Araujo","Uruguay",R),("49","Manuel Ugarte","Uruguay",R),("50","Federico Valverde","Uruguay",R),
    ("51","Ronald Araujo","Uruguay",R),("52","Darwin Nunez","Uruguay",R),("53","Facundo Pellistri","Uruguay",R),
    ("54","Dusan Vlahovic","Serbia",R),("55","Lazar Samardzic","Serbia",R),("56","Nikola Milenkovic","Serbia",R),
    ("57","Josko Gvardiol","Croatia",R),("58","Ivan Perisic","Croatia",R),("59","Mateo Kovacic","Croatia",R),
    ("60","Josip Stanisic","Croatia",R),("61","Luka Modric","Croatia",R),
    ("62","Harry Kane","England",R),("63","Jude Bellingham","England",R),("64","Jordan Pickford","England",R),
    ("65","Bukayo Saka","England",R),("66","Declan Rice","England",R),("67","Anthony Gordon","England",R),
    ("68","Eberechi Eze","England",R),("69","Phil Foden","England",R),("70","Cole Palmer","England",R),
    ("71","Trent Alexander-Arnold","England",R),("72","Myles Lewis-Skelly","England",R),("73","Jarrod Bowen","England",R),
    ("74","Raul Jimenez","Mexico",R),("75","Santiago Gimenez","Mexico",R),("76","Edson Alvarez","Mexico",R),
    ("77","Cesar Huerta","Mexico",R),("78","Luis Romo","Mexico",R),("79","Johan Vasquez","Mexico",R),
    ("80","Hugo Larsson","Sweden",R),("81","Alexander Isak","Sweden",R),("82","Viktor Gyokeres","Sweden",R),
    ("83","Dejan Kulusevski","Sweden",R),
    ("84","Rafael Leao","Portugal",R),("85","Bernardo Silva","Portugal",R),("86","Joao Neves","Portugal",R),
    ("87","Diogo Costa","Portugal",R),("88","Francisco Conceicao","Portugal",R),("89","Vitinha","Portugal",R),
    ("90","Bruno Fernandes","Portugal",R),("91","Cristiano Ronaldo","Portugal",R),("92","Nuno Mendes","Portugal",R),
    ("93","Ruben Dias","Portugal",R),("94","Pedro Neto","Portugal",R),("95","Goncalo Ramos","Portugal",R),
    ("96","Brahim Diaz","Morocco",R),("97","Bilal El Khannouss","Morocco",R),("98","Eliesse Ben Seghir","Morocco",R),
    ("99","Achraf Hakimi","Morocco",R),("100","Youssef En-Nesyri","Morocco",R),("101","Abde Ezzalzouli","Morocco",R),
    ("102","Heung-Min Son","Korea Republic",R),("103","Hee-chan Hwang","Korea Republic",R),
    ("104","Kang-in Lee","Korea Republic",R),("105","Min-Hyuk Yang","Korea Republic",R),
    ("106","Edrick Menjivar","Honduras",R),("107","Joseph Rosales","Honduras",R),
    ("108","Romell Quioto","Honduras",R),("109","Kervin Arriaga","Honduras",R),
    ("110","Sandro Tonali","Italy",R),("111","Moise Kean","Italy",R),("112","Gianluigi Donnarumma","Italy",R),
    ("113","Davide Frattesi","Italy",R),("114","Nicolo Barella","Italy",R),("115","Mateo Retegui","Italy",R),
    ("116","Riccardo Calafiori","Italy",R),("117","Giovanni Di Lorenzo","Italy",R),
    ("118","Giacomo Raspadori","Italy",R),("119","Alessandro Bastoni","Italy",R),
    ("120","Samuele Ricci","Italy",R),("121","Destiny Udogie","Italy",R),
    ("122","Luis Suarez","Colombia",R),("123","James Rodriguez","Colombia",R),("124","Jhon Arias","Colombia",R),
    ("125","Luis Diaz","Colombia",R),("126","Richard Rios","Colombia",R),
    ("127","Mohammed Kudus","Ghana",R),("128","Jordan Ayew","Ghana",R),("129","Ernest Nuamah","Ghana",R),
    ("130","Inaki Williams","Ghana",R),("131","Antoine Semenyo","Ghana",R),
    ("132","Scott McTominay","Scotland",R),("133","John McGinn","Scotland",R),("134","Billy Gilmour","Scotland",R),
    ("135","Bradley Barcola","France",R),("136","Manu Kone","France",R),("137","Ousmane Dembele","France",R),
    ("138","Jules Kounde","France",R),("139","Mike Maignan","France",R),("140","Michael Olise","France",R),
    ("141","Eduardo Camavinga","France",R),("142","William Saliba","France",R),("143","Desire Doue","France",R),
    ("144","Matteo Guendouzi","France",R),("145","Kylian Mbappe","France",R),("146","Randal Kolo Muani","France",R),
    ("147","Theo Hernandez","France",R),("148","Marcus Thuram","France",R),("149","Warren Zaire-Emery","France",R),
    ("150","Aurelien Tchouameni","France",R),
    ("151","Ramon Sosa","Paraguay",R),("152","Julio Enciso","Paraguay",R),("153","Diego Gomez","Paraguay",R),
    ("154","Lionel Messi","Argentina",R),("155","Thiago Almada","Argentina",R),("156","Alexis Mac Allister","Argentina",R),
    ("157","Julian Alvarez","Argentina",R),("158","Enzo Fernandez","Argentina",R),("159","Nico Gonzalez","Argentina",R),
    ("160","Emiliano Martinez","Argentina",R),("161","Rodrigo de Paul","Argentina",R),("162","Cristian Romero","Argentina",R),
    ("163","Lautaro Martinez","Argentina",R),("164","Nico Paz","Argentina",R),("165","Giuliano Simeone","Argentina",R),
    ("166","Martin Odegaard","Norway",R),("167","Andreas Schjelderup","Norway",R),("168","Antonio Nusa","Norway",R),
    ("169","Alexander Sorloth","Norway",R),("170","Erling Haaland","Norway",R),("171","Sander Berge","Norway",R),
    ("172","Caoimhin Kelleher","Republic of Ireland",R),("173","Nathan Collins","Republic of Ireland",R),
    ("174","Evan Ferguson","Republic of Ireland",R),
    ("175","Gregor Kobel","Switzerland",R),("176","Manuel Akanji","Switzerland",R),("177","Granit Xhaka","Switzerland",R),
    ("178","Breel Embolo","Switzerland",R),
    ("179","Vini Jr.","Brazil",R),("180","Gabriel Magalhaes","Brazil",R),("181","Bruno Guimaraes","Brazil",R),
    ("182","Matheus Cunha","Brazil",R),("183","Rodrygo","Brazil",R),("184","Gabriel Martinelli","Brazil",R),
    ("185","Alisson Becker","Brazil",R),("186","Savinho","Brazil",R),("187","Vanderson","Brazil",R),("188","Endrick","Brazil",R),
    ("189","Calvin Bassey","Nigeria",R),("190","Victor Osimhen","Nigeria",R),("191","Ademola Lookman","Nigeria",R),
    ("192","Victor Boniface","Nigeria",R),("193","Alex Iwobi","Nigeria",R),("194","Samuel Chukwueze","Nigeria",R),
    ("195","Piotr Zielinski","Poland",R),("196","Jakub Kiwior","Poland",R),("197","Robert Lewandowski","Poland",R),
    ("198","Kacper Urbanski","Poland",R),("199","Sebastian Szymanski","Poland",R),("200","Nicola Zalewski","Poland",R),
]
add_cards(insert_sets["Base"], base_cards)
print(f"  Base: {len(base_cards)} cards")

# ─── Rated Rookies (201-250) ─────────────────────────────────────
T = True
rr_cards = [
    ("201","Damion Downs","United States",T),("202","Alex Freeman","United States",T),("203","Jaminton Campaz","Colombia",T),
    ("204","Franjo Ivanovic","Croatia",T),("205","Petar Sucic","Croatia",T),("206","Jordan James","Cymru",T),
    ("207","Lewis Koumas","Cymru",T),("208","Nick Woltemade","Germany",T),("209","Lawrence Agyekum","Ghana",T),
    ("210","Ebenezer Annan","Ghana",T),("211","Denzell Garcia","Mexico",T),("212","Erik Lira","Mexico",T),
    ("213","Pablo Monroy","Mexico",T),("214","Gilberto Mora","Mexico",T),("215","Luka Vuskovic","Croatia",T),
    ("216","Osame Sahraoui","Morocco",T),("217","Oussama Targhalline","Morocco",T),("218","Tolu Arokodare","Nigeria",T),
    ("219","Isaac Price","Northern Ireland",T),("220","Justin Devenny","Northern Ireland",T),
    ("221","Pierce Charles","Northern Ireland",T),("222","Shea Charles","Northern Ireland",T),
    ("223","Sindre Walle Egeli","Norway",T),("224","Thelo Aasgaard","Norway",T),
    ("225","Damian Bobadilla","Paraguay",T),("226","Matias Galarza Fonda","Paraguay",T),
    ("227","Antoni Kozubal","Poland",T),("228","Przemyslaw Wisniewski","Poland",T),
    ("229","Andrew Moran","Republic of Ireland",T),("230","Rocco Vata","Republic of Ireland",T),
    ("231","Troy Parrott","Republic of Ireland",T),
    ("232","James Wilson","Scotland",T),("233","Max Johnston","Scotland",T),("234","Tommy Conway","Scotland",T),
    ("235","Antoine Mendy","Senegal",T),("236","El Hadji Malick Diouf","Senegal",T),("237","Ilay Camara","Senegal",T),
    ("238","Andrija Maksimovic","Serbia",T),("239","Mihailo Ivanovic","Serbia",T),("240","Mihajlo Cvetkovic","Serbia",T),
    ("241","Ognjen Mimovic","Serbia",T),("242","Besfort Zeneli","Sweden",T),("243","Hugo Bolin","Sweden",T),
    ("244","Nils Zatterstrom","Sweden",T),("245","Sebastian Nanasi","Sweden",T),
    ("246","Noahkai Banks","United States",T),("247","Alvyn Sanches","Switzerland",T),
    ("248","Aurele Amenda","Switzerland",T),("249","Leonidas Stergiou","Switzerland",T),
    ("250","Johan Manzambi","Switzerland",T),
]
add_cards(insert_sets["Base - Rated Rookies"], rr_cards)
print(f"  Base - Rated Rookies: {len(rr_cards)} cards")

# ─── Copy Base → Base Optic ──────────────────────────────────────
def copy_cards(src_is_id, dst_is_id):
    rows = cur.execute("SELECT player_id, card_number, is_rookie, team FROM player_appearances WHERE insert_set_id = ?", (src_is_id,)).fetchall()
    for player_id, card_number, is_rookie, team in rows:
        cur.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)",
                    (player_id, dst_is_id, card_number, is_rookie, team))
    return len(rows)

n1 = copy_cards(insert_sets["Base"], insert_sets["Base Optic"])
n2 = copy_cards(insert_sets["Base - Rated Rookies"], insert_sets["Base Optic - Rated Rookies"])
print(f"  Base Optic: {n1} cards (copied from Base)")
print(f"  Base Optic - Rated Rookies: {n2} cards (copied from Base - Rated Rookies)")

# ─── Generate slugs ──────────────────────────────────────────────
cur.execute("SELECT id, name FROM players WHERE set_id = ?", (set_id,))
all_players = cur.fetchall()
used_slugs = set()
for pid, pname in all_players:
    slug = slugify(pname)
    if slug in used_slugs:
        i = 2
        while f"{slug}-{i}" in used_slugs: i += 1
        slug = f"{slug}-{i}"
    used_slugs.add(slug)
    cur.execute("UPDATE players SET slug = ? WHERE id = ?", (slug, pid))

# ─── Commit ──────────────────────────────────────────────────────
conn.commit()

# Stats
player_count = cur.execute("SELECT COUNT(*) FROM players WHERE set_id = ?", (set_id,)).fetchone()[0]
app_count = cur.execute("SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON pa.insert_set_id = i.id WHERE i.set_id = ?", (set_id,)).fetchone()[0]
is_count = cur.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id = ?", (set_id,)).fetchone()[0]

print(f"\nDone! Set ID: {set_id}")
print(f"  Players: {player_count}")
print(f"  Appearances: {app_count}")
print(f"  Insert sets: {is_count}")
conn.close()
