"use client";

/** Footer link that reopens the cookie banner (Manage view) with current choices. */
export function CookieSettingsLink() {
  return (
    <button
      type="button"
      onClick={() => window.dispatchEvent(new Event("c2:open-consent"))}
      className="text-sm text-[var(--brand-slate)] hover:text-[var(--brand-ink)] transition-colors"
      style={{ background: "none", border: "none", padding: 0, cursor: "pointer", font: "inherit", textAlign: "left" }}
    >
      Cookie settings
    </button>
  );
}
