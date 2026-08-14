import { db, rawQuery } from "@/lib/db";
import {
  sets,
  players,
  insertSets,
  parallels,
  playerAppearances,
} from "@/lib/schema";
import { eq, inArray, sql, and } from "drizzle-orm";
import { notFound, redirect } from "next/navigation";
import type { Metadata } from "next";
import { SetDetailClient, type RelatedLink, type SubsetChecklist } from "@/components/sets/SetDetailClient";
import type { LeaderboardRow } from "@/components/sets/types";
import type { BreakSheetPlayer } from "@/components/BreakSheetModal";
import { articles } from "@/lib/articles";
import { buildSetMeta, computeSetAeo, SITE_URL } from "@/lib/setSeo";
import { getCardGalleryImages } from "@/lib/cardGallery";

export const revalidate = 3600;

export async function generateMetadata({
  params,
}: {
  params: Promise<{ id: string }>;
}): Promise<Metadata> {
  const { id: rawParam } = await params;
  const isNumeric = /^\d+$/.test(rawParam);

  interface MetaRow {
    id: number;
    name: string;
    img: string | null;
    hasOdds: number;
    slug: string | null;
  }
  let row: MetaRow | undefined;
  try {
    row = isNumeric
      ? await rawQuery.get<MetaRow>(
          `SELECT id, name, sample_image_url AS img,
                  (pack_odds IS NOT NULL) AS hasOdds, slug
           FROM sets WHERE id = ?`,
          parseInt(rawParam, 10)
        )
      : await rawQuery.get<MetaRow>(
          `SELECT id, name, sample_image_url AS img,
                  (pack_odds IS NOT NULL) AS hasOdds, slug
           FROM sets WHERE slug = ?`,
          rawParam
        );
  } catch { /* slug column may not exist yet */ }
  if (!row) return {};

  const cardRow = await rawQuery.get<{ c: number }>(
    `SELECT COUNT(*) AS c
     FROM player_appearances pa
     JOIN insert_sets i ON i.id = pa.insert_set_id
     WHERE i.set_id = ?`,
    row.id
  );

  const { title, description } = buildSetMeta(row.name, cardRow?.c ?? 0, !!row.hasOdds);
  const url = `${SITE_URL}/sets/${row.slug ?? row.id}`;
  const ogImage = row.img ? `${SITE_URL}${row.img}` : undefined;

  return {
    title,
    description,
    alternates: { canonical: url },
    openGraph: {
      title,
      description,
      url,
      type: "website",
      siteName: "Checklist²",
      ...(ogImage ? { images: [{ url: ogImage }] } : {}),
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
      ...(ogImage ? { images: [ogImage] } : {}),
    },
  };
}

export default async function V2SetPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id: rawParam } = await params;
  const isNumeric = /^\d+$/.test(rawParam);

  let setRow;
  if (isNumeric) {
    setRow = await db.query.sets.findFirst({
      where: (t, { eq }) => eq(t.id, parseInt(rawParam, 10)),
    });
    // Redirect numeric ID to slug URL if slug exists
    if (setRow) {
      let slug: string | null = null;
      try {
        const slugRow = await rawQuery.get<{ slug: string | null }>(
          "SELECT slug FROM sets WHERE id = ?", setRow.id
        );
        slug = slugRow?.slug ?? null;
      } catch { /* slug column may not exist yet */ }
      if (slug) redirect(`/sets/${slug}`);
    }
  } else {
    // Try slug lookup
    try {
      const slugRow = await rawQuery.get<{ id: number }>(
        "SELECT id FROM sets WHERE slug = ?", rawParam
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

  // Canonical slug for static-asset lookup. The card-image gallery lives in
  // public/sets/cards/{slug}/; read it server-side (Node runtime, works at
  // build + ISR revalidation). Returns [] when the folder is absent, so
  // folderless sets render no gallery.
  let canonicalSlug: string | null = null;
  try {
    const slugRow = await rawQuery.get<{ slug: string | null }>(
      "SELECT slug FROM sets WHERE id = ?",
      setId
    );
    canonicalSlug = slugRow?.slug ?? null;
  } catch { /* slug column may not exist yet */ }
  const cardImages = await getCardGalleryImages(canonicalSlug);

  // Optional per-set Topps product URL (added via ALTER, not in the Drizzle
  // schema — read defensively like slug so pre-migration Turso doesn't error).
  let toppsUrl: string | null = null;
  try {
    const urlRow = await rawQuery.get<{ topps_url: string | null }>(
      "SELECT topps_url FROM sets WHERE id = ?",
      setId
    );
    toppsUrl = urlRow?.topps_url ?? null;
  } catch { /* topps_url column may not exist yet */ }

  // Related article links (JSON array of {url, source, title, description}) —
  // read defensively; the column is added via ALTER and may not exist pre-migration.
  let relatedLinks: RelatedLink[] = [];
  try {
    const linkRow = await rawQuery.get<{ related_links: string | null }>(
      "SELECT related_links FROM sets WHERE id = ?",
      setId
    );
    if (linkRow?.related_links) {
      const parsed = JSON.parse(linkRow.related_links);
      if (Array.isArray(parsed)) relatedLinks = parsed as RelatedLink[];
    }
  } catch { /* related_links column may not exist yet, or invalid JSON */ }

  // Insert set IDs
  const insertSetIdRows = await db
    .select({ id: insertSets.id })
    .from(insertSets)
    .where(eq(insertSets.setId, setId));
  const insertSetIds = insertSetIdRows.map((r) => r.id);

  // ── Stats ─────────────────────────────────────────────────────────────────
  const [athleteCountRow] = await db
    .select({ count: sql<number>`cast(count(*) as integer)` })
    .from(players)
    .where(eq(players.setId, setId));

  // Determine the dominant subject role for display labels
  const dominantRoleRow = await rawQuery.get<{ role: string }>(
    `SELECT subject_role as role FROM players WHERE set_id = ? GROUP BY subject_role ORDER BY COUNT(*) DESC LIMIT 1`,
    setId
  );
  const subjectLabel = dominantRoleRow?.role === "character" ? "Characters"
    : dominantRoleRow?.role === "coach" ? "Coaches"
    : dominantRoleRow?.role === "celebrity" ? "Celebrities"
    : dominantRoleRow?.role === "sketch_artist" ? "Sketch Artists"
    : dominantRoleRow?.role === "attraction" ? "Attractions"
    : "Athletes";
  // For entertainment sets the "team" field holds a movie/franchise, not a sports team.
  const teamLabel = dominantRoleRow?.role === "character" ? "Movie" : "Team";

  const [cardCountRow] = await db
    .select({ count: sql<number>`cast(count(*) as integer)` })
    .from(playerAppearances)
    .where(
      insertSetIds.length > 0
        ? inArray(playerAppearances.insertSetId, insertSetIds)
        : sql`1 = 0`
    );

  const [parallelTypesRow] = await db
    .select({ count: sql<number>`cast(count(distinct ${parallels.name}) as integer)` })
    .from(parallels)
    .where(
      insertSetIds.length > 0 ? inArray(parallels.insertSetId, insertSetIds) : sql`1 = 0`
    );

  const totalParallelsResult =
    insertSetIds.length > 0
      ? ((await rawQuery.get<{ total: number }>(
          `SELECT COALESCE(SUM(apps * pars), 0) AS total FROM (
             SELECT
               (SELECT COUNT(*) FROM player_appearances WHERE insert_set_id = i.id) AS apps,
               (SELECT COUNT(*) FROM parallels WHERE insert_set_id = i.id) AS pars
             FROM insert_sets i
             WHERE i.id IN (${insertSetIds.map(() => "?").join(",")})
           )`,
          ...insertSetIds
        )) ?? { total: 0 })
      : { total: 0 };

  const autoInsertSetIds =
    insertSetIds.length > 0
      ? (
          await db
            .select({ id: insertSets.id })
            .from(insertSets)
            .where(
              and(
                inArray(insertSets.id, insertSetIds),
                eq(insertSets.isAutograph, true)
              )
            )
        ).map((r) => r.id)
      : [];

  // Names of autograph subsets — the single source of truth for classifying
  // odds keys into the Autograph Odds tab (see categorize() in SetDetailClient).
  const autographSubsetNames =
    insertSetIds.length > 0
      ? (
          await db
            .select({ name: insertSets.name })
            .from(insertSets)
            .where(
              and(
                inArray(insertSets.id, insertSetIds),
                eq(insertSets.isAutograph, true)
              )
            )
        ).map((r) => r.name)
      : [];

  const [autographCountRow] = await db
    .select({ count: sql<number>`cast(count(*) as integer)` })
    .from(playerAppearances)
    .where(
      autoInsertSetIds.length > 0
        ? inArray(playerAppearances.insertSetId, autoInsertSetIds)
        : sql`1 = 0`
    );

  const autoParallelsResult =
    autoInsertSetIds.length > 0
      ? ((await rawQuery.get<{ total: number }>(
          `SELECT COALESCE(SUM(apps * pars), 0) AS total FROM (
             SELECT
               (SELECT COUNT(*) FROM player_appearances WHERE insert_set_id = i.id) AS apps,
               (SELECT COUNT(*) FROM parallels WHERE insert_set_id = i.id) AS pars
             FROM insert_sets i
             WHERE i.id IN (${autoInsertSetIds.map(() => "?").join(",")})
           )`,
          ...autoInsertSetIds
        )) ?? { total: 0 })
      : { total: 0 };

  // All parallels (name + print_run) for odds matching
  const allParallelsRaw =
    insertSetIds.length > 0
      ? await rawQuery.all<{ name: string; printRun: number | null }>(
          `SELECT DISTINCT name, print_run AS printRun FROM parallels WHERE insert_set_id IN (${insertSetIds.map(() => "?").join(",")})`,
          ...insertSetIds
        )
      : [];
  const allParallels = allParallelsRaw.map((p) => ({ name: p.name, printRun: p.printRun ?? null }));

  // Per-subset checklists for the card-type tabs (Base/Insert/Relic/Autograph/Booklets).
  // One row per appearance (primary subject); flags drive tab membership client-side.
  let subsetChecklists: SubsetChecklist[] = [];
  if (insertSetIds.length > 0) {
    const ph = insertSetIds.map(() => "?").join(",");
    const subRows = await rawQuery.all<{
      id: number; name: string; is_autograph: number; is_base: number; is_relic: number; is_booklet: number;
    }>(
      `SELECT id, name, is_autograph, is_base, is_relic, is_booklet FROM insert_sets WHERE set_id = ? ORDER BY id`,
      setId
    );
    const appRows = await rawQuery.all<{
      insert_set_id: number; code: string; player: string; team: string | null; is_rookie: number;
    }>(
      `SELECT pa.insert_set_id, pa.card_number AS code, p.name AS player, pa.team, pa.is_rookie
       FROM player_appearances pa JOIN players p ON p.id = pa.player_id
       WHERE pa.insert_set_id IN (${ph}) ORDER BY pa.insert_set_id, pa.id`,
      ...insertSetIds
    );
    const parRows = await rawQuery.all<{ insert_set_id: number; name: string; print_run: number | null }>(
      `SELECT insert_set_id, name, print_run FROM parallels WHERE insert_set_id IN (${ph}) ORDER BY insert_set_id, id`,
      ...insertSetIds
    );
    const appsBy = new Map<number, { code: string; player: string; team: string | null; isRookie: boolean }[]>();
    for (const a of appRows) {
      if (!appsBy.has(a.insert_set_id)) appsBy.set(a.insert_set_id, []);
      appsBy.get(a.insert_set_id)!.push({ code: a.code, player: a.player, team: a.team, isRookie: !!a.is_rookie });
    }
    const parsBy = new Map<number, { name: string; printRun: number | null }[]>();
    for (const p of parRows) {
      if (!parsBy.has(p.insert_set_id)) parsBy.set(p.insert_set_id, []);
      parsBy.get(p.insert_set_id)!.push({ name: p.name, printRun: p.print_run ?? null });
    }
    subsetChecklists = subRows.map((s) => ({
      name: s.name,
      isAutograph: !!s.is_autograph,
      isBase: !!s.is_base,
      isRelic: !!s.is_relic,
      isBooklet: !!s.is_booklet,
      cards: appsBy.get(s.id) ?? [],
      parallels: parsBy.get(s.id) ?? [],
    }));
  }

  // Numbered parallels
  const numberedParallelsResult =
    insertSetIds.length > 0
      ? ((await rawQuery.get<{ total: number }>(
          `SELECT COUNT(*) AS total FROM parallels WHERE insert_set_id IN (${insertSetIds.map(() => "?").join(",")}) AND print_run IS NOT NULL`,
          ...insertSetIds
        )) ?? { total: 0 })
      : { total: 0 };

  // ── Break Sheet data ───────────────────────────────────────────────────────
  const allPlayers = await db.query.players.findMany({
    where: (t, { eq: e }) => e(t.setId, setId),
    orderBy: (p, { asc: a }) => [a(p.name)],
  });

  const rookieRows =
    insertSetIds.length > 0
      ? await db
          .selectDistinct({ playerId: playerAppearances.playerId })
          .from(playerAppearances)
          .where(
            and(
              eq(playerAppearances.isRookie, true),
              inArray(playerAppearances.insertSetId, insertSetIds)
            )
          )
      : [];
  const rookiePlayerIds = new Set(rookieRows.map((r) => r.playerId));

  function classifyIS(name: string, isAutoFlag?: boolean): "base" | "pure_auto" | "mem_auto" | "relic" | "insert" {
    if (name === "Base Set") return "base";
    const lower = name.toLowerCase();
    const isAuto = isAutoFlag || /auto|autograph|signature|signed|ink|script|mark/.test(lower);
    const isRelic = /relic|memorabilia/.test(lower);
    if (isAuto && isRelic) return "mem_auto";
    if (isAuto) return "pure_auto";
    if (isRelic) return "relic";
    return "insert";
  }

  const allAppearancesForSheet =
    insertSetIds.length > 0
      ? await db
          .select({ playerId: playerAppearances.playerId, insertSetName: insertSets.name, isAutograph: insertSets.isAutograph })
          .from(playerAppearances)
          .innerJoin(insertSets, eq(playerAppearances.insertSetId, insertSets.id))
          .where(
            and(
              inArray(playerAppearances.insertSetId, insertSetIds),
              sql`${insertSets.name} != 'Base Set'`
            )
          )
      : [];

  type PlayerBreakAccum = {
    autoSetNames: Set<string>;
    hasMemAuto: boolean;
    hasRelic: boolean;
    insertSetNamesSet: Set<string>;
  };
  const breakMap = new Map<number, PlayerBreakAccum>();
  for (const p of allPlayers) {
    breakMap.set(p.id, { autoSetNames: new Set(), hasMemAuto: false, hasRelic: false, insertSetNamesSet: new Set() });
  }
  for (const app of allAppearancesForSheet) {
    const e = breakMap.get(app.playerId);
    if (!e) continue;
    const type = classifyIS(app.insertSetName, !!app.isAutograph);
    if (type === "pure_auto") e.autoSetNames.add(app.insertSetName);
    else if (type === "mem_auto") e.hasMemAuto = true;
    else if (type === "relic") e.hasRelic = true;
    else if (type === "insert") e.insertSetNamesSet.add(app.insertSetName);
  }

  const breakSheetPlayers: BreakSheetPlayer[] = allPlayers.map((p) => {
    const d = breakMap.get(p.id)!;
    return {
      id: p.id,
      name: p.name,
      autoCount: d.autoSetNames.size,
      hasMemAuto: d.hasMemAuto,
      hasRelic: d.hasRelic,
      isRookie: rookiePlayerIds.has(p.id),
      insertSetNames: Array.from(d.insertSetNamesSet),
    };
  });

  // ── Leaderboard ─────────────────────────────────────────────────────────────
  const leaderboardRaw = await rawQuery.all<{
    id: number;
    name: string;
    slug: string | null;
    totalCards: number;
    isRookie: number;
    team: string | null;
    autographs: number;
    inserts: number;
    numberedParallels: number;
    nbaPlayerId: number | null;
    ufcImageUrl: string | null;
    mlbPlayerId: number | null;
    imageUrl: string | null;
  }>(
    `WITH team_counts AS (
       -- Per-player team frequency; empty/NULL teams excluded. Counts both direct
       -- appearances and co-subject links (co-subjects inherit the card's team).
       SELECT player_id, team, COUNT(*) AS cnt, MAX(is_base) AS is_base
       FROM (
         SELECT pa.player_id AS player_id, pa.team AS team,
                CASE WHEN i2.name = 'Base Set' THEN 1 ELSE 0 END AS is_base
         FROM player_appearances pa
         INNER JOIN players p2 ON p2.id = pa.player_id
         LEFT JOIN insert_sets i2 ON i2.id = pa.insert_set_id
         WHERE p2.set_id = ? AND pa.team IS NOT NULL AND pa.team != ''
         UNION ALL
         SELECT cp.co_player_id AS player_id, pa.team AS team,
                CASE WHEN i2.name = 'Base Set' THEN 1 ELSE 0 END AS is_base
         FROM appearance_co_players cp
         INNER JOIN player_appearances pa ON pa.id = cp.appearance_id
         INNER JOIN players p2 ON p2.id = cp.co_player_id
         LEFT JOIN insert_sets i2 ON i2.id = pa.insert_set_id
         WHERE p2.set_id = ? AND pa.team IS NOT NULL AND pa.team != ''
       )
       GROUP BY player_id, team
     ),
     team_mode AS (
       -- Most-frequent team wins; ties → base-set team, then alphabetical (deterministic).
       SELECT player_id, team FROM (
         SELECT player_id, team,
           ROW_NUMBER() OVER (
             PARTITION BY player_id ORDER BY cnt DESC, is_base DESC, team ASC
           ) AS rn
         FROM team_counts
       ) WHERE rn = 1
     ),
     player_is AS (
       SELECT DISTINCT pa.player_id, pa.insert_set_id
       FROM player_appearances pa
       INNER JOIN players p ON p.id = pa.player_id
       WHERE p.set_id = ?
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
       tm.team AS team,
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
     LEFT JOIN player_appearances pa ON pa.player_id = p.id
     LEFT JOIN insert_sets i ON i.id = pa.insert_set_id
     LEFT JOIN numbered n ON n.player_id = p.id
     LEFT JOIN team_mode tm ON tm.player_id = p.id
     WHERE p.set_id = ?
     GROUP BY p.id
     ORDER BY p.unique_cards DESC`,
    setId,
    setId,
    setId,
    setId
  );

  const leaderboardEntries: LeaderboardRow[] = leaderboardRaw.map((r) => ({
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

  const hasTeamData = leaderboardEntries.some((e) => e.team != null && e.team !== "");

  // ── SEO / AEO: summary, Q&A, structured data ────────────────────────────
  const { description: metaDescription } = buildSetMeta(
    setRow.name,
    cardCountRow.count,
    !!setRow.packOdds
  );
  const aeo = await computeSetAeo({
    setId,
    setName: setRow.name,
    sport: setRow.sport,
    releaseDate: setRow.releaseDate ?? null,
    packOdds: setRow.packOdds ?? null,
    boxConfig: setRow.boxConfig ?? null,
    totalCards: cardCountRow.count,
    autographCount: autographCountRow.count,
    parallelTypes: parallelTypesRow.count,
    numberedParallels: numberedParallelsResult.total,
    allParallels,
    subjectRole: dominantRoleRow?.role ?? null,
    leaderboard: leaderboardEntries.map((e) => ({
      id: e.id,
      name: e.name,
      totalCards: e.totalCards,
      isRookie: e.isRookie,
      team: e.team,
    })),
  });

  const pageUrl = `${SITE_URL}/sets/${rawParam}`;
  const datasetLd = {
    "@context": "https://schema.org",
    "@type": "Dataset",
    name: `${setRow.name} Checklist`,
    description: metaDescription,
    url: pageUrl,
    creator: { "@type": "Organization", name: "Checklist²", url: SITE_URL },
    keywords: [
      setRow.name,
      `${setRow.name} checklist`,
      `${setRow.name} pack odds`,
      `${setRow.sport} cards`,
      "sports card checklist",
    ],
    ...(setRow.releaseDate ? { datePublished: setRow.releaseDate } : {}),
  };
  const faqLd =
    aeo.faqs.length > 0
      ? {
          "@context": "https://schema.org",
          "@type": "FAQPage",
          mainEntity: aeo.faqs.map((f) => ({
            "@type": "Question",
            name: f.q,
            acceptedAnswer: { "@type": "Answer", text: f.a },
          })),
        }
      : null;
  const toJsonLd = (obj: unknown) => JSON.stringify(obj).replace(/</g, "\\u003c");

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: toJsonLd(datasetLd) }}
      />
      {faqLd && (
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: toJsonLd(faqLd) }}
        />
      )}
      <SetDetailClient
      setName={setRow.name}
      sport={setRow.sport}
      league={setRow.league ?? null}
      tier={setRow.tier}
      releaseDate={setRow.releaseDate ?? null}
      setId={setId}
      setSlug={rawParam}
      sampleImageUrl={setRow.sampleImageUrl ?? null}
      cards={cardCountRow.count}
      cardTypes={insertSetIds.length}
      parallelTypes={parallelTypesRow.count}
      autographs={autographCountRow.count}
      autoParallels={autoParallelsResult.total}
      totalParallels={totalParallelsResult.total}
      athleteCount={athleteCountRow.count}
      subjectLabel={subjectLabel}
      teamLabel={teamLabel}
      hasChecklist={cardCountRow.count > 0}
      hasNumberedParallels={numberedParallelsResult.total > 0}
      hasBoxConfig={!!setRow.boxConfig}
      hasPackOdds={!!setRow.packOdds}
      subsets={subsetChecklists}
      relatedLinks={relatedLinks}
      boxConfig={setRow.boxConfig ?? null}
      packOdds={setRow.packOdds ?? null}
      entries={leaderboardEntries}
      hasTeamData={hasTeamData}
      breakSheetPlayers={breakSheetPlayers}
      parallelsList={allParallels}
      autographSubsetNames={autographSubsetNames}
      featuredArticle={articles.find((a) => a.setId === setId) ? {
        slug: articles.find((a) => a.setId === setId)!.id,
        title: articles.find((a) => a.setId === setId)!.title,
        description: articles.find((a) => a.setId === setId)!.description,
        heroImage: articles.find((a) => a.setId === setId)!.heroImage,
      } : null}
        aeoSummary={aeo.summary}
        faqs={aeo.faqs}
        cardImages={cardImages}
        toppsUrl={toppsUrl}
      />
    </>
  );
}
