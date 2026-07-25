import { test, expect } from "@playwright/test";
import { readFileSync, readdirSync, statSync } from "fs";
import { join, extname } from "path";

// ARQ-304 (docs/architecture/16-architecture-backlog.md) — formatação
// inconsistente de @media (espaço após ':', ex. "max-width:768px" vs.
// "max-width: 768px" no mesmo arquivo).
//
// tests/breakpoint-tokens.spec.ts (ARQ-302) já guarda a formatação das
// ocorrências de "@media (max-width: ...)" especificamente. Este teste
// cobre o escopo mais amplo de ARQ-304: qualquer @media, com qualquer
// media feature (max-width, prefers-reduced-motion, etc.) — para não
// deixar features fora de max-width sem guarda contra regressão.

const PUBLIC_DIR = join(__dirname, "..", "public");

function walk(dir: string, exts: string[], out: string[] = []): string[] {
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    const s = statSync(full);
    if (s.isDirectory()) walk(full, exts, out);
    else if (exts.includes(extname(entry))) out.push(full);
  }
  return out;
}

type MediaRule = { file: string; line: number; raw: string };

function findMediaRules(): MediaRule[] {
  const files = walk(PUBLIC_DIR, [".css", ".html"]);
  const found: MediaRule[] = [];
  for (const file of files) {
    const lines = readFileSync(file, "utf8").split("\n");
    lines.forEach((line, i) => {
      const m = line.match(/@media\s*\(.*\)\s*\{/);
      if (m) found.push({ file, line: i + 1, raw: line.trim() });
    });
  }
  return found;
}

test.describe("Formatação de @media (ARQ-304)", () => {
  test("todo @media do repositório segue \"@media (feature: valor) {\" (espaço após @media, após ':' e antes de '{')", () => {
    const occurrences = findMediaRules();
    expect(occurrences.length).toBeGreaterThan(0); // guarda contra falso-positivo do parser

    const canonical = /^@media \([a-z-]+: [^)]+\) \{$/;
    const malformed = occurrences.filter((o) => !canonical.test(o.raw));
    expect(
      malformed,
      `formatação inconsistente (esperado "@media (feature: valor) {"):\n${malformed
        .map((o) => `  ${o.file}:${o.line} — "${o.raw}"`)
        .join("\n")}`
    ).toEqual([]);
  });
});
