#!/usr/bin/env node

/**
 * ADICIONA data-i18n NOS ITENS DOS DROPDOWNS
 * Garante que todos os links de dropdown sejam traduzíveis
 */

const fs = require('fs');
const path = require('path');
const glob = require('glob');

const ROOT = path.join(__dirname, '..');

// Mapa de texto → chave i18n
const DROPDOWN_I18N_MAP = {
  // Soluções
  'Governo': 'navigation.government',
  'Empresas': 'navigation.companies',
  'Pessoas': 'navigation.individuals',
  
  // Base Jurídica
  'Preservação Probatória': 'navigation.preservation',
  'Fundamento Jurídico': 'navigation.legalBasis',
  'Termos de Custódia': 'navigation.terms',
  'Política de Privacidade': 'navigation.privacy',
  'Institucional': 'navigation.institucional'
};

const htmlFiles = glob.sync('public/**/*.html', { 
  cwd: ROOT,
  ignore: ['**/test*.html', '**/en/**', '**/es/**']
});

console.log('🔧 ADICIONANDO data-i18n NOS DROPDOWNS\n');

let updatedCount = 0;

htmlFiles.forEach(file => {
  const filePath = path.join(ROOT, file);
  let html = fs.readFileSync(filePath, 'utf8');
  let modified = false;
  
  // Para cada mapeamento, adiciona data-i18n
  Object.entries(DROPDOWN_I18N_MAP).forEach(([text, i18nKey]) => {
    // Padrão: <li><a href="...">TEXT</a></li>
    const pattern = new RegExp(
      `<li><a href="([^"]+)">${text}</a></li>`,
      'g'
    );
    
    const replacement = `<li><a href="$1" data-i18n="${i18nKey}">${text}</a></li>`;
    
    if (pattern.test(html)) {
      html = html.replace(pattern, replacement);
      modified = true;
    }
  });
  
  if (modified) {
    fs.writeFileSync(filePath, html, 'utf8');
    console.log(`✅ ${file}`);
    updatedCount++;
  }
});

console.log(`\n✅ ATUALIZAÇÃO CONCLUÍDA: ${updatedCount} arquivo(s) modificado(s)\n`);

// Verifica resultado
console.log('🔍 Verificando resultado...\n');
const { execSync } = require('child_process');
try {
  execSync('node scripts/check-dropdown-i18n.js', { 
    cwd: ROOT,
    stdio: 'inherit' 
  });
} catch (e) {
  // Script já exibe resultado
}
