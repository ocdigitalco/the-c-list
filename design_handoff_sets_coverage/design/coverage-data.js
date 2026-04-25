// Sets Coverage data — admin view of set completeness
// Each set tracks 5 coverage signals: checklist, packOdds, boxConfig, parallels, releaseDate
// Field values: true = covered, false = missing (releaseDate stores ISO date string or null)

window.MANUFACTURERS = [
  { id: 'all', label: 'All' },
  { id: 'topps', label: 'Topps', color: '#E11D48' },
  { id: 'panini', label: 'Panini', color: '#F2C230' },
];

window.COVERAGE_SPORTS = [
  { id: 'all', label: 'All' },
  { id: 'basketball', label: 'Basketball' },
  { id: 'baseball', label: 'Baseball' },
  { id: 'soccer', label: 'Soccer' },
  { id: 'mma', label: 'MMA' },
  { id: 'wrestling', label: 'Wrestling' },
  { id: 'racing', label: 'Racing' },
  { id: 'football', label: 'Football' },
  { id: 'entertainment', label: 'Entertainment' },
  { id: 'other', label: 'Other' },
];

// Helper to seed deterministic-ish coverage flags
function mkSet(id, name, mfr, sport, year, dateStr, flags) {
  return {
    id, name, mfr, sport, year,
    releaseDate: dateStr || null,
    checklist: flags.checklist !== false,
    parallels: flags.parallels !== false,
    boxConfig: flags.boxConfig !== false,
    packOdds: flags.packOdds !== false,
  };
}

window.COVERAGE_SETS = [
  // 2026 BASKETBALL
  mkSet('s1','2025-26 Topps Hoops Basketball','panini','basketball',2026,'2026-05-14',{}),
  mkSet('s2','2025-26 Topps Cosmic Chrome Basketball','topps','basketball',2026,'2026-04-29',{}),
  mkSet('s3','2025-26 Bowman Basketball','topps','basketball',2026,'2026-04-22',{}),
  mkSet('s4',"2025 Topps Chrome McDonald's All-American Basketball",'topps','basketball',2026,'2026-03-12',{}),
  mkSet('s5','2025-26 Topps Three Basketball','topps','basketball',2026,'2026-03-05',{}),
  mkSet('s6','2025-26 Topps Finest Basketball','topps','basketball',2026,'2026-02-26',{}),
  mkSet('s7','2025-26 Topps Chrome Cactus Jack Basketball','topps','basketball',2026,'2026-02-13',{boxConfig:false, packOdds:false}),
  mkSet('s8','2025-26 Topps Chrome Sapphire Basketball','topps','basketball',2026,'2026-01-22',{}),
  mkSet('s9','2025-26 Topps Court Kings','panini','basketball',2026,'2026-04-08',{packOdds:false}),
  mkSet('s10','2025-26 Vanguard Hoops','panini','basketball',2026,null,{checklist:false, packOdds:false, boxConfig:false}),
  // 2026 BASEBALL
  mkSet('s11','2026 Bowman Baseball','topps','baseball',2026,'2026-05-13',{}),
  mkSet('s12','2026 Topps Heritage Baseball','topps','baseball',2026,'2026-03-18',{}),
  mkSet('s13','2026 Topps Chrome Baseball','topps','baseball',2026,'2026-04-09',{}),
  mkSet('s14','2026 Topps Series 1 Baseball','topps','baseball',2026,'2026-02-04',{}),
  mkSet('s15','2026 Topps Finest Baseball','topps','baseball',2026,null,{checklist:false, parallels:false, boxConfig:false, packOdds:false}),
  mkSet('s16','2026 Bowman Chrome Baseball','topps','baseball',2026,'2026-05-27',{packOdds:false}),
  mkSet('s17','2026 Diamond Kings','panini','baseball',2026,'2026-03-25',{}),
  // 2026 SOCCER
  mkSet('s18','2025-26 Topps Chrome UEFA','topps','soccer',2026,'2026-04-15',{}),
  mkSet('s19','2025-26 Topps Finest Premier League','topps','soccer',2026,'2026-04-01',{}),
  mkSet('s20','2025-26 Panini Prizm Premier League','panini','soccer',2026,'2026-03-18',{boxConfig:false}),
  mkSet('s21','2026 Topps Bundesliga','topps','soccer',2026,null,{checklist:false, parallels:false}),
  // 2026 RACING
  mkSet('s22','2026 Donruss Racing','panini','racing',2026,'2026-02-20',{}),
  mkSet('s23','2026 Chrome F1','topps','racing',2026,'2026-04-30',{packOdds:false}),
  // 2026 FOOTBALL
  mkSet('s24','2025 Panini Prizm Football','panini','football',2026,'2026-01-15',{}),
  mkSet('s25','2025 Topps Chrome Football','topps','football',2026,'2026-02-08',{}),
  mkSet('s26','2025 Donruss Football','panini','football',2026,'2026-01-29',{}),
  // 2026 MMA / WRESTLING / ENT
  mkSet('s27','2026 Topps Chrome UFC','topps','mma',2026,'2026-03-04',{}),
  mkSet('s28','2026 Panini Impeccable UFC','panini','mma',2026,null,{checklist:false, parallels:false, boxConfig:false}),
  mkSet('s29','2026 Topps Chrome WWE','topps','wrestling',2026,'2026-04-18',{}),
  mkSet('s30','2026 Panini Mosaic WWE','panini','wrestling',2026,'2026-05-06',{packOdds:false, boxConfig:false}),
  mkSet('s31','2026 Studio Legends','panini','entertainment',2026,'2026-03-11',{}),
  mkSet('s32','2026 Park Anniversary','panini','entertainment',2026,null,{checklist:false}),

  // 2025 (collapsed by default)
  mkSet('s33','2024-25 Topps Hoops Basketball','panini','basketball',2025,'2025-05-14',{}),
  mkSet('s34','2024-25 Bowman Basketball','topps','basketball',2025,'2025-04-22',{}),
  mkSet('s35','2025 Bowman Baseball','topps','baseball',2025,'2025-05-08',{}),
  mkSet('s36','2025 Topps Heritage Baseball','topps','baseball',2025,'2025-03-12',{}),
  mkSet('s37','2025 Topps Chrome UFC','topps','mma',2025,'2025-03-04',{}),
  mkSet('s38','2024-25 Topps Chrome UEFA','topps','soccer',2025,'2025-04-15',{}),
  mkSet('s39','2025 Donruss Football','panini','football',2025,'2025-01-29',{}),
  mkSet('s40','2025 Panini Prizm Premier League','panini','soccer',2025,'2025-03-18',{}),

  // 2024
  mkSet('s41','2023-24 Topps Hoops Basketball','panini','basketball',2024,'2024-05-14',{}),
  mkSet('s42','2024 Topps Chrome Baseball','topps','baseball',2024,'2024-04-09',{}),
  mkSet('s43','2024 Donruss Football','panini','football',2024,'2024-01-29',{}),
];

window.COVERAGE_FIELDS = [
  { key: 'checklist',   label: 'Checklist',   short: 'Checklist' },
  { key: 'releaseDate', label: 'Release Date', short: null },
  { key: 'parallels',   label: 'Parallels',   short: 'Parallels' },
  { key: 'boxConfig',   label: 'Box Config',  short: 'Box Config' },
  { key: 'packOdds',    label: 'Pack Odds',   short: 'Pack Odds' },
];
