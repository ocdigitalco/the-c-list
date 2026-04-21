import sqlite3, json

db = sqlite3.connect('the-c-list.db')
cursor = db.execute("SELECT id, pack_odds FROM sets WHERE name LIKE '%Bowman%Basketball%' AND name LIKE '%2025%'")
row = cursor.fetchone()
set_id, pack_odds_json = row
pack_odds = json.loads(pack_odds_json)

replacements = {
    'Crystalized NBA': 'Crystallized NBA',
    'Crystalized NIL': 'Crystallized NIL',
    'Crystalized NBA Gold Crystal Refractor': 'Crystallized NBA Gold Crystal Refractor',
    'Crystalized NIL Gold Crystal Refractor': 'Crystallized NIL Gold Crystal Refractor',
    'Crystalized NBA Orange Crystal Refractor': 'Crystallized NBA Orange Crystal Refractor',
    'Crystalized NIL Orange Crystal Refractor': 'Crystallized NIL Orange Crystal Refractor',
    'Crystalized NBA Red Crystal Refractor': 'Crystallized NBA Red Crystal Refractor',
    'Crystalized NIL Red Crystal Refractor': 'Crystallized NIL Red Crystal Refractor',
    'Crystalized NBA SuperFractor': 'Crystallized NBA SuperFractor',
    'Crystalized NIL SuperFractor': 'Crystallized NIL SuperFractor',
}

for box_type, box_odds in pack_odds.items():
    for old_key, new_key in replacements.items():
        if old_key in box_odds:
            box_odds[new_key] = box_odds.pop(old_key)
            print(f"  [{box_type}] {old_key} -> {new_key}")

db.execute("UPDATE sets SET pack_odds = ? WHERE id = ?", (json.dumps(pack_odds), set_id))
db.commit()
print("Done.")
db.close()
