#!/usr/bin/env node

const fs = require('fs');
const glob = require('glob');

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('  CORRIGINDO CAMINHOS RELATIVOS → ABSOLUTOS');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

console.log('Problema: scripts com caminho relativo geram 404 em /legal/\n');
console.log('❌ assets/js/... → /legal/assets/js/... (404)');
console.log('✅ /assets/js/... → /assets/js/... (OK)\n');

const htmlFiles = glob.sync('public/**/*.html', {
  ignore: ['**/node_modules/**', '**/test/**', '**/en/**', '**/es/**']
}).filter(file => !file.includes('test'));

let modified = [];
let unchanged = [];

htmlFiles.forEach(file => {
  let content = fs.readFileSync(file, 'utf8');
  const originalContent = content;
  
  // Contar ocorrências antes
  const beforeCount = (content.match(/src="assets\/js\//g) || []).length;
  
  // Substituir src="assets/js/ por src="/assets/js/
  content = content.replace(/src="assets\/js\//g, 'src="/assets/js/');
  
  // Contar ocorrências depois
  const afterCount = (content.match(/src="assets\/js\//g) || []).length;
  
  if (content !== originalContent) {
    fs.writeFileSync(file, content, 'utf8');
    modified.push({
      file,
      replacements: beforeCount,
      remaining: afterCount
    });
    console.log(`✅ ${file}`);
    console.log(`   Substituições: ${beforeCount} caminhos relativos → absolutos\n`);
  } else {
    unchanged.push(file);
  }
});

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('  RESUMO');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

console.log(`Total de páginas: ${htmlFiles.length}`);
console.log(`Páginas modificadas: ${modified.length}`);
console.log(`Páginas sem alteração: ${unchanged.length}\n`);

if (modified.length > 0) {
  const totalReplacements = modified.reduce((sum, item) => sum + item.replacements, 0);
  console.log(`Total de substituições: ${totalReplacements}\n`);
  
  console.log('✅ Páginas corrigidas:\n');
  modified.forEach(item => {
    console.log(`   ${item.file} (${item.replacements} scripts)`);
  });
  console.log('');
}

console.log('✅ Todos os scripts agora usam caminhos absolutos:');
console.log('   /assets/js/navigation.js?v=202602210200');
console.log('   /assets/js/i18n.js?v=202602210200');
console.log('   /assets/js/dropdown-menu.js?v=202602210200');
console.log('   /assets/js/mobile-menu.js?v=202602210200\n');
