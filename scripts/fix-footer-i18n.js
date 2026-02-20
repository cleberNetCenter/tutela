#!/usr/bin/env node

/**
 * CORRIGE TRADUÇÕES DO RODAPÉ
 * Adiciona data-i18n nos títulos <h4> que estão fixos
 */

const fs = require('fs');
const path = require('path');
const glob = require('glob');

const ROOT = path.join(__dirname, '..');

// Encontra todos os arquivos HTML
const htmlFiles = glob.sync('public/**/*.html', { cwd: ROOT });

console.log(`🔧 CORRIGINDO TRADUÇÕES DO RODAPÉ\n`);
console.log(`📁 Arquivos HTML encontrados: ${htmlFiles.length}\n`);

let fixedCount = 0;

htmlFiles.forEach(file => {
  const filePath = path.join(ROOT, file);
  let html = fs.readFileSync(filePath, 'utf8');
  let modified = false;

  // Fix 1: Coluna "Plataforma" sem data-i18n
  if (html.includes('<h4>Plataforma</h4>')) {
    html = html.replace(
      '<h4>Plataforma</h4>',
      '<h4 data-i18n="footer.platform">Plataforma</h4>'
    );
    modified = true;
  }

  // Fix 2: Coluna "Público" sem data-i18n
  if (html.includes('<h4>Público</h4>')) {
    html = html.replace(
      '<h4>Público</h4>',
      '<h4 data-i18n="footer.audience">Público</h4>'
    );
    modified = true;
  }

  if (modified) {
    fs.writeFileSync(filePath, html, 'utf8');
    console.log(`✅ ${file}`);
    fixedCount++;
  }
});

console.log(`\n✅ CORREÇÃO CONCLUÍDA: ${fixedCount} arquivo(s) modificado(s)\n`);
