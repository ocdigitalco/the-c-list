"""Seed 2026 Topps Disney Neon (update stub ID 59)."""
import sqlite3, json, os, re, unicodedata

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA foreign_keys=ON")
cur = conn.cursor()

SET_ID = 59

def slugify(t):
    s = t.lower()
    s = unicodedata.normalize("NFD", s)
    s = re.sub(r"[\u0300-\u036f]", "", s)
    s = re.sub(r"[^a-z0-9-]+", "-", s).strip("-")
    s = re.sub(r"-+", "-", s)
    return s

# Box config
bc = {"hobby":{"cards_per_pack":5,"packs_per_box":20,"boxes_per_case":10,"numbered_parallels_or_inserts_per_box":2,"neon_lights_petg_inserts_per_box":1,"chrome_neon_etch_inserts_per_box":3},"value":{"cards_per_pack":5,"packs_per_box":7,"boxes_per_case":None,"diamante_parallels_per_box":2,"notes":"Boxes per case TBA"},"mega":{"cards_per_pack":5,"packs_per_box":10,"boxes_per_case":20,"snow_cap_parallels_per_box":3,"neon_lights_petg_inserts_per_box":1,"muppets_puzzle_inserts_per_box":3}}

# Pack odds (abbreviated - full JSON in update)
po_hobby = {"Rainbow Foilboard":"1:2","Green":"1:44","Pink/Green/Blue":"1:58","Purple/Yellow/Blue":"1:87","Gold":"1:172","Orange Diamante":"1:343","Pink Diamante":"1:572","Black Diamante":"1:858","Red Diamante":"1:1,715","Foilfractor":"1:8,547","Topps Neon Autographs":"1:1,092","Topps Neon Autographs Gold":"1:1,440","Topps Neon Autographs Red":"1:14,346","Topps Neon Autographs Pink":"1:70,885","Phineas and Ferb Auto Variation Gold Refractor":"1:6,180","Phineas and Ferb Auto Variation Orange Refractor":"1:12,297","Phineas and Ferb Auto Variation Black Refractor":"1:30,899","Phineas and Ferb Auto Variation Red Refractor":"1:60,252","A Goofy Movie 30th Anniversary Auto Variation Gold Refractor":"1:7,216","A Goofy Movie 30th Anniversary Auto Variation Orange Refractor":"1:14,346","A Goofy Movie 30th Anniversary Auto Variation Black Refractor":"1:36,517","A Goofy Movie 30th Anniversary Auto Variation Red Refractor":"1:70,885","Mickey Shorts Short Prints Auto Variation Gold Refractor":"1:6,180","Mickey Shorts Short Prints Auto Variation Orange Refractor":"1:12,297","Mickey Shorts Short Prints Auto Variation Black Refractor":"1:30,899","Mickey Shorts Short Prints Auto Variation Red Refractor":"1:60,252","Mickey Shorts Dual Auto Variation Black Wave":"1:21,910","Mickey Shorts Dual Auto Variation Red Wave":"1:43,038","Chrome Neon Etch Autographs":"1:301","Chrome Neon Etch Autographs Gold Shimmer":"1:786","Chrome Neon Etch Autographs Orange Wave":"1:1,516","Chrome Neon Etch Autographs Black Speckle":"1:3,545","Chrome Neon Etch Autographs Red Lava":"1:7,089","Chrome Neon Etch Autographs Superfractor":"1:35,443","Mickey Mouse Comic Cuts":"1:17,552","Family First":"1:2","Family First Gold":"1:980","Family First Orange":"1:1,960","Family First Black":"1:4,899","Family First Red":"1:9,798","Family First Foilfractor":"1:48,202","Family First Rivals Variations":"1:495","Family First Rivals Gold Refractor":"1:980","Family First Rivals Orange Refractor":"1:1,960","Family First Rivals Black Refractor":"1:4,899","Family First Rivals Red Refractor":"1:9,798","Family First Rivals Superfractor":"1:48,202","Phineas and Ferb":"1:5","Phineas and Ferb Gold":"1:1,715","Phineas and Ferb Orange":"1:3,434","Phineas and Ferb Black":"1:8,547","Phineas and Ferb Red":"1:17,215","Phineas and Ferb Foilfractor":"1:86,075","Manga Madness":"1:7","Manga Madness Gold":"1:2,856","Manga Madness Orange":"1:5,739","Manga Madness Black":"1:14,346","Manga Madness Red":"1:28,692","Manga Madness Foilfractor":"1:133,894","A Goofy Movie":"1:7","A Goofy Movie Gold":"1:2,856","A Goofy Movie Orange":"1:5,739","A Goofy Movie Black":"1:14,346","A Goofy Movie Red":"1:28,692","A Goofy Movie Foilfractor":"1:133,894","Epic Mickey":"1:7","Epic Mickey Gold Refractor":"1:1,481","Epic Mickey Orange Refractor":"1:2,961","Epic Mickey Black Refractor":"1:7,393","Epic Mickey Red Refractor":"1:14,878","Epic Mickey Superfractor":"1:70,885","Neon Lights PETG":"1:20","Mickey Shorts Short Prints":"1:240","Mickey Shorts Short Prints Gold Wave":"1:1,481","Mickey Shorts Short Prints Orange Wave":"1:2,961","Mickey Shorts Short Prints Black Wave":"1:7,393","Mickey Shorts Short Prints Red Wave":"1:14,878","Magic Carpet Ride":"1:1,200","Neon Villains":"1:2,470","Neon Villains Gold Lava":"1:4,899","Neon Villains Orange Lava":"1:9,798","Neon Villains Black Lava":"1:24,593","Neon Villains Red Lava":"1:48,202","Neon Villains Superfractor":"1:241,008","Chrome Neon Etch":"1:7","Chrome Neon Etch Refractor":"1:86","Chrome Neon Etch Green Lazer":"1:172","Chrome Neon Etch Gold Shimmer":"1:253","Chrome Neon Etch Orange Wave":"1:682","Chrome Neon Etch Black Speckle":"1:1,262","Chrome Neon Etch Red Lava":"1:2,527","Chrome Neon Etch Superfractor":"1:17,215","Scrooge's Money Bin":"1:302","Scrooge's Money Bin Gold":"1:62,434","Scrooge's Money Bin Rose Gold":"1:133,894"}

po_value = {"Rainbow Foilboard":"1:3","Diamante":"1:3","Green":"1:330","Pink/Green/Blue":"1:436","Purple/Yellow/Blue":"1:660","Gold":"1:1,306","Orange Diamante":"1:2,611","Pink Diamante":"1:4,360","Black Diamante":"1:6,520","Red Diamante":"1:13,040","Foilfractor":"1:65,393","Topps Neon Autographs":"1:3,718","Topps Neon Autographs Gold":"1:4,894","Topps Neon Autographs Red":"1:49,609","Topps Neon Autographs Pink":"1:287,728","Phineas and Ferb Auto Variation Gold Refractor":"1:21,157","Phineas and Ferb Auto Variation Orange Refractor":"1:43,596","Phineas and Ferb Auto Variation Black Refractor":"1:110,665","Phineas and Ferb Auto Variation Red Refractor":"1:205,520","A Goofy Movie 30th Anniversary Auto Variation Gold Refractor":"1:24,805","A Goofy Movie 30th Anniversary Auto Variation Orange Refractor":"1:49,609","A Goofy Movie 30th Anniversary Auto Variation Black Refractor":"1:130,786","A Goofy Movie 30th Anniversary Auto Variation Red Refractor":"1:287,728","Mickey Shorts Short Prints Auto Variation Gold Refractor":"1:21,157","Mickey Shorts Short Prints Auto Variation Orange Refractor":"1:43,596","Mickey Shorts Short Prints Auto Variation Black Refractor":"1:110,665","Mickey Shorts Short Prints Auto Variation Red Refractor":"1:205,520","Mickey Shorts Dual Auto Variation Black Wave":"1:75,718","Mickey Shorts Dual Auto Variation Red Wave":"1:143,864","Chrome Neon Etch Autographs":"1:1,021","Chrome Neon Etch Autographs Gold Shimmer":"1:2,675","Chrome Neon Etch Autographs Orange Wave":"1:5,157","Chrome Neon Etch Autographs Black Speckle":"1:12,090","Chrome Neon Etch Autographs Red Lava":"1:24,384","Chrome Neon Etch Autographs Superfractor":"1:130,786","Family First":"1:3","Family First Gold":"1:7,445","Family First Orange":"1:14,889","Family First Black":"1:37,859","Family First Red":"1:73,889","Family First Foilfractor":"1:399,000","Family First Rivals Variations":"1:3,776","Family First Rivals Gold Refractor":"1:7,445","Family First Rivals Orange Refractor":"1:14,889","Family First Rivals Black Refractor":"1:37,859","Family First Rivals Red Refractor":"1:73,889","Family First Rivals Superfractor":"1:399,000","Phineas and Ferb":"1:5","Phineas and Ferb Gold":"1:13,079","Phineas and Ferb Orange":"1:26,158","Phineas and Ferb Black":"1:65,393","Phineas and Ferb Red":"1:130,786","Phineas and Ferb Foilfractor":"1:719,320","Manga Madness":"1:7","Manga Madness Gold":"1:21,685","Manga Madness Orange":"1:43,370","Manga Madness Black":"1:110,834","Manga Madness Red":"1:221,667","Manga Madness Foilfractor":"1:997,501","A Goofy Movie":"1:9","A Goofy Movie Gold":"1:21,685","A Goofy Movie Orange":"1:43,370","A Goofy Movie Black":"1:110,834","A Goofy Movie Red":"1:221,667","A Goofy Movie Foilfractor":"1:997,501","Epic Mickey Gold Refractor":"1:11,510","Epic Mickey Orange Refractor":"1:23,204","Epic Mickey Black Refractor":"1:57,546","Epic Mickey Red Refractor":"1:119,887","Epic Mickey Superfractor":"1:498,751","Neon Lights PETG":"1:140","Mickey Shorts Short Prints":"1:1,401","Mickey Shorts Short Prints Gold Wave":"1:11,510","Mickey Shorts Short Prints Orange Wave":"1:23,204","Mickey Shorts Short Prints Black Wave":"1:57,546","Mickey Shorts Short Prints Red Wave":"1:119,887","Magic Carpet Ride":"1:8,400","Neon Villains":"1:18,821","Neon Villains Gold Lava":"1:37,859","Neon Villains Orange Lava":"1:73,889","Neon Villains Black Lava":"1:181,364","Neon Villains Red Lava":"1:399,000","Neon Villains Superfractor":"1:1,995,001","Chrome Neon Etch Refractor":"1:657","Chrome Neon Etch Green Lazer":"1:1,320","Chrome Neon Etch Orange Wave":"1:5,232","Chrome Neon Etch Superfractor":"1:133,000"}

po_mega = {"Rainbow Foilboard":"1:2","Snow Caps":"1:3","Green":"1:235","Pink/Green/Blue":"1:310","Purple/Yellow/Blue":"1:469","Gold":"1:927","Orange Diamante":"1:1,857","Pink Diamante":"1:3,088","Black Diamante":"1:4,663","Red Diamante":"1:9,178","Foilfractor":"1:46,161","Topps Neon Autographs":"1:3,713","Topps Neon Autographs Gold":"1:4,895","Topps Neon Autographs Red":"1:50,831","Topps Neon Autographs Pink":"1:330,400","Phineas and Ferb Auto Variation Gold Refractor":"1:21,317","Phineas and Ferb Auto Variation Orange Refractor":"1:44,054","Phineas and Ferb Auto Variation Black Refractor":"1:110,134","Phineas and Ferb Auto Variation Red Refractor":"1:330,400","A Goofy Movie 30th Anniversary Auto Variation Gold Refractor":"1:24,475","A Goofy Movie 30th Anniversary Auto Variation Orange Refractor":"1:50,831","A Goofy Movie 30th Anniversary Auto Variation Black Refractor":"1:132,160","A Goofy Movie 30th Anniversary Auto Variation Red Refractor":"1:330,400","Mickey Shorts Short Prints Auto Variation Gold Refractor":"1:21,317","Mickey Shorts Short Prints Auto Variation Orange Refractor":"1:44,054","Mickey Shorts Short Prints Auto Variation Black Refractor":"1:110,134","Mickey Shorts Short Prints Auto Variation Red Refractor":"1:330,400","Mickey Shorts Dual Auto Variation Black Wave":"1:73,423","Mickey Shorts Dual Auto Variation Red Wave":"1:165,200","Chrome Neon Etch Autographs":"1:1,022","Chrome Neon Etch Autographs Gold Shimmer":"1:2,676","Chrome Neon Etch Autographs Orange Wave":"1:5,163","Chrome Neon Etch Autographs Black Speckle":"1:12,015","Chrome Neon Etch Autographs Red Lava":"1:24,475","Chrome Neon Etch Autographs Superfractor":"1:132,160","Family First":"1:3","Family First Gold":"1:5,287","Family First Orange":"1:10,612","Family First Black":"1:26,378","Family First Red":"1:54,306","Family First Foilfractor":"1:230,801","Family First Rivals Variations":"1:2,676","Family First Rivals Gold Refractor":"1:5,287","Family First Rivals Orange Refractor":"1:10,612","Family First Rivals Black Refractor":"1:26,378","Family First Rivals Red Refractor":"1:54,306","Family First Rivals Superfractor":"1:230,801","Phineas and Ferb":"1:5","Phineas and Ferb Gold":"1:9,178","Phineas and Ferb Orange":"1:18,356","Phineas and Ferb Black":"1:47,200","Phineas and Ferb Red":"1:94,400","Phineas and Ferb Foilfractor":"1:461,601","Manga Madness":"1:9","Manga Madness Gold":"1:15,368","Manga Madness Orange":"1:30,774","Manga Madness Black":"1:76,934","Manga Madness Red":"1:153,867","Manga Madness Foilfractor":"1:923,201","A Goofy Movie":"1:7","A Goofy Movie Gold":"1:15,368","A Goofy Movie Orange":"1:30,774","A Goofy Movie Black":"1:76,934","A Goofy Movie Red":"1:153,867","A Goofy Movie Foilfractor":"1:923,201","Epic Mickey Gold Refractor":"1:8,260","Epic Mickey Orange Refractor":"1:16,520","Epic Mickey Black Refractor":"1:41,300","Epic Mickey Red Refractor":"1:82,600","Epic Mickey Superfractor":"1:330,400","The Muppets Puzzle":"1:3","Neon Lights PETG":"1:10","Mickey Shorts Short Prints":"1:200","Mickey Shorts Short Prints Gold Wave":"1:8,260","Mickey Shorts Short Prints Orange Wave":"1:16,520","Mickey Shorts Short Prints Black Wave":"1:41,300","Mickey Shorts Short Prints Red Wave":"1:82,600","Magic Carpet Ride":"1:2,000","Neon Villains":"1:13,380","Neon Villains Gold Lava":"1:26,378","Neon Villains Orange Lava":"1:54,306","Neon Villains Black Lava":"1:131,886","Neon Villains Red Lava":"1:230,801","Neon Villains Superfractor":"1:923,201","Chrome Neon Etch Refractor":"1:467","Chrome Neon Etch Green Lazer":"1:936","Chrome Neon Etch Orange Wave":"1:3,723","Chrome Neon Etch Superfractor":"1:92,321","Scrooge's Money Bin":"1:370","Scrooge's Money Bin Gold":"1:31,835","Scrooge's Money Bin Rose Gold":"1:61,547"}

pack_odds = {"hobby": po_hobby, "value": po_value, "mega": po_mega}

slug = slugify("2026 Topps Disney Neon")
cur.execute("UPDATE sets SET name=?, sport=?, season=?, league=?, tier=?, release_date=?, box_config=?, pack_odds=?, slug=? WHERE id=?",
    ("2026 Topps Disney Neon", "Entertainment", "2026", "Disney", "Standard", "2026-04-10", json.dumps(bc), json.dumps(pack_odds), slug, SET_ID))
print(f"Updated set {SET_ID}")

# Helpers
def gop(name):
    cur.execute("SELECT id FROM players WHERE set_id=? AND name=?", (SET_ID, name))
    r = cur.fetchone()
    if r: return r[0]
    s = slugify(name)
    cur.execute("INSERT INTO players (set_id,name,slug,unique_cards,total_print_run,one_of_ones,insert_set_count) VALUES (?,?,?,0,0,0,0)", (SET_ID, name, s))
    return cur.lastrowid

def cis(name):
    cur.execute("INSERT INTO insert_sets (set_id,name) VALUES (?,?)", (SET_ID, name))
    return cur.lastrowid

def cp(is_id, name, pr):
    cur.execute("INSERT INTO parallels (insert_set_id,name,print_run) VALUES (?,?,?)", (is_id, name, pr))

def ca(pid, is_id, cn, team=None):
    cur.execute("INSERT INTO player_appearances (player_id,insert_set_id,card_number,is_rookie,team) VALUES (?,?,?,0,?)", (pid, is_id, cn, team))

BASE_PARS = [("Rainbow Foilboard",None),("Snow Caps",None),("Diamante",None),("Green",None),("Pink/Green/Blue",None),("Purple/Yellow/Blue",None),("Gold",None),("Orange Diamante",None),("Pink Diamante",None),("Black Diamante",None),("Red Diamante",None),("Foilfractor",1)]

is_id = cis("Base")
for pn, pr in BASE_PARS: cp(is_id, pn, pr)

cards = [
(1,"Phineas","Phineas and Ferb"),(2,"Ferb","Phineas and Ferb"),(3,"Isabella","Phineas and Ferb"),(4,"Dr. Doofenshmirtz","Phineas and Ferb"),(5,"Perry the Platypus","Phineas and Ferb"),(6,"Candace","Phineas and Ferb"),(7,"Tigger","Winnie the Pooh"),(8,"Peter Pan","Peter Pan"),(9,"Captain Hook","Peter Pan"),(10,"Mr. Smee","Peter Pan"),
(11,"The Beast","Beauty and the Beast"),(12,"Gaston","Beauty and the Beast"),(13,"Lumi\u00e8re","Beauty and the Beast"),(14,"Stitch","Lilo & Stitch"),(15,"Lilo","Lilo & Stitch"),(16,"Jumba","Lilo & Stitch"),(17,"Pleakley","Lilo & Stitch"),(18,"Captain Gantu","Lilo & Stitch"),(19,"WALL-E","WALL-E"),(20,"Eve","WALL-E"),
(21,"Moana","Moana 2"),(22,"Moni","Moana 2"),(23,"Loto","Moana 2"),(24,"Kele","Moana 2"),(25,"Matangi","Moana 2"),(26,"Maui","Moana 2"),(27,"The Kakamora","Moana 2"),(28,"Aladdin","Aladdin"),(29,"Genie","Aladdin"),(30,"Jafar","Aladdin"),
(31,"Buzz Lightyear","Toy Story"),(32,"Woody","Toy Story"),(33,"Jessie","Toy Story"),(34,"Zurg","Toy Story 2"),(35,"Duke Caboom","Toy Story 4"),(36,"Ducky & Bunny","Toy Story 4"),(37,"Kuzco","The Emperor's New Groove"),(38,"Yzma","The Emperor's New Groove"),(39,"Kronk","The Emperor's New Groove"),(40,"Mufasa","The Lion King"),
(41,"Simba","The Lion King"),(42,"Nala","The Lion King"),(43,"Scar","The Lion King"),(44,"Joe Gardner","Soul"),(45,"22","Soul"),(46,"Moonwind","Soul"),(47,"Terry","Soul"),(48,"Dorothea Williams","Soul"),(49,"Dez","Soul"),(50,"Bruni","Frozen 2"),
(51,"Mr. Incredible","The Incredibles"),(52,"Mrs. Incredible","The Incredibles"),(53,"Syndrome","The Incredibles"),(54,"Dash Parr","The Incredibles"),(55,"Violet Parr","The Incredibles"),(56,"Frozone","The Incredibles"),(57,"Mirage","The Incredibles"),(58,"The Underminer","The Incredibles"),(59,"Screenslaver","Incredibles 2"),(60,"Flynn Rider","Tangled"),
(61,"Nick Wilde","Zootopia"),(62,"Judy Hopps","Zootopia"),(63,"Flash","Zootopia"),(64,"Gazelle","Zootopia"),(65,"Miguel","Coco"),(66,"H\u00e9ctor","Coco"),(67,"Ernesto de la Cruz","Coco"),(68,"Chicharr\u00f3n","Coco"),(69,"Pepita","Coco"),(70,"Alebrije Dante","Coco"),
(71,"Remy","Ratatouille"),(72,"Linguini","Ratatouille"),(73,"Anton Ego","Ratatouille"),(74,"Gusteau","Ratatouille"),(75,"Mulan","Mulan"),(76,"Mushu","Mulan"),(77,"Li Shang","Mulan"),(78,"Shan Yu","Mulan"),(79,"Nemo","Finding Nemo"),(80,"Marlin","Finding Nemo"),
(81,"Dory","Finding Nemo"),(82,"Crush & Squirt","Finding Nemo"),(83,"Bruce","Finding Nemo"),(84,"Gill","Finding Nemo"),(85,"Hank","Finding Dory"),(86,"Pinocchio","Pinocchio"),(87,"Jiminy Cricket","Pinocchio"),(88,"Cruz Ramirez","Cars 3"),(89,"Mater","Cars"),(90,"Chick Hicks","Cars"),
(91,"Jackson Storm","Cars 3"),(92,"Ramone","Cars"),(93,"The King","Cars"),(94,"Francesco Bernoulli","Cars 2"),(95,"Lightning McQueen","Cars"),(96,"Wingo","Cars"),(97,"Snot Rod","Cars"),(98,"Boost","Cars"),(99,"DJ","Cars"),(100,"Maleficent","Sleeping Beauty"),
(101,"Powerline","A Goofy Movie"),(102,"Goofy","A Goofy Movie"),(103,"Pete","A Goofy Movie"),(104,"P.J.","A Goofy Movie"),(105,"Max Goof","A Goofy Movie"),(106,"Roxanne","A Goofy Movie"),(107,"Ralph","Wreck-It Ralph"),(108,"Felix","Wreck-It Ralph"),(109,"Vanellope von Schweetz","Wreck-It Ralph"),(110,"King Candy","Wreck-It Ralph"),
(111,"Sergeant Calhoun","Wreck-It Ralph"),(112,"Sour Bill","Wreck-It Ralph"),(113,"Shank","Ralph Breaks the Internet"),(114,"Yesss","Ralph Breaks the Internet"),(115,"Chicken Little","Chicken Little"),(116,"Fish Out of Water","Chicken Little"),(117,"Kirby","Chicken Little"),(118,"Sulley","Monsters, Inc."),(119,"Mike Wazowski","Monsters, Inc."),(120,"Randall Boggs","Monsters, Inc."),
(121,"Art","Monsters University"),(122,"Squishy","Monsters University"),(123,"Darkwing Duck","Darkwing Duck"),(124,"Launchpad McQuack","Darkwing Duck"),(125,"Baymax","Big Hero 6"),(126,"Hiro Hamada","Big Hero 6"),(127,"Yokai","Big Hero 6"),(128,"Bolt","Bolt"),(129,"Carl Fredricksen","Up"),(130,"Russell","Up"),
(131,"Hercules","Hercules"),(132,"Hades","Hercules"),(133,"Megara","Hercules"),(134,"Goliath","Gargoyles"),(135,"Demona","Gargoyles"),(136,"Hudson","Gargoyles"),(137,"Brooklyn","Gargoyles"),(138,"Broadway","Gargoyles"),(139,"Lexington","Gargoyles"),(140,"Lewis","Meet the Robinsons"),
(141,"Wilbur Robinson","Meet the Robinsons"),(142,"Bowler Hat Guy & DOR-15","Meet the Robinsons"),(143,"Carl the Robot","Meet the Robinsons"),(144,"Tiny","Meet the Robinsons"),(145,"Merlin","The Sword in the Stone"),(146,"Elio Sol\u00eds","Elio"),(147,"Glordon","Elio"),(148,"Lord Grigon","Elio"),(149,"Jim Hawkins","Treasure Planet"),(150,"B.E.N.","Treasure Planet"),
(151,"Scrooge McDuck","Ducktales"),(152,"Huey, Dewey, Louie","Ducktales"),(153,"Chernabog","Fantasia"),(154,"Ian Lightfoot","Onward"),(155,"Barley Lightfoot","Onward"),(156,"Mal","Descendants"),(157,"Evie","Descendants"),(158,"Jay","Descendants"),(159,"Carlos","Descendants"),(160,"Uma","Descendants"),
(161,"Red","Descendants"),(162,"Elliott","Pete's Dragon"),(163,"Joy","Inside Out"),(164,"Fear","Inside Out"),(165,"Anger","Inside Out"),(166,"Sadness","Inside Out"),(167,"Disgust","Inside Out"),(168,"Bing Bong","Inside Out"),(169,"Anxiety","Inside Out 2"),(170,"Embarrassment","Inside Out 2"),
(171,"Ennui","Inside Out 2"),(172,"Bloofy & Pouchy","Inside Out 2"),(173,"Lance Slashblade","Inside Out 2"),(174,"Milo","Atlantis: The Lost Empire"),(175,"Kida","Atlantis: The Lost Empire"),(176,"Ursula","The Little Mermaid"),(177,"King Triton","The Little Mermaid"),(178,"Chef Louis","The Little Mermaid"),(179,"Flotsam and Jetsam","The Little Mermaid"),(180,"Sebastian","The Little Mermaid"),
(181,"Ember Lumen","Elemental"),(182,"Wade Ripple","Elemental"),(183,"Cruella de Vil","One Hundred and One Dalmatians"),(184,"Timothy Q. Mouse","Dumbo"),(185,"Dumbo","Dumbo"),(186,"Kermit","The Muppets"),(187,"Miss Piggy","The Muppets"),(188,"Pep\u00e9","The Muppets"),(189,"Rizzo","The Muppets"),(190,"Swedish Chef","The Muppets"),
(191,"Gonzo","The Muppets"),(192,"Fozzie Bear","The Muppets"),(193,"Dr. Bunsen Honeydew & Beaker","The Muppets"),(194,"Animal","The Muppets"),(195,"Sam Eagle","The Muppets"),(196,"Donald Duck","Mickey & Friends"),(197,"Daisy Duck","Mickey & Friends"),(198,"Pluto","Mickey & Friends"),(199,"Minnie Mouse","Mickey & Friends"),(200,"Mickey Mouse","Mickey & Friends"),
]

for cn, name, team in cards:
    ca(gop(name), is_id, str(cn), team)
print("  Base: 200 cards")

# Compute stats
print("\nComputing player stats...")
cur.execute("SELECT id FROM players WHERE set_id=?", (SET_ID,))
for (pid,) in cur.fetchall():
    cur.execute("SELECT pa.id, pa.insert_set_id FROM player_appearances pa WHERE pa.player_id=?", (pid,))
    apps = cur.fetchall()
    is_ids = set(a[1] for a in apps)
    uc, tpr, o1 = 0, 0, 0
    for _, isid in apps:
        uc += 1
        cur.execute("SELECT name, print_run FROM parallels WHERE insert_set_id=?", (isid,))
        for _, pr in cur.fetchall():
            uc += 1
            if pr is not None:
                tpr += pr
                if pr == 1: o1 += 1
    cur.execute("UPDATE players SET unique_cards=?, total_print_run=?, one_of_ones=?, insert_set_count=? WHERE id=?", (uc, tpr, o1, len(is_ids), pid))

conn.commit()

cur.execute("SELECT COUNT(*) FROM players WHERE set_id=?", (SET_ID,)); tp=cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id=?", (SET_ID,)); ti=cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM player_appearances pa JOIN players p ON p.id=pa.player_id WHERE p.set_id=?", (SET_ID,)); ta=cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM parallels par JOIN insert_sets i ON i.id=par.insert_set_id WHERE i.set_id=?", (SET_ID,)); tpar=cur.fetchone()[0]

total_odds = sum(len(v) for v in pack_odds.values())
print(f"\n{'='*50}")
print(f"Set ID:            {SET_ID}")
print(f"Players:           {tp}")
print(f"Insert Sets:       {ti}")
print(f"Appearances:       {ta}")
print(f"Parallel types:    {tpar}")
print(f"Pack odds entries: {total_odds}")
print(f"{'='*50}")
conn.close()
print("\nDone!")
