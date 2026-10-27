import type { MetadataRoute } from "next";
import { SITE_URL } from "@/lib/setSeo";

// Block training / bulk-scraping crawlers that cost a function invocation + a
// cache write per page across a ~34k-URL surface, while keeping real search and
// AI-search referral traffic (Google, Bing, OAI-SearchBot, PerplexityBot) allowed.
// AI referral is a named GA channel, so only training/bulk crawlers are blocked.
const BLOCKED_BOTS = [
  "GPTBot",
  "CCBot",
  "Bytespider",
  "PetalBot",
  "Amazonbot",
  "ClaudeBot",
  "anthropic-ai",
  "meta-externalagent",
];

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      // Named bulk/training crawlers: disallow the whole site.
      ...BLOCKED_BOTS.map((userAgent) => ({ userAgent, disallow: "/" })),
      // Everyone else (Googlebot, Bingbot, OAI-SearchBot, PerplexityBot, …):
      // allowed, except the dead legacy set subtrees.
      {
        userAgent: "*",
        allow: "/",
        disallow: ["/sets-v2/", "/sets-legacy/"],
      },
    ],
    sitemap: `${SITE_URL}/sitemap.xml`,
  };
}
