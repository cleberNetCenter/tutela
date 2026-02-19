#!/usr/bin/env python3
"""
Adicionar CSS faltante para páginas governo/empresas/pessoas
============================================================
Problema: Páginas .page-header não têm estilos para h1, h2, p
Solução: Adicionar CSS específico para essas páginas MPA
"""

import os

def main():
    print("🔧 ADICIONANDO CSS PARA PÁGINAS GOVERNO/EMPRESAS/PESSOAS\n")
    
    css_path = "/home/user/webapp/public/assets/css/styles-clean.css"
    
    # 1. Ler CSS atual
    print("1️⃣ Lendo CSS atual...")
    with open(css_path, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    original_lines = len(css_content.split('\n'))
    print(f"   ✅ CSS atual: {original_lines} linhas")
    
    # 2. Encontrar onde inserir (após .page-header-content)
    print("\n2️⃣ Localizando ponto de inserção...")
    
    # Buscar linha com .page-header-content {
    lines = css_content.split('\n')
    insert_index = -1
    
    for i, line in enumerate(lines):
        if '.page-header-content {' in line:
            # Encontrar o fechamento deste bloco
            brace_count = 0
            for j in range(i, len(lines)):
                if '{' in lines[j]:
                    brace_count += lines[j].count('{')
                if '}' in lines[j]:
                    brace_count -= lines[j].count('}')
                if brace_count == 0:
                    insert_index = j + 1
                    break
            break
    
    if insert_index == -1:
        print("   ❌ Não foi possível encontrar .page-header-content")
        return
    
    print(f"   ✅ Ponto de inserção encontrado: linha {insert_index}")
    
    # 3. CSS a ser adicionado
    print("\n3️⃣ Preparando CSS para páginas MPA...")
    
    new_css = """
\t\t/* Estilos para títulos e texto dentro do page-header */
\t\t.page-header h1,
\t\t.page-header-content h1 {
\t\t\tfont-family: var(--font-display);
\t\t\tfont-size: clamp(2rem, 4vw, 3rem);
\t\t\tfont-weight: 500;
\t\t\tcolor: var(--color-text-strong);
\t\t\tmargin-bottom: var(--space-md);
\t\t\tletter-spacing: -0.02em;
\t\t\tline-height: 1.2;
\t\t}

\t\t.page-header p,
\t\t.page-header-content p {
\t\t\tfont-size: 1.125rem;
\t\t\tcolor: var(--color-text-muted);
\t\t\tline-height: 1.6;
\t\t\tmargin-bottom: var(--space-lg);
\t\t}

\t\t/* Seções de conteúdo */
\t\t.content-section {
\t\t\tpadding: var(--space-2xl) var(--space-lg);
\t\t\tbackground: var(--color-surface-light);
\t\t}

\t\t.content-section-inner {
\t\t\tmax-width: var(--max-width);
\t\t\tmargin: 0 auto;
\t\t}

\t\t.content-section h2 {
\t\t\tfont-family: var(--font-display);
\t\t\tfont-size: clamp(1.75rem, 3vw, 2.5rem);
\t\t\tfont-weight: 500;
\t\t\tcolor: var(--color-text-strong);
\t\t\tmargin-bottom: var(--space-lg);
\t\t\tletter-spacing: -0.01em;
\t\t}

\t\t.content-section h3 {
\t\t\tfont-family: var(--font-body);
\t\t\tfont-size: 1.25rem;
\t\t\tfont-weight: 600;
\t\t\tcolor: var(--color-text-strong);
\t\t\tmargin-bottom: var(--space-md);
\t\t}

\t\t.content-section p {
\t\t\tfont-size: 1rem;
\t\t\tcolor: var(--color-text-base);
\t\t\tline-height: 1.7;
\t\t\tmargin-bottom: var(--space-md);
\t\t}

\t\t/* Steps/Benefits sections */
\t\t.steps,
\t\t.benefits {
\t\t\tpadding: var(--space-2xl) var(--space-lg);
\t\t\tbackground: var(--color-surface-muted);
\t\t}

\t\t.steps-inner,
\t\t.benefits-inner {
\t\t\tmax-width: var(--max-width);
\t\t\tmargin: 0 auto;
\t\t}

\t\t.steps h2,
\t\t.benefits h2 {
\t\t\tfont-family: var(--font-display);
\t\t\tfont-size: clamp(1.75rem, 3vw, 2.5rem);
\t\t\tfont-weight: 500;
\t\t\tcolor: var(--color-text-strong);
\t\t\ttext-align: center;
\t\t\tmargin-bottom: var(--space-xl);
\t\t\tletter-spacing: -0.01em;
\t\t}

\t\t.steps-list,
\t\t.benefits-list {
\t\t\tdisplay: grid;
\t\t\tgrid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
\t\t\tgap: var(--space-lg);
\t\t}

\t\t.step-item,
\t\t.benefit-item {
\t\t\tbackground: var(--color-surface-light);
\t\t\tpadding: var(--space-lg);
\t\t\tborder: 1px solid var(--color-border-soft);
\t\t\tborder-radius: 8px;
\t\t}

\t\t.step-item h3,
\t\t.benefit-item h3 {
\t\t\tfont-family: var(--font-body);
\t\t\tfont-size: 1.125rem;
\t\t\tfont-weight: 600;
\t\t\tcolor: var(--color-text-strong);
\t\t\tmargin-bottom: var(--space-sm);
\t\t}

\t\t.step-item p,
\t\t.benefit-item p {
\t\t\tfont-size: 0.9375rem;
\t\t\tcolor: var(--color-text-base);
\t\t\tline-height: 1.6;
\t\t}

\t\t/* Responsividade para páginas MPA */
\t\t@media (max-width: 768px) {
\t\t\t.page-header--split {
\t\t\t\tgrid-template-columns: 1fr;
\t\t\t\tgap: var(--space-lg);
\t\t\t}

\t\t\t.page-header-graphic {
\t\t\t\tdisplay: none;
\t\t\t}

\t\t\t.page-header h1,
\t\t\t.page-header-content h1 {
\t\t\t\tfont-size: 2rem;
\t\t\t}

\t\t\t.steps-list,
\t\t\t.benefits-list {
\t\t\t\tgrid-template-columns: 1fr;
\t\t\t}
\t\t}
"""
    
    new_lines = len(new_css.split('\n'))
    print(f"   ✅ CSS preparado: {new_lines} linhas")
    
    # 4. Inserir CSS
    print("\n4️⃣ Inserindo CSS no arquivo...")
    lines.insert(insert_index, new_css)
    
    # 5. Escrever arquivo
    updated_css = '\n'.join(lines)
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(updated_css)
    
    final_lines = len(updated_css.split('\n'))
    print(f"   ✅ Arquivo atualizado!")
    
    # 6. Resumo
    print("\n📊 RESULTADO:")
    print(f"   • Linhas antes: {original_lines}")
    print(f"   • Linhas adicionadas: {new_lines}")
    print(f"   • Linhas depois: {final_lines}")
    print(f"   • Inserção na linha: {insert_index}")
    
    print("\n✅ CSS PARA PÁGINAS MPA ADICIONADO!")
    print("\n📋 Estilos adicionados:")
    print("   • .page-header h1, .page-header-content h1 (títulos)")
    print("   • .page-header p, .page-header-content p (subtítulos)")
    print("   • .content-section (seções de conteúdo)")
    print("   • .steps, .benefits (listas de benefícios)")
    print("   • .step-item, .benefit-item (cards)")
    print("   • Media queries mobile (responsividade)")
    
    print("\n✅ Páginas governo.html, empresas.html, pessoas.html agora têm formatação completa!")

if __name__ == "__main__":
    main()
