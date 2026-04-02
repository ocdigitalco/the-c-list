"""
Parser for 2025-26 Topps Chrome UEFA Club Competitions.

Outputs chrome_uefa_2526_parsed.json for use with seed.ts.

Usage:
    python scripts/parse_chrome_uefa_2526.py
    npx tsx scripts/seed.ts chrome_uefa_2526_parsed.json
"""

import json

# ── Parallels ────────────────────────────────────────────────────────────────

# Chrome parallels used across most insert sets
NO_PARALLELS = []

# ── Data ─────────────────────────────────────────────────────────────────────

# (number, name, team, is_rookie)
# RC suffix and [Future Stars] tag stripped during parsing
BASE_SET = [
    ("1", "Rayan Cherki", "Manchester City", False),
    ("2", "Bernardo Silva", "Manchester City", False),
    ("3", "Ousmane Dembélé", "Paris Saint-Germain", False),
    ("4", "Michael Olise", "FC Bayern München", False),
    ("5", "Jobe Bellingham", "Borussia Dortmund", True),
    ("6", "Jeremie Frimpong", "Liverpool FC", False),
    ("7", "Matteo Politano", "SSC Napoli", False),
    ("8", "Jamaldeen Jimoh-Aloba", "Aston Villa", True),
    ("9", "Axel Tapé", "Bayer 04 Leverkusen", True),
    ("10", "Lamine Yamal", "FC Barcelona", False),
    ("11", "Stanislav Lobotka", "SSC Napoli", False),
    ("12", "Bukayo Saka", "Arsenal FC", False),
    ("13", "Antony", "Real Betis Balompié", False),
    ("14", "João Neves", "Paris Saint-Germain", False),
    ("15", "Weston McKennie", "Juventus", False),
    ("16", "Richard Ríos", "SL Benfica", True),
    ("17", "Jonathan David", "Juventus", False),
    ("18", "Brennan Johnson", "Tottenham Hotspur", False),
    ("19", "Gabriel Martinelli", "Arsenal FC", False),
    ("20", "Iñaki Williams", "Athletic Club", False),
    ("21", "Ethan Nwaneri", "Arsenal FC", False),
    ("22", "Senny Mayulu", "Paris Saint-Germain", False),
    ("23", "Joelinton", "Newcastle United", False),
    ("24", "Malik Tillman", "Bayer 04 Leverkusen", False),
    ("25", "Julien Duranville", "Borussia Dortmund", False),
    ("26", "Robin Mirisola", "KRC Genk", True),
    ("27", "Christian Kofane", "Bayer 04 Leverkusen", True),
    ("28", "John McGinn", "Aston Villa", False),
    ("29", "Kendry Páez", "RC Strasbourg Alsace", True),
    ("30", "Jota", "Celtic FC", False),
    ("31", "Eduardo Camavinga", "Real Madrid C.F.", False),
    ("32", "Shumaira Mheuka", "Chelsea FC", True),
    ("33", "Savinho", "Manchester City", False),
    ("34", "Vangelis Pavlidis", "SL Benfica", False),
    ("35", "Isco", "Real Betis Balompié", False),
    ("36", "Hugo Larsson", "Eintracht Frankfurt", False),
    ("37", "Federico Dimarco", "FC Internazionale Milano", False),
    ("38", "Nico Williams", "Athletic Club", False),
    ("39", "Dean Huijsen", "Real Madrid C.F.", False),
    ("40", "Reo Hatate", "Celtic FC", False),
    ("41", "Scott McTominay", "SSC Napoli", False),
    ("42", "Viktor Gyökeres", "Arsenal FC", False),
    ("43", "Sean Steur", "AFC Ajax", True),
    ("44", "Alejo Sarco", "Bayer 04 Leverkusen", True),
    ("45", "Mohamed Diomandé", "Rangers F.C.", False),
    ("46", "Vitinha", "Paris Saint-Germain", False),
    ("47", "Jérémy Doku", "Manchester City", False),
    ("48", "Marcus Thuram", "FC Internazionale Milano", False),
    ("49", "Divine Mukasa", "Manchester City", True),
    ("50", "William Gomes", "FC Porto", False),
    ("51", "Cucho", "Real Betis Balompié", False),
    ("52", "Myles Lewis-Skelly", "Arsenal FC", False),
    ("53", "Morgan Gibbs-White", "Nottingham Forest", False),
    ("54", "Robert Lewandowski", "FC Barcelona", False),
    ("55", "Joshua Kimmich", "FC Bayern München", False),
    ("56", "Mikey Moore", "Rangers F.C.", False),
    ("57", "Max Dowman", "Arsenal FC", True),
    ("58", "Tyrique George", "Chelsea FC", False),
    ("59", "Serhou Guirassy", "Borussia Dortmund", False),
    ("60", "Eduardo Felicíssimo", "Sporting Clube de Portugal", True),
    ("61", "Elye Wahi", "Eintracht Frankfurt", False),
    ("62", "Martim Fernandes", "FC Porto", False),
    ("63", "Bradley Barcola", "Paris Saint-Germain", False),
    ("64", "Jude Bellingham", "Real Madrid C.F.", False),
    ("65", "Federico Valverde", "Real Madrid C.F.", False),
    ("66", "Estêvão Willian", "Chelsea FC", True),
    ("67", "Alexis Mac Allister", "Liverpool FC", False),
    ("68", "Nick Woltemade", "Newcastle United", False),
    ("69", "Nuno Mendes", "Paris Saint-Germain", False),
    ("70", "Reggie Walsh", "Chelsea FC", True),
    ("71", "Khéphren Thuram", "Juventus", False),
    ("72", "Ibrahim Maza", "Bayer 04 Leverkusen", False),
    ("73", "Giovanni Leoni", "Liverpool FC", True),
    ("74", "Florian Wirtz", "Liverpool FC", False),
    ("75", "Emiliano Martínez", "Aston Villa", False),
    ("76", "Romelu Lukaku", "SSC Napoli", False),
    ("77", "Giovanni Di Lorenzo", "SSC Napoli", False),
    ("78", "Dominik Szoboszlai", "Liverpool FC", False),
    ("79", "Virgil van Dijk", "Liverpool FC", False),
    ("80", "Omar Marmoush", "Manchester City", False),
    ("81", "Julian Brandt", "Borussia Dortmund", False),
    ("82", "Antoine Griezmann", "Atlético de Madrid", False),
    ("83", "Rodrigo Mora", "FC Porto", False),
    ("84", "Claudio Echeverri", "Bayer 04 Leverkusen", True),
    ("85", "Xavi Simons", "Tottenham Hotspur", False),
    ("86", "Endrick", "Real Madrid C.F.", False),
    ("87", "Gabri Veiga", "FC Porto", False),
    ("88", "Wisdom Mike", "FC Bayern München", True),
    ("89", "Mohammed Kudus", "Tottenham Hotspur", False),
    ("90", "Alphonso Davies", "FC Bayern München", False),
    ("91", "Victor Froholdt", "FC Porto", True),
    ("92", "Marquinhos", "Paris Saint-Germain", False),
    ("93", "Quim Junyent", "FC Barcelona", True),
    ("94", "Lucas Michal", "AS Monaco", True),
    ("95", "Geovany Quenda", "Sporting Clube de Portugal", False),
    ("96", "Elliot Anderson", "Nottingham Forest", False),
    ("97", "Raphinha", "FC Barcelona", False),
    ("98", "Daizen Maeda", "Celtic FC", False),
    ("99", "Nico Schlotterbeck", "Borussia Dortmund", False),
    ("100", "Giuliano Simeone", "Atlético de Madrid", False),
    ("101", "Minjae Kim", "FC Bayern München", False),
    ("102", "Rodrygo", "Real Madrid C.F.", False),
    ("103", "Phil Foden", "Manchester City", False),
    ("104", "Ousmane Diomande", "Sporting Clube de Portugal", False),
    ("105", "Maroan Sannadi", "Athletic Club", False),
    ("106", "Ricardo Pepi", "PSV Eindhoven", False),
    ("107", "Andrey Santos", "Chelsea FC", False),
    ("108", "Nicolò Barella", "FC Internazionale Milano", False),
    ("109", "Sandro Tonali", "Newcastle United", False),
    ("110", "Emmanuel Emegha", "RC Strasbourg Alsace", False),
    ("111", "Dro", "FC Barcelona", True),
    ("112", "Kylian Mbappé", "Real Madrid C.F.", False),
    ("113", "William Saliba", "Arsenal FC", False),
    ("114", "Abdoul Ouattara", "RC Strasbourg Alsace", True),
    ("115", "Vini Jr.", "Real Madrid C.F.", False),
    ("116", "Alexander Isak", "Liverpool FC", False),
    ("117", "Bruno Guimarães", "Newcastle United", False),
    ("118", "Cole Palmer", "Chelsea FC", False),
    ("119", "Arthur Theate", "Eintracht Frankfurt", False),
    ("120", "Ousmane Diallo", "Borussia Dortmund", True),
    ("121", "Lucas Bergvall", "Tottenham Hotspur", False),
    ("122", "Noah Adedeji-Sternberg", "KRC Genk", True),
    ("123", "Takumi Minamino", "AS Monaco", False),
    ("124", "Ollie Watkins", "Aston Villa", False),
    ("125", "Ben Parkinson", "Newcastle United", True),
    ("126", "Jarne Steuckers", "KRC Genk", True),
    ("127", "Kenneth Taylor", "AFC Ajax", False),
    ("128", "Karim Adeyemi", "Borussia Dortmund", False),
    ("129", "George Ilenikhena", "AS Monaco", False),
    ("130", "Jamal Musiala", "FC Bayern München", False),
    ("131", "Luis Henrique", "FC Internazionale Milano", False),
    ("132", "Gavi", "FC Barcelona", False),
    ("133", "Samu Aghehowa", "FC Porto", False),
    ("134", "Callum Olusesi", "Tottenham Hotspur", True),
    ("135", "Frenkie de Jong", "FC Barcelona", False),
    ("136", "Mohamed Salah", "Liverpool FC", False),
    ("137", "Omar Janneh", "Atlético de Madrid", True),
    ("138", "Ferran Torres", "FC Barcelona", False),
    ("139", "Ivan Perišić", "PSV Eindhoven", False),
    ("140", "Nasser Djiga", "Rangers F.C.", True),
    ("141", "Trent Alexander-Arnold", "Real Madrid C.F.", False),
    ("142", "Reigan Heskey", "Manchester City", True),
    ("143", "Alessandro Bastoni", "FC Internazionale Milano", False),
    ("144", "Dominic Solanke", "Tottenham Hotspur", False),
    ("145", "Denzel Dumfries", "FC Internazionale Milano", False),
    ("146", "Michael Bresser", "PSV Eindhoven", True),
    ("147", "Kenan Yildiz", "Juventus", False),
    ("148", "Alistair Johnston", "Celtic FC", False),
    ("149", "Abde Ezzalzouli", "Real Betis Balompié", False),
    ("150", "Konstantinos Karetsas", "KRC Genk", True),
    ("151", "Mika Godts", "AFC Ajax", False),
    ("152", "Gleison Bremer", "Juventus", False),
    ("153", "Patrik Schick", "Bayer 04 Leverkusen", False),
    ("154", "Julián Alvarez", "Atlético de Madrid", False),
    ("155", "Tijjani Reijnders", "Manchester City", False),
    ("156", "Lautaro Martínez", "FC Internazionale Milano", False),
    ("157", "Martin Ødegaard", "Arsenal FC", False),
    ("158", "Ibrahim Mbaye", "Paris Saint-Germain", False),
    ("159", "Anthony Gordon", "Newcastle United", False),
    ("160", "Leandro Santos", "SL Benfica", True),
    ("161", "Igor Jesus", "Nottingham Forest", True),
    ("162", "Mario Götze", "Eintracht Frankfurt", False),
    ("163", "Pio Esposito", "FC Internazionale Milano", True),
    ("164", "Declan Rice", "Arsenal FC", False),
    ("165", "Archie Gray", "Tottenham Hotspur", False),
    ("166", "Quentin Ndjantou", "Paris Saint-Germain", True),
    ("167", "Khvicha Kvaratskhelia", "Paris Saint-Germain", False),
    ("168", "João Rego", "SL Benfica", True),
    ("169", "Sergiño Dest", "PSV Eindhoven", False),
    ("170", "Warren Zaïre-Emery", "Paris Saint-Germain", False),
    ("171", "Rodri", "Manchester City", False),
    ("172", "Franco Mastantuono", "Real Madrid C.F.", True),
    ("173", "Don-Angelo Konadu", "AFC Ajax", True),
    ("174", "Pablo García", "Real Betis Balompié", True),
    ("175", "Dušan Vlahović", "Juventus", False),
    ("176", "Hugo Ekitike", "Liverpool FC", False),
    ("177", "Mathis Amougou", "RC Strasbourg Alsace", True),
    ("178", "Mika Biereth", "AS Monaco", False),
    ("179", "Luis Díaz", "FC Bayern München", False),
    ("180", "Guela Doué", "RC Strasbourg Alsace", False),
    ("181", "Erling Haaland", "Manchester City", False),
    ("182", "Harry Kane", "FC Bayern München", False),
    ("183", "Pau Cubarsí", "FC Barcelona", False),
    ("184", "João Pedro", "Chelsea FC", False),
    ("185", "Kang-in Lee", "Paris Saint-Germain", False),
    ("186", "Chris Wood", "Nottingham Forest", False),
    ("187", "Lennart Karl", "FC Bayern München", True),
    ("188", "James Tavernier", "Rangers F.C.", False),
    ("189", "Conor Gallagher", "Atlético de Madrid", False),
    ("190", "Guille Fernández", "FC Barcelona", True),
    ("191", "Rio Ngumoha", "Liverpool FC", True),
    ("192", "Liam Delap", "Chelsea FC", False),
    ("193", "Ryan Gravenberch", "Liverpool FC", False),
    ("194", "Eberechi Eze", "Arsenal FC", False),
    ("195", "Oihan Sancet", "Athletic Club", False),
    ("196", "Pedri", "FC Barcelona", False),
    ("197", "Morgan Rogers", "Aston Villa", False),
    ("198", "Désiré Doué", "Paris Saint-Germain", False),
    ("199", "Morten Hjulmand", "Sporting Clube de Portugal", False),
    ("200", "Kevin De Bruyne", "SSC Napoli", False),
]

# Future Stars card numbers (belong to "Base - Future Stars" insert set)
FUTURE_STARS_NUMBERS = {"21", "22", "52", "56", "58", "83", "86", "95", "129", "158"}

# ── Insert Sets ──────────────────────────────────────────────────────────────

BOWMAN_UEFA_YOUTH_LEAGUE = [
    ("BU-ET", "Ebrima Tunkara", "FC Barcelona"),
    ("BU-FS", "Floyd Samba", "Manchester City"),
    ("BU-JU", "Jaden Umeh", "SL Benfica"),
    ("BU-LWB", "Lucá Williams-Barnett", "Tottenham Hotspur"),
    ("BU-MA", "Mathis Albert", "Borussia Dortmund"),
    ("BU-OB", "Oliver Boast", "Tottenham Hotspur"),
    ("BU-RM", "Ryan McAidoo", "Manchester City"),
    ("BU-SI", "Samuele Inacio", "Borussia Dortmund"),
    ("BU-SK", "Shane Kluivert", "FC Barcelona"),
    ("BU-SM", "Stephen Mfuni", "Manchester City"),
    ("BU-TL", "Teddie Lamb", "Manchester City"),
]

LAST_DANCE = [
    ("LD-1", "Toni Kroos", "Real Madrid C.F."),
    ("LD-2", "Xavi Hernández", "FC Barcelona"),
    ("LD-3", "Gareth Bale", "Real Madrid C.F."),
    ("LD-4", "Frank Rijkaard", "AFC Ajax"),
    ("LD-5", "David Villa", "Atlético de Madrid"),
    ("LD-6", "Steven Gerrard", "Liverpool FC"),
    ("LD-7", "Dennis Bergkamp", "Arsenal FC"),
    ("LD-8", "John Terry", "Chelsea FC"),
    ("LD-9", "Ronaldinho", "AC Milan"),
    ("LD-10", "Diego Maradona", "SSC Napoli"),
    ("LD-11", "Paolo Maldini", "AC Milan"),
    ("LD-12", "Ryan Giggs", "Manchester United"),
    ("LD-13", "Philipp Lahm", "FC Bayern München"),
    ("LD-14", "Javier Zanetti", "FC Internazionale Milano"),
]

WONDERKIDS = [
    ("WK-1", "Rio Ngumoha", "Liverpool FC", True),
    ("WK-2", "Reigan Heskey", "Manchester City", True),
    ("WK-3", "Estêvão Willian", "Chelsea FC", True),
    ("WK-4", "Max Dowman", "Arsenal FC", True),
    ("WK-5", "Dro", "FC Barcelona", True),
    ("WK-6", "Dean Huijsen", "Real Madrid C.F.", False),
    ("WK-7", "Franco Mastantuono", "Real Madrid C.F.", True),
    ("WK-8", "Lennart Karl", "FC Bayern München", True),
    ("WK-9", "Jobe Bellingham", "Borussia Dortmund", True),
    ("WK-10", "Pio Esposito", "FC Internazionale Milano", True),
    ("WK-11", "Désiré Doué", "Paris Saint-Germain", False),
    ("WK-12", "Konstantinos Karetsas", "KRC Genk", True),
    ("WK-13", "Myles Lewis-Skelly", "Arsenal FC", False),
    ("WK-14", "Tyrique George", "Chelsea FC", False),
    ("WK-15", "Rodrigo Mora", "FC Porto", False),
    ("WK-16", "Pablo García", "Real Betis Balompié", True),
    ("WK-17", "Reggie Walsh", "Chelsea FC", True),
    ("WK-18", "Wisdom Mike", "FC Bayern München", True),
    ("WK-19", "Christian Kofane", "Bayer 04 Leverkusen", True),
    ("WK-20", "Quentin Ndjantou", "Paris Saint-Germain", True),
]

SILENCED = [
    ("SHH-1", "Neymar Jr", "Paris Saint-Germain"),
    ("SHH-2", "Thierry Henry", "Arsenal FC"),
    ("SHH-3", "Zlatan Ibrahimović", "FC Internazionale Milano"),
    ("SHH-4", "Luis Suárez", "FC Barcelona"),
    ("SHH-5", "Khvicha Kvaratskhelia", "Paris Saint-Germain"),
    ("SHH-6", "Mario Balotelli", "AC Milan"),
    ("SHH-7", "Michael Olise", "FC Bayern München"),
    ("SHH-8", "Vini Jr.", "Real Madrid C.F."),
    ("SHH-9", "Samuel Eto'o", "FC Internazionale Milano"),
    ("SHH-10", "Phil Foden", "Manchester City"),
]

POWER_PLAYERS = [
    ("PP-1", "Jeremie Frimpong", "Liverpool FC"),
    ("PP-2", "Hugo Ekitike", "Liverpool FC"),
    ("PP-3", "Gabriel Martinelli", "Arsenal FC"),
    ("PP-4", "Myles Lewis-Skelly", "Arsenal FC"),
    ("PP-5", "Joelinton", "Newcastle United"),
    ("PP-6", "Erling Haaland", "Manchester City"),
    ("PP-7", "Jérémy Doku", "Manchester City"),
    ("PP-8", "Liam Delap", "Chelsea FC"),
    ("PP-9", "Lautaro Martínez", "FC Internazionale Milano"),
    ("PP-10", "Dominic Solanke", "Tottenham Hotspur"),
    ("PP-11", "Mohammed Kudus", "Tottenham Hotspur"),
    ("PP-12", "Romelu Lukaku", "SSC Napoli"),
    ("PP-13", "Raphinha", "FC Barcelona"),
    ("PP-14", "Vini Jr.", "Real Madrid C.F."),
    ("PP-15", "Federico Valverde", "Real Madrid C.F."),
    ("PP-16", "Giuliano Simeone", "Atlético de Madrid"),
    ("PP-17", "Iñaki Williams", "Athletic Club"),
    ("PP-18", "Weston McKennie", "Juventus"),
    ("PP-19", "Alphonso Davies", "FC Bayern München"),
    ("PP-20", "Luis Díaz", "FC Bayern München"),
    ("PP-21", "Karim Adeyemi", "Borussia Dortmund"),
    ("PP-22", "Patrik Schick", "Bayer 04 Leverkusen"),
    ("PP-23", "Morgan Rogers", "Aston Villa"),
    ("PP-24", "Denzel Dumfries", "FC Internazionale Milano"),
    ("PP-25", "Chris Wood", "Nottingham Forest"),
    ("PP-26", "Dušan Vlahović", "Juventus"),
    ("PP-27", "Antony", "Real Betis Balompié"),
    ("PP-28", "Marquinhos", "Paris Saint-Germain"),
    ("PP-29", "Folarin Balogun", "AS Monaco"),
    ("PP-30", "George Ilenikhena", "AS Monaco"),
    ("PP-31", "Ousmane Diomande", "Sporting Clube de Portugal"),
    ("PP-32", "Richard Ríos", "SL Benfica", True),
    ("PP-33", "Samu Aghehowa", "FC Porto"),
    ("PP-34", "Alistair Johnston", "Celtic FC"),
    ("PP-35", "William Gomes", "FC Porto"),
]

VENI_VIDI_VICI = [
    ("VVV-1", "Mohamed Salah", "Liverpool FC"),
    ("VVV-2", "Bukayo Saka", "Arsenal FC"),
    ("VVV-3", "Lamine Yamal", "FC Barcelona"),
    ("VVV-4", "Jude Bellingham", "Real Madrid C.F."),
    ("VVV-5", "Lautaro Martínez", "FC Internazionale Milano"),
]

YOUTHQUAKE = [
    ("YQ-1", "Rio Ngumoha", "Liverpool FC", True),
    ("YQ-2", "Divine Mukasa", "Manchester City", True),
    ("YQ-3", "Estêvão Willian", "Chelsea FC", True),
    ("YQ-4", "Xavi Simons", "Tottenham Hotspur", False),
    ("YQ-5", "Pau Cubarsí", "FC Barcelona", False),
    ("YQ-6", "Franco Mastantuono", "Real Madrid C.F.", True),
    ("YQ-7", "Pablo García", "Real Betis Balompié", True),
    ("YQ-8", "Lennart Karl", "FC Bayern München", True),
    ("YQ-9", "Jobe Bellingham", "Borussia Dortmund", True),
    ("YQ-10", "Pio Esposito", "FC Internazionale Milano", True),
    ("YQ-11", "João Neves", "Paris Saint-Germain", False),
    ("YQ-12", "Kendry Páez", "RC Strasbourg Alsace", True),
    ("YQ-13", "Nico O'Reilly", "Manchester City", False),
    ("YQ-14", "Senny Mayulu", "Paris Saint-Germain", False),
    ("YQ-15", "Geovany Quenda", "Sporting Clube de Portugal", False),
]

ULTRA_VIOLET = [
    ("UV-1", "Steven Gerrard", "Liverpool FC"),
    ("UV-2", "Thierry Henry", "Arsenal FC"),
    ("UV-3", "Yaya Touré", "Manchester City"),
    ("UV-4", "Didier Drogba", "Chelsea FC"),
    ("UV-5", "Gareth Bale", "Tottenham Hotspur"),
    ("UV-6", "Ronaldinho", "FC Barcelona"),
    ("UV-7", "Neymar Jr", "FC Barcelona"),
    ("UV-8", "Raúl", "Real Madrid C.F."),
    ("UV-9", "Roberto Carlos", "Real Madrid C.F."),
    ("UV-10", "Fernando Torres", "Atlético de Madrid"),
    ("UV-11", "Franck Ribéry", "FC Bayern München"),
    ("UV-12", "Pierre-Emerick Aubameyang", "Borussia Dortmund"),
    ("UV-13", "Kaká", "AC Milan"),
    ("UV-14", "Ronaldo", "FC Internazionale Milano"),
    ("UV-15", "Alessandro Del Piero", "Juventus"),
    ("UV-16", "George Weah", "AC Milan"),
    ("UV-17", "Zlatan Ibrahimović", "Paris Saint-Germain"),
    ("UV-18", "Ángel Di María", "Paris Saint-Germain"),
    ("UV-19", "Johan Cruyff", "AFC Ajax"),
    ("UV-20", "Henrik Larsson", "Celtic FC"),
]

# Radiating Rookies — same card numbers as base, same players
RADIATING_ROOKIES_NUMBERS = [
    "5", "29", "57", "66", "88", "91", "111", "142", "150",
    "163", "166", "172", "174", "187", "191",
]

SHADOW_ETCH = [
    ("SE-1", "Antoine Griezmann", "Atlético de Madrid", False),
    ("SE-2", "Jamal Musiala", "FC Bayern München", False),
    ("SE-3", "Vini Jr.", "Real Madrid C.F.", False),
    ("SE-4", "Ousmane Dembélé", "Paris Saint-Germain", False),
    ("SE-5", "Franco Mastantuono", "Real Madrid C.F.", True),
    ("SE-6", "Pedri", "FC Barcelona", False),
    ("SE-7", "Alexander Isak", "Liverpool FC", False),
    ("SE-8", "Viktor Gyökeres", "Arsenal FC", False),
    ("SE-9", "Didier Drogba", "Chelsea FC", False),
    ("SE-10", "Raúl", "Real Madrid C.F.", False),
    ("SE-11", "Luis Suárez", "FC Barcelona", False),
    ("SE-12", "Dro", "FC Barcelona", True),
    ("SE-13", "Pablo García", "Real Betis Balompié", True),
    ("SE-14", "Roberto Baggio", "Juventus", False),
    ("SE-15", "Zlatan Ibrahimović", "Paris Saint-Germain", False),
    ("SE-16", "Marquinhos", "Paris Saint-Germain", False),
    ("SE-17", "Andriy Shevchenko", "AC Milan", False),
    ("SE-18", "Lionel Messi", "FC Barcelona", False),
    ("SE-19", "Jude Bellingham", "Real Madrid C.F.", False),
    ("SE-20", "Victor Froholdt", "FC Porto", True),
]

BIONIC = [
    ("B-1", "Robert Lewandowski", "FC Barcelona"),
    ("B-2", "Erling Haaland", "Manchester City"),
    ("B-3", "Jude Bellingham", "Real Madrid C.F."),
    ("B-4", "Lamine Yamal", "FC Barcelona"),
    ("B-5", "João Neves", "Paris Saint-Germain"),
]

METAVERSE = [
    ("MV-1", "Ángel Di María", "Paris Saint-Germain"),
    ("MV-2", "Phil Foden", "Manchester City"),
    ("MV-3", "Virgil van Dijk", "Liverpool FC"),
    ("MV-4", "Martin Ødegaard", "Arsenal FC"),
    ("MV-5", "Xavi Simons", "Tottenham Hotspur"),
    ("MV-6", "Raphinha", "FC Barcelona"),
    ("MV-7", "Sergio Agüero", "Manchester City"),
    ("MV-8", "Gareth Bale", "Tottenham Hotspur"),
    ("MV-9", "Vini Jr.", "Real Madrid C.F."),
    ("MV-10", "Lautaro Martínez", "FC Internazionale Milano"),
    ("MV-11", "Serhou Guirassy", "Borussia Dortmund"),
    ("MV-12", "Wayne Rooney", "Manchester United"),
    ("MV-13", "Rodrigo Mora", "FC Porto"),
    ("MV-14", "Claudio Echeverri", "Bayer 04 Leverkusen", True),
]

BUDAPEST_AT_NIGHT = [
    ("BN-1", "Lamine Yamal", "FC Barcelona", False),
    ("BN-2", "Kylian Mbappé", "Real Madrid C.F.", False),
    ("BN-3", "Max Dowman", "Arsenal FC", True),
    ("BN-4", "Estêvão Willian", "Chelsea FC", True),
    ("BN-5", "Rio Ngumoha", "Liverpool FC", True),
    ("BN-6", "Michael Olise", "FC Bayern München", False),
    ("BN-7", "Désiré Doué", "Paris Saint-Germain", False),
    ("BN-8", "Lautaro Martínez", "FC Internazionale Milano", False),
    ("BN-9", "Khvicha Kvaratskhelia", "Paris Saint-Germain", False),
    ("BN-10", "Jobe Bellingham", "Borussia Dortmund", True),
]

HELIX = [
    ("H-1", "Diego Maradona", "SSC Napoli", False),
    ("H-2", "Estêvão Willian", "Chelsea FC", True),
    ("H-3", "Kylian Mbappé", "Real Madrid C.F.", False),
    ("H-4", "Franco Mastantuono", "Real Madrid C.F.", True),
    ("H-5", "Lennart Karl", "FC Bayern München", True),
    ("H-6", "Konstantinos Karetsas", "KRC Genk", True),
    ("H-7", "Ronaldinho", "FC Barcelona", False),
    ("H-8", "Neymar Jr", "Paris Saint-Germain", False),
    ("H-9", "Max Dowman", "Arsenal FC", True),
    ("H-10", "Jobe Bellingham", "Borussia Dortmund", True),
]

CHAMPION_REFRACTORS = [
    ("CC-1", "Nuno Mendes", "Paris Saint-Germain"),
    ("CC-2", "Willian Pacho", "Paris Saint-Germain"),
    ("CC-3", "Marquinhos", "Paris Saint-Germain"),
    ("CC-4", "Fabián Ruiz", "Paris Saint-Germain"),
    ("CC-5", "Vitinha", "Paris Saint-Germain"),
    ("CC-6", "João Neves", "Paris Saint-Germain"),
    ("CC-7", "Khvicha Kvaratskhelia", "Paris Saint-Germain"),
    ("CC-8", "Ousmane Dembélé", "Paris Saint-Germain"),
    ("CC-9", "Désiré Doué", "Paris Saint-Germain"),
    ("CC-10", "Bradley Barcola", "Paris Saint-Germain"),
    ("CC-11", "Kang-in Lee", "Paris Saint-Germain"),
    ("CC-12", "Paris Saint-Germain", "Paris Saint-Germain"),  # team card
]

# Trophy cards
TROPHIES = [
    ("CL-1", "UCL Trophy", "UEFA"),
    ("EL-1", "UEL Trophy", "UEFA"),
    ("CO-1", "UECL Trophy", "UEFA"),
]

THE_GRAIL = [
    ("G-1", "Zlatan Ibrahimović", "AFC Ajax"),
    ("G-3", "Zlatan Ibrahimović", "FC Internazionale Milano"),
]

CHROME_ANIME = [
    ("CA-1", "Michael Olise", "FC Bayern München", False),
    ("CA-2", "Kylian Mbappé", "Real Madrid C.F.", False),
    ("CA-3", "Lamine Yamal", "FC Barcelona", False),
    ("CA-4", "Estêvão Willian", "Chelsea FC", True),
    ("CA-5", "Désiré Doué", "Paris Saint-Germain", False),
    ("CA-6", "Rio Ngumoha", "Liverpool FC", True),
    ("CA-7", "Florian Wirtz", "Liverpool FC", False),
]

# ── Autograph Sets ───────────────────────────────────────────────────────────

CHROME_AUTOGRAPHS = [
    ("CA-A", "Antony", "Real Betis Balompié", False),
    ("CA-AB", "Alessandro Bastoni", "FC Internazionale Milano", False),
    ("CA-AD", "Alphonso Davies", "FC Bayern München", False),
    ("CA-AE", "Anthony Elanga", "Newcastle United", False),
    ("CA-AG", "Antoine Griezmann", "Atlético de Madrid", False),
    ("CA-AJ", "Alistair Johnston", "Celtic FC", False),
    ("CA-AK", "Arnaud Kalimuendo", "Nottingham Forest", False),
    ("CA-AL", "Julián Alvarez", "Atlético de Madrid", False),
    ("CA-AR", "Arda Güler", "Real Madrid C.F.", False),
    ("CA-AS", "Alejo Sarco", "Bayer 04 Leverkusen", True),
    ("CA-AT", "Aurélien Tchouaméni", "Real Madrid C.F.", False),
    ("CA-BB", "Bradley Barcola", "Paris Saint-Germain", False),
    ("CA-BG", "Bruno Guimarães", "Newcastle United", False),
    ("CA-BJ", "Brennan Johnson", "Tottenham Hotspur", False),
    ("CA-BR", "Julian Brandt", "Borussia Dortmund", False),
    ("CA-BS", "Bukayo Saka", "Arsenal FC", False),
    ("CA-CCV", "Cameron Carter-Vickers", "Celtic FC", False),
    ("CA-CG", "Cody Gakpo", "Liverpool FC", False),
    ("CA-CP", "Cole Palmer", "Chelsea FC", False),
    ("CA-CW", "Chris Wood", "Nottingham Forest", False),
    ("CA-DH", "Dean Huijsen", "Real Madrid C.F.", False),
    ("CA-DK", "Don-Angelo Konadu", "AFC Ajax", True),
    ("CA-DM", "Donyell Malen", "Aston Villa", False),
    ("CA-DO", "Dani Olmo", "FC Barcelona", False),
    ("CA-DR", "Declan Rice", "Arsenal FC", False),
    ("CA-DS", "Dominic Solanke", "Tottenham Hotspur", False),
    ("CA-DU", "Destiny Udogie", "Tottenham Hotspur", False),
    ("CA-DV", "Dušan Vlahović", "Juventus", False),
    ("CA-DZ", "Daizen Maeda", "Celtic FC", False),
    ("CA-EC", "Eduardo Camavinga", "Real Madrid C.F.", False),
    ("CA-EH", "Erling Haaland", "Manchester City", False),
    ("CA-EL", "Elye Wahi", "Eintracht Frankfurt", False),
    ("CA-EM", "Emiliano Martínez", "Aston Villa", False),
    ("CA-EN", "Arne Engels", "Celtic FC", False),
    ("CA-EW", "Estêvão Willian", "Chelsea FC", True),
    ("CA-FB", "Folarin Balogun", "AS Monaco", False),
    ("CA-FC", "Francisco Conceição", "Juventus", False),
    ("CA-FM", "Franco Mastantuono", "Real Madrid C.F.", True),
    ("CA-FT", "Ferran Torres", "FC Barcelona", False),
    ("CA-FV", "Federico Valverde", "Real Madrid C.F.", False),
    ("CA-G", "Gavi", "FC Barcelona", False),
    ("CA-GF", "Guille Fernández", "FC Barcelona", True),
    ("CA-GL", "Giovanni Leoni", "Liverpool FC", True),
    ("CA-GM", "Gabriel Martinelli", "Arsenal FC", False),
    ("CA-GO", "Anthony Gordon", "Newcastle United", False),
    ("CA-GU", "Serhou Guirassy", "Borussia Dortmund", False),
    ("CA-HA", "Reo Hatate", "Celtic FC", False),
    ("CA-HB", "Héctor Bellerín", "Real Betis Balompié", False),
    ("CA-HE", "Hugo Ekitike", "Liverpool FC", False),
    ("CA-HK", "Harry Kane", "FC Bayern München", False),
    ("CA-IK", "Ibrahima Konaté", "Liverpool FC", False),
    ("CA-IS", "Isco", "Real Betis Balompié", False),
    ("CA-JA", "Jamal Musiala", "FC Bayern München", False),
    ("CA-JB", "Jobe Bellingham", "Borussia Dortmund", True),
    ("CA-JF", "Jeremie Frimpong", "Liverpool FC", False),
    ("CA-JM", "John McGinn", "Aston Villa", False),
    ("CA-JN", "João Neves", "Paris Saint-Germain", False),
    ("CA-JP", "João Pedro", "Chelsea FC", False),
    ("CA-JU", "Jude Bellingham", "Real Madrid C.F.", False),
    ("CA-KDB", "Kevin De Bruyne", "SSC Napoli", False),
    ("CA-KH", "Khvicha Kvaratskhelia", "Paris Saint-Germain", False),
    ("CA-KI", "Joshua Kimmich", "FC Bayern München", False),
    ("CA-KK", "Konstantinos Karetsas", "KRC Genk", True),
    ("CA-KP", "Kendry Páez", "RC Strasbourg Alsace", True),
    ("CA-KY", "Kenan Yildiz", "Juventus", False),
    ("CA-LK", "Lennart Karl", "FC Bayern München", True),
    ("CA-LM", "Lautaro Martínez", "FC Internazionale Milano", False),
    ("CA-LO", "Loïs Openda", "Juventus", False),
    ("CA-LY", "Lamine Yamal", "FC Barcelona", False),
    ("CA-MB", "Maximilian Beier", "Borussia Dortmund", False),
    ("CA-MD", "Max Dowman", "Arsenal FC", True),
    ("CA-MG", "Marc Guiu", "Chelsea FC", False),
    ("CA-MI", "Michael Olise", "FC Bayern München", False),
    ("CA-MK", "Mohammed Kudus", "Tottenham Hotspur", False),
    ("CA-MN", "Manuel Neuer", "FC Bayern München", False),
    ("CA-MO", "Martin Ødegaard", "Arsenal FC", False),
    ("CA-MR", "Morgan Rogers", "Aston Villa", False),
    ("CA-MS", "Mohamed Salah", "Liverpool FC", False),
    ("CA-MT", "Mario Götze", "Eintracht Frankfurt", False),
    ("CA-MU", "Divine Mukasa", "Manchester City", True),
    ("CA-MZ", "Milos Kerkez", "Liverpool FC", False),
    ("CA-NI", "Nico Williams", "Athletic Club", False),
    ("CA-NM", "Nuno Mendes", "Paris Saint-Germain", False),
    ("CA-OB", "Oscar Bobb", "Manchester City", False),
    ("CA-OD", "Ousmane Dembélé", "Paris Saint-Germain", False),
    ("CA-OG", "Oscar Gloukh", "AFC Ajax", False),
    ("CA-OW", "Ollie Watkins", "Aston Villa", False),
    ("CA-P", "Pedri", "FC Barcelona", False),
    ("CA-PA", "Pablo Barrios", "Atlético de Madrid", False),
    ("CA-PB", "Paris Brunner", "AS Monaco", False),
    ("CA-PF", "Phil Foden", "Manchester City", False),
    ("CA-PG", "Pablo García", "Real Betis Balompié", True),
    ("CA-QJ", "Quim Junyent", "FC Barcelona", True),
    ("CA-QN", "Quentin Ndjantou", "Paris Saint-Germain", True),
    ("CA-RD", "Rodrygo", "Real Madrid C.F.", False),
    ("CA-RH", "Rasmus Højlund", "SSC Napoli", False),
    ("CA-RHE", "Reigan Heskey", "Manchester City", True),
    ("CA-RL", "Robert Lewandowski", "FC Barcelona", False),
    ("CA-RN", "Rio Ngumoha", "Liverpool FC", True),
    ("CA-RW", "Reggie Walsh", "Chelsea FC", True),
    ("CA-S", "Savinho", "Manchester City", False),
    ("CA-ST", "Sandro Tonali", "Newcastle United", False),
    ("CA-TR", "Tijjani Reijnders", "Manchester City", False),
    ("CA-VJ", "Vini Jr.", "Real Madrid C.F.", False),
    ("CA-VVD", "Virgil van Dijk", "Liverpool FC", False),
    ("CA-WP", "Willian Pacho", "Paris Saint-Germain", False),
    ("CA-WS", "William Saliba", "Arsenal FC", False),
    ("CA-XS", "Xavi Simons", "Tottenham Hotspur", False),
    ("CA-IA", "Adriano", "FC Internazionale Milano", False),
]

CHROME_LEGENDS_AUTOGRAPHS = [
    ("CLA-ADP", "Alessandro Del Piero", "Juventus"),
    ("CLA-AI", "Andrés Iniesta", "FC Barcelona"),
    ("CLA-AP", "Andrea Pirlo", "AC Milan"),
    ("CLA-AS", "Alan Shearer", "Newcastle United"),
    ("CLA-BA", "Roberto Baggio", "Juventus"),
    ("CLA-BS", "Bastian Schweinsteiger", "FC Bayern München"),
    ("CLA-CT", "Carlos Tevez", "Juventus"),
    ("CLA-CV", "Christian Vieri", "FC Internazionale Milano"),
    ("CLA-DA", "Daniel Sturridge", "Liverpool FC"),
    ("CLA-DS", "David Silva", "Manchester City"),
    ("CLA-DT", "David Trezeguet", "Juventus"),
    ("CLA-EH", "Eden Hazard", "Chelsea FC"),
    ("CLA-FI", "Filippo Inzaghi", "AC Milan"),
    ("CLA-FL", "Frank Lampard", "Chelsea FC"),
    ("CLA-FR", "Franck Ribéry", "FC Bayern München"),
    ("CLA-FT", "Fernando Torres", "Liverpool FC"),
    ("CLA-G", "Guti", "Real Madrid C.F."),
    ("CLA-GB", "Gareth Bale", "Tottenham Hotspur"),
    ("CLA-GN", "Gary Neville", "Manchester United"),
    ("CLA-HL", "Henrik Larsson", "Celtic FC"),
    ("CLA-IC", "Iker Casillas", "Real Madrid C.F."),
    ("CLA-IW", "Ian Wright", "Arsenal FC"),
    ("CLA-JC", "Jamie Carragher", "Liverpool FC"),
    ("CLA-JM", "Juan Mata", "Chelsea FC"),
    ("CLA-JT", "John Terry", "Chelsea FC"),
    ("CLA-KK", "Kaká", "AC Milan"),
    ("CLA-LM", "Lionel Messi", "FC Barcelona"),
    ("CLA-LO", "Lothar Matthäus", "FC Internazionale Milano"),
    ("CLA-LS", "Luis Suárez", "FC Barcelona"),
    ("CLA-MD", "Luka Modrić", "Tottenham Hotspur"),
    ("CLA-MK", "Miroslav Klose", "FC Bayern München"),
    ("CLA-MO", "Mesut Özil", "Real Madrid C.F."),
    ("CLA-MR", "Marco Reus", "Borussia Dortmund"),
    ("CLA-NJ", "Neymar Jr", "Paris Saint-Germain"),
    ("CLA-PL", "Philipp Lahm", "FC Bayern München"),
    ("CLA-PM", "Paolo Maldini", "AC Milan"),
    ("CLA-PN", "Pavel Nedvěd", "Juventus"),
    ("CLA-PS", "Paul Scholes", "Manchester United"),
    ("CLA-R", "Rivaldo", "FC Barcelona"),
    ("CLA-R10", "Ronaldinho", "FC Barcelona"),
    ("CLA-R9", "Ronaldo", "FC Internazionale Milano"),
    ("CLA-RA", "Raúl", "Real Madrid C.F."),
    ("CLA-RG", "Ryan Giggs", "Manchester United"),
    ("CLA-RM", "Riyad Mahrez", "Manchester City"),
    ("CLA-RO", "Romário", "FC Barcelona"),
    ("CLA-RVP", "Robin van Persie", "Manchester United"),
    ("CLA-SA", "Sergio Agüero", "Manchester City"),
    ("CLA-SAF", "Sir Alex Ferguson", "Manchester United"),
    ("CLA-SB", "Sergio Busquets", "FC Barcelona"),
    ("CLA-SC", "Santi Cazorla", "Arsenal FC"),
    ("CLA-SDB", "David Beckham", "Real Madrid C.F."),
    ("CLA-SE", "Samuel Eto'o", "FC Internazionale Milano"),
    ("CLA-SH", "Andriy Shevchenko", "AC Milan"),
    ("CLA-SK", "Shinji Kagawa", "Borussia Dortmund"),
    ("CLA-SM", "Sadio Mané", "Liverpool FC"),
    ("CLA-TH", "Thierry Henry", "Arsenal FC"),
    ("CLA-TK", "Toni Kroos", "Real Madrid C.F."),
    ("CLA-TS", "Thiago Silva", "Paris Saint-Germain"),
    ("CLA-WR", "Wayne Rooney", "Manchester United"),
    ("CLA-WS", "Wesley Sneijder", "FC Internazionale Milano"),
    ("CLA-XH", "Xavi Hernández", "FC Barcelona"),
    ("CLA-YT", "Yaya Touré", "Manchester City"),
    ("CLA-ZI", "Zlatan Ibrahimović", "Paris Saint-Germain"),
    ("CLA-ZZ", "Zinédine Zidane", "Real Madrid C.F."),
]

FUTURE_STARS_AUTOGRAPHS = [
    ("FSA-E", "Endrick", "Real Madrid C.F.", False),
    ("FSA-GQ", "Geovany Quenda", "Sporting Clube de Portugal", False),
    ("FSA-MLS", "Myles Lewis-Skelly", "Arsenal FC", False),
    ("FSA-MM", "Mikey Moore", "Rangers F.C.", False),
    ("FSA-RM", "Rodrigo Mora", "FC Porto", False),
    ("FSA-SM", "Senny Mayulu", "Paris Saint-Germain", False),
]

# Dual Autographs: (code, player1, team1, player2, team2)
DUAL_AUTOGRAPHS = [
    ("CDA-BF", "David Beckham", "Manchester United", "Sir Alex Ferguson", "Manchester United"),
    ("CDA-BM", "Bastian Schweinsteiger", "FC Bayern München", "Miroslav Klose", "FC Bayern München"),
    ("CDA-CL", "Cole Palmer", "Chelsea FC", "Frank Lampard", "Chelsea FC"),
    ("CDA-GA", "Antoine Griezmann", "Atlético de Madrid", "Julián Alvarez", "Atlético de Madrid"),
    ("CDA-HF", "Erling Haaland", "Manchester City", "Phil Foden", "Manchester City"),
    ("CDA-HN", "Reo Hatate", "Celtic FC", "Shunsuke Nakamura", "Celtic FC"),
    ("CDA-IR", "Zlatan Ibrahimović", "FC Internazionale Milano", "Ronaldo", "FC Internazionale Milano"),
    ("CDA-KB", "Konstantinos Karetsas", "KRC Genk", "Kevin De Bruyne", "KRC Genk"),
    ("CDA-KP", "Kaká", "AC Milan", "Andrea Pirlo", "AC Milan"),
    ("CDA-KR", "Shinji Kagawa", "Borussia Dortmund", "Marco Reus", "Borussia Dortmund"),
    ("CDA-MB", "Luka Modrić", "Tottenham Hotspur", "Gareth Bale", "Tottenham Hotspur"),
    ("CDA-OR", "Martin Ødegaard", "Arsenal FC", "Declan Rice", "Arsenal FC"),
    ("CDA-PB", "Alessandro Del Piero", "Juventus", "Roberto Baggio", "Juventus"),
    ("CDA-PG", "Paul Scholes", "Manchester United", "Ryan Giggs", "Manchester United"),
    ("CDA-PI", "Pedri", "FC Barcelona", "Andrés Iniesta", "FC Barcelona"),
    ("CDA-RA", "Ronaldo", "FC Internazionale Milano", "Adriano", "FC Internazionale Milano"),
    ("CDA-RE", "Ronaldinho", "FC Barcelona", "Samuel Eto'o", "FC Barcelona"),
    ("CDA-RL", "Raphinha", "FC Barcelona", "Robert Lewandowski", "FC Barcelona"),
    ("CDA-RV", "Rio Ferdinand", "Manchester United", "Nemanja Vidić", "Manchester United"),
    ("CDA-SG", "Mohamed Salah", "Liverpool FC", "Steven Gerrard", "Liverpool FC"),
    ("CDA-SH", "Bukayo Saka", "Arsenal FC", "Thierry Henry", "Arsenal FC"),
    ("CDA-SK", "Xavi Simons", "Tottenham Hotspur", "Mohammed Kudus", "Tottenham Hotspur"),
    ("CDA-WP", "Wayne Rooney", "Manchester United", "Robin van Persie", "Manchester United"),
    ("CDA-YM", "Lamine Yamal", "FC Barcelona", "Lionel Messi", "FC Barcelona"),
    ("CDA-YN", "Lamine Yamal", "FC Barcelona", "Neymar Jr", "FC Barcelona"),
    ("CDA-ZR", "Zinédine Zidane", "Real Madrid C.F.", "Raúl", "Real Madrid C.F."),
]

# Triple Autographs: (code, [(player, team), ...])
TRIPLE_AUTOGRAPHS = [
    ("CTA-BSG", [("David Beckham", "Manchester United"), ("Paul Scholes", "Manchester United"), ("Ryan Giggs", "Manchester United")]),
    ("CTA-CBB", [("Giorgio Chiellini", "Juventus"), ("Leonardo Bonucci", "Juventus"), ("Gianluigi Buffon", "Juventus")]),
    ("CTA-CBN", [("Petr Čech", "Chelsea FC"), ("Gianluigi Buffon", "Juventus"), ("Manuel Neuer", "FC Bayern München")]),
    ("CTA-KGS", [("Kevin Keegan", "Newcastle United"), ("Paul Gascoigne", "Newcastle United"), ("Alan Shearer", "Newcastle United")]),
    ("CTA-KPG", [("Kaká", "AC Milan"), ("Andrea Pirlo", "AC Milan"), ("Gennaro Gattuso", "AC Milan")]),
    ("CTA-KSR", [("Patrick Kluivert", "AFC Ajax"), ("Clarence Seedorf", "AFC Ajax"), ("Frank Rijkaard", "AFC Ajax")]),
    ("CTA-MND", [("Paolo Maldini", "AC Milan"), ("Alessandro Nesta", "AC Milan"), ("Dida", "AC Milan")]),
    ("CTA-MSN", [("Lionel Messi", "FC Barcelona"), ("Luis Suárez", "FC Barcelona"), ("Neymar Jr", "FC Barcelona")]),
    ("CTA-NRR", [("Neymar Jr", "FC Barcelona"), ("Ronaldinho", "FC Barcelona"), ("Rivaldo", "FC Barcelona")]),
    ("CTA-PGL", [("Pedri", "FC Barcelona"), ("Gavi", "FC Barcelona"), ("Fermín López", "FC Barcelona")]),
    ("CTA-SFM", [("Mohamed Salah", "Liverpool FC"), ("Roberto Firmino", "Liverpool FC"), ("Sadio Mané", "Liverpool FC")]),
    ("CTA-SGR", [("William Saliba", "Arsenal FC"), ("Gabriel", "Arsenal FC"), ("Declan Rice", "Arsenal FC")]),
    ("CTA-TAG", [("Fernando Torres", "Atlético de Madrid"), ("Sergio Agüero", "Atlético de Madrid"), ("Antoine Griezmann", "Atlético de Madrid")]),
    ("CTA-ZBP", [("Zinédine Zidane", "Juventus"), ("Roberto Baggio", "Juventus"), ("Alessandro Del Piero", "Juventus")]),
]

# Quad Autographs: (code, [(player, team), ...])
QUAD_AUTOGRAPHS = [
    ("QA-2024", [("Vini Jr.", "Real Madrid C.F."), ("Rodrygo", "Real Madrid C.F."), ("Jude Bellingham", "Real Madrid C.F."), ("Arda Güler", "Real Madrid C.F.")]),
    ("QA-JOGA", [("Ronaldo", "FC Internazionale Milano"), ("Neymar Jr", "Paris Saint-Germain"), ("Ronaldinho", "FC Barcelona"), ("Kaká", "AC Milan")]),
    ("QA-MASIA", [("Lionel Messi", "FC Barcelona"), ("Xavi Hernández", "FC Barcelona"), ("Andrés Iniesta", "FC Barcelona"), ("Sergio Busquets", "FC Barcelona")]),
]

BLACK_LAZER_AUTOGRAPHS = [
    ("BLA-ADP", "Alessandro Del Piero", "Juventus", False),
    ("BLA-BS", "Bastian Schweinsteiger", "FC Bayern München", False),
    ("BLA-DM", "Daizen Maeda", "Celtic FC", False),
    ("BLA-DV", "Dušan Vlahović", "Juventus", False),
    ("BLA-EH", "Erling Haaland", "Manchester City", False),
    ("BLA-EW", "Estêvão Willian", "Chelsea FC", True),
    ("BLA-FB", "Franck Ribéry", "FC Bayern München", False),
    ("BLA-FL", "Frank Lampard", "Chelsea FC", False),
    ("BLA-FM", "Franco Mastantuono", "Real Madrid C.F.", True),
    ("BLA-GB", "Gareth Bale", "Tottenham Hotspur", False),
    ("BLA-HK", "Harry Kane", "FC Bayern München", False),
    ("BLA-JA", "Julián Alvarez", "Atlético de Madrid", False),
    ("BLA-JM", "Jamal Musiala", "FC Bayern München", False),
    ("BLA-JU", "Jude Bellingham", "Real Madrid C.F.", False),
    ("BLA-KA", "Kaká", "AC Milan", False),
    ("BLA-KDB", "Kevin De Bruyne", "SSC Napoli", False),
    ("BLA-KK", "Konstantinos Karetsas", "KRC Genk", True),
    ("BLA-LK", "Lennart Karl", "FC Bayern München", True),
    ("BLA-LM", "Lionel Messi", "FC Barcelona", False),
    ("BLA-LY", "Lamine Yamal", "FC Barcelona", False),
    ("BLA-MA", "Lautaro Martínez", "FC Internazionale Milano", False),
    ("BLA-MD", "Max Dowman", "Arsenal FC", True),
    ("BLA-MK", "Mohammed Kudus", "Tottenham Hotspur", False),
    ("BLA-MO", "Martin Ødegaard", "Arsenal FC", False),
    ("BLA-MS", "Mohamed Salah", "Liverpool FC", False),
    ("BLA-NJ", "Neymar Jr", "Paris Saint-Germain", False),
    ("BLA-OD", "Ousmane Dembélé", "Paris Saint-Germain", False),
    ("BLA-P", "Pedri", "FC Barcelona", False),
    ("BLA-PF", "Phil Foden", "Manchester City", False),
    ("BLA-PM", "Paolo Maldini", "AC Milan", False),
    ("BLA-R10", "Ronaldinho", "FC Barcelona", False),
    ("BLA-R9", "Ronaldo", "FC Internazionale Milano", False),
    ("BLA-RA", "Raúl", "Real Madrid C.F.", False),
    ("BLA-RL", "Robert Lewandowski", "FC Barcelona", False),
    ("BLA-RN", "Rio Ngumoha", "Liverpool FC", True),
    ("BLA-RW", "Reggie Walsh", "Chelsea FC", True),
    ("BLA-SC", "Santi Cazorla", "Arsenal FC", False),
    ("BLA-SDB", "David Beckham", "Real Madrid C.F.", False),
    ("BLA-SE", "Samuel Eto'o", "FC Internazionale Milano", False),
    ("BLA-SK", "Shinji Kagawa", "Borussia Dortmund", False),
    ("BLA-SM", "Sadio Mané", "Liverpool FC", False),
    ("BLA-TH", "Thierry Henry", "Arsenal FC", False),
    ("BLA-WR", "Wayne Rooney", "Manchester United", False),
    ("BLA-XS", "Xavi Simons", "Tottenham Hotspur", False),
    ("BLA-ZZ", "Zinédine Zidane", "Real Madrid C.F.", False),
]

# Piece of Club History: (code, [(player, team), ...])
PIECE_OF_CLUB_HISTORY = [
    ("CH-1900", [("Franz Beckenbauer", "FC Bayern München"), ("Lothar Matthäus", "FC Bayern München"), ("Philipp Lahm", "FC Bayern München"), ("Bastian Schweinsteiger", "FC Bayern München"), ("Manuel Neuer", "FC Bayern München"), ("Jamal Musiala", "FC Bayern München")]),
    ("CH-BARCA", [("Ronaldinho", "FC Barcelona"), ("Samuel Eto'o", "FC Barcelona"), ("Xavi Hernández", "FC Barcelona"), ("Lionel Messi", "FC Barcelona"), ("Pedri", "FC Barcelona"), ("Lamine Yamal", "FC Barcelona")]),
    ("CH-COYG", [("Tony Adams", "Arsenal FC"), ("Ian Wright", "Arsenal FC"), ("Dennis Bergkamp", "Arsenal FC"), ("Thierry Henry", "Arsenal FC"), ("Martin Ødegaard", "Arsenal FC"), ("Bukayo Saka", "Arsenal FC")]),
    ("CH-FORZA", [("Franco Baresi", "AC Milan"), ("Marco van Basten", "AC Milan"), ("Paolo Maldini", "AC Milan"), ("Andriy Shevchenko", "AC Milan"), ("Andrea Pirlo", "AC Milan"), ("Kaká", "AC Milan")]),
    ("CH-YNWA", [("Kevin Keegan", "Liverpool FC"), ("Kenny Dalglish", "Liverpool FC"), ("Jamie Carragher", "Liverpool FC"), ("Steven Gerrard", "Liverpool FC"), ("Virgil van Dijk", "Liverpool FC"), ("Mohamed Salah", "Liverpool FC")]),
]

GLOBAL_ATTRACTION = [
    ("GA26-AD", "Alphonso Davies", "FC Bayern München", False),
    ("GA26-CG", "Cody Gakpo", "Liverpool FC", False),
    ("GA26-DM", "Daizen Maeda", "Celtic FC", False),
    ("GA26-DR", "Declan Rice", "Arsenal FC", False),
    ("GA26-EH", "Erling Haaland", "Manchester City", False),
    ("GA26-EW", "Estêvão Willian", "Chelsea FC", True),
    ("GA26-FB", "Folarin Balogun", "AS Monaco", False),
    ("GA26-FM", "Franco Mastantuono", "Real Madrid C.F.", True),
    ("GA26-HK", "Harry Kane", "FC Bayern München", False),
    ("GA26-JA", "Julián Alvarez", "Atlético de Madrid", False),
    ("GA26-JB", "Jude Bellingham", "Real Madrid C.F.", False),
    ("GA26-JM", "Jamal Musiala", "FC Bayern München", False),
    ("GA26-KDB", "Kevin De Bruyne", "SSC Napoli", False),
    ("GA26-LM", "Lionel Messi", "FC Barcelona", False),
    ("GA26-LY", "Lamine Yamal", "FC Barcelona", False),
    ("GA26-MK", "Mohammed Kudus", "Tottenham Hotspur", False),
    ("GA26-MO", "Luka Modrić", "Tottenham Hotspur", False),
    ("GA26-MS", "Mohamed Salah", "Liverpool FC", False),
    ("GA26-OD", "Ousmane Dembélé", "Paris Saint-Germain", False),
    ("GA26-OM", "Martin Ødegaard", "Arsenal FC", False),
    ("GA26-P", "Pedri", "FC Barcelona", False),
    ("GA26-VJ", "Vini Jr.", "Real Madrid C.F.", False),
    ("GA26-VVD", "Virgil van Dijk", "Liverpool FC", False),
    ("GA26-WM", "Weston McKennie", "Juventus", False),
]

ROAD_TO_GLORY = [
    ("RTG-AD", "Alessandro Del Piero", "Juventus"),
    ("RTG-ADM", "Ángel Di María", "Real Madrid C.F."),
    ("RTG-AG", "Arda Güler", "Real Madrid C.F."),
    ("RTG-AI", "Andrés Iniesta", "FC Barcelona"),
    ("RTG-AP", "Andrea Pirlo", "AC Milan"),
    ("RTG-AS", "Andriy Shevchenko", "AC Milan"),
    ("RTG-BB", "Bradley Barcola", "Paris Saint-Germain"),
    ("RTG-CS", "Clarence Seedorf", "AC Milan"),
    ("RTG-CT", "Carlos Tevez", "Manchester United"),
    ("RTG-DA", "Alphonso Davies", "FC Bayern München"),
    ("RTG-EH", "Erling Haaland", "Manchester City"),
    ("RTG-FI", "Filippo Inzaghi", "AC Milan"),
    ("RTG-FL", "Frank Lampard", "Chelsea FC"),
    ("RTG-FM", "Fernando Morientes", "Real Madrid C.F."),
    ("RTG-FR", "Franck Ribéry", "FC Bayern München"),
    ("RTG-FV", "Federico Valverde", "Real Madrid C.F."),
    ("RTG-GB", "Gareth Bale", "Real Madrid C.F."),
    ("RTG-GG", "Gennaro Gattuso", "AC Milan"),
    ("RTG-JB", "Jude Bellingham", "Real Madrid C.F."),
    ("RTG-JC", "Jamie Carragher", "Liverpool FC"),
    ("RTG-JK", "Joshua Kimmich", "FC Bayern München"),
    ("RTG-JM", "Javier Mascherano", "FC Barcelona"),
    ("RTG-JN", "João Neves", "Paris Saint-Germain"),
    ("RTG-JU", "Juan Mata", "Chelsea FC"),
    ("RTG-KA", "Kaká", "AC Milan"),
    ("RTG-KD", "Kenny Dalglish", "Liverpool FC"),
    ("RTG-LM", "Lionel Messi", "FC Barcelona"),
    ("RTG-LS", "Luis Suárez", "FC Barcelona"),
    ("RTG-MN", "Manuel Neuer", "FC Bayern München"),
    ("RTG-MS", "Matthias Sammer", "Borussia Dortmund"),
    ("RTG-MU", "Jamal Musiala", "FC Bayern München"),
    ("RTG-MVB", "Marco van Basten", "AC Milan"),
    ("RTG-NV", "Nemanja Vidić", "Manchester United"),
    ("RTG-OD", "Ousmane Dembélé", "Paris Saint-Germain"),
    ("RTG-PC", "Petr Čech", "Chelsea FC"),
    ("RTG-PF", "Phil Foden", "Manchester City"),
    ("RTG-PK", "Patrick Kluivert", "AFC Ajax"),
    ("RTG-PL", "Philipp Lahm", "FC Bayern München"),
    ("RTG-PM", "Paolo Maldini", "AC Milan"),
    ("RTG-PS", "Paul Scholes", "Manchester United"),
    ("RTG-R10", "Ronaldinho", "FC Barcelona"),
    ("RTG-RA", "Raúl", "Real Madrid C.F."),
    ("RTG-RB", "Roberto Firmino", "Liverpool FC"),
    ("RTG-RC", "Roberto Carlos", "Real Madrid C.F."),
    ("RTG-RD", "Rodrygo", "Real Madrid C.F."),
    ("RTG-RG", "Ryan Giggs", "Manchester United"),
    ("RTG-RI", "Frank Rijkaard", "AFC Ajax"),
    ("RTG-RK", "Ronald Koeman", "FC Barcelona"),
    ("RTG-RM", "Riyad Mahrez", "Manchester City"),
    ("RTG-SA", "Mohamed Salah", "Liverpool FC"),
    ("RTG-SB", "Sergio Busquets", "FC Barcelona"),
    ("RTG-SC", "Bastian Schweinsteiger", "FC Bayern München"),
    ("RTG-SDB", "David Beckham", "Manchester United"),
    ("RTG-SE", "Samuel Eto'o", "FC Internazionale Milano"),
    ("RTG-SM", "Sadio Mané", "Liverpool FC"),
    ("RTG-TK", "Toni Kroos", "Real Madrid C.F."),
    ("RTG-TM", "Thomas Müller", "FC Bayern München"),
    ("RTG-VD", "Virgil van Dijk", "Liverpool FC"),
    ("RTG-VJ", "Vini Jr.", "Real Madrid C.F."),
    ("RTG-WR", "Wayne Rooney", "Manchester United"),
    ("RTG-WS", "Wesley Sneijder", "FC Internazionale Milano"),
    ("RTG-XH", "Xavi Hernández", "FC Barcelona"),
    ("RTG-ZZ", "Zinédine Zidane", "Real Madrid C.F."),
]

BOWMAN_YOUTH_LEAGUE_AUTOGRAPHS = [
    ("BYA-MA", "Mathis Albert", "Borussia Dortmund"),
    ("BYA-SI", "Samuele Inacio", "Borussia Dortmund"),
    ("BYA-LWB", "Lucá Williams-Barnett", "Tottenham Hotspur"),
    ("BYA-TL", "Teddie Lamb", "Manchester City"),
]

MARKS_OF_EXCELLENCE = [
    ("ME-AG3", "Arda Güler", "Real Madrid C.F."),
    ("ME-BB1", "Bradley Barcola", "Paris Saint-Germain"),
    ("ME-CP1", "Cole Palmer", "Chelsea FC"),
    ("ME-HK1", "Harry Kane", "FC Bayern München"),
    ("ME-LM1", "Lionel Messi", "FC Barcelona"),
    ("ME-MS1", "Mohamed Salah", "Liverpool FC"),
    ("ME-SAF1", "Sir Alex Ferguson", "Manchester United"),
    ("ME-TO1", "Fernando Torres", "Chelsea FC"),
]

UCL_FINAL_PERFORMERS = [
    ("UFH-CB", "Colin Brittain", "Linkin Park"),
    ("UFH-DF", "Dave \"Phoenix\" Farrell", "Linkin Park"),
    ("UFH-EA", "Emily Armstrong", "Linkin Park"),
    ("UFH-JH", "Joe Hahn", "Linkin Park"),
    ("UFH-MS", "Mike Shinoda", "Linkin Park"),
]

# UCL Final Performers Dual Autographs
UCL_FINAL_PERFORMERS_DUAL = [
    ("LPDA-SA", "Mike Shinoda", "Linkin Park", "Emily Armstrong", "Linkin Park"),
]

SUPERIOR_SIGNATURES_VETERANS = [
    ("SSV-AG", "Antoine Griezmann", "Atlético de Madrid", False),
    ("SSV-DM", "Divine Mukasa", "Manchester City", True),
    ("SSV-HK", "Harry Kane", "FC Bayern München", False),
    ("SSV-JA", "Julián Alvarez", "Atlético de Madrid", False),
    ("SSV-JB", "Jude Bellingham", "Real Madrid C.F.", False),
    ("SSV-JM", "Jamal Musiala", "FC Bayern München", False),
    ("SSV-LK", "Lennart Karl", "FC Bayern München", True),
    ("SSV-MD", "Max Dowman", "Arsenal FC", True),
    ("SSV-QJ", "Quim Junyent", "FC Barcelona", True),
    ("SSV-RN", "Rio Ngumoha", "Liverpool FC", True),
    ("SSV-V", "Vini Jr.", "Real Madrid C.F.", False),
]

SUPERIOR_SIGNATURES_LEGENDS = [
    ("SSL-AI", "Andrés Iniesta", "FC Barcelona"),
    ("SSL-BG", "Dennis Bergkamp", "Arsenal FC"),
    ("SSL-GB", "Gareth Bale", "Real Madrid C.F."),
    ("SSL-LJ", "Freddie Ljungberg", "Arsenal FC"),
    ("SSL-LM", "Lionel Messi", "FC Barcelona"),
    ("SSL-RB", "Roberto Baggio", "FC Internazionale Milano"),
    ("SSL-TH", "Thierry Henry", "Arsenal FC"),
]


# ── Build ────────────────────────────────────────────────────────────────────

def build():
    players = {}  # name -> {is_rookie, appearances}
    sections = {}  # insert_set_name -> {parallels, cards}

    def add_card(insert_set, card_number, player, team, is_rookie, co_players=None):
        if player not in players:
            players[player] = {"is_rookie": False, "appearances": []}
        if is_rookie:
            players[player]["is_rookie"] = True
        app = {
            "insert_set": insert_set,
            "card_number": card_number,
            "team": team,
            "is_rookie": is_rookie,
        }
        if co_players:
            app["co_players"] = co_players
        players[player]["appearances"].append(app)
        if insert_set not in sections:
            sections[insert_set] = {"parallels": NO_PARALLELS, "cards": []}
        sections[insert_set]["cards"].append({
            "card_number": card_number,
            "player": player,
            "team": team,
            "is_rookie": is_rookie,
        })

    # ── Base Set (non-Future Stars) ──
    for num, name, team, is_rc in BASE_SET:
        if num not in FUTURE_STARS_NUMBERS:
            add_card("Base Set", num, name, team, is_rc)

    # ── Base - Future Stars ──
    for num, name, team, is_rc in BASE_SET:
        if num in FUTURE_STARS_NUMBERS:
            add_card("Base - Future Stars", num, name, team, is_rc)

    # ── Radiating Rookies ──
    base_map = {num: (name, team, is_rc) for num, name, team, is_rc in BASE_SET}
    for num in RADIATING_ROOKIES_NUMBERS:
        name, team, is_rc = base_map[num]
        add_card("Topps Chrome Radiating Rookies", num, name, team, True)

    # ── Standard inserts (3-tuple: no RC flag) ──
    for data, insert_set_name in [
        (BOWMAN_UEFA_YOUTH_LEAGUE, "Bowman UEFA Youth League"),
        (LAST_DANCE, "Last Dance"),
        (SILENCED, "Silenced"),
        (VENI_VIDI_VICI, "Veni Vidi Vici"),
        (ULTRA_VIOLET, "Ultra Violet"),
        (CHAMPION_REFRACTORS, "Topps Chrome Champion Refractors"),
        (TROPHIES, "Trophies"),
        (THE_GRAIL, "The Grail"),
        (BIONIC, "Bionic"),
    ]:
        for row in data:
            num, name, team = row[0], row[1], row[2]
            add_card(insert_set_name, num, name, team, False)

    # ── Standard inserts (4-tuple: with RC flag) ──
    for data, insert_set_name in [
        (WONDERKIDS, "Wonderkids"),
        (SHADOW_ETCH, "Shadow Etch"),
        (BUDAPEST_AT_NIGHT, "Budapest at Night"),
        (HELIX, "Helix"),
        (CHROME_ANIME, "Chrome Anime"),
    ]:
        for row in data:
            num, name, team, is_rc = row[0], row[1], row[2], row[3]
            add_card(insert_set_name, num, name, team, is_rc)

    # ── Power Players (mixed 3/4-tuple) ──
    for row in POWER_PLAYERS:
        num, name, team = row[0], row[1], row[2]
        is_rc = row[3] if len(row) == 4 else False
        add_card("Power Players", num, name, team, is_rc)

    # ── Youthquake ──
    for num, name, team, is_rc in YOUTHQUAKE:
        add_card("Topps Chrome Youthquake", num, name, team, is_rc)

    # ── Metaverse (mixed 3/4-tuple) ──
    for row in METAVERSE:
        num, name, team = row[0], row[1], row[2]
        is_rc = row[3] if len(row) == 4 else False
        add_card("Metaverse", num, name, team, is_rc)

    # ── Autograph sets (4-tuple) ──
    for data, insert_set_name in [
        (CHROME_AUTOGRAPHS, "Chrome Autograph Cards"),
        (BLACK_LAZER_AUTOGRAPHS, "Black Lazer Autographs"),
        (FUTURE_STARS_AUTOGRAPHS, "Future Stars Autograph Variation"),
        (SUPERIOR_SIGNATURES_VETERANS, "Chrome Superior Signatures Veterans and Rookies"),
    ]:
        for num, name, team, is_rc in data:
            add_card(insert_set_name, num, name, team, is_rc)

    # ── Autograph sets (3-tuple, no RC) ──
    for data, insert_set_name in [
        (CHROME_LEGENDS_AUTOGRAPHS, "Chrome Legends Autograph Cards"),
        (ROAD_TO_GLORY, "Road to Glory Autographs"),
        (BOWMAN_YOUTH_LEAGUE_AUTOGRAPHS, "Bowman UEFA Youth League Autographs"),
        (MARKS_OF_EXCELLENCE, "Marks of Excellence"),
        (UCL_FINAL_PERFORMERS, "UCL Final Performers Autographs"),
        (SUPERIOR_SIGNATURES_LEGENDS, "Chrome Superior Signatures Legends"),
    ]:
        for num, name, team in data:
            add_card(insert_set_name, num, name, team, False)

    # ── Global Attraction (4-tuple) ──
    for num, name, team, is_rc in GLOBAL_ATTRACTION:
        add_card("Global Attraction Summer of 2026 Autographs", num, name, team, is_rc)

    # ── Dual Autographs ──
    for code, p1, t1, p2, t2 in DUAL_AUTOGRAPHS:
        add_card("Chrome Dual Autograph Cards", code, p1, t1, False, co_players=[p2])
        add_card("Chrome Dual Autograph Cards", code, p2, t2, False, co_players=[p1])

    # ── UCL Final Performers Dual Autographs ──
    for code, p1, t1, p2, t2 in UCL_FINAL_PERFORMERS_DUAL:
        add_card("UCL Final Performers Dual Autographs", code, p1, t1, False, co_players=[p2])
        add_card("UCL Final Performers Dual Autographs", code, p2, t2, False, co_players=[p1])

    # ── Triple Autographs ──
    for code, players_list in TRIPLE_AUTOGRAPHS:
        names = [p[0] for p in players_list]
        for name, team in players_list:
            co = [n for n in names if n != name]
            add_card("Chrome Triple Autograph Cards", code, name, team, False, co_players=co)

    # ── Quad Autographs ──
    for code, players_list in QUAD_AUTOGRAPHS:
        names = [p[0] for p in players_list]
        for name, team in players_list:
            co = [n for n in names if n != name]
            add_card("Chrome Quad Autograph Cards", code, name, team, False, co_players=co)

    # ── Piece of Club History ──
    for code, players_list in PIECE_OF_CLUB_HISTORY:
        names = [p[0] for p in players_list]
        for name, team in players_list:
            co = [n for n in names if n != name]
            add_card("Piece of Club History Autograph Book Cards", code, name, team, False, co_players=co)

    # ── Propagate is_rookie to all appearances ──
    rc_players = {p for p, d in players.items() if d["is_rookie"]}
    for p in rc_players:
        for app in players[p]["appearances"]:
            app["is_rookie"] = True
        for sec in sections.values():
            for card in sec["cards"]:
                if card["player"] == p:
                    card["is_rookie"] = True

    # ── Build sections list ──
    sections_list = []
    for insert_set, data in sections.items():
        sections_list.append({
            "insert_set": insert_set,
            "parallels": data["parallels"],
            "cards": data["cards"],
        })

    # ── Build players list with stats ──
    players_list = []
    for name, data in players.items():
        unique_cards = len(data["appearances"])
        players_list.append({
            "player": name,
            "appearances": data["appearances"],
            "stats": {
                "unique_cards": unique_cards,
                "total_print_run": 0,
                "one_of_ones": 0,
                "insert_sets": len({a["insert_set"] for a in data["appearances"]}),
            },
        })

    players_list.sort(key=lambda p: p["player"])

    output = {
        "set_name": "2025-26 Topps Chrome UEFA Club Competitions",
        "sport": "Soccer",
        "season": "2025-26",
        "league": "UEFA",
        "sections": sections_list,
        "players": players_list,
    }

    with open("chrome_uefa_2526_parsed.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    total_cards = sum(len(s["cards"]) for s in sections_list)
    print(f"Sections: {len(sections_list)}")
    print(f"Players:  {len(players_list)}")
    print(f"Cards:    {total_cards}")


if __name__ == "__main__":
    build()
