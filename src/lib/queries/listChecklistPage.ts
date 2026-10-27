import { listSets, type SetListItem } from "./listSets";

/**
 * Data for the Checklists page (`/` and `/checklists`). Wraps listSets() and:
 *  - hides "ghost" sets with no cover art (sample_image_url empty/null) — these
 *    are empty shells with no checklist data; they never render on this page.
 *    The filter is scoped to this page only: /sets/[id] and /break-sheet-builder
 *    still see the full list from listSets().
 *  - derives `recentlyAdded`: the sets added in the last 14 days (listSets'
 *    `featured` flag), newest-added first, for the Recently Added row.
 *
 * `allSports` is passed through unchanged (the chip strip still offers every
 * sport, even those whose only sets are ghosts — harmless, the grid just shows
 * nothing for them, same as a sport with zero matches today).
 */
export async function listChecklistPage(): Promise<{
  sets: SetListItem[];
  recentlyAdded: SetListItem[];
  allSports: string[];
}> {
  const { sets, allSports } = await listSets();

  const hasCover = (s: SetListItem) => !!s.sampleImageUrl && s.sampleImageUrl.trim() !== "";
  const visible = sets.filter(hasCover);

  const recentlyAdded = visible
    .filter((s) => s.featured && s.createdAt)
    .sort((a, b) => {
      const ta = new Date(a.createdAt as string).getTime();
      const tb = new Date(b.createdAt as string).getTime();
      return tb - ta || b.id - a.id; // newest-added first, stable by id
    });

  return { sets: visible, recentlyAdded, allSports };
}
