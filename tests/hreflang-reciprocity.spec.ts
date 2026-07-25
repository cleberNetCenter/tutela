import { test, expect } from "@playwright/test";
import { readFileSync } from "fs";
import { join } from "path";

// ARQ-202 (docs/architecture/16-architecture-backlog.md) — débito técnico #5
// (docs/architecture/12-technical-debt.md): o cluster de 4 páginas do pillar
// de Ativos Digitais declarava hreflang recíproco em apenas 3 das 4 páginas;
// a página apontada como x-default (/ativos-digitais/) não declarava, ela
// mesma, o bloco de volta.
//
// Este guard-test parseia o <head> das 4 páginas físicas do cluster e
// confirma reciprocidade formal: cada página deve declarar um link
// hreflang para cada uma das outras 3 variantes de idioma + x-default,
// e todos os 4 arquivos devem concordar exatamente sobre qual URL
// corresponde a cada hreflang (nenhum aponta para destino divergente).

const SITE = "https://tuteladigital.com.br";

const CLUSTER = [
  { file: "public/ativos-digitais/index.html", canonical: `${SITE}/ativos-digitais/` },
  { file: "public/pt/ativos-digitais/index.html", canonical: `${SITE}/pt/ativos-digitais/` },
  { file: "public/en/digital-assets/index.html", canonical: `${SITE}/en/digital-assets/` },
  { file: "public/es/activos-digitales/index.html", canonical: `${SITE}/es/activos-digitales/` },
];

const EXPECTED_HREFLANGS = ["pt-BR", "en", "es", "x-default"];

// pt-BR aponta para o espelho com prefixo (/pt/ativos-digitais/), não para
// a própria raiz sem prefixo — x-default é quem aponta para a raiz.
const EXPECTED_TARGETS: Record<string, string> = {
  "pt-BR": `${SITE}/pt/ativos-digitais/`,
  en: `${SITE}/en/digital-assets/`,
  es: `${SITE}/es/activos-digitales/`,
  "x-default": `${SITE}/ativos-digitais/`,
};

function readHead(file: string): string {
  const html = readFileSync(join(__dirname, "..", file), "utf8");
  const match = html.match(/<head>([\s\S]*?)<\/head>/);
  expect(match, `${file} deveria conter um <head>...</head>`).not.toBeNull();
  return match![1];
}

function parseHreflangs(head: string): Record<string, string> {
  const links = [...head.matchAll(/<link\s+rel="alternate"\s+hreflang="([^"]+)"\s+href="([^"]+)"\s*\/?>/g)];
  const map: Record<string, string> = {};
  for (const [, hreflang, href] of links) {
    expect(map[hreflang], `${hreflang} duplicado no mesmo <head>`).toBeUndefined();
    map[hreflang] = href;
  }
  return map;
}

function parseCanonical(head: string): string {
  const match = head.match(/<link\s+rel="canonical"\s+href="([^"]+)"\s*\/?>/);
  expect(match, "canonical ausente").not.toBeNull();
  return match![1];
}

test.describe("Reciprocidade de hreflang no cluster Ativos Digitais (ARQ-202)", () => {
  for (const page of CLUSTER) {
    test(`${page.file} declara canonical correto e as 4 entradas hreflang esperadas`, () => {
      const head = readHead(page.file);

      expect(parseCanonical(head)).toBe(page.canonical);

      const hreflangs = parseHreflangs(head);
      expect(Object.keys(hreflangs).sort()).toEqual([...EXPECTED_HREFLANGS].sort());

      for (const lang of EXPECTED_HREFLANGS) {
        expect(hreflangs[lang], `hreflang="${lang}" em ${page.file}`).toBe(EXPECTED_TARGETS[lang]);
      }
    });
  }

  test("as 4 páginas concordam simetricamente (nenhuma diverge do consenso do cluster)", () => {
    const perFile = CLUSTER.map((page) => ({
      file: page.file,
      hreflangs: parseHreflangs(readHead(page.file)),
    }));

    const [reference, ...rest] = perFile;
    for (const other of rest) {
      expect(other.hreflangs, `${other.file} deveria ser idêntico a ${reference.file}`).toEqual(
        reference.hreflangs,
      );
    }
  });
});
