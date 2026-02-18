#!/usr/bin/env python3
"""
Convert index-en.html and index-es.html to use i18n.js system

These files currently have static translated content.
We need to replace them with the PT version + i18n.js
so translations happen dynamically.
"""

import shutil
from pathlib import Path

PUBLIC_DIR = Path('public')

def backup_files():
    """Backup EN and ES versions"""
    print("\n" + "="*70)
    print("CRIANDO BACKUP DAS VERSÕES TRADUZIDAS")
    print("="*70)
    
    for lang in ['en', 'es']:
        source = PUBLIC_DIR / f'index-{lang}.html'
        backup = PUBLIC_DIR / f'index-{lang}.html.backup'
        
        if source.exists():
            shutil.copy(source, backup)
            print(f"✅ Backup criado: {backup.name}")

def create_dynamic_versions():
    """
    Create dynamic i18n versions of index-en.html and index-es.html
    by copying index.html and setting the correct lang attribute
    """
    print("\n" + "="*70)
    print("CRIANDO VERSÕES DINÂMICAS COM i18n.js")
    print("="*70)
    
    # Read PT version (which already has i18n)
    index_pt = PUBLIC_DIR / 'index.html'
    content_pt = index_pt.read_text(encoding='utf-8')
    
    # Create EN version
    content_en = content_pt.replace('<html lang="pt-BR">', '<html lang="en">')
    content_en = content_en.replace(
        "gtag('config', 'G-KXVB267PYJ');",
        "gtag('config', 'G-KXVB267PYJ');\n  // Auto-set language to English\n  localStorage.setItem('preferredLanguage', 'en');"
    )
    
    index_en = PUBLIC_DIR / 'index-en.html'
    index_en.write_text(content_en, encoding='utf-8')
    print(f"✅ Criado: index-en.html (com i18n.js + auto-switch para EN)")
    
    # Create ES version
    content_es = content_pt.replace('<html lang="pt-BR">', '<html lang="es">')
    content_es = content_es.replace(
        "gtag('config', 'G-KXVB267PYJ');",
        "gtag('config', 'G-KXVB267PYJ');\n  // Auto-set language to Spanish\n  localStorage.setItem('preferredLanguage', 'es');"
    )
    
    index_es = PUBLIC_DIR / 'index-es.html'
    index_es.write_text(content_es, encoding='utf-8')
    print(f"✅ Criado: index-es.html (com i18n.js + auto-switch para ES)")

def main():
    """Execute conversion"""
    print("\n" + "="*70)
    print("🔄 CONVERTENDO index-en/es.html PARA SISTEMA i18n DINÂMICO")
    print("="*70)
    
    backup_files()
    create_dynamic_versions()
    
    print("\n" + "="*70)
    print("✅ CONVERSÃO COMPLETA")
    print("="*70)
    
    print("\n📋 MUDANÇAS REALIZADAS:")
    print("✅ index-en.html → agora usa i18n.js (tradução dinâmica)")
    print("✅ index-es.html → agora usa i18n.js (tradução dinâmica)")
    print("✅ localStorage define idioma automaticamente ao acessar")
    print("✅ Backups das versões antigas criados (.backup)")
    
    print("\n🎯 RESULTADO:")
    print("Todas as seções (Government, Companies, Individuals, How It Works,")
    print("Security) agora serão traduzidas automaticamente em EN/ES usando")
    print("as chaves do i18n JSON.")
    
    print("\n⚠️  IMPORTANTE:")
    print("As versões antigas (estáticas) foram salvas como .backup")
    print("Caso necessário reverter, renomeie os arquivos .backup")

if __name__ == '__main__':
    main()
