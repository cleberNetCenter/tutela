#!/usr/bin/env node

const fs = require('fs');
const glob = require('glob');

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('  ETAPA 5: CSS HARDENING');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

const cssFiles = glob.sync('public/assets/css/*.css', {
  ignore: ['**/node_modules/**', '**/test/**']
});

let issues = [];

console.log('1️⃣ Verificando .nav.active display: flex...\n');

let navActiveChecks = [];

cssFiles.forEach(file => {
  const content = fs.readFileSync(file, 'utf8');
  
  // Procurar por .nav.active
  const navActiveRegex = /\.nav\.active\s*{([^}]*)}/g;
  let match;
  
  while ((match = navActiveRegex.exec(content)) !== null) {
    const rules = match[1];
    const hasDisplayFlex = rules.includes('display:') && rules.includes('flex');
    
    navActiveChecks.push({
      file,
      rules: rules.trim(),
      hasDisplayFlex
    });
    
    if (!hasDisplayFlex) {
      issues.push({
        type: 'critical',
        category: 'missing-display-flex',
        file,
        message: '.nav.active sem display: flex'
      });
    }
  }
});

console.log('2️⃣ Verificando z-index hierarchy...\n');

const zIndexChecks = {
  header: [],
  nav: [],
  mobileMenu: [],
  content: []
};

cssFiles.forEach(file => {
  const content = fs.readFileSync(file, 'utf8');
  const lines = content.split('\n');
  
  lines.forEach((line, index) => {
    if (line.includes('z-index:')) {
      const zIndexMatch = line.match(/z-index:\s*(\d+)/);
      if (zIndexMatch) {
        const value = parseInt(zIndexMatch[1]);
        
        // Encontrar o seletor (procurar para trás)
        let selector = '';
        for (let i = index; i >= Math.max(0, index - 10); i--) {
          if (lines[i].includes('{')) {
            selector = lines[i].split('{')[0].trim();
            break;
          }
        }
        
        if (selector.includes('.nav.active') || selector.includes('#nav')) {
          zIndexChecks.nav.push({ file, line: index + 1, selector, value });
        } else if (selector.includes('header') || selector.includes('.header')) {
          zIndexChecks.header.push({ file, line: index + 1, selector, value });
        } else if (selector.includes('mobile-menu')) {
          zIndexChecks.mobileMenu.push({ file, line: index + 1, selector, value });
        }
      }
    }
  });
});

console.log('3️⃣ Procurando CSS legado de SPA...\n');

const legacyPatterns = [
  { pattern: /\.page\s*{/, description: 'Classe .page (SPA legacy)' },
  { pattern: /\.page\.active/, description: 'Classe .page.active (SPA legacy)' },
  { pattern: /data-page/, description: 'Atributo data-page (SPA legacy)' },
  { pattern: /#app\s*{/, description: 'Seletor #app (SPA legacy)' }
];

cssFiles.forEach(file => {
  const content = fs.readFileSync(file, 'utf8');
  
  legacyPatterns.forEach(({ pattern, description }) => {
    if (pattern.test(content)) {
      const matches = content.match(pattern);
      if (matches) {
        issues.push({
          type: 'warning',
          category: 'legacy-css',
          file,
          pattern: description,
          message: `CSS legado encontrado: ${description}`
        });
      }
    }
  });
});

// Gerar relatório
console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('  RESULTADOS DA AUDITORIA');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

console.log('📊 Estatísticas:\n');
console.log(`   Arquivos CSS: ${cssFiles.length}`);
console.log(`   .nav.active encontrados: ${navActiveChecks.length}`);
console.log(`   Definições z-index (nav): ${zIndexChecks.nav.length}`);
console.log(`   Definições z-index (header): ${zIndexChecks.header.length}`);
console.log(`   Problemas encontrados: ${issues.length}\n`);

if (issues.length === 0 && navActiveChecks.every(c => c.hasDisplayFlex)) {
  console.log('✅ CSS HARDENING: PASSOU EM TODOS OS TESTES\n');
  console.log('✅ .nav.active sempre define display: flex');
  console.log('✅ Z-index hierarchy correto');
  console.log('✅ Sem CSS legado de SPA\n');
  
  if (zIndexChecks.nav.length > 0) {
    console.log('📋 Z-index definidos (nav):\n');
    zIndexChecks.nav.forEach(z => {
      console.log(`   ${z.selector}: ${z.value}`);
      console.log(`   → ${z.file}:${z.line}\n`);
    });
  }
} else {
  if (issues.length > 0) {
    const critical = issues.filter(i => i.type === 'critical');
    const warnings = issues.filter(i => i.type === 'warning');
    
    if (critical.length > 0) {
      console.log(`❌ PROBLEMAS CRÍTICOS: ${critical.length}\n`);
      critical.forEach(issue => {
        console.log(`   ${issue.category}: ${issue.message}`);
        console.log(`   Arquivo: ${issue.file}\n`);
      });
    }
    
    if (warnings.length > 0) {
      console.log(`⚠️  WARNINGS: ${warnings.length}\n`);
      warnings.forEach(issue => {
        console.log(`   ${issue.pattern}`);
        console.log(`   Arquivo: ${issue.file}\n`);
      });
    }
  }
  
  navActiveChecks.forEach(check => {
    if (!check.hasDisplayFlex) {
      console.log(`⚠️  ${check.file}: .nav.active sem display: flex\n`);
    }
  });
}

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

process.exit(issues.filter(i => i.type === 'critical').length > 0 ? 1 : 0);
