import { db, rawQuery } from "@/lib/db";
import { sets } from "@/lib/schema";
import { notFound, redirect } from "next/navigation";
import { TeamDetailClient } from "@/components/sets/TeamDetailClient";

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

  // ── Team aggregate stats ──────────────────────────────────────────────────
  const teamStats = await rawQuery.get<{
    totalCards: number;
    numberedParallels: number;
    oneOfOnes: number;
  }>(
    `SELECT
       COUNT(DISTINCT pa.id) AS totalCards,
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
     FROM player_appearances pa
     JOIN insert_sets i ON i.id = pa.insert_set_id
     WHERE i.set_id = ? AND pa.team = ?`,
    setId, teamName, setId, teamName, setId, teamName
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
    />
  );
}
