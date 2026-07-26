import { test, expect } from "@playwright/test";
import { existsSync, readFileSync } from "fs";
import { join } from "path";
import { execSync } from "child_process";

// ARQ-201 (docs/architecture/16-architecture-backlog.md) — débito técnico #1
// (docs/architecture/12-technical-debt.md): og-image.jpg era referenciado
// via og:image/twitter:image em 15 páginas mas nunca existiu no repositório.
//
// A investigação original (Sprint 18) tratou isso como bloqueio por arte
// pendente. Não é: o site não usa nenhuma imagem rasterizada de conteúdo
// por decisão de design — os elementos visuais das páginas (ex.
// fundamento-juridico) são inteiramente CSS/SVG inline. As referências a
// .jpg/.png eram herança de migração de um template anterior, nunca
// implementadas. Confirmado: o único <img> do site inteiro são as 3
// bandeiras SVG do seletor de idioma (public/partials/header.html).
//
// Removidas nesta sprint, todas comprovadamente órfãs (arquivo nunca
// existiu em nenhum commit do histórico):
// - og:image / twitter:image apontando para og-image.jpg, og-default.jpg
//   (diretório assets/img/, que nunca existiu) e og-ativos-digitais.jpg
// - twitter:card="summary_large_image" sem imagem nenhuma (4 páginas que
//   nunca tiveram og:image) — rebaixado para "summary" em todas as 15
//   páginas afetadas, já que nenhuma tem imagem de fato
// - <link rel="apple-touch-icon" href="/apple-touch-icon.png"> — corrigido
//   para apontar ao asset real /assets/illustrations/favicon.png
// - <link rel="alternate icon" href="/favicon.ico"> — removido, nenhum
//   arquivo .ico existe no repositório
// - schema.org "logo": ".../logo.png" — corrigido para o favicon.svg real,
//   mesmo padrão já usado pela maioria das páginas do site
//
// Este guard-test substitui o antigo tests/og-image.spec.ts (que aguardava
// a entrega de uma arte que não vai existir). Em vez de checar a presença
// de um arquivo específico, varre todo HTML versionado em busca de
// QUALQUER referência (href/src/content/schema.org) a um asset de imagem
// local que não existe no disco — cobre as 4 categorias de bug encontradas
// nesta sprint e previne reintrodução de qualquer uma delas no futuro.

const REPO_ROOT = join(__dirname, "..");
const SITE = "https://tuteladigital.com.br";
const IMAGE_EXT = "svg|png|jpg|jpeg|ico|webp|gif";

function htmlFiles(): string[] {
  return execSync("git ls-files", { cwd: REPO_ROOT, encoding: "utf8" })
    .split("\n")
    .filter((f) => /^public\/.*\.html$/.test(f));
}

function extractLocalImageRefs(html: string): string[] {
  const refs = new Set<string>();

  // href="/foo.png" ou src="/foo.png" (caminho relativo à raiz do site)
  const attrPattern = new RegExp(`(?:href|src)="(/[^"]+\\.(?:${IMAGE_EXT}))(?:\\?[^"]*)?"`, "g");
  for (const m of html.matchAll(attrPattern)) refs.add(m[1]);

  // content="https://tuteladigital.com.br/foo.png" (meta og:/twitter:)
  const metaPattern = new RegExp(
    `content="${SITE}(/[^"]+\\.(?:${IMAGE_EXT}))(?:\\?[^"]*)?"`,
    "g",
  );
  for (const m of html.matchAll(metaPattern)) refs.add(m[1]);

  // "url"/"logo": "https://tuteladigital.com.br/foo.png" (schema.org JSON-LD)
  const jsonPattern = new RegExp(
    `"(?:url|logo)":\\s*"${SITE}(/[^"]+\\.(?:${IMAGE_EXT}))(?:\\?[^"]*)?"`,
    "g",
  );
  for (const m of html.matchAll(jsonPattern)) refs.add(m[1]);

  return [...refs];
}

test("nenhuma página referencia um asset de imagem que não existe no repositório", () => {
  const offenders: string[] = [];

  for (const file of htmlFiles()) {
    const html = readFileSync(join(REPO_ROOT, file), "utf8");
    for (const ref of extractLocalImageRefs(html)) {
      const localPath = join(REPO_ROOT, "public", ref);
      if (!existsSync(localPath)) {
        offenders.push(`${file} → ${ref}`);
      }
    }
  }

  expect(
    offenders,
    "referências a assets de imagem ausentes do repositório (ver docs/architecture/12-technical-debt.md, item #1)",
  ).toEqual([]);
});
