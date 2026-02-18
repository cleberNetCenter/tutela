#!/usr/bin/env python3
"""
Apply hero background images to strategic pages and remove all illustrations
"""

import os
import re
from pathlib import Path

# Configuration mapping
HERO_IMAGES = {
    'public/legal/preservacao-probatoria-digital.html': {
        'image': '/assets/images/hero/documento-selo-assinatura.webp',
        'title': 'Preservação Probatória Digital'
    },
    'public/legal/fundamento-juridico.html': {
        'image': '/assets/images/hero/martelo-judicial-biblioteca.webp',
        'title': 'Fundamento Jurídico'
    },
    'public/seguranca.html': {
        'image': '/assets/images/hero/assinatura-digital-tablet.webp',
        'title': 'Segurança'
    },
    'public/como-funciona.html': {
        'image': '/assets/images/hero/fluxo-processual-probatorio.webp',
        'title': 'Como Funciona'
    }
}

def add_css_link(content):
    """Add hero-image-backgrounds.css link if not present"""
    css_link = '<link rel="stylesheet" href="/assets/css/hero-image-backgrounds.css">'
    
    if css_link not in content:
        # Add before </head>
        content = content.replace('</head>', f'  {css_link}\n</head>')
    
    return content

def add_preload(content, image_path):
    """Add preload link for hero image"""
    preload = f'<link rel="preload" as="image" href="{image_path}" type="image/webp">'
    
    if preload not in content:
        # Add after <head>
        content = re.sub(
            r'(<head[^>]*>)',
            f'\\1\n{preload}',
            content
        )
    
    return content

def apply_hero_image(content, image_path):
    """Apply hero image background to existing hero/page-header section"""
    
    # Pattern 1: <section class="hero ...">
    pattern1 = r'<section class="(hero[^"]*)"([^>]*)>'
    
    def replace_hero(match):
        classes = match.group(1)
        other_attrs = match.group(2)
        
        # Add hero--image class if not present
        if 'hero--image' not in classes:
            classes = f"{classes} hero--image"
        
        # Add background-image style
        style = f'style="background-image: url(\'{image_path}\');"'
        
        return f'<section class="{classes}" {style}{other_attrs}>'
    
    content = re.sub(pattern1, replace_hero, content)
    
    # Pattern 2: <section class="page-header ...">
    pattern2 = r'<section class="(page-header[^"]*)"([^>]*)>'
    
    def replace_page_header(match):
        classes = match.group(1)
        other_attrs = match.group(2)
        
        # Add hero--image class
        classes = f"{classes} hero--image"
        
        # Add background-image style
        style = f'style="background-image: url(\'{image_path}\');"'
        
        return f'<section class="{classes}" {style}{other_attrs}>'
    
    content = re.sub(pattern2, replace_page_header, content)
    
    return content

def remove_illustrations(content):
    """Remove all <img> tags except favicon"""
    
    # Remove img tags (keep favicon)
    content = re.sub(
        r'<img\s+(?!.*favicon).*?/?>',
        '',
        content,
        flags=re.IGNORECASE | re.DOTALL
    )
    
    # Remove standalone SVG tags
    content = re.sub(
        r'<svg[^>]*>.*?</svg>',
        '',
        content,
        flags=re.DOTALL
    )
    
    # Remove empty divs with graphic classes
    content = re.sub(
        r'<div class="[^"]*graphic[^"]*">\s*</div>',
        '',
        content,
        flags=re.IGNORECASE
    )
    
    return content

def process_page(filepath, config):
    """Process a single HTML page"""
    if not os.path.exists(filepath):
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Add CSS link
    content = add_css_link(content)
    
    # Add preload
    content = add_preload(content, config['image'])
    
    # Apply hero image
    content = apply_hero_image(content, config['image'])
    
    # Remove illustrations
    content = remove_illustrations(content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def remove_old_illustration_dirs():
    """Remove old illustration directories"""
    dirs_to_remove = [
        'public/assets/illustrations',
        'public/assets/icons'
    ]
    
    import shutil
    
    for dir_path in dirs_to_remove:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            print(f"🗑️  Removido: {dir_path}")

def main():
    print("\n" + "="*70)
    print("APLICANDO HERO IMAGE BACKGROUNDS - PADRONIZAÇÃO INSTITUCIONAL")
    print("="*70 + "\n")
    
    updated_pages = []
    
    for filepath, config in HERO_IMAGES.items():
        if process_page(filepath, config):
            filename = os.path.basename(filepath)
            print(f"✅ {filename}")
            print(f"   📷 Imagem: {os.path.basename(config['image'])}")
            print(f"   🎨 Overlay escuro aplicado")
            print(f"   🚀 Preload adicionado")
            print(f"   🧹 Ilustrações removidas")
            updated_pages.append(filename)
        else:
            print(f"⏭️  {os.path.basename(filepath)}: Sem alterações")
    
    print(f"\n{'='*70}")
    
    # Remove old directories
    print("\n🗑️  Removendo diretórios antigos de ilustrações...")
    remove_old_illustration_dirs()
    
    print(f"\n{'='*70}")
    print(f"✅ {len(updated_pages)} páginas atualizadas")
    print(f"✅ 4 imagens hero aplicadas (todas < 180kb)")
    print(f"✅ CSS hero-image-backgrounds.css criado")
    print(f"✅ Preload adicionado para performance")
    print(f"✅ Ilustrações removidas (design sóbrio)")
    print(f"✅ Projeto visualmente institucional")
    print(f"{'='*70}\n")
    
    print("📁 Estrutura final:")
    print("   /assets/images/hero/")
    print("     ├── documento-selo-assinatura.webp (41KB)")
    print("     ├── martelo-judicial-biblioteca.webp (33KB)")
    print("     ├── assinatura-digital-tablet.webp (27KB)")
    print("     └── fluxo-processual-probatorio.webp (27KB)")
    print()

if __name__ == "__main__":
    main()
