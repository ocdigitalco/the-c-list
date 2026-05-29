import { NextRequest, NextResponse } from "next/server";
import { revalidatePath } from "next/cache";

export async function POST(request: NextRequest) {
  const authHeader = request.headers.get("authorization");
  const expectedSecret = process.env.REVALIDATE_SECRET;

  if (!expectedSecret) {
    return NextResponse.json({ error: "REVALIDATE_SECRET not configured" }, { status: 500 });
  }

  if (authHeader !== `Bearer ${expectedSecret}`) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const body = await request.json().catch(() => ({}));
  const paths: string[] = Array.isArray(body.paths) ? body.paths : [];
  const setSlug: string | undefined = body.setSlug;

  if (paths.length === 0 && !setSlug) {
    return NextResponse.json({ error: "Must provide either paths array or setSlug" }, { status: 400 });
  }

  const revalidated: string[] = [];

  for (const path of paths) {
    try {
      revalidatePath(path);
      revalidated.push(path);
    } catch (err) {
      console.error(`Failed to revalidate ${path}:`, err);
    }
  }

  if (setSlug) {
    const setPaths = [
      "/",
      "/checklists",
      "/articles",
      `/sets/${setSlug}`,
    ];
    for (const path of setPaths) {
      try {
        revalidatePath(path, "page");
        revalidated.push(path);
      } catch (err) {
        console.error(`Failed to revalidate ${path}:`, err);
      }
    }
  }

  return NextResponse.json({ revalidated, timestamp: new Date().toISOString() });
}
