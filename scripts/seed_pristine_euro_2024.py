"""
Seed script: 2023 Topps Pristine Road to Euro 2024
Usage: python3 scripts/seed_pristine_euro_2024.py
"""
import sqlite3, json, os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA foreign_keys=ON")
cur = conn.cursor()

def get_or_create_player(set_id, name):
    cur.execute("SELECT id FROM players WHERE set_id = ? AND name = ?", (set_id, name))
    r = cur.fetchone()
    if r: return r[0]
    cur.execute("INSERT INTO players (set_id, name, unique_cards, total_print_run, one_of_ones, insert_set_count) VALUES (?, ?, 0, 0, 0, 0)", (set_id, name))
    return cur.lastrowid

def create_insert_set(set_id, name):
    cur.execute("INSERT INTO insert_sets (set_id, name) VALUES (?, ?)", (set_id, name))
    return cur.lastrowid

def create_parallel(is_id, name, pr):
    cur.execute("INSERT INTO parallels (insert_set_id, name, print_run) VALUES (?, ?, ?)", (is_id, name, pr))

def create_appearance(pid, is_id, cn, team=None):
    cur.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, ?)", (pid, is_id, cn, team))
    return cur.lastrowid

def create_co_player(app_id, co_pid):
    cur.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (app_id, co_pid))

def add_cards(is_id, cards):
    for cn, name, team in cards:
        pid = get_or_create_player(set_id, name)
        create_appearance(pid, is_id, cn, team)

def add_dual_cards(is_id, cards):
    for cn, pairs in cards:
        aids, pids = [], []
        for name, team in pairs:
            pid = get_or_create_player(set_id, name)
            aid = create_appearance(pid, is_id, cn, team)
            aids.append(aid); pids.append(pid)
        for i, aid in enumerate(aids):
            for j, cpid in enumerate(pids):
                if i != j: create_co_player(aid, cpid)

def make_is(name, pars, cards, dual=False):
    is_id = create_insert_set(set_id, name)
    for pn, pr in pars: create_parallel(is_id, pn, pr)
    if dual: add_dual_cards(is_id, cards)
    else: add_cards(is_id, cards)
    return is_id

# ─── Create set ───────────────────────────────────────────────────────────────

SET_NAME = "2023 Topps Pristine Road to Euro 2024"
cur.execute("SELECT id FROM sets WHERE name = ?", (SET_NAME,))
if cur.fetchone():
    print(f"Set '{SET_NAME}' already exists. Aborting."); conn.close(); exit(1)

box_config = {"hobby": {"cards_per_pack": 10, "packs_per_box": 6, "boxes_per_case": 8, "autos_per_box": 3, "fresh_faces_per_box": 3, "inevitable_per_box": 3, "pristine_borders_per_box": 5, "refractors_per_box": 6}}
pack_odds = {"hobby": {"Refractor": "1:1", "Inevitable": "1:3", "Fresh Faces": "1:3", "Pristine Borders": "1:2", "Marvelous Moments": "1:12"}}

import re, unicodedata
def slugify(text):
    s = text.lower()
    s = unicodedata.normalize("NFD", s)
    s = re.sub(r"[\u0300-\u036f]", "", s)
    s = re.sub(r"[®©™'':]", "", s)
    s = re.sub(r"\s+x\s+", " ", s)
    s = re.sub(r"[^a-z0-9-]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s

slug = slugify(SET_NAME)

cur.execute("INSERT INTO sets (name, sport, season, league, tier, release_date, box_config, pack_odds, slug) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
    (SET_NAME, "Soccer", "2023", "UEFA", "Premium", "2024-04-26", json.dumps(box_config), json.dumps(pack_odds), slug))
set_id = cur.lastrowid
print(f"Created set '{SET_NAME}' with id {set_id}")

# ─── Parallels ────────────────────────────────────────────────────────────────

BASE_PARS = [("Refractor", None), ("Green Refractor", 125), ("Purple Refractor", 99), ("Blue Refractor", 75), ("Blue Pristine Refractor", 75), ("Gold Refractor", 50), ("Gold Pristine Refractor", 50), ("Orange Refractor", 25), ("Orange Pristine Refractor", 25), ("Red Refractor", 5), ("Red Pristine Refractor", 5), ("Black Pristine Refractor", 1), ("Superfractor", 1)]
MM_AUTO_PARS = [("Red Refractor", 5), ("Superfractor", 1)]
PD_RELIC_PARS = [("Orange Refractor", 25), ("Pink Refractor", 15), ("Red Refractor", 5), ("Superfractor", 1)]
PRISTINE_AUTO_PARS = [("Pristine", 99), ("Gold Pristine", 50), ("Orange Pristine", 25), ("Black Pristine", 1)]
PB_RELIC_PARS = [("Pristine", 99), ("Gold Refractor", 50), ("Orange Refractor", 25), ("Red Refractor", 5), ("Superfractor", 1)]
PB_AUTO_PARS = [("Gold Refractor", 50), ("Orange Refractor", 25), ("Red Refractor", 5), ("Superfractor", 1)]
DUAL_PARS = [("Red Refractor", 5), ("Superfractor", 1)]
PRODIGY_AUTO_PARS = [("Red Refractor", 5), ("Superfractor", 1)]
INSERT_PARS = [("Gold Refractor", 50), ("Orange Refractor", 25), ("Red Refractor", 5), ("Superfractor", 1)]
ICONIC_PARS = [("Red Refractor", 5), ("Superfractor", 1)]
PRODIGY_PARS = [("Red Refractor", 5), ("Superfractor", 1)]

# ─── BASE SET (200 cards) ────────────────────────────────────────────────────

BASE = [
    ("1","David Alaba","Austria"),("2","Yusuf Demir","Austria"),("3","Patrick Wimmer","Austria"),("4","Marcel Sabitzer","Austria"),("5","Muhammed Cham","Austria"),("6","Nicolas Seiwald","Austria"),
    ("7","Romelu Lukaku","Belgium"),("8","Kevin De Bruyne","Belgium"),("9","Thibaut Courtois","Belgium"),("10","Charles De Ketelaere","Belgium"),("11","Zeno Debast","Belgium"),("12","Youri Tielemans","Belgium"),("13","Yannick Carrasco","Belgium"),("14","Leandro Trossard","Belgium"),("15","Lo\u00efs Openda","Belgium"),
    ("16","Mateo Kova\u010di\u0107","Croatia"),("17","Josip \u0160utalo","Croatia"),("18","Luka Modri\u0107","Croatia"),("19","Luka Su\u010di\u0107","Croatia"),("20","Lovro Majer","Croatia"),("21","Jo\u0161ko Gvardiol","Croatia"),
    ("22","Mojm\u00edr Chyt\u00edl","Czechia"),("23","Tom\u00e1\u0161 Sou\u010dek","Czechia"),("24","Pavel Ned\u011bv\u011bd","Czechia"),("25","V\u00e1clav \u010cern\u00fd","Czechia"),("26","Vlad\u00edm\u00edr Coufal","Czechia"),
    ("27","Christian Eriksen","Denmark"),("28","Pierre-Emile H\u00f8jbjerg","Denmark"),("29","Mikkel Damsgaard","Denmark"),("30","Peter Schmeichel","Denmark"),
    ("31","Jack Grealish","England"),("32","Harry Kane","England"),("33","Alan Shearer","England"),("34","Michael Owen","England"),("35","\u017dan Vipotnik","Slovenia"),("36","Jonas Wind","Denmark"),("37","Phil Foden","England"),("38","Micah Richards","England"),("39","Sandi Lovri\u0107","Slovenia"),("40","Wayne Rooney","England"),
    ("41","Bari\u015f Alper Yilmaz","T\u00fcrkiye"),("42","Adam Hlo\u017eek","Czechia"),("43","Mason Mount","England"),("44","Trent Alexander-Arnold","England"),("45","Philip Billing","Denmark"),("46","Luke Shaw","England"),
    ("47","Eduardo Camavinga","France"),("48","Robert Pires","France"),("49","Theo Hern\u00e1ndez","France"),("50","Jules Kound\u00e9","France"),("51","Petar Stojanovi\u0107","Slovenia"),("52","Dominik Szoboszlai","Hungary"),("53","D\u00e1niel Gazdag","Hungary"),("54","Ousmane Demb\u00e9l\u00e9","France"),("55","Zin\u00e9dine Zidane","France"),("56","Antoine Griezmann","France"),("57","Karim Benzema","France"),("58","Moussa Diaby","France"),("59","Randal Kolo Muani","France"),
    ("60","Giorgi Mamardashvili","Georgia"),("61","Khvicha Kvaratskhelia","Georgia"),("62","Zuriko Davitashvili","Georgia"),("63","Giorgi Tsitaishvili","Georgia"),
    ("64","Matthias Sammer","Germany"),("65","Youssoufa Moukoko","Germany"),("66","Sepp Maier","Germany"),("67","Timo Werner","Germany"),("68","Thomas M\u00fcller","Germany"),
    ("69","Petar Musa","Croatia"),("70","\u00c1d\u00e1m Nagy","Hungary"),("71","Willi Orb\u00e1n","Hungary"),("72","Konrad Laimer","Austria"),("73","Mario Pa\u0161ali\u0107","Croatia"),("74","D\u00e9nes Dibusz","Hungary"),("75","Luka Ivanu\u0161ec","Croatia"),
    ("76","Jamal Musiala","Germany"),("77","Anthony Elanga","Sweden"),("78","\u00cdsak Bergmann Johannesso","Iceland"),("79","Eidur Gudjohnsen","Iceland"),("80","Andri Gudjohnsen","Iceland"),("81","\u00cdsak Snaer Thorvaldsson","Iceland"),
    ("82","Oscar Gloukh","Israel"),("83","Omri Glazer","Israel"),("84","Liel Abada","Israel"),("85","Eden Karzev","Israel"),("86","Manor Solomon","Israel"),
    ("87","Gianluigi Buffon","Italy"),("88","Giorgio Chiellini","Italy"),("89","Filippo Inzaghi","Italy"),("90","Nicol\u00f2 Fagioli","Italy"),("91","Benjamin \u0160e\u0161ko","Slovenia"),("92","Sandro Tonali","Italy"),("93","Marco Verratti","Italy"),("94","Gareth Bale","Wales"),("95","Gianluigi Donnarumma","Italy"),("96","Wilfried Gnonto","Italy"),
    ("97","Rasmus H\u00f8jlund","Denmark"),("98","H\u00e1kon Arnar Haraldsson","Iceland"),("99","Johan Bakayoko","Belgium"),("100","Elias Jelert","Denmark"),
    ("101","Jan Oblak","Slovenia"),("102","Orkun K\u00f6k\u00e7\u00fc","T\u00fcrkiye"),("103","Francesco Totti","Italy"),("104","Samuele Ricci","Italy"),
    ("105","Cody Gakpo","Netherlands"),("106","Xavi Simons","Netherlands"),("107","Frenkie de Jong","Netherlands"),("108","Memphis Depay","Netherlands"),("109","Denzel Dumfries","Netherlands"),("110","Matthijs de Ligt","Netherlands"),("111","Virgil van Dijk","Netherlands"),("112","Dennis Bergkamp","Netherlands"),("113","Patrick Kluivert","Netherlands"),("114","Tyrell Malacia","Netherlands"),("115","Wout Weghorst","Netherlands"),("116","Ronald De Boer","Netherlands"),
    ("117","Leo \u00d8stig\u00e5rd","Norway"),("118","Erling Haaland","Norway"),("119","Martin \u00d8degaard","Norway"),("120","Hugo Vetlesen","Norway"),("121","Ola Brynhildsen","Norway"),("122","Sivert Mannsverk","Norway"),
    ("123","Robert Lewandowski","Poland"),("124","Wojciech Szcz\u0119sny","Poland"),("125","Nicola Zalewski","Poland"),("126","Piotr Zieli\u0144ski","Poland"),("127","Jakub Kiwior","Poland"),("128","Arkadiusz Milik","Poland"),("129","Sebastian Szyma\u0144ski","Poland"),
    ("130","Bernardo Silva","Portugal"),("131","Cristiano Ronaldo","Portugal"),("132","Vitinha","Portugal"),("133","Bruno Fernandes","Portugal"),("134","Jo\u00e3o Cancelo","Portugal"),("135","R\u00faben Dias","Portugal"),("136","Lu\u00eds Figo","Portugal"),("137","Jo\u00e3o F\u00e9lix","Portugal"),("138","Ant\u00f3nio Silva","Portugal"),("139","Rapha\u00ebl Guerreiro","Portugal"),("140","Matheus Nunes","Portugal"),("141","Gon\u00e7alo Ramos","Portugal"),("142","Rafael Le\u00e3o","Portugal"),
    ("143","Roy Keane","Republic of Ireland"),("144","Gavin Bazunu","Republic of Ireland"),("145","Evan Ferguson","Republic of Ireland"),("146","Matt Doherty","Republic of Ireland"),("147","Chiedozie Ogbene","Republic of Ireland"),("148","Seamus Coleman","Republic of Ireland"),
    ("149","Andy Robertson","Scotland"),("150","Jack Hendry","Scotland"),("151","Billy Gilmour","Scotland"),("152","Ryan Porteous","Scotland"),("153","Scott McTominay","Scotland"),("154","John McGinn","Scotland"),
    ("155","Aleksandar Mitrovi\u0107","Serbia"),("156","Du\u0161an Vlahovi\u0107","Serbia"),("157","Lazar Samard\u017ei\u0107","Serbia"),("158","Luka Jovi\u0107","Serbia"),("159","Du\u0161an Tadi\u0107","Serbia"),("160","Sergej Milinkovi\u0107-Savi\u0107","Serbia"),
    ("161","Nico Williams","Spain"),("162","Ansu Fati","Spain"),("163","Gavi","Spain"),("164","Sergio Busquets","Spain"),("165","Jordan James","Wales"),("166","Alejandro Balde","Spain"),("167","Rodri","Spain"),("168","Aymeric Laporte","Spain"),("169","Xabi Alonso","Spain"),("170","Andr\u00e9s Iniesta","Spain"),("171","Xavi","Spain"),("172","Pau Torres","Spain"),("173","Fernando Torres","Spain"),
    ("174","Alexander Isak","Sweden"),("175","Joe Mendes","Sweden"),("176","Bilal Hussein","Sweden"),("177","Yasin Ayari","Sweden"),("178","Dejan Kulusevski","Sweden"),("179","Hugo Larsson","Sweden"),("180","Omar Faraj","Sweden"),("181","Henrik Larsson","Sweden"),
    ("182","Granit Xhaka","Switzerland"),("183","Ardon Jashari","Switzerland"),("184","Noah Okafor","Switzerland"),("185","Denis Zakaria","Switzerland"),("186","Xherdan Shaqiri","Switzerland"),("187","Fabian Rieder","Switzerland"),("188","Manuel Akanji","Switzerland"),
    ("189","Hakan \u00c7alhano\u011flu","T\u00fcrkiye"),("190","Arda G\u00fcler","T\u00fcrkiye"),("191","Salih \u00d6zcan","T\u00fcrkiye"),("192","Emirhan \u0130lkhan","T\u00fcrkiye"),("193","Enes \u00dcnal","T\u00fcrkiye"),("194","Cengiz \u00dcnder","T\u00fcrkiye"),
    ("195","Ethan Ampadu","Wales"),("196","Dylan Levitt","Wales"),("197","Rubin Colwill","Wales"),("198","Aaron Ramsey","Wales"),("199","Brennan Johnson","Wales"),("200","Ian Rush","Wales"),
]
make_is("Base", BASE_PARS, BASE)
print("  Base: 200 cards")

# ─── AUTOGRAPH SETS ───────────────────────────────────────────────────────────

make_is("Marvelous Moments Autographs", MM_AUTO_PARS, [
    ("MMA-FT","Fernando Torres","Spain"),("MMA-MVB","Marco van Basten","Netherlands"),("MMA-PE","Pedri","Spain"),("MMA-PS","Peter Schmeichel","Denmark"),("MMA-RS","Renato Sanches","Portugal"),
])
print("  Marvelous Moments Autographs: 5 cards")

make_is("Popular Demand Autograph Relics", PD_RELIC_PARS, [
    ("PDR-BF","Bruno Fernandes","Portugal"),("PDR-CR","Cristiano Ronaldo","Portugal"),("PDR-DS","David Seaman","England"),("PDR-JB","John Barnes","England"),("PDR-KDB","Kevin De Bruyne","Belgium"),("PDR-MD","Memphis Depay","Netherlands"),
])
print("  Popular Demand Autograph Relics: 6 cards")

make_is("Pristine Autographs", PRISTINE_AUTO_PARS, [
    ("PA-AE","Anthony Elanga","Sweden"),("PA-AF","Ansu Fati","Spain"),("PA-AI","Alexander Isak","Sweden"),("PA-AO","Amadou Onana","Belgium"),("PA-AS","Alan Shearer","England"),("PA-CD","Charles De Ketelaere","Belgium"),("PA-CG","Cody Gakpo","Netherlands"),("PA-CR","Cristiano Ronaldo","Portugal"),("PA-DA","David Alaba","Austria"),("PA-DO","Dani Olmo","Spain"),("PA-DZ","Denis Zakaria","Switzerland"),("PA-EC","Eric Cantona","France"),("PA-EF","Evan Ferguson","Republic of Ireland"),("PA-EH","Erling Haaland","Norway"),("PA-EV","Edwin van der Sar","Netherlands"),("PA-FR","Frank Rijkaard","Netherlands"),("PA-FRA","Fabrizio Ravanelli","Italy"),("PA-GB","Gianluigi Buffon","Italy"),("PA-GR","Gon\u00e7alo Ramos","Portugal"),("PA-HK","Harry Kane","England"),("PA-HL","Henrik Larsson","Sweden"),("PA-HLA","Hugo Larsson","Sweden"),("PA-IC","Iker Casillas","Spain"),("PA-IW","Ian Wright","England"),("PA-JG","Jo\u0161ko Gvardiol","Croatia"),("PA-JM","Jamal Musiala","Germany"),("PA-JMC","James McFadden","Scotland"),("PA-JO","Jorginho","Italy"),("PA-KB","Karim Benzema","France"),("PA-LA","Liel Abada","Israel"),("PA-LE","Luis Enrique","Spain"),("PA-LF","Lu\u00eds Figo","Portugal"),("PA-LM","Luka Modri\u0107","Croatia"),("PA-LO","Lo\u00efs Openda","Belgium"),("PA-LS","Luke Shaw","England"),("PA-MC","Muhammed Cham","Austria"),("PA-MD","Memphis Depay","Netherlands"),("PA-MK","Mateo Kova\u010di\u0107","Croatia"),("PA-MO","Michael Owen","England"),("PA-MR","Micah Richards","England"),("PA-MV","Marco Verratti","Italy"),("PA-MVB","Marco van Basten","Netherlands"),("PA-NA","Nathan Ak\u00e9","Netherlands"),("PA-NO","Noah Okafor","Switzerland"),("PA-NV","Nemanja Vidi\u0107","Serbia"),("PA-OG","Oscar Gloukh","Israel"),("PA-OK","Oliver Kahn","Germany"),("PA-PE","Pedri","Spain"),("PA-PG","Paul Gascoigne","England"),("PA-PN","Pavel Ned\u011bv\u011bd","Czechia"),("PA-RD","Ronald De Boer","Netherlands"),("PA-RK","Robbie Keane","Republic of Ireland"),("PA-RL","Robert Lewandowski","Poland"),("PA-RO","Rodri","Spain"),("PA-RP","Ray Parlour","England"),("PA-SM","Sivert Mannsverk","Norway"),("PA-ST","Sandro Tonali","Italy"),("PA-TM","Thomas M\u00fcller","Germany"),("PA-TW","Timo Werner","Germany"),("PA-XA","Xabi Alonso","Spain"),("PA-YA","Yasin Ayari","Sweden"),("PA-YM","Youssoufa Moukoko","Germany"),("PA-ZB","Zvonimir Boban","Croatia"),("PA-ZZ","Zin\u00e9dine Zidane","France"),
])
print("  Pristine Autographs: 64 cards")

make_is("Pristine Borders Autograph Relics", PB_RELIC_PARS, [
    ("PBR-BF","Bruno Fernandes","Portugal"),("PBR-MD","Memphis Depay","Netherlands"),
])
print("  Pristine Borders Autograph Relics: 2 cards")

make_is("Pristine Borders Autographs", PB_AUTO_PARS, [
    ("PBA-AG","Antoine Griezmann","France"),("PBA-AI","Alexander Isak","Sweden"),("PBA-AO","Amadou Onana","Belgium"),("PBA-AR","Andy Robertson","Scotland"),("PBA-BA","Johan Bakayoko","Belgium"),("PBA-BF","Bruno Fernandes","Portugal"),("PBA-EF","Evan Ferguson","Republic of Ireland"),("PBA-GX","Granit Xhaka","Switzerland"),("PBA-IJ","\u00cdsak Bergmann Johannesso","Iceland"),("PBA-JG","Jo\u0161ko Gvardiol","Croatia"),("PBA-JK","Joshua Kimmich","Germany"),("PBA-JO","Jorginho","Italy"),("PBA-LM","Luka Modri\u0107","Croatia"),("PBA-MO","Martin \u00d8degaard","Norway"),("PBA-MS","Marcel Sabitzer","Austria"),("PBA-NF","Nicol\u00f2 Fagioli","Italy"),("PBA-RH","Rasmus H\u00f8jlund","Denmark"),("PBA-RL","Rafael Le\u00e3o","Portugal"),("PBA-ST","Sandro Tonali","Italy"),("PBA-TM","Thomas M\u00fcller","Germany"),("PBA-YD","Yusuf Demir","Austria"),
])
print("  Pristine Borders Autographs: 21 cards")

make_is("Pristine Nations Patch Autographs", [], [
    ("PNP-BF","Bruno Fernandes","Portugal"),("PNP-MD","Memphis Depay","Netherlands"),
])
print("  Pristine Nations Patch Autographs: 2 cards")

# Dual autographs
is_id = create_insert_set(set_id, "Pristine Pair Dual Autographs")
for pn, pr in DUAL_PARS: create_parallel(is_id, pn, pr)
add_dual_cards(is_id, [
    ("PDA-AI", [("Paul Ince","England"),("Tony Adams","England")]),
    ("PDA-LL", [("Brian Laudrup","Denmark"),("Michael Laudrup","Denmark")]),
    ("PDA-RH", [("Erling Haaland","Norway"),("Cristiano Ronaldo","Portugal")]),
    ("PDA-RK", [("Roy Keane","Republic of Ireland"),("Micah Richards","England")]),
    ("PDA-TI", [("Francesco Totti","Italy"),("Filippo Inzaghi","Italy")]),
])
print("  Pristine Pair Dual Autographs: 5 cards")

make_is("Pristine Prodigies Autographs", PRODIGY_AUTO_PARS, [
    ("PPA-EF","Evan Ferguson","Republic of Ireland"),("PPA-JM","Jamal Musiala","Germany"),("PPA-NW","Nico Williams","Spain"),("PPA-OG","Oscar Gloukh","Israel"),("PPA-RK","Randal Kolo Muani","France"),("PPA-WG","Wilfried Gnonto","Italy"),
])
print("  Pristine Prodigies Autographs: 6 cards")

# ─── INSERT SETS ──────────────────────────────────────────────────────────────

make_is("Inevitable", INSERT_PARS, [
    ("IV-AM","Aleksandar Mitrovi\u0107","Serbia"),("IV-AS","Alan Shearer","England"),("IV-BJ","Brennan Johnson","Wales"),("IV-CR","Cristiano Ronaldo","Portugal"),("IV-EG","Eidur Gudjohnsen","Iceland"),("IV-EH","Erling Haaland","Norway"),("IV-FT","Fernando Torres","Spain"),("IV-FTO","Francesco Totti","Italy"),("IV-GR","Gon\u00e7alo Ramos","Portugal"),("IV-HK","Harry Kane","England"),("IV-HL","Henrik Larsson","Sweden"),("IV-NO","Noah Okafor","Switzerland"),("IV-PK","Patrick Kluivert","Netherlands"),("IV-RH","Rasmus H\u00f8jlund","Denmark"),("IV-RK","Randal Kolo Muani","France"),("IV-RL","Robert Lewandowski","Poland"),("IV-RLE","Rafael Le\u00e3o","Portugal"),("IV-RLU","Romelu Lukaku","Belgium"),("IV-WR","Wayne Rooney","England"),("IV-YM","Youssoufa Moukoko","Germany"),
])
print("  Inevitable: 20 cards")

make_is("Fresh Faces", INSERT_PARS, [
    ("FF-AG","Arda G\u00fcler","T\u00fcrkiye"),("FF-AS","Ant\u00f3nio Silva","Portugal"),("FF-BH","Bilal Hussein","Sweden"),("FF-EF","Evan Ferguson","Republic of Ireland"),("FF-FR","Fabian Rieder","Switzerland"),("FF-GR","Gon\u00e7alo Ramos","Portugal"),("FF-HL","Hugo Larsson","Sweden"),("FF-JJ","Jordan James","Wales"),("FF-NF","Nicol\u00f2 Fagioli","Italy"),("FF-NW","Nico Williams","Spain"),("FF-OB","Ola Brynhildsen","Norway"),("FF-OG","Oscar Gloukh","Israel"),("FF-RK","Randal Kolo Muani","France"),("FF-SM","Sivert Mannsverk","Norway"),("FF-WG","Wilfried Gnonto","Italy"),
])
print("  Fresh Faces: 15 cards")

make_is("Iconic XI", ICONIC_PARS, [
    ("IC-CR","Cristiano Ronaldo","Portugal"),("IC-FB","Franz Beckenbauer","Germany"),("IC-FC","Fabio Cannavaro","Italy"),("IC-GB","Gianluigi Buffon","Italy"),("IC-LM","Luka Modri\u0107","Croatia"),("IC-MD","Marcel Desailly","France"),("IC-MVB","Marco van Basten","Netherlands"),("IC-RK","Roy Keane","Republic of Ireland"),("IC-RKO","Ronald Koeman","Netherlands"),("IC-WR","Wayne Rooney","England"),("IC-ZZ","Zin\u00e9dine Zidane","France"),
])
print("  Iconic XI: 11 cards")

make_is("Marvelous Moments", INSERT_PARS, [
    ("MM-AC","Andreas Christensen","Denmark"),("MM-AI","Andr\u00e9s Iniesta","Spain"),("MM-CR","Cristiano Ronaldo","Portugal"),("MM-FT","Fernando Torres","Spain"),("MM-MVB","Marco van Basten","Netherlands"),("MM-PE","Pedri","Spain"),("MM-PK","Patrick Kluivert","Netherlands"),("MM-PS","Peter Schmeichel","Denmark"),("MM-PSC","Patrik Schick","Czechia"),("MM-RS","Renato Sanches","Portugal"),
])
print("  Marvelous Moments: 10 cards")

make_is("Pristine Borders", INSERT_PARS, [
    ("PB-AG","Antoine Griezmann","France"),("PB-AGU","Arda G\u00fcler","T\u00fcrkiye"),("PB-AI","Alexander Isak","Sweden"),("PB-AM","\u00c1lvaro Morata","Spain"),("PB-AO","Amadou Onana","Belgium"),("PB-AR","Andy Robertson","Scotland"),("PB-BF","Bruno Fernandes","Portugal"),("PB-BS","Benjamin \u0160e\u0161ko","Slovenia"),("PB-DD","Denzel Dumfries","Netherlands"),("PB-DS","Dominik Szoboszlai","Hungary"),("PB-DT","Du\u0161an Tadi\u0107","Serbia"),("PB-EF","Evan Ferguson","Republic of Ireland"),("PB-GA","Gavi","Spain"),("PB-GX","Granit Xhaka","Switzerland"),("PB-HV","Hugo Vetlesen","Norway"),("PB-IJ","\u00cdsak Bergmann Johannesso","Iceland"),("PB-JG","Jo\u0161ko Gvardiol","Croatia"),("PB-KK","Khvicha Kvaratskhelia","Georgia"),("PB-LM","Luka Modri\u0107","Croatia"),("PB-MO","Martin \u00d8degaard","Norway"),("PB-MS","Marcel Sabitzer","Austria"),("PB-PM","Petar Musa","Croatia"),("PB-RH","Rasmus H\u00f8jlund","Denmark"),("PB-RL","Rafael Le\u00e3o","Portugal"),("PB-SM","Sergej Milinkovi\u0107-Savi\u0107","Serbia"),("PB-TC","Thibaut Courtois","Belgium"),("PB-TM","Thomas M\u00fcller","Germany"),("PB-WS","Wojciech Szcz\u0119sny","Poland"),("PB-XS","Xavi Simons","Netherlands"),("PB-YD","Yusuf Demir","Austria"),
])
print("  Pristine Borders: 30 cards")

make_is("Pristine Prodigies", PRODIGY_PARS, [
    ("PP-AS","Ant\u00f3nio Silva","Portugal"),("PP-EF","Evan Ferguson","Republic of Ireland"),("PP-GA","Gavi","Spain"),("PP-JM","Jamal Musiala","Germany"),("PP-NW","Nico Williams","Spain"),("PP-NZ","Nicola Zalewski","Poland"),("PP-OG","Oscar Gloukh","Israel"),("PP-RK","Randal Kolo Muani","France"),("PP-WG","Wilfried Gnonto","Italy"),
])
print("  Pristine Prodigies: 9 cards")

# ─── Compute player stats ─────────────────────────────────────────────────────

print("\nComputing player stats...")
cur.execute("SELECT id FROM players WHERE set_id = ?", (set_id,))
for (pid,) in cur.fetchall():
    cur.execute("SELECT pa.id, pa.insert_set_id FROM player_appearances pa WHERE pa.player_id = ?", (pid,))
    appearances = cur.fetchall()
    is_ids = set(a[1] for a in appearances)
    uc, tpr, o1 = 0, 0, 0
    for _, isid in appearances:
        uc += 1
        cur.execute("SELECT name, print_run FROM parallels WHERE insert_set_id = ?", (isid,))
        for _, pr in cur.fetchall():
            uc += 1
            if pr is not None:
                tpr += pr
                if pr == 1: o1 += 1
    cur.execute("UPDATE players SET unique_cards=?, total_print_run=?, one_of_ones=?, insert_set_count=? WHERE id=?", (uc, tpr, o1, len(is_ids), pid))

conn.commit()

# Verify
cur.execute("SELECT COUNT(*) FROM players WHERE set_id = ?", (set_id,)); tp = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id = ?", (set_id,)); ti = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM player_appearances pa JOIN players p ON p.id=pa.player_id WHERE p.set_id=?", (set_id,)); ta = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM appearance_co_players ac JOIN player_appearances pa ON pa.id=ac.appearance_id JOIN players p ON p.id=pa.player_id WHERE p.set_id=?", (set_id,)); tc = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM parallels par JOIN insert_sets i ON i.id=par.insert_set_id WHERE i.set_id=?", (set_id,)); tpar = cur.fetchone()[0]

print(f"\n{'='*50}")
print(f"Set ID:            {set_id}")
print(f"Players:           {tp}")
print(f"Insert Sets:       {ti}")
print(f"Appearances:       {ta}")
print(f"Co-player links:   {tc}")
print(f"Parallel types:    {tpar}")
print(f"{'='*50}")
conn.close()
print("\nDone!")
