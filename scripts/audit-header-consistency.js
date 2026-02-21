#!/usr/bin/env node

const fs = require('fs');
const glob = require('glob');
const crypto = require('crypto');

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('  ETAPA 3: HEADER CONSISTÊNCIA');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

// 1. Extrair header de seguranca.html como referência
console.log('1️⃣ Extraindo header de referência (public/seguranca.html)...\n');

const referenceFile = 'public/seguranca.html';
const referenceContent = fs.readFileSync(referenceFile, 'utf8');
const referenceHeaderMatch = referenceContent.match(/<header[^>]*id="header"[^>]*>[\s\S]*?<\/header>/);

if (!referenceHeaderMatch) {
  console.log('❌ ERRO: Não foi possível extrair o header de public/seguranca.html\n');
  process.exit(1);
}

const referenceHeader = referenceHeaderMatch[0];
const referenceHash = crypto.createHash('md5').update(referenceHeader).digest('hex');

console.log(`✅ Header de referência extraído (${referenceHeader.length} caracteres)`);
console.log(`   Hash MD5: ${referenceHash}\n`);

// 2. Verificar consistência em todas as páginas
console.log('2️⃣ Verificando consistência em todas as páginas...\n');

const htmlFiles = glob.sync('public/**/*.html', {
  ignore: ['**/node_modules/**', '**/test/**', '**/en/**', '**/es/**']
});

let consistentPages = [];
let inconsistentPages = [];
let missingHeaderPages = [];

htmlFiles.forEach(file => {
  const content = fs.readFileSync(file, 'utf8');
  const headerMatch = content.match(/<header[^>]*id="header"[^>]*>[\s\S]*?<\/header>/);
  
  if (!headerMatch) {
    missingHeaderPages.push(file);
    return;
  }
  
  const pageHeader = headerMatch[0];
  const pageHash = crypto.createHash('md5').update(pageHeader).digest('hex');
  
  if (pageHash === referenceHash) {
    consistentPages.push({ file, hash: pageHash });
  } else {
    inconsistentPages.push({ 
      file, 
      hash: pageHash,
      sizeDiff: pageHeader.length - referenceHeader.length
    });
  }
});

// 3. Validar elementos críticos do header
console.log('3️⃣ Validando elementos críticos...\n');

const criticalElements = {
  'id="header"': 0,
  'id="nav"': 0,
  'class="mobile-menu-btn"': 0,
  'class="nav-dropdown"': 0,
  'class="lang-dropdown"': 0
};

let elementValidation = [];

htmlFiles.forEach(file => {
  const content = fs.readFileSync(file, 'utf8');
  const headerMatch = content.match(/<header[^>]*id="header"[^>]*>[\s\S]*?<\/header>/);
  
  if (!headerMatch) return;
  
  const header = headerMatch[0];
  let issues = [];
  
  Object.keys(criticalElements).forEach(element => {
    const regex = new RegExp(element, 'g');
    const count = (header.match(regex) || []).length;
    
    if (element === 'id="header"' || element === 'id="nav"' || element === 'class="mobile-menu-btn"') {
      if (count !== 1) {
        issues.push(`${element} encontrado ${count} vezes (esperado: 1)`);
      }
    }
  });
  
  // Verificar spans do botão mobile
  const mobileButtonMatch = header.match(/<button[^>]*class="mobile-menu-btn"[^>]*>([\s\S]*?)<\/button>/);
  if (mobileButtonMatch) {
    const buttonContent = mobileButtonMatch[1];
    const spanCount = (buttonContent.match(/<span>/g) || []).length;
    if (spanCount !== 3) {
      issues.push(`Botão mobile tem ${spanCount} spans (esperado: 3)`);
    }
  }
  
  if (issues.length > 0) {
    elementValidation.push({ file, issues });
  }
});

// Gerar relatório
console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('  RESULTADOS DA AUDITORIA');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

console.log(`📊 Estatísticas:\n`);
console.log(`   Total de páginas HTML: ${htmlFiles.length}`);
console.log(`   Headers consistentes: ${consistentPages.length}`);
console.log(`   Headers inconsistentes: ${inconsistentPages.length}`);
console.log(`   Headers ausentes: ${missingHeaderPages.length}`);
console.log(`   Problemas de validação: ${elementValidation.length}\n`);

if (inconsistentPages.length === 0 && missingHeaderPages.length === 0 && elementValidation.length === 0) {
  console.log('✅ HEADER CONSISTÊNCIA: PASSOU EM TODOS OS TESTES\n');
  console.log('✅ Todos os headers são idênticos ao de seguranca.html');
  console.log('✅ Todos os elementos críticos estão presentes');
  console.log('✅ Botões mobile têm exatamente 3 spans');
  console.log('✅ IDs únicos (header, nav) em todas as páginas\n');
} else {
  if (inconsistentPages.length > 0) {
    console.log(`⚠️  HEADERS INCONSISTENTES: ${inconsistentPages.length}\n`);
    inconsistentPages.forEach(page => {
      console.log(`   ${page.file}`);
      console.log(`   Hash: ${page.hash}`);
      console.log(`   Diferença de tamanho: ${page.sizeDiff > 0 ? '+' : ''}${page.sizeDiff} caracteres\n`);
    });
  }
  
  if (missingHeaderPages.length > 0) {
    console.log(`❌ HEADERS AUSENTES: ${missingHeaderPages.length}\n`);
    missingHeaderPages.forEach(page => {
      console.log(`   ${page}\n`);
    });
  }
  
  if (elementValidation.length > 0) {
    console.log(`⚠️  PROBLEMAS DE VALIDAÇÃO: ${elementValidation.length}\n`);
    elementValidation.forEach(item => {
      console.log(`   ${item.file}`);
      item.issues.forEach(issue => {
        console.log(`   → ${issue}`);
      });
      console.log('');
    });
  }
}

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

const hasIssues = inconsistentPages.length > 0 || missingHeaderPages.length > 0 || elementValidation.length > 0;
process.exit(hasIssues ? 1 : 0);
