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

test.describe("Formulário de diagnóstico — tratamento de erro do fetch (ARQ-101)", () => {
  test("resposta de sucesso (200): renderiza o card de resultado", async ({ page }) => {
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
});
