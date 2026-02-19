#!/usr/bin/env python3
"""
Fix Homepage Infrastructure Section Layout
1. Mover título "Pilares da Infraestrutura" para fora do .features-inner
2. Aplicar fonte display no título
3. Converter cards de 3 colunas para grid 2x2
4. Centralizar cards com max-width
"""

import re

def fix_homepage_infrastructure():
    """Corrige a seção 'Pilares da Infraestrutura' na homepage"""
    
    file_path = "public/index.html"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. REESTRUTURAR HTML - Mover H2 para fora do .features-inner
    old_html = '''<section class="features">
<div class="features-inner">
<h2 data-i18n="home_pillars_title">Pilares da Infraestrutura</h2>
<div class="features-grid">'''
    
    new_html = '''<section class="features features--homepage-pillars">
<h2 class="features-title-centered" data-i18n="home_pillars_title">Pilares da Infraestrutura</h2>
<div class="features-inner">
<div class="features-grid features-grid--2x2">'''
    
    content = content.replace(old_html, new_html)
    
    # 2. ADICIONAR CSS INLINE NO <head> (antes do </style> existente)
    css_to_add = '''
/* ================================
   HOMEPAGE - PILARES DA INFRAESTRUTURA
================================ */
/* Título centralizado fora do container */
.features--homepage-pillars {
  padding: 4rem 2rem 3rem 2rem;
}

.features-title-centered {
  font-family: var(--font-display);
  font-size: clamp(1.8rem, 3vw, 2.3rem);
  font-weight: 500;
  text-align: center;
  color: var(--color-text-strong);
  margin: 0 0 3rem 0;
  letter-spacing: -0.01em;
}

/* Grid 2x2 centralizado */
.features-grid--2x2 {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2.5rem;
  max-width: 960px;
  margin: 0 auto;
}

.features-grid--2x2 .feature-item {
  text-align: center;
  padding: 2rem;
}

/* Responsivo - Mobile 1 coluna */
@media (max-width: 768px) {
  .features--homepage-pillars {
    padding: 3rem 1.5rem 2rem 1.5rem;
  }
  
  .features-grid--2x2 {
    grid-template-columns: 1fr;
    gap: 2rem;
    max-width: 100%;
  }
  
  .features-grid--2x2 .feature-item {
    padding: 1.5rem;
  }
}
'''
    
    # Procurar o último </style> antes do </head>
    # Inserir o CSS antes do fechamento do style do hero
    content = content.replace('</style>\n\n</head>', css_to_add + '\n</style>\n\n</head>')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {file_path} corrigido:")
    print("   - Título movido para fora do .features-inner")
    print("   - Fonte do título: var(--font-display)")
    print("   - Layout: Grid 2x2 (2 cards por linha)")
    print("   - Cards centralizados (max-width: 960px)")
    print("   - Mobile: 1 coluna")

if __name__ == "__main__":
    print("🔧 Corrigindo seção 'Pilares da Infraestrutura'...\n")
    fix_homepage_infrastructure()
    print("\n✅ Correção aplicada com sucesso!")
