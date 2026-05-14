"""
Seed: 2025 Topps Exalted WWE — Full checklist with parallels and pack odds.
100 base, 7 main auto subsets, 6 special auto subsets, 6 memorabilia subsets.
Usage: python3 scripts/seed_exalted_wwe_2025.py
"""
import sqlite3, os, json

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
db = sqlite3.connect(DB_PATH)
db.execute("PRAGMA journal_mode=WAL")
db.execute("PRAGMA foreign_keys=ON")

SET_ID = 60

# ─── Update Set Metadata ────────────────────────────────────────────────────
box_config = json.dumps({
    "hobby": {
        "cards_per_pack": 5,
        "packs_per_box": 1,
        "boxes_per_case": 10,
        "notes": "Per box: 2 autographs + 1 memorabilia + 1 numbered parallel + 1 base card"
    }
})
db.execute("""
    UPDATE sets SET sample_image_url = '/sets/2025-topps-exalted-wwe.jpg',
    release_date = '2026-04-01', box_config = ?, created_at = '2026-05-13T14:00:00Z'
    WHERE id = ?
""", (box_config, SET_ID))
print(f"Updated set ID: {SET_ID}")

H = "Hobby"

def get_or_create(name):
    row = db.execute("SELECT id FROM players WHERE set_id = ? AND name = ?", (SET_ID, name)).fetchone()
    if row: return row[0]
    db.execute("INSERT INTO players (set_id, name, unique_cards, total_print_run, one_of_ones, insert_set_count) VALUES (?, ?, 0, 0, 0, 0)", (SET_ID, name))
    return db.execute("SELECT last_insert_rowid()").fetchone()[0]

def add_is(name):
    db.execute("INSERT INTO insert_sets (set_id, name) VALUES (?, ?)", (SET_ID, name))
    return db.execute("SELECT last_insert_rowid()").fetchone()[0]

def add_par(is_id, name, print_run=None, excl=H):
    db.execute("INSERT INTO parallels (insert_set_id, name, print_run, exclusivity) VALUES (?, ?, ?, ?)",
               (is_id, name, print_run, excl))

def add_pars(is_id, pars):
    for p in pars:
        add_par(is_id, p[0], p[1], p[2] if len(p) > 2 else H)
    return len(pars)

def add_cards(is_id, cards):
    for num, name, team in cards:
        pid = get_or_create(name)
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, ?)",
                   (pid, is_id, str(num), team))

def add_dual_cards(is_id, cards):
    for num, n1, n2 in cards:
        pid1 = get_or_create(n1)
        pid2 = get_or_create(n2)
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, NULL)", (pid1, is_id, str(num)))
        a_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a_id, pid2))

def add_quad_cards(is_id, cards):
    for num, n1, n2, n3, n4 in cards:
        pid1 = get_or_create(n1)
        pid2 = get_or_create(n2)
        pid3 = get_or_create(n3)
        pid4 = get_or_create(n4)
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, NULL)", (pid1, is_id, str(num)))
        a_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a_id, pid2))
        db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a_id, pid3))
        db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a_id, pid4))

# Standard 6-parallel ladder for autos and memorabilia
std_pars = [("Base", None), ("Aqua", 99), ("Green", 50), ("Blue", 25), ("Red", 5), ("Black", 1)]

# ─── BASE SET (100 cards) ───────────────────────────────────────────────────
base_id = add_is("Base Set")
base_pars = [("Base", None), ("Aqua", 99), ("Green", 50), ("Blue", 25), ("White", 150), ("Purple", 10), ("Red", 5), ("Black", 1)]
add_pars(base_id, base_pars)

base_cards = [
    (1,"John Cena","Legend"),(2,"The Rock","Legend"),(3,"Triple H","Legend"),
    (4,"Undertaker","Legend"),(5,"Shawn Michaels","Legend"),
    (6,'"The American Nightmare" Cody Rhodes',"Smackdown"),(7,"Gunther","Raw"),
    (8,"Razor Ramon","Legend"),(9,"Penta","Raw"),(10,"Trish Stratus","Legend"),
    (11,"Stacy Keibler","Legend"),(12,"Kevin Owens","Smackdown"),
    (13,"Ricky Saints","NXT"),(14,"Andrade","Smackdown"),(15,"Bron Breakker","Raw"),
    (16,'"Stone Cold" Steve Austin',"Legend"),(17,"Zaria","NXT"),
    (18,"Kelani Jordan","NXT"),(19,"Lita","Legend"),(20,"Tommaso Ciampa","Smackdown"),
    (21,"Dusty Rhodes","Legend"),(22,"Batista","Legend"),(23,"Eddie Guerrero","Legend"),
    (24,"Liv Morgan","Raw"),(25,"Torrie Wilson","Legend"),(26,"Becky Lynch","Raw"),
    (27,"Kevin Nash","Legend"),(28,"Giulia","Smackdown"),(29,"Lola Vice","NXT"),
    (30,"Jordynne Grace","NXT"),(31,"Jey Uso","Raw"),(32,"Kofi Kingston","Raw"),
    (33,"Ultimate Warrior","Legend"),(34,"Candice LeRae","Smackdown"),
    (35,"Seth Rollins","Raw"),(36,"Kairi Sane","Raw"),(37,"Nikkita Lyons","NXT"),
    (38,"Stephanie Vaquer","Raw"),(39,"Nia Jax","Smackdown"),(40,"Bayley","Raw"),
    (41,"Ludwig Kaiser","Raw"),(42,"Bronson Reed","Raw"),
    (43,"Johnny Gargano","Smackdown"),(44,"Lyra Valkyria","Raw"),
    (45,"Austin Theory","Smackdown"),(46,"Rusev","Raw"),(47,"Lash Legend","NXT"),
    (48,"LA Knight","Smackdown"),(49,"Iyo Sky","Raw"),(50,"Sheamus","Raw"),
    (51,"Jimmy Uso","Smackdown"),(52,"Angelo Dawkins","Smackdown"),
    (53,"The Miz","Smackdown"),(54,"CM Punk","Raw"),(55,"Jacob Fatu","Smackdown"),
    (56,"Wes Lee","NXT"),(57,"Rey Fenix","Smackdown"),(58,"Tony D'Angelo","NXT"),
    (59,"Sami Zayn","Raw"),(60,"Sol Ruca","NXT"),(61,"Finn Balor","Raw"),
    (62,"JD McDonagh","Raw"),(63,"AJ Styles","Raw"),(64,"Blake Monroe","NXT"),
    (65,"Chelsea Green","Smackdown"),(66,"Tiffany Stratton","Smackdown"),
    (67,"Aleister Black","Smackdown"),(68,"Charlotte Flair","Smackdown"),
    (69,"Roxanne Perez","Raw"),(70,"Randy Orton","Smackdown"),
    (71,"Arianna Grace","NXT"),(72,"Carmelo Hayes","Smackdown"),
    (73,"Tonga Loa","Smackdown"),(74,"Pete Dunne","Smackdown"),
    (75,'"Dirty" Dominik Mysterio',"Raw"),(76,"Nathan Frazer","Smackdown"),
    (77,"Axiom","Smackdown"),(78,"Otis","Raw"),(79,"Bianca Belair","Smackdown"),
    (80,"Jade Cargill","Smackdown"),(81,"Ethan Page","NXT"),
    (82,"Naomi","Smackdown"),(83,"Alexa Bliss","Raw"),(84,"Rey Mysterio","Raw"),
    (85,"Chad Gable","Raw"),(86,"Xavier Woods","Raw"),(87,"Solo Sikoa","Smackdown"),
    (88,'Bret "Hit Man" Hart',"Legend"),(89,"Dude Love","Legend"),
    (90,"Trick Williams","NXT"),(91,"R-Truth","Smackdown"),(92,"Asuka","Raw"),
    (93,"Zelina Vega","Smackdown"),(94,"Drew McIntyre","Raw"),
    (95,"Tama Tonga","Smackdown"),(96,"Oba Femi","NXT"),
    (97,"Montez Ford","Smackdown"),(98,"Bray Wyatt","Legend"),
    (99,"Raquel Rodriguez","Raw"),(100,"Roman Reigns","Smackdown"),
]
add_cards(base_id, base_cards)
print(f"  Base Set: {len(base_cards)} cards, {len(base_pars)} parallels")

# ─── MAIN AUTOGRAPH SUBSETS (7 subsets × 6 parallels) ───────────────────────

# Exalted Autographs (47 cards — EXA + EXT prefixes)
exa_id = add_is("Exalted Autographs")
add_pars(exa_id, std_pars)
exa_cards = [
    ("EXA-AND","Andrade","Smackdown"),("EXA-ANG","Angelo Dawkins","Smackdown"),
    ("EXA-ARI","Arianna Grace","NXT"),("EXA-ASU","Asuka","WWE"),
    ("EXA-AVA","Ava","NXT"),("EXA-BEC","Becky Lynch","Raw"),
    ("EXA-BIA","Bianca Belair","Smackdown"),("EXA-CAC","Cactus Jack","Legend"),
    ("EXA-CBO",'"Cowboy" Bob Orton',"Legend"),("EXA-CHA","Charlie Dempsey","NXT"),
    ("EXA-COD",'"The American Nightmare" Cody Rhodes',"Smackdown"),
    ("EXA-DAM","Damian Priest","Smackdown"),("EXA-FAL","Fallon Henley","NXT"),
    ("EXA-GIU","Giulia","Smackdown"),("EXA-IZZ","Izzi Dame","NXT"),
    ("EXA-JAC","Jacy Jayne","NXT"),("EXA-JAI","Jaida Parker","NXT"),
    ("EXA-JAK",'Jake "The Snake" Roberts',"Legend"),("EXA-JOE","Joe Gacy","Smackdown"),
    ("EXA-JOH","John Cena","Legend"),("EXA-JOR","Jordynne Grace","NXT"),
    ("EXA-KUR","Kurt Angle","Legend"),("EXA-LAK","LA Knight","Smackdown"),
    ("EXA-LAS","Lash Legend","NXT"),("EXA-LEX","Lexis King","NXT"),
    ("EXA-MIC","Michelle McCool","Legend"),("EXA-NAT","Nathan Frazer","Smackdown"),
    ("EXA-OTI","Otis","Raw"),("EXA-PET","Karmen Petrovic","NXT"),
    ("EXA-PIP","Piper Niven","Smackdown"),("EXA-RAQ","Raquel Rodriguez","Raw"),
    ("EXA-RHE","Rhea Ripley","Raw"),("EXA-RIC","Ricky Saints","NXT"),
    ("EXA-SAN","Santos Escobar","Smackdown"),("EXA-SET","Seth Rollins","Raw"),
    ("EXA-SHA","Shawn Spears","NXT"),("EXA-TIF","Tiffany Stratton","Smackdown"),
    ("EXA-TOM","Tommaso Ciampa","Smackdown"),("EXA-TRI","Trick Williams","NXT"),
    ("EXA-UND","Undertaker","Legend"),("EXA-XAV","Xavier Woods","Raw"),
    ("EXA-ZAR","Zaria","NXT"),
    # EXT-prefix cards (same subset per source)
    ("EXT-ELT","Elton Prince","Smackdown"),("EXT-IRS","IRS","Legend"),
    ("EXT-KIT","Kit Wilson","Smackdown"),("EXT-MAR","Mark Henry","Legend"),
    ("EXT-NAT","Natalya","Raw"),
]
add_cards(exa_id, exa_cards)
print(f"  Exalted Autographs: {len(exa_cards)} cards")

# Streamline Signatures (21 cards)
sts_id = add_is("Streamline Signatures")
add_pars(sts_id, std_pars)
sts_cards = [
    ("STS-ABS","Alexa Bliss","Smackdown"),("STS-BCD","Brutus Creed","Raw"),
    ("STS-BRD","Bubba Ray Dudley","Legend"),("STS-CMP","CM Punk","Raw"),
    ("STS-DAR","Noam Dar","NXT"),("STS-DMI","Drew McIntyre","Smackdown"),
    ("STS-ERW","Erick Rowan","Smackdown"),("STS-GWR","Grayson Waller","Raw"),
    ("STS-HTM","The Honky Tonk Man","Legend"),("STS-JCD","Julius Creed","Raw"),
    ("STS-JGG","Johnny Gargano","Smackdown"),("STS-KJM","Kiana James","Raw"),
    ("STS-KJN","Kelani Jordan","NXT"),("STS-NLN","Nikkita Lyons","NXT"),
    ("STS-RKO","Randy Orton","Smackdown"),("STS-RKS","Rikishi","Legend"),
    ("STS-RRS","Roman Reigns","Smackdown"),("STS-SMS","Shawn Michaels","Legend"),
    ("STS-SSA",'"Stone Cold" Steve Austin',"Legend"),("STS-ZSK","Zoey Stark","Raw"),
    ("STS-ZVA","Zelina Vega","Raw"),
]
add_cards(sts_id, sts_cards)
print(f"  Streamline Signatures: {len(sts_cards)} cards")

# Ambient Autographs (21 cards — AMA + APA prefixes)
ama_id = add_is("Ambient Autographs")
add_pars(ama_id, std_pars)
ama_cards = [
    ("AMA-BBK","Bron Breakker","Raw"),("AMA-BRT","Booker T","Legend"),
    ("AMA-CGN","Chelsea Green","Smackdown"),("AMA-HKH","Hulk Hogan","Legend"),
    ("AMA-JCG","Jade Cargill","Smackdown"),("AMA-JZN","Jazmyn Nyx","NXT"),
    ("AMA-LKR","Ludwig Kaiser","Raw"),("AMA-LOA","Tonga Loa","Smackdown"),
    ("AMA-LVC","Lola Vice","NXT"),("AMA-LVE","Lyra Valkyria","Raw"),
    ("AMA-MXD","Maxxine Dupri","Raw"),("AMA-PDE","Pete Dunne","Raw"),
    ("AMA-RDJ","Road Dogg Jesse James","Legend"),("AMA-SKB","Stacy Keibler","Legend"),
    ("AMA-TSS","Trish Stratus","Legend"),("AMA-TWN","Torrie Wilson","Legend"),
    ("AMA-WCO","Wendy Choo","NXT"),("AMA-XPC","X-Pac","Legend"),
    # APA-prefix cards belonging to Ambient (not Apparition)
    ("APA-ADR","Adriana Rizzo","NXT"),("APA-JCF","Jacob Fatu","Smackdown"),
    ("APA-OBA","Oba Femi","NXT"),
]
add_cards(ama_id, ama_cards)
print(f"  Ambient Autographs: {len(ama_cards)} cards")

# Insignia Ink (19 cards)
ini_id = add_is("Insignia Ink")
add_pars(ini_id, std_pars)
ini_cards = [
    ("INI-AJS","AJ Styles","Smackdown"),("INI-BLY","Bayley","Raw"),
    ("INI-CMP","CM Punk","Raw"),("INI-CRS",'"The American Nightmare" Cody Rhodes',"Smackdown"),
    ("INI-DME","Drew McIntyre","Raw"),("INI-DPT","Damian Priest","Smackdown"),
    ("INI-DRJ","The Rock","Legend"),("INI-JCA","John Cena","Legend"),
    ("INI-KOS","Kevin Owens","Smackdown"),("INI-LAK","LA Knight","Smackdown"),
    ("INI-LMN","Liv Morgan","Raw"),("INI-MIZ","The Miz","Raw"),
    ("INI-RRS","Roman Reigns","Smackdown"),("INI-RRY","Rhea Ripley","Raw"),
    ("INI-SCS",'"Stone Cold" Steve Austin',"Legend"),("INI-SFR","Seth Rollins","Raw"),
    ("INI-SHS","Sheamus","Smackdown"),("INI-TSN","Tiffany Stratton","Smackdown"),
    ("INI-UTR","Undertaker","Legend"),
]
add_cards(ini_id, ini_cards)
print(f"  Insignia Ink: {len(ini_cards)} cards")

# Elevated Ink (29 cards)
eli_id = add_is("Elevated Ink")
add_pars(eli_id, std_pars)
eli_cards = [
    ("ELI-ATY","Austin Theory","Smackdown"),("ELI-AXM","Axiom","Smackdown"),
    ("ELI-BHH",'Bret "Hit Man" Hart',"Legend"),("ELI-BRD","Bronson Reed","Raw"),
    ("ELI-BRT","Booker T","Legend"),("ELI-CFR","Charlotte Flair","Smackdown"),
    ("ELI-DDM",'"Dirty" Dominik Mysterio',"Raw"),("ELI-DDP","Diamond Dallas Page","Legend"),
    ("ELI-DNL","Dragon Lee","Raw"),("ELI-FBR","Finn Balor","Raw"),
    ("ELI-IDV","Ilja Dragunov","Raw"),("ELI-IYO","Iyo Sky","Raw"),
    ("ELI-JCL","Jade Cargill","Smackdown"),("ELI-JDM","JD McDonagh","Raw"),
    ("ELI-JUO","Jey Uso","Raw"),("ELI-KKN","Kofi Kingston","Raw"),
    ("ELI-KSE","Kairi Sane","Raw"),("ELI-LTA","Lita","Legend"),
    ("ELI-MFD","Montez Ford","Smackdown"),("ELI-NJX","Nia Jax","Smackdown"),
    ("ELI-PEN","Penta","Raw"),("ELI-RMO","Rey Mysterio","Raw"),
    ("ELI-RON","Randy Orton","Smackdown"),("ELI-RSR","Rick Steiner","Legend"),
    ("ELI-RVD","Rob Van Dam","Legend"),("ELI-SMS","Shawn Michaels","Legend"),
    ("ELI-SSR","Scott Steiner","Legend"),("ELI-SZN","Sami Zayn","Raw"),
    ("ELI-TSS","Trish Stratus","Legend"),
]
add_cards(eli_id, eli_cards)
print(f"  Elevated Ink: {len(eli_cards)} cards")

# Black and White Signatures (19 cards)
bws_id = add_is("Black and White Signatures")
add_pars(bws_id, std_pars)
bws_cards = [
    ("BWS-ABK","Aleister Black","Smackdown"),("BWS-ASY","Alex Shelley","Smackdown"),
    ("BWS-BBR","Bianca Belair","Smackdown"),("BWS-BLY","Becky Lynch","Raw"),
    ("BWS-CGE","Chad Gable","Raw"),("BWS-CHS","Carmelo Hayes","Smackdown"),
    ("BWS-CSN","Chris Sabin","Smackdown"),("BWS-DSL","Diesel","Legend"),
    ("BWS-GNT","Gunther","Raw"),("BWS-JBL","JBL","Legend"),
    ("BWS-JIM","Jimmy Uso","Smackdown"),("BWS-KNE","Kane","Legend"),
    ("BWS-RFX","Rey Fenix","Smackdown"),("BWS-RPZ","Roxanne Perez","Raw"),
    ("BWS-RTH","R-Truth","Smackdown"),("BWS-RUS","Rusev","Raw"),
    ("BWS-SNK","Shinsuke Nakamura","Smackdown"),("BWS-SSK","Solo Sikoa","Smackdown"),
    ("BWS-SVR","Stephanie Vaquer","Raw"),
]
add_cards(bws_id, bws_cards)
print(f"  Black and White Signatures: {len(bws_cards)} cards")

# Apparition Autographs (21 cards — APA prefix, distinct from APA cards in Ambient)
apa_id = add_is("Apparition Autographs")
add_pars(apa_id, std_pars)
apa_cards = [
    ("APA-AFY","Alba Fyre","Smackdown"),("APA-BRC","Brinley Reece","NXT"),
    ("APA-CKY","Cathy Kelley","Raw"),("APA-CLR","Candice LeRae","Smackdown"),
    ("APA-DLM","Dexter Lumis","Smackdown"),("APA-EPG","Ethan Page","NXT"),
    ("APA-EVE","Eve","Legend"),("APA-IVA","Ivar","Raw"),("APA-IVY","Ivy Nile","Raw"),
    ("APA-JBL","JBL","Legend"),("APA-LEX","Lex Luger","Legend"),
    ("APA-LLD","Lash Legend","NXT"),("APA-NCS","Nikki Cross","Smackdown"),
    ("APA-OMS","Omos","WWE"),("APA-SOL","Sol Ruca","NXT"),
    ("APA-TDA","Tony D'Angelo","NXT"),
    ("APA-TDB",'"Million Dollar Man" Ted DiBiase',"Legend"),
    ("APA-THL","Thea Hail","NXT"),("APA-TPY","Tatum Paxley","NXT"),
    ("APA-TSM","The Sandman","Legend"),("APA-YIM","Michin","Smackdown"),
]
add_cards(apa_id, apa_cards)
print(f"  Apparition Autographs: {len(apa_cards)} cards")

# ─── SPECIAL AUTOGRAPH SUBSETS ──────────────────────────────────────────────

# John Cena: The Last Time Is Now Autograph (1 card)
jcfa_id = add_is("John Cena: The Last Time Is Now Autograph")
jcfa_pars = [("Aqua", 99), ("Green", 50), ("Blue", 25), ("Red", 5), ("Black", 1)]
add_pars(jcfa_id, jcfa_pars)
add_cards(jcfa_id, [("JCFA-JC", "John Cena", "WWE")])
print(f"  John Cena: The Last Time Is Now Autograph: 1 card, {len(jcfa_pars)} parallels")

# Celebrating Cena Autographs (4 cards, base /10, no parallel ladder)
cca_id = add_is("Celebrating Cena Autographs")
add_cards(cca_id, [
    ("CCA-18","John Cena","WWE"),("CCA-19","John Cena","WWE"),
    ("CCA-20","John Cena","WWE"),("CCA-21","John Cena","WWE"),
])
print(f"  Celebrating Cena Autographs: 4 cards (base /10, no parallels)")

# The Rock Retrospective Autographs (2 cards, base /10)
rra_id = add_is("The Rock Retrospective Autographs")
rra_pars = [("Red Refractor", 5), ("Superfractor", 1)]
add_pars(rra_id, rra_pars)
add_cards(rra_id, [("RRA-6","The Rock","Legend"),("RRA-7","The Rock","Legend")])
print(f"  The Rock Retrospective Autographs: 2 cards, {len(rra_pars)} parallels")

# Triple H Tribute Autographs (3 cards, base /10, no parallels)
tta_id = add_is("Triple H Tribute Autographs")
add_cards(tta_id, [
    ("TTA-9","Triple H","Legend"),("TTA-10","Triple H","Legend"),("TTA-11","Triple H","Legend"),
])
print(f"  Triple H Tribute Autographs: 3 cards (base /10, no parallels)")

# Superstar Rivalry Signatures (2 dual-subject cards, base /5)
ssr_id = add_is("Superstar Rivalry Signatures")
ssr_pars = [("Superfractor", 1)]
add_pars(ssr_id, ssr_pars)
add_dual_cards(ssr_id, [
    ("SSR-TR", "Triple H", "The Rock"),
    ("SSR-TS", "Triple H", "Shawn Michaels"),
])
print(f"  Superstar Rivalry Signatures: 2 cards (dual), {len(ssr_pars)} parallels")

# Superstar Rivalry Variation Signatures (1 dual-subject card, base /25)
rsv_id = add_is("Superstar Rivalry Variation Signatures")
rsv_pars = [("Black Refractor", 10), ("Red Refractor", 5), ("Superfractor", 1)]
add_pars(rsv_id, rsv_pars)
add_dual_cards(rsv_id, [("RSV-ST", "Stephanie McMahon", "Trish Stratus")])
print(f"  Superstar Rivalry Variation Signatures: 1 card (dual), {len(rsv_pars)} parallels")

# ─── MEMORABILIA SUBSETS ────────────────────────────────────────────────────

# Exalted Relics (49 cards)
er_id = add_is("Exalted Relics")
add_pars(er_id, std_pars)
er_cards = [
    ("ER-ABS","Alexa Bliss","Raw"),("ER-ADS","Angelo Dawkins","Smackdown"),
    ("ER-AGE","Arianna Grace","NXT"),("ER-AND","Andrade","Smackdown"),
    ("ER-ATY","Austin Theory","Smackdown"),("ER-BBR","Bianca Belair","Smackdown"),
    ("ER-BLH","Becky Lynch","Raw"),("ER-BRD","Bronson Reed","Raw"),
    ("ER-BSN","Braun Strowman","Smackdown"),("ER-CAR","Carlito","Raw"),
    ("ER-CLE","Candice LeRae","Smackdown"),("ER-DKI","Dakota Kai","Raw"),
    ("ER-DLE","Dragon Lee","Raw"),("ER-DLS","Dexter Lumis","Smackdown"),
    ("ER-ERN","Erick Rowan","Smackdown"),("ER-GDN","Gigi Dolin","NXT"),
    ("ER-JES","Je'Von Evans","NXT"),("ER-JGE","Jordynne Grace","NXT"),
    ("ER-JGY","Joe Gacy","Smackdown"),("ER-KJN","Kelani Jordan","NXT"),
    ("ER-KKN","Kofi Kingston","Raw"),("ER-KKS","Karrion Kross","Raw"),
    ("ER-LKG","Lexis King","NXT"),("ER-LKR","Ludwig Kaiser","Raw"),
    ("ER-LVA","Lyra Valkyria","Raw"),("ER-LVE","Lola Vice","NXT"),
    ("ER-MDI","Maxxine Dupri","Raw"),("ER-MFD","Montez Ford","Smackdown"),
    ("ER-MIC","Michin","Smackdown"),("ER-NAO","Naomi","Smackdown"),
    ("ER-NCS","Nikki Cross","Smackdown"),("ER-NJX","Nia Jax","Smackdown"),
    ("ER-OTI","Otis","Raw"),("ER-PEN","Penta","Raw"),("ER-RMO","Rey Mysterio","Raw"),
    ("ER-RRZ","Raquel Rodriguez","Raw"),("ER-SFR","Seth Rollins","Raw"),
    ("ER-SHE","Sheamus","Raw"),("ER-SNA","Shinsuke Nakamura","Smackdown"),
    ("ER-SRA","Sol Ruca","NXT"),("ER-SSS","Shawn Spears","NXT"),
    ("ER-SVR","Stephanie Vaquer","Raw"),("ER-TBE","Tyler Bate","Raw"),
    ("ER-THL","Thea Hail","NXT"),("ER-TMZ","The Miz","Raw"),
    ("ER-UWY","Uncle Howdy","Smackdown"),("ER-WLE","Wes Lee","NXT"),
    ("ER-XWS","Xavier Woods","Raw"),("ER-ZVA","Zelina Vega","Smackdown"),
]
add_cards(er_id, er_cards)
print(f"  Exalted Relics: {len(er_cards)} cards")

# Mega Materials (25 cards)
mm_id = add_is("Mega Materials")
add_pars(mm_id, std_pars)
mm_cards = [
    ("MM-AB","Alexa Bliss","Smackdown"),("MM-CF","Charlotte Flair","Smackdown"),
    ("MM-CH","Carmelo Hayes","Smackdown"),("MM-CM","CM Punk","Raw"),
    ("MM-CR",'"The American Nightmare" Cody Rhodes',"Smackdown"),
    ("MM-DM","Drew McIntyre","Smackdown"),("MM-DP","Damian Priest","Smackdown"),
    ("MM-EP","Ethan Page","NXT"),("MM-GR","Gunther","Raw"),
    ("MM-JC","John Cena","WWE"),("MM-JF","Jacob Fatu","Smackdown"),
    ("MM-JL","Jade Cargill","Smackdown"),("MM-JU","Jimmy Uso","Smackdown"),
    ("MM-JY","Jey Uso","Raw"),("MM-KO","Kevin Owens","Smackdown"),
    ("MM-LA","LA Knight","Smackdown"),("MM-LM","Liv Morgan","Raw"),
    ("MM-RO","Randy Orton","Smackdown"),("MM-RP","Roxanne Perez","Raw"),
    ("MM-RR","Roman Reigns","Smackdown"),("MM-SS","Solo Sikoa","Smackdown"),
    ("MM-TL","Tonga Loa","Smackdown"),("MM-TS","Tiffany Stratton","Smackdown"),
    ("MM-TT","Tama Tonga","Smackdown"),("MM-TW","Trick Williams","NXT"),
]
add_cards(mm_id, mm_cards)
print(f"  Mega Materials: {len(mm_cards)} cards")

# Rivaled Relics (10 dual-subject)
rr_id = add_is("Rivaled Relics")
add_pars(rr_id, std_pars)
add_dual_cards(rr_id, [
    ("RR-BD","Ilja Dragunov","Bron Breakker"),("RR-BS","Bayley","Iyo Sky"),
    ("RR-KS","AJ Styles","LA Knight"),("RR-ME","Santos Escobar","Rey Mysterio"),
    ("RR-MP","CM Punk","Drew McIntyre"),("RR-RG","Seth Rollins","Gunther"),
    ("RR-RM","Liv Morgan","Rhea Ripley"),
    ("RR-RR","Roman Reigns",'"The American Nightmare" Cody Rhodes'),
    ("RR-UU","Jimmy Uso","Jey Uso"),("RR-ZG","Chad Gable","Sami Zayn"),
])
print(f"  Rivaled Relics: 10 cards (dual)")

# Tag Team Relics (10 dual-subject)
tt_id = add_is("Tag Team Relics")
add_pars(tt_id, std_pars)
add_dual_cards(tt_id, [
    ("TT-AS","Kairi Sane","Asuka"),("TT-BC","Bianca Belair","Jade Cargill"),
    ("TT-BS","Shayna Baszler","Zoey Stark"),("TT-CC","Kayden Carter","Katana Chance"),
    ("TT-CG","Johnny Gargano","Tommaso Ciampa"),("TT-FA","Axiom","Nathan Frazer"),
    ("TT-FD","Montez Ford","Angelo Dawkins"),("TT-NG","Piper Niven","Chelsea Green"),
    ("TT-SS","Chris Sabin","Alex Shelley"),("TT-WP","Elton Prince","Kit Wilson"),
])
print(f"  Tag Team Relics: 10 cards (dual)")

# Quad Relics (5 quad-subject)
qr_id = add_is("Quad Relics")
add_pars(qr_id, std_pars)
add_quad_cards(qr_id, [
    ("QR-HRLG","Uncle Howdy","Dexter Lumis","Joe Gacy","Erick Rowan"),
    ("QR-MBMC","Finn Balor","Carlito","JD McDonagh",'"Dirty" Dominik Mysterio'),
    ("QR-PVJJ","Lola Vice","Roxanne Perez","Cora Jade","Kelani Jordan"),
    ("QR-PWFE","Trick Williams","Je'Von Evans","Ethan Page","Oba Femi"),
    ("QR-SFTL","Jacob Fatu","Tama Tonga","Tonga Loa","Solo Sikoa"),
])
print(f"  Quad Relics: 5 cards (quad)")

# John Cena: The Last Time Is Now Relic (1 card)
jfcr_id = add_is("John Cena: The Last Time Is Now Relic")
jfcr_pars = [("Aqua", 99), ("Green", 50), ("Blue", 25), ("Red", 5), ("Black", 1)]
add_pars(jfcr_id, jfcr_pars)
add_cards(jfcr_id, [("JFCR-JC", "John Cena", "WWE")])
print(f"  John Cena: The Last Time Is Now Relic: 1 card, {len(jfcr_pars)} parallels")

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

print(f"\n{'='*50}")
print(f"Set ID: {SET_ID}")
print(f"Total subsets: {total_subsets}")
print(f"Total unique players: {total_players}")
print(f"Total card appearances: {total_appearances}")
print(f"Total parallels: {total_parallels}")
print(f"Expected: 390 cards")
db.close()
print("Done!")
