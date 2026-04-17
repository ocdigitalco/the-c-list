import sqlite3, json

db = sqlite3.connect('the-c-list.db')

cursor = db.execute("SELECT id, pack_odds FROM sets WHERE name LIKE '%Chrome%Football%' AND name LIKE '%2025 Topps%'")
row = cursor.fetchone()
set_id, pack_odds_json = row
pack_odds = json.loads(pack_odds_json)

new_hobby_entries = {
  "Kaiju Superfractor": "1:518,770",
  "Game Genies Superfractor": "1:230,565",
  "Tecmo Superfractor": "1:230,565",
  "Helix Superfractor": "1:188,644",
  "Let's Go Superfractor": "1:1,037,540",
  "Ultraviolet Superfractor": "1:345,847",
  "Lightning Leaders Superfractor": "1:345,847",
  "Shadow Etch Superfractor": "1:345,847",
  "Chrome Radiating Rookies Superfractor": "1:296,440",
  "Rookie Superfractor": "1:103,754",
  "Chrome Base Etch Variation Superfractor": "1:103,754",
  "Chrome Rookies Etch Variation Superfractor": "1:103,754",
  "1990 Topps Football Autographs Superfractor": "1:148,220",
  "Chromographs Superfractor": "1:207,508",
  "Future Stars Autographs Superfractor": "1:188,644",
  "Chrome Legends Autographs Superfractor": "1:172,924",
  "Hall Of Chrome Autographs Superfractor": "1:207,508",
  "Dual Autographs Superfractor": "1:415,016",
  "Rookie Variation Autographs Superfractor": "1:83,004",
  "Base Variation Autographs Superfractor": "1:115,283",
  "Topps Chrome Rookie Patch Autographs Superfractor": "1:122,064",
  "1975 Topps Superfractor": "1:207,508",
  "Future Stars Superfractor": "1:188,644",
  "Power Players Superfractor": "1:188,644",
  "All-Chrome Team Superfractor": "1:188,644",
  "Fortune 15 Superfractor": "1:138,339",
  "Legends Of The Gridiron Superfractor": "1:129,693",
  "Tecmo Autographs Superfractor": "1:259,385",
  "Base Image Variation Superfractor": "1:345,847",
  "Rookie Image Variation Superfractor": "1:518,770",
}

for key, value in new_hobby_entries.items():
  if key not in pack_odds.get('hobby', {}):
    pack_odds['hobby'][key] = value
    print(f"Added: {key} → {value}")
  else:
    print(f"Skipped (already exists): {key}")

db.execute("UPDATE sets SET pack_odds = ? WHERE id = ?", (json.dumps(pack_odds), set_id))
db.commit()
print(f"\nDone. Updated set ID {set_id}")
db.close()
