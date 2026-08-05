import { test, expect, Page } from "@playwright/test";

// ARQ-301 — rede de regressão visual granular para a migração --ux-* → --ad-*.
//
// tests/visual-contrast.spec.ts (Sprint 10/ARQ-604) cobre "/ativos-digitais/"
// (public/ativos-digitais/index.html), que NÃO inclui o partial
// ativos-digitais-pillar-styles.html (confirmado via grep: só as 3 páginas
// de idioma do cluster incluem esse partial via SSI) — logo aquela baseline
// não cobre nenhum uso real de --ux-*. Este spec cobre as 3 páginas que de
// fato consomem --ux-* (pt/en/es), seção por seção, para isolar qualquer
// regressão a um bloco específico durante a migração token por token.
//
// Baseline (`--update-snapshots`) gerado ANTES da migração desta sprint.
// Re-executado DEPOIS da migração para revisão manual do diff.

const PAGES = [
  { slug: "pt", path: "/pt/ativos-digitais/" },
  { slug: "en", path: "/en/digital-assets/" },
  { slug: "es", path: "/es/activos-digitales/" },
];

// Mesmo racional de tests/visual-contrast.spec.ts: neutraliza o
// scroll-reveal (IntersectionObserver) para evitar flakiness de timing
// não relacionada à migração de tokens.
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

const OPTS = { maxDiffPixelRatio: 0.005 } as const;

// ARQ-107 (Sprint 37): banner de consentimento de cookies aparece em toda
// primeira visita e é fixed/bottom — pré-registrar uma recusa mantém o
// banner oculto nestes screenshots, sem depender de rede real ao Google.
// Comportamento do próprio banner é coberto por tests/cookie-consent.spec.ts.
async function presetCookieConsentRejected(page: Page) {
  await page.addInitScript(() => {
    localStorage.setItem("cookieConsent", JSON.stringify({ status: "rejected", timestamp: Date.now() }));
  });
}

test.describe("Regressão visual granular — migração --ux-*/--ad-* (ARQ-301)", () => {
  for (const { slug, path } of PAGES) {
    test.describe(`${slug}: ${path}`, () => {
      test.beforeEach(async ({ page }) => {
        await presetCookieConsentRejected(page);
        await page.goto(path);
        await freezeScrollReveal(page);
      });

      test(`${slug}: página completa`, async ({ page }) => {
        // Sprint 34: o timeout de 30000ms do assert abaixo já era intencional
        // (captura fullPage é mais pesada que os recortes de componente desta
        // suíte), mas o timeout padrão do teste em si (30000ms, herdado do
        // Playwright) começa a contar antes do goto/addStyleTag do
        // beforeEach — na prática o assert nunca podia usar seu próprio
        // orçamento inteiro. Confirmado via trace (ARQ-604/Sprint 34) que a
        // captura em si, sob `--workers=16`, pode legitimamente levar
        // ~24-27s (CPU disputada por 16 instâncias Chromium renderizando/
        // codificando PNG simultaneamente) sem nenhuma trava real da
        // página — daí o teste precisar de orçamento próprio maior que o
        // do assert.
        test.setTimeout(60000);
        await expect(page).toHaveScreenshot(`${slug}-full.png`, { fullPage: true, ...OPTS, timeout: 30000 });
      });

      test(`${slug}: hero (page-header-inner, fundo escuro)`, async ({ page }) => {
        const hero = page.locator(".page-header-inner");
        await expect(hero).toHaveScreenshot(`${slug}-hero.png`, OPTS);
      });

      test(`${slug}: stats-grid (stat-card)`, async ({ page }) => {
        const stats = page.locator(".stats-grid");
        await expect(stats).toHaveScreenshot(`${slug}-stats-grid.png`, OPTS);
      });

      test(`${slug}: grid-2 (card + card-danger)`, async ({ page }) => {
        const grid = page.locator(".grid-2").first();
        await expect(grid).toHaveScreenshot(`${slug}-grid-2.png`, OPTS);
      });

      test(`${slug}: steps`, async ({ page }) => {
        const steps = page.locator(".steps");
        await expect(steps).toHaveScreenshot(`${slug}-steps.png`, OPTS);
      });

      test(`${slug}: checklist`, async ({ page }) => {
        const checklist = page.locator(".checklist");
        await expect(checklist).toHaveScreenshot(`${slug}-checklist.png`, OPTS);
      });

      test(`${slug}: whitepaper-container (tipografia h2/h3/p, fundo claro)`, async ({ page }) => {
        // Sprint 34: mesmo racional do teste "página completa" acima — o
        // timeout: 30000 do assert é maior que o de qualquer outro recorte
        // desta suíte (bloco de texto grande), mas ficava sem efeito real
        // preso ao timeout padrão de teste, também 30000ms.
        test.setTimeout(60000);
        const container = page.locator(".whitepaper-container");
        await expect(container).toHaveScreenshot(`${slug}-whitepaper-container.png`, {
          ...OPTS,
          maxDiffPixelRatio: 0.01,
          timeout: 30000,
        });
      });

      test(`${slug}: insight-cta-inner (CTA final, fundo escuro)`, async ({ page }) => {
        const cta = page.locator(".insight-cta-inner");
        await expect(cta).toHaveScreenshot(`${slug}-insight-cta.png`, OPTS);
      });
    });
  }
});
