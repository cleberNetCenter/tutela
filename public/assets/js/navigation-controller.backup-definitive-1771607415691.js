/* =========================================================
   MOBILE NAVIGATION CONTROLLER - ENTERPRISE GRADE
   Cross-browser compatible (Chrome, Safari iOS, Android)
   ========================================================= */

(function() {
  'use strict';

  // Dynamic viewport height for iOS Safari
  function setAppHeight() {
    const vh = window.innerHeight;
    document.documentElement.style.setProperty('--app-height', vh + 'px');
  }

  // Initialize viewport
  setAppHeight();
  window.addEventListener('resize', setAppHeight);
  window.addEventListener('orientationchange', setAppHeight);

  // Wait for DOM
  document.addEventListener('DOMContentLoaded', function() {
    const mobileBtn = document.querySelector('.mobile-menu-btn');
    const nav = document.getElementById('nav');

    if (!mobileBtn || !nav) {
      console.warn('Mobile menu elements not found');
      return;
    }

    // Single event delegation for all menu interactions
    document.addEventListener('click', function(e) {
      // Mobile menu toggle
      const btn = e.target.closest('.mobile-menu-btn');
      if (btn) {
        e.preventDefault();
        e.stopPropagation();
        
        nav.classList.toggle('active');
        btn.classList.toggle('active');
        document.documentElement.classList.toggle('menu-open');
        
        return;
      }

      // Desktop dropdown hover (desktop only)
      // Mobile dropdown click
      const dropdownLink = e.target.closest('.nav-dropdown > a');
      if (dropdownLink) {
        // On mobile, prevent default and toggle dropdown
        if (window.innerWidth <= 1200) {
          e.preventDefault();
          const dropdown = dropdownLink.closest('.nav-dropdown');
          if (dropdown) {
            dropdown.classList.toggle('active');
          }
        }
        return;
      }

      // Close menu when clicking navigation links
      const navLink = e.target.closest('.nav a');
      if (navLink && !navLink.closest('.nav-dropdown > a')) {
        if (nav.classList.contains('active')) {
          nav.classList.remove('active');
          mobileBtn.classList.remove('active');
          document.documentElement.classList.remove('menu-open');
        }
      }
    });

    console.log('Navigation controller initialized');
  });
})();
