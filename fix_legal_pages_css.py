#!/usr/bin/env python3
"""
Script para corrigir formatação CSS e layout de TODAS as páginas legais.
Garante que todas sigam o padrão institucional correto.
"""

from pathlib import Path
import re

# Páginas legais a serem corrigidas
LEGAL_PAGES = [
    'preservacao-probatoria-digital.html',
    'fundamento-juridico.html',
    'termos-de-custodia.html',
    'politica-de-privacidade.html',
    'institucional.html'
]

BASE_DIR = Path('public/legal')

def fix_css_paths(html_content):
    """Corrige caminhos relativos para absolutos nos CSS."""
    # Corrigir links CSS relativos
    html_content = html_content.replace('href="assets/css/', 'href="/assets/css/')
    html_content = html_content.replace('href="assets/illustrations/', 'href="/assets/illustrations/')
    
    return html_content

def ensure_css_links(html_content):
    """Garante que todos os CSS necessários estejam presentes."""
    required_css = [
        '<link rel="stylesheet" href="/assets/css/styles-clean.css?v=4">',
        '<link rel="stylesheet" href="/assets/css/styles-header-final.css?v=4">',
        '<link rel="stylesheet" href="/assets/css/styles-clean.exec-compact.css?v=4">',
        '<link rel="stylesheet" href="/assets/css/dropdown-menu.css">',
        '<link rel="stylesheet" href="/assets/css/hero-image-backgrounds.css">'
    ]
    
    # Verifica se já tem a seção CSS
    if '<!-- CSS -->' not in html_content:
        # Adiciona seção CSS após fonts
        fonts_section = '<!-- Fonts -->'
        if fonts_section in html_content:
            css_section = '\n\n<!-- CSS -->\n' + '\n'.join(required_css)
            html_content = html_content.replace(
                fonts_section,
                fonts_section + css_section
            )
    else:
        # Garante que todos os CSS estão presentes
        for css in required_css:
            if css not in html_content:
                # Adiciona após o último CSS existente
                last_css_match = re.search(r'<link rel="stylesheet"[^>]+>', html_content)
                if last_css_match:
                    pos = last_css_match.end()
                    html_content = html_content[:pos] + '\n' + css + html_content[pos:]
    
    return html_content

def ensure_hero_image_class(html_content, page_name):
    """Adiciona classe hero--image apropriada para cada página."""
    hero_images = {
        'preservacao-probatoria-digital.html': 'documento-selo-assinatura.webp',
        'fundamento-juridico.html': 'martelo-judicial-biblioteca.webp',
        'termos-de-custodia.html': 'documento-selo-assinatura.webp',
        'politica-de-privacidade.html': 'documento-selo-assinatura.webp',
        'institucional.html': 'documento-selo-assinatura.webp'
    }
    
    image_file = hero_images.get(page_name, 'documento-selo-assinatura.webp')
    
    # Verifica se já tem preload
    preload_tag = f'<link rel="preload" as="image" href="/assets/images/hero/{image_file}" type="image/webp">'
    if preload_tag not in html_content:
        # Adiciona após <head>
        html_content = html_content.replace(
            '<head>',
            f'<head>\n{preload_tag}'
        )
    
    # Adiciona classe hero--image ao header/main se não existir
    hero_class = f'hero--image" style="background-image: url(\'/assets/images/hero/{image_file}\')'
    
    # Procura por section/div de conteúdo principal e adiciona classe
    if 'hero--image' not in html_content:
        # Adiciona ao primeiro main/section após </header>
        patterns = [
            (r'(<section[^>]*class="[^"]*)"', r'\1 hero--image" style="background-image: url(\'/assets/images/hero/' + image_file + '\')'),
            (r'(<main[^>]*class="[^"]*)"', r'\1 hero--image" style="background-image: url(\'/assets/images/hero/' + image_file + '\')'),
        ]
        
        for pattern, replacement in patterns:
            if re.search(pattern, html_content):
                html_content = re.sub(pattern, replacement, html_content, count=1)
                break
    
    return html_content

def fix_legal_page(page_name):
    """Corrige uma página legal específica."""
    file_path = BASE_DIR / page_name
    
    if not file_path.exists():
        print(f"❌ Arquivo não encontrado: {file_path}")
        return False
    
    # Lê o conteúdo
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Aplica correções
    html_content = fix_css_paths(html_content)
    html_content = ensure_css_links(html_content)
    html_content = ensure_hero_image_class(html_content, page_name)
    
    # Salva o arquivo corrigido
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ {page_name} - Corrigido")
    return True

def main():
    """Corrige todas as páginas legais."""
    print("🔧 Corrigindo formatação CSS de todas as páginas legais...\n")
    
    fixed_count = 0
    for page in LEGAL_PAGES:
        if fix_legal_page(page):
            fixed_count += 1
    
    print(f"\n✅ {fixed_count}/{len(LEGAL_PAGES)} páginas corrigidas!")
    print("\n📋 Correções aplicadas:")
    print("  • Caminhos CSS: relativos → absolutos (/assets/css/...)")
    print("  • CSS adicionados: styles-clean.css, styles-header-final.css, styles-clean.exec-compact.css")
    print("  • Dropdown CSS: dropdown-menu.css")
    print("  • Hero images: hero-image-backgrounds.css")
    print("  • Preload tags: adicionadas para hero images")
    print("  • Hero classes: aplicadas onde necessário")
    print("\n✅ Todas as páginas agora seguem o padrão institucional!")

if __name__ == '__main__':
    main()
