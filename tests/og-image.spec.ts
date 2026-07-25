import { test, expect } from "@playwright/test";
import { existsSync, readFileSync } from "fs";
import { join } from "path";

// ARQ-201 (docs/architecture/16-architecture-backlog.md) — débito técnico #1
// (docs/architecture/12-technical-debt.md): og-image.jpg é referenciado via
// og:image/twitter:image em todas as páginas com metadata social, mas o
// arquivo nunca existiu no repositório versionado. A Sprint 5 (ARQ-108)
// confirmou por auditoria externa (curl) 404 em produção e homologação —
// não é um caso de "existe só em produção", é ausência real nos dois
// ambientes. O item está BLOQUEADO: depende da entrega da arte final pelo
// time de conteúdo/design, não de trabalho de engenharia.
//
// Specs esperadas para o asset (Open Graph): 1200×630px, JPEG, peso
// recomendado < 300KB (limite prático para preview rápido em apps de
// mensagem/redes sociais — Open Graph em si não impõe um teto formal).
//
// Este guard-test documenta o débito de forma executável em vez de só em
// texto: enquanto o arquivo não existir, roda como "fixme" (visível no
// relatório, não conta como falha nem quebra `npm test`). Assim que
// public/assets/images/og-image.jpg for adicionado, passa a rodar de
// verdade e falha só se o arquivo for removido de novo no futuro.
test.describe("Asset de Open Graph (ARQ-201)", () => {
  const OG_IMAGE_PATH = join(__dirname, "..", "public/assets/images/og-image.jpg");

  test("og-image.jpg existe em public/assets/images/", () => {
    test.fixme(
      !existsSync(OG_IMAGE_PATH),
      "ARQ-201 BLOQUEADO (docs/architecture/16-architecture-backlog.md#arq-201): " +
        "aguardando arte final (1200×630px, JPEG) do time de conteúdo/design.",
    );

    expect(
      existsSync(OG_IMAGE_PATH),
      "public/assets/images/og-image.jpg deve existir — referenciado por og:image/twitter:image " +
        "em 11 páginas (ver docs/architecture/12-technical-debt.md, item #1)",
    ).toBe(true);
  });

  // Achado da Sprint 18, adjacente mas fora do escopo original de ARQ-201:
  // /ativos-digitais/index.html referenciava um segundo asset ausente,
  // og-ativos-digitais.jpg, apontando para um diretório que nunca existiu
  // no repositório (assets/img/, corrigido nesta sprint para
  // assets/images/ — mesma convenção do resto do site). Diferente da
  // correção de diretório (inequivocamente um bug), o nome de arquivo
  // distinto foi mantido como está: pode ser uma decisão de conteúdo
  // (imagem social dedicada ao cluster de Ativos Digitais) que não cabe
  // a este guard-test presumir — ver observação em ARQ-201 no backlog.
  const OG_ATIVOS_DIGITAIS_PATH = join(
    __dirname,
    "..",
    "public/assets/images/og-ativos-digitais.jpg",
  );

  test("og-ativos-digitais.jpg existe em public/assets/images/", () => {
    test.fixme(
      !existsSync(OG_ATIVOS_DIGITAIS_PATH),
      "Achado da Sprint 18 (relacionado a ARQ-201, fora do escopo original): aguardando decisão " +
        "de conteúdo + arte de public/assets/images/og-ativos-digitais.jpg, hoje referenciado " +
        "só por /ativos-digitais/index.html.",
    );

    expect(existsSync(OG_ATIVOS_DIGITAIS_PATH)).toBe(true);
  });
});

// Guarda de regressão independente da existência do binário: garante que
// nenhuma página volte a referenciar o diretório inexistente `assets/img/`
// (bug real encontrado e corrigido nesta sprint em 4 meta tags/3 páginas —
// og-default.jpg foi consolidado em og-image.jpg; og-ativos-digitais.jpg
// manteve o nome, só corrigiu o diretório). Roda hoje, sem depender do
// asset existir.
test("nenhuma página referencia o diretório inexistente assets/img/ em og:image/twitter:image", () => {
  const REPO_ROOT = join(__dirname, "..");
  const files = execListHtmlFiles(REPO_ROOT);

  const offenders: string[] = [];
  for (const file of files) {
    const html = readFileSync(join(REPO_ROOT, file), "utf8");
    const matches = html.match(/(?:og:image|twitter:image)"\s+content="[^"]*"/g) ?? [];
    for (const tag of matches) {
      if (tag.includes("/assets/img/")) {
        offenders.push(`${file}: ${tag}`);
      }
    }
  }

  expect(offenders, "meta tags apontando para o diretório assets/img/ (inexistente)").toEqual([]);
});

function execListHtmlFiles(repoRoot: string): string[] {
  const { execSync } = require("child_process") as typeof import("child_process");
  return execSync("git ls-files", { cwd: repoRoot, encoding: "utf8" })
    .split("\n")
    .filter((f) => /^public\/.*\.html$/.test(f));
}
