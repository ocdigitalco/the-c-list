/**
 * Cover-image gate.
 *
 * For a local cover (sample_image_url begins with "/"), asserts the file exists
 * under public/ and its magic-byte signature matches its extension
 * (.jpg/.jpeg → JPEG, .png → PNG, .webp → WebP). This is what caught set 885
 * shipping a WebP saved as .jpg.
 *
 * JPEG covers are additionally checked for color space: a 4-component (CMYK/YCCK)
 * JPEG renders with wrong/inverted colors in browsers, so it fails the gate with
 * a clear message. This caught set 890 shipping a CMYK cover from Photoshop.
 *
 * DB resolution mirrors src/lib/db.ts: Turso via @libsql/client when
 * TURSO_DATABASE_URL and TURSO_AUTH_TOKEN are set (the Vercel build env), else a
 * local better-sqlite3 file. If NEITHER is available (e.g. a CI checkout with no
 * DB), it prints "cover check skipped: no database" and exits 0 so a missing DB
 * never fails the build. Whenever a DB is reachable the gate runs strictly.
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
import { readSync, openSync, closeSync, existsSync } from "fs";
import path from "path";

const [lo, hi] = process.argv.slice(2).map((n) => parseInt(n, 10));
const strict = Number.isInteger(lo) && Number.isInteger(hi);
// Sets at/after this id were all built under the current pipeline with a
// specified local cover, so prebuild requires a valid local cover for them.
const NEW_SET_CUTOFF = 880;
const LOCAL_DB = "the-c-list.db";

interface Row { id: number; slug: string | null; sample_image_url: string | null }

/** Load the sets to check, from Turso or local SQLite — same precedence as the app. */
async function loadRows(): Promise<Row[] | null> {
  const sql = strict
    ? "SELECT id, slug, sample_image_url FROM sets WHERE id BETWEEN ? AND ? ORDER BY id"
    : "SELECT id, slug, sample_image_url FROM sets WHERE is_visible = 1 ORDER BY id";
  const args: (number)[] = strict ? [lo, hi] : [];

  if (process.env.TURSO_DATABASE_URL && process.env.TURSO_AUTH_TOKEN) {
    const { createClient } = await import("@libsql/client");
    const db = createClient({ url: process.env.TURSO_DATABASE_URL, authToken: process.env.TURSO_AUTH_TOKEN });
    try {
      const res = await db.execute({ sql, args });
      return res.rows as unknown as Row[];
    } finally { db.close(); }
  }
  if (existsSync(LOCAL_DB)) {
    const Database = (await import("better-sqlite3")).default;
    const db = new Database(LOCAL_DB, { readonly: true });
    try {
      return db.prepare(sql).all(...args) as Row[];
    } finally { db.close(); }
  }
  return null; // no database reachable
}

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

/**
 * Number of color components in a JPEG (1 = grayscale, 3 = YCbCr/RGB, 4 = CMYK/YCCK),
 * read from the SOFn frame header. Returns null if no SOF marker is found.
 */
function jpegComponents(file: string): number | null {
  const fd = openSync(file, "r");
  try {
    const b = Buffer.alloc(256 * 1024);
    const n = readSync(fd, b, 0, b.length, 0);
    let pos = 2; // skip SOI (FFD8)
    while (pos + 9 < n) {
      if (b[pos] !== 0xff) { pos++; continue; }
      let marker = b[pos + 1];
      // skip fill bytes (0xFF padding)
      while (marker === 0xff && pos + 1 < n) { pos++; marker = b[pos + 1]; }
      // SOF markers carry the component count; exclude DHT(C4), JPG(C8), DAC(CC)
      const isSOF = marker >= 0xc0 && marker <= 0xcf && marker !== 0xc4 && marker !== 0xc8 && marker !== 0xcc;
      if (isSOF) return b[pos + 9]; // marker(2)+len(2)+precision(1)+height(2)+width(2) → components
      if (marker === 0xda || marker === 0xd9) return null; // SOS/EOI: no SOF seen
      // standalone markers (RSTn D0-D7, TEM 01) have no length payload
      if ((marker >= 0xd0 && marker <= 0xd7) || marker === 0x01) { pos += 2; continue; }
      const len = (b[pos + 2] << 8) | b[pos + 3];
      if (len < 2) return null;
      pos += 2 + len;
    }
    return null;
  } finally { closeSync(fd); }
}

async function main() {
  const rows = await loadRows();
  if (rows === null) {
    console.log("cover check skipped: no database");
    process.exit(0);
  }

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
    if (sig === "jpeg") {
      const comps = jpegComponents(file);
      if (comps === 4) { console.log(`FAIL  ${r.id} ${r.slug} — CMYK JPEG cover (4 components); re-encode to sRGB RGB: ${file}`); failures++; continue; }
    }
  }
  console.log(
    `cover-image gate (${strict ? `strict ${lo}-${hi}` : `prebuild, require-local id>=${NEW_SET_CUTOFF}`}): ${checked} local covers checked, ${failures} failed` +
    (strict ? "" : `; skipped ${skippedNull} NULL + ${skippedRemote} remote (all id<${NEW_SET_CUTOFF})`)
  );
  process.exit(failures ? 1 : 0);
}

main().catch((e) => { console.error("cover-image gate error:", e); process.exit(1); });
