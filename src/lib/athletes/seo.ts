import { cache } from "react";
import type { Metadata } from "next";
import { SITE_URL } from "@/lib/setSeo";
import { getAthleteBySlug, getAthletePage, type AthleteCore, type AthletePageData } from "./queries";
import { athleteHref, segmentToPageKind, type PageKind } from "./util";

// React-cache the loaders so generateMetadata and the page render (same request)
// share one DB read each, not two.
export const loadAthlete = cache(async (slug: string) => getAthleteBySlug(slug));
export const loadAthletePage = cache(async (core: AthleteCore) => getAthletePage(core));

/** Canonical absolute URL for a subject's master page. */
export function athleteUrl(core: AthleteCore): string {
  return `${SITE_URL}${athleteHref(core.pageKind, core.slug) ?? ""}`;
}

/** True when `segment` (e.g. "characters") is the route that serves this subject's
 * page_kind — so /characters/<slug> only renders characters, etc. */
export function matchesSegment(core: AthleteCore, segment: string): boolean {
  return segmentToPageKind(segment) === core.pageKind;
}

/** Thin pages (card_count < 3 AND set_count = 1) still render + link, but noindex. */
export function isThin(core: AthleteCore): boolean {
  return core.cardCount < 3 && core.setCount === 1;
}

function sportWord(core: AthleteCore): string {
  return core.sport === "Entertainment" ? "trading" : core.sport;
}

export function buildAthleteMetadata(core: AthleteCore, data?: AthletePageData): Metadata {
  const url = athleteUrl(core);
  const title = `${core.name} Cards — every ${sportWord(core)} card checklist | Checklist²`;

  const parts: string[] = [`${core.cardCount} cards across ${core.setCount} set${core.setCount === 1 ? "" : "s"}`];
  if (data) {
    if (data.stats.autographs > 0) parts.push(`${data.stats.autographs} autograph${data.stats.autographs === 1 ? "" : "s"}`);
    if (data.stats.ones > 0) parts.push(`${data.stats.ones} one-of-one${data.stats.ones === 1 ? "" : "s"}`);
    if (data.stats.rookieCards > 0) parts.push(`${data.stats.rookieCards} rookie card${data.stats.rookieCards === 1 ? "" : "s"}`);
  }
  const description = `${core.name} on Checklist²: ${parts.join(", ")}. The full checklist of every ${sportWord(core)} card across every set.`;

  const meta: Metadata = {
    title,
    description,
    alternates: { canonical: url },
    openGraph: { title, description, url, type: "profile", siteName: "Checklist²" },
    twitter: { card: "summary", title, description },
  };
  if (isThin(core)) meta.robots = { index: false, follow: true };
  return meta;
}

/** JSON-LD: a subject node (Person / Thing / SportsTeam) + a BreadcrumbList. */
export function athleteJsonLd(core: AthleteCore): object[] {
  const url = athleteUrl(core);
  const subjectType: Record<PageKind, string> = {
    player: "Person",
    person: "Person",
    character: "Thing",
    team: "SportsTeam",
    none: "Thing",
  };
  const subject: Record<string, unknown> = {
    "@context": "https://schema.org",
    "@type": subjectType[core.pageKind],
    name: core.name,
    url,
  };
  if (core.aliases.filter((a) => a !== core.name).length) {
    subject.alternateName = core.aliases.filter((a) => a !== core.name);
  }
  if (core.pageKind === "player" || core.pageKind === "team") {
    subject.sport = core.sport;
  }

  const breadcrumb = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: [
      { "@type": "ListItem", position: 1, name: "Home", item: SITE_URL },
      { "@type": "ListItem", position: 2, name: "Athletes", item: `${SITE_URL}/athletes` },
      { "@type": "ListItem", position: 3, name: core.name, item: url },
    ],
  };
  return [subject, breadcrumb];
}

/** Escape `<` so JSON-LD can't break out of the <script> tag. */
export function toJsonLd(obj: unknown): string {
  return JSON.stringify(obj).replace(/</g, "\\u003c");
}

export type { AthleteCore, AthletePageData };
