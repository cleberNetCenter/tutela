import { defineConfig, devices } from "@playwright/test";

const PORT = 8080;

export default defineConfig({
  testDir: "./tests",
  fullyParallel: true,
  retries: 0,
  reporter: [["list"]],
  // Fontes agora são servidas localmente pelo próprio servidor de teste
  // (ARQ-604, antes vinham de fonts.googleapis.com) — mais I/O de disco
  // local por página sob a concorrência default do Playwright. 10s (em vez
  // do default de 5s) dá margem para `waiting for fonts to load` sem
  // mascarar timeouts genuínos (o timeout de teste continua 30s).
  expect: { timeout: 10000 },
  use: {
    baseURL: `http://localhost:${PORT}`,
    trace: "retain-on-failure",
  },
  webServer: {
    command: `node tests/support/ssi-server.js`,
    port: PORT,
    reuseExistingServer: !process.env.CI,
    env: { PORT: String(PORT) },
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],
});
