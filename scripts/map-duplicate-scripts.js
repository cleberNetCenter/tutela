#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const glob = require('glob');

// Scripts a verificar
const SCRIPTS = [
  '/assets/js/navigation.js',
  '/assets/js/i18n.js',
  '/assets/js/mobile-menu.js',
  '/assets/js/dropdown-menu.js'
];

console.log('🔍 MAPEANDO SCRIPTS DUPLICADOS\n');

// Encontrar todos os arquivos HTML (exceto test, en, es)
const htmlFiles = glob.sync('public/**/*.html', {
  ignore: ['**/test*.html', '**/en/**', '**/es/**']
});

const report = [];
let totalDuplicates = 0;

htmlFiles.forEach(file => {
  const content = fs.readFileSync(file, 'utf8');
  const duplicates = [];
  
  SCRIPTS.forEach(script => {
    const regex = new RegExp(`<script[^>]*src=["']${script}["'][^>]*>\\s*</script>`, 'g');
    const matches = content.match(regex);
    
    if (matches && matches.length > 1) {
      duplicates.push({
        script,
        count: matches.length
      });
      totalDuplicates += matches.length - 1;
    }
  });
  
  if (duplicates.length > 0) {
    report.push({
      file,
      duplicates
    });
  }
});

if (report.length === 0) {
  console.log('✅ Nenhum script duplicado encontrado!\n');
  process.exit(0);
}

console.log(`❌ DUPLICIDADES DETECTADAS: ${totalDuplicates} scripts duplicados\n`);

report.forEach(({ file, duplicates }) => {
  console.log(`📄 ${file}`);
  duplicates.forEach(({ script, count }) => {
    console.log(`   ❌ ${script} aparece ${count}x (${count - 1} duplicatas)`);
  });
  console.log('');
});

console.log(`\n📊 RESUMO:`);
console.log(`   Páginas com duplicidade: ${report.length}`);
console.log(`   Total de duplicatas: ${totalDuplicates}`);
