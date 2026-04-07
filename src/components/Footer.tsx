import Link from "next/link";

const exploreLinks = [
  { href: "/checklists", label: "Checklists" },
  { href: "/sets", label: "Sets" },
  { href: "/overview", label: "Overview" },
  { href: "/admin/analytics", label: "Searches" },
];

const toolLinks = [
  { href: "/resources/break-hit-calculator", label: "Break Hit Calculator" },
  { href: "/checklists", label: "Break Sheet Builder" },
  { href: "/resources/glossary", label: "Glossary" },
];

const resourceLinks = [
  { href: "/resources", label: "Resources" },
  { href: "/articles", label: "Articles" },
  { href: "/resources/break-hit-calculator", label: "Break Hit Calculator Guide" },
];

const companyLinks = [
  { href: "/about", label: "About" },
  { href: "/terms", label: "Terms of Use" },
  { href: "/privacy", label: "Privacy Policy" },
];

const platformLinks = [
  { href: "https://www.whatnot.com", label: "Whatnot" },
  { href: "https://www.tiktok.com", label: "TikTok" },
  { href: "https://www.ebay.com", label: "eBay" },
];

export function Footer() {
  return (
    <footer className="shrink-0 bg-zinc-950 border-t border-zinc-800/80">
      <div className="max-w-6xl mx-auto px-6 py-14">

        {/* Top section: wordmark + link columns */}
        <div className="flex flex-col lg:flex-row gap-12 lg:gap-20">

          {/* Wordmark + tagline */}
          <div className="lg:w-64 shrink-0">
            <Link href="/" className="inline-flex items-center mb-3">
              <img src="/checklist2-dark.svg" alt="Checklist²" height={50} className="h-[50px] w-auto logo-for-light" />
              <img src="/checklist2-light.svg" alt="Checklist²" height={50} className="h-[50px] w-auto logo-for-dark" />
            </Link>
            <p className="text-sm text-zinc-500 leading-relaxed">
              The complete sports card checklist platform for collectors and breakers.
            </p>
          </div>

          {/* Link columns */}
          <div className="grid grid-cols-2 sm:grid-cols-5 gap-10 flex-1">

            {/* Explore */}
            <div>
              <p className="text-xs font-semibold text-zinc-400 uppercase tracking-widest mb-4">Explore</p>
              <ul className="space-y-3">
                {exploreLinks.map((link) => (
                  <li key={link.href + link.label}>
                    <Link href={link.href} className="text-sm text-zinc-500 hover:text-zinc-200 transition-colors">
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>

            {/* Tools */}
            <div>
              <p className="text-xs font-semibold text-zinc-400 uppercase tracking-widest mb-4">Tools</p>
              <ul className="space-y-3">
                {toolLinks.map((link) => (
                  <li key={link.label}>
                    <Link href={link.href} className="text-sm text-zinc-500 hover:text-zinc-200 transition-colors">
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>

            {/* Resources */}
            <div>
              <p className="text-xs font-semibold text-zinc-400 uppercase tracking-widest mb-4">Resources</p>
              <ul className="space-y-3">
                {resourceLinks.map((link) => (
                  <li key={link.href + link.label}>
                    <Link href={link.href} className="text-sm text-zinc-500 hover:text-zinc-200 transition-colors">
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>

            {/* Company */}
            <div>
              <p className="text-xs font-semibold text-zinc-400 uppercase tracking-widest mb-4">Company</p>
              <ul className="space-y-3">
                {companyLinks.map((link) => (
                  <li key={link.href}>
                    <Link href={link.href} className="text-sm text-zinc-500 hover:text-zinc-200 transition-colors">
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>

            {/* Platforms */}
            <div>
              <p className="text-xs font-semibold text-zinc-400 uppercase tracking-widest mb-4">Platforms</p>
              <ul className="space-y-3">
                {platformLinks.map((link) => (
                  <li key={link.href}>
                    <a
                      href={link.href}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm text-zinc-500 hover:text-zinc-200 transition-colors inline-flex items-center gap-1.5"
                    >
                      {link.label}
                      <svg className="w-3 h-3 opacity-60" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 6H5.25A2.25 2.25 0 003 8.25v10.5A2.25 2.25 0 005.25 21h10.5A2.25 2.25 0 0018 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25" />
                      </svg>
                    </a>
                  </li>
                ))}
              </ul>
            </div>

          </div>
        </div>

        {/* Bottom bar */}
        <div className="mt-12 pt-6 border-t border-zinc-800/60 space-y-3">
          <div className="flex items-center justify-between gap-4 flex-wrap">
            <p className="text-base text-zinc-600">© 2026 Checklist2. All rights reserved.</p>
            <p className="text-base text-zinc-600">Created by Tyler Lawrence</p>
          </div>
          <p className="text-base text-zinc-600 leading-relaxed">
            All third-party trademarks and logos are the property of their respective owners. Checklist2 is not affiliated with, endorsed by, or sponsored by Whatnot, UFC, EPL, NBA, MLS, MLB, NFL, UEFA, WWE, WWF, Cactus Jack, Olympics, Topps, or Panini.
          </p>
        </div>

      </div>
    </footer>
  );
}
