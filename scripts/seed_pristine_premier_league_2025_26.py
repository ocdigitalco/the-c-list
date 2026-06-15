# -*- coding: utf-8 -*-
"""
Seed: 2025-26 Topps Pristine Premier League (second EPL set after Merlin).
200 base + 11 insert subsets + 8 single-subject auto subsets + 1 dual-auto + 4 auto-relic.
687 cards. Single format "Tri-Stack". release_date NULL, box_config NULL.
Pack odds attach now (flat JSON); print runs deferred (all parallels print_run NULL).
Parallels are derived from the pack_odds keys (longest-prefix match) so odds keys and
parallel rows stay consistent.
Usage: python3 scripts/seed_pristine_premier_league_2025_26.py
"""
import sqlite3, os, json, re, unicodedata

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
db = sqlite3.connect(DB_PATH)
db.execute("PRAGMA journal_mode=WAL")
db.execute("PRAGMA foreign_keys=ON")

SLUG = "2025-26-topps-pristine-premier-league"
if db.execute("SELECT id FROM sets WHERE slug = ?", (SLUG,)).fetchone():
    raise SystemExit(f"ABORT: set with slug {SLUG} already exists.")

pack_odds = json.dumps({
  "Base Refractor": "2:1",
  "Base Top Corner": "1:1",
  "Base Blue Refractor": "1:3",
  "Base Gold Refractor": "1:4",
  "Base Orange Refractor": "1:7",
  "Base Pink Refractor": "1:12",
  "Base PL Trophy Malachite Refractor": "1:18",
  "Base Red Refractor": "1:35",
  "Base Superfractor": "1:173",
  "Precisionaries": "1:1",
  "Precisionaries Red Refractor": "1:69",
  "Precisionaries Superfractor": "1:337",
  "Pure Strike": "1:1",
  "Pure Strike Red Refractor": "1:69",
  "Pure Strike Superfractor": "1:337",
  "Generational": "1:1",
  "Generational Red Refractor": "1:69",
  "Generational Superfractor": "1:337",
  "Perseverance": "1:1",
  "Perseverance Red Refractor": "1:69",
  "Perseverance Superfractor": "1:337",
  "Pristine Seasons": "1:84",
  "Pristine Seasons Superfractor": "1:1734",
  "Glacier": "1:330",
  "Glacier Superfractor": "1:1734",
  "Amped": "1:42",
  "Amped Superfractor": "1:1734",
  "Pearlescent": "1:42",
  "Pearlescent Superfractor": "1:845",
  "Pristine Ivory": "1:132",
  "Pristine Ivory Superfractor": "1:659",
  "The Grail": "1:659",
  "Pristine Legacy Autographs Gold Refractor": "1:96",
  "Pristine Legacy Autographs Orange Refractor": "1:75",
  "Pristine Legacy Autographs Pink Refractor": "1:119",
  "Pristine Legacy Autographs PL Trophy Malachite Refractor": "1:163",
  "Pristine Legacy Autographs Red Refractor": "1:340",
  "Pristine Legacy Autographs Superfractor": "1:1569",
  "Pristine Pairs Dual Autographs": "1:57",
  "Pristine Pairs Dual Autographs PL Trophy Malachite Refractor": "1:241",
  "Pristine Pairs Dual Autographs Red Refractor": "1:452",
  "Pristine Pairs Dual Autographs Superfractor": "1:2196",
  "Pristine Personal Endorsements Autographs": "1:423",
  "Pristine Personal Endorsements Autographs PL Trophy Malachite Refractor": "1:388",
  "Pristine Personal Endorsements Autographs Red Refractor": "1:452",
  "Pristine Personal Endorsements Autographs Superfractor": "1:2059",
  "Pristine Pieces Autograph Relics": "1:59",
  "Pristine Pieces Autograph Relics Purple": "1:32",
  "Pristine Pieces Autograph Relics Blue": "1:29",
  "Pristine Pieces Autograph Relics Gold": "1:33",
  "Pristine Pieces Autograph Relics Orange": "1:65",
  "Pristine Pieces Autograph Relics Pink": "1:103",
  "Pristine Pieces Autograph Relics PL Trophy Malachite": "1:142",
  "Pristine Pieces Autograph Relics Red": "1:280",
  "Pristine Pieces Autograph Relics Black": "1:1373",
  "Pristine Seasons Autograph Edition": "1:340",
  "Pristine Seasons Autograph Edition PL Trophy Malachite Refractor": "1:412",
  "Pristine Seasons Autograph Edition Red Refractor": "1:589",
  "Pristine Seasons Autograph Edition Superfractor": "1:2534",
  "Rookie Jumbo Relic Autographs": "1:559",
  "Rookie Jumbo Relic Autographs Pristine Black": "1:8235",
  "Rookie Jumbo Relic Autographs Pristine PL Trophy Malachite": "1:1136",
  "Rookie Jumbo Relic Autographs Pristine Red": "1:2196",
  "Day 1 Pristine": "1:845",
  "Day 1 Pristine PL Trophy Malachite": "1:1136",
  "Day 1 Pristine Red": "1:2196",
  "Day 1 Pristine Black": "1:8235",
  "Popular Demand Autograph Relics": "1:57",
  "Popular Demand Autograph Relics Pristine Purple": "1:32",
  "Popular Demand Autograph Relics Pristine Blue": "1:29",
  "Popular Demand Autograph Relics Pristine Gold": "1:40",
  "Popular Demand Autograph Relics Pristine Orange": "1:68",
  "Popular Demand Autograph Relics Pristine Pink": "1:108",
  "Popular Demand Autograph Relics Pristine PL Trophy Malachite": "1:148",
  "Popular Demand Autograph Relics Pristine Red": "1:280",
  "Popular Demand Autograph Relics Pristine Black": "1:1373",
  "Pristine Autographs": "1:24",
  "Pristine Autographs Green": "1:9",
  "Pristine Autographs Purple": "1:11",
  "Pristine Autographs Blue": "1:8",
  "Pristine Autographs Gold": "1:11",
  "Pristine Autographs Orange": "1:20",
  "Pristine Autographs Pink": "1:33",
  "Pristine Autographs PL Trophy Malachite": "1:48",
  "Pristine Autographs Red": "1:91",
  "Pristine Autographs Black": "1:446",
  "Pristine Bianco": "1:1647",
  "Pristine From The Pitch": "1:43",
  "Pristine From The Pitch PL Trophy Malachite": "1:188",
  "Pristine From The Pitch Red": "1:375",
  "Pristine From The Pitch Black": "1:1830",
})

db.execute("""
    INSERT INTO sets (name, sport, season, league, tier, slug, is_visible,
                      sample_image_url, release_date, box_config, pack_odds, created_at)
    VALUES ('2025-26 Topps Pristine Premier League', 'Soccer', '2026', 'Premier League', 'Pristine',
            ?, 1, ?, NULL, NULL, ?, '2026-06-15T12:00:00Z')
""", (SLUG, f"/sets/{SLUG}.jpg", pack_odds))
SET_ID = db.execute("SELECT last_insert_rowid()").fetchone()[0]
print(f"Created set ID: {SET_ID}")

def slugify(t):
    s = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode('ascii')
    s = s.lower().strip(); s = re.sub(r'[^\w\s-]', '', s); s = re.sub(r'[\s_]+', '-', s)
    return re.sub(r'-+', '-', s).strip('-')

_sc = {}
def goc(name, role="athlete"):
    name = name.strip()
    row = db.execute("SELECT id FROM players WHERE set_id = ? AND name = ?", (SET_ID, name)).fetchone()
    if row: return row[0]
    slug = slugify(name)
    c = slug; i = 2
    while c in _sc: c = f"{slug}-{i}"; i += 1
    _sc[c] = True
    db.execute("INSERT INTO players (set_id, name, slug, unique_cards, total_print_run, one_of_ones, insert_set_count, subject_role) VALUES (?, ?, ?, 0, 0, 0, 0, ?)",
               (SET_ID, name, c, role))
    return db.execute("SELECT last_insert_rowid()").fetchone()[0]

def ais(name, is_auto=False):
    db.execute("INSERT INTO insert_sets (set_id, name, is_autograph) VALUES (?, ?, ?)", (SET_ID, name, 1 if is_auto else 0))
    return db.execute("SELECT last_insert_rowid()").fetchone()[0]

def ins(name, cards, is_auto=False):
    is_id = ais(name, is_auto)
    for c in cards:
        num, pname, team = c[0], c[1], c[2]
        rc = c[3] if len(c) > 3 else False
        pid = goc(pname)
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)",
                   (pid, is_id, str(num), 1 if rc else 0, team))
    print(f"  {name}: {len(cards)} cards")
    return is_id

R = True

# ═══ BASE (200) ══════════════════════════════════════════════════════════════
ins("Base", [
(1,"David Brooks","AFC Bournemouth"),(2,"Bafodé Diakité","AFC Bournemouth"),(3,"Junior Kroupi","AFC Bournemouth"),(4,"Evanilson","AFC Bournemouth"),(5,"Adrien Truffert","AFC Bournemouth"),(6,"Veljko Milosavljević","AFC Bournemouth",R),(7,"Tyler Adams","AFC Bournemouth"),(8,"Julio Soler","AFC Bournemouth",R),(9,"Marcos Senesi","AFC Bournemouth"),(10,"Alex Scott","AFC Bournemouth"),
(11,"Max Dowman","Arsenal",R),(12,"Martín Zubimendi","Arsenal"),(13,"Declan Rice","Arsenal"),(14,"Leandro Trossard","Arsenal"),(15,"Riccardo Calafiori","Arsenal"),(16,"Gabriel Magalhães","Arsenal"),(17,"Bukayo Saka","Arsenal"),(18,"Martin Ødegaard","Arsenal"),(19,"Viktor Gyökeres","Arsenal"),(20,"Jurriën Timber","Arsenal"),
(21,"Morgan Rogers","Aston Villa"),(22,"Ollie Watkins","Aston Villa"),(23,"Amadou Onana","Aston Villa"),(24,"Bradley Burrowes","Aston Villa",R),(25,"John McGinn","Aston Villa"),(26,"Matty Cash","Aston Villa"),(27,"Youri Tielemans","Aston Villa"),(28,"Emiliano Martínez","Aston Villa"),(29,"Pau Torres","Aston Villa"),(30,"Emiliano Buendía","Aston Villa"),
(31,"Kevin Schade","Brentford"),(32,"Dango Ouattara","Brentford"),(33,"Mathias Jensen","Brentford"),(34,"Mikkel Damsgaard","Brentford"),(35,"Igor Thiago","Brentford"),(36,"Michael Kayode","Brentford"),(37,"Fábio Carvalho","Brentford"),(38,"Jordan Henderson","Brentford"),(39,"Reiss Nelson","Brentford"),(40,"Romelle Donovan","Brentford",R),
(41,"Harry Howell","Brighton & Hove Albion",R),(42,"Kaoru Mitoma","Brighton & Hove Albion"),(43,"Carlos Baleba","Brighton & Hove Albion"),(44,"Georginio Rutter","Brighton & Hove Albion"),(45,"Yasin Ayari","Brighton & Hove Albion",R),(46,"Diego Gómez","Brighton & Hove Albion"),(47,"Danny Welbeck","Brighton & Hove Albion"),(48,"Ferdi Kadioglu","Brighton & Hove Albion"),(49,"Charalampos Kostoulas","Brighton & Hove Albion"),(50,"Yankuba Minteh","Brighton & Hove Albion"),
(51,"Zian Flemming","Burnley FC",R),(52,"Kyle Walker","Burnley FC"),(53,"Lesley Ugochukwu","Burnley FC"),(54,"Loum Tchaouna","Burnley FC"),(55,"Jaidon Anthony","Burnley FC"),(56,"Quilindschy Hartman","Burnley FC"),(57,"Josh Cullen","Burnley FC"),(58,"Maxime Estève","Burnley FC"),(59,"Jacob Bruun Larsen","Burnley FC"),(60,"Lyle Foster","Burnley FC"),
(61,"Cole Palmer","Chelsea"),(62,"Alejandro Garnacho","Chelsea"),(63,"Moisés Caicedo","Chelsea"),(64,"Estêvão Willian","Chelsea",R),(65,"Jorrel Hato","Chelsea"),(66,"Enzo Fernández","Chelsea"),(67,"Robert Sánchez","Chelsea"),(68,"Pedro Neto","Chelsea"),(69,"Malo Gusto","Chelsea"),(70,"Reece James","Chelsea"),
(71,"Daniel Muñoz","Crystal Palace"),(72,"Daichi Kamada","Crystal Palace"),(73,"Ismaïla Sarr","Crystal Palace"),(74,"Jean-Philippe Mateta","Crystal Palace"),(75,"Adam Wharton","Crystal Palace"),(76,"Jaydee Canvot","Crystal Palace",R),(77,"Dean Henderson","Crystal Palace"),(78,"Yéremy Pino","Crystal Palace"),(79,"Will Hughes","Crystal Palace"),(80,"Eddie Nketiah","Crystal Palace"),
(81,"Iliman Ndiaye","Everton"),(82,"Jack Grealish","Everton"),(83,"Jake O'Brien","Everton"),(84,"Idrissa Gueye","Everton"),(85,"Charly Alcaraz","Everton"),(86,"Jarrad Branthwaite","Everton"),(87,"James Garner","Everton"),(88,"Thierno Barry","Everton"),(89,"Beto","Everton"),(90,"Kiernan Dewsbury-Hall","Everton"),
(91,"Kevin","Fulham"),(92,"Josh King","Fulham",R),(93,"Raúl Jiménez","Fulham"),(94,"Alex Iwobi","Fulham"),(95,"Rodrigo Muniz","Fulham"),(96,"Harry Wilson","Fulham"),(97,"Calvin Bassey","Fulham"),(98,"Ryan Sessegnon","Fulham"),(99,"Sander Berge","Fulham"),(100,"Kenny Tete","Fulham"),
(101,"Dominic Calvert-Lewin","Leeds United"),(102,"Pascal Struijk","Leeds United"),(103,"Gabriel Gudmundsson","Leeds United"),(104,"Wilfried Gnonto","Leeds United"),(105,"Anton Stach","Leeds United"),(106,"Lukas Nmecha","Leeds United"),(107,"Ao Tanaka","Leeds United"),(108,"Brenden Aaronson","Leeds United"),(109,"Jayden Bogle","Leeds United"),(110,"Daniel James","Leeds United"),
(111,"Alexander Isak","Liverpool FC"),(112,"Mohamed Salah","Liverpool FC"),(113,"Florian Wirtz","Liverpool FC"),(114,"Hugo Ekitike","Liverpool FC"),(115,"Alexis Mac Allister","Liverpool FC"),(116,"Virgil van Dijk","Liverpool FC"),(117,"Rio Ngumoha","Liverpool FC",R),(118,"Cody Gakpo","Liverpool FC"),(119,"Curtis Jones","Liverpool FC"),(120,"Dominik Szoboszlai","Liverpool FC"),
(121,"Phil Foden","Manchester City"),(122,"Erling Haaland","Manchester City"),(123,"Rayan Cherki","Manchester City"),(124,"Rodri","Manchester City"),(125,"Tijjani Reijnders","Manchester City"),(126,"Gianluigi Donnarumma","Manchester City"),(127,"Omar Marmoush","Manchester City"),(128,"Jérémy Doku","Manchester City"),(129,"Savinho","Manchester City"),(130,"Rayan Aït-Nouri","Manchester City"),
(131,"Matheus Cunha","Manchester United"),(132,"Bruno Fernandes","Manchester United"),(133,"Benjamin Šeško","Manchester United"),(134,"Bryan Mbeumo","Manchester United"),(135,"Amad","Manchester United"),(136,"Manuel Ugarte","Manchester United"),(137,"Leny Yoro","Manchester United"),(138,"Casemiro","Manchester United"),(139,"Kobbie Mainoo","Manchester United"),(140,"Mason Mount","Manchester United"),
(141,"Bruno Guimarães","Newcastle United"),(142,"Anthony Gordon","Newcastle United"),(143,"Nick Woltemade","Newcastle United"),(144,"Sandro Tonali","Newcastle United"),(145,"Jacob Murphy","Newcastle United"),(146,"Lewis Miley","Newcastle United"),(147,"Anthony Elanga","Newcastle United"),(148,"Malick Thiaw","Newcastle United"),(149,"Jacob Ramsey","Newcastle United"),(150,"Harvey Barnes","Newcastle United"),
(151,"Igor Jesus","Nottingham Forest",R),(152,"Chris Wood","Nottingham Forest"),(153,"Murillo","Nottingham Forest"),(154,"Morgan Gibbs-White","Nottingham Forest"),(155,"Ibrahim Sangaré","Nottingham Forest"),(156,"Nikola Milenković","Nottingham Forest"),(157,"Nicolás Domínguez","Nottingham Forest"),(158,"Taiwo Awoniyi","Nottingham Forest"),(159,"Jair","Nottingham Forest",R),(160,"Ryan Yates","Nottingham Forest"),
(161,"Eliezer Mayenda","Sunderland",R),(162,"Chris Rigg","Sunderland",R),(163,"Dan Ballard","Sunderland",R),(164,"Wilson Isidor","Sunderland",R),(165,"Granit Xhaka","Sunderland"),(166,"Chemsdine Talbi","Sunderland"),(167,"Nordi Mukiele","Sunderland"),(168,"Lutsharel Geertruida","Sunderland"),(169,"Robin Roefs","Sunderland",R),(170,"Noah Sadiki","Sunderland",R),
(171,"Mathys Tel","Tottenham Hotspur"),(172,"Micky van de Ven","Tottenham Hotspur"),(173,"Xavi Simons","Tottenham Hotspur"),(174,"Dominic Solanke","Tottenham Hotspur"),(175,"Cristian Romero","Tottenham Hotspur"),(176,"João Palhinha","Tottenham Hotspur"),(177,"Pape Matar Sarr","Tottenham Hotspur"),(178,"Mohammed Kudus","Tottenham Hotspur"),(179,"Wilson Odobert","Tottenham Hotspur"),(180,"Rodrigo Bentancur","Tottenham Hotspur"),
(181,"El Hadji Malick Diouf","West Ham United",R),(182,"Soungoutou Magassa","West Ham United"),(183,"Jean-Clair Todibo","West Ham United"),(184,"Freddie Potts","West Ham United",R),(185,"Mateus Fernandes","West Ham United"),(186,"Jarrod Bowen","West Ham United"),(187,"Mohamadou Kanté","West Ham United",R),(188,"Tomáš Souček","West Ham United"),(189,"Callum Wilson","West Ham United"),(190,"Crysencio Summerville","West Ham United"),
(191,"André","Wolverhampton Wanderers"),(192,"Tolu Arokodare","Wolverhampton Wanderers",R),(193,"Mateus Mané","Wolverhampton Wanderers",R),(194,"João Gomes","Wolverhampton Wanderers"),(195,"Hwang Hee-Chan","Wolverhampton Wanderers"),(196,"Jean-Ricner Bellegarde","Wolverhampton Wanderers"),(197,"Toti Gomes","Wolverhampton Wanderers"),(198,"Matt Doherty","Wolverhampton Wanderers"),(199,"Hugo Bueno","Wolverhampton Wanderers"),(200,"Rodrigo Gomes","Wolverhampton Wanderers"),
])

# ═══ PRECISIONARIES (PC-, 50) ════════════════════════════════════════════════
ins("Precisionaries", [
("PC-1","Viktor Gyökeres","Arsenal"),("PC-2","Thierry Henry","Arsenal"),("PC-3","Dennis Bergkamp","Arsenal"),("PC-4","Junior Kroupi","AFC Bournemouth"),("PC-5","Evanilson","AFC Bournemouth"),("PC-6","Ollie Watkins","Aston Villa"),("PC-7","Gabriel Agbonlahor","Aston Villa"),("PC-8","Kevin Schade","Brentford"),("PC-9","Igor Thiago","Brentford"),("PC-10","Kaoru Mitoma","Brighton & Hove Albion"),
("PC-11","Stefanos Tzimas","Brighton & Hove Albion",R),("PC-12","Zian Flemming","Burnley FC",R),("PC-13","Ashley Barnes","Burnley FC"),("PC-14","Didier Drogba","Chelsea"),("PC-15","João Pedro","Chelsea"),("PC-16","Nicolas Anelka","Chelsea"),("PC-17","Jean-Philippe Mateta","Crystal Palace"),("PC-18","Andy Johnson","Crystal Palace"),("PC-19","Iliman Ndiaye","Everton"),("PC-20","Duncan Ferguson","Everton"),
("PC-21","Clint Dempsey","Fulham"),("PC-22","Louis Saha","Fulham"),("PC-23","Zlatan Ibrahimović","Manchester United"),("PC-24","Bryan Mbeumo","Manchester United"),("PC-25","Mohamed Salah","Liverpool FC"),("PC-26","Michael Owen","Liverpool FC"),("PC-27","Fernando Torres","Liverpool FC"),("PC-28","Erling Haaland","Manchester City"),("PC-29","Sergio Agüero","Manchester City"),("PC-30","Carlos Tevez","Manchester City"),
("PC-31","Wayne Rooney","Manchester United"),("PC-32","Andy Cole","Manchester United"),("PC-33","Jimmy Floyd Hasselbaink","Leeds United"),("PC-34","Nick Woltemade","Newcastle United"),("PC-35","Alan Shearer","Newcastle United"),("PC-36","Chris Wood","Nottingham Forest"),("PC-37","Wilson Isidor","Sunderland",R),("PC-38","Jermain Defoe","Sunderland"),("PC-39","Teddy Sheringham","Tottenham Hotspur"),("PC-40","Heung-Min Son","Tottenham Hotspur"),
("PC-41","Robbie Keane","Tottenham Hotspur"),("PC-42","Diego Costa","Chelsea"),("PC-43","Michail Antonio","West Ham United"),("PC-44","Wilfried Gnonto","Leeds United"),("PC-45","Dwight Yorke","Aston Villa"),("PC-46","Harry Kane","Tottenham Hotspur"),("PC-47","Leon Osman","Everton"),("PC-48","Robbie Fowler","Liverpool FC"),("PC-49","Ian Wright","Arsenal"),("PC-50","Eidur Gudjohnsen","Chelsea"),
])

# ═══ PURE STRIKE (PK-, 20) ═══════════════════════════════════════════════════
ins("Pure Strike", [
("PK-1","Marcus Tavernier","AFC Bournemouth"),("PK-2","Leandro Trossard","Arsenal"),("PK-3","Youri Tielemans","Aston Villa"),("PK-4","Dango Ouattara","Brentford"),("PK-5","Diego Gómez","Brighton & Hove Albion"),("PK-6","Lesley Ugochukwu","Burnley FC"),("PK-7","Cole Palmer","Chelsea"),("PK-8","Ismaïla Sarr","Crystal Palace"),("PK-9","Charly Alcaraz","Everton"),("PK-10","Raúl Jiménez","Fulham"),
("PK-11","Anton Stach","Leeds United"),("PK-12","Dominik Szoboszlai","Liverpool FC"),("PK-13","Omar Marmoush","Manchester City"),("PK-14","Bruno Fernandes","Manchester United"),("PK-15","Fabian Schär","Newcastle United"),("PK-16","Morgan Gibbs-White","Nottingham Forest"),("PK-17","Granit Xhaka","Sunderland"),("PK-18","Xavi Simons","Tottenham Hotspur"),("PK-19","Mateus Fernandes","West Ham United"),("PK-20","Tolu Arokodare","Wolverhampton Wanderers",R),
])

# ═══ GENERATIONAL (G-, 10) ═══════════════════════════════════════════════════
ins("Generational", [
("G-1","Moisés Caicedo","Chelsea"),("G-2","Martin Ødegaard","Arsenal"),("G-3","Declan Rice","Arsenal"),("G-4","Bukayo Saka","Arsenal"),("G-5","Erling Haaland","Manchester City"),("G-6","Mohamed Salah","Liverpool FC"),("G-7","Bruno Fernandes","Manchester United"),("G-8","Sandro Tonali","Newcastle United"),("G-9","Cole Palmer","Chelsea"),("G-10","Rodri","Manchester City"),
])

# ═══ PERSEVERANCE (PV-, 20) ══════════════════════════════════════════════════
ins("Perseverance", [
("PV-1","Martin Ødegaard","Arsenal"),("PV-2","Jordan Henderson","Brentford"),("PV-3","James Milner","Brighton & Hove Albion"),("PV-4","Mikkel Damsgaard","Brentford"),("PV-5","Danny Welbeck","Brighton & Hove Albion"),("PV-6","Eberechi Eze","Arsenal"),("PV-7","Youri Tielemans","Aston Villa"),("PV-8","Moisés Caicedo","Chelsea"),("PV-9","Marc Guéhi","Manchester City"),("PV-10","Kieran Trippier","Newcastle United"),
("PV-11","Harry Wilson","Fulham"),("PV-12","Alexander Isak","Liverpool FC"),("PV-13","Virgil van Dijk","Liverpool FC"),("PV-14","Erling Haaland","Manchester City"),("PV-15","Rodri","Manchester City"),("PV-16","Bruno Guimarães","Newcastle United"),("PV-17","Anthony Gordon","Newcastle United"),("PV-18","Chris Wood","Nottingham Forest"),("PV-19","Kyle Walker","Burnley"),("PV-20","Nathan Collins","Brentford"),
])

# ═══ AMPED (A-, 20) ══════════════════════════════════════════════════════════
ins("Amped", [
("A-1","Max Dowman","Arsenal",R),("A-2","Marc Cucurella","Chelsea"),("A-3","Joelinton","Newcastle United"),("A-4","Gabriel Magalhães","Arsenal"),("A-5","Erling Haaland","Manchester City"),("A-6","El Hadji Malick Diouf","West Ham United",R),("A-7","Noni Madueke","Arsenal"),("A-8","Emiliano Martínez","Aston Villa"),("A-9","Benjamin Šeško","Manchester United"),("A-10","Estêvão Willian","Chelsea",R),
("A-11","Murillo","Nottingham Forest"),("A-12","Rio Ngumoha","Liverpool FC",R),("A-13","Micky van de Ven","Tottenham Hotspur"),("A-14","Veljko Milosavljević","AFC Bournemouth",R),("A-15","Daniel Muñoz","Crystal Palace"),("A-16","Bukayo Saka","Arsenal"),("A-17","Hugo Ekitike","Liverpool FC"),("A-18","Tijjani Reijnders","Manchester City"),("A-19","Pedro Neto","Chelsea"),("A-20","Phil Foden","Manchester City"),
])

# ═══ PEARLESCENT (P-, 40) ════════════════════════════════════════════════════
ins("Pearlescent", [
("P-1","Estêvão Willian","Chelsea",R),("P-2","Nick Woltemade","Newcastle United"),("P-3","Chris Rigg","Sunderland",R),("P-4","Paul Scholes","Manchester United"),("P-5","Martín Zubimendi","Arsenal"),("P-6","Mario Balotelli","Manchester City"),("P-7","Robin van Persie","Manchester United"),("P-8","Ruud Gullit","Chelsea"),("P-9","Noah Sadiki","Sunderland",R),("P-10","Harry Kane","Tottenham Hotspur"),
("P-11","Faustino Asprilla","Newcastle United"),("P-12","Dan Ballard","Sunderland",R),("P-13","Alexis Mac Allister","Liverpool FC"),("P-14","Alexander Isak","Liverpool FC"),("P-15","Mohamed Salah","Liverpool FC"),("P-16","Juan Pablo Ángel","Aston Villa"),("P-17","Harry Howell","Brighton & Hove Albion",R),("P-18","Stuart Pearce","Nottingham Forest"),("P-19","Roy Keane","Nottingham Forest"),("P-20","Stefanos Tzimas","Brighton & Hove Albion",R),
("P-21","Freddie Potts","West Ham United",R),("P-22","James Rodríguez","Everton"),("P-23","Max Dowman","Arsenal",R),("P-24","Roberto Firmino","Liverpool FC"),("P-25","Edgar Davids","Tottenham Hotspur"),("P-26","Gareth Bale","Tottenham Hotspur"),("P-27","Kevin De Bruyne","Manchester City"),("P-28","Rayan Cherki","Manchester City"),("P-29","Robbie Fowler","Leeds United"),("P-30","Robbie Keane","Leeds United"),
("P-31","Morgan Rogers","Aston Villa"),("P-32","Mikkel Damsgaard","Brentford"),("P-33","Rio Ngumoha","Liverpool FC",R),("P-34","Eden Hazard","Chelsea"),("P-35","Mikel Arteta","Arsenal"),("P-36","Santi Cazorla","Arsenal"),("P-37","Patrick Vieira","Arsenal"),("P-38","Zlatan Ibrahimović","Manchester United"),("P-39","Ryan Giggs","Manchester United"),("P-40","Edwin van der Sar","Manchester United"),
])

# ═══ PRISTINE SEASONS (PS-, 20) ══════════════════════════════════════════════
ins("Pristine Seasons", [
("PS-1","Luis Suárez","Liverpool FC"),("PS-2","Erling Haaland","Manchester City"),("PS-3","Virgil van Dijk","Liverpool FC"),("PS-4","John Terry","Chelsea"),("PS-5","Petr Čech","Chelsea"),("PS-6","Didier Drogba","Chelsea"),("PS-7","Thierry Henry","Arsenal"),("PS-8","Roy Keane","Manchester United"),("PS-9","Alan Shearer","Newcastle United"),("PS-10","Yaya Touré","Manchester City"),
("PS-11","Frank Lampard","Chelsea"),("PS-12","Andy Cole","Manchester United"),("PS-13","Mohamed Salah","Liverpool FC"),("PS-14","Eden Hazard","Chelsea"),("PS-15","Andy Cole","Newcastle United"),("PS-16","Ricardo Carvalho","Chelsea"),("PS-17","Rodri","Manchester City"),("PS-18","Kevin De Bruyne","Manchester City"),("PS-19","Gareth Bale","Tottenham Hotspur"),("PS-20","Robin van Persie","Manchester United"),
])

# ═══ GLACIER (GL-, 20) ═══════════════════════════════════════════════════════
ins("Glacier", [
("GL-1","Dominik Szoboszlai","Liverpool FC"),("GL-2","Declan Rice","Arsenal"),("GL-3","William Saliba","Arsenal"),("GL-4","Kaoru Mitoma","Brighton & Hove Albion"),("GL-5","Martin Ødegaard","Arsenal"),("GL-6","Estêvão Willian","Chelsea",R),("GL-7","Bukayo Saka","Arsenal"),("GL-8","Bruno Fernandes","Manchester United"),("GL-9","Erling Haaland","Manchester City"),("GL-10","Cole Palmer","Chelsea"),
("GL-11","Virgil van Dijk","Liverpool FC"),("GL-12","Mohamed Salah","Liverpool FC"),("GL-13","Hugo Ekitike","Liverpool FC"),("GL-14","Rio Ngumoha","Liverpool FC",R),("GL-15","Moisés Caicedo","Chelsea"),("GL-16","Jérémy Doku","Manchester City"),("GL-17","Phil Foden","Manchester City"),("GL-18","Matheus Cunha","Manchester United"),("GL-19","Nick Woltemade","Newcastle United"),("GL-20","Granit Xhaka","Sunderland"),
])

# ═══ PRISTINE IVORY (PI-, 50) ════════════════════════════════════════════════
ins("Pristine Ivory", [
("PI-1","Antoine Semenyo","Manchester City"),("PI-2","Declan Rice","Arsenal"),("PI-3","Gabriel Magalhães","Arsenal"),("PI-4","Didier Drogba","Chelsea"),("PI-5","Dennis Bergkamp","Arsenal"),("PI-6","Thierry Henry","Arsenal"),("PI-7","Bukayo Saka","Arsenal"),("PI-8","Morgan Rogers","Aston Villa"),("PI-9","Juan Pablo Ángel","Aston Villa"),("PI-10","Igor Thiago","Brentford"),
("PI-11","Paul Merson","Arsenal"),("PI-12","Cole Palmer","Chelsea"),("PI-13","Moisés Caicedo","Chelsea"),("PI-14","Estêvão Willian","Chelsea",R),("PI-15","Gianfranco Zola","Chelsea"),("PI-16","Frank Lampard","Chelsea"),("PI-17","Ashley Cole","Chelsea"),("PI-18","Claude Makélélé","Chelsea"),("PI-19","Adam Wharton","Crystal Palace"),("PI-20","Max Dowman","Arsenal",R),
("PI-21","Jack Grealish","Everton"),("PI-22","Duncan Ferguson","Everton"),("PI-23","Josh King","Fulham",R),("PI-24","Dimitar Berbatov","Fulham"),("PI-25","Clint Dempsey","Fulham"),("PI-26","Mohamed Salah","Liverpool FC"),("PI-27","Rio Ngumoha","Liverpool FC",R),("PI-28","Luis Suárez","Liverpool FC"),("PI-29","Steven Gerrard","Liverpool FC"),("PI-30","Phil Foden","Manchester City"),
("PI-31","Micah Richards","Manchester City"),("PI-32","Sergio Agüero","Manchester City"),("PI-33","Kevin De Bruyne","Manchester City"),("PI-34","Riyad Mahrez","Manchester City"),("PI-35","Matheus Cunha","Manchester United"),("PI-36","Bryan Mbeumo","Manchester United"),("PI-37","Juan Sebastián Verón","Manchester United"),("PI-38","Henrik Larsson","Manchester United"),("PI-39","Michael Carrick","Manchester United"),("PI-40","Nick Woltemade","Newcastle United"),
("PI-41","Bruno Guimarães","Newcastle United"),("PI-42","Andy Cole","Newcastle United"),("PI-43","Morgan Gibbs-White","Nottingham Forest"),("PI-44","Eliezer Mayenda","Sunderland",R),("PI-45","Chris Rigg","Sunderland",R),("PI-46","Kevin Phillips","Sunderland"),("PI-47","Xavi Simons","Tottenham Hotspur"),("PI-48","Heung-Min Son","Tottenham Hotspur"),("PI-49","Mousa Dembélé","Tottenham Hotspur"),("PI-50","Viktor Gyökeres","Arsenal"),
])

# ═══ THE GRAIL (G-, 1) ═══════════════════════════════════════════════════════
ins("The Grail", [
("G-7","Zlatan Ibrahimović","Manchester United"),
])

# ═══ PRISTINE AUTOGRAPHS (PA-, 77) [auto] ════════════════════════════════════
ins("Pristine Autographs", [
("PA-AJ","Andy Johnson","Crystal Palace"),("PA-AR","Antonee Robinson","Fulham"),("PA-AS","Andriy Shevchenko","Chelsea"),("PA-AT","Adrien Truffert","AFC Bournemouth"),("PA-AW","Adam Wharton","Crystal Palace"),("PA-BG","Bruno Guimarães","Newcastle United"),("PA-BM","Bryan Mbeumo","Manchester United"),("PA-BN","Jarrod Bowen","West Ham United"),("PA-BR","Bryan Robson","Manchester United"),("PA-BS","Bukayo Saka","Arsenal"),
("PA-CO","Casemiro","Manchester United"),("PA-CR","Chris Rigg","Sunderland",R),("PA-DD","Diogo Dalot","Manchester United"),("PA-DF","Jermain Defoe","Sunderland"),("PA-DR","Declan Rice","Arsenal"),("PA-DW","Dennis Wise","Chelsea"),("PA-EA","Emmanuel Adebayor","Tottenham Hotspur"),("PA-EG","Eidur Gudjohnsen","Chelsea"),("PA-EH","Erling Haaland","Manchester City"),("PA-EK","Junior Kroupi","AFC Bournemouth"),
("PA-EO","Estêvão Willian","Chelsea",R),("PA-FB","Facundo Buonanotte","Leeds United"),("PA-FC","Federico Chiesa","Liverpool FC"),("PA-GM","Gabriel Magalhães","Arsenal"),("PA-GP","Gustavo Poyet","Chelsea"),("PA-GR","Georginio Rutter","Brighton & Hove Albion"),("PA-GX","Granit Xhaka","Sunderland"),("PA-HK","Harry Kane","Tottenham Hotspur"),("PA-IN","Iliman Ndiaye","Everton"),("PA-JB","Jayden Bogle","Leeds United"),
("PA-JD","Jérémy Doku","Manchester City"),("PA-JG","Jack Grealish","Everton"),("PA-JM","John McGinn","Aston Villa"),("PA-JR","John Arne Riise","Liverpool FC"),("PA-KDH","Kiernan Dewsbury-Hall","Everton"),("PA-KM","Kobbie Mainoo","Manchester United"),("PA-KS","Kevin Schade","Brentford"),("PA-KZ","Milos Kerkez","Liverpool FC"),("PA-LG","Lutsharel Geertruida","Sunderland"),("PA-LM","Lewis Miley","Newcastle United"),
("PA-LS","Leroy Sané","Manchester City"),("PA-LT","Loum Tchaouna","Burnley FC"),("PA-LY","Leny Yoro","Manchester United"),("PA-MA","Mikel Arteta","Arsenal"),("PA-MD","El Hadji Malick Diouf","West Ham United",R),("PA-ME","Michael Essien","Chelsea"),("PA-MI","Giorgi Mamardashvili","Liverpool FC"),("PA-MK","Mohammed Kudus","Tottenham Hotspur"),("PA-MM","Mason Mount","Manchester United"),("PA-MR","Morgan Rogers","Aston Villa"),
("PA-MS","Mohamed Salah","Liverpool FC"),("PA-MU","Manuel Ugarte","Manchester United"),("PA-MX","Max Dowman","Arsenal",R),("PA-MØ","Martin Ødegaard","Arsenal"),("PA-OG","Olivier Giroud","Arsenal"),("PA-PC","Philippe Coutinho","Liverpool FC"),("PA-PF","Phil Foden","Manchester City"),("PA-RM","Riyad Mahrez","Manchester City"),("PA-RN","Rio Ngumoha","Liverpool FC"),("PA-RO","Cristian Romero","Tottenham Hotspur"),
("PA-SE","Samuel Eto'o","Chelsea"),("PA-SG","Steven Gerrard","Liverpool FC"),("PA-SK","Benjamin Šeško","Manchester United"),("PA-SL","Shea Lacey","Manchester United",R),("PA-SM","Sadio Mané","Liverpool FC"),("PA-SP","Stuart Pearce","Nottingham Forest"),("PA-ST","Sandro Tonali","Newcastle United"),("PA-TD","Tyler Dibling","Everton"),("PA-TL","Tino Livramento","Newcastle United"),("PA-TR","Tijjani Reijnders","Manchester City"),
("PA-VS","Edwin van der Sar","Fulham"),("PA-VV","Rafael van der Vaart","Tottenham Hotspur"),("PA-WK","Danny Welbeck","Brighton & Hove Albion"),("PA-YA","Yasin Ayari","Brighton & Hove Albion",R),("PA-YO","Antoine Semenyo","Manchester City"),("PA-YY","Yehor Yarmolyuk","Brentford"),
], is_auto=True)

# ═══ PRISTINE LEGACY AUTOGRAPHS (PLA-, 21) [auto] ════════════════════════════
ins("Pristine Legacy Autographs", [
("PLA-AS","Alan Shearer","Newcastle United"),("PLA-BK","David Beckham","Manchester United"),("PLA-DB","Dennis Bergkamp","Arsenal"),("PLA-DD","Didier Drogba","Chelsea"),("PLA-EH","Eden Hazard","Chelsea"),("PLA-FL","Frank Lampard","Chelsea"),("PLA-FT","Fernando Torres","Liverpool FC"),("PLA-HK","Harry Kane","Tottenham Hotspur"),("PLA-HS","Heung-Min Son","Tottenham Hotspur"),("PLA-JT","John Terry","Chelsea"),
("PLA-KDB","Kevin De Bruyne","Manchester City"),("PLA-LS","Luis Suárez","Liverpool FC"),("PLA-PE","Peter Schmeichel","Manchester United"),("PLA-PS","Paul Scholes","Manchester United"),("PLA-PV","Patrick Vieira","Arsenal"),("PLA-RG","Ryan Giggs","Manchester United"),("PLA-RK","Roy Keane","Manchester United"),("PLA-SA","Sergio Agüero","Manchester City"),("PLA-SG","Steven Gerrard","Liverpool FC"),("PLA-TH","Thierry Henry","Arsenal"),
("PLA-WR","Wayne Rooney","Manchester United"),
], is_auto=True)

# ═══ PRISTINE SEASONS AUTOGRAPH EDITION (PSA-, 13) [auto] ════════════════════
ins("Pristine Seasons Autograph Edition", [
("PSA-AC","Andy Cole","Manchester United"),("PSA-AS","Alan Shearer","Newcastle United"),("PSA-EH","Eden Hazard","Chelsea"),("PSA-FL","Frank Lampard","Chelsea"),("PSA-HA","Erling Haaland","Manchester City"),("PSA-JT","John Terry","Chelsea"),("PSA-KP","Kevin Phillips","Sunderland"),("PSA-LS","Luis Suárez","Liverpool FC"),("PSA-MS","Mohamed Salah","Liverpool FC"),("PSA-PC","Petr Čech","Chelsea"),
("PSA-RK","Roy Keane","Manchester United"),("PSA-TH","Thierry Henry","Arsenal"),("PSA-VVD","Virgil van Dijk","Liverpool FC"),
], is_auto=True)

# ═══ PRISTINE PERSONAL ENDORSEMENTS AUTOGRAPHS (PPA-, 16) [auto] ═════════════
ins("Pristine Personal Endorsements Autographs", [
("PPA-AS","Alan Shearer","Newcastle United"),("PPA-AT","Ao Tanaka","Leeds United"),("PPA-BF","Bruno Fernandes","Manchester United"),("PPA-DB","David Beckham","Manchester United"),("PPA-DD","Didier Drogba","Chelsea"),("PPA-DR","Declan Rice","Arsenal"),("PPA-EG","Eidur Gudjohnsen","Chelsea"),("PPA-EH","Erling Haaland","Manchester City"),("PPA-EM","El Hadji Malick Diouf","West Ham United",R),("PPA-GB","Gareth Bale","Tottenham Hotspur"),
("PPA-PV","Patrick Vieira","Arsenal"),("PPA-RN","Rio Ngumoha","Liverpool FC",R),("PPA-TA","Thiago Alcântara","Liverpool FC"),("PPA-TH","Thierry Henry","Arsenal"),("PPA-TR","Tijjani Reijnders","Manchester City"),("PPA-TW","Tom Watson","Brighton & Hove Albion",R),
], is_auto=True)

# ═══ PRISTINE BIANCO (PB-, 20) [auto] ════════════════════════════════════════
ins("Pristine Bianco", [
("PB-AS","Alan Shearer","Newcastle United"),("PB-DB","Dennis Bergkamp","Arsenal"),("PB-DG","David Ginola","Tottenham Hotspur"),("PB-DS","David Silva","Manchester City"),("PB-EH","Eden Hazard","Chelsea"),("PB-EZE","Eberechi Eze","Arsenal"),("PB-GB","Gareth Bale","Tottenham Hotspur"),("PB-HA","Erling Haaland","Manchester City"),("PB-HE","Hugo Ekitike","Liverpool FC"),("PB-HK","Harry Kane","Tottenham Hotspur"),
("PB-JB","Jarrod Bowen","West Ham United"),("PB-JT","John Terry","Chelsea"),("PB-KD","Kevin De Bruyne","Manchester City"),("PB-MC","Moisés Caicedo","Chelsea"),("PB-MS","Mohamed Salah","Liverpool FC"),("PB-NQ","Niall Quinn","Sunderland"),("PB-PS","Paul Scholes","Manchester United"),("PB-RN","Rio Ngumoha","Liverpool FC",R),("PB-TR","Tijjani Reijnders","Manchester City"),("PB-TW","Tom Watson","Brighton & Hove Albion",R),
], is_auto=True)

# ═══ PRISTINE FROM THE PITCH (PFTP-, 18) [auto-relic] ════════════════════════
ins("Pristine From The Pitch", [
("PFTP-AR","Andy Robertson","Liverpool FC"),("PFTP-AW","Adam Wharton","Crystal Palace"),("PFTP-CP","Cole Palmer","Chelsea"),("PFTP-DK","Dejan Kulusevski","Tottenham Hotspur"),("PFTP-DO","Dango Ouattara","Brentford"),("PFTP-EH","Erling Haaland","Manchester City"),("PFTP-EZE","Eberechi Eze","Arsenal"),("PFTP-HW","Harry Wilson","Fulham"),("PFTP-JB","Jarrod Bowen","West Ham United"),("PFTP-KDB","Kevin De Bruyne","Manchester City"),
("PFTP-KS","Kevin Schade","Brentford"),("PFTP-KZ","Milos Kerkez","Liverpool FC"),("PFTP-MK","Mohammed Kudus","Tottenham Hotspur"),("PFTP-NC","Nathan Collins","Brentford"),("PFTP-RS","Ryan Sessegnon","Fulham"),("PFTP-TR","Tijjani Reijnders","Manchester City"),("PFTP-TS","Tomáš Souček","West Ham United"),("PFTP-WS","William Saliba","Arsenal"),
], is_auto=True)

# ═══ DAY 1 PRISTINE (PD1-, 4) [auto-relic] ═══════════════════════════════════
ins("Day 1 Pristine", [
("PD1-BM","Bryan Mbeumo","Manchester United"),("PD1-EH","Erling Haaland","Manchester City"),("PD1-EO","Estêvão Willian","Chelsea",R),("PD1-FW","Florian Wirtz","Liverpool FC"),
], is_auto=True)

# ═══ PRISTINE PAIRS DUAL AUTOGRAPHS (PP-, 15 × 2 subjects) [auto, join table] ═
pairs = [
("PP-AS","Manchester City","Leroy Sané",["Sergio Agüero"]),
("PP-BO","Everton","Leighton Baines",["Leon Osman"]),
("PP-DZ","Chelsea","Gianfranco Zola",["Marcel Desailly"]),
("PP-FK","Leeds United","Robbie Keane",["Robbie Fowler"]),
("PP-HF","Manchester City","Phil Foden",["Erling Haaland"]),
("PP-HG","Liverpool FC","Sami Hyypiä",["John Arne Riise"]),
("PP-IL","Manchester United","Amir Ibragimov",["Shea Lacey"]),
("PP-KG","Manchester United","Roy Keane",["Ryan Giggs"]),
("PP-PS","Arsenal","Gilberto Silva",["Emmanuel Petit"]),
("PP-RG","Liverpool FC","Ian Rush",["Steven Gerrard"]),
("PP-SA","Arsenal","David Seaman",["Tony Adams"]),
("PP-SE","Tottenham Hotspur","Gareth Bale",["Heung-Min Son"]),
("PP-SG","Liverpool FC","Steven Gerrard",["Mohamed Salah"]),
("PP-SS","Newcastle United","Nolberto Solano",["Alan Shearer"]),
("PP-TG","Newcastle United","Sandro Tonali",["Bruno Guimarães"]),
]
pp_id = ais("Pristine Pairs Dual Autographs", is_auto=True)
for num, team, primary, cos in pairs:
    p1 = goc(primary)
    db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, ?)", (p1, pp_id, num, team))
    aid = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    for co in cos:
        db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (aid, goc(co)))
print(f"  Pristine Pairs Dual Autographs: {len(pairs)} cards (dual)")

# ═══ POPULAR DEMAND AUTOGRAPH RELICS (PDAR-, 24) [auto-relic] ═════════════════
ins("Popular Demand Autograph Relics", [
("PDAR-BG","Bruno Guimarães","Newcastle United"),("PDAR-BS","Bukayo Saka","Arsenal"),("PDAR-CR","Cristian Romero","Tottenham Hotspur"),("PDAR-EH","Erling Haaland","Manchester City"),("PDAR-EM","Emiliano Martínez","Aston Villa"),("PDAR-ESR","Emile Smith Rowe","Fulham"),("PDAR-HK","Harry Kane","Tottenham Hotspur"),("PDAR-IK","Ibrahima Konaté","Liverpool FC"),("PDAR-JD","Jérémy Doku","Manchester City"),("PDAR-JP","João Palhinha","Tottenham Hotspur"),
("PDAR-MC","Matheus Cunha","Manchester United"),("PDAR-MD","El Hadji Malick Diouf","West Ham United",R),("PDAR-MK","Mohammed Kudus","Tottenham Hotspur"),("PDAR-MLS","Myles Lewis-Skelly","Arsenal"),("PDAR-MO","Mohamed Salah","Liverpool FC"),("PDAR-MR","Morgan Rogers","Aston Villa"),("PDAR-MX","Max Dowman","Arsenal",R),("PDAR-NM","Noni Madueke","Arsenal"),("PDAR-NV","Nemanja Vidić","Manchester United"),("PDAR-OD","Martin Ødegaard","Arsenal"),
("PDAR-PS","Peter Schmeichel","Manchester United"),("PDAR-SC","Sol Campbell","Arsenal"),("PDAR-WR","Wayne Rooney","Manchester United"),("PDAR-YB","Yannick Bolasie","Crystal Palace"),
], is_auto=True)

# ═══ PRISTINE PIECES AUTOGRAPH RELICS (PPAR-, 24) [auto-relic] ═══════════════
ins("Pristine Pieces Autograph Relics", [
("PPAR-AW","Adam Wharton","Crystal Palace"),("PPAR-BF","Bruno Fernandes","Manchester United"),("PPAR-DG","David Ginola","Aston Villa"),("PPAR-DK","Dejan Kulusevski","Tottenham Hotspur"),("PPAR-EH","Eden Hazard","Chelsea"),("PPAR-EM","Emiliano Martínez","Aston Villa"),("PPAR-FL","Frank Lampard","Chelsea"),("PPAR-FT","Fernando Torres","Liverpool FC"),("PPAR-GS","Ryan Giggs","Manchester United"),("PPAR-HW","Harry Wilson","Fulham"),
("PPAR-JB","Jarrod Bowen","West Ham United"),("PPAR-JC","Jamie Carragher","Liverpool FC"),("PPAR-JG","Jack Grealish","Everton"),("PPAR-JK","Josh King","Fulham",R),("PPAR-JR","John Arne Riise","Liverpool FC"),("PPAR-KDB","Kevin De Bruyne","Manchester City"),("PPAR-LS","Luis Suárez","Liverpool FC"),("PPAR-MD","Max Dowman","Arsenal",R),("PPAR-MK","Milos Kerkez","Liverpool FC"),("PPAR-RIO","Rio Ngumoha","Liverpool FC",R),
("PPAR-SG","Steven Gerrard","Liverpool FC"),("PPAR-SON","Heung-Min Son","Tottenham Hotspur"),("PPAR-TA","Tony Adams","Arsenal"),("PPAR-TH","Thierry Henry","Arsenal"),
], is_auto=True)

# ═══ ROOKIE JUMBO RELIC AUTOGRAPHS (PRJR-, 4) [auto-relic] ═══════════════════
ins("Rookie Jumbo Relic Autographs", [
("PRJR-EO","Estêvão Willian","Chelsea",R),("PRJR-JK","Josh King","Fulham",R),("PRJR-MD","Max Dowman","Arsenal",R),("PRJR-RN","Rio Ngumoha","Liverpool FC",R),
], is_auto=True)

db.commit()

# ═══ PARALLELS — derived from pack_odds keys (longest-prefix match) ═══════════
# Every odds key either names a subset exactly (subset-level odds, not a parallel)
# or is "<subset> <parallel>". Map each key to its longest matching subset name.
subset_rows = db.execute("SELECT id, name FROM insert_sets WHERE set_id = ?", (SET_ID,)).fetchall()
name_to_id = {n: i for i, n in subset_rows}
names_by_len = sorted(name_to_id.keys(), key=len, reverse=True)
odds = json.loads(pack_odds)
seen = set()
bad = []
n_par = 0
for key in odds:
    match = next((n for n in names_by_len if key == n or key.startswith(n + " ")), None)
    if match is None:
        bad.append(key); continue
    if key == match:
        continue  # subset-level odds, not a parallel
    par_name = key[len(match) + 1:]
    sig = (name_to_id[match], par_name)
    if sig in seen:
        continue
    seen.add(sig)
    db.execute("INSERT INTO parallels (insert_set_id, name, print_run, exclusivity) VALUES (?, ?, NULL, NULL)",
               (name_to_id[match], par_name))
    n_par += 1
db.commit()
print(f"  Parallels inserted (print_run NULL): {n_par}")
if bad:
    print("  !! PACK ODDS KEYS NOT MATCHING ANY SUBSET:")
    for b in bad: print(f"     {b}")

# ═══ VERIFICATION ════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
total = 0
EXPECT = {
    "Base":200,"Precisionaries":50,"Pure Strike":20,"Generational":10,"Perseverance":20,
    "Amped":20,"Pearlescent":40,"Pristine Seasons":20,"Glacier":20,"Pristine Ivory":50,
    "The Grail":1,"Pristine Autographs":77,"Pristine Legacy Autographs":21,
    "Pristine Seasons Autograph Edition":13,"Pristine Personal Endorsements Autographs":16,
    "Pristine Bianco":20,"Pristine From The Pitch":18,"Day 1 Pristine":4,
    "Pristine Pairs Dual Autographs":15,"Popular Demand Autograph Relics":24,
    "Pristine Pieces Autograph Relics":24,"Rookie Jumbo Relic Autographs":4,
}
for name, cnt in db.execute("""
    SELECT is2.name, COUNT(pa.id) FROM insert_sets is2
    LEFT JOIN player_appearances pa ON pa.insert_set_id = is2.id
    WHERE is2.set_id = ? GROUP BY is2.id ORDER BY is2.id""", (SET_ID,)).fetchall():
    total += cnt
    exp = EXPECT.get(name)
    flag = "" if exp == cnt else f"  <-- expected {exp}"
    print(f"  {name}: {cnt}{flag}")
print(f"  TOTAL: {total} (expected 687)")

n_players = db.execute("SELECT COUNT(*) FROM players WHERE set_id = ?", (SET_ID,)).fetchone()[0]
n_subsets = db.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id = ?", (SET_ID,)).fetchone()[0]
n_pars = db.execute("SELECT COUNT(*) FROM parallels WHERE insert_set_id IN (SELECT id FROM insert_sets WHERE set_id = ?)", (SET_ID,)).fetchone()[0]
n_co = db.execute("SELECT COUNT(*) FROM appearance_co_players WHERE appearance_id IN (SELECT pa.id FROM player_appearances pa JOIN insert_sets i ON i.id = pa.insert_set_id WHERE i.set_id = ?)", (SET_ID,)).fetchone()[0]
print(f"\n  Subsets: {n_subsets} (expected 22)")
print(f"  Unique players: {n_players}")
print(f"  Parallels: {n_pars}")
print(f"  Dual-auto co-player join rows: {n_co} (expected 15)")

# Mononym phantom check
phantom = db.execute("SELECT name FROM players WHERE set_id = ? AND name IN ('Kevin Fulham','André Wolverhampton Wanderers','Murillo Nottingham Forest','Beto Everton')", (SET_ID,)).fetchall()
print(f"  Mononym phantom check (expect 0): {len(phantom)} {phantom if phantom else ''}")

# G-7 collision
g7 = db.execute("""SELECT is2.name, p.name FROM player_appearances pa
    JOIN insert_sets is2 ON is2.id = pa.insert_set_id
    JOIN players p ON p.id = pa.player_id
    WHERE is2.set_id = ? AND pa.card_number = 'G-7' ORDER BY is2.name""", (SET_ID,)).fetchall()
print(f"  G-7 collision (expect Generational/Bruno Fernandes + The Grail/Zlatan): {g7}")

# PA-MØ non-ASCII card number preserved
pamo = db.execute("SELECT card_number FROM player_appearances pa JOIN insert_sets i ON i.id = pa.insert_set_id WHERE i.set_id = ? AND pa.card_number = 'PA-MØ'", (SET_ID,)).fetchone()
print(f"  PA-MØ preserved: {pamo[0] if pamo else 'MISSING'}")

print("Done!")
