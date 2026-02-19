#!/usr/bin/env python3
"""
refine_legal_pages.py

Refinamento final:
- Remover completamente gráficos decorativos (fundamento-point, etc.)
- Garantir hero limpo e centralizado
- Manter apenas H1 + divider + parágrafo
"""

import re
from pathlib import Path

LEGAL_PAGES = [
    "public/legal/preservacao-probatoria-digital.html",
    "public/legal/fundamento-juridico.html",
    "public/legal/termos-de-custodia.html",
    "public/legal/politica-de-privacidade.html",
    "public/legal/institucional.html"
]

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def clean_hero_graphics(html):
    """
    Remover todos os gráficos decorativos do hero
    - fundamento-point
    - fundamento-graphic
    - Manter apenas h1, divider, p
    """
    # Remover blocos fundamento-graphic completos
    html = re.sub(
        r'<div class="fundamento-graphic">.*?</div>\s*</div>\s*</div>',
        '</div>',
        html,
        flags=re.DOTALL
    )
    
    # Remover fundamento-points soltos
    html = re.sub(
        r'<div class="fundamento-point[^"]*">.*?</div>\s*</div>',
        '',
        html,
        flags=re.DOTALL
    )
    
    # Remover SVGs soltos no hero
    html = re.sub(
        r'<svg xmlns="http://www\.w3\.org/2000/svg"[^>]*>.*?</svg>',
        '',
        html,
        flags=re.DOTALL
    )
    
    # Limpar divs vazias extras no hero
    html = re.sub(
        r'<div class="point-[^"]*">.*?</div>',
        '',
        html,
        flags=re.DOTALL
    )
    
    return html

def clean_whitespace_in_hero(html):
    """
    Limpar espaços em branco excessivos no hero
    """
    # Dentro de page-header--legal, limpar múltiplas linhas vazias
    pattern = r'(<div class="page-header--legal">)(.*?)(</div>)'
    
    def clean_content(match):
        opening = match.group(1)
        content = match.group(2)
        closing = match.group(3)
        
        # Remover múltiplas linhas vazias
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        
        return opening + content + closing
    
    html = re.sub(pattern, clean_content, html, flags=re.DOTALL)
    
    return html

def process_page(file_path):
    """Processar uma página"""
    print(f"\n🔧 Refinando: {file_path}")
    
    html = read_file(file_path)
    
    html = clean_hero_graphics(html)
    print("  ✓ Gráficos decorativos removidos")
    
    html = clean_whitespace_in_hero(html)
    print("  ✓ Espaços em branco limpos")
    
    write_file(file_path, html)
    print("  ✅ Página refinada")

def main():
    print("=" * 70)
    print("🔬 REFINAMENTO FINAL – HERO LIMPO")
    print("=" * 70)
    
    for page in LEGAL_PAGES:
        if Path(page).exists():
            process_page(page)
        else:
            print(f"⚠️  Não encontrado: {page}")
    
    print("\n" + "=" * 70)
    print("✅ REFINAMENTO CONCLUÍDO")
    print("=" * 70)

if __name__ == "__main__":
    main()
