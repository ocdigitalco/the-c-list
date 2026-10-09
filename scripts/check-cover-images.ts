/**
 * Cover-image gate + gallery byte-signature check.
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
 * GALLERY CHECK: every file under public/sets/cards/<slug>/ is checked the same
 * way — .jpg/.jpeg must be JPEG, .png must be PNG, and any file whose bytes are
 * WebP or AVIF is reported (regardless of its name). This is REPORT-ONLY in
 * prebuild: it lists mismatches but never fails the build. Pass --fix to
 * re-encode each mismatched file to its extension's real format in place (via
 * sharp) and regenerate the gallery manifest. A genuine .webp file (webp bytes
 * under a .webp name) is reported but not rewritten — its extension already
 * matches, and the manifest supports webp.
 *
 * DB resolution mirrors src/lib/db.ts: Turso via @libsql/client when
 * TURSO_DATABASE_URL and TURSO_AUTH_TOKEN are set (the Vercel build env), else a
 * local better-sqlite3 file. If NEITHER is available (e.g. a CI checkout with no
 * DB), it prints "cover check skipped: no database" and exits 0 so a missing DB
 * never fails the build. Whenever a DB is reachable the gate runs strictly.
 *
 * Modes:
 *   • prebuild (no args): cover gate over VISIBLE sets. Sets with id >=
 *     NEW_SET_CUTOFF are every set built under the current pipeline, which
 *     specify a local cover — these must have a valid LOCAL cover (NULL/empty
 *     and remote URLs fail). Older sets (id < cutoff) are format-checked only: a
 *     broken local cover fails, but NULL/remote are skipped (773 of the catalog
 *     store NULL and 29 store a remote URL, so failing those would break every
 *     build). Then the gallery report (report-only) runs.
 *   • strict range (two ids): `npx tsx scripts/check-cover-images.ts 880 885`
 *     — every cover in range must be a valid LOCAL file (NULL/remote fail),
 *     regardless of id. Use this in the set-build flow. (No gallery scan.)
 *   • --fix: scan the gallery, re-encode every fixable byte/extension mismatch
 *     in place, regenerate the manifest, and exit 0. (No cover gate.)
 *
 * Exits non-zero only if a checked COVER fails (the gallery check never fails).
 */
import { readSync, openSync, closeSync, existsSync, readdirSync, statSync, writeFileSync } from "fs";
import { execFileSync } from "child_process";
import path from "path";

const argv = process.argv.slice(2);
const fix = argv.includes("--fix");
const nums = argv.filter((a) => /^\d+$/.test(a)).map((n) => parseInt(n, 10));
const [lo, hi] = nums;
const strict = nums.length === 2 && Number.isInteger(lo) && Number.isInteger(hi);
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

type Sig = "jpeg" | "png" | "webp" | "avif" | "unknown";
function signatureOf(file: string): Sig {
  const fd = openSync(file, "r");
  try {
    const b = Buffer.alloc(32);
    readSync(fd, b, 0, 32, 0);
    if (b[0] === 0xff && b[1] === 0xd8 && b[2] === 0xff) return "jpeg";
    if (b[0] === 0x89 && b[1] === 0x50 && b[2] === 0x4e && b[3] === 0x47) return "png";
    if (b.toString("ascii", 0, 4) === "RIFF" && b.toString("ascii", 8, 12) === "WEBP") return "webp";
    // AVIF/HEIF: ISO-BMFF "ftyp" box at offset 4 with an avif brand in the header.
    if (b.toString("ascii", 4, 8) === "ftyp") {
      const head = b.toString("ascii", 0, 32);
      if (head.includes("avif") || head.includes("avis")) return "avif";
    }
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

const CARDS_ROOT = path.join("public", "sets", "cards");
const GALLERY_EXT = new Set([".jpg", ".jpeg", ".png", ".webp", ".avif"]);

interface GalleryMiss { slug: string; file: string; abs: string; ext: string; sig: Sig; target: string | null }

/**
 * Scan every public/sets/cards/<slug>/ image and flag byte/extension mismatches:
 *   .jpg/.jpeg whose bytes aren't JPEG, .png whose bytes aren't PNG, and any file
 *   whose bytes are WebP or AVIF (under any name).
 * `target` is the extension's real format when it differs and is re-encodable
 * (jpeg/png); null when nothing to rewrite (a .webp named webp, or avif has no
 * supported extension here) so --fix can skip it.
 */
function scanGallery(): GalleryMiss[] {
  if (!existsSync(CARDS_ROOT)) return [];
  const out: GalleryMiss[] = [];
  const slugs = readdirSync(CARDS_ROOT).filter((d) => {
    try { return statSync(path.join(CARDS_ROOT, d)).isDirectory(); } catch { return false; }
  }).sort();
  for (const slug of slugs) {
    const dir = path.join(CARDS_ROOT, slug);
    for (const file of readdirSync(dir).sort()) {
      if (file.startsWith(".")) continue;
      const ext = path.extname(file).toLowerCase();
      if (!GALLERY_EXT.has(ext)) continue;
      const abs = path.join(dir, file);
      const sig = signatureOf(abs);
      const extFmt = EXT_SIG[ext]; // jpeg | png | webp | undefined(.avif)
      const mismatch =
        ((ext === ".jpg" || ext === ".jpeg") && sig !== "jpeg") ||
        (ext === ".png" && sig !== "png") ||
        sig === "webp" || sig === "avif";
      if (!mismatch) continue;
      // Re-encodable only when the extension maps to jpeg/png and the bytes differ.
      const target = (extFmt === "jpeg" || extFmt === "png") && sig !== extFmt ? extFmt : null;
      out.push({ slug, file, abs, ext, sig, target });
    }
  }
  return out;
}

/** Report-only: print each gallery mismatch grouped by set. Never fails the build. */
function reportGallery(misses: GalleryMiss[]): void {
  if (misses.length === 0) {
    console.log("gallery byte-signature check: 0 mismatches across public/sets/cards");
    return;
  }
  console.log(`gallery byte-signature check (report-only): ${misses.length} mismatch(es) — run \`tsx scripts/check-cover-images.ts --fix\` to re-encode:`);
  let cur = "";
  for (const m of misses) {
    if (m.slug !== cur) { console.log(`  ${m.slug}:`); cur = m.slug; }
    const note = m.target ? `${m.ext} but bytes are ${m.sig} → re-encode to ${m.target}` : `bytes are ${m.sig} (extension ${m.ext} already matches; not auto-fixed)`;
    console.log(`    ${m.file} — ${note}`);
  }
}

/** --fix: re-encode every re-encodable mismatch in place via sharp, then regenerate the manifest. */
async function fixGallery(misses: GalleryMiss[]): Promise<void> {
  const fixable = misses.filter((m) => m.target);
  const skipped = misses.filter((m) => !m.target);
  const sharp = (await import("sharp")).default;
  const byConv = new Map<string, number>();
  let fixed = 0;
  for (const m of fixable) {
    const img = sharp(m.abs);
    const buf = m.target === "jpeg"
      ? await img.flatten({ background: "#ffffff" }).jpeg({ quality: 90 }).toBuffer()
      : await img.png().toBuffer();
    writeFileSync(m.abs, buf);
    const key = `${m.sig}→${m.target}`;
    byConv.set(key, (byConv.get(key) ?? 0) + 1);
    fixed++;
    console.log(`  fixed ${m.slug}/${m.file} (${m.sig} → ${m.target})`);
  }
  console.log(`\ngallery --fix: re-encoded ${fixed} file(s)` + (fixable.length ? ` [${[...byConv].map(([k, v]) => `${k}: ${v}`).join(", ")}]` : ""));
  if (skipped.length) {
    console.log(`skipped ${skipped.length} file(s) whose extension already matches their (webp/avif) bytes:`);
    for (const m of skipped) console.log(`  ${m.slug}/${m.file} (${m.sig})`);
  }
  console.log("\nregenerating gallery manifest...");
  execFileSync("npx", ["tsx", "scripts/generate-card-gallery-manifest.ts"], { stdio: "inherit" });
}

async function main() {
  if (fix) {
    const misses = scanGallery();
    console.log(`gallery byte-signature --fix: ${misses.length} mismatch(es) found`);
    await fixGallery(misses);
    process.exit(0);
  }

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

  // Gallery byte-signature check: report-only in prebuild (never fails the build).
  if (!strict) reportGallery(scanGallery());

  process.exit(failures ? 1 : 0);
}

main().catch((e) => { console.error("cover-image gate error:", e); process.exit(1); });
