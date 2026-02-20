#!/usr/bin/env python3
"""
🧪 TESTE COMPLETO - MOBILE DROPDOWN FUNCIONAL
Simula interações mobile com os dropdowns e valida comportamento
"""

import asyncio
from playwright.async_api import async_playwright
import sys

async def test_mobile_dropdowns():
    """Testa os dropdowns em modo mobile"""
    
    print("=" * 60)
    print("🧪 TESTE MOBILE DROPDOWN - VALIDAÇÃO COMPLETA")
    print("=" * 60)
    print()
    
    async with async_playwright() as p:
        # Abrir browser em modo mobile
        browser = await p.chromium.launch(headless=True)
        
        # iPhone 12 Pro dimensions
        context = await browser.new_context(
            viewport={'width': 390, 'height': 844},
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
        )
        
        page = await context.new_page()
        
        # Capturar console logs
        console_logs = []
        page.on('console', lambda msg: console_logs.append(f"[{msg.type}] {msg.text}"))
        
        # Abrir página
        url = "http://localhost:8000/public/test_dropdown_inline.html"
        print(f"📱 Abrindo página: {url}")
        
        try:
            await page.goto(url, wait_until='networkidle', timeout=15000)
        except Exception as e:
            print(f"❌ ERRO ao carregar página: {e}")
            await browser.close()
            return False
        
        print(f"✅ Página carregada")
        print()
        
        # Aguardar DOM carregar
        await page.wait_for_selector('.mobile-menu-btn', timeout=5000)
        
        # Obter dimensões
        viewport_width = await page.evaluate('window.innerWidth')
        print(f"📐 Largura viewport: {viewport_width}px")
        
        if viewport_width > 1200:
            print("❌ ERRO: Viewport não está em modo mobile!")
            await browser.close()
            return False
        
        print("✅ Modo mobile detectado")
        print()
        
        # ========== TESTE 1: Abrir Menu Mobile ==========
        print("TEST 1: Abrindo menu mobile...")
        await page.click('.mobile-menu-btn')
        await asyncio.sleep(0.3)
        
        nav_active = await page.evaluate('document.getElementById("nav").classList.contains("active")')
        
        if nav_active:
            print("✅ PASSOU: Menu mobile aberto")
        else:
            print("❌ FALHOU: Menu mobile NÃO abriu")
            await browser.close()
            return False
        
        print()
        
        # ========== TESTE 2: Abrir Dropdown 1 ==========
        print("TEST 2: Abrindo Dropdown 1 (Soluções)...")
        
        dropdowns = await page.query_selector_all('.nav-dropdown')
        if len(dropdowns) < 2:
            print(f"❌ ERRO: Apenas {len(dropdowns)} dropdown(s) encontrado(s)")
            await browser.close()
            return False
        
        # Clicar no primeiro dropdown
        await dropdowns[0].query_selector('.nav-link').then(lambda el: el.click())
        await asyncio.sleep(0.3)
        
        d1_active = await page.evaluate('document.querySelectorAll(".nav-dropdown")[0].classList.contains("active")')
        
        if d1_active:
            print("✅ PASSOU: Dropdown 1 aberto")
        else:
            print("❌ FALHOU: Dropdown 1 NÃO abriu")
            
            # Debug
            print("\n🔍 DEBUG INFO:")
            classes = await page.evaluate('document.querySelectorAll(".nav-dropdown")[0].className')
            print(f"   Classes dropdown 1: {classes}")
            
            await browser.close()
            return False
        
        print()
        
        # ========== TESTE 3: Abrir Dropdown 2 (deve fechar Dropdown 1) ==========
        print("TEST 3: Abrindo Dropdown 2 (Base Jurídica)...")
        
        await dropdowns[1].query_selector('.nav-link').then(lambda el: el.click())
        await asyncio.sleep(0.3)
        
        d1_active = await page.evaluate('document.querySelectorAll(".nav-dropdown")[0].classList.contains("active")')
        d2_active = await page.evaluate('document.querySelectorAll(".nav-dropdown")[1].classList.contains("active")')
        
        if not d1_active and d2_active:
            print("✅ PASSOU: Dropdown 2 aberto, Dropdown 1 fechado")
        else:
            print("❌ FALHOU: Comportamento incorreto")
            print(f"   Dropdown 1: {'aberto' if d1_active else 'fechado'}")
            print(f"   Dropdown 2: {'aberto' if d2_active else 'fechado'}")
            await browser.close()
            return False
        
        print()
        
        # ========== TESTE 4: Fechar Dropdown clicando no toggle ==========
        print("TEST 4: Fechando Dropdown 2 (clique no toggle)...")
        
        await dropdowns[1].query_selector('.nav-link').then(lambda el: el.click())
        await asyncio.sleep(0.3)
        
        d2_active = await page.evaluate('document.querySelectorAll(".nav-dropdown")[1].classList.contains("active")')
        
        if not d2_active:
            print("✅ PASSOU: Dropdown 2 fechado")
        else:
            print("❌ FALHOU: Dropdown 2 ainda aberto")
            await browser.close()
            return False
        
        print()
        
        # ========== TESTE 5: Verificar CSS display do dropdown menu ==========
        print("TEST 5: Verificando display CSS do dropdown menu...")
        
        # Abrir dropdown 1
        await dropdowns[0].query_selector('.nav-link').then(lambda el: el.click())
        await asyncio.sleep(0.3)
        
        # Verificar se o .dropdown-menu está visível
        menu_display = await page.evaluate('''
            const menu = document.querySelectorAll('.nav-dropdown')[0].querySelector('.dropdown-menu');
            window.getComputedStyle(menu).display;
        ''')
        
        if menu_display == 'flex':
            print(f"✅ PASSOU: Dropdown menu display = '{menu_display}'")
        else:
            print(f"❌ FALHOU: Dropdown menu display = '{menu_display}' (esperado: 'flex')")
            await browser.close()
            return False
        
        print()
        
        # ========== TESTE 6: Verificar links dentro do dropdown ==========
        print("TEST 6: Verificando links dentro do dropdown...")
        
        links = await page.evaluate('''
            const menu = document.querySelectorAll('.nav-dropdown')[0].querySelector('.dropdown-menu');
            Array.from(menu.querySelectorAll('a')).map(a => a.textContent.trim());
        ''')
        
        print(f"   Links encontrados: {len(links)}")
        for link in links:
            print(f"     - {link}")
        
        if len(links) >= 3:
            print("✅ PASSOU: Links do dropdown encontrados")
        else:
            print("❌ FALHOU: Número insuficiente de links")
            await browser.close()
            return False
        
        print()
        
        # ========== RESUMO ==========
        print("=" * 60)
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("=" * 60)
        print()
        print("✅ Menu mobile funcional")
        print("✅ Dropdowns abrem/fecham corretamente")
        print("✅ Apenas um dropdown aberto por vez")
        print("✅ CSS display correto")
        print("✅ Links internos acessíveis")
        print()
        print("📋 Console Logs da página:")
        for log in console_logs[-10:]:  # Últimos 10 logs
            print(f"   {log}")
        print()
        
        await browser.close()
        return True

if __name__ == "__main__":
    print()
    result = asyncio.run(test_mobile_dropdowns())
    
    if result:
        print("✅ RESULTADO FINAL: SUCESSO")
        print()
        sys.exit(0)
    else:
        print("❌ RESULTADO FINAL: FALHA")
        print()
        sys.exit(1)
