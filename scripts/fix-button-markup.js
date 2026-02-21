#!/usr/bin/env node

const fs = require('fs');
const glob = require('glob');

console.log('🔧 CORRIGINDO MARKUP DOS BOTÕES MOBILE\n');

const htmlFiles = glob.sync('public/**/*.html', {
  ignore: ['**/test*.html', '**/en/**', '**/es/**']
});

console.log(`📄 ${htmlFiles.length} arquivos HTML encontrados\n`);

let modified = 0;

htmlFiles.forEach(file => {
  let content = fs.readFileSync(file, 'utf8');
  const before = content;
  
  // Corrigir o markup duplicado
  // De: <button class="mobile-menu-btn" <button class="mobile-menu-btn">
  // Para: <button class="mobile-menu-btn">
  content = content.replace(
    /<button class="mobile-menu-btn" <button class="mobile-menu-btn">/g,
    '<button class="mobile-menu-btn">'
  );
  
  if (content !== before) {
    fs.writeFileSync(file, content, 'utf8');
    modified++;
    console.log(`✅ ${file} - markup corrigido`);
  }
});

console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
console.log(`📊 RESUMO:\n`);
console.log(`✅ Arquivos corrigidos: ${modified}`);
console.log(`⏭️  Arquivos sem alteração: ${htmlFiles.length - modified}\n`);

if (modified > 0) {
  console.log('✅ MARKUP DOS BOTÕES CORRIGIDO\n');
  console.log('Resultado:');
  console.log('  Antes:  <button class="mobile-menu-btn" <button class="mobile-menu-btn">');
  console.log('  Depois: <button class="mobile-menu-btn">\n');
}

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
