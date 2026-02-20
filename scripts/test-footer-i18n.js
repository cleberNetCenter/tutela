#!/usr/bin/env node

/**
 * TESTE DE TRADUÇÕES DO RODAPÉ
 * Verifica se todas as chaves data-i18n do rodapé existem nos arquivos JSON
 */

const fs = require('fs');
const path = require('path');

// Carregar JSONs
const pt = JSON.parse(fs.readFileSync('public/assets/lang/pt.json', 'utf8'));
const en = JSON.parse(fs.readFileSync('public/assets/lang/en.json', 'utf8'));
const es = JSON.parse(fs.readFileSync('public/assets/lang/es.json', 'utf8'));

// Chaves usadas no footer (extraídas do HTML)
const footerKeys = [
  'global.brand',
  'global.footerEmail',
  'global.footerInstagram',
  'navigation.howItWorks',
  'navigation.security',
  'navigation.preservation',
  'navigation.government',
  'navigation.companies',
  'navigation.individuals',
  'navigation.legal_base',
  'navigation.institucional',
  'navigation.legalBasis',
  'navigation.terms',
  'navigation.privacy',
  'global.footerRights'
];

console.log('🔍 TESTE DE TRADUÇÕES DO RODAPÉ\n');

// Função para buscar valor aninhado
function getNestedValue(obj, key) {
  return key.split('.').reduce((o, k) => o?.[k], obj);
}

// Teste para cada idioma
[
  { name: 'Português', code: 'pt', data: pt },
  { name: 'Inglês', code: 'en', data: en },
  { name: 'Espanhol', code: 'es', data: es }
].forEach(({ name, code, data }) => {
  console.log(`\n📋 ${name} (${code}):`);
  
  let missing = 0;
  footerKeys.forEach(key => {
    const value = getNestedValue(data, key);
    if (!value) {
      console.log(`   ❌ Faltando: ${key}`);
      missing++;
    } else {
      console.log(`   ✅ ${key}: "${value}"`);
    }
  });
  
  if (missing === 0) {
    console.log(`   ✅ TODAS AS CHAVES PRESENTES (${footerKeys.length}/${footerKeys.length})`);
  } else {
    console.log(`   ⚠️  FALTAM ${missing} CHAVES`);
  }
});

console.log('\n✅ TESTE CONCLUÍDO\n');
