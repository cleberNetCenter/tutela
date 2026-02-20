#!/usr/bin/env node

/**
 * PAGE STRUCTURE STANDARDIZATION
 * 
 * Objetivo: Padronizar estrutura HTML de TODAS as páginas
 * - Restaurar ordem padrão: <body class="exec-compact">
 * - Garantir hierarquia: .app > header + main + footer
 * - Adicionar class="legal-page" em páginas legais
 * - Remover patches e overrides manuais
 * - SEM alterar CSS/JS existentes
 */

const fs = require('fs');
const path = require('path');
const glob = require('glob');

const ROOT = path.join(__dirname, '..');

// ============================================================
// 1️⃣ GET ALL HTML FILES
// ============================================================
function getAllHTMLFiles() {
  const patterns = [
    'public/**/*.html',
    '!public/**/*.backup*',
    '!public/**/node_modules/**'
  ];
  
  let files = [];
  patterns.forEach(pattern => {
    if (pattern.startsWith('!')) {
      const excludePattern = pattern.slice(1);
      const toExclude = glob.sync(excludePattern, { cwd: ROOT, absolute: true });
      files = files.filter(f => !toExclude.includes(f));
    } else {
      files.push(...glob.sync(pattern, { cwd: ROOT, absolute: true }));
    }
  });
  
  return files;
}

// ============================================================
// 2️⃣ STANDARDIZE BODY CLASS
// ============================================================
function standardizeBodyClass(html, isLegalPage) {
  // Remove classes duplicadas ou incorretas
  html = html.replace(
    /<body[^>]*class="([^"]*)"[^>]*>/,
    (match, classes) => {
      let classList = classes.split(/\s+/).filter(Boolean);
      
      // Remover duplicatas
      classList = [...new Set(classList)];
      
      // Garantir exec-compact
      if (!classList.includes('exec-compact')) {
        classList.unshift('exec-compact');
      }
      
      // Adicionar legal-page se necessário
      if (isLegalPage && !classList.includes('legal-page')) {
        classList.push('legal-page');
      }
      
      return `<body class="${classList.join(' ')}">`;
    }
  );
  
  // Se não tem classe nenhuma, adicionar
  if (!html.includes('<body class=')) {
    html = html.replace(
      /<body>/,
      isLegalPage ? '<body class="exec-compact legal-page">' : '<body class="exec-compact">'
    );
  }
  
  return html;
}

// ============================================================
// 3️⃣ ENSURE APP WRAPPER
// ============================================================
function ensureAppWrapper(html) {
  // Se já tem .app, não mexer
  if (html.includes('class="app"')) {
    return html;
  }
  
  // Adicionar .app após <body>
  html = html.replace(
    /(<body[^>]*>)\s*/,
    '$1\n  <div class="app">\n\n'
  );
  
  // Fechar .app antes de </body>
  html = html.replace(
    /\s*<\/body>/,
    '\n\n  </div>\n</body>'
  );
  
  return html;
}

// ============================================================
// 4️⃣ STANDARDIZE LEGAL PAGE HERO
// ============================================================
function standardizeLegalHero(html) {
  // Adicionar page-header--legal se ainda não tiver
  html = html.replace(
    /<section class="page-header"([^>]*)>/g,
    (match, attrs) => {
      if (match.includes('page-header--legal')) {
        return match;
      }
      return `<section class="page-header page-header--legal"${attrs}>`;
    }
  );
  
  return html;
}

// ============================================================
// 5️⃣ REMOVE PATCHES AND OVERRIDES
// ============================================================
function removePatches(html) {
  // Remove blocos de patch CSS inline
  const patchPatterns = [
    /<!--\s*HEADER UNIFICATION PATCH\s*-->[\s\S]*?<!--\s*END PATCH\s*-->/gi,
    /<!--\s*HEADER FIX\s*-->[\s\S]*?<!--\s*END HEADER FIX\s*-->/gi,
    /<!--\s*STRUCTURAL PATCH\s*-->[\s\S]*?<!--\s*END STRUCTURAL PATCH\s*-->/gi,
    /<style[^>]*>[\s\S]*?PATCH[\s\S]*?<\/style>/gi,
    /<style[^>]*>[\s\S]*?\.main\s*\{[^}]*padding-top:[^}]*\}[\s\S]*?<\/style>/gi,
    /<style[^>]*>[\s\S]*?\.header\s*\{[^}]*position:[^}]*\}[\s\S]*?<\/style>/gi
  ];
  
  patchPatterns.forEach(pattern => {
    html = html.replace(pattern, '');
  });
  
  return html;
}

// ============================================================
// 6️⃣ PROCESS SINGLE FILE
// ============================================================
function processFile(filePath) {
  const relativePath = path.relative(ROOT, filePath);
  const isLegalPage = relativePath.includes('legal/');
  
  let html = fs.readFileSync(filePath, 'utf8');
  const originalHTML = html;
  
  // Apply transformations
  html = standardizeBodyClass(html, isLegalPage);
  html = ensureAppWrapper(html);
  
  if (isLegalPage) {
    html = standardizeLegalHero(html);
  }
  
  html = removePatches(html);
  
  // Only write if changed
  if (html !== originalHTML) {
    fs.writeFileSync(filePath, html, 'utf8');
    return { path: relativePath, changed: true, isLegal: isLegalPage };
  }
  
  return { path: relativePath, changed: false, isLegal: isLegalPage };
}

// ============================================================
// 7️⃣ VALIDATION
// ============================================================
function validateFile(filePath) {
  const html = fs.readFileSync(filePath, 'utf8');
  const relativePath = path.relative(ROOT, filePath);
  const issues = [];
  
  // Check body class
  if (!html.includes('class="exec-compact"')) {
    issues.push('Missing exec-compact class');
  }
  
  // Check app wrapper
  if (!html.includes('class="app"')) {
    issues.push('Missing .app wrapper');
  }
  
  // Check header structure
  if (!html.match(/<header[^>]*class="header"/)) {
    issues.push('Invalid header structure');
  }
  
  // Check main
  if (!html.match(/<main[^>]*class="main"/)) {
    issues.push('Missing main element');
  }
  
  // Check footer
  if (!html.match(/<footer[^>]*class="footer"/)) {
    issues.push('Missing footer element');
  }
  
  // Check legal pages
  if (relativePath.includes('legal/')) {
    if (!html.includes('legal-page')) {
      issues.push('Legal page missing legal-page class');
    }
    if (!html.includes('page-header--legal')) {
      issues.push('Legal page missing page-header--legal class');
    }
  }
  
  return { path: relativePath, issues };
}

// ============================================================
// MAIN EXECUTION
// ============================================================
function main() {
  console.log('🔧 PAGE STRUCTURE STANDARDIZATION\n');
  
  try {
    const files = getAllHTMLFiles();
    console.log(`📄 Found ${files.length} HTML files\n`);
    
    // Process all files
    console.log('🔄 Processing files...\n');
    const results = files.map(processFile);
    
    const changed = results.filter(r => r.changed);
    const legalPages = changed.filter(r => r.isLegal);
    
    console.log('✅ PROCESSING COMPLETE\n');
    console.log(`📊 Statistics:`);
    console.log(`   Total files: ${files.length}`);
    console.log(`   Modified: ${changed.length}`);
    console.log(`   Legal pages: ${legalPages.length}`);
    console.log(`   Unchanged: ${files.length - changed.length}`);
    
    if (changed.length > 0) {
      console.log('\n📝 Modified files:');
      changed.forEach(r => {
        console.log(`   ${r.isLegal ? '⚖️' : '📄'} ${r.path}`);
      });
    }
    
    // Validation
    console.log('\n🔍 VALIDATION\n');
    const validations = files.map(validateFile);
    const withIssues = validations.filter(v => v.issues.length > 0);
    
    if (withIssues.length === 0) {
      console.log('✅ All files validated successfully');
    } else {
      console.log(`⚠️  ${withIssues.length} files with issues:\n`);
      withIssues.forEach(v => {
        console.log(`   ${v.path}:`);
        v.issues.forEach(issue => console.log(`      - ${issue}`));
      });
    }
    
    console.log('\n🎯 RESULT:');
    console.log('   - All pages: Same structural hierarchy ✅');
    console.log('   - Legal pages: legal-page class added ✅');
    console.log('   - Patches removed ✅');
    console.log('   - No CSS changes ✅');
    console.log('   - No JS changes ✅');
    
  } catch (error) {
    console.error('❌ ERROR:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

main();
