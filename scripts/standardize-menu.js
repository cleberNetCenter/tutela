#!/usr/bin/env node

/**
 * PADRONIZA MENU DE NAVEGAÇÃO
 * Aplica o menu padrão (com i18n) em todas as páginas
 */

const fs = require('fs');
const path = require('path');
const glob = require('glob');

const ROOT = path.join(__dirname, '..');

// Menu padrão (extraído de public/index.html)
const STANDARD_NAV = `<nav class="nav" id="nav">
<a class="nav-link" href="/"><span data-i18n="nav.home">Início</span></a>
<a class="nav-link" href="/como-funciona.html"><span data-i18n="nav.how_it_works">Como Funciona</span></a>
<a class="nav-link" href="/seguranca.html"><span data-i18n="nav.security">Segurança</span></a>

<div class="nav-dropdown">
<a href="#" class="nav-link"><span data-i18n="nav.solutions">Soluções</span></a>
<ul class="dropdown-menu">
<li><a href="/governo.html">Governo</a></li>
<li><a href="/empresas.html">Empresas</a></li>
<li><a href="/pessoas.html">Pessoas</a></li>
</ul>
</div>

<div class="nav-dropdown">
<a href="#" class="nav-link"><span data-i18n="nav.legal_basis">Base Jurídica</span></a>
<ul class="dropdown-menu">
<li><a href="/legal/preservacao-probatoria-digital.html">Preservação Probatória</a></li>
<li><a href="/legal/fundamento-juridico.html">Fundamento Jurídico</a></li>
<li><a href="/legal/termos-de-custodia.html">Termos de Custódia</a></li>
<li><a href="/legal/politica-de-privacidade.html">Política de Privacidade</a></li>
<li><a href="/legal/institucional.html">Institucional</a></li>
</ul>
</div>
</nav>`;

// Lista de páginas a serem atualizadas (excluindo testes e EN/ES que precisam tratamento especial)
const pagesToUpdate = [
  'public/legal/termos-de-custodia.html',
  'public/legal/preservacao-probatoria-digital.html',
  'public/legal/politica-de-privacidade.html',
  'public/legal/institucional.html',
  'public/legal/fundamento-juridico.html'
];

console.log('🔧 PADRONIZANDO MENUS DE NAVEGAÇÃO\n');

let updatedCount = 0;

pagesToUpdate.forEach(file => {
  const filePath = path.join(ROOT, file);
  
  if (!fs.existsSync(filePath)) {
    console.log(`⚠️  Arquivo não encontrado: ${file}`);
    return;
  }
  
  let html = fs.readFileSync(filePath, 'utf8');
  
  // Substitui o bloco <nav>...</nav>
  const navRegex = /<nav[^>]*>[\s\S]*?<\/nav>/;
  
  if (navRegex.test(html)) {
    html = html.replace(navRegex, STANDARD_NAV);
    fs.writeFileSync(filePath, html, 'utf8');
    console.log(`✅ ${file}`);
    updatedCount++;
  } else {
    console.log(`⚠️  <nav> não encontrado: ${file}`);
  }
});

console.log(`\n✅ PADRONIZAÇÃO CONCLUÍDA: ${updatedCount} arquivo(s) atualizado(s)\n`);

// Verifica resultado
console.log('🔍 Verificando resultado...\n');
const { execSync } = require('child_process');
try {
  execSync('node scripts/check-menu-consistency.js', { 
    cwd: ROOT,
    stdio: 'inherit' 
  });
} catch (e) {
  // Script já exibe resultado
}
