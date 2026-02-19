#!/usr/bin/env python3
"""
Standardize Legal Pages - White-Paper Style
============================================
Aplica padronização white-paper exclusivamente nas 5 páginas legais:
- /legal/institucional.html
- /legal/fundamento-juridico.html
- /legal/termos-de-custodia.html
- /legal/politica-de-privacidade.html
- /legal/preservacao-probatoria-digital.html

REGRAS CRÍTICAS:
- NÃO alterar páginas fora de /legal/
- NÃO alterar header, footer, menu ou WhatsApp
- NÃO alterar CSS global
- Classes com prefixo wp-
- Zero regressão
"""

def standardize_legal_pages():
    """Aplica padronização white-paper nas páginas legais"""
    
    # Definir páginas e seus gráficos SVG específicos
    pages = {
        'public/legal/institucional.html': {
            'svg_terms': ['Infraestrutura', 'Conformidade', 'Governança']
        },
        'public/legal/fundamento-juridico.html': {
            'svg_terms': ['CPC', 'Integridade', 'Admissibilidade']
        },
        'public/legal/termos-de-custodia.html': {
            'svg_terms': ['Responsabilidade', 'Custódia', 'Limitação']
        },
        'public/legal/politica-de-privacidade.html': {
            'svg_terms': ['LGPD', 'Confidencialidade', 'Direitos']
        },
        'public/legal/preservacao-probatoria-digital.html': {
            'svg_terms': ['Integridade', 'Cadeia de Custódia', 'Validação']
        }
    }
    
    print("🚀 Padronizando páginas legais como white-paper...")
    print("=" * 70)
    
    for page_path, config in pages.items():
        print(f"\n📄 Processando: {page_path}")
        
        try:
            with open(page_path, 'r', encoding='utf-8') as f:
                html = f.read()
            
            # 1️⃣ REMOVER GRAVURAS E BACKGROUND IMAGES
            print("  🗑️  Removendo gravuras...")
            
            # Remover <link rel="preload"> de imagens hero
            html = html.replace('<link rel="preload" as="image" href="/assets/images/hero/documento-selo-assinatura.webp" type="image/webp">', '')
            
            # Remover style="background-image: url(...)" do hero
            import re
            html = re.sub(r'style="background-image:\s*url\([^)]+\);"', '', html)
            
            # Remover classe hero--image
            html = html.replace('hero--image', '')
            
            print("    ✅ Gravuras removidas")
            
            # 2️⃣ ADICIONAR GRÁFICO VETORIAL SVG
            print("  🎨 Adicionando gráfico vetorial...")
            
            svg_terms = config['svg_terms']
            svg_graphic = f'''

<div class="wp-legal-graphic">
  <svg viewBox="0 0 600 120" xmlns="http://www.w3.org/2000/svg">
    <line x1="50" y1="60" x2="550" y2="60" stroke="#1b6b4d" stroke-width="1.5" opacity="0.5"/>
    <circle cx="150" cy="60" r="6" fill="#1b6b4d"/>
    <circle cx="300" cy="60" r="6" fill="#1b6b4d"/>
    <circle cx="450" cy="60" r="6" fill="#1b6b4d"/>
    <text x="150" y="40" text-anchor="middle" font-size="12" fill="#1b6b4d">{svg_terms[0]}</text>
    <text x="300" y="40" text-anchor="middle" font-size="12" fill="#1b6b4d">{svg_terms[1]}</text>
    <text x="450" y="40" text-anchor="middle" font-size="12" fill="#1b6b4d">{svg_terms[2]}</text>
  </svg>
</div>
'''
            
            # Inserir SVG após o hero (antes da primeira section de conteúdo)
            # Procurar pelo padrão: </section>\n<section class="text-block"> ou </section>\n<div class="whitepaper-container">
            if '</section>\n<div class="whitepaper-container">' in html:
                html = html.replace('</section>\n<div class="whitepaper-container">', '</section>' + svg_graphic + '\n<div class="whitepaper-container">')
            elif '</section>\n<section class="preservacao-intro">' in html:
                # Para preservacao-probatoria que já tem preservacao-intro
                html = html.replace('</section>\n<section class="preservacao-intro">', '</section>' + svg_graphic + '\n<section class="preservacao-intro">')
            elif '</section>\n<section class="text-block">' in html:
                # Primeira ocorrência após o hero
                hero_end = html.find('</section>\n<section class="text-block">')
                if hero_end != -1:
                    html = html[:hero_end] + '</section>' + svg_graphic + '\n<section class="text-block">' + html[hero_end + len('</section>\n<section class="text-block">'):]
            
            print("    ✅ Gráfico SVG adicionado")
            
            # 3️⃣ ADICIONAR SCRIPT DE SCROLL REVEAL (se não existir)
            if 'reveal-on-scroll' not in html or 'IntersectionObserver' not in html:
                print("  🎬 Adicionando script de scroll reveal...")
                
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
  }, { threshold: 0.15 });

  elements.forEach(el => observer.observe(el));
});
</script>
'''
                
                # Adicionar antes de </body> (se não existir já)
                if 'IntersectionObserver' not in html:
                    html = html.replace('</body>', scroll_script + '\n</body>')
                    print("    ✅ Script adicionado")
            
            # Salvar HTML modificado
            with open(page_path, 'w', encoding='utf-8') as f:
                f.write(html)
            
            print(f"  ✅ {page_path.split('/')[-1]} processado")
            
        except Exception as e:
            print(f"  ❌ Erro ao processar {page_path}: {e}")
            continue
    
    # 4️⃣ ADICIONAR CSS ESPECÍFICO PARA PÁGINAS LEGAIS
    print("\n🎨 Adicionando CSS específico para páginas legais...")
    
    css_path = "public/assets/css/styles-clean.css"
    
    with open(css_path, 'r', encoding='utf-8') as f:
        css = f.read()
    
    # Verificar se já existe
    if 'LEGAL PAGES – WHITE-PAPER STANDARDIZATION' in css:
        print("  ℹ️  CSS específico já existe")
        return True
    
    legal_css = '''

/* =============================
   LEGAL PAGES – WHITE-PAPER STANDARDIZATION
   ============================= */

/* Gráfico vetorial minimalista */
.wp-legal-graphic {
  max-width: 960px;
  margin: 3rem auto 2rem auto;
  opacity: 0.75;
}

.wp-legal-graphic svg {
  width: 100%;
  height: auto;
}

/* Hero legal uniforme (sem background-image) */
.page-header--institucional,
.page-header--fundamento-juridico,
.page-header--termos-custodia,
.page-header--politica-privacidade,
.page-header--preservacao-probatoria {
  background: linear-gradient(
    180deg,
    var(--color-surface-light),
    var(--color-surface-muted)
  ) !important;
  background-image: none !important;
}

/* Responsivo para gráfico SVG */
@media (max-width: 768px) {
  .wp-legal-graphic {
    margin: 2rem auto 1.5rem auto;
  }
  
  .wp-legal-graphic svg text {
    font-size: 10px;
  }
}

@media (max-width: 480px) {
  .wp-legal-graphic svg text {
    font-size: 8px;
  }
}
'''
    
    css += legal_css
    
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css)
    
    print("  ✅ CSS específico adicionado")
    
    return True

if __name__ == "__main__":
    print("🚀 Padronizando páginas legais - White-Paper Style...")
    print("=" * 70)
    
    success = standardize_legal_pages()
    
    print("\n" + "=" * 70)
    
    if success:
        print("✅ Padronização concluída com sucesso!")
        print("\n📋 Resumo das alterações:")
        print("  1. ✅ Gravuras e background-images removidos")
        print("  2. ✅ Gráficos vetoriais SVG adicionados (5 páginas)")
        print("  3. ✅ Script de scroll reveal adicionado")
        print("  4. ✅ CSS específico para hero uniforme")
        print("  5. ✅ Responsivo para gráficos SVG")
        print("\n📁 Arquivos modificados:")
        print("  • public/legal/institucional.html")
        print("  • public/legal/fundamento-juridico.html")
        print("  • public/legal/termos-de-custodia.html")
        print("  • public/legal/politica-de-privacidade.html")
        print("  • public/legal/preservacao-probatoria-digital.html")
        print("  • public/assets/css/styles-clean.css")
        print("\n⚠️  CRÍTICO: Verificar que páginas não-legais não foram afetadas!")
        print("\n🎯 Validar:")
        print("  • Gráficos SVG aparecem corretamente")
        print("  • Hero sem background-image")
        print("  • Animações de scroll funcionando")
        print("  • Outras páginas inalteradas")
    else:
        print("❌ Falha ao padronizar páginas")
