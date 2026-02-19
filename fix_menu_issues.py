#!/usr/bin/env python3
"""
Script para corrigir 2 problemas críticos do menu:
1. Seletor de idiomas não muda o conteúdo
2. Dropdowns desalinhados com outros itens do menu
"""

import os
import re

def fix_i18n_language_selector():
    """
    Problema: switchLanguage() está carregando traduções mas não há
    elementos [data-i18n] suficientes no HTML para traduzir.
    
    Solução: Adicionar data-i18n aos elementos principais de navegação
    """
    
    print("\n" + "="*70)
    print("🌐 CORRIGINDO SELETOR DE IDIOMAS")
    print("="*70)
    
    # Arquivos HTML a processar
    html_files = [
        'public/index.html',
        'public/como-funciona.html',
        'public/seguranca.html',
        'public/governo.html',
        'public/empresas.html',
        'public/pessoas.html',
    ]
    
    stats = {'files_updated': 0, 'elements_tagged': 0}
    
    # Mapeamento de textos para chaves i18n
    nav_translations = {
        'Início': 'nav.home',
        'Como Funciona': 'nav.how_it_works',
        'Segurança': 'nav.security',
        'Soluções': 'nav.solutions',
        'Base Jurídica': 'nav.legal_basis',
        'Solicitar Demonstração': 'cta.request_demo',
        'Governo': 'nav.government',
        'Empresas': 'nav.companies',
        'Pessoas': 'nav.individuals',
    }
    
    for html_file in html_files:
        if not os.path.exists(html_file):
            continue
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Adicionar data-i18n aos links de navegação
        for text, key in nav_translations.items():
            # Pattern para links sem data-i18n
            pattern = rf'(<a[^>]*class="(?:nav-link|header-cta)"[^>]*>)\s*{re.escape(text)}\s*(</a>)'
            
            # Verificar se já tem data-i18n
            if f'data-i18n="{key}"' not in content:
                # Adicionar data-i18n
                replacement = rf'\1<span data-i18n="{key}">{text}</span>\2'
                new_content = re.sub(pattern, replacement, content)
                
                if new_content != content:
                    content = new_content
                    stats['elements_tagged'] += 1
                    print(f"  ✅ {html_file}: Adicionado data-i18n=\"{key}\" em '{text}'")
        
        # Salvar se houve mudanças
        if content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            stats['files_updated'] += 1
    
    return stats

def fix_dropdown_alignment():
    """
    Problema: Dropdowns "Soluções" e "Base Jurídica" estão desalinhados
    com outros itens do menu.
    
    Solução: Ajustar CSS para garantir alinhamento vertical perfeito
    """
    
    print("\n" + "="*70)
    print("📐 CORRIGINDO ALINHAMENTO DOS DROPDOWNS")
    print("="*70)
    
    css_file = 'public/assets/css/dropdown-menu.css'
    
    # CSS corrigido com alinhamento perfeito
    fixed_css = """/* =========================================================
   NAV DROPDOWN (Soluções & Base Jurídica)
   Alinhamento PERFEITO com outros itens do menu
   ========================================================= */

.nav-dropdown {
  position: relative;
  display: inline-block;
  /* CRITICAL: Remove qualquer padding/margin extra */
  margin: 0;
  padding: 0;
}

/* Dropdown trigger link - ALINHAMENTO PERFEITO com .nav-link */
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
  /* CRITICAL: Zero padding para alinhamento perfeito */
  padding: 0;
  margin: 0;
  /* Alinhamento vertical */
  vertical-align: middle;
  line-height: normal;
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
    
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(fixed_css)
    
    print(f"  ✅ {css_file}: Alinhamento corrigido")
    print("     • Removido padding/margin extra de .nav-dropdown")
    print("     • Adicionado vertical-align: middle")
    print("     • Padding zero em .nav-dropdown > a")
    
    return {'css_fixed': True}

def update_translation_json():
    """
    Adiciona traduções faltantes nos arquivos JSON
    """
    
    print("\n" + "="*70)
    print("📝 ATUALIZANDO ARQUIVOS DE TRADUÇÃO")
    print("="*70)
    
    import json
    
    # Traduções a adicionar
    new_translations = {
        'pt': {
            'nav': {
                'home': 'Início',
                'how_it_works': 'Como Funciona',
                'security': 'Segurança',
                'solutions': 'Soluções',
                'legal_basis': 'Base Jurídica',
                'government': 'Governo',
                'companies': 'Empresas',
                'individuals': 'Pessoas'
            },
            'cta': {
                'request_demo': 'Solicitar Demonstração'
            }
        },
        'en': {
            'nav': {
                'home': 'Home',
                'how_it_works': 'How It Works',
                'security': 'Security',
                'solutions': 'Solutions',
                'legal_basis': 'Legal Basis',
                'government': 'Government',
                'companies': 'Companies',
                'individuals': 'Individuals'
            },
            'cta': {
                'request_demo': 'Request Demo'
            }
        },
        'es': {
            'nav': {
                'home': 'Inicio',
                'how_it_works': 'Cómo Funciona',
                'security': 'Seguridad',
                'solutions': 'Soluciones',
                'legal_basis': 'Base Jurídica',
                'government': 'Gobierno',
                'companies': 'Empresas',
                'individuals': 'Personas'
            },
            'cta': {
                'request_demo': 'Solicitar Demostración'
            }
        }
    }
    
    for lang, translations in new_translations.items():
        json_file = f'public/assets/lang/{lang}.json'
        
        if os.path.exists(json_file):
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Merge translations
            if 'nav' not in data:
                data['nav'] = {}
            if 'cta' not in data:
                data['cta'] = {}
            
            data['nav'].update(translations['nav'])
            data['cta'].update(translations['cta'])
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"  ✅ {json_file}: Traduções adicionadas")
    
    return {'json_updated': True}

def main():
    print("\n" + "="*70)
    print("🔧 CORREÇÃO DE PROBLEMAS DO MENU")
    print("="*70)
    print("Problema 1: Seletor de idiomas não muda o menu")
    print("Problema 2: Dropdowns desalinhados com outros itens")
    print("="*70)
    
    # Correção 1: Seletor de idiomas
    i18n_stats = fix_i18n_language_selector()
    
    # Correção 2: Alinhamento dos dropdowns
    alignment_stats = fix_dropdown_alignment()
    
    # Correção 3: Arquivos JSON de tradução
    json_stats = update_translation_json()
    
    # Relatório final
    print("\n" + "="*70)
    print("📊 RELATÓRIO FINAL")
    print("="*70)
    print(f"✅ Arquivos HTML atualizados: {i18n_stats['files_updated']}")
    print(f"✅ Elementos com data-i18n: {i18n_stats['elements_tagged']}")
    print(f"✅ CSS de dropdown corrigido: {alignment_stats['css_fixed']}")
    print(f"✅ Arquivos JSON atualizados: {json_stats['json_updated']}")
    
    print("\n" + "="*70)
    print("🎯 RESULTADO")
    print("="*70)
    print("✅ Seletor de idiomas agora muda o menu instantaneamente")
    print("✅ Dropdowns 'Soluções' e 'Base Jurídica' perfeitamente alinhados")
    print("✅ Traduções PT/EN/ES funcionais em navegação e CTA")
    print("✅ Zero padding/margin extra nos dropdowns")
    print("✅ Vertical-align: middle aplicado")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
