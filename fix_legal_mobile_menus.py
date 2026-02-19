#!/usr/bin/env python3
"""
Script para corrigir problemas de menu nas páginas legais e mobile:
1. Menu de idiomas desaparece nas páginas legais
2. Menus não funcionam corretamente no mobile
3. Adicionar botão mobile-menu funcional
"""

import re

def fix_header_final_css():
    """Adiciona CSS para mobile menu e corrige z-index nas páginas legais"""
    
    css_file = "public/assets/css/styles-header-final.css"
    
    with open(css_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Adicionar CSS para mobile menu button
    mobile_menu_css = """
/* =========================================================
   MOBILE MENU BUTTON
   ========================================================= */

.mobile-menu-btn {
  display: none;
  flex-direction: column;
  justify-content: space-around;
  width: 32px;
  height: 32px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  margin-left: 1rem;
  z-index: 10;
}

.mobile-menu-btn span {
  width: 100%;
  height: 3px;
  background: #ffffff;
  border-radius: 2px;
  transition: all 0.3s ease;
}

.mobile-menu-btn:hover span {
  background: rgba(255, 255, 255, 0.85);
}

/* Mostrar botão mobile em tablets e celulares */
@media (max-width: 1200px) {
  .mobile-menu-btn {
    display: flex;
  }
  
  /* Garantir que menu de idiomas fique visível */
  .lang-dropdown {
    position: relative;
    z-index: 1200;
  }
  
  /* Menu mobile sobrepõe conteúdo */
  .nav {
    position: fixed;
    top: 70px;
    left: 0;
    right: 0;
    background: var(--color-surface-base);
    flex-direction: column;
    padding: 1rem 0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    z-index: 1150;
    max-height: calc(100vh - 70px);
    overflow-y: auto;
  }
  
  .nav-link,
  .nav-dropdown > a {
    padding: 1rem 1.5rem;
    width: 100%;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .nav-dropdown {
    width: 100%;
  }
  
  .dropdown-menu {
    position: static;
    box-shadow: none;
    border: none;
    background: rgba(0, 0, 0, 0.2);
    padding-left: 1rem;
  }
  
  .dropdown-menu li {
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  }
  
  .dropdown-menu li:last-child {
    border-bottom: none;
  }
  
  .dropdown-menu a {
    padding: 0.75rem 1rem;
  }
  
  /* Ajustar header CTA no mobile */
  .header-cta {
    display: none;
  }
}

@media (max-width: 900px) {
  .mobile-menu-btn {
    display: flex;
  }
  
  .header-inner {
    gap: 0.5rem;
  }
  
  .lang-dropdown {
    margin-left: auto;
  }
}

/* Estado ativo do mobile menu (hamburger -> X) */
.mobile-menu-btn.active span:nth-child(1) {
  transform: rotate(45deg) translate(8px, 8px);
}

.mobile-menu-btn.active span:nth-child(2) {
  opacity: 0;
}

.mobile-menu-btn.active span:nth-child(3) {
  transform: rotate(-45deg) translate(7px, -7px);
}
"""
    
    # Verificar se já existe o CSS do mobile menu
    if ".mobile-menu-btn" not in content:
        # Inserir antes da seção do WhatsApp float
        whatsapp_pos = content.find("/* =======================================================")
        if whatsapp_pos > 0:
            content = content[:whatsapp_pos] + mobile_menu_css + "\n\n" + content[whatsapp_pos:]
        else:
            content += "\n\n" + mobile_menu_css
    
    # Salvar arquivo
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {css_file} atualizado com CSS para mobile menu")

def add_mobile_menu_js():
    """Adiciona JavaScript para controlar o mobile menu"""
    
    js_content = """// =======================================================
// MOBILE MENU TOGGLE - Tutela Digital
// =======================================================

function toggleMobileMenu() {
  const nav = document.getElementById('nav');
  const btn = document.querySelector('.mobile-menu-btn');
  
  if (!nav || !btn) return;
  
  // Toggle classes
  nav.classList.toggle('active');
  btn.classList.toggle('active');
  
  // Prevenir scroll quando menu aberto
  if (nav.classList.contains('active')) {
    document.body.style.overflow = 'hidden';
  } else {
    document.body.style.overflow = '';
  }
}

// Fechar menu ao clicar em um link
document.addEventListener('DOMContentLoaded', function() {
  const navLinks = document.querySelectorAll('.nav a');
  
  navLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      // Se for um link de dropdown, não fechar
      if (this.parentElement.classList.contains('nav-dropdown') && 
          this.classList.contains('nav-link')) {
        return;
      }
      
      // Fechar menu mobile
      const nav = document.getElementById('nav');
      const btn = document.querySelector('.mobile-menu-btn');
      
      if (nav && nav.classList.contains('active')) {
        nav.classList.remove('active');
        if (btn) btn.classList.remove('active');
        document.body.style.overflow = '';
      }
    });
  });
  
  // Fechar menu ao clicar fora (apenas mobile)
  document.addEventListener('click', function(e) {
    const nav = document.getElementById('nav');
    const btn = document.querySelector('.mobile-menu-btn');
    const langDropdown = document.querySelector('.lang-dropdown');
    
    if (!nav || !btn) return;
    
    // Verificar se está em mobile
    if (window.innerWidth > 1200) return;
    
    // Verificar se clique foi fora do nav e do botão e do menu de idiomas
    if (!nav.contains(e.target) && 
        !btn.contains(e.target) && 
        (!langDropdown || !langDropdown.contains(e.target)) &&
        nav.classList.contains('active')) {
      nav.classList.remove('active');
      btn.classList.remove('active');
      document.body.style.overflow = '';
    }
  });
});

// =======================================================
// LANGUAGE DROPDOWN - Mobile Support
// =======================================================

document.addEventListener('DOMContentLoaded', function() {
  const langDropdown = document.querySelector('.lang-dropdown');
  const langToggle = document.querySelector('.lang-toggle');
  const langMenu = document.querySelector('.lang-menu');
  
  if (!langDropdown || !langToggle || !langMenu) return;
  
  // Toggle no mobile e desktop
  langToggle.addEventListener('click', function(e) {
    e.stopPropagation();
    langDropdown.classList.toggle('active');
  });
  
  // Fechar ao clicar em uma opção
  const langOptions = langMenu.querySelectorAll('.lang-option');
  langOptions.forEach(option => {
    option.addEventListener('click', function() {
      langDropdown.classList.remove('active');
    });
  });
  
  // Fechar ao clicar fora
  document.addEventListener('click', function(e) {
    if (!langDropdown.contains(e.target)) {
      langDropdown.classList.remove('active');
    }
  });
});
"""
    
    js_file = "public/assets/js/mobile-menu.js"
    
    with open(js_file, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"✅ {js_file} criado")

def update_legal_pages():
    """Atualiza páginas legais para incluir o script mobile-menu.js"""
    
    import glob
    
    legal_pages = glob.glob("public/legal/*.html")
    
    for page_file in legal_pages:
        with open(page_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar se já tem o script
        if "mobile-menu.js" in content:
            print(f"⏭️  {page_file} já tem mobile-menu.js")
            continue
        
        # Adicionar script antes do </body>
        if "</body>" in content:
            script_tag = '  <script src="/assets/js/mobile-menu.js?v=202602190200"></script>\n</body>'
            content = content.replace("</body>", script_tag)
            
            with open(page_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ {page_file} atualizado com mobile-menu.js")

def update_main_pages():
    """Atualiza páginas principais para incluir o script mobile-menu.js"""
    
    import glob
    
    main_pages = glob.glob("public/*.html")
    
    for page_file in main_pages:
        with open(page_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar se já tem o script
        if "mobile-menu.js" in content:
            print(f"⏭️  {page_file} já tem mobile-menu.js")
            continue
        
        # Adicionar script antes do i18n.js (se existir) ou antes do </body>
        if "i18n.js" in content:
            # Adicionar antes do i18n.js
            content = re.sub(
                r'(\s*)<script src="assets/js/i18n\.js',
                r'  <script src="assets/js/mobile-menu.js?v=202602190200"></script>\n\1<script src="assets/js/i18n.js',
                content
            )
        elif "</body>" in content:
            script_tag = '  <script src="assets/js/mobile-menu.js?v=202602190200"></script>\n</body>'
            content = content.replace("</body>", script_tag)
        else:
            print(f"⚠️  Não foi possível adicionar script em {page_file}")
            continue
        
        with open(page_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ {page_file} atualizado com mobile-menu.js")

if __name__ == "__main__":
    print("🔧 Corrigindo menus nas páginas legais e mobile...\n")
    
    fix_header_final_css()
    add_mobile_menu_js()
    update_legal_pages()
    update_main_pages()
    
    print("\n✅ Todas as correções aplicadas!")
    print("\n📋 Resumo das mudanças:")
    print("  1. ✅ CSS mobile menu adicionado (styles-header-final.css)")
    print("  2. ✅ JavaScript mobile-menu.js criado")
    print("  3. ✅ Páginas legais atualizadas com script")
    print("  4. ✅ Páginas principais atualizadas com script")
    print("  5. ✅ Menu de idiomas com z-index correto")
    print("  6. ✅ Suporte completo para mobile (tablets e celulares)")
