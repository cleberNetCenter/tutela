#!/usr/bin/env python3
"""
Script para padronizar páginas legais SEM hero image seguindo estrutura da página governo.

PÁGINAS LEGAIS:
- preservacao-probatoria-digital.html (TEM hero image) ✅
- fundamento-juridico.html (TEM hero image) ✅
- termos-de-custodia.html (REMOVER hero image, usar padrão governo)
- politica-de-privacidade.html (REMOVER hero image, usar padrão governo)
- institucional.html (REMOVER hero image, usar padrão governo)

PADRÃO GOVERNO (sem hero image):
- CSS: assets/css/ (relativo) com ?v=4
- Body: <body class="exec-compact"> (sem <div class="app">)
- Main: <main class="main"> (sem main--hero-top)
- Page header: <section class="page-header page-header--{page}">
- Sem preload de hero image
- Sem hero--image class
"""

from pathlib import Path
import re

PUBLIC_DIR = Path('public')
LEGAL_DIR = PUBLIC_DIR / 'legal'

# Páginas que NÃO devem ter hero image (usar padrão governo)
PAGES_WITHOUT_HERO = [
    'termos-de-custodia.html',
    'politica-de-privacidade.html',
    'institucional.html'
]

def remove_hero_image_elements(html_content, page_name):
    """Remove elementos relacionados a hero images."""
    
    # 1. Remover preload de hero image
    html_content = re.sub(
        r'<link rel="preload" as="image" href="/assets/images/hero/[^"]+\.webp" type="image/webp">\n?',
        '',
        html_content
    )
    
    # 2. Remover classe hero--image do page-header
    html_content = re.sub(
        r'(<section class="page-header[^"]*)\s+hero--image"([^>]*style="background-image:[^"]+")?>',
        r'\1"\2>',
        html_content
    )
    
    # Remover style de background-image
    html_content = re.sub(
        r'<section class="page-header[^"]*"\s+style="background-image:[^"]+">',
        lambda m: m.group(0).split(' style=')[0] + '>',
        html_content
    )
    
    # 3. Remover classe main--hero-top
    html_content = re.sub(
        r'<main class="main main--hero-top">',
        '<main class="main">',
        html_content
    )
    
    # 4. Remover <div class="app"> wrapper
    html_content = re.sub(
        r'<body class="exec-compact">\s*<div class="app">\s*',
        '<body class="exec-compact">\n',
        html_content
    )
    
    # Remover fechamento de </div> antes de </body>
    html_content = re.sub(
        r'</div>\s*</body>',
        '</body>',
        html_content
    )
    
    return html_content

def fix_css_paths_to_relative(html_content):
    """Converte CSS paths de absoluto para relativo (padrão governo)."""
    
    # /assets/css/ → assets/css/ (relativo)
    html_content = html_content.replace('href="/assets/css/', 'href="assets/css/')
    
    # Adicionar ?v=4 se não existir
    html_content = re.sub(
        r'href="assets/css/(styles-clean\.css|styles-header-final\.css|styles-clean\.exec-compact\.css)"',
        r'href="assets/css/\1?v=4"',
        html_content
    )
    
    return html_content

def ensure_governo_structure(html_content, page_name):
    """Garante estrutura idêntica à página governo."""
    
    # Adicionar página-specific class no page-header
    page_class = page_name.replace('.html', '').replace('-', '_')
    
    html_content = re.sub(
        r'<section class="page-header">',
        f'<section class="page-header page-header--{page_class}">',
        html_content
    )
    
    return html_content

def fix_legal_page(page_name):
    """Corrige uma página legal para seguir padrão governo."""
    file_path = LEGAL_DIR / page_name
    
    if not file_path.exists():
        print(f"❌ {page_name} não encontrado")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Aplica correções
    html_content = remove_hero_image_elements(html_content, page_name)
    html_content = fix_css_paths_to_relative(html_content)
    html_content = ensure_governo_structure(html_content, page_name)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ {page_name} - Ajustado para padrão governo (sem hero image)")
    return True

def main():
    """Executa correções em todas as páginas legais sem hero image."""
    print("🔧 Ajustando páginas legais para padrão governo (sem hero image)...\n")
    
    fixed_count = 0
    for page in PAGES_WITHOUT_HERO:
        if fix_legal_page(page):
            fixed_count += 1
    
    print(f"\n✅ {fixed_count}/{len(PAGES_WITHOUT_HERO)} páginas ajustadas!")
    print("\n📋 Alterações aplicadas:")
    print("  • Hero image preload: REMOVIDO")
    print("  • Classe hero--image: REMOVIDA")
    print("  • Background-image style: REMOVIDO")
    print("  • Classe main--hero-top: REMOVIDA")
    print("  • Wrapper <div class='app'>: REMOVIDO")
    print("  • CSS paths: absolutos → relativos (assets/css/...?v=4)")
    print("  • Estrutura: idêntica à página governo")
    print("\n✅ Páginas legais agora seguem padrão consistente!")
    print(f"\nCOM hero image (2): preservacao-probatoria-digital.html, fundamento-juridico.html")
    print(f"SEM hero image (3): {', '.join(PAGES_WITHOUT_HERO)}")

if __name__ == '__main__':
    main()
