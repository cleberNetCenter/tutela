import { test, expect, Page } from "@playwright/test";

// ARQ-107 (docs/architecture/16-architecture-backlog.md) — banner de
// consentimento de cookies (CMP), opt-in estrito, categoria única
// ("aceitar analytics" sim/não), persistência de 12 meses.
//
// Sprint 37: GA deixou de ser um snippet inline duplicado em 16 páginas
// (mesmo ID G-KXVB267PYJ) e passou a ser centralizado em
// assets/js/consent.js, incluído via partials/scripts.html — logo cobrindo
// as 37 páginas reais do site (exceto o stub de redirect puro
// insights/ativos-digitais/o-que-sao-ativos-digitais/, que não carrega
// scripts.html nem precisa de analytics). O gate de consentimento garante
// que essa centralização não passou a disparar GA sem consentimento em
// páginas que antes não tinham GA algum.
//
// O teste mais importante deste arquivo é "nenhuma requisição ao Google
// antes da interação" — é a prova técnica de que o opt-in é estrito
// (nenhuma chamada de rede a googletagmanager.com/google-analytics.com
// antes do aceite), não só uma checagem visual do banner.

const GA_URL_PATTERN = /googletagmanager\.com|google-analytics\.com/;

// 1 página por cluster + pelo menos 2 páginas que, antes desta sprint,
// não tinham GA (ver Sprint 36: só 16 das 43 páginas tinham o snippet).
const PAGES = {
  home: "/",
  ativosDigitais: "/ativos-digitais/", // cluster ativos-digitais; não tinha GA antes
  legal: "/legal/termos-de-uso.html", // cluster legal; já tinha GA antes
  insights: "/insights/ativos-digitais/marco-regulatorio/", // cluster insights; não tinha GA antes
};

const PREVIOUSLY_WITHOUT_GA = [PAGES.ativosDigitais, PAGES.insights];

async function trackGARequests(page: Page) {
  const requests: string[] = [];
  await page.route(GA_URL_PATTERN, (route) => {
    requests.push(route.request().url());
    route.fulfill({ status: 200, contentType: "application/javascript", body: "" });
  });
  return requests;
}

test.describe("Banner de consentimento de cookies (ARQ-107)", () => {
  // Cada teste roda em um contexto de browser isolado (padrão do
  // Playwright) — localStorage já começa vazio, sem precisar de limpeza
  // manual. Importante: NÃO usar addInitScript para "limpar" storage aqui,
  // porque ele reexecutaria a cada navegação, inclusive em page.reload() —
  // apagaria exatamente o consentimento que os testes de persistência
  // acabaram de gravar antes de recarregar.

  for (const [cluster, url] of Object.entries(PAGES)) {
    test(`opt-in estrito: nenhuma requisição ao Google antes da interação (${cluster})`, async ({ page }) => {
      const gaRequests = await trackGARequests(page);

      await page.goto(url);
      await page.waitForLoadState("networkidle");
      // margem extra: garante que nenhum carregamento assíncrono tardio
      // dispara a chamada fora da janela de "networkidle"
      await page.waitForTimeout(500);

      expect(
        gaRequests,
        `requisição ao Google detectada antes de qualquer interação com o banner em ${url}`,
      ).toEqual([]);

      const banner = page.locator("#cookieBanner");
      await expect(banner).toBeVisible();
    });
  }

  test("banner visível na primeira visita (nenhuma escolha registrada)", async ({ page }) => {
    await page.goto(PAGES.home);
    await expect(page.locator("#cookieBanner")).toBeVisible();
    await expect(page.locator("#cookieBannerAccept")).toBeVisible();
    await expect(page.locator("#cookieBannerDecline")).toBeVisible();
  });

  test("skip-link continua sendo o primeiro elemento focável", async ({ page }) => {
    await page.goto(PAGES.home);
    await page.keyboard.press("Tab");
    const focused = await page.evaluate(() => document.activeElement?.className);
    expect(focused).toContain("skip-link");
  });

  test("aceitar: registra escolha, injeta/dispara GA e some o banner", async ({ page }) => {
    const gaRequests = await trackGARequests(page);

    await page.goto(PAGES.home);
    await expect(page.locator("#cookieBanner")).toBeVisible();

    const gaRequestPromise = page.waitForRequest(GA_URL_PATTERN);
    await page.click("#cookieBannerAccept");
    await gaRequestPromise;

    expect(gaRequests.length).toBeGreaterThan(0);
    await expect(page.locator("#cookieBanner")).toBeHidden();

    const consent = await page.evaluate(() => localStorage.getItem("cookieConsent"));
    expect(consent).not.toBeNull();
    const parsed = JSON.parse(consent as string);
    expect(parsed.status).toBe("accepted");
    expect(typeof parsed.timestamp).toBe("number");
  });

  test("recusar: registra escolha, GA nunca carrega e o banner some", async ({ page }) => {
    const gaRequests = await trackGARequests(page);

    await page.goto(PAGES.home);
    await expect(page.locator("#cookieBanner")).toBeVisible();

    await page.click("#cookieBannerDecline");
    await page.waitForTimeout(500);

    expect(gaRequests).toEqual([]);
    await expect(page.locator("#cookieBanner")).toBeHidden();

    const consent = await page.evaluate(() => localStorage.getItem("cookieConsent"));
    const parsed = JSON.parse(consent as string);
    expect(parsed.status).toBe("rejected");
  });

  test("escolha 'aceitar' persiste entre reloads: banner some e GA continua carregando", async ({ page }) => {
    const gaRequests = await trackGARequests(page);

    await page.goto(PAGES.home);
    await page.click("#cookieBannerAccept");
    await page.waitForTimeout(300);

    await page.reload();
    await page.waitForLoadState("networkidle");

    await expect(page.locator("#cookieBanner")).toBeHidden();
    expect(gaRequests.length).toBeGreaterThan(0); // recarregou GA na nova página, sem novo prompt
  });

  test("escolha 'recusar' persiste entre reloads: banner continua ausente e GA nunca carrega", async ({ page }) => {
    const gaRequests = await trackGARequests(page);

    await page.goto(PAGES.home);
    await page.click("#cookieBannerDecline");
    await page.waitForTimeout(300);

    await page.reload();
    await page.waitForLoadState("networkidle");
    await page.waitForTimeout(500);

    await expect(page.locator("#cookieBanner")).toBeHidden();
    expect(gaRequests).toEqual([]);
  });

  test("escolha expirada (>12 meses) faz o banner reaparecer e não carrega GA sozinho", async ({ page }) => {
    const gaRequests = await trackGARequests(page);

    await page.goto(PAGES.home);
    const THIRTEEN_MONTHS_MS = 396 * 24 * 60 * 60 * 1000;
    await page.evaluate((ageMs) => {
      localStorage.setItem(
        "cookieConsent",
        JSON.stringify({ status: "accepted", timestamp: Date.now() - ageMs }),
      );
    }, THIRTEEN_MONTHS_MS);

    await page.reload();
    await page.waitForLoadState("networkidle");

    await expect(page.locator("#cookieBanner")).toBeVisible();
    expect(gaRequests).toEqual([]); // consentimento expirado não é válido: sem GA até novo aceite
  });

  for (const url of PREVIOUSLY_WITHOUT_GA) {
    test(`nova cobertura: ${url} (antes sem GA) respeita o opt-in e carrega GA só após aceite`, async ({ page }) => {
      const gaRequests = await trackGARequests(page);

      await page.goto(url);
      await page.waitForLoadState("networkidle");
      expect(gaRequests).toEqual([]);

      const gaRequestPromise = page.waitForRequest(GA_URL_PATTERN);
      await page.click("#cookieBannerAccept");
      await gaRequestPromise;
      expect(gaRequests.length).toBeGreaterThan(0);
    });
  }

  test("página de redirect puro (sem scripts.html) não tem banner nem GA", async ({ page }) => {
    const gaRequests = await trackGARequests(page);
    await page.goto("/insights/ativos-digitais/o-que-sao-ativos-digitais/", { waitUntil: "domcontentloaded" });
    expect(await page.locator("#cookieBanner").count()).toBe(0);
    expect(gaRequests).toEqual([]);
  });

  test("texto do banner traduz nos 3 idiomas suportados", async ({ page }) => {
    const messages: Record<string, string> = {
      pt: "Usamos cookies de análise",
      en: "We use analytics cookies",
      es: "Usamos cookies de análisis",
    };
    for (const [lang, expectedSubstring] of Object.entries(messages)) {
      await page.addInitScript((l) => localStorage.setItem("tutela_lang", l), lang);
      await page.goto(PAGES.home);
      await expect(page.locator(".cookie-banner-text")).toContainText(expectedSubstring);
    }
  });

  test("banner traduz mesmo em página legal com idioma != pt (corpo permanece em pt)", async ({ page }) => {
    await page.addInitScript(() => localStorage.setItem("tutela_lang", "en"));
    await page.goto(PAGES.legal);
    await expect(page.locator(".cookie-banner-text")).toContainText("We use analytics cookies");
    await expect(page.locator("#cookieBannerAccept")).toHaveText("Accept");
  });
});
