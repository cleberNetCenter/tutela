// =======================================================
// SHARED NAVIGATION – Tutela Digital (PT / EN / ES)
// Com transições suaves entre páginas
// =======================================================

const PAGE_TRANSITION_DURATION = 350; // ms (deve bater com o CSS)
const PAGE_ROUTE_MAP = {
  home: '/',
  governo: '/governo.html',
  empresas: '/empresas.html',
  pessoas: '/pessoas.html',
  'como-funciona': '/como-funciona.html',
  seguranca: '/seguranca.html',
  'preservacao-probatoria': '/legal/preservacao-probatoria-digital.html',
  institucional: '/legal/institucional.html',
  'fundamento-juridico': '/legal/fundamento-juridico.html',
  'termos-de-custodia': '/legal/termos-de-custodia.html',
  'politica-de-privacidade': '/legal/politica-de-privacidade.html'
};

function normalizePath(path) {
  if (!path || path === '/') return '/';
  return path.endsWith('/') ? path.slice(0, -1) : path;
}

function navigateTo(page) {
  const pages = document.querySelectorAll('.content');
  const current = document.querySelector('.content.active');
  const target = document.getElementById('page-' + page);

  if (!target) {
    const fallbackRoute = PAGE_ROUTE_MAP[page];
    const currentPath = normalizePath(window.location.pathname);

    if (fallbackRoute && normalizePath(fallbackRoute) !== currentPath) {
      window.location.assign(fallbackRoute);
      return;
    }

    console.warn('[navigateTo] Page not found and no redirect available:', page);
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
  const allPages = document.querySelectorAll('.content');
  if (!allPages.length) {
    return;
  }

  const hasActive = document.querySelector('.content.active');
  if (!hasActive) {
    if (document.getElementById('page-home')) {
      navigateTo('home');
      return;
    }

    allPages[0].classList.add('active');
  }
})();
