#!/usr/bin/env python3
"""
Remove i18n.js dependencies from legal pages (Portuguese only)
"""

import os
import re

LEGAL_DIR = "public/legal"
LEGAL_PAGES = [
    "institucional.html",
    "fundamento-juridico.html",
    "termos-de-custodia.html",
    "politica-de-privacidade.html",
    "preservacao-probatoria-digital.html"
]

def remove_i18n_from_file(filepath):
    """Remove i18n.js script tag from HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Remove i18n.js script tag
    content = re.sub(
        r'<script src="[^"]*i18n\.js"></script>\s*',
        '',
        content,
        flags=re.IGNORECASE
    )
    
    # Remove data-i18n attributes from navigation items (if any remain)
    content = re.sub(
        r'\s+data-i18n="[^"]*"',
        '',
        content
    )
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    print("\n" + "="*60)
    print("REMOVENDO DEPENDÊNCIAS i18n.js DAS PÁGINAS LEGAIS")
    print("="*60 + "\n")
    
    updated = 0
    
    for page in LEGAL_PAGES:
        filepath = os.path.join(LEGAL_DIR, page)
        if os.path.exists(filepath):
            if remove_i18n_from_file(filepath):
                print(f"✅ {page}: i18n.js removido")
                updated += 1
            else:
                print(f"⏭️  {page}: Nenhuma alteração necessária")
        else:
            print(f"❌ {page}: Arquivo não encontrado")
    
    print(f"\n✅ {updated} páginas atualizadas")
    print("✅ Páginas legais agora são 100% Portuguese-only")
    print("✅ Sem dependências JavaScript de tradução")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
