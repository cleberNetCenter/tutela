import { test, expect } from "@playwright/test";

const DEPRECATED_CSS = [
  "/assets/css/dropdown-menu.css",
  "/assets/css/pages/ativos-digitais-pillar-styles.css",
  "/assets/css/pages/fundamento-juridico.css",
  "/assets/css/pages/politica-de-privacidade.css",
  "/assets/css/pages/preservacao-probatoria-digital.css",
  "/assets/css/pages/termos-de-custodia.css",
];

test.describe("Regressão Sprint 1 (ARQ-402) e Sprint 2 (ARQ-404/ARQ-503)", () => {
  test("página legal (termos-de-uso) carrega com CSS ativo, sem <link> para CSS deprecated (ARQ-404)", async ({
    page,
  }) => {
    const response = await page.goto("/legal/termos-de-uso.html");
    expect(response?.status()).toBe(200);

    const hrefs = await page.locator('link[rel="stylesheet"]').evaluateAll((links) =>
      links.map((l) => (l as HTMLLinkElement).getAttribute("href") || "")
    );

    for (const deprecated of DEPRECATED_CSS) {
      expect(hrefs.some((href) => href.includes(deprecated))).toBe(false);
    }
    expect(hrefs.some((href) => href.includes("/assets/css/styles-header-final.css"))).toBe(true);
    expect(hrefs.some((href) => href.includes("/assets/css/legal-shared.css"))).toBe(true);
  });

  test("exatamente 1 par de preconnect de fontes por página, injetado 1x (ARQ-503)", async ({ page }) => {
    await page.goto("/");
    await page.waitForFunction(() => document.getElementById("global-fonts-loaded") !== null);

    const preconnectHrefs = await page
      .locator('link[rel="preconnect"]')
      .evaluateAll((links) => links.map((l) => (l as HTMLLinkElement).href));

    const fontsGoogleapis = preconnectHrefs.filter((href) => href.includes("fonts.googleapis.com"));
    const fontsGstatic = preconnectHrefs.filter((href) => href.includes("fonts.gstatic.com"));

    expect(fontsGoogleapis).toHaveLength(1);
    expect(fontsGstatic).toHaveLength(1);
  });

  test("isLegalPage() detecta página legal só pela classe, sem os IDs vestigiais removidos (ARQ-402)", async ({
    page,
  }) => {
    await page.goto("/legal/termos-de-uso.html");
    await expect(page.locator("body")).toHaveClass(/legal-page/);
    await page.waitForFunction(() => (window as any).I18N !== undefined);
    const isLegalOnLegalPage = await page.evaluate(() => (window as any).I18N.isLegalPage());
    expect(isLegalOnLegalPage).toBe(true);

    await page.goto("/");
    await page.waitForFunction(() => (window as any).I18N !== undefined);
    const isLegalOnHome = await page.evaluate(() => (window as any).I18N.isLegalPage());
    expect(isLegalOnHome).toBe(false);
  });
});
