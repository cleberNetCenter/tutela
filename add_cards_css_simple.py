#!/usr/bin/env python3
"""
Adicionar CSS de cards antes da seção GRIDS
"""

def main():
    print("🔧 ADICIONANDO CSS DE CARDS\n")
    
    css_path = "/home/user/webapp/public/assets/css/styles-clean.css"
    
    with open(css_path, 'r', encoding='utf-8') as f:
        css_lines = f.readlines()
    
    # Encontrar linha com /* ===================== GRIDS
    insert_line = None
    for i, line in enumerate(css_lines):
        if '/* ===================== GRIDS' in line:
            insert_line = i
            break
    
    if insert_line is None:
        print("❌ Não encontrou GRIDS")
        return
    
    print(f"✅ Inserindo antes da linha {insert_line + 1}")
    
    cards_css = """
/* ===================== FEATURE CARDS ==================== */
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
    
    # Inserir
    css_lines.insert(insert_line, cards_css)
    
    # Salvar
    with open(css_path, 'w', encoding='utf-8') as f:
        f.writelines(css_lines)
    
    print("✅ CSS de cards adicionado!")
    print(f"   • {len(cards_css.split(chr(10)))} linhas adicionadas")
    print("   • .feature-item, .vertical-card, .feature-icon")

if __name__ == "__main__":
    main()
