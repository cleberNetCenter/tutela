#!/usr/bin/env python3
"""
CORREÇÃO URGENTE: Menu mostrando chaves ao invés de textos

Problema: Os <span data-i18n="nav.home">nav.home</span> estão mostrando
a chave ao invés do texto original "Início"

Solução: Manter o texto original dentro do span, o i18n.js vai substituir
"""

import os
import re

def fix_nav_text_content():
    """
    Corrige os elementos data-i18n para mostrar o texto correto
    ao invés das chaves
    """
    
    print("\n" + "="*70)
    print("🔧 CORRIGINDO TEXTOS DO MENU")
    print("="*70)
    
    html_files = [
        'public/index.html',
        'public/como-funciona.html',
        'public/seguranca.html',
        'public/governo.html',
        'public/empresas.html',
        'public/pessoas.html',
    ]
    
    # Mapeamento correto: chave → texto PT
    correct_texts = {
        'nav.home': 'Início',
        'nav.how_it_works': 'Como Funciona',
        'nav.security': 'Segurança',
        'nav.solutions': 'Soluções',
        'nav.legal_basis': 'Base Jurídica',
        'nav.government': 'Governo',
        'nav.companies': 'Empresas',
        'nav.individuals': 'Pessoas',
        'cta.request_demo': 'Solicitar Demonstração'
    }
    
    stats = {'files_updated': 0, 'elements_fixed': 0}
    
    for html_file in html_files:
        if not os.path.exists(html_file):
            continue
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Corrigir cada chave
        for key, correct_text in correct_texts.items():
            # Pattern: <span data-i18n="KEY">WRONG_TEXT</span>
            # Onde WRONG_TEXT pode ser a própria chave
            pattern = rf'<span data-i18n="{re.escape(key)}">[^<]*</span>'
            replacement = f'<span data-i18n="{key}">{correct_text}</span>'
            
            new_content, count = re.subn(pattern, replacement, content)
            
            if count > 0:
                content = new_content
                stats['elements_fixed'] += count
                print(f"  ✅ {html_file}: '{key}' → '{correct_text}' ({count}x)")
        
        # Salvar se houve mudanças
        if content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            stats['files_updated'] += 1
    
    return stats

def main():
    print("\n" + "="*70)
    print("🚨 CORREÇÃO URGENTE: MENU MOSTRANDO CHAVES")
    print("="*70)
    print("Problema: Menu exibe 'nav.home' ao invés de 'Início'")
    print("Solução: Manter texto PT original nos spans")
    print("="*70)
    
    stats = fix_nav_text_content()
    
    print("\n" + "="*70)
    print("📊 RELATÓRIO FINAL")
    print("="*70)
    print(f"✅ Arquivos atualizados: {stats['files_updated']}")
    print(f"✅ Elementos corrigidos: {stats['elements_fixed']}")
    
    print("\n" + "="*70)
    print("🎯 RESULTADO")
    print("="*70)
    print("✅ Menu agora mostra 'Início', 'Como Funciona', etc.")
    print("✅ i18n.js vai substituir ao trocar idioma")
    print("✅ PT: Início → EN: Home → ES: Inicio")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
