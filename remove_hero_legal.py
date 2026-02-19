#!/usr/bin/env python3
"""
Script direto para remover hero images das 3 páginas legais.
"""

from pathlib import Path
import re

LEGAL_DIR = Path('public/legal')

PAGES = {
    'institucional.html': 'institucional',
    'termos-de-custodia.html': 'termos-custodia', 
    'politica-de-privacidade.html': 'politica-privacidade'
}

for filename, page_class in PAGES.items():
    filepath = LEGAL_DIR / filename
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Encontrar e substituir o page-header
    pattern = r'<section class="page-header[^>]*hero--image"[^>]*>'
    
    replacement = f'<section class="page-header page-header--{page_class}">'
    
    content = re.sub(pattern, replacement, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {filename} - hero--image removido, usando page-header--{page_class}")

print("\n✅ Todas as 3 páginas corrigidas!")
