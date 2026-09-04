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
import { writeFileSync } from "fs";

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

// Verbatim from the athlete-tab affiliate disclosure (AthleteShopDisclosure).
const DISCLOSURE = "Checklist² earns a commission on qualifying eBay purchases through these links.";

// Build the formats line from pack_odds keys. pack_odds keys are the format
// identifiers ("hobby", "jumbo", …) but also include non-pack odds groups
// (box toppers, loaders, case hits) that shouldn't be described as "pack odds";
// those are excluded before building the line.
const NON_PACK_KEY = /topper|loader|case/i;
function formatsLine(packOdds: string | null): string {
  let keys: string[] = [];
  if (packOdds && packOdds.trim() !== "") {
    try {
      const o = JSON.parse(packOdds);
      if (o && typeof o === "object") keys = Object.keys(o);
    } catch {
      /* ignore */
    }
  }
  const names = keys
    .filter((k) => !NON_PACK_KEY.test(k))
    .map((k) => k.toLowerCase().replace(/_/g, " "));
  if (names.length === 0) return "Topps has published the pack odds for this set.";
  if (names.length === 1) return `Topps has published the ${names[0]} pack odds for this set.`;
  if (names.length === 2) return `Topps has published the ${names[0]} and ${names[1]} pack odds for this set.`;
  const head = names.slice(0, -1).join(", ");
  const last = names[names.length - 1];
  return `Topps has published the ${head}, and ${last} pack odds for this set.`;
}

function emailHtml(setName: string, slug: string, token: string, packOdds: string | null): string {
  const setUrl = `${SITE}/sets/${slug}`;
  const unsubUrl = `${SITE}/api/alerts/unsubscribe?token=${token}`;
  const name = escapeHtml(setName);
  const formatsLineText = escapeHtml(formatsLine(packOdds));
  const disclosure = escapeHtml(DISCLOSURE);
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pack odds are live: ${name}</title>
<link href="https://fonts.googleapis.com/css2?family=Carter+One&family=Inter:wght@400;500&display=swap" rel="stylesheet">
</head>
<body style="margin:0;padding:0;background:#F7F5F0;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#F7F5F0;">
  <tr>
    <td align="center" style="padding:32px 16px;">
      <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;">

        <tr>
          <td align="center" style="padding:0 0 18px;font-family:'Carter One',Georgia,serif;font-size:26px;line-height:1;color:#0E0E0E;">
            Checklist<span style="display:inline-block;background:#D63A20;color:#F1EDE4;font-size:14px;line-height:1;padding:3px 5px;border-radius:3px;vertical-align:top;margin-left:2px;font-family:'Carter One',Georgia,serif;">2</span>
          </td>
        </tr>

        <tr>
          <td style="background:#FFFFFF;border:1px solid #E4E0D6;border-radius:10px;padding:28px 28px 24px;">
            <p style="margin:0 0 6px;font-family:Inter,Helvetica,Arial,sans-serif;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:#6B6860;">Odds published</p>
            <p style="margin:0 0 14px;font-family:'Carter One',Georgia,serif;font-size:24px;line-height:1.2;color:#0E0E0E;">${name}</p>
            <p style="margin:0 0 22px;font-family:Inter,Helvetica,Arial,sans-serif;font-size:15px;line-height:1.6;color:#0E0E0E;">${formatsLineText} Every parallel and insert now shows its pull rate, and the box breakdown is filled in.</p>
            <table role="presentation" cellpadding="0" cellspacing="0">
              <tr>
                <td style="background:#0E0E0E;border-radius:6px;">
                  <a href="${setUrl}" style="display:inline-block;padding:12px 20px;font-family:Inter,Helvetica,Arial,sans-serif;font-size:15px;font-weight:500;color:#F1EDE4;text-decoration:none;">View the odds</a>
                </td>
              </tr>
            </table>
            <p style="margin:22px 0 0;font-family:Inter,Helvetica,Arial,sans-serif;font-size:13px;line-height:1.5;color:#6B6860;">You asked for one email when this set's odds were added. This is it.</p>
          </td>
        </tr>

        <tr>
          <td align="center" style="padding:18px 8px 0;font-family:Inter,Helvetica,Arial,sans-serif;font-size:12px;line-height:1.7;color:#6B6860;">
            <p style="margin:0;">${disclosure}</p>
            <p style="margin:0;"><a href="${unsubUrl}" style="color:#6B6860;text-decoration:underline;">Stop alerts for this set</a> &nbsp;&middot;&nbsp; <a href="https://checklist2.com/updates" style="color:#6B6860;text-decoration:underline;">Latest updates</a></p>
          </td>
        </tr>

      </table>
    </td>
  </tr>
</table>
</body>
</html>`;
}

// Plain-text alternative: the three lines of copy plus the two URLs.
function emailText(setName: string, slug: string, token: string, packOdds: string | null): string {
  const setUrl = `${SITE}/sets/${slug}`;
  const unsubUrl = `${SITE}/api/alerts/unsubscribe?token=${token}`;
  return [
    formatsLine(packOdds),
    "Every parallel and insert now shows its pull rate, and the box breakdown is filled in.",
    "You asked for one email when this set's odds were added. This is it.",
    "",
    `View the odds: ${setUrl}`,
    `Stop alerts for this set: ${unsubUrl}`,
  ].join("\n");
}

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

async function main() {
  const args = process.argv.slice(2);
  const dryRun = args.includes("--dry-run");
  const preview = args.includes("--preview");
  const slug = args.find((a) => !a.startsWith("--"));
  if (!slug) {
    console.error("Usage: npx tsx scripts/send-odds-alerts.ts <set-slug> [--dry-run] [--preview]");
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

  // Preview: render the HTML to a file with a placeholder token and exit. Works
  // for sets with or without odds — it is a rendering check, not a send, so it
  // runs before the odds guard and never touches subscribers.
  if (preview) {
    const placeholderToken = "preview-token-0000000000000000000000000000000000000000000000000000";
    const html = emailHtml(set.name, slug, placeholderToken, set.pack_odds);
    const out = "/tmp/odds-alert-preview.html";
    writeFileSync(out, html, "utf8");
    console.log(`Preview written to ${out}`);
    return;
  }

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
          html: emailHtml(set.name, slug, r.token, set.pack_odds),
          text: emailText(set.name, slug, r.token, set.pack_odds),
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
