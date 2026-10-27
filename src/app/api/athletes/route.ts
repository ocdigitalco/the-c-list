import { NextRequest, NextResponse } from "next/server";
import { getAthleteIndex, type AthleteSort } from "@/lib/athletes/queries";

export const runtime = "nodejs";
// Cacheable at the edge; the index page itself stays static and defers search /
// filter / sort / load-more here. Not per-request dynamic.
export const revalidate = 86400;

const SORTS: AthleteSort[] = ["cards", "az", "newest", "trending"];

export async function GET(req: NextRequest) {
  const sp = req.nextUrl.searchParams;
  const sortParam = sp.get("sort") as AthleteSort | null;
  const sort: AthleteSort = sortParam && SORTS.includes(sortParam) ? sortParam : "cards";
  const page = Math.max(0, parseInt(sp.get("page") ?? "0", 10) || 0);

  const result = await getAthleteIndex({
    sport: sp.get("sport"),
    q: sp.get("q"),
    rookie: sp.get("rookie") === "1" || sp.get("rookie") === "true",
    sort,
    page,
  });

  return NextResponse.json(result, {
    headers: {
      "Cache-Control": "public, s-maxage=86400, stale-while-revalidate=86400",
    },
  });
}
