#!/usr/bin/env python3
"""
Adiciona atributos data-i18n faltantes na página seguranca.html
para permitir tradução completa para EN/ES
"""
import re
from pathlib import Path

def add_i18n_to_security():
    """Adiciona data-i18n em todos os elementos que precisam tradução"""
    
    file_path = Path('public/seguranca.html')
    print(f"📄 Processando: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes = []
    
    # 1. Subtitle do hero (linha ~404)
    pattern1 = r'(<p class="page-header-subtitle">)Fundamentos técnicos e jurídicos que sustentam a infraestrutura de preservação probatória\.(</p>)'
    if re.search(pattern1, content):
        content = re.sub(
            pattern1,
            r'\1<span data-i18n="security.p1">Fundamentos técnicos e jurídicos que sustentam a infraestrutura de preservação probatória.</span>\2',
            content
        )
        changes.append("Subtitle do hero")
    
    # 2. Título "Arquitetura de Segurança"
    pattern2 = r'(<h2>)Arquitetura de Segurança(</h2>)'
    if re.search(pattern2, content):
        content = re.sub(
            pattern2,
            r'\1<span data-i18n="security.h2Main">Arquitetura de Segurança</span>\2',
            content
        )
        changes.append("Título 'Arquitetura de Segurança'")
    
    # 3. Primeiro parágrafo da seção de arquitetura
    pattern3 = r'(<p>)A infraestrutura da Tutela Digital® foi estruturada para oferecer mecanismos técnicos de preservação de integridade e rastreabilidade combinados com documentação jurídica\. Cada componente do sistema foi desenvolvido considerando requisitos de segurança da informação, conformidade regulatória e reconhecimento probatório\.(</p>)'
    if re.search(pattern3, content):
        content = re.sub(
            pattern3,
            r'\1<span data-i18n="security.p2">A infraestrutura da Tutela Digital® foi estruturada para oferecer mecanismos técnicos de preservação de integridade e rastreabilidade combinados com documentação jurídica. Cada componente do sistema foi desenvolvido considerando requisitos de segurança da informação, conformidade regulatória e reconhecimento probatório.</span>\2',
            content
        )
        changes.append("Parágrafo 1 da arquitetura")
    
    # 4. Segundo parágrafo da seção de arquitetura
    pattern4 = r'(<p>)A integração com o sistema e-Notariado garante que o processo de onboarding seja realizado com fé pública, enquanto mecanismos técnicos estruturados asseguram a integridade e rastreabilidade dos ativos ao longo de todo o ciclo de preservação\.(</p>)'
    if re.search(pattern4, content):
        content = re.sub(
            pattern4,
            r'\1<span data-i18n="security.p3">A integração com o sistema e-Notariado garante que o processo de onboarding seja realizado com fé pública, enquanto mecanismos técnicos estruturados asseguram a integridade e rastreabilidade dos ativos ao longo de todo o ciclo de preservação.</span>\2',
            content
        )
        changes.append("Parágrafo 2 da arquitetura")
    
    # 5. Subtitle "Pilares de Segurança"
    pattern5 = r'(<h3 class="security-subtitle">)Pilares de Segurança(</h3>)'
    if re.search(pattern5, content):
        content = re.sub(
            pattern5,
            r'\1<span data-i18n="security.h2Secondary">Pilares de Segurança</span>\2',
            content
        )
        changes.append("Subtitle 'Pilares de Segurança'")
    
    # 6-11. Cards de segurança (títulos e descrições sem data-i18n)
    
    # Card 1: e-Notariado
    pattern6 = r'(<h3>)e-Notariado(</h3>\s*<p>)Onboarding com validação de identidade através da plataforma oficial dos cartórios brasileiros, garantindo fé pública\.(</p>)'
    if re.search(pattern6, content, re.DOTALL):
        content = re.sub(
            pattern6,
            r'\1<span data-i18n="security.eNotarialTitle">e-Notariado</span>\2<span data-i18n="security.eNotarialDesc">Onboarding com validação de identidade através da plataforma oficial dos cartórios brasileiros, garantindo fé pública.</span>\3',
            content,
            flags=re.DOTALL
        )
        changes.append("Card 'e-Notariado'")
    
    # Card 2: Não Repúdio
    pattern7 = r'(<h3>)Não Repúdio(</h3>\s*<p>)Mecanismos técnicos e jurídicos que impedem a negação de autoria ou alteração dos ativos custodiados\.(</p>)'
    if re.search(pattern7, content, re.DOTALL):
        content = re.sub(
            pattern7,
            r'\1<span data-i18n="security.nonRepudiationTitle">Não Repúdio</span>\2<span data-i18n="security.nonRepudiationDesc">Mecanismos técnicos e jurídicos que impedem a negação de autoria ou alteração dos ativos custodiados.</span>\3',
            content,
            flags=re.DOTALL
        )
        changes.append("Card 'Não Repúdio'")
    
    # Card 3: Criptografia (descrição)
    pattern8 = r'(<h3 class="subsection-title" data-i18n="security\.h3Encryption">Criptografia de Ponta a Ponta</h3>\s*<p>)Algoritmos de criptografia de alto padrão que protegem os ativos durante transmissão e armazenamento\.(</p>)'
    if re.search(pattern8, content, re.DOTALL):
        content = re.sub(
            pattern8,
            r'\1<span data-i18n="security.encryptionDesc">Algoritmos de criptografia de alto padrão que protegem os ativos durante transmissão e armazenamento.</span>\2',
            content,
            flags=re.DOTALL
        )
        changes.append("Card 'Criptografia' (descrição)")
    
    # Card 4: Registro Técnico (descrição)
    pattern9 = r'(<h4 class="detail-title" data-i18n="security\.h4BlockchainRecord">Registro Distribuído como Prova Complementar</h4>\s*<p>)Registro distribuído e imutável que garante a integridade e rastreabilidade de todas as operações\.(</p>)'
    if re.search(pattern9, content, re.DOTALL):
        content = re.sub(
            pattern9,
            r'\1<span data-i18n="security.blockchainDesc">Registro distribuído e imutável que garante a integridade e rastreabilidade de todas as operações.</span>\2',
            content,
            flags=re.DOTALL
        )
        changes.append("Card 'Registro Técnico' (descrição)")
    
    # Card 5: Cadeia de Custódia
    pattern10 = r'(<h3>)Cadeia de Custódia Imutável(</h3>\s*<p>)Histórico completo e inalterável de todas as ações realizadas sobre cada ativo digital custodiado\.(</p>)'
    if re.search(pattern10, content, re.DOTALL):
        content = re.sub(
            pattern10,
            r'\1<span data-i18n="security.chainOfCustodyTitle">Cadeia de Custódia Imutável</span>\2<span data-i18n="security.chainOfCustodyDesc">Histórico completo e inalterável de todas as ações realizadas sobre cada ativo digital custodiado.</span>\3',
            content,
            flags=re.DOTALL
        )
        changes.append("Card 'Cadeia de Custódia'")
    
    # Card 6: Validade Probatória
    pattern11 = r'(<h3>)Validade Probatória(</h3>\s*<p>)Suporte à admissibilidade dos ativos preservados como prova em procedimentos administrativos e judiciais\.(</p>)'
    if re.search(pattern11, content, re.DOTALL):
        content = re.sub(
            pattern11,
            r'\1<span data-i18n="security.evidentialValidityTitle">Validade Probatória</span>\2<span data-i18n="security.evidentialValidityDesc">Suporte à admissibilidade dos ativos preservados como prova em procedimentos administrativos e judiciais.</span>\3',
            content,
            flags=re.DOTALL
        )
        changes.append("Card 'Validade Probatória'")
    
    # 12. Seção "Confiabilidade Probatória"
    pattern12 = r'(<h2>)Confiabilidade Probatória(</h2>\s*<p>)A confiabilidade jurídica da prova digital depende da demonstração de integridade, rastreabilidade e controle de autoria\. A arquitetura foi estruturada para atender a esses requisitos técnicos\.(</p>)'
    if re.search(pattern12, content, re.DOTALL):
        content = re.sub(
            pattern12,
            r'\1<span data-i18n="security.reliabilityTitle">Confiabilidade Probatória</span>\2<span data-i18n="security.reliabilityDesc">A confiabilidade jurídica da prova digital depende da demonstração de integridade, rastreabilidade e controle de autoria. A arquitetura foi estruturada para atender a esses requisitos técnicos.</span>\3',
            content,
            flags=re.DOTALL
        )
        changes.append("Seção 'Confiabilidade Probatória'")
    
    # 13-14. CTA final
    pattern13 = r'(<h2>)Conheça nossa infraestrutura de segurança(</h2>)'
    if re.search(pattern13, content):
        content = re.sub(
            pattern13,
            r'\1<span data-i18n="security.ctaTitle">Conheça nossa infraestrutura de segurança</span>\2',
            content
        )
        changes.append("CTA título")
    
    pattern14 = r'(<p>)Acesse a plataforma e conheça nossa infraestrutura de preservação probatória estruturada\.(</p>)'
    if re.search(pattern14, content):
        content = re.sub(
            pattern14,
            r'\1<span data-i18n="security.ctaDesc">Acesse a plataforma e conheça nossa infraestrutura de preservação probatória estruturada.</span>\2',
            content
        )
        changes.append("CTA descrição")
    
    # Salvar alterações
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n✅ {len(changes)} elementos corrigidos:")
        for i, change in enumerate(changes, 1):
            print(f"   {i}. {change}")
        return True
    else:
        print("ℹ️  Nenhuma alteração necessária")
        return False

def main():
    """Executa a correção"""
    print("🔧 CORREÇÃO COMPLETA - i18n Página Segurança")
    print("=" * 60)
    
    if add_i18n_to_security():
        print("\n" + "=" * 60)
        print("✅ CONCLUÍDO: página seguranca.html pronta para tradução PT/EN/ES")
    else:
        print("\n⚠️  Nenhuma alteração foi necessária")

if __name__ == '__main__':
    main()
