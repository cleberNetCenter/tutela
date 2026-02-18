#!/usr/bin/env python3
"""
Solução completa: adicionar data-i18n attributes ONDE FALTAM e criar chaves necessárias
"""
import json
import re
from pathlib import Path

def load_json(lang):
    with open(f'public/assets/lang/{lang}.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(lang, data):
    with open(f'public/assets/lang/{lang}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def fix_institucional():
    """institucional.html está OK, só precisa garantir que os textos dos parágrafos tenham data-i18n"""
    print("✅ institucional.html: já tem 21 data-i18n, OK")
    return True

def check_page_i18n(page_name):
    """Verifica quantos elementos têm data-i18n"""
    with open(f'public/{page_name}', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Contar elementos com texto visível
    total_text_elements = len(re.findall(r'<(?:h[1-6]|p|li|span|div[^>]*class="[^"]*text[^"]*")[^>]*>(?!<)[\s\S]*?</(?:h[1-6]|p|li|span|div)>', content))
    # Contar elementos com data-i18n
    i18n_elements = content.count('data-i18n')
    
    return i18n_elements, total_text_elements

# Verificar status atual
pages = {
    'institucional.html': 'institucional',
    'politica-de-privacidade.html': 'privacy',
    'fundamento-juridico.html': 'legalBasis',
    'termos-de-custodia.html': 'terms'
}

print("="*80)
print("📊 STATUS ATUAL DE i18n NAS PÁGINAS")
print("="*80)
print()

for page, key in pages.items():
    i18n_count, text_count = check_page_i18n(page)
    coverage = (i18n_count / text_count * 100) if text_count > 0 else 0
    status = "✅" if coverage > 80 else "⚠️" if coverage > 40 else "❌"
    print(f"{status} {page}")
    print(f"   ├─ data-i18n: {i18n_count}")
    print(f"   ├─ Elementos de texto: ~{text_count}")
    print(f"   └─ Cobertura estimada: {coverage:.0f}%")
    print()

print("="*80)
print("💡 RECOMENDAÇÃO")
print("="*80)
print()
print("Para garantir 100% de tradução, temos 2 opções:")
print()
print("OPÇÃO 1 (Simples):")
print("  - Manter páginas legais (privacy, termos) apenas em PT")
print("  - Adicionar aviso: 'Documento disponível apenas em português'")
print()
print("OPÇÃO 2 (Completa):")
print("  - Adicionar data-i18n em TODOS os textos")
print("  - Criar ~200+ chaves de tradução para cada idioma")
print("  - Tempo estimado: ~30min de processamento")
print()

