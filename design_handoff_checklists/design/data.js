// Sport taxonomy + fictional card sets
window.SPORTS = [
  { id: 'all', label: 'All' },
  { id: 'basketball', label: 'Basketball' },
  { id: 'baseball', label: 'Baseball' },
  { id: 'soccer', label: 'Soccer' },
  { id: 'mma', label: 'MMA' },
  { id: 'wrestling', label: 'Wrestling' },
  { id: 'racing', label: 'Racing' },
  { id: 'football', label: 'Football' },
  { id: 'entertainment', label: 'Entertainment' },
  { id: 'boxing', label: 'Boxing' },
  { id: 'hockey', label: 'Hockey' },
  { id: 'olympics', label: 'Olympics' },
  { id: 'other', label: 'Other' },
];

// Palettes for card-art placeholders, tagged by sport
window.SPORT_PALETTES = {
  basketball: ['#E86A2C', '#1C1917', '#F4E3C1'],
  baseball:   ['#0B3D91', '#FAF4E6', '#C8102E'],
  soccer:     ['#0F7B3B', '#F4D03F', '#0B3D91'],
  mma:        ['#3A2D6E', '#D81E5B', '#F3F3F3'],
  wrestling:  ['#B8251F', '#F2C230', '#111111'],
  racing:     ['#111111', '#E10600', '#F5F5F5'],
  football:   ['#1E3A8A', '#E11D48', '#F8FAFC'],
  entertainment: ['#5B2C83', '#F5C518', '#111111'],
  boxing:     ['#A80000', '#1B1B1B', '#E8C547'],
  hockey:     ['#0B3552', '#E6EEF5', '#C9102F'],
  olympics:   ['#1F5BA0', '#F2C230', '#D62828'],
  other:      ['#4A4A4A', '#D4D4D4', '#7A7A7A'],
};

// Tier/brand labels used on sets
window.TIERS = ['Chrome', 'Prism', 'Refractor', 'Auto', 'Base', 'Heritage', 'Neon', 'Premier', 'Signature'];

// Fictional but plausible set names
window.SETS = [
  { id: 's01', name: '2026 Apex Midnight UFC',        sport: 'mma',           leagues: ['UFC'],           tiers: ['Chrome'],   athletes: 178, cards: 484,  year: 2026, featured: true },
  { id: 's02', name: '2025-26 Court Kings Hoops',     sport: 'basketball',    leagues: ['NBA'],           tiers: [],           athletes: 338, cards: 1011, year: 2025, featured: true },
  { id: 's03', name: '2025-26 Continental Club Cup',  sport: 'soccer',        leagues: ['UEFA'],          tiers: ['Chrome'],   athletes: 353, cards: 912,  year: 2025, featured: true },
  { id: 's04', name: '2025-26 Cosmic Chrome Hoops',   sport: 'basketball',    leagues: ['NBA'],           tiers: ['Chrome'],   athletes: 270, cards: 687,  year: 2025, featured: false },
  { id: 's05', name: '2026 Finest Premier League',    sport: 'soccer',        leagues: ['Premier League'],tiers: ['Chrome'],   athletes: 307, cards: 767,  year: 2026, featured: false },
  { id: 's06', name: '2025-26 Vanguard Hoops',        sport: 'basketball',    leagues: ['NBA'],           tiers: [],           athletes: 353, cards: 1503, year: 2025, featured: false },
  { id: 's07', name: '2025 Chrome Gridiron',          sport: 'football',      leagues: ['NFL'],           tiers: ['Chrome'],   athletes: 547, cards: 2366, year: 2025, featured: true },
  { id: 's08', name: '2026 Chrome Squared Circle',    sport: 'wrestling',     leagues: ['WWE'],           tiers: ['Chrome'],   athletes: 269, cards: 1137, year: 2026, featured: false },
  { id: 's09', name: '2026 Neon Parade',              sport: 'entertainment', leagues: ['Animation'],     tiers: ['Neon'],     athletes: 339, cards: 753,  year: 2026, featured: false },
  { id: 's10', name: '2025 Chrome Mercenaries',       sport: 'entertainment', leagues: ['Film'],          tiers: ['Chrome'],   athletes: 88,  cards: 212,  year: 2025, featured: false },
  { id: 's11', name: '2026 Heritage Diamond',         sport: 'baseball',      leagues: ['MLB'],           tiers: ['Heritage'], athletes: 421, cards: 890,  year: 2026, featured: false },
  { id: 's12', name: '2025 Park Anniversary',         sport: 'entertainment', leagues: ['Parks'],         tiers: [],           athletes: 62,  cards: 140,  year: 2025, featured: false },
  { id: 's13', name: '2026 Octagon Prism',            sport: 'mma',           leagues: ['UFC'],           tiers: ['Prism'],    athletes: 144, cards: 360,  year: 2026, featured: false },
  { id: 's14', name: '2026 Pitchers Premier',         sport: 'baseball',      leagues: ['MLB'],           tiers: ['Premier'],  athletes: 210, cards: 540,  year: 2026, featured: false },
  { id: 's15', name: '2025-26 Ice Kings',             sport: 'hockey',        leagues: ['NHL'],           tiers: [],           athletes: 298, cards: 796,  year: 2025, featured: false },
  { id: 's16', name: '2026 Chrome Refractor Ice',     sport: 'hockey',        leagues: ['NHL'],           tiers: ['Chrome','Refractor'], athletes: 201, cards: 512, year: 2026, featured: false },
  { id: 's17', name: '2024 Paris Podium',             sport: 'olympics',      leagues: ['IOC'],           tiers: [],           athletes: 612, cards: 1420, year: 2024, featured: false },
  { id: 's18', name: '2026 Chrome Canvas',            sport: 'racing',        leagues: ['F1'],            tiers: ['Chrome'],   athletes: 92,  cards: 268,  year: 2026, featured: false },
  { id: 's19', name: '2025 Finish Line',              sport: 'racing',        leagues: ['NASCAR'],        tiers: [],           athletes: 110, cards: 320,  year: 2025, featured: false },
  { id: 's20', name: '2026 Apex Lightweights',        sport: 'boxing',        leagues: ['WBC'],           tiers: ['Signature'],athletes: 64,  cards: 186,  year: 2026, featured: false },
  { id: 's21', name: '2025 Heritage Gloves',          sport: 'boxing',        leagues: ['WBA'],           tiers: ['Heritage'], athletes: 88,  cards: 244,  year: 2025, featured: false },
  { id: 's22', name: '2025-26 La Liga Select',        sport: 'soccer',        leagues: ['La Liga'],       tiers: [],           athletes: 244, cards: 612,  year: 2025, featured: false },
  { id: 's23', name: '2026 Serie A Auto',             sport: 'soccer',        leagues: ['Serie A'],       tiers: ['Auto'],     athletes: 180, cards: 480,  year: 2026, featured: false },
  { id: 's24', name: '2025 Chrome Quarterbacks',      sport: 'football',      leagues: ['NFL'],           tiers: ['Chrome'],   athletes: 64,  cards: 192,  year: 2025, featured: false },
  { id: 's25', name: '2026 Finest College Hoops',     sport: 'basketball',    leagues: ['NCAA'],          tiers: ['Chrome'],   athletes: 301, cards: 712,  year: 2026, featured: false },
  { id: 's26', name: '2025 Rookie Class Baseball',    sport: 'baseball',      leagues: ['MLB'],           tiers: [],           athletes: 120, cards: 280,  year: 2025, featured: false },
  { id: 's27', name: '2026 Wrestlemania Prism',       sport: 'wrestling',     leagues: ['WWE'],           tiers: ['Prism'],    athletes: 145, cards: 390,  year: 2026, featured: false },
  { id: 's28', name: '2025 Indie Mat Heroes',         sport: 'wrestling',     leagues: ['Indie'],         tiers: [],           athletes: 88,  cards: 220,  year: 2025, featured: false },
  { id: 's29', name: '2026 Studio Legends',           sport: 'entertainment', leagues: ['Film'],          tiers: ['Signature'],athletes: 140, cards: 360,  year: 2026, featured: false },
  { id: 's30', name: '2025 Podcast Royalty',          sport: 'other',         leagues: ['Podcasts'],      tiers: [],           athletes: 44,  cards: 120,  year: 2025, featured: false },
  { id: 's31', name: '2026 Winter Games Chrome',      sport: 'olympics',      leagues: ['IOC'],           tiers: ['Chrome'],   athletes: 412, cards: 980,  year: 2026, featured: false },
  { id: 's32', name: '2026 Arena Goaltenders',        sport: 'hockey',        leagues: ['NHL'],           tiers: ['Signature'],athletes: 64,  cards: 160,  year: 2026, featured: false },
];
