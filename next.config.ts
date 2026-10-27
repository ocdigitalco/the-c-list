import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  serverExternalPackages: ["better-sqlite3"],
  // Belt-and-suspenders: the card-gallery runtime now reads a static build-time
  // manifest instead of scanning public/sets/cards/** via fs (see
  // scripts/generate-card-gallery-manifest.ts + src/lib/cardGallery.ts), which
  // is what actually stops @vercel/nft from tracing the image tree. This
  // exclusion guarantees the (multi-hundred-MB) card images can never be traced
  // into any serverless function even if a future fs read reintroduces the path
  // — keeping the sets/[id] function under Vercel's 250MB limit. The images are
  // served as static assets by the CDN, so functions never need them on disk.
  outputFileTracingExcludes: {
    "*": ["public/sets/cards/**"],
    "/sets/[id]": ["public/sets/cards/**"],
  },
  // The legacy per-set player routes are retired in favour of the canonical
  // athlete pages (Stage 2). Nothing links to them and `/players/:id` was a
  // per-set integer with no canonical target, so both 301 to the new index.
  // Static config redirects cost zero function invocations.
  async redirects() {
    return [
      { source: "/players", destination: "/athletes", statusCode: 301 },
      { source: "/players/:id", destination: "/athletes", statusCode: 301 },
    ];
  },
};

export default nextConfig;
