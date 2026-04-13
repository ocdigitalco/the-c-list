export function slugify(text: string): string {
  return text
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[®©™]/g, "")
    .replace(/['']/g, "")
    .replace(/:/g, "")
    .replace(/\s+x\s+/g, " ")
    .replace(/[^a-z0-9-]+/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "");
}

export function generateUniqueSlug(
  text: string,
  existingSlugs: Set<string>
): string {
  const base = slugify(text);
  if (!existingSlugs.has(base)) return base;
  let i = 2;
  while (existingSlugs.has(`${base}-${i}`)) i++;
  return `${base}-${i}`;
}
