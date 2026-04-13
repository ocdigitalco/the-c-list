"""
Seed ~600 set reference entries into the database.
Skips any set whose name already exists (case-insensitive).
Usage: python3 scripts/seed_set_catalogue.py
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA foreign_keys=ON")
cur = conn.cursor()

# Get existing set names (lowercase for comparison)
cur.execute("SELECT LOWER(name) FROM sets")
existing = set(r[0] for r in cur.fetchall())

TIER_MAP = {
    "Standard": "Standard",
    "Chrome": "Chrome",
    "Chrome Black": "Chrome",
    "Sapphire": "Sapphire",
    "Finest": "Standard",
    "Heritage": "Standard",
    "Bowman": "Standard",
    "Bowman's Best": "Standard",
    "Archives": "Standard",
    "Allen & Ginter": "Standard",
    "Stadium Club": "Standard",
    "Museum Collection": "Standard",
    "Pristine": "Premium",
    "Transcendent": "Premium",
    "Dynasty": "Premium",
    "Tribute": "Standard",
    "Inception": "Standard",
    "Definitive": "Premium",
    "Diamond Icons": "Premium",
    "Sterling": "Standard",
    "Tier One": "Standard",
    "Five Star": "Premium",
    "Triple Threads": "Standard",
    "Midnight": "Standard",
    "Prizm": "Prizm",
}

def tier_to_db(tier_label):
    return TIER_MAP.get(tier_label, "Standard")

added = 0
skipped = 0

def add_set(name, sport, league, tier_label, season):
    global added, skipped
    if name.lower() in existing:
        skipped += 1
        return
    tier = tier_to_db(tier_label)
    cur.execute(
        "INSERT INTO sets (name, sport, season, league, tier) VALUES (?, ?, ?, ?, ?)",
        (name, sport, season, league, tier),
    )
    existing.add(name.lower())
    added += 1

# ═══════════════════════════════════════════════════════════════════════════════
# 2026 sets
# ═══════════════════════════════════════════════════════════════════════════════
add_set("2026 Bowman Baseball", "Baseball", "MLB", "Bowman", "2026")
add_set("2025-26 Bowman Basketball", "Basketball", "NBA", "Bowman", "2025-26")
add_set("2025 Bowman Draft Baseball Sapphire Edition", "Baseball", "MLB", "Sapphire", "2025")
add_set("2026 Topps Brooklyn Collection", "Baseball", "MLB", "Standard", "2026")
add_set("2025-26 Topps Chrome Cactus Jack Basketball", "Basketball", "NBA", "Chrome", "2025-26")
add_set("2025 Topps Chrome Football", "Football", "NFL", "Chrome", "2025")
add_set("2025 Topps Chrome Formula 1 Sapphire Edition", "Racing", "F1", "Sapphire", "2025")
add_set("2026 Topps Collector Kit", "Other", None, "Standard", "2026")
add_set("2025 Topps Definitive Baseball", "Baseball", "MLB", "Definitive", "2025")
add_set("2026 Topps Disney Neon", "Entertainment", "Disney", "Standard", "2026")
add_set("2025 Topps Exalted WWE", "Wrestling", "WWE", "Standard", "2025")
add_set("2026 Topps Finest Fantastic Four", "Entertainment", "Marvel", "Standard", "2026")
add_set("2025 Topps Marvel Studios Chrome Sapphire", "Entertainment", "Marvel", "Sapphire", "2025")
add_set("2025 Topps Marvel The Collector", "Entertainment", "Marvel", "Standard", "2025")
add_set("2025 Topps Star Wars Smugglers Outpost", "Entertainment", "Star Wars", "Standard", "2025")
add_set("2025 Topps Transcendent Collection Baseball", "Baseball", "MLB", "Premium", "2025")
add_set("2025 Topps 30 Years of Toy Story", "Entertainment", "Disney", "Standard", "2025")

# ═══════════════════════════════════════════════════════════════════════════════
# 2025 sets
# ═══════════════════════════════════════════════════════════════════════════════
add_set("2025 Bowman Baseball", "Baseball", "MLB", "Standard", "2025")
add_set("2025 Bowman Baseball Sapphire", "Baseball", "MLB", "Sapphire", "2025")
add_set("2025 Bowman Mega Box Baseball", "Baseball", "MLB", "Standard", "2025")
add_set("2025 Bowman Chrome Baseball", "Baseball", "MLB", "Chrome", "2025")
add_set("2025 Bowman Chrome Baseball Mega Box", "Baseball", "MLB", "Chrome", "2025")
add_set("2025 Bowman Chrome Baseball Sapphire Edition", "Baseball", "MLB", "Sapphire", "2025")
add_set("2025 Bowman Draft Baseball", "Baseball", "MLB", "Standard", "2025")
add_set("2025 Bowman Draft Baseball Mega Box", "Baseball", "MLB", "Standard", "2025")
add_set("2024-25 Bowman University Best Basketball", "Basketball", "NCAA", "Standard", "2024-25")
add_set("2024 Bowman University Best Football", "Football", "NCAA", "Standard", "2024")
add_set("2024-25 Bowman University Chrome Basketball", "Basketball", "NCAA", "Chrome", "2024-25")
add_set("2024-25 Bowman University Chrome Basketball Sapphire", "Basketball", "NCAA", "Sapphire", "2024-25")
add_set("2025 Bowman University Chrome Football", "Football", "NCAA", "Chrome", "2025")
add_set("2025 Pixar Gold", "Entertainment", "Disney", "Standard", "2025")
add_set("2024 Topps Archives Baseball", "Baseball", "MLB", "Standard", "2024")
add_set("2025 Topps Archives Signature Series Active Player Edition", "Baseball", "MLB", "Standard", "2025")
add_set("2025 Topps Chrome Baseball", "Baseball", "MLB", "Chrome", "2025")
add_set("2025 Topps Chrome Baseball Logofractor Edition", "Baseball", "MLB", "Chrome", "2025")
add_set("2025 Topps Chrome Baseball Sapphire Edition", "Baseball", "MLB", "Sapphire", "2025")
add_set("2025 Topps Chrome Baseball Update Series", "Baseball", "MLB", "Chrome", "2025")
add_set("2025-26 Topps Chrome Basketball", "Basketball", "NBA", "Chrome", "2025-26")
add_set("2024-25 Topps Chrome Basketball", "Basketball", "NBA", "Chrome", "2024-25")
add_set("2025 Topps Chrome Basketball Sapphire", "Basketball", "NBA", "Sapphire", "2025")
add_set("2025 Topps Chrome Black Baseball", "Baseball", "MLB", "Chrome", "2025")
add_set("2024 Topps Chrome Black Star Wars", "Entertainment", "Star Wars", "Chrome", "2024")
add_set("2025 Topps Chrome Bundesliga", "Soccer", "Bundesliga", "Chrome", "2025")
add_set("2025 Topps x Bob Ross The Joy of Baseball", "Baseball", "MLB", "Standard", "2025")
add_set("2025 Topps Chrome Sapphire Bundesliga", "Soccer", "Bundesliga", "Sapphire", "2025")
add_set("2025 Topps Chrome Disney", "Entertainment", "Disney", "Chrome", "2025")
add_set("2025 Topps Chrome Disney Sapphire", "Entertainment", "Disney", "Sapphire", "2025")
add_set("2024 Topps Chrome Football", "Football", "NFL", "Chrome", "2024")
add_set("2024 Topps Chrome Football Sapphire Edition", "Football", "NFL", "Sapphire", "2024")
add_set("2024 Topps Chrome Sapphire Formula 1", "Racing", "F1", "Sapphire", "2024")
add_set("2024 Topps Chrome Sapphire Garbage Pail Kids", "Entertainment", "GPK", "Sapphire", "2024")
add_set("2025 Topps Chrome Spongebob 25th Anniversary", "Entertainment", None, "Chrome", "2025")
add_set("2025 Topps Chrome Spongebob 25th Anniversary Sapphire", "Entertainment", None, "Sapphire", "2025")
add_set("2025 Topps Chrome Star Wars", "Entertainment", "Star Wars", "Chrome", "2025")
add_set("2025 Topps Chrome Star Wars Costco", "Entertainment", "Star Wars", "Chrome", "2025")
add_set("2025 Topps Chrome Star Wars Galaxy", "Entertainment", "Star Wars", "Chrome", "2025")
add_set("2025 Topps Chrome Star Wars The National", "Entertainment", "Star Wars", "Chrome", "2025")
add_set("2024 Topps Chrome Boxing", "Boxing", None, "Chrome", "2024")
add_set("2024-25 Topps Chrome UEFA Club Competitions Sapphire Edition", "Soccer", "UEFA", "Sapphire", "2024-25")
add_set("2025 Topps Chrome UFC Sapphire Edition", "MMA", "UFC", "Sapphire", "2025")
add_set("2025 Topps Chrome VeeFriends", "Entertainment", None, "Chrome", "2025")
add_set("2025 Topps Chrome WWE x Cactus Jack", "Wrestling", "WWE", "Chrome", "2025")
add_set("2025 Topps Complete Sets Baseball", "Baseball", "MLB", "Standard", "2025")
add_set("2024 Topps Cosmic Chrome Football", "Football", "NFL", "Chrome", "2024")
add_set("2024 Topps Definitive Baseball", "Baseball", "MLB", "Premium", "2024")
add_set("2025 Topps Diamond Icons Baseball", "Baseball", "MLB", "Premium", "2025")
add_set("2024 Topps Diamond Icons Baseball", "Baseball", "MLB", "Premium", "2024")
add_set("2025 Topps Disney Wonder", "Entertainment", "Disney", "Standard", "2025")
add_set("2024 Topps Dune Chrome", "Entertainment", None, "Chrome", "2024")
add_set("2025 Topps Dynamic Duals Baseball", "Baseball", "MLB", "Standard", "2025")
add_set("2024 Topps Dynasty Baseball", "Baseball", "MLB", "Premium", "2024")
add_set("2025 Topps Dynasty Formula 1", "Racing", "F1", "Premium", "2025")
add_set("2024 Topps Dynasty Formula 1", "Racing", "F1", "Premium", "2024")
add_set("2025 Topps Finest Baseball", "Baseball", "MLB", "Standard", "2025")
add_set("2024-25 Topps Finest Basketball", "Basketball", "NBA", "Standard", "2024-25")
add_set("2024 Topps Finest Football", "Football", "NFL", "Standard", "2024")
add_set("2024 Topps Finest Formula 1", "Racing", "F1", "Standard", "2024")
add_set("2025 Topps Formula 1 Fanatics Fest Exclusive", "Racing", "F1", "Standard", "2025")
add_set("2024 Topps Finest MLS", "Soccer", "MLS", "Standard", "2024")
add_set("2024-25 Topps Finest UCC", "Soccer", "UEFA", "Standard", "2024-25")
add_set("2024 Topps Finest UFC", "MMA", "UFC", "Standard", "2024")
add_set("2025 Topps Finest X-Men 97", "Entertainment", "Marvel", "Standard", "2025")
add_set("2024 Topps Garbage Pail Kids Chrome 7 Hobby", "Entertainment", "GPK", "Chrome", "2024")
add_set("2024 Topps Garbage Pail Kids Chrome 7 Retail", "Entertainment", "GPK", "Chrome", "2024")
add_set("2024 GPK Battle of the Bands Green Day", "Entertainment", "GPK", "Standard", "2024")
add_set("2024-25 Topps G-League Basketball", "Basketball", "NBA", "Standard", "2024-25")
add_set("2025 Topps Heritage Baseball", "Baseball", "MLB", "Standard", "2025")
add_set("2024 Topps Heritage High Number", "Baseball", "MLB", "Standard", "2024")
add_set("2024 Topps High-Tek Stranger Things", "Entertainment", None, "Standard", "2024")
add_set("2025 Topps Holiday Baseball", "Baseball", "MLB", "Standard", "2025")
add_set("2025-26 Topps Holiday Basketball", "Basketball", "NBA", "Standard", "2025-26")
add_set("2024 Topps Inception Baseball", "Baseball", "MLB", "Standard", "2024")
add_set("2024-25 Topps Inception Basketball", "Basketball", "NBA", "Standard", "2024-25")
add_set("2024 Topps Inception Football", "Football", "NFL", "Standard", "2024")
add_set("2025 Topps Knockout UFC", "MMA", "UFC", "Standard", "2025")
add_set("2024 Topps Luminaries Baseball", "Baseball", "MLB", "Standard", "2024")
add_set("2025 Marvel Comic Book Heroes 1975 Anniversary", "Entertainment", "Marvel", "Standard", "2025")
add_set("2025 Topps Marvel Comics Chrome", "Entertainment", "Marvel", "Chrome", "2025")
add_set("2025 Topps Marvel Comics Chrome Sapphire", "Entertainment", "Marvel", "Sapphire", "2025")
add_set("2025 Topps Marvel Studios Chrome", "Entertainment", "Marvel", "Chrome", "2025")
add_set("2024 Topps Masterwork Star Wars", "Entertainment", "Star Wars", "Standard", "2024")
add_set("2024 Topps McDonald's All American Chrome", "Basketball", "NCAA", "Chrome", "2024")
add_set("2024-25 Topps Midnight Bundesliga", "Soccer", "Bundesliga", "Standard", "2024-25")
add_set("2024 Topps Midnight Football", "Football", "NFL", "Standard", "2024")
add_set("2025 Topps Mint Disney", "Entertainment", "Disney", "Standard", "2025")
add_set("2025 Topps Mint Marvel", "Entertainment", "Marvel", "Standard", "2025")
add_set("2025 Topps MLB Dynamic Duals", "Baseball", "MLB", "Standard", "2025")
add_set("2024 Topps MLS Chrome Sapphire Edition", "Soccer", "MLS", "Sapphire", "2024")
add_set("2023-24 Topps Motif Basketball", "Basketball", "NBA", "Standard", "2023-24")
add_set("2024-25 Topps NBL Chrome Basketball", "Basketball", "NBL", "Chrome", "2024-25")
add_set("2024-25 Topps NHL Sticker Collection", "Hockey", "NHL", "Standard", "2024-25")
add_set("2024 Topps NOW Football Rookie Campaign", "Football", "NFL", "Standard", "2024")
add_set("2025-26 Topps Premier League", "Soccer", "EPL", "Standard", "2025-26")
add_set("2025 Topps Pro Debut Baseball", "Baseball", "MLB", "Standard", "2025")
add_set("2024 Topps Resurgence Football", "Football", "NFL", "Standard", "2024")
add_set("2024-25 Topps Reverence UCC", "Soccer", "UEFA", "Standard", "2024-25")
add_set("2023-24 Topps Royalty Basketball", "Basketball", "NBA", "Standard", "2023-24")
add_set("2024 Topps Royalty Tennis", "Tennis", None, "Standard", "2024")
add_set("2025 Topps Series 1 Baseball", "Baseball", "MLB", "Standard", "2025")
add_set("2025 Topps Series 1 Mega Celebration", "Baseball", "MLB", "Standard", "2025")
add_set("2025 Topps Series 2 Baseball", "Baseball", "MLB", "Standard", "2025")
add_set("2025 Topps Welcome to the Club", "Baseball", "MLB", "Standard", "2025")
add_set("2024 Topps Signature Class Football", "Football", "NFL", "Standard", "2024")
add_set("2024 Topps Star Wars Galactic Antiquities", "Entertainment", "Star Wars", "Standard", "2024")
add_set("2024 Topps Star Wars High-Tek", "Entertainment", "Star Wars", "Standard", "2024")
add_set("2025 Topps Star Wars Hyperspace", "Entertainment", "Star Wars", "Standard", "2025")
add_set("2024 Topps Star Wars Hyperspace", "Entertainment", "Star Wars", "Standard", "2024")
add_set("2025 Topps Star Wars Meiyo", "Entertainment", "Star Wars", "Standard", "2025")
add_set("2025 Topps Sterling Baseball", "Baseball", "MLB", "Standard", "2025")
add_set("2023-24 Topps Three Basketball", "Basketball", "NBA", "Standard", "2023-24")
add_set("2025 Topps Tier One Baseball", "Baseball", "MLB", "Standard", "2025")
add_set("2025 Topps Tribute Baseball", "Baseball", "MLB", "Standard", "2025")
add_set("2025 Topps Baseball Update Series", "Baseball", "MLB", "Standard", "2025")
add_set("2025 Topps Wacky Packages All New Series", "Entertainment", "GPK", "Standard", "2025")
add_set("2025 Topps Wacky Packages All New Series Halloween Edition", "Entertainment", "GPK", "Standard", "2025")
add_set("2025 Topps WWE Chrome", "Wrestling", "WWE", "Chrome", "2025")
add_set("2025 Topps Chrome Sapphire WWE", "Wrestling", "WWE", "Sapphire", "2025")
add_set("2025 Worst of Garbage Pail Kids 40th Anniversary", "Entertainment", "GPK", "Standard", "2025")
add_set("2025 Topps Finest WWE", "Wrestling", "WWE", "Standard", "2025")

# ═══════════════════════════════════════════════════════════════════════════════
# 2024 sets
# ═══════════════════════════════════════════════════════════════════════════════
S24 = [
    ("2024 Topps Baseball Series 1", "Baseball", "MLB", "Standard", "2024"),
    ("2024 Topps Baseball Series 2", "Baseball", "MLB", "Standard", "2024"),
    ("2024 Topps Allen & Ginter Baseball", "Baseball", "MLB", "Standard", "2024"),
    ("2024 Topps Allen & Ginter X", "Baseball", "MLB", "Standard", "2024"),
    ("2024 Topps Baseball Holiday Mega Box", "Baseball", "MLB", "Standard", "2024"),
    ("2024 Topps Baseball Holiday Advent Calendar", "Baseball", "MLB", "Standard", "2024"),
    ("2024 Bowman Baseball", "Baseball", "MLB", "Standard", "2024"),
    ("2024 Bowman Baseball Sapphire Edition", "Baseball", "MLB", "Sapphire", "2024"),
    ("2024 Bowman's Best Baseball", "Baseball", "MLB", "Standard", "2024"),
    ("2024 Bowman Chrome Baseball", "Baseball", "MLB", "Chrome", "2024"),
    ("2024 Bowman Chrome Baseball Mega Box", "Baseball", "MLB", "Chrome", "2024"),
    ("2023 Bowman Draft Baseball Sapphire Edition", "Baseball", "MLB", "Sapphire", "2023"),
    ("2024 Bowman Draft Baseball", "Baseball", "MLB", "Standard", "2024"),
    ("2024 Bowman Draft Baseball Sapphire Edition", "Baseball", "MLB", "Sapphire", "2024"),
    ("2023 Bowman Inception Baseball", "Baseball", "MLB", "Standard", "2023"),
    ("2024 Bowman Mega Box Baseball", "Baseball", "MLB", "Standard", "2024"),
    ("2024 Bowman Sterling Baseball", "Baseball", "MLB", "Standard", "2024"),
    ("2023 Bowman University Best Football", "Football", "NCAA", "Standard", "2023"),
    ("2023-24 Bowman University Chrome Basketball", "Basketball", "NCAA", "Chrome", "2023-24"),
    ("2024 Bowman University Chrome Football", "Football", "NCAA", "Chrome", "2024"),
    ("2024 Bowman University Chrome Football Sapphire Edition", "Football", "NCAA", "Sapphire", "2024"),
    ("2024 Bowman U Best Basketball", "Basketball", "NCAA", "Standard", "2024"),
    ("2024 Complete Sets Baseball", "Baseball", "MLB", "Standard", "2024"),
    ("2024 Topps Cosmic Chrome Baseball", "Baseball", "MLB", "Chrome", "2024"),
    ("2023-24 Topps Cosmic Chrome Basketball", "Basketball", "NBA", "Chrome", "2023-24"),
    ("2024 Cosmic Chrome X Cactus Jack", "Baseball", "MLB", "Chrome", "2024"),
    ("2024 National Silver Pack", "Baseball", "MLB", "Standard", "2024"),
    ("2024 Topps Brooklyn Collection Baseball", "Baseball", "MLB", "Standard", "2024"),
    ("2023-24 Topps Chrome NBL", "Basketball", "NBL", "Chrome", "2023-24"),
    ("2024 Topps Chrome Baseball", "Baseball", "MLB", "Chrome", "2024"),
    ("2024 Topps Chrome Baseball FFNYC", "Baseball", "MLB", "Chrome", "2024"),
    ("2024 Topps Chrome Baseball Sapphire Edition", "Baseball", "MLB", "Sapphire", "2024"),
    ("2023-24 Topps Chrome Basketball Hobby", "Basketball", "NBA", "Chrome", "2023-24"),
    ("2023-24 Topps Chrome Basketball Retail", "Basketball", "NBA", "Chrome", "2023-24"),
    ("2023-24 Topps Chrome Basketball Sapphire Edition", "Basketball", "NBA", "Sapphire", "2023-24"),
    ("2023-24 Topps Chrome Bundesliga", "Soccer", "Bundesliga", "Chrome", "2023-24"),
    ("2024 Topps Chrome Baseball Logofractor Edition", "Baseball", "MLB", "Chrome", "2024"),
    ("2024 Topps Chrome Formula 1", "Racing", "F1", "Chrome", "2024"),
    ("2024 Topps Chrome Tennis", "Tennis", None, "Chrome", "2024"),
    ("2024 Topps Chrome Tennis Sapphire Edition", "Tennis", None, "Sapphire", "2024"),
    ("2024 Topps Chrome UFC", "MMA", "UFC", "Chrome", "2024"),
    ("2023-24 Topps Chrome UEFA Club Competitions", "Soccer", "UEFA", "Chrome", "2023-24"),
    ("2023-24 Topps Chrome UEFA Club Competitions Sapphire Edition", "Soccer", "UEFA", "Sapphire", "2023-24"),
    ("2024 Topps Chrome UEFA EURO", "Soccer", "UEFA", "Chrome", "2024"),
    ("2024 Topps Chrome UEFA EURO Sapphire Edition", "Soccer", "UEFA", "Sapphire", "2024"),
    ("2024 Topps Chrome UEFA Women's Champions League Sapphire Edition", "Soccer", "UEFA", "Sapphire", "2024"),
    ("2024 Topps Chrome Update Series Baseball", "Baseball", "MLB", "Chrome", "2024"),
    ("2024 Topps Chrome Updates Baseball Sapphire Edition", "Baseball", "MLB", "Sapphire", "2024"),
    ("2023-24 Topps Chrome UWCL", "Soccer", "UEFA", "Chrome", "2023-24"),
    ("2023-24 Topps Finest Basketball", "Basketball", "NBA", "Standard", "2023-24"),
    ("2024 GPK Series 1", "Entertainment", "GPK", "Standard", "2024"),
    ("2023-24 Topps G League Basketball", "Basketball", "NBA", "Standard", "2023-24"),
    ("2024 Topps Gilded Collection Baseball", "Baseball", "MLB", "Standard", "2024"),
    ("2024 Topps Gold Label UFC", "MMA", "UFC", "Standard", "2024"),
    ("2024 Topps Graphite Tennis", "Tennis", None, "Standard", "2024"),
    ("2024 Topps Heritage Baseball", "Baseball", "MLB", "Standard", "2024"),
    ("2024 Topps Heritage Mini Edition", "Baseball", "MLB", "Standard", "2024"),
    ("2024 Topps Knockout UFC", "MMA", "UFC", "Standard", "2024"),
    ("2023 Topps Luminaries Baseball", "Baseball", "MLB", "Standard", "2023"),
    ("2023-24 Topps Midnight Basketball", "Basketball", "NBA", "Standard", "2023-24"),
    ("2023-24 Topps Mercury Victor Wembanyama", "Basketball", "NBA", "Standard", "2023-24"),
    ("2024 MLB Topps NOW", "Baseball", "MLB", "Standard", "2024"),
    ("2024 Topps MLS Chrome Hobby", "Soccer", "MLS", "Chrome", "2024"),
    ("2024 Topps MLS Chrome Mania", "Soccer", "MLS", "Chrome", "2024"),
    ("2024 Topps MLS Superstars", "Soccer", "MLS", "Standard", "2024"),
    ("2024 Topps Midnight UFC", "MMA", "UFC", "Standard", "2024"),
    ("2023 Topps Motif Football", "Football", "NFL", "Standard", "2023"),
    ("2024 Topps Museum Collection Baseball", "Baseball", "MLB", "Standard", "2024"),
    ("2023-24 Topps Museum Collection UEFA Champions League", "Soccer", "UEFA", "Standard", "2023-24"),
    ("2024 Topps UFC NYC", "MMA", "UFC", "Standard", "2024"),
    ("2023-24 Topps NBL", "Basketball", "NBL", "Standard", "2023-24"),
    ("2024 Olympics Games Topps NOW", "Other", None, "Standard", "2024"),
    ("2023-24 Topps Overtime Elite Chrome", "Basketball", None, "Chrome", "2023-24"),
    ("2024 Topps Paddock Pass Formula 1", "Racing", "F1", "Standard", "2024"),
    ("2024 Topps Pristine Baseball", "Baseball", "MLB", "Premium", "2024"),
    ("Topps Pristine Road to UEFA EURO 2024", "Soccer", "UEFA", "Premium", "2024"),
    ("2024 Topps Pro Debut Baseball", "Baseball", "MLB", "Standard", "2024"),
    ("2024 Topps 50/50 Shohei Ohtani", "Baseball", "MLB", "Standard", "2024"),
    ("2023 Topps Stadium Club Baseball", "Baseball", "MLB", "Standard", "2023"),
    ("2024 Topps Stadium Club Baseball", "Baseball", "MLB", "Standard", "2024"),
    ("2024 Topps Stadium Club Chrome UEFA Champions League", "Soccer", "UEFA", "Chrome", "2024"),
    ("2024 Topps Star Wars Chrome", "Entertainment", "Star Wars", "Chrome", "2024"),
    ("2024 Topps Star Wars Chrome Galaxy", "Entertainment", "Star Wars", "Chrome", "2024"),
    ("2024 Topps Star Wars Chrome Sapphire", "Entertainment", "Star Wars", "Sapphire", "2024"),
    ("2024 Topps Sterling Baseball", "Baseball", "MLB", "Standard", "2024"),
    ("2024 Topps Tier One Baseball", "Baseball", "MLB", "Standard", "2024"),
    ("2024 Topps Tribute Baseball", "Baseball", "MLB", "Standard", "2024"),
    ("2024 Topps Triple Threads Baseball", "Baseball", "MLB", "Standard", "2024"),
    ("2023 Topps Transcendent Collection Baseball", "Baseball", "MLB", "Premium", "2023"),
    ("2024 Topps Transcendent Baseball", "Baseball", "MLB", "Premium", "2024"),
    ("2024 Topps Transcendent VIP Baseball", "Baseball", "MLB", "Premium", "2024"),
    ("2023-24 Topps UCC Merlin", "Soccer", "UEFA", "Standard", "2023-24"),
    ("2022-23 Topps UCL Dynasty", "Soccer", "UEFA", "Premium", "2022-23"),
    ("2023-24 Topps UEFA Club Competitions", "Soccer", "UEFA", "Standard", "2023-24"),
    ("2024-25 Topps UEFA Club Competitions", "Soccer", "UEFA", "Standard", "2024-25"),
    ("2024 Topps Baseball Update Series", "Baseball", "MLB", "Standard", "2024"),
    ("2022 Clerks III", "Entertainment", None, "Standard", "2022"),
    ("2022 Clerks III One-Hitter", "Entertainment", None, "Standard", "2022"),
    ("2024 Topps Archives Signature Series Active Player Edition", "Baseball", "MLB", "Standard", "2024"),
    ("2024 Topps Archives Signature Series Retired Player Edition", "Baseball", "MLB", "Standard", "2024"),
    ("2024 Topps Big League Baseball", "Baseball", "MLB", "Standard", "2024"),
    ("2024 Topps Chrome Black Baseball", "Baseball", "MLB", "Chrome", "2024"),
    ("2023 Topps Chrome Platinum 54 Baseball", "Baseball", "MLB", "Chrome", "2023"),
    ("2023 Topps Composite Football", "Football", "NFL", "Standard", "2023"),
    ("2023 Topps Diamond Icons Baseball", "Baseball", "MLB", "Premium", "2023"),
    ("2023 Topps Dynasty Baseball", "Baseball", "MLB", "Premium", "2023"),
    ("2024 Topps Five Star Baseball", "Baseball", "MLB", "Premium", "2024"),
    ("2024 Topps Finest Baseball", "Baseball", "MLB", "Standard", "2024"),
    ("2023 Topps Finest MLS", "Soccer", "MLS", "Standard", "2023"),
    ("Topps Finest Road to EURO 2024", "Soccer", "UEFA", "Standard", "2024"),
    ("2023-24 Topps Finest UEFA Club Competitions", "Soccer", "UEFA", "Standard", "2023-24"),
    ("2023 Topps Five Star Baseball", "Baseball", "MLB", "Premium", "2023"),
    ("2023 Topps Formula 1 Chrome", "Racing", "F1", "Chrome", "2023"),
    ("2023 Topps Formula 1 Chrome Sapphire Edition", "Racing", "F1", "Sapphire", "2023"),
    ("2023 Topps Formula 1 Dynasty", "Racing", "F1", "Premium", "2023"),
    ("2024 Topps NOW Football", "Football", "NFL", "Standard", "2024"),
    ("2024 Topps 206 Baseball", "Baseball", "MLB", "Standard", "2024"),
    ("2024 Topps x Lids", "Baseball", "MLB", "Standard", "2024"),
]
for s in S24:
    add_set(*s)

# ═══════════════════════════════════════════════════════════════════════════════
# 2023 sets
# ═══════════════════════════════════════════════════════════════════════════════
S23 = [
    ("2022 Topps Allen and Ginter Chrome", "Baseball", "MLB", "Standard", "2022"),
    ("2023 Topps Allen and Ginter Baseball", "Baseball", "MLB", "Standard", "2023"),
    ("2023 Topps Allen and Ginter X", "Baseball", "MLB", "Standard", "2023"),
    ("2023 Topps Archives Baseball", "Baseball", "MLB", "Standard", "2023"),
    ("2023 Topps Archives Signature Series Active Player Edition", "Baseball", "MLB", "Standard", "2023"),
    ("2023 Topps Athletes Unlimited", "Other", None, "Standard", "2023"),
    ("2023 Topps Baseball Update Series", "Baseball", "MLB", "Standard", "2023"),
    ("2023 Topps Big League Baseball", "Baseball", "MLB", "Standard", "2023"),
    ("2023 Bowman Baseball", "Baseball", "MLB", "Standard", "2023"),
    ("2023 Bowman Baseball First Edition", "Baseball", "MLB", "Standard", "2023"),
    ("2022 Bowman's Best Baseball", "Baseball", "MLB", "Standard", "2022"),
    ("2023 Bowman's Best Baseball", "Baseball", "MLB", "Standard", "2023"),
    ("2023 Bowman Chrome Baseball", "Baseball", "MLB", "Chrome", "2023"),
    ("2023 Bowman Chrome Baseball Sapphire Edition", "Baseball", "MLB", "Sapphire", "2023"),
    ("2023 Bowman Chrome Mega", "Baseball", "MLB", "Chrome", "2023"),
    ("2023 Bowman Draft Baseball Sapphire Edition", "Baseball", "MLB", "Sapphire", "2023"),
    ("2022 Bowman Inception Baseball", "Baseball", "MLB", "Standard", "2022"),
    ("2023 Bowman Platinum Baseball", "Baseball", "MLB", "Standard", "2023"),
    ("2023 Bowman Sapphire Baseball", "Baseball", "MLB", "Sapphire", "2023"),
    ("2023 Bowman Sterling Baseball", "Baseball", "MLB", "Standard", "2023"),
    ("2023 Bowman U Alabama Football", "Football", "NCAA", "Standard", "2023"),
    ("2022-23 Bowman University Best Basketball", "Basketball", "NCAA", "Standard", "2022-23"),
    ("2022-23 Bowman University Best Football", "Football", "NCAA", "Standard", "2022-23"),
    ("2023 Bowman University Best Football", "Football", "NCAA", "Standard", "2023"),
    ("2022-23 Bowman University Chrome Basketball", "Basketball", "NCAA", "Chrome", "2022-23"),
    ("2023-24 Bowman University Chrome Basketball", "Basketball", "NCAA", "Chrome", "2023-24"),
    ("2022 Bowman University Chrome Football", "Football", "NCAA", "Chrome", "2022"),
    ("2023 Bowman University Chrome Football", "Football", "NCAA", "Chrome", "2023"),
    ("2023 Bowman University Chrome Football Sapphire Edition", "Football", "NCAA", "Sapphire", "2023"),
    ("2022-23 Bowman University Inception", "Basketball", "NCAA", "Standard", "2022-23"),
    ("2023 Topps Brooklyn Collection Baseball", "Baseball", "MLB", "Standard", "2023"),
    ("2023-24 Topps Bundesliga Chrome Sapphire Edition", "Soccer", "Bundesliga", "Sapphire", "2023-24"),
    ("2023 Topps Chrome Baseball", "Baseball", "MLB", "Chrome", "2023"),
    ("2022 Topps Chrome Baseball Sonic Edition", "Baseball", "MLB", "Chrome", "2022"),
    ("2023 Topps Chrome Black Baseball", "Baseball", "MLB", "Chrome", "2023"),
    ("2022 Topps Chrome Bundesliga", "Soccer", "Bundesliga", "Chrome", "2022"),
    ("2023 Topps Chrome Formula 1", "Racing", "F1", "Chrome", "2023"),
    ("2023 Topps Chrome Logofractor", "Baseball", "MLB", "Chrome", "2023"),
    ("2022 Topps Chrome McDonald's All American Basketball", "Basketball", "NCAA", "Chrome", "2022"),
    ("2023 Topps Chrome McDonald's All American Basketball", "Basketball", "NCAA", "Chrome", "2023"),
    ("2023 Topps Chrome NBL", "Basketball", "NBL", "Chrome", "2023"),
    ("2022-23 Topps Chrome NHL Stickers", "Hockey", "NHL", "Chrome", "2022-23"),
    ("2022 Topps Chrome Platinum Anniversary", "Baseball", "MLB", "Chrome", "2022"),
    ("2023 Topps Chrome Sapphire Baseball", "Baseball", "MLB", "Sapphire", "2023"),
    ("2023 Topps Chrome Update Series Baseball", "Baseball", "MLB", "Chrome", "2023"),
    ("2023 Topps Chrome Update Series Sapphire Edition", "Baseball", "MLB", "Sapphire", "2023"),
    ("2023 Topps Complete Set Baseball", "Baseball", "MLB", "Standard", "2023"),
    ("2023 Topps Cosmic Chrome Baseball", "Baseball", "MLB", "Chrome", "2023"),
    ("2023 Topps Definitive Baseball", "Baseball", "MLB", "Premium", "2023"),
    ("2023 Topps Diamond Icons Baseball", "Baseball", "MLB", "Premium", "2023"),
    ("2022 Topps Dynasty Baseball", "Baseball", "MLB", "Premium", "2022"),
    ("2023 Topps Finest Baseball", "Baseball", "MLB", "Standard", "2023"),
    ("2023 Topps Finest Bundesliga", "Soccer", "Bundesliga", "Standard", "2023"),
    ("2023 Topps Finest Flashbacks Baseball", "Baseball", "MLB", "Standard", "2023"),
    ("2022-23 Topps Finest Flashbacks UEFA Club Competitions", "Soccer", "UEFA", "Standard", "2022-23"),
    ("2022-23 Topps Finest Overtime Elite", "Basketball", None, "Standard", "2022-23"),
    ("2023 Topps Finest UEFA Champions League", "Soccer", "UEFA", "Standard", "2023"),
    ("2022 Topps Formula 1 Dynasty", "Racing", "F1", "Premium", "2022"),
    ("2023 Topps Gilded Collection Baseball", "Baseball", "MLB", "Standard", "2023"),
    ("2022 Topps Gold Label Baseball", "Baseball", "MLB", "Standard", "2022"),
    ("2023 Topps GPK Kids Go on Vacation", "Entertainment", "GPK", "Standard", "2023"),
    ("2023 Hidden Gems", "Baseball", "MLB", "Standard", "2023"),
    ("2023 Topps GPK Sapphire Edition", "Entertainment", "GPK", "Sapphire", "2023"),
    ("2023 Topps GPK Series 2", "Entertainment", "GPK", "Standard", "2023"),
    ("2023 Topps GPK x View Askew", "Entertainment", "GPK", "Standard", "2023"),
    ("2023 Topps Heritage Baseball", "Baseball", "MLB", "Standard", "2023"),
    ("2023 Topps Heritage High Number Baseball", "Baseball", "MLB", "Standard", "2023"),
    ("2023 Topps Baseball Holiday", "Baseball", "MLB", "Standard", "2023"),
    ("2023 Topps Inception Baseball", "Baseball", "MLB", "Standard", "2023"),
    ("2023 Topps Major League Soccer", "Soccer", "MLS", "Standard", "2023"),
    ("2023 Topps Major League Soccer Chrome", "Soccer", "MLS", "Chrome", "2023"),
    ("2023 Topps Museum Collection Baseball", "Baseball", "MLB", "Standard", "2023"),
    ("2022-23 Topps Museum Collection UEFA Champions League", "Soccer", "UEFA", "Standard", "2022-23"),
    ("2023 The National Checklist", "Baseball", "MLB", "Standard", "2023"),
    ("2022-23 Topps NBL", "Basketball", "NBL", "Standard", "2022-23"),
    ("2022-23 Topps Overtime Elite Chrome Basketball", "Basketball", None, "Chrome", "2022-23"),
    ("2023 Topps Pristine Baseball", "Baseball", "MLB", "Premium", "2023"),
    ("2023 Topps Pro Debut Baseball", "Baseball", "MLB", "Standard", "2023"),
    ("2023 Topps Rip Baseball", "Baseball", "MLB", "Standard", "2023"),
    ("2022 Topps Stadium Club Chrome", "Baseball", "MLB", "Chrome", "2022"),
    ("2023 Topps Star Wars Chrome", "Entertainment", "Star Wars", "Chrome", "2023"),
    ("2023 Topps Star Wars Chrome Black", "Entertainment", "Star Wars", "Chrome", "2023"),
    ("2023 Topps Series 1 Baseball", "Baseball", "MLB", "Standard", "2023"),
    ("2023 Topps Series 1 Baseball First Edition", "Baseball", "MLB", "Standard", "2023"),
    ("2023 Topps Series 2 Baseball", "Baseball", "MLB", "Standard", "2023"),
    ("2023 Topps Star Wars Chrome Galaxy", "Entertainment", "Star Wars", "Chrome", "2023"),
    ("2023 Topps Star Wars Finest", "Entertainment", "Star Wars", "Standard", "2023"),
    ("2023 Topps Star Wars High-Tek", "Entertainment", "Star Wars", "Standard", "2023"),
    ("2022 Topps Star Masterwork", "Entertainment", "Star Wars", "Standard", "2022"),
    ("2023 Topps Star Wars Obi-Wan Kenobi", "Entertainment", "Star Wars", "Standard", "2023"),
    ("2023 Star Wars Sapphire Return of the Jedi 40th Anniversary", "Entertainment", "Star Wars", "Sapphire", "2023"),
    ("2023 Topps Star Wars Signature Series", "Entertainment", "Star Wars", "Standard", "2023"),
    ("2023 Topps Sterling Baseball", "Baseball", "MLB", "Standard", "2023"),
    ("2023 Stranger Things Fright Flicks", "Entertainment", None, "Standard", "2023"),
    ("2021 Topps Tennis Chrome", "Tennis", None, "Chrome", "2021"),
    ("2023 Topps Tier One Baseball", "Baseball", "MLB", "Standard", "2023"),
    ("2023 Topps Tribute Baseball", "Baseball", "MLB", "Standard", "2023"),
    ("2023 Topps World Baseball Classic Global Stars", "Baseball", "MLB", "Standard", "2023"),
    ("2022-23 Topps UEFA Champions Competitions 1st Edition", "Soccer", "UEFA", "Standard", "2022-23"),
    ("2023 Topps UEFA Champions League Club Competitions", "Soccer", "UEFA", "Standard", "2023"),
    ("2023 Topps UEFA Chrome", "Soccer", "UEFA", "Chrome", "2023"),
    ("2023 Topps UEFA Champions League Chrome Sapphire", "Soccer", "UEFA", "Sapphire", "2023"),
    ("2023 Topps UEFA Merlin", "Soccer", "UEFA", "Standard", "2023"),
    ("2022-23 Topps UEFA Womens Champions League Chrome Sapphire", "Soccer", "UEFA", "Sapphire", "2022-23"),
    ("2023 Topps World Baseball Classic", "Baseball", "MLB", "Standard", "2023"),
]
for s in S23:
    add_set(*s)

# Due to the massive size, I'll batch the remaining years more concisely
# ═══════════════════════════════════════════════════════════════════════════════
# 2022 sets
# ═══════════════════════════════════════════════════════════════════════════════
S22 = [
    ("2022 Topps Series 1 Baseball", "Baseball", "MLB", "Standard", "2022"),
    ("2022 Topps Series 1 Baseball First Edition", "Baseball", "MLB", "Standard", "2022"),
    ("2022 Topps Series 2 Baseball", "Baseball", "MLB", "Standard", "2022"),
    ("2022 Topps 3D Baseball", "Baseball", "MLB", "Standard", "2022"),
    ("2022 Topps Allen & Ginter", "Baseball", "MLB", "Standard", "2022"),
    ("2022 Topps Archives Baseball", "Baseball", "MLB", "Standard", "2022"),
    ("2022 Topps Archives Signature Series Active Edition", "Baseball", "MLB", "Standard", "2022"),
    ("2022 Topps Archives Signature Baseball Retired Edition", "Baseball", "MLB", "Standard", "2022"),
    ("2022 Topps Archives Snapshots Baseball", "Baseball", "MLB", "Standard", "2022"),
    ("2021 Topps Big League Baseball", "Baseball", "MLB", "Standard", "2021"),
    ("2022 Topps Bowman Baseball", "Baseball", "MLB", "Standard", "2022"),
    ("2022 Topps Bowman Chrome Baseball", "Baseball", "MLB", "Chrome", "2022"),
    ("2022 Topps Bowman Chrome Mega Box", "Baseball", "MLB", "Chrome", "2022"),
    ("2022 Topps Bowman Chrome Sapphire", "Baseball", "MLB", "Sapphire", "2022"),
    ("2022 Topps Bowman Chrome X", "Baseball", "MLB", "Chrome", "2022"),
    ("2022 Topps Bowman Draft", "Baseball", "MLB", "Standard", "2022"),
    ("2022 Topps Bowman Draft 1st Edition", "Baseball", "MLB", "Standard", "2022"),
    ("2022 Topps Bowman Draft Sapphire", "Baseball", "MLB", "Sapphire", "2022"),
    ("2022 Topps Bowman Platinum Baseball", "Baseball", "MLB", "Standard", "2022"),
    ("2022 Topps Bowman Sterling Baseball", "Baseball", "MLB", "Standard", "2022"),
    ("2021-22 Topps Bowman University Basketball", "Basketball", "NCAA", "Standard", "2021-22"),
    ("2021-22 Topps Bowman University Football", "Football", "NCAA", "Standard", "2021-22"),
    ("2022 Topps Bowman First Edition", "Baseball", "MLB", "Standard", "2022"),
    ("2022 Topps Bowman Sapphire", "Baseball", "MLB", "Sapphire", "2022"),
    ("2022 Brooklyn Collection", "Baseball", "MLB", "Standard", "2022"),
    ("2022 Topps Bundesliga", "Soccer", "Bundesliga", "Standard", "2022"),
    ("2022 Topps Bundesliga Chrome", "Soccer", "Bundesliga", "Chrome", "2022"),
    ("2022 Topps Bundesliga Chrome Sapphire", "Soccer", "Bundesliga", "Sapphire", "2022"),
    ("2021-22 Topps Bundesliga Finest", "Soccer", "Bundesliga", "Standard", "2021-22"),
    ("2022 Bowman Chrome Road to UEFA Under-21 European Championship", "Soccer", "UEFA", "Chrome", "2022"),
    ("2022 Topps Bundesliga Tier One", "Soccer", "Bundesliga", "Standard", "2022"),
    ("2021-22 Topps Bundesliga Stadium Chrome", "Soccer", "Bundesliga", "Chrome", "2021-22"),
    ("2022 Topps Chrome Baseball", "Baseball", "MLB", "Chrome", "2022"),
    ("2022 Topps Chrome Baseball Ben Baller Edition", "Baseball", "MLB", "Chrome", "2022"),
    ("2022 Topps Chrome Black Baseball", "Baseball", "MLB", "Chrome", "2022"),
    ("2022 Topps Chrome Logofractor Edition", "Baseball", "MLB", "Chrome", "2022"),
    ("2021 Topps Chrome Platinum Anniversary Baseball", "Baseball", "MLB", "Chrome", "2021"),
    ("2022 Topps Chrome Sapphire Baseball", "Baseball", "MLB", "Sapphire", "2022"),
    ("2022 Topps Chrome Updates Baseball", "Baseball", "MLB", "Chrome", "2022"),
    ("2022 Topps Chrome Updates Sapphire", "Baseball", "MLB", "Sapphire", "2022"),
    ("2021-22 Topps Complete Set Baseball", "Baseball", "MLB", "Standard", "2021-22"),
    ("2022 Topps Cosmic Chrome", "Baseball", "MLB", "Chrome", "2022"),
    ("2022 Topps Clearly Authentic Baseball", "Baseball", "MLB", "Standard", "2022"),
    ("2022 Topps Definitive Collection Baseball", "Baseball", "MLB", "Premium", "2022"),
    ("2022 Topps Diamond Icons", "Baseball", "MLB", "Premium", "2022"),
    ("2022 Dynamic Duals", "Baseball", "MLB", "Standard", "2022"),
    ("2021 Topps Finest Basketball", "Basketball", "NBA", "Standard", "2021"),
    ("2022 Topps Finest Baseball", "Baseball", "MLB", "Standard", "2022"),
    ("2022 Topps Fire Baseball", "Baseball", "MLB", "Standard", "2022"),
    ("2022 Topps Five Star Baseball", "Baseball", "MLB", "Premium", "2022"),
    ("2022 Topps Formula 1", "Racing", "F1", "Standard", "2022"),
    ("2021 Topps Formula 1", "Racing", "F1", "Standard", "2021"),
    ("2021 Topps Formula 1 Chrome", "Racing", "F1", "Chrome", "2021"),
    ("2022 Topps Formula 1 Chrome", "Racing", "F1", "Chrome", "2022"),
    ("2022 Topps Formula 1 Chrome Lite", "Racing", "F1", "Chrome", "2022"),
    ("2021 Topps Formula 1 Chrome Sapphire", "Racing", "F1", "Sapphire", "2021"),
    ("2022 Topps Formula 1 Chrome Sapphire", "Racing", "F1", "Sapphire", "2022"),
    ("2021 Topps Formula 1 Dynasty", "Racing", "F1", "Premium", "2021"),
    ("2022 Topps Gallery Baseball", "Baseball", "MLB", "Standard", "2022"),
    ("2022 Topps Gilded Collection", "Baseball", "MLB", "Standard", "2022"),
    ("2021 Topps GPK Chrome", "Entertainment", "GPK", "Chrome", "2021"),
    ("2022 Topps GPK Chrome", "Entertainment", "GPK", "Chrome", "2022"),
    ("2021 Topps GPK Chrome Sapphire", "Entertainment", "GPK", "Sapphire", "2021"),
    ("2022 Topps GPK Chrome Sapphire", "Entertainment", "GPK", "Sapphire", "2022"),
    ("2022 Topps GPK Series 1 Bookworms", "Entertainment", "GPK", "Standard", "2022"),
    ("2022 Topps GPK Taste Buds 2", "Entertainment", "GPK", "Standard", "2022"),
    ("2022 Topps GQ Baseball", "Baseball", "MLB", "Standard", "2022"),
    ("2022 Topps Heritage Baseball", "Baseball", "MLB", "Standard", "2022"),
    ("2022 Topps Heritage High Number Baseball", "Baseball", "MLB", "Standard", "2022"),
    ("2022 Topps Heritage MiLB Baseball", "Baseball", "MLB", "Standard", "2022"),
    ("2022 Topps Holiday Mega Box", "Baseball", "MLB", "Standard", "2022"),
    ("2022 Topps Inception Baseball", "Baseball", "MLB", "Standard", "2022"),
    ("2022 International Trading Card Day", "Baseball", "MLB", "Standard", "2022"),
    ("2022 Topps Luminaries", "Baseball", "MLB", "Standard", "2022"),
    ("2022 Topps MetaZoo Wilderness", "Entertainment", None, "Standard", "2022"),
    ("2022 Topps Mini Baseball", "Baseball", "MLB", "Standard", "2022"),
    ("2022 Topps MLS", "Soccer", "MLS", "Standard", "2022"),
    ("2022 Topps MLS Chrome", "Soccer", "MLS", "Chrome", "2022"),
    ("2022 Topps MLS Finest", "Soccer", "MLS", "Standard", "2022"),
    ("2022 Topps Museum Collection", "Baseball", "MLB", "Standard", "2022"),
    ("2022 National Sports Collectors Convention", "Baseball", "MLB", "Standard", "2022"),
    ("2022-23 Topps NHL Sticker Album", "Hockey", "NHL", "Standard", "2022-23"),
    ("2022 Topps Opening Day", "Baseball", "MLB", "Standard", "2022"),
    ("2021-22 Topps Overtime Elite Chrome Basketball", "Basketball", None, "Chrome", "2021-22"),
    ("2021-22 Topps Overtime Elite Inception", "Basketball", None, "Standard", "2021-22"),
    ("2022 Topps PLL Lacrosse", "Other", None, "Standard", "2022"),
    ("2022 Topps Pristine", "Baseball", "MLB", "Premium", "2022"),
    ("2022 Topps Pro Debut", "Baseball", "MLB", "Standard", "2022"),
    ("2022 Topps Rip Baseball", "Baseball", "MLB", "Standard", "2022"),
    ("2022 Topps Stadium Club Baseball", "Baseball", "MLB", "Standard", "2022"),
    ("2021 Topps Star Wars Book of Boba Fett", "Entertainment", "Star Wars", "Standard", "2021"),
    ("2021 Topps Star Wars Bounty Hunters", "Entertainment", "Star Wars", "Standard", "2021"),
    ("2022 Topps Star Wars Chrome Black", "Entertainment", "Star Wars", "Chrome", "2022"),
    ("2022 Topps Star Wars Chrome Sapphire", "Entertainment", "Star Wars", "Sapphire", "2022"),
    ("2022 Topps Star Wars Finest", "Entertainment", "Star Wars", "Standard", "2022"),
    ("2022 Topps Star Wars Galaxy Chrome", "Entertainment", "Star Wars", "Chrome", "2022"),
    ("2021 Topps Star Wars Masterwork", "Entertainment", "Star Wars", "Standard", "2021"),
    ("2022 Topps Star Wars Mandalorian Chrome", "Entertainment", "Star Wars", "Chrome", "2022"),
    ("2022 Topps Sterling Baseball", "Baseball", "MLB", "Standard", "2022"),
    ("2022 Topps Tier One", "Baseball", "MLB", "Standard", "2022"),
    ("2022 Topps Tribute", "Baseball", "MLB", "Standard", "2022"),
    ("2022 Topps Triple Threads Baseball", "Baseball", "MLB", "Standard", "2022"),
    ("2021-22 Topps UEFA Champions League", "Soccer", "UEFA", "Standard", "2021-22"),
    ("2022 Topps UEFA Champions League Chrome", "Soccer", "UEFA", "Chrome", "2022"),
    ("2021-22 Topps UEFA Champions League Chrome Sapphire", "Soccer", "UEFA", "Sapphire", "2021-22"),
    ("2022 Topps UEFA Champions League Finest", "Soccer", "UEFA", "Standard", "2022"),
    ("2021-22 Topps UEFA Champions League Finest Flashbacks", "Soccer", "UEFA", "Standard", "2021-22"),
    ("2021-22 Topps UEFA Champions League First Edition", "Soccer", "UEFA", "Standard", "2021-22"),
    ("2021-22 Topps UEFA Champions League Inception", "Soccer", "UEFA", "Standard", "2021-22"),
    ("2022 Topps UEFA Champions League Museum Collection", "Soccer", "UEFA", "Standard", "2022"),
    ("2022 Topps UEFA Champions League Stadium Club", "Soccer", "UEFA", "Standard", "2022"),
    ("2021-22 Topps UCL Merlin Collection", "Soccer", "UEFA", "Standard", "2021-22"),
    ("2022 Topps UEFA Women's Champions League Chrome", "Soccer", "UEFA", "Chrome", "2022"),
    ("2022 Topps Update Baseball", "Baseball", "MLB", "Standard", "2022"),
    ("2021 Topps WWE Women's Division", "Wrestling", "WWE", "Standard", "2021"),
]
for s in S22:
    add_set(*s)

# 2021, 2020, 2019, 2018 — insert all remaining in bulk
# Due to context limits, I'll handle these with a compact approach
REMAINING = [
    # 2021
    ("2021 Allen & Ginter", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Allen & Ginter Chrome", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Topps All-Star Rookie Cup", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Ginter X", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Archives", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Archive Signature Series Active Players Edition", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Archive Signature Series Retired Players Edition", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Archive Snapshots", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Aoki x UEFA Chrome", "Soccer", "UEFA", "Chrome", "2021"),
    ("2021 Ben Baller Chrome Baseball", "Baseball", "MLB", "Chrome", "2021"),
    ("2021 Bowman Sapphire Baseball", "Baseball", "MLB", "Sapphire", "2021"),
    ("2021 Bowman Sterling Baseball", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Bowman Baseball", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Bowman Best Baseball", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Bowman Draft Baseball", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Bowman Chrome Baseball", "Baseball", "MLB", "Chrome", "2021"),
    ("2021 Bowman Chrome X", "Baseball", "MLB", "Chrome", "2021"),
    ("2021 Bowman Chrome MegaBox Baseball", "Baseball", "MLB", "Chrome", "2021"),
    ("2021 Bowman Heritage", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Bowman Inception", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Bowman First Edition", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Bowman Platinum", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Bowman Transcendent Baseball", "Baseball", "MLB", "Premium", "2021"),
    ("2021 Brooklyn Collection Baseball", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Bundesliga Chrome", "Soccer", "Bundesliga", "Chrome", "2021"),
    ("2021 Bundesliga Tier One", "Soccer", "Bundesliga", "Standard", "2021"),
    ("2021 Topps Chrome Updates Sapphire", "Baseball", "MLB", "Sapphire", "2021"),
    ("2021 Topps Chrome Baseball", "Baseball", "MLB", "Chrome", "2021"),
    ("2021 Topps Chrome Baseball Sapphire Edition", "Baseball", "MLB", "Sapphire", "2021"),
    ("2021 Topps Chrome Black", "Baseball", "MLB", "Chrome", "2021"),
    ("2020 Topps Definitive Baseball", "Baseball", "MLB", "Premium", "2020"),
    ("2020 Topps Diamond Icons Baseball", "Baseball", "MLB", "Premium", "2020"),
    ("2020 Topps Dynasty Formula 1", "Racing", "F1", "Premium", "2020"),
    ("2021 Topps Dynasty Baseball", "Baseball", "MLB", "Premium", "2021"),
    ("2021 Topps Dynamic Duals", "Baseball", "MLB", "Standard", "2021"),
    ("2020 Topps Finest Baseball", "Baseball", "MLB", "Standard", "2020"),
    ("2021 Topps Finest Flashbacks Baseball", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Topps Five Star Baseball", "Baseball", "MLB", "Premium", "2021"),
    ("2020 Topps Formula 1 Chrome", "Racing", "F1", "Chrome", "2020"),
    ("2021 Topps Gallery Baseball", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Gold Label Baseball", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Topps GPK Series 1", "Entertainment", "GPK", "Standard", "2021"),
    ("2021 Gypsy Queen", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Heritage Baseball", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Heritage Minor League Baseball", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Heritage High Number Baseball", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Holiday Baseball", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Inception Baseball", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Luminaries Baseball", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Topps x Mantle", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Topps MetaZoo", "Entertainment", None, "Standard", "2021"),
    ("2021 Topps MLS", "Soccer", "MLS", "Standard", "2021"),
    ("2021 Topps On-Demand MLS Playoff Set", "Soccer", "MLS", "Standard", "2021"),
    ("2021 Topps MLS Chrome", "Soccer", "MLS", "Chrome", "2021"),
    ("2021 Topps MLS Chrome Sapphire", "Soccer", "MLS", "Sapphire", "2021"),
    ("2021 Topps Museum Baseball", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Topps NHL Stickers", "Hockey", "NHL", "Standard", "2021"),
    ("2021 Opening Day Baseball", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Olympics", "Other", None, "Standard", "2021"),
    ("2021 Topps ESPN 30for30 Once Upon A Time In Queens", "Other", None, "Standard", "2021"),
    ("2021 Topps Pro Debut", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Topps Rip", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Topps Series 1 Baseball", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Topps Series 2 Baseball", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Topps Star Wars Battle Plans", "Entertainment", "Star Wars", "Standard", "2021"),
    ("2021 Topps Star Wars Signature Series", "Entertainment", "Star Wars", "Standard", "2021"),
    ("2021 Topps Star Wars Chrome Galaxy", "Entertainment", "Star Wars", "Chrome", "2021"),
    ("2021 Topps Star Wars Chrome Legacy", "Entertainment", "Star Wars", "Chrome", "2021"),
    ("2021 Topps Star Wars Stellar Signatures", "Entertainment", "Star Wars", "Standard", "2021"),
    ("2021 Topps Sterling Baseball", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Topps Stadium Club Chrome", "Baseball", "MLB", "Chrome", "2021"),
    ("2021 Topps Tier One Baseball", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Topps Transcendent", "Baseball", "MLB", "Premium", "2021"),
    ("2021 Topps Transcendent HOF", "Baseball", "MLB", "Premium", "2021"),
    ("2021 Topps Tribute Baseball", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Topps Triple Threads Baseball", "Baseball", "MLB", "Standard", "2021"),
    ("2021 Topps Updates Baseball", "Baseball", "MLB", "Standard", "2021"),
    ("2021 UEFA Finest", "Soccer", "UEFA", "Standard", "2021"),
    ("2021 UEFA Merlin", "Soccer", "UEFA", "Standard", "2021"),
    ("2021 UEFA Museum", "Soccer", "UEFA", "Standard", "2021"),
    ("2021 UEFA Chrome Sapphire", "Soccer", "UEFA", "Sapphire", "2021"),
    ("2021 Topps UEFA Champions League Stadium Club Chrome", "Soccer", "UEFA", "Chrome", "2021"),
    ("2021 WWE", "Wrestling", "WWE", "Standard", "2021"),
    ("2020 WWE Chrome", "Wrestling", "WWE", "Chrome", "2020"),
    ("2021 WWE Heritage", "Wrestling", "WWE", "Standard", "2021"),
    ("2020 WWE Fully Loaded", "Wrestling", "WWE", "Standard", "2020"),
    ("2021 WWE Fully Loaded", "Wrestling", "WWE", "Standard", "2021"),
    ("2020 WWE Womens Division", "Wrestling", "WWE", "Standard", "2020"),
    ("2021 Topps WWE NXT", "Wrestling", "WWE", "Standard", "2021"),
    ("2021 Topps WWE Transcendent", "Wrestling", "WWE", "Premium", "2021"),
    # 2020
    ("2020 Transcendant Collection", "Baseball", "MLB", "Premium", "2020"),
    ("2020 Allen & Ginter Baseball", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Allen & Ginter Chrome Baseball", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Archives Baseball", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Big League Baseball", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Bowman Baseball First Edition", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Bowman Baseball", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Bowman Chrome Baseball", "Baseball", "MLB", "Chrome", "2020"),
    ("2020 Bowman Draft Baseball", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Bowman Draft Baseball Sapphire", "Baseball", "MLB", "Sapphire", "2020"),
    ("2020 Bowman Transcendent Baseball", "Baseball", "MLB", "Premium", "2020"),
    ("2020 Bowman Platinum Baseball", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Bowman Sterling Baseball", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Bundesliga Museum", "Soccer", "Bundesliga", "Standard", "2020"),
    ("2020 Topps Archives Signature Series", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Topps Clearly Authentic", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Topps Chrome", "Baseball", "MLB", "Chrome", "2020"),
    ("2020 Topps Chrome Black Edition", "Baseball", "MLB", "Chrome", "2020"),
    ("2020 Topps Definitive Collection Baseball", "Baseball", "MLB", "Premium", "2020"),
    ("2020 Topps Dynasty Baseball", "Baseball", "MLB", "Premium", "2020"),
    ("2020 Topps Finest Baseball", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Topps Finest Flashbacks Baseball", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Topps Fire", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Topps Five Star Baseball", "Baseball", "MLB", "Premium", "2020"),
    ("2020 Topps GPK Series 2", "Entertainment", "GPK", "Standard", "2020"),
    ("2020 Topps GPK Chrome", "Entertainment", "GPK", "Chrome", "2020"),
    ("2020 Topps Gold Label Baseball", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Topps Heritage Baseball", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Topps Heritage Minor League Baseball", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Topps Inception Baseball", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Topps Baseball Series 1", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Topps Baseball Series 2", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Topps Luminaries Baseball", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Topps Museum Collection Baseball", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Topps MLS", "Soccer", "MLS", "Standard", "2020"),
    ("2020 NHL Stickers", "Hockey", "NHL", "Standard", "2020"),
    ("2020 Topps Opening Day Baseball", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Pro Debut Baseball", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Topps Sterling Baseball", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Topps Stadium Club Chrome", "Baseball", "MLB", "Chrome", "2020"),
    ("2020 Topps Transcendent Baseball Hall of Fame", "Baseball", "MLB", "Premium", "2020"),
    ("2020 Topps Tribute Baseball", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Topps Triple Threads Baseball", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Topps Updates Baseball", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Star Wars Black & White", "Entertainment", "Star Wars", "Standard", "2020"),
    ("2020 Star Wars Chrome", "Entertainment", "Star Wars", "Chrome", "2020"),
    ("2020 Star Wars Mandalorian The Journey of the Child", "Entertainment", "Star Wars", "Standard", "2020"),
    ("2020 Star Wars Masterwork", "Entertainment", "Star Wars", "Standard", "2020"),
    ("2020 Star Wars Series 2", "Entertainment", "Star Wars", "Standard", "2020"),
    ("2020 Star Wars Stellar Signatures", "Entertainment", "Star Wars", "Standard", "2020"),
    ("2020 MLB Stickers", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Topps UEFA Museum Collection", "Soccer", "UEFA", "Standard", "2020"),
    ("2020 Topps UEFA Chrome Sapphire", "Soccer", "UEFA", "Sapphire", "2020"),
    ("2020 UFC", "MMA", "UFC", "Standard", "2020"),
    ("2020 UFC Knockout", "MMA", "UFC", "Standard", "2020"),
    ("2020 UFC Signatures", "MMA", "UFC", "Standard", "2020"),
    ("2020 WWE Chrome", "Wrestling", "WWE", "Chrome", "2020"),
    ("2020 WWE Finest", "Wrestling", "WWE", "Standard", "2020"),
    ("2020 WWE Road to WrestleMania", "Wrestling", "WWE", "Standard", "2020"),
    ("2020 WWE Transcendent", "Wrestling", "WWE", "Premium", "2020"),
    # 2020 online exclusives
    ("2020 Allen & Ginter X", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Archives Snapshots", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Bowman Prospect Pool", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Ben Baller Chrome Edition", "Baseball", "MLB", "Chrome", "2020"),
    ("2020 Brooklyn Collection 582 Member Exclusive", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Topps Chrome Sapphire Edition", "Baseball", "MLB", "Sapphire", "2020"),
    ("2020 Topps RIP", "Baseball", "MLB", "Standard", "2020"),
    ("2020 MLB 3D", "Baseball", "MLB", "Standard", "2020"),
    ("2020 MLB Summer Camp Wave 1", "Baseball", "MLB", "Standard", "2020"),
    ("2020 MLB Summer Camp Wave 2", "Baseball", "MLB", "Standard", "2020"),
    ("2020 MLB Summer Camp Wave 3", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Topps T206 Wave 1", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Topps T206 Wave 2", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Topps T206 Wave 3", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Topps T206 Wave 4", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Topps Total Wave 1", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Topps Total Wave 2", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Topps Total Wave 3", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Topps Total Wave 4", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Topps Total Wave 5", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Topps Total Wave 6", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Topps Total Wave 7", "Baseball", "MLB", "Standard", "2020"),
    ("2020 Topps Total Wave 8", "Baseball", "MLB", "Standard", "2020"),
    # 2019
    ("2019 Art of TMNT", "Entertainment", None, "Standard", "2019"),
    ("2019 Topps Allen & Ginter Baseball", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Topps Alliance of American Football", "Football", None, "Standard", "2019"),
    ("2019 Topps Archives Baseball", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Topps Archives Signature Series Active Player", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Topps Archives Signature Series Retired Player", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Bowman Best Baseball", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Bowman Chrome Baseball", "Baseball", "MLB", "Chrome", "2019"),
    ("2019 Bowman Draft Baseball", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Bowman Mega Box Baseball", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Bowman Baseball", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Bowman Sterling Baseball", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Topps Chrome Mega Baseball", "Baseball", "MLB", "Chrome", "2019"),
    ("2019 Topps Clearly Authentic Baseball", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Topps Dynasty Baseball", "Baseball", "MLB", "Premium", "2019"),
    ("2019 Topps Gallery Baseball", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Topps Baseball Gypsy Queen", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Topps Heritage Baseball", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Topps Heritage High Number Baseball", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Topps Heritage Minor League Baseball", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Topps High Tek Baseball", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Topps Holiday Mega Box Baseball", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Topps Baseball Inception", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Topps Baseball Series One", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Topps Baseball Series 2", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Topps Baseball Stadium Club", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Topps Baseball Opening Day", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Topps Big League Baseball", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Bowman Platinum Baseball", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Topps Bundesliga Chrome", "Soccer", "Bundesliga", "Chrome", "2019"),
    ("2019 Topps Chrome Baseball", "Baseball", "MLB", "Chrome", "2019"),
    ("2019 Topps Definitive Collection Baseball", "Baseball", "MLB", "Premium", "2019"),
    ("2019 Topps Diamond Icons Baseball", "Baseball", "MLB", "Premium", "2019"),
    ("2019 Topps Finest Baseball", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Topps Fire Baseball", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Topps Five Star Baseball", "Baseball", "MLB", "Premium", "2019"),
    ("2019 Topps Garbage Pail Kids Horror-ible", "Entertainment", "GPK", "Standard", "2019"),
    ("2019 Topps Luminaries Baseball", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Topps MLB Sticker Collection", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Topps MLS", "Soccer", "MLS", "Standard", "2019"),
    ("2019 Topps Museum Collection Baseball", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Topps NHL Sticker Collection", "Hockey", "NHL", "Standard", "2019"),
    ("2019 Topps Pro Debut Baseball", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Topps Star Wars Chrome Legacy", "Entertainment", "Star Wars", "Chrome", "2019"),
    ("2019 Topps Star Wars Episode 9", "Entertainment", "Star Wars", "Standard", "2019"),
    ("2019 Topps Star Wars Journey to Episode 9", "Entertainment", "Star Wars", "Standard", "2019"),
    ("2019 Topps Star Wars Masterwork", "Entertainment", "Star Wars", "Standard", "2019"),
    ("2019 Topps Star Wars Skywalker Saga", "Entertainment", "Star Wars", "Standard", "2019"),
    ("2019 Topps Star Wars Stellar Signatures", "Entertainment", "Star Wars", "Standard", "2019"),
    ("2019 Topps Stranger Things Season 2", "Entertainment", None, "Standard", "2019"),
    ("2019 Topps Stranger Things Upside Down", "Entertainment", None, "Standard", "2019"),
    ("2019 Topps Tier One Baseball", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Topps Transcendent Collection", "Baseball", "MLB", "Premium", "2019"),
    ("2019 Topps Tribute Baseball", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Topps Triple Threads Baseball", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Topps Updates Baseball", "Baseball", "MLB", "Standard", "2019"),
    ("2019 Topps UFC Chrome", "MMA", "UFC", "Chrome", "2019"),
    ("2019 Topps UFC Knockout", "MMA", "UFC", "Standard", "2019"),
    ("2019 Topps UFC Museum", "MMA", "UFC", "Standard", "2019"),
    ("2019 Topps WWE Money in the Bank", "Wrestling", "WWE", "Standard", "2019"),
    ("2019 Topps WWE Road to WrestleMania", "Wrestling", "WWE", "Standard", "2019"),
    ("2019 Topps WWE Undisputed", "Wrestling", "WWE", "Standard", "2019"),
    ("2019 Topps WWE Transcendent Collection", "Wrestling", "WWE", "Premium", "2019"),
    ("2019 Topps WWE Raw", "Wrestling", "WWE", "Standard", "2019"),
    ("2019 Topps WWE Smackdown", "Wrestling", "WWE", "Standard", "2019"),
    ("2019 Topps WWE SummerSlam", "Wrestling", "WWE", "Standard", "2019"),
    ("2019 Topps WWE Women's Division", "Wrestling", "WWE", "Standard", "2019"),
    ("2018-19 Topps Finest UEFA Champions League Soccer", "Soccer", "UEFA", "Standard", "2018-19"),
    ("2018-19 Topps UEFA Champions League Chrome", "Soccer", "UEFA", "Chrome", "2018-19"),
    ("2019 Topps UEFA Champions League Museum Collection", "Soccer", "UEFA", "Standard", "2019"),
    # 2018
    ("2018 Bowman Baseball", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Bowman Baseball Mega Box", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Bowman Chrome Baseball", "Baseball", "MLB", "Chrome", "2018"),
    ("2018 Bowman Draft Baseball", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Bowman High Tek Baseball", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Bowman's Best Baseball", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Topps Allen & Ginter Baseball", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Topps Allen & Ginter X Baseball", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Topps Archives Baseball Hobby", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Topps Archives Baseball Retail", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Topps Archives Signature Series Active Player Ed", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Topps Archives Signature Series Retired Player Ed", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Topps Archives Snapshots Baseball", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Topps Baseball Series One", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Topps Baseball Series Two", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Topps Baseball Update Series", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Topps Big League Baseball", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Topps Chrome Baseball", "Baseball", "MLB", "Chrome", "2018"),
    ("2018 Topps Clearly Authentic Baseball", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Topps Definitive Collection Baseball", "Baseball", "MLB", "Premium", "2018"),
    ("2018 Topps Diamond Icons Baseball", "Baseball", "MLB", "Premium", "2018"),
    ("2018 Topps Dynasty Baseball", "Baseball", "MLB", "Premium", "2018"),
    ("2018 Topps Finest Baseball", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Topps Five Star Baseball", "Baseball", "MLB", "Premium", "2018"),
    ("2018 Topps Gallery Baseball", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Topps Garbage Pail Kids Hate the 80s", "Entertainment", "GPK", "Standard", "2018"),
    ("2018 Topps Garbage Pail Kids Horror-ible", "Entertainment", "GPK", "Standard", "2018"),
    ("2018 Topps Gold Label Baseball", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Topps Gypsy Queen Baseball", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Topps Heritage Baseball", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Topps Heritage High Number", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Topps Heritage Minor League Baseball", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Topps Inception Baseball", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Topps Luminaries Baseball", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Topps MLS", "Soccer", "MLS", "Standard", "2018"),
    ("2018 Topps Museum Collection", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Topps Opening Day Baseball", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Topps Premier League Gold", "Soccer", "EPL", "Standard", "2018"),
    ("2018 Topps Premier League Platinum", "Soccer", "EPL", "Standard", "2018"),
    ("2018 Topps Pro Debut Baseball", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Topps Solo A Star Wars Story", "Entertainment", "Star Wars", "Standard", "2018"),
    ("2018 Topps Stranger Things Season One", "Entertainment", None, "Standard", "2018"),
    ("2018 Topps Stadium Club Baseball", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Topps Stadium Club MLS", "Soccer", "MLS", "Standard", "2018"),
    ("2018 Topps Star Wars Archive Signatures", "Entertainment", "Star Wars", "Standard", "2018"),
    ("2018 Topps Star Wars A New Hope Black and White", "Entertainment", "Star Wars", "Standard", "2018"),
    ("2018 Topps Star Wars Finest", "Entertainment", "Star Wars", "Standard", "2018"),
    ("2018 Topps Star Wars Galactic Files", "Entertainment", "Star Wars", "Standard", "2018"),
    ("2018 Topps Star Wars Galaxy", "Entertainment", "Star Wars", "Standard", "2018"),
    ("2018 Topps Star Wars Masterwork", "Entertainment", "Star Wars", "Standard", "2018"),
    ("2018 Topps Stellar Signatures", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Topps Tier One Baseball", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Topps Transcendent Baseball", "Baseball", "MLB", "Premium", "2018"),
    ("2018 Topps Tribute Baseball", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Topps Triple Threads Baseball", "Baseball", "MLB", "Standard", "2018"),
    ("2018 Topps UFC Chrome", "MMA", "UFC", "Chrome", "2018"),
    ("2018 Topps UFC Knockout", "MMA", "UFC", "Standard", "2018"),
    ("2018 Topps UFC Museum Collection", "MMA", "UFC", "Standard", "2018"),
    ("2018 Topps US Olympics & Paralympics Hopefuls", "Other", None, "Standard", "2018"),
    ("2018 Topps WWE", "Wrestling", "WWE", "Standard", "2018"),
    ("2018 Topps WWE Heritage", "Wrestling", "WWE", "Standard", "2018"),
    ("2018 Topps WWE Legends", "Wrestling", "WWE", "Standard", "2018"),
    ("2018 Topps WWE NXT", "Wrestling", "WWE", "Standard", "2018"),
    ("2018 Topps WWE Road to Wrestlemania", "Wrestling", "WWE", "Standard", "2018"),
    ("2018 Topps WWE Then Now & Forever", "Wrestling", "WWE", "Standard", "2018"),
    ("2018 Topps WWE Undisputed", "Wrestling", "WWE", "Standard", "2018"),
    ("2018 Topps WWE Womens Division", "Wrestling", "WWE", "Standard", "2018"),
    ("2018-19 Topps Champions League Museum Collection", "Soccer", "UEFA", "Standard", "2018-19"),
    ("2018-19 Topps Chrome UEFA Champions League", "Soccer", "UEFA", "Chrome", "2018-19"),
    ("2018-19 Topps Chrome Premier League", "Soccer", "EPL", "Chrome", "2018-19"),
]
for s in REMAINING:
    add_set(*s)

conn.commit()
conn.close()
print(f"\nTotal added: {added}")
print(f"Skipped (duplicates): {skipped}")
print("Done!")
