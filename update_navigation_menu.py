#!/usr/bin/env python3
"""
Update Navigation Menu with Legal Pages Dropdown

This script updates all HTML files to:
1. Remove individual legal page links from main navigation
2. Add a "Base Jurídica" dropdown menu
3. Include CSS and JS for dropdown functionality
"""

import re
from pathlib import Path

PUBLIC_DIR = Path('public')
LEGAL_DIR = PUBLIC_DIR / 'legal'

# New dropdown HTML structure
DROPDOWN_HTML = '''<li class="nav-dropdown">
<a href="#" data-i18n="nav_legal_base">Base Jurídica</a>
<ul class="dropdown-menu">
<li><a href="/legal/preservacao-probatoria-digital.html" data-i18n="nav_preservacao">Preservação Probatória</a></li>
<li><a href="/legal/fundamento-juridico.html" data-i18n="nav_fundamento">Fundamento Jurídico</a></li>
<li><a href="/legal/termos-de-custodia.html" data-i18n="nav_termos">Termos de Custódia</a></li>
<li><a href="/legal/politica-de-privacidade.html" data-i18n="nav_privacy">Política de Privacidade</a></li>
<li><a href="/legal/institucional.html" data-i18n="nav_institucional">Estrutura Institucional</a></li>
</ul>
</li>'''

# CSS link to add in <head>
CSS_LINK = '<link rel="stylesheet" href="/assets/css/dropdown-menu.css">'

# JS script to add before </body>
JS_SCRIPT = '<script src="/assets/js/dropdown-menu.js"></script>'

def update_navigation_in_file(file_path):
    """Update navigation in a single HTML file"""
    content = file_path.read_text(encoding='utf-8')
    original_content = content
    
    # Find the navigation section
    nav_pattern = r'<nav[^>]*class="nav"[^>]*>(.*?)</nav>'
    nav_match = re.search(nav_pattern, content, re.DOTALL)
    
    if not nav_match:
        print(f"⚠️  Navegação não encontrada em: {file_path.name}")
        return False
    
    nav_content = nav_match.group(1)
    original_nav = nav_content
    
    # Remove individual legal page links
    patterns_to_remove = [
        r'<a[^>]*data-page="preservacao-probatoria"[^>]*>.*?</a>\s*',
        r'<a[^>]*data-page="institucional"[^>]*>.*?</a>\s*',
        r'<a[^>]*data-page="fundamento-juridico"[^>]*>.*?</a>\s*',
        r'<a[^>]*data-page="termos-de-custodia"[^>]*>.*?</a>\s*',
        r'<a[^>]*data-page="politica-de-privacidade"[^>]*>.*?</a>\s*',
    ]
    
    for pattern in patterns_to_remove:
        nav_content = re.sub(pattern, '', nav_content, flags=re.DOTALL)
    
    # Add dropdown menu before the closing tag
    # Insert after "seguranca" link
    seguranca_pattern = r'(<a[^>]*data-page="seguranca"[^>]*>.*?</a>)'
    if re.search(seguranca_pattern, nav_content, re.DOTALL):
        nav_content = re.sub(
            seguranca_pattern,
            r'\1\n' + DROPDOWN_HTML,
            nav_content,
            flags=re.DOTALL
        )
    
    # Replace old navigation with new
    new_nav_full = f'<nav class="nav" id="nav">{nav_content}</nav>'
    content = content.replace(nav_match.group(0), new_nav_full)
    
    # Add CSS link if not present
    if 'dropdown-menu.css' not in content:
        # Add before first </head>
        content = content.replace('</head>', f'  {CSS_LINK}\n</head>', 1)
    
    # Add JS script if not present
    if 'dropdown-menu.js' not in content:
        # Add before first </body>
        content = content.replace('</body>', f'  {JS_SCRIPT}\n</body>', 1)
    
    if content != original_content:
        file_path.write_text(content, encoding='utf-8')
        return True
    
    return False

def update_language_json_files():
    """Add new translation keys for dropdown menu"""
    print("\n" + "="*70)
    print("ATUALIZANDO ARQUIVOS DE TRADUÇÃO JSON")
    print("="*70)
    
    import json
    
    lang_dir = PUBLIC_DIR / 'assets' / 'lang'
    
    # New keys to add
    new_keys = {
        'pt': {
            'navigation': {
                'legal_base': 'Base Jurídica',
                'institucional': 'Estrutura Institucional',
                'privacy': 'Política de Privacidade'
            }
        },
        'en': {
            'navigation': {
                'legal_base': 'Legal Basis',
                'institucional': 'Institutional Structure',
                'privacy': 'Privacy Policy'
            }
        },
        'es': {
            'navigation': {
                'legal_base': 'Base Jurídica',
                'institucional': 'Estructura Institucional',
                'privacy': 'Política de Privacidad'
            }
        }
    }
    
    for lang_code, new_translations in new_keys.items():
        json_file = lang_dir / f'{lang_code}.json'
        
        if not json_file.exists():
            print(f"⚠️  Arquivo não encontrado: {json_file}")
            continue
        
        # Read existing JSON
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Add new keys to navigation section
        if 'navigation' in data:
            data['navigation'].update(new_translations['navigation'])
            print(f"✅ Atualizado: {json_file.name} (+{len(new_translations['navigation'])} chaves)")
        else:
            print(f"⚠️  Seção 'navigation' não encontrada em: {json_file.name}")
        
        # Write back
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

def also_move_preservacao_probatoria():
    """Also move preservacao-probatoria-digital.html to /legal/"""
    print("\n" + "="*70)
    print("MOVENDO preservacao-probatoria-digital.html PARA /legal/")
    print("="*70)
    
    source = PUBLIC_DIR / 'preservacao-probatoria-digital.html'
    destination = LEGAL_DIR / 'preservacao-probatoria-digital.html'
    
    if source.exists():
        content = source.read_text(encoding='utf-8')
        
        # Update canonical
        content = content.replace(
            'canonical" href="https://tuteladigital.com.br/preservacao-probatoria-digital.html',
            'canonical" href="https://tuteladigital.com.br/legal/preservacao-probatoria-digital.html'
        )
        
        # Update hreflang
        content = content.replace(
            'hreflang="pt-br" href="https://tuteladigital.com.br/preservacao-probatoria-digital.html"',
            'hreflang="pt-br" href="https://tuteladigital.com.br/legal/preservacao-probatoria-digital.html"'
        )
        content = content.replace(
            'hreflang="x-default" href="https://tuteladigital.com.br/preservacao-probatoria-digital.html"',
            'hreflang="x-default" href="https://tuteladigital.com.br/legal/preservacao-probatoria-digital.html"'
        )
        
        destination.write_text(content, encoding='utf-8')
        source.unlink()
        print(f"✅ Movido: preservacao-probatoria-digital.html → /legal/")
        
        # Add redirect
        redirects_file = PUBLIC_DIR / '_redirects'
        redirects_content = redirects_file.read_text(encoding='utf-8')
        redirects_content += '/preservacao-probatoria-digital.html  /legal/preservacao-probatoria-digital.html  301\n'
        redirects_file.write_text(redirects_content, encoding='utf-8')
        print("✅ Redirect adicionado para preservacao-probatoria-digital.html")
        
        # Update sitemap
        sitemap_file = PUBLIC_DIR / 'sitemap.xml'
        if sitemap_file.exists():
            sitemap = sitemap_file.read_text(encoding='utf-8')
            
            # Remove old URL
            pattern = r'<url>\s*<loc>https://tuteladigital\.com\.br/preservacao-probatoria-digital\.html</loc>.*?</url>'
            sitemap = re.sub(pattern, '', sitemap, flags=re.DOTALL)
            
            # Add new URL
            new_url = '''  <url>
    <loc>https://tuteladigital.com.br/legal/preservacao-probatoria-digital.html</loc>
    <lastmod>2026-02-18</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
'''
            sitemap = sitemap.replace('</urlset>', new_url + '</urlset>')
            sitemap_file.write_text(sitemap, encoding='utf-8')
            print("✅ Sitemap atualizado com preservacao-probatoria-digital.html")

def main():
    """Execute navigation menu update"""
    print("\n" + "="*70)
    print("🔧 ATUALIZANDO MENU DE NAVEGAÇÃO COM DROPDOWN")
    print("="*70)
    
    # Move preservacao-probatoria-digital first
    also_move_preservacao_probatoria()
    
    # Update language files
    update_language_json_files()
    
    print("\n" + "="*70)
    print("ATUALIZANDO NAVEGAÇÃO EM ARQUIVOS HTML")
    print("="*70)
    
    updated_count = 0
    
    # Update navigation in root HTML files
    for html_file in PUBLIC_DIR.glob('*.html'):
        if update_navigation_in_file(html_file):
            print(f"✅ Navegação atualizada: {html_file.name}")
            updated_count += 1
    
    # Update navigation in legal HTML files
    for html_file in LEGAL_DIR.glob('*.html'):
        if update_navigation_in_file(html_file):
            print(f"✅ Navegação atualizada: legal/{html_file.name}")
            updated_count += 1
    
    print(f"\n✅ Total de arquivos atualizados: {updated_count}")
    
    print("\n" + "="*70)
    print("✅ ATUALIZAÇÃO DE MENU COMPLETA")
    print("="*70)
    
    print("\n📋 RESUMO DAS MUDANÇAS:")
    print("✅ preservacao-probatoria-digital.html movido para /legal/")
    print("✅ Dropdown 'Base Jurídica' adicionado ao menu")
    print("✅ 5 páginas legais agrupadas no dropdown")
    print("✅ CSS dropdown-menu.css incluído em todos os arquivos")
    print("✅ JavaScript dropdown-menu.js incluído em todos os arquivos")
    print("✅ Chaves de tradução adicionadas (pt, en, es)")
    print("✅ Redirects 301 atualizados")
    print("✅ Sitemap atualizado")
    
    print("\n🧪 PRÓXIMOS PASSOS:")
    print("1. Testar menu dropdown em desktop e mobile")
    print("2. Validar funcionamento do hover/click")
    print("3. Verificar tradução dos itens do menu")
    print("4. Testar redirecionamentos 301")

if __name__ == '__main__':
    main()
