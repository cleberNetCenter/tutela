#!/usr/bin/env node

const fs = require('fs');
const glob = require('glob');

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('  CORRIGINDO ORDEM DOS SCRIPTS');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

const targetVersion = '202602210200';
const expectedOrder = [
  {name: 'navigation.js', version: targetVersion},
  {name: 'i18n.js', version: targetVersion},
  {name: 'dropdown-menu.js', version: targetVersion},
  {name: 'mobile-menu.js', version: targetVersion}
];

const htmlFiles = glob.sync('public/**/*.html', {
  ignore: ['**/node_modules/**', '**/test/**', '**/en/**', '**/es/**']
}).filter(file => !file.includes('test'));

let modified = [];

htmlFiles.forEach(file => {
  let content = fs.readFileSync(file, 'utf8');
  let originalContent = content;
  
  // Remover todos os scripts existentes
  expectedOrder.forEach(script => {
    const regex = new RegExp(`\\s*<script[^>]*src="[^"]*${script.name}[^"]*"[^>]*></script>\\s*`, 'g');
    content = content.replace(regex, '\n');
  });
  
  // Adicionar scripts na ordem correta antes de </body>
  const scriptsHTML = expectedOrder.map(script => 
    `    <script src="assets/js/${script.name}?v=${script.version}"></script>`
  ).join('\n') + '\n';
  
  content = content.replace('</body>', scriptsHTML + '  </body>');
  
  if (content !== originalContent) {
    fs.writeFileSync(file, content, 'utf8');
    modified.push(file);
    console.log(`✅ ${file}`);
  }
});

console.log(`\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
console.log(`Páginas modificadas: ${modified.length}/${htmlFiles.length}\n`);
console.log(`✅ Ordem correta aplicada:`);
expectedOrder.forEach((script, index) => {
  console.log(`   ${index + 1}. ${script.name} (v=${script.version})`);
});
console.log('');
