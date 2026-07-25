import { test, expect } from "@playwright/test";
import { readFileSync, readdirSync, statSync } from "fs";
import { join, extname, relative } from "path";

// ARQ-303 (docs/architecture/16-architecture-backlog.md) — tokens globais
// --radius-*/--shadow-*, débito técnico #6 (fragmentação de tokens).
//
// Diferente de ARQ-302 (breakpoints): var() funciona normalmente em
// border-radius/box-shadow em qualquer contexto de CSS, então a migração
// aqui é literal→var() de verdade (não uma lista de valores aprovados para
// @media). Guardas deste arquivo:
//   1) --radius-*/--shadow-* em tokens.css batem com o nome (mesmo padrão
//      de tests/breakpoint-tokens.spec.ts).
//   2) Nenhum border-radius literal (fora de var()) sobrevive em
//      public/**/*.css ou public/**/*.html — 100% migrado nesta sprint
//      (diferente de box-shadow, ver item 3).
//   3) box-shadow é majoritariamente uma sombra composta única por
//      marca/página (não uma escala compartilhada) — não é exigido migrar
//      TODA ocorrência, mas nenhuma ocorrência literal pode duplicar
//      exatamente um valor já coberto por --shadow-* (isso indicaria uma
//      sombra compartilhada reintroduzida como literal em vez de var(),
//      o drift que este guard-test previne).

const TOKENS_CSS = join(__dirname, "..", "public/assets/css/foundation/tokens.css");
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

function scanFiles(): string[] {
  // public/partials/ (incluído via SSI) já está sob PUBLIC_DIR
  return walk(PUBLIC_DIR, [".css", ".html"]);
}

function approvedRadiusTokens(): Map<string, string> {
  const css = readFileSync(TOKENS_CSS, "utf8");
  const map = new Map<string, string>();
  for (const m of css.matchAll(/--radius-(\d+):\s*(\d+px|0);/g)) {
    expect(m[2], `--radius-${m[1]} deveria valer ${m[1]}px, não ${m[2]}`).toBe(
      m[1] === "0" ? "0" : `${m[1]}px`
    );
    map.set(`--radius-${m[1]}`, m[2]);
  }
  const pill = css.match(/--radius-pill:\s*([^;]+);/);
  const full = css.match(/--radius-full:\s*([^;]+);/);
  if (pill) map.set("--radius-pill", pill[1].trim());
  if (full) map.set("--radius-full", full[1].trim());
  return map;
}

function approvedShadowTokens(): Map<string, string> {
  const css = readFileSync(TOKENS_CSS, "utf8");
  const map = new Map<string, string>();
  for (const m of css.matchAll(/--(shadow-[a-z-]+):\s*([^;]+);/g)) {
    map.set(`--${m[1]}`, m[2].trim());
  }
  return map;
}

type Declaration = { file: string; index: number; raw: string; value: string };

function findDeclarations(prop: "border-radius" | "box-shadow"): Declaration[] {
  const found: Declaration[] = [];
  for (const file of scanFiles()) {
    if (file === TOKENS_CSS) continue; // definições legítimas, não uso
    const content = readFileSync(file, "utf8");
    const re = new RegExp(`${prop}:\\s*([^;]+);`, "g");
    for (const m of content.matchAll(re)) {
      found.push({
        file: relative(join(__dirname, ".."), file),
        index: m.index ?? 0,
        raw: m[0],
        value: m[1].trim(),
      });
    }
  }
  return found;
}

function lineOf(content: string, index: number): number {
  return content.slice(0, index).split("\n").length;
}

test.describe("Tokens de radius/shadow (ARQ-303)", () => {
  test("foundation/tokens.css declara os tokens --radius-* com nome == valor", () => {
    const tokens = approvedRadiusTokens();
    expect(tokens.size).toBeGreaterThan(0);
    expect(tokens.get("--radius-pill")).toBe("999px");
    expect(tokens.get("--radius-full")).toBe("50%");
  });

  test("foundation/tokens.css declara os tokens --shadow-* usados como fonte de verdade", () => {
    const tokens = approvedShadowTokens();
    expect(tokens.size).toBeGreaterThan(0);
  });

  test("nenhum border-radius literal (fora de var()) fora de tokens.css", () => {
    const declarations = findDeclarations("border-radius");
    expect(declarations.length).toBeGreaterThan(0); // guarda contra falso-positivo do parser

    const literals = declarations.filter((d) => !d.value.includes("var("));
    expect(
      literals,
      `border-radius literal fora de var() — use um token --radius-* existente ou crie um novo:\n${literals
        .map((d) => {
          const content = readFileSync(join(__dirname, "..", d.file), "utf8");
          return `  ${d.file}:${lineOf(content, d.index)} — ${d.raw}`;
        })
        .join("\n")}`
    ).toEqual([]);
  });

  test("nenhum box-shadow literal duplica um valor já coberto por --shadow-*", () => {
    const shadowTokens = approvedShadowTokens();
    const approvedValues = new Set(shadowTokens.values());
    const declarations = findDeclarations("box-shadow");
    expect(declarations.length).toBeGreaterThan(0); // guarda contra falso-positivo do parser

    const drifted = declarations.filter(
      (d) => !d.value.includes("var(") && approvedValues.has(d.value)
    );
    expect(
      drifted,
      `box-shadow literal duplica um valor já coberto por --shadow-* — use o token em vez do literal:\n${drifted
        .map((d) => {
          const content = readFileSync(join(__dirname, "..", d.file), "utf8");
          return `  ${d.file}:${lineOf(content, d.index)} — ${d.raw}`;
        })
        .join("\n")}`
    ).toEqual([]);
  });
});
