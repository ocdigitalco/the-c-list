/**
 * Cover-image gate for the set-build flow.
 *
 * For each set in range, asserts:
 *   1. sample_image_url is non-NULL and non-empty;
 *   2. the file it points at exists under public/;
 *   3. the file's magic-byte signature matches its extension
 *      (.jpg/.jpeg → JPEG, .png → PNG, .webp → WebP).
 *
 * Usage:
 *   npx tsx scripts/check-cover-images.ts            # all visible sets
 *   npx tsx scripts/check-cover-images.ts 880 885    # inclusive id range
 *
 * Exits non-zero if any checked set fails, so it can gate a set build.
 */
import Database from "better-sqlite3";
import { readSync, openSync, closeSync, existsSync } from "fs";
import path from "path";

const db = new Database("the-c-list.db", { readonly: true });

const [lo, hi] = process.argv.slice(2).map((n) => parseInt(n, 10));
const rows = (lo && hi
  ? db.prepare("SELECT id, slug, sample_image_url FROM sets WHERE id BETWEEN ? AND ? ORDER BY id").all(lo, hi)
  : db.prepare("SELECT id, slug, sample_image_url FROM sets WHERE is_visible = 1 ORDER BY id").all()
) as { id: number; slug: string | null; sample_image_url: string | null }[];

/** Read the leading bytes and classify the image signature. */
function signatureOf(file: string): "jpeg" | "png" | "webp" | "unknown" {
  const fd = openSync(file, "r");
  try {
    const b = Buffer.alloc(16);
    readSync(fd, b, 0, 16, 0);
    if (b[0] === 0xff && b[1] === 0xd8 && b[2] === 0xff) return "jpeg";
    if (b[0] === 0x89 && b[1] === 0x50 && b[2] === 0x4e && b[3] === 0x47) return "png";
    if (b.toString("ascii", 0, 4) === "RIFF" && b.toString("ascii", 8, 12) === "WEBP") return "webp";
    return "unknown";
  } finally { closeSync(fd); }
}

const EXT_SIG: Record<string, string> = { ".jpg": "jpeg", ".jpeg": "jpeg", ".png": "png", ".webp": "webp" };

let failures = 0;
for (const r of rows) {
  const url = (r.sample_image_url ?? "").trim();
  if (!url) { console.log(`FAIL  ${r.id} ${r.slug} — sample_image_url is NULL/empty`); failures++; continue; }
  const file = path.join("public", url.replace(/^\//, ""));
  if (!existsSync(file)) { console.log(`FAIL  ${r.id} ${r.slug} — file not found: ${file}`); failures++; continue; }
  const ext = path.extname(url).toLowerCase();
  const want = EXT_SIG[ext];
  const sig = signatureOf(file);
  if (!want) { console.log(`FAIL  ${r.id} ${r.slug} — unsupported extension ${ext}`); failures++; continue; }
  if (sig !== want) { console.log(`FAIL  ${r.id} ${r.slug} — ${ext} but bytes are ${sig}`); failures++; continue; }
  console.log(`ok    ${r.id} ${r.slug} — ${ext} / ${sig}`);
}
console.log(`\n${rows.length} checked, ${failures} failed`);
db.close();
process.exit(failures ? 1 : 0);
