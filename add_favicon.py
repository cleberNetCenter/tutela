#!/usr/bin/env python3
"""
Script para adicionar favicon em todas as páginas HTML
"""

import glob
import os

def create_favicon_svg():
    """Cria um favicon SVG simples com TD"""
    
    svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <rect width="512" height="512" fill="#0a3d2e" rx="64"/>
  <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" 
        font-family="serif" font-size="280" font-weight="700" fill="#ffffff">TD</text>
</svg>'''
    
    with open('public/assets/illustrations/favicon.svg', 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    print("✅ favicon.svg criado")

def update_html_files():
    """Atualiza todas as páginas HTML para incluir favicon"""
    
    # Páginas principais
    html_files = glob.glob('public/*.html')
    
    # Páginas legais
    html_files.extend(glob.glob('public/legal/*.html'))
    
    favicon_tags = '''<link rel="icon" type="image/svg+xml" href="/assets/illustrations/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/illustrations/favicon.png">
<link rel="apple-touch-icon" sizes="180x180" href="/assets/illustrations/favicon.png">'''
    
    updated_count = 0
    
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar se já tem favicon
        if 'favicon.svg' in content:
            print(f"⏭️  {html_file} já tem favicon")
            continue
        
        # Remover referências antigas
        content = content.replace('<link href="assets/illustrations/favicon.svg" rel="icon" type="image/svg+xml"/>', '')
        content = content.replace('<link href="/assets/illustrations/favicon.svg" rel="icon" type="image/svg+xml"/>', '')
        
        # Adicionar após <meta name="viewport"...>
        if '<meta name="viewport"' in content:
            content = content.replace(
                '<meta name="viewport"',
                f'{favicon_tags}\n<meta name="viewport"'
            )
            updated_count += 1
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ {html_file} atualizado")
        else:
            print(f"⚠️  {html_file} não tem meta viewport - adicionar manualmente")
    
    return updated_count

def validate_favicon():
    """Valida que o favicon foi adicionado corretamente"""
    
    print("\n🔍 Validando favicon...")
    
    # Verificar se arquivos existem
    files = [
        'public/assets/illustrations/favicon.svg',
        'public/assets/illustrations/favicon.png'
    ]
    
    for file in files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"  ✅ {file} ({size} bytes)")
        else:
            print(f"  ❌ {file} - NÃO ENCONTRADO")
            return False
    
    # Verificar em páginas HTML
    html_files = glob.glob('public/*.html') + glob.glob('public/legal/*.html')
    
    with_favicon = 0
    without_favicon = 0
    
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            if 'favicon.svg' in content or 'favicon.png' in content:
                with_favicon += 1
            else:
                without_favicon += 1
                print(f"  ⚠️  {html_file} sem favicon")
    
    print(f"\n📊 Resumo:")
    print(f"  ✅ Com favicon: {with_favicon}")
    print(f"  ❌ Sem favicon: {without_favicon}")
    
    return without_favicon == 0

if __name__ == "__main__":
    print("=" * 60)
    print("🎨 ADICIONANDO FAVICON AO SITE")
    print("=" * 60)
    print()
    
    # 1. Criar SVG
    create_favicon_svg()
    
    # 2. Atualizar HTMLs
    print()
    updated = update_html_files()
    
    # 3. Validar
    print()
    if validate_favicon():
        print("\n" + "=" * 60)
        print("✅ FAVICON ADICIONADO COM SUCESSO")
        print("=" * 60)
        print(f"\n📊 Estatísticas:")
        print(f"  - Arquivos criados: 2 (SVG + PNG)")
        print(f"  - Páginas atualizadas: {updated}")
        print(f"  - Formatos: SVG (moderno), PNG (fallback)")
        print("\n🌐 Teste:")
        print("  1. Abrir site no navegador")
        print("  2. Verificar ícone na aba do navegador")
        print("  3. Adicionar aos favoritos → ver ícone")
    else:
        print("\n❌ Validação falhou - verificar erros acima")
