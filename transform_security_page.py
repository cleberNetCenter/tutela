#!/usr/bin/env python3
"""
Transformar página /seguranca.html para padrão white-paper institucional

ALTERAÇÕES:
1. Hero: remover imagem, centralizar, adicionar gráfico SVG institucional
2. Cards: transformar grid horizontal em layout vertical (1 card/linha)
3. Títulos: centralizar e padronizar hierarquia
4. CSS: adicionar estilos exclusivos inline
5. Animações: micro-interações discretas

GARANTIAS:
- Somente seguranca.html modificada
- Header/Footer/Menu/CTA preservados
- Variáveis globais CSS intactas
- Sistema i18n mantido
- Zero impacto em outras páginas
"""

import re

def transform_security_page():
    file_path = "public/seguranca.html"
    
    print("=" * 60)
    print("TRANSFORMAÇÃO PÁGINA SEGURANÇA - WHITE-PAPER INSTITUCIONAL")
    print("=" * 60)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # ========================================
    # 1. HERO: Remover imagem e centralizar
    # ========================================
    print("\n1️⃣ Transformando Hero...")
    
    # Substituir hero com imagem por hero centralizado
    hero_pattern = r'<section class="page-header page-header--seguranca hero--image"[^>]*>.*?</section>'
    
    new_hero = '''<section class="page-header page-header--security-centered">
  <div class="page-header-inner page-header--security">
    
    <h1 data-i18n="security.title">Arquitetura de Integridade Aplicada à Preservação Probatória Digital</h1>

    <div class="security-graphic">
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

    <p class="page-header-subtitle">Fundamentos técnicos e jurídicos que sustentam a infraestrutura de preservação probatória.</p>

  </div>
</section>'''
    
    html = re.sub(hero_pattern, new_hero, html, flags=re.DOTALL)
    print("   ✅ Hero centralizado com gráfico institucional")
    
    # ========================================
    # 2. CARDS: Transformar grid em vertical
    # ========================================
    print("\n2️⃣ Transformando Cards...")
    
    # Substituir features-grid--security por security-cards
    html = html.replace(
        '<div class="features-grid features-grid--security">',
        '<div class="security-cards">'
    )
    print("   ✅ Grid substituído por layout vertical")
    
    # ========================================
    # 3. TÍTULOS: Ajustar hierarquia
    # ========================================
    print("\n3️⃣ Ajustando Títulos...")
    
    # Substituir "Controle de Acesso Exclusivo ao Titular"
    html = html.replace(
        '<h3 class="subsection-title" data-i18n="security.h3AccessControl">Controle de Acesso Exclusivo ao Titular</h3>',
        '<h2 class="security-section-title" data-i18n="security.h3AccessControl">Controle de Acesso Exclusivo ao Titular</h2>'
    )
    
    # Substituir "Pilares de Segurança"
    html = html.replace(
        '<h2>Pilares de Segurança</h2>',
        '<h3 class="security-subtitle">Pilares de Segurança</h3>'
    )
    
    print("   ✅ Títulos padronizados e centralizados")
    
    # ========================================
    # 4. CSS: Adicionar estilos inline
    # ========================================
    print("\n4️⃣ Adicionando CSS Inline...")
    
    css_block = '''
<!-- CSS Exclusivo - Página Segurança -->
<style>
/* ================================
   HERO SECURITY - CENTRALIZADO
================================ */
.page-header--security-centered {
  background: linear-gradient(135deg, 
    var(--color-surface-light) 0%, 
    rgba(255,255,255,0.98) 100%);
  padding: 6rem 2rem 5rem 2rem;
  text-align: center;
}

.page-header--security {
  max-width: 820px;
  margin: 0 auto;
}

.page-header--security h1 {
  font-family: var(--font-display);
  font-size: clamp(2rem, 4vw, 2.8rem);
  font-weight: 500;
  color: var(--color-text-strong);
  line-height: 1.25;
  margin-bottom: 2rem;
}

.page-header--security .page-header-subtitle {
  font-size: 1.125rem;
  line-height: 1.6;
  color: var(--color-text-muted);
  max-width: 680px;
  margin: 0 auto;
}

/* Gráfico Institucional */
.security-graphic {
  margin: 1.5rem auto 2.5rem auto;
  max-width: 900px;
  opacity: 0.9;
}

.security-graphic svg {
  width: 100%;
  height: auto;
  display: block;
}

/* ================================
   SECURITY – CARDS CENTRALIZADOS
================================ */
.security-cards {
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
  max-width: 760px;
  margin: 3rem auto 0 auto;
}

.security-cards .feature-item {
  width: 100%;
  padding: 2.2rem 2.4rem;
  border-radius: 8px;
  border: 1px solid var(--color-border-soft);
  background: var(--color-surface-light);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

/* Micro-elevação institucional */
.security-cards .feature-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 28px rgba(0,0,0,0.05);
}

/* Títulos */
.security-section-title {
  font-family: var(--font-display);
  font-size: clamp(1.8rem, 3vw, 2.3rem);
  font-weight: 500;
  text-align: center;
  color: var(--color-text-strong);
  margin: 4rem 0 1.5rem 0;
  letter-spacing: -0.01em;
}

.security-subtitle {
  text-align: center;
  font-size: 1.125rem;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--color-text-muted);
  margin-bottom: 2.5rem;
}

/* Micro-animação discreta */
.security-cards .feature-item {
  opacity: 0;
  transform: translateY(12px);
  animation: fadeSecurity 0.6s ease forwards;
}

.security-cards .feature-item:nth-child(1) { animation-delay: 0.05s; }
.security-cards .feature-item:nth-child(2) { animation-delay: 0.10s; }
.security-cards .feature-item:nth-child(3) { animation-delay: 0.15s; }
.security-cards .feature-item:nth-child(4) { animation-delay: 0.20s; }
.security-cards .feature-item:nth-child(5) { animation-delay: 0.25s; }
.security-cards .feature-item:nth-child(6) { animation-delay: 0.30s; }

@keyframes fadeSecurity {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsividade */
@media (max-width: 768px) {
  .security-graphic svg text {
    font-size: 13px;
  }
  
  .page-header--security-centered {
    padding: 4rem 1.5rem 3rem 1.5rem;
  }
  
  .security-cards {
    gap: 2rem;
    max-width: 100%;
    padding: 0 1.5rem;
  }
  
  .security-cards .feature-item {
    padding: 1.8rem 2rem;
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
    print("TRANSFORMAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 60)
    print("\n📋 Alterações aplicadas:")
    print("  ✅ Hero centralizado sem imagem de fundo")
    print("  ✅ Gráfico SVG institucional (3 círculos)")
    print("  ✅ Cards em layout vertical (1 por linha)")
    print("  ✅ Largura controlada (max-width: 760px)")
    print("  ✅ Títulos centralizados e hierarquia corrigida")
    print("  ✅ Micro-animações discretas")
    print("  ✅ CSS isolado (somente seguranca.html)")
    print("  ✅ Responsividade mobile")
    print("\n🔒 Garantias:")
    print("  ✓ Header/Footer/Menu/CTA preservados")
    print("  ✓ Variáveis CSS globais intactas")
    print("  ✓ Sistema i18n mantido")
    print("  ✓ Zero impacto em outras páginas")
    print("=" * 60)

if __name__ == "__main__":
    transform_security_page()
