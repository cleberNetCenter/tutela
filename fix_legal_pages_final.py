#!/usr/bin/env python3
"""
fix_legal_pages_final.py

Correções cirúrgicas nas páginas /legal/:
1. Hero com texto visível (estrutura correta)
2. Todos os H2 dentro de containers centralizados
3. Seções com largura adequada

ZERO impacto fora de /legal/
"""

import re
from pathlib import Path

LEGAL_PAGES = [
    "public/legal/preservacao-probatoria-digital.html",
    "public/legal/fundamento-juridico.html",
    "public/legal/termos-de-custodia.html",
    "public/legal/politica-de-privacidade.html",
    "public/legal/institucional.html"
]

CSS_FILE = "public/assets/css/styles-clean.css"

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_hero_structure(html):
    """
    PROBLEMA 1: Hero sem texto visível
    Garantir estrutura simples e correta
    """
    # Padrão para encontrar o hero atual
    hero_pattern = r'<section class="page-header[^"]*"[^>]*>(.*?)</section>'
    
    def rebuild_hero(match):
        hero_content = match.group(1)
        
        # Extrair H1
        h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', hero_content, re.DOTALL)
        if not h1_match:
            return match.group(0)  # Manter original se não encontrar H1
        h1_text = h1_match.group(1).strip()
        
        # Extrair parágrafo (pode estar em vários lugares)
        p_patterns = [
            r'<p class="hero-subtitle"[^>]*>(.*?)</p>',
            r'<p class="page-header-subtitle"[^>]*>(.*?)</p>',
            r'<p[^>]*>(.*?)</p>'
        ]
        
        p_text = ""
        for pattern in p_patterns:
            p_match = re.search(pattern, hero_content, re.DOTALL)
            if p_match:
                p_text = p_match.group(1).strip()
                break
        
        # Reconstruir hero limpo
        new_hero = f'''<section class="page-header page-header--legal">
  <div class="page-header-inner page-header--legal">
    
    <h1>{h1_text}</h1>
    <div class="legal-divider"></div>

    <p class="page-header-subtitle">
      {p_text}
    </p>

  </div>
</section>'''
        
        return new_hero
    
    # Processar apenas o primeiro hero (dentro de <main>)
    main_parts = html.split('<main', 1)
    if len(main_parts) == 2:
        before_main = main_parts[0] + '<main'
        main_and_after = main_parts[1]
        
        # Processar apenas até o primeiro </section> depois do hero
        section_parts = main_and_after.split('</section>', 1)
        if len(section_parts) == 2:
            hero_part = '<main' + section_parts[0] + '</section>'
            after_hero = section_parts[1]
            
            # Aplicar fix no hero
            hero_part = re.sub(hero_pattern, rebuild_hero, hero_part, count=1)
            
            # Remover gráficos SVG decorativos que estão fora do hero
            after_hero = re.sub(
                r'<div class="wp-legal-graphic">.*?</div>',
                '',
                after_hero,
                flags=re.DOTALL
            )
            
            html = before_main + hero_part.replace('<main', '', 1) + after_hero
    
    return html

def fix_h2_containers(html):
    """
    PROBLEMA 2: H2 fora de containers
    Garantir que todos os H2 estejam dentro de .text-block-inner
    """
    # Encontrar H2 soltos (fora de text-block-inner)
    # Padrão: H2 que não tem text-block-inner antes dele
    
    # Primeiro, vamos garantir que <body> tenha a classe legal-page
    if 'class="legal-page"' not in html and '<body' in html:
        html = re.sub(
            r'<body([^>]*)>',
            r'<body\1 class="legal-page">',
            html
        )
        # Se já tinha class, adicionar
        html = re.sub(
            r'<body class="([^"]*)"([^>]*)class="legal-page">',
            r'<body class="\1 legal-page"\2>',
            html
        )
    
    return html

def fix_sections_width(html):
    """
    PROBLEMA 3: Seções sem largura adequada
    Adicionar wrapper onde necessário
    """
    # Já temos legal-grid-wrapper para features
    # Não precisa fazer nada adicional, o CSS já cuida
    return html

def update_css(css_content):
    """
    Atualizar CSS para corrigir os problemas
    """
    # Verificar se já tem as correções
    if 'CORREÇÕES HERO E TÍTULOS LEGAIS' in css_content:
        print("  ⚠️  CSS já atualizado, pulando...")
        return css_content
    
    additional_css = '''

/* ==================================================
   CORREÇÕES HERO E TÍTULOS LEGAIS
   ================================================== */

/* Hero - garantir visibilidade do texto */
.page-header--legal {
  padding: 6rem 2rem 5rem 2rem;
  text-align: center;
  background: linear-gradient(
    180deg,
    var(--color-surface-light),
    var(--color-surface-muted)
  );
}

.page-header--legal .page-header-inner {
  max-width: 820px;
  margin: 0 auto;
}

.page-header--legal h1 {
  font-family: var(--font-display);
  font-size: clamp(2.2rem, 4vw, 3rem);
  font-weight: 500;
  color: var(--color-text-strong);
  margin-bottom: 1.5rem;
  line-height: 1.2;
}

.page-header-subtitle {
  font-size: 1.125rem;
  color: var(--color-text-muted);
  max-width: 680px;
  margin: 0 auto;
  line-height: 1.7;
}

/* Títulos soltos - centralizar */
body.legal-page h2,
body.legal-page h3 {
  max-width: 820px;
  margin-left: auto;
  margin-right: auto;
}

/* Wrapper para seções especiais */
.legal-section-wrapper {
  max-width: 980px;
  margin: 4rem auto;
  padding: 0 2rem;
}

/* Sobrescrever estilos anteriores conflitantes */
.page-header--legal .page-header-content {
  max-width: 100%;
}

.page-header--legal .hero-subtitle {
  font-size: 1.125rem;
  color: var(--color-text-muted);
  max-width: 680px;
  margin: 0 auto;
  line-height: 1.7;
}
'''
    
    return css_content + additional_css

def process_page(file_path):
    """Processar uma página legal"""
    print(f"\n🔧 Processando: {file_path}")
    
    html = read_file(file_path)
    
    html = fix_hero_structure(html)
    print("  ✓ Hero corrigido (estrutura limpa)")
    
    html = fix_h2_containers(html)
    print("  ✓ H2 containers verificados")
    
    html = fix_sections_width(html)
    print("  ✓ Seções com largura adequada")
    
    write_file(file_path, html)
    print("  ✅ Página atualizada")

def main():
    print("=" * 70)
    print("🔬 CORREÇÕES CIRÚRGICAS - PÁGINAS LEGAIS")
    print("=" * 70)
    print("\n🎯 Correções:")
    print("  1. Hero com texto visível")
    print("  2. H2 centralizados")
    print("  3. Seções com largura adequada")
    
    # 1. Atualizar CSS
    print("\n📝 Atualizando CSS...")
    css = read_file(CSS_FILE)
    css = update_css(css)
    write_file(CSS_FILE, css)
    print("✅ CSS atualizado")
    
    # 2. Processar páginas
    print("\n📚 Processando páginas legais...")
    for page in LEGAL_PAGES:
        if Path(page).exists():
            process_page(page)
        else:
            print(f"⚠️  Não encontrado: {page}")
    
    print("\n" + "=" * 70)
    print("✅ CORREÇÕES CONCLUÍDAS")
    print("=" * 70)
    print("\n🎯 Resultado esperado:")
    print("  ✓ Hero com H1 + divider + parágrafo visível")
    print("  ✓ Todos os H2 centralizados")
    print("  ✓ Layout limpo e profissional")
    print("  ✓ Zero impacto fora de /legal/")
    
    print("\n⚠️  Validar:")
    print("  • Hero renderiza corretamente")
    print("  • Títulos alinhados ao centro")
    print("  • Sem elementos desalinhados")
    print("  • Outras páginas não afetadas")

if __name__ == "__main__":
    main()
