#!/usr/bin/env python3
"""Build 2026 Topps Knockout UFC into local SQLite from the inline prompt data.

Parses card lines from /tmp/ufc_prompt.txt by exact code-prefix (unambiguous),
which avoids hand-transcription error. Idempotent: aborts if slug already exists.
Writes ONLY to local the-c-list.db. Does NOT touch Turso.
"""
import sqlite3, json, re, sys

DB = 'the-c-list.db'
SLUG = '2026-topps-knockout-ufc'
SRC = '/tmp/ufc_prompt.txt'

# ---- parallel ladders -------------------------------------------------------
P_BASE_SET = [('Bronze',299),('Gold',199),('Teal',149),('Holo Silver',125),
              ('Lime Green',99),('Orange',88),('Blue',50),('Red',25),
              ('Black & White',15),('Black',10),('Holo Gold',8),('Emerald',5),
              ('Platinum',1)]
P_AUTO5   = [('Lime Green',99),('Blue',50),('Red',25),('Gold',8),('Platinum',1)]
P_GP      = [('Gold',8),('Platinum',1)]
P_REL4    = [('Blue',50),('Red',25),('Gold',8),('Platinum',1)]
P_UFCR    = [('Emerald',5),('Platinum',1)]
P_INS7    = [('Lime Green',99),('Blue',50),('Red',25),('Black',10),('Gold',8),
             ('Emerald',5),('Platinum',1)]
P_MUSEUM  = [('Blue',50),('Red',25),('Black',10),('Gold',8),('Emerald',5),
             ('Platinum',1)]

# ---- subset definitions (in display order) ----------------------------------
# (display_name, prefixes, is_auto, base_run, parallels, multi_n, expected)
SUBSETS = [
    ('Base Set',                          ['__BASE__'], 0, None, P_BASE_SET, 1, 100),
    ('Knockout Autographs',               ['KOA-'],     1, 299,  P_AUTO5,    1, 57),
    ('Octagon Warriors Signatures',       ['OWS-'],     1, 299,  P_AUTO5,    1, 29),
    ('Collageagraphs',                    ['CGS-'],     1, 99,   P_GP,       1, 27),
    ('Inception Signatures',              ['INS-'],     1, 99,   P_GP,       1, 25),
    ('AKA Ink',                           ['AKA-'],     1, 25,   P_GP,       1, 18),
    ('Distinctive Signs',                 ['DDS-','DSS-'], 1, 25, P_GP,      1, 9),
    ('Dynamic Duels',                     ['DD-'],      1, 25,   [],         2, 9),
    ('Triumphant Trios',                  ['TT-'],      1, 10,   [],         3, 4),
    ('From The Rafters Autograph Booklets',['FTR-'],    1, 10,   [],         1, 19),
    ('UFC Staredown Signatures Booklets', ['SS-'],      1, 10,   [],         2, 10),
    ('Quad Autograph Booklets',           ['QAB-'],     1, 10,   [],         4, 6),
    ('Tier 1 Dual Relic Autographs',      ['TOA-'],     1, 299,  P_AUTO5,    1, 21),
    ('Knockout Autographed Relics',       ['KAR-'],     1, 299,  P_AUTO5,    1, 30),
    ('Autographed Fight Mat Relics',      ['AFM-'],     1, 299,  P_AUTO5,    1, 18),
    ('Triple Threads Autographed Relics', ['TTA-'],     1, 99,   P_REL4,     1, 13),
    ('Knockout Relics',                   ['KOR-'],     0, 199,  P_REL4,     1, 51),
    ('1-2 Combo Relics',                  ['OTC-'],     0, 199,  P_REL4,     1, 25),
    ('Triple Threads Relics',             ['TTR-'],     0, 199,  P_REL4,     1, 17),
    ('UFC Relics',                        ['UFCR-'],    0, 10,   P_UFCR,     1, 50),
    ('Knockout Artists',                  ['KA-'],      0, None, P_INS7,     1, 25),
    ('Final Face Off',                    ['FF-'],      0, None, P_INS7,     2, 10),
    ('Octagon Successors',                ['OS-'],      0, None, P_INS7,     2, 30),
    ('Instant Arrival',                   ['IA-'],      0, None, P_INS7,     1, 20),
    ('Fight DNA',                         ['DNA-'],     0, None, P_INS7,     1, 15),
    ('Museum Collection',                 ['MC-'],      0, None, P_MUSEUM,   1, 100),
]

BOX_CONFIG = json.dumps({
    'hobby': {
        'cards_per_pack': 8, 'packs_per_box': 4, 'boxes_per_case': 8,
        'premium_autographs_per_box': 3, 'autograph_relic_per_box': 1,
    }
})

SERIAL_RE = re.compile(r'\s*/\d+\s*$')
NICK_RE   = re.compile(r"'([^']*)'")


def parse_subject(s):
    """Return (name, is_rookie, nickname) from a single subject string."""
    nick = None
    m = NICK_RE.search(s)
    if m:
        nick = m.group(1)
        s = NICK_RE.sub('', s).strip()
    is_rc = 0
    if s.endswith(' RC'):
        is_rc = 1
        s = s[:-3].strip()
    elif s == 'RC':
        pass
    s = re.sub(r'\s+', ' ', s).strip()
    return s, is_rc, nick


def parse_cards(lines, prefixes, base_numeric):
    cards = []
    if base_numeric:  # base set: lines like "1 Conor McGregor" / "36 Name RC"
        for ln in lines:
            t = ln.strip()
            m = re.match(r'^(\d+)\s+(.+)$', t)
            if not m:
                continue
            num, rest = m.group(1), m.group(2)
            name, rc, _ = parse_subject(rest)
            cards.append({'code': num, 'subjects': [(name, rc, None)]})
        return cards
    for ln in lines:
        t = ln.strip()
        code = None
        for p in prefixes:
            if t.startswith(p):
                code = t.split()[0]
                break
        if code is None:
            continue
        rest = t[len(code):].strip()
        rest = SERIAL_RE.sub('', rest).strip()           # drop trailing /NN serial
        parts = [p.strip() for p in rest.split(' / ') if p.strip()]
        subs = [parse_subject(p) for p in parts]
        cards.append({'code': code, 'subjects': subs})
    return cards


def main():
    raw = open(SRC, encoding='utf-8').read().splitlines()
    # Base set region: between "BASE SET — 100 cards" and the "AUTOGRAPHS" divider.
    def idx(pred):
        for i, l in enumerate(raw):
            if pred(l):
                return i
        return -1
    base_start = idx(lambda l: l.strip().startswith('BASE SET'))
    base_end   = idx(lambda l: l.strip() == 'AUTOGRAPHS')
    verify_start = idx(lambda l: l.strip().startswith('POST-INSERT VERIFICATION'))
    base_lines = raw[base_start:base_end]
    # Restrict prefix parsing to the card-body region only. This excludes the
    # RECONCILIATION NOTES above BASE SET (which contain example lines like
    # "INS-DD ..." and "KOR-BO ..." that are NOT cards) and the verification
    # table below, both of which otherwise pollute prefix matches.
    body_lines = raw[base_start:verify_start]

    db = sqlite3.connect(DB)
    db.execute('PRAGMA foreign_keys=OFF')
    cur = db.cursor()
    if cur.execute('SELECT id FROM sets WHERE slug=?', (SLUG,)).fetchone():
        sys.exit('ABORT: set already exists')

    cur.execute(
        """INSERT INTO sets (name, sport, season, league, tier, sample_image_url,
            pack_odds, box_config, release_date, slug, is_visible, created_at)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,datetime('now'))""",
        ('2026 Topps Knockout UFC', 'MMA', '2026', 'UFC', 'Standard',
         f'/sets/{SLUG}.jpg', None, BOX_CONFIG, None, SLUG, 1))
    set_id = cur.lastrowid

    players = {}

    def get_player(name):
        if name in players:
            return players[name]
        cur.execute(
            """INSERT INTO players (set_id, name, unique_cards, total_print_run,
                one_of_ones, insert_set_count, subject_role)
               VALUES (?,?,0,0,0,0,'athlete')""", (set_id, name))
        players[name] = cur.lastrowid
        return players[name]

    report = []
    for disp, prefixes, is_auto, base_run, parallels, multi_n, expected in SUBSETS:
        cur.execute('INSERT INTO insert_sets (set_id, name, is_autograph) VALUES (?,?,?)',
                    (set_id, disp, is_auto))
        iset_id = cur.lastrowid
        ladder = ([('Base', base_run)] if base_run is not None else []) + parallels
        for pn, pr in ladder:
            cur.execute('INSERT INTO parallels (insert_set_id, name, print_run, exclusivity) VALUES (?,?,?,?)',
                        (iset_id, pn, pr, None))

        is_base_numeric = (prefixes == ['__BASE__'])
        src_lines = base_lines if is_base_numeric else body_lines
        cards = parse_cards(src_lines, prefixes, is_base_numeric)

        co_links = 0
        for card in cards:
            subs = card['subjects']
            pname, prc, pnick = subs[0]
            pid = get_player(pname)
            subset_tag = pnick  # AKA Ink nickname preserved here; else None
            cur.execute(
                """INSERT INTO player_appearances
                    (player_id, insert_set_id, card_number, is_rookie, subset_tag, team)
                   VALUES (?,?,?,?,?,?)""",
                (pid, iset_id, card['code'], prc, subset_tag, None))
            app_id = cur.lastrowid
            for cname, _crc, _cn in subs[1:]:
                co_pid = get_player(cname)
                cur.execute('INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?,?)',
                            (app_id, co_pid))
                co_links += 1
        report.append((disp, len(cards), expected, is_auto, multi_n, co_links))

    db.commit()
    print(f'set_id={set_id}  players={len(players)}')
    print(f'{"subset":40s} {"got":>4} {"exp":>4} {"auto":>4} {"co":>4}')
    total = 0
    for disp, got, exp, is_auto, multi_n, co in report:
        flag = '' if got == exp else '  <-- MISMATCH'
        co_exp = (multi_n - 1) * exp if multi_n > 1 else 0
        coflag = '' if co == co_exp else f'  CO!={co_exp}'
        print(f'{disp:40s} {got:>4} {exp:>4} {is_auto:>4} {co:>4}{flag}{coflag}')
        total += got
    print(f'{"TOTAL":40s} {total:>4}')
    db.close()


if __name__ == '__main__':
    main()
