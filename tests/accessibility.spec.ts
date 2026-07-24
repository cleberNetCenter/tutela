import { test, expect } from "@playwright/test";

// ARQ-601 — skip-link (`#main-content`). Cobre 1 página por cluster relevante:
// home, página legal e cluster Ativos Digitais (o mesmo `header.html`, via SSI,
// é a única fonte do skip-link nas 37 páginas — ver 16-architecture-backlog.md).
const PAGES = [
  { name: "Home", path: "/" },
  { name: "página legal (termos-de-uso)", path: "/legal/termos-de-uso.html" },
  { name: "cluster Ativos Digitais", path: "/ativos-digitais/" },
];

test.describe("Skip-link de acessibilidade (ARQ-601)", () => {
  for (const { name, path } of PAGES) {
    test(`${name}: skip-link existe, fica oculto até o foco via Tab, e ao ativar move o foco para #main-content`, async ({
      page,
    }) => {
      await page.goto(path);

      const skipLink = page.locator(".skip-link");
      const main = page.locator("#main-content");

      await expect(skipLink).toHaveAttribute("href", "#main-content");
      await expect(main).toHaveCount(1);

      // Oculto visualmente antes do foco: fora da viewport (técnica de
      // transform, não display:none, que impediria o foco por Tab).
      const boxBeforeFocus = await skipLink.boundingBox();
      expect(boxBeforeFocus).not.toBeNull();
      expect(boxBeforeFocus!.y + boxBeforeFocus!.height).toBeLessThanOrEqual(0);

      // Skip-link é o primeiro elemento focável da página.
      await page.keyboard.press("Tab");
      await expect(skipLink).toBeFocused();

      // Visível ao receber foco via teclado.
      const boxAfterFocus = await skipLink.boundingBox();
      expect(boxAfterFocus).not.toBeNull();
      expect(boxAfterFocus!.y).toBeGreaterThanOrEqual(0);

      // Ativar o link (Enter) move o foco para o conteúdo principal.
      await page.keyboard.press("Enter");
      await expect(main).toBeFocused();
      expect(page.url()).toContain("#main-content");
    });
  }
});

// ARQ-602 — auditoria de landmarks/ARIA. Cobre as 3 correções de baixo risco
// aplicadas nesta sprint (ver 16-architecture-backlog.md).
test.describe("Landmarks e ARIA (ARQ-602)", () => {
  test("dropdowns de navegação: aria-expanded, aria-haspopup e aria-controls apontam para o menu correto", async ({
    page,
  }) => {
    await page.goto("/");

    const toggles = page.locator(".nav-dropdown .nav-toggle");
    await expect(toggles).toHaveCount(4);

    const count = await toggles.count();
    for (let i = 0; i < count; i++) {
      const toggle = toggles.nth(i);
      await expect(toggle).toHaveAttribute("aria-haspopup", "true");
      await expect(toggle).toHaveAttribute("aria-expanded", "false");

      const controlsId = await toggle.getAttribute("aria-controls");
      expect(controlsId).toBeTruthy();
      await expect(page.locator(`#${controlsId}`)).toHaveClass(/dropdown-menu/);
    }
  });

  test("seletor de idioma (desktop): ícones de bandeira têm alt text", async ({ page }) => {
    await page.goto("/");

    const flags = page.locator(".lang-switch .lang-flag img");
    await expect(flags).toHaveCount(3);

    const count = await flags.count();
    for (let i = 0; i < count; i++) {
      const alt = await flags.nth(i).getAttribute("alt");
      expect(alt).toBeTruthy();
    }
  });

  test.describe("aside duplicados têm aria-labelledby distinto", () => {
    const PAGES_WITH_TWO_ASIDES = [
      { name: "Empresas", path: "/empresas.html" },
      { name: "Governo", path: "/governo.html" },
      { name: "Pessoas", path: "/pessoas.html" },
      { name: "Ativos Digitais (visão geral)", path: "/ativos-digitais/" },
    ];

    for (const { name, path } of PAGES_WITH_TWO_ASIDES) {
      test(`${name}: 2 landmarks <aside> com aria-labelledby apontando para um id existente e distinto entre si`, async ({
        page,
      }) => {
        await page.goto(path);

        const asides = page.locator("aside");
        await expect(asides).toHaveCount(2);

        const labelledbyIds = new Set<string>();
        for (const aside of await asides.all()) {
          const labelledby = await aside.getAttribute("aria-labelledby");
          expect(labelledby).toBeTruthy();
          await expect(page.locator(`#${labelledby}`)).toHaveCount(1);
          labelledbyIds.add(labelledby!);
        }
        expect(labelledbyIds.size).toBe(2);
      });
    }
  });
});
