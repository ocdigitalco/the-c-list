import type { Metadata } from "next";
import { listSets } from "@/lib/queries/listSets";
import { getBreakSheetData } from "@/lib/queries/breakSheetData";
import { paramsToConfig } from "@/lib/breakSheet";
import { BreakSheetBuilderClient, type SetOption } from "./BreakSheetBuilderClient";

export const metadata: Metadata = {
  title: "Break Sheet Builder — Checklist²",
  description:
    "Build a Whatnot-ready break sheet from any set's checklist — auto-generated athlete titles, giveaways, pricing, and a shareable configuration.",
};

// Reads query params (set + compact config), so this page renders dynamically.
export const dynamic = "force-dynamic";

type SearchParams = Record<string, string | string[] | undefined>;

export default async function BreakSheetBuilderPage({
  searchParams,
}: {
  searchParams: Promise<SearchParams>;
}) {
  const sp = await searchParams;
  const get = (key: string): string | null => {
    const v = sp[key];
    return typeof v === "string" ? v : Array.isArray(v) ? v[0] ?? null : null;
  };

  const selectedSlug = get("set");
  const initialConfig = paramsToConfig(get);

  const [{ sets }, data] = await Promise.all([
    listSets(),
    selectedSlug ? getBreakSheetData(selectedSlug) : Promise.resolve(null),
  ]);

  // Sets that can actually be built into a sheet (have a slug + a checklist).
  const setOptions: SetOption[] = sets
    .filter((s) => s.slug && s.cardCount > 0)
    .map((s) => ({ slug: s.slug as string, name: s.name, sport: s.sport }));

  return (
    <BreakSheetBuilderClient setOptions={setOptions} data={data} initialConfig={initialConfig} />
  );
}
