"""
Parser for 2025 Topps Stadium Club Baseball.

sport: Baseball, league: MLB, season: 2025, tier: Standard
RC-tagged players: strip " RC" from name, set is_rookie=True.
Dual Autographs use co_players logic (same card_number in same insert_set).
All parallels have print_run=null.
"""

from __future__ import annotations
import json


SET_NAME = "2025 Topps Stadium Club Baseball"
SPORT = "Baseball"
SEASON = "2025"
LEAGUE = "MLB"


def parse_rc(name: str) -> tuple[str, bool]:
    """Strip ' RC' suffix and return (clean_name, is_rookie)."""
    if name.endswith(" RC"):
        return name[:-3].strip(), True
    return name, False


def make_parallels(names: list[str]) -> list[dict]:
    return [{"name": n, "print_run": None} for n in names]


# ── Card data ─────────────────────────────────────────────────────────────────

# Base Set (200 cards)
BASE_SET_RAW = [
    ("1", "Frank Thomas", "Chicago White Sox"),
    ("2", "Joey Votto", "Cincinnati Reds"),
    ("3", "Michael Busch", "Chicago Cubs"),
    ("4", "Ronald Acuna Jr.", "Atlanta Braves"),
    ("5", "Matt Olson", "Atlanta Braves"),
    ("6", "Bobby Witt Jr.", "Kansas City Royals"),
    ("7", "Rafael Devers", "San Francisco Giants"),
    ("8", "Tomoyuki Sugano", "Baltimore Orioles RC"),
    ("9", "Nick Kurtz", "Athletics RC"),
    ("10", "Alex Bregman", "Boston Red Sox"),
    ("11", "Jose Ramirez", "Cleveland Guardians"),
    ("12", "Shane Bieber", "Toronto Blue Jays"),
    ("13", "Logan Henderson", "Milwaukee Brewers RC"),
    ("14", "Brent Rooker", "Athletics"),
    ("15", "Mark McGwire", "St. Louis Cardinals"),
    ("16", "Elly De La Cruz", "Cincinnati Reds"),
    ("17", "Moises Ballesteros", "Chicago Cubs RC"),
    ("18", "Garrett Crochet", "Boston Red Sox"),
    ("19", "Cal Ripken Jr.", "Baltimore Orioles"),
    ("20", "Nomar Garciaparra", "Boston Red Sox"),
    ("21", "Josh Naylor", "Seattle Mariners"),
    ("22", "Luis Gonzalez", "Arizona Diamondbacks"),
    ("23", "Brenton Doyle", "Colorado Rockies"),
    ("24", "Cade Horton", "Chicago Cubs RC"),
    ("25", "Chase Meidroth", "Chicago White Sox RC"),
    ("26", "Yainer Diaz", "Houston Astros"),
    ("27", "Barry Larkin", "Cincinnati Reds"),
    ("28", "Max Muncy", "Athletics RC"),
    ("29", "Christian Walker", "Houston Astros"),
    ("30", "Salvador Perez", "Kansas City Royals"),
    ("31", "Denzel Clarke", "Athletics RC"),
    ("32", "Mike Trout", "Los Angeles Angels"),
    ("33", "Jacob Wilson", "Athletics RC"),
    ("34", "Kristian Campbell", "Boston Red Sox RC"),
    ("35", "Cole Ragans", "Kansas City Royals"),
    ("36", "Larry Walker", "Colorado Rockies"),
    ("37", "Zach Neto", "Los Angeles Angels"),
    ("38", "Gleyber Torres", "Detroit Tigers"),
    ("39", "Matt McLain", "Cincinnati Reds"),
    ("40", "Ozzie Albies", "Atlanta Braves"),
    ("41", "Adael Amador", "Colorado Rockies RC"),
    ("42", "Chase Dollander", "Colorado Rockies RC"),
    ("43", "Andrew Benintendi", "Chicago White Sox"),
    ("44", "Jon Berti", "Chicago Cubs"),
    ("45", "Adley Rutschman", "Baltimore Orioles"),
    ("46", "Sammy Sosa", "Chicago Cubs"),
    ("47", "Jace Jung", "Detroit Tigers RC"),
    ("48", "Shota Imanaga", "Chicago Cubs"),
    ("49", "Luis Severino", "Athletics"),
    ("50", "Jackson Jobe", "Detroit Tigers RC"),
    ("51", "Ketel Marte", "Arizona Diamondbacks"),
    ("52", "Logan Evans", "Seattle Mariners RC"),
    ("53", "Paul Konerko", "Chicago White Sox"),
    ("54", "Caden Dana", "Los Angeles Angels RC"),
    ("55", "Miguel Cabrera", "Detroit Tigers"),
    ("56", "Steven Kwan", "Cleveland Guardians"),
    ("57", "Luke Keaschall", "Minnesota Twins RC"),
    ("58", "Shohei Ohtani", "Los Angeles Dodgers"),
    ("59", "Chase Petty", "Cincinnati Reds RC"),
    ("60", "Cam Smith", "Houston Astros RC"),
    ("61", "Drake Baldwin", "Atlanta Braves RC"),
    ("62", "Coby Mayo", "Baltimore Orioles RC"),
    ("63", "Seiya Suzuki", "Chicago Cubs"),
    ("64", "Justyn-Henry Malloy", "Detroit Tigers RC"),
    ("65", "Matt Shaw", "Chicago Cubs RC"),
    ("66", "Edgar Quero", "Chicago White Sox RC"),
    ("67", "Tarik Skubal", "Detroit Tigers"),
    ("68", "Ezequiel Tovar", "Colorado Rockies"),
    ("69", "David Ortiz", "Boston Red Sox"),
    ("70", "Clayton Kershaw", "Los Angeles Dodgers"),
    ("71", "Greg Maddux", "Atlanta Braves"),
    ("72", "Austin Riley", "Atlanta Braves"),
    ("73", "Jackson Holliday", "Baltimore Orioles"),
    ("74", "Marcelo Mayer", "Boston Red Sox RC"),
    ("75", "Yordan Alvarez", "Houston Astros"),
    ("76", "Riley Greene", "Detroit Tigers"),
    ("77", "Kyle Tucker", "Chicago Cubs"),
    ("78", "Lawrence Butler", "Athletics"),
    ("79", "Nolan Ryan", "Houston Astros"),
    ("80", "Zac Gallen", "Arizona Diamondbacks"),
    ("81", "Michael Harris II", "Atlanta Braves"),
    ("82", "Kyle Manzardo", "Cleveland Guardians"),
    ("83", "Corbin Carroll", "Arizona Diamondbacks"),
    ("84", "Chipper Jones", "Atlanta Braves"),
    ("85", "Pedro Martinez", "Boston Red Sox"),
    ("86", "Pete Crow-Armstrong", "Chicago Cubs"),
    ("87", "Luis Robert Jr.", "Chicago White Sox"),
    ("88", "Nolan Schanuel", "Los Angeles Angels"),
    ("89", "Craig Biggio", "Houston Astros"),
    ("90", "Spencer Strider", "Atlanta Braves"),
    ("91", "Kevin Alcantara", "Chicago Cubs RC"),
    ("92", "Hunter Greene", "Cincinnati Reds"),
    ("93", "Spencer Schwellenbach", "Atlanta Braves"),
    ("94", "Jordan Westburg", "Baltimore Orioles"),
    ("95", "Rhett Lowder", "Cincinnati Reds RC"),
    ("96", "Gunnar Henderson", "Baltimore Orioles"),
    ("97", "Jose Altuve", "Houston Astros"),
    ("98", "Grayson Rodriguez", "Baltimore Orioles"),
    ("99", "George Brett", "Kansas City Royals"),
    ("100", "Corbin Burnes", "Arizona Diamondbacks"),
    ("101", "Ryan Zimmerman", "Washington Nationals"),
    ("102", "Dylan Crews", "Washington Nationals RC"),
    ("103", "Chandler Simpson", "Tampa Bay Rays RC"),
    ("104", "Giancarlo Stanton", "New York Yankees"),
    ("105", "Paul Skenes", "Pittsburgh Pirates"),
    ("106", "Adolis Garcia", "Texas Rangers"),
    ("107", "Xavier Edwards", "Miami Marlins"),
    ("108", "Agustin Ramirez", "Miami Marlins RC"),
    ("109", "Jackson Merrill", "San Diego Padres"),
    ("110", "Evan Longoria", "Tampa Bay Rays"),
    ("111", "Cody Bellinger", "New York Yankees"),
    ("112", "Willy Adames", "San Francisco Giants"),
    ("113", "Royce Lewis", "Minnesota Twins"),
    ("114", "Zack Wheeler", "Philadelphia Phillies"),
    ("115", "Luisangel Acuna", "New York Mets RC"),
    ("116", "Corey Seager", "Texas Rangers"),
    ("117", "Dylan Cease", "San Diego Padres"),
    ("118", "Jung Hoo Lee", "San Francisco Giants"),
    ("119", "Albert Pujols", "St. Louis Cardinals"),
    ("120", "Sandy Alcantara", "Miami Marlins"),
    ("121", "Max Fried", "New York Yankees"),
    ("122", "Yu Darvish", "San Diego Padres"),
    ("123", "Francisco Alvarez", "New York Mets"),
    ("124", "Bo Bichette", "Toronto Blue Jays"),
    ("125", "Will Smith", "Los Angeles Dodgers"),
    ("126", "Bryce Harper", "Philadelphia Phillies"),
    ("127", "Nolan Arenado", "St. Louis Cardinals"),
    ("128", "Michael King", "San Diego Padres"),
    ("129", "Mark Vientos", "New York Mets"),
    ("130", "Alex Rodriguez", "Texas Rangers"),
    ("131", "Eury Perez", "Miami Marlins"),
    ("132", "Trea Turner", "Philadelphia Phillies"),
    ("133", "Buster Posey", "San Francisco Giants"),
    ("134", "George Kirby", "Seattle Mariners"),
    ("135", "Ken Griffey Jr.", "Seattle Mariners"),
    ("136", "Max Scherzer", "Toronto Blue Jays"),
    ("137", "Marcus Semien", "Texas Rangers"),
    ("138", "Jackson Chourio", "Milwaukee Brewers"),
    ("139", "Aaron Judge", "New York Yankees"),
    ("140", "Gerrit Cole", "New York Yankees"),
    ("141", "Brooks Lee", "Minnesota Twins RC"),
    ("142", "Caleb Durbin", "Milwaukee Brewers RC"),
    ("143", "Anthony Santander", "Toronto Blue Jays"),
    ("144", "Kodai Senga", "New York Mets"),
    ("145", "Aaron Nola", "Philadelphia Phillies"),
    ("146", "Junior Caminero", "Tampa Bay Rays"),
    ("147", "Luis Castillo", "Seattle Mariners"),
    ("148", "Ryan Howard", "Philadelphia Phillies"),
    ("149", "Connor Norby", "Miami Marlins RC"),
    ("150", "William Contreras", "Milwaukee Brewers"),
    ("151", "Shane McClanahan", "Tampa Bay Rays"),
    ("152", "Juan Soto", "New York Mets"),
    ("153", "Byron Buxton", "Minnesota Twins"),
    ("154", "Dalton Rushing", "Los Angeles Dodgers RC"),
    ("155", "Pete Alonso", "New York Mets"),
    ("156", "Mike Piazza", "New York Mets"),
    ("157", "Thomas Saggese", "St. Louis Cardinals RC"),
    ("158", "Logan Gilbert", "Seattle Mariners"),
    ("159", "Mick Abel", "Philadelphia Phillies RC"),
    ("160", "Mookie Betts", "Los Angeles Dodgers"),
    ("161", "Prince Fielder", "Milwaukee Brewers"),
    ("162", "Justin Verlander", "San Francisco Giants"),
    ("163", "Ben Williamson", "Seattle Mariners RC"),
    ("164", "Jazz Chisholm Jr.", "New York Yankees"),
    ("165", "Sonny Gray", "St. Louis Cardinals"),
    ("166", "Andrew McCutchen", "Pittsburgh Pirates"),
    ("167", "Matt Chapman", "San Francisco Giants"),
    ("168", "Freddie Freeman", "Los Angeles Dodgers"),
    ("169", "Oneil Cruz", "Pittsburgh Pirates"),
    ("170", "Randy Arozarena", "Seattle Mariners"),
    ("171", "Christian Yelich", "Milwaukee Brewers"),
    ("172", "Derek Jeter", "New York Yankees"),
    ("173", "Chase Utley", "Philadelphia Phillies"),
    ("174", "Vladimir Guerrero Jr.", "Toronto Blue Jays"),
    ("175", "James Wood", "Washington Nationals RC"),
    ("176", "Jimmy Rollins", "Philadelphia Phillies"),
    ("177", "Joe Mauer", "Minnesota Twins"),
    ("178", "Mackenzie Gore", "Washington Nationals"),
    ("179", "Kumar Rocker", "Texas Rangers RC"),
    ("180", "Manny Machado", "San Diego Padres"),
    ("181", "Francisco Lindor", "New York Mets"),
    ("182", "Ichiro", "Seattle Mariners"),
    ("183", "Masyn Winn", "St. Louis Cardinals"),
    ("184", "Yoshinobu Yamamoto", "Los Angeles Dodgers"),
    ("185", "Julio Rodriguez", "Seattle Mariners"),
    ("186", "David Festa", "Minnesota Twins RC"),
    ("187", "Roki Sasaki", "Los Angeles Dodgers RC"),
    ("188", "CJ Abrams", "Washington Nationals"),
    ("189", "Wyatt Langford", "Texas Rangers"),
    ("190", "Braxton Ashcraft", "Pittsburgh Pirates RC"),
    ("191", "Fernando Tatis Jr.", "San Diego Padres"),
    ("192", "Trevor Hoffman", "San Diego Padres"),
    ("193", "Brice Turang", "Milwaukee Brewers"),
    ("194", "Jacob DeGrom", "Texas Rangers"),
    ("195", "Honus Wagner", "Pittsburgh Pirates"),
    ("196", "Ben Rice", "New York Yankees RC"),
    ("197", "Bryan Woo", "Seattle Mariners"),
    ("198", "Luis Arraez", "San Diego Padres"),
    ("199", "Johan Santana", "Minnesota Twins"),
    ("200", "Hyeseong Kim", "Los Angeles Dodgers RC"),
]

BASE_SET_PARALLELS = make_parallels([
    "Sepia", "Pink", "Light Blue", "Lime Green", "Red", "Bronze", "Blue",
    "Green", "Black And White", "Turquoise", "Members Only", "Gold",
    "Photographer's Proof", "Rainbow Foilboard", "Gold Rainbow Foilboard",
])

# Base Autographs (161 cards)
BASE_AUTO_RAW = [
    ("SCBA-AS", "Aaron Schunk", "Colorado Rockies"),
    ("SCBA-AMA", "Adam Mazur", "Miami Marlins"),
    ("SCBA-AD", "Adrian Del Castillo", "Arizona Diamondbacks"),
    ("SCBA-AB", "Alec Burleson", "St. Louis Cardinals"),
    ("SCBA-AGO", "Alex Gordon", "Kansas City Royals"),
    ("SCBA-AC", "Andres Chaparro", "Washington Nationals"),
    ("SCBA-AG", "Andres Gimenez", "Toronto Blue Jays"),
    ("SCBA-AW", "Andrew Walters", "Cleveland Guardians"),
    ("SCBA-ACH", "Angel Chivilli", "Colorado Rockies"),
    ("SCBA-AM", "Angel Martinez", "Cleveland Guardians"),
    ("SCBA-AV", "Anthony Volpe", "New York Yankees"),
    ("SCBA-BCO", "Bartolo Colon", "New York Mets"),
    ("SCBA-BCA", "Ben Casparius", "Los Angeles Dodgers"),
    ("SCBA-BR", "Ben Rice", "New York Yankees"),
    ("SCBA-BBL", "Bert Blyleven", "Minnesota Twins"),
    ("SCBA-BC", "Billy Cook", "Pittsburgh Pirates"),
    ("SCBA-BD", "Blake Dunn", "Cincinnati Reds"),
    ("SCBA-BBA", "Brady Basso", "Athletics"),
    ("SCBA-BCR", "Brandon Crawford", "San Francisco Giants"),
    ("SCBA-BLO", "Brandon Lockridge", "San Diego Padres"),
    ("SCBA-BWE", "Brandon Webb", "Arizona Diamondbacks"),
    ("SCBA-BH", "Brant Hurter", "Detroit Tigers"),
    ("SCBA-BRO", "Brian Roberts", "Baltimore Orioles"),
    ("SCBA-BB", "Brooks Baldwin", "Chicago White Sox"),
    ("SCBA-BL", "Brooks Lee", "Minnesota Twins"),
    ("SCBA-CP", "Cade Povich", "Baltimore Orioles"),
    ("SCBA-CD", "Caden Dana", "Los Angeles Angels"),
    ("SCBA-CRA", "Cal Raleigh", "Seattle Mariners"),
    ("SCBA-CR", "Carlos Rodriguez", "Milwaukee Brewers"),
    ("SCBA-CMU", "Cedric Mullins", "Baltimore Orioles"),
    ("SCBA-CSI", "Chandler Simpson", "Tampa Bay Rays"),
    ("SCBA-CMD", "Chayce McDermott", "Baltimore Orioles"),
    ("SCBA-CM", "Coby Mayo", "Baltimore Orioles"),
    ("SCBA-CCO", "Colton Cowser", "Baltimore Orioles"),
    ("SCBA-CN", "Connor Norby", "Miami Marlins"),
    ("SCBA-CME", "Cristian Mena", "Arizona Diamondbacks"),
    ("SCBA-DS", "Daniel Schneemann", "Cleveland Guardians"),
    ("SCBA-DB", "Darren Baker", "Washington Nationals"),
    ("SCBA-DK", "DaShawn Keirsey", "Minnesota Twins"),
    ("SCBA-DF", "David Festa", "Minnesota Twins"),
    ("SCBA-DE", "Dennis Eckersley", "Athletics"),
    ("SCBA-DD", "Dillon Dingler", "Detroit Tigers"),
    ("SCBA-DHE", "DJ Herz", "Washington Nationals"),
    ("SCBA-DG", "Doc Gooden", "New York Mets"),
    ("SCBA-DBA", "Drake Baldwin", "Atlanta Braves"),
    ("SCBA-DT", "Drew Thorpe", "Chicago White Sox"),
    ("SCBA-DH", "Dustin Harris", "Texas Rangers"),
    ("SCBA-DC", "Dylan Crews", "Washington Nationals"),
    ("SCBA-EM", "Edgar Martinez", "Seattle Mariners"),
    ("SCBA-EQ", "Edgar Quero", "Chicago White Sox"),
    ("SCBA-EH", "Edgardo Henriquez", "Los Angeles Dodgers"),
    ("SCBA-ED", "Eric Davis", "Cincinnati Reds"),
    ("SCBA-EG", "Eric Gagne", "Los Angeles Dodgers"),
    ("SCBA-ET", "Ezequiel Tovar", "Colorado Rockies"),
    ("SCBA-FP", "Freddy Peralta", "Milwaukee Brewers"),
    ("SCBA-GCR", "Garrett Crochet", "Boston Red Sox"),
    ("SCBA-GSH", "Gary Sheffield", "New York Yankees"),
    ("SCBA-GF", "George Foster", "Cincinnati Reds"),
    ("SCBA-GK", "George Kirby", "Seattle Mariners"),
    ("SCBA-GS", "George Springer", "Toronto Blue Jays"),
    ("SCBA-GH", "Grant Holmes", "Atlanta Braves"),
    ("SCBA-GJ", "Greg Jones", "Chicago White Sox"),
    ("SCBA-GM", "Grant McCray", "San Francisco Giants"),
    ("SCBA-GC", "Griffin Conine", "Miami Marlins"),
    ("SCBA-HB", "Hayden Birdsong", "San Francisco Giants"),
    ("SCBA-HF", "Hunter Feduccia", "Los Angeles Dodgers"),
    ("SCBA-HW", "Hurston Waldrep", "Atlanta Braves"),
    ("SCBA-HK", "Hyeseong Kim", "Los Angeles Dodgers"),
    ("SCBA-IH", "Ian Happ", "Chicago Cubs"),
    ("SCBA-IC", "Isaac Collins", "Milwaukee Brewers"),
    ("SCBA-JJ", "Jace Jung", "Detroit Tigers"),
    ("SCBA-JK", "Jack Kochanowicz", "Los Angeles Angels"),
    ("SCBA-JJO", "Jackson Jobe", "Detroit Tigers"),
    ("SCBA-JWI", "Jacob Wilson", "Athletics"),
    ("SCBA-JY", "Jacob Young", "Washington Nationals"),
    ("SCBA-JB", "Jake Bloss", "Toronto Blue Jays"),
    ("SCBA-JE", "Jake Eder", "Los Angeles Angels"),
    ("SCBA-JW", "James Wood", "Washington Nationals"),
    ("SCBA-JS", "Javier Sanoja", "Miami Marlins"),
    ("SCBA-JBU", "Jay Buhner", "Seattle Mariners"),
    ("SCBA-JWE", "Jayson Werth", "Philadelphia Phillies"),
    ("SCBA-JLU", "Jesus Luzardo", "Philadelphia Phillies"),
    ("SCBA-JN", "Jhonkensy Noel", "Cleveland Guardians"),
    ("SCBA-JED", "Jim Edmonds", "St. Louis Cardinals"),
    ("SCBA-JPA", "Jim Palmer", "Baltimore Orioles"),
    ("SCBA-JC", "Joey Cantillo", "Cleveland Guardians"),
    ("SCBA-JKR", "John Kruk", "Philadelphia Phillies"),
    ("SCBA-JP", "Jorge Posada", "New York Yankees"),
    ("SCBA-JR", "Jose Reyes", "New York Mets"),
    ("SCBA-JGO", "Juan Gonzalez", "Texas Rangers"),
    ("SCBA-KM", "Keider Montero", "Detroit Tigers"),
    ("SCBA-KG", "Ken Griffey Sr.", "Cincinnati Reds"),
    ("SCBA-KC", "Kerry Carpenter", "Detroit Tigers"),
    ("SCBA-KA", "Kevin Alcantara", "Chicago Cubs"),
    ("SCBA-KB", "Ky Bush", "Chicago White Sox"),
    ("SCBA-KMA", "Kyle Manzardo", "Cleveland Guardians"),
    ("SCBA-LH", "Logan Henderson", "Milwaukee Brewers"),
    ("SCBA-LG", "Luis Gil", "New York Yankees"),
    ("SCBA-LGO", "Luis Gonzalez", "Arizona Diamondbacks"),
    ("SCBA-LP", "Luis Peralta", "Colorado Rockies"),
    ("SCBA-LA", "Luisangel Acuna", "New York Mets"),
    ("SCBA-MMA", "Marcelo Mayer", "Boston Red Sox"),
    ("SCBA-MS", "Marcus Semien", "Texas Rangers"),
    ("SCBA-MT", "Mark Teixeira", "New York Yankees"),
    ("SCBA-MMO", "Mason Montgomery", "Tampa Bay Rays"),
    ("SCBA-MM", "Michael McGreevy", "St. Louis Cardinals"),
    ("SCBA-MY", "Michael Young", "Texas Rangers"),
    ("SCBA-NA", "Nacho Alvarez Jr.", "Atlanta Braves"),
    ("SCBA-NE", "Nathan Eovaldi", "Texas Rangers"),
    ("SCBA-NGO", "Nick Gonzales", "Pittsburgh Pirates"),
    ("SCBA-NSO", "Nick Sogard", "Boston Red Sox"),
    ("SCBA-NY", "Nick Yorke", "Pittsburgh Pirates"),
    ("SCBA-NH", "Nico Hoerner", "Chicago Cubs"),
    ("SCBA-NK", "Niko Kavadas", "Los Angeles Angels"),
    ("SCBA-NS", "Nolan Schanuel", "Los Angeles Angels"),
    ("SCBA-OM", "Orelvis Martinez", "Toronto Blue Jays"),
    ("SCBA-OA", "Ozzie Albies", "Atlanta Braves"),
    ("SCBA-OS", "Ozzie Smith", "St. Louis Cardinals"),
    ("SCBA-PK", "Paul Konerko", "Chicago White Sox"),
    ("SCBA-PL", "Pedro Leon", "Houston Astros"),
    ("SCBA-RD", "R.A. Dickey", "New York Mets"),
    ("SCBA-RFU", "Rafael Furcal", "Atlanta Braves"),
    ("SCBA-RL", "Rhett Lowder", "Cincinnati Reds"),
    ("SCBA-RF", "Richard Fitts", "Boston Red Sox"),
    ("SCBA-RR", "River Ryan", "Los Angeles Dodgers"),
    ("SCBA-RS", "Roki Sasaki", "Los Angeles Dodgers"),
    ("SCBA-RG", "Ron Guidry", "New York Yankees"),
    ("SCBA-RB", "Ryan Bliss", "Seattle Mariners"),
    ("SCBA-RHW", "Ryan Howard", "Philadelphia Phillies"),
    ("SCBA-RZ", "Ryan Zimmerman", "Washington Nationals"),
    ("SCBA-SF", "Sal Frelick", "Milwaukee Brewers"),
    ("SCBA-SA", "Sam Aldegheri", "Los Angeles Angels"),
    ("SCBA-SBU", "Sean Burke", "Chicago White Sox"),
    ("SCBA-SJ", "Seth Johnson", "Philadelphia Phillies"),
    ("SCBA-SL", "Seth Lugo", "Kansas City Royals"),
    ("SCBA-SM", "Shane McClanahan", "Tampa Bay Rays"),
    ("SCBA-SG", "Shawn Green", "Toronto Blue Jays"),
    ("SCBA-SW", "Shay Whitcomb", "Houston Astros"),
    ("SCBA-SS", "Spencer Schwellenbach", "Atlanta Braves"),
    ("SCBA-SST", "Spencer Steer", "Cincinnati Reds"),
    ("SCBA-SK", "Steven Kwan", "Cleveland Guardians"),
    ("SCBA-THA", "Thomas Harrington", "Pittsburgh Pirates"),
    ("SCBA-TS", "Thomas Saggese", "St. Louis Cardinals"),
    ("SCBA-TGE", "Tom Glavine", "Atlanta Braves"),
    ("SCBA-TE", "Tommy Edman", "Los Angeles Dodgers"),
    ("SCBA-THU", "Torii Hunter", "Minnesota Twins"),
    ("SCBA-TH", "Trevor Hoffman", "San Diego Padres"),
    ("SCBA-TSW", "Trey Sweeney", "Detroit Tigers"),
    ("SCBA-TM", "Ty Madden", "Detroit Tigers"),
    ("SCBA-TG", "Tyler Gentry", "Kansas City Royals"),
    ("SCBA-TL", "Tyler Locklear", "Seattle Mariners"),
    ("SCBA-TP", "Tyler Phillips", "Miami Marlins"),
    ("SCBA-VB", "Valente Bellozo", "Miami Marlins"),
    ("SCBA-VW", "Vernon Wells", "Toronto Blue Jays"),
    ("SCBA-VM", "Victor Martinez", "Detroit Tigers"),
    ("SCBA-WCL", "Will Clark", "Texas Rangers"),
    ("SCBA-WW", "Will Wagner", "Toronto Blue Jays"),
    ("SCBA-WWA", "Will Warren", "New York Yankees"),
    ("SCBA-YDI", "Yainer Diaz", "Houston Astros"),
    ("SCBA-YD", "Yilber Diaz", "Arizona Diamondbacks"),
    ("SCBA-ZD", "Zach Dezenzo", "Houston Astros"),
]

BASE_AUTO_PARALLELS = make_parallels([
    "Yellow", "Turquoise", "Gold", "Rainbow Foilboard", "Green", "Gold Rainbow Foil",
])

# Chrome Autographs (73 cards)
CHROME_AUTO_RAW = [
    ("SCCA-AJ", "Aaron Judge", "New York Yankees"),
    ("SCCA-AM", "Andrew McCutchen", "Pittsburgh Pirates"),
    ("SCCA-AP", "Albert Pujols", "St. Louis Cardinals"),
    ("SCCA-ARA", "Agustin Ramirez", "Miami Marlins"),
    ("SCCA-ARU", "Adley Rutschman", "Baltimore Orioles"),
    ("SCCA-BB", "Barry Bonds", "San Francisco Giants"),
    ("SCCA-BL", "Brooks Lee", "Minnesota Twins"),
    ("SCCA-BLA", "Barry Larkin", "Cincinnati Reds"),
    ("SCCA-BR", "Ben Rice", "New York Yankees"),
    ("SCCA-BW", "Bobby Witt Jr.", "Kansas City Royals"),
    ("SCCA-CD", "Caden Dana", "Los Angeles Angels"),
    ("SCCA-CDO", "Chase Dollander", "Colorado Rockies"),
    ("SCCA-CH", "Cade Horton", "Chicago Cubs"),
    ("SCCA-CK", "Clayton Kershaw", "Los Angeles Dodgers"),
    ("SCCA-CM", "Coby Mayo", "Baltimore Orioles"),
    ("SCCA-CN", "Connor Norby", "Miami Marlins"),
    ("SCCA-CP", "Cade Povich", "Baltimore Orioles"),
    ("SCCA-CSM", "Cam Smith", "Houston Astros"),
    ("SCCA-CU", "Chase Utley", "Philadelphia Phillies"),
    ("SCCA-DC", "Dylan Crews", "Washington Nationals"),
    ("SCCA-DJ", "Derek Jeter", "New York Yankees"),
    ("SCCA-DR", "Dalton Rushing", "Los Angeles Dodgers"),
    ("SCCA-DS", "Darryl Strawberry", "New York Mets"),
    ("SCCA-ED", "Elly De La Cruz", "Cincinnati Reds"),
    ("SCCA-FH", "Felix Hernandez", "Seattle Mariners"),
    ("SCCA-FL", "Francisco Lindor", "New York Mets"),
    ("SCCA-FT", "Fernando Tatis Jr.", "San Diego Padres"),
    ("SCCA-GB", "George Brett", "Kansas City Royals"),
    ("SCCA-GHO", "Grant Holmes", "Atlanta Braves"),
    ("SCCA-HK", "Hyeseong Kim", "Los Angeles Dodgers"),
    ("SCCA-I", "Ichiro", "Seattle Mariners"),
    ("SCCA-IR", "Ivan Rodriguez", "Texas Rangers"),
    ("SCCA-JB", "Johnny Bench", "Cincinnati Reds"),
    ("SCCA-JC", "Jackson Chourio", "Milwaukee Brewers"),
    ("SCCA-JD", "Jasson Dominguez", "New York Yankees"),
    ("SCCA-JJ", "Jace Jung", "Detroit Tigers"),
    ("SCCA-JJO", "Jackson Jobe", "Detroit Tigers"),
    ("SCCA-JN", "Jhonkensy Noel", "Cleveland Guardians"),
    ("SCCA-JR", "Julio Rodriguez", "Seattle Mariners"),
    ("SCCA-JRO", "Jimmy Rollins", "Philadelphia Phillies"),
    ("SCCA-JS", "Juan Soto", "New York Mets"),
    ("SCCA-JSA", "Johan Santana", "Minnesota Twins"),
    ("SCCA-JW", "James Wood", "Washington Nationals"),
    ("SCCA-JWI", "Jacob Wilson", "Athletics"),
    ("SCCA-KA", "Kevin Alcantara", "Chicago Cubs"),
    ("SCCA-KC", "Kristian Campbell", "Boston Red Sox"),
    ("SCCA-KR", "Kumar Rocker", "Texas Rangers"),
    ("SCCA-LK", "Luke Keaschall", "Minnesota Twins"),
    ("SCCA-MA", "Mick Abel", "Philadelphia Phillies"),
    ("SCCA-MMC", "Mark McGwire", "St. Louis Cardinals"),
    ("SCCA-MS", "Matt Shaw", "Chicago Cubs"),
    ("SCCA-MT", "Mike Trout", "Los Angeles Angels"),
    ("SCCA-NA", "Nolan Arenado", "St. Louis Cardinals"),
    ("SCCA-NK", "Nick Kurtz", "Athletics"),
    ("SCCA-OH", "Orel Hershiser", "Los Angeles Dodgers"),
    ("SCCA-PS", "Paul Skenes", "Pittsburgh Pirates"),
    ("SCCA-RA", "Ronald Acuna Jr.", "Atlanta Braves"),
    ("SCCA-RC", "Roger Clemens", "New York Yankees"),
    ("SCCA-RHA", "Robert Hassell III", "Washington Nationals"),
    ("SCCA-RJ", "Randy Johnson", "Arizona Diamondbacks"),
    ("SCCA-RL", "Rhett Lowder", "Cincinnati Reds"),
    ("SCCA-RS", "Roki Sasaki", "Los Angeles Dodgers"),
    ("SCCA-SK", "Steven Kwan", "Cleveland Guardians"),
    ("SCCA-SO", "Shohei Ohtani", "Los Angeles Dodgers"),
    ("SCCA-SS", "Spencer Schwellenbach", "Atlanta Braves"),
    ("SCCA-SW", "Shay Whitcomb", "Houston Astros"),
    ("SCCA-TL", "Tyler Locklear", "Seattle Mariners"),
    ("SCCA-TS", "Thomas Saggese", "St. Louis Cardinals"),
    ("SCCA-TSW", "Trey Sweeney", "Detroit Tigers"),
    ("SCCA-VG", "Vladimir Guerrero Jr.", "Toronto Blue Jays"),
    ("SCCA-WB", "Wade Boggs", "Boston Red Sox"),
    ("SCCA-WL", "Wyatt Langford", "Texas Rangers"),
    ("SCCA-ZV", "Zac Veen", "Colorado Rockies"),
]

CHROME_AUTO_PARALLELS = make_parallels([
    "Turquoise", "Gold", "Orange", "Superfractor",
])

# Savage Sluggers Autographs (18 cards)
SAVAGE_SLUGGERS_AUTO_RAW = [
    ("SS-AP", "Albert Pujols", "St. Louis Cardinals"),
    ("SS-AR", "Alex Rodriguez", "Texas Rangers"),
    ("SS-BW", "Bobby Witt Jr.", "Kansas City Royals"),
    ("SS-CR", "Cal Ripken Jr.", "Baltimore Orioles"),
    ("SS-DO", "David Ortiz", "Boston Red Sox"),
    ("SS-FM", "Fred McGriff", "Atlanta Braves"),
    ("SS-JR", "Julio Rodriguez", "Seattle Mariners"),
    ("SS-JS", "Juan Soto", "New York Mets"),
    ("SS-KC", "Kristian Campbell", "Boston Red Sox"),
    ("SS-MM", "Manny Machado", "San Diego Padres"),
    ("SS-MT", "Mike Trout", "Los Angeles Angels"),
    ("SS-NK", "Nick Kurtz", "Athletics"),
    ("SS-PA", "Pete Alonso", "New York Mets"),
    ("SS-RJ", "Reggie Jackson", "Oakland Athletics"),
    ("SS-SO", "Shohei Ohtani", "Los Angeles Dodgers"),
    ("SS-SS", "Sammy Sosa", "Chicago Cubs"),
    ("SS-VG", "Vladimir Guerrero", "Los Angeles Angels"),
    ("SS-WL", "Wyatt Langford", "Texas Rangers"),
]

SAVAGE_SLUGGERS_AUTO_PARALLELS = make_parallels([
    "Turquoise", "Purple", "Green", "Gold Rainbow Foilboard",
])

# In Case Of Emergency Autographs (17 cards)
ICOEA_RAW = [
    ("ICOEA-AP", "Albert Pujols", "St. Louis Cardinals"),
    ("ICOEA-BW", "Bobby Witt Jr.", "Kansas City Royals"),
    ("ICOEA-DC", "Dylan Crews", "Washington Nationals"),
    ("ICOEA-DJ", "Derek Jeter", "New York Yankees"),
    ("ICOEA-DR", "Dalton Rushing", "Los Angeles Dodgers"),
    ("ICOEA-FT", "Fernando Tatis Jr.", "San Diego Padres"),
    ("ICOEA-FTH", "Frank Thomas", "Chicago White Sox"),
    ("ICOEA-HK", "Hyeseong Kim", "Los Angeles Dodgers"),
    ("ICOEA-I", "Ichiro", "Seattle Mariners"),
    ("ICOEA-JA", "Jose Altuve", "Houston Astros"),
    ("ICOEA-JC", "Jackson Chourio", "Milwaukee Brewers"),
    ("ICOEA-JR", "Julio Rodriguez", "Seattle Mariners"),
    ("ICOEA-JV", "Joey Votto", "Cincinnati Reds"),
    ("ICOEA-JW", "James Wood", "Washington Nationals"),
    ("ICOEA-JWI", "Jacob Wilson", "Athletics"),
    ("ICOEA-MS", "Mike Schmidt", "Philadelphia Phillies"),
    ("ICOEA-WB", "Wade Boggs", "Boston Red Sox"),
]

ICOEA_PARALLELS = make_parallels([
    "Turquoise", "Purple", "Green", "Gold Rainbow Foilboard",
])

# Dual Autographs (9 cards) -- co_players
DUAL_AUTO_RAW = [
    ("DA-BW", [("George Brett", "Kansas City Royals"), ("Bobby Witt Jr.", "Kansas City Royals")]),
    ("DA-CN", [("Steve Carlton", "Philadelphia Phillies"), ("Aaron Nola", "Philadelphia Phillies")]),
    ("DA-HH", [("Jackson Holliday", "Baltimore Orioles"), ("Gunnar Henderson", "Baltimore Orioles")]),
    ("DA-JA", [("Chipper Jones", "Atlanta Braves"), ("Ronald Acuna Jr.", "Atlanta Braves")]),
    ("DA-LC", [("Evan Longoria", "Tampa Bay Rays"), ("Junior Caminero", "Tampa Bay Rays")]),
    ("DA-LD", [("Barry Larkin", "Cincinnati Reds"), ("Elly De La Cruz", "Cincinnati Reds")]),
    ("DA-RS", [("Alex Rodriguez", "Texas Rangers"), ("Corey Seager", "Texas Rangers")]),
    ("DA-WC", [("Dylan Crews", "Washington Nationals"), ("James Wood", "Washington Nationals")]),
    ("DA-WK", [("Nick Kurtz", "Athletics"), ("Jacob Wilson", "Athletics")]),
]

DUAL_AUTO_PARALLELS = make_parallels([
    "Turquoise", "Purple", "Green", "Gold Rainbow Foilboard",
])

# Goin' Yard Autographs (16 cards)
GOIN_YARD_AUTO_RAW = [
    ("GYA-BB", "Barry Bonds", "San Francisco Giants"),
    ("GYA-FT", "Frank Thomas", "Chicago White Sox"),
    ("GYA-GH", "Gunnar Henderson", "Baltimore Orioles"),
    ("GYA-GS", "Gary Sheffield", "Los Angeles Dodgers"),
    ("GYA-JR", "Jose Ramirez", "Cleveland Guardians"),
    ("GYA-JS", "Juan Soto", "New York Mets"),
    ("GYA-KC", "Kristian Campbell", "Boston Red Sox"),
    ("GYA-KS", "Kyle Schwarber", "Philadelphia Phillies"),
    ("GYA-MM", "Manny Machado", "San Diego Padres"),
    ("GYA-MMC", "Mark McGwire", "St. Louis Cardinals"),
    ("GYA-PA", "Pete Alonso", "New York Mets"),
    ("GYA-RA", "Ronald Acuna Jr.", "Atlanta Braves"),
    ("GYA-RH", "Ryan Howard", "Philadelphia Phillies"),
    ("GYA-SO", "Shohei Ohtani", "Los Angeles Dodgers"),
    ("GYA-SS", "Sammy Sosa", "Chicago Cubs"),
    ("GYA-VG", "Vladimir Guerrero Jr.", "Toronto Blue Jays"),
]

GOIN_YARD_AUTO_PARALLELS = make_parallels([
    "Turquoise", "Purple", "Green", "Gold Rainbow Foilboard",
])

# Abstract Autographs (14 cards)
ABSTRACT_AUTO_RAW = [
    ("AA-AB", "Adrian Beltre", "Texas Rangers"),
    ("AA-BP", "Buster Posey", "San Francisco Giants"),
    ("AA-CJ", "Chipper Jones", "Atlanta Braves"),
    ("AA-CY", "Christian Yelich", "Milwaukee Brewers"),
    ("AA-DC", "Dylan Crews", "Washington Nationals"),
    ("AA-EM", "Eddie Murray", "Baltimore Orioles"),
    ("AA-JD", "Jasson Dominguez", "New York Yankees"),
    ("AA-JV", "Joey Votto", "Cincinnati Reds"),
    ("AA-JW", "James Wood", "Washington Nationals"),
    ("AA-LA", "Luisangel Acuna", "New York Mets"),
    ("AA-MM", "Marcelo Mayer", "Boston Red Sox"),
    ("AA-MP", "Mike Piazza", "New York Mets"),
    ("AA-MS", "Matt Shaw", "Chicago Cubs"),
    ("AA-RJ", "Reggie Jackson", "New York Yankees"),
]

ABSTRACT_AUTO_PARALLELS = make_parallels([
    "Turquoise", "Purple", "Green", "Gold Rainbow Foilboard",
])

# Concentration Autographs (12 cards)
CONCENTRATION_AUTO_RAW = [
    ("TVA-CD", "Chase Dollander", "Colorado Rockies"),
    ("TVA-CH", "Cade Horton", "Chicago Cubs"),
    ("TVA-CS", "Chris Sale", "Atlanta Braves"),
    ("TVA-GM", "Greg Maddux", "Atlanta Braves"),
    ("TVA-NR", "Nolan Ryan", "Houston Astros"),
    ("TVA-PM", "Pedro Martinez", "Boston Red Sox"),
    ("TVA-PS", "Paul Skenes", "Pittsburgh Pirates"),
    ("TVA-RC", "Roger Clemens", "New York Yankees"),
    ("TVA-RJ", "Randy Johnson", "Arizona Diamondbacks"),
    ("TVA-RS", "Roki Sasaki", "Los Angeles Dodgers"),
    ("TVA-TS", "Tarik Skubal", "Detroit Tigers"),
    ("TVA-YY", "Yoshinobu Yamamoto", "Los Angeles Dodgers"),
]

CONCENTRATION_AUTO_PARALLELS = make_parallels([
    "Turquoise", "Purple", "Green", "Gold Rainbow Foilboard",
])

# ── Insert Sets ───────────────────────────────────────────────────────────────

# Beam Team (20 cards, no parallels)
BEAM_TEAM_RAW = [
    ("BT-1", "Roki Sasaki", "Los Angeles Dodgers RC"),
    ("BT-2", "James Wood", "Washington Nationals RC"),
    ("BT-3", "Dylan Crews", "Washington Nationals RC"),
    ("BT-4", "Jacob Wilson", "Athletics RC"),
    ("BT-5", "Marcelo Mayer", "Boston Red Sox RC"),
    ("BT-6", "Kristian Campbell", "Boston Red Sox RC"),
    ("BT-7", "Nick Kurtz", "Athletics RC"),
    ("BT-8", "Brooks Lee", "Minnesota Twins RC"),
    ("BT-9", "Jackson Jobe", "Detroit Tigers RC"),
    ("BT-10", "Gunnar Henderson", "Baltimore Orioles"),
    ("BT-11", "Jackson Chourio", "Milwaukee Brewers"),
    ("BT-12", "Elly De La Cruz", "Cincinnati Reds"),
    ("BT-13", "Bryce Harper", "Philadelphia Phillies"),
    ("BT-14", "Mike Trout", "Los Angeles Angels"),
    ("BT-15", "Julio Rodriguez", "Seattle Mariners"),
    ("BT-16", "Aaron Judge", "New York Yankees"),
    ("BT-17", "Mookie Betts", "Los Angeles Dodgers"),
    ("BT-18", "Bobby Witt Jr.", "Kansas City Royals"),
    ("BT-19", "Shohei Ohtani", "Los Angeles Dodgers"),
    ("BT-20", "Francisco Lindor", "New York Mets"),
]

# Savage Sluggers (25 cards)
SAVAGE_SLUGGERS_RAW = [
    ("SS-1", "Julio Rodriguez", "Seattle Mariners"),
    ("SS-2", "Wyatt Langford", "Texas Rangers"),
    ("SS-3", "Cal Ripken Jr.", "Baltimore Orioles"),
    ("SS-4", "Fred McGriff", "Atlanta Braves"),
    ("SS-5", "Sammy Sosa", "Chicago Cubs"),
    ("SS-6", "Bobby Witt Jr.", "Kansas City Royals"),
    ("SS-7", "Shohei Ohtani", "Los Angeles Dodgers"),
    ("SS-8", "Juan Soto", "New York Mets"),
    ("SS-9", "Alex Rodriguez", "Texas Rangers"),
    ("SS-10", "Albert Pujols", "St. Louis Cardinals"),
    ("SS-11", "Reggie Jackson", "Oakland Athletics"),
    ("SS-12", "David Ortiz", "Boston Red Sox"),
    ("SS-13", "Mike Trout", "Los Angeles Angels"),
    ("SS-14", "Pete Alonso", "New York Mets"),
    ("SS-15", "Kristian Campbell", "Boston Red Sox RC"),
    ("SS-16", "Vladimir Guerrero Sr.", "Los Angeles Angels"),
    ("SS-17", "Manny Machado", "San Diego Padres"),
    ("SS-18", "Cal Raleigh", "Seattle Mariners"),
    ("SS-19", "Aaron Judge", "New York Yankees"),
    ("SS-20", "James Wood", "Washington Nationals RC"),
    ("SS-21", "Nick Kurtz", "Athletics RC"),
    ("SS-22", "Coby Mayo", "Baltimore Orioles RC"),
    ("SS-23", "Cam Smith", "Houston Astros RC"),
    ("SS-24", "Ken Griffey Jr.", "Seattle Mariners"),
    ("SS-25", "Yordan Alvarez", "Houston Astros"),
]

SAVAGE_SLUGGERS_PARALLELS = make_parallels([
    "Pink", "Turquoise", "Gold", "Gold Rainbow Foil",
])

# Concentration (25 cards)
CONCENTRATION_RAW = [
    ("C-1", "Roger Clemens", "New York Yankees"),
    ("C-2", "Randy Johnson", "Arizona Diamondbacks"),
    ("C-3", "Greg Maddux", "Atlanta Braves"),
    ("C-4", "Tarik Skubal", "Detroit Tigers"),
    ("C-5", "Chris Sale", "Atlanta Braves"),
    ("C-6", "Paul Skenes", "Pittsburgh Pirates"),
    ("C-7", "Roki Sasaki", "Los Angeles Dodgers RC"),
    ("C-8", "Nolan Ryan", "Houston Astros"),
    ("C-9", "Cade Horton", "Chicago Cubs RC"),
    ("C-10", "Jackson Jobe", "Detroit Tigers RC"),
    ("C-11", "Pedro Martinez", "Boston Red Sox"),
    ("C-12", "Yoshinobu Yamamoto", "Los Angeles Dodgers"),
    ("C-13", "Clayton Kershaw", "Los Angeles Dodgers"),
    ("C-14", "Zack Wheeler", "Philadelphia Phillies"),
    ("C-15", "Shota Imanaga", "Chicago Cubs"),
    ("C-16", "Hunter Greene", "Cincinnati Reds"),
    ("C-17", "Corbin Burnes", "Arizona Diamondbacks"),
    ("C-18", "Justin Verlander", "San Francisco Giants"),
    ("C-19", "Max Scherzer", "Toronto Blue Jays"),
    ("C-20", "Felix Hernandez", "Seattle Mariners"),
    ("C-21", "Johan Santana", "Minnesota Twins"),
    ("C-22", "Spencer Schwellenbach", "Atlanta Braves"),
    ("C-23", "Rhett Lowder", "Cincinnati Reds RC"),
    ("C-24", "Kumar Rocker", "Texas Rangers RC"),
    ("C-25", "Eury Perez", "Miami Marlins"),
]

CONCENTRATION_PARALLELS = make_parallels([
    "Pink", "Turquoise", "Gold", "Gold Rainbow Foil",
])

# Yours For The Taking (25 cards)
YOURS_FOR_THE_TAKING_RAW = [
    ("YK-1", "James Wood", "Washington Nationals RC"),
    ("YK-2", "Dylan Crews", "Washington Nationals RC"),
    ("YK-3", "Matt Shaw", "Chicago Cubs RC"),
    ("YK-4", "Kristian Campbell", "Boston Red Sox RC"),
    ("YK-5", "Cam Smith", "Houston Astros RC"),
    ("YK-6", "Jacob Wilson", "Athletics RC"),
    ("YK-7", "Coby Mayo", "Baltimore Orioles RC"),
    ("YK-8", "Luisangel Acuna", "New York Mets RC"),
    ("YK-9", "Brooks Lee", "Minnesota Twins RC"),
    ("YK-10", "Roki Sasaki", "Los Angeles Dodgers RC"),
    ("YK-11", "Jackson Jobe", "Detroit Tigers RC"),
    ("YK-12", "Jackson Holliday", "Baltimore Orioles"),
    ("YK-13", "Jackson Chourio", "Milwaukee Brewers"),
    ("YK-14", "Jackson Merrill", "San Diego Padres"),
    ("YK-15", "Junior Caminero", "Tampa Bay Rays"),
    ("YK-16", "Bobby Witt Jr.", "Kansas City Royals"),
    ("YK-17", "Gunnar Henderson", "Baltimore Orioles"),
    ("YK-18", "Corbin Carroll", "Arizona Diamondbacks"),
    ("YK-19", "Vladimir Guerrero Jr.", "Toronto Blue Jays"),
    ("YK-20", "Elly De La Cruz", "Cincinnati Reds"),
    ("YK-21", "Yordan Alvarez", "Houston Astros"),
    ("YK-22", "Julio Rodriguez", "Seattle Mariners"),
    ("YK-23", "Wyatt Langford", "Texas Rangers"),
    ("YK-24", "Juan Soto", "New York Mets"),
    ("YK-25", "Fernando Tatis Jr.", "San Diego Padres"),
]

YOURS_FOR_THE_TAKING_PARALLELS = make_parallels([
    "Pink", "Turquoise", "Gold", "Gold Rainbow Foil",
])

# In Case Of Emergency (25 cards)
IN_CASE_OF_EMERGENCY_RAW = [
    ("ICE-1", "Bobby Witt Jr.", "Kansas City Royals"),
    ("ICE-2", "Dalton Rushing", "Los Angeles Dodgers RC"),
    ("ICE-3", "Jackson Chourio", "Milwaukee Brewers"),
    ("ICE-4", "Jackson Merrill", "San Diego Padres"),
    ("ICE-5", "Jose Altuve", "Houston Astros"),
    ("ICE-6", "Albert Pujols", "St. Louis Cardinals"),
    ("ICE-7", "Derek Jeter", "New York Yankees"),
    ("ICE-8", "Ichiro", "Seattle Mariners"),
    ("ICE-9", "Fernando Tatis Jr.", "San Diego Padres"),
    ("ICE-10", "Mike Schmidt", "Philadelphia Phillies"),
    ("ICE-11", "James Wood", "Washington Nationals RC"),
    ("ICE-12", "Dylan Crews", "Washington Nationals RC"),
    ("ICE-13", "Jacob Wilson", "Athletics RC"),
    ("ICE-14", "Julio Rodriguez", "Seattle Mariners"),
    ("ICE-15", "Joey Votto", "Cincinnati Reds"),
    ("ICE-16", "Frank Thomas", "Chicago White Sox"),
    ("ICE-17", "Wade Boggs", "Boston Red Sox"),
    ("ICE-18", "Hyeseong Kim", "Los Angeles Dodgers RC"),
    ("ICE-19", "Coby Mayo", "Baltimore Orioles RC"),
    ("ICE-20", "Brooks Lee", "Minnesota Twins RC"),
    ("ICE-21", "Kyle Tucker", "Chicago Cubs"),
    ("ICE-22", "Matt Shaw", "Chicago Cubs RC"),
    ("ICE-23", "Kristian Campbell", "Boston Red Sox RC"),
    ("ICE-24", "Cam Smith", "Houston Astros RC"),
    ("ICE-25", "Mike Trout", "Los Angeles Angels"),
]

IN_CASE_OF_EMERGENCY_PARALLELS = make_parallels([
    "Pink", "Turquoise", "Gold", "Gold Rainbow Foil",
])


# ── Build logic ───────────────────────────────────────────────────────────────

def build_single_cards(raw: list[tuple[str, str, str]]) -> list[dict]:
    """Build card dicts from (card_number, name, team) tuples."""
    cards = []
    for num, name, team in raw:
        clean_name, name_rc = parse_rc(name)
        clean_team, team_rc = parse_rc(team)
        cards.append({
            "card_number": num,
            "player": clean_name,
            "team": clean_team,
            "is_rookie": name_rc or team_rc,
            "subset": None,
        })
    return cards


def build_multi_cards(raw: list[tuple[str, list[tuple[str, str]]]]) -> list[dict]:
    """Build card dicts from multi-player (card_number, [(name, team), ...]) tuples.
    Each player gets their own card entry with the same card_number so seed.ts
    detects them as co-players."""
    cards = []
    for num, player_list in raw:
        for name, team in player_list:
            clean_name, name_rc = parse_rc(name)
            clean_team, team_rc = parse_rc(team)
            cards.append({
                "card_number": num,
                "player": clean_name,
                "team": clean_team,
                "is_rookie": name_rc or team_rc,
                "subset": None,
            })
    return cards


# ── Sections ──────────────────────────────────────────────────────────────────

SECTIONS: list[tuple[str, list[dict], list[dict]]] = [
    ("Base Set", build_single_cards(BASE_SET_RAW), BASE_SET_PARALLELS),
    ("Base Autographs", build_single_cards(BASE_AUTO_RAW), BASE_AUTO_PARALLELS),
    ("Chrome Autographs", build_single_cards(CHROME_AUTO_RAW), CHROME_AUTO_PARALLELS),
    ("Savage Sluggers Autographs", build_single_cards(SAVAGE_SLUGGERS_AUTO_RAW), SAVAGE_SLUGGERS_AUTO_PARALLELS),
    ("In Case Of Emergency Autographs", build_single_cards(ICOEA_RAW), ICOEA_PARALLELS),
    ("Dual Autographs", build_multi_cards(DUAL_AUTO_RAW), DUAL_AUTO_PARALLELS),
    ("Goin' Yard Autographs", build_single_cards(GOIN_YARD_AUTO_RAW), GOIN_YARD_AUTO_PARALLELS),
    ("Abstract Autographs", build_single_cards(ABSTRACT_AUTO_RAW), ABSTRACT_AUTO_PARALLELS),
    ("Concentration Autographs", build_single_cards(CONCENTRATION_AUTO_RAW), CONCENTRATION_AUTO_PARALLELS),
    ("Beam Team", build_single_cards(BEAM_TEAM_RAW), []),
    ("Savage Sluggers", build_single_cards(SAVAGE_SLUGGERS_RAW), SAVAGE_SLUGGERS_PARALLELS),
    ("Concentration", build_single_cards(CONCENTRATION_RAW), CONCENTRATION_PARALLELS),
    ("Yours For The Taking", build_single_cards(YOURS_FOR_THE_TAKING_RAW), YOURS_FOR_THE_TAKING_PARALLELS),
    ("In Case Of Emergency", build_single_cards(IN_CASE_OF_EMERGENCY_RAW), IN_CASE_OF_EMERGENCY_PARALLELS),
]


# ── Player aggregation ────────────────────────────────────────────────────────

def main() -> None:
    sections_out: list[dict] = []
    players_map: dict[str, dict] = {}  # keyed by player.lower()

    for section_name, cards, section_parallels in SECTIONS:
        sections_out.append({
            "insert_set": section_name,
            "parallels": section_parallels,
            "cards": cards,
        })

        for card in cards:
            key = card["player"].lower()
            if key not in players_map:
                players_map[key] = {
                    "player": card["player"],
                    "appearances": [],
                    "insert_sets_seen": set(),
                }
            entry = players_map[key]
            entry["appearances"].append({
                "insert_set": section_name,
                "card_number": card["card_number"],
                "team": card["team"],
                "is_rookie": card["is_rookie"],
                "subset_tag": card.get("subset"),
                "parallels": section_parallels,
            })
            entry["insert_sets_seen"].add(section_name)

    # Build player list with stats
    players_out: list[dict] = []
    for entry in sorted(players_map.values(), key=lambda e: e["player"]):
        unique_cards = len(entry["appearances"])
        total_print_run = 0  # all parallels have null print_run
        one_of_ones = 0
        insert_sets = len(entry["insert_sets_seen"])

        players_out.append({
            "player": entry["player"],
            "appearances": entry["appearances"],
            "stats": {
                "unique_cards": unique_cards,
                "total_print_run": total_print_run,
                "one_of_ones": one_of_ones,
                "insert_sets": insert_sets,
            },
        })

    output = {
        "set_name": SET_NAME,
        "sport": SPORT,
        "season": SEASON,
        "league": LEAGUE,
        "sections": sections_out,
        "players": players_out,
    }

    total_cards = sum(len(s["cards"]) for s in sections_out)
    print(f"Sections: {len(sections_out)}")
    print(f"Total cards: {total_cards}")
    print(f"Unique players: {len(players_out)}")

    out_path = "stadium_club_baseball_2025_parsed.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"Written to {out_path}")


if __name__ == "__main__":
    main()
