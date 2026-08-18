# -*- coding: utf-8 -*-
"""
Seed 2026 Topps Mint Marvel (Phase 1 + published parallels) into local SQLite.
Structure + 480 cards + 72 parallels (published runs + exclusivities). NO pack odds
(odds PDF unpublished). NO box config (unpublished). Local SQLite only; Tyler migrates.

Modeling notes (from preflight):
  * insert_sets flag col is `is_autograph` (prompt's is_autograph_subset).
  * exclusivity stored verbatim in parallels.exclusivity (string).
  * code-less Sketch Cards use card_number='' (NOT NULL col; '' is the code-less
    convention, 64 existing rows) -- codes are NOT invented.
  * Marvel Studios actor autographs: subset_tag = "as {character}" (the established
    format; property is NOT part of it -- flagged in the run report, not invented).
  * Spider-Man Comic Cuts: subject/player = "Spider-Man" (all 15); the printed issue
    goes in subset_tag (only per-appearance label field).
  * Chrome tiers reuse the identical 125-card Base checklist (per source).
"""
import os, sqlite3

DB = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")

SET = dict(
    name="2026 Topps Mint Marvel", sport="Entertainment", season="2026", league="Marvel",
    tier="Premium", sample_image_url="/sets/2026-topps-mint-marvel.jpg",
    release_date="2026-08-19", slug="2026-topps-mint-marvel", is_visible=1,
    created_at="2026-08-17 12:00:00",
    topps_url="https://www.topps.com/pages/topps-mint-marvel",
)

# (name, is_base, is_relic, is_autograph, is_booklet) -- explicit
SUBSETS = [
    ("Base – Bronze", 1, 0, 0, 0),
    ("Base – Silver", 1, 0, 0, 0),
    ("Base – Gold", 1, 0, 0, 0),
    ("Base – Platinum", 1, 0, 0, 0),
    ("Chrome – Bronze", 1, 0, 0, 0),
    ("Chrome – Silver", 1, 0, 0, 0),
    ("Chrome – Gold", 1, 0, 0, 0),
    ("Chrome – Platinum", 1, 0, 0, 0),
    ("SDCC Exclusive Art Cards", 0, 0, 0, 0),
    ("Mass Symbiote Takeover", 0, 0, 0, 0),
    ("Cerebro", 0, 0, 0, 0),
    ("Chrome Autographs – Comic Creators", 0, 0, 1, 0),
    ("Chrome Autographs – Marvel Studios", 0, 0, 1, 0),
    ("Marvel Cut Signature", 0, 0, 1, 0),
    ("Spider-Man Comic Cuts", 0, 1, 0, 0),
    ("Sketch Cards", 0, 0, 0, 0),
]

DASH = "–"  # en dash used in tier subset names
def B(t): return f"Base {DASH} {t}"
def C(t): return f"Chrome {DASH} {t}"

# ---- 125-card base checklist (code -> name); Bronze 1-50, Silver 51-75, Gold 76-100, Platinum 101-125
BASE125 = [
 "The Thing","Eternity","Colossus","Baron Zemo","Groot","Elektra","Man-Thing","Squirrel Girl","Nick Fury","Thena",
 "Corruption","Lockjaw","Ghost-Spider","Phoenix","Dormammu","Bishop","Winter Soldier","Mr. Sinister","Spider-Ham","Scarlet Witch",
 "Black Knight","Kraven the Hunter","Red Hulk","Enchantress","Spider-Man 2099","Infinity","Luke Cage","Scarlet Spider","Drax","Green Goblin",
 "Mysterio","Dazzler","Wiccan","Beta Ray Bill","Carnage","Spider-Punk","Juggernaut","Cable","Doomasaur","Ant-Man",
 "Mephisto","Wasp","Hobgoblin","Rocket Raccoon","Black Winter","Iron Fist","Jubilee","Gwenpool","Ms. Marvel","She-Hulk",
 "Blue Marvel","Cloak & Dagger","Major League Venom","Mighty Thor","The Prowler","Blade","Emma Frost","Black Bolt","Gambit","Vision",
 "Iceman","Taskmaster","Magik","Silver Sable","Ultron","Black Widow","Spider-Man Noir","Black Cat","Mister Fantastic","Kate Bishop",
 "Phantom Rider","Hawkeye","Spider-Girl","Invisible Woman","Captain America (Sam Wilson)",
 "Daredevil","Shang-Chi","Bullseye","Sentry","Howard the Duck","Beast","Iron Patriot","Gamora","Killmonger","Rogue",
 "Wonder Man","Human Torch","Kitty Pryde","Nova","Doctor Strange","Adam Warlock","Doctor Octopus","Kingpin","Captain Marvel","Odin",
 "Star-Lord","Nightcrawler","Annihilus","Ghost Rider","Electro",
 "Black Panther","Venom","Spider-Man","Cyclops","Sabretooth","Loki","Storm","Jean Grey","Silver Surfer","Captain America",
 "Miles Morales","Hulk","Thor","Apocalypse","Moon Knight","Galactus","Thanos","Iron Man","Namor","Spider-Woman",
 "Wolverine","Doctor Doom","Jeff the Land Shark","Professor X","Magneto",
]
assert len(BASE125) == 125, len(BASE125)

def tier_for(code):  # code is 1-based int
    if code <= 50: return "Bronze"
    if code <= 75: return "Silver"
    if code <= 100: return "Gold"
    return "Platinum"

SDCC = [("SDCC-H","Hulk"),("SDCC-P","Punisher"),("SDCC-S","Spider-Man")]

MST = [  # code, name
 ("MS-1","Knull"),("MS-2","Venom"),("MS-3","Major League Venom"),("MS-4","Scorpion"),("MS-5","Riot"),
 ("MS-6","Carnage"),("MS-7","Agent Venom"),("MS-8","Mania"),("MS-9","Scream"),("MS-10","She-Venom"),
 ("MS-11","Symbiote Spider-Man 2099"),("MS-12","Silence"),("MS-13","Venom 2099"),("MS-14","Agony"),
 ("MS-15","Jeff the Venomized Land Shark"),("MS-16","Phage"),("MS-17","Sleeper"),("MS-18","Scorn"),
 ("MS-19","Grendel"),("MS-20","Wolverine"),("MS-21","Lasher"),("MS-22","Toxin"),("MS-23","Anti-Venom"),
 ("MS-24","Red Goblin"),("MS-25","Spider-Man"),("MS-26","Mary Jane"),("MS-27","Misery"),("MS-28","Black Cat"),
 ("MS-29","Widow"),("MS-30","Loki"),
]

CEREBRO = [
 "Professor X","Quicksilver","Hulk","Doctor Doom","Wolverine","Blade","Scarlet Witch","Havok","Doctor Strange","Storm",
 "Cable","The Thing","Rogue","Moon Knight","Magneto","Kitty Pryde","Ghost Rider","Iceman","Jean Grey","Miles Morales",
 "Forge","Mister Fantastic","Cyclops","Angel","Captain America","Thanos","Nightcrawler","Beast","Mystique","Hope Summers",
 "X-23","Apocalypse","Colossus","Sabretooth","Legion","Gambit","Human Torch","Polaris","Domino","Phoenix",
 "Daredevil","Rachel Summers","Thor","Magik","Jubilee","Emma Frost","Psylocke","Bishop","Juggernaut","Spider-Man",
 "Black Widow","Venom","Onslaught","Invisible Woman","Black Panther",
]
assert len(CEREBRO) == 55

CREATORS = [  # code, name
 ("CA-AAD","Arthur Adams"),("CA-AG","Adi Granov"),("CA-AK","Adam Kubert"),("CA-ANK","Andy Kubert"),
 ("CA-BS","Bill Sienkiewicz"),("CA-CK","Craig Kyle"),("CA-CY","Christopher Yost"),("CA-DCT","Donny Cates"),
 ("CA-FM","Frank Miller"),("CA-GC","Greg Capullo"),("CA-JAA","Jason Aaron"),("CA-JC","Joshua Cassara"),
 ("CA-JH","Jonathan Hickman"),("CA-LP","Lucio Parrillo"),("CA-MB","Mark Brooks"),("CA-MBA","Mark Bagley"),
 ("CA-MS","Marc Silvestri"),("CA-MZ","Mike Zeck"),("CA-PM","Paco Medina"),("CA-RO","Ryan Ottley"),
 ("CA-RRS","Rod Reis"),("CA-RS","Ryan Stegman"),("CA-SM","Steve McNiven"),("CA-SW","Scott Williams"),
 ("CA-TD","Tony Daniel"),("CA-WP","Whilce Portacio"),("CA-ZW","Zeb Wells"),
]
assert len(CREATORS) == 27

STUDIOS = [  # code, name, character (tag), property (flagged; not stored in tag)
 ("CA-BC","Bradley Cooper","Rocket","Guardians of the Galaxy Vol. 2"),
 ("CA-HS","Hailee Steinfeld","Kate Bishop","Hawkeye"),
 ("CA-HJ","Hugh Jackman","Wolverine","Deadpool & Wolverine"),
 ("CA-OI","Oscar Isaac","Moon Knight","Moon Knight"),
 ("CA-SLJ","Samuel L. Jackson","Nick Fury","Marvel's The Avengers"),
 ("CA-VDO","Vincent D'Onofrio","Mayor Wilson Fisk","Daredevil: Born Again"),
]

CUTSIG = [("CS-SL","Stan Lee")]

COMICCUTS = [  # code, issue (subject = Spider-Man for all)
 ("CC-ASM5","The Amazing Spider-Man (1963) #5"),("CC-ASM16","The Amazing Spider-Man (1963) #16"),
 ("CC-ASM20","The Amazing Spider-Man (1963) #20"),("CC-ASM100","The Amazing Spider-Man (1963) #100"),
 ("CC-ASM101","The Amazing Spider-Man (1963) #101"),("CC-ASM134","The Amazing Spider-Man (1963) #134"),
 ("CC-ASM345","The Amazing Spider-Man (1963) #345"),("CC-DD16","Daredevil (1964) #16"),
 ("CC-MTU27","Marvel Team-Up (1972) #27"),("CC-MTU43","Marvel Team-Up (1972) #43"),
 ("CC-MTU53","Marvel Team-Up (1972) #53"),("CC-MTU54","Marvel Team-Up (1972) #54"),
 ("CC-MTU150","Marvel Team-Up (1972) #150"),("CC-MTUA1","Marvel Team-Up Annual (1976) #1"),
 ("CC-UXM35","Uncanny X-Men (1963) #35"),
]
assert len(COMICCUTS) == 15

SKETCH = [
 "Adam Fields","Adam Harris","Aditya Chandra","Al Stefano","Alcione Silva","Alessandro Micelli","Allen Serrano",
 "Andy Tiu","Angelo De Capua","Ariel Aguire","Brent Ragland","Carlo Allen Victoria","Charlie Cody","Chris Botterill",
 "Chris Meeks","Christoffer Allen Victoria","Christopher Foreman","Cisco Rivera","Daniel M Chavez","Daniel Riveron",
 "Danishson Borgonos","Darrin Pepe","Débora Centeio","Dexter Wee","Don Mark Noceda","Dove Mchargue","Duke","DYJ",
 "Dylan Riley","Elisa Raffaelli","Elisabete Silva","Elvin Hernandez","Emmanuel Villafaña \"Emmvill\"","Eric Lehtonen",
 "Ernest Romero","Fabio Ramacci","Frank A. Kadar","Franklim Teixeira","Gener Pedrina","George Vega","Gilbert Perez",
 "Greg Treize","Hector Barros","Honeybee Federeso","Ian Quirante","Ian Sateikis","Isiah Bradley","Jason Queen",
 "Jason Christner","Jason Rodriguez","Jason Saldajeno","Jason Sobol","Jessica Court","Jessica Hickman","Jezreel Rojales",
 "Jiaxin \"Yinshan\" Sun","Jim O'riley","John Pleak","John Paul Howard","Johnruzel Jimenez","José David Lima Da Silva",
 "Joshua Nunez","Lauro Santiago","Lee Lightfoot","Leon Braojos","Lucas Ackerman","Marcelino Servicio","Marcia Dye",
 "Marlo Martos","Matt Stewart","Michael Mastermaker","Mirko Di Noia","Mohammad Jilani","Nathan Nelson","Nick Gribbon",
 "Noval Hernawan","Patricio Carrasco","Percival Kholoma","Rich Hennemann","Richard Valbuena","Robert Blancas",
 "Robert Demers","Roberto Mamani","Ronel Gravo","Rustico Limosinero Jr.","Sherwin Santiago","Stephane Leonardi",
 "Steve Alce","Sturdy","Tim Shinn","Toma","Uko Smith","Vincenzo D'ippolito",
]
assert len(SKETCH) == 93

# ---- parallels (72): (subset, name, print_run, exclusivity)
def base_ladder(sub):
    return [
     (sub,"Sky Blue Foil",100,None),(sub,"Green Mint Foil",75,None),(sub,"Gold Foil",50,None),
     (sub,"Orange Diamante Foil",25,"Hobby Box Exclusive"),(sub,"Orange Foil",25,None),
     (sub,"Black Foil",10,None),(sub,"Black & Yellow Electric Dots Foil",10,"SDCC Exclusive"),
     (sub,"Red Diamante Foil",5,"Hobby Box Exclusive"),(sub,"Red Foil",5,None),(sub,"Foilfractor",1,None),
    ]
def chrome_ladder(sub, base_run):
    return [(sub,"Black Refractor",10,None),(sub,"Red Refractor",5,None),(sub,"Superfractor",1,None),(sub,"Base",base_run,None)]

PARALLELS = []
for t in ("Bronze","Silver","Gold"): PARALLELS += base_ladder(B(t))
PARALLELS += [(B("Platinum"),"Black Electric Dots Foil",10,"Hobby Exclusive"),
              (B("Platinum"),"Red Foil",5,None),(B("Platinum"),"Foilfractor",1,None),
              (B("Platinum"),"Base",99,None)]
PARALLELS += chrome_ladder(C("Bronze"),100)
PARALLELS += chrome_ladder(C("Silver"),75)
PARALLELS += chrome_ladder(C("Gold"),50)
PARALLELS += chrome_ladder(C("Platinum"),25)
PARALLELS += [("SDCC Exclusive Art Cards","Black Refractor",10,None),("SDCC Exclusive Art Cards","Red Refractor",5,None),
              ("SDCC Exclusive Art Cards","Superfractor",1,None),("SDCC Exclusive Art Cards","Base",50,None)]
PARALLELS += [("Mass Symbiote Takeover","Gold Foil",50,None),("Mass Symbiote Takeover","Orange Foil",25,None),
              ("Mass Symbiote Takeover","Black and Gold Foil",10,None),("Mass Symbiote Takeover","Red Carnage Foil",5,None),
              ("Mass Symbiote Takeover","Foilfractor",1,None)]
PARALLELS += [("Cerebro","Orange Refractor",25,None),("Cerebro","Black and Gold Refractor",10,None),
              ("Cerebro","Red Carnage Refractor",5,None),("Cerebro","Superfractor",1,None),("Cerebro","Base",99,None)]
for sub in ("Chrome Autographs – Comic Creators","Chrome Autographs – Marvel Studios"):
    PARALLELS += [(sub,"Black Refractor",10,None),(sub,"Red Refractor",5,None),(sub,"Superfractor",1,None)]
PARALLELS += [("Marvel Cut Signature","Base",1,None),("Spider-Man Comic Cuts","Base",1,None)]


def main():
    db = sqlite3.connect(os.path.abspath(DB))
    if db.execute("SELECT id FROM sets WHERE slug=? OR name=?", (SET["slug"], SET["name"])).fetchone():
        print("STOP: set already exists."); raise SystemExit(1)

    cur = db.execute(
        """INSERT INTO sets (name, sport, season, league, tier, sample_image_url, release_date,
                             slug, is_visible, created_at, topps_url, box_config, pack_odds)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,NULL,NULL)""",
        (SET["name"], SET["sport"], SET["season"], SET["league"], SET["tier"], SET["sample_image_url"],
         SET["release_date"], SET["slug"], SET["is_visible"], SET["created_at"], SET["topps_url"]))
    set_id = cur.lastrowid
    print(f"Created set id {set_id}")

    is_id = {}
    for name, b, r, a, k in SUBSETS:
        is_id[name] = db.execute(
            "INSERT INTO insert_sets (set_id, name, is_autograph, is_base, is_relic, is_booklet) VALUES (?,?,?,?,?,?)",
            (set_id, name, a, b, r, k)).lastrowid
    print(f"Created {len(is_id)} subsets")

    # parallels
    for sub, pname, pr, ex in PARALLELS:
        db.execute("INSERT INTO parallels (insert_set_id, name, print_run, exclusivity) VALUES (?,?,?,?)",
                   (is_id[sub], pname, pr, ex))

    # players: one per (name, role); assert no name collides across roles
    role_of = {}
    def want(name, role):
        if name in role_of and role_of[name] != role:
            raise SystemExit(f"STOP: subject '{name}' has conflicting roles {role_of[name]} vs {role}")
        role_of[name] = role
    for nm in BASE125: want(nm, "character")
    for _, nm in SDCC: want(nm, "character")
    for _, nm in MST: want(nm, "character")
    for nm in CEREBRO: want(nm, "character")
    for _, nm in CREATORS: want(nm, "celebrity")
    for _, nm, *_ in STUDIOS: want(nm, "celebrity")
    for _, nm in CUTSIG: want(nm, "celebrity")
    want("Spider-Man", "character")  # comic cuts subject (already character)
    for nm in SKETCH: want(nm, "celebrity")

    pid = {}
    for nm, role in role_of.items():
        pid[nm] = db.execute("INSERT INTO players (set_id, name, subject_role) VALUES (?,?,?)",
                             (set_id, nm, role)).lastrowid

    def app(subset, code, subject, tag=None):
        db.execute("""INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, subset_tag, team)
                      VALUES (?,?,?,0,?,NULL)""", (pid[subject], is_id[subset], code, tag))

    # base + chrome (same 125 checklist)
    for i, nm in enumerate(BASE125, start=1):
        t = tier_for(i)
        app(B(t), str(i), nm)
        app(C(t), str(i), nm)
    for code, nm in SDCC: app("SDCC Exclusive Art Cards", code, nm)
    for code, nm in MST: app("Mass Symbiote Takeover", code, nm)
    for i, nm in enumerate(CEREBRO, start=1): app("Cerebro", str(i), nm)
    for code, nm in CREATORS: app("Chrome Autographs – Comic Creators", code, nm)
    for code, nm, char, prop in STUDIOS: app("Chrome Autographs – Marvel Studios", code, nm, tag=f"as {char}")
    for code, nm in CUTSIG: app("Marvel Cut Signature", code, nm)
    for code, issue in COMICCUTS: app("Spider-Man Comic Cuts", code, "Spider-Man", tag=issue)
    for nm in SKETCH: app("Sketch Cards", "", nm)  # '' = code-less convention

    # ---------- integrity gates (pre-commit) ----------
    fail = []
    def q(sql, *a): return db.execute(sql, a).fetchone()[0]

    n_sub = q("SELECT COUNT(*) FROM insert_sets WHERE set_id=?", set_id)
    if n_sub != 16: fail.append(f"subsets={n_sub} exp 16")
    n_par = q("SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id WHERE i.set_id=?", set_id)
    if n_par != 72: fail.append(f"parallels={n_par} exp 72")
    total = q("SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id WHERE i.set_id=?", set_id)
    if total != 480: fail.append(f"cards={total} exp 480")

    per = {
     B("Bronze"):50, B("Silver"):25, B("Gold"):25, B("Platinum"):25,
     C("Bronze"):50, C("Silver"):25, C("Gold"):25, C("Platinum"):25,
     "SDCC Exclusive Art Cards":3, "Mass Symbiote Takeover":30, "Cerebro":55,
     "Chrome Autographs – Comic Creators":27, "Chrome Autographs – Marvel Studios":6,
     "Marvel Cut Signature":1, "Spider-Man Comic Cuts":15, "Sketch Cards":93,
    }
    for sub, exp in per.items():
        got = q("SELECT COUNT(*) FROM player_appearances WHERE insert_set_id=?", is_id[sub])
        if got != exp: fail.append(f"cards[{sub}]={got} exp {exp}")

    # parallel run distribution
    from collections import Counter
    runs = Counter(r[0] for r in db.execute(
        "SELECT p.print_run FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id WHERE i.set_id=?", (set_id,)))
    exp_runs = {100:4, 99:2, 75:4, 50:6, 25:9, 10:16, 5:16, 1:15}
    if dict(runs) != exp_runs: fail.append(f"run dist={dict(sorted(runs.items()))} exp {exp_runs}")
    n_ex = q("SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id WHERE i.set_id=? AND p.exclusivity IS NOT NULL", set_id)
    if n_ex != 10: fail.append(f"exclusive parallels={n_ex} exp 10")
    n_baserow = q("SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id WHERE i.set_id=? AND p.name='Base'", set_id)
    if n_baserow != 9: fail.append(f"Base-named parallel rows={n_baserow} exp 9")

    n_rook = q("SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id WHERE i.set_id=? AND pa.is_rookie=1", set_id)
    if n_rook != 0: fail.append(f"rookies={n_rook} exp 0")
    n_pl = q("SELECT COUNT(*) FROM players WHERE set_id=?", set_id)
    n_char = q("SELECT COUNT(*) FROM players WHERE set_id=? AND subject_role='character'", set_id)
    n_cel = q("SELECT COUNT(*) FROM players WHERE set_id=? AND subject_role='celebrity'", set_id)
    if n_pl != 289: fail.append(f"players(subjects)={n_pl} exp 289")
    if n_char != 162: fail.append(f"character subjects={n_char} exp 162")
    if n_cel != 127: fail.append(f"celebrity subjects={n_cel} exp 127")
    n_co = q("""SELECT COUNT(*) FROM appearance_co_players acp JOIN player_appearances pa ON pa.id=acp.appearance_id
               JOIN insert_sets i ON i.id=pa.insert_set_id WHERE i.set_id=?""", set_id)
    if n_co != 0: fail.append(f"co_players={n_co} exp 0")
    po = db.execute("SELECT pack_odds FROM sets WHERE id=?", (set_id,)).fetchone()[0]
    if po is not None: fail.append(f"pack_odds not NULL: {po!r}")
    n_sketch_codeless = q("SELECT COUNT(*) FROM player_appearances WHERE insert_set_id=? AND card_number=''", is_id["Sketch Cards"])
    if n_sketch_codeless != 93: fail.append(f"code-less sketch rows={n_sketch_codeless} exp 93")

    print(f"\nTotals: cards={total} subsets={n_sub} parallels={n_par} players={n_pl} (char {n_char}/cel {n_cel})")
    print(f"parallel runs={dict(sorted(runs.items(), reverse=True))} exclusives={n_ex} base-rows={n_baserow}")
    if fail:
        db.rollback()
        print("\nINTEGRITY GATE MISMATCHES (rolled back, nothing written):")
        for m in fail: print("  ", m)
        raise SystemExit(1)
    db.commit()
    print("\nINTEGRITY GATES: all pass. Committed. set_id=%d" % set_id)
    db.close()


if __name__ == "__main__":
    main()
