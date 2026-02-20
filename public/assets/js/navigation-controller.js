/* =========================================================
   NAVIGATION CONTROLLER - SIMPLIFIED WORKING VERSION
   Basic functionality restored
   ========================================================= */

document.addEventListener('DOMContentLoaded', function () {
  console.log('Navigation controller loaded');

  // Get elements
  const btn = document.querySelector('.mobile-menu-btn');
  const nav = document.getElementById('nav');

  if (!btn || !nav) {
    console.warn('Menu elements not found:', { btn: !!btn, nav: !!nav });
    return;
  }

  console.log('Menu elements found - ready');

  // Mobile menu toggle
  btn.addEventListener('click', function (e) {
    e.preventDefault();
    e.stopPropagation();
    
    const isActive = nav.classList.contains('active');
    
    nav.classList.toggle('active');
    btn.classList.toggle('active');
    
    console.log('Menu toggled:', !isActive ? 'opened' : 'closed');
  });

  // Close menu when clicking links
  const navLinks = nav.querySelectorAll('a');
  navLinks.forEach(link => {
    link.addEventListener('click', function() {
      nav.classList.remove('active');
      btn.classList.remove('active');
      console.log('Menu closed via link click');
    });
  });

  // Dropdown functionality (if exists)
  const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
  dropdownToggles.forEach(toggle => {
    toggle.addEventListener('click', function(e) {
      e.preventDefault();
      const dropdown = this.closest('.dropdown');
      if (dropdown) {
        dropdown.classList.toggle('active');
      }
    });
  });

  console.log('Navigation controller initialized');
});
