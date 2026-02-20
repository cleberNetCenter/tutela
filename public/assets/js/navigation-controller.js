/**
 * NAVIGATION CONTROLLER - UNIFIED SYSTEM
 * Single source of truth for mobile menu
 * Uses .active class only
 * Breakpoint: 1200px
 */

document.addEventListener('DOMContentLoaded', function () {
  console.log('🚀 Navigation Controller (Unified) loaded');

  const btn = document.querySelector('.mobile-menu-btn');
  const nav = document.getElementById('nav');

  if (!btn || !nav) {
    console.warn('⚠️ Mobile menu button or nav not found');
    return;
  }

  // Toggle mobile menu
  btn.addEventListener('click', function (e) {
    e.preventDefault();
    e.stopPropagation();

    nav.classList.toggle('active');
    btn.classList.toggle('active');

    const isOpen = nav.classList.contains('active');
    btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    
    console.log(`📱 Menu ${isOpen ? 'opened' : 'closed'}`);
  });

  // Close on link click
  nav.addEventListener('click', function (e) {
    if (e.target.closest('a')) {
      nav.classList.remove('active');
      btn.classList.remove('active');
      btn.setAttribute('aria-expanded', 'false');
      console.log('🔗 Menu closed (link clicked)');
    }
  });

  // Close on outside click
  document.addEventListener('click', function (e) {
    if (!nav.contains(e.target) && !btn.contains(e.target)) {
      nav.classList.remove('active');
      btn.classList.remove('active');
      btn.setAttribute('aria-expanded', 'false');
    }
  });

  // Dropdown mobile toggle
  document.addEventListener('click', function(e) {
    const dropdownLink = e.target.closest('.nav-dropdown > a');
    if (dropdownLink && window.innerWidth <= 1200) {
      e.preventDefault();
      const dropdown = dropdownLink.closest('.nav-dropdown');
      if (dropdown) {
        dropdown.classList.toggle('active');
        console.log('📂 Dropdown toggled');
      }
    }
  });

  console.log('✅ Navigation Controller initialized');
});
