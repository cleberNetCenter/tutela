#!/usr/bin/env node

const fs = require('fs');
const glob = require('glob');

console.log('🔧 CORRIGINDO SCRIPTS DUPLICADOS E AUSENTES\n');

const htmlFiles = glob.sync('public/**/*.html', {
  ignore: ['**/test*.html', '**/en/**', '**/es/**']
});

let fixedFiles = 0;
const changes = [];

htmlFiles.forEach(file => {
  let content = fs.readFileSync(file, 'utf8');
  let modified = false;
  const fileChanges = [];
  
  // 1. Remover duplicatas de navigation.js
  const navMatches = content.match(/<script[^>]*src=["'][\/]?assets\/js\/navigation\.js[^"']*["'][^>]*>\s*<\/script>/g);
  if (navMatches && navMatches.length > 1) {
    // Manter apenas a primeira ocorrência
    const firstNav = navMatches[0];
    // Remover todas
    navMatches.forEach(match => {
      content = content.replace(match, '');
    });
    // Adicionar apenas uma no final antes de </body>
    content = content.replace('</body>', `${firstNav}\n</body>`);
    modified = true;
    fileChanges.push(`Removidas ${navMatches.length - 1} duplicatas de navigation.js`);
  }
  
  // 2. Remover duplicatas de dropdown-menu.js
  const dropdownMatches = content.match(/<script[^>]*src=["'][\/]?assets\/js\/dropdown-menu\.js[^"']*["'][^>]*>\s*<\/script>/g);
  if (dropdownMatches && dropdownMatches.length > 1) {
    // Manter apenas a primeira ocorrência
    const firstDropdown = dropdownMatches[0];
    // Remover todas
    dropdownMatches.forEach(match => {
      content = content.replace(match, '');
    });
    // Adicionar apenas uma no final antes de </body>
    content = content.replace('</body>', `${firstDropdown}\n</body>`);
    modified = true;
    fileChanges.push(`Removidas ${dropdownMatches.length - 1} duplicatas de dropdown-menu.js`);
  }
  
  // 3. Adicionar navigation.js ausente (para páginas que não têm nenhuma ocorrência)
  const hasNav = /<script[^>]*src=["'][\/]?assets\/js\/navigation\.js/g.test(content);
  if (!hasNav) {
    // Adicionar antes de i18n.js ou no início dos scripts
    const i18nMatch = content.match(/<script[^>]*src=["'][\/]?assets\/js\/i18n\.js[^"']*["'][^>]*>\s*<\/script>/);
    if (i18nMatch) {
      content = content.replace(i18nMatch[0], `<script src="assets/js/navigation.js?v=202602190108"></script>\n${i18nMatch[0]}`);
      modified = true;
      fileChanges.push('Adicionado navigation.js ausente');
    }
  }
  
  if (modified) {
    fs.writeFileSync(file, content, 'utf8');
    fixedFiles++;
    changes.push({ file, fileChanges });
  }
});

console.log('📊 CORREÇÕES APLICADAS:\n');

if (changes.length === 0) {
  console.log('✅ Nenhuma correção necessária!\n');
  process.exit(0);
}

changes.forEach(({ file, fileChanges }) => {
  console.log(`📄 ${file}`);
  fileChanges.forEach(change => console.log(`   ✅ ${change}`));
  console.log('');
});

console.log(`\n✅ CONCLUÍDO: ${fixedFiles} arquivo(s) corrigido(s)\n`);
