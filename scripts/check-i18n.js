const fs = require('fs');
const path = require('path');

const PROJECT_ROOT = path.resolve(__dirname, '..');
const PUBLIC_DIR = path.join(PROJECT_ROOT, 'public');
const LANG_DIR = path.join(PUBLIC_DIR, 'assets', 'lang');

const LANGUAGES = ['pt', 'en', 'es'];

function getAllHtmlFiles(dir, fileList = []) {
  const files = fs.readdirSync(dir);

  files.forEach(file => {
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);

    if (stat.isDirectory()) {
      getAllHtmlFiles(fullPath, fileList);
    } else if (file.endsWith('.html')) {
      fileList.push(fullPath);
    }
  });

  return fileList;
}

function extractI18nKeysFromHtml(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const regex = /data-i18n="([^"]+)"/g;
  const keys = new Set();

  let match;
  while ((match = regex.exec(content)) !== null) {
    keys.add(match[1]);
  }

  return keys;
}

function flattenObject(obj, prefix = '', result = {}) {
  for (let key in obj) {
    const newKey = prefix ? `${prefix}.${key}` : key;
    if (typeof obj[key] === 'object' && obj[key] !== null) {
      flattenObject(obj[key], newKey, result);
    } else {
      result[newKey] = obj[key];
    }
  }
  return result;
}

function loadLanguage(lang) {
  const filePath = path.join(LANG_DIR, `${lang}.json`);
  if (!fs.existsSync(filePath)) {
    console.error(`❌ Arquivo de idioma não encontrado: ${lang}.json`);
    process.exit(1);
  }

  const raw = fs.readFileSync(filePath, 'utf8');
  const parsed = JSON.parse(raw);
  return flattenObject(parsed);
}

function main() {
  console.log('🔎 Iniciando verificação de chaves i18n...\n');

  const htmlFiles = getAllHtmlFiles(PUBLIC_DIR);

  const usedKeys = new Set();

  htmlFiles.forEach(file => {
    const keys = extractI18nKeysFromHtml(file);
    keys.forEach(k => usedKeys.add(k));
  });

  console.log(`📄 HTML analisados: ${htmlFiles.length}`);
  console.log(`🔑 Total de chaves encontradas: ${usedKeys.size}\n`);

  const languageMaps = {};
  LANGUAGES.forEach(lang => {
    languageMaps[lang] = loadLanguage(lang);
  });

  let hasError = false;

  usedKeys.forEach(key => {
    LANGUAGES.forEach(lang => {
      if (!languageMaps[lang][key]) {
        console.error(`❌ Chave faltando em ${lang}.json → ${key}`);
        hasError = true;
      }
    });
  });

  if (hasError) {
    console.error('\n🚨 Falha: inconsistência detectada nas traduções.');
    process.exit(1);
  }

  console.log('✅ Todas as chaves estão sincronizadas.');
  process.exit(0);
}

main();
