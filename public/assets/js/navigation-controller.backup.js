
// iOS Safari viewport fix
function setAppHeight() {
  document.documentElement.style.setProperty(
    '--app-height',
    `${window.innerHeight}px`
  );
}

window.addEventListener('resize', setAppHeight);
window.addEventListener('orientationchange', setAppHeight);
setAppHeight();

/* =========================================================
   NAVIGATION CONTROLLER - UNIFIED ARCHITECTURE
   Single source of truth for all navigation interactions
   ========================================================= */

document.addEventListener('DOMContentLoaded', function () {
// Mobile menu event delegation
document.addEventListener('click', function (e) {
  const mobileBtn = e.target.closest('.mobile-menu-btn');
  
  if (mobileBtn) {
    const nav = document.getElementById('nav');
    if (nav) {
      nav.classList.toggle('active');
      mobileBtn.classList.toggle('active');
      document.documentElement.classList.toggle('menu-open');
    }
    return;
  }

  // Close menu when clicking nav links
  const navLink = e.target.closest('.nav a');
  if (navLink) {
    const nav = document.getElementById('nav');
    if (nav) {
      nav.classList.remove('active');
      document.documentElement.classList.remove('menu-open');
    }
    const mobileBtn = document.querySelector('.mobile-menu-btn');
    if (mobileBtn) {
      mobileBtn.classList.remove('active');
    }
  }
});


  const nav = document.getElementById('nav');
  const mobileBtn = document.querySelector('.mobile-menu-btn');

  function isMobile() {
    return window.innerWidth <= 1200;
  }

  document.addEventListener('click', function (e) {

    const target = e.target;

    // MOBILE MENU BUTTON
    if (target.closest('.mobile-menu-btn')) {
      if (!nav) return;

      nav.classList.toggle('active');
      mobileBtn.classList.toggle('active');

      document.body.style.overflow =
        nav.classList.contains('active') ? 'hidden' : '';

      return;
    }

    // DROPDOWN TOGGLE (mobile only)
    const dropdownToggle = target.closest('.nav-dropdown > .nav-link');

    if (dropdownToggle && isMobile()) {
      e.preventDefault();

      const dropdown = dropdownToggle.parentElement;

      document.querySelectorAll('.nav-dropdown.active')
        .forEach(d => {
          if (d !== dropdown) d.classList.remove('active');
        });

      dropdown.classList.toggle('active');
      return;
    }

    // LANGUAGE DROPDOWN
    const langToggle = target.closest('.lang-toggle');

    if (langToggle) {
      const langDropdown = langToggle.closest('.lang-dropdown');
      langDropdown.classList.toggle('active');
      return;
    }

    // LINK INTERNO (mobile)
    if (target.closest('.nav a') && isMobile()) {
      nav.classList.remove('active');
      mobileBtn.classList.remove('active');
      
    }

    // GLOBAL CLOSE (click outside header)
    if (!target.closest('.header')) {

      if (nav) nav.classList.remove('active');
      if (mobileBtn) mobileBtn.classList.remove('active');
      

      document.querySelectorAll('.nav-dropdown.active')
        .forEach(d => d.classList.remove('active'));

      document.querySelectorAll('.lang-dropdown.active')
        .forEach(d => d.classList.remove('active'));
    }

  });

  window.addEventListener('resize', function () {
    if (!isMobile()) {
      document.querySelectorAll('.nav-dropdown.active')
        .forEach(d => d.classList.remove('active'));
    }
  });

});
