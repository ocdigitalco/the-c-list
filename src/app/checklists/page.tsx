import { listSets } from "@/lib/queries/listSets";
import { ChecklistSearch } from "./ChecklistSearch";

export const revalidate = 3600;

export default async function ChecklistsPage() {
  const { sets, allSports } = await listSets();

  return (
    <div
      className="h-full overflow-y-auto"
      style={{ background: "var(--cl-bg-page)" }}
    >
      <div
        className="page-container"
        style={{ paddingTop: 40, paddingBottom: 80 }}
      >
        {/* Breadcrumb */}
        <a
          href="/"
          style={{
            fontSize: 13,
            color: "var(--cl-text-tertiary)",
            textDecoration: "none",
            fontFamily: "var(--cl-font-display)",
          }}
        >
          &lsaquo; Home
        </a>

        {/* Title */}
        <h1 className="page-title" style={{ margin: "12px 0 0" }}>
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

        <ChecklistSearch sets={sets} allSports={allSports} />
      </div>
    </div>
  );
}
