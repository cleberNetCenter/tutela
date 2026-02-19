#!/usr/bin/env python3
"""
Fix Privacy Policy Email Link
==============================
Transforma o email contato@tuteladigital.com.br em um link clicável
na página de política de privacidade, igual ao formato usado no rodapé.

Alteração única: linha 345 (seção 11. Canal de Contato)
"""

def fix_privacy_email_link():
    """Transforma o email em link clicável"""
    
    privacy_html_path = "public/legal/politica-de-privacidade.html"
    
    # Ler o arquivo
    with open(privacy_html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # String a ser substituída (linha 345)
    old_string = '<p><strong>contato@tuteladigital.com.br</strong></p>'
    
    # Nova string com link (mesmo formato do rodapé, linha 364)
    new_string = '<p><a href="mailto:contato@tuteladigital.com.br"><strong>contato@tuteladigital.com.br</strong></a></p>'
    
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
    
    print("✅ Email transformado em link clicável!")
    return True

if __name__ == "__main__":
    print("🔧 Transformando email em link...")
    print("=" * 60)
    
    success = fix_privacy_email_link()
    
    print("=" * 60)
    
    if success:
        print("✅ Correção aplicada com sucesso!")
        print("\nArquivo modificado:")
        print("  • public/legal/politica-de-privacidade.html")
        print("\nAlteração:")
        print("  Antes: <p><strong>contato@tuteladigital.com.br</strong></p>")
        print("  Depois: <p><a href=\"mailto:contato@tuteladigital.com.br\">")
        print("            <strong>contato@tuteladigital.com.br</strong>")
        print("          </a></p>")
        print("\n✨ Resultado:")
        print("  • Email agora é um link clicável (mailto:)")
        print("  • Mesmo formato usado no rodapé da página")
        print("  • Nenhuma outra alteração no HTML")
    else:
        print("❌ Falha ao aplicar correção")
