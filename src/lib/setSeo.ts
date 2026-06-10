/**
 * SEO / AEO content builders for set pages.
 *
 * Produces the meta title/description, the data-computed summary paragraph,
 * and the Q&A (FAQ) entries rendered in the Overview tab. The same computed
 * object feeds both the visible Q&A and the FAQPage JSON-LD so they always
 * match 1:1.
 *
 * All computation happens server-side at ISR generation time.
 */

import { rawQuery } from "./db";
import {
  buildOddsPool,
  getOddsForBoxType,
  getBulkAthleteAnyCardOdds,
  type BoxFormatConfig,
} from "./athleteOdds";
import { denomToDisplay } from "./parseOdds";

export const SITE_URL = "https://www.checklist2.com";

// ─── Meta title & description ────────────────────────────────────────────────

export function buildSetMeta(
  setName: string,
  totalCards: number,
  hasPackOdds: boolean
): { title: string; description: string } {
  // 3-tier title fallback to stay under ~65 chars
  const full = `${setName} Checklist, Pack Odds & Break Calculator | Checklist²`;
  const mid = `${setName} Checklist & Pack Odds | Checklist²`;
  const short = `${setName} Checklist | Checklist²`;
  const title = full.length <= 65 ? full : mid.length <= 65 ? mid : short;

  const cards = totalCards.toLocaleString("en-US");
  const description = hasPackOdds
    ? `Complete ${setName} checklist with ${cards} cards, pack odds, numbered parallels, and box configurations. Free break hit calculator for collectors and breakers.`
    : `Complete ${setName} checklist with ${cards} cards, numbered parallels, and box configuration data for collectors.`;

  return { title, description };
}

// ─── Helpers ─────────────────────────────────────────────────────────────────

function joinList(items: string[]): string {
  if (items.length <= 1) return items[0] ?? "";
  if (items.length === 2) return `${items[0]} and ${items[1]}`;
  return `${items.slice(0, -1).join(", ")}, and ${items[items.length - 1]}`;
}

function num(n: number): string {
  return n.toLocaleString("en-US");
}

function cardsWord(n: number): string {
  return `${num(n)} card${n !== 1 ? "s" : ""}`;
}

const BOX_LABELS: Record<string, string> = {
  hobby: "Hobby", jumbo: "Jumbo", mega: "Mega", blaster: "Blaster",
  value: "Value", fat_pack: "Fat Pack", hanger: "Hanger",
  breakers_delight: "Breaker's Delight", first_day_issue: "First Day Issue",
  breaker: "Breaker", hobby_hybrid: "Hobby Hybrid", sapphire: "Sapphire",
  hongbao: "Hongbao", logofractor: "Logofractor", ffnyc: "FFNYC", fdi: "First Day Issue",
};

function fmtBoxLabel(key: string): string {
  return BOX_LABELS[key] ?? key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function normKey(k: string): string {
  return k.toLowerCase().replace(/[\s_]/g, "");
}

function formatDate(dateStr: string): string {
  return new Date(dateStr + "T00:00:00Z").toLocaleDateString("en-US", {
    month: "long", day: "numeric", year: "numeric", timeZone: "UTC",
  });
}

function extractYearAndManufacturer(setName: string): { year: string; manufacturer: string } {
  const yearMatch = setName.match(/^\d{4}(?:-\d{2})?/);
  const year = yearMatch ? yearMatch[0] : "";
  const manMatch = setName.match(/\b(Topps|Bowman|Panini|Upper Deck|Leaf|Donruss)\b/i);
  const manufacturer = manMatch ? manMatch[0] : "Topps";
  return { year, manufacturer };
}

interface SubjectNouns {
  singular: string;
  plural: string;
  /** Label for the "team" questions; null = skip team questions for this role */
  teamLabel: string | null;
}

function subjectNouns(role: string | null): SubjectNouns {
  switch (role) {
    case "character":
      return { singular: "character", plural: "characters", teamLabel: "show or film" };
    case "celebrity":
      return { singular: "celebrity", plural: "celebrities", teamLabel: null };
    case "sketch_artist":
      return { singular: "sketch artist", plural: "sketch artists", teamLabel: null };
    case "coach":
      return { singular: "coach", plural: "coaches", teamLabel: "team" };
    default:
      return { singular: "athlete", plural: "athletes", teamLabel: "team" };
  }
}

function pct(probability: number): string {
  const p = Math.round(probability * 1000) / 10;
  if (p > 99.9) return ">99.9%";
  return `${p.toFixed(1)}%`;
}

// ─── Box config parsing ──────────────────────────────────────────────────────

interface BoxFormat {
  key: string;
  label: string;
  cardsPerPack: number | null;
  packsPerBox: number | null;
  boxesPerCase: number | null;
  autosPerBox: number | null;
  tba: boolean;
}

/* eslint-disable @typescript-eslint/no-explicit-any */
function parseBoxFormats(boxConfigJson: string | null): BoxFormat[] {
  if (!boxConfigJson) return [];
  let raw: any;
  try {
    raw = JSON.parse(boxConfigJson);
  } catch {
    return [];
  }
  const firstVal = Object.values(raw)[0];
  const isMulti = firstVal !== null && typeof firstVal === "object";
  const entries: [string, any][] = isMulti ? Object.entries(raw) : [["hobby", raw]];

  return entries.map(([key, fmt]) => {
    const packsPerBox = fmt?.packs_per_box ?? null;
    const cardsPerPack = fmt?.cards_per_pack ?? null;
    const autosPerBox =
      fmt?.autos_per_box ??
      fmt?.autos_or_memorabilia_per_box ??
      fmt?.autos_or_relics_per_box ??
      fmt?.autos_or_auto_relics_per_box ??
      null;
    return {
      key,
      label: fmtBoxLabel(key),
      cardsPerPack,
      packsPerBox,
      boxesPerCase: fmt?.boxes_per_case ?? null,
      autosPerBox,
      tba: packsPerBox == null && cardsPerPack == null,
    };
  });
}
/* eslint-enable @typescript-eslint/no-explicit-any */

// ─── Main AEO computation ────────────────────────────────────────────────────

export interface SetFaq {
  q: string;
  a: string;
}

export interface SetAeoInput {
  setId: number;
  setName: string;
  sport: string;
  releaseDate: string | null;
  packOdds: string | null;
  boxConfig: string | null;
  totalCards: number;
  autographCount: number;
  parallelTypes: number;
  numberedParallels: number;
  allParallels: { name: string; printRun: number | null }[];
  subjectRole: string | null;
  leaderboard: {
    id: number;
    name: string;
    totalCards: number;
    isRookie: boolean;
    team: string | null;
  }[];
}

export interface SetAeoResult {
  summary: string;
  faqs: SetFaq[];
}

export async function computeSetAeo(input: SetAeoInput): Promise<SetAeoResult> {
  const {
    setId, setName, sport, releaseDate, packOdds, boxConfig,
    totalCards, autographCount, parallelTypes, allParallels, subjectRole, leaderboard,
  } = input;

  const nouns = subjectNouns(subjectRole);
  const faqs: SetFaq[] = [];

  // ── Additional queries ──────────────────────────────────────────────────
  const subsetRows = await rawQuery.all<{
    id: number; name: string; isAuto: number; cards: number;
  }>(
    `SELECT i.id, i.name, i.is_autograph AS isAuto, COUNT(pa.id) AS cards
     FROM insert_sets i
     LEFT JOIN player_appearances pa ON pa.insert_set_id = i.id
     WHERE i.set_id = ?
     GROUP BY i.id
     ORDER BY cards DESC, i.name`,
    setId
  );

  const subsetCount = subsetRows.length;
  const BASE_NAMES = new Set(["Base Set", "Base", "Base Cards"]);
  const baseCount = subsetRows
    .filter((r) => BASE_NAMES.has(r.name))
    .reduce((s, r) => s + r.cards, 0);
  const autoSubsets = subsetRows.filter((r) => r.isAuto === 1 && r.cards > 0);
  const autoKeyword = /auto|autograph|signature|signed|ink|script/i;
  const baseRe = /^base\b/i;
  const insertSubsets = subsetRows.filter(
    (r) => !baseRe.test(r.name) && r.isAuto !== 1 && !autoKeyword.test(r.name) && r.cards > 0
  );

  const baseLadder = await rawQuery.all<{ name: string; printRun: number | null }>(
    `SELECT p.name, p.print_run AS printRun
     FROM parallels p
     JOIN insert_sets i ON i.id = p.insert_set_id
     WHERE i.set_id = ? AND i.name IN ('Base Set', 'Base', 'Base Cards')
     ORDER BY p.id`,
    setId
  );

  const autoLeaders =
    autographCount > 0
      ? await rawQuery.all<{ name: string; c: number }>(
          `SELECT pl.name, COUNT(*) AS c
           FROM player_appearances pa
           JOIN players pl ON pl.id = pa.player_id
           JOIN insert_sets i ON i.id = pa.insert_set_id
           WHERE i.set_id = ? AND i.is_autograph = 1
           GROUP BY pl.id
           ORDER BY c DESC, pl.name
           LIMIT 5`,
          setId
        )
      : [];

  const teamAutoLeaders =
    autographCount > 0 && nouns.teamLabel
      ? await rawQuery.all<{ team: string; c: number }>(
          `SELECT pa.team AS team, COUNT(*) AS c
           FROM player_appearances pa
           JOIN insert_sets i ON i.id = pa.insert_set_id
           WHERE i.set_id = ? AND i.is_autograph = 1
             AND pa.team IS NOT NULL AND pa.team != ''
           GROUP BY pa.team
           ORDER BY c DESC
           LIMIT 5`,
          setId
        )
      : [];

  // ── Odds setup (shared by break-hit + hardest-pull questions) ───────────
  let oddsData: Record<string, number> | null = null;
  let oddsLabel = "Hobby";
  let breakBoxConfig: BoxFormatConfig | null = null;

  if (packOdds) {
    let oddsKeys: string[] | null = null;
    try {
      const raw = JSON.parse(packOdds);
      const firstVal = Object.values(raw)[0];
      if (firstVal !== null && typeof firstVal === "object") oddsKeys = Object.keys(raw);
    } catch { /* unparseable */ }

    const preferredKey = oddsKeys
      ? oddsKeys.find((k) => normKey(k) === "hobby") ??
        oddsKeys.find((k) => normKey(k).startsWith("hobby")) ??
        oddsKeys[0]
      : "hobby";
    oddsData = getOddsForBoxType(packOdds, preferredKey);
    oddsLabel = fmtBoxLabel(preferredKey);

    // Resolve a usable box config for the same (or closest) format
    const formats = parseBoxFormats(boxConfig);
    const matched =
      formats.find((f) => normKey(f.key) === normKey(preferredKey)) ??
      formats.find((f) => normKey(f.key) === "hobby") ??
      formats[0];
    if (matched && !matched.tba && matched.packsPerBox != null) {
      breakBoxConfig = {
        label: matched.label,
        packsPerBox: matched.packsPerBox,
        boxesPerCase: matched.boxesPerCase ?? 8,
        guaranteedAutos: matched.autosPerBox ?? 0,
      };
      oddsLabel = matched.label;
    }
  }

  const pool = oddsData ? await buildOddsPool(setId, oddsData) : [];

  // ── Q1: total cards ──────────────────────────────────────────────────────
  if (totalCards > 0) {
    let a = `${setName} has ${num(totalCards)} cards across ${num(subsetCount)} subsets`;
    if (baseCount > 0) a += `, including ${num(baseCount)} base cards`;
    a += ".";
    faqs.push({ q: `How many cards are in ${setName}?`, a });
  }

  // ── Q2: autograph cards ──────────────────────────────────────────────────
  if (autographCount > 0 && autoSubsets.length > 0) {
    const shown = autoSubsets.slice(0, 8);
    const more = autoSubsets.length - shown.length;
    let a = `${setName} includes ${num(autographCount)} autograph cards across ${num(autoSubsets.length)} autograph subset${autoSubsets.length !== 1 ? "s" : ""}. The largest ${shown.length === 1 ? "is" : "are"} ${joinList(shown.map((s) => `${s.name} (${cardsWord(s.cards)})`))}`;
    if (more > 0) a += `, and ${num(more)} more`;
    a += ".";
    faqs.push({ q: `How many autograph cards are in ${setName}?`, a });
  }

  // ── Q3: top subject by cards ─────────────────────────────────────────────
  const cardLeaders = leaderboard.filter((e) => e.totalCards > 0).slice(0, 5);
  if (cardLeaders.length > 0) {
    const [top, ...rest] = cardLeaders;
    let a = `${top.name} leads ${setName} with ${num(top.totalCards)} cards, including parallels.`;
    if (rest.length > 0) {
      a += ` The next closest ${rest.length === 1 ? "is" : "are"} ${joinList(rest.map((r) => `${r.name} (${num(r.totalCards)})`))}.`;
    }
    faqs.push({ q: `Which ${nouns.singular} has the most cards in ${setName}?`, a });
  }

  // ── Q4: top subject by autograph cards ───────────────────────────────────
  if (autoLeaders.length > 0) {
    const [top, ...rest] = autoLeaders;
    let a = `${top.name} has the most autograph cards in ${setName} with ${num(top.c)}.`;
    if (rest.length > 0) {
      a += ` The next closest ${rest.length === 1 ? "is" : "are"} ${joinList(rest.map((r) => `${r.name} (${num(r.c)})`))}.`;
    }
    faqs.push({ q: `Which ${nouns.singular} has the most autograph cards in ${setName}?`, a });
  }

  // ── Q5: most likely break hit ────────────────────────────────────────────
  if (pool.length > 0 && breakBoxConfig) {
    const bulk = await getBulkAthleteAnyCardOdds(setId, pool, breakBoxConfig, 1);
    const top5 = bulk.slice(0, 5);
    if (top5.length > 0) {
      const [top, ...rest] = top5;
      let a = `Based on ${oddsLabel} pack odds, ${top.playerName} is the most likely ${nouns.singular} to pull from a single box of ${setName}, with a ${pct(top.probability)} chance.`;
      if (rest.length > 0) {
        a += ` The next most likely are ${joinList(rest.map((r) => `${r.playerName} (${pct(r.probability)})`))}.`;
      }
      faqs.push({
        q: `Which ${nouns.singular} are you most likely to pull from a box of ${setName}?`,
        a,
      });
    }
  }

  // ── Q6: team with most cards ─────────────────────────────────────────────
  if (nouns.teamLabel) {
    const teamTotals = new Map<string, number>();
    for (const e of leaderboard) {
      if (!e.team) continue;
      teamTotals.set(e.team, (teamTotals.get(e.team) ?? 0) + e.totalCards);
    }
    const teams = [...teamTotals.entries()].sort((a, b) => b[1] - a[1]).slice(0, 5);
    if (teams.length > 0) {
      const [[topTeam, topCount], ...rest] = teams;
      let a = `${topTeam} leads ${setName} with ${cardsWord(topCount)}.`;
      if (rest.length > 0) {
        a += ` The next closest ${rest.length === 1 ? "is" : "are"} ${joinList(rest.map(([t, c]) => `${t} (${num(c)})`))}.`;
      }
      faqs.push({ q: `Which ${nouns.teamLabel} has the most cards in ${setName}?`, a });
    }
  }

  // ── Q7: team with most autograph cards ───────────────────────────────────
  if (teamAutoLeaders.length > 0 && nouns.teamLabel) {
    const [top, ...rest] = teamAutoLeaders;
    let a = `${top.team} leads ${setName} with ${num(top.c)} autograph card${top.c !== 1 ? "s" : ""}.`;
    if (rest.length > 0) {
      a += ` The next closest ${rest.length === 1 ? "is" : "are"} ${joinList(rest.map((r) => `${r.team} (${num(r.c)})`))}.`;
    }
    faqs.push({ q: `Which ${nouns.teamLabel} has the most autograph cards in ${setName}?`, a });
  }

  // ── Q8: rookies ──────────────────────────────────────────────────────────
  const rookies = leaderboard.filter((e) => e.isRookie);
  if (rookies.length > 0) {
    const shown = rookies.slice(0, 10);
    const more = rookies.length - shown.length;
    let a = `${setName} features ${num(rookies.length)} rookie${rookies.length !== 1 ? "s" : ""}. The most featured ${shown.length === 1 ? "is" : "are"} ${joinList(shown.map((r) => `${r.name} (${cardsWord(r.totalCards)})`))}`;
    if (more > 0) a += `, and ${num(more)} more`;
    a += ".";
    faqs.push({ q: `Which rookies are in ${setName}?`, a });
  }

  // ── Q9: parallels ────────────────────────────────────────────────────────
  if (parallelTypes > 0) {
    let a = `${setName} has ${num(parallelTypes)} distinct parallel types.`;
    if (baseLadder.length > 0) {
      const shown = baseLadder.slice(0, 12);
      const more = baseLadder.length - shown.length;
      a += ` The base set parallel ladder includes ${joinList(shown.map((p) => (p.printRun != null ? `${p.name} (/${num(p.printRun)})` : p.name)))}`;
      if (more > 0) a += `, and ${num(more)} more`;
      a += ".";
    }
    const printRuns = allParallels.map((p) => p.printRun).filter((n): n is number => n != null);
    if (printRuns.length > 0) {
      const max = Math.max(...printRuns);
      const min = Math.min(...printRuns);
      a += max === min
        ? ` Serial-numbered parallels are limited to /${num(min)}.`
        : ` Print runs range from /${num(max)} to /${num(min)}.`;
    }
    faqs.push({ q: `How many parallels are in ${setName}?`, a });
  }

  // ── Q10: hardest pulls ───────────────────────────────────────────────────
  if (pool.length > 0) {
    const hardest = [...pool]
      .sort((a, b) => a.weight - b.weight)
      .slice(0, 5)
      .map((e) => ({
        label: e.parallelName ? `${e.insertSetName} ${e.parallelName}` : e.insertSetName,
        display: denomToDisplay(1 / e.weight),
      }));
    if (hardest.length > 0) {
      const [top, ...rest] = hardest;
      let a = `Based on ${oddsLabel} pack odds, the hardest card to pull in ${setName} is ${top.label} at ${top.display} packs.`;
      if (rest.length > 0) {
        a += ` Other tough pulls include ${joinList(rest.map((h) => `${h.label} (${h.display})`))}.`;
      }
      faqs.push({ q: `What are the hardest cards to pull in ${setName}?`, a });
    }
  }

  // ── Q11: release date ────────────────────────────────────────────────────
  const isFuture = releaseDate ? releaseDate > new Date().toISOString().slice(0, 10) : false;
  if (releaseDate) {
    faqs.push({
      q: isFuture ? `When does ${setName} release?` : `When was ${setName} released?`,
      a: isFuture
        ? `${setName} releases on ${formatDate(releaseDate)}.`
        : `${setName} was released on ${formatDate(releaseDate)}.`,
    });
  }

  // ── Q12: box formats ─────────────────────────────────────────────────────
  const formats = parseBoxFormats(boxConfig);
  if (formats.length > 0) {
    const sentences = formats.map((f) => {
      if (f.tba) return `${f.label} box configuration is TBA.`;
      const parts: string[] = [];
      if (f.packsPerBox != null && f.cardsPerPack != null) {
        parts.push(`${num(f.packsPerBox)} packs of ${num(f.cardsPerPack)} cards`);
      } else if (f.packsPerBox != null) {
        parts.push(`${num(f.packsPerBox)} packs`);
      } else if (f.cardsPerPack != null) {
        parts.push(`${num(f.cardsPerPack)} cards per pack`);
      }
      if (f.autosPerBox != null && f.autosPerBox > 0) {
        parts.push(`${num(f.autosPerBox)} autograph${f.autosPerBox !== 1 ? "s" : ""} per box`);
      }
      let s = `${f.label} boxes contain ${parts.join(" with ")}`;
      if (f.boxesPerCase != null) s += ` (${num(f.boxesPerCase)} boxes per case)`;
      return s + ".";
    });
    faqs.push({
      q: `What box formats are available for ${setName}?`,
      a: sentences.join(" "),
    });
  }

  // ── Q13: insert sets ─────────────────────────────────────────────────────
  if (insertSubsets.length > 0) {
    const shown = insertSubsets.slice(0, 12);
    const more = insertSubsets.length - shown.length;
    let a = `${setName} includes ${num(insertSubsets.length)} insert sets: ${joinList(shown.map((s) => s.name))}`;
    if (more > 0) a += `, and ${num(more)} more`;
    a += ".";
    faqs.push({ q: `What insert sets are in ${setName}?`, a });
  }

  // ── Summary paragraph ────────────────────────────────────────────────────
  const { year, manufacturer } = extractYearAndManufacturer(setName);
  const sportNoun = sport.toLowerCase();
  const includingParts: string[] = [];
  if (baseCount > 0) includingParts.push(`${num(baseCount)} base cards`);
  if (autographCount > 0) includingParts.push(`${num(autographCount)} autograph cards`);
  if (parallelTypes > 0) includingParts.push(`${num(parallelTypes)} parallel types`);

  let summary = `${setName} is a ${year ? `${year} ` : ""}${manufacturer} ${sportNoun} release featuring ${num(totalCards)} cards across ${num(subsetCount)} subsets`;
  if (includingParts.length > 0) summary += `, including ${joinList(includingParts)}`;
  summary += ".";
  if (releaseDate) {
    summary += isFuture
      ? ` It releases on ${formatDate(releaseDate)}.`
      : ` It was released on ${formatDate(releaseDate)}.`;
  }
  const formatsWithData = formats.filter((f) => !f.tba);
  if (formatsWithData.length > 0) {
    summary += ` Box formats include ${joinList(
      formatsWithData.map((f) =>
        f.packsPerBox != null && f.cardsPerPack != null
          ? `${f.label} (${num(f.packsPerBox)} packs × ${num(f.cardsPerPack)} cards)`
          : f.label
      )
    )}.`;
  } else if (formats.length > 0) {
    summary += ` Box configuration is TBA.`;
  }

  return { summary, faqs };
}
