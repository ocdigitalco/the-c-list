"""
Seed: 2025-26 Donruss Road to FIFA World Cup 26 — Part 3
Autograph sets: Beautiful Game Autographs, Beautiful Game Dual Autographs, Signature Series.
Usage: python3 scripts/seed_donruss_autographs.py
"""
import sqlite3, os, re

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA foreign_keys=ON")
cur = conn.cursor()

SET_ID = 836

def get_or_create_player(name):
    cur.execute("SELECT id FROM players WHERE set_id = ? AND name = ?", (SET_ID, name))
    row = cur.fetchone()
    if row: return row[0]
    cur.execute("INSERT INTO players (set_id, name, unique_cards, total_print_run, one_of_ones, insert_set_count) VALUES (?, ?, 0, 0, 0, 0)", (SET_ID, name))
    return cur.lastrowid

def get_is_id(name):
    row = cur.execute("SELECT id FROM insert_sets WHERE set_id = ? AND name = ?", (SET_ID, name)).fetchone()
    if not row: raise ValueError(f"Insert set '{name}' not found")
    return row[0]

def add_appearance(player_id, is_id, card_number, is_rookie=False, team=None):
    cur.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, ?, ?)",
                (player_id, is_id, card_number, int(is_rookie), team))
    return cur.lastrowid

def create_co_player(appearance_id, co_player_id):
    cur.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)",
                (appearance_id, co_player_id))

def add_cards(is_id, cards):
    for num, name, team in cards:
        pid = get_or_create_player(name)
        add_appearance(pid, is_id, num, False, team)

def add_dual_cards(is_id, cards):
    """cards = [(num, name1, team1, name2, team2), ...]"""
    for num, n1, t1, n2, t2 in cards:
        p1 = get_or_create_player(n1)
        p2 = get_or_create_player(n2)
        a1 = add_appearance(p1, is_id, num, False, t1)
        a2 = add_appearance(p2, is_id, num, False, t2)
        create_co_player(a1, p2)
        create_co_player(a2, p1)

# ─── BEAUTIFUL GAME AUTOGRAPHS ───────────────────────────────────
bga_id = get_is_id("Beautiful Game Autographs")
bga = [
    ("1","Lamine Yamal","Spain"),("2","David Ospina","Colombia"),("3","Erling Haaland","Norway"),
    ("5","Vanderson","Brazil"),("6","Will Smallbone","Republic of Ireland"),("8","Deniz Undav","Germany"),
    ("9","Gabriel Magalhaes","Brazil"),("10","Lovro Majer","Croatia"),("11","Heung-Min Son","Korea Republic"),
    ("12","Ademola Lookman","Nigeria"),("13","Aurelien Tchouameni","France"),("14","Warren Zaire-Emery","France"),
    ("15","Bradley Barcola","France"),("16","Jimmy Dunne","Republic of Ireland"),("17","Cavan Sullivan","United States"),
    ("18","Vitinha","Portugal"),("19","Cristian Romero","Argentina"),("20","Pedri","Spain"),
    ("21","Matty Cash","Poland"),("22","Nicola Zalewski","Poland"),("23","Giuliano Simeone","Argentina"),
    ("24","Noah Okafor","Switzerland"),("25","John McGinn","Scotland"),("26","Inaki Williams","Ghana"),
    ("27","Richard Rios","Colombia"),("29","Pape Matar Sarr","Senegal"),("30","Cesar Huerta","Mexico"),
    ("31","Mario Balotelli","Italy"),("32","Luis Suarez","Uruguay"),("33","Jorge Campos","Mexico"),
    ("34","Rafael Marquez","Mexico"),("35","Carlos Tevez","Argentina"),("36","Angel Di Maria","Argentina"),
    ("37","Ledley King","England"),("38","Ronaldo","Brazil"),("39","Mario Yepes","Colombia"),
    ("40","Luis Figo","Portugal"),("42","John Obi Mikel","Nigeria"),("43","Manuel Neuer","Germany"),
    ("44","Pavel Pardo","Mexico"),("45","Savo Milosevic","Serbia"),
]
add_cards(bga_id, bga)
print(f"  Beautiful Game Autographs: {len(bga)} cards")

# ─── BEAUTIFUL GAME DUAL AUTOGRAPHS ──────────────────────────────
bgd_id = get_is_id("Beautiful Game Dual Autographs")
bgd = [
    ("2","Harry Kane","England","Kyle Walker","England"),
    ("3","David Trezeguet","France","Jean-Pierre Papin","France"),
    ("4","Fernando Torres","Spain","Ferran Torres","Spain"),
    ("5","Bruno Fernandes","Portugal","Luis Figo","Portugal"),
    ("6","Assane Diao","Senegal","Pape Matar Sarr","Senegal"),
    ("7","Manuel Neuer","Germany","Sepp Maier","Germany"),
    ("8","Hugo Sanchez","Mexico","Luis Hernandez","Mexico"),
    ("9","Javier Mascherano","Argentina","Sergio Aguero","Argentina"),
    ("10","Gianluigi Buffon","Italy","Gianluigi Donnarumma","Italy"),
]
add_dual_cards(bgd_id, bgd)
print(f"  Beautiful Game Dual Autographs: {len(bgd)} dual cards ({len(bgd)*2} appearances)")

# ─── SIGNATURE SERIES ────────────────────────────────────────────
ss_id = get_is_id("Signature Series")
ss = [
    ("1","Lionel Messi","Argentina"),("2","George Hirst","Scotland"),("3","Trai Hume","Northern Ireland"),
    ("4","Kylian Mbappe","France"),("5","Arkadiusz Milik","Poland"),("7","William Saliba","France"),
    ("8","Christian Pulisic","United States"),("9","Karl-Heinz Riedle","Germany"),("10","Luis Palma","Honduras"),
    ("11","Shea Charles","Northern Ireland"),("12","Yunus Musah","United States"),("13","Emiliano Martinez","Argentina"),
    ("14","Harry Kane","England"),("15","Goncalo Ramos","Portugal"),("16","Robert Lewandowski","Poland"),
    ("17","Raul Jimenez","Mexico"),("18","Andi Zeqiri","Switzerland"),("19","Moses Simon","Nigeria"),
    ("20","Marcus Rashford","England"),("21","Alexis Vega","Mexico"),("22","Raoul Bellanova","Italy"),
    ("23","Ethan Galbraith","Northern Ireland"),("24","Pedro Porro","Spain"),("25","Omar Alderete","Paraguay"),
    ("26","Uriel Antuna","Mexico"),("27","Assane Diao","Senegal"),("28","Jhon Lucumi","Colombia"),
    ("29","Maximilian Beier","Germany"),("30","Billy Gilmour","Scotland"),("31","Martin Odegaard","Norway"),
    ("32","Brahim Diaz","Morocco"),("33","Antoine Semenyo","Ghana"),("34","Graeme Souness","Scotland"),
    ("35","Jamie Vardy","England"),("36","Jeffrey Schlupp","Ghana"),("37","Roy Keane","Republic of Ireland"),
    ("38","Nemanja Vidic","Serbia"),("39","Lothar Matthaus","Germany"),("40","Willian","Brazil"),
    ("41","Juan Camilo Zuniga","Colombia"),("42","Kaka","Brazil"),("43","Jay-Jay Okocha","Nigeria"),
    ("44","Freddie Ljungberg","Sweden"),("45","Edinson Cavani","Uruguay"),
]
add_cards(ss_id, ss)
print(f"  Signature Series: {len(ss)} cards")

# ─── Generate slugs for new players ──────────────────────────────
def slugify(text):
    s = text.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_]+', '-', s)
    return re.sub(r'-+', '-', s).strip('-')

cur.execute("SELECT id, name FROM players WHERE set_id = ? AND slug IS NULL", (SET_ID,))
new_players = cur.fetchall()
existing_slugs = set(r[0] for r in cur.execute("SELECT slug FROM players WHERE set_id = ? AND slug IS NOT NULL", (SET_ID,)).fetchall())

for pid, pname in new_players:
    slug = slugify(pname)
    if slug in existing_slugs:
        i = 2
        while f"{slug}-{i}" in existing_slugs: i += 1
        slug = f"{slug}-{i}"
    existing_slugs.add(slug)
    cur.execute("UPDATE players SET slug = ? WHERE id = ?", (slug, pid))

print(f"  Generated slugs for {len(new_players)} new players")

conn.commit()

# Stats
app_count = cur.execute("SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON pa.insert_set_id = i.id WHERE i.set_id = ?", (SET_ID,)).fetchone()[0]
player_count = cur.execute("SELECT COUNT(*) FROM players WHERE set_id = ?", (SET_ID,)).fetchone()[0]
auto_count = cur.execute("""
    SELECT COUNT(*) FROM player_appearances pa
    JOIN insert_sets i ON pa.insert_set_id = i.id
    WHERE i.set_id = ? AND (i.name LIKE '%Auto%' OR i.name LIKE '%Signature%')
""", (SET_ID,)).fetchone()[0]

print(f"\nDone! Set ID: {SET_ID}")
print(f"  Total players: {player_count}")
print(f"  Total appearances: {app_count}")
print(f"  Autograph appearances: {auto_count}")
conn.close()
