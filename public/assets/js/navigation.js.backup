// =======================================================
// SHARED NAVIGATION – Tutela Digital (PT / EN / ES)
// Com transições suaves entre páginas
// =======================================================

const PAGE_TRANSITION_DURATION = 350; // ms (deve bater com o CSS)

function navigateTo(page) {
  const pages = document.querySelectorAll('.page');
  const current = document.querySelector('.page.active');
  const target = document.getElementById('page-' + page);

  if (!target) {
    console.warn('[navigateTo] Page not found:', page);
    return;
  }

  /* =========================================
     DESATIVA PÁGINA ATUAL (fade out)
     ========================================= */
  if (current && current !== target) {
    current.classList.remove('active');
  }

  /* =========================================
     ATIVA NOVA PÁGINA (fade in)
     ========================================= */
  setTimeout(() => {
    pages.forEach(p => p.classList.remove('active'));
    target.classList.add('active');

    /* Atualiza estado do menu */
    document.querySelectorAll('.nav-link').forEach(link => {
      link.classList.toggle(
        'active',
        link.dataset.page === page
      );
    });

    /* Scroll sempre para o topo */
    window.scrollTo({
      top: 0,
      left: 0,
      behavior: 'smooth'
    });

  }, current ? PAGE_TRANSITION_DURATION : 0);
}

// =======================================================
// INIT (fallback seguro)
// =======================================================

(function initNavigation() {
  const hasActive = document.querySelector('.page.active');
  if (!hasActive) {
    navigateTo('home');
  }
})();
