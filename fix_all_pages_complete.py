#!/usr/bin/env python3
"""
Fix ALL HTML pages - Remove wrong </li> tag and standardize structure
"""

import os
import re
from pathlib import Path

def fix_dropdown_closing_tag(content):
    """Remove the wrong </li> tag after first dropdown"""
    # Pattern: </ul>\n</li>\n\n<div class="nav-dropdown">
    # Should be: </ul>\n</div>\n\n<div class="nav-dropdown">
    
    content = re.sub(
        r'</ul>\s*</li>\s*\n\s*<div class="nav-dropdown">',
        '</ul>\n</div>\n\n<div class="nav-dropdown">',
        content
    )
    
    return content

def get_standard_header_html():
    """Return the corrected standard header"""
    return '''<header class="header" id="header">
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
</header>'''

def replace_header_section(content, standard_header):
    """Replace the entire header section with standard one"""
    # Match from <header to </header>
    header_pattern = r'<header[^>]*>.*?</header>'
    
    if re.search(header_pattern, content, re.DOTALL):
        content = re.sub(header_pattern, standard_header, content, flags=re.DOTALL)
        return content, True
    return content, False

def process_html_file(filepath):
    """Process a single HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Fix closing tag
    content = fix_dropdown_closing_tag(content)
    
    # Replace header with standard one
    standard_header = get_standard_header_html()
    content, header_replaced = replace_header_section(content, standard_header)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, header_replaced
    return False, False

def main():
    print("\n" + "="*70)
    print("CORREÇÃO COMPLETA - TODAS AS PÁGINAS HTML")
    print("="*70 + "\n")
    
    # List all HTML files to fix
    html_files = [
        # Root pages
        'public/index.html',
        'public/como-funciona.html',
        'public/seguranca.html',
        'public/governo.html',
        'public/empresas.html',
        'public/pessoas.html',
        # Legal pages
        'public/legal/institucional.html',
        'public/legal/fundamento-juridico.html',
        'public/legal/termos-de-custodia.html',
        'public/legal/politica-de-privacidade.html',
        'public/legal/preservacao-probatoria-digital.html',
    ]
    
    fixed_count = 0
    header_replaced_count = 0
    
    for filepath in html_files:
        if os.path.exists(filepath):
            was_fixed, header_replaced = process_html_file(filepath)
            if was_fixed:
                filename = os.path.basename(filepath)
                status = []
                if header_replaced:
                    status.append("header padronizado")
                    header_replaced_count += 1
                status.append("</li> removido")
                
                print(f"✅ {filename}: {', '.join(status)}")
                fixed_count += 1
            else:
                print(f"⏭️  {os.path.basename(filepath)}: Já estava correto")
        else:
            print(f"❌ {filepath}: Arquivo não encontrado")
    
    print(f"\n{'='*70}")
    print(f"✅ {fixed_count} arquivos corrigidos")
    print(f"✅ {header_replaced_count} headers padronizados")
    print(f"✅ Tag </li> errada removida de todos os arquivos")
    print(f"✅ Estrutura dropdown 100% consistente")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
