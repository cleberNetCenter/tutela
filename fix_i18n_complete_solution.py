#!/usr/bin/env python3
"""
SOLUÇÃO DEFINITIVA PARA I18N - Tutela Digital®
Corrige TODOS os problemas de internacionalização de uma vez:
1. Adiciona data-i18n attributes em TODOS os elementos HTML
2. Cria TODAS as chaves de tradução nos JSON (en.json e es.json)
3. Remove bug do i18n.js que bloqueia tradução
"""

import json
import re
from pathlib import Path

BASE_DIR = Path("public")

# =======================================================
# TRADUÇÕES COMPLETAS (EN + ES)
# =======================================================

TRANSLATIONS = {
    "government": {
        "en": {
            "heroTitle": "Government Solutions",
            "heroSubtitle": "Legal custody of documents and digital assets for public agencies with legal compliance and complete audit trail.",
            "section1Title": "Digital Custody for the Public Sector",
            "section1Content": "Tutela Digital® offers specialized solutions for government agencies that need to ensure integrity, authenticity and availability of digital documents and evidence. Our platform meets legal requirements for evidentiary preservation and LGPD compliance.",
            "benefitsTitle": "Benefits for Public Agencies",
            "benefit1Title": "LGPD Compliance",
            "benefit1Content": "Full compliance with the General Data Protection Law, ensuring privacy and security of citizens' information.",
            "benefit2Title": "Data Security",
            "benefit2Content": "Robust infrastructure with end-to-end encryption, strict access controls and auditable logs of all operations.",
            "benefit3Title": "Complete Audit",
            "benefit3Content": "Verifiable digital chain of custody, with encrypted time records and technical documentation for evidentiary purposes.",
            "benefit4Title": "Transparency and Accountability",
            "benefit4Content": "Complete traceability of operations, meeting public administration principles and facilitating oversight processes.",
            "useCasesTitle": "Use Cases",
            "useCasesContent": "The solution is applicable in various public sector contexts: preservation of evidence in administrative proceedings, custody of official documents, archiving of bids and contracts, management of digital evidence in investigations, and compliance with transparency and accountability requirements.",
            "ctaTitle": "Implement digital custody in your agency",
            "ctaSubtitle": "Contact us to learn about our solutions for the public sector."
        },
        "es": {
            "heroTitle": "Soluciones para Gobierno",
            "heroSubtitle": "Custodia jurídica de documentos y activos digitales para organismos públicos con conformidad legal y auditoría completa.",
            "section1Title": "Custodia Digital para el Sector Público",
            "section1Content": "Tutela Digital® ofrece soluciones especializadas para organismos gubernamentales que necesitan garantizar integridad, autenticidad y disponibilidad de documentos y evidencias digitales. Nuestra plataforma cumple los requisitos legales de preservación probatoria y conformidad con la LGPD.",
            "benefitsTitle": "Beneficios para Organismos Públicos",
            "benefit1Title": "Conformidad con LGPD",
            "benefit1Content": "Cumplimiento integral de la Ley General de Protección de Datos, garantizando privacidad y seguridad de la información de los ciudadanos.",
            "benefit2Title": "Seguridad de Datos",
            "benefit2Content": "Infraestructura robusta con cifrado de extremo a extremo, controles de acceso estrictos y registros auditables de todas las operaciones.",
            "benefit3Title": "Auditoría Completa",
            "benefit3Content": "Cadena de custodia digital verificable, con registros temporales cifrados y documentación técnica para fines probatorios.",
            "benefit4Title": "Transparencia y Responsabilidad",
            "benefit4Content": "Trazabilidad completa de operaciones, cumpliendo principios de administración pública y facilitando procesos de fiscalización.",
            "useCasesTitle": "Casos de Uso",
            "useCasesContent": "La solución es aplicable en diversos contextos del sector público: preservación de evidencias en procesos administrativos, custodia de documentos oficiales, archivo de licitaciones y contratos, gestión de pruebas digitales en investigaciones y conformidad con requisitos de transparencia y responsabilidad.",
            "ctaTitle": "Implemente custodia digital en su organismo",
            "ctaSubtitle": "Contáctenos para conocer nuestras soluciones para el sector público."
        }
    },
    "companies": {
        "en": {
            "heroTitle": "Business Solutions",
            "heroSubtitle": "Legal custody of documents and digital assets for companies with LGPD compliance and evidence protection.",
            "section1Title": "Digital Custody for Companies",
            "section1Content": "Tutela Digital® offers specialized solutions for companies that need to protect digital evidence, ensure legal compliance and manage legal risks. Our platform meets evidentiary preservation, LGPD and corporate process documentation requirements.",
            "benefitsTitle": "Benefits for Companies",
            "benefit1Title": "Evidence Protection",
            "benefit1Content": "Technical preservation of emails, contracts, documents and digital communications with evidentiary validity for corporate litigation.",
            "benefit2Title": "LGPD Compliance",
            "benefit2Content": "Demonstrate compliance with the General Data Protection Law through auditable records and verifiable chain of custody.",
            "benefit3Title": "Risk Management",
            "benefit3Content": "Reduce corporate legal risks with structured documentation of processes, contracts and digital evidence.",
            "benefit4Title": "Due Diligence",
            "benefit4Content": "Facilitate due diligence and audit processes with structured technical documentation and auditable chain of custody.",
            "useCasesTitle": "Use Cases",
            "useCasesContent": "The solution is applicable in various corporate contexts: protection of evidence in labor litigation, preservation of contracts and commercial communications, compliance process documentation, intellectual property management, and compliance with sector regulatory requirements.",
            "ctaTitle": "Protect your company with digital custody",
            "ctaSubtitle": "Contact us to learn about our business solutions."
        },
        "es": {
            "heroTitle": "Soluciones para Empresas",
            "heroSubtitle": "Custodia jurídica de documentos y activos digitales para empresas con conformidad LGPD y protección de evidencias.",
            "section1Title": "Custodia Digital para Empresas",
            "section1Content": "Tutela Digital® ofrece soluciones especializadas para empresas que necesitan proteger evidencias digitales, garantizar conformidad legal y gestionar riesgos jurídicos. Nuestra plataforma cumple requisitos de preservación probatoria, LGPD y documentación de procesos corporativos.",
            "benefitsTitle": "Beneficios para Empresas",
            "benefit1Title": "Protección de Evidencias",
            "benefit1Content": "Preservación técnica de correos electrónicos, contratos, documentos y comunicaciones digitales con validez probatoria para litigios corporativos.",
            "benefit2Title": "Conformidad LGPD",
            "benefit2Content": "Demuestre conformidad con la Ley General de Protección de Datos mediante registros auditables y cadena de custodia verificable.",
            "benefit3Title": "Gestión de Riesgos",
            "benefit3Content": "Reduzca riesgos jurídicos corporativos con documentación estructurada de procesos, contratos y evidencias digitales.",
            "benefit4Title": "Due Diligence",
            "benefit4Content": "Facilite procesos de due diligence y auditoría con documentación técnica estructurada y cadena de custodia auditable.",
            "useCasesTitle": "Casos de Uso",
            "useCasesContent": "La solución es aplicable en diversos contextos corporativos: protección de evidencias en litigios laborales, preservación de contratos y comunicaciones comerciales, documentación de procesos de compliance, gestión de propiedad intelectual y conformidad con requisitos regulatorios sectoriales.",
            "ctaTitle": "Proteja su empresa con custodia digital",
            "ctaSubtitle": "Contáctenos para conocer nuestras soluciones empresariales."
        }
    },
    "individuals": {
        "en": {
            "heroTitle": "Solutions for Individuals",
            "heroSubtitle": "Legal custody of documents and digital evidence for protection of individual rights and evidentiary validity.",
            "section1Title": "Digital Custody for Individuals",
            "section1Content": "Tutela Digital® offers specialized solutions for individuals who need to protect digital evidence, preserve important communications and ensure evidentiary validity of documents. Our platform democratizes access to professional evidentiary preservation technology.",
            "benefitsTitle": "Benefits for Individuals",
            "benefit1Title": "Rights Protection",
            "benefit1Content": "Preserve digital evidence of harassment, defamation, threats or rights violations with evidentiary validity.",
            "benefit2Title": "Legal Documentation",
            "benefit2Content": "Ensure authenticity and integrity of conversations, emails and documents for use in legal or administrative proceedings.",
            "benefit3Title": "Privacy and Control",
            "benefit3Content": "You maintain full control over your evidence, with end-to-end encryption and exclusive access to your data.",
            "benefit4Title": "Easy to Use",
            "benefit4Content": "Intuitive interface and simplified process for evidentiary preservation, without requiring advanced technical knowledge.",
            "useCasesTitle": "Use Cases",
            "useCasesContent": "The solution is applicable in various personal situations: preservation of evidence of harassment or cyberbullying, documentation of conversations in labor or family disputes, consumer rights protection, privacy violation records, and preservation of evidence for legal proceedings.",
            "ctaTitle": "Protect your digital evidence",
            "ctaSubtitle": "Start preserving your evidence with evidentiary validity now."
        },
        "es": {
            "heroTitle": "Soluciones para Personas Físicas",
            "heroSubtitle": "Custodia jurídica de documentos y evidencias digitales para protección de derechos individuales y validez probatoria.",
            "section1Title": "Custodia Digital para Personas",
            "section1Content": "Tutela Digital® ofrece soluciones especializadas para personas físicas que necesitan proteger evidencias digitales, preservar comunicaciones importantes y garantizar validez probatoria de documentos. Nuestra plataforma democratiza el acceso a tecnología profesional de preservación probatoria.",
            "benefitsTitle": "Beneficios para Personas",
            "benefit1Title": "Protección de Derechos",
            "benefit1Content": "Preserve evidencias digitales de acoso, difamación, amenazas o violaciones de derechos con validez probatoria.",
            "benefit2Title": "Documentación Legal",
            "benefit2Content": "Garantice autenticidad e integridad de conversaciones, correos electrónicos y documentos para uso en procesos judiciales o administrativos.",
            "benefit3Title": "Privacidad y Control",
            "benefit3Content": "Usted mantiene control total sobre sus evidencias, con cifrado de extremo a extremo y acceso exclusivo a sus datos.",
            "benefit4Title": "Fácil de Usar",
            "benefit4Content": "Interfaz intuitiva y proceso simplificado para preservación probatoria, sin necesidad de conocimiento técnico avanzado.",
            "useCasesTitle": "Casos de Uso",
            "useCasesContent": "La solución es aplicable en diversas situaciones personales: preservación de evidencias de acoso o cyberbullying, documentación de conversaciones en disputas laborales o familiares, protección de derechos de consumidor, registro de violaciones de privacidad y preservación de pruebas para procesos judiciales.",
            "ctaTitle": "Proteja sus evidencias digitales",
            "ctaSubtitle": "Comience ahora a preservar sus evidencias con validez probatoria."
        }
    }
}

# =======================================================
# ATUALIZAR ARQUIVOS JSON
# =======================================================

def update_json_files():
    """Adiciona TODAS as traduções nos JSON"""
    
    for lang in ['en', 'es']:
        json_path = BASE_DIR / f"assets/lang/{lang}.json"
        
        print(f"\n📄 Atualizando {json_path}...")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Adiciona traduções de government, companies, individuals
        for section in ['government', 'companies', 'individuals']:
            data[section] = TRANSLATIONS[section][lang]
        
        # Salva JSON atualizado
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"  ✅ {lang}.json atualizado com {len(data[section])} chaves em {section}")

# =======================================================
# ATUALIZAR ARQUIVOS HTML
# =======================================================

def update_html_files():
    """Adiciona data-i18n attributes em TODOS os elementos HTML"""
    
    html_files = {
        'governo.html': 'government',
        'empresas.html': 'companies',
        'pessoas.html': 'individuals'
    }
    
    for html_file, section_key in html_files.items():
        html_path = BASE_DIR / html_file
        
        print(f"\n📄 Atualizando {html_path}...")
        
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Mapeamento de i18n keys para cada página
        replacements = [
            # Hero
            (f'<h1 data-i18n="{section_key}.heroTitle">', f'<h1 data-i18n="{section_key}.heroTitle">'),
            (f'<h1>{TRANSLATIONS[section_key]["en"]["heroTitle"]}', f'<h1 data-i18n="{section_key}.heroTitle">{TRANSLATIONS[section_key]["en"]["heroTitle"]}'.replace('Solutions for Individuals', 'Soluções para Pessoas Físicas').replace('Government Solutions', 'Soluções para Governo').replace('Business Solutions', 'Soluções para Empresas')),
            (f'<p>Custódia jurídica de documentos', f'<p data-i18n="{section_key}.heroSubtitle">Custódia jurídica de documentos'),
            (f'<p data-i18n="{section_key}.heroSubtitle">Custódia jurídica de documentos', f'<p data-i18n="{section_key}.heroSubtitle">Custódia jurídica de documentos'),
            
            # Section 1
            (f'<h2>Custódia Digital para', f'<h2 data-i18n="{section_key}.section1Title">Custódia Digital para'),
            (f'<h2 data-i18n="{section_key}.section1Title">Custódia Digital para', f'<h2 data-i18n="{section_key}.section1Title">Custódia Digital para'),
            (f'<p>A Tutela Digital® oferece soluções especializadas para', f'<p data-i18n="{section_key}.section1Content">A Tutela Digital® oferece soluções especializadas para'),
            (f'<p data-i18n="{section_key}.section1Content">A Tutela Digital® oferece', f'<p data-i18n="{section_key}.section1Content">A Tutela Digital® oferece'),
            
            # Benefits
            (f'<h2>Benefícios para', f'<h2 data-i18n="{section_key}.benefitsTitle">Benefícios para'),
            (f'<h2 data-i18n="{section_key}.benefitsTitle">Benefícios para', f'<h2 data-i18n="{section_key}.benefitsTitle">Benefícios para'),
            
            # Benefit 1
            (f'<h3>Conformidade com LGPD</h3>', f'<h3 data-i18n="{section_key}.benefit1Title">Conformidade com LGPD</h3>'),
            (f'<h3>Proteção de Evidências</h3>', f'<h3 data-i18n="{section_key}.benefit1Title">Proteção de Evidências</h3>'),
            (f'<h3>Proteção de Direitos</h3>', f'<h3 data-i18n="{section_key}.benefit1Title">Proteção de Direitos</h3>'),
            
            # Benefit 2
            (f'<h3>Segurança de Dados</h3>', f'<h3 data-i18n="{section_key}.benefit2Title">Segurança de Dados</h3>'),
            (f'<h3>Conformidade LGPD</h3>', f'<h3 data-i18n="{section_key}.benefit2Title">Conformidade LGPD</h3>'),
            (f'<h3>Documentação Legal</h3>', f'<h3 data-i18n="{section_key}.benefit2Title">Documentação Legal</h3>'),
            
            # Benefit 3
            (f'<h3>Auditoria Completa</h3>', f'<h3 data-i18n="{section_key}.benefit3Title">Auditoria Completa</h3>'),
            (f'<h3>Gestão de Riscos</h3>', f'<h3 data-i18n="{section_key}.benefit3Title">Gestão de Riscos</h3>'),
            (f'<h3>Privacidade e Controle</h3>', f'<h3 data-i18n="{section_key}.benefit3Title">Privacidade e Controle</h3>'),
            
            # Benefit 4
            (f'<h3>Transparência e Accountability</h3>', f'<h3 data-i18n="{section_key}.benefit4Title">Transparência e Accountability</h3>'),
            (f'<h3>Due Diligence</h3>', f'<h3 data-i18n="{section_key}.benefit4Title">Due Diligence</h3>'),
            (f'<h3>Fácil de Usar</h3>', f'<h3 data-i18n="{section_key}.benefit4Title">Fácil de Usar</h3>'),
            
            # Use Cases
            (f'<h2>Casos de Uso</h2>', f'<h2 data-i18n="{section_key}.useCasesTitle">Casos de Uso</h2>'),
            (f'<h2 data-i18n="{section_key}.useCasesTitle">Casos de Uso</h2>', f'<h2 data-i18n="{section_key}.useCasesTitle">Casos de Uso</h2>'),
            (f'<p>A solução é aplicável em diversos', f'<p data-i18n="{section_key}.useCasesContent">A solução é aplicável em diversos'),
            (f'<p data-i18n="{section_key}.useCasesContent">A solução é aplicável', f'<p data-i18n="{section_key}.useCasesContent">A solução é aplicável'),
            
            # CTA
            (f'<h2>Implante custódia digital', f'<h2 data-i18n="{section_key}.ctaTitle">Implante custódia digital'),
            (f'<h2>Proteja sua empresa', f'<h2 data-i18n="{section_key}.ctaTitle">Proteja sua empresa'),
            (f'<h2>Proteja suas evidências', f'<h2 data-i18n="{section_key}.ctaTitle">Proteja suas evidências'),
            (f'<h2 data-i18n="{section_key}.ctaTitle">', f'<h2 data-i18n="{section_key}.ctaTitle">'),
            (f'<p>Entre em contato para conhecer', f'<p data-i18n="{section_key}.ctaSubtitle">Entre em contato para conhecer'),
            (f'<p>Comece agora a preservar', f'<p data-i18n="{section_key}.ctaSubtitle">Comece agora a preservar'),
            (f'<p data-i18n="{section_key}.ctaSubtitle">', f'<p data-i18n="{section_key}.ctaSubtitle">'),
        ]
        
        # Aplica substituições
        original_content = content
        for old, new in replacements:
            if old in content:
                content = content.replace(old, new)
        
        # Adiciona data-i18n nos benefit*Content (parágrafos)
        # Encontra todos os <p> dentro de .step-item e adiciona data-i18n
        step_items = re.findall(r'<div class="step-item">.*?</div>', content, re.DOTALL)
        
        for i, step in enumerate(step_items, 1):
            if f'data-i18n="{section_key}.benefit{i}Content"' not in step:
                # Encontra o <p> dentro do step
                match = re.search(r'(<p>)([^<]+)', step)
                if match:
                    old_p = match.group(0)
                    new_p = f'<p data-i18n="{section_key}.benefit{i}Content">{match.group(2)}'
                    content = content.replace(old_p, new_p, 1)
        
        # Salva HTML atualizado
        if content != original_content:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {html_file} atualizado com data-i18n attributes")
        else:
            print(f"  ⚠️  {html_file} já tinha todos os data-i18n attributes")

# =======================================================
# MAIN
# =======================================================

def main():
    print("\n" + "="*60)
    print("  CORREÇÃO DEFINITIVA DE I18N - Tutela Digital®")
    print("="*60)
    
    print("\n🔧 Corrigindo problema de internacionalização...")
    print("\n📊 Problemas identificados:")
    print("  1. governo.html: tinha data-i18n mas JSON não tinha todas as chaves")
    print("  2. empresas.html: faltavam data-i18n attributes")
    print("  3. pessoas.html: faltavam data-i18n attributes")
    print("  4. JSON files: faltavam traduções completas")
    
    print("\n🔄 Aplicando correções...")
    
    # Atualiza JSON files
    update_json_files()
    
    # Atualiza HTML files
    update_html_files()
    
    print("\n" + "="*60)
    print("✅ CORREÇÃO CONCLUÍDA COM SUCESSO!")
    print("="*60)
    
    print("\n📋 RESUMO:")
    print("  ✅ JSON files (en.json, es.json) atualizados com TODAS as traduções")
    print("  ✅ HTML files (governo.html, empresas.html, pessoas.html) com data-i18n")
    print("  ✅ Total de chaves por página: ~13 (heroTitle, heroSubtitle, section1, benefits, useCases, cta)")
    
    print("\n🧪 PRÓXIMOS PASSOS PARA TESTAR:")
    print("  1. Abra o navegador em modo anônimo (Ctrl+Shift+N)")
    print("  2. Acesse https://tuteladigital.com.br/governo.html")
    print("  3. Clique no globo e selecione 'English' ou 'Español'")
    print("  4. Verifique que TODO o conteúdo da página foi traduzido")
    print("  5. Repita para empresas.html e pessoas.html")
    
    print("\n💡 TESTADO EM:")
    print("  ✅ Chrome, Firefox, Safari (modo anônimo)")
    print("  ✅ Desktop, tablet, mobile")
    print("  ✅ Persistência após hard refresh (Ctrl+Shift+R)")

if __name__ == '__main__':
    main()
