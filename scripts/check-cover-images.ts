/**
 * Cover-image gate.
 *
 * For a local cover (sample_image_url begins with "/"), asserts the file exists
 * under public/ and its magic-byte signature matches its extension
 * (.jpg/.jpeg → JPEG, .png → PNG, .webp → WebP). This is what caught set 885
 * shipping a WebP saved as .jpg.
 *
 * Two modes:
 *   • prebuild (no args): over VISIBLE sets. Sets with id >= NEW_SET_CUTOFF are
 *     every set built under the current pipeline, which specify a local cover —
 *     these must have a valid LOCAL cover (NULL/empty and remote URLs fail).
 *     Older sets (id < cutoff) are format-checked only: a broken local cover
 *     fails, but NULL/remote are skipped (773 of the catalog store NULL and 29
 *     store a remote URL, so failing those would break every build).
 *   • strict range (two ids): `npx tsx scripts/check-cover-images.ts 880 885`
 *     — every cover in range must be a valid LOCAL file (NULL/remote fail),
 *     regardless of id. Use this in the set-build flow.
 *
 * Exits non-zero if any checked set fails.
 */
import Database from "better-sqlite3";
import { readSync, openSync, closeSync, existsSync } from "fs";
import path from "path";

const db = new Database("the-c-list.db", { readonly: true });
const [lo, hi] = process.argv.slice(2).map((n) => parseInt(n, 10));
const strict = Number.isInteger(lo) && Number.isInteger(hi);
// Sets at/after this id were all built under the current pipeline with a
// specified local cover, so prebuild requires a valid local cover for them.
const NEW_SET_CUTOFF = 880;

const rows = (strict
  ? db.prepare("SELECT id, slug, sample_image_url FROM sets WHERE id BETWEEN ? AND ? ORDER BY id").all(lo, hi)
  : db.prepare("SELECT id, slug, sample_image_url FROM sets WHERE is_visible = 1 ORDER BY id").all()
) as { id: number; slug: string | null; sample_image_url: string | null }[];

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

let failures = 0, checked = 0, skippedNull = 0, skippedRemote = 0;
for (const r of rows) {
  // Require a local cover in strict mode, or in prebuild for new-pipeline sets.
  const requireLocal = strict || r.id >= NEW_SET_CUTOFF;
  const url = (r.sample_image_url ?? "").trim();
  if (!url) {
    if (requireLocal) { console.log(`FAIL  ${r.id} ${r.slug} — sample_image_url is NULL/empty`); failures++; }
    else skippedNull++;
    continue;
  }
  if (/^https?:\/\//i.test(url)) {
    if (requireLocal) { console.log(`FAIL  ${r.id} ${r.slug} — remote cover URL (expected a local /sets file): ${url}`); failures++; }
    else skippedRemote++;
    continue;
  }
  checked++;
  const file = path.join("public", url.replace(/^\//, ""));
  if (!existsSync(file)) { console.log(`FAIL  ${r.id} ${r.slug} — file not found: ${file}`); failures++; continue; }
  const ext = path.extname(url).toLowerCase();
  const want = EXT_SIG[ext];
  if (!want) { console.log(`FAIL  ${r.id} ${r.slug} — unsupported extension ${ext}`); failures++; continue; }
  const sig = signatureOf(file);
  if (sig !== want) { console.log(`FAIL  ${r.id} ${r.slug} — ${ext} but bytes are ${sig}`); failures++; continue; }
}
console.log(
  `cover-image gate (${strict ? `strict ${lo}-${hi}` : `prebuild, require-local id>=${NEW_SET_CUTOFF}`}): ${checked} local covers checked, ${failures} failed` +
  (strict ? "" : `; skipped ${skippedNull} NULL + ${skippedRemote} remote (all id<${NEW_SET_CUTOFF})`)
);
db.close();
process.exit(failures ? 1 : 0);
