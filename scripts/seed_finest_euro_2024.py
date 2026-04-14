"""
Seed: 2023 Topps Finest Road to UEFA EURO 2024 (update existing stub ID 297)
Usage: python3 scripts/seed_finest_euro_2024.py
"""
import sqlite3, json, os, re, unicodedata

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA foreign_keys=ON")
cur = conn.cursor()

SET_ID = 297

# Update the stub
def slugify(t):
    s = t.lower()
    s = unicodedata.normalize("NFD", s)
    s = re.sub(r"[\u0300-\u036f]", "", s)
    s = re.sub(r"[^a-z0-9-]+", "-", s).strip("-")
    s = re.sub(r"-+", "-", s)
    return s

box_config = {"hobby":{"cards_per_pack":5,"packs_per_box":12,"boxes_per_case":8,"autos_per_box":2,"euro_masters_per_box":1,"finest_debutants_per_box":2,"prized_footballers_per_box":4,"notes":"Two 6-pack mini boxes per hobby box"}}

pack_odds = {"hobby":{"Refractor":"1:3","Blue Aqua Vaporwave Refractor":"1:12","Blue Refractor":"1:19","Green Speckle Refractor":"1:23","Green Refractor":"1:28","Lava Green Refractor":"1:28","Rose Gold Refractor":"1:37","Gold Refractor":"1:56","Rose Gold Mini-Diamond Refractor":"1:56","Orange Refractor":"1:111","Red Black Vaporwave Refractor":"1:276","Red Refractor":"1:550","Purple Pink Vaporwave Refractor":"1:915","Superfractor":"1:2,716","Base Autographs":"1:11","Base Autographs Blue Refractor":"1:73","Base Autographs Neon Green Refractor":"1:105","Base Autographs Neon Green Wave Refractor":"1:105","Base Autographs Fuchsia Lava Refractor":"1:139","Base Autographs Gold Refractor":"1:200","Base Autographs Orange Refractor":"1:400","Base Autographs Orange Wave Refractor":"1:385","Base Autographs Red Refractor":"1:1,909","Base Autographs Red Wave Refractor":"1:1,843","Base Autographs Superfractor":"1:8,782","Euro Masters Autographs":"1:1,076","Euro Masters Autographs Superfractor":"1:52,688","Finest Debutants Autographs":"1:338","Finest Debutants Autographs Superfractor":"1:52,688","Finest Dual Autographs":"1:309","Finest Dual Autographs Gold Refractor":"1:1,076","Finest Dual Autographs Orange Refractor":"1:2,142","Finest Dual Autographs Orange Wave Refractor":"1:2,142","Finest Dual Autographs Red Refractor":"1:10,538","Finest Dual Autographs Red Wave Refractor":"1:10,538","Finest Dual Autographs Superfractor":"1:52,688","The Man Autographs":"1:338","The Man Autographs Superfractor":"1:52,688","Prized Footballers Autographs":"1:68","Prized Footballers Autographs Red Refractor":"1:3,560","Prized Footballers Autographs Superfractor":"1:17,563","Prized Footballers Fusion Rose Gold Gold Variations Autographs":"1:52,688","Euro Masters":"1:12","Euro Masters Rose Gold Refractor":"1:367","Euro Masters Gold Refractor":"1:550","Euro Masters Orange Refractor":"1:1,098","Euro Masters Red Refractor":"1:5,377","Euro Masters Superfractor":"1:26,344","Finest Debutants":"1:6","Finest Debutants Rose Gold Refractor":"1:367","Finest Debutants Gold Refractor":"1:550","Finest Debutants Orange Refractor":"1:1,098","Finest Debutants Red Refractor":"1:5,377","Finest Debutants Superfractor":"1:26,344","Giants of Europe":"1:92","The Man":"1:49","The Man Rose Gold Refractor":"1:367","The Man Gold Refractor":"1:550","The Man Orange Refractor":"1:1,098","The Man Red Refractor":"1:5,377","The Man Superfractor":"1:26,344","Prized Footballers":"1:3","Prized Footballers Rose Gold Refractor":"1:245","Prized Footballers Gold Refractor":"1:367","Prized Footballers Orange Refractor":"1:732","Prized Footballers Red Refractor":"1:3,609","Prized Footballers Superfractor":"1:17,563","Prized Footballers Fusion Variations Yellow Red":"1:283","Prized Footballers Fusion Variations Blue Red":"1:367","Prized Footballers Fusion Variations Orange Red":"1:459","Prized Footballers Fusion Variations Green Red":"1:612","Prized Footballers Fusion Variations Pink Red":"1:915","Prized Footballers Fusion Variations Red Red":"1:3,609","Prized Footballers Fusion Variations Black Gold":"1:17,563","Prized Footballers Fusion Variations Rose Gold Gold":"1:17,563"}}

new_name = "2023 Topps Finest Road to UEFA EURO 2024"
new_slug = slugify(new_name)

cur.execute("UPDATE sets SET name=?, sport=?, season=?, league=?, tier=?, release_date=?, sample_image_url=?, box_config=?, pack_odds=?, slug=? WHERE id=?",
    (new_name, "Soccer", "2023", "UEFA", "Standard", "2024-03-22", "/sets/2023-topps-finest-uefa-road-to-euro-2024.jpg", json.dumps(box_config), json.dumps(pack_odds), new_slug, SET_ID))
print(f"Updated set {SET_ID}: {new_name}")

# Helpers
def gop(name):
    cur.execute("SELECT id FROM players WHERE set_id=? AND name=?", (SET_ID, name))
    r = cur.fetchone()
    if r: return r[0]
    s = slugify(name)
    cur.execute("INSERT INTO players (set_id,name,slug,unique_cards,total_print_run,one_of_ones,insert_set_count) VALUES (?,?,?,0,0,0,0)", (SET_ID, name, s))
    return cur.lastrowid

def cis(name):
    cur.execute("INSERT INTO insert_sets (set_id,name) VALUES (?,?)", (SET_ID, name))
    return cur.lastrowid

def cp(is_id, name, pr):
    cur.execute("INSERT INTO parallels (insert_set_id,name,print_run) VALUES (?,?,?)", (is_id, name, pr))

def ca(pid, is_id, cn, team=None):
    cur.execute("INSERT INTO player_appearances (player_id,insert_set_id,card_number,is_rookie,team) VALUES (?,?,?,0,?)", (pid, is_id, cn, team))
    return cur.lastrowid

def cco(aid, cpid):
    cur.execute("INSERT INTO appearance_co_players (appearance_id,co_player_id) VALUES (?,?)", (aid, cpid))

def add(is_id, cards):
    for cn,n,t in cards:
        ca(gop(n), is_id, cn, t)

def add_dual(is_id, cards):
    for cn, pairs in cards:
        aids, pids = [], []
        for n, t in pairs:
            pid = gop(n)
            aid = ca(pid, is_id, cn, t)
            aids.append(aid); pids.append(pid)
        for i, aid in enumerate(aids):
            for j, cpid in enumerate(pids):
                if i != j: cco(aid, cpid)

def mis(name, pars, cards, dual=False):
    is_id = cis(name)
    for pn, pr in pars: cp(is_id, pn, pr)
    if dual: add_dual(is_id, cards)
    else: add(is_id, cards)
    return is_id

# Parallels
BASE_P = [("Refractor",None),("Blue Aqua Vaporwave Refractor",250),("Blue Refractor",150),("Green Speckle Refractor",125),("Green Refractor",99),("Lava Green Refractor",99),("Rose Gold Refractor",75),("Gold Refractor",50),("Rose Gold Mini-Diamond Refractor",50),("Orange Refractor",25),("Red Black Vaporwave Refractor",10),("Red Refractor",5),("Purple Pink Vaporwave Refractor",3),("Superfractor",1)]
BA_P = [("Blue Refractor",150),("Neon Green Refractor",99),("Neon Green Wave Refractor",99),("Fuchsia Lava Refractor",75),("Gold Refractor",50),("Orange Refractor",25),("Orange Wave Refractor",25),("Red Refractor",5),("Red Wave Refractor",5),("Superfractor",1)]
EMA_P = [("Superfractor",1)]
FDA_P = [("Superfractor",1)]
FDUAL_P = [("Gold Refractor",50),("Orange Refractor",25),("Orange Wave Refractor",25),("Red Refractor",5),("Red Wave Refractor",5),("Superfractor",1)]
TMA_P = [("Superfractor",1)]
PFA_P = [("Red Refractor",5),("Superfractor",1)]
INSERT_P = [("Rose Gold Refractor",75),("Gold Refractor",50),("Orange Refractor",25),("Red Refractor",5),("Superfractor",1)]
PFV_P = [("Blue Red",50),("Orange Red",None),("Green Red",30),("Pink Red",None),("Red Red",5),("Black Gold",None),("Rose Gold Gold",1)]

# BASE (100)
mis("Base", BASE_P, [
("1","David Alaba","Austria"),("2","Yusuf Demir","Austria"),("3","Patrick Wimmer","Austria"),("4","Marcel Sabitzer","Austria"),("5","Romelu Lukaku","Belgium"),("6","Kevin De Bruyne","Belgium"),("7","Thibaut Courtois","Belgium"),("8","Charles De Ketelaere","Belgium"),("9","Youri Tielemans","Belgium"),("10","Johan Bakayoko","Belgium"),("11","Lo\u00efs Openda","Belgium"),("12","Mateo Kova\u010di\u0107","Croatia"),("13","Josip \u0160utalo","Croatia"),("14","Luka Modri\u0107","Croatia"),("15","Petar Musa","Croatia"),("16","Christian Eriksen","Denmark"),("17","Pierre-Emile H\u00f8jbjerg","Denmark"),("18","Rasmus H\u00f8jlund","Denmark"),("19","Mikkel Damsgaard","Denmark"),("20","Elias Jelert","Denmark"),
("21","Jack Grealish","England"),("22","Harry Kane","England"),("23","Mason Mount","England"),("24","Trent Alexander-Arnold","England"),("25","Luke Shaw","England"),("26","Phil Foden","England"),("27","Eduardo Camavinga","France"),("28","Antoine Griezmann","France"),("29","Karim Benzema","France"),("30","Randal Kolo Muani","France"),("31","Khvicha Kvaratskhelia","Georgia"),("32","Zuriko Davitashvili","Georgia"),("33","Giorgi Tsitaishvili","Georgia"),("34","Leo \u00d8stig\u00e5rd","Norway"),("35","Luka Jovi\u0107","Serbia"),("36","Thomas M\u00fcller","Germany"),("37","Jamal Musiala","Germany"),("38","Youssoufa Moukoko","Germany"),("39","Timo Werner","Germany"),("40","Doron Leidner","Israel"),
("41","Oscar Gloukh","Israel"),("42","Manor Solomon","Israel"),("43","Sandro Tonali","Italy"),("44","Wilfried Gnonto","Italy"),("45","Seamus Coleman","Republic of Ireland"),("46","Fabio Miretti","Italy"),("47","Gianluigi Donnarumma","Italy"),("48","Denzel Dumfries","Netherlands"),("49","Cody Gakpo","Netherlands"),("50","Xavi Simons","Netherlands"),("51","Frenkie de Jong","Netherlands"),("52","Memphis Depay","Netherlands"),("53","Matthijs de Ligt","Netherlands"),("54","Virgil van Dijk","Netherlands"),("55","Erling Haaland","Norway"),("56","Martin \u00d8degaard","Norway"),("57","Ola Brynhildsen","Norway"),("58","Sivert Mannsverk","Norway"),("59","Robert Lewandowski","Poland"),("60","Nicola Zalewski","Poland"),
("61","Arkadiusz Milik","Poland"),("62","Sebastian Szyma\u0144ski","Poland"),("63","Cristiano Ronaldo","Portugal"),("64","Vitinha","Portugal"),("65","Bruno Fernandes","Portugal"),("66","Jo\u00e3o Cancelo","Portugal"),("67","Jo\u00e3o F\u00e9lix","Portugal"),("68","Ant\u00f3nio Silva","Portugal"),("69","Gon\u00e7alo Ramos","Portugal"),("70","Rafael Le\u00e3o","Portugal"),("71","Aleksandar Mitrovi\u0107","Serbia"),("72","Du\u0161an Vlahovi\u0107","Serbia"),("73","Du\u0161an Tadi\u0107","Serbia"),("74","Sergej Milinkovi\u0107-Savi\u0107","Serbia"),("75","Nico Williams","Spain"),("76","Ansu Fati","Spain"),("77","Gavi","Spain"),("78","Alejandro Balde","Spain"),("79","Pedri","Spain"),("80","Aymeric Laporte","Spain"),
("81","Sergio Busquets","Spain"),("82","Alexander Isak","Sweden"),("83","Yasin Ayari","Sweden"),("84","Dejan Kulusevski","Sweden"),("85","Hugo Larsson","Sweden"),("86","Omar Faraj","Sweden"),("87","Granit Xhaka","Switzerland"),("88","Ardon Jashari","Switzerland"),("89","Noah Okafor","Switzerland"),("90","Fabian Rieder","Switzerland"),("91","Hakan \u00c7alhano\u011flu","T\u00fcrkiye"),("92","Arda G\u00fcler","T\u00fcrkiye"),("93","Emirhan \u0130lkhan","T\u00fcrkiye"),("94","Cengiz \u00dcnder","T\u00fcrkiye"),("95","Mykhailo Mudryk","Ukraine"),("96","Oleksandr Zinchenko","Ukraine"),("97","Ilya Zabarnyi","Ukraine"),("98","Evan Ferguson","Republic of Ireland"),("99","Gavin Bazunu","Republic of Ireland"),("100","Mikey Johnston","Republic of Ireland"),
])
print("  Base: 100 cards")

# AUTOGRAPH SETS
mis("Base Autographs", BA_P, [
("BCA-AG","Arda G\u00fcler","T\u00fcrkiye"),("BCA-BA","Johan Bakayoko","Belgium"),("BCA-CG","Cody Gakpo","Netherlands"),("BCA-CR","Cristiano Ronaldo","Portugal"),("BCA-DK","Dejan Kulusevski","Sweden"),("BCA-DV","Dante Vanzeir","Belgium"),("BCA-EH","Erling Haaland","Norway"),("BCA-GD","Gianluigi Donnarumma","Italy"),("BCA-GX","Granit Xhaka","Switzerland"),("BCA-HL","Hugo Larsson","Sweden"),("BCA-IJ","\u00cdsak Bergmann J\u00f3hannesson","Iceland"),("BCA-JF","Jo\u00e3o F\u00e9lix","Portugal"),("BCA-JG","Jack Grealish","England"),("BCA-JM","Jamal Musiala","Germany"),("BCA-KKO","Kacper Koz\u0142owski","Poland"),("BCA-KM","Randal Kolo Muani","France"),("BCA-LO","Lo\u00efs Openda","Belgium"),("BCA-MM","Mykhailo Mudryk","Ukraine"),("BCA-MN","Matheus Nunes","Portugal"),("BCA-NW","Nico Williams","Spain"),("BCA-OB","Ola Brynhildsen","Norway"),("BCA-OC","Oscar Gloukh","Israel"),("BCA-RH","Rasmus H\u00f8jlund","Denmark"),("BCA-SB","Sven Botman","Netherlands"),("BCA-ST","Sandro Tonali","Italy"),("BCA-VVD","Virgil van Dijk","Netherlands"),("BCA-XV","Xaver Schlager","Austria"),("BCA-YD","Yusuf Demir","Austria"),("BCA-YM","Youssoufa Moukoko","Germany"),
])
print("  Base Autographs: 29 cards")

mis("Euro Masters Autographs", EMA_P, [
("EM-AS","Alan Shearer","England"),("EM-DS","David Seaman","England"),("EM-FT","Francesco Totti","Italy"),("EM-JB","John Barnes","England"),("EM-TA","Tony Adams","England"),("EM-TM","Thomas M\u00fcller","Germany"),("EM-ZZ","Zin\u00e9dine Zidane","France"),
])
print("  Euro Masters Autographs: 7 cards")

mis("Finest Debutants Autographs", FDA_P, [
("FD-HL","Hugo Larsson","Sweden"),("FD-JB","Johan Bakayoko","Belgium"),("FD-NW","Nico Williams","Spain"),("FD-OB","Ola Brynhildsen","Norway"),("FD-OG","Oscar Gloukh","Israel"),
])
print("  Finest Debutants Autographs: 5 cards")

is_id = cis("Finest Dual Autographs")
for pn,pr in FDUAL_P: cp(is_id, pn, pr)
add_dual(is_id, [
    ("FDA-HR",[("Erling Haaland","Norway"),("Cristiano Ronaldo","Portugal")]),
    ("FDA-KL",[("Henrik Larsson","Sweden"),("Patrick Kluivert","Netherlands")]),
    ("FDA-MS",[("Lothar Matth\u00e4us","Germany"),("Matthias Sammer","Germany")]),
    ("FDA-SB",[("Gianluigi Buffon","Italy"),("Peter Schmeichel","Denmark")]),
    ("FDA-VT",[("Nemanja Vidi\u0107","Serbia"),("John Terry","England")]),
])
print("  Finest Dual Autographs: 5 cards")

mis("The Man Autographs", TMA_P, [
("TM-BF","Bruno Fernandes","Portugal"),("TM-KB","Karim Benzema","France"),("TM-MO","Martin \u00d8degaard","Norway"),("TM-RL","Rafael Le\u00e3o","Portugal"),
])
print("  The Man Autographs: 4 cards")

mis("Prized Footballers Autographs", PFA_P, [
("PF-AG","Antoine Griezmann","France"),("PF-CG","Cody Gakpo","Netherlands"),("PF-CR","Cristiano Ronaldo","Portugal"),("PF-EH","Erling Haaland","Norway"),("PF-HK","Harry Kane","England"),("PF-JM","Jamal Musiala","Germany"),("PF-LM","Luka Modri\u0107","Croatia"),("PF-MM","Mykhailo Mudryk","Ukraine"),("PF-PE","Pedri","Spain"),("PF-RL","Robert Lewandowski","Poland"),
])
print("  Prized Footballers Autographs: 10 cards")

# All /1
is_id = cis("Prized Footballers Fusion Rose Gold Gold Variations Autographs")
cp(is_id, "Base /1", 1)
add(is_id, [
("PFAV-AG","Antoine Griezmann","France"),("PFAV-CR","Cristiano Ronaldo","Portugal"),("PFAV-HK","Harry Kane","England"),("PFAV-KD","Kevin De Bruyne","Belgium"),("PFAV-LM","Luka Modri\u0107","Croatia"),
])
print("  Prized Footballers Fusion Rose Gold Gold Variations Autographs: 5 cards")

# INSERT SETS
mis("Euro Masters", INSERT_P, [
("EM-AS","Alan Shearer","England"),("EM-CR","Cristiano Ronaldo","Portugal"),("EM-DS","David Seaman","England"),("EM-FT","Francesco Totti","Italy"),("EM-JB","John Barnes","England"),("EM-PK","Patrick Kluivert","Netherlands"),("EM-TA","Tony Adams","England"),("EM-TM","Thomas M\u00fcller","Germany"),("EM-XA","Xavi","Spain"),("EM-ZZ","Zin\u00e9dine Zidane","France"),
])
print("  Euro Masters: 10 cards")

mis("Finest Debutants", INSERT_P, [
("FD-AG","Arda G\u00fcler","T\u00fcrkiye"),("FD-EF","Evan Ferguson","Republic of Ireland"),("FD-EJ","Elias Jelert","Denmark"),("FD-HL","Hugo Larsson","Sweden"),("FD-JB","Johan Bakayoko","Belgium"),("FD-NW","Nico Williams","Spain"),("FD-OB","Ola Brynhildsen","Norway"),("FD-OG","Oscar Gloukh","Israel"),("FD-RH","Rasmus H\u00f8jlund","Denmark"),("FD-VI","Vitinha","Portugal"),
])
print("  Finest Debutants: 10 cards")

mis("Giants of Europe", [], [
("GE-CE","Christian Eriksen","Denmark"),("GE-CG","Cody Gakpo","Netherlands"),("GE-DV","Du\u0161an Vlahovi\u0107","Serbia"),("GE-EH","Erling Haaland","Norway"),("GE-GR","Gon\u00e7alo Ramos","Portugal"),("GE-GX","Granit Xhaka","Switzerland"),("GE-JG","Jo\u0161ko Gvardiol","Croatia"),("GE-MM","Mykhailo Mudryk","Ukraine"),("GE-SB","Sergio Busquets","Spain"),("GE-TC","Thibaut Courtois","Belgium"),
])
print("  Giants of Europe: 10 cards")

mis("The Man", INSERT_P, [
("TM-AI","Andr\u00e9s Iniesta","Spain"),("TM-AM","Aleksandar Mitrovi\u0107","Serbia"),("TM-AP","Andrea Pirlo","Italy"),("TM-BF","Bruno Fernandes","Portugal"),("TM-FD","Frenkie de Jong","Netherlands"),("TM-JM","Jamal Musiala","Germany"),("TM-KB","Karim Benzema","France"),("TM-MO","Martin \u00d8degaard","Norway"),("TM-RL","Rafael Le\u00e3o","Portugal"),("TM-ZI","Zlatan Ibrahimovi\u0107","Sweden"),
])
print("  The Man: 10 cards")

mis("Prized Footballers", INSERT_P, [
("PF-AG","Antoine Griezmann","France"),("PF-AI","Alexander Isak","Sweden"),("PF-CG","Cody Gakpo","Netherlands"),("PF-CR","Cristiano Ronaldo","Portugal"),("PF-EH","Erling Haaland","Norway"),("PF-GA","Gavi","Spain"),("PF-GR","Gon\u00e7alo Ramos","Portugal"),("PF-HK","Harry Kane","England"),("PF-JM","Jamal Musiala","Germany"),("PF-KD","Kevin De Bruyne","Belgium"),("PF-KK","Khvicha Kvaratskhelia","Georgia"),("PF-LM","Luka Modri\u0107","Croatia"),("PF-MM","Mykhailo Mudryk","Ukraine"),("PF-PE","Pedri","Spain"),("PF-RL","Robert Lewandowski","Poland"),
])
print("  Prized Footballers: 15 cards")

mis("Prized Footballers Fusion Variations", PFV_P, [
("PFV-AG","Antoine Griezmann","France"),("PFV-AI","Alexander Isak","Sweden"),("PFV-CG","Cody Gakpo","Netherlands"),("PFV-CR","Cristiano Ronaldo","Portugal"),("PFV-EH","Erling Haaland","Norway"),("PFV-GA","Gavi","Spain"),("PFV-GR","Gon\u00e7alo Ramos","Portugal"),("PFV-HK","Harry Kane","England"),("PFV-JM","Jamal Musiala","Germany"),("PFV-KD","Kevin De Bruyne","Belgium"),("PFV-KK","Khvicha Kvaratskhelia","Georgia"),("PFV-LM","Luka Modri\u0107","Croatia"),("PFV-MM","Mykhailo Mudryk","Ukraine"),("PFV-PE","Pedri","Spain"),("PFV-RL","Robert Lewandowski","Poland"),
])
print("  Prized Footballers Fusion Variations: 15 cards")

# Compute stats
print("\nComputing player stats...")
cur.execute("SELECT id FROM players WHERE set_id=?", (SET_ID,))
for (pid,) in cur.fetchall():
    cur.execute("SELECT pa.id, pa.insert_set_id FROM player_appearances pa WHERE pa.player_id=?", (pid,))
    apps = cur.fetchall()
    is_ids = set(a[1] for a in apps)
    uc, tpr, o1 = 0, 0, 0
    for _, isid in apps:
        uc += 1
        cur.execute("SELECT name, print_run FROM parallels WHERE insert_set_id=?", (isid,))
        for _, pr in cur.fetchall():
            uc += 1
            if pr is not None:
                tpr += pr
                if pr == 1: o1 += 1
    cur.execute("UPDATE players SET unique_cards=?, total_print_run=?, one_of_ones=?, insert_set_count=? WHERE id=?", (uc, tpr, o1, len(is_ids), pid))

conn.commit()

cur.execute("SELECT COUNT(*) FROM players WHERE set_id=?", (SET_ID,)); tp=cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id=?", (SET_ID,)); ti=cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM player_appearances pa JOIN players p ON p.id=pa.player_id WHERE p.set_id=?", (SET_ID,)); ta=cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM appearance_co_players ac JOIN player_appearances pa ON pa.id=ac.appearance_id JOIN players p ON p.id=pa.player_id WHERE p.set_id=?", (SET_ID,)); tc=cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM parallels par JOIN insert_sets i ON i.id=par.insert_set_id WHERE i.set_id=?", (SET_ID,)); tpar=cur.fetchone()[0]

print(f"\n{'='*50}")
print(f"Set ID:            {SET_ID}")
print(f"Players:           {tp}")
print(f"Insert Sets:       {ti}")
print(f"Appearances:       {ta}")
print(f"Co-player links:   {tc}")
print(f"Parallel types:    {tpar}")
print(f"{'='*50}")
conn.close()
print("\nDone!")
