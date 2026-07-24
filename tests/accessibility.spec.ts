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
