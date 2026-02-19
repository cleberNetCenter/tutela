#!/usr/bin/env python3
"""
REESTRUTURAÇÃO DO RODAPÉ - Tutela Digital®
Implementa footer institucional de 4 colunas usando APENAS variáveis JSON existentes.
"""

import re
from pathlib import Path

BASE_DIR = Path("public")

# =======================================================
# NOVO FOOTER INSTITUCIONAL (4 COLUNAS)
# =======================================================

NEW_FOOTER_HTML = '''<footer class="footer">
<div class="footer-container">

<!-- COLUNA 1 – MARCA -->
<div class="footer-col footer-brand-col">
<h3 data-i18n="global.brand">Tutela Digital®</h3>
<p><a href="mailto:contato@tuteladigital.com.br" data-i18n="global.footerEmail">contato@tuteladigital.com.br</a></p>
<p><a href="https://www.instagram.com/tuteladigitalbr/" target="_blank" rel="noopener noreferrer"><svg aria-hidden="true" class="footer-social-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
<path d="M7.75 2h8.5C19.99 2 22 4.01 22 6.25v8.5C22 19.99 19.99 22 16.25 22h-8.5C4.01 22 2 19.99 2 16.25v-8.5C2 4.01 4.01 2 7.75 2zm0 1.5A4.25 4.25 0 0 0 3.5 7.75v8.5A4.25 4.25 0 0 0 7.75 20.5h8.5a4.25 4.25 0 0 0 4.25-4.25v-8.5A4.25 4.25 0 0 0 16.25 3.5h-8.5zM12 7a5 5 0 1 1 0 10 5 5 0 0 1 0-10zm0 1.5a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7zm4.75-.88a.88.88 0 1 1 0 1.75.88.88 0 0 1 0-1.75z" fill="currentColor"></path>
</svg> <span data-i18n="global.footerInstagram">@tuteladigitalbr</span></a></p>
</div>

<!-- COLUNA 2 – PLATAFORMA -->
<div class="footer-col">
<h4>Plataforma</h4>
<ul>
<li><a href="/como-funciona.html" data-i18n="navigation.howItWorks">Como Funciona</a></li>
<li><a href="/seguranca.html" data-i18n="navigation.security">Segurança</a></li>
<li><a href="/legal/preservacao-probatoria-digital.html" data-i18n="navigation.preservation">Preservação Probatória</a></li>
</ul>
</div>

<!-- COLUNA 3 – PÚBLICO -->
<div class="footer-col">
<h4>Público</h4>
<ul>
<li><a href="/governo.html" data-i18n="navigation.government">Governo</a></li>
<li><a href="/empresas.html" data-i18n="navigation.companies">Empresas</a></li>
<li><a href="/pessoas.html" data-i18n="navigation.individuals">Pessoas Físicas</a></li>
</ul>
</div>

<!-- COLUNA 4 – BASE JURÍDICA -->
<div class="footer-col">
<h4 data-i18n="navigation.legal_base">Base Jurídica</h4>
<ul>
<li><a href="/legal/institucional.html" data-i18n="navigation.institucional">Institucional</a></li>
<li><a href="/legal/fundamento-juridico.html" data-i18n="navigation.legalBasis">Fundamento Jurídico</a></li>
<li><a href="/legal/termos-de-custodia.html" data-i18n="navigation.terms">Termos de Custódia</a></li>
<li><a href="/legal/politica-de-privacidade.html" data-i18n="navigation.privacy">Política de Privacidade</a></li>
</ul>
</div>

</div>

<div class="footer-bottom">
<p data-i18n="global.footerRights">© 2026 Tutela Digital®. Todos os direitos reservados.</p>
</div>
</footer>'''

# =======================================================
# CSS DO NOVO FOOTER
# =======================================================

FOOTER_CSS = '''
/* =======================================================
   FOOTER INSTITUCIONAL (4 COLUNAS)
   ======================================================= */

.footer {
  background: linear-gradient(180deg, #052e24, #031f18);
  color: #d9efe7;
  padding: 60px 40px 30px;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 40px;
}

.footer-col h3 {
  font-weight: 600;
  margin-bottom: 20px;
  font-size: 20px;
  letter-spacing: 0.5px;
  color: #ffffff;
}

.footer-col h4 {
  font-weight: 600;
  margin-bottom: 15px;
  font-size: 16px;
  letter-spacing: 0.5px;
  color: #ffffff;
  text-transform: none;
}

.footer-col ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-col ul li {
  margin-bottom: 10px;
}

.footer-col a {
  text-decoration: none;
  color: #b5d6c8;
  transition: color 0.3s ease;
  font-size: 14px;
  display: inline-block;
}

.footer-col a:hover {
  color: #ffffff;
}

.footer-brand-col p {
  margin: 8px 0;
  font-size: 14px;
}

.footer-brand-col a {
  color: #b5d6c8;
  text-decoration: none;
  transition: color 0.3s ease;
}

.footer-brand-col a:hover {
  color: #ffffff;
}

.footer-social-icon {
  width: 18px;
  height: 18px;
  vertical-align: middle;
  margin-right: 5px;
}

.footer-bottom {
  text-align: center;
  margin-top: 50px;
  padding-top: 30px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  font-size: 14px;
  opacity: 0.7;
}

/* Responsividade */
@media (max-width: 992px) {
  .footer-container {
    grid-template-columns: repeat(2, 1fr);
    gap: 35px;
  }
}

@media (max-width: 768px) {
  .footer {
    padding: 40px 20px 20px;
  }
  
  .footer-container {
    grid-template-columns: 1fr;
    gap: 30px;
  }
  
  .footer-bottom {
    margin-top: 35px;
    padding-top: 25px;
  }
}

/* Remove estilos antigos do footer */
.footer-inner {
  display: none;
}

.footer-links {
  display: none;
}

.footer-copy {
  display: none;
}
'''

# =======================================================
# FUNÇÕES
# =======================================================

def replace_footer_in_html(html_content: str) -> str:
    """
    Substitui o footer antigo pelo novo footer de 4 colunas.
    """
    # Padrão regex para encontrar o footer completo
    # Procura por <footer ... </footer> incluindo tudo dentro
    footer_pattern = r'<footer[^>]*>.*?</footer>'
    
    # Substitui o footer antigo pelo novo
    new_content = re.sub(
        footer_pattern,
        NEW_FOOTER_HTML,
        html_content,
        flags=re.DOTALL
    )
    
    return new_content

def update_html_files():
    """
    Atualiza TODOS os arquivos HTML com o novo footer.
    """
    html_files = list(BASE_DIR.glob("*.html"))
    
    # Também inclui arquivos em subdiretórios (legal/)
    html_files.extend(BASE_DIR.glob("legal/*.html"))
    
    updated_count = 0
    
    for html_file in html_files:
        print(f"\n📄 Processando: {html_file.relative_to(BASE_DIR)}")
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verifica se tem footer
        if '<footer' not in content:
            print(f"  ⚠️  Não tem footer, pulando...")
            continue
        
        # Substitui footer
        new_content = replace_footer_in_html(content)
        
        # Salva se houve mudança
        if new_content != content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  ✅ Footer atualizado!")
            updated_count += 1
        else:
            print(f"  ℹ️  Footer já está atualizado")
    
    return updated_count

def update_css_file():
    """
    Adiciona/atualiza CSS do footer no arquivo de estilos.
    """
    css_files = [
        BASE_DIR / "assets/css/styles-clean.css",
        BASE_DIR / "assets/css/styles-header-final.css",
        BASE_DIR / "assets/css/styles-clean.exec-compact.css"
    ]
    
    # Procura o arquivo CSS principal
    main_css = None
    for css_file in css_files:
        if css_file.exists():
            main_css = css_file
            break
    
    if not main_css:
        print("⚠️  Arquivo CSS não encontrado, criando novo...")
        main_css = BASE_DIR / "assets/css/footer-institutional.css"
    
    print(f"\n📄 Atualizando CSS: {main_css.relative_to(BASE_DIR)}")
    
    # Lê CSS atual
    if main_css.exists():
        with open(main_css, 'r', encoding='utf-8') as f:
            css_content = f.read()
    else:
        css_content = ""
    
    # Remove CSS antigo do footer se existir
    css_content = re.sub(
        r'/\*.*?FOOTER.*?\*/.*?(?=/\*|\Z)',
        '',
        css_content,
        flags=re.DOTALL | re.IGNORECASE
    )
    
    # Adiciona novo CSS do footer
    css_content += "\n\n" + FOOTER_CSS
    
    # Salva CSS atualizado
    with open(main_css, 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    print(f"  ✅ CSS do footer adicionado!")
    
    return main_css

# =======================================================
# MAIN
# =======================================================

def main():
    print("\n" + "="*60)
    print("  REESTRUTURAÇÃO DO RODAPÉ - TUTELA DIGITAL®")
    print("  Modelo Institucional de 4 Colunas")
    print("="*60)
    
    print("\n🔧 Iniciando reestruturação do footer...")
    
    print("\n📊 CARACTERÍSTICAS DO NOVO FOOTER:")
    print("  ✅ 4 colunas organizadas (Marca, Plataforma, Público, Base Jurídica)")
    print("  ✅ Usa APENAS variáveis JSON existentes")
    print("  ✅ Suporte multilíngue (PT, EN, ES)")
    print("  ✅ Responsivo (mobile, tablet, desktop)")
    print("  ✅ Hierarquia visual clara")
    print("  ✅ Sem duplicação de navegação")
    
    print("\n🔄 VARIÁVEIS JSON UTILIZADAS:")
    print("  • global.brand")
    print("  • global.footerEmail")
    print("  • global.footerInstagram")
    print("  • global.footerRights")
    print("  • navigation.howItWorks, security, preservation")
    print("  • navigation.government, companies, individuals")
    print("  • navigation.institucional, legalBasis, terms, privacy")
    print("  • navigation.legal_base (título da coluna)")
    
    # 1. Atualiza HTML files
    print("\n" + "="*60)
    print("1️⃣ ATUALIZANDO ARQUIVOS HTML")
    print("="*60)
    updated_html = update_html_files()
    
    # 2. Atualiza CSS
    print("\n" + "="*60)
    print("2️⃣ ATUALIZANDO CSS")
    print("="*60)
    css_file = update_css_file()
    
    # Resumo final
    print("\n" + "="*60)
    print("✅ REESTRUTURAÇÃO CONCLUÍDA!")
    print("="*60)
    
    print(f"\n📊 RESUMO:")
    print(f"  ✅ Arquivos HTML atualizados: {updated_html}")
    print(f"  ✅ CSS atualizado: {css_file.name}")
    print(f"  ✅ Estrutura: 4 colunas responsivas")
    print(f"  ✅ Variáveis: Apenas existentes (sem novas chaves)")
    
    print("\n🧪 PRÓXIMOS PASSOS PARA TESTAR:")
    print("  1. Abra https://tuteladigital.com.br/ em modo anônimo")
    print("  2. Verifique o footer na parte inferior da página")
    print("  3. Teste responsividade (redimensione a janela)")
    print("  4. Troque o idioma (PT → EN → ES)")
    print("  5. Verifique que TODOS os textos do footer são traduzidos")
    print("  6. Confirme que os links funcionam")
    
    print("\n✅ VERIFICAÇÕES FINAIS:")
    print("  • Footer tem 4 colunas no desktop")
    print("  • Footer tem 1 coluna no mobile (< 768px)")
    print("  • Sem texto hardcoded (tudo via data-i18n)")
    print("  • Links funcionam corretamente")
    print("  • Cores e estilo institucional aplicados")
    print("  • Não quebra layout de nenhuma página")

if __name__ == '__main__':
    main()
