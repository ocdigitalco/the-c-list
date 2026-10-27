import type { Metadata } from "next";
import { getAthleteIndex, getIndexSports } from "@/lib/athletes/queries";
import { AthletesIndexClient } from "@/components/athletes/AthletesIndexClient";
import { SITE_URL } from "@/lib/setSeo";

// Static index: top 60 by cards, no searchParams read in the server render. All
// search / sport / rookie / sort / load-more is deferred to GET /api/athletes
// (edge-cached), so this page never becomes per-request dynamic.
export const revalidate = 86400;

export const metadata: Metadata = {
  title: "Athletes — every player's card checklist | Checklist²",
  description:
    "Browse every athlete, character, and creator across every trading card set. Find anyone to see all their cards — autographs, numbered parallels, rookie cards, and more.",
  alternates: { canonical: `${SITE_URL}/athletes` },
  openGraph: {
    title: "Athletes — every player's card checklist | Checklist²",
    description:
      "Browse every athlete, character, and creator across every trading card set. Find anyone to see all their cards.",
    url: `${SITE_URL}/athletes`,
    type: "website",
    siteName: "Checklist²",
  },
};

export default async function AthletesIndexPage() {
  const [first, sportRows] = await Promise.all([getAthleteIndex({ sort: "cards", page: 0 }), getIndexSports()]);
  const totalAll = first.total;
  const sports = sportRows.map((s) => s.sport);

  return (
    <AthletesIndexClient
      initialTiles={first.tiles}
      initialTotal={first.total}
      initialHasMore={first.hasMore}
      sports={sports}
      totalAll={totalAll}
    />
  );
}
