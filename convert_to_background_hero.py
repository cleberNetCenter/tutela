#!/usr/bin/env python3
"""
Script para transformar o infográfico em background do hero,
seguindo o mesmo modelo da página de segurança.
"""

import re
import os

# Cores
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def log_info(msg):
    print(f"{GREEN}✓{RESET} {msg}")

def log_warning(msg):
    print(f"{YELLOW}⚠{RESET} {msg}")

def log_error(msg):
    print(f"{RED}✗{RESET} {msg}")

def convert_to_background_hero():
    """Converte o infográfico para background do hero"""
    html_path = 'public/como-funciona.html'
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 1. Adicionar hero--image class e background-image inline style
    # Encontrar: <section class="page-header page-header--como-funciona">
    # Substituir por: <section class="page-header page-header--como-funciona hero--image" style="background-image: url('/assets/images/fluxo-cadeia-custodia-verde.png');">
    
    content = re.sub(
        r'<section class="page-header page-header--como-funciona">',
        '<section class="page-header page-header--como-funciona hero--image" style="background-image: url(\'/assets/images/fluxo-cadeia-custodia-verde.png\');">',
        content
    )
    
    log_info("Hero class e background-image adicionados")
    
    # 2. Remover o <div class="page-header-graphic"> completamente
    content = re.sub(
        r'<div class="page-header-graphic">.*?</div>\n',
        '',
        content,
        flags=re.DOTALL
    )
    
    log_info("Elemento page-header-graphic removido")
    
    # Salvar apenas se houve mudanças
    if content != original_content:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        log_info(f"HTML atualizado: {html_path}")
        return True
    else:
        log_warning(f"Nenhuma mudança necessária em {html_path}")
        return False

def remove_hero_graphic_css():
    """Remove CSS do hero-graphic que não é mais necessário"""
    css_path = 'public/assets/css/styles-clean.exec-compact.css'
    
    with open(css_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Remover toda a seção de HERO INFOGRAPHIC
    content = re.sub(
        r'/\* ={50,}\n   HERO INFOGRAPHIC - Fluxo Probatório\n   ={50,} \*/.*?(?=\n/\*|$)',
        '',
        content,
        flags=re.DOTALL
    )
    
    if content != original_content:
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(content)
        log_info(f"CSS do hero-graphic removido: {css_path}")
        return True
    else:
        log_warning("CSS já estava limpo")
        return False

def add_preload_tag():
    """Adiciona preload tag para a imagem do hero"""
    html_path = 'public/como-funciona.html'
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar se já existe preload
    if 'fluxo-cadeia-custodia-verde.png' in content and 'preload' in content:
        log_warning("Preload tag já existe")
        return False
    
    # Adicionar preload após <head>
    preload_tag = '<link rel="preload" as="image" href="/assets/images/fluxo-cadeia-custodia-verde.png" type="image/png">'
    
    content = re.sub(
        r'(<head>\n)',
        r'\1' + preload_tag + '\n',
        content
    )
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    log_info("Preload tag adicionada")
    return True

def main():
    print(f"\n{BOLD}=== Converter Infográfico para Background do Hero ==={RESET}\n")
    print(f"{YELLOW}Seguindo o modelo da página de segurança:{RESET}")
    print(f"  → Hero com class 'hero--image'")
    print(f"  → Background inline: style='background-image: url(...)'")
    print(f"  → Imagem cobre todo o hero como fundo\n")
    
    # 1. Converter para background hero
    html_updated = convert_to_background_hero()
    
    # 2. Remover CSS desnecessário
    css_updated = remove_hero_graphic_css()
    
    # 3. Adicionar preload
    preload_added = add_preload_tag()
    
    # Relatório final
    print(f"\n{BOLD}=== Resumo das Alterações ==={RESET}")
    log_info(f"✓ Hero convertido para background: {html_updated}")
    log_info(f"✓ CSS hero-graphic removido: {css_updated}")
    log_info(f"✓ Preload tag adicionada: {preload_added}")
    
    print(f"\n{GREEN}{BOLD}✓ Conversão concluída com sucesso!{RESET}\n")
    print(f"{YELLOW}Estrutura final (igual à página de segurança):{RESET}")
    print(f"  <section class='page-header hero--image'")
    print(f"           style='background-image: url(...);'>")
    print(f"    <div class='page-header-inner'>")
    print(f"      <div class='page-header-content'>")
    print(f"        → Texto sobre o background")
    print(f"      </div>")
    print(f"    </div>")
    print(f"  </section>")
    print(f"\n{YELLOW}Próximos passos:{RESET}")
    print(f"  1. Verificar a página: public/como-funciona.html")
    print(f"  2. Confirmar imagem como background do hero")
    print(f"  3. Commit e push das alterações\n")

if __name__ == '__main__':
    main()
