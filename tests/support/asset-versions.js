// ARQ-502 (docs/architecture/16-architecture-backlog.md) — descoberta de
// referências ?v= (convenção única: contador inteiro simples) e hash de
// conteúdo dos assets versionados. Usado por tests/cache-busting.spec.ts
// (guarda) e tests/support/generate-asset-versions.js (regenera o
// manifesto tests/support/asset-versions.json após um bump manual).
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const REPO_ROOT = path.join(__dirname, "..", "..");
const PUBLIC_DIR = path.join(REPO_ROOT, "public");
const MANIFEST_PATH = path.join(__dirname, "asset-versions.json");

function walk(dir, exts, out = []) {
  for (const entry of fs.readdirSync(dir)) {
    const full = path.join(dir, entry);
    const stat = fs.statSync(full);
    if (stat.isDirectory()) walk(full, exts, out);
    else if (exts.includes(path.extname(entry))) out.push(full);
  }
  return out;
}

// Referências estáticas: <link href="...?v=N"> / <script src="...?v=N">.
// Só .html: neste projeto nenhum .css carrega outro asset via href/src —
// scanear .css pegaria falso-positivo de comentários de documentação
// (ex. o cabeçalho de institucional.css, que ilustra a ordem do <head>
// da página em um comentário).
function findStaticRefs() {
  const files = walk(PUBLIC_DIR, [".html"]);
  const refs = [];
  const pattern = /(?:href|src)="(\/assets\/[^"?]+\.(?:css|js))\?v=([^"]+)"/g;
  for (const file of files) {
    const lines = fs.readFileSync(file, "utf8").split("\n");
    lines.forEach((line, i) => {
      for (const m of line.matchAll(pattern)) {
        refs.push({
          assetPath: m[1],
          version: m[2],
          file: path.relative(REPO_ROOT, file),
          line: i + 1,
        });
      }
    });
  }
  return refs;
}

// Duas exceções conhecidas: versão embutida dentro de um fetch() em JS, não
// em atributo href/src — não cobertas pelo padrão acima.
function findEmbeddedRefs() {
  const refs = [];

  const i18nRel = "assets/js/i18n.js";
  const i18nSrc = fs.readFileSync(path.join(PUBLIC_DIR, i18nRel), "utf8");
  const langMatch = i18nSrc.match(/\/assets\/lang\/\$\{lang\}\.json\?v=(\S+?)`/);
  if (langMatch) {
    for (const lang of ["pt", "en", "es"]) {
      refs.push({
        assetPath: `/assets/lang/${lang}.json`,
        version: langMatch[1],
        file: `public/${i18nRel}`,
        line: null,
      });
    }
  }

  const searchRel = "assets/js/search.js";
  const searchSrc = fs.readFileSync(path.join(PUBLIC_DIR, searchRel), "utf8");
  const searchMatch = searchSrc.match(/\/assets\/search-index\.json\?v=(\S+?)"/);
  if (searchMatch) {
    refs.push({
      assetPath: "/assets/search-index.json",
      version: searchMatch[1],
      file: `public/${searchRel}`,
      line: null,
    });
  }

  return refs;
}

function findAllRefs() {
  return [...findStaticRefs(), ...findEmbeddedRefs()];
}

// Referência que já apontava para um arquivo inexistente ANTES desta
// sprint (legal/termos-de-uso.html → pages/termos-de-uso.css, nunca
// existiu no histórico do repositório). Fora do escopo de ARQ-502 (que
// trata convenção de versionamento, não assets ausentes — mesma
// disciplina de escopo de ARQ-201); fica listada aqui, não ignorada
// silenciosamente, para não quebrar a geração do manifesto e para que
// um novo asset morto introduzido no futuro continue sendo pego (ver
// assertExistsOrKnownDead).
const KNOWN_DEAD_ASSETS = new Set(["/assets/css/pages/termos-de-uso.css"]);

function assetExists(assetPath) {
  return fs.existsSync(path.join(PUBLIC_DIR, assetPath.replace(/^\//, "")));
}

function hashFile(assetPath) {
  const full = path.join(PUBLIC_DIR, assetPath.replace(/^\//, ""));
  const content = fs.readFileSync(full);
  return crypto.createHash("sha256").update(content).digest("hex").slice(0, 12);
}

function loadManifest() {
  return JSON.parse(fs.readFileSync(MANIFEST_PATH, "utf8"));
}

module.exports = {
  findAllRefs,
  hashFile,
  loadManifest,
  assetExists,
  KNOWN_DEAD_ASSETS,
  MANIFEST_PATH,
  PUBLIC_DIR,
  REPO_ROOT,
};
