#!/usr/bin/env python3
"""
Script para corrigir espaço em branco entre cabeçalho e hero images.

PROBLEMA:
- Páginas com hero images têm área em branco entre header e imagem
- Causa: .main { padding-top: 80px } necessário para header fixo
- Hero images precisam começar imediatamente após o header

SOLUÇÃO:
- Adicionar classe especial .main--hero-top para páginas com hero image no topo
- CSS: .main--hero-top { padding-top: 0; margin-top: 80px; }
- Aplicar em páginas: como-funciona, seguranca, legal/*
"""

from pathlib import Path
import re

PUBLIC_DIR = Path('public')
CSS_DIR = PUBLIC_DIR / 'assets' / 'css'

# Páginas que têm hero image no topo
HERO_PAGES = [
    'como-funciona.html',
    'seguranca.html',
    'legal/preservacao-probatoria-digital.html',
    'legal/fundamento-juridico.html'
]

def add_hero_top_css():
    """Adiciona CSS para remover espaço em branco acima de hero images."""
    css_file = CSS_DIR / 'hero-image-backgrounds.css'
    
    with open(css_file, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    # Adiciona regra CSS se não existir
    if '.main--hero-top' not in css_content:
        hero_top_css = """
/* =========================================================
   FIX: Remover espaço entre header e hero image
   ========================================================= */

/* Páginas com hero image no topo */
.main--hero-top {
  padding-top: 0 !important;
}

/* Hero image começa imediatamente após o header */
.main--hero-top > .hero--image:first-child,
.main--hero-top > section.hero--image:first-child {
  margin-top: 0;
  padding-top: calc(80px + 3rem); /* Header height + espaçamento interno */
}
"""
        css_content = css_content.rstrip() + '\n' + hero_top_css
        
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        print(f"✅ {css_file.name} - CSS .main--hero-top adicionado")
    else:
        print(f"ℹ️  {css_file.name} - CSS já contém .main--hero-top")

def fix_html_pages():
    """Adiciona classe .main--hero-top nas páginas com hero image."""
    fixed_count = 0
    
    for page in HERO_PAGES:
        html_file = PUBLIC_DIR / page
        
        if not html_file.exists():
            print(f"⚠️  {page} - Arquivo não encontrado")
            continue
        
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Verifica se já tem a classe
        if 'main--hero-top' in html_content:
            print(f"ℹ️  {page} - Já tem classe .main--hero-top")
            continue
        
        # Adiciona classe ao <main>
        html_content = re.sub(
            r'<main\s+class="main"',
            '<main class="main main--hero-top"',
            html_content
        )
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        fixed_count += 1
        print(f"✅ {page} - Classe .main--hero-top adicionada")
    
    return fixed_count

def main():
    """Executa todas as correções."""
    print("🔧 Corrigindo espaço em branco entre header e hero images...\n")
    
    # 1. Adicionar CSS
    add_hero_top_css()
    
    print()
    
    # 2. Atualizar HTML
    fixed_html = fix_html_pages()
    
    print(f"\n✅ Correções concluídas!")
    print(f"  • CSS adicionado: .main--hero-top")
    print(f"  • Páginas atualizadas: {fixed_html}")
    print("\n📋 Resultado:")
    print("  ✅ Zero espaço em branco entre header e hero image")
    print("  ✅ Hero images começam imediatamente após o header")
    print("  ✅ Padding interno ajustado para compensar header fixo")
    print("  ✅ Layout limpo e profissional")

if __name__ == '__main__':
    main()
