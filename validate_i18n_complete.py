#!/usr/bin/env python3
"""
Script de validação COMPLETA do sistema i18n
Valida TODAS as chaves antes do deploy
"""

import json
import re
import sys

def validate_json_files():
    """Valida que os arquivos JSON são válidos"""
    print("🔍 Validando arquivos JSON...")
    
    langs = ['pt', 'en', 'es']
    json_data = {}
    
    for lang in langs:
        file_path = f'public/assets/lang/{lang}.json'
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json_data[lang] = json.load(f)
                print(f"  ✅ {lang}.json: válido ({len(json_data[lang])} seções)")
        except json.JSONDecodeError as e:
            print(f"  ❌ {lang}.json: ERRO DE SINTAXE - {e}")
            return False, None
        except FileNotFoundError:
            print(f"  ❌ {lang}.json: arquivo não encontrado")
            return False, None
    
    return True, json_data

def extract_keymap_from_js():
    """Extrai o keyMap do i18n.js"""
    print("\n🔍 Extraindo keyMap do i18n.js...")
    
    with open('public/assets/js/i18n.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extrai o objeto keyMap
    keymap_match = re.search(r'keyMap:\s*\{(.*?)\},\s*\/\*\*', content, re.DOTALL)
    
    if not keymap_match:
        print("  ❌ Não foi possível extrair keyMap")
        return None
    
    keymap_str = keymap_match.group(1)
    
    # Parse manual das linhas do keyMap
    keymap = {}
    for line in keymap_str.split('\n'):
        match = re.search(r"'([^']+)':\s*'([^']+)'", line)
        if match:
            keymap[match.group(1)] = match.group(2)
    
    print(f"  ✅ keyMap extraído: {len(keymap)} mapeamentos")
    return keymap

def extract_data_i18n_from_html():
    """Extrai todas as chaves data-i18n do HTML"""
    print("\n🔍 Extraindo chaves data-i18n dos HTMLs...")
    
    import glob
    
    html_files = glob.glob('public/*.html') + glob.glob('public/legal/*.html')
    all_keys = set()
    
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            keys = re.findall(r'data-i18n="([^"]+)"', content)
            all_keys.update(keys)
    
    print(f"  ✅ Chaves encontradas: {len(all_keys)}")
    return all_keys

def resolve_key(key, keymap, json_data, lang):
    """Resolve uma chave usando o keyMap e retorna a tradução"""
    
    # 1. Verifica se existe mapeamento
    mapped_key = keymap.get(key, key)
    
    # 2. Se a chave tem ponto, navega pelo objeto
    if '.' in mapped_key:
        parts = mapped_key.split('.')
        value = json_data[lang]
        
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return None
        
        return value
    
    # 3. Chave simples
    return json_data[lang].get(mapped_key)

def validate_all_keys():
    """Validação completa de todas as chaves"""
    
    print("=" * 60)
    print("🔍 VALIDAÇÃO COMPLETA DO SISTEMA I18N")
    print("=" * 60)
    
    # 1. Validar JSON
    valid, json_data = validate_json_files()
    if not valid:
        return False
    
    # 2. Extrair keyMap
    keymap = extract_keymap_from_js()
    if not keymap:
        return False
    
    # 3. Extrair chaves do HTML
    html_keys = extract_data_i18n_from_html()
    
    # 4. Validar cada chave em cada idioma
    print("\n🔍 Validando traduções das chaves HTML...")
    
    missing_keys = {
        'pt': [],
        'en': [],
        'es': []
    }
    
    for key in sorted(html_keys):
        print(f"\n  Chave: {key}")
        
        for lang in ['pt', 'en', 'es']:
            translation = resolve_key(key, keymap, json_data, lang)
            
            if translation:
                # Truncar tradução longa
                display = translation if len(translation) <= 60 else translation[:60] + '...'
                print(f"    ✅ {lang.upper()}: {display}")
            else:
                print(f"    ❌ {lang.upper()}: TRADUÇÃO AUSENTE")
                missing_keys[lang].append(key)
    
    # 5. Validar especificamente home_applicability
    print("\n" + "=" * 60)
    print("🎯 VALIDAÇÃO ESPECIAL: home_applicability")
    print("=" * 60)
    
    for key in ['home_applicability_title', 'home_applicability_desc']:
        print(f"\n  Chave: {key}")
        
        # Verifica mapeamento
        mapped = keymap.get(key, key)
        print(f"    🔀 Mapeado para: {mapped}")
        
        for lang in ['pt', 'en', 'es']:
            translation = resolve_key(key, keymap, json_data, lang)
            
            if translation:
                display = translation if len(translation) <= 100 else translation[:100] + '...'
                print(f"    ✅ {lang.upper()}: {display}")
            else:
                print(f"    ❌ {lang.upper()}: TRADUÇÃO AUSENTE")
                missing_keys[lang].append(key)
    
    # 6. Resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO DA VALIDAÇÃO")
    print("=" * 60)
    
    total_missing = sum(len(keys) for keys in missing_keys.values())
    
    if total_missing == 0:
        print("✅ TODAS AS CHAVES TÊM TRADUÇÕES!")
        print(f"   - Total de chaves validadas: {len(html_keys)}")
        print(f"   - Idiomas: PT, EN, ES")
        print(f"   - Mapeamentos no keyMap: {len(keymap)}")
        return True
    else:
        print(f"❌ ENCONTRADAS {total_missing} TRADUÇÕES AUSENTES!")
        for lang, keys in missing_keys.items():
            if keys:
                print(f"\n  {lang.upper()} ({len(keys)} ausentes):")
                for key in keys[:10]:  # mostrar apenas primeiras 10
                    print(f"    - {key}")
                if len(keys) > 10:
                    print(f"    ... e mais {len(keys) - 10}")
        return False

if __name__ == "__main__":
    success = validate_all_keys()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ VALIDAÇÃO COMPLETA: SUCESSO")
        print("=" * 60)
        print("\n🚀 Sistema i18n está correto e pronto para deploy!")
        sys.exit(0)
    else:
        print("❌ VALIDAÇÃO COMPLETA: FALHA")
        print("=" * 60)
        print("\n⚠️  Corrija os erros antes do deploy!")
        sys.exit(1)
