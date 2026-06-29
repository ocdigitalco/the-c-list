import { promises as fs } from "fs";
import path from "path";

export interface CardGalleryImage {
  /** Public-relative src, e.g. /sets/cards/2026-topps-disney-neon/2026-topps-disney-neon-1.jpg */
  src: string;
  /** The trailing integer parsed from the filename (used for alt text + sort). */
  n: number;
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
  const matched: CardGalleryImage[] = [];
  const unexpected: string[] = [];

  for (const file of entries) {
    if (file.startsWith(".")) continue; // skip .gitkeep and other dotfiles
    const m = file.match(pattern);
    if (m) {
      matched.push({ src: `/sets/cards/${slug}/${file}`, n: parseInt(m[1], 10) });
    } else {
      unexpected.push(file);
    }
  }

  if (unexpected.length > 0) {
    console.warn(
      `[cardGallery] ${slug}: ignoring ${unexpected.length} file(s) not matching {slug}-{n}.{ext}: ${unexpected.join(", ")}`
    );
  }

  matched.sort((a, b) => a.n - b.n);
  return matched;
}
