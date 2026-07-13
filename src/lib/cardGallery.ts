import { promises as fs } from "fs";
import path from "path";

export interface CardGalleryImage {
  /** Public-relative src, e.g. /sets/cards/2026-topps-disney-neon/2026-topps-disney-neon-1.jpg */
  src: string;
  /** The trailing integer parsed from the filename (used for alt text + sort). */
  n: number;
  /** Intrinsic pixel width — drives the gallery card's aspect ratio (no layout shift). */
  width: number;
  /** Intrinsic pixel height. */
  height: number;
}

// Fallback aspect when dimensions can't be read: 5:7 (matches the classic
// vertical card), so a read failure degrades to today's exact behaviour.
const FALLBACK_W = 500;
const FALLBACK_H = 700;

/** Read an image's intrinsic dimensions via sharp; fall back to 5:7 on any error. */
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

const IMAGE_EXT = "(?:jpe?g|png|webp)";

function escapeRegExp(s: string): string {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

/**
 * Read card-gallery images for a set from public/sets/cards/{slug}/.
 *
 * Convention: files are named {slug}-{n}.{ext} where {n} is a sequential
 * integer (1-based). Images are sorted ascending by the parsed integer, NOT
 * lexicographically (so ...-10 sorts after ...-9, not after ...-1). Files that
 * don't match the pattern (including .gitkeep / dotfiles) are ignored; any
 * unexpected names are logged server-side rather than crashing the read.
 *
 * Returns [] when the folder is missing or empty, so the ~800 folderless sets
 * are unaffected and the gallery section simply does not render.
 */
export async function getCardGalleryImages(
  slug: string | null | undefined
): Promise<CardGalleryImage[]> {
  if (!slug) return [];

  const dir = path.join(process.cwd(), "public", "sets", "cards", slug);

  let entries: string[];
  try {
    entries = await fs.readdir(dir);
  } catch {
    // Folder missing (the common case for most sets) → render nothing.
    return [];
  }

  const pattern = new RegExp(`^${escapeRegExp(slug)}-(\\d+)\\.${IMAGE_EXT}$`, "i");
  const files: { file: string; n: number }[] = [];
  const unexpected: string[] = [];

  for (const file of entries) {
    if (file.startsWith(".")) continue; // skip .gitkeep and other dotfiles
    const m = file.match(pattern);
    if (m) {
      files.push({ file, n: parseInt(m[1], 10) });
    } else {
      unexpected.push(file);
    }
  }

  if (unexpected.length > 0) {
    console.warn(
      `[cardGallery] ${slug}: ignoring ${unexpected.length} file(s) not matching {slug}-{n}.{ext}: ${unexpected.join(", ")}`
    );
  }

  // Read intrinsic dimensions so each card can reserve its natural width at a
  // fixed height with no layout shift (horizontal cards render wider).
  const matched: CardGalleryImage[] = await Promise.all(
    files.map(async ({ file, n }) => {
      const { width, height } = await readDimensions(path.join(dir, file));
      return { src: `/sets/cards/${slug}/${file}`, n, width, height };
    })
  );

  matched.sort((a, b) => a.n - b.n);
  return matched;
}
