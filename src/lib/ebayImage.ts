/**
 * eBay image CDN URLs encode the requested size in a trailing `s-l<n>` token
 * (e.g. .../s-l140.jpg, .../s-l225.webp). The cached offer feed gives us small
 * thumbnails; rewrite the token at render time to request a larger variant.
 *
 * Only touches i.ebayimg.com URLs that carry an s-l<n> token; anything else is
 * returned unchanged. Do NOT bake this into the stored JSON — apply per <img>.
 */
export function ebayImageAt(url: string, size: number): string {
  if (!url || !url.includes("i.ebayimg.com")) return url;
  // Replace the size token immediately before the file extension (s-l140.jpg → s-l960.jpg).
  return url.replace(/s-l\d+(?=\.\w)/, `s-l${size}`);
}
