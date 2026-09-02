import type { Metadata } from "next";
import { db } from "@/lib/db";
import { sets } from "@/lib/schema";
import { sql } from "drizzle-orm";
import { SimulatorPageClient } from "./SimulatorPageClient";

export const metadata: Metadata = {
  title: "Box Break Simulator — Checklist2",
  description:
    "Run 10,000 simulated breaks and see realistic outcome distributions based on official pack odds.",
};

export default async function BreakSimulatorPage() {
  // Fetch all sets that have both pack_odds and box_config
  const eligibleSets = await db
    .select({
      id: sets.id,
      name: sets.name,
      sport: sets.sport,
      season: sets.season,
      packOdds: sets.packOdds,
      boxConfig: sets.boxConfig,
    })
    .from(sets)
    .where(
      sql`${sets.packOdds} IS NOT NULL AND ${sets.boxConfig} IS NOT NULL`
    )
    .orderBy(sql`${sets.season} DESC, ${sets.name}`);

  // Extract box type keys per set
  const setOptions = eligibleSets.map((s) => {
    const boxTypes: string[] = [];
    if (s.packOdds) {
      try {
        const raw = JSON.parse(s.packOdds);
        const firstVal = Object.values(raw)[0];
        if (firstVal !== null && typeof firstVal === "object") {
          boxTypes.push(...Object.keys(raw));
        } else {
          // Flat odds — derive from box_config keys
          if (s.boxConfig) {
            const bc = JSON.parse(s.boxConfig);
            const bcFirst = Object.values(bc)[0];
            if (bcFirst !== null && typeof bcFirst === "object") {
              boxTypes.push(...Object.keys(bc));
            } else {
              boxTypes.push("hobby");
            }
          }
        }
      } catch {
        // skip
      }
    }
    return {
      id: s.id,
      name: s.name,
      sport: s.sport,
      season: s.season,
      boxTypes: boxTypes.length > 0 ? boxTypes : ["hobby"],
    };
  });

  return (
    <div className="flex-1">
      <div className="max-w-[800px] mx-auto px-6 py-10 space-y-6">
        <div>
          <h1 className="text-2xl font-normal text-[var(--brand-ink)] tracking-tight" style={{ fontFamily: "var(--brand-font-head)", fontSynthesisWeight: "none" }}>
            Box Break Simulator
          </h1>
          <p className="text-sm text-[var(--brand-slate)] mt-1">
            Run 10,000 simulated breaks and see realistic outcome distributions.
            Results are based on official pack odds and checklist data.
          </p>
        </div>
        <SimulatorPageClient sets={setOptions} />
      </div>
    </div>
  );
}
