// =======================================================
// MOBILE MENU TOGGLE - Tutela Digital
// =======================================================

function toggleMobileMenu() {
  const { nav, btn } = getMobileMenuElements();
  
  if (!nav || !btn) return;
  
  // Toggle classes
  nav.classList.toggle('active');
  btn.classList.toggle('active');
  
  // Prevenir scroll quando menu aberto
  if (nav.classList.contains('active')) {
    document.body.style.overflow = 'hidden';
  } else {
    document.body.style.overflow = '';
  }
}

function getMobileMenuElements() {
  return {
    nav: document.getElementById('nav'),
    btn: document.querySelector('.mobile-menu-btn')
  };
}

function closeMobileMenu() {
  const { nav, btn } = getMobileMenuElements();

  if (!nav || !btn || !nav.classList.contains('active')) return;

  nav.classList.remove('active');
  btn.classList.remove('active');
  document.body.style.overflow = '';
}

function isMobileViewport() {
  return window.innerWidth <= 1200;
}

// Fechar menu ao clicar em um link
document.addEventListener('DOMContentLoaded', function() {
  const navLinks = document.querySelectorAll('.nav a');
  
  navLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      // Se for um link de dropdown, não fechar
      if (this.parentElement.classList.contains('nav-dropdown') && 
          this.classList.contains('nav-link')) {
        return;
      }
      
      // Fechar menu mobile
      closeMobileMenu();
    });
  });
  
  // Fechar menu ao clicar fora (apenas mobile)
  document.addEventListener('click', function(e) {
    const { nav, btn } = getMobileMenuElements();
    const langDropdown = document.querySelector('.lang-dropdown');
    
    if (!nav || !btn) return;
    
    // Verificar se está em mobile
    if (!isMobileViewport()) return;
    
    // Verificar se clique foi fora do nav e do botão e do menu de idiomas
    if (!nav.contains(e.target) && 
        !btn.contains(e.target) && 
        (!langDropdown || !langDropdown.contains(e.target)) &&
        nav.classList.contains('active')) {
      closeMobileMenu();
    }
  });
});

// =======================================================
// LANGUAGE DROPDOWN - Mobile Support
// =======================================================

document.addEventListener('DOMContentLoaded', function() {
  const langDropdown = document.querySelector('.lang-dropdown');
  const langToggle = document.querySelector('.lang-toggle');
  const langMenu = document.querySelector('.lang-menu');
  
  if (!langDropdown || !langToggle || !langMenu) return;
  
  // Toggle no mobile e desktop
  langToggle.addEventListener('click', function(e) {
    e.stopPropagation();
    langDropdown.classList.toggle('active');
  });
  
  // Fechar ao clicar em uma opção
  const langOptions = langMenu.querySelectorAll('.lang-option');
  langOptions.forEach(option => {
    option.addEventListener('click', function() {
      langDropdown.classList.remove('active');
    });
  });
  
  // Fechar ao clicar fora
  document.addEventListener('click', function(e) {
    if (!langDropdown.contains(e.target)) {
      langDropdown.classList.remove('active');
    }
  });
});
