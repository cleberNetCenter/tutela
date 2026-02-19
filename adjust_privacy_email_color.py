#!/usr/bin/env python3
"""
Adjust Privacy Policy Email Link Color
=======================================
Altera a cor do link de email para tom verde, mantendo o sublinhado.
Adiciona estilo inline para consistência visual com a paleta de cores do site.
"""

def adjust_email_link_color():
    """Adiciona cor verde ao link de email"""
    
    privacy_html_path = "public/legal/politica-de-privacidade.html"
    
    # Ler o arquivo
    with open(privacy_html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # String atual (link sem estilo)
    old_string = '<p><a href="mailto:contato@tuteladigital.com.br"><strong>contato@tuteladigital.com.br</strong></a></p>'
    
    # Nova string com estilo verde (usando --color-green-800 da paleta)
    new_string = '<p><a href="mailto:contato@tuteladigital.com.br" style="color: #16503b; text-decoration: underline;"><strong>contato@tuteladigital.com.br</strong></a></p>'
    
    # Verificar se a string existe
    if old_string not in content:
        print("❌ String original não encontrada!")
        print("Procurando por:", old_string)
        return False
    
    # Fazer a substituição
    content = content.replace(old_string, new_string)
    
    # Salvar o arquivo
    with open(privacy_html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Cor verde aplicada ao link de email!")
    return True

if __name__ == "__main__":
    print("🎨 Ajustando cor do link de email...")
    print("=" * 60)
    
    success = adjust_email_link_color()
    
    print("=" * 60)
    
    if success:
        print("✅ Cor aplicada com sucesso!")
        print("\nArquivo modificado:")
        print("  • public/legal/politica-de-privacidade.html")
        print("\nEstilo aplicado:")
        print("  • Cor: #16503b (var(--color-green-800))")
        print("  • Text-decoration: underline (mantido)")
        print("  • Font-weight: bold (mantido via <strong>)")
        print("\n✨ Resultado:")
        print("  • Link com tom verde consistente com a paleta")
        print("  • Sublinhado mantido para indicar interatividade")
        print("  • Melhor consistência visual com o tema do site")
    else:
        print("❌ Falha ao aplicar correção")
