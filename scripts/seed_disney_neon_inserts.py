"""Seed insert sets for 2026 Topps Disney Neon (set 59)."""
import sqlite3, os, re, unicodedata

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA foreign_keys=ON")
cur = conn.cursor()
SET_ID = 59

def slugify(t):
    s = t.lower()
    s = unicodedata.normalize("NFD", s)
    s = re.sub(r"[\u0300-\u036f]", "", s)
    s = re.sub(r"[^a-z0-9-]+", "-", s).strip("-")
    return re.sub(r"-+", "-", s)

def gop(name):
    cur.execute("SELECT id FROM players WHERE set_id=? AND name=?", (SET_ID, name))
    r = cur.fetchone()
    if r: return r[0]
    cur.execute("INSERT INTO players (set_id,name,slug,unique_cards,total_print_run,one_of_ones,insert_set_count) VALUES (?,?,?,0,0,0,0)", (SET_ID, name, slugify(name)))
    return cur.lastrowid

def cis(name):
    cur.execute("INSERT INTO insert_sets (set_id,name) VALUES (?,?)", (SET_ID, name))
    return cur.lastrowid

def cp(is_id, name, pr):
    cur.execute("INSERT INTO parallels (insert_set_id,name,print_run) VALUES (?,?,?)", (is_id, name, pr))

def ca(pid, is_id, cn, team=None):
    cur.execute("INSERT INTO player_appearances (player_id,insert_set_id,card_number,is_rookie,team) VALUES (?,?,?,0,?)", (pid, is_id, cn, team))
    return cur.lastrowid

def cco(aid, cpid):
    cur.execute("INSERT INTO appearance_co_players (appearance_id,co_player_id) VALUES (?,?)", (aid, cpid))

def add(is_id, cards):
    for cn, n, t in cards: ca(gop(n), is_id, cn, t)

def add_dual(is_id, cards):
    for cn, pairs in cards:
        aids, pids = [], []
        for n, t in pairs:
            pid = gop(n)
            aid = ca(pid, is_id, cn, t)
            aids.append(aid); pids.append(pid)
        for i in range(len(aids)):
            for j in range(len(pids)):
                if i != j: cco(aids[i], pids[j])

def add_triple(is_id, cards):
    for cn, triples in cards:
        aids, pids = [], []
        for n, t in triples:
            pid = gop(n)
            aid = ca(pid, is_id, cn, t)
            aids.append(aid); pids.append(pid)
        for i in range(len(aids)):
            for j in range(len(pids)):
                if i != j: cco(aids[i], pids[j])

def mis(name, pars, cards):
    is_id = cis(name)
    for pn, pr in pars: cp(is_id, pn, pr)
    add(is_id, cards)
    print(f"  {name}: {len(cards)} cards")
    return is_id

# ── TOPPS NEON AUTOGRAPHS (30) ───────────────────────────────────────────────
mis("Topps Neon Autographs", [("Gold",None),("Red",None),("Pink",None)], [
("TNA-AB","Marlin","Finding Nemo"),("TNA-AG","Nemo","Finding Nemo"),("TNA-ANR","Tiana","The Princess and the Frog"),("TNA-AC","Moana","Moana"),("TNA-BB","Ernesto de la Cruz","Coco"),("TNA-BC","Mike Wazowski","Monsters, Inc."),("TNA-CE","Buzz Lightyear","Lightyear"),("TNA-CPI","King Magnifico","Wish"),("TNA-CDB","Prince Eric","The Little Mermaid"),("TNA-GB","H\u00e9ctor","Coco"),("TNA-IM","Elsa","Frozen"),("TNA-IB","Pocahontas","Pocahontas"),("TNA-JB","Ariel","The Little Mermaid"),("TNA-GO","Sulley","Monsters, Inc."),("TNA-JF","Jafar","Aladdin"),("TNA-JGF","Kristoff","Frozen"),("TNA-JG","Olaf","Frozen"),("TNA-KM","Merida","Brave"),("TNA-LL","Jasmine","Aladdin"),("TNA-MK","Tinker Bell","Peter Pan"),("TNA-MNW","Mulan","Mulan"),("TNA-POH","Belle","Beauty and the Beast"),("TNA-PO","Remy","Ratatouille"),("TNA-PS","Sadness","Inside Out"),("TNA-RW","Gaston","Beauty and the Beast"),("TNA-SB","Mirabel","Encanto"),("TNA-SE","Megara","Hercules"),("TNA-TA","Buzz Lightyear","Toy Story"),("TNA-TH","Woody","Toy Story"),("TNA-TAN","Donald Duck","Mickey & Friends")])

# ── PHINEAS AND FERB AUTO VARIATION (7) ───────────────────────────────────────
mis("Phineas and Ferb Auto Variation", [("Gold Refractor",None),("Orange Refractor",None),("Black Refractor",None),("Red Refractor",None),("Superfractor",1)], [
("P&FA-VM","Phineas","Phineas and Ferb"),("P&FA-DEJ","Ferb","Phineas and Ferb"),("P&FA-DP","Dr. Doofenshmirtz","Phineas and Ferb"),("P&FA-JSM","Major Monogram","Phineas and Ferb"),("P&FA-DBB","Perry the Platypus","Phineas and Ferb"),("P&FA-AS","Isabella","Phineas and Ferb"),("P&FA-KH","Stacy","Phineas and Ferb")])

# ── A GOOFY MOVIE 30TH ANNIVERSARY AUTO VARIATION (6) ────────────────────────
mis("A Goofy Movie 30th Anniversary Auto Variation", [("Gold Refractor",None),("Orange Refractor",None),("Black Refractor",None),("Red Refractor",None),("Superfractor",1)], [
("AGMA-BF","Goofy","A Goofy Movie"),("AGMA-JC","Pete","A Goofy Movie"),("AGMA-RP","P.J.","A Goofy Movie"),("AGMA-KM","Roxanne","A Goofy Movie"),("AGMA-PS","Bobby Zimuruski","A Goofy Movie"),("AGMA-FW","Bigfoot","A Goofy Movie")])

# ── MICKEY SHORTS SHORT PRINTS AUTO VARIATION (7) ────────────────────────────
mis("Mickey Shorts Short Prints Auto Variation", [("Gold Refractor",None),("Orange Refractor",None),("Black Refractor",None),("Red Refractor",None),("Superfractor",1)], [
("MSA-CD","Mickey Mouse","Mickey & Friends"),("MSA-CDI","Mickey Mouse","Mickey & Friends"),("MSA-KR","Minnie Mouse","Mickey & Friends"),("MSA-KRB","Minnie Mouse","Mickey & Friends"),("MSA-TA","Donald Duck","Mickey & Friends"),("MSA-BFG","Goofy","Mickey & Friends"),("MSA-BFAP","Pluto","Mickey & Friends")])

# ── MICKEY SHORTS DUAL AUTO VARIATION (9) co_players ─────────────────────────
is_id = cis("Mickey Shorts Dual Auto Variation")
for pn, pr in [("Black Wave",None),("Red Wave",None),("Superfractor",1)]: cp(is_id, pn, pr)
add_dual(is_id, [
("MSDA-DA",[("Mickey Mouse","Mickey & Friends"),("Donald Duck","Mickey & Friends")]),
("MSDA-DFG",[("Mickey Mouse","Mickey & Friends"),("Goofy","Mickey & Friends")]),
("MSDA-DFP",[("Mickey Mouse","Mickey & Friends"),("Pluto","Mickey & Friends")]),
("MSDA-RA",[("Minnie Mouse","Mickey & Friends"),("Donald Duck","Mickey & Friends")]),
("MSDA-RFG",[("Minnie Mouse","Mickey & Friends"),("Goofy","Mickey & Friends")]),
("MSDA-RFP",[("Minnie Mouse","Mickey & Friends"),("Pluto","Mickey & Friends")]),
("MSDA-AFG",[("Donald Duck","Mickey & Friends"),("Goofy","Mickey & Friends")]),
("MSDA-AFP",[("Donald Duck","Mickey & Friends"),("Pluto","Mickey & Friends")]),
("MSDA-BF",[("Goofy","Mickey & Friends"),("Pluto","Mickey & Friends")])])
print("  Mickey Shorts Dual Auto Variation: 9 cards")

# ── TRIPLE BOOKLET SUPERFRACTOR (11) triple co_players ────────────────────────
is_id = cis("Triple Booklet Superfractor")
cp(is_id, "Base /1", 1)
add_triple(is_id, [
("TBS-DRF",[("Mickey Mouse","Mickey Shorts"),("Minnie Mouse","Mickey Shorts"),("Goofy","Mickey Shorts")]),
("TBS-DRA",[("Mickey Mouse","Mickey Shorts"),("Minnie Mouse","Mickey Shorts"),("Donald Duck","Mickey Shorts")]),
("TBS-DFR",[("Mickey Mouse","Mickey Shorts"),("Pluto","Mickey Shorts"),("Minnie Mouse","Mickey Shorts")]),
("TBS-DFF",[("Mickey Mouse","Mickey Shorts"),("Goofy","Mickey Shorts"),("Pluto","Mickey Shorts")]),
("TBS-DFA",[("Mickey Mouse","Mickey Shorts"),("Goofy","Mickey Shorts"),("Donald Duck","Mickey Shorts")]),
("TBS-FAF",[("Goofy","Mickey Shorts"),("Donald Duck","Mickey Shorts"),("Pluto","Mickey Shorts")]),
("TBS-IRF",[("Mickey Mouse","Mickey & Friends Classic"),("Minnie Mouse","Mickey & Friends Classic"),("Goofy","Mickey & Friends Classic")]),
("TBS-IRA",[("Mickey Mouse","Mickey & Friends Classic"),("Minnie Mouse","Mickey & Friends Classic"),("Donald Duck","Mickey & Friends Classic")]),
("TBS-IFR",[("Mickey Mouse","Mickey & Friends Classic"),("Pluto","Mickey & Friends Classic"),("Minnie Mouse","Mickey & Friends Classic")]),
("TBS-IFF",[("Mickey Mouse","Mickey & Friends Classic"),("Goofy","Mickey & Friends Classic"),("Pluto","Mickey & Friends Classic")]),
("TBS-IFA",[("Mickey Mouse","Mickey & Friends Classic"),("Goofy","Mickey & Friends Classic"),("Donald Duck","Mickey & Friends Classic")])])
print("  Triple Booklet Superfractor: 11 cards")

# ── CHROME NEON ETCH AUTOGRAPHS (60) ─────────────────────────────────────────
mis("Chrome Neon Etch Autographs", [("Gold Shimmer",None),("Orange Wave",None),("Black Speckle",None),("Red Lava",None),("Superfractor",1)], [
("CNA-VM","Phineas","Phineas and Ferb"),("CNA-DEJ","Ferb","Phineas and Ferb"),("CNA-AST","Isabella","Phineas and Ferb"),("CNA-DP","Dr. Doofenshmirtz","Phineas and Ferb"),("CNA-DBB","Perry the Platypus","Phineas and Ferb"),("CNA-JC","Tigger","Winnie the Pooh"),("CNA-RB","Beast","Beauty and the Beast"),("CNA-RW","Gaston","Beauty and the Beast"),("CNA-CS","Stitch","Lilo & Stitch"),("CNA-SB","Mirabel","Encanto"),("CNA-BB","WALL-E","WALL-E"),("CNA-AC","Moana","Moana 2"),("CNA-SW","Aladdin","Aladdin"),("CNA-JF","Jafar","Aladdin"),("CNA-TA","Buzz Lightyear","Toy Story"),("CNA-THX","Woody","Toy Story"),("CNA-AS","Zurg","Toy Story 2"),("CNA-DS","Kuzco","The Emperor's New Groove"),("CNA-PW","Kronk","The Emperor's New Groove"),("CNA-MB","Simba","The Lion King"),("CNA-DM","Mother Gothel","Tangled"),("CNA-IM","Elsa","Frozen"),("CNA-HH","Mrs. Incredible","The Incredibles"),("CNA-SF","Dash Parr","The Incredibles"),("CNA-HM","Dash Parr","The Incredibles"),("CNA-SLJ","Frozone","The Incredibles"),("CNA-JR","The Underminer","The Incredibles"),("CNA-AGN","Miguel","Coco"),("CNA-GGB","H\u00e9ctor","Coco"),("CNA-BBR","Ernesto de la Cruz","Coco"),("CNA-PO","Remy","Ratatouille"),("CNA-BG","Gusteau","Ratatouille"),("CNA-MNW","Mulan","Mulan"),("CNA-BDW","Li Shang","Mulan"),("CNA-AG","Nemo","Finding Nemo"),("CNA-AB","Marlin","Finding Nemo"),("CNA-LCG","Mater","Cars"),("CNA-OW","Lightning McQueen","Cars"),("CNA-BF","Goofy","A Goofy Movie"),("CNA-JCM","Pete","A Goofy Movie"),("CNA-RP","P.J.","A Goofy Movie"),("CNA-KM","Roxanne","A Goofy Movie"),("CNA-JG","Sulley","Monsters, Inc."),("CNA-BC","Mike Wazowski","Monsters, Inc."),("CNA-TD","Hercules","Hercules"),("CNA-SE","Megara","Hercules"),("CNA-BGR","Lord Grigon","Elio"),("CNA-THL","Fear","Inside Out"),("CNA-LB","Anger","Inside Out"),("CNA-PS","Sadness","Inside Out"),("CNA-LL","Disgust","Inside Out"),("CNA-RK","Bing Bong","Inside Out"),("CNA-CP","King Magnifico","Wish"),("CNA-LLW","Ember Lumen","Elemental"),("CNA-MA","Wade Ripple","Elemental"),("CNA-TAN","Donald Duck","Mickey & Friends"),("CNA-BFR","Pluto","Mickey & Friends"),("CNA-KR","Minnie Mouse","Mickey & Friends"),("CNA-BI","Mickey Mouse","Mickey & Friends"),("CNA-BS","Jay","Descendants")])

# ── SCROOGE'S MONEY BIN CUT SIG (1) ──────────────────────────────────────────
is_id = cis("Scrooge's Money Bin Cut Sig Variation")
cp(is_id, "Base /1", 1)
add(is_id, [("SMBA-AY","Scrooge McDuck","Ducktales")])
print("  Scrooge's Money Bin Cut Sig Variation: 1 card")

# ── MICKEY MOUSE COMIC CUTS (1) ──────────────────────────────────────────────
mis("Mickey Mouse Comic Cuts", [], [("MM-CC","Mickey Mouse","Mickey & Friends")])

# ── FAMILY FIRST (35) co_players ──────────────────────────────────────────────
FF_PARS = [("Gold",None),("Orange",None),("Black",None),("Red",None),("Foilfractor",1)]
is_id = cis("Family First")
for pn, pr in FF_PARS: cp(is_id, pn, pr)
add_dual(is_id, [
("FF-1",[("Mirabel","Encanto"),("Abuela Alma","Encanto")]),("FF-2",[("Miguel","Coco"),("H\u00e9ctor","Coco")]),("FF-3",[("Wendy","Peter Pan"),("John & Michael","Peter Pan")]),("FF-4",[("Geppetto","Pinocchio"),("Pinocchio","Pinocchio")]),("FF-5",[("Simba","The Lion King"),("Mufasa","The Lion King")]),("FF-6",[("Mulan","Mulan"),("Fa Zhou","Mulan")]),("FF-7",[("Bernard","The Rescuers"),("Miss Bianca","The Rescuers")]),("FF-8",[("Mowgli","The Jungle Book"),("Baloo","The Jungle Book")]),("FF-9",[("Hercules","Hercules"),("Hera","Hercules")]),("FF-10",[("Lewis","Meet the Robinsons"),("Wilbur Robinson","Meet the Robinsons")]),("FF-11",[("Tweedle Dee","Alice in Wonderland"),("Tweedle Dum","Alice in Wonderland")]),("FF-12",[("Lady","Lady and the Tramp"),("Tramp","Lady and the Tramp")]),("FF-13",[("Belle","Beauty and the Beast"),("Maurice","Beauty and the Beast")]),("FF-14",[("Pongo","One Hundred and One Dalmatians"),("Perdita","One Hundred and One Dalmatians")]),("FF-15",[("Ian Lightfoot","Onward"),("Barley Lightfoot","Onward")]),("FF-16",[("Bambi","Bambi"),("Mother","Bambi")]),("FF-17",[("Merida","Brave"),("Queen Elinor","Brave")]),("FF-18",[("Chicken Little","Chicken Little"),("Buck Cluck","Chicken Little")]),("FF-19",[("Ariel","The Little Mermaid"),("King Triton","The Little Mermaid")]),("FF-20",[("Jaq","Cinderella"),("Gus","Cinderella")]),("FF-21",[("Kanga","Winnie the Pooh"),("Roo","Winnie the Pooh")]),("FF-22",[("Lilo","Lilo & Stitch"),("Nani","Lilo & Stitch")]),("FF-23",[("Goofy","A Goofy Movie"),("Max Goof","A Goofy Movie")]),("FF-24",[("Pacha","The Emperor's New Groove"),("Chicha","The Emperor's New Groove")]),("FF-25",[("Dumbo","Dumbo"),("Mrs. Jumbo","Dumbo")]),("FF-26",[("Elsa","Frozen"),("Anna","Frozen")]),("FF-27",[("Remy","Ratatouille"),("Emile","Ratatouille")]),("FF-28",[("Mei Lee","Turning Red"),("Ming Lee","Turning Red")]),("FF-29",[("Anastasia","Cinderella"),("Drizella","Cinderella")]),("FF-30",[("Phineas","Phineas and Ferb"),("Ferb","Phineas and Ferb")]),("FF-31",[("Mrs. Potts","Beauty and the Beast"),("Chip","Beauty and the Beast")]),("FF-32",[("Nemo","Finding Nemo"),("Marlin","Finding Nemo")]),("FF-33",[("Violet Parr","The Incredibles"),("Dash Parr","The Incredibles")]),("FF-34",[("Mal","Descendants"),("Maleficent","Descendants")]),("FF-35",[("Perdita","One Hundred and One Dalmatians"),("Her Puppies","One Hundred and One Dalmatians")])])
print("  Family First: 35 cards")

# ── FAMILY FIRST RIVALS VARIATIONS (35) co_players ───────────────────────────
FFR_PARS = [("Gold Refractor",None),("Orange Refractor",None),("Black Refractor",None),("Red Refractor",None),("Superfractor",1)]
is_id = cis("Family First Rivals Variations")
for pn, pr in FFR_PARS: cp(is_id, pn, pr)
add_dual(is_id, [
("FFR-1",[("Snow White","Snow White and the Seven Dwarfs"),("Evil Queen","Snow White and the Seven Dwarfs")]),("FFR-2",[("Sulley","Monsters, Inc."),("Randall Boggs","Monsters, Inc.")]),("FFR-3",[("Buzz Lightyear","Toy Story 2"),("Zurg","Toy Story 2")]),("FFR-4",[("Robin Hood","Robin Hood"),("Prince John","Robin Hood")]),("FFR-5",[("Tiana","The Princess and the Frog"),("Dr. Facilier","The Princess and the Frog")]),("FFR-6",[("Stitch","Lilo & Stitch"),("Captain Gantu","Lilo & Stitch")]),("FFR-7",[("Mr. Incredible","The Incredibles"),("Syndrome","The Incredibles")]),("FFR-8",[("Peter Pan","Peter Pan"),("Captain Hook","Peter Pan")]),("FFR-9",[("Mowgli","The Jungle Book"),("Shere Khan","The Jungle Book")]),("FFR-10",[("Alice","Alice in Wonderland"),("Queen of Hearts","Alice in Wonderland")]),("FFR-11",[("Hercules","Hercules"),("Hades","Hercules")]),("FFR-12",[("Winnie the Pooh","Winnie the Pooh"),("Heffalumps","Winnie the Pooh")]),("FFR-13",[("Belle","Beauty and the Beast"),("Gaston","Beauty and the Beast")]),("FFR-14",[("Quasimodo","The Hunchback of Notre Dame"),("Judge Claude Frollo","The Hunchback of Notre Dame")]),("FFR-15",[("Vanellope von Schweetz","Wreck-It Ralph"),("King Candy","Wreck-It Ralph")]),("FFR-16",[("Aladdin","Aladdin"),("Jafar","Aladdin")]),("FFR-17",[("Ariel","The Little Mermaid"),("Ursula","The Little Mermaid")]),("FFR-18",[("Lewis Robinson","Meet the Robinsons"),("Bowler Hat Guy","Meet the Robinsons")]),("FFR-19",[("Asha","Wish"),("King Magnifico","Wish")]),("FFR-20",[("Mufasa","The Lion King"),("Scar","The Lion King")]),("FFR-21",[("Flik","A Bug's Life"),("Hopper","A Bug's Life")]),("FFR-22",[("Aurora","Sleeping Beauty"),("Maleficent","Sleeping Beauty")]),("FFR-23",[("The Dalmatians","One Hundred and One Dalmatians"),("Cruella de Vil","One Hundred and One Dalmatians")]),("FFR-24",[("Cinderella","Cinderella"),("Lady Tremaine","Cinderella")]),("FFR-25",[("Linguini & Remy","Ratatouille"),("Anton Ego","Ratatouille")]),("FFR-26",[("Rapunzel","Tangled"),("Mother Gothel","Tangled")]),("FFR-27",[("Jaq & Gus","Cinderella"),("Lucifer","Cinderella")]),("FFR-28",[("Anna","Frozen"),("Prince Hans","Frozen")]),("FFR-29",[("Pocahontas","Pocahontas"),("Governor Ratcliffe","Pocahontas")]),("FFR-30",[("Mulan","Mulan"),("Shan Yu","Mulan")]),("FFR-31",[("Hiro Hamada","Big Hero 6"),("Yokai","Big Hero 6")]),("FFR-32",[("Kuzco","The Emperor's New Groove"),("Yzma","The Emperor's New Groove")]),("FFR-33",[("Mickey Mouse","Mickey & Friends"),("Pete","Mickey & Friends")]),("FFR-34",[("Carl Fredricksen","Up"),("Charles F. Muntz","Up")]),("FFR-35",[("Woody","Toy Story 3"),("Lotso","Toy Story 3")])])
print("  Family First Rivals Variations: 35 cards")

# ── Simple insert sets ────────────────────────────────────────────────────────
INS5 = [("Gold",None),("Orange",None),("Black",None),("Red",None),("Foilfractor",1)]

mis("Phineas and Ferb", INS5, [("P&F-"+str(i),n,t) for i,(n,t) in enumerate([(n,t) for n,t in [("Phineas","Phineas and Ferb"),("Ferb","Phineas and Ferb"),("Baljeet","Phineas and Ferb"),("Buford","Phineas and Ferb"),("Perry the Platypus","Phineas and Ferb"),("Isabella","Phineas and Ferb"),("Linda Flynn-Fletcher","Phineas and Ferb"),("Lawrence Fletcher","Phineas and Ferb"),("Jeremy Johnson","Phineas and Ferb"),("Candace","Phineas and Ferb"),("Stacy","Phineas and Ferb"),("Balloony","Phineas and Ferb"),("Charlene Doofenshmirtz","Phineas and Ferb"),("Vanessa Doofenshmirtz","Phineas and Ferb"),("Dr. Doofenshmirtz","Phineas and Ferb"),("Major Monogram","Phineas and Ferb"),("Carl the Intern","Phineas and Ferb"),("Meap","Phineas and Ferb"),("Peter the Panda","Phineas and Ferb"),("Agent P","Phineas and Ferb")]],1)])

mis("Manga Madness", INS5, [("MM-"+str(i),n,t) for i,(n,t) in enumerate([("Woody","Toy Story"),("Jessie","Toy Story"),("Bo Peep","Toy Story"),("Rex","Toy Story"),("Buzz Lightyear","Toy Story"),("Snot Rod","Cars"),("Boost","Cars"),("DJ","Cars"),("Wingo","Cars"),("Lightning McQueen","Cars"),("Aladdin","Aladdin"),("Prince Charming","Cinderella"),("Rapunzel","Tangled"),("Snow White","Snow White and the Seven Dwarfs"),("Evil Queen","Snow White and the Seven Dwarfs")],1)])

mis("A Goofy Movie", INS5, [("AGM-"+str(i),n,t) for i,(n,t) in enumerate([("Goofy","A Goofy Movie"),("Pete","A Goofy Movie"),("P.J.","A Goofy Movie"),("Roxanne","A Goofy Movie"),("Max Goof","A Goofy Movie"),("Bobby Zimuruski","A Goofy Movie"),("Bigfoot","A Goofy Movie"),("Powerline","A Goofy Movie"),("Goofy","A Goofy Movie"),("Max Goof","A Goofy Movie"),("Goofy","A Goofy Movie"),("Powerline","A Goofy Movie")],1)])

mis("Epic Mickey", [("Gold Refractor",None),("Orange Refractor",None),("Black Refractor",None),("Red Refractor",None),("Superfractor",1)], [("EM-"+str(i),n,"Epic Mickey") for i,n in enumerate(["Mickey Mouse","Horace Horsecollar","Clarabelle Cow","Abner","Oswald the Lucky Rabbit","Ortensia","Witch Tanker Beetleworx","Tomorrow City Tanker Beetleworx","Captain Basher Beetleworx","Steamboat Willie","Pirate Moody","Brave Little Tailor","Small Pete","Gus the Gremlin","Animatronic Donald","Animatronic Daisy","Spladoosh Blotling","Spatter Blotling","Seer Blotling","Mickey Mouse","Tanker Beetleworx","Basher Beetleworx","Clock Tower","Clock Tower","Shadow Blot"],1)])

mis("The Muppets Puzzle", [], [("MP-"+str(i),n,"The Muppets") for i,n in enumerate(["Animal","Beaker","Camilla the Chicken","Dr. Bunsen Honeydew","Dr. Teeth","Floyd Pepper","Fozzie Bear","Gonzo","Janice","Kermit","Miss Piggy","Pep\u00e9","Rizzo","Rowlf the Dog","Sam Eagle","Scooter","Statler","Swedish Chef","Waldorf","Walter","Zoot"],1)])

mis("Neon Lights", [], [("NPL-"+str(i),n,t) for i,(n,t) in enumerate([("Alice","Alice in Wonderland"),("Angel","Lilo & Stitch"),("Ariel","The Little Mermaid"),("Belle","Beauty and the Beast"),("Buzz Lightyear","Toy Story"),("Daisy Duck","Mickey & Friends"),("Donald Duck","Mickey & Friends"),("Elsa","Frozen"),("Genie","Aladdin"),("Goofy","Mickey & Friends"),("Hercules","Hercules"),("Joy","Inside Out"),("Lightning McQueen","Cars"),("Mickey Mouse","Mickey & Friends"),("Minnie Mouse","Mickey & Friends"),("Mirabel","Encanto"),("Moana","Moana"),("Peter Pan","Peter Pan"),("Pinocchio","Pinocchio"),("Pluto","Mickey & Friends"),("Simba","The Lion King"),("Stitch","Lilo & Stitch"),("Sulley","Monsters, Inc."),("Tinker Bell","Peter Pan"),("Wreck-It Ralph","Wreck-It Ralph")],1)])

mis("Mickey Shorts Short Prints", [("Gold Wave",None),("Orange Wave",None),("Black Wave",None),("Red Wave",None),("Superfractor",1)], [
("MSSP-1","Mickey Mouse","Mickey & Friends"),("MSSP-2","Mickey Mouse","Mickey & Friends"),("MSSP-3","Mickey Mouse","Mickey & Friends"),("MSSP-4","Mickey Mouse","Mickey & Friends"),("MSSP-5","Mickey & Minnie Mouse","Mickey & Friends"),("MSSP-6","Minnie Mouse","Mickey & Friends"),("MSSP-7","Minnie Mouse","Mickey & Friends"),("MSSP-8","Minnie Mouse","Mickey & Friends"),("MSSP-9","Minnie Mouse","Mickey & Friends"),("MSSP-10","Donald Duck","Mickey & Friends"),("MSSP-11","Donald Duck","Mickey & Friends"),("MSSP-12","Donald Duck","Mickey & Friends"),("MSSP-13","Donald Duck","Mickey & Friends"),("MSSP-14","Daisy Duck","Mickey & Friends"),("MSSP-15","Daisy Duck","Mickey & Friends"),("MSSP-16","Daisy Duck","Mickey & Friends"),("MSSP-17","Goofy","Mickey & Friends"),("MSSP-18","Goofy","Mickey & Friends"),("MSSP-19","Goofy","Mickey & Friends"),("MSSP-20","Goofy","Mickey & Friends"),("MSSP-21","Pluto","Mickey & Friends"),("MSSP-22","Pluto","Mickey & Friends"),("MSSP-23","Pluto","Mickey & Friends")])

mis("Magic Carpet Ride", [], [("MCR-1","Magic Carpet","Aladdin")])

mis("Neon Villains", [("Gold Lava",None),("Orange Lava",None),("Black Lava",None),("Red Lava",None),("Superfractor",1)], [
("NV-1","Ursula","The Little Mermaid"),("NV-2","Hades","Hercules"),("NV-3","Dr. Facilier","The Princess and the Frog"),("NV-4","Chernabog","Fantasia"),("NV-5","Evil Queen","Snow White and the Seven Dwarfs"),("NV-6","Scar","The Lion King"),("NV-7","Maleficent","Sleeping Beauty")])

# ── CHROME NEON ETCH (100) ────────────────────────────────────────────────────
CNE_PARS = [("Refractor",None),("Green Lazer",None),("Gold Shimmer",None),("Orange Wave",None),("Black Speckle",None),("Red Lava",None),("Superfractor",1)]
cne_cards = [
("CNE-1","Phineas","Phineas and Ferb"),("CNE-2","Ferb","Phineas and Ferb"),("CNE-4","Dr. Doofenshmirtz","Phineas and Ferb"),("CNE-5","Perry the Platypus","Phineas and Ferb"),("CNE-7","Tigger","Winnie the Pooh"),("CNE-8","Peter Pan","Peter Pan"),("CNE-9","Captain Hook","Peter Pan"),("CNE-11","The Beast","Beauty and the Beast"),("CNE-14","Stitch","Lilo & Stitch"),("CNE-15","Lilo","Lilo & Stitch"),("CNE-19","WALL-E","WALL-E"),("CNE-20","Eve","WALL-E"),("CNE-28","Aladdin","Aladdin"),("CNE-29","Genie","Aladdin"),("CNE-30","Jafar","Aladdin"),("CNE-31","Buzz Lightyear","Toy Story"),("CNE-32","Woody","Toy Story"),("CNE-33","Jessie","Toy Story"),("CNE-34","Zurg","Toy Story 2"),("CNE-37","Kuzco","The Emperor's New Groove"),("CNE-38","Yzma","The Emperor's New Groove"),("CNE-39","Kronk","The Emperor's New Groove"),("CNE-40","Mufasa","The Lion King"),("CNE-41","Simba","The Lion King"),("CNE-42","Nala","The Lion King"),("CNE-43","Scar","The Lion King"),("CNE-51","Mr. Incredible","The Incredibles"),("CNE-52","Mrs. Incredible","The Incredibles"),("CNE-53","Syndrome","The Incredibles"),("CNE-56","Frozone","The Incredibles"),("CNE-60","Flynn Rider","Tangled"),("CNE-61","Nick Wilde","Zootopia"),("CNE-62","Judy Hopps","Zootopia"),("CNE-65","Miguel","Coco"),("CNE-66","H\u00e9ctor","Coco"),("CNE-67","Ernesto de la Cruz","Coco"),("CNE-69","Pepita","Coco"),("CNE-70","Alebrije Dante","Coco"),("CNE-71","Remy","Ratatouille"),("CNE-72","Linguini","Ratatouille"),("CNE-75","Mulan","Mulan"),("CNE-76","Mushu","Mulan"),("CNE-79","Nemo","Finding Nemo"),("CNE-80","Marlin","Finding Nemo"),("CNE-81","Dory","Finding Nemo"),("CNE-86","Pinocchio","Pinocchio"),("CNE-87","Jiminy Cricket","Pinocchio"),("CNE-89","Mater","Cars"),("CNE-95","Lightning McQueen","Cars"),("CNE-100","Maleficent","Sleeping Beauty"),("CNE-101","Powerline","A Goofy Movie"),("CNE-102","Goofy","A Goofy Movie"),("CNE-105","Max Goof","A Goofy Movie"),("CNE-107","Ralph","Wreck-It Ralph"),("CNE-108","Felix","Wreck-It Ralph"),("CNE-109","Vanellope von Schweetz","Wreck-It Ralph"),("CNE-115","Chicken Little","Chicken Little"),("CNE-117","Kirby","Chicken Little"),("CNE-118","Sulley","Monsters, Inc."),("CNE-119","Mike Wazowski","Monsters, Inc."),("CNE-120","Randall Boggs","Monsters, Inc."),("CNE-123","Darkwing Duck","Darkwing Duck"),("CNE-125","Baymax","Big Hero 6"),("CNE-126","Hiro Hamada","Big Hero 6"),("CNE-128","Bolt","Bolt"),("CNE-130","Russell","Up"),("CNE-131","Hercules","Hercules"),("CNE-132","Hades","Hercules"),("CNE-133","Megara","Hercules"),("CNE-134","Goliath","Gargoyles"),("CNE-140","Lewis","Meet the Robinsons"),("CNE-145","Merlin","The Sword in the Stone"),("CNE-146","Elio Sol\u00eds","Elio"),("CNE-147","Glordon","Elio"),("CNE-150","B.E.N.","Treasure Planet"),("CNE-151","Scrooge McDuck","Ducktales"),("CNE-153","Chernabog","Fantasia"),("CNE-162","Elliott","Pete's Dragon"),("CNE-163","Joy","Inside Out"),("CNE-164","Fear","Inside Out"),("CNE-165","Anger","Inside Out"),("CNE-166","Sadness","Inside Out"),("CNE-167","Disgust","Inside Out"),("CNE-168","Bing Bong","Inside Out"),("CNE-169","Anxiety","Inside Out 2"),("CNE-174","Milo","Atlantis: The Lost Empire"),("CNE-175","Kida","Atlantis: The Lost Empire"),("CNE-176","Ursula","The Little Mermaid"),("CNE-180","Sebastian","The Little Mermaid"),("CNE-181","Ember Lumen","Elemental"),("CNE-185","Dumbo","Dumbo"),("CNE-186","Kermit","The Muppets"),("CNE-187","Miss Piggy","The Muppets"),("CNE-191","Gonzo","The Muppets"),("CNE-194","Animal","The Muppets"),("CNE-196","Donald Duck","Mickey & Friends"),("CNE-197","Daisy Duck","Mickey & Friends"),("CNE-198","Pluto","Mickey & Friends"),("CNE-199","Minnie Mouse","Mickey & Friends"),("CNE-200","Mickey Mouse","Mickey & Friends")]
mis("Chrome Neon Etch", CNE_PARS, cne_cards)

# ── SCROOGE'S MONEY BIN (1) ──────────────────────────────────────────────────
mis("Scrooge's Money Bin", [("Gold",None),("Rose Gold",None),("Foilfractor",1)], [("SMB-1","Scrooge McDuck","Ducktales")])

# ── Compute stats ─────────────────────────────────────────────────────────────
print("\nComputing player stats...")
cur.execute("SELECT id FROM players WHERE set_id=?", (SET_ID,))
for (pid,) in cur.fetchall():
    cur.execute("SELECT pa.id, pa.insert_set_id FROM player_appearances pa WHERE pa.player_id=?", (pid,))
    apps = cur.fetchall()
    is_ids = set(a[1] for a in apps)
    uc, tpr, o1 = 0, 0, 0
    for _, isid in apps:
        uc += 1
        cur.execute("SELECT name, print_run FROM parallels WHERE insert_set_id=?", (isid,))
        for _, pr in cur.fetchall():
            uc += 1
            if pr is not None:
                tpr += pr
                if pr == 1: o1 += 1
    cur.execute("UPDATE players SET unique_cards=?, total_print_run=?, one_of_ones=?, insert_set_count=? WHERE id=?", (uc, tpr, o1, len(is_ids), pid))
conn.commit()

cur.execute("SELECT COUNT(*) FROM players WHERE set_id=?", (SET_ID,))
tp = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM insert_sets WHERE set_id=?", (SET_ID,))
ti = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM player_appearances pa JOIN players p ON p.id=pa.player_id WHERE p.set_id=?", (SET_ID,))
ta = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM appearance_co_players ac JOIN player_appearances pa ON pa.id=ac.appearance_id JOIN players p ON p.id=pa.player_id WHERE p.set_id=?", (SET_ID,))
tc = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM parallels par JOIN insert_sets i ON i.id=par.insert_set_id WHERE i.set_id=?", (SET_ID,))
tpar = cur.fetchone()[0]
print(f"\n{'='*50}")
print(f"Set ID:            {SET_ID}")
print(f"Players:           {tp}")
print(f"Insert Sets:       {ti}")
print(f"Appearances:       {ta}")
print(f"Co-player links:   {tc}")
print(f"Parallel types:    {tpar}")
print(f"{'='*50}")
conn.close()
print("\nDone!")
