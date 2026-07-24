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
