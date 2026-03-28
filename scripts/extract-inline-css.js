const fs = require("fs");
const path = require("path");

const ROOT = "./public";
const CSS_OUTPUT = "./public/assets/css/pages";

if (!fs.existsSync(CSS_OUTPUT)) {
  fs.mkdirSync(CSS_OUTPUT, { recursive: true });
}

function getPageName(filePath) {
  const parts = filePath.split("/");
  let name = parts[parts.length - 1].replace(".html", "");

  if (name === "index") {
    name = parts[parts.length - 2] || "home";
  }

  return name.toLowerCase().replace(/[^a-z0-9]/g, "-");
}

function extractStyles(html) {
  const regex = /<style[^>]*>([\s\S]*?)<\/style>/gi;
  let match;
  const styles = [];

  while ((match = regex.exec(html))) {
    styles.push(match[1].trim());
  }

  return styles;
}

function removeStyles(html) {
  return html.replace(/<style[^>]*>[\s\S]*?<\/style>/gi, "");
}

function scopeCSS(css, pageClass) {
  return css.replace(/(^|\})\s*([^{@}][^{]+)\s*\{/g, (match, prefix, selector) => {
    const scoped = selector
      .split(",")
      .map(s => `.page-${pageClass} ${s.trim()}`)
      .join(", ");

    return `${prefix} ${scoped} {`;
  });
}

function injectCSSLink(html, cssPath) {
  if (html.includes(cssPath)) return html;

  return html.replace(
    /<\/head>/i,
    `  <link rel="stylesheet" href="${cssPath}?v=1">\n</head>`
  );
}

function processFile(filePath) {
  // Ignorar página já tratada
  if (filePath.includes("seguranca.html")) {
    console.log(`⏭ Ignorado: ${filePath}`);
    return;
  }

  let html = fs.readFileSync(filePath, "utf-8");

  const styles = extractStyles(html);
  if (styles.length === 0) return;

  const pageName = getPageName(filePath);
  const cssFileName = `${pageName}.css`;
  const cssPath = `/assets/css/pages/${cssFileName}`;
  const fullCssPath = path.join(CSS_OUTPUT, cssFileName);

  const combinedCSS = styles.join("\n\n");
  const scopedCSS = scopeCSS(combinedCSS, pageName);

  if (!fs.existsSync(fullCssPath)) {
    fs.writeFileSync(fullCssPath, scopedCSS);
  } else {
    console.log(`⚠ CSS já existe, ignorado: ${fullCssPath}`);
  }

  html = removeStyles(html);

  html = html.replace(/<body([^>]*)>/i, (match, attrs) => {
    if (attrs.includes("page-")) return match;

    let newAttrs = attrs;

    if (attrs.includes("class=")) {
      newAttrs = attrs.replace(/class="([^"]*)"/, (m, classes) => {
        let updated = classes;

        if (!updated.includes("exec-compact")) {
          updated += " exec-compact";
        }

        updated += ` page page-${pageName}`;

        return `class="${updated.trim()}"`;
      });
    } else {
      newAttrs = `${attrs} class="exec-compact page page-${pageName}"`;
    }

    return `<body${newAttrs}>`;
  });

  html = injectCSSLink(html, cssPath);

  fs.writeFileSync(filePath, html);

  console.log(`✔ Processado: ${filePath}`);
}

function walk(dir) {
  const files = fs.readdirSync(dir);

  files.forEach(file => {
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);

    if (stat.isDirectory()) {
      walk(fullPath);
    } else if (file.endsWith(".html")) {
      processFile(fullPath);
    }
  });
}

walk(ROOT);

console.log("\n✅ Finalizado!");
