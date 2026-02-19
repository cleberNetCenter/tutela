#!/usr/bin/env python3
"""
Fix CTA Buttons - ALL Pages
Adiciona data-i18n e CSS 3D em todas as páginas HTML
"""

import re
import os

def fix_page(file_path):
    """Corrige uma página HTML"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes = 0
    
    # 1. HEADER CTA - adicionar data-i18n se não tiver
    if 'class="header-cta"' in content and 'data-i18n="global.cta_button"' not in content:
        # Pattern mais flexível
        pattern = r'(<a class="header-cta"[^>]*)(>)'
        if re.search(pattern, content):
            # Verificar se já tem data-i18n
            match = re.search(pattern, content)
            if match and 'data-i18n' not in match.group(1):
                content = re.sub(
                    pattern,
                    r'\1 data-i18n="global.cta_button"\2',
                    content,
                    count=1
                )
                changes += 1
                print(f"   ✅ Header CTA: data-i18n adicionado")
    
    # 2. BOTÕES .btn-primary - adicionar data-i18n se não tiver
    pattern = r'(<a class="btn btn-primary"[^>]*)(>)(Acessar a Plataforma)</a>'
    matches = re.findall(pattern, content)
    
    for match in matches:
        tag_start = match[0]
        if 'data-i18n' not in tag_start:
            old = tag_start + match[1] + match[2] + '</a>'
            new = tag_start + ' data-i18n="global.cta_button"' + match[1] + match[2] + '</a>'
            content = content.replace(old, new, 1)
            changes += 1
    
    if changes > 0:
        print(f"   ✅ {changes} botão(ões) .btn-primary com data-i18n adicionado")
    
    # 3. ADICIONAR CSS 3D se não existir
    if '.header-cta' in content and 'border-radius: 8px !important' not in content:
        css_to_add = '''
/* ================================
   CTA BUTTONS - 3D STYLE
================================ */
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
        
        # Inserir antes do </head>
        content = content.replace('</head>', '<style>' + css_to_add + '\n</style>\n</head>')
        changes += 1
        print(f"   ✅ CSS 3D adicionado")
    
    # Salvar
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return changes

def main():
    """Processa todas as páginas HTML"""
    
    pages = [
        'public/index.html',
        'public/governo.html',
        'public/empresas.html',
        'public/pessoas.html',
        'public/como-funciona.html',
        'public/seguranca.html'
    ]
    
    total_changes = 0
    
    for page in pages:
        if os.path.exists(page):
            print(f"\n📄 {page}")
            changes = fix_page(page)
            total_changes += changes
            if changes == 0:
                print(f"   ⏭️  Já está correto")
    
    print(f"\n\n✅ Total: {total_changes} alterações em {len(pages)} páginas")

if __name__ == "__main__":
    print("🔧 Corrigindo TODOS os botões CTA...\n")
    main()
    print("\n✅ Correção concluída!")
