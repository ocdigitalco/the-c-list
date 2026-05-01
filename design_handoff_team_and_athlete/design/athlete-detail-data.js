// Sample data for the Athlete Detail page
// (Single athlete inside a set — companion to checklist-detail-data.js)

window.ATHLETE_DETAIL = {
  id: 'drake-maye-2025-topps-chrome-football',
  name: 'Drake Maye',
  team: 'New England Patriots',
  teamShort: 'Patriots',
  position: 'QB',
  jersey: 10,
  rookie: false,
  setName: '2025 Topps Chrome Football',
  setHref: '#',
  // Athlete-level totals
  cardTypes: 24,
  totalCards: 196,
  numberedParallels: 2410,
  oneOfOnes: 18,
};

window.TEAM_DETAILS = {
  team: 'New England Patriots',
  teamShort: 'Patriots',
  athletesInSet: 17,
  totalCards: 1842,
  autographs: 38,
  rookies: 4,
  numberedParallels: 18420,
  topAthletes: [
    { name: 'Drake Maye',     position: 'QB', cards: 196 },
    { name: 'Rhamondre Stevenson', position: 'RB', cards: 142 },
    { name: 'DeMario Douglas', position: 'WR', cards: 128 },
  ],
};

window.BREAK_HIT_CALC = {
  cases: 1,
  boxes: 12,
  packs: 240,
  rows: [
    {
      label: 'Any Card',
      sub: 'Based on pack odds across 15 insert sets',
      odds: '99.9%',
      perBox: '~1 in 1 box',
      tone: 'good',
    },
    {
      label: 'Numbered Parallel',
      sub: 'Based on pack odds across 42 numbered parallels',
      odds: '48.9%',
      perBox: '~1 in 2.0 boxes',
      tone: 'medium',
    },
    {
      label: 'Autograph',
      sub: 'Based on pack odds across 9 autograph types',
      odds: '12.4%',
      perBox: '~1 in 8.1 boxes',
      tone: 'low',
    },
  ],
};

// Insert sets the athlete appears in. Each set has cards, parallels, and (optionally)
// per-card details + parallel chips with print runs.
window.INSERT_SETS = [
  {
    name: 'Base',
    kind: 'base',
    cards: 1,
    parallels: 9,
    expandable: true,
    details: {
      cardNumber: '#10',
      subject: 'Drake Maye',
      team: 'New England Patriots',
      parallels: [
        { name: 'Refractor',          run: '/199', tone: 'silver' },
        { name: 'Prism Refractor',    run: '/99',  tone: 'silver' },
        { name: 'Neon Pulse',         run: '/75',  tone: 'orange' },
        { name: 'Aqua Refractor',     run: '/50',  tone: 'teal'   },
        { name: 'Blue Refractor',     run: '/35',  tone: 'blue'   },
        { name: 'Green Refractor',    run: '/15',  tone: 'green'  },
        { name: 'Black Refractor',    run: '/10',  tone: 'black'  },
        { name: 'Red Refractor',      run: '/5',   tone: 'red'    },
        { name: 'Superfractor',       run: '1/1',  tone: 'gold'   },
      ],
    },
  },
  { name: 'Power Players',           kind: 'insert', cards: 1, parallels: 6, expandable: true },
  { name: 'Legends Of The Gridiron', kind: 'insert', cards: 1, parallels: 6, expandable: true },
  { name: '1975 Topps',              kind: 'insert', cards: 1, parallels: 6, expandable: true },
  { name: 'Fortune 15',              kind: 'insert', cards: 1, parallels: 6, expandable: true },
  { name: 'Future Stars',            kind: 'insert', cards: 1, parallels: 4, expandable: true },
  { name: 'All-Chrome Team',         kind: 'insert', cards: 1, parallels: 4, expandable: true },
  { name: 'Shadow Etch',             kind: 'insert', cards: 1, parallels: 3, expandable: true },
  {
    name: 'Image Variations',
    kind: 'variation',
    cards: 1,
    parallels: 3,
    expandable: true,
    highlight: true,
    details: {
      cardNumber: '#10',
      subject: 'Drake Maye',
      team: 'New England Patriots',
      parallels: [
        { name: 'Refractor',          run: '/199', tone: 'silver' },
        { name: 'Aqua Refractor',     run: '/50',  tone: 'teal' },
        { name: 'Red Refractor',      run: '/5',   tone: 'red'  },
      ],
    },
  },
  { name: 'Team Camo Variation',     kind: 'variation', cards: 1, parallels: 3, expandable: true },
];

// Derived: only the themed inserts (used by the "Inserts" tab).
window.INSERTS_ONLY = window.INSERT_SETS.filter(s => s.kind === 'insert');

// Inserts table — set header + parallel rows, structured like AUTOGRAPH_SETS so
// the Autographs table component can render it.
window.INSERT_TABLE = [
  {
    name: 'Power Players',
    cardNumber: '#PP-12',
    subject: 'Drake Maye',
    parallels: [
      { name: 'Power Players',         run: 'unnumbered', odds: '1:24'  },
      { name: 'Refractor',             run: '/199', odds: '1:144'   },
      { name: 'Aqua Refractor',        run: '/50',  odds: '1:576'   },
      { name: 'Blue Refractor',        run: '/25',  odds: '1:1,152' },
      { name: 'Green Refractor',       run: '/15',  odds: '1:1,920' },
      { name: 'Red Refractor',         run: '/5',   odds: '1:5,760', rare: true },
      { name: 'Superfractor',          run: '1/1',  odds: '1:28,800', rare: true },
    ],
  },
  {
    name: 'Legends Of The Gridiron',
    cardNumber: '#LG-8',
    subject: 'Drake Maye',
    parallels: [
      { name: 'Legends Of The Gridiron', run: 'unnumbered', odds: '1:36' },
      { name: 'Refractor',             run: '/199', odds: '1:216'   },
      { name: 'Aqua Refractor',        run: '/50',  odds: '1:864'   },
      { name: 'Blue Refractor',        run: '/25',  odds: '1:1,728' },
      { name: 'Green Refractor',       run: '/15',  odds: '1:2,880' },
      { name: 'Red Refractor',         run: '/5',   odds: '1:8,640', rare: true },
      { name: 'Superfractor',          run: '1/1',  odds: '1:43,200', rare: true },
    ],
  },
  {
    name: '1975 Topps',
    cardNumber: '#75T-4',
    subject: 'Drake Maye',
    parallels: [
      { name: '1975 Topps',            run: 'unnumbered', odds: '1:18' },
      { name: 'Refractor',             run: '/199', odds: '1:108'   },
      { name: 'Aqua Refractor',        run: '/50',  odds: '1:432'   },
      { name: 'Blue Refractor',        run: '/25',  odds: '1:864'   },
      { name: 'Green Refractor',       run: '/15',  odds: '1:1,440' },
      { name: 'Red Refractor',         run: '/5',   odds: '1:4,320', rare: true },
      { name: 'Superfractor',          run: '1/1',  odds: '1:21,600', rare: true },
    ],
  },
  {
    name: 'Fortune 15',
    cardNumber: '#F15-3',
    subject: 'Drake Maye',
    parallels: [
      { name: 'Fortune 15',            run: 'unnumbered', odds: '1:48' },
      { name: 'Refractor',             run: '/199', odds: '1:288'   },
      { name: 'Aqua Refractor',        run: '/50',  odds: '1:1,152' },
      { name: 'Blue Refractor',        run: '/25',  odds: '1:2,304' },
      { name: 'Green Refractor',       run: '/15',  odds: '1:3,840' },
      { name: 'Red Refractor',         run: '/5',   odds: '1:11,520', rare: true },
      { name: 'Superfractor',          run: '1/1',  odds: '1:57,600', rare: true },
    ],
  },
  {
    name: 'Future Stars',
    cardNumber: '#FS-7',
    subject: 'Drake Maye',
    parallels: [
      { name: 'Future Stars',          run: 'unnumbered', odds: '1:30' },
      { name: 'Refractor',             run: '/199', odds: '1:180'   },
      { name: 'Blue Refractor',        run: '/25',  odds: '1:1,440' },
      { name: 'Red Refractor',         run: '/5',   odds: '1:7,200', rare: true },
      { name: 'Superfractor',          run: '1/1',  odds: '1:36,000', rare: true },
    ],
  },
  {
    name: 'All-Chrome Team',
    cardNumber: '#ACT-2',
    subject: 'Drake Maye',
    parallels: [
      { name: 'All-Chrome Team',       run: 'unnumbered', odds: '1:60' },
      { name: 'Refractor',             run: '/199', odds: '1:360'   },
      { name: 'Blue Refractor',        run: '/25',  odds: '1:2,880' },
      { name: 'Red Refractor',         run: '/5',   odds: '1:14,400', rare: true },
      { name: 'Superfractor',          run: '1/1',  odds: '1:72,000', rare: true },
    ],
  },
  {
    name: 'Shadow Etch',
    cardNumber: '#SE-9',
    subject: 'Drake Maye',
    parallels: [
      { name: 'Shadow Etch',           run: '/250', odds: '1:120'   },
      { name: 'Blue Etch',             run: '/25',  odds: '1:1,200' },
      { name: 'Red Etch',              run: '/5',   odds: '1:6,000', rare: true },
    ],
  },
];

window.AUTOGRAPH_SETS = [
  {
    name: 'Rookie Auto',
    cardNumber: '#RA-DM',
    subject: 'Drake Maye',
    team: 'New England Patriots',
    parallels: [
      { name: 'Auto Refractor',    run: '/250', odds: '1:360',    per: '1 in ~18.0 boxes' },
      { name: 'Auto Prism',        run: '/99',  odds: '1:900',    per: '1 in ~45.0 boxes' },
      { name: 'Auto Neon Pulse',   run: '/75',  odds: '1:1,200',  per: '1 in ~60.0 boxes' },
      { name: 'Auto Aqua',         run: '/50',  odds: '1:1,800',  per: '1 in ~90.0 boxes' },
      { name: 'Auto Blue',         run: '/25',  odds: '1:3,600',  per: '1 in ~180 boxes' },
      { name: 'Auto Red',          run: '/5',   odds: '1:18,000', per: '1 in ~900 boxes', rare: true },
      { name: 'Superfractor Auto', run: '1/1',  odds: '1:90,000', per: '1 in ~4,500 boxes', rare: true },
    ],
  },
  {
    name: 'Veteran Auto',
    cardNumber: '#VA-DM',
    subject: 'Drake Maye',
    team: 'New England Patriots',
    parallels: [
      { name: 'Auto Refractor',    run: '/199', odds: '1:288',    per: '1 in ~14.4 boxes' },
      { name: 'Auto Prism',        run: '/99',  odds: '1:480',    per: '1 in ~24.0 boxes' },
      { name: 'Auto Neon Pulse',   run: '/75',  odds: '1:720',    per: '1 in ~36.0 boxes' },
      { name: 'Auto Aqua',         run: '/50',  odds: '1:1,080',  per: '1 in ~54.0 boxes' },
      { name: 'Auto Blue',         run: '/25',  odds: '1:2,160',  per: '1 in ~108 boxes' },
      { name: 'Auto Red',          run: '/5',   odds: '1:10,800', per: '1 in ~540 boxes', rare: true },
      { name: 'Superfractor Auto', run: '1/1',  odds: '1:54,000', per: '1 in ~2,700 boxes', rare: true },
    ],
  },
  {
    name: 'Power Players Auto',
    cardNumber: '#PP-DM',
    subject: 'Drake Maye',
    team: 'New England Patriots',
    parallels: [
      { name: 'Auto',              run: '/99',  odds: '1:1,440', per: '1 in ~72.0 boxes' },
      { name: 'Auto Gold',         run: '/50',  odds: '1:2,880', per: '1 in ~144 boxes' },
      { name: 'Auto Orange',       run: '/25',  odds: '1:5,760', per: '1 in ~288 boxes' },
      { name: 'Auto Red',          run: '/5',   odds: '1:28,800', per: '1 in ~1,440 boxes', rare: true },
      { name: 'Superfractor Auto', run: '1/1',  odds: '1:144,000', per: '1 in ~7,200 boxes', rare: true },
    ],
  },
  {
    name: 'Dual Auto · Maye / Bowers',
    cardNumber: '#DA-MB',
    subject: 'Drake Maye / Kyle Bowers',
    team: 'New England Patriots',
    parallels: [
      { name: 'Auto',              run: '/50',  odds: '1:4,320', per: '1 in ~216 boxes' },
      { name: 'Auto Gold',         run: '/25',  odds: '1:8,640', per: '1 in ~432 boxes' },
      { name: 'Auto Orange',       run: '/10',  odds: '1:21,600', per: '1 in ~1,080 boxes', rare: true },
      { name: 'Auto Red',          run: '/5',   odds: '1:43,200', per: '1 in ~2,160 boxes', rare: true },
      { name: 'Superfractor Auto', run: '1/1',  odds: '1:216,000', per: '1 in ~10,800 boxes', rare: true },
    ],
  },
];

window.ALSO_APPEARS_IN = [
  { name: '2025 Topps Chrome Football Update',  brand: 'Topps Chrome',     year: 2025, sport: 'NFL', cards: 8,  autos: 2, parallels: 56 },
  { name: '2025 Bowman Chrome U Football',      brand: 'Bowman Chrome',    year: 2025, sport: 'NFL', cards: 6,  autos: 1, parallels: 38 },
  { name: '2025 Topps Football Flagship',       brand: 'Topps',            year: 2025, sport: 'NFL', cards: 4,  autos: 0, parallels: 24 },
  { name: '2026 Topps Stadium Club Football',   brand: 'Stadium Club',     year: 2026, sport: 'NFL', cards: 12, autos: 3, parallels: 64 },
  { name: '2026 Topps Chrome Football',         brand: 'Topps Chrome',     year: 2026, sport: 'NFL', cards: 18, autos: 4, parallels: 92 },
  { name: '2026 Topps Finest Football',         brand: 'Topps Finest',     year: 2026, sport: 'NFL', cards: 9,  autos: 2, parallels: 48 },
  { name: '2026 Topps Inception Football',      brand: 'Topps Inception',  year: 2026, sport: 'NFL', cards: 5,  autos: 3, parallels: 32 },
  { name: '2026 Topps Definitive Football',     brand: 'Definitive',       year: 2026, sport: 'NFL', cards: 3,  autos: 2, parallels: 14 },
];

window.ATHLETE_TABS = ['Overview', 'Card Types', 'Base Parallels', 'Inserts', 'Autographs', 'Also Featured In'];
