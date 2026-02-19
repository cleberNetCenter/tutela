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
    
    # Encontrar e substituir o hero completo
    hero_pattern = r'<section class="page-header[^"]*"[^>]*>.*?</section>'
    
    def fix_hero(match):
        content = match.group(0)
        
        # Extrair H1
        h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
        h1 = h1_match.group(1).strip() if h1_match else "Título"
        
        # Extrair parágrafo
        p_match = re.search(r'<p[^>]*>(.*?)</p>', content, re.DOTALL)
        p = p_match.group(1).strip() if p_match else ""
        
        # Reconstruir hero limpo
        return f'''<section class="page-header page-header--legal">
  <div class="page-header-inner page-header--legal">
    
    <h1>{h1}</h1>
    <div class="legal-divider"></div>

    <p class="page-header-subtitle">
      {p}
    </p>

  </div>
</section>'''
    
    # Substituir apenas o primeiro hero
    html = re.sub(hero_pattern, fix_hero, html, count=1, flags=re.DOTALL)
    
    # Remover SVG decorativo fora do hero
    html = re.sub(
        r'\n<div class="wp-legal-graphic">.*?</div>',
        '',
        html,
        flags=re.DOTALL
    )
    
    with open(page, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ Hero limpo: {page}")

print("✅ Heroes corrigidos")
