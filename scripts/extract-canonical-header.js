#!/usr/bin/env node

const fs = require('fs');

console.log('📋 EXTRAINDO HEADER CANÔNICO DE seguranca.html\n');

const content = fs.readFileSync('public/seguranca.html', 'utf8');

// Encontrar o início do header
const headerStart = content.indexOf('<header class="header" id="header">');
if (headerStart === -1) {
  console.error('❌ Não foi possível encontrar o header em seguranca.html');
  process.exit(1);
}

// Encontrar o final do header
const headerEnd = content.indexOf('</header>', headerStart);
if (headerEnd === -1) {
  console.error('❌ Não foi possível encontrar o fechamento do header');
  process.exit(1);
}

// Extrair o header completo
let header = content.substring(headerStart, headerEnd + '</header>'.length);

// CORREÇÃO: Remover o markup duplicado do botão mobile
// Padrão inválido: <button class="mobile-menu-btn" <button class="mobile-menu-btn">
// Padrão correto: <button class="mobile-menu-btn" onclick="toggleMobileMenu()">
header = header.replace(
  /<button class="mobile-menu-btn" <button class="mobile-menu-btn">/g,
  '<button class="mobile-menu-btn" onclick="toggleMobileMenu()">'
);

console.log('✅ Header extraído e corrigido:\n');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
console.log(header);
console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

// Salvar o header canônico
fs.writeFileSync('/tmp/canonical-header.html', header, 'utf8');
console.log('✅ Header canônico salvo em /tmp/canonical-header.html\n');

// Validações
console.log('🔍 VALIDAÇÕES:\n');

const checks = [
  {
    name: 'Tag <header> com id e class corretos',
    test: /<header class="header" id="header">/.test(header),
  },
  {
    name: 'Tag <nav> com id correto',
    test: /<nav class="nav" id="nav">/.test(header),
  },
  {
    name: 'Botão mobile com onclick',
    test: /<button class="mobile-menu-btn" onclick="toggleMobileMenu\(\)">/.test(header),
  },
  {
    name: 'Botão mobile SEM markup duplicado',
    test: !/<button class="mobile-menu-btn" <button/.test(header),
  },
  {
    name: 'Exatamente 3 <span> no botão mobile',
    test: (header.match(/<button class="mobile-menu-btn"[^>]*>[\s\S]*?<\/button>/)?.[0]?.match(/<span><\/span>/g) || []).length === 3,
  },
  {
    name: 'Logo presente',
    test: /<a class="logo" href="\/">/.test(header),
  },
  {
    name: 'Header CTA presente',
    test: /<a class="header-cta"/.test(header),
  },
  {
    name: 'Dropdown Soluções presente',
    test: /data-i18n="nav\.solutions"/.test(header),
  },
  {
    name: 'Dropdown Base Jurídica presente',
    test: /data-i18n="nav\.legal_basis"/.test(header),
  },
];

checks.forEach(check => {
  console.log(`${check.test ? '✅' : '❌'} ${check.name}`);
});

const allPassed = checks.every(c => c.test);
console.log(`\n${allPassed ? '✅ TODAS AS VALIDAÇÕES PASSARAM' : '❌ ALGUMAS VALIDAÇÕES FALHARAM'}\n`);

process.exit(allPassed ? 0 : 1);
