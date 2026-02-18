#!/usr/bin/env python3
"""
Adiciona noindex em /en/ e /es/ + Ajusta hreflang
"""

import re
from pathlib import Path

PUBLIC_DIR = Path('public')
EN_DIR = PUBLIC_DIR / 'en'
ES_DIR = PUBLIC_DIR / 'es'
LEGAL_DIR = PUBLIC_DIR / 'legal'

print("\n" + "="*60)
print("AJUSTANDO NOINDEX E HREFLANG")
print("="*60)

# Função para adicionar noindex
def add_noindex_meta(content):
    """Adiciona noindex, follow"""
    if 'robots' in content and 'noindex' in content:
        return content  # Já tem noindex
    
    # Procurar <meta name="viewport"...> e adicionar noindex depois
    pattern = r'(<meta\s+name="viewport"[^>]*>)'
    noindex_meta = '''
    <meta name="robots" content="noindex,follow">
    <meta name="googlebot" content="noindex,follow">'''
    
    content = re.sub(pattern, rf'\1{noindex_meta}', content)
    return content

# Função para remover/ajustar hreflang
def fix_hreflang(content, page_type='legal'):
    """Remove hreflang inválidos, mantém apenas pt-br + x-default"""
    
    # Remover TODOS os hreflang primeiro
    content = re.sub(r'<link\s+rel="alternate"\s+hreflang="[^"]*"\s+href="[^"]*"\s*/>', '', content, flags=re.MULTILINE)
    
    if page_type == 'legal':
        # Páginas legais: NÃO devem ter hreflang (apenas português)
        return content
    
    if page_type == 'homepage_pt':
        # Homepage PT: apenas pt-br + x-default
        viewport_pattern = r'(</title>)'
        hreflang_pt = '''
    <link rel="alternate" hreflang="pt-br" href="https://tuteladigital.com.br/" />
    <link rel="alternate" hreflang="x-default" href="https://tuteladigital.com.br/" />'''
        
        content = re.sub(viewport_pattern, rf'\1{hreflang_pt}', content)
    
    return content

# Processar páginas /en/
print("\n[1] Adicionando noindex em /en/...")
for html_file in EN_DIR.glob('*.html'):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = add_noindex_meta(content)
    content = fix_hreflang(content, 'en')
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {html_file.name}: noindex adicionado, hreflang removido")

# Processar páginas /es/
print("\n[2] Adicionando noindex em /es/...")
for html_file in ES_DIR.glob('*.html'):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = add_noindex_meta(content)
    content = fix_hreflang(content, 'es')
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {html_file.name}: noindex adicionado, hreflang removido")

# Processar páginas legais
print("\n[3] Ajustando hreflang em páginas legais...")
for html_file in LEGAL_DIR.glob('*.html'):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = fix_hreflang(content, 'legal')
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {html_file.name}: hreflang removido (páginas legais não têm EN/ES)")

# Processar homepage PT
print("\n[4] Ajustando hreflang na homepage PT...")
index_file = PUBLIC_DIR / 'index.html'
if index_file.exists():
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = fix_hreflang(content, 'homepage_pt')
    
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ index.html: hreflang ajustado (apenas pt-br + x-default)")

print("\n✅ NOINDEX E HREFLANG AJUSTADOS")
print("="*60)
