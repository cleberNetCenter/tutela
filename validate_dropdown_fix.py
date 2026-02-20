#!/usr/bin/env python3
"""
🧪 TESTE SIMPLIFICADO - Validação de estrutura HTML/CSS/JS
Verifica se os elementos necessários estão presentes e configurados corretamente
"""

import re
import sys
from pathlib import Path

def log(message, status='info'):
    symbols = {
        'info': '📋',
        'success': '✅',
        'error': '❌',
        'warning': '⚠️'
    }
    print(f"{symbols.get(status, '•')} {message}")

def test_dropdown_structure():
    """Testa a estrutura dos arquivos dropdown"""
    
    print("=" * 60)
    print("🧪 VALIDAÇÃO ESTRUTURA DROPDOWN MOBILE")
    print("=" * 60)
    print()
    
    errors = []
    warnings = []
    
    # ========== TESTE 1: Arquivo dropdown-menu.js ==========
    log("TEST 1: Verificando dropdown-menu.js...", 'info')
    
    js_file = Path('public/assets/js/dropdown-menu.js')
    if not js_file.exists():
        errors.append("Arquivo dropdown-menu.js não encontrado")
        log("FALHOU: Arquivo não encontrado", 'error')
    else:
        js_content = js_file.read_text()
        
        # Verificar se o bug do querySelector foi corrigido
        if '> a, > .nav-link' in js_content:
            errors.append("BUG CRÍTICO: querySelector com '> a' ainda presente!")
            log("FALHOU: Seletor inválido '> a' encontrado", 'error')
        else:
            log("PASSOU: Seletor corrigido", 'success')
        
        # Verificar se tem Array.from para buscar children
        if 'Array.from' in js_content and 'children' in js_content:
            log("PASSOU: Array.from(dropdown.children) presente", 'success')
        else:
            errors.append("Correção Array.from não encontrada")
            log("FALHOU: Correção não aplicada", 'error')
        
        # Verificar preventDefault e stopPropagation
        if 'e.preventDefault()' in js_content and 'e.stopPropagation()' in js_content:
            log("PASSOU: preventDefault e stopPropagation presentes", 'success')
        else:
            warnings.append("preventDefault ou stopPropagation ausentes")
            log("AVISO: Propagação de eventos pode ter problemas", 'warning')
        
        # Verificar função isMobile
        if 'function isMobile()' in js_content or 'isMobile()' in js_content:
            log("PASSOU: Função isMobile() presente", 'success')
        else:
            warnings.append("Função isMobile não encontrada")
            log("AVISO: Detecção mobile pode não funcionar", 'warning')
        
        # Verificar toggle de classe .active
        if "classList.toggle('active')" in js_content or "classList.add('active')" in js_content:
            log("PASSOU: Toggle de classe .active presente", 'success')
        else:
            errors.append("Toggle de classe .active não encontrado")
            log("FALHOU: Dropdowns não poderão abrir", 'error')
    
    print()
    
    # ========== TESTE 2: Arquivo dropdown-menu.css ==========
    log("TEST 2: Verificando dropdown-menu.css...", 'info')
    
    css_file = Path('public/assets/css/dropdown-menu.css')
    if not css_file.exists():
        errors.append("Arquivo dropdown-menu.css não encontrado")
        log("FALHOU: Arquivo não encontrado", 'error')
    else:
        css_content = css_file.read_text()
        
        # Verificar regra mobile @media
        if '@media (max-width: 1200px)' in css_content:
            log("PASSOU: Media query mobile presente", 'success')
        else:
            errors.append("Media query mobile não encontrada")
            log("FALHOU: CSS mobile ausente", 'error')
        
        # Verificar regra .nav-dropdown.active .dropdown-menu
        if '.nav-dropdown.active .dropdown-menu' in css_content:
            log("PASSOU: Regra .nav-dropdown.active .dropdown-menu presente", 'success')
            
            # Verificar se display: flex está presente
            active_rule = css_content[css_content.find('.nav-dropdown.active .dropdown-menu'):]
            active_rule = active_rule[:active_rule.find('}')]
            
            if 'display: flex' in active_rule or 'display:flex' in active_rule:
                log("PASSOU: display: flex configurado corretamente", 'success')
            else:
                errors.append("display: flex ausente na regra .active")
                log("FALHOU: Dropdown não ficará visível", 'error')
        else:
            errors.append("Regra CSS .nav-dropdown.active ausente")
            log("FALHOU: Dropdowns não poderão ser mostrados", 'error')
        
        # Verificar desabilitar hover no mobile
        if '.nav-dropdown:hover .dropdown-menu' in css_content:
            hover_section = css_content[css_content.find('@media (max-width: 1200px)'):]
            if 'display: none' in hover_section[:500]:  # Procurar nos primeiros 500 chars
                log("PASSOU: Hover desabilitado no mobile", 'success')
            else:
                warnings.append("Hover pode interferir no mobile")
                log("AVISO: Hover não explicitamente desabilitado", 'warning')
    
    print()
    
    # ========== TESTE 3: Verificar mobile-menu.js ==========
    log("TEST 3: Verificando mobile-menu.js...", 'info')
    
    mobile_js = Path('public/assets/js/mobile-menu.js')
    if not mobile_js.exists():
        errors.append("Arquivo mobile-menu.js não encontrado")
        log("FALHOU: Arquivo não encontrado", 'error')
    else:
        mobile_content = mobile_js.read_text()
        
        # Verificar função toggleMobileMenu
        if 'function toggleMobileMenu()' in mobile_content:
            log("PASSOU: Função toggleMobileMenu presente", 'success')
        else:
            errors.append("Função toggleMobileMenu não encontrada")
            log("FALHOU: Menu mobile não funcionará", 'error')
        
        # Verificar toggle de classe active no nav
        if "nav.classList.toggle('active')" in mobile_content:
            log("PASSOU: Toggle classe .active no #nav", 'success')
        else:
            errors.append("Toggle de #nav.active não encontrado")
            log("FALHOU: Menu não abrirá", 'error')
    
    print()
    
    # ========== TESTE 4: Verificar styles-header-final.css ==========
    log("TEST 4: Verificando styles-header-final.css...", 'info')
    
    header_css = Path('public/assets/css/styles-header-final.css')
    if not header_css.exists():
        errors.append("Arquivo styles-header-final.css não encontrado")
        log("FALHOU: Arquivo não encontrado", 'error')
    else:
        header_content = header_css.read_text()
        
        # Verificar se .nav.active existe
        if '.nav.active' in header_content:
            log("PASSOU: Regra .nav.active presente", 'success')
            
            # Verificar se display: flex está dentro da regra
            nav_active_pos = header_content.find('.nav.active')
            nav_active_rule = header_content[nav_active_pos:nav_active_pos + 500]
            
            if 'display: flex' in nav_active_rule or 'display:flex' in nav_active_rule:
                log("PASSOU: .nav.active com display: flex", 'success')
            else:
                errors.append(".nav.active sem display: flex")
                log("FALHOU: Menu mobile não ficará visível", 'error')
        else:
            errors.append("Regra .nav.active ausente")
            log("FALHOU: Menu mobile não poderá ser mostrado", 'error')
        
        # Verificar media query mobile
        if '@media (max-width: 1200px)' in header_content:
            log("PASSOU: Media query mobile presente", 'success')
        else:
            warnings.append("Media query mobile não encontrada")
            log("AVISO: Estilos mobile podem não aplicar", 'warning')
    
    print()
    
    # ========== TESTE 5: Verificar páginas HTML ==========
    log("TEST 5: Verificando páginas HTML...", 'info')
    
    html_pages = [
        'public/index.html',
        'public/como-funciona.html',
        'public/seguranca.html',
        'public/legal/institucional.html'
    ]
    
    missing_scripts = []
    for page_path in html_pages:
        page = Path(page_path)
        if page.exists():
            content = page.read_text()
            
            has_dropdown_js = 'dropdown-menu.js' in content
            has_mobile_js = 'mobile-menu.js' in content
            has_mobile_btn = 'mobile-menu-btn' in content
            has_nav_dropdown = 'nav-dropdown' in content
            
            if not (has_dropdown_js and has_mobile_js and has_mobile_btn and has_nav_dropdown):
                missing_scripts.append(page_path)
    
    if not missing_scripts:
        log(f"PASSOU: {len(html_pages)} páginas verificadas", 'success')
    else:
        warnings.append(f"{len(missing_scripts)} páginas com scripts ausentes")
        log(f"AVISO: {len(missing_scripts)} páginas com problemas", 'warning')
        for page in missing_scripts:
            log(f"  - {page}", 'warning')
    
    print()
    
    # ========== RESUMO ==========
    print("=" * 60)
    print("📊 RESUMO DA VALIDAÇÃO")
    print("=" * 60)
    print()
    
    if not errors:
        log("SUCESSO: Estrutura correta!", 'success')
        log("Todos os arquivos necessários presentes e configurados", 'success')
        print()
        log("✅ dropdown-menu.js: Seletor corrigido", 'success')
        log("✅ dropdown-menu.css: Regras mobile presentes", 'success')
        log("✅ mobile-menu.js: Função toggle presente", 'success')
        log("✅ styles-header-final.css: .nav.active configurado", 'success')
        log("✅ Páginas HTML: Scripts incluídos", 'success')
        print()
        
        if warnings:
            print("⚠️  AVISOS (não críticos):")
            for warn in warnings:
                log(warn, 'warning')
            print()
        
        print("🎉 VALIDAÇÃO COMPLETA - PRONTO PARA DEPLOY")
        return True
    else:
        log("FALHA: Erros encontrados!", 'error')
        print()
        print("❌ ERROS CRÍTICOS:")
        for error in errors:
            log(error, 'error')
        print()
        
        if warnings:
            print("⚠️  AVISOS:")
            for warn in warnings:
                log(warn, 'warning')
            print()
        
        print("🚫 NÃO FAZER DEPLOY - Corrigir erros primeiro")
        return False

if __name__ == "__main__":
    print()
    result = test_dropdown_structure()
    print()
    sys.exit(0 if result else 1)
