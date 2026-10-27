/**
 * Post-seed chain — run after seeding a NEW set, BEFORE migrate-to-turso.ts.
 * Replaces the bare `build-athletes` step so a new set's players get both an
 * athlete_id and a headshot:
 *
 *   1. build-athletes        → assign athlete_id to the new set's players
 *   2. backfill-headshots    → sibling-copy ids from the same athletes' older
 *      --set <slug>            rows, external match the set's remaining NULLs,
 *                              normalize UFC urls
 *   3. build-athletes        → recompute athletes.headshot_url now that the
 *                              set's players carry ids
 *
 * Usage:
 *   npx tsx scripts/post-seed.ts --set <slug>
 *   npx tsx scripts/post-seed.ts --set <slug> --no-external   # sibling-copy only
 */
import { execFileSync } from "child_process";

const args = process.argv.slice(2);
const slug = args.includes("--set") ? args[args.indexOf("--set") + 1] : null;
const noExternal = args.includes("--no-external");
if (!slug) {
  console.error("Usage: npx tsx scripts/post-seed.ts --set <slug> [--no-external]");
  process.exit(1);
}

function run(cmd: string, a: string[]) {
  console.log(`\n▶ ${cmd} ${a.join(" ")}`);
  execFileSync(cmd, a, { stdio: "inherit" });
}

run("npx", ["tsx", "scripts/build-athletes.ts"]);
run("npx", ["tsx", "scripts/backfill-headshots.ts", "--set", slug, ...(noExternal ? ["--no-external"] : [])]);
run("npx", ["tsx", "scripts/build-athletes.ts"]);
console.log("\n✓ post-seed complete. Review scratchpad/headshot-fuzzy.csv, then run migrate-to-turso.ts.");
