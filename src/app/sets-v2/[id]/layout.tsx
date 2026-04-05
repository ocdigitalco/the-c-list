import { db, rawQuery } from "@/lib/db";
import { sets, insertSets, players, playerAppearances } from "@/lib/schema";
import { eq, and, inArray } from "drizzle-orm";
import { notFound } from "next/navigation";
import { V2Shell } from "@/components/sets-v2/V2Shell";
import type { SidebarPlayer, BoxFormatSummary, BoxConfigSingle, BoxConfigMulti } from "@/components/sets-v2/types";

export const dynamic = "force-dynamic";

const BOX_LABEL_MAP: Record<string, string> = {
  hobby: "Hobby",
  jumbo: "Jumbo",
  mega: "Mega",
  blaster: "Blaster",
  value: "Value",
  fat_pack: "Fat Pack",
  hanger: "Hanger",
  breakers_delight: "Breaker's Delight",
  first_day_issue: "First Day Issue",
  breaker: "Breaker",
  hobby_hybrid: "Hobby Hybrid",
  sapphire: "Sapphire",
  hongbao: "Hongbao",
  logofractor: "Logofractor",
  ffnyc: "FFNYC",
};

function formatBoxLabel(key: string): string {
  return BOX_LABEL_MAP[key] ?? key.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function isMultiConfig(cfg: BoxConfigSingle | BoxConfigMulti): cfg is BoxConfigMulti {
  const first = Object.values(cfg)[0];
  return first !== null && typeof first === "object";
}

export default async function V2Layout({
  params,
  children,
}: {
  params: Promise<{ id: string }>;
  children: React.ReactNode;
}) {
  const { id } = await params;
  const setId = parseInt(id, 10);
  if (isNaN(setId)) notFound();

  const setRow = await db.query.sets.findFirst({
    where: (t, { eq }) => eq(t.id, setId),
  });
  if (!setRow) notFound();

  // Players for sidebar
  const allPlayers = await db.query.players.findMany({
    where: (t, { eq }) => eq(t.setId, setId),
    orderBy: (p, { asc }) => [asc(p.name)],
  });

  // Detect rookies
  const insertSetIdRows = await db
    .select({ id: insertSets.id })
    .from(insertSets)
    .where(eq(insertSets.setId, setId));
  const insertSetIds = insertSetIdRows.map((r) => r.id);

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

  const sidebarPlayers: SidebarPlayer[] = allPlayers.map((p) => ({
    id: p.id,
    name: p.name,
    totalCards: p.uniqueCards,
    hasRookie: rookiePlayerIds.has(p.id),
  }));

  // Box format summaries
  const boxFormats: BoxFormatSummary[] = (() => {
    if (!setRow.boxConfig) return [];
    const raw = JSON.parse(setRow.boxConfig) as BoxConfigSingle | BoxConfigMulti;
    if (isMultiConfig(raw)) {
      return Object.entries(raw).map(([key, fmt]) => ({
        label: formatBoxLabel(key),
        packsPerBox: fmt.packs_per_box ?? 1,
        autosPerBox:
          fmt.autos_per_box ??
          fmt.autos_or_memorabilia_per_box ??
          fmt.autos_or_relics_per_box ??
          fmt.autos_or_auto_relics_per_box ??
          0,
        notes: fmt.notes ?? fmt.note,
      }));
    }
    const flat = raw as BoxConfigSingle;
    return [
      {
        label: "Hobby",
        packsPerBox: flat.packs_per_box ?? 1,
        autosPerBox:
          flat.autos_per_box ??
          flat.autos_or_memorabilia_per_box ??
          flat.autos_or_relics_per_box ??
          flat.autos_or_auto_relics_per_box ??
          0,
        notes: flat.notes ?? flat.note,
      },
    ];
  })();

  return (
    <V2Shell
      setId={setId}
      setName={setRow.name}
      sport={setRow.sport}
      league={setRow.league ?? null}
      season={setRow.season}
      tier={setRow.tier}
      releaseDate={setRow.releaseDate ?? null}
      sampleImageUrl={setRow.sampleImageUrl ?? null}
      boxFormats={boxFormats}
      players={sidebarPlayers}
    >
      {children}
    </V2Shell>
  );
}
