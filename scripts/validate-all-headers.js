#!/usr/bin/env node

const fs = require('fs');
const glob = require('glob');

console.log('🔍 VALIDANDO TODOS OS HEADERS\n');

const htmlFiles = glob.sync('public/**/*.html', {
  ignore: ['**/test*.html', '**/en/**', '**/es/**']
});

console.log(`📄 Validando ${htmlFiles.length} arquivos HTML\n`);

const validations = [];
let allValid = true;

htmlFiles.forEach(file => {
  const content = fs.readFileSync(file, 'utf8');
  
  // Extrair apenas o header
  const headerMatch = content.match(/<header[\s\S]*?<\/header>/);
  if (!headerMatch) {
    validations.push({
      file,
      valid: false,
      errors: ['Header não encontrado']
    });
    allValid = false;
    return;
  }
  
  const header = headerMatch[0];
  const errors = [];
  
  // Validação 1: Tag <header> com id e class corretos
  if (!/<header class="header" id="header">/.test(header)) {
    errors.push('Tag <header> sem class="header" id="header" corretos');
  }
  
  // Validação 2: Tag <nav> com id correto
  if (!/<nav class="nav" id="nav">/.test(header)) {
    errors.push('Tag <nav> sem class="nav" id="nav" corretos');
  }
  
  // Validação 3: Botão mobile com onclick correto
  if (!/<button class="mobile-menu-btn" onclick="toggleMobileMenu\(\)">/.test(header)) {
    errors.push('Botão mobile sem onclick="toggleMobileMenu()" correto');
  }
  
  // Validação 4: Botão mobile SEM markup duplicado
  if (/<button class="mobile-menu-btn" <button/.test(header)) {
    errors.push('Botão mobile com markup duplicado/inválido');
  }
  
  // Validação 5: Exatamente 3 <span> no botão mobile
  const buttonMatch = header.match(/<button class="mobile-menu-btn"[^>]*>[\s\S]*?<\/button>/);
  if (buttonMatch) {
    const spans = (buttonMatch[0].match(/<span><\/span>/g) || []).length;
    if (spans !== 3) {
      errors.push(`Botão mobile tem ${spans} spans (esperado: 3)`);
    }
  } else {
    errors.push('Botão mobile não encontrado');
  }
  
  // Validação 6: Logo presente
  if (!/<a class="logo" href="\/">/.test(header)) {
    errors.push('Logo não encontrado ou com estrutura incorreta');
  }
  
  // Validação 7: Header CTA presente
  if (!/<a class="header-cta"/.test(header)) {
    errors.push('Header CTA não encontrado');
  }
  
  // Validação 8: Dropdown Soluções presente
  if (!/data-i18n="nav\.solutions"/.test(header)) {
    errors.push('Dropdown Soluções não encontrado');
  }
  
  // Validação 9: Dropdown Base Jurídica presente
  if (!/data-i18n="nav\.legal_basis"/.test(header)) {
    errors.push('Dropdown Base Jurídica não encontrado');
  }
  
  // Validação 10: Dropdown de idioma presente
  if (!/<div class="lang-dropdown">/.test(header)) {
    errors.push('Dropdown de idioma não encontrado');
  }
  
  validations.push({
    file,
    valid: errors.length === 0,
    errors
  });
  
  if (errors.length > 0) {
    allValid = false;
  }
});

// Exibir resultados
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

validations.forEach(({ file, valid, errors }) => {
  if (valid) {
    console.log(`✅ ${file}`);
  } else {
    console.log(`❌ ${file}`);
    errors.forEach(err => console.log(`   ❌ ${err}`));
  }
});

console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

const validCount = validations.filter(v => v.valid).length;
const invalidCount = validations.filter(v => !v.valid).length;

console.log('📊 RESUMO DE VALIDAÇÃO:\n');
console.log(`✅ Headers válidos: ${validCount}`);
console.log(`❌ Headers inválidos: ${invalidCount}`);
console.log(`📄 Total de páginas: ${htmlFiles.length}\n`);

if (allValid) {
  console.log('✅ TODOS OS HEADERS ESTÃO PADRONIZADOS E VÁLIDOS!\n');
} else {
  console.log('❌ ALGUNS HEADERS AINDA TÊM PROBLEMAS\n');
}

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

process.exit(allValid ? 0 : 1);
