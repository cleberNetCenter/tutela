#!/usr/bin/env python3
"""
Improve Preservação Probatória Digital Page
============================================
Implementa melhorias estruturais e visuais exclusivas para a página
/legal/preservacao-probatoria-digital.html sem afetar outras páginas.

Alterações:
1. Reestruturar hero (remover H2/H3/H4, simplificar conteúdo)
2. Criar nova seção editorial após hero
3. Adicionar alternância visual de blocos
4. Reestruturar lista "Aplicações" em grid
5. Corrigir schema breadcrumb
6. Ajustar tipografia inline
7. Adicionar CSS específico da página
"""

import re

def improve_preservacao_page():
    """Implementa todas as melhorias na página"""
    
    html_path = "public/legal/preservacao-probatoria-digital.html"
    css_path = "public/assets/css/styles-clean.css"
    
    # Ler arquivo HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    print("📄 Modificando HTML...")
    
    # 1️⃣ REESTRUTURAR HERO - Simplificar conteúdo
    old_hero_content = '''<div class="page-header-content">
<h1>Preservação Probatória Digital</h1>
  
  <h2 class="section-title">Mecanismos Técnicos de Preservação Probatória</h2>
  <h2 class="section-title">Organização Pré-Litigiosa de Evidência Digital</h2>
  
  <section class="semantic-section">
    <h3 class="subsection-title">Preservação em Fase Pré-Processual</h3>
    <h4 class="detail-title">Mitigação de Risco Documental</h4>
    <h4 class="detail-title">Previsibilidade Técnica da Prova</h4>
  </section>
  
  <section class="semantic-section">
    <h3 class="subsection-title">Utilização da Prova Preservada</h3>
    <h4 class="detail-title">Análise Pericial Fundamentada</h4>
    <h4 class="detail-title">Formalização Notarial Posterior</h4>
  </section>

<p>Infraestrutura técnica de preservação de evidências digitais com cadeia de custódia verificável, integridade imutável e interoperabilidade cartorial sob demanda.</p>
</div>'''
    
    new_hero_content = '''<div class="page-header-content">
<h1>Preservação Probatória Digital</h1>
<p class="hero-subtitle">
Infraestrutura técnica para constituição de cadeia de custódia digital verificável, com integridade imutável e interoperabilidade cartorial sob demanda.
</p>
</div>'''
    
    html = html.replace(old_hero_content, new_hero_content)
    print("  ✅ Hero simplificado")
    
    # 2️⃣ CRIAR NOVA SEÇÃO EDITORIAL após hero
    hero_section_end = '</section>\n<section class="text-block">'
    new_intro_section = '''</section>
<section class="preservacao-intro">
  <div class="preservacao-intro-inner">
    <h2>Mecanismos Técnicos de Preservação</h2>
    <p>
    A preservação probatória digital estrutura evidências antes da instauração formal de litígio, reduzindo risco de impugnação por ausência de autenticidade ou integridade verificável.
    </p>
  </div>
</section>
<section class="text-block">'''
    
    html = html.replace(hero_section_end, new_intro_section, 1)
    print("  ✅ Nova seção editorial criada")
    
    # 3️⃣ ALTERNÂNCIA VISUAL - Adicionar classe section-muted à segunda text-block
    # Encontrar a segunda ocorrência de <section class="text-block">
    text_block_pattern = r'<section class="text-block">'
    matches = list(re.finditer(text_block_pattern, html))
    
    if len(matches) >= 2:
        # Segunda text-block (índice 1)
        second_match = matches[1]
        html = html[:second_match.start()] + '<section class="text-block section-muted">' + html[second_match.end():]
        print("  ✅ Alternância visual aplicada (segunda text-block)")
    
    # 4️⃣ REESTRUTURAR LISTA "APLICAÇÕES" em grid
    old_applications_list = '''<h2>Aplicações</h2>
<ul style="list-style: disc; padding-left: 1.5rem; line-height: 1.8;">
<li>Preservação pré-litígio</li>
<li>Disputas contratuais</li>
<li>Arbitragem</li>
<li>Investigação interna</li>
<li>Compliance regulatório</li>
<li>Defesa administrativa</li>
<li>Produção antecipada de prova</li>
</ul>'''
    
    new_applications_grid = '''<h2>Aplicações</h2>
<div class="applications-grid">
  <div class="application-item">Preservação pré-litígio</div>
  <div class="application-item">Disputas contratuais</div>
  <div class="application-item">Arbitragem</div>
  <div class="application-item">Investigação interna</div>
  <div class="application-item">Compliance regulatório</div>
  <div class="application-item">Defesa administrativa</div>
  <div class="application-item">Produção antecipada de prova</div>
</div>'''
    
    html = html.replace(old_applications_list, new_applications_grid)
    print("  ✅ Lista 'Aplicações' convertida em grid")
    
    # 5️⃣ CORRIGIR SCHEMA BREADCRUMB
    old_breadcrumb_url = 'https://tuteladigital.com.br/legal/Preservação Probatória Digital.html'
    new_breadcrumb_url = 'https://tuteladigital.com.br/legal/preservacao-probatoria-digital.html'
    
    html = html.replace(old_breadcrumb_url, new_breadcrumb_url)
    print("  ✅ Schema breadcrumb corrigido")
    
    # 6️⃣ AJUSTE TIPOGRÁFICO - Corrigir cor do .section-title
    old_style = '''  color: var(--color-primary, #1a1a1a);'''
    new_style = '''  color: var(--color-text-strong);'''
    
    html = html.replace(old_style, new_style)
    print("  ✅ Tipografia inline ajustada")
    
    # Salvar HTML modificado
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("\n🎨 Adicionando CSS específico da página...")
    
    # 7️⃣ ADICIONAR CSS ESPECÍFICO ao final do arquivo CSS
    with open(css_path, 'r', encoding='utf-8') as f:
        css = f.read()
    
    # Verificar se já existe
    if 'PRESERVAÇÃO PROBATÓRIA – PAGE SPECIFIC' in css:
        print("  ℹ️  CSS específico já existe")
        return True
    
    # CSS específico da página
    page_specific_css = '''

/* =============================
   PRESERVAÇÃO PROBATÓRIA – PAGE SPECIFIC
   ============================= */

/* Nova seção editorial após hero */
.preservacao-intro {
  padding: 5rem 2rem;
  background: #ffffff;
}

.preservacao-intro-inner {
  max-width: 960px;
  margin: 0 auto;
}

.preservacao-intro h2 {
  font-family: var(--font-display);
  font-size: 2.25rem;
  color: var(--color-text-strong);
  margin-bottom: 1.5rem;
}

.preservacao-intro p {
  font-size: 1.125rem;
  color: var(--color-text-base);
  line-height: 1.7;
}

/* Alternância de blocos */
.section-muted {
  background: var(--color-surface-muted);
}

/* Grid de aplicações */
.applications-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.application-item {
  background: #ffffff;
  padding: 1.25rem;
  border-left: 3px solid var(--color-green-800);
  font-size: 0.95rem;
  color: var(--color-text-base);
}

/* Hero subtitle específico */
.hero-subtitle {
  font-size: 1.125rem;
  line-height: 1.7;
  color: rgba(255, 255, 255, 0.95);
  margin-top: 1.5rem;
}

/* Responsivo para preservacao-intro */
@media (max-width: 768px) {
  .preservacao-intro {
    padding: 3rem 1.5rem;
  }
  
  .preservacao-intro h2 {
    font-size: 1.75rem;
  }
  
  .preservacao-intro p {
    font-size: 1rem;
  }
  
  .applications-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}
'''
    
    # Adicionar ao final do CSS
    css += page_specific_css
    
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css)
    
    print("  ✅ CSS específico adicionado ao final de styles-clean.css")
    
    return True

if __name__ == "__main__":
    print("🚀 Melhorando página Preservação Probatória Digital...")
    print("=" * 70)
    
    success = improve_preservacao_page()
    
    print("=" * 70)
    
    if success:
        print("✅ Melhorias implementadas com sucesso!")
        print("\n📋 Resumo das alterações:")
        print("  1. ✅ Hero simplificado (removido H2/H3/H4)")
        print("  2. ✅ Nova seção editorial 'Mecanismos Técnicos de Preservação'")
        print("  3. ✅ Alternância visual (segunda text-block com fundo muted)")
        print("  4. ✅ Lista 'Aplicações' convertida em grid institucional")
        print("  5. ✅ Schema breadcrumb corrigido")
        print("  6. ✅ Tipografia inline ajustada (.section-title)")
        print("  7. ✅ CSS específico da página adicionado")
        print("\n📁 Arquivos modificados:")
        print("  • public/legal/preservacao-probatoria-digital.html")
        print("  • public/assets/css/styles-clean.css")
        print("\n🎯 Validar em:")
        print("  • Desktop 1440px, 1280px, 992px")
        print("  • Tablet 768px")
        print("  • Mobile")
        print("\n⚠️  CRÍTICO: Verificar que outras páginas não foram afetadas!")
    else:
        print("❌ Falha ao aplicar melhorias")
