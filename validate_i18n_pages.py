#!/usr/bin/env python3
"""
Script para validar se todas as páginas HTML têm i18n corretamente implementado
"""
import re
from pathlib import Path

def analyze_html_page(file_path):
    """Analisa uma página HTML para verificar implementação i18n"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    results = {
        'file': file_path.name,
        'has_i18n_script': bool(re.search(r'<script[^>]*src=["\'].*i18n\.js["\']', content)),
        'data_i18n_count': len(re.findall(r'data-i18n=["\'][^"\']+["\']', content)),
        'lang_buttons': len(re.findall(r'data-lang=["\'][a-z]{2}["\']', content)),
        'hardcoded_pt_text': [],
        'has_lang_selector': bool(re.search(r'lang-option|language-selector', content)),
    }
    
    # Procurar por textos hard-coded em português (comum em textos longos)
    # Busca por parágrafos ou divs com texto português típico
    hardcoded_patterns = [
        r'<h[1-6][^>]*>(?!.*data-i18n)[^<]*(?:preservação|custódia|jurídico|segurança|institucional)[^<]*</h[1-6]>',
        r'<p[^>]*>(?!.*data-i18n)[^<]{100,}(?:preservação|custódia|digital|jurídico|probatória)[^<]*</p>',
        r'<div[^>]*class=["\'][^"\']*(?:content|section)[^"\']*["\'][^>]*>(?!.*data-i18n)[^<]{50,}(?:preservação|custódia)[^<]*</div>',
    ]
    
    for pattern in hardcoded_patterns:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            text_preview = match.group(0)[:150] + '...' if len(match.group(0)) > 150 else match.group(0)
            results['hardcoded_pt_text'].append(text_preview)
    
    # Verificar seções específicas problemáticas
    sections_to_check = [
        (r'<section[^>]*id=["\']termos[^>]*>(.*?)</section>', 'Termos section'),
        (r'<section[^>]*id=["\']privacidade[^>]*>(.*?)</section>', 'Privacidade section'),
        (r'<section[^>]*id=["\']institucional[^>]*>(.*?)</section>', 'Institucional section'),
    ]
    
    for pattern, section_name in sections_to_check:
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            section_content = match.group(1)
            # Verificar se há textos longos sem data-i18n
            long_texts = re.findall(r'<(?:p|div|h[1-6])[^>]*>(?!.*data-i18n)([^<]{80,})</(?:p|div|h[1-6])>', section_content)
            if long_texts:
                results['hardcoded_pt_text'].append(f"{section_name}: {len(long_texts)} textos longos sem data-i18n")
    
    return results

def main():
    public_dir = Path('public')
    html_files = [
        'index.html',
        'como-funciona.html',
        'fundamento-juridico.html',
        'institucional.html',
        'politica-de-privacidade.html',
        'preservacao-probatoria-digital.html',
        'seguranca.html',
        'termos-de-custodia.html'
    ]
    
    print("=" * 80)
    print("🔍 VALIDAÇÃO DE IMPLEMENTAÇÃO i18n - TODAS AS PÁGINAS")
    print("=" * 80)
    print()
    
    issues_found = []
    
    for html_file in html_files:
        file_path = public_dir / html_file
        if not file_path.exists():
            print(f"⚠️  {html_file}: ARQUIVO NÃO ENCONTRADO")
            issues_found.append(html_file)
            continue
        
        result = analyze_html_page(file_path)
        
        # Status da página
        has_issues = False
        status_icon = "✅"
        
        if not result['has_i18n_script']:
            status_icon = "❌"
            has_issues = True
        elif result['data_i18n_count'] < 5:
            status_icon = "⚠️ "
            has_issues = True
        elif result['hardcoded_pt_text']:
            status_icon = "⚠️ "
            has_issues = True
        
        print(f"{status_icon} {result['file']}")
        print(f"   ├─ i18n.js carregado: {'✅ Sim' if result['has_i18n_script'] else '❌ NÃO'}")
        print(f"   ├─ Atributos data-i18n: {result['data_i18n_count']}")
        print(f"   ├─ Botões de idioma: {result['lang_buttons']}")
        print(f"   └─ Seletor de idioma: {'✅ Sim' if result['has_lang_selector'] else '❌ NÃO'}")
        
        if result['hardcoded_pt_text']:
            print(f"   ⚠️  POSSÍVEL CONTEÚDO HARD-CODED:")
            for i, text in enumerate(result['hardcoded_pt_text'][:3], 1):  # Limitar a 3 exemplos
                print(f"      {i}. {text[:100]}...")
            if len(result['hardcoded_pt_text']) > 3:
                print(f"      ... e mais {len(result['hardcoded_pt_text']) - 3} ocorrências")
        
        if has_issues:
            issues_found.append(html_file)
        
        print()
    
    print("=" * 80)
    print("📊 RESUMO DA VALIDAÇÃO")
    print("=" * 80)
    print(f"Total de páginas analisadas: {len(html_files)}")
    print(f"Páginas com problemas: {len(issues_found)}")
    
    if issues_found:
        print(f"\n⚠️  PÁGINAS QUE PRECISAM DE CORREÇÃO:")
        for page in issues_found:
            print(f"   - {page}")
    else:
        print("\n✅ TODAS AS PÁGINAS ESTÃO OK!")
    
    print()

if __name__ == "__main__":
    main()
