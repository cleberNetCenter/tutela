#!/usr/bin/env python3
"""
Script DEFINITIVO para testar menu mobile LOCALMENTE antes do deploy
Inicia servidor HTTP local e abre navegador para teste manual
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from threading import Timer

PORT = 8888

def start_server():
    """Inicia servidor HTTP local"""
    os.chdir('public')
    
    Handler = http.server.SimpleHTTPRequestHandler
    Handler.extensions_map.update({
        '.js': 'application/javascript',
        '.css': 'text/css',
        '.html': 'text/html',
    })
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("=" * 60)
        print("🌐 SERVIDOR DE TESTE LOCAL")
        print("=" * 60)
        print(f"\n📡 Servidor rodando em: http://localhost:{PORT}")
        print(f"📱 Página de teste: http://localhost:{PORT}/test-mobile-dropdowns.html")
        print(f"🏠 Homepage: http://localhost:{PORT}/index.html")
        print("\n📋 INSTRUÇÕES DE TESTE:")
        print("  1. Abrir DevTools (F12)")
        print("  2. Toggle Device Toolbar (Ctrl+Shift+M)")
        print("  3. Selecionar 'iPhone 12' ou outro dispositivo")
        print("  4. Testar:")
        print("     a) Clicar no hamburger (☰)")
        print("     b) Menu deve aparecer ✅")
        print("     c) Clicar em 'Soluções' → dropdown abre ✅")
        print("     d) Clicar em 'Base Jurídica' → dropdown abre ✅")
        print("     e) Clicar fora → menu fecha ✅")
        print("\n🛑 Pressione Ctrl+C para parar o servidor")
        print("=" * 60)
        print()
        
        # Abrir navegador automaticamente
        def open_browser():
            url = f"http://localhost:{PORT}/test-mobile-dropdowns.html"
            print(f"🌐 Abrindo {url} no navegador...")
            webbrowser.open(url)
        
        Timer(1, open_browser).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 Servidor encerrado")
            sys.exit(0)

def validate_files():
    """Valida que os arquivos necessários existem"""
    print("🔍 Validando arquivos...")
    
    required_files = [
        'public/index.html',
        'public/test-mobile-dropdowns.html',
        'public/assets/css/styles-header-final.css',
        'public/assets/js/mobile-menu.js',
        'public/assets/js/dropdown-menu.js',
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
            print(f"  ❌ {file} - NÃO ENCONTRADO")
        else:
            print(f"  ✅ {file}")
    
    if missing:
        print(f"\n❌ {len(missing)} arquivo(s) ausente(s)")
        return False
    
    print("\n✅ Todos os arquivos encontrados")
    return True

def check_css_rule():
    """Verifica se a regra .nav.active existe no CSS"""
    print("\n🔍 Verificando regra CSS .nav.active...")
    
    css_file = 'public/assets/css/styles-header-final.css'
    
    with open(css_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
        if '.nav.active' in content:
            print("  ✅ Regra .nav.active encontrada")
            return True
        else:
            print("  ❌ Regra .nav.active NÃO ENCONTRADA")
            print("  ⚠️  Menu mobile NÃO vai funcionar sem esta regra!")
            return False

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🧪 TESTE LOCAL - MENU MOBILE")
    print("=" * 60)
    print()
    
    # Validar arquivos
    if not validate_files():
        print("\n❌ Validação falhou - arquivos ausentes")
        sys.exit(1)
    
    # Verificar CSS
    if not check_css_rule():
        print("\n❌ Validação falhou - regra CSS ausente")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ VALIDAÇÃO COMPLETA - Iniciando servidor...")
    print("=" * 60)
    print()
    
    # Iniciar servidor
    try:
        start_server()
    except OSError as e:
        if 'Address already in use' in str(e):
            print(f"\n❌ Porta {PORT} já está em uso")
            print(f"💡 Tente: killall python3 ou use outra porta")
        else:
            print(f"\n❌ Erro: {e}")
        sys.exit(1)
