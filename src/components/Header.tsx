"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { ThemeToggle } from "./ThemeToggle";

const navLinks = [
  { href: "/checklists", label: "Checklists" },
  { href: "/sets", label: "Sets" },
  { href: "/overview", label: "Overview" },
  { href: "/admin/analytics", label: "Searches" },
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
    <header className="shrink-0 bg-zinc-950 border-b border-zinc-800/80">
      <div className="flex items-center justify-between px-6 h-14">
        {/* Wordmark */}
        <Link href="/" className="flex items-center">
          {/* Dark logo (black text) — shown in light mode */}
          <img src="/checklist2-dark.svg" alt="Checklist²" height={40} className="h-10 w-auto logo-for-light" />
          {/* Light logo (white text) — shown in dark mode (default) */}
          <img src="/checklist2-light.svg" alt="Checklist²" height={40} className="h-10 w-auto logo-for-dark" />
        </Link>

        {/* Desktop nav */}
        <nav className="hidden md:flex items-center gap-1">
          {navLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className={`px-3 py-1.5 rounded-md text-sm transition-colors ${
                isActive(link.href)
                  ? "text-white font-medium bg-zinc-800/60"
                  : "text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/40"
              }`}
            >
              {link.label}
            </Link>
          ))}
        </nav>

        {/* Right side: theme toggle + hamburger */}
        <div className="flex items-center gap-1">
          <ThemeToggle />

          {/* Hamburger */}
          <button
            className="md:hidden p-1.5 text-zinc-400 hover:text-white transition-colors rounded-md hover:bg-zinc-800/60"
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
      </div>

      {/* Mobile menu */}
      {menuOpen && (
        <nav className="md:hidden border-t border-zinc-800/80 px-4 py-2 flex flex-col">
          {navLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              onClick={() => setMenuOpen(false)}
              className={`px-3 py-2.5 rounded-md text-sm transition-colors ${
                isActive(link.href)
                  ? "text-white font-medium bg-zinc-800/60"
                  : "text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/40"
              }`}
            >
              {link.label}
            </Link>
          ))}
        </nav>
      )}
    </header>
  );
}
