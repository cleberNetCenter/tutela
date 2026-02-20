/* =========================================================
   NAVIGATION CONTROLLER - SIMPLIFIED
   No overlay, no body lock, just toggle
   ========================================================= */

document.addEventListener('DOMContentLoaded', function () {

  const btn = document.querySelector('.mobile-menu-btn');
  const nav = document.getElementById('nav');

  if (!btn || !nav) {
    console.warn('Navigation elements not found');
    return;
  }

  // Simple toggle
  btn.addEventListener('click', function (e) {
    e.preventDefault();
    e.stopPropagation();

    nav.classList.toggle('mobile-open');
    btn.classList.toggle('active');

    // Update ARIA
    const isOpen = nav.classList.contains('mobile-open');
    btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
  });

  // Close when clicking a link
  const navLinks = nav.querySelectorAll('a');
  navLinks.forEach(link => {
    link.addEventListener('click', function() {
      nav.classList.remove('mobile-open');
      btn.classList.remove('active');
      btn.setAttribute('aria-expanded', 'false');
    });
  });

  // Close when clicking outside
  document.addEventListener('click', function (e) {
    if (nav.classList.contains('mobile-open')) {
      if (!nav.contains(e.target) && !btn.contains(e.target)) {
        nav.classList.remove('mobile-open');
        btn.classList.remove('active');
        btn.setAttribute('aria-expanded', 'false');
      }
    }
  });

  // Dropdown toggle (mobile)
  document.addEventListener('click', function(e) {
    const dropdownLink = e.target.closest('.nav-dropdown > a');
    if (dropdownLink && window.innerWidth <= 900) {
      e.preventDefault();
      const dropdown = dropdownLink.closest('.nav-dropdown');
      if (dropdown) {
        dropdown.classList.toggle('active');
      }
    }
  });

  console.log('Navigation controller initialized (simplified version)');

});
