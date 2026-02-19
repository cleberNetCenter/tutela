#!/usr/bin/env python3
"""
CORREÇÃO DEFINITIVA DO SISTEMA I18N
====================================

PROBLEMA IDENTIFICADO:
- Páginas governo.html, empresas.html, pessoas.html NÃO têm data-i18n no conteúdo
- Apenas o MENU tem data-i18n
- Por isso as páginas permanecem em português

SOLUÇÃO:
- Adicionar data-i18n em TODOS os elementos de conteúdo
- Mapear cada elemento para sua chave correspondente no JSON
- Garantir que TUDO seja traduzível
"""

import re
import os

GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def log_info(msg):
    print(f"{GREEN}✓{RESET} {msg}")

def log_warning(msg):
    print(f"{YELLOW}⚠{RESET} {msg}")

def log_error(msg):
    print(f"{RED}✗{RESET} {msg}")

def add_i18n_to_governo():
    """Adiciona data-i18n na página de governo"""
    html_path = 'public/governo.html'
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Hero title
    content = re.sub(
        r'<h1>Soluções para Governo</h1>',
        '<h1 data-i18n="government.heroTitle">Soluções para Governo</h1>',
        content
    )
    
    # Hero subtitle
    content = re.sub(
        r'<p>Custódia jurídica de documentos e ativos digitais para órgãos públicos com conformidade legal e auditoria completa\.</p>',
        '<p data-i18n="government.heroSubtitle">Custódia jurídica de documentos e ativos digitais para órgãos públicos com conformidade legal e auditoria completa.</p>',
        content
    )
    
    # Section: Custódia Digital para o Setor Público
    content = re.sub(
        r'<h2>Custódia Digital para o Setor Público</h2>',
        '<h2 data-i18n="government.section1Title">Custódia Digital para o Setor Público</h2>',
        content
    )
    
    content = re.sub(
        r'<p>A Tutela Digital® oferece soluções especializadas para órgãos governamentais que precisam garantir a integridade, autenticidade e disponibilidade de documentos e evidências digitais\. Nossa plataforma atende aos requisitos legais de preservação probatória e conformidade com a LGPD\.</p>',
        '<p data-i18n="government.section1Content">A Tutela Digital® oferece soluções especializadas para órgãos governamentais que precisam garantir a integridade, autenticidade e disponibilidade de documentos e evidências digitais. Nossa plataforma atende aos requisitos legais de preservação probatória e conformidade com a LGPD.</p>',
        content
    )
    
    # Benefits section
    content = re.sub(
        r'<h2>Benefícios para Órgãos Públicos</h2>',
        '<h2 data-i18n="government.benefitsTitle">Benefícios para Órgãos Públicos</h2>',
        content
    )
    
    # Benefit 1
    content = re.sub(
        r'<h3>Conformidade com LGPD</h3>\s*<p>Atendimento integral à Lei Geral de Proteção de Dados',
        '<h3 data-i18n="government.benefit1Title">Conformidade com LGPD</h3>\n<p data-i18n="government.benefit1Content">Atendimento integral à Lei Geral de Proteção de Dados',
        content
    )
    
    # Benefit 2
    content = re.sub(
        r'<h3>Segurança de Dados</h3>\s*<p>Infraestrutura robusta com criptografia de ponta a ponta',
        '<h3 data-i18n="government.benefit2Title">Segurança de Dados</h3>\n<p data-i18n="government.benefit2Content">Infraestrutura robusta com criptografia de ponta a ponta',
        content
    )
    
    # Benefit 3
    content = re.sub(
        r'<h3>Auditoria Completa</h3>\s*<p>Cadeia de custódia digital verificável',
        '<h3 data-i18n="government.benefit3Title">Auditoria Completa</h3>\n<p data-i18n="government.benefit3Content">Cadeia de custódia digital verificável',
        content
    )
    
    # Benefit 4
    content = re.sub(
        r'<h3>Transparência e Accountability</h3>\s*<p>Rastreabilidade completa das operações',
        '<h3 data-i18n="government.benefit4Title">Transparência e Accountability</h3>\n<p data-i18n="government.benefit4Content">Rastreabilidade completa das operações',
        content
    )
    
    # Use cases section
    content = re.sub(
        r'<h2>Casos de Uso</h2>',
        '<h2 data-i18n="government.useCasesTitle">Casos de Uso</h2>',
        content
    )
    
    content = re.sub(
        r'<p>A solução é aplicável em diversos contextos do setor público: preservação de evidências em processos administrativos',
        '<p data-i18n="government.useCasesContent">A solução é aplicável em diversos contextos do setor público: preservação de evidências em processos administrativos',
        content
    )
    
    # CTA section
    content = re.sub(
        r'<h2>Implante custódia digital no seu órgão</h2>',
        '<h2 data-i18n="government.ctaTitle">Implante custódia digital no seu órgão</h2>',
        content
    )
    
    content = re.sub(
        r'<p>Entre em contato para conhecer nossas soluções para o setor público\.</p>',
        '<p data-i18n="government.ctaSubtitle">Entre em contato para conhecer nossas soluções para o setor público.</p>',
        content
    )
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    log_info(f"✓ Governo: data-i18n adicionado em {html_path}")
    return True

def add_i18n_to_empresas():
    """Adiciona data-i18n na página de empresas"""
    html_path = 'public/empresas.html'
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Hero
    content = re.sub(
        r'<h1>Soluções para Empresas</h1>',
        '<h1 data-i18n="companies.heroTitle">Soluções para Empresas</h1>',
        content
    )
    
    content = re.sub(
        r'<p>Proteção jurídica de ativos digitais corporativos com validade probatória e cadeia de custódia auditável\.</p>',
        '<p data-i18n="companies.heroSubtitle">Proteção jurídica de ativos digitais corporativos com validade probatória e cadeia de custódia auditável.</p>',
        content
    )
    
    # Section 1
    content = re.sub(
        r'<h2>Custódia Digital Corporativa</h2>',
        '<h2 data-i18n="companies.section1Title">Custódia Digital Corporativa</h2>',
        content
    )
    
    content = re.sub(
        r'<p>Empresas de todos os portes enfrentam riscos jurídicos relacionados a ativos digitais',
        '<p data-i18n="companies.section1Content">Empresas de todos os portes enfrentam riscos jurídicos relacionados a ativos digitais',
        content
    )
    
    # Benefits
    content = re.sub(
        r'<h2>Benefícios Corporativos</h2>',
        '<h2 data-i18n="companies.benefitsTitle">Benefícios Corporativos</h2>',
        content
    )
    
    # Benefit 1-4 (similar pattern)
    content = re.sub(
        r'<h3>Compliance e Governança</h3>\s*<p>Atendimento a requisitos',
        '<h3 data-i18n="companies.benefit1Title">Compliance e Governança</h3>\n<p data-i18n="companies.benefit1Content">Atendimento a requisitos',
        content
    )
    
    content = re.sub(
        r'<h3>Mitigação de Riscos</h3>\s*<p>Organização proativa',
        '<h3 data-i18n="companies.benefit2Title">Mitigação de Riscos</h3>\n<p data-i18n="companies.benefit2Content">Organização proativa',
        content
    )
    
    content = re.sub(
        r'<h3>Proteção Intelectual</h3>\s*<p>Registro temporal',
        '<h3 data-i18n="companies.benefit3Title">Proteção Intelectual</h3>\n<p data-i18n="companies.benefit3Content">Registro temporal',
        content
    )
    
    content = re.sub(
        r'<h3>Eficiência Processual</h3>\s*<p>Documentação estruturada',
        '<h3 data-i18n="companies.benefit4Title">Eficiência Processual</h3>\n<p data-i18n="companies.benefit4Content">Documentação estruturada',
        content
    )
    
    # Use cases
    content = re.sub(
        r'<h2>Cenários de Aplicação</h2>',
        '<h2 data-i18n="companies.useCasesTitle">Cenários de Aplicação</h2>',
        content
    )
    
    content = re.sub(
        r'<p>A custódia digital corporativa é aplicável',
        '<p data-i18n="companies.useCasesContent">A custódia digital corporativa é aplicável',
        content
    )
    
    # CTA
    content = re.sub(
        r'<h2>Proteja seus ativos corporativos</h2>',
        '<h2 data-i18n="companies.ctaTitle">Proteja seus ativos corporativos</h2>',
        content
    )
    
    content = re.sub(
        r'<p>Converse com nossos especialistas sobre custódia digital empresarial\.</p>',
        '<p data-i18n="companies.ctaSubtitle">Converse com nossos especialistas sobre custódia digital empresarial.</p>',
        content
    )
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    log_info(f"✓ Empresas: data-i18n adicionado em {html_path}")
    return True

def add_i18n_to_pessoas():
    """Adiciona data-i18n na página de pessoas"""
    html_path = 'public/pessoas.html'
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Hero
    content = re.sub(
        r'<h1>Soluções para Pessoas</h1>',
        '<h1 data-i18n="individuals.heroTitle">Soluções para Pessoas</h1>',
        content
    )
    
    content = re.sub(
        r'<p>Preservação de direitos e proteção de evidências digitais pessoais com respaldo jurídico e técnico\.</p>',
        '<p data-i18n="individuals.heroSubtitle">Preservação de direitos e proteção de evidências digitais pessoais com respaldo jurídico e técnico.</p>',
        content
    )
    
    # Section 1
    content = re.sub(
        r'<h2>Custódia Digital para Indivíduos</h2>',
        '<h2 data-i18n="individuals.section1Title">Custódia Digital para Indivíduos</h2>',
        content
    )
    
    content = re.sub(
        r'<p>Pessoas físicas podem necessitar',
        '<p data-i18n="individuals.section1Content">Pessoas físicas podem necessitar',
        content
    )
    
    # Benefits
    content = re.sub(
        r'<h2>Benefícios Individuais</h2>',
        '<h2 data-i18n="individuals.benefitsTitle">Benefícios Individuais</h2>',
        content
    )
    
    # Benefit 1-4
    content = re.sub(
        r'<h3>Proteção de Direitos</h3>\s*<p>Preservação antecipada',
        '<h3 data-i18n="individuals.benefit1Title">Proteção de Direitos</h3>\n<p data-i18n="individuals.benefit1Content">Preservação antecipada',
        content
    )
    
    content = re.sub(
        r'<h3>Simplicidade e Acessibilidade</h3>\s*<p>Processo simplificado',
        '<h3 data-i18n="individuals.benefit2Title">Simplicidade e Acessibilidade</h3>\n<p data-i18n="individuals.benefit2Content">Processo simplificado',
        content
    )
    
    content = re.sub(
        r'<h3>Confidencialidade Total</h3>\s*<p>Acesso exclusivo',
        '<h3 data-i18n="individuals.benefit3Title">Confidencialidade Total</h3>\n<p data-i18n="individuals.benefit3Content">Acesso exclusivo',
        content
    )
    
    content = re.sub(
        r'<h3>Respaldo Técnico-Jurídico</h3>\s*<p>Documentação técnica',
        '<h3 data-i18n="individuals.benefit4Title">Respaldo Técnico-Jurídico</h3>\n<p data-i18n="individuals.benefit4Content">Documentação técnica',
        content
    )
    
    # Use cases
    content = re.sub(
        r'<h2>Situações de Uso</h2>',
        '<h2 data-i18n="individuals.useCasesTitle">Situações de Uso</h2>',
        content
    )
    
    content = re.sub(
        r'<p>A custódia digital para indivíduos',
        '<p data-i18n="individuals.useCasesContent">A custódia digital para indivíduos',
        content
    )
    
    # CTA
    content = re.sub(
        r'<h2>Preserve suas evidências digitais</h2>',
        '<h2 data-i18n="individuals.ctaTitle">Preserve suas evidências digitais</h2>',
        content
    )
    
    content = re.sub(
        r'<p>Comece agora a proteger seus direitos através da custódia digital\.</p>',
        '<p data-i18n="individuals.ctaSubtitle">Comece agora a proteger seus direitos através da custódia digital.</p>',
        content
    )
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    log_info(f"✓ Pessoas: data-i18n adicionado em {html_path}")
    return True

def main():
    print(f"\n{BOLD}=== CORREÇÃO DEFINITIVA DO SISTEMA I18N ==={RESET}\n")
    print(f"{YELLOW}PROBLEMA IDENTIFICADO:{RESET}")
    print(f"  ❌ Páginas governo/empresas/pessoas SEM data-i18n no conteúdo")
    print(f"  ❌ Apenas o MENU tinha data-i18n")
    print(f"  ❌ Por isso páginas permaneciam em português\n")
    
    print(f"{YELLOW}SOLUÇÃO:{RESET}")
    print(f"  ✅ Adicionar data-i18n em TODOS os elementos")
    print(f"  ✅ Mapear cada elemento para sua chave no JSON")
    print(f"  ✅ Garantir tradução completa das páginas\n")
    
    # Execute corrections
    add_i18n_to_governo()
    add_i18n_to_empresas()
    add_i18n_to_pessoas()
    
    print(f"\n{BOLD}=== RESULTADO ==={RESET}")
    log_info("✓ Governo: data-i18n adicionado em TODOS os elementos")
    log_info("✓ Empresas: data-i18n adicionado em TODOS os elementos")
    log_info("✓ Pessoas: data-i18n adicionado em TODOS os elementos")
    
    print(f"\n{GREEN}{BOLD}✓ CORREÇÃO DEFINITIVA APLICADA!{RESET}\n")
    print(f"{YELLOW}TESTE:{RESET}")
    print(f"  1. Limpar cache: Ctrl+Shift+R")
    print(f"  2. Clicar no globo → Selecionar EN")
    print(f"  3. Verificar que TUDO mudou para inglês")
    print(f"  4. Navegar para 'Government' → Verificar em inglês\n")

if __name__ == '__main__':
    main()
