import { test, expect, type Browser, type Page, type BrowserContext } from "@playwright/test";

/**
 * Consent-gating regression test.
 *
 * Google Analytics (gtag, id G-3T45WWZ64Y) must never load until the visitor
 * accepts the "analytics" category. This suite records every outgoing request
 * and asserts no analytics host is hit — and no `_ga` cookie is set — until
 * (and only until) "Accept all" is clicked. It also honors Global Privacy
 * Control (the banner opens in its reject state) and verifies the gtag loader
 * is absent from the server-rendered HTML (loads post-hydration only).
 */

const TENNIS = "/sets/2026-topps-triumphant-tennis";
const GA_ID = "G-3T45WWZ64Y";
const ANALYTICS_HOST = /(?:^|\.)(?:googletagmanager\.com|google-analytics\.com|analytics\.google\.com)$/i;

/** Attach a request recorder to a page; returns the growing list of URLs. */
function recordRequests(page: Page): string[] {
  const urls: string[] = [];
  page.on("request", (r) => urls.push(r.url()));
  return urls;
}

/** URLs whose host matches a Google Analytics / Tag Manager host. */
function analyticsHits(urls: string[]): string[] {
  return urls.filter((u) => {
    try {
      return ANALYTICS_HOST.test(new URL(u).host);
    } catch {
      return false;
    }
  });
}

async function gaCookies(context: BrowserContext): Promise<string[]> {
  const cookies = await context.cookies();
  return cookies.filter((c) => c.name.startsWith("_ga")).map((c) => c.name);
}

async function readC2Consent(context: BrowserContext): Promise<Record<string, unknown> | null> {
  const cookie = (await context.cookies()).find((c) => c.name === "c2_consent");
  if (!cookie) return null;
  return JSON.parse(decodeURIComponent(cookie.value));
}

/** Dump the request log into the failure message so CI shows what fired. */
function withLog(message: string, urls: string[]): string {
  const hits = analyticsHits(urls);
  return `${message}\n--- analytics requests (${hits.length}) ---\n${hits.join("\n") || "(none)"}\n--- all requests (${urls.length}) ---\n${urls.join("\n")}`;
}

async function settle(page: Page): Promise<void> {
  // Let any post-hydration / afterInteractive scripts fire (or prove they don't).
  await page.waitForLoadState("networkidle").catch(() => {});
  await page.waitForTimeout(1500);
}

// ── (1) Fresh context, no choice: zero analytics requests, no _ga cookie ──────
test("no analytics before any consent choice", async ({ browser }) => {
  const context = await browser.newContext();
  const page = await context.newPage();
  const urls = recordRequests(page);

  await page.goto("/", { waitUntil: "domcontentloaded" });
  await settle(page);
  await page.goto(TENNIS, { waitUntil: "domcontentloaded" });
  await settle(page);

  expect(analyticsHits(urls), withLog("analytics loaded with no consent choice", urls)).toEqual([]);
  expect(await gaCookies(context)).toEqual([]);
  await context.close();
});

// ── (2) Reject all: still no analytics; c2_consent.analytics === false ────────
test("reject all keeps analytics off across navigations", async ({ browser }) => {
  const context = await browser.newContext();
  const page = await context.newPage();
  const urls = recordRequests(page);

  await page.goto("/", { waitUntil: "domcontentloaded" });
  const dialog = page.getByRole("dialog", { name: "Cookie consent" });
  await expect(dialog).toBeVisible();
  await page.getByRole("button", { name: "Reject all" }).click();

  await page.goto(TENNIS, { waitUntil: "domcontentloaded" });
  await settle(page);
  await page.goto("/sets", { waitUntil: "domcontentloaded" });
  await settle(page);

  expect(analyticsHits(urls), withLog("analytics loaded after Reject all", urls)).toEqual([]);
  expect(await gaCookies(context)).toEqual([]);

  const consent = await readC2Consent(context);
  expect(consent, "c2_consent cookie missing after Reject all").not.toBeNull();
  expect(consent!.analytics).toBe(false);
  await context.close();
});

// ── (3) Accept all: gtag loads, /g/collect fires, _ga cookie set ──────────────
test("accept all loads GA and fires a hit", async ({ browser }) => {
  const context = await browser.newContext();
  const page = await context.newPage();
  const urls = recordRequests(page);

  await page.goto("/", { waitUntil: "domcontentloaded" });
  await expect(page.getByRole("dialog", { name: "Cookie consent" })).toBeVisible();

  const gtagReq = page.waitForRequest(
    (r) => r.url().includes(`googletagmanager.com/gtag/js`) && r.url().includes(`id=${GA_ID}`),
    { timeout: 8000 },
  );
  const collectReq = page.waitForRequest((r) => /\/g\/collect(?:\?|$)/.test(r.url()), { timeout: 5000 });

  await page.getByRole("button", { name: "Accept all" }).click();

  await expect(gtagReq, withLog("gtag/js loader never requested after Accept all", urls)).resolves.toBeTruthy();
  await expect(collectReq, withLog("no /g/collect hit within 5s of Accept all", urls)).resolves.toBeTruthy();

  await expect
    .poll(async () => (await gaCookies(context)).length, { timeout: 3000 })
    .toBeGreaterThan(0);
  await context.close();
});

// ── (4) Global Privacy Control: banner opens in reject state; stays gated ─────
test("global privacy control defaults to reject", async ({ browser }) => {
  const context = await browser.newContext();
  await context.addInitScript(() => {
    Object.defineProperty(navigator, "globalPrivacyControl", { get: () => true, configurable: true });
  });
  const page = await context.newPage();
  const urls = recordRequests(page);

  await page.goto("/", { waitUntil: "domcontentloaded" });
  const dialog = page.getByRole("dialog", { name: "Cookie consent" });
  await expect(dialog).toBeVisible();

  // Reject state: opening Manage shows the Analytics toggle unchecked.
  await page.getByRole("button", { name: "Manage" }).click();
  await expect(page.getByRole("checkbox")).not.toBeChecked();

  // Case (1) assertions still hold after a page load under GPC.
  await page.goto(TENNIS, { waitUntil: "domcontentloaded" });
  await settle(page);
  expect(analyticsHits(urls), withLog("analytics loaded under GPC", urls)).toEqual([]);
  expect(await gaCookies(context)).toEqual([]);
  await context.close();
});

// ── Prerender: server HTML must not embed the gtag loader ─────────────────────
test("server-rendered HTML does not contain the gtag loader", async ({ request }) => {
  const res = await request.get("/");
  expect(res.ok()).toBeTruthy();
  const html = await res.text();
  expect(html).not.toContain("googletagmanager");
});
