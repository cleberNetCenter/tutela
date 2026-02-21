#!/usr/bin/env node

const fs = require('fs');
const glob = require('glob');

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('  ETAPA 1: AUDITORIA DE DEBUG');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

const patterns = {
  'alert(': [],
  'debugger': [],
  'console.log(': [],
  'console.warn(': [],
  'console.error(': []
};

// Logs estruturais permitidos
const allowedLogs = [
  '[i18n]',
  '[dropdown]',
  '[navigateTo]'
];

const jsFiles = glob.sync('public/**/*.js', {
  ignore: ['**/node_modules/**', '**/test/**', '**/en/**', '**/es/**']
});

jsFiles.forEach(file => {
  const content = fs.readFileSync(file, 'utf8');
  const lines = content.split('\n');
  
  lines.forEach((line, index) => {
    Object.keys(patterns).forEach(pattern => {
      if (line.includes(pattern)) {
        // Verificar se é log estrutural permitido
        const isAllowed = allowedLogs.some(allowed => line.includes(allowed));
        
        if (!isAllowed && pattern !== 'alert(' && pattern !== 'debugger') {
          // console.log/warn/error sem tag estrutural
          patterns[pattern].push({
            file,
            line: index + 1,
            content: line.trim()
          });
        } else if (pattern === 'alert(' || pattern === 'debugger') {
          // alert e debugger NUNCA são permitidos
          patterns[pattern].push({
            file,
            line: index + 1,
            content: line.trim()
          });
        }
      }
    });
  });
});

let totalIssues = 0;
let criticalIssues = 0;

Object.keys(patterns).forEach(pattern => {
  const issues = patterns[pattern];
  if (issues.length > 0) {
    const isCritical = pattern === 'alert(' || pattern === 'debugger';
    if (isCritical) criticalIssues += issues.length;
    totalIssues += issues.length;
    
    console.log(`\n${isCritical ? '❌ CRÍTICO' : '⚠️  WARNING'}: Encontrado "${pattern}" (${issues.length} ocorrências)\n`);
    issues.forEach(issue => {
      console.log(`   ${issue.file}:${issue.line}`);
      console.log(`   → ${issue.content}\n`);
    });
  }
});

if (totalIssues === 0) {
  console.log('✅ Nenhum código de debug temporário encontrado\n');
  console.log('✅ Todos os logs são estruturais e documentados\n');
} else {
  console.log(`\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
  console.log(`Total de problemas: ${totalIssues}`);
  console.log(`Críticos (alert/debugger): ${criticalIssues}`);
  console.log(`Warnings (console sem tag): ${totalIssues - criticalIssues}`);
  console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`);
}

process.exit(totalIssues > 0 ? 1 : 0);
