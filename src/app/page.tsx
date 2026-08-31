import { listSets } from "@/lib/queries/listSets";
import { ChecklistSearch } from "./checklists/ChecklistSearch";

export const revalidate = 3600;

export default async function HomePage() {
  const { sets, allSports } = await listSets();

  return (
    <div
      className="h-full overflow-y-auto"
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

        <ChecklistSearch sets={sets} allSports={allSports} />
      </div>
    </div>
  );
}
