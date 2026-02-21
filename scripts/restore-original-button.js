#!/usr/bin/env node

const fs = require('fs');
const glob = require('glob');

console.log('🔄 RESTAURANDO MARKUP ORIGINAL DO BOTÃO MOBILE\n');

// Markup original de seguranca.html (SEM correção)
const originalButton = '<button class="mobile-menu-btn" <button class="mobile-menu-btn">';
const correctedButton = '<button class="mobile-menu-btn" onclick="toggleMobileMenu()">';

console.log('❌ Removendo correção aplicada incorretamente...\n');
console.log(`Substituindo: ${correctedButton}`);
console.log(`Por:          ${originalButton}\n`);

const htmlFiles = glob.sync('public/**/*.html', {
  ignore: ['**/test*.html', '**/en/**', '**/es/**']
});

console.log(`📄 ${htmlFiles.length} arquivos HTML encontrados\n`);

let modified = 0;

htmlFiles.forEach(file => {
  let content = fs.readFileSync(file, 'utf8');
  
  if (content.includes(correctedButton)) {
    content = content.replace(correctedButton, originalButton);
    fs.writeFileSync(file, content, 'utf8');
    modified++;
    console.log(`✅ ${file}`);
  }
});

console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
console.log(`📊 RESUMO:\n`);
console.log(`✅ Arquivos modificados: ${modified}`);
console.log(`⏭️  Arquivos não modificados: ${htmlFiles.length - modified}\n`);

if (modified > 0) {
  console.log('✅ MARKUP ORIGINAL RESTAURADO EM TODAS AS PÁGINAS\n');
  console.log('📝 Nota: O markup original de seguranca.html foi preservado\n');
} else {
  console.log('⚠️  Nenhum arquivo precisou ser modificado\n');
}

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
