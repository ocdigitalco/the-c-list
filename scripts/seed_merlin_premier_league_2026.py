"""
Seed: 2026 Topps Merlin Premier League — Full checklist (714 cards).
200 base, 13 inserts, 5 auto subsets (1 multi-subject trio), 1 auto-relic.
Two formats (Hobby + Value) with FULL dual-format pack odds AND print runs.
Usage: python3 scripts/seed_merlin_premier_league_2026.py
"""
import sqlite3, os, json, re, unicodedata

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
db = sqlite3.connect(DB_PATH)
db.execute("PRAGMA journal_mode=WAL")
db.execute("PRAGMA foreign_keys=ON")

box_config = json.dumps({
    "hobby": {"cards_per_pack": 4, "packs_per_box": 18, "boxes_per_case": 12, "autos_per_box": 1},
    "value": {"cards_per_pack": 4, "packs_per_box": 7, "boxes_per_case": 40, "autos_per_box": 0},
})

pack_odds = json.dumps({
  "Hobby": {
    "Refractor": "1:3", "Mojo": "1:6", "Vintage Merlin": "1:18",
    "Pink Refractor": "1:47", "Aqua Refractor": "1:42", "Aqua Mojo": "1:20",
    "Blue Refractor": "1:56", "Blue Mojo": "1:27",
    "Green Refractor": "1:96", "Green Mojo": "1:40",
    "Purple Refractor": "1:120", "Purple Mojo": "1:53",
    "Gold Refractor": "1:215", "Gold Mojo": "1:79",
    "Orange Refractor": "1:355", "Orange Mojo": "1:157",
    "Black Refractor": "1:1040", "Black Mojo": "1:392",
    "Red Refractor": "1:1825", "Red Mojo": "1:784",
    "SuperFractor": "1:5712",
    "Merlin Premier League 1996 Edition": "1:375",
    "Merlin Premier League 1996 Edition Black Refractor": "1:2201",
    "Merlin Premier League 1996 Edition Red Refractor": "1:4157",
    "Merlin Premier League 1996 Edition SuperFractor": "1:23382",
    "Fantasy Football": "1:2",
    "Fantasy Football Gold Refractor": "1:220",
    "Fantasy Football Orange Refractor": "1:480",
    "Fantasy Football Black Refractor": "1:1066",
    "Fantasy Football Red Refractor": "1:2598",
    "Fantasy Football SuperFractor": "1:11691",
    "Mystic Afternoons": "1:2",
    "Mystic Afternoons Gold Refractor": "1:220",
    "Mystic Afternoons Orange Refractor": "1:480",
    "Mystic Afternoons Black Refractor": "1:1066",
    "Mystic Afternoons Red Refractor": "1:2598",
    "Mystic Afternoons SuperFractor": "1:11691",
    "Merlin's Young Magicians": "1:2",
    "Merlin's Young Magicians Gold Refractor": "1:220",
    "Merlin's Young Magicians Orange Refractor": "1:480",
    "Merlin's Young Magicians Black Refractor": "1:1066",
    "Merlin's Young Magicians Red Refractor": "1:2598",
    "Merlin's Young Magicians SuperFractor": "1:11691",
    "Merlin Speaks": "1:2",
    "Merlin Speaks Gold Refractor": "1:220",
    "Merlin Speaks Orange Refractor": "1:480",
    "Merlin Speaks Black Refractor": "1:1066",
    "Merlin Speaks Red Refractor": "1:2598",
    "Merlin Speaks SuperFractor": "1:11691",
    "Merlin's Mythical Art": "1:216",
    "Merlin's Mythical Art Kaleidoscope": "1:3131",
    "Merlin's Mythical Art Shimmer": "1:7877",
    "Merlin's Mythical Art RayWave": "1:15588",
    "Merlin's Mythical Art SuperFractor": "1:74823",
    "Magic in His Boots": "1:998",
    "Magic in His Boots Red Refractor": "1:5543",
    "Magic in His Boots SuperFractor": "1:29929",
    "Renaissance": "1:832",
    "Renaissance Red Refractor": "1:10392",
    "Renaissance SuperFractor": "1:53445",
    "Merlin's Magnum Opus": "1:4157",
    "Merlin's Magnum Opus SuperFractor": "1:46764",
    "The Shiny": "1:502",
    "The Shiny Gold Speckle": "1:46764",
    "Autograph Variations": "1:65",
    "Autograph Variations Blue Refractor": "1:104",
    "Autograph Variations Green Refractor": "1:147",
    "Autograph Variations Purple Refractor": "1:175",
    "Autograph Variations Gold Refractor": "1:246",
    "Autograph Variations Orange Refractor": "1:466",
    "Autograph Variations Black Refractor": "1:1132",
    "Autograph Variations Red Refractor": "1:2195",
    "Autograph Variations SuperFractor": "1:11004",
    "Enchanted Pen": "1:933",
    "Enchanted Pen Gold Refractor": "1:1134",
    "Enchanted Pen Orange Refractor": "1:2361",
    "Enchanted Pen Black Refractor": "1:5345",
    "Enchanted Pen Red Refractor": "1:10689",
    "Enchanted Pen SuperFractor": "1:49882",
    "Mystic Afternoons Autographs": "1:1069",
    "Mystic Afternoons Autographs Gold Refractor": "1:2208",
    "Mystic Afternoons Autographs Orange Refractor": "1:4276",
    "Mystic Afternoons Autographs Black Refractor": "1:10250",
    "Mystic Afternoons Autographs Red Refractor": "1:18250",
    "Mystic Afternoons Autographs SuperFractor": "1:83136",
    "Spellbinding Trios": "1:3563",
    "Spellbinding Trios Black Refractor": "1:16628",
    "Spellbinding Trios Red Refractor": "1:32532",
    "Spellbinding Trios SuperFractor": "1:149645",
    "Merlin's Magical Ink Kaleidoscope": "1:1667",
    "Merlin's Magical Ink Black Kaleidoscope": "1:3563",
    "Merlin's Magical Ink Red Kaleidoscope": "1:7483",
    "Merlin's Magical Ink SuperFractor": "1:35630",
    "Merlin's Match Ball Signatures": "1:331",
    "Merlin's Match Ball Signatures Orange Refractor": "1:990",
    "Merlin's Match Ball Signatures Black Refractor": "1:2478",
    "Merlin's Match Ball Signatures Red Refractor": "1:4619",
    "Merlin's Match Ball Signatures SuperFractor": "1:23382",
    "Mask Off": "1:24941",
    "Mask Off Red & White Refractor": "1:93528",
    "Mask Off Black Refractor": "1:106890",
    "Mask Off Red Refractor": "1:249408",
    "Mask Off SuperFractor": "1:748224"
  },
  "Value": {
    "Refractor": "1:3", "RayWave": "1:2", "VHS Refractor": "1:7",
    "Pink Refractor": "1:29", "Aqua Refractor": "1:46",
    "Blue Refractor": "1:61", "Green Refractor": "1:82",
    "Battle of Britpop Refractor": "1:51",
    "Purple Refractor": "1:113", "Gold Refractor": "1:151",
    "Orange Refractor": "1:346", "Black Refractor": "1:791",
    "Red Refractor": "1:1786", "SuperFractor": "1:17679",
    "Merlin Premier League 1996 Edition": "1:1804",
    "Merlin Premier League 1996 Edition Black Refractor": "1:7577",
    "Merlin Premier League 1996 Edition Red Refractor": "1:19183",
    "Merlin Premier League 1996 Edition SuperFractor": "1:90160",
    "Fantasy Football": "1:2",
    "Fantasy Football Gold Refractor": "1:707",
    "Fantasy Football Orange Refractor": "1:1145",
    "Fantasy Football Black Refractor": "1:3837",
    "Fantasy Football Red Refractor": "1:5094",
    "Fantasy Football SuperFractor": "1:36064",
    "Mystic Afternoons": "1:2",
    "Mystic Afternoons Gold Refractor": "1:707",
    "Mystic Afternoons Orange Refractor": "1:1145",
    "Mystic Afternoons Black Refractor": "1:3837",
    "Mystic Afternoons Red Refractor": "1:5094",
    "Mystic Afternoons SuperFractor": "1:36064",
    "Merlin's Young Magicians": "1:2",
    "Merlin's Young Magicians Gold Refractor": "1:707",
    "Merlin's Young Magicians Orange Refractor": "1:1145",
    "Merlin's Young Magicians Black Refractor": "1:3837",
    "Merlin's Young Magicians Red Refractor": "1:5094",
    "Merlin's Young Magicians SuperFractor": "1:36064",
    "Merlin Speaks": "1:2",
    "Merlin Speaks Gold Refractor": "1:707",
    "Merlin Speaks Orange Refractor": "1:1145",
    "Merlin Speaks Black Refractor": "1:3837",
    "Merlin Speaks Red Refractor": "1:5094",
    "Merlin Speaks SuperFractor": "1:36064",
    "Rainbow Flick": "1:280",
    "Rainbow Flick Black Refractor": "1:3990",
    "Rainbow Flick Red Refractor": "1:8754",
    "Rainbow Flick SuperFractor": "1:53036",
    "Ta-Da": "1:3",
    "Ta-Da Green Refractor": "1:194",
    "Ta-Da Purple Refractor": "1:256",
    "Ta-Da Gold Refractor": "1:384",
    "Ta-Da Orange Refractor": "1:781",
    "Ta-Da Black Refractor": "1:1965",
    "Ta-Da Red Refractor": "1:3972",
    "Ta-Da SuperFractor": "1:21467",
    "Magic in His Boots": "1:3607",
    "Magic in His Boots Red Refractor": "1:18032",
    "Magic in His Boots SuperFractor": "1:75134",
    "Renaissance": "1:9016",
    "Renaissance Red Refractor": "1:45080",
    "Renaissance SuperFractor": "1:225400",
    "Merlin's Magnum Opus": "1:45080",
    "Merlin's Magnum Opus SuperFractor": "1:450800",
    "The Shiny": "1:1779",
    "The Shiny Gold Speckle": "1:450800",
    "Autograph Variations": "1:229",
    "Autograph Variations Blue Refractor": "1:2227",
    "Autograph Variations Green Refractor": "1:2947",
    "Autograph Variations Purple Refractor": "1:3870",
    "Autograph Variations Gold Refractor": "1:5152",
    "Autograph Variations Orange Refractor": "1:7213",
    "Autograph Variations Black Refractor": "1:12880",
    "Autograph Variations Red Refractor": "1:20491",
    "Autograph Variations SuperFractor": "1:90160",
    "Enchanted Pen": "1:3220",
    "Enchanted Pen Gold Refractor": "1:7514",
    "Enchanted Pen Orange Refractor": "1:12351",
    "Enchanted Pen Black Refractor": "1:33393",
    "Enchanted Pen Red Refractor": "1:69354",
    "Enchanted Pen SuperFractor": "1:300534",
    "Mystic Afternoons Autographs": "1:2424",
    "Mystic Afternoons Autographs Gold Refractor": "1:17679",
    "Mystic Afternoons Autographs Orange Refractor": "1:20491",
    "Mystic Afternoons Autographs Black Refractor": "1:60107",
    "Mystic Afternoons Autographs Red Refractor": "1:112700",
    "Mystic Afternoons Autographs SuperFractor": "1:450800",
    "Spellbinding Trios": "1:27322",
    "Spellbinding Trios Black Refractor": "1:64400",
    "Spellbinding Trios Red Refractor": "1:150267",
    "Spellbinding Trios SuperFractor": "1:901600",
    "Merlin's Magical Ink Kaleidoscope": "1:28175",
    "Merlin's Magical Ink Black Kaleidoscope": "1:32200",
    "Merlin's Magical Ink Red Kaleidoscope": "1:42934",
    "Merlin's Magical Ink SuperFractor": "1:300534",
    "Mask Off": "1:45080",
    "Mask Off Red & White Refractor": "1:150267",
    "Mask Off Black Refractor": "1:300534",
    "Mask Off Red Refractor": "1:450800"
  }
})

db.execute("""
    INSERT INTO sets (name, sport, season, league, tier, slug, is_visible,
                      sample_image_url, release_date, box_config, pack_odds, created_at)
    VALUES ('2026 Topps Merlin Premier League', 'Soccer', '2026', 'Premier League', 'Merlin',
            '2026-merlin-premier-league', 1,
            '/sets/2026-merlin-premier-league-soccer.jpg', '2026-06-11', ?, ?, '2026-06-09T12:00:00Z')
""", (box_config, pack_odds))
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

# parallels: list of (name, print_run_or_None, exclusivity_or_None)
def par(is_id, plist):
    for pname, prun, excl in plist:
        db.execute("INSERT INTO parallels (insert_set_id, name, print_run, exclusivity) VALUES (?, ?, ?, ?)",
                   (is_id, pname, prun, excl))

R = True; F = False

# ═══ BASE (200) ══════════════════════════════════════════════════════════════
base_id = ins("Base", [
(1,"Alex Scott","AFC Bournemouth"),(2,"Marcos Senesi","AFC Bournemouth"),(3,"Marcus Tavernier","AFC Bournemouth"),(4,"Julio Soler","AFC Bournemouth",R),(5,"Junior Kroupi","AFC Bournemouth"),(6,"Evanilson","AFC Bournemouth"),(7,"Adrien Truffert","AFC Bournemouth"),(8,"Amine Adli","AFC Bournemouth"),(9,"Veljko Milosavljević","AFC Bournemouth",R),(10,"Bafodé Diakité","AFC Bournemouth"),
(11,"Bukayo Saka","Arsenal"),(12,"Viktor Gyökeres","Arsenal"),(13,"Martin Ødegaard","Arsenal"),(14,"Eberechi Eze","Arsenal"),(15,"Noni Madueke","Arsenal"),(16,"Martín Zubimendi","Arsenal"),(17,"Mikel Merino","Arsenal"),(18,"Andre Harriman-Annous","Arsenal",R),(19,"Josh Nichols","Arsenal",R),(20,"Max Dowman","Arsenal",R),
(21,"Ian Maatsen","Aston Villa"),(22,"Morgan Rogers","Aston Villa"),(23,"Ollie Watkins","Aston Villa"),(24,"Amadou Onana","Aston Villa"),(25,"Youri Tielemans","Aston Villa"),(26,"Bradley Burrowes","Aston Villa",R),(27,"Jamaldeen Jimoh-Aloba","Aston Villa",R),(28,"Matty Cash","Aston Villa"),(29,"Lamare Bogarde","Aston Villa"),(30,"Boubacar Kamara","Aston Villa"),
(31,"Mathias Jensen","Brentford"),(32,"Mikkel Damsgaard","Brentford"),(33,"Kevin Schade","Brentford"),(34,"Dango Ouattara","Brentford"),(35,"Igor Thiago","Brentford"),(36,"Jordan Henderson","Brentford"),(37,"Michael Kayode","Brentford"),(38,"Caoimhín Kelleher","Brentford"),(39,"Nathan Collins","Brentford"),(40,"Yehor Yarmolyuk","Brentford"),
(41,"Yasin Ayari","Brighton & Hove Albion",R),(42,"Tom Watson","Brighton & Hove Albion",R),(43,"Kaoru Mitoma","Brighton & Hove Albion"),(44,"Yankuba Minteh","Brighton & Hove Albion"),(45,"Diego Gómez","Brighton & Hove Albion"),(46,"Lewis Dunk","Brighton & Hove Albion"),(47,"Jan Paul van Hecke","Brighton & Hove Albion"),(48,"Ferdi Kadioglu","Brighton & Hove Albion"),(49,"Harry Howell","Brighton & Hove Albion",R),(50,"Stefanos Tzimas","Brighton & Hove Albion",R),
(51,"Jaidon Anthony","Burnley FC"),(52,"Marcus Edwards","Burnley FC"),(53,"Kyle Walker","Burnley FC"),(54,"Josh Laurent","Burnley FC",R),(55,"Florentino Luís","Burnley FC"),(56,"Martin Dúbravka","Burnley FC"),(57,"Quilindschy Hartman","Burnley FC"),(58,"Jacob Bruun Larsen","Burnley FC"),(59,"Lyle Foster","Burnley FC"),(60,"Josh Cullen","Burnley FC"),
(61,"Moisés Caicedo","Chelsea"),(62,"Reece James","Chelsea"),(63,"Estêvão Willian","Chelsea",R),(64,"Roméo Lavia","Chelsea"),(65,"João Pedro","Chelsea"),(66,"Liam Delap","Chelsea"),(67,"Cole Palmer","Chelsea"),(68,"Josh Acheampong","Chelsea"),(69,"Marc Cucurella","Chelsea"),(70,"Alejandro Garnacho","Chelsea"),
(71,"Daniel Muñoz","Crystal Palace"),(72,"Daichi Kamada","Crystal Palace"),(73,"Justin Devenny","Crystal Palace",R),(74,"Yéremy Pino","Crystal Palace"),(75,"Ismaïla Sarr","Crystal Palace"),(76,"Joél Drakes-Thomas","Crystal Palace",R),(77,"Adam Wharton","Crystal Palace"),(78,"Jaydee Canvot","Crystal Palace",R),(79,"Tyrick Mitchell","Crystal Palace"),(80,"Jefferson Lerma","Crystal Palace"),
(81,"Merlin Röhl","Everton"),(82,"Iliman Ndiaye","Everton"),(83,"Jack Grealish","Everton"),(84,"Tyler Dibling","Everton"),(85,"Tim Iroegbunam","Everton"),(86,"Kiernan Dewsbury-Hall","Everton"),(87,"Jake O'Brien","Everton"),(88,"Idrissa Gueye","Everton"),(89,"Jordan Pickford","Everton"),(90,"Vitalii Mykolenko","Everton"),
(91,"Josh King","Fulham",R),(92,"Emile Smith Rowe","Fulham"),(93,"Harry Wilson","Fulham"),(94,"Jonah Kusi-Asare","Fulham",R),(95,"Kevin","Fulham"),(96,"Calvin Bassey","Fulham"),(97,"Ryan Sessegnon","Fulham"),(98,"Sander Berge","Fulham"),(99,"Joachim Andersen","Fulham"),(100,"Saša Lukić","Fulham"),
(101,"Dominic Calvert-Lewin","Leeds United"),(102,"Ethan Ampadu","Leeds United"),(103,"Gabriel Gudmundsson","Leeds United"),(104,"Ao Tanaka","Leeds United"),(105,"Sean Longstaff","Leeds United"),(106,"Daniel James","Leeds United"),(107,"Lukas Nmecha","Leeds United"),(108,"Jayden Bogle","Leeds United"),(109,"Wilfried Gnonto","Leeds United"),(110,"Anton Stach","Leeds United"),
(111,"Rio Ngumoha","Liverpool FC",R),(112,"Federico Chiesa","Liverpool FC"),(113,"Virgil van Dijk","Liverpool FC"),(114,"Alexander Isak","Liverpool FC"),(115,"Mohamed Salah","Liverpool FC"),(116,"Florian Wirtz","Liverpool FC"),(117,"Hugo Ekitike","Liverpool FC"),(118,"Cody Gakpo","Liverpool FC"),(119,"Conor Bradley","Liverpool FC"),(120,"Ryan Gravenberch","Liverpool FC"),
(121,"Tijjani Reijnders","Manchester City"),(122,"Phil Foden","Manchester City"),(123,"Erling Haaland","Manchester City"),(124,"Rayan Cherki","Manchester City"),(125,"Rodri","Manchester City"),(126,"Divine Mukasa","Manchester City",R),(127,"Jérémy Doku","Manchester City"),(128,"Abdukodir Khusanov","Manchester City"),(129,"Antoine Semenyo","Manchester City"),(130,"Rúben Dias","Manchester City"),
(131,"Bryan Mbeumo","Manchester United"),(132,"Amir Ibragimov","Manchester United",R),(133,"Matheus Cunha","Manchester United"),(134,"Bruno Fernandes","Manchester United"),(135,"Benjamin Šeško","Manchester United"),(136,"Leny Yoro","Manchester United"),(137,"Casemiro","Manchester United"),(138,"Shea Lacey","Manchester United",R),(139,"Bendito Mantato","Manchester United",R),(140,"Jack Fletcher","Manchester United",R),
(141,"Bruno Guimarães","Newcastle United"),(142,"Anthony Gordon","Newcastle United"),(143,"Nick Woltemade","Newcastle United"),(144,"Sven Botman","Newcastle United"),(145,"Malick Thiaw","Newcastle United"),(146,"Jacob Ramsey","Newcastle United"),(147,"Kieran Trippier","Newcastle United"),(148,"Sandro Tonali","Newcastle United"),(149,"Harvey Barnes","Newcastle United"),(150,"Joe Willock","Newcastle United"),
(151,"Igor Jesus","Nottingham Forest",R),(152,"Callum Hudson-Odoi","Nottingham Forest"),(153,"Morgan Gibbs-White","Nottingham Forest"),(154,"Zach Abbott","Nottingham Forest",R),(155,"Jair","Nottingham Forest",R),(156,"Ibrahim Sangaré","Nottingham Forest"),(157,"Nikola Milenković","Nottingham Forest"),(158,"Murillo","Nottingham Forest"),(159,"Chris Wood","Nottingham Forest"),(160,"Dilane Bakwa","Nottingham Forest",R),
(161,"Noah Sadiki","Sunderland",R),(162,"Eliezer Mayenda","Sunderland",R),(163,"Chris Rigg","Sunderland",R),(164,"Dan Ballard","Sunderland",R),(165,"Simon Adingra","Sunderland"),(166,"Granit Xhaka","Sunderland"),(167,"Chemsdine Talbi","Sunderland"),(168,"Nordi Mukiele","Sunderland"),(169,"Robin Roefs","Sunderland",R),(170,"Trai Hume","Sunderland",R),
(171,"Xavi Simons","Tottenham Hotspur"),(172,"Mohammed Kudus","Tottenham Hotspur"),(173,"Kevin Danso","Tottenham Hotspur"),(174,"Richarlison","Tottenham Hotspur"),(175,"Conor Gallagher","Tottenham Hotspur"),(176,"Dominic Solanke","Tottenham Hotspur"),(177,"João Palhinha","Tottenham Hotspur"),(178,"Pape Matar Sarr","Tottenham Hotspur"),(179,"Rodrigo Bentancur","Tottenham Hotspur"),(180,"Cristian Romero","Tottenham Hotspur"),
(181,"El Hadji Malick Diouf","West Ham United",R),(182,"Soungoutou Magassa","West Ham United"),(183,"Crysencio Summerville","West Ham United"),(184,"Konstantinos Mavropanos","West Ham United"),(185,"Freddie Potts","West Ham United",R),(186,"Kyle Walker-Peters","West Ham United"),(187,"Mateus Fernandes","West Ham United"),(188,"Mohamadou Kanté","West Ham United",R),(189,"Jarrod Bowen","West Ham United"),(190,"Pablo Felipe","West Ham United",R),
(191,"Tolu Arokodare","Wolverhampton Wanderers",R),(192,"Jackson Tchatchoua","Wolverhampton Wanderers"),(193,"João Gomes","Wolverhampton Wanderers"),(194,"Fer López","Wolverhampton Wanderers",R),(195,"Toti Gomes","Wolverhampton Wanderers"),(196,"Hugo Bueno","Wolverhampton Wanderers"),(197,"Ladislav Krejci","Wolverhampton Wanderers"),(198,"David Møller Wolfe","Wolverhampton Wanderers"),(199,"André","Wolverhampton Wanderers"),(200,"Mateus Mané","Wolverhampton Wanderers",R),
])
par(base_id, [
("Refractor",None,None),("Mojo",None,"Hobby"),("RayWave",None,"Value"),("VHS Refractor",None,"Value"),("Vintage Merlin",None,"Hobby"),
("Pink Refractor",250,None),("Aqua Refractor",199,None),("Aqua Mojo",199,"Hobby"),("Blue Refractor",150,None),("Blue Mojo",150,"Hobby"),
("Green Refractor",99,None),("Green Mojo",99,"Hobby"),("Battle of Britpop Refractor",95,"Value"),("Purple Refractor",75,None),("Purple Mojo",75,"Hobby"),
("Gold Refractor",50,None),("Gold Mojo",50,"Hobby"),("Orange Refractor",25,None),("Orange Mojo",25,"Hobby"),
("Black Refractor",10,None),("Black Mojo",10,"Hobby"),("Red Refractor",5,None),("Red Mojo",5,"Hobby"),("SuperFractor",1,None),
])

# ═══ MERLIN PREMIER LEAGUE 1996 EDITION (M-, 50) ════════════════════════════
m96 = ins("Merlin Premier League 1996 Edition", [
("M-1","Alex Scott","AFC Bournemouth"),("M-2","Veljko Milosavljević","AFC Bournemouth",R),("M-3","Bukayo Saka","Arsenal"),("M-4","Jurriën Timber","Arsenal"),("M-5","Eberechi Eze","Arsenal"),
("M-6","Youri Tielemans","Aston Villa"),("M-7","Jamaldeen Jimoh-Aloba","Aston Villa",R),("M-8","Nathan Collins","Brentford"),("M-9","Igor Thiago","Brentford"),("M-10","Tom Watson","Brighton & Hove Albion",R),
("M-11","Yankuba Minteh","Brighton & Hove Albion"),("M-12","Kaoru Mitoma","Brighton & Hove Albion"),("M-13","Jaidon Anthony","Burnley FC"),("M-14","Marcus Edwards","Burnley FC"),("M-15","Moisés Caicedo","Chelsea"),
("M-16","Cole Palmer","Chelsea"),("M-17","Estêvão Willian","Chelsea",R),("M-18","Daniel Muñoz","Crystal Palace"),("M-19","Adam Wharton","Crystal Palace"),("M-20","Jordan Pickford","Everton"),
("M-21","Jack Grealish","Everton"),("M-22","Harry Wilson","Fulham"),("M-23","Josh King","Fulham",R),("M-24","Kevin","Fulham"),("M-25","Jayden Bogle","Leeds United"),
("M-26","Anton Stach","Leeds United"),("M-27","Mohamed Salah","Liverpool FC"),("M-28","Rio Ngumoha","Liverpool FC",R),("M-29","Hugo Ekitike","Liverpool FC"),("M-30","Phil Foden","Manchester City"),
("M-31","Erling Haaland","Manchester City"),("M-32","Rodri","Manchester City"),("M-33","Matheus Cunha","Manchester United"),("M-34","Benjamin Šeško","Manchester United"),("M-35","Bruno Fernandes","Manchester United"),
("M-36","Bruno Guimarães","Newcastle United"),("M-37","Nick Woltemade","Newcastle United"),("M-38","Anthony Gordon","Newcastle United"),("M-39","Igor Jesus","Nottingham Forest",R),("M-40","Morgan Gibbs-White","Nottingham Forest"),
("M-41","Eliezer Mayenda","Sunderland",R),("M-42","Chris Rigg","Sunderland",R),("M-43","Granit Xhaka","Sunderland"),("M-44","Xavi Simons","Tottenham Hotspur"),("M-45","João Palhinha","Tottenham Hotspur"),
("M-46","El Hadji Malick Diouf","West Ham United",R),("M-47","Pablo Felipe","West Ham United",R),("M-48","Soungoutou Magassa","West Ham United"),("M-49","Fer López","Wolverhampton Wanderers",R),("M-50","André","Wolverhampton Wanderers"),
])
par(m96, [("Black Refractor",10,None),("Red Refractor",5,None),("SuperFractor",1,None)])

COMMON_PARS = [("Gold Refractor",50,None),("Orange Refractor",25,None),("Black Refractor",10,None),("Red Refractor",5,None),("SuperFractor",1,None)]

# ═══ FANTASY FOOTBALL (FF-, 40) ══════════════════════════════════════════════
ff = ins("Fantasy Football", [
("FF-1","Ben White","Arsenal"),("FF-2","Kai Havertz","Arsenal"),("FF-3","Emiliano Buendía","Aston Villa"),("FF-4","Boubacar Kamara","Aston Villa"),("FF-5","David Brooks","AFC Bournemouth"),
("FF-6","Junior Kroupi","AFC Bournemouth"),("FF-7","Fábio Carvalho","Brentford"),("FF-8","Aaron Hickey","Brentford"),("FF-9","Brajan Gruda","Brighton & Hove Albion"),("FF-10","Maxim De Cuyper","Brighton & Hove Albion",R),
("FF-11","Quilindschy Hartman","Burnley FC"),("FF-12","Jacob Bruun Larsen","Burnley FC"),("FF-13","Pedro Neto","Chelsea"),("FF-14","Dário Essugo","Chelsea"),("FF-15","Daichi Kamada","Crystal Palace"),
("FF-16","Will Hughes","Crystal Palace"),("FF-17","Iliman Ndiaye","Everton"),("FF-18","Idrissa Gueye","Everton"),("FF-19","Emile Smith Rowe","Fulham"),("FF-20","Harry Wilson","Fulham"),
("FF-21","Noah Okafor","Leeds United"),("FF-22","Ao Tanaka","Leeds United"),("FF-23","Alexis Mac Allister","Liverpool FC"),("FF-24","Dominik Szoboszlai","Liverpool FC"),("FF-25","Antoine Semenyo","Manchester City"),
("FF-26","Nico O'Reilly","Manchester City"),("FF-27","Kobbie Mainoo","Manchester United"),("FF-28","Mason Mount","Manchester United"),("FF-29","Joelinton","Newcastle United"),("FF-30","Fabian Schär","Newcastle United"),
("FF-31","Callum Hudson-Odoi","Nottingham Forest"),("FF-32","Dan Ndoye","Nottingham Forest"),("FF-33","Wilson Isidor","Sunderland",R),("FF-34","Luke O'Nien","Sunderland",R),("FF-35","Cristian Romero","Tottenham Hotspur"),
("FF-36","Micky van de Ven","Tottenham Hotspur"),("FF-37","Crysencio Summerville","West Ham United"),("FF-38","Taty Castellanos","West Ham United"),("FF-39","Rodrigo Gomes","Wolverhampton Wanderers"),("FF-40","Jean-Ricner Bellegarde","Wolverhampton Wanderers"),
])
par(ff, COMMON_PARS)

# ═══ MYSTIC AFTERNOONS (MA-, 20) ═════════════════════════════════════════════
ma = ins("Mystic Afternoons", [
("MA-1","Evanilson","AFC Bournemouth"),("MA-2","Martin Ødegaard","Arsenal"),("MA-3","Ollie Watkins","Aston Villa"),("MA-4","Kevin Schade","Brentford"),("MA-5","Yasin Ayari","Brighton & Hove Albion",R),
("MA-6","Kyle Walker","Burnley FC"),("MA-7","Estêvão Willian","Chelsea",R),("MA-8","Adam Wharton","Crystal Palace"),("MA-9","Merlin Röhl","Everton"),("MA-10","Enzo Fernández","Chelsea"),
("MA-11","Dominic Calvert-Lewin","Leeds United"),("MA-12","Rio Ngumoha","Liverpool FC",R),("MA-13","Erling Haaland","Manchester City"),("MA-14","Casemiro","Manchester United"),("MA-15","Anthony Elanga","Newcastle United"),
("MA-16","Elliot Anderson","Nottingham Forest"),("MA-17","Noah Sadiki","Sunderland",R),("MA-18","Mohammed Kudus","Tottenham Hotspur"),("MA-19","Virgil van Dijk","Liverpool FC"),("MA-20","Tolu Arokodare","Wolverhampton Wanderers",R),
])
par(ma, COMMON_PARS)

# ═══ MERLIN'S YOUNG MAGICIANS (YM-, 20) ══════════════════════════════════════
ym = ins("Merlin's Young Magicians", [
("YM-1","Veljko Milosavljević","AFC Bournemouth",R),("YM-2","Junior Kroupi","AFC Bournemouth"),("YM-3","Max Dowman","Arsenal",R),("YM-4","Bradley Burrowes","Aston Villa",R),("YM-5","Jamaldeen Jimoh-Aloba","Aston Villa",R),
("YM-6","Tom Watson","Brighton & Hove Albion",R),("YM-7","Stefanos Tzimas","Brighton & Hove Albion",R),("YM-8","Estêvão Willian","Chelsea",R),("YM-9","Jorrel Hato","Chelsea"),("YM-10","Tyler Dibling","Everton"),
("YM-11","Josh King","Fulham",R),("YM-12","Rio Ngumoha","Liverpool FC",R),("YM-13","Divine Mukasa","Manchester City",R),("YM-14","Leny Yoro","Manchester United"),("YM-15","Lewis Miley","Newcastle United"),
("YM-16","Eliezer Mayenda","Sunderland",R),("YM-17","Chris Rigg","Sunderland",R),("YM-18","Archie Gray","Tottenham Hotspur"),("YM-19","Lucas Bergvall","Tottenham Hotspur"),("YM-20","Freddie Potts","West Ham United",R),
])
par(ym, COMMON_PARS)

# ═══ MERLIN SPEAKS (MS-, 20) ═════════════════════════════════════════════════
ms = ins("Merlin Speaks", [
("MS-1","Riccardo Calafiori","Arsenal"),("MS-2","Álex Jiménez","AFC Bournemouth"),("MS-3","Morgan Rogers","Aston Villa"),("MS-4","Carlos Baleba","Brighton & Hove Albion"),("MS-5","Loum Tchaouna","Burnley FC"),
("MS-6","Cole Palmer","Chelsea"),("MS-7","Eddie Nketiah","Crystal Palace"),("MS-8","Jarrad Branthwaite","Everton"),("MS-9","Raúl Jiménez","Fulham"),("MS-10","Alexander Isak","Liverpool FC"),
("MS-11","Brenden Aaronson","Leeds United"),("MS-12","Rayan Cherki","Manchester City"),("MS-13","Bruno Fernandes","Manchester United"),("MS-14","Nick Woltemade","Newcastle United"),("MS-15","James McAtee","Nottingham Forest"),
("MS-16","Simon Adingra","Sunderland"),("MS-17","Archie Gray","Tottenham Hotspur"),("MS-18","Ollie Scarles","West Ham United"),("MS-19","Mikkel Damsgaard","Brentford"),("MS-20","James Milner","Brighton & Hove Albion"),
])
par(ms, COMMON_PARS)

# ═══ TA-DA (TD-, 50) [Value exclusive] ═══════════════════════════════════════
td = ins("Ta-Da", [
("TD-1","Julio Soler","AFC Bournemouth",R),("TD-2","Tyler Adams","AFC Bournemouth"),("TD-3","Cristhian Mosquera","Arsenal"),("TD-4","Declan Rice","Arsenal"),("TD-5","Tony Adams","Arsenal"),
("TD-6","Youri Tielemans","Aston Villa"),("TD-7","Lucas Digne","Aston Villa"),("TD-8","Gareth Barry","Aston Villa"),("TD-9","Vitaly Janelt","Brentford"),("TD-10","Mathias Jensen","Brentford"),
("TD-11","Charalampos Kostoulas","Brighton & Hove Albion"),("TD-12","James Milner","Brighton & Hove Albion"),("TD-13","Josh Cullen","Burnley FC"),("TD-14","Zian Flemming","Burnley FC",R),("TD-15","Malo Gusto","Chelsea"),
("TD-16","Alejandro Garnacho","Chelsea"),("TD-17","Ashley Cole","Chelsea"),("TD-18","Jaydee Canvot","Crystal Palace",R),("TD-19","João Gomes","Wolverhampton Wanderers"),("TD-20","Yannick Bolasie","Crystal Palace"),
("TD-21","Charly Alcaraz","Everton"),("TD-22","Jake O'Brien","Everton"),("TD-23","Neville Southall","Everton"),("TD-24","Tom Cairney","Fulham"),("TD-25","Sander Berge","Fulham"),
("TD-26","Anton Stach","Leeds United"),("TD-27","Joe Rodon","Leeds United"),("TD-28","Alexander Isak","Liverpool FC"),("TD-29","Virgil van Dijk","Liverpool FC"),("TD-30","Fernando Torres","Liverpool FC"),
("TD-31","Jérémy Doku","Manchester City"),("TD-32","Gianluigi Donnarumma","Manchester City"),("TD-33","Yaya Touré","Manchester City"),("TD-34","Benjamin Šeško","Manchester United"),("TD-35","Bryan Mbeumo","Manchester United"),
("TD-36","Robin van Persie","Manchester United"),("TD-37","Jacob Murphy","Newcastle United"),("TD-38","Sandro Tonali","Newcastle United"),("TD-39","Andy Cole","Newcastle United"),("TD-40","Nicolò Savona","Nottingham Forest"),
("TD-41","Ryan Yates","Nottingham Forest"),("TD-42","Enzo Le Fée","Sunderland"),("TD-43","Robin Roefs","Sunderland",R),("TD-44","João Palhinha","Tottenham Hotspur"),("TD-45","Lucas Bergvall","Tottenham Hotspur"),
("TD-46","Edgar Davids","Tottenham Hotspur"),("TD-47","Callum Wilson","West Ham United"),("TD-48","Mateus Fernandes","West Ham United"),("TD-49","Matt Doherty","Wolverhampton Wanderers"),("TD-50","Hwang Hee-Chan","Wolverhampton Wanderers"),
])
par(td, [("Green Refractor",99,"Value"),("Purple Refractor",75,"Value"),("Gold Refractor",50,"Value"),("Orange Refractor",25,"Value"),("Black Refractor",10,"Value"),("Red Refractor",5,"Value"),("SuperFractor",1,"Value")])

# ═══ MERLIN'S MYTHICAL ART (MM-, 11) [Hobby exclusive] ═══════════════════════
mm = ins("Merlin's Mythical Art", [
("MM-AN","Antoine Semenyo","Manchester City"),("MM-AS","Alan Shearer","Newcastle United"),("MM-BM","Bryan Mbeumo","Manchester United"),("MM-CD","Clint Dempsey","Fulham"),("MM-EE","Eberechi Eze","Arsenal"),
("MM-ES","Estêvão Willian","Chelsea",R),("MM-FW","Florian Wirtz","Liverpool FC"),("MM-GB","Gareth Bale","Tottenham Hotspur"),("MM-RN","Rio Ngumoha","Liverpool FC",R),("MM-RO","Rodri","Manchester City"),
("MM-TH","Thierry Henry","Arsenal"),
])
par(mm, [("Kaleidoscope",25,"Hobby"),("Shimmer",10,"Hobby"),("RayWave",5,"Hobby"),("SuperFractor",1,"Hobby")])

# ═══ RAINBOW FLICK (RB-, 30) [Value exclusive] ═══════════════════════════════
rb = ins("Rainbow Flick", [
("RB-1","Matheus Cunha","Manchester United"),("RB-2","Tyler Dibling","Everton"),("RB-3","Chemsdine Talbi","Sunderland"),("RB-4","Ryan Gravenberch","Liverpool FC"),("RB-5","Gabriel Martinelli","Arsenal"),
("RB-6","Savinho","Manchester City"),("RB-7","Brajan Gruda","Brighton & Hove Albion"),("RB-8","Jordan Henderson","Brentford"),("RB-9","Anthony Gordon","Newcastle United"),("RB-10","Kevin","Fulham"),
("RB-11","Yéremy Pino","Crystal Palace"),("RB-12","Wilfried Gnonto","Leeds United"),("RB-13","Omari Hutchinson","Nottingham Forest"),("RB-14","Wilson Odobert","Tottenham Hotspur"),("RB-15","Max Dowman","Arsenal",R),
("RB-16","Fer López","Wolverhampton Wanderers",R),("RB-17","David Ginola","Aston Villa"),("RB-18","Justin Kluivert","AFC Bournemouth"),("RB-19","Lesley Ugochukwu","Burnley FC"),("RB-20","João Pedro","Chelsea"),
("RB-21","Harry Kane","Tottenham Hotspur"),("RB-22","Philippe Coutinho","Liverpool FC"),("RB-23","Henrik Larsson","Manchester United"),("RB-24","Joe Cole","West Ham United"),("RB-25","Hernán Crespo","Chelsea"),
("RB-26","Sergio Agüero","Manchester City"),("RB-27","Leon Osman","Everton"),("RB-28","Daniel Sturridge","Liverpool FC"),("RB-29","Wayne Rooney","Manchester United"),("RB-30","Santi Cazorla","Arsenal"),
])
par(rb, [("Black Refractor",10,"Value"),("Red Refractor",5,"Value"),("SuperFractor",1,"Value")])

# ═══ MAGIC IN HIS BOOTS (MB-, 39 — no MB-14 per source) ══════════════════════
mhb = ins("Magic in His Boots", [
("MB-1","Martin Ødegaard","Arsenal"),("MB-2","Dennis Bergkamp","Arsenal"),("MB-3","Santi Cazorla","Arsenal"),("MB-4","Bukayo Saka","Arsenal"),("MB-5","Riccardo Calafiori","Arsenal"),
("MB-6","Morgan Rogers","Aston Villa"),("MB-7","Kaoru Mitoma","Brighton & Hove Albion"),("MB-8","Tom Watson","Brighton & Hove Albion",R),("MB-9","Cole Palmer","Chelsea"),("MB-10","Eden Hazard","Chelsea"),
("MB-11","Estêvão Willian","Chelsea",R),("MB-12","Jack Grealish","Everton"),("MB-13","Iliman Ndiaye","Everton"),("MB-15","Hugo Ekitike","Liverpool FC"),("MB-16","Juan Mata","Manchester United"),
("MB-17","Mohamed Salah","Liverpool FC"),("MB-18","Luis Suárez","Liverpool FC"),("MB-19","Rio Ngumoha","Liverpool FC",R),("MB-20","Phil Foden","Manchester City"),("MB-21","David Silva","Manchester City"),
("MB-22","Kevin De Bruyne","Manchester City"),("MB-23","Florian Wirtz","Liverpool FC"),("MB-24","Thiago Alcântara","Liverpool FC"),("MB-25","Matheus Cunha","Manchester United"),("MB-26","Nick Woltemade","Newcastle United"),
("MB-27","Bruno Guimarães","Newcastle United"),("MB-28","Chris Rigg","Sunderland",R),("MB-29","Gareth Bale","Tottenham Hotspur"),("MB-30","Mohammed Kudus","Tottenham Hotspur"),("MB-31","Rayan Cherki","Manchester City"),
("MB-32","Adam Wharton","Crystal Palace"),("MB-33","Joe Cole","Chelsea"),("MB-34","David Ginola","Tottenham Hotspur"),("MB-35","Zlatan Ibrahimović","Manchester United"),("MB-36","Gianfranco Zola","Chelsea"),
("MB-37","Riyad Mahrez","Manchester City"),("MB-38","Mikkel Damsgaard","Brentford"),("MB-39","Dimitar Berbatov","Fulham"),("MB-40","Harry Kane","Tottenham Hotspur"),
])
par(mhb, [("Red Refractor",5,None),("SuperFractor",1,None)])

# ═══ THE SHINY (TS-, 20) ═════════════════════════════════════════════════════
tsh = ins("The Shiny", [
("TS-1","Junior Kroupi","AFC Bournemouth"),("TS-2","Declan Rice","Arsenal"),("TS-3","Stiliyan Petrov","Aston Villa"),("TS-4","Dango Ouattara","Brentford"),("TS-5","Kaoru Mitoma","Brighton & Hove Albion"),
("TS-6","Jimmy Floyd Hasselbaink","Leeds United"),("TS-7","Estêvão Willian","Chelsea",R),("TS-8","Wilfried Zaha","Crystal Palace"),("TS-9","Yakubu","Everton"),("TS-10","Steed Malbranque","Fulham"),
("TS-11","Kalvin Phillips","Leeds United"),("TS-12","Thiago Alcântara","Liverpool FC"),("TS-13","David Silva","Manchester City"),("TS-14","Gianfranco Zola","Chelsea"),("TS-15","Alan Shearer","Newcastle United"),
("TS-16","Stuart Pearce","Nottingham Forest"),("TS-17","Chris Rigg","Sunderland",R),("TS-18","Heung-Min Son","Tottenham Hotspur"),("TS-19","El Hadji Malick Diouf","West Ham United",R),("TS-20","Kevin Doyle","Wolverhampton Wanderers"),
])
par(tsh, [("Gold Speckle",1,None)])

# ═══ RENAISSANCE (R-, 20) ════════════════════════════════════════════════════
ren = ins("Renaissance", [
("R-1","Ian Wright","Arsenal"),("R-2","Max Dowman","Arsenal",R),("R-3","Veljko Milosavljević","AFC Bournemouth",R),("R-4","Igor Thiago","Brentford"),("R-5","Kaoru Mitoma","Brighton & Hove Albion"),
("R-6","Moisés Caicedo","Chelsea"),("R-7","Adam Wharton","Crystal Palace"),("R-8","Jack Grealish","Everton"),("R-9","Louis Saha","Fulham"),("R-10","Sandro Tonali","Newcastle United"),
("R-11","Rio Ngumoha","Liverpool FC",R),("R-12","Hugo Ekitike","Liverpool FC"),("R-13","Tijjani Reijnders","Manchester City"),("R-14","Erling Haaland","Manchester City"),("R-15","Nolberto Solano","Newcastle United"),
("R-16","Roy Keane","Nottingham Forest"),("R-17","Granit Xhaka","Sunderland"),("R-18","Luka Modrić","Tottenham Hotspur"),("R-19","Joe Cole","West Ham United"),("R-20","Michael Carrick","Manchester United"),
])
par(ren, [("Red Refractor",5,None),("SuperFractor",1,None)])

# ═══ MERLIN'S MAGNUM OPUS (MG-, 20) ══════════════════════════════════════════
mg = ins("Merlin's Magnum Opus", [
("MG-1","Mohamed Salah","Liverpool FC"),("MG-2","Luis Suárez","Liverpool FC"),("MG-3","Bukayo Saka","Arsenal"),("MG-4","Max Dowman","Arsenal",R),("MG-5","Nick Woltemade","Newcastle United"),
("MG-6","Didier Drogba","Chelsea"),("MG-7","Eden Hazard","Chelsea"),("MG-8","Estêvão Willian","Chelsea",R),("MG-9","Rio Ngumoha","Liverpool FC",R),("MG-10","Carlos Tevez","West Ham United"),
("MG-11","Paul Scholes","Manchester United"),("MG-12","Bruno Fernandes","Manchester United"),("MG-13","Clint Dempsey","Fulham"),("MG-14","Thierry Henry","Arsenal"),("MG-15","Alan Shearer","Newcastle United"),
("MG-16","Steven Gerrard","Liverpool FC"),("MG-17","Frank Lampard","Chelsea"),("MG-18","Kevin De Bruyne","Manchester City"),("MG-19","Heung-Min Son","Tottenham Hotspur"),("MG-20","Martín Zubimendi","Arsenal"),
])
par(mg, [("SuperFractor",1,None)])

# ═══ MASK OFF (MO-, 1) ═══════════════════════════════════════════════════════
mo = ins("Mask Off", [("MO-1","Viktor Gyökeres","Arsenal")])
par(mo, [("Red & White Refractor",14,None),("Black Refractor",10,None),("Red Refractor",5,None),("SuperFractor",1,"Hobby")])

# ═══ AUTOGRAPH VARIATIONS (MV-, 80) [auto] ═══════════════════════════════════
mv = ins("Autograph Variations", [
("MV-AE","André","Wolverhampton Wanderers"),("MV-AG","Alejandro Garnacho","Chelsea"),("MV-AI","Alexander Isak","Liverpool FC"),("MV-AS","Antoine Semenyo","Manchester City"),("MV-AX","Alex Scott","AFC Bournemouth"),
("MV-BG","Bruno Guimarães","Newcastle United"),("MV-BM","Bryan Mbeumo","Manchester United"),("MV-BS","Benjamin Šeško","Manchester United"),("MV-BU","Bukayo Saka","Arsenal"),("MV-BW","Jarrod Bowen","West Ham United"),
("MV-BY","Conor Bradley","Liverpool FC"),("MV-CG","Cody Gakpo","Liverpool FC"),("MV-CM","Casemiro","Manchester United"),("MV-CO","Moisés Caicedo","Chelsea"),("MV-CP","Cole Palmer","Chelsea"),
("MV-CR","Chris Rigg","Sunderland",R),("MV-CT","Chemsdine Talbi","Sunderland"),("MV-CU","Matheus Cunha","Manchester United"),("MV-DJ","Daniel James","Leeds United"),("MV-DL","Matthijs De Ligt","Manchester United"),
("MV-DN","Kevin Danso","Tottenham Hotspur"),("MV-DR","Declan Rice","Arsenal"),("MV-DS","Dominic Solanke","Tottenham Hotspur"),("MV-DW","Max Dowman","Arsenal",R),("MV-EH","Erling Haaland","Manchester City"),
("MV-EJ","Junior Kroupi","AFC Bournemouth"),("MV-EN","Evanilson","AFC Bournemouth"),("MV-EO","Estêvão Willian","Chelsea",R),("MV-ESR","Emile Smith Rowe","Fulham"),("MV-EZE","Eberechi Eze","Arsenal"),
("MV-FC","Federico Chiesa","Liverpool FC"),("MV-FW","Florian Wirtz","Liverpool FC"),("MV-GR","Conor Gallagher","Tottenham Hotspur"),("MV-GX","Granit Xhaka","Sunderland"),("MV-GY","Archie Gray","Tottenham Hotspur"),
("MV-IN","Iliman Ndiaye","Everton"),("MV-IV","Amir Ibragimov","Manchester United",R),("MV-JD","Jérémy Doku","Manchester City"),("MV-JG","Jack Grealish","Everton"),("MV-JH","Jordan Henderson","Brentford"),
("MV-JY","Jayden Bogle","Leeds United"),("MV-KD","Mohammed Kudus","Tottenham Hotspur"),("MV-KDH","Kiernan Dewsbury-Hall","Everton"),("MV-KM","Konstantinos Mavropanos","West Ham United"),("MV-KS","Kevin Schade","Brentford"),
("MV-KT","Kieran Trippier","Newcastle United"),("MV-KW","Kyle Walker","Burnley FC"),("MV-LD","Lewis Dunk","Brighton & Hove Albion"),("MV-LN","Lukas Nmecha","Leeds United"),("MV-LY","Leny Yoro","Manchester United"),
("MV-MC","Matty Cash","Aston Villa"),("MV-MD","El Hadji Malick Diouf","West Ham United",R),("MV-MK","Divine Mukasa","Manchester City",R),("MV-MM","Mikel Merino","Arsenal"),("MV-MO","Mohamed Salah","Liverpool FC"),
("MV-MP","Jacob Murphy","Newcastle United"),("MV-MT","Malick Thiaw","Newcastle United"),("MV-MØ","Martin Ødegaard","Arsenal"),("MV-NC","Nathan Collins","Brentford"),("MV-OW","Ollie Watkins","Aston Villa"),
("MV-PA","João Palhinha","Tottenham Hotspur"),("MV-PD","Jordan Pickford","Everton"),("MV-PF","Phil Foden","Manchester City"),("MV-RD","Rúben Dias","Manchester City"),("MV-RI","Rodri","Manchester City"),
("MV-RJ","Reece James","Chelsea"),("MV-RN","Rio Ngumoha","Liverpool FC",R),("MV-RS","Ryan Sessegnon","Fulham"),("MV-SB","Sven Botman","Newcastle United"),("MV-SL","Shea Lacey","Manchester United",R),
("MV-ST","Sandro Tonali","Newcastle United"),("MV-TD","Tyler Dibling","Everton"),("MV-TR","Tijjani Reijnders","Manchester City"),("MV-TW","Tom Watson","Brighton & Hove Albion",R),("MV-VM","Vitalii Mykolenko","Everton"),
("MV-VVD","Virgil van Dijk","Liverpool FC"),("MV-WT","Nick Woltemade","Newcastle United"),("MV-YA","Yasin Ayari","Brighton & Hove Albion",R),("MV-YY","Yehor Yarmolyuk","Brentford"),("MV-ZA","Zach Abbott","Nottingham Forest",R),
], is_auto=True)
par(mv, [("Blue Refractor",150,None),("Green Refractor",99,None),("Purple Refractor",75,None),("Gold Refractor",50,None),("Orange Refractor",25,None),("Black Refractor",10,None),("Red Refractor",5,None),("SuperFractor",1,None)])

# ═══ MYSTIC AFTERNOONS AUTOGRAPHS (MY-, 11) [auto] ═══════════════════════════
my = ins("Mystic Afternoons Autographs", [
("MY-AW","Adam Wharton","Crystal Palace"),("MY-EN","Evanilson","AFC Bournemouth"),("MY-EO","Estêvão Willian","Chelsea",R),("MY-ERL","Erling Haaland","Manchester City"),("MY-KS","Kevin Schade","Brentford"),
("MY-KW","Kyle Walker","Burnley FC"),("MY-MK","Mohammed Kudus","Tottenham Hotspur"),("MY-MØ","Martin Ødegaard","Arsenal"),("MY-OW","Ollie Watkins","Aston Villa"),("MY-RN","Rio Ngumoha","Liverpool FC",R),
("MY-YA","Yasin Ayari","Brighton & Hove Albion",R),
], is_auto=True)
par(my, COMMON_PARS)

# ═══ ENCHANTED PEN (EP-, 18) [auto] ══════════════════════════════════════════
ep = ins("Enchanted Pen", [
("EP-CP","Cole Palmer","Chelsea"),("EP-CT","Carlos Tevez","West Ham United"),("EP-DL","David Luiz","Chelsea"),("EP-DR","Declan Rice","Arsenal"),("EP-EA","Emmanuel Adebayor","Tottenham Hotspur"),
("EP-EH","Erling Haaland","Manchester City"),("EP-EO","Estêvão Willian","Chelsea",R),("EP-EZE","Eberechi Eze","Arsenal"),("EP-FC","Federico Chiesa","Liverpool FC"),("EP-GZ","Gianfranco Zola","Chelsea"),
("EP-JG","Jack Grealish","Everton"),("EP-KP","Junior Kroupi","AFC Bournemouth"),("EP-MM","Mikel Merino","Arsenal"),("EP-MT","Mason Mount","Manchester United"),("EP-RD","Rafael van der Vaart","Tottenham Hotspur"),
("EP-RM","Riyad Mahrez","Manchester City"),("EP-RN","Rio Ngumoha","Liverpool FC",R),("EP-TR","Tijjani Reijnders","Manchester City"),
], is_auto=True)
par(ep, COMMON_PARS)

# ═══ MERLIN'S MAGICAL INK (MI-, 25) [auto, base finish Kaleidoscope] ═════════
mi = ins("Merlin's Magical Ink", [
("MI-AS","Alan Shearer","Newcastle United"),("MI-BM","David Beckham","Manchester United"),("MI-CO","Moisés Caicedo","Chelsea"),("MI-DB","Dennis Bergkamp","Arsenal"),("MI-EH","Erling Haaland","Manchester City"),
("MI-FL","Frank Lampard","Chelsea"),("MI-GB","Gareth Bale","Tottenham Hotspur"),("MI-GZ","Gianfranco Zola","Chelsea"),("MI-HZ","Eden Hazard","Chelsea"),("MI-IW","Ian Wright","Arsenal"),
("MI-JC","Joe Cole","West Ham United"),("MI-JF","Jimmy Floyd Hasselbaink","Leeds United"),("MI-MD","Max Dowman","Arsenal",R),("MI-MK","Mohammed Kudus","Tottenham Hotspur"),("MI-MO","Mohamed Salah","Liverpool FC"),
("MI-PI","Paul Ince","Manchester United"),("MI-PS","Paul Scholes","Manchester United"),("MI-RN","Rio Ngumoha","Liverpool FC",R),("MI-SG","Steven Gerrard","Liverpool FC"),("MI-SL","Shea Lacey","Manchester United",R),
("MI-SON","Heung-Min Son","Tottenham Hotspur"),("MI-TH","Thierry Henry","Arsenal"),("MI-TW","Tom Watson","Brighton & Hove Albion",R),("MI-WR","Wayne Rooney","Manchester United"),("MI-ZI","Zlatan Ibrahimović","Manchester United"),
], is_auto=True)
par(mi, [("Black Kaleidoscope",10,None),("Red Kaleidoscope",5,None),("SuperFractor",1,None)])

# ═══ SPELLBINDING TRIOS (ST-, 6 multi-subject) [auto] ════════════════════════
st = ais("Spellbinding Trios", True)
trios = [
("ST-ABY","Aston Villa",["Gareth Barry","Gabriel Agbonlahor","Ashley Young"]),
("ST-DSS","Manchester City",["Jérémy Doku","Savinho","Antoine Semenyo"]),
("ST-EMØ","Arsenal",["Martin Ødegaard","Eberechi Eze","Mikel Merino"]),
("ST-PSH","Liverpool FC",["Philippe Coutinho","Jordan Henderson","Daniel Sturridge"]),
("ST-SCS","Manchester United",["Teddy Sheringham","Paul Scholes","Andy Cole"]),
("ST-SKS","AFC Bournemouth",["Alex Scott","Evanilson","Junior Kroupi"]),
]
for num, team, names in trios:
    p1 = goc(names[0])
    db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, ?)", (p1, st, num, team))
    aid = db.execute("SELECT last_insert_rowid()").fetchone()[0]
    for co in names[1:]:
        db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (aid, goc(co)))
print(f"  Spellbinding Trios: {len(trios)} cards (trios)")
par(st, [("Black Refractor",10,None),("Red Refractor",5,None),("SuperFractor",1,None)])

# ═══ MERLIN'S MATCH BALL SIGNATURES (MB- initials, 33) [auto-relic, Hobby] ═══
mbs = ins("Merlin's Match Ball Signatures", [
("MB-AR","Antonee Robinson","Fulham"),("MB-AS","Alex Scott","AFC Bournemouth"),("MB-BA","Brenden Aaronson","Leeds United"),("MB-BB","Bradley Burrowes","Aston Villa",R),("MB-BF","Bruno Fernandes","Manchester United"),
("MB-BG","Bruno Guimarães","Newcastle United"),("MB-BM","Bryan Mbeumo","Manchester United"),("MB-BS","Benjamin Šeško","Manchester United"),("MB-CR","Cristian Romero","Tottenham Hotspur"),("MB-DM","Divine Mukasa","Manchester City",R),
("MB-DW","Danny Welbeck","Brighton & Hove Albion"),("MB-EH","Erling Haaland","Manchester City"),("MB-EM","Emiliano Martínez","Aston Villa"),("MB-EZE","Eberechi Eze","Arsenal"),("MB-GR","Georginio Rutter","Brighton & Hove Albion"),
("MB-JZ","Joshua Zirkzee","Manchester United"),("MB-KS","Kevin Schade","Brentford"),("MB-MC","Matheus Cunha","Manchester United"),("MB-MS","Mohamed Salah","Liverpool FC"),("MB-MT","Mathys Tel","Tottenham Hotspur"),
("MB-NM","Nikola Milenković","Nottingham Forest"),("MB-OW","Ollie Watkins","Aston Villa"),("MB-PF","Phil Foden","Manchester City"),("MB-PK","Jordan Pickford","Everton"),("MB-RG","Chris Rigg","Sunderland",R),
("MB-RIO","Rio Ngumoha","Liverpool FC",R),("MB-SE","Antoine Semenyo","Manchester City"),("MB-SL","Shea Lacey","Manchester United",R),("MB-SV","Savinho","Manchester City"),("MB-TI","Sandro Tonali","Newcastle United"),
("MB-TR","Tijjani Reijnders","Manchester City"),("MB-VVD","Virgil van Dijk","Liverpool FC"),("MB-WS","William Saliba","Arsenal"),
], is_auto=True)
par(mbs, [("Orange Refractor",25,"Hobby"),("Black Refractor",10,"Hobby"),("Red Refractor",5,"Hobby"),("SuperFractor",1,"Hobby")])

db.commit()

# ═══ VERIFICATION ════════════════════════════════════════════════════════════
print("\n" + "=" * 50)
total = 0
for name, cnt in db.execute("""
    SELECT is2.name, COUNT(pa.id) FROM insert_sets is2
    LEFT JOIN player_appearances pa ON pa.insert_set_id = is2.id
    WHERE is2.set_id = ? GROUP BY is2.id ORDER BY is2.id""", (SET_ID,)).fetchall():
    total += cnt
n_players = db.execute("SELECT COUNT(*) FROM players WHERE set_id = ?", (SET_ID,)).fetchone()[0]
n_subsets = db.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id = ?", (SET_ID,)).fetchone()[0]
n_pars = db.execute("SELECT COUNT(*) FROM parallels WHERE insert_set_id IN (SELECT id FROM insert_sets WHERE set_id = ?)", (SET_ID,)).fetchone()[0]
n_co = db.execute("SELECT COUNT(*) FROM appearance_co_players WHERE appearance_id IN (SELECT pa.id FROM player_appearances pa JOIN insert_sets i ON i.id = pa.insert_set_id WHERE i.set_id = ?)", (SET_ID,)).fetchone()[0]
print(f"Set ID: {SET_ID}")
print(f"Total subsets: {n_subsets} (expected 20)")
print(f"Total cards: {total} (expected 714)")
print(f"Total unique athletes: {n_players}")
print(f"Total parallels: {n_pars}")
print(f"Co-player join rows: {n_co} (expected 12, i.e. 6 trios x 2 co-players)")

# Pack odds key sanity check: every odds key's subset prefix must match an inserted subset name
subset_names = sorted([r[0] for r in db.execute("SELECT name FROM insert_sets WHERE set_id = ?", (SET_ID,)).fetchall()], key=len, reverse=True)
base_par_names = [r[0] for r in db.execute("SELECT name FROM parallels WHERE insert_set_id = ?", (base_id,)).fetchall()]
odds = json.loads(pack_odds)
bad = []
for fmt, keys in odds.items():
    for k in keys:
        if any(k == n or k.startswith(n + " ") for n in subset_names):
            continue
        if k in base_par_names:  # base parallel keys
            continue
        bad.append(f"{fmt}: {k}")
if bad:
    print("PACK ODDS KEY MISMATCHES:")
    for b in bad: print(f"  {b}")
else:
    print("Pack odds key sanity check: all keys match subset names or base parallels. OK")
print("Done!")
