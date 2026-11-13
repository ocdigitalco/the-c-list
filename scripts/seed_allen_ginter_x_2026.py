"""
Seed: 2026 Topps Allen & Ginter X Baseball — 1,226 cards, 12 subsets, hobby odds + parallels.

Sources:
  scratchpad/agx.jsonl     — 1,226 card rows: subset, card_number, subject, team,
                             optional rookie, optional subject_role (celebrity|attraction).
  scratchpad/agxodds.jsonl — 18 rows: subset lines (parallel=null) carrying hobby odds,
                             and 8 parallel lines (2 numbered mini-base, 6 null-run autos).

Rulings applied (Phase 0 report + go, 2026-11-12):
  - Precedent = set 891 (2026 Topps Allen & Ginter Baseball): tier Standard, non-person
    mini-insert role = 'event' (not the file's 'attraction'), autograph/insert naming
    already matches the file.
  - Rename the three base variations to 891's forms (subsets AND pack_odds keys):
        Base Cards Mini Variation        -> Base Minis
        Base Cards Chrome Variation      -> Chrome Variation
        Base Cards Mini Chrome Variation -> Mini Chrome Variation
    Spot-checks: Base Minis 1:1, Base Minis Silver 1:748, Chrome Variation 1:18,
    Mini Chrome Variation 1:90.
  - Base Minis subset note = the odds sheet's "Base Card Mini Sized Black Parallel"
    text (stored as the subset note, NOT a parallel).
  - Non-person role: file 'attraction' -> 'event' (70 subjects: 50 Ways to Say Hello,
    Musical Methods).
  - Beltre -> Beltré fold: the file carries both 'Adrian Beltré' (Base) and
    'Adrian Beltre' (MA-AB); fold to the accented canonical so both attach to one
    player. => 431 raw subject strings - 1 = 430 players.
  - Garrett Nickelsen: card printed 'M-GN' in Mini Non-Baseball Autographs; stored as
    'MA-GN' with the per-card note "printed M-GN on the Topps checklist" (subset_tag).
  - Anne Hathaway seeds a new Baseball/celebrity node like the other 58 celebrities
    (the Soccer/athlete node 245652 is left untouched); build-athletes keys by
    (name, sport), so no collision.
  - Official-sheet autograph odds stand (Baseball 1:23/1:40/1:140 are the common ones;
    Non-Baseball 1:46/1:85/1:393 the rarer), opposite the pasted list.

Set facts: Baseball / MLB / Standard / season 2026 / release_date 2026-11-11.
box_config hobby only: 8 cards/pack, 18 packs/box, boxes_per_case null, autos_per_box 1
(no notes line). pack_odds.hobby = 17 keys (9 subset + 8 parallel). 8 parallels
(2 numbered, 6 null-run). topps_url NULL (no A&G X precedent has one). No relics, no
booklets, no co-players.

Run post-seed.ts (build-athletes -> backfill-headshots --set -> build-athletes) after
this, then migrate-to-turso.ts --set 2026-topps-allen-ginter-x-baseball.
Usage: python3 scripts/seed_allen_ginter_x_2026.py
"""
import sqlite3, os, json, re, unicodedata

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
JSONL = os.path.join(os.path.dirname(__file__), "..", "scratchpad", "agx.jsonl")
ODDS = os.path.join(os.path.dirname(__file__), "..", "scratchpad", "agxodds.jsonl")

SET_NAME = "2026 Topps Allen & Ginter X Baseball"
SET_SLUG = "2026-topps-allen-ginter-x-baseball"

# rename base variations to the 891 precedent forms (applied to card rows AND odds rows)
SUBSET_RENAME = {
    "Base Cards Mini Variation": "Base Minis",
    "Base Cards Chrome Variation": "Chrome Variation",
    "Base Cards Mini Chrome Variation": "Mini Chrome Variation",
}

# in-set spelling-twin fold: unaccented sheet form -> accented canonical
NAME_FIX = {"Adrian Beltre": "Adrian Beltré"}

# Non-person subjects (50 Ways to Say Hello + Musical Methods): set 891 (2026 A&G
# Baseball) already seeded these same 70 page_kind='none' trivia subjects under dash/
# all-caps forms. Seed 912's under 891's EXACT strings so they merge into the existing
# nodes instead of colliding on the kebab slug and re-slugging 891's live rows (which
# tripped the scoped-push drift guard). 1:1 bijection, verified at build time.
NONPERSON_RENAME = {
    "8-Track Tape Player": "8-TRACK TAPE PLAYER",
    "Aarite (Kriol)": "Aarite - Kriol",
    "Ahoj (Czech)": "Ahoj - Czech",
    "Aloha (Hawaiian)": "Aloha - Hawaiian",
    "Amplifier": "AMPLIFIER",
    "Annyeong haseyo (Korean)": "Annyeong haseyo - Korean",
    "Barev (Armenian)": "Barev - Armenian",
    "Bluetooth Speaker": "BLUETOOTH SPEAKER",
    "Bok (Croatian)": "Bok - Croatian",
    "Bonjour (French)": "Bonjour - French",
    "Boombox": "BOOMBOX",
    "CD Player": "CD PLAYER",
    "Car Stereo": "CAR STEREO",
    "Cassette Player": "CASSETTE PLAYER",
    "Ciao (Italian)": "Ciao - Italian",
    "Dia dhuit (Irish)": "Dia dhuit - Irish",
    "Earbuds": "EARBUDS",
    "Gramophone": "GRAMOPHONE",
    "Gruess Gott (Austrian)": "Gruess Gott - Austrian",
    "Hallo (Afrikaans)": "Hallo - Afrikaans",
    "Hallo (Dutch)": "Hallo - Dutch",
    "Hallo (German)": "Hallo - German",
    "Halo (Indonesian)": "Halo - Indonesian",
    "Headphones": "HEADPHONES",
    "Hei (Norwegian)": "Hei - Norwegian",
    "Hej (Swedish)": "Hej - Swedish",
    "Hello (English)": "Hello - English",
    "Helo (Welsh)": "Helo - Welsh",
    "Hola (Spanish)": "Hola - Spanish",
    "Hyālō (Bengali)": "Hyālō - Bengali",
    "Hēllō (Gujarati)": "Hēllō - Gujarati",
    "In-Ear Monitors": "IN-EAR MONITORS",
    "Jambo (Swahili)": "Jambo - Swahili",
    "Jukebox": "JUKEBOX",
    "Kamisaraki (Aymara)": "Kamisaraki - Aymara",
    "Kia ora (Maori)": "Kia ora - Maori",
    "Konnichiwa (Japanese)": "Konnichiwa - Japanese",
    "Kumusta (Filipino)": "Kumusta - Filipino",
    "MP3 Player": "MP3 PLAYER",
    "Marhaban (Arabic)": "Marhaban - Arabic",
    "Merhaba (Turkish)": "Merhaba - Turkish",
    "Moien (Luxembourgish)": "Moien - Luxembourgish",
    "Namaste (Hindi)": "Namaste - Hindi",
    "Nǐ hǎo (Chinese)": "Nǐ hǎo - Chinese",
    "Olá (Portuguese)": "Olá - Portuguese",
    "Osiyo (Cherokee)": "Osiyo - Cherokee",
    "Phonograph": "PHONOGRAPH",
    "Privet (Russian)": "Privet - Russian",
    "Pryvit (Ukrainian)": "Pryvit - Ukrainian",
    "Pẹlẹ o (Yoruba)": "Pẹlẹ o - Yoruba",
    "Record Player": "RECORD PLAYER",
    "Rimaykullayki (Quechua)": "Rimaykullayki - Quechua",
    "Sain bainuu (Mongolian)": "Sain bainuu - Mongolian",
    "Salam (Pashto)": "Salam - Pashto",
    "Salam (Persian)": "Salam - Persian",
    "Salam (Urdu)": "Salam - Urdu",
    "Salve (Latin)": "Salve - Latin",
    "Sawasdee (Thai)": "Sawasdee - Thai",
    "Sawubona (Zulu)": "Sawubona - Zulu",
    "Shalom (Hebrew)": "Shalom - Hebrew",
    "Shlam l’khon (Aramaic)": "Shlam l’khon - Aramaic",
    "Smartphone": "SMARTPHONE",
    "Soundbar": "SOUNDBAR",
    "Subwoofer": "SUBWOOFER",
    "Transistor Radio": "TRANSISTOR RADIO",
    "Turntable": "TURNTABLE",
    "Vaṇakkam (Tamil)": "Vaṇakkam - Tamil",
    "Xin chào (Vietnamese)": "Xin chào - Vietnamese",
    "Yahsoo (Greek)": "Yahsoo - Greek",
    "Yáʼátʼééh (Navajo)": "Yáʼátʼééh - Navajo",
}

# printed card-number quirk: store MA-GN, annotate the card
CARD_FIX = {("Mini Non-Baseball Autographs", "M-GN"): ("MA-GN", "printed M-GN on the Topps checklist")}

# file subject_role -> our stored role
ROLE_MAP = {"celebrity": "celebrity", "attraction": "event"}

# subset-flag classification (post-rename names)
BASE_SUBSETS = {"Base", "Base Minis", "Chrome Variation", "Mini Chrome Variation"}
AUTOGRAPH_SUBSETS = {"Mini Baseball Autographs", "Mini Non-Baseball Autographs"}
# relics/booklets: none. inserts (no flags): 50 Ways to Say Hello, Musical Methods,
# Rookie Design Variations, N34, N43, Wicked Power


def ren(sub):
    return SUBSET_RENAME.get(sub, sub)


def canon(name):
    name = name.strip()
    name = NAME_FIX.get(name, name)
    name = NONPERSON_RENAME.get(name, name)
    return unicodedata.normalize("NFC", name)


def slugify(t):
    s = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode("ascii")
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")


def to_denom(s):
    return int(s.split(":", 1)[1])


def main():
    rows = [json.loads(l) for l in open(JSONL) if l.strip()]
    assert len(rows) == 1226, f"expected 1226 rows, got {len(rows)}"
    odds = [json.loads(l) for l in open(ODDS) if l.strip()]
    assert len(odds) == 18, f"expected 18 odds rows, got {len(odds)}"

    # ── per-subject role (celebrity/event/athlete), with the Beltré fold applied ──
    subj_role = {}
    for r in rows:
        name = canon(r["subject"])
        role = ROLE_MAP.get(r.get("subject_role"), "athlete")
        prev = subj_role.get(name)
        # a non-athlete role wins if any row carries it (subjects are single-role here)
        if prev is None or (prev == "athlete" and role != "athlete"):
            subj_role[name] = role

    # ── derive pack_odds + parallel rows + subset notes from the odds file ──
    hobby_odds = {}        # pack_odds key -> int denominator
    parallel_rows = []     # (subset, parallel, print_run)
    subset_notes = {}      # subset -> note
    for o in odds:
        sub = ren(o["subset"])
        par = o.get("parallel")
        pr = o.get("print_run")
        hob = (o.get("odds") or {}).get("hobby")
        if not par:
            key = sub
            if o.get("note"):
                subset_notes[sub] = o["note"]
        else:
            parallel_rows.append((sub, par, pr))
            key = f"{sub} {par}"
        if hob:
            hobby_odds[key] = to_denom(hob)
    assert len(parallel_rows) == 8, f"expected 8 parallels, got {len(parallel_rows)}"
    assert len(hobby_odds) == 17, f"expected 17 hobby odds keys, got {len(hobby_odds)}"

    box_config = json.dumps({
        "hobby": {
            "cards_per_pack": 8, "packs_per_box": 18, "boxes_per_case": None,
            "autos_per_box": 1,
        },
    })
    pack_odds = json.dumps({"hobby": hobby_odds})

    db = sqlite3.connect(DB_PATH)
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA foreign_keys=ON")

    if db.execute("SELECT id FROM sets WHERE name = ?", (SET_NAME,)).fetchone():
        raise SystemExit(f"Set '{SET_NAME}' already exists — aborting.")

    try:
        cur = db.execute(
            """INSERT INTO sets (name, sport, season, league, tier, slug, is_visible,
                   sample_image_url, release_date, box_config, pack_odds, topps_url, created_at)
               VALUES (?, 'Baseball', '2026', 'MLB', 'Standard', ?, 1, ?, ?, ?, ?, NULL, ?)""",
            (SET_NAME, SET_SLUG, f"/sets/{SET_SLUG}.jpg", "2026-11-11", box_config,
             pack_odds, "2026-11-12T12:00:00Z"),
        )
        set_id = cur.lastrowid
        print(f"Created set id {set_id}")

        slug_cache = {}

        def goc(name):
            name = canon(name)
            r = db.execute("SELECT id FROM players WHERE set_id=? AND name=?", (set_id, name)).fetchone()
            if r:
                return r[0]
            role = subj_role.get(name, "athlete")
            base = slugify(name) or "player"
            c, i = base, 2
            while c in slug_cache:
                c = f"{base}-{i}"; i += 1
            slug_cache[c] = True
            return db.execute(
                """INSERT INTO players (set_id, name, slug, unique_cards, total_print_run,
                       one_of_ones, insert_set_count, subject_role)
                   VALUES (?, ?, ?, 0, 0, 0, 0, ?)""",
                (set_id, name, c, role),
            ).lastrowid

        # ── insert_sets in JSONL first-appearance order (post-rename) ──
        is_ids = {}
        for r in rows:
            sub = ren(r["subset"])
            if sub in is_ids:
                continue
            is_ids[sub] = db.execute(
                """INSERT INTO insert_sets (set_id, name, is_base, is_autograph, is_relic,
                       is_booklet, print_run, notes)
                   VALUES (?, ?, ?, ?, 0, 0, NULL, ?)""",
                (set_id, sub,
                 1 if sub in BASE_SUBSETS else 0,
                 1 if sub in AUTOGRAPH_SUBSETS else 0,
                 subset_notes.get(sub)),
            ).lastrowid
        print(f"Created {len(is_ids)} subsets")

        for sub, _, _ in parallel_rows:
            assert sub in is_ids, f"parallel subset not in checklist: {sub!r}"
        for key in hobby_odds:
            pass  # keys validated by construction (subset or 'subset parallel')

        # ── parallels ──
        for sub, par, pr in parallel_rows:
            db.execute(
                "INSERT INTO parallels (insert_set_id, name, print_run) VALUES (?, ?, ?)",
                (is_ids[sub], par, pr))

        # ── appearances (one per card row; no co-players) ──
        for r in rows:
            sub = ren(r["subset"])
            card = str(r["card_number"])
            tag = None
            fix = CARD_FIX.get((sub, card))
            if fix:
                card, tag = fix
            isid = is_ids[sub]
            pid = goc(r["subject"])
            db.execute(
                """INSERT INTO player_appearances
                       (player_id, insert_set_id, card_number, is_rookie, team, subset_tag)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (pid, isid, card, 1 if r.get("rookie") else 0, r.get("team"), tag),
            )

        db.commit()

        # ── verification ──
        def q1(sql, *a):
            return db.execute(sql, a).fetchone()[0]

        n_sub = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=?", set_id)
        n_base = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_base=1", set_id)
        n_auto = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_autograph=1", set_id)
        n_relic = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_relic=1", set_id)
        n_bk = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND is_booklet=1", set_id)
        n_pr = q1("SELECT COUNT(*) FROM insert_sets WHERE set_id=? AND print_run IS NOT NULL", set_id)
        n_cards = q1("""SELECT COUNT(DISTINCT pa.insert_set_id || ':' || pa.card_number)
                        FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                        WHERE i.set_id=?""", set_id)
        n_app = q1("""SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                      WHERE i.set_id=?""", set_id)
        n_players = q1("SELECT COUNT(*) FROM players WHERE set_id=?", set_id)
        n_rookie = q1("""SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                         WHERE i.set_id=? AND pa.is_rookie=1""", set_id)
        n_athlete = q1("SELECT COUNT(*) FROM players WHERE set_id=? AND subject_role='athlete'", set_id)
        n_celeb = q1("SELECT COUNT(*) FROM players WHERE set_id=? AND subject_role='celebrity'", set_id)
        n_event = q1("SELECT COUNT(*) FROM players WHERE set_id=? AND subject_role='event'", set_id)
        n_par = q1("""SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id
                      WHERE i.set_id=?""", set_id)
        n_par_pr = q1("""SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id
                         WHERE i.set_id=? AND p.print_run IS NOT NULL""", set_id)
        n_colink = q1("""SELECT COUNT(*) FROM appearance_co_players acp
                         JOIN player_appearances pa ON pa.id=acp.appearance_id
                         JOIN insert_sets i ON i.id=pa.insert_set_id WHERE i.set_id=?""", set_id)
        n_oddskeys = len(json.loads(q1("SELECT pack_odds FROM sets WHERE id=?", set_id))["hobby"])
        beltre_bad = q1("SELECT COUNT(*) FROM players WHERE set_id=? AND name='Adrian Beltre'", set_id)
        beltre_ok = q1("SELECT COUNT(*) FROM players WHERE set_id=? AND name='Adrian Beltré'", set_id)
        magn = q1("""SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                     WHERE i.set_id=? AND pa.card_number='MA-GN'""", set_id)
        mgn_bad = q1("""SELECT COUNT(*) FROM player_appearances pa JOIN insert_sets i ON i.id=pa.insert_set_id
                        WHERE i.set_id=? AND pa.card_number='M-GN'""", set_id)

        print(f"subsets={n_sub} (base={n_base} auto={n_auto} relic={n_relic} booklet={n_bk})")
        print(f"subset_print_runs={n_pr}  cards={n_cards}  appearances={n_app}  players={n_players}")
        print(f"rookie_appearances={n_rookie}  roles: athlete={n_athlete} celebrity={n_celeb} event={n_event}")
        print(f"parallels={n_par} (numbered={n_par_pr})  pack_odds_hobby_keys={n_oddskeys}  co_links={n_colink}")
        print(f"Beltré fold: 'Adrian Beltre'={beltre_bad} (want 0)  'Adrian Beltré'={beltre_ok} (want 1)")
        print(f"MA-GN present={magn} (want 1)  M-GN present={mgn_bad} (want 0)")

        assert n_sub == 12 and (n_base, n_auto, n_relic, n_bk) == (4, 2, 0, 0), "subset-flag gate failed"
        assert n_pr == 0, "subset print_run gate failed (expected all NULL)"
        assert n_cards == 1226, "card count gate failed"
        assert n_app == 1226, "appearance count gate failed (no co-players)"
        assert n_rookie == 284, "rookie gate failed (expected 284)"
        assert n_players == 430, "player gate failed (431 strings - 1 Beltré fold = 430)"
        assert (n_athlete, n_celeb, n_event) == (301, 59, 70), "role gate failed (301/59/70)"
        assert n_par == 8 and n_par_pr == 2, "parallel gate failed (8 total, 2 numbered)"
        assert n_oddskeys == 17, "pack_odds gate failed (17 hobby keys)"
        assert n_colink == 0, "co-player gate failed (expected 0)"
        assert beltre_bad == 0 and beltre_ok == 1, "Beltré fold gate failed"
        assert magn == 1 and mgn_bad == 0, "MA-GN gate failed"
        assert json.loads(pack_odds)["hobby"]["Base Minis"] == 1, "spot-check Base Minis 1:1 failed"
        assert json.loads(pack_odds)["hobby"]["Base Minis Silver"] == 748, "spot-check Base Minis Silver failed"
        assert json.loads(pack_odds)["hobby"]["Chrome Variation"] == 18, "spot-check Chrome Variation failed"
        assert json.loads(pack_odds)["hobby"]["Mini Chrome Variation"] == 90, "spot-check Mini Chrome Variation failed"
        print("ALL LOCAL GATES PASSED.")
        print(f"DONE. set id {set_id}")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
