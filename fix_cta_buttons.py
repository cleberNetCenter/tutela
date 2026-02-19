#!/usr/bin/env python3
"""
Fix CTA Buttons: i18n + 3D Style
1. Adicionar data-i18n="global.cta_button" em todos os botões sem i18n
2. Adicionar CSS 3D com cantos arredondados (header-cta e btn-primary)
"""

import re

def fix_cta_buttons():
    """Corrige botões CTA com i18n e estilo 3D"""
    
    file_path = "public/index.html"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. ADICIONAR data-i18n no HEADER CTA
    # Buscar: <a class="header-cta" ...>Acessar a Plataforma</a>
    old_header_cta = '<a class="header-cta" href="https://app.tuteladigital.com.br/" rel="noopener noreferrer" target="_blank">\n\t\t\t\t\t  Acessar a Plataforma\n\t\t\t\t\t</a>'
    
    new_header_cta = '<a class="header-cta" href="https://app.tuteladigital.com.br/" rel="noopener noreferrer" target="_blank" data-i18n="global.cta_button">\n\t\t\t\t\t  Acessar a Plataforma\n\t\t\t\t\t</a>'
    
    content = content.replace(old_header_cta, new_header_cta)
    
    # 2. ADICIONAR data-i18n em TODOS OS BOTÕES .btn-primary SEM data-i18n
    # Regex para encontrar botões sem data-i18n
    pattern = r'(<a class="btn btn-primary" href="https://app\.tuteladigital\.com\.br/" rel="noopener noreferrer" target="_blank")>Acessar a Plataforma</a>'
    
    replacement = r'\1 data-i18n="global.cta_button">Acessar a Plataforma</a>'
    
    content = re.sub(pattern, replacement, content)
    
    # 3. ADICIONAR CSS 3D para .header-cta e .btn-primary
    css_to_add = '''
/* ================================
   CTA BUTTONS - 3D STYLE
================================ */
/* Header CTA - 3D com cantos arredondados */
.header-cta {
  border-radius: 8px !important;
  box-shadow: 
    0 4px 6px rgba(0, 0, 0, 0.1),
    0 2px 4px rgba(0, 0, 0, 0.06),
    inset 0 -2px 0 rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
  position: relative;
  top: 0;
}

.header-cta:hover {
  box-shadow: 
    0 6px 10px rgba(0, 0, 0, 0.15),
    0 3px 6px rgba(0, 0, 0, 0.1),
    inset 0 -2px 0 rgba(0, 0, 0, 0.15);
  top: -2px;
}

.header-cta:active {
  box-shadow: 
    0 2px 4px rgba(0, 0, 0, 0.1),
    inset 0 2px 4px rgba(0, 0, 0, 0.15);
  top: 2px;
}

/* Botões CTA Primários - 3D com cantos arredondados */
.btn-primary {
  border-radius: 8px !important;
  box-shadow: 
    0 4px 6px rgba(0, 0, 0, 0.1),
    0 2px 4px rgba(0, 0, 0, 0.06),
    inset 0 -2px 0 rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
  position: relative;
  top: 0;
}

.btn-primary:hover {
  box-shadow: 
    0 6px 10px rgba(0, 0, 0, 0.15),
    0 3px 6px rgba(0, 0, 0, 0.1),
    inset 0 -2px 0 rgba(0, 0, 0, 0.15);
  top: -2px;
}

.btn-primary:active {
  box-shadow: 
    0 2px 4px rgba(0, 0, 0, 0.1),
    inset 0 2px 4px rgba(0, 0, 0, 0.15);
  top: 2px;
}
'''
    
    # Inserir CSS antes do </style> final
    content = content.replace('</style>\n\n</head>', css_to_add + '\n</style>\n\n</head>')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {file_path} corrigido:")
    print("   - data-i18n=\"global.cta_button\" adicionado ao header-cta")
    print("   - data-i18n=\"global.cta_button\" adicionado a todos os .btn-primary")
    print("   - CSS 3D com cantos arredondados (8px) aplicado")
    print("   - Efeito hover: eleva -2px")
    print("   - Efeito active: desce +2px (pressionar)")
    print("   - Box-shadow com múltiplas camadas (profundidade)")

if __name__ == "__main__":
    print("🔧 Corrigindo botões CTA (i18n + 3D)...\n")
    fix_cta_buttons()
    print("\n✅ Correção aplicada com sucesso!")
