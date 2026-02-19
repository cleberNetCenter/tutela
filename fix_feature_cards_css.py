#!/usr/bin/env python3
"""
Adicionar CSS faltante para cards (.feature-item, .vertical-card)
===================================================================
Problema: Cards sumiram da página preservação probatória
Causa: CSS para .feature-item foi removido durante consolidações
Solução: Adicionar CSS completo para feature-item, vertical-card, feature-icon
"""

def main():
    print("🔧 ADICIONANDO CSS DE CARDS (FEATURE-ITEM)\n")
    
    css_path = "/home/user/webapp/public/assets/css/styles-clean.css"
    
    # 1. Ler CSS
    print("1️⃣ Lendo CSS atual...")
    with open(css_path, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    original_lines = len(css_content.split('\n'))
    print(f"   ✅ {original_lines} linhas")
    
    # 2. Verificar se já existe
    if '.feature-item' in css_content:
        print("\n⚠️  .feature-item já existe no CSS!")
        return
    
    print("\n2️⃣ .feature-item NÃO encontrado - adicionando...")
    
    # 3. Encontrar ponto de inserção (após .features)
    features_pos = css_content.find('/* FEATURES */')
    if features_pos == -1:
        features_pos = css_content.find('.features {')
    
    if features_pos == -1:
        print("   ❌ Não encontrou seção FEATURES")
        return
    
    # Encontrar fim da seção features (próximo /* ou antes de GRIDS)
    insert_pos = css_content.find('/* ===================== GRIDS', features_pos)
    if insert_pos == -1:
        insert_pos = css_content.find('\n\n/* ==', features_pos + 500)
    
    if insert_pos == -1:
        print("   ❌ Não encontrou ponto de inserção")
        return
    
    print(f"   ✅ Inserção antes de GRIDS na posição {insert_pos}")
    
    # 4. CSS a ser adicionado
    print("\n3️⃣ Preparando CSS de cards...")
    
    cards_css = """
        /* FEATURE ITEMS / CARDS */
        .feature-item {
            background: var(--color-surface-light);
            padding: var(--space-lg);
            border: 1px solid var(--color-border-soft);
            border-radius: 4px;
        }
        
        .feature-item,
        .vertical-card {
            background: var(--color-surface-light);
            border: 1px solid var(--color-border-soft);
        }

        .feature-item h3,
        .vertical-card h3 {
            color: var(--color-text-strong);
        }
                
        .feature-icon {
            width: 48px;
            height: 48px;
            margin-bottom: var(--space-md);
            color: var(--color-text-base);
        }
        
        .feature-item h3 {
            font-family: var(--font-body);
            font-size: 1.125rem;
            font-weight: 600;
            color: var(--color-text-strong);
            margin-bottom: var(--space-sm);
        }
        
        .feature-item p {
            color: var(--color-text-muted);
            font-size: 0.9375rem;
            line-height: 1.7;
        }

        .vertical-card {
            padding: var(--space-lg);
            border-radius: 4px;
        }

        .vertical-card h3 {
            font-family: var(--font-body);
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: var(--space-sm);
        }

        .vertical-card p {
            color: var(--color-text-base);
            font-size: 0.9375rem;
            line-height: 1.7;
        }

"""
    
    new_lines = len(cards_css.split('\n'))
    print(f"   ✅ {new_lines} linhas de CSS preparadas")
    
    # 5. Inserir CSS
    print("\n4️⃣ Inserindo CSS...")
    updated_css = css_content[:insert_pos] + cards_css + css_content[insert_pos:]
    
    # 6. Salvar
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(updated_css)
    
    final_lines = len(updated_css.split('\n'))
    
    print(f"   ✅ CSS atualizado!")
    
    # 7. Resumo
    print("\n📊 RESULTADO:")
    print(f"   • Linhas antes: {original_lines}")
    print(f"   • Linhas adicionadas: {new_lines}")
    print(f"   • Linhas depois: {final_lines}")
    
    print("\n✅ CSS DE CARDS ADICIONADO!")
    print("\n📋 Estilos adicionados:")
    print("   • .feature-item (background, padding, border)")
    print("   • .feature-item h3 (tipografia)")
    print("   • .feature-item p (cor, tamanho)")
    print("   • .feature-icon (ícones 48x48px)")
    print("   • .vertical-card (cards verticais)")
    print("   • .vertical-card h3, p (conteúdo)")
    
    print("\n✅ Página preservação probatória agora deve mostrar todos os cards!")

if __name__ == "__main__":
    main()
