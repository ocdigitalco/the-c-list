"""
Seed: 2025 Topps Star Wars Masterwork — Full checklist.
100 base, 7 insert subsets, 6 auto subsets, 3 relic subsets, 4 auto-relic subsets,
4 sketch subsets, ~180 sketch artists. Full parallel matrix + pack odds.
Usage: python3 scripts/seed_star_wars_masterwork_2025.py
"""
import sqlite3, os, json, re, unicodedata

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
db = sqlite3.connect(DB_PATH)
db.execute("PRAGMA journal_mode=WAL")
db.execute("PRAGMA foreign_keys=ON")

# ─── Create Set ──────────────────────────────────────────────────────────────
box_config = json.dumps({
    "hobby": {
        "cards_per_pack": 5,
        "packs_per_box": 4,
        "boxes_per_case": 8,
        "notes": "5 cards per mini box, 4 mini boxes per master box. 2 autographs per master box."
    }
})

db.execute("""
    INSERT INTO sets (name, sport, season, tier, slug, is_visible,
                      sample_image_url, release_date, box_config, created_at)
    VALUES ('2025 Topps Star Wars Masterwork', 'Entertainment', '2025', 'Standard',
            '2025-topps-star-wars-masterwork', 1,
            '/sets/2025-topps-star-wars-masterwork.jpg', '2026-06-03', ?, '2026-05-27T12:00:00Z')
""", (box_config,))
SET_ID = db.execute("SELECT last_insert_rowid()").fetchone()[0]
print(f"Created set ID: {SET_ID}")

H = "Hobby"

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
    if not _slug_cache:
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

def add_pars(is_id, pars):
    for name, pr in pars:
        db.execute("INSERT INTO parallels (insert_set_id, name, print_run, exclusivity) VALUES (?, ?, ?, ?)",
                   (is_id, name, pr, H))
    return len(pars)

def add_cards(is_id, cards, role="character"):
    for num, name in cards:
        pid = get_or_create(name, role)
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, NULL)",
                   (pid, is_id, str(num)))

def add_dual(is_id, cards):
    for num, n1, n2 in cards:
        pid1 = get_or_create(n1)
        pid2 = get_or_create(n2)
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, NULL)", (pid1, is_id, str(num)))
        a = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a, pid2))

def add_triple(is_id, cards):
    for num, n1, n2, n3 in cards:
        pids = [get_or_create(n) for n in [n1, n2, n3]]
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, NULL)", (pids[0], is_id, str(num)))
        a = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        for p in pids[1:]:
            db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a, p))

def add_quad(is_id, cards):
    for num, n1, n2, n3, n4 in cards:
        pids = [get_or_create(n) for n in [n1, n2, n3, n4]]
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, NULL)", (pids[0], is_id, str(num)))
        a = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        for p in pids[1:]:
            db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a, p))

def add_multi(is_id, num, names):
    pids = [get_or_create(n) for n in names]
    db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, NULL)", (pids[0], is_id, str(num)))
    a = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    for p in pids[1:]:
        db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a, p))

def ins(name, cards, is_auto=False, role="character"):
    is_id = add_is(name, is_auto=is_auto)
    add_cards(is_id, cards, role=role)
    print(f"  {name}: {len(cards)} cards")
    return is_id

# ─── BASE SET (100 cards) ───────────────────────────────────────────────────
base_id = add_is("Base Set")
base_pars = [
    ("Base", None), ("Blue", None), ("Green", 99), ("Purple", 50),
    ("Red", 25), ("Orange", 10), ("Black", 5), ("Gold", 1),
    ("Printing Plate Cyan", 1), ("Printing Plate Magenta", 1),
    ("Printing Plate Yellow", 1), ("Printing Plate Black", 1),
]
add_pars(base_id, base_pars)

base_cards = [
    (1,"Luke Skywalker"),(2,"R2-D2"),(3,"Han Solo"),(4,"Jedi Master Sol"),
    (5,"Jedi Master Indara"),(6,"Jod Na Nawood"),(7,"Yoda"),(8,"Grogu"),
    (9,"Neel"),(10,"Captain Brutus"),(11,"Jedi Master Vernestra Rwoh"),
    (12,"The Stranger"),(13,"Boba Fett"),(14,"The Mandalorian"),
    (15,"Captain Phasma"),(16,"Padme Amidala"),(17,"Anakin Skywalker"),
    (18,"Obi-Wan Kenobi"),(19,"Shin Hati"),(20,"Baylan Skoll"),
    (21,"Grand Admiral Thrawn"),(22,"Ahsoka Tano"),(23,"Sabine Wren"),
    (24,"Ezra Bridger"),(25,"Hera Syndulla"),(26,"Chopper"),
    (27,"Imperial Snowtrooper"),(28,"Mace Windu"),(29,"Darth Vader"),
    (30,"Jyn Erso"),(31,"Cassian Andor"),(32,"Mon Mothma"),
    (33,"Luthen Rael"),(34,"Maul"),(35,"Cobb Vanth"),(36,"Dedra Meero"),
    (37,"Rebel Trooper"),(38,"Chewbacca"),(39,"Qui-Gon Jinn"),(40,"Rey"),
    (41,"Kylo Ren"),(42,"Kleya Marki"),(43,"Ryder Azadi"),(44,"C-3PO"),
    (45,"Jedi Master Kelnacca"),(46,"Bo-Katan Kryze"),(47,"Greef Karga"),
    (48,"Vel Sartha"),(49,"Cinta Kaz"),(50,"Arvel Skeen"),
    (51,"Lando Calrissian"),(52,"Syril Karn"),(53,"Morgan Elsbeth"),
    (54,"Supervisor Lonni Jung"),(55,"Director Orson Krennic"),(56,"BB-8"),
    (57,"Saw Gerrera"),(58,"Jedi Master Dooku"),(59,"Major Partagaz"),
    (60,"Tredgar Volk"),(61,"Vane"),(62,"Migs Mayfeld"),
    (63,"Grand Moff Tarkin"),(64,"General Hux"),(65,"Wilmon Paak"),
    (66,"Darth Sidious"),(67,"Snap Wexley"),(68,"Maz Kanata"),
    (69,"Bix Caleen"),(70,"Kaydel Connix"),(71,"Qi'ra"),
    (72,"Jedi Padawan Jecki Lon"),(73,"Boolio"),(74,"Chirrut Imwe"),
    (75,"SM-33"),(76,"K-2SO"),(77,"Poe Dameron"),(78,"Moff Gideon"),
    (79,"Asajj Ventress"),(80,"Admiral Ackbar"),(81,"Kh'ymm"),
    (82,"Cad Bane"),(83,"Haja Estree"),(84,"Jar Jar Binks"),(85,"Jawa"),
    (86,"Bail Organa"),(87,"Moroff"),(88,"The Fourth Sister"),
    (89,"The Fifth Brother"),(90,"The Seventh Sister"),(91,"IG-12"),
    (92,"Vulptex"),(93,"Fennec Shand"),(94,"Vect Nokru"),(95,"Gunter"),
    (96,"Zett Jukassa"),(97,"Babu Frik"),(98,"General Grievous"),
    (99,"Lobot"),(100,"Leia Organa"),
]
add_cards(base_id, base_cards)
print(f"  Base Set: {len(base_cards)} cards, {len(base_pars)} parallels")

# ─── INSERT SUBSETS ─────────────────────────────────────────────────────────
# Shared insert parallel ladder (Under Disguise, Fall of the Chosen One, Short Circuit)
std_insert_pars = [
    ("Base", None), ("Rainbow Foil", 299), ("Canvas", 25), ("Wood", 10),
    ("Metal", 5), ("Gold Metal", 1),
    ("Printing Plate Cyan", 1), ("Printing Plate Magenta", 1),
    ("Printing Plate Yellow", 1), ("Printing Plate Black", 1),
]

# Galactic Die Cut Pods ladder (no Metal/Gold Metal)
gpod_pars = [
    ("Base", None), ("Rainbow Foil", 299), ("Canvas", 25), ("Wood", 10),
    ("Printing Plate Cyan", 1), ("Printing Plate Magenta", 1),
    ("Printing Plate Yellow", 1), ("Printing Plate Black", 1),
]

# BB-8 ladder
bb8_pars = [
    ("Base", None), ("Rainbow Foil", 299), ("Colored Metal", 5), ("Canvas", 25),
    ("Wood", 10),
    ("Printing Plate Cyan", 1), ("Printing Plate Magenta", 1),
    ("Printing Plate Yellow", 1), ("Printing Plate Black", 1),
]

# Under Disguise
ud_id = ins("Under Disguise", [
    ("UN-1","The Mandalorian"),("UN-2","Bo-Katan Kryze"),("UN-3","Captain Silvo"),
    ("UN-4","Zorii Bliss"),("UN-5","The Armorer"),("UN-6","Jango Fett"),
    ("UN-7","Kylo Ren"),("UN-8","Carib Diss"),("UN-9","Paz Vizsla"),
    ("UN-10","Sith Trooper"),("UN-11","Alazmec"),("UN-12","Vicrul"),
    ("UN-13","Kuruk"),("UN-14","Ushar"),("UN-15","Trudgen"),("UN-16","Ap'Lek"),
    ("UN-17","Cardo"),("UN-18","Lando Calrissian"),("UN-19","Captain Enoch"),
    ("UN-20","Night Trooper"),("UN-21","The Stranger"),("UN-22","Constable Zuvio"),
    ("UN-23","Captain Rex"),("UN-24","Fennec Shand"),("UN-25","Boba Fett"),
    ("UN-26","Darth Vader"),
])
add_pars(ud_id, std_insert_pars)

# Fall of the Chosen One (scenes)
fotco_id = ins("Fall of the Chosen One", [
    ("FALL-1",'"I Sense Great Fear In You"'),("FALL-2",'"Do It"'),
    ("FALL-3","Padme Amidala's Confession"),("FALL-4","Blinded by Love"),
    ("FALL-5","Anakin Skywalker's Troubling Vision"),("FALL-6","Yoda's Counsel"),
    ("FALL-7","The Eyes, Ears, And Voice Of The Republic"),
    ("FALL-8","An Outburst At The Council"),("FALL-9","An Unofficial Assignment"),
    ("FALL-10","A Request From Padme Amidala"),("FALL-11",'"Not From A Jedi"'),
    ("FALL-12","Obi-Wan Kenobi Chosen Over Anakin Skywalker"),
    ("FALL-13","A Brother's Final Goodbye"),("FALL-14","A Sith Lord, Revealed"),
    ("FALL-15","Conflicted"),("FALL-16",'"I Am The Senate"'),("FALL-17","A Fatal Choice"),
    ("FALL-18","Anakin Skywalker Becomes Darth Vader"),("FALL-19","Knightfall"),
    ("FALL-20","Finishing Off The Separatists"),("FALL-21","The First Galactic Empire"),
    ("FALL-22","The End Of Brotherhood"),("FALL-23","More Machine Than Man"),
    ("FALL-24","The Sith Lords"),
])
add_pars(fotco_id, std_insert_pars)

# Galactic Die Cut Pods
gpod_id = ins("Galactic Die Cut Pods", [
    ("GPOD-1","Padme Amidala"),("GPOD-2","Bail Organa"),("GPOD-3","Mon Mothma"),
    ("GPOD-4","Mas Amedda"),("GPOD-5","Nute Gunray"),("GPOD-6","Riyo Chuchi"),
    ("GPOD-7","Mee Deechi"),("GPOD-8","Rush Clovis"),("GPOD-9","Onaconda Farr"),
    ("GPOD-10","Halle Burtoni"),("GPOD-11","Orn Free Taa"),("GPOD-12","Hamato Xiono"),
    ("GPOD-13","Aks Moe"),("GPOD-14","Mina Bonteri"),("GPOD-15","Sheev Palpatine"),
    ("GPOD-16","Sly Moore"),("GPOD-17","Gall Trayvis"),("GPOD-18","Nix Card"),
    ("GPOD-19","Kharrus"),("GPOD-20","Lott Dod"),("GPOD-21","Ask Aak"),
    ("GPOD-22","Finis Valorum"),("GPOD-23","Jar Jar Binks"),("GPOD-24","Darth Sidious"),
])
add_pars(gpod_id, gpod_pars)

# Short Circuit
sc_id = ins("Short Circuit", [
    ("SHOC-1","R2-D2"),("SHOC-2","BD-72"),("SHOC-3","MD-15C"),
    ("SHOC-4","SE8 Waiter Droid"),("SHOC-5","D-0"),("SHOC-6","R4-DT"),
    ("SHOC-7","First Order Interrogator Droid"),("SHOC-8","R5-X3"),
    ("SHOC-9","Star Navigator Droid"),("SHOC-10","BB-8"),
    ("SHOC-11","HK-87 Assassin Droid"),("SHOC-12","C2-B5"),("SHOC-13","R2-BHD"),
    ("SHOC-14","1-JAC"),("SHOC-15","Chopper"),("SHOC-16","Lola"),
    ("SHOC-17","Imperial Probe Droid"),("SHOC-18","Pip"),
    ("SHOC-19","Scorpenek Annihilator Droid"),("SHOC-20","Homing Spider Droid"),
    ("SHOC-21","G2-1B7"),("SHOC-22","K-2SO"),("SHOC-23","RA-7 Protocol Droid"),
    ("SHOC-24","Nevarro Copper Droid"),("SHOC-25","C-3PO"),("SHOC-26","AD-4M"),
])
add_pars(sc_id, std_insert_pars)

# BB-8 (scenes)
bb8_id = ins("BB-8", [
    ("BB8-1","An Initial Threat"),("BB8-2","Freed By Rey"),("BB8-3","Shocking Finn"),
    ("BB8-4","Rolling In The Millennium Falcon"),("BB8-5","Thumbs Up"),
    ("BB8-6","Reunited With Poe Dameron"),("BB8-7","Waking Up R2-D2"),
    ("BB8-8","Rolling Slot Machine"),("BB8-9","Carried by Chewbacca"),
    ("BB8-10","Fixing D-O"),
])
add_pars(bb8_id, bb8_pars)

# Lothal Jedi Temple Mortis Gods Painting Puzzle (no parallels)
ins("Lothal Jedi Temple Mortis Gods Painting Puzzle", [
    ("MORTIS-1","Piece 1"),("MORTIS-2","Piece 2"),("MORTIS-3","Piece 3"),
    ("MORTIS-4","Piece 4"),("MORTIS-5","Piece 5"),("MORTIS-6","Piece 6"),
    ("MORTIS-7","Piece 7"),("MORTIS-8","Piece 8"),("MORTIS-9","Piece 9"),
])

# 10 Years of Masterworks Buybacks (empty shell)
add_is("10 Years of Masterworks Buybacks")
print(f"  10 Years of Masterworks Buybacks: empty (buyback subset)")

# ─── AUTOGRAPH SUBSETS ──────────────────────────────────────────────────────
auto_pars = [
    ("Base", None), ("Blue Foil", 99), ("Rainbow Foil", 50), ("Canvas", 25),
    ("Wood", 10), ("Silver-Framed", 5), ("Gold-Framed", 1),
    ("Printing Plate Cyan", 1), ("Printing Plate Magenta", 1),
    ("Printing Plate Yellow", 1), ("Printing Plate Black", 1),
]

# On Card Autographs — subject is the character
oca_id = add_is("2025 Masterworks On Card Autographs", is_auto=True)
add_pars(oca_id, auto_pars)
# Characters from the auto checklist (use character names as subjects)
oca_cards = [
    ("A-A","Am"),("A-AA","Bix Caleen"),("A-AB","Jar Jar Binks"),
    ("A-AE","Han Solo"),("A-AK","Alexsandr Kallus"),("A-AT","K-2SO"),
    ("A-BDT","DJ"),("A-BDW","Lando Calrissian"),("A-BL","Kaydel Connix"),
    ("A-BN","Boss Nass"),("A-C","Kelnacca"),("A-CA","Cassian Andor"),
    ("A-CAM","Jedi Master Indara"),("A-CB","Yord Fandar"),("A-CJ","Krrsantan"),
    ("A-CL","Commissioner Helgait"),("A-DB","Jabba The Hutt"),("A-DC","BB-8"),
    ("A-DCC","Torbin"),("A-DF","Hype Fazon"),("A-DG","General Hux"),
    ("A-DK","Jecki Lon"),("A-DL","Wedge Antilles"),("A-DM","Dedra Meero"),
    ("A-DO","Cad Bane"),("A-DR","Rey"),("A-EC","Qi'ra"),("A-EE","Ezra Bridger"),
    ("A-EK","Enfys Nest"),("A-ES","The Armorer"),("A-EW","Jace Rucklin"),
    ("A-F","Finn"),("A-FJ","Jyn Erso"),("A-FPJ","Kanan Jarrus"),
    ("A-FW","Saw Gerrera"),("A-GC","Captain Phasma"),("A-GE","Moff Gideon"),
    ("A-GO","Mon Mothma"),("A-GT","Lok Durd"),("A-HC","Anakin Skywalker"),
    ("A-HO","Hondo Ohnaka"),("A-IM","Emperor Palpatine"),("A-IS","Shin Hati"),
    ("A-JGL","Slowen Lo"),("A-JI","The Grand Inquisitor"),("A-JL","Anakin Skywalker"),
    ("A-JNN","Jod Na Nawood"),("A-JT","Master Codebreaker"),("A-KB","KB"),
    ("A-KK","Sabe"),("A-KL","Kino Loy"),("A-KMT","Rose Tico"),
    ("A-KR","Zorii Bliss"),("A-KS","Bo-Katan Kryze"),("A-L","The Duchess"),
    ("A-LD","Vice Admiral Holdo"),("A-LJJ","Jedi Master Sol"),("A-LL","Bandit Leader"),
    ("A-LM","Grand Admiral Thrawn"),("A-LY","Ahsoka Tano"),("A-MC","Poggle the Lesser"),
    ("A-MEW","Hera Syndulla"),("A-MH","Luke Skywalker"),("A-MJ","The Stranger"),
    ("A-NK","Klaud"),("A-S","Supreme Leader Snoke"),("A-W","Watto"),
    ("A-33","SM-33"),("A-FB","Fifth Brother"),("A-GN","Gha Nachkt"),
    ("A-HAY","Darth Vader"),("A-JAL","Gunter"),("A-MNW","Fennec Shand"),
    ("A-MV","Koska Reeves"),("A-MW","General Grievous"),("A-NA","Jannah"),
    ("A-NLB","Sabine Wren"),("A-OJJ","Kawlan Roken"),("A-PB","Dryden Vos"),
    ("A-RA","Bodhi Rook"),("A-RD","Ahsoka Tano"),("A-RF","The Grand Inquisitor"),
    ("A-RH","Vernestra Rwoh"),("A-RP","Darth Maul"),("A-SC","Ki-Adi-Mundi"),
    ("A-SH","Babu Frik"),("A-SL","Lah Zhima"),("A-SLJ","Mace Windu"),
    ("A-SP","Unkar Plutt"),("A-SS","Luthen Rael"),("A-SW","Maul"),
    ("A-TM","Boba Fett"),("A-TR","Admiral Ackbar"),("A-TW","IG-11"),
    ("A-WD","Wicket W. Warrick"),("A-ZB","Freck"),
]
add_cards(oca_id, oca_cards)
print(f"  2025 Masterworks On Card Autographs: {len(oca_cards)} cards")

# Duo Autographs
duo_pars = [("Base", 25), ("Wood", 10), ("Silver-Framed", 5), ("Gold-Framed", 1)]
duo_id = add_is("Duo Autographs", is_auto=True)
add_pars(duo_id, duo_pars)
add_dual(duo_id, [
    ("DUO-AA","Watto","Jar Jar Binks"),("DUO-DA","Bix Caleen","Dedra Meero"),
    ("DUO-DG","Cassian Andor","Mon Mothma"),("DUO-HS","Mace Windu","Padme Amidala"),
    ("DUO-IF","Saw Gerrera","Moroff"),("DUO-JB","Master Codebreaker","DJ"),
    ("DUO-JBBW","Lando Calrissian","Boba Fett"),("DUO-KA","Syril Karn","Bix Caleen"),
    ("DUO-MD","The Stranger","Jecki Lon"),("DUO-RH","Anakin Skywalker","Ahsoka Tano"),
])
print(f"  Duo Autographs: 10 cards (dual)")

# Trio Autographs
trio_pars = [("Base", 25), ("Wood", 10), ("Silver-Framed", 5), ("Gold-Framed", 1)]
trio_id = add_is("Trio Autographs", is_auto=True)
add_pars(trio_id, trio_pars)
add_triple(trio_id, [
    ("T-AHE","Obi-Wan Kenobi","Anakin Skywalker","C-3PO"),
    ("T-DJA","Rey","C-3PO","Chewbacca"),
    ("T-FAV","Hera Syndulla","Kanan Jarrus","Ahsoka Tano"),
    ("T-NJR","Jod Na Nawood","Neel","SM-33"),
    ("T-STP","Drash","The Mandalorian","Boba Fett"),
])
print(f"  Trio Autographs: 5 cards (triple)")

# Quad Autographs
quad_pars = [("Base", 15), ("Gold", 1)]
quad_id = add_is("Quad Autographs", is_auto=True)
add_pars(quad_id, quad_pars)
add_quad(quad_id, [
    ("Q-CALM","Jedi Master Indara","Jecki Lon","The Stranger","Jedi Master Sol"),
    ("Q-CLOUD","Boba Fett","Darth Vader","Han Solo","Lando Calrissian"),
    ("Q-DAKD","Dedra Meero","Syril Karn","Cassian Andor","Bix Caleen"),
    ("Q-E3","Darth Vader","Darth Sidious","Obi-Wan Kenobi","Mace Windu"),
    ("Q-JNFJ","Captain Brutus","Gunter","Jod Na Nawood","SM-33"),
])
print(f"  Quad Autographs: 5 cards (quad)")

# Ultimate Book Card Autographs (4 multi-signer cards)
ubc_id = add_is("Ultimate Book Card Autographs", is_auto=True)
ubc_pars = [("Silver", 5), ("Gold", 1)]
add_pars(ubc_id, ubc_pars)
add_multi(ubc_id, "UBC-456", ["Boba Fett","Lando Calrissian","The Emperor","Darth Vader","C-3PO","Chewbacca","Leia Organa","Han Solo","Luke Skywalker","Jabba the Hutt"])
add_multi(ubc_id, "UBC-MAN", ["Luke Skywalker","Bo-Katan Kryze","IG-11","Commissioner Helgait","Ahsoka Tano","The Mandalorian","Boba Fett","Moff Gideon","Fennec Shand","Cobb Vanth"])
add_multi(ubc_id, "UBC-REV", ["Clone Commander Cody","C-3PO","Chewbacca","Darth Sidious","Aayla Secura","Obi-Wan Kenobi","Padme Amidala","Anakin Skywalker","Mace Windu","General Grievous"])
add_multi(ubc_id, "UBC-SKY", ["C-3PO","Beaumont Kin","Lando Calrissian","Finn","Nien Nunb","Kaydel Ko Connix","Poe Dameron","BB-8","Rey","Kylo Ren"])
print(f"  Ultimate Book Card Autographs: 4 cards (10 signers each)")

# Harrison Ford Buyback (empty)
add_is("Harrison Ford Buyback On Card Autographs", is_auto=True)
print(f"  Harrison Ford Buyback: empty (buyback subset)")

# ─── RELIC SUBSETS ──────────────────────────────────────────────────────────
# Skeleton Crew Relic
scr_pars = [("Base", 50), ("Purple", 50), ("Red", 25), ("Orange", 10), ("Black", 5), ("Gold", 1)]
scr_id = ins("Skeleton Crew Relic", [
    ("SCR-1","KB"),("SCR-2","Fern"),("SCR-3","Wim"),("SCR-4","Neel"),
    ("SCR-5","Dinghy Driver"),("SCR-6","SM-33"),("SCR-7","Vane"),
    ("SCR-8","Gunter"),("SCR-9","Brutus"),("SCR-10","Jod Na Nawood"),
])
add_pars(scr_id, scr_pars)

# Relic Cards
rel_pars = [("Base", None), ("Green", 99), ("Purple", 50), ("Red", 25), ("Orange", 10), ("Black", 5), ("Gold", 1)]
rel_id = ins("Relic Cards", [
    ("REL-1","The Mandalorian"),("REL-2","Ezra Bridger"),("REL-3","Death Trooper"),
    ("REL-4","Captain Enoch"),("REL-5","Huyang"),("REL-6","Morgan Elsbeth"),
    ("REL-7","Ahsoka Tano"),("REL-8","Sabine Wren"),("REL-9","Jawa"),
    ("REL-10","Moff Gideon"),("REL-11","Cassian Andor"),("REL-12","Dedra Meero"),
])
add_pars(rel_id, rel_pars)

# ROTJ Film Cel Relic (91 cards, 1/1 each)
rotj_id = add_is("ROTJ Film Cel Relic")
add_pars(rotj_id, [("Base", 1)])
rotj_cards = [
    ("ROC-1","Moff Jerjerrod"),("ROC-2","Darth Vader"),("ROC-3","R2-D2"),
    ("ROC-4","C-3PO"),("ROC-5","Bib Fortuna"),("ROC-6","Jabba the Hutt"),
    ("ROC-7","R2-D2"),("ROC-8","Salacious B. Crumb"),("ROC-9","Bib Fortuna"),
    ("ROC-10","Han Solo"),("ROC-11","EV-9D9"),("ROC-12","Sy Snootles"),
    ("ROC-13","Max Rebo"),("ROC-14","C-3PO"),("ROC-15","Chewbacca"),
    ("ROC-16","Boba Fett"),("ROC-17","Lando Calrissian"),("ROC-18","Leia Organa"),
    ("ROC-19","Leia Organa"),("ROC-20","Han Solo"),("ROC-21","Luke Skywalker"),
    ("ROC-22","Gamorrean Guard"),("ROC-23","Malakili"),("ROC-24","R2-D2"),
    ("ROC-25","Luke Skywalker"),("ROC-26","Boba Fett"),("ROC-27","Luke Skywalker"),
    ("ROC-28","Imperial Royal Guard"),("ROC-29","Yoda"),("ROC-30","Luke Skywalker"),
    ("ROC-31","Lando Calrissian"),("ROC-32","Mon Mothma"),("ROC-33","Admiral Ackbar"),
    ("ROC-34","Han Solo"),("ROC-35","The Emperor"),("ROC-36","Chewbacca"),
    ("ROC-37","Leia Organa"),("ROC-38","Luke Skywalker"),("ROC-39","Wicket W. Warrick"),
    ("ROC-40","The Emperor"),("ROC-41","Logray"),("ROC-42","C-3PO"),
    ("ROC-43","Leia Organa"),("ROC-44","C-3PO"),("ROC-45","C-3PO"),
    ("ROC-46","Leia Organa"),("ROC-47","Luke Skywalker"),("ROC-48","Han Solo"),
    ("ROC-49","Sy Snootles"),("ROC-50","Darth Vader"),("ROC-51","Luke Skywalker"),
    ("ROC-52","Wicket W. Warrick"),("ROC-53","Admiral Ackbar"),("ROC-54","Nien Nunb"),
    ("ROC-55","Wicket W. Warrick"),("ROC-56","R2-D2"),("ROC-57","Han Solo"),
    ("ROC-58","Imperial Royal Guard"),("ROC-59","The Emperor"),
    ("ROC-60","Wicket W. Warrick"),("ROC-61","Wedge Antilles"),
    ("ROC-62","Admiral Ackbar"),("ROC-63","The Emperor"),("ROC-64","Logray"),
    ("ROC-65","Admiral Piett"),("ROC-66","Nien Nunb"),("ROC-67","R2-D2"),
    ("ROC-68","Luke Skywalker"),("ROC-69","Chewbacca"),("ROC-70","Darth Vader"),
    ("ROC-71","Han Solo"),("ROC-72","Luke Skywalker"),("ROC-73","The Emperor"),
    ("ROC-74","The Emperor"),("ROC-75","Wedge Antilles"),("ROC-76","Nien Nunb"),
    ("ROC-77","Admiral Ackbar"),("ROC-78","Admiral Piett"),("ROC-79","Luke Skywalker"),
    ("ROC-80","Darth Vader"),("ROC-81","Wedge Antilles"),("ROC-82","Lando Calrissian"),
    ("ROC-83","Nien Nunb"),("ROC-84","Luke Skywalker"),("ROC-85","Han Solo"),
    ("ROC-86","Leia Organa"),("ROC-87","Luke Skywalker"),("ROC-88","Wicket W. Warrick"),
    ("ROC-89","Lando Calrissian"),("ROC-90","Leia Organa"),("ROC-91","Han Solo"),
]
add_cards(rotj_id, rotj_cards)
print(f"  ROTJ Film Cel Relic: {len(rotj_cards)} cards")

# ─── AUTOGRAPH RELIC SUBSETS ────────────────────────────────────────────────
# Skeleton Crew Autograph Relic
scar_pars = [("Base", 10), ("Black", 5), ("Gold", 1)]
scar_id = ins("Skeleton Crew Autograph Relic", [
    ("SCAR-FRO","SM-33"),("SCAR-JAL","Gunter"),("SCAR-KK","KB"),
    ("SCAR-LAWA","Jod Na Nawood"),("SCAR-MAT","Vane"),("SCAR-RCC","Wim"),
    ("SCAR-STS","Neel"),("SCAR-TAT","Brutus"),("SCAR-WIT","Dinghy Driver"),
], is_auto=True)
add_pars(scar_id, scar_pars)

# Autograph Relic Cards
arc_pars = [("Base", 10), ("Black", 5), ("Gold", 1)]
arc_id = ins("Autograph Relic Cards", [
    ("ARC-DAW","Ahsoka Tano"),("ARC-EE","Ezra Bridger"),("ARC-ESP","Moff Gideon"),
    ("ARC-GOU","Dedra Meero"),("ARC-LEE","Morgan Elsbeth"),("ARC-LIU","Sabine Wren"),
    ("ARC-LUNA","Cassian Andor"),("ARC-PAS","The Mandalorian"),("ARC-SHI","Jawa"),
    ("ARC-TEN","Huyang"),("ARC-WES","Captain Enoch"),
], is_auto=True)
add_pars(arc_id, arc_pars)

# ROTJ Film Cel Autograph Relic (33 cards, 1/1 each)
rar_id = add_is("ROTJ Film Cel Autograph Relic", is_auto=True)
add_pars(rar_id, [("Base", 1)])
rar_cards = [
    ("RAR-C3","C-3PO"),("RAR-HA","Luke Skywalker"),("RAR-JB","Boba Fett"),
    ("RAR-MH","Luke Skywalker"),("RAR-PO","C-3PO"),("RAR-TR","Admiral Ackbar"),
    ("RAR-WWW","Wicket W. Warrick"),("RAR-BW","Lando Calrissian"),
    ("RAR-EM","The Emperor"),("RAR-IMD","The Emperor"),("RAR-MC","The Emperor"),
    ("RAR-PIE","Admiral Piett"),("RAR-SW","Simon Williamson"),
    ("RAR-WW","Wicket W. Warrick"),("RAR-BIL","Lando Calrissian"),
    ("RAR-IM","The Emperor"),("RAR-PAL","The Emperor"),
    ("RAR-WIC","Wicket W. Warrick"),("RAR-AD","C-3PO"),
    ("RAR-CAR","Leia Organa"),("RAR-IAN","The Emperor"),
    ("RAR-LU","Luke Skywalker"),("RAR-MQ","Nien Nunb"),("RAR-SO","Han Solo"),
    ("RAR-WI","Wicket W. Warrick"),("RAR-AA","Admiral Ackbar"),
    ("RAR-CAL","Lando Calrissian"),("RAR-HF","Han Solo"),
    ("RAR-LA","Lando Calrissian"),("RAR-MP","Moff Jerjerrod"),
    ("RAR-ROS","Admiral Ackbar"),("RAR-WAR","Wicket W. Warrick"),
]
add_cards(rar_id, rar_cards)
print(f"  ROTJ Film Cel Autograph Relic: {len(rar_cards)} cards")

# Pen Autograph Relic (~75 cards, same character subjects as main autos with slight differences)
par_id = add_is("Pen Autograph Relic", is_auto=True)
add_pars(par_id, [("Base", 1)])
# Insert the same characters from oca_cards minus ~16 excluded + 2 added
pen_excluded = {"A-CB","A-A","A-AT","A-JGL","A-JL","A-LL","A-MV","A-SC","A-SH","A-SL","A-SP","A-FB"}
pen_cards = [(num, name) for num, name in oca_cards if num not in pen_excluded]
pen_cards.append(("A-RCC", "Wim"))
pen_cards.append(("A-VLB", "Leia Organa"))
add_cards(par_id, pen_cards)
print(f"  Pen Autograph Relic: {len(pen_cards)} cards")

# ─── SKETCH CARDS ───────────────────────────────────────────────────────────
sketch_artists = """Adam Beck,Adam D. Perler,Aleksandr Gigov,Alex Mines,Alexander Diab,Allen Geneta,Allen Grimes,Andrew Fernandes,Andrew Fry,Andy Hanks,Angel Aviles,Angelina Benedetti,Anthony Pietszak,Anthony Richichi,Antni Ellison,Ash,Ashley Marsh,AsylumArtz,Basak Kahraman,Bean,Ben AbuSaada,Ben Jones,Benjamin Lombart,Bistek Javier,Bobby Blakey,Bradley Hudson,Brandon Klein,C DUB,C. Deakes,Candice Dailey,Carrie Craggs,Charlie Cody,Chenduz,Chris Colyer,Chris Meeks,Chris Thorne,Christoffer Allen Victoria,Cisco Rivera,Cory Payne CMP,Court,Cyrus Sherkat,Dan Bergren,Dan Cooney,Dan Curto,Dan Gorman,Dan Lawler,Dan Tearle,Daniel Riveron,Darrin Pepe,Dave Gaskin,David Willingham,Dawn Murphy,Don Nguyen,Douglas Stromenger,Dove McHargue,Dwayne Carpenter,DYJ,Dylan Riley,El Smetcho,Elvin A Hernandez,Emre Varlibas,Enso Solo,Eric Lehtonen,Eric Medina,Erik Muller,Frank A. Kadar,Frank Sansone,Franklim Teixeira,Gabe Farber,Gabe Rogue,Gary Shipman,Gawanimayk,Gerry Garcia Jr,Getatom,Ghoulie Julie,Greg Treize,Ian McKesson,Ian Yoshio Roberts,Ink Nerd,Isiah Xavier Bradley,Jaime Lopez,James Boyd,James Harris,Jamie Richards,Jamison Murdock,Jane Rushton,Jason Brower,Jason Christner,Jason Davies,Jason Pearce,Jason Queen,Jason Saldajeno,Jason Sobol,Jay Manchand,Jeffrey C. Benitez,Jenn DePaola,Jenny Kim,Jessica Hickman,Jessica Van Dusen,Jesus,Jiaxin Sun,Jim Dickson,Jim O'Riley,Jodie Rae Charity,Joe Ortiz,John Rodriguez,John Boren,John Bruce,John Still,Jojo Hilario,Jon Mangini,Josh Trout,Juan Rosales,Julia McKenzie,Kang Jing,Karl Jones,Kevin Cleveland,Kevin Graham,Kevin P. West,Kevin Scott Jacobs,Kris Penix,Kyle Babbitt,Laura Inglis,Lee Lightfoot,Leon Braojos,Lily Zapata Mercado,Limuel Pinzon,Lindsey Greyling,Loc Nguyen,Luke Rushton LR,Marcia Dye,Marlo Agunos,Marlo Martos,Mathilde Machuel,Matt Stewart,Matthew Maldonado,Matthew Skillern,Michael Foster,Michael Mastermaker,Michael W. Foreman II,Mike J Sealie,Mike James,Mohammad Jilani,Neil A Brady,Neil Camera,Nick Gribbon,Nik Muggli,Nino John Benitez,Oscar Chavez,Patricio Carrasco,Patrick Giles,Paul Hill,Phillip Trujillo,R.Goto,Randy Siplon,Rebeca Louro,Rees Chua-Finlay,Rich Molinelli,Rich Hennemann,Rico Dela Rosa,RJ Tomascik,Rob Demers,Robert Hendrickson,Rodney Roberts,Roy Cover,Rustico Limosinero,Rusty!,Rutvig Vaid,Ryan Crosby,Ryan Edwards,Ryan Finley,Ryan Johnston,Ryan Olsen,Ryan Thompson,Sammy Gomez,Sandy Meeks,Scott Anthony,Scott Houseman,Scribbling Joe,Sean Earey,Sean Mathews,Shaow Siong,Shyla Lee,Sir Edmund Duke,Snorpixel,Stephane Leonardi,Stephanie Swanger,Steve Alce,Ted Dastick Jr,Tim Shinn,Todd Aaron Smith,Tom Amici,TOMA,Tomoko Taniguchi,Tony Riley,Traci Easterday,Trent Westbrook,Tyler Newcomb,Veronica Louro,Veronica Smith,W Green,Ward Silverman,Will Pleydon,William ROGER,yungmilllz,Yves Van Berlo,Zach Woolsey,Jason""".split(",")

# Create sketch card subsets
for subset_name in ["Sketch Cards", "Sketch Cards Book Cards", "Sketch Cards Panoramic Cards", "Sketch Cards Triptych Cards"]:
    sk_id = add_is(subset_name)
    for artist in sketch_artists:
        artist = artist.strip()
        if not artist:
            continue
        pid = get_or_create(artist, "sketch_artist")
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, NULL)",
                   (pid, sk_id, artist))
    print(f"  {subset_name}: {len(sketch_artists)} artists")

# ─── PACK ODDS JSON ─────────────────────────────────────────────────────────
pack_odds = {"hobby": {
    # Base
    "Base Set": "1:1", "Base Set Blue": "1:1", "Base Set Green": "1:6", "Base Set Purple": "1:11",
    "Base Set Red": "1:22", "Base Set Orange": "1:56", "Base Set Black": "1:113", "Base Set Gold": "1:566",
    "Base Set Printing Plate Cyan": "1:141", "Base Set Printing Plate Magenta": "1:141",
    "Base Set Printing Plate Yellow": "1:141", "Base Set Printing Plate Black": "1:141",
    # Under Disguise
    "Under Disguise": "1:1", "Under Disguise Rainbow Foil": "1:7", "Under Disguise Canvas": "1:87",
    "Under Disguise Wood": "1:217", "Under Disguise Metal": "1:433", "Under Disguise Gold Metal": "1:2,149",
    "Under Disguise Printing Plate Cyan": "1:543", "Under Disguise Printing Plate Magenta": "1:543",
    "Under Disguise Printing Plate Yellow": "1:543", "Under Disguise Printing Plate Black": "1:543",
    # Fall of the Chosen One
    "Fall of the Chosen One": "1:2", "Fall of the Chosen One Rainbow Foil": "1:8",
    "Fall of the Chosen One Canvas": "1:94", "Fall of the Chosen One Wood": "1:234",
    "Fall of the Chosen One Metal": "1:471", "Fall of the Chosen One Gold Metal": "1:2,336",
    "Fall of the Chosen One Printing Plate Cyan": "1:584", "Fall of the Chosen One Printing Plate Magenta": "1:584",
    "Fall of the Chosen One Printing Plate Yellow": "1:584", "Fall of the Chosen One Printing Plate Black": "1:584",
    # Galactic Die Cut Pods
    "Galactic Die Cut Pods": "1:3", "Galactic Die Cut Pods Rainbow Foil": "1:8",
    "Galactic Die Cut Pods Canvas": "1:94", "Galactic Die Cut Pods Wood": "1:234",
    "Galactic Die Cut Pods Printing Plate Cyan": "1:584", "Galactic Die Cut Pods Printing Plate Magenta": "1:584",
    "Galactic Die Cut Pods Printing Plate Yellow": "1:584", "Galactic Die Cut Pods Printing Plate Black": "1:584",
    # Short Circuit
    "Short Circuit": "1:4", "Short Circuit Rainbow Foil": "1:7", "Short Circuit Canvas": "1:87",
    "Short Circuit Wood": "1:217", "Short Circuit Metal": "1:433", "Short Circuit Gold Metal": "1:2,149",
    "Short Circuit Printing Plate Cyan": "1:543", "Short Circuit Printing Plate Magenta": "1:543",
    "Short Circuit Printing Plate Yellow": "1:543", "Short Circuit Printing Plate Black": "1:543",
    # BB-8
    "BB-8": "1:4", "BB-8 Rainbow Foil": "1:19", "BB-8 Colored Metal": "1:119",
    "BB-8 Canvas": "1:225", "BB-8 Wood": "1:566",
    "BB-8 Printing Plate Cyan": "1:1,378", "BB-8 Printing Plate Magenta": "1:1,378",
    "BB-8 Printing Plate Yellow": "1:1,378", "BB-8 Printing Plate Black": "1:1,378",
    # Lothal Jedi Temple
    "Lothal Jedi Temple Mortis Gods Painting Puzzle": "1:160",
    # Buybacks
    "10 Years of Masterworks Buybacks": "1:566",
    # On Card Autographs
    "2025 Masterworks On Card Autographs": "1:2",
    "2025 Masterworks On Card Autographs Blue Foil": "1:16",
    "2025 Masterworks On Card Autographs Rainbow Foil": "1:25",
    "2025 Masterworks On Card Autographs Canvas": "1:48",
    "2025 Masterworks On Card Autographs Wood": "1:76",
    "2025 Masterworks On Card Autographs Silver-Framed": "1:121",
    "2025 Masterworks On Card Autographs Gold-Framed": "1:611",
    "2025 Masterworks On Card Autographs Printing Plate Cyan": "1:179",
    "2025 Masterworks On Card Autographs Printing Plate Magenta": "1:179",
    "2025 Masterworks On Card Autographs Printing Plate Yellow": "1:179",
    "2025 Masterworks On Card Autographs Printing Plate Black": "1:179",
    # Duo Autographs
    "Duo Autographs": "1:1,143", "Duo Autographs Wood": "1:1,414",
    "Duo Autographs Silver-Framed": "1:1,414", "Duo Autographs Gold-Framed": "1:5,373",
    # Trio Autographs
    "Trio Autographs": "1:2,239", "Trio Autographs Wood": "1:5,373",
    "Trio Autographs Silver-Framed": "1:10,746", "Trio Autographs Gold-Framed": "1:10,746",
    # Quad Autographs
    "Quad Autographs": "1:2,239", "Quad Autographs Gold": "1:10,746",
    # Ultimate Book Card
    "Ultimate Book Card Autographs Silver": "1:10,746", "Ultimate Book Card Autographs Gold": "1:13,432",
    # Harrison Ford Buyback
    "Harrison Ford Buyback On Card Autographs": "1:10,746",
    # Skeleton Crew Relic
    "Skeleton Crew Relic": "1:46", "Skeleton Crew Relic Purple": "1:113",
    "Skeleton Crew Relic Red": "1:225", "Skeleton Crew Relic Orange": "1:566",
    "Skeleton Crew Relic Black": "1:119", "Skeleton Crew Relic Gold": "1:5,373",
    # Relic Cards
    "Relic Cards": "1:25", "Relic Cards Green": "1:47", "Relic Cards Purple": "1:94",
    "Relic Cards Red": "1:188", "Relic Cards Orange": "1:471",
    "Relic Cards Black": "1:943", "Relic Cards Gold": "1:4,477",
    # ROTJ Film Cel Relic
    "ROTJ Film Cel Relic": "1:618",
    # Skeleton Crew Autograph Relic
    "Skeleton Crew Autograph Relic": "1:1,414",
    "Skeleton Crew Autograph Relic Black": "1:1,249",
    "Skeleton Crew Autograph Relic Gold": "1:5,570",
    # Autograph Relic Cards
    "Autograph Relic Cards": "1:2,828",
    "Autograph Relic Cards Black": "1:1,033",
    "Autograph Relic Cards Gold": "1:4,884",
    # Film Cel Autograph Relic
    "ROTJ Film Cel Autograph Relic": "1:1,791",
    # Pen Autograph Relic
    "Pen Autograph Relic": "1:672",
    # Sketch Cards
    "Sketch Cards": "1:4",
    "Sketch Cards Book Cards": "1:640",
    "Sketch Cards Panoramic Cards": "1:802",
    "Sketch Cards Triptych Cards": "1:867",
}}

db.execute("UPDATE sets SET pack_odds = ? WHERE id = ?", (json.dumps(pack_odds), SET_ID))
print(f"\nAttached pack odds ({len(pack_odds['hobby'])} keys)")

# ─── Summary ────────────────────────────────────────────────────────────────
db.commit()

total_players = db.execute("SELECT COUNT(*) FROM players WHERE set_id = ?", (SET_ID,)).fetchone()[0]
total_appearances = db.execute("""
    SELECT COUNT(*) FROM player_appearances pa
    JOIN insert_sets ins ON pa.insert_set_id = ins.id WHERE ins.set_id = ?
""", (SET_ID,)).fetchone()[0]
total_subsets = db.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id = ?", (SET_ID,)).fetchone()[0]
total_parallels = db.execute("""
    SELECT COUNT(*) FROM parallels p
    JOIN insert_sets ins ON p.insert_set_id = ins.id WHERE ins.set_id = ?
""", (SET_ID,)).fetchone()[0]
sketch_count = db.execute("SELECT COUNT(*) FROM players WHERE set_id = ? AND subject_role = 'sketch_artist'", (SET_ID,)).fetchone()[0]

print(f"\n{'='*50}")
print(f"Set ID: {SET_ID}")
print(f"Total subsets: {total_subsets}")
print(f"Total unique subjects: {total_players}")
print(f"  - Sketch artists: {sketch_count}")
print(f"  - Characters/scenes: {total_players - sketch_count}")
print(f"Total card appearances: {total_appearances}")
print(f"Total parallels: {total_parallels}")
db.close()
print("Done!")
