// =======================================================
// NAVIGATION CONTROLLER - Tutela Digital
// Estado único para menu mobile + dropdowns + idioma
// =======================================================

(function initNavigationController() {
  if (window.__tutelaNavigationControllerInitialized) {
    return;
  }

  window.__tutelaNavigationControllerInitialized = true;

  const MOBILE_MAX_WIDTH = 1200;
  const MENU_CLOSE_GUARD_MS = 300;
  const POINTER_TO_CLICK_DEDUPE_MS = 450;
  let suppressNextClickUntil = 0;
  let ignoreGlobalCloseUntil = 0;

  function isMobileViewport() {
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
    if (!nav || !menuBtn) {
      return;
    }

    nav.classList.add('active');
    menuBtn.classList.add('active');
    document.body.style.overflow = 'hidden';
    ignoreGlobalCloseUntil = Date.now() + MENU_CLOSE_GUARD_MS;
  }

  function closeMobileMenu() {
    const { nav, menuBtn } = getHeaderElements();
    if (!nav || !menuBtn) {
      return;
    }

    nav.classList.remove('active');
    menuBtn.classList.remove('active');
    document.body.style.overflow = '';
    closeAllDropdowns();
  }

  function toggleMobileMenu() {
    const { nav } = getHeaderElements();
    if (!nav) {
      return;
    }

    if (nav.classList.contains('active')) {
      closeMobileMenu();
    } else {
      openMobileMenu();
    }
  }

  function canToggleDropdownInCurrentState(nav) {
    if (!isMobileViewport()) {
      return true;
    }

    return Boolean(nav && nav.classList.contains('active'));
  }

  function handleDropdownInteraction(event) {
    if (event.type === 'pointerdown') {
      suppressNextClickUntil = Date.now() + POINTER_TO_CLICK_DEDUPE_MS;
    } else if (event.type === 'click' && Date.now() < suppressNextClickUntil) {
      return;
    }

    const target = event.target;
    const { header, nav, menuBtn, langDropdown, langToggle } = getHeaderElements();

    if (!header || !nav || !menuBtn) {
      return;
    }

    if (menuBtn.contains(target)) {
      return;
    }

    if (langToggle && langToggle.contains(target)) {
      event.preventDefault();
      event.stopPropagation();
      langDropdown.classList.toggle('active');
      return;
    }

    const langOption = target.closest('.lang-option');
    if (langOption) {
      closeLanguageDropdown();
      return;
    }

    const dropdownToggle = target.closest('.nav-dropdown > a, .nav-dropdown > .nav-link');
    if (dropdownToggle) {
      const dropdown = dropdownToggle.closest('.nav-dropdown');
      if (!dropdown || !canToggleDropdownInCurrentState(nav)) {
        return;
      }

      event.preventDefault();
      const willOpen = !dropdown.classList.contains('active');
      closeAllDropdowns(dropdown);
      dropdown.classList.toggle('active', willOpen);
      return;
    }

    const dropdownItemLink = target.closest('.dropdown-menu a');
    if (dropdownItemLink) {
      closeAllDropdowns();
      if (isMobileViewport()) {
        closeMobileMenu();
      }
      return;
    }

    const navLink = target.closest('.nav a');
    if (navLink && !navLink.closest('.nav-dropdown')) {
      if (isMobileViewport()) {
        closeMobileMenu();
      }
      return;
    }

    const clickedInsideHeader = header.contains(target);
    if (!clickedInsideHeader) {
      if (isMobileViewport() && nav.classList.contains('active') && Date.now() < ignoreGlobalCloseUntil) {
        return;
      }

      closeAllDropdowns();
      closeLanguageDropdown();

      if (isMobileViewport()) {
        closeMobileMenu();
      }

      return;
    }

    if (!langDropdown || !langDropdown.contains(target)) {
      closeLanguageDropdown();
    }
  }

  function handleResize() {
    if (!isMobileViewport()) {
      document.body.style.overflow = '';
      const { nav, menuBtn } = getHeaderElements();
      if (nav) {
        nav.classList.remove('active');
      }
      if (menuBtn) {
        menuBtn.classList.remove('active');
      }
      closeAllDropdowns();
    }
  }

  function init() {
    document.addEventListener('pointerdown', handleDropdownInteraction);
    document.addEventListener('click', handleDropdownInteraction);
    window.addEventListener('resize', handleResize);
    window.toggleMobileMenu = toggleMobileMenu;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();
