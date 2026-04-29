"""
Seed: 2025 Topps 30 Years of Toy Story — Part 3
Autograph sets and sketch cards.
Usage: python3 scripts/seed_toy_story_p3.py
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

def add_auto(is_id, card_num, char_name, actor_name, team):
    pid = get_or_create_player(char_name)
    db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, subset_tag, team) VALUES (?, ?, ?, 0, ?, ?)",
               (pid, is_id, str(card_num), actor_name, team))

def add_dual_auto(is_id, card_num, p1_char, p1_actor, p1_team, p2_char, p2_actor, p2_team):
    p1 = get_or_create_player(p1_char)
    p2 = get_or_create_player(p2_char)
    db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, subset_tag, team) VALUES (?, ?, ?, 0, ?, ?)",
               (p1, is_id, str(card_num), f"{p1_actor} / {p2_actor}", p1_team))
    a1 = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a1, p2))

# ─── YOU. ARE. A. TOY... STORY AUTOGRAPHS (29 cards) ─────────────────────────
yrt_id = get_is_id('You. Are. A. Toy... Story Autographs')
yrt = [
    ('YRT-TH','Woody','Tom Hanks','Toy Story'),
    ('YRT-TA','Buzz Lightyear','Tim Allen','Toy Story'),
    ('YRT-JM','Andy Davis','John Morris','Toy Story'),
    ('YRT-AS','Zurg','Andrew Stanton','Toy Story 2'),
    ('YRT-JC','Jessie','Joan Cusack','Toy Story 2'),
    ('YRT-JR','Hamm','John Ratzenberger','Toy Story'),
    ('YRT-WS','Rex','Wallace Shawn','Toy Story'),
    ('YRT-FW','Bullseye','Frank Welker','Toy Story 2'),
    ('YRT-AP','Bo Peep','Annie Potts','Toy Story'),
    ('YRT-BC','Slinky Dog','Blake Clark','Toy Story'),
    ('YRT-WK','Al McWhiggin','Wayne Knight','Toy Story 2'),
    ('YRT-KG','Stinky Pete','Kelsey Grammer','Toy Story 2'),
    ('YRT-JP','Alien','Jeff Pidgeon','Toy Story'),
    ('YRT-EVD','Sid Phillips','Erik von Detten','Toy Story'),
    ('YRT-JB','Barbie','Jodi Benson','Toy Story 3'),
    ('YRT-RK','The Bookworm','Richard Kind','Toy Story 3'),
    ('YRT-WG','Stretch','Whoopi Goldberg','Toy Story 3'),
    ('YRT-KS','Trixie','Kristen Schaal','Toy Story 3'),
    ('YRT-BH','Dolly','Bonnie Hunt','Toy Story 3'),
    ('YRT-LA',"Bonnie's Mom",'Lori Alan','Toy Story 3'),
    ('YRT-TN','Mini Buzz','Teddy Newton','Small Fry'),
    ('YRT-JH','Mini Zurg','Jess Harnell','Small Fry'),
    ('YRT-THL','Forky','Tony Hale','Toy Story 4'),
    ('YRT-CH','Gabby Gabby','Christina Hendricks','Toy Story 4'),
    ('YRT-SP','Benson','Steve Purcell','Toy Story 4'),
    ('YRT-AM','Officer Giggle McDimples','Ally Maki','Toy Story 4'),
    ('YRT-MV','Karen Beverly','Melissa Villaseñor','Toy Story 4'),
    ('YRT-MB','Melephant Brooks','Mel Brooks','Toy Story 4'),
    ('YRT-AO','Old Timer','Alan Oppenheimer','Toy Story 4'),
]
for cn, char, actor, team in yrt:
    add_auto(yrt_id, cn, char, actor, team)
print(f"  You. Are. A. Toy... Story Autographs: {len(yrt)} cards")

# ─── YOU'VE GOT A FRIEND IN ME DUAL AUTOGRAPHS (13 dual cards) ───────────────
ygfda_id = get_is_id("You've Got A Friend In Me Dual Autographs")
ygfda = [
    ('YGF-HA','Woody','Tom Hanks','Toy Story','Buzz Lightyear','Tim Allen','Toy Story'),
    ('YGF-AS','Buzz Lightyear','Tim Allen','Toy Story','Zurg','Andrew Stanton','Toy Story 2'),
    ('YGF-RS','Hamm','John Ratzenberger','Toy Story','Rex','Wallace Shawn','Toy Story'),
    ('YGF-MV','Andy Davis','John Morris','Toy Story','Sid Phillips','Erik von Detten','Toy Story'),
    ('YGF-HP','Woody','Tom Hanks','Toy Story','Bo Peep','Annie Potts','Toy Story'),
    ('YGF-AN','Buzz Lightyear','Tim Allen','Toy Story','Mini Buzz','Teddy Newton','Small Fry'),
    ('YGF-CW','Jessie','Joan Cusack','Toy Story 2','Bullseye','Frank Welker','Toy Story 2'),
    ('YGF-SS','Rex','Wallace Shawn','Toy Story','Trixie','Kristen Schaal','Toy Story 3'),
    ('YGF-NH','Mini Buzz','Teddy Newton','Small Fry','Mini Zurg','Jess Harnell','Small Fry'),
    ('YGF-PH','Benson','Steve Purcell','Toy Story 4','Gabby Gabby','Christina Hendricks','Toy Story 4'),
    ('YGF-KB','The Bookworm','Richard Kind','Toy Story 3','Melephant Brooks','Mel Brooks','Toy Story 4'),
    ('YGF-PM','Bo Peep','Annie Potts','Toy Story','Officer Giggle McDimples','Ally Maki','Toy Story 4'),
    ('YGF-HV','Forky','Tony Hale','Toy Story 4','Karen Beverly','Melissa Villaseñor','Toy Story 4'),
]
for cn, p1c, p1a, p1t, p2c, p2a, p2t in ygfda:
    add_dual_auto(ygfda_id, cn, p1c, p1a, p1t, p2c, p2a, p2t)
print(f"  You've Got A Friend In Me Dual Autographs: {len(ygfda)} dual cards")

# ─── GOLDEN TOYS SHADOWBOX AUTOGRAPHS (10 cards, /20 base) ───────────────────
gt_id = get_is_id('Golden Toys Shadowbox Autographs')
gt = [
    ('GT-TH','Woody','Tom Hanks','Toy Story'),
    ('GT-TA','Buzz Lightyear','Tim Allen','Toy Story'),
    ('GT-JM','Andy Davis','John Morris','Toy Story'),
    ('GT-AS','Zurg','Andrew Stanton','Toy Story 2'),
    ('GT-JC','Jessie','Joan Cusack','Toy Story 2'),
    ('GT-JR','Hamm','John Ratzenberger','Toy Story'),
    ('GT-WS','Rex','Wallace Shawn','Toy Story'),
    ('GT-AP','Bo Peep','Annie Potts','Toy Story'),
    ('GT-KG','Stinky Pete','Kelsey Grammer','Toy Story 2'),
    ('GT-THL','Forky','Tony Hale','Toy Story 4'),
]
for cn, char, actor, team in gt:
    add_auto(gt_id, cn, char, actor, team)
print(f"  Golden Toys Shadowbox Autographs: {len(gt)} cards (/20 base)")

# ─── EXECUTIVE STUDIO CREATIONS SKETCH CARDS (2 artists) ─────────────────────
esc_id = get_is_id('Executive Studio Creations Sketch Cards')
esc = ['Andrew Stanton', 'Bob Peterson']
for i, artist in enumerate(esc, 1):
    pid = get_or_create_player(artist)
    db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, subset_tag, team) VALUES (?, ?, ?, 0, ?, NULL)",
               (pid, esc_id, f'ESC-{i}', 'Executive Studio Creations'))
print(f"  Executive Studio Creations Sketch Cards: {len(esc)} artists")

# ─── STUDIO CREATIONS SKETCH CARDS (8 artists) ───────────────────────────────
sc_id = get_is_id('Studio Creations Sketch Cards')
sc = ['Dan Holland','Derek Thompson','Keiko Murayama',"Kevin O'Brien",
      'Mitra Shahidi','Sandeep','Valerie LaPointe','Yung-Han Chang']
for i, artist in enumerate(sc, 1):
    pid = get_or_create_player(artist)
    db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, subset_tag, team) VALUES (?, ?, ?, 0, ?, NULL)",
               (pid, sc_id, f'SC-{i}', 'Studio Creations'))
print(f"  Studio Creations Sketch Cards: {len(sc)} artists")

# ─── TOY STORY SKETCH CARDS (74 artists) ─────────────────────────────────────
ts_id = get_is_id('Toy Story Sketch Cards')
ts = [
    'Aaron Laurich','Adam Fields','Alex Mines','Anthony Pietszak','Antni Ellison',
    'Ariel Mamani','Ashley Marsh Bean','Benjamin Lombart','Brent Ragland','Charlie Cody',
    'Chenduz','Chris Colyer','Cisco Rivera','Cyrus Sherkat','Dan Cooney',
    'Dan Gorman','Darrin Pepe','David Willingham','Dawn Murphy','DMN',
    'DYJ','Eddie Rhodes III','El Smetchö','Eric Lehtonen','Eric Medina',
    'Fox Layng','Frank Sansone','Garrett Dix','Getatom','Greg Treize',
    'Halsey Camera','Ian McKesson','Isiah Xavier Bradley','James Harris','Jason Crosby',
    'Jason Rodriguez','Jason Sobol','Jay Manchand','Jeffrey C. Benitez','Jessica Hickman',
    'Jessica Van Dusen',"Jim O'Riley",'John Pleak','Julie-Anne','Kevin Graham',
    'Kevin P. West','Lindsey Greyling','Lucas Madison Emerick','Marlo Martos','Matthew Maldonado',
    'Michael Mastermaker','Mike Ritchey','Mike Stephens','Neil Camera','Nick Gribbon',
    'Niño John Benitez','Rich Hennemann','RJ Tomascik','Rob Demers','Ryan Finley',
    'Ryan Johnston','Ryan Thompson','Sandy Lopopolo','Sandy Meeks','Semra Bulut',
    'Stephanie Swanger','Steve Alce','Steve Crockett','Ted Dastick Jr','Tim Shinn',
    'Todd Aaron Smith','Tom Amici','Veronica Louro','Jason (Japanese)',
]
for i, artist in enumerate(ts, 1):
    pid = get_or_create_player(artist)
    db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, subset_tag, team) VALUES (?, ?, ?, 0, ?, NULL)",
               (pid, ts_id, f'TSK-{i}', 'Toy Story Sketch'))
print(f"  Toy Story Sketch Cards: {len(ts)} artists")

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

player_count = db.execute("SELECT COUNT(*) FROM players WHERE set_id = ?", (SET_ID,)).fetchone()[0]
app_count = db.execute("SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON pa.insert_set_id = i.id WHERE i.set_id = ?", (SET_ID,)).fetchone()[0]
print(f"\nDone! Set ID: {SET_ID}")
print(f"  Players: {player_count}")
print(f"  Appearances: {app_count}")
db.close()
