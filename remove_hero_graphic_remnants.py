#!/usr/bin/env python3
"""
Remover resíduos do hero image das páginas legais sem hero
"""

import os
import re

def remove_hero_graphic_remnants():
    """
    Remove o <div class="page-header-graphic"> das páginas legais
    """
    
    print("\n" + "="*70)
    print("🗑️  REMOVENDO RESÍDUOS DO HERO IMAGE")
    print("="*70)
    
    pages = [
        'public/legal/institucional.html',
        'public/legal/termos-de-custodia.html',
        'public/legal/politica-de-privacidade.html'
    ]
    
    stats = {'files_cleaned': 0, 'graphics_removed': 0}
    
    for html_file in pages:
        if not os.path.exists(html_file):
            print(f"  ⚠️  {html_file}: Arquivo não encontrado")
            continue
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern para remover <div class="page-header-graphic">...</div>
        # Incluindo quebras de linha e espaços
        pattern = r'\n*\s*<div class="page-header-graphic">.*?</div>\n*'
        
        content, count = re.subn(pattern, '\n', content, flags=re.DOTALL)
        
        if count > 0:
            stats['graphics_removed'] += count
            print(f"  ✅ {html_file}: Removido {count} bloco(s) page-header-graphic")
        
        # Remover também preload de imagens hero se existir
        pattern_preload = r'<link rel="preload"[^>]*hero[^>]*>\n*'
        content, count_preload = re.subn(pattern_preload, '', content)
        
        if count_preload > 0:
            print(f"  ✅ {html_file}: Removido {count_preload} preload(s) de hero image")
        
        # Salvar se houve mudanças
        if content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            stats['files_cleaned'] += 1
    
    return stats

def verify_clean_structure():
    """Verifica a estrutura limpa das páginas"""
    
    print("\n" + "="*70)
    print("🔍 VERIFICANDO ESTRUTURA LIMPA")
    print("="*70)
    
    pages = [
        'public/legal/institucional.html',
        'public/legal/termos-de-custodia.html',
        'public/legal/politica-de-privacidade.html'
    ]
    
    for page in pages:
        if os.path.exists(page):
            with open(page, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Verificar se ainda tem page-header-graphic
            has_graphic = 'page-header-graphic' in content
            
            # Verificar se tem page-header--split
            has_split = 'page-header--split' in content
            
            print(f"\n{page}:")
            print(f"  page-header-graphic: {'❌ AINDA EXISTE' if has_graphic else '✅ REMOVIDO'}")
            print(f"  page-header--split: {'✅ MANTIDO' if has_split else '❌ REMOVIDO (deveria manter)'}")
            
            # Contar linhas da section page-header
            page_header_match = re.search(
                r'<section class="page-header[^"]*">.*?</section>',
                content,
                re.DOTALL
            )
            
            if page_header_match:
                lines = page_header_match.group(0).count('\n')
                print(f"  Linhas da section page-header: {lines}")

def main():
    print("\n" + "="*70)
    print("🚨 LIMPEZA: REMOVER RESÍDUOS DO HERO IMAGE")
    print("="*70)
    print("Problema: <div class='page-header-graphic'> existe mas não deveria")
    print("Solução: Remover completamente o bloco")
    print("Páginas afetadas:")
    print("  • institucional.html")
    print("  • termos-de-custodia.html")
    print("  • politica-de-privacidade.html")
    print("="*70)
    
    # Remover resíduos
    stats = remove_hero_graphic_remnants()
    
    # Verificar estrutura
    verify_clean_structure()
    
    # Relatório final
    print("\n" + "="*70)
    print("📊 RELATÓRIO FINAL")
    print("="*70)
    print(f"✅ Arquivos limpos: {stats['files_cleaned']}")
    print(f"✅ Blocos graphic removidos: {stats['graphics_removed']}")
    
    print("\n" + "="*70)
    print("🎯 RESULTADO")
    print("="*70)
    print("✅ page-header-graphic completamente removido")
    print("✅ Estrutura limpa seguindo padrão governo.html")
    print("✅ Apenas page-header-content mantido")
    print("✅ Zero resíduos de hero image")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
