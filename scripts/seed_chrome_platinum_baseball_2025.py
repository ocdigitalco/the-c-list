"""
Seed: 2025 Topps Chrome Platinum Baseball — Full checklist.
500 base, 40 image variations, 80 city variations, 4 inserts (70 cards),
10 employee SSPs, 178 Chrome Platinum Autos, 92 City Variations Autos.
Parallels attached, pack odds deferred.
Usage: python3 scripts/seed_chrome_platinum_baseball_2025.py
"""
import sqlite3, os, json, re, unicodedata

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
db = sqlite3.connect(DB_PATH)
db.execute("PRAGMA journal_mode=WAL")
db.execute("PRAGMA foreign_keys=ON")

box_config = json.dumps({
    "hobby": {"cards_per_pack": 4, "packs_per_box": 20, "boxes_per_case": 12,
              "notes": "Per box: 1 autograph + 4 inserts"},
    "value": {"cards_per_pack": 4, "packs_per_box": 8, "boxes_per_case": 40,
              "notes": "Per box: 3 prism parallels + 1 insert"},
})

db.execute("""
    INSERT INTO sets (name, sport, season, tier, slug, is_visible,
                      sample_image_url, release_date, box_config, created_at)
    VALUES ('2025 Topps Chrome Platinum Baseball', 'Baseball', '2025', 'Chrome',
            '2025-topps-chrome-platinum-baseball', 1,
            '/sets/2025-topps-chrome-platinum-baseball.jpg', '2026-06-05', ?, '2026-05-29T18:00:00Z')
""", (box_config,))
SET_ID = db.execute("SELECT last_insert_rowid()").fetchone()[0]
print(f"Created set ID: {SET_ID}")

H = "Hobby"
R_EX = "Retail"

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
    if not _sc:
        for r in db.execute("SELECT slug FROM players WHERE set_id = ? AND slug IS NOT NULL", (SET_ID,)).fetchall():
            _sc[r[0]] = True
    c = slug; i = 2
    while c in _sc: c = f"{slug}-{i}"; i += 1
    _sc[c] = True
    db.execute("INSERT INTO players (set_id, name, slug, unique_cards, total_print_run, one_of_ones, insert_set_count, subject_role) VALUES (?, ?, ?, 0, 0, 0, 0, ?)",
               (SET_ID, name, c, role))
    return db.execute("SELECT last_insert_rowid()").fetchone()[0]

def ais(name, is_auto=False):
    db.execute("INSERT INTO insert_sets (set_id, name, is_autograph) VALUES (?, ?, ?)", (SET_ID, name, 1 if is_auto else 0))
    return db.execute("SELECT last_insert_rowid()").fetchone()[0]

def ap(is_id, pars):
    for p in pars:
        name, pr = p[0], p[1]
        excl = p[2] if len(p) > 2 else None
        db.execute("INSERT INTO parallels (insert_set_id, name, print_run, exclusivity) VALUES (?, ?, ?, ?)",
                   (is_id, name, pr, excl))
    return len(pars)

def ac(is_id, cards, role="athlete"):
    for num, name, team, rc in cards:
        pid = goc(name, role)
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)",
                   (pid, is_id, str(num), 1 if rc else 0, team))

def ad(is_id, cards):
    for num, n1, n2 in cards:
        p1, p2 = goc(n1), goc(n2)
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, NULL)", (p1, is_id, str(num)))
        a = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a, p2))

T = True; F = False

# ═══ BASE SET (500 cards) ═══════════════════════════════════════════════════
base_id = ais("Base Set")

# Base parallels (35)
base_pars = [
    ("Refractor",None),("X-Fractor",None,H),("Prism Refractor",None,R_EX),
    ("Blue Prism Refractor",None,R_EX),("Gold Prism Refractor",None,R_EX),
    ("Red Prism Refractor",None,R_EX),("Topps Refractor",499),
    ("Vibrations Refractor",250),("Blue Mini-Diamond Refractor",199),
    ("Blue Vibrations Refractor",150),("Speckle Refractor",150),
    ("Platinum Toile Cream/Fuchsia Shimmer",100,H),("Blue Lava Refractor",100,R_EX),
    ("Platinum Toile White/Green Refractor",99),("Green Wave Refractor",99),
    ("Green Vibrations Refractor",99),("Rose Gold Refractor",75),
    ("Platinum Toile Cream/Rose Gold Refractor",75),("Rose Gold Mini-Diamond Refractor",75),
    ("Diamond Etch Refractor",55),("Gold Refractor",50),("Gold Vibrations Refractor",50),
    ("Gold Wave Refractor",50,H),("Platinum Toile Cream/Gold Refractor",50),
    ("Orange Refractor",25),("Platinum Toile White/Orange Refractor",25),
    ("Orange Vibrations Refractor",25),("Orange Wave Refractor",25,H),
    ("Black Refractor",10),("Platinum Toile Cream/Black Refractor",10),
    ("Black Vibrations Refractor",10),("Red Refractor",5),
    ("Platinum Toile Cream/Red Refractor",5),("Red Vibrations Refractor",5),
    ("Red Lava Refractor",5,H),("SuperFractor",1),
]
n = ap(base_id, base_pars)
print(f"  Base parallels: {n}")

# Cards 1-500 (I'll insert them all programmatically)
base_cards = [
(1,"Mike Trout","Los Angeles Angels",F),(2,"Jarren Duran","Boston Red Sox",F),(3,"Shane Bieber","Toronto Blue Jays",F),(4,"Elly De La Cruz","Cincinnati Reds",F),(5,"Ronald Acuna Jr.","Atlanta Braves",F),(6,"Andres Gimenez","Toronto Blue Jays",F),(7,"Shota Imanaga","Chicago Cubs",F),(8,"Yoshinobu Yamamoto","Los Angeles Dodgers",F),(9,"Michael Harris II","Atlanta Braves",F),(10,"Colton Cowser","Baltimore Orioles",F),
(11,"Josh Naylor","Seattle Mariners",F),(12,"Josh Hader","Houston Astros",F),(13,"Jose Altuve","Houston Astros",F),(14,"Yordan Alvarez","Houston Astros",F),(15,"Cole Ragans","Kansas City Royals",F),(16,"Jackson Chourio","Milwaukee Brewers",F),(17,"Shohei Ohtani","Los Angeles Dodgers",F),(18,"Tommy Edman","Los Angeles Dodgers",F),(19,"Christian Yelich","Milwaukee Brewers",F),(20,"Austin Riley","Atlanta Braves",F),
(21,"Cedric Mullins","New York Mets",F),(22,"Mick Abel","Minnesota Twins",T),(23,"Denzel Clarke","Oakland Athletics",T),(24,"Nico Hoerner","Chicago Cubs",F),(25,"Willi Castro","Chicago Cubs",F),(26,"Cody Bellinger","New York Yankees",F),(27,"Clayton Kershaw","Los Angeles Dodgers",F),(28,"Freddy Peralta","Milwaukee Brewers",F),(29,"Ozzie Albies","Atlanta Braves",F),(30,"Riley Greene","Detroit Tigers",F),
(31,"Javier Baez","Detroit Tigers",F),(32,"Ketel Marte","Arizona Diamondbacks",F),(33,"Blake Snell","Los Angeles Dodgers",F),(34,"Tyler Anderson","Los Angeles Angels",F),(35,"Masataka Yoshida","Boston Red Sox",F),(36,"Francisco Lindor","New York Mets",F),(37,"Maikel Garcia","Kansas City Royals",F),(38,"Zac Gallen","Arizona Diamondbacks",F),(39,"Teoscar Hernandez","Los Angeles Dodgers",F),(40,"Isaac Paredes","Houston Astros",F),
(41,"Bobby Witt Jr.","Kansas City Royals",F),(42,"Trevor Story","Boston Red Sox",F),(43,"Byron Buxton","Minnesota Twins",F),(44,"Framber Valdez","Houston Astros",F),(45,"Jeff McNeil","New York Mets",F),(46,"William Contreras","Milwaukee Brewers",F),(47,"Spencer Steer","Cincinnati Reds",F),(48,"Ceddanne Rafaela","Boston Red Sox",F),(49,"Chris Sale","Atlanta Braves",F),(50,"Michael Toglia","Colorado Rockies",F),
(51,"Shea Langeliers","Oakland Athletics",F),(52,"Brenton Doyle","Colorado Rockies",F),(53,"Spencer Torkelson","Detroit Tigers",F),(54,"Joc Pederson","Texas Rangers",F),(55,"Jeremy Pena","Houston Astros",F),(56,"Wilyer Abreu","Boston Red Sox",F),(57,"Seiya Suzuki","Chicago Cubs",F),(58,"Brandon Nimmo","New York Mets",F),(59,"Starling Marte","New York Mets",F),(60,"Seth Lugo","Kansas City Royals",F),
(61,"Carlos Correa","Houston Astros",F),(62,"Zach Neto","Los Angeles Angels",F),(63,"Rhys Hoskins","Milwaukee Brewers",F),(64,"Matt Olson","Atlanta Braves",F),(65,"Mookie Betts","Los Angeles Dodgers",F),(66,"Justin Verlander","San Francisco Giants",F),(67,"Jackson Holliday","Baltimore Orioles",F),(68,"Tarik Skubal","Detroit Tigers",F),(69,"Kerry Carpenter","Detroit Tigers",F),(70,"Corbin Carroll","Arizona Diamondbacks",F),
(71,"Hunter Greene","Cincinnati Reds",F),(72,"Kyle Stowers","Miami Marlins",F),(73,"Pete Crow-Armstrong","Chicago Cubs",F),(74,"JJ Bleday","Oakland Athletics",F),(75,"Jose Ramirez","Cleveland Guardians",F),(76,"Nolan Schanuel","Los Angeles Angels",F),(77,"Mason Miller","San Diego Padres",F),(78,"Mark Vientos","New York Mets",F),(79,"Freddie Freeman","Los Angeles Dodgers",F),(80,"Ian Happ","Chicago Cubs",F),
(81,"Steven Kwan","Cleveland Guardians",F),(82,"Brent Rooker","Oakland Athletics",F),(83,"Rafael Devers","San Francisco Giants",F),(84,"Garrett Crochet","Boston Red Sox",F),(85,"Gabriel Moreno","Arizona Diamondbacks",F),(86,"Dansby Swanson","Chicago Cubs",F),(87,"Salvador Perez","Kansas City Royals",F),(88,"Xavier Edwards","Miami Marlins",F),(89,"Vinnie Pasquantino","Kansas City Royals",F),(90,"Luis Robert Jr.","Chicago White Sox",F),
(91,"Kyle Tucker","Chicago Cubs",F),(92,"Ryan McMahon","New York Yankees",F),(93,"Carlos Santana","Chicago Cubs",F),(94,"Max Fried","New York Yankees",F),(95,"Ezequiel Tovar","Colorado Rockies",F),(96,"Gunnar Henderson","Baltimore Orioles",F),(97,"Marcell Ozuna","Atlanta Braves",F),(98,"Andrew Benintendi","Chicago White Sox",F),(99,"Adley Rutschman","Baltimore Orioles",F),(100,"Lawrence Butler","Oakland Athletics",F),
(101,"CJ Abrams","Washington Nationals",F),(102,"Trea Turner","Philadelphia Phillies",F),(103,"Michael King","San Diego Padres",F),(104,"Jasson Dominguez","New York Yankees",F),(105,"Mitch Haniger","Seattle Mariners",F),(106,"Jung Hoo Lee","San Francisco Giants",F),(107,"Trevor Williams","Washington Nationals",F),(108,"Willson Contreras","St. Louis Cardinals",F),(109,"Max Scherzer","Toronto Blue Jays",F),(110,"Triston Casas","Boston Red Sox",F),
(111,"Matt Chapman","San Francisco Giants",F),(112,"Jacob deGrom","Texas Rangers",F),(113,"Andrew McCutchen","Pittsburgh Pirates",F),(114,"Royce Lewis","Minnesota Twins",F),(115,"Bo Bichette","Toronto Blue Jays",F),(116,"Adolis Garcia","Texas Rangers",F),(117,"Bryan Reynolds","Pittsburgh Pirates",F),(118,"Jarred Kelenic","Atlanta Braves",F),(119,"Brice Turang","Milwaukee Brewers",F),(120,"Zack Wheeler","Philadelphia Phillies",F),
(121,"Edwin Diaz","New York Mets",F),(122,"Triston McKenzie","Cleveland Guardians",F),(123,"Jackson Merrill","San Diego Padres",F),(124,"Ernie Clement","Toronto Blue Jays",F),(125,"George Kirby","Seattle Mariners",F),(126,"Lars Nootbaar","St. Louis Cardinals",F),(127,"Luis Gil","New York Yankees",F),(128,"Jordan Walker","St. Louis Cardinals",F),(129,"Logan Gilbert","Seattle Mariners",F),(130,"Jazz Chisholm Jr.","New York Yankees",F),
(131,"Jose Berrios","Toronto Blue Jays",F),(132,"Josh Lowe","Tampa Bay Rays",F),(133,"Eugenio Suarez","Seattle Mariners",F),(134,"Randy Arozarena","Seattle Mariners",F),(135,"Bryce Harper","Philadelphia Phillies",F),(136,"Aaron Judge","New York Yankees",F),(137,"Jose Siri","New York Mets",F),(138,"J.P. Crawford","Seattle Mariners",F),(139,"Sonny Gray","St. Louis Cardinals",F),(140,"Fernando Tatis Jr.","San Diego Padres",F),
(141,"Luis Arraez","San Diego Padres",F),(142,"Wyatt Langford","Texas Rangers",F),(143,"Kodai Senga","New York Mets",F),(144,"Gerrit Cole","New York Yankees",F),(145,"Bryson Stott","Philadelphia Phillies",F),(146,"Vladimir Guerrero Jr.","Toronto Blue Jays",F),(147,"Nolan Arenado","St. Louis Cardinals",F),(148,"Spencer Strider","Atlanta Braves",F),(149,"Brendan Donovan","St. Louis Cardinals",F),(150,"Yu Darvish","San Diego Padres",F),
(151,"Justin Steele","Chicago Cubs",F),(152,"Daulton Varsho","Toronto Blue Jays",F),(153,"Christopher Morel","Tampa Bay Rays",F),(154,"Mike Yastrzemski","Kansas City Royals",F),(155,"Corey Seager","Texas Rangers",F),(156,"Aaron Nola","Philadelphia Phillies",F),(157,"Ke'Bryan Hayes","Cincinnati Reds",F),(158,"Christian Walker","Houston Astros",F),(159,"Carlos Rodon","New York Yankees",F),(160,"Cal Raleigh","Seattle Mariners",F),
(161,"Corbin Burnes","Arizona Diamondbacks",F),(162,"Anthony Volpe","New York Yankees",F),(163,"Masyn Winn","St. Louis Cardinals",F),(164,"Jonathan India","Kansas City Royals",F),(165,"Austin Wells","New York Yankees",F),(166,"MacKenzie Gore","Washington Nationals",F),(167,"Manny Machado","San Diego Padres",F),(168,"Junior Caminero","Tampa Bay Rays",F),(169,"Lourdes Gurriel Jr.","Arizona Diamondbacks",F),(170,"Willy Adames","San Francisco Giants",F),
(171,"J.T. Realmuto","Philadelphia Phillies",F),(172,"Oneil Cruz","Pittsburgh Pirates",F),(173,"Alec Burleson","St. Louis Cardinals",F),(174,"Xander Bogaerts","San Diego Padres",F),(175,"Kyle Schwarber","Philadelphia Phillies",F),(176,"Logan Webb","San Francisco Giants",F),(177,"Josh Smith","Texas Rangers",F),(178,"Dylan Cease","San Diego Padres",F),(179,"Julio Rodriguez","Seattle Mariners",F),(180,"Yandy Diaz","Tampa Bay Rays",F),
(181,"Marcus Semien","Texas Rangers",F),(182,"Will Smith","Los Angeles Dodgers",F),(183,"Logan O'Hoppe","Los Angeles Angels",F),(184,"Hunter Brown","Houston Astros",F),(185,"Ryan Helsley","New York Mets",F),(186,"Christian Encarnacion-Strand","Cincinnati Reds",F),(187,"Nolan Gorman","St. Louis Cardinals",F),(188,"Giancarlo Stanton","New York Yankees",F),(189,"Alec Bohm","Philadelphia Phillies",F),(190,"Luis Garcia Jr.","Washington Nationals",F),
(191,"Heliot Ramos","San Francisco Giants",F),(192,"George Springer","Toronto Blue Jays",F),(193,"Pete Alonso","New York Mets",F),(194,"Brandon Lowe","Tampa Bay Rays",F),(195,"Chris Bassitt","Toronto Blue Jays",F),(196,"Alex Bregman","Boston Red Sox",F),(197,"Paul Skenes","Pittsburgh Pirates",F),(198,"Evan Carter","Texas Rangers",F),(199,"Juan Soto","New York Mets",F),(200,"Tyler Glasnow","Los Angeles Dodgers",F),
(201,"Will Wagner","San Diego Padres",T),(202,"Grant McCray","San Francisco Giants",T),(203,"Jack Kochanowicz","Los Angeles Angels",T),(204,"Ichiro","Seattle Mariners",F),(205,"Rhett Lowder","Cincinnati Reds",T),(206,"Paul Goldschmidt","New York Yankees",F),(207,"Darren Baker","Washington Nationals",T),(208,"Juan Marichal","San Francisco Giants",F),(209,"Kumar Rocker","Texas Rangers",T),(210,"Fraser Ellard","Chicago White Sox",T),
(211,"Shane Smith","Chicago White Sox",T),(212,"Matthew Boyd","Chicago Cubs",F),(213,"Billy Wagner","Houston Astros",F),(214,"Thurman Munson","New York Yankees",F),(215,"Kameron Misner","Tampa Bay Rays",T),(216,"Moises Ballesteros","Chicago Cubs",T),(217,"Thomas Saggese","St. Louis Cardinals",T),(218,"Noah Cameron","Kansas City Royals",T),(219,"Coby Mayo","Baltimore Orioles",T),(220,"Nacho Alvarez Jr.","Atlanta Braves",T),
(221,"Jaden Hill","Colorado Rockies",T),(222,"Cade Horton","Chicago Cubs",T),(223,"Dustin Harris","Texas Rangers",T),(224,"Jairo Iriarte","Chicago White Sox",T),(225,"Manny Ramirez","Boston Red Sox",F),(226,"Tim Tawa","Arizona Diamondbacks",T),(227,"CC Sabathia","New York Yankees",F),(228,"Hideki Matsui","New York Yankees",F),(229,"Edgar Quero","Chicago White Sox",T),(230,"Ty Madden","Detroit Tigers",T),
(231,"Jackson Jobe","Detroit Tigers",T),(232,"Chan Ho Park","Los Angeles Dodgers",F),(233,"Hideo Nomo","Los Angeles Dodgers",F),(234,"Jorbit Vivas","New York Yankees",T),(235,"Jose Canseco","Oakland Athletics",F),(236,"River Ryan","Los Angeles Dodgers",T),(237,"Luis Peralta","Colorado Rockies",T),(238,"Zebby Matthews","Minnesota Twins",T),(239,"Roki Sasaki","Los Angeles Dodgers",T),(240,"Dave Parker","Pittsburgh Pirates",F),
(241,"Agustin Ramirez","Miami Marlins",T),(242,"Andres Galarraga","Montreal Expos",F),(243,"Tim Elko","Chicago White Sox",T),(244,"Dylan Crews","Washington Nationals",T),(245,"Chayce McDermott","Baltimore Orioles",T),(246,"Samuel Aldegheri","Los Angeles Angels",T),(247,"Caden Dana","Los Angeles Angels",T),(248,"Bo Jackson","Kansas City Royals",F),(249,"Zach Dezenzo","Houston Astros",T),(250,"Daniel Robert","Philadelphia Phillies",T),
(251,"Cy Young","Boston Red Sox",F),(252,"Brooks Baldwin","Chicago White Sox",T),(253,"Luisangel Acuna","New York Mets",T),(254,"Nick Kurtz","Oakland Athletics",T),(255,"Tyler Callihan","Cincinnati Reds",T),(256,"Carlos Narvaez","Boston Red Sox",T),(257,"Jace Jung","Detroit Tigers",T),(258,"John Smoltz","Atlanta Braves",F),(259,"Erik Sabrowski","Cleveland Guardians",T),(260,"Thomas Harrington","Pittsburgh Pirates",T),
(261,"David Morgan","San Diego Padres",T),(262,"Griffin Conine","Miami Marlins",T),(263,"Dick Allen","Philadelphia Phillies",F),(264,"DaShawn Keirsey","Minnesota Twins",T),(265,"Drake Baldwin","Atlanta Braves",T),(266,"Andres Chaparro","Washington Nationals",T),(267,"Marcelo Mayer","Boston Red Sox",T),(268,"Richard Fitts","Boston Red Sox",T),(269,"Craig Yoho","Milwaukee Brewers",T),(270,"Ted Simmons","St. Louis Cardinals",F),
(271,"Chase Petty","Cincinnati Reds",T),(272,"Luke Keaschall","Minnesota Twins",T),(273,"Marc Church","Texas Rangers",T),(274,"Logan Evans","Seattle Mariners",T),(275,"Isaac Collins","Milwaukee Brewers",T),(276,"Jason Giambi","Oakland Athletics",F),(277,"Chandler Simpson","Tampa Bay Rays",T),(278,"Niko Kavadas","Los Angeles Angels",T),(279,"Adrian Del Castillo","Arizona Diamondbacks",T),(280,"Scott Rolen","St. Louis Cardinals",F),
(281,"Shay Whitcomb","Houston Astros",T),(282,"Eric Wagaman","Miami Marlins",T),(283,"Jacob Wilson","Oakland Athletics",T),(284,"Nick Yorke","Pittsburgh Pirates",T),(285,"Max Muncy","Oakland Athletics",T),(286,"Bryce Teodosio","Los Angeles Angels",T),(287,"Kevin Alcantara","Chicago Cubs",T),(288,"Chase Dollander","Colorado Rockies",T),(289,"Nic Enright","Cleveland Guardians",T),(290,"Michael McGreevy","St. Louis Cardinals",T),
(291,"Joey Cantillo","Cleveland Guardians",T),(292,"Dillon Dingler","Detroit Tigers",T),(293,"Jake Mangum","Tampa Bay Rays",T),(294,"Will Warren","New York Yankees",T),(295,"Dalton Rushing","Los Angeles Dodgers",T),(296,"Hunter Bigge","Tampa Bay Rays",T),(297,"Caleb Durbin","Milwaukee Brewers",T),(298,"Trey Sweeney","Detroit Tigers",T),(299,"Edgardo Henriquez","Los Angeles Dodgers",T),(300,"Robert Hassell III","Washington Nationals",T),
(301,"Spencer Bivens","San Francisco Giants",T),(302,"Wade Boggs","Boston Red Sox",F),(303,"Greg Maddux","Chicago Cubs",F),(304,"Hank Aaron","Atlanta Braves",F),(305,"Cal Ripken Jr.","Baltimore Orioles",F),(306,"Jim Palmer","Baltimore Orioles",F),(307,"Billy Williams","Chicago Cubs",F),(308,"Valente Bellozo","Miami Marlins",T),(309,"Matt Shaw","Chicago Cubs",T),(310,"Adam Mazur","Miami Marlins",T),
(311,"Ben Rice","New York Yankees",T),(312,"Luis Gonzalez","Arizona Diamondbacks",F),(313,"Mike Mussina","Baltimore Orioles",F),(314,"Brady Basso","Oakland Athletics",T),(315,"Brooks Lee","Minnesota Twins",T),(316,"Paul O'Neill","New York Yankees",F),(317,"Colton Gordon","Houston Astros",T),(318,"Kristian Campbell","Boston Red Sox",T),(319,"Cade Povich","Baltimore Orioles",T),(320,"Rickey Henderson","Oakland Athletics",F),
(321,"Connor Norby","Miami Marlins",T),(322,"Blake Dunn","Cincinnati Reds",T),(323,"Eddie Mathews","Atlanta Braves",F),(324,"Cliff Lee","Philadelphia Phillies",F),(325,"Zac Veen","Colorado Rockies",T),(326,"Randy Johnson","Arizona Diamondbacks",F),(327,"Leo Jimenez","Toronto Blue Jays",T),(328,"Justyn-Henry Malloy","Detroit Tigers",T),(329,"Jhonkensy Noel","Cleveland Guardians",T),(330,"Rece Hinds","Cincinnati Reds",T),
(331,"Jake Bloss","Toronto Blue Jays",T),(332,"Spencer Schwellenbach","Atlanta Braves",T),(333,"Lee Smith","St. Louis Cardinals",F),(334,"Brandon Webb","Arizona Diamondbacks",F),(335,"Steward Berroa","Milwaukee Brewers",T),(336,"Hayden Birdsong","San Francisco Giants",T),(337,"Reggie Jackson","Oakland Athletics",F),(338,"Keider Montero","Detroit Tigers",T),(339,"Angel Chivilli","Colorado Rockies",T),(340,"Ernie Banks","Chicago Cubs",F),
(341,"Daniel Schneemann","Cleveland Guardians",T),(342,"Lefty Grove","Philadelphia Athletics",F),(343,"Adam Jones","Baltimore Orioles",F),(344,"David Ortiz","Boston Red Sox",F),(345,"Luis Contreras","Houston Astros",T),(346,"Jim Edmonds","California Angels",F),(347,"Rod Carew","California Angels",F),(348,"Ryne Sandberg","Chicago Cubs",F),(349,"Orelvis Martinez","Toronto Blue Jays",T),(350,"Tyler Phillips","Miami Marlins",T),
(351,"Ted Williams","Boston Red Sox",F),(352,"Duke Ellis","New York Yankees",T),(353,"Warren Spahn","Milwaukee Braves",F),(354,"Adrian Gonzalez","San Diego Padres",F),(355,"DJ Herz","Washington Nationals",T),(356,"Ryan Howard","Philadelphia Phillies",F),(357,"Carlton Fisk","Boston Red Sox",F),(358,"Adael Amador","Colorado Rockies",T),(359,"Angel Martinez","Cleveland Guardians",T),(360,"Hyeseong Kim","Los Angeles Dodgers",T),
(361,"Grant Holmes","Atlanta Braves",T),(362,"Matthew Lugo","Los Angeles Angels",T),(363,"Dale Murphy","Atlanta Braves",F),(364,"Fergie Jenkins","Chicago Cubs",F),(365,"Barry Zito","Oakland Athletics",F),(366,"Cam Smith","Houston Astros",T),(367,"James Wood","Washington Nationals",T),(368,"Carl Yastrzemski","Boston Red Sox",F),(369,"David Festa","Minnesota Twins",T),(370,"Vladimir Guerrero","Los Angeles Angels",F),
(371,"Cristian Mena","Arizona Diamondbacks",T),(372,"Drew Thorpe","Chicago White Sox",T),(373,"Tyler Locklear","Arizona Diamondbacks",T),(374,"Chipper Jones","Atlanta Braves",F),(375,"Justin Morneau","Minnesota Twins",F),(376,"Gordon Graceffo","St. Louis Cardinals",T),(377,"Bradley Blalock","Colorado Rockies",T),(378,"Tommy Nance","Toronto Blue Jays",F),(379,"Luis Tiant","Boston Red Sox",F),(380,"Bryan King","Houston Astros",T),
(381,"Eddie Murray","Baltimore Orioles",F),(382,"Dennis Eckersley","Oakland Athletics",F),(383,"Mark Grace","Chicago Cubs",F),(384,"Steven Wilson","Chicago White Sox",F),(385,"Gunnar Hoglund","Oakland Athletics",T),(386,"Aaron Schunk","Colorado Rockies",T),(387,"Tanner Gordon","Colorado Rockies",T),(388,"Chase Meidroth","Chicago White Sox",T),(389,"Eric Orze","Tampa Bay Rays",T),(390,"Gavin Hollowell","Chicago Cubs",F),
(391,"Dusty Baker","Los Angeles Dodgers",F),(392,"Yilber Diaz","Arizona Diamondbacks",T),(393,"Justin Wrobleski","Los Angeles Dodgers",T),(394,"Tomoyuki Sugano","Baltimore Orioles",T),(395,"Fred Lynn","Boston Red Sox",F),(396,"Sammy Sosa","Chicago Cubs",F),(397,"Ryan Bliss","Seattle Mariners",T),(398,"Nolan Ryan","California Angels",F),(399,"Tirso Ornelas","San Diego Padres",T),(400,"Hurston Waldrep","Atlanta Braves",T),
(401,"Alex Rodriguez","Seattle Mariners",F),(402,"Craig Biggio","Houston Astros",F),(403,"Roberto Clemente","Pittsburgh Pirates",F),(404,"Willie McCovey","San Francisco Giants",F),(405,"Ken Griffey Jr.","Seattle Mariners",F),(406,"Vladimir Guerrero","Montreal Expos",F),(407,"Paul Konerko","Chicago White Sox",F),(408,"Bob Gibson","St. Louis Cardinals",F),(409,"Gaylord Perry","San Francisco Giants",F),(410,"Joe Torre","St. Louis Cardinals",F),
(411,"Don Drysdale","Los Angeles Dodgers",F),(412,"Bobby Abreu","Philadelphia Phillies",F),(413,"Luis Aparicio","Chicago White Sox",F),(414,"Tyler O'Neill","Baltimore Orioles",F),(415,"Duke Snider","Brooklyn Dodgers",F),(416,"Mike Schmidt","Philadelphia Phillies",F),(417,"Prince Fielder","Milwaukee Brewers",F),(418,"Babe Ruth","New York Yankees",F),(419,"Alex Gordon","Kansas City Royals",F),(420,"Darryl Strawberry","New York Mets",F),
(421,"Willie Stargell","Pittsburgh Pirates",F),(422,"Jorge Posada","New York Yankees",F),(423,"Jimmy Rollins","Philadelphia Phillies",F),(424,"Derrek Lee","Chicago Cubs",F),(425,"Andre Dawson","Montreal Expos",F),(426,"Joe Morgan","Houston Astros",F),(427,"Roger Maris","St. Louis Cardinals",F),(428,"Larry Walker","Colorado Rockies",F),(429,"George Brett","Kansas City Royals",F),(430,"Hal Newhouser","Detroit Tigers",F),
(431,"Tony Gwynn","San Diego Padres",F),(432,"Harmon Killebrew","Minnesota Twins",F),(433,"Paul Molitor","Minnesota Twins",F),(434,"Ozzie Smith","San Diego Padres",F),(435,"Pedro Martinez","Montreal Expos",F),(436,"Orlando Cepeda","San Francisco Giants",F),(437,"Tom Seaver","New York Mets",F),(438,"Tris Speaker","Cleveland Indians",F),(439,"Honus Wagner","Pittsburgh Pirates",F),(440,"Cecil Fielder","Detroit Tigers",F),
(441,"Rafael Palmeiro","Texas Rangers",F),(442,"Goose Gossage","Chicago White Sox",F),(443,"Rogers Hornsby","St. Louis Cardinals",F),(444,"Billy Martin","New York Yankees",F),(445,"Tony Oliva","Minnesota Twins",F),(446,"Jason Kendall","Pittsburgh Pirates",F),(447,"Sandy Koufax","Brooklyn Dodgers",F),(448,"Kirby Puckett","Minnesota Twins",F),(449,"Frank Thomas","Chicago White Sox",F),(450,"Yogi Berra","New York Yankees",F),
(451,"Barry Larkin","Cincinnati Reds",F),(452,"Bert Blyleven","Minnesota Twins",F),(453,"Evan Longoria","Tampa Bay Rays",F),(454,"Johnny Bench","Cincinnati Reds",F),(455,"Fred McGriff","Toronto Blue Jays",F),(456,"Roger Clemens","Toronto Blue Jays",F),(457,"Tony Perez","Cincinnati Reds",F),(458,"Derek Jeter","New York Yankees",F),(459,"Jose Cruz","Houston Astros",F),(460,"Alan Trammell","Detroit Tigers",F),
(461,"Albert Pujols","St. Louis Cardinals",F),(462,"Trevor Hoffman","San Diego Padres",F),(463,"Bill Mazeroski","Pittsburgh Pirates",F),(464,"Edgar Martinez","Seattle Mariners",F),(465,"Mike Piazza","New York Mets",F),(466,"Felix Hernandez","Seattle Mariners",F),(467,"Pete Rose","Cincinnati Reds",F),(468,"Jeff Bagwell","Houston Astros",F),(469,"Willie Mays","San Francisco Giants",F),(470,"Miguel Cabrera","Detroit Tigers",F),
(471,"Adrian Gonzalez","Los Angeles Dodgers",F),(472,"Matt Holliday","Colorado Rockies",F),(473,"Bret Saberhagen","Kansas City Royals",F),(474,"Mark Buehrle","Chicago White Sox",F),(475,"Johnny Damon","Kansas City Royals",F),(476,"Tim Raines","Montreal Expos",F),(477,"Joey Votto","Cincinnati Reds",F),(478,"Jack Morris","Detroit Tigers",F),(479,"Chase Utley","Philadelphia Phillies",F),(480,"Jackie Robinson","Brooklyn Dodgers",F),
(481,"Ron Guidry","New York Yankees",F),(482,"Gary Carter","Montreal Expos",F),(483,"David Wright","New York Mets",F),(484,"Dave Winfield","San Diego Padres",F),(485,"Michael Young","Texas Rangers",F),(486,"Robin Yount","Milwaukee Brewers",F),(487,"Al Kaline","Detroit Tigers",F),(488,"Orel Hershiser","Los Angeles Dodgers",F),(489,"Adrian Beltre","Texas Rangers",F),(490,"Lou Gehrig","New York Yankees",F),
(491,"Andy Van Slyke","Pittsburgh Pirates",F),(492,"Ty Cobb","Detroit Tigers",F),(493,"Carlos Beltran","New York Mets",F),(494,"Ivan Rodriguez","Texas Rangers",F),(495,"Steve Carlton","Philadelphia Phillies",F),(496,"Kirk Gibson","Los Angeles Dodgers",F),(497,"Hanley Ramirez","Florida Marlins",F),(498,"Christy Mathewson","New York Giants",F),(499,"Satchel Paige","Cleveland Indians",F),(500,"Buster Posey","San Francisco Giants",F),
]
ac(base_id, base_cards)
print(f"  Base Set: {len(base_cards)} cards")

# ═══ IMAGE VARIATIONS (40 cards) ════════════════════════════════════════════
iv_id = ais("Base Card Image Variations")
iv_nums = [1,4,5,8,14,16,17,27,36,41,57,65,79,96,135,136,146,155,167,179,197,219,231,239,244,253,254,267,283,295,309,315,318,326,351,366,367,405,418,469]
for num in iv_nums:
    # Find the base card's athlete
    card = next((c for c in base_cards if c[0] == num), None)
    if card:
        pid = goc(card[1])
        rc = card[3]
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)",
                   (pid, iv_id, str(num), 1 if rc else 0, card[2]))
print(f"  Base Card Image Variations: {len(iv_nums)} cards")

# ═══ CITY VARIATIONS (80 cards) ═════════════════════════════════════════════
cv_id = ais("1955 Topps City Variations")
cv_cards = [
("55CV-1","Mike Trout","Los Angeles Angels",F),("55CV-2","Rod Carew","California Angels",F),("55CV-3","Randy Johnson","Arizona Diamondbacks",F),("55CV-4","Corbin Carroll","Arizona Diamondbacks",F),("55CV-5","Reggie Jackson","Oakland Athletics",F),("55CV-6","Rickey Henderson","Oakland Athletics",F),("55CV-7","Ronald Acuna Jr.","Atlanta Braves",F),("55CV-8","Dale Murphy","Atlanta Braves",F),("55CV-9","Chipper Jones","Atlanta Braves",F),("55CV-10","Cal Ripken Jr.","Baltimore Orioles",F),
("55CV-11","Jackson Holliday","Baltimore Orioles",F),("55CV-12","Gunnar Henderson","Baltimore Orioles",F),("55CV-13","Eddie Murray","Baltimore Orioles",F),("55CV-14","David Ortiz","Boston Red Sox",F),("55CV-15","Carl Yastrzemski","Boston Red Sox",F),("55CV-16","Rafael Devers","San Francisco Giants",F),("55CV-17","Shota Imanaga","Chicago Cubs",F),("55CV-18","Pete Crow-Armstrong","Chicago Cubs",F),("55CV-19","Dansby Swanson","Chicago Cubs",F),("55CV-20","Matt Shaw","Chicago Cubs",T),
("55CV-21","Jim Thome","Chicago White Sox",F),("55CV-22","Frank Thomas","Chicago White Sox",F),("55CV-23","Johnny Bench","Cincinnati Reds",F),("55CV-24","Elly De La Cruz","Cincinnati Reds",F),("55CV-25","Cade Horton","Chicago Cubs",T),("55CV-26","Jose Ramirez","Cleveland Guardians",F),("55CV-27","Larry Walker","Colorado Rockies",F),("55CV-28","Riley Greene","Detroit Tigers",F),("55CV-29","Ivan Rodriguez","Detroit Tigers",F),("55CV-30","Gary Sheffield","Florida Marlins",F),
("55CV-31","Yordan Alvarez","Houston Astros",F),("55CV-32","Jose Altuve","Houston Astros",F),("55CV-33","Kyle Tucker","Chicago Cubs",F),("55CV-34","Bo Jackson","Kansas City Royals",F),("55CV-35","Bobby Witt Jr.","Kansas City Royals",F),("55CV-36","George Brett","Kansas City Royals",F),("55CV-37","Shohei Ohtani","Los Angeles Dodgers",F),("55CV-38","Clayton Kershaw","Los Angeles Dodgers",F),("55CV-39","Drake Baldwin","Atlanta Braves",T),("55CV-40","Yoshinobu Yamamoto","Los Angeles Dodgers",F),
("55CV-41","Mookie Betts","Los Angeles Dodgers",F),("55CV-42","Roki Sasaki","Los Angeles Dodgers",T),("55CV-43","Sandy Koufax","Brooklyn Dodgers",F),("55CV-44","Christian Yelich","Milwaukee Brewers",F),("55CV-45","Jackson Chourio","Milwaukee Brewers",F),("55CV-46","Paul Molitor","Minnesota Twins",F),("55CV-47","Pedro Martinez","Montreal Expos",F),("55CV-48","Darryl Strawberry","New York Mets",F),("55CV-49","Pete Alonso","New York Mets",F),("55CV-50","Francisco Lindor","New York Mets",F),
("55CV-51","Derek Jeter","New York Yankees",F),("55CV-52","Cal Raleigh","Seattle Mariners",F),("55CV-53","Aaron Judge","New York Yankees",F),("55CV-54","Juan Soto","New York Mets",F),("55CV-55","Kristian Campbell","Boston Red Sox",T),("55CV-56","Bryce Harper","Philadelphia Phillies",F),("55CV-57","Chase Utley","Philadelphia Phillies",F),("55CV-58","Mike Schmidt","Philadelphia Phillies",F),("55CV-59","Paul Skenes","Pittsburgh Pirates",F),("55CV-60","Manny Machado","San Diego Padres",F),
("55CV-61","Fernando Tatis Jr.","San Diego Padres",F),("55CV-62","Nick Kurtz","Oakland Athletics",T),("55CV-63","Buster Posey","San Francisco Giants",F),("55CV-64","Will Clark","San Francisco Giants",F),("55CV-65","Ichiro","Seattle Mariners",F),("55CV-66","Ken Griffey Jr.","Seattle Mariners",F),("55CV-67","Julio Rodriguez","Seattle Mariners",F),("55CV-68","Edgar Martinez","Seattle Mariners",F),("55CV-69","Albert Pujols","St. Louis Cardinals",F),("55CV-70","Yadier Molina","St. Louis Cardinals",F),
("55CV-71","Nolan Arenado","St. Louis Cardinals",F),("55CV-72","Mark McGwire","St. Louis Cardinals",F),("55CV-73","Wade Boggs","Tampa Bay Devil Rays",F),("55CV-74","Nolan Ryan","Texas Rangers",F),("55CV-75","Alex Rodriguez","Texas Rangers",F),("55CV-76","Corey Seager","Texas Rangers",F),("55CV-77","Adrian Beltre","Texas Rangers",F),("55CV-78","Vladimir Guerrero Jr.","Toronto Blue Jays",F),("55CV-79","James Wood","Washington Nationals",T),("55CV-80","Dylan Crews","Washington Nationals",T),
]
ac(cv_id, cv_cards)
print(f"  1955 Topps City Variations: {len(cv_cards)} cards")

# ═══ INSERT SUBSETS ══════════════════════════════════════════════════════════
insert_pars = [("Green Refractor",99),("Gold Refractor",50),("Orange Refractor",25),("Black Refractor",10),("Red Refractor",5),("SuperFractor",1)]

# 55WS
ws_id = ais("1955 World Series")
ap(ws_id, insert_pars)
ac(ws_id, [("55WS-1","Roy Campanella","Brooklyn Dodgers",F),("55WS-2","Pee Wee Reese","Brooklyn Dodgers",F),("55WS-3","Jackie Robinson","Brooklyn Dodgers",F),("55WS-4","Duke Snider","Brooklyn Dodgers",F),("55WS-5","Gil Hodges","Brooklyn Dodgers",F),("55WS-6","Sandy Koufax","Brooklyn Dodgers",F),("55WS-7","Casey Stengel","New York Yankees",F),("55WS-8","Yogi Berra","New York Yankees",F),("55WS-9","Whitey Ford","New York Yankees",F),("55WS-10","Mickey Mantle","New York Yankees",F)])
print(f"  1955 World Series: 10 cards")

# 55RS
rs_id = ais("1955 Topps Rails and Sails")
ap(rs_id, insert_pars)
ac(rs_id, [("55RS-1","Juan Soto","New York Mets",F),("55RS-2","Lou Brock","St. Louis Cardinals",F),("55RS-3","Francisco Lindor","New York Mets",F),("55RS-4","Albert Pujols","St. Louis Cardinals",F),("55RS-5","Roger Clemens","New York Yankees",F),("55RS-6","Alex Rodriguez","New York Yankees",F),("55RS-7","Rickey Henderson","Oakland Athletics",F),("55RS-8","Ken Griffey Jr.","Seattle Mariners",F),("55RS-9","Ivan Rodriguez","Texas Rangers",F),("55RS-10","Giancarlo Stanton","New York Yankees",F),
("55RS-11","Vladimir Guerrero","Los Angeles Angels",F),("55RS-12","Manny Ramirez","Boston Red Sox",F),("55RS-13","Pedro Martinez","Boston Red Sox",F),("55RS-14","Randy Johnson","Arizona Diamondbacks",F),("55RS-15","Nolan Ryan","Texas Rangers",F),("55RS-16","Greg Maddux","Chicago Cubs",F),("55RS-17","Eddie Murray","Baltimore Orioles",F),("55RS-18","Manny Machado","San Diego Padres",F),("55RS-19","Shohei Ohtani","Los Angeles Dodgers",F),("55RS-20","Bryce Harper","Philadelphia Phillies",F)])
print(f"  1955 Topps Rails and Sails: 20 cards")

# 55DH (dual-subject)
dh_id = ais("1955 Topps Doubleheaders")
ap(dh_id, insert_pars)
ad(dh_id, [
("55DH-1","Sandy Koufax","Shohei Ohtani"),("55DH-2","Mickey Mantle","Aaron Judge"),("55DH-3","Jackie Robinson","Mookie Betts"),("55DH-4","Mike Schmidt","Bryce Harper"),("55DH-5","Mike Piazza","Francisco Lindor"),("55DH-6","Albert Pujols","Stan Musial"),("55DH-7","Carl Yastrzemski","Ted Williams"),("55DH-8","Ken Griffey Jr.","Ichiro"),("55DH-9","Roki Sasaki","Yoshinobu Yamamoto"),("55DH-10","Roger Maris","Mickey Mantle"),
("55DH-11","Ronald Acuna Jr.","Hank Aaron"),("55DH-12","Bobby Witt Jr.","George Brett"),("55DH-13","Cal Ripken Jr.","Gunnar Henderson"),("55DH-14","Tony Gwynn","Fernando Tatis Jr."),("55DH-15","Vladimir Guerrero Jr.","Vladimir Guerrero"),("55DH-16","Pedro Martinez","David Ortiz"),("55DH-17","Brooks Robinson","Eddie Murray"),("55DH-18","Nolan Ryan","Mike Trout"),("55DH-19","Lou Brock","Bob Gibson"),("55DH-20","Nick Kurtz","Jacob Wilson"),
])
print(f"  1955 Topps Doubleheaders: 20 cards (dual)")

# 55NW
nw_id = ais("1955 Cards That Never Were")
ap(nw_id, [("SuperFractor",1,H)])
ac(nw_id, [("55NW-1","Stan Musial","St. Louis Cardinals",F),("55NW-2","Whitey Ford","New York Yankees",F),("55NW-3","Bob Feller","Cleveland Indians",F),("55NW-4","Mickey Mantle","New York Yankees",F),("55NW-5","Roy Campanella","Brooklyn Dodgers",F),("55NW-6","Pee Wee Reese","Brooklyn Dodgers",F),("55NW-7","Richie Ashburn","Philadelphia Phillies",F),("55NW-8","Ralph Kiner","Cleveland Indians",F),("55NW-9","Brooks Robinson","Baltimore Orioles",F),("55NW-10","Jim Bunning","Detroit Tigers",F),
("55NW-11","Hoyt Wilhelm","New York Giants",F),("55NW-12","Red Schoendienst","St. Louis Cardinals",F),("55NW-13","George Kell","Detroit Tigers",F),("55NW-14","Larry Doby","Cleveland Indians",F),("55NW-15","Early Wynn","Cleveland Indians",F),("55NW-16","Robin Roberts","Philadelphia Phillies",F),("55NW-17","Don Larsen","New York Yankees",F),("55NW-18","Al Lopez","Cleveland Indians",F),("55NW-19","Bob Lemon","Cleveland Indians",F),("55NW-20","Casey Stengel","New York Yankees",F)])
print(f"  1955 Cards That Never Were: 20 cards")

# 55E (Topps employees - celebrity role)
e_id = ais("1955 Topps Employee Super Short Prints")
ac(e_id, [("55E-AC","Ariel Charnowitz","Arizona Diamondbacks",F),("55E-HS","Hunter Stanley","Los Angeles Dodgers",F),("55E-JR","Josh Ringler","New York Yankees",F),("55E-KA","Keith Andrews","New York Mets",F),("55E-KB","Krystal Beisick","New York Yankees",F),("55E-KR","Keith Rothschild","New York Mets",F),("55E-MD","Michelle Diller","New York Yankees",F),("55E-ML","Micah Layton","Texas Rangers",F),("55E-NR","Nikki Rubin","New York Yankees",F),("55E-PO","Pat O'Sullivan","Boston Red Sox",F)], role="celebrity")
print(f"  1955 Topps Employee SSPs: 10 cards (celebrity)")

# ═══ CHROME PLATINUM AUTOGRAPHS (178 cards) ═════════════════════════════════
cpa_id = ais("Chrome Platinum Autographs", is_auto=True)
cpa_pars = [("Refractor",199),("Aqua Refractor",150),("Platinum Toile Cream/Blue Refractor",99),("Blue Prism Refractor",99,H),("Green Mini Diamond Refractor",75,R_EX),("Gold Refractor",50),("Orange Refractor",25,H),("Pink Refractor",15,H),("Black Refractor",10),("Red Refractor",5),("Platinum Toile Cream/Red Refractor",5),("SuperFractor",1)]
ap(cpa_id, cpa_pars)

cpa_cards = [
("CPA-AA","Adael Amador","Colorado Rockies",T),("CPA-AD","Andre Dawson","Montreal Expos",F),("CPA-AG","Alex Gordon","Kansas City Royals",F),("CPA-AJ","Aaron Judge","New York Yankees",F),("CPA-AM","Angel Martinez","Cleveland Guardians",T),("CPA-AMA","Adam Mazur","Miami Marlins",T),("CPA-AP","Andy Pettitte","New York Yankees",F),("CPA-API","AJ Pierzynski","Chicago White Sox",F),("CPA-AR","Alex Rodriguez","Texas Rangers",F),("CPA-ARI","Austin Riley","Atlanta Braves",F),
("CPA-ARU","Adley Rutschman","Baltimore Orioles",F),("CPA-AS","Aaron Schunk","Colorado Rockies",T),("CPA-AV","Anthony Volpe","New York Yankees",F),("CPA-AVA","Andy Van Slyke","Pittsburgh Pirates",F),("CPA-BB","Brady Basso","Oakland Athletics",T),("CPA-BBA","Brooks Baldwin","Chicago White Sox",T),("CPA-BBL","Bradley Blalock","Colorado Rockies",T),("CPA-BD","Brendan Donovan","St. Louis Cardinals",F),("CPA-BDU","Blake Dunn","Cincinnati Reds",T),("CPA-BL","Brooks Lee","Minnesota Twins",T),
("CPA-BN","Brandon Nimmo","New York Mets",F),("CPA-BR","Ben Rice","New York Yankees",T),("CPA-BS","Bryson Stott","Philadelphia Phillies",F),("CPA-BW","Bobby Witt Jr.","Kansas City Royals",F),("CPA-BWI","Billy Williams","Chicago Cubs",F),("CPA-CAD","Caden Dana","Los Angeles Angels",T),("CPA-CAN","Carlos Narvaez","Boston Red Sox",T),("CPA-CB","Craig Biggio","Houston Astros",F),("CPA-CC","Corbin Carroll","Arizona Diamondbacks",F),("CPA-CCO","Colton Cowser","Baltimore Orioles",F),
("CPA-CF","Carlton Fisk","Boston Red Sox",F),("CPA-CHP","Chan Ho Park","Los Angeles Dodgers",F),("CPA-CK","Clayton Kershaw","Los Angeles Dodgers",F),("CPA-CKE","Colt Keith","Detroit Tigers",F),("CPA-CM","Cedric Mullins","Baltimore Orioles",F),("CPA-CMA","Coby Mayo","Baltimore Orioles",T),("CPA-CMD","Chayce McDermott","Baltimore Orioles",T),("CPA-CME","Cristian Mena","Arizona Diamondbacks",T),("CPA-CML","Christopher Morel","Tampa Bay Rays",F),("CPA-CN","Connor Norby","Miami Marlins",T),
("CPA-CP","Cade Povich","Baltimore Orioles",T),("CPA-CR","Cal Raleigh","Seattle Mariners",F),("CPA-CRO","Carlos Rodriguez","Milwaukee Brewers",T),("CPA-CS","Cam Smith","Houston Astros",T),("CPA-CY","Christian Yelich","Milwaukee Brewers",F),("CPA-DA","Dalton Rushing","Los Angeles Dodgers",T),("CPA-DC","Dylan Crews","Washington Nationals",T),("CPA-DE","Dennis Eckersley","Boston Red Sox",F),("CPA-DF","David Festa","Minnesota Twins",T),("CPA-DG","Dwight Gooden","New York Mets",F),
("CPA-DH","DJ Herz","Washington Nationals",T),("CPA-DJ","Derek Jeter","New York Yankees",F),("CPA-DJU","David Justice","Atlanta Braves",F),("CPA-DO","Chase Dollander","Colorado Rockies",T),("CPA-DR","Drew Romo","Colorado Rockies",T),("CPA-DS","Darryl Strawberry","New York Mets",F),("CPA-DSCH","Daniel Schneemann","Cleveland Guardians",T),("CPA-DT","Drew Thorpe","Chicago White Sox",T),("CPA-EC","Evan Carter","Texas Rangers",F),("CPA-FL","Fred Lynn","Boston Red Sox",F),
("CPA-FLI","Francisco Lindor","New York Mets",F),("CPA-FT","Frank Thomas","Chicago White Sox",F),("CPA-GB","George Brett","Kansas City Royals",F),("CPA-GG","Gordon Graceffo","St. Louis Cardinals",T),("CPA-GH","Gunnar Henderson","Baltimore Orioles",F),("CPA-GJ","Greg Jones","Colorado Rockies",T),("CPA-GRC","Griffin Conine","Miami Marlins",T),("CPA-HB","Harrison Bader","New York Mets",F),("CPA-HK","Hyeseong Kim","Los Angeles Dodgers",T),("CPA-HR","Hanley Ramirez","Florida Marlins",F),
("CPA-HW","Hurston Waldrep","Atlanta Braves",T),("CPA-I","Ichiro","Seattle Mariners",F),("CPA-IH","Ian Happ","Chicago Cubs",F),("CPA-JA","Julian Aguiar","Cincinnati Reds",T),("CPA-JB","Jordan Beck","Colorado Rockies",F),("CPA-JBA","Jeff Bagwell","Houston Astros",F),("CPA-JBL","Jake Bloss","Toronto Blue Jays",T),("CPA-JC","Jackson Chourio","Milwaukee Brewers",F),("CPA-JCA","Joe Carter","Toronto Blue Jays",F),("CPA-JCM","Junior Caminero","Tampa Bay Rays",F),
("CPA-JD","Jasson Dominguez","New York Yankees",F),("CPA-JDU","Jarren Duran","Boston Red Sox",F),("CPA-JE","Jim Edmonds","California Angels",F),("CPA-JG","Juan Gonzalez","Texas Rangers",F),("CPA-JH","Jackson Holliday","Baltimore Orioles",F),("CPA-JJ","Jace Jung","Detroit Tigers",T),("CPA-JJO","Jackson Jobe","Detroit Tigers",T),("CPA-JK","John Kruk","Philadelphia Phillies",F),("CPA-JKO","Jack Kochanowicz","Los Angeles Angels",T),("CPA-JL","Joey Loperfido","Toronto Blue Jays",F),
("CPA-JMA","Justyn-Henry Malloy","Detroit Tigers",T),("CPA-JN","Jhonkensy Noel","Cleveland Guardians",T),("CPA-JNE","Jack Neely","Chicago Cubs",T),("CPA-JOB","Johnny Bench","Cincinnati Reds",F),("CPA-JR","Julio Rodriguez","Seattle Mariners",F),("CPA-JRA","Jose Ramirez","Cleveland Guardians",F),("CPA-JRO","Jimmy Rollins","Philadelphia Phillies",F),("CPA-JS","Juan Soto","New York Mets",F),("CPA-JW","James Wood","Washington Nationals",T),("CPA-JWI","Jacob Wilson","Oakland Athletics",T),
("CPA-JWR","Justin Wrobleski","Los Angeles Dodgers",T),("CPA-KAL","Kevin Alcantara","Chicago Cubs",T),("CPA-KC","Kristian Campbell","Boston Red Sox",T),("CPA-KG","Ken Griffey Jr.","Seattle Mariners",F),("CPA-KH","Ke'Bryan Hayes","Cincinnati Reds",F),("CPA-KM","Kyle Manzardo","Cleveland Guardians",F),("CPA-KMO","Keider Montero","Detroit Tigers",T),("CPA-KT","Kyle Tucker","Chicago Cubs",F),("CPA-KU","Nick Kurtz","Oakland Athletics",T),("CPA-LAC","Luisangel Acuna","New York Mets",T),
("CPA-LEJ","Levi Jordan","Cincinnati Reds",T),("CPA-LG","Luis Gil","New York Yankees",F),("CPA-LJ","Leo Jimenez","Toronto Blue Jays",T),("CPA-LN","Lars Nootbaar","St. Louis Cardinals",F),("CPA-MA","Matt Shaw","Chicago Cubs",T),("CPA-MB","Mark Buehrle","Chicago White Sox",F),("CPA-MH","Michael Harris II","Atlanta Braves",F),("CPA-MM","Manny Machado","San Diego Padres",F),("CPA-MMA","Marcelo Mayer","Boston Red Sox",T),("CPA-MMC","Michael McGreevy","St. Louis Cardinals",T),
("CPA-MME","Michael Mercado","Philadelphia Phillies",T),("CPA-MOZ","Marcell Ozuna","Atlanta Braves",F),("CPA-MSC","Mike Schmidt","Philadelphia Phillies",F),("CPA-MT","Mike Trout","Los Angeles Angels",F),("CPA-MW","Masyn Winn","St. Louis Cardinals",F),("CPA-MY","Michael Young","Texas Rangers",F),("CPA-NA","Nolan Arenado","St. Louis Cardinals",F),("CPA-NAL","Nacho Alvarez Jr.","Atlanta Braves",T),("CPA-NK","Niko Kavadas","Los Angeles Angels",T),("CPA-NL","Nathaniel Lowe","Washington Nationals",F),
("CPA-NR","Nolan Ryan","Texas Rangers",F),("CPA-OH","Orlando Hernandez","New York Yankees",F),("CPA-OM","Orelvis Martinez","Toronto Blue Jays",T),("CPA-PA","Pete Alonso","New York Mets",F),("CPA-PC","Pete Crow-Armstrong","Chicago Cubs",F),("CPA-PG","Paul Goldschmidt","New York Yankees",F),("CPA-PK","Paul Konerko","Chicago White Sox",F),("CPA-PM","Paul Molitor","Minnesota Twins",F),("CPA-PS","Paul Skenes","Pittsburgh Pirates",F),("CPA-RA","Ronald Acuna Jr.","Atlanta Braves",F),
("CPA-RB","Ronel Blanco","Houston Astros",F),("CPA-RBL","Ryan Bliss","Seattle Mariners",T),("CPA-RF","Rafael Furcal","Atlanta Braves",F),("CPA-RH","Rece Hinds","Cincinnati Reds",T),("CPA-RJ","Randy Johnson","Arizona Diamondbacks",F),("CPA-RL","Rhett Lowder","Cincinnati Reds",T),("CPA-RR","River Ryan","Los Angeles Dodgers",T),("CPA-RS","Roki Sasaki","Los Angeles Dodgers",T),("CPA-RY","Robin Yount","Milwaukee Brewers",F),("CPA-RZ","Ryan Zimmerman","Washington Nationals",F),
("CPA-SB","Steward Berroa","Toronto Blue Jays",T),("CPA-SF","Sal Frelick","Milwaukee Brewers",F),("CPA-SGA","Steve Garvey","Los Angeles Dodgers",F),("CPA-SI","Shota Imanaga","Chicago Cubs",F),("CPA-SM","Shane McClanahan","Tampa Bay Rays",F),("CPA-SR","Scott Rolen","Philadelphia Phillies",F),("CPA-SS","Spencer Steer","Cincinnati Reds",F),("CPA-SSC","Spencer Schwellenbach","Atlanta Braves",T),("CPA-SW","Shay Whitcomb","Houston Astros",T),("CPA-TH","Trevor Hoffman","San Diego Padres",F),
("CPA-TL","Tyler Locklear","Seattle Mariners",T),("CPA-TM","Ty Madden","Detroit Tigers",T),("CPA-TP","Tyler Phillips","Philadelphia Phillies",T),("CPA-TSA","Thomas Saggese","St. Louis Cardinals",T),("CPA-TSI","Ted Simmons","St. Louis Cardinals",F),("CPA-TSO","Tyler Soderstrom","Oakland Athletics",F),("CPA-TSW","Trey Sweeney","Detroit Tigers",T),("CPA-TT","Trea Turner","Philadelphia Phillies",F),("CPA-VB","Valente Bellozo","Miami Marlins",T),("CPA-VG","Vladimir Guerrero Jr.","Toronto Blue Jays",F),
("CPA-WA","Wilyer Abreu","Boston Red Sox",F),("CPA-WL","Wyatt Langford","Texas Rangers",F),("CPA-WW","Will Wagner","Toronto Blue Jays",T),("CPA-WWA","Will Warren","New York Yankees",T),("CPA-YD","Yilber Diaz","Arizona Diamondbacks",T),("CPA-YM","Yuki Matsui","San Diego Padres",F),("CPA-YY","Yoshinobu Yamamoto","Los Angeles Dodgers",F),("CPA-ZEM","Zebby Matthews","Minnesota Twins",T),
]
ac(cpa_id, cpa_cards)
print(f"  Chrome Platinum Autographs: {len(cpa_cards)} cards, {len(cpa_pars)} parallels")

# ═══ 1955 CITY VARIATIONS AUTOGRAPHS (92 cards, all /5) ════════════════════
cva_id = ais("1955 Topps City Variations Chrome Packs Autographs", is_auto=True)
ap(cva_id, [("Base",5),("SuperFractor",1)])

cva_cards = [
("55CVA-AB","Adrian Beltre","Texas Rangers",F),("55CVA-AD","Andre Dawson","Montreal Expos",F),("55CVA-AJ","Aaron Judge","New York Yankees",F),("55CVA-AP","Albert Pujols","St. Louis Cardinals",F),("55CVA-AR","Austin Riley","Atlanta Braves",F),("55CVA-ARO","Alex Rodriguez","Texas Rangers",F),("55CVA-ARU","Adley Rutschman","Baltimore Orioles",F),("55CVA-BB","Barry Bonds","San Francisco Giants",F),("55CVA-BH","Bryce Harper","Philadelphia Phillies",F),("55CVA-BJ","Bo Jackson","Kansas City Royals",F),
("55CVA-BL","Barry Larkin","Cincinnati Reds",F),("55CVA-BP","Buster Posey","San Francisco Giants",F),("55CVA-BR","Ben Rice","New York Yankees",T),("55CVA-BW","Bobby Witt Jr.","Kansas City Royals",F),("55CVA-CB","Cody Bellinger","New York Yankees",F),("55CVA-CC","Corbin Carroll","Arizona Diamondbacks",F),("55CVA-CJ","Chipper Jones","Atlanta Braves",F),("55CVA-CK","Clayton Kershaw","Los Angeles Dodgers",F),("55CVA-CR","Cal Ripken Jr.","Baltimore Orioles",F),("55CVA-CU","Chase Utley","Philadelphia Phillies",F),
("55CVA-CYE","Christian Yelich","Milwaukee Brewers",F),("55CVA-DC","Dylan Crews","Washington Nationals",T),("55CVA-DJ","Derek Jeter","New York Yankees",F),("55CVA-DM","Dale Murphy","Atlanta Braves",F),("55CVA-DO","David Ortiz","Boston Red Sox",F),("55CVA-DST","Darryl Strawberry","New York Mets",F),("55CVA-DW","David Wright","New York Mets",F),("55CVA-DWI","Dave Winfield","New York Yankees",F),("55CVA-EM","Eddie Murray","Baltimore Orioles",F),("55CVA-EMA","Edgar Martinez","Seattle Mariners",F),
("55CVA-FL","Francisco Lindor","New York Mets",F),("55CVA-FM","Fred McGriff","Atlanta Braves",F),("55CVA-FT","Frank Thomas","Chicago White Sox",F),("55CVA-FTA","Fernando Tatis Jr.","San Diego Padres",F),("55CVA-GB","George Brett","Kansas City Royals",F),("55CVA-GH","Gunnar Henderson","Baltimore Orioles",F),("55CVA-GM","Greg Maddux","Atlanta Braves",F),("55CVA-GS","Gary Sheffield","Florida Marlins",F),("55CVA-HN","Hideo Nomo","Los Angeles Dodgers",F),("55CVA-I","Ichiro","Seattle Mariners",F),
("55CVA-IR","Ivan Rodriguez","Detroit Tigers",F),("55CVA-JA","Jose Altuve","Houston Astros",F),("55CVA-JB","Johnny Bench","Cincinnati Reds",F),("55CVA-JBA","Jeff Bagwell","Houston Astros",F),("55CVA-JC","Jackson Chourio","Milwaukee Brewers",F),("55CVA-JD","Johnny Damon","Boston Red Sox",F),("55CVA-JH","Jackson Holliday","Baltimore Orioles",F),("55CVA-JP","Jorge Posada","New York Yankees",F),("55CVA-JR","Jose Ramirez","Cleveland Guardians",F),("55CVA-JRO","Julio Rodriguez","Seattle Mariners",F),
("55CVA-JS","Juan Soto","New York Mets",F),("55CVA-JT","Joe Torre","New York Yankees",F),("55CVA-JW","James Wood","Washington Nationals",T),("55CVA-KG","Ken Griffey Jr.","Seattle Mariners",F),("55CVA-KT","Kyle Tucker","Chicago Cubs",F),("55CVA-LR","Luis Robert Jr.","Chicago White Sox",F),("55CVA-LW","Larry Walker","Colorado Rockies",F),("55CVA-MM","Marcelo Mayer","Boston Red Sox",T),("55CVA-MMA","Manny Machado","San Diego Padres",F),("55CVA-MMC","Mark McGwire","St. Louis Cardinals",F),
("55CVA-MP","Mike Piazza","New York Mets",F),("55CVA-MR","Mariano Rivera","New York Yankees",F),("55CVA-MS","Mike Schmidt","Philadelphia Phillies",F),("55CVA-MT","Mike Trout","Los Angeles Angels",F),("55CVA-NA","Nolan Arenado","St. Louis Cardinals",F),("55CVA-NR","Nolan Ryan","Texas Rangers",F),("55CVA-OA","Ozzie Albies","Atlanta Braves",F),("55CVA-OH","Orel Hershiser","Los Angeles Dodgers",F),("55CVA-OS","Ozzie Smith","San Diego Padres",F),("55CVA-PA","Pete Alonso","New York Mets",F),
("55CVA-PM","Paul Molitor","Minnesota Twins",F),("55CVA-PMA","Pedro Martinez","Montreal Expos",F),("55CVA-PS","Paul Skenes","Pittsburgh Pirates",F),("55CVA-RA","Ronald Acuna Jr.","Atlanta Braves",F),("55CVA-RC","Rod Carew","California Angels",F),("55CVA-RD","Rafael Devers","Boston Red Sox",F),("55CVA-RG","Riley Greene","Detroit Tigers",F),("55CVA-RJ","Randy Johnson","Arizona Diamondbacks",F),("55CVA-RJA","Reggie Jackson","Oakland Athletics",F),("55CVA-SA","Roki Sasaki","Los Angeles Dodgers",T),
("55CVA-SI","Shota Imanaga","Chicago Cubs",F),("55CVA-SK","Sandy Koufax","Brooklyn Dodgers",F),("55CVA-SO","Shohei Ohtani","Los Angeles Dodgers",F),("55CVA-SOH","Sadaharu Oh","Yomiuri Giants",F),("55CVA-SR","Scott Rolen","Philadelphia Phillies",F),("55CVA-TH","Torii Hunter","Minnesota Twins",F),("55CVA-VG","Vladimir Guerrero Jr.","Toronto Blue Jays",F),("55CVA-WB","Wade Boggs","Tampa Bay Devil Rays",F),("55CVA-WC","Will Clark","San Francisco Giants",F),("55CVA-WL","Wyatt Langford","Texas Rangers",F),
("55CVA-YM","Yadier Molina","St. Louis Cardinals",F),("55CVA-YY","Yoshinobu Yamamoto","Los Angeles Dodgers",F),
]
ac(cva_id, cva_cards)
print(f"  1955 City Variations Autographs: {len(cva_cards)} cards")

# ═══ BACKFILL IMAGE IDs ═════════════════════════════════════════════════════
db.commit()
updated = db.execute("""
    UPDATE players SET mlb_player_id = (SELECT p2.mlb_player_id FROM players p2 WHERE p2.name = players.name AND p2.mlb_player_id IS NOT NULL LIMIT 1)
    WHERE set_id = ? AND mlb_player_id IS NULL AND EXISTS (SELECT 1 FROM players p2 WHERE p2.name = players.name AND p2.mlb_player_id IS NOT NULL)
""", (SET_ID,)).rowcount
print(f"\nBackfilled {updated} MLB player IDs")

# ═══ SUMMARY ════════════════════════════════════════════════════════════════
db.commit()
tp = db.execute("SELECT COUNT(*) FROM players WHERE set_id = ?", (SET_ID,)).fetchone()[0]
ta = db.execute("SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets ins ON pa.insert_set_id = ins.id WHERE ins.set_id = ?", (SET_ID,)).fetchone()[0]
ts = db.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id = ?", (SET_ID,)).fetchone()[0]
tpar = db.execute("SELECT COUNT(*) FROM parallels p JOIN insert_sets ins ON p.insert_set_id = ins.id WHERE ins.set_id = ?", (SET_ID,)).fetchone()[0]

print(f"\n{'='*50}")
print(f"Set ID: {SET_ID}")
print(f"Total subsets: {ts}")
print(f"Total unique athletes: {tp}")
print(f"Total card appearances: {ta}")
print(f"Total parallels: {tpar}")
print(f"Expected: 970 cards")
db.close()
print("Done!")
