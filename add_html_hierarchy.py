#!/usr/bin/env python3
"""
FASE 4 - Adicionar hierarquia semântica H2→H4 nos HTMLs
Preserva layout, CSS e estrutura existente
"""
from pathlib import Path
import re

# CSS classes para a hierarquia
CSS_CLASSES = {
    'h2': 'section-title',
    'h3': 'subsection-title',
    'h4': 'detail-title'
}

# Adicionar CSS se necessário
NEW_CSS = """
/* Hierarquia Semântica H2→H4 */
.section-title {
  font-size: 2rem;
  font-weight: 600;
  margin: 2.5rem 0 1.5rem 0;
  color: var(--color-primary, #1a1a1a);
  line-height: 1.3;
}

.subsection-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 2rem 0 1rem 0;
  color: var(--color-secondary, #333);
  line-height: 1.4;
}

.detail-title {
  font-size: 1.25rem;
  font-weight: 500;
  margin: 1.5rem 0 0.75rem 0;
  color: var(--color-text, #444);
  line-height: 1.5;
}
"""

def add_css_to_file(file_path: Path):
    """Adiciona CSS para hierarquia semântica"""
    print(f"\n📝 Verificando CSS em {file_path.name}...")
    
    content = file_path.read_text(encoding='utf-8')
    
    # Verifica se já tem as classes
    if 'section-title' in content and 'subsection-title' in content:
        print("  ✅ CSS já existe, pulando...")
        return
    
    # Encontra o último </style> ou cria novo
    if '</style>' in content:
        content = content.replace('</style>', f'\n{NEW_CSS}\n</style>', 1)
        print("  ➕ CSS adicionado ao <style> existente")
    else:
        # Adiciona antes de </head>
        content = content.replace('</head>', f'<style>{NEW_CSS}</style>\n</head>', 1)
        print("  ➕ <style> criado com CSS")
    
    file_path.write_text(content, encoding='utf-8')

def add_headings_to_home_section(content: str) -> str:
    """
    Adiciona H2/H3/H4 na seção home (hero)
    """
    # Procura pelo hero-subtitle
    pattern = r'(<p[^>]*data-i18n="home\.heroSubtitle"[^>]*>.*?</p>)'
    
    if not re.search(pattern, content, re.DOTALL):
        print("  ⚠️  home.heroSubtitle não encontrado")
        return content
    
    # Adiciona H2 principal depois do subtitle
    h2_main = '''
  <h2 class="section-title" data-i18n="home.h2Main">Organização Técnica de Evidências com Validade Probatória</h2>
'''
    
    content = re.sub(
        pattern,
        r'\1' + h2_main,
        content,
        count=1,
        flags=re.DOTALL
    )
    
    print("  ✅ H2/H3/H4 adicionados na seção home")
    return content

def add_headings_to_preservation_page(file_path: Path):
    """
    Adiciona hierarquia H2→H4 na página preservacao-probatoria-digital.html
    """
    print(f"\n📝 Processando {file_path.name}...")
    
    if not file_path.exists():
        print(f"  ⚠️  Arquivo não existe, pulando...")
        return
    
    content = file_path.read_text(encoding='utf-8')
    
    # Procura pelo H1 existente
    h1_pattern = r'(<h1[^>]*data-i18n="preservation\.title"[^>]*>.*?</h1>)'
    
    if not re.search(h1_pattern, content, re.DOTALL):
        print("  ⚠️  H1 preservation.title não encontrado")
        return
    
    # Adiciona H2/H3/H4 depois do H1
    new_hierarchy = '''
  
  <h2 class="section-title" data-i18n="preservation.h2Main">Mecanismos Técnicos de Preservação Probatória</h2>
  <h2 class="section-title" data-i18n="preservation.h2Secondary">Organização Pré-Litigiosa de Evidência Digital</h2>
  
  <section class="semantic-section">
    <h3 class="subsection-title" data-i18n="preservation.h3PreLitigation">Preservação em Fase Pré-Processual</h3>
    <h4 class="detail-title" data-i18n="preservation.h4RiskMitigation">Mitigação de Risco Documental</h4>
    <h4 class="detail-title" data-i18n="preservation.h4DocumentPredictability">Previsibilidade Técnica da Prova</h4>
  </section>
  
  <section class="semantic-section">
    <h3 class="subsection-title" data-i18n="preservation.h3ProceduralUse">Utilização da Prova Preservada</h3>
    <h4 class="detail-title" data-i18n="preservation.h4ExpertAnalysis">Análise Pericial Fundamentada</h4>
    <h4 class="detail-title" data-i18n="preservation.h4FutureFormalization">Formalização Notarial Posterior</h4>
  </section>
'''
    
    content = re.sub(
        h1_pattern,
        r'\1' + new_hierarchy,
        content,
        count=1,
        flags=re.DOTALL
    )
    
    file_path.write_text(content, encoding='utf-8')
    print("  ✅ Hierarquia H2→H4 adicionada")

def add_headings_to_legal_basis_page(file_path: Path):
    """
    Adiciona hierarquia H2→H4 na página fundamento-juridico.html
    """
    print(f"\n📝 Processando {file_path.name}...")
    
    if not file_path.exists():
        print(f"  ⚠️  Arquivo não existe, pulando...")
        return
    
    content = file_path.read_text(encoding='utf-8')
    
    # Procura pelo H1 existente
    h1_pattern = r'(<h1[^>]*data-i18n="legalBasis\.title"[^>]*>.*?</h1>)'
    
    if not re.search(h1_pattern, content, re.DOTALL):
        print("  ⚠️  H1 legalBasis.title não encontrado")
        return
    
    # Adiciona H2/H3/H4 depois do H1
    new_hierarchy = '''
  
  <h2 class="section-title" data-i18n="legalBasis.h2Main">Base Legal da Admissibilidade de Prova Eletrônica</h2>
  <h2 class="section-title" data-i18n="legalBasis.h2Secondary">Legislação Brasileira Aplicável à Evidência Digital</h2>
  
  <section class="semantic-section">
    <h3 class="subsection-title" data-i18n="legalBasis.h3CivilProcedure">Código de Processo Civil — Arts. 369, 422 e 439</h3>
    <h3 class="subsection-title" data-i18n="legalBasis.h3ElectronicProcessLaw">Lei 11.419/2006 — Processo Judicial Eletrônico</h3>
    <h3 class="subsection-title" data-i18n="legalBasis.h3DigitalSignature">MP 2.200-2/2001 — ICP-Brasil e Assinatura Digital</h3>
  </section>
  
  <section class="semantic-section">
    <h3 class="subsection-title" data-i18n="legalBasis.h3LGPD">Lei 13.709/2018 — Proteção de Dados e Preservação Probatória</h3>
    <h4 class="detail-title" data-i18n="legalBasis.h4DataProtection">Compatibilidade com LGPD</h4>
    <h4 class="detail-title" data-i18n="legalBasis.h4ConfidentialityLimits">Limites da Confidencialidade Jurídica</h4>
  </section>
'''
    
    content = re.sub(
        h1_pattern,
        r'\1' + new_hierarchy,
        content,
        count=1,
        flags=re.DOTALL
    )
    
    file_path.write_text(content, encoding='utf-8')
    print("  ✅ Hierarquia H2→H4 adicionada")

def add_headings_to_security_page(file_path: Path):
    """
    Adiciona hierarquia H2→H4 na página seguranca.html
    """
    print(f"\n📝 Processando {file_path.name}...")
    
    if not file_path.exists():
        print(f"  ⚠️  Arquivo não existe, pulando...")
        return
    
    content = file_path.read_text(encoding='utf-8')
    
    # Procura pelo H1 existente
    h1_pattern = r'(<h1[^>]*data-i18n="security\.title"[^>]*>.*?</h1>)'
    
    if not re.search(h1_pattern, content, re.DOTALL):
        print("  ⚠️  H1 security.title não encontrado")
        return
    
    # Adiciona H2/H3/H4 depois do H1
    new_hierarchy = '''
  
  <h2 class="section-title" data-i18n="security.h2Main">Segurança Técnica e Confidencialidade Processual</h2>
  <h2 class="section-title" data-i18n="security.h2Secondary">Mecanismos Criptográficos de Integridade Probatória</h2>
  
  <section class="semantic-section">
    <h3 class="subsection-title" data-i18n="security.h3Encryption">Criptografia de Ponta a Ponta</h3>
    <h3 class="subsection-title" data-i18n="security.h3AccessControl">Controle de Acesso Exclusivo ao Titular</h3>
  </section>
  
  <section class="semantic-section">
    <h3 class="subsection-title" data-i18n="security.h3ImmutableRegistration">Registro Técnico Imutável</h3>
    <h4 class="detail-title" data-i18n="security.h4BlockchainRecord">Registro Distribuído como Prova Complementar</h4>
    <h4 class="detail-title" data-i18n="security.h4TemporalIntegrity">Integridade Temporal Verificável</h4>
  </section>
'''
    
    content = re.sub(
        h1_pattern,
        r'\1' + new_hierarchy,
        content,
        count=1,
        flags=re.DOTALL
    )
    
    file_path.write_text(content, encoding='utf-8')
    print("  ✅ Hierarquia H2→H4 adicionada")

def main():
    print("=" * 70)
    print("FASE 4 - Adicionar Hierarquia Semântica H2→H4 nos HTMLs")
    print("=" * 70)
    
    public_dir = Path('public')
    
    # Adicionar CSS
    html_files = [
        public_dir / 'index.html',
        public_dir / 'preservacao-probatoria-digital.html',
        public_dir / 'fundamento-juridico.html',
        public_dir / 'seguranca.html'
    ]
    
    for html_file in html_files:
        if html_file.exists():
            add_css_to_file(html_file)
    
    # Adicionar headings nas páginas
    add_headings_to_preservation_page(public_dir / 'preservacao-probatoria-digital.html')
    add_headings_to_legal_basis_page(public_dir / 'fundamento-juridico.html')
    add_headings_to_security_page(public_dir / 'seguranca.html')
    
    print("\n✅ FASE 4 CONCLUÍDA!")
    print("📋 Hierarquia H2→H4 adicionada em 3 páginas")
    print("🎨 CSS semântico adicionado")

if __name__ == '__main__':
    main()
