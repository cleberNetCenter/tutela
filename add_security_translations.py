#!/usr/bin/env python3
"""
Adiciona traduções faltantes para a página de segurança
nos arquivos pt.json, en.json, es.json
"""
import json
from pathlib import Path

# Novas chaves a serem adicionadas
new_translations = {
    "pt": {
        "eNotarialTitle": "e-Notariado",
        "eNotarialDesc": "Onboarding com validação de identidade através da plataforma oficial dos cartórios brasileiros, garantindo fé pública.",
        "nonRepudiationTitle": "Não Repúdio",
        "nonRepudiationDesc": "Mecanismos técnicos e jurídicos que impedem a negação de autoria ou alteração dos ativos custodiados.",
        "encryptionDesc": "Algoritmos de criptografia de alto padrão que protegem os ativos durante transmissão e armazenamento.",
        "blockchainDesc": "Registro distribuído e imutável que garante a integridade e rastreabilidade de todas as operações.",
        "chainOfCustodyTitle": "Cadeia de Custódia Imutável",
        "chainOfCustodyDesc": "Histórico completo e inalterável de todas as ações realizadas sobre cada ativo digital custodiado.",
        "evidentialValidityTitle": "Validade Probatória",
        "evidentialValidityDesc": "Suporte à admissibilidade dos ativos preservados como prova em procedimentos administrativos e judiciais.",
        "reliabilityTitle": "Confiabilidade Probatória",
        "reliabilityDesc": "A confiabilidade jurídica da prova digital depende da demonstração de integridade, rastreabilidade e controle de autoria. A arquitetura foi estruturada para atender a esses requisitos técnicos.",
        "ctaTitle": "Conheça nossa infraestrutura de segurança",
        "ctaDesc": "Acesse a plataforma e conheça nossa infraestrutura de preservação probatória estruturada."
    },
    "en": {
        "eNotarialTitle": "e-Notary",
        "eNotarialDesc": "Onboarding with identity validation through the official Brazilian notary platform, ensuring public faith.",
        "nonRepudiationTitle": "Non-Repudiation",
        "nonRepudiationDesc": "Technical and legal mechanisms that prevent the denial of authorship or modification of custodied assets.",
        "encryptionDesc": "High-standard encryption algorithms that protect assets during transmission and storage.",
        "blockchainDesc": "Distributed and immutable ledger that guarantees the integrity and traceability of all operations.",
        "chainOfCustodyTitle": "Immutable Chain of Custody",
        "chainOfCustodyDesc": "Complete and unalterable history of all actions performed on each custodied digital asset.",
        "evidentialValidityTitle": "Evidentiary Validity",
        "evidentialValidityDesc": "Support for admissibility of preserved assets as evidence in administrative and judicial proceedings.",
        "reliabilityTitle": "Evidentiary Reliability",
        "reliabilityDesc": "The legal reliability of digital evidence depends on demonstrating integrity, traceability, and authorship control. The architecture is structured to meet these technical requirements.",
        "ctaTitle": "Learn about our security infrastructure",
        "ctaDesc": "Access the platform and learn about our structured evidentiary preservation infrastructure."
    },
    "es": {
        "eNotarialTitle": "e-Notariado",
        "eNotarialDesc": "Incorporación con validación de identidad a través de la plataforma oficial de notarías brasileñas, garantizando fe pública.",
        "nonRepudiationTitle": "No Repudio",
        "nonRepudiationDesc": "Mecanismos técnicos y jurídicos que impiden la negación de autoría o alteración de activos custodiados.",
        "encryptionDesc": "Algoritmos de cifrado de alto estándar que protegen los activos durante la transmisión y el almacenamiento.",
        "blockchainDesc": "Registro distribuido e inmutable que garantiza la integridad y trazabilidad de todas las operaciones.",
        "chainOfCustodyTitle": "Cadena de Custodia Inmutable",
        "chainOfCustodyDesc": "Historial completo e inalterable de todas las acciones realizadas sobre cada activo digital custodiado.",
        "evidentialValidityTitle": "Validez Probatoria",
        "evidentialValidityDesc": "Soporte para la admisibilidad de activos preservados como prueba en procedimientos administrativos y judiciales.",
        "reliabilityTitle": "Confiabilidad Probatoria",
        "reliabilityDesc": "La confiabilidad jurídica de la prueba digital depende de la demostración de integridad, trazabilidad y control de autoría. La arquitectura está estructurada para cumplir con estos requisitos técnicos.",
        "ctaTitle": "Conozca nuestra infraestructura de seguridad",
        "ctaDesc": "Acceda a la plataforma y conozca nuestra infraestructura de preservación probatoria estructurada."
    }
}

def update_translation_file(lang_code):
    """Atualiza arquivo de tradução com novas chaves"""
    file_path = Path(f'public/assets/lang/{lang_code}.json')
    
    print(f"\n📄 Processando: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Adicionar novas traduções na seção security
    if 'security' not in data:
        data['security'] = {}
    
    added = 0
    for key, value in new_translations[lang_code].items():
        if key not in data['security']:
            data['security'][key] = value
            added += 1
            print(f"   ✓ Adicionado: security.{key}")
    
    if added > 0:
        # Salvar com indentação bonita
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"   ✅ {added} traduções adicionadas")
        return True
    else:
        print(f"   ℹ️  Todas as traduções já existem")
        return False

def main():
    """Atualiza todos os arquivos de tradução"""
    print("🌐 ADICIONANDO TRADUÇÕES - Página Segurança")
    print("=" * 60)
    
    total_updated = 0
    for lang in ['pt', 'en', 'es']:
        if update_translation_file(lang):
            total_updated += 1
    
    print("\n" + "=" * 60)
    print(f"✅ CONCLUÍDO: {total_updated} arquivos atualizados")
    print("\n📋 Novas chaves adicionadas em security:")
    for key in new_translations['pt'].keys():
        print(f"   • security.{key}")

if __name__ == '__main__':
    main()
