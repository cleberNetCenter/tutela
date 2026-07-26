import { test, expect } from "@playwright/test";
import { findAllRefs, hashFile, loadManifest, assetExists, KNOWN_DEAD_ASSETS } from "./support/asset-versions";

// ARQ-502 (docs/architecture/16-architecture-backlog.md) — débito técnico
// #12 (docs/architecture/12-technical-debt.md): três convenções de
// cache-busting coexistiam sem critério (contador simples, data
// AAAAMMDDNN, contador por arquivo), e a mesma inconsistência já causava
// bugs reais antes desta sprint: assets-digital.css era referenciado como
// ?v=2 em 10 páginas e ?v=7 em 5, e insights-pilar.css como ?v=1 em uma
// página e ?v=2 em outras duas — mesmo arquivo físico, números divergentes.
//
// Convenção unificada: contador inteiro simples, único por arquivo, com o
// hash de conteúdo correspondente registrado em
// tests/support/asset-versions.json. Isso torna a convenção verificável,
// não só documentada: se o conteúdo de um arquivo mudar sem o ?v= ser
// incrementado (e o manifesto regenerado via
// node tests/support/generate-asset-versions.js), o teste de hash abaixo
// falha.

test.describe("Cache-busting unificado (ARQ-502)", () => {
  test("toda query string ?v= usa o formato de contador inteiro simples", () => {
    // 1 a 4 dígitos, sem zero à esquerda: um contador real deste site nunca
    // vai passar de poucas dezenas de bumps por arquivo. O limite existe
    // para rejeitar exatamente o que esta sprint elimina — versões
    // codificadas como data (ex. 2026041001, 20260221), que são "só
    // dígitos" mas não um contador (um regex /^\d+$/ sozinho não pegaria
    // essa diferença).
    const COUNTER = /^[1-9]\d{0,3}$/;
    const refs = findAllRefs();
    expect(refs.length).toBeGreaterThan(0); // guarda contra falso-positivo do parser

    const malformed = refs.filter((r) => !COUNTER.test(r.version));
    expect(
      malformed,
      `versão fora do formato de contador inteiro (convenção única ARQ-502):\n${malformed
        .map((r) => `  ${r.file}${r.line ? ":" + r.line : ""} — ${r.assetPath}?v=${r.version}`)
        .join("\n")}`,
    ).toEqual([]);
  });

  test("cada arquivo tem uma única versão referenciada em todo o site", () => {
    const refs = findAllRefs();
    const byAsset = new Map();
    for (const r of refs) {
      if (!byAsset.has(r.assetPath)) byAsset.set(r.assetPath, new Set());
      byAsset.get(r.assetPath).add(r.version);
    }

    const inconsistent = [...byAsset.entries()].filter(([, versions]) => versions.size > 1);
    expect(
      inconsistent,
      `mesmo arquivo referenciado com versões diferentes em páginas diferentes (exatamente o bug que ARQ-502 elimina):\n${inconsistent
        .map(([assetPath, versions]) => `  ${assetPath}: ${[...versions].join(", ")}`)
        .join("\n")}`,
    ).toEqual([]);
  });

  test("nenhum asset referenciado deixa de existir no disco, além dos já catalogados como mortos (fora de escopo)", () => {
    // Complementa tests/dead-asset-references.spec.ts (que cobre imagens):
    // aqui a checagem é sobre os próprios CSS/JS/JSON versionados por
    // ?v=. legal/termos-de-uso.html → pages/termos-de-uso.css é um caso
    // pré-existente, já catalogado (ver KNOWN_DEAD_ASSETS) — fora do
    // escopo de ARQ-502 (débito técnico #12 é sobre convenção de
    // versionamento, não sobre asset ausente).
    const refs = findAllRefs();
    const referenced = new Set(refs.map((r) => r.assetPath));
    const newlyDead = [...referenced].filter((a) => !assetExists(a) && !KNOWN_DEAD_ASSETS.has(a));
    expect(newlyDead, "asset referenciado mas ausente do disco, não catalogado em KNOWN_DEAD_ASSETS").toEqual([]);
  });

  test("o manifesto (tests/support/asset-versions.json) cobre exatamente os assets versionados existentes", () => {
    const refs = findAllRefs();
    const referenced = new Set(refs.map((r) => r.assetPath).filter((a) => assetExists(a)));
    const manifest = loadManifest();
    const manifested = new Set(Object.keys(manifest));

    const missingFromManifest = [...referenced].filter((a) => !manifested.has(a));
    const orphanedInManifest = [...manifested].filter((a) => !referenced.has(a));

    expect(missingFromManifest, "assets referenciados no site mas ausentes do manifesto").toEqual([]);
    expect(orphanedInManifest, "assets no manifesto que não são mais referenciados em lugar nenhum").toEqual([]);
  });

  test("versão referenciada no código bate com a versão registrada no manifesto", () => {
    const refs = findAllRefs();
    const manifest = loadManifest();
    const mismatched = refs.filter(
      (r) => manifest[r.assetPath] && manifest[r.assetPath].version !== r.version,
    );
    expect(
      mismatched,
      `referência usa uma versão diferente da registrada no manifesto:\n${mismatched
        .map(
          (r) =>
            `  ${r.file} — ${r.assetPath}?v=${r.version} (manifesto: ${manifest[r.assetPath]?.version})`,
        )
        .join("\n")}`,
    ).toEqual([]);
  });

  test("hash de conteúdo de cada asset bate com o registrado no manifesto (detecta bump esquecido)", () => {
    const manifest = loadManifest();
    const stale = Object.entries(manifest).filter(
      ([assetPath, entry]) => hashFile(assetPath) !== entry.hash,
    );
    expect(
      stale,
      `conteúdo do arquivo mudou sem incrementar o ?v= (ou o manifesto não foi regenerado — rode node tests/support/generate-asset-versions.js):\n${stale
        .map(([assetPath]) => `  ${assetPath}`)
        .join("\n")}`,
    ).toEqual([]);
  });
});
