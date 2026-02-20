#!/usr/bin/env node

/**
 * VERIFICA SE TODAS AS TRADUÇÕES DOS DROPDOWNS EXISTEM
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');

// Carregar JSONs
const pt = JSON.parse(fs.readFileSync(path.join(ROOT, 'public/assets/lang/pt.json'), 'utf8'));
const en = JSON.parse(fs.readFileSync(path.join(ROOT, 'public/assets/lang/en.json'), 'utf8'));
const es = JSON.parse(fs.readFileSync(path.join(ROOT, 'public/assets/lang/es.json'), 'utf8'));

// Chaves dos dropdowns
const dropdownKeys = [
  'navigation.government',
  'navigation.companies',
  'navigation.individuals',
  'navigation.preservation',
  'navigation.legalBasis',
  'navigation.terms',
  'navigation.privacy',
  'navigation.institucional'
];

console.log('🔍 VERIFICANDO TRADUÇÕES DOS DROPDOWNS\n');

function getNestedValue(obj, key) {
  return key.split('.').reduce((o, k) => o?.[k], obj);
}

[
  { name: 'Português', code: 'pt', data: pt },
  { name: 'Inglês', code: 'en', data: en },
  { name: 'Espanhol', code: 'es', data: es }
].forEach(({ name, code, data }) => {
  console.log(`\n📋 ${name} (${code}):`);
  
  let missing = 0;
  dropdownKeys.forEach(key => {
    const value = getNestedValue(data, key);
    if (!value) {
      console.log(`   ❌ Faltando: ${key}`);
      missing++;
    } else {
      console.log(`   ✅ ${key}: "${value}"`);
    }
  });
  
  if (missing === 0) {
    console.log(`   ✅ TODAS AS CHAVES PRESENTES (${dropdownKeys.length}/${dropdownKeys.length})`);
  } else {
    console.log(`   ⚠️  FALTAM ${missing} CHAVES`);
  }
});

console.log('\n✅ VERIFICAÇÃO CONCLUÍDA\n');
