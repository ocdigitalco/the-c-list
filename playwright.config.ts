import { defineConfig, devices } from "@playwright/test";

/**
 * Consent-gating regression suite. Runs against a production build
 * (`npm run build && npm start`) on localhost so the prerendered HTML and the
 * post-hydration gtag loader behave exactly as in production.
 */
const PORT = Number(process.env.PORT || 3100);
const BASE_URL = `http://localhost:${PORT}`;

export default defineConfig({
  testDir: "./tests",
  fullyParallel: false,
  workers: 1,
  retries: 0,
  timeout: 60_000,
  reporter: [["list"]],
  use: {
    baseURL: BASE_URL,
    trace: "retain-on-failure",
  },
  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
  ],
  webServer: {
    command: `npm run build && npm start -- -p ${PORT}`,
    url: BASE_URL,
    timeout: 300_000,
    reuseExistingServer: !process.env.CI,
    stdout: "pipe",
    stderr: "pipe",
  },
});
