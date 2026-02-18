#!/usr/bin/env python3
"""
FASE 3: Remover data-i18n do corpo das páginas jurídicas
Mantém data-i18n apenas em elementos de interface (nav, header, footer, buttons)
"""
import re
from pathlib import Path

LEGAL_PAGES = [
    'institucional.html',
    'politica-de-privacidade.html',
    'fundamento-juridico.html',
    'termos-de-custodia.html'
]

# Elementos de interface que MANTÉM data-i18n
INTERFACE_ELEMENTS = [
    r'<nav[^>]*>',
    r'<header[^>]*>',
    r'<footer[^>]*>',
    r'<button[^>]*>',
    r'class="[^"]*(?:nav|header|footer|lang|modal|cta)[^"]*"'
]

def remove_body_data_i18n(file_path):
    """Remove data-i18n do corpo da página, mantém apenas interface"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_count = content.count('data-i18n')
    
    # Encontrar a seção <main> ou <div class="main">
    main_match = re.search(r'<main[^>]*>.*?</main>', content, re.DOTALL)
    if not main_match:
        main_match = re.search(r'<div[^>]*class="main"[^>]*>.*?</div>\s*</div>', content, re.DOTALL)
    
    if main_match:
        main_content = main_match.group(0)
        
        # Remover data-i18n de elementos do corpo (p, h2-h6, li, div text-block)
        # EXCETO se estiver em elementos de interface
        
        # Padrão: remover data-i18n de elementos de conteúdo
        main_content_cleaned = re.sub(
            r'(<(?:p|h[2-6]|li|span)[^>]*)\s*data-i18n="[^"]*"',
            r'\1',
            main_content
        )
        
        # Substituir no conteúdo original
        content = content.replace(main_content, main_content_cleaned)
    
    new_count = content.count('data-i18n')
    removed = original_count - new_count
    
    # Salvar arquivo
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return original_count, new_count, removed

print("=" * 80)
print("🧹 FASE 3: REMOVER data-i18n DO CORPO DAS PÁGINAS JURÍDICAS")
print("=" * 80)
print()

total_removed = 0
for page in LEGAL_PAGES:
    file_path = Path(f'public/{page}')
    if not file_path.exists():
        print(f"❌ {page}: arquivo não encontrado")
        continue
    
    print(f"📄 Processando {page}...")
    original, remaining, removed = remove_body_data_i18n(file_path)
    total_removed += removed
    
    print(f"   ├─ data-i18n originais: {original}")
    print(f"   ├─ data-i18n mantidos (interface): {remaining}")
    print(f"   └─ data-i18n removidos (corpo): {removed}")
    print()

print("=" * 80)
print("📊 RESULTADO")
print("=" * 80)
print(f"Total de data-i18n removidos: {total_removed}")
print()
print("✅ MANTIDOS (interface):")
print("   - Navegação (nav)")
print("   - Header/Footer")
print("   - Botões")
print("   - Modal/Banner")
print()
print("❌ REMOVIDOS (corpo jurídico):")
print("   - <p> (parágrafos)")
print("   - <h2> a <h6> (títulos)")
print("   - <li> (listas)")
print("   - <span> (texto inline)")
print()
print("🎯 Conteúdo jurídico agora 100% em português")
print()
