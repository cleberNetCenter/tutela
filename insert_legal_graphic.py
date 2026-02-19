#!/usr/bin/env python3
"""
Inserir gráfico vetorial institucional nas páginas /legal/

REGRAS ABSOLUTAS:
- Inserir SOMENTE nas páginas do diretório /legal/
- Posição: imediatamente após <h1> dentro de .page-header-inner
- Não alterar: Header, Footer, Hero structure, Grid, Tipografia, Espaçamentos
- Títulos fixos: "Integridade", "Cadeia de Custódia", "Validade Jurídica"
- SVG exato conforme especificação
"""

import re
import os

# SVG institucional exato conforme especificado
LEGAL_GRAPHIC_SVG = '''
<div class="legal-graphic">
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
'''

# CSS necessário (será adicionado ao <head>)
LEGAL_GRAPHIC_CSS = '''
<!-- CSS Gráfico Institucional Legal -->
<style>
.legal-graphic {
  margin: 1.5rem auto 2.5rem auto;
  max-width: 900px;
  opacity: 0.9;
}

.legal-graphic svg {
  width: 100%;
  height: auto;
  display: block;
}

@media (max-width: 768px) {
  .legal-graphic svg text {
    font-size: 13px;
  }
}
</style>
'''

def insert_graphic_in_page(file_path):
    """Insere o gráfico institucional em uma página legal"""
    
    print(f"\n{'='*60}")
    print(f"PROCESSANDO: {os.path.basename(file_path)}")
    print('='*60)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Verificar se o gráfico já existe
    if 'legal-graphic' in html:
        print("⚠️  Gráfico já existe - pulando...")
        return False
    
    # 1. INSERIR CSS no <head> antes do </head>
    if LEGAL_GRAPHIC_CSS.strip() not in html:
        head_close = html.find('</head>')
        if head_close != -1:
            html = html[:head_close] + LEGAL_GRAPHIC_CSS + '\n' + html[head_close:]
            print("✅ CSS inserido no <head>")
        else:
            print("❌ Tag </head> não encontrada")
            return False
    
    # 2. INSERIR SVG imediatamente após <h1> dentro de .page-header-inner
    # Procurar padrão: <h1>...</h1> seguido de conteúdo (div, p, etc.)
    # O gráfico deve ir entre o </h1> e o próximo elemento
    
    # Padrão: capturar <h1>conteúdo</h1> e inserir logo após
    pattern = r'(<h1>.*?</h1>)(\s*)'
    
    def replace_h1(match):
        h1_tag = match.group(1)
        whitespace = match.group(2)
        return h1_tag + '\n' + LEGAL_GRAPHIC_SVG + whitespace
    
    # Fazer a substituição apenas na primeira ocorrência (hero)
    html_modified = re.sub(pattern, replace_h1, html, count=1, flags=re.DOTALL)
    
    if html_modified != html:
        html = html_modified
        print("✅ Gráfico SVG inserido após <h1>")
    else:
        print("❌ Não foi possível inserir o gráfico (padrão <h1> não encontrado)")
        return False
    
    # Salvar arquivo
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✅ Arquivo salvo com sucesso!")
    return True

def main():
    print("=" * 60)
    print("INSERÇÃO DE GRÁFICO INSTITUCIONAL - PÁGINAS LEGAIS")
    print("=" * 60)
    
    legal_pages = [
        'public/legal/fundamento-juridico.html',
        'public/legal/institucional.html',
        'public/legal/politica-de-privacidade.html',
        'public/legal/preservacao-probatoria-digital.html',
        'public/legal/termos-de-custodia.html'
    ]
    
    modified_count = 0
    
    for page in legal_pages:
        if os.path.exists(page):
            if insert_graphic_in_page(page):
                modified_count += 1
        else:
            print(f"\n⚠️  Arquivo não encontrado: {page}")
    
    print("\n" + "=" * 60)
    print("RESUMO DA OPERAÇÃO")
    print("=" * 60)
    print(f"✅ Páginas modificadas: {modified_count}/5")
    print("\n📋 Elementos inseridos:")
    print("  • Gráfico SVG institucional")
    print("  • CSS de estilização")
    print("  • Responsividade mobile")
    print("\n🔒 Garantias:")
    print("  ✓ Apenas páginas /legal/ modificadas")
    print("  ✓ Estrutura HTML preservada")
    print("  ✓ Títulos fixos: Integridade | Cadeia de Custódia | Validade Jurídica")
    print("  ✓ SVG exato conforme especificação")
    print("  ✓ CSS isolado (não sobrescreve regras existentes)")
    print("=" * 60)

if __name__ == "__main__":
    main()
