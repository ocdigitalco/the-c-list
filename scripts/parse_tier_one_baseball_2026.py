#!/usr/bin/env python3
"""Parse 2026 Topps Tier One Baseball checklist PDF into structured card data.

Position-based parser: groups words into rows by y-coordinate, splits columns by
x-coordinate (code / name / team / Rookie marker). Sections delimited by all-caps
header rows. Multi-subject cards detected by a repeated card code within a subset.

Run with --dry-run to print the per-subset count table vs the spec expected counts.
Run with --json <path> to dump parsed card data for the build step.
"""
import sys, re, json
import pdfplumber

PDF = '/Users/tyler/Downloads/CheckList_26T1BB.pdf'

CODE_RE = re.compile(r'^[A-Z0-9]+-[A-Z0-9]+$')      # e.g. BCA-APU, ADRB-BW, BKSA-BB1
GLYPHS = '\u00ae\u2122'                               # ® ™

# Column x-boundaries (validated against word dump)
NAME_X = 128.0
TEAM_X = 268.0
ROOKIE_X = 420.0

GROUP_HEADERS = {'BASE', 'AUTOGRAPH', 'RELIC', 'AUTOGRAPH RELIC'}

# Ordered subset spec: header_text -> (prefix, expected_count, group, is_autograph, multi_subjects)
# multi_subjects: 0 = single subject; N = each card has N subjects
SUBSETS = [
    ('BASE TIER 1',                              ('BASE1', 20, 'base', False, 0)),
    ('BASE TIER 2',                              ('BASE2', 50, 'base', False, 0)),
    ('BASE TIER 3',                              ('BASE3', 30, 'base', False, 0)),
    ('BASE TIER 1 AUTOGRAPHS',                   ('BCA1', 9,  'auto', True, 0)),
    ('BASE TIER 2 AUTOGRAPHS',                   ('BCA2', 27, 'auto', True, 0)),
    ('BASE TIER 3 AUTOGRAPHS',                   ('BCA3', 28, 'auto', True, 0)),
    ('TIER ONE AUTOGRAPHS',                      ('T1A', 33, 'auto', True, 0)),
    ('TIER ONE OPERATORS',                       ('T1OA', 20, 'auto', True, 0)),
    ('PRIME PERFORMERS AUTOGRAPHS',              ('PPA', 60, 'auto', True, 0)),
    ('BREAK OUT AUTOGRAPHS',                     ('BOA', 83, 'auto', True, 0)),
    ('TIER ONE TALENT AUTOGRAPHS',               ('T1TA', 37, 'auto', True, 0)),
    ('TOP SHELF SIGNATURES',                     ('TSS', 20, 'auto', True, 0)),
    ('CITY CONNECT SIGNATURES',                  ('CCS', 17, 'auto', True, 0)),
    ('TIER ONE SHOTS',                           ('T1S', 18, 'auto', True, 0)),
    ('CLEARLY PERFECT AUTOGRAPHS',               ('CPA', 22, 'auto', True, 0)),
    ('MACHINED SIGNATURES',                      ('MSA', 21, 'auto', True, 0)),
    ('DUAL AUTOGRAPHS',                          ('DA', 9, 'auto', True, 2)),
    ('TRIPLE AUTOGRAPHS',                        ('TA', 2, 'auto', True, 3)),
    ('TIER ONE XPLOSION AUTOGRAPHS',             ('T1XA', 38, 'auto', True, 0)),
    ('TIER ONE ROOKIE CLASS',                    ('T1RCA', 17, 'auto', True, 0)),
    ('CONNOISSEURS',                             ('CA', 18, 'auto', True, 0)),
    ('RETRO 2011 BASE AUTOGRAPHS',               ('R11A', 20, 'auto', True, 0)),
    ('CUT SIGNATURES',                           ('T1CS', 61, 'relic', True, 0)),  # cut autos
    ('CUT SIGNATURE RELICS',                     ('CSR', 13, 'relic', False, 0)),
    ('TIER ONE RELICS',                          ('T1R', 79, 'relic', False, 0)),
    ('DUAL PLAYER RELICS',                       ('DPR', 22, 'relic', False, 2)),
    ('ROOKIE RELICS',                            ('RR', 11, 'relic', False, 0)),
    ('TIER ONE LEGEND RELICS',                   ('T1LR', 22, 'relic', False, 0)),
    ('TIER ONE RELICS DIE CUT',                  ('T1RD', 33, 'relic', False, 0)),
    ('TIER ONE BAT KNOBS',                       ('BKR', 87, 'relic', False, 0)),
    ('TIER ONE LIMITED LUMBER',                  ('LLR', 161, 'relic', False, 0)),
    ('GRIPPING RELICS',                          ('GR', 30, 'relic', False, 0)),
    ('JERSEY NUMBER RELICS',                     ('JNR', 25, 'relic', False, 0)),
    ('SHADOW RELICS',                            ('SR', 34, 'relic', False, 0)),
    ('TIER ONE TALENT RELIC',                    ('T1TR', 20, 'relic', False, 0)),
    ('PRODIGIOUS PATCHES',                       ('PPR', 44, 'relic', False, 0)),
    ('GRIPPING AUTOGRAPHED RELICS',              ('GAR', 25, 'autorelic', True, 0)),
    ('HICKORY AND HIDE AUTOGRAPHS',              ('HHA', 9, 'autorelic', True, 0)),
    ('AUTOGRAPHED PRODIGIOUS PATCHES',           ('APP', 38, 'autorelic', True, 0)),
    ('AUTOGRAPHED DUAL RELICS BAT',              ('ADRB', 12, 'autorelic', True, 2)),
    ('AUTOGRAPHED TIER ONE RELICS DIE CUT BOOK', ('ARDB', 29, 'autorelic', True, 0)),
    ('AUTOGRAPHED TIER ONE RELICS',              ('AT1R', 86, 'autorelic', True, 0)),
    ('AUTOGRAPHED TIER ONE JUMBO RELICS',        ('AT1JR', 55, 'autorelic', True, 0)),
    ('TIER ONE AUTOGRAPHED BAT KNOBS',           ('BKA', 89, 'autorelic', True, 0)),
    ('MLB BAT KNOB STICKER AUTOGRAPH CARDS',     ('BKSA', 11, 'autorelic', True, 0)),
    ('TIER ONE AUTOGRAPHED LIMITED LUMBER',      ('LLA', 82, 'autorelic', True, 0)),
    ('MILESTONE MATERIAL AUTOGRAPH RELIC',       ('MMAR', 1, 'autorelic', True, 0)),
]
HEADER_LOOKUP = {h: spec for h, spec in SUBSETS}
SUBSET_ORDER = [spec[0] for _, spec in SUBSETS]


def cluster_rows(words):
    """Group words on a page into rows by top coordinate."""
    rows = {}
    for w in words:
        key = None
        for t in rows:
            if abs(t - w['top']) <= 6:
                key = t
                break
        if key is None:
            key = w['top']
            rows[key] = []
        rows[key].append(w)
    out = []
    for top in sorted(rows):
        ws = sorted(rows[top], key=lambda w: w['x0'])
        out.append(ws)
    return out


def row_is_header(ws):
    first = ws[0]['text']
    if CODE_RE.match(first) or first.isdigit():
        return False
    # join non-rookie-column text; header if all letters uppercase
    txt = ' '.join(w['text'] for w in ws if w['x0'] < ROOKIE_X)
    letters = [c for c in txt if c.isalpha()]
    return bool(letters) and all(c.isupper() for c in letters)


def parse_row(ws):
    code = ws[0]['text']
    name_words, team_words = [], []
    is_rookie = False
    for w in ws[1:]:
        if w['x0'] >= ROOKIE_X:
            if w['text'].strip().lower() == 'rookie':
                is_rookie = True
        elif w['x0'] >= TEAM_X:
            team_words.append(w['text'])
        else:
            name_words.append(w['text'])
    name = ' '.join(name_words)
    team = ' '.join(team_words)
    for g in GLYPHS:
        team = team.replace(g, '')
    team = team.strip()
    # also strip a trailing 'Rookie' that slipped into name/team text columns
    if name.endswith(' Rookie'):
        name = name[:-7].strip(); is_rookie = True
    if team.endswith(' Rookie'):
        team = team[:-7].strip(); is_rookie = True
    return code, name, team, is_rookie


def parse():
    pdf = pdfplumber.open(PDF)
    sections = {}       # prefix -> list of cards
    order = []
    current = None      # (prefix, multi)
    header_text_buffer = ''
    for page in pdf.pages:
        for ws in cluster_rows(page.extract_words()):
            txt = ' '.join(w['text'] for w in ws if w['x0'] < ROOKIE_X).strip()
            if row_is_header(ws):
                if txt in GROUP_HEADERS:
                    continue
                if txt in HEADER_LOOKUP:
                    spec = HEADER_LOOKUP[txt]
                    current = spec
                    if spec[0] not in sections:
                        sections[spec[0]] = []
                        order.append(spec[0])
                    continue
                # unknown header -> flag
                raise SystemExit(f'UNKNOWN HEADER: {txt!r}')
            if current is None:
                continue
            # A real data row must start with a token in the CODE column (x0 < NAME_X).
            # Rows whose only/leading token sits in the rookie column (e.g. a lone
            # "Rookie" marker that wrapped) are continuations of the previous card.
            if ws[0]['x0'] >= NAME_X:
                if any(w['x0'] >= ROOKIE_X and w['text'].strip().lower() == 'rookie' for w in ws):
                    if sections[current[0]]:
                        sections[current[0]][-1]['is_rookie'] = True
                continue
            code, name, team, is_rookie = parse_row(ws)
            sections[current[0]].append({
                'code': code, 'name': name, 'team': team, 'is_rookie': is_rookie,
            })
    return sections, order


def group_cards(prefix, rows, multi):
    """Group rows into cards. Multi-subject cards share a code across consecutive rows."""
    cards = []
    by_code = {}
    for r in rows:
        by_code.setdefault(r['code'], []).append(r)
    # preserve first-seen order
    seen = []
    for r in rows:
        if r['code'] not in seen:
            seen.append(r['code'])
    for code in seen:
        subs = by_code[code]
        cards.append({'code': code, 'subjects': subs})
    return cards


def main():
    sections, order = parse()
    print(f'{"SUBSET":<42} {"prefix":<7} {"exp":>4} {"got":>4} {"subj":>5}  status')
    print('-' * 78)
    total_cards = 0
    mismatches = []
    for header, (prefix, exp, grp, is_auto, multi) in SUBSETS:
        rows = sections.get(prefix, [])
        cards = group_cards(prefix, rows, multi)
        got = len(cards)
        total_cards += got
        # subject distribution
        subj_counts = sorted(set(len(c['subjects']) for c in cards)) if cards else []
        subj_str = ','.join(str(s) for s in subj_counts)
        status = 'OK' if got == exp else f'*** MISMATCH (exp {exp})'
        if got != exp:
            mismatches.append((header, prefix, exp, got))
        # multi-subject validation
        if multi:
            bad = [c['code'] for c in cards if len(c['subjects']) != multi]
            if bad:
                status += f' subj!=expected:{bad[:5]}'
        print(f'{header:<42} {prefix:<7} {exp:>4} {got:>4} {subj_str:>5}  {status}')
    print('-' * 78)
    print(f'TOTAL CARDS (distinct, all subsets): {total_cards}')
    print(f'MISMATCHES: {len(mismatches)}')
    for m in mismatches:
        print('  ', m)

    if '--json' in sys.argv:
        path = sys.argv[sys.argv.index('--json') + 1]
        out = {}
        for header, (prefix, exp, grp, is_auto, multi) in SUBSETS:
            rows = sections.get(prefix, [])
            cards = group_cards(prefix, rows, multi)
            out[prefix] = {
                'header': header, 'group': grp, 'is_autograph': is_auto,
                'multi': multi, 'cards': cards,
            }
        json.dump(out, open(path, 'w'), ensure_ascii=False, indent=1)
        print(f'\nWrote {path}')


if __name__ == '__main__':
    main()
