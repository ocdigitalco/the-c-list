"""
Seed: 2026 Topps Chrome Disney — Full checklist.
200 base, 10 image variations, 27 insert subsets, 4 auto subsets, 1 MLB subset.
Parallels/pack odds pending sell sheet.
Usage: python3 scripts/seed_chrome_disney_2026.py
"""
import sqlite3, os, json, re, unicodedata

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
db = sqlite3.connect(DB_PATH)
db.execute("PRAGMA journal_mode=WAL")
db.execute("PRAGMA foreign_keys=ON")

# ─── Create Set ──────────────────────────────────────────────────────────────
# TODO: Parallels (Pulsar Refractor, X-Fractor, RayWave, numbered ladder) pending sell sheet
# TODO: Pack odds pending sell sheet
# TODO: Value and Mega boxes_per_case TBA
box_config = json.dumps({
    "hobby": {"cards_per_pack": 6, "packs_per_box": 12, "boxes_per_case": 20, "notes": "Per box: TBA"},
    "value": {"cards_per_pack": 4, "packs_per_box": 8, "boxes_per_case": None, "notes": "Per box: 2 RayWave Parallels"},
    "mega": {"cards_per_pack": 7, "packs_per_box": 8, "boxes_per_case": None, "notes": "Per box: 4 X-Fractors"},
})

db.execute("""
    INSERT INTO sets (name, sport, season, tier, slug, is_visible,
                      sample_image_url, release_date, box_config, created_at)
    VALUES ('2026 Topps Chrome Disney', 'Entertainment', '2026', 'Chrome',
            '2026-topps-chrome-disney', 1,
            '/sets/2026-topps-chrome-disney.jpg', '2026-06-17', ?, '2026-05-20T12:00:00Z')
""", (box_config,))
SET_ID = db.execute("SELECT last_insert_rowid()").fetchone()[0]
print(f"Created set ID: {SET_ID}")

def slugify(text):
    s = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    s = s.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_]+', '-', s)
    return re.sub(r'-+', '-', s).strip('-')

_slug_cache = {}
def get_or_create(name, role="character"):
    row = db.execute("SELECT id FROM players WHERE set_id = ? AND name = ?", (SET_ID, name)).fetchone()
    if row: return row[0]
    slug = slugify(name)
    if slug not in _slug_cache:
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

def add_cards(is_id, cards):
    for num, name, team, rookie in cards:
        pid = get_or_create(name)
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)",
                   (pid, is_id, str(num), 1 if rookie else 0, team))

def add_cards_with_tag(is_id, cards):
    """cards = list of (num, name, team, rookie, subset_tag)"""
    for num, name, team, rookie, tag in cards:
        pid = get_or_create(name)
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team, subset_tag) VALUES (?, ?, ?, ?, ?, ?)",
                   (pid, is_id, str(num), 1 if rookie else 0, team, tag))

def add_dual(is_id, cards):
    for num, n1, n2 in cards:
        pid1 = get_or_create(n1)
        pid2 = get_or_create(n2)
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, NULL)", (pid1, is_id, str(num)))
        a = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a, pid2))

def add_triple(is_id, cards):
    for num, n1, n2, n3 in cards:
        pid1, pid2, pid3 = get_or_create(n1), get_or_create(n2), get_or_create(n3)
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, NULL)", (pid1, is_id, str(num)))
        a = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a, pid2))
        db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a, pid3))

def add_quad(is_id, cards):
    for num, n1, n2, n3, n4 in cards:
        pid1, pid2, pid3, pid4 = get_or_create(n1), get_or_create(n2), get_or_create(n3), get_or_create(n4)
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, NULL)", (pid1, is_id, str(num)))
        a = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        for p in [pid2, pid3, pid4]:
            db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a, p))

def ins(name, cards):
    is_id = add_is(name)
    add_cards(is_id, cards)
    print(f"  {name}: {len(cards)} cards")

R = True
F = False

# ─── BASE SET (200 cards) ───────────────────────────────────────────────────
base_id = add_is("Base Set")
base = [
(1,"Snow White","Snow White and the Seven Dwarfs",F),(2,"Evil Queen","Snow White and the Seven Dwarfs",F),
(3,"Mr. Toad","Mr. Toad",F),(4,"Hannah Montana","Hannah Montana",F),
(5,"Mirabel","Encanto",F),(6,"Kirby","Chicken Little",F),
(7,"Alex Russo","Wizards of Waverly Place",F),(8,"Thumper","Bambi",F),
(9,"Flower","Bambi",F),(10,"Moana","Moana 2",F),(11,"Maui","Moana 2",F),
(12,"Matangi","Moana 2",F),(13,"Kotu","Moana 2",R),
(14,"Jack Sparrow","Pirates of the Caribbean: On Stranger Tides",F),
(15,"Blackbeard","Pirates of the Caribbean: On Stranger Tides",F),
(16,"Hector Barbossa","Pirates of the Caribbean: On Stranger Tides",F),
(17,"Emperor Kuzco","The Emperor's New Groove",F),(18,"Kronk","The Emperor's New Groove",F),
(19,"Tex Dinoco","Cars",F),(20,"Lightning McQueen","Cars",F),(21,"Mater","Cars",F),
(22,"Sally","Cars",F),(23,"Guido","Cars",F),(24,"Red","Cars",F),(25,"Fillmore","Cars",F),
(26,"Sheriff","Cars",F),(27,"Chick Hicks","Cars",F),
(28,"Mike Wazowski","Monsters, Inc.",F),(29,"Sulley","Monsters, Inc.",F),
(30,"Quasimodo","The Hunchback of Notre Dame",F),(31,"Esmeralda","The Hunchback of Notre Dame",F),
(32,"Judge Claude Frollo","The Hunchback of Notre Dame",F),(33,"Mitchie Torres","Camp Rock",F),
(34,"Sisu","Raya and the Last Dragon",F),(35,"Belle","Beauty and the Beast",F),
(36,"The Beast","Beauty and the Beast",F),(37,"Gaston","Beauty and the Beast",F),
(38,"Mrs. Potts & Chip","Beauty and the Beast",F),(39,"Wardrobe","Beauty and the Beast",F),
(40,"Basil of Baker Street","The Great Mouse Detective",F),
(41,"Professor Ratigan","The Great Mouse Detective",F),
(42,"Olivia Flaversham","The Great Mouse Detective",F),
(43,"Asha","Wish",F),(44,"Star","Wish",F),
(45,"Tod","The Fox and the Hound",F),(46,"Copper","The Fox and the Hound",F),
(47,"Remy","Ratatouille",F),(48,"Linguini","Ratatouille",F),(49,"Emile","Ratatouille",F),
(50,"Mickey Mouse","Mickey & Friends",F),(51,"Minnie Mouse","Mickey & Friends",F),
(52,"Goofy","Mickey & Friends",F),(53,"Pluto","Mickey & Friends",F),
(54,"Daisy Duck","Mickey & Friends",F),(55,"Kermit the Frog","The Muppets",F),
(56,"Fozzie Bear","The Muppets",F),(57,"Gonzo","The Muppets",F),
(58,"Dr. Bunsen Honeydew","The Muppets",F),(59,"Beaker","The Muppets",F),
(60,"Sam Eagle","The Muppets",F),(61,"Miss Piggy","The Muppets",F),
(62,"Jim Hawkins","Treasure Planet",F),(63,"John Silver","Treasure Planet",F),
(64,"B.E.N.","Treasure Planet",F),(65,"Cruella de Vil","One Hundred and One Dalmatians",F),
(66,"Judy Hopps","Zootopia 2",F),(67,"Nick Wilde","Zootopia 2",F),
(68,"Gary De'Snake","Zootopia 2",R),(69,"Mayor Winddancer","Zootopia 2",R),
(70,"Nibbles Maplestick","Zootopia 2",R),(71,"Pawbert Lynxley","Zootopia 2",R),
(72,"Dr. Fuzzby","Zootopia 2",R),(73,"Robert Furwin","Zootopia 2",R),
(74,"Gazelle","Zootopia 2",F),(75,"Alice","Alice in Wonderland",F),
(76,"Mad Hatter","Alice in Wonderland",F),(77,"Cheshire Cat","Alice in Wonderland",F),
(78,"Caterpillar","Alice in Wonderland",F),(79,"March Hare","Alice in Wonderland",F),
(80,"Doorknob","Alice in Wonderland",F),(81,"Aladdin","Aladdin",F),
(82,"Jasmine","Aladdin",F),(83,"Genie","Aladdin",F),(84,"Jafar","Aladdin",F),
(85,"Dumbo","Dumbo",F),(86,"Timothy Q. Mouse","Dumbo",F),(87,"Mrs. Jumbo","Dumbo",F),
(88,"Nemo","Finding Nemo",F),(89,"Marlin","Finding Nemo",F),(90,"Dory","Finding Nemo",F),
(91,"Crush","Finding Nemo",F),(92,"Nigel","Finding Nemo",F),(93,"Gill","Finding Nemo",F),
(94,"Jacques","Finding Nemo",F),(95,"Pinocchio","Pinocchio (2022)",F),
(96,"Geppetto","Pinocchio (2022)",F),
(97,"José Carioca","The Three Caballeros",F),(98,"Panchito","The Three Caballeros",F),
(99,"Donald Duck","The Three Caballeros",F),(100,"Winnie the Pooh","Winnie the Pooh",F),
(101,"Tigger","Winnie the Pooh",F),(102,"Eeyore","Winnie the Pooh",F),
(103,"Piglet","Winnie the Pooh",F),(104,"Owl","Winnie the Pooh",F),
(105,"Elliott","Pete's Dragon",F),(106,"Ariel","The Little Mermaid",F),
(107,"Sebastian","The Little Mermaid",F),(108,"Ursula","The Little Mermaid",F),
(109,"Lizzie McGuire","Lizzie McGuire",F),
(110,"Mabel Beaver","Hoppers",R),(111,"King George","Hoppers",R),
(112,"Mayor Jerry","Hoppers",R),(113,"Ellen Bear","Hoppers",R),(114,"Tom Lizard","Hoppers",R),
(115,"Phineas","Phineas and Ferb",F),(116,"Ferb","Phineas and Ferb",F),
(117,"Agent P","Phineas and Ferb",F),(118,"Scrooge McDuck","Ducktales",F),
(119,"Huey","Ducktales",F),(120,"Dewey","Ducktales",F),(121,"Louie","Ducktales",F),
(122,"Miguel","Coco",F),(123,"Dante","Coco",F),(124,"Héctor","Coco",F),
(125,"Mamá Coco","Coco",F),(126,"Mr. Incredible","The Incredibles",F),
(127,"Frozone","The Incredibles",F),(128,"Edna Mode","The Incredibles",F),
(129,"Mulan","Mulan",F),(130,"Yao","Mulan",F),(131,"Ling","Mulan",F),
(132,"Chien-Po","Mulan",F),(133,"The Emperor","Mulan",F),
(134,"Wreck-It Ralph","Wreck-It Ralph",F),(135,"Darkwing Duck","Darkwing Duck",F),
(136,"Dug","Up",F),(137,"Kevin","Up",F),(138,"Tiana","The Princess and the Frog",F),
(139,"Dr. Facilier","The Princess and the Frog",F),
(140,"Elio","Elio",F),(141,"Glordon","Elio",F),(142,"Ooooo","Elio",R),
(143,"Baymax","Big Hero 6",F),(144,"Captain B. McCrea","WALL-E",F),
(145,"WALL-E","WALL-E",F),(146,"EVE","WALL-E",F),(147,"M-O","WALL-E",F),
(148,"Ares","Tron: Ares",R),(149,"Lilo","Lilo & Stitch",F),(150,"Stitch","Lilo & Stitch",F),
(151,"Nani","Lilo & Stitch",F),(152,"David Kawena","Lilo & Stitch",F),
(153,"Jumba","Lilo & Stitch",F),(154,"Pleakley","Lilo & Stitch",F),
(155,"Captain Gantu","Lilo & Stitch",F),(156,"Cobra Bubbles","Lilo & Stitch",F),
(157,"Pocahontas","Pocahontas",F),(158,"Giselle","Enchanted",F),
(159,"Prince Edward","Enchanted",F),(160,"Robert Philip","Enchanted",F),
(161,"Dusty Crophopper","Planes",F),(162,"Simba","The Lion King",F),
(163,"Scar","The Lion King",F),(164,"Mufasa","The Lion King",F),
(165,"Peter Pan","Peter Pan",F),(166,"Tinker Bell","Peter Pan",F),
(167,"The Crocodile","Peter Pan",F),(168,"Elsa","Frozen II",F),
(169,"Anna","Frozen II",F),(170,"Olaf","Frozen II",F),
(171,"Joy","Inside Out",F),(172,"Sadness","Inside Out",F),(173,"Anger","Inside Out",F),
(174,"Fear","Inside Out",F),(175,"Disgust","Inside Out",F),(176,"Bing Bong","Inside Out",F),
(177,"Anxiety","Inside Out 2",F),(178,"Nostalgia","Inside Out 2",F),
(179,"Cinderella","Cinderella",F),(180,"Fairy Godmother","Cinderella",F),
(181,"Gus","Cinderella",F),(182,"Troy Bolton","High School Musical",F),
(183,"Gabriella Montez","High School Musical",F),(184,"Sharpay Evans","High School Musical",F),
(185,"Ryan Evans","High School Musical",F),(186,"Chad Danforth","High School Musical",F),
(187,"Taylor McKessie","High School Musical",F),(188,"Rapunzel","Tangled",F),
(189,"Pascal","Tangled",F),(190,"Combat Carl","Toy Story 4",F),
(191,"Melephant Brooks","Toy Story 4",F),(192,"Forky","Toy Story 4",F),
(193,"Karen Beverly","Toy Story 5",R),(194,"Woody","Toy Story 5",F),
(195,"Jessie","Toy Story 5",F),(196,"Atlas","Toy Story 5",R),
(197,"Snappy","Toy Story 5",R),(198,"Smarty Pants","Toy Story 5",R),
(199,"Lilypad","Toy Story 5",R),(200,"Hi-Tech Edition Buzz Lightyear","Toy Story 5",R),
]
add_cards(base_id, base)
print(f"  Base Set: {len(base)} cards")

# ─── BASE CARD IMAGE VARIATIONS (10 cards) ──────────────────────────────────
bcv_id = add_is("Base Card Image Variations")
# Reuse existing character athlete_ids; store variation name in subset_tag
bcv_data = [
    (11, "Maui", "Moana", F, "Mini Maui"),
    (14, "Jack Sparrow", "Pirates of the Caribbean: On Stranger Tides", F, "Captain Jack Sparrow"),
    (17, "Emperor Kuzco", "The Emperor's New Groove", F, "Kuzco"),
    (21, "Mater", "Cars", F, None),
    (47, "Remy", "Ratatouille", F, None),
    (85, "Dumbo", "Dumbo (2019)", F, None),
    (100, "Winnie the Pooh", "Winnie the Pooh", F, None),
    (117, "Agent P", "Phineas and Ferb", F, "Perry the Platypus"),
    (123, "Dante", "Coco", F, "Alebrije Dante"),
    (158, "Giselle", "Enchanted", F, None),
]
add_cards_with_tag(bcv_id, bcv_data)
print(f"  Base Card Image Variations: {len(bcv_data)} cards")

# ─── INSERT SUBSETS ─────────────────────────────────────────────────────────

# Iconic Moments (scenes)
ins("Iconic Moments", [
("IM-1","Be Our Guest","Beauty and the Beast",F),
("IM-2","Cruella's Entrance","One Hundred and One Dalmatians",F),
("IM-3","On Syndrome's Island","The Incredibles",F),
("IM-4","Isn't This a Silly Song?","Snow White and the Seven Dwarfs",F),
("IM-5","A Whole New World","Aladdin",F),
("IM-6","I'm Gonna Go Touch the Butt","Finding Nemo",F),
("IM-7","Restoring the Heart of Te Fiti","Moana",F),
("IM-8","Meet the Scarers","Monsters, Inc.",F),
("IM-9","The Poison. The Poison for Kuzco. The Poison Chosen Specially to Kill Kuzco. Kuzco's Poison.","The Emperor's New Groove",F),
("IM-10","Into the Unknown","Frozen II",F),
("IM-11","Pocahontas Meets John Smith","Pocahontas",F),
("IM-12","Silenzio Bruno","Luca",F),
("IM-13","Speed, I Am Speed","Cars",F),
("IM-14","I'll Make a Man Out of You","Mulan",F),
("IM-15","Hawaiian Roller Coaster Ride","Lilo & Stitch",F),
])

ins("Future Stars", [
("FS-1","Star","Wish",F),("FS-2","Bambi","Bambi",F),("FS-3","Dumbo","Dumbo",F),
("FS-4","Chicken Little","Chicken Little",F),("FS-5","Dopey","Snow White and the Seven Dwarfs",F),
("FS-6","White Rabbit","Alice in Wonderland",F),("FS-7","Koda","Brother Bear",F),
("FS-8","Jaq and Gus","Cinderella",F),("FS-9","Wendy","Peter Pan",F),("FS-10","Russell","Up",F),
])

ins("Scorched", [
("SC-1","Bolt","Bolt",F),("SC-2","Crush","Finding Nemo",F),
("SC-3","Kristoff & Sven","Frozen",F),("SC-4","Pegasus","Hercules",F),("SC-5","Doc Hudson","Cars",F),
])

ins("Super Strength Chrome", [
("ST-1","Mulan","Mulan",F),("ST-2","Baymax","Big Hero 6",F),("ST-3","Mei Lee","Turning Red",F),
("ST-4","Zeus","Hercules",F),("ST-5","Genie","Aladdin",F),
])

ins("Helix", [
("HX-1","Mickey Mouse","Mickey & Friends",F),("HX-2","Woody","Toy Story",F),
("HX-3","Winnie the Pooh","The Many Adventures of Winnie the Pooh",F),
("HX-4","Snow White","Snow White and the Seven Dwarfs",F),("HX-5","Stitch","Lilo & Stitch",F),
])

ins("Golden Age Posters", [
("GA-1","Snow White and the Seven Dwarfs","Snow White and the Seven Dwarfs",F),
("GA-2","Pinocchio","Pinocchio",F),("GA-3","Fantasia","Fantasia",F),
("GA-4","Dumbo","Dumbo",F),("GA-5","Bambi","Bambi",F),
])

ins("Disney Ink and Paint", [
("I&P-1","Snow White","Snow White and the Seven Dwarfs",F),
("I&P-2","Jiminy Cricket","Pinocchio",F),
("I&P-3","Sorcerer's Apprentice Mickey","Fantasia",F),
("I&P-4","Dumbo","Dumbo",F),("I&P-5","Bambi","Bambi",F),
("I&P-6","The Three Caballeros","The Three Caballeros",F),
("I&P-7","Mr. Toad","The Adventures of Ichabod and Mr. Toad",F),
("I&P-8","Alice","Alice in Wonderland",F),("I&P-9","Peter Pan","Peter Pan",F),
("I&P-10","Merlin","The Sword in the Stone",F),
])

ins("Disney Channel", [
("DC-1","Lizzie McGuire","Lizzie McGuire",F),("DC-2","Raven Baxter","That's So Raven",F),
("DC-3","Hannah Montana","Hannah Montana",F),("DC-4","Alex Russo","Wizards of Waverly Place",F),
("DC-5","Justin Russo","Wizards of Waverly Place",F),("DC-6","Max Russo","Wizards of Waverly Place",F),
("DC-7","Harper Finkle","Wizards of Waverly Place",F),("DC-8","Jerry Russo","Wizards of Waverly Place",F),
("DC-9","Theresa Russo","Wizards of Waverly Place",F),("DC-10","Mitchie Torres","Camp Rock",F),
("DC-11","Shane Gray","Camp Rock",F),("DC-12","Nate Gray","Camp Rock",F),
("DC-13","Jason Gray","Camp Rock",F),("DC-14","Caitlyn Gellar","Camp Rock",F),
("DC-15","Rocky Blue","Shake It Up",F),("DC-16","CeCe Jones","Shake It Up",F),
("DC-17","Jessie","Jessie",F),("DC-18","Liv and Maddie","Liv and Maddie",F),
("DC-19","Riley Matthews","Girl Meets World",F),("DC-20","Maya Hart","Girl Meets World",F),
])

ins("TRON TEK", [
("TR0N-1","He fights for the Users","Tron",F),
("TR0N-2","Together, we will be complete","Tron",F),
("TR0N-3","Vacate entry port, program!","Tron",F),
("TR0N-4","Bio-digital jazz, man","Tron: Legacy",F),
("TR0N-5","I'm a User, I'll improvise","Tron: Legacy",F),
("TR0N-6","The Last ISO","Tron: Legacy",F),
("TR0N-7","Am I still to create the perfect system?","Tron: Legacy",F),
("TR0N-8","Tron Lives","Tron: Legacy",F),
("TR0N-9","Proceed to Games","Tron: Legacy",F),
("TR0N-10","My world is coming to destroy yours","Tron: Ares",F),
])

ins("Toy Story 5 First Edition", [
("TS5-1","Lilypad","Toy Story 5",F),("TS5-2","Karen Beverly","Toy Story 5",F),
("TS5-3","Smarty Pants","Toy Story 5",F),("TS5-4","Atlas","Toy Story 5",F),
("TS5-5","Hi-Tech Edition Buzz Lightyear","Toy Story 5",F),
])

# Moana 10th Anniversary — MN-6 Mini Maui dedupes to Maui
mn_id = add_is("Moana 10th Anniversary")
mn_cards = [
("MN-1","Moana","Moana",F),("MN-2","Heihei","Moana",F),("MN-3","Pua","Moana",F),
("MN-4","Gramma Tala","Moana",F),("MN-5","Maui","Moana",F),
# MN-6 dedupes to Maui, display name "Mini Maui"
("MN-7","Kakamora","Moana",F),("MN-8","Tamatoa","Moana",F),
("MN-9","Te Kā","Moana",F),("MN-10","Te Fiti","Moana",F),
]
add_cards(mn_id, mn_cards)
# Add MN-6 as Maui with subset_tag
maui_pid = get_or_create("Maui")
db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team, subset_tag) VALUES (?, ?, 'MN-6', 0, 'Moana', 'Mini Maui')",
           (maui_pid, mn_id))
print(f"  Moana 10th Anniversary: 10 cards")

ins("High School Musical 20th Anniversary", [
("HSM-1","Troy Bolton","High School Musical",F),("HSM-2","Gabriella Montez","High School Musical",F),
("HSM-3","Sharpay Evans","High School Musical",F),("HSM-4","Ryan Evans","High School Musical",F),
("HSM-5","Chad Danforth","High School Musical",F),("HSM-6","Taylor McKessie","High School Musical",F),
("HSM-7","Kelsi Nielsen","High School Musical",F),("HSM-8","Ms. Darbus","High School Musical",F),
("HSM-9","Zeke Baylor","High School Musical",F),("HSM-10","Coach Bolton","High School Musical",F),
("HSM-11","Jason Cross","High School Musical",F),
])

ins("Cars 20th Anniversary", [
("CRS-1","The King Advises The Rookie","Cars",F),("CRS-2","Sleepy Mack","Cars",F),
("CRS-3","Our Founder: Stanley","Cars",F),("CRS-4","Mater Meets Lightning","Cars",F),
("CRS-5","Sally and Red","Cars",F),("CRS-6","Beautiful Ornament Valley","Cars",F),
("CRS-7","Sally Goes for a Drive","Cars",F),("CRS-8","Doc Hudson Hits the Track","Cars",F),
("CRS-9","Cadillac Range","Cars",F),("CRS-10","Downtown Radiator Springs","Cars",F),
])

ins("Monsters, Inc. 25th Anniversary", [
("MI-1","James P. Sullivan","Monsters, Inc.",F),("MI-2","Boo","Monsters, Inc.",F),
("MI-3","Henry J. Waternoose III","Monsters, Inc.",F),("MI-4","George Sanderson","Monsters, Inc.",F),
("MI-5","Mike Wazowski","Monsters, Inc.",F),("MI-6","Celia Mae","Monsters, Inc.",F),
("MI-7","Roz","Monsters, Inc.",F),("MI-8","Smitty","Monsters, Inc.",F),
("MI-9","Needleman","Monsters, Inc.",F),("MI-10","Randall Boggs","Monsters, Inc.",F),
("MI-11","Fungus","Monsters, Inc.",F),("MI-12","Bile","Monsters, Inc.",F),
("MI-13","CDA Agent","Monsters, Inc.",F),("MI-14","Bob Peterson","Monsters, Inc.",F),
("MI-15","Ted Pauley","Monsters, Inc.",F),
])

ins("Darkwing Duck 35th Anniversary", [
("DD-1","Darkwing Duck","Darkwing Duck",F),("DD-2","Drake Mallard","Darkwing Duck",F),
("DD-3","Gosalyn Mallard","Darkwing Duck",F),("DD-4","Gizmoduck","Darkwing Duck",F),
("DD-5","Launchpad McQuack","Darkwing Duck",F),("DD-6","Splatter Phoenix","Darkwing Duck",F),
("DD-7","Dr. Reginald Bushroot","Darkwing Duck",F),("DD-8","Megavolt","Darkwing Duck",F),
("DD-9","Quackerjack","Darkwing Duck",F),("DD-10","Negaduck","Darkwing Duck",F),
])

ins("Alice in Wonderland 75th Anniversary", [
("AW-1","Following the White Rabbit","Alice in Wonderland",F),
("AW-2","Down the Rabbit Hole","Alice in Wonderland",F),
("AW-3","A Garden of Flowers","Alice in Wonderland",F),
("AW-4","A Mad Tea Party","Alice in Wonderland",F),
("AW-5","A Court of Cards","Alice in Wonderland",F),
("AW-6","Steaming Teapots","Alice in Wonderland",F),
("AW-7","The Mad Hatter","Alice in Wonderland",F),
("AW-8","Who Are You?","Alice in Wonderland",F),
("AW-9","Alice and the White Rabbit","Alice in Wonderland",F),
("AW-10","Painting the Roses Red","Alice in Wonderland",F),
])

ins("Dumbo 85th Anniversary", [("DM-1","Dumbo","Dumbo",F)])

ins("Winnie the Pooh 100th Anniversary", [
("WP-1","Winnie the Pooh","Winnie the Pooh",F),("WP-2","Tigger","Winnie the Pooh",F),
("WP-3","Eeyore","Winnie the Pooh",F),("WP-4","Piglet","Winnie the Pooh",F),
("WP-5","Christopher Robin","Winnie the Pooh",F),("WP-6","Rabbit","Winnie the Pooh",F),
("WP-7","Owl","Winnie the Pooh",F),("WP-8","Roo","Winnie the Pooh",F),
("WP-9","Kanga","Winnie the Pooh",F),("WP-10","Heffalump","Winnie the Pooh",F),
])

ins("Art of Disney", [
("AD-1","Winnie the Pooh","Winnie the Pooh (100 YEARS)",F),
("AD-2","Dumbo","Dumbo (85 YEARS)",F),
("AD-3","Alice in Wonderland","Alice in Wonderland (75 YEARS)",F),
("AD-4","One Hundred and One Dalmatians","One Hundred and One Dalmatians (65 YEARS)",F),
("AD-5","Fox and the Hound","The Fox and the Hound (45 YEARS)",F),
("AD-6","Beauty and the Beast","Beauty and the Beast (35 YEARS)",F),
("AD-7","Darkwing Duck","Darkwing Duck (35 YEARS)",F),
("AD-8","Hunchback of Notre Dame","The Hunchback of Notre Dame (30 YEARS)",F),
("AD-9","Zootopia","Zootopia (10 YEARS)",F),
("AD-10","Moana","Moana (10 YEARS)",F),
])

ins("Disney Reflections", [
("R-1","Genie and Aladdin","Aladdin",F),("R-2","Simba and Mufasa","The Lion King",F),
("R-3","Mulan","Mulan",F),("R-4","Alice and The Doorknob","Alice in Wonderland",F),
("R-5","Darkwing Duck and Negaduck","Darkwing Duck",F),
])

ins("Mickey and Friends Ukiyo-e", [
("UK-1","Mickey Mouse","Mickey & Friends",F),("UK-2","Donald Duck","Mickey & Friends",F),
("UK-3","Daisy Duck","Mickey & Friends",F),("UK-4","Pete","Mickey & Friends",F),
("UK-5","Minnie Mouse","Mickey & Friends",F),("UK-6","Pluto","Mickey & Friends",F),
("UK-7","Chip & Dale","Mickey & Friends",F),("UK-8","Clarabelle","Mickey & Friends",F),
("UK-9","Horace","Mickey & Friends",F),("UK-10","Goofy","Mickey & Friends",F),
])

ins("Lilo & Stitch Shadowbox", [
("LS-1","Stitch","Lilo & Stitch",F),("LS-2","Jumba","Lilo & Stitch",F),
("LS-3","Pleakley","Lilo & Stitch",F),("LS-4","Alien","Lilo & Stitch",F),
("LS-5","Alien","Lilo & Stitch",F),("LS-6","Grand Councilwoman","Lilo & Stitch",F),
("LS-7","Lilo","Lilo & Stitch",F),
])

ins("The Rose Shadowbox", [("RSS-1","The Rose","Beauty and the Beast",F)])
ins("The Heart of Te Fiti Shadowbox", [("TF-1","The Heart of Te Fiti","Moana",F)])

ins("The One and Only", [
("OO-1","Joe Gardner","Soul",F),("OO-2","Mowgli","The Jungle Book",F),
("OO-3","Princess Aurora","Sleeping Beauty",F),("OO-4","Bo Peep","Toy Story",F),
("OO-5","Carl Fredricksen","Up",F),
])

# The One and Only Walt — celebrity
oow_id = add_is("The One and Only Walt")
walt_pid = get_or_create("Walt Disney", "celebrity")
db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, 'OOW-1', 0, 'Walt Disney')",
           (walt_pid, oow_id))
print(f"  The One and Only Walt: 1 card (celebrity)")

# ─── AUTOGRAPH SUBSETS ──────────────────────────────────────────────────────
fa_id = add_is("Disney Chrome Facsimile Autographs", is_auto=True)
fa_cards = [
("FA-1","Mickey Mouse","Mickey & Friends",F),("FA-2","Belle","Beauty and the Beast",F),
("FA-3","Nemo","Finding Nemo",F),("FA-4","Donald Duck","Mickey & Friends",F),
("FA-5","Sharpay Evans","High School Musical",F),("FA-6","Miguel","Coco",F),
("FA-7","Goofy","Mickey & Friends",F),("FA-8","Moana","Moana",F),
("FA-9","Elio Solís","Elio",F),("FA-10","Scrooge McDuck","Ducktales",F),
("FA-11","Rapunzel","Tangled",F),("FA-12","Minnie Mouse","Mickey & Friends",F),
("FA-13","Troy Bolton","High School Musical",F),("FA-14","Ernesto de la Cruz","Coco",F),
("FA-15","Mirabel","Encanto",F),
]
add_cards(fa_id, fa_cards)
print(f"  Disney Chrome Facsimile Autographs: {len(fa_cards)} cards")

# Dual Autographs
dl_id = add_is("Disney Chrome Facsimile Dual Autographs", is_auto=True)
add_dual(dl_id, [
("DL-1","Mickey Mouse","Minnie Mouse"),("DL-2","Scrooge McDuck","Donald Duck"),
("DL-3","Mr. Incredible","Mrs. Incredible"),("DL-4","Miguel","Ernesto de la Cruz"),
("DL-5","Troy Bolton","Gabriella Montez"),("DL-6","WALL-E","EVE"),
])
# Create Mrs. Incredible if not exists
get_or_create("Mrs. Incredible")
print(f"  Disney Chrome Facsimile Dual Autographs: 6 cards (dual)")

# Triple Autographs
tr_id = add_is("Disney Chrome Facsimile Triple Autographs", is_auto=True)
add_triple(tr_id, [
("TR-1","Chip & Dale","Pluto","Dale"),  # Chip is part of "Chip & Dale" character
("TR-2","Elsa","Moana","Mirabel"),
("TR-3","Ariel","Mulan","Belle"),
("TR-4","Huey","Dewey","Louie"),
("TR-5","Clarabelle","Horace","Pete"),
])
# Note: TR-1 has Chip/Pluto/Dale — "Chip & Dale" is already one character, but source lists 3 subjects.
# Create "Dale" as separate for the triple join; "Chip & Dale" exists as a pair character from Ukiyo-e.
get_or_create("Dale")
print(f"  Disney Chrome Facsimile Triple Autographs: 5 cards (triple)")

# Quad Autographs
qd_id = add_is("Disney Chrome Facsimile Quad Autographs", is_auto=True)
add_quad(qd_id, [
("QD-1","Mickey Mouse","Minnie Mouse","Goofy","Pluto"),
("QD-2","Woody","Sulley","Mr. Incredible","Lightning McQueen"),
("QD-3","Troy Bolton","Gabriella Montez","Sharpay Evans","Chad Danforth"),
])
print(f"  Disney Chrome Facsimile Quad Autographs: 3 cards (quad)")

# ─── MLB HOME JERSEY SET ────────────────────────────────────────────────────
mlb_id = add_is("Mickey and Friends MLB Home Jersey Set")
mlb_cards = [
("MLBH-31","Goofy","Los Angeles Dodgers",F),("MLBH-32","Goofy","San Diego Padres",F),
("MLBH-33","Goofy","San Francisco Giants",F),("MLBH-34","Goofy","Arizona Diamondbacks",F),
("MLBH-35","Goofy","Colorado Rockies",F),("MLBH-36","Goofy","Angels",F),
("MLBH-37","Goofy","Athletics",F),("MLBH-38","Goofy","Houston Astros",F),
("MLBH-39","Goofy","Seattle Mariners",F),("MLBH-40","Goofy","Texas Rangers",F),
("MLBH-41","Mickey Mouse","Cleveland Guardians",F),("MLBH-42","Mickey Mouse","Chicago White Sox",F),
("MLBH-43","Mickey Mouse","Detroit Tigers",F),("MLBH-44","Mickey Mouse","Kansas City Royals",F),
("MLBH-45","Mickey Mouse","Minnesota Twins",F),("MLBH-46","Mickey Mouse","St. Louis Cardinals",F),
("MLBH-47","Mickey Mouse","Milwaukee Brewers",F),("MLBH-48","Mickey Mouse","Chicago Cubs",F),
("MLBH-49","Mickey Mouse","Cincinnati Reds",F),("MLBH-50","Mickey Mouse","Pittsburgh Pirates",F),
("MLBH-51","Donald Duck","Atlanta Braves",F),("MLBH-52","Donald Duck","New York Mets",F),
("MLBH-53","Donald Duck","Washington Nationals",F),("MLBH-54","Donald Duck","Miami Marlins",F),
("MLBH-55","Donald Duck","Philadelphia Phillies",F),("MLBH-56","Donald Duck","Toronto Blue Jays",F),
("MLBH-57","Donald Duck","Tampa Bay Rays",F),("MLBH-58","Donald Duck","Boston Red Sox",F),
("MLBH-59","Donald Duck","Baltimore Orioles",F),("MLBH-60","Donald Duck","New York Yankees",F),
]
add_cards(mlb_id, mlb_cards)
print(f"  Mickey and Friends MLB Home Jersey Set: {len(mlb_cards)} cards")

# ─── Summary ────────────────────────────────────────────────────────────────
db.commit()

total_players = db.execute("SELECT COUNT(*) FROM players WHERE set_id = ?", (SET_ID,)).fetchone()[0]
total_appearances = db.execute("""
    SELECT COUNT(*) FROM player_appearances pa
    JOIN insert_sets ins ON pa.insert_set_id = ins.id WHERE ins.set_id = ?
""", (SET_ID,)).fetchone()[0]
total_subsets = db.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id = ?", (SET_ID,)).fetchone()[0]

# Verify Maui dedupe
maui_cards = db.execute("""
    SELECT pa.card_number, ins.name FROM player_appearances pa
    JOIN insert_sets ins ON pa.insert_set_id = ins.id
    JOIN players p ON pa.player_id = p.id
    WHERE p.name = 'Maui' AND p.set_id = ?
""", (SET_ID,)).fetchall()
print(f"\nMaui cards: {len(maui_cards)}")
for cn, sn in maui_cards:
    print(f"  {cn} in {sn}")

print(f"\n{'='*50}")
print(f"Set ID: {SET_ID}")
print(f"Total subsets: {total_subsets}")
print(f"Total unique characters: {total_players}")
print(f"Total card appearances: {total_appearances}")
print(f"Expected: 485 cards")
print(f"0 parallels (pending sell sheet)")
db.close()
print("Done!")
