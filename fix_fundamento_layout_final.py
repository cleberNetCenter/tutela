#!/usr/bin/env python3
"""
fix_fundamento_layout_final.py

Aplica correções de layout na página /legal/fundamento-juridico.html:
- Garante um único <h1>
- Substitui o hero por um split layout
- Adiciona gráfico minimalista com micro-animações
- Insere CSS isolado via <style> inline
- Adiciona script de IntersectionObserver
- NÃO altera outras páginas, CSS global ou componentes compartilhados
"""

import re

FILE_PATH = "public/legal/fundamento-juridico.html"

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_fundamento_layout(html):
    """
    Aplica todas as correções solicitadas:
    1. Remove hero antigo e insere novo hero split
    2. Garante um único <h1>
    3. Adiciona gráfico minimalista
    4. Insere CSS isolado
    5. Adiciona script de micro-animação
    """
    
    # 1. Remover preload da imagem hero antiga
    html = re.sub(
        r'<link rel="preload" as="image" href="/assets/images/hero/[^"]+" type="image/webp">',
        '',
        html
    )
    
    # 2. Adicionar CSS isolado no <head> antes do </head>
    isolated_css = """
<!-- CSS Isolado - Fundamento Jurídico -->
<style>
/* Hero Split Layout - Exclusivo fundamento-juridico.html */
.page-header--fundamento {
  background: linear-gradient(180deg, var(--color-surface-light), var(--color-surface-muted));
  padding: var(--space-2xl) var(--space-lg);
  position: relative;
}

.page-header--split {
  display: grid;
  grid-template-columns: 1fr 0.8fr;
  align-items: center;
  column-gap: var(--space-xl);
  max-width: 1200px;
  margin: 0 auto;
}

.hero-text-content {
  max-width: 640px;
}

.hero-text-content h1 {
  font-family: var(--font-display);
  font-size: 2.75rem;
  line-height: 1.15;
  margin-bottom: 1.25rem;
  color: var(--color-text-strong);
}

.hero-text-content p {
  font-size: 1.15rem;
  line-height: 1.85;
  color: var(--color-text-medium);
  max-width: 70ch;
}

/* Gráfico Minimalista */
.fundamento-graphic {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-lg);
}

.fundamento-points {
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
  width: 100%;
  max-width: 360px;
}

.fundamento-point {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  opacity: 0;
  transform: translateX(-20px);
}

.fundamento-point.visible {
  animation: fadeInRight 0.6s ease forwards;
}

.fundamento-point:nth-child(1) {
  animation-delay: 0.2s;
}

.fundamento-point:nth-child(2) {
  animation-delay: 0.4s;
}

.fundamento-point:nth-child(3) {
  animation-delay: 0.6s;
}

.point-circle {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(27, 107, 77, 0.2);
}

.point-circle svg {
  width: 24px;
  height: 24px;
  color: white;
}

.point-text {
  font-family: var(--font-display);
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-text-strong);
  flex: 1;
}

@keyframes fadeInRight {
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Ritmo Vertical */
.whitepaper-container {
  max-width: 960px;
  margin: 0 auto;
  padding: var(--space-2xl) var(--space-lg);
}

.text-block {
  margin-bottom: var(--space-2xl);
}

.text-block h2 {
  font-family: var(--font-display);
  font-size: 2.1rem;
  line-height: 1.25;
  margin-bottom: 1.25rem;
  color: var(--color-text-strong);
}

.text-block h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-top: 2rem;
  margin-bottom: 1rem;
  color: var(--color-text-strong);
}

.text-block p {
  font-size: 1.075rem;
  line-height: 1.85;
  max-width: 70ch;
  color: var(--color-text-medium);
  margin-bottom: 1rem;
}

/* Responsivo */
@media (max-width: 768px) {
  .page-header--split {
    grid-template-columns: 1fr;
    gap: var(--space-lg);
  }
  
  .hero-text-content h1 {
    font-size: 2rem;
  }
  
  .fundamento-graphic {
    padding: var(--space-md);
  }
  
  .text-block h2 {
    font-size: 1.75rem;
  }
}
</style>
"""
    
    html = html.replace('</head>', isolated_css + '\n</head>')
    
    # 3. Substituir o hero antigo pelo novo split layout
    # Encontrar o hero atual (entre <main> e primeiro <section>)
    hero_pattern = r'(<main[^>]*>)(.*?)(<section[^>]*class="[^"]*text-block)'
    
    new_hero = r'''\1
<!-- Hero Split Layout -->
<section class="page-header page-header--fundamento hero--image">
  <div class="page-header--split">
    <div class="hero-text-content fade-in-up">
      <h1>Fundamento Jurídico da Preservação Probatória Digital</h1>
      <p>Base normativa para admissibilidade da prova eletrônica, integridade da cadeia de custódia tecnológica e validade probatória sob os princípios do Código de Processo Civil e legislação correlata.</p>
    </div>
    
    <div class="fundamento-graphic">
      <div class="fundamento-points">
        <div class="fundamento-point fade-in-up">
          <div class="point-circle">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
              <line x1="16" y1="13" x2="8" y2="13"></line>
              <line x1="16" y1="17" x2="8" y2="17"></line>
              <polyline points="10 9 9 9 8 9"></polyline>
            </svg>
          </div>
          <div class="point-text">CPC</div>
        </div>
        
        <div class="fundamento-point fade-in-up">
          <div class="point-circle">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
          </div>
          <div class="point-text">Integridade</div>
        </div>
        
        <div class="fundamento-point fade-in-up">
          <div class="point-circle">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
          </div>
          <div class="point-text">Admissibilidade</div>
        </div>
      </div>
    </div>
  </div>
</section>

\3'''
    
    html = re.sub(hero_pattern, new_hero, html, flags=re.DOTALL)
    
    # 4. Remover qualquer <h1> duplicado no conteúdo (manter apenas o do hero)
    # Procurar por <h1> fora do hero e substituir por <h2>
    def replace_duplicate_h1(match):
        full_match = match.group(0)
        # Se não estiver dentro de page-header, substituir por h2
        if 'page-header' not in full_match[:100]:  # Verificar contexto anterior
            return full_match.replace('<h1', '<h2').replace('</h1>', '</h2>')
        return full_match
    
    # Encontrar todos os h1 após o hero
    parts = html.split('</section>', 1)
    if len(parts) > 1:
        before_content = parts[0] + '</section>'
        after_content = parts[1]
        after_content = re.sub(r'<h1([^>]*)>(.*?)</h1>', r'<h2\1>\2</h2>', after_content)
        html = before_content + after_content
    
    # 5. Adicionar script de micro-animação antes de </body>
    animation_script = """
<!-- Script de Micro-Animação - Fundamento Jurídico -->
<script>
(function() {
  // IntersectionObserver para fade-in-up
  const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.15
  };
  
  const fadeInObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        // Observar apenas uma vez
        fadeInObserver.unobserve(entry.target);
      }
    });
  }, observerOptions);
  
  // Observar elementos com fade-in-up
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.fade-in-up, .fundamento-point').forEach(el => {
      fadeInObserver.observe(el);
    });
  });
})();
</script>
"""
    
    html = html.replace('</body>', animation_script + '\n</body>')
    
    return html

def main():
    print("🔧 Aplicando correções de layout em fundamento-juridico.html...")
    
    # Ler arquivo
    html = read_file(FILE_PATH)
    print(f"✅ Arquivo lido: {FILE_PATH}")
    
    # Aplicar correções
    html = fix_fundamento_layout(html)
    print("✅ Correções aplicadas:")
    print("   • Hero substituído por split layout")
    print("   • H1 único garantido")
    print("   • Gráfico minimalista adicionado")
    print("   • CSS isolado inserido")
    print("   • Script de animação adicionado")
    
    # Salvar
    write_file(FILE_PATH, html)
    print(f"✅ Arquivo salvo: {FILE_PATH}")
    
    print("\n🎯 Resultado esperado:")
    print("   • Hero alinhado com split editorial")
    print("   • Hierarquia HTML correta (único h1)")
    print("   • Ritmo vertical consistente")
    print("   • Gráfico com micro-animações")
    print("   • Zero impacto em outras páginas")
    
    print("\n⚠️  Validar:")
    print("   • Alinhamento do hero")
    print("   • Animação dos três pontos")
    print("   • Semântica HTML")
    print("   • Responsividade (1440px, 992px, 768px)")

if __name__ == "__main__":
    main()
