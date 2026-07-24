import { test, expect } from "@playwright/test";

test.describe("Navegação principal", () => {
  test("dropdown de desktop abre no hover e fecha com Escape", async ({ page }) => {
    // O toggle também abre no `mouseenter` do `.nav-dropdown` (navigation-menu.js).
    // Um .click() do Playwright move o mouse até o elemento antes de clicar,
    // o que já dispara esse hover e abre o menu — testar hover diretamente
    // reflete a interação real de um usuário de mouse.
    await page.goto("/");

    const dropdown = page.locator(".nav-dropdown").first();
    const toggle = dropdown.locator(".nav-toggle");
    const menu = dropdown.locator(".dropdown-menu");

    await expect(toggle).toHaveAttribute("aria-expanded", "false");

    await dropdown.hover();
    await expect(toggle).toHaveAttribute("aria-expanded", "true");
    await expect(menu).toHaveClass(/open/);

    await page.keyboard.press("Escape");
    await expect(toggle).toHaveAttribute("aria-expanded", "false");
    await expect(menu).not.toHaveClass(/open/);
  });

  test("dropdown de desktop alterna com clique direto (sem hover prévio)", async ({ page }) => {
    // dispatchEvent não move o mouse, então isola o handler de click do
    // handler de mouseenter — cobre o toggle por clique isoladamente.
    await page.goto("/");

    const toggle = page.locator(".nav-dropdown .nav-toggle").first();
    const menu = page.locator(".nav-dropdown .dropdown-menu").first();

    await expect(toggle).toHaveAttribute("aria-expanded", "false");

    await toggle.dispatchEvent("click");
    await expect(toggle).toHaveAttribute("aria-expanded", "true");
    await expect(menu).toHaveClass(/open/);

    await toggle.dispatchEvent("click");
    await expect(toggle).toHaveAttribute("aria-expanded", "false");
    await expect(menu).not.toHaveClass(/open/);
  });

  test("menu mobile abre e fecha", async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 });
    await page.goto("/");

    const mobileBtn = page.locator(".mobile-menu-btn");
    const nav = page.locator("#nav");

    await expect(mobileBtn).toHaveAttribute("aria-expanded", "false");

    await mobileBtn.click();
    await expect(mobileBtn).toHaveAttribute("aria-expanded", "true");
    await expect(nav).toHaveClass(/open/);

    await mobileBtn.click();
    await expect(mobileBtn).toHaveAttribute("aria-expanded", "false");
    await expect(nav).not.toHaveClass(/open/);
  });
});

test.describe("Navegação por teclado nos dropdowns (ARQ-603)", () => {
  test("Enter e Space no toggle abrem e fecham o dropdown, equivalente ao clique", async ({ page }) => {
    await page.goto("/");

    const toggle = page.locator(".nav-dropdown .nav-toggle").first();
    const menu = page.locator(".nav-dropdown .dropdown-menu").first();

    await toggle.focus();
    await page.keyboard.press("Enter");
    await expect(toggle).toHaveAttribute("aria-expanded", "true");
    await expect(menu).toHaveClass(/open/);

    await page.keyboard.press("Enter");
    await expect(toggle).toHaveAttribute("aria-expanded", "false");
    await expect(menu).not.toHaveClass(/open/);

    // Fechar move o foco para fora do toggle (mesma lógica que já evita o
    // dropdown ficar visualmente preso aberto via `:focus-within` depois de
    // um fechamento por clique de mouse — ver closeDrop em navigation-menu.js).
    // Refocar o toggle replica o que um usuário de teclado faria (Tab/Shift+Tab
    // de volta) antes de acionar Space.
    await toggle.focus();
    await page.keyboard.press("Space");
    await expect(toggle).toHaveAttribute("aria-expanded", "true");
    await expect(menu).toHaveClass(/open/);
  });

  test("Tab entra no dropdown já aberto e navega pelos itens do submenu em ordem lógica", async ({ page }) => {
    await page.goto("/");

    const dropdown = page.locator(".nav-dropdown").first();
    const toggle = dropdown.locator(".nav-toggle");
    const items = dropdown.locator(".dropdown-menu a");

    await toggle.focus();
    await page.keyboard.press("Enter");
    await expect(toggle).toHaveAttribute("aria-expanded", "true");

    await page.keyboard.press("Tab");
    await expect(items.first()).toBeFocused();

    await page.keyboard.press("Tab");
    await expect(items.nth(1)).toBeFocused();
  });

  test("ArrowDown no toggle abre o dropdown e foca o primeiro item; ArrowDown/ArrowUp navegam entre itens com wrap-around", async ({
    page,
  }) => {
    await page.goto("/");

    const dropdown = page.locator(".nav-dropdown").first();
    const toggle = dropdown.locator(".nav-toggle");
    const items = dropdown.locator(".dropdown-menu a");
    const itemCount = await items.count();

    await toggle.focus();
    await page.keyboard.press("ArrowDown");
    await expect(toggle).toHaveAttribute("aria-expanded", "true");
    await expect(items.first()).toBeFocused();

    await page.keyboard.press("ArrowDown");
    await expect(items.nth(1)).toBeFocused();

    await page.keyboard.press("ArrowUp");
    await expect(items.first()).toBeFocused();

    // Wrap-around: ArrowUp no primeiro item volta para o último.
    await page.keyboard.press("ArrowUp");
    await expect(items.nth(itemCount - 1)).toBeFocused();
  });

  test("Escape fecha o dropdown e devolve o foco ao toggle, mesmo com o foco em um item do submenu", async ({
    page,
  }) => {
    await page.goto("/");

    const dropdown = page.locator(".nav-dropdown").first();
    const toggle = dropdown.locator(".nav-toggle");
    const menu = dropdown.locator(".dropdown-menu");
    const firstItem = menu.locator("a").first();

    await toggle.focus();
    await page.keyboard.press("ArrowDown");
    await expect(firstItem).toBeFocused();

    await page.keyboard.press("Escape");
    await expect(toggle).toHaveAttribute("aria-expanded", "false");
    await expect(menu).not.toHaveClass(/open/);
    await expect(toggle).toBeFocused();
  });

  test("menu mobile: Enter/Space abrem via teclado, aria-label alterna 'Abrir menu'/'Fechar menu', Escape fecha e devolve o foco", async ({
    page,
  }) => {
    await page.setViewportSize({ width: 375, height: 812 });
    // Fixa o idioma em pt (chave usada por i18n.js), já que o texto do
    // aria-label é traduzível e o locale do navegador de teste não é
    // garantidamente pt-BR — sem isso o teste ficaria dependente do
    // ambiente de execução.
    await page.addInitScript(() => localStorage.setItem("tutela_lang", "pt"));
    await page.goto("/");

    const mobileBtn = page.locator(".mobile-menu-btn");
    const nav = page.locator("#nav");

    await expect(mobileBtn).toHaveAttribute("aria-label", "Abrir menu");

    await mobileBtn.focus();
    await page.keyboard.press("Enter");
    await expect(mobileBtn).toHaveAttribute("aria-expanded", "true");
    await expect(nav).toHaveClass(/open/);
    await expect(mobileBtn).toHaveAttribute("aria-label", "Fechar menu");

    await page.keyboard.press("Escape");
    await expect(mobileBtn).toHaveAttribute("aria-expanded", "false");
    await expect(nav).not.toHaveClass(/open/);
    await expect(mobileBtn).toHaveAttribute("aria-label", "Abrir menu");
    await expect(mobileBtn).toBeFocused();
  });
});
