import { db } from "@/lib/db";
import { setAlerts } from "@/lib/schema";
import { eq } from "drizzle-orm";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

function page(): string {
  // Minimal branded confirmation. Identical output whether or not the token
  // matched — we never reveal whether a subscription existed.
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="robots" content="noindex" />
<title>Unsubscribed — Checklist²</title>
<style>
  :root { color-scheme: light; }
  body { margin:0; background:#F7F5F0; color:#0E0E0E;
         font-family: 'Inter', system-ui, -apple-system, sans-serif;
         display:flex; align-items:center; justify-content:center; min-height:100vh; padding:24px; }
  .card { background:#FFFFFF; border:1px solid #E7E2D6; border-radius:12px;
          max-width:460px; width:100%; padding:32px 28px; text-align:center; }
  h1 { font-size:20px; margin:0 0 10px; }
  p { font-size:15px; line-height:1.6; color:#5A5247; margin:0 0 20px; }
  a { display:inline-block; background:#D63A20; color:#fff; text-decoration:none;
      font-weight:600; font-size:14px; padding:10px 18px; border-radius:8px; }
</style>
</head>
<body>
  <div class="card">
    <h1>You won&rsquo;t be notified about this set.</h1>
    <p>Your email has been removed from this set&rsquo;s odds alert. You can sign up again any time from the set page.</p>
    <a href="https://checklist2.com/sets">Browse sets</a>
  </div>
</body>
</html>`;
}

export async function GET(req: Request) {
  const token = new URL(req.url).searchParams.get("token") ?? "";
  if (token) {
    try {
      await db.delete(setAlerts).where(eq(setAlerts.token, token));
    } catch (err) {
      // Deletion failure shouldn't change what the visitor sees.
      console.error("[alerts/unsubscribe] delete failed:", err);
    }
  }
  return new Response(page(), {
    status: 200,
    headers: { "Content-Type": "text/html; charset=utf-8" },
  });
}
