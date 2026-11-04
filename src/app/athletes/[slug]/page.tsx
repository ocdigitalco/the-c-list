import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { loadAthlete, loadAthletePage, buildAthleteMetadata, matchesSegment } from "@/lib/athletes/seo";
import { AthleteMasterPage } from "@/components/athletes/AthleteMasterPage";

const SEGMENT = "athletes"; // page_kind = player

// Static on first request. On-demand revalidation (the migration revalidates
// each touched path) refreshes the page when the data changes; the 7-day timer
// is a safety net so a bad render can't persist indefinitely. No
// cookies/searchParams are read in the server render, so the page is fully cacheable.
export const revalidate = 604800; // 7 days
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

export default async function AthletePage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const core = await loadAthlete(slug);
  if (!core || !matchesSegment(core, SEGMENT)) notFound();
  return <AthleteMasterPage core={core} />;
}
