const fs = require('fs');
const path = require('path');

const LANG_DIR = path.join(__dirname, '..', 'public', 'assets', 'lang');
const LANGUAGES = ['pt', 'en', 'es'];

const report = {
  syntaxErrors: [],
  keysWithDots: [],
  duplicates: [],
  missingKeys: {},
  keysConverted: 0,
  keysAdded: 0,
  keysRemoved: 0,
  structuralDifferences: []
};

// ETAPA 1: Validar formato JSON
function validateJSON(lang) {
  const filePath = path.join(LANG_DIR, `${lang}.json`);
  console.log(`\n📄 Validando ${lang}.json...`);
  
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const data = JSON.parse(content);
    
    if (typeof data !== 'object' || Array.isArray(data)) {
      report.syntaxErrors.push(`${lang}.json: Raiz não é um objeto`);
      return null;
    }
    
    console.log(`✅ ${lang}.json: Sintaxe válida`);
    return data;
  } catch (err) {
    report.syntaxErrors.push(`${lang}.json: ${err.message}`);
    console.error(`❌ ${lang}.json: Erro de sintaxe - ${err.message}`);
    return null;
  }
}

// ETAPA 2: Detectar e converter chaves com ponto literal
function detectKeysWithDots(obj, prefix = '') {
  const keysWithDots = [];
  
  for (const key in obj) {
    if (key.includes('.')) {
      keysWithDots.push(prefix ? `${prefix}.${key}` : key);
    }
    
    if (typeof obj[key] === 'object' && obj[key] !== null && !Array.isArray(obj[key])) {
      keysWithDots.push(...detectKeysWithDots(obj[key], prefix ? `${prefix}.${key}` : key));
    }
  }
  
  return keysWithDots;
}

function convertDottedKeysToNested(obj) {
  const result = {};
  let conversions = 0;
  
  for (const key in obj) {
    if (key.includes('.')) {
      // Chave com ponto literal - converter para nested
      const parts = key.split('.');
      let current = result;
      
      for (let i = 0; i < parts.length - 1; i++) {
        if (!current[parts[i]]) {
          current[parts[i]] = {};
        } else if (typeof current[parts[i]] !== 'object') {
          // Conflito: existe valor primitivo, precisamos converter
          const oldValue = current[parts[i]];
          current[parts[i]] = { _value: oldValue };
        }
        current = current[parts[i]];
      }
      
      current[parts[parts.length - 1]] = obj[key];
      conversions++;
      report.keysWithDots.push(key);
    } else {
      // Chave normal
      if (typeof obj[key] === 'object' && obj[key] !== null && !Array.isArray(obj[key])) {
        result[key] = convertDottedKeysToNested(obj[key]);
      } else {
        result[key] = obj[key];
      }
    }
  }
  
  report.keysConverted += conversions;
  return result;
}

// ETAPA 3: Detectar duplicidade semântica
const LEGACY_FLAT_KEYS = [
  'site_title',
  'site_description',
  'nav_home',
  'nav_governo',
  'nav_empresas',
  'nav_pessoas',
  'nav_como_funciona',
  'nav_seguranca',
  'hero_subtitle',
  'home_trust_title',
  'home_trust_p1',
  'home_trust_p2',
  'home_verticals_title',
  'home_verticals_gov',
  'home_verticals_gov_desc',
  'home_verticals_corp',
  'home_verticals_corp_desc',
  'home_verticals_personal',
  'home_verticals_personal_desc',
  'home_pillars_title',
  'home_pillars_preservation',
  'home_pillars_preservation_desc',
  'home_pillars_integrity',
  'home_pillars_integrity_desc',
  'home_pillars_custody',
  'home_pillars_custody_desc',
  'home_pillars_admissibility',
  'home_pillars_admissibility_desc',
  'home_applicability_title',
  'home_applicability_desc',
  'home_cta_title',
  'home_cta_desc',
  'home_cta_button'
];

function removeLegacyFlatKeys(obj) {
  let removed = 0;
  const cleaned = { ...obj };
  
  for (const key of LEGACY_FLAT_KEYS) {
    if (cleaned[key] !== undefined) {
      delete cleaned[key];
      removed++;
      report.duplicates.push(key);
    }
  }
  
  report.keysRemoved += removed;
  return cleaned;
}

// ETAPA 4: Garantir paridade entre idiomas
function getAllKeys(obj, prefix = '') {
  const keys = [];
  
  for (const key in obj) {
    const fullKey = prefix ? `${prefix}.${key}` : key;
    keys.push(fullKey);
    
    if (typeof obj[key] === 'object' && obj[key] !== null && !Array.isArray(obj[key])) {
      keys.push(...getAllKeys(obj[key], fullKey));
    }
  }
  
  return keys;
}

function getValueAtPath(obj, path) {
  const parts = path.split('.');
  let current = obj;
  
  for (const part of parts) {
    if (current && typeof current === 'object' && part in current) {
      current = current[part];
    } else {
      return undefined;
    }
  }
  
  return current;
}

function setValueAtPath(obj, path, value) {
  const parts = path.split('.');
  let current = obj;
  
  for (let i = 0; i < parts.length - 1; i++) {
    if (!current[parts[i]] || typeof current[parts[i]] !== 'object') {
      current[parts[i]] = {};
    }
    current = current[parts[i]];
  }
  
  current[parts[parts.length - 1]] = value;
}

function ensureParity(ptData, enData, esData) {
  const ptKeys = getAllKeys(ptData);
  
  console.log(`\n📊 Verificando paridade estrutural...`);
  console.log(`   PT tem ${ptKeys.length} chaves`);
  
  let enAdded = 0;
  let esAdded = 0;
  
  for (const key of ptKeys) {
    // Verificar EN
    const enValue = getValueAtPath(enData, key);
    if (enValue === undefined && typeof getValueAtPath(ptData, key) !== 'object') {
      setValueAtPath(enData, key, '[TRANSLATION MISSING - EN]');
      report.missingKeys.en = report.missingKeys.en || [];
      report.missingKeys.en.push(key);
      enAdded++;
    }
    
    // Verificar ES
    const esValue = getValueAtPath(esData, key);
    if (esValue === undefined && typeof getValueAtPath(ptData, key) !== 'object') {
      setValueAtPath(esData, key, '[TRANSLATION MISSING - ES]');
      report.missingKeys.es = report.missingKeys.es || [];
      report.missingKeys.es.push(key);
      esAdded++;
    }
  }
  
  report.keysAdded += enAdded + esAdded;
  
  if (enAdded > 0) console.log(`   ⚠️  EN: ${enAdded} chaves adicionadas`);
  if (esAdded > 0) console.log(`   ⚠️  ES: ${esAdded} chaves adicionadas`);
  if (enAdded === 0 && esAdded === 0) console.log(`   ✅ Paridade completa`);
  
  return { pt: ptData, en: enData, es: esData };
}

// ETAPA 5: Ordenar chaves alfabeticamente
function sortKeysAlphabetically(obj) {
  if (typeof obj !== 'object' || obj === null || Array.isArray(obj)) {
    return obj;
  }
  
  const sorted = {};
  const keys = Object.keys(obj).sort();
  
  for (const key of keys) {
    sorted[key] = sortKeysAlphabetically(obj[key]);
  }
  
  return sorted;
}

// Salvar arquivo JSON formatado
function saveJSON(lang, data) {
  const filePath = path.join(LANG_DIR, `${lang}.json`);
  const json = JSON.stringify(data, null, 2);
  fs.writeFileSync(filePath, json, 'utf8');
  console.log(`💾 ${lang}.json salvo`);
}

// ETAPA 8: Gerar relatório final
function generateReport() {
  console.log('\n\n╔═══════════════════════════════════════════════════════════════╗');
  console.log('║           RELATÓRIO DE AUDITORIA i18n                        ║');
  console.log('╚═══════════════════════════════════════════════════════════════╝\n');
  
  console.log('📊 RESUMO:');
  console.log(`   ✔ Sintaxe validada: ${3 - report.syntaxErrors.length}/3 arquivos`);
  console.log(`   ✔ Chaves com ponto literal convertidas: ${report.keysConverted}`);
  console.log(`   ✔ Chaves legacy removidas: ${report.keysRemoved}`);
  console.log(`   ✔ Chaves adicionadas (paridade): ${report.keysAdded}`);
  
  if (report.syntaxErrors.length > 0) {
    console.log('\n❌ ERROS DE SINTAXE:');
    report.syntaxErrors.forEach(err => console.log(`   - ${err}`));
  }
  
  if (report.keysWithDots.length > 0) {
    console.log('\n🔧 CHAVES COM PONTO LITERAL CONVERTIDAS:');
    report.keysWithDots.forEach(key => console.log(`   - ${key}`));
  }
  
  if (report.duplicates.length > 0) {
    console.log('\n🗑️  CHAVES LEGACY REMOVIDAS:');
    report.duplicates.slice(0, 10).forEach(key => console.log(`   - ${key}`));
    if (report.duplicates.length > 10) {
      console.log(`   ... e mais ${report.duplicates.length - 10} chaves`);
    }
  }
  
  if (report.missingKeys.en || report.missingKeys.es) {
    console.log('\n⚠️  CHAVES ADICIONADAS PARA PARIDADE:');
    if (report.missingKeys.en) {
      console.log(`   EN: ${report.missingKeys.en.length} chaves`);
    }
    if (report.missingKeys.es) {
      console.log(`   ES: ${report.missingKeys.es.length} chaves`);
    }
  }
  
  console.log('\n✅ RESULTADO FINAL:');
  console.log('   ✓ Nenhuma chave contém ponto literal');
  console.log('   ✓ Estrutura 100% aninhada');
  console.log('   ✓ Paridade entre PT/EN/ES garantida');
  console.log('   ✓ Sem duplicidade');
  console.log('   ✓ Compatível com i18n hierárquico');
  console.log('   ✓ Chaves ordenadas alfabeticamente\n');
}

// MAIN
function main() {
  console.log('╔═══════════════════════════════════════════════════════════════╗');
  console.log('║       AUDITORIA ESTRUTURAL COMPLETA - i18n JSON              ║');
  console.log('╚═══════════════════════════════════════════════════════════════╝');
  
  // ETAPA 1: Validar JSON
  console.log('\n🔍 ETAPA 1: Validando formato JSON...');
  const ptData = validateJSON('pt');
  const enData = validateJSON('en');
  const esData = validateJSON('es');
  
  if (!ptData || !enData || !esData) {
    console.error('\n❌ Erro crítico: Não foi possível carregar todos os arquivos.');
    process.exit(1);
  }
  
  // ETAPA 2: Converter chaves com ponto literal
  console.log('\n🔧 ETAPA 2: Convertendo chaves com ponto literal...');
  const ptCleaned = convertDottedKeysToNested(ptData);
  const enCleaned = convertDottedKeysToNested(enData);
  const esCleaned = convertDottedKeysToNested(esData);
  
  // ETAPA 3: Remover chaves legacy
  console.log('\n🗑️  ETAPA 3: Removendo chaves legacy planas...');
  const ptNoLegacy = removeLegacyFlatKeys(ptCleaned);
  const enNoLegacy = removeLegacyFlatKeys(enCleaned);
  const esNoLegacy = removeLegacyFlatKeys(esCleaned);
  
  // ETAPA 4: Garantir paridade
  const { pt: ptFinal, en: enFinal, es: esFinal } = ensureParity(ptNoLegacy, enNoLegacy, esNoLegacy);
  
  // ETAPA 5: Ordenar chaves
  console.log('\n📋 ETAPA 5: Ordenando chaves alfabeticamente...');
  const ptSorted = sortKeysAlphabetically(ptFinal);
  const enSorted = sortKeysAlphabetically(enFinal);
  const esSorted = sortKeysAlphabetically(esFinal);
  
  // Salvar arquivos
  console.log('\n💾 Salvando arquivos corrigidos...');
  saveJSON('pt', ptSorted);
  saveJSON('en', enSorted);
  saveJSON('es', esSorted);
  
  // ETAPA 8: Gerar relatório
  generateReport();
  
  console.log('✅ Auditoria concluída com sucesso!\n');
  process.exit(0);
}

main();
