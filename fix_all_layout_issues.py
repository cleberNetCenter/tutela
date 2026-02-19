#!/usr/bin/env python3
"""
Fix All Layout Issues
1. Corrigir fonte e alinhamento de "Pilares de Segurança" 
2. Mudar cards de 1 coluna para 2 colunas (grid 2x3)
3. Ocultar páginas SPA após o rodapé no index.html
"""

def fix_security_page():
    """Corrige layout da página de segurança"""
    
    file_path = "public/seguranca.html"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. CORRIGIR CSS DO SUBTITLE - Fonte display + centralizado
    old_subtitle_css = """.security-subtitle {
  text-align: center;
  font-size: 1.125rem;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--color-text-muted);
  margin-bottom: 2.5rem;
}"""
    
    new_subtitle_css = """.security-subtitle {
  font-family: var(--font-display);
  text-align: center;
  font-size: 1.125rem;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--color-text-muted);
  margin-bottom: 2.5rem;
}"""
    
    content = content.replace(old_subtitle_css, new_subtitle_css)
    
    # 2. MUDAR CARDS DE COLUNA PARA GRID 2x3
    old_cards_css = """.security-cards {
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
  max-width: 760px;
  margin: 3rem auto 0 auto;
}"""
    
    new_cards_css = """.security-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
  max-width: 1000px;
  margin: 3rem auto 0 auto;
}"""
    
    content = content.replace(old_cards_css, new_cards_css)
    
    # 3. AJUSTAR RESPONSIVO - MOBILE VOLTA PARA 1 COLUNA
    old_mobile_cards = """  .security-cards {
    gap: 2rem;
    max-width: 100%;
    padding: 0 1.5rem;
  }"""
    
    new_mobile_cards = """  .security-cards {
    grid-template-columns: 1fr;
    gap: 1.5rem;
    max-width: 100%;
    padding: 0 1.5rem;
  }"""
    
    content = content.replace(old_mobile_cards, new_mobile_cards)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {file_path} corrigido:")
    print("   - Fonte de 'Pilares de Segurança': var(--font-display)")
    print("   - Layout: 2 cards por linha (grid 2x3)")
    print("   - Mobile: 1 card por linha")

def fix_spa_pages_visibility():
    """Oculta páginas SPA que aparecem após o rodapé"""
    
    file_path = "public/index.html"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Procurar por CSS existente ou adicionar antes do </style>
    css_to_add = """
/* ================================
   FIX: OCULTAR PÁGINAS SPA INATIVAS
================================ */
.content {
  display: none;
}

.content.active {
  display: block;
}

/* Garantir que apenas a página home seja visível por padrão */
#page-home {
  display: block;
}
"""
    
    # Verificar se já existe algum CSS para .content
    if '.content {' not in content:
        # Adicionar antes do </style> final (antes do </head>)
        content = content.replace('</style>', css_to_add + '\n</style>', 1)
    else:
        # Substituir CSS existente
        # Procurar padrão existente e substituir
        import re
        # Se já existir, vamos adicionar display:none como prioridade
        if 'display: none' not in content or '.content.active' not in content:
            content = content.replace('</style>', css_to_add + '\n</style>', 1)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ {file_path} corrigido:")
    print("   - Páginas SPA ocultas por padrão (.content { display: none })")
    print("   - Apenas página ativa visível (.content.active { display: block })")
    print("   - Home visível por padrão (#page-home { display: block })")

if __name__ == "__main__":
    print("🔧 Iniciando correções de layout...\n")
    fix_security_page()
    fix_spa_pages_visibility()
    print("\n✅ Todas as correções aplicadas com sucesso!")
