#!/usr/bin/env python3
"""
Adiciona breadcrumb + Schema BreadcrumbList nas páginas legais
"""

import re
from pathlib import Path

PUBLIC_DIR = Path('public')
LEGAL_DIR = PUBLIC_DIR / 'legal'

print("\n" + "="*60)
print("ADICIONANDO BREADCRUMB EM PÁGINAS LEGAIS")
print("="*60)

# Mapeamento de páginas para títulos
paginas_legais = {
    'institucional.html': 'Institucional',
    'fundamento-juridico.html': 'Fundamento Jurídico',
    'termos-de-custodia.html': 'Termos de Custódia',
    'politica-de-privacidade.html': 'Política de Privacidade',
    'preservacao-probatoria-digital.html': 'Preservação Probatória Digital'
}

def criar_breadcrumb_html(titulo_pagina):
    """Cria HTML do breadcrumb + Schema"""
    return f'''
    <!-- Breadcrumb -->
    <nav class="breadcrumb" aria-label="Breadcrumb">
        <ol>
            <li><a href="/">Início</a></li>
            <li><a href="/legal/institucional.html">Base Jurídica</a></li>
            <li aria-current="page">{titulo_pagina}</li>
        </ol>
    </nav>
    
    <!-- Schema.org BreadcrumbList -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{
          "@type": "ListItem",
          "position": 1,
          "name": "Início",
          "item": "https://tuteladigital.com.br/"
        }},
        {{
          "@type": "ListItem",
          "position": 2,
          "name": "Base Jurídica",
          "item": "https://tuteladigital.com.br/legal/institucional.html"
        }},
        {{
          "@type": "ListItem",
          "position": 3,
          "name": "{titulo_pagina}",
          "item": "https://tuteladigital.com.br/legal/{Path(titulo_pagina).stem}.html"
        }}
      ]
    }}
    </script>
    '''

def adicionar_breadcrumb(filepath, titulo):
    """Adiciona breadcrumb logo após o <header>"""
    if not filepath.exists():
        print(f"⚠️  Não existe: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    breadcrumb_html = criar_breadcrumb_html(titulo)
    
    # Adicionar breadcrumb após </header>
    if '</header>' in content and '<nav class="breadcrumb"' not in content:
        content = content.replace('</header>', f'</header>\n{breadcrumb_html}\n')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {filepath.name}: Breadcrumb adicionado")
        return True
    elif '<nav class="breadcrumb"' in content:
        print(f"⏭️  {filepath.name}: Breadcrumb já existe")
        return False
    else:
        print(f"⚠️  {filepath.name}: Sem </header>")
        return False

# Adicionar breadcrumb CSS simples no início
breadcrumb_css = '''
<style>
.breadcrumb {
    padding: 1rem 2rem;
    background: #f5f5f5;
    font-size: 0.9rem;
}
.breadcrumb ol {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    gap: 0.5rem;
}
.breadcrumb li {
    display: flex;
    align-items: center;
}
.breadcrumb li:not(:last-child)::after {
    content: "›";
    margin-left: 0.5rem;
    color: #666;
}
.breadcrumb a {
    color: #2c5aa0;
    text-decoration: none;
}
.breadcrumb a:hover {
    text-decoration: underline;
}
.breadcrumb li[aria-current="page"] {
    color: #666;
    font-weight: 500;
}
</style>
'''

# Processar páginas
print("\nAdicionando breadcrumbs...")
count = 0
for filename, titulo in paginas_legais.items():
    filepath = LEGAL_DIR / filename
    if adicionar_breadcrumb(filepath, titulo):
        count += 1

# Adicionar CSS
print("\nAdicionando CSS do breadcrumb...")
for filename in paginas_legais.keys():
    filepath = LEGAL_DIR / filename
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if '<style>' not in content or '.breadcrumb' not in content:
            # Adicionar CSS antes de </head>
            content = content.replace('</head>', f'{breadcrumb_css}\n</head>')
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ {filename}: CSS adicionado")

print(f"\n✅ {count} breadcrumbs adicionados")
print("✅ Schema BreadcrumbList implementado")
print("="*60)
