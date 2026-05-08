"""
Seed: 2026 Topps Chrome UFC — Full checklist.
Base (200), 21 insert sets, 10 autograph sets, parallels mirrored from 2025 Chrome UFC.
Usage: python3 scripts/seed_chrome_ufc_2026.py
"""
import sqlite3, os, re

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
db = sqlite3.connect(DB_PATH)
db.execute("PRAGMA journal_mode=WAL")
db.execute("PRAGMA foreign_keys=ON")

# ─── Create Set ──────────────────────────────────────────────────────────────
db.execute("""
    INSERT INTO sets (name, sport, league, season, tier, slug, is_visible,
                      sample_image_url, release_date)
    VALUES ('2026 Topps Chrome UFC', 'MMA', 'UFC', '2026', 'Standard',
            '2026-topps-chrome-ufc', 1,
            '/sets/2026-topps-chrome-ufc.jpg', '2026-05-08')
""")
SET_ID = db.execute("SELECT last_insert_rowid()").fetchone()[0]
print(f"Created set ID: {SET_ID}")

T = True; R = False

def get_or_create_player(name):
    row = db.execute("SELECT id FROM players WHERE set_id = ? AND name = ?", (SET_ID, name)).fetchone()
    if row: return row[0]
    db.execute("INSERT INTO players (set_id, name, unique_cards, total_print_run, one_of_ones, insert_set_count) VALUES (?, ?, 0, 0, 0, 0)", (SET_ID, name))
    return db.execute("SELECT last_insert_rowid()").fetchone()[0]

def add_is(name):
    db.execute("INSERT INTO insert_sets (set_id, name) VALUES (?, ?)", (SET_ID, name))
    return db.execute("SELECT last_insert_rowid()").fetchone()[0]

def add_parallel(is_id, name, print_run=None):
    db.execute("INSERT INTO parallels (insert_set_id, name, print_run) VALUES (?, ?, ?)", (is_id, name, print_run))

def add_cards(is_id, cards):
    for num, name, rookie in cards:
        pid = get_or_create_player(name)
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, NULL)",
                   (pid, is_id, str(num), int(rookie)))
    print(f"  {db.execute('SELECT name FROM insert_sets WHERE id=?',(is_id,)).fetchone()[0]}: {len(cards)} cards")

def add_dual_cards(is_id, cards):
    for num, p1, p2 in cards:
        pid1 = get_or_create_player(p1)
        pid2 = get_or_create_player(p2)
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, NULL)", (pid1, is_id, str(num)))
        a1 = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a1, pid2))
    print(f"  {db.execute('SELECT name FROM insert_sets WHERE id=?',(is_id,)).fetchone()[0]}: {len(cards)} dual cards")

# ─── Parallel ladders (mirrored from 2025 Chrome UFC set 28) ────────────────
BASE_PARALLELS = [
    ("Refractor", None), ("Magenta", None), ("Negative", None), ("Prism", None),
    ("Purple", None), ("Sepia", None), ("X-Fractor", None),
    ("Speckle", 299), ("Aqua", 199), ("Blue", 150), ("Green", 99),
    ("Blue Wave", 75), ("Gold", 50), ("Orange", 25), ("Black", 10),
    ("Red", 5), ("Superfractor", 1),
]

INSERT_PARALLELS = [
    ("Refractor", None), ("Gold", 50), ("Black", 10), ("Red", 5), ("Superfractor", 1),
]

AUTO_PARALLELS = [
    ("Refractor", 150), ("Gold", 50), ("Orange", 25), ("Black", 10), ("Red", 5), ("Superfractor", 1),
]

# ─── BASE CARDS I (1-100) ────────────────────────────────────────────────────
base_id = add_is("Base Set")
for p_name, p_run in BASE_PARALLELS:
    add_parallel(base_id, p_name, p_run)

base1 = [
    (1,"Ilia Topuria",R),(2,"Sean Strickland",R),(3,"Valentina Shevchenko",R),
    (4,"Gabriel Santos",T),(5,"Conor McGregor",R),(6,"Leon Edwards",R),
    (7,"Gautier Ateba",T),(8,"Daniel Cormier",R),(9,"Patrick Mix",T),
    (10,"Dricus Du Plessis",R),(11,"Michael Aswell",T),(12,"Alexander Volkov",R),
    (13,"Wang Cong",T),(14,"Anderson Silva",R),(15,"Joshua Van",R),
    (16,"Alvin Hines",T),(17,"Payton Talbott",R),(18,"Ciryl Gane",R),
    (19,"Azamat Murzakanov",R),(20,"Zhang Weili",R),(21,"Sharabutdin Magomedov",R),
    (22,"Rafael Estevam",T),(23,"Paddy Pimblett",R),(24,"Islam Dulatov",T),
    (25,"Nazim Sadykhov",R),(26,"Kai Asakura",R),(27,"Kamaru Usman",R),
    (28,"Jean Matsumoto",R),(29,"JJ Aldrich",T),(30,"Alexander Volkanovski",R),
    (31,"Mario Pinto",T),(32,"Amanda Ribas",R),(33,"Dione Barbosa",T),
    (34,"Ailin Perez",R),(35,"Chase Hooper",R),(36,"Jon Jones",R),
    (37,"Jacqueline Cavalcanti",T),(38,"Reinier De Ridder",R),(39,"Justin Gaethje",R),
    (40,"Alexandre Pantoja",R),(41,"Elijah Smith",T),(42,"Jiri Prochazka",R),
    (43,"Daniel Marcos",R),(44,"Tofiq Musayev",T),(45,"Yadong Song",R),
    (46,"Bo Nickal",R),(47,"Islam Makhachev",R),(48,"Youssef Zalal",T),
    (49,"Esteban Ribovics",R),(50,"Merab Dvalishvili",R),(51,"Muhammadjon Naimov",R),
    (52,"Michael Parkin",T),(53,"Petr Yan",R),(54,"Brandon Royval",R),
    (55,"Kayla Harrison",R),(56,"Joaquin Buckley",R),(57,"Quillan Salkilld",T),
    (58,"Tracy Cortez",R),(59,"Mansur Abdul-Malik",T),(60,"Magomed Ankalaev",R),
    (61,"Marcus Almeida",T),(62,"Mario Bautista",R),(63,"Erin Blanchfield",R),
    (64,"Trevor Peek",R),(65,"Cory Sandhagen",R),(66,"Rei Tsuruya",T),
    (67,"Michael Morales",R),(68,"Norma Dumont",R),(69,"Tallison Teixeira",T),
    (70,"Manon Fiorot",R),(71,"Carlos Leal",T),(72,"Tatsuro Taira",R),
    (73,"Virna Jandiroba",R),(74,"Nursulton Ruziboev",T),(75,"Jack Della Maddalena",R),
    (76,"Caio Borralho",R),(77,"Ramazan Temirov",T),(78,"Dustin Poirier",R),
    (79,"Jasmine Jasudavicius",R),(80,"Tom Aspinall",R),(81,"Casey O'Neill",R),
    (82,"Derrick Lewis",R),(83,"Bruna Brasil",T),(84,"Sergei Pavlovich",R),
    (85,"Piera Rodriguez",R),(86,"Austin Vanderford",T),(87,"Rose Namajunas",R),
    (88,"Aaron Pico",T),(89,"Deiveson Figueiredo",R),(90,"Alex Pereira",R),
    (91,"Colby Covington",R),(92,"Tatiana Suarez",R),(93,"Ian Machado Garry",R),
    (94,"Patricio Freire",T),(95,"Jamahal Hill",R),(96,"Curtis Blaydes",R),
    (97,"Oumar Sy",T),(98,"Amir Albazi",R),(99,"Francis Marshall",T),
    (100,"Max Holloway",R),
]
add_cards(base_id, base1)

# ─── BASE CARDS II (101-200) ─────────────────────────────────────────────────
base2 = [
    (101,"Belal Muhammad",R),(102,"Mark Choinski",T),(103,"Raquel Pennington",R),
    (104,"Seok Hyeon Ko",T),(105,"Macy Chiasson",R),(106,"Sean Brady",R),
    (107,"Waldo Cortes",R),(108,"Kaue Fernandes",T),(109,"Kai Kara-France",R),
    (110,"Carlos Ulberg",R),(111,"Chris Padilla",T),(112,"Amanda Lemos",R),
    (113,"Tom Nolan",T),(114,"Gabriel Bonfim",R),(115,"Umar Nurmagomedov",R),
    (116,"Yan Xiaonan",R),(117,"Danny Barlow",R),(118,"Malcolm Wellmaker",T),
    (119,"Jan Błachowicz",R),(120,"Arman Tsarukyan",R),(121,"Andreas Gustafsson",T),
    (122,"Vinicius Oliveira",R),(123,"Carlos Prates",R),(124,"Talita Alencar",T),
    (125,"Khamzat Chimaev",R),(126,"Oban Elliott",T),(127,"Karine Silva",R),
    (128,"Diego Lopes",R),(129,"Shi Ming",T),(130,"Jose Mariscal",R),
    (131,"Nassourdine Imavov",R),(132,"Jailton Almeida",R),(133,"Jackson McVey",T),
    (134,"Hyunsung Park",R),(135,"Michael Page",R),(136,"Gillian Robertson",R),
    (137,"Daniel Santos",T),(138,"Jessica Andrade",R),(139,"Chang Ho Lee",T),
    (140,"Khabib Nurmagomedov",R),(141,"Josh Emmett",R),(142,"Tim Elliott",R),
    (143,"Kody Steele",T),(144,"Miranda Maverick",R),(145,"Ludovit Klein",R),
    (146,"Joo Sang Yoo",T),(147,"Manel Kape",R),(148,"David Onama",T),
    (149,"Roman Kopylov",R),(150,"Charles Oliveira",R),(151,"Lone'er Kavanagh",T),
    (152,"Daniel Hooker",R),(153,"Yair Rodríguez",R),(154,"Navajo Stirling",T),
    (155,"Arnold Allen",R),(156,"Marco Silva",T),(157,"Khalil Rountree Jr.",R),
    (158,"Fatima Kline",T),(159,"Michael Chandler",R),(160,"Felipe Lima",T),
    (161,"Robert Whittaker",R),(162,"Brandon Moreno",R),(163,"Jean Silva",R),
    (164,"Rizvan Kuniev",T),(165,"Movsar Evloev",R),(166,"Torrez Finney",T),
    (167,"Luana Santos",R),(168,"Marquel Mederos",T),(169,"Charles Jourdain",R),
    (170,"Alexa Grasso",R),(171,"Raul Rosas",R),(172,"Zhu Rong",T),
    (173,"Irene Aldana",R),(174,"Nasrat Haqparast",T),(175,"Julianna Peña",R),
    (176,"Shavkat Rakhmonov",R),(177,"Mingyang Zhang",T),(178,"Mauricio Santos",R),
    (179,"Nora Cornolle",T),(180,"Maycee Barber",R),(181,"Thiago Moises",R),
    (182,"Jaqueline Amorim",T),(183,"Marcus McGhee",R),(184,"Clayton Carpenter",T),
    (185,"Mackenzie Dern",R),(186,"Stephen Erceg",R),(187,"Aleksandre Topuria",T),
    (188,"Natalia Cristina da Silva",R),(189,"Ibo Aslan",T),(190,"Lerone Murphy",R),
    (191,"Alexia Thainara",T),(192,"Daniel Zellhuber",R),(193,"Andre Lima",T),
    (194,"Brian Ortega",R),(195,"Amanda Nunes",R),(196,"Jeong Yeong Lee",T),
    (197,"Israel Adesanya",R),(198,"Ketlen Vieira",R),(199,"Hyder Amil",T),
    (200,"Sean O'Malley",R),
]
add_cards(base_id, base2)

# ─── INSERT SUBSETS ──────────────────────────────────────────────────────────

def add_insert_with_parallels(name, cards, parallels=INSERT_PARALLELS):
    is_id = add_is(name)
    for p_name, p_run in parallels:
        add_parallel(is_id, p_name, p_run)
    add_cards(is_id, cards)
    return is_id

# Sapphire Selections
add_insert_with_parallels("Sapphire Selections", [
    ("SS-1","Nassourdine Imavov",R),("SS-2","Khamzat Chimaev",R),("SS-3","Arman Tsarukyan",R),
    ("SS-4","Max Holloway",R),("SS-5","Bo Nickal",R),("SS-6","Sean O'Malley",R),
    ("SS-7","Paddy Pimblett",R),("SS-8","Dustin Poirier",R),("SS-9","Zhang Weili",R),
    ("SS-10","Conor McGregor",R),("SS-11","Jon Jones",R),("SS-12","Tom Aspinall",R),
    ("SS-13","Alex Pereira",R),("SS-14","Joshua Van",R),("SS-15","Justin Gaethje",R),
])

# Infinite
add_insert_with_parallels("Infinite", [
    ("IN-1","Khabib Nurmagomedov",R),("IN-2","Anderson Silva",R),("IN-3","Ilia Topuria",R),
    ("IN-4","Islam Makhachev",R),("IN-5","Kayla Harrison",R),("IN-6","Dricus Du Plessis",R),
    ("IN-7","Alexa Grasso",R),("IN-8","Israel Adesanya",R),("IN-9","Alexandre Pantoja",R),
    ("IN-10","Merab Dvalishvili",R),
])

# All Action
add_insert_with_parallels("All Action", [
    ("AA-1","Ilia Topuria",R),("AA-2","Colby Covington",R),("AA-3","Mauricio Santos",R),
    ("AA-4","Robert Whittaker",R),("AA-5","Daniel Hooker",R),("AA-6","Ramazan Temirov",T),
    ("AA-7","Alexandre Pantoja",R),("AA-8","Youssef Zalal",T),("AA-9","Nassourdine Imavov",R),
    ("AA-10","Julianna Peña",R),("AA-11","Manel Kape",R),("AA-12","Jacqueline Cavalcanti",R),
    ("AA-13","Rose Namajunas",R),("AA-14","Michael Page",R),("AA-15","David Onama",T),
    ("AA-16","Khamzat Chimaev",R),("AA-17","Iasmin Lucindo",R),("AA-18","Dustin Poirier",R),
    ("AA-19","Sharabutdin Magomedov",R),("AA-20","Paddy Pimblett",R),("AA-21","Maycee Barber",R),
    ("AA-22","Tallison Teixeira",T),("AA-23","Arman Tsarukyan",R),("AA-24","Diego Lopes",R),
    ("AA-25","Erin Blanchfield",R),("AA-26","Ian Machado Garry",R),("AA-27","Michael Parkin",T),
    ("AA-28","Justin Gaethje",R),("AA-29","Oumar Sy",T),("AA-30","Jiri Prochazka",R),
    ("AA-31","Umar Nurmagomedov",R),("AA-32","Sean Brady",R),("AA-33","Kevin Holland",R),
    ("AA-34","Tabatha Ricci",R),("AA-35","Dricus Du Plessis",R),("AA-36","Benoit Saint Denis",R),
    ("AA-37","Rizvan Kuniev",T),("AA-38","Movsar Evloev",R),("AA-39","Brandon Royval",R),
    ("AA-40","Sean O'Malley",R),("AA-41","Yair Rodríguez",R),("AA-42","Raul Rosas",R),
    ("AA-43","JJ Aldrich",T),("AA-44","Derrick Lewis",R),("AA-45","Islam Makhachev",R),
    ("AA-46","Caio Borralho",R),("AA-47","Wang Cong",T),("AA-48","Payton Talbott",R),
    ("AA-49","Jamahal Hill",R),("AA-50","Mingyang Zhang",T),
])

# 1986 Topps
add_insert_with_parallels("1986 Topps", [
    ("86-1","Kayla Harrison",R),("86-2","Robert Whittaker",R),("86-3","Alexandre Pantoja",R),
    ("86-4","Joshua Van",R),("86-5","Ilia Topuria",R),("86-6","Maycee Barber",R),
    ("86-7","Raul Rosas",R),("86-8","Dricus Du Plessis",R),("86-9","Khamzat Chimaev",R),
    ("86-10","Michael Page",R),("86-11","Dustin Poirier",R),("86-12","Rose Namajunas",R),
    ("86-13","Sharabutdin Magomedov",R),("86-14","Ian Machado Garry",R),("86-15","Diego Lopes",R),
    ("86-16","Conor McGregor",R),("86-17","Movsar Evloev",R),("86-18","Shavkat Rakhmonov",R),
    ("86-19","Julianna Peña",R),("86-20","Islam Makhachev",R),
])

# Striking Distance
add_insert_with_parallels("Striking Distance", [
    ("SD-1","Payton Talbott",R),("SD-2","Raul Rosas",R),("SD-3","Tallison Teixeira",T),
    ("SD-4","Alexander Volkanovski",R),("SD-5","Maycee Barber",R),("SD-6","Alexandre Pantoja",R),
    ("SD-7","Jiri Prochazka",R),("SD-8","Kayla Harrison",R),("SD-9","Sharabutdin Magomedov",R),
    ("SD-10","Ian Machado Garry",R),("SD-11","Colby Covington",R),("SD-12","Reinier De Ridder",R),
    ("SD-13","Dustin Poirier",R),("SD-14","Arman Tsarukyan",R),("SD-15","Rose Namajunas",R),
    ("SD-16","Ramazan Temirov",T),("SD-17","Islam Makhachev",R),("SD-18","Stephen Erceg",R),
    ("SD-19","Shavkat Rakhmonov",R),("SD-20","Justin Gaethje",R),("SD-21","Mingyang Zhang",T),
    ("SD-22","Sean O'Malley",R),("SD-23","Bo Nickal",R),("SD-24","Michael Page",R),
    ("SD-25","Youssef Zalal",T),("SD-26","Diego Lopes",R),("SD-27","Rizvan Kuniev",T),
    ("SD-28","Daniel Hooker",R),("SD-29","Merab Dvalishvili",R),("SD-30","Robert Whittaker",R),
])

# Big Ticket
add_insert_with_parallels("Big Ticket", [
    ("BT-1","Alexandre Pantoja",R),("BT-2","Max Holloway",R),("BT-3","Jon Jones",R),
    ("BT-4","Paddy Pimblett",R),("BT-5","Alexa Grasso",R),("BT-6","Kayla Harrison",R),
    ("BT-7","Conor McGregor",R),("BT-8","Dricus Du Plessis",R),("BT-9","Georges St-Pierre",R),
    ("BT-10","Cody Garbrandt",R),("BT-11","Islam Makhachev",R),("BT-12","Kamaru Usman",R),
    ("BT-13","Charles Oliveira",R),("BT-14","Sean Strickland",R),("BT-15","Khamzat Chimaev",R),
    ("BT-16","Ilia Topuria",R),("BT-17","Alex Pereira",R),("BT-18","Anderson Silva",R),
    ("BT-19","Merab Dvalishvili",R),("BT-20","Dustin Poirier",R),("BT-21","Israel Adesanya",R),
    ("BT-22","Tom Aspinall",R),("BT-23","Khabib Nurmagomedov",R),("BT-24","Diego Lopes",R),
    ("BT-25","Sean O'Malley",R),
])

# Split Decision (dual cards)
sp_id = add_is("Split Decision")
for p_name, p_run in INSERT_PARALLELS:
    add_parallel(sp_id, p_name, p_run)
sp_cards = [
    ("SP-1","Amanda Nunes","Kayla Harrison"),("SP-2","Jon Jones","Daniel Cormier"),
    ("SP-3","Ian Machado Garry","Shavkat Rakhmonov"),("SP-4","Charles Oliveira","Ilia Topuria"),
    ("SP-5","Alexandre Pantoja","Joshua Van"),("SP-6","Kevin Holland","Michael Page"),
    ("SP-7","Dustin Poirier","Max Holloway"),("SP-8","Khamzat Chimaev","Dricus Du Plessis"),
    ("SP-9","Belal Muhammad","Jack Della Maddalena"),("SP-10","Valentina Shevchenko","Alexa Grasso"),
    ("SP-11","Manon Fiorot","Erin Blanchfield"),("SP-12","Rose Namajunas","Zhang Weili"),
    ("SP-13","Khabib Nurmagomedov","Conor McGregor"),("SP-14","Raquel Pennington","Julianna Peña"),
    ("SP-15","Arman Tsarukyan","Islam Makhachev"),("SP-16","Diego Lopes","Alexander Volkanovski"),
    ("SP-17","Jiri Prochazka","Jamahal Hill"),("SP-18","Merab Dvalishvili","Sean O'Malley"),
    ("SP-19","Colby Covington","Joaquin Buckley"),("SP-20","Alex Pereira","Israel Adesanya"),
    ("SP-21","Gregory Rodrigues","Jared Cannonier"),("SP-22","Ciryl Gane","Tom Aspinall"),
    ("SP-23","Anderson Silva","Chael Sonnen"),("SP-24","Dricus Du Plessis","Sean Strickland"),
    ("SP-25","BJ Penn","Georges St-Pierre"),
]
add_dual_cards(sp_id, sp_cards)

# Remaining inserts (same pattern)
for name, cards in [
    ("Fight Night Flashback", [
        ("FNF-1","Zhang Weili",R),("FNF-2","Khabib Nurmagomedov",R),("FNF-3","Kamaru Usman",R),
        ("FNF-4","Justin Gaethje",R),("FNF-5","Jon Jones",R),("FNF-6","Petr Yan",R),
        ("FNF-7","Ilia Topuria",R),("FNF-8","Sean O'Malley",R),("FNF-9","Dricus Du Plessis",R),
        ("FNF-10","Charles Oliveira",R),("FNF-11","Israel Adesanya",R),("FNF-12","Conor McGregor",R),
        ("FNF-13","Robert Whittaker",R),("FNF-14","Valentina Shevchenko",R),("FNF-15","Max Holloway",R),
        ("FNF-16","Colby Covington",R),("FNF-17","Jiri Prochazka",R),("FNF-18","Alex Pereira",R),
        ("FNF-19","Yair Rodríguez",R),("FNF-20","Dustin Poirier",R),
    ]),
    ("Pulse Check", [
        ("PC-1","Sean O'Malley",R),("PC-2","Diego Lopes",R),("PC-3","Bo Nickal",R),
        ("PC-4","Maycee Barber",R),("PC-5","Islam Makhachev",R),("PC-6","Belal Muhammad",R),
        ("PC-7","Raul Rosas",R),("PC-8","Reinier De Ridder",R),("PC-9","Michael Page",R),
        ("PC-10","Shavkat Rakhmonov",R),("PC-11","Alex Pereira",R),("PC-12","Payton Talbott",R),
        ("PC-13","Magomed Ankalaev",R),("PC-14","Colby Covington",R),("PC-15","Max Holloway",R),
    ]),
    ("Youthquake", [
        ("YQ-1","Carlos Prates",R),("YQ-2","Ramazan Temirov",T),("YQ-3","Youssef Zalal",T),
        ("YQ-4","Nora Cornolle",T),("YQ-5","Jacqueline Cavalcanti",T),("YQ-6","Joshua Van",R),
        ("YQ-7","David Onama",T),("YQ-8","Tallison Teixeira",T),("YQ-9","Wang Cong",T),
        ("YQ-10","JJ Aldrich",T),("YQ-11","Patricio Freire",T),("YQ-12","Michael Parkin",T),
        ("YQ-13","Mingyang Zhang",T),("YQ-14","Rizvan Kuniev",T),("YQ-15","Jean Silva",R),
    ]),
    ("Global Warriors", [
        ("GW-1","Tom Aspinall",R),("GW-2","Alexander Volkanovski",R),("GW-3","Valentina Shevchenko",R),
        ("GW-4","Khamzat Chimaev",R),("GW-5","Dricus Du Plessis",R),("GW-6","Alexandre Pantoja",R),
        ("GW-7","Alexander Volkov",R),("GW-8","Conor McGregor",R),("GW-9","Jack Della Maddalena",R),
        ("GW-10","Zhang Weili",R),("GW-11","Charles Oliveira",R),("GW-12","Movsar Evloev",R),
        ("GW-13","Alex Pereira",R),("GW-14","Diego Lopes",R),("GW-15","Alexa Grasso",R),
        ("GW-16","Israel Adesanya",R),("GW-17","Islam Makhachev",R),("GW-18","Manon Fiorot",R),
        ("GW-19","Khabib Nurmagomedov",R),("GW-20","Reinier De Ridder",R),("GW-21","Ilia Topuria",R),
        ("GW-22","Belal Muhammad",R),("GW-23","Shavkat Rakhmonov",R),("GW-24","Merab Dvalishvili",R),
        ("GW-25","Umar Nurmagomedov",R),
    ]),
    ("Allen and Ginter", [
        ("AG-1","Alex Pereira",R),("AG-2","Michael Chandler",R),("AG-3","Jack Della Maddalena",R),
        ("AG-4","Sean Strickland",R),("AG-5","Tallison Teixeira",T),("AG-6","Sean O'Malley",R),
        ("AG-7","Oumar Sy",T),("AG-8","Leon Edwards",R),("AG-9","Magomed Ankalaev",R),
        ("AG-10","Israel Adesanya",R),("AG-11","Carlos Prates",R),("AG-12","Charles Oliveira",R),
        ("AG-13","Tatsuro Taira",R),("AG-14","Bo Nickal",R),("AG-15","Payton Talbott",R),
        ("AG-16","Stipe Miocic",R),("AG-17","Kamaru Usman",R),("AG-18","Max Holloway",R),
        ("AG-19","Diego Lopes",R),("AG-20","Colby Covington",R),("AG-21","Shavkat Rakhmonov",R),
        ("AG-22","Zhu Rong",T),("AG-23","Khabib Nurmagomedov",R),("AG-24","Iasmin Lucindo",R),
        ("AG-25","Belal Muhammad",R),("AG-26","Dricus Du Plessis",R),("AG-27","Wang Cong",T),
        ("AG-28","Alexa Grasso",R),("AG-29","Valentina Shevchenko",R),("AG-30","Alexander Volkanovski",R),
    ]),
    ("Manifesting Moments", [
        ("MM-1","Tom Aspinall",R),("MM-2","Magomed Ankalaev",R),("MM-3","Conor McGregor",R),
        ("MM-4","Joshua Van",R),("MM-5","Kayla Harrison",R),("MM-6","Max Holloway",R),
        ("MM-7","Zhang Weili",R),("MM-8","Jack Della Maddalena",R),("MM-9","Alex Pereira",R),
        ("MM-10","Reinier De Ridder",R),
    ]),
    ("In Your Face", [
        ("IYF-1","Tom Aspinall",R),("IYF-2","Reinier De Ridder",R),("IYF-3","Bo Nickal",R),
        ("IYF-4","Michael Chandler",R),("IYF-5","Rei Tsuruya",T),("IYF-6","Sean O'Malley",R),
        ("IYF-7","Caio Borralho",R),("IYF-8","Jon Jones",R),("IYF-9","Sean Strickland",R),
        ("IYF-10","Chuck Liddell",R),("IYF-11","Zhang Weili",R),("IYF-12","Israel Adesanya",R),
        ("IYF-13","Alexander Volkanovski",R),("IYF-14","Justin Gaethje",R),
        ("IYF-15","Joanna Jędrzejczyk",R),
    ]),
    ("Impact Point", [
        ("IP-1","Alex Pereira",R),("IP-2","Tom Nolan",T),("IP-3","Shavkat Rakhmonov",R),
        ("IP-4","Manon Fiorot",R),("IP-5","Oumar Sy",T),("IP-6","Tom Aspinall",R),
        ("IP-7","Diego Lopes",R),("IP-8","Dricus Du Plessis",R),("IP-9","Sean Strickland",R),
        ("IP-10","Tatsuro Taira",R),("IP-11","Payton Talbott",R),("IP-12","Zhu Rong",T),
        ("IP-13","Max Holloway",R),("IP-14","Patricio Freire",T),("IP-15","Bo Nickal",R),
        ("IP-16","Magomed Ankalaev",R),("IP-17","JJ Aldrich",T),("IP-18","Zhang Weili",R),
        ("IP-19","Michael Page",R),("IP-20","Michael Parkin",T),
    ]),
    ("Immortal Force", [
        ("IF-1","Sean O'Malley",R),("IF-2","Ilia Topuria",R),("IF-3","Dricus Du Plessis",R),
        ("IF-4","Jon Jones",R),("IF-5","Merab Dvalishvili",R),("IF-6","Derrick Lewis",R),
        ("IF-7","Alexander Volkanovski",R),("IF-8","Alex Pereira",R),("IF-9","Zhang Weili",R),
        ("IF-10","Charles Oliveira",R),("IF-11","Justin Gaethje",R),("IF-12","Dustin Poirier",R),
        ("IF-13","Amanda Nunes",R),("IF-14","Chuck Liddell",R),("IF-15","Jack Della Maddalena",R),
        ("IF-16","Conor McGregor",R),("IF-17","Israel Adesanya",R),("IF-18","Anderson Silva",R),
        ("IF-19","Tom Aspinall",R),("IF-20","Alexa Grasso",R),("IF-21","Islam Makhachev",R),
        ("IF-22","Khabib Nurmagomedov",R),("IF-23","Kamaru Usman",R),("IF-24","Max Holloway",R),
        ("IF-25","Daniel Cormier",R),("IF-26","Sean Strickland",R),("IF-27","Alexandre Pantoja",R),
        ("IF-28","José Aldo",R),("IF-29","Kayla Harrison",R),("IF-30","Georges St-Pierre",R),
    ]),
    ("Radiating Rookies", [
        ("RR-1","Youssef Zalal",T),("RR-2","JJ Aldrich",T),("RR-3","Rafael Estevam",T),
        ("RR-4","David Onama",T),("RR-5","Oumar Sy",T),("RR-6","Rizvan Kuniev",T),
        ("RR-7","Wang Cong",T),("RR-8","Aleksandre Topuria",T),("RR-9","Jacqueline Cavalcanti",T),
        ("RR-10","Zhu Rong",T),("RR-11","Ramazan Temirov",T),("RR-12","Fatima Kline",T),
        ("RR-13","Nora Cornolle",T),("RR-14","Tom Nolan",T),("RR-15","Patricio Freire",T),
        ("RR-16","Rei Tsuruya",T),("RR-17","Mingyang Zhang",T),("RR-18","Michael Parkin",T),
        ("RR-19","Felipe Lima",T),("RR-20","Tallison Teixeira",T),
    ]),
    ("Kings and Queens", [
        ("KQ-1","Mauricio Santos",R),("KQ-2","Kayla Harrison",R),("KQ-3","Jon Jones",R),
        ("KQ-4","Nora Cornolle",T),("KQ-5","Alexander Volkanovski",R),("KQ-6","Zhang Weili",R),
        ("KQ-7","Charles Oliveira",R),("KQ-8","Natalia Cristina da Silva",R),
        ("KQ-9","Alexandre Pantoja",R),("KQ-10","Ilia Topuria",R),("KQ-11","Conor McGregor",R),
        ("KQ-12","Amanda Nunes",R),("KQ-13","Jack Della Maddalena",R),("KQ-14","Max Holloway",R),
        ("KQ-15","Alex Pereira",R),("KQ-16","Valentina Shevchenko",R),("KQ-17","Magomed Ankalaev",R),
        ("KQ-18","Alexa Grasso",R),("KQ-19","Merab Dvalishvili",R),("KQ-20","Tatiana Suarez",R),
    ]),
    ("Helix", [
        ("HX-1","Ilia Topuria",R),("HX-2","Patricio Freire",T),("HX-3","Merab Dvalishvili",R),
        ("HX-4","Oumar Sy",T),("HX-5","Youssef Zalal",T),("HX-6","Paddy Pimblett",R),
        ("HX-7","Conor McGregor",R),("HX-8","Kayla Harrison",R),("HX-9","Tom Aspinall",R),
        ("HX-10","Rei Tsuruya",T),
    ]),
    ("Hidden Gems", [
        ("HG-1","Conor McGregor",R),("HG-2","Kayla Harrison",R),("HG-3","Tom Aspinall",R),
        ("HG-4","Sean O'Malley",R),("HG-5","Jon Jones",R),
    ]),
    ("Let's Go", [
        ("LG-1","Dustin Poirier",R),("LG-2","Merab Dvalishvili",R),("LG-3","Alex Pereira",R),
        ("LG-4","Alexa Grasso",R),("LG-5","Max Holloway",R),
    ]),
]:
    add_insert_with_parallels(name, cards)

# ─── AUTOGRAPH SUBSETS ───────────────────────────────────────────────────────

def add_auto_set(name, cards, parallels=AUTO_PARALLELS):
    is_id = add_is(name)
    for p_name, p_run in parallels:
        add_parallel(is_id, p_name, p_run)
    add_cards(is_id, cards)
    return is_id

# Base Cards Autograph Variations
bav_cards = [
    ("BAV-AE","Alexia Thainara",T),("BAV-AG","Gautier Ateba",T),("BAV-AH","Anthony Hernandez",R),
    ("BAV-AL","Andre Lima",T),("BAV-AN","Andreas Gustafsson",T),("BAV-AO","Aaron Pico",T),
    ("BAV-AP","Alex Pereira",R),("BAV-AS","Aljamain Sterling",R),("BAV-AT","Arman Tsarukyan",R),
    ("BAV-AU","Austin Vanderford",T),("BAV-AV","Alvin Hines",T),("BAV-AZ","Alex Perez",R),
    ("BAV-BB","Bruna Brasil",T),("BAV-BM","Brandon Moreno",R),("BAV-BN","Bo Nickal",R),
    ("BAV-CC","Colby Covington",R),("BAV-CE","Chang Ho Lee",T),("BAV-CH","Chase Hooper",R),
    ("BAV-CL","Carlos Leal",T),("BAV-CP","Chris Padilla",T),("BAV-CR","Clayton Carpenter",T),
    ("BAV-CS","Cory Sandhagen",R),("BAV-CU","Carlos Ulberg",R),("BAV-DB","Dione Barbosa",T),
    ("BAV-DD","Dricus Du Plessis",R),("BAV-DH","Daniel Hooker",R),("BAV-DI","Dan Ige",R),
    ("BAV-DO","David Onama",T),("BAV-DP","Dustin Poirier",R),("BAV-DS","Daniel Santos",T),
    ("BAV-ES","Elijah Smith",T),("BAV-FL","Felipe Lima",T),("BAV-FM","Francis Marshall",T),
    ("BAV-GR","Gillian Robertson",R),("BAV-GS","Gabriel Santos",T),("BAV-HA","Hyder Amil",T),
    ("BAV-IA","Ibo Aslan",T),("BAV-IL","Iasmin Lucindo",R),("BAV-JA","Jaqueline Amorim",T),
    ("BAV-JC","Jacqueline Cavalcanti",T),("BAV-JD","Jack Della Maddalena",R),
    ("BAV-JE","Josh Emmett",R),("BAV-JH","Jamahal Hill",R),("BAV-JJ","JJ Aldrich",T),
    ("BAV-JM","Jailton Malhadinho",R),("BAV-JS","Joo Sang Yoo",T),("BAV-JV","Jackson McVey",T),
    ("BAV-KF","Kaue Fernandes",T),("BAV-KJ","Khalil Rountree Jr.",R),("BAV-KK","Kai Kara-France",R),
    ("BAV-KR","Karol Rosa",R),("BAV-KS","Kody Steele",T),("BAV-LK","Lone'er Kavanagh",T),
    ("BAV-MA","Mansur Abdul-Malik",T),("BAV-MB","Maycee Barber",R),("BAV-MC","Mark Choinski",T),
    ("BAV-MJ","Montel Jackson",R),("BAV-ML","Michael Aswell",T),("BAV-MM","Marquel Mederos",T),
    ("BAV-MO","Mario Pinto",T),("BAV-MP","Michael Parkin",T),("BAV-MS","Shi Ming",T),
    ("BAV-MT","Marco Silva",T),("BAV-MZ","Marcus Almeida",T),("BAV-NC","Nora Cornolle",T),
    ("BAV-NH","Nasrat Haqparast",T),("BAV-NR","Nursulton Ruziboev",T),("BAV-OE","Oban Elliott",T),
    ("BAV-PL","Patricio Freire",T),("BAV-PP","Paddy Pimblett",R),("BAV-QS","Quillan Salkilld",T),
    ("BAV-RE","Rafael Estevam",T),("BAV-RM","Renato Moicano",R),("BAV-RN","Rose Namajunas",R),
    ("BAV-RT","Rei Tsuruya",T),("BAV-RU","Zhu Rong",T),("BAV-RV","Ramazan Temirov",T),
    ("BAV-RW","Robert Whittaker",R),("BAV-SK","Seok Hyeon Ko",T),("BAV-SR","Shavkat Rakhmonov",R),
    ("BAV-ST","Stephen Thompson",R),("BAV-TA","Talita Alencar",T),("BAV-TF","Torrez Finney",T),
    ("BAV-TN","Tom Nolan",T),("BAV-TR","Tabatha Ricci",R),("BAV-TT","Tallison Teixeira",T),
    ("BAV-UN","Umar Nurmagomedov",R),("BAV-WC","Wang Cong",T),("BAV-YZ","Youssef Zalal",T),
]
add_auto_set("Base Cards Autograph Variations", bav_cards)

# 1986 Topps Signatures
add_auto_set("1986 Topps Signatures", [
    ("86S-BO","Brian Ortega",R),("86S-DL","Diego Lopes",R),("86S-EB","Erin Blanchfield",R),
    ("86S-GN","Geoff Neal",R),("86S-IA","Israel Adesanya",R),("86S-IG","Ian Machado Garry",R),
    ("86S-IR","Irene Aldana",R),("86S-JA","José Aldo",R),("86S-JB","Jan Błachowicz",R),
    ("86S-JG","Justin Gaethje",R),("86S-JW","Johnny Walker",R),("86S-KC","Khamzat Chimaev",R),
    ("86S-KH","Kayla Harrison",R),("86S-KV","Ketlen Vieira",R),("86S-LE","Leon Edwards",R),
    ("86S-MD","Mackenzie Dern",R),("86S-MH","Max Holloway",R),("86S-MV","Marlon Vera",R),
    ("86S-NS","Natalia Cristina da Silva",R),("86S-RP","Raquel Pennington",R),
    ("86S-RR","Raul Rosas",R),("86S-SB","Sean Brady",R),("86S-SO","Sean O'Malley",R),
    ("86S-SP","Sergei Pavlovich",R),("86S-SS","Sean Strickland",R),("86S-TT","Tatsuro Taira",R),
    ("86S-TU","Tai Tuivasa",R),("86S-VJ","Virna Jandiroba",R),("86S-YS","Yadong Song",R),
    ("86S-ZW","Zhang Weili",R),
])

# Chrome Lineage Autographs
add_auto_set("Chrome Lineage Autographs", [
    ("CCA-AA","Arnold Allen",R),("CCA-AG","Alexa Grasso",R),("CCA-AL","Amanda Lemos",R),
    ("CCA-AR","Amanda Ribas",R),("CCA-BR","Brandon Royval",R),("CCA-CB","Caio Borralho",R),
    ("CCA-CM","Conor McGregor",R),("CCA-CO","Charles Oliveira",R),("CCA-CS","Curtis Blaydes",R),
    ("CCA-DF","Deiveson Figueiredo",R),("CCA-GB","Gilbert Burns",R),("CCA-IM","Islam Makhachev",R),
    ("CCA-IT","Ilia Topuria",R),("CCA-JP","Jiri Prochazka",R),("CCA-KH","Kevin Holland",R),
    ("CCA-LM","Lerone Murphy",R),("CCA-MA","Macy Chiasson",R),("CCA-MB","Mayra Bueno",R),
    ("CCA-MC","Michael Chandler",R),("CCA-MF","Manon Fiorot",R),("CCA-MK","Manel Kape",R),
    ("CCA-MM","Michael Morales",R),("CCA-MP","Michael Page",R),("CCA-MR","Marina Rodriguez",R),
    ("CCA-NI","Nassourdine Imavov",R),("CCA-RD","Roman Dolidze",R),
    ("CCA-SM","Sharabutdin Magomedov",R),("CCA-TS","Tatiana Suarez",R),("CCA-YX","Yan Xiaonan",R),
])

# Marks of Champions
add_auto_set("Marks of Champions", [
    ("MOC-AP","Alexandre Pantoja",R),("MOC-AV","Alexander Volkanovski",R),
    ("MOC-BM","Belal Muhammad",R),("MOC-DC","Daniel Cormier",R),("MOC-JJ","Jon Jones",R),
    ("MOC-JP","Julianna Peña",R),("MOC-MA","Magomed Ankalaev",R),("MOC-MD","Merab Dvalishvili",R),
    ("MOC-TA","Tom Aspinall",R),("MOC-VS","Valentina Shevchenko",R),
])

# Octagon Legends Autographs
add_auto_set("Octagon Legends Autographs", [
    ("OLA-AN","Amanda Nunes",R),("OLA-AS","Anderson Silva",R),("OLA-BJ","BJ Penn",R),
    ("OLA-CL","Chuck Liddell",R),("OLA-DR","Dominick Reyes",R),("OLA-DW","Dana White",R),
    ("OLA-GS","Georges St-Pierre",R),("OLA-KN","Khabib Nurmagomedov",R),("OLA-MK","Mark Kerr",R),
    ("OLA-SM","Stipe Miocic",R),
])

# Future Stars Autographs
add_auto_set("Future Stars Autographs", [
    ("FSA-AA","Assu Almabayev",R),("FSA-AP","Ailin Perez",R),("FSA-BG","Bogdan Guskov",R),
    ("FSA-CP","Carlos Prates",R),("FSA-DZ","Daniel Zellhuber",R),("FSA-JB","Joaquin Buckley",R),
    ("FSA-JM","Jean Matsumoto",R),("FSA-JP","Joe Pyfer",R),("FSA-JS","Jean Silva",R),
    ("FSA-JV","Joshua Van",R),("FSA-KA","Kai Asakura",R),("FSA-MS","Mauricio Santos",R),
    ("FSA-ND","Norma Dumont",R),("FSA-PT","Payton Talbott",R),("FSA-RK","Roman Kopylov",R),
    ("FSA-RR","Reinier de Ridder",R),("FSA-SE","Stephen Erceg",R),("FSA-SG","Shamil Gaziev",R),
    ("FSA-VO","Vinicius Oliveira",R),("FSA-WC","Waldo Cortes",R),
])

# Quoted Autographs
add_auto_set("Quoted Autographs", [
    ("QA-AG","Alexa Grasso",R),("QA-AV","Alexander Volkanovski",R),("QA-BR","Brandon Royval",R),
    ("QA-CB","Caio Borralho",R),("QA-CC","Colby Covington",R),("QA-DC","Daniel Cormier",R),
    ("QA-DL","Diego Lopes",R),("QA-DP","Dustin Poirier",R),("QA-DW","Dana White",R),
    ("QA-IA","Israel Adesanya",R),("QA-IG","Ian Machado Garry",R),("QA-JG","Justin Gaethje",R),
    ("QA-JJ","Jon Jones",R),("QA-JP","Jiri Prochazka",R),("QA-MD","Merab Dvalishvili",R),
    ("QA-MH","Max Holloway",R),("QA-PP","Paddy Pimblett",R),("QA-RN","Rose Namajunas",R),
    ("QA-RR","Raul Rosas",R),("QA-SO","Sean O'Malley",R),
])

# Topps 2009 Variation Signatures
add_auto_set("Topps 2009 Variation Signatures", [
    ("09-AA","Alexandre Pantoja",R),("09-AP","Alex Pereira",R),("09-AS","Aljamain Sterling",R),
    ("09-AT","Arman Tsarukyan",R),("09-BM","Belal Muhammad",R),("09-CH","Chase Hooper",R),
    ("09-CU","Carlos Ulberg",R),("09-DD","Dricus Du Plessis",R),("09-DH","Daniel Hooker",R),
    ("09-EB","Erin Blanchfield",R),("09-IM","Islam Makhachev",R),("09-JD","Jack Della Maddalena",R),
    ("09-KA","Kai Asakura",R),("09-KC","Khamzat Chimaev",R),("09-KH","Kayla Harrison",R),
    ("09-KN","Khabib Nurmagomedov",R),("09-MA","Magomed Ankalaev",R),("09-MB","Maycee Barber",R),
    ("09-MF","Manon Fiorot",R),("09-MS","Mauricio Santos",R),("09-NI","Nassourdine Imavov",R),
    ("09-PP","Patricio Freire",T),("09-PY","Petr Yan",R),("09-RR","Reinier De Ridder",R),
    ("09-SS","Sean Strickland",R),("09-TA","Tom Aspinall",R),("09-TS","Tatiana Suarez",R),
    ("09-VS","Valentina Shevchenko",R),
])

# Vanquisher Ink
add_auto_set("Vanquisher Ink", [
    ("VI-AN","Arnold Allen",R),("VI-AP","Aaron Pico",T),("VI-AR","Aleksandar Rakic",R),
    ("VI-AS","Anderson Silva",R),("VI-AV","Alexander Volkov",R),("VI-BM","Brandon Moreno",R),
    ("VI-BN","Bo Nickal",R),("VI-CL","Chuck Liddell",R),("VI-CM","Conor McGregor",R),
    ("VI-CP","Carlos Prates",R),("VI-DO","David Onama",T),("VI-GS","Georges St-Pierre",R),
    ("VI-JA","José Aldo",R),("VI-JB","Joaquin Buckley",R),("VI-JC","Jacqueline Cavalcanti",T),
    ("VI-JM","Jailton Malhadinho",R),("VI-JP","Julianna Peña",R),("VI-JS","Jean Silva",R),
    ("VI-JZ","Jan Błachowicz",R),("VI-KH","Kevin Holland",R),("VI-KK","Kai Kara-France",R),
    ("VI-KV","Ketlen Vieira",R),("VI-LE","Leon Edwards",R),("VI-MC","Michael Chandler",R),
    ("VI-MD","Mackenzie Dern",R),("VI-ME","Movsar Evloev",R),("VI-MK","Manel Kape",R),
    ("VI-MM","Michael Morales",R),("VI-MN","Michael Parkin",T),("VI-MP","Michael Page",R),
    ("VI-ND","Norma Dumont",R),("VI-PT","Payton Talbott",R),("VI-RA","Rei Tsuruya",T),
    ("VI-RP","Raquel Pennington",R),("VI-RT","Ramazan Temirov",T),("VI-RW","Robert Whittaker",R),
    ("VI-SB","Sean Brady",R),("VI-SP","Sergei Pavlovich",R),("VI-TA","Tallison Teixeira",T),
    ("VI-TT","Tatsuro Taira",R),("VI-UN","Umar Nurmagomedov",R),("VI-VJ","Virna Jandiroba",R),
    ("VI-YX","Yan Xiaonan",R),("VI-YZ","Youssef Zalal",T),
])

# ─── Generate slugs ──────────────────────────────────────────────────────────
def slugify(text):
    s = text.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_]+', '-', s)
    return re.sub(r'-+', '-', s).strip('-')

rows = db.execute("SELECT id, name FROM players WHERE set_id = ? AND slug IS NULL", (SET_ID,)).fetchall()
existing = set(r[0] for r in db.execute("SELECT slug FROM players WHERE set_id = ? AND slug IS NOT NULL", (SET_ID,)).fetchall())
for pid, pname in rows:
    slug = slugify(pname)
    if slug in existing:
        i = 2
        while f"{slug}-{i}" in existing: i += 1
        slug = f"{slug}-{i}"
    existing.add(slug)
    db.execute("UPDATE players SET slug = ? WHERE id = ?", (slug, pid))

db.commit()

# ─── Summary ─────────────────────────────────────────────────────────────────
player_count = db.execute("SELECT COUNT(*) FROM players WHERE set_id = ?", (SET_ID,)).fetchone()[0]
app_count = db.execute("SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON pa.insert_set_id = i.id WHERE i.set_id = ?", (SET_ID,)).fetchone()[0]
is_count = db.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id = ?", (SET_ID,)).fetchone()[0]
par_count = db.execute("SELECT COUNT(*) FROM parallels WHERE insert_set_id IN (SELECT id FROM insert_sets WHERE set_id = ?)", (SET_ID,)).fetchone()[0]
co_count = db.execute("SELECT COUNT(*) FROM appearance_co_players ac JOIN player_appearances pa ON pa.id = ac.appearance_id JOIN insert_sets i ON i.id = pa.insert_set_id WHERE i.set_id = ?", (SET_ID,)).fetchone()[0]

print(f"\nDone! Set ID: {SET_ID}")
print(f"  Players: {player_count}")
print(f"  Appearances: {app_count}")
print(f"  Insert sets: {is_count}")
print(f"  Parallels: {par_count}")
print(f"  Co-player links: {co_count}")
db.close()
