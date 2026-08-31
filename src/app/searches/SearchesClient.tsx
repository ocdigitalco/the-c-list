"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import type { LeaderboardEntry } from "./page";
import styles from "./searches.module.css";

// ─── Types ────────────────────────────────────────────────────────────────────

interface Props {
  views: LeaderboardEntry[];
  searches: LeaderboardEntry[];
  allSports: string[];
  currentRange: string;
  currentSport: string | null;
}

interface Athlete {
  name: string;
  sport: string;
  setName: string;
  slug: string | null;
  setSlug: string | null;
  nbaPlayerId: number | null;
  ufcImageUrl: string | null;
  mlbPlayerId: number | null;
  imageUrl: string | null;
  views: number;
  searches: number;
}

// ─── Avatar (real headshot, initials fallback) ────────────────────────────────

function headshotUrl(a: Athlete): string | null {
  if (a.nbaPlayerId) return `https://cdn.nba.com/headshots/nba/latest/1040x760/${a.nbaPlayerId}.png`;
  if (a.ufcImageUrl) return a.ufcImageUrl;
  if (a.mlbPlayerId) return `https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:67:current.png/w_213,q_auto:best/v1/people/${a.mlbPlayerId}/headshot/67/current`;
  if (a.imageUrl) return a.imageUrl;
  return null;
}

function initials(name: string): string {
  return name
    .split(/[\s-]+/)
    .filter((w) => /[A-Za-zÀ-ÿ]/.test(w))
    .slice(0, 2)
    .map((w) => w[0].toUpperCase())
    .join("");
}

function Avatar({ a }: { a: Athlete }) {
  const url = headshotUrl(a);
  return (
    <span className={styles.av}>
      {url ? (
        // eslint-disable-next-line @next/next/no-img-element
        <img
          src={url}
          alt={a.name}
          onError={(e) => { (e.currentTarget as HTMLImageElement).style.display = "none"; }}
        />
      ) : (
        initials(a.name)
      )}
    </span>
  );
}

// ─── Constants ────────────────────────────────────────────────────────────────

const RANGES = [
  { label: "24h", value: "24h" },
  { label: "7 days", value: "7d" },
  { label: "30 days", value: "30d" },
  { label: "1 year", value: "1y" },
  { label: "All time", value: "all" },
];

const SPORTS = ["All", "Basketball", "Baseball", "Soccer", "MMA", "Wrestling", "Racing", "Football", "Entertainment", "Other"];

const attention = (a: Athlete) => a.views + a.searches * 2;

// ─── Component ────────────────────────────────────────────────────────────────

export function SearchesClient({ views, searches, allSports, currentRange, currentSport }: Props) {
  const router = useRouter();
  const [view, setView] = useState<"combined" | "split">("combined");
  const [sort, setSort] = useState<"views" | "searches">("views");
  const [expanded, setExpanded] = useState(false);

  const availableSports = SPORTS.filter((s) => s === "All" || allSports.includes(s));

  // Merge the two already-fetched top lists into one athlete pool (both counts).
  const pool = useMemo<Athlete[]>(() => {
    const map = new Map<string, Athlete>();
    const upsert = (e: LeaderboardEntry, kind: "views" | "searches") => {
      let a = map.get(e.playerName);
      if (!a) {
        a = {
          name: e.playerName, sport: e.sport, setName: e.setName, slug: e.slug, setSlug: e.setSlug,
          nbaPlayerId: e.nbaPlayerId, ufcImageUrl: e.ufcImageUrl, mlbPlayerId: e.mlbPlayerId, imageUrl: e.imageUrl,
          views: 0, searches: 0,
        };
        map.set(e.playerName, a);
      }
      a[kind] = e.eventCount;
      if (!a.slug && e.slug) { a.slug = e.slug; a.setSlug = e.setSlug; a.setName = e.setName; a.sport = e.sport; }
    };
    views.forEach((e) => upsert(e, "views"));
    searches.forEach((e) => upsert(e, "searches"));
    return [...map.values()];
  }, [views, searches]);

  const sortedBy = (key: "views" | "searches", list: Athlete[]) =>
    [...list].sort((x, y) => y[key] - x[key] || attention(y) - attention(x) || x.name.localeCompare(y.name));

  const podium = useMemo(() => [...pool].sort((x, y) => attention(y) - attention(x) || y.views - x.views).slice(0, 3), [pool]);

  function navigate(range: string, sport: string | null) {
    const params = new URLSearchParams();
    params.set("range", range);
    if (sport) params.set("sport", sport);
    router.push(`/searches?${params.toString()}`);
  }

  const hrefFor = (a: Athlete) => (a.setSlug && a.slug ? `/sets/${a.setSlug}/athlete/${a.slug}` : null);

  return (
    <div className={`${styles.wrap} h-full overflow-y-auto`}>
      <div className="page-container" style={{ paddingTop: 40, paddingBottom: 90 }}>
        {/* Breadcrumb */}
        <div className={styles.crumb}>‹ <a href="/">Home</a></div>

        {/* Title */}
        <h1 className="page-title" style={{ margin: "14px 0 0" }}>Searches</h1>
        <p className={styles.sub}>
          What collectors are looking for on Checklist². Searched terms and athlete pages viewed, ranked together.
        </p>

        {/* Controls: time range · view toggle */}
        <div className={styles.controls}>
          <div className={styles.seg}>
            {RANGES.map((r) => {
              const on = currentRange === r.value;
              return (
                <button key={r.value} className={on ? `${styles.segBtn} ${styles.segOn}` : styles.segBtn} aria-pressed={on}
                  onClick={() => navigate(r.value, currentSport)}>
                  {r.label}
                </button>
              );
            })}
          </div>
          <div className={styles.rightCtl}>
            <div className={styles.seg}>
              <button className={view === "combined" ? `${styles.segBtn} ${styles.segOn}` : styles.segBtn} aria-pressed={view === "combined"}
                onClick={() => { setView("combined"); setExpanded(false); }}>Combined</button>
              <button className={view === "split" ? `${styles.segBtn} ${styles.segOn}` : styles.segBtn} aria-pressed={view === "split"}
                onClick={() => { setView("split"); setExpanded(false); }}>Side by side</button>
            </div>
          </div>
        </div>

        {/* Sport chips (server-filtered via URL) */}
        <div className={styles.chips}>
          {availableSports.map((sp) => {
            const on = sp === "All" ? !currentSport : currentSport === sp;
            return (
              <button key={sp} className={on ? `${styles.chip} ${styles.chipOn}` : styles.chip} aria-pressed={on}
                onClick={() => navigate(currentRange, sp === "All" ? null : sp)}>
                {sp}
              </button>
            );
          })}
        </div>

        {pool.length === 0 ? (
          <div className={styles.tbl} style={{ borderBottom: "1px solid var(--brand-fog)", marginTop: 30 }}>
            <div className={styles.empty}>No athletes for this range{currentSport ? ` in ${currentSport}` : ""} yet.</div>
          </div>
        ) : (
          <>
            {/* Podium */}
            <div className={styles.eyebrow} style={{ margin: "30px 0 12px" }}>Top 3 this period</div>
            <div className={styles.podium}>
              {podium.map((a, i) => {
                const href = hrefFor(a);
                const inner = (
                  <>
                    <div className={styles.podRk}>{i + 1}</div>
                    <Avatar a={a} />
                    <div style={{ minWidth: 0 }}>
                      <div className={styles.podNm}>{a.name}</div>
                      <div className={styles.podMeta}>{a.sport} · {a.setName}</div>
                      <div className={styles.podStats}>
                        <span><b>{a.views.toLocaleString()}</b> views</span>
                        <span><b>{a.searches.toLocaleString()}</b> searches</span>
                      </div>
                    </div>
                  </>
                );
                const cls = `${styles.pod}${i === 0 ? ` ${styles.podTop}` : ""}`;
                return href
                  ? <Link key={a.name} href={href} className={cls}>{inner}</Link>
                  : <div key={a.name} className={cls}>{inner}</div>;
              })}
            </div>

            {view === "combined" ? (
              <CombinedTable pool={pool} sort={sort} setSort={setSort} expanded={expanded} setExpanded={setExpanded}
                sortedBy={sortedBy} hrefFor={hrefFor} />
            ) : (
              <div className={styles.split}>
                <SplitColumn title="Most viewed" desc="Athlete pages opened" metric="views"
                  list={sortedBy("views", pool).filter((a) => a.views > 0).slice(0, expanded ? 999 : 10)} hrefFor={hrefFor} />
                <SplitColumn title="Most searched" desc="Terms typed into search" metric="searches"
                  list={sortedBy("searches", pool).filter((a) => a.searches > 0).slice(0, expanded ? 999 : 10)} hrefFor={hrefFor} />
              </div>
            )}

            {/* Hint */}
            <div className={styles.hint}>
              <b>Note</b>
              <span>
                {view === "combined"
                  ? "One ranking, two metrics — sorting swaps the emphasis instead of repeating a second list, so you can see who is both viewed and searched versus viewed but never typed."
                  : "Side by side keeps the two metrics separate — good for scanning one list, harder for spotting the athletes that appear in both."}
              </span>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

// ─── Combined table ───────────────────────────────────────────────────────────

function CombinedTable({
  pool, sort, setSort, expanded, setExpanded, sortedBy, hrefFor,
}: {
  pool: Athlete[];
  sort: "views" | "searches";
  setSort: (s: "views" | "searches") => void;
  expanded: boolean;
  setExpanded: (b: boolean) => void;
  sortedBy: (key: "views" | "searches", list: Athlete[]) => Athlete[];
  hrefFor: (a: Athlete) => string | null;
}) {
  const s = sortedBy(sort, pool);
  const max = Math.max(1, ...s.map((a) => (sort === "searches" ? a.searches : a.views)));
  const shown = expanded ? s : s.slice(0, 10);

  return (
    <>
      <div className={styles.eyebrow} style={{ margin: "0 0 12px" }}>
        Full ranking · {s.length} athletes · sorted by {sort}
      </div>
      <div className={styles.tbl}>
        <div className={styles.hd}>
          <span className={styles.hdCell} style={{ textAlign: "center" }}>#</span>
          <span className={styles.hdCell} />
          <span className={styles.hdCell}>Athlete</span>
          <span className={`${styles.hdCell} ${styles.cBar}`}>Attention</span>
          <button className={`${styles.srt}${sort === "views" ? ` ${styles.srtOn}` : ""}`} aria-pressed={sort === "views"}
            onClick={() => setSort("views")}>Views{sort === "views" ? " ▾" : ""}</button>
          <button className={`${styles.srt}${sort === "searches" ? ` ${styles.srtOn}` : ""}`} aria-pressed={sort === "searches"}
            onClick={() => setSort("searches")}>Searches{sort === "searches" ? " ▾" : ""}</button>
        </div>
        {shown.map((a, i) => {
          const v = sort === "searches" ? a.searches : a.views;
          const href = hrefFor(a);
          const inner = (
            <>
              <div className={styles.rowRk}>{i + 1}</div>
              <Avatar a={a} />
              <div className={styles.who}>
                <div className={styles.whoNm}>{a.name}</div>
                <div className={styles.whoMeta}><span className={styles.sp}>{a.sport}</span> · {a.setName}</div>
              </div>
              <div className={styles.cBar}>
                <div className={`${styles.bar}${sort === "searches" ? ` ${styles.barS}` : ""}`}>
                  <i style={{ width: `${Math.max(4, (v / max) * 100)}%` }} />
                </div>
              </div>
              <div className={`${styles.num}${a.views ? "" : ` ${styles.numZ}`}`}>{a.views ? a.views.toLocaleString() : "—"}</div>
              <div className={`${styles.num}${a.searches ? "" : ` ${styles.numZ}`}`}>{a.searches ? a.searches.toLocaleString() : "—"}</div>
            </>
          );
          const cls = `${styles.row}${i < 3 ? ` ${styles.rowTop}` : ""}`;
          return href
            ? <Link key={a.name} href={href} className={cls}>{inner}</Link>
            : <div key={a.name} className={cls}>{inner}</div>;
        })}
      </div>
      {s.length > 10 && (
        <div className={styles.more}>
          <button onClick={() => setExpanded(!expanded)}>
            {expanded ? "Show top 10 only" : `Show all ${s.length} athletes`}
          </button>
        </div>
      )}
    </>
  );
}

// ─── Split column ─────────────────────────────────────────────────────────────

function SplitColumn({
  title, desc, metric, list, hrefFor,
}: {
  title: string;
  desc: string;
  metric: "views" | "searches";
  list: Athlete[];
  hrefFor: (a: Athlete) => string | null;
}) {
  return (
    <div>
      <h2 className={styles.colH}>{title}</h2>
      <p className={styles.colP}>{desc}</p>
      <div className={styles.tbl} style={{ borderBottom: "1px solid var(--brand-fog)" }}>
        <div className={styles.hd}>
          <span className={styles.hdCell} style={{ textAlign: "center" }}>#</span>
          <span className={styles.hdCell} />
          <span className={styles.hdCell}>Athlete</span>
          <span className={styles.hdCell} style={{ textAlign: "right" }}>{metric}</span>
        </div>
        {list.length === 0 ? (
          <div className={styles.empty}>Nothing here yet.</div>
        ) : (
          list.map((a, i) => {
            const href = hrefFor(a);
            const inner = (
              <>
                <div className={styles.rowRk}>{i + 1}</div>
                <Avatar a={a} />
                <div className={styles.who}>
                  <div className={styles.whoNm}>{a.name}</div>
                  <div className={styles.whoMeta}><span className={styles.sp}>{a.sport}</span> · {a.setName}</div>
                </div>
                <div className={styles.num}>{a[metric].toLocaleString()}</div>
              </>
            );
            const cls = `${styles.row}${i < 3 ? ` ${styles.rowTop}` : ""}`;
            return href
              ? <Link key={a.name} href={href} className={cls}>{inner}</Link>
              : <div key={a.name} className={cls}>{inner}</div>;
          })
        )}
      </div>
    </div>
  );
}
