#!/usr/bin/env python3
"""
Fix dropdown CSS structure and restore page formatting
"""

import os
import re

def fix_dropdown_structure(content):
    """Replace <li class="nav-dropdown"> with <div class="nav-dropdown">"""
    
    # Replace opening tag
    content = content.replace('<li class="nav-dropdown">', '<div class="nav-dropdown">')
    
    # Replace closing tag
    content = content.replace('</li>\n\n<li class="nav-dropdown">', '</div>\n\n<div class="nav-dropdown">')
    content = content.replace('</li>\n</nav>', '</div>\n</nav>')
    
    # Fix nested <li> to keep them (they're inside <ul>)
    # No changes needed for <li> inside <ul class="dropdown-menu">
    
    return content

def get_full_header():
    """Return complete header HTML with proper structure"""
    return '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>{title}</title>
<meta content="{description}" name="description"/>
<link href="/assets/illustrations/favicon.svg" rel="icon" type="image/svg+xml"/>
<link rel="stylesheet" href="/assets/css/styles-clean.css">
<link rel="stylesheet" href="/assets/css/styles-header-final.css">
<link rel="stylesheet" href="/assets/css/styles-clean.exec-compact.css">
<link rel="stylesheet" href="/assets/css/dropdown-menu.css">
</head>
<body class="exec-compact">
<header class="header" id="header">
<div class="header-inner">
<a class="logo" href="/">
    Tutela Digital<sup>®</sup>
</a>
<nav class="nav" id="nav">
<a class="nav-link" href="/">Início</a>
<a class="nav-link" href="/como-funciona.html">Como Funciona</a>
<a class="nav-link" href="/seguranca.html">Segurança</a>

<div class="nav-dropdown">
<a href="#" class="nav-link">Soluções</a>
<ul class="dropdown-menu">
<li><a href="/governo.html">Governo</a></li>
<li><a href="/empresas.html">Empresas</a></li>
<li><a href="/pessoas.html">Pessoas</a></li>
</ul>
</div>

<div class="nav-dropdown">
<a href="#" class="nav-link">Base Jurídica</a>
<ul class="dropdown-menu">
<li><a href="/legal/preservacao-probatoria-digital.html">Preservação Probatória</a></li>
<li><a href="/legal/fundamento-juridico.html">Fundamento Jurídico</a></li>
<li><a href="/legal/termos-de-custodia.html">Termos de Custódia</a></li>
<li><a href="/legal/politica-de-privacidade.html">Política de Privacidade</a></li>
<li><a href="/legal/institucional.html">Institucional</a></li>
</ul>
</div>
</nav>
<a class="header-cta" href="https://app.tuteladigital.com.br/" rel="noopener noreferrer" target="_blank">
    Acessar a Plataforma
</a>
<button class="mobile-menu-btn" onclick="toggleMobileMenu()">
<span></span>
<span></span>
<span></span>
</button>
<div class="lang-dropdown">
  <button class="lang-toggle" aria-label="Selecionar idioma">
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 4px;">
      <circle cx="12" cy="12" r="10"></circle>
      <line x1="2" y1="12" x2="22" y2="12"></line>
      <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
    </svg> <span class="lang-code">PT</span>
  </button>
  <div class="lang-menu">
    <button class="lang-option" data-lang="pt">🇧🇷 Português</button>
    <button class="lang-option" data-lang="en">🇺🇸 English</button>
    <button class="lang-option" data-lang="es">🇪🇸 Español</button>
  </div>
</div>
</div>
</header>
'''

def fix_solution_pages():
    """Fix Governo, Empresas, Pessoas pages"""
    pages = {
        'governo.html': {
            'title': 'Governo | Tutela Digital®',
            'description': 'Soluções de custódia digital para órgãos públicos e governamentais.'
        },
        'empresas.html': {
            'title': 'Empresas | Tutela Digital®',
            'description': 'Soluções de custódia digital para empresas e organizações.'
        },
        'pessoas.html': {
            'title': 'Pessoas | Tutela Digital®',
            'description': 'Soluções de custódia digital para pessoas físicas.'
        }
    }
    
    for page, metadata in pages.items():
        filepath = f"public/{page}"
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract main content (between <main> and </main>)
            main_match = re.search(r'<main>(.*?)</main>', content, re.DOTALL)
            if main_match:
                main_content = main_match.group(1)
                
                # Create full page
                header = get_full_header().format(
                    title=metadata['title'],
                    description=metadata['description']
                )
                
                footer = '''
<script src="/assets/js/mobile-menu.js"></script>
<script src="/assets/js/language-selector.js"></script>
<script src="/assets/js/dropdown-menu.js"></script>
</body>
</html>'''
                
                full_page = header + '\n<main>' + main_content + '</main>\n' + footer
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(full_page)
                
                print(f"✅ {page}: Header completo restaurado")

def fix_all_pages_dropdown_structure():
    """Fix dropdown structure in all HTML files"""
    html_files = []
    
    # Root pages
    for f in ['index.html', 'como-funciona.html', 'seguranca.html', 
              'governo.html', 'empresas.html', 'pessoas.html']:
        html_files.append(f"public/{f}")
    
    # Legal pages
    for f in ['institucional.html', 'fundamento-juridico.html', 
              'termos-de-custodia.html', 'politica-de-privacidade.html',
              'preservacao-probatoria-digital.html']:
        html_files.append(f"public/legal/{f}")
    
    updated = 0
    for filepath in html_files:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            content = fix_dropdown_structure(content)
            
            if content != original:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated += 1
                print(f"✅ {os.path.basename(filepath)}: Estrutura dropdown corrigida")
    
    return updated

def main():
    print("\n" + "="*60)
    print("CORRIGINDO ESTRUTURA DOS DROPDOWNS E PÁGINAS")
    print("="*60 + "\n")
    
    print("1️⃣ Corrigindo estrutura dos dropdowns (li → div)...\n")
    updated_dropdowns = fix_all_pages_dropdown_structure()
    
    print(f"\n2️⃣ Restaurando header completo nas páginas de soluções...\n")
    fix_solution_pages()
    
    print(f"\n✅ {updated_dropdowns} páginas com dropdown corrigido")
    print("✅ 3 páginas de soluções restauradas")
    print("✅ Estrutura agora segue padrão do lang-dropdown")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
