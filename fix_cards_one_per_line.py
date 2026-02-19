#!/usr/bin/env python3
"""
fix_cards_one_per_line.py

Alterar layout dos cards para:
- 1 card por linha (grid-template-columns: 1fr)
- Largura total horizontal
- Altura reduzida (min-height: 100px)
"""

import re

FILE = "public/legal/preservacao-probatoria-digital.html"

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_css():
    print("🔧 Ajustando CSS dos cards para 1 por linha")
    
    html = read_file(FILE)
    
    # CSS atual que precisa ser alterado
    old_css = """/* Garantir que todos os cards tenham altura mínima consistente */
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
</style>"""
    
    # Novo CSS: 1 card por linha, largura total, altura reduzida
    new_css = """/* Cards: 1 por linha, largura total, altura reduzida */
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
</style>"""
    
    html = html.replace(old_css, new_css)
    
    print("  ✓ Grid alterado para 1 coluna (1fr)")
    print("  ✓ Gap reduzido para 1.5rem")
    print("  ✓ Min-height alterado para 100px")
    print("  ✓ Padding ajustado para 1.5rem 2rem")
    
    write_file(FILE, html)
    print("✅ CSS atualizado")
    
    return True

def main():
    print("=" * 70)
    print("🔬 AJUSTE DE LAYOUT - 1 CARD POR LINHA")
    print("=" * 70)
    
    print("\n🎯 Objetivo:")
    print("  • 1 card por linha (largura total horizontal)")
    print("  • Altura reduzida pela metade (min-height: 100px)")
    print("  • Manter todos os 6 cards visíveis")
    
    fix_css()
    
    print("\n" + "=" * 70)
    print("✅ AJUSTE CONCLUÍDO")
    print("=" * 70)
    
    print("\n📊 Resultado esperado:")
    print("  ┌─────────────────────────────────────┐")
    print("  │ Card 1: Identificação do Ativo      │")
    print("  ├─────────────────────────────────────┤")
    print("  │ Card 2: Geração de Hash...          │")
    print("  ├─────────────────────────────────────┤")
    print("  │ Card 3: Assinatura Digital          │")
    print("  ├─────────────────────────────────────┤")
    print("  │ Card 4: Registro Temporal Imutável  │")
    print("  ├─────────────────────────────────────┤")
    print("  │ Card 5: Auditoria e Rastreabilidade │")
    print("  ├─────────────────────────────────────┤")
    print("  │ Card 6: Interoperabilidade Notarial │")
    print("  └─────────────────────────────────────┘")
    
    print("\n⚠️  Validar:")
    print("  • Cada card ocupa toda a largura")
    print("  • Altura reduzida (≈100px de min-height)")
    print("  • Layout vertical limpo")

if __name__ == "__main__":
    main()
