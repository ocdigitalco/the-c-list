import { loadAthletePage, athleteJsonLd, toJsonLd, type AthleteCore } from "@/lib/athletes/seo";
import { buildEbayAthleteSearchUrl } from "@/lib/ebay/searchUrl";
import { AthleteMasterClient } from "./AthleteMasterClient";

/** Server wrapper shared by /athletes, /characters, /people, /teams. Fetches the
 * page payload (React-cached, shared with generateMetadata), emits JSON-LD, and
 * mounts the interactive client. */
export async function AthleteMasterPage({ core }: { core: AthleteCore }) {
  const data = await loadAthletePage(core);
  const soldCompsEnabled = process.env.SOLD_COMPS_ENABLED === "true";
  const ebayAllUrl = buildEbayAthleteSearchUrl(core.name, core.sport, core.slug, process.env.EPN_CAMPAIGN_ID);
  const ld = athleteJsonLd(core);

  return (
    <>
      {ld.map((obj, i) => (
        <script key={i} type="application/ld+json" dangerouslySetInnerHTML={{ __html: toJsonLd(obj) }} />
      ))}
      <AthleteMasterClient data={data} soldCompsEnabled={soldCompsEnabled} ebayAllUrl={ebayAllUrl} />
    </>
  );
}
