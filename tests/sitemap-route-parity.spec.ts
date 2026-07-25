import { test, expect } from "@playwright/test";
import { execSync } from "child_process";
import { readFileSync } from "fs";
import { join } from "path";

// ARQ-203 (docs/architecture/16-architecture-backlog.md) — 04-routing.md
// registrava uma divergência entre "35 rotas reais" e "37 URLs no sitemap",
// não investigada a fundo. A investigação (Sprint 17) encontrou que, na
// prática, as duas contagens já eram idênticas (37 = 37, reciprocidade
// item a item confirmada); o "35" era um erro de contagem na própria
// documentação, não um problema de código ou do workflow gerador — mesmo
// no commit que introduziu a frase, o comando documentado já retornava 37.
//
// Este guard-test replica exatamente a lógica de `.github/workflows/sitemap.yml`
// (fonte: `git ls-files`, não o disco — o gerador reflete o que está
// commitado — ignora `public/partials/`) para derivar a lista de rotas
// reais esperadas, e compara contra as <loc> de `public/sitemap.xml`.
// Falha se qualquer rota real estiver ausente do sitemap, se qualquer URL
// do sitemap não corresponder a uma rota real, ou se as contagens
// divergirem — sem exigir baseURL/servidor, pois é uma checagem estática
// de arquivos.

const SITE = "https://tuteladigital.com.br";
const REPO_ROOT = join(__dirname, "..");

function expectedRoutesFromGit(): string[] {
  const output = execSync("git ls-files", { cwd: REPO_ROOT, encoding: "utf8" });
  const files = output
    .split("\n")
    .filter((f) => /^public\/.*\.html$/.test(f))
    .filter((f) => !f.startsWith("public/partials/"));

  return files
    .map((file) => {
      const clean = file.slice("public/".length);
      let url: string;
      if (clean === "index.html") {
        url = "";
      } else if (clean.endsWith("/index.html")) {
        url = clean.slice(0, -"index.html".length);
      } else {
        url = clean.slice(0, -".html".length);
      }
      return url === "" ? `${SITE}/` : `${SITE}/${url.replace(/\/$/, "")}/`;
    })
    .sort();
}

function sitemapUrls(): string[] {
  const xml = readFileSync(join(REPO_ROOT, "public/sitemap.xml"), "utf8");
  const matches = [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)];
  return matches.map((m) => m[1]).sort();
}

test.describe("Paridade rotas reais × sitemap.xml (ARQ-203)", () => {
  test("toda rota real (git ls-files, exclui partials) está no sitemap", () => {
    const routes = expectedRoutesFromGit();
    const sitemap = sitemapUrls();
    const missing = routes.filter((r) => !sitemap.includes(r));
    expect(missing, `Rotas reais ausentes do sitemap: ${missing.join(", ")}`).toEqual([]);
  });

  test("toda URL do sitemap corresponde a uma rota real", () => {
    const routes = expectedRoutesFromGit();
    const sitemap = sitemapUrls();
    const orphaned = sitemap.filter((u) => !routes.includes(u));
    expect(orphaned, `URLs no sitemap sem rota real correspondente: ${orphaned.join(", ")}`).toEqual([]);
  });

  test("contagem de rotas reais é igual à contagem de URLs no sitemap", () => {
    const routes = expectedRoutesFromGit();
    const sitemap = sitemapUrls();
    expect(
      sitemap.length,
      `Rotas reais: ${routes.length}, URLs no sitemap: ${sitemap.length}. Se a divergência for intencional, justifique por escrito em 16-architecture-backlog.md (ARQ-203) e ajuste este teste.`,
    ).toBe(routes.length);
  });
});
