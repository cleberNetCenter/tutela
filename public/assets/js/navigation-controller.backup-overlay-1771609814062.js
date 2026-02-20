/* =========================================================
   NAVIGATION CONTROLLER - ENTERPRISE FINAL
   Single Source of Truth
   ========================================================= */

document.addEventListener('DOMContentLoaded', function () {

  const btn = document.querySelector('.mobile-menu-btn');
  const nav = document.getElementById('nav');

  if (!btn || !nav) {
    console.warn('Navigation elements not found');
    return;
  }

  function openMenu() {
    nav.classList.add('mobile-open');
    btn.classList.add('active');
    btn.setAttribute('aria-expanded', 'true');
  }

  function closeMenu() {
    nav.classList.remove('mobile-open');
    btn.classList.remove('active');
    btn.setAttribute('aria-expanded', 'false');
  }

  function toggleMenu(e) {
    e.preventDefault();
    e.stopPropagation();

    if (nav.classList.contains('mobile-open')) {
      closeMenu();
    } else {
      openMenu();
    }
  }

  // Toggle via button
  btn.addEventListener('click', toggleMenu);

  // Close when clicking a link inside nav
  nav.addEventListener('click', function (e) {
    if (e.target.closest('a')) {
      closeMenu();
    }
  });

  // Close when clicking outside
  document.addEventListener('click', function (e) {
    if (!nav.contains(e.target) && !btn.contains(e.target)) {
      closeMenu();
    }
  });

  // Close on ESC key
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      closeMenu();
    }
  });

  console.log('Navigation controller initialized (enterprise version)');

});
