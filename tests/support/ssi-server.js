// Servidor HTTP mínimo, exclusivo para os testes Playwright.
//
// Por quê existe: em produção/homologação, o Nginx resolve
// `<!--#include virtual="..." -->` (SSI) para montar header/footer/scripts
// em cada página. `python3 -m http.server`, único servidor local documentado
// em docs/architecture/13-development-workflow.md, não resolve SSI — serviria
// o comentário cru em vez do header/nav real, impedindo testar navegação e
// detecção de legal-page. Este servidor replica só essa resolução, com
// módulos nativos do Node (sem dependência nova), sem alterar nenhum arquivo
// de public/ e sem rodar em produção.
const http = require("http");
const fs = require("fs");
const path = require("path");

const PUBLIC_DIR = path.join(__dirname, "..", "..", "public");

const MIME_TYPES = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".ico": "image/x-icon",
  ".xml": "application/xml; charset=utf-8",
  ".txt": "text/plain; charset=utf-8",
  ".webmanifest": "application/manifest+json",
};

const INCLUDE_RE = /<!--#include\s+virtual="([^"]+)"\s*-->/g;

function resolveIncludes(html, depth = 0) {
  if (depth > 5) return html; // guarda contra include recursivo/circular
  if (!INCLUDE_RE.test(html)) return html;
  INCLUDE_RE.lastIndex = 0;
  return html.replace(INCLUDE_RE, (match, virtualPath) => {
    const includeFile = path.join(PUBLIC_DIR, virtualPath);
    if (!includeFile.startsWith(PUBLIC_DIR)) return "";
    try {
      const included = fs.readFileSync(includeFile, "utf8");
      return resolveIncludes(included, depth + 1);
    } catch {
      return `<!-- SSI include not found: ${virtualPath} -->`;
    }
  });
}

function resolveFilePath(urlPath) {
  const decoded = decodeURIComponent(urlPath.split("?")[0]);
  let filePath = path.join(PUBLIC_DIR, decoded);

  if (!filePath.startsWith(PUBLIC_DIR)) {
    return null; // bloqueia path traversal
  }

  try {
    if (fs.statSync(filePath).isDirectory()) {
      filePath = path.join(filePath, "index.html");
    }
  } catch {
    // arquivo não existe como diretório; segue para checagem abaixo
  }

  return filePath;
}

function createSSIServer() {
  return http.createServer((req, res) => {
    const filePath = resolveFilePath(req.url);

    if (!filePath || !fs.existsSync(filePath) || !fs.statSync(filePath).isFile()) {
      res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
      res.end("404 Not Found");
      return;
    }

    const ext = path.extname(filePath);
    const contentType = MIME_TYPES[ext] || "application/octet-stream";

    if (ext === ".html") {
      const raw = fs.readFileSync(filePath, "utf8");
      const resolved = resolveIncludes(raw);
      res.writeHead(200, { "Content-Type": contentType });
      res.end(resolved);
      return;
    }

    res.writeHead(200, { "Content-Type": contentType });
    fs.createReadStream(filePath).pipe(res);
  });
}

if (require.main === module) {
  const port = Number(process.env.PORT) || 8080;
  createSSIServer().listen(port, () => {
    console.log(`SSI test server listening on http://localhost:${port}`);
  });
}

module.exports = { createSSIServer };
