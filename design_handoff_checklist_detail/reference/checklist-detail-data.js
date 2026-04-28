// Sample data for the Checklist Detail page (2025 Topps Chrome Football)
// Placeholder content — bind to real schema in production.

window.SET_DETAIL = {
  id: 'set-2025-topps-chrome-football',
  name: '2025 Topps Chrome Football',
  sport: 'Football',
  league: 'NFL',
  brand: 'Chrome',
  manufacturer: 'topps',
  releaseDate: '2026-04-15',
  released: 'April 15, 2026',
  athletes: 547,
  cards: 2366,
  cardTypes: 39,
  parallelTypes: 80,
  autographs: 483,
  autoParallels: 9293,
  totalParallels: 35924,
  coverage: {
    athleteChecklist: true,
    numberedParallels: true,
    boxConfig: true,
    packOdds: true,
  },
};

window.BOX_CONFIG = [
  { type: 'Hobby',  cardsPerPack: 4,  packsPerBox: 20, boxesPerCase: 12, packsPerCase: 240, autosPerBox: 1 },
  { type: 'Jumbo',  cardsPerPack: 11, packsPerBox: 12, boxesPerCase: 8,  packsPerCase: 96,  autosPerBox: 2 },
  { type: 'Value',  cardsPerPack: 4,  packsPerBox: 7,  boxesPerCase: null, packsPerCase: null, autosPerBox: null },
  { type: 'Mega',   cardsPerPack: 6,  packsPerBox: 7,  boxesPerCase: 20, packsPerCase: 140, autosPerBox: null },
  { type: 'Hanger', cardsPerPack: 20, packsPerBox: 1,  boxesPerCase: null, packsPerCase: null, autosPerBox: null },
];

window.BOX_CONFIG_NOTES = [
  'Exclusive Red, White, and Blue Refractors',
  'Exclusive Hot Pink and Lime Green X-Fractors',
  'Exclusive Pulsar Refractors',
];

window.PACK_ODDS_TABS = ['Hobby', 'First Day Issue', 'Jumbo', "Breaker's Delight", 'Sapphire', 'Value', 'Mega', 'Hanger', 'Fanatics'];

window.BASE_PARALLELS = [
  { name: 'Base Refractor',          odds: '1:4',     per: '~5.0×' },
  { name: 'Base Prism Refractor',    odds: '1:9',     per: '~2.2×' },
  { name: 'Base Neon Pulse Refractor', odds: '1:30',  per: '1 in ~1.5 boxes' },
  { name: 'Base Teal Refractor',     odds: '1:117',   per: '1 in ~5.8 boxes' },
  { name: 'Base Yellow Wave Refractor', odds: '1:127', per: '1 in ~6.3 boxes' },
  { name: 'Base Pink Refractor',     odds: '1:140',   per: '1 in ~7.0 boxes' },
  { name: 'Base Pink Wave Refractor',odds: '1:140',   per: '1 in ~7.0 boxes' },
  { name: 'Base Team Camo Variation',odds: '1:155',   per: '1 in ~7.8 boxes' },
  { name: 'Base Aqua Refractor',     odds: '1:175',   per: '1 in ~8.8 boxes' },
  { name: 'Base Aqua Wave Refractor',odds: '1:175',   per: '1 in ~8.8 boxes' },
  { name: 'Base Blue Refractor',     odds: '1:232',   per: '1 in ~11.6 boxes' },
  { name: 'Base Blue Wave Refractor',odds: '1:232',   per: '1 in ~11.6 boxes' },
  { name: 'Base Image Variation',    odds: '1:234',   per: '1 in ~11.7 boxes' },
  { name: 'Base Green Refractor',    odds: '1:352',   per: '1 in ~17.6 boxes' },
  { name: 'Base Red Refractor',      odds: '1:6,987', per: '1 in ~349.4 boxes', rare: true },
  { name: 'Base Frozenfractor',      odds: '1:6,987', per: '1 in ~349.4 boxes', rare: true },
  { name: 'Base Red Wave Refractor', odds: '1:6,987', per: '1 in ~349.4 boxes', rare: true },
  { name: 'Base Red Lava Refractor', odds: '1:6,987', per: '1 in ~349.4 boxes', rare: true },
];

window.INSERTS = [
  { name: 'Rookie',                   odds: '1:1',   per: '~20.0×' },
  { name: 'Rookie Refractor',         odds: '1:7',   per: '~2.9×' },
  { name: 'Power Players',            odds: '1:9',   per: '~2.2×' },
  { name: 'Legends Of The Gridiron',  odds: '1:9',   per: '~2.2×' },
  { name: '1975 Topps',               odds: '1:11',  per: '~1.8×' },
  { name: 'Fortune 15',               odds: '1:11',  per: '~1.8×' },
  { name: 'Future Stars',             odds: '1:15',  per: '~1.3×' },
  { name: 'All-Chrome Team',          odds: '1:15',  per: '~1.3×' },
  { name: 'Rookie Prism Refractor',   odds: '1:25',  per: '1 in ~1.3 boxes' },
  { name: 'Rookie Neon Pulse Refractor', odds: '1:90', per: '1 in ~4.5 boxes' },
  { name: 'Rookie Image Variation',   odds: '1:351', per: '1 in ~17.6 boxes' },
  { name: 'Shadow Etch',              odds: '1:387', per: '1 in ~19.4 boxes' },
  { name: 'Rookie Team Camo Variation', odds: '1:464', per: '1 in ~23.2 boxes' },
];

window.AUTOGRAPHS = [
  { name: 'Rookie Auto',              odds: '1:96',   per: '1 in ~4.8 boxes', numbered: '/499' },
  { name: 'Rookie Auto Refractor',    odds: '1:288',  per: '1 in ~14.4 boxes', numbered: '/250' },
  { name: 'Rookie Auto Prism',        odds: '1:480',  per: '1 in ~24.0 boxes', numbered: '/199' },
  { name: 'Rookie Auto Neon Pulse',   odds: '1:1,440',per: '1 in ~72 boxes',  numbered: '/99' },
  { name: 'Veteran Auto',             odds: '1:120',  per: '1 in ~6.0 boxes', numbered: '/350' },
  { name: 'Veteran Auto Refractor',   odds: '1:360',  per: '1 in ~18.0 boxes', numbered: '/199' },
  { name: 'Power Players Auto',       odds: '1:600',  per: '1 in ~30.0 boxes', numbered: '/99' },
  { name: 'Legends Auto',             odds: '1:1,200',per: '1 in ~60 boxes',  numbered: '/50' },
  { name: 'Superfractor Auto',        odds: '1:14,400', per: '1 in ~720 boxes', numbered: '1/1', rare: true },
];

// Athletes — top of leaderboard plus more
window.ATHLETES = [
  { rank: 1,  name: 'Cam Ward',        team: 'Tennessee Titans',     pos: 'QB', rookie: true,  totalCards: 214 },
  { rank: 2,  name: 'Ashton Jeanty',   team: 'Las Vegas Raiders',    pos: 'RB', rookie: true,  totalCards: 210 },
  { rank: 3,  name: 'Puka Nacua',      team: 'Los Angeles Rams',     pos: 'WR', rookie: false, totalCards: 210 },
  { rank: 4,  name: 'Josh Allen',      team: 'Buffalo Bills',        pos: 'QB', rookie: false, totalCards: 209 },
  { rank: 5,  name: 'Tyler Warren',    team: 'Indianapolis Colts',   pos: 'TE', rookie: true,  totalCards: 208 },
  { rank: 6,  name: 'Jayden Daniels',  team: 'Washington Commanders',pos: 'QB', rookie: false, totalCards: 206 },
  { rank: 7,  name: 'Jaxson Dart',     team: 'New York Giants',      pos: 'QB', rookie: true,  totalCards: 205 },
  { rank: 8,  name: 'Bo Nix',          team: 'Denver Broncos',       pos: 'QB', rookie: false, totalCards: 201 },
  { rank: 9,  name: 'Omarion Hampton', team: 'Los Angeles Chargers', pos: 'RB', rookie: true,  totalCards: 198 },
  { rank: 10, name: 'Drake Maye',      team: 'New England Patriots', pos: 'QB', rookie: false, totalCards: 196 },
  { rank: 11, name: 'Brock Bowers',    team: 'Las Vegas Raiders',    pos: 'TE', rookie: false, totalCards: 192 },
  { rank: 12, name: 'Caleb Williams',  team: 'Chicago Bears',        pos: 'QB', rookie: false, totalCards: 188 },
  { rank: 13, name: 'Marvin Harrison Jr.', team: 'Arizona Cardinals',pos: 'WR', rookie: false, totalCards: 184 },
  { rank: 14, name: 'Patrick Mahomes', team: 'Kansas City Chiefs',   pos: 'QB', rookie: false, totalCards: 180 },
  { rank: 15, name: 'CeeDee Lamb',     team: 'Dallas Cowboys',       pos: 'WR', rookie: false, totalCards: 178 },
  { rank: 16, name: 'Saquon Barkley',  team: 'Philadelphia Eagles',  pos: 'RB', rookie: false, totalCards: 175 },
  { rank: 17, name: 'Justin Jefferson',team: 'Minnesota Vikings',    pos: 'WR', rookie: false, totalCards: 172 },
  { rank: 18, name: 'Lamar Jackson',   team: 'Baltimore Ravens',     pos: 'QB', rookie: false, totalCards: 170 },
  { rank: 19, name: 'Tyreek Hill',     team: 'Miami Dolphins',       pos: 'WR', rookie: false, totalCards: 168 },
  { rank: 20, name: "Ja'Marr Chase",   team: 'Cincinnati Bengals',   pos: 'WR', rookie: false, totalCards: 166 },
];
