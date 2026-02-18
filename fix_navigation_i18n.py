#!/usr/bin/env python3
"""
Fix navigation i18n attributes to use correct keys
"""

from pathlib import Path

PUBLIC_DIR = Path('public')
LEGAL_DIR = PUBLIC_DIR / 'legal'

def fix_navigation_in_file(file_path):
    """Fix navigation i18n keys in a single file"""
    content = file_path.read_text(encoding='utf-8')
    original_content = content
    
    # Fix the dropdown menu
    # Change data-i18n="nav_legal_base" to data-i18n="navigation.legal_base"
    content = content.replace('data-i18n="nav_legal_base"', 'data-i18n="navigation.legal_base"')
    
    # Fix institucional
    # Change data-i18n="nav_institucional" to data-i18n="navigation.institucional"
    content = content.replace('data-i18n="nav_institucional"', 'data-i18n="navigation.institucional"')
    
    # Fix privacy
    # Change data-i18n="nav_privacy" to data-i18n="navigation.privacy"
    content = content.replace('data-i18n="nav_privacy"', 'data-i18n="navigation.privacy"')
    
    if content != original_content:
        file_path.write_text(content, encoding='utf-8')
        return True
    return False

def main():
    """Fix all HTML files"""
    print("\n" + "="*70)
    print("🔧 CORRIGINDO CHAVES i18n DA NAVEGAÇÃO")
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
    print("  nav_legal_base → navigation.legal_base")
    print("  nav_institucional → navigation.institucional")
    print("  nav_privacy → navigation.privacy")

if __name__ == '__main__':
    main()
