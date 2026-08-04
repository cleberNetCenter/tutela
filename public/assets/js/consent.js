// =======================================================
// CONSENTIMENTO DE COOKIES + CARREGAMENTO DO GOOGLE ANALYTICS
// Tutela Digital™ — ARQ-107
//
// Opt-in estrito: o script do GA (gtag.js) só é criado no DOM depois
// de uma escolha "accepted" registrada por este arquivo — nunca no
// carregamento inicial da página. Enquanto não houver escolha válida
// (ou a escolha for "rejected"), nenhuma requisição de rede é feita a
// googletagmanager.com/google-analytics.com.
// =======================================================

(function () {
  if (window.__tutelaConsentInitialized) return;
  window.__tutelaConsentInitialized = true;

  const STORAGE_KEY = "cookieConsent";
  const CONSENT_TTL_DAYS = 365; // ~12 meses (padrão de mercado para CMPs)
  const GA_MEASUREMENT_ID = "G-KXVB267PYJ";

  function readConsent() {
    let raw;
    try {
      raw = localStorage.getItem(STORAGE_KEY);
    } catch (e) {
      return null; // localStorage indisponível (modo privado restrito etc.)
    }
    if (!raw) return null;
    let parsed;
    try {
      parsed = JSON.parse(raw);
    } catch (e) {
      return null;
    }
    if (!parsed || (parsed.status !== "accepted" && parsed.status !== "rejected") || !parsed.timestamp) {
      return null;
    }
    const ageMs = Date.now() - parsed.timestamp;
    if (ageMs > CONSENT_TTL_DAYS * 24 * 60 * 60 * 1000) return null;
    return parsed;
  }

  function writeConsent(status) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({ status, timestamp: Date.now() }));
    } catch (e) {
      // Se localStorage não estiver disponível, a escolha não persiste
      // entre reloads, mas continua válida para a sessão atual.
    }
  }

  function loadGA() {
    if (window.__tutelaGALoaded) return;
    window.__tutelaGALoaded = true;

    window.dataLayer = window.dataLayer || [];
    function gtag() { window.dataLayer.push(arguments); }
    window.gtag = gtag;
    gtag("js", new Date());
    // linker cobre a navegação para app.tuteladigital.com.br, presente
    // no CTA do header em todas as páginas — antes da centralização,
    // só 3 das 16 páginas com GA aplicavam esse config (inconsistência
    // pré-existente, corrigida aqui pela unificação em um único script).
    gtag("config", GA_MEASUREMENT_ID, {
      linker: { domains: ["tuteladigital.com.br", "app.tuteladigital.com.br"] },
    });

    const script = document.createElement("script");
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`;
    document.head.appendChild(script);
  }

  function init() {
    const consent = readConsent();

    if (consent && consent.status === "accepted") {
      loadGA();
      return;
    }
    if (consent && consent.status === "rejected") {
      return; // escolha válida de recusa: banner não reaparece, GA não carrega
    }

    // Sem escolha válida (primeira visita ou expirada): mostra o banner.
    const banner = document.getElementById("cookieBanner");
    if (!banner) return;
    banner.hidden = false;
    document.body.classList.add("has-cookie-banner");

    const acceptBtn = document.getElementById("cookieBannerAccept");
    const declineBtn = document.getElementById("cookieBannerDecline");

    acceptBtn?.addEventListener("click", () => {
      writeConsent("accepted");
      banner.hidden = true;
      document.body.classList.remove("has-cookie-banner");
      loadGA();
    });

    declineBtn?.addEventListener("click", () => {
      writeConsent("rejected");
      banner.hidden = true;
      document.body.classList.remove("has-cookie-banner");
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
