// =======================================================
// NAVIGATION CONTROLLER - Tutela Digital
// MPA Pura - Estável - Determinística - Produção
// =======================================================

(function initNavigationController() {
  if (window.__tutelaNavigationControllerInitialized) {
    return;
  }

  window.__tutelaNavigationControllerInitialized = true;

  const MOBILE_MAX_WIDTH = 1200;

  function isMobileViewport() {
    console.log("WIDTH:", window.innerWidth);
    alert("WIDTH: " + window.innerWidth);
    return window.matchMedia(`(max-width: ${MOBILE_MAX_WIDTH}px)`).matches;
  }

  function getHeaderElements() {
    return {
      header: document.getElementById('header'),
      nav: document.getElementById('nav'),
      menuBtn: document.querySelector('.mobile-menu-btn'),
      langDropdown: document.querySelector('.lang-dropdown'),
      langToggle: document.querySelector('.lang-toggle')
    };
  }

  function closeAllDropdowns(exceptDropdown) {
    document.querySelectorAll('.nav-dropdown.active').forEach((dropdown) => {
      if (dropdown !== exceptDropdown) {
        dropdown.classList.remove('active');
      }
    });
  }

  function closeLanguageDropdown() {
    const { langDropdown } = getHeaderElements();
    if (langDropdown) {
      langDropdown.classList.remove('active');
    }
  }

  function openMobileMenu() {
    const { nav, menuBtn } = getHeaderElements();
    if (!nav || !menuBtn) return;

    nav.classList.add('active');
    menuBtn.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeMobileMenu() {
    const { nav, menuBtn } = getHeaderElements();
    if (!nav || !menuBtn) return;

    nav.classList.remove('active');
    menuBtn.classList.remove('active');
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

  function canToggleDropdown(nav) {
    if (!isMobileViewport()) {
      return true; // Desktop usa hover + clique opcional
    }

    return nav && nav.classList.contains('active');
  }

  function handleDocumentClick(event) {
    const target = event.target;
    const { header, nav, menuBtn, langDropdown, langToggle } = getHeaderElements();

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
    // LANGUAGE TOGGLE
    // ===================================================
    if (langToggle && langToggle.contains(target)) {
      event.preventDefault();
      langDropdown.classList.toggle('active');
      return;
    }

    const langOption = target.closest('.lang-option');
    if (langOption) {
      closeLanguageDropdown();
      return;
    }

    // ===================================================
    // DROPDOWN TOGGLE
    // ===================================================
    const dropdownToggle = target.closest('.nav-dropdown > a, .nav-dropdown > .nav-link');
    if (dropdownToggle) {
      const dropdown = dropdownToggle.closest('.nav-dropdown');

      if (!dropdown || !canToggleDropdown(nav)) {
        return;
      }

      if (isMobileViewport()) {
        event.preventDefault();

        const willOpen = !dropdown.classList.contains('active');
        closeAllDropdowns(dropdown);
        dropdown.classList.toggle('active', willOpen);
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
      closeLanguageDropdown();

      if (isMobileViewport()) {
        closeMobileMenu();
      }
    } else {
      // Clique dentro do header mas fora do idioma
      if (!langDropdown || !langDropdown.contains(target)) {
        closeLanguageDropdown();
      }
    }
  }

  function handleResize() {
    if (!isMobileViewport()) {
      document.body.style.overflow = '';

      const { nav, menuBtn } = getHeaderElements();

      if (nav) nav.classList.remove('active');
      if (menuBtn) menuBtn.classList.remove('active');

      closeAllDropdowns();
    }
  }

  function init() {
    alert("WIDTH: " + window.innerWidth);
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