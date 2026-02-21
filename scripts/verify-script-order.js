#!/usr/bin/env node

const fs = require('fs');
const glob = require('glob');

// Ordem esperada
const EXPECTED_ORDER = [
  '/assets/js/navigation.js',
  '/assets/js/i18n.js',
  '/assets/js/mobile-menu.js',
  '/assets/js/dropdown-menu.js'
];

console.log('🔍 VERIFICANDO ORDEM DOS SCRIPTS\n');

const htmlFiles = glob.sync('public/**/*.html', {
  ignore: ['**/test*.html', '**/en/**', '**/es/**']
});

let allCorrect = true;
const report = [];

htmlFiles.forEach(file => {
  const content = fs.readFileSync(file, 'utf8');
  const foundScripts = [];
  
  EXPECTED_ORDER.forEach(script => {
    const regex = new RegExp(`<script[^>]*src=["']${script}["'][^>]*>`, 'g');
    const match = content.match(regex);
    if (match) {
      const index = content.indexOf(match[0]);
      foundScripts.push({ script, index });
    }
  });
  
  // Verificar ordem
  const sortedScripts = [...foundScripts].sort((a, b) => a.index - b.index);
  const currentOrder = sortedScripts.map(s => s.script);
  const expectedFiltered = EXPECTED_ORDER.filter(s => currentOrder.includes(s));
  
  const isCorrect = JSON.stringify(currentOrder) === JSON.stringify(expectedFiltered);
  
  if (!isCorrect) {
    allCorrect = false;
    report.push({
      file,
      current: currentOrder,
      expected: expectedFiltered
    });
  }
});

if (allCorrect) {
  console.log('✅ Todos os scripts estão na ordem correta!\n');
  console.log(`📊 Páginas verificadas: ${htmlFiles.length}\n`);
  process.exit(0);
}

console.log(`❌ PÁGINAS COM ORDEM INCORRETA: ${report.length}\n`);

report.forEach(({ file, current, expected }) => {
  console.log(`📄 ${file}`);
  console.log('   Ordem atual:');
  current.forEach((s, i) => console.log(`      ${i+1}. ${s}`));
  console.log('   Ordem esperada:');
  expected.forEach((s, i) => console.log(`      ${i+1}. ${s}`));
  console.log('');
});

console.log(`\n📊 RESUMO:`);
console.log(`   Páginas verificadas: ${htmlFiles.length}`);
console.log(`   Páginas com ordem incorreta: ${report.length}`);
console.log(`   Páginas corretas: ${htmlFiles.length - report.length}`);
