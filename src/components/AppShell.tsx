"use client";

import { usePathname } from "next/navigation";
import { Footer } from "@/components/Footer";

/**
 * Owns the <main> region and the site-wide footer.
 *
 * Two route classes need different scroll models:
 *  - Split-pane app shells (set detail, athlete, team — /sets/<id>/…): a
 *    fixed-viewport main with an internal sticky-sidebar + scrolling content
 *    pane. These render their OWN <Footer/> as the last child of that pane, so
 *    the layout must NOT add one here (guards against a double footer).
 *  - Every other route: a single shared scroller with <Footer/> appended below
 *    {children}, so the footer scrolls into view at the end of the content.
 */
function isSplitPane(pathname: string | null): boolean {
  // /sets → standard index page (gets the layout footer).
  // /sets/<id>, /sets/<id>/athlete/…, /sets/<id>/team/… → split-pane shells.
  return !!pathname && /^\/sets\/[^/]+(\/|$)/.test(pathname);
}

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  if (isSplitPane(pathname)) {
    return <main className="flex-1 overflow-hidden">{children}</main>;
  }

  return (
    <main
      className="flex-1 overflow-y-auto"
      style={{ background: "var(--brand-page)" }}
    >
      <div className="min-h-full flex flex-col">
        <div className="flex-1 flex flex-col">{children}</div>
        <Footer />
      </div>
    </main>
  );
}
