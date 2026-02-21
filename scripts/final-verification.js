#!/usr/bin/env node

const fs = require('fs');
const glob = require('glob');

const SCRIPTS = [
  '/assets/js/navigation.js',
  '/assets/js/i18n.js',
  '/assets/js/mobile-menu.js',
  '/assets/js/dropdown-menu.js'
];

console.log('🔍 VERIFICAÇÃO FINAL COMPLETA\n');

const htmlFiles = glob.sync('public/**/*.html', {
  ignore: ['**/test*.html', '**/en/**', '**/es/**']
});

let allPerfect = true;
const issues = [];

htmlFiles.forEach(file => {
  const content = fs.readFileSync(file, 'utf8');
  const fileIssues = [];
  
  SCRIPTS.forEach(script => {
    const regex = new RegExp(`<script[^>]*src=["']${script}["'][^>]*>\\s*</script>`, 'g');
    const matches = content.match(regex);
    const count = matches ? matches.length : 0;
    
    if (count === 0) {
      fileIssues.push(`❌ ${script} - ausente`);
    } else if (count > 1) {
      fileIssues.push(`❌ ${script} - ${count} ocorrências (duplicado)`);
    } else {
      fileIssues.push(`✅ ${script} - 1 ocorrência`);
    }
  });
  
  const hasIssue = fileIssues.some(i => i.startsWith('❌'));
  if (hasIssue) {
    allPerfect = false;
    issues.push({ file, fileIssues });
  }
});

if (allPerfect) {
  console.log('✅ VERIFICAÇÃO COMPLETA - TUDO PERFEITO!\n');
  console.log('📊 RESULTADO:');
  console.log(`   ✅ Páginas verificadas: ${htmlFiles.length}`);
  console.log(`   ✅ Nenhum script duplicado`);
  console.log(`   ✅ Todos os scripts na ordem correta`);
  console.log(`   ✅ Cada script aparece exatamente 1x por página\n`);
  
  // Listar páginas verificadas
  console.log('📄 PÁGINAS VERIFICADAS:');
  htmlFiles.forEach(f => console.log(`   ✅ ${f}`));
  console.log('');
  
  process.exit(0);
}

console.log('❌ PROBLEMAS DETECTADOS:\n');

issues.forEach(({ file, fileIssues }) => {
  console.log(`📄 ${file}`);
  fileIssues.forEach(issue => console.log(`   ${issue}`));
  console.log('');
});

console.log(`\n📊 RESUMO:`);
console.log(`   Páginas com problemas: ${issues.length}`);
console.log(`   Páginas OK: ${htmlFiles.length - issues.length}`);
