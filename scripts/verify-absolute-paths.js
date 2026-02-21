#!/usr/bin/env node

const fs = require('fs');
const glob = require('glob');

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('  VERIFICAÇÃO: CAMINHOS ABSOLUTOS');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

const htmlFiles = glob.sync('public/**/*.html', {
  ignore: ['**/node_modules/**', '**/test/**', '**/en/**', '**/es/**']
}).filter(file => !file.includes('test'));

let allCorrect = true;
let issues = [];

htmlFiles.forEach(file => {
  const content = fs.readFileSync(file, 'utf8');
  
  // Verificar caminhos relativos (ERRO)
  const relativeMatches = content.match(/src="assets\/js\//g) || [];
  
  // Verificar caminhos absolutos (OK)
  const absoluteMatches = content.match(/src="\/assets\/js\//g) || [];
  
  if (relativeMatches.length > 0) {
    allCorrect = false;
    issues.push({
      file,
      type: 'relative',
      count: relativeMatches.length
    });
  }
  
  console.log(`${relativeMatches.length === 0 ? '✅' : '❌'} ${file}`);
  console.log(`   Caminhos relativos: ${relativeMatches.length}`);
  console.log(`   Caminhos absolutos: ${absoluteMatches.length}\n`);
});

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('  RESULTADO DA VERIFICAÇÃO');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

if (allCorrect) {
  console.log('✅ TODOS OS CAMINHOS ESTÃO CORRETOS (ABSOLUTOS)\n');
  console.log(`   Total de páginas verificadas: ${htmlFiles.length}`);
  console.log(`   Páginas com caminhos absolutos: ${htmlFiles.length}`);
  console.log(`   Páginas com caminhos relativos: 0\n`);
  console.log('✅ Páginas em /legal/ agora carregarão scripts corretamente');
  console.log('✅ Nenhum erro 404 esperado\n');
} else {
  console.log(`❌ PROBLEMAS ENCONTRADOS: ${issues.length}\n`);
  issues.forEach(issue => {
    console.log(`   ${issue.file}`);
    console.log(`   → ${issue.count} caminhos relativos encontrados\n`);
  });
}

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

process.exit(allCorrect ? 0 : 1);
