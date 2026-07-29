import { test, expect } from "@playwright/test";

// Regressão: aviso "conteúdo disponível só em português" (#legal-lang-notice,
// i18n.js showLegalPageNoticeIfNeeded()) depende de DOIS marcadores presentes
// ao mesmo tempo: body.legal-page (isLegalPage()) e um elemento com classe
// "main" no DOM (document.querySelector(".main"), ponto de inserção do aviso).
//
// 5 dos 10 artigos de insights (4 em insights/ativos-digitais/*, 1 em
// insights/prova-digital/ia-custodia-qualificada/) tinham <body> e <main>
// sem nenhuma classe — o clique em EN/ES não fazia nada visível: sem aviso,
// sem tradução de corpo de artigo (nenhuma página do site traduz o corpo,
// só o chrome via data-i18n). Corrigido alinhando esses 5 arquivos à mesma
// convenção já usada pelos 5 artigos irmãos que funcionavam
// (body: "legal-page page-insight ..."; main: "main main--hero-top legal-page").
//
// Este spec fixa o comportamento esperado: com idioma pt-BR (padrão),
// nenhum aviso aparece; ao trocar para EN/ES, o aviso aparece em TODOS os
// artigos reais de insights (evita que um artigo novo repita a omissão).

const ARTICLES = [
  "/insights/prova-digital/cadeia-custodia-prova-digital/",
  "/insights/prova-digital/producao-antecipada-prova-digital/",
  "/insights/prova-digital/prova-digital-processo-civil-brasileiro/",
  "/insights/prova-digital/hash-criptografico-temporalidade/",
  "/insights/prova-digital/integridade-tecnica-admissibilidade/",
  "/insights/prova-digital/ia-custodia-qualificada/",
  "/insights/ativos-digitais/sucessao-digital/",
  "/insights/ativos-digitais/marco-regulatorio/",
  "/insights/ativos-digitais/custodia-ativos-digitais/",
  "/insights/ativos-digitais/compliance-lgpd/",
  // hubs de cluster (têm body.legal-page, mesmo critério dos artigos)
  "/insights/prova-digital/",
  "/insights/ativos-digitais/",
  // hub geral — corrigido na Sprint 12 (faltava legal-page em <body>, só
  // <main> tinha; ver commit da correção para o detalhe de CSS neutralizado
  // em insights-pilar.css para não regredir a largura dos títulos td-*)
  "/insights/",
];

test.describe("Aviso de idioma PT-only em artigos de insights", () => {
  test.use({ locale: "pt-BR" });

  for (const path of ARTICLES) {
    test(`${path}: sem aviso em pt, aviso aparece ao trocar para EN`, async ({ page }) => {
      await page.goto(path);
      await expect(page.locator("#legal-lang-notice")).toHaveCount(0);

      await page.click('.lang-switch .lang-flag[data-lang="en"]');
      const notice = page.locator("#legal-lang-notice");
      await expect(notice).toBeVisible();
      await expect(notice).toContainText("Portuguese");
    });
  }
});

// insights/ativos-digitais/index.html não incluía partials/scripts.html —
// i18n.js (e demais scripts globais) nunca carregavam nessa página, então o
// clique em qualquer bandeira de idioma não fazia absolutamente nada (sem
// erro visível). Cobre também /insights/ (hub geral) — a troca de idioma do
// chrome deve funcionar sem erro de console, independente do aviso PT-only
// (coberto separadamente no describe acima).
test.describe("Troca de idioma funciona no chrome (nav) de todas as páginas de insights", () => {
  test.use({ locale: "pt-BR" });

  for (const path of ["/insights/ativos-digitais/", "/insights/"]) {
    test(`${path}: clicar em EN traduz a nav e não gera erro de console`, async ({ page }) => {
      const consoleErrors: string[] = [];
      page.on("console", (msg) => {
        if (msg.type() === "error") consoleErrors.push(msg.text());
      });
      page.on("pageerror", (err) => consoleErrors.push(err.message));

      await page.goto(path);
      await expect(page.locator(".nav-link").first()).toHaveText("Início");

      await page.click('.lang-switch .lang-flag[data-lang="en"]');
      await expect(page.locator(".nav-link").first()).toHaveText("Home");
      await expect(page.locator('.lang-switch .lang-flag[data-lang="en"]')).toHaveClass(/active/);

      expect(consoleErrors).toEqual([]);
    });
  }
});

// governo.html carregava um segundo script de i18n inline, duplicado e
// quebrado (fetch em `/assets/i18n/${lang}.json`, caminho inexistente — os
// arquivos reais estão em `/assets/lang/`), que falhava silenciosamente em
// toda carga da página (só console.error). empresas.html e pessoas.html
// tinham um resquício mais grave da mesma limpeza incompleta: o script
// duplicado tinha sido "removido" só no comentário — o corpo da função
// (`el.textContent = value; ... window.addEventListener('storage', ...)`)
// continuou fora de qualquer tag <script>, renderizando como texto visível
// no rodapé da página. Sprint 28 removeu os três por completo, mantendo só
// o carregamento padrão de i18n.js via partials/scripts.html.
test.describe("governo: sem script de i18n duplicado/quebrado", () => {
  test.use({ locale: "pt-BR" });

  for (const path of ["/governo.html"]) {
    test(`${path}: troca de idioma sem erro de console, sem texto de script órfão no corpo`, async ({ page }) => {
      const consoleErrors: string[] = [];
      page.on("console", (msg) => {
        if (msg.type() === "error") consoleErrors.push(msg.text());
      });
      page.on("pageerror", (err) => consoleErrors.push(err.message));

      await page.goto(path);
      await page.click('.lang-switch .lang-flag[data-lang="en"]');
      await expect(page.locator(".nav-link").first()).toHaveText("Home");

      expect(consoleErrors).toEqual([]);

      const bodyText = await page.locator("body").innerText();
      expect(bodyText).not.toContain("el.textContent = value");
      expect(bodyText).not.toContain("addEventListener('storage'");
    });
  }
});

// ARQ-607 (Sprint 27) registrou a tradução do rodapé (footer.trademarkNotice)
// como pendente em en/es — publicada nesta sprint. Fixa o texto exato
// aprovado nas 3 línguas, no rodapé compartilhado (partials/footer.html).
test.describe("Rodapé: nota de marca (INPI) traduzida nas 3 línguas", () => {
  test.use({ locale: "pt-BR" });

  const EXPECTED: Record<string, string> = {
    pt: "Tutela Digital™ – Marca em processo de registro no INPI.",
    en: "Tutela Digital™ – Trademark application pending with INPI (Brazil's National Institute of Industrial Property).",
    es: "Tutela Digital™ – Marca en proceso de registro ante el INPI (Instituto Nacional de la Propiedad Industrial de Brasil).",
  };

  for (const lang of ["en", "es"] as const) {
    test(`troca para ${lang} exibe o texto aprovado, sem chave crua`, async ({ page }) => {
      await page.goto("/governo.html");
      await page.click(`.lang-switch .lang-flag[data-lang="${lang}"]`);
      const notice = page.locator('[data-i18n="footer.trademarkNotice"]');
      await expect(notice).toHaveText(EXPECTED[lang]);
      await expect(notice).not.toHaveText("footer.trademarkNotice");
    });
  }

  test("pt-BR (padrão) exibe o texto original", async ({ page }) => {
    await page.goto("/governo.html");
    const notice = page.locator('[data-i18n="footer.trademarkNotice"]');
    await expect(notice).toHaveText(EXPECTED.pt);
  });
});
