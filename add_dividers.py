#!/usr/bin/env python3
import re

PAGES = [
    "public/legal/preservacao-probatoria-digital.html",
    "public/legal/fundamento-juridico.html",
    "public/legal/termos-de-custodia.html",
    "public/legal/politica-de-privacidade.html",
    "public/legal/institucional.html"
]

for page in PAGES:
    with open(page, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Adicionar divider após h1 se não existir
    if '<div class="legal-divider"></div>' not in html:
        html = re.sub(
            r'(<h1[^>]*>.*?</h1>)',
            r'\1\n    <div class="legal-divider"></div>',
            html
        )
        print(f"✓ Divider adicionado: {page}")
    else:
        print(f"→ Divider já existe: {page}")
    
    with open(page, 'w', encoding='utf-8') as f:
        f.write(html)

print("✅ Dividers verificados")
