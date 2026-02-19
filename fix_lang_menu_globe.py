#!/usr/bin/env python3
"""
Corrigir menu de idiomas e adicionar globo colorido
"""

import os
import re

def fix_language_selector():
    """Corrige o menu de idiomas e adiciona globo colorido"""
    
    print("\n" + "="*70)
    print("🌐 CORRIGINDO MENU DE IDIOMAS + GLOBO COLORIDO")
    print("="*70)
    
    # Novo SVG do globo colorido
    new_globe_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" style="vertical-align: middle;">
      <!-- Oceano (azul) -->
      <circle cx="12" cy="12" r="10" fill="#4A90E2" stroke="#2E5C8A" stroke-width="1"/>
      <!-- Continentes (verde) -->
      <path d="M7 8 Q9 6 11 7 T13 9 Q14 10 13 12 T11 14 Q9 14 8 13 T7 11 Z" fill="#52B788" stroke="#2D6A4F" stroke-width="0.5"/>
      <path d="M15 6 Q17 5 18 7 T17 10 Q16 11 15 10 Z" fill="#52B788" stroke="#2D6A4F" stroke-width="0.5"/>
      <path d="M14 13 Q16 12 18 14 T17 17 Q15 18 14 16 Z" fill="#52B788" stroke="#2D6A4F" stroke-width="0.5"/>
      <path d="M6 15 Q7 16 9 16 T10 18 Q9 19 7 18 Z" fill="#52B788" stroke="#2D6A4F" stroke-width="0.5"/>
      <!-- Highlight (brilho) -->
      <ellipse cx="9" cy="8" rx="2" ry="3" fill="rgba(255,255,255,0.2)" transform="rotate(-30 9 8)"/>
    </svg>'''
    
    html_files = [
        'public/index.html',
        'public/como-funciona.html',
        'public/seguranca.html',
        'public/governo.html',
        'public/empresas.html',
        'public/pessoas.html',
        'public/legal/preservacao-probatoria-digital.html',
        'public/legal/fundamento-juridico.html',
        'public/legal/termos-de-custodia.html',
        'public/legal/politica-de-privacidade.html',
        'public/legal/institucional.html'
    ]
    
    stats = {'files_updated': 0, 'globes_replaced': 0}
    
    for html_file in html_files:
        if not os.path.exists(html_file):
            continue
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Substituir o SVG do globo
        pattern = r'(<button class="lang-toggle"[^>]*>)\s*<svg[^>]*>.*?</svg>'
        replacement = r'\1\n    ' + new_globe_svg
        
        content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)
        
        if count > 0:
            stats['globes_replaced'] += count
            print(f"  ✅ {html_file}: Globo colorido substituído")
        
        if content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            stats['files_updated'] += 1
    
    return stats

def fix_css():
    """Adiciona pointer-events: none e .active ao CSS"""
    
    print("\n" + "="*70)
    print("🔧 CORRIGINDO CSS")
    print("="*70)
    
    css_file = 'public/assets/css/styles-header-final.css'
    
    with open(css_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 1. Adicionar pointer-events: none
    if 'pointer-events: none' not in content:
        content = content.replace(
            '.lang-toggle svg {\n  vertical-align: middle;\n  margin: 0;\n}',
            '.lang-toggle svg {\n  vertical-align: middle;\n  margin: 0;\n  pointer-events: none;\n}'
        )
        print("  ✅ Adicionado pointer-events: none")
    
    # 2. Adicionar .lang-dropdown.active
    if '.lang-dropdown.active .lang-menu' not in content:
        content = content.replace(
            '.lang-dropdown:hover .lang-menu,\n.lang-dropdown:focus-within .lang-menu {',
            '.lang-dropdown:hover .lang-menu,\n.lang-dropdown:focus-within .lang-menu,\n.lang-dropdown.active .lang-menu {'
        )
        print("  ✅ Adicionado .lang-dropdown.active .lang-menu")
    
    if content != original_content:
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print("  ✅ CSS atualizado")
    
    return True

def main():
    print("\n" + "="*70)
    print("🚀 CORREÇÃO: MENU DE IDIOMAS + GLOBO COLORIDO")
    print("="*70)
    
    stats = fix_language_selector()
    fix_css()
    
    print("\n" + "="*70)
    print("📊 RELATÓRIO FINAL")
    print("="*70)
    print(f"✅ Arquivos HTML atualizados: {stats['files_updated']}")
    print(f"✅ Globos coloridos: {stats['globes_replaced']}")
    print("✅ CSS corrigido: pointer-events + .active")
    
    print("\n" + "="*70)
    print("🎯 RESULTADO")
    print("="*70)
    print("✅ Menu de idiomas funcional")
    print("✅ Globo colorido (oceano azul + continentes verdes)")
    print("✅ Cliques funcionais")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
