"use client";

import type { BoxOffer } from "@/lib/ebayBrowse";
import { trackEvent } from "@/lib/analytics";

const FONT_MONO = "var(--cl-font-mono), 'JetBrains Mono', ui-monospace, monospace";

export interface SealedBoxFormatData {
  format: string;
  label: string;
  offers: BoxOffer[];
  fallbackUrl: string | null;
  refreshedRelative: string | null;
}
export interface SealedBoxData {
  formats: SealedBoxFormatData[];
  disclosure: string;
}

function money(n: number, currency = "USD"): string {
  return n.toLocaleString("en-US", { style: "currency", currency });
}

function shippingLabel(o: BoxOffer): string {
  if (o.shippingUnknown) return "+ shipping";
  if (o.shipping === 0) return "free shipping";
  return `+ ${money(o.shipping, o.currency)} ship`;
}

/**
 * Live sealed-box listings from the eBay Browse API (cached, EPN-tagged). One
 * row per box format that has offers; formats with none show a tagged search
 * link. Thumbnails load directly from eBay's CDN (never proxied). Hidden when
 * no format has offers or a fallback link.
 */
export function SealedBoxOffers({ data, setSlug }: { data: SealedBoxData | null; setSlug: string }) {
  if (!data) return null;
  const formats = data.formats.filter((f) => f.offers.length > 0 || f.fallbackUrl);
  if (formats.length === 0) return null;
  const refreshed = formats.find((f) => f.refreshedRelative)?.refreshedRelative ?? null;

  return (
    <div style={{ marginTop: 24 }}>
      <div style={{ fontFamily: FONT_MONO, fontSize: 9, fontWeight: 600, letterSpacing: 1.6, color: "var(--brand-slate)", textTransform: "uppercase", marginBottom: 12 }}>
        Sealed Boxes on eBay
      </div>

      <div className="space-y-3">
        {formats.map((f) => (
          <div key={f.format} style={{ background: "var(--brand-card)", border: "1px solid var(--brand-line)", borderRadius: 10, padding: "12px 14px" }}>
            <div className="flex items-baseline justify-between" style={{ marginBottom: f.offers.length ? 10 : 6 }}>
              <span style={{ fontFamily: "var(--cl-font-display), 'Inter Tight', sans-serif", fontSize: 15, fontWeight: 600, color: "var(--brand-ink)" }}>
                {f.label}
              </span>
              {f.offers.length > 0 && (
                <span style={{ fontSize: 13, color: "var(--brand-slate)" }}>
                  from <span style={{ fontFamily: FONT_MONO, fontWeight: 600, color: "var(--brand-ink)" }}>{money(f.offers[0].total, f.offers[0].currency)}</span>
                </span>
              )}
            </div>

            {f.offers.length > 0 ? (
              <div className="space-y-2">
                {f.offers.map((o, i) => (
                  <a
                    key={o.itemId || i}
                    href={o.url}
                    target="_blank"
                    rel="nofollow sponsored noopener"
                    onClick={() => trackEvent("ebay_offer_click", { set_slug: setSlug, format: f.format, rank: i + 1, total: o.total })}
                    className="flex items-center gap-3"
                    style={{ textDecoration: "none", padding: "6px", borderRadius: 8, border: "1px solid var(--brand-line)", background: "var(--brand-page)" }}
                  >
                    {/* Thumbnail — loaded directly from eBay's CDN, never proxied/cached. */}
                    {o.imageUrl ? (
                      // eslint-disable-next-line @next/next/no-img-element
                      <img src={o.imageUrl} alt="" width={56} height={56} loading="lazy"
                        style={{ width: 56, height: 56, flexShrink: 0, objectFit: "cover", borderRadius: 6, background: "var(--brand-track)" }} />
                    ) : (
                      <div aria-hidden style={{ width: 56, height: 56, flexShrink: 0, borderRadius: 6, background: "var(--brand-track)" }} />
                    )}
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div className="flex items-center gap-2" style={{ marginBottom: 2 }}>
                        {i === 0 && (
                          <span style={{ flexShrink: 0, fontFamily: FONT_MONO, fontSize: 9, fontWeight: 700, letterSpacing: 0.4, color: "var(--brand-ok)", background: "rgba(31,143,74,0.10)", border: "1px solid rgba(31,143,74,0.25)", padding: "1px 5px", borderRadius: 3 }}>
                            Best deal
                          </span>
                        )}
                        <span className="truncate" style={{ fontSize: 13, color: "var(--brand-ink)", minWidth: 0 }} title={o.title}>{o.title}</span>
                      </div>
                      <div style={{ fontSize: 12, color: "var(--brand-slate)" }}>
                        <span style={{ fontFamily: FONT_MONO, fontWeight: 600, color: "var(--brand-ink)" }}>{money(o.price, o.currency)}</span>
                        {" "}<span>{shippingLabel(o)}</span>
                        {o.seller && (
                          <span> · {o.seller}{o.sellerFeedbackPct != null ? ` (${o.sellerFeedbackPct}%)` : ""}</span>
                        )}
                      </div>
                    </div>
                    <span style={{ flexShrink: 0, fontFamily: FONT_MONO, fontSize: 12, fontWeight: 600, color: "var(--brand-accent-deep)", whiteSpace: "nowrap" }}>View on eBay ↗</span>
                  </a>
                ))}
              </div>
            ) : (
              <a
                href={f.fallbackUrl!}
                target="_blank"
                rel="nofollow sponsored noopener"
                onClick={() => trackEvent("ebay_offer_search_click", { set_slug: setSlug, format: f.format })}
                style={{ fontSize: 13, fontWeight: 600, color: "var(--brand-accent-deep)", textDecoration: "none" }}
              >
                Search eBay for {f.label} boxes ↗
              </a>
            )}
          </div>
        ))}
      </div>

      <div style={{ fontSize: 11, color: "var(--brand-fog)", marginTop: 10 }}>
        Prices from eBay{refreshed ? `, refreshed ${refreshed}` : ""}. {data.disclosure}
      </div>
    </div>
  );
}
