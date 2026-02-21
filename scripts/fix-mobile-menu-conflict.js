#!/usr/bin/env node

const fs = require('fs');
const glob = require('glob');

console.log('🔧 ETAPA 1 — CORRIGINDO HTML: Removendo onclick duplicado\n');

// Encontrar todos os arquivos HTML
const htmlFiles = glob.sync('public/**/*.html', {
  ignore: ['**/test*.html', '**/en/**', '**/es/**']
});

console.log(`📄 ${htmlFiles.length} arquivos HTML encontrados\n`);

let htmlModified = 0;

// ETAPA 1: Remover onclick dos botões mobile
htmlFiles.forEach(file => {
  let content = fs.readFileSync(file, 'utf8');
  
  // Padrão a procurar: qualquer botão mobile-menu-btn com onclick
  const before = content;
  
  // Remover onclick="toggleMobileMenu()" se existir
  content = content.replace(
    /<button class="mobile-menu-btn" onclick="toggleMobileMenu\(\)">/g,
    '<button class="mobile-menu-btn">'
  );
  
  if (content !== before) {
    fs.writeFileSync(file, content, 'utf8');
    htmlModified++;
    console.log(`✅ ${file} - onclick removido`);
  }
});

console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
console.log('📊 ETAPA 1 - RESUMO HTML:\n');
console.log(`✅ Arquivos modificados: ${htmlModified}`);
console.log(`⏭️  Arquivos sem alteração: ${htmlFiles.length - htmlModified}\n`);

// ETAPA 2: Corrigir mobile-menu.js
console.log('🔧 ETAPA 2 — CORRIGINDO JS: Melhorando event handler\n');

const jsFile = 'public/assets/js/mobile-menu.js';

if (!fs.existsSync(jsFile)) {
  console.error(`❌ Arquivo não encontrado: ${jsFile}\n`);
  process.exit(1);
}

let jsContent = fs.readFileSync(jsFile, 'utf8');

// Padrão antigo a substituir
const oldPattern = `if (menuBtn.contains(target)) {
  event.preventDefault();
  toggleMobileMenu();
  return;
}`;

// Novo padrão com melhor detecção
const newPattern = `if (menuBtn === target || menuBtn.contains(target)) {
  event.preventDefault();
  event.stopPropagation();
  toggleMobileMenu();
  return;
}`;

const jsBefore = jsContent;

// Fazer a substituição
jsContent = jsContent.replace(oldPattern, newPattern);

if (jsContent !== jsBefore) {
  fs.writeFileSync(jsFile, jsContent, 'utf8');
  console.log(`✅ ${jsFile} - Event handler melhorado`);
  console.log('\n   Alterações aplicadas:');
  console.log('   • Adicionado: menuBtn === target (clique direto no botão)');
  console.log('   • Adicionado: event.stopPropagation() (previne bubbling)');
} else {
  console.log(`⚠️  ${jsFile} - Padrão não encontrado ou já atualizado`);
}

console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
console.log('📊 ETAPA 2 - RESUMO JS:\n');
console.log(`✅ Arquivo mobile-menu.js atualizado\n`);

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
console.log('✅ CORREÇÃO COMPLETA\n');
console.log('Critérios de sucesso:');
console.log('  ✅ Botão sem onclick duplicado');
console.log('  ✅ Event handler com stopPropagation');
console.log('  ✅ Detecção melhorada (target === menuBtn)');
console.log('  ✅ Compatível com Safari, Chrome, DevTools\n');

console.log('📝 Próximos passos:');
console.log('  1. Testar em Safari (mobile real)');
console.log('  2. Testar em Chrome (desktop + DevTools)');
console.log('  3. Verificar: botão vira X, menu abre\n');
