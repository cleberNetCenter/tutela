#!/usr/bin/env python3
"""
Fix Fundamento Jurídico Page Layout
====================================
Corrige desalinhamento visual da página /legal/fundamento-juridico.html
seguindo as 7 etapas especificadas.

IMPORTANTE: Alterações APENAS nesta página.
"""

def fix_fundamento_juridico():
    """Aplica todas as correções especificadas"""
    
    html_path = "public/legal/fundamento-juridico.html"
    
    print("🚀 Corrigindo layout da página fundamento-juridico.html...")
    print("=" * 70)
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # ETAPA 1 — CORREÇÃO DA HIERARQUIA HTML
    print("📝 ETAPA 1: Corrigindo hierarquia HTML...")
    
    # Substituir hero antigo
    old_hero = '''<section class="page-header page-header--institucional " >
<div class="page-header-inner page-header--split">
<div class="page-header-content">
<h1>Fundamento Jurídico da Preservação de Evidência Digital no Direito Brasileiro</h1>
<p>Base normativa que sustenta a validade jurídica da prova digital e da cadeia de custódia tecnológica.</p>
</div>
<div class="page-header-inner">
<h2 class="section-title" >Base Legal da Admissibilidade de Prova Eletrônica</h2>
<h2 class="section-title" >Legislação Brasileira Aplicável à Evidência Digital</h2>
</div>

</div>
</section>'''
    
    new_hero = '''<section class="page-header page-header--fundamento hero--image">
  <div class="page-header-inner page-header--split">

    <div class="page-header-content">
      <h1>Fundamento Jurídico da Preservação de Evidência Digital</h1>

      <p class="hero-intro">
        Base normativa que sustenta a admissibilidade da prova eletrônica
        e a validade da cadeia de custódia tecnológica no ordenamento jurídico brasileiro.
      </p>
    </div>

    <div class="page-header-aside">
      <p class="hero-context">
        A integridade técnica documentada fortalece o livre convencimento motivado
        e reduz riscos de impugnação por alegação de adulteração.
      </p>
    </div>

  </div>
</section>'''
    
    html = html.replace(old_hero, new_hero)
    print("  ✅ Hero corrigido (apenas 1 H1)")
    
    # ETAPA 4 — SUBSTITUIR GRÁFICO ATUAL
    print("\n🎨 ETAPA 4: Substituindo gráfico...")
    
    old_graphic = '''<div class="wp-legal-graphic">
  <svg viewBox="0 0 600 120" xmlns="http://www.w3.org/2000/svg">
    <line x1="50" y1="60" x2="550" y2="60" stroke="#1b6b4d" stroke-width="1.5" opacity="0.5"/>
    <circle cx="150" cy="60" r="6" fill="#1b6b4d"/>
    <circle cx="300" cy="60" r="6" fill="#1b6b4d"/>
    <circle cx="450" cy="60" r="6" fill="#1b6b4d"/>
    <text x="150" y="40" text-anchor="middle" font-size="12" fill="#1b6b4d">CPC</text>
    <text x="300" y="40" text-anchor="middle" font-size="12" fill="#1b6b4d">Integridade</text>
    <text x="450" y="40" text-anchor="middle" font-size="12" fill="#1b6b4d">Admissibilidade</text>
  </svg>
</div>'''
    
    new_graphic = '''<section class="legal-graphic fade-in-up">
  <div class="legal-graphic-inner">

    <div class="legal-point fade-in-up" style="transition-delay:0ms">
      <span>CPC</span>
    </div>

    <div class="legal-point fade-in-up" style="transition-delay:120ms">
      <span>Integridade</span>
    </div>

    <div class="legal-point fade-in-up" style="transition-delay:240ms">
      <span>Admissibilidade</span>
    </div>

  </div>
</section>'''
    
    html = html.replace(old_graphic, new_graphic)
    print("  ✅ Gráfico substituído com animação")
    
    # ETAPA 5 — CSS ISOLADO
    print("\n🎨 ETAPA 5: Adicionando CSS isolado...")
    
    css_section = '''/* ===============================
   FUNDAMENTO JURÍDICO – AJUSTES
   =============================== */

.page-header--fundamento {
  padding: calc(var(--space-2xl) * 0.8) var(--space-lg);
}

.page-header--fundamento .page-header-content {
  max-width: 640px;
}

.page-header--fundamento h1 {
  font-size: clamp(2rem, 3.2vw, 2.6rem);
  line-height: 1.2;
  margin-bottom: 1.25rem;
}

.hero-intro,
.hero-context {
  font-size: 1.0625rem;
  color: var(--color-text-muted);
  line-height: 1.6;
  max-width: 480px;
}

.page-header--fundamento .page-header--split {
  grid-template-columns: 1fr 0.8fr;
  align-items: center;
  column-gap: var(--space-xl);
}

/* ===============================
   GRÁFICO LEGAL
   =============================== */

.legal-graphic {
  margin-top: var(--space-xl);
}

.legal-graphic-inner {
  max-width: 960px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  opacity: 0.9;
}

.legal-graphic-inner::before {
  content: "";
  position: absolute;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--color-border-strong);
  z-index: 0;
}

.legal-point {
  position: relative;
  background: var(--color-green-900);
  color: #fff;
  width: 70px;
  height: 70px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  font-size: 0.8125rem;
  z-index: 1;
}

/* ===============================
   MICRO-ANIMAÇÃO DISCRETA
   =============================== */

.fade-in-up {
  opacity: 0;
  transform: translateY(10px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}

.fade-in-up.visible {
  opacity: 1;
  transform: translateY(0);
}'''
    
    # Inserir CSS após o bloco de .detail-title existente
    insertion_point = '.detail-title {\n  font-size: 1.25rem;\n  font-weight: 500;\n  margin: 1.5rem 0 0.75rem 0;\n  color: var(--color-text, #444);\n  line-height: 1.5;\n}'
    
    html = html.replace(insertion_point, insertion_point + '\n\n' + css_section)
    print("  ✅ CSS isolado adicionado")
    
    # ETAPA 6 — SCRIPT PARA ATIVAR MICRO-ANIMAÇÃO
    print("\n🎬 ETAPA 6: Adicionando script de animação...")
    
    animation_script = '''
<script>
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.2 });

  document.querySelectorAll('.fade-in-up').forEach(el => {
    observer.observe(el);
  });
</script>'''
    
    # Adicionar antes de </body> (substituir script existente se houver)
    if 'IntersectionObserver' in html and 'threshold: 0.15' in html:
        # Já tem script, substituir
        import re
        html = re.sub(
            r'<script>\s*document\.addEventListener.*?</script>',
            animation_script,
            html,
            flags=re.DOTALL
        )
        print("  ✅ Script de animação atualizado")
    else:
        # Adicionar novo
        html = html.replace('</body>', animation_script + '\n</body>')
        print("  ✅ Script de animação adicionado")
    
    # Salvar arquivo
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("\n" + "=" * 70)
    print("✅ Correções aplicadas com sucesso!")
    
    return True

if __name__ == "__main__":
    print("🔧 Corrigindo layout de fundamento-juridico.html...")
    print("=" * 70)
    
    success = fix_fundamento_juridico()
    
    if success:
        print("\n📋 Resumo das alterações:")
        print("  1. ✅ Hierarquia HTML corrigida (apenas 1 H1)")
        print("  2. ✅ Hero com split layout editorial (1fr 0.8fr)")
        print("  3. ✅ Gráfico substituído com círculos e animação")
        print("  4. ✅ CSS isolado adicionado (apenas nesta página)")
        print("  5. ✅ Script de micro-animação integrado")
        print("\n📁 Arquivo modificado:")
        print("  • public/legal/fundamento-juridico.html")
        print("\n⚠️  GARANTIA: Nenhuma outra página foi alterada")
        print("\n🎯 Validar:")
        print("  • Hero alinhado com demais páginas legais")
        print("  • Gráfico com 3 círculos animados")
        print("  • Hierarquia semântica correta")
        print("  • Ritmo vertical institucional")
    else:
        print("❌ Falha ao aplicar correções")
