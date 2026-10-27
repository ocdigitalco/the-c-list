import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { loadAthlete, loadAthletePage, buildAthleteMetadata, matchesSegment } from "@/lib/athletes/seo";
import { AthleteMasterPage } from "@/components/athletes/AthleteMasterPage";

const SEGMENT = "characters"; // page_kind = character

// Static on first request, cached until the data changes (the migration
// revalidates each touched athlete's path). No cookies/searchParams are read in
// the server render, so the page is fully cacheable.
export const revalidate = false;
export const dynamicParams = true;
export function generateStaticParams() {
  return [];
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const core = await loadAthlete(slug);
  if (!core || !matchesSegment(core, SEGMENT)) return {};
  const data = await loadAthletePage(core);
  return buildAthleteMetadata(core, data);
}

export default async function CharacterPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const core = await loadAthlete(slug);
  if (!core || !matchesSegment(core, SEGMENT)) notFound();
  return <AthleteMasterPage core={core} />;
}
