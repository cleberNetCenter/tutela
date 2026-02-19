#!/usr/bin/env python3
"""
Diagnóstico e Correção COMPLETA do CSS para páginas MPA
========================================================
Verificar todos os seletores necessários e adicionar os faltantes
"""

import re

def main():
    print("🔍 DIAGNÓSTICO COMPLETO DO CSS PARA PÁGINAS MPA\n")
    
    css_path = "/home/user/webapp/public/assets/css/styles-clean.css"
    
    # 1. Ler CSS atual
    print("1️⃣ Lendo CSS atual...")
    with open(css_path, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    # 2. Verificar seletores existentes
    print("\n2️⃣ Verificando seletores existentes...")
    
    selectors_to_check = [
        '.page-header',
        '.page-header h1',
        '.page-header p',
        '.page-header-content h1',
        '.page-header-content p',
        '.text-block',
        '.text-block h2',
        '.text-block p',
        '.steps',
        '.steps h2',
        '.steps-list',
        '.step-item',
        '.step-item h3',
        '.step-item p',
        '.step-number',
        '.benefits',
        '.benefit-item',
        '.cta-final',
        '.cta-final h2'
    ]
    
    missing = []
    for selector in selectors_to_check:
        # Escape special characters for regex
        pattern = re.escape(selector).replace(r'\ ', r'\s*')
        if not re.search(pattern, css_content):
            missing.append(selector)
            print(f"   ❌ FALTANDO: {selector}")
        else:
            print(f"   ✅ PRESENTE: {selector}")
    
    if not missing:
        print("\n✅ Todos os seletores necessários estão presentes!")
        print("\nProblema pode estar em:")
        print("   • Ordem de importação do CSS")
        print("   • Cache do navegador")
        print("   • Conflitos com exec-compact")
        return
    
    print(f"\n❌ Faltam {len(missing)} seletores críticos!")
    
    # 3. Adicionar CSS completo e robusto
    print("\n3️⃣ Adicionando CSS robusto para todas as seções...")
    
    # Encontrar ponto de inserção (após footer, antes do final)
    footer_end = css_content.rfind('.footer-bottom')
    if footer_end == -1:
        print("   ❌ Não encontrou .footer-bottom")
        return
    
    # Encontrar o fechamento do bloco footer
    insert_pos = css_content.find('\n\n', footer_end + 500)
    if insert_pos == -1:
        insert_pos = len(css_content) - 500
    
    print(f"   ✅ Ponto de inserção: posição {insert_pos}")
    
    # CSS robusto e completo
    robust_css = """

/* =======================================================
   PÁGINAS MPA - CSS COMPLETO E ROBUSTO
   (governo.html, empresas.html, pessoas.html)
   ======================================================= */

/* ========== PAGE HEADER (Hero das páginas MPA) ========== */
.page-header {
  padding: var(--space-2xl) var(--space-lg);
  background: linear-gradient(180deg, var(--color-surface-light), var(--color-surface-muted));
}

.page-header-inner {
  max-width: var(--max-width);
  margin: 0 auto;
}

.page-header h1,
.page-header-content h1 {
  font-family: var(--font-display);
  font-size: clamp(2rem, 4vw, 3rem);
  font-weight: 500;
  color: var(--color-text-strong);
  margin-bottom: var(--space-md);
  letter-spacing: -0.02em;
  line-height: 1.2;
}

.page-header p,
.page-header-content p {
  font-size: 1.125rem;
  color: var(--color-text-muted);
  line-height: 1.6;
  margin-bottom: var(--space-lg);
  max-width: 600px;
}

/* ========== TEXT BLOCK (Seções de texto) ========== */
.text-block {
  padding: var(--space-2xl) var(--space-lg);
  background: var(--color-surface-light);
}

.text-block-inner {
  max-width: var(--max-width-narrow);
  margin: 0 auto;
}

.text-block h2 {
  font-family: var(--font-display);
  font-size: clamp(1.75rem, 3vw, 2.5rem);
  font-weight: 500;
  color: var(--color-text-strong);
  margin-bottom: var(--space-lg);
  letter-spacing: -0.01em;
}

.text-block h3 {
  font-family: var(--font-body);
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-text-strong);
  margin-bottom: var(--space-md);
}

.text-block p {
  font-size: 1.0625rem;
  color: var(--color-text-base);
  line-height: 1.7;
  margin-bottom: var(--space-md);
}

.text-block p:last-child {
  margin-bottom: 0;
}

/* ========== STEPS / BENEFITS (Listas de benefícios) ========== */
.steps,
.benefits {
  padding: var(--space-2xl) var(--space-lg);
  background: var(--color-surface-muted);
}

.steps-inner,
.benefits-inner {
  max-width: var(--max-width);
  margin: 0 auto;
}

.steps h2,
.benefits h2 {
  font-family: var(--font-display);
  font-size: clamp(1.75rem, 3vw, 2.5rem);
  font-weight: 500;
  color: var(--color-text-strong);
  text-align: center;
  margin-bottom: var(--space-xl);
  letter-spacing: -0.01em;
}

.steps-list,
.benefits-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--space-lg);
}

.step-item,
.benefit-item {
  background: var(--color-surface-light);
  padding: var(--space-lg);
  border: 1px solid var(--color-border-soft);
  border-radius: 8px;
  text-align: center;
}

.step-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  margin: 0 auto var(--space-md);
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 500;
  color: var(--color-text-strong);
  border: 2px solid var(--color-border-strong);
  border-radius: 50%;
}

.step-item h3,
.benefit-item h3 {
  font-family: var(--font-body);
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-text-strong);
  margin-bottom: var(--space-sm);
}

.step-item p,
.benefit-item p {
  font-size: 0.9375rem;
  color: var(--color-text-base);
  line-height: 1.6;
  margin-bottom: 0;
}

/* ========== CTA FINAL (Call-to-action final) ========== */
.cta-final {
  padding: var(--space-2xl) var(--space-lg);
  background: linear-gradient(135deg, var(--color-green-900), var(--color-green-850));
  text-align: center;
  color: var(--color-text-inverse);
}

.cta-final-inner {
  max-width: var(--max-width-narrow);
  margin: 0 auto;
}

.cta-final h2 {
  font-family: var(--font-display);
  font-size: clamp(1.75rem, 3vw, 2.5rem);
  font-weight: 500;
  color: var(--color-text-inverse);
  margin-bottom: var(--space-md);
}

.cta-final p {
  font-size: 1.125rem;
  color: var(--color-text-inverse);
  opacity: 0.9;
  margin-bottom: var(--space-lg);
  line-height: 1.6;
}

.cta-final .btn-primary {
  background: var(--color-text-inverse);
  color: var(--color-green-900);
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.cta-final .btn-primary:hover {
  background: transparent;
  color: var(--color-text-inverse);
  border-color: var(--color-text-inverse);
}

/* ========== RESPONSIVIDADE MOBILE ========== */
@media (max-width: 768px) {
  .page-header--split {
    grid-template-columns: 1fr;
    gap: var(--space-lg);
  }

  .page-header-graphic {
    display: none;
  }

  .page-header h1,
  .page-header-content h1 {
    font-size: 2rem;
  }

  .steps-list,
  .benefits-list {
    grid-template-columns: 1fr;
    gap: var(--space-md);
  }

  .step-item,
  .benefit-item {
    padding: var(--space-md);
  }

  .text-block,
  .steps,
  .benefits,
  .cta-final {
    padding: var(--space-xl) var(--space-md);
  }
}

/* ========== EXEC COMPACT OVERRIDES ========== */
body.exec-compact .page-header {
  padding: 2.5rem var(--space-lg);
}

body.exec-compact .text-block,
body.exec-compact .steps,
body.exec-compact .benefits {
  padding: 2.5rem var(--space-lg);
}

body.exec-compact .cta-final {
  padding: 3rem var(--space-lg);
}

body.exec-compact .cta-final h2 {
  font-size: 1.6rem;
}

body.exec-compact .cta-final p {
  font-size: 0.9375rem;
}
"""
    
    # 4. Inserir CSS
    print("\n4️⃣ Inserindo CSS robusto...")
    updated_css = css_content[:insert_pos] + robust_css + css_content[insert_pos:]
    
    # 5. Escrever arquivo
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(updated_css)
    
    new_lines = len(robust_css.split('\n'))
    final_lines = len(updated_css.split('\n'))
    
    print(f"   ✅ CSS robusto adicionado: {new_lines} linhas")
    print(f"   ✅ Total final: {final_lines} linhas")
    
    print("\n✅ CORREÇÃO COMPLETA APLICADA!")
    print("\n📋 CSS adicionado:")
    print("   • .page-header (hero)")
    print("   • .page-header h1, p (títulos e subtítulos)")
    print("   • .text-block (seções de texto)")
    print("   • .text-block h2, h3, p (conteúdo)")
    print("   • .steps, .benefits (listas)")
    print("   • .step-item, .benefit-item (cards)")
    print("   • .step-number (números dos passos)")
    print("   • .cta-final (call-to-action)")
    print("   • Media queries mobile (<768px)")
    print("   • Overrides exec-compact")
    
    print("\n✅ Todas as páginas MPA agora devem estar 100% formatadas!")

if __name__ == "__main__":
    main()
