#!/usr/bin/env python3
"""Parser for 2026 Topps Finest Premier League."""
import json, re

# ---------------------------------------------------------------------------
# Parallel definitions
# ---------------------------------------------------------------------------

BASE_PARALLELS = [
    {"name": "Refractor",              "print_run": None},
    {"name": "Green Refractor",        "print_run": 199},
    {"name": "Blue Refractor",         "print_run": 150},
    {"name": "Purple Refractor",       "print_run": 99},
    {"name": "Gold Refractor",         "print_run": 50},
    {"name": "Black Refractor",        "print_run": 25},
    {"name": "Orange Refractor",       "print_run": 10},
    {"name": "Red Refractor",          "print_run": 5},
    {"name": "SuperFractor",           "print_run": 1},
]

INSERT_PARALLELS = [
    {"name": "Refractor",              "print_run": None},
    {"name": "Green Refractor",        "print_run": 99},
    {"name": "Gold Refractor",         "print_run": 50},
    {"name": "Orange Refractor",       "print_run": 10},
    {"name": "Red Refractor",          "print_run": 5},
    {"name": "SuperFractor",           "print_run": 1},
]

AUTO_PARALLELS = [
    {"name": "Refractor",              "print_run": None},
    {"name": "Green Refractor",        "print_run": 99},
    {"name": "Blue Refractor",         "print_run": 75},
    {"name": "Gold Refractor",         "print_run": 50},
    {"name": "Orange Refractor",       "print_run": 25},
    {"name": "Red Refractor",          "print_run": 10},
    {"name": "SuperFractor",           "print_run": 1},
]

FINEST_PARTNERSHIPS_PARALLELS = [
    {"name": "Refractor",              "print_run": None},
    {"name": "Green Refractor",        "print_run": 99},
    {"name": "Gold Refractor",         "print_run": 50},
    {"name": "Orange Refractor",       "print_run": 10},
    {"name": "Red Refractor",          "print_run": 5},
    {"name": "SuperFractor",           "print_run": 1},
]

FINEST_FANS_PARALLELS = [
    {"name": "Refractor",              "print_run": None},
    {"name": "Gold Refractor",         "print_run": 50},
    {"name": "SuperFractor",           "print_run": 1},
]

NO_PARALLELS = []

SECTION_PARALLELS = {
    "Base Set":                          BASE_PARALLELS,
    "Expected Brilliance":               INSERT_PARALLELS,
    "Swerve":                            INSERT_PARALLELS,
    "Swerve Fusion Variation":           INSERT_PARALLELS,
    "Arrivals":                          INSERT_PARALLELS,
    "Clean":                             INSERT_PARALLELS,
    "Gusto":                             INSERT_PARALLELS,
    "Nightmare Fuel":                    INSERT_PARALLELS,
    "Main Attraction":                   INSERT_PARALLELS,
    "Polka":                             INSERT_PARALLELS,
    "Headliners":                        INSERT_PARALLELS,
    "Aura":                              INSERT_PARALLELS,
    "Finest Idols":                      INSERT_PARALLELS,
    "Finest Autographs":                 AUTO_PARALLELS,
    "Finest Moments Autographs":         AUTO_PARALLELS,
    "Finest Seasons 1995-96":            INSERT_PARALLELS,
    "Finest Partnerships":               FINEST_PARTNERSHIPS_PARALLELS,
    "Arrivals Autograph Edition":        AUTO_PARALLELS,
    "Main Attraction Autograph Edition": AUTO_PARALLELS,
    "Gustographs":                       AUTO_PARALLELS,
    "Finest Fans":                       FINEST_FANS_PARALLELS,
}

# Sections where all cards are rookies
ROOKIE_SECTIONS = {"Arrivals", "Arrivals Autograph Edition"}

# Sections that are dual/multi-player cards
PARTNERSHIP_SECTIONS = {"Finest Partnerships"}

# ---------------------------------------------------------------------------
# Raw data (inlined)
# ---------------------------------------------------------------------------

SECTIONS_DATA = {}  # will be populated below

def add_section(name, cards_raw):
    SECTIONS_DATA[name] = cards_raw

# Base Set cards (300 cards across Common / Uncommon / Rare)
BASE_CARDS_RAW = [
    # COMMON (1-100)
    ("1", "Antoine Semenyo", "AFC Bournemouth", False),
    ("2", "Julio Soler", "AFC Bournemouth", True),
    ("3", "Eli Junior Kroupi", "AFC Bournemouth", False),
    ("4", "Amine Adli", "AFC Bournemouth", False),
    ("5", "Leandro Trossard", "Arsenal", False),
    ("6", "Jurriën Timber", "Arsenal", False),
    ("7", "Riccardo Calafiori", "Arsenal", False),
    ("8", "Noni Madueke", "Arsenal", False),
    ("9", "Ben Broggio", "Aston Villa", True),
    ("10", "Rory Wilson", "Aston Villa", True),
    ("11", "Jamaldeen Jimoh-Aloba", "Aston Villa", True),
    ("12", "Mikkel Damsgaard", "Brentford", False),
    ("13", "Kevin Schade", "Brentford", False),
    ("14", "Michael Kayode", "Brentford", False),
    ("15", "Dango Ouattara", "Brentford", False),
    ("16", "Tom Watson", "Brighton & Hove Albion", True),
    ("17", "Kaoru Mitoma", "Brighton & Hove Albion", False),
    ("18", "Yasin Ayari", "Brighton & Hove Albion", True),
    ("19", "Harry Howell", "Brighton & Hove Albion", True),
    ("20", "Jaidon Anthony", "Burnley FC", False),
    ("21", "Lyle Foster", "Burnley FC", False),
    ("22", "Lesley Ugochukwu", "Burnley FC", False),
    ("23", "Jaydon Banel", "Burnley FC", True),
    ("24", "Bashir Humphreys", "Burnley FC", True),
    ("25", "Zian Flemming", "Burnley FC", True),
    ("26", "Kyle Walker", "Burnley FC", False),
    ("27", "Josh Laurent", "Burnley FC", True),
    ("28", "Estêvão Willian", "Chelsea", True),
    ("29", "Cole Palmer", "Chelsea", False),
    ("30", "Josh Acheampong", "Chelsea", False),
    ("31", "Shumaira Mheuka", "Chelsea", True),
    ("32", "Harrison Murray-Campbell", "Chelsea", True),
    ("33", "Romain Esse", "Crystal Palace", True),
    ("34", "Zach Marsh", "Crystal Palace", True),
    ("35", "Max Dowman", "Arsenal", True),
    ("36", "Justin Devenny", "Crystal Palace", True),
    ("37", "Yéremy Pino", "Crystal Palace", False),
    ("38", "Jack Grealish", "Everton", False),
    ("39", "Kiernan Dewsbury-Hall", "Everton", False),
    ("40", "Tyler Dibling", "Everton", False),
    ("41", "Roman Dixon", "Everton", True),
    ("42", "Charly Alcaraz", "Everton", False),
    ("43", "Jonah Kusi-Asare", "Fulham", True),
    ("44", "Samuel Chukwueze", "Fulham", False),
    ("45", "Kevin", "Fulham", False),
    ("46", "Josh King", "Fulham", True),
    ("47", "Gabriel Gudmundsson", "Leeds United", False),
    ("48", "Noah Okafor", "Leeds United", False),
    ("49", "Anton Stach", "Leeds United", False),
    ("50", "Dominic Calvert-Lewin", "Leeds United", False),
    ("51", "Harry Gray", "Leeds United", True),
    ("52", "Alfie Cresswell", "Leeds United", True),
    ("53", "Sean Longstaff", "Leeds United", False),
    ("54", "Virgil van Dijk", "Liverpool FC", False),
    ("55", "Rio Ngumoha", "Liverpool FC", True),
    ("56", "Mohamed Salah", "Liverpool FC", False),
    ("57", "Alexander Isak", "Liverpool FC", False),
    ("58", "Hugo Ekitike", "Liverpool FC", False),
    ("59", "Trent Koné-Doherty", "Liverpool FC", True),
    ("60", "Giovanni Leoni", "Liverpool FC", True),
    ("61", "Erling Haaland", "Manchester City", False),
    ("62", "Rayan Cherki", "Manchester City", False),
    ("63", "Rodri", "Manchester City", False),
    ("64", "Tijjani Reijnders", "Manchester City", False),
    ("65", "Divine Mukasa", "Manchester City", True),
    ("66", "Gianluigi Donnarumma", "Manchester City", False),
    ("67", "Benjamin Šeško", "Manchester United", False),
    ("68", "Matheus Cunha", "Manchester United", False),
    ("69", "Amir Ibragimov", "Manchester United", True),
    ("70", "Bruno Fernandes", "Manchester United", False),
    ("71", "Bendito Mantato", "Manchester United", True),
    ("72", "Joelinton", "Newcastle United", False),
    ("73", "Sandro Tonali", "Newcastle United", False),
    ("74", "Bruno Guimarães", "Newcastle United", False),
    ("75", "Anthony Gordon", "Newcastle United", False),
    ("76", "Seung-Soo Park", "Newcastle United", True),
    ("77", "Nick Woltemade", "Newcastle United", False),
    ("78", "Morgan Gibbs-White", "Nottingham Forest", False),
    ("79", "James McAtee", "Nottingham Forest", False),
    ("80", "Igor Jesus", "Nottingham Forest", True),
    ("81", "Zach Abbott", "Nottingham Forest", True),
    ("82", "Jair", "Nottingham Forest", True),
    ("83", "Chris Rigg", "Sunderland", True),
    ("84", "Noah Sadiki", "Sunderland", True),
    ("85", "Eliezer Mayenda", "Sunderland", True),
    ("86", "Wilson Isidor", "Sunderland", True),
    ("87", "Simon Adingra", "Sunderland", False),
    ("88", "Lucas Bergvall", "Tottenham Hotspur", False),
    ("89", "Djed Spence", "Tottenham Hotspur", False),
    ("90", "João Palhinha", "Tottenham Hotspur", False),
    ("91", "Xavi Simons", "Tottenham Hotspur", False),
    ("92", "Kōta Takai", "Tottenham Hotspur", True),
    ("93", "Crysencio Summerville", "West Ham United", False),
    ("94", "Lucas Paquetá", "West Ham United", False),
    ("95", "El Hadji Malick Diouf", "West Ham United", True),
    ("96", "Freddie Potts", "West Ham United", True),
    ("97", "Callum Marshall", "West Ham United", False),
    ("98", "Fer López", "Wolverhampton Wanderers", True),
    ("99", "Enso González", "Wolverhampton Wanderers", True),
    ("100", "Wesley Okoduwa", "Wolverhampton Wanderers", True),
    # UNCOMMON (101-200)
    ("101", "Antoine Semenyo", "AFC Bournemouth", False),
    ("102", "Justin Kluivert", "AFC Bournemouth", False),
    ("103", "Tyler Adams", "AFC Bournemouth", False),
    ("104", "Eli Junior Kroupi", "AFC Bournemouth", False),
    ("105", "Evanilson", "AFC Bournemouth", False),
    ("106", "Bukayo Saka", "Arsenal", False),
    ("107", "Gabriel Magalhães", "Arsenal", False),
    ("108", "Max Dowman", "Arsenal", True),
    ("109", "Viktor Gyökeres", "Arsenal", False),
    ("110", "Jaydee Canvot", "Crystal Palace", True),
    ("111", "Cristhian Mosquera", "Arsenal", False),
    ("112", "William Saliba", "Arsenal", False),
    ("113", "Piero Hincapié", "Arsenal", False),
    ("114", "Igor Thiago", "Brentford", False),
    ("115", "Ollie Watkins", "Aston Villa", False),
    ("116", "Ben Broggio", "Aston Villa", True),
    ("117", "Morgan Rogers", "Aston Villa", False),
    ("118", "Youri Tielemans", "Aston Villa", False),
    ("119", "John McGinn", "Aston Villa", False),
    ("120", "Jamaldeen Jimoh-Aloba", "Aston Villa", True),
    ("121", "Jair", "Nottingham Forest", True),
    ("122", "Mikkel Damsgaard", "Brentford", False),
    ("123", "Dango Ouattara", "Brentford", False),
    ("124", "Gustavo Nunes", "Brentford", True),
    ("125", "Nathan Collins", "Brentford", False),
    ("126", "Romelle Donovan", "Brentford", True),
    ("127", "Jordan Henderson", "Brentford", False),
    ("128", "Antoni Milambo", "Brentford", False),
    ("129", "Kaoru Mitoma", "Brighton & Hove Albion", False),
    ("130", "Stefanos Tzimas", "Brighton & Hove Albion", True),
    ("131", "Brajan Gruda", "Brighton & Hove Albion", False),
    ("132", "Yasin Ayari", "Brighton & Hove Albion", True),
    ("133", "Yankuba Minteh", "Brighton & Hove Albion", False),
    ("134", "Josh Laurent", "Burnley FC", True),
    ("135", "Estêvão Willian", "Chelsea", True),
    ("136", "Cole Palmer", "Chelsea", False),
    ("137", "Moisés Caicedo", "Chelsea", False),
    ("138", "Enzo Fernández", "Chelsea", False),
    ("139", "Alejandro Garnacho", "Chelsea", False),
    ("140", "Jean-Philippe Mateta", "Crystal Palace", False),
    ("141", "Christantus Uche", "Crystal Palace", False),
    ("142", "Yéremy Pino", "Crystal Palace", False),
    ("143", "Jack Grealish", "Everton", False),
    ("144", "Charly Alcaraz", "Everton", False),
    ("145", "Iliman Ndiaye", "Everton", False),
    ("146", "Dwight McNeil", "Everton", False),
    ("147", "Jarrad Branthwaite", "Everton", False),
    ("148", "Thierno Barry", "Everton", False),
    ("149", "Emile Smith Rowe", "Fulham", False),
    ("150", "Kevin", "Fulham", False),
    ("151", "Josh King", "Fulham", True),
    ("152", "Raúl Jiménez", "Fulham", False),
    ("153", "Brenden Aaronson", "Leeds United", False),
    ("154", "Alexander Isak", "Liverpool FC", False),
    ("155", "Rio Ngumoha", "Liverpool FC", True),
    ("156", "Mohamed Salah", "Liverpool FC", False),
    ("157", "Virgil van Dijk", "Liverpool FC", False),
    ("158", "Florian Wirtz", "Liverpool FC", False),
    ("159", "Hugo Ekitike", "Liverpool FC", False),
    ("160", "Erling Haaland", "Manchester City", False),
    ("161", "Rayan Cherki", "Manchester City", False),
    ("162", "Rodri", "Manchester City", False),
    ("163", "Omar Marmoush", "Manchester City", False),
    ("164", "Tijjani Reijnders", "Manchester City", False),
    ("165", "Divine Mukasa", "Manchester City", True),
    ("166", "Reigan Heskey", "Manchester City", True),
    ("167", "Phil Foden", "Manchester City", False),
    ("168", "Benjamin Šeško", "Manchester United", False),
    ("169", "Bryan Mbeumo", "Manchester United", False),
    ("170", "Matheus Cunha", "Manchester United", False),
    ("171", "Bruno Fernandes", "Manchester United", False),
    ("172", "Shea Lacey", "Manchester United", True),
    ("173", "Fabian Schär", "Newcastle United", False),
    ("174", "Bruno Guimarães", "Newcastle United", False),
    ("175", "Anthony Gordon", "Newcastle United", False),
    ("176", "Nick Woltemade", "Newcastle United", False),
    ("177", "Morgan Gibbs-White", "Nottingham Forest", False),
    ("178", "James McAtee", "Nottingham Forest", False),
    ("179", "Chris Rigg", "Sunderland", True),
    ("180", "Granit Xhaka", "Sunderland", False),
    ("181", "Noah Sadiki", "Sunderland", True),
    ("182", "Eliezer Mayenda", "Sunderland", True),
    ("183", "Enzo Le Fée", "Sunderland", False),
    ("184", "Simon Adingra", "Sunderland", False),
    ("185", "Wilson Odobert", "Tottenham Hotspur", False),
    ("186", "Pape Matar Sarr", "Tottenham Hotspur", False),
    ("187", "Pedro Porro", "Tottenham Hotspur", False),
    ("188", "Xavi Simons", "Tottenham Hotspur", False),
    ("189", "Mohammed Kudus", "Tottenham Hotspur", False),
    ("190", "Crysencio Summerville", "West Ham United", False),
    ("191", "Lucas Paquetá", "West Ham United", False),
    ("192", "El Hadji Malick Diouf", "West Ham United", True),
    ("193", "Freddie Potts", "West Ham United", True),
    ("194", "Luis Guilherme", "West Ham United", True),
    ("195", "Ollie Scarles", "West Ham United", False),
    ("196", "Jørgen Strand Larsen", "Wolverhampton Wanderers", False),
    ("197", "André", "Wolverhampton Wanderers", False),
    ("198", "João Gomes", "Wolverhampton Wanderers", False),
    ("199", "Jhon Arias", "Wolverhampton Wanderers", False),
    ("200", "Tolu Arokodare", "Wolverhampton Wanderers", True),
    # RARE (201-300)
    ("201", "Antoine Semenyo", "AFC Bournemouth", False),
    ("202", "Amine Adli", "AFC Bournemouth", False),
    ("203", "Tyler Adams", "AFC Bournemouth", False),
    ("204", "Eli Junior Kroupi", "AFC Bournemouth", False),
    ("205", "Evanilson", "AFC Bournemouth", False),
    ("206", "Veljko Milosavljević", "AFC Bournemouth", True),
    ("207", "Bukayo Saka", "Arsenal", False),
    ("208", "Viktor Gyökeres", "Arsenal", False),
    ("209", "Maxim De Cuyper", "Brighton & Hove Albion", True),
    ("210", "Martin Ødegaard", "Arsenal", False),
    ("211", "Martín Zubimendi", "Arsenal", False),
    ("212", "Declan Rice", "Arsenal", False),
    ("213", "Max Dowman", "Arsenal", True),
    ("214", "Myles Lewis-Skelly", "Arsenal", False),
    ("215", "Jamaldeen Jimoh-Aloba", "Aston Villa", True),
    ("216", "Morgan Rogers", "Aston Villa", False),
    ("217", "Ollie Watkins", "Aston Villa", False),
    ("218", "Youri Tielemans", "Aston Villa", False),
    ("219", "Kevin Schade", "Brentford", False),
    ("220", "Dango Ouattara", "Brentford", False),
    ("221", "Romelle Donovan", "Brentford", True),
    ("222", "Kaoru Mitoma", "Brighton & Hove Albion", False),
    ("223", "Harry Howell", "Brighton & Hove Albion", True),
    ("224", "Brajan Gruda", "Brighton & Hove Albion", False),
    ("225", "Stefanos Tzimas", "Brighton & Hove Albion", True),
    ("226", "Yasin Ayari", "Brighton & Hove Albion", True),
    ("227", "Tom Watson", "Brighton & Hove Albion", True),
    ("228", "Quilindschy Hartman", "Burnley FC", False),
    ("229", "Estêvão Willian", "Chelsea", True),
    ("230", "Cole Palmer", "Chelsea", False),
    ("231", "Moisés Caicedo", "Chelsea", False),
    ("232", "Enzo Fernández", "Chelsea", False),
    ("233", "Jorrel Hato", "Chelsea", False),
    ("234", "Liam Delap", "Chelsea", False),
    ("235", "João Pedro", "Chelsea", False),
    ("236", "Adam Wharton", "Crystal Palace", False),
    ("237", "Jean-Philippe Mateta", "Crystal Palace", False),
    ("238", "Chris Richards", "Crystal Palace", False),
    ("239", "Daichi Kamada", "Crystal Palace", False),
    ("240", "Daniel Muñoz", "Crystal Palace", False),
    ("241", "Yéremy Pino", "Crystal Palace", False),
    ("242", "Christantus Uche", "Crystal Palace", False),
    ("243", "Jack Grealish", "Everton", False),
    ("244", "Tyler Dibling", "Everton", False),
    ("245", "Charly Alcaraz", "Everton", False),
    ("246", "Iliman Ndiaye", "Everton", False),
    ("247", "Thierno Barry", "Everton", False),
    ("248", "Emile Smith Rowe", "Fulham", False),
    ("249", "Raúl Jiménez", "Fulham", False),
    ("250", "Alex Iwobi", "Fulham", False),
    ("251", "Rodrigo Muniz", "Fulham", False),
    ("252", "Adama Traoré", "Fulham", False),
    ("253", "Reggie Walsh", "Chelsea", True),
    ("254", "Harry Gray", "Leeds United", True),
    ("255", "Ao Tanaka", "Leeds United", False),
    ("256", "Jayden Bogle", "Leeds United", False),
    ("257", "Rio Ngumoha", "Liverpool FC", True),
    ("258", "Mohamed Salah", "Liverpool FC", False),
    ("259", "Virgil van Dijk", "Liverpool FC", False),
    ("260", "Florian Wirtz", "Liverpool FC", False),
    ("261", "Hugo Ekitike", "Liverpool FC", False),
    ("262", "Alexis Mac Allister", "Liverpool FC", False),
    ("263", "Alexander Isak", "Liverpool FC", False),
    ("264", "Erling Haaland", "Manchester City", False),
    ("265", "Rodri", "Manchester City", False),
    ("266", "Omar Marmoush", "Manchester City", False),
    ("267", "Tijjani Reijnders", "Manchester City", False),
    ("268", "Phil Foden", "Manchester City", False),
    ("269", "Benjamin Šeško", "Manchester United", False),
    ("270", "Bryan Mbeumo", "Manchester United", False),
    ("271", "Amir Ibragimov", "Manchester United", True),
    ("272", "Matheus Cunha", "Manchester United", False),
    ("273", "Bruno Fernandes", "Manchester United", False),
    ("274", "Shea Lacey", "Manchester United", True),
    ("275", "Bruno Guimarães", "Newcastle United", False),
    ("276", "Anthony Gordon", "Newcastle United", False),
    ("277", "Joelinton", "Newcastle United", False),
    ("278", "Sandro Tonali", "Newcastle United", False),
    ("279", "Seung-Soo Park", "Newcastle United", True),
    ("280", "Anthony Elanga", "Newcastle United", False),
    ("281", "James McAtee", "Nottingham Forest", False),
    ("282", "Igor Jesus", "Nottingham Forest", True),
    ("283", "Callum Hudson-Odoi", "Nottingham Forest", False),
    ("284", "Morgan Gibbs-White", "Nottingham Forest", False),
    ("285", "Murillo", "Nottingham Forest", False),
    ("286", "Chris Rigg", "Sunderland", True),
    ("287", "Eliezer Mayenda", "Sunderland", True),
    ("288", "Xavi Simons", "Tottenham Hotspur", False),
    ("289", "Mohammed Kudus", "Tottenham Hotspur", False),
    ("290", "Dominic Solanke", "Tottenham Hotspur", False),
    ("291", "Archie Gray", "Tottenham Hotspur", False),
    ("292", "Lucas Bergvall", "Tottenham Hotspur", False),
    ("293", "Micky van de Ven", "Tottenham Hotspur", False),
    ("294", "Lucas Paquetá", "West Ham United", False),
    ("295", "Jarrod Bowen", "West Ham United", False),
    ("296", "João Gomes", "Wolverhampton Wanderers", False),
    ("297", "André", "Wolverhampton Wanderers", False),
    ("298", "Jørgen Strand Larsen", "Wolverhampton Wanderers", False),
    ("299", "Jhon Arias", "Wolverhampton Wanderers", False),
    ("300", "Enso González", "Wolverhampton Wanderers", True),
]

EXPECTED_BRILLIANCE_RAW = [
    ("XB-1", "Evanilson", "AFC Bournemouth", False),
    ("XB-2", "Antoine Semenyo", "AFC Bournemouth", False),
    ("XB-3", "Eberechi Eze", "Arsenal", False),
    ("XB-4", "Viktor Gyökeres", "Arsenal", False),
    ("XB-5", "Ollie Watkins", "Aston Villa", False),
    ("XB-6", "Harvey Elliott", "Aston Villa", False),
    ("XB-7", "Dango Ouattara", "Brentford", False),
    ("XB-8", "Mikkel Damsgaard", "Brentford", False),
    ("XB-9", "Charalampos Kostoulas", "Brighton & Hove Albion", False),
    ("XB-10", "Stefanos Tzimas", "Brighton & Hove Albion", True),
    ("XB-11", "Armando Broja", "Burnley FC", False),
    ("XB-12", "Jaidon Anthony", "Burnley FC", False),
    ("XB-13", "Facundo Buonanotte", "Chelsea", False),
    ("XB-14", "João Pedro", "Chelsea", False),
    ("XB-15", "Jean-Philippe Mateta", "Crystal Palace", False),
    ("XB-16", "Yéremy Pino", "Crystal Palace", False),
    ("XB-17", "Charly Alcaraz", "Everton", False),
    ("XB-18", "Thierno Barry", "Everton", False),
    ("XB-19", "Jonah Kusi-Asare", "Fulham", True),
    ("XB-20", "Kevin", "Fulham", False),
    ("XB-21", "Harry Gray", "Leeds United", True),
    ("XB-22", "Wilfried Gnonto", "Leeds United", False),
    ("XB-23", "Alexander Isak", "Liverpool FC", False),
    ("XB-24", "Hugo Ekitike", "Liverpool FC", False),
    ("XB-25", "Erling Haaland", "Manchester City", False),
    ("XB-26", "Omar Marmoush", "Manchester City", False),
    ("XB-27", "Bryan Mbeumo", "Manchester United", False),
    ("XB-28", "Matheus Cunha", "Manchester United", False),
    ("XB-29", "Nick Woltemade", "Newcastle United", False),
    ("XB-30", "Sandro Tonali", "Newcastle United", False),
    ("XB-31", "Chris Wood", "Nottingham Forest", False),
    ("XB-32", "Arnaud Kalimuendo", "Nottingham Forest", False),
    ("XB-33", "Eliezer Mayenda", "Sunderland", True),
    ("XB-34", "Habib Diarra", "Sunderland", False),
    ("XB-35", "Xavi Simons", "Tottenham Hotspur", False),
    ("XB-36", "Randal Kolo Muani", "Tottenham Hotspur", False),
    ("XB-37", "El Hadji Malick Diouf", "West Ham United", True),
    ("XB-38", "Mateus Fernandes", "West Ham United", False),
    ("XB-39", "Tolu Arokodare", "Wolverhampton Wanderers", True),
    ("XB-40", "Fer López", "Wolverhampton Wanderers", True),
]

SWERVE_RAW = [
    ("SV-1", "Justin Kluivert", "AFC Bournemouth", False),
    ("SV-2", "Amine Adli", "AFC Bournemouth", False),
    ("SV-3", "Max Dowman", "Arsenal", True),
    ("SV-4", "Ethan Nwaneri", "Arsenal", False),
    ("SV-5", "Morgan Rogers", "Aston Villa", False),
    ("SV-6", "Youri Tielemans", "Aston Villa", False),
    ("SV-7", "Antoni Milambo", "Brentford", False),
    ("SV-8", "Romelle Donovan", "Brentford", True),
    ("SV-9", "Yasin Ayari", "Brighton & Hove Albion", True),
    ("SV-10", "Brajan Gruda", "Brighton & Hove Albion", False),
    ("SV-11", "Lesley Ugochukwu", "Burnley FC", False),
    ("SV-12", "Quilindschy Hartman", "Burnley FC", False),
    ("SV-13", "Dário Essugo", "Chelsea", False),
    ("SV-14", "Alejandro Garnacho", "Chelsea", False),
    ("SV-15", "Ismaïla Sarr", "Crystal Palace", False),
    ("SV-16", "Romain Esse", "Crystal Palace", True),
    ("SV-17", "Kiernan Dewsbury-Hall", "Everton", False),
    ("SV-18", "Tyler Dibling", "Everton", False),
    ("SV-19", "Josh King", "Fulham", True),
    ("SV-20", "Emile Smith Rowe", "Fulham", False),
    ("SV-21", "Brenden Aaronson", "Leeds United", False),
    ("SV-22", "Ao Tanaka", "Leeds United", False),
    ("SV-23", "Alexis Mac Allister", "Liverpool FC", False),
    ("SV-24", "Rio Ngumoha", "Liverpool FC", True),
    ("SV-25", "Tijjani Reijnders", "Manchester City", False),
    ("SV-26", "Jérémy Doku", "Manchester City", False),
    ("SV-27", "Bruno Fernandes", "Manchester United", False),
    ("SV-28", "Benjamin Šeško", "Manchester United", False),
    ("SV-29", "Sandro Tonali", "Newcastle United", False),
    ("SV-30", "Tino Livramento", "Newcastle United", False),
    ("SV-31", "Arnaud Kalimuendo", "Nottingham Forest", False),
    ("SV-32", "Ryan Yates", "Nottingham Forest", False),
    ("SV-33", "Granit Xhaka", "Sunderland", False),
    ("SV-34", "Enzo Le Fée", "Sunderland", False),
    ("SV-35", "João Palhinha", "Tottenham Hotspur", False),
    ("SV-36", "Lucas Bergvall", "Tottenham Hotspur", False),
    ("SV-37", "Lucas Paquetá", "West Ham United", False),
    ("SV-38", "Luis Guilherme", "West Ham United", True),
    ("SV-39", "Jhon Arias", "Wolverhampton Wanderers", False),
    ("SV-40", "João Gomes", "Wolverhampton Wanderers", False),
]

SWERVE_FUSION_RAW = [
    ("FV-1", "Justin Kluivert", "AFC Bournemouth", False),
    ("FV-2", "Amine Adli", "AFC Bournemouth", False),
    ("FV-3", "Max Dowman", "Arsenal", True),
    ("FV-4", "Ethan Nwaneri", "Arsenal", False),
    ("FV-5", "Morgan Rogers", "Aston Villa", False),
    ("FV-6", "Youri Tielemans", "Aston Villa", False),
    ("FV-7", "Antoni Milambo", "Brentford", False),
    ("FV-8", "Romelle Donovan", "Brentford", True),
    ("FV-9", "Yasin Ayari", "Brighton & Hove Albion", True),
    ("FV-10", "Brajan Gruda", "Brighton & Hove Albion", False),
    ("FV-11", "Lesley Ugochukwu", "Burnley FC", False),
    ("FV-12", "Quilindschy Hartman", "Burnley FC", False),
    ("FV-13", "Dário Essugo", "Chelsea", False),
    ("FV-14", "Alejandro Garnacho", "Chelsea", False),
    ("FV-15", "Ismaïla Sarr", "Crystal Palace", False),
    ("FV-16", "Romain Esse", "Crystal Palace", True),
    ("FV-17", "Kiernan Dewsbury-Hall", "Everton", False),
    ("FV-18", "Tyler Dibling", "Everton", False),
    ("FV-19", "Josh King", "Fulham", True),
    ("FV-20", "Emile Smith Rowe", "Fulham", False),
    ("FV-21", "Brenden Aaronson", "Leeds United", False),
    ("FV-22", "Ao Tanaka", "Leeds United", False),
    ("FV-23", "Alexis Mac Allister", "Liverpool FC", False),
    ("FV-24", "Rio Ngumoha", "Liverpool FC", True),
    ("FV-25", "Tijjani Reijnders", "Manchester City", False),
    ("FV-26", "Jérémy Doku", "Manchester City", False),
    ("FV-27", "Bruno Fernandes", "Manchester United", False),
    ("FV-28", "Benjamin Šeško", "Manchester United", False),
    ("FV-29", "Sandro Tonali", "Newcastle United", False),
    ("FV-30", "Tino Livramento", "Newcastle United", False),
    ("FV-31", "Arnaud Kalimuendo", "Nottingham Forest", False),
    ("FV-32", "Ryan Yates", "Nottingham Forest", False),
    ("FV-33", "Granit Xhaka", "Sunderland", False),
    ("FV-34", "Enzo Le Fée", "Sunderland", False),
    ("FV-35", "João Palhinha", "Tottenham Hotspur", False),
    ("FV-36", "Lucas Bergvall", "Tottenham Hotspur", False),
    ("FV-37", "Lucas Paquetá", "West Ham United", False),
    ("FV-38", "Luis Guilherme", "West Ham United", True),
    ("FV-39", "Jhon Arias", "Wolverhampton Wanderers", False),
    ("FV-40", "João Gomes", "Wolverhampton Wanderers", False),
]

ARRIVALS_RAW = [
    ("AV-1", "Chris Rigg", "Sunderland", True),
    ("AV-2", "Josh King", "Fulham", True),
    ("AV-3", "Reggie Walsh", "Chelsea", True),
    ("AV-4", "Shea Lacey", "Manchester United", True),
    ("AV-5", "Harry Gray", "Leeds United", True),
    ("AV-6", "Max Dowman", "Arsenal", True),
    ("AV-7", "Rio Ngumoha", "Liverpool FC", True),
    ("AV-8", "Jaydee Canvot", "Crystal Palace", True),
    ("AV-9", "Tom Watson", "Brighton & Hove Albion", True),
    ("AV-10", "Estêvão Willian", "Chelsea", True),
]

CLEAN_RAW = [
    ("CN-1", "Virgil van Dijk", "Liverpool FC", False),
    ("CN-2", "Riccardo Calafiori", "Arsenal", False),
    ("CN-3", "David Raya", "Arsenal", False),
    ("CN-4", "Dan Burn", "Newcastle United", False),
    ("CN-5", "Micky van de Ven", "Tottenham Hotspur", False),
    ("CN-6", "Jorrel Hato", "Chelsea", False),
    ("CN-7", "Nathan Collins", "Brentford", False),
    ("CN-8", "Murillo", "Nottingham Forest", False),
    ("CN-9", "Gianluigi Donnarumma", "Manchester City", False),
    ("CN-10", "Lewis Dunk", "Brighton & Hove Albion", False),
]

GUSTO_RAW = [
    ("GO-1", "Kai Havertz", "Arsenal", False),
    ("GO-2", "Benjamin Šeško", "Manchester United", False),
    ("GO-3", "Jarrod Bowen", "West Ham United", False),
    ("GO-4", "Diego León", "Manchester United", True),
    ("GO-5", "Heung-Min Son", "Tottenham Hotspur", False),
    ("GO-6", "Martín Zubimendi", "Arsenal", False),
    ("GO-7", "Yaya Touré", "Manchester City", False),
    ("GO-8", "Shea Lacey", "Manchester United", True),
    ("GO-9", "Anthony Gordon", "Newcastle United", False),
    ("GO-10", "Declan Rice", "Arsenal", False),
    ("GO-11", "Alexis Mac Allister", "Liverpool FC", False),
    ("GO-12", "Hugo Ekitike", "Liverpool FC", False),
    ("GO-13", "Dominik Szoboszlai", "Liverpool FC", False),
    ("GO-14", "Mohammed Kudus", "Tottenham Hotspur", False),
    ("GO-15", "Bruno Guimarães", "Newcastle United", False),
    ("GO-16", "Chris Rigg", "Sunderland", True),
    ("GO-17", "Enzo Fernández", "Chelsea", False),
    ("GO-18", "João Pedro", "Chelsea", False),
    ("GO-19", "Malo Gusto", "Chelsea", False),
    ("GO-20", "Divine Mukasa", "Manchester City", True),
]

NIGHTMARE_FUEL_RAW = [
    ("NF-1", "Benjamin Šeško", "Manchester United", False),
    ("NF-2", "Mohamed Salah", "Liverpool FC", False),
    ("NF-3", "Viktor Gyökeres", "Arsenal", False),
    ("NF-4", "Carlos Tevez", "Manchester City", False),
    ("NF-5", "Estêvão Willian", "Chelsea", True),
    ("NF-6", "Rio Ngumoha", "Liverpool FC", True),
    ("NF-7", "Wayne Rooney", "Manchester United", False),
    ("NF-8", "Harry Kane", "Tottenham Hotspur", False),
    ("NF-9", "Fernando Torres", "Liverpool FC", False),
    ("NF-10", "Dennis Bergkamp", "Arsenal", False),
    ("NF-11", "Erling Haaland", "Manchester City", False),
    ("NF-12", "Didier Drogba", "Chelsea", False),
    ("NF-13", "Robbie Fowler", "Liverpool FC", False),
    ("NF-14", "Eric Cantona", "Manchester United", False),
    ("NF-15", "Bukayo Saka", "Arsenal", False),
    ("NF-16", "Alexander Isak", "Liverpool FC", False),
    ("NF-17", "Sergio Agüero", "Manchester City", False),
    ("NF-18", "Thierry Henry", "Arsenal", False),
    ("NF-19", "Ian Wright", "Arsenal", False),
    ("NF-20", "Alan Shearer", "Newcastle United", False),
]

MAIN_ATTRACTION_RAW = [
    ("MA-1", "Antoine Semenyo", "AFC Bournemouth", False),
    ("MA-2", "Florian Wirtz", "Liverpool FC", False),
    ("MA-3", "Rodri", "Manchester City", False),
    ("MA-4", "Cole Palmer", "Chelsea", False),
    ("MA-5", "Gareth Bale", "Tottenham Hotspur", False),
    ("MA-6", "Martín Zubimendi", "Arsenal", False),
    ("MA-7", "Mohamed Salah", "Liverpool FC", False),
    ("MA-8", "Matheus Cunha", "Manchester United", False),
    ("MA-9", "Bruno Fernandes", "Manchester United", False),
    ("MA-10", "Kaoru Mitoma", "Brighton & Hove Albion", False),
    ("MA-11", "David Silva", "Manchester City", False),
    ("MA-12", "Ethan Nwaneri", "Arsenal", False),
    ("MA-13", "Virgil van Dijk", "Liverpool FC", False),
    ("MA-14", "Andy Cole", "Manchester United", False),
    ("MA-15", "Morgan Rogers", "Aston Villa", False),
    ("MA-16", "Estêvão Willian", "Chelsea", True),
    ("MA-17", "Moisés Caicedo", "Chelsea", False),
    ("MA-18", "Carlos Tevez", "Manchester City", False),
    ("MA-19", "Kevin", "Fulham", False),
    ("MA-20", "Luka Modrić", "Tottenham Hotspur", False),
]

POLKA_RAW = [
    ("PK-1", "David Beckham", "Manchester United", False),
    ("PK-2", "Mohamed Salah", "Liverpool FC", False),
    ("PK-3", "Erling Haaland", "Manchester City", False),
    ("PK-4", "Rio Ngumoha", "Liverpool FC", True),
    ("PK-5", "Kevin De Bruyne", "Manchester City", False),
    ("PK-6", "Gareth Bale", "Tottenham Hotspur", False),
    ("PK-7", "Harry Kane", "Tottenham Hotspur", False),
    ("PK-8", "Bukayo Saka", "Arsenal", False),
    ("PK-9", "Eden Hazard", "Chelsea", False),
    ("PK-10", "Nick Woltemade", "Newcastle United", False),
    ("PK-11", "Heung-Min Son", "Tottenham Hotspur", False),
    ("PK-12", "Alan Shearer", "Newcastle United", False),
    ("PK-13", "Thierry Henry", "Arsenal", False),
    ("PK-14", "Wayne Rooney", "Manchester United", False),
    ("PK-15", "Max Dowman", "Arsenal", True),
    ("PK-16", "Frank Lampard", "Chelsea", False),
    ("PK-17", "Steven Gerrard", "Liverpool FC", False),
    ("PK-18", "Paul Scholes", "Manchester United", False),
    ("PK-19", "Dennis Bergkamp", "Arsenal", False),
    ("PK-20", "Sergio Agüero", "Manchester City", False),
]

HEADLINERS_RAW = [
    ("HS-1", "Mohammed Kudus", "Tottenham Hotspur", False),
    ("HS-2", "Bruno Fernandes", "Manchester United", False),
    ("HS-3", "Phil Foden", "Manchester City", False),
    ("HS-4", "Martin Ødegaard", "Arsenal", False),
    ("HS-5", "Rodri", "Manchester City", False),
    ("HS-6", "Hugo Ekitike", "Liverpool FC", False),
    ("HS-7", "Declan Rice", "Arsenal", False),
    ("HS-8", "Anthony Gordon", "Newcastle United", False),
    ("HS-9", "Bryan Mbeumo", "Manchester United", False),
    ("HS-10", "Morgan Gibbs-White", "Nottingham Forest", False),
]

AURA_RAW = [
    ("AU-1", "Mario Balotelli", "Manchester City", False),
    ("AU-2", "Gianfranco Zola", "Chelsea", False),
    ("AU-3", "Phil Foden", "Manchester City", False),
    ("AU-4", "Paul Gascoigne", "Everton", False),
    ("AU-5", "Jack Grealish", "Everton", False),
    ("AU-6", "Declan Rice", "Arsenal", False),
    ("AU-7", "Fernandinho", "Manchester City", False),
    ("AU-8", "Claude Makélélé", "Chelsea", False),
    ("AU-9", "Roy Keane", "Manchester United", False),
    ("AU-10", "William Saliba", "Arsenal", False),
    ("AU-11", "Bukayo Saka", "Arsenal", False),
    ("AU-12", "Wayne Rooney", "Manchester United", False),
    ("AU-13", "Alexander Isak", "Liverpool FC", False),
    ("AU-14", "Steven Gerrard", "Liverpool FC", False),
    ("AU-15", "Estêvão Willian", "Chelsea", True),
    ("AU-16", "Mohamed Salah", "Liverpool FC", False),
    ("AU-17", "Florian Wirtz", "Liverpool FC", False),
    ("AU-18", "Thierry Henry", "Arsenal", False),
    ("AU-19", "Harry Kane", "Tottenham Hotspur", False),
    ("AU-20", "Didier Drogba", "Chelsea", False),
]

FINEST_IDOLS_RAW = [
    ("FI-1", "Steven Gerrard", "Liverpool FC", False),
    ("FI-2", "Frank Lampard", "Chelsea", False),
    ("FI-3", "Sergio Agüero", "Manchester City", False),
    ("FI-4", "Harry Kane", "Tottenham Hotspur", False),
    ("FI-5", "Wayne Rooney", "Manchester United", False),
]

FINEST_AUTOGRAPHS_RAW = [
    ("FA-AC", "Alfie Cresswell", "Leeds United", True),
    ("FA-AE", "Anthony Elanga", "Newcastle United", False),
    ("FA-AG", "Archie Gray", "Tottenham Hotspur", False),
    ("FA-AI", "Alexander Isak", "Liverpool FC", False),
    ("FA-AN", "Anthony Gordon", "Newcastle United", False),
    ("FA-AR", "Antonee Robinson", "Fulham", False),
    ("FA-AY", "Ashley Young", "Aston Villa", False),
    ("FA-BE", "Bendito Mantato", "Manchester United", True),
    ("FA-BF", "Bruno Fernandes", "Manchester United", False),
    ("FA-BG", "Brajan Gruda", "Brighton & Hove Albion", False),
    ("FA-BM", "Bryan Mbeumo", "Manchester United", False),
    ("FA-BO", "Jarrod Bowen", "West Ham United", False),
    ("FA-BS", "Bukayo Saka", "Arsenal", False),
    ("FA-CA", "Santi Cazorla", "Arsenal", False),
    ("FA-CD", "Clint Dempsey", "Fulham", False),
    ("FA-CG", "Cody Gakpo", "Liverpool FC", False),
    ("FA-CH", "Callum Hudson-Odoi", "Nottingham Forest", False),
    ("FA-CP", "Cole Palmer", "Chelsea", False),
    ("FA-CR", "Chris Richards", "Crystal Palace", False),
    ("FA-CW", "Chris Wood", "Nottingham Forest", False),
    ("FA-DD", "Diogo Dalot", "Manchester United", False),
    ("FA-DI", "Denis Irwin", "Manchester United", False),
    ("FA-DK", "Dirk Kuyt", "Liverpool FC", False),
    ("FA-DL", "David Luiz", "Chelsea", False),
    ("FA-DO", "Dango Ouattara", "Brentford", False),
    ("FA-DR", "Declan Rice", "Arsenal", False),
    ("FA-DS", "Dominic Solanke", "Tottenham Hotspur", False),
    ("FA-EA", "Emmanuel Adebayor", "Arsenal", False),
    ("FA-EF", "Enzo Fernández", "Chelsea", False),
    ("FA-EH", "Erling Haaland", "Manchester City", False),
    ("FA-EM", "El Hadji Malick Diouf", "West Ham United", True),
    ("FA-EN", "Ethan Nwaneri", "Arsenal", False),
    ("FA-ES", "Emile Smith Rowe", "Fulham", False),
    ("FA-EW", "Estêvão Willian", "Chelsea", True),
    ("FA-GI", "Jamie Gittens", "Chelsea", False),
    ("FA-GU", "Bruno Guimarães", "Newcastle United", False),
    ("FA-GX", "Granit Xhaka", "Sunderland", False),
    ("FA-HG", "Harry Gray", "Leeds United", True),
    ("FA-IB", "Amir Ibragimov", "Manchester United", True),
    ("FA-IN", "Iliman Ndiaye", "Everton", False),
    ("FA-JB", "Jayden Bogle", "Leeds United", False),
    ("FA-JG", "Jack Grealish", "Everton", False),
    ("FA-JM", "John McGinn", "Aston Villa", False),
    ("FA-JO", "João Palhinha", "Tottenham Hotspur", False),
    ("FA-JR", "Jacob Ramsey", "Newcastle United", False),
    ("FA-JS", "Jørgen Strand Larsen", "Wolverhampton Wanderers", False),
    ("FA-JZ", "Joshua Zirkzee", "Manchester United", False),
    ("FA-KS", "Kevin Schade", "Brentford", False),
    ("FA-KU", "Dejan Kulusevski", "Tottenham Hotspur", False),
    ("FA-KW", "Kyle Walker", "Burnley FC", False),
    ("FA-LD", "Liam Delap", "Chelsea", False),
    ("FA-LP", "Lucas Paquetá", "West Ham United", False),
    ("FA-LS", "Leroy Sané", "Manchester City", False),
    ("FA-MC", "Moisés Caicedo", "Chelsea", False),
    ("FA-MD", "Max Dowman", "Arsenal", True),
    ("FA-MG", "Marc Guiu", "Chelsea", False),
    ("FA-MI", "Milos Kerkez", "Liverpool FC", False),
    ("FA-MK", "Mohammed Kudus", "Tottenham Hotspur", False),
    ("FA-ML", "Myles Lewis-Skelly", "Arsenal", False),
    ("FA-MS", "Mohamed Salah", "Liverpool FC", False),
    ("FA-MZ", "Martín Zubimendi", "Arsenal", False),
    ("FA-NC", "Nathan Collins", "Brentford", False),
    ("FA-NM", "Noni Madueke", "Arsenal", False),
    ("FA-NV", "Nemanja Vidić", "Manchester United", False),
    ("FA-NW", "Nick Woltemade", "Newcastle United", False),
    ("FA-OG", "Olivier Giroud", "Arsenal", False),
    ("FA-OM", "Omar Marmoush", "Manchester City", False),
    ("FA-OW", "Ollie Watkins", "Aston Villa", False),
    ("FA-PE", "João Pedro", "Chelsea", False),
    ("FA-PF", "Phil Foden", "Manchester City", False),
    ("FA-PN", "Pedro Neto", "Chelsea", False),
    ("FA-RG", "Chris Rigg", "Sunderland", True),
    ("FA-RI", "John Arne Riise", "Liverpool FC", False),
    ("FA-RM", "Riyad Mahrez", "Manchester City", False),
    ("FA-RN", "Rio Ngumoha", "Liverpool FC", True),
    ("FA-RW", "Reggie Walsh", "Chelsea", True),
    ("FA-SA", "Simon Adingra", "Sunderland", False),
    ("FA-SC", "Sol Campbell", "Arsenal", False),
    ("FA-SL", "Shea Lacey", "Manchester United", True),
    ("FA-SM", "Shumaira Mheuka", "Chelsea", True),
    ("FA-TD", "Tyler Dibling", "Everton", False),
    ("FA-TO", "Sandro Tonali", "Newcastle United", False),
    ("FA-TR", "Tijjani Reijnders", "Manchester City", False),
    ("FA-TW", "Tom Watson", "Brighton & Hove Albion", True),
    ("FA-VD", "Virgil van Dijk", "Liverpool FC", False),
    ("FA-VG", "Viktor Gyökeres", "Arsenal", False),
    ("FA-WS", "William Saliba", "Arsenal", False),
    ("FA-YA", "Yasin Ayari", "Brighton & Hove Albion", True),
    ("FA-YY", "Yehor Yarmolyuk", "Brentford", False),
]

FINEST_MOMENTS_AUTOS_RAW = [
    ("FM-AS", "Alan Shearer", "Newcastle United", False),
    ("FM-AY", "Ashley Young", "Aston Villa", False),
    ("FM-BM", "David Beckham", "Manchester United", False),
    ("FM-CT", "Carlos Tevez", "West Ham United", False),
    ("FM-DB", "Dennis Bergkamp", "Arsenal", False),
    ("FM-DJ", "David James", "Manchester City", False),
    ("FM-EH", "Erling Haaland", "Manchester City", False),
    ("FM-HS", "Heung-Min Son", "Tottenham Hotspur", False),
    ("FM-HZ", "Eden Hazard", "Chelsea", False),
    ("FM-IW", "Ian Wright", "Arsenal", False),
    ("FM-JH", "Jordan Henderson", "Sunderland", False),
    ("FM-JM", "José Mourinho", "Chelsea", False),
    ("FM-KK", "Kevin Keegan", "Newcastle United", False),
    ("FM-LS", "Lee Sharpe", "Manchester United", False),
    ("FM-ME", "Michael Essien", "Chelsea", False),
    ("FM-OG", "Olivier Giroud", "Arsenal", False),
    ("FM-PC", "Papiss Cissé", "Newcastle United", False),
    ("FM-PG", "Pep Guardiola", "Manchester City", False),
    ("FM-PV", "Patrick Vieira", "Arsenal", False),
    ("FM-RK", "Roy Keane", "Manchester United", False),
    ("FM-SA", "Sergio Agüero", "Manchester City", False),
    ("FM-SB", "Steve Bruce", "Manchester United", False),
    ("FM-TA", "Tony Adams", "Arsenal", False),
    ("FM-WR", "Wayne Rooney", "Everton", False),
]

FINEST_SEASONS_RAW = [
    ("FS-AK", "Andrei Kanchelskis", "Everton", False),
    ("FS-DJ", "David James", "Liverpool FC", False),
    ("FS-DY", "Dwight Yorke", "Aston Villa", False),
    ("FS-EC", "Eric Cantona", "Manchester United", False),
    ("FS-GN", "Gary Neville", "Manchester United", False),
    ("FS-IW", "Ian Wright", "Arsenal", False),
    ("FS-LF", "Les Ferdinand", "Newcastle United", False),
    ("FS-PS", "Peter Schmeichel", "Manchester United", False),
    ("FS-RF", "Robbie Fowler", "Liverpool FC", False),
    ("FS-RG", "Ruud Gullit", "Chelsea", False),
    ("FS-RL", "Rob Lee", "Newcastle United", False),
    ("FS-SC", "Stan Collymore", "Liverpool FC", False),
    ("FS-SS", "Steve Stone", "Nottingham Forest", False),
    ("FS-TA", "Tony Adams", "Arsenal", False),
    ("FS-TS", "Teddy Sheringham", "Tottenham Hotspur", False),
]

# Finest Partnerships: dual cards — (code, player1, player2, team)
FINEST_PARTNERSHIPS_RAW = [
    ("FP-AS", "Darren Anderton", "Teddy Sheringham", "Tottenham Hotspur"),
    ("FP-CY", "Dwight Yorke", "Andy Cole", "Manchester United"),
    ("FP-DK", "Robbie Keane", "Jermain Defoe", "Tottenham Hotspur"),
    ("FP-DL", "Didier Drogba", "Frank Lampard", "Chelsea"),
    ("FP-GH", "Jimmy Floyd Hasselbaink", "Eiður Guðjohnsen", "Chelsea"),
    ("FP-HB", "Thierry Henry", "Dennis Bergkamp", "Arsenal"),
    ("FP-HP", "Thierry Henry", "Robert Pirès", "Arsenal"),
    ("FP-KS", "Heung-Min Son", "Harry Kane", "Tottenham Hotspur"),
    ("FP-MS", "Gabriel Magalhães", "William Saliba", "Arsenal"),
    ("FP-PQ", "Niall Quinn", "Kevin Phillips", "Sunderland"),
    ("FP-SF", "Alan Shearer", "Les Ferdinand", "Newcastle United"),
    ("FP-SM", "Sadio Mané", "Mohamed Salah", "Liverpool FC"),
    ("FP-SS", "Luis Suárez", "Daniel Sturridge", "Liverpool FC"),
    ("FP-TC", "John Terry", "Ricardo Carvalho", "Chelsea"),
    ("FP-ZP", "Gustavo Poyet", "Gianfranco Zola", "Chelsea"),
]

ARRIVALS_AUTO_RAW = [
    ("AA-AI", "Amir Ibragimov", "Manchester United", True),
    ("AA-BB", "Ben Broggio", "Aston Villa", True),
    ("AA-BM", "Bendito Mantato", "Manchester United", True),
    ("AA-CR", "Chris Rigg", "Sunderland", True),
    ("AA-EW", "Estêvão Willian", "Chelsea", True),
    ("AA-JK", "Josh King", "Fulham", True),
    ("AA-MD", "Max Dowman", "Arsenal", True),
    ("AA-RD", "Romelle Donovan", "Brentford", True),
    ("AA-RN", "Rio Ngumoha", "Liverpool FC", True),
    ("AA-SL", "Shea Lacey", "Manchester United", True),
    ("AA-TW", "Tom Watson", "Brighton & Hove Albion", True),
]

MAIN_ATTRACTION_AUTO_RAW = [
    ("MA-AC", "Andy Cole", "Manchester United", False),
    ("MA-BF", "Bruno Fernandes", "Manchester United", False),
    ("MA-CP", "Cole Palmer", "Chelsea", False),
    ("MA-CT", "Carlos Tevez", "Manchester City", False),
    ("MA-DS", "David Silva", "Manchester City", False),
    ("MA-EW", "Estêvão Willian", "Chelsea", True),
    ("MA-GB", "Gareth Bale", "Tottenham Hotspur", False),
    ("MA-JG", "Jack Grealish", "Everton", False),
    ("MA-LM", "Luka Modrić", "Tottenham Hotspur", False),
    ("MA-MC", "Matheus Cunha", "Manchester United", False),
    ("MA-MO", "Moisés Caicedo", "Chelsea", False),
    ("MA-MR", "Morgan Rogers", "Aston Villa", False),
    ("MA-MS", "Mohamed Salah", "Liverpool FC", False),
    ("MA-MZ", "Martín Zubimendi", "Arsenal", False),
    ("MA-RO", "Rodri", "Manchester City", False),
    ("MA-VD", "Virgil van Dijk", "Liverpool FC", False),
]

GUSTOGRAPHS_RAW = [
    ("GG-AG", "Anthony Gordon", "Newcastle United", False),
    ("GG-BG", "Bruno Guimarães", "Newcastle United", False),
    ("GG-BS", "Benjamin Šeško", "Manchester United", False),
    ("GG-CR", "Chris Rigg", "Sunderland", True),
    ("GG-DR", "Declan Rice", "Arsenal", False),
    ("GG-DS", "Dominik Szoboszlai", "Liverpool FC", False),
    ("GG-EF", "Enzo Fernández", "Chelsea", False),
    ("GG-HE", "Hugo Ekitike", "Liverpool FC", False),
    ("GG-JB", "Jarrod Bowen", "West Ham United", False),
    ("GG-JP", "João Pedro", "Chelsea", False),
    ("GG-KH", "Kai Havertz", "Arsenal", False),
    ("GG-MK", "Mohammed Kudus", "Tottenham Hotspur", False),
    ("GG-MZ", "Martín Zubimendi", "Arsenal", False),
    ("GG-SL", "Shea Lacey", "Manchester United", True),
    ("GG-TR", "Tijjani Reijnders", "Manchester City", False),
]

# Finest Fans: (code, name, team_or_None)
FINEST_FANS_RAW = [
    ("FF-AH", "Anne Hathaway", "Arsenal"),
    ("FF-CT", "Charlize Theron", None),
    ("FF-JM", "Joe Marler", "Brighton & Hove Albion"),
    ("FF-JS", "Jill Scott", "Sunderland"),
    ("FF-LBJ", "LeBron James", "Liverpool FC"),
    ("FF-LW", "Laura Woods", "Arsenal"),
    ("FF-MB", "Mel B", "Leeds United"),
    ("FF-MBB", "Millie Bobby Brown", "Liverpool FC"),
    ("FF-MC", "Mel C", "Liverpool FC"),
    ("FF-RI", "Ralph Ineson", "Leeds United"),
    ("FF-SB", "Stuart Broad", "Nottingham Forest"),
    ("FF-SLJ", "Samuel L. Jackson", "Liverpool FC"),
]

# ---------------------------------------------------------------------------
# Build sections list (ordered)
# ---------------------------------------------------------------------------

ALL_SECTIONS_RAW = [
    ("Base Set",                          BASE_CARDS_RAW,              False),
    ("Expected Brilliance",               EXPECTED_BRILLIANCE_RAW,     False),
    ("Swerve",                            SWERVE_RAW,                  False),
    ("Swerve Fusion Variation",           SWERVE_FUSION_RAW,           False),
    ("Arrivals",                          ARRIVALS_RAW,                 True),   # all RC
    ("Clean",                             CLEAN_RAW,                   False),
    ("Gusto",                             GUSTO_RAW,                   False),
    ("Nightmare Fuel",                    NIGHTMARE_FUEL_RAW,          False),
    ("Main Attraction",                   MAIN_ATTRACTION_RAW,         False),
    ("Polka",                             POLKA_RAW,                   False),
    ("Headliners",                        HEADLINERS_RAW,              False),
    ("Aura",                              AURA_RAW,                    False),
    ("Finest Idols",                      FINEST_IDOLS_RAW,            False),
    ("Finest Autographs",                 FINEST_AUTOGRAPHS_RAW,       False),
    ("Finest Moments Autographs",         FINEST_MOMENTS_AUTOS_RAW,    False),
    ("Finest Seasons 1995-96",            FINEST_SEASONS_RAW,          False),
    ("Arrivals Autograph Edition",        ARRIVALS_AUTO_RAW,            True),   # all RC
    ("Main Attraction Autograph Edition", MAIN_ATTRACTION_AUTO_RAW,    False),
    ("Gustographs",                       GUSTOGRAPHS_RAW,             False),
    ("Finest Fans",                       FINEST_FANS_RAW,             False),
]

# ---------------------------------------------------------------------------
# Build output
# ---------------------------------------------------------------------------

def calc_stats(appearances, section_parallels_map):
    unique_cards = 0
    total_print_run = 0
    one_of_ones = 0
    insert_set_names = set()
    for app in appearances:
        insert_set_names.add(app["insert_set"])
        pars = section_parallels_map.get(app["insert_set"], [])
        numbered = [p for p in pars if p["print_run"] is not None]
        unique_cards += 1 + len(numbered)
        total_print_run += sum(p["print_run"] for p in numbered)
        one_of_ones += sum(1 for p in numbered if p["print_run"] == 1)
    return {
        "unique_cards": unique_cards,
        "total_print_run": total_print_run,
        "one_of_ones": one_of_ones,
        "insert_sets": len(insert_set_names),
    }


def build():
    sections = []
    # player name → list of appearances
    players_map = {}  # name → {appearances: [], is_rookie_globally: bool}

    def add_player_appearance(name, appearance, is_rc_flag):
        if name not in players_map:
            players_map[name] = {"appearances": [], "is_rookie_globally": False}
        players_map[name]["appearances"].append(appearance)
        if is_rc_flag:
            players_map[name]["is_rookie_globally"] = True

    # --- Finest Partnerships (dual cards — processed before main loop) ---
    fp_parallels = SECTION_PARALLELS["Finest Partnerships"]
    fp_section_cards = []
    for code, player1, player2, team in FINEST_PARTNERSHIPS_RAW:
        for player_name in [player1, player2]:
            app = {
                "insert_set": "Finest Partnerships",
                "card_number": code,
                "team": team,
                "is_rookie": False,
                "subset_tag": None,
                "parallels": fp_parallels,
            }
            add_player_appearance(player_name, app, False)
        fp_section_cards.append({
            "card_number": code,
            "player": player1,
            "team": team,
            "is_rookie": False,
            "subset": None,
        })
    sections.append({
        "insert_set": "Finest Partnerships",
        "parallels": fp_parallels,
        "cards": fp_section_cards,
    })

    for section_name, cards_raw, all_rc in ALL_SECTIONS_RAW:
        parallels_list = SECTION_PARALLELS.get(section_name, [])

        # --- Handle Finest Partnerships (dual cards) ---
        if section_name == "Finest Partnerships":
            section_cards = []
            for code, player1, player2, team in cards_raw:
                # Both players share the same card code
                for player_name in [player1, player2]:
                    app = {
                        "insert_set": section_name,
                        "card_number": code,
                        "team": team,
                        "is_rookie": False,
                        "subset_tag": None,
                        "parallels": parallels_list,
                    }
                    add_player_appearance(player_name, app, False)
                # For sections list: store first player as representative card entry
                section_cards.append({
                    "card_number": code,
                    "player": player1,
                    "team": team,
                    "is_rookie": False,
                    "subset": None,
                })
            sections.append({
                "insert_set": section_name,
                "parallels": parallels_list,
                "cards": section_cards,
            })
            continue

        # --- Handle Finest Fans (nullable team) ---
        if section_name == "Finest Fans":
            section_cards = []
            for code, name, team in cards_raw:
                app = {
                    "insert_set": section_name,
                    "card_number": code,
                    "team": team,
                    "is_rookie": False,
                    "subset_tag": None,
                    "parallels": parallels_list,
                }
                add_player_appearance(name, app, False)
                section_cards.append({
                    "card_number": code,
                    "player": name,
                    "team": team,
                    "is_rookie": False,
                    "subset": None,
                })
            sections.append({
                "insert_set": section_name,
                "parallels": parallels_list,
                "cards": section_cards,
            })
            continue

        # --- Normal sections ---
        section_cards = []
        for code, name, team, is_rc in cards_raw:
            effective_rc = is_rc or all_rc
            app = {
                "insert_set": section_name,
                "card_number": code,
                "team": team,
                "is_rookie": effective_rc,
                "subset_tag": None,
                "parallels": parallels_list,
            }
            add_player_appearance(name, app, effective_rc)
            section_cards.append({
                "card_number": code,
                "player": name,
                "team": team,
                "is_rookie": effective_rc,
                "subset": None,
            })
        sections.append({
            "insert_set": section_name,
            "parallels": parallels_list,
            "cards": section_cards,
        })

    # --- RC propagation: apply is_rookie globally ---
    for player_name, pdata in players_map.items():
        if pdata["is_rookie_globally"]:
            for app in pdata["appearances"]:
                app["is_rookie"] = True

    # --- Build players list ---
    players_out = []
    for player_name, pdata in players_map.items():
        # Strip parallels key from appearances before output
        appearances_out = []
        for app in pdata["appearances"]:
            appearances_out.append({
                "insert_set": app["insert_set"],
                "card_number": app["card_number"],
                "team": app["team"],
                "is_rookie": app["is_rookie"],
                "subset_tag": app.get("subset_tag"),
            })
        stats = calc_stats(pdata["appearances"], SECTION_PARALLELS)
        players_out.append({
            "player": player_name,
            "appearances": appearances_out,
            "stats": stats,
        })

    return {
        "set_name": "2026 Topps Finest Premier League",
        "sport": "Soccer",
        "season": "2025-26",
        "league": "Premier League",
        "sections": sections,
        "players": players_out,
    }


if __name__ == "__main__":
    import os
    result = build()
    out_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "finest_pl_2026_parsed.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    total_cards = sum(len(s["cards"]) for s in result["sections"])
    print(f"Sections:   {len(result['sections'])}")
    print(f"Players:    {len(result['players'])}")
    print(f"Cards:      {total_cards}")
    print(f"Written to: {out_path}")
