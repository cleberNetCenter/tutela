#!/usr/bin/env python3
"""
Fix all dropdown i18n attributes to use correct navigation keys
"""

from pathlib import Path

PUBLIC_DIR = Path('public')
LEGAL_DIR = PUBLIC_DIR / 'legal'

def fix_navigation_in_file(file_path):
    """Fix navigation i18n keys in a single file"""
    content = file_path.read_text(encoding='utf-8')
    original_content = content
    
    # Fix all navigation keys
    replacements = [
        ('data-i18n="nav_preservacao"', 'data-i18n="navigation.preservation"'),
        ('data-i18n="nav_fundamento"', 'data-i18n="navigation.legalBasis"'),
        ('data-i18n="nav_termos"', 'data-i18n="navigation.terms"'),
    ]
    
    for old, new in replacements:
        content = content.replace(old, new)
    
    if content != original_content:
        file_path.write_text(content, encoding='utf-8')
        return True
    return False

def main():
    """Fix all HTML files"""
    print("\n" + "="*70)
    print("🔧 CORRIGINDO TODAS AS CHAVES i18n DO DROPDOWN")
    print("="*70)
    
    fixed_count = 0
    
    # Fix root HTML files
    for html_file in PUBLIC_DIR.glob('*.html'):
        if fix_navigation_in_file(html_file):
            print(f"✅ Corrigido: {html_file.name}")
            fixed_count += 1
    
    # Fix legal HTML files  
    for html_file in LEGAL_DIR.glob('*.html'):
        if fix_navigation_in_file(html_file):
            print(f"✅ Corrigido: legal/{html_file.name}")
            fixed_count += 1
    
    print(f"\n✅ Total de arquivos corrigidos: {fixed_count}")
    
    print("\n" + "="*70)
    print("✅ CORREÇÃO COMPLETA")
    print("="*70)
    
    print("\nChaves corrigidas:")
    print("  nav_preservacao → navigation.preservation")
    print("  nav_fundamento → navigation.legalBasis")
    print("  nav_termos → navigation.terms")

if __name__ == '__main__':
    main()
