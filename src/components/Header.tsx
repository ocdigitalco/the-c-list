"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { Wordmark } from "@/components/Wordmark";
const navLinks = [
  { href: "/checklists", label: "Checklists" },
  { href: "/sets", label: "Sets" },
  { href: "/overview", label: "Overview" },
  { href: "/searches", label: "Searches" },
  { href: "/resources", label: "Resources" },
  { href: "/articles", label: "Articles" },
  { href: "/updates", label: "Updates" },
];

export function Header() {
  const pathname = usePathname();
  const [menuOpen, setMenuOpen] = useState(false);

  const isActive = (href: string) => {
    if (pathname === href) return true;
    // For /sets, don't match /sets/123 (set detail pages)
    if (href === "/sets") return false;
    return pathname.startsWith(href + "/");
  };

  return (
    <header className="shrink-0 border-b" style={{ background: "var(--brand-head)", borderColor: "var(--brand-line)" }}>
      <div className="flex items-center justify-between h-14 px-5 min-[640px]:px-8">
        {/* Wordmark */}
        <Link href="/" className="flex items-center" style={{ textDecoration: "none" }} aria-label="Checklist²">
          <span className="hidden min-[640px]:inline-flex">
            <Wordmark size={45} />
          </span>
          <span className="inline-flex min-[640px]:hidden">
            <Wordmark size={36} />
          </span>
        </Link>

        {/* Desktop nav */}
        <nav className="hidden md:flex items-center gap-1">
          {navLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="hdr-nav"
              aria-current={isActive(link.href) ? "page" : undefined}
            >
              {link.label}
            </Link>
          ))}
        </nav>

        {/* Hamburger (mobile only; on desktop it is display:none so the nav sits flush right) */}
        <button
          className="md:hidden p-1.5 transition-colors rounded-md"
          style={{ color: "var(--brand-ink-soft)" }}
          onClick={() => setMenuOpen((o) => !o)}
          aria-label="Toggle menu"
        >
          {menuOpen ? (
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          ) : (
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          )}
        </button>
      </div>

      {/* Mobile menu */}
      {menuOpen && (
        <nav className="md:hidden px-4 py-2 flex flex-col gap-0.5" style={{ borderTop: "1px solid var(--brand-line)" }}>
          {navLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              onClick={() => setMenuOpen(false)}
              className="hdr-nav"
              aria-current={isActive(link.href) ? "page" : undefined}
            >
              {link.label}
            </Link>
          ))}
        </nav>
      )}
    </header>
  );
}
