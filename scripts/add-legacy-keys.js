const fs = require('fs');
const path = require('path');

const LANG_DIR = path.join(__dirname, '..', 'public', 'assets', 'lang');

// Mapa de chaves legadas para novas chaves nested
const LEGACY_MAP = {
  // Site meta
  'site_title': 'Tutela Digital® - Custódia Jurídica de Ativos Digitais',
  'site_description': 'Infraestrutura de custódia jurídica e governança de ativos digitais com validade legal, inviolabilidade técnica e cadeia de custódia auditável.',
  
  // Navigation legacy
  'nav_home': 'Início',
  'nav_governo': 'Governo',
  'nav_empresas': 'Empresas',
  'nav_pessoas': 'Pessoas Físicas',
  'nav_como_funciona': 'Como Funciona',
  'nav_seguranca': 'Segurança',
  
  // Home page legacy
  'hero_subtitle': 'Infraestrutura jurídica de custódia digital com integridade técnica verificável e validade probatória estruturada.',
  'home_trust_title': 'Confiança Institucional',
  'home_trust_p1': 'A Tutela Digital® oferece infraestrutura de preservação probatória digital estruturada para organizações públicas, empresas e indivíduos que necessitam de documentação técnica de ativos digitais com integridade verificável.',
  'home_trust_p2': 'Operada pela NetCenter, empresa com 30 anos de experiência em infraestrutura tecnológica, a solução integra conformidade legal, segurança técnica e governança corporativa.',
  'home_verticals_title': 'Soluções por Segmento',
  'home_verticals_gov': 'Governo e Administração Pública',
  'home_verticals_gov_desc': 'Preservação estruturada de atos administrativos, decisões e documentos oficiais.',
  'home_verticals_corp': 'Empresas e Corporações',
  'home_verticals_corp_desc': 'Gestão de evidências contratuais, transacionais e corporativas com rastreabilidade.',
  'home_verticals_personal': 'Pessoas Físicas',
  'home_verticals_personal_desc': 'Proteção de evidências pessoais relevantes para defesa de direitos individuais.',
  'home_pillars_title': 'Pilares da Infraestrutura',
  'home_pillars_preservation': 'Preservação Probatória',
  'home_pillars_preservation_desc': 'Registro cronológico e estruturado de ativos digitais com potencial relevância jurídica.',
  'home_pillars_integrity': 'Integridade Técnica',
  'home_pillars_integrity_desc': 'Mecanismos criptográficos que asseguram inviolabilidade e autenticidade verificável.',
  'home_pillars_custody': 'Cadeia de Custódia',
  'home_pillars_custody_desc': 'Rastreamento completo de todos os eventos relacionados ao ativo digital preservado.',
  'home_pillars_admissibility': 'Admissibilidade Probatória',
  'home_pillars_admissibility_desc': 'Estrutura fundamentada em legislação processual brasileira para uso em procedimentos judiciais.',
  'home_applicability_title': 'Aplicabilidade Jurídica',
  'home_applicability_desc': 'A preservação probatória digital pode ser utilizada para instrução de processos judiciais, defesas administrativas, procedimentos arbitrais, investigações internas e formalizações notariais, conforme avaliação da autoridade competente.',
  'home_cta_title': 'Iniciar Preservação Probatória',
  'home_cta_desc': 'Estruture suas evidências digitais com integridade técnica verificável e suporte à eventual formalização notarial.',
  'home_cta_button': 'Acessar Plataforma',
  'government.content': 'Infraestrutura para preservação de atos administrativos e decisões governamentais.'
};

// Traduções em inglês
const LEGACY_MAP_EN = {
  'site_title': 'Tutela Digital® - Legal Custody of Digital Assets',
  'site_description': 'Infrastructure for legal custody and governance of digital assets with legal validity, technical inviolability and auditable chain of custody.',
  'nav_home': 'Home',
  'nav_governo': 'Government',
  'nav_empresas': 'Companies',
  'nav_pessoas': 'Individuals',
  'nav_como_funciona': 'How It Works',
  'nav_seguranca': 'Security',
  'hero_subtitle': 'Legal infrastructure for digital custody with verifiable technical integrity and structured probative validity.',
  'home_trust_title': 'Institutional Trust',
  'home_trust_p1': 'Tutela Digital® offers structured digital evidentiary preservation infrastructure for public organizations, companies and individuals who need technical documentation of digital assets with verifiable integrity.',
  'home_trust_p2': 'Operated by NetCenter, a company with 30 years of experience in technological infrastructure, the solution integrates legal compliance, technical security and corporate governance.',
  'home_verticals_title': 'Solutions by Segment',
  'home_verticals_gov': 'Government and Public Administration',
  'home_verticals_gov_desc': 'Structured preservation of administrative acts, decisions and official documents.',
  'home_verticals_corp': 'Companies and Corporations',
  'home_verticals_corp_desc': 'Management of contractual, transactional and corporate evidence with traceability.',
  'home_verticals_personal': 'Individuals',
  'home_verticals_personal_desc': 'Protection of personal evidence relevant to the defense of individual rights.',
  'home_pillars_title': 'Infrastructure Pillars',
  'home_pillars_preservation': 'Evidentiary Preservation',
  'home_pillars_preservation_desc': 'Chronological and structured recording of digital assets with potential legal relevance.',
  'home_pillars_integrity': 'Technical Integrity',
  'home_pillars_integrity_desc': 'Cryptographic mechanisms that ensure inviolability and verifiable authenticity.',
  'home_pillars_custody': 'Chain of Custody',
  'home_pillars_custody_desc': 'Complete tracking of all events related to the preserved digital asset.',
  'home_pillars_admissibility': 'Evidentiary Admissibility',
  'home_pillars_admissibility_desc': 'Structure based on Brazilian procedural law for use in judicial proceedings.',
  'home_applicability_title': 'Legal Applicability',
  'home_applicability_desc': 'Digital evidentiary preservation can be used for instruction of judicial proceedings, administrative defenses, arbitration procedures, internal investigations and notarial formalizations, subject to evaluation by the competent authority.',
  'home_cta_title': 'Start Evidentiary Preservation',
  'home_cta_desc': 'Structure your digital evidence with verifiable technical integrity and support for possible notarial formalization.',
  'home_cta_button': 'Access Platform',
  'government.content': 'Infrastructure for preservation of administrative acts and government decisions.'
};

// Traduções em espanhol
const LEGACY_MAP_ES = {
  'site_title': 'Tutela Digital® - Custodia Legal de Activos Digitales',
  'site_description': 'Infraestructura de custodia legal y gobernanza de activos digitales con validez legal, inviolabilidad técnica y cadena de custodia auditable.',
  'nav_home': 'Inicio',
  'nav_governo': 'Gobierno',
  'nav_empresas': 'Empresas',
  'nav_pessoas': 'Individuos',
  'nav_como_funciona': 'Cómo Funciona',
  'nav_seguranca': 'Seguridad',
  'hero_subtitle': 'Infraestructura jurídica de custodia digital con integridad técnica verificable y validez probatoria estructurada.',
  'home_trust_title': 'Confianza Institucional',
  'home_trust_p1': 'Tutela Digital® ofrece infraestructura estructurada de preservación probatoria digital para organizaciones públicas, empresas e individuos que necesitan documentación técnica de activos digitales con integridad verificable.',
  'home_trust_p2': 'Operada por NetCenter, empresa con 30 años de experiencia en infraestructura tecnológica, la solución integra cumplimiento legal, seguridad técnica y gobernanza corporativa.',
  'home_verticals_title': 'Soluciones por Segmento',
  'home_verticals_gov': 'Gobierno y Administración Pública',
  'home_verticals_gov_desc': 'Preservación estructurada de actos administrativos, decisiones y documentos oficiales.',
  'home_verticals_corp': 'Empresas y Corporaciones',
  'home_verticals_corp_desc': 'Gestión de evidencias contractuales, transaccionales y corporativas con trazabilidad.',
  'home_verticals_personal': 'Individuos',
  'home_verticals_personal_desc': 'Protección de evidencias personales relevantes para la defensa de derechos individuales.',
  'home_pillars_title': 'Pilares de la Infraestructura',
  'home_pillars_preservation': 'Preservación Probatoria',
  'home_pillars_preservation_desc': 'Registro cronológico y estructurado de activos digitales con potencial relevancia jurídica.',
  'home_pillars_integrity': 'Integridad Técnica',
  'home_pillars_integrity_desc': 'Mecanismos criptográficos que aseguran inviolabilidad y autenticidad verificable.',
  'home_pillars_custody': 'Cadena de Custodia',
  'home_pillars_custody_desc': 'Seguimiento completo de todos los eventos relacionados con el activo digital preservado.',
  'home_pillars_admissibility': 'Admisibilidad Probatoria',
  'home_pillars_admissibility_desc': 'Estructura fundamentada en legislación procesal brasileña para uso en procedimientos judiciales.',
  'home_applicability_title': 'Aplicabilidad Jurídica',
  'home_applicability_desc': 'La preservación probatoria digital puede ser utilizada para instrucción de procesos judiciales, defensas administrativas, procedimientos arbitrales, investigaciones internas y formalizaciones notariales, según evaluación de la autoridad competente.',
  'home_cta_title': 'Iniciar Preservación Probatoria',
  'home_cta_desc': 'Estructure sus evidencias digitales con integridad técnica verificable y soporte para eventual formalización notarial.',
  'home_cta_button': 'Acceder a la Plataforma',
  'government.content': 'Infraestructura para preservación de actos administrativos y decisiones gubernamentales.'
};

function addLegacyKeys(lang, legacyMap) {
  const filePath = path.join(LANG_DIR, `${lang}.json`);
  const content = fs.readFileSync(filePath, 'utf8');
  const data = JSON.parse(content);
  
  // Adicionar chaves legadas no nível raiz
  Object.keys(legacyMap).forEach(key => {
    if (!data[key]) {
      data[key] = legacyMap[key];
    }
  });
  
  // Salvar com formatação bonita
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
  console.log(`✅ ${lang}.json atualizado com ${Object.keys(legacyMap).length} chaves legadas`);
}

console.log('🔧 Adicionando chaves legadas aos arquivos de idioma...\n');

addLegacyKeys('pt', LEGACY_MAP);
addLegacyKeys('en', LEGACY_MAP_EN);
addLegacyKeys('es', LEGACY_MAP_ES);

console.log('\n✅ Todas as chaves legadas foram adicionadas!');
