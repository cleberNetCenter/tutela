#!/usr/bin/env python3
"""
Gerador completo de páginas MPA a partir do SPA index.html
Gera: preservacao-probatoria-digital.html, seguranca.html, como-funciona.html
"""
import re
from datetime import datetime
from pathlib import Path

def extract_page_content(spa_html, page_id):
    """Extrai o conteúdo de uma página específica do SPA"""
    # Tenta encontrar o padrão: <div class="page" id="page-xxx">...<!-- == -->
    pattern = rf'<div class="page[^"]*" id="{page_id}">(.*?)(?=<div class="page"|<!-- ==|</body>)'
    match = re.search(pattern, spa_html, re.DOTALL)
    if match:
        content = match.group(1).strip()
        # Remove o </div> final se existir
        content = re.sub(r'</div>\s*$', '', content).strip()
        return content
    return None

def create_head(title, description, url, last_modified, og_type="article"):
    """Cria o <head> personalizado para cada página"""
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>{title}</title>
<meta content="{description}" name="description"/>
<meta name="last-modified" content="{last_modified}"/>
<link rel="canonical" href="{url}"/>
<link href="assets/illustrations/favicon.svg" rel="icon" type="image/svg+xml"/>

<!-- Open Graph / Facebook -->
<meta property="og:type" content="{og_type}"/>
<meta property="og:url" content="{url}"/>
<meta property="og:title" content="{title}"/>
<meta property="og:description" content="{description}"/>
<meta property="og:site_name" content="Tutela Digital®"/>

<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image"/>
<meta property="twitter:url" content="{url}"/>
<meta property="twitter:title" content="{title}"/>
<meta property="twitter:description" content="{description}"/>

<!-- Hreflang -->
<link rel="alternate" hreflang="pt-br" href="{url}"/>
<link rel="alternate" hreflang="x-default" href="{url}"/>

<!-- Fonts -->
<link href="https://fonts.googleapis.com" rel="preconnect"/>
<link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>

<!-- CSS -->
<link rel="stylesheet" href="assets/css/styles-clean.css?v=4">
<link rel="stylesheet" href="assets/css/styles-header-final.css?v=4">
<link rel="stylesheet" href="assets/css/styles-clean.exec-compact.css?v=4">

<!-- Google Analytics -->
<script async="" src="https://www.googletagmanager.com/gtag/js?id=G-KXVB267PYJ"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-KXVB267PYJ');
</script>
</head>'''

def create_header():
    """Cria o header MPA (com links reais)"""
    return '''<body class="exec-compact">
<header class="header" id="header">
<div class="header-inner">
<a class="logo" href="/">
                    Tutela Digital<sup>®</sup>
</a>
<nav class="nav" id="nav">
<a class="nav-link" href="/" data-i18n="nav_home">Início</a>
<a class="nav-link" href="/como-funciona.html" data-i18n="nav_como_funciona">Como Funciona</a>
<a class="nav-link" href="/seguranca.html" data-i18n="nav_seguranca">Segurança</a>
<a class="nav-link" href="/preservacao-probatoria-digital.html" data-i18n="nav_preservacao">Preservação Probatória</a>
<a class="nav-link" href="/institucional.html">Institucional</a>
<a class="nav-link" href="/fundamento-juridico.html" data-i18n="nav_fundamento">Fundamento Jurídico</a>
<a class="nav-link" href="/termos-de-custodia.html" data-i18n="nav_termos">Termos de Custódia</a>
</nav>
<a class="header-cta" href="https://app.tuteladigital.com.br/" rel="noopener noreferrer" target="_blank">
				  Acessar a Plataforma
				</a>
<button class="mobile-menu-btn" onclick="toggleMobileMenu()">
<span></span>
<span></span>
<span></span>
</button>
<div class="lang-dropdown">
  <button class="lang-toggle" aria-label="Selecionar idioma">
    🌐 <span class="lang-code">PT</span>
  </button>
  <div class="lang-menu">
    <button class="lang-option" data-lang="pt">🇧🇷 Português</button>
    <button class="lang-option" data-lang="en">🇺🇸 English</button>
    <button class="lang-option" data-lang="es">🇪🇸 Español</button>
  </div>
</div>
</div>
</header>

<main class="main">'''

def create_footer():
    """Cria o footer MPA (com links reais)"""
    return '''</main>

<footer class="footer">
<div class="footer-inner">
<div class="footer-brand">
<div class="footer-logo">
						Tutela Digital<sup>®</sup>
</div>
<a class="footer-link footer-link--social" href="https://www.instagram.com/tuteladigitalbr/" rel="noopener noreferrer" target="_blank">
<svg aria-hidden="true" class="footer-social-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
<path d="M7.75 2h8.5C19.99 2 22 4.01 22 6.25v8.5C22 19.99 19.99 22 16.25 22h-8.5C4.01 22 2 19.99 2 16.25v-8.5C2 4.01 4.01 2 7.75 2zm0 1.5A4.25 4.25 0 0 0 3.5 7.75v8.5A4.25 4.25 0 0 0 7.75 20.5h8.5a4.25 4.25 0 0 0 4.25-4.25v-8.5A4.25 4.25 0 0 0 16.25 3.5h-8.5zM12 7a5 5 0 1 1 0 10 5 5 0 0 1 0-10zm0 1.5a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7zm4.75-.88a.88.88 0 1 1 0 1.75.88.88 0 0 1 0-1.75z" fill="currentColor"></path>
</svg>
<span>@tuteladigitalbr</span>
</a>
</div>
<div class="footer-links">
<a class="footer-link" href="/como-funciona.html">Como Funciona</a>
<a class="footer-link" href="/seguranca.html">Segurança</a>
<a class="footer-link" href="/preservacao-probatoria-digital.html">Preservação Probatória</a>
<a class="footer-link" href="/institucional.html">Institucional</a>
<a class="footer-link" href="/fundamento-juridico.html">Fundamento Jurídico</a>
<a class="footer-link" href="/termos-de-custodia.html">Termos de Custódia</a>
</div>
<div class="footer-copy">
                    © 2025 Tutela Digital®. Todos os direitos reservados.
                </div>
</div>
</footer>

<!-- WhatsApp Floating Button -->
<a aria-label="Fale com nosso especialista" class="whatsapp-float" href="https://wa.me/5531975460050" rel="noopener noreferrer" target="_blank">
<span class="whatsapp-tooltip">Fale com nosso especialista</span>
<svg class="whatsapp-icon" fill="currentColor" viewbox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
<path d="M19.11 17.44c-.27-.14-1.6-.79-1.85-.88-.25-.09-.43-.14-.61.14-.18.27-.7.88-.86 1.06-.16.18-.32.2-.59.07-.27-.14-1.15-.42-2.19-1.35-.81-.72-1.36-1.61-1.52-1.88-.16-.27-.02-.42.12-.56.12-.12.27-.32.41-.48.14-.16.18-.27.27-.45.09-.18.05-.34-.02-.48-.07-.14-.61-1.47-.84-2.02-.22-.53-.45-.46-.61-.47h-.52c-.18 0-.48.07-.73.34-.25.27-.96.93-.96 2.27s.98 2.64 1.11 2.82c.14.18 1.93 2.95 4.68 4.13.65.28 1.16.45 1.56.58.65.21 1.25.18 1.72.11.53-.08 1.6-.65 1.83-1.28.23-.63.23-1.17.16-1.28-.07-.11-.25-.18-.52-.32z"></path>
<path d="M16 3C8.82 3 3 8.82 3 16c0 2.82.93 5.44 2.5 7.56L3 29l5.65-2.47A12.9 12.9 0 0 0 16 29c7.18 0 13-5.82 13-13S23.18 3 16 3zm0 23.5c-2.3 0-4.45-.67-6.27-1.82l-.45-.28-3.35 1.47.89-3.56-.29-.46A10.4 10.4 0 0 1 5.6 16C5.6 10.27 10.27 5.6 16 5.6S26.4 10.27 26.4 16 21.73 26.5 16 26.5z"></path>
</svg>
</a>

<script src="assets/js/i18n.js"></script>
<script>
  function toggleMobileMenu() {
    const nav = document.getElementById('nav');
    nav.classList.toggle('mobile-open');
  }

  // Fecha o menu mobile ao clicar em qualquer link
  document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      document.getElementById('nav').classList.remove('mobile-open');
    });
  });
</script>
</body>
</html>'''

# Configuração das páginas a serem geradas
PAGES = {
    'preservacao-probatoria-digital': {
        'page_id': 'page-preservacao-probatoria',
        'title': 'Preservação Probatória Digital | Tutela Digital®',
        'description': 'Tecnologia de preservação probatória digital com cadeia de custódia verificável e infraestrutura para formalização notarial.',
        'url': 'https://tuteladigital.com.br/preservacao-probatoria-digital.html'
    },
    'seguranca': {
        'page_id': 'page-seguranca',
        'title': 'Arquitetura de Segurança | Tutela Digital®',
        'description': 'Infraestrutura de segurança com criptografia de ponta a ponta, autenticação biométrica e cadeia de custódia verificável.',
        'url': 'https://tuteladigital.com.br/seguranca.html'
    },
    'como-funciona': {
        'page_id': 'page-como-funciona',
        'title': 'Como Funciona a Preservação Probatória | Tutela Digital®',
        'description': 'Processo técnico de preservação probatória: identificação, depósito, registro técnico, cadeia de custódia e acesso controlado.',
        'url': 'https://tuteladigital.com.br/como-funciona.html'
    }
}

def main():
    # Lê o arquivo SPA original
    spa_path = Path('public/index.html')
    if not spa_path.exists():
        print(f"❌ Erro: {spa_path} não encontrado!")
        return
    
    spa_html = spa_path.read_text(encoding='utf-8')
    last_modified = datetime.now().strftime('%Y-%m-%d')
    
    print("🔧 Gerando páginas MPA...\n")
    
    for filename, config in PAGES.items():
        print(f"📄 Gerando {filename}.html...")
        
        # Extrai o conteúdo da página
        content = extract_page_content(spa_html, config['page_id'])
        
        if not content:
            print(f"   ⚠️  Aviso: Conteúdo de '{config['page_id']}' não encontrado no SPA!")
            continue
        
        # Monta a página completa
        html = create_head(
            config['title'],
            config['description'],
            config['url'],
            last_modified
        )
        html += create_header()
        html += f'\n{content}\n'
        html += create_footer()
        
        # Salva o arquivo
        output_path = Path(f'public/{filename}.html')
        output_path.write_text(html, encoding='utf-8')
        print(f"   ✅ Salvo em {output_path} ({len(html)} bytes)\n")
    
    print("✅ Geração concluída!")
    print(f"\n📊 Páginas criadas:")
    for filename in PAGES.keys():
        print(f"   - {filename}.html")

if __name__ == '__main__':
    main()
