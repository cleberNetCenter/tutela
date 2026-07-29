import { test, expect } from "@playwright/test";

// Regressão (ARQ-4xx, Sprint 27): o modal de política de privacidade em
// /diagnostico ficava presente no DOM mas permanentemente invisível —
// `loadPrivacyPolicyContent()` (diagnostico.js) clona `.text-block` de
// /legal/politica-de-privacidade.html, que carrega a classe
// `.reveal-on-scroll` (opacity: 0 até um IntersectionObserver da página de
// ORIGEM adicionar `.visible`). O clone ia para o modal sem esse observer,
// então o texto nunca era revelado — inclusive o texto de consentimento que
// o backend passou a exigir na Sprint 26. Corrigido em c7a0ee6
// (`clone.classList.remove('reveal-on-scroll')`).
//
// Testes anteriores só verificavam presença no DOM (`toBeAttached`), nunca
// visibilidade real — por isso o bug passou despercebido. Este spec fixa
// visibilidade de fato (`toBeVisible` + opacity computado > 0), não só
// presença, para o elemento exato que causou o bug e para os elementos
// levantados na auditoria da Sprint 27 com o mesmo padrão (clone de
// conteúdo de um contexto com mecanismo de revelação para um contexto sem
// esse mecanismo).

async function answerDiagStep(page: import("@playwright/test").Page, step: number) {
  await page.locator(`.diag-step[data-step="${step}"] .diag-opt`).first().click();
  await page.locator(`.diag-step[data-step="${step}"] .diag-next-btn`).click();
}

test.describe("Modal de política de privacidade (/diagnostico) — visibilidade real do conteúdo clonado", () => {
  test("conteúdo clonado da política fica de fato visível (não só presente no DOM)", async ({ page }) => {
    await page.goto("/diagnostico.html");

    await answerDiagStep(page, 1);
    await answerDiagStep(page, 2);
    await answerDiagStep(page, 3);

    await page.locator("#openPrivacyModal").click();

    const modal = page.locator("#privacyModal");
    await expect(modal).toBeVisible();
    await expect(modal).toHaveAttribute("aria-hidden", "false");

    const content = page.locator("#privacyModalContent");
    // Espera o fetch de /legal/politica-de-privacidade.html + clone terminar
    // (loadPrivacyPolicyContent oculta #privacyModalStatus ao concluir).
    await expect(page.locator("#privacyModalStatus")).toBeHidden();

    const sections = content.locator(".text-block");
    await expect(sections.first()).toBeVisible();

    const sectionCount = await sections.count();
    expect(sectionCount).toBeGreaterThan(0);

    for (let i = 0; i < sectionCount; i++) {
      const section = sections.nth(i);
      await expect(section).toBeVisible();
      // A classe causadora do bug original: se `reveal-on-scroll` sobrevivesse
      // no clone (regressão), opacity computado seria 0 mesmo com
      // `toBeVisible()` potencialmente já passando por outros motivos de
      // layout — checagem explícita de opacity computado pega exatamente
      // essa classe de bug.
      await expect(section).not.toHaveClass(/reveal-on-scroll/);
      const opacity = await section.evaluate((el) => getComputedStyle(el).opacity);
      expect(Number(opacity)).toBeGreaterThan(0);
    }
  });
});

// Sanity permanente do mecanismo de origem (reveal-on-scroll + IntersectionObserver):
// não é o padrão do bug (aqui o clone não existe, o mecanismo roda no mesmo
// contexto que declarou o observer), mas garante que uma alteração futura no
// CSS/observer compartilhado (pages-consolidated.css, legal-shared.css,
// legal-animations.js) não regrida silenciosamente a página de origem — o
// que também quebraria o conteúdo clonado no modal, já que ele depende do
// mesmo HTML de origem.
test.describe("Página de origem (/legal/politica-de-privacidade) — reveal-on-scroll revela ao rolar", () => {
  test("seções reveal-on-scroll ficam visíveis após rolar até elas", async ({ page }) => {
    await page.goto("/legal/politica-de-privacidade.html");

    const section = page.locator(".text-block.reveal-on-scroll").nth(3);
    await section.scrollIntoViewIfNeeded();
    await expect(section).toHaveClass(/visible/);
    await expect(section).toBeVisible();

    const opacity = await section.evaluate((el) => getComputedStyle(el).opacity);
    expect(Number(opacity)).toBeGreaterThan(0);
  });
});
