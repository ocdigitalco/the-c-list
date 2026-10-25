"use client";

import { useEffect, useId, useMemo, useState } from "react";
import { trackEvent } from "@/lib/analytics";
import { ebayImageAt } from "@/lib/ebayImage";
import type { Break, BreaksPayload } from "@/lib/breaks/refresh";
import styles from "./LiveBreaks.module.css";

const REL = "sponsored noopener";

const FORMAT_LABELS: Record<string, string> = {
  PYT: "Pick your team",
  PYP: "Pick your player",
  PYD: "Pick your division",
  random: "Random team",
  team: "Team break",
  case: "Case break",
  mixer: "Mixer",
};

// Athlete-page attribution: the stored affiliate/search URLs carry
// customid=breaks:<set-slug>; append :<player-id> so clicks from an athlete page
// read breaks:<set-slug>:<player-id>. Defensive — returns the URL unchanged if it
// has no customid or can't be parsed.
function withPlayerRef(url: string | null | undefined, playerId: number | undefined): string | undefined {
  if (!url) return url ?? undefined;
  if (playerId == null) return url;
  try {
    const u = new URL(url);
    const cur = u.searchParams.get("customid");
    if (!cur) return url;
    const suffix = `:${playerId}`;
    if (!cur.endsWith(suffix)) u.searchParams.set("customid", cur + suffix);
    return u.toString();
  } catch {
    return url;
  }
}

function money(cents: number | null, currency = "USD"): string {
  if (cents == null) return "—";
  return (cents / 100).toLocaleString("en-US", { style: "currency", currency, maximumFractionDigits: 0 });
}

// Exact price (with cents) for an individual, purchasable spot chip — unlike the
// row's rounded "from" summary, the listed buy price is shown to the cent.
function moneyExact(cents: number | null, currency = "USD"): string {
  if (cents == null) return "—";
  return (cents / 100).toLocaleString("en-US", { style: "currency", currency });
}

function relativeLabel(iso: string | null): string | null {
  if (!iso) return null;
  const diff = Date.now() - Date.parse(iso);
  if (!isFinite(diff)) return null;
  const d = Math.floor(diff / 86_400_000);
  if (d <= 0) return "today";
  if (d === 1) return "yesterday";
  if (d < 30) return `${d} days ago`;
  return null;
}

// Fetch the grouped breaks for a set (optionally filtered to a player). Client-
// side because the host pages are cached indefinitely / for a week but break data
// turns over hourly; the API response is itself CDN-cached for 15 min.
function useBreaks(url: string | null): { data: BreaksPayload | null; loading: boolean } {
  const [data, setData] = useState<BreaksPayload | null>(null);
  const [loading, setLoading] = useState<boolean>(!!url);
  useEffect(() => {
    if (!url) return;
    let alive = true;
    setLoading(true);
    fetch(url)
      .then((r) => (r.ok ? r.json() : null))
      .then((j: BreaksPayload | null) => { if (alive) { setData(j); setLoading(false); } })
      .catch(() => { if (alive) { setData(null); setLoading(false); } });
    return () => { alive = false; };
  }, [url]);
  return { data, loading };
}

function BreakCard({ b, setSlug, playerId, playerName }: {
  b: Break; setSlug: string; playerId?: number; playerName?: string | null;
}) {
  const listed = relativeLabel(b.listedAt);
  const fmt = b.formatGuess ? FORMAT_LABELS[b.formatGuess] ?? "Break" : "Break";
  const href = withPlayerRef(b.viewUrl, playerId);
  return (
    <a
      className={styles.card}
      href={href}
      target="_blank"
      rel={REL}
      onClick={() => trackEvent("break_click", { source: "ebay", set: setSlug, ...(playerId != null ? { player: playerId } : {}), seller: b.seller })}
    >
      {b.imageUrl ? (
        // eslint-disable-next-line @next/next/no-img-element -- eBay CDN, never proxied
        <img className={styles.thumb} src={ebayImageAt(b.imageUrl, 200)} alt="" width={64} height={64} loading="lazy" decoding="async" />
      ) : (
        <div className={styles.thumbEmpty} aria-hidden />
      )}

      <div className={styles.main}>
        <div className={styles.titleRow}>
          <span className={styles.seller}>{b.seller}</span>
          {b.sellerFeedbackPct != null && <span className={styles.feedback}>{b.sellerFeedbackPct}%</span>}
          <span className={styles.chip}>{fmt}</span>
          {b.namesPlayer && playerName && <span className={`${styles.chip} ${styles.chipPlayer}`}>names {playerName.split(" ").slice(-1)[0]}</span>}
          <span className={styles.chip}>{b.buyingLabel}</span>
        </div>
        <div className={styles.meta}>
          {b.spotCount} spot{b.spotCount === 1 ? "" : "s"}
          {listed && (
            <>
              {" "}<span className={styles.sep}>·</span>{" "}
              <span className={b.listedToday ? styles.today : undefined}>listed {listed}</span>
            </>
          )}
        </div>
      </div>

      <div className={styles.right}>
        <span className={styles.priceWrap}>
          <span className={styles.priceLabel}>from</span>
          <span className={styles.price}>{money(b.startingPriceCents, b.currency)}</span>
        </span>
        <span className={styles.cta}>View spots ↗</span>
      </div>
    </a>
  );
}

function WhatnotRow({ url, setSlug }: { url: string; setSlug: string }) {
  return (
    <a
      className={styles.whatnot}
      href={url}
      target="_blank"
      rel={REL}
      onClick={() => trackEvent("break_click", { source: "whatnot", set: setSlug })}
    >
      <span className={styles.whatnotText}>
        <b className={styles.whatnotTitle}>New to Whatnot? Get $25 toward your first break</b>
        Sign up with our invite and a $25 credit is applied to your first purchase.
      </span>
      <span className={styles.whatnotCta}>Claim $25 on Whatnot ↗</span>
    </a>
  );
}

// ── Set page: one break as an expandable row of per-spot chips ────────────────
const SPOTS_COLLAPSED = 16;

function SpotAccordionRow({ b, setSlug }: { b: Break; setSlug: string }) {
  const [open, setOpen] = useState(false);
  const [showAll, setShowAll] = useState(false);
  const [sort, setSort] = useState<"price" | "az">("price");
  const panelId = useId();

  const listed = relativeLabel(b.listedAt);
  const fmt = b.formatGuess ? FORMAT_LABELS[b.formatGuess] ?? "Break" : "Break";

  const sorted = useMemo(() => {
    const s = [...b.spots];
    if (sort === "az") s.sort((x, y) => x.label.localeCompare(y.label, "en", { numeric: true }));
    else s.sort((x, y) => (x.priceCents ?? Infinity) - (y.priceCents ?? Infinity));
    return s;
  }, [b.spots, sort]);
  const visible = showAll ? sorted : sorted.slice(0, SPOTS_COLLAPSED);

  return (
    <div className={`${styles.card} ${open ? styles.cardExpanded : ""}`}>
      {b.imageUrl ? (
        // eslint-disable-next-line @next/next/no-img-element -- eBay CDN, never proxied
        <img className={styles.thumb} src={ebayImageAt(b.imageUrl, 200)} alt="" width={64} height={64} loading="lazy" decoding="async" />
      ) : (
        <div className={styles.thumbEmpty} aria-hidden />
      )}

      <div className={styles.main}>
        <div className={styles.titleRow}>
          <span className={styles.seller}>{b.seller}</span>
          {b.sellerFeedbackPct != null && <span className={styles.feedback}>{b.sellerFeedbackPct}%</span>}
          <span className={styles.chip}>{fmt}</span>
          <span className={styles.chip}>{b.buyingLabel}</span>
        </div>
        <div className={styles.meta}>
          {b.spotCount} spot{b.spotCount === 1 ? "" : "s"}
          {listed && (
            <>
              {" "}<span className={styles.sep}>·</span>{" "}
              <span className={b.listedToday ? styles.today : undefined}>listed {listed}</span>
            </>
          )}
          {b.breakRef && (
            <>
              {" "}<span className={styles.sep}>·</span>{" "}Break #{b.breakRef}
            </>
          )}
        </div>
      </div>

      <div className={styles.right}>
        <span className={styles.priceWrap}>
          <span className={styles.priceLabel}>from</span>
          <span className={styles.price}>{money(b.startingPriceCents, b.currency)}</span>
        </span>
        <button
          type="button"
          className={`${styles.toggle} ${open ? styles.toggleOpen : ""}`}
          aria-expanded={open}
          aria-controls={panelId}
          onClick={() => setOpen((v) => !v)}
        >
          {open ? "Hide spots ▴" : `Show ${b.spotCount} spot${b.spotCount === 1 ? "" : "s"} ▾`}
        </button>
      </div>

      {open && (
        <div className={styles.spotsPanel} id={panelId}>
          <div className={styles.spotsHeader}>
            <span>{b.spotCount} spots · tap a spot to open its eBay listing</span>
            <span className={styles.sortToggle} role="group" aria-label="Sort spots">
              <button
                type="button"
                className={sort === "price" ? styles.sortActive : styles.sortBtn}
                aria-pressed={sort === "price"}
                onClick={() => setSort("price")}
              >
                Price ↑
              </button>
              <button
                type="button"
                className={sort === "az" ? styles.sortActive : styles.sortBtn}
                aria-pressed={sort === "az"}
                onClick={() => setSort("az")}
              >
                A–Z
              </button>
            </span>
          </div>
          <ul className={styles.chipGrid}>
            {visible.map((s) => (
              <li key={s.id}>
                <a
                  className={styles.spotChip}
                  href={s.url ?? undefined}
                  target="_blank"
                  rel={REL}
                  title={s.label}
                  onClick={() => trackEvent("break_click", { source: "ebay", set: setSlug, seller: b.seller, spot: s.label })}
                >
                  <span className={styles.spotName}>{s.label}</span>
                  <span className={styles.spotPrice}>{moneyExact(s.priceCents, b.currency)}</span>
                </a>
              </li>
            ))}
          </ul>
          {sorted.length > SPOTS_COLLAPSED && !showAll && (
            <button type="button" className={styles.showAll} onClick={() => setShowAll(true)}>
              Show all {sorted.length} spots ▾
            </button>
          )}
        </div>
      )}
    </div>
  );
}

// ── Set page: rollup with an empty state ──────────────────────────────────────
export function LiveBreaksSet({ setSlug, enabled, max = 6 }: { setSlug: string; enabled: boolean; max?: number }) {
  const { data, loading } = useBreaks(enabled ? `/api/breaks?set=${encodeURIComponent(setSlug)}` : null);
  if (!enabled) return null;
  if (loading || !data || !data.enabled) return null;

  const shown = data.breaks.slice(0, max);
  const refreshed = data.refreshedRelative;

  return (
    <section className={styles.wrap} aria-label="Live breaks on eBay">
      <div className={styles.heading}>Live breaks on eBay</div>
      <div className={styles.panel}>
        <WhatnotRow url={data.whatnotUrl} setSlug={setSlug} />
        {shown.length === 0 ? (
          <p className={styles.emptyLine}>
            No live breaks cached right now
            {data.searchUrl && (
              <>
                {" · "}
                <a href={data.searchUrl} target="_blank" rel={REL} className={styles.emptyLink}
                  onClick={() => trackEvent("break_click", { source: "ebay", set: setSlug, seller: "search" })}>
                  Search eBay breaks for {data.setName} ↗
                </a>
              </>
            )}
          </p>
        ) : (
          shown.map((b) => <SpotAccordionRow key={`${b.seller}:${b.breakRef ?? ""}`} b={b} setSlug={setSlug} />)
        )}
        <div className={styles.footer}>
          {data.searchUrl && shown.length > 0 && (
            <a className={styles.seeAll} href={data.searchUrl} target="_blank" rel={REL}
              onClick={() => trackEvent("break_click", { source: "ebay", set: setSlug, seller: "search" })}>
              See all breaks on eBay →
            </a>
          )}
        </div>
      </div>
      <div className={styles.disclosure}>
        Live break spots from eBay{refreshed ? `, refreshed ${refreshed}` : ""}. {data.disclosure}
      </div>
    </section>
  );
}

// ── Athlete page: this set's breaks, player-named spots first; NO empty state ──
export function LiveBreaksAthlete({ setSlug, playerId, enabled, max = 5 }: {
  setSlug: string; playerId: number; enabled: boolean; max?: number;
}) {
  const { data, loading } = useBreaks(
    enabled ? `/api/breaks?set=${encodeURIComponent(setSlug)}&player=${playerId}` : null
  );
  if (!enabled) return null;
  if (loading || !data || !data.enabled || data.breaks.length === 0) return null; // no empty state here

  const shown = data.breaks.slice(0, max);
  const name = data.playerName;
  return (
    <section className={styles.wrap} aria-label="Live breaks for this set">
      <div className={styles.heading}>
        Live breaks on eBay <span className={styles.subhead}>— break this set{name ? ` to pull ${name}` : ""}</span>
      </div>
      <div className={styles.panel}>
        {shown.map((b) => (
          <BreakCard key={`${b.seller}:${b.breakRef ?? ""}`} b={b} setSlug={setSlug} playerId={playerId} playerName={name} />
        ))}
        <div className={styles.footer}>
          {data.searchUrl && (
            <a className={styles.seeAll} href={withPlayerRef(data.searchUrl, playerId)} target="_blank" rel={REL}
              onClick={() => trackEvent("break_click", { source: "ebay", set: setSlug, player: playerId, seller: "search" })}>
              See all breaks on eBay →
            </a>
          )}
        </div>
      </div>
      <div className={styles.disclosure}>
        Most break spots are team or random breaks that don&apos;t name a player — breaking this set is how you pull {name ?? "them"}. {data.disclosure}
      </div>
    </section>
  );
}
