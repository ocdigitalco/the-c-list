import { listChecklistPage } from "@/lib/queries/listChecklistPage";
import { ChecklistSearch } from "./checklists/ChecklistSearch";

export const revalidate = 86400; // 24h; / and /checklists also revalidated on demand by the migration

export default async function HomePage() {
  const { sets, recentlyAdded, allSports } = await listChecklistPage();

  return (
    <div
      className="flex-1"
      style={{ background: "var(--cl-bg-page)" }}
    >
      <div
        className="mx-auto cl-container"
        style={{ maxWidth: 1440, padding: "40px 56px 80px" }}
      >
        {/* Title */}
        <h1 className="page-title">
          Checklists
        </h1>

        {/* Subtitle */}
        <p
          style={{
            fontSize: 14,
            color: "var(--cl-text-tertiary)",
            margin: "6px 0 0",
          }}
        >
          Browse all sports card sets in the app
        </p>

        <ChecklistSearch sets={sets} recentlyAdded={recentlyAdded} allSports={allSports} />
      </div>
    </div>
  );
}
