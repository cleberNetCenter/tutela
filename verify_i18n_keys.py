#!/usr/bin/env python3
"""
Verifica se todas as chaves data-i18n do HTML existem nos arquivos JSON
"""
import re
import json
from pathlib import Path

def extract_i18n_keys_from_html(html_file):
    """Extrai todas as chaves data-i18n do HTML"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar todas as ocorrências de data-i18n="..."
    pattern = r'data-i18n="([^"]+)"'
    keys = re.findall(pattern, content)
    
    # Filtrar apenas chaves que começam com "security."
    security_keys = [k for k in keys if k.startswith('security.')]
    
    return sorted(set(security_keys))

def check_translation_coverage(lang_code):
    """Verifica se todas as chaves existem no arquivo de tradução"""
    json_file = Path(f'public/assets/lang/{lang_code}.json')
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    security_section = data.get('security', {})
    
    return security_section

def main():
    """Verifica cobertura de traduções"""
    print("🔍 VERIFICANDO COBERTURA DE TRADUÇÕES - seguranca.html")
    print("=" * 70)
    
    # Extrair chaves do HTML
    html_keys = extract_i18n_keys_from_html('public/seguranca.html')
    
    print(f"\n📄 Chaves data-i18n encontradas no HTML: {len(html_keys)}")
    for key in html_keys:
        print(f"   • {key}")
    
    # Verificar cada idioma
    for lang in ['pt', 'en', 'es']:
        print(f"\n🌐 Verificando idioma: {lang.upper()}")
        translations = check_translation_coverage(lang)
        
        print(f"   Traduções disponíveis: {len(translations)} chaves")
        
        # Verificar quais chaves estão faltando
        missing = []
        for key in html_keys:
            # Remover prefixo "security."
            key_name = key.replace('security.', '')
            if key_name not in translations:
                missing.append(key)
        
        if missing:
            print(f"   ❌ FALTANDO {len(missing)} traduções:")
            for key in missing:
                print(f"      • {key}")
        else:
            print(f"   ✅ Todas as traduções disponíveis")
    
    print("\n" + "=" * 70)

if __name__ == '__main__':
    main()
