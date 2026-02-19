#!/usr/bin/env python3
"""
Adiciona scripts i18n.js e dropdown-menu.js nas páginas legais
para suportar troca de idioma e exibição de aviso
"""
import re
from pathlib import Path

def add_i18n_scripts(html_file):
    """Adiciona scripts i18n antes do </body>"""
    print(f"\n📄 Processando: {html_file.name}")
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar se já tem os scripts
    if 'i18n.js' in content:
        print("  ℹ️  Scripts i18n já existem")
        return False
    
    # Scripts a adicionar (antes do </body>)
    scripts = '''
<!-- Scripts de internacionalização e navegação -->
<script src="/assets/js/navigation.js?v=202602190108"></script>
<script src="/assets/js/i18n.js?v=9"></script>
<script src="/assets/js/dropdown-menu.js?v=202602190108"></script>

<!-- Inicializar i18n para páginas legais -->
<script>
document.addEventListener('DOMContentLoaded', async () => {
  // Inicializa sistema i18n
  await I18N.init();
  
  // Força exibição do aviso se não estiver em PT
  if (I18N.currentLang !== 'pt') {
    console.log('[Legal Page] Idioma atual:', I18N.currentLang, '- Exibindo aviso');
    I18N.showLegalPageNoticeIfNeeded();
  }
});
</script>

</body>'''
    
    # Substituir </body> pelo novo conteúdo
    if '</body>' in content:
        content = content.replace('</body>', scripts)
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("  ✅ Scripts adicionados")
        return True
    else:
        print("  ❌ Tag </body> não encontrada")
        return False

def main():
    """Adiciona scripts em todas as páginas legais"""
    print("🔧 ADICIONANDO SCRIPTS i18n - Páginas Legais")
    print("=" * 70)
    
    legal_dir = Path('public/legal')
    html_files = list(legal_dir.glob('*.html'))
    
    print(f"\n📁 Encontradas {len(html_files)} páginas legais")
    
    updated = 0
    for html_file in html_files:
        if add_i18n_scripts(html_file):
            updated += 1
    
    print("\n" + "=" * 70)
    print(f"✅ CONCLUÍDO: {updated} páginas atualizadas")
    
    if updated > 0:
        print("\n📋 Scripts adicionados:")
        print("   • navigation.js (suporte ao menu)")
        print("   • i18n.js v=9 (sistema de tradução)")
        print("   • dropdown-menu.js (menu dropdown)")
        print("   • Inicializador automático do i18n")
        print("   • Exibição automática de aviso em idiomas não-PT")

if __name__ == '__main__':
    main()
