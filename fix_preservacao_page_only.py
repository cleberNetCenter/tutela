#!/usr/bin/env python3
"""
fix_preservacao_page_only.py

Correções SOMENTE na página preservacao-probatoria-digital.html:
1. Centralizar e corrigir fonte dos títulos:
   - "Elementos da Cadeia de Custódia Digital"
   - "Fundamento Jurídico da Preservação Digital"
2. Corrigir estrutura do primeiro card "Identificação do Ativo"
"""

import re

FILE = "public/legal/preservacao-probatoria-digital.html"

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_page():
    print("🔧 Corrigindo página preservacao-probatoria-digital.html")
    
    html = read_file(FILE)
    
    # PROBLEMA 1: Título "Elementos da Cadeia de Custódia Digital"
    # Está fora do container, precisa estar dentro com classe correta
    
    # Encontrar o bloco da seção features com esse título
    pattern1 = r'(<section class="features">\s*<div class="features-inner">\s*)(<h2>Elementos da Cadeia de Custódia Digital</h2>)'
    
    replacement1 = r'''\1<div class="legal-section-title-wrapper">
  \2
</div>'''
    
    html = re.sub(pattern1, replacement1, html)
    print("  ✓ Título 'Elementos da Cadeia' envolto em wrapper")
    
    # PROBLEMA 2: Título "Fundamento Jurídico da Preservação Digital"
    # Mesmo problema, fora do container adequado
    
    pattern2 = r'(<section class="features">\s*<div class="features-inner">\s*)(<h2>Fundamento Jurídico da Preservação Digital</h2>)'
    
    replacement2 = r'''\1<div class="legal-section-title-wrapper">
  \2
</div>'''
    
    html = re.sub(pattern2, replacement2, html)
    print("  ✓ Título 'Fundamento Jurídico' envolto em wrapper")
    
    # PROBLEMA 3: Primeiro card "Identificação do Ativo" com div extra
    # A estrutura está assim:
    # <div class="legal-grid">
    #   <div class="feature-item">
    #     <h3>Identificação do Ativo</h3>
    #     <p>...</p>
    #   </div>
    # </div>  <- Esta div fecha o grid prematuramente!
    # <div class="feature-item"> <- Os outros cards ficam fora do grid
    
    # Precisamos remover essa div extra e garantir que todos os cards estejam dentro de legal-grid
    
    # Encontrar o bloco do grid
    grid_pattern = r'(<div class="legal-grid-wrapper">\s*<div class="legal-grid">)(.*?)(</div>\s*</div>)(\s*<div class="feature-item">.*?</section>)'
    
    def fix_grid(match):
        wrapper_open = match.group(1)
        first_card = match.group(2)
        premature_close = match.group(3)
        rest_cards = match.group(4)
        
        # Remover os fechamentos prematuros
        # Encontrar todos os cards restantes
        all_cards_after = re.findall(r'<div class="feature-item">.*?</div>', rest_cards, re.DOTALL)
        
        # Reconstruir o grid com todos os cards dentro
        new_grid = wrapper_open + first_card
        
        for card in all_cards_after:
            new_grid += "\n" + card
        
        # Fechar o grid corretamente
        new_grid += "\n    </div>\n  </div>"
        
        # Adicionar o fechamento da seção
        section_close = "\n</div>\n</section>"
        
        return new_grid + section_close
    
    # Aplicar fix no grid
    html = re.sub(grid_pattern, fix_grid, html, flags=re.DOTALL)
    print("  ✓ Estrutura do grid de cards corrigida")
    
    write_file(FILE, html)
    print("✅ Página salva")
    
    return True

def create_css_fix():
    """
    Criar CSS específico para esta página
    Será inline na própria página para não afetar outras
    """
    css = """
<!-- CSS Fix - Preservação Probatória -->
<style>
/* Títulos das seções features - centralizar e fonte display */
.legal-section-title-wrapper {
  max-width: 820px;
  margin: 0 auto 3rem auto;
  text-align: center;
}

.legal-section-title-wrapper h2 {
  font-family: var(--font-display);
  font-size: clamp(2rem, 3.5vw, 2.5rem);
  font-weight: 500;
  color: var(--color-text-strong);
  line-height: 1.25;
}

/* Garantir que todos os cards tenham altura mínima consistente */
.legal-grid .feature-item {
  min-height: 200px;
  display: flex;
  flex-direction: column;
}

.legal-grid .feature-item h3 {
  margin-bottom: 1rem;
}

.legal-grid .feature-item p {
  flex: 1;
}
</style>
"""
    
    html = read_file(FILE)
    
    # Verificar se já existe CSS inline
    if 'CSS Fix - Preservação Probatória' in html:
        print("  ⚠️  CSS inline já existe")
        return
    
    # Adicionar CSS antes do </head>
    html = html.replace('</head>', css + '\n</head>')
    
    write_file(FILE, html)
    print("  ✓ CSS inline adicionado")

def main():
    print("=" * 70)
    print("🔬 CORREÇÕES - PRESERVAÇÃO PROBATÓRIA (SOMENTE ESTA PÁGINA)")
    print("=" * 70)
    
    print("\n🎯 Correções a aplicar:")
    print("  1. Centralizar título 'Elementos da Cadeia de Custódia Digital'")
    print("  2. Centralizar título 'Fundamento Jurídico da Preservação Digital'")
    print("  3. Corrigir fonte dos títulos (font-display)")
    print("  4. Corrigir estrutura do card 'Identificação do Ativo'")
    
    # Aplicar correções HTML
    fix_page()
    
    # Adicionar CSS inline
    print("\n📝 Adicionando CSS inline...")
    create_css_fix()
    
    print("\n" + "=" * 70)
    print("✅ CORREÇÕES CONCLUÍDAS")
    print("=" * 70)
    
    print("\n🎯 Resultado esperado:")
    print("  ✓ Títulos centralizados com fonte display")
    print("  ✓ Todos os cards com altura consistente")
    print("  ✓ Grid funcionando corretamente")
    print("  ✓ Apenas esta página afetada")
    
    print("\n⚠️  Validar em:")
    print("  https://www.tuteladigital.com.br/legal/preservacao-probatoria-digital.html")

if __name__ == "__main__":
    main()
