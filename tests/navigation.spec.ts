import { test, expect } from "@playwright/test";

test.describe("Navegação principal", () => {
  test("dropdown de desktop abre no hover e fecha com Escape", async ({ page }) => {
    // O toggle também abre no `mouseenter` do `.nav-dropdown` (mobile-menu.js).
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
