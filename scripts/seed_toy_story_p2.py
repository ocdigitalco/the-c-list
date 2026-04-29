"""
Seed: 2025 Topps 30 Years of Toy Story — Part 2
Base cards and all non-autograph insert sets.
Usage: python3 scripts/seed_toy_story_p2.py
"""
import sqlite3, os, re

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
db = sqlite3.connect(DB_PATH)
db.execute("PRAGMA journal_mode=WAL")
db.execute("PRAGMA foreign_keys=ON")

SET_ID = 66

def get_is_id(name):
    row = db.execute("SELECT id FROM insert_sets WHERE set_id = ? AND name = ?", (SET_ID, name)).fetchone()
    if not row: raise ValueError(f"Insert set not found: '{name}'")
    return row[0]

def get_or_create_player(name):
    row = db.execute("SELECT id FROM players WHERE set_id = ? AND name = ?", (SET_ID, name)).fetchone()
    if row: return row[0]
    db.execute("INSERT INTO players (set_id, name, unique_cards, total_print_run, one_of_ones, insert_set_count) VALUES (?, ?, 0, 0, 0, 0)", (SET_ID, name))
    return db.execute("SELECT last_insert_rowid()").fetchone()[0]

def add_card(is_id, name, team, card_num, is_rookie=0, subset_tag=None):
    pid = get_or_create_player(name)
    db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, subset_tag, team) VALUES (?, ?, ?, ?, ?, ?)",
               (pid, is_id, str(card_num), is_rookie, subset_tag, team))

def add_dual_card(is_id, card_num, p1_name, p1_team, p2_name, p2_team):
    p1 = get_or_create_player(p1_name)
    p2 = get_or_create_player(p2_name)
    db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, ?)",
               (p1, is_id, str(card_num), p1_team))
    a1 = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a1, p2))

def add_cards(is_name, cards, subset_tag=None):
    is_id = get_is_id(is_name)
    for entry in cards:
        card_num, name, team = entry[0], entry[1], entry[2]
        add_card(is_id, name, team, card_num, subset_tag=subset_tag)
    print(f"  {is_name}: {len(cards)} cards")

# ─── BASE (100 cards) ────────────────────────────────────────────────────────
base = [
    (1,'Woody','Toy Story'),(2,'Robot','Toy Story'),(3,'Rubber Shark','Toy Story'),
    (4,'RC','Toy Story'),(5,'Rex','Toy Story'),(6,'Lenny','Toy Story'),
    (7,'Andy Davis','Toy Story'),(8,'Mrs. Davis','Toy Story'),(9,'Mr. Spell','Toy Story'),
    (10,'Mr. Potato Head','Toy Story'),(11,'Hockey Puck','Toy Story'),(12,'Snake','Toy Story'),
    (13,'Etch-A-Sketch','Toy Story'),(14,'Rocky Gibraltar','Toy Story'),(15,'Hamm','Toy Story'),
    (16,'Green Army Soldiers','Toy Story'),(17,'Sarge','Toy Story'),(18,'Troikas','Toy Story'),
    (19,'Mr. Mike','Toy Story'),(20,'Slinky Dog','Toy Story'),(21,'Roly Poly Clown','Toy Story'),
    (22,'Pizza Planet Truck','Toy Story'),(23,'The Claw','Toy Story'),(24,'Alien','Toy Story'),
    (25,'Buzz Lightyear','Toy Story'),(26,"Pizza Planet's Robot Guard",'Toy Story'),
    (27,'Barrel of Monkeys','Toy Story'),(28,'Sid Phillips','Toy Story'),(29,'Scud','Toy Story'),
    (30,'Babyhead','Toy Story'),(31,'Wind-Up Frog','Toy Story'),(32,'Ducky','Toy Story'),
    (33,'Roller Bob','Toy Story'),(34,'Jingle Joe','Toy Story'),(35,'Rockmobile','Toy Story'),
    (36,'Hand-in-the-Box','Toy Story'),(37,"Hannah's Doll",'Toy Story'),
    (38,'Her Little Sister','Toy Story'),(39,'Hannah Phillips','Toy Story'),
    (40,'Bo Peep','Toy Story'),(41,'Billy, Goat, and Gruff','Toy Story'),
    (42,'Molly Davis','Toy Story'),(43,"See 'N Say, The Farmer Says",'Toy Story'),
    (44,'ABC Blocks','Toy Story'),(45,"Andy's Plane",'Toy Story'),
    (46,'Little Tikes Toddle Tots Firemen','Toy Story'),
    (47,'Little Tikes Toddle Tots Doc And Cowboy','Toy Story'),
    (48,'Evil Dr. Porkchop','Toy Story 2'),(49,'Buster','Toy Story 2'),
    (50,'Pixar Ball','Toy Story'),(51,'Bullseye','Toy Story 2'),
    (52,'Stinky Pete','Toy Story 2'),(53,'Al McWhiggin','Toy Story 2'),
    (54,'Jessie','Toy Story 2'),(55,'Wheezy','Toy Story 2'),
    (56,'Mrs. Potato Head','Toy Story 2'),(57,'The Cleaner','Toy Story 2'),
    (58,"Woody's Roundup Carriage",'Toy Story 2'),(59,'Video Game Strategy Guide','Toy Story 2'),
    (60,'Emperor Zurg','Toy Story 2'),(61,"Zurg's Robot",'Toy Story 2'),
    (62,'New Buzz Lightyear','Toy Story 2'),(63,'Critter Beaver','Toy Story 2'),
    (64,'Critter Armadillo','Toy Story 2'),(65,'Critter Deer','Toy Story 2'),
    (66,'Barbie','Toy Story 3'),(67,'Ken','Toy Story 3'),(68,'Bonnie','Toy Story 3'),
    (69,'Mr. Pricklepants','Toy Story 3'),(70,'Trixie','Toy Story 3'),
    (71,'Buttercup','Toy Story 3'),(72,'Dolly','Toy Story 3'),
    (73,'Peas-in-a-Pod','Toy Story 3'),(74,'Jack-in-the-Box','Toy Story 3'),
    (75,'Lotso','Toy Story 3'),(76,'Big Baby','Toy Story 3'),
    (77,'Chuckles','Toy Story 3'),(78,'The Bookworm','Toy Story 3'),
    (79,'Chatter Telephone','Toy Story 3'),(80,'Twitch','Toy Story 3'),
    (81,'Stretch','Toy Story 3'),(82,'Chunk','Toy Story 3'),
    (83,'Sparks','Toy Story 3'),(84,'Mini Buzz','Small Fry'),
    (85,'Mini Zurg','Small Fry'),(86,'Combat Carl','Toy Story of Terror!'),
    (87,'Melephant Brooks','Toy Story 4'),(88,'Tinny','Toy Story 4'),
    (89,'Officer Giggle McDimples','Toy Story 4'),(90,'Duke Caboom','Toy Story 4'),
    (91,'Gabby Gabby','Toy Story 4'),(92,'Benson','Toy Story 4'),
    (93,'Margaret','Toy Story 4'),(94,'Dragon the Cat','Toy Story 4'),
    (95,'Harmony','Toy Story 4'),(96,'Axel the Carnival Worker','Toy Story 4'),
    (97,'Ducky','Toy Story 4'),(98,'Bunny','Toy Story 4'),
    (99,'Karen Beverly','Toy Story 4'),(100,'Forky','Toy Story 4'),
]
add_cards('Base', base)

# ─── IMAGE VARIATIONS (17 cards) ─────────────────────────────────────────────
iv = [
    ('1','Woody','Toy Story'),('5','Rex','Toy Story'),('7','Andy Davis','Toy Story'),
    ('16','Green Army Soldiers','Toy Story'),('18','Troikas','Toy Story'),
    ('23','The Claw','Toy Story'),('25a','Buzz Lightyear','Toy Story'),
    ('25b','Buzz Lightyear','Toy Story'),('25c','Spanish Buzz','Toy Story 3'),
    ('40','Bo Peep','Toy Story'),('45',"Andy's Plane",'Toy Story'),
    ('49','Buster','Toy Story 2'),('53','Al McWhiggin','Toy Story 2'),
    ('60','Emperor Zurg','Toy Story 2'),('73','Peas-in-a-Pod','Toy Story 3'),
    ('88','Tinny','Toy Story 2'),('100','Forky','Toy Story 4'),
]
add_cards('Image Variations', iv)

# ─── PIZZA PLANET VARIATION (27 cards) ───────────────────────────────────────
ppv = [
    ('1','Woody','Toy Story'),('4','RC','Toy Story'),('5','Rex','Toy Story'),
    ('10','Mr. Potato Head','Toy Story'),('15','Hamm','Toy Story'),
    ('20','Slinky Dog','Toy Story'),('22','Pizza Planet Truck','Toy Story'),
    ('23','The Claw','Toy Story'),('24','Alien','Toy Story'),
    ('25','Buzz Lightyear','Toy Story'),('26',"Pizza Planet's Robot Guard",'Toy Story'),
    ('40','Bo Peep','Toy Story'),('51','Bullseye','Toy Story 2'),
    ('52','Stinky Pete','Toy Story 2'),('54','Jessie','Toy Story 2'),
    ('55','Wheezy','Toy Story 2'),('56','Mrs. Potato Head','Toy Story 2'),
    ('60','Emperor Zurg','Toy Story 2'),('69','Mr. Pricklepants','Toy Story 3'),
    ('70','Trixie','Toy Story 3'),('71','Buttercup','Toy Story 3'),
    ('75','Lotso','Toy Story 3'),('90','Duke Caboom','Toy Story 4'),
    ('91','Gabby Gabby','Toy Story 4'),('97','Ducky','Toy Story 4'),
    ('98','Bunny','Toy Story 4'),('100','Forky','Toy Story 4'),
]
add_cards('Pizza Planet Variation', ppv)

# ─── CONE VARIATION (5 cards) ────────────────────────────────────────────────
add_cards('Cone Variation', [
    ('5','Rex','Toy Story'),('10','Mr. Potato Head','Toy Story'),
    ('15','Hamm','Toy Story'),('20','Slinky Dog','Toy Story'),
    ('25','Buzz Lightyear','Toy Story'),
])

# ─── PIXAR BALL VARIATION (31 cards) ─────────────────────────────────────────
pb = [
    ('1','Woody','Toy Story'),('4','RC','Toy Story'),('5','Rex','Toy Story'),
    ('10','Mr. Potato Head','Toy Story'),('15','Hamm','Toy Story'),
    ('20','Slinky Dog','Toy Story'),('24','Alien','Toy Story'),
    ('25','Buzz Lightyear','Toy Story'),('40','Bo Peep','Toy Story'),
    ('51','Bullseye','Toy Story 2'),('52','Stinky Pete','Toy Story 2'),
    ('53','Al McWhiggin','Toy Story 2'),('54','Jessie','Toy Story 2'),
    ('55','Wheezy','Toy Story 2'),('56','Mrs. Potato Head','Toy Story 2'),
    ('60','Emperor Zurg','Toy Story 2'),('69','Mr. Pricklepants','Toy Story 3'),
    ('70','Trixie','Toy Story 3'),('71','Buttercup','Toy Story 3'),
    ('72','Dolly','Toy Story 3'),('75','Lotso','Toy Story 3'),
    ('84','Mini Buzz','Small Fry'),('85','Mini Zurg','Small Fry'),
    ('86','Combat Carl','Toy Story of Terror!'),('88','Tinny','Toy Story 4'),
    ('89','Officer Giggle McDimples','Toy Story 4'),('90','Duke Caboom','Toy Story 4'),
    ('91','Gabby Gabby','Toy Story 4'),('97','Ducky','Toy Story 4'),
    ('98','Bunny','Toy Story 4'),('100','Forky','Toy Story 4'),
]
add_cards('Pixar Ball Variation', pb)

# ─── 30 YEARS AND BEYOND (35 cards) ──────────────────────────────────────────
beyond = [
    ('30Y-1','Andy Plays with One-Eyed Bart','Toy Story'),
    ('30Y-2','Briefing the Toys','Toy Story'),
    ('30Y-3','Cast Aside','Toy Story'),
    ('30Y-4','Buzz Lightyear: Space Ranger','Toy Story'),
    ('30Y-5','To Infinity, and Beyond!','Toy Story'),
    ('30Y-6','You Are A Toy!','Toy Story'),
    ('30Y-7','Pizza Planet Truck: Buzz is Safer in the Cockpit','Toy Story'),
    ('30Y-8','The Claw','Toy Story'),
    ('30Y-9',"Stuck in Sid's Room",'Toy Story'),
    ('30Y-10','As Seen on TV: Buzz Lightyear','Toy Story'),
    ('30Y-11','Mrs. Nesbitt Has a Tea Party','Toy Story'),
    ('30Y-12','Woody Throws a Line','Toy Story'),
    ('30Y-13','Buzz and The Big One','Toy Story'),
    ('30Y-14',"Woody's Escape Plan",'Toy Story'),
    ('30Y-15',"That's right, I'm talking to you",'Toy Story'),
    ('30Y-16',"This isn't flying, this is falling with style",'Toy Story'),
    ('30Y-17','No sign of intelligent life anywhere','Toy Story 2'),
    ('30Y-18','Woody, look under your boot','Toy Story 2'),
    ('30Y-19',"Hurry on Down to Al's Toy Barn",'Toy Story 2'),
    ('30Y-20',"Woody's Nightmare: I don't wanna play with you anymore",'Toy Story 2'),
    ('30Y-21','Wheezy is Rescued from the Yard Sale','Toy Story 2'),
    ('30Y-22',"Woody's Round Up",'Toy Story 2'),
    ('30Y-23','Cone Crossing','Toy Story 2'),
    ('30Y-24','College-Bound Andy Encounters His Old Pals','Toy Story 3'),
    ('30Y-25','Lotso Welcomes the Gang to Sunnyside Daycare','Toy Story 3'),
    ('30Y-26','Lotso is Left Behind','Toy Story 3'),
    ('30Y-27','Facing the Incinerator Together','Toy Story 3'),
    ('30Y-28','Return of the Toys','Toy Story 3'),
    ('30Y-29','Andy Shows Bonnie Her New Toys','Toy Story 3'),
    ('30Y-30','The Toys Get a New Home','Toy Story 3'),
    ('30Y-31','Woody Reassures Forky On the Road','Toy Story 4'),
    ('30Y-32','Woody Reunites with Bo','Toy Story 4'),
    ('30Y-33','Gabby Gabby and Benson in Second Chance Antiques','Toy Story 4'),
    ('30Y-34','The Carnival Comes to Town','Toy Story 4'),
    ('30Y-35',"Duke Caboom: Canada's Greatest Stuntman",'Toy Story 4'),
]
add_cards('30 Years And Beyond', beyond)

# ─── YOU'VE GOT A FRIEND IN ME (15 dual cards) ──────────────────────────────
ygf_id = get_is_id("You've Got A Friend In Me")
ygf = [
    ('YGF-1','Woody','Toy Story','Buzz Lightyear','Toy Story'),
    ('YGF-2','Hamm','Toy Story','Rex','Toy Story'),
    ('YGF-3','Mr. Potato Head','Toy Story','Mrs. Potato Head','Toy Story 2'),
    ('YGF-4','Jessie','Toy Story 2','Bullseye','Toy Story 2'),
    ('YGF-5','Buzz Lightyear','Toy Story','Jessie','Toy Story 2'),
    ('YGF-6','Woody','Toy Story','Slinky Dog','Toy Story'),
    ('YGF-7','Bo Peep','Toy Story','Billy, Goat, and Gruff','Toy Story'),
    ('YGF-8','Mr. Pricklepants','Toy Story 3','Buttercup','Toy Story 3'),
    ('YGF-9','Barbie','Toy Story 3','Ken','Toy Story 3'),
    ('YGF-10','Buzz Lightyear','Toy Story','Mini Buzz','Small Fry'),
    ('YGF-11','Rex','Toy Story','Trixie','Toy Story 3'),
    ('YGF-12','Woody','Toy Story','Forky','Toy Story 4'),
    ('YGF-13','Ducky','Toy Story 4','Bunny','Toy Story 4'),
    ('YGF-14','Bo Peep','Toy Story','Officer Giggle McDimples','Toy Story 4'),
    ('YGF-15','Forky','Toy Story 4','Karen Beverly','Toy Story 4'),
]
for cn, p1n, p1t, p2n, p2t in ygf:
    add_dual_card(ygf_id, cn, p1n, p1t, p2n, p2t)
print(f"  You've Got A Friend In Me: {len(ygf)} dual cards")

# ─── FALLING WITH STYLE (10 cards) ───────────────────────────────────────────
add_cards('Falling With Style', [
    ('FWS-1','Woody','Toy Story'),('FWS-2','Duke Caboom','Toy Story 4'),
    ('FWS-3','Alien','Toy Story'),('FWS-4','Rex','Toy Story'),
    ('FWS-5','Forky','Toy Story 4'),('FWS-6','Jessie','Toy Story 2'),
    ('FWS-7','Hamm','Toy Story'),('FWS-8','Buzz Lightyear','Toy Story'),
    ('FWS-9','Bullseye','Toy Story 2'),('FWS-10','Bo Peep','Toy Story'),
])

# ─── SO PLAY NICE (10 cards) ─────────────────────────────────────────────────
add_cards('So Play Nice', [
    ('SPN-1','Sid Phillips','Toy Story'),('SPN-2','Mutant Toys','Toy Story'),
    ('SPN-3','Al McWhiggin','Toy Story 2'),('SPN-4','Stinky Pete','Toy Story 2'),
    ('SPN-5','Emperor Zurg','Toy Story 2'),('SPN-6','Lotso','Toy Story 3'),
    ('SPN-7','Big Baby','Toy Story 3'),('SPN-8','Demo-Mode Buzz','Toy Story 3'),
    ('SPN-9','Benson','Toy Story 4'),('SPN-10','Gabby Gabby','Toy Story 4'),
])

# ─── TOPPS 1995 (26 cards) ───────────────────────────────────────────────────
add_cards('Topps 1995', [
    ('T95-1','Woody','Toy Story'),('T95-2','RC','Toy Story'),
    ('T95-3','Rex','Toy Story'),('T95-4','Hamm','Toy Story'),
    ('T95-5','Buzz Lightyear','Toy Story'),('T95-6','Slinky Dog','Toy Story'),
    ('T95-7','Bucket of Soldiers','Toy Story'),('T95-8','Mr. Potato Head','Toy Story'),
    ('T95-9','Bo Peep','Toy Story'),('T95-10','Alien','Toy Story'),
    ('T95-11','Babyhead','Toy Story'),('T95-12','Janie Pterodactyl','Toy Story'),
    ('T95-13','Wheezy','Toy Story 2'),('T95-14','Stinky Pete','Toy Story 2'),
    ('T95-15','Jessie','Toy Story 2'),('T95-16','Bullseye','Toy Story 2'),
    ('T95-17','Zurg','Toy Story 2'),('T95-18','Mrs. Potato Head','Toy Story 2'),
    ('T95-19','Lotso','Toy Story 3'),('T95-20','Barbie','Toy Story 3'),
    ('T95-21','Chunk','Toy Story 3'),('T95-22','Combat Carl Jr.','Toy Story of Terror!'),
    ('T95-23','Gabby Gabby','Toy Story 4'),('T95-24','Ducky','Toy Story 4'),
    ('T95-25','Bunny','Toy Story 4'),('T95-26','Forky','Toy Story 4'),
])

# ─── AL'S TOY BARN (5 cards) ─────────────────────────────────────────────────
add_cards("Al's Toy Barn", [
    ('ATB-1','Al McWhiggin','Toy Story 2'),('ATB-2','Stinky Pete','Toy Story 2'),
    ('ATB-3','Zurg','Toy Story 2'),('ATB-4','Tour Guide Barbie','Toy Story 2'),
    ('ATB-5','New Buzz','Toy Story 2'),
])

# ─── TO INFINITY… (2 cards) ──────────────────────────────────────────────────
add_cards('To Infinity…', [
    ('B-TI','Buzz Lightyear','Toy Story'),('B-AI','Spanish Buzz','Toy Story 3'),
])

# ─── …AND BEYOND (2 cards) ───────────────────────────────────────────────────
add_cards('…And Beyond', [
    ('B-AB','Buzz Lightyear','Toy Story'),('B-YMA','Spanish Buzz','Toy Story 3'),
])

# ─── TOY TAAFFEITE (10 cards) ────────────────────────────────────────────────
add_cards('Toy Taaffeite', [
    ('TT-1','Bo Peep','Toy Story'),('TT-2','Bullseye','Toy Story 2'),
    ('TT-3','Buzz Lightyear','Toy Story'),('TT-4','Hamm','Toy Story'),
    ('TT-5','Jessie','Toy Story 2'),('TT-6','Mr. Potato Head','Toy Story'),
    ('TT-7','Rex','Toy Story'),('TT-8','Slinky Dog','Toy Story'),
    ('TT-9','Wheezy','Toy Story 2'),('TT-10','Woody','Toy Story'),
])

# ─── ART OF TOY STORY (20 cards) ─────────────────────────────────────────────
add_cards('Art Of Toy Story', [
    ('ART-1','Sheriff Woody','Toy Story'),('ART-2','Slinky Dog and Woody','Toy Story'),
    ('ART-3','The Bucket of Soldiers Deploy','Toy Story'),('ART-4','The Aliens','Toy Story'),
    ('ART-5','Early Buzz Lightyear','Toy Story'),('ART-6','Buzz Lightyear Exploration','Toy Story'),
    ('ART-7','Rex Games as Buzz, with Buzz','Toy Story'),('ART-8','Jessie','Toy Story 2'),
    ('ART-9','Bullseye','Toy Story 2'),('ART-10','Buzz and Woody Exploration','Toy Story'),
    ('ART-11','Buzz Lightyear, Batteries Not Included','Toy Story'),
    ('ART-12','RC Propels Buzz and Woody','Toy Story'),
    ('ART-13','Bonnie and Her New Toys','Toy Story 3'),('ART-14','Woody Exploration','Toy Story'),
    ('ART-15','Buttercup','Toy Story 3'),('ART-16','Dolly','Toy Story 3'),
    ('ART-17','The Dummies','Toy Story 4'),('ART-18','Forky','Toy Story 4'),
    ('ART-19','Stinky Pete','Toy Story 2'),('ART-20','Buzz Lightyear','Toy Story'),
])

# ─── SID HAS YOUR CARDS (10 cards, SSP /5) ───────────────────────────────────
add_cards('Sid Has Your Cards', [
    ('SHC-1','Buzz Lightyear','Toy Story'),('SHC-2','Rex','Toy Story'),
    ('SHC-3','Rockmobile','Toy Story'),('SHC-4','Hamm','Toy Story'),
    ('SHC-5','Babyhead','Toy Story'),('SHC-6','Sarge','Toy Story'),
    ('SHC-7','RC','Toy Story'),('SHC-8','Roller Bob','Toy Story'),
    ('SHC-9','Slinky Dog','Toy Story'),('SHC-10','Woody','Toy Story'),
])

# ─── ANDY'S CARDS SHADOWBOX (10 cards) ────────────────────────────────────────
add_cards("Andy's Cards Shadowbox", [
    ('AC-1','Woody','Toy Story'),('AC-2','Bullseye','Toy Story 2'),
    ('AC-3','Mr. Potato Head','Toy Story'),('AC-4','Rex','Toy Story'),
    ('AC-5','Jessie','Toy Story 2'),('AC-6','Hamm','Toy Story'),
    ('AC-7','RC','Toy Story'),('AC-8','Slinky Dog','Toy Story'),
    ('AC-9','Bo Peep','Toy Story'),('AC-10','Buzz Lightyear','Toy Story'),
])

# ─── THE CLAW SHADOWBOX (10 cards) ───────────────────────────────────────────
add_cards('The Claw Shadowbox', [
    ('TC-1','Rocky Gibraltar','Toy Story'),('TC-2','Robot','Toy Story'),
    ('TC-3','Rex','Toy Story'),('TC-4','Mr. Potato Head','Toy Story'),
    ('TC-5','Buzz Lightyear','Toy Story'),('TC-6','Hamm','Toy Story'),
    ('TC-7','Sarge','Toy Story'),('TC-8','Wheezy','Toy Story 2'),
    ('TC-9','Duke Caboom','Toy Story 4'),('TC-10','Zurg','Toy Story 2'),
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

# Verify
player_count = db.execute("SELECT COUNT(*) FROM players WHERE set_id = ?", (SET_ID,)).fetchone()[0]
app_count = db.execute("SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON pa.insert_set_id = i.id WHERE i.set_id = ?", (SET_ID,)).fetchone()[0]
print(f"\nDone! Set ID: {SET_ID}")
print(f"  Players: {player_count}")
print(f"  Appearances: {app_count}")
db.close()
