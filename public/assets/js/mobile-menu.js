// =======================================================
// NAVIGATION CONTROLLER - Tutela Digital
// MPA Pura - Estável - Determinística - Produção
// =======================================================

(function initNavigationController() {
  if (window.__tutelaNavigationControllerInitialized) {
    return;
  }

  window.__tutelaNavigationControllerInitialized = true;

  const MOBILE_MAX_WIDTH = 1024;

  function isMobileViewport() {
    return window.innerWidth <= MOBILE_MAX_WIDTH;
  }

  function getHeaderElements() {
    return {
      header: document.getElementById('header'),
      nav: document.getElementById('nav'),
      menuBtn: document.querySelector('.mobile-menu-btn')
    };
  }

  function closeAllDropdowns(exceptDropdown) {
    document.querySelectorAll('.nav-dropdown.active').forEach((dropdown) => {
      if (dropdown !== exceptDropdown) {
        dropdown.classList.remove('active');
        const toggle = dropdown.querySelector('.nav-toggle');
        if (toggle) toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  function openMobileMenu() {
    const { nav, menuBtn } = getHeaderElements();
    if (!nav || !menuBtn) return;

    nav.classList.add('active');
    menuBtn.classList.add('active');
    menuBtn.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
  }

  function closeMobileMenu() {
    const { nav, menuBtn } = getHeaderElements();
    if (!nav || !menuBtn) return;

    nav.classList.remove('active');
    menuBtn.classList.remove('active');
    menuBtn.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
    closeAllDropdowns();
  }

  function toggleMobileMenu() {
    const { nav } = getHeaderElements();
    if (!nav) return;

    if (nav.classList.contains('active')) {
      closeMobileMenu();
    } else {
      openMobileMenu();
    }
  }

  function handleDocumentClick(event) {
    const target = event.target;
    const { header, nav, menuBtn } = getHeaderElements();

    if (!header || !nav || !menuBtn) return;

    // ===================================================
    // MOBILE MENU BUTTON
    // ===================================================
    if (menuBtn === target || menuBtn.contains(target)) {
      event.preventDefault();
      event.stopPropagation();
      toggleMobileMenu();
      return;
    }

    // ===================================================
    // DROPDOWN TOGGLE
    // ===================================================
    const dropdownToggle = target.closest('.nav-dropdown > .nav-toggle');
    if (dropdownToggle) {
      event.preventDefault();
      event.stopPropagation();

      const dropdown = dropdownToggle.closest('.nav-dropdown');
      if (!dropdown) return;

      const willOpen = !dropdown.classList.contains('active');

      closeAllDropdowns(dropdown);

      if (willOpen) {
        dropdown.classList.add('active');
        dropdownToggle.setAttribute('aria-expanded', 'true');
      }

      if (isMobileViewport()) {
        dropdown.scrollIntoView({ block: 'nearest' });
      }

      return;
    }
    // ===================================================
    // DROPDOWN ITEM CLICK
    // ===================================================
    const dropdownItemLink = target.closest('.dropdown-menu a');
    if (dropdownItemLink) {
      closeAllDropdowns();

      if (isMobileViewport()) {
        closeMobileMenu();
      }

      return; // Navegação natural ocorre
    }

    // ===================================================
    // NORMAL NAV LINK (não dropdown)
    // ===================================================
    const navLink = target.closest('.nav a');
    if (navLink && !navLink.closest('.nav-dropdown')) {
      if (isMobileViewport()) {
        closeMobileMenu();
      }
      return; // Navegação natural
    }

    // ===================================================
    // CLICK FORA DO HEADER
    // ===================================================
    if (!header.contains(target)) {
      closeAllDropdowns();

      if (isMobileViewport()) {
        closeMobileMenu();
      }
    }
  }

  function handleResize() {
    if (window.innerWidth > MOBILE_MAX_WIDTH) {
      document.body.style.overflow = '';

      const { nav, menuBtn } = getHeaderElements();

      if (nav) nav.classList.remove('active');
      if (menuBtn) menuBtn.classList.remove('active');

      closeAllDropdowns();
    }
  }

  function init() {
    document.addEventListener('click', handleDocumentClick);
    window.addEventListener('resize', handleResize);
    window.toggleMobileMenu = toggleMobileMenu;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }

})();
