#!/usr/bin/env node

const fs = require('fs');
const glob = require('glob');

// Possíveis caminhos de scripts (com e sem barra inicial)
const SCRIPT_PATTERNS = [
  { name: 'navigation.js', patterns: ['assets/js/navigation.js', '/assets/js/navigation.js'] },
  { name: 'i18n.js', patterns: ['assets/js/i18n.js', '/assets/js/i18n.js'] },
  { name: 'mobile-menu.js', patterns: ['assets/js/mobile-menu.js', '/assets/js/mobile-menu.js'] },
  { name: 'dropdown-menu.js', patterns: ['assets/js/dropdown-menu.js', '/assets/js/dropdown-menu.js'] }
];

console.log('🔍 MAPEANDO TODOS OS SCRIPTS\n');

const htmlFiles = glob.sync('public/**/*.html', {
  ignore: ['**/test*.html', '**/en/**', '**/es/**']
});

const report = [];

htmlFiles.forEach(file => {
  const content = fs.readFileSync(file, 'utf8');
  const scriptInfo = [];
  
  SCRIPT_PATTERNS.forEach(({ name, patterns }) => {
    let totalMatches = 0;
    const matches = [];
    
    patterns.forEach(pattern => {
      const escapedPattern = pattern.replace(/\//g, '\\/');
      const regex = new RegExp(`<script[^>]*src=["']${escapedPattern}[^"']*["'][^>]*>`, 'g');
      const found = content.match(regex);
      if (found) {
        totalMatches += found.length;
        matches.push(...found);
      }
    });
    
    scriptInfo.push({
      name,
      count: totalMatches,
      matches
    });
  });
  
  report.push({
    file,
    scripts: scriptInfo
  });
});

console.log('📄 RELATÓRIO COMPLETO:\n');

report.forEach(({ file, scripts }) => {
  console.log(`📄 ${file}`);
  scripts.forEach(({ name, count, matches }) => {
    if (count === 0) {
      console.log(`   ❌ ${name} - ausente`);
    } else if (count === 1) {
      console.log(`   ✅ ${name} - 1 ocorrência`);
      console.log(`      ${matches[0].substring(0, 100)}...`);
    } else {
      console.log(`   ⚠️  ${name} - ${count} ocorrências (DUPLICADO)`);
      matches.forEach((m, i) => {
        console.log(`      ${i+1}. ${m.substring(0, 100)}...`);
      });
    }
  });
  console.log('');
});

// Resumo
const totalDuplicates = report.reduce((sum, r) => 
  sum + r.scripts.filter(s => s.count > 1).length, 0
);
const totalMissing = report.reduce((sum, r) => 
  sum + r.scripts.filter(s => s.count === 0).length, 0
);

console.log('\n📊 RESUMO GERAL:');
console.log(`   Páginas verificadas: ${htmlFiles.length}`);
console.log(`   Scripts com duplicatas: ${totalDuplicates}`);
console.log(`   Scripts ausentes: ${totalMissing}`);
