
// Legal Pages Dropdown - Mobile Support
document.addEventListener('DOMContentLoaded', function() {
  const navDropdown = document.querySelector('.nav-dropdown');
  
  if (!navDropdown) return;
  
  const dropdownToggle = navDropdown.querySelector('> a');
  const dropdownMenu = navDropdown.querySelector('.dropdown-menu');
  
  // Function to check if we're on mobile
  function isMobile() {
    return window.innerWidth <= 768;
  }
  
  // Mobile: toggle dropdown on click
  dropdownToggle.addEventListener('click', function(e) {
    // Only prevent default on mobile
    if (isMobile()) {
      e.preventDefault();
      navDropdown.classList.toggle('active');
    }
  });
  
  // Close dropdown when clicking outside (mobile only)
  document.addEventListener('click', function(e) {
    if (isMobile() && !navDropdown.contains(e.target)) {
      navDropdown.classList.remove('active');
    }
  });
  
  // Close dropdown after clicking a link (mobile)
  const dropdownLinks = dropdownMenu.querySelectorAll('a');
  dropdownLinks.forEach(function(link) {
    link.addEventListener('click', function() {
      if (isMobile()) {
        navDropdown.classList.remove('active');
      }
    });
  });
});
