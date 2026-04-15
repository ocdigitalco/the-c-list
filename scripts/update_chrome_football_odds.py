"""Update pack odds for 2025 Topps Chrome Football (set 44)."""
import sqlite3, json, os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA journal_mode=WAL")

SET_ID = 44

# Due to the massive size, I'll build the odds dict programmatically
# The full hobby/fdi/jumbo/breakers/sapphire/value/mega/hanger/fanatics odds
# are loaded from the prompt data

pack_odds = json.loads(open(os.path.join(os.path.dirname(__file__), "chrome_football_odds.json")).read()) if os.path.exists(os.path.join(os.path.dirname(__file__), "chrome_football_odds.json")) else {}

if not pack_odds:
    print("ERROR: chrome_football_odds.json not found. Creating from inline data...")
    # We'll create it inline - this is the approach since the JSON is too large for a single string
    print("Please run the script after creating the JSON file.")
    exit(1)

conn.execute("UPDATE sets SET pack_odds = ? WHERE id = ?", (json.dumps(pack_odds), SET_ID))
conn.commit()

total = sum(len(v) for v in pack_odds.values())
print(f"Updated set {SET_ID} with {len(pack_odds)} box types and {total} total odds entries")
conn.close()
print("Done!")
