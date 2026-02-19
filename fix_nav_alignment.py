#!/usr/bin/env python3
"""
Fix Navigation Vertical Alignment
==================================
Adiciona as regras CSS especificadas para alinhar verticalmente todos os
itens do menu superior (incluindo dropdowns) sem alterar estrutura HTML,
classes, breakpoints, CTA, dropdown de idioma ou responsividade.

Regras a adicionar:
1. .nav { align-items: center; } (adicionar se não existir)
2. .nav > a, .nav > div, .nav .nav-link, .nav .nav-item { 
     display: flex; align-items: center; height: 48px; 
   }
3. .nav .dropdown { display: flex; align-items: center; } (se não existir)
"""

def fix_header_alignment():
    """Adiciona regras de alinhamento vertical ao styles-header-final.css"""
    
    header_css_path = "public/assets/css/styles-header-final.css"
    
    # Ler o arquivo atual
    with open(header_css_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Encontrar a regra .nav existente (linha ~40)
    nav_rule_start = content.find('.nav {')
    if nav_rule_start == -1:
        print("❌ Regra .nav não encontrada!")
        return False
    
    # Encontrar o fechamento da regra .nav
    nav_rule_end = content.find('}', nav_rule_start)
    
    # Extrair a regra .nav atual
    nav_rule = content[nav_rule_start:nav_rule_end + 1]
    
    # Verificar se align-items: center já existe
    if 'align-items: center;' not in nav_rule:
        # Adicionar align-items: center antes do fechamento
        new_nav_rule = nav_rule.replace(
            'gap: 1.5rem;',
            'gap: 1.5rem;\n  align-items: center;'
        )
        content = content.replace(nav_rule, new_nav_rule)
        print("✅ Adicionado 'align-items: center' à regra .nav")
    else:
        print("ℹ️  'align-items: center' já existe na regra .nav")
    
    # Adicionar novas regras após a regra .nav
    nav_section_end = content.find('.nav-link {')
    
    new_rules = """
/* Alinhamento vertical de todos os itens do menu */
.nav > a,
.nav > div,
.nav .nav-link,
.nav .nav-item {
  display: flex;
  align-items: center;
  height: 48px;
}

.nav .dropdown {
  display: flex;
  align-items: center;
}

"""
    
    # Verificar se as regras já existem
    if '.nav > a,' not in content:
        # Inserir as novas regras
        content = content[:nav_section_end] + new_rules + content[nav_section_end:]
        print("✅ Adicionadas regras de alinhamento vertical (.nav > a, .nav > div, etc.)")
    else:
        print("ℹ️  Regras de alinhamento vertical já existem")
    
    # Salvar o arquivo atualizado
    with open(header_css_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def fix_dropdown_alignment():
    """Ajusta dropdown-menu.css para alinhar com a nova altura de 48px"""
    
    dropdown_css_path = "public/assets/css/dropdown-menu.css"
    
    # Ler o arquivo atual
    with open(dropdown_css_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Localizar a regra .nav-dropdown > a
    nav_dropdown_start = content.find('.nav-dropdown > a,')
    if nav_dropdown_start == -1:
        print("❌ Regra .nav-dropdown > a não encontrada!")
        return False
    
    # Encontrar o fechamento da regra
    nav_dropdown_end = content.find('}', nav_dropdown_start)
    
    # Extrair a regra atual
    dropdown_rule = content[nav_dropdown_start:nav_dropdown_end + 1]
    
    # Verificar se height: 48px já existe
    if 'height: 48px;' not in dropdown_rule:
        # Substituir height: auto por height: 48px
        new_dropdown_rule = dropdown_rule.replace(
            'height: auto;',
            'height: 48px;'
        )
        content = content.replace(dropdown_rule, new_dropdown_rule)
        print("✅ Ajustado height de .nav-dropdown > a para 48px")
    else:
        print("ℹ️  Height 48px já existe em .nav-dropdown > a")
    
    # Salvar o arquivo atualizado
    with open(dropdown_css_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

if __name__ == "__main__":
    print("🔧 Corrigindo alinhamento vertical do menu...")
    print("=" * 60)
    
    success_header = fix_header_alignment()
    success_dropdown = fix_dropdown_alignment()
    
    print("=" * 60)
    
    if success_header and success_dropdown:
        print("✅ Alinhamento vertical corrigido com sucesso!")
        print("\nArquivos modificados:")
        print("  • public/assets/css/styles-header-final.css")
        print("  • public/assets/css/dropdown-menu.css")
        print("\nRegras adicionadas:")
        print("  1. .nav { align-items: center; }")
        print("  2. .nav > a, .nav > div, .nav .nav-link, .nav .nav-item {")
        print("       display: flex; align-items: center; height: 48px;")
        print("     }")
        print("  3. .nav .dropdown { display: flex; align-items: center; }")
        print("\n✨ Resultado esperado:")
        print("  • Todos os itens do menu alinhados verticalmente")
        print("  • Dropdowns alinhados como links simples")
        print("  • Sem alterações em padding, gaps, hover, CTA ou idioma")
        print("  • Validar em: 1440px, 1280px, 1200px e 900px")
    else:
        print("❌ Falha ao aplicar correções")
