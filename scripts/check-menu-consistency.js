#!/usr/bin/env node

/**
 * VERIFICA CONSISTÊNCIA DOS MENUS
 * Extrai e compara o menu de navegação de todas as páginas HTML
 */

const fs = require('fs');
const path = require('path');
const glob = require('glob');

const ROOT = path.join(__dirname, '..');

// Encontra todos os arquivos HTML
const htmlFiles = glob.sync('public/**/*.html', { cwd: ROOT });

console.log('🔍 VERIFICANDO CONSISTÊNCIA DOS MENUS\n');
console.log(`📁 Arquivos HTML encontrados: ${htmlFiles.length}\n`);

// Extrai menu de cada página
const menus = {};

htmlFiles.forEach(file => {
  const filePath = path.join(ROOT, file);
  const html = fs.readFileSync(filePath, 'utf8');
  
  // Extrai o bloco <nav>...</nav>
  const navMatch = html.match(/<nav[^>]*>([\s\S]*?)<\/nav>/);
  
  if (navMatch) {
    const navContent = navMatch[1]
      .replace(/\s+/g, ' ')  // Normaliza espaços
      .replace(/\t/g, '')     // Remove tabs
      .trim();
    
    menus[file] = navContent;
  } else {
    menus[file] = 'NAV NÃO ENCONTRADO';
  }
});

// Agrupa páginas com menus idênticos
const menuGroups = {};
Object.entries(menus).forEach(([file, content]) => {
  const hash = content.substring(0, 50); // Primeiros 50 chars como hash
  if (!menuGroups[hash]) {
    menuGroups[hash] = { content, files: [] };
  }
  menuGroups[hash].files.push(file);
});

// Exibe resultados
console.log(`\n📊 GRUPOS DE MENUS ENCONTRADOS: ${Object.keys(menuGroups).length}\n`);

Object.entries(menuGroups).forEach(([hash, { content, files }], index) => {
  console.log(`\n─────────────────────────────────────────────────`);
  console.log(`GRUPO ${index + 1} (${files.length} página(s)):`);
  console.log(`─────────────────────────────────────────────────`);
  
  files.forEach(f => console.log(`  📄 ${f}`));
  
  console.log(`\n  📝 Menu (primeiros 200 caracteres):`);
  console.log(`  ${content.substring(0, 200)}...`);
});

// Identifica o grupo majoritário
const sortedGroups = Object.entries(menuGroups)
  .sort((a, b) => b[1].files.length - a[1].files.length);

console.log(`\n\n═══════════════════════════════════════════════════`);
console.log(`RESULTADO:`);
console.log(`═══════════════════════════════════════════════════`);

if (sortedGroups.length === 1) {
  console.log(`✅ TODOS OS MENUS SÃO IDÊNTICOS`);
} else {
  const [majorityHash, majorityGroup] = sortedGroups[0];
  console.log(`⚠️  MENUS INCONSISTENTES DETECTADOS`);
  console.log(`\n📌 Menu padrão (${majorityGroup.files.length} páginas):`);
  majorityGroup.files.forEach(f => console.log(`   ${f}`));
  
  console.log(`\n❌ Páginas com menu diferente:`);
  sortedGroups.slice(1).forEach(([hash, { files }]) => {
    files.forEach(f => console.log(`   ${f}`));
  });
}

console.log(`\n✅ VERIFICAÇÃO CONCLUÍDA\n`);
