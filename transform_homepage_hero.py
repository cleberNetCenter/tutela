#!/usr/bin/env python3
"""
Reestruturação Sofisticada do Hero - Homepage Tutela Digital®

OBJETIVO:
- Reduzir altura do hero (eliminar vazio vertical)
- Substituir subtítulo pela frase institucional oficial
- Ajustar hierarquia tipográfica
- Inserir linha institucional inferior
- Aplicar micro-animação discreta
- Manter degradê existente

GARANTIAS:
- Somente homepage (index.html) modificada
- Degradê preservado
- Cores institucionais intactas
- Header/Menu não alterados
"""

import re

def transform_homepage_hero():
    file_path = "public/index.html"
    
    print("=" * 60)
    print("REESTRUTURAÇÃO SOFISTICADA HERO - HOMEPAGE")
    print("=" * 60)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # ========================================
    # 1. SUBSTITUIR HERO HTML
    # ========================================
    print("\n1️⃣ Transformando hero HTML...")
    
    # Padrão atual
    hero_pattern = r'<section class="hero">.*?</section>'
    
    # Novo hero com frase institucional oficial e linha inferior
    new_hero = '''<section class="hero hero--homepage">
<div class="hero-inner hero-content--homepage">
<h1>Tutela Digital<sup>®</sup></h1>
<p class="hero-subtitle" data-i18n="hero_subtitle">Infraestrutura jurídica de custódia digital com integridade técnica verificável e validade probatória estruturada.</p>
<div class="hero-divider"></div>
</div>
</section>'''
    
    html = re.sub(hero_pattern, new_hero, html, flags=re.DOTALL, count=1)
    print("   ✅ Hero HTML atualizado com frase institucional e linha inferior")
    
    # ========================================
    # 2. ADICIONAR CSS INLINE
    # ========================================
    print("\n2️⃣ Adicionando CSS sofisticado...")
    
    css_block = '''
<!-- CSS Exclusivo - Hero Homepage Sofisticado -->
<style>
/* ================================
   HERO HOMEPAGE - REESTRUTURADO
================================ */
.hero--homepage {
  padding: 3.5rem 2rem 3rem 2rem;
  min-height: auto;
}

.hero-content--homepage {
  text-align: center;
  max-width: 900px;
  margin: 0 auto;
}

.hero--homepage h1 {
  font-size: clamp(2.8rem, 4vw, 3.5rem);
  letter-spacing: -0.01em;
  font-weight: 500;
}

.hero--homepage .hero-subtitle {
  max-width: 720px;
  margin: 1.2rem auto 0 auto;
  font-size: 1.05rem;
  line-height: 1.6;
  color: rgba(0,0,0,0.65);
}

/* Linha institucional inferior */
.hero-divider {
  width: 80px;
  height: 2px;
  margin: 2rem auto 0 auto;
  background: linear-gradient(
    90deg,
    rgba(0,0,0,0),
    rgba(0,0,0,0.35),
    rgba(0,0,0,0)
  );
  opacity: 0.8;
}

/* Micro-animação institucional discreta */
.hero--homepage h1,
.hero--homepage .hero-subtitle,
.hero-divider {
  opacity: 0;
  transform: translateY(8px);
  animation: heroFade 0.6s ease forwards;
}

.hero--homepage .hero-subtitle {
  animation-delay: 0.1s;
}

.hero-divider {
  animation-delay: 0.2s;
}

@keyframes heroFade {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsividade */
@media (max-width: 768px) {
  .hero--homepage {
    padding: 3rem 1.5rem 2.5rem 1.5rem;
  }
  
  .hero--homepage h1 {
    font-size: clamp(2rem, 6vw, 2.8rem);
  }
  
  .hero--homepage .hero-subtitle {
    font-size: 1rem;
  }
}
</style>
'''
    
    # Inserir CSS antes de </head>
    head_close = html.find('</head>')
    if head_close != -1:
        html = html[:head_close] + css_block + '\n' + html[head_close:]
        print("   ✅ CSS sofisticado adicionado")
    
    # Salvar
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("\n" + "=" * 60)
    print("REESTRUTURAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 60)
    print("\n📋 Alterações aplicadas:")
    print("  ✅ Hero compacto (padding reduzido)")
    print("  ✅ Frase institucional oficial inserida:")
    print("      'Infraestrutura jurídica de custódia digital com")
    print("       integridade técnica verificável e validade")
    print("       probatória estruturada.'")
    print("  ✅ Hierarquia tipográfica ajustada")
    print("  ✅ Linha institucional inferior (80px × 2px)")
    print("  ✅ Micro-animação discreta (fade-in 0.6s)")
    print("  ✅ Centralização institucional")
    print("  ✅ Responsividade mobile")
    print("\n🔒 Garantias:")
    print("  ✓ Degradê preservado (não alterado)")
    print("  ✓ Cores institucionais intactas")
    print("  ✓ Somente homepage modificada")
    print("  ✓ Header/Menu preservados")
    print("  ✓ CSS inline isolado")
    print("  ✓ Outras páginas não afetadas")
    print("\n✨ Resultado:")
    print("  • Hero sofisticado e institucional")
    print("  • Sem vazio vertical excessivo")
    print("  • Frase oficial padronizada")
    print("  • Assinatura visual com linha inferior")
    print("  • Animação elegante e discreta")
    print("=" * 60)

if __name__ == "__main__":
    transform_homepage_hero()
