#!/usr/bin/env python3
"""
Script para mover o infográfico do fluxo probatório para dentro do hero.
A imagem deve estar no hero, não em uma seção separada no meio da página.
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

def move_infographic_to_hero():
    """Move o infográfico para dentro do hero section"""
    html_path = 'public/como-funciona.html'
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 1. Remover a seção infografico-section completa do meio da página
    infographic_section_pattern = r'<section class="infografico-section">.*?</section>\n'
    content = re.sub(infographic_section_pattern, '', content, flags=re.DOTALL)
    
    log_info("Seção infográfico-section removida do meio da página")
    
    # 2. Adicionar a imagem dentro do hero como page-header-graphic
    # Encontrar o fechamento de page-header-content e adicionar a graphic antes do fechamento de page-header-inner
    hero_pattern = r'(<div class="page-header-content">.*?</div>)\n\n(</div>\n</section>)'
    
    hero_graphic = r'''\1
<div class="page-header-graphic">
<img src="/assets/images/fluxo-cadeia-custodia-verde.png" alt="Fluxo da Cadeia de Custódia Digital" class="hero-infographic" width="600" height="300">
</div>

\2'''
    
    content = re.sub(hero_pattern, hero_graphic, content, flags=re.DOTALL)
    
    log_info("Imagem adicionada ao hero como page-header-graphic")
    
    # Salvar apenas se houve mudanças
    if content != original_content:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        log_info(f"HTML atualizado: {html_path}")
        return True
    else:
        log_warning(f"Nenhuma mudança necessária em {html_path}")
        return False

def update_css_for_hero_graphic():
    """Atualiza CSS para o infográfico no hero"""
    css_path = 'public/assets/css/styles-clean.exec-compact.css'
    
    with open(css_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remover CSS antigo do infografico-section se existir
    if '.infografico-section' in content:
        # Remover toda a seção de CSS do infográfico
        content = re.sub(
            r'/\* ={50,}\n   INFOGRÁFICO DO FLUXO PROBATÓRIO\n   ={50,} \*/.*?(?=\n/\*|$)',
            '',
            content,
            flags=re.DOTALL
        )
        log_info("CSS antigo do infográfico removido")
    
    # Adicionar CSS para o hero-infographic
    hero_graphic_css = '''
/* =========================================================
   HERO INFOGRAPHIC - Fluxo Probatório
   ========================================================= */

.page-header-graphic {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.hero-infographic {
  width: 100%;
  max-width: 600px;
  height: auto;
  display: block;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

@media (max-width: 968px) {
  .page-header--split {
    flex-direction: column;
  }
  
  .page-header-graphic {
    margin-top: 30px;
    padding: 0;
  }
  
  .hero-infographic {
    max-width: 100%;
  }
}

@media (max-width: 768px) {
  .page-header-graphic {
    margin-top: 20px;
  }
  
  .hero-infographic {
    border-radius: 4px;
  }
}
'''
    
    # Adicionar no final do arquivo
    content += '\n' + hero_graphic_css
    
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    log_info(f"CSS atualizado: {css_path}")
    return True

def main():
    print(f"\n{BOLD}=== Mover Infográfico para o Hero ==={RESET}\n")
    
    # 1. Mover infográfico para o hero
    html_updated = move_infographic_to_hero()
    
    # 2. Atualizar CSS
    css_updated = update_css_for_hero_graphic()
    
    # Relatório final
    print(f"\n{BOLD}=== Resumo das Alterações ==={RESET}")
    log_info(f"✓ Infográfico movido para o hero: {html_updated}")
    log_info(f"✓ CSS atualizado para hero-graphic: {css_updated}")
    
    print(f"\n{GREEN}{BOLD}✓ Alteração concluída com sucesso!{RESET}\n")
    print(f"{YELLOW}Estrutura final:{RESET}")
    print(f"  Hero: <div class='page-header-inner page-header--split'>")
    print(f"    → <div class='page-header-content'> (texto)")
    print(f"    → <div class='page-header-graphic'> (imagem)")
    print(f"\n{YELLOW}Próximos passos:{RESET}")
    print(f"  1. Verificar a página: public/como-funciona.html")
    print(f"  2. Testar layout (texto + imagem lado a lado)")
    print(f"  3. Commit e push das alterações\n")

if __name__ == '__main__':
    main()
