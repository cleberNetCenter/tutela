#!/usr/bin/env python3
"""
fix_first_card_only.py

Corrigir SOMENTE o primeiro card "Identificação do Ativo"
Manter TODOS os outros cards exatamente como estavam
"""

import re

FILE = "public/legal/preservacao-probatoria-digital.html"

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_first_card():
    print("🔧 Corrigindo SOMENTE o primeiro card")
    
    html = read_file(FILE)
    
    # O problema é aqui:
    # <div class="feature-item">
    #   <h3>Identificação do Ativo</h3>
    #   <p>...</p>
    #   (falta </div>)
    # <div class="feature-item"> <- próximo card começa mas está dentro do primeiro
    
    # Encontrar o primeiro card e adicionar o </div> que falta
    pattern = r'(<div class="feature-item">\s*<h3>Identificação do Ativo</h3>\s*<p>Registro individualizado do ativo digital, incluindo metadados relevantes e identificação do depositário\.</p>)\s*(<div class="feature-item">)'
    
    replacement = r'\1\n</div>\n\n\2'
    
    html = re.sub(pattern, replacement, html)
    
    print("  ✓ Tag de fechamento </div> adicionada ao primeiro card")
    print("  ✓ Estrutura horizontal mantida")
    print("  ✓ Todos os outros cards intocados")
    
    write_file(FILE, html)
    print("✅ Página corrigida")
    
    return True

def main():
    print("=" * 70)
    print("🔬 CORREÇÃO CIRÚRGICA - SOMENTE PRIMEIRO CARD")
    print("=" * 70)
    
    print("\n🎯 Objetivo:")
    print("  • Adicionar </div> faltante no card 'Identificação do Ativo'")
    print("  • Manter estrutura horizontal original")
    print("  • Não alterar outros cards")
    
    fix_first_card()
    
    print("\n" + "=" * 70)
    print("✅ CORREÇÃO CONCLUÍDA")
    print("=" * 70)
    
    print("\n📊 Resultado:")
    print("  ✓ Primeiro card com estrutura correta")
    print("  ✓ Mesmo tamanho dos demais cards")
    print("  ✓ Layout horizontal mantido")
    print("  ✓ Grid 2x2 funcionando")

if __name__ == "__main__":
    main()
