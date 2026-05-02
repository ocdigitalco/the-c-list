"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { CL2Wordmark, CL2 } from "@/components/brand";
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
    <header className="shrink-0 border-b" style={{ background: CL2.paper, borderColor: CL2.fog }}>
      <div className="flex items-center justify-between px-6 h-14">
        {/* Wordmark */}
        <Link href="/" className="flex items-center" style={{ textDecoration: "none" }}>
          <CL2Wordmark size={44} supSize={34} ink={CL2.ink} accent={CL2.accent} />
        </Link>

        {/* Desktop nav */}
        <nav className="hidden md:flex items-center gap-1">
          {navLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="px-3 py-1.5 rounded-md text-sm font-bold transition-colors"
              style={{
                color: isActive(link.href) ? CL2.ink : CL2.slate,
                background: isActive(link.href) ? CL2.paperDeep : "transparent",
              }}
            >
              {link.label}
            </Link>
          ))}
        </nav>

        {/* Right side: hamburger */}
        <div className="flex items-center gap-1">
          {/* Hamburger */}
          <button
            className="md:hidden p-1.5 transition-colors rounded-md"
            style={{ color: CL2.slate }}
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
        <nav className="md:hidden px-4 py-2 flex flex-col" style={{ borderTop: `1px solid ${CL2.fog}` }}>
          {navLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              onClick={() => setMenuOpen(false)}
              className="px-3 py-2.5 rounded-md text-sm font-bold transition-colors"
              style={{
                color: isActive(link.href) ? CL2.ink : CL2.slate,
                background: isActive(link.href) ? CL2.paperDeep : "transparent",
              }}
            >
              {link.label}
            </Link>
          ))}
        </nav>
      )}
    </header>
  );
}
