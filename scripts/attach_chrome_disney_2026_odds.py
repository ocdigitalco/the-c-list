#!/usr/bin/env python3
"""
Attach pack odds + numbered parallels + 7-format box configs to the EXISTING
2026 Topps Chrome Disney set (slug 2026-topps-chrome-disney, set id 846).

ATTACH ONLY — never creates a subset. Any odds/parallel whose subset has no
existing DB insert_set is skipped and reported.

Odds values stored as "1:N" strings (commas stripped); parser handles them.
Parallel DB names == odds-key suffix so the calculator joins via
`{prefix} {parallel.name}` (see src/lib/athleteOdds.ts).
"""
import sqlite3, json, sys, os

DB = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
SET_ID = 846

FORMATS = ["Hobby", "Value Box CEE", "Value Box EA", "Value Box SE",
           "Mega Box CEE", "Mega Box EA", "Mega Box SE"]

# ── Box configs: 7 keys matching the 7 pack_odds format keys exactly ──
BOX_CONFIG = {
    "Hobby":         {"cards_per_pack": 6, "packs_per_box": 12, "boxes_per_case": 20, "notes": "Per box: TBA"},
    "Value Box CEE": {"cards_per_pack": 4, "packs_per_box": 8,  "boxes_per_case": None, "notes": "Per box: 2 RayWave Parallels"},
    "Value Box EA":  {"cards_per_pack": 4, "packs_per_box": 8,  "boxes_per_case": None, "notes": "Per box: 2 RayWave Parallels"},
    "Value Box SE":  {"cards_per_pack": 4, "packs_per_box": 8,  "boxes_per_case": None, "notes": "Per box: 2 RayWave Parallels"},
    "Mega Box CEE":  {"cards_per_pack": 7, "packs_per_box": 8,  "boxes_per_case": None, "notes": "Per box: 4 X-Fractors"},
    "Mega Box EA":   {"cards_per_pack": 7, "packs_per_box": 8,  "boxes_per_case": None, "notes": "Per box: 4 X-Fractors"},
    "Mega Box SE":   {"cards_per_pack": 7, "packs_per_box": 8,  "boxes_per_case": None, "notes": "Per box: 4 X-Fractors"},
}

# ── Print-run resolution ──
# Subset-specific overrides take priority (None = unnumbered base-tier chrome).
PR_OVERRIDE = {
    (1645, "Raywave"): None,            # base Value-excl base-tier (NOT the /5 art Raywave)
    (1646, "Base Speckle"): None,       # image variations base
    (1649, "Base Speckle"): 20,         # Scorched
    (1656, "Base Speckle"): 20,         # Toy Story 5
    (1652, "Sparkle Base"): 20,         # Golden Age Posters
    (1650, "Base Speckle"): 100,        # Super Strength Chrome
    (1663, "Base Speckle"): None,       # Dumbo
    (1664, "Base Speckle Refractor"): None,  # Winnie
    (1668, "Base Sparkle"): None,       # Lilo
    (1670, "Base Sparkle"): None,       # Heart of Te Fiti
    (1669, "Base Sparkle"): None,       # The Rose
    (1667, "Base"): None,               # Ukiyo-e base tier
    (1665, "Raywave"): 5, (1666, "Raywave"): 5, (1667, "Raywave"): 5,  # art shadowboxes
}
UNIV = {
    "Magenta Refractor": 399, "Pink Refractor": 250, "Yellow and Green Raywave": 225,
    "Aqua Refractor": 199, "Purple and Light Green Shimmer Refractor": 175, "Blue Refractor": 150,
    "Dark Blue and Light Blue Lava": 125, "101 Dalmatians Black and White Shimmer": 101,
    "Green Refractor": 99, "Purple Refractor": 75, "Gold Refractor": 50, "Pearl Refractor": 30,
    "Mickey Mouse Red and Black Refractor": 28, "Mickey Mouse Red and Black": 28,
    "Orange Refractor": 25, "Black Refractor": 10, "Red Refractor": 5, "Superfractor": 1,
    "Pink Mini Diamond": 250, "Aqua Mini Diamond": 199, "Blue Mini Diamond": 150, "Green Mini Diamond": 99,
    "Aqua Wave": 199, "Blue Wave": 150, "Green Wave": 99, "Gold Wave": 50, "Red Wave": 5,
    "When You Wish Upon a Star Refractor": 15,
    "Orange Speckle": 25, "Black Speckle": 10, "Red Speckle": 5,
    "Kaleidoscope": 25, "Shimmer": 10, "Raywave": 5,
    "Gold": 50, "Orange": 25, "Green": 10, "Red": 5, "Black": 1,  # TRON TEK bare colours
    "Refractor": None, "Prism Refractor": None, "X-Fractor": None,
}

def print_run(sid, suffix):
    if (sid, suffix) in PR_OVERRIDE:
        return PR_OVERRIDE[(sid, suffix)]
    return UNIV.get(suffix, None)

def excl_from_cols(cols):
    """Derive format-exclusivity tag from which of the 7 columns have odds."""
    has = [c != "-" for c in cols]
    hobby = has[0]; value = any(has[1:4]); mega = any(has[4:7])
    if hobby and not value and not mega: return "Hobby"
    if value and mega and not hobby:     return "Retail"
    if value and not mega and not hobby: return "Value"
    if mega and not value and not hobby: return "Mega"
    return None

def v(s):
    """Strip commas; '-' -> None (omit)."""
    return None if s == "-" else s.replace(",", "")

# ── Matched subsets: id, odds-key prefix, base row (or None), parallels ──
# Each parallel = (odds-suffix name, [7 raw values]).  "-" = absent for that format.
A = "1:"  # brevity not used; values written in full below
SUBSETS = [
 # id, prefix, base(7 or None), [ (suffix,[7]) ... ]
 (1645, "Base", ["1:1","1:1","1:1","1:1","1:1","1:1","1:1"], [
   ("Refractor", ["1:2","1:4","1:4","1:4","1:3","1:3","1:3"]),
   ("Magenta Refractor", ["1:21","1:124","1:124","1:124","1:69","1:68","1:68"]),
   ("Pink Refractor", ["1:33","1:198","1:198","1:198","1:109","1:109","1:109"]),
   ("Yellow and Green Raywave", ["1:37","1:220","1:220","1:220","1:121","1:121","1:121"]),
   ("Aqua Refractor", ["1:42","1:249","1:249","1:249","1:138","1:138","1:138"]),
   ("Purple and Light Green Shimmer Refractor", ["1:47","1:284","1:284","1:284","1:157","1:157","1:157"]),
   ("Blue Refractor", ["1:55","1:329","1:329","1:329","1:181","1:181","1:181"]),
   ("Dark Blue and Light Blue Lava", ["1:66","1:395","1:395","1:395","1:218","1:217","1:218"]),
   ("101 Dalmatians Black and White Shimmer", ["1:81","1:488","1:488","1:488","1:269","1:269","1:269"]),
   ("Green Refractor", ["1:83","1:498","1:498","1:498","1:274","1:274","1:274"]),
   ("Purple Refractor", ["1:109","1:657","1:658","1:657","1:363","1:362","1:362"]),
   ("Gold Refractor", ["1:163","1:986","1:986","1:986","1:543","1:543","1:543"]),
   ("Pearl Refractor", ["1:266","1:1,609","1:1,609","1:1,610","1:888","1:885","1:887"]),
   ("Mickey Mouse Red and Black Refractor", ["1:291","1:1,761","1:1,762","1:1,760","1:969","1:970","1:970"]),
   ("Orange Refractor", ["1:326","1:1,971","1:1,967","1:1,971","1:1,085","1:1,085","1:1,087"]),
   ("Black Refractor", ["1:814","1:4,909","1:4,934","1:4,931","1:2,712","1:2,705","1:2,719"]),
   ("Red Refractor", ["1:1,628","1:9,817","1:9,867","1:9,895","1:5,423","1:5,486","1:5,413"]),
   ("Superfractor", ["1:6,686","1:64,356","1:98,667","1:54,235","1:34,858","1:64,000","1:31,622"]),
   ("Prism Refractor", ["1:3","-","-","-","-","-","-"]),
   ("Aqua Wave", ["1:21","-","-","-","-","-","-"]),
   ("Blue Wave", ["1:28","-","-","-","-","-","-"]),
   ("Green Wave", ["1:42","-","-","-","-","-","-"]),
   ("Gold Wave", ["1:83","-","-","-","-","-","-"]),
   ("When You Wish Upon a Star Refractor", ["1:283","-","-","-","-","-","-"]),
   ("Red Wave", ["1:831","-","-","-","-","-","-"]),
   ("X-Fractor", ["-","-","-","-","1:2","1:2","1:2"]),
   ("Raywave", ["-","1:4","1:4","1:4","-","-","-"]),
   ("Pink Mini Diamond", ["-","1:92","1:92","1:92","1:53","1:53","1:53"]),
   ("Aqua Mini Diamond", ["-","1:115","1:115","1:115","1:66","1:66","1:66"]),
   ("Blue Mini Diamond", ["-","1:153","1:153","1:153","1:87","1:87","1:87"]),
   ("Green Mini Diamond", ["-","1:231","1:231","1:231","1:132","1:132","1:132"]),
 ]),
 (1661, "Darkwing Duck 35th Anniversary", ["1:10","1:10","1:10","1:10","1:10","1:10","1:10"], [
   ("Orange Refractor", ["1:6,524","1:38,614","1:39,467","1:39,577","1:22,182","1:21,334","1:21,458"]),
   ("Black Refractor", ["1:16,509","1:96,534","1:98,667","1:97,622","1:61,000","1:48,000","1:54,619"]),
   ("Red Refractor", ["1:32,356","1:193,067","1:197,334","1:209,189","1:122,000","1:96,000","1:100,134"]),
   ("Superfractor", ["-","-","-","-","-","-","-"]),
 ]),
 (1662, "Alice in Wonderland 75th Anniversary", ["1:10","1:10","1:10","1:10","1:10","1:10","1:10"], [
   ("Orange Refractor", ["1:6,524","1:38,614","1:39,467","1:39,577","1:22,182","1:21,334","1:21,458"]),
   ("Black Refractor", ["1:16,509","1:96,534","1:98,667","1:97,622","1:61,000","1:48,000","1:54,619"]),
   ("Red Refractor", ["1:32,356","1:193,067","1:197,334","1:209,189","1:122,000","1:96,000","1:100,134"]),
   ("Superfractor", ["-","-","-","-","-","-","-"]),
 ]),
 (1659, "Cars 20th Anniversary", ["1:10","1:10","1:10","1:10","1:10","1:10","1:10"], [
   ("Orange Refractor", ["1:6,524","1:38,614","1:39,467","1:39,577","1:22,182","1:21,334","1:21,458"]),
   ("Black Refractor", ["1:16,509","1:96,534","1:98,667","1:97,622","1:61,000","1:48,000","1:54,619"]),
   ("Red Refractor", ["1:32,356","1:193,067","1:197,334","1:209,189","1:122,000","1:96,000","1:100,134"]),
   ("Superfractor", ["-","-","-","-","-","-","-"]),
 ]),
 (1660, "Monsters, Inc. 25th Anniversary", ["1:7","1:7","1:7","1:7","1:7","1:7","1:7"], [
   ("Orange Refractor", ["1:4,349","1:26,328","1:26,910","1:26,149","1:14,353","1:14,770","1:14,305"]),
   ("Black Refractor", ["1:10,932","1:64,356","1:65,778","1:66,560","1:34,858","1:38,400","1:35,342"]),
   ("Red Refractor", ["1:21,863","1:144,800","1:148,000","1:133,120","1:81,334","1:64,000","1:75,100"]),
   ("Superfractor", ["-","-","-","-","-","-","-"]),
 ]),
 (1654, "Disney Channel", ["1:5","1:5","1:5","1:5","1:5","1:5","1:5"], [
   ("Orange Refractor", ["1:3,262","1:19,973","1:19,734","1:19,789","1:11,091","1:10,667","1:10,924"]),
   ("Black Refractor", ["1:8,171","1:48,267","1:49,334","1:50,494","1:27,112","1:27,429","1:27,310"]),
   ("Red Refractor", ["1:16,509","1:96,534","1:98,667","1:97,622","1:61,000","1:48,000","1:54,619"]),
   ("Superfractor", ["1:80,890","1:579,200","1:592,000","1:488,107","1:244,000","1:192,000","1:300,400"]),
 ]),
 (1653, "Disney Ink and Paint", ["1:10","1:10","1:10","1:10","1:10","1:10","1:10"], [
   ("Mickey Mouse Red and Black Refractor", ["1:5,820","1:36,200","1:34,824","1:34,865","1:18,770","1:19,200","1:19,381"]),
   ("Orange Refractor", ["1:6,524","1:38,614","1:39,467","1:39,577","1:22,182","1:21,334","1:21,458"]),
   ("Black Refractor", ["1:16,509","1:96,534","1:98,667","1:97,622","1:61,000","1:48,000","1:54,619"]),
   ("Red Refractor", ["1:32,356","1:193,067","1:197,334","1:209,189","1:122,000","1:96,000","1:100,134"]),
   ("Superfractor", ["-","-","-","-","-","-","-"]),
 ]),
 (1648, "Future Stars", ["1:10","1:10","1:10","1:10","1:10","1:10","1:10"], [
   ("Mickey Mouse Red and Black Refractor", ["1:5,820","1:36,200","1:34,824","1:34,865","1:18,770","1:19,200","1:19,381"]),
   ("Orange Refractor", ["1:6,524","1:38,614","1:39,467","1:39,577","1:22,182","1:21,334","1:21,458"]),
   ("Black Refractor", ["1:16,509","1:96,534","1:98,667","1:97,622","1:61,000","1:48,000","1:54,619"]),
   ("Red Refractor", ["1:32,356","1:193,067","1:197,334","1:209,189","1:122,000","1:96,000","1:100,134"]),
   ("Superfractor", ["-","-","-","-","-","-","-"]),
 ]),
 (1647, "Iconic Moments", ["1:7","1:7","1:7","1:7","1:7","1:7","1:7"], [
   ("Mickey Mouse Red and Black Refractor", ["1:3,871","1:23,168","1:23,680","1:23,244","1:12,843","1:12,800","1:13,061"]),
   ("Orange Refractor", ["1:4,349","1:26,328","1:26,910","1:26,149","1:14,353","1:14,770","1:14,305"]),
   ("Black Refractor", ["1:10,932","1:64,356","1:65,778","1:66,560","1:34,858","1:38,400","1:35,342"]),
   ("Red Refractor", ["1:21,863","1:144,800","1:148,000","1:133,120","1:81,334","1:64,000","1:75,100"]),
   ("Superfractor", ["-","-","-","-","-","-","-"]),
 ]),
 (1646, "Base Card Image Variations", None, [
   ("Base Speckle", ["1:543","1:3,291","1:3,289","1:3,284","1:1,808","1:1,812","1:1,810"]),
   ("Mickey Mouse Red and Black", ["1:5,820","1:36,200","1:34,824","1:34,865","1:18,770","1:19,200","1:19,381"]),
   ("Orange Speckle", ["1:6,524","1:38,614","1:39,467","1:39,577","1:22,182","1:21,334","1:21,458"]),
   ("Black Speckle", ["1:16,509","1:96,534","1:98,667","1:97,622","1:61,000","1:48,000","1:54,619"]),
   ("Red Speckle", ["1:32,356","1:193,067","1:197,334","1:209,189","1:122,000","1:96,000","1:100,134"]),
   ("Superfractor", ["-","-","-","-","-","-","-"]),
 ]),
 (1651, "Helix", ["1:3,262","1:19,973","1:19,734","1:19,789","1:11,091","1:10,667","1:10,924"], [
   ("Superfractor", ["-","-","-","-","-","-","-"]),
 ]),
 (1677, "Mickey and Friends MLB Home Jersey Set", ["1:987","1:5,972","1:5,980","1:5,977","1:3,298","1:3,311","1:3,284"], [
   ("Black Refractor", ["1:5,429","1:32,178","1:32,889","1:33,280","1:18,770","1:17,455","1:18,207"]),
   ("Red Refractor", ["1:10,932","1:64,356","1:65,778","1:66,560","1:34,858","1:38,400","1:35,342"]),
   ("Superfractor", ["1:53,927","1:289,600","1:296,000","1:366,080","1:244,000","1:192,000","1:200,267"]),
 ]),
 (1649, "Scorched", None, [
   ("Base Speckle", ["1:16,509","1:96,534","1:98,667","1:97,622","1:61,000","1:48,000","1:54,619"]),
   ("Black Refractor", ["1:32,356","1:193,067","1:197,334","1:209,189","1:122,000","1:96,000","1:100,134"]),
   ("Red Refractor", ["1:67,408","1:289,600","1:296,000","1:366,080","1:244,000","1:192,000","1:200,267"]),
   ("Superfractor", ["-","-","-","-","-","-","-"]),
 ]),
 (1656, "Toy Story 5 First Edition", None, [
   ("Base Speckle", ["1:16,509","1:96,534","1:98,667","1:97,622","1:61,000","1:48,000","1:54,619"]),
   ("Black Refractor", ["1:32,356","1:193,067","1:197,334","1:209,189","1:122,000","1:96,000","1:100,134"]),
   ("Red Refractor", ["1:67,408","1:289,600","1:296,000","1:366,080","1:244,000","1:192,000","1:200,267"]),
   ("Superfractor", ["-","-","-","-","-","-","-"]),
 ]),
 (1652, "Golden Age Posters", None, [
   ("Sparkle Base", ["1:16,509","1:96,534","1:98,667","1:97,622","1:61,000","1:48,000","-"]),
   ("Black Refractor", ["1:32,356","1:193,067","1:197,334","1:209,189","1:122,000","1:96,000","-"]),
   ("Red Refractor", ["1:67,408","1:289,600","1:296,000","1:366,080","1:244,000","1:192,000","-"]),
   ("Superfractor", ["-","-","-","-","-","-","-"]),
 ]),
 (1655, "TRON TEK", ["1:96","1:320","1:320","1:320","1:160","1:160","1:160"], [
   ("Gold", ["1:3,262","1:19,973","1:19,734","1:19,789","1:11,091","1:10,667","1:10,924"]),
   ("Orange", ["1:6,524","1:38,614","1:39,467","1:39,577","1:22,182","1:21,334","1:21,458"]),
   ("Green", ["1:16,509","1:96,534","1:98,667","1:97,622","1:61,000","1:48,000","1:54,619"]),
   ("Red", ["1:32,356","1:193,067","1:197,334","1:209,189","1:122,000","1:96,000","1:100,134"]),
   ("Black", ["-","-","-","-","-","-","-"]),
 ]),
 (1665, "Art of Disney", ["1:99","1:400","1:400","1:400","1:200","1:200","1:200"], [
   ("Kaleidoscope", ["1:6,524","1:38,614","1:39,467","1:39,577","1:22,182","1:21,334","1:21,458"]),
   ("Shimmer", ["1:16,509","1:96,534","1:98,667","1:97,622","1:61,000","1:48,000","1:54,619"]),
   ("Raywave", ["1:32,356","1:193,067","1:197,334","1:209,189","1:122,000","1:96,000","1:100,134"]),
   ("Superfractor", ["-","-","-","-","-","-","-"]),
 ]),
 (1666, "Disney Reflections", ["1:511","1:1,600","1:1,600","1:1,600","1:880","1:880","1:880"], [
   ("Kaleidoscope", ["1:13,047","1:82,743","1:84,572","1:81,352","1:40,667","1:48,000","1:42,915"]),
   ("Shimmer", ["1:32,356","1:193,067","1:197,334","1:209,189","1:122,000","1:96,000","1:100,134"]),
   ("Raywave", ["1:67,408","1:289,600","1:296,000","1:366,080","1:244,000","1:192,000","1:200,267"]),
   ("Superfractor", ["-","-","-","-","-","-","-"]),
 ]),
 (1658, "High School Musical 20th Anniversary", ["-","1:8","1:8","1:8","-","-","-"], [
   ("Orange Refractor", ["-","1:9,984","1:9,984","1:9,984","-","-","-"]),
   ("Black Refractor", ["-","1:25,342","1:25,342","1:25,342","-","-","-"]),
   ("Red Refractor", ["-","1:51,677","1:51,677","1:51,677","-","-","-"]),
   ("Superfractor", ["-","1:329,440","1:329,440","1:329,440","-","-","-"]),
 ]),
 (1657, "Moana 10th Anniversary", ["-","-","-","-","1:4","1:4","1:4"], [
   ("Orange Refractor", ["-","-","-","-","1:4,320","1:4,320","1:4,320"]),
   ("Black Refractor", ["-","-","-","-","1:10,800","1:10,800","1:10,800"]),
   ("Red Refractor", ["-","-","-","-","1:22,060","1:22,060","1:22,060"]),
   ("Superfractor", ["-","-","-","-","1:148,115","1:148,115","1:148,115"]),
 ]),
 (1673, "Disney Chrome Facsimile Autographs", ["1:3,871","1:23,168","1:23,680","1:23,244","1:12,843","1:12,800","1:13,061"], [
   ("Black Refractor", ["1:10,932","1:64,356","1:65,778","1:66,560","1:34,858","1:38,400","1:35,342"]),
   ("Red Refractor", ["1:21,863","1:144,800","1:148,000","1:133,120","1:81,334","1:64,000","1:75,100"]),
   ("Superfractor", ["-","-","-","-","-","-","-"]),
 ]),
 (1674, "Disney Chrome Facsimile Dual Autographs", ["1:9,746","1:57,920","1:59,200","1:58,573","1:30,500","1:32,000","1:31,622"], [
   ("Black Refractor", ["1:26,964","1:144,800","1:148,000","1:162,703","1:81,334","1:192,000","1:100,134"]),
   ("Red Refractor", ["1:53,927","1:289,600","1:296,000","1:366,080","1:244,000","-","1:200,267"]),
   ("Superfractor", ["-","-","-","-","-","-","-"]),
 ]),
 (1675, "Disney Chrome Facsimile Triple Autographs", ["1:11,556","1:72,400","1:65,778","1:69,730","1:40,667","1:38,400","1:37,550"], [
   ("Black Refractor", ["1:32,356","1:193,067","1:197,334","1:209,189","1:122,000","1:96,000","1:100,134"]),
   ("Red Refractor", ["1:67,408","1:289,600","1:296,000","1:366,080","1:244,000","1:192,000","1:200,267"]),
   ("Superfractor", ["-","-","-","-","-","-","-"]),
 ]),
 (1676, "Disney Chrome Facsimile Quad Autographs", ["1:19,260","1:115,840","1:118,400","1:112,640","1:61,000","1:64,000","1:66,756"], [
   ("Black Refractor", ["1:53,927","1:289,600","1:296,000","1:366,080","1:244,000","1:192,000","1:200,267"]),
   ("Red Refractor", ["1:101,112","1:579,200","1:592,000","1:732,160","1:244,000","-","1:300,400"]),
   ("Superfractor", ["-","-","-","-","-","-","-"]),
 ]),
 # ── Hobby-exclusive inserts (only Hobby column populated) ──
 (1663, "Dumbo 85th Anniversary", None, [
   ("Base Speckle", ["1:9,987","-","-","-","-","-","-"]),
   ("Red Refractor", ["1:404,448","-","-","-","-","-","-"]),
   ("Superfractor", ["1:808,896","-","-","-","-","-","-"]),
 ]),
 (1664, "Winnie the Pooh 100th Anniversary", None, [
   ("Base Speckle Refractor", ["1:839","-","-","-","-","-","-"]),
   ("Red Refractor", ["1:17,211","-","-","-","-","-","-"]),
   ("Superfractor", ["1:115,557","-","-","-","-","-","-"]),
 ]),
 (1650, "Super Strength Chrome", None, [
   ("Base Speckle", ["1:8,426","-","-","-","-","-","-"]),
   ("Black Refractor", ["1:17,211","-","-","-","-","-","-"]),
   ("Red Refractor", ["1:36,768","-","-","-","-","-","-"]),
   ("Superfractor", ["1:161,780","-","-","-","-","-","-"]),
 ]),
 (1668, "Lilo & Stitch Shadowbox", None, [   # NOTE: odds sheet says Orange/Black/Red; Step-4 said Kaleidoscope/Shimmer/RayWave (CONFLICT — following odds sheet)
   ("Base Sparkle", ["1:1,425","-","-","-","-","-","-"]),
   ("Orange Refractor", ["1:4,844","-","-","-","-","-","-"]),
   ("Black Refractor", ["1:12,074","-","-","-","-","-","-"]),
   ("Red Refractor", ["1:23,792","-","-","-","-","-","-"]),
   ("Superfractor", ["1:115,557","-","-","-","-","-","-"]),
 ]),
 (1670, "The Heart of Te Fiti Shadowbox", None, [
   ("Base Sparkle", ["1:11,393","-","-","-","-","-","-"]),
   ("Orange Refractor", ["1:33,704","-","-","-","-","-","-"]),
   ("Black Refractor", ["1:80,890","-","-","-","-","-","-"]),
   ("Red Refractor", ["1:161,780","-","-","-","-","-","-"]),
   ("Superfractor", ["1:808,896","-","-","-","-","-","-"]),
 ]),
 (1669, "The Rose Shadowbox", None, [
   ("Base Sparkle", ["1:23,792","-","-","-","-","-","-"]),
   ("Black Refractor", ["1:80,890","-","-","-","-","-","-"]),
   ("Red Refractor", ["1:161,780","-","-","-","-","-","-"]),
   ("Superfractor", ["1:808,896","-","-","-","-","-","-"]),
 ]),
 (1667, "Mickey and Friends Ukiyo-e", None, [
   ("Base", ["1:335","-","-","-","-","-","-"]),
   ("Kaleidoscope", ["1:3,371","-","-","-","-","-","-"]),
   ("Shimmer", ["1:8,426","-","-","-","-","-","-"]),
   ("Raywave", ["1:17,211","-","-","-","-","-","-"]),
   ("Superfractor", ["1:80,890","-","-","-","-","-","-"]),
 ]),
]

# Subsets that exist but get NO parallels (cards are inherently 1/1; odds all "-")
NO_PARALLEL = {1671, 1672}  # The One and Only / The One and Only Walt

# Source subset labels in the odds sheet that have NO DB subset → skip + report
SKIPPED = [
    "Sketch Cards Gold / Sketch Cards Black (sketch inserts — no checklist subset)",
    "Disney Internal Artists Sketch (sketch insert — no checklist subset)",
    "Pixar Internal Artists Sketch (sketch insert — no checklist subset)",
    "Authentic Autographs (hard-signed auto subset — not in checklist)",
    "Cars Authentic Autographs (hard-signed auto subset — not in checklist)",
    "Disney Channel Autograph Variation (auto-variation subset — not in checklist)",
    "Disney Princesses Autographs (auto subset — not in checklist)",
    "Disney Dual Autographs (auto subset — not in checklist)",
    "Disney Triple Autographs (auto subset — not in checklist)",
    "Disney Quad Autographs (auto subset — not in checklist)",
]


def main():
    con = sqlite3.connect(os.path.abspath(DB))
    cur = con.cursor()

    # Existing subsets for this set (sanity / id validation)
    db_subsets = {r[0]: r[1] for r in cur.execute(
        "SELECT id, name FROM insert_sets WHERE set_id=?", (SET_ID,))}

    pack_odds = {f: {} for f in FORMATS}
    parallels = []   # (insert_set_id, name, print_run, exclusivity)
    key_prefixes = set()
    odds_key_count = 0

    for sid, prefix, base, pars in SUBSETS:
        assert sid in db_subsets, f"subset id {sid} not in set {SET_ID}"
        key_prefixes.add(prefix)
        # subset default exclusivity (for all-"-" parallels): first row with odds
        rows = ([base] if base else []) + [p[1] for p in pars]
        subset_default = None
        for r in rows:
            e = excl_from_cols(r)
            if e is not None:
                subset_default = e; break
        # base odds key
        if base:
            for i, f in enumerate(FORMATS):
                val = v(base[i])
                if val is not None:
                    pack_odds[f][prefix] = val; odds_key_count += 1
        # parallels
        for suffix, cols in pars:
            key = f"{prefix} {suffix}"
            for i, f in enumerate(FORMATS):
                val = v(cols[i])
                if val is not None:
                    pack_odds[f][key] = val; odds_key_count += 1
            if sid not in NO_PARALLEL:
                e = excl_from_cols(cols)
                if e is None and all(c == "-" for c in cols):
                    e = subset_default
                parallels.append((sid, suffix, print_run(sid, suffix), e or ""))

    # ── Sanity: every pack_odds key prefix must match a known prefix ──
    bad = []
    for f, d in pack_odds.items():
        for k in d:
            if not any(k == p or k.startswith(p + " ") for p in key_prefixes):
                bad.append((f, k))
    if bad:
        print("FATAL — keys with no matching subset prefix:")
        for f, k in bad[:20]:
            print(f"   [{f}] {k}")
        sys.exit(1)

    if "--commit" not in sys.argv:
        print("DRY RUN (pass --commit to write)\n")
        print(f"Subsets attached : {len(SUBSETS)}  (+{len(NO_PARALLEL)} left bare: One and Only / Walt)")
        print(f"Parallels        : {len(parallels)}")
        print(f"Pack-odds keys   : {odds_key_count} across {len(FORMATS)} formats")
        for f in FORMATS:
            print(f"   {f:<14} {len(pack_odds[f])} keys")
        numbered = sum(1 for _,_,pr,_ in parallels if pr is not None)
        print(f"Numbered parallels: {numbered} / {len(parallels)}")
        print("\nSkipped (no DB subset):")
        for s in SKIPPED:
            print(f"   - {s}")
        # spot prints
        print("\nSample Hobby base ladder:")
        for k in ["Base","Base Refractor","Base Superfractor","Base Prism Refractor","Base X-Fractor","Base Raywave","Base Pink Mini Diamond"]:
            print(f"   {k}: {pack_odds['Hobby'].get(k,'(absent)')}  | Mega CEE: {pack_odds['Mega Box CEE'].get(k,'(absent)')} | Value CEE: {pack_odds['Value Box CEE'].get(k,'(absent)')}")
        con.close()
        return

    # ── Commit ──
    ids = list(db_subsets.keys())
    ph = ",".join("?" for _ in ids)
    cur.execute(f"DELETE FROM parallels WHERE insert_set_id IN ({ph})", ids)
    cur.executemany(
        "INSERT INTO parallels (insert_set_id, name, print_run, exclusivity) VALUES (?,?,?,?)",
        [(sid, name, pr, exc) for (sid, name, pr, exc) in parallels])
    cur.execute("UPDATE sets SET pack_odds=?, box_config=? WHERE id=?",
                (json.dumps(pack_odds), json.dumps(BOX_CONFIG), SET_ID))
    con.commit()
    print(f"COMMITTED: {len(parallels)} parallels, pack_odds ({odds_key_count} keys), box_config (7 formats).")
    con.close()


if __name__ == "__main__":
    main()
