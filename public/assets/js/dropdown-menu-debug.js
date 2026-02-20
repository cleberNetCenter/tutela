
// =======================================================
// NAVIGATION DROPDOWNS - Mobile & Desktop Support + DEBUG
// Suporta MÚLTIPLOS dropdowns (Soluções, Base Jurídica, etc.)
// =======================================================

(function() {
  'use strict';
  
  // DEBUG: Flag para habilitar logs detalhados
  const DEBUG = true;
  
  function debugLog(message, type = 'info') {
    if (!DEBUG) return;
    
    const styles = {
      info: 'color: #00aaff; font-weight: bold;',
      success: 'color: #00ff00; font-weight: bold;',
      error: 'color: #ff0000; font-weight: bold;',
      warning: 'color: #ffaa00; font-weight: bold;'
    };
    
    console.log(`%c[DROPDOWN-DEBUG] ${message}`, styles[type] || styles.info);
  }

  document.addEventListener('DOMContentLoaded', function() {
    debugLog('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'info');
    debugLog('INICIALIZANDO DROPDOWN MOBILE', 'info');
    debugLog('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'info');
    debugLog(`Timestamp: ${new Date().toISOString()}`, 'info');
    debugLog(`Window Width: ${window.innerWidth}px`, 'info');
    debugLog(`Window Height: ${window.innerHeight}px`, 'info');
    debugLog(`User Agent: ${navigator.userAgent}`, 'info');
    
    // Função para verificar se está em mobile
    function isMobile() {
      const mobile = window.innerWidth <= 1200;
      debugLog(`isMobile() = ${mobile} (width: ${window.innerWidth}px)`, mobile ? 'success' : 'warning');
      return mobile;
    }
    
    // Selecionar TODOS os dropdowns
    debugLog('Procurando por .nav-dropdown...', 'info');
    const navDropdowns = document.querySelectorAll('.nav-dropdown');
    
    if (navDropdowns.length === 0) {
      debugLog('❌ ERRO: Nenhum dropdown encontrado!', 'error');
      debugLog('Verifique se os elementos HTML possuem a classe .nav-dropdown', 'warning');
      return;
    }
    
    debugLog(`✅ ${navDropdowns.length} dropdown(s) encontrado(s)`, 'success');
    
    // Configurar cada dropdown individualmente
    navDropdowns.forEach((dropdown, index) => {
      debugLog(`\n--- Configurando Dropdown ${index + 1} ---`, 'info');
      
      // FIX: querySelector não aceita '>' no início - buscar filhos diretos manualmente
      debugLog(`Buscando toggle (filho direto <a> ou .nav-link)...`, 'info');
      
      const children = Array.from(dropdown.children);
      debugLog(`Dropdown tem ${children.length} filho(s) direto(s)`, 'info');
      
      children.forEach((child, i) => {
        debugLog(`  Filho ${i}: <${child.tagName}> classes=[${child.className}]`, 'info');
      });
      
      const toggle = children.find(el => 
        el.tagName === 'A' || el.classList.contains('nav-link')
      );
      
      if (toggle) {
        debugLog(`✅ Toggle encontrado: <${toggle.tagName}> "${toggle.textContent.trim()}"`, 'success');
      } else {
        debugLog(`❌ Toggle NÃO encontrado!`, 'error');
      }
      
      const menu = dropdown.querySelector('.dropdown-menu');
      
      if (menu) {
        const menuLinks = menu.querySelectorAll('a');
        debugLog(`✅ Menu encontrado com ${menuLinks.length} link(s)`, 'success');
      } else {
        debugLog(`❌ Menu (.dropdown-menu) NÃO encontrado!`, 'error');
      }
      
      if (!toggle || !menu) {
        debugLog(`⚠️ Dropdown ${index + 1} incompleto - PULANDO`, 'warning');
        return;
      }
      
      // Mobile: toggle dropdown ao clicar
      debugLog(`Adicionando event listener 'click' no toggle...`, 'info');
      
      toggle.addEventListener('click', function(e) {
        debugLog(`\n🖱️ CLICK no dropdown ${index + 1}`, 'info');
        debugLog(`  isMobile: ${isMobile()}`, 'info');
        debugLog(`  Target: <${e.target.tagName}>`, 'info');
        debugLog(`  CurrentTarget: <${e.currentTarget.tagName}>`, 'info');
        
        if (isMobile()) {
          debugLog(`  ✅ Modo mobile - processando click`, 'success');
          e.preventDefault();
          e.stopPropagation();
          debugLog(`  preventDefault() e stopPropagation() chamados`, 'info');
          
          const wasActive = dropdown.classList.contains('active');
          debugLog(`  Estado atual: ${wasActive ? 'ABERTO' : 'FECHADO'}`, 'info');
          
          // Fechar outros dropdowns
          let closedCount = 0;
          navDropdowns.forEach((otherDropdown, otherIndex) => {
            if (otherDropdown !== dropdown && otherDropdown.classList.contains('active')) {
              otherDropdown.classList.remove('active');
              closedCount++;
              debugLog(`  Fechando dropdown ${otherIndex + 1}`, 'warning');
            }
          });
          
          if (closedCount > 0) {
            debugLog(`  ${closedCount} dropdown(s) fechado(s)`, 'info');
          }
          
          // Toggle este dropdown
          dropdown.classList.toggle('active');
          const nowActive = dropdown.classList.contains('active');
          
          debugLog(`  Novo estado: ${nowActive ? 'ABERTO' : 'FECHADO'}`, nowActive ? 'success' : 'warning');
          
          // Verificar CSS aplicado
          if (nowActive) {
            const menuDisplay = window.getComputedStyle(menu).display;
            debugLog(`  Display do menu: ${menuDisplay}`, menuDisplay === 'flex' ? 'success' : 'error');
            
            if (menuDisplay !== 'flex') {
              debugLog(`  ⚠️ PROBLEMA: Menu não está visível!`, 'error');
              debugLog(`  Verifique se existe a regra CSS:`, 'warning');
              debugLog(`  @media (max-width: 1200px) { .nav-dropdown.active .dropdown-menu { display: flex; } }`, 'warning');
            }
          }
        } else {
          debugLog(`  ℹ️ Modo desktop - usando hover (ignorando click)`, 'info');
        }
      });
      
      debugLog(`✅ Event listener adicionado ao dropdown ${index + 1}`, 'success');
      
      // Fechar dropdown ao clicar em um link interno
      const dropdownLinks = menu.querySelectorAll('a');
      dropdownLinks.forEach(function(link, linkIndex) {
        link.addEventListener('click', function(e) {
          if (isMobile()) {
            debugLog(`\n🔗 Link ${linkIndex + 1} clicado no dropdown ${index + 1}`, 'info');
            debugLog(`  Fechando dropdown...`, 'info');
            dropdown.classList.remove('active');
          }
        });
      });
      
      debugLog(`✅ Event listeners adicionados aos ${dropdownLinks.length} links`, 'success');
    });
    
    // Fechar todos os dropdowns ao clicar fora (mobile only)
    debugLog(`\nAdicionando listener global de click (fechar ao clicar fora)...`, 'info');
    
    document.addEventListener('click', function(e) {
      if (!isMobile()) return;
      
      // Verificar se o clique foi dentro de algum dropdown
      let clickedInside = false;
      let clickedDropdown = -1;
      
      navDropdowns.forEach((dropdown, index) => {
        if (dropdown.contains(e.target)) {
          clickedInside = true;
          clickedDropdown = index + 1;
        }
      });
      
      if (clickedInside) {
        debugLog(`\n🖱️ Click dentro do dropdown ${clickedDropdown}`, 'info');
      } else {
        debugLog(`\n🖱️ Click FORA dos dropdowns`, 'warning');
        
        let closedCount = 0;
        navDropdowns.forEach((dropdown, index) => {
          if (dropdown.classList.contains('active')) {
            dropdown.classList.remove('active');
            closedCount++;
            debugLog(`  Fechando dropdown ${index + 1}`, 'warning');
          }
        });
        
        if (closedCount > 0) {
          debugLog(`  ${closedCount} dropdown(s) fechado(s)`, 'info');
        }
      }
    });
    
    debugLog(`✅ Listener global adicionado`, 'success');
    
    // Fechar dropdowns ao redimensionar para desktop
    debugLog(`\nAdicionando listener de resize...`, 'info');
    
    window.addEventListener('resize', function() {
      if (!isMobile()) {
        debugLog(`\n📐 Resize para desktop - fechando todos os dropdowns`, 'warning');
        navDropdowns.forEach((dropdown, index) => {
          if (dropdown.classList.contains('active')) {
            dropdown.classList.remove('active');
            debugLog(`  Fechando dropdown ${index + 1}`, 'warning');
          }
        });
      }
    });
    
    debugLog(`✅ Listener de resize adicionado`, 'success');
    
    debugLog('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'success');
    debugLog('✅ INICIALIZAÇÃO COMPLETA!', 'success');
    debugLog('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'success');
    debugLog(`Total de dropdowns configurados: ${navDropdowns.length}`, 'success');
    debugLog(`Modo atual: ${isMobile() ? 'MOBILE' : 'DESKTOP'}`, 'info');
    debugLog('\nClique em um dropdown para ver os logs de debug!', 'info');
  });
  
  debugLog('Script dropdown-menu.js carregado', 'info');
})();
