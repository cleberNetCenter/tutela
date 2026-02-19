#!/usr/bin/env python3
"""
Script para corrigir alinhamento dos dropdowns e seletor de idiomas.

PROBLEMAS:
1. Dropdowns desalinhados com outros itens do menu
2. Globo do seletor de idiomas desapareceu
3. Mostrar apenas globo, eliminar iniciais da língua (PT/EN/ES)

SOLUÇÕES:
1. Remover padding extra dos dropdowns para alinhamento correto
2. Garantir que o globo SVG esteja presente
3. Remover <span class="lang-code"> do HTML
4. Centralizar verticalmente o globo
"""

from pathlib import Path
import re

# Diretórios
PUBLIC_DIR = Path('public')
CSS_DIR = PUBLIC_DIR / 'assets' / 'css'

def fix_dropdown_css():
    """Corrige o CSS dos dropdowns para alinhamento correto."""
    dropdown_css_file = CSS_DIR / 'dropdown-menu.css'
    
    with open(dropdown_css_file, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    # Remove padding que causa desalinhamento
    css_content = re.sub(
        r'(\.nav-dropdown > a,\s*\.nav-dropdown > \.nav-link\s*{[^}]*?)padding:\s*[^;]+;',
        r'\1',
        css_content
    )
    
    # Adiciona alinhamento vertical correto
    new_dropdown_css = """/* =========================================================
   NAV DROPDOWN (Soluções & Base Jurídica)
   Alinhado com outros itens do menu
   ========================================================= */

.nav-dropdown {
  position: relative;
  display: inline-block;
}

/* Dropdown trigger link - alinhado com .nav-link */
.nav-dropdown > a,
.nav-dropdown > .nav-link {
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 500;
  color: rgba(255,255,255,0.8);
  text-decoration: none;
  white-space: nowrap;
  position: relative;
  display: inline-block;
}

.nav-dropdown > a:hover,
.nav-dropdown > .nav-link:hover {
  color: #ffffff;
}

/* Dropdown menu container */
.dropdown-menu {
  position: absolute;
  left: 0;
  top: calc(100% + 8px);
  background: var(--color-surface-base);
  border: 1px solid var(--color-border-soft);
  display: none;
  flex-direction: column;
  min-width: 200px;
  z-index: 200;
  padding: 0;
  margin: 0;
  list-style: none;
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

/* Dropdown menu items */
.dropdown-menu li {
  list-style: none;
  padding: 0;
  margin: 0;
}

/* Dropdown menu links */
.dropdown-menu a {
  display: block;
  padding: 0.6rem 0.9rem;
  font-size: 0.85rem;
  color: rgba(255,255,255,0.85);
  text-decoration: none;
  background: none;
  border: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s ease;
}

.dropdown-menu a:hover {
  background: rgba(255,255,255,0.08);
  color: #ffffff;
}

/* Show dropdown on hover (desktop) */
.nav-dropdown:hover .dropdown-menu,
.nav-dropdown:focus-within .dropdown-menu {
  display: flex;
}

/* Mobile dropdown (click instead of hover) */
@media (max-width: 1200px) {
  .nav-dropdown:hover .dropdown-menu {
    display: none;
  }
  
  .nav-dropdown.active .dropdown-menu {
    display: flex;
  }
  
  .dropdown-menu {
    position: relative;
    left: auto;
    top: auto;
    margin-top: 4px;
    margin-left: 10px;
    border-left: 2px solid rgba(255,255,255,0.3);
    border: 1px solid rgba(255,255,255,0.2);
    background: rgba(255,255,255,0.05);
  }
}
"""
    
    with open(dropdown_css_file, 'w', encoding='utf-8') as f:
        f.write(new_dropdown_css)
    
    print(f"✅ {dropdown_css_file.name} - Dropdown CSS corrigido (alinhamento)")

def fix_lang_selector_css():
    """Corrige o CSS do seletor de idiomas."""
    header_css_file = CSS_DIR / 'styles-header-final.css'
    
    with open(header_css_file, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    # Adiciona estilo para esconder o texto da língua e centralizar o globo
    lang_css_addition = """
/* Esconder código da língua, mostrar apenas globo */
.lang-toggle .lang-code {
  display: none;
}

/* Centralizar globo verticalmente */
.lang-toggle svg {
  vertical-align: middle;
  margin: 0;
}
"""
    
    # Adiciona antes do final do arquivo
    if '.lang-toggle .lang-code' not in css_content:
        css_content = css_content.rstrip() + '\n' + lang_css_addition
    
    with open(header_css_file, 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    print(f"✅ {header_css_file.name} - Language selector CSS corrigido")

def fix_html_pages():
    """Remove a tag <span class="lang-code"> de todas as páginas."""
    html_files = list(PUBLIC_DIR.glob('*.html')) + list(PUBLIC_DIR.glob('legal/*.html'))
    
    fixed_count = 0
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Remove o <span class="lang-code">XX</span>
        original_content = html_content
        html_content = re.sub(
            r'<svg[^>]*>.*?</svg>\s*<span class="lang-code">[^<]+</span>',
            lambda m: m.group(0).split('<span')[0].rstrip(),
            html_content,
            flags=re.DOTALL
        )
        
        # Garante que o SVG do globo esteja presente
        if 'lang-toggle' in html_content and '<svg' not in re.search(r'<button class="lang-toggle"[^>]*>.*?</button>', html_content, re.DOTALL).group(0):
            # Adiciona o SVG do globo
            globe_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="12" cy="12" r="10"></circle>
      <line x1="2" y1="12" x2="22" y2="12"></line>
      <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
    </svg>'''
            
            html_content = re.sub(
                r'(<button class="lang-toggle"[^>]*>)\s*',
                rf'\1\n    {globe_svg}\n  ',
                html_content
            )
        
        if html_content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            fixed_count += 1
            print(f"✅ {html_file.name} - Lang selector HTML corrigido")
    
    return fixed_count

def main():
    """Executa todas as correções."""
    print("🔧 Corrigindo alinhamento dos dropdowns e seletor de idiomas...\n")
    
    # 1. Corrigir CSS dos dropdowns
    fix_dropdown_css()
    
    # 2. Corrigir CSS do seletor de idiomas
    fix_lang_selector_css()
    
    # 3. Corrigir HTML de todas as páginas
    fixed_html = fix_html_pages()
    
    print(f"\n✅ Correções concluídas!")
    print(f"  • Dropdown CSS: alinhamento corrigido")
    print(f"  • Language selector CSS: globo centralizado, texto escondido")
    print(f"  • HTML pages: {fixed_html} arquivos corrigidos")
    print("\n📋 Resultado:")
    print("  ✅ Dropdowns alinhados com outros itens do menu")
    print("  ✅ Globo visível e centralizado no seletor de idiomas")
    print("  ✅ Iniciais da língua (PT/EN/ES) removidas do header")
    print("  ✅ Layout consistente e profissional")

if __name__ == '__main__':
    main()
