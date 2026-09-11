/**
 * Manual eBay sealed-box refresh (local/dev).
 *   npx tsx scripts/refresh-ebay-offers.ts [set-slug] [--query "override"]
 * No slug → all sets in the 18-month window. --query forces one query for every
 * format (used to test the nonsense-query / no-results path). Writes to whatever
 * @/lib/db targets (Turso when TURSO_DATABASE_URL is set, else local file).
 */
import { config } from "dotenv";
config({ path: ".env.local" });

(async () => {
  // Dynamic imports AFTER dotenv so db.ts reads TURSO_DATABASE_URL (ESM would
  // otherwise evaluate the db module before the config() call above).
  const { getRefreshPairs, refreshPair, sleep } = await import("../src/lib/ebayRefresh");
  const { getAppToken } = await import("../src/lib/ebayBrowse");

  const argv = process.argv.slice(2);
  const qIdx = argv.indexOf("--query");
  const queryOverride = qIdx >= 0 ? argv[qIdx + 1] : undefined;
  const slug = argv.find((a, i) => !a.startsWith("--") && !(qIdx >= 0 && i === qIdx + 1));

  const { pairs, setsInWindow, setsSkippedOld } = await getRefreshPairs({ slug });
  console.log(`${slug ? `set "${slug}"` : `all sets`}: ${pairs.length} (set,format) pairs  [sets in window: ${setsInWindow}, older skipped: ${setsSkippedOld}]`);
  if (pairs.length === 0) { console.log("nothing to refresh."); return; }
  if (queryOverride) console.log(`(query override: "${queryOverride}")`);

  const token = await getAppToken();
  let refreshed = 0, errors = 0;
  for (let i = 0; i < pairs.length; i++) {
    const p = pairs[i];
    const r = await refreshPair(p, token, queryOverride);
    if (r.ok) refreshed++; else errors++;
    const best = r.best ? `best $${r.best.total.toFixed(2)} (${r.best.title.slice(0, 48)})` : "no offers";
    console.log(`  ${p.slug} · ${p.format}: result_count=${r.resultCount}  ${best}${r.ok ? "" : `  ERROR: ${r.error}`}`);
    if (i < pairs.length - 1) await sleep(100);
  }
  console.log(`\nDone: refreshed ${refreshed} / errors ${errors} / ${pairs.length} pairs.`);
})();
