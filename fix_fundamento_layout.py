#!/usr/bin/env python3
"""
fix_fundamento_layout.py

Aplicar mesmo layout da página preservacao em fundamento-juridico:
1. Corrigir estrutura HTML dos cards
2. Centralizar e ajustar fonte do título "Princípios Jurídicos Aplicáveis"
3. Adicionar CSS inline: 1 card por linha, largura total, altura reduzida
"""

import re

FILE = "public/legal/fundamento-juridico.html"

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_first_card():
    """Corrigir estrutura do primeiro card (adicionar </div> faltante)"""
    print("\n1️⃣ Corrigindo estrutura do primeiro card...")
    
    html = read_file(FILE)
    
    # O primeiro card está sem fechamento
    pattern = r'(<div class="feature-item">\s*<h3>Livre Convencimento Motivado</h3>\s*<p>O juiz aprecia livremente a prova, atendendo aos fatos e circunstâncias constantes dos autos\.</p>)\s*(</div>\s*</div>\s*<div class="feature-item">)'
    
    replacement = r'\1\n</div>\n\n\2'
    
    html = re.sub(pattern, replacement, html)
    
    print("  ✓ Tag </div> adicionada ao primeiro card")
    
    write_file(FILE, html)

def wrap_title():
    """Envolver título em wrapper para centralização"""
    print("\n2️⃣ Centralizando título 'Princípios Jurídicos'...")
    
    html = read_file(FILE)
    
    # Envolver o título em wrapper
    pattern = r'(<section class="features">\s*<div class="features-inner">\s*)(<h2>Princípios Jurídicos Aplicáveis</h2>)'
    
    replacement = r'\1<div class="legal-section-title-wrapper">\n  \2\n</div>'
    
    html = re.sub(pattern, replacement, html)
    
    print("  ✓ Título envolto em .legal-section-title-wrapper")
    
    write_file(FILE, html)

def add_inline_css():
    """Adicionar CSS inline para layout 1 card por linha"""
    print("\n3️⃣ Adicionando CSS inline...")
    
    html = read_file(FILE)
    
    # Verificar se já existe CSS inline
    if 'CSS Fix - Fundamento Jurídico' in html:
        print("  ⚠️  CSS inline já existe")
        return
    
    css = """
<!-- CSS Fix - Fundamento Jurídico -->
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

/* Cards: 1 por linha, largura total, altura reduzida */
.legal-grid {
  grid-template-columns: 1fr !important;
  gap: 1.5rem !important;
}

.legal-grid .feature-item {
  min-height: 100px;
  display: flex;
  flex-direction: column;
  padding: 1.5rem 2rem;
}

.legal-grid .feature-item h3 {
  margin-bottom: 0.75rem;
  font-size: 1.1rem;
}

.legal-grid .feature-item p {
  flex: 1;
  margin: 0;
}
</style>
"""
    
    # Adicionar antes do </head>
    html = html.replace('</head>', css + '\n</head>')
    
    print("  ✓ CSS inline adicionado")
    print("    - Grid: 1 coluna (1fr)")
    print("    - Min-height: 100px")
    print("    - Gap: 1.5rem")
    print("    - Padding: 1.5rem 2rem")
    
    write_file(FILE, html)

def main():
    print("=" * 70)
    print("🔬 APLICAR LAYOUT EM FUNDAMENTO JURÍDICO")
    print("=" * 70)
    
    print("\n🎯 Objetivo:")
    print("  • Corrigir estrutura HTML dos cards")
    print("  • Centralizar título 'Princípios Jurídicos Aplicáveis'")
    print("  • 1 card por linha, largura total, altura reduzida")
    
    # Executar correções
    fix_first_card()
    wrap_title()
    add_inline_css()
    
    print("\n" + "=" * 70)
    print("✅ LAYOUT APLICADO COM SUCESSO")
    print("=" * 70)
    
    print("\n📊 Resultado esperado:")
    print("  ✓ Título 'Princípios Jurídicos' centralizado")
    print("  ✓ 4 cards em layout vertical (1 por linha)")
    print("  ✓ Largura total horizontal")
    print("  ✓ Altura reduzida (100px)")
    print("  ✓ Layout consistente com página preservação")
    
    print("\n⚠️  Validar em:")
    print("  https://www.tuteladigital.com.br/legal/fundamento-juridico.html")

if __name__ == "__main__":
    main()
