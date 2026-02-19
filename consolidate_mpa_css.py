#!/usr/bin/env python3
"""
Consolidação e Fortalecimento do CSS para páginas MPA
=====================================================
Remover duplicatas e garantir que os estilos sejam aplicados
"""

import re

def main():
    print("🔧 CONSOLIDAÇÃO COMPLETA DO CSS MPA\n")
    
    css_path = "/home/user/webapp/public/assets/css/styles-clean.css"
    
    # 1. Ler CSS
    print("1️⃣ Lendo CSS atual...")
    with open(css_path, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    original_lines = len(css_content.split('\n'))
    print(f"   • Linhas: {original_lines}")
    
    # 2. Remover seção duplicada de MPA (se existir)
    print("\n2️⃣ Removendo duplicatas...")
    
    # Procurar por marcador de MPA pages
    mpa_start = css_content.find('/* Estilos para títulos e texto dentro do page-header */')
    if mpa_start != -1:
        # Encontrar o fim desta seção (próximo comentário principal ou final do arquivo)
        mpa_end = css_content.find('\n\n/* =======', mpa_start + 100)
        if mpa_end == -1:
            mpa_end = css_content.find('\n\n\n/* =======', mpa_start + 100)
        
        if mpa_end != -1:
            print(f"   ✅ Removendo seção duplicada MPA (posição {mpa_start} a {mpa_end})")
            css_content = css_content[:mpa_start] + css_content[mpa_end:]
        else:
            print("   ⚠️  Seção MPA encontrada mas sem fim claro")
    
    # 3. Encontrar ponto de inserção APÓS .footer-bottom, ANTES do WhatsApp
    print("\n3️⃣ Localizando ponto de inserção ideal...")
    
    # Procurar footer-bottom
    footer_bottom = css_content.rfind('.footer-bottom {')
    if footer_bottom == -1:
        print("   ❌ .footer-bottom não encontrado")
        return
    
    # Encontrar o fechamento deste bloco
    brace_count = 0
    insert_pos = footer_bottom
    for i in range(footer_bottom, len(css_content)):
        if css_content[i] == '{':
            brace_count += 1
        elif css_content[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                # Encontrou o fim do bloco
                insert_pos = i + 1
                # Pular até próxima linha dupla
                while insert_pos < len(css_content) and css_content[insert_pos] in '\n\t ':
                    insert_pos += 1
                break
    
    print(f"   ✅ Inserção após .footer-bottom: posição {insert_pos}")
    
    # 4. CSS consolidado e forte
    print("\n4️⃣ Preparando CSS consolidado...")
    
    consolidated_css = """

/* =======================================================
   PÁGINAS MPA - CSS CONSOLIDADO
   (governo.html, empresas.html, pessoas.html)
   ======================================================= */

/* ========== PAGE HEADER ========== */
.page-header {
  padding: var(--space-2xl) var(--space-lg);
  background: linear-gradient(180deg, var(--color-surface-light), var(--color-surface-muted));
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
}

/* ========== TEXT BLOCK ========== */
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

.text-block p {
  font-size: 1.0625rem;
  color: var(--color-text-base);
  line-height: 1.7;
  margin-bottom: var(--space-md);
}

/* ========== STEPS / BENEFITS ========== */
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
}

/* ========== CTA FINAL ========== */
.cta-final {
  padding: var(--space-2xl) var(--space-lg);
  background: linear-gradient(135deg, var(--color-green-900), var(--color-green-850));
  text-align: center;
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
}

.cta-final .btn-primary {
  background: var(--color-text-inverse);
  color: var(--color-green-900);
}

.cta-final .btn-primary:hover {
  background: transparent;
  color: var(--color-text-inverse);
  border-color: var(--color-text-inverse);
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .page-header--split {
    grid-template-columns: 1fr;
  }
  
  .page-header-graphic {
    display: none;
  }
  
  .steps-list,
  .benefits-list {
    grid-template-columns: 1fr;
  }
}
"""
    
    # 5. Inserir CSS consolidado
    print("\n5️⃣ Inserindo CSS consolidado...")
    updated_css = css_content[:insert_pos] + consolidated_css + css_content[insert_pos:]
    
    # 6. Escrever arquivo
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(updated_css)
    
    final_lines = len(updated_css.split('\n'))
    added_lines = len(consolidated_css.split('\n'))
    
    print(f"   ✅ CSS consolidado adicionado: {added_lines} linhas")
    print(f"   ✅ Total final: {final_lines} linhas")
    
    print("\n✅ CONSOLIDAÇÃO COMPLETA!")
    print("\n📋 CSS garantido:")
    print("   • .page-header (hero com gradient)")
    print("   • .page-header h1, p (Cormorant + DM Sans)")
    print("   • .text-block (seções intermediárias)")
    print("   • .steps, .benefits (listas com grid)")
    print("   • .step-item, .step-number (cards numerados)")
    print("   • .cta-final (call-to-action verde)")
    print("   • Media queries mobile")
    
    print("\n🎯 Páginas governo/empresas/pessoas devem estar 100% formatadas!")

if __name__ == "__main__":
    main()
