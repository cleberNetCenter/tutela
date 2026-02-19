#!/usr/bin/env python3
"""
Adicionar traduções PT completas para páginas MPA (governo/empresas/pessoas)
=============================================================================
Problema: pt.json tem apenas 2 chaves, en.json e es.json têm 17 chaves cada
Solução: Adicionar todas as 45 traduções faltantes (3 páginas × 15 chaves)
"""

import json

def main():
    print("🌐 ADICIONANDO TRADUÇÕES PT PARA PÁGINAS MPA\n")
    
    pt_json_path = "/home/user/webapp/public/assets/lang/pt.json"
    
    # 1. Ler JSON atual
    print("1️⃣ Lendo pt.json...")
    with open(pt_json_path, 'r', encoding='utf-8') as f:
        pt_data = json.load(f)
    
    print(f"   ✅ JSON carregado")
    
    # 2. Preparar traduções completas
    print("\n2️⃣ Preparando traduções PT...")
    
    # Traduções para GOVERNO
    pt_data["government"] = {
        "heroTitle": "Soluções para Governo",
        "heroSubtitle": "Custódia jurídica de documentos e ativos digitais para órgãos públicos com conformidade LGPD, segurança de dados e auditoria completa.",
        "section1Title": "Custódia Digital para o Setor Público",
        "section1Content": "A Tutela Digital® oferece soluções especializadas para órgãos governamentais que precisam garantir a integridade, autenticidade e disponibilidade de documentos e evidências digitais. Nossa plataforma atende aos requisitos legais de preservação probatória e conformidade com a LGPD.",
        "benefitsTitle": "Benefícios para Órgãos Públicos",
        "benefit1Title": "Conformidade com LGPD",
        "benefit1Content": "Atendimento integral à Lei Geral de Proteção de Dados, garantindo a privacidade e segurança das informações dos cidadãos.",
        "benefit2Title": "Segurança de Dados",
        "benefit2Content": "Infraestrutura robusta com criptografia de ponta a ponta, controles de acesso rigorosos e logs auditáveis de todas as operações.",
        "benefit3Title": "Auditoria Completa",
        "benefit3Content": "Cadeia de custódia digital verificável, com registros temporais criptografados e documentação técnica para fins probatórios.",
        "benefit4Title": "Transparência e Accountability",
        "benefit4Content": "Rastreabilidade completa das operações, atendendo aos princípios da administração pública e facilitando processos de fiscalização.",
        "useCasesTitle": "Casos de Uso",
        "useCasesContent": "A solução é aplicável em diversos contextos do setor público: preservação de evidências em processos administrativos, custódia de documentos oficiais, arquivamento de licitações e contratos, gestão de provas digitais em investigações, e conformidade com requisitos de transparência e accountability.",
        "ctaTitle": "Implemente custódia digital em seu órgão",
        "ctaSubtitle": "Entre em contato para conhecer nossas soluções para o setor público."
    }
    
    print("   ✅ Governo: 17 chaves")
    
    # Traduções para EMPRESAS
    pt_data["companies"] = {
        "heroTitle": "Soluções para Empresas",
        "heroSubtitle": "Custódia jurídica de documentos e ativos digitais para empresas com conformidade LGPD, proteção de evidências e gestão de riscos.",
        "section1Title": "Custódia Digital para Empresas",
        "section1Content": "A Tutela Digital® oferece soluções especializadas para empresas que precisam proteger evidências digitais, garantir conformidade legal e gerenciar riscos jurídicos. Nossa plataforma atende aos requisitos de preservação probatória, LGPD e documentação de processos corporativos.",
        "benefitsTitle": "Benefícios para Empresas",
        "benefit1Title": "Proteção de Evidências",
        "benefit1Content": "Preservação técnica de e-mails, contratos, documentos e comunicações digitais com validade probatória para litígios empresariais.",
        "benefit2Title": "Conformidade LGPD",
        "benefit2Content": "Demonstre conformidade com a Lei Geral de Proteção de Dados através de registros auditáveis e cadeia de custódia verificável.",
        "benefit3Title": "Gestão de Riscos",
        "benefit3Content": "Reduza riscos jurídicos corporativos com documentação estruturada de processos, contratos e evidências digitais.",
        "benefit4Title": "Due Diligence",
        "benefit4Content": "Facilite processos de due diligence e auditoria com documentação técnica estruturada e cadeia de custódia auditável.",
        "useCasesTitle": "Casos de Uso",
        "useCasesContent": "A solução é aplicável em diversos contextos corporativos: proteção de evidências em litígios trabalhistas, preservação de contratos e comunicações comerciais, documentação de processos de compliance, gestão de propriedade intelectual e conformidade com requisitos regulatórios do setor.",
        "ctaTitle": "Proteja sua empresa com custódia digital",
        "ctaSubtitle": "Entre em contato para conhecer nossas soluções empresariais."
    }
    
    print("   ✅ Empresas: 17 chaves")
    
    # Traduções para PESSOAS
    pt_data["individuals"] = {
        "heroTitle": "Soluções para Pessoas Físicas",
        "heroSubtitle": "Custódia jurídica de documentos e evidências digitais para proteção de direitos individuais e validade probatória.",
        "section1Title": "Custódia Digital para Pessoas Físicas",
        "section1Content": "A Tutela Digital® oferece soluções especializadas para pessoas físicas que precisam proteger evidências digitais, preservar comunicações importantes e garantir validade probatória de documentos. Nossa plataforma democratiza o acesso à tecnologia profissional de preservação probatória.",
        "benefitsTitle": "Benefícios para Pessoas Físicas",
        "benefit1Title": "Proteção de Direitos",
        "benefit1Content": "Preserve evidências digitais de assédio, difamação, ameaças ou violações de direitos com validade probatória.",
        "benefit2Title": "Documentação Jurídica",
        "benefit2Content": "Garanta autenticidade e integridade de conversas, e-mails e documentos para uso em processos judiciais ou administrativos.",
        "benefit3Title": "Privacidade e Controle",
        "benefit3Content": "Você mantém controle total sobre suas evidências, com criptografia de ponta a ponta e acesso exclusivo aos seus dados.",
        "benefit4Title": "Facilidade de Uso",
        "benefit4Content": "Interface intuitiva e processo simplificado, permitindo que qualquer pessoa proteja suas evidências digitais sem conhecimento técnico.",
        "useCasesTitle": "Casos de Uso",
        "useCasesContent": "A solução é aplicável em diversos contextos pessoais: proteção contra cyberbullying e assédio digital, preservação de evidências em disputas contratuais, documentação de danos morais, proteção de direitos autorais e propriedade intelectual pessoal, e preservação de comunicações em disputas familiares ou trabalhistas.",
        "ctaTitle": "Proteja seus direitos com custódia digital",
        "ctaSubtitle": "Entre em contato para conhecer nossas soluções para pessoas físicas."
    }
    
    print("   ✅ Pessoas: 17 chaves")
    
    # 3. Salvar JSON atualizado
    print("\n3️⃣ Salvando pt.json atualizado...")
    with open(pt_json_path, 'w', encoding='utf-8') as f:
        json.dump(pt_data, f, ensure_ascii=False, indent=2)
    
    print("   ✅ Arquivo salvo!")
    
    # 4. Resumo
    print("\n✅ TRADUÇÕES PT COMPLETAS ADICIONADAS!")
    print("\n📊 RESUMO:")
    print(f"   • Governo: 2 → 17 chaves (+15)")
    print(f"   • Empresas: 2 → 17 chaves (+15)")
    print(f"   • Pessoas: 2 → 17 chaves (+15)")
    print(f"   • TOTAL: 6 → 51 chaves (+45)")
    
    print("\n📋 Chaves adicionadas por página:")
    print("   1. heroTitle")
    print("   2. heroSubtitle")
    print("   3. section1Title")
    print("   4. section1Content")
    print("   5. benefitsTitle")
    print("   6. benefit1Title")
    print("   7. benefit1Content")
    print("   8. benefit2Title")
    print("   9. benefit2Content")
    print("   10. benefit3Title")
    print("   11. benefit3Content")
    print("   12. benefit4Title")
    print("   13. benefit4Content")
    print("   14. useCasesTitle")
    print("   15. useCasesContent")
    print("   16. ctaTitle")
    print("   17. ctaSubtitle")
    
    print("\n✅ Páginas governo.html, empresas.html, pessoas.html agora funcionam em PORTUGUÊS!")

if __name__ == "__main__":
    main()
