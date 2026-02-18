#!/usr/bin/env python3
"""
Remove SPA - Converte navegação SPA para links MPA reais
"""

import re
from pathlib import Path

PUBLIC_DIR = Path('public')

print("\n" + "="*60)
print("REMOVENDO NAVEGAÇÃO SPA")
print("="*60)

# Arquivos HTML para processar
html_files = [
    PUBLIC_DIR / 'index.html',
    PUBLIC_DIR / 'como-funciona.html',
    PUBLIC_DIR / 'seguranca.html',
    PUBLIC_DIR / 'governo.html',
    PUBLIC_DIR / 'empresas.html',
    PUBLIC_DIR / 'pessoas.html',
]

def remove_spa_from_file(filepath):
    """Remove lógica SPA e converte para MPA"""
    if not filepath.exists():
        print(f"⏭️  Ignorado: {filepath} (não existe)")
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes = []
    
    # 1. Remover <script src="/assets/js/navigation.js"></script>
    if 'navigation.js' in content:
        content = re.sub(r'<script\s+src="/assets/js/navigation\.js"[^>]*></script>', '', content)
        changes.append("Removido navigation.js")
    
    # 2. Converter onclick="navigateTo('page')" para href="/page.html"
    # Pattern: onclick="navigateTo('como-funciona'); return false;"
    pattern_navigateTo = r'onclick="navigateTo\(\'([^\']+)\'\);?\s*return\s+false;"'
    matches = re.findall(pattern_navigateTo, content)
    if matches:
        for page in matches:
            # Determinar URL correta
            if page == 'home':
                url = '/'
            else:
                url = f'/{page}.html'
            
            # Substituir onclick por href (mantendo href="#" existente ou adicionando)
            old_pattern = f'href="#" onclick="navigateTo(\'{page}\'); return false;"'
            new_href = f'href="{url}"'
            
            if old_pattern in content:
                content = content.replace(old_pattern, new_href)
            else:
                # Caso alternativo: onclick sem href="#"
                content = re.sub(
                    rf'onclick="navigateTo\(\'{page}\'\);?\s*return\s+false;"',
                    f'href="{url}"',
                    content
                )
        
        changes.append(f"Convertido {len(matches)} navigateTo() para href")
    
    # 3. Remover data-page attributes
    if 'data-page=' in content:
        content = re.sub(r'\s*data-page="[^"]*"', '', content)
        changes.append("Removido data-page attributes")
    
    # 4. Remover classes .page e .active da estrutura SPA
    # <div class="page active" id="page-home"> → <div id="page-home">
    content = re.sub(r'class="page\s+active"', 'class="content"', content)
    content = re.sub(r'class="page"', 'class="content"', content)
    
    # 5. Remover data-i18n="nav_..." para navegação
    content = re.sub(r'data-i18n="nav_[^"]*"', '', content)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Atualizado: {filepath.name}")
        for change in changes:
            print(f"   - {change}")
    else:
        print(f"⏭️  Sem mudanças: {filepath.name}")

# Processar arquivos
for filepath in html_files:
    remove_spa_from_file(filepath)

print("\n✅ NAVEGAÇÃO SPA REMOVIDA")
print("="*60)
