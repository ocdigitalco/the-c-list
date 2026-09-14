"use client";

import type { ReactNode } from "react";
import type { BoxOffer } from "@/lib/ebayBrowse";
import type { SealedBoxData, SealedBoxFormatData } from "@/lib/ebayRefresh";
import { trackEvent } from "@/lib/analytics";
import { ebayImageAt } from "@/lib/ebayImage";
import styles from "./SealedBoxOffers.module.css";

// Single source of truth for the shape lives in @/lib/ebayRefresh; re-export so
// SetDetailClient can keep importing it from this component.
export type { SealedBoxData };

const REL = "nofollow sponsored noopener";

function money(n: number, currency = "USD"): string {
  return n.toLocaleString("en-US", { style: "currency", currency });
}

/** Shipping label + seller/feedback meta. Free shipping and the feedback % render
 *  in the success color; everything else is muted. */
function metaNodes(o: BoxOffer): ReactNode {
  let ship: ReactNode;
  if (o.shippingUnknown) ship = "+ shipping";
  else if (o.shipping === 0) ship = <span className={styles.ok}>Free shipping</span>;
  else ship = `+ ${money(o.shipping, o.currency)} ship`;
  return (
    <>
      {ship}
      {o.seller && (
        <>
          {" · "}{o.seller}
          {o.sellerFeedbackPct != null && <> <span className={styles.ok}>{o.sellerFeedbackPct}%</span></>}
        </>
      )}
    </>
  );
}

/**
 * Live sealed-box listings from the eBay Browse API (cached, EPN-tagged).
 * Hero + runners-up per box type: the cheapest listing (by total) is the hero,
 * the next up-to-three are compact rows. Formats with no cached offers are shown
 * only as footer cross-links; if no format has offers a single tagged search
 * line is shown so new releases keep the affiliate link.
 */
export function SealedBoxOffers({ data, setSlug }: { data: SealedBoxData | null; setSlug: string }) {
  if (!data) return null;
  const withOffers = data.formats.filter((f) => f.offers.length > 0);

  // No box type has cached offers (incl. sets with no recognized formats / no
  // box_config) → one compact tagged-search line so every visible set keeps the
  // affiliate link. Prefer the first format's tagged search, else the set-wide one.
  if (withOffers.length === 0) {
    const url = data.formats[0]?.searchUrl ?? data.searchUrl;
    if (!url) return null;
    return (
      <section className={styles.wrap} aria-label="Sealed boxes on eBay">
        <div className={styles.heading}>Sealed boxes on eBay</div>
        <p className={styles.emptyLine}>
          No sealed boxes cached yet ·{" "}
          <a href={url} target="_blank" rel={REL} className={styles.emptyLink}
            onClick={() => trackEvent("ebay_offer_search_click", { set_slug: setSlug, format: data.formats[0]?.format ?? "any" })}>
            Search eBay for {data.setName} boxes ↗
          </a>
        </p>
        <div className={styles.disclosure}>{data.disclosure}</div>
      </section>
    );
  }

  const refreshed = withOffers.find((f) => f.refreshedRelative)?.refreshedRelative ?? null;

  return (
    <section className={styles.wrap} aria-label="Sealed boxes on eBay">
      <div className={styles.heading}>Sealed boxes on eBay</div>
      {withOffers.map((group) => (
        <BoxGroup key={group.format} group={group} allFormats={data.formats} setSlug={setSlug} />
      ))}
      <div className={styles.disclosure}>
        Prices from eBay{refreshed ? `, refreshed ${refreshed}` : ""}. {data.disclosure}
      </div>
    </section>
  );
}

function BoxGroup({ group, allFormats, setSlug }: {
  group: SealedBoxFormatData;
  allFormats: SealedBoxFormatData[];
  setSlug: string;
}) {
  const offers = group.offers;
  const hero = offers[0];
  const rows = offers.slice(1, 4); // up to 3 runners-up
  const others = allFormats.filter((f) => f.format !== group.format);

  return (
    <div id={`sealed-${group.format}`} className={styles.group}>
      <div className={styles.eyebrow}>{group.label}</div>

      <div className={styles.grid} data-single={rows.length === 0 ? "1" : undefined}>
        {/* Hero — whole card is the click target; the button is the affordance. */}
        <a
          className={styles.hero}
          href={hero.url}
          target="_blank"
          rel={REL}
          onClick={() => trackEvent("ebay_offer_click", { set_slug: setSlug, format: group.format, rank: 1, total: hero.total })}
        >
          {/* Fixed-aspect box; the image is absolutely filled (object-fit:cover)
              so a tall eBay portrait can't drive the hero height. width/height
              stay for CLS but don't affect layout. */}
          <div className={styles.photoWrap} aria-hidden={!hero.imageUrl}>
            {hero.imageUrl && (
              // eslint-disable-next-line @next/next/no-img-element -- eBay CDN, never proxied
              <img
                className={styles.photo}
                src={ebayImageAt(hero.imageUrl, 960)}
                srcSet={`${ebayImageAt(hero.imageUrl, 500)} 500w, ${ebayImageAt(hero.imageUrl, 960)} 960w, ${ebayImageAt(hero.imageUrl, 1600)} 1600w`}
                sizes="(min-width: 860px) 420px, (min-width: 700px) 340px, 100vw"
                alt=""
                width={400}
                height={300}
                loading="lazy"
                decoding="async"
              />
            )}
          </div>
          <div className={styles.heroBody}>
            <div className={styles.badgeRow}>
              <span className={styles.bestDeal}>Best deal</span>
              <span className={styles.lowestOf}>lowest of {offers.length} listing{offers.length === 1 ? "" : "s"}</span>
            </div>
            <div className={styles.heroTitle}>{hero.title}</div>
            <div className={styles.priceRow}>
              <div>
                <div className={styles.heroPrice}>{money(hero.total, hero.currency)}</div>
                <div className={styles.meta}>{metaNodes(hero)}</div>
              </div>
              <span className={styles.ctaSolid}>View on eBay ↗</span>
            </div>
          </div>
        </a>

        {/* Runners-up */}
        {rows.length > 0 && (
          <div className={styles.runners}>
            <div className={styles.runnersHead}>Other listings</div>
            {rows.map((o, i) => (
              <a
                key={o.itemId || i}
                className={styles.row}
                href={o.url}
                target="_blank"
                rel={REL}
                onClick={() => trackEvent("ebay_offer_click", { set_slug: setSlug, format: group.format, rank: i + 2, total: o.total })}
              >
                {o.imageUrl ? (
                  // eslint-disable-next-line @next/next/no-img-element -- eBay CDN, never proxied
                  <img
                    className={styles.thumb}
                    src={ebayImageAt(o.imageUrl, 300)}
                    srcSet={`${ebayImageAt(o.imageUrl, 300)} 1x, ${ebayImageAt(o.imageUrl, 500)} 2x`}
                    alt=""
                    width={96}
                    height={96}
                    loading="lazy"
                    decoding="async"
                  />
                ) : (
                  <div className={styles.thumbEmpty} aria-hidden />
                )}
                <div className={styles.rowMain}>
                  <div className={styles.rowTitle}>{o.title}</div>
                  <div className={styles.meta}>{metaNodes(o)}</div>
                </div>
                <div className={styles.rowRight}>
                  <div className={styles.rowPrice}>{money(o.total, o.currency)}</div>
                  <span className={styles.ctaOutline}>View on eBay ↗</span>
                </div>
              </a>
            ))}
          </div>
        )}
      </div>

      <div className={styles.groupFooter}>
        <span className={styles.crosslinks}>
          {others.map((f, i) => (
            <span key={f.format}>
              {i > 0 && " · "}
              {f.offers.length > 0 ? (
                <a href={`#sealed-${f.format}`}>{f.label} from {money(f.offers[0].total, f.offers[0].currency)}</a>
              ) : f.searchUrl ? (
                <a href={f.searchUrl} target="_blank" rel={REL}
                  onClick={() => trackEvent("ebay_offer_search_click", { set_slug: setSlug, format: f.format })}>
                  {f.label} · search eBay →
                </a>
              ) : (
                <span>{f.label}</span>
              )}
            </span>
          ))}
        </span>
        {group.searchUrl && (
          <a
            className={styles.seeAll}
            href={group.searchUrl}
            target="_blank"
            rel={REL}
            onClick={() => trackEvent("ebay_offer_search_click", { set_slug: setSlug, format: group.format })}
          >
            See all sealed boxes →
          </a>
        )}
      </div>
    </div>
  );
}
