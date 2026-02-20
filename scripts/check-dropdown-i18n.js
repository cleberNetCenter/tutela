#!/usr/bin/env node

/**
 * VERIFICA data-i18n NOS DROPDOWNS
 * Detecta links de dropdown sem tradução
 */

const fs = require('fs');
const path = require('path');
const glob = require('glob');

const ROOT = path.join(__dirname, '..');

const htmlFiles = glob.sync('public/**/*.html', { 
  cwd: ROOT,
  ignore: ['**/test*.html', '**/en/**', '**/es/**']
});

console.log('🔍 VERIFICANDO data-i18n NOS DROPDOWNS\n');

let issuesFound = 0;

htmlFiles.forEach(file => {
  const filePath = path.join(ROOT, file);
  const html = fs.readFileSync(filePath, 'utf8');
  
  // Extrai os dropdowns
  const dropdownRegex = /<div class="nav-dropdown">([\s\S]*?)<\/div>/g;
  let match;
  
  let hasIssues = false;
  const issues = [];
  
  while ((match = dropdownRegex.exec(html)) !== null) {
    const dropdownContent = match[1];
    
    // Extrai os links <a> dentro do dropdown
    const linkRegex = /<a[^>]*>(.*?)<\/a>/g;
    let linkMatch;
    
    while ((linkMatch = linkRegex.exec(dropdownContent)) !== null) {
      const linkTag = match[0];
      const linkText = linkMatch[1];
      
      // Verifica se o link principal do dropdown tem data-i18n
      if (linkTag.includes('class="nav-link"') && !linkTag.includes('data-i18n')) {
        issues.push(`❌ Link dropdown SEM data-i18n: "${linkText}"`);
        hasIssues = true;
      }
    }
    
    // Verifica links do <ul> dentro do dropdown
    const ulRegex = /<ul class="dropdown-menu">([\s\S]*?)<\/ul>/;
    const ulMatch = dropdownContent.match(ulRegex);
    
    if (ulMatch) {
      const ulContent = ulMatch[1];
      const itemRegex = /<li><a[^>]*>(.*?)<\/a><\/li>/g;
      let itemMatch;
      
      while ((itemMatch = itemRegex.exec(ulContent)) !== null) {
        const itemTag = itemMatch[0];
        const itemText = itemMatch[1];
        
        if (!itemTag.includes('data-i18n')) {
          issues.push(`⚠️  Item dropdown SEM data-i18n: "${itemText}"`);
          hasIssues = true;
        }
      }
    }
  }
  
  if (hasIssues) {
    console.log(`\n📄 ${file}:`);
    issues.forEach(issue => console.log(`   ${issue}`));
    issuesFound++;
  }
});

if (issuesFound === 0) {
  console.log('✅ TODOS OS DROPDOWNS TÊM data-i18n CORRETO\n');
} else {
  console.log(`\n⚠️  ENCONTRADOS PROBLEMAS EM ${issuesFound} ARQUIVO(S)\n`);
}
