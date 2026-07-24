import { test, expect } from "@playwright/test";

test.describe("Home", () => {
  test("carrega sem erro de console e sem 404 em assets críticos", async ({ page, baseURL }) => {
    const consoleErrors: string[] = [];
    const failedRequests: string[] = [];

    page.on("console", (msg) => {
      if (msg.type() === "error") consoleErrors.push(msg.text());
    });
    page.on("pageerror", (err) => consoleErrors.push(err.message));
    page.on("response", (response) => {
      const url = response.url();
      if (url.startsWith(baseURL!) && response.status() === 404) {
        failedRequests.push(`${response.status()} ${url}`);
      }
    });

    const response = await page.goto("/");
    expect(response?.status()).toBe(200);
    await page.waitForLoadState("networkidle");

    expect(failedRequests, `Assets locais retornando 404: ${failedRequests.join(", ")}`).toEqual([]);
    expect(consoleErrors, `Erros de console: ${consoleErrors.join(", ")}`).toEqual([]);
    await expect(page).toHaveTitle(/Tutela Digital/);
  });
});
