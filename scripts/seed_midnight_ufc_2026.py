"""
Seed script: 2026 Topps Midnight UFC
Usage: python3 scripts/seed_midnight_ufc_2026.py
"""
import sqlite3, json, os, re

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA foreign_keys=ON")
cur = conn.cursor()

def get_or_create_player(set_id, name):
    cur.execute("SELECT id FROM players WHERE set_id = ? AND name = ?", (set_id, name))
    row = cur.fetchone()
    if row: return row[0]
    cur.execute("INSERT INTO players (set_id, name, unique_cards, total_print_run, one_of_ones, insert_set_count) VALUES (?, ?, 0, 0, 0, 0)", (set_id, name))
    return cur.lastrowid

def create_insert_set(set_id, name):
    cur.execute("INSERT INTO insert_sets (set_id, name) VALUES (?, ?)", (set_id, name))
    return cur.lastrowid

def create_parallel(insert_set_id, name, print_run):
    cur.execute("INSERT INTO parallels (insert_set_id, name, print_run) VALUES (?, ?, ?)", (insert_set_id, name, print_run))

def create_appearance(player_id, insert_set_id, card_number, is_rookie=False, team=None):
    cur.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)", (player_id, insert_set_id, card_number, int(is_rookie), team))
    return cur.lastrowid

def create_co_player(appearance_id, co_player_id):
    cur.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (appearance_id, co_player_id))

def add_cards(is_id, cards):
    for num, name, rookie in cards:
        pid = get_or_create_player(set_id, name)
        create_appearance(pid, is_id, num, rookie)

def add_multi_cards(is_id, cards):
    for num, players_list in cards:
        app_ids, player_ids = [], []
        for name in players_list:
            pid = get_or_create_player(set_id, name)
            app_id = create_appearance(pid, is_id, num, False)
            app_ids.append(app_id)
            player_ids.append(pid)
        for i, app_id in enumerate(app_ids):
            for j, other_pid in enumerate(player_ids):
                if i != j: create_co_player(app_id, other_pid)

def slugify(text):
    s = text.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_]+', '-', s)
    return re.sub(r'-+', '-', s).strip('-')

# ─── Check if set exists ──────────────────────────────────────────
SET_NAME = "2026 Topps Midnight UFC"
cur.execute("SELECT id FROM sets WHERE name = ?", (SET_NAME,))
if cur.fetchone():
    print(f"Set '{SET_NAME}' already exists. Aborting.")
    conn.close()
    exit(1)

# ─── Create set ───────────────────────────────────────────────────
box_config = {
    "hobby": {
        "cards_per_pack": 7,
        "packs_per_box": 1,
        "boxes_per_case": 8,
        "autos_per_box": 3,
    }
}

cur.execute(
    "INSERT INTO sets (name, sport, season, league, tier, sample_image_url, box_config, release_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    (SET_NAME, "MMA", "2026", "UFC", "Standard", "/sets/2026-topps-midnight-ufc.jpg", json.dumps(box_config), "2026-05-22"),
)
set_id = cur.lastrowid
cur.execute("UPDATE sets SET slug = ? WHERE id = ?", ("2026-topps-midnight-ufc", set_id))
print(f"Created set '{SET_NAME}' with id {set_id}")

# ─── RC flag helper ───────────────────────────────────────────────
RC = True
NR = False

# ─── BASE SET ─────────────────────────────────────────────────────
base_is = create_insert_set(set_id, "Base Set")
base = [
    ("1","Ilia Topuria",NR),("2","Fatima Kline",RC),("3","Anderson Silva",NR),("4","Dione Barbosa",RC),("5","Sean O'Malley",NR),("6","MarQuel Mederos",RC),("7","Shi Ming",RC),("8","Khabib Nurmagomedov",NR),("9","Carlos Leal",RC),("10","Tom Aspinall",NR),
    ("11","Natalia Cristina da Silva",NR),("12","Felipe Lima",RC),("13","Arman Tsarukyan",NR),("14","Chang Ho Lee",RC),("15","Virna Jandiroba",NR),("16","Rei Tsuruya",RC),("17","Sean Brady",NR),("18","Kaue Fernandes",RC),("19","Quillan Salkilld",RC),("20","Alexander Volkanovski",NR),
    ("21","Hyder Amil",RC),("22","Nassourdine Imavov",NR),("23","Kody Steele",RC),("24","Gabriel Santos",RC),("25","Magomed Ankalaev",NR),("26","Mingyang Zhang",RC),("27","Julianna Peña",NR),("28","Mario Pinto",RC),("29","Marco Silva",RC),("30","Joshua Van",NR),
    ("31","Jaqueline Amorim",RC),("32","Jiri Prochazka",NR),("33","Zhu Rong",RC),("34","JJ Aldrich",RC),("35","Jon Jones",NR),("36","Max Holloway",NR),("37","Oumar Sy",RC),("38","Alexander Volkov",NR),("39","Ramazan Temirov",RC),("40","Diego Lopes",NR),
    ("41","Aleksandre Topuria",RC),("42","David Onama",RC),("43","Charles Oliveira",NR),("44","Mansur Abdul-Malik",RC),("45","Paddy Pimblett",NR),("46","Youssef Zalal",RC),("47","Sean Strickland",NR),("48","Navajo Stirling",RC),("49","Austin Vanderford",RC),("50","Conor McGregor",NR),
    ("51","Oban Elliott",RC),("52","Manon Fiorot",NR),("53","Islam Dulatov",RC),("54","Nursulton Ruziboev",RC),("55","Khamzat Chimaev",NR),("56","Chris Padilla",RC),("57","Bruna Brasil",RC),("58","Alex Pereira",NR),("59","Torrez Finney",RC),("60","Kayla Harrison",NR),
    ("61","Andre Lima",RC),("62","Tatiana Suarez",NR),("63","Gautier Ateba",RC),("64","Tom Nolan",RC),("65","Ciryl Gane",NR),("66","Seok Hyeon Ko",RC),("67","Jacqueline Cavalcanti",RC),("68","Dricus Du Plessis",NR),("69","Daniel Santos",RC),("70","Valentina Shevchenko",NR),
    ("71","Alexia Thainara",RC),("72","Brandon Moreno",NR),("73","Tallison Teixeira",RC),("74","Patrick Mix",RC),("75","Jack Della Maddalena",NR),("76","Michael Parkin",RC),("77","Umar Nurmagomedov",NR),("78","Wang Cong",RC),("79","Malcolm Wellmaker",RC),("80","Alexandre Pantoja",NR),
    ("81","Ibo Aslan",RC),("82","Belal Muhammad",NR),("83","JeongYeong Lee",RC),("84","Clayton Carpenter",RC),("85","Dustin Poirier",NR),("86","Michael Aswell",RC),("87","Elijah Smith",RC),("88","Islam Makhachev",NR),("89","Patricio Freire",RC),("90","Zhang Weili",NR),
    ("91","Rafael Estevam",RC),("92","Raquel Pennington",NR),("93","Nasrat Haqparast",RC),("94","Amanda Nunes",NR),("95","Joo Sang Yoo",RC),("96","Lone'er Kavanagh",RC),("97","Movsar Evloev",NR),("98","Andreas Gustafsson",RC),("99","Aaron Pico",RC),("100","Merab Dvalishvili",NR),
]
add_cards(base_is, base)
print(f"  Base Set: {len(base)} cards")

# ─── NIGHT WATCH ──────────────────────────────────────────────────
nw_is = create_insert_set(set_id, "Night Watch")
nw = [
    ("PC-1","Max Holloway",NR),("PC-2","Islam Makhachev",NR),("PC-3","Julianna Peña",NR),("PC-4","Yair Rodríguez",NR),("PC-5","Conor McGregor",NR),
    ("PC-6","Charles Oliveira",NR),("PC-7","Valentina Shevchenko",NR),("PC-8","Jiri Prochazka",NR),("PC-9","Magomed Ankalaev",NR),("PC-10","Kayla Harrison",NR),
    ("PC-11","Youssef Zalal",RC),("PC-12","Ian Machado Garry",NR),("PC-13","Sean Strickland",NR),("PC-14","Michael Parkin",RC),("PC-15","Movsar Evloev",NR),
    ("PC-16","Khabib Nurmagomedov",NR),("PC-17","Wang Cong",RC),("PC-18","Michael Page",NR),("PC-19","Diego Lopes",NR),("PC-20","Jacqueline Cavalcanti",RC),
    ("PC-21","Yadong Song",NR),("PC-22","Ilia Topuria",NR),("PC-23","Robert Whittaker",NR),("PC-24","Nassourdine Imavov",NR),("PC-25","Alex Pereira",NR),
]
add_cards(nw_is, nw)
print(f"  Night Watch: {len(nw)} cards")

# ─── ZERO HOUR ────────────────────────────────────────────────────
zh_is = create_insert_set(set_id, "Zero Hour")
zh = [
    ("ZH-1","Tom Aspinall",NR),("ZH-2","Colby Covington",NR),("ZH-3","Sean O'Malley",NR),("ZH-4","Jon Jones",NR),("ZH-5","Valentina Shevchenko",NR),
    ("ZH-6","Natalia Cristina da Silva",NR),("ZH-7","Khamzat Chimaev",NR),("ZH-8","Israel Adesanya",NR),("ZH-9","Oumar Sy",RC),("ZH-10","Merab Dvalishvili",NR),
    ("ZH-11","Alexander Volkanovski",NR),("ZH-12","Paddy Pimblett",NR),("ZH-13","Zhang Weili",NR),("ZH-14","Patricio Freire",RC),("ZH-15","Jamahal Hill",NR),
    ("ZH-16","Umar Nurmagomedov",NR),("ZH-17","Alexandre Pantoja",NR),("ZH-18","Jack Della Maddalena",NR),("ZH-19","Manel Kape",NR),("ZH-20","Ramazan Temirov",RC),
]
add_cards(zh_is, zh)
print(f"  Zero Hour: {len(zh)} cards")

# ─── CELESTIAL COMBOS (dual cards) ───────────────────────────────
cc_is = create_insert_set(set_id, "Celestial Combos")
cc = [
    ("CC-1",["Sean O'Malley","Merab Dvalishvili"]),("CC-2",["Valentina Shevchenko","Zhang Weili"]),
    ("CC-3",["Jack Della Maddalena","Islam Makhachev"]),("CC-4",["Charles Oliveira","Ilia Topuria"]),
    ("CC-5",["Alexandre Pantoja","Joshua Van"]),("CC-6",["Amanda Nunes","Kayla Harrison"]),
    ("CC-7",["Magomed Ankalaev","Alex Pereira"]),("CC-8",["Dricus Du Plessis","Khamzat Chimaev"]),
    ("CC-9",["Tom Aspinall","Ciryl Gane"]),("CC-10",["Dustin Poirier","Conor McGregor"]),
]
add_multi_cards(cc_is, cc)
print(f"  Celestial Combos: {len(cc)} cards")

# ─── LUNAR APEX ───────────────────────────────────────────────────
la_is = create_insert_set(set_id, "Lunar Apex")
la = [
    ("LA-1","Khabib Nurmagomedov",NR),("LA-2","Charles Oliveira",NR),("LA-3","Jean Silva",NR),("LA-4","Reinier De Ridder",NR),("LA-5","Merab Dvalishvili",NR),
    ("LA-6","Georges St-Pierre",NR),("LA-7","Benoit Saint Denis",NR),("LA-8","Sean Strickland",NR),("LA-9","Raul Rosas",NR),("LA-10","Sharabutdin Magomedov",NR),
    ("LA-11","Kayla Harrison",NR),("LA-12","Magomed Ankalaev",NR),("LA-13","Robert Whittaker",NR),("LA-14","Joshua Van",NR),("LA-15","Kamaru Usman",NR),
    ("LA-16","Tallison Teixeira",RC),("LA-17","Maycee Barber",NR),("LA-18","Lerone Murphy",NR),("LA-19","Patricio Freire",RC),("LA-20","Max Holloway",NR),
]
add_cards(la_is, la)
print(f"  Lunar Apex: {len(la)} cards")

# ─── INSOMNIA ─────────────────────────────────────────────────────
ins_is = create_insert_set(set_id, "Insomnia")
ins = [
    ("IN-1","Ilia Topuria",NR),("IN-2","Sean O'Malley",NR),("IN-3","Alexander Volkanovski",NR),("IN-4","Islam Makhachev",NR),("IN-5","Natalia Cristina da Silva",NR),
    ("IN-6","Tom Aspinall",NR),("IN-7","Dricus Du Plessis",NR),("IN-8","Bo Nickal",NR),("IN-9","Jon Jones",NR),("IN-10","Belal Muhammad",NR),
    ("IN-11","Israel Adesanya",NR),("IN-12","Joe Pyfer",NR),("IN-13","Caio Borralho",NR),("IN-14","Conor McGregor",NR),("IN-15","Reinier De Ridder",NR),
    ("IN-16","Khamzat Chimaev",NR),("IN-17","Alex Pereira",NR),("IN-18","Rose Namajunas",NR),("IN-19","Paddy Pimblett",NR),("IN-20","Justin Gaethje",NR),
    ("IN-21","Jack Della Maddalena",NR),("IN-22","Vinicius Oliveira",NR),("IN-23","Alexandre Pantoja",NR),("IN-24","Zhang Weili",NR),("IN-25","Diego Lopes",NR),
]
add_cards(ins_is, ins)
print(f"  Insomnia: {len(ins)} cards")

# ─── LAST ONE STANDING ────────────────────────────────────────────
lo_is = create_insert_set(set_id, "Last One Standing")
lo = [
    ("LO-1","Jon Jones",NR),("LO-2","Valentina Shevchenko",NR),("LO-3","Merab Dvalishvili",NR),("LO-4","Max Holloway",NR),("LO-5","Jack Della Maddalena",NR),
    ("LO-6","Khabib Nurmagomedov",NR),("LO-7","Dricus Du Plessis",NR),("LO-8","Carlos Prates",NR),("LO-9","Magomed Ankalaev",NR),("LO-10","Joshua Van",NR),
    ("LO-11","Arman Tsarukyan",NR),("LO-12","Sean O'Malley",NR),("LO-13","Mauricio Santos",NR),("LO-14","Lerone Murphy",NR),("LO-15","Kayla Harrison",NR),
    ("LO-16","Umar Nurmagomedov",NR),("LO-17","Movsar Evloev",NR),("LO-18","Shavkat Rakhmonov",NR),("LO-19","Diego Lopes",NR),("LO-20","Ilia Topuria",NR),
    ("LO-21","Sean Strickland",NR),("LO-22","Anderson Silva",NR),("LO-23","Bo Nickal",NR),("LO-24","Charles Oliveira",NR),("LO-25","Daniel Hooker",NR),
    ("LO-26","Brendan Allen",NR),("LO-27","Jean Silva",NR),("LO-28","Alex Pereira",NR),("LO-29","Justin Gaethje",NR),("LO-30","Israel Adesanya",NR),
]
add_cards(lo_is, lo)
print(f"  Last One Standing: {len(lo)} cards")

# ─── NEON APEX ────────────────────────────────────────────────────
na_is = create_insert_set(set_id, "Neon Apex")
na = [
    ("NA-1","Ilia Topuria",NR),("NA-2","Conor McGregor",NR),("NA-3","Zhang Weili",NR),("NA-4","Paddy Pimblett",NR),("NA-5","Natalia Cristina da Silva",NR),
    ("NA-6","Mauricio Santos",NR),("NA-7","Khalil Rountree Jr.",NR),("NA-8","Alexander Volkanovski",NR),("NA-9","Ciryl Gane",NR),("NA-10","Khamzat Chimaev",NR),
    ("NA-11","Payton Talbott",NR),("NA-12","Mackenzie Dern",NR),("NA-13","Manon Fiorot",NR),("NA-14","Caio Borralho",NR),("NA-15","Tom Aspinall",NR),
    ("NA-16","Diego Lopes",NR),("NA-17","Magomed Ankalaev",NR),("NA-18","Islam Makhachev",NR),("NA-19","Derrick Lewis",NR),("NA-20","Alexander Volkov",NR),
    ("NA-21","Assu Almabayev",NR),("NA-22","Joshua Van",NR),("NA-23","Brandon Royval",NR),("NA-24","Dricus Du Plessis",NR),("NA-25","Sean O'Malley",NR),
]
add_cards(na_is, na)
print(f"  Neon Apex: {len(na)} cards")

# ─── TWILIGHT ─────────────────────────────────────────────────────
tw_is = create_insert_set(set_id, "Twilight")
tw = [
    ("TL-1","Khamzat Chimaev",NR),("TL-2","Jean Silva",NR),("TL-3","Valentina Shevchenko",NR),("TL-4","Joshua Van",NR),("TL-5","Erin Blanchfield",NR),
    ("TL-6","Reinier De Ridder",NR),("TL-7","Natalia Cristina da Silva",NR),("TL-8","Khabib Nurmagomedov",NR),("TL-9","Nassourdine Imavov",NR),("TL-10","Jack Della Maddalena",NR),
    ("TL-11","Justin Gaethje",NR),("TL-12","Ilia Topuria",NR),("TL-13","Arman Tsarukyan",NR),("TL-14","Georges St-Pierre",NR),("TL-15","Alexander Volkanovski",NR),
    ("TL-16","Alex Pereira",NR),("TL-17","Dustin Poirier",NR),("TL-18","Tracy Cortez",NR),("TL-19","Paddy Pimblett",NR),("TL-20","Alexandre Pantoja",NR),
]
add_cards(tw_is, tw)
print(f"  Twilight: {len(tw)} cards")

# ─── CEMENTED ─────────────────────────────────────────────────────
cm_is = create_insert_set(set_id, "Cemented")
cm = [
    ("CM-1","Tom Aspinall",NR),("CM-2","Charles Oliveira",NR),("CM-3","Israel Adesanya",NR),("CM-4","Kayla Harrison",NR),("CM-5","Sean O'Malley",NR),
    ("CM-6","Alexa Grasso",NR),("CM-7","Anderson Silva",NR),("CM-8","Dricus Du Plessis",NR),("CM-9","Leon Edwards",NR),("CM-10","Alexandre Pantoja",NR),
    ("CM-11","Chuck Liddell",NR),("CM-12","Jiri Prochazka",NR),("CM-13","Jon Jones",NR),("CM-14","Conor McGregor",NR),("CM-15","Rose Namajunas",NR),
    ("CM-16","Sean Strickland",NR),("CM-17","Khabib Nurmagomedov",NR),("CM-18","Yair Rodríguez",NR),("CM-19","Amanda Nunes",NR),("CM-20","Alex Pereira",NR),
    ("CM-21","Dustin Poirier",NR),("CM-22","Max Holloway",NR),("CM-23","Mackenzie Dern",NR),("CM-24","Islam Makhachev",NR),("CM-25","Merab Dvalishvili",NR),
]
add_cards(cm_is, cm)
print(f"  Cemented: {len(cm)} cards")

# ─── ROOKIE RELIC AUTOGRAPHS ─────────────────────────────────────
rra_is = create_insert_set(set_id, "Rookie Relic Autographs")
rra = [
    ("RRA-AA","Alexia Thainara",RC),("RRA-AG","Gautier Ateba",RC),("RRA-AL","Andre Lima",RC),("RRA-AP","Aaron Pico",RC),("RRA-AS","Andreas Gustafsson",RC),
    ("RRA-AV","Austin Vanderford",RC),("RRA-BB","Bruna Brasil",RC),("RRA-CC","Clayton Carpenter",RC),("RRA-CH","Chang Ho Lee",RC),("RRA-CL","Carlos Leal",RC),
    ("RRA-CP","Chris Padilla",RC),("RRA-DB","Dione Barbosa",RC),("RRA-DO","David Onama",RC),("RRA-DS","Daniel Santos",RC),("RRA-ES","Elijah Smith",RC),
    ("RRA-FL","Felipe Lima",RC),("RRA-GS","Gabriel Santos",RC),("RRA-HA","Hyder Amil",RC),("RRA-JA","Jaqueline Amorim",RC),("RRA-JC","Jacqueline Cavalcanti",RC),
    ("RRA-JJ","JJ Aldrich",RC),("RRA-JL","JeongYeong Lee",RC),("RRA-JY","Joo Sang Yoo",RC),("RRA-KF","Kaue Fernandes",RC),("RRA-KS","Kody Steele",RC),
    ("RRA-LK","Lone'er Kavanagh",RC),("RRA-MA","Mansur Abdul-Malik",RC),("RRA-MI","Michael Aswell",RC),("RRA-MM","MarQuel Mederos",RC),("RRA-MN","Michael Parkin",RC),
    ("RRA-MP","Mario Pinto",RC),("RRA-MS","Shi Ming",RC),("RRA-MT","Marco Silva",RC),("RRA-MW","Malcolm Wellmaker",RC),("RRA-NR","Nursulton Ruziboev",RC),
    ("RRA-PP","Patricio Freire",RC),("RRA-QS","Quillan Salkilld",RC),("RRA-RE","Rafael Estevam",RC),("RRA-RT","Rei Tsuruya",RC),("RRA-RU","Zhu Rong",RC),
    ("RRA-SK","Seok Hyeon Ko",RC),("RRA-TF","Torrez Finney",RC),("RRA-TN","Tom Nolan",RC),("RRA-TT","Tallison Teixeira",RC),("RRA-WC","Wang Cong",RC),
    ("RRA-YZ","Youssef Zalal",RC),
]
add_cards(rra_is, rra)
print(f"  Rookie Relic Autographs: {len(rra)} cards")

# ─── RELIC AUTOGRAPHS ────────────────────────────────────────────
vra_is = create_insert_set(set_id, "Relic Autographs")
vra = [
    ("VRA-AP","Alexandre Pantoja",NR),("VRA-AT","Arman Tsarukyan",NR),("VRA-AV","Alexander Volkanovski",NR),("VRA-CH","Chase Hooper",NR),("VRA-CO","Charles Oliveira",NR),
    ("VRA-DD","Dricus Du Plessis",NR),("VRA-DP","Dustin Poirier",NR),("VRA-EB","Erin Blanchfield",NR),("VRA-IA","Israel Adesanya",NR),("VRA-JD","Jack Della Maddalena",NR),
    ("VRA-JG","Justin Gaethje",NR),("VRA-JJ","Jon Jones",NR),("VRA-KC","Khamzat Chimaev",NR),("VRA-MD","Merab Dvalishvili",NR),("VRA-MF","Manon Fiorot",NR),
    ("VRA-NC","Natalia Cristina da Silva",NR),("VRA-ND","Norma Dumont",NR),("VRA-NI","Nassourdine Imavov",NR),("VRA-PP","Paddy Pimblett",NR),("VRA-SB","Sean Brady",NR),
    ("VRA-TC","Tracy Cortez",NR),
]
add_cards(vra_is, vra)
print(f"  Relic Autographs: {len(vra)} cards")

# ─── FIGHT GLOVE RELIC AUTOGRAPHS ─────────────────────────���──────
fga_is = create_insert_set(set_id, "Fight Glove Relic Autographs")
fga = [
    ("FGA-AG","Alexa Grasso",NR),("FGA-AP","Alexandre Pantoja",NR),("FGA-AV","Alexander Volkanovski",NR),("FGA-CO","Charles Oliveira",NR),("FGA-DD","Dricus Du Plessis",NR),
    ("FGA-DP","Dustin Poirier",NR),("FGA-IA","Israel Adesanya",NR),("FGA-IM","Islam Makhachev",NR),("FGA-JD","Jack Della Maddalena",NR),("FGA-JG","Justin Gaethje",NR),
    ("FGA-JJ","Jon Jones",NR),("FGA-KC","Khamzat Chimaev",NR),("FGA-KH","Kayla Harrison",NR),("FGA-MA","Magomed Ankalaev",NR),("FGA-MD","Merab Dvalishvili",NR),
    ("FGA-MH","Max Holloway",NR),("FGA-PE","Alex Pereira",NR),("FGA-PP","Paddy Pimblett",NR),("FGA-SO","Sean O'Malley",NR),("FGA-SR","Shavkat Rakhmonov",NR),
    ("FGA-TA","Tom Aspinall",NR),("FGA-TS","Tatiana Suarez",NR),("FGA-VS","Valentina Shevchenko",NR),("FGA-ZW","Zhang Weili",NR),
]
add_cards(fga_is, fga)
print(f"  Fight Glove Relic Autographs: {len(fga)} cards")

# ─── AUTOGRAPH VARIATION ─────────────────────────────────────────
bav_is = create_insert_set(set_id, "Autograph Variation")
bav = [
    ("BAV-AG","Aljamain Sterling",NR),("BAV-AH","Anthony Hernandez",NR),("BAV-AL","Amanda Lemos",NR),("BAV-AN","Amanda Nunes",NR),("BAV-AP","Alex Perez",NR),
    ("BAV-AR","Aleksandar Rakic",NR),("BAV-AS","Anderson Silva",NR),("BAV-AV","Alexander Volkov",NR),("BAV-AY","Adrian Yanez",NR),("BAV-BD","Beneil Dariush",NR),
    ("BAV-BM","Belal Muhammad",NR),("BAV-BO","Brian Ortega",NR),("BAV-CC","Colby Covington",NR),("BAV-CL","Chuck Liddell",NR),("BAV-CM","Conor McGregor",NR),
    ("BAV-CP","Carlos Prates",NR),("BAV-CU","Carlos Ulberg",NR),("BAV-DC","Daniel Cormier",NR),("BAV-DE","Donald Cerrone",NR),("BAV-DH","Daniel Hooker",NR),
    ("BAV-DL","Diego Lopes",NR),("BAV-FM","Frank Mir",NR),("BAV-GS","Georges St-Pierre",NR),("BAV-JA","Jessica Andrade",NR),("BAV-JE","Josh Emmett",NR),
    ("BAV-JI","Jiri Prochazka",NR),("BAV-JJ","Jasmine Jasudavicius",NR),("BAV-JP","Joe Pyfer",NR),("BAV-JS","Jean Silva",NR),("BAV-KH","Kevin Holland",NR),
    ("BAV-KN","Khabib Nurmagomedov",NR),("BAV-KV","Ketlen Vieira",NR),("BAV-LE","Leon Edwards",NR),("BAV-LM","Lerone Murphy",NR),("BAV-MB","Maycee Barber",NR),
    ("BAV-MC","Macy Chiasson",NR),("BAV-MD","Mackenzie Dern",NR),("BAV-MG","Mateusz Gamrot",NR),("BAV-MH","Max Holloway",NR),("BAV-MK","Manel Kape",NR),
    ("BAV-MM","Michael Morales",NR),("BAV-MO","Myktybek Orolbai",NR),("BAV-MP","Michael Page",NR),("BAV-RD","Reinier de Ridder",NR),("BAV-RN","Rose Namajunas",NR),
    ("BAV-RR","Raul Rosas",NR),("BAV-SE","Stephen Erceg",NR),("BAV-SO","Sean O'Malley",NR),("BAV-SS","Sean Strickland",NR),("BAV-TA","Tom Aspinall",NR),
    ("BAV-TR","Tabatha Ricci",NR),("BAV-UN","Umar Nurmagomedov",NR),("BAV-VJ","Virna Jandiroba",NR),("BAV-VS","Valentina Shevchenko",NR),("BAV-YR","Yair Rodríguez",NR),
    ("BAV-YS","Yadong Song",NR),("BAV-YX","Yan Xiaonan",NR),
]
add_cards(bav_is, bav)
print(f"  Autograph Variation: {len(bav)} cards")

# ─── HORIZON SIGNATURES ──────────────────────────────────────────
hzs_is = create_insert_set(set_id, "Horizon Signatures")
hzs = [
    ("HZS-AA","Arnold Allen",NR),("HZS-AG","Alexa Grasso",NR),("HZS-AP","Alex Pereira",NR),("HZS-BM","Brandon Moreno",NR),("HZS-BN","Bo Nickal",NR),
    ("HZS-BR","Brandon Royval",NR),("HZS-CB","Caio Borralho",NR),("HZS-CG","Ciryl Gane",NR),("HZS-CS","Cory Sandhagen",NR),("HZS-DZ","Daniel Zellhuber",NR),
    ("HZS-IG","Ian Machado Garry",NR),("HZS-IM","Islam Makhachev",NR),("HZS-JP","Julianna Peña",NR),("HZS-JV","Joshua Van",NR),("HZS-KA","Kai Asakura",NR),
    ("HZS-KH","Kayla Harrison",NR),("HZS-KK","Kai Kara-France",NR),("HZS-MC","Michael Chandler",NR),("HZS-PT","Payton Talbott",NR),("HZS-PY","Petr Yan",NR),
    ("HZS-RE","Rashad Evans",NR),("HZS-RM","Renato Moicano",NR),("HZS-RP","Raquel Pennington",NR),("HZS-ST","Stephen Thompson",NR),("HZS-TT","Tatsuro Taira",NR),
    ("HZS-ZW","Zhang Weili",NR),
]
add_cards(hzs_is, hzs)
print(f"  Horizon Signatures: {len(hzs)} cards")

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

# ─── Commit ───────────────────────────────────────────────────────
conn.commit()

cur.execute("SELECT COUNT(*) FROM players WHERE set_id = ?", (set_id,))
player_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON pa.insert_set_id = i.id WHERE i.set_id = ?", (set_id,))
app_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id = ?", (set_id,))
is_count = cur.fetchone()[0]

print(f"\nDone! Set ID: {set_id}")
print(f"  Players: {player_count}")
print(f"  Appearances: {app_count}")
print(f"  Insert sets: {is_count}")
conn.close()
