#!/usr/bin/env node

const fs = require('fs');

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('  VERIFICAÇÃO: FIX SOBREPOSIÇÃO DE DROPDOWNS');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

let allCorrect = true;

// Verificar CSS
console.log('1️⃣ Verificando CSS (dropdown-menu.css)...\n');

const cssContent = fs.readFileSync('public/assets/css/dropdown-menu.css', 'utf8');

// Verificar remoção de hover/focus-within
const hasHover = cssContent.includes('.nav-dropdown:hover .dropdown-menu');
const hasFocusWithin = cssContent.includes('.nav-dropdown:focus-within .dropdown-menu');

if (hasHover) {
  console.log('❌ ERRO: Ainda contém regra :hover');
  allCorrect = false;
} else {
  console.log('✅ Regra :hover removida');
}

if (hasFocusWithin) {
  console.log('❌ ERRO: Ainda contém regra :focus-within');
  allCorrect = false;
} else {
  console.log('✅ Regra :focus-within removida');
}

// Verificar manutenção da regra .active
const hasActive = cssContent.includes('.nav-dropdown.active .dropdown-menu');
if (hasActive) {
  console.log('✅ Regra .active mantida');
} else {
  console.log('❌ ERRO: Regra .active não encontrada');
  allCorrect = false;
}

console.log('');

// Verificar JS
console.log('2️⃣ Verificando JS (mobile-menu.js)...\n');

const jsContent = fs.readFileSync('public/assets/js/mobile-menu.js', 'utf8');

// Verificar estrutura do novo código
const hasCloseAll = jsContent.includes('closeAllDropdowns();');
const hasWillOpen = jsContent.includes('const willOpen = !dropdown.classList.contains(\'active\');');
const hasAddActive = jsContent.includes('dropdown.classList.add(\'active\');');

if (hasCloseAll) {
  console.log('✅ closeAllDropdowns() presente');
} else {
  console.log('❌ ERRO: closeAllDropdowns() não encontrado');
  allCorrect = false;
}

if (hasWillOpen) {
  console.log('✅ willOpen check presente');
} else {
  console.log('❌ ERRO: willOpen check não encontrado');
  allCorrect = false;
}

if (hasAddActive) {
  console.log('✅ dropdown.classList.add(\'active\') presente');
} else {
  console.log('❌ ERRO: dropdown.classList.add(\'active\') não encontrado');
  allCorrect = false;
}

// Verificar remoção de código antigo
const hasCanToggle = jsContent.includes('canToggleDropdown(nav)');
const hasToggleMethod = jsContent.includes('dropdown.classList.toggle(\'active\', willOpen)');

if (hasCanToggle) {
  console.log('⚠️  WARNING: canToggleDropdown ainda presente (pode ser usado em outro lugar)');
}

if (hasToggleMethod) {
  console.log('❌ ERRO: Código antigo com toggle ainda presente');
  allCorrect = false;
} else {
  console.log('✅ Código antigo removido');
}

console.log('');

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('  RESULTADO DA VERIFICAÇÃO');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

if (allCorrect) {
  console.log('✅ TODAS AS CORREÇÕES APLICADAS CORRETAMENTE\n');
  console.log('Comportamento esperado:');
  console.log('✅ Desktop: Click para abrir/fechar dropdown');
  console.log('✅ Mobile: Click para abrir/fechar dropdown');
  console.log('✅ Apenas UM dropdown aberto por vez');
  console.log('✅ Sem sobreposição de dropdowns');
  console.log('✅ closeAllDropdowns() fecha todos antes de abrir novo\n');
} else {
  console.log('❌ PROBLEMAS ENCONTRADOS - Revisar correções\n');
}

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

process.exit(allCorrect ? 0 : 1);
