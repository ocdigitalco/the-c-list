"use client";

import { useEffect, useLayoutEffect } from "react";
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

  // On client navigation the root layout (and its scroll containers) persist, so
  // main/.v2-root can arrive with a residual scrollTop that slides content up
  // under the sticky header. Reset every scroll container before paint on each
  // pathname change — unless the URL carries a hash, in which case we leave the
  // browser's anchor jump alone. Runs in useLayoutEffect so it beats the paint.
  useLayoutEffect(() => {
    if (typeof window === "undefined") return;
    if (window.location.hash) return;
    window.scrollTo(0, 0);
    document.querySelectorAll<HTMLElement>("main, .v2-root").forEach((el) => {
      el.scrollTop = 0;
    });
  }, [pathname]);

  // The document itself must never scroll — the app scrolls inside main/.v2-root.
  // A hash/anchor jump into a nested scroller (e.g. #sealed-value_blaster) makes
  // the browser scroll .v2-root correctly AND also nudge the window, which slides
  // everything (incl. the sticky header) up. Pin the window back to 0; the nested
  // scroller keeps its own (scroll-padding-aware) position, so the target lands
  // just below the header.
  useEffect(() => {
    const pin = () => { if (window.scrollY !== 0 || window.scrollX !== 0) window.scrollTo(0, 0); };
    window.addEventListener("scroll", pin, { passive: true });
    return () => window.removeEventListener("scroll", pin);
  }, []);

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
