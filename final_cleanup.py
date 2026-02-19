#!/usr/bin/env python3
import re
from pathlib import Path

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
    
    # Remover divs vazias consecutivas
    html = re.sub(r'(<div[^>]*>\s*</div>\s*)+', '', html)
    
    # Limpar múltiplas linhas vazias
    html = re.sub(r'\n\s*\n\s*\n+', '\n\n', html)
    
    with open(page, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ Limpo: {page}")

print("✅ Limpeza final concluída")
