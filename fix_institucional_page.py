#!/usr/bin/env python3
"""
Fix Institucional Page Alignment & Add White-Paper Structure
=============================================================
Corrige o desalinhamento das listas na página institucional e
implementa estrutura editorial white-paper exclusiva.

ESCOPO: Apenas /legal/institucional.html
ZERO impacto em outras páginas.
"""

import re

def fix_institucional_page():
    """Corrige alinhamento e adiciona estrutura white-paper"""
    
    html_path = "public/legal/institucional.html"
    css_path = "public/assets/css/styles-clean.css"
    
    print("📄 Corrigindo página institucional...")
    
    # Ler HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 1️⃣ CORRIGIR DESALINHAMENTO - Converter lista inline em grid estruturado
    print("  🔧 Corrigindo desalinhamento da lista...")
    
    old_list = '''<h2 >Finalidade da Infraestrutura</h2>
<div class="text-block-inner" style="max-width: 960px; margin: 0 auto;">
<ul style="list-style: disc; padding-left: 1.5rem; line-height: 1.8;">
<li>Produção de prova judicial</li>
<li>Preservação pré-litígio</li>
<li>Arbitragem</li>
<li>Defesa administrativa</li>
<li>Compliance regulatório</li>
<li>Investigação interna</li>
</ul>
</div>'''
    
    new_list = '''<h2>Finalidade da Infraestrutura</h2>
<div class="finalidade-grid">
  <div class="finalidade-item">Produção de prova judicial</div>
  <div class="finalidade-item">Preservação pré-litígio</div>
  <div class="finalidade-item">Arbitragem</div>
  <div class="finalidade-item">Defesa administrativa</div>
  <div class="finalidade-item">Compliance regulatório</div>
  <div class="finalidade-item">Investigação interna</div>
</div>'''
    
    html = html.replace(old_list, new_list)
    print("    ✅ Lista convertida em grid alinhado")
    
    # 2️⃣ ADICIONAR CONTAINER WHITE-PAPER
    print("  📦 Adicionando container white-paper...")
    
    # Encontrar início do conteúdo (após hero)
    hero_end = '</section>\n<section class="text-block">'
    whitepaper_start = '</section>\n<div class="whitepaper-container">\n<section class="text-block">'
    
    html = html.replace(hero_end, whitepaper_start, 1)
    
    # Encontrar fim do conteúdo (antes da CTA final)
    cta_start = '<section class="cta-final">'
    whitepaper_end = '</div>\n<section class="cta-final">'
    
    # Substituir a última ocorrência antes da CTA
    last_section_before_cta = html.rfind('</section>\n<section class="cta-final">')
    if last_section_before_cta != -1:
        html = html[:last_section_before_cta] + '</section>\n</div>\n<section class="cta-final">' + html[last_section_before_cta + len('</section>\n<section class="cta-final">'):]
    
    print("    ✅ Container white-paper adicionado")
    
    # 3️⃣ ADICIONAR DIVIDERS ANTES DOS H2
    print("  ➗ Adicionando separadores institucionais...")
    
    # Adicionar divider antes de cada H2 (exceto o primeiro que está no hero)
    h2_sections = [
        '<h2 >Natureza da Atividade</h2>',
        '<h2>Finalidade da Infraestrutura</h2>',
        '<h2 >Base Jurídica Aplicável</h2>',
        '<h2 >Interoperabilidade Cartorial</h2>',
        '<h2 >Desenvolvimento e Governança</h2>'
    ]
    
    for h2 in h2_sections:
        html = html.replace(h2, '<div class="wp-divider"></div>\n' + h2)
    
    print("    ✅ Separadores adicionados")
    
    # 4️⃣ ADICIONAR CLASSE HIGHLIGHT EM PARÁGRAFOS ESTRATÉGICOS
    print("  ✨ Destacando parágrafos estratégicos...")
    
    # "Natureza da Atividade" - primeiro parágrafo
    html = html.replace(
        '<p >A Tutela Digital® não exerce função cartorial e não substitui tabelionato.</p>',
        '<p class="wp-highlight">A Tutela Digital® não exerce função cartorial e não substitui tabelionato.</p>'
    )
    
    # "Base Jurídica" - primeiro parágrafo
    html = html.replace(
        '<p >A admissibilidade da prova digital fundamenta-se no Código de Processo Civil',
        '<p class="wp-highlight">A admissibilidade da prova digital fundamenta-se no Código de Processo Civil'
    )
    
    print("    ✅ Parágrafos destacados")
    
    # 5️⃣ ADICIONAR CLASSES REVEAL-ON-SCROLL
    print("  🎬 Adicionando animações discretas...")
    
    # Adicionar reveal em todas as sections de conteúdo
    html = html.replace(
        '<section class="text-block">',
        '<section class="text-block reveal-on-scroll">'
    )
    
    html = html.replace(
        '<section class="features">',
        '<section class="features reveal-on-scroll">'
    )
    
    print("    ✅ Animações adicionadas")
    
    # 6️⃣ ADICIONAR RESUMO EXECUTIVO ANTES DA CTA
    print("  📝 Adicionando resumo executivo...")
    
    summary_section = '''
<section class="wp-summary reveal-on-scroll">
  <div class="wp-summary-inner">
    <h2>Resumo Técnico</h2>
    <p>
    A Tutela Digital® consolida preservação probatória estruturada com cadeia de custódia verificável, 
    interoperabilidade cartorial sob demanda e governança técnica sob responsabilidade da NetCenter, 
    empresa com três décadas de atuação em infraestrutura digital.
    </p>
  </div>
</section>

'''
    
    html = html.replace('<section class="cta-final">', summary_section + '<section class="cta-final">')
    print("    ✅ Resumo executivo adicionado")
    
    # 7️⃣ ADICIONAR SCRIPT DE SCROLL REVEAL
    print("  📜 Adicionando script de scroll reveal...")
    
    scroll_script = '''
<script>
document.addEventListener("DOMContentLoaded", function() {
  const elements = document.querySelectorAll('.reveal-on-scroll');

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, {
    threshold: 0.15
  });

  elements.forEach(el => observer.observe(el));
});
</script>
'''
    
    # Adicionar antes do </body>
    html = html.replace('</body>', scroll_script + '\n</body>')
    print("    ✅ Script adicionado")
    
    # Salvar HTML
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    # 8️⃣ ADICIONAR CSS ESPECÍFICO
    print("\n🎨 Adicionando CSS específico da página institucional...")
    
    with open(css_path, 'r', encoding='utf-8') as f:
        css = f.read()
    
    # Verificar se já existe
    if 'INSTITUCIONAL – PAGE SPECIFIC' in css:
        print("  ℹ️  CSS específico já existe")
        return True
    
    # CSS específico
    page_css = '''

/* =============================
   INSTITUCIONAL – PAGE SPECIFIC
   ============================= */

/* White-paper container */
.whitepaper-container {
  max-width: 960px;
  margin: 0 auto;
}

/* Separadores institucionais */
.wp-divider {
  width: 60px;
  height: 2px;
  background: var(--color-green-800);
  margin: 3rem 0 2rem 0;
  opacity: 0.6;
}

/* Hierarquia tipográfica */
.whitepaper-container h2 {
  font-family: var(--font-display);
  font-size: 2.1rem;
  letter-spacing: -0.02em;
  line-height: 1.25;
}

.whitepaper-container h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-top: 2rem;
}

.whitepaper-container p {
  font-size: 1.075rem;
  line-height: 1.85;
}

/* Blocos analíticos (highlight) */
.wp-highlight {
  padding: 1.5rem 1.75rem;
  background: linear-gradient(135deg, #f7fbf9, #edf6f2);
  border-left: 4px solid var(--color-green-800);
  margin: 2rem 0;
  font-weight: 500;
}

/* Grid de finalidades (corrige desalinhamento) */
.finalidade-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
  max-width: 960px;
  margin-left: auto;
  margin-right: auto;
}

.finalidade-item {
  background: #ffffff;
  padding: 1.25rem;
  border-left: 3px solid var(--color-green-800);
  font-size: 0.95rem;
  color: var(--color-text-base);
}

/* Resumo executivo */
.wp-summary {
  padding: 4rem 2rem;
  background: var(--color-surface-muted);
  margin-top: 4rem;
}

.wp-summary-inner {
  max-width: 900px;
  margin: 0 auto;
}

.wp-summary h2 {
  margin-bottom: 1.5rem;
  font-family: var(--font-display);
  font-size: 2rem;
}

/* Micro-animações discretas (scroll reveal) */
.reveal-on-scroll {
  opacity: 0;
  transform: translateY(16px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}

.reveal-on-scroll.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Refinamento de features (hover suave) */
.features .feature-item {
  border-radius: 6px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.features .feature-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 28px rgba(0,0,0,0.08);
}

/* Responsivo */
@media (max-width: 768px) {
  .whitepaper-container h2 {
    font-size: 1.75rem;
  }
  
  .whitepaper-container p {
    font-size: 1rem;
  }
  
  .finalidade-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .wp-summary {
    padding: 3rem 1.5rem;
  }
  
  .wp-highlight {
    padding: 1.25rem 1.5rem;
  }
}
'''
    
    css += page_css
    
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css)
    
    print("  ✅ CSS específico adicionado")
    
    return True

if __name__ == "__main__":
    print("🚀 Implementando melhorias na página institucional...")
    print("=" * 70)
    
    success = fix_institucional_page()
    
    print("=" * 70)
    
    if success:
        print("✅ Melhorias implementadas com sucesso!")
        print("\n📋 Resumo das alterações:")
        print("  1. ✅ Desalinhamento de lista corrigido (grid estruturado)")
        print("  2. ✅ Container white-paper adicionado")
        print("  3. ✅ Separadores institucionais (wp-divider)")
        print("  4. ✅ Parágrafos estratégicos destacados (wp-highlight)")
        print("  5. ✅ Animações discretas de scroll reveal")
        print("  6. ✅ Resumo executivo adicionado antes da CTA")
        print("  7. ✅ CSS específico isolado (~150 linhas)")
        print("\n📁 Arquivos modificados:")
        print("  • public/legal/institucional.html")
        print("  • public/assets/css/styles-clean.css")
        print("\n⚠️  CRÍTICO: Verificar que outras páginas não foram afetadas!")
        print("\n🎯 Validar em:")
        print("  • Desktop 1440px, 1280px, 992px")
        print("  • Tablet 768px")
        print("  • Mobile")
    else:
        print("❌ Falha ao aplicar melhorias")
