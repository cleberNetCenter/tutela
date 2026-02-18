#!/usr/bin/env python3
"""
FASE 1: Limpar JSON EN/ES
Remove objetos jurídicos, mantém apenas interface/navegação
"""
import json
from pathlib import Path

# Chaves a serem REMOVIDAS (conteúdo jurídico)
KEYS_TO_REMOVE = [
    'institutional',  # textos longos jurídicos
    'institucional',  # textos longos jurídicos
    'terms',          # termos de custódia completos
    'privacy',        # política de privacidade completa
    'legalBasis',     # fundamento jurídico completo
    'preservation'    # se contém textos longos jurídicos
]

# Chaves a MANTER (interface e navegação)
KEYS_TO_KEEP = [
    'global',
    'navigation',
    'modal',
    'home',
    'howItWorks',
    'security',
    'government',
    'companies',
    'individuals'
]

def clean_json_file(file_path):
    """Remove chaves jurídicas, mantém interface"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    original_keys = set(data.keys())
    
    # Remover chaves jurídicas
    for key in KEYS_TO_REMOVE:
        if key in data:
            del data[key]
            print(f"  ✅ Removido: {key}")
    
    # Verificar o que sobrou
    remaining_keys = set(data.keys())
    removed_keys = original_keys - remaining_keys
    
    # Salvar JSON limpo
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return len(original_keys), len(remaining_keys), removed_keys

print("=" * 80)
print("🧹 FASE 1: LIMPEZA DOS JSON EN/ES")
print("=" * 80)
print()

for lang in ['en', 'es']:
    file_path = Path(f'public/assets/lang/{lang}.json')
    print(f"📄 Processando {lang}.json...")
    
    original_count, remaining_count, removed = clean_json_file(file_path)
    
    print(f"   ├─ Chaves originais: {original_count}")
    print(f"   ├─ Chaves mantidas: {remaining_count}")
    print(f"   ├─ Chaves removidas: {len(removed)}")
    print(f"   └─ Lista: {', '.join(sorted(removed))}")
    print()

print("=" * 80)
print("📊 RESULTADO")
print("=" * 80)
print()
print("✅ Chaves MANTIDAS (interface):")
for key in KEYS_TO_KEEP:
    print(f"   - {key}")
print()
print("❌ Chaves REMOVIDAS (jurídico):")
for key in KEYS_TO_REMOVE:
    print(f"   - {key}")
print()
print("🎯 Estratégia:")
print("   - Páginas jurídicas permanecem 100% em português")
print("   - Interface (menu, botões) continua multilíngue")
print("   - Sem tradução client-side de textos legais")
print()
