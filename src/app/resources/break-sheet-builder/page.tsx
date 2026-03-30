import type { Metadata } from "next";
import Link from "next/link";
import { Footer } from "@/components/Footer";

export const metadata: Metadata = {
  title: "Break Sheet Builder — Checklist2",
  description:
    "How the Break Sheet Builder generates Whatnot-ready CSVs and what each column contains",
};

const csvColumns: { column: string; value: string }[] = [
  { column: "Category", value: "Sport-based (e.g. \"UFC Breaks\", \"NBA Breaks\")" },
  { column: "Sub Category", value: "League name (e.g. \"UFC\", \"NBA\")" },
  { column: "Title", value: "Auto-generated athlete title with tag summary" },
  { column: "Description", value: "Breaker's custom break description" },
  { column: "Quantity", value: "Always 1" },
  { column: "Type", value: "Buy it Now or Auction" },
  { column: "Price", value: "Empty -- breaker fills in after download" },
  { column: "Shipping Profile", value: "Empty" },
  { column: "Offerable", value: "TRUE" },
  { column: "Hazmat", value: "Not Hazmat" },
  { column: "Condition", value: "New" },
  { column: "Cost Per Item", value: "Empty" },
  { column: "SKU", value: "Empty" },
  { column: "Image URLs", value: "Empty" },
];

const tips = [
  "Use the Break Description field to include case and box counts and key hit guarantees -- buyers look for this info before purchasing slots.",
  "Download the CSV, add your prices in a spreadsheet, then upload directly to Whatnot.",
  "The file is named automatically: [Set Name] - Break Sheet.csv",
];

export default function BreakSheetBuilderPage() {
  return (
    <div className="h-full overflow-y-auto">
      <div className="max-w-3xl mx-auto px-6 py-10 space-y-10">
        {/* Breadcrumb */}
        <div className="flex items-center gap-1.5">
          <Link
            href="/resources"
            className="flex items-center gap-1 text-xs text-zinc-500 hover:text-zinc-300 transition-colors"
          >
            <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
            </svg>
            Resources
          </Link>
          <span className="text-zinc-700 text-xs">/</span>
          <span className="text-xs text-zinc-400">Break Sheet Builder</span>
        </div>

        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight mb-2">
            Break Sheet Builder
          </h1>
          <p className="text-sm text-zinc-400 leading-relaxed">
            How the Break Sheet Builder works and what each column in the downloaded CSV contains.
          </p>
        </div>

        {/* What is it */}
        <Section title="What is the Break Sheet Builder?">
          <p>
            The Break Sheet Builder is a tool built into every set page on Checklist2. It generates
            a Whatnot-ready CSV file pre-filled with athlete slots for a break, saving breakers
            hours of manual data entry. Each row in the CSV represents one purchasable slot -- the
            buyer of that slot receives all cards pulled for that athlete during the break.
          </p>
        </Section>

        {/* Where does it appear */}
        <Section title="Where does it appear?">
          <p>
            The Break Sheet Builder button appears in the header of every set page. Clicking it
            opens a modal where breakers can customize the output before downloading.
          </p>
        </Section>

        {/* What can you customize */}
        <Section title="What can you customize?">
          <div className="space-y-3">
            <CustomizeRow label="Break Description">
              A free-text field that populates the Description column for every row (e.g.{" "}
              <span className="font-mono text-zinc-300 text-xs">
                3 Cases! 2024 Topps Midnight UFC -- 24 Boxes | 72 Autos
              </span>
              ).
            </CustomizeRow>
            <CustomizeRow label="Listing Type">
              Choose between Buy it Now or Auction, which populates the Type column.
            </CustomizeRow>
            <CustomizeRow label="Tag Labels">
              Define how each card type appears in the athlete&apos;s title (e.g. AUTO, MEM AUTO,
              RELIC, RC). These can be customized before downloading.
            </CustomizeRow>
            <CustomizeRow label="Live Preview">
              See exactly how the first few rows will look before downloading.
            </CustomizeRow>
          </div>
        </Section>

        {/* How titles are generated */}
        <Section title="How are athlete titles generated?">
          <p className="mb-4">
            Each athlete&apos;s title is automatically built from their card data in the set. The
            builder scans every card appearance and summarizes what that athlete has using the
            customizable tag labels. For example:
          </p>
          <div className="rounded-lg border border-zinc-800 bg-zinc-950 divide-y divide-zinc-800 overflow-hidden">
            {[
              "Islam Makhachev (AUTOx3)(RELIC)",
              "Cooper Flagg (RC)(AUTO)",
              "Paul Skenes (AUTOx2)(MEM AUTO)",
            ].map((title) => (
              <div key={title} className="px-4 py-3">
                <p className="text-sm font-mono text-zinc-300">{title}</p>
              </div>
            ))}
          </div>
        </Section>

        {/* CSV column table */}
        <Section title="What does each CSV column contain?">
          <div className="rounded-xl border border-zinc-800 overflow-hidden">
            <table className="w-full">
              <thead>
                <tr className="border-b border-zinc-800 bg-zinc-900/60">
                  <th className="text-left text-xs font-semibold text-zinc-500 uppercase tracking-wider px-4 py-2.5 w-[38%]">
                    Column
                  </th>
                  <th className="text-left text-xs font-semibold text-zinc-500 uppercase tracking-wider px-4 py-2.5">
                    Value
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-800/60">
                {csvColumns.map((row, i) => (
                  <tr
                    key={row.column}
                    className={i % 2 === 0 ? "bg-zinc-900" : "bg-zinc-900/40"}
                  >
                    <td className="px-4 py-2.5 text-sm font-medium text-zinc-300 align-top">
                      {row.column}
                    </td>
                    <td className="px-4 py-2.5 text-sm text-zinc-500">
                      {row.value}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Section>

        {/* Platform support */}
        <Section title="What platforms support this CSV format?">
          <p>
            The CSV is formatted specifically for Whatnot, the leading live break platform. The
            column structure matches Whatnot&apos;s bulk listing upload template exactly, allowing
            breakers to upload the file directly after adding their prices.
          </p>
        </Section>

        {/* Tips */}
        <Section title="Tips for breakers">
          <ul className="space-y-2 text-sm text-zinc-400">
            {tips.map((tip) => (
              <li key={tip} className="flex items-start gap-2">
                <span className="shrink-0 text-zinc-600 mt-0.5">--</span>
                {tip}
              </li>
            ))}
          </ul>
        </Section>
      </div>
      <Footer />
    </div>
  );
}

function Section({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <section>
      <h2 className="text-base font-semibold text-white mb-3 pb-2 border-b border-zinc-800">
        {title}
      </h2>
      <div className="text-sm text-zinc-400 leading-relaxed space-y-3">{children}</div>
    </section>
  );
}

function CustomizeRow({
  label,
  children,
}: {
  label: string;
  children: React.ReactNode;
}) {
  return (
    <div className="rounded-lg border border-zinc-800 bg-zinc-900 px-4 py-3">
      <p className="text-sm font-semibold text-white mb-1">{label}</p>
      <p className="text-sm text-zinc-400 leading-relaxed">{children}</p>
    </div>
  );
}
