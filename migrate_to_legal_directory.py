#!/usr/bin/env python3
"""
Comprehensive Legal Pages Migration Script

This script performs a complete migration of legal pages to /legal/ directory:
1. Creates /public/legal/ directory
2. Moves legal HTML files
3. Updates all internal links
4. Updates canonical URLs
5. Updates hreflang tags
6. Creates 301 redirect configuration
7. Updates sitemap.xml
8. Validates all changes
"""

import os
import re
from pathlib import Path
import json

# Configuration
LEGAL_PAGES = [
    'institucional.html',
    'fundamento-juridico.html',
    'termos-de-custodia.html',
    'politica-de-privacidade.html',
]

# Also include preservacao-probatoria-digital.html in the menu
ADDITIONAL_MENU_PAGES = ['preservacao-probatoria-digital.html']

PUBLIC_DIR = Path('public')
LEGAL_DIR = PUBLIC_DIR / 'legal'

def create_legal_directory():
    """Create /public/legal/ directory"""
    print("\n" + "="*70)
    print("FASE 1: CRIANDO DIRETÓRIO /legal/")
    print("="*70)
    
    LEGAL_DIR.mkdir(exist_ok=True)
    print(f"✅ Diretório criado: {LEGAL_DIR}")

def move_legal_files():
    """Move legal HTML files to /legal/ directory"""
    print("\n" + "="*70)
    print("FASE 1: MOVENDO ARQUIVOS")
    print("="*70)
    
    moved_files = []
    
    for filename in LEGAL_PAGES:
        source = PUBLIC_DIR / filename
        destination = LEGAL_DIR / filename
        
        if source.exists():
            # Read content
            content = source.read_text(encoding='utf-8')
            
            # Write to new location
            destination.write_text(content, encoding='utf-8')
            print(f"✅ Movido: {filename} → /legal/{filename}")
            
            # Remove old file
            source.unlink()
            print(f"   Removido: {filename}")
            
            moved_files.append(filename)
        else:
            print(f"⚠️  Arquivo não encontrado: {filename}")
    
    return moved_files

def update_internal_links_in_file(file_path):
    """Update internal links in a single file"""
    content = file_path.read_text(encoding='utf-8')
    original_content = content
    
    # Update links to legal pages
    for page in LEGAL_PAGES:
        # Match various link formats
        patterns = [
            (rf'href="/{page}"', f'href="/legal/{page}"'),
            (rf'href="{page}"', f'href="/legal/{page}"'),
            (rf"href='/{page}'", f"href='/legal/{page}'"),
            (rf"href='{page}'", f"href='/legal/{page}'"),
        ]
        
        for old_pattern, new_pattern in patterns:
            content = re.sub(old_pattern, new_pattern, content)
    
    # Update canonical URLs
    for page in LEGAL_PAGES:
        old_canonical = f'https://tuteladigital.com.br/{page}'
        new_canonical = f'https://tuteladigital.com.br/legal/{page}'
        content = content.replace(old_canonical, new_canonical)
    
    # Update hreflang URLs
    for page in LEGAL_PAGES:
        # pt-br
        old_hreflang_pt = f'hreflang="pt-br" href="https://tuteladigital.com.br/{page}"'
        new_hreflang_pt = f'hreflang="pt-br" href="https://tuteladigital.com.br/legal/{page}"'
        content = content.replace(old_hreflang_pt, new_hreflang_pt)
        
        # x-default
        old_hreflang_def = f'hreflang="x-default" href="https://tuteladigital.com.br/{page}"'
        new_hreflang_def = f'hreflang="x-default" href="https://tuteladigital.com.br/legal/{page}"'
        content = content.replace(old_hreflang_def, new_hreflang_def)
    
    # Update breadcrumb structured data
    for page in LEGAL_PAGES:
        old_breadcrumb = f'https://www.tuteladigital.com.br/{page}'
        new_breadcrumb = f'https://www.tuteladigital.com.br/legal/{page}'
        content = content.replace(old_breadcrumb, new_breadcrumb)
    
    if content != original_content:
        file_path.write_text(content, encoding='utf-8')
        return True
    return False

def update_all_internal_links():
    """Update internal links in all HTML files"""
    print("\n" + "="*70)
    print("FASE 1: ATUALIZANDO LINKS INTERNOS")
    print("="*70)
    
    updated_files = []
    
    # Update links in legal pages
    for html_file in LEGAL_DIR.glob('*.html'):
        if update_internal_links_in_file(html_file):
            updated_files.append(str(html_file))
            print(f"✅ Links atualizados: {html_file.name}")
    
    # Update links in root pages
    for html_file in PUBLIC_DIR.glob('*.html'):
        if update_internal_links_in_file(html_file):
            updated_files.append(str(html_file))
            print(f"✅ Links atualizados: {html_file.name}")
    
    print(f"\n✅ Total de arquivos atualizados: {len(updated_files)}")
    return updated_files

def create_redirect_configuration():
    """Create 301 redirect configuration"""
    print("\n" + "="*70)
    print("FASE 2: CRIANDO CONFIGURAÇÃO DE REDIRECIONAMENTO 301")
    print("="*70)
    
    # Create _redirects file for Netlify/Cloudflare Pages
    redirects_content = "# 301 Redirects - Legal Pages Migration\n\n"
    
    for page in LEGAL_PAGES:
        redirects_content += f"/{page}  /legal/{page}  301\n"
    
    redirects_file = PUBLIC_DIR / '_redirects'
    redirects_file.write_text(redirects_content, encoding='utf-8')
    print(f"✅ Criado: {redirects_file}")
    print("\nConteúdo:")
    print(redirects_content)
    
    # Create vercel.json for Vercel
    vercel_config = {
        "redirects": [
            {
                "source": f"/{page}",
                "destination": f"/legal/{page}",
                "permanent": True
            }
            for page in LEGAL_PAGES
        ]
    }
    
    vercel_file = PUBLIC_DIR / 'vercel.json'
    vercel_file.write_text(json.dumps(vercel_config, indent=2), encoding='utf-8')
    print(f"✅ Criado: {vercel_file}")
    
    return redirects_file, vercel_file

def update_sitemap():
    """Update sitemap.xml with new URLs"""
    print("\n" + "="*70)
    print("FASE 3: ATUALIZANDO SITEMAP")
    print("="*70)
    
    sitemap_file = PUBLIC_DIR / 'sitemap.xml'
    
    if not sitemap_file.exists():
        print("⚠️  sitemap.xml não encontrado")
        return
    
    content = sitemap_file.read_text(encoding='utf-8')
    original_content = content
    
    # Remove old URLs
    for page in LEGAL_PAGES:
        # Match the entire <url> block
        pattern = rf'<url>\s*<loc>https://tuteladigital\.com\.br/{page}</loc>.*?</url>'
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Add new URLs before </urlset>
    new_urls = ""
    for page in LEGAL_PAGES:
        new_urls += f"""  <url>
    <loc>https://tuteladigital.com.br/legal/{page}</loc>
    <lastmod>2026-02-18</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
"""
    
    # Insert before </urlset>
    content = content.replace('</urlset>', new_urls + '</urlset>')
    
    sitemap_file.write_text(content, encoding='utf-8')
    print(f"✅ Sitemap atualizado: {sitemap_file}")
    print(f"   - {len(LEGAL_PAGES)} URLs antigas removidas")
    print(f"   - {len(LEGAL_PAGES)} URLs novas adicionadas em /legal/")

def update_navigation_menu():
    """Update navigation menu to use dropdown"""
    print("\n" + "="*70)
    print("FASE 4: REESTRUTURANDO MENU PRINCIPAL")
    print("="*70)
    
    # Read navigation.js or identify HTML files with navigation
    html_files = list(PUBLIC_DIR.glob('*.html')) + list(LEGAL_DIR.glob('*.html'))
    
    updated_count = 0
    
    for html_file in html_files:
        content = html_file.read_text(encoding='utf-8')
        original_content = content
        
        # Check if file has navigation
        if '<nav' not in content and 'navigation' not in content.lower():
            continue
        
        # Remove individual legal links from main navigation
        # This is a placeholder - actual implementation depends on HTML structure
        # The navigation restructuring should be done manually or with more specific patterns
        
        print(f"ℹ️  Arquivo com navegação encontrado: {html_file.name}")
        updated_count += 1
    
    print(f"\n✅ {updated_count} arquivos de navegação identificados")
    print("\n⚠️  AÇÃO MANUAL NECESSÁRIA:")
    print("   Atualizar estrutura do menu para incluir dropdown 'Base Jurídica'")
    print("   Ver FASE 4 nas instruções para estrutura HTML correta")

def create_dropdown_css():
    """Create CSS for dropdown menu"""
    print("\n" + "="*70)
    print("FASE 5: CRIANDO CSS PARA DROPDOWN")
    print("="*70)
    
    css_content = """
/* Legal Pages Dropdown Menu */
.nav-dropdown {
  position: relative;
}

.nav-dropdown > a {
  cursor: pointer;
}

.dropdown-menu {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  background: white;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  padding: 10px 0;
  min-width: 250px;
  z-index: 1000;
  border-radius: 4px;
  margin-top: 5px;
}

.dropdown-menu li {
  list-style: none;
  padding: 0;
  margin: 0;
}

.dropdown-menu a {
  display: block;
  padding: 10px 20px;
  color: #333;
  text-decoration: none;
  transition: background-color 0.2s;
}

.dropdown-menu a:hover {
  background-color: #f5f5f5;
  color: #2c5aa0;
}

.nav-dropdown:hover .dropdown-menu {
  display: block;
}

/* Mobile dropdown (click instead of hover) */
@media (max-width: 768px) {
  .nav-dropdown:hover .dropdown-menu {
    display: none;
  }
  
  .nav-dropdown.active .dropdown-menu {
    display: block;
  }
  
  .dropdown-menu {
    position: relative;
    box-shadow: none;
    border-left: 2px solid #2c5aa0;
    margin-left: 10px;
  }
}
"""
    
    css_file = PUBLIC_DIR / 'assets' / 'css' / 'dropdown-menu.css'
    css_file.parent.mkdir(parents=True, exist_ok=True)
    css_file.write_text(css_content, encoding='utf-8')
    print(f"✅ CSS criado: {css_file}")
    
    return css_file

def create_dropdown_js():
    """Create JavaScript for mobile dropdown"""
    print("\n" + "="*70)
    print("FASE 6: CRIANDO JAVASCRIPT PARA MOBILE")
    print("="*70)
    
    js_content = """
// Legal Pages Dropdown - Mobile Support
document.addEventListener('DOMContentLoaded', function() {
  const navDropdown = document.querySelector('.nav-dropdown');
  
  if (!navDropdown) return;
  
  // Only apply on mobile
  if (window.innerWidth <= 768) {
    const dropdownToggle = navDropdown.querySelector('> a');
    
    dropdownToggle.addEventListener('click', function(e) {
      e.preventDefault();
      navDropdown.classList.toggle('active');
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
      if (!navDropdown.contains(e.target)) {
        navDropdown.classList.remove('active');
      }
    });
  }
});
"""
    
    js_file = PUBLIC_DIR / 'assets' / 'js' / 'dropdown-menu.js'
    js_file.parent.mkdir(parents=True, exist_ok=True)
    js_file.write_text(js_content, encoding='utf-8')
    print(f"✅ JavaScript criado: {js_file}")
    
    return js_file

def validate_migration():
    """Validate the migration"""
    print("\n" + "="*70)
    print("FASE 7: VALIDAÇÃO SEO E ESTRUTURAL")
    print("="*70)
    
    checks = []
    
    # Check if legal directory exists
    if LEGAL_DIR.exists():
        checks.append(("✅", "Diretório /legal/ existe"))
    else:
        checks.append(("❌", "Diretório /legal/ não existe"))
    
    # Check if files were moved
    for page in LEGAL_PAGES:
        if (LEGAL_DIR / page).exists():
            checks.append(("✅", f"/legal/{page} existe"))
        else:
            checks.append(("❌", f"/legal/{page} não encontrado"))
    
    # Check if old files were removed
    for page in LEGAL_PAGES:
        if not (PUBLIC_DIR / page).exists():
            checks.append(("✅", f"/{page} removido (sucesso)"))
        else:
            checks.append(("⚠️ ", f"/{page} ainda existe (deveria ser removido)"))
    
    # Check if redirects exist
    if (PUBLIC_DIR / '_redirects').exists():
        checks.append(("✅", "_redirects criado"))
    else:
        checks.append(("❌", "_redirects não criado"))
    
    # Check if sitemap was updated
    sitemap_file = PUBLIC_DIR / 'sitemap.xml'
    if sitemap_file.exists():
        sitemap_content = sitemap_file.read_text()
        if '/legal/' in sitemap_content:
            checks.append(("✅", "Sitemap contém URLs /legal/"))
        else:
            checks.append(("❌", "Sitemap não contém URLs /legal/"))
    
    # Check if CSS was created
    if (PUBLIC_DIR / 'assets' / 'css' / 'dropdown-menu.css').exists():
        checks.append(("✅", "CSS dropdown criado"))
    else:
        checks.append(("❌", "CSS dropdown não criado"))
    
    # Check if JS was created
    if (PUBLIC_DIR / 'assets' / 'js' / 'dropdown-menu.js').exists():
        checks.append(("✅", "JavaScript dropdown criado"))
    else:
        checks.append(("❌", "JavaScript dropdown não criado"))
    
    # Check canonical updates in legal pages
    canonical_ok = 0
    for page in LEGAL_PAGES:
        legal_file = LEGAL_DIR / page
        if legal_file.exists():
            content = legal_file.read_text()
            if f'canonical" href="https://tuteladigital.com.br/legal/{page}' in content:
                canonical_ok += 1
    
    if canonical_ok == len(LEGAL_PAGES):
        checks.append(("✅", f"Canonical atualizado em todas {len(LEGAL_PAGES)} páginas"))
    else:
        checks.append(("⚠️ ", f"Canonical atualizado em {canonical_ok}/{len(LEGAL_PAGES)} páginas"))
    
    print("\nResultados da Validação:")
    print("-" * 70)
    for status, message in checks:
        print(f"{status} {message}")
    
    # Summary
    success_count = sum(1 for s, _ in checks if s == "✅")
    warning_count = sum(1 for s, _ in checks if s == "⚠️ ")
    error_count = sum(1 for s, _ in checks if s == "❌")
    
    print("\n" + "="*70)
    print("RESUMO DA VALIDAÇÃO")
    print("="*70)
    print(f"✅ Sucesso: {success_count}")
    print(f"⚠️  Avisos:  {warning_count}")
    print(f"❌ Erros:   {error_count}")
    
    if error_count == 0 and warning_count == 0:
        print("\n🎉 MIGRAÇÃO COMPLETA E VALIDADA COM SUCESSO!")
    elif error_count == 0:
        print("\n⚠️  MIGRAÇÃO COMPLETA COM AVISOS")
    else:
        print("\n❌ MIGRAÇÃO INCOMPLETA - VERIFICAR ERROS")
    
    return checks

def main():
    """Execute full migration"""
    print("\n" + "="*70)
    print("🚀 MIGRAÇÃO DE PÁGINAS JURÍDICAS PARA /legal/")
    print("="*70)
    print(f"\nDiretório de trabalho: {Path.cwd()}")
    print(f"Páginas a migrar: {len(LEGAL_PAGES)}")
    
    try:
        # Phase 1: File migration
        create_legal_directory()
        moved_files = move_legal_files()
        updated_files = update_all_internal_links()
        
        # Phase 2: Redirects
        create_redirect_configuration()
        
        # Phase 3: Sitemap
        update_sitemap()
        
        # Phase 4: Navigation (manual step documented)
        update_navigation_menu()
        
        # Phase 5: CSS
        create_dropdown_css()
        
        # Phase 6: JavaScript
        create_dropdown_js()
        
        # Phase 7: Validation
        validate_migration()
        
        print("\n" + "="*70)
        print("✅ MIGRAÇÃO COMPLETA")
        print("="*70)
        
        print("\n⚠️  PRÓXIMOS PASSOS MANUAIS:")
        print("1. Revisar e atualizar estrutura do menu em todos os arquivos HTML")
        print("2. Adicionar <link> para dropdown-menu.css no <head>")
        print("3. Adicionar <script> para dropdown-menu.js antes de </body>")
        print("4. Testar redirecionamentos 301 no servidor")
        print("5. Validar Lighthouse SEO")
        print("6. Submeter novo sitemap ao Google Search Console")
        
    except Exception as e:
        print(f"\n❌ ERRO DURANTE MIGRAÇÃO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
