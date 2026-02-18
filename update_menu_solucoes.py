#!/usr/bin/env python3
"""
Adiciona menu dropdown 'Soluções' em todas as páginas
"""

import re
from pathlib import Path

PUBLIC_DIR = Path('public')

print("\n" + "="*60)
print("ATUALIZANDO MENU: DROPDOWN SOLUÇÕES")
print("="*60)

# Menu completo com dropdown Soluções
menu_completo = '''        <nav class="nav">
            <a href="/" class="nav-link">Início</a>
            <a href="/como-funciona.html" class="nav-link">Como Funciona</a>
            <a href="/seguranca.html" class="nav-link">Segurança</a>
            
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

# Arquivos para atualizar
arquivos_pt = [
    PUBLIC_DIR / 'index.html',
    PUBLIC_DIR / 'como-funciona.html',
    PUBLIC_DIR / 'seguranca.html',
    PUBLIC_DIR / 'governo.html',
    PUBLIC_DIR / 'empresas.html',
    PUBLIC_DIR / 'pessoas.html',
]

arquivos_legal = list((PUBLIC_DIR / 'legal').glob('*.html'))

def atualizar_menu(filepath, menu_html):
    """Atualiza o menu em um arquivo HTML"""
    if not filepath.exists():
        print(f"⚠️  Não encontrado: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Procurar <nav class="nav"> ... </nav>
    pattern = r'<nav class="nav">.*?</nav>'
    
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, menu_html, content, flags=re.DOTALL)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Atualizado: {filepath.name}")
        return True
    else:
        print(f"⚠️  Menu não encontrado: {filepath.name}")
        return False

# Atualizar páginas PT
print("\n[1] Atualizando páginas PT...")
for arquivo in arquivos_pt:
    atualizar_menu(arquivo, menu_completo)

# Atualizar páginas legais
print("\n[2] Atualizando páginas legais...")
for arquivo in arquivos_legal:
    atualizar_menu(arquivo, menu_completo)

print("\n✅ MENU DROPDOWN SOLUÇÕES ADICIONADO")
print("="*60)
print("\nMENU FINAL:")
print("  Início")
print("  Como Funciona")
print("  Segurança")
print("  Soluções ▼")
print("    ├─ Governo")
print("    ├─ Empresas")
print("    └─ Pessoas")
print("  Base Jurídica ▼")
print("    ├─ Preservação Probatória")
print("    ├─ Fundamento Jurídico")
print("    ├─ Termos de Custódia")
print("    ├─ Política de Privacidade")
print("    └─ Institucional")
print("="*60)
