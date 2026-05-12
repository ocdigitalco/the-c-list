"""
Seed: 2026 Topps Chrome VeeFriends — Full checklist.
Base (200), inserts, relics, autographs, sketch cards, parallels, pack odds.
Usage: python3 scripts/seed_chrome_veefriends_2026.py
"""
import sqlite3, os, re, json

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
db = sqlite3.connect(DB_PATH)
db.execute("PRAGMA journal_mode=WAL")
db.execute("PRAGMA foreign_keys=ON")

# ─── Create Set ──────────────────────────────────────────────────────────────
box_config = json.dumps({
    "hobby": {
        "cards_per_pack": 4,
        "packs_per_box": 18,
        "boxes_per_case": None,
        "notes": "Per box: 72 cards total"
    }
})

db.execute("""
    INSERT INTO sets (name, sport, season, tier, slug, is_visible,
                      sample_image_url, release_date, box_config)
    VALUES ('2026 Topps Chrome VeeFriends', 'Entertainment', '2026', 'Chrome',
            '2026-topps-chrome-veefriends', 1,
            '/sets/2026-topps-chrome-veefriends.jpg', '2026-05-12', ?)
""", (box_config,))
SET_ID = db.execute("SELECT last_insert_rowid()").fetchone()[0]
print(f"Created set ID: {SET_ID}")

R = False  # No rookies in this set

def get_or_create(name):
    row = db.execute("SELECT id FROM players WHERE set_id = ? AND name = ?", (SET_ID, name)).fetchone()
    if row: return row[0]
    db.execute("INSERT INTO players (set_id, name, unique_cards, total_print_run, one_of_ones, insert_set_count) VALUES (?, ?, 0, 0, 0, 0)", (SET_ID, name))
    return db.execute("SELECT last_insert_rowid()").fetchone()[0]

def add_is(name):
    db.execute("INSERT INTO insert_sets (set_id, name) VALUES (?, ?)", (SET_ID, name))
    return db.execute("SELECT last_insert_rowid()").fetchone()[0]

def add_par(is_id, name, print_run=None):
    db.execute("INSERT INTO parallels (insert_set_id, name, print_run) VALUES (?, ?, ?)", (is_id, name, print_run))

def add_cards(is_id, cards):
    for num, name in cards:
        pid = get_or_create(name)
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, NULL)", (pid, is_id, str(num)))

def add_dual_cards(is_id, cards):
    for num, p1, p2 in cards:
        pid1 = get_or_create(p1)
        pid2 = get_or_create(p2)
        db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, NULL)", (pid1, is_id, str(num)))
        a1 = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        db.execute("INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?, ?)", (a1, pid2))

# ─── BASE SET (200 cards) ────────────────────────────────────────────────────
base_id = add_is("Base Set")

# Base parallels
for n, pr in [
    ("Refractor", None),("Aqua Raywave Refractor", None),("Pink Refractor", None),
    ("Blue Refractor", None),("VF Green Refractor", None),("Purple Refractor", None),
    ("Gold Refractor", None),("Pearl Refractor", None),("Orange Refractor", None),
    ("Black Wave Refractor", None),("Black Refractor", None),("Red Wave Refractor", None),
    ("Black Cat Refractor", None),("Red Refractor", None),("Superfractor", 1),
    # Sapphire exclusives
    ("Sapphire", None),("Gold Sapphire", None),("White Sapphire", None),
    ("Orange Sapphire", None),("Black Sapphire", None),("Red Sapphire", None),
    ("Padparadscha Sapphire", None),
    # Value exclusives
    ("Yellow Refractor", None),("Blast Off", None),
    # Mega exclusives
    ("X-Fractor", None),("Purple Mini-Diamond Refractor", None),
    ("Gold Mini-Diamond Refractor", None),("Orange Mini-Diamond Refractor", None),
    ("Black Mini-Diamond Refractor", None),("Red Mini-Diamond Refractor", None),
]:
    add_par(base_id, n, pr)
# Gary Vee Autograph Parallel modeled as a base parallel
add_par(base_id, "Gary Vee Autograph Parallel", None)
print(f"  Base Set: 31 parallels")

base_cards = [
    (1,"Cynical Cat"),(2,"Fearless Fairy"),(3,"Decisive Duck"),(4,"Thoughtful Three Horned Harpik"),
    (5,"Motivated Monster"),(6,"Versatile Viking"),(7,"Notorious Ninja"),(8,"Gary Bee"),
    (9,"Kind Warrior"),(10,"Rare Robot"),(11,"Adventurous Astronaut"),(12,"Mindful Minokawa"),
    (13,"Patient Pig"),(14,"Dialed In Dog"),(15,"Driven Dragon"),(16,"Gritty Ghost"),
    (17,"Accountable Ant"),(18,"Alert Ape"),(19,"Amiable Anchovy"),(20,"Amped Aye Aye"),
    (21,"Arbitraging Admiral"),(22,"Articulate Armadillo"),(23,"Aspiring Alpaca"),
    (24,"Authentic Anaconda"),(25,"Awesome African Civet"),(26,"Bad Intentions"),
    (27,"Bad-Ass Bulldog"),(28,"Balanced Beetle"),(29,"Bashful Blobfish"),
    (30,"Be The Bigger Person"),(31,"Jolly Jack-O"),(32,"Befuddled Burglar"),
    (33,"Big Game Bandicoot"),(34,"Boisterous Beaver"),(35,"Bombastic Baboon"),
    (36,"Boss Bobcat"),(37,"Brave Bison"),(38,"Brilliant Barb"),(39,"Bubbly Buzzard"),
    (40,"Bullish Bull"),(41,"Calm Clam"),(42,"Candid Clownfish"),(43,"Capable Caterpillar"),
    (44,"Caring Camel"),(45,"Charming Cheetah"),(46,"Cheerful Chipmunk"),
    (47,"Chill Chinchilla"),(48,"Clever Crocodile"),(49,"Common Sense Cow"),
    (50,"Compassionate Catfish"),(51,"Adaptable Alien"),(52,"Competitive Clown"),
    (53,"Confident Cobra"),(54,"Considerate Cowboy"),
    (55,"Very, Very, Very, Very, Lucky Black Cat"),(56,"Consistent Cougar"),
    (57,"Content Condor"),(58,"Conviction Cockroach"),(59,"Courageous Cockatoo"),
    (60,"Creative Crab"),(61,"Curious Crane"),(62,"Dapper Dachshund"),
    (63,"Dedicated Dragonfly"),(64,"Detail-Oriented Dumbo Octopus"),
    (65,"Determined Dolphin"),(66,"Resilient Red Devil"),(67,"Dope Dodo"),
    (68,"Dynamic Dinosaur"),(69,"Earnest Ermine"),(70,"Empathy Elephant"),
    (71,"Enamoured Emu"),(72,"Entrepreneur Elf"),(73,"Faithful Pheasant"),
    (74,"Flex'n Fox"),(75,"Focused Falcon"),(76,"Eager Eagle"),(77,"Forever Phoenix"),
    (78,"Forgiving Horned Frog"),(79,"Forthright Flamingo"),(80,"Gentle Giant"),
    (81,"Genuine Giraffe"),(82,"Gifted Gopher"),(83,"Gleeful Sugar Glider"),
    (84,"Glowing Glow Worm"),(85,"Gracious Goose"),(86,"Gracious Grasshopper"),
    (87,"Gracious Grizzly Bear"),(88,"Grateful Gar"),(89,"Gratitude Gorilla"),
    (90,"Happy Hermit Crab"),(91,"Hard-Working Wombat"),(92,"Headstrong Honey Badger"),
    (93,"Heart Trooper"),(94,"Helpful Hippo"),(95,"Honorable Olm"),(96,"Hot Shot Hornet"),
    (97,"Humble Hedgehog"),(98,"Humble Hummingbird"),(99,"Hungry Hammerhead"),
    (100,"Hustling Hamster"),(101,"Hype Horse"),(102,"Impeccable Inostranet"),
    (103,"Independent Inch Worm"),(104,"Intuitive Iguana"),(105,"Joyous Jellyfish"),
    (106,"Just Jackal"),(107,"Keen Kingfisher"),(108,"Kindred Kangaroo"),
    (109,"Knowing Gnome"),(110,"Legendary Lemur"),(111,"Ambitious Angel"),
    (112,"Likable Leopard"),(113,"Like A Sponge"),(114,"Lit Lamb"),
    (115,"Logical Lion"),(116,"Loyal Lobster"),(117,"Macho Manta Ray"),
    (118,"Macro Micro"),(119,"Magnanimous Maltese"),(120,"Meticulous Magpie"),
    (121,"Mint Mink"),(122,"Modest Moose"),(123,"Mojo Mouse"),(124,"Monday Mole"),
    (125,"Moral Monkey"),(126,"Noble Numbat"),(127,"Observant Oyster"),
    (128,"Offense Oriented Orangutan"),(129,"Optimistic Otter"),(130,"Organized Ostrich"),
    (131,"Outgoing Octopus"),(132,"Passionate Parrot"),(133,"Pea Salad"),
    (134,"Perfect Persian Cat"),(135,"Persistent Penguin"),(136,"Perspective Pigeon"),
    (137,"Persuasive Pigeon"),(138,"Polished Poodle"),(139,"Positive Porcupine"),
    (140,"Practical Peacock"),(141,"Productive Puffin"),(142,"Profound Possum"),
    (143,"Protective Panther"),(144,"Prudent Polar Bear"),(145,"Radical Rabbit"),
    (146,"Reliable Rat"),(147,"Respectful Racoon"),(148,"Responsive Ram"),
    (149,"Secure Sparrow"),(150,"Self-Aware Hare"),(151,"Selfless Sloth"),
    (152,"Sensible Sommelier"),(153,"Sensitive Centipede"),(154,"Sentimental Salamander"),
    (155,"Serious Sperm Whale"),(156,"Sharing Squirrel"),(157,"Shrewd Sheep"),
    (158,"Sincere Skunk"),(159,"Skilled Skeleton"),(160,"Slay'n Slug"),
    (161,"Spiffy Salmon"),(162,"Spontaneous Seahorse"),(163,"Steadfast Snake"),
    (164,"Stoic Slime"),(165,"Stunned Sun"),(166,"Sufficient Shrimp"),
    (167,"Suffocate Hate"),(168,"Swaggy Sea Lion"),(169,"Tasteful Malayan Tapir"),
    (170,"Tenacious Termite"),(171,"Tenacious Turkey"),(172,"The Oak Monster"),
    (173,"The World Has Plenty Of Love Start Listening To It"),(174,"Tidy Troll"),
    (175,"To The Moon Meerkat"),(176,"Tolerant Tortoise"),(177,"Tolerant Tuna"),
    (178,"Tough To Beat A Worm From The Dirt!"),(179,"Tranquil Toad"),
    (180,"Ponder It From All Angles"),(181,"Tremendous Tiger"),(182,"Truculent T-Rex"),
    (183,"Trusting Tarantula"),(184,"Turnt Tick"),(185,"Unwavering Urchin"),
    (186,"Vibe'n Vampire"),(187,"Warm Wolverine"),(188,"Well-Connected Werewolf"),
    (189,"Well-Rounded Warthog"),(190,"Whimsical Wolf"),(191,"Wild Wallaby"),
    (192,"Willful Wizard"),(193,"Wily Wild Boar"),(194,"Woke Walrus"),
    (195,"Yolo Yak"),(196,"You're Gonna Die Fly"),
    (197,"Your Poor Relationship With Time Is Your Biggest Vulnerability"),
    (198,"Zealous Zombie"),(199,"Zestful Zebra"),(200,"Last Glass Standing"),
]
add_cards(base_id, base_cards)
print(f"  Base Set: {len(base_cards)} cards")

# ─── INSERT SUBSETS ──────────────────────────────────────────────────────────

def add_subset(name, cards, parallels=None):
    is_id = add_is(name)
    if parallels:
        for pn, pr in parallels:
            add_par(is_id, pn, pr)
    add_cards(is_id, cards)
    print(f"  {name}: {len(cards)} cards, {len(parallels) if parallels else 0} parallels")
    return is_id

# Topps 1986
add_subset("Topps 1986 Base Set Variation", [
    ("TF-AA","Amped Aye Aye"),("TF-AU","Authentic Anaconda"),("TF-BA","Bad-Ass Bulldog"),
    ("TF-BB","Big Game Bandicoot"),("TF-CB","Considerate Cowboy"),("TF-CC","Consistent Cougar"),
    ("TF-DD","Determined Dolphin"),("TF-EE","Eager Eagle"),("TF-FF","Focused Falcon"),
    ("TF-FH","Forgiving Horned Frog"),("TF-GB","Gracious Grizzly Bear"),("TF-GG","Gentle Giant"),
    ("TF-GP","Gifted Gopher"),("TF-LL","Logical Lion"),("TF-NN","Noble Numbat"),
    ("TF-OO","Offense Oriented Orangutan"),("TF-PP","Protective Panther"),("TF-RB","Radical Rabbit"),
    ("TF-RR","Responsive Ram"),("TF-TG","Tremendous Tiger"),("TF-TT","Tenacious Turkey"),
    ("TF-VV","Versatile Viking"),("TF-WD","Tough To Beat A Worm From The Dirt!"),
    ("TF-WW","Warm Wolverine"),("TF-ZZ","Zestful Zebra"),
], [("Superfractor", 1)])

# Manga Speckle Set (100 cards)
manga_pars = [("Orange Speckle Refractor", None),("Purple Speckle Refractor", None),
              ("Red Speckle Refractor", None),("Black Speckle Refractor", None)]
manga_cards = [
    ("SSA-1","Thoughtful Three Horned Harpik"),("SSA-2","Motivated Monster"),("SSA-3","Gary Bee"),
    ("SSA-4","Kind Warrior"),("SSA-5","Driven Dragon"),("SSA-6","Gritty Ghost"),
    ("SSA-7","Accountable Ant"),("SSA-8","Amiable Anchovy"),("SSA-9","Arbitraging Admiral"),
    ("SSA-10","Aspiring Alpaca"),("SSA-11","Awesome African Civet"),("SSA-12","Bad Intentions"),
    ("SSA-13","Be The Bigger Person"),("SSA-14","Jolly Jack-O"),("SSA-15","Befuddled Burglar"),
    ("SSA-16","Big Game Bandicoot"),("SSA-17","Bombastic Baboon"),("SSA-18","Boss Bobcat"),
    ("SSA-19","Brave Bison"),("SSA-20","Brilliant Barb"),("SSA-21","Bubbly Buzzard"),
    ("SSA-22","Calm Clam"),("SSA-23","Candid Clownfish"),("SSA-24","Caring Camel"),
    ("SSA-25","Cheerful Chipmunk"),("SSA-26","Clever Crocodile"),("SSA-27","Compassionate Catfish"),
    ("SSA-28","Conviction Cockroach"),("SSA-29","Courageous Cockatoo"),("SSA-30","Curious Crane"),
    ("SSA-31","Dedicated Dragonfly"),("SSA-32","Detail-Oriented Dumbo Octopus"),
    ("SSA-33","Determined Dolphin"),("SSA-34","Earnest Ermine"),("SSA-35","Faithful Pheasant"),
    ("SSA-36","Flex'n Fox"),("SSA-37","Forever Phoenix"),("SSA-38","Gentle Giant"),
    ("SSA-39","Genuine Giraffe"),("SSA-40","Gleeful Sugar Glider"),("SSA-41","Gracious Grasshopper"),
    ("SSA-42","Grateful Gar"),("SSA-43","Gratitude Gorilla"),("SSA-44","Happy Hermit Crab"),
    ("SSA-45","Hard-Working Wombat"),("SSA-46","Helpful Hippo"),("SSA-47","Honorable Olm"),
    ("SSA-48","Hot Shot Hornet"),("SSA-49","Humble Hummingbird"),("SSA-50","Hungry Hammerhead"),
    ("SSA-51","Hype Horse"),("SSA-52","Independent Inch Worm"),("SSA-53","Intuitive Iguana"),
    ("SSA-54","Just Jackal"),("SSA-55","Keen Kingfisher"),("SSA-56","Kindred Kangaroo"),
    ("SSA-57","Knowing Gnome"),("SSA-58","Likable Leopard"),("SSA-59","Lit Lamb"),
    ("SSA-60","Loyal Lobster"),("SSA-61","Macho Manta Ray"),("SSA-62","Magnanimous Maltese"),
    ("SSA-63","Meticulous Magpie"),("SSA-64","Mint Mink"),("SSA-65","Modest Moose"),
    ("SSA-66","Mojo Mouse"),("SSA-67","Observant Oyster"),("SSA-68","Organized Ostrich"),
    ("SSA-69","Passionate Parrot"),("SSA-70","Pea Salad"),("SSA-71","Persistent Penguin"),
    ("SSA-72","Perspective Pigeon"),("SSA-73","Polished Poodle"),("SSA-74","Positive Porcupine"),
    ("SSA-75","Practical Peacock"),("SSA-76","Profound Possum"),("SSA-77","Reliable Rat"),
    ("SSA-78","Respectful Racoon"),("SSA-79","Responsive Ram"),("SSA-80","Self-Aware Hare"),
    ("SSA-81","Sentimental Salamander"),("SSA-82","Serious Sperm Whale"),("SSA-83","Sharing Squirrel"),
    ("SSA-84","Sincere Skunk"),("SSA-85","Spiffy Salmon"),("SSA-86","Steadfast Snake"),
    ("SSA-87","Stoic Slime"),("SSA-88","Swaggy Sea Lion"),("SSA-89","Tasteful Malayan Tapir"),
    ("SSA-90","The World Has Plenty Of Love Start Listening To It"),("SSA-91","Tolerant Tuna"),
    ("SSA-92","Truculent T-Rex"),("SSA-93","Turnt Tick"),("SSA-94","Well-Connected Werewolf"),
    ("SSA-95","Wily Wild Boar"),("SSA-96","Woke Walrus"),("SSA-97","Yolo Yak"),
    ("SSA-98","You're Gonna Die Fly"),
    ("SSA-99","Your Poor Relationship With Time Is Your Biggest Vulnerability"),
    ("SSA-100","Zealous Zombie"),
]
add_subset("Manga Speckle Set", manga_cards, manga_pars)

# Standard insert parallel ladder
std_insert_pars = [("VF Green Refractor", None),("Gold Refractor", None),("Orange Refractor", None),
                    ("Black Refractor", None),("Red Refractor", None),("Superfractor", 1)]

# Chalkboard
add_subset("Chalkboard", [
    ("C-1","Cynical Cat"),("C-2","Patient Pig"),("C-3","Dialed In Dog"),
    ("C-4","Articulate Armadillo"),("C-5","Boisterous Beaver"),("C-6","Bullish Bull"),
    ("C-7","Charming Cheetah"),("C-8","Common Sense Cow"),("C-9","Skilled Skeleton"),
    ("C-10","Creative Crab"),("C-11","Dope Dodo"),("C-12","Enamoured Emu"),
    ("C-13","Entrepreneur Elf"),("C-14","Flex'n Fox"),("C-15","Genuine Giraffe"),
    ("C-16","Gracious Goose"),("C-17","Productive Puffin"),("C-18","Like A Sponge"),
    ("C-19","Outgoing Octopus"),("C-20","Moral Monkey"),
], std_insert_pars)

# Content Condors
add_subset("Content Condors", [
    ("CC-CB","Chris Brickley"),("CC-CL",'Cody "Clix" Conrod'),("CC-GV","Gary Vaynerchuk"),
    ("CC-MB",'Jimmy "MrBeast" Donaldson'),("CC-MG",'Kyle "Mongraal" Jackson'),("CC-MR","Mel Robbins"),
], std_insert_pars)

# Original Sketch Selections
add_subset("Original Sketch Selections", [
    ("OSS-1","Motivated Monster"),("OSS-2","Gary Bee"),("OSS-3","Rare Robot"),
    ("OSS-4","Very, Very, Very, Very, Lucky Black Cat"),("OSS-5","Empathy Elephant"),
], [("Gold Refractor", None),("Orange Refractor", None),("Black Refractor", None),
    ("Red Refractor", None),("Superfractor", 1)])

# Neon Lights
add_subset("Neon Lights", [
    ("NE-1","Decisive Duck"),("NE-2","Mindful Minokawa"),("NE-3","Whimsical Wolf"),
    ("NE-4","Vibe'n Vampire"),("NE-5","Chill Chinchilla"),("NE-6","Competitive Clown"),
    ("NE-7","Very, Very, Very, Very, Lucky Black Cat"),("NE-8","Tranquil Toad"),
    ("NE-9","Resilient Red Devil"),("NE-10","Forever Phoenix"),("NE-11","Glowing Glow Worm"),
    ("NE-12","Suffocate Hate"),("NE-13","Heart Trooper"),("NE-14","Hot Shot Hornet"),
    ("NE-15","Humble Hedgehog"),("NE-16","Joyous Jellyfish"),("NE-17","Perfect Persian Cat"),
    ("NE-18","Respectful Racoon"),("NE-19","Stunned Sun"),("NE-20","Stoic Slime"),
], std_insert_pars)

# Infinite Sapphire (Sapphire exclusive)
add_subset("Infinite Sapphire", [
    ("IS-1","Rare Robot"),("IS-2","Kind Warrior"),("IS-3","Adventurous Astronaut"),
    ("IS-4","Passionate Parrot"),("IS-5","Very, Very, Very, Very, Lucky Black Cat"),
], None)

# VeeFriends Variants
add_subset("VeeFriends Variants", [
    ("3","Decisive Duck"),("7","Notorious Ninja"),("11","Adventurous Astronaut"),
    ("15","Driven Dragon"),("39","Bubbly Buzzard"),("54","Considerate Cowboy"),
    ("109","Knowing Gnome"),("111","Ambitious Angel"),("143","Protective Panther"),
    ("175","To The Moon Meerkat"),
], [("Purple Variant", None),("Green Variant", None)])

# VeeFriends Variants - Last Glass Standing
add_subset("VeeFriends Variants - Last Glass Standing", [
    ("200","Last Glass Standing"),
], [("White Variant", None),("Rosé Variant", None)])

# VeeFriends Variants - Gritty Ghost
add_subset("VeeFriends Variants - Gritty Ghost", [("16","Gritty Ghost")], None)

# Stellar Haze
add_subset("Stellar Haze", [
    ("SH-1","Notorious Ninja"),("SH-2","Adventurous Astronaut"),("SH-3","Alert Ape"),
    ("SH-4","Bad Intentions"),("SH-5","Adaptable Alien"),("SH-6","Content Condor"),
    ("SH-7","Entrepreneur Elf"),("SH-8","Headstrong Honey Badger"),("SH-9","Hype Horse"),
    ("SH-10","Impeccable Inostranet"),("SH-11","Legendary Lemur"),("SH-12","Ambitious Angel"),
    ("SH-13","Persuasive Pigeon"),("SH-14","Prudent Polar Bear"),("SH-15","Tenacious Termite"),
    ("SH-16","To The Moon Meerkat"),("SH-17","Truculent T-Rex"),("SH-18","Well-Connected Werewolf"),
    ("SH-19","Willful Wizard"),("SH-20","Zealous Zombie"),
], [("Gold Refractor", None),("Orange Refractor", None),("Black Refractor", None),
    ("Red Refractor", None),("Superfractor", 1)])

# Balance Battles (dual cards, except BB-7 single)
bb_id = add_is("Balance Battles")
for pn, pr in [("Gold Refractor", None),("Orange Refractor", None),("Black Refractor", None),
               ("Red Refractor", None),("Superfractor", 1)]:
    add_par(bb_id, pn, pr)
bb_duals = [
    ("BB-1","Candid Clownfish","Compassionate Catfish"),
    ("BB-2","Chill Chinchilla","Hard-Working Wombat"),
    ("BB-3","Confident Cobra","Humble Hedgehog"),
    ("BB-4","Curious Crane","Knowing Gnome"),
    ("BB-5","Happy Hermit Crab","Accountable Ant"),
    ("BB-6","Intuitive Iguana","Logical Lion"),
    ("BB-8","Patient Pig","Ambitious Angel"),
    ("BB-9","Practical Peacock","Optimistic Otter"),
    ("BB-10","You're Gonna Die Fly","Forever Phoenix"),
]
add_dual_cards(bb_id, bb_duals)
# BB-7 single subject
pid_mm = get_or_create("Macro Micro")
db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, 'BB-7', 0, NULL)", (pid_mm, bb_id))
print(f"  Balance Battles: 10 cards (9 dual + 1 single), 5 parallels")

# Iconics (no parallels)
add_subset("Iconics", [
    ("I-1","Kind Warrior"),("I-2","Accountable Ant"),("I-3","Arbitraging Admiral"),
    ("I-4","Befuddled Burglar"),("I-5","Very, Very, Very, Very, Lucky Black Cat"),
    ("I-6","Conviction Cockroach"),("I-7","Intuitive Iguana"),("I-8","Loyal Lobster"),
    ("I-9","Passionate Parrot"),("I-10","Positive Porcupine"),("I-11","Reliable Rat"),
    ("I-12","Secure Sparrow"),("I-13","Sensible Sommelier"),("I-14","Shrewd Sheep"),
    ("I-15","Spontaneous Seahorse"),("I-16","Tolerant Tortoise"),("I-17","Trusting Tarantula"),
    ("I-18","Turnt Tick"),("I-19","Unwavering Urchin"),("I-20","Well-Rounded Warthog"),
], None)

# Erupt!
add_subset("Erupt!", [
    ("E-1","Fearless Fairy"),("E-2","Thoughtful Three Horned Harpik"),("E-3","Motivated Monster"),
    ("E-4","Versatile Viking"),("E-5","Gary Bee"),("E-6","Rare Robot"),
    ("E-7","Adventurous Astronaut"),("E-8","Driven Dragon"),("E-9","Bad Intentions"),
    ("E-10","Bashful Blobfish"),("E-11","Jolly Jack-O"),("E-12","Adaptable Alien"),
    ("E-13","Competitive Clown"),("E-14","Confident Cobra"),
    ("E-15","Very, Very, Very, Very, Lucky Black Cat"),("E-16","Resilient Red Devil"),
    ("E-17","Empathy Elephant"),("E-18","Gratitude Gorilla"),("E-19","Tidy Troll"),
    ("E-20","Willful Wizard"),
], [("Black Lava Refractor", None),("Superfractor", 1)])

# MegaHeads (Mega exclusive)
add_subset("MegaHeads", [
    ("M-1","Adventurous Astronaut"),("M-2","Fearless Fairy"),("M-3","Notorious Ninja"),
    ("M-4","Kind Warrior"),("M-5","Rare Robot"),("M-6","Ambitious Angel"),
    ("M-7","Be The Bigger Person"),("M-8","Clever Crocodile"),("M-9","Common Sense Cow"),
    ("M-10","Competitive Clown"),("M-11","Dynamic Dinosaur"),("M-12","Heart Trooper"),
    ("M-13","Hustling Hamster"),("M-14","Jolly Jack-O"),("M-15","Knowing Gnome"),
    ("M-16","Modest Moose"),("M-17","Optimistic Otter"),("M-18","Passionate Parrot"),
    ("M-19","Ponder It From All Angles"),("M-20","Resilient Red Devil"),
    ("M-21","Self-Aware Hare"),("M-22","Sensitive Centipede"),("M-23","Steadfast Snake"),
    ("M-24","Zealous Zombie"),("M-25","Very, Very, Very, Very, Lucky Black Cat"),
], [("Red Refractor", None),("Superfractor", 1)])

# Hidden Gems (Sapphire exclusive)
add_subset("Hidden Gems", [
    ("HG-1","Notorious Ninja"),("HG-2","Resilient Red Devil"),
    ("HG-3","Thoughtful Three Horned Harpik"),("HG-4","Gratitude Gorilla"),
    ("HG-5","Very, Very, Very, Very, Lucky Black Cat"),
], [("Emerald", None),("Onyx", None),("Ruby", None),("Padparadscha Sapphire", None)])

# ─── RELIC SUBSET ────────────────────────────────────────────────────────────
# Comic Clippings (CC-N numeric prefix — separate from Content Condors CC-XX letter prefix)
add_subset("Comic Clippings", [
    ("CC-1","VeeFriends #1 - The Battle For Balance Begins!"),
    ("CC-2","VeeFriends #2 - The Origin Of Fearless Fairy"),
    ("CC-3","VeeFriends #3 - World Tour"),
    ("CC-4","VeeFriends #4 - Hunt for Harpik"),
    ("CC-5","VeeFriends #5 - Motivated Monster"),
    ("CC-6","VeeFriends #6 - Vee Is For Viking"),
    ("CC-7","VeeFriends #7 - Notorious Ninja"),
    ("CC-8","VeeFriends #8 - Gary Bee"),
    ("CC-9","VeeFriends #9 - Kind Warrior"),
    ("CC-10","VeeFriends #10 - Rare Robot"),
], None)

# ─── AUTOGRAPH SUBSETS ───────────────────────────────────────────────────────
# Content Condors Autographs
add_subset("Content Condors Autographs", [
    ("CCA-GV","Gary Vaynerchuk"),("CCA-JP","Jake Paul"),("CCA-KP","Kam Patterson"),
    ("CCA-LD","Livvy Dunne"),("CCA-MR","Mel Robbins"),
    ("CC-CB","Chris Brickley"),("CC-CL",'Cody "Clix" Conrod'),
    ("CC-MG",'Kyle "Mongraal" Jackson'),
], [("Red Refractor", None),("Superfractor", 1)])

# ─── SKETCH CARDS ────────────────────────────────────────────────────────────
# Blank Canvas (1 card, 1/1)
add_subset("Blank Canvas Sketch Cards", [("BCS-1","Gary Vee")], None)

# Sketch Cards (multi-artist, all 1/1)
sketch_artists = [
    "Gary Vee","Aaron Laurich","Adam Fields","Adam Harris","Adam Lister","Adriane R Wiltse",
    "Ali Castro","Anderson Bluu",'Anthony "HiAnthony" Massucci',"Anthony Pietszak","Aston Cover",
    "AtomicCoffeeBro","Basak Kahraman","Bobby Blakey","Bradley Fleisher","Brent Ragland",
    "Brian Machelski","Camila Nogueira","Chad Scheres","Chris Botterill","Chris Campana",
    "Chris Fason","Chris Thorne","Christopher Clements","COHEN","Crystal Groves","Dan Doll",
    "Daniel Chavez","Daniel Goodroad","Darrin Pepe","David Acevedo","David Willingham",
    "D.J. Coffman","Don Mark Noceda","Dove Mchargue","Eddie Rhodes III","Eric Deaube",
    "Eric Medina","Erik Muller","Fox Layng","Franklim Teixeira","Gregory Fages","Ian Mckesson",
    "ibenkind","Isiah Bradley","J Hammond","Jade Kuei","James Harris","Jane Rushton",
    "Jason Bryant","Jason Christner","Jason Queen","Jason Rodriguez","Jason Saldajeno","Jeff Cox",
    '"Jeremy "Grails" Gill',"Jessica Court","Jessica Van Dusen","Jim Mahfood","Jim Rugg",
    "Joey Fitchett","John Monserrat","John Rodriguez","Jordan Spector","Julia Mckenzie",
    "Julie Kutlesic","Kat Zell","Kate Windels","Kimber Grobman","Leeeeeeeeexx","Luke Rushton",
    "Mark Parisi","Marlo Agunos","Marlo Martos","Matthew Maldonado","Merienne",
    "Miami Luxury Realtor","Michael Davidson","Michael Mastermaker","Michelle Sifre",
    "Mike Stephens","Neil Camera","Nick Gribbon","Nik Castaneda","Nik Muggli","Patrick Giles",
    "Rich Hennemann","RJ Tomascik","Rob Messer","Robert Blancas","Robert Demers","Robert Harris",
    "Roberto Garcia","Rusty Gilligan","Ryan Finley","Ryan Thompson","Sandy Lopopolo",
    "Sebastian Cortez","Semra Bulut","Señor Pants & Aria Heath","Shaow Siong","Simone Arena",
    "Stephane Leonardi","Steve Crockett","Steve Stylianou","Tim Shinn","Todd Beats",
    "Tom Bancroft","Vincenzo D'Ippolito","William Roger","Zachary Maers",
]
sketch_id = add_is("Sketch Cards")
for i, artist in enumerate(sketch_artists, 1):
    pid = get_or_create(artist)
    db.execute("INSERT INTO player_appearances (player_id, insert_set_id, card_number, is_rookie, team) VALUES (?, ?, ?, 0, NULL)",
               (pid, sketch_id, f"SK-{i}"))
print(f"  Sketch Cards: {len(sketch_artists)} artists (all 1/1)")

# ─── PACK ODDS ───────────────────────────────────────────────────────────────
pack_odds = {
    "hobby": {
        "Base Cards": "3:1",
        "Base Cards Refractor": "1:2",
        "Base Cards Aqua Raywave Refractor": "1:31",
        "Base Cards Pink Refractor": "1:25",
        "Base Cards Blue Refractor": "1:41",
        "Base Cards VF Green Refractor": "1:62",
        "Base Cards Purple Refractor": "1:82",
        "Base Cards Gold Refractor": "1:122",
        "Base Cards Pearl Refractor": "1:203",
        "Base Cards Orange Refractor": "1:244",
        "Base Cards Black Wave Refractor": "1:329",
        "Base Cards Black Refractor": "1:609",
        "Base Cards Red Wave Refractor": "1:657",
        "Base Cards Black Cat Refractor": "1:869",
        "Base Cards Red Refractor": "1:1,217",
        "Base Cards Gary Vee Autograph Parallel": "1:1,225",
        "Base Cards Superfractor": "1:6,083",
        "Topps 1986 Base Set Variation": "1:43",
        "Topps 1986 Base Set Variation Superfractor": "1:53,364",
        "Manga Speckle Set": "1:2",
        "Manga Speckle Set Orange Speckle Refractor": "1:487",
        "Manga Speckle Set Purple Speckle Refractor": "1:1,217",
        "Manga Speckle Set Red Speckle Refractor": "1:2,436",
        "Manga Speckle Set Black Speckle Refractor": "1:12,230",
        "Chalkboard": "1:62",
        "Chalkboard VF Green Refractor": "1:615",
        "Chalkboard Gold Refractor": "1:1,217",
        "Chalkboard Orange Refractor": "1:2,436",
        "Chalkboard Black Refractor": "1:6,083",
        "Chalkboard Red Refractor": "1:12,230",
        "Chalkboard Superfractor": "1:69,059",
        "Content Condors": "1:207",
        "Content Condors VF Green Refractor": "1:2,049",
        "Content Condors Gold Refractor": "1:4,063",
        "Content Condors Orange Refractor": "1:8,153",
        "Content Condors Black Refractor": "1:20,965",
        "Content Condors Red Refractor": "1:43,482",
        "Content Condors Superfractor": "1:391,334",
        "Original Sketch Selections": "1:244",
        "Original Sketch Selections Gold Refractor": "1:4,792",
        "Original Sketch Selections Orange Refractor": "1:9,703",
        "Original Sketch Selections Black Refractor": "1:24,979",
        "Original Sketch Selections Red Refractor": "1:53,364",
        "Original Sketch Selections Superfractor": "1:587,000",
        "Neon Lights": "1:62",
        "Neon Lights VF Green Refractor": "1:615",
        "Neon Lights Gold Refractor": "1:1,217",
        "Neon Lights Orange Refractor": "1:2,436",
        "Neon Lights Black Refractor": "1:6,083",
        "Neon Lights Red Refractor": "1:12,230",
        "Neon Lights Superfractor": "1:69,059",
        "Stellar Haze": "1:62",
        "Stellar Haze Gold Refractor": "1:1,217",
        "Stellar Haze Orange Refractor": "1:2,436",
        "Stellar Haze Black Refractor": "1:6,083",
        "Stellar Haze Red Refractor": "1:12,230",
        "Stellar Haze Superfractor": "1:69,059",
        "Balance Battles": "1:122",
        "Balance Battles Gold Refractor": "1:2,436",
        "Balance Battles Orange Refractor": "1:4,892",
        "Balance Battles Black Refractor": "1:12,230",
        "Balance Battles Red Refractor": "1:24,979",
        "Balance Battles Superfractor": "1:167,715",
        "Iconics": "1:648",
        "Erupt!": "1:2,160",
        "Erupt! Black Lava Refractor": "1:6,083",
        "Erupt! Superfractor": "1:69,059",
        "VeeFriends Variants Purple Variant": "1:155",
        "VeeFriends Variants Green Variant": "1:1,240",
        "VeeFriends Variants Last Glass Standing White Variant": "1:1,550",
        "VeeFriends Variants Last Glass Standing Rosé Variant": "1:3,099",
        "VeeFriends Variants Gritty Ghost": "1:1,550",
        "Content Condor On-Card Autograph": "1:1,280",
        "Content Condor On-Card Autograph Red Refractor": "1:57,240",
        "Content Condor On-Card Autograph Superfractor": "1:314,820",
        "Sketch Cards": "1:326",
        "Blank Canvas Sketch Cards": "1:104,940",
        "Comic Clippings": "1:1,164",
    }
}
db.execute("UPDATE sets SET pack_odds = ? WHERE id = ?", (json.dumps(pack_odds), SET_ID))
print(f"\n  Pack odds: {len(pack_odds['hobby'])} hobby entries")

# ─── Generate slugs ──────────────────────────────────────────────────────────
def slugify(text):
    s = text.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_]+', '-', s)
    return re.sub(r'-+', '-', s).strip('-')

rows = db.execute("SELECT id, name FROM players WHERE set_id = ? AND slug IS NULL", (SET_ID,)).fetchall()
existing = set(r[0] for r in db.execute("SELECT slug FROM players WHERE set_id = ? AND slug IS NOT NULL", (SET_ID,)).fetchall())
for pid, pname in rows:
    slug = slugify(pname)
    if slug in existing:
        i = 2
        while f"{slug}-{i}" in existing: i += 1
        slug = f"{slug}-{i}"
    existing.add(slug)
    db.execute("UPDATE players SET slug = ? WHERE id = ?", (slug, pid))

db.commit()

# ─── Summary ─────────────────────────────────────────────────────────────────
player_count = db.execute("SELECT COUNT(*) FROM players WHERE set_id = ?", (SET_ID,)).fetchone()[0]
app_count = db.execute("SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON pa.insert_set_id = i.id WHERE i.set_id = ?", (SET_ID,)).fetchone()[0]
is_count = db.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id = ?", (SET_ID,)).fetchone()[0]
par_count = db.execute("SELECT COUNT(*) FROM parallels WHERE insert_set_id IN (SELECT id FROM insert_sets WHERE set_id = ?)", (SET_ID,)).fetchone()[0]
co_count = db.execute("SELECT COUNT(*) FROM appearance_co_players ac JOIN player_appearances pa ON pa.id = ac.appearance_id JOIN insert_sets i ON i.id = pa.insert_set_id WHERE i.set_id = ?", (SET_ID,)).fetchone()[0]

print(f"\nDone! Set ID: {SET_ID}")
print(f"  Characters/Subjects: {player_count}")
print(f"  Appearances: {app_count}")
print(f"  Insert sets: {is_count}")
print(f"  Parallels: {par_count}")
print(f"  Co-player links: {co_count}")
db.close()
