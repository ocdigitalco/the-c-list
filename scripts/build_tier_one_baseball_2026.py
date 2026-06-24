#!/usr/bin/env python3
"""Build 2026 Topps Tier One Baseball into local SQLite from parsed card data.

Reads /tmp/t1_cards.json (produced by parse_tier_one_baseball_2026.py --json).
Idempotent guard: aborts if the slug already exists.
"""
import sqlite3, json, sys

DB = 'the-c-list.db'
SLUG = '2026-topps-tier-one-baseball'
CARDS = json.load(open('/tmp/t1_cards.json'))

# Ordered subsets: prefix -> display name (parser keys -> human names)
DISPLAY = {
    'BASE1': 'Base Tier 1', 'BASE2': 'Base Tier 2', 'BASE3': 'Base Tier 3',
    'BCA1': 'Base Tier 1 Autographs', 'BCA2': 'Base Tier 2 Autographs',
    'BCA3': 'Base Tier 3 Autographs',
    'T1A': 'Tier One Autographs', 'T1OA': 'Tier One Operators',
    'PPA': 'Prime Performers Autographs', 'BOA': 'Break Out Autographs',
    'T1TA': 'Tier One Talent Autographs', 'TSS': 'Top Shelf Signatures',
    'CCS': 'City Connect Signatures', 'T1S': 'Tier One Shots',
    'CPA': 'Clearly Perfect Autographs', 'MSA': 'Machined Signatures',
    'DA': 'Dual Autographs', 'TA': 'Triple Autographs',
    'T1XA': 'Tier One Xplosion Autographs', 'T1RCA': 'Tier One Rookie Class',
    'CA': 'Connoisseurs', 'R11A': 'Retro 2011 Base Autographs',
    'T1CS': 'Cut Signatures', 'CSR': 'Cut Signature Relics',
    'T1R': 'Tier One Relics', 'DPR': 'Dual Player Relics', 'RR': 'Rookie Relics',
    'T1LR': 'Tier One Legend Relics', 'T1RD': 'Tier One Relics Die Cut',
    'BKR': 'Tier One Bat Knobs', 'LLR': 'Tier One Limited Lumber',
    'GR': 'Gripping Relics', 'JNR': 'Jersey Number Relics', 'SR': 'Shadow Relics',
    'T1TR': 'Tier One Talent Relic', 'PPR': 'Prodigious Patches',
    'GAR': 'Gripping Autographed Relics', 'HHA': 'Hickory and Hide Autographs',
    'APP': 'Autographed Prodigious Patches', 'ADRB': 'Autographed Dual Relics Bat',
    'ARDB': 'Autographed Tier One Relics Die Cut Book',
    'AT1R': 'Autographed Tier One Relics',
    'AT1JR': 'Autographed Tier One Jumbo Relics',
    'BKA': 'Tier One Autographed Bat Knobs',
    'BKSA': 'MLB Bat Knob Sticker Autograph Cards',
    'LLA': 'Tier One Autographed Limited Lumber',
    'MMAR': 'Milestone Material Autograph Relic',
}
ORDER = list(DISPLAY.keys())

# Parallel ladders: prefix -> list of (name, print_run). Empty list = no parallel rows.
L_AUTO5 = lambda base: [('Base', base), ('Blue', 99), ('Green', 49), ('Red', 25),
                        ('Holo Silver', 10), ('Holo Platinum Blue', 1)]
L_REL4 = lambda base: [('Base', base), ('Green', 49), ('Red', 25),
                       ('Holo Silver', 10), ('Holo Platinum Blue', 1)]
LADDERS = {
    'BASE1': [('Base', 99), ('Holo Gold', None), ('Silver', 75), ('Purple', 50),
              ('Blue', 40), ('Green', 30), ('Red', 25), ('Holo Silver', 10),
              ('Pink', 5), ('Holo Platinum Blue', 1), ('Printing Plates', 1)],
    'BASE2': [('Base', 125), ('Bronze', None), ('Holo Gold', None), ('Silver', 99),
              ('Purple', 75), ('Orange', 60), ('Blue', 50), ('Green', 40),
              ('Red', 25), ('Holo Silver', 10), ('Pink', 5),
              ('Holo Platinum Blue', 1), ('Printing Plates', 1)],
    'BASE3': [('Bronze', None), ('Holo Gold', None), ('Blue', 125), ('Green', 99),
              ('Red', 50), ('Holo Silver', 10), ('Pink', 5),
              ('Holo Platinum Blue', 1), ('Printing Plates', 1)],
    'BOA': L_AUTO5(299),
    'T1TA': L_AUTO5(199), 'CCS': L_AUTO5(199), 'T1S': L_AUTO5(199),
    'CPA': [('Base', 75)], 'MSA': [('Base', 49)],
    'T1CS': [('Base', 1)], 'CSR': [('Base', 1)],
    'BKR': [('Base', 1)], 'LLR': [('Base', 1)],
    'GR': [('Base', 10), ('Holo Platinum Blue', 1)],
    'PPR': [('Base', 10), ('Holo Platinum Blue', 1)],
    'JNR': L_REL4(99), 'SR': L_REL4(99), 'T1TR': L_REL4(99),
    'AT1R': [('Base', 199), ('Dual', 99), ('Triple', 49), ('Dual Patch', 10),
             ('Button', 5), ('Triple Patch', 1)],
    'BKA': [('Base', 1)], 'LLA': [('Base', 1)],
}

CELEB_CODES = {'T1CS-CM', 'T1CS-HF', 'T1CS-GP', 'T1CS-JD', 'T1CS-MG',
               'T1CS-OW', 'T1CS-TJ'}
CELEB_NAMES = {CARDS['T1CS']['cards'][i]['subjects'][0]['name']
               for i, c in enumerate(CARDS['T1CS']['cards']) if c['code'] in CELEB_CODES}
NULL_TEAM_CODES = CELEB_CODES | {'T1CS-CB'}  # Cool Papa Bell "Outfield" -> NULL

BOX_CONFIG = json.dumps({
    'hobby': {
        'cards_per_pack': 4, 'packs_per_box': 1, 'boxes_per_case': 12,
        'autographs_per_box': 2, 'memorabilia_per_box': 1,
        'base_or_parallel_per_box': 1,
    }
})


def main():
    db = sqlite3.connect(DB)
    db.execute('PRAGMA foreign_keys=OFF')
    cur = db.cursor()
    if cur.execute('SELECT id FROM sets WHERE slug=?', (SLUG,)).fetchone():
        sys.exit('ABORT: set already exists')

    cur.execute(
        """INSERT INTO sets (name, sport, season, league, tier, sample_image_url,
            pack_odds, box_config, release_date, slug, is_visible, created_at)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,datetime('now'))""",
        ('2026 Topps Tier One Baseball', 'Baseball', '2026', 'MLB', 'Tier One',
         f'/sets/{SLUG}.jpg', None, BOX_CONFIG, '2026-06-24', SLUG, 1))
    set_id = cur.lastrowid

    # players: reuse by (set_id, name)
    players = {}

    def get_player(name, role='athlete'):
        if name in players:
            pid = players[name]
            if role == 'celebrity':
                cur.execute('UPDATE players SET subject_role=? WHERE id=?', (role, pid))
            return pid
        cur.execute(
            """INSERT INTO players (set_id, name, unique_cards, total_print_run,
                one_of_ones, insert_set_count, subject_role)
               VALUES (?,?,0,0,0,0,?)""", (set_id, name, role))
        players[name] = cur.lastrowid
        return players[name]

    counts = {}
    for pfx in ORDER:
        info = CARDS[pfx]
        is_auto = 1 if info['is_autograph'] else 0
        cur.execute('INSERT INTO insert_sets (set_id, name, is_autograph) VALUES (?,?,?)',
                    (set_id, DISPLAY[pfx], is_auto))
        iset_id = cur.lastrowid
        for pname, prun in LADDERS.get(pfx, []):
            cur.execute('INSERT INTO parallels (insert_set_id, name, print_run, exclusivity) VALUES (?,?,?,?)',
                        (iset_id, pname, prun, None))
        n = 0
        for card in info['cards']:
            code = card['code']
            subs = card['subjects']
            prim = subs[0]
            role = 'celebrity' if (code in CELEB_CODES or prim['name'] in CELEB_NAMES) else 'athlete'
            pid = get_player(prim['name'], role)
            team = None if (code in NULL_TEAM_CODES or not prim['team']) else prim['team']
            cur.execute(
                """INSERT INTO player_appearances
                    (player_id, insert_set_id, card_number, is_rookie, subset_tag, team)
                   VALUES (?,?,?,?,?,?)""",
                (pid, iset_id, code, 1 if prim['is_rookie'] else 0, None, team))
            app_id = cur.lastrowid
            for s in subs[1:]:
                co_pid = get_player(s['name'])
                cur.execute('INSERT INTO appearance_co_players (appearance_id, co_player_id) VALUES (?,?)',
                            (app_id, co_pid))
            n += 1
        counts[pfx] = n

    db.commit()
    print(f'set_id={set_id}  players={len(players)}  total_cards={sum(counts.values())}')
    print(f'insert_sets={len(ORDER)}')
    db.close()


if __name__ == '__main__':
    main()
