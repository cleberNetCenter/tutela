import { test, expect, Page } from "@playwright/test";

// ARQ-303 (docs/architecture/16-architecture-backlog.md) — tokenização de
// --radius-*/--shadow-*. Cobertura por cluster de página onde cards/CTAs/
// botões (elementos que tipicamente usam border-radius/box-shadow) aparecem:
// home, cluster Ativos Digitais, página legal, hub de Insights.
//
// Baseline gerado ANTES de qualquer migração de literal para var(); a suíte
// é rodada de novo DEPOIS de cada lote de migração para revisão manual do
// diff (ver entrega da Sprint 13 em 16-architecture-backlog.md).

async function freezeScrollReveal(page: Page) {
  await page.addStyleTag({
    content: `
      .reveal, .reveal-on-scroll, .legal-animate,
      .assets-page .reveal {
        opacity: 1 !important;
        transform: none !important;
        transition: none !important;
      }
    `,
  });
}

const FULL_PAGE_OPTS = { fullPage: true, maxDiffPixelRatio: 0.005 } as const;

test.describe("Regressão visual — tokenização --radius-*/--shadow-* (ARQ-303)", () => {
  test("Home: viewport completo", async ({ page }) => {
    await page.goto("/");
    await freezeScrollReveal(page);
    await expect(page).toHaveScreenshot("radius-shadow-home-full.png", FULL_PAGE_OPTS);
  });

  test("Cluster Ativos Digitais: viewport completo", async ({ page }) => {
    await page.goto("/ativos-digitais/");
    await freezeScrollReveal(page);
    await expect(page).toHaveScreenshot("radius-shadow-ativos-digitais-full.png", FULL_PAGE_OPTS);
  });

  test("Página legal (termos-de-uso): viewport completo", async ({ page }) => {
    await page.goto("/legal/termos-de-uso.html");
    await freezeScrollReveal(page);
    await expect(page).toHaveScreenshot("radius-shadow-legal-termos-de-uso-full.png", FULL_PAGE_OPTS);
  });

  test("Insights (hub geral): viewport completo", async ({ page }) => {
    await page.goto("/insights/");
    await freezeScrollReveal(page);
    await expect(page).toHaveScreenshot("radius-shadow-insights-full.png", FULL_PAGE_OPTS);
  });
});
