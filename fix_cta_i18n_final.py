#!/usr/bin/env python3
"""
Correção DEFINITIVA dos botões CTA - i18n
Substitui data-i18n="global.cta_button" por data-i18n="global.accessPlatform"
"""
import re
from pathlib import Path

def fix_cta_buttons(html_file):
    """Corrige atributos data-i18n dos botões CTA"""
    print(f"\n📄 Processando: {html_file.name}")
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes = 0
    
    # 1. Corrigir header CTA: data-i18n="global.cta_button" → data-i18n="global.accessPlatform"
    pattern1 = r'(<a[^>]*class="header-cta"[^>]*)data-i18n="global\.cta_button"'
    if re.search(pattern1, content):
        content = re.sub(pattern1, r'\1data-i18n="global.accessPlatform"', content)
        changes += len(re.findall(pattern1, original_content))
        print(f"  ✓ Corrigido header-cta: global.cta_button → global.accessPlatform")
    
    # 2. Corrigir footer CTA (btn-primary): data-i18n="global.cta_button" → data-i18n="global.accessPlatform"
    pattern2 = r'(<a[^>]*class="btn btn-primary"[^>]*)data-i18n="global\.cta_button"'
    matches = len(re.findall(pattern2, original_content))
    if matches > 0:
        content = re.sub(pattern2, r'\1data-i18n="global.accessPlatform"', content)
        changes += matches
        print(f"  ✓ Corrigido {matches} btn-primary: global.cta_button → global.accessPlatform")
    
    # 3. Adicionar data-i18n em botões que não têm (mas mantêm texto PT como fallback)
    # Header CTA sem data-i18n
    pattern3 = r'<a\s+([^>]*class="header-cta"[^>]*)(?!.*data-i18n)([^>]*>)([^<]*)</a>'
    if re.search(pattern3, content):
        def add_i18n_header(match):
            attrs = match.group(1)
            close_attrs = match.group(2)
            text = match.group(3).strip()
            if 'data-i18n' not in attrs and 'data-i18n' not in close_attrs:
                return f'<a {attrs.strip()} data-i18n="global.accessPlatform"{close_attrs}{text}</a>'
            return match.group(0)
        
        new_content = re.sub(pattern3, add_i18n_header, content)
        if new_content != content:
            content = new_content
            changes += 1
            print(f"  ✓ Adicionado data-i18n em header-cta")
    
    # Footer CTA (btn-primary) sem data-i18n
    pattern4 = r'<a\s+([^>]*class="btn btn-primary"[^>]*)(?!.*data-i18n)([^>]*>)([^<]*)</a>'
    if re.search(pattern4, content):
        def add_i18n_footer(match):
            attrs = match.group(1)
            close_attrs = match.group(2)
            text = match.group(3).strip()
            if 'data-i18n' not in attrs and 'data-i18n' not in close_attrs:
                return f'<a {attrs.strip()} data-i18n="global.accessPlatform"{close_attrs}{text}</a>'
            return match.group(0)
        
        new_content = re.sub(pattern4, add_i18n_footer, content)
        if new_content != content:
            content = new_content
            changes += 1
            print(f"  ✓ Adicionado data-i18n em btn-primary")
    
    if changes > 0:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ {changes} alterações salvas")
        return True
    else:
        print(f"  ℹ️  Nenhuma alteração necessária")
        return False

def main():
    """Corrige todos os arquivos HTML"""
    print("🔧 CORREÇÃO DEFINITIVA - Botões CTA i18n")
    print("=" * 60)
    
    public_dir = Path('public')
    html_files = [
        'index.html',
        'governo.html',
        'empresas.html',
        'pessoas.html',
        'como-funciona.html',
        'seguranca.html'
    ]
    
    total_fixed = 0
    for filename in html_files:
        file_path = public_dir / filename
        if file_path.exists():
            if fix_cta_buttons(file_path):
                total_fixed += 1
        else:
            print(f"\n⚠️  Arquivo não encontrado: {filename}")
    
    print("\n" + "=" * 60)
    print(f"✅ CONCLUÍDO: {total_fixed} arquivos corrigidos")
    print("\n📋 Chave i18n correta: global.accessPlatform")
    print("   • PT: 'Acessar Plataforma'")
    print("   • EN: 'Access Platform'")
    print("   • ES: 'Acceder a la Plataforma'")

if __name__ == '__main__':
    main()
