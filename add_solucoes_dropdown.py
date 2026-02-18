#!/usr/bin/env python3
"""
Adiciona dropdown Soluções mantendo estrutura existente
"""

import re
from pathlib import Path

PUBLIC_DIR = Path('public')

print("\n" + "="*60)
print("ADICIONANDO DROPDOWN SOLUÇÕES AO MENU")
print("="*60)

# Novo menu com dropdown Soluções
novo_menu = '''<nav class="nav" id="nav">
<a class="nav-link" href="/">Início</a>
<a class="nav-link" href="/como-funciona.html">Como Funciona</a>
<a class="nav-link" href="/seguranca.html">Segurança</a>

<li class="nav-dropdown">
<a href="#">Soluções</a>
<ul class="dropdown-menu">
<li><a href="/governo.html">Governo</a></li>
<li><a href="/empresas.html">Empresas</a></li>
<li><a href="/pessoas.html">Pessoas</a></li>
</ul>
</li>

<li class="nav-dropdown">
<a href="#">Base Jurídica</a>
<ul class="dropdown-menu">
<li><a href="/legal/preservacao-probatoria-digital.html">Preservação Probatória</a></li>
<li><a href="/legal/fundamento-juridico.html">Fundamento Jurídico</a></li>
<li><a href="/legal/termos-de-custodia.html">Termos de Custódia</a></li>
<li><a href="/legal/politica-de-privacidade.html">Política de Privacidade</a></li>
<li><a href="/legal/institucional.html">Institucional</a></li>
</ul>
</li>
</nav>'''

arquivos = [
    PUBLIC_DIR / 'index.html',
    PUBLIC_DIR / 'como-funciona.html',
    PUBLIC_DIR / 'seguranca.html',
    PUBLIC_DIR / 'governo.html',
    PUBLIC_DIR / 'empresas.html',
    PUBLIC_DIR / 'pessoas.html',
]

# Adicionar páginas legais
arquivos.extend(list((PUBLIC_DIR / 'legal').glob('*.html')))

def atualizar_menu(filepath):
    """Substitui o menu inteiro"""
    if not filepath.exists():
        print(f"⚠️  Não existe: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern: <nav class="nav" id="nav"> até </nav>
    pattern = r'<nav class="nav"[^>]*>.*?</nav>'
    
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, novo_menu, content, flags=re.DOTALL)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {filepath.name}")
        return True
    else:
        print(f"⏭️  Sem <nav>: {filepath.name}")
        return False

# Atualizar arquivos
print("\nAtualizando arquivos...")
count = 0
for arquivo in arquivos:
    if atualizar_menu(arquivo):
        count += 1

print(f"\n✅ {count} arquivos atualizados")
print("="*60)
print("\n📋 MENU FINAL:")
print("  • Início")
print("  • Como Funciona")
print("  • Segurança")
print("  • Soluções ▼")
print("     - Governo")
print("     - Empresas")
print("     - Pessoas")
print("  • Base Jurídica ▼")
print("     - Preservação Probatória")
print("     - Fundamento Jurídico")
print("     - Termos de Custódia")
print("     - Política de Privacidade")
print("     - Institucional")
print("="*60)
