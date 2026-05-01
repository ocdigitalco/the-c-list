// Team Detail page data — companion to athlete-detail-data.js
// Subject: New England Patriots in 2025 Topps Chrome Football

window.TEAM_DETAIL = {
  id: 'patriots-2025-topps-chrome-football',
  team: 'New England Patriots',
  teamShort: 'Patriots',
  league: 'NFL',
  sport: 'Football',
  city: 'Foxborough, MA',
  conference: 'AFC East',
  // Team brand colors — used for the hero crest tile
  primary: '#0B2244',
  secondary: '#C2102E',
  setName: '2025 Topps Chrome Football',
  setHref: '#',
  // Aggregate totals across all Patriots cards in this set
  athletes: 17,
  totalCards: 1842,
  numberedParallels: 18420,
  oneOfOnes: 24,
  rookies: 4,
  autographs: 38,
};

// Per-athlete breakdown — drives the main flat table.
// Columns: Total Cards, Autographs, Inserts, Numbered Parallels.
window.TEAM_ATHLETES = [
  { rank: 1,  name: 'Drake Maye',          position: 'QB', jersey: 10, rookie: false, totalCards: 196, autographs: 4, inserts: 9,  numberedParallels: 162 },
  { rank: 2,  name: 'Rhamondre Stevenson', position: 'RB', jersey: 38, rookie: false, totalCards: 142, autographs: 2, inserts: 6,  numberedParallels: 118 },
  { rank: 3,  name: 'DeMario Douglas',     position: 'WR', jersey: 81, rookie: false, totalCards: 128, autographs: 2, inserts: 5,  numberedParallels: 104 },
  { rank: 4,  name: 'Hunter Henry',        position: 'TE', jersey: 85, rookie: false, totalCards: 116, autographs: 2, inserts: 5,  numberedParallels:  94 },
  { rank: 5,  name: 'Christian Gonzalez',  position: 'CB', jersey: 0,  rookie: false, totalCards: 112, autographs: 2, inserts: 5,  numberedParallels:  92 },
  { rank: 6,  name: 'Kyle Bowers',         position: 'DE', jersey: 91, rookie: true,  totalCards: 168, autographs: 5, inserts: 7,  numberedParallels: 142 },
  { rank: 7,  name: 'Ja\u2019Lynn Polk',   position: 'WR', jersey: 86, rookie: true,  totalCards: 154, autographs: 4, inserts: 7,  numberedParallels: 128 },
  { rank: 8,  name: 'Marcus Jones',        position: 'CB', jersey: 25, rookie: false, totalCards:  98, autographs: 1, inserts: 4,  numberedParallels:  82 },
  { rank: 9,  name: 'Kyle Dugger',         position: 'S',  jersey: 23, rookie: false, totalCards:  96, autographs: 1, inserts: 4,  numberedParallels:  78 },
  { rank: 10, name: 'Jabrill Peppers',     position: 'S',  jersey: 5,  rookie: false, totalCards:  88, autographs: 1, inserts: 3,  numberedParallels:  72 },
  { rank: 11, name: 'Mike Onwenu',         position: 'OT', jersey: 71, rookie: false, totalCards:  82, autographs: 1, inserts: 3,  numberedParallels:  66 },
  { rank: 12, name: 'Caedan Wallace',      position: 'OT', jersey: 75, rookie: true,  totalCards: 124, autographs: 3, inserts: 6,  numberedParallels: 102 },
  { rank: 13, name: 'Antonio Gibson',      position: 'RB', jersey: 26, rookie: false, totalCards:  86, autographs: 1, inserts: 3,  numberedParallels:  70 },
  { rank: 14, name: 'Austin Hooper',       position: 'TE', jersey: 87, rookie: false, totalCards:  74, autographs: 1, inserts: 3,  numberedParallels:  60 },
  { rank: 15, name: 'Kayshon Boutte',      position: 'WR', jersey: 9,  rookie: false, totalCards:  78, autographs: 1, inserts: 3,  numberedParallels:  64 },
  { rank: 16, name: 'Anfernee Jennings',   position: 'LB', jersey: 58, rookie: false, totalCards:  62, autographs: 0, inserts: 2,  numberedParallels:  50 },
  { rank: 17, name: 'Jahlani Tavai',       position: 'LB', jersey: 48, rookie: false, totalCards:  38, autographs: 0, inserts: 1,  numberedParallels:  28 },
];

// All teams in the set — drives a "switch team" drawer/select.
window.TEAMS_IN_SET = [
  { name: 'New England Patriots',   short: 'Patriots',  athletes: 17, totalCards: 1842 },
  { name: 'Buffalo Bills',          short: 'Bills',     athletes: 18, totalCards: 1986 },
  { name: 'Kansas City Chiefs',     short: 'Chiefs',    athletes: 21, totalCards: 2410 },
  { name: 'San Francisco 49ers',    short: '49ers',     athletes: 20, totalCards: 2218 },
  { name: 'Dallas Cowboys',         short: 'Cowboys',   athletes: 19, totalCards: 2104 },
  { name: 'Philadelphia Eagles',    short: 'Eagles',    athletes: 19, totalCards: 2078 },
  { name: 'Detroit Lions',          short: 'Lions',     athletes: 18, totalCards: 1942 },
  { name: 'Baltimore Ravens',       short: 'Ravens',    athletes: 18, totalCards: 1958 },
  { name: 'Cincinnati Bengals',     short: 'Bengals',   athletes: 17, totalCards: 1810 },
  { name: 'Miami Dolphins',         short: 'Dolphins',  athletes: 17, totalCards: 1796 },
  { name: 'New York Jets',          short: 'Jets',      athletes: 17, totalCards: 1788 },
  { name: 'Houston Texans',         short: 'Texans',    athletes: 18, totalCards: 1872 },
];
