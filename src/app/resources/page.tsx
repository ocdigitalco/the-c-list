import type { Metadata } from "next";
import Link from "next/link";
import { PageShell } from "@/components/PageShell";

export const metadata: Metadata = {
  title: "Resources — Checklist2",
  description: "Everything you need to understand how Checklist2 works",
};

const resources = [
  {
    href: "/resources/glossary",
    title: "Glossary",
    description: "Definitions for every term and data point used across the app.",
  },
  {
    href: "/resources/break-hit-calculator",
    title: "Break Hit Calculator",
    description:
      "Learn how the break hit calculator works and what it means for your breaks.",
  },
  {
    href: "/resources/break-sheet-builder",
    title: "Break Sheet Builder",
    description:
      "How the Break Sheet Builder generates Whatnot-ready CSVs and what each column contains.",
  },
  {
    href: "/resources/break-simulator",
    title: "Box Break Simulator",
    description:
      "Run 10,000 simulated breaks for any set and see realistic outcome distributions based on official pack odds.",
  },
];

export default function ResourcesPage() {
  return (
    <PageShell
      breadcrumb={{ label: "Home", href: "/checklists" }}
      title="Resources"
      description="Guides, tools, and reference material for collectors and breakers"
    >
        <div className="grid sm:grid-cols-2 gap-4">
          {resources.map((r) => (
            <Link
              key={r.href}
              href={r.href}
              className="group block rounded-xl border border-zinc-800 bg-zinc-900 px-6 py-5 hover:border-zinc-600 hover:bg-zinc-800/60 transition-colors"
            >
              <div className="flex items-start justify-between gap-3">
                <div>
                  <h2 className="text-base font-semibold text-white mb-1.5">{r.title}</h2>
                  <p className="text-sm text-zinc-400 leading-relaxed">{r.description}</p>
                </div>
                <svg
                  className="shrink-0 w-4 h-4 text-zinc-600 group-hover:text-zinc-400 mt-0.5 transition-colors"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth={2}
                >
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </Link>
          ))}
        </div>
    </PageShell>
  );
}
