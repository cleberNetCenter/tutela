
// =======================================================
// NAVIGATION DROPDOWNS - Mobile & Desktop Support
// Suporta MÚLTIPLOS dropdowns (Soluções, Base Jurídica, etc.)
// =======================================================

document.addEventListener('DOMContentLoaded', function() {
  
  // Função para verificar se está em mobile
  function isMobile() {
    return window.innerWidth <= 1200;
  }
  
  // Selecionar TODOS os dropdowns
  const navDropdowns = document.querySelectorAll('.nav-dropdown');
  
  if (navDropdowns.length === 0) {
    console.log('[dropdown] Nenhum dropdown encontrado');
    return;
  }
  
  console.log(`[dropdown] Inicializando ${navDropdowns.length} dropdown(s)`);
  
  // Configurar cada dropdown individualmente
  navDropdowns.forEach((dropdown, index) => {
    const toggle = dropdown.querySelector('> a, > .nav-link');
    const menu = dropdown.querySelector('.dropdown-menu');
    
    if (!toggle || !menu) {
      console.warn(`[dropdown] Dropdown ${index} incompleto`);
      return;
    }
    
    // Mobile: toggle dropdown ao clicar
    toggle.addEventListener('click', function(e) {
      if (isMobile()) {
        e.preventDefault();
        e.stopPropagation();
        
        // Fechar outros dropdowns
        navDropdowns.forEach((otherDropdown) => {
          if (otherDropdown !== dropdown) {
            otherDropdown.classList.remove('active');
          }
        });
        
        // Toggle este dropdown
        dropdown.classList.toggle('active');
        
        console.log(`[dropdown] Toggle dropdown ${index}: ${dropdown.classList.contains('active')}`);
      }
    });
    
    // Fechar dropdown ao clicar em um link interno
    const dropdownLinks = menu.querySelectorAll('a');
    dropdownLinks.forEach(function(link) {
      link.addEventListener('click', function() {
        if (isMobile()) {
          dropdown.classList.remove('active');
          console.log(`[dropdown] Link clicado, fechando dropdown ${index}`);
        }
      });
    });
  });
  
  // Fechar todos os dropdowns ao clicar fora (mobile only)
  document.addEventListener('click', function(e) {
    if (!isMobile()) return;
    
    // Verificar se o clique foi dentro de algum dropdown
    let clickedInside = false;
    navDropdowns.forEach(dropdown => {
      if (dropdown.contains(e.target)) {
        clickedInside = true;
      }
    });
    
    // Se clicou fora, fechar todos
    if (!clickedInside) {
      navDropdowns.forEach(dropdown => {
        dropdown.classList.remove('active');
      });
      console.log('[dropdown] Clique fora, fechando todos os dropdowns');
    }
  });
  
  // Fechar dropdowns ao redimensionar para desktop
  window.addEventListener('resize', function() {
    if (!isMobile()) {
      navDropdowns.forEach(dropdown => {
        dropdown.classList.remove('active');
      });
    }
  });
  
  console.log('[dropdown] Inicialização completa');
});
