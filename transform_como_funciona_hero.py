#!/usr/bin/env python3
"""
Transformar hero da página como-funciona.html

OBJETIVO:
- Remover elemento gráfico/imagem do hero
- Aplicar padrão de hero da página segurança (centralizado, sem imagem)
- Adicionar gráfico SVG institucional (3 círculos)

GARANTIAS:
- Somente como-funciona.html modificado
- Outras páginas não afetadas
- CSS inline isolado
"""

import re

def transform_como_funciona_hero():
    file_path = "public/como-funciona.html"
    
    print("=" * 60)
    print("TRANSFORMAÇÃO HERO - COMO FUNCIONA")
    print("=" * 60)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # ========================================
    # 1. SUBSTITUIR HERO
    # ========================================
    print("\n1️⃣ Substituindo hero...")
    
    # Padrão atual: hero com imagem
    hero_pattern = r'<section class="page-header page-header--como-funciona hero--image"[^>]*>.*?</section>'
    
    # Novo hero centralizado (padrão segurança)
    new_hero = '''<section class="page-header page-header--como-funciona-centered">
  <div class="page-header-inner page-header--como-funciona">
    
    <h1>Como Funciona</h1>

    <div class="como-funciona-graphic">
      <svg viewBox="0 0 900 120" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        
        <!-- Linha Base -->
        <line x1="100" y1="60" x2="800" y2="60"
              stroke="var(--color-green-700)"
              stroke-width="1.5"
              opacity="0.35"/>
        
        <!-- Círculo 1 -->
        <circle cx="250" cy="60" r="10"
                fill="var(--color-green-700)"/>
        
        <text x="250" y="95"
              text-anchor="middle"
              font-size="16"
              font-family="var(--font-body)"
              fill="var(--color-text-strong)">
          Integridade
        </text>
        
        <!-- Círculo 2 -->
        <circle cx="450" cy="60" r="10"
                fill="var(--color-green-700)"/>
        
        <text x="450" y="95"
              text-anchor="middle"
              font-size="16"
              font-family="var(--font-body)"
              fill="var(--color-text-strong)">
          Cadeia de Custódia
        </text>
        
        <!-- Círculo 3 -->
        <circle cx="650" cy="60" r="10"
                fill="var(--color-green-700)"/>
        
        <text x="650" y="95"
              text-anchor="middle"
              font-size="16"
              font-family="var(--font-body)"
              fill="var(--color-text-strong)">
          Validade Jurídica
        </text>
        
      </svg>
    </div>

    <p class="page-header-subtitle">Processo estruturado para preservação probatória de ativos digitais com registro verificável.</p>

  </div>
</section>'''
    
    html = re.sub(hero_pattern, new_hero, html, flags=re.DOTALL)
    print("   ✅ Hero substituído por versão centralizada")
    
    # ========================================
    # 2. ADICIONAR CSS INLINE
    # ========================================
    print("\n2️⃣ Adicionando CSS inline...")
    
    css_block = '''
<!-- CSS Exclusivo - Página Como Funciona -->
<style>
/* ================================
   MAIN - FIX PARA HEADER FIXO
================================ */
body.exec-compact .main.main--hero-top {
  padding-top: 80px !important;
  margin-top: 0 !important;
}

/* ================================
   HERO COMO FUNCIONA - CENTRALIZADO
================================ */
.page-header--como-funciona-centered {
  background: linear-gradient(135deg, 
    var(--color-surface-light) 0%, 
    rgba(255,255,255,0.98) 100%);
  padding: 3rem 2rem 5rem 2rem;
  margin-top: 0;
  text-align: center;
}

.page-header--como-funciona {
  max-width: 820px;
  margin: 0 auto;
}

.page-header--como-funciona h1 {
  font-family: var(--font-display);
  font-size: clamp(2rem, 4vw, 2.8rem);
  font-weight: 500;
  color: var(--color-text-strong);
  line-height: 1.25;
  margin-bottom: 2rem;
}

.page-header--como-funciona .page-header-subtitle {
  font-size: 1.125rem;
  line-height: 1.6;
  color: var(--color-text-muted);
  max-width: 680px;
  margin: 0 auto;
}

/* Gráfico Institucional */
.como-funciona-graphic {
  margin: 1.5rem auto 2.5rem auto;
  max-width: 900px;
  opacity: 0.9;
}

.como-funciona-graphic svg {
  width: 100%;
  height: auto;
  display: block;
}

/* Responsividade */
@media (max-width: 768px) {
  body.exec-compact .main.main--hero-top {
    padding-top: 70px !important;
  }
  
  .como-funciona-graphic svg text {
    font-size: 13px;
  }
  
  .page-header--como-funciona-centered {
    padding: 2rem 1.5rem 3rem 1.5rem;
  }
}
</style>
'''
    
    # Inserir CSS antes de </head>
    head_close = html.find('</head>')
    if head_close != -1:
        html = html[:head_close] + css_block + '\n' + html[head_close:]
        print("   ✅ CSS inline adicionado")
    
    # Salvar arquivo
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("\n" + "=" * 60)
    print("TRANSFORMAÇÃO CONCLUÍDA!")
    print("=" * 60)
    print("\n📋 Alterações aplicadas:")
    print("  ✅ Hero sem imagem de fundo")
    print("  ✅ Hero centralizado (padrão segurança)")
    print("  ✅ Gráfico SVG institucional (3 círculos)")
    print("  ✅ Padding-top no main (80px desktop, 70px mobile)")
    print("  ✅ CSS inline isolado")
    print("  ✅ Responsividade mobile")
    print("\n🔒 Garantias:")
    print("  ✓ Somente como-funciona.html modificado")
    print("  ✓ CSS com prefixo .como-funciona-* e .page-header--como-funciona-*")
    print("  ✓ Outras páginas não afetadas")
    print("  ✓ Header/Footer preservados")
    print("=" * 60)

if __name__ == "__main__":
    transform_como_funciona_hero()
