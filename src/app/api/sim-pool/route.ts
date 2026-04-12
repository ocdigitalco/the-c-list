import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { buildSimPool } from "@/lib/breakSimulator";

export async function GET(request: NextRequest) {
  const setId = Number(request.nextUrl.searchParams.get("setId"));
  const boxType = request.nextUrl.searchParams.get("boxType") ?? "hobby";

  if (isNaN(setId) || setId <= 0) {
    return NextResponse.json({ error: "Invalid setId" }, { status: 400 });
  }

  const setRow = await db.query.sets.findFirst({
    where: (t, { eq }) => eq(t.id, setId),
  });

  if (!setRow) {
    return NextResponse.json({ error: "Set not found" }, { status: 404 });
  }

  const simConfig = await buildSimPool(
    setId,
    setRow.packOdds,
    setRow.boxConfig,
    boxType
  );

  if (!simConfig) {
    return NextResponse.json(
      { error: "Simulation not available for this set/box type" },
      { status: 404 }
    );
  }

  return NextResponse.json(simConfig);
}
