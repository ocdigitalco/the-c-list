/**
 * Data layer for the canonical athlete master pages (Stage 2).
 *
 * Everything reads the Stage-1 identity layer: a canonical `athletes` row, with
 * every per-set `players` row pointing to it via `players.athlete_id`. We read
 * through rawQuery because `players.athlete_id` / `players.slug` are intentionally
 * outside the Drizzle model (see schema.ts). The whole page builds from a handful
 * of index-driven queries (never one-per-set): athlete row, one appearance join,
 * parallels for the touched insert_sets, cached sales. No cookies/searchParams are
 * read, so the pages stay statically cacheable (revalidate=false / 86400).
 */
import { rawQuery } from "@/lib/db";
import { extractYearAndManufacturer } from "@/lib/setSeo";
import { buildEbaySearchUrl, buildEbayItemUrl } from "@/lib/ebay/searchUrl";
import type { PageKind } from "./util";

export interface AthleteCore {
  id: number;
  slug: string;
  name: string;
  sport: string;
  subjectRole: string;
  pageKind: PageKind;
  aliases: string[];
  setCount: number;
  cardCount: number;
  firstYear: number | null;
  rookieYear: number | null;
  headshotUrl: string | null;
}

function parseAliases(raw: string | null): string[] {
  if (!raw) return [];
  try {
    const v = JSON.parse(raw);
    return Array.isArray(v) ? v.filter((x) => typeof x === "string") : [];
  } catch {
    return [];
  }
}

function coreFromRow(r: Record<string, unknown>): AthleteCore {
  return {
    id: r.id as number,
    slug: r.slug as string,
    name: r.name as string,
    sport: r.sport as string,
    subjectRole: r.subject_role as string,
    pageKind: r.page_kind as PageKind,
    aliases: parseAliases((r.aliases as string | null) ?? null),
    setCount: (r.set_count as number) ?? 0,
    cardCount: (r.card_count as number) ?? 0,
    firstYear: (r.first_year as number | null) ?? null,
    rookieYear: (r.rookie_year as number | null) ?? null,
    headshotUrl: (r.headshot_url as string | null) ?? null,
  };
}

/** Resolve a master-page subject by slug. Returns null for unknown slugs or
 * page_kind='none' (those get no page). */
export async function getAthleteBySlug(slug: string): Promise<AthleteCore | null> {
  const row = await rawQuery.get<Record<string, unknown>>(
    `SELECT id, slug, name, sport, subject_role, page_kind, aliases,
            set_count, card_count, first_year, rookie_year, headshot_url
     FROM athletes WHERE slug = ?`,
    slug
  );
  if (!row || row.page_kind === "none") return null;
  return coreFromRow(row);
}

// ── Detail page payload ──────────────────────────────────────────────────────

interface RawAppearance {
  pa_id: number;
  player_id: number;
  player_slug: string | null;
  card_number: string;
  subset_tag: string | null;
  team: string | null;
  is_rookie: number;
  insert_set_id: number;
  insert_set_name: string;
  is_autograph: number;
  is_base: number;
  insert_print_run: number | null;
  set_id: number;
  set_name: string;
  set_slug: string | null;
  set_league: string | null;
  set_season: string;
  release_date: string | null;
  sample_image_url: string | null;
}

export interface AthleteStats {
  sets: number;
  totalCards: number;
  autographs: number;
  numbered: number;
  ones: number;
  rookieCards: number;
}

export interface TeamBar {
  name: string;
  cards: number;
  pct: number;
}

export interface CardsBySetRow {
  setId: number;
  setSlug: string | null;
  setHref: string;
  setName: string;
  manufacturer: string;
  releaseDate: string | null;
  cards: number;
  autos: number;
  numbered: number;
  ones: number;
}

export interface GalleryTile {
  setId: number;
  setSlug: string | null;
  setHref: string;
  setName: string;
  image: string | null;
  chip: string;
  chipKind: "oneofone" | "numbered" | "auto" | "insert" | "base";
}

export interface AllCardRow {
  paId: number;
  playerId: number;
  setId: number;
  insertSetId: number;
  setName: string;
  setSlug: string | null;
  setHref: string;
  subset: string | null; // insert-set name, or null for the base set
  cardNumber: string;
  parallelCount: number;
  printRunLabel: string | null; // "/N", "1/1", or null
  lowestPrintRun: number | null;
  isAutograph: boolean;
  isNumbered: boolean;
  isRookie: boolean;
  isOneOfOne: boolean;
  releaseYear: number | null;
  ebayUrl: string | null;
}

export interface SaleRow {
  cardLabel: string;
  setName: string;
  grade: string; // e.g. "RAW"
  saleType: string; // "Auction" | "Buy It Now" | "Best Offer" | raw
  soldAt: string | null;
  priceCents: number | null;
  url: string | null;
  isAutograph: boolean;
  isNumbered: boolean;
  isGraded: boolean;
}

export interface RailSetRow {
  setId: number;
  setSlug: string | null;
  setHref: string;
  setName: string;
  sport: string;
  cardTypes: number; // distinct insert_sets the athlete appears in, for this set
  cards: number;
  autos: number;
  inserts: number;
  numbered: number;
  ones: number;
  releaseYear: number | null;
  isRookieYear: boolean;
}

export interface AthletePageData {
  athlete: AthleteCore;
  stats: AthleteStats;
  teams: TeamBar[];
  cardsBySet: CardsBySetRow[];
  gallery: GalleryTile[];
  cardsPerYear: { year: number; count: number }[];
  hardestToPull: { parallelName: string; setName: string; printRun: number }[];
  rightCard: {
    newestSet: { name: string; date: string | null } | null;
    rookie: { year: number; cards: number } | null;
    aliases: string[];
    upcomingCount: number;
  };
  allCards: AllCardRow[];
  rail: RailSetRow[];
  recentSales: SaleRow[];
  recentSalesPricedCount: number;
  ebayAllUrl: string | null;
  yearRange: { from: number; to: number } | null;
}

function releaseYear(dateOrSeason: string | null, season: string): number | null {
  if (dateOrSeason) {
    const m = dateOrSeason.match(/^(\d{4})/);
    if (m) return parseInt(m[1], 10);
  }
  const m2 = season.match(/(\d{4})/);
  return m2 ? parseInt(m2[1], 10) : null;
}

/** Deep link from the master page down to a set-scoped athlete page. */
function setAthleteHref(setSlug: string | null, setId: number, playerSlug: string | null, playerId: number): string {
  return `/sets/${setSlug ?? setId}/athlete/${playerSlug ?? playerId}`;
}

function saleTypeLabel(t: string | null): string {
  switch (t) {
    case "auction":
      return "Auction";
    case "bin":
      return "Buy It Now";
    case "best_offer":
      return "Best Offer";
    default:
      return t ? t : "—";
  }
}

/** Build the full master-page payload for a canonical athlete id. */
export async function getAthletePage(athlete: AthleteCore): Promise<AthletePageData> {
  const campaignId = process.env.EPN_CAMPAIGN_ID ?? null;
  const athleteId = athlete.id;

  // 1 — every appearance (card) of this athlete, across every set.
  const apps = await rawQuery.all<RawAppearance>(
    `SELECT pa.id AS pa_id, p.id AS player_id, p.slug AS player_slug, pa.card_number, pa.subset_tag, pa.team, pa.is_rookie,
            ins.id AS insert_set_id, ins.name AS insert_set_name, ins.is_autograph, ins.is_base,
            ins.print_run AS insert_print_run,
            s.id AS set_id, s.name AS set_name, s.slug AS set_slug, s.league AS set_league,
            s.season AS set_season, s.release_date, s.sample_image_url
     FROM players p
     JOIN player_appearances pa ON pa.player_id = p.id
     JOIN insert_sets ins ON ins.id = pa.insert_set_id
     JOIN sets s ON s.id = ins.set_id
     WHERE p.athlete_id = ?`,
    athleteId
  );

  // 2 — parallels for every insert_set the athlete touches (one query).
  const insertSetIds = Array.from(new Set(apps.map((a) => a.insert_set_id)));
  const parallelsByInsertSet = new Map<number, { name: string; printRun: number | null }[]>();
  if (insertSetIds.length) {
    const placeholders = insertSetIds.map(() => "?").join(",");
    const parRows = await rawQuery.all<{ insert_set_id: number; name: string; print_run: number | null }>(
      `SELECT insert_set_id, name, print_run FROM parallels WHERE insert_set_id IN (${placeholders})`,
      ...insertSetIds
    );
    for (const pr of parRows) {
      const list = parallelsByInsertSet.get(pr.insert_set_id) ?? [];
      list.push({ name: pr.name, printRun: pr.print_run });
      parallelsByInsertSet.set(pr.insert_set_id, list);
    }
  }

  // Per-insert-set derived facts used across the page.
  const insertSetNumbered = new Map<number, boolean>();
  const insertSetOnes = new Map<number, number>(); // # of 1/1 parallels on the insert_set
  for (const isid of insertSetIds) {
    const pars = parallelsByInsertSet.get(isid) ?? [];
    const ones = pars.filter((p) => p.printRun === 1).length;
    insertSetOnes.set(isid, ones);
    const hasNumberedParallel = pars.some((p) => p.printRun != null);
    insertSetNumbered.set(isid, hasNumberedParallel);
  }

  // ── Stats ────────────────────────────────────────────────────────────────
  const setIds = new Set<number>();
  let autographs = 0;
  let numbered = 0;
  let ones = 0;
  let rookieCards = 0;
  for (const a of apps) {
    setIds.add(a.set_id);
    if (a.is_autograph) autographs++;
    const numberedByInsert = a.insert_print_run != null || insertSetNumbered.get(a.insert_set_id) === true;
    if (numberedByInsert) numbered++;
    if (a.is_rookie) rookieCards++;
    // 1/1 versions touching this card: 1/1 parallels on its insert_set, plus the
    // card itself when the insert_set base is a 1/1.
    ones += (insertSetOnes.get(a.insert_set_id) ?? 0) + (a.insert_print_run === 1 ? 1 : 0);
  }
  const stats: AthleteStats = {
    sets: setIds.size,
    totalCards: apps.length,
    autographs,
    numbered,
    ones,
    rookieCards,
  };

  // ── Teams (most cards first; first = current team) ─────────────────────────
  const teamCounts = new Map<string, number>();
  for (const a of apps) {
    const t = (a.team ?? "").trim();
    if (!t) continue;
    teamCounts.set(t, (teamCounts.get(t) ?? 0) + 1);
  }
  const maxTeam = Math.max(1, ...Array.from(teamCounts.values()));
  const teams: TeamBar[] = Array.from(teamCounts.entries())
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .map(([name, cards]) => ({ name, cards, pct: Math.round((cards / maxTeam) * 100) }));

  // ── Per-set aggregation (Cards by set + rail + gallery) ────────────────────
  interface SetAgg {
    setId: number;
    setSlug: string | null;
    setName: string;
    league: string | null;
    sport: string;
    playerId: number;
    playerSlug: string | null;
    releaseDate: string | null;
    season: string;
    image: string | null;
    cards: number;
    autos: number;
    numbered: number;
    ones: number;
    inserts: number;
    insertSetIds: Set<number>;
    year: number | null;
    // gallery chip resolution
    bestOne: boolean;
    lowestPrintRun: number | null;
    hasAuto: boolean;
    hasInsert: boolean;
  }
  const setAggs = new Map<number, SetAgg>();
  // athlete.sport is the canonical sport; per-set we keep the set's own if present.
  for (const a of apps) {
    let agg = setAggs.get(a.set_id);
    if (!agg) {
      agg = {
        setId: a.set_id,
        setSlug: a.set_slug,
        setName: a.set_name,
        league: a.set_league,
        sport: athlete.sport,
        playerId: a.player_id,
        playerSlug: a.player_slug,
        releaseDate: a.release_date,
        season: a.set_season,
        image: a.sample_image_url,
        cards: 0,
        autos: 0,
        numbered: 0,
        ones: 0,
        inserts: 0,
        insertSetIds: new Set(),
        year: releaseYear(a.release_date, a.set_season),
        bestOne: false,
        lowestPrintRun: null,
        hasAuto: false,
        hasInsert: false,
      };
      setAggs.set(a.set_id, agg);
    }
    agg.cards++;
    agg.insertSetIds.add(a.insert_set_id);
    if (a.is_autograph) {
      agg.autos++;
      agg.hasAuto = true;
    }
    if (!a.is_base) agg.hasInsert = true;
    const numberedByInsert = a.insert_print_run != null || insertSetNumbered.get(a.insert_set_id) === true;
    if (numberedByInsert) agg.numbered++;
    const cardOnes = (insertSetOnes.get(a.insert_set_id) ?? 0) + (a.insert_print_run === 1 ? 1 : 0);
    agg.ones += cardOnes;
    if (cardOnes > 0) agg.bestOne = true;
    // lowest print run touching this card (insert base run or any numbered parallel)
    const runs: number[] = [];
    if (a.insert_print_run != null) runs.push(a.insert_print_run);
    for (const p of parallelsByInsertSet.get(a.insert_set_id) ?? []) {
      if (p.printRun != null) runs.push(p.printRun);
    }
    if (runs.length) {
      const lo = Math.min(...runs);
      agg.lowestPrintRun = agg.lowestPrintRun == null ? lo : Math.min(agg.lowestPrintRun, lo);
    }
  }
  for (const agg of setAggs.values()) {
    agg.inserts = Array.from(agg.insertSetIds).length;
  }

  const aggList = Array.from(setAggs.values());

  const cardsBySet: CardsBySetRow[] = [...aggList]
    .sort((a, b) => b.cards - a.cards || (a.setName < b.setName ? -1 : 1))
    .map((agg) => ({
      setId: agg.setId,
      setSlug: agg.setSlug,
      setHref: setAthleteHref(agg.setSlug, agg.setId, agg.playerSlug, agg.playerId),
      setName: agg.setName,
      manufacturer: extractYearAndManufacturer(agg.setName).manufacturer,
      releaseDate: agg.releaseDate,
      cards: agg.cards,
      autos: agg.autos,
      numbered: agg.numbered,
      ones: agg.ones,
    }));

  // Gallery — newest first; chip = most notable card type in that set.
  const gallery: GalleryTile[] = [...aggList]
    .sort((a, b) => (b.releaseDate ?? "").localeCompare(a.releaseDate ?? "") || b.cards - a.cards)
    .map((agg) => {
      let chip = "Base";
      let chipKind: GalleryTile["chipKind"] = "base";
      if (agg.bestOne) {
        chip = "1/1";
        chipKind = "oneofone";
      } else if (agg.lowestPrintRun != null) {
        chip = `/${agg.lowestPrintRun}`;
        chipKind = "numbered";
      } else if (agg.hasAuto) {
        chip = "Auto";
        chipKind = "auto";
      } else if (agg.hasInsert) {
        chip = "Insert";
        chipKind = "insert";
      }
      return {
        setId: agg.setId,
        setSlug: agg.setSlug,
        setHref: setAthleteHref(agg.setSlug, agg.setId, agg.playerSlug, agg.playerId),
        setName: agg.setName,
        image: agg.image,
        chip,
        chipKind,
      };
    });

  // Cards per year (by set release year).
  const yearCounts = new Map<number, number>();
  for (const a of apps) {
    const y = releaseYear(a.release_date, a.set_season);
    if (y == null) continue;
    yearCounts.set(y, (yearCounts.get(y) ?? 0) + 1);
  }
  const cardsPerYear = Array.from(yearCounts.entries())
    .sort((a, b) => a[0] - b[0])
    .map(([year, count]) => ({ year, count }));
  const yearRange = cardsPerYear.length
    ? { from: cardsPerYear[0].year, to: cardsPerYear[cardsPerYear.length - 1].year }
    : null;

  // Hardest to pull — three lowest print runs across their cards.
  interface HardRow {
    parallelName: string;
    setName: string;
    printRun: number;
  }
  const hard: HardRow[] = [];
  const seenHard = new Set<string>();
  for (const a of apps) {
    const setName = a.set_name;
    if (a.insert_print_run != null) {
      const key = `${a.insert_set_id}|base|${a.insert_print_run}`;
      if (!seenHard.has(key)) {
        seenHard.add(key);
        hard.push({ parallelName: a.insert_set_name, setName, printRun: a.insert_print_run });
      }
    }
    for (const p of parallelsByInsertSet.get(a.insert_set_id) ?? []) {
      if (p.printRun == null) continue;
      const key = `${a.insert_set_id}|${p.name}|${p.printRun}`;
      if (seenHard.has(key)) continue;
      seenHard.add(key);
      hard.push({ parallelName: `${a.insert_set_name !== "Base Set" ? a.insert_set_name + " " : ""}${p.name}`.trim(), setName, printRun: p.printRun });
    }
  }
  const hardestToPull = hard.sort((a, b) => a.printRun - b.printRun).slice(0, 3);

  // ── Right card ─────────────────────────────────────────────────────────────
  const todayIso = new Date().toISOString().slice(0, 10);
  let newestSet: { name: string; date: string | null } | null = null;
  let upcomingCount = 0;
  for (const agg of aggList) {
    if (agg.releaseDate) {
      if (!newestSet || agg.releaseDate > (newestSet.date ?? "")) {
        newestSet = { name: agg.setName, date: agg.releaseDate };
      }
      if (agg.releaseDate > todayIso) upcomingCount++;
    }
  }
  const rookieCardsThatYear = athlete.rookieYear
    ? apps.filter((a) => releaseYear(a.release_date, a.set_season) === athlete.rookieYear).length
    : 0;
  const aliasesExtra = athlete.aliases.filter((a) => a !== athlete.name);

  // ── All cards (per-appearance rows for the tabs) ───────────────────────────
  const allCards: AllCardRow[] = apps
    .map((a) => {
      const pars = parallelsByInsertSet.get(a.insert_set_id) ?? [];
      const numberedByInsert = a.insert_print_run != null || insertSetNumbered.get(a.insert_set_id) === true;
      const runs = pars.map((p) => p.printRun).filter((r): r is number => r != null);
      if (a.insert_print_run != null) runs.push(a.insert_print_run);
      const lowestPrintRun = runs.length ? Math.min(...runs) : null;
      const isOne = (insertSetOnes.get(a.insert_set_id) ?? 0) > 0 || a.insert_print_run === 1;
      const subset = a.is_base ? null : a.insert_set_name;
      const ebayUrl = buildEbaySearchUrl(
        {
          setName: a.set_name,
          player: athlete.name,
          subset,
          parallel: "Base",
          printRun: null,
          athleteId,
          setId: a.set_id,
          insertSetId: a.insert_set_id,
          parallelId: null,
        },
        campaignId
      );
      return {
        paId: a.pa_id,
        playerId: a.player_id,
        setId: a.set_id,
        insertSetId: a.insert_set_id,
        setName: a.set_name,
        setSlug: a.set_slug,
        setHref: setAthleteHref(a.set_slug, a.set_id, a.player_slug, a.player_id),
        subset,
        cardNumber: a.card_number,
        parallelCount: pars.length,
        printRunLabel: lowestPrintRun == null ? null : lowestPrintRun === 1 ? "1/1" : `/${lowestPrintRun}`,
        lowestPrintRun,
        isAutograph: !!a.is_autograph,
        isNumbered: numberedByInsert,
        isRookie: !!a.is_rookie,
        isOneOfOne: isOne,
        releaseYear: releaseYear(a.release_date, a.set_season),
        ebayUrl,
      };
    })
    .sort(
      (a, b) =>
        (b.releaseYear ?? 0) - (a.releaseYear ?? 0) ||
        a.setName.localeCompare(b.setName) ||
        a.cardNumber.localeCompare(b.cardNumber, undefined, { numeric: true })
    );

  // ── Rail set list ──────────────────────────────────────────────────────────
  const rail: RailSetRow[] = [...aggList]
    .sort((a, b) => b.cards - a.cards || (a.setName < b.setName ? -1 : 1))
    .map((agg) => ({
      setId: agg.setId,
      setSlug: agg.setSlug,
      setHref: setAthleteHref(agg.setSlug, agg.setId, agg.playerSlug, agg.playerId),
      setName: agg.setName,
      sport: agg.sport,
      cardTypes: agg.inserts,
      cards: agg.cards,
      autos: agg.autos,
      inserts: agg.inserts,
      numbered: agg.numbered,
      ones: agg.ones,
      releaseYear: agg.year,
      isRookieYear: athlete.rookieYear != null && agg.year === athlete.rookieYear,
    }));

  // ── Recent sales (cached only; sold_comps may be empty in dev) ─────────────
  let recentSales: SaleRow[] = [];
  let recentSalesPricedCount = 0;
  try {
    const playerIds = Array.from(new Set(apps.map((a) => a.player_id)));
    if (playerIds.length) {
      const ph = playerIds.map(() => "?").join(",");
      const saleRows = await rawQuery.all<{
        insert_set_name: string;
        is_base: number;
        is_autograph: number;
        card_number: string;
        set_name: string;
        insert_print_run: number | null;
        grade_filter: string;
        last_sold_type: string | null;
        last_sold_at: string | null;
        last_sold_price_cents: number | null;
        last_sold_url: string | null;
      }>(
        `SELECT ins.name AS insert_set_name, ins.is_base, ins.is_autograph, ins.print_run AS insert_print_run,
                sc.card_number, s.name AS set_name, sc.grade_filter, sc.last_sold_type,
                sc.last_sold_at, sc.last_sold_price_cents, sc.last_sold_url
         FROM sold_comps sc
         JOIN insert_sets ins ON ins.id = sc.insert_set_id
         JOIN sets s ON s.id = sc.set_id
         WHERE sc.player_id IN (${ph}) AND sc.last_sold_price_cents IS NOT NULL
         ORDER BY sc.last_sold_at DESC
         LIMIT 50`,
        ...playerIds
      );
      recentSalesPricedCount = saleRows.length;
      recentSales = saleRows.map((r) => {
        const subset = r.is_base ? `Base #${r.card_number}` : `${r.insert_set_name} #${r.card_number}`;
        const grade = (r.grade_filter || "raw").toUpperCase();
        return {
          cardLabel: subset,
          setName: r.set_name,
          grade,
          saleType: saleTypeLabel(r.last_sold_type),
          soldAt: r.last_sold_at,
          priceCents: r.last_sold_price_cents,
          url: buildEbayItemUrl(r.last_sold_url, campaignId, `athlete:${athlete.slug}|src:sold`),
          isAutograph: !!r.is_autograph,
          isNumbered: r.insert_print_run != null,
          isGraded: grade !== "RAW",
        };
      });
    }
  } catch {
    // sold_comps absent (dev) → no cached sales.
  }

  return {
    athlete,
    stats,
    teams,
    cardsBySet,
    gallery,
    cardsPerYear,
    hardestToPull,
    rightCard: {
      newestSet,
      rookie: athlete.rookieYear ? { year: athlete.rookieYear, cards: rookieCardsThatYear } : null,
      aliases: aliasesExtra,
      upcomingCount,
    },
    allCards,
    rail,
    recentSales,
    recentSalesPricedCount,
    ebayAllUrl: null, // set by the page (needs slug + sport); kept here for shape parity
    yearRange,
  };
}

// ── Index ────────────────────────────────────────────────────────────────────

export interface AthleteTile {
  slug: string;
  name: string;
  sport: string;
  pageKind: PageKind;
  league: string | null;
  setCount: number;
  cardCount: number;
  rookieYear: number | null;
  trending: boolean;
  headshotUrl: string | null;
}

export type AthleteSort = "cards" | "az" | "newest" | "trending";

export interface AthleteIndexParams {
  sport?: string | null;
  q?: string | null;
  rookie?: boolean;
  sort?: AthleteSort;
  page?: number;
}

export interface AthleteIndexResult {
  tiles: AthleteTile[];
  total: number;
  page: number;
  pageSize: number;
  hasMore: boolean;
}

export const INDEX_PAGE_SIZE = 60;

/** The sport chips the index offers, ordered by athlete count (All first). */
export async function getIndexSports(): Promise<{ sport: string; count: number }[]> {
  const rows = await rawQuery.all<{ sport: string; count: number }>(
    `SELECT sport, COUNT(*) AS count FROM athletes WHERE page_kind != 'none'
     GROUP BY sport ORDER BY count DESC`
  );
  return rows;
}

/**
 * Paginated, filterable index query. Trending uses a one-pass player_events CTE
 * (views in the last 30 days) rather than a per-row correlated subquery. All
 * reads are index-driven and the result is cached by the caller (static page or
 * /api/athletes with s-maxage), so none of this makes a page dynamic.
 */
export async function getAthleteIndex(params: AthleteIndexParams): Promise<AthleteIndexResult> {
  const sort: AthleteSort = params.sort ?? "cards";
  const page = Math.max(0, params.page ?? 0);
  const pageSize = INDEX_PAGE_SIZE;
  const now = new Date();
  const rookieCutoff = now.getUTCFullYear() - 2;
  const trendCutoff = now.getTime() - 30 * 24 * 60 * 60 * 1000;

  const where: string[] = ["a.page_kind != 'none'"];
  const args: (string | number)[] = [];

  if (params.sport && params.sport !== "All") {
    where.push("a.sport = ?");
    args.push(params.sport);
  }
  if (params.rookie) {
    where.push("a.rookie_year IS NOT NULL AND a.rookie_year >= ?");
    args.push(rookieCutoff);
  }
  const q = (params.q ?? "").trim();
  if (q) {
    const like = `%${q}%`;
    where.push(
      `(a.name LIKE ?
        OR EXISTS (SELECT 1 FROM players p JOIN player_appearances pa ON pa.player_id = p.id
                   WHERE p.athlete_id = a.id AND pa.team LIKE ?)
        OR EXISTS (SELECT 1 FROM players p JOIN sets s ON s.id = p.set_id
                   WHERE p.athlete_id = a.id AND s.league LIKE ?))`
    );
    args.push(like, like, like);
  }
  const whereSql = where.join(" AND ");

  // Trending CTE only when needed.
  let trendJoin = "";
  let orderSql = "a.card_count DESC, a.name ASC";
  if (sort === "az") orderSql = "a.name ASC";
  else if (sort === "newest") orderSql = "COALESCE(a.first_year, 0) DESC, a.card_count DESC";
  else if (sort === "trending") {
    // trend count is computed and ordered; athletes with no recent views sink.
    trendJoin = `LEFT JOIN (
        SELECT p.athlete_id AS aid, COUNT(*) AS v
        FROM player_events e JOIN players p ON p.id = e.player_id
        WHERE e.event_type = 'view' AND e.created_at > ? AND p.athlete_id IS NOT NULL
        GROUP BY p.athlete_id
      ) t ON t.aid = a.id`;
    orderSql = "COALESCE(t.v, 0) DESC, a.card_count DESC";
  }

  // The league chip: most common set league across the athlete's appearances.
  const leagueExpr = `(SELECT s2.league FROM players p2 JOIN sets s2 ON s2.id = p2.set_id
                       WHERE p2.athlete_id = a.id AND s2.league IS NOT NULL
                       GROUP BY s2.league ORDER BY COUNT(*) DESC LIMIT 1)`;

  const selectArgs: (string | number)[] = [];
  if (sort === "trending") selectArgs.push(trendCutoff);

  const countRow = await rawQuery.get<{ n: number }>(
    `SELECT COUNT(*) AS n FROM athletes a WHERE ${whereSql}`,
    ...args
  );
  const total = countRow?.n ?? 0;

  const rows = await rawQuery.all<Record<string, unknown>>(
    `SELECT a.slug, a.name, a.sport, a.page_kind, a.set_count, a.card_count, a.rookie_year, a.headshot_url,
            ${leagueExpr} AS league${sort === "trending" ? ", COALESCE(t.v,0) AS trend" : ""}
     FROM athletes a
     ${trendJoin}
     WHERE ${whereSql}
     ORDER BY ${orderSql}
     LIMIT ? OFFSET ?`,
    ...selectArgs,
    ...args,
    pageSize,
    page * pageSize
  );

  const tiles: AthleteTile[] = rows.map((r) => ({
    slug: r.slug as string,
    name: r.name as string,
    sport: r.sport as string,
    pageKind: r.page_kind as PageKind,
    league: (r.league as string | null) ?? null,
    setCount: (r.set_count as number) ?? 0,
    cardCount: (r.card_count as number) ?? 0,
    rookieYear: (r.rookie_year as number | null) ?? null,
    trending: sort === "trending" ? ((r.trend as number) ?? 0) > 0 : false,
    headshotUrl: (r.headshot_url as string | null) ?? null,
  }));

  return {
    tiles,
    total,
    page,
    pageSize,
    hasMore: (page + 1) * pageSize < total,
  };
}
