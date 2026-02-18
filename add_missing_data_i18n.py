#!/usr/bin/env python3
"""
Script para adicionar data-i18n em TODOS os textos das páginas
(não apenas títulos, mas também parágrafos, listas, etc.)
"""
import re
from pathlib import Path

def add_data_i18n_institucional():
    """Adiciona data-i18n em todos os textos de institucional.html"""
    file_path = Path('public/institucional.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Substituições linha por linha
    replacements = [
        # Subtitle
        (r'<p>Informações jurídicas e estruturais da entidade responsável pela preservação probatória digital\.</p>',
         r'<p data-i18n="institucional.subtitle">Informações jurídicas e estruturais da entidade responsável pela preservação probatória digital.</p>'),
        
        # Legal ID section - manter texto hard-coded para CNPJ/endereço (dados factuais)
        (r'<p>A Tutela Digital® é infraestrutura privada de preservação probatória digital desenvolvida no Brasil, com atuação nacional\.</p>',
         r'<p data-i18n="institucional.legalIdDescription">A Tutela Digital® é infraestrutura privada de preservação probatória digital desenvolvida no Brasil, com atuação nacional.</p>'),
        
        # Activity Nature paragraphs
        (r'<p>A Tutela Digital® não exerce função cartorial e não substitui tabelionato\.</p>',
         r'<p data-i18n="institucional.activityNatureP1">A Tutela Digital® não exerce função cartorial e não substitui tabelionato.</p>'),
        (r'<p>Sua atuação consiste na preservação técnica estruturada de ativos digitais com cadeia de custódia verificável, integridade criptográfica e registro temporal imutável\.</p>',
         r'<p data-i18n="institucional.activityNatureP2">Sua atuação consiste na preservação técnica estruturada de ativos digitais com cadeia de custódia verificável, integridade criptográfica e registro temporal imutável.</p>'),
        (r'<p>Quando solicitado, os ativos podem ser submetidos à formalização cartorial por meio de ata notarial junto a tabelionato competente\.</p>',
         r'<p data-i18n="institucional.activityNatureP3">Quando solicitado, os ativos podem ser submetidos à formalização cartorial por meio de ata notarial junto a tabelionato competente.</p>'),
        
        # Legal Basis paragraphs
        (r'<p>A admissibilidade da prova digital fundamenta-se no Código de Processo Civil, na Lei nº 11\.419/2006, na Medida Provisória nº 2\.200-2/2001 e na Lei nº 13\.709/2018 \(LGPD\)\.</p>',
         r'<p data-i18n="institucional.legalBasisP1">A admissibilidade da prova digital fundamenta-se no Código de Processo Civil, na Lei nº 11.419/2006, na Medida Provisória nº 2.200-2/2001 e na Lei nº 13.709/2018 (LGPD).</p>'),
        (r'<p>A integridade e autenticidade podem ser demonstradas por mecanismos técnicos idôneos e cadeia de custódia verificável\.</p>',
         r'<p data-i18n="institucional.legalBasisP2">A integridade e autenticidade podem ser demonstradas por mecanismos técnicos idôneos e cadeia de custódia verificável.</p>'),
        
        # Interoperability paragraphs
        (r'<p>A infraestrutura permite interoperabilidade com tabelionatos para eventual emissão de ata notarial, mediante solicitação do titular\.</p>',
         r'<p data-i18n="institucional.interopP1">A infraestrutura permite interoperabilidade com tabelionatos para eventual emissão de ata notarial, mediante solicitação do titular.</p>'),
        (r'<p>A formalização notarial ocorre exclusivamente pelo tabelionato competente\.</p>',
         r'<p data-i18n="institucional.interopP2">A formalização notarial ocorre exclusivamente pelo tabelionato competente.</p>'),
        
        # Governance paragraphs
        (r'<p>A plataforma foi desenvolvida pela NetCenter, empresa com mais de 30 anos de atuação em tecnologia da informação\.</p>',
         r'<p data-i18n="institucional.govP1">A plataforma foi desenvolvida pela NetCenter, empresa com mais de 30 anos de atuação em tecnologia da informação.</p>'),
        (r'<p>O produto Tutela Digital® opera como unidade especializada com foco exclusivo em preservação probatória digital\.</p>',
         r'<p data-i18n="institucional.govP2">O produto Tutela Digital® opera como unidade especializada com foco exclusivo em preservação probatória digital.</p>'),
        (r'<p>Detalhes técnicos proprietários não são divulgados publicamente para preservação de segurança e propriedade intelectual\.</p>',
         r'<p data-i18n="institucional.govP3">Detalhes técnicos proprietários não são divulgados publicamente para preservação de segurança e propriedade intelectual.</p>'),
        
        # CTA text
        (r'<p>Conheça também os fundamentos jurídicos e termos de custódia\.</p>',
         r'<p data-i18n="institucional.ctaText">Conheça também os fundamentos jurídicos e termos de custódia.</p>'),
    ]
    
    for old, new in replacements:
        content = re.sub(old, new, content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ institucional.html: adicionados data-i18n em parágrafos")

def add_data_i18n_privacy():
    """Adiciona data-i18n em todos os textos de politica-de-privacidade.html"""
    file_path = Path('public/politica-de-privacidade.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Adicionar data-i18n no subtitle
    content = re.sub(
        r'<p>Diretrizes aplicáveis ao tratamento de dados pessoais no contexto da custódia probatória digital\.</p>',
        r'<p data-i18n="privacy.subtitle">Diretrizes aplicáveis ao tratamento de dados pessoais no contexto da custódia probatória digital.</p>',
        content
    )
    
    # Precisamos adicionar data-i18n nos parágrafos de cada seção
    # Por simplicidade, vou usar um padrão que detecta parágrafos após cada H2
    
    # Scope section
    content = re.sub(
        r'(<h2 data-i18n="privacy\.scope_title">.*?</h2>\s*<div class="text-block-inner">\s*)<p>(A presente Política de Privacidade.*?LGPD\)\.)</p>',
        r'\1<p data-i18n="privacy.scope_text">\2</p>',
        content,
        flags=re.DOTALL
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ politica-de-privacidade.html: adicionados data-i18n em parágrafos")

def main():
    print("=" * 80)
    print("🔧 ADICIONANDO data-i18n EM TODOS OS TEXTOS")
    print("=" * 80)
    print()
    
    add_data_i18n_institucional()
    add_data_i18n_privacy()
    
    print()
    print("=" * 80)
    print("✅ CONCLUSÃO")
    print("=" * 80)
    print()
    
    # Contar data-i18n em cada página
    for page in ['institucional.html', 'politica-de-privacidade.html', 'fundamento-juridico.html', 'termos-de-custodia.html']:
        file_path = Path(f'public/{page}')
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                count = f.read().count('data-i18n')
            print(f"  {page}: {count} data-i18n attributes")
    print()

if __name__ == "__main__":
    main()
