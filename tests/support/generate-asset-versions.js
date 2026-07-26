#!/usr/bin/env node
// Regenera tests/support/asset-versions.json (ARQ-502) com o hash de
// conteúdo atual de cada asset versionado. Rodar sempre que um ?v= for
// incrementado manualmente em HTML/CSS/JS, antes de commitar.
//
// Uso: node tests/support/generate-asset-versions.js
const fs = require("fs");
const { findAllRefs, hashFile, assetExists, KNOWN_DEAD_ASSETS, MANIFEST_PATH } = require("./asset-versions");

const byAsset = new Map();
for (const ref of findAllRefs()) {
  if (!byAsset.has(ref.assetPath)) byAsset.set(ref.assetPath, new Set());
  byAsset.get(ref.assetPath).add(ref.version);
}

const inconsistent = [...byAsset.entries()].filter(([, versions]) => versions.size > 1);
if (inconsistent.length > 0) {
  console.error("Versões divergentes para o mesmo arquivo — corrija todas as referências antes de gerar o manifesto:");
  for (const [assetPath, versions] of inconsistent) {
    console.error(`  ${assetPath}: ${[...versions].join(", ")}`);
  }
  process.exit(1);
}

const manifest = {};
for (const assetPath of [...byAsset.keys()].sort()) {
  if (!assetExists(assetPath)) {
    if (!KNOWN_DEAD_ASSETS.has(assetPath)) {
      console.error(`Asset referenciado mas ausente do disco (não catalogado em KNOWN_DEAD_ASSETS): ${assetPath}`);
      process.exit(1);
    }
    console.warn(`Ignorando asset morto conhecido (fora do escopo ARQ-502): ${assetPath}`);
    continue;
  }
  const version = [...byAsset.get(assetPath)][0];
  manifest[assetPath] = { version, hash: hashFile(assetPath) };
}

fs.writeFileSync(MANIFEST_PATH, JSON.stringify(manifest, null, 2) + "\n");
console.log(`tests/support/asset-versions.json atualizado (${Object.keys(manifest).length} assets).`);
