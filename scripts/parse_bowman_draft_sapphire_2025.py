"""
Parser for 2025 Bowman Draft Sapphire Baseball.

sport: Baseball, league: MLB, season: 2025, tier: Sapphire
No is_rookie — all players are prospects/draft picks.
Normalize "Athletics" → "Oakland Athletics".
"""

from __future__ import annotations
import json

SET_NAME = "2025 Bowman Draft Sapphire Baseball"
SPORT = "Baseball"
SEASON = "2025"
LEAGUE = "MLB"

# ── Name / team normalization ─────────────────────────────────────────────────

TEAM_FIXES = {
    "Athletics": "Oakland Athletics",
}

def fix_team(team: str) -> str:
    return TEAM_FIXES.get(team.strip(), team.strip())

# ── Parallels ─────────────────────────────────────────────────────────────────

BASE_PARALLELS = [
    {"name": "Yellow", "print_run": 75},
    {"name": "Gold", "print_run": 50},
    {"name": "Orange", "print_run": 25},
    {"name": "Black", "print_run": 10},
    {"name": "Red", "print_run": 5},
    {"name": "Padparadscha", "print_run": 1},
]

CPA_PARALLELS = [
    {"name": "Green Sapphire", "print_run": 99},
    {"name": "Gold Sapphire", "print_run": 50},
    {"name": "Orange Sapphire", "print_run": 25},
    {"name": "Black Sapphire", "print_run": 10},
    {"name": "Red Sapphire", "print_run": 5},
    {"name": "Padparadscha Sapphire", "print_run": 1},
]

SSA_PARALLELS = [
    {"name": "Orange Sapphire", "print_run": 25},
    {"name": "Red Sapphire", "print_run": 5},
    {"name": "Superfractor", "print_run": 1},
]

SS_PARALLELS = [
    {"name": "Gold Refractor", "print_run": 50},
    {"name": "Orange Refractor", "print_run": 25},
    {"name": "Red Refractor", "print_run": 5},
    {"name": "Superfractor", "print_run": 1},
]

# ── Base Set (200 cards) ──────────────────────────────────────────────────────

BASE_SET_RAW = [
    ("BDC-1", "Eli Willits", "Washington Nationals"),
    ("BDC-2", "Xavier Neyens", "Houston Astros"),
    ("BDC-3", "Kade Anderson", "Seattle Mariners"),
    ("BDC-4", "Gage Wood", "Philadelphia Phillies"),
    ("BDC-5", "Max Belyeu", "Colorado Rockies"),
    ("BDC-6", "Aidan West", "Los Angeles Dodgers"),
    ("BDC-7", "Taitin Gray", "Tampa Bay Rays"),
    ("BDC-8", "JoJo Parker", "Toronto Blue Jays"),
    ("BDC-9", "Spencer Jones", "New York Yankees"),
    ("BDC-10", "Billy Carlson", "Chicago White Sox"),
    ("BDC-11", "Mike Sirota", "Los Angeles Dodgers"),
    ("BDC-12", "Liam Doyle", "St. Louis Cardinals"),
    ("BDC-13", "Franklin Arias", "Boston Red Sox"),
    ("BDC-14", "J.D. Thompson", "Milwaukee Brewers"),
    ("BDC-15", "Gavin Fien", "Texas Rangers"),
    ("BDC-16", "Ike Irish", "Baltimore Orioles"),
    ("BDC-17", "Ethan Conrad", "Chicago Cubs"),
    ("BDC-18", "Braden Montgomery", "Chicago White Sox"),
    ("BDC-19", "Roc Riggio", "Colorado Rockies"),
    ("BDC-20", "Steele Hall", "Cincinnati Reds"),
    ("BDC-21", "Josiah Hartshorn", "Chicago Cubs"),
    ("BDC-22", "Zach Root", "Los Angeles Dodgers"),
    ("BDC-23", "Riley Quick", "Minnesota Twins"),
    ("BDC-24", "Joswa Lugo", "Los Angeles Angels"),
    ("BDC-25", "Seth Hernandez", "Pittsburgh Pirates"),
    ("BDC-26", "Thomas White", "Miami Marlins"),
    ("BDC-27", "Mason Peters", "Seattle Mariners"),
    ("BDC-28", "Gavin Turley", "Oakland Athletics"),
    ("BDC-29", "Kyson Witherspoon", "Boston Red Sox"),
    ("BDC-30", "Jamie Arnold", "Oakland Athletics"),
    ("BDC-31", "Yandel Ricardo", "Kansas City Royals"),
    ("BDC-32", "Tyson Lewis", "Cincinnati Reds"),
    ("BDC-33", "Dante Nori", "Philadelphia Phillies"),
    ("BDC-34", "Andrew Salas", "Miami Marlins"),
    ("BDC-35", "Arjun Nimmala", "Toronto Blue Jays"),
    ("BDC-36", "Tommy Troy", "Arizona Diamondbacks"),
    ("BDC-37", "Tyler Bremner", "Los Angeles Angels"),
    ("BDC-38", "Nate Snead", "Los Angeles Angels"),
    ("BDC-39", "Eduardo Tait", "Minnesota Twins"),
    ("BDC-40", "Gavin Kilen", "San Francisco Giants"),
    ("BDC-41", "Ryan Waldschmidt", "Arizona Diamondbacks"),
    ("BDC-42", "Jacob Morrison", "Milwaukee Brewers"),
    ("BDC-43", "George Lombard Jr.", "New York Yankees"),
    ("BDC-44", "Landon Harmon", "Washington Nationals"),
    ("BDC-45", "Walker Janek", "Houston Astros"),
    ("BDC-46", "Trevor Cohen", "San Francisco Giants"),
    ("BDC-47", "Colin Yeaman", "Baltimore Orioles"),
    ("BDC-48", "Max Clark", "Detroit Tigers"),
    ("BDC-49", "Travis Bazzana", "Cleveland Guardians"),
    ("BDC-50", "Easton Carmichael", "Pittsburgh Pirates"),
    ("BDC-51", "AJ Russell", "Texas Rangers"),
    ("BDC-52", "Pico Kohn", "New York Yankees"),
    ("BDC-53", "Dominick Reid", "Chicago Cubs"),
    ("BDC-54", "Marcus Phillips", "Boston Red Sox"),
    ("BDC-55", "Jhonny Level", "San Francisco Giants"),
    ("BDC-56", "Antonio Jimenez", "New York Mets"),
    ("BDC-57", "Matthew Miura", "St. Louis Cardinals"),
    ("BDC-58", "Ty Harvey", "San Diego Padres"),
    ("BDC-59", "Kevin McGonigle", "Detroit Tigers"),
    ("BDC-60", "Josue Briceno", "Detroit Tigers"),
    ("BDC-61", "Luke Dickerson", "Washington Nationals"),
    ("BDC-62", "Justin Lamkin", "Kansas City Royals"),
    ("BDC-63", "Caden Bodine", "Baltimore Orioles"),
    ("BDC-64", "Brandon Compton", "Miami Marlins"),
    ("BDC-65", "Kaeden Kent", "New York Yankees"),
    ("BDC-66", "Mason Morris", "Cincinnati Reds"),
    ("BDC-67", "Ethan Frey", "Houston Astros"),
    ("BDC-68", "Max Williams", "Miami Marlins"),
    ("BDC-69", "Korbyn Dickerson", "Seattle Mariners"),
    ("BDC-70", "Tate Southisene", "Atlanta Braves"),
    ("BDC-71", "Mitch Voit", "New York Mets"),
    ("BDC-72", "Rainiel Rodriguez", "St. Louis Cardinals"),
    ("BDC-73", "Tim Piasentin", "Toronto Blue Jays"),
    ("BDC-74", "James Tibbs III", "Los Angeles Dodgers"),
    ("BDC-75", "Jefferson Rojas", "Chicago Cubs"),
    ("BDC-76", "Michael Salina", "San Diego Padres"),
    ("BDC-77", "Ryan Mitchell", "St. Louis Cardinals"),
    ("BDC-78", "JB Middleton", "Colorado Rockies"),
    ("BDC-79", "Riley Kelly", "Colorado Rockies"),
    ("BDC-80", "Cade Obermueller", "Philadelphia Phillies"),
    ("BDC-81", "Briggs McKenzie", "Atlanta Braves"),
    ("BDC-82", "Joshua Flores", "Milwaukee Brewers"),
    ("BDC-83", "Gabe Davis", "Chicago White Sox"),
    ("BDC-84", "Kayson Cunningham", "Arizona Diamondbacks"),
    ("BDC-85", "JT Quinn", "Baltimore Orioles"),
    ("BDC-86", "Nolan Sailors", "Kansas City Royals"),
    ("BDC-87", "Leo De Vries", "Oakland Athletics"),
    ("BDC-88", "Tommy White", "Oakland Athletics"),
    ("BDC-89", "Patrick Forbes", "Arizona Diamondbacks"),
    ("BDC-90", "Tanner Franklin", "St. Louis Cardinals"),
    ("BDC-91", "Cody Miller", "Atlanta Braves"),
    ("BDC-92", "Quentin Young", "Minnesota Twins"),
    ("BDC-93", "Landon Hodge", "Chicago White Sox"),
    ("BDC-94", "Ryan Sloan", "Seattle Mariners"),
    ("BDC-95", "Kash Mayfield", "San Diego Padres"),
    ("BDC-96", "Charles Davalan", "Los Angeles Dodgers"),
    ("BDC-97", "Jake Cook", "Toronto Blue Jays"),
    ("BDC-98", "Aroon Escobar", "Philadelphia Phillies"),
    ("BDC-99", "Cameron Maldonado", "San Francisco Giants"),
    ("BDC-100", "Nick Becker", "Seattle Mariners"),
    ("BDC-101", "Griffin Hugus", "Seattle Mariners"),
    ("BDC-102", "Konnor Griffin", "Pittsburgh Pirates"),
    ("BDC-103", "Felnin Celesten", "Seattle Mariners"),
    ("BDC-104", "Sean Youngerman", "Philadelphia Phillies"),
    ("BDC-105", "Luis Pena", "Milwaukee Brewers"),
    ("BDC-106", "Matthew Fisher", "Philadelphia Phillies"),
    ("BDC-107", "Yolfran Castillo", "Texas Rangers"),
    ("BDC-108", "Murf Gray", "Pittsburgh Pirates"),
    ("BDC-109", "Mason Neville", "Cincinnati Reds"),
    ("BDC-110", "Esmerlyn Valdez", "Pittsburgh Pirates"),
    ("BDC-111", "Eduardo Quintero", "Los Angeles Dodgers"),
    ("BDC-112", "Gustavo Melendez", "Pittsburgh Pirates"),
    ("BDC-113", "Nate George", "Baltimore Orioles"),
    ("BDC-114", "Dean Moss", "Tampa Bay Rays"),
    ("BDC-115", "Elian Pena", "New York Mets"),
    ("BDC-116", "Anthony Eyanson", "Boston Red Sox"),
    ("BDC-117", "Mason McConnaughey", "Texas Rangers"),
    ("BDC-118", "Michael Lombardi", "Kansas City Royals"),
    ("BDC-119", "Josh Owens", "Texas Rangers"),
    ("BDC-120", "Kaelen Culpepper", "Minnesota Twins"),
    ("BDC-121", "Theo Gillen", "Tampa Bay Rays"),
    ("BDC-122", "Cam Caminiti", "Atlanta Braves"),
    ("BDC-123", "Luke Lacourse", "Los Angeles Angels"),
    ("BDC-124", "Conor Essenburg", "Atlanta Braves"),
    ("BDC-125", "Joshua Kuroda-Grauer", "Oakland Athletics"),
    ("BDC-126", "Adonys Guzman", "Pittsburgh Pirates"),
    ("BDC-127", "Christian Foutch", "Boston Red Sox"),
    ("BDC-128", "Jake Munroe", "Los Angeles Angels"),
    ("BDC-129", "Dean Curley", "Cleveland Guardians"),
    ("BDC-130", "Cameron Nelson", "Colorado Rockies"),
    ("BDC-131", "Kaleb Wing", "Chicago Cubs"),
    ("BDC-132", "Carlos Lagrange", "New York Yankees"),
    ("BDC-133", "Alfredo Duno", "Cincinnati Reds"),
    ("BDC-134", "Aaron Walton", "Cleveland Guardians"),
    ("BDC-135", "Devin Taylor", "Oakland Athletics"),
    ("BDC-136", "Charlie Condon", "Colorado Rockies"),
    ("BDC-137", "Travis Sykora", "Washington Nationals"),
    ("BDC-138", "Carson Benge", "New York Mets"),
    ("BDC-139", "Dakota Jordan", "San Francisco Giants"),
    ("BDC-140", "Cody Bowker", "Philadelphia Phillies"),
    ("BDC-141", "Ben Jacobs", "Detroit Tigers"),
    ("BDC-142", "Chase Shores", "Los Angeles Angels"),
    ("BDC-143", "Brody Brecht", "Colorado Rockies"),
    ("BDC-144", "Kyle Lodise", "Chicago White Sox"),
    ("BDC-145", "JJ Wetherholt", "St. Louis Cardinals"),
    ("BDC-146", "Dax Kilby", "New York Yankees"),
    ("BDC-147", "Jared Thomas", "Colorado Rockies"),
    ("BDC-148", "Ethan Hedges", "Colorado Rockies"),
    ("BDC-149", "Sean Episcope", "Milwaukee Brewers"),
    ("BDC-150", "Jack Gurevitch", "St. Louis Cardinals"),
    ("BDC-151", "Ethan Petry", "Washington Nationals"),
    ("BDC-152", "Slade Caldwell", "Arizona Diamondbacks"),
    ("BDC-153", "Johnny Slawinski", "Los Angeles Angels"),
    ("BDC-154", "Matt Barr", "Minnesota Twins"),
    ("BDC-155", "Bryce Cunningham", "New York Yankees"),
    ("BDC-156", "Michael Oliveto", "Detroit Tigers"),
    ("BDC-157", "Cooper Pratt", "Milwaukee Brewers"),
    ("BDC-158", "Landyn Vidourek", "Los Angeles Dodgers"),
    ("BDC-159", "Walker Jenkins", "Minnesota Twins"),
    ("BDC-160", "Blake Mitchell", "Kansas City Royals"),
    ("BDC-161", "JD Dix", "Arizona Diamondbacks"),
    ("BDC-162", "Jordan Yost", "Detroit Tigers"),
    ("BDC-163", "Jonny Farmelo", "Seattle Mariners"),
    ("BDC-164", "James Ellwanger", "Minnesota Twins"),
    ("BDC-165", "Ching-Hsien Ko", "Los Angeles Dodgers"),
    ("BDC-166", "Cooper Flemming", "Tampa Bay Rays"),
    ("BDC-167", "Hagen Smith", "Chicago White Sox"),
    ("BDC-168", "Thayron Liranzo", "Detroit Tigers"),
    ("BDC-169", "Sebastian Walcott", "Texas Rangers"),
    ("BDC-170", "Brian Curley", "Arizona Diamondbacks"),
    ("BDC-171", "Grant Richardson", "Oakland Athletics"),
    ("BDC-172", "Malachi Witherspoon", "Detroit Tigers"),
    ("BDC-173", "Jaxon Wiggins", "Chicago Cubs"),
    ("BDC-174", "Shotaro Morii", "Oakland Athletics"),
    ("BDC-175", "Dean Livingston", "Arizona Diamondbacks"),
    ("BDC-176", "Cameron Millar", "Kansas City Royals"),
    ("BDC-177", "Yohandy Morales", "Washington Nationals"),
    ("BDC-178", "Sean Gamble", "Kansas City Royals"),
    ("BDC-179", "Peter Kussow", "New York Mets"),
    ("BDC-180", "Aidan Miller", "Philadelphia Phillies"),
    ("BDC-181", "Miguel Sime Jr.", "Washington Nationals"),
    ("BDC-182", "Josuar Gonzalez", "San Francisco Giants"),
    ("BDC-183", "Cade Crossland", "St. Louis Cardinals"),
    ("BDC-184", "Caleb Bonemer", "Chicago White Sox"),
    ("BDC-185", "Josh Hammond", "Kansas City Royals"),
    ("BDC-186", "Joseph Dzierwa", "Baltimore Orioles"),
    ("BDC-187", "Sammy Stafura", "Pittsburgh Pirates"),
    ("BDC-188", "Jacob Reimer", "New York Mets"),
    ("BDC-189", "Dominic Fritton", "Tampa Bay Rays"),
    ("BDC-190", "Ryan Wideman", "San Diego Padres"),
    ("BDC-191", "Malcolm Moore", "Texas Rangers"),
    ("BDC-192", "Nolan Schubart", "Cleveland Guardians"),
    ("BDC-193", "Aaron Watson", "Cincinnati Reds"),
    ("BDC-194", "Brady Ebel", "Milwaukee Brewers"),
    ("BDC-195", "Caleb Leys", "Detroit Tigers"),
    ("BDC-196", "Jesus Made", "Milwaukee Brewers"),
    ("BDC-197", "CJ Gray", "Los Angeles Angels"),
    ("BDC-198", "Enrique Bradfield Jr.", "Baltimore Orioles"),
    ("BDC-199", "JR Ritchie", "Atlanta Braves"),
    ("BDC-200", "Kane Kepley", "Chicago Cubs"),
]

# ── Chrome Prospect Autographs (30 cards) ────────────────────────────────────

CPA_RAW = [
    ("CPA-BC", "Billy Carlson", "Chicago White Sox"),
    ("CPA-BCO", "Brandon Compton", "Miami Marlins"),
    ("CPA-BE", "Brady Ebel", "Milwaukee Brewers"),
    ("CPA-CB", "Caden Bodine", "Baltimore Orioles"),
    ("CPA-CD", "Charles Davalan", "Los Angeles Dodgers"),
    ("CPA-DK", "Dax Kilby", "New York Yankees"),
    ("CPA-EC", "Ethan Conrad", "Chicago Cubs"),
    ("CPA-EP", "Ethan Petry", "Washington Nationals"),
    ("CPA-EW", "Eli Willits", "Washington Nationals"),
    ("CPA-GF", "Gavin Fien", "Texas Rangers"),
    ("CPA-GK", "Gavin Kilen", "San Francisco Giants"),
    ("CPA-GW", "Gage Wood", "Philadelphia Phillies"),
    ("CPA-II", "Ike Irish", "Baltimore Orioles"),
    ("CPA-JH", "Josh Hammond", "Kansas City Royals"),
    ("CPA-JP", "JoJo Parker", "Toronto Blue Jays"),
    ("CPA-KA", "Kade Anderson", "Seattle Mariners"),
    ("CPA-KC", "Kayson Cunningham", "Arizona Diamondbacks"),
    ("CPA-KK", "Kane Kepley", "Chicago Cubs"),
    ("CPA-LD", "Liam Doyle", "St. Louis Cardinals"),
    ("CPA-MB", "Max Belyeu", "Colorado Rockies"),
    ("CPA-MP", "Marcus Phillips", "Boston Red Sox"),
    ("CPA-MV", "Mitch Voit", "New York Mets"),
    ("CPA-PF", "Patrick Forbes", "Arizona Diamondbacks"),
    ("CPA-QY", "Quentin Young", "Minnesota Twins"),
    ("CPA-RQ", "Riley Quick", "Minnesota Twins"),
    ("CPA-SH", "Seth Hernandez", "Pittsburgh Pirates"),
    ("CPA-SHA", "Steele Hall", "Cincinnati Reds"),
    ("CPA-TB", "Tyler Bremner", "Los Angeles Angels"),
    ("CPA-TS", "Tate Southisene", "Atlanta Braves"),
    ("CPA-XN", "Xavier Neyens", "Houston Astros"),
]

# ── Sapphire Selections Autographs (15 cards) ────────────────────────────────

SSA_RAW = [
    ("SSA-BC", "Billy Carlson", "Chicago White Sox"),
    ("SSA-BE", "Brady Ebel", "Milwaukee Brewers"),
    ("SSA-EW", "Eli Willits", "Washington Nationals"),
    ("SSA-GF", "Gavin Fien", "Texas Rangers"),
    ("SSA-GK", "Gavin Kilen", "San Francisco Giants"),
    ("SSA-II", "Ike Irish", "Baltimore Orioles"),
    ("SSA-JA", "Jamie Arnold", "Oakland Athletics"),
    ("SSA-JP", "JoJo Parker", "Toronto Blue Jays"),
    ("SSA-KA", "Kade Anderson", "Seattle Mariners"),
    ("SSA-KC", "Kayson Cunningham", "Arizona Diamondbacks"),
    ("SSA-KW", "Kyson Witherspoon", "Boston Red Sox"),
    ("SSA-LD", "Liam Doyle", "St. Louis Cardinals"),
    ("SSA-SH", "Seth Hernandez", "Pittsburgh Pirates"),
    ("SSA-SHA", "Steele Hall", "Cincinnati Reds"),
    ("SSA-TB", "Tyler Bremner", "Los Angeles Angels"),
]

# ── Sapphire Selections insert (18 cards) ────────────────────────────────────

SS_RAW = [
    ("SS-1", "Gavin Fien", "Texas Rangers"),
    ("SS-2", "Kyson Witherspoon", "Boston Red Sox"),
    ("SS-3", "Kade Anderson", "Seattle Mariners"),
    ("SS-4", "Tyler Bremner", "Los Angeles Angels"),
    ("SS-5", "Liam Doyle", "St. Louis Cardinals"),
    ("SS-6", "Seth Hernandez", "Pittsburgh Pirates"),
    ("SS-7", "Ike Irish", "Baltimore Orioles"),
    ("SS-8", "Eli Willits", "Washington Nationals"),
    ("SS-9", "Brady Ebel", "Milwaukee Brewers"),
    ("SS-10", "Gage Wood", "Philadelphia Phillies"),
    ("SS-11", "Tate Southisene", "Atlanta Braves"),
    ("SS-12", "Steele Hall", "Cincinnati Reds"),
    ("SS-13", "JoJo Parker", "Toronto Blue Jays"),
    ("SS-14", "Billy Carlson", "Chicago White Sox"),
    ("SS-15", "Jamie Arnold", "Oakland Athletics"),
    ("SS-16", "Kayson Cunningham", "Arizona Diamondbacks"),
    ("SS-17", "Gavin Kilen", "San Francisco Giants"),
    ("SS-18", "Xavier Neyens", "Houston Astros"),
]

# ── Build sections ────────────────────────────────────────────────────────────

def build_cards(raw: list[tuple]) -> list[dict]:
    return [
        {
            "card_number": str(num),
            "player": name,
            "team": fix_team(team),
            "is_rookie": False,
            "subset": None,
        }
        for num, name, team in raw
    ]


def build_section(name: str, cards: list[dict], parallels: list[dict]) -> dict:
    return {"insert_set": name, "parallels": parallels, "cards": cards}


SECTIONS_DEF = [
    ("Base Set", build_cards(BASE_SET_RAW), BASE_PARALLELS),
    ("Chrome Prospect Autographs", build_cards(CPA_RAW), CPA_PARALLELS),
    ("Sapphire Selections Autographs", build_cards(SSA_RAW), SSA_PARALLELS),
    ("Sapphire Selections", build_cards(SS_RAW), SS_PARALLELS),
]

sections = [build_section(name, cards, pars) for name, cards, pars in SECTIONS_DEF]

# ── Build players ─────────────────────────────────────────────────────────────

players_map: dict[str, dict] = {}

for section in sections:
    for card in section["cards"]:
        key = card["player"].lower()
        if key not in players_map:
            players_map[key] = {
                "player": card["player"],
                "appearances": [],
                "_insert_sets": set(),
            }
        players_map[key]["appearances"].append({
            "insert_set": section["insert_set"],
            "card_number": card["card_number"],
            "team": card["team"],
            "is_rookie": False,
            "subset_tag": None,
            "parallels": section["parallels"],
        })
        players_map[key]["_insert_sets"].add(section["insert_set"])

# Compute stats
players_list = []
for p in sorted(players_map.values(), key=lambda x: x["player"].lower()):
    numbered = []
    for app in p["appearances"]:
        for par in app["parallels"]:
            if par["print_run"] is not None:
                numbered.append(par["print_run"])
    stats = {
        "unique_cards": len(p["appearances"]),
        "total_print_run": sum(numbered),
        "one_of_ones": sum(1 for pr in numbered if pr == 1),
        "insert_sets": len(p["_insert_sets"]),
    }
    players_list.append({
        "player": p["player"],
        "appearances": p["appearances"],
        "stats": stats,
    })

# ── Output ────────────────────────────────────────────────────────────────────

output = {
    "set_name": SET_NAME,
    "sport": SPORT,
    "season": SEASON,
    "league": LEAGUE,
    "sections": sections,
    "players": players_list,
}

total_cards = sum(len(s["cards"]) for s in sections)
unique_players = len(players_list)

print(f"Set: {SET_NAME}")
print(f"Sections: {len(sections)}")
print(f"Total cards: {total_cards}")
print(f"Unique players: {unique_players}")
print(f"Base set: {len(BASE_SET_RAW)} cards")
print(f"Chrome Prospect Autographs: {len(CPA_RAW)} cards")
print(f"Sapphire Selections Autographs: {len(SSA_RAW)} cards")
print(f"Sapphire Selections: {len(SS_RAW)} cards")

out_path = "scripts/bowman_draft_sapphire_2025_parsed.json"
with open(out_path, "w") as f:
    json.dump(output, f, indent=2)
print(f"\nWrote {out_path}")
