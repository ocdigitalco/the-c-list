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
};

export default nextConfig;
