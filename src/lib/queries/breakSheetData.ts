import { db, rawQuery } from "@/lib/db";
import { insertSets, playerAppearances } from "@/lib/schema";
import { and, eq, inArray, sql } from "drizzle-orm";
import type { BreakSheetData, BreakSheetPlayerRow } from "@/lib/breakSheet";
import type { BoxConfigSingle, BoxConfigMulti } from "@/components/sets-v2/types";

export type { BreakSheetData, BreakSheetPlayerRow };

/**
 * Classify an insert set the same way the set page does, so titles and the
 * autograph/relic/insert buckets stay consistent with the existing modal.
 */
function classifyIS(
  name: string,
  isAutoFlag?: boolean
): "base" | "pure_auto" | "mem_auto" | "relic" | "insert" {
  if (name === "Base Set") return "base";
  const lower = name.toLowerCase();
  const isAuto = isAutoFlag || /auto|autograph|signature|signed|ink|script|mark/.test(lower);
  const isRelic = /relic|memorabilia/.test(lower);
  if (isAuto && isRelic) return "mem_auto";
  if (isAuto) return "pure_auto";
  if (isRelic) return "relic";
  return "insert";
}

function isMultiConfig(cfg: BoxConfigSingle | BoxConfigMulti): cfg is BoxConfigMulti {
  const first = Object.values(cfg)[0];
  return first !== null && typeof first === "object";
}

function autosPerBoxOf(fmt: BoxConfigSingle): number | null {
  return (
    fmt.autos_per_box ??
    fmt.autos_or_memorabilia_per_box ??
    fmt.autos_or_relics_per_box ??
    fmt.autos_or_auto_relics_per_box ??
    null
  );
}

/**
 * Parse box config JSON and return the primary format's boxes-per-case and
 * autos-per-box. For multi-format configs, prefer "hobby" and otherwise the
 * first entry — matching how BoxConfigTable presents the headline numbers.
 */
function primaryBoxFormat(boxConfig: string | null): {
  boxesPerCase: number | null;
  autosPerBox: number | null;
} {
  if (!boxConfig) return { boxesPerCase: null, autosPerBox: null };
  let raw: BoxConfigSingle | BoxConfigMulti;
  try {
    raw = JSON.parse(boxConfig) as BoxConfigSingle | BoxConfigMulti;
  } catch {
    return { boxesPerCase: null, autosPerBox: null };
  }
  let fmt: BoxConfigSingle;
  if (isMultiConfig(raw)) {
    fmt = raw["hobby"] ?? Object.values(raw)[0];
    if (!fmt) return { boxesPerCase: null, autosPerBox: null };
  } else {
    fmt = raw;
  }
  return {
    boxesPerCase: fmt.boxes_per_case ?? null,
    autosPerBox: autosPerBoxOf(fmt),
  };
}

interface SetRow {
  id: number;
  name: string;
  sport: string;
  league: string | null;
  sampleImageUrl: string | null;
  boxConfig: string | null;
  slug: string | null;
}

async function resolveSet(slugOrId: string): Promise<SetRow | null> {
  const isNumeric = /^\d+$/.test(slugOrId);
  const query = `SELECT id, name, sport, league,
                        sample_image_url AS sampleImageUrl,
                        box_config AS boxConfig, slug
                 FROM sets WHERE ${isNumeric ? "id = ?" : "slug = ?"}`;
  const param: string | number = isNumeric ? parseInt(slugOrId, 10) : slugOrId;
  try {
    return (await rawQuery.get<SetRow>(query, param)) ?? null;
  } catch {
    // slug column may not exist yet on older DBs — fall back to id-only lookup
    if (!isNumeric) return null;
    return (
      (await rawQuery.get<SetRow>(
        `SELECT id, name, sport, league, sample_image_url AS sampleImageUrl,
                box_config AS boxConfig, NULL AS slug FROM sets WHERE id = ?`,
        parseInt(slugOrId, 10)
      )) ?? null
    );
  }
}

/**
 * Load everything the Break Sheet Builder needs for one set: every player with
 * their auto/mem-auto/relic/insert/numbered flags and team, the distinct team
 * list, and the primary box format's boxes-per-case / autos-per-box.
 *
 * Read-only. Reuses the same classification the set page applies to the modal.
 */
export async function getBreakSheetData(
  slugOrId: string
): Promise<BreakSheetData | null> {
  const setRow = await resolveSet(slugOrId);
  if (!setRow) return null;
  const setId = setRow.id;

  const insertSetIdRows = await db
    .select({ id: insertSets.id })
    .from(insertSets)
    .where(eq(insertSets.setId, setId));
  const insertSetIds = insertSetIdRows.map((r) => r.id);

  const allPlayers = await db.query.players.findMany({
    where: (t, { eq: e }) => e(t.setId, setId),
    orderBy: (p, { asc: a }) => [a(p.name)],
  });

  // Rookie player ids (from appearances within this set's insert sets)
  const rookiePlayerIds = new Set<number>();
  if (insertSetIds.length > 0) {
    const rookieRows = await db
      .selectDistinct({ playerId: playerAppearances.playerId })
      .from(playerAppearances)
      .where(
        and(
          eq(playerAppearances.isRookie, true),
          inArray(playerAppearances.insertSetId, insertSetIds)
        )
      );
    for (const r of rookieRows) rookiePlayerIds.add(r.playerId);
  }

  // Insert sets that carry at least one numbered parallel
  const numberedInsertSetIds = new Set<number>();
  if (insertSetIds.length > 0) {
    const rows = await rawQuery.all<{ insertSetId: number }>(
      `SELECT DISTINCT insert_set_id AS insertSetId FROM parallels
       WHERE insert_set_id IN (${insertSetIds.map(() => "?").join(",")})
         AND print_run IS NOT NULL`,
      ...insertSetIds
    );
    for (const r of rows) numberedInsertSetIds.add(r.insertSetId);
  }

  // Per-player appearances (name + id + auto flag) for classification & numbered
  const appearances =
    insertSetIds.length > 0
      ? await db
          .select({
            playerId: playerAppearances.playerId,
            insertSetId: playerAppearances.insertSetId,
            insertSetName: insertSets.name,
            isAutograph: insertSets.isAutograph,
          })
          .from(playerAppearances)
          .innerJoin(insertSets, eq(playerAppearances.insertSetId, insertSets.id))
          .where(
            and(
              inArray(playerAppearances.insertSetId, insertSetIds),
              sql`${insertSets.name} != 'Base Set'`
            )
          )
      : [];

  type Accum = {
    autoSetNames: Set<string>;
    hasMemAuto: boolean;
    hasRelic: boolean;
    hasNumbered: boolean;
    insertSetNames: Set<string>;
  };
  const accum = new Map<number, Accum>();
  for (const p of allPlayers) {
    accum.set(p.id, {
      autoSetNames: new Set(),
      hasMemAuto: false,
      hasRelic: false,
      hasNumbered: false,
      insertSetNames: new Set(),
    });
  }
  for (const a of appearances) {
    const e = accum.get(a.playerId);
    if (!e) continue;
    const type = classifyIS(a.insertSetName, !!a.isAutograph);
    if (type === "pure_auto") e.autoSetNames.add(a.insertSetName);
    else if (type === "mem_auto") e.hasMemAuto = true;
    else if (type === "relic") e.hasRelic = true;
    else if (type === "insert") e.insertSetNames.add(a.insertSetName);
    if (numberedInsertSetIds.has(a.insertSetId)) e.hasNumbered = true;
  }

  // Most-frequent team per player + distinct team list (excludes empty teams)
  const teamRows = await rawQuery.all<{ playerId: number; team: string; cnt: number }>(
    `SELECT pa.player_id AS playerId, pa.team AS team, COUNT(*) AS cnt
     FROM player_appearances pa
     INNER JOIN players p ON p.id = pa.player_id
     WHERE p.set_id = ? AND pa.team IS NOT NULL AND pa.team != ''
     GROUP BY pa.player_id, pa.team`,
    setId
  );
  const teamByPlayer = new Map<number, { team: string; cnt: number }>();
  const teamSet = new Set<string>();
  for (const r of teamRows) {
    teamSet.add(r.team);
    const cur = teamByPlayer.get(r.playerId);
    // tie-break deterministically on team name for stable output
    if (!cur || r.cnt > cur.cnt || (r.cnt === cur.cnt && r.team < cur.team)) {
      teamByPlayer.set(r.playerId, { team: r.team, cnt: r.cnt });
    }
  }

  const playersOut: BreakSheetPlayerRow[] = allPlayers.map((p) => {
    const d = accum.get(p.id)!;
    return {
      id: p.id,
      name: p.name,
      team: teamByPlayer.get(p.id)?.team ?? "",
      isRookie: rookiePlayerIds.has(p.id),
      autoCount: d.autoSetNames.size,
      hasMemAuto: d.hasMemAuto,
      hasRelic: d.hasRelic,
      hasInsert: d.insertSetNames.size > 0,
      hasNumbered: d.hasNumbered,
      insertSetNames: Array.from(d.insertSetNames),
    };
  });

  const teams = Array.from(teamSet).sort((a, b) => a.localeCompare(b));
  const { boxesPerCase, autosPerBox } = primaryBoxFormat(setRow.boxConfig);

  return {
    slug: setRow.slug ?? String(setRow.id),
    setName: setRow.name,
    sport: setRow.sport,
    league: setRow.league,
    sampleImageUrl: setRow.sampleImageUrl,
    athleteCount: playersOut.length,
    teamCount: teams.length,
    boxesPerCase,
    autosPerBox,
    players: playersOut,
    teams,
  };
}
