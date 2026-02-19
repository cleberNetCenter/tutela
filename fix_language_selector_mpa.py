#!/usr/bin/env python3
"""
Script para corrigir o seletor de idiomas no contexto MPA.

PROBLEMA:
- i18n.js faz window.location.reload() ao trocar idioma
- No MPA, isso recarrega a mesma página em PT (sem efeito)
- Menu não muda quando seleciona outra língua

SOLUÇÃO:
- Atualizar switchLanguage() para redirecionar para versões traduzidas
- Estrutura de URLs:
  • PT: /index.html, /como-funciona.html, /seguranca.html
  • EN: /index-en.html, /como-funciona-en.html, /seguranca-en.html
  • ES: /index-es.html, /como-funciona-es.html, /seguranca-es.html
- Salvar idioma no localStorage
- Atualizar visual do botão lang-toggle
"""

from pathlib import Path

PUBLIC_DIR = Path('public')
JS_FILE = PUBLIC_DIR / 'assets' / 'js' / 'i18n.js'

def fix_i18n_mpa():
    """Corrige i18n.js para funcionar em MPA."""
    
    with open(JS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Substituir a função switchLanguage
    old_switch = """  /**
   * Troca de idioma
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
    
    // Recarrega a página para aplicar traduções completas
    console.log('[i18n] Idioma alterado para:', lang, '- Recarregando página...');
    window.location.reload();
  },"""
    
    new_switch = """  /**
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
    
    content = content.replace(old_switch, new_switch)
    
    with open(JS_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {JS_FILE.name} - switchLanguage() atualizado para MPA")

def main():
    """Executa a correção."""
    print("🔧 Corrigindo seletor de idiomas para MPA...\n")
    
    fix_i18n_mpa()
    
    print("\n✅ Correção concluída!")
    print("\n📋 Mudanças aplicadas:")
    print("  • switchLanguage() agora redireciona para URLs traduzidas")
    print("  • PT: /page.html")
    print("  • EN: /page-en.html")
    print("  • ES: /page-es.html")
    print("  • localStorage salva preferência do usuário")
    print("\n✅ Seletor de idiomas agora funcional no MPA!")

if __name__ == '__main__':
    main()
