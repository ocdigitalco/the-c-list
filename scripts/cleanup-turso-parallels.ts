/**
 * Delete parallels for set 44 from Turso.
 * Usage: npx tsx scripts/cleanup-turso-parallels.ts
 */
import dotenv from "dotenv";
dotenv.config({ path: ".env.local" });
import { createClient } from "@libsql/client";

const url = process.env.TURSO_DATABASE_URL!;
const authToken = process.env.TURSO_AUTH_TOKEN!;
if (!url || !authToken) {
  console.error("Missing TURSO_DATABASE_URL or TURSO_AUTH_TOKEN");
  process.exit(1);
}

const turso = createClient({ url, authToken });

async function main() {
  // Count before
  const before = await turso.execute(
    "SELECT COUNT(*) AS n FROM parallels WHERE insert_set_id IN (SELECT id FROM insert_sets WHERE set_id = 44)"
  );
  console.log(`Parallels for set 44 before: ${before.rows[0].n}`);

  // Delete
  const result = await turso.execute(
    "DELETE FROM parallels WHERE insert_set_id IN (SELECT id FROM insert_sets WHERE set_id = 44)"
  );
  console.log(`Deleted ${result.rowsAffected} rows`);

  // Count after
  const after = await turso.execute(
    "SELECT COUNT(*) AS n FROM parallels WHERE insert_set_id IN (SELECT id FROM insert_sets WHERE set_id = 44)"
  );
  console.log(`Parallels for set 44 after: ${after.rows[0].n}`);
}

main().catch((err) => {
  console.error("Failed:", err);
  process.exit(1);
});
