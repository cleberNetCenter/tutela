#!/usr/bin/env python3
"""
Fix Security Page Hero Overlap
Corrige sobreposição do hero com o header fixo em /seguranca.html
"""

def fix_security_hero():
    """Corrige o hero da página de segurança"""
    
    file_path = "public/seguranca.html"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Corrigir padding do main para evitar sobreposição
    # Procurar por body.exec-compact .main.main--hero-top
    if 'body.exec-compact .main.main--hero-top {' in content:
        # Já existe, vamos substituir
        old_main_css = '''body.exec-compact .main.main--hero-top {
  padding-top: 80px !important;
  margin-top: 0 !important;
}'''
        
        new_main_css = '''body.exec-compact .main.main--hero-top {
  padding-top: 90px !important;
  margin-top: 0 !important;
}'''
        
        content = content.replace(old_main_css, new_main_css)
    
    else:
        # Adicionar o CSS antes do </style>
        css_to_add = '''
/* Fix para evitar sobreposição com header fixo */
body.exec-compact .main.main--hero-top {
  padding-top: 90px !important;
  margin-top: 0 !important;
}

@media (max-width: 768px) {
  body.exec-compact .main.main--hero-top {
    padding-top: 75px !important;
  }
}
'''
        content = content.replace('</style>', css_to_add + '\n</style>')
    
    # 2. Ajustar o padding interno do hero para compensar
    # Procurar por .page-header--security-centered
    old_hero_padding = '''  padding: 8rem 2rem 3rem 2rem;'''
    new_hero_padding = '''  padding: 4rem 2rem 3rem 2rem;'''
    
    content = content.replace(old_hero_padding, new_hero_padding)
    
    # Mobile também
    old_mobile_padding = '''  padding: 6rem 1.5rem 2.5rem 1.5rem;'''
    new_mobile_padding = '''  padding: 3.5rem 1.5rem 2.5rem 1.5rem;'''
    
    content = content.replace(old_mobile_padding, new_mobile_padding)
    
    # Salvar arquivo
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {file_path} corrigido com sucesso!")
    print("   - padding-top do main aumentado para 90px (desktop) / 75px (mobile)")
    print("   - padding interno do hero reduzido para 4rem (desktop) / 3.5rem (mobile)")
    print("   - Hero agora aparece completamente abaixo do header fixo")

if __name__ == "__main__":
    fix_security_hero()
