// =======================================================
// NAVIGATION DROPDOWNS - Mobile & Desktop Support
// Suporta MÚLTIPLOS dropdowns (Soluções, Base Jurídica, etc.)
// =======================================================

document.addEventListener('DOMContentLoaded', function() {
  const MOBILE_MAX_WIDTH = 1200;
  const navDropdowns = Array.from(document.querySelectorAll('.nav-dropdown'));

  function isMobile() {
    return window.innerWidth <= MOBILE_MAX_WIDTH;
  }

  function closeAllDropdowns(exceptDropdown) {
    navDropdowns.forEach((dropdown) => {
      if (dropdown !== exceptDropdown) {
        dropdown.classList.remove('active');
      }
    });
  }

  if (navDropdowns.length === 0) {
    console.log('[dropdown] Nenhum dropdown encontrado');
    return;
  }

  console.log(`[dropdown] Inicializando ${navDropdowns.length} dropdown(s)`);

  // Mapa de toggles válidos por dropdown (mesma lógica anterior: filho direto A ou .nav-link)
  const dropdownToggles = new Map();
  navDropdowns.forEach((dropdown, index) => {
    const toggle = Array.from(dropdown.children).find((el) => {
      return el.tagName === 'A' || el.classList.contains('nav-link');
    });

    if (!toggle || !dropdown.querySelector('.dropdown-menu')) {
      console.warn(`[dropdown] Dropdown ${index} incompleto`);
      return;
    }

    dropdownToggles.set(dropdown, toggle);
  });

  // Delegação no documento para manter suporte a clique fora + toggle/link interno
  document.addEventListener('click', function(e) {
    if (!isMobile()) {
      return;
    }

    const clickedDropdown = e.target.closest('.nav-dropdown');

    // Clique fora de qualquer dropdown => fecha todos
    if (!clickedDropdown) {
      closeAllDropdowns();
      return;
    }

    // Clique em link interno do menu => fechar apenas dropdown atual
    if (e.target.closest('.dropdown-menu a')) {
      clickedDropdown.classList.remove('active');
      return;
    }

    // Toggle somente no elemento de topo previamente validado
    const toggle = dropdownToggles.get(clickedDropdown);
    if (!toggle || !toggle.contains(e.target)) {
      return;
    }

    e.preventDefault();
    e.stopPropagation();

    closeAllDropdowns(clickedDropdown);
    clickedDropdown.classList.toggle('active');
  });

  // Fechar dropdowns ao redimensionar para desktop
  window.addEventListener('resize', function() {
    if (!isMobile()) {
      closeAllDropdowns();
    }
  });

  console.log('[dropdown] Inicialização completa');
});
