import { test, expect } from "@playwright/test";

// Overflow horizontal residual de ~11px no footer (`.tdf-*`), identificado
// incidentalmente durante o fix do header mobile (commit 8684df4). Causa
// raiz: `.tdf-trust-pill` (footer.css) usa `white-space: nowrap` para todos
// os 5 selos, mas o último ("Tecnologia protegida · PCT/IB2026/055458
// (patent pending)") tem texto muito mais longo que os demais e não cabe
// numa única linha em viewports estreitos — forçando o container `.tdf-trust`
// (flex-wrap: wrap) a um min-content maior que o viewport, o que também
// empurra o selo "ICP-Brasil" para fora da linha. Diferente do bug do
// header: ali faltava `flex-wrap`; aqui o wrap do container já existe, mas
// um item individual não podia quebrar internamente.

const NARROW_VIEWPORTS = [
  { name: "iPhone 15 Pro", width: 393, height: 852 },
  { name: "iPhone SE", width: 375, height: 667 },
  { name: "Android comum", width: 360, height: 800 },
];

test.describe("Footer: overflow horizontal", () => {
  for (const vp of NARROW_VIEWPORTS) {
    test(`sem overflow horizontal em ${vp.name} (${vp.width}x${vp.height})`, async ({ page }) => {
      await page.setViewportSize({ width: vp.width, height: vp.height });
      await page.goto("/");
      await page.waitForLoadState("networkidle");

      const { scrollWidth, innerWidth, offenders } = await page.evaluate(() => {
        const offenders: string[] = [];
        document.querySelectorAll<HTMLElement>('[class*="tdf-"]').forEach((el) => {
          const r = el.getBoundingClientRect();
          if (r.right > window.innerWidth + 0.5) {
            offenders.push(`${el.tagName}.${el.className} (right=${r.right.toFixed(1)})`);
          }
        });
        return {
          scrollWidth: document.documentElement.scrollWidth,
          innerWidth: window.innerWidth,
          offenders,
        };
      });

      expect(offenders, `Elementos .tdf-* ultrapassando o viewport: ${offenders.join(", ")}`).toEqual([]);
      expect(scrollWidth).toBeLessThanOrEqual(innerWidth);
    });
  }
});
