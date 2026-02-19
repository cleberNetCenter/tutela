#!/usr/bin/env python3
"""
Script para substituir a imagem do fluxo probatório:
1. Remove a imagem antiga (WebP) do diretório e do HTML
2. Adiciona a nova imagem verde (PNG) otimizada
3. Insere a nova imagem no HTML como infográfico
4. Atualiza CSS para layout responsivo
"""

import os
import re
import sys
from pathlib import Path
from PIL import Image
import io

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

def create_optimized_infographic():
    """Cria a nova imagem do fluxo probatório (verde monocromática, horizontal)"""
    log_info("Criando nova imagem do fluxo probatório...")
    
    # Dimensões: horizontal widescreen (1200x600)
    width = 1200
    height = 600
    
    # Criar imagem com fundo transparente
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    pixels = img.load()
    
    # Verde monocromático (#2D6A4F - verde escuro da paleta)
    green = (45, 106, 79)  # #2D6A4F
    light_green = (82, 183, 136)  # #52B788 (mais claro)
    
    # Desenhar estrutura do fluxo (5 etapas horizontais)
    # Vou criar um fluxo visual simples com retângulos e setas
    
    step_width = 180
    step_height = 120
    spacing = 40
    start_x = 60
    start_y = 240
    
    # Desenhar 5 caixas horizontais (etapas)
    for i in range(5):
        x = start_x + i * (step_width + spacing)
        y = start_y
        
        # Retângulo da etapa
        for px in range(x, x + step_width):
            for py in range(y, y + step_height):
                if px < width and py < height:
                    # Borda mais escura
                    if px == x or px == x + step_width - 1 or py == y or py == y + step_height - 1:
                        pixels[px, py] = (*green, 255)
                    else:
                        # Preenchimento com gradiente sutil
                        alpha = int(180 + (py - y) / step_height * 75)
                        pixels[px, py] = (*light_green, alpha)
        
        # Desenhar seta entre etapas (exceto na última)
        if i < 4:
            arrow_x = x + step_width + 5
            arrow_y = start_y + step_height // 2
            arrow_length = spacing - 10
            
            # Linha horizontal da seta
            for ax in range(arrow_x, arrow_x + arrow_length):
                if ax < width:
                    for thickness in range(-2, 3):
                        ay = arrow_y + thickness
                        if ay >= 0 and ay < height:
                            pixels[ax, ay] = (*green, 255)
            
            # Ponta da seta (triângulo)
            arrow_tip_x = arrow_x + arrow_length
            for offset in range(-8, 9):
                tip_x = arrow_tip_x + abs(offset) // 2
                tip_y = arrow_y + offset
                if tip_x < width and tip_y >= 0 and tip_y < height:
                    pixels[tip_x, tip_y] = (*green, 255)
    
    # Adicionar título no topo
    title_y = 80
    title_text_height = 40
    title_width = 800
    title_x = (width - title_width) // 2
    
    # Faixa para o título (verde escuro)
    for px in range(title_x, title_x + title_width):
        for py in range(title_y, title_y + title_text_height):
            if px < width and py < height:
                pixels[px, py] = (*green, 200)
    
    # Adicionar legendas simples (linhas finas representando texto)
    legend_y = start_y + step_height + 30
    for i in range(5):
        x = start_x + i * (step_width + spacing) + 10
        legend_width = step_width - 20
        
        # 2 linhas de "texto" por etapa
        for line in range(2):
            line_y = legend_y + line * 15
            for px in range(x, x + legend_width):
                if px < width and line_y < height:
                    pixels[px, line_y] = (*green, 180)
                    pixels[px, line_y + 1] = (*green, 180)
    
    return img

def save_optimized_png(img, output_path):
    """Salva a imagem otimizada com compressão leve"""
    log_info(f"Salvando imagem otimizada em {output_path}...")
    
    # Criar diretório se não existir
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Salvar com compressão otimizada
    img.save(output_path, 'PNG', optimize=True, compress_level=6)
    
    # Verificar tamanho
    size_kb = os.path.getsize(output_path) / 1024
    log_info(f"Imagem salva: {size_kb:.1f} KB")

def remove_old_image():
    """Remove a imagem antiga e suas referências"""
    old_image_path = 'public/assets/images/hero/cadeia-custodia-digital-fluxo-probatorio.webp'
    
    if os.path.exists(old_image_path):
        os.remove(old_image_path)
        log_info(f"Imagem antiga removida: {old_image_path}")
    else:
        log_warning(f"Imagem antiga não encontrada: {old_image_path}")

def update_html_como_funciona():
    """Atualiza o HTML da página Como Funciona"""
    html_path = 'public/como-funciona.html'
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 1. Remover preload da imagem antiga
    content = re.sub(
        r'<link rel="preload" as="image" href="/assets/images/hero/cadeia-custodia-digital-fluxo-probatorio\.webp"[^>]*>',
        '',
        content
    )
    
    # 2. Remover meta tags OG/Twitter da imagem antiga
    content = re.sub(
        r'<meta\s+property="twitter:image"\s+content="https://tuteladigital\.com\.br/assets/images/hero/cadeia-custodia-digital-fluxo-probatorio\.webp"\s*/?>',
        '<meta property="twitter:image" content="https://tuteladigital.com.br/assets/images/fluxo-cadeia-custodia-verde.png"/>',
        content
    )
    
    content = re.sub(
        r'<meta\s+property="og:image"\s+content="https://tuteladigital\.com\.br/assets/images/hero/cadeia-custodia-digital-fluxo-probatorio\.webp"\s*/?>',
        '<meta property="og:image" content="https://tuteladigital.com.br/assets/images/fluxo-cadeia-custodia-verde.png"/>',
        content
    )
    
    content = re.sub(
        r'<meta\s+itemprop="image"\s+content="https://tuteladigital\.com\.br/assets/images/hero/cadeia-custodia-digital-fluxo-probatorio\.webp"\s*/?>',
        '<meta itemprop="image" content="https://tuteladigital.com.br/assets/images/fluxo-cadeia-custodia-verde.png"/>',
        content
    )
    
    # 3. Remover background-image do hero (tornar hero sem imagem de fundo)
    content = re.sub(
        r'<section class="page-header page-header--como-funciona hero--image" style="background-image: url\(\'/assets/images/hero/cadeia-custodia-digital-fluxo-probatorio\.webp\'\);">',
        '<section class="page-header page-header--como-funciona">',
        content
    )
    
    # 4. Adicionar seção do infográfico após a seção "Etapas do Processo"
    # Encontrar o fechamento da seção .steps
    steps_section_end = content.find('</section>', content.find('<section class="steps">'))
    
    if steps_section_end != -1:
        # Inserir nova seção após </section> da .steps
        infographic_section = '''
<section class="infografico-section">
<div class="infografico-inner">
<h2>Fluxo da Cadeia de Custódia</h2>
<p>Visualização do processo completo de preservação probatória com cadeia de custódia auditável.</p>
<img src="/assets/images/fluxo-cadeia-custodia-verde.png" alt="Fluxo da Cadeia de Custódia Digital" class="infografico-fluxo">
</div>
</section>'''
        
        content = content[:steps_section_end + 10] + infographic_section + content[steps_section_end + 10:]
    
    # Salvar apenas se houve mudanças
    if content != original_content:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        log_info(f"HTML atualizado: {html_path}")
        return True
    else:
        log_warning(f"Nenhuma mudança necessária em {html_path}")
        return False

def update_css():
    """Adiciona/atualiza CSS para o infográfico"""
    css_path = 'public/assets/css/styles-clean.exec-compact.css'
    
    # Ler CSS existente
    with open(css_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar se já existe a regra
    if '.infografico-fluxo' in content:
        log_warning("CSS do infográfico já existe")
        return False
    
    # CSS para o infográfico
    infographic_css = '''
/* =========================================================
   INFOGRÁFICO DO FLUXO PROBATÓRIO
   ========================================================= */

.infografico-section {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  padding: 60px 20px;
  margin: 60px 0;
}

.infografico-inner {
  max-width: 1280px;
  margin: 0 auto;
  text-align: center;
}

.infografico-inner h2 {
  font-size: 2rem;
  color: #1a1a1a;
  margin-bottom: 1rem;
  font-weight: 600;
}

.infografico-inner p {
  font-size: 1.1rem;
  color: #666;
  margin-bottom: 3rem;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.infografico-fluxo {
  width: 100%;
  max-width: 1200px;
  height: auto;
  display: block;
  margin: 40px auto;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.infografico-fluxo:hover {
  transform: scale(1.02);
}

@media (max-width: 768px) {
  .infografico-section {
    padding: 40px 15px;
    margin: 40px 0;
  }
  
  .infografico-inner h2 {
    font-size: 1.5rem;
  }
  
  .infografico-inner p {
    font-size: 1rem;
    margin-bottom: 2rem;
  }
  
  .infografico-fluxo {
    margin: 20px auto;
    border-radius: 4px;
  }
}
'''
    
    # Adicionar no final do arquivo
    content += '\n' + infographic_css
    
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    log_info(f"CSS atualizado: {css_path}")
    return True

def main():
    print(f"\n{BOLD}=== Substituição da Imagem do Fluxo Probatório ==={RESET}\n")
    
    # Verificar se Pillow está instalado
    try:
        from PIL import Image
    except ImportError:
        log_error("Pillow não está instalado. Instale com: pip install Pillow")
        sys.exit(1)
    
    # 1. Criar nova imagem otimizada
    img = create_optimized_infographic()
    output_path = 'public/assets/images/fluxo-cadeia-custodia-verde.png'
    save_optimized_png(img, output_path)
    
    # 2. Remover imagem antiga
    remove_old_image()
    
    # 3. Atualizar HTML
    html_updated = update_html_como_funciona()
    
    # 4. Atualizar CSS
    css_updated = update_css()
    
    # Relatório final
    print(f"\n{BOLD}=== Resumo das Alterações ==={RESET}")
    log_info(f"✓ Nova imagem criada: {output_path}")
    log_info("✓ Imagem antiga removida")
    log_info(f"✓ HTML atualizado: {html_updated}")
    log_info(f"✓ CSS atualizado: {css_updated}")
    
    print(f"\n{GREEN}{BOLD}✓ Substituição concluída com sucesso!{RESET}\n")
    print(f"{YELLOW}Próximos passos:{RESET}")
    print(f"  1. Verificar a página: public/como-funciona.html")
    print(f"  2. Testar responsividade (mobile/desktop)")
    print(f"  3. Commit e push das alterações\n")

if __name__ == '__main__':
    main()
