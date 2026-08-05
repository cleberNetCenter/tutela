import { test, expect, Page } from "@playwright/test";

// ARQ-604 — rede de regressão visual (lacuna registrada desde ARQ-301/Sprint 4;
// Sprint 9/ARQ-603 mudou UI de dropdown sem nenhuma captura). Cobre, no mínimo:
// home, um cluster de marca distinto (Ativos Digitais), uma página legal e o
// estado aberto de um dropdown — exatamente as áreas tocadas pela auditoria de
// contraste desta sprint (--color-text-muted, --text-3 do header/footer).
//
// Baseline (`--update-snapshots`) foi gerado ANTES das correções de cor desta
// sprint; a suíte foi rodada de novo DEPOIS das correções para revisão manual
// do diff (ver entrega da Sprint 10 em 16-architecture-backlog.md).

// As páginas legais (e outras seções) usam scroll-reveal via IntersectionObserver
// (.reveal-on-scroll/.legal-animate, ver legal-animations.js; .reveal na home,
// ver 06-design-system.md § Animações). Um screenshot de página inteira pode
// capturar seções ainda no estado "não revelado" dependendo do timing do
// observer durante o scroll interno do Playwright — isso é uma fonte de
// flakiness pré-existente do próprio site, não uma regressão desta sprint.
// Forçar o estado final "visível" antes de capturar neutraliza essa variável
// sem alterar nenhum CSS/JS de produção.
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

// Screenshots de página inteira (fullPage) em páginas com header `position:
// sticky` sofrem um artefato conhecido do Chromium/Playwright: a captura é
// feita em fatias (~altura do viewport) e recompostas, e a costura entre
// fatias pode gerar jitter de sub-pixel no anti-aliasing de texto sublinhado
// próximo à borda de uma fatia — não é uma diferença de cor real. Medido
// nesta sprint: ~0.16% dos pixels da página, concentrados em um único bloco
// de texto perto de y=720px (altura padrão do viewport). Uma regressão de
// cor real afetaria uma fração muito maior da página. Tolerância pequena
// (0.5%) absorve esse ruído sem mascarar uma regressão real.
const FULL_PAGE_OPTS = { fullPage: true, maxDiffPixelRatio: 0.005 } as const;

// ARQ-107 (Sprint 37): o banner de consentimento de cookies aparece em toda
// primeira visita (sem escolha registrada) e é fixed/bottom, cobrindo parte
// do viewport — introduziria diff nestes screenshots sem relação com o que
// cada suíte realmente testa. Pré-registrar uma recusa (via addInitScript,
// aplicado antes de qualquer script da página rodar) mantém o banner oculto
// sem depender de rede real ao Google (o comportamento do próprio banner é
// coberto por tests/cookie-consent.spec.ts).
async function presetCookieConsentRejected(page: Page) {
  await page.addInitScript(() => {
    localStorage.setItem("cookieConsent", JSON.stringify({ status: "rejected", timestamp: Date.now() }));
  });
}

test.describe("Regressão visual (ARQ-604)", () => {
  test.beforeEach(async ({ page }) => {
    await presetCookieConsentRejected(page);
  });

  test("Home: viewport completo", async ({ page }) => {
    await page.goto("/");
    await freezeScrollReveal(page);
    await expect(page).toHaveScreenshot("home-full.png", FULL_PAGE_OPTS);
  });

  test("Cluster Ativos Digitais: viewport completo", async ({ page }) => {
    await page.goto("/ativos-digitais/");
    await freezeScrollReveal(page);
    await expect(page).toHaveScreenshot("ativos-digitais-full.png", FULL_PAGE_OPTS);
  });

  test("Página legal (termos-de-uso): viewport completo", async ({ page }) => {
    await page.goto("/legal/termos-de-uso.html");
    await freezeScrollReveal(page);
    await expect(page).toHaveScreenshot("legal-termos-de-uso-full.png", FULL_PAGE_OPTS);
  });

  test("Footer: recorte (usa --text-3, tocado pela correção desta sprint)", async ({ page }) => {
    await page.goto("/");
    const footer = page.locator("footer.tdf, .tdf").first();
    await footer.scrollIntoViewIfNeeded();
    await expect(footer).toHaveScreenshot("footer.png");
  });

  test("Dropdown de navegação aberto: recorte do header", async ({ page }) => {
    await page.goto("/");
    const dropdown = page.locator(".nav-dropdown").first();
    await dropdown.hover();
    await expect(dropdown.locator(".nav-toggle")).toHaveAttribute("aria-expanded", "true");
    const header = page.locator(".header");
    await expect(header).toHaveScreenshot("dropdown-open-header.png");
  });
});

// ARQ-307 (Sprint 31) reduziu o padding-top do .hero e o padding de
// `main > section` em assets-digital.css, mas descobriu que essas 2 regras
// afetam 14 páginas (não só as 5 do cluster /ativos-digitais/*), sem
// baseline visual dedicada às 10 páginas de artigo extras. Sprint 32
// fecha essa lacuna: validado visualmente (screenshot manual, sem
// distorção) que as 10 páginas de /insights/ativos-digitais/*
// e /insights/prova-digital/* que carregam assets-digital.css
// (body.assets-page.assets-pillar-page) receberam a redução de
// espaçamento corretamente — ver 16-architecture-backlog.md (ARQ-308).
const INSIGHTS_ASSETS_DIGITAL_PAGES = [
  { slug: "compliance-lgpd", path: "/insights/ativos-digitais/compliance-lgpd/" },
  { slug: "custodia-ativos-digitais", path: "/insights/ativos-digitais/custodia-ativos-digitais/" },
  { slug: "marco-regulatorio", path: "/insights/ativos-digitais/marco-regulatorio/" },
  { slug: "sucessao-digital", path: "/insights/ativos-digitais/sucessao-digital/" },
  { slug: "cadeia-custodia-prova-digital", path: "/insights/prova-digital/cadeia-custodia-prova-digital/" },
  { slug: "hash-criptografico-temporalidade", path: "/insights/prova-digital/hash-criptografico-temporalidade/" },
  { slug: "ia-custodia-qualificada", path: "/insights/prova-digital/ia-custodia-qualificada/" },
  { slug: "integridade-tecnica-admissibilidade", path: "/insights/prova-digital/integridade-tecnica-admissibilidade/" },
  { slug: "producao-antecipada-prova-digital", path: "/insights/prova-digital/producao-antecipada-prova-digital/" },
  { slug: "prova-digital-processo-civil-brasileiro", path: "/insights/prova-digital/prova-digital-processo-civil-brasileiro/" },
];

test.describe("Regressão visual — artigos de insights afetados por assets-digital.css (ARQ-308)", () => {
  test.beforeEach(async ({ page }) => {
    await presetCookieConsentRejected(page);
  });

  for (const { slug, path } of INSIGHTS_ASSETS_DIGITAL_PAGES) {
    test(`${slug}: viewport completo`, async ({ page }) => {
      await page.goto(path);
      await freezeScrollReveal(page);
      await expect(page).toHaveScreenshot(`insights-${slug}-full.png`, FULL_PAGE_OPTS);
    });
  }
});
