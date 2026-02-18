#!/usr/bin/env python3
"""
Remove hreflang inválidos (EN/ES) de páginas que não têm versões separadas
Mantém apenas pt-br e x-default
"""
import re
from pathlib import Path

# Páginas que precisam correção (não têm /en/ e /es/)
pages = [
    'institucional.html',
    'politica-de-privacidade.html',
    'fundamento-juridico.html',
    'termos-de-custodia.html',
    'como-funciona.html',
    'seguranca.html',
    'preservacao-probatoria-digital.html'
]

def fix_hreflang(file_path):
    """Remove hreflang EN/ES inválidos, mantém PT-BR e x-default"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    page_name = file_path.name
    
    # Remove linhas hreflang EN
    content = re.sub(
        r'<link rel="alternate" hreflang="en" href="https://tuteladigital\.com\.br/en/[^"]+"/>\n',
        '',
        content
    )
    
    # Remove linhas hreflang ES
    content = re.sub(
        r'<link rel="alternate" hreflang="es" href="https://tuteladigital\.com\.br/es/[^"]+"/>\n',
        '',
        content
    )
    
    # Contar quantas foram removidas
    removed = original_content.count('hreflang="en"') + original_content.count('hreflang="es"')
    remaining = content.count('hreflang')
    
    if removed > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {page_name}: removidos {removed} hreflang inválidos, mantidos {remaining}")
        return True
    else:
        print(f"⚠️  {page_name}: nenhum hreflang EN/ES encontrado")
        return False

print("=" * 80)
print("🔧 REMOVENDO HREFLANG INVÁLIDOS (EN/ES)")
print("=" * 80)
print()

fixed_count = 0
for page in pages:
    file_path = Path(f'public/{page}')
    if file_path.exists():
        if fix_hreflang(file_path):
            fixed_count += 1
    else:
        print(f"❌ {page}: arquivo não encontrado")

print()
print("=" * 80)
print("📊 RESUMO")
print("=" * 80)
print(f"Total de páginas processadas: {len(pages)}")
print(f"Páginas corrigidas: {fixed_count}")
print()
print("✅ Hreflang mantidos (válidos):")
print("   - pt-br: https://tuteladigital.com.br/{page}.html")
print("   - x-default: https://tuteladigital.com.br/{page}.html")
print()
print("❌ Hreflang removidos (inválidos - 404):")
print("   - en: https://tuteladigital.com.br/en/{page}.html")
print("   - es: https://tuteladigital.com.br/es/{page}.html")
print()
