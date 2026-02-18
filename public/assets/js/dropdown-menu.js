
// Legal Pages Dropdown - Mobile Support
document.addEventListener('DOMContentLoaded', function() {
  const navDropdown = document.querySelector('.nav-dropdown');
  
  if (!navDropdown) return;
  
  // Only apply on mobile
  if (window.innerWidth <= 768) {
    const dropdownToggle = navDropdown.querySelector('> a');
    
    dropdownToggle.addEventListener('click', function(e) {
      e.preventDefault();
      navDropdown.classList.toggle('active');
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
      if (!navDropdown.contains(e.target)) {
        navDropdown.classList.remove('active');
      }
    });
  }
});
