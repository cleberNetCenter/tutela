#!/usr/bin/env node

const fs = require('fs');
const glob = require('glob');

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('  ETAPA 2: MOBILE MENU HARDENING');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

let issues = [];

// 1. Verificar carregamento único de scripts
console.log('1️⃣ Verificando carregamento único de scripts...\n');

const htmlFiles = glob.sync('public/**/*.html', {
  ignore: ['**/node_modules/**', '**/test/**', '**/en/**', '**/es/**']
});

const scriptsToCheck = [
  'mobile-menu.js',
  'navigation.js',
  'dropdown-menu.js',
  'i18n.js'
];

htmlFiles.forEach(file => {
  const content = fs.readFileSync(file, 'utf8');
  
  scriptsToCheck.forEach(script => {
    const regex = new RegExp(`<script[^>]*src="[^"]*${script}[^"]*"`, 'g');
    const matches = content.match(regex) || [];
    
    if (matches.length > 1) {
      issues.push({
        type: 'critical',
        category: 'duplicate-script',
        file,
        script,
        count: matches.length,
        message: `Script ${script} carregado ${matches.length} vezes`
      });
    }
  });
});

// 2. Verificar onclick="toggleMobileMenu()" no HTML
console.log('2️⃣ Verificando onclick inline no HTML...\n');

htmlFiles.forEach(file => {
  const content = fs.readFileSync(file, 'utf8');
  const lines = content.split('\n');
  
  lines.forEach((line, index) => {
    if (line.includes('onclick=') && line.includes('toggleMobileMenu')) {
      issues.push({
        type: 'critical',
        category: 'inline-onclick',
        file,
        line: index + 1,
        content: line.trim(),
        message: 'onclick inline encontrado - deve ser 100% via JS'
      });
    }
  });
});

// 3. Verificar múltiplas definições de window.toggleMobileMenu
console.log('3️⃣ Verificando múltiplas definições de toggleMobileMenu...\n');

const jsFiles = glob.sync('public/**/*.js', {
  ignore: ['**/node_modules/**', '**/test/**', '**/en/**', '**/es/**']
});

let toggleDefinitions = [];

jsFiles.forEach(file => {
  const content = fs.readFileSync(file, 'utf8');
  const lines = content.split('\n');
  
  lines.forEach((line, index) => {
    if (line.includes('window.toggleMobileMenu') && line.includes('=')) {
      toggleDefinitions.push({
        file,
        line: index + 1,
        content: line.trim()
      });
    }
  });
});

if (toggleDefinitions.length > 1) {
  issues.push({
    type: 'critical',
    category: 'multiple-toggle-definitions',
    count: toggleDefinitions.length,
    definitions: toggleDefinitions,
    message: `window.toggleMobileMenu definido ${toggleDefinitions.length} vezes`
  });
}

// 4. Verificar breakpoint mobile único (max-width: 1200px)
console.log('4️⃣ Verificando breakpoints mobile...\n');

jsFiles.forEach(file => {
  const content = fs.readFileSync(file, 'utf8');
  
  // Procurar por definições de breakpoint
  const breakpointRegex = /(?:max-width|MOBILE_MAX_WIDTH|breakpoint).*?(\d{3,4})(?:px)?/gi;
  let match;
  
  while ((match = breakpointRegex.exec(content)) !== null) {
    const value = parseInt(match[1]);
    if (value !== 1200 && (value >= 900 && value <= 1400)) {
      issues.push({
        type: 'warning',
        category: 'inconsistent-breakpoint',
        file,
        value,
        message: `Breakpoint ${value}px encontrado (esperado: 1200px)`
      });
    }
  }
});

// 5. Verificar media query 900px controlando .nav
console.log('5️⃣ Verificando media queries CSS...\n');

const cssFiles = glob.sync('public/**/*.css', {
  ignore: ['**/node_modules/**', '**/test/**']
});

cssFiles.forEach(file => {
  const content = fs.readFileSync(file, 'utf8');
  
  // Procurar por media queries com 900px
  const mediaQueryRegex = /@media[^{]*\((?:max|min)-width:\s*900px\)[^{]*{[^}]*\.nav[^}]*}/g;
  const matches = content.match(mediaQueryRegex) || [];
  
  if (matches.length > 0) {
    issues.push({
      type: 'warning',
      category: 'legacy-media-query',
      file,
      count: matches.length,
      message: `Media query @media (max-width: 900px) controlando .nav encontrada`
    });
  }
});

// Gerar relatório
console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('  RESULTADOS DA AUDITORIA');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

const criticalIssues = issues.filter(i => i.type === 'critical');
const warnings = issues.filter(i => i.type === 'warning');

if (issues.length === 0) {
  console.log('✅ Mobile menu hardening: PASSOU EM TODOS OS TESTES\n');
  console.log('✅ Scripts carregados uma única vez');
  console.log('✅ Controle 100% via JS (sem onclick inline)');
  console.log('✅ window.toggleMobileMenu definido apenas uma vez');
  console.log('✅ Breakpoint mobile único (1200px)');
  console.log('✅ Sem media queries legadas (900px)\n');
} else {
  if (criticalIssues.length > 0) {
    console.log(`❌ PROBLEMAS CRÍTICOS: ${criticalIssues.length}\n`);
    criticalIssues.forEach(issue => {
      console.log(`   ${issue.category}: ${issue.message}`);
      if (issue.file) console.log(`   Arquivo: ${issue.file}`);
      if (issue.line) console.log(`   Linha: ${issue.line}`);
      if (issue.content) console.log(`   → ${issue.content}`);
      if (issue.definitions) {
        issue.definitions.forEach(def => {
          console.log(`   ${def.file}:${def.line}`);
          console.log(`   → ${def.content}`);
        });
      }
      console.log('');
    });
  }
  
  if (warnings.length > 0) {
    console.log(`⚠️  WARNINGS: ${warnings.length}\n`);
    warnings.forEach(issue => {
      console.log(`   ${issue.category}: ${issue.message}`);
      if (issue.file) console.log(`   Arquivo: ${issue.file}`);
      console.log('');
    });
  }
}

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

// Verificações adicionais
console.log('✅ Verificações adicionais:\n');
console.log(`   - Scripts verificados: ${scriptsToCheck.length}`);
console.log(`   - Páginas HTML: ${htmlFiles.length}`);
console.log(`   - Arquivos JS: ${jsFiles.length}`);
console.log(`   - Arquivos CSS: ${cssFiles.length}`);
console.log(`   - Definições toggleMobileMenu: ${toggleDefinitions.length}`);
console.log('');

process.exit(criticalIssues.length > 0 ? 1 : 0);
