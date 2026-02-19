#!/usr/bin/env python3
"""
fix_fundamento_cards_uniformly.py

Ajustar cards 2, 3 e 4 para ficarem iguais ao card 1
Baseado na análise da imagem: todos devem ter mesmo fundo, borda e estilo
"""

import re

FILE = "public/legal/fundamento-juridico.html"

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def update_cards_css():
    """Atualizar CSS inline para garantir uniformidade dos cards"""
    print("🔧 Ajustando CSS dos cards...")
    
    html = read_file(FILE)
    
    # Encontrar o CSS inline existente e adicionar regras para uniformidade
    css_pattern = r'(/\* Cards: 1 por linha, largura total, altura reduzida \*/\s*\.legal-grid \{[^}]+\})'
    
    # Novo CSS com estilo uniforme para todos os cards
    new_cards_css = """/* Cards: 1 por linha, largura total, altura reduzida */
.legal-grid {
  grid-template-columns: 1fr !important;
  gap: 1.5rem !important;
}

.legal-grid .feature-item {
  min-height: 100px;
  display: flex;
  flex-direction: column;
  padding: 1.5rem 2rem;
  background: var(--color-surface-light);
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 8px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.legal-grid .feature-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}"""
    
    # Substituir o CSS existente
    html = re.sub(css_pattern, new_cards_css, html)
    
    print("  ✓ CSS atualizado com:")
    print("    - Background uniforme (var(--color-surface-light))")
    print("    - Border sutil (1px solid rgba(0, 0, 0, 0.08))")
    print("    - Border-radius 8px")
    print("    - Hover effect (translateY + shadow)")
    
    write_file(FILE, html)

def main():
    print("=" * 70)
    print("🔬 UNIFORMIZAR CARDS - FUNDAMENTO JURÍDICO")
    print("=" * 70)
    
    print("\n🎯 Objetivo:")
    print("  • Ajustar cards 2, 3 e 4 para ficarem iguais ao card 1")
    print("  • Aplicar background, borda e estilo uniformes")
    print("  • Manter layout 1 por linha")
    
    update_cards_css()
    
    print("\n" + "=" * 70)
    print("✅ CARDS UNIFORMIZADOS")
    print("=" * 70)
    
    print("\n📊 Estilo aplicado:")
    print("  ✓ Background: var(--color-surface-light)")
    print("  ✓ Border: 1px solid rgba(0, 0, 0, 0.08)")
    print("  ✓ Border-radius: 8px")
    print("  ✓ Padding: 1.5rem 2rem")
    print("  ✓ Hover: translateY(-2px) + shadow")
    
    print("\n⚠️  Validar:")
    print("  • Todos os 4 cards com mesmo fundo cinza claro")
    print("  • Mesma borda sutil")
    print("  • Mesmo arredondamento")
    print("  • Hover suave em todos")

if __name__ == "__main__":
    main()
