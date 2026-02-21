#!/usr/bin/env node

const fs = require('fs');
const glob = require('glob');

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('  ETAPA 4: SCRIPT ORDER VALIDATION');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

const expectedOrder = [
  'navigation.js',
  'i18n.js',
  'dropdown-menu.js',
  'mobile-menu.js'
];

console.log('Ordem esperada dos scripts:\n');
expectedOrder.forEach((script, index) => {
  console.log(`   ${index + 1}. ${script}`);
});
console.log('');

const htmlFiles = glob.sync('public/**/*.html', {
  ignore: ['**/node_modules/**', '**/test/**', '**/en/**', '**/es/**']
}).filter(file => !file.includes('test'));

let correctPages = [];
let incorrectPages = [];
let versionInconsistencies = [];

htmlFiles.forEach(file => {
  const content = fs.readFileSync(file, 'utf8');
  
  // Extrair todos os scripts do body
  const bodyMatch = content.match(/<body[\s\S]*?<\/body>/);
  if (!bodyMatch) return;
  
  const body = bodyMatch[0];
  
  // Encontrar todos os scripts com os nomes esperados
  let scripts = [];
  expectedOrder.forEach(scriptName => {
    const regex = new RegExp(`<script[^>]*src="[^"]*${scriptName}(?:\\?v=([^"]*))?"[^>]*>`, 'g');
    let match;
    while ((match = regex.exec(body)) !== null) {
      const index = body.indexOf(match[0]);
      scripts.push({
        name: scriptName,
        position: index,
        version: match[1] || 'no-version',
        fullMatch: match[0]
      });
    }
  });
  
  // Ordenar por posição no arquivo
  scripts.sort((a, b) => a.position - b.position);
  
  // Verificar ordem
  const actualOrder = scripts.map(s => s.name);
  const isCorrectOrder = JSON.stringify(actualOrder) === JSON.stringify(expectedOrder);
  
  // Verificar consistência de versões
  const versions = scripts.map(s => s.version);
  const uniqueVersions = [...new Set(versions)];
  const hasConsistentVersions = uniqueVersions.length === 1 && uniqueVersions[0] !== 'no-version';
  
  if (isCorrectOrder && hasConsistentVersions) {
    correctPages.push({ file, version: uniqueVersions[0] });
  } else {
    incorrectPages.push({
      file,
      actualOrder,
      expectedOrder,
      scripts,
      hasCorrectOrder: isCorrectOrder,
      hasConsistentVersions,
      versions: uniqueVersions
    });
  }
});

// Gerar relatório
console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('  RESULTADOS DA AUDITORIA');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

console.log(`📊 Estatísticas:\n`);
console.log(`   Total de páginas: ${htmlFiles.length}`);
console.log(`   Ordem correta: ${correctPages.length}`);
console.log(`   Ordem incorreta: ${incorrectPages.length}\n`);

if (incorrectPages.length === 0) {
  console.log('✅ SCRIPT ORDER: PASSOU EM TODOS OS TESTES\n');
  console.log('✅ Todos os scripts na ordem correta');
  console.log('✅ Todos os scripts com version stamp consistente\n');
  
  if (correctPages.length > 0) {
    const version = correctPages[0].version;
    console.log(`✅ Version stamp: ?v=${version}\n`);
  }
} else {
  console.log(`⚠️  PÁGINAS COM PROBLEMAS: ${incorrectPages.length}\n`);
  
  incorrectPages.forEach(page => {
    console.log(`   📄 ${page.file}\n`);
    
    if (!page.hasCorrectOrder) {
      console.log(`   ❌ Ordem incorreta:`);
      console.log(`      Esperado: ${page.expectedOrder.join(' → ')}`);
      console.log(`      Atual:    ${page.actualOrder.join(' → ')}\n`);
    }
    
    if (!page.hasConsistentVersions) {
      console.log(`   ⚠️  Versões inconsistentes:`);
      page.scripts.forEach(script => {
        console.log(`      ${script.name}: v=${script.version}`);
      });
      console.log('');
    }
    
    console.log('   Scripts encontrados:');
    page.scripts.forEach((script, index) => {
      console.log(`      ${index + 1}. ${script.name} (v=${script.version})`);
    });
    console.log('\n');
  });
}

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

process.exit(incorrectPages.length > 0 ? 1 : 0);
