/* =========================================================
   NAVIGATION CONTROLLER - FULL SCREEN OVERLAY
   Enterprise-grade with body scroll lock
   ========================================================= */

document.addEventListener('DOMContentLoaded', function () {

  const btn = document.querySelector('.mobile-menu-btn');
  const nav = document.getElementById('nav');

  if (!btn || !nav) {
    console.warn('Navigation elements not found');
    return;
  }

  // Mobile menu toggle with body scroll lock
  btn.addEventListener('click', function (e) {
    e.preventDefault();
    e.stopPropagation();

    const isOpen = nav.classList.toggle('mobile-open');
    btn.classList.toggle('active', isOpen);

    // Bloquear scroll do body
    document.body.style.overflow = isOpen ? 'hidden' : '';

    // Update ARIA
    btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
  });

  // Close when clicking a link inside nav
  const navLinks = nav.querySelectorAll('a');
  navLinks.forEach(link => {
    link.addEventListener('click', function() {
      nav.classList.remove('mobile-open');
      btn.classList.remove('active');
      document.body.style.overflow = '';
      btn.setAttribute('aria-expanded', 'false');
    });
  });

  // Close when clicking outside
  document.addEventListener('click', function (e) {
    if (nav.classList.contains('mobile-open')) {
      if (!nav.contains(e.target) && !btn.contains(e.target)) {
        nav.classList.remove('mobile-open');
        btn.classList.remove('active');
        document.body.style.overflow = '';
        btn.setAttribute('aria-expanded', 'false');
      }
    }
  });

  // Close on ESC key
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && nav.classList.contains('mobile-open')) {
      nav.classList.remove('mobile-open');
      btn.classList.remove('active');
      document.body.style.overflow = '';
      btn.setAttribute('aria-expanded', 'false');
    }
  });

  console.log('Navigation controller initialized (full-screen overlay version)');

});
