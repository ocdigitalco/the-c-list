"""
Seed: 2025-26 Topps Chrome UEFA Women's Champions League — Full checklist.
100 base (95 vets/rookies + 5 Future Stars), 10 insert subsets, 5 auto subsets,
2 auto-relic subsets. Parallels pending sell sheet.
Usage: python3 scripts/seed_chrome_uwcl_2025.py
"""
import sqlite3, os, json, re, unicodedata

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
db = sqlite3.connect(DB_PATH)
db.execute("PRAGMA journal_mode=WAL")
db.execute("PRAGMA foreign_keys=ON")

# ─── Create Set ──────────────────────────────────────────────────────────────
# TODO: Parallels (Pulsar Refractor, Base Refractor, numbered ladder) pending sell sheet
# TODO: boxes_per_case is TBA
box_config = json.dumps({
    "hobby": {
        "cards_per_pack": 4,
        "packs_per_box": 20,
        "boxes_per_case": None,
        "notes": "Per box: 2 autographs + 3 Pulsar Refractors + 6 Base Refractors + 5 numbered parallels"
    }
})

db.execute("""
    INSERT INTO sets (name, sport, season, tier, slug, is_visible,
                      sample_image_url, release_date, box_config, created_at)
    VALUES ('2025-26 Topps Chrome UEFA Women''s Champions League', 'Soccer', '2025-26', 'Chrome',
            '2025-26-topps-chrome-uefa-womens-champions-league', 1,
            '/sets/2025-26-topps-chrome-uefa-womens-champions-league.jpg', '2026-05-19', ?, '2026-05-19T12:00:00Z')
""", (box_config,))
SET_ID = db.execute("SELECT last_insert_rowid()").fetchone()[0]
print(f"Created set ID: {SET_ID}")

def slugify(text):
    s = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    s = s.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_]+', '-', s)
    return re.sub(r'-+', '-', s).strip('-')

def get_or_create(name, role="athlete"):
    row = db.execute("SELECT id FROM players WHERE set_id = ? AND name = ?", (SET_ID, name)).fetchone()
    if row: return row[0]
    slug = slugify(name)
    # Handle slug collisions within set
    existing = set(r[0] for r in db.execute("SELECT slug FROM players WHERE set_id = ? AND slug IS NOT NULL", (SET_ID,)).fetchall())
    candidate = slug
    i = 2
    while candidate in existing:
        candidate = f"{slug}-{i}"
        i += 1
    db.execute("INSERT INTO players (set_id, name, slug, unique_cards, total_print_run, one_of_ones, insert_set_count, subject_role) VALUES (?, ?, ?, 0, 0, 0, 0, ?)",
               (SET_ID, name, candidate, role))
    return db.execute("SELECT last_insert_rowid()").fetchone()[0]

def add_is(name, is_auto=False):
    db.execute("INSERT INTO insert_sets (set_id, name, is_autograph) VALUES (?, ?, ?)", (SET_ID, name, 1 if is_auto else 0))
    return db.execute("SELECT last_insert_rowid()").fetchone()[0]

def add_cards(is_id, cards):
    """cards = list of (card_num, name, team, is_rookie)"""
    for num, name, team, rookie in cards:
        pid = get_or_create(name)
        db.execute(
            "INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)",
            (pid, is_id, str(num), 1 if rookie else 0, team))

def add_dual_cards(is_id, cards):
    for num, n1, n2 in cards:
        pid1 = get_or_create(n1)
        pid2 = get_or_create(n2)
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, NULL)", (pid1, is_id, str(num)))
        a_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a_id, pid2))

def add_triple_cards(is_id, cards):
    for num, n1, n2, n3 in cards:
        pid1 = get_or_create(n1)
        pid2 = get_or_create(n2)
        pid3 = get_or_create(n3)
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, NULL)", (pid1, is_id, str(num)))
        a_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a_id, pid2))
        db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a_id, pid3))

R = True
F = False

# ─── BASE: Veterans and Rookies (95 cards) ──────────────────────────────────
base_id = add_is("Base Set")
base_cards = [
    (1,"Jule Brand","OL Lyonnes",F),(2,"Georgia Stanway","FC Bayern München",F),
    (3,"Ewa Pajor","FC Barcelona",F),(4,"Leah Williamson","Arsenal FC",F),
    (5,"Kadidiatou Diani","OL Lyonnes",F),(6,"Lindsey Heaps","OL Lyonnes",F),
    (7,"Florianne Jourde","Paris Saint-Germain",R),(8,"Ada Hegerberg","OL Lyonnes",F),
    (9,"Veerle Buurman","Chelsea FC",R),(10,"Athenea del Castillo","Real Madrid C.F.",F),
    (11,"Alexia Putellas","FC Barcelona",F),(12,"Chloe Kelly","Arsenal FC",F),
    (13,"Momoko Tanikawa","FC Bayern München",R),(14,"Aitana Bonmatí","FC Barcelona",F),
    (15,"Chloe Sarwie","Chelsea FC",R),(16,"Olivia Smith","Arsenal FC",R),
    (17,"Melvine Malard","Manchester United",F),(18,"Alyssa Thompson","Chelsea FC",F),
    (19,"Aggie Beever-Jones","Chelsea FC",F),(20,"Sam Kerr","Chelsea FC",F),
    (21,"Naomi Girma","Chelsea FC",F),(22,"Clàudia Pina","FC Barcelona",F),
    (23,"Aurélie Reynders","Oud-Heverlee Leuven",R),(24,"Guro Reiten","Chelsea FC",F),
    (25,"Eva Navarro","Real Madrid C.F.",F),(26,"Patri Guijarro","FC Barcelona",F),
    (27,"Janou Levels","VfL Wolfsburg",R),(28,"Korbin Shrader","OL Lyonnes",F),
    (29,"Jess Park","Manchester United",F),(30,"Caroline Graham Hansen","FC Barcelona",F),
    (31,"Clara Serrajordi","FC Barcelona",R),(32,"Lineth Beerensteyn","VfL Wolfsburg",F),
    (33,"Lauren James","Chelsea FC",F),(34,"Lena Oberdorf","FC Bayern München",F),
    (35,"Merveille Kanjinga","Paris Saint-Germain",R),(36,"Olga Carmona","Paris Saint-Germain",F),
    (37,"Lily Yohannes","OL Lyonnes",F),(38,"Bella Andersson","Real Madrid C.F.",R),
    (39,"Kika Nazareth","FC Barcelona",F),(40,"Giulia Galli","AS Roma",R),
    (41,"Melchie Dumornay","OL Lyonnes",F),(42,"Sophie Proost","F.C. Twente",R),
    (45,"Pernille Harder","FC Bayern München",F),(46,"Vicky López","FC Barcelona",F),
    (47,"Manuela Giugliano","AS Roma",F),(48,"Kadhiya de Ceuster","Oud-Heverlee Leuven",R),
    (49,"Rasheedat Ajibade","Paris Saint-Germain",F),(50,"Julie Biesmans","Oud-Heverlee Leuven",F),
    (51,"Giulia Gwinn","FC Bayern München",F),(52,"Maeline Mendy","Paris FC",R),
    (53,"Liana Joseph","OL Lyonnes",R),(54,"Wendie Renard","OL Lyonnes",F),
    (56,"Eva Oude Elberink","F.C. Twente",R),(57,"Kim Little","Arsenal FC",F),
    (58,"Jayde Riviere","Manchester United",R),(59,"Clara Mateo","Paris FC",F),
    (60,"Cristiana Girelli","Juventus",F),(61,"Barbara Bonansea","Juventus",F),
    (62,"Kessya Bussy","VfL Wolfsburg",R),(63,"Linda Caicedo","Real Madrid C.F.",F),
    (64,"Cora Zicai","VfL Wolfsburg",R),(65,"Frida Maanum","Arsenal FC",F),
    (66,"Lea Schüller","Manchester United",F),(67,"Sandy Baltimore","Chelsea FC",F),
    (68,"Irene Paredes","FC Barcelona",F),(69,"Aïcha Camara","FC Barcelona",R),
    (70,"Lia Wälti","Juventus",F),(71,"Elisabeth Terland","Manchester United",R),
    (72,"Romée Leuchter","Paris Saint-Germain",F),(73,"Rose Ivens","F.C. Twente",R),
    (74,"Chiara Beccari","Juventus",F),(75,"Fridolina Rolfö","Manchester United",F),
    (76,"Alexandra Popp","VfL Wolfsburg",F),(77,"Catarina Macario","Chelsea FC",F),
    (78,"Flo Hermans","Oud-Heverlee Leuven",R),(79,"Katie McCabe","Arsenal FC",F),
    (80,"Mariona Caldentey","Arsenal FC",F),(81,"Maya Le Tissier","Manchester United",F),
    (83,"Mayra Ramírez","Chelsea FC",F),(84,"Janina Minge","VfL Wolfsburg",F),
    (85,"Alice Corelli","AS Roma",F),(86,"Alara Şehitler","FC Bayern München",F),
    (87,"Caroline Weir","Real Madrid C.F.",F),(88,"Salma Paralluelo","FC Barcelona",F),
    (90,"Selma Bacha","OL Lyonnes",F),(91,"Hinata Miyazawa","Manchester United",F),
    (92,"Klara Bühl","FC Bayern München",F),(93,"Iris Santiago","Real Madrid C.F.",R),
    (94,"Alessia Russo","Arsenal FC",F),(95,"Stina Blackstenius","Arsenal FC",F),
    (96,"Jill Roord","F.C. Twente",F),(97,"Kenza Roche-Dufour","Paris FC",R),
    (98,"Marie-Antoinette Katoto","OL Lyonnes",F),(99,"Ella Toone","Manchester United",F),
    (100,"Beth Mead","Arsenal FC",F),
]
add_cards(base_id, base_cards)
print(f"  Base Set: {len(base_cards)} cards")

# ─── BASE: Future Stars (5 cards) ──────────────────────────────────────────
fs_id = add_is("Future Stars")
fs_cards = [
    (43,"Wieke Kaptein","Chelsea FC",F),(44,"Paula Comendador","Real Madrid C.F.",F),
    (55,"Sydney Schertenleib","FC Barcelona",F),(82,"Eva Schatzer","Juventus",F),
    (89,"Irune Dorado","Real Madrid C.F.",F),
]
add_cards(fs_id, fs_cards)
print(f"  Future Stars: {len(fs_cards)} cards")

# ─── INSERT SUBSETS ─────────────────────────────────────────────────────────
def add_insert(name, cards):
    is_id = add_is(name)
    add_cards(is_id, cards)
    print(f"  {name}: {len(cards)} cards")

add_insert("Poetic Precision", [
    ("P-1","Aitana Bonmatí","FC Barcelona",F),("P-2","Lily Yohannes","OL Lyonnes",F),
    ("P-3","Olivia Smith","Arsenal FC",R),("P-4","Sandy Baltimore","Chelsea FC",F),
    ("P-5","Hinata Miyazawa","Manchester United",F),("P-6","Giulia Gwinn","FC Bayern München",F),
    ("P-7","Romée Leuchter","Paris Saint-Germain",F),("P-8","Alexandra Popp","VfL Wolfsburg",F),
    ("P-9","Linda Caicedo","Real Madrid C.F.",F),("P-10","Barbara Bonansea","Juventus",F),
])

add_insert("Finals Destination", [
    ("FD-1","Sophie Proost","F.C. Twente",R),("FD-2","Patri Guijarro","FC Barcelona",F),
    ("FD-3","Filippa Angeldahl","Real Madrid C.F.",F),("FD-4","Olga Carmona","Paris Saint-Germain",F),
    ("FD-5","Frida Maanum","Arsenal FC",F),("FD-6","Caitlin Foord","Arsenal FC",F),
    ("FD-7","Hannah Hampton","Chelsea FC",F),("FD-8","Veerle Buurman","Chelsea FC",R),
    ("FD-9","Jess Park","Manchester United",F),("FD-10","Ada Hegerberg","OL Lyonnes",F),
    ("FD-11","Kadidiatou Diani","OL Lyonnes",F),("FD-12","Georgia Stanway","FC Bayern München",F),
    ("FD-13","Maeline Mendy","Paris FC",R),("FD-14","Janou Levels","VfL Wolfsburg",R),
    ("FD-15","Bella Andersson","Real Madrid C.F.",R),("FD-16","Vicky López","FC Barcelona",F),
    ("FD-17","Barbara Bonansea","Juventus",F),("FD-18","Giulia Dragoni","AS Roma",F),
    ("FD-19","Alara Şehitler","FC Bayern München",F),("FD-20","Aurélie Reynders","Oud-Heverlee Leuven",R),
])

add_insert("Queens of Football", [
    ("QF-1","Mapi León","FC Barcelona",F),("QF-2","Emily Fox","Arsenal FC",F),
    ("QF-3","Ewa Pajor","FC Barcelona",F),("QF-4","Caroline Weir","Real Madrid C.F.",F),
    ("QF-5","Ashley Lawrence","OL Lyonnes",F),("QF-6","María Méndez","Real Madrid C.F.",R),
    ("QF-7","Lineth Beerensteyn","VfL Wolfsburg",F),("QF-8","Mariona Caldentey","Arsenal FC",F),
    ("QF-9","Chloe Kelly","Arsenal FC",F),("QF-10","Aggie Beever-Jones","Chelsea FC",F),
    ("QF-11","Alexia Putellas","FC Barcelona",F),("QF-12","Naomi Girma","Chelsea FC",F),
    ("QF-13","Maya Le Tissier","Manchester United",F),("QF-14","Ella Toone","Manchester United",F),
    ("QF-15","Melvine Malard","Manchester United",F),("QF-16","Klara Bühl","FC Bayern München",F),
    ("QF-17","Lia Wälti","Juventus",F),("QF-18","Jule Brand","OL Lyonnes",F),
    ("QF-19","Athenea del Castillo","Real Madrid C.F.",F),("QF-20","Sakina Karchaoui","Paris Saint-Germain",F),
    ("QF-21","Clara Mateo","Paris FC",F),("QF-22","Alexandra Popp","VfL Wolfsburg",F),
    ("QF-23","Alessia Russo","Arsenal FC",F),("QF-24","Lena Oberdorf","FC Bayern München",F),
    ("QF-25","Mayra Ramírez","Chelsea FC",F),("QF-26","Marie-Antoinette Katoto","OL Lyonnes",F),
    ("QF-27","Cristiana Girelli","Juventus",F),("QF-28","Lindsey Heaps","OL Lyonnes",F),
    ("QF-29","Jill Roord","F.C. Twente",F),("QF-30","Julie Biesmans","Oud-Heverlee Leuven",F),
])

add_insert("Inside Look", [
    ("IL-1","Esmee Brugts","FC Barcelona",F),("IL-2","Beth Mead","Arsenal FC",F),
    ("IL-3","Alba Redondo","Real Madrid C.F.",F),("IL-4","Lucy Bronze","Chelsea FC",F),
    ("IL-5","Frida Maanum","Arsenal FC",F),("IL-6","Celin Bizet","Manchester United",R),
    ("IL-7","Katie McCabe","Arsenal FC",F),("IL-8","Sam Kerr","Chelsea FC",F),
    ("IL-9","Korbin Shrader","OL Lyonnes",F),("IL-10","Johanna Rytting Kaneryd","Chelsea FC",F),
    ("IL-11","Jayde Riviere","Manchester United",R),("IL-12","Merveille Kanjinga","Paris Saint-Germain",R),
    ("IL-13","Ada Hegerberg","OL Lyonnes",F),("IL-14","Giulia Galli","AS Roma",R),
    ("IL-15","Selma Bacha","OL Lyonnes",F),("IL-16","Romée Leuchter","Paris Saint-Germain",F),
    ("IL-17","Sara Däbritz","Real Madrid C.F.",F),("IL-18","Kenza Roche-Dufour","Paris FC",R),
    ("IL-19","Chiara Beccari","Juventus",F),("IL-20","Caroline Graham Hansen","FC Barcelona",F),
])

add_insert("Dreamballer", [
    ("DB-1","Kadhiya de Ceuster","Oud-Heverlee Leuven",R),("DB-2","Clara Serrajordi","FC Barcelona",R),
    ("DB-3","Eva Navarro","Real Madrid C.F.",F),("DB-4","Kessya Bussy","VfL Wolfsburg",R),
    ("DB-5","Leah Williamson","Arsenal FC",F),("DB-6","Rasheedat Ajibade","Paris Saint-Germain",F),
    ("DB-7","Melchie Dumornay","OL Lyonnes",F),("DB-8","Lauren James","Chelsea FC",F),
    ("DB-9","Fridolina Rolfö","Manchester United",F),("DB-10","Clàudia Pina","FC Barcelona",F),
    ("DB-11","Pernille Harder","FC Bayern München",F),("DB-12","Liana Joseph","OL Lyonnes",R),
    ("DB-13","Keira Walsh","Chelsea FC",F),("DB-14","Florianne Jourde","Paris Saint-Germain",R),
    ("DB-15","Iris Santiago","Real Madrid C.F.",R),("DB-16","Janina Minge","VfL Wolfsburg",F),
    ("DB-17","Lena Oberdorf","FC Bayern München",F),("DB-18","Chloe Kelly","Arsenal FC",F),
    ("DB-19","Elisabeth Terland","Manchester United",R),("DB-20","Alice Corelli","AS Roma",F),
])

add_insert("Helix", [
    ("H-1","Alexia Putellas","FC Barcelona",F),("H-2","Olivia Smith","Arsenal FC",R),
    ("H-3","Lily Yohannes","OL Lyonnes",F),("H-4","Momoko Tanikawa","FC Bayern München",R),
    ("H-5","Alyssa Thompson","Chelsea FC",F),
])

add_insert("Arise", [
    ("A-1","Maya Le Tissier","Manchester United",F),("A-2","Pernille Harder","FC Bayern München",F),
    ("A-3","Clara Serrajordi","FC Barcelona",R),("A-4","Caroline Weir","Real Madrid C.F.",F),
    ("A-5","Leah Williamson","Arsenal FC",F),("A-6","Melchie Dumornay","OL Lyonnes",F),
    ("A-7","Olivia Smith","Arsenal FC",R),("A-8","Aurélie Reynders","Oud-Heverlee Leuven",R),
    ("A-9","Iris Santiago","Real Madrid C.F.",R),("A-10","Aggie Beever-Jones","Chelsea FC",F),
    ("A-11","Alessia Russo","Arsenal FC",F),("A-12","Ella Toone","Manchester United",F),
    ("A-13","Ada Hegerberg","OL Lyonnes",F),("A-14","Alexia Putellas","FC Barcelona",F),
    ("A-15","Liana Joseph","OL Lyonnes",R),("A-16","Alexandra Popp","VfL Wolfsburg",F),
    ("A-17","Alyssa Thompson","Chelsea FC",F),("A-18","Momoko Tanikawa","FC Bayern München",R),
    ("A-19","Aitana Bonmatí","FC Barcelona",F),("A-20","Lauren James","Chelsea FC",F),
])

add_insert("Noble One", [
    ("N-1","Alessia Russo","Arsenal FC",F),("N-2","Giulia Gwinn","FC Bayern München",F),
    ("N-3","Hinata Miyazawa","Manchester United",F),("N-4","Stina Blackstenius","Arsenal FC",F),
    ("N-5","Salma Paralluelo","FC Barcelona",F),("N-6","Jule Brand","OL Lyonnes",F),
    ("N-7","Lindsey Heaps","OL Lyonnes",F),("N-8","Clàudia Pina","FC Barcelona",F),
    ("N-9","Naomi Girma","Chelsea FC",F),("N-10","Athenea del Castillo","Real Madrid C.F.",F),
])

add_insert("Oslo at Night", [
    ("OAN-1","Sam Kerr","Chelsea FC",F),("OAN-2","Alexandra Popp","VfL Wolfsburg",F),
    ("OAN-3","Mariona Caldentey","Arsenal FC",F),("OAN-4","Georgia Stanway","FC Bayern München",F),
    ("OAN-5","Lindsey Heaps","OL Lyonnes",F),("OAN-6","Aitana Bonmatí","FC Barcelona",F),
    ("OAN-7","Melchie Dumornay","OL Lyonnes",F),("OAN-8","Sandy Baltimore","Chelsea FC",F),
    ("OAN-9","Caroline Graham Hansen","FC Barcelona",F),("OAN-10","Linda Caicedo","Real Madrid C.F.",F),
])

# UWCL Chrome Trophy — no athlete, use placeholder character
trophy_id = add_is("UWCL Chrome Trophy")
trophy_pid = get_or_create("UWCL Trophy", "character")
db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, 'TRO-1', 0, NULL)",
           (trophy_pid, trophy_id))
print(f"  UWCL Chrome Trophy: 1 card (trophy placeholder)")

# ─── AUTOGRAPH SUBSETS ──────────────────────────────────────────────────────

# Veterans and Rookies Autograph Cards (CA-XX) — 53 cards
ca_id = add_is("Veterans and Rookies Autograph Cards", is_auto=True)
ca_cards = [
    ("CA-AB","Aitana Bonmatí","FC Barcelona",F),("CA-ABJ","Aggie Beever-Jones","Chelsea FC",F),
    ("CA-AD","Athenea del Castillo","Real Madrid C.F.",F),("CA-AH","Ada Hegerberg","OL Lyonnes",F),
    ("CA-AP","Alexia Putellas","FC Barcelona",F),("CA-AR","Alessia Russo","Arsenal FC",F),
    ("CA-AS","Alara Şehitler","FC Bayern München",F),("CA-AT","Alyssa Thompson","Chelsea FC",F),
    ("CA-BB","Barbara Bonansea","Juventus",F),("CA-BM","Beth Mead","Arsenal FC",F),
    ("CA-BU","Klara Bühl","FC Bayern München",F),("CA-CG","Cristiana Girelli","Juventus",F),
    ("CA-CGH","Caroline Graham Hansen","FC Barcelona",F),("CA-CK","Chloe Kelly","Arsenal FC",F),
    ("CA-CM","Catarina Macario","Chelsea FC",F),("CA-CP","Clàudia Pina","FC Barcelona",F),
    ("CA-CS","Clara Serrajordi","FC Barcelona",R),("CA-CW","Caroline Weir","Real Madrid C.F.",F),
    ("CA-CZ","Cora Zicai","VfL Wolfsburg",R),("CA-EP","Ewa Pajor","FC Barcelona",F),
    ("CA-ET","Ella Toone","Manchester United",F),("CA-FR","Fridolina Rolfö","Manchester United",F),
    ("CA-GG","Giulia Gwinn","FC Bayern München",F),("CA-GR","Guro Reiten","Chelsea FC",F),
    ("CA-GS","Georgia Stanway","FC Bayern München",F),("CA-HM","Hinata Miyazawa","Manchester United",F),
    ("CA-JB","Jule Brand","OL Lyonnes",F),("CA-JO","Liana Joseph","OL Lyonnes",R),
    ("CA-JP","Jess Park","Manchester United",F),("CA-KD","Kadidiatou Diani","OL Lyonnes",F),
    ("CA-LC","Linda Caicedo","Real Madrid C.F.",F),("CA-LH","Lindsey Heaps","OL Lyonnes",F),
    ("CA-LJ","Lauren James","Chelsea FC",F),("CA-LO","Lena Oberdorf","FC Bayern München",F),
    ("CA-LS","Lea Schüller","Manchester United",F),("CA-LW","Leah Williamson","Arsenal FC",F),
    ("CA-MC","Mariona Caldentey","Arsenal FC",F),("CA-MD","Melchie Dumornay","OL Lyonnes",F),
    ("CA-MG","Manuela Giugliano","AS Roma",F),("CA-MK","Marie-Antoinette Katoto","OL Lyonnes",F),
    ("CA-ML","Maya Le Tissier","Manchester United",F),("CA-MT","Momoko Tanikawa","FC Bayern München",R),
    ("CA-MY","Mayra Ramírez","Chelsea FC",F),("CA-OS","Olivia Smith","Arsenal FC",R),
    ("CA-PG","Patri Guijarro","FC Barcelona",F),("CA-PH","Pernille Harder","FC Bayern München",F),
    ("CA-POP","Alexandra Popp","VfL Wolfsburg",F),("CA-RL","Romée Leuchter","Paris Saint-Germain",F),
    ("CA-SB","Sandy Baltimore","Chelsea FC",F),("CA-SK","Sam Kerr","Chelsea FC",F),
    ("CA-SP","Salma Paralluelo","FC Barcelona",F),("CA-VL","Vicky López","FC Barcelona",F),
    ("CA-WR","Wendie Renard","OL Lyonnes",F),
]
add_cards(ca_id, ca_cards)
print(f"  Veterans and Rookies Autograph Cards: {len(ca_cards)} cards")

# Future Stars Autograph Cards (FSA-XX) — 4 cards
fsa_id = add_is("Future Stars Autograph Cards", is_auto=True)
fsa_cards = [
    ("FSA-ES","Eva Schatzer","Juventus",F),("FSA-PC","Paula Comendador","Real Madrid C.F.",F),
    ("FSA-SS","Sydney Schertenleib","FC Barcelona",F),("FSA-WK","Wieke Kaptein","Chelsea FC",F),
]
add_cards(fsa_id, fsa_cards)
print(f"  Future Stars Autograph Cards: {len(fsa_cards)} cards")

# Chrome Dual Autograph Cards (DA-XX) — 10 dual-subject
da_id = add_is("Chrome Dual Autograph Cards", is_auto=True)
da_duals = [
    ("DA-BJ","Aggie Beever-Jones","Lauren James"),
    ("DA-CB","Mariona Caldentey","Stina Blackstenius"),
    ("DA-DB","Melchie Dumornay","Jule Brand"),
    ("DA-KD","Marie-Antoinette Katoto","Kadidiatou Diani"),
    ("DA-LB","Vicky López","Aitana Bonmatí"),
    ("DA-LT","Maya Le Tissier","Ella Toone"),
    ("DA-PB","Alexia Putellas","Aitana Bonmatí"),
    ("DA-PP","Ewa Pajor","Clàudia Pina"),
    ("DA-TM","Alyssa Thompson","Catarina Macario"),
    ("DA-WC","Caroline Weir","Linda Caicedo"),
]
add_dual_cards(da_id, da_duals)
print(f"  Chrome Dual Autograph Cards: {len(da_duals)} cards (dual)")

# Chrome Triple Autograph Cards (TA-XX) — 6 triple-subject
ta_id = add_is("Chrome Triple Autograph Cards", is_auto=True)
ta_triples = [
    ("TA-BPG","Aitana Bonmatí","Alexia Putellas","Patri Guijarro"),
    ("TA-BRJ","Aggie Beever-Jones","Mayra Ramírez","Lauren James"),
    ("TA-LPN","Vicky López","Clàudia Pina","Kika Nazareth"),
    ("TA-MBP","Janina Minge","Lineth Beerensteyn","Alexandra Popp"),
    ("TA-PPG","Ewa Pajor","Salma Paralluelo","Caroline Graham Hansen"),
    ("TA-WDC","Caroline Weir","Athenea del Castillo","Linda Caicedo"),
]
add_triple_cards(ta_id, ta_triples)
print(f"  Chrome Triple Autograph Cards: {len(ta_triples)} cards (triple)")

# Queens of Football Autograph Cards (QFA-XX) — 19 cards
qfa_id = add_is("Queens of Football Autograph Cards", is_auto=True)
qfa_cards = [
    ("QFA-AB","Aggie Beever-Jones","Chelsea FC",F),("QFA-AD","Athenea del Castillo","Real Madrid C.F.",F),
    ("QFA-AP","Alexia Putellas","FC Barcelona",F),("QFA-AR","Alessia Russo","Arsenal FC",F),
    ("QFA-CK","Chloe Kelly","Arsenal FC",F),("QFA-CW","Caroline Weir","Real Madrid C.F.",F),
    ("QFA-EP","Ewa Pajor","FC Barcelona",F),("QFA-ET","Ella Toone","Manchester United",F),
    ("QFA-JB","Jule Brand","OL Lyonnes",F),("QFA-JR","Jill Roord","F.C. Twente",F),
    ("QFA-LH","Lindsey Heaps","OL Lyonnes",F),("QFA-LO","Lena Oberdorf","FC Bayern München",F),
    ("QFA-LW","Lia Wälti","Juventus",F),("QFA-MC","Mariona Caldentey","Arsenal FC",F),
    ("QFA-MK","Marie-Antoinette Katoto","OL Lyonnes",F),("QFA-ML","Maya Le Tissier","Manchester United",F),
    ("QFA-MM","Melvine Malard","Manchester United",F),("QFA-PO","Alexandra Popp","VfL Wolfsburg",F),
    ("QFA-SK","Sakina Karchaoui","Paris Saint-Germain",F),
]
add_cards(qfa_id, qfa_cards)
print(f"  Queens of Football Autograph Cards: {len(qfa_cards)} cards")

# ─── AUTO-RELIC SUBSETS ─────────────────────────────────────────────────────

# Official Draw Card Autograph Relics (DCA-XX) — 11 cards
dca_id = add_is("Official Draw Card Autograph Relics", is_auto=True)
dca_cards = [
    ("DCA-AB","Aitana Bonmatí","FC Barcelona",F),("DCA-AD","Athenea del Castillo","Real Madrid C.F.",F),
    ("DCA-LW","Leah Williamson","Arsenal FC",F),("DCA-LJ","Lauren James","Chelsea FC",F),
    ("DCA-LH","Lindsey Heaps","OL Lyonnes",F),("DCA-OC","Olga Carmona","Paris Saint-Germain",F),
    ("DCA-AP","Alexandra Popp","VfL Wolfsburg",F),("DCA-GG","Giulia Gwinn","FC Bayern München",F),
    ("DCA-WA","Lia Wälti","Juventus",F),("DCA-MG","Manuela Giugliano","AS Roma",F),
    ("DCA-JR","Jill Roord","F.C. Twente",F),
]
add_cards(dca_id, dca_cards)
print(f"  Official Draw Card Autograph Relics: {len(dca_cards)} cards")

# Chrome Premium Autograph Relics (CPA-XX) — 23 cards
cpa_id = add_is("Chrome Premium Autograph Relics", is_auto=True)
cpa_cards = [
    ("CPA-AB","Aitana Bonmatí","FC Barcelona",F),("CPA-ABJ","Aggie Beever-Jones","Chelsea FC",F),
    ("CPA-AH","Ada Hegerberg","OL Lyonnes",F),("CPA-AP","Alexia Putellas","FC Barcelona",F),
    ("CPA-AR","Alessia Russo","Arsenal FC",F),("CPA-AT","Alyssa Thompson","Chelsea FC",F),
    ("CPA-CM","Catarina Macario","Chelsea FC",F),("CPA-CP","Clàudia Pina","FC Barcelona",F),
    ("CPA-CW","Caroline Weir","Real Madrid C.F.",F),("CPA-EP","Ewa Pajor","FC Barcelona",F),
    ("CPA-ET","Ella Toone","Manchester United",F),("CPA-GS","Georgia Stanway","FC Bayern München",F),
    ("CPA-JO","Liana Joseph","OL Lyonnes",R),("CPA-LC","Linda Caicedo","Real Madrid C.F.",F),
    ("CPA-LH","Lindsey Heaps","OL Lyonnes",F),("CPA-LJ","Lauren James","Chelsea FC",F),
    ("CPA-LW","Leah Williamson","Arsenal FC",F),("CPA-MC","Mariona Caldentey","Arsenal FC",F),
    ("CPA-MD","Melchie Dumornay","OL Lyonnes",F),("CPA-ML","Maya Le Tissier","Manchester United",F),
    ("CPA-OS","Olivia Smith","Arsenal FC",R),("CPA-PH","Pernille Harder","FC Bayern München",F),
    ("CPA-PO","Alexandra Popp","VfL Wolfsburg",F),
]
add_cards(cpa_id, cpa_cards)
print(f"  Chrome Premium Autograph Relics: {len(cpa_cards)} cards")

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
print(f"Expected: 372 cards")
print(f"0 parallels (pending sell sheet)")
db.close()
print("Done!")
