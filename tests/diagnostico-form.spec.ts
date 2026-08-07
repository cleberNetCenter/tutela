import { test, expect } from "@playwright/test";

// Regressão (ARQ-101, Sprint 29): enviar() (diagnostico.js) não checava
// response.ok — qualquer resposta HTTP do backend, incluindo erro (4xx/5xx,
// como o 400 que a Sprint 26 passou a retornar para submissão sem
// consentimento), era tratada como sucesso e renderizava o card de
// resultado. Corrigido verificando response.ok antes de renderizar,
// exibindo o mesmo alert() de erro já usado no formulário para outras
// falhas (fetch de rede, validação incompleta).
//
// grecaptcha real não carrega neste ambiente de teste (script externo do
// Google) — o botão de envio fica sempre disabled porque
// verificarEstadoBotao() exige captcha preenchido. Isso é só uma trava de
// UI: enviar() em si não valida o captcha, então os testes chamam
// enviar() diretamente via page.evaluate(), o mesmo caminho de código que
// o clique no botão dispararia.

async function answerDiagStep(page: import("@playwright/test").Page, step: number) {
  await page.locator(`.diag-step[data-step="${step}"] .diag-opt`).first().click();
  await page.locator(`.diag-step[data-step="${step}"] .diag-next-btn`).click();
}

async function preencherStep4(page: import("@playwright/test").Page) {
  await answerDiagStep(page, 1);
  await answerDiagStep(page, 2);
  await answerDiagStep(page, 3);

  await page.locator("#nome").fill("Ana Teste");
  await page.locator("#email").fill("ana@example.com");
  await page.locator("#consentimento").evaluate((el: HTMLInputElement) => {
    el.checked = true;
    el.dispatchEvent(new Event("change", { bubbles: true }));
  });
}

// Sprint 35 (estabilização de flake, ARQ-101): sob `--workers=16` os 3
// testes deste describe reproduziram "Test timeout of 30000ms exceeded" com
// taxa significativa (10/20 numa bateria dedicada). Trace ação-por-ação
// (call@14, clique em `.diag-next-btn` do passo 1) mostrou "element is
// visible, enabled and stable" resolvendo em ~15ms — não há repetição de
// "waiting for element to stop moving", ou seja, não é a mesma race de
// scroll da Sprint 33 (`waitForScrollSettled`, reaproveitado em
// content-visibility.spec.ts) atingindo um teste que não usa o helper: o
// tempo é consumido antes disso, na resolução do próprio locator via CDP
// (814ms só para resolver `.diag-next-btn` nesse exemplo) e no `page.goto`
// inicial (8s completos numa das reproduções). Hipótese descartada com
// evidência: content-visibility.spec.ts JÁ usa `waitForScrollSettled()` e
// falhou na mesma bateria a uma taxa igual ou maior (16/20), o que não
// seria esperado se a causa fosse a mesma race que o helper corrige — o
// helper, quando chamado, resolve rápido (169-307ms) nos traces
// inspecionados. Causa real: goto + 6 cliques do wizard + 2 preenchimentos
// somam, sob disputa real de CPU (16 processos Chromium), mais que os
// 30000ms padrão do teste — mesmo padrão da Sprint 34
// (visual-design-tokens.spec.ts): o timeout do teste como um todo começa a
// contar antes das ações que ele precisa orçar, e nunca sobra tempo para a
// asserção final rodar seu próprio timeout de retry. Corrigido dando
// orçamento maior ao teste, não à asserção.
test.describe("Formulário de diagnóstico — tratamento de erro do fetch (ARQ-101)", () => {
  test("resposta de sucesso (200): renderiza o card de resultado", async ({ page }) => {
    test.setTimeout(60000);
    await page.route("**/api/diagnostico", route => {
      route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ success: true }) });
    });

    await page.goto("/diagnostico.html");
    await preencherStep4(page);

    await page.evaluate(() => (window as any).enviar());

    await expect(page.locator("#resultado")).toBeVisible();
    await expect(page.locator(".diag-resultado-card")).toBeVisible();
  });

  test("resposta de erro (400, ex.: consentimento ausente no backend): NÃO renderiza sucesso, exibe alerta", async ({ page }) => {
    test.setTimeout(60000);
    await page.route("**/api/diagnostico", route => {
      route.fulfill({ status: 400, contentType: "application/json", body: JSON.stringify({ error: "Consentimento obrigatório" }) });
    });

    let dialogMessage = "";
    page.once("dialog", async dialog => {
      dialogMessage = dialog.message();
      await dialog.accept();
    });

    await page.goto("/diagnostico.html");
    await preencherStep4(page);

    await page.evaluate(() => (window as any).enviar());
    await page.waitForFunction(() => document.querySelectorAll(".diag-resultado-card").length === 0 || true);

    expect(dialogMessage).toMatch(/erro/i);
    await expect(page.locator(".diag-resultado-card")).toHaveCount(0);
    await expect(page.locator("#diagSteps")).toBeVisible();
  });

  test("resposta de erro do servidor (500): NÃO renderiza sucesso, exibe alerta", async ({ page }) => {
    test.setTimeout(60000);
    await page.route("**/api/diagnostico", route => {
      route.fulfill({ status: 500, contentType: "application/json", body: JSON.stringify({ error: "Erro interno" }) });
    });

    let dialogMessage = "";
    page.once("dialog", async dialog => {
      dialogMessage = dialog.message();
      await dialog.accept();
    });

    await page.goto("/diagnostico.html");
    await preencherStep4(page);

    await page.evaluate(() => (window as any).enviar());
    await page.waitForFunction(() => document.querySelectorAll(".diag-resultado-card").length === 0 || true);

    expect(dialogMessage).toMatch(/erro/i);
    await expect(page.locator(".diag-resultado-card")).toHaveCount(0);
  });

  // Regressão: enviar() (diagnostico.js) nunca incluía `nivel` no corpo do
  // POST — só calculava o nível de risco depois da resposta, dentro de
  // renderResultado(), para exibição. O backend usa req.body.nivel no
  // assunto do e-mail de notificação ("Novo diagnóstico - ${nivel}"), que
  // chegava como "undefined" em todo envio. Corrigido calculando o nível
  // antes do fetch e enviando no corpo.
  test("envia o campo `nivel` (nível de risco) no corpo do POST", async ({ page }) => {
    test.setTimeout(60000);

    let sentBody: Record<string, unknown> | null = null;
    await page.route("**/api/diagnostico", route => {
      sentBody = route.request().postDataJSON();
      route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ success: true }) });
    });

    await page.goto("/diagnostico.html");
    await preencherStep4(page);

    await page.evaluate(() => (window as any).enviar());
    await expect(page.locator("#resultado")).toBeVisible();

    expect(sentBody).not.toBeNull();
    expect(sentBody!.nivel).toBeTruthy();
    expect(sentBody!.nivel).not.toBe("undefined");
  });
});
