export type V2Theme = "light" | "dark";

export interface SidebarPlayer {
  id: number;
  name: string;
  slug: string | null;
  totalCards: number;
  hasRookie: boolean;
}

export interface SetStats {
  insertSets: number;
  athletes: number;
  cards: number;
  numberedParallels: number;
  oneOfOnes: number;
}

export interface LeaderboardRow {
  id: number;
  name: string;
  slug: string | null;
  team: string | null;
  isRookie: boolean;
  totalCards: number;
  autographs: number;
  inserts: number;
  numberedParallels: number;
  nbaPlayerId: number | null;
  ufcImageUrl: string | null;
  mlbPlayerId: number | null;
  imageUrl: string | null;
}

export interface InsertSetDetail {
  insertSetId: number;
  insertSetName: string;
  appearances: {
    cardNumber: string;
    team: string | null;
    isRookie: boolean;
    subsetTag: string | null;
    coPlayers: { id: number; name: string; slug: string | null }[];
  }[];
  parallels: { id: number; name: string; printRun: number | null }[];
}

export interface BoxConfigSingle {
  cards_per_pack?: number;
  packs_per_box?: number;
  boxes_per_case?: number | null;
  autos_per_box?: number;
  autos_or_memorabilia_per_box?: number;
  autos_or_relics_per_box?: number;
  autos_or_auto_relics_per_box?: number;
  nba_autos_per_box?: number;
  ncaa_autos_per_box?: number;
  memorabilia_per_box?: number;
  relics_per_box?: number;
  total_boxes_produced?: number;
  total_packs_produced?: number;
  notes?: string;
  note?: string;
  [key: string]: number | string | null | undefined;
}

export type BoxConfigMulti = Record<string, BoxConfigSingle>;

export interface BoxFormatSummary {
  label: string;
  packsPerBox: number;
  autosPerBox: number;
  notes?: string;
}
