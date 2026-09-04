/**
 * send-odds-alerts.ts <set-slug> [--dry-run]
 *
 * Sends the one-time "pack odds are live" email to everyone who signed up for a
 * set's odds alert. Run MANUALLY, against Turso only, AFTER
 *   npx tsx scripts/migrate-to-turso.ts <set-slug>
 * has attached the odds. Refuses to run if the set still has no odds.
 *
 * set_alerts is production-owned (Turso is the source of truth); this script
 * both reads and updates it directly on Turso.
 */
import { createClient } from "@libsql/client";
import { config } from "dotenv";
import { Resend } from "resend";

config({ path: ".env.local" });

const FROM = "Checklist² <updates@updates.checklist2.com>";
const SITE = "https://checklist2.com";
const BATCH = 10;
const BATCH_DELAY_MS = 1100;

function escapeHtml(s: string): string {
  return s
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}

function oddsAbsent(packOdds: string | null): boolean {
  if (!packOdds || packOdds.trim() === "") return true;
  try {
    const o = JSON.parse(packOdds);
    return !o || typeof o !== "object" || Object.keys(o).length === 0;
  } catch {
    return false;
  }
}

function emailHtml(setName: string, slug: string, token: string): string {
  const url = `${SITE}/sets/${slug}`;
  const unsub = `${SITE}/api/alerts/unsubscribe?token=${token}`;
  const name = escapeHtml(setName);
  return `<!doctype html><html><body style="margin:0;background:#F7F5F0;font-family:Inter,system-ui,-apple-system,sans-serif;color:#0E0E0E;">
  <div style="max-width:520px;margin:0 auto;padding:32px 24px;">
    <p style="font-size:16px;line-height:1.6;margin:0 0 20px;">
      Good news — Topps has published the pack odds for <strong>${name}</strong>. You can now see the full pull rates for every parallel and insert.
    </p>
    <p style="margin:0 0 24px;">
      <a href="${url}" style="display:inline-block;background:#D63A20;color:#ffffff;text-decoration:none;font-weight:600;font-size:15px;padding:12px 22px;border-radius:8px;">View the odds</a>
    </p>
    <hr style="border:none;border-top:1px solid #E7E2D6;margin:24px 0;" />
    <p style="font-size:12px;color:#5A5247;line-height:1.6;margin:0 0 8px;">
      Checklist² earns a commission on qualifying eBay purchases through these links.
    </p>
    <p style="font-size:12px;color:#5A5247;line-height:1.6;margin:0;">
      You&rsquo;re getting this because you asked to be notified about this set.
      <a href="${unsub}" style="color:#5A5247;">Unsubscribe</a>.
    </p>
  </div>
</body></html>`;
}

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

async function main() {
  const args = process.argv.slice(2);
  const dryRun = args.includes("--dry-run");
  const slug = args.find((a) => !a.startsWith("--"));
  if (!slug) {
    console.error("Usage: npx tsx scripts/send-odds-alerts.ts <set-slug> [--dry-run]");
    process.exit(1);
  }

  const url = process.env.TURSO_DATABASE_URL;
  const authToken = process.env.TURSO_AUTH_TOKEN;
  if (!url) {
    console.error("TURSO_DATABASE_URL not set — this script runs against Turso only.");
    process.exit(1);
  }
  const db = createClient({ url, authToken });

  // Resolve the set on Turso.
  const setRes = await db.execute({
    sql: "SELECT id, name, pack_odds FROM sets WHERE slug = ?",
    args: [slug],
  });
  if (setRes.rows.length === 0) {
    console.error(`Set not found for slug "${slug}".`);
    process.exit(1);
  }
  const set = setRes.rows[0] as unknown as { id: number; name: string; pack_odds: string | null };

  // Guard: refuse to run if odds are still unpublished.
  if (oddsAbsent(set.pack_odds)) {
    console.error(`Refusing to send: "${set.name}" (${slug}) still has no pack odds on Turso.`);
    console.error("Attach odds and migrate first, then re-run.");
    process.exit(1);
  }

  const pending = (await db.execute({
    sql: "SELECT id, email, token FROM set_alerts WHERE set_id = ? AND notified_at IS NULL ORDER BY id",
    args: [set.id],
  })).rows as unknown as { id: number; email: string; token: string }[];

  if (pending.length === 0) {
    console.log(`No pending subscribers for "${set.name}". Nothing to send. (sent 0 / failed 0 / skipped 0)`);
    return;
  }

  const subject = `Pack odds are live: ${set.name}`;

  if (dryRun) {
    console.log(`[DRY RUN] Would send "${subject}" to ${pending.length} recipient(s):`);
    for (const r of pending) console.log(`  - ${r.email}`);
    console.log(`\n(sent 0 / failed 0 / skipped ${pending.length}) — dry run, nothing sent.`);
    return;
  }

  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) {
    console.error("RESEND_API_KEY not set.");
    process.exit(1);
  }
  const resend = new Resend(apiKey);

  let sent = 0, failed = 0;
  for (let i = 0; i < pending.length; i += BATCH) {
    const batch = pending.slice(i, i + BATCH);
    for (const r of batch) {
      try {
        const { error } = await resend.emails.send({
          from: FROM,
          to: r.email,
          subject,
          html: emailHtml(set.name, slug, r.token),
        });
        if (error) {
          failed++;
          console.error(`  ✗ ${r.email}: ${JSON.stringify(error)}`);
          continue;
        }
        // Mark notified only after a successful send.
        await db.execute({
          sql: "UPDATE set_alerts SET notified_at = datetime('now') WHERE id = ?",
          args: [r.id],
        });
        sent++;
        console.log(`  ✓ ${r.email}`);
      } catch (err) {
        failed++;
        console.error(`  ✗ ${r.email}: ${err instanceof Error ? err.message : String(err)}`);
      }
    }
    if (i + BATCH < pending.length) await sleep(BATCH_DELAY_MS);
  }

  console.log(`\nDone: sent ${sent} / failed ${failed} / skipped 0 (of ${pending.length} pending).`);
  if (failed > 0) process.exit(1);
}

main();
