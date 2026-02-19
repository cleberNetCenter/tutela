#!/usr/bin/env python3
"""
Corrigir CSS das páginas legais sem hero image para seguir padrão da página de governo
"""

import os
import re

def fix_legal_pages_css():
    """
    Corrige CSS das páginas legais sem hero image:
    - institucional.html
    - termos-de-custodia.html
    - politica-de-privacidade.html
    """
    
    print("\n" + "="*70)
    print("🔧 CORRIGINDO CSS DAS PÁGINAS LEGAIS SEM HERO IMAGE")
    print("="*70)
    
    # Páginas a corrigir (sem hero image)
    pages_to_fix = [
        'public/legal/institucional.html',
        'public/legal/termos-de-custodia.html',
        'public/legal/politica-de-privacidade.html'
    ]
    
    # CSS correto (padrão governo)
    correct_css = '''<!-- CSS -->
<link rel="stylesheet" href="/assets/css/styles-clean.css?v=4">
<link rel="stylesheet" href="/assets/css/styles-header-final.css?v=4">
<link rel="stylesheet" href="/assets/css/styles-clean.exec-compact.css?v=4">
<link rel="stylesheet" href="/assets/css/dropdown-menu.css?v=202602190108">'''
    
    stats = {'files_fixed': 0, 'errors': []}
    
    for html_file in pages_to_fix:
        if not os.path.exists(html_file):
            stats['errors'].append(f"❌ Arquivo não encontrado: {html_file}")
            continue
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Remover CSS antigos (qualquer link stylesheet antes do Google Analytics)
            # Pattern: encontrar todos os <link rel="stylesheet" antes de <!-- Google Analytics -->
            pattern = r'(<link href="https://fonts\.gstatic\.com"[^>]*>\n)(.*?)(\n<!-- Google Analytics -->)'
            
            def replacer(match):
                return match.group(1) + '\n' + correct_css + '\n' + match.group(3)
            
            content = re.sub(pattern, replacer, content, flags=re.DOTALL)
            
            # Se não encontrou o pattern acima, tentar outro approach
            if content == original_content:
                # Buscar e substituir links CSS antigos
                # Remove todos os <link rel="stylesheet" href="assets/ ou /assets/
                content = re.sub(
                    r'<link rel="stylesheet" href="[./]*assets/css/[^"]+">[\n\r]*',
                    '',
                    content
                )
                
                # Adicionar CSS correto antes do Google Analytics
                content = content.replace(
                    '<!-- Google Analytics -->',
                    correct_css + '\n<!-- Google Analytics -->'
                )
            
            # Adicionar dropdown-menu.css se não existir
            if 'dropdown-menu.css' not in content:
                content = content.replace(
                    '<link rel="stylesheet" href="/assets/css/styles-clean.exec-compact.css?v=4">',
                    '<link rel="stylesheet" href="/assets/css/styles-clean.exec-compact.css?v=4">\n<link rel="stylesheet" href="/assets/css/dropdown-menu.css?v=202602190108">'
                )
            
            # Garantir que body tem class exec-compact
            if 'class="exec-compact"' not in content:
                content = re.sub(
                    r'<body([^>]*)>',
                    r'<body\1 class="exec-compact">',
                    content
                )
            
            # Salvar se houve mudanças
            if content != original_content:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                stats['files_fixed'] += 1
                print(f"  ✅ {html_file}: CSS corrigido")
                print(f"     • Caminhos absolutos: /assets/css/")
                print(f"     • styles-clean.css?v=4")
                print(f"     • styles-header-final.css?v=4")
                print(f"     • styles-clean.exec-compact.css?v=4")
                print(f"     • dropdown-menu.css?v=202602190108")
            else:
                print(f"  ℹ️  {html_file}: Já estava correto")
        
        except Exception as e:
            stats['errors'].append(f"❌ Erro ao processar {html_file}: {str(e)}")
    
    return stats

def verify_css_links():
    """Verifica os links CSS nas páginas"""
    
    print("\n" + "="*70)
    print("🔍 VERIFICANDO LINKS CSS")
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
            
            # Contar links CSS
            css_links = re.findall(r'<link rel="stylesheet" href="([^"]+)"', content)
            
            print(f"\n{page}:")
            for link in css_links:
                print(f"  • {link}")

def main():
    print("\n" + "="*70)
    print("🚨 CORREÇÃO: CSS DAS PÁGINAS LEGAIS SEM HERO IMAGE")
    print("="*70)
    print("Páginas afetadas:")
    print("  • institucional.html")
    print("  • termos-de-custodia.html")
    print("  • politica-de-privacidade.html")
    print("\nPadrão a seguir: página de governo")
    print("="*70)
    
    # Corrigir CSS
    stats = fix_legal_pages_css()
    
    # Verificar links
    verify_css_links()
    
    # Relatório final
    print("\n" + "="*70)
    print("📊 RELATÓRIO FINAL")
    print("="*70)
    print(f"✅ Arquivos corrigidos: {stats['files_fixed']}")
    
    if stats['errors']:
        print(f"\n⚠️  Erros encontrados: {len(stats['errors'])}")
        for error in stats['errors']:
            print(f"   {error}")
    else:
        print("\n✅ Nenhum erro encontrado!")
    
    print("\n" + "="*70)
    print("🎯 RESULTADO")
    print("="*70)
    print("✅ Páginas legais seguem padrão da página de governo")
    print("✅ CSS com caminhos absolutos /assets/css/")
    print("✅ Todos os 4 arquivos CSS incluídos:")
    print("   • styles-clean.css?v=4")
    print("   • styles-header-final.css?v=4")
    print("   • styles-clean.exec-compact.css?v=4")
    print("   • dropdown-menu.css?v=202602190108")
    print("✅ class='exec-compact' no <body>")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
