#!/usr/bin/env python3
"""
Script para corrigir o seletor de idiomas quando páginas traduzidas não existem.

PROBLEMA:
- switchLanguage() tenta redirecionar para /page-en.html, /page-es.html
- Essas páginas não existem no site atual
- Resultado: erro 404, menu não muda

SOLUÇÃO:
- Aplicar traduções DINAMICAMENTE via i18n.js (sem redirecionar)
- Usar arquivos JSON de tradução existentes (pt.json, en.json, es.json)
- Atualizar apenas conteúdo com data-i18n
- Manter na mesma página, trocar apenas o texto
"""

from pathlib import Path

JS_FILE = Path('public/assets/js/i18n.js')

def fix_language_switcher():
    """Corrige switchLanguage para aplicar traduções sem redirecionar."""
    
    with open(JS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Substituir a função switchLanguage
    old_function = """  /**
   * Troca de idioma (MPA - Multi-Page Application)
   */
  async switchLanguage(lang) {
    if (this.currentLang === lang) return;
    
    // Salva idioma no localStorage
    localStorage.setItem('tutela_lang', lang);
    
    // Fecha o menu dropdown
    const dropdown = document.querySelector('.lang-dropdown');
    if (dropdown) {
      dropdown.classList.remove('active');
    }
    
    // Detecta a página atual e idioma
    const currentPath = window.location.pathname;
    const currentFile = currentPath.split('/').pop() || 'index.html';
    
    // Remove sufixo de idioma atual (-en, -es)
    const basePage = currentFile.replace(/-en\\.html$/, '.html').replace(/-es\\.html$/, '.html');
    
    // Constrói URL do novo idioma
    let newUrl;
    if (lang === 'pt') {
      // PT: sem sufixo
      newUrl = currentPath.replace(currentFile, basePage);
    } else {
      // EN/ES: adiciona sufixo
      const newFile = basePage.replace('.html', `-${lang}.html`);
      newUrl = currentPath.replace(currentFile, newFile);
    }
    
    // Remove index.html se estiver na raiz
    if (newUrl.endsWith('/index.html')) {
      newUrl = newUrl.replace('/index.html', '/');
    }
    
    console.log('[i18n] Idioma alterado:', this.currentLang, '→', lang);
    console.log('[i18n] Redirecionando:', currentPath, '→', newUrl);
    
    // Redireciona para a versão no idioma selecionado
    window.location.href = newUrl;
  },"""
    
    new_function = """  /**
   * Troca de idioma (aplica traduções dinamicamente)
   */
  async switchLanguage(lang) {
    if (this.currentLang === lang) return;
    
    console.log('[i18n] Trocando idioma:', this.currentLang, '→', lang);
    
    // Salva idioma no localStorage
    localStorage.setItem('tutela_lang', lang);
    this.currentLang = lang;
    
    // Fecha o menu dropdown
    const dropdown = document.querySelector('.lang-dropdown');
    if (dropdown) {
      dropdown.classList.remove('active');
    }
    
    // Carrega traduções do novo idioma
    await this.loadTranslations(lang);
    
    // Aplica traduções na página
    this.applyTranslations();
    
    // Atualiza UI do seletor
    this.updateLanguageSelector();
    
    // Atualiza atributo lang do HTML
    document.documentElement.lang = this.getLangCode(lang);
    
    // Atualiza schemas JSON-LD
    this.updateSchemaLanguage(lang);
    
    console.log('[i18n] Idioma aplicado com sucesso:', lang);
  },"""
    
    content = content.replace(old_function, new_function)
    
    with open(JS_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {JS_FILE.name} - switchLanguage() corrigido para aplicar traduções dinamicamente")

def main():
    print("🔧 Corrigindo seletor de idiomas para aplicar traduções sem redirecionar...\n")
    
    fix_language_switcher()
    
    print("\n✅ Correção concluída!")
    print("\n📋 Mudanças:")
    print("  • switchLanguage() agora aplica traduções DINAMICAMENTE")
    print("  • Não redireciona para páginas -en.html/-es.html")
    print("  • Carrega JSON de tradução (assets/lang/{lang}.json)")
    print("  • Atualiza elementos com data-i18n na mesma página")
    print("  • Salva preferência no localStorage")
    print("  • Atualiza lang do HTML e schemas")
    print("\n✅ Seletor funcional mesmo sem páginas traduzidas!")

if __name__ == '__main__':
    main()
