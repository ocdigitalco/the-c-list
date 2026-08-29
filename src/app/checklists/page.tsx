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
        className="mx-auto cl-container"
        style={{ maxWidth: 1440, padding: "40px 56px 80px" }}
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
        <h1
          className="cl-title"
          style={{
            fontFamily: "var(--brand-font-head)",
            fontSize: 48,
            fontWeight: 600,
            letterSpacing: "-1.2px",
            color: "var(--cl-text-primary)",
            margin: "12px 0 0",
            lineHeight: 1.1,
          }}
        >
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
