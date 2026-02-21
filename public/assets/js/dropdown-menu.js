// =======================================================
// NAVIGATION DROPDOWNS - Mobile & Desktop Support
// Suporta MÚLTIPLOS dropdowns (Soluções, Base Jurídica, etc.)
// =======================================================

document.addEventListener('DOMContentLoaded', function() {
  if (window.__tutelaDropdownMenuInitialized) {
    return;
  }

  window.__tutelaDropdownMenuInitialized = true;

  const MOBILE_MAX_WIDTH = 1200;
  const navDropdowns = Array.from(document.querySelectorAll('.nav-dropdown'));
  let lastTouchLikeEventAt = 0;

  function isMobile() {
    return window.matchMedia(`(max-width: ${MOBILE_MAX_WIDTH}px)`).matches;
  }

  function isNavigableHref(href) {
    if (!href) {
      return false;
    }

    const normalizedHref = href.trim();
    return normalizedHref !== '#' && !normalizedHref.toLowerCase().startsWith('javascript:');
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

  function handleDropdownInteraction(e) {
    if (!isMobile()) {
      return;
    }

    const clickedDropdown = e.target.closest('.nav-dropdown');

    if (!clickedDropdown) {
      closeAllDropdowns();
      return;
    }

    if (e.target.closest('.dropdown-menu a')) {
      clickedDropdown.classList.remove('active');
      return;
    }

    const toggle = dropdownToggles.get(clickedDropdown);
    if (!toggle || !toggle.contains(e.target)) {
      return;
    }

    const isOpen = clickedDropdown.classList.contains('active');
    const href = toggle.getAttribute('href');

    if (!isOpen) {
      e.preventDefault();
      closeAllDropdowns(clickedDropdown);
      clickedDropdown.classList.add('active');
      return;
    }

    if (!isNavigableHref(href)) {
      e.preventDefault();
      clickedDropdown.classList.remove('active');
      return;
    }

    closeAllDropdowns();
  }

  document.addEventListener('pointerdown', function(e) {
    if (e.pointerType === 'mouse') {
      return;
    }

    lastTouchLikeEventAt = Date.now();
    handleDropdownInteraction(e);
  });

  document.addEventListener('click', function(e) {
    if (Date.now() - lastTouchLikeEventAt < 700) {
      return;
    }

    handleDropdownInteraction(e);
  });

  // Fechar dropdowns ao redimensionar para desktop
  window.addEventListener('resize', function() {
    if (!isMobile()) {
      closeAllDropdowns();
    }
  });

  console.log('[dropdown] Inicialização completa');
});
