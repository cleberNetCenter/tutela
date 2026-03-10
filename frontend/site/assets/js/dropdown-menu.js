// =======================================================
// NAVIGATION DROPDOWNS (bridge)
// A lógica principal foi centralizada em mobile-menu.js
// para evitar listeners duplicados e conflitos touch/click.
// =======================================================

(function ensureNavigationController() {
  if (window.__tutelaNavigationControllerInitialized) {
    return;
  }

  console.warn('[dropdown] Navigation controller ainda não inicializado. Verifique a ordem dos scripts.');
})();
