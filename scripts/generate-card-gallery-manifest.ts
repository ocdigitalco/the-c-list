/**
 * Build-time card-gallery manifest generator.
 *
 * Scans public/sets/cards/{slug}/ once and emits a static JSON manifest so the
 * runtime (src/lib/cardGallery.ts) never touches the filesystem, sharp, or
 * process.cwd(). This stops @vercel/nft from tracing the entire
 * public/sets/cards/** image tree into the sets/[id] serverless function
 * (which pushed that function past Vercel's 250MB limit).
 *
 * Wired into `npm run build` (and `npm run dev`) via the "prebuild"/"predev"
 * lifecycle scripts so the manifest can never go stale.
 *
 * The dedup + sort + dimension logic MUST stay byte-for-byte equivalent to the
 * old runtime implementation so gallery output is identical.
 */
import { promises as fs } from "fs";
import path from "path";

const CARDS_ROOT = path.join(process.cwd(), "public", "sets", "cards");
const OUT_PATH = path.join(process.cwd(), "src", "generated", "cardGalleryManifest.json");

// Fallback aspect when dimensions can't be read: 5:7 vertical card.
const FALLBACK_W = 500;
const FALLBACK_H = 700;

const IMAGE_EXT = "jpe?g|png|webp";
// Prefer the more efficient encoding when the same {slug}-{n} exists in multiple
// extensions: webp > png > jpg/jpeg.
const EXT_PREFERENCE: Record<string, number> = { webp: 0, png: 1, jpg: 2, jpeg: 2 };

interface ManifestImage {
  file: string;
  width: number;
  height: number;
}

function escapeRegExp(s: string): string {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

async function readDimensions(absPath: string): Promise<{ width: number; height: number }> {
  try {
    const sharp = (await import("sharp")).default;
    const meta = await sharp(absPath).metadata();
    if (meta.width && meta.height) return { width: meta.width, height: meta.height };
  } catch {
    // sharp unavailable / unreadable → fall through to the 5:7 default
  }
  return { width: FALLBACK_W, height: FALLBACK_H };
}

async function buildSlug(slug: string): Promise<ManifestImage[]> {
  const dir = path.join(CARDS_ROOT, slug);
  const entries = await fs.readdir(dir);

  const pattern = new RegExp(`^${escapeRegExp(slug)}-(\\d+)\\.(${IMAGE_EXT})$`, "i");
  const matched: { file: string; n: number; ext: string }[] = [];
  const unexpected: string[] = [];

  for (const file of entries) {
    if (file.startsWith(".")) continue; // skip .gitkeep and other dotfiles
    const m = file.match(pattern);
    if (m) matched.push({ file, n: parseInt(m[1], 10), ext: m[2].toLowerCase() });
    else unexpected.push(file);
  }

  // Dedup by parsed integer, preferring webp > png > jpg.
  const byNumber = new Map<number, { file: string; n: number; ext: string }>();
  for (const f of matched) {
    const cur = byNumber.get(f.n);
    if (!cur || (EXT_PREFERENCE[f.ext] ?? 99) < (EXT_PREFERENCE[cur.ext] ?? 99)) {
      byNumber.set(f.n, f);
    }
  }
  const deduped = [...byNumber.values()].sort((a, b) => a.n - b.n);

  if (unexpected.length > 0) {
    console.warn(
      `[gallery-manifest] ${slug}: ignoring ${unexpected.length} file(s) not matching {slug}-{n}.{ext}: ${unexpected.join(", ")}`
    );
  }

  const images: ManifestImage[] = [];
  for (const { file } of deduped) {
    const { width, height } = await readDimensions(path.join(dir, file));
    images.push({ file, width, height });
  }
  return images;
}

async function main() {
  const manifest: Record<string, ManifestImage[]> = {};

  let slugs: string[] = [];
  try {
    const entries = await fs.readdir(CARDS_ROOT, { withFileTypes: true });
    slugs = entries.filter((e) => e.isDirectory()).map((e) => e.name).sort();
  } catch {
    // No cards root at all → empty manifest (every gallery renders nothing).
    console.warn(`[gallery-manifest] ${CARDS_ROOT} not found; writing empty manifest`);
  }

  for (const slug of slugs) {
    const images = await buildSlug(slug);
    if (images.length > 0) manifest[slug] = images;
  }

  await fs.mkdir(path.dirname(OUT_PATH), { recursive: true });
  await fs.writeFile(OUT_PATH, JSON.stringify(manifest, null, 2) + "\n", "utf-8");

  const totalImages = Object.values(manifest).reduce((a, v) => a + v.length, 0);
  console.log(
    `[gallery-manifest] wrote ${Object.keys(manifest).length} sets / ${totalImages} images → ${path.relative(process.cwd(), OUT_PATH)}`
  );
}

main().catch((err) => {
  console.error("[gallery-manifest] FAILED:", err);
  process.exit(1);
});
