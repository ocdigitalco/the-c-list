"""
Parser for 2025 Topps Chrome McDonald's All-American Basketball.

No is_rookie tags — these are high school prospects, not NBA rookies.
Team field = "East" or "West".
"""

import json

SET_NAME = "2025 Topps Chrome McDonald's All-American Basketball"
SPORT = "Basketball"
SEASON = "2025"
LEAGUE = "McDonald's"

# Name normalization
NAME_FIXES = {
    "zakiyah johnson": "ZaKiyah Johnson",
    "ronald holland ii": "Ron Holland II",
}

def fix_name(name: str) -> str:
    key = name.lower().strip()
    if key in NAME_FIXES:
        return NAME_FIXES[key]
    return name.strip()

# ── Parallels ────────────────────────────────────────────────────────────────

BASE_PARALLELS = [
    {"name": "Refractor", "print_run": None},
    {"name": "Purple Refractor", "print_run": 299},
    {"name": "Blue Refractor", "print_run": 199},
    {"name": "Green Refractor", "print_run": 99},
    {"name": "Gold Refractor", "print_run": 50},
    {"name": "Orange Refractor", "print_run": 25},
    {"name": "Red Refractor", "print_run": 5},
    {"name": "SuperFractor", "print_run": 1},
]

AUTO_PARALLELS = [
    {"name": "Refractor", "print_run": None},
    {"name": "Purple Refractor", "print_run": 299},
    {"name": "Blue Refractor", "print_run": 199},
    {"name": "Green Refractor", "print_run": 99},
    {"name": "Gold Refractor", "print_run": 50},
    {"name": "Orange Refractor", "print_run": 25},
    {"name": "Red Refractor", "print_run": 5},
    {"name": "SuperFractor", "print_run": 1},
]

INSERT_PARALLELS = [
    {"name": "Refractor", "print_run": None},
    {"name": "Purple Refractor", "print_run": 299},
    {"name": "Blue Refractor", "print_run": 199},
    {"name": "Green Refractor", "print_run": 99},
    {"name": "Gold Refractor", "print_run": 50},
    {"name": "Orange Refractor", "print_run": 25},
    {"name": "Red Refractor", "print_run": 5},
    {"name": "SuperFractor", "print_run": 1},
]

# ── Data ─────────────────────────────────────────────────────────────────────

BASE_SET = [
    (1, "Shon Abaev", "East"), (2, "Darius Adams", "East"), (3, "Nate Ament", "East"),
    (4, "Jalen Haralson", "East"), (5, "Zai Harwell", "East"), (6, "Eric Reibe", "East"),
    (7, "AJ Dybantsa", "West"), (8, "Brayden Burries", "West"), (9, "Mikel Brown Jr.", "West"),
    (10, "Caleb Wilson", "West"), (11, "Chris Cenac Jr.", "West"), (12, "Darryn Peterson", "West"),
    (13, "Koa Peat", "West"), (14, "Nikola Bundalo", "West"), (15, "Tounde Yessoufou", "West"),
    (16, "Aaliyah Crump", "East"), (17, "Agot Makeer", "East"), (18, "Deniya Prawl", "East"),
    (19, "Hailee Swain", "East"), (20, "Jaida Civil", "East"), (21, "Jaliya Davis", "East"),
    (22, "Kaelyn Carroll", "East"), (23, "Lara Somfai", "East"), (24, "Leah Macy", "East"),
    (25, "Mia Pauldo", "East"), (26, "Nyla Brooks", "East"), (27, "ZaKiyah Johnson", "East"),
    (28, "Aaliyah Chavez", "West"), (29, "Addie Deal", "West"), (30, "Alexandra Eschmeyer", "West"),
    (31, "Aliyahna Morris", "West"), (32, "Ayla McDowell", "West"), (33, "Brynn McGaughy", "West"),
    (34, "Darriana Alexander", "West"), (35, "Emilee Skinner", "West"), (36, "Grace Knox", "West"),
    (37, "Jordan Speiser", "West"), (38, "Sienna Betts", "West"),
    (39, "Shon Abaev", "East"), (40, "Darius Adams", "East"), (41, "Nate Ament", "East"),
    (42, "Jalen Haralson", "East"), (43, "Zai Harwell", "East"), (44, "Eric Reibe", "East"),
    (45, "AJ Dybantsa", "West"), (46, "Brayden Burries", "West"), (47, "Mikel Brown Jr.", "West"),
    (48, "Caleb Wilson", "West"), (49, "Chris Cenac Jr.", "West"), (50, "Darryn Peterson", "West"),
    (51, "Koa Peat", "West"), (52, "Nikola Bundalo", "West"), (53, "Tounde Yessoufou", "West"),
    (54, "Aaliyah Crump", "East"), (55, "Agot Makeer", "East"), (56, "Deniya Prawl", "East"),
    (57, "Hailee Swain", "East"), (58, "Jaida Civil", "East"), (59, "Jaliya Davis", "East"),
    (60, "Kaelyn Carroll", "East"), (61, "Lara Somfai", "East"), (62, "Leah Macy", "East"),
    (63, "Mia Pauldo", "East"), (64, "Nyla Brooks", "East"), (65, "ZaKiyah Johnson", "East"),
    (66, "Aaliyah Chavez", "West"), (67, "Addie Deal", "West"), (68, "Alexandra Eschmeyer", "West"),
    (69, "Aliyahna Morris", "West"), (70, "Ayla McDowell", "West"), (71, "Brynn McGaughy", "West"),
    (72, "Darriana Alexander", "West"), (73, "Emilee Skinner", "West"), (74, "Grace Knox", "West"),
    (75, "Jordan Speiser", "West"), (76, "Sienna Betts", "West"),
    (77, "Bronny James", "West"), (78, "Jayson Tatum", "East"), (79, "Al Harrington", "East"),
    (80, "Tyrese Maxey", "West"), (81, "Rip Hamilton", "West"), (82, "Amar'e Stoudemire", "East"),
    (83, "Juwan Howard", "West"), (84, "JuJu Watkins", "West"), (85, "Anthony Black", "West"),
    (86, "Dwight Howard", "East"), (87, "Eric Gordon", "West"), (88, "Ron Holland II", "West"),
    (89, "Jarace Walker", "East"), (90, "Quentin Grimes", "West"), (91, "Marcus Smart", "West"),
    (92, "Immanuel Quickley", "East"), (93, "Dereck Lively II", "East"), (94, "Cole Anthony", "East"),
    (95, "Jaren Jackson Jr.", "West"), (96, "Kel'el Ware", "West"), (97, "Gradey Dick", "West"),
    (98, "LeBron James", "East"), (99, "Amari Bailey", "West"), (100, "Myles Turner", "East"),
]

BILLBOARD_INK = [
    ("BI-AC", "Aaliyah Chavez", "West"), ("BI-ACR", "Aaliyah Crump", "East"),
    ("BI-AD", "AJ Dybantsa", "West"), ("BI-ADE", "Addie Deal", "West"),
    ("BI-AE", "Alexandra Eschmeyer", "West"), ("BI-AM", "Agot Makeer", "East"),
    ("BI-AMD", "Ayla McDowell", "West"), ("BI-AMO", "Aliyahna Morris", "West"),
    ("BI-BB", "Brayden Burries", "West"), ("BI-BM", "Brynn McGaughy", "West"),
    ("BI-CC", "Chris Cenac Jr.", "West"), ("BI-CW", "Caleb Wilson", "West"),
    ("BI-DA", "Darius Adams", "East"), ("BI-DAL", "Darriana Alexander", "West"),
    ("BI-DP", "Darryn Peterson", "West"), ("BI-DPR", "Deniya Prawl", "East"),
    ("BI-ER", "Eric Reibe", "East"), ("BI-ES", "Emilee Skinner", "West"),
    ("BI-GK", "Grace Knox", "West"), ("BI-HS", "Hailee Swain", "East"),
    ("BI-JC", "Jaida Civil", "East"), ("BI-JD", "Jaliya Davis", "East"),
    ("BI-JH", "Jalen Haralson", "East"), ("BI-JS", "Jordan Speiser", "West"),
    ("BI-KC", "Kaelyn Carroll", "East"), ("BI-KP", "Koa Peat", "West"),
    ("BI-LM", "Leah Macy", "East"), ("BI-LS", "Lara Somfai", "East"),
    ("BI-MB", "Mikel Brown Jr.", "West"), ("BI-MP", "Mia Pauldo", "East"),
    ("BI-NA", "Nate Ament", "East"), ("BI-NB", "Nikola Bundalo", "West"),
    ("BI-NBR", "Nyla Brooks", "East"), ("BI-SA", "Shon Abaev", "East"),
    ("BI-SB", "Sienna Betts", "West"), ("BI-TY", "Tounde Yessoufou", "West"),
    ("BI-ZH", "Zai Harwell", "East"), ("BI-ZJ", "ZaKiyah Johnson", "East"),
]

LEGENDS_AUTOGRAPHS = [
    ("LA-AB", "Amari Bailey", "West"), ("LA-CA", "Cole Anthony", "East"),
    ("LA-DH", "Dwight Howard", "East"), ("LA-DL", "Dereck Lively II", "East"),
    ("LA-EG", "Eric Gordon", "West"), ("LA-IQ", "Immanuel Quickley", "East"),
    ("LA-JH", "Juwan Howard", "West"), ("LA-JJ", "Jaren Jackson Jr.", "West"),
    ("LA-JT", "Jayson Tatum", "East"), ("LA-JW", "JuJu Watkins", "West"),
    ("LA-KW", "Kel'el Ware", "West"), ("LA-LJ", "LeBron James", "East"),
    ("LA-MS", "Marcus Smart", "West"), ("LA-MT", "Myles Turner", "East"),
    ("LA-QG", "Quentin Grimes", "West"), ("LA-RH", "Rip Hamilton", "West"),
    ("LA-RHO", "Ron Holland II", "West"), ("LA-TM", "Tyrese Maxey", "West"),
]

WINNING_TAGS = [
    ("WT-AC", "Aaliyah Chavez", "West"), ("WT-ACR", "Aaliyah Crump", "East"),
    ("WT-AD", "AJ Dybantsa", "West"), ("WT-ADE", "Addie Deal", "West"),
    ("WT-AE", "Alexandra Eschmeyer", "West"), ("WT-AM", "Agot Makeer", "East"),
    ("WT-AMD", "Ayla McDowell", "West"), ("WT-AMO", "Aliyahna Morris", "West"),
    ("WT-BB", "Brayden Burries", "West"), ("WT-BM", "Brynn McGaughy", "West"),
    ("WT-CC", "Chris Cenac Jr.", "West"), ("WT-CW", "Caleb Wilson", "West"),
    ("WT-DA", "Darius Adams", "East"), ("WT-DAL", "Darriana Alexander", "West"),
    ("WT-DP", "Darryn Peterson", "West"), ("WT-DPR", "Deniya Prawl", "East"),
    ("WT-ER", "Eric Reibe", "East"), ("WT-ES", "Emilee Skinner", "West"),
    ("WT-GK", "Grace Knox", "West"), ("WT-HS", "Hailee Swain", "East"),
    ("WT-JC", "Jaida Civil", "East"), ("WT-JD", "Jaliya Davis", "East"),
    ("WT-JH", "Jalen Haralson", "East"), ("WT-JS", "Jordan Speiser", "West"),
    ("WT-KC", "Kaelyn Carroll", "East"), ("WT-KP", "Koa Peat", "West"),
    ("WT-LM", "Leah Macy", "East"), ("WT-LS", "Lara Somfai", "East"),
    ("WT-MB", "Mikel Brown Jr.", "West"), ("WT-MP", "Mia Pauldo", "East"),
    ("WT-NA", "Nate Ament", "East"), ("WT-NB", "Nikola Bundalo", "West"),
    ("WT-NBR", "Nyla Brooks", "East"), ("WT-SA", "Shon Abaev", "East"),
    ("WT-SB", "Sienna Betts", "West"), ("WT-TY", "Tounde Yessoufou", "West"),
    ("WT-ZH", "Zai Harwell", "East"), ("WT-ZJ", "ZaKiyah Johnson", "East"),
]

EVENT_AUTOGRAPHS = [
    ("EA-AC", "Aaliyah Crump", "East"), ("EA-ACH", "Aaliyah Chavez", "West"),
    ("EA-AD", "AJ Dybantsa", "West"), ("EA-ADE", "Addie Deal", "West"),
    ("EA-AE", "Alexandra Eschmeyer", "West"), ("EA-AM", "Agot Makeer", "East"),
    ("EA-AMD", "Ayla McDowell", "West"), ("EA-AMO", "Aliyahna Morris", "West"),
    ("EA-BB", "Brayden Burries", "West"), ("EA-BMG", "Brynn McGaughy", "West"),
    ("EA-CC", "Chris Cenac Jr.", "West"), ("EA-CW", "Caleb Wilson", "West"),
    ("EA-DA", "Darius Adams", "East"), ("EA-DAL", "Darriana Alexander", "West"),
    ("EA-DP", "Darryn Peterson", "West"), ("EA-DPR", "Deniya Prawl", "East"),
    ("EA-ER", "Eric Reibe", "East"), ("EA-ES", "Emilee Skinner", "West"),
    ("EA-GK", "Grace Knox", "West"), ("EA-HS", "Hailee Swain", "East"),
    ("EA-JC", "Jaida Civil", "East"), ("EA-JD", "Jaliya Davis", "East"),
    ("EA-JH", "Jalen Haralson", "East"), ("EA-JS", "Jordan Speiser", "West"),
    ("EA-KC", "Kaelyn Carroll", "East"), ("EA-KP", "Koa Peat", "West"),
    ("EA-LM", "Leah Macy", "East"), ("EA-LS", "Lara Somfai", "East"),
    ("EA-MB", "Mikel Brown Jr.", "West"), ("EA-MP", "Mia Pauldo", "East"),
    ("EA-NA", "Nate Ament", "East"), ("EA-NB", "Nikola Bundalo", "West"),
    ("EA-NBR", "Nyla Brooks", "East"), ("EA-SA", "Shon Abaev", "East"),
    ("EA-SB", "Sienna Betts", "West"), ("EA-TY", "Tounde Yessoufou", "West"),
    ("EA-ZH", "Zai Harwell", "East"), ("EA-ZJ", "ZaKiyah Johnson", "East"),
]

GOLDEN_PATCH_AUTOGRAPHS = [
    ("GP-AC", "Aaliyah Chavez", "West"), ("GP-ACR", "Aaliyah Crump", "East"),
    ("GP-AD", "AJ Dybantsa", "West"), ("GP-ADE", "Addie Deal", "West"),
    ("GP-AE", "Alexandra Eschmeyer", "West"), ("GP-AM", "Agot Makeer", "East"),
    ("GP-AMD", "Ayla McDowell", "West"), ("GP-AMO", "Aliyahna Morris", "West"),
    ("GP-BB", "Brayden Burries", "West"), ("GP-BM", "Brynn McGaughy", "West"),
    ("GP-CC", "Chris Cenac Jr.", "West"), ("GP-CW", "Caleb Wilson", "West"),
    ("GP-DA", "Darius Adams", "East"), ("GP-DAL", "Darriana Alexander", "West"),
    ("GP-DP", "Darryn Peterson", "West"), ("GP-DPR", "Deniya Prawl", "East"),
    ("GP-ER", "Eric Reibe", "East"), ("GP-ES", "Emilee Skinner", "West"),
    ("GP-GK", "Grace Knox", "West"), ("GP-HS", "Hailee Swain", "East"),
    ("GP-JC", "Jaida Civil", "East"), ("GP-JD", "Jaliya Davis", "East"),
    ("GP-JH", "Jalen Haralson", "East"), ("GP-JS", "Jordan Speiser", "West"),
    ("GP-KC", "Kaelyn Carroll", "East"), ("GP-KP", "Koa Peat", "West"),
    ("GP-LM", "Leah Macy", "East"), ("GP-LS", "Lara Somfai", "East"),
    ("GP-MB", "Mikel Brown Jr.", "West"), ("GP-MP", "Mia Pauldo", "East"),
    ("GP-NA", "Nate Ament", "East"), ("GP-NB", "Nikola Bundalo", "West"),
    ("GP-NBR", "Nyla Brooks", "East"), ("GP-SA", "Shon Abaev", "East"),
    ("GP-SB", "Sienna Betts", "West"), ("GP-TY", "Tounde Yessoufou", "West"),
    ("GP-ZH", "Zai Harwell", "East"), ("GP-ZJ", "ZaKiyah Johnson", "East"),
]

HIGH_RISES = [
    ("HR-1", "Shon Abaev", "East"), ("HR-2", "Darius Adams", "East"),
    ("HR-3", "Nate Ament", "East"), ("HR-4", "Jalen Haralson", "East"),
    ("HR-5", "Zai Harwell", "East"), ("HR-6", "Eric Reibe", "East"),
    ("HR-7", "AJ Dybantsa", "West"), ("HR-8", "Brayden Burries", "West"),
    ("HR-9", "Mikel Brown Jr.", "West"), ("HR-10", "Caleb Wilson", "West"),
    ("HR-11", "Chris Cenac Jr.", "West"), ("HR-12", "Darryn Peterson", "West"),
    ("HR-13", "Koa Peat", "West"), ("HR-14", "Nikola Bundalo", "West"),
    ("HR-15", "Tounde Yessoufou", "West"), ("HR-16", "Aaliyah Crump", "East"),
    ("HR-17", "Agot Makeer", "East"), ("HR-18", "Deniya Prawl", "East"),
    ("HR-19", "Hailee Swain", "East"), ("HR-20", "Jaida Civil", "East"),
    ("HR-21", "Jaliya Davis", "East"), ("HR-22", "Kaelyn Carroll", "East"),
    ("HR-23", "Lara Somfai", "East"), ("HR-24", "Leah Macy", "East"),
    ("HR-25", "Mia Pauldo", "East"), ("HR-26", "Nyla Brooks", "East"),
    ("HR-27", "ZaKiyah Johnson", "East"), ("HR-28", "Aaliyah Chavez", "West"),
    ("HR-29", "Addie Deal", "West"), ("HR-30", "Alexandra Eschmeyer", "West"),
    ("HR-31", "Aliyahna Morris", "West"), ("HR-32", "Ayla McDowell", "West"),
    ("HR-33", "Brynn McGaughy", "West"), ("HR-34", "Darriana Alexander", "West"),
    ("HR-35", "Emilee Skinner", "West"), ("HR-36", "Grace Knox", "West"),
    ("HR-37", "Jordan Speiser", "West"), ("HR-38", "Sienna Betts", "West"),
]

TOP_RECRUITS = [
    ("TP-1", "Shon Abaev", "East"), ("TP-2", "Darius Adams", "East"),
    ("TP-3", "Nate Ament", "East"), ("TP-4", "Jalen Haralson", "East"),
    ("TP-5", "Zai Harwell", "East"), ("TP-6", "Eric Reibe", "East"),
    ("TP-7", "AJ Dybantsa", "West"), ("TP-8", "Brayden Burries", "West"),
    ("TP-9", "Mikel Brown Jr.", "West"), ("TP-10", "Caleb Wilson", "West"),
    ("TP-11", "Chris Cenac Jr.", "West"), ("TP-12", "Darryn Peterson", "West"),
    ("TP-13", "Koa Peat", "West"), ("TP-14", "Nikola Bundalo", "West"),
    ("TP-15", "Tounde Yessoufou", "West"), ("TP-16", "Aaliyah Crump", "East"),
    ("TP-17", "Agot Makeer", "East"), ("TP-18", "Deniya Prawl", "East"),
    ("TP-19", "Hailee Swain", "East"), ("TP-20", "Jaida Civil", "East"),
    ("TP-21", "Jaliya Davis", "East"), ("TP-22", "Kaelyn Carroll", "East"),
    ("TP-23", "Lara Somfai", "East"), ("TP-24", "Leah Macy", "East"),
    ("TP-25", "Mia Pauldo", "East"), ("TP-26", "Nyla Brooks", "East"),
    ("TP-27", "ZaKiyah Johnson", "East"), ("TP-28", "Aaliyah Chavez", "West"),
    ("TP-29", "Addie Deal", "West"), ("TP-30", "Alexandra Eschmeyer", "West"),
    ("TP-31", "Aliyahna Morris", "West"), ("TP-32", "Ayla McDowell", "West"),
]

PROSPECT_PATHS = [
    ("PP-1", "Shon Abaev", "East"), ("PP-2", "Darius Adams", "East"),
    ("PP-3", "Nate Ament", "East"), ("PP-4", "Jalen Haralson", "East"),
    ("PP-5", "Zai Harwell", "East"), ("PP-6", "Eric Reibe", "East"),
    ("PP-7", "AJ Dybantsa", "West"), ("PP-8", "Brayden Burries", "West"),
    ("PP-9", "Mikel Brown Jr.", "West"), ("PP-10", "Caleb Wilson", "West"),
    ("PP-11", "Chris Cenac Jr.", "West"), ("PP-12", "Darryn Peterson", "West"),
    ("PP-13", "Koa Peat", "West"), ("PP-14", "Leah Macy", "East"),
    ("PP-15", "Mia Pauldo", "East"), ("PP-16", "Nyla Brooks", "East"),
    ("PP-17", "ZaKiyah Johnson", "East"), ("PP-18", "Aaliyah Chavez", "West"),
    ("PP-19", "Addie Deal", "West"), ("PP-20", "Alexandra Eschmeyer", "West"),
]

HYPE_TO_LEGACY = [
    ("HL-1", "AJ Dybantsa", "West"), ("HL-2", "Nate Ament", "East"),
    ("HL-3", "Koa Peat", "West"), ("HL-4", "Darryn Peterson", "West"),
    ("HL-5", "Caleb Wilson", "West"), ("HL-6", "Aaliyah Chavez", "West"),
    ("HL-7", "Chris Cenac Jr.", "West"), ("HL-8", "Sienna Betts", "West"),
    ("HL-9", "Emilee Skinner", "West"), ("HL-10", "Aaliyah Crump", "East"),
]

ALL_AMERICAN_DRIP = [
    ("AA-1", "AJ Dybantsa", "West"), ("AA-2", "Nate Ament", "East"),
    ("AA-3", "Koa Peat", "West"), ("AA-4", "Darryn Peterson", "West"),
    ("AA-5", "Caleb Wilson", "West"), ("AA-6", "Aaliyah Chavez", "West"),
    ("AA-7", "Chris Cenac Jr.", "West"), ("AA-8", "Sienna Betts", "West"),
    ("AA-9", "Emilee Skinner", "West"), ("AA-10", "Aaliyah Crump", "East"),
]

CONCRETE_CANVAS = [
    ("CC-1", "AJ Dybantsa", "West"), ("CC-2", "Nate Ament", "East"),
    ("CC-3", "Koa Peat", "West"), ("CC-4", "Darryn Peterson", "West"),
    ("CC-5", "Caleb Wilson", "West"), ("CC-6", "Aaliyah Chavez", "West"),
    ("CC-7", "Chris Cenac Jr.", "West"), ("CC-8", "Sienna Betts", "West"),
    ("CC-9", "Emilee Skinner", "West"), ("CC-10", "Aaliyah Crump", "East"),
    ("CC-11", "Mikel Brown Jr.", "West"), ("CC-12", "Tounde Yessoufou", "West"),
    ("CC-13", "Brayden Burries", "West"), ("CC-14", "Jalen Haralson", "East"),
    ("CC-15", "Darius Adams", "East"), ("CC-16", "Shon Abaev", "East"),
    ("CC-17", "Leah Macy", "East"), ("CC-18", "Grace Knox", "West"),
    ("CC-19", "ZaKiyah Johnson", "East"), ("CC-20", "Nyla Brooks", "East"),
]

# ── Build sections (seed.ts format) ──────────────────────────────────────────

def build_section(name: str, cards: list, parallels: list) -> dict:
    return {
        "insert_set": name,
        "parallels": parallels,
        "cards": [
            {"card_number": str(num), "player": fix_name(n), "team": t, "is_rookie": False, "subset": None}
            for num, n, t in cards
        ],
    }

SECTIONS_DEF = [
    ("Base Set", BASE_SET, BASE_PARALLELS),
    ("Billboard Ink", BILLBOARD_INK, AUTO_PARALLELS),
    ("Legends Autographs", LEGENDS_AUTOGRAPHS, AUTO_PARALLELS),
    ("Winning Tags", WINNING_TAGS, AUTO_PARALLELS),
    ("Event Autographs", EVENT_AUTOGRAPHS, AUTO_PARALLELS),
    ("Golden Patch Autographs", GOLDEN_PATCH_AUTOGRAPHS, AUTO_PARALLELS),
    ("High Rises", HIGH_RISES, INSERT_PARALLELS),
    ("Top Recruits", TOP_RECRUITS, INSERT_PARALLELS),
    ("Prospect Paths", PROSPECT_PATHS, INSERT_PARALLELS),
    ("Hype To Legacy", HYPE_TO_LEGACY, INSERT_PARALLELS),
    ("All-American Drip", ALL_AMERICAN_DRIP, INSERT_PARALLELS),
    ("Concrete Canvas", CONCRETE_CANVAS, INSERT_PARALLELS),
]

sections = [build_section(name, cards, pars) for name, cards, pars in SECTIONS_DEF]

# ── Build players (seed.ts format) ──────────────────────────────────────────

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

# Compute stats and finalize
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

# ── Output ───────────────────────────────────────────────────────────────────

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
auto_names = {"Billboard Ink", "Legends Autographs", "Winning Tags", "Event Autographs", "Golden Patch Autographs"}
auto_cards = sum(len(s["cards"]) for s in sections if s["insert_set"] in auto_names)
insert_cards = sum(len(s["cards"]) for s in sections if s["insert_set"] not in auto_names and s["insert_set"] != "Base Set")

print(f"Set: {SET_NAME}")
print(f"Sections: {len(sections)}")
print(f"Total cards: {total_cards}")
print(f"Unique players: {unique_players}")
print(f"Base set: {len(BASE_SET)} cards")
print(f"Autograph sets: {len(auto_names)} ({auto_cards} cards)")
print(f"Insert sets: {len(sections) - len(auto_names) - 1} ({insert_cards} cards)")

out_path = "scripts/mcdonalds_allamerican_2025_parsed.json"
with open(out_path, "w") as f:
    json.dump(output, f, indent=2)
print(f"\nWrote {out_path}")
