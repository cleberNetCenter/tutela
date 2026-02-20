// =======================================================
// MOBILE MENU + LANGUAGE DROPDOWN - Tutela Digital
// =======================================================

(function initHeaderInteractions() {
  const MOBILE_MAX_WIDTH = 1200;

  function getMobileMenuElements() {
    return {
      nav: document.getElementById('nav'),
      btn: document.querySelector('.mobile-menu-btn')
    };
  }

  function isMobileViewport() {
    return window.innerWidth <= MOBILE_MAX_WIDTH;
  }

  function closeMobileMenu() {
    const { nav, btn } = getMobileMenuElements();

    if (!nav || !btn || !nav.classList.contains('active')) {
      return;
    }

    nav.classList.remove('active');
    btn.classList.remove('active');
    document.body.style.overflow = '';
  }

  function toggleMobileMenu() {
    const { nav, btn } = getMobileMenuElements();

    if (!nav || !btn) {
      return;
    }

    nav.classList.toggle('active');
    btn.classList.toggle('active');
    document.body.style.overflow = nav.classList.contains('active') ? 'hidden' : '';
  }

  function initMobileMenuLinks() {
    const navLinks = document.querySelectorAll('.nav a');

    navLinks.forEach((link) => {
      link.addEventListener('click', function onNavClick() {
        const isDropdownToggle = this.parentElement.classList.contains('nav-dropdown') &&
          this.classList.contains('nav-link');

        if (isDropdownToggle) {
          return;
        }

        closeMobileMenu();
      });
    });

    document.addEventListener('click', function onDocumentClick(event) {
      const { nav, btn } = getMobileMenuElements();
      const langDropdown = document.querySelector('.lang-dropdown');

      if (!nav || !btn || !isMobileViewport()) {
        return;
      }

      const clickedOutsideHeaderControls =
        !nav.contains(event.target) &&
        !btn.contains(event.target) &&
        (!langDropdown || !langDropdown.contains(event.target));

      if (clickedOutsideHeaderControls && nav.classList.contains('active')) {
        closeMobileMenu();
      }
    });
  }

  function initLanguageDropdown() {
    const langDropdown = document.querySelector('.lang-dropdown');
    const langToggle = document.querySelector('.lang-toggle');
    const langMenu = document.querySelector('.lang-menu');

    if (!langDropdown || !langToggle || !langMenu) {
      return;
    }

    langToggle.addEventListener('click', function onLangToggle(event) {
      event.stopPropagation();
      langDropdown.classList.toggle('active');
    });

    const langOptions = langMenu.querySelectorAll('.lang-option');
    langOptions.forEach((option) => {
      option.addEventListener('click', function onLangOptionClick() {
        langDropdown.classList.remove('active');
      });
    });

    document.addEventListener('click', function onDocumentLangClick(event) {
      if (!langDropdown.contains(event.target)) {
        langDropdown.classList.remove('active');
      }
    });
  }

  document.addEventListener('DOMContentLoaded', function onReady() {
    initMobileMenuLinks();
    initLanguageDropdown();
  });

  // Mantém compatibilidade com onclick="toggleMobileMenu()" existente no HTML.
  window.toggleMobileMenu = toggleMobileMenu;
})();
