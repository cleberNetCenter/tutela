#!/usr/bin/env python3
"""
apply_legal_whitepaper_surgical.py

PROMPT CIRÚRGICO – Padrão White-Paper Legal
Aplicar em todas as páginas /legal/:
- Hero centralizado (remover split 2 colunas)
- Linha divisória institucional sob H1
- Grid jurídico 2x2 elegante
- Ritmo vertical harmonizado
- Micro-interações discretas
- Zero impacto fora de /legal/
"""

import re
from pathlib import Path

# Páginas alvo
LEGAL_PAGES = [
    "public/legal/preservacao-probatoria-digital.html",
    "public/legal/fundamento-juridico.html",
    "public/legal/termos-de-custodia.html",
    "public/legal/politica-de-privacidade.html",
    "public/legal/institucional.html"
]

CSS_FILE = "public/assets/css/styles-clean.css"

def read_file(path):
    """Ler arquivo com encoding UTF-8"""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    """Escrever arquivo com encoding UTF-8"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def transform_hero_to_centered(html):
    """
    ETAPA 1: Hero centralizado
    - Substituir .page-header--split por .page-header--legal
    - Remover grid de 2 colunas
    """
    # Substituir classe split por legal
    html = re.sub(
        r'page-header--split',
        'page-header--legal',
        html
    )
    
    # Se houver div com hero-text-content e fundamento-graphic, centralizar tudo
    # Remover estrutura de grid e manter apenas o conteúdo textual
    pattern = r'<div class="page-header--legal">\s*<div class="hero-text-content[^"]*">(.*?)</div>\s*<div class="fundamento-graphic">.*?</div>\s*</div>'
    
    def replace_split_hero(match):
        text_content = match.group(1)
        return f'<div class="page-header--legal">\n{text_content}\n</div>'
    
    html = re.sub(pattern, replace_split_hero, html, flags=re.DOTALL)
    
    return html

def add_legal_divider_after_h1(html):
    """
    ETAPA 2: Linha divisória institucional
    - Adicionar <div class="legal-divider"></div> após cada <h1> no hero
    """
    # Procurar H1 dentro de page-header e adicionar divider logo após
    pattern = r'(<h1[^>]*>.*?</h1>)(\s*)(?!<div class="legal-divider">)'
    replacement = r'\1\n    <div class="legal-divider"></div>\2'
    
    # Aplicar apenas dentro de page-header
    parts = html.split('<section class="page-header')
    if len(parts) > 1:
        for i in range(1, len(parts)):
            # Processar apenas até o fim da seção page-header
            section_parts = parts[i].split('</section>', 1)
            if len(section_parts) == 2:
                header_content = section_parts[0]
                rest = section_parts[1]
                
                # Adicionar divider após h1 se ainda não existir
                if '<div class="legal-divider">' not in header_content:
                    header_content = re.sub(pattern, replacement, header_content)
                
                parts[i] = header_content + '</section>' + rest
        
        html = '<section class="page-header'.join(parts)
    
    return html

def add_body_class_legal(html):
    """
    Adicionar classe 'legal-page' ao body se não existir
    """
    if 'legal-page' not in html:
        html = re.sub(
            r'<body([^>]*)>',
            r'<body\1 class="legal-page">',
            html
        )
        # Se já tinha class, adicionar à classe existente
        html = re.sub(
            r'<body([^>]*) class="([^"]*)"([^>]*)class="legal-page">',
            r'<body\1 class="\2 legal-page"\3>',
            html
        )
    return html

def add_animation_script(html):
    """
    ETAPA 5: Adicionar script de micro-animações discretas
    - Fade-in progressivo por seção
    - Apenas se ainda não existir
    """
    script = '''
<!-- Script de Micro-Animações Jurídicas -->
<script>
document.addEventListener("DOMContentLoaded", function () {
  const sections = document.querySelectorAll(
    ".page-header, .text-block, .features, .cta-final"
  );

  sections.forEach(section => {
    section.classList.add("legal-animate");
  });

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  document.querySelectorAll(".legal-animate").forEach(el => {
    observer.observe(el);
  });
});
</script>
'''
    
    # Adicionar apenas se não existir script similar
    if 'legal-animate' not in html and 'Micro-Animações Jurídicas' not in html:
        html = html.replace('</body>', script + '\n</body>')
    
    return html

def remove_inline_styles(html):
    """
    Remover estilos inline específicos das páginas que conflitam
    """
    # Remover style blocks com CSS isolado de fundamento-juridico
    html = re.sub(
        r'<!-- CSS Isolado - Fundamento Jurídico -->.*?</style>',
        '',
        html,
        flags=re.DOTALL
    )
    
    # Remover scripts duplicados de animação
    html = re.sub(
        r'<!-- Script de Micro-Animação - Fundamento Jurídico -->.*?</script>',
        '',
        html,
        flags=re.DOTALL
    )
    
    return html

def transform_grids_to_legal_grid(html):
    """
    ETAPA 3: Grid jurídico 2x2
    - Envolver .features em .legal-grid-wrapper > .legal-grid
    - Manter estrutura de cards
    """
    # Procurar blocos .features e envolver com legal-grid-wrapper
    pattern = r'(<section[^>]*class="[^"]*features[^"]*"[^>]*>)(.*?)(</section>)'
    
    def wrap_features(match):
        opening_tag = match.group(1)
        content = match.group(2)
        closing_tag = match.group(3)
        
        # Se já tem legal-grid-wrapper, não duplicar
        if 'legal-grid-wrapper' in content:
            return match.group(0)
        
        # Encontrar o grid interno
        if '<div class="features-grid">' in content or '<div class="grid">' in content:
            # Substituir a classe do grid
            content = content.replace('class="features-grid"', 'class="legal-grid"')
            content = content.replace('class="grid"', 'class="legal-grid"')
            
            # Envolver com wrapper se ainda não tiver
            if '<div class="legal-grid-wrapper">' not in content:
                # Encontrar onde começa o conteúdo do grid
                grid_start = content.find('<div class="legal-grid">')
                if grid_start > -1:
                    before_grid = content[:grid_start]
                    grid_and_after = content[grid_start:]
                    
                    # Encontrar o fim do grid
                    grid_end = grid_and_after.find('</div>') + 6  # +6 para incluir </div>
                    grid_content = grid_and_after[:grid_end]
                    after_grid = grid_and_after[grid_end:]
                    
                    content = before_grid + '\n  <div class="legal-grid-wrapper">\n    ' + grid_content + '\n  </div>' + after_grid
        
        return opening_tag + content + closing_tag
    
    html = re.sub(pattern, wrap_features, html, flags=re.DOTALL)
    
    return html

def add_legal_css_to_global(css_content):
    """
    Adicionar CSS do padrão white-paper ao arquivo global
    """
    # Verificar se já existe
    if 'LEGAL – HERO WHITE PAPER CENTRALIZADO' in css_content:
        print("⚠️  CSS legal já existe, pulando adição...")
        return css_content
    
    legal_css = '''

/* ==================================================
   LEGAL – HERO WHITE PAPER CENTRALIZADO
   ================================================== */

.page-header--legal {
  max-width: 820px;
  margin: 0 auto;
  text-align: center;
}

.page-header--legal h1 {
  max-width: 760px;
  margin: 0 auto 1.5rem auto;
}

.page-header--legal p {
  max-width: 680px;
  margin: 0 auto;
}

/* ==================================================
   LEGAL – DIVISOR INSTITUCIONAL
   ================================================== */

.legal-divider {
  width: 72px;
  height: 2px;
  margin: 1.5rem auto 2.5rem auto;
  background: linear-gradient(
    90deg,
    transparent,
    var(--color-primary),
    transparent
  );
  opacity: 0.6;
}

/* ==================================================
   LEGAL – GRID 2x2 WHITE PAPER
   ================================================== */

.legal-grid-wrapper {
  max-width: 980px;
  margin: 4rem auto;
  padding: 0 2rem;
}

.legal-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2.5rem;
}

.legal-grid .feature-item {
  padding: 2.5rem;
  min-height: 230px;
  border-radius: 8px;
  transition: transform .25s ease, box-shadow .25s ease;
}

.legal-grid .feature-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 18px 38px rgba(0,0,0,0.06);
}

@media (max-width: 768px) {
  .legal-grid {
    grid-template-columns: 1fr;
  }
}

/* ==================================================
   LEGAL – RITMO VERTICAL INSTITUCIONAL
   ================================================== */

body.legal-page .text-block {
  padding: 5rem 2rem;
}

body.legal-page .features {
  padding: 5rem 2rem;
}

body.legal-page .page-header {
  padding: 6rem 2rem 5rem 2rem;
}

/* ==================================================
   LEGAL – MICRO ANIMAÇÕES DISCRETAS
   ================================================== */

.legal-animate {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity .6s ease, transform .6s ease;
}

.legal-animate.visible {
  opacity: 1;
  transform: translateY(0);
}
'''
    
    return css_content + legal_css

def process_legal_page(file_path):
    """
    Processar uma página legal aplicando todas as transformações
    """
    print(f"\n📄 Processando: {file_path}")
    
    html = read_file(file_path)
    original_length = len(html)
    
    # Aplicar transformações em ordem
    html = remove_inline_styles(html)
    print("  ✓ Removidos estilos inline conflitantes")
    
    html = transform_hero_to_centered(html)
    print("  ✓ Hero centralizado")
    
    html = add_legal_divider_after_h1(html)
    print("  ✓ Linha divisória institucional adicionada")
    
    html = transform_grids_to_legal_grid(html)
    print("  ✓ Grid jurídico 2x2 aplicado")
    
    html = add_body_class_legal(html)
    print("  ✓ Classe legal-page adicionada ao body")
    
    html = add_animation_script(html)
    print("  ✓ Script de micro-animações adicionado")
    
    write_file(file_path, html)
    new_length = len(html)
    diff = new_length - original_length
    
    print(f"  📊 Tamanho: {original_length} → {new_length} ({diff:+d} bytes)")
    
    return True

def main():
    """
    Executar transformação cirúrgica em todas as páginas legais
    """
    print("=" * 70)
    print("🔬 PADRÃO WHITE-PAPER LEGAL – IMPLEMENTAÇÃO CIRÚRGICA")
    print("=" * 70)
    
    # 1. Processar CSS global
    print("\n📝 Atualizando CSS global...")
    css_content = read_file(CSS_FILE)
    css_content = add_legal_css_to_global(css_content)
    write_file(CSS_FILE, css_content)
    print("✅ CSS global atualizado")
    
    # 2. Processar cada página legal
    print("\n📚 Processando páginas legais...")
    success_count = 0
    
    for page in LEGAL_PAGES:
        if Path(page).exists():
            if process_legal_page(page):
                success_count += 1
        else:
            print(f"⚠️  Arquivo não encontrado: {page}")
    
    # 3. Resumo final
    print("\n" + "=" * 70)
    print("✅ IMPLEMENTAÇÃO CONCLUÍDA")
    print("=" * 70)
    print(f"\n📊 Resumo:")
    print(f"   • Páginas processadas: {success_count}/{len(LEGAL_PAGES)}")
    print(f"   • CSS global atualizado: {CSS_FILE}")
    
    print(f"\n🎯 Transformações aplicadas:")
    print(f"   ✓ Hero centralizado (remover split 2 colunas)")
    print(f"   ✓ Linha divisória institucional sob H1")
    print(f"   ✓ Grid jurídico 2x2 elegante")
    print(f"   ✓ Ritmo vertical harmonizado")
    print(f"   ✓ Micro-interações discretas (fade-in)")
    print(f"   ✓ Classe body.legal-page adicionada")
    
    print(f"\n🔒 Garantias:")
    print(f"   ✓ Zero impacto fora de /legal/")
    print(f"   ✓ Prefixo .legal- em todas as classes")
    print(f"   ✓ Header/Footer intocados")
    print(f"   ✓ Variáveis globais preservadas")
    
    print(f"\n⚠️  Validação necessária:")
    print(f"   • Hero centralizado em todas as páginas")
    print(f"   • Linha divisória visível")
    print(f"   • Grid 2x2 funcionando")
    print(f"   • Animações suaves no scroll")
    print(f"   • Responsividade mobile (768px)")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
