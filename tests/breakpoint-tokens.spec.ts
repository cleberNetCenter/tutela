import { test, expect } from "@playwright/test";
import { readFileSync, readdirSync, statSync } from "fs";
import { join, extname } from "path";

// ARQ-302 (docs/architecture/16-architecture-backlog.md) — 13 valores de
// max-width usados em @media sem token compartilhado (débito técnico #10).
//
// CSS não permite var() dentro da condição de @media, e o projeto não usa
// pré-processador nem build step (docs/architecture/02-stack.md) — não há
// forma de "tokenizar" a query em si sem mudar a arquitetura de build.
// A tokenização possível aqui é: declarar os 13 valores como fonte única
// em foundation/tokens.css (--breakpoint-*, utilizável via var() fora de
// @media) e usar este teste como guarda automatizado de que nenhum
// @media (max-width: ...) do repositório introduz um 14º valor não
// documentado, e que todos seguem a mesma formatação.

const TOKENS_CSS = join(__dirname, "..", "public/assets/css/foundation/tokens.css");
const PUBLIC_DIR = join(__dirname, "..", "public");

function approvedBreakpoints(): number[] {
  const css = readFileSync(TOKENS_CSS, "utf8");
  const matches = [...css.matchAll(/--breakpoint-(\d+):\s*(\d+)px;/g)];
  return matches.map((m) => {
    const name = Number(m[1]);
    const value = Number(m[2]);
    expect(value, `--breakpoint-${m[1]} deveria valer ${m[1]}px, não ${value}px`).toBe(name);
    return value;
  });
}

function walk(dir: string, exts: string[], out: string[] = []): string[] {
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    const s = statSync(full);
    if (s.isDirectory()) walk(full, exts, out);
    else if (exts.includes(extname(entry))) out.push(full);
  }
  return out;
}

type MediaMaxWidth = { file: string; line: number; raw: string; value: number };

function findMediaMaxWidths(): MediaMaxWidth[] {
  const files = walk(PUBLIC_DIR, [".css", ".html"]);
  const found: MediaMaxWidth[] = [];
  for (const file of files) {
    const lines = readFileSync(file, "utf8").split("\n");
    lines.forEach((line, i) => {
      const m = line.match(/@media[^{]*max-width\s*:\s*(\d+)px[^{]*\{/);
      if (m) {
        found.push({ file, line: i + 1, raw: line.trim(), value: Number(m[1]) });
      }
    });
  }
  return found;
}

test.describe("Breakpoints tokenizados (ARQ-302)", () => {
  test("foundation/tokens.css declara os 13 valores aprovados", () => {
    const values = approvedBreakpoints();
    expect(new Set(values).size).toBe(values.length); // sem duplicatas
    expect(values.sort((a, b) => a - b)).toEqual([
      480, 540, 560, 600, 640, 720, 760, 768, 860, 900, 1024, 1180, 1200,
    ]);
  });

  test("todo @media (max-width: ...) do repositório usa um valor aprovado", () => {
    const approved = new Set(approvedBreakpoints());
    const occurrences = findMediaMaxWidths();
    expect(occurrences.length).toBeGreaterThan(0); // guarda contra falso-positivo do parser

    const unauthorized = occurrences.filter((o) => !approved.has(o.value));
    expect(
      unauthorized,
      `valor(es) de max-width fora da lista aprovada em --breakpoint-*:\n${unauthorized
        .map((o) => `  ${o.file}:${o.line} — ${o.raw}`)
        .join("\n")}`
    ).toEqual([]);
  });

  test("todo @media (max-width: ...) segue a formatação padrão (espaço após @media e após :)", () => {
    const occurrences = findMediaMaxWidths();
    const canonical = /^@media \(max-width: \d+px\) \{$/;
    const malformed = occurrences.filter((o) => !canonical.test(o.raw));
    expect(
      malformed,
      `formatação inconsistente (esperado "@media (max-width: Npx) {"):\n${malformed
        .map((o) => `  ${o.file}:${o.line} — "${o.raw}"`)
        .join("\n")}`
    ).toEqual([]);
  });
});
