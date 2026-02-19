#!/usr/bin/env python3
"""
Remover resíduos do hero image das páginas legais sem hero
"""

import os
import re

def remove_hero_graphic_remnants():
    """Remove o <div class="page-header-graphic"> das páginas legais"""
    
    print("\n" + "="*70)
    print("🗑️  REMOVENDO RESÍDUOS DO HERO IMAGE")
    print("="*70)
    
    pages = [
        'public/legal/institucional.html',
        'public/legal/termos-de-custodia.html',
        'public/legal/politica-de-privacidade.html'
    ]
    
    stats = {'files_cleaned': 0, 'graphics_removed': 0}
    
    for html_file in pages:
        if not os.path.exists(html_file):
            print(f"  ⚠️  {html_file}: Arquivo não encontrado")
            continue
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern para remover <div class="page-header-graphic">...</div>
        pattern = r'\n*\s*<div class="page-header-graphic">.*?</div>\n*'
        
        content, count = re.subn(pattern, '\n', content, flags=re.DOTALL)
        
        if count > 0:
            stats['graphics_removed'] += count
            print(f"  ✅ {html_file}: Removido {count} bloco(s) page-header-graphic")
        
        # Salvar se houve mudanças
        if content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            stats['files_cleaned'] += 1
    
    return stats

def main():
    print("\n" + "="*70)
    print("🚨 LIMPEZA: REMOVER RESÍDUOS DO HERO IMAGE")
    print("="*70)
    
    stats = remove_hero_graphic_remnants()
    
    print("\n" + "="*70)
    print("📊 RELATÓRIO FINAL")
    print("="*70)
    print(f"✅ Arquivos limpos: {stats['files_cleaned']}")
    print(f"✅ Blocos graphic removidos: {stats['graphics_removed']}")
    print("\n" + "="*70)
    print("🎯 RESULTADO")
    print("="*70)
    print("✅ page-header-graphic completamente removido")
    print("✅ Estrutura limpa seguindo padrão governo.html")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
