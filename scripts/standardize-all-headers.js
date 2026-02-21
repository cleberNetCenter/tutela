#!/usr/bin/env node

const fs = require('fs');
const glob = require('glob');

console.log('🔧 PADRONIZANDO HEADERS EM TODAS AS PÁGINAS\n');

// Carregar o header canônico
const canonicalHeader = fs.readFileSync('/tmp/canonical-header.html', 'utf8');

console.log('✅ Header canônico carregado\n');

// Encontrar todos os arquivos HTML (exceto test, en, es)
const htmlFiles = glob.sync('public/**/*.html', {
  ignore: ['**/test*.html', '**/en/**', '**/es/**']
});

console.log(`📄 ${htmlFiles.length} arquivos HTML encontrados\n`);

const modified = [];
const skipped = [];
const errors = [];

htmlFiles.forEach(file => {
  try {
    let content = fs.readFileSync(file, 'utf8');
    
    // Encontrar o header atual
    const headerStartRegex = /<header[^>]*>/;
    const headerStart = content.search(headerStartRegex);
    
    if (headerStart === -1) {
      skipped.push({ file, reason: 'Header não encontrado' });
      return;
    }
    
    // Encontrar o final do header
    const headerEnd = content.indexOf('</header>', headerStart);
    
    if (headerEnd === -1) {
      errors.push({ file, reason: 'Fechamento do header não encontrado' });
      return;
    }
    
    // Substituir o header
    const before = content.substring(0, headerStart);
    const after = content.substring(headerEnd + '</header>'.length);
    const newContent = before + canonicalHeader + after;
    
    // Verificar se houve mudança
    if (newContent !== content) {
      fs.writeFileSync(file, newContent, 'utf8');
      modified.push(file);
      console.log(`✅ ${file}`);
    } else {
      skipped.push({ file, reason: 'Header já está padronizado' });
    }
    
  } catch (error) {
    errors.push({ file, reason: error.message });
    console.error(`❌ ${file}: ${error.message}`);
  }
});

console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
console.log('📊 RESUMO:\n');
console.log(`✅ Arquivos modificados: ${modified.length}`);
console.log(`⏭️  Arquivos não modificados: ${skipped.length}`);
console.log(`❌ Erros: ${errors.length}\n`);

if (modified.length > 0) {
  console.log('📝 ARQUIVOS MODIFICADOS:\n');
  modified.forEach(f => console.log(`   ✅ ${f}`));
  console.log('');
}

if (skipped.length > 0 && skipped.some(s => s.reason !== 'Header já está padronizado')) {
  console.log('⚠️  ARQUIVOS PULADOS:\n');
  skipped.filter(s => s.reason !== 'Header já está padronizado').forEach(s => {
    console.log(`   ⏭️  ${s.file}: ${s.reason}`);
  });
  console.log('');
}

if (errors.length > 0) {
  console.log('❌ ERROS:\n');
  errors.forEach(e => console.log(`   ❌ ${e.file}: ${e.reason}`));
  console.log('');
}

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

// Salvar relatório
const report = {
  timestamp: new Date().toISOString(),
  total: htmlFiles.length,
  modified: modified.length,
  skipped: skipped.length,
  errors: errors.length,
  modifiedFiles: modified,
  skippedFiles: skipped,
  errorFiles: errors
};

fs.writeFileSync('/tmp/header-standardization-report.json', JSON.stringify(report, null, 2), 'utf8');
console.log('✅ Relatório salvo em /tmp/header-standardization-report.json\n');
