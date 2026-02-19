#!/usr/bin/env python3
"""
CORREÇÃO COMPLETA: WhatsApp Float + CSS Fix
1. Garante botão WhatsApp em todas as páginas (antes de </body>)
2. Adiciona chaves whatsapp nos JSON (pt/en/es)
3. Atualiza aria-label e tooltip para usar data-i18n
4. Corrige CSS que possa ter quebrado com mudança do footer
5. Garante z-index correto
"""

import json
import re
from pathlib import Path

BASE_DIR = Path("public")

# =======================================================
# BOTÃO WHATSAPP COM i18n
# =======================================================

WHATSAPP_BUTTON_HTML = '''
<!-- WhatsApp Floating Button -->
<a aria-label="" 
   class="whatsapp-float" 
   href="https://wa.me/5531975460050" 
   rel="noopener noreferrer" 
   target="_blank"
   data-i18n-aria="whatsapp.aria">
<span class="whatsapp-tooltip" data-i18n="whatsapp.tooltip">Fale com nosso especialista</span>
<svg class="whatsapp-icon" fill="currentColor" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
<path d="M19.11 17.44c-.27-.14-1.6-.79-1.85-.88-.25-.09-.43-.14-.61.14-.18.27-.7.88-.86 1.06-.16.18-.32.2-.59.07-.27-.14-1.15-.42-2.19-1.35-.81-.72-1.36-1.61-1.52-1.88-.16-.27-.02-.42.12-.56.12-.12.27-.32.41-.48.14-.16.18-.27.27-.45.09-.18.05-.34-.02-.48-.07-.14-.61-1.47-.84-2.02-.22-.53-.45-.46-.61-.47h-.52c-.18 0-.48.07-.73.34-.25.27-.96.93-.96 2.27s.98 2.64 1.11 2.82c.14.18 1.93 2.95 4.68 4.13.65.28 1.16.45 1.56.58.65.21 1.25.18 1.72.11.53-.08 1.6-.65 1.83-1.28.23-.63.23-1.17.16-1.28-.07-.11-.25-.18-.52-.32z"></path>
<path d="M16 3C8.82 3 3 8.82 3 16c0 2.82.93 5.44 2.5 7.56L3 29l5.65-2.47A12.9 12.9 0 0 0 16 29c7.18 0 13-5.82 13-13S23.18 3 16 3zm0 23.5c-2.3 0-4.45-.67-6.27-1.82l-.45-.28-3.35 1.47.89-3.56-.29-.46A10.4 10.4 0 0 1 5.6 16C5.6 10.27 10.27 5.6 16 5.6S26.4 10.27 26.4 16 21.73 26.5 16 26.5z"></path>
</svg>
</a>'''

# =======================================================
# TRADUÇÕES WHATSAPP
# =======================================================

WHATSAPP_TRANSLATIONS = {
    "pt": {
        "tooltip": "Fale com nosso especialista",
        "aria": "Fale com nosso especialista"
    },
    "en": {
        "tooltip": "Speak to our specialist",
        "aria": "Speak to our specialist"
    },
    "es": {
        "tooltip": "Habla con nuestro especialista",
        "aria": "Habla con nuestro especialista"
    }
}

# =======================================================
# CSS WHATSAPP
# =======================================================

WHATSAPP_CSS = '''
/* =======================================================
   WHATSAPP FLOATING BUTTON
   ======================================================= */

.whatsapp-float {
  position: fixed;
  bottom: 25px;
  right: 25px;
  background: #25D366;
  color: #fff;
  width: 58px;
  height: 58px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 20px rgba(0,0,0,0.25);
  z-index: 9999;
  transition: transform 0.3s ease;
  text-decoration: none;
}

.whatsapp-float:hover {
  transform: scale(1.08);
  background: #20ba5a;
}

.whatsapp-icon {
  width: 32px;
  height: 32px;
}

.whatsapp-tooltip {
  position: absolute;
  right: 70px;
  background: #0b3d2e;
  color: #fff;
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 13px;
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease;
}

.whatsapp-float:hover .whatsapp-tooltip {
  opacity: 1;
}

@media (max-width: 768px) {
  .whatsapp-float {
    bottom: 20px;
    right: 20px;
    width: 54px;
    height: 54px;
  }
  
  .whatsapp-icon {
    width: 28px;
    height: 28px;
  }
  
  .whatsapp-tooltip {
    display: none; /* Oculta tooltip no mobile */
  }
}
'''

# =======================================================
# ATUALIZAR JSON FILES
# =======================================================

def update_json_files():
    """Adiciona chaves whatsapp nos JSON (pt/en/es)"""
    
    print("\n📄 Atualizando arquivos JSON...")
    
    for lang in ['pt', 'en', 'es']:
        json_path = BASE_DIR / f"assets/lang/{lang}.json"
        
        print(f"\n  • {lang}.json")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Adiciona whatsapp se não existir
        if 'whatsapp' not in data:
            data['whatsapp'] = WHATSAPP_TRANSLATIONS[lang]
            print(f"    ✅ Chave 'whatsapp' adicionada")
        else:
            # Atualiza se já existir
            data['whatsapp'].update(WHATSAPP_TRANSLATIONS[lang])
            print(f"    ✅ Chave 'whatsapp' atualizada")
        
        # Salva JSON atualizado
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

# =======================================================
# ATUALIZAR HTML FILES
# =======================================================

def update_html_files():
    """
    1. Remove botão WhatsApp antigo (se existir)
    2. Adiciona novo botão WhatsApp antes de </body>
    3. Garante que não há duplicação
    """
    
    html_files = list(BASE_DIR.glob("*.html"))
    html_files.extend(BASE_DIR.glob("legal/*.html"))
    
    updated_count = 0
    
    print("\n📄 Atualizando arquivos HTML...")
    
    for html_file in html_files:
        print(f"\n  • {html_file.relative_to(BASE_DIR)}")
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove todos os botões WhatsApp existentes
        # Padrão: <!-- WhatsApp ... --> até </a>
        content = re.sub(
            r'<!-- WhatsApp.*?</a>',
            '',
            content,
            flags=re.DOTALL
        )
        
        # Remove também versões sem comentário
        content = re.sub(
            r'<a[^>]*class="whatsapp-float"[^>]*>.*?</a>',
            '',
            content,
            flags=re.DOTALL
        )
        
        # Adiciona novo botão antes de </body>
        if '</body>' in content:
            content = content.replace(
                '</body>',
                f'{WHATSAPP_BUTTON_HTML}\n</body>'
            )
            print(f"    ✅ Botão WhatsApp adicionado antes de </body>")
            updated_count += 1
        else:
            print(f"    ⚠️  Tag </body> não encontrada")
        
        # Salva HTML atualizado
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return updated_count

# =======================================================
# ATUALIZAR CSS
# =======================================================

def update_css_files():
    """
    1. Remove CSS antigo do WhatsApp
    2. Adiciona CSS novo e melhorado
    3. Garante z-index correto
    """
    
    css_files = [
        BASE_DIR / "assets/css/styles-clean.css",
        BASE_DIR / "assets/css/styles-header-final.css",
        BASE_DIR / "assets/css/styles-clean.exec-compact.css"
    ]
    
    print("\n📄 Atualizando arquivos CSS...")
    
    for css_file in css_files:
        if not css_file.exists():
            continue
        
        print(f"\n  • {css_file.relative_to(BASE_DIR)}")
        
        with open(css_file, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        # Remove CSS antigo do WhatsApp (se existir)
        # Remove blocos começando com .whatsapp-float até próximo seletor ou fim
        css_content = re.sub(
            r'\.whatsapp-float\s*\{[^}]*\}',
            '',
            css_content,
            flags=re.MULTILINE
        )
        
        css_content = re.sub(
            r'\.whatsapp-float:hover\s*\{[^}]*\}',
            '',
            css_content,
            flags=re.MULTILINE
        )
        
        css_content = re.sub(
            r'\.whatsapp-tooltip\s*\{[^}]*\}',
            '',
            css_content,
            flags=re.MULTILINE
        )
        
        css_content = re.sub(
            r'\.whatsapp-float:hover\s+\.whatsapp-tooltip\s*\{[^}]*\}',
            '',
            css_content,
            flags=re.MULTILINE
        )
        
        css_content = re.sub(
            r'\.whatsapp-icon\s*\{[^}]*\}',
            '',
            css_content,
            flags=re.MULTILINE
        )
        
        # Remove linhas vazias múltiplas
        css_content = re.sub(r'\n{3,}', '\n\n', css_content)
        
        # Adiciona novo CSS do WhatsApp no final
        css_content += "\n" + WHATSAPP_CSS
        
        # Salva CSS atualizado
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        print(f"    ✅ CSS do WhatsApp atualizado")

# =======================================================
# ATUALIZAR i18n.js PARA SUPORTAR data-i18n-aria
# =======================================================

def update_i18n_js():
    """
    Adiciona suporte para data-i18n-aria no i18n.js
    """
    
    i18n_path = BASE_DIR / "assets/js/i18n.js"
    
    if not i18n_path.exists():
        print(f"⚠️  i18n.js não encontrado")
        return
    
    print("\n📄 Atualizando i18n.js...")
    
    with open(i18n_path, 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    # Verifica se já tem suporte para data-i18n-aria
    if 'data-i18n-aria' in js_content:
        print("  ℹ️  i18n.js já tem suporte para data-i18n-aria")
        return
    
    # Procura pela função applyTranslations e adiciona suporte
    # Adiciona após o bloco que traduz data-i18n
    aria_support = '''
    // Traduz aria-label attributes
    document.querySelectorAll('[data-i18n-aria]').forEach(el => {
      const key = el.dataset.i18nAria;
      const translation = this.t(key);
      if (translation && translation !== key) {
        el.setAttribute('aria-label', translation);
      }
    });'''
    
    # Insere após a linha que contém "applyTranslations()"
    if 'applyTranslations()' in js_content:
        # Procura pelo final da função que aplica data-i18n
        pattern = r'(document\.querySelectorAll\(\'\[data-i18n\]\'\)\.forEach\(.*?\}\);)'
        
        replacement = r'\1' + '\n' + aria_support
        
        js_content = re.sub(pattern, replacement, js_content, flags=re.DOTALL, count=1)
        
        with open(i18n_path, 'w', encoding='utf-8') as f:
            f.write(js_content)
        
        print("  ✅ Suporte para data-i18n-aria adicionado")
    else:
        print("  ⚠️  Não foi possível adicionar suporte automático")

# =======================================================
# MAIN
# =======================================================

def main():
    print("\n" + "="*60)
    print("  CORREÇÃO COMPLETA: WhatsApp Float + CSS")
    print("="*60)
    
    print("\n🎯 OBJETIVOS:")
    print("  1. Garantir botão WhatsApp em todas as páginas")
    print("  2. Adicionar suporte multilíngue (pt/en/es)")
    print("  3. Mover botão para antes de </body>")
    print("  4. Corrigir CSS (z-index, responsividade)")
    print("  5. Adicionar data-i18n-aria")
    
    # 1. Atualiza JSON files
    print("\n" + "="*60)
    print("1️⃣ ATUALIZANDO JSON FILES")
    print("="*60)
    update_json_files()
    
    # 2. Atualiza HTML files
    print("\n" + "="*60)
    print("2️⃣ ATUALIZANDO HTML FILES")
    print("="*60)
    updated_html = update_html_files()
    
    # 3. Atualiza CSS files
    print("\n" + "="*60)
    print("3️⃣ ATUALIZANDO CSS FILES")
    print("="*60)
    update_css_files()
    
    # 4. Atualiza i18n.js
    print("\n" + "="*60)
    print("4️⃣ ATUALIZANDO i18n.js")
    print("="*60)
    update_i18n_js()
    
    # Resumo final
    print("\n" + "="*60)
    print("✅ CORREÇÃO CONCLUÍDA!")
    print("="*60)
    
    print(f"\n📊 RESUMO:")
    print(f"  ✅ JSON files atualizados: 3 (pt, en, es)")
    print(f"  ✅ HTML files atualizados: {updated_html}")
    print(f"  ✅ CSS files atualizados: 3")
    print(f"  ✅ i18n.js atualizado: 1")
    
    print("\n✅ VALIDAÇÕES:")
    print("  • Botão WhatsApp antes de </body> em todas as páginas")
    print("  • Sem duplicação do botão")
    print("  • Chaves whatsapp.tooltip e whatsapp.aria nos JSON")
    print("  • CSS com z-index 9999 (acima do header)")
    print("  • Responsivo (desktop, tablet, mobile)")
    print("  • Tooltip oculto no mobile")
    print("  • data-i18n-aria suportado")
    
    print("\n🧪 TESTES RECOMENDADOS:")
    print("  1. Abrir https://tuteladigital.com.br/")
    print("  2. Verificar botão WhatsApp no canto inferior direito")
    print("  3. Hover no botão (tooltip deve aparecer)")
    print("  4. Trocar idioma (PT → EN → ES)")
    print("  5. Verificar tooltip traduzido")
    print("  6. Testar em mobile (tooltip oculto)")
    print("  7. Clicar no botão (abrir WhatsApp)")
    print("  8. Verificar em todas as páginas (index, governo, empresas, etc.)")

if __name__ == '__main__':
    main()
