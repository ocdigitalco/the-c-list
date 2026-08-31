export function BreakCalcWarning({
  missingBoxConfig,
  missingPackOdds,
}: {
  missingBoxConfig: boolean;
  missingPackOdds: boolean;
}) {
  let message: string;
  if (missingBoxConfig && missingPackOdds) {
    message =
      "Box configuration and pack odds data have not been confirmed for this set yet. Once verified this calculator will be available.";
  } else if (missingBoxConfig) {
    message =
      "Box configuration data (packs per box, boxes per case) has not been confirmed for this set. Once verified this calculator will be available.";
  } else {
    message =
      "Official pack odds have not been added for this set yet. Once available this calculator will be enabled.";
  }

  return (
    <div className="rounded-xl border border-[var(--brand-accent-deep)] bg-[var(--brand-accent-deep)] px-5 py-4">
      <div className="flex items-start gap-3">
        <svg
          className="shrink-0 w-4 h-4 text-[var(--brand-accent-deep)] mt-0.5"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth={2}
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"
          />
        </svg>
        <div>
          <p className="text-xs font-semibold text-[var(--brand-accent-deep)] mb-1">
            Break Hit Calculator Unavailable
          </p>
          <p className="text-xs text-[var(--brand-accent-deep)] leading-relaxed">{message}</p>
        </div>
      </div>
    </div>
  );
}
