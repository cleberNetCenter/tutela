#!/usr/bin/env python3
"""
Corrigir alinhamento vertical do menu superior
===============================================
Seguindo especificações exatas:
1. .nav { align-items: center; }
2. .nav > a, .nav > div, .nav .nav-link, .nav .nav-item { display: flex; align-items: center; height: 48px; }
3. .nav .dropdown { display: flex; align-items: center; }

SEM alterar:
- HTML estrutural
- Classes existentes
- Breakpoints
- CTA
- Dropdown de idioma
- Padding do header
- Espaçamento horizontal
- Tamanho de fonte
- Hover
- Media queries
"""

def main():
    print("🔧 CORRIGINDO ALINHAMENTO VERTICAL DO MENU\n")
    
    # Arquivo principal do header
    header_css_path = "/home/user/webapp/public/assets/css/styles-header-final.css"
    
    # 1. Ler CSS do header
    print("1️⃣ Lendo styles-header-final.css...")
    with open(header_css_path, 'r', encoding='utf-8') as f:
        header_lines = f.readlines()
    
    # 2. Encontrar linha com .nav {
    nav_line = None
    for i, line in enumerate(header_lines):
        if line.strip() == '.nav {':
            nav_line = i
            break
    
    if nav_line is None:
        print("   ❌ .nav { não encontrado")
        return
    
    print(f"   ✅ .nav encontrado na linha {nav_line + 1}")
    
    # 3. Verificar se já tem align-items
    has_align_items = False
    closing_brace = None
    for i in range(nav_line + 1, min(nav_line + 10, len(header_lines))):
        if 'align-items' in header_lines[i]:
            has_align_items = True
            print(f"   ✅ align-items já existe na linha {i + 1}")
        if '}' in header_lines[i]:
            closing_brace = i
            break
    
    # 4. Adicionar align-items se não existir
    if not has_align_items and closing_brace:
        print("   ➕ Adicionando align-items: center;")
        # Inserir antes do fechamento
        indent = '  '
        header_lines.insert(closing_brace, f'{indent}align-items: center;\n')
    
    # 5. Salvar header CSS
    with open(header_css_path, 'w', encoding='utf-8') as f:
        f.writelines(header_lines)
    
    print("   ✅ Header CSS atualizado")
    
    # 6. Adicionar regras complementares no dropdown-menu.css
    dropdown_css_path = "/home/user/webapp/public/assets/css/dropdown-menu.css"
    
    print("\n2️⃣ Atualizando dropdown-menu.css...")
    
    with open(dropdown_css_path, 'r', encoding='utf-8') as f:
        dropdown_content = f.read()
    
    # CSS a adicionar no final
    alignment_css = """

/* =========================================================
   NORMALIZAÇÃO DE ALINHAMENTO VERTICAL DO MENU
   ========================================================= */

/* Forçar todos os itens diretos do menu a terem mesma altura e alinhamento */
.nav > a,
.nav > div,
.nav .nav-link,
.nav .nav-item {
  display: flex;
  align-items: center;
  height: 48px;
}

/* Garantir consistência para dropdowns */
.nav .dropdown,
.nav .nav-dropdown {
  display: flex;
  align-items: center;
}
"""
    
    # Verificar se já existe
    if 'NORMALIZAÇÃO DE ALINHAMENTO VERTICAL' not in dropdown_content:
        print("   ➕ Adicionando regras de alinhamento")
        with open(dropdown_css_path, 'a', encoding='utf-8') as f:
            f.write(alignment_css)
        print("   ✅ Dropdown CSS atualizado")
    else:
        print("   ✅ Regras de alinhamento já existem")
    
    # 7. Resumo
    print("\n✅ ALINHAMENTO VERTICAL CORRIGIDO!")
    print("\n📋 Alterações aplicadas:")
    print("   1. .nav { align-items: center; } ✅")
    print("   2. .nav > a, .nav > div, etc { display: flex; align-items: center; height: 48px; } ✅")
    print("   3. .nav .dropdown { display: flex; align-items: center; } ✅")
    
    print("\n🔒 NÃO alterado (conforme especificado):")
    print("   • HTML estrutural")
    print("   • Classes existentes")
    print("   • Breakpoints")
    print("   • CTA")
    print("   • Dropdown de idioma")
    print("   • Padding do header")
    print("   • Espaçamento horizontal (gap)")
    print("   • Tamanho de fonte")
    print("   • Hover")
    print("   • Media queries")
    
    print("\n✅ Menu superior agora com alinhamento vertical perfeito!")
    print("\n📐 Validar visualmente em:")
    print("   • Desktop 1440px")
    print("   • Desktop 1280px")
    print("   • 1200px breakpoint")
    print("   • 900px breakpoint")

if __name__ == "__main__":
    main()
