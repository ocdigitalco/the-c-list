"""
Seed: 2025-26 Donruss Road to FIFA World Cup 26 — Part 2
Insert sets and memorabilia cards.
Usage: python3 scripts/seed_donruss_fifa_2025_part2.py
"""
import sqlite3, os, re

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA foreign_keys=ON")
cur = conn.cursor()

SET_ID = 836

def get_or_create_player(name):
    cur.execute("SELECT id FROM players WHERE set_id = ? AND name = ?", (SET_ID, name))
    row = cur.fetchone()
    if row: return row[0]
    cur.execute("INSERT INTO players (set_id, name, unique_cards, total_print_run, one_of_ones, insert_set_count) VALUES (?, ?, 0, 0, 0, 0)", (SET_ID, name))
    return cur.lastrowid

def get_is_id(name):
    row = cur.execute("SELECT id FROM insert_sets WHERE set_id = ? AND name = ?", (SET_ID, name)).fetchone()
    if not row: raise ValueError(f"Insert set '{name}' not found")
    return row[0]

def add_cards(is_name, cards):
    is_id = get_is_id(is_name)
    for num, name, team, rookie in cards:
        pid = get_or_create_player(name)
        cur.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)",
                    (pid, is_id, num, int(rookie), team))
    print(f"  {is_name}: {len(cards)} cards")

R = False
T = True

# ─── ANIMATION ────────────────────────────────────────────────────
add_cards("Animation", [
    ("1","Lamine Yamal","Spain",R),("2","Erling Haaland","Norway",R),("3","Nico Williams","Spain",R),
    ("4","Lionel Messi","Argentina",R),("5","Cristiano Ronaldo","Portugal",R),("6","Kylian Mbappe","France",R),
    ("7","Viktor Gyokeres","Sweden",R),("8","Florian Wirtz","Germany",R),("9","Vini Jr.","Brazil",R),
    ("10","Robert Lewandowski","Poland",R),("11","Luka Modric","Croatia",R),("12","Alexander Isak","Sweden",R),
    ("13","Pedri","Spain",R),("14","Jude Bellingham","England",R),("15","Kaka","Brazil",R),
    ("16","Gabriel Batistuta","Argentina",R),("17","Gianluigi Buffon","Italy",R),("18","Luis Suarez","Uruguay",R),
    ("19","Ronaldo","Brazil",R),("20","Edinson Cavani","Uruguay",R),("21","Neymar Jr","Brazil",R),
    ("22","Manuel Neuer","Germany",R),("23","Pele","Brazil",R),("24","Diego Maradona","Argentina",R),
    ("25","Franz Beckenbauer","Germany",R),
])

# ─── CRAFTSMEN ────────────────────────────────────────────────────
add_cards("Craftsmen", [
    ("1","Cristian Romero","Argentina",R),("2","Gabriel Martinelli","Brazil",R),("3","Chris Richards","United States",R),
    ("4","James Rodriguez","Colombia",R),("5","Ivan Perisic","Croatia",R),("6","Ollie Watkins","England",R),
    ("7","Eduardo Camavinga","France",R),("8","Joshua Kimmich","Germany",R),("9","Mohammed Salisu","Ghana",R),
    ("10","Deybi Flores","Honduras",R),("11","Sandro Tonali","Italy",R),("12","In-Beom Hwang","Korea Republic",R),
    ("13","Santiago Gimenez","Mexico",R),("14","Noussair Mazraoui","Morocco",R),("15","Ademola Lookman","Nigeria",R),
    ("16","Enzo Fernandez","Argentina",R),("17","Bruno Guimaraes","Brazil",R),("18","Marcus Rashford","England",R),
    ("19","Alessandro Bastoni","Italy",R),("20","Goncalo Ramos","Portugal",R),("21","Dani Olmo","Spain",R),
    ("22","Ruben Vargas","Switzerland",R),("23","Joao Neves","Portugal",R),("24","Jakub Moder","Poland",R),
    ("25","Fabian Ruiz","Spain",R),
])

# ─── DOMINATORS ───────────────────────────────────────────────────
add_cards("Dominators", [
    ("1","Leroy Sane","Germany",R),("2","Gianluigi Donnarumma","Italy",R),("3","Lionel Messi","Argentina",R),
    ("4","Francisco Conceicao","Portugal",R),("5","Kalidou Koulibaly","Senegal",R),("6","Declan Rice","England",R),
    ("7","Nico Williams","Spain",R),("8","Mohammed Kudus","Ghana",R),("9","Alisson Becker","Brazil",R),
    ("10","Josko Gvardiol","Croatia",R),("11","David Raum","Germany",R),("12","Alexander Isak","Sweden",R),
    ("13","Yassine Bounou","Morocco",R),("14","Morgan Rogers","England",R),("15","Mateo Retegui","Italy",R),
    ("16","Nuno Mendes","Portugal",R),("17","Emiliano Martinez","Argentina",R),("18","Antonee Robinson","United States",R),
    ("19","Mikel Oyarzabal","Spain",R),("20","Dusan Vlahovic","Serbia",R),("21","Vini Jr.","Brazil",R),
    ("22","Martin Odegaard","Norway",R),("23","Diego Maradona","Argentina",R),("24","Franz Beckenbauer","Germany",R),
    ("25","Pele","Brazil",R),
])

# ─── ELITE SERIES ─────────────────────────────────────────────────
add_cards("Elite Series", [
    ("1","Brennan Johnson","Cymru",R),("2","Idrissa Gueye","Senegal",R),("3","Christian Pulisic","United States",R),
    ("4","Martin Baturina","Croatia",R),("5","Paddy McNair","Northern Ireland",R),("6","Jose Maria Gimenez","Uruguay",R),
    ("7","Lazar Samardzic","Serbia",R),("8","Aleksandar Pavlovic","Germany",R),("9","Gianluigi Donnarumma","Italy",R),
    ("10","Anthony Elanga","Sweden",R),("11","Vanderson","Brazil",R),("12","Jae-sung Lee","Korea Republic",R),
    ("13","Denil Maldonado","Honduras",R),("14","Vitinha","Portugal",R),("15","Ezri Konsa","England",R),
    ("16","Che Adams","Scotland",R),("17","Antonio Sanabria","Paraguay",R),("18","Erling Haaland","Norway",R),
    ("19","Evan Ferguson","Republic of Ireland",R),("20","Ousmane Dembele","France",R),
    ("21","Nicolas Otamendi","Argentina",R),("22","Karol Swiderski","Poland",R),("23","Zeki Amdouni","Switzerland",R),
    ("24","Mateo Kovacic","Croatia",R),("25","Lamine Yamal","Spain",R),
])

# ─── KABOOM ───────────────────────────────────────────────────────
add_cards("Kaboom", [
    ("1","Lionel Messi","Argentina",R),("2","Cristiano Ronaldo","Portugal",R),("3","Heung-Min Son","Korea Republic",R),
    ("4","Jude Bellingham","England",R),("5","Bukayo Saka","England",R),("6","Vini Jr.","Brazil",R),
    ("7","Martin Odegaard","Norway",R),("8","Luka Modric","Croatia",R),("9","Moise Kean","Italy",R),
    ("10","Kai Havertz","Germany",R),("11","Alexander Isak","Sweden",R),("12","Lamine Yamal","Spain",R),
    ("13","Pedri","Spain",R),("14","Michael Olise","France",R),("15","Robert Lewandowski","Poland",R),
    ("16","Edinson Cavani","Uruguay",R),("17","Angel Di Maria","Argentina",R),("18","Thierry Henry","France",R),
    ("19","Mesut Ozil","Germany",R),("20","Ronaldo","Brazil",R),("21","Sergio Aguero","Argentina",R),
    ("23","Pele","Brazil",R),("24","Diego Maradona","Argentina",R),("25","Franz Beckenbauer","Germany",R),
])

# ─── KABOOM OVERSIZE (copy from Kaboom) ───────────────────────────
kaboom_is = get_is_id("Kaboom")
oversize_is = get_is_id("Kaboom Oversize")
kaboom_rows = cur.execute("SELECT player_id, card_number, is_rookie, team FROM player_appearances WHERE insert_set_id = ?", (kaboom_is,)).fetchall()
for pid, cn, ir, team in kaboom_rows:
    cur.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)",
                (pid, oversize_is, cn, ir, team))
print(f"  Kaboom Oversize: {len(kaboom_rows)} cards (copied)")

# ─── MAGICIANS ────────────────────────────────────────────────────
add_cards("Magicians", [
    ("1","Moise Kean","Italy",R),("2","Marcus Thuram","France",R),("3","Bernardo Silva","Portugal",R),
    ("4","Rodrygo","Brazil",R),("5","Luka Modric","Croatia",R),("6","Antonio Nusa","Norway",R),
    ("7","Alexis Mac Allister","Argentina",R),("8","Marc Cucurella","Spain",R),("9","Folarin Balogun","United States",R),
    ("10","Trent Alexander-Arnold","England",R),("11","Riccardo Calafiori","Italy",R),("12","Dan Ndoye","Switzerland",R),
    ("13","Endrick","Brazil",R),("14","Victor Osimhen","Nigeria",R),("15","Pascal Gross","Germany",R),
    ("16","Scott McTominay","Scotland",R),("17","Heung-Min Son","Korea Republic",R),("18","Pedro Neto","Portugal",R),
    ("19","Antoine Semenyo","Ghana",R),("20","Maximiliano Araujo","Uruguay",R),("21","Robin Koch","Germany",R),
    ("22","Robert Lewandowski","Poland",R),("23","Eberechi Eze","England",R),("24","Pedri","Spain",R),
    ("25","Nico Paz","Argentina",R),
])

# ─── NET MARVELS ──────────────────────────────────────────────────
add_cards("Net Marvels", [
    ("1","Jordan Pickford","England",R),("2","Cristiano Ronaldo","Portugal",R),("3","Moise Kean","Italy",R),
    ("4","Luis Diaz","Colombia",R),("5","Rodrygo","Brazil",R),("6","Inaki Williams","Ghana",R),
    ("7","Robert Lewandowski","Poland",R),("8","Raul Jimenez","Mexico",R),("9","Samu Aghehowa","Spain",R),
    ("10","Alexander Isak","Sweden",R),("11","Ricardo Pepi","United States",R),("12","Dominic Solanke","England",R),
    ("13","Youssef En-Nesyri","Morocco",R),("14","Julian Alvarez","Argentina",R),("15","Randal Kolo Muani","France",R),
    ("16","Federico Valverde","Uruguay",R),("17","Mateo Retegui","Italy",R),("18","Vini Jr.","Brazil",R),
    ("19","Alexander Sorloth","Norway",R),("20","Victor Boniface","Nigeria",R),("21","Lionel Messi","Argentina",R),
    ("22","Serge Gnabry","Germany",R),("23","Ferran Torres","Spain",R),("24","Viktor Gyokeres","Sweden",R),
    ("25","Rafael Leao","Portugal",R),
])

# ─── NIGHT MOVES ──────────────────────────────────────────────────
add_cards("Night Moves", [
    ("1","Christian Pulisic","United States",R),("2","Harry Kane","England",R),("3","Rodrygo","Brazil",R),
    ("4","Endrick","Brazil",R),("5","Lionel Messi","Argentina",R),("6","Cristiano Ronaldo","Portugal",R),
    ("7","Phil Foden","England",R),("8","Cole Palmer","England",R),("9","Nico Williams","Spain",R),
    ("10","Erling Haaland","Norway",R),("11","Jamal Musiala","Germany",R),("12","Bradley Barcola","France",R),
    ("13","Mateo Retegui","Italy",R),("14","Viktor Gyokeres","Sweden",R),("15","Julian Alvarez","Argentina",R),
    ("16","Luis Suarez","Uruguay",R),("17","Kaka","Brazil",R),("18","Carlos Tevez","Argentina",R),
    ("19","Lothar Matthaus","Germany",R),("20","Pele","Brazil",R),("21","Steven Gerrard","England",R),
    ("22","Neymar Jr","Brazil",R),("23","Diego Maradona","Argentina",R),("24","Paolo Maldini","Italy",R),
    ("25","Franz Beckenbauer","Germany",R),
])

# ─── PITCH KINGS ──────────────────────────────────────────────────
add_cards("Pitch Kings", [
    ("1","Savinho","Brazil",R),("2","Bruno Fernandes","Portugal",R),("3","Tom Bischof","Germany",R),
    ("4","Matt Turner","United States",R),("5","Reece James","England",R),("6","Nico Williams","Spain",R),
    ("7","Davide Frattesi","Italy",R),("8","Kevin Castano","Colombia",R),("9","Lautaro Martinez","Argentina",R),
    ("10","Ruben Dias","Portugal",R),("11","Martin Odegaard","Norway",R),("12","Pedri","Spain",R),
    ("13","Endrick","Brazil",R),("14","Rodrigo de Paul","Argentina",R),("15","Luka Modric","Croatia",R),
    ("16","Achraf Hakimi","Morocco",R),("17","Maximilian Mittelstadt","Germany",R),("18","Curtis Jones","England",R),
    ("19","Mike Maignan","France",R),("20","Darwin Nunez","Uruguay",R),("21","Giovanni Di Lorenzo","Italy",R),
    ("22","Hugo Larsson","Sweden",R),("23","Pele","Brazil",R),("24","Diego Maradona","Argentina",R),
    ("25","Franz Beckenbauer","Germany",R),
])

# ─── ROOKIE KINGS ─────────────────────────────────────────────────
add_cards("Rookie Kings", [
    ("1","Denzell Garcia","Mexico",T),("2","Petar Sucic","Croatia",T),("3","Osame Sahraoui","Morocco",T),
    ("4","Shea Charles","Northern Ireland",T),("5","El Hadji Malick Diouf","Senegal",T),
    ("6","Sindre Walle Egeli","Norway",T),("7","Troy Parrott","Republic of Ireland",T),
    ("8","Tolu Arokodare","Nigeria",T),("9","Sebastian Nanasi","Sweden",T),("10","Gilberto Mora","Mexico",T),
    ("11","Mihajlo Cvetkovic","Serbia",T),("12","Dominik Marczuk","Poland",T),("13","Justin Devenny","Northern Ireland",T),
    ("14","Alvyn Sanches","Switzerland",T),("15","Jordan James","Cymru",T),("16","Luciano Rodriguez","Uruguay",T),
    ("17","Luka Vuskovic","Croatia",T),("18","Pierce Charles","Northern Ireland",T),("19","Hugo Bolin","Sweden",T),
    ("20","Erik Lira","Mexico",T),("21","Leonidas Stergiou","Switzerland",T),("22","Tommy Conway","Scotland",T),
    ("23","Damion Downs","United States",T),("24","Andrija Maksimovic","Serbia",T),("25","Nick Woltemade","Germany",T),
])

# ─── ZERO GRAVITY ─────────────────────────────────────────────────
add_cards("Zero Gravity", [
    ("1","Isaac Price","Northern Ireland",R),("2","Erling Haaland","Norway",R),("3","Miguel Almiron","Paraguay",R),
    ("4","Piotr Zielinski","Poland",R),("5","Diogo Costa","Portugal",R),("6","Jake O'Brien","Republic of Ireland",R),
    ("7","Andy Robertson","Scotland",R),("8","Assane Diao","Senegal",R),("9","Ivan Ilic","Serbia",R),
    ("10","Lamine Yamal","Spain",R),("11","Viktor Gyokeres","Sweden",R),("12","Gregor Kobel","Switzerland",R),
    ("13","Brenden Aaronson","United States",R),("14","Federico Valverde","Uruguay",R),("15","Ethan Ampadu","Cymru",R),
    ("16","Theo Hernandez","France",R),("17","Lautaro Martinez","Argentina",R),("18","Jamie Leweling","Germany",R),
    ("19","Nicolo Barella","Italy",R),("20","Cristiano Ronaldo","Portugal",R),("21","Gabriel Magalhaes","Brazil",R),
    ("22","Daniel Munoz","Colombia",R),("23","Mikel Merino","Spain",R),("24","Nico Schlotterbeck","Germany",R),
    ("25","Levi Colwill","England",R),
])

# ─── KIT KINGS ────────────────────────────────────────────────────
add_cards("Kit Kings", [
    ("1","Ethan Ampadu","Cymru",R),("2","Brennan Johnson","Cymru",R),("3","Maximiliano Araujo","Uruguay",R),
    ("4","Federico Valverde","Uruguay",R),("5","Josh Sargent","United States",R),("6","Giovanni Reyna","United States",R),
    ("7","Weston McKennie","United States",R),("8","Alexander Isak","Sweden",R),("9","Dejan Kulusevski","Sweden",R),
    ("10","Pedri","Spain",R),("11","Dean Huijsen","Spain",R),("12","Lamine Yamal","Spain",R),
    ("13","Strahinja Pavlovic","Serbia",R),("14","Andrija Maksimovic","Serbia",R),("15","Ismaila Sarr","Senegal",R),
    ("16","Lamine Camara","Senegal",R),("17","Cristiano Ronaldo","Portugal",R),("18","Rafael Leao","Portugal",R),
    ("19","Omar Alderete","Paraguay",R),("20","Alexander Sorloth","Norway",R),("21","Erling Haaland","Norway",R),
    ("22","Achraf Hakimi","Morocco",R),("23","Ismael Saibari","Morocco",R),("24","Luis Malagon","Mexico",R),
    ("25","Raul Jimenez","Mexico",R),("26","Min-jae Kim","Korea Republic",R),("27","Heung-Min Son","Korea Republic",R),
    ("28","Nicolo Barella","Italy",R),("29","Gianluigi Donnarumma","Italy",R),("30","Samuele Ricci","Italy",R),
    ("31","Tom Bischof","Germany",R),("32","Nick Woltemade","Germany",R),("33","Kai Havertz","Germany",R),
    ("34","Jonathan Tah","Germany",R),("35","William Saliba","France",R),("36","Manu Kone","France",R),
    ("37","Ousmane Dembele","France",R),("38","Desire Doue","France",R),("39","Anthony Gordon","England",R),
    ("40","Kyle Walker","England",R),("41","Jarrod Bowen","England",R),("42","Ivan Perisic","Croatia",R),
    ("43","Luka Modric","Croatia",R),("44","Luis Diaz","Colombia",R),("45","Jefferson Lerma","Colombia",R),
    ("46","Endrick","Brazil",R),("47","Savinho","Brazil",R),("48","Rodrygo","Brazil",R),
    ("49","Nico Paz","Argentina",R),("50","Lionel Messi","Argentina",R),
])

# ─── KIT SERIES ───────────────────────────────────────────────────
add_cards("Kit Series", [
    ("1","Lautaro Martinez","Argentina",R),("2","Julian Alvarez","Argentina",R),("3","Vini Jr.","Brazil",R),
    ("4","Gabriel Martinelli","Brazil",R),("5","Bruno Guimaraes","Brazil",R),("6","Jhon Duran","Colombia",R),
    ("7","James Rodriguez","Colombia",R),("8","Ante Budimir","Croatia",R),("9","Andrej Kramaric","Croatia",R),
    ("10","Curtis Jones","England",R),("11","Ezri Konsa","England",R),("12","Reece James","England",R),
    ("13","Matteo Guendouzi","France",R),("14","Jules Kounde","France",R),("15","Aurelien Tchouameni","France",R),
    ("16","Michael Olise","France",R),("17","Jamal Musiala","Germany",R),("18","Angelo Stiller","Germany",R),
    ("19","Florian Wirtz","Germany",R),("20","Antonio Rudiger","Germany",R),("21","Mateo Retegui","Italy",R),
    ("22","Nicolo Rovella","Italy",R),("23","Moise Kean","Italy",R),("24","Min-Hyuk Yang","Korea Republic",R),
    ("25","Jun-Ho Bae","Korea Republic",R),("26","Roberto Alvarado","Mexico",R),("27","Santiago Gimenez","Mexico",R),
    ("28","Eliesse Ben Seghir","Morocco",R),("29","Bilal El Khannouss","Morocco",R),("30","Martin Odegaard","Norway",R),
    ("31","Sindre Walle Egeli","Norway",R),("32","Renato Veiga","Portugal",R),("33","Bruno Fernandes","Portugal",R),
    ("34","Seamus Coleman","Republic of Ireland",R),("35","Sadio Mane","Senegal",R),("36","Nicolas Jackson","Senegal",R),
    ("37","Mihajlo Cvetkovic","Serbia",R),("38","Dusan Vlahovic","Serbia",R),("39","Pau Cubarsi","Spain",R),
    ("40","Samu Aghehowa","Spain",R),("41","Nico Williams","Spain",R),("42","Viktor Gyokeres","Sweden",R),
    ("43","Lucas Bergvall","Sweden",R),("44","Benjamin Cremaschi","United States",R),("45","Diego Luna","United States",R),
    ("46","Christian Pulisic","United States",R),("47","Darwin Nunez","Uruguay",R),("48","Mathias Olivera","Uruguay",R),
    ("49","Neco Williams","Cymru",R),("50","Daniel James","Cymru",R),
])

# ─── Generate slugs for new players ──────────────────────────────
cur.execute("SELECT id, name FROM players WHERE set_id = ? AND slug IS NULL", (SET_ID,))
new_players = cur.fetchall()
existing_slugs = set(r[0] for r in cur.execute("SELECT slug FROM players WHERE set_id = ? AND slug IS NOT NULL", (SET_ID,)).fetchall())

def slugify(text):
    s = text.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_]+', '-', s)
    return re.sub(r'-+', '-', s).strip('-')

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
app_count = cur.execute("SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON pa.insert_set_id = i.id WHERE i.set_id = ?", (SET_ID,)).fetchone()[0]
player_count = cur.execute("SELECT COUNT(*) FROM players WHERE set_id = ?", (SET_ID,)).fetchone()[0]

print(f"\nDone! Set ID: {SET_ID}")
print(f"  Total players: {player_count}")
print(f"  Total appearances: {app_count}")
conn.close()
