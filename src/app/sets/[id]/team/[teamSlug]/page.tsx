import { db, rawQuery } from "@/lib/db";
import { sets } from "@/lib/schema";
import { notFound, redirect } from "next/navigation";
import { TeamDetailClient } from "@/components/sets/TeamDetailClient";
import { findOddsKey } from "@/lib/oddsUtils";
import type { PackOddsSlot, BoxFormat } from "@/components/PackOddsCalculator";

export const revalidate = 3600;

function slugify(text: string): string {
  return text.toLowerCase().replace(/[^\w\s-]/g, "").replace(/[\s_]+/g, "-").replace(/-+/g, "-").trim();
}

export default async function TeamDetailPage({
  params,
}: {
  params: Promise<{ id: string; teamSlug: string }>;
}) {
  const { id: rawSetParam, teamSlug } = await params;
  const isNumeric = /^\d+$/.test(rawSetParam);

  // Resolve set
  let setRow;
  if (isNumeric) {
    setRow = await db.query.sets.findFirst({
      where: (t, { eq }) => eq(t.id, parseInt(rawSetParam, 10)),
    });
    if (setRow) {
      let slug: string | null = null;
      try {
        const slugRow = await rawQuery.get<{ slug: string | null }>(
          "SELECT slug FROM sets WHERE id = ?", setRow.id
        );
        slug = slugRow?.slug ?? null;
      } catch { /* slug column may not exist yet */ }
      if (slug) redirect(`/sets/${slug}/team/${teamSlug}`);
    }
  } else {
    try {
      const slugRow = await rawQuery.get<{ id: number }>(
        "SELECT id FROM sets WHERE slug = ?", rawSetParam
      );
      if (slugRow) {
        setRow = await db.query.sets.findFirst({
          where: (t, { eq }) => eq(t.id, slugRow.id),
        });
      }
    } catch { /* slug column may not exist yet */ }
  }
  if (!setRow) notFound();

  const setId = setRow.id;

  // Decode the team slug back to team name by finding teams in this set
  const allTeamsRaw = await rawQuery.all<{ team: string }>(
    `SELECT DISTINCT pa.team FROM player_appearances pa
     JOIN insert_sets i ON i.id = pa.insert_set_id
     WHERE i.set_id = ? AND pa.team IS NOT NULL AND pa.team != ''`,
    setId
  );
  const allTeams = allTeamsRaw.map((r) => r.team);

  // Match slug to team name
  const teamName = allTeams.find((t) => slugify(t) === teamSlug);
  if (!teamName) notFound();

  // ── Team athletes with aggregates ─────────────────────────────────────────
  const athleteRows = await rawQuery.all<{
    id: number;
    name: string;
    slug: string | null;
    totalCards: number;
    isRookie: number;
    team: string;
    autographs: number;
    inserts: number;
    numberedParallels: number;
    nbaPlayerId: number | null;
    ufcImageUrl: string | null;
    mlbPlayerId: number | null;
    imageUrl: string | null;
  }>(
    `WITH player_is AS (
       SELECT DISTINCT pa.player_id, pa.insert_set_id
       FROM player_appearances pa
       INNER JOIN players p ON p.id = pa.player_id
       INNER JOIN insert_sets i ON i.id = pa.insert_set_id
       WHERE p.set_id = ? AND pa.team = ?
     ),
     numbered AS (
       SELECT pis.player_id, COUNT(*) AS cnt
       FROM player_is pis
       INNER JOIN parallels par ON par.insert_set_id = pis.insert_set_id
       WHERE par.print_run IS NOT NULL
       GROUP BY pis.player_id
     )
     SELECT
       p.id,
       p.name,
       p.slug,
       p.unique_cards AS totalCards,
       CAST(MAX(CASE WHEN pa.is_rookie = 1 THEN 1 ELSE 0 END) AS INTEGER) AS isRookie,
       ? AS team,
       COUNT(DISTINCT CASE
         WHEN lower(i.name) LIKE '%auto%'
           OR lower(i.name) LIKE '%signature%'
           OR lower(i.name) LIKE '%signed%'
           OR lower(i.name) LIKE '%autograph%'
         THEN pa.insert_set_id END) AS autographs,
       COUNT(DISTINCT CASE
         WHEN i.name != 'Base Set'
           AND lower(i.name) NOT LIKE '%auto%'
           AND lower(i.name) NOT LIKE '%signature%'
           AND lower(i.name) NOT LIKE '%signed%'
           AND lower(i.name) NOT LIKE '%autograph%'
         THEN pa.insert_set_id END) AS inserts,
       COALESCE(n.cnt, 0) AS numberedParallels,
       p.nba_player_id AS nbaPlayerId,
       p.ufc_image_url AS ufcImageUrl,
       p.mlb_player_id AS mlbPlayerId,
       p.image_url AS imageUrl
     FROM players p
     INNER JOIN player_appearances pa ON pa.player_id = p.id
     INNER JOIN insert_sets i ON i.id = pa.insert_set_id
     LEFT JOIN numbered n ON n.player_id = p.id
     WHERE p.set_id = ? AND pa.team = ?
     GROUP BY p.id
     ORDER BY p.unique_cards DESC`,
    setId, teamName, teamName, setId, teamName
  );

  // ── Team aggregate stats (matches leaderboard aggregation: sum of unique_cards) ──
  const teamStats = await rawQuery.get<{
    totalCards: number;
    numberedParallels: number;
    oneOfOnes: number;
  }>(
    `SELECT
       (SELECT COALESCE(SUM(p2.unique_cards), 0) FROM players p2
        WHERE p2.set_id = ? AND p2.id IN (
          SELECT DISTINCT pa2.player_id FROM player_appearances pa2
          JOIN insert_sets i2 ON i2.id = pa2.insert_set_id
          WHERE i2.set_id = ? AND pa2.team = ?
        )) AS totalCards,
       (SELECT COUNT(*) FROM parallels par
        WHERE par.insert_set_id IN (
          SELECT DISTINCT pa2.insert_set_id FROM player_appearances pa2
          JOIN insert_sets i2 ON i2.id = pa2.insert_set_id
          WHERE i2.set_id = ? AND pa2.team = ?
        ) AND par.print_run IS NOT NULL) AS numberedParallels,
       (SELECT COUNT(*) FROM parallels par
        WHERE par.insert_set_id IN (
          SELECT DISTINCT pa2.insert_set_id FROM player_appearances pa2
          JOIN insert_sets i2 ON i2.id = pa2.insert_set_id
          WHERE i2.set_id = ? AND pa2.team = ?
        ) AND par.print_run = 1) AS oneOfOnes
     FROM (SELECT 1)`,
    setId, setId, teamName, setId, teamName, setId, teamName
  );

  // ── Teams in set (for drawer/switcher) ────────────────────────────────────
  const teamsInSet = await rawQuery.all<{
    team: string;
    athletes: number;
    totalCards: number;
  }>(
    `SELECT
       pa.team,
       COUNT(DISTINCT pa.player_id) AS athletes,
       COUNT(DISTINCT pa.id) AS totalCards
     FROM player_appearances pa
     JOIN insert_sets i ON i.id = pa.insert_set_id
     WHERE i.set_id = ? AND pa.team IS NOT NULL AND pa.team != ''
     GROUP BY pa.team
     ORDER BY pa.team`,
    setId
  );

  // ── Set-wide leaderboard (for left column) ────────────────────────────────
  const leaderboardRaw = await rawQuery.all<{
    id: number; name: string; slug: string | null; totalCards: number;
    isRookie: number; team: string | null; autographs: number; inserts: number;
    numberedParallels: number; nbaPlayerId: number | null; ufcImageUrl: string | null;
    mlbPlayerId: number | null; imageUrl: string | null;
  }>(
    `WITH player_is AS (
       SELECT DISTINCT pa.player_id, pa.insert_set_id
       FROM player_appearances pa INNER JOIN players p ON p.id = pa.player_id WHERE p.set_id = ?
     ),
     numbered AS (
       SELECT pis.player_id, COUNT(*) AS cnt FROM player_is pis
       INNER JOIN parallels par ON par.insert_set_id = pis.insert_set_id
       WHERE par.print_run IS NOT NULL GROUP BY pis.player_id
     )
     SELECT p.id, p.name, p.slug, p.unique_cards AS totalCards,
       CAST(MAX(CASE WHEN pa.is_rookie = 1 THEN 1 ELSE 0 END) AS INTEGER) AS isRookie,
       MAX(pa.team) AS team,
       COUNT(DISTINCT CASE WHEN i.is_autograph = 1 THEN pa.insert_set_id END) AS autographs,
       COUNT(DISTINCT CASE WHEN i.name != 'Base Set' AND i.is_autograph = 0 THEN pa.insert_set_id END) AS inserts,
       COALESCE(n.cnt, 0) AS numberedParallels,
       p.nba_player_id AS nbaPlayerId, p.ufc_image_url AS ufcImageUrl,
       p.mlb_player_id AS mlbPlayerId, p.image_url AS imageUrl
     FROM players p
     LEFT JOIN player_appearances pa ON pa.player_id = p.id
     LEFT JOIN insert_sets i ON i.id = pa.insert_set_id
     LEFT JOIN numbered n ON n.player_id = p.id
     WHERE p.set_id = ? GROUP BY p.id ORDER BY p.unique_cards DESC`,
    setId, setId
  );
  const leaderboardEntries = leaderboardRaw.map((r) => ({
    id: r.id, name: r.name, slug: r.slug, team: r.team,
    isRookie: r.isRookie === 1, totalCards: r.totalCards,
    autographs: r.autographs, inserts: r.inserts,
    numberedParallels: r.numberedParallels, nbaPlayerId: r.nbaPlayerId,
    ufcImageUrl: r.ufcImageUrl, mlbPlayerId: r.mlbPlayerId, imageUrl: r.imageUrl,
  }));
  const hasTeamData = leaderboardEntries.some((e) => e.team != null && e.team !== "");

  const athletes = athleteRows.map((r) => ({
    id: r.id,
    name: r.name,
    slug: r.slug,
    team: r.team,
    isRookie: r.isRookie === 1,
    totalCards: r.totalCards,
    autographs: r.autographs,
    inserts: r.inserts,
    numberedParallels: r.numberedParallels,
    nbaPlayerId: r.nbaPlayerId,
    ufcImageUrl: r.ufcImageUrl,
    mlbPlayerId: r.mlbPlayerId,
    imageUrl: r.imageUrl,
  }));

  // ── Break Hit Calculator data (team-aggregated) ────────────────────────────
  const hasBoxConfig = !!setRow.boxConfig;
  const hasPackOdds = !!setRow.packOdds;
  let packOddsSlotsByFormat: Record<string, PackOddsSlot[]> = {};
  let boxFormats: BoxFormat[] = [];
  let totalAutoCards = 0;
  let teamAutoCards = 0;

  if (hasBoxConfig) {
    try {
      const rawBox = JSON.parse(setRow.boxConfig!);
      const BOX_LABEL_MAP: Record<string, string> = {
        hobby: "Hobby", jumbo: "Jumbo", hobby_jumbo: "Hobby Jumbo",
        mega: "Mega", blaster: "Blaster", value: "Value",
        breakers_delight: "Breaker's Delight",
      };
      for (const [k, cfg] of Object.entries(rawBox as Record<string, Record<string, number | null>>)) {
        const label = BOX_LABEL_MAP[k] ?? k.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
        boxFormats.push({
          label,
          boxesPerCase: (cfg.boxes_per_case as number) ?? 8,
          packsPerCase: ((cfg.boxes_per_case as number) ?? 8) * ((cfg.packs_per_box as number) ?? 1),
          packsPerBox: (cfg.packs_per_box as number) ?? 1,
          guaranteedAutos: (cfg.autos_per_box as number) ?? 0,
          note: cfg.notes as unknown as string | undefined,
        });
      }
    } catch { /* ignore */ }
  }

  if (hasPackOdds && athleteRows.length > 0) {
    const { normalizeOddsObj } = await import("@/lib/parseOdds");
    const rawOdds = JSON.parse(setRow.packOdds!);
    const firstVal = Object.values(rawOdds)[0];
    const isNestedOdds = firstVal !== null && typeof firstVal === "object";

    // Get all insert sets this team's athletes appear in
    const teamPlayerIds = athleteRows.map((r) => r.id);
    const teamInsertSets = await rawQuery.all<{
      insert_set_id: number; name: string; is_autograph: number;
      team_apps: number; total_apps: number;
    }>(
      `SELECT i.id AS insert_set_id, i.name, i.is_autograph,
              COUNT(DISTINCT CASE WHEN pa.player_id IN (${teamPlayerIds.map(() => "?").join(",")}) THEN pa.id END) AS team_apps,
              COUNT(DISTINCT pa.id) AS total_apps
       FROM insert_sets i
       JOIN player_appearances pa ON pa.insert_set_id = i.id
       WHERE i.set_id = ?
       GROUP BY i.id`,
      ...teamPlayerIds, setId
    );

    // Get parallels for these insert sets
    const isIds = teamInsertSets.map((r) => r.insert_set_id);
    const parallelRows = isIds.length > 0
      ? await rawQuery.all<{ insert_set_id: number; name: string; print_run: number | null }>(
          `SELECT insert_set_id, name, print_run FROM parallels WHERE insert_set_id IN (${isIds.map(() => "?").join(",")})`,
          ...isIds
        )
      : [];
    const parallelsByIS = new Map<number, typeof parallelRows>();
    for (const p of parallelRows) {
      if (!parallelsByIS.has(p.insert_set_id)) parallelsByIS.set(p.insert_set_id, []);
      parallelsByIS.get(p.insert_set_id)!.push(p);
    }

    const autoKeywords = ["auto", "signature", "graph", "relic", "dual", "triple", "ink", "script", "mark"];

    function resolvePrefix(name: string, packOddsData: Record<string, number>): string {
      if (name === "Base Set") return findOddsKey("Base Set", Object.keys(packOddsData)) ?? "Base";
      const found = findOddsKey(name, Object.keys(packOddsData));
      if (found) return found;
      // Prefer the subset's own name when odds keys are composed as "{name} <tier>"
      // (e.g. "Base Cards Base" / "Base Cards Refractors").
      if (Object.keys(packOddsData).some((k) => k.startsWith(`${name} `))) return name;
      if (name.startsWith("Base")) {
        if ("Base Cards" in packOddsData) return "Base Cards";
      }
      return name;
    }

    function buildSlots(packOddsData: Record<string, number>): PackOddsSlot[] {
      return teamInsertSets.map((is) => {
        const isAuto = is.is_autograph === 1 || autoKeywords.some((kw) => is.name.toLowerCase().includes(kw));
        const prefix = resolvePrefix(is.name, packOddsData);
        const baseDenom = packOddsData[prefix] ?? packOddsData[`${prefix} Refractor`] ?? packOddsData[`${prefix} Base`] ?? packOddsData[`${prefix} Refractors`] ?? null;
        const pars = parallelsByIS.get(is.insert_set_id) ?? [];
        return {
          insertSetName: is.name,
          playerApps: is.team_apps,
          totalApps: is.total_apps,
          baseOddsDenom: baseDenom,
          isAuto,
          serializedParallels: pars
            .filter((p) => p.print_run !== null)
            .map((p) => ({
              name: p.name,
              printRun: p.print_run!,
              denom: packOddsData[`${prefix} ${p.name}`] ?? null,
            })),
        };
      });
    }

    if (isNestedOdds) {
      for (const [key, data] of Object.entries(rawOdds as Record<string, Record<string, unknown>>)) {
        const label = key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
        const BOX_LABEL_MAP: Record<string, string> = { hobby: "Hobby", hobby_jumbo: "Hobby Jumbo", mega: "Mega", value: "Value", breakers_delight: "Breaker's Delight" };
        const resolvedLabel = BOX_LABEL_MAP[key] ?? label;
        if (!(resolvedLabel in packOddsSlotsByFormat)) {
          packOddsSlotsByFormat[resolvedLabel] = buildSlots(normalizeOddsObj(data));
        }
      }
    } else {
      const slots = buildSlots(normalizeOddsObj(rawOdds as Record<string, unknown>));
      for (const fmt of boxFormats) {
        packOddsSlotsByFormat[fmt.label] = slots;
      }
      if (boxFormats.length === 0) packOddsSlotsByFormat["default"] = slots;
    }

    // Total auto cards in set
    totalAutoCards = teamInsertSets
      .filter((is) => is.is_autograph === 1 || autoKeywords.some((kw) => is.name.toLowerCase().includes(kw)))
      .reduce((sum, is) => sum + is.total_apps, 0);

    // Team auto cards
    teamAutoCards = teamInsertSets
      .filter((is) => is.is_autograph === 1 || autoKeywords.some((kw) => is.name.toLowerCase().includes(kw)))
      .reduce((sum, is) => sum + is.team_apps, 0);
  }

  const hasBreakCalc = hasBoxConfig && hasPackOdds && Object.keys(packOddsSlotsByFormat).length > 0;

  return (
    <TeamDetailClient
      setName={setRow.name}
      setSlug={rawSetParam}
      setId={setId}
      sport={setRow.sport}
      league={setRow.league ?? null}
      teamName={teamName}
      teamSlug={teamSlug}
      athletes={athletes}
      athleteCount={athleteRows.length}
      totalCards={teamStats?.totalCards ?? 0}
      numberedParallels={teamStats?.numberedParallels ?? 0}
      oneOfOnes={teamStats?.oneOfOnes ?? 0}
      teamsInSet={teamsInSet.map((t) => ({
        name: t.team,
        slug: slugify(t.team),
        athletes: t.athletes,
        totalCards: t.totalCards,
      }))}
      leaderboardEntries={leaderboardEntries}
      hasLeaderboardTeamData={hasTeamData}
      packOddsJson={setRow.packOdds ?? null}
      boxConfigJson={setRow.boxConfig ?? null}
      packOddsSlotsByFormat={packOddsSlotsByFormat}
      boxFormats={boxFormats}
      totalAutoCards={totalAutoCards}
      teamAutoCards={teamAutoCards}
      hasBreakCalc={hasBreakCalc}
    />
  );
}
