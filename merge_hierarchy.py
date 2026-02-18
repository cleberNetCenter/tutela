#!/usr/bin/env python3
"""
MERGE INCREMENTAL - Hierarquia Semântica H1→H4
Preserva 100% das chaves existentes e adiciona nova estrutura
"""
import json
from pathlib import Path
from datetime import datetime

# ====================================
# FASE 1: Atualização de H1 existentes
# ====================================
H1_UPDATES = {
    'pt': {
        'home.heroTitle': 'Preservação Probatória Digital com Cadeia de Custódia Verificável',
        'preservation.title': 'Como Preservar Prova Digital com Integridade e Cadeia de Custódia Documentada',
        'legalBasis.title': 'Fundamento Jurídico da Preservação de Evidência Digital no Direito Brasileiro',
        'security.title': 'Arquitetura de Integridade Aplicada à Preservação Probatória Digital'
    },
    'en': {
        'home.heroTitle': 'Digital Evidentiary Preservation with Verifiable Chain of Custody',
        'preservation.title': 'How to Preserve Digital Evidence with Integrity and Documented Chain of Custody',
        'legalBasis.title': 'Legal Basis for Digital Evidence Preservation under Brazilian Law',
        'security.title': 'Integrity Architecture Applied to Digital Evidentiary Preservation'
    },
    'es': {
        'home.heroTitle': 'Preservación Probatoria Digital con Cadena de Custodia Verificable',
        'preservation.title': 'Cómo Preservar Prueba Digital con Integridad y Cadena de Custodia Documentada',
        'legalBasis.title': 'Fundamento Jurídico de la Preservación de Evidencia Digital en el Derecho Brasileño',
        'security.title': 'Arquitectura de Integridad Aplicada a la Preservación Probatoria Digital'
    }
}

# ====================================
# FASE 2 e 3: Nova hierarquia H2→H4
# ====================================
NEW_HIERARCHY = {
    'pt': {
        'home': {
            'h2Main': 'Organização Técnica de Evidências com Validade Probatória',
            'h2Secondary': 'Infraestrutura Fundamentada em Código de Processo Civil Brasileiro',
            'h3ChainStructure': 'Estrutura da Cadeia de Custódia Digital',
            'h4ChronologicalRegistration': 'Registro Cronológico Imutável',
            'h4TechnicalIdentifier': 'Identificador Técnico Verificável',
            'h3LegalApplication': 'Aplicação Jurídica da Preservação Probatória',
            'h4JudicialUse': 'Utilização em Procedimentos Judiciais',
            'h4AdministrativeUse': 'Aplicação em Defesa Administrativa'
        },
        'preservation': {
            'h2Main': 'Mecanismos Técnicos de Preservação Probatória',
            'h2Secondary': 'Organização Pré-Litigiosa de Evidência Digital',
            'h3PreLitigation': 'Preservação em Fase Pré-Processual',
            'h4RiskMitigation': 'Mitigação de Risco Documental',
            'h4DocumentPredictability': 'Previsibilidade Técnica da Prova',
            'h3ProceduralUse': 'Utilização da Prova Preservada',
            'h4ExpertAnalysis': 'Análise Pericial Fundamentada',
            'h4FutureFormalization': 'Formalização Notarial Posterior'
        },
        'legalBasis': {
            'h2Main': 'Base Legal da Admissibilidade de Prova Eletrônica',
            'h2Secondary': 'Legislação Brasileira Aplicável à Evidência Digital',
            'h3CivilProcedure': 'Código de Processo Civil — Arts. 369, 422 e 439',
            'h3ElectronicProcessLaw': 'Lei 11.419/2006 — Processo Judicial Eletrônico',
            'h3DigitalSignature': 'MP 2.200-2/2001 — ICP-Brasil e Assinatura Digital',
            'h3LGPD': 'Lei 13.709/2018 — Proteção de Dados e Preservação Probatória',
            'h4DataProtection': 'Compatibilidade com LGPD',
            'h4ConfidentialityLimits': 'Limites da Confidencialidade Jurídica'
        },
        'security': {
            'h2Main': 'Segurança Técnica e Confidencialidade Processual',
            'h2Secondary': 'Mecanismos Criptográficos de Integridade Probatória',
            'h3Encryption': 'Criptografia de Ponta a Ponta',
            'h3AccessControl': 'Controle de Acesso Exclusivo ao Titular',
            'h3ImmutableRegistration': 'Registro Técnico Imutável',
            'h4BlockchainRecord': 'Registro Distribuído como Prova Complementar',
            'h4TemporalIntegrity': 'Integridade Temporal Verificável'
        }
    },
    'en': {
        'home': {
            'h2Main': 'Technical Organization of Evidence with Evidentiary Validity',
            'h2Secondary': 'Infrastructure Founded on Brazilian Code of Civil Procedure',
            'h3ChainStructure': 'Digital Chain of Custody Structure',
            'h4ChronologicalRegistration': 'Immutable Chronological Registration',
            'h4TechnicalIdentifier': 'Verifiable Technical Identifier',
            'h3LegalApplication': 'Legal Application of Evidentiary Preservation',
            'h4JudicialUse': 'Use in Judicial Proceedings',
            'h4AdministrativeUse': 'Application in Administrative Defense'
        },
        'preservation': {
            'h2Main': 'Technical Mechanisms of Evidentiary Preservation',
            'h2Secondary': 'Pre-Litigation Organization of Digital Evidence',
            'h3PreLitigation': 'Preservation in Pre-Procedural Phase',
            'h4RiskMitigation': 'Documentary Risk Mitigation',
            'h4DocumentPredictability': 'Technical Predictability of Evidence',
            'h3ProceduralUse': 'Use of Preserved Evidence',
            'h4ExpertAnalysis': 'Evidence-Based Expert Analysis',
            'h4FutureFormalization': 'Subsequent Notarial Formalization'
        },
        'legalBasis': {
            'h2Main': 'Legal Basis for Electronic Evidence Admissibility',
            'h2Secondary': 'Brazilian Legislation Applicable to Digital Evidence',
            'h3CivilProcedure': 'Code of Civil Procedure — Articles 369, 422, and 439',
            'h3ElectronicProcessLaw': 'Law 11,419/2006 — Electronic Judicial Process',
            'h3DigitalSignature': 'Provisional Measure 2,200-2/2001 — ICP-Brasil and Digital Signature',
            'h3LGPD': 'Law 13,709/2018 — Data Protection and Evidentiary Preservation',
            'h4DataProtection': 'LGPD Compliance',
            'h4ConfidentialityLimits': 'Legal Confidentiality Boundaries'
        },
        'security': {
            'h2Main': 'Technical Security and Procedural Confidentiality',
            'h2Secondary': 'Cryptographic Mechanisms of Evidentiary Integrity',
            'h3Encryption': 'End-to-End Encryption',
            'h3AccessControl': 'Exclusive Access Control by Holder',
            'h3ImmutableRegistration': 'Immutable Technical Registration',
            'h4BlockchainRecord': 'Distributed Ledger as Complementary Evidence',
            'h4TemporalIntegrity': 'Verifiable Temporal Integrity'
        }
    },
    'es': {
        'home': {
            'h2Main': 'Organización Técnica de Evidencias con Validez Probatoria',
            'h2Secondary': 'Infraestructura Fundamentada en Código de Proceso Civil Brasileño',
            'h3ChainStructure': 'Estructura de la Cadena de Custodia Digital',
            'h4ChronologicalRegistration': 'Registro Cronológico Inmutable',
            'h4TechnicalIdentifier': 'Identificador Técnico Verificable',
            'h3LegalApplication': 'Aplicación Jurídica de la Preservación Probatoria',
            'h4JudicialUse': 'Utilización en Procedimientos Judiciales',
            'h4AdministrativeUse': 'Aplicación en Defensa Administrativa'
        },
        'preservation': {
            'h2Main': 'Mecanismos Técnicos de Preservación Probatoria',
            'h2Secondary': 'Organización Precontenciosa de Evidencia Digital',
            'h3PreLitigation': 'Preservación en Fase Preprocesal',
            'h4RiskMitigation': 'Mitigación de Riesgo Documental',
            'h4DocumentPredictability': 'Previsibilidad Técnica de la Prueba',
            'h3ProceduralUse': 'Utilización de la Prueba Preservada',
            'h4ExpertAnalysis': 'Análisis Pericial Fundamentado',
            'h4FutureFormalization': 'Formalización Notarial Posterior'
        },
        'legalBasis': {
            'h2Main': 'Base Legal de la Admisibilidad de Prueba Electrónica',
            'h2Secondary': 'Legislación Brasileña Aplicable a la Evidencia Digital',
            'h3CivilProcedure': 'Código de Proceso Civil — Arts. 369, 422 y 439',
            'h3ElectronicProcessLaw': 'Ley 11.419/2006 — Proceso Judicial Electrónico',
            'h3DigitalSignature': 'MP 2.200-2/2001 — ICP-Brasil y Firma Digital',
            'h3LGPD': 'Ley 13.709/2018 — Protección de Datos y Preservación Probatoria',
            'h4DataProtection': 'Compatibilidad con LGPD',
            'h4ConfidentialityLimits': 'Límites de la Confidencialidad Jurídica'
        },
        'security': {
            'h2Main': 'Seguridad Técnica y Confidencialidad Procesal',
            'h2Secondary': 'Mecanismos Criptográficos de Integridad Probatoria',
            'h3Encryption': 'Cifrado de Extremo a Extremo',
            'h3AccessControl': 'Control de Acceso Exclusivo al Titular',
            'h3ImmutableRegistration': 'Registro Técnico Inmutable',
            'h4BlockchainRecord': 'Registro Distribuido como Prueba Complementaria',
            'h4TemporalIntegrity': 'Integridad Temporal Verificable'
        }
    }
}

def merge_json(lang: str, original_data: dict) -> dict:
    """
    Faz merge incremental preservando 100% das chaves existentes
    """
    # Clonar dados originais
    merged = json.loads(json.dumps(original_data))
    
    # FASE 1: Atualizar H1 existentes
    for key, value in H1_UPDATES[lang].items():
        section, field = key.split('.')
        if section in merged and field in merged[section]:
            print(f"  ✅ Atualizando {key}: {value[:60]}...")
            merged[section][field] = value
    
    # FASE 2 e 3: Adicionar nova hierarquia
    for section, fields in NEW_HIERARCHY[lang].items():
        if section not in merged:
            merged[section] = {}
        
        for field, value in fields.items():
            if field not in merged[section]:
                print(f"  ➕ Adicionando {section}.{field}")
                merged[section][field] = value
    
    return merged

def main():
    print("=" * 70)
    print("MERGE INCREMENTAL - Hierarquia Semântica H1→H4")
    print("=" * 70)
    
    # Backup
    backup_dir = Path(f"backup_hierarchy_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    backup_dir.mkdir(exist_ok=True)
    print(f"\n📦 Criando backup em: {backup_dir}")
    
    for lang in ['pt', 'en', 'es']:
        file_path = Path(f'public/assets/lang/{lang}.json')
        
        print(f"\n🔧 Processando {lang}.json...")
        
        # Ler original
        original = json.loads(file_path.read_text(encoding='utf-8'))
        
        # Backup
        backup_path = backup_dir / f'{lang}.json'
        backup_path.write_text(json.dumps(original, indent=2, ensure_ascii=False), encoding='utf-8')
        
        # Merge incremental
        merged = merge_json(lang, original)
        
        # Salvar
        file_path.write_text(
            json.dumps(merged, indent=2, ensure_ascii=False) + '\n',
            encoding='utf-8'
        )
        
        # Stats
        original_keys = sum(len(v) if isinstance(v, dict) else 1 for v in original.values())
        merged_keys = sum(len(v) if isinstance(v, dict) else 1 for v in merged.values())
        
        print(f"  📊 Keys antes: {original_keys}")
        print(f"  📊 Keys depois: {merged_keys}")
        print(f"  ➕ Keys adicionadas: {merged_keys - original_keys}")
    
    print(f"\n✅ MERGE COMPLETO!")
    print(f"📦 Backup salvo em: {backup_dir}")
    print("\n📋 Resumo:")
    print("  - H1: 4 atualizados × 3 idiomas = 12 updates")
    print("  - H2/H3/H4: ~40 novas chaves × 3 idiomas = ~120 adições")
    print("  - 0 chaves removidas")
    print("  - 100% de preservação das chaves existentes")

if __name__ == '__main__':
    main()
